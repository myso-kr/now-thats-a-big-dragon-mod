//! Opens the windows through which the mod reaches game state.
//!
//! There are three bridges, and they are different in kind:
//!   store     wraps the zustand persist factory to expose the per-slot stores
//!   dispatch  grabs the React context dispatch (the game's own command path)
//!   stats     exposes the per-unit generation table the game already computes

use regex::Regex;

/// The identifier a pattern matched, if it matched at all.
pub struct Found {
    pub id: Option<String>,
}

/// Escape regex metacharacters. Minified identifiers commonly contain `$`, and left
/// unescaped it is read as an end anchor, so the pattern never matches anything.
fn quote(id: &str) -> String {
    let mut s = String::with_capacity(id.len() * 2);
    for c in id.chars() {
        if ".*+?^$(){}|[]\\".contains(c) {
            s.push('\\');
        }
        s.push(c);
    }
    s
}

/// Of all the `[,X]=Y.useReducer(` sites, take only the one handed to a Provider value.
pub fn dispatch(src: &str) -> Found {
    let pat = Regex::new(r"\[,([A-Za-z0-9_$]+)\]=[A-Za-z0-9_$]+\.useReducer\(").unwrap();
    for m in pat.captures_iter(src) {
        let id = &m[1];
        let whole = m.get(0).unwrap();
        let window_end = (whole.start() + 900).min(src.len());
        let confirm = Regex::new(&format!(r"\.Provider,\{{value:{}[,}}]", quote(id))).unwrap();
        if confirm.is_match(&src[whole.start()..window_end]) {
            return Found {
                id: Some(id.to_owned()),
            };
        }
    }
    Found { id: None }
}

/// Find the generation table by its `X={total:{},click:{},warrior:{}` signature.
pub fn stats(src: &str) -> Found {
    let pat = Regex::new(r"([A-Za-z0-9_$]+)=\{total:\{\},click:\{\},warrior:\{\}").unwrap();
    match pat.captures(src) {
        Some(c) => Found {
            id: Some(c[1].to_owned()),
        },
        None => Found { id: None },
    }
}

/// Where a matched pattern's identifier appears, plus the patched code.
pub struct Injected {
    pub code: String,
    pub id: Option<String>,
}

/// Index of the ')' matching the '(' at `open`, ignoring brackets inside strings.
fn close_paren(src: &str, open: usize) -> Option<usize> {
    crate::patch::scan::balanced(src, open).map(|e| e - 1)
}

/// Hand the React context dispatch to `window.__bd_dispatch`.
///
/// Game commands (buying, firing inspiration, changing level) leave only through the
/// context dispatch. The Provider passes useReducer's dispatch as its value, so we
/// intercept it there. Going through it rather than writing stores directly means
/// the game's own events, unlocks and achievements all still fire.
pub fn inject_dispatch(src: &str) -> Injected {
    let found = dispatch(src);
    let Some(id) = found.id.clone() else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    let pat = Regex::new(&format!(
        r"\[,{}\]=[A-Za-z0-9_$]+\.useReducer\(",
        quote(&id)
    ))
    .unwrap();
    let Some(m) = pat.find(src) else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    let open = m.end() - 1; // the '(' of useReducer(
    let Some(close) = close_paren(src, open) else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    if src.as_bytes().get(close + 1) != Some(&b';') {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    }
    let at = close + 2;
    // The catch parameter is named apart so it cannot shadow the dispatch identifier.
    let code = format!("try{{window.__bd_dispatch={id};}}catch(_bd){{}}");
    let mut out = String::with_capacity(src.len() + code.len());
    out.push_str(&src[..at]);
    out.push_str(&code);
    out.push_str(&src[at..]);
    Injected {
        code: out,
        id: Some(id),
    }
}

/// Expose the per-unit generation table the game already computes.
///
/// It holds effective output with every upgrade and inspiration multiplier already
/// applied, so reading it saves autoplay from reimplementing the damage formulas.
pub fn inject_stats(src: &str) -> Injected {
    let found = stats(src);
    let Some(id) = found.id.clone() else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    let Some(at) = src.find(&format!("{id}={{total:{{}},click:{{}},warrior:{{}}")) else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    let brace = at + id.len() + 1;
    let Some(end) = crate::patch::scan::balanced(src, brace) else {
        return Injected {
            code: src.to_owned(),
            id: None,
        };
    };
    let code = format!(
        ",__bd_stats_bridge=(()=>{{try{{window.__bd_stats={id};}}catch(_bd){{}}return 0;}})()"
    );
    let mut out = String::with_capacity(src.len() + code.len());
    out.push_str(&src[..end]);
    out.push_str(&code);
    out.push_str(&src[end..]);
    Injected {
        code: out,
        id: Some(id),
    }
}

/// Store identifiers, found by meaning rather than by name so minification cannot
/// break them.
const STORE_PATTERNS: [(&str, &str); 6] = [
    ("currency", r"([A-Za-z0-9_$]+)\.getState\(\)\.setGold\("),
    ("generators", r"([A-Za-z0-9_$]+)\.getState\(\)\.generators"),
    ("upgrades", r"([A-Za-z0-9_$]+)\.getState\(\)\.upgrades"),
    (
        "dragon",
        r"([A-Za-z0-9_$]+)\.getState\(\)\.sync\(\{dragonHealth",
    ),
    ("combat", r"([A-Za-z0-9_$]+)\.getState\(\)\.enterCombat\("),
    ("levels", r"([A-Za-z0-9_$]+)\.getState\(\)\.beatenLevels"),
];

/// The values actually in play sit in per-slot stores, which the game collects into
/// one `[{store, baseKey}]` array. Grabbing that array reaches the active stores
/// without needing to know the slot name.
const SLOT_REGISTRY: &str = r"([A-Za-z0-9_$]+)\.push\(\{store:[A-Za-z0-9_$]+,baseKey:";

pub struct StoreBridge {
    pub code: String,
    pub wrapped: Option<String>,
    pub found: Vec<String>,
}

/// Wrap the persist-store factory so each store registers itself by saveKey.
///
/// The game's real state lives in module-scope zustand stores, not in the
/// `global_game_store` on window - that one only mirrors variables for Ink dialogue,
/// and gold written there is overwritten on the next tick.
fn wrap_store_factory(src: &str) -> (String, Option<String>) {
    let Some(anchor) = src.find("savePrefix") else {
        return (src.to_owned(), None);
    };
    let Some(head) = src[..anchor].rfind("function ") else {
        return (src.to_owned(), None);
    };
    let sig = Regex::new(r"^function\s+([A-Za-z0-9_$]+)\s*\(([^)]*)\)\s*\{").unwrap();
    let Some(m) = sig.captures(&src[head..anchor]) else {
        return (src.to_owned(), None);
    };
    let name = m.get(1).unwrap().as_str().to_owned();
    let args = m.get(2).unwrap().as_str().to_owned();
    let brace_at = head + m.get(0).unwrap().end() - 1;
    let Some(body_end) = crate::patch::scan::balanced(src, brace_at) else {
        return (src.to_owned(), None);
    };

    let renamed = format!("function {name}$bd({args}){{");
    let wrapper = format!(
        "function {name}(...a){{const s={name}$bd(...a);\
         try{{const k=a[0]&&a[0].saveKey;if(k){{(window.__bd_stores||(window.__bd_stores={{}}))[k]=s;}}}}catch(e){{}}\
         return s;}}"
    );
    let mut out = String::with_capacity(src.len() + wrapper.len() + 8);
    out.push_str(&src[..head]);
    out.push_str(&renamed);
    out.push_str(&src[brace_at + 1..body_end]);
    out.push_str(&wrapper);
    out.push_str(&src[body_end..]);
    (out, Some(name))
}

/// Export the module-scope store constants onto window at the end of the module.
fn append_store_epilogue(src: &str) -> (String, Vec<String>) {
    let mut found = Vec::new();
    let mut parts = Vec::new();

    if let Some(c) = Regex::new(SLOT_REGISTRY).unwrap().captures(src) {
        let id = &c[1];
        found.push("__slots".to_owned());
        parts.push(format!("try{{window.__bd_slotStores={id};}}catch(e){{}}"));
    }
    for (key, pat) in STORE_PATTERNS {
        let Some(c) = Regex::new(pat).unwrap().captures(src) else {
            continue;
        };
        let id = &c[1];
        found.push(key.to_owned());
        // Each gets its own try, so one out-of-scope name cannot take the rest down.
        parts.push(format!(
            "try{{(window.__bd_stores||(window.__bd_stores={{}})).{key}={id};}}catch(e){{}}"
        ));
    }
    if parts.is_empty() {
        return (src.to_owned(), found);
    }
    // The leading newline matters: the bundle's last line may be a `//#` comment,
    // and appending to it would comment the whole epilogue out.
    (format!("{src}\n;{}\n", parts.join("")), found)
}

pub fn inject_stores(src: &str) -> StoreBridge {
    let (a, wrapped) = wrap_store_factory(src);
    let (code, found) = append_store_epilogue(&a);
    StoreBridge {
        code,
        wrapped,
        found,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn app(id: &str) -> String {
        format!(
            "function App(){{const[,{id}]=R.useReducer(rd,init);\
             return J(C.Provider,{{value:{id},children:null}});}}"
        )
    }

    #[test]
    fn finds_an_ordinary_identifier() {
        assert_eq!(dispatch(&app("dp")).id.as_deref(), Some("dp"));
    }

    #[test]
    fn finds_an_identifier_containing_a_dollar_sign() {
        // Without escaping, `$` becomes an end anchor and nothing ever matches.
        assert_eq!(dispatch(&app("d$p")).id.as_deref(), Some("d$p"));
        assert_eq!(dispatch(&app("$")).id.as_deref(), Some("$"));
    }

    #[test]
    fn skips_a_use_reducer_that_does_not_reach_a_provider() {
        let src = "const[,x]=R.useReducer(a,b);const y=1;";
        assert_eq!(dispatch(src).id, None);
    }

    #[test]
    fn finds_the_generation_table() {
        let src = "var Pi={total:{},click:{},warrior:{},wizard:{}};";
        assert_eq!(stats(src).id.as_deref(), Some("Pi"));
    }

    #[test]
    fn escapes_metacharacters() {
        assert_eq!(quote("d$p"), r"d\$p");
        assert_eq!(quote("ab"), "ab");
    }
}

//! Slots a bundled font in beside each original pixel font.
//!
//! Which fonts, for which language, is data — locale/languages.json — so this file
//! knows nothing about any particular language.
//!
//! The game's fonts are pixel fonts, so "how many units is one design pixel" is a
//! fixed number. Ours only looks like the same font if its pixel grid is matched to
//! that, which is what size-adjust does. But size-adjust scales the metrics along
//! with the grid, so ascent and descent overrides have to be divided by the same
//! ratio to keep line height identical to the original.
//!
//! Mirrors patch/css.js.

const GENERIC_FAMILIES: &[&str] = &[
    "sans-serif",
    "serif",
    "monospace",
    "cursive",
    "fantasy",
    "system-ui",
];

/// A family name with a space or a non-identifier character has to be quoted; a
/// generic keyword must not be.
fn quote_family(name: &str) -> String {
    if GENERIC_FAMILIES.contains(&name) {
        return name.to_owned();
    }
    let plain = !name.is_empty()
        && name.starts_with(|c: char| c.is_ascii_alphabetic())
        && name
            .chars()
            .all(|c| c.is_ascii_alphanumeric() || c == '_' || c == '-');
    if plain {
        name.to_owned()
    } else {
        format!("'{name}'")
    }
}

use crate::language::Font;

#[derive(Debug, Default)]
pub struct Report {
    pub faces: usize,
    pub stacks: usize,
    /// One per language whose font the page can switch to.
    pub rules: usize,
}

/// A percentage the way the Node reference writes it: four decimals at most, with
/// trailing zeros dropped. The two have to agree to the byte.
fn pct(n: f64) -> String {
    let s = format!("{n:.4}");
    let s = if s.contains('.') {
        s.trim_end_matches('0').trim_end_matches('.')
    } else {
        &s
    };
    s.to_owned()
}

fn face(f: &Font) -> String {
    let ratio = f.px_per_em / f.base_px_per_em;

    // Pin the line height to the original font's, so a taller glyph does not change
    // the UI's line spacing. size-adjust scales the overrides along with the glyphs,
    // so they are divided by the same ratio to cancel that out.
    //
    // A font that declares no overrides gets none: emitting a default here would pin
    // its line box to a number nobody chose.
    let metrics = match (f.ascent_override, f.descent_override) {
        (Some(a), Some(d)) => format!(
            "ascent-override:{}%;descent-override:{}%;line-gap-override:0%;",
            pct(a / ratio),
            pct(d / ratio),
        ),
        _ => String::new(),
    };
    format!(
        // The stylesheet lives under assets/, so the URL has to climb out of it.
        "@font-face{{font-family:{};src:url(../{}) format(\"woff2\");\
         font-display:block;{metrics}size-adjust:{}%}}",
        f.family,
        f.url,
        pct(ratio * 100.0),
    )
}

/// The two families the game itself declares. Everything else in the stylesheet is
/// somebody else's font.
const BASE_FAMILIES: [&str; 2] = ["everyday_standard", "high_birth"];

/// The settings screen lays the language flags out in one non-wrapping row. The game
/// ships five; we add one per bundled language, and the row simply grows — pushing
/// the dialog wider than the window. Letting it wrap costs nothing at five and is the
/// only thing that works at twenty.
///
/// `min-width:0` is the part that does it: a flex item defaults to its content's
/// minimum width, so `flex-wrap` alone would still refuse to shrink.
const LANGUAGE_ROW: &str = ".language-container{align-items:flex-start}.language-flags{flex-wrap:wrap;min-width:0;flex:1 1 auto;row-gap:8px}";

/// One language as the stylesheet needs it.
pub struct CssLang<'a> {
    pub lang: &'a str,
    pub fonts: &'a [Font],
    pub fallback: &'a [String],
}

/// Slot every bundled language's font in, and let the page pick by its own `lang`.
///
/// Every language offered, not only the one being applied. The settings screen lists
/// them all and the game switches without reloading, so a stylesheet naming one font
/// keeps that font after the player switches: Korean to Simplified Chinese used to keep
/// Galmuri, which has none of the simplified characters, and drew 269 empty boxes.
///
/// The game funnels every family through `--font-primary` and `--font-heading`, and it
/// already sets `document.documentElement.lang` and updates it on `languageChanged`.
/// One `html[lang="xx"]` rule per language redefines those two, and the switch takes
/// effect the moment the player makes it.
///
/// Mirrors `patch/css.js`; `tests/bundle.rs` compares the two byte for byte.
pub fn patch_all(src: &str, langs: &[CssLang]) -> (String, Report) {
    let mut rep = Report::default();
    let mut faces = String::new();
    let mut rules = String::new();

    for l in langs {
        let sys: Vec<String> = l.fallback.iter().map(|f| quote_family(f)).collect();
        let sys = sys.join(", ");
        let mut mine: Vec<&Font> = Vec::new();
        for f in l.fonts {
            faces.push_str(&face(f));
            rep.faces += 1;
            mine.push(f);
        }
        if mine.is_empty() && sys.is_empty() {
            continue;
        }
        let stack = |base: &str| {
            let mut parts = vec![base.to_owned()];
            if let Some(f) = mine.iter().find(|f| f.replaces == base) {
                parts.push(f.family.clone());
            }
            if !sys.is_empty() {
                parts.push(sys.clone());
            }
            parts.join(", ")
        };
        rules.push_str(&format!(
            "html[lang={:?}]{{--font-primary:{};--font-heading:{}}}",
            l.lang,
            stack(BASE_FAMILIES[0]),
            stack(BASE_FAMILIES[1])
        ));
        rep.rules += 1;
    }

    // Two places keep the bare name: inside an `@font-face`, where it *is* the font
    // being defined, and inside a `--font-primary:` declaration, which the rules above
    // override and which would otherwise refer to itself. Everything else that names a
    // family directly becomes the variable, so the per-language rules govern all of it.
    // With no language rule to govern them, funnelling the direct declarations through
    // the variables would change the stylesheet for no gain - and patching with nothing
    // to add has to leave it byte for byte as it was.
    let body_out = if rep.rules == 0 {
        src.to_owned()
    } else {
        rewrite_named(src, &mut rep)
    };

    // @charset has to stay on the first line, so insert after it.
    let insert_at = if body_out.starts_with("@charset") {
        body_out.find(';').map(|i| i + 1).unwrap_or(0)
    } else {
        0
    };
    let row = if rep.faces > 0 || rep.rules > 0 {
        LANGUAGE_ROW
    } else {
        ""
    };
    let mut out = String::with_capacity(body_out.len() + faces.len() + rules.len() + 64);
    out.push_str(&body_out[..insert_at]);
    out.push_str(&faces);
    out.push_str(row);
    out.push_str(&body_out[insert_at..]);
    // The language rules go last: the game declares `--font-primary` on a selector of
    // its own, and `html[lang="xx"]` only outranks it when it is more specific, which
    // is not something to bet the whole font switch on. Last one wins on a tie.
    out.push_str(&rules);
    (out, rep)
}

/// Turn a family named directly into the variable it belongs to.
fn rewrite_named(src: &str, rep: &mut Report) -> String {
    // The @font-face blocks are collected up front so their own names can be skipped.
    let mut skip: Vec<(usize, usize)> = Vec::new();
    let mut from = 0;
    while let Some(rel) = src[from..].find("@font-face") {
        let at = from + rel;
        if let Some(brace) = src[at..].find('{') {
            if let Some(end) = crate::patch::scan::balanced(src, at + brace) {
                skip.push((at, end));
                from = end;
                continue;
            }
        }
        from = at + "@font-face".len();
    }
    let in_skip = |i: usize| skip.iter().any(|&(a, b)| i >= a && i < b);

    let bytes = src.as_bytes();
    let mut out = String::with_capacity(src.len() + 128);
    let mut cursor = 0usize;
    let mut i = 0usize;
    while i < src.len() {
        let quote = match bytes.get(i) {
            Some(&q @ (b'"' | b'\'')) => Some(q),
            _ => None,
        };
        let name_at = if quote.is_some() { i + 1 } else { i };
        let hit = BASE_FAMILIES.iter().find(|name| {
            if in_skip(i) || !src[name_at..].starts_with(**name) {
                return false;
            }
            let after = bytes.get(name_at + name.len());
            match quote {
                Some(q) => after == Some(&q),
                None => !matches!(after, Some(c) if c.is_ascii_alphanumeric() || *c == b'_' || *c == b'-'),
            }
        });
        let Some(name) = hit else {
            i += 1;
            continue;
        };
        let end = name_at + name.len() + usize::from(quote.is_some());

        // A declaration of the variable itself is left alone; the rules override it.
        //
        // Skipping past the whole thing, not one byte. Node's regex consumes the
        // quotes with the name, so it never looks inside again; stepping one byte on
        // lands on the letter after the opening quote, matches the bare name there,
        // and rewrites the inside of a string Node left alone.
        let before = src[..i].trim_end();
        if before.ends_with("--font-primary:")
            || before.ends_with("--font-heading:")
            || before.ends_with("--font-primary: \"")
            || before.ends_with("--font-heading: \"")
        {
            i = end;
            continue;
        }
        out.push_str(&src[cursor..i]);
        out.push_str(if *name == BASE_FAMILIES[0] {
            "var(--font-primary)"
        } else {
            "var(--font-heading)"
        });
        i = end;
        cursor = i;
        rep.stacks += 1;
    }
    out.push_str(&src[cursor..]);
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    /// One language, the shape the tests were written against.
    fn one<'a>(fonts: &'a [Font], fallback: &'a [String]) -> Vec<CssLang<'a>> {
        vec![CssLang {
            lang: "ko",
            fonts,
            fallback,
        }]
    }

    /// The Korean fonts, as the shipped catalogue defines them.
    fn ko_fonts() -> Vec<Font> {
        let cat = crate::assets::catalogue().expect("locale/languages.json");
        cat.languages["ko"].fonts.clone()
    }

    fn fallback() -> Vec<String> {
        crate::assets::catalogue().unwrap().languages["ko"]
            .fallback
            .clone()
    }

    /// Patch with the Korean font set, which is what every case here is about.
    fn patch_ko(src: &str) -> (String, Report) {
        patch_all(src, &one(&ko_fonts(), &fallback()))
    }

    #[test]
    fn a_usage_becomes_the_variable_and_a_declaration_is_left_alone() {
        // The stack lives in the per-language rule now. A usage that named the family
        // directly is routed through the variable so that rule governs it too; the
        // @font-face name *is* the font, and the variable's own declaration would
        // otherwise refer to itself.
        let css = "@font-face{font-family:everyday_standard;src:url(a.woff2)}                   :root{--font-primary: \"everyday_standard\"}                   .t{font-family:everyday_standard}";
        let (out, rep) = patch_ko(css);
        assert_eq!(rep.faces, 2, "two Korean faces are added");
        assert_eq!(
            rep.stacks, 1,
            "the usage, and neither the face nor the declaration"
        );
        assert!(
            out.contains(".t{font-family:var(--font-primary)}"),
            "got: {out}"
        );
        assert!(
            out.contains("@font-face{font-family:everyday_standard;"),
            "got: {out}"
        );
        assert!(
            out.contains("--font-primary: \"everyday_standard\""),
            "got: {out}"
        );
    }

    #[test]
    fn the_original_font_stays_first() {
        // Latin glyphs must keep coming from the game's own font; ours only catches
        // what the original has no glyph for.
        let (out, _) = patch_ko(".t{font-family:everyday_standard}");
        let decl = &out[out.find(".t{font-family:").unwrap()..];
        assert!(
            decl.find("everyday_standard").unwrap() < decl.find("bd_ko_body").unwrap(),
            "the original has to precede ours"
        );
    }

    #[test]
    fn the_stack_is_never_wrapped_in_one_pair_of_quotes() {
        // Wrapping the whole stack in one pair makes it a single family name that does
        // not exist, so no font applies at all. That was a real bug; it used to be
        // possible at the usage sites and now it is only possible in the language rule,
        // which is where it is guarded.
        let (out, _) = patch_ko(".t{--font-primary:\"everyday_standard\"}");
        let rule = &out[out.find("html[lang=").expect("a language rule")..];
        assert!(
            rule.starts_with("html[lang=\"ko\"]{--font-primary:everyday_standard, bd_ko_body,"),
            "got: {rule}"
        );
        assert!(
            !rule.contains("\"everyday_standard, "),
            "the stack was quoted whole"
        );
    }

    #[test]
    fn a_quoted_declaration_of_the_variable_is_left_alone() {
        // It is the thing the language rules override, and rewriting it to
        // `var(--font-primary)` would make it refer to itself.
        let (out, _) = patch_ko(".t{--font-primary:\"everyday_standard\"}");
        assert!(
            out.contains(".t{--font-primary:\"everyday_standard\"}"),
            "got: {out}"
        );
    }

    #[test]
    fn single_quotes_work_the_same_way() {
        let (out, _) = patch_ko(".t{font-family:'high_birth'}");
        assert!(
            out.contains("--font-heading:high_birth, bd_ko_heading,"),
            "got: {out}"
        );
    }

    #[test]
    fn a_longer_quoted_string_starting_with_the_name_is_not_matched() {
        let (_, rep) = patch_ko(".t{content:\"everyday_standard_extra\"}");
        assert_eq!(rep.stacks, 0);
    }

    #[test]
    fn generic_families_are_bare_but_spaced_names_are_quoted() {
        let (out, _) = patch_ko(".t{font-family:everyday_standard}");
        assert!(
            out.contains("'Malgun Gothic'"),
            "a name with a space needs quotes"
        );
        assert!(
            out.contains(", sans-serif"),
            "a generic keyword must stay bare"
        );
    }

    #[test]
    fn the_font_url_climbs_out_of_the_assets_directory() {
        let (out, _) = patch_ko(".t{}");
        assert!(out.contains("url(../fonts/bd-ko-body.woff2)"), "got: {out}");
    }

    #[test]
    fn inserts_after_charset() {
        let (out, _) = patch_ko("@charset \"utf-8\";.t{color:red}");
        assert!(
            out.starts_with("@charset \"utf-8\";"),
            "@charset must stay on line one"
        );
    }

    #[test]
    fn size_adjust_is_the_grid_ratio() {
        let (out, _) = patch_ko(".t{}");
        assert!(out.contains("size-adjust:133.3333%"), "8/6 = 133.33%");
    }

    #[test]
    fn metrics_are_divided_by_size_adjust() {
        let (out, _) = patch_ko(".t{}");
        // 150% ascent divided by a ratio of 1.3333 gives 112.5%
        assert!(
            out.contains("ascent-override:112.5%"),
            "trailing zeros are dropped, as the Node reference writes it"
        );
    }

    #[test]
    fn a_slot_with_no_font_of_ours_still_gets_the_system_stack() {
        // Russian is the case: the game's own Everyday_Standard draws Cyrillic, so only
        // the heading slot is replaced. The body slot must still fall through to the
        // system font rather than being left with the game's font alone.
        let heading = crate::assets::catalogue().unwrap().languages["ru"]
            .fonts
            .clone();
        let sys = vec!["Segoe UI".to_string(), "sans-serif".to_string()];
        let css = ".a{font-family:everyday_standard}.b{font-family:high_birth}";
        let (out, rep) = patch_all(css, &one(&heading, &sys));
        assert_eq!(rep.faces, 1, "one @font-face, for the heading");
        assert_eq!(rep.rules, 1, "one language rule");
        assert!(
            out.contains("--font-primary:everyday_standard, 'Segoe UI', sans-serif"),
            "got: {out}"
        );
        assert!(
            out.contains("--font-heading:high_birth, bd_ru_heading, 'Segoe UI', sans-serif"),
            "got: {out}"
        );
    }

    #[test]
    fn the_language_row_is_made_to_wrap() {
        // The game lays the flags out in one row and we keep adding to it. Without
        // this the settings dialog grows wider than the window.
        let (out, _) = patch_ko(".t{}");
        assert!(
            out.contains(".language-flags{flex-wrap:wrap;"),
            "got: {out}"
        );
        assert!(
            out.contains("min-width:0"),
            "flex-wrap alone will not shrink it"
        );
    }

    #[test]
    fn with_nothing_to_add_the_stylesheet_is_left_alone() {
        let css = ".a{font-family:everyday_standard}";
        let (out, rep) = patch_all(css, &one(&[], &[]));
        assert_eq!(out, css);
        assert_eq!(rep.stacks, 0, "a no-op must not report work");
    }
}

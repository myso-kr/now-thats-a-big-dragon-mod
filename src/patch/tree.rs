//! The upgrade tree, read out of the bundle.
//!
//! Unlocking is done by the UI click handler, not the reducer:
//!   dispatch(buy_upgrade)
//!   purchased == 0                     -> dispatch(show_upgrade,   {children})
//!   purchased + 1 == (unlockAt ?? 3)   -> dispatch(unlock_upgrade, {children})
//! Autoplay sends only buy_upgrade, which leaves the tree shut forever - 12 of the 88
//! upgrades reachable. Sending those two signals ourselves needs each upgrade's
//! children and its unlockAt, and that is what this reads.
//!
//! It used to come from a file `tools/extract-tree.js` wrote by hand. That file is
//! derived from the game and so is not committed, which meant this launcher - the one
//! that actually ships - never had it at all, and autoplay stalled at twelve upgrades.
//! Reading the bundle both launchers already patch fixes that and cannot go stale.
//!
//! `patch/tree.js` is the Node reference implementation; `tests/bundle.rs` compares the
//! two byte for byte on a real bundle.

use serde_json::{json, Map, Value};

/// `click:[{id:ge.CarpalCure` - the first branch of the tree, and the only place in
/// the bundle where a tree node literal follows a branch name.
const ANCHOR: &str = "click:[{id:ge.";

/// `n.CarpalCure="carpalCure"` throughout the bundle, as a map from the one to the
/// other. The first spelling wins, matching Node's `if (!(m[1] in ids))`.
fn upgrade_ids(src: &str) -> std::collections::HashMap<&str, &str> {
    let mut out = std::collections::HashMap::new();
    let bytes = src.as_bytes();
    let mut from = 0;
    while let Some(at) = src[from..].find("n.") {
        let start = from + at + 2;
        from = start;
        // An identifier beginning with a capital, then `="`, then a lowercase name.
        let name_end = start
            + src[start..]
                .find(|c: char| !c.is_ascii_alphanumeric())
                .unwrap_or(0);
        let name = &src[start..name_end];
        if name.is_empty() || !name.starts_with(|c: char| c.is_ascii_uppercase()) {
            continue;
        }
        if !src[name_end..].starts_with("=\"") {
            continue;
        }
        let vstart = name_end + 2;
        let Some(vlen) = src[vstart..].find('"') else {
            continue;
        };
        let value = &src[vstart..vstart + vlen];
        if value.is_empty()
            || !value.starts_with(|c: char| c.is_ascii_alphabetic())
            || !value.bytes().all(|b| b.is_ascii_alphanumeric())
        {
            continue;
        }
        // `xn.Foo="bar"` is not `n.Foo="bar"`; the byte before has to end the token.
        let before = start.checked_sub(3).map(|i| bytes[i]);
        if before.is_some_and(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'$') {
            continue;
        }
        out.entry(name).or_insert(value);
    }
    out
}

/// Rewrite every `ge.Xxx` as the string it stands for. `None` if one is unknown.
fn resolve(literal: &str, ids: &std::collections::HashMap<&str, &str>) -> Option<String> {
    let mut out = String::with_capacity(literal.len());
    let mut rest = literal;
    while let Some(at) = rest.find("ge.") {
        out.push_str(&rest[..at]);
        let after = &rest[at + 3..];
        let end = after
            .find(|c: char| !c.is_ascii_alphanumeric())
            .unwrap_or(after.len());
        let name = &after[..end];
        if !name.starts_with(|c: char| c.is_ascii_uppercase()) {
            // Not a reference - copy `ge.` through and carry on.
            out.push_str("ge.");
            rest = after;
            continue;
        }
        out.push_str(&serde_json::to_string(ids.get(name)?).ok()?);
        rest = &after[end..];
    }
    out.push_str(rest);
    Some(out)
}

/// `{ family: { upgrade: { children, unlockAt } } }`, or `None` when the anchor is gone.
///
/// `None` rather than an error is deliberate: a game update that moves this costs
/// autoplay its unlock signals and nothing else - the translation, the cheats and the
/// rest of the patch should still go in.
pub fn extract(src: &str) -> Option<Value> {
    let at = src.find(ANCHOR)?;
    let ids = upgrade_ids(src);

    // Walk back to the brace that opens the whole tree, not the nearest one.
    //
    // The nearest `{` before `click:` is the tree's own only while every branch
    // declared ahead of it is empty - which today is true, because `BUG_HIDE:[]` is
    // first and holds nothing. One node in front of `click:` and the nearest `{` would
    // be that node's, and this would quietly return a single upgrade as though it were
    // the tree. So candidates are tried outwards until one parses to an object with a
    // `click` branch in it, which only the tree itself has.
    let mut parsed = None;
    let mut from = at;
    while let Some(start) = src[..=from.min(src.len() - 1)].rfind('{') {
        if let Some(end) = super::scan::balanced(src, start) {
            if end > at {
                let literal = resolve(&src[start..end], &ids)?;
                if let Ok(v) = super::jsval::parse(&literal) {
                    if v.get("click").is_some_and(Value::is_array) {
                        parsed = Some(v);
                        break;
                    }
                }
            }
        }
        if start == 0 {
            break;
        }
        from = start - 1;
    }
    let parsed = parsed?;

    let branches = parsed.as_object()?;
    let mut out = Map::new();
    // serde_json keeps insertion order (preserve_order), so the branches are sorted to
    // match Node's `Object.keys(tree).sort()` and the two serialise identically.
    let mut names: Vec<&String> = branches.keys().collect();
    names.sort();
    for cat in names {
        if cat == "BUG_HIDE" {
            continue;
        }
        let Some(list) = branches[cat].as_array() else {
            continue;
        };
        let mut m = Map::new();
        for node in list {
            let Some(id) = node.get("id").and_then(Value::as_str) else {
                continue;
            };
            let children = node
                .get("children")
                .and_then(Value::as_array)
                .cloned()
                .unwrap_or_default();
            // The game's own default, from `subTreeConfig?.unlockAt ?? 3`.
            //
            // Read as f64 and rounded: the JS literal parser has no integer type, so
            // `unlockAt:1` arrives as 1.0, `as_i64` says None, and every node silently
            // took the default of 3. It would also have serialised as `1.0` where Node
            // writes `1`, which the byte comparison would have caught - but only after
            // the wrong unlock signals had already shipped.
            let unlock_at = node
                .get("subTreeConfig")
                .and_then(|c| c.get("unlockAt"))
                .and_then(Value::as_f64)
                .map(|n| n as i64)
                .unwrap_or(3);
            m.insert(
                id.to_owned(),
                json!({ "children": children, "unlockAt": unlock_at }),
            );
        }
        out.insert(cat.clone(), Value::Object(m));
    }
    (!out.is_empty()).then(|| Value::Object(out))
}

/// How many nodes a tree holds, for the log line.
pub fn count_nodes(tree: Option<&Value>) -> usize {
    tree.and_then(Value::as_object)
        .map(|m| {
            m.values()
                .filter_map(Value::as_object)
                .map(Map::len)
                .sum::<usize>()
        })
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    // Minified, the way the real bundle is - the literal parser reads what the game
    // ships, not a pretty-printed version of it.
    const BUNDLE: &str = concat!(
        r#"var x=1;n.CarpalCure="carpalCure",n.IronFinger="ironFinger","#,
        r#"n.Barbarian="barbarian";var t={click:[{id:ge.CarpalCure,"#,
        r#"children:[ge.IronFinger],subTreeConfig:{unlockAt:1}},"#,
        r#"{id:ge.IronFinger,children:[]}],warrior:[{id:ge.Barbarian,children:[]}],"#,
        r#"BUG_HIDE:[{id:ge.CarpalCure}]};"#,
    );

    #[test]
    fn reads_the_tree_and_resolves_every_name() {
        let t = extract(BUNDLE).expect("a tree");
        assert_eq!(t["click"]["carpalCure"]["children"][0], "ironFinger");
        assert_eq!(t["click"]["carpalCure"]["unlockAt"], 1);
        assert_eq!(
            t["warrior"]["barbarian"]["children"]
                .as_array()
                .unwrap()
                .len(),
            0
        );
    }

    #[test]
    fn a_node_with_no_subtree_config_gets_the_games_default_of_three() {
        let t = extract(BUNDLE).expect("a tree");
        assert_eq!(t["click"]["ironFinger"]["unlockAt"], 3);
    }

    #[test]
    fn the_hidden_debug_branch_is_left_out() {
        let t = extract(BUNDLE).expect("a tree");
        assert!(t.get("BUG_HIDE").is_none());
    }

    #[test]
    fn branches_come_out_sorted_so_the_two_launchers_serialise_alike() {
        let t = extract(BUNDLE).expect("a tree");
        let keys: Vec<&String> = t.as_object().unwrap().keys().collect();
        assert_eq!(keys, ["click", "warrior"]);
    }

    #[test]
    fn a_bundle_without_the_anchor_gives_nothing_rather_than_failing() {
        assert!(extract("var x=1;").is_none());
        assert_eq!(count_nodes(None), 0);
    }

    #[test]
    fn the_tree_is_found_even_with_a_populated_branch_ahead_of_click() {
        // The nearest `{` before `click:` is then a node's, not the tree's. Taking it
        // would return one upgrade as though it were the whole tree.
        let src = concat!(
            r#"n.A="a",n.B="b";var t={warrior:[{id:ge.B,children:[]}],"#,
            r#"click:[{id:ge.A,children:[]}]};"#,
        );
        let t = extract(src).expect("a tree");
        let keys: Vec<&String> = t.as_object().unwrap().keys().collect();
        assert_eq!(keys, ["click", "warrior"]);
    }

    #[test]
    fn an_unresolvable_name_gives_nothing_rather_than_a_wrong_tree() {
        // A tree naming an upgrade the bundle never defines is a tree we cannot trust,
        // and a wrong unlock signal is worse than none.
        let src = r#"var t={click:[{id:ge.CarpalCure,children:[ge.NeverDefined]}]};"#;
        assert!(extract(src).is_none());
    }
}

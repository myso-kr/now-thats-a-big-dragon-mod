//! Find the English i18n tables in the bundle and merge Korean into them.
//!
//! The game refers to one object per namespace, as `en:{upgrades:X,common:Y,…}`.
//! We locate the literal each of those references points at and swap it wholesale.

use crate::patch::scan;
use serde_json::Value;

/// The namespaces the game uses. This order has nothing to do with bundle order.
pub const NAMESPACES: &[&str] = &[
    "upgrades",
    "common",
    "statistics",
    "generators",
    "settings",
    "menus",
    "tooltip",
    "infos",
    "game",
    "dungeon",
    "summaries",
    "levels",
    // Arrived with game 1.1.0. table_ids matches by membership, not end to end, so a
    // namespace the game adds does not break the anchor.
    "artifacts",
];

#[derive(Debug, Default)]
pub struct Report {
    pub replaced: Vec<String>,
    pub translated: usize,
    pub total: usize,
}

/// Pull the namespace-to-identifier mapping out of an `en:{ns:ident,…}` block.
pub fn table_ids(src: &str) -> Option<Vec<(String, String)>> {
    // Take the en mapping in which every namespace appears.
    let needle = "en:{";
    let mut from = 0;
    while let Some(rel) = src[from..].find(needle) {
        let at = from + rel;
        let brace = at + needle.len() - 1;
        if let Some(end) = scan::balanced(src, brace) {
            let body = &src[brace + 1..end - 1];
            let pairs = parse_pairs(body);
            if NAMESPACES
                .iter()
                .all(|ns| pairs.iter().any(|(k, _)| k == ns))
            {
                return Some(pairs);
            }
        }
        from = at + needle.len();
    }
    None
}

/// Split `a:X,b:Y` into (key, identifier). Nesting is not handled — this block is flat.
fn parse_pairs(body: &str) -> Vec<(String, String)> {
    body.split(',')
        .filter_map(|part| {
            let (k, v) = part.split_once(':')?;
            let k = k.trim();
            let v = v.trim();
            let ident_ok = !v.is_empty()
                && v.chars()
                    .all(|c| c.is_ascii_alphanumeric() || c == '_' || c == '$');
            ident_ok.then(|| (k.to_owned(), v.to_owned()))
        })
        .collect()
}

/// Use the ko value where there is one, the en value otherwise.
///
/// Structure follows en, then picks up whatever keys only the translation has. That
/// tail is not padding: English has two plural forms and Russian four, so
/// `seconds_few` and `seconds_many` exist on our side alone — dropping them leaves
/// i18next printing the wrong form for 2, 3 and 4.
pub fn deep_merge(en: &Value, ko: Option<&Value>, count: &mut (usize, usize)) -> Value {
    match en {
        Value::Object(map) => {
            let mut out = serde_json::Map::new();
            for (k, v) in map {
                let sub = ko.and_then(|k2| k2.get(k));
                out.insert(k.clone(), deep_merge(v, sub, count));
            }
            if let Some(Value::Object(extra)) = ko {
                for (k, v) in extra {
                    if !out.contains_key(k) {
                        out.insert(k.clone(), v.clone());
                    }
                }
            }
            Value::Object(out)
        }
        Value::String(_) => {
            count.1 += 1;
            match ko {
                Some(Value::String(s)) => {
                    count.0 += 1;
                    Value::String(s.clone())
                }
                _ => en.clone(),
            }
        }
        _ => en.clone(),
    }
}

/// Count how many strings the Korean side actually covers.
fn count_strings(en: &Value, ko: Option<&Value>, acc: &mut (usize, usize)) {
    match en {
        Value::String(s) => {
            acc.1 += 1;
            if let Some(Value::String(k)) = ko {
                if k != s {
                    acc.0 += 1;
                }
            }
        }
        Value::Object(map) => {
            for (k, v) in map {
                count_strings(v, ko.and_then(|x| x.get(k)), acc);
            }
        }
        _ => {}
    }
}

/// Every namespace, merged over the English table, as one object keyed by namespace.
///
/// This is what goes into the i18next resources bundle as a whole new locale. The
/// merge over English is not optional: the game sets no `fallbackLng` of its own, so
/// a key our translation is missing would render as the key itself rather than as the
/// original text. `locale::set_fallback` fixes that for the general case; merging
/// still matters because it is what the resources entry is built from.
pub fn merged(src: &str, ko: &Value) -> Result<(Value, Report), String> {
    let ids = table_ids(src)
        .ok_or("could not find the en i18n tables - the game looks to have been updated")?;
    let mut rep = Report::default();
    let mut out = serde_json::Map::new();

    for (ns, id) in &ids {
        if !NAMESPACES.contains(&ns.as_str()) {
            continue;
        }
        let Some((start, end)) = scan::object_literal(src, id) else {
            continue;
        };
        let en = match crate::patch::jsval::parse(&src[start..end]) {
            Ok(v) => v,
            Err(e) => {
                crate::warn!("skipping the {ns} table: {e}");
                continue;
            }
        };
        let ko_ns = ko.get(ns);
        let mut counts = (0usize, 0usize);
        count_strings(&en, ko_ns, &mut counts);
        out.insert(ns.clone(), deep_merge(&en, ko_ns, &mut (0, 0)));
        rep.replaced.push(ns.clone());
        rep.translated += counts.0;
        rep.total += counts.1;
    }
    Ok((Value::Object(out), rep))
}

/// The six time-unit names a language prints, read out of its statistics table.
///
/// None when any of them is missing — a Scale with five English keys and one
/// translated one would print a mix, which is worse than printing English.
pub fn time_units(ko: &Value) -> Option<Vec<String>> {
    let stats = ko.get("statistics")?;
    let mut out = Vec::with_capacity(TIME_UNITS.len());
    for unit in TIME_UNITS {
        match stats.get(format!("{unit}_other")).and_then(Value::as_str) {
            Some(l) if !l.is_empty() => out.push(l.to_owned()),
            _ => return None,
        }
    }
    Some(out)
}

/// Replace every English table with the Korean-merged one.
///
/// Edits are applied back to front so that earlier byte offsets stay valid. The
/// replacement is emitted as JSON, which is a subset of what a JS object literal
/// accepts, so the game reads it back identically.
pub fn patch(src: &str, ko: &Value) -> Result<(String, Report), String> {
    let ids = table_ids(src)
        .ok_or("could not find the en i18n tables - the game looks to have been updated")?;
    let mut rep = Report::default();
    let mut edits: Vec<(usize, usize, String)> = Vec::new();

    for (ns, id) in &ids {
        if !NAMESPACES.contains(&ns.as_str()) {
            continue;
        }
        let Some((start, end)) = scan::object_literal(src, id) else {
            continue;
        };
        let en = match crate::patch::jsval::parse(&src[start..end]) {
            Ok(v) => v,
            // One unreadable table must not take the other eleven with it.
            Err(e) => {
                crate::warn!("skipping the {ns} table: {e}");
                continue;
            }
        };
        let ko_ns = ko.get(ns);
        let mut counts = (0usize, 0usize);
        count_strings(&en, ko_ns, &mut counts);
        let merged = deep_merge(&en, ko_ns, &mut (0, 0));
        edits.push((
            start,
            end,
            serde_json::to_string(&merged).map_err(|e| e.to_string())?,
        ));
        rep.replaced.push(ns.clone());
        rep.translated += counts.0;
        rep.total += counts.1;
    }

    // Back to front, so applying one edit cannot shift the next one's offsets.
    edits.sort_by_key(|e| std::cmp::Reverse(e.0));
    let mut out = src.to_owned();
    for (start, end, text) in edits {
        out.replace_range(start..end, &text);
    }
    Ok((out, rep))
}

// The unit shown in "5.28 minutes" does not come from the i18n tables. Each language
// has its own Scale object, and the key names are printed verbatim:
//   en: new Scale({seconds:1, minutes:60, hours:3600, days:86400, ...})
// So the keys themselves have to be rewritten.
const TIME_SCALE: &str = "{seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3}";
const TIME_UNITS: [&str; 6] = ["seconds", "minutes", "hours", "days", "months", "years"];
const TIME_VALUES: [&str; 6] = ["1", "60", "3600", "86400", "2592e3", "31536e3"];

/// Rewrite the English Scale keys into Korean.
///
/// The labels come from the i18n tables (statistics.*_other) rather than a second
/// list here, so there is one source for them. Only the English Scale matches this
/// pattern; the other languages have different keys and are left alone.
pub fn patch_time_scale(src: &str, ko: &Value) -> (String, bool) {
    let stats = ko.get("statistics");
    let mut parts = Vec::with_capacity(TIME_UNITS.len());
    for (i, unit) in TIME_UNITS.iter().enumerate() {
        let label = stats
            .and_then(|s| s.get(format!("{unit}_other")))
            .and_then(Value::as_str);
        match label {
            Some(l) if !l.is_empty() => {
                parts.push(format!(
                    "{}:{}",
                    serde_json::Value::String(l.into()),
                    TIME_VALUES[i]
                ));
            }
            _ => return (src.to_owned(), false),
        }
    }
    if !src.contains(TIME_SCALE) {
        return (src.to_owned(), false);
    }
    (
        src.replacen(TIME_SCALE, &format!("{{{}}}", parts.join(",")), 1),
        true,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn finds_every_namespace_in_the_en_mapping() {
        let src = format!(
            "var L={{en:{{{}}},fr:{{}}}};",
            NAMESPACES
                .iter()
                .enumerate()
                .map(|(i, ns)| format!("{ns}:F{i}"))
                .collect::<Vec<_>>()
                .join(",")
        );
        let ids = table_ids(&src).expect("should have been found");
        assert_eq!(ids.len(), NAMESPACES.len());
        assert_eq!(ids[0].1, "F0");
    }

    #[test]
    fn does_not_pick_a_block_that_has_only_some_of_them() {
        let src = "var L={en:{upgrades:A,common:B}};";
        assert!(table_ids(src).is_none());
    }

    #[test]
    fn korean_wins_where_there_is_korean() {
        let en = json!({"a":"A","b":{"c":"C"}});
        let ko = json!({"a":"가"});
        let mut n = (0, 0);
        let out = deep_merge(&en, Some(&ko), &mut n);
        assert_eq!(out["a"], "가");
        assert_eq!(out["b"]["c"], "C", "untranslated strings keep the original");
        assert_eq!(n, (1, 2), "1 translated of 2");
    }

    #[test]
    fn non_string_values_are_not_counted() {
        let en = json!({"n":1,"s":"x"});
        let mut n = (0, 0);
        deep_merge(&en, None, &mut n);
        assert_eq!(n.1, 1, "only strings are counted");
    }

    #[test]
    fn plural_forms_english_does_not_have_survive_the_merge() {
        // Russian needs four; English carries two. Following the English structure
        // alone would silently drop `_few` and `_many`, and i18next would then print
        // the wrong word for 2, 3 and 4.
        let en = json!({"bard_one": "Bard", "bard_other": "Bards"});
        let ru = json!({
            "bard_one": "бард", "bard_few": "барда",
            "bard_many": "бардов", "bard_other": "барда",
        });
        let mut n = (0, 0);
        let out = deep_merge(&en, Some(&ru), &mut n);
        assert_eq!(out, ru);
        assert_eq!(n.1, 2, "only the English strings count towards the total");
    }

    #[test]
    fn an_extra_key_does_not_displace_the_english_ones() {
        let en = json!({"a": "A", "b": "B"});
        let tr = json!({"a": "А", "c": "В"});
        let mut n = (0, 0);
        let out = deep_merge(&en, Some(&tr), &mut n);
        assert_eq!(out, json!({"a": "А", "b": "B", "c": "В"}));
    }

    #[test]
    fn the_time_units_come_out_of_the_statistics_table() {
        let ko = json!({"statistics": {
            "seconds_other": "초", "minutes_other": "분", "hours_other": "시간",
            "days_other": "일", "months_other": "개월", "years_other": "년",
        }});
        assert_eq!(time_units(&ko).unwrap().len(), 6);
        // One missing unit would give a Scale with a mix of languages in its keys,
        // which is worse than leaving it in English.
        let mut short = ko.clone();
        short["statistics"]
            .as_object_mut()
            .unwrap()
            .remove("years_other");
        assert!(time_units(&short).is_none());
        assert!(time_units(&json!({})).is_none());
    }
}

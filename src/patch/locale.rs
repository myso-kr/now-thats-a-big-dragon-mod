//! Adds a language to the game's own language list, so it appears in the settings
//! screen as one more flag to click.
//!
//! This is a different job from merging a translation into a table (i18n.rs). Here we
//! edit the game's *list* of languages, in six places:
//!
//!   resources   the i18next bundle, `{en:{…},fr:{…},…}`
//!   supported   `["en","fr","de","pt","tr"]`, which the settings UI maps over
//!   flags       `{en:"us.png",…}`, the image for each code
//!   labels      `languages:{en:"English",…}` inside every locale's settings namespace
//!   time scale  `{en:new X.Scale({seconds:1,…}),…}`, the printed unit names
//!   default     the settings a fresh profile starts with
//!
//! The flag list the UI renders is derived from the supported array, so adding a code
//! there and a file here is enough for the button to appear.
//!
//! Every edit past the first is optional and reported separately. Only the resources
//! edit is required; if it fails the caller falls back to overwriting `en`, so a game
//! update that moves the settings UI costs the settings integration, not the
//! translation. Mirrors patch/locale.js.

use regex::Regex;
use serde_json::Value;

/// What actually happened, anchor by anchor.
#[derive(Debug, Default)]
pub struct Added {
    pub lang: String,
    pub resources: bool,
    pub supported: bool,
    pub flag: bool,
    pub labels: usize,
    pub time_scale: bool,
    pub default: bool,
}

/// The resources object is the one whose `en` entry holds every namespace. Finding it
/// by that shape rather than by its minified name is what survives a rebuild.
fn resources_at(src: &str) -> Option<usize> {
    Regex::new(r"en:\{upgrades:[A-Za-z0-9_$]+,common:[A-Za-z0-9_$]+")
        .unwrap()
        .find(src)
        .map(|m| m.start())
}

/// Insert a whole locale into the i18next resources object.
///
/// The tables have to be merged over English already: the game sets no `fallbackLng`,
/// so a key missing from our locale renders as the key itself rather than falling
/// back to the original text.
pub fn add_locale(src: &str, lang: &str, tables: &Value) -> Option<String> {
    let at = resources_at(src)?;
    let entry = format!("{}:{},", Value::String(lang.into()), tables);
    let mut out = String::with_capacity(src.len() + entry.len());
    out.push_str(&src[..at]);
    out.push_str(&entry);
    out.push_str(&src[at..]);
    Some(out)
}

/// Add the code to the list the settings screen offers.
pub fn add_supported(src: &str, lang: &str) -> Option<String> {
    let needle = r#"["en","fr","de","pt","tr"]"#;
    let at = src.find(needle)?;
    let replaced = format!(
        r#"["en","fr","de","pt","tr",{}]"#,
        Value::String(lang.into())
    );
    Some(format!(
        "{}{replaced}{}",
        &src[..at],
        &src[at + needle.len()..]
    ))
}

/// Name the flag image for the code. The file itself is served by the launcher.
pub fn add_flag(src: &str, lang: &str, file: &str) -> Option<String> {
    let needle = r#"{en:"us.png",fr:"fr.png",de:"de.png",pt:"br.png",tr:"tr.png"}"#;
    let at = src.find(needle)?;
    let replaced = format!(
        "{},{}:{}}}",
        &needle[..needle.len() - 1],
        Value::String(lang.into()),
        Value::String(file.into())
    );
    Some(format!(
        "{}{replaced}{}",
        &src[..at],
        &src[at + needle.len()..]
    ))
}

/// Add our language's name to every locale's list of language names, so the button
/// has a label whichever language the UI is in.
///
/// The same name is used in all of them: a language is best named in itself, and
/// "한국어" is more use to a French player than "Coréen" would be to a Korean one.
pub fn add_labels(src: &str, lang: &str, label: &str) -> (String, usize) {
    let re = Regex::new(r#"languages:\{en:"[^"]*",fr:"[^"]*",de:"[^"]*",pt:"[^"]*",tr:"[^"]*"\}"#)
        .unwrap();
    let mut count = 0;
    let mut out = String::with_capacity(src.len());
    let mut last = 0;
    for m in re.find_iter(src) {
        count += 1;
        out.push_str(&src[last..m.start()]);
        let whole = m.as_str();
        out.push_str(&whole[..whole.len() - 1]);
        out.push(',');
        out.push_str(&Value::String(lang.into()).to_string());
        out.push(':');
        out.push_str(&Value::String(label.into()).to_string());
        out.push('}');
        last = m.end();
    }
    out.push_str(&src[last..]);
    (out, count)
}

const TIME_VALUES: [&str; 6] = ["1", "60", "3600", "86400", "2592e3", "31536e3"];

/// Give the new language its own time-unit Scale.
///
/// The game looks these up as `Fj[lang] ?? Fj.en`, so a language without one simply
/// shows English units — which is why this is added rather than the English entry
/// being overwritten. Overwriting would put Korean units in front of English players.
///
/// The Scale constructor's minified name is read out of the anchor itself, so nothing
/// here depends on knowing what a rebuild called it.
pub fn add_time_scale(src: &str, lang: &str, labels: &[String]) -> Option<String> {
    if labels.len() != TIME_VALUES.len() || labels.iter().any(String::is_empty) {
        return None;
    }
    // The `en:` key is part of the match so the insertion point is the start of an
    // entry, not an offset counted backwards from one.
    let re = Regex::new(
        r"en:new ([A-Za-z0-9_$]+)\.Scale\(\{seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3\}\)",
    )
    .unwrap();
    let m = re.captures(src)?;
    let whole = m.get(0)?;
    let ctor = m.get(1)?.as_str();

    let units: Vec<String> = labels
        .iter()
        .zip(TIME_VALUES)
        .map(|(l, v)| format!("{}:{v}", Value::String(l.clone())))
        .collect();
    let entry = format!(
        "{}:new {ctor}.Scale({{{}}}),",
        Value::String(lang.into()),
        units.join(",")
    );
    Some(format!(
        "{}{entry}{}",
        &src[..whole.start()],
        &src[whole.start()..]
    ))
}

/// Make our language the one a fresh profile starts in.
///
/// This is the default, not an override: the moment the player picks a language in
/// the settings screen the game persists that, and the persisted value wins from then
/// on. So the system's language decides where to start, and the player decides after.
pub fn set_default_language(src: &str, lang: &str) -> Option<String> {
    let re = Regex::new(r#"(chromaticAberration:\d+,largerTextSize:!\d,language:)"en""#).unwrap();
    let m = re.captures(src)?;
    let whole = m.get(0)?;
    let head = m.get(1)?.as_str();
    Some(format!(
        "{}{head}{}{}",
        &src[..whole.start()],
        Value::String(lang.into()),
        &src[whole.end()..]
    ))
}

/// Give i18next a fallback language.
///
/// The game sets none, so i18next falls back to its own default of `dev` — and a key
/// missing from the selected locale renders as the key itself. That is what a player
/// sees when their saved language is one this build does not carry: a screen of
/// `TABS.TROOPS` and `smallDragon`. Falling back to English is always readable.
pub fn set_fallback(src: &str, lang: &str) -> Option<String> {
    let re = Regex::new(r"\.init\(\{resources:[A-Za-z0-9_$]+,lng:[A-Za-z0-9_$]+,").unwrap();
    let m = re.find(src)?;
    Some(format!(
        "{}fallbackLng:{},{}",
        &src[..m.end()],
        Value::String(lang.into()),
        &src[m.end()..]
    ))
}

/// One language, with everything the settings screen needs in order to offer it.
pub struct Bundled<'a> {
    pub lang: &'a str,
    pub label: &'a str,
    pub flag_file: &'a str,
    pub tables: &'a Value,
    pub units: Option<&'a [String]>,
}

/// What happened when every language went in at once.
#[derive(Debug, Default)]
pub struct AddedAll {
    pub langs: Vec<String>,
    pub resources: usize,
    pub supported: bool,
    pub flag: bool,
    pub labels: usize,
    pub time_scale: usize,
    pub fallback: bool,
    pub default: bool,
}

/// Insert one comma-joined run of entries just inside the closing bracket of `needle`.
fn extend(src: &str, needle: &str, entries: &str) -> Option<String> {
    let at = src.find(needle)?;
    let (body, close) = needle.split_at(needle.len() - 1);
    Some(format!(
        "{}{body},{entries}{close}{}",
        &src[..at],
        &src[at + needle.len()..]
    ))
}

/// Add every language at once.
///
/// They have to go in together: each anchor is matched by the shape the game shipped,
/// and adding one language changes that shape. Doing them one at a time would find
/// the anchor once and miss it for everyone after.
///
/// All of them are added, not just the one being selected — the settings screen is a
/// list, and a player whose saved choice is missing from it gets untranslated keys.
///
/// `default_lang` is the one a fresh profile starts in. It is only a default: the
/// moment the player picks a language the game persists that, and the persisted value
/// wins from then on.
///
/// Returns None only when the resources anchor is missing, which is the one edit the
/// rest is worthless without.
pub fn add_languages(
    src: &str,
    langs: &[Bundled],
    default_lang: Option<&str>,
) -> Option<(String, AddedAll)> {
    let mut report = AddedAll {
        langs: langs.iter().map(|l| l.lang.to_owned()).collect(),
        ..AddedAll::default()
    };

    let mut code = src.to_owned();
    for l in langs {
        code = add_locale(&code, l.lang, l.tables)?;
        report.resources += 1;
    }

    let joined = |f: &dyn Fn(&Bundled) -> String| -> String {
        langs.iter().map(f).collect::<Vec<_>>().join(",")
    };

    let codes = joined(&|l: &Bundled| Value::String(l.lang.into()).to_string());
    if let Some(next) = extend(&code, r#"["en","fr","de","pt","tr"]"#, &codes) {
        code = next;
        report.supported = true;
    }

    let flags = joined(&|l: &Bundled| {
        format!(
            "{}:{}",
            Value::String(l.lang.into()),
            Value::String(l.flag_file.into())
        )
    });
    let flag_anchor = r#"{en:"us.png",fr:"fr.png",de:"de.png",pt:"br.png",tr:"tr.png"}"#;
    if let Some(next) = extend(&code, flag_anchor, &flags) {
        code = next;
        report.flag = true;
    }

    let labels = joined(&|l: &Bundled| {
        format!(
            "{}:{}",
            Value::String(l.lang.into()),
            Value::String(l.label.into())
        )
    });
    let re = Regex::new(r#"languages:\{en:"[^"]*",fr:"[^"]*",de:"[^"]*",pt:"[^"]*",tr:"[^"]*"\}"#)
        .unwrap();
    let mut out = String::with_capacity(code.len());
    let mut last = 0;
    for m in re.find_iter(&code) {
        report.labels += 1;
        out.push_str(&code[last..m.start()]);
        let whole = m.as_str();
        out.push_str(&whole[..whole.len() - 1]);
        out.push(',');
        out.push_str(&labels);
        out.push('}');
        last = m.end();
    }
    out.push_str(&code[last..]);
    code = out;

    for l in langs {
        if let Some(u) = l.units {
            if let Some(next) = add_time_scale(&code, l.lang, u) {
                code = next;
                report.time_scale += 1;
            }
        }
    }

    if let Some(next) = set_fallback(&code, "en") {
        code = next;
        report.fallback = true;
    }

    if let Some(d) = default_lang {
        if let Some(next) = set_default_language(&code, d) {
            code = next;
            report.default = true;
        }
    }

    Some((code, report))
}

/// Everything needed for one language to appear in the settings screen.
///
/// Returns None only when the resources anchor is missing, which is the one edit the
/// rest is worthless without.
pub fn add_language(
    src: &str,
    lang: &str,
    label: &str,
    flag_file: &str,
    tables: &Value,
    units: Option<&[String]>,
) -> Option<(String, Added)> {
    let mut report = Added {
        lang: lang.to_owned(),
        ..Added::default()
    };

    let mut code = add_locale(src, lang, tables)?;
    report.resources = true;

    if let Some(next) = add_supported(&code, lang) {
        code = next;
        report.supported = true;
    }
    if let Some(next) = add_flag(&code, lang, flag_file) {
        code = next;
        report.flag = true;
    }
    let (next, count) = add_labels(&code, lang, label);
    code = next;
    report.labels = count;

    if let Some(u) = units {
        if let Some(next) = add_time_scale(&code, lang, u) {
            code = next;
            report.time_scale = true;
        }
    }
    if let Some(next) = set_default_language(&code, lang) {
        code = next;
        report.default = true;
    }
    Some((code, report))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn bundle() -> String {
        let ns: Vec<String> = crate::patch::i18n::NAMESPACES
            .iter()
            .enumerate()
            .map(|(i, n)| format!("{n}:E{i}"))
            .collect();
        format!(
            "var MLe={{en:{{{}}},fr:{{x:1}}}},M7=[\"en\",\"fr\",\"de\",\"pt\",\"tr\"],pF=\"en\";\
             var BGe={{en:\"us.png\",fr:\"fr.png\",de:\"de.png\",pt:\"br.png\",tr:\"tr.png\"}};\
             var E4={{languages:{{en:\"English\",fr:\"French\",de:\"German\",pt:\"Portuguese\",tr:\"Turkish\"}}}};\
             var F4={{languages:{{en:\"Anglais\",fr:\"Français\",de:\"Allemand\",pt:\"Portugais\",tr:\"Turc\"}}}};\
             var Fj={{en:new M_.Scale({{seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3}})}};\
             a={{chromaticAberration:10,largerTextSize:!1,language:\"en\"}};\
             q9.use(k7).init({{resources:MLe,lng:pF,interpolation:{{escapeValue:!1}}}});",
            ns.join(",")
        )
    }

    fn units() -> Vec<String> {
        ["초", "분", "시간", "일", "개월", "년"]
            .iter()
            .map(|s| s.to_string())
            .collect()
    }

    #[test]
    fn a_locale_is_inserted_and_english_is_left_alone() {
        let out = add_locale(&bundle(), "ko", &json!({"common":{"hello":"안녕"}})).unwrap();
        assert!(out.contains(r#""ko":{"common":{"hello":"안녕"}}"#));
        assert!(out.contains("en:{upgrades:E0"));
    }

    #[test]
    fn the_code_joins_the_supported_list() {
        let out = add_supported(&bundle(), "ko").unwrap();
        assert!(out.contains(r#"["en","fr","de","pt","tr","ko"]"#));
    }

    #[test]
    fn the_flag_map_gains_an_entry() {
        let out = add_flag(&bundle(), "ko", "kr.png").unwrap();
        assert!(out.contains(r#"tr:"tr.png","ko":"kr.png"}"#));
    }

    #[test]
    fn every_locale_learns_the_new_language_name() {
        let (out, n) = add_labels(&bundle(), "ko", "한국어");
        assert_eq!(n, 2, "the English and the French settings tables");
        assert!(out.contains(r#"tr:"Turkish","ko":"한국어""#));
        assert!(out.contains(r#"tr:"Turc","ko":"한국어""#));
    }

    #[test]
    fn a_scale_is_added_rather_than_the_english_one_replaced() {
        let out = add_time_scale(&bundle(), "ko", &units()).unwrap();
        assert!(out.contains(r#""ko":new M_.Scale({"초":1,"분":60"#));
        assert!(
            out.contains("en:new M_.Scale({seconds:1"),
            "English units must survive"
        );
    }

    #[test]
    fn an_incomplete_unit_list_adds_no_scale() {
        assert!(add_time_scale(&bundle(), "ko", &["초".to_string()]).is_none());
        let mut blank = units();
        blank[2] = String::new();
        assert!(add_time_scale(&bundle(), "ko", &blank).is_none());
    }

    #[test]
    fn a_fresh_profile_starts_in_the_added_language() {
        let out = set_default_language(&bundle(), "ko").unwrap();
        assert!(out.contains(r#"largerTextSize:!1,language:"ko""#));
    }

    #[test]
    fn the_whole_thing_reports_each_anchor() {
        let (_, r) = add_language(
            &bundle(),
            "ko",
            "한국어",
            "kr.png",
            &json!({"common":{}}),
            Some(&units()),
        )
        .unwrap();
        assert!(r.resources && r.supported && r.flag && r.time_scale && r.default);
        assert_eq!(r.labels, 2);
    }

    #[test]
    fn losing_the_settings_anchors_still_leaves_the_translation() {
        // A game update that moves the settings UI must not cost us the translation.
        let partial = bundle()
            .replace(r#"["en","fr","de","pt","tr"]"#, "SOMETHING_ELSE")
            .replace(
                r#"{en:"us.png",fr:"fr.png",de:"de.png",pt:"br.png",tr:"tr.png"}"#,
                "{}",
            );
        let (_, r) = add_language(
            &partial,
            "ko",
            "한국어",
            "kr.png",
            &json!({"common":{}}),
            Some(&units()),
        )
        .unwrap();
        assert!(r.resources, "the locale still went in");
        assert!(!r.supported);
        assert!(!r.flag);
    }

    #[test]
    fn without_the_resources_anchor_nothing_is_attempted() {
        assert!(add_language("var x=1;", "ko", "한국어", "kr.png", &json!({}), None).is_none());
    }

    #[test]
    fn a_fallback_language_is_given_to_i18next() {
        let out = set_fallback(&bundle(), "en").expect("the init call");
        assert!(
            out.contains(r#"init({resources:MLe,lng:pF,fallbackLng:"en","#),
            "got: {out}"
        );
    }

    #[test]
    fn a_bundle_without_an_init_call_is_reported_rather_than_guessed_at() {
        assert!(set_fallback("var x=1;", "en").is_none());
    }

    fn two() -> (Value, Value) {
        (
            json!({"common": {"a": "가"}}),
            json!({"common": {"a": "甲"}}),
        )
    }

    #[test]
    fn every_language_goes_in_on_one_pass() {
        // Adding one at a time would find each anchor for the first language and miss
        // it for the second, because the insertion changes the shape being matched.
        let (ko, zh) = two();
        let langs = vec![
            Bundled {
                lang: "ko",
                label: "한국어",
                flag_file: "kr.png",
                tables: &ko,
                units: None,
            },
            Bundled {
                lang: "zh-Hans",
                label: "简体中文",
                flag_file: "cn.png",
                tables: &zh,
                units: None,
            },
        ];
        let (out, rep) = add_languages(&bundle(), &langs, Some("ko")).expect("resources anchor");

        assert_eq!(rep.resources, 2);
        assert!(rep.supported);
        assert!(rep.flag);
        assert_eq!(rep.labels, 2, "one per locale's settings namespace");
        assert!(rep.fallback);
        assert!(rep.default);

        assert!(
            out.contains(r#"["en","fr","de","pt","tr","ko","zh-Hans"]"#),
            "got: {out}"
        );
        assert!(
            out.contains(r#""ko":"kr.png","zh-Hans":"cn.png"}"#),
            "got: {out}"
        );
        assert!(
            out.contains(r#"tr:"Turkish","ko":"한국어","zh-Hans":"简体中文"}"#),
            "got: {out}"
        );
        assert!(
            out.contains(r#"tr:"Turc","ko":"한국어","zh-Hans":"简体中文"}"#),
            "both locales"
        );
        assert!(
            out.contains(r#"language:"ko""#),
            "the fresh-profile default"
        );
        assert!(out.contains(r#""ko":{"common":{"a":"가"}}"#), "got: {out}");
        assert!(
            out.contains(r#""zh-Hans":{"common":{"a":"甲"}}"#),
            "got: {out}"
        );
    }

    #[test]
    fn english_is_left_alone() {
        // The whole point of adding rather than overwriting: an English player who
        // launches with the mod still gets English.
        let (ko, zh) = two();
        let langs = vec![
            Bundled {
                lang: "ko",
                label: "한국어",
                flag_file: "kr.png",
                tables: &ko,
                units: None,
            },
            Bundled {
                lang: "zh-Hans",
                label: "简体中文",
                flag_file: "cn.png",
                tables: &zh,
                units: None,
            },
        ];
        let (out, _) = add_languages(&bundle(), &langs, Some("ko")).expect("resources anchor");
        assert!(out.contains(r#"en:"us.png""#));
        assert!(out.contains(r#"languages:{en:"English""#));
        assert!(
            out.contains("en:new M_.Scale({seconds:1,"),
            "the English Scale is untouched"
        );
    }

    #[test]
    fn each_language_gets_its_own_time_scale() {
        let (ko, zh) = two();
        let zh_units: Vec<String> = ["秒", "分钟", "小时", "天", "个月", "年"]
            .iter()
            .map(|s| s.to_string())
            .collect();
        let ko_units = units();
        let langs = vec![
            Bundled {
                lang: "ko",
                label: "한국어",
                flag_file: "kr.png",
                tables: &ko,
                units: Some(&ko_units),
            },
            Bundled {
                lang: "zh-Hans",
                label: "简体中文",
                flag_file: "cn.png",
                tables: &zh,
                units: Some(&zh_units),
            },
        ];
        let (out, rep) = add_languages(&bundle(), &langs, None).expect("resources anchor");
        assert_eq!(rep.time_scale, 2);
        assert!(out.contains(r#""ko":new M_.Scale({"초":1,"#), "got: {out}");
        assert!(
            out.contains(r#""zh-Hans":new M_.Scale({"秒":1,"#),
            "got: {out}"
        );
        assert!(!rep.default, "no default was asked for, so none was set");
        assert!(
            out.contains(r#"language:"en""#),
            "the default is left as shipped"
        );
    }

    #[test]
    fn without_the_resources_anchor_no_language_goes_in() {
        let (ko, _) = two();
        let langs = vec![Bundled {
            lang: "ko",
            label: "한국어",
            flag_file: "kr.png",
            tables: &ko,
            units: None,
        }];
        assert!(add_languages("var x=1;", &langs, Some("ko")).is_none());
    }
}

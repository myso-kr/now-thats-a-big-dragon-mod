//! Which language to patch in, and why.
//!
//! The game ships en/fr/de/pt/tr and picks one from the system locale itself.
//! Anything else falls back to `en` — which is the slot this mod overwrites. So a
//! language is only patched in when the game does not already have it, and the
//! system's own choice is what decides.
//!
//! Mirrors lib/language.js; the two must agree, because the Node launcher is the
//! reference implementation and a difference here is a difference users would see.

use serde::Deserialize;
use std::collections::BTreeMap;

/// locale/languages.json.
#[derive(Debug, Deserialize)]
pub struct Catalogue {
    #[serde(rename = "gameSupports", default)]
    pub game_supports: Vec<String>,
    #[serde(default)]
    pub languages: BTreeMap<String, Language>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Language {
    #[serde(default)]
    pub name: String,
    #[serde(default)]
    pub matches: Vec<String>,
    #[serde(default)]
    pub fallback: Vec<String>,
    #[serde(rename = "flagFile", default)]
    pub flag_file: String,
    #[serde(default)]
    pub fonts: Vec<Font>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Font {
    pub replaces: String,
    pub family: String,
    pub file: String,
    pub url: String,
    #[serde(rename = "pxPerEm")]
    pub px_per_em: f64,
    #[serde(rename = "basePxPerEm")]
    pub base_px_per_em: f64,
    #[serde(rename = "ascentOverride")]
    pub ascent_override: Option<f64>,
    #[serde(rename = "descentOverride")]
    pub descent_override: Option<f64>,
}

/// `ko_KR.UTF-8` becomes `ko-kr`. Locales arrive in several shapes.
pub fn normalise(locale: &str) -> String {
    locale
        .trim()
        .split('.')
        .next()
        .unwrap_or("")
        .replace('_', "-")
        .to_lowercase()
}

/// The primary subtag: `zh-hant-tw` becomes `zh`.
pub fn primary(locale: &str) -> String {
    let n = normalise(locale);
    n.split('-').next().unwrap_or("").to_owned()
}

/// The language whose `matches` best fits this locale, or None.
/// Longer prefixes win, so `zh-hant` beats `zh` for `zh-Hant-TW`.
pub fn match_locale(cat: &Catalogue, locale: &str) -> Option<String> {
    let want = normalise(locale);
    if want.is_empty() {
        return None;
    }
    let mut best: Option<(String, usize)> = None;
    for (lang, def) in &cat.languages {
        for prefix in &def.matches {
            let p = normalise(prefix);
            if want != p && !want.starts_with(&format!("{p}-")) {
                continue;
            }
            if best.as_ref().is_none_or(|(_, len)| p.len() > *len) {
                best = Some((lang.clone(), p.len()));
            }
        }
    }
    best.map(|(lang, _)| lang)
}

pub struct Choice {
    pub lang: Option<String>,
    pub reason: String,
}

/// Decide what to apply.
pub fn resolve(
    cat: &Catalogue,
    requested: Option<&str>,
    locale: &str,
    available: &[String],
) -> Choice {
    // An explicit choice is taken at face value, including one the game already
    // supports — asking for it is a deliberate override.
    if let Some(req) = requested {
        let want = normalise(req);
        // An exact code first: `zh-Hans` must not be reduced to `zh`, which is a
        // different language as far as this catalogue is concerned.
        let mut lang = available.iter().find(|a| normalise(a) == want).cloned();
        // Otherwise treat it as a locale, so `ko-KR` and `zh-Hant-TW` also work.
        if lang.is_none() {
            lang = match_locale(cat, req).filter(|hit| available.contains(hit));
        }
        if let Some(lang) = lang {
            return Choice {
                lang: Some(lang),
                reason: format!("requested: {req}"),
            };
        }
        let have = if available.is_empty() {
            "none".to_owned()
        } else {
            available.join(", ")
        };
        return Choice {
            lang: None,
            reason: format!("no translation for {req} (have: {have})"),
        };
    }

    let Some(hit) = match_locale(cat, locale) else {
        let shown = if locale.is_empty() { "unknown" } else { locale };
        return Choice {
            lang: None,
            reason: format!("no translation for the system locale ({shown})"),
        };
    };
    // The game already speaks this one; ours would only get in the way.
    if cat.game_supports.contains(&hit) {
        return Choice {
            lang: None,
            reason: format!("the game supports {hit} natively"),
        };
    }
    if !available.contains(&hit) {
        return Choice {
            lang: None,
            reason: format!("no {hit} translation files are present"),
        };
    }
    Choice {
        lang: Some(hit),
        reason: format!("system locale: {locale}"),
    }
}

/// The user's locale, as Windows reports it.
///
/// Reading the registry avoids a dependency on the Windows API crates for one value.
/// The launcher already shells out to tasklist, so this is in keeping.
pub fn system_locale() -> String {
    for key in ["BIG_DRAGON_LANG", "LC_ALL", "LANG"] {
        if let Ok(v) = std::env::var(key) {
            if !v.trim().is_empty() {
                return v;
            }
        }
    }
    let out = std::process::Command::new("reg")
        .args([
            "query",
            r"HKCU\Control Panel\International",
            "/v",
            "LocaleName",
        ])
        .output();
    let Ok(out) = out else { return String::new() };
    parse_reg_locale(&String::from_utf8_lossy(&out.stdout)).unwrap_or_default()
}

/// Pull the value out of `LocaleName    REG_SZ    ko-KR`.
fn parse_reg_locale(text: &str) -> Option<String> {
    for line in text.lines() {
        let mut parts = line.split_whitespace();
        if parts.next() != Some("LocaleName") {
            continue;
        }
        let _ty = parts.next()?;
        let value = parts.next()?;
        if !value.is_empty() {
            return Some(value.to_owned());
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    fn catalogue() -> Catalogue {
        serde_json::from_str(
            r#"{
              "gameSupports": ["en","fr","de","pt","tr"],
              "languages": {
                "ko":      {"matches":["ko"],      "fallback":[], "fonts":[]},
                "ja":      {"matches":["ja"],      "fallback":[], "fonts":[]},
                "zh-Hans": {"matches":["zh-hans","zh-cn","zh"], "fallback":[], "fonts":[]},
                "zh-Hant": {"matches":["zh-hant","zh-tw"],      "fallback":[], "fonts":[]},
                "de":      {"matches":["de"],      "fallback":[], "fonts":[]}
              }
            }"#,
        )
        .unwrap()
    }

    fn have() -> Vec<String> {
        ["ko", "ja", "zh-Hans", "zh-Hant", "de"]
            .iter()
            .map(|s| s.to_string())
            .collect()
    }

    #[test]
    fn locales_are_normalised_whatever_shape_they_arrive_in() {
        assert_eq!(normalise("ko_KR.UTF-8"), "ko-kr");
        assert_eq!(normalise("ko-KR"), "ko-kr");
        assert_eq!(normalise("  ja  "), "ja");
        assert_eq!(primary("zh-Hant-TW"), "zh");
    }

    #[test]
    fn a_plain_language_matches() {
        let c = catalogue();
        assert_eq!(match_locale(&c, "ko-KR").as_deref(), Some("ko"));
    }

    #[test]
    fn a_longer_prefix_wins_so_scripts_are_distinguished() {
        let c = catalogue();
        assert_eq!(match_locale(&c, "zh-Hant-TW").as_deref(), Some("zh-Hant"));
        assert_eq!(match_locale(&c, "zh-CN").as_deref(), Some("zh-Hans"));
        assert_eq!(match_locale(&c, "zh").as_deref(), Some("zh-Hans"));
    }

    #[test]
    fn a_prefix_must_end_at_a_subtag_boundary() {
        // `kok` (Konkani) is not Korean.
        assert_eq!(match_locale(&catalogue(), "kok-IN"), None);
    }

    #[test]
    fn the_system_locale_decides_when_we_have_that_language() {
        let r = resolve(&catalogue(), None, "ko-KR", &have());
        assert_eq!(r.lang.as_deref(), Some("ko"));
    }

    #[test]
    fn a_language_the_game_already_speaks_is_left_to_the_game() {
        let r = resolve(&catalogue(), None, "de-DE", &have());
        assert_eq!(r.lang, None);
        assert!(r.reason.contains("natively"), "{}", r.reason);
    }

    #[test]
    fn a_language_we_have_no_files_for_is_not_applied() {
        let r = resolve(&catalogue(), None, "ja-JP", &["ko".to_string()]);
        assert_eq!(r.lang, None);
    }

    #[test]
    fn an_unknown_locale_leaves_the_game_as_it_is() {
        let r = resolve(&catalogue(), None, "sv-SE", &have());
        assert_eq!(r.lang, None);
    }

    #[test]
    fn an_explicit_request_overrides_the_system_locale() {
        let r = resolve(&catalogue(), Some("ja"), "ko-KR", &have());
        assert_eq!(r.lang.as_deref(), Some("ja"));
    }

    #[test]
    fn a_request_we_cannot_honour_does_not_silently_fall_back() {
        let r = resolve(&catalogue(), Some("sv"), "ko-KR", &have());
        assert_eq!(r.lang, None);
        assert!(r.reason.contains("have: "), "{}", r.reason);
    }

    #[test]
    fn an_explicit_script_tagged_code_is_not_reduced_to_its_primary_subtag() {
        // `zh-Hans` and `zh-Hant` are different languages here; collapsing either to
        // `zh` picks the wrong one, or nothing at all.
        let c = catalogue();
        assert_eq!(
            resolve(&c, Some("zh-Hans"), "en-US", &have())
                .lang
                .as_deref(),
            Some("zh-Hans")
        );
        assert_eq!(
            resolve(&c, Some("zh-Hant-TW"), "en-US", &have())
                .lang
                .as_deref(),
            Some("zh-Hant")
        );
    }

    #[test]
    fn a_request_in_full_locale_form_is_accepted() {
        let r = resolve(&catalogue(), Some("ko-KR"), "en-US", &have());
        assert_eq!(r.lang.as_deref(), Some("ko"));
    }

    #[test]
    fn the_registry_line_is_parsed() {
        let text = "\r\nHKEY_CURRENT_USER\\Control Panel\\International\r\n    LocaleName    REG_SZ    ko-KR\r\n";
        assert_eq!(parse_reg_locale(text).as_deref(), Some("ko-KR"));
    }

    #[test]
    fn a_registry_dump_without_the_value_gives_nothing() {
        assert_eq!(
            parse_reg_locale("    sCountry    REG_SZ    Korea\r\n"),
            None
        );
        assert_eq!(parse_reg_locale(""), None);
    }

    #[test]
    fn the_shipped_catalogue_parses_and_is_consistent() {
        let text = include_str!("../locale/languages.json");
        let cat: Catalogue = serde_json::from_str(text).expect("locale/languages.json");
        assert!(cat.game_supports.contains(&"en".to_string()));
        for (lang, def) in &cat.languages {
            assert!(!def.matches.is_empty(), "{lang}: needs matches");
            assert!(!def.fallback.is_empty(), "{lang}: needs a system fallback");
            assert!(
                !cat.game_supports.contains(lang),
                "{lang}: the game already ships this, so patching it in is pointless"
            );
        }
    }
}

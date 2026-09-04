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

pub fn patch(src: &str, fonts: &[Font], fallback: &[String]) -> (String, Report) {
    let mut out = String::with_capacity(src.len() + 512);
    let mut rep = Report::default();

    // @charset has to stay on the first line, so insert after it.
    let insert_at = if src.starts_with("@charset") {
        src.find(';').map(|i| i + 1).unwrap_or(0)
    } else {
        0
    };
    out.push_str(&src[..insert_at]);
    for f in fonts {
        out.push_str(&face(f));
        rep.faces += 1;
    }
    // Only when a language is actually being applied. With nothing to add, patching
    // must leave the stylesheet byte for byte as it was.
    if !fonts.is_empty() || !fallback.is_empty() {
        out.push_str(LANGUAGE_ROW);
    }

    // Append our font behind the original wherever the original is used, so Latin
    // glyphs still come from the game's font and only the rest falls through to ours.
    // The @font-face declarations themselves are left alone.
    let body = &src[insert_at..];
    let mut cursor = 0usize;
    let mut patched = String::with_capacity(body.len() + 256);

    // Collect the @font-face block ranges up front so declarations can be skipped.
    let mut skip: Vec<(usize, usize)> = Vec::new();
    let mut from = 0;
    while let Some(rel) = body[from..].find("@font-face") {
        let at = from + rel;
        if let Some(brace) = body[at..].find('{') {
            if let Some(end) = crate::patch::scan::balanced(body, at + brace) {
                skip.push((at, end));
                from = end;
                continue;
            }
        }
        from = at + "@font-face".len();
    }
    let in_skip = |i: usize| skip.iter().any(|&(a, b)| i >= a && i < b);

    let bytes = body.as_bytes();
    let mut i = 0usize;
    while i < body.len() {
        // The name may be bare or quoted: `font-family:everyday_standard` and
        // `--font-primary:"everyday_standard"` both occur. A quote has to stay
        // wrapped around the original name alone — quoting the whole stack turns it
        // into one nonexistent family name and nothing applies at all.
        let quote = match bytes.get(i) {
            Some(&q @ (b'"' | b'\'')) => Some(q),
            _ => None,
        };
        let name_at = if quote.is_some() { i + 1 } else { i };
        // Both base families are recognised, not only the ones we have a font for: a
        // language may replace one slot and leave the other to the game's own font,
        // and that slot still wants the system stack behind it.
        let hit = BASE_FAMILIES.iter().find(|name| {
            if in_skip(i) || !body[name_at..].starts_with(**name) {
                return false;
            }
            let after = bytes.get(name_at + name.len());
            match quote {
                // A quoted name has to be closed by the same quote, or this is some
                // longer string that merely begins with the font name.
                Some(q) => after == Some(&q),
                // A bare name has to end here too — `everyday_standard_extra` is a
                // different token, not this font.
                None => !matches!(after, Some(c) if c.is_ascii_alphanumeric() || *c == b'_' || *c == b'-'),
            }
        });
        match hit {
            Some(name) => {
                let ours = fonts.iter().find(|f| f.replaces == **name);
                // Nothing to add means nothing to rewrite: counting this as a hit
                // would report work that did not happen.
                if ours.is_none() && fallback.is_empty() {
                    i += 1;
                    continue;
                }
                let end = name_at + name.len() + usize::from(quote.is_some());
                patched.push_str(&body[cursor..i]);
                patched.push_str(&body[i..end]); // the original, quotes and all
                for extra in ours
                    .map(|f| f.family.as_str())
                    .into_iter()
                    .chain(fallback.iter().map(String::as_str))
                {
                    patched.push_str(", ");
                    patched.push_str(&quote_family(extra));
                }
                i = end;
                cursor = i;
                rep.stacks += 1;
            }
            None => i += 1,
        }
    }
    patched.push_str(&body[cursor..]);
    out.push_str(&patched);
    (out, rep)
}

#[cfg(test)]
mod tests {
    use super::*;

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
        patch(src, &ko_fonts(), &fallback())
    }

    #[test]
    fn rewrites_usages_but_not_declarations() {
        let css = "@font-face{font-family:everyday_standard;src:url(a.woff2)}\
                   .t{font-family:everyday_standard}";
        let (out, rep) = patch_ko(css);
        assert_eq!(rep.faces, 2, "two Korean faces are added");
        assert_eq!(rep.stacks, 1, "one usage, and not the declaration");
        assert!(out.contains("everyday_standard, bd_body, 'Malgun Gothic', sans-serif"));
    }

    #[test]
    fn the_original_font_stays_first() {
        // Latin glyphs must keep coming from the game's own font; ours only catches
        // what the original has no glyph for.
        let (out, _) = patch_ko(".t{font-family:everyday_standard}");
        let decl = &out[out.find(".t{font-family:").unwrap()..];
        assert!(
            decl.find("everyday_standard").unwrap() < decl.find("bd_body").unwrap(),
            "the original has to precede ours"
        );
    }

    #[test]
    fn a_quoted_name_keeps_its_quotes_around_the_name_alone() {
        // Wrapping the whole stack in one pair of quotes makes it a single family
        // name that does not exist, so no font applies at all. That was a real bug.
        let (out, rep) = patch_ko(".t{--font-primary:\"everyday_standard\"}");
        assert_eq!(rep.stacks, 1);
        assert!(
            out.contains("\"everyday_standard\", bd_body,"),
            "got: {}",
            &out[out.find("--font-primary").unwrap()..]
        );
    }

    #[test]
    fn single_quotes_work_the_same_way() {
        let (out, _) = patch_ko(".t{font-family:'high_birth'}");
        assert!(out.contains("'high_birth', bd_heading,"), "got: {out}");
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
        assert!(out.contains("url(../fonts/bd-body.woff2)"), "got: {out}");
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
        // Russian is the case: the game's own Everyday_Standard draws Cyrillic, so
        // only the heading slot is replaced. The body slot must still fall through to
        // the system font rather than being left alone.
        let heading = crate::assets::catalogue().unwrap().languages["ru"]
            .fonts
            .clone();
        let sys = vec!["Segoe UI".to_string(), "sans-serif".to_string()];
        let css = ".a{font-family:everyday_standard}.b{font-family:high_birth}";
        let (out, rep) = patch(css, &heading, &sys);
        assert_eq!(rep.faces, 1, "one @font-face, for the heading");
        assert_eq!(rep.stacks, 2, "both slots are rewritten");
        assert!(
            out.contains("font-family:everyday_standard, 'Segoe UI', sans-serif}"),
            "got: {out}"
        );
        assert!(
            out.contains("font-family:high_birth, bd_heading, 'Segoe UI', sans-serif}"),
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
        let (out, rep) = patch(css, &[], &[]);
        assert_eq!(out, css);
        assert_eq!(rep.stacks, 0, "a no-op must not report work");
    }
}

//! Reading the option labels out of an .ink file.
//!
//! Autoplay has to choose an option, and until now it did that by looking for a
//! Korean substring - so in the other thirteen languages nothing matched, four of the
//! eight branching dialogues held for thirty seconds and then took whatever came
//! first, and the invasion silently paid the ransom. The dialogue *id* was never the
//! problem: the game's `start_dialog` event carries it and knows no language. Only the
//! mapping from "the option I want" to "the option on screen" did, because it went
//! through text.
//!
//! So the labels are read out of the .ink files this mod itself writes, for whichever
//! language is being patched in, and handed to the renderer. Policies then name an
//! option by its position in the file - which `tools/check-dialogs.js` already
//! guarantees is the same in every language - and the label is only used to find that
//! option on screen.
//!
//! `lib/ink.js` is the Node reference implementation; `tests/bundle.rs` checks the two
//! produce the same table.

use serde_json::{Map, Value};

/// The option labels of one .ink file, in the order they appear.
///
/// A choice is `*` or `+` at the start of a line, optionally followed by conditions in
/// braces, then the label in square brackets. Ink also allows a choice with no
/// brackets, where the whole line is both the label and the text; the game's own files
/// never use that form, and one appearing would be a translation error rather than
/// something to guess at, so it is left out.
pub fn choices(src: &str) -> Vec<&str> {
    let mut out = Vec::new();
    for raw in src.lines() {
        let line = raw.trim();
        if !(line.starts_with('*') || line.starts_with('+')) {
            continue;
        }
        // A gather (`-`) is not a choice, and `**` is a nested choice - still a choice.
        let body = line.trim_start_matches(['*', '+', ' ', '\t']);
        let Some(open) = body.find('[') else { continue };
        let Some(close) = body[open..].find(']') else {
            continue;
        };
        out.push(&body[open + 1..open + close]);
    }
    out
}

/// The table handed to the renderer: `{ "<file stem>": [label, ...] }`.
///
/// Files are visited in name order, the same as Node's, so the two serialise
/// identically - which is what makes a byte comparison of the injected source
/// meaningful rather than a test of `HashMap` iteration order.
pub fn choice_table(files: &[(&str, &str)]) -> Value {
    let mut names: Vec<&(&str, &str)> = files.iter().collect();
    names.sort_by_key(|(name, _)| *name);

    let mut out = Map::new();
    for (name, body) in names {
        // The embedded dialogues are keyed by stem; Node reads a directory and sees
        // file names. Both end up at the stem, which is what the renderer looks up.
        let stem = name.strip_suffix(".ink").unwrap_or(name);
        let labels = choices(body);
        if labels.is_empty() {
            continue;
        }
        out.insert(
            stem.to_owned(),
            Value::Array(
                labels
                    .into_iter()
                    .map(|l| Value::String(l.to_owned()))
                    .collect(),
            ),
        );
    }
    Value::Object(out)
}

/// The table for one bundled language.
pub fn choice_table_for(lang: &str) -> Value {
    let dialogs = crate::assets::dialogs(lang);
    let files: Vec<(&str, &str)> = dialogs.into_iter().collect();
    choice_table(&files)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_labels_in_order_and_ignores_the_conditions() {
        let src = "\
VAR canAfford = 0
* { canAfford > 0 } [Food {amount}]
* { canAfford > 0 } [Wood {amount}]
* [No thanks]
    -> END
";
        assert_eq!(
            choices(src),
            ["Food {amount}", "Wood {amount}", "No thanks"]
        );
    }

    #[test]
    fn a_gather_is_not_a_choice() {
        assert_eq!(choices("- Just a line\n  -> END\n").len(), 0);
    }

    #[test]
    fn a_choice_with_no_brackets_is_left_out_rather_than_guessed_at() {
        assert_eq!(choices("* Just a line\n").len(), 0);
    }

    #[test]
    fn a_file_with_no_options_is_left_out_of_the_table() {
        let t = choice_table(&[("intro.ink", "Hello\n"), ("trading.ink", "* [Buy]\n")]);
        assert!(t.get("intro").is_none());
        assert_eq!(t["trading"][0], "Buy");
    }

    #[test]
    fn the_bundled_korean_dialogue_has_every_group_the_policies_name() {
        let t = choice_table_for("ko");
        // The counts the autoplay policies index into. A change here means the game's
        // dialogue changed, and web/autoplay/engine/dialog.js has to change with it.
        for (file, n) in [
            ("trading", 6),
            ("pope_visit", 2),
            ("invasion_start", 3),
            ("catapult", 2),
            ("dungeon_rescue", 1),
            ("king_dungeon", 2),
            ("king_dungeon_2", 1),
        ] {
            let got = t[file].as_array().map(Vec::len).unwrap_or(0);
            assert_eq!(got, n, "{file}: {got} options, expected {n}");
        }
    }
}

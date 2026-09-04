'use strict';

// Reading the option labels out of an .ink file.
//
// Autoplay has to choose an option, and until now it did that by looking for a Korean
// substring - so in the other thirteen languages nothing matched, four of the eight
// branching dialogues held for thirty seconds and then took whatever came first, and
// the invasion silently paid the ransom. The dialogue *id* was never the problem: the
// game's `start_dialog` event carries it and knows no language. Only the mapping from
// "the option I want" to "the option on screen" did, because it went through text.
//
// So the labels are read out of the .ink files this mod itself writes, for whichever
// language is being patched in, and handed to the renderer. Policies then name an
// option by its position in the file - which `tools/check-dialogs.js` already
// guarantees is the same in every language - and the label is only used to find that
// option on screen.
//
// The Rust launcher does the same in `src/ink.rs`; `tests/bundle.rs` checks the two
// agree. (lib/ink.test.js)

/**
 * The option labels of one .ink file, in the order they appear.
 *
 * A choice is `*` or `+` at the start of a line, optionally followed by conditions in
 * braces, then the label in square brackets. Ink also allows a choice with no
 * brackets, where the whole line is both the label and the text; the game's own files
 * never use that form, and one appearing would be a translation error rather than
 * something to guess at, so it is left out.
 *
 * @param {string} src the .ink source
 * @returns {string[]} labels, `{interpolations}` left in place
 */
function choices(src) {
  const out = [];
  for (const raw of src.split(/\r?\n/)) {
    const line = raw.trim();
    if (!(line.startsWith('*') || line.startsWith('+'))) continue;
    // A gather (`-`) is not a choice, and `**` is a nested choice - still a choice.
    const body = line.replace(/^[*+\s]+/, '');
    const open = body.indexOf('[');
    if (open < 0) continue;
    const close = body.indexOf(']', open);
    if (close < 0) continue;
    out.push(body.slice(open + 1, close));
  }
  return out;
}

/**
 * The table handed to the renderer: `{ "<file stem>": [label, ...] }`.
 *
 * @param {(name: string) => string} read given `trading.ink`, its source
 * @param {string[]} files the .ink file names of one language
 */
function choiceTable(read, files) {
  const out = {};
  for (const name of files.slice().sort()) {
    if (!name.endsWith('.ink')) continue;
    const labels = choices(read(name));
    if (labels.length) out[name.slice(0, -4)] = labels;
  }
  return out;
}

module.exports = { choices, choiceTable };

'use strict';

// Slots a bundled font in beside each original pixel font.
//
// The original fonts have no glyphs outside Latin. We serve ours through @font-face
// and append it behind the original in the stack, so Latin text is still drawn by
// the game's font and everything else falls through to ours.
//
// The two only look like one font if their "design pixel" sizes are matched 1:1,
// which is what size-adjust does.
//
// Mirrors src/patch/css.rs.

const GENERIC_FAMILIES = new Set(['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy', 'system-ui']);

/** A font name with a space or a non-ASCII character in it has to be quoted. */
function quoteFamily(name) {
  if (GENERIC_FAMILIES.has(name)) return name;
  return /^[A-Za-z][A-Za-z0-9_-]*$/.test(name) ? name : `'${name}'`;
}

/** The @font-face rule for one Korean font, with its metrics corrected. */
function faceFor(f) {
  const pct = (n) => String(+n.toFixed(4));
  const ratio = f.pxPerEm / f.basePxPerEm;

  // Pin line height to the original font's, so a larger Korean glyph does not change
  // the UI's line spacing. The catch: size-adjust scales the ascent and descent
  // overrides along with the glyphs, so they have to be divided by the same ratio to
  // cancel that out and land on the original's line box.
  const metrics = (f.ascentOverride !== undefined && f.descentOverride !== undefined)
    ? `ascent-override:${pct(f.ascentOverride / ratio)}%;`
      + `descent-override:${pct(f.descentOverride / ratio)}%;`
      + 'line-gap-override:0%;'
    : '';

  return `@font-face{font-family:${f.family};`
    + `src:url(../${f.url}) format("woff2");`
    + 'font-display:block;'
    + metrics
    + `size-adjust:${pct(ratio * 100)}%}`;
}

// The settings screen lays the language flags out in one non-wrapping row. The game
// ships five; we add one per bundled language, and the row simply grows — pushing the
// dialog wider than the window. Letting the row wrap costs nothing when there are
// five and is the only thing that works when there are twenty.
//
// `min-width:0` is the part that actually does it: a flex item defaults to its
// content's minimum width, so `flex-wrap` alone would still refuse to shrink.
const LANGUAGE_ROW = '.language-container{align-items:flex-start}'
  + '.language-flags{flex-wrap:wrap;min-width:0;flex:1 1 auto;row-gap:8px}';

function patch(src, koFonts, systemFallback) {
  const sysStack = (systemFallback || []).map(quoteFamily).join(', ');
  const byBase = new Map();
  const faces = [];

  for (const f of koFonts || []) {
    // An entry with no `replaces` ships the file for comparison only; it is not
    // put into the CSS.
    if (!f.replaces) continue;
    byBase.set(f.replaces, f);
    faces.push(faceFor(f));
  }

  let out = src;
  let hits = 0;

  // Every form the name appears in: font-family:everyday_standard,
  // --font-primary:"everyday_standard", and so on.
  out = out.replace(/(["']?)(everyday_standard|high_birth)\1/g, (whole, q, name, offset) => {
    // The font-family inside an @font-face declaration must not be touched — that
    // would rename the font itself rather than extend a stack.
    const before = out.slice(Math.max(0, offset - 200), offset);
    if (/@font-face\s*\{[^}]*$/.test(before)) return whole;

    const ko = byBase.get(name);
    const stack = [ko && ko.family, sysStack].filter(Boolean).join(', ');
    // Count only what is actually rewritten. Counting attempts would overstate the
    // number the launcher reports, and a nothing-changed run would look successful.
    if (!stack) return whole;
    hits += 1;
    return `${q}${name}${q}, ${stack}`;
  });

  // @charset is only valid at the very start of a stylesheet, so insert after it.
  const charset = /^\s*@charset\s+[^;]+;/.exec(out);
  const at = charset ? charset[0].length : 0;
  // Only when a language is actually being applied. With nothing to add, patching
  // must leave the stylesheet exactly as it was.
  const row = (faces.length || sysStack) ? LANGUAGE_ROW : '';
  const code = out.slice(0, at) + faces.join('') + row + out.slice(at);

  return { code, hits, faces: faces.length };
}

module.exports = { patch, quoteFamily, faceFor, LANGUAGE_ROW, GENERIC_FAMILIES };

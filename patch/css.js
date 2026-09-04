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

/** The two families the game funnels everything through. */
const BASE_FAMILIES = ['everyday_standard', 'high_birth'];

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

/**
 * Slot every bundled language's font in, and let the page pick by its own `lang`.
 *
 * `langs` is one entry per language offered - `{ lang, fonts, fallback }` - not just
 * the one being applied. The settings screen lists them all, and the game switches
 * without reloading, so a stylesheet that names only one font is a stylesheet that
 * keeps that font after the player switches: Korean to Simplified Chinese used to keep
 * Galmuri, which has none of the simplified characters, and drew 269 empty boxes.
 *
 * The game funnels every family through two custom properties, `--font-primary` and
 * `--font-heading`, and it already sets `document.documentElement.lang` and updates it
 * on `languageChanged`. So one `html[lang="xx"]` rule per language redefines those two
 * properties, and the switch takes effect the moment the player makes it.
 */
/**
 * Slot every bundled language's font in, and let the page pick by its own `lang`.
 *
 * `langs` is one entry per language offered - `{ lang, fonts, fallback }` - not just
 * the one being applied. The settings screen lists them all and the game switches
 * without reloading, so a stylesheet naming one font is a stylesheet that keeps that
 * font after the player switches: Korean to Simplified Chinese used to keep Galmuri,
 * which has none of the simplified characters, and drew 269 empty boxes.
 *
 * The game funnels every family through two custom properties, `--font-primary` and
 * `--font-heading`, and it already sets `document.documentElement.lang` and updates it
 * on `languageChanged`. So one `html[lang="xx"]` rule per language redefines those two
 * properties and the switch takes effect the moment the player makes it.
 *
 * A handful of the game's rules name a family directly rather than through the
 * variable. Those are rewritten to the variable, not given a stack of their own: a
 * direct `font-family: everyday_standard` cannot vary by language, and appending one
 * language's font to it is exactly how the wrong font survived a switch.
 */
function patch(src, langs, fallbackWhenBare) {
  // The old two-argument shape - a bare font list and a fallback - is what the launcher
  // used to pass. Still answered, so a caller with one language behaves as it did.
  const bare = !(Array.isArray(langs) && langs.length && langs[0] && langs[0].fonts);
  const list = bare
    ? [{ lang: null, fonts: langs || [], fallback: fallbackWhenBare || [] }]
    : langs;

  const faces = [];
  const rules = [];
  for (const L of list) {
    const sysStack = (L.fallback || []).map(quoteFamily).join(', ');
    const mine = new Map();
    for (const f of L.fonts || []) {
      // An entry with no `replaces` ships the file for comparison only; it is not put
      // into the CSS.
      if (!f.replaces) continue;
      mine.set(f.replaces, f);
      faces.push(faceFor(f));
    }
    if (!mine.size && !sysStack) continue;
    const stack = (name) => {
      const ours = mine.get(name);
      return [name, ours && ours.family, sysStack].filter(Boolean).join(', ');
    };
    const selector = L.lang ? `html[lang="${L.lang}"]` : ':root';
    rules.push(`${selector}{--font-primary:${stack(BASE_FAMILIES[0])};`
      + `--font-heading:${stack(BASE_FAMILIES[1])}}`);
  }

  // Two places keep the bare name: inside an `@font-face`, where it *is* the font being
  // defined, and inside a `--font-primary:` declaration, which the rules above override
  // and which would otherwise refer to itself.
  const NAMED = /(["']?)(everyday_standard|high_birth)\1/g;
  const VAR_OF = {
    everyday_standard: 'var(--font-primary)',
    high_birth: 'var(--font-heading)',
  };
  let hits = 0;
  // With no language rule to govern them, funnelling the direct declarations through
  // the variables would change the stylesheet for no gain - and patching with nothing
  // to add has to leave it byte for byte as it was.
  const out = !rules.length ? src : src.replace(NAMED, (whole, quote, name, offset) => {
    const before = src.slice(Math.max(0, offset - 200), offset);
    if (/@font-face\s*\{[^}]*$/.test(before)) return whole;
    if (/--font-(primary|heading)\s*:\s*$/.test(before)) return whole;
    hits += 1;
    return VAR_OF[name];
  });

  // @charset is only valid at the very start of a stylesheet, so insert after it.
  const charset = /^\s*@charset\s+[^;]+;/.exec(out);
  const at = charset ? charset[0].length : 0;
  // With nothing to add, patching must leave the stylesheet exactly as it was.
  const row = (faces.length || rules.length) ? LANGUAGE_ROW : '';
  // The faces go at the top; the language rules go at the very end. The game declares
  // `--font-primary` on a selector of its own, and `html[lang="xx"]` only outranks it
  // when it is more specific - which is not something to bet the whole font switch on.
  // Last one wins on a tie, so last is where they go.
  const code = out.slice(0, at) + faces.join('') + row + out.slice(at) + rules.join('');

  return { code, hits, faces: faces.length, rules: rules.length };
}

module.exports = {
  patch, quoteFamily, faceFor, LANGUAGE_ROW, GENERIC_FAMILIES, BASE_FAMILIES,
};

'use strict';

// Checks that every character a translation uses is actually in the font that
// language ships.
//
//   node tools/check-fonts.js         every bundled language
//   node tools/check-fonts.js zh-Hans just that one
//
// This exists because the assumption failed silently once: Galmuri carries 6,360 Han
// glyphs, which are the Korean hanja set, so it covered Korean perfectly and was
// missing 269 of the 867 characters the Simplified Chinese translation needs — every
// one of them a simplified form. On screen that is a page of empty boxes, and nothing
// in the launcher log would have said so.
//
// A font declaring a character is not quite proof that the glyph is drawn, but a font
// *not* declaring it is proof that it is not.

const fs = require('fs');
const path = require('path');
const cfg = require('../config');

/** Every character a language's translation actually uses. */
function charactersOf(lang) {
  const used = new Set();
  const walk = (o) => {
    if (typeof o === 'string') for (const c of o) used.add(c);
    else if (o && typeof o === 'object') for (const v of Object.values(o)) walk(v);
  };
  const table = cfg.PATHS.i18n(lang);
  if (fs.existsSync(table)) walk(JSON.parse(fs.readFileSync(table, 'utf8')));

  const dialogs = cfg.PATHS.dialogs(lang);
  if (fs.existsSync(dialogs)) {
    for (const f of fs.readdirSync(dialogs).filter((x) => x.endsWith('.ink'))) {
      walk(fs.readFileSync(path.join(dialogs, f), 'utf8'));
    }
  }
  return used;
}

/**
 * The characters a woff2 declares, read straight out of its cmap.
 *
 * Parsing the table by hand keeps this dependency-free, which matters because it runs
 * in CI. woff2 is compressed, so the bytes are handed to the same decompressor the
 * browser would use — Node has one built in for the Brotli stream.
 */
function cmapOf(file) {
  const zlib = require('zlib');
  const buf = fs.readFileSync(file);
  if (buf.toString('latin1', 0, 4) !== 'wOF2') throw new Error(`${file}: not woff2`);

  const numTables = buf.readUInt16BE(12);
  let p = 48;
  const readBase128 = () => {
    let v = 0;
    for (let i = 0; i < 5; i += 1) {
      const b = buf[p]; p += 1;
      v = (v * 128) + (b & 0x7f);
      if ((b & 0x80) === 0) return v;
    }
    throw new Error('malformed UIntBase128');
  };
  // The 63 tags woff2 can name by index instead of spelling out.
  const KNOWN = ['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post',
    'cvt ', 'fpgm', 'glyf', 'loca', 'prep', 'CFF ', 'VORG', 'EBDT', 'EBLC', 'gasp',
    'hdmx', 'kern', 'LTSH', 'PCLT', 'VDMX', 'vhea', 'vmtx', 'BASE', 'GDEF', 'GPOS',
    'GSUB', 'EBSC', 'JSTF', 'MATH', 'CBDT', 'CBLC', 'COLR', 'CPAL', 'SVG ', 'sbix',
    'acnt', 'avar', 'bdat', 'bloc', 'bsln', 'cvar', 'fdsc', 'feat', 'fmtx', 'fvar',
    'gvar', 'hsty', 'just', 'lcar', 'mort', 'morx', 'opbd', 'prop', 'trak', 'Zapf',
    'Silf', 'Glat', 'Gloc', 'Feat', 'Sill'];

  // Offsets are into the decompressed stream, where tables sit back to back with no
  // padding — and a transformed table occupies its transformed length, not its
  // original one. Getting either of those wrong lands you in the middle of a table.
  let offset = 0;
  let cmapAt = -1;
  for (let i = 0; i < numTables; i += 1) {
    const flags = buf[p]; p += 1;
    let tag;
    if ((flags & 0x3f) === 0x3f) { tag = buf.toString('latin1', p, p + 4); p += 4; }
    else tag = KNOWN[flags & 0x3f];
    const version = (flags >> 6) & 3;
    const origLength = readBase128();
    // glyf and loca invert the convention: for them version 0 *is* the transform.
    const transformed = (tag === 'glyf' || tag === 'loca') ? version === 0 : version !== 0;
    const length = transformed ? readBase128() : origLength;
    if (tag === 'cmap') cmapAt = offset;
    offset += length;
  }
  if (cmapAt < 0) throw new Error(`${file}: no cmap table`);

  const font = zlib.brotliDecompressSync(buf.subarray(p));
  const chars = new Set();
  const n = font.readUInt16BE(cmapAt + 2);
  for (let i = 0; i < n; i += 1) {
    const sub = cmapAt + font.readUInt32BE(cmapAt + 4 + i * 8 + 4);
    const format = font.readUInt16BE(sub);
    if (format === 4) {
      const segX2 = font.readUInt16BE(sub + 6);
      const ends = sub + 14;
      const starts = ends + segX2 + 2;
      const deltas = starts + segX2;
      const ranges = deltas + segX2;
      for (let seg = 0; seg < segX2 / 2; seg += 1) {
        const end = font.readUInt16BE(ends + seg * 2);
        const start = font.readUInt16BE(starts + seg * 2);
        if (start > end) continue;
        const delta = font.readInt16BE(deltas + seg * 2);
        const rangeOffset = font.readUInt16BE(ranges + seg * 2);
        for (let u = start; u <= end && u < 0xffff; u += 1) {
          if (rangeOffset === 0) {
            if (((u + delta) & 0xffff) !== 0) chars.add(u);
          } else {
            const gi = ranges + seg * 2 + rangeOffset + (u - start) * 2;
            if (gi + 1 < font.length && font.readUInt16BE(gi) !== 0) chars.add(u);
          }
        }
      }
    } else if (format === 12) {
      const groups = font.readUInt32BE(sub + 12);
      for (let g = 0; g < groups; g += 1) {
        const go = sub + 16 + g * 12;
        const start = font.readUInt32BE(go);
        const end = font.readUInt32BE(go + 4);
        for (let u = start; u <= end; u += 1) chars.add(u);
      }
    }
  }
  return chars;
}

/**
 * What the game's own font for a slot can draw.
 *
 * Recorded once by tools/make-game-coverage.py, because the fonts are the game's and
 * are not in this repository. Without it a Latin-script translation cannot be checked
 * at all — Spanish bundles no font of ours, so the only question is whether the
 * game's own font has `ñ`, and that question has an answer.
 */
function gameCoverage(base) {
  const p = path.join(cfg.PATHS.FONTS, 'GAME-COVERAGE.json');
  if (!fs.existsSync(p)) return null;
  const entry = JSON.parse(fs.readFileSync(p, 'utf8')).fonts[base];
  if (!entry) return null;
  const out = new Set();
  for (const [lo, hi] of entry.ranges) for (let c = lo; c <= hi; c += 1) out.add(c);
  return out;
}

/** The two font slots the stylesheet has, and what each will actually draw. */
function slots(L) {
  return ['everyday_standard', 'high_birth'].map((base) => {
    // On screen the stack is `original, ours, system`. The system font is a real
    // fallback but not one we can promise anything about, so what counts as covered
    // is the game's font plus whatever we put behind it.
    const game = gameCoverage(base);
    const ours = L.fonts.find((f) => f.replaces === base);
    const mine = ours ? cmapOf(path.join(cfg.PATHS.FONTS, ours.file)) : new Set();
    return { base, game, file: ours ? ours.file : null, mine };
  });
}

/**
 * Ranges a language has explicitly signed off as drawn by the reader's system font.
 *
 * No open pixel font covers Thai or Arabic at the sizes the game uses, so those
 * languages ship no font of ours and the system's takes over. That is a decision, not
 * an oversight, and it is written down in locale/languages.json as `systemScripts` —
 * a list of [first, last] code point pairs, with `note` saying why. Everything
 * outside those ranges is still checked, so a Thai translation that picks up a stray
 * em dash still fails.
 */
function signedOff(L) {
  const out = [];
  for (const [lo, hi] of L.systemScripts || []) out.push([lo, hi]);
  return (cp) => out.some(([lo, hi]) => cp >= lo && cp <= hi);
}

function check(lang) {
  const L = cfg.language(lang);
  const used = charactersOf(lang);
  if (!used.size) return { lang, skipped: 'no translation files' };

  // Every character is checked, not only the non-ASCII ones. An earlier version drew
  // the line at U+2000, which silently exempted every Cyrillic, Greek and accented
  // letter — the whole of a Russian translation sat under that threshold.
  const chars = [...used].filter((c) => c !== '\n' && c !== '\r');
  const system = signedOff(L);
  const missing = new Map();
  const delegated = new Set();
  let unchecked = 0;

  for (const s of slots(L)) {
    if (!s.game) { unchecked += 1; continue; }
    const gone = [];
    for (const c of chars) {
      const cp = c.codePointAt(0);
      if (s.game.has(cp) || s.mine.has(cp)) continue;
      if (system(cp)) { delegated.add(c); continue; }
      gone.push(c);
    }
    if (gone.length) missing.set(s.file ? `${s.base} + ${s.file}` : s.base, gone);
  }
  return { lang, used: chars.length, missing, unchecked, delegated: delegated.size };
}

function main() {
  const only = process.argv[2];
  const langs = only ? [only] : cfg.availableLanguages();
  let bad = 0;
  for (const lang of langs) {
    const r = check(lang);
    if (r.skipped) { console.log(`${lang}: skipped (${r.skipped})`); continue; }
    if (r.unchecked) {
      console.log(`${lang}: ${r.unchecked} slot(s) unchecked`
        + ' — run tools/make-game-coverage.py against the game\'s fonts');
    }
    if (!r.missing.size) {
      console.log(`${lang}: ${r.used} characters, all covered`
        + (r.delegated ? `, ${r.delegated} left to the system font by design` : ''));
      continue;
    }
    bad += 1;
    for (const [where, gone] of r.missing) {
      console.error(`${lang}: ${where} cannot draw ${gone.length} character(s)`);
      console.error(`  ${gone.slice(0, 60).join('')}`);
    }
  }
  return bad;
}

if (require.main === module) process.exit(main() ? 1 : 0);

module.exports = { charactersOf, cmapOf, check, main };

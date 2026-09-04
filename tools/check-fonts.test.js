'use strict';
// The woff2 cmap reader, checked against the fonts actually shipped.
//
// These assert on real files rather than a fixture because the bug being guarded
// against was a real font not containing what we assumed it did. A synthetic font
// would only prove the parser parses itself.

const test = require('node:test');
const assert = require('node:assert');
const path = require('path');
const fs = require('fs');
const cfg = require('../config');
const { cmapOf, check } = require('./check-fonts');


const font = (f) => cmapOf(path.join(cfg.PATHS.FONTS, f));
const cp = (c) => c.codePointAt(0);

test('a woff2 cmap is read, and comes back a plausible size', () => {
  const galmuri = font('Galmuri7.woff2');
  // Hangul syllables alone are 11,172; anything far below this means the table
  // directory walk landed in the wrong place and produced garbage.
  assert.ok(galmuri.size > 15000, `only found ${galmuri.size} characters`);
  assert.ok(galmuri.has(cp('가')));
  assert.ok(galmuri.has(cp('힣')));
  assert.ok(galmuri.has(cp('A')));
});

test('Galmuri does not contain simplified Chinese', () => {
  // Its 6,360 Han glyphs are the Korean hanja set — traditional forms. Reading the
  // glyph count as "covers Chinese too" is the mistake this file exists to catch.
  const galmuri = font('Galmuri7.woff2');
  assert.ok(galmuri.has(cp('龍')), 'the traditional form is there');
  assert.ok(!galmuri.has(cp('龙')), 'the simplified form is not');
});

test('Fusion Pixel contains both forms', () => {
  for (const f of ['FusionPixel8-zh_hans.woff2', 'FusionPixel10-zh_hans.woff2']) {
    const fp = font(f);
    assert.ok(fp.has(cp('龙')), `${f}: 龙`);
    assert.ok(fp.has(cp('龍')), `${f}: 龍`);
    assert.ok(fp.has(cp('가')), `${f}: Hangul, since the UI mixes languages`);
  }
});

test('a font is rejected rather than misread when it is not woff2', () => {
  assert.throws(() => font('OFL-Galmuri.txt'), /not woff2/);
});

test('every bundled language can draw its own translation', () => {
  for (const lang of cfg.availableLanguages()) {
    const r = check(lang);
    if (r.skipped) continue;
    const gaps = [...r.missing].map(([where, gone]) => `${where}: ${gone.join('')}`);
    assert.deepStrictEqual(gaps, [], `${lang} would render empty boxes`);
  }
});

test('both font slots are actually checked, not silently skipped', () => {
  // The check is only worth anything if it knows what the game's own fonts draw.
  // Without that file a Latin-script language passes by default, which is the
  // failure mode this whole tool exists to remove.
  const p = path.join(cfg.PATHS.FONTS, 'GAME-COVERAGE.json');
  assert.ok(fs.existsSync(p), 'run tools/make-game-coverage.py');
  for (const lang of cfg.availableLanguages()) {
    const r = check(lang);
    if (r.skipped) continue;
    assert.strictEqual(r.unchecked, 0, `${lang}: a font slot went unchecked`);
  }
});

test('the game font is credited for what it draws', () => {
  // Russian bundles a font for the heading slot only, because the game's own body
  // font already has Cyrillic. If that were not taken into account the language
  // would look uncoverable and someone would bundle a second font for nothing.
  const ru = cfg.language('ru');
  assert.strictEqual(ru.fonts.length, 1, 'only the heading slot is replaced');
  assert.strictEqual(ru.fonts[0].replaces, 'high_birth');
  assert.deepStrictEqual([...check('ru').missing], []);
});

test('a script no pixel font covers is delegated, but only where it was signed off', () => {
  // Thai ships no font of ours because none exists at these sizes. That is a decision
  // recorded in the catalogue, not a hole in the check: everything outside the
  // signed-off ranges is still checked, so a stray em dash in a Thai string fails.
  const th = cfg.language('th');
  assert.deepStrictEqual(th.fonts, [], 'Thai bundles no font');
  assert.ok(th.systemScripts.length, 'and says so, with the range it means');
  const r = check('th');
  assert.deepStrictEqual([...r.missing], [], 'nothing outside that range is uncovered');
  assert.ok(r.delegated > 0, 'and the Thai letters are accounted for, not ignored');

  for (const [lo, hi] of th.systemScripts) {
    assert.ok(lo <= 0x0e01 && hi >= 0x0e5b, `${lo}-${hi} should be the Thai block`);
  }
});

test('a language with no sign-off delegates nothing', () => {
  // The opt-out has to be opt-in. If it leaked, every language would pass.
  for (const lang of cfg.availableLanguages()) {
    const L = cfg.language(lang);
    if (L.systemScripts.length) continue;
    assert.strictEqual(check(lang).delegated, 0, `${lang} delegated without saying so`);
  }
});

test('the extended game fonts add glyphs and drop none', () => {
  // They are the game's own fonts with letters added, under CC BY 4.0. If a rebuild
  // ever loses a glyph the game itself draws, the game's own text breaks — so the
  // superset property is the thing to hold onto.
  const game = JSON.parse(fs.readFileSync(path.join(cfg.PATHS.FONTS, 'GAME-COVERAGE.json'), 'utf8'));
  for (const [base, file] of [
    ['everyday_standard', 'Everyday_Standard-bd.woff2'],
    ['high_birth', 'High_Birth-bd.woff2'],
  ]) {
    const ours = cmapOf(path.join(cfg.PATHS.FONTS, file));
    const lost = [];
    for (const [lo, hi] of game.fonts[base].ranges) {
      for (let c = lo; c <= hi; c += 1) if (!ours.has(c)) lost.push(c);
    }
    assert.deepStrictEqual(lost, [], `${file} lost glyphs the game's own font has`);
    assert.ok(ours.size > game.fonts[base].chars, `${file} added nothing`);
    // The letters the extension exists for.
    for (const ch of 'ČčĚěŘřŠšŤťŮůŽžŐőŰűĂăȘșȚț') {
      assert.ok(ours.has(ch.codePointAt(0)), `${file}: ${ch}`);
    }
  }
});

test('a language on the extended fonts needs no size correction', () => {
  // They are the same face on the same grid as the game's, so a size-adjust or an
  // ascent override would be correcting something that is not wrong.
  for (const f of cfg.language('cs').fonts) {
    assert.strictEqual(f.pxPerEm, f.basePxPerEm, `${f.file}: grids differ`);
    assert.strictEqual(f.ascentOverride, undefined, `${f.file}: overrides the metrics`);
    assert.strictEqual(f.descentOverride, undefined, `${f.file}: overrides the metrics`);
  }
});

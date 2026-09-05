'use strict';
// THIRD-PARTY.md publishes a sha256 for every font bundled here, and a statement of
// changes for the three it modifies. Both had quietly stopped being true: the extended
// fonts had gained 95 more glyphs than the statement named, and every build stamped
// head.modified with the clock, so no two builds of the same input agreed anyway.
//
// A licence file that says something false about the files beside it is worse than one
// that says nothing, and CC BY and the OFL both make the statement of changes an
// obligation rather than a courtesy. So it is a test.

const test = require('node:test');
const assert = require('node:assert');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const cfg = require('../config');
const { cmapOf } = require('./check-fonts');

const text = fs.readFileSync(path.join(__dirname, '..', 'THIRD-PARTY.md'), 'utf8');

/** Every `  <sha256>  <name>.woff2` line the document publishes. */
const published = () =>
  [...text.matchAll(/^ {2}([0-9a-f]{64}) {2}(\S+\.woff2)$/gm)]
    .map(([, hash, file]) => ({ hash, file }));

const font = (f) => cmapOf(path.join(cfg.PATHS.FONTS, f));
const sha256 = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

test('every hash in THIRD-PARTY.md is the file that ships', () => {
  const rows = published();
  // A floor, not a count. It is here so that a regex which quietly stops matching fails
  // loudly instead of passing over an empty list; the number of fonts is allowed to
  // change, and did when Galmuri11 was dropped for being 505 KB nothing used.
  assert.ok(rows.length >= 8, `only ${rows.length} hashes found; the format changed`);
  for (const { hash, file } of rows) {
    const p = path.join(cfg.PATHS.FONTS, file);
    assert.ok(fs.existsSync(p), `${file} is listed but not bundled`);
    assert.strictEqual(sha256(p), hash, `${file} is not the file THIRD-PARTY.md names`);
  }
});

test('every bundled source font is accounted for', () => {
  const listed = new Set(published().map((r) => r.file));
  // The per-language builds are cut from these by tools/build-webfonts.py and carry no
  // licence of their own; what is listed is the source each one comes from.
  for (const f of fs.readdirSync(cfg.PATHS.FONTS)) {
    if (!f.endsWith('.woff2') || f.startsWith('bd-')) continue;
    assert.ok(listed.has(f), `${f} is bundled but THIRD-PARTY.md does not list it`);
  }
});

test('the letters the statement of changes names are the letters in the font', () => {
  // The list is written out in the document, so count it there rather than trusting
  // the number beside it - that number is exactly what went stale.
  const listed = /`((?:[^`\s] )+[^`\s])`\.\nEveryday_Standard/.exec(text);
  assert.ok(listed, 'THIRD-PARTY.md no longer lists the letters that were added');
  const letters = listed[1].split(' ');

  const claimed = /High_Birth carries (\d+) of them/.exec(text);
  assert.ok(claimed, 'THIRD-PARTY.md no longer states how many High_Birth carries');
  assert.strictEqual(letters.length, Number(claimed[1]),
    'the count and the list in THIRD-PARTY.md disagree');

  const high = font('High_Birth-bd.woff2');
  const body = font('Everyday_Standard-bd.woff2');
  for (const ch of letters) {
    assert.ok(high.has(ch.codePointAt(0)), `High_Birth-bd is missing ${ch}`);
    assert.ok(body.has(ch.codePointAt(0)), `Everyday_Standard-bd is missing ${ch}`);
  }
});

// Monotonic Greek: twenty-four letters in both cases, the final sigma, and the accented
// forms a modern text actually uses. No polytonic breathings.
const GREEK = ('ΆΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
             + 'άέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώ');

test('the Greek the statement of changes claims is all there', () => {
  const claimed = /Everyday_Standard carries those 56 and (\d+) more/.exec(text);
  assert.ok(claimed, 'THIRD-PARTY.md no longer states what Everyday_Standard added');
  assert.strictEqual(Number(claimed[1]), GREEK.length);

  const body = font('Everyday_Standard-bd.woff2');
  for (const ch of GREEK) {
    assert.ok(body.has(ch.codePointAt(0)), `Everyday_Standard-bd is missing ${ch}`);
  }

  // The heading font is Galmuri's, and only the seven accented capitals are ours.
  const heading = font('Galmuri9-bd.woff2');
  for (const ch of GREEK) {
    assert.ok(heading.has(ch.codePointAt(0)), `Galmuri9-bd is missing ${ch}`);
  }
  const original = font('Galmuri9.woff2');
  const added = [...GREEK].filter((ch) => !original.has(ch.codePointAt(0)));
  assert.deepStrictEqual(added, [...'ΆΈΉΊΌΎΏ'],
    'Galmuri9 now differs from the seven letters the statement of changes claims');
});

test('the fonts we extended are additions only', () => {
  // The whole licence position rests on this: the originals are untouched and only
  // gained glyphs. A build that dropped one would still hash consistently.
  const pairs = [
    ['Galmuri9.woff2', 'Galmuri9-bd.woff2'],
  ];
  for (const [before, after] of pairs) {
    const a = font(before);
    const b = font(after);
    const lost = [...a].filter((c) => !b.has(c));
    assert.deepStrictEqual(lost, [], `${after} lost ${lost.length} of ${before}'s glyphs`);
  }
});

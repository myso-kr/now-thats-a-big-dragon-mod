'use strict';
// The documents publish numbers - twenty-two languages, 51.10% of Steam, 620 strings,
// 142 Rust tests - and every one of them was true when it was written. That is the
// problem: THIRD-PARTY.md's font hashes had already gone stale once, and the Korean page
// spent months describing a design the code had replaced.
//
// So the claims are a test. Anything countable from the repository is counted here; the
// one number that cannot be (the JavaScript test total, which loops produce at runtime)
// is checked by the CI workflow against the runner's own summary.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const read = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');

/** Every language with a built i18n table - the same test build-site.py applies. */
const shipping = () => {
  const cat = JSON.parse(read('locale/languages.json')).languages;
  return Object.keys(cat).filter((c) => fs.existsSync(path.join(ROOT, 'locale', `i18n.${c}.json`)));
};

const DOCS = ['README.md', 'CHANGELOG.md', 'THIRD-PARTY.md', 'translations/README.md',
              'docs/index.md', 'docs/ko/index.md', 'docs/llms.txt', 'docs/DESIGN.md',
              'docs/ANCHORS.md', 'docs/CONVENTIONS.md'];

test('the language count every document publishes is the number that ships', () => {
  const n = shipping().length;
  assert.ok(n >= 20, `only ${n} languages have an i18n table; the layout changed`);
  for (const doc of DOCS) {
    const text = read(doc);
    // "22 languages", "22개 언어", "22-language" - the number, then the word, in any script.
    for (const [, claimed] of text.matchAll(/(\d+)\s*(?:languages|-language|개 언어|개언어)/g)) {
      assert.strictEqual(Number(claimed), n, `${doc} says ${claimed} languages; ${n} ship`);
    }
  }
});

test('the Steam share every document publishes is the sum of what ships', () => {
  const cat = JSON.parse(read('locale/languages.json')).languages;
  const total = shipping().reduce((s, c) => s + (cat[c].steamShare || 0), 0);
  const said = total.toFixed(2);
  for (const doc of DOCS) {
    for (const [, claimed] of read(doc).matchAll(/(\d+\.\d\d)%\s*(?:of Steam|의 스팀|Steam)/g)) {
      assert.strictEqual(claimed, said, `${doc} says ${claimed}%; the catalogue sums to ${said}%`);
    }
  }
});

test('the string and dialogue counts are the files that exist', () => {
  const leaves = (o) =>
    typeof o !== 'object' || o === null ? 1 : Object.values(o).reduce((n, v) => n + leaves(v), 0);
  const strings = leaves(JSON.parse(read('locale/i18n.ko.json')));
  const dialogs = fs.readdirSync(path.join(ROOT, 'locale', 'dialogs', 'ko'))
    .filter((f) => f.endsWith('.ink')).length;
  for (const doc of DOCS) {
    const text = read(doc);
    for (const [, claimed] of text.matchAll(/(\d+)\s*(?:UI strings|UI 문자열)/g)) {
      assert.strictEqual(Number(claimed), strings, `${doc} claims ${claimed} strings; there are ${strings}`);
    }
    for (const [, claimed] of text.matchAll(/(\d+)\s*(?:dialogue scripts|개 대사 파일)/g)) {
      assert.strictEqual(Number(claimed), dialogs, `${doc} claims ${claimed} dialogues; there are ${dialogs}`);
    }
  }
});

test('the Rust test count is the number of #[test] in the tree', () => {
  const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) return e.name === 'target' ? [] : walk(p);
    return e.name.endsWith('.rs') ? [p] : [];
  });
  const n = [...walk(path.join(ROOT, 'src')), ...walk(path.join(ROOT, 'tests'))]
    .reduce((s, p) => s + (fs.readFileSync(p, 'utf8').match(/#\[test\]/g) || []).length, 0);
  for (const doc of DOCS) {
    for (const [, claimed] of read(doc).matchAll(/(\d+)(?:%20)?\s*Rust(?:%20)?\s*tests?/g)) {
      assert.strictEqual(Number(claimed), n, `${doc} claims ${claimed} Rust tests; there are ${n}`);
    }
  }
});

test('NOTICE accounts for every translation and every bundled font', () => {
  // NOTICE is the summary that travels inside the release zip, and it is the document
  // a rights holder or a font author would read first. It had gone a long way stale:
  // it covered the Korean translation alone while twenty-one others shipped beside it,
  // and listed a Galmuri file that had been deleted while omitting the two CC BY fonts
  // the binary actually embeds.
  const notice = read('NOTICE');

  for (const code of shipping()) {
    assert.ok(notice.includes(code), `NOTICE does not mention the ${code} translation`);
  }

  // Every font that ships, minus the per-language subsets, which NOTICE covers as a class.
  const fonts = fs.readdirSync(path.join(ROOT, 'locale', 'fonts'))
    .filter((f) => f.endsWith('.woff2') && !f.startsWith('bd-'));
  for (const f of fonts) {
    // FusionPixel8-ja and its siblings are named with a brace expansion in NOTICE.
    const family = f.replace(/-(zh_hans|zh_hant|ja)\.woff2$/, '');
    assert.ok(notice.includes(f) || notice.includes(family),
      `NOTICE does not account for ${f}`);
  }

  // And the licence texts it points at have to be there to point at.
  for (const [, ref] of notice.matchAll(/locale\/fonts\/([A-Za-z0-9.\-]+\.txt)/g)) {
    assert.ok(fs.existsSync(path.join(ROOT, 'locale', 'fonts', ref)),
      `NOTICE cites locale/fonts/${ref}, which is not bundled`);
  }

  // CC BY 4.0 makes the statement of changes a condition, not a courtesy.
  assert.match(notice, /STATEMENT OF CHANGES/,
    'NOTICE no longer carries the statement of changes CC BY 4.0 requires');
});

test('the release notes will name the game builds that were verified', () => {
  // The Release workflow composes its notes from package.json, not from the fingerprint
  // record - so these two drifting apart publishes a release that tells players the
  // version most of them are on was never checked. It had already drifted by one game.
  const fp = JSON.parse(read('generated/fingerprint.json')).supported;
  const pkg = JSON.parse(read('package.json')).bigDragon;
  assert.deepStrictEqual(pkg.supportedGameVersions, fp.map((e) => e.gameVersion),
    'package.json and generated/fingerprint.json disagree about which games were verified');
  assert.deepStrictEqual(pkg.supportedBuildIds, fp.map((e) => e.steamBuildId),
    'package.json and generated/fingerprint.json disagree about the Steam build ids');
});

test('no document names a file that is not there', () => {
  // Backticked paths only - prose names things loosely, but `patch/fonts/` is a promise.
  // A reference is matched as a suffix of a real path, so `fonts/bd-ko-*.woff2` resolves
  // against locale/fonts without every document having to spell the prefix out.
  const ELSEWHERE = new Set([
    'patcher.rs', 'helpers', 'utils',              // named as counter-examples in CONVENTIONS
    'flags/4x3',                                   // a path inside lipis/flag-icons, cited as its source
    'assets/index-', 'assets/style-',              // paths inside the game's own bundle
    'dungeon-crawler/tiles', 'dialogs/en',
    'undefined/undefined',                         // a value a bug printed, quoted in CHANGELOG
  ]);
  const outside = (ref) => [...ELSEWHERE].some((e) => ref.startsWith(e));

  const all = [];
  const walk = (dir, rel) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (['node_modules', 'target', '.git', '__pycache__', '_site'].includes(e.name)) continue;
      const r = rel ? `${rel}/${e.name}` : e.name;
      all.push(r);
      if (e.isDirectory()) walk(path.join(dir, e.name), r);
    }
  };
  walk(ROOT, '');
  const known = new Set(all);
  const suffix = (ref) => known.has(ref) || all.some((p) => p.endsWith(`/${ref}`));

  const missing = [];
  for (const doc of DOCS) {
    for (const [, ref] of read(doc).matchAll(/`([a-zA-Z0-9_\-]+(?:\/[a-zA-Z0-9_.*\-]+)+\/?)`/g)) {
      if (outside(ref)) continue;
      const bare = ref.replace(/\/$/, '').replace(/\/[^/]*\*.*$/, '');   // the directory a glob lives in
      if (!suffix(bare)) missing.push(`${doc}: \`${ref}\``);
    }
  }
  const dead = [...new Set(missing)];
  assert.deepStrictEqual(dead, [], `documents name paths that do not exist:\n  ${dead.join('\n  ')}`);
});

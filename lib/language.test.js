'use strict';
// Language selection, checked against a small catalogue rather than the real one, so
// the cases stay readable and adding a language cannot break these tests.

const test = require('node:test');
const assert = require('node:assert');
const { normalise, primary, match, resolve } = require('./language');

const CATALOGUE = {
  gameSupports: ['en', 'fr', 'de', 'pt', 'tr'],
  languages: {
    ko: { matches: ['ko'] },
    ja: { matches: ['ja'] },
    'zh-Hans': { matches: ['zh-hans', 'zh-cn', 'zh'] },
    'zh-Hant': { matches: ['zh-hant', 'zh-tw', 'zh-hk'] },
    fil: { matches: ['fil', 'tl'] },
    de: { matches: ['de'] },
  },
};
const HAVE = ['ko', 'ja', 'zh-Hans', 'zh-Hant', 'fil', 'de'];

test('locales are normalised whatever shape they arrive in', () => {
  assert.strictEqual(normalise('ko_KR.UTF-8'), 'ko-kr');
  assert.strictEqual(normalise('ko-KR'), 'ko-kr');
  assert.strictEqual(normalise('  ja  '), 'ja');
  assert.strictEqual(normalise(undefined), '');
  assert.strictEqual(primary('zh-Hant-TW'), 'zh');
});

test('a plain language matches', () => {
  assert.strictEqual(match(CATALOGUE, 'ko-KR'), 'ko');
  assert.strictEqual(match(CATALOGUE, 'ja-JP'), 'ja');
});

test('a longer prefix wins, so scripts are distinguished', () => {
  assert.strictEqual(match(CATALOGUE, 'zh-Hant-TW'), 'zh-Hant');
  assert.strictEqual(match(CATALOGUE, 'zh-TW'), 'zh-Hant');
  assert.strictEqual(match(CATALOGUE, 'zh-CN'), 'zh-Hans');
  assert.strictEqual(match(CATALOGUE, 'zh'), 'zh-Hans', 'bare zh takes the simplified default');
});

test('a language with two names matches on either', () => {
  assert.strictEqual(match(CATALOGUE, 'fil-PH'), 'fil');
  assert.strictEqual(match(CATALOGUE, 'tl-PH'), 'fil');
});

test('a prefix must end at a subtag boundary', () => {
  // `kok` (Konkani) is not Korean.
  assert.strictEqual(match(CATALOGUE, 'kok-IN'), null);
});

test('an unknown locale matches nothing', () => {
  assert.strictEqual(match(CATALOGUE, 'sv-SE'), null);
  assert.strictEqual(match(CATALOGUE, ''), null);
});

test('the system locale decides when we have that language', () => {
  const r = resolve(CATALOGUE, { locale: 'ko-KR', available: HAVE });
  assert.strictEqual(r.lang, 'ko');
  assert.match(r.reason, /system locale/);
});

test('a language the game already speaks is left to the game', () => {
  const r = resolve(CATALOGUE, { locale: 'de-DE', available: HAVE });
  assert.strictEqual(r.lang, null);
  assert.match(r.reason, /natively/);
});

test('a language we have no files for is not applied', () => {
  const r = resolve(CATALOGUE, { locale: 'ja-JP', available: ['ko'] });
  assert.strictEqual(r.lang, null);
  assert.match(r.reason, /no ja translation/);
});

test('an unknown system locale leaves the game as it is', () => {
  const r = resolve(CATALOGUE, { locale: 'sv-SE', available: HAVE });
  assert.strictEqual(r.lang, null);
  assert.match(r.reason, /system locale/);
});

test('an explicit request overrides the system locale', () => {
  const r = resolve(CATALOGUE, { requested: 'ja', locale: 'ko-KR', available: HAVE });
  assert.strictEqual(r.lang, 'ja');
  assert.match(r.reason, /requested/);
});

test('an explicit request wins even over a language the game supports', () => {
  // Asking for it is deliberate; the game's own German is then overridden.
  const r = resolve(CATALOGUE, { requested: 'de', locale: 'en-US', available: HAVE });
  assert.strictEqual(r.lang, 'de');
});

test('an explicit request we cannot honour says so, and lists what there is', () => {
  const r = resolve(CATALOGUE, { requested: 'sv', locale: 'ko-KR', available: HAVE });
  assert.strictEqual(r.lang, null, 'it must not silently fall back to Korean');
  assert.match(r.reason, /no translation for sv/);
  assert.match(r.reason, /have: ko/);
});

test('a request in full locale form is accepted', () => {
  assert.strictEqual(resolve(CATALOGUE, { requested: 'ko-KR', available: HAVE }).lang, 'ko');
});

test('with nothing available, nothing is applied', () => {
  const r = resolve(CATALOGUE, { locale: 'ko-KR', available: [] });
  assert.strictEqual(r.lang, null);
});

test('the shipped catalogue is well formed', () => {
  const real = require('../locale/languages.json');
  assert.ok(Array.isArray(real.gameSupports) && real.gameSupports.includes('en'));
  for (const [lang, def] of Object.entries(real.languages)) {
    assert.ok(Array.isArray(def.matches) && def.matches.length, `${lang}: needs matches`);
    assert.ok(Array.isArray(def.fonts), `${lang}: needs a fonts list`);
    assert.ok(Array.isArray(def.fallback), `${lang}: needs a system fallback`);
    assert.ok(
      !real.gameSupports.includes(lang),
      `${lang}: the game already ships this, so patching it in is pointless`,
    );
    for (const f of def.fonts) {
      for (const k of ['replaces', 'family', 'file', 'url', 'pxPerEm', 'basePxPerEm']) {
        assert.ok(f[k] !== undefined, `${lang}/${f.file}: missing ${k}`);
      }
    }
  }
});

test('an explicit script-tagged code is not reduced to its primary subtag', () => {
  // `zh-Hans` and `zh-Hant` are different languages here; collapsing either to `zh`
  // picks the wrong one, or nothing at all.
  const r = resolve(CATALOGUE, { requested: 'zh-Hans', available: HAVE });
  assert.strictEqual(r.lang, 'zh-Hans');
  assert.strictEqual(resolve(CATALOGUE, { requested: 'zh-Hant', available: HAVE }).lang, 'zh-Hant');
});

test('an explicit full locale still resolves through the catalogue', () => {
  assert.strictEqual(resolve(CATALOGUE, { requested: 'zh-Hant-TW', available: HAVE }).lang, 'zh-Hant');
  assert.strictEqual(resolve(CATALOGUE, { requested: 'ko-KR', available: HAVE }).lang, 'ko');
});

'use strict';
// Adding a language to the game's own list, checked against fixtures shaped like the
// real bundle.

const test = require('node:test');
const assert = require('node:assert');
const locale = require('./locale');
const i18n = require('./i18n');

/** The four shapes this module edits, in one string, as the bundle has them. */
const BUNDLE = [
  'var MLe={',
  `en:{${i18n.NAMESPACES.map((ns, n) => `${ns}:E${n}`).join(',')}},`,
  `fr:{${i18n.NAMESPACES.map((ns, n) => `${ns}:F${n}`).join(',')}}`,
  '},M7=["en","fr","de","pt","tr"],pF="en";',
  'var BGe={en:"us.png",fr:"fr.png",de:"de.png",pt:"br.png",tr:"tr.png"};',
  'var E4={language:"Language",languages:{en:"English",fr:"French",de:"German",pt:"Portuguese",tr:"Turkish"}};',
  'var F4={language:"Langue",languages:{en:"Anglais",fr:"Français",de:"Allemand",pt:"Portugais",tr:"Turc"}};',
].join('');

const TABLES = { common: { hello: '안녕' } };

test('a locale is inserted into the resources object', () => {
  const r = locale.addLocale(BUNDLE, 'ko', TABLES);
  assert.strictEqual(r.ok, true);
  assert.ok(r.code.includes('"ko":{"common":{"hello":"안녕"}}'));
  assert.ok(r.code.includes('en:{upgrades:E0'), 'the English entry is left alone');
});

test('the inserted locale sits inside the resources object, before en', () => {
  const r = locale.addLocale(BUNDLE, 'ko', TABLES);
  assert.ok(r.code.indexOf('"ko":') > r.code.indexOf('var MLe={'));
  assert.ok(r.code.indexOf('"ko":') < r.code.indexOf('en:{upgrades:'));
});

test('a bundle with no resources object is reported, not guessed at', () => {
  const r = locale.addLocale('var x=1;', 'ko', TABLES);
  assert.strictEqual(r.ok, false);
  assert.match(r.reason, /resources/);
});

test('the code joins the supported list', () => {
  const r = locale.addSupported(BUNDLE, 'ko');
  assert.strictEqual(r.ok, true);
  assert.ok(r.code.includes('["en","fr","de","pt","tr","ko"]'));
});

test('the flag map gains an entry', () => {
  const r = locale.addFlag(BUNDLE, 'ko', 'kr.png');
  assert.strictEqual(r.ok, true);
  assert.ok(r.code.includes('tr:"tr.png","ko":"kr.png"}'));
});

test('every locale learns the new language name', () => {
  const r = locale.addLabels(BUNDLE, 'ko', '한국어');
  assert.strictEqual(r.count, 2, 'both the English and the French settings tables');
  assert.ok(r.code.includes('tr:"Turkish","ko":"한국어"'));
  assert.ok(r.code.includes('tr:"Turc","ko":"한국어"'));
});

test('the same name is used in every locale, since a language names itself best', () => {
  const r = locale.addLabels(BUNDLE, 'ko', '한국어');
  assert.strictEqual((r.code.match(/"ko":"한국어"/g) || []).length, 2);
});

test('the whole thing together reports each anchor', () => {
  const r = locale.addLanguage(BUNDLE, {
    lang: 'ko', label: '한국어', flagFile: 'kr.png', tables: TABLES,
  });
  assert.deepStrictEqual(r.report, {
    lang: 'ko',
    resources: true,
    supported: true,
    flag: true,
    labels: 2,
    // The fixture has neither a Scale nor a settings-defaults object.
    timeScale: false,
    default: false,
  });
});

test('losing the settings anchors still leaves the translation in place', () => {
  // A game update that moves the settings UI must not cost us the translation.
  const partial = BUNDLE
    .replace('M7=["en","fr","de","pt","tr"]', 'M7=SOMETHING_ELSE')
    .replace(/\{en:"us\.png"[^}]*\}/, '{}')
    .replace(/languages:\{[^}]*\}/g, 'languages:{}');
  const r = locale.addLanguage(partial, {
    lang: 'ko', label: '한국어', flagFile: 'kr.png', tables: TABLES,
  });
  assert.strictEqual(r.report.resources, true, 'the locale still went in');
  assert.strictEqual(r.report.supported, false);
  assert.strictEqual(r.report.flag, false);
  assert.strictEqual(r.report.labels, 0);
});

test('without the resources anchor nothing is changed at all', () => {
  const r = locale.addLanguage('var x=1;', {
    lang: 'ko', label: '한국어', flagFile: 'kr.png', tables: TABLES,
  });
  assert.strictEqual(r.code, 'var x=1;');
  assert.strictEqual(r.report.resources, false);
});

test('the patched bundle is still parseable JavaScript', () => {
  const r = locale.addLanguage(BUNDLE, {
    lang: 'ko', label: '한국어', flagFile: 'kr.png', tables: TABLES,
  });
  // The fixture references undefined identifiers, so only parse it, do not run it.
  assert.doesNotThrow(() => new Function(`if(0){${r.code}}`));
});

test('a table containing quotes and newlines survives serialisation', () => {
  const tricky = { common: { q: 'say "hi"', n: 'a\nb', s: 'back\\slash' } };
  const r = locale.addLocale(BUNDLE, 'ko', tricky);
  const value = new Function(`return {${r.code.slice(r.code.indexOf('"ko":'), r.code.indexOf(',en:{'))}}`)();
  assert.deepStrictEqual(value.ko, tricky);
});

test('a fresh profile starts in the added language', () => {
  const defaults = 'a={musicVolume:25,chromaticAberration:10,largerTextSize:!1,language:"en"};';
  const r = locale.setDefaultLanguage(defaults, 'ko');
  assert.strictEqual(r.ok, true);
  assert.ok(r.code.includes('largerTextSize:!1,language:"ko"'));
});

test('only the default is changed, never a persisted choice', () => {
  // The pattern is anchored to the neighbouring defaults, so a `language:"en"`
  // anywhere else in the bundle is left alone.
  const other = 'x={language:"en"};a={chromaticAberration:10,largerTextSize:!1,language:"en"};';
  const r = locale.setDefaultLanguage(other, 'ko');
  assert.ok(r.code.startsWith('x={language:"en"}'), 'the unrelated one is untouched');
  assert.strictEqual((r.code.match(/language:"ko"/g) || []).length, 1);
});

test('a missing defaults object is reported', () => {
  assert.strictEqual(locale.setDefaultLanguage('var x=1;', 'ko').ok, false);
});

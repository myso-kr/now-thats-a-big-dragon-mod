'use strict';
// The translation workbench's validation, which is the only thing standing between a
// machine-drafted TSV and a broken string on screen.

const test = require('node:test');
const assert = require('node:assert');
const {
  flatten, nest, problems, pluralCategories, sourceFor, mixedScript,
} = require('./translate');

const EN = new Map([
  ['upgrades.title', 'Upgrades'],
  ['upgrades.multiplier', '+{{multi}}'],
  ['generators.bard_one', 'Bard'],
  ['generators.bard_other', 'Bards'],
]);

test('a flat map and the nested shape round-trip', () => {
  const nested = nest(EN);
  assert.deepStrictEqual(nested.generators, { bard_one: 'Bard', bard_other: 'Bards' });
  assert.deepStrictEqual([...flatten(nested)], [...EN]);
});

test('a translation that keeps its placeholders passes', () => {
  const tr = new Map([['upgrades.multiplier', '+{{multi}}배']]);
  assert.deepStrictEqual(problems(EN, tr, 'ko'), []);
});

test('a dropped placeholder is caught', () => {
  const tr = new Map([['upgrades.multiplier', '+배']]);
  const bad = problems(EN, tr, 'ko');
  assert.strictEqual(bad.length, 1);
  assert.match(bad[0], /placeholders differ/);
});

test('a renamed placeholder is caught, since the game interpolates by name', () => {
  const tr = new Map([['upgrades.multiplier', '+{{multiplier}}배']]);
  assert.match(problems(EN, tr, 'ko')[0], /placeholders differ/);
});

test('a key the game does not have is caught', () => {
  const tr = new Map([['upgrades.nonsense', '아무거나']]);
  assert.match(problems(EN, tr, 'ko')[0], /not a key the game has/);
});

test('a missing key is not a problem — the merge falls back to English', () => {
  assert.deepStrictEqual(problems(EN, new Map(), 'ko'), []);
});

test('an empty translation is skipped rather than flagged', () => {
  assert.deepStrictEqual(problems(EN, new Map([['upgrades.multiplier', '']]), 'ko'), []);
});

test('a language reports the plural categories CLDR gives it', () => {
  assert.deepStrictEqual([...pluralCategories('ko')].sort(), ['other']);
  assert.deepStrictEqual([...pluralCategories('ru')].sort(), ['few', 'many', 'one', 'other']);
  assert.deepStrictEqual([...pluralCategories('en')].sort(), ['one', 'other']);
});

test('an unknown language falls back to the English pair rather than throwing', () => {
  assert.deepStrictEqual([...pluralCategories('not-a-language')].sort(), ['one', 'other']);
});

test('Russian may add the plural forms English has no word for', () => {
  // English shows two forms, Russian needs four. Rejecting `_few` as an unknown key
  // would reject every correct Russian translation.
  const tr = new Map([
    ['generators.bard_one', 'бард'],
    ['generators.bard_few', 'барда'],
    ['generators.bard_many', 'бардов'],
    ['generators.bard_other', 'барда'],
  ]);
  assert.deepStrictEqual(problems(EN, tr, 'ru'), []);
});

test('a plural form the language does not use is still caught', () => {
  const tr = new Map([['generators.bard_few', '음유시인']]);
  const bad = problems(EN, tr, 'ko');
  assert.strictEqual(bad.length, 1);
  assert.match(bad[0], /no "few" plural form/);
});

test('an extra plural form is checked against the English plural, not skipped', () => {
  const en = new Map([['n.item_other', '{{count}} items']]);
  const tr = new Map([['n.item_few', 'предмета']]);
  assert.match(problems(en, tr, 'ru')[0], /placeholders differ/);
});

test('the English string a plural form is checked against is the plural one', () => {
  assert.strictEqual(sourceFor(EN, 'generators.bard_few'), 'Bards');
  assert.strictEqual(sourceFor(EN, 'generators.bard_one'), 'Bard');
  assert.strictEqual(sourceFor(EN, 'generators.lute_few'), undefined);
});

test('a Latin letter inside a Cyrillic word is caught', () => {
  // Both letters are in the font, so it renders — it just spells the word wrong.
  // Nothing else in this file would notice.
  assert.deepStrictEqual(mixedScript('Pятуйте'), ['Pятуйте (Latin + Cyrillic)']);
  assert.deepStrictEqual(mixedScript('гриндy'), ['гриндy (Latin + Cyrillic)']);
});

test('a hyphen or a space separates words, so a borrowed term is not a mix', () => {
  assert.deepStrictEqual(mixedScript('CRT-фільтр'), []);
  assert.deepStrictEqual(mixedScript('Discord-сервера'), []);
  assert.deepStrictEqual(mixedScript('WASD або стрілки'), []);
  assert.deepStrictEqual(mixedScript('Клікайте або тисніть Z'), []);
});

test('a translation that borrows an English word from the source passes', () => {
  const en = new Map([['a', 'Join the Discord']]);
  assert.deepStrictEqual(problems(en, new Map([['a', 'Приєднатися до Discord']]), 'uk'), []);
});

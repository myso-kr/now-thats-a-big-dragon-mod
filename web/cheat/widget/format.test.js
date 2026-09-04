'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { num, fmt, short } = require('./format.js');

test('typed numbers tolerate the separators people paste in', () => {
  assert.strictEqual(num('1,234,567'), 1234567);
  assert.strictEqual(num('1 000'), 1000);
  assert.strictEqual(num('1_000'), 1000);
  assert.strictEqual(num('42'), 42);
  assert.strictEqual(num('1e6'), 1000000);
});

test('nonsense is null, not NaN, so callers can test for it', () => {
  assert.strictEqual(num('abc'), null);
  assert.strictEqual(num(''), 0, 'an empty box reads as zero');
  assert.strictEqual(num('Infinity'), null, 'not finite, so not a value');
});

test('a missing value shows as a dash rather than undefined', () => {
  assert.strictEqual(fmt(undefined), '—');
  assert.strictEqual(fmt(null), '—');
  assert.strictEqual(short(undefined), '—');
  assert.strictEqual(short(NaN), '—');
  assert.strictEqual(short(Infinity), '—');
});

test('short keeps three significant figures so columns line up', () => {
  assert.strictEqual(short(1234567), '1.23M');
  assert.strictEqual(short(12345678), '12.3M');
  assert.strictEqual(short(123456789), '123M');
  assert.strictEqual(short(1500), '1.50K');
  assert.strictEqual(short(1.5e12), '1.50T');
});

test('small numbers are shown whole', () => {
  assert.strictEqual(short(999), '999');
  assert.strictEqual(short(0), '0');
  assert.strictEqual(short(12.7), '12');
});

test('negatives keep their sign and their magnitude', () => {
  assert.strictEqual(short(-1234567), '-1.23M');
});

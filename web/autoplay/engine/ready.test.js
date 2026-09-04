'use strict';
// The latch has to distinguish "not computed yet" from "genuinely zero right now".

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./ready.js');

const s = (level, stats, hp, gold) => ({ level, stats, hp, gold });

// The latch needs three samples before it can fire: the first registers the level,
// the second records the baseline counters, and only the third can see them move.
function prime(r, level, stats, hp, gold) {
  r.update(s(level, stats, hp, gold));
  r.update(s(level, stats, hp, gold));
}
const EMPTY = {};
const LIVE = { warrior: { mainIndividualGenerationStat: 3 } };

test('an empty table is never ready', () => {
  const r = create({});
  prime(r, 'mainGame', EMPTY, 100, 0);
  r.update(s('mainGame', EMPTY, 90, 10));
  assert.strictEqual(r.on, false);
});

test('a filled table alone is not enough - a tick must have run', () => {
  const r = create({});
  r.update(s('mainGame', LIVE, 100, 0));
  assert.strictEqual(r.on, false, 'first sample only records a baseline');
});

test('falling boss HP counts as a tick', () => {
  const r = create({});
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 99, 0));
  assert.strictEqual(r.on, true);
});

test('rising gold also counts as a tick', () => {
  const r = create({});
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 100, 5));
  assert.strictEqual(r.on, true);
});

test('once on, it stays on even if the table empties out', () => {
  const r = create({});
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 99, 0));
  r.update(s('mainGame', EMPTY, 98, 0));
  assert.strictEqual(r.on, true, 'a mana drought must not read as not-yet-computed');
});

test('changing level starts the latch over', () => {
  const r = create({});
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 99, 0));
  assert.strictEqual(r.on, true);
  r.update(s('newGamePlus', LIVE, 500, 0));
  assert.strictEqual(r.on, false, 'a new chapter is a new run');
});

test('reset covers restarting the same chapter, where the level name does not change', () => {
  const r = create({});
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 99, 0));
  assert.strictEqual(r.on, true);
  r.reset();
  assert.strictEqual(r.on, false);
  r.update(s('mainGame', LIVE, 100, 0));
  assert.strictEqual(r.on, false, 'after a reset it needs a fresh tick');
});

test('a non-finite entry does not make the table look ready', () => {
  const r = create({});
  const bad = { warrior: { mainIndividualGenerationStat: Infinity } };
  prime(r, 'mainGame', bad, 100, 0);
  r.update(s('mainGame', bad, 99, 0));
  assert.strictEqual(r.on, false);
});

test('it announces itself exactly once', () => {
  const lines = [];
  const r = create({ log: (tag, text) => lines.push(text) });
  prime(r, 'mainGame', LIVE, 100, 0);
  r.update(s('mainGame', LIVE, 99, 0));
  r.update(s('mainGame', LIVE, 98, 0));
  assert.strictEqual(lines.length, 1);
});

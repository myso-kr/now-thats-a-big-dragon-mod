'use strict';
// Checks the purchase arithmetic against the game's formulas, without the game.

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./cost.js');

const c = create({ PERIOD_UPGRADE: { thief: 'fastHands' } });

test('a flat price is just base times n', () => {
  assert.strictEqual(c.costOf(10, 1, 0, 5), 50);
  assert.strictEqual(c.costOf(10, 1, 99, 5), 50, 'growth 1 ignores what is owned');
});

test('a growing price is the geometric series, not base times n', () => {
  // 10 + 11 + 12.1 = 33.1, whereas base*n would say 30.
  assert.ok(Math.abs(c.costOf(10, 1.1, 0, 3) - 33.1) < 1e-9);
});

test('already-owned copies move the starting price', () => {
  // Owning 2 means the next one costs 10 * 1.1^2.
  assert.ok(Math.abs(c.costOf(10, 1.1, 2, 1) - 12.1) < 1e-9);
});

test('maxAffordable is the exact inverse of costOf', () => {
  for (const growth of [1, 1.07, 1.15]) {
    for (const purchased of [0, 3, 20]) {
      const n = c.maxAffordable(100000, 10, growth, purchased);
      assert.ok(c.costOf(10, growth, purchased, n) <= 100000, `n=${n} must be affordable`);
      assert.ok(c.costOf(10, growth, purchased, n + 1) > 100000, `n+1 must not be`);
    }
  }
});

test('no gold buys nothing, and neither does a free item', () => {
  assert.strictEqual(c.maxAffordable(0, 10, 1.1, 0), 0);
  assert.strictEqual(c.maxAffordable(100, 0, 1.1, 0), 0);
  assert.strictEqual(c.maxAffordable(-5, 10, 1.1, 0), 0);
});

test('the effective period follows the game dp(), not the stored value', () => {
  const snap = {
    gen: { thief: { ticksToGenerate: 5 }, warrior: { ticksToGenerate: 1 } },
    up: { thief: { fastHands: { multiplier: -4 } } },
  };
  assert.strictEqual(c.effectivePeriod(snap, 'thief'), 1, '5 + (-4) = 1');
  assert.strictEqual(c.effectivePeriod(snap, 'warrior'), 1, 'no period upgrade, use stored');
});

test('the period never drops below one tick', () => {
  const snap = { gen: { thief: { ticksToGenerate: 5 } }, up: { thief: { fastHands: { multiplier: -99 } } } };
  assert.strictEqual(c.effectivePeriod(snap, 'thief'), 1);
});

test('an unowned upgrade leaves the stored period alone', () => {
  const snap = { gen: { thief: { ticksToGenerate: 5 } }, up: {} };
  assert.strictEqual(c.effectivePeriod(snap, 'thief'), 5);
});

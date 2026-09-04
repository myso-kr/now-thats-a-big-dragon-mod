'use strict';
// Resource bookkeeping, checked without the game.

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./resource.js');

const r = create({
  RESOURCES: ['food', 'wood', 'ore'],
  RESOURCE_UNITS: { farmer: 'food', lumberjack: 'wood', miner: 'ore' },
  UPKEEP: { warrior: { ore: 1 }, wizard: { food: 1 }, outpost: { food: 1, wood: 3 } },
});

/** A resource chapter with the given units owned and stockpiles. */
function snap(owned, stock, perUnit) {
  const gen = {};
  for (const [id, n] of Object.entries(owned)) gen[id] = { owned: n, isUnlocked: true };
  const stats = {};
  for (const [id, v] of Object.entries(perUnit || {})) stats[id] = { mainIndividualGenerationStat: v };
  return Object.assign({ level: 'newGamePlus', gen, stats }, stock);
}

test('flow is production minus upkeep', () => {
  const s = snap({ farmer: 2, wizard: 3 }, { food: 100 }, { farmer: 10 });
  assert.strictEqual(r.resourceFlow(s).food, 17, '2 farmers at 10 = 20, minus 3 wizards');
});

test('a unit with several upkeep lines is charged on each', () => {
  const s = snap({ outpost: 2 }, {}, {});
  const flow = r.resourceFlow(s);
  assert.strictEqual(flow.food, -2);
  assert.strictEqual(flow.wood, -6);
});

test('runway is stock divided by the worst drain', () => {
  const s = snap({ wizard: 2 }, { food: 100, wood: 0, ore: 0 }, {});
  assert.strictEqual(r.runway(s), 50, '100 food draining at 2/s');
});

test('a positive flow never runs out', () => {
  const s = snap({ farmer: 5 }, { food: 10, wood: 0, ore: 0 }, { farmer: 10 });
  assert.strictEqual(r.runway(s), Infinity);
});

test('outside a resource chapter nothing is constrained', () => {
  const s = Object.assign(snap({ wizard: 99 }, { food: 0 }, {}), { level: 'mainGame' });
  assert.strictEqual(r.runway(s), Infinity);
  assert.strictEqual(r.resourceNeed(s), null);
  assert.strictEqual(r.unsafeToBuy(s, 'wizard'), false);
});

test('the resource in deepest deficit is the one to buy', () => {
  const s = snap({ wizard: 10, warrior: 2, farmer: 1, miner: 1 },
    { food: 1e6, wood: 1e6, ore: 1e6 }, { farmer: 1, miner: 1 });
  const need = r.resourceNeed(s);
  assert.strictEqual(need.id, 'farmer', 'food is short by far the most');
});

test('a locked producer is never proposed', () => {
  const s = snap({ wizard: 10, farmer: 0 }, { food: 0, wood: 0, ore: 0 }, {});
  s.gen.farmer = { owned: 0, isUnlocked: false };
  const need = r.resourceNeed(s);
  assert.ok(!need || need.id !== 'farmer');
});

test('a comfortable surplus with stock on hand needs nothing', () => {
  const s = snap({ wizard: 1, farmer: 100 }, { food: 1e9, wood: 1e9, ore: 1e9 },
    { farmer: 10, lumberjack: 10, miner: 10 });
  s.gen.lumberjack = { owned: 100, isUnlocked: true };
  s.gen.miner = { owned: 100, isUnlocked: true };
  assert.strictEqual(r.resourceNeed(s), null);
});

test('stock alone does not excuse a deficit', () => {
  // Flow is negative, so however large the pile is, this still needs a producer.
  const s = snap({ wizard: 10, farmer: 1 }, { food: 1e12, wood: 1e12, ore: 1e12 }, { farmer: 1 });
  const need = r.resourceNeed(s);
  assert.strictEqual(need && need.id, 'farmer');
});

test('a purchase that would tip a resource negative is refused', () => {
  const s = snap({ farmer: 1, wizard: 0 }, { food: 100 }, { farmer: 1 });
  assert.strictEqual(r.unsafeToBuy(s, 'wizard'), false, 'flow 1 - 1 = 0, which is not a deficit');
  s.gen.wizard = { owned: 1, isUnlocked: true };
  assert.strictEqual(r.unsafeToBuy(s, 'wizard'), true, 'flow is now 0, so one more goes negative');
});

test('a unit with no upkeep is always safe', () => {
  const s = snap({ farmer: 0 }, { food: 0, wood: 0, ore: 0 }, {});
  assert.strictEqual(r.unsafeToBuy(s, 'elf'), false);
});

'use strict';
// Candidate selection, checked without the game.

const test = require('node:test');
const assert = require('node:assert');
const consts = require('./consts.js');
const cost = require('./cost.js').create({ PERIOD_UPGRADE: consts.PERIOD_UPGRADE });
const { create } = require('./plan.js');

/** A planner whose valuation is a stub, so tests state values directly. */
function planner(over) {
  const o = over || {};
  return create({
    cfg: Object.assign({ reservePct: 0, buyPaused: false }, o.cfg),
    consts,
    cost,
    ready: Object.assign({ on: true }, o.ready),
    resource: Object.assign({ unsafeToBuy: () => false }, o.resource),
    value: Object.assign({
      unitValue: (snap, id) => (snap.gen[id].worth || 0),
      periodValue: () => null,
      defensiveValue: () => null,
    }, o.value),
    cal: o.cal || null,
    calKey: o.calKey || ((x) => `${x.kind}:${x.id}`),
    SPECIAL_VALUE: o.SPECIAL_VALUE || {},
  });
}

/** A generator entry priced at a flat `c` gold. */
const gen = (c, worth, extra) => Object.assign(
  { isUnlocked: true, cost: { gold: c }, costGrowthRate: 1, purchased: 0, worth }, extra,
);

const snapOf = (g, up) => ({ gold: 1000, gen: g, up: up || {}, stats: {} });

test('candidates rank by value per gold, not by value', () => {
  const p = planner();
  const list = p.candidates(snapOf({
    cheap: gen(10, 100),      // score 10
    pricey: gen(500, 1000),   // score 2
  }), 100);
  assert.deepStrictEqual(list.map((x) => x.id), ['cheap', 'pricey']);
});

test('anything unaffordable is left out', () => {
  const p = planner();
  const list = p.candidates(snapOf({ rich: gen(5000, 1e9) }), 100);
  assert.deepStrictEqual(list, []);
});

test('the gold reserve shrinks the budget', () => {
  const p = planner({ cfg: { reservePct: 50 } });
  const list = p.candidates(snapOf({ mid: gen(600, 10) }), 100);
  assert.deepStrictEqual(list, [], '600 is over the 500 budget');
});

test('a locked generator is never a candidate', () => {
  const p = planner();
  const list = p.candidates(snapOf({ locked: gen(10, 100, { isUnlocked: false }) }), 100);
  assert.deepStrictEqual(list, []);
});

test('a purchase that would starve a resource is skipped', () => {
  const p = planner({ resource: { unsafeToBuy: (snap, id) => id === 'greedy' } });
  const list = p.candidates(snapOf({ greedy: gen(10, 100), fine: gen(10, 50) }), 100);
  assert.deepStrictEqual(list.map((x) => x.id), ['fine']);
});

test('resource units never compete on score', () => {
  const p = planner();
  const list = p.candidates(snapOf({ farmer: gen(10, 1e9) }), 100);
  assert.deepStrictEqual(list, []);
});

test('a drought pauses buying entirely', () => {
  const p = planner({ cfg: { buyPaused: true } });
  assert.deepStrictEqual(p.candidates(snapOf({ cheap: gen(10, 100) }), 100), []);
});

test('before ready, the opening rule runs instead of the score model', () => {
  const p = planner({
    ready: { on: false },
    value: { unitValue: () => { throw new Error('the score model must not run'); } },
  });
  const list = p.candidates(snapOf({
    warrior: Object.assign(gen(10), { baseGeneration: 1 }),   // 0.1 per gold
    wizard: Object.assign(gen(10), { baseGeneration: 5 }),    // 0.5 per gold
  }), 100);
  assert.strictEqual(list.length, 1, 'the opening buys one kind at a time');
  assert.strictEqual(list[0].id, 'wizard');
  assert.strictEqual(list[0].opening, true);
  assert.strictEqual(list[0].value, undefined, 'the opening is kept out of learning');
});

test('the opening ignores units that are not direct damage', () => {
  const p = planner({ ready: { on: false } });
  const list = p.candidates(snapOf({
    garrison: Object.assign(gen(1), { baseGeneration: 1e6 }),
  }), 100);
  assert.deepStrictEqual(list, []);
});

test('an upgrade is bought on status, not isUnlocked', () => {
  const p = planner();
  const up = {
    warrior: {
      open: { status: 'unlocked', cost: { gold: 10 }, costGrowthRate: 1, purchased: 0, bonusPerOwned: 5, multiplier: 1 },
      shut: { status: 'hidden', cost: { gold: 10 }, costGrowthRate: 1, purchased: 0, bonusPerOwned: 5, multiplier: 1 },
    },
  };
  const snap = snapOf({}, up);
  snap.stats = { warrior: { damagePerTick: 100 } };
  const list = p.candidates(snap, 100);
  assert.deepStrictEqual(list.map((x) => x.id), ['open']);
});

test('the blacklist and dungeon-only upgrades never appear', () => {
  const p = planner();
  const mk = () => ({ status: 'unlocked', cost: { gold: 1 }, costGrowthRate: 1, purchased: 0, bonusPerOwned: 5, multiplier: 1 });
  const snap = snapOf({}, { bard: { cacofonix: mk(), lockPick: mk() } });
  snap.stats = { bard: { damagePerTick: 100 } };
  assert.deepStrictEqual(p.candidates(snap, 100), []);
});

test('an upgrade at its purchase limit is done', () => {
  const p = planner();
  const snap = snapOf({}, {
    bard: { maxed: { status: 'unlocked', cost: { gold: 1 }, costGrowthRate: 1, purchased: 3, purchaseLimit: 3, bonusPerOwned: 5, multiplier: 1 } },
  });
  snap.stats = { bard: { damagePerTick: 100 } };
  assert.deepStrictEqual(p.candidates(snap, 100), []);
});

test('a quarantined family is dropped', () => {
  const p = planner({
    cal: { quarantined: (k) => k === 'gen:bad', alpha: () => 1 },
  });
  const list = p.candidates(snapOf({ bad: gen(10, 100), good: gen(10, 50) }), 100);
  assert.deepStrictEqual(list.map((x) => x.id), ['good']);
});

test('the calibration coefficient reorders score but leaves value alone', () => {
  const p = planner({
    cal: { quarantined: () => false, alpha: (k) => (k === 'gen:under' ? 10 : 1) },
  });
  const list = p.candidates(snapOf({ under: gen(10, 20), over: gen(10, 100) }), 100);
  assert.strictEqual(list[0].id, 'under', '20 x 10 beats 100 x 1');
  assert.strictEqual(list[0].value, 20, 'the prediction fed to learning is unscaled');
});

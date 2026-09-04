'use strict';
// The tick executor, checked without the game.

const test = require('node:test');
const assert = require('node:assert');
const consts = require('./consts.js');
const cost = require('./cost.js').create({ PERIOD_UPGRADE: consts.PERIOD_UPGRADE });
const { create, BATCH_CAP } = require('./exec.js');

function harness(over) {
  const o = over || {};
  const sent = [];
  const bought = [];
  let gold = o.gold != null ? o.gold : 1000;
  const gen = o.gen || { warrior: { cost: { gold: 10 }, costGrowthRate: 1, purchased: 0 } };
  const up = o.up || {};
  const plan = { list: (o.plan || []).slice(), planH: 300, at: 0, replan: () => { plan.replanned = true; } };
  const state = { running: true, phase: 'RUNNING', lastAction: '', lastActionAt: 0 };
  const notes = [];

  const e = create({
    cfg: Object.assign({ buy: true, reservePct: 0 }, o.cfg),
    state,
    log: () => {},
    dispatch: (type, payload) => { sent.push([type, payload]); return o.dispatchOk !== false; },
    buyUpgrade: (cat, id, before) => { bought.push([cat, id, before]); return o.buyOk !== false; },
    cost,
    resource: Object.assign({ resourceNeed: () => null }, o.resource),
    plan,
    game: {
      currency: () => (o.noCurrency ? null : { getState: () => ({ gold }) }),
      generators: () => gen,
      upgrades: () => up,
      slotStore: () => ({ getState: () => ({ phase: o.phase !== undefined ? o.phase : 'combat' }) }),
    },
    snapshot: () => o.snap || { gen, up, stats: {} },
    playable: () => o.playable !== false,
    calNote: (key, v, H) => notes.push([key, v, H]),
    now: () => 1e6,
  });
  return { e, sent, bought, plan, state, notes, setGold: (g) => { gold = g; } };
}

const item = (extra) => Object.assign({ kind: 'gen', id: 'warrior', cost: 10, value: 100, key: 'gen:warrior' }, extra);

test('a plan item is bought in bulk, not one at a time', () => {
  const h = harness({ plan: [item()], gold: 1000 });
  h.e.onTick();
  assert.strictEqual(h.sent.length, 1);
  assert.deepStrictEqual(h.sent[0], ['buy_generator', { id: 'warrior', amountToBuy: 25 }]);
});

test('the batch is capped even with unlimited gold', () => {
  const h = harness({ plan: [item()], gold: 1e12 });
  h.e.onTick();
  assert.strictEqual(h.sent[0][1].amountToBuy, BATCH_CAP);
});

test('an opening pick is bought one at a time', () => {
  const h = harness({ plan: [item({ opening: true })], gold: 1e6 });
  h.e.onTick();
  assert.strictEqual(h.sent[0][1].amountToBuy, 1, 'thin evidence, small steps');
});

test('nothing is bought without the gold for the head of the plan', () => {
  const h = harness({ plan: [item({ cost: 5000 })], gold: 100 });
  h.e.onTick();
  assert.deepStrictEqual(h.sent, []);
  assert.ok(h.plan.list.length, 'the plan is kept, not discarded');
});

test('the gold reserve is withheld', () => {
  const h = harness({ plan: [item({ cost: 600 })], gold: 1000, cfg: { reservePct: 50 } });
  h.e.onTick();
  assert.deepStrictEqual(h.sent, [], '600 is over the 500 budget');
});

test('spending inside one tick is deducted optimistically', () => {
  // dispatch is asynchronous, so gold does not drop until later. Without the
  // deduction the second item in the plan would be bought with money already spent.
  const h = harness({
    plan: [item({ cost: 10 }), item({ id: 'wizard', cost: 10 })],
    gen: {
      warrior: { cost: { gold: 600 }, costGrowthRate: 1, purchased: 0 },
      wizard: { cost: { gold: 600 }, costGrowthRate: 1, purchased: 0 },
    },
    gold: 1000,
  });
  h.e.onTick();
  assert.strictEqual(h.sent.length, 1, 'only 1000 gold, so only one 600 purchase');
});

test('buying outside a combat phase is refused', () => {
  const h = harness({ plan: [item()], phase: 'victory_cutscene' });
  h.e.onTick();
  assert.deepStrictEqual(h.sent, [], 'the generation table is frozen and stale');
});

test('the null phase counts as buyable', () => {
  const h = harness({ plan: [item()], phase: null });
  h.e.onTick();
  assert.strictEqual(h.sent.length, 1);
});

test('nothing happens while not playable', () => {
  const h = harness({ plan: [item()], playable: false });
  h.e.onTick();
  assert.deepStrictEqual(h.sent, []);
});

test('nothing happens while held', () => {
  const h = harness({ plan: [item()] });
  h.state.phase = 'HOLD';
  h.e.onTick();
  assert.deepStrictEqual(h.sent, []);
});

test('a resource shortfall is filled before anything else, and ends the tick', () => {
  const h = harness({
    plan: [item()],
    gen: {
      warrior: { cost: { gold: 10 }, costGrowthRate: 1, purchased: 0 },
      farmer: { cost: { gold: 10 }, costGrowthRate: 1, purchased: 0 },
    },
    resource: { resourceNeed: () => ({ id: 'farmer', r: 'food', deficit: 5 }) },
  });
  h.e.onTick();
  assert.strictEqual(h.sent.length, 1);
  assert.strictEqual(h.sent[0][1].id, 'farmer');
  assert.strictEqual(h.plan.list.length, 1, 'the unit plan is untouched this tick');
});

test('an unaffordable resource need does not block unit buying', () => {
  const h = harness({
    plan: [item()],
    gold: 10,
    gen: {
      warrior: { cost: { gold: 10 }, costGrowthRate: 1, purchased: 0 },
      farmer: { cost: { gold: 1e9 }, costGrowthRate: 1, purchased: 0 },
    },
    resource: { resourceNeed: () => ({ id: 'farmer', r: 'food', deficit: 5 }) },
  });
  h.e.onTick();
  assert.strictEqual(h.sent.length, 1);
  assert.strictEqual(h.sent[0][1].id, 'warrior');
});

test('an upgrade goes through buyUpgrade, so the unlock signals are sent', () => {
  const h = harness({
    plan: [{ kind: 'up', cat: 'warrior', id: 'sharpSwords', cost: 10, value: 50, key: 'up:sharpSwords' }],
    up: { warrior: { sharpSwords: { cost: { gold: 10 }, costGrowthRate: 1, purchased: 2 } } },
  });
  h.e.onTick();
  assert.deepStrictEqual(h.bought, [['warrior', 'sharpSwords', 2]]);
  assert.deepStrictEqual(h.sent, [], 'never a raw buy_upgrade dispatch');
});

test('a vanished plan item is dropped rather than bought', () => {
  const h = harness({ plan: [item({ id: 'ghost' })] });
  h.e.onTick();
  assert.deepStrictEqual(h.sent, []);
  assert.strictEqual(h.plan.list.length, 0);
});

test('the prediction is recorded for learning', () => {
  const h = harness({ plan: [item()] });
  h.e.onTick();
  assert.deepStrictEqual(h.notes, [['gen:warrior', 100, 300]]);
});

test('an opening pick is kept out of learning', () => {
  const h = harness({ plan: [item({ opening: true })] });
  h.e.onTick();
  assert.deepStrictEqual(h.notes, []);
});

test('emptying the plan triggers an immediate replan', () => {
  const h = harness({ plan: [item()] });
  h.e.onTick();
  assert.strictEqual(h.plan.replanned, true);
});

'use strict';
// Valuation, checked without the game. Fire survival is stubbed so each test states
// exactly the survival assumption it depends on.

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./value.js');

const CHAIN = { garrison: 'warrior' };
const RESOURCE_UNITS = { farmer: 'food' };
const FIRE_DEATH = { warrior: 1, wizard: 0.75 };

/** Nothing ever dies, so alive time is always the whole horizon. */
function immortal(extra) {
  return create(Object.assign({
    CHAIN,
    RESOURCE_UNITS,
    GOLD_WEIGHT: 0.5,
    FIRE_DEATH,
    FIRE_PERIOD: 600,
    effectivePeriod: (snap, id) => (snap.gen[id] && snap.gen[id].period) || 1,
    aliveTime: (snap, id, H) => H,
    aliveTimeD: (d, H) => H * (1 - d),
    deathRate: () => 0,
    firePeriod: () => 600,
  }, extra || {}));
}

const snapOf = (gen, stats, rest) => Object.assign({ gen, stats, up: {} }, rest || {});

test('horizon tracks how long the boss will take', () => {
  const v = immortal();
  assert.strictEqual(v.horizon({ level: 'infinite' }), 900);
  assert.strictEqual(v.horizon({ level: 'mainGame', hp: 0, dps: 0 }), 300, 'no data: a default');
  assert.strictEqual(v.horizon({ level: 'mainGame', hp: 1000, dps: 10 }), 300, '3 x 100s');
  assert.strictEqual(v.horizon({ level: 'mainGame', hp: 1e12, dps: 1 }), 900, 'clamped above');
  assert.strictEqual(v.horizon({ level: 'mainGame', hp: 1, dps: 1e9 }), 60, 'clamped below');
});

test('per-second output divides the table value by the firing period', () => {
  const v = immortal();
  const snap = snapOf(
    { warrior: { period: 1 }, college: { period: 300 } },
    { warrior: { mainIndividualGenerationStat: 3 }, college: { mainIndividualGenerationStat: 300 } },
  );
  assert.strictEqual(v.perUnit(snap, 'warrior'), 3);
  assert.strictEqual(v.perUnit(snap, 'college'), 1, '300 per firing every 300 ticks');
});

test('gold output is folded in at the gold weight', () => {
  const v = immortal();
  const snap = snapOf(
    { thief: { period: 1, owned: 2 } },
    { thief: { mainIndividualGenerationStat: 1, goldGeneration: 8 } },
  );
  assert.strictEqual(v.unitRate(snap, 'thief', 0), 1 + 4 * 0.5, '8 gold over 2 owned, weighted');
});

test('a chain unit is worth the children it makes, not its own damage', () => {
  const v = immortal();
  const snap = snapOf(
    { garrison: { period: 1 }, warrior: { period: 1, owned: 1 } },
    { garrison: { mainIndividualGenerationStat: 2 }, warrior: { mainIndividualGenerationStat: 3 } },
  );
  // 2 warriors/s, each worth 3/s, over H=100: 2 * 3 * 100 * 100 / 2
  assert.strictEqual(v.unitValue(snap, 'garrison', 100, 0), 30000);
});

test('a leaf unit is rate times how long it lives', () => {
  const v = immortal();
  const snap = snapOf({ warrior: { period: 1 } }, { warrior: { mainIndividualGenerationStat: 3 } });
  assert.strictEqual(v.unitValue(snap, 'warrior', 100, 0), 300);
});

test('resource units are worth zero here - they are priced as a constraint', () => {
  const v = immortal();
  const snap = snapOf({ farmer: { period: 1 } }, { farmer: { mainIndividualGenerationStat: 90 } });
  assert.strictEqual(v.unitValue(snap, 'farmer', 100, 0), 0);
});

test('a unit producing nothing is worth nothing', () => {
  const v = immortal();
  const snap = snapOf({ wizard: { period: 1 } }, { wizard: { mainIndividualGenerationStat: 0 } });
  assert.strictEqual(v.unitValue(snap, 'wizard', 100, 0), 0);
});

test('dying shortens the payback', () => {
  const v = immortal({ aliveTime: (snap, id, H) => (id === 'warrior' ? H / 2 : H) });
  const snap = snapOf({ warrior: { period: 1 } }, { warrior: { mainIndividualGenerationStat: 3 } });
  assert.strictEqual(v.unitValue(snap, 'warrior', 100, 0), 150);
});

test('a period upgrade is valued by the output multiple it creates', () => {
  const v = immortal();
  const snap = snapOf(
    { thief: { period: 2, owned: 10, ticksToGenerate: 5 } },
    { thief: { mainIndividualGenerationStat: 2 } },
  );
  // Now 5 + (-3) = 2 ticks; one more step gives 5 + (-3) + (-1) = 1 tick.
  // Rate is 2/2 = 1 per thief, so the gain is 10 * 1 * (2/1 - 1) = 10 over H.
  const got = v.periodValue(snap, 'thief', { multiplier: -3, bonusPerOwned: -1 }, 100);
  assert.strictEqual(got, 1000);
});

test('a period upgrade with no units owned has no value', () => {
  const v = immortal();
  const snap = snapOf({ thief: { period: 5, owned: 0, ticksToGenerate: 5 } }, { thief: {} });
  assert.strictEqual(v.periodValue(snap, 'thief', { multiplier: 0, bonusPerOwned: -1 }, 100), null);
});

test('a period upgrade that shortens nothing has no value', () => {
  const v = immortal();
  const snap = snapOf(
    { thief: { period: 1, owned: 10, ticksToGenerate: 5 } },
    { thief: { mainIndividualGenerationStat: 2 } },
  );
  // Already at the floor of 1, so one more step buys nothing.
  assert.strictEqual(v.periodValue(snap, 'thief', { multiplier: -4, bonusPerOwned: -1 }, 100), null);
});

test('a defensive upgrade is worth the output it keeps alive', () => {
  const v = immortal({
    deathRate: () => 0.5,
    aliveTimeD: (d, H) => H * (1 - d),
  });
  const snap = snapOf(
    { warrior: { period: 1, owned: 10 } },
    { warrior: { mainIndividualGenerationStat: 1 } },
  );
  // 0.5 death rate falls to 0.5 - 1 * 20/100 = 0.3; alive time goes 50 -> 70.
  const got = v.defensiveValue(snap, 'warrior', 'fireArmor', { bonusPerOwned: 20 }, 100);
  assert.ok(Math.abs(got - 10 * 1 * 20) < 1e-9);
});

test('defence is worth nothing when nothing dies', () => {
  const v = immortal();   // deathRate 0
  const snap = snapOf({ warrior: { period: 1, owned: 10 } },
    { warrior: { mainIndividualGenerationStat: 1 } });
  assert.strictEqual(v.defensiveValue(snap, 'warrior', 'fireArmor', { bonusPerOwned: 20 }, 100), null);
});

test('an upgrade that is not defensive is not valued here', () => {
  const v = immortal({ deathRate: () => 0.5 });
  const snap = snapOf({ warrior: { period: 1, owned: 10 } },
    { warrior: { mainIndividualGenerationStat: 1 } });
  assert.strictEqual(v.defensiveValue(snap, 'warrior', 'somethingElse', { bonusPerOwned: 20 }, 100), null);
});

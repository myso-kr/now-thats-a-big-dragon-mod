'use strict';
// Checks the recovered breath formulas without the game.

const test = require('node:test');
const assert = require('node:assert');
const { create, FIRE_DEATH } = require('./fire.js');

/** Build any breath event. null means "this chapter has no breath". */
function withFire(ev) {
  return create({ timedEvent: (id) => (id === 'fire' ? ev : null) });
}

const justBreathed = { duration: 600, elapsed: 0, rate: 1 };
const breathImminent = { duration: 600, elapsed: 590, rate: 1 };

function snap(over = {}) {
  return { up: {}, gen: {}, ...over };
}

test('with no defence every warrior dies', () => {
  const f = withFire(justBreathed);
  assert.strictEqual(f.deathRate(snap(), 'warrior'), 1);
});

test('elves and catapults do not die', () => {
  const f = withFire(justBreathed);
  assert.strictEqual(f.deathRate(snap(), 'elf'), 0);
  assert.strictEqual(f.deathRate(snap(), 'catapult'), 0);
  assert.strictEqual(f.deathRate(snap(), 'farmer'), 0, 'nor do the resource units');
});

test('the death rates match the game', () => {
  assert.deepStrictEqual(FIRE_DEATH,
    { warrior: 1, wizard: 0.75, thief: 0.5, bard: 0.5, cleric: 0.5 });
});

test('fire armour applies to warriors only', () => {
  const s = snap({ up: { warrior: { fireArmor: { multiplier: 25 } } } });
  const f = withFire(justBreathed);
  assert.strictEqual(f.deathRate(s, 'warrior'), 0.75, '1.0 × (1 − 25/100)');
  assert.strictEqual(f.deathRate(s, 'wizard'), 0.75, 'wizards are unaffected');
});

test('the blessing applies to every unit', () => {
  const s = snap({ up: { cleric: { blessedAura: { multiplier: 50 } } } });
  const f = withFire(justBreathed);
  assert.strictEqual(f.deathRate(s, 'warrior'), 0.5);
  assert.strictEqual(f.deathRate(s, 'thief'), 0.25, '0.5 × (1 − 50/100)');
});

test('reduction beyond 100 never turns the rate negative', () => {
  const s = snap({ up: {
    warrior: { fireArmor: { multiplier: 75 } },
    cleric: { blessedAura: { multiplier: 100 } },
  } });
  assert.strictEqual(withFire(justBreathed).deathRate(s, 'warrior'), 0);
});

test('the smoke bomb discounts by its expected value', () => {
  const s = snap({ up: { thief: { smokeBomb: { purchased: 1, bonusPerOwned: 5 } } } });
  // blocking chance 1x5+5 = 10%
  assert.strictEqual(withFire(justBreathed).deathRate(s, 'warrior'), 0.9);
});

test('the sonic barrier lengthens the period', () => {
  const f = withFire(justBreathed);
  assert.strictEqual(f.firePeriod(snap()), 600);
  const s = snap({ up: { bard: { sonicBarrier: { multiplier: 50 } } } });
  assert.strictEqual(f.firePeriod(s), 1200, 'a 50% rate doubles the period');
});

test('a unit that cannot die survives the whole horizon', () => {
  const f = withFire(justBreathed);
  assert.strictEqual(f.aliveTime(snap(), 'elf', 900), 900);
});

test('an unarmoured warrior lasts until the first breath and no further', () => {
  const f = withFire(breathImminent);   // 10 seconds to go
  assert.strictEqual(f.aliveTime(snap(), 'warrior', 900), 10,
    'at a death rate of 1.0 nobody is left after it');
});

test('survival time collapses as the breath approaches, which holds back a purchase made just before it', () => {
  const after = withFire(justBreathed).aliveTime(snap(), 'wizard', 900);
  const imminent = withFire(breathImminent).aliveTime(snap(), 'wizard', 900);
  assert.ok(imminent < after, `imminent ${imminent} has to be below just-after ${after}`);
});

test('nobody dies in a chapter with no breath', () => {
  const f = create({ timedEvent: () => null });
  assert.strictEqual(f.fireIn(), null);
  // with no readable event, half a period is the expected wait
  assert.ok(f.aliveTime(snap(), 'warrior', 900) > 0);
});

test('a stopped event counts as absent', () => {
  const f = create({ timedEvent: () => null });   // a paused event is filtered out by the lookup
  assert.strictEqual(f.fireIn(), null);
});

test('the time remaining accounts for the event rate', () => {
  const f = withFire({ duration: 600, elapsed: 100, rate: 0.5 });
  assert.strictEqual(f.fireIn(), 1000, '(600 − 100) / 0.5');
});

test('the number of deaths rounds down', () => {
  const s = snap({ gen: { thief: { owned: 7 } } });
  assert.strictEqual(withFire(justBreathed).casualties(s, 'thief'), 3, 'floor(7 × 0.5)');
});

test('survival time never exceeds the horizon', () => {
  const f = withFire({ duration: 600, elapsed: 0, rate: 1 });
  for (const id of ['warrior', 'wizard', 'thief', 'elf']) {
    const t = f.aliveTime(snap(), id, 300);
    assert.ok(t <= 300 + 1e-9, `${id}: ${t} <= 300`);
  }
});

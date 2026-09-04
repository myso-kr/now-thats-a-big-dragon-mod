'use strict';
// Checks the sign-inverted upgrade valuations without the game.
// The generic formula never picks these, so this is the only net under them.

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./special.js');

function mk(over = {}) {
  return create({
    effectivePeriod: over.effectivePeriod || (() => 1),
    aliveTime: over.aliveTime || ((snap, id, H) => H),
    timedEvent: over.timedEvent || (() => null),
    GOLD_WEIGHT: 0.5,
  });
}

/** A snapshot with bards in it, so inspiration accrues. */
function withBard(over = {}) {
  return {
    dps: 1000, gps: 0, mana: 0,
    stats: { bard: { inspirationGeneration: 2 } },
    gen: {}, up: {},
    ...over,
  };
}

// ── encore: the inspiration cooldown ────────────────────────────

test('encore shortens the cooldown, so inspiration is up more of the time', () => {
  const s = mk();
  const v = s.encoreValue(withBard(), { multiplier: 60, bonusPerOwned: -1 }, 900);
  assert.ok(v > 0, 'it has to be positive (the ordinary formula gives -1/60)');
});

test('encore is worth nothing with no unit making inspiration', () => {
  const s = mk();
  const snap = withBard({ stats: {} });
  assert.strictEqual(s.encoreValue(snap, { multiplier: 60, bonusPerOwned: -1 }, 900), null);
});

test('encore is worth nothing when the cooldown does not shorten', () => {
  const s = mk();
  assert.strictEqual(s.encoreValue(withBard(), { multiplier: 60, bonusPerOwned: 0 }, 900), null);
});

test('a shorter cooldown means inspiration is up more of the time', () => {
  const s = mk();
  const snap = withBard();
  assert.ok(s.inspirationDuty(snap, 20) > s.inspirationDuty(snap, 60));
});

test('the inspiration duty cycle stays between 0 and 1', () => {
  const s = mk();
  for (const cd of [0, 20, 60, 600]) {
    const d = s.inspirationDuty(withBard(), cd);
    assert.ok(d >= 0 && d <= 1, `cooldown ${cd}: ${d}`);
  }
});

// ── manaBoost: the wizard's doubled band ────────────────────────

test('manaBoost: the double-damage band does not exist until it is bought', () => {
  // threshold 100 against maximum mana 100: mana > 100 is never true
  const s = mk();
  const snap = { stats: { wizard: { damagePerTick: 500 } }, up: {}, gen: {} };
  const v = s.manaBoostValue(snap, { multiplier: 100, bonusPerOwned: -2 }, 900);
  assert.ok(v > 0, 'the first purchase is the step from nothing to something, so it has a value');
});

test('manaBoost is worth nothing when wizards deal no damage', () => {
  const s = mk();
  const snap = { stats: { wizard: { damagePerTick: 0 } }, up: {}, gen: {} };
  assert.strictEqual(s.manaBoostValue(snap, { multiplier: 100, bonusPerOwned: -2 }, 900), null);
});

// ── piercedEardrums: the stun period ───────────────────────────

test('nothing is valued in a chapter with no roar', () => {
  const s = mk({ timedEvent: () => null });
  assert.strictEqual(s.earValue(withBard(), { multiplier: 100, bonusPerOwned: -5 }, 900), null);
});

test('with a roar it is worth the reduction in stun duty', () => {
  const s = mk({ timedEvent: (id) => (id === 'roar' ? { duration: 420 } : null) });
  const v = s.earValue(withBard(), { multiplier: 100, bonusPerOwned: -5 }, 900);
  assert.ok(v > 0);
});

// ── manaSurge: refilling mana ──────────────────────────────────

const withWizards = {
  mana: 0, dps: 0, gps: 0,
  gen: { wizard: { owned: 10, baseGeneration: 1 } },
  stats: { wizard: { damagePerTick: 0 } },
  up: { wizard: {} },
  inspiration: {},
};

test('manaSurge is worth buying when mana has run out', () => {
  const s = mk();
  const v = s.manaSurgeValue(withWizards, {}, 900);
  assert.ok(v > 0);
});

test('manaSurge is worth nothing when mana is full', () => {
  const s = mk();
  const snap = { ...withWizards, mana: 100, stats: { wizard: { damagePerTick: 5 } } };
  assert.strictEqual(s.manaSurgeValue(snap, {}, 900), null);
});

test('manaSurge is worth nothing with no wizards', () => {
  const s = mk();
  const snap = { ...withWizards, gen: { wizard: { owned: 0 } } };
  assert.strictEqual(s.manaSurgeValue(snap, {}, 900), null);
});

test('mana present and damage at zero means mana is not what is blocking', () => {
  // the ra gate is shut by a shortage or a toggle: refilling changes nothing
  const s = mk();
  const snap = { ...withWizards, mana: 50, stats: { wizard: { damagePerTick: 0 } } };
  assert.strictEqual(s.manaSurgeValue(snap, {}, 900), null,
    'without this test the coefficient drifts towards overvaluing it');
});

test('manaSurge is worth more the more wizards there are', () => {
  const s = mk();
  const few = s.manaSurgeValue(withWizards, {}, 900);
  const many = s.manaSurgeValue(
    { ...withWizards, gen: { wizard: { owned: 100, baseGeneration: 1 } } }, {}, 900);
  assert.ok(many > few);
});

test('gains beyond the horizon are not counted', () => {
  const s = mk();
  const short = s.manaSurgeValue(withWizards, {}, 10);
  const long = s.manaSurgeValue(withWizards, {}, 900);
  assert.ok(short < long);
});

// ── Registration ───────────────────────────────────────────────

test('all four kinds are registered', () => {
  const s = mk();
  for (const id of ['encore', 'manaBoost', 'piercedEardrums', 'manaSurge']) {
    assert.strictEqual(typeof s.byId[id], 'function', `${id} is missing`);
  }
});

test('total output is the sum with gold weighted in', () => {
  const s = mk();
  assert.strictEqual(s.totalRate({ dps: 100, gps: 40 }), 120, '100 + 40×0.5');
});

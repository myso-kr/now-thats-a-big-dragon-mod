'use strict';
// Level changes have to move the multiplier by the game's own rule, or the level
// shows as changed and the effect never arrives.

const test = require('node:test');
const assert = require('node:assert');
const { create, levelTo, limitOf } = require('./upgrades.js');

const up = (over) => Object.assign(
  { purchased: 0, multiplier: 0, bonusPerOwned: 5, status: 'hidden', isUnlocked: false }, over,
);

test('raising a level moves the multiplier by bonus times the difference', () => {
  const u = up();
  assert.strictEqual(levelTo(u, 3), 3);
  assert.strictEqual(u.multiplier, 15);
});

test('lowering a level moves it back down', () => {
  const u = up({ purchased: 5, multiplier: 25 });
  levelTo(u, 2);
  assert.strictEqual(u.multiplier, 10);
});

test('going to zero returns the multiplier to where it started', () => {
  const u = up({ purchased: 4, multiplier: 20 });
  levelTo(u, 0);
  assert.strictEqual(u.multiplier, 0);
  assert.strictEqual(u.purchased, 0);
});

test('an existing multiplier offset is preserved, not overwritten', () => {
  // Some upgrades start at a non-zero multiplier; the change is relative to it.
  const u = up({ purchased: 0, multiplier: 100, bonusPerOwned: -5 });
  levelTo(u, 3);
  assert.strictEqual(u.multiplier, 85);
});

test('a purchase limit caps the level', () => {
  const u = up({ purchaseLimit: 2 });
  assert.strictEqual(levelTo(u, 99), 2);
  assert.strictEqual(u.multiplier, 10);
});

test('a negative target is clamped to zero', () => {
  const u = up({ purchased: 3, multiplier: 15 });
  assert.strictEqual(levelTo(u, -5), 0);
  assert.strictEqual(u.multiplier, 0);
});

test('no limit means no cap', () => {
  assert.strictEqual(limitOf(up()), Infinity);
  assert.strictEqual(limitOf(up({ purchaseLimit: 3 })), 3);
});

test('owning any level unlocks the upgrade', () => {
  const u = up();
  levelTo(u, 1);
  assert.strictEqual(u.status, 'unlocked');
  assert.strictEqual(u.isUnlocked, true);
});

test('going back to zero leaves it unlocked, as the game does', () => {
  const u = up({ purchased: 2, multiplier: 10, status: 'unlocked', isUnlocked: true });
  levelTo(u, 0);
  assert.strictEqual(u.status, 'unlocked');
});

test('a change is handed back through the store setter, not written in place', () => {
  // Editing the live object would skip the setter and nothing would re-render.
  let handedBack = null;
  const live = { warrior: { sharpSwords: up() } };
  const u = create({
    win: {},
    slotStore: () => ({
      getState: () => ({ upgrades: live, setUpgrades: (t) => { handedBack = t; } }),
    }),
  });
  assert.strictEqual(u.setLevel('warrior', 'sharpSwords', 3), true);
  assert.ok(handedBack, 'setUpgrades was called');
  assert.strictEqual(handedBack.warrior.sharpSwords.purchased, 3);
  assert.strictEqual(live.warrior.sharpSwords.purchased, 0, 'the live tree was not mutated');
});

test('with no store, a level change fails rather than throwing', () => {
  const u = create({ win: {}, slotStore: () => null });
  assert.strictEqual(u.setLevel('warrior', 'x', 1), false);
});

test('names fall back to the id when no name table is present', () => {
  const u = create({ win: {}, slotStore: () => null });
  assert.strictEqual(u.nameOf('sharpSwords'), 'sharpSwords');
  const named = create({ win: { __bd_upgradeNames: { sharpSwords: '날카로운 검' } }, slotStore: () => null });
  assert.strictEqual(named.nameOf('sharpSwords'), '날카로운 검');
});

'use strict';
// Slot resolution and resource writes, checked without the game.

const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./store.js');

/** A zustand-ish store over a plain object. */
const stub = (state) => ({
  getState: () => state,
  setState: (p) => Object.assign(state, p),
});

function win(slots, mirrorGold) {
  const stores = {};
  for (const [name, gold] of Object.entries(slots)) {
    stores[`slot_${name}_currency`] = stub({ gold, wood: 1, setGold(v) { this.gold = v; } });
  }
  return {
    __bd_stores: stores,
    global_game_store: mirrorGold === undefined ? undefined
      : { state: { globalVariables: { value: { gold: mirrorGold } } } },
  };
}

test('a single slot is used without needing the mirror', () => {
  const s = create({ win: win({ campaign: 100 }) });
  assert.strictEqual(s.activeSlot(), 'campaign');
  assert.strictEqual(s.getRes('gold'), 100);
});

test('with no slots at all there is nothing to read', () => {
  const s = create({ win: { __bd_stores: {} } });
  assert.strictEqual(s.activeSlot(), null);
  assert.strictEqual(s.getRes('gold'), undefined);
});

test('the slot closest to the Ink mirror is the one being played', () => {
  const s = create({ win: win({ campaign: 100, newGamePlus: 9000 }, 8990) });
  assert.strictEqual(s.activeSlot(), 'newGamePlus');
});

test('without a mirror value, the first slot is used rather than none', () => {
  const s = create({ win: win({ campaign: 100, newGamePlus: 9000 }) });
  assert.strictEqual(s.activeSlot(), 'campaign');
});

test('a write goes through the game setter where there is one', () => {
  const w = win({ campaign: 100 });
  const s = create({ win: w });
  assert.strictEqual(s.setRes('gold', 5000), true);
  assert.strictEqual(w.__bd_stores.slot_campaign_currency.getState().gold, 5000);
});

test('a field with no setter falls back to setState', () => {
  const w = win({ campaign: 100 });
  const s = create({ win: w });
  s.setRes('wood', 42);
  assert.strictEqual(w.__bd_stores.slot_campaign_currency.getState().wood, 42);
});

test('writing with no bridge fails rather than pretending', () => {
  const s = create({ win: {} });
  assert.strictEqual(s.setRes('gold', 1), false);
});

test('an unslotted store is used when there is no slotted one', () => {
  const s = create({ win: { __bd_stores: { currency: stub({ gold: 7 }) } } });
  assert.strictEqual(s.getRes('gold'), 7);
});

test('the status store is found by its field, not its name', () => {
  const s = create({ win: { __bd_stores: { 'some-renamed-store': stub({ tickLength: 1000 }) } } });
  assert.ok(s.statusStore(), 'found despite the name being unrecognised');
  assert.strictEqual(s.statusStore().getState().tickLength, 1000);
});

test('the conventionally named status store is preferred', () => {
  const s = create({
    win: {
      __bd_stores: {
        'game-status': stub({ tickLength: 1000, marker: 'right' }),
        other: stub({ tickLength: 500, marker: 'wrong' }),
      },
    },
  });
  assert.strictEqual(s.statusStore().getState().marker, 'right');
});

test('a store that throws on read is skipped, not fatal', () => {
  const s = create({
    win: {
      __bd_stores: {
        broken: { getState: () => { throw new Error('nope'); } },
        good: stub({ tickLength: 1000 }),
      },
    },
  });
  assert.ok(s.statusStore());
});

test('no status store anywhere returns null', () => {
  const s = create({ win: { __bd_stores: { currency: stub({ gold: 1 }) } } });
  assert.strictEqual(s.statusStore(), null);
});

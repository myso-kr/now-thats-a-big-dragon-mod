'use strict';
// The action channel, checked without the game. The two guarantees under test are
// "destructive actions cannot leave" and "the unlock signals are sent".

const test = require('node:test');
const assert = require('node:assert');
const consts = require('./consts.js');
const { create, PER_SEC } = require('./action.js');

function harness(over) {
  const o = over || {};
  const sent = [];
  const stops = [];
  const logs = [];
  let clock = 1e6;
  const state = { actions: 0 };
  const a = create({
    ALLOWED: consts.ALLOWED,
    BLOCKED: consts.BLOCKED,
    rawDispatch: () => (o.noDispatch ? undefined : (act) => {
      if (o.throws) throw new Error('reducer blew up');
      sent.push(act);
    }),
    playable: () => o.playable !== false,
    upgrades: () => o.upgrades || {},
    upgradeTree: () => o.tree || null,
    state,
    log: (tag, text) => logs.push([tag, text]),
    stop: (r) => stops.push(r),
    now: () => clock,
  });
  return { a, sent, stops, logs, state, tick: (ms) => { clock += ms; } };
}

test('an allowed action goes through', () => {
  const h = harness();
  assert.strictEqual(h.a.dispatch('buy_generator', { id: 'warrior' }), true);
  assert.deepStrictEqual(h.sent, [{ type: 'buy_generator', payload: { id: 'warrior' } }]);
  assert.strictEqual(h.state.actions, 1);
});

test('a destructive action is refused and stops autoplay', () => {
  const h = harness();
  assert.strictEqual(h.a.dispatch('clear_save', {}), false);
  assert.deepStrictEqual(h.sent, []);
  assert.strictEqual(h.stops.length, 1);
});

test('an action nobody allowlisted is also refused', () => {
  const h = harness();
  assert.strictEqual(h.a.dispatch('some_new_action', {}), false);
  assert.deepStrictEqual(h.sent, []);
  assert.strictEqual(h.stops.length, 1, 'unknown is treated as unsafe, not as fine');
});

test('nothing is sent while the game is not playable', () => {
  const h = harness({ playable: false });
  assert.strictEqual(h.a.dispatch('buy_generator', {}), false);
  assert.deepStrictEqual(h.sent, []);
});

test('nothing is sent without a dispatch to send it to', () => {
  const h = harness({ noDispatch: true });
  assert.strictEqual(h.a.dispatch('buy_generator', {}), false);
});

test('the rate limit holds, and lifts after a second', () => {
  const h = harness();
  for (let i = 0; i < PER_SEC; i += 1) h.a.dispatch('buy_generator', {});
  assert.strictEqual(h.sent.length, PER_SEC);
  assert.strictEqual(h.a.dispatch('buy_generator', {}), false, 'over the limit');
  h.tick(1001);
  assert.strictEqual(h.a.dispatch('buy_generator', {}), true, 'the window has rolled');
});

test('a throwing reducer is reported, not propagated', () => {
  const h = harness({ throws: true });
  assert.strictEqual(h.a.dispatch('buy_generator', {}), false);
  assert.strictEqual(h.logs[0][0], 'ERR');
});

test('an upgrade with no children needs only the buy', () => {
  const h = harness({ tree: { warrior: { sharpSwords: {} } } });
  assert.strictEqual(h.a.buyUpgrade('warrior', 'sharpSwords', 3), true);
  assert.deepStrictEqual(h.sent.map((x) => x.type), ['buy_upgrade']);
});

test('the first purchase also reveals the children', () => {
  const h = harness({ tree: { warrior: { s: { children: ['a'], unlockAt: 5 } } } });
  h.a.buyUpgrade('warrior', 's', 0);
  assert.deepStrictEqual(h.sent.map((x) => x.type), ['buy_upgrade', 'show_upgrade']);
});

test('reaching unlockAt unlocks the children', () => {
  const h = harness({ tree: { warrior: { s: { children: ['a'], unlockAt: 5 } } } });
  h.a.buyUpgrade('warrior', 's', 4);   // 4 + 1 === 5
  assert.deepStrictEqual(h.sent.map((x) => x.type), ['buy_upgrade', 'unlock_upgrade']);
});

test('a save already past unlockAt is caught up rather than left locked', () => {
  const h = harness({ tree: { warrior: { s: { children: ['a'], unlockAt: 5 } } } });
  h.a.buyUpgrade('warrior', 's', 40);
  assert.ok(h.sent.map((x) => x.type).includes('unlock_upgrade'),
    'this is why >= is used instead of ===');
});

test('children already open are not unlocked again', () => {
  const h = harness({
    tree: { warrior: { s: { children: ['a'], unlockAt: 5 } } },
    upgrades: { warrior: { a: { status: 'unlocked' } } },
  });
  h.a.buyUpgrade('warrior', 's', 40);
  assert.deepStrictEqual(h.sent.map((x) => x.type), ['buy_upgrade']);
});

test('a failed buy sends no follow-up signals', () => {
  const h = harness({ playable: false, tree: { warrior: { s: { children: ['a'], unlockAt: 1 } } } });
  assert.strictEqual(h.a.buyUpgrade('warrior', 's', 0), false);
  assert.deepStrictEqual(h.sent, []);
});

test('an upgrade missing from the tree still buys', () => {
  const h = harness({ tree: {} });
  assert.strictEqual(h.a.buyUpgrade('warrior', 'unknown', 0), true);
  assert.deepStrictEqual(h.sent.map((x) => x.type), ['buy_upgrade']);
});

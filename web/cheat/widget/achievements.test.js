'use strict';
// The guard must actually stop the calls, and must not double-wrap.

const test = require('node:test');
const assert = require('node:assert');
const { create, GUARDED } = require('./achievements.js');

function harness(blockedRef) {
  const calls = [];
  const handler = {};
  for (const name of GUARDED) {
    handler[name] = (...a) => { calls.push([name, ...a]); return 'sent'; };
  }
  const win = { achievements_handler: handler };
  const a = create({ win, blocked: () => blockedRef.on });
  return { a, win, handler, calls };
}

test('every submission method is wrapped', () => {
  const ref = { on: true };
  const h = harness(ref);
  assert.strictEqual(h.a.install(), true);
  for (const name of GUARDED) h.win.achievements_handler[name]('x');
  assert.deepStrictEqual(h.calls, [], 'nothing reached Steam');
});

test('a blocked call returns undefined rather than an error', () => {
  const ref = { on: true };
  const h = harness(ref);
  h.a.install();
  assert.strictEqual(h.win.achievements_handler.unlockAchievement('x'), undefined);
});

test('turning the guard off lets calls through', () => {
  const ref = { on: true };
  const h = harness(ref);
  h.a.install();
  ref.on = false;
  assert.strictEqual(h.win.achievements_handler.unlockAchievement('x'), 'sent');
  assert.deepStrictEqual(h.calls, [['unlockAchievement', 'x']]);
});

test('the switch is read per call, so toggling takes effect at once', () => {
  const ref = { on: false };
  const h = harness(ref);
  h.a.install();
  h.win.achievements_handler.storeStats();
  ref.on = true;
  h.win.achievements_handler.storeStats();
  assert.strictEqual(h.calls.length, 1, 'only the first call got through');
});

test('installing twice does not wrap twice', () => {
  const ref = { on: false };
  const h = harness(ref);
  assert.strictEqual(h.a.install(), true);
  assert.strictEqual(h.a.install(), false, 'already guarded');
  h.win.achievements_handler.unlockAchievement('x');
  assert.strictEqual(h.calls.length, 1, 'the call passed through exactly one wrapper');
});

test('with no handler yet, install waits rather than failing', () => {
  const a = create({ win: {}, blocked: () => true });
  assert.strictEqual(a.install(), false);
  assert.strictEqual(a.installed(), false);
});

test('a method the handler does not have is skipped', () => {
  const win = { achievements_handler: { unlockAchievement: () => 'sent' } };
  const a = create({ win, blocked: () => true });
  assert.strictEqual(a.install(), true);
  assert.strictEqual(win.achievements_handler.unlockAchievement('x'), undefined);
});

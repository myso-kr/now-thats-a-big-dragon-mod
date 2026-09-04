'use strict';
// The saturation guard, checked without the game. The subtle case is that zero ticks
// means the game is stopped, not that it is drowning.

const test = require('node:test');
const assert = require('node:assert');
const { create, diagnose, lowerSpeed, clampSpeed, LIMITS, BASE_TICK } = require('./speed.js');

/**
 * A healthy 4x sample. The window is 2 seconds, so 4 ticks/s is 8 ticks and 60 fps
 * is 120 frames.
 */
const healthy = (over) => Object.assign({
  ticks: 8, frames: 120, tickMs: 250, visible: true,
  heapMB: 200, baseHeapMB: 190, actors: 100,
}, over);

test('a healthy sample needs no intervention', () => {
  assert.strictEqual(diagnose(healthy()), null);
});

test('ticks far below target read as saturation', () => {
  const v = diagnose(healthy({ ticks: 1 }));   // 0.5/s against a target of 4
  assert.ok(v);
  assert.strictEqual(v.saturated, true);
  assert.match(v.why, /ticks\/s/);
});

test('zero ticks is a stopped game, not a drowning one', () => {
  // A menu, a dialogue or a cutscene stops ticks entirely. Reading that as saturation
  // would drop the speed every time the player opened a menu.
  assert.strictEqual(diagnose(healthy({ ticks: 0, frames: 120 })), null);
});

test('at 1x, a slow tick rate is not judged at all', () => {
  // target is 1/s, which is below the 1.2 threshold - there is nothing to speed-check.
  assert.strictEqual(diagnose(healthy({ ticks: 1, tickMs: BASE_TICK })), null);
});

test('a low frame rate reads as saturation', () => {
  const v = diagnose(healthy({ frames: 20 }));   // 10 fps
  assert.ok(v);
  assert.strictEqual(v.saturated, true);
  assert.match(v.why, /fps/);
});

test('a hidden window is not judged on frame rate', () => {
  // A backgrounded tab is throttled by the browser; that is not the game struggling.
  assert.strictEqual(diagnose(healthy({ frames: 2, visible: false })), null);
});

test('zero frames is not judged either', () => {
  assert.strictEqual(diagnose(healthy({ frames: 0 })), null);
});

test('a heap ceiling is a reason to back off, but not saturation', () => {
  const v = diagnose(healthy({ heapMB: 1500 }));
  assert.ok(v);
  assert.strictEqual(v.saturated, false, 'memory means go to 1x, not one step down');
  assert.match(v.why, /memory/);
});

test('heap growth is caught even below the ceiling', () => {
  const v = diagnose(healthy({ heapMB: 700, baseHeapMB: 200 }));
  assert.ok(v);
  assert.match(v.why, /\+500MB/);
});

test('an actor explosion is caught', () => {
  const v = diagnose(healthy({ actors: 5000 }));
  assert.ok(v);
  assert.strictEqual(v.saturated, false);
  assert.match(v.why, /actors/);
});

test('missing heap readings are simply not used', () => {
  // performance.memory does not exist everywhere; its absence must not read as 0.
  assert.strictEqual(diagnose(healthy({ heapMB: null, baseHeapMB: 0 })), null);
});

test('stepping down goes one speed at a time, never below 1', () => {
  assert.strictEqual(lowerSpeed(8), 4);
  assert.strictEqual(lowerSpeed(4), 2);
  assert.strictEqual(lowerSpeed(2), 1);
  assert.strictEqual(lowerSpeed(1), 1);
  assert.strictEqual(lowerSpeed(3), 2, 'an off-step value falls to the step below');
});

test('speed is clamped to the safe range', () => {
  assert.strictEqual(clampSpeed(99), 8);
  assert.strictEqual(clampSpeed(0.01), 0.25);
  assert.strictEqual(clampSpeed('nonsense'), 1);
  assert.strictEqual(clampSpeed(undefined), 1);
});

// ── The stateful half ────────────────────────────────────────────────

function harness(over) {
  const o = over || {};
  let tickLength = o.tickLength != null ? o.tickLength : BASE_TICK;
  const engine = { timescale: 1 };
  const status = {
    getState: () => ({ tickLength }),
    setState: (p) => { tickLength = p.tickLength; },
  };
  const win = {
    performance: {},
    requestAnimationFrame: () => 0,
    setInterval: () => 1,
    clearInterval: () => {},
  };
  const s = create({
    win,
    doc: { visibilityState: 'visible' },
    store: {
      statusStore: () => (o.noStatus ? null : status),
      engine: () => engine,
      bus: () => ({ on: () => () => {} }),
    },
    limits: LIMITS,
  });
  return { s, engine, tick: () => tickLength };
}

test('raising the speed shortens the tick and sets the timescale', () => {
  const h = harness();
  h.s.setSpeed(4);
  assert.strictEqual(h.tick(), 250, '1000 / 4');
  assert.strictEqual(h.engine.timescale, 4);
});

test('returning to 1x puts the original tick back', () => {
  const h = harness();
  h.s.setSpeed(4);
  h.s.setSpeed(1);
  assert.strictEqual(h.tick(), BASE_TICK);
  assert.strictEqual(h.engine.timescale, 1);
});

test('the original tick is captured once, not on every change', () => {
  const h = harness();
  h.s.setSpeed(2);      // 500
  h.s.setSpeed(4);      // must be 1000/4, not 500/4
  assert.strictEqual(h.tick(), 250);
});

test('a short tick left in the save does not become the new baseline', () => {
  // A session that ended badly can leave 125 ms saved. Treating that as the original
  // would compound every time, ending at an unrecoverably tiny tick.
  const h = harness({ tickLength: 125 });
  h.s.setSpeed(2);
  assert.strictEqual(h.tick(), 500, 'the default is used as the baseline, not 125');
});

test('boot repairs a short tick left behind', () => {
  const h = harness({ tickLength: 125 });
  assert.strictEqual(h.s.healTickOnBoot(), true);
  assert.strictEqual(h.tick(), BASE_TICK);
});

test('boot leaves a normal tick alone', () => {
  const h = harness();
  assert.strictEqual(h.s.healTickOnBoot(), false);
  assert.strictEqual(h.tick(), BASE_TICK);
});

test('with no status store, speed changes do not throw', () => {
  const h = harness({ noStatus: true });
  assert.strictEqual(h.s.setSpeed(4), 4);
  assert.strictEqual(h.engine.timescale, 4, 'the visual speed still applies');
});

'use strict';
// Checks self-correction without the game, with time and output driven by hand.

const test = require('node:test');
const assert = require('node:assert');
const { create, keyOf, CAL_WINDOW, GHOST_STRIKES } = require('./calib.js');

/** A bench where the clock and the total output are turned by hand. */
function rig(over = {}) {
  let t = 0;
  let rate = 0;
  const logs = [];
  const c = create({
    totalRate: () => rate,
    isAlive: over.isAlive || (() => false),
    log: (tag, text, level) => logs.push({ tag, text, level }),
    now: () => t,
  });
  return {
    c, logs,
    tick: (ms) => { t += ms; },
    setRate: (v) => { rate = v; },
    snap: (o = {}) => ({ phase: 'combat', inspiration: {}, stats: {}, ...o }),
  };
}

test('units are keyed by kind and upgrades by family', () => {
  assert.strictEqual(keyOf({ kind: 'gen', id: 'warrior' }), 'gen:warrior');
  assert.strictEqual(keyOf({ kind: 'up', id: 'shortSword', cat: 'warrior' }), 'up:warrior');
});

test('an unknown family has a coefficient of 1', () => {
  const { c } = rig();
  assert.strictEqual(c.alpha('gen:warrior'), 1);
});

test('a window is not settled before it is full', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap());
  r.tick(CAL_WINDOW - 1);
  r.c.settle(r.snap());
  assert.strictEqual(r.c.report().stats.taken, 0);
});

test('output arriving as predicted leaves the coefficient near 1', () => {
  const r = rig();
  r.setRate(0);
  r.c.note('gen:warrior', 900, 900, r.snap());   // predict a contribution of 1 per second
  r.tick(CAL_WINDOW);
  r.setRate(1);                                   // measured 1 as well
  r.c.settle(r.snap());
  assert.strictEqual(r.c.report().stats.taken, 1);
  assert.ok(Math.abs(r.c.alpha('gen:warrior') - 1) < 0.01);
});

test('more output than predicted raises the coefficient', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap());
  r.tick(CAL_WINDOW);
  r.setRate(3);
  r.c.settle(r.snap());
  assert.ok(r.c.alpha('gen:warrior') > 1);
});

test('less output than predicted lowers it', () => {
  const r = rig();
  r.c.note('up:wizard', 900, 900, r.snap());
  r.tick(CAL_WINDOW);
  r.setRate(0.2);
  r.c.settle(r.snap());
  assert.ok(r.c.alpha('up:wizard') < 1);
});

test('a window overlapping inspiration is dropped - better to learn nothing than the wrong thing', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap({ inspiration: { remainingActive: 5 } }));
  r.tick(CAL_WINDOW);
  r.setRate(99);
  r.c.settle(r.snap());
  const rep = r.c.report();
  assert.strictEqual(rep.stats.taken, 0);
  assert.strictEqual(rep.stats.droppedInspired, 1);
  assert.strictEqual(r.c.alpha('gen:warrior'), 1, 'it must not learn from a contaminated window');
});

test('a window outside combat is dropped too', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap());
  r.tick(CAL_WINDOW);
  r.c.settle(r.snap({ phase: 'victory_cutscene' }));
  assert.strictEqual(r.c.report().stats.droppedPhase, 1);
});

test('a purchase that dominates a window and returns nothing is quarantined', () => {
  const r = rig();
  for (let i = 0; i < GHOST_STRIKES; i += 1) {
    r.setRate(0);
    r.c.note('up:wizard', 900, 900, r.snap());
    r.tick(CAL_WINDOW);
    r.setRate(0);                                  // measured 0 - nothing came back
    r.c.settle(r.snap());
  }
  assert.ok(r.c.quarantined('up:wizard'), `${GHOST_STRIKES} strikes and it is quarantined`);
  assert.ok(r.logs.some((l) => l.level === 'warn' && l.text.includes('ghost purchase')));
});

test('only a family that dominated the window can be called a ghost', () => {
  const r = rig();
  for (let i = 0; i < GHOST_STRIKES + 2; i += 1) {
    r.setRate(0);
    // splitting a window evenly means neither dominates it
    r.c.note('up:wizard', 450, 900, r.snap());
    r.c.note('up:elf', 450, 900, r.snap());
    r.tick(CAL_WINDOW);
    r.setRate(0);
    r.c.settle(r.snap());
  }
  assert.ok(!r.c.quarantined('up:wizard'), 'a 50% share is not enough to call it one');
});

test('quarantine lifts once the output comes back', () => {
  let alive = false;
  const r = rig({ isAlive: () => alive });
  for (let i = 0; i < GHOST_STRIKES; i += 1) {
    r.setRate(0);
    r.c.note('up:wizard', 900, 900, r.snap());
    r.tick(CAL_WINDOW);
    r.c.settle(r.snap());
  }
  assert.ok(r.c.quarantined('up:wizard'));
  r.c.release(r.snap());
  assert.ok(r.c.quarantined('up:wizard'), 'still nothing, so it stays');
  alive = true;
  r.c.release(r.snap());
  assert.ok(!r.c.quarantined('up:wizard'), 'it came back, so it is released');
});

test('one outlier cannot run the coefficient away (it is clipped)', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap());
  r.tick(CAL_WINDOW);
  r.setRate(1e9);                                  // an absurd measurement
  r.c.settle(r.snap());
  const a = r.c.alpha('gen:warrior');
  assert.ok(a < Math.exp(0.2) + 1e-9, `ln lambda is clipped to +/-1, so one step cannot exceed e^0.2: ${a}`);
});

test('an empty window is not taken', () => {
  const r = rig();
  r.c.note('gen:warrior', 0, 900, r.snap());       // a prediction of 0 is not recorded
  r.tick(CAL_WINDOW);
  r.c.settle(r.snap());
  assert.strictEqual(r.c.report().stats.taken, 0);
});

test('the diagnostic report shows the window in progress', () => {
  const r = rig();
  r.c.note('gen:warrior', 900, 900, r.snap());
  const rep = r.c.report();
  assert.ok(rep.window, 'an open window appears in the report');
  assert.strictEqual(rep.window.entries, 1);
});

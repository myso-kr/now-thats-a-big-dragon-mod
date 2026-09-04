'use strict';
// Chapter policy, checked without the game. The DOM is a stub that records clicks.

const test = require('node:test');
const assert = require('node:assert');
const consts = require('./consts.js');
const { create, COOLDOWN_MS } = require('./chapter.js');

/** A DOM stub. `present` lists the testids that exist; clicks are recorded. */
function domOf(present, clicks) {
  return {
    querySelector: (sel) => {
      const id = sel.replace(/^\[data-testid=?"?/, '').replace(/"?\]$/, '');
      if (!present.includes(id)) return null;
      return { click: () => clicks.push(id), disabled: false };
    },
  };
}

function harness(over) {
  const o = over || {};
  const clicks = [];
  const logs = [];
  const snaps = [];
  const stops = [];
  let clock = 1e6;
  const c = create({
    doc: o.doc || domOf(o.present || [], clicks),
    log: (tag, text) => logs.push(text),
    stop: (r) => stops.push(r),
    cfg: Object.assign({ chapterMode: 'advance', repeatChapter: null }, o.cfg),
    consts,
    resource: Object.assign({ isResourceChapter: () => false, runway: () => Infinity }, o.resource),
    snapshotState: (r) => snaps.push(r),
    levelUnlocks: o.levelUnlocks || (() => null),
    slotStore: o.slotStore || (() => null),
    onSwitch: o.onSwitch || (() => {}),
    now: () => clock,
    wait: () => Promise.resolve(),
  });
  return { c, clicks, logs, snaps, stops, tick: (ms) => { clock += ms; } };
}

// chapterStep/repeatStep start changeChapter without awaiting it, the way the
// supervisor does. Let its microtasks run before asserting on the clicks.
const settle = () => new Promise((r) => setImmediate(r));

const snapOf = (level, extra) => Object.assign(
  { level, dps: 1e12, mana: 100, inspiration: {} }, extra,
);

test('a chapter change presses the game menu, never dispatch', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'] });
  assert.strictEqual(await h.c.changeChapter('dummy', 'go'), true);
  assert.deepStrictEqual(h.clicks, ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button']);
});

test('with no menu button there is nothing to press', async () => {
  const h = harness({ present: [] });
  assert.strictEqual(await h.c.changeChapter('dummy', 'go'), false);
});

test('restart mode prefers the restart button where it exists', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'settings-level-restart-dummy', 'settings-level-go-dummy', 'close-level-selector-menu-button'] });
  await h.c.changeChapter('dummy', 'restart');
  assert.ok(h.clicks.includes('settings-level-restart-dummy'));
  assert.ok(!h.clicks.includes('settings-level-go-dummy'));
});

test('restart mode falls back to go when the chapter was never cleared', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'] });
  await h.c.changeChapter('dummy', 'restart');
  assert.ok(h.clicks.includes('settings-level-go-dummy'));
});

test('a switch clears the ready latch, since the level name may not change', async () => {
  let cleared = 0;
  const h = harness({
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
    onSwitch: () => { cleared += 1; },
  });
  await h.c.changeChapter('dummy', 'go');
  assert.strictEqual(cleared, 1);
});

test('the menu is closed even when the target button is missing', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'close-level-selector-menu-button'] });
  assert.strictEqual(await h.c.changeChapter('dummy', 'go'), false);
  assert.ok(h.clicks.includes('close-level-selector-menu-button'), 'a menu left open blocks everything after');
});

test('advancing needs the current level beaten', () => {
  const h = harness({
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
    levelUnlocks: () => ({ beatenLevels: {}, unlockPrerequisites: { dummy: true } }),
  });
  h.c.chapterStep(snapOf('mainGame'));
  assert.deepStrictEqual(h.clicks, []);
});

test('advancing is refused while the next boss is out of reach', () => {
  const h = harness({
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
    levelUnlocks: () => ({ beatenLevels: { mainGame: true }, unlockPrerequisites: { dummy: true } }),
  });
  h.c.chapterStep(snapOf('mainGame', { dps: 1 }));   // 1e9 HP at 1 dps
  assert.deepStrictEqual(h.clicks, [], 'a boss that would take 30 years is not ready');
});

test('advancing snapshots before it moves', async () => {
  const h = harness({
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
    levelUnlocks: () => ({ beatenLevels: { mainGame: true }, unlockPrerequisites: { dummy: true } }),
  });
  h.c.chapterStep(snapOf('mainGame'));
  await settle();
  assert.strictEqual(h.snaps.length, 1);
  assert.ok(h.clicks.includes('settings-level-go-dummy'));
});

test('the king battle waits for mana and inspiration', async () => {
  const unlocks = () => ({
    beatenLevels: { infinite: true },
    unlockPrerequisites: { kingBattle: true },
  });
  const present = ['level-selector-menu-button', 'settings-level-go-kingBattle', 'close-level-selector-menu-button'];
  const cold = harness({ present, levelUnlocks: unlocks });
  cold.c.chapterStep(snapOf('infinite', { mana: 10 }));
  assert.deepStrictEqual(cold.clicks, [], 'not enough mana');

  const cooling = harness({ present, levelUnlocks: unlocks });
  cooling.c.chapterStep(snapOf('infinite', { inspiration: { remainingCooldown: 5 } }));
  assert.deepStrictEqual(cooling.clicks, [], 'inspiration still on cooldown');

  const go = harness({ present, levelUnlocks: unlocks });
  go.c.chapterStep(snapOf('infinite'));
  await settle();
  assert.ok(go.clicks.includes('settings-level-go-kingBattle'));
});

test('advancing does nothing outside advance mode', () => {
  const h = harness({
    cfg: { chapterMode: 'off' },
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
    levelUnlocks: () => ({ beatenLevels: { mainGame: true }, unlockPrerequisites: { dummy: true } }),
  });
  h.c.chapterStep(snapOf('mainGame'));
  assert.deepStrictEqual(h.clicks, []);
});

test('repeat restarts the current chapter', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'settings-level-restart-campaign', 'close-level-selector-menu-button'] });
  h.c.repeatStep(snapOf('mainGame'));
  await settle();
  assert.ok(h.clicks.includes('settings-level-restart-campaign'));
  assert.strictEqual(h.snaps.length, 1);
});

test('repeat moves to the named chapter first', async () => {
  const h = harness({
    cfg: { repeatChapter: 'dummy' },
    present: ['level-selector-menu-button', 'settings-level-go-dummy', 'close-level-selector-menu-button'],
  });
  h.c.repeatStep(snapOf('mainGame'));
  await settle();
  assert.ok(h.clicks.includes('settings-level-go-dummy'));
});

test('an unknown repeat chapter stops autoplay rather than guessing', () => {
  const h = harness({ cfg: { repeatChapter: 'nope' } });
  h.c.repeatStep(snapOf('mainGame'));
  assert.strictEqual(h.stops.length, 1);
});

test('the cooldown prevents a second switch straight away', async () => {
  const h = harness({ present: ['level-selector-menu-button', 'settings-level-restart-campaign', 'close-level-selector-menu-button'] });
  h.c.repeatStep(snapOf('mainGame'));
  await settle();
  const first = h.clicks.length;
  h.c.repeatStep(snapOf('mainGame'));
  await settle();
  assert.strictEqual(h.clicks.length, first, 'still inside the cooldown');
  h.tick(COOLDOWN_MS + 1);
  h.c.repeatStep(snapOf('mainGame'));
  await settle();
  assert.ok(h.clicks.length > first, 'allowed once the cooldown passes');
});

test('production is switched off worst-first when the runway is short', () => {
  const offs = [];
  const h = harness({
    resource: { isResourceChapter: () => true, runway: () => 30 },
    slotStore: () => ({ getState: () => ({
      enabledByGenerator: {},
      setProductionEnabled: (id, on) => offs.push([id, on]),
    }) }),
  });
  h.c.manageProduction({
    level: 'newGamePlus',
    gen: { warrior: { owned: 5 }, wizard: { owned: 5 } },
    // warrior: 1 output per 1 ore = 1.0; wizard: 0.5 per 1 food = 0.5
    stats: { warrior: { mainIndividualGenerationStat: 1 }, wizard: { mainIndividualGenerationStat: 0.5 } },
  });
  assert.deepStrictEqual(offs, [['wizard', false]], 'the least efficient goes first');
});

test('production comes back best-first once recovered', () => {
  const ons = [];
  const h = harness({
    resource: { isResourceChapter: () => true, runway: () => 1200 },
    slotStore: () => ({ getState: () => ({
      enabledByGenerator: { warrior: false, wizard: false },
      setProductionEnabled: (id, on) => ons.push([id, on]),
    }) }),
  });
  h.c.manageProduction({
    level: 'newGamePlus',
    gen: { warrior: { owned: 5 }, wizard: { owned: 5 } },
    stats: { warrior: { mainIndividualGenerationStat: 1 }, wizard: { mainIndividualGenerationStat: 0.5 } },
  });
  assert.deepStrictEqual(ons, [['warrior', true]], 'the most efficient comes back first');
});

test('production is left alone in a comfortable middle', () => {
  const calls = [];
  const h = harness({
    resource: { isResourceChapter: () => true, runway: () => 300 },
    slotStore: () => ({ getState: () => ({
      enabledByGenerator: {},
      setProductionEnabled: (id, on) => calls.push([id, on]),
    }) }),
  });
  h.c.manageProduction({ level: 'newGamePlus', gen: { warrior: { owned: 5 } }, stats: {} });
  assert.deepStrictEqual(calls, []);
});

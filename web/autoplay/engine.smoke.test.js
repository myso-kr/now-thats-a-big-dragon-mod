'use strict';
// Loads the whole autoplay engine the way the launcher does — every engine/*.js in
// name order, then engine.js — against a stub browser, and drives it through a few
// ticks with no game present.
//
// The unit tests cover each module in isolation; nothing there can catch a module
// that fails to load, a wiring argument in the wrong order, or a call into a game
// that is not there. Those failures happen in the renderer, where they leave nothing
// in the launcher log, so this is the only place they surface.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const DIR = __dirname;

/** The exact file list, in the exact order, that the launcher injects. */
function sources() {
  const modDir = path.join(DIR, 'engine');
  const mods = fs.readdirSync(modDir)
    .filter((f) => f.endsWith('.js') && !f.endsWith('.test.js'))
    .sort()
    .map((f) => path.join(modDir, f));
  return mods.concat([path.join(DIR, 'engine.js')]);
}

/** A DOM stub: every query misses, which is the worst case the engine must survive. */
function docStub() {
  return {
    querySelector: () => null,
    querySelectorAll: () => [],
  };
}

/** Run the engine in a fresh context and hand back its window. */
function load(over) {
  const listeners = {};
  const win = Object.assign({
    document: docStub(),
    addEventListener: (k, fn) => { (listeners[k] = listeners[k] || []).push(fn); },
    setInterval: () => 0,
    clearInterval: () => {},
    setTimeout: (fn, ms) => setTimeout(fn, ms),
    clearTimeout: (h) => clearTimeout(h),
    console: { log: () => {}, error: (m) => { win.__errors.push(m); } },
    __errors: [],
  }, over || {});
  win.window = win;
  win.self = win;
  win.globalThis = win;
  vm.createContext(win);
  for (const f of sources()) {
    vm.runInContext(fs.readFileSync(f, 'utf8'), win, { filename: f });
  }
  return { win, listeners };
}

test('every module the launcher ships registers itself', () => {
  const { win } = load();
  const files = fs.readdirSync(path.join(DIR, 'engine'))
    .filter((f) => f.endsWith('.js') && !f.endsWith('.test.js'))
    .map((f) => f.replace(/\.js$/, ''));
  for (const name of files) {
    assert.ok(win.__bd_mod[name], `engine/${name}.js did not register as __bd_mod.${name}`);
  }
});

test('the engine comes up with no game present, and does not throw', () => {
  const { win } = load();
  assert.deepStrictEqual(win.__errors, [], 'no module reported itself missing');
  assert.ok(win.__bd_auto, 'the public surface is exposed');
  assert.strictEqual(typeof win.__bd_auto.start, 'function');
});

test('a missing module is named rather than dying as a TypeError', () => {
  const win = { document: docStub(), addEventListener: () => {}, __errors: [] };
  win.window = win; win.self = win; win.globalThis = win;
  win.console = { log: () => {}, error: (m) => win.__errors.push(m) };
  vm.createContext(win);
  // Load engine.js alone, with none of its modules.
  vm.runInContext(fs.readFileSync(path.join(DIR, 'engine.js'), 'utf8'), win);
  assert.strictEqual(win.__errors.length, 1);
  assert.match(win.__errors[0], /engine\/consts\.js/);
  assert.strictEqual(win.__bd_auto, undefined, 'nothing half-built is left behind');
});

test('reading state with no game returns null instead of throwing', () => {
  const { win } = load();
  assert.strictEqual(win.__bd_auto.snapshot(), null);
  assert.strictEqual(win.__bd_auto.fire(), null);
  assert.strictEqual(win.__bd_auto.cand(), null);
  assert.strictEqual(win.__bd_auto.defense('fireArmor'), null);
});

test('start refuses without a dispatch bridge, rather than half-starting', () => {
  const { win } = load();
  win.__bd_auto.start();
  assert.strictEqual(win.__bd_auto.state.running, false);
  assert.strictEqual(win.__bd_auto.state.phase, 'STOPPED');
  assert.ok(win.__bd_auto.log().some((l) => /dispatch/.test(l.text)));
});

test('the supervisor and planner survive a run with no game behind them', () => {
  const sent = [];
  const { win } = load({ __bd_dispatch: (a) => sent.push(a) });
  win.__bd_auto.start();
  assert.strictEqual(win.__bd_auto.state.running, true, 'a dispatch bridge is enough to start');
  // The clocks are stubs here, so drive the cycles directly. Nothing may throw and
  // nothing may be dispatched, because there is no game state to act on.
  for (let i = 0; i < 5; i += 1) {
    win.__bd_auto.snapshotState('smoke');
    // Arrays cross a realm boundary here, so compare length rather than identity.
    assert.strictEqual(win.__bd_auto.plan().length, 0);
  }
  assert.deepStrictEqual(sent, [], 'no action is sent without game state');
  win.__bd_auto.stop('smoke test done');
  assert.strictEqual(win.__bd_auto.state.running, false);
});

test('loading twice does not build a second engine', () => {
  const { win } = load();
  const first = win.__bd_auto;
  vm.runInContext(fs.readFileSync(path.join(DIR, 'engine.js'), 'utf8'), win);
  assert.strictEqual(win.__bd_auto, first, 'the __BD_AUTO__ guard held');
});

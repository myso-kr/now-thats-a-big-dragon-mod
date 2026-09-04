'use strict';
// Loads the cheat widget the way the launcher does — every widget/*.js in name
// order, then widget.js — against a stub browser with no game behind it.
//
// The unit tests cover each module alone; only this can catch a module that fails to
// load or a wiring argument in the wrong place. Both of those fail in the renderer,
// where nothing reaches the launcher log.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const DIR = __dirname;

/** The exact file list, in the exact order, that the launcher injects. */
function sources() {
  const modDir = path.join(DIR, 'widget');
  const mods = fs.readdirSync(modDir)
    .filter((f) => f.endsWith('.js') && !f.endsWith('.test.js'))
    .sort()
    .map((f) => path.join(modDir, f));
  return mods.concat([path.join(DIR, 'widget.js')]);
}

/** A DOM stub recording what the widget appends, with every query missing. */
function docStub(win) {
  const made = [];
  const el = () => ({
    style: {}, dataset: {}, classList: { toggle: () => {}, add: () => {} },
    appendChild: () => {}, addEventListener: () => {},
    querySelectorAll: () => [], querySelector: () => null,
    set innerHTML(v) { this._html = v; }, get innerHTML() { return this._html; },
  });
  return {
    made,
    visibilityState: 'visible',
    head: { appendChild: (x) => made.push(x) },
    body: { appendChild: (x) => made.push(x) },
    createElement: (tag) => { const e = el(); e.tagName = tag.toUpperCase(); return e; },
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
  };
}

function load(over) {
  const win = Object.assign({
    addEventListener: () => {},
    removeEventListener: () => {},
    setInterval: () => 0,
    clearInterval: () => {},
    setTimeout: () => 0,
    clearTimeout: () => {},
    requestAnimationFrame: () => 0,
    performance: {},
    console: {
      log: () => {},
      warn: (...a) => win.__warns.push(a.join(' ')),
      error: (m) => win.__errors.push(m),
    },
    __errors: [],
    __warns: [],
  }, over || {});
  win.document = docStub(win);
  win.window = win;
  win.self = win;
  win.globalThis = win;
  vm.createContext(win);
  for (const f of sources()) {
    vm.runInContext(fs.readFileSync(f, 'utf8'), win, { filename: f });
  }
  return win;
}

test('every module the launcher ships registers itself', () => {
  const win = load();
  const files = fs.readdirSync(path.join(DIR, 'widget'))
    .filter((f) => f.endsWith('.js') && !f.endsWith('.test.js'))
    .map((f) => f.replace(/\.js$/, ''));
  for (const name of files) {
    assert.ok(win.__bd_cheat_mod[name], `widget/${name}.js did not register as ${name}`);
  }
});

test('the widget comes up with no game present, and does not throw', () => {
  const win = load();
  assert.deepStrictEqual(win.__errors, [], 'no module reported itself missing');
  assert.ok(win.__bd_cheat, 'the console surface is exposed');
  assert.strictEqual(typeof win.__bd_cheat.setSpeed, 'function');
});

test('a missing module is named rather than dying as a TypeError', () => {
  const win = {
    addEventListener: () => {}, setInterval: () => 0, __errors: [], __warns: [],
  };
  win.console = { log: () => {}, warn: () => {}, error: (m) => win.__errors.push(m) };
  win.document = docStub(win);
  win.window = win; win.self = win; win.globalThis = win;
  vm.createContext(win);
  vm.runInContext(fs.readFileSync(path.join(DIR, 'widget.js'), 'utf8'), win);
  assert.strictEqual(win.__errors.length, 1);
  assert.match(win.__errors[0], /widget\/css\.js/);
  assert.strictEqual(win.__bd_cheat, undefined, 'nothing half-built is left behind');
});

test('reading state with no game returns nothing instead of throwing', () => {
  const win = load();
  assert.strictEqual(win.__bd_cheat.getRes('gold'), undefined);
  assert.strictEqual(win.__bd_cheat.setRes('gold', 1), false);
  assert.strictEqual(win.__bd_cheat.upgrades(), null);
  assert.strictEqual(win.__bd_cheat.slot(), null);
  assert.strictEqual(win.__bd_cheat.tickMs(), null);
});

test('achievement blocking is on before anything else happens', () => {
  const win = load();
  assert.strictEqual(win.__bd_cheat.state.blockAchievements, true,
    'cheated progress must not reach Steam by default');
});

test('the stylesheet is real CSS, not an empty string', () => {
  const win = load();
  assert.ok(win.__bd_cheat_mod.css.CSS.includes('#bd{'), 'the panel has styles');
  assert.ok(win.__bd_cheat_mod.css.CSS.length > 1000);
});

test('loading twice does not build a second widget', () => {
  const win = load();
  const first = win.__bd_cheat;
  vm.runInContext(fs.readFileSync(path.join(DIR, 'widget.js'), 'utf8'), win);
  assert.strictEqual(win.__bd_cheat, first, 'the __BD_CHEAT__ guard held');
});

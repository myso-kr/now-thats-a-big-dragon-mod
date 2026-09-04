'use strict';
// Checks the dialogue policy without the game, against an injected fake DOM.
//
// The option labels come from the real .ink files rather than from strings written
// here, and every test runs in more than one language. Policies used to match a Korean
// substring, so once the mod became multilingual four of the eight branching dialogues
// held for thirty seconds and then took whatever came first - and no test noticed,
// because every test was written in Korean too.

const fs = require('fs');
const path = require('path');
const test = require('node:test');
const assert = require('node:assert');
const { create } = require('./dialog.js');
const ink = require('../../../lib/ink.js');

const LOCALE = path.join(__dirname, '..', '..', '..', 'locale', 'dialogs');

/** The option-label table of one shipped language, exactly as the launcher injects it. */
function tableFor(lang) {
  const dir = path.join(LOCALE, lang);
  return ink.choiceTable((n) => fs.readFileSync(path.join(dir, n), 'utf8'), fs.readdirSync(dir));
}

// Korean was the language the policies were written against; the others are the ones
// that were silently broken. Vietnamese and Russian differ from Korean in word order
// and in script, and Spanish puts an interpolation at the front of a label.
const LANGS = ['ko', 'vi', 'ru', 'es', 'zh-Hans'];
const TABLES = Object.fromEntries(LANGS.map((l) => [l, tableFor(l)]));

/** What the game would draw for one dialogue: its labels with the values filled in. */
function onScreen(lang, file, from, count, values = {}) {
  return TABLES[lang][file].slice(from, from + count)
    .map((label) => label.replace(/\{(\w+)\}/g, (_, k) => (k in values ? values[k] : '1000')));
}

/** A minimal fake DOM. querySelector uses the selector string itself as the key. */
function fakeDoc({ wrapper = true, choices = [], cont = false, skip = false } = {}) {
  const clicked = [];
  const mk = (text, i) => ({
    textContent: text,
    click() { clicked.push(i); },
  });
  const nodes = choices.map(mk);
  return {
    clicked,
    querySelector(sel) {
      if (sel === '[data-testid=dialog-wrapper]') return wrapper ? {} : null;
      if (sel === '.no-choice-prompt') return cont ? mk('continue', 'cont') : null;
      if (sel === '[data-testid=dialog-skip-typing]') return skip ? mk('skip', 'skip') : null;
      return null;
    },
    querySelectorAll(sel) {
      return sel === '.choice-prompt' ? nodes : [];
    },
  };
}

function make(doc, over = {}) {
  const logs = [];
  const holds = [];
  const d = create({
    cfg: { askChoices: false },
    log: (tag, text, level) => logs.push({ tag, text, level }),
    hold: (why) => holds.push(why),
    resourceFlow: () => ({ food: -1, wood: -10, ore: -1 }),
    RESOURCES: ['food', 'wood', 'ore'],
    choiceTable: TABLES.ko,
    doc,
    now: over.now || Date.now,
    ...over,
  });
  return { d, logs, holds };
}

const SNAP = { food: 1000, wood: 100, ore: 1000 };

test('with no choices it presses continue', () => {
  const doc = fakeDoc({ cont: true });
  const { d } = make(doc);
  assert.strictEqual(d.handleDialog(SNAP), true);
  assert.deepStrictEqual(doc.clicked, ['cont']);
});

test('no dialogue means false - returning true here stalls autoplay forever', () => {
  const { d } = make(fakeDoc({ wrapper: false }));
  assert.strictEqual(d.handleDialog(SNAP), false);
});

test('options not yet drawn are not mistaken for an unknown dialogue', () => {
  const doc = fakeDoc({ choices: ['', '', ''] });
  const { d, holds } = make(doc);
  assert.strictEqual(d.handleDialog(SNAP), true);
  assert.deepStrictEqual(doc.clicked, [], 'nothing is pressed');
  assert.deepStrictEqual(holds, [], 'and nothing is held');
});

for (const lang of LANGS) {
  const opts = (file, from, count, values) => onScreen(lang, file, from, count, values);
  const mk = (doc, over) => make(doc, { choiceTable: TABLES[lang], ...over });

  test(`[${lang}] merchant: buys whichever resource runs out first`, () => {
    // wood flow -10 against a stock of 100: a 10-second runway, the most urgent
    const doc = fakeDoc({ choices: opts('trading', 0, 4) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [1], 'wood is the one to buy');
  });

  test(`[${lang}] merchant: buys nothing when nothing is short`, () => {
    const doc = fakeDoc({ choices: opts('trading', 0, 4) });
    const { d } = mk(doc, { resourceFlow: () => ({ food: 5, wood: 5, ore: 5 }) });
    d.handleDialog({ food: 1e6, wood: 1e6, ore: 1e6 });
    assert.deepStrictEqual(doc.clicked, [3]);
  });

  test(`[${lang}] merchant: only the refusal is shown when nothing is affordable`, () => {
    // The three resource options sit behind one ink condition, so they are all absent
    // together - and then the on-screen index of the refusal is 0, not 3.
    const doc = fakeDoc({ choices: opts('trading', 3, 1) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [0]);
  });

  test(`[${lang}] merchant farewell: does not ask him to come less often`, () => {
    const doc = fakeDoc({ choices: opts('trading', 4, 2) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [0], 'coming less often costs 600 ticks of trading');
  });

  test(`[${lang}] pope: contributes, because refusing heals the boss`, () => {
    const doc = fakeDoc({ choices: opts('pope_visit', 0, 2) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [0]);
  });

  test(`[${lang}] invasion: defends with the larger force`, () => {
    const doc = fakeDoc({
      choices: opts('invasion_start', 0, 3, { unitsCountFew: '200', unitsCountMany: '1000' }),
    });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [2], 'the small force is wiped out');
  });

  test(`[${lang}] invasion: pays only when no defence is offered`, () => {
    const doc = fakeDoc({ choices: opts('invasion_start', 0, 1) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [0]);
  });

  test(`[${lang}] catapult: pays for it (cats are ten times the damage)`, () => {
    const doc = fakeDoc({ choices: opts('catapult', 0, 2) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [1]);
  });

  test(`[${lang}] king's dungeon: takes the bribe - he can be stopped later`, () => {
    const doc = fakeDoc({ choices: opts('king_dungeon', 0, 2) });
    const { d } = mk(doc);
    d.handleDialog(SNAP);
    assert.deepStrictEqual(doc.clicked, [1]);
  });

  test(`[${lang}] every option group is recognised from its text alone`, () => {
    const { d } = mk(fakeDoc());
    const groups = [
      ['trading', 0, 4], ['trading', 4, 2], ['pope_visit', 0, 2],
      ['invasion_start', 0, 3], ['catapult', 0, 2], ['dungeon_rescue', 0, 1],
      ['king_dungeon', 0, 2], ['king_dungeon_2', 0, 1],
    ];
    for (const [file, from, count] of groups) {
      const id = d.identifyStory(opts(file, from, count));
      assert.ok(d.CHOICE_POLICY[id], `not classified: ${file}[${from}]`);
    }
  });
}

test('unknown options: a person is given time to step in first', () => {
  const doc = fakeDoc({ choices: ['An option never seen before', 'Nor this one'] });
  const { d, holds } = make(doc, { now: () => 1000 });
  assert.strictEqual(d.handleDialog(SNAP), true);
  assert.deepStrictEqual(doc.clicked, [], 'nothing is pressed straight away');
  assert.strictEqual(holds.length, 1);
});

test('unknown options: after the grace period it takes the first', () => {
  const doc = fakeDoc({ choices: ['An option never seen before', 'Nor this one'] });
  let t = 1000;
  const { d, logs } = make(doc, { now: () => t });
  d.handleDialog(SNAP);          // first observation
  t += 31000;                    // past the grace period
  d.handleDialog(SNAP);
  assert.deepStrictEqual(doc.clicked, [0], 'better than standing still');
  assert.ok(logs.some((l) => l.level === 'warn'), 'and it says so loudly');
});

test('with no option labels at all it holds rather than guessing', () => {
  // What the old code did in every language but Korean. It must be visible, not silent.
  const doc = fakeDoc({ choices: onScreen('vi', 'trading', 0, 4) });
  const { d, holds } = make(doc, { choiceTable: {}, now: () => 1000 });
  d.handleDialog(SNAP);
  assert.deepStrictEqual(doc.clicked, []);
  assert.strictEqual(holds.length, 1);
});

test('the ask-me setting hands the choice back to the player', () => {
  const doc = fakeDoc({ choices: onScreen('ko', 'trading', 0, 4) });
  const { d, holds } = make(doc, { cfg: { askChoices: true } });
  d.handleDialog(SNAP);
  assert.deepStrictEqual(doc.clicked, []);
  assert.deepStrictEqual(holds, ['waiting on a choice']);
});

test('the story id from start_dialog survives an option set we cannot match', () => {
  const doc = fakeDoc({ choices: onScreen('ko', 'king_dungeon', 0, 2) });
  const { d } = make(doc);
  d.noteStory('king_dungeon');
  d.handleDialog(SNAP);
  assert.deepStrictEqual(doc.clicked, [1]);
});

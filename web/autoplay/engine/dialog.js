// Answering dialogue: pick an option, and never stall forever on an unknown one.
//
// It reaches for neither the game nor the DOM directly - everything it needs is
// injected, which is what makes it testable without the game. (engine/dialog.test.js)
(function (root) {
  'use strict';

  // Which slice of a file's option labels belongs to which dialogue id.
  //
  // Nearly every file has one group of options and the two line up; `trading` is the
  // exception, where refusing to buy raises a second, separate group. Assuming one
  // group per file is exactly why that one was missed once already.
  //
  // The positions are the same in every language - tools/check-dialogs.js enforces
  // that a translated .ink keeps the structure of the original - so a policy can name
  // an option by where it sits in the file and never by what it says.
  const STORY_CHOICES = [
    { id: 'trading', file: 'trading', from: 0, count: 4 },
    { id: 'trading_farewell', file: 'trading', from: 4, count: 2 },
    { id: 'pope_visit', file: 'pope_visit', from: 0, count: 2 },
    { id: 'invasion_start', file: 'invasion_start', from: 0, count: 3 },
    { id: 'catapult', file: 'catapult', from: 0, count: 2 },
    { id: 'dungeon_rescue', file: 'dungeon_rescue', from: 0, count: 1 },
    { id: 'king_dungeon', file: 'king_dungeon', from: 0, count: 2 },
    { id: 'king_dungeon_2', file: 'king_dungeon_2', from: 0, count: 1 },
  ];

  // Positions within a group, so a policy reads as what it means rather than as an
  // index. These follow the option order in the .ink files, which is fixed.
  const OPT = {
    trading: { food: 0, wood: 1, ore: 2, decline: 3 },
    trading_farewell: { goodbye: 0, comeLessOften: 1 },
    pope_visit: { contribute: 0, convert: 1 },
    invasion_start: { pay: 0, defendFew: 1, defendMany: 2 },
    catapult: { keepRocks: 0, pay: 1 },
    king_dungeon: { stopHim: 0, takeBribe: 1 },
  };

  // How long a person gets to step in on an unknown option. After that, take the first.
  const UNKNOWN_CHOICE_GRACE = 30000;

  /**
   * A matcher for one option label.
   *
   * The label holds the interpolations ink will fill in - `Pay {cost} gold` reaches
   * the screen as `Pay 1.2M gold` - so the literal parts have to match and the rest
   * is free. Everything else is escaped: a label may contain `(`, `?` or `.`, and
   * Spanish opens questions with `¿`.
   */
  function labelMatcher(label) {
    // Both sides are trimmed. A label carrying a stray space at its end is a typo
    // nobody would ever see in the game, and it must not be the reason autoplay stops
    // recognising an option - the Chinese merchant had exactly one.
    const parts = String(label).trim()
      .split(/\{[^}]*\}/)
      .map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    return new RegExp(`^\\s*${parts.join('.*')}\\s*$`);
  }

  /**
   * @param {object} deps
   *   cfg          { askChoices }
   *   log          (tag, text, level?) => void
   *   hold         (reason) => void
   *   resourceFlow (snap) => { food, wood, ore }
   *   RESOURCES    ['food','wood','ore']
   *   doc          document (a fake DOM in tests)
   *   now          () => number
   *   choiceTable  { '<file stem>': ['label', ...] } for the language in play
   */
  function create(deps) {
    const { cfg, log, hold, resourceFlow, RESOURCES } = deps;
    const doc = deps.doc || (typeof document !== 'undefined' ? document : null);
    const now = deps.now || Date.now;
    const table = deps.choiceTable
      || (typeof window !== 'undefined' ? window.__bd_dialogChoices : null)
      || {};

    let currentStory = null;
    const unknownChoice = { sig: null, at: 0 };

    /** The compiled matchers for one dialogue's options, or null if we have no labels. */
    function matchersFor(id) {
      const spec = STORY_CHOICES.find((s) => s.id === id);
      if (!spec) return null;
      const labels = table[spec.file];
      if (!labels) return null;
      const slice = labels.slice(spec.from, spec.from + spec.count);
      return slice.length === spec.count ? slice.map(labelMatcher) : null;
    }

    /**
     * Which dialogue is on screen.
     *
     * The game's `start_dialog` event carries the id and knows no language, so that is
     * the signal; this only has to recognise a dialogue the event did not announce -
     * one already on screen when autoplay started, say. A dialogue matches when every
     * option on screen matches one of its labels.
     */
    function identifyStory(texts) {
      const shown = texts.filter((t) => t && t.length);
      if (shown.length) {
        for (const spec of STORY_CHOICES) {
          const ms = matchersFor(spec.id);
          if (!ms) continue;
          if (shown.every((t) => ms.some((re) => re.test(t)))) {
            currentStory = spec.id;
            return spec.id;
          }
        }
      }
      return currentStory;
    }

    /**
     * Where option `n` of dialogue `id` is on screen, or -1.
     *
     * Options behind an ink condition are simply absent when it does not hold - the
     * merchant with nothing you can afford shows only "no thanks" - so the position in
     * the file is not the position on screen, and the label is what bridges them.
     *
     * Two options can also carry the *same* label: the invasion offers "defend with
     * {unitsCountFew} units" and "defend with {unitsCountMany} units", which differ
     * only in a number ink fills in. Nothing in the text can separate those, so the
     * k-th option with a given label is matched to the k-th such option on screen -
     * ink never reorders them.
     */
    function optionAt(id, n, texts) {
      const ms = matchersFor(id);
      if (!ms || !ms[n]) return -1;
      const want = ms[n].source;
      const nth = ms.slice(0, n).filter((re) => re.source === want).length;
      let seen = 0;
      for (let i = 0; i < texts.length; i += 1) {
        if (!ms[n].test(texts[i])) continue;
        if (seen === nth) return i;
        seen += 1;
      }
      // Fewer of them are on screen than the file has - the condition on the later one
      // did not hold. The last match is then the best available.
      let last = -1;
      texts.forEach((t, i) => { if (ms[n].test(t)) last = i; });
      return nth > 0 ? last : -1;
    }

    const CHOICE_POLICY = {
      trading: (texts, snap, at) => {
        const flow = resourceFlow(snap);
        const want = RESOURCES
          .map((r) => ({ r, rw: flow[r] < 0 ? snap[r] / -flow[r] : Infinity }))
          .sort((a, b) => a.rw - b.rw)[0];
        const i = at(OPT.trading[want.r]);
        return want.rw < 600 && i >= 0 ? i : at(OPT.trading.decline);
      },
      // "Come less often" only pushes the trading event back 600 ticks. In a resource
      // chapter, trading is the only gold-to-resource path, so more visits is better.
      // Both options were measured to resume the dialogue group correctly.
      trading_farewell: (t, s, at) => at(OPT.trading_farewell.goodbye),
      pope_visit: (t, s, at) => at(OPT.pope_visit.contribute),
      // Defending with few units loses them all, so take the larger force when the
      // game offers it and pay the ransom only when it does not.
      invasion_start: (t, s, at) => {
        const many = at(OPT.invasion_start.defendMany);
        if (many >= 0) return many;
        const few = at(OPT.invasion_start.defendFew);
        return few >= 0 ? few : at(OPT.invasion_start.pay);
      },
      catapult: (t, s, at) => at(OPT.catapult.pay),      // cats are ten times the damage
      dungeon_rescue: (t, s, at) => at(0),
      king_dungeon: (t, s, at) => at(OPT.king_dungeon.takeBribe),  // he can be stopped later
      king_dungeon_2: (t, s, at) => at(0),
    };

    /** True when a dialogue was handled; false when none is on screen. */
    function handleDialog(snap) {
      if (!doc) return false;
      const wrap = doc.querySelector('[data-testid=dialog-wrapper]');
      if (!wrap) return false;

      const choices = [...doc.querySelectorAll('.choice-prompt')];
      if (choices.length) {
        if (cfg.askChoices) { hold('waiting on a choice'); return true; }
        const texts = choices.map((e) => (e.textContent || '').trim());
        // While options are still being drawn their text is empty. That is not an unknown
        // dialogue but one that has not arrived - look again next cycle rather than stall.
        if (!texts.some((t) => t.length)) return true;

        const story = identifyStory(texts);
        const policy = CHOICE_POLICY[story];
        const idx = policy
          ? policy(texts, snap, (n) => optionAt(story, n, texts))
          : -1;

        if (idx < 0 || !choices[idx]) {
          // Stalling forever on an unknown option ends an unattended run right there.
          // So hold briefly - a watching person can choose - and if that passes, take the
          // first option and say so loudly. Moving on beats standing still.
          const sig = texts.filter(Boolean).join(' / ').slice(0, 80);
          if (unknownChoice.sig !== sig) { unknownChoice.sig = sig; unknownChoice.at = now(); }
          if (now() - unknownChoice.at < UNKNOWN_CHOICE_GRACE) {
            hold(`unclassified choice: ${story || sig}`);
            return true;
          }
          unknownChoice.sig = null;
          log('DLG', `unclassified choice - taking the first: ${sig}`, 'warn');
          choices[0].click();
          return true;
        }

        unknownChoice.sig = null;
        choices[idx].click();
        log('DLG', `${story} -> "${texts[idx]}"`);
        return true;
      }

      const cont = doc.querySelector('.no-choice-prompt');
      if (cont) { cont.click(); return true; }
      const skip = doc.querySelector('[data-testid=dialog-skip-typing]');
      if (skip) { skip.click(); return true; }
      return true;
    }

    /**
     * The dialogue id from the game's start_dialog event. Language-independent, and
     * the primary signal - matching option text only has to cover a dialogue that was
     * already on screen before autoplay began.
     */
    function noteStory(id) { if (id) currentStory = id; }

    return {
      handleDialog, identifyStory, noteStory, optionAt, CHOICE_POLICY, STORY_CHOICES,
    };
  }

  const api = { create, STORY_CHOICES, OPT, UNKNOWN_CHOICE_GRACE, labelMatcher };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too, and the usual "module exists, therefore Node" check is wrong here.
  // Register on the namespace whenever a window exists, and fill module.exports too.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).dialog = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).dialog = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

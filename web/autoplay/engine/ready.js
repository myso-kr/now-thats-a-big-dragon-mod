// The ready latch: has the game's generation table been computed for this run yet?
//
// Right after a run starts the table is empty. That is the only moment at which a
// unit's defined `baseGeneration` should stand in for its measured output — but
// deciding that per unit, by "no value, so substitute", cannot tell two zeros apart:
//
//   zero because the run just began and nothing is computed yet
//   zero because mana ran dry and this wizard really does produce nothing
//
// Substituting for the second kind keeps buying useless units. That bug was real.
//
// Becoming ready is a single monotonic transition per run, so it belongs in a latch.
// Once on it never flips back for that run, and no unit gets a substitute afterwards.
// That makes "mana drought mistaken for not-yet-computed" structurally impossible.
// (engine/ready.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const log = deps.log || function () {};
    const state = { on: false, level: null, hp: null, gold: null };

    /** Forget everything and wait for readiness again. */
    function reset() {
      state.on = false; state.level = null; state.hp = null; state.gold = null;
    }

    function update(snap) {
      if (snap.level !== state.level) {          // a different run: start over
        state.level = snap.level;
        state.on = false; state.hp = null; state.gold = null;
        return;
      }
      if (state.on) return;

      // Condition 1: the table holds at least one finite positive number.
      let any = false;
      for (const k of Object.keys(snap.stats || {})) {
        const v = snap.stats[k] && snap.stats[k].mainIndividualGenerationStat;
        if (typeof v === 'number' && Number.isFinite(v) && v > 0) { any = true; break; }
      }
      if (!any) return;

      // Condition 2: a tick has actually run — a monotonic counter moved.
      if (state.hp != null && (snap.hp < state.hp || snap.gold > state.gold)) {
        state.on = true;
        log('SYS', 'generation table ready - no more defined-value substitution');
      }
      state.hp = snap.hp; state.gold = snap.gold;
    }

    return {
      update,
      reset,
      get on() { return state.on; },
      report: () => Object.assign({}, state),
    };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).ready = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).ready = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

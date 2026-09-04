// Purchase arithmetic: what n more of something costs, how many we can afford, and
// how often a unit actually fires.
//
// Every formula here is the game's own, re-derived rather than approximated, so a
// plan made from these numbers is affordable at execution time. (engine/cost.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const PERIOD_UPGRADE = deps.PERIOD_UPGRADE || {};

    /**
     * Cost of buying `n` more when `purchased` are already owned.
     * The game prices each successive copy at `growth` times the last, so the total
     * is a geometric series — not `base * n`.
     */
    const costOf = (base, growth, purchased, n) => (growth === 1
      ? base * n
      : base * Math.pow(growth, purchased) * (1 - Math.pow(growth, n)) / (1 - growth));

    /**
     * The largest n with costOf(...) <= gold. Inverting the series analytically
     * rather than counting up, which the tick executor calls too often to afford.
     */
    function maxAffordable(gold, base, growth, purchased) {
      if (!(base > 0) || !(gold > 0)) return 0;
      if (growth === 1) return Math.floor(gold / base);
      const r = Math.pow(growth, purchased);
      const s = 1 + (gold * (growth - 1)) / (base * r);
      if (!(s > 0)) return 0;
      return Math.max(0, Math.floor(Math.log(s) / Math.log(growth)));
    }

    /**
     * Ticks between two firings, after period-shortening upgrades. The game's dp():
     *   max(1, ticksToGenerate + multiplier)
     *
     * Reading `ticksToGenerate` alone is the bug this replaces: a thief with fastHands
     * fires five times as often as its stored period claims, so every valuation that
     * ignored this understated thieves by the same factor.
     */
    function effectivePeriod(snap, id) {
      const g = snap.gen[id];
      const base = (g && g.ticksToGenerate) || 1;
      const key = PERIOD_UPGRADE[id];
      if (!key) return base;
      const u = (snap.up && snap.up[id] && snap.up[id][key]) || null;
      if (!u || typeof u.multiplier !== 'number') return base;
      return Math.max(1, base + u.multiplier);
    }

    return { costOf, maxAffordable, effectivePeriod };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).cost = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).cost = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

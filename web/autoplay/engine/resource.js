// Resources: what we produce, what we spend, and how long until we run dry.
//
// Resources are not something that makes DPS — they are the precondition for making
// any. So they are handled as a constraint ("top up when short"), never as a
// candidate competing on score. Per-second food and per-second damage are not
// commensurable, and putting them on one scale buys nothing but farmers.
// (engine/resource.test.js)
(function (root) {
  'use strict';

  // Keep this much surplus relative to consumption.
  const SURPLUS_MARGIN = 0.15;
  // Hold this many seconds of consumption as stock.
  const STOCK_SECONDS = 300;

  function create(deps) {
    const RESOURCES = deps.RESOURCES;
    const RESOURCE_UNITS = deps.RESOURCE_UNITS;
    const UPKEEP = deps.UPKEEP;

    // Spending resources is this chapter's rule. Deciding it from units owned would
    // read false at the start of every new run, exactly when it matters most.
    const isResourceChapter = (snap) => snap.level === 'newGamePlus';

    /** Production minus upkeep. Negative here means it dries up eventually. */
    function resourceFlow(snap) {
      const out = {};
      for (const r of RESOURCES) out[r] = 0;
      for (const [id, res] of Object.entries(RESOURCE_UNITS)) {
        const u = snap.stats[id];
        const per = (u && u.mainIndividualGenerationStat) || 0;
        out[res] += per * ((snap.gen[id] && snap.gen[id].owned) || 0);
      }
      for (const [id, up] of Object.entries(UPKEEP)) {
        const owned = (snap.gen[id] && snap.gen[id].owned) || 0;
        if (!owned) continue;
        for (const [r, v] of Object.entries(up)) out[r] -= v * owned;
      }
      return out;
    }

    function totalUpkeep(snap) {
      const out = {};
      for (const r of RESOURCES) out[r] = 0;
      for (const [id, up] of Object.entries(UPKEEP)) {
        const owned = (snap.gen[id] && snap.gen[id].owned) || 0;
        if (!owned) continue;
        for (const [r, v] of Object.entries(up)) out[r] += v * owned;
      }
      return out;
    }

    /** Seconds until the first resource hits zero. Infinite outside a resource chapter. */
    function runway(snap) {
      if (!isResourceChapter(snap)) return Infinity;
      const flow = resourceFlow(snap);
      let min = Infinity;
      for (const r of RESOURCES) {
        if (flow[r] >= 0) continue;
        min = Math.min(min, snap[r] / -flow[r]);
      }
      return min;
    }

    /** The one resource unit to buy right now, or null when none is needed. */
    function resourceNeed(snap) {
      if (!isResourceChapter(snap)) return null;
      const flow = resourceFlow(snap);
      const upkeep = totalUpkeep(snap);
      let worst = null;
      for (const [id, r] of Object.entries(RESOURCE_UNITS)) {
        const g = snap.gen[id];
        if (!g || !g.isUnlocked) continue;
        const target = Math.max(1, upkeep[r] * SURPLUS_MARGIN);
        const stockShort = upkeep[r] > 0 && snap[r] < upkeep[r] * STOCK_SECONDS;
        if (flow[r] >= target && !stockShort) continue;       // already fine
        const deficit = target - flow[r];
        if (!worst || deficit > worst.deficit) worst = { id, r, deficit };
      }
      return worst;
    }

    /**
     * Would buying one of `id` push any resource into deficit? Refusing up front is
     * always cheaper than firing units afterwards.
     */
    function unsafeToBuy(snap, id) {
      if (!isResourceChapter(snap) || !UPKEEP[id]) return false;
      const flow = resourceFlow(snap);
      for (const [r, v] of Object.entries(UPKEEP[id])) if (flow[r] - v < 0) return true;
      return false;
    }

    return {
      isResourceChapter, resourceFlow, totalUpkeep, runway, resourceNeed, unsafeToBuy,
    };
  }

  const api = { create, SURPLUS_MARGIN, STOCK_SECONDS };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).resource = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).resource = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

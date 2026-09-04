// What to buy next, in order. Turns valuations into a ranked, affordable shortlist.
//
// This module decides nothing about *when* to buy — the tick executor does that. It
// only answers "given this snapshot and this horizon, what is worth the gold?"
// (engine/plan.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const cfg = deps.cfg;
    const value = deps.value;                 // engine/value.js
    const cost = deps.cost;                   // engine/cost.js
    const resource = deps.resource;           // engine/resource.js
    const ready = deps.ready;                 // engine/ready.js
    const cal = deps.cal || null;             // engine/calib.js, may be absent
    const calKey = deps.calKey || (() => '');
    const SPECIAL_VALUE = deps.SPECIAL_VALUE || {};
    const C = deps.consts;

    /**
     * Add a candidate to the list, applying the calibration coefficient and dropping
     * quarantined families.
     *
     * `value` is the horizon integral and `score` is contribution per gold. The
     * coefficient multiplies only `score`: the prediction fed back into learning has
     * to be the model's own number, or the comparison against measurement is circular.
     */
    function push(list, x) {
      const key = calKey(x);
      if (cal && cal.quarantined(key)) return;
      x.key = key;
      x.score = (x.value / x.cost) * (cal ? cal.alpha(key) : 1);
      list.push(x);
    }

    /**
     * The fixed opening rule, used before the generation table is ready.
     * "Of the affordable direct-damage units, buy one of whichever has the highest
     * baseGeneration per gold."
     *
     * Not running the score model here is the whole point. Feeding defined values
     * into the score model lets those substitutes leak into normal operation — the
     * bug where a mana-starved wizard kept being bought at full price took exactly
     * that path. Substitutes stay confined to this rule.
     */
    function openingPlan(snap, budget) {
      let best = null;
      for (const id of C.OPENING_UNITS) {
        const g = snap.gen[id];
        if (!g || !g.isUnlocked) continue;
        const c = cost.costOf(g.cost.gold || 0, g.costGrowthRate, g.purchased, 1);
        if (!(c > 0) || c > budget) continue;
        const v = (g.baseGeneration || 0) / c;
        if (v > 0 && (!best || v > best.v)) best = { id, cost: c, v };
      }
      if (!best) return [];
      // `value` is what the calibration loop learns from. The opening rests on thin
      // evidence, so it is marked and kept out of learning entirely.
      return [{ kind: 'gen', id: best.id, cost: best.cost, score: best.v, opening: true }];
    }

    function candidates(snap, H) {
      const list = [];
      const budget = snap.gold * (1 - cfg.reservePct / 100);

      // During a resource drought, buy nothing that adds upkeep. Producers are
      // handled separately by resourceNeed(), outside this list.
      if (cfg.buyPaused) return list;

      // Before the table is ready, the score model is not run at all.
      if (!ready.on) return openingPlan(snap, budget);

      for (const [id, g] of Object.entries(snap.gen)) {
        if (!g.isUnlocked) continue;
        const c = cost.costOf(g.cost.gold || 0, g.costGrowthRate, g.purchased, 1);
        if (!(c > 0) || c > budget) continue;
        if (resource.unsafeToBuy(snap, id)) continue;
        // Resource units do not compete on score. 90 food per second and 0.75 damage
        // per second are not commensurable, and on one scale only food gets bought.
        if (C.RESOURCE_UNITS[id]) continue;
        const v = value.unitValue(snap, id, H, 0);
        if (v > 0) push(list, { kind: 'gen', id, cost: c, value: v });
      }

      for (const [cat, items] of Object.entries(snap.up || {})) {
        const catStat = snap.stats[cat] || {};
        const base = (catStat.damagePerTick || 0)
          + (catStat.goldGeneration || 0) * C.GOLD_WEIGHT;
        for (const [id, u] of Object.entries(items)) {
          // Whether an upgrade can be bought is `status`. `isUnlocked` belongs to
          // generators and is almost always false on upgrades — reading it is what
          // made 12 upgrades look like 1.
          if (u.status !== 'unlocked') continue;
          if (C.UPGRADE_BLACKLIST.has(id) || C.DUNGEON_ONLY.has(id)) continue;
          if (typeof u.purchaseLimit === 'number' && u.purchased >= u.purchaseLimit) continue;
          const c = cost.costOf((u.cost && u.cost.gold) || 0, u.costGrowthRate, u.purchased, 1);
          if (!(c > 0) || c > budget) continue;

          // Upgrades whose effect runs opposite to the generic formula are priced
          // first. Their bonusPerOwned is negative, so "bonus over multiplier" would
          // rank them below everything forever.
          const def = value.defensiveValue(snap, cat, id, u, H);
          if (def) { push(list, { kind: 'up', id, cat, cost: c, value: def }); continue; }
          if (C.PERIOD_UPGRADE[cat] === id) {
            const pv = value.periodValue(snap, cat, u, H);
            if (pv) push(list, { kind: 'up', id, cat, cost: c, value: pv });
            continue;
          }
          if (SPECIAL_VALUE[id]) {
            const sv = SPECIAL_VALUE[id](snap, u, H);
            if (sv) push(list, { kind: 'up', id, cat, cost: c, value: sv });
            continue;
          }
          const ratio = (u.bonusPerOwned || 0) / Math.max(1, u.multiplier || 1);
          let v = base * ratio * H * 2;        // upgrades are permanent: twice the horizon
          // With no units of that family yet, output is 0 and the formula cannot
          // price it. One-shot unlocks are worth taking when they are cheap.
          if (!(v > 0) && c <= budget * 0.2) v = H;
          if (v > 0) push(list, { kind: 'up', id, cat, cost: c, value: v });
        }
      }
      list.sort((a, b) => b.score - a.score);
      return list;
    }

    return { candidates, openingPlan, push };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).plan = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).plan = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

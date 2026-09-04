// The tick executor: spends gold against the current plan, once per game tick.
//
// This module makes no judgements about what is worth buying — the planner already
// ranked everything. Its whole job is to turn that ranking into purchases that are
// still affordable at this instant, without overspending. (engine/exec.test.js)
(function (root) {
  'use strict';

  // Actions per tick. Buying one would mean one purchase per second at 1x speed,
  // far below what the game comfortably absorbs.
  const TICK_BUDGET = 5;
  // Most units bought in a single dispatch.
  const BATCH_CAP = 25;

  // Only during a combat phase does the generation table update and units fight.
  //   coup_de_grace  ticks stop, clicks still land - the boss's last HP needs clicks
  //   any other non-combat phase  both ticks and clicks are dead
  // Either way the table freezes at its last combat value, so buying from it spends
  // gold on stale evidence. We stop buying and keep clicking.
  const BUY_PHASES = ['combat', null];

  function create(deps) {
    const cfg = deps.cfg;
    const S = deps.state;
    const log = deps.log;
    const dispatch = deps.dispatch;
    const buyUpgrade = deps.buyUpgrade;
    const cost = deps.cost;
    const resource = deps.resource;
    const plan = deps.plan;                 // { list, planH, at, replan }
    const game = deps.game;                 // currency / generators / upgrades / slotStore
    const snapshot = deps.snapshot;
    const playable = deps.playable;
    const calNote = deps.calNote || function () {};
    const now = deps.now || (() => Date.now());

    /** Gold we are allowed to commit, after the reserve and what this tick already spent. */
    const budgetOf = (c, spent) => c.getState().gold * (1 - cfg.reservePct / 100) - spent;

    /**
     * Resource shortfall comes before anything else — it is a constraint, not a
     * purchase competing on score. Returns true when it consumed this tick.
     */
    function fillResource(snap, c) {
      const need = resource.resourceNeed(snap);
      if (!need) return false;
      const g = snap.gen[need.id];
      const n = Math.min(BATCH_CAP, cost.maxAffordable(
        budgetOf(c, 0), g.cost.gold || 0, g.costGrowthRate, g.purchased,
      ));
      if (n >= 1 && dispatch('buy_generator', { id: need.id, amountToBuy: n })) {
        S.lastAction = need.id + (n > 1 ? ` x${n}` : '');
        S.lastActionAt = now();
        log('RES', S.lastAction);
        return true;
      }
      // Not affordable: fall through. Stopping here would block unit buying forever.
      return false;
    }

    function onTick() {
      if (!S.running || S.phase === 'HOLD') return;
      if (!playable()) return;
      if (!cfg.buy) return;
      const phaseStore = game.slotStore('campaign-phase');
      const phase = phaseStore ? phaseStore.getState().phase : null;
      if (!BUY_PHASES.includes(phase)) return;

      const c = game.currency();
      if (!c) return;

      const snapNow = snapshot();
      if (snapNow && fillResource(snapNow, c)) return;

      let replanSoon = false;
      let spent = 0;
      for (let i = 0; i < TICK_BUDGET && plan.list.length; i += 1) {
        const gold = budgetOf(c, spent);
        const head = plan.list[0];
        if (!head || gold < head.cost) return;   // most ticks end here, in O(1)

        let ok = false;
        let label = head.id;
        if (head.kind === 'gen') {
          const g = game.generators()[head.id];
          if (!g) { plan.list.shift(); continue; }
          // The plan's price may be stale; recompute it at the moment of spending.
          const cap = head.opening ? 1 : BATCH_CAP;   // the opening buys one at a time
          const n = Math.min(cap, cost.maxAffordable(
            gold, g.cost.gold || 0, g.costGrowthRate, g.purchased,
          ));
          if (n < 1) { plan.list.shift(); replanSoon = true; continue; }
          // Buying in bulk is far cheaper in reducer and re-render cost than N ones.
          ok = dispatch('buy_generator', { id: head.id, amountToBuy: n });
          // dispatch goes through a React reducer, so it is asynchronous and the
          // result cannot be read here. Deduct optimistically to avoid overspending
          // within this same tick.
          if (ok) spent += cost.costOf(g.cost.gold || 0, g.costGrowthRate, g.purchased, n);
          if (ok && n > 1) label = `${head.id} x${n}`;
        } else {
          const u = (game.upgrades()[head.cat] || {})[head.id];
          if (!u) { plan.list.shift(); continue; }
          const uc = cost.costOf((u.cost && u.cost.gold) || 0, u.costGrowthRate, u.purchased, 1);
          if (!(uc > 0) || uc > gold) { plan.list.shift(); replanSoon = true; continue; }
          ok = buyUpgrade(head.cat, head.id, u.purchased || 0);
          if (ok) spent += uc;
        }
        if (!ok) return;
        // Record the prediction. When the window fills, it is compared against what
        // actually happened and the coefficient is learned from the difference.
        if (snapNow && head.key && !head.opening) calNote(head.key, head.value, plan.planH, snapNow);
        S.lastAction = `${head.kind === 'gen' ? '' : '^'}${label}`;
        S.lastActionAt = now();
        log(head.kind === 'gen' ? 'BUY' : 'UPG', label);
        plan.list.shift();
      }

      // Plan exhausted with gold still in hand: rebuild it now rather than idling up
      // to a second waiting for the 1 Hz planner.
      if ((replanSoon || !plan.list.length) && now() - plan.at > 250) plan.replan();
    }

    return { onTick, fillResource };
  }

  const api = { create, TICK_BUDGET, BATCH_CAP, BUY_PHASES };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).exec = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).exec = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

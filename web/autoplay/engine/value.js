// What one more of a thing is worth, in damage, over the planning horizon.
//
// Everything here answers one question: "if I spend gold on this, what do I get back
// before the boss dies?" It knows nothing about gold on hand, what is unlocked, or
// what to buy — that is the planner's job. (engine/value.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const CHAIN = deps.CHAIN;
    const RESOURCE_UNITS = deps.RESOURCE_UNITS;
    const GOLD_WEIGHT = deps.GOLD_WEIGHT;
    const FIRE_DEATH = deps.FIRE_DEATH || {};
    const FIRE_PERIOD = deps.FIRE_PERIOD || 600;
    const effectivePeriod = deps.effectivePeriod;
    const aliveTime = deps.aliveTime;
    const aliveTimeD = deps.aliveTimeD;
    const deathRate = deps.deathRate;
    const firePeriod = deps.firePeriod;

    /**
     * How far ahead to plan. The longer the boss takes, the better production chains
     * look, so the horizon has to follow the fight rather than be a fixed constant.
     */
    function horizon(snap) {
      if (snap.level === 'infinite' || snap.level === 'dummy') return 900;
      if (!snap.hp || !snap.dps) return 300;
      return Math.max(60, Math.min(900, 3 * (snap.hp / snap.dps)));
    }

    /**
     * One unit's output per second.
     *
     * The generation table is per firing, and a firing happens every
     * effectivePeriod ticks — a college (300 ticks) and a warrior (1 tick) are 300x
     * apart, so without this division they are not comparable at all.
     *
     * There is deliberately no substitution of defined values here. Before the ready
     * latch flips, the score model is not run at all, so this is never reached; after
     * it flips, a zero always means "genuinely zero right now" (a wizard with no mana),
     * and substituting there is what kept buying useless units.
     */
    function perUnit(snap, id) {
      const s = snap.stats[id];
      return ((s && s.mainIndividualGenerationStat) || 0) / effectivePeriod(snap, id);
    }

    /** One unit's value per second: damage plus gold converted to damage. */
    function unitRate(snap, id, depth) {
      const per = perUnit(snap, id);
      if (!per) return 0;
      const child = CHAIN[id];
      if (child) return depth >= 2 ? 0 : per * unitRate(snap, child, depth + 1);
      const s = snap.stats[id] || {};
      const owned = (snap.gen[id] && snap.gen[id].owned) || 0;
      const gold = owned > 0 ? ((s.goldGeneration || 0) / owned) / effectivePeriod(snap, id) : 0;
      return per + gold * GOLD_WEIGHT;
    }

    /**
     * Cumulative contribution of one more unit over horizon H.
     *   leaf:  value per second times how long it stays alive.
     *   chain: it makes r children per second and each works for the time remaining,
     *          so the integral folds to H squared over two.
     */
    function unitValue(snap, id, H, depth) {
      if (RESOURCE_UNITS[id]) return 0;         // resources are priced as a constraint
      const per = perUnit(snap, id);
      if (!per) return 0;
      const child = CHAIN[id];
      if (child) {
        if (depth >= 2) return 0;               // deep chains are unstable at short H
        const cr = unitRate(snap, child, depth + 1);
        if (!cr) return 0;
        // Production buildings do not die to the breath, but their children do.
        const life = aliveTime(snap, child, H);
        return per * cr * H * life / 2;
      }
      return unitRate(snap, id, depth) * aliveTime(snap, id, H);
    }

    /**
     * Value of a period-shortening upgrade. Taking the period from T to T' multiplies
     * that unit's output by T/T'.
     *
     * The generic "bonus divided by multiplier" formula scores these permanently
     * negative, because bonusPerOwned is negative for exactly the upgrades that help.
     */
    function periodValue(snap, id, u, H) {
      const g = snap.gen[id];
      const owned = (g && g.owned) || 0;
      if (!owned) return null;
      const T0 = effectivePeriod(snap, id);
      const T1 = Math.max(1, ((g && g.ticksToGenerate) || 1)
        + (u.multiplier || 0) + (u.bonusPerOwned || 0));
      if (T1 >= T0) return null;
      const gain = owned * unitRate(snap, id, 0) * (T0 / T1 - 1);
      return gain > 0 ? gain * aliveTime(snap, id, H) : null;
    }

    /**
     * Output that a defensive upgrade preserves. Lowering the death rate extends how
     * long every existing unit survives, and that increment is the upgrade's value.
     * The bonus/multiplier ratio formula cannot see this class of upgrade at all.
     */
    function defensiveValue(snap, cat, id, u, H) {
      const bonus = u.bonusPerOwned || 0;
      if (!bonus) return null;
      const targets = id === 'fireArmor' ? ['warrior']
        : (id === 'blessedAura' || id === 'smokeBomb' || id === 'sonicBarrier')
          ? Object.keys(FIRE_DEATH) : null;
      if (!targets) return null;

      const P0 = firePeriod(snap);
      // The sonic barrier lengthens the breath period rather than lowering deaths.
      const P1 = id === 'sonicBarrier'
        ? FIRE_PERIOD * 100 / Math.max(1, (u.multiplier != null ? u.multiplier : 100) + bonus)
        : P0;

      let sum = 0;
      for (const t of targets) {
        const owned = (snap.gen[t] && snap.gen[t].owned) || 0;
        if (!owned) continue;
        const rate = unitRate(snap, t, 0);
        if (!(rate > 0)) continue;
        const d0 = deathRate(snap, t);
        if (d0 <= 0) continue;                  // already immortal, nothing to protect
        // The death rate after buying one more step of this upgrade.
        let d1 = d0;
        if (id === 'sonicBarrier') {
          // deaths unchanged; only the period stretches
        } else if (id === 'smokeBomb') {
          const sb = (snap.up.thief && snap.up.thief.smokeBomb) || {};
          const p0 = sb.purchased > 0 ? Math.min(100, sb.purchased * bonus + 5) : 0;
          const p1 = Math.min(100, (sb.purchased + 1) * bonus + 5);
          d1 = p0 >= 100 ? 0 : d0 * (1 - p1 / 100) / (1 - p0 / 100);
        } else {
          d1 = Math.max(0, d0 - (FIRE_DEATH[t] || 0) * bonus / 100);
        }
        sum += owned * rate * (aliveTimeD(d1, H, P1) - aliveTimeD(d0, H, P0));
      }
      return sum > 0 ? sum : null;
    }

    return { horizon, perUnit, unitRate, unitValue, periodValue, defensiveValue };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).value = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).value = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

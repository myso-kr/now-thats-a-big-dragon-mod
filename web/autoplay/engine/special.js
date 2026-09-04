// Upgrades whose effect runs opposite to the sign of their bonusPerOwned.
//
// The generic "bonus over multiplier" formula scores every one of these at zero or
// below, forever, because a good effect is expressed as a negative number.
// So each is priced separately, by the game's own arithmetic. (engine/special.test.js)
(function (root) {
  'use strict';

  // Constants read out of the game. All in ticks.
  // Active duration is obnoxiousGuitarist.multiplier, defined as 10. The 5 below matches
  // the game's own ?? fallback, used only when that upgrade object is absent entirely.
  const INSP_ACTIVE = 5;
  const INSP_COOLDOWN = 60;   // encore.multiplier, as defined
  const INSP_FILL = 100;      // inspirationFillAmount - every this much raises the multiplier by 0.5
  const INSP_STEP = 0.5;
  const STUN_TICKS = 20;      // stunEffectTotalTickDuration 20000 / 1000
  const ROAR_PERIOD = 420;
  const MAX_MANA = 100;
  const GOLD_PER_DAMAGE = 0.1;

  /**
   * @param {object} deps
   *   effectivePeriod (snap, id) => number    effective firing period, in ticks
   *   aliveTime       (snap, id, H) => number time alive, allowing for the breath
   *   timedEvent      (id) => event | null
   *   GOLD_WEIGHT     the coefficient converting gold into damage
   */
  function create(deps) {
    const { effectivePeriod, aliveTime, timedEvent } = deps;
    const GOLD_WEIGHT = deps.GOLD_WEIGHT != null ? deps.GOLD_WEIGHT : 0.5;

    /** Total output per second as the game sums it: damage plus gold converted. */
    function totalRate(snap) {
      return (snap.dps || 0) + (snap.gps || 0) * GOLD_WEIGHT;
    }

    /** How fast inspiration accrues per second - bards, war cries and the rest. */
    function inspirationRate(snap) {
      let r = 0;
      for (const id of Object.keys(snap.stats || {})) {
        const g = snap.stats[id] && snap.stats[id].inspirationGeneration;
        if (g > 0) r += g / effectivePeriod(snap, id);
      }
      return r;
    }

    /**
     * Inspiration duty cycle: active / (active + cooldown + fill).
     * It can only fire once filled - the multiplier has to reach the luteSolo cap -
     * and the multiplier resets to 1 when active ends, so it fills from scratch each time.
     */
    function inspirationDuty(snap, cooldown) {
      const rate = inspirationRate(snap);
      if (!(rate > 0)) return 0;                      // nothing here generates inspiration
      const up = snap.up || {};
      const cap = (up.bard && up.bard.luteSolo && up.bard.luteSolo.multiplier) || 1.5;
      const og = up.bard && up.bard.obnoxiousGuitarist;
      const active = og && typeof og.multiplier === 'number' ? og.multiplier : INSP_ACTIVE;
      if (!(active > 0)) return 0;
      const steps = Math.max(1, (cap - 1) / INSP_STEP);
      const fill = INSP_FILL * steps / rate;          // seconds spent filling
      return active / (active + cooldown + fill);
    }

    /** encore shortens the inspiration cooldown; a higher duty cycle means all output spends longer multiplied. */
    function encoreValue(snap, u, H) {
      const c0 = typeof u.multiplier === 'number' ? u.multiplier : INSP_COOLDOWN;
      const c1 = Math.max(0, c0 + (u.bonusPerOwned || 0));
      if (c1 >= c0) return null;
      const up = snap.up || {};
      const cap = (up.bard && up.bard.luteSolo && up.bard.luteSolo.multiplier) || 1.5;
      const gain = totalRate(snap) * (cap - 1)
        * (inspirationDuty(snap, c1) - inspirationDuty(snap, c0));
      return gain > 0 ? gain * H : null;
    }

    /**
     * manaBoost lowers the mana threshold for a wizard's doubled damage.
     * The test is mana > multiplier, which starts at 100 while maximum mana is also
     * 100 - so before buying it, the doubled band never opens at all. The first
     * purchase is the transition from nothing to something.
     *
     * Time spent in the band is approximated as (max - threshold) / max, taking mana
     * to move across its whole range.
     */
    function manaBoostValue(snap, u, H) {
      const wiz = (snap.stats && snap.stats.wizard) || {};
      const dmg = (wiz.damagePerTick || 0) / effectivePeriod(snap, 'wizard');
      if (!(dmg > 0)) return null;
      const up = snap.up || {};
      const maxMana = ((up.wizard && up.wizard.manaPool && up.wizard.manaPool.multiplier)
        || MAX_MANA);
      const t0 = typeof u.multiplier === 'number' ? u.multiplier : MAX_MANA;
      const t1 = Math.max(0, t0 + (u.bonusPerOwned || 0));
      const band = (t) => Math.min(1, Math.max(0, (maxMana - t) / maxMana));
      const gain = dmg * (band(t1) - band(t0));       // the band doubles damage, so the increment is the damage itself
      return gain > 0 ? gain * aliveTime(snap, 'wizard', H) : null;
    }

    /**
     * piercedEardrums delays the stun. While stunned, only resource units run and
     * purchases are refused. It lowers roar's rate to multiplier%, lengthening the period.
     */
    function earValue(snap, u, H) {
      const base = timedEvent('roar');
      if (!base) return null;                        // this chapter has no roar
      const m0 = typeof u.multiplier === 'number' ? u.multiplier : 100;
      const m1 = Math.max(1, m0 + (u.bonusPerOwned || 0));
      if (m1 >= m0) return null;
      const period = base.duration || ROAR_PERIOD;
      const duty = (m) => Math.min(1, STUN_TICKS / (period * 100 / m));
      const gain = totalRate(snap) * (duty(m0) - duty(m1));
      return gain > 0 ? gain * H : null;
    }

    /**
     * manaSurge refills mana. Both multiplier and bonusPerOwned are 0, so the ratio
     * formula cannot price it and it falls through to the "cheap, so take it" fallback.
     * What it really does is fill mana to maximum, and mana drains by 1 per tick in
     * total, regardless of how many wizards there are. So the amount filled is exactly
     * how many seconds the wizards go on working.
     *
     * The generation table is no help here: with mana at 0 it reads 0. Potential
     * output is therefore computed directly, from the defined values and the upgrade
     * multipliers.
     */
    function manaSurgeValue(snap, u, H) {
      const g = snap.gen && snap.gen.wizard;
      const owned = (g && g.owned) || 0;
      if (!owned) return null;
      const up = (snap.up && snap.up.wizard) || {};
      const mult = (k, d) => (up[k] && typeof up[k].multiplier === 'number' ? up[k].multiplier : d);

      const maxMana = mult('manaPool', MAX_MANA) || MAX_MANA;
      const mana = snap.mana || 0;
      if (mana >= maxMana) return null;                 // already full: nothing to buy

      // Damage at 0 with mana in hand means mana is not what is blocking it - the ra gate
      // is shut, from a resource shortage or a production toggle. Filling mana then
      // achieves nothing at all.
      const st = (snap.stats && snap.stats.wizard) || {};
      if (mana > 0 && !(st.damagePerTick > 0)) return null;

      // Summed damage-multiplier-times-ticks still to come at mana m. Above the threshold it doubles.
      const thr = mult('manaBoost', MAX_MANA);
      const dmgTicks = (m) => 2 * Math.max(0, m - thr) + Math.min(m, thr);
      let gain = dmgTicks(maxMana) - dmgTicks(mana);
      if (!(gain > 0)) return null;
      gain = Math.min(gain, H);                          // nothing beyond the horizon counts

      const insp = (snap.inspiration && snap.inspiration.remainingActive > 0)
        ? (snap.inspiration.multiplier || 1) : 1;
      const s = ((g && g.baseGeneration) || 1) + mult('archimage', 0);
      const perTick = s * mult('magicMissile', 1) * insp * owned;   // relative to a=1
      const staff = mult('silverStaff', 1) * mult('goldenStaff', 1);
      const rate = perTick * (1 + GOLD_PER_DAMAGE * staff * GOLD_WEIGHT);

      // The warrior's manaSword - a bonus at mana >= 90 - is deliberately left out.
      // Including it would only raise the value, and undervaluing a 50-gold item is safe.
      const v = rate * gain;
      return v > 0 ? v : null;
    }

    const byId = {
      encore: encoreValue,
      manaBoost: manaBoostValue,
      piercedEardrums: earValue,
      manaSurge: manaSurgeValue,
    };

    return {
      byId,
      totalRate,
      inspirationRate,
      inspirationDuty,
      encoreValue,
      manaBoostValue,
      earValue,
      manaSurgeValue,
    };
  }

  const api = { create, INSP_ACTIVE, INSP_COOLDOWN, STUN_TICKS, ROAR_PERIOD, MAX_MANA };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).special = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).special = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

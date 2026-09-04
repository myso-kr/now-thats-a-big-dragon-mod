// Fire breath: what dies, when, how much of it, and how long a unit bought now lives.
//
// These are the game's own formulas, recovered from the bundle. This file knows
// nothing about the game - it takes a snapshot and an event lookup. (engine/fire.test.js)
(function (root) {
  'use strict';

  // Deaths are not a chance roll but a deterministic count: floor(owned x rate x (1 - mitigation/100)).
  // Warriors are at 1.0 - with no defence, one breath takes every last one of them.
  // Elves, catapults, buildings and resource units are absent here, so they never die.
  const FIRE_DEATH = { warrior: 1, wizard: 0.75, thief: 0.5, bard: 0.5, cleric: 0.5 };
  const FIRE_PERIOD = 600;   // Ticks. The game's event is defined as duration:600, once:false

  /** Find an upgrade wherever it sits. Tree membership does not match the formulas. */
  function findUp(snap, id) {
    for (const items of Object.values(snap.up || {})) if (items && items[id]) return items[id];
    return null;
  }

  /**
   * @param {object} deps
   *   timedEvent (id) => {duration,elapsed,rate,paused} | null
   *              Looks up a timed game event. Chapters differ in which events exist,
   *              so it must return null when absent - pricing an event that is not
   */
  function create(deps) {
    const timedEvent = deps.timedEvent;

    /** Breath period in seconds. sonicBarrier lowers the event rate to multiplier%. */
    function firePeriod(snap) {
      const sb = findUp(snap, 'sonicBarrier');
      const m = sb && typeof sb.multiplier === 'number' ? sb.multiplier : 100;
      return FIRE_PERIOD * 100 / Math.max(1, m);
    }

    /** Seconds to the next breath, or null when unreadable (half a period is assumed). */
    function fireIn() {
      const e = timedEvent('fire');
      if (!e) return null;
      const rate = typeof e.rate === 'number' && e.rate > 0 ? e.rate : 1;
      return Math.max(0, ((e.duration || FIRE_PERIOD) - (e.elapsed || 0)) / rate);
    }

    /** The fraction of this unit lost to one breath. Zero means it does not die. */
    function deathRate(snap, id) {
      const base = FIRE_DEATH[id];
      if (!base) return 0;
      const u = snap.up || {};
      const aura = ((u.cleric && u.cleric.blessedAura && u.cleric.blessedAura.multiplier) || 0);
      const armor = id === 'warrior'
        ? ((u.warrior && u.warrior.fireArmor && u.warrior.fireArmor.multiplier) || 0) : 0;
      let d = Math.max(0, base * (1 - (aura + armor) / 100));
      // The smoke bomb voids the breath outright, so discount by its expected value
      const sb = u.thief && u.thief.smokeBomb;
      if (sb && sb.purchased > 0) {
        const p = Math.min(100, sb.purchased * (sb.bonusPerOwned || 0) + 5);
        d *= 1 - p / 100;
      }
      return d;
    }

    /**
     * Seconds alive within horizon H, at death rate d and period P.
     * Untouched until the next breath, then multiplied by (1-d) each period after.
     * At d=1 - an unarmoured warrior - the first breath is the whole of its life.
     */
    function aliveTimeD(d, H, P) {
      if (d <= 0) return H;
      const t = fireIn();
      const first = Math.min(H, t == null ? P / 2 : t);
      const rem = H - first;
      if (rem <= 0 || d >= 1) return first;
      const k = 1 - d;
      return first + P * k * (1 - Math.pow(k, rem / P)) / (1 - k);
    }

    /** Seconds a unit bought right now actually works within horizon H. */
    function aliveTime(snap, id, H) {
      return aliveTimeD(deathRate(snap, id), H, firePeriod(snap));
    }

    /** How many die to this breath. Truncated, because the game floors it. */
    function casualties(snap, id) {
      const owned = (snap.gen && snap.gen[id] && snap.gen[id].owned) || 0;
      return Math.floor(owned * deathRate(snap, id));
    }

    return { firePeriod, fireIn, deathRate, aliveTime, aliveTimeD, casualties, findUp };
  }

  const api = { create, FIRE_DEATH, FIRE_PERIOD };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).fire = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).fire = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

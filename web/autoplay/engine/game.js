// The game contact surface. Everything that reaches into the running game goes
// through here, so the rest of the engine can be tested without a game at all.
//
// The one non-obvious part is finding `dispatch`. Two paths:
//
//   1) Walk up the React fiber tree from a DOM node and take the Provider's value.
//      This depends on no minified identifier at all, so it survives a game rebuild.
//   2) Failing that, use window.__bd_dispatch, which the bundle patch plants.
//
// They were measured to be the same object (=== true). Path 1 goes first because the
// dispatch confirmation step was the one bundle anchor tied to a minified identifier,
// and when it broke, all of autoplay went with it. (engine/game.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const win = deps.win;
    const doc = deps.doc;
    let fiberDispatch = null;
    let slot = null;

    const stores = () => win.__bd_stores || {};
    const stats = () => win.__bd_stats || {};
    const gameStore = () => win.global_game_store;
    const bus = () => win.events_manager;
    const engine = () => win.___EXCALIBUR_DEVTOOL;

    function findDispatchViaFiber() {
      try {
        let host = doc.querySelector('#ui-wrapper');
        if (!host) {
          host = [...doc.querySelectorAll('body *')]
            .find((e) => Object.keys(e).some((k) => k.startsWith('__reactFiber$')));
        }
        if (!host) return null;
        const key = Object.keys(host).find((k) => k.startsWith('__reactFiber$'));
        if (!key) return null;
        let f = host[key];
        for (let hop = 0; f && hop < 200; hop += 1) {
          const v = f.memoizedProps && f.memoizedProps.value;
          // The function handed to a Provider as its value is dispatch. One argument.
          if (typeof v === 'function' && v.length === 1) return v;
          f = f.return;
        }
      } catch (_bd) { /* the fiber shape changed: fall through to the patch */ }
      return null;
    }

    function rawDispatch() {
      if (typeof fiberDispatch === 'function') return fiberDispatch;
      fiberDispatch = findDispatchViaFiber();
      return fiberDispatch || win.__bd_dispatch;
    }

    const context = () => { const g = gameStore(); return g ? g.state.context.value : null; };
    const level = () => { const g = gameStore(); return g ? g.state.currentLevel.value : null; };

    /**
     * May we act on the game right now?
     *
     * A context of `dialog` with nothing on screen still means the game is running.
     * The game sometimes fails to put the context flag back, and taking it at face
     * value stops autoplay forever — so the screen, not the flag, is the evidence.
     */
    function playable() {
      const c = context();
      if (c === 'in_game') return true;
      if (c !== 'dialog') return false;
      return !doc.querySelector('[data-testid=dialog-wrapper]')
        && !doc.querySelector('.choice-prompt');
    }

    /**
     * The values actually in play live in the per-slot stores (slot_<slot>_<key>),
     * not the bare ones. Find the slot once from whichever currency store exists.
     */
    function slotStore(base) {
      const all = stores();
      if (!slot || !all[`slot_${slot}_${base}`]) {
        const k = Object.keys(all).find((x) => /^slot_.+_currency$/.test(x));
        slot = k ? k.slice(5, -('_currency'.length)) : null;
      }
      return (slot && all[`slot_${slot}_${base}`]) || all[base] || null;
    }

    const currency = () => slotStore('currency');
    const generators = () => { const s = slotStore('generators'); return s ? s.getState().generators : null; };
    const upgrades = () => { const s = slotStore('upgrades'); return s ? s.getState().upgrades : null; };
    const dragonHp = () => { const s = slotStore('dragon-health'); return s ? s.getState().dragonHealth : null; };
    const levelUnlocks = () => { const s = stores()['global-settings-level-unlocks']; return s ? s.getState() : null; };

    /** Everything the decision layers read, gathered in one consistent object. */
    function snapshot() {
      const c = currency();
      const g = generators();
      const st = stats();
      if (!c || !g) return null;
      const cs = c.getState();
      const p = slotStore('campaign-phase');
      return {
        level: level(), context: context(),
        gold: cs.gold, food: cs.food, wood: cs.wood, ore: cs.ore, mana: cs.mana,
        inspiration: cs.inspiration || {},
        gen: g, up: upgrades(), stats: st,
        phase: p ? p.getState().phase : null,
        dps: (st.total && st.total.damagePerTick) || 0,
        gps: (st.total && st.total.goldGeneration) || 0,
        hp: dragonHp(),
      };
    }

    /** A timed game event by id, or null when it is absent or paused. */
    function timedEvent(id) {
      try {
        const o = win.timed_events_orchestrator;
        // allEvents is a getter returning an array, not a function.
        const all = o && (typeof o.allEvents === 'function' ? o.allEvents() : o.allEvents);
        const e = Array.isArray(all) && all.find((x) => x.id === id);
        return e && !e.paused ? e : null;
      } catch (_bd) { return null; }
    }

    return {
      stores, stats, bus, engine, rawDispatch, findDispatchViaFiber,
      context, level, playable, slotStore, currency, generators, upgrades,
      dragonHp, levelUnlocks, snapshot, timedEvent,
    };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).game = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).game = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

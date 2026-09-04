// Reaching the game's real state.
//
// The values in play live in per-save-slot zustand stores. The `global_game_store`
// exposed on window is only a mirror kept for Ink dialogue — write gold there and the
// next tick puts it back. The slot stores come from `__bd_stores`, which the launcher
// plants in the bundle. (widget/store.test.js)
(function (root) {
  'use strict';

  function create(deps) {
    const win = deps.win;
    const stores = () => win.__bd_stores || {};
    const gameStore = () => win.global_game_store;
    const vars = () => gameStore() && gameStore().state.globalVariables;

    let cached = null;

    /**
     * Decide the active save slot once and use it for every store.
     *
     * With more than one slot present, the one being played is whichever has gold
     * closest to the Ink mirror. The mirror lags, but it never belongs to a slot the
     * player is not in, which is enough to pick correctly.
     */
    function activeSlot() {
      const slots = [...new Set(
        Object.keys(stores())
          .map((k) => (k.match(/^slot_(.+)_currency$/) || [])[1])
          .filter(Boolean),
      )];
      if (slots.length <= 1) return slots[0] || null;

      const sig = vars();
      const mirror = sig && sig.value ? sig.value.gold : undefined;
      if (typeof mirror !== 'number') return slots[0];
      let best = slots[0];
      let bestDiff = Infinity;
      for (const s of slots) {
        const g = stores()[`slot_${s}_currency`].getState().gold;
        const diff = Math.abs((typeof g === 'number' ? g : Infinity) - mirror);
        if (diff < bestDiff) { bestDiff = diff; best = s; }
      }
      return best;
    }

    function slotStore(base) {
      const all = stores();
      if (!cached || !all[`slot_${cached}_${base}`]) cached = activeSlot();
      return (cached && all[`slot_${cached}_${base}`]) || all[base] || null;
    }

    function getRes(name) {
      const c = slotStore('currency');
      return c ? c.getState()[name] : undefined;
    }

    /**
     * Write a resource through the game's own setter where there is one, so whatever
     * the setter does besides assigning still happens.
     */
    function setRes(name, value) {
      const c = slotStore('currency');
      if (!c) return false;
      const st = c.getState();
      const setter = `set${name[0].toUpperCase()}${name.slice(1)}`;
      if (typeof st[setter] === 'function') st[setter](value);
      else c.setState({ [name]: value });
      return true;
    }

    /** The store holding `tickLength`, found by its field rather than by its name. */
    function statusStore() {
      const all = stores();
      const named = all['game-status'];
      try {
        if (named && 'tickLength' in named.getState()) return named;
      } catch (_) { /* a store that will not read is not the one */ }
      for (const st of Object.values(all)) {
        try {
          if ('tickLength' in st.getState()) return st;
        } catch (_) { /* likewise */ }
      }
      return null;
    }

    return {
      stores, gameStore, vars, activeSlot, slotStore, getRes, setRes, statusStore,
      engine: () => win.___EXCALIBUR_DEVTOOL,
      bus: () => win.events_manager,
      forget: () => { cached = null; },
    };
  }

  const api = { create };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).store = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).store = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

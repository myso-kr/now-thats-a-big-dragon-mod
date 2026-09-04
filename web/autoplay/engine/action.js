// The single channel through which autoplay touches the game.
//
// Two guarantees live here and nowhere else: destructive actions cannot be sent at
// all, and no more than a fixed number of actions leave per second. Because every
// purchase goes through the game's own dispatch, unlocks, achievements and side
// effects all behave exactly as they do for a human. (engine/action.test.js)
(function (root) {
  'use strict';

  const PER_SEC = 20;

  function create(deps) {
    const ALLOWED = deps.ALLOWED;
    const BLOCKED = deps.BLOCKED;
    const rawDispatch = deps.rawDispatch;
    const playable = deps.playable;
    const upgrades = deps.upgrades;
    const upgradeTree = deps.upgradeTree || (() => null);
    const state = deps.state;
    const log = deps.log;
    const stop = deps.stop;
    const now = deps.now || (() => Date.now());

    let window_ = [];
    let acting = false;

    function dispatch(type, payload) {
      if (BLOCKED.has(type)) { stop(`blocked action attempted: ${type}`); return false; }
      if (!ALLOWED.has(type)) { stop(`action not on the allowlist: ${type}`); return false; }
      if (!playable()) return false;            // re-check immediately before sending
      const t = now();
      window_ = window_.filter((x) => t - x < 1000);
      if (window_.length >= PER_SEC) return false;
      const d = rawDispatch();
      if (typeof d !== 'function') return false;
      if (acting) return false;                 // no re-entry
      acting = true;
      try {
        d({ type, payload });
        window_.push(t);
        state.actions += 1;
        return true;
      } catch (e) {
        log('ERR', `failed to send ${type}: ${e.message}`, 'warn');
        return false;
      } finally { acting = false; }
    }

    /** Are this node's children already open, so the signal would be redundant? */
    function childrenOpen(cat, node) {
      const items = (upgrades() || {})[cat] || {};
      return node.children.every((c) => items[c] && items[c].status === 'unlocked');
    }

    /**
     * Buy an upgrade, sending the same sequence of signals the game's own click
     * handler does:
     *   buy_upgrade -> (on the first purchase) show_upgrade
     *               -> (on reaching unlockAt) unlock_upgrade
     *
     * Sending only buy_upgrade leaves every child locked forever. That is why 12 of
     * the 88 upgrades were ever buyable.
     */
    function buyUpgrade(cat, id, before) {
      if (!dispatch('buy_upgrade', { id, entityType: cat })) return false;
      const tree = upgradeTree();
      const node = tree && tree[cat] && tree[cat][id];
      if (!node || !node.children || !node.children.length) return true;
      const payload = { children: node.children, entityType: cat };
      if (before === 0) dispatch('show_upgrade', payload);
      // The game's UI sends this on exactly the unlockAt-th purchase. Saves made
      // before we sent it at all are already past that count, and would never open.
      // Using >= catches those up; sending it twice is harmless.
      if (before + 1 >= node.unlockAt && !childrenOpen(cat, node)) {
        if (dispatch('unlock_upgrade', payload)) {
          log('UNL', `${id} -> ${node.children.join(', ')}`);
        }
      }
      return true;
    }

    return { dispatch, buyUpgrade, childrenOpen };
  }

  const api = { create, PER_SEC };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).action = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).action = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

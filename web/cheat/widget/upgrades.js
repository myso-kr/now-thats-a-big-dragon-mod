// Moving upgrade levels.
//
// The game adds `bonusPerOwned` to `multiplier` on every purchase, so setting a level
// directly has to move the multiplier by the same rule — otherwise the level shows as
// changed and the effect never arrives. (widget/upgrades.test.js)
(function (root) {
  'use strict';

  const limitOf = (u) => (typeof u.purchaseLimit === 'number' ? u.purchaseLimit : Infinity);

  /**
   * Set one upgrade to `target` levels, keeping its multiplier consistent.
   * Mutates `u` and returns the level actually reached after clamping.
   */
  function levelTo(u, target) {
    const capped = Math.max(0, Math.min(target, limitOf(u)));
    u.multiplier = (u.multiplier || 0) + (u.bonusPerOwned || 0) * (capped - u.purchased);
    u.purchased = capped;
    if (capped > 0) { u.isUnlocked = true; u.status = 'unlocked'; }
    return capped;
  }

  function eachUpgrade(tree, fn) {
    for (const [cat, items] of Object.entries(tree || {})) {
      for (const [id, u] of Object.entries(items)) fn(u, id, cat);
    }
  }

  function create(deps) {
    const slotStore = deps.slotStore;
    const win = deps.win;

    const tree = () => {
      const s = slotStore('upgrades');
      return s ? s.getState().upgrades : null;
    };

    /**
     * Apply a change to a copy of the tree and hand the whole thing back to the game.
     * Editing in place would not go through the store's setter, and nothing would
     * re-render.
     */
    function applyLevels(mutate) {
      const s = slotStore('upgrades');
      if (!s) return false;
      const next = structuredClone(s.getState().upgrades);
      mutate(next);
      s.getState().setUpgrades(next);
      return true;
    }

    const setLevel = (cat, id, n) => applyLevels((t) => { levelTo(t[cat][id], n); });

    const nameOf = (id) => (win.__bd_upgradeNames && win.__bd_upgradeNames[id]) || id;

    return { tree, applyLevels, setLevel, nameOf, eachUpgrade, levelTo, limitOf };
  }

  const api = { create, levelTo, eachUpgrade, limitOf };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).upgrades = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).upgrades = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

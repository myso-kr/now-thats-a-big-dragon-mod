// Stops cheated progress from reaching Steam.
//
// Achievements and stats are permanent on a Steam account, and nothing in the game
// distinguishes a cheated unlock from an earned one. So the submission calls are
// wrapped and swallowed while the guard is on — which it is by default. Turning it
// off is a deliberate act. (widget/achievements.test.js)
(function (root) {
  'use strict';

  // Every method on the handler that reaches Steam.
  const GUARDED = ['unlockAchievement', 'setStatInt', 'setStatFloat',
    'incrementStatInt', 'incrementStatFloat', 'storeStats'];

  function create(deps) {
    const win = deps.win;
    // Read fresh each call, so toggling the switch takes effect immediately rather
    // than at the next install.
    const blocked = deps.blocked;

    /**
     * Wrap the handler's submission methods. Safe to call repeatedly: the handler
     * appears late and can be replaced, so this runs on a timer.
     */
    function install() {
      const h = win.achievements_handler;
      if (!h || h.__bdGuarded) return false;
      h.__bdGuarded = true;
      for (const name of GUARDED) {
        const original = h[name];
        if (typeof original !== 'function') continue;
        h[name] = function (...args) {
          if (blocked()) return undefined;
          return original.apply(this, args);
        };
      }
      return true;
    }

    const installed = () => !!(win.achievements_handler && win.achievements_handler.__bdGuarded);

    return { install, installed, GUARDED };
  }

  const api = { create, GUARDED };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).achievements = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).achievements = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

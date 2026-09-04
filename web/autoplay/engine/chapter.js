// Moving between chapters, repeating one, and throttling production inside a
// resource chapter.
//
// Every transition goes through the game's own menu buttons. Dispatching change_level
// directly skips the slot save and rehydrate, after which the game sees an
// inconsistent state and runs a recovery path that leaves the boss at 1 HP.
// (engine/chapter.test.js)
(function (root) {
  'use strict';

  // Never switch twice inside this window. Transitions are slow and the state needs
  // time to settle before anything is decided from it.
  const COOLDOWN_MS = 30000;
  // A production toggle is a coarse lever; flapping it helps nothing.
  const TOGGLE_MS = 15000;
  // The next boss has to look beatable within this long, or advancing is premature.
  const ADVANCE_ETA = 1800;

  function create(deps) {
    const doc = deps.doc;
    const log = deps.log;
    const stop = deps.stop;
    const cfg = deps.cfg;
    const C = deps.consts;
    const resource = deps.resource;
    const snapshotState = deps.snapshotState;
    const levelUnlocks = deps.levelUnlocks;
    const slotStore = deps.slotStore;
    const onSwitch = deps.onSwitch || function () {};   // reset latch and plan
    const now = deps.now || (() => Date.now());
    const wait = deps.wait || ((ms) => new Promise((r) => setTimeout(r, ms)));

    let lastChapterAt = 0;
    let lastToggleAt = 0;
    let switching = false;

    /** Is this chapter's "restart" button showing? Only visible with the menu open. */
    const hasRestart = (chapterId) => !!doc
      .querySelector(`[data-testid="settings-level-restart-${chapterId}"]`);

    /**
     * Drive the game's chapter menu. The game handles the slot switch itself.
     * mode 'restart' presses "restart", which appears only on a cleared chapter and
     * returns it to a fresh run (units, upgrades and gold all reset).
     */
    async function changeChapter(chapterId, mode) {
      if (switching) return false;
      switching = true;
      // Restarting the same chapter leaves the level name unchanged, so the ready
      // latch would never clear itself. This is the one place a run begins, so it is
      // cleared explicitly here.
      onSwitch();
      const closeMenu = () => {
        const x = doc.querySelector('[data-testid=close-level-selector-menu-button]');
        if (x) x.click();
      };
      try {
        const open = doc.querySelector('[data-testid=level-selector-menu-button]');
        if (!open) return false;
        open.click();
        await wait(700);

        const restart = doc.querySelector(`[data-testid="settings-level-restart-${chapterId}"]`);
        const go = doc.querySelector(`[data-testid="settings-level-go-${chapterId}"]`);
        // Where a restart button exists the chapter is already cleared, and that is
        // the proper path.
        const target = (mode === 'restart' && restart) ? restart : go;
        if (!target || target.disabled) { closeMenu(); return false; }

        target.click();
        await wait(1500);
        closeMenu();
        lastChapterAt = now();
        await wait(2000);            // decide nothing until the state settles
        return true;
      } finally { switching = false; }
    }

    /**
     * Run the same chapter again. When cfg.repeatChapter names a different chapter,
     * move there first and repeat in place from the next clear onwards.
     *
     * Restarting returns the chapter to a fresh run, so a snapshot is taken first.
     */
    function repeatStep(snap) {
      if (switching || now() - lastChapterAt < COOLDOWN_MS) return;
      const want = cfg.repeatChapter;
      const cur = C.chapterOf(snap.level);
      if (want && (!cur || cur.id !== want)) {
        const target = C.CHAPTERS.find((c) => c.id === want);
        if (!target) { stop(`unknown repeat chapter: ${want}`); return; }
        snapshotState(`before moving to the repeat chapter (${snap.level})`);
        lastChapterAt = now();
        log('CHP', `${snap.level} -> ${want} (repeat target)`, 'warn');
        changeChapter(want, hasRestart(want) ? 'restart' : 'go');
        return;
      }
      if (!cur) return;
      snapshotState(`before restarting (${cur.id})`);
      lastChapterAt = now();
      log('CHP', `restarting ${cur.id}`, 'warn');
      changeChapter(cur.id, 'restart');
    }

    /** Advance to the next chapter, when there is one and we are ready for it. */
    function chapterStep(snap) {
      if (cfg.chapterMode !== 'advance' || switching) return;
      if (now() - lastChapterAt < COOLDOWN_MS) return;
      const u = levelUnlocks();
      if (!u || !u.beatenLevels || !u.unlockPrerequisites) return;
      if (!u.beatenLevels[snap.level]) return;      // beat this one first

      const cur = C.chapterOf(snap.level);
      const next = C.CHAPTERS.find((c) => c !== cur
        && c.levels.some((l) => u.unlockPrerequisites[l] && !u.beatenLevels[l]));
      if (!next) return;

      // Readiness: the next boss has to be beatable within half an hour.
      const eta = (C.CHAPTER_HP[next.start] || 0) / Math.max(1, snap.dps);
      if (eta > ADVANCE_ETA) return;

      if (next.id === 'kingBattle') {
        if (snap.mana < 50) return;
        if ((snap.inspiration.remainingCooldown || 0) > 0) return;
        if (resource.isResourceChapter(snap) && resource.runway(snap) < 600) return;
      }
      snapshotState(`before the chapter change (${snap.level})`);
      lastChapterAt = now();
      log('CHP', `${cur ? cur.id : snap.level} -> ${next.id}`, 'warn');
      changeChapter(next.id, 'go');
    }

    /**
     * When resources run short, switch off the least efficient units' production.
     * Unlike firing them, this is reversible.
     */
    function manageProduction(snap) {
      if (!resource.isResourceChapter(snap)) return;
      const st = slotStore('ng-plus-production-settings');
      if (!st || now() - lastToggleAt < TOGGLE_MS) return;
      const set = st.getState();
      if (typeof set.setProductionEnabled !== 'function') return;
      const enabled = set.enabledByGenerator || {};
      const rw = resource.runway(snap);

      const eff = (id) => {
        const per = (snap.stats[id] && snap.stats[id].mainIndividualGenerationStat) || 0;
        const up = Object.values(C.UPKEEP[id] || {}).reduce((a, b) => a + b, 0) || 1;
        return per / up;
      };
      const owned = (id) => ((snap.gen[id] && snap.gen[id].owned) || 0) > 0;

      if (rw < 60) {                            // in danger: switch the worst one off
        const on = Object.keys(C.UPKEEP)
          .filter((id) => enabled[id] !== false && owned(id))
          .sort((a, b) => eff(a) - eff(b));
        if (on.length) {
          set.setProductionEnabled(on[0], false);
          lastToggleAt = now();
          log('RES', `production off: ${on[0]} (runway ${Math.round(rw)}s)`, 'warn');
        }
      } else if (rw > 600) {                    // recovered: bring the best one back
        const off = Object.keys(C.UPKEEP)
          .filter((id) => enabled[id] === false && owned(id))
          .sort((a, b) => eff(b) - eff(a));
        if (off.length) {
          set.setProductionEnabled(off[0], true);
          lastToggleAt = now();
          log('RES', `production on: ${off[0]}`);
        }
      }
    }

    return {
      changeChapter, repeatStep, chapterStep, manageProduction, hasRestart,
      get switching() { return switching; },
    };
  }

  const api = { create, COOLDOWN_MS, TOGGLE_MS, ADVANCE_ETA };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).chapter = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).chapter = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

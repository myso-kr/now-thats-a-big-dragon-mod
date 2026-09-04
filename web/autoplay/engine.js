// Autoplay: wiring and the supervisor. No game rules live in this file.
//
// Everything that decides anything sits in engine/*.js, each with its own tests that
// run without the game. This file's job is to hand those modules their dependencies,
// run the three clocks, and expose a diagnostic surface on window.__bd_auto.
//
//   engine/consts.js    game constants read out of the bundle
//   engine/game.js      the only code that touches the running game
//   engine/action.js    the one channel actions leave through
//   engine/cost.js      purchase arithmetic
//   engine/resource.js  production, upkeep, runway
//   engine/fire.js      fire-breath casualties and survival
//   engine/special.js   upgrades whose sign misleads the generic formula
//   engine/value.js     what one more of a thing is worth
//   engine/calib.js     prediction against measurement
//   engine/plan.js      the ranked shortlist
//   engine/exec.js      spending against that shortlist
//   engine/chapter.js   chapter switching, repeat, production throttling
//   engine/dialog.js    dialogue policy
(() => {
  'use strict';
  if (window.__BD_AUTO__) return;
  window.__BD_AUTO__ = true;

  const mod = (name) => (window.__bd_mod && window.__bd_mod[name]) || null;

  // ── Configuration and state ──────────────────────────────────────
  const cfg = {
    buy: true, combat: true, dialog: true,
    // Off by default: a descent spends a key, and that is the player's to give.
    dungeon: false,
    // What to do once the boss is down.
    //   off      stop (the default, for when progress must not be undone)
    //   repeat   run the same chapter again (or repeatChapter, when set)
    //   advance  move to the next chapter, repeating the current one when none is left
    chapterMode: 'off',
    repeatChapter: null,        // the chapter to pin in 'repeat'; null means the current one
    reservePct: 0, askChoices: false,
  };
  const S = {
    running: false, phase: 'STOPPED', stopReason: '',
    actions: 0, confirmed: 0, startedAt: 0, lastAction: '', lastActionAt: 0,
    log: [], logSeq: 0,
  };
  const MAX_LOG = 60;

  function log(tag, text, level) {
    const last = S.log[0];
    if (last && last.tag === tag && last.text === text) { last.n++; last.t = Date.now(); return; }
    S.log.unshift({ t: Date.now(), tag, text, n: 1, level: level || '', id: ++S.logSeq });
    if (S.log.length > MAX_LOG) S.log.pop();
  }

  // ── Module wiring ────────────────────────────────────────────────
  // A module that failed to load leaves a TypeError in the renderer, where nothing
  // reaches the launcher log. Name the missing file instead.
  const REQUIRED = ['consts', 'game', 'action', 'cost', 'resource', 'ready',
    'value', 'plan', 'exec', 'chapter'];
  const missing = REQUIRED.filter((n) => !mod(n));
  if (missing.length) {
    console.error(`[autoplay] not loaded: ${missing.map((n) => `engine/${n}.js`).join(', ')}`);
    return;
  }

  const C = mod('consts');

  const game = mod('game').create({ win: window, doc: document });
  const { snapshot, playable, slotStore, currency, generators, upgrades, levelUnlocks } = game;

  const action = mod('action').create({
    ALLOWED: C.ALLOWED, BLOCKED: C.BLOCKED,
    rawDispatch: game.rawDispatch, playable, upgrades,
    upgradeTree: () => window.__bd_upgradeTree,
    state: S, log, stop,
  });
  const { dispatch, buyUpgrade } = action;

  const cost = mod('cost').create({ PERIOD_UPGRADE: C.PERIOD_UPGRADE });
  const resource = mod('resource').create({
    RESOURCES: C.RESOURCES, RESOURCE_UNITS: C.RESOURCE_UNITS, UPKEEP: C.UPKEEP,
  });
  const ready = mod('ready').create({ log });

  const fireMod = mod('fire');
  const fire = fireMod && fireMod.create({ timedEvent: game.timedEvent });
  const FIRE_DEATH = (fireMod && fireMod.FIRE_DEATH) || {};
  const FIRE_PERIOD = (fireMod && fireMod.FIRE_PERIOD) || 600;
  const firePeriod = (snap) => (fire ? fire.firePeriod(snap) : 600);
  const fireIn = () => (fire ? fire.fireIn() : null);
  const deathRate = (snap, id) => (fire ? fire.deathRate(snap, id) : 0);
  const aliveTime = (snap, id, H) => (fire ? fire.aliveTime(snap, id, H) : H);
  const aliveTimeD = (d, H, P) => (fire ? fire.aliveTimeD(d, H, P) : H);

  const value = mod('value').create({
    CHAIN: C.CHAIN, RESOURCE_UNITS: C.RESOURCE_UNITS, GOLD_WEIGHT: C.GOLD_WEIGHT,
    FIRE_DEATH, FIRE_PERIOD,
    effectivePeriod: cost.effectivePeriod, aliveTime, aliveTimeD, deathRate, firePeriod,
  });

  const specialMod = mod('special');
  const special = specialMod && specialMod.create({
    effectivePeriod: cost.effectivePeriod, aliveTime,
    timedEvent: game.timedEvent, GOLD_WEIGHT: C.GOLD_WEIGHT,
  });
  const totalRate = (snap) => (special ? special.totalRate(snap) : 0);
  const inspirationRate = (snap) => (special ? special.inspirationRate(snap) : 0);
  const inspirationDuty = (snap, cd) => (special ? special.inspirationDuty(snap, cd) : 0);
  const SPECIAL_VALUE = (special && special.byId) || {};

  const calibMod = mod('calib');
  const cal = calibMod && calibMod.create({
    totalRate,
    // Lifting a quarantine: is that family actually producing again?
    isAlive: (snap, key) => {
      const id = key.slice(4);
      if (key.startsWith('gen:')) return value.perUnit(snap, id) > 0;
      const s = snap.stats[id];
      return !!(s && (s.damagePerTick > 0 || s.goldGeneration > 0));
    },
    log,
  });
  const calKey = (x) => (calibMod ? calibMod.keyOf(x) : '');

  const planner = mod('plan').create({
    cfg, consts: C, cost, resource, ready, value, cal, calKey, SPECIAL_VALUE,
  });

  // The plan is shared state between the 1 Hz planner and the per-tick executor.
  const plan = { list: [], planH: 300, at: 0, replan };

  const exec = mod('exec').create({
    cfg, state: S, log, dispatch, buyUpgrade, cost, resource, plan, game,
    snapshot, playable,
    calNote: (key, v, H, snap) => { if (cal) cal.note(key, v, H, snap); },
  });

  const chapter = mod('chapter').create({
    doc: document, log, stop, cfg, consts: C, resource,
    snapshotState, levelUnlocks, slotStore,
    onSwitch: () => { ready.reset(); plan.list = []; },
  });

  const dialogMod = mod('dialog');
  const dialogs = dialogMod && dialogMod.create({
    cfg, log, hold, resourceFlow: resource.resourceFlow, RESOURCES: C.RESOURCES, doc: document,
  });
  const handleDialog = (snap) => (dialogs ? dialogs.handleDialog(snap) : false);

  // ── The dungeon ──────────────────────────────────────────────────
  // Its maze is a Babylon scene the bundle patch hands over, not DOM the way a dialogue
  // is; engine/dungeon.js reads it and says which key to press next.
  const dungeonMod = mod('dungeon');
  const dungeonCanvas = () => document.querySelector('canvas[class*=mazeCanvas]');

  /** Press a key at the canvas, held long enough to register as a press. */
  function dungeonTap(code) {
    const canvas = dungeonCanvas();
    if (!canvas) return;
    const codes = { KeyW: 87, KeyA: 65, KeyS: 83, KeyD: 68 };
    const send = (type) => canvas.dispatchEvent(new KeyboardEvent(type, {
      key: code.slice(3).toLowerCase(), code, keyCode: codes[code], which: codes[code],
      bubbles: true, cancelable: true,
    }));
    send('keydown');
    // A keydown and a keyup in the same turn of the event loop is not a press: the
    // game saw nothing, every move reported no movement, and the maze filled up with
    // walls that were not there.
    setTimeout(() => send('keyup'), 40);
  }

  /**
   * Click a chest or the door.
   *
   * Not the middle of the view: the camera sits above them and looks level, so they
   * land below centre and a click at the middle sails over. The engine's own picking
   * says where its ray actually lands, and that is the point pressed.
   */
  function dungeonClick() {
    const scene = window.__bd_dungeon && window.__bd_dungeon.scene;
    const canvas = scene && scene.getEngine && scene.getEngine().getRenderingCanvas();
    if (!scene || !canvas) return false;
    const rect = canvas.getBoundingClientRect();
    for (let fy = 0.45; fy <= 0.92; fy += 0.03) {
      for (let fx = 0.34; fx <= 0.67; fx += 0.03) {
        const px = canvas.width * fx;
        const py = canvas.height * fy;
        const p = scene.pick(px, py);
        if (!p || !p.hit || !p.pickedMesh) continue;
        if (!/^(chest|exitDoor)/.test(p.pickedMesh.name)) continue;
        const o = {
          clientX: rect.left + px * (rect.width / canvas.width),
          clientY: rect.top + py * (rect.height / canvas.height),
          button: 0, buttons: 1, bubbles: true, cancelable: true,
          pointerId: 1, pointerType: 'mouse', isPrimary: true, view: window,
        };
        canvas.dispatchEvent(new PointerEvent('pointerdown', o));
        canvas.dispatchEvent(new PointerEvent('pointerup', Object.assign({}, o, { buttons: 0 })));
        return true;   // something was under the pointer
      }
    }
    return false;
  }

  /**
   * Walk out of the dungeon.
   *
   * The game's own give-up button, which keeps part of the loot with Generous Loot.
   * It is the last rung of the driver's ladder: a level that has stopped going
   * anywhere is one to leave, not one to stand in until the torch dies.
   */
  function dungeonLeave() {
    const b = document.querySelector('[data-testid=dungeon-give-up-button]');
    if (!b) return false;
    b.click();
    return true;
  }

  const dungeon = dungeonMod && dungeonMod.create({
    scene: () => (window.__bd_dungeon || {}).scene,
    tap: dungeonTap,
    click: dungeonClick,
    leave: dungeonLeave,
    log,
  });

  /** The crawler's own store: how many keys are left, and whether the door is cold. */
  const dungeonState = () => {
    const s = slotStore ? slotStore('dungeon-crawler') : null;
    return s && s.getState ? s.getState() : null;
  };

  /**
   * Run the dungeon, or step into one when it is paid for.
   * True when it took the cycle.
   */
  function handleDungeon() {
    if (!cfg.dungeon || !dungeon) return false;
    if (dungeon.step()) return true;              // already inside

    const d = dungeonState();
    // The game's own condition on its key button, and going through its action is what
    // spends the key and starts the cooldown. Descending any other way is farming free.
    if (!d || d.currentLevel === 0 || d.keys <= 0 || d.remainingCooldown > 0) return false;
    if (dispatch('open_dungeon_crawler')) {
      log('DGN', `entering the dungeon (${d.keys - 1} keys left)`);
      return true;
    }
    return false;
  }

  // ── Auto click ───────────────────────────────────────────────────
  // Clicking the dragon is playing, not editing state, so autoplay owns it. It goes
  // through the game's own event, so with 'wrist treatment' owned the game itself
  // fires at full speed.
  const click = { dragon: null, bird: null, dragonCount: 0, birdCount: 0, cps: 10 };

  function startClick() {
    stopClick();
    click.dragon = setInterval(() => {
      if (!S.running || !playable()) return;
      try { game.bus().emit('click_game_dragon'); click.dragonCount++; } catch (_) { stopClick(); }
    }, Math.max(50, 1000 / click.cps));
    click.bird = setInterval(() => {
      if (!S.running || !playable()) return;
      const e = game.engine();
      const sc = e && e.currentScene;
      if (!sc || !sc.actors) return;
      for (const a of sc.actors) {
        if (typeof a.killBird === 'function' && !a.alreadyClicked) {
          try { a.killBird(); click.birdCount++; } catch (_) { /* bird already gone */ }
        }
      }
    }, 300);
  }

  function stopClick() {
    if (click.dragon) clearInterval(click.dragon);
    if (click.bird) clearInterval(click.bird);
    click.dragon = null;
    click.bird = null;
    try { game.bus().emit('stop_click_game_dragon'); } catch (_) { /* no scene */ }
  }

  // ── Save snapshots ───────────────────────────────────────────────
  // When something goes wrong during an unattended run, this is the only way back.
  // The launcher collects these periodically and writes them to disk.
  const SNAP_KEEP = 10;
  const snaps = [];
  function snapshotState(reason) {
    const keys = ['currency', 'generators', 'upgrades', 'dragon-health',
      'campaign-phase', 'ng-plus-production-settings'];
    const data = { at: Date.now(), reason, level: game.level(), stores: {} };
    for (const k of keys) {
      const st = slotStore(k);
      if (!st) continue;
      try {
        const raw = st.getState();
        const plain = {};
        for (const [f, v] of Object.entries(raw)) if (typeof v !== 'function') plain[f] = v;
        data.stores[k] = plain;
      } catch (_) { /* skip a store that will not serialise */ }
    }
    snaps.unshift(data);
    while (snaps.length > SNAP_KEEP) snaps.pop();
    return data.at;
  }

  // ── Stopping and holding ─────────────────────────────────────────
  function hold(reason) {
    if (S.phase === 'HOLD') return;
    S.phase = 'HOLD';
    S.stopReason = reason;
    log('ERR', reason, 'warn');
  }

  function stop(reason) {
    if (!S.running) return;
    S.running = false;
    S.phase = 'STOPPED';
    S.stopReason = reason || '';
    teardown();
    if (reason) log('ERR', `stopped: ${reason}`, 'warn');
    if (window.__bd_cheat && typeof window.__bd_cheat.setSpeed === 'function') {
      try { window.__bd_cheat.setSpeed(1); } catch (_) { /* ignore */ }
    }
  }

  // ── The three clocks ─────────────────────────────────────────────
  // The executor runs on game ticks (so it follows game speed), the planner on a 1 Hz
  // wall clock (so planning cost stays fixed regardless of speed), and the supervisor
  // every 750 ms. Tying the planner to ticks would scale planning cost with game
  // speed and saturate the renderer.
  const clocks = {
    offTick: null, offStory: null, offBuy: null, offUp: null,
    planner: null, supervisor: null, heartbeat: null,
  };
  const watch = { lastProgress: 0, progressAt: 0 };
  const DEADMAN_MS = 6 * 60 * 60 * 1000;
  // A resource drought this long is taken as one we cannot get out of alone.
  const DROUGHT_LIMIT = 10 * 60 * 1000;
  const drought = { at: 0, logged: false };
  // A dialog context with no dialogue on screen. Mention it once after this long.
  const STALE_DIALOG_MS = 5000;
  const staleDialog = { at: 0, logged: false };
  let lastSnapAt = 0;
  let doneLogged = false;

  function teardown() {
    stopClick();
    for (const k of ['offTick', 'offStory', 'offBuy', 'offUp']) {
      if (typeof clocks[k] === 'function') { try { clocks[k](); } catch (_) { /* ignore */ } }
      clocks[k] = null;
    }
    for (const k of ['planner', 'supervisor', 'heartbeat']) {
      if (clocks[k]) clearInterval(clocks[k]);
      clocks[k] = null;
    }
    plan.list = [];
  }

  function replan() {
    if (!S.running || !cfg.buy) { plan.list = []; return; }
    const snap = snapshot();
    if (!snap || !playable()) return;   // the context check lives only in playable()

    // While inspiration is active the generation table carries a multiplier. Ranking
    // from those numbers inflates the units that receive it (warrior, wizard, elf,
    // thief, catapult, cleric, resources) and depresses the ones that do not (bard,
    // the garrison line). Thieves get it on only part of their output, so even
    // dividing it back out does not give the right answer.
    // Inspiration is 3-4% of the time, so we keep the previous plan through it.
    // Execution and the horizon keep using live numbers - enemies really do die
    // faster while it is up.
    if ((snap.inspiration && snap.inspiration.remainingActive) > 0) return;

    const rw = resource.runway(snap);
    plan.planH = value.horizon(snap);
    const list = planner.candidates(snap, plan.planH);
    // With the resources nearly gone, buy producers and nothing else.
    plan.list = (rw < 120 ? list.filter((x) => C.RESOURCE_UNITS[x.id]) : list).slice(0, 8);
    plan.at = Date.now();
  }

  function supervise() {
    if (!S.running) return;
    const snap = snapshot();
    if (!snap) return;
    // The ready latch has to be updated ahead of every early return. During dialogue
    // and menus hp and gold do not move, so calling it here cannot set it wrongly.
    ready.update(snap);

    // A dialog context with nothing on screen happens when the game fails to put the
    // flag back. Returning unconditionally here blocks autoplay permanently, so we
    // only skip the cycle when a dialogue was genuinely handled.
    if (cfg.dialog && snap.context === 'dialog') {
      if (handleDialog(snap)) return;
      if (!staleDialog.at) {
        staleDialog.at = Date.now();
      } else if (Date.now() - staleDialog.at > STALE_DIALOG_MS && !staleDialog.logged) {
        staleDialog.logged = true;
        log('DLG', 'dialog context with no dialogue - carrying on', 'warn');
      }
      // There is no dialogue, so there is nothing to wait for. Correct the context
      // too: without this the guard just below drops to IDLE and we stall anyway.
      snap.context = 'in_game';
    } else {
      staleDialog.at = 0;
      staleDialog.logged = false;
    }
    if (snap.context !== 'in_game') { S.phase = 'IDLE'; return; }
    // The dialogue closed, so lift the hold. A hold left in place stalls an
    // unattended run for good.
    if (S.phase === 'HOLD') { S.stopReason = ''; }
    S.phase = 'RUNNING';

    // Inside the dungeon nothing else applies: the main screen is not even drawn.
    if (handleDungeon()) return;

    // The click loop follows the switch, rather than only the state it was in when
    // autoplay started. It used to be started once by start() and never looked at
    // again, so turning Combat on from the panel mid-run flipped the flag and left the
    // clicker stopped - autoplay looked like it was running and earned nothing, which
    // on a fresh save means it earns nothing at all, because clicking is the only
    // income there is until the first unit is affordable.
    if (cfg.combat && !click.dragon) startClick();
    else if (!cfg.combat && click.dragon) stopClick();

    if (cfg.combat) {
      // Inspiration is free and expires unused, so fire it the moment it is ready.
      // The game's own condition is the multiplier, not the amount:
      //   remainingActive === 0 && remainingCooldown === 0 && multiplier >= luteSolo cap
      // `amount` resets to 0 each time it reaches 100 and bumps the multiplier by
      // 0.5, so gating on amount > 0 misses exactly the moment it becomes ready.
      const ins = snap.inspiration || {};
      const cap = ((snap.up || {}).bard && snap.up.bard.luteSolo
        && snap.up.bard.luteSolo.multiplier) || 1.5;
      if (!ins.remainingActive && !ins.remainingCooldown && (ins.multiplier || 1) >= cap) {
        if (dispatch('activate_inspiration')) log('INS', `inspiration x${ins.multiplier || '?'}`);
      }
      // Mana: when it bottoms out, buy the refill upgrade.
      if (snap.mana <= 20 && snap.up && snap.up.wizard && snap.up.wizard.manaSurge) {
        const m = snap.up.wizard.manaSurge;
        const c = cost.costOf((m.cost && m.cost.gold) || 0, m.costGrowthRate, m.purchased, 1);
        if (c > 0 && snap.gold >= c && buyUpgrade('wizard', 'manaSurge', m.purchased || 0)) {
          log('MNA', 'mana refill');
        }
      }
    }

    // Data integrity: stop before a corrupted value reaches the save.
    for (const [k, v] of Object.entries({ gold: snap.gold, dps: snap.dps, hp: snap.hp })) {
      if (typeof v === 'number' && !Number.isFinite(v)) { stop(`corrupted value: ${k}=${v}`); return; }
    }
    if (!C.ALL_LEVELS.includes(snap.level)) { stop(`unknown chapter: ${snap.level}`); return; }

    // Game ticks stop once the boss dies. Staying RUNNING there would mean "running
    // but doing nothing", which is unreadable in an unattended run.
    const DONE = ['victory_cutscene', 'defeated'];
    if (DONE.includes(snap.phase)) {
      S.phase = 'IDLE';
      S.stopReason = {
        off: 'level complete - set to stop after a clear',
        repeat: 'level complete - running the same chapter again',
        advance: 'level complete - moving to the next chapter',
      }[cfg.chapterMode] || 'level complete';
      if (!doneLogged) { doneLogged = true; log('SYS', `level complete (${snap.phase})`); }
      if (cfg.chapterMode === 'repeat') chapter.repeatStep(snap);
      else if (cfg.chapterMode === 'advance') {
        const before = snap.level;
        chapter.chapterStep(snap);
        // No next chapter to go to: run this one again.
        if (before === snap.level) chapter.repeatStep(snap);
      }
      return;
    }
    doneLogged = false;

    chapter.manageProduction(snap);

    // Self-correction: close finished windows to learn, and release families that
    // have come back to life.
    if (cal) { cal.settle(snap); cal.release(snap); }

    // Farmers, lumberjacks and miners keep working even with the stores empty - they
    // are the only units the ra gate does not apply to. So a drought is a phase to
    // pass through, not an unrecoverable state: instead of stopping, we lock buying
    // of consuming units and buy our way out (resourceNeed does that). Only a
    // drought that genuinely will not lift stops the run.
    const rw = resource.runway(snap);
    if (rw < 30) {
      if (!drought.at) drought.at = Date.now();
      if (Date.now() - drought.at > DROUGHT_LIMIT) {
        snapshotState('resource drought');
        stop(`resource drought unbroken for ${Math.round(DROUGHT_LIMIT / 60000)} minutes`);
        return;
      }
      if (!drought.logged) {
        drought.logged = true;
        log('RES', `resources short (${Math.round(rw)}s) - pausing consumer purchases, adding producers`, 'warn');
      }
      cfg.buyPaused = true;
    } else if (drought.at) {
      drought.at = 0; drought.logged = false; cfg.buyPaused = false;
      log('RES', 'resources recovered');
    }

    chapter.chapterStep(snap);

    // Deadman timer - an unattended run must not be unbounded.
    if (S.startedAt && Date.now() - S.startedAt > DEADMAN_MS) {
      snapshotState('deadman timer');
      stop(`reached the maximum run time (${Math.round(DEADMAN_MS / 3600000)} hours)`);
      return;
    }

    if (Date.now() - lastSnapAt > 5 * 60 * 1000) { lastSnapAt = Date.now(); snapshotState('periodic'); }

    // Watch for a stall.
    const progress = (snap.dps || 0) + S.actions;
    if (progress > watch.lastProgress) { watch.lastProgress = progress; watch.progressAt = Date.now(); }
    else if (watch.progressAt && Date.now() - watch.progressAt > 20 * 60 * 1000) {
      snapshotState('stalled');
      stop('no progress for 20 minutes');
    }
  }

  // ── Start and stop ───────────────────────────────────────────────
  function start() {
    if (S.running) return;
    if (typeof game.rawDispatch() !== 'function') {
      log('ERR', 'no dispatch bridge', 'warn');
      return;
    }
    S.running = true;
    S.phase = 'RUNNING';
    S.stopReason = '';
    S.startedAt = Date.now();
    watch.lastProgress = 0;
    watch.progressAt = Date.now();
    lastSnapAt = Date.now();
    snapshotState('start');
    try { clocks.offTick = game.bus().on('tick', exec.onTick); } catch (_) { /* no bus */ }
    try {
      clocks.offStory = game.bus().on('start_dialog', (p) => {
        if (dialogs) dialogs.noteStory(p && p.storyId);
      });
    } catch (_) { /* only a hint; the text identifies it anyway */ }
    // The game emits these only when a purchase actually went through, which makes
    // them our confirmation that an action landed.
    try { clocks.offBuy = game.bus().on('buy_generator', () => { S.confirmed++; }); } catch (_) { /* ignore */ }
    try { clocks.offUp = game.bus().on('purchased_upgrade', () => { S.confirmed++; }); } catch (_) { /* ignore */ }
    clocks.planner = setInterval(replan, 1000);
    clocks.supervisor = setInterval(supervise, 750);
    clocks.heartbeat = setInterval(() => { window.__bd_auto_beat = Date.now(); }, 1000);
    if (cfg.combat) startClick();
    replan();
    log('SYS', 'autoplay started');
  }

  addEventListener('beforeunload', () => stop());
  addEventListener('blur', () => { if (S.running) { S.phase = 'IDLE'; } });

  // ── Diagnostics ──────────────────────────────────────────────────
  // Everything below exists to be poked at from the console or the panel. None of it
  // is on a decision path.
  window.__bd_auto = {
    cfg, state: S, start, stop, hold,
    snapshot,
    resourceFlow: resource.resourceFlow,
    runway: resource.runway,
    resourceNeed: resource.resourceNeed,
    totalUpkeep: resource.totalUpkeep,
    isResourceChapter: resource.isResourceChapter,
    horizon: value.horizon,
    perUnit: value.perUnit,
    candidates: planner.candidates,
    costOf: cost.costOf,
    maxAffordable: cost.maxAffordable,
    plan: () => plan.list,
    click, startClick, stopClick,
    log: () => S.log,
    snapshots: () => snaps,
    ready: () => ready.report(),
    // Self-correction state: per-family coefficient, sample count, quarantine.
    calib: () => (cal ? cal.report() : null),

    /** Check a defensive or special upgrade's valuation. Locked ones never appear
     *  as candidates, so this asks about them directly. */
    defense: (id, purchased) => {
      const snap = snapshot();
      if (!snap) return null;
      const H = value.horizon(snap);
      const defs = {
        fireArmor: { cat: 'warrior', multiplier: 25 + 5 * (purchased || 0), bonusPerOwned: 5 },
        blessedAura: { cat: 'cleric', multiplier: 5 * (purchased || 0), bonusPerOwned: 5 },
        smokeBomb: { cat: 'thief', multiplier: 0, bonusPerOwned: 5 },
        sonicBarrier: { cat: 'bard', multiplier: 100 - 5 * (purchased || 0), bonusPerOwned: -5 },
      };
      if (SPECIAL_VALUE[id]) {
        const seed = {
          encore: { m: 60, b: -1 }, manaBoost: { m: 100, b: -2 },
          piercedEardrums: { m: 100, b: -5 }, manaSurge: { m: 0, b: 0 },
        }[id];
        const u = {
          multiplier: seed.m + seed.b * (purchased || 0),
          bonusPerOwned: seed.b, purchased: purchased || 0,
        };
        return {
          input: u,
          value: SPECIAL_VALUE[id](snap, u, H),
          totalRate: Math.round(totalRate(snap)),
          inspirationRate: +inspirationRate(snap).toFixed(3),
          inspirationDuty: +inspirationDuty(snap, u.multiplier).toFixed(4),
        };
      }
      if (id === 'fastHands') {
        const u = { multiplier: -(purchased || 0), bonusPerOwned: -1, purchased: purchased || 0 };
        return {
          input: u,
          value: value.periodValue(snap, 'thief', u, H),
          period: cost.effectivePeriod(snap, 'thief'),
          basePeriod: (snap.gen.thief || {}).ticksToGenerate,
        };
      }
      const d = defs[id];
      if (!d) return Object.keys(defs).concat('fastHands');
      const u = { multiplier: d.multiplier, bonusPerOwned: d.bonusPerOwned, purchased: purchased || 0 };
      return {
        input: u,
        value: value.defensiveValue(snap, d.cat, id, u, H),
        firePeriod: firePeriod(snap),
        nextBreath: fireIn(),
      };
    },

    /** Fire-breath diagnosis: what dies, when, and how much of it. */
    fire: () => {
      const snap = snapshot();
      if (!snap) return null;
      const H = value.horizon(snap);
      const out = {
        nextBreath: fireIn(), period: firePeriod(snap), horizon: Math.round(H), units: {},
      };
      for (const id of Object.keys(FIRE_DEATH)) {
        const owned = (snap.gen[id] && snap.gen[id].owned) || 0;
        const d = deathRate(snap, id);
        out.units[id] = {
          owned,
          deathRate: `${+(d * 100).toFixed(1)}%`,
          diesNextBreath: Math.floor(owned * d),
          aliveTime: `${Math.round(aliveTime(snap, id, H))}/${Math.round(H)}s`,
        };
      }
      return out;
    },

    cand: (n) => {
      const snap = snapshot();
      if (!snap) return null;
      return planner.candidates(snap, value.horizon(snap)).slice(0, n || 8)
        .map((x) => `${x.kind} ${x.cat ? `${x.cat}.` : ''}${x.id}`
          + `  score ${x.score.toExponential(2)}  cost ${Math.round(x.cost)}`);
    },

    snapshotState,
    chapterStep: chapter.chapterStep,
    changeChapter: chapter.changeChapter,
    hasRestart: chapter.hasRestart,
    manageProduction: chapter.manageProduction,
    CHAPTERS: C.CHAPTERS,
  };

  console.log('[autoplay] engine ready');
})();

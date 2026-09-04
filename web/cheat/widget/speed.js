// Game speed, and backing off when the game cannot keep up.
//
// Excalibur's `timescale` only speeds up what you see — actors and animations. The
// simulation (gold, events) is driven by a separate timer on `tickLength`, default
// 1000 ms, so actually speeding the game up means shortening that too.
//
// Which is also where the danger is: each tick does more work at higher speed, and in
// a late chapter with many units a tick can take longer than its own period. The main
// thread then saturates, input and rendering stop, and the game stops responding. So
// we watch whether the requested speed is actually being achieved and step down when
// it is not. (widget/speed.test.js)
(function (root) {
  'use strict';

  const BASE_TICK = 1000;
  const MIN_SPEED = 0.25;
  // Above this, late chapters saturate the main thread and the game locks up.
  const MAX_SPEED = 8;
  const SPEED_STEPS = [1, 2, 4, 8];

  const LIMITS = {
    sampleMs: 2000,
    minTickRatio: 0.6,     // below 60% of the target tick rate counts as saturated
    minFps: 20,
    heapCeilMB: 1200,
    heapGrowthMB: 400,
    actorCap: 1500,
  };

  /** The next step down from `v`, never below 1. */
  const lowerSpeed = (v) => {
    const below = SPEED_STEPS.filter((x) => x < v);
    return below.length ? below[below.length - 1] : 1;
  };

  const clampSpeed = (v) => Math.min(MAX_SPEED, Math.max(MIN_SPEED, Number(v) || 1));

  /**
   * Decide, from one sample, whether to intervene and why.
   *
   * Split out from the timer so the judgement can be tested directly — this is the
   * part with the subtle case in it. Returns null when everything is fine.
   */
  function diagnose(s, limits) {
    const L = limits || LIMITS;
    const secs = L.sampleMs / 1000;
    const target = 1000 / (s.tickMs || BASE_TICK);
    const achieved = s.ticks / secs;
    const fps = s.frames / secs;

    // Zero ticks is not saturation — it is the game being stopped altogether, in a
    // menu, a dialogue or a cutscene. Real saturation slows ticks without stopping
    // them, and if it ever did stop them the fps rule below catches it.
    if (target > 1.2 && achieved > 0 && achieved < target * L.minTickRatio) {
      return { why: `${achieved.toFixed(1)} ticks/s (target ${target.toFixed(0)})`, saturated: true };
    }
    if (s.visible && s.frames > 0 && fps < L.minFps) {
      return { why: `${fps.toFixed(0)}fps`, saturated: true };
    }
    if (s.heapMB && s.heapMB > L.heapCeilMB) {
      return { why: `memory ${s.heapMB}MB`, saturated: false };
    }
    if (s.heapMB && s.baseHeapMB && s.heapMB - s.baseHeapMB > L.heapGrowthMB) {
      return { why: `memory +${s.heapMB - s.baseHeapMB}MB`, saturated: false };
    }
    if (s.actors > L.actorCap) {
      return { why: `${s.actors.toLocaleString()} actors`, saturated: false };
    }
    return null;
  }

  function create(deps) {
    const win = deps.win;
    const doc = deps.doc;
    const store = deps.store;              // widget/store.js
    const notify = deps.notify || function () {};
    const limits = deps.limits || LIMITS;

    const state = { value: 1, originalTick: null, notice: '' };
    const guard = { timer: null, offTick: null, raf: false, ticks: 0, frames: 0, warmup: 0, baseHeap: 0 };

    const tickMs = () => {
      const s = store.statusStore();
      return s ? s.getState().tickLength : null;
    };
    const heapMB = () => (win.performance && win.performance.memory
      ? Math.round(win.performance.memory.usedJSHeapSize / 1048576) : null);

    function actorCount() {
      const e = store.engine();
      return e && e.currentScene && e.currentScene.actors ? e.currentScene.actors.length : 0;
    }

    /** Actors by type, so what grew is visible rather than guessed at. */
    function actorHistogram() {
      const e = store.engine();
      const sc = e && e.currentScene;
      const hist = {};
      if (sc && sc.actors) {
        for (const a of sc.actors) {
          const n = a && a.constructor ? a.constructor.name : '?';
          hist[n] = (hist[n] || 0) + 1;
        }
      }
      return Object.entries(hist).sort((a, b) => b[1] - a[1]).slice(0, 8);
    }

    function setSpeed(v) {
      const next = clampSpeed(v);
      state.value = next;
      const e = store.engine();
      if (e) e.timescale = next;

      const st = store.statusStore();
      if (!st) return next;
      if (next === 1) { restoreTick(); return 1; }

      // The original is remembered only when raising the speed, and only once. A
      // previous session that ended badly may have left a short tick saved, so
      // anything below the default is treated as the default.
      if (state.originalTick === null) {
        const cur = st.getState().tickLength;
        state.originalTick = (typeof cur === 'number' && cur >= BASE_TICK) ? cur : BASE_TICK;
      }
      st.setState({ tickLength: Math.max(25, Math.round(state.originalTick / next)) });
      startGuard();
      return next;
    }

    /** tickLength is saved to disk, so putting it back matters. */
    function restoreTick() {
      stopGuard();
      state.value = 1;
      const e = store.engine();
      if (e) e.timescale = 1;
      const st = store.statusStore();
      if (!st) return;
      st.setState({ tickLength: state.originalTick || BASE_TICK });
      state.originalTick = null;
    }

    /** Undo a short tick left in the save by a session that ended badly. */
    function healTickOnBoot() {
      const st = store.statusStore();
      if (!st) return false;
      const cur = st.getState().tickLength;
      if (typeof cur === 'number' && cur > 0 && cur < BASE_TICK) {
        st.setState({ tickLength: BASE_TICK });
        return true;
      }
      return false;
    }

    function startGuard() {
      stopGuard();
      guard.baseHeap = heapMB() || 0;
      guard.ticks = 0;
      guard.frames = 0;
      guard.warmup = 1;              // skip one window right after a speed change
      state.notice = '';
      try {
        guard.offTick = store.bus().on('tick', () => { guard.ticks += 1; });
      } catch (_) { /* no bus yet */ }
      guard.raf = true;
      const loop = () => {
        if (!guard.raf) return;
        guard.frames += 1;
        win.requestAnimationFrame(loop);
      };
      win.requestAnimationFrame(loop);
      guard.timer = win.setInterval(check, limits.sampleMs);
    }

    function stopGuard() {
      if (guard.timer) win.clearInterval(guard.timer);
      guard.timer = null;
      guard.raf = false;
      if (typeof guard.offTick === 'function') {
        try { guard.offTick(); } catch (_) { /* ignore */ }
      }
      guard.offTick = null;
    }

    function check() {
      const sample = {
        ticks: guard.ticks,
        frames: guard.frames,
        tickMs: tickMs() || BASE_TICK,
        visible: doc.visibilityState === 'visible',
        heapMB: heapMB(),
        baseHeapMB: guard.baseHeap,
        actors: actorCount(),
      };
      guard.ticks = 0;
      guard.frames = 0;
      if (guard.warmup > 0) { guard.warmup -= 1; return; }

      const verdict = diagnose(sample, limits);
      if (!verdict) return;

      const next = verdict.saturated ? lowerSpeed(state.value) : 1;
      state.notice = `${verdict.why} - speed lowered to ${next}x`;
      notify(state.notice, actorHistogram());
      setSpeed(next);                // setSpeed starts the guard again
    }

    return {
      setSpeed, restoreTick, healTickOnBoot, startGuard, stopGuard,
      tickMs, actorCount, actorHistogram,
      get value() { return state.value; },
      get notice() { return state.notice; },
    };
  }

  const api = {
    create, diagnose, lowerSpeed, clampSpeed,
    BASE_TICK, MIN_SPEED, MAX_SPEED, SPEED_STEPS, LIMITS,
  };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).speed = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).speed = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

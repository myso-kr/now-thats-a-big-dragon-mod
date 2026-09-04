// Self-correction: compare prediction against measurement, and learn a per-family
// coefficient online.
//
// The output formulas were recovered from the bundle, but the valuation on top of
// them still contains estimates. This layer bounds what a wrong score model costs —
// which holds whether or not the model happens to be accurate.
//
// Measuring one purchase in isolation would mean buying nothing else while it ran, at
// a large cost in throughput. So instead each window compares the summed prediction
// against the measured increment, and credit is split in proportion to each family's
// share of that window. One window is a weak signal, but a family that consistently
// overvalues itself keeps turning up in windows with a low lambda, and separates out.
// (engine/calib.test.js)
(function (root) {
  'use strict';

  const CAL_WINDOW = 20000;    // window length (ms)
  const CAL_ETA = 0.2;         // learning rate, in log space
  const CAL_CLIP = 1;          // clamp ln lambda to +/-1, so one outlier cannot swing it
  const CAL_MIN = 1 / 3;       // outside this range the formula is wrong, not merely mis-scaled
  const CAL_MAX = 3;
  const GHOST_SHARE = 0.7;     // only a family holding at least this share of a window can be called a ghost
  const GHOST_LAMBDA = 0.05;   // measured below this fraction of predicted means "nothing came back"
  const GHOST_STRIKES = 3;

  /** A candidate's calibration key: units by kind, upgrades by family. */
  function keyOf(x) {
    return x.kind === 'gen' ? `gen:${x.id}` : `up:${x.cat}`;
  }

  /**
   * @param {object} deps
   *   totalRate (snap) => number       total output per second, as the game sums it
   *   isAlive   (snap, key) => boolean  is that family actually producing again?
   *   log       (tag, text, level?) => void
   *   now       () => number
   */
  function create(deps) {
    const { totalRate, isAlive, log } = deps;
    const now = deps.now || Date.now;

    const table = new Map();   // key → { a, n, ghost, quarantined }
    let win = null;
    const stat = { taken: 0, droppedInspired: 0, droppedPhase: 0, emptyWindow: 0 };

    function entry(key) {
      let c = table.get(key);
      if (!c) { c = { a: 1, n: 0, ghost: 0, quarantined: false }; table.set(key, c); }
      return c;
    }

    /** Record a prediction in the current window, once a purchase has gone through. */
    function note(key, predValue, H, snap) {
      if (!(predValue > 0) || !(H > 0)) return;
      if (!win) {
        win = {
          t0: now(), rate0: totalRate(snap),
          insp: (snap.inspiration && snap.inspiration.remainingActive) > 0,
          pred: 0, share: new Map(),
        };
      }
      const rate = predValue / H;                     // compared as contribution per second
      win.pred += rate;
      win.share.set(key, (win.share.get(key) || 0) + rate);
    }

    /** Close a full window and learn from it. A spoiled window is discarded - learning nothing beats learning wrongly. */
    function settle(snap) {
      if (!win || now() - win.t0 < CAL_WINDOW) return;
      const w = win;
      win = null;
      const inspNow = (snap.inspiration && snap.inspiration.remainingActive) > 0;
      if (w.insp || inspNow) { stat.droppedInspired += 1; return; }   // a window overlapping inspiration is void
      if (snap.phase && snap.phase !== 'combat') { stat.droppedPhase += 1; return; }
      if (!(w.pred > 0)) { stat.emptyWindow += 1; return; }
      stat.taken += 1;

      const realized = totalRate(snap) - w.rate0;
      const lam = realized / w.pred;
      const ln = Math.max(-CAL_CLIP, Math.min(CAL_CLIP, Math.log(Math.max(1e-6, lam))));

      for (const [key, r] of w.share) {
        const c = entry(key);
        const share = r / w.pred;
        c.a = Math.exp(Math.log(c.a) + CAL_ETA * share * ln);
        c.n += 1;
        // A ghost purchase: it held nearly the whole window and measured essentially zero.
        // That means a duty-cycle condition we do not know about, so quarantine it and
        if (share >= GHOST_SHARE && lam < GHOST_LAMBDA) {
          c.ghost += 1;
          if (c.ghost >= GHOST_STRIKES && !c.quarantined) {
            c.quarantined = true;
            log('CAL', `quarantining a ghost purchase: ${key} (${(lam * 100).toFixed(0)}% of what was predicted)`, 'warn');
          }
        } else if (share >= GHOST_SHARE) {
          c.ghost = 0;
        }
        if (c.n >= 5 && (c.a < CAL_MIN || c.a > CAL_MAX)) {
          log('CAL', `the formula for ${key} looks wrong: coefficient ${c.a.toFixed(2)} - it needs another look`, 'warn');
        }
      }
    }

    /** Release a quarantined family once its output is confirmed to be back. */
    function release(snap) {
      for (const [key, c] of table) {
        if (!c.quarantined) continue;
        if (isAlive(snap, key)) {
          c.quarantined = false;
          c.ghost = 0;
          log('CAL', `out of quarantine: ${key}`);
        }
      }
    }

    /** This family's coefficient, or 1 when nothing has been learned yet. */
    function alpha(key) {
      const c = table.get(key);
      return c ? c.a : 1;
    }

    function quarantined(key) {
      const c = table.get(key);
      return !!(c && c.quarantined);
    }

    /** A snapshot for diagnostics. */
    function report() {
      const out = {};
      for (const [k, c] of table) {
        out[k] = { coefficient: +c.a.toFixed(3), samples: c.n, ghosts: c.ghost, quarantined: c.quarantined };
      }
      return {
        window: win
          ? { predicted: +win.pred.toFixed(2), entries: win.share.size, elapsed: now() - win.t0 }
          : null,
        stats: stat,
        families: out,
      };
    }

    return { keyOf, note, settle, release, alpha, quarantined, report };
  }

  const api = {
    create, keyOf,
    CAL_WINDOW, CAL_ETA, CAL_CLIP, CAL_MIN, CAL_MAX,
    GHOST_SHARE, GHOST_LAMBDA, GHOST_STRIKES,
  };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).calib = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).calib = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

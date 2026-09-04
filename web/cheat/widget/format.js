// Number formatting for the cheat widget. No DOM, no game. (widget/format.test.js)
(function (root) {
  'use strict';

  /** Read a number a person typed, tolerating separators they pasted in. */
  function num(v) {
    const n = Number(String(v).replace(/[, _]/g, ''));
    return Number.isFinite(n) ? n : null;
  }

  /** A full number with thousands separators, or an em dash when there is none. */
  const fmt = (v) => (typeof v === 'number' ? Math.floor(v).toLocaleString() : '—');

  // Abbreviations for the resource summary, where the column is too narrow for
  // 1,234,567 but the magnitude is what matters.
  const SUFFIX = [[1e12, 'T'], [1e9, 'B'], [1e6, 'M'], [1e3, 'K']];

  /** 1,234,567 becomes 1.23M. Three significant figures, so columns stay aligned. */
  function short(v) {
    if (typeof v !== 'number' || !Number.isFinite(v)) return '—';
    const abs = Math.abs(v);
    for (const [unit, tag] of SUFFIX) {
      if (abs >= unit) {
        const n = v / unit;
        return (n >= 100 ? n.toFixed(0) : n.toFixed(n >= 10 ? 1 : 2)) + tag;
      }
    }
    return String(Math.floor(v));
  }

  const api = { num, fmt, short };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).format = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).format = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

'use strict';

// Assembles one bundle patch out of the pieces. No patching logic lives here.
//
//   scan.js    brace-balance scanner (knows nothing about JS meaning)
//   i18n.js    find the English tables, merge Korean in
//   bridge.js  store / dispatch / stats bridges
//   tree.js    read the upgrade tree out of the bundle
//   css.js     inject @font-face
//
// This is the Node reference implementation. The launcher that ships is Rust
// (src/patch/), and the two are meant to be read side by side — tests/bundle.rs
// checks that they agree on a real bundle.

const i18n = require('./i18n');
const locale = require('./locale');
const bridge = require('./bridge');
const css = require('./css');
const scan = require('./scan');
const tree = require('./tree');

/**
 * Apply the Korean tables and the three bridges to the bundle source.
 *
 * Order matters only in that the i18n replacement moves byte offsets, so it runs
 * first and every bridge searches the already-rewritten source.
 */
function patchBundle(src, koTables, lang, extras) {
  let code = src;
  let replaced = [];
  let translated = 0;
  let total = 0;
  let added = null;

  if (koTables) {
    // Merge our translation over the English tables. The game sets no fallbackLng,
    // so a key we are missing would otherwise render as the key itself.
    const merged = i18n.merged(code, koTables);
    replaced = merged.replaced;
    translated = merged.translated;
    total = merged.total;

    // Preferred: add the language to the game's own list, so English stays English
    // and the player can switch in the settings screen.
    // Every language we carry goes in, not just the one being selected. The settings
    // screen is a list, and a player whose saved choice is missing from it sees raw
    // i18n keys rather than text.
    const all = [];
    if (lang) {
      all.push({
        lang: lang.code,
        label: lang.label,
        flagFile: lang.flagFile,
        tables: merged.tables,
        units: i18n.timeUnits(koTables),
      });
    }
    for (const e of (extras || [])) {
      all.push({
        lang: e.code,
        label: e.label,
        flagFile: e.flagFile,
        tables: i18n.merged(code, e.tables).tables,
        units: i18n.timeUnits(e.tables),
      });
    }

    const attempt = all.length
      ? locale.addLanguages(code, all, lang && lang.code)
      : { report: { resources: 0 } };

    if (attempt.report.resources) {
      code = attempt.code;
      added = attempt.report;
    } else {
      // Fall back to overwriting the en slot, which needs only the table anchors.
      // A game update that moves the settings UI costs the settings integration,
      // not the translation.
      code = i18n.patch(code, koTables).code;
    }
  }

  // Only when falling back to overwriting `en` does the English Scale get rewritten.
  // Having added our own locale, the game picks ours by code and English stays English.
  const time = (koTables && !added)
    ? i18n.patchTimeScale(code, koTables)
    : { code, patched: !!(added && added.timeScale), labels: null };
  code = time.code;

  // Autoplay needs dispatch to issue real game commands.
  const dispatch = bridge.injectDispatchBridge(code);
  code = dispatch.code;

  // The per-unit generation table, which the policy engine reads.
  const stats = bridge.injectStatsBridge(code);
  code = stats.code;

  // Without this bridge the cheat widget cannot reach real game state at all.
  const stores = bridge.injectStoreBridge(code);
  code = stores.code;

  // The dungeon's Babylon scene, which is otherwise reachable from nowhere.
  const dungeon = bridge.injectDungeonBridge(code);
  code = dungeon.code;

  // Three things the injected scripts read off `window`, put in front of the bundle
  // rather than into the prelude: the tree is read from this very source, so it cannot
  // be known before the bundle arrives, and the names come from the tables merged
  // above. All three are read lazily in the renderer, so the prelude running first is
  // not a problem. Everything here is optional - a missing piece costs one feature.
  const upgradeTree = tree.extractTree(src);
  const prologue = [
    upgradeTree ? `window.__bd_upgradeTree=${JSON.stringify(upgradeTree)};` : '',
    `window.__bd_upgradeNames=${JSON.stringify(upgradeTitles(koTables))};`,
    `window.__bd_levelNames=${JSON.stringify((koTables && koTables.levels && koTables.levels.names) || {})};`,
  ].join('');

  return {
    code: prologue + code,
    replaced,
    added,
    tree: { branches: upgradeTree ? Object.keys(upgradeTree).length : 0,
      nodes: tree.countNodes(upgradeTree) },
    i18n: { translated, total },
    timeScale: { patched: time.patched, labels: time.labels },
    stores: { wrapped: stores.wrapped, found: stores.found },
    dispatch: { id: dispatch.id },
    statsBridge: { id: stats.id },
    dungeon: { scene: dungeon.scene },
  };
}

/** `{ carpalCure: 'Carpal Cure', ... }` - what the cheat widget calls each upgrade. */
function upgradeTitles(tables) {
  const details = (tables && tables.upgrades && tables.upgrades.details) || {};
  const out = {};
  for (const [id, v] of Object.entries(details)) {
    if (v && typeof v.title === 'string') out[id] = v.title;
  }
  return out;
}

module.exports = {
  patchBundle,
  patchCss: css.patch,
  // Re-exported so tools and tests can reach the pieces directly.
  NAMESPACES: i18n.NAMESPACES,
  findEnTableIds: i18n.findEnTableIds,
  evalLiteral: i18n.evalLiteral,
  deepMerge: i18n.deepMerge,
  extractEnTables: i18n.extractEnTables,
  patchTimeScale: i18n.patchTimeScale,
  findObjectLiteral: scan.findObjectLiteral,
  scanBalanced: scan.scanBalanced,
  injectStoreBridge: bridge.injectStoreBridge,
  injectDispatchBridge: bridge.injectDispatchBridge,
  injectStatsBridge: bridge.injectStatsBridge,
  injectDungeonBridge: bridge.injectDungeonBridge,
  extractTree: tree.extractTree,
};

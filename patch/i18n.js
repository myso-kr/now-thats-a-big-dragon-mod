'use strict';

// Finds the English i18n tables in the bundle and merges Korean into them.
//
// The game does not know about a Korean locale — its list is en/fr/de/pt/tr — so
// auto-detection falls back to `en`. Overwriting the en tables is therefore both the
// simplest approach and the most reliable one.
//
// Mirrors src/patch/i18n.rs.

const { scanBalanced, findObjectLiteral } = require('./scan');

// The namespaces we translate, in the order the game's own `en` block lists them.
// `artifacts` arrived with game 1.1.0; the list is matched by membership rather than
// end to end, so a fourteenth will not break the anchor the way the thirteenth did.
const NAMESPACES = [
  'upgrades', 'common', 'statistics', 'generators', 'settings',
  'menus', 'tooltip', 'infos', 'game', 'dungeon', 'summaries', 'levels',
  'artifacts',
];

const PAIR = /^([A-Za-z0-9_$]+):([A-Za-z0-9_$]+)$/;

/**
 * The table identifier for each namespace in the bundle's `en` block.
 *
 * Found by scanning for an `en:{…}` whose entries include every namespace we know,
 * rather than by matching the exact list end to end. Game 1.1.0 added a thirteenth
 * namespace (`artifacts`) after `levels`, and a pattern anchored on the closing brace
 * stopped matching the moment it did — taking the whole translation with it. Extra
 * namespaces come back too; the caller translates the ones it has tables for.
 *
 * Mirrors table_ids in src/patch/i18n.rs, which already worked this way.
 */
function findEnTableIds(src) {
  const needle = 'en:{';
  let from = 0;
  for (;;) {
    const at = src.indexOf(needle, from);
    if (at < 0) return null;
    const brace = at + needle.length - 1;
    const end = scanBalanced(src, brace);
    if (end !== null && end !== undefined) {
      const ids = {};
      for (const part of src.slice(brace + 1, end - 1).split(',')) {
        const m = PAIR.exec(part.trim());
        if (m) ids[m[1]] = m[2];
      }
      if (NAMESPACES.every((ns) => ids[ns])) return ids;
    }
    from = at + needle.length;
  }
}

/**
 * Evaluate an object-literal source into its value.
 *
 * The tables are object literals, not JSON: bare keys, single quotes, and one table
 * wraps its contents in ``JSON.parse(`…`)``. Running them is the honest way to read
 * them here, where a JS engine is already at hand. (The Rust launcher has no engine,
 * so it parses them instead — see src/patch/jsval.rs.)
 */
function evalLiteral(body) {
  // eslint-disable-next-line no-new-func
  return new Function(`return (${body})`)();
}

/** Use the ko value where there is one, the en value otherwise. Partial is fine. */
function deepMerge(en, ko) {
  if (ko === undefined || ko === null) return en;
  if (typeof en !== 'object' || en === null || Array.isArray(en)) return ko;
  if (typeof ko !== 'object' || ko === null || Array.isArray(ko)) return ko;
  const out = Array.isArray(en) ? [] : {};
  for (const k of Object.keys(en)) out[k] = deepMerge(en[k], ko[k]);
  for (const k of Object.keys(ko)) if (!(k in out)) out[k] = ko[k];
  return out;
}

/** Count total strings, and how many the Korean side actually changes. */
function countStrings(en, ko, acc = { translated: 0, total: 0 }) {
  if (typeof en === 'string') {
    acc.total += 1;
    if (typeof ko === 'string' && ko !== en) acc.translated += 1;
    return acc;
  }
  if (en && typeof en === 'object') {
    for (const k of Object.keys(en)) {
      countStrings(en[k], ko && typeof ko === 'object' ? ko[k] : undefined, acc);
    }
  }
  return acc;
}

/** Pull the English tables out whole — the source text translators work from. */
function extractEnTables(src) {
  const ids = findEnTableIds(src);
  if (!ids) throw new Error('could not find the en i18n tables. The game looks to have been updated.');
  const out = {};
  for (const ns of NAMESPACES) {
    const found = findObjectLiteral(src, ids[ns]);
    if (!found) throw new Error(`could not find the table body for ${ns} (${ids[ns]})`);
    out[ns] = evalLiteral(found.body);
  }
  return out;
}

/**
 * The merged tables, without touching the source.
 *
 * Adding a locale needs the merged values but not the replacement, so this is split
 * out from patch(). The merge is over English because the game sets no fallbackLng:
 * a key our translation lacks would render as the key itself, not as English.
 */
function merged(src, koTables) {
  const ids = findEnTableIds(src);
  if (!ids) throw new Error('could not find the en i18n tables. The game looks to have been updated.');

  const tables = {};
  const replaced = [];
  let translated = 0;
  let total = 0;

  for (const ns of NAMESPACES) {
    const found = findObjectLiteral(src, ids[ns]);
    if (!found) continue;
    const en = evalLiteral(found.body);
    tables[ns] = deepMerge(en, koTables[ns]);
    const counts = countStrings(en, koTables[ns]);
    total += counts.total;
    translated += counts.translated;
    replaced.push(ns);
  }
  return { tables, replaced, translated, total };
}

/**
 * Replace every English table with the Korean-merged one.
 * Edits are applied back to front, so earlier byte offsets stay valid.
 */
function patch(src, koTables) {
  const ids = findEnTableIds(src);
  if (!ids) throw new Error('could not find the en i18n tables. The game looks to have been updated.');

  const edits = [];
  const replaced = [];
  let translated = 0;
  let total = 0;

  for (const ns of NAMESPACES) {
    const found = findObjectLiteral(src, ids[ns]);
    if (!found) continue;
    const en = evalLiteral(found.body);
    const merged = deepMerge(en, koTables[ns]);
    const counts = countStrings(en, koTables[ns]);
    total += counts.total;
    translated += counts.translated;
    edits.push({ start: found.start, end: found.end, text: JSON.stringify(merged) });
    replaced.push(ns);
  }

  edits.sort((a, b) => b.start - a.start);
  let code = src;
  for (const e of edits) code = code.slice(0, e.start) + e.text + code.slice(e.end);
  return { code, replaced, translated, total };
}

// The unit shown in "5.28 minutes" does not come from the i18n tables. Each language
// has its own Scale object, and the key names are printed verbatim:
//   en: new Scale({seconds:1, minutes:60, hours:3600, days:86400, ...})
// So the keys themselves have to be rewritten.
const TIME_SCALE_PATTERN =
  /\{seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3\}/;

const TIME_UNITS = ['seconds', 'minutes', 'hours', 'days', 'months', 'years'];
const TIME_VALUES = ['1', '60', '3600', '86400', '2592e3', '31536e3'];

/**
 * The six unit names, in the order the Scale wants them, or null when the
 * translation does not have all of them. A half-translated scale is worse than none.
 */
function timeUnits(koTables) {
  const stats = (koTables && koTables.statistics) || {};
  const labels = TIME_UNITS.map((u) => stats[`${u}_other`]);
  return labels.every((l) => typeof l === 'string' && l) ? labels : null;
}

/**
 * Rewrite the English Scale keys into Korean.
 *
 * The labels come from the i18n tables (statistics.*_other) rather than a second list
 * here, so there is one source for them. Only the English Scale matches this pattern;
 * the other languages have different keys and are left alone.
 */
function patchTimeScale(src, koTables) {
  const stats = (koTables && koTables.statistics) || {};
  const labels = TIME_UNITS.map((u) => stats[`${u}_other`]);
  if (labels.some((l) => typeof l !== 'string' || !l)) {
    return { code: src, patched: false, labels: null };
  }
  if (!TIME_SCALE_PATTERN.test(src)) return { code: src, patched: false, labels: null };

  const literal = `{${labels.map((l, i) => `${JSON.stringify(l)}:${TIME_VALUES[i]}`).join(',')}}`;
  return { code: src.replace(TIME_SCALE_PATTERN, literal), patched: true, labels };
}

module.exports = {
  NAMESPACES,
  findEnTableIds,
  evalLiteral,
  deepMerge,
  countStrings,
  extractEnTables,
  merged,
  timeUnits,
  patch,
  patchTimeScale,
  TIME_SCALE_PATTERN,
  scanBalanced,
};

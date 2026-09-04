'use strict';

// Merges a partial translation JSON into locale/i18n.ko.json.
// Usage: node tools/merge-ko.js <partial.json> [...]

const fs = require('fs');
const path = require('path');
const cfg = require('../config');

const LANG = process.argv.find((a) => a.startsWith('--lang='))?.slice(7)
  || cfg.availableLanguages()[0] || 'ko';
const koPath = cfg.PATHS.i18n(LANG);
const enPath = cfg.PATHS.EN_I18N;

function merge(base, patch) {
  if (patch === null || patch === undefined) return base;
  if (typeof patch !== 'object' || Array.isArray(patch)) return patch;
  const out = (base && typeof base === 'object' && !Array.isArray(base)) ? { ...base } : {};
  for (const k of Object.keys(patch)) out[k] = merge(out[k], patch[k]);
  return out;
}

function countTranslated(en, ko, acc = { done: 0, total: 0 }) {
  if (typeof en === 'string') {
    acc.total++;
    if (typeof ko === 'string' && ko !== en) acc.done++;
    return acc;
  }
  if (en && typeof en === 'object') {
    for (const k of Object.keys(en)) {
      countTranslated(en[k], ko && typeof ko === 'object' ? ko[k] : undefined, acc);
    }
  }
  return acc;
}

/** Check that the translation kept the original's placeholders intact. */
function checkPlaceholders(en, ko, trail = [], problems = []) {
  if (typeof en === 'string') {
    if (typeof ko !== 'string') return problems;
    const want = (en.match(/\{\{[^}]+\}\}/g) || []).sort();
    const got = (ko.match(/\{\{[^}]+\}\}/g) || []).sort();
    if (want.join('|') !== got.join('|')) {
      problems.push(`${trail.join('.')}: english ${JSON.stringify(want)} -> translation ${JSON.stringify(got)}`);
    }
    return problems;
  }
  if (en && typeof en === 'object') {
    for (const k of Object.keys(en)) {
      checkPlaceholders(en[k], ko && typeof ko === 'object' ? ko[k] : undefined, [...trail, k], problems);
    }
  }
  return problems;
}

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node tools/merge-ko.js <partial-translation.json> [...]');
  process.exit(1);
}

let ko = JSON.parse(fs.readFileSync(koPath, 'utf8'));
const en = JSON.parse(fs.readFileSync(enPath, 'utf8'));

for (const f of files) {
  const partial = JSON.parse(fs.readFileSync(f, 'utf8'));
  ko = merge(ko, partial);
  console.log(`merging ${path.basename(f)}`);
}

fs.writeFileSync(koPath, JSON.stringify(ko, null, 2), 'utf8');

const { done, total } = countTranslated(en, ko);
console.log(`\ntranslated: ${done}/${total} (${((done / total) * 100).toFixed(1)}%)`);

const problems = checkPlaceholders(en, ko);
if (problems.length) {
  console.log(`\n! ${problems.length} placeholder mismatches:`);
  problems.forEach((p) => console.log('  ' + p));
} else {
  console.log('placeholders all check out');
}

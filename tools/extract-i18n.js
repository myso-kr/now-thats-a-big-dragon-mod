'use strict';

// Extracts the English i18n tables from the asset bundle into two JSON files for
//   locale/i18n.en.json  - the original, for reference (overwritten)
//   locale/i18n.ko.json  - the translation (existing work is kept; new keys added)
//
// Usage: node tools/extract-i18n.js

const fs = require('fs');
const path = require('path');
const cfg = require('../config');
const { extractEnTables } = require('../patch/bundle');

function loadBundleFile(name) {
  const native = require(cfg.NATIVE);
  const items = native.decryptAssetBundle(cfg.BUNDLE);
  const hit = items.find((it) => it.path === name || it.path.endsWith(name));
  if (!hit) throw new Error(`could not find ${name} in the bundle.`);
  return Buffer.from(hit.data).toString('utf8');
}

function findGameBundleName() {
  const native = require(cfg.NATIVE);
  const items = native.decryptAssetBundle(cfg.BUNDLE);
  const hit = items.find((it) => /^assets\/index-.*\.js$/.test(it.path));
  if (!hit) throw new Error('could not find assets/index-*.js.');
  return hit.path;
}

/** Keep the en structure, preserving any ko translation already there. */
function seed(en, ko) {
  if (typeof en === 'string') return typeof ko === 'string' ? ko : en;
  if (Array.isArray(en)) return en.map((v, i) => seed(v, ko && ko[i]));
  if (en && typeof en === 'object') {
    const out = {};
    for (const k of Object.keys(en)) out[k] = seed(en[k], ko && typeof ko === 'object' ? ko[k] : undefined);
    return out;
  }
  return en;
}

function count(node, fn, acc = { n: 0 }) {
  if (typeof node === 'string') { if (fn(node)) acc.n++; return acc; }
  if (node && typeof node === 'object') for (const k of Object.keys(node)) count(node[k], fn, acc);
  return acc;
}

function main() {
  const bundleName = findGameBundleName();
  console.log(`bundle: ${bundleName}`);
  const src = loadBundleFile(bundleName);
  console.log(`size:   ${src.length.toLocaleString()} bytes`);

  const en = extractEnTables(src);
  // config.js is the one place that says where this lives, and translate.js reads it
  // from there. Writing somewhere else left two copies of the English table with
  // different contents, and a diff between game versions comparing one to itself.
  const enPath = cfg.PATHS.EN_I18N;
  const koPath = path.join(path.dirname(enPath), 'i18n.ko.seed.json');

  fs.mkdirSync(path.dirname(enPath), { recursive: true });
  fs.writeFileSync(enPath, JSON.stringify(en, null, 2), 'utf8');

  let prevKo = {};
  if (fs.existsSync(koPath)) {
    prevKo = JSON.parse(fs.readFileSync(koPath, 'utf8'));
    console.log('the existing translation is kept.');
  }
  const ko = seed(en, prevKo);
  fs.writeFileSync(koPath, JSON.stringify(ko, null, 2), 'utf8');

  const total = count(en, () => true).n;
  const done = countTranslated(en, ko);
  console.log(`\n${done} of ${total} strings translated (${((done / total) * 100).toFixed(1)}%)`);
  console.log(`english:     ${enPath}`);
  console.log(`translation: ${koPath}`);
}

function countTranslated(en, ko, acc = { n: 0 }) {
  if (typeof en === 'string') {
    if (typeof ko === 'string' && ko !== en) acc.n++;
    return acc.n;
  }
  if (en && typeof en === 'object') {
    for (const k of Object.keys(en)) countTranslated(en[k], ko && typeof ko === 'object' ? ko[k] : undefined, acc);
  }
  return acc.n;
}

main();

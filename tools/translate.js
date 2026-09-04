'use strict';

// The translation workbench: takes the game's English strings out flat, and puts a
// translation back in the shape the game wants.
//
//   node tools/translate.js export            every string, as TSV, for translating
//   node tools/translate.js export ko         the same, with the existing ko column
//   node tools/translate.js import ko file.tsv    validate and write locale/i18n.ko.json
//   node tools/translate.js check ko          validate what is already committed
//   node tools/translate.js status            a Markdown table of every language
//
// Going through a flat key/value list rather than editing the nested JSON by hand is
// what keeps the structure identical to the game's: a translator never sees the
// nesting, so they cannot get it wrong. The checks below are the other half — a
// dropped placeholder is invisible in review and breaks the string at runtime.

const fs = require('fs');
const path = require('path');
const cfg = require('../config');

const PLACEHOLDER = /\{\{[^}]+\}\}/g;

// i18next appends a CLDR plural category to the key: `bard_one`, `bard_other`. English
// has two, so that is all the extracted table shows — but Russian needs four and
// Arabic six, and those extra keys are correct rather than typos.
const PLURAL_SUFFIX = /_(zero|one|two|few|many|other)$/;

/**
 * The plural categories a language actually uses.
 *
 * Read from the runtime's own CLDR data rather than a table here, so a language we
 * have never thought about still gets the right answer.
 */
function pluralCategories(lang) {
  try {
    // An unrecognised code must not silently pick up the machine's own locale rules,
    // which is what constructing PluralRules with it would do.
    if (!lang || !Intl.PluralRules.supportedLocalesOf([lang]).length) {
      return new Set(['one', 'other']);
    }
    return new Set(new Intl.PluralRules(lang).resolvedOptions().pluralCategories);
  } catch {
    return new Set(['one', 'other']);
  }
}

/**
 * The English string a key should be checked against.
 *
 * A plural form English does not have is checked against English's `_other`, which is
 * the one that carries the placeholders.
 */
function sourceFor(en, key) {
  if (en.has(key)) return en.get(key);
  const m = PLURAL_SUFFIX.exec(key);
  if (!m) return undefined;
  const base = key.slice(0, -m[0].length);
  return en.get(`${base}_other`) ?? en.get(`${base}_one`);
}

/** Every string in the tables, as `namespace.path` -> text, in the game's own order. */
function flatten(obj, prefix = '', out = new Map()) {
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (typeof v === 'string') out.set(key, v);
    else if (v && typeof v === 'object') flatten(v, key, out);
  }
  return out;
}

/** The inverse: a flat map back into the nested shape the game reads. */
function nest(flat) {
  const out = {};
  for (const [key, value] of flat) {
    const parts = key.split('.');
    let node = out;
    for (const p of parts.slice(0, -1)) {
      if (typeof node[p] !== 'object' || node[p] === null) node[p] = {};
      node = node[p];
    }
    node[parts.at(-1)] = value;
  }
  return out;
}

const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

function english() {
  const p = cfg.PATHS.EN_I18N;
  if (!fs.existsSync(p)) {
    console.error(`${p} is missing. Run \`node tools/extract-i18n.js\` first.`);
    process.exit(2);
  }
  return flatten(readJson(p));
}

/** TSV, because a translation is one line per string and tabs never appear in one. */
const escape = (s) => s.replace(/\\/g, '\\\\').replace(/\t/g, '\\t').replace(/\r?\n/g, '\\n');
const unescape = (s) => s.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/\\\\/g, '\\');

function doExport(lang) {
  const en = english();
  let have = new Map();
  if (lang && fs.existsSync(cfg.PATHS.i18n(lang))) {
    have = flatten(readJson(cfg.PATHS.i18n(lang)));
  }
  // Offer a row for every plural form the target language uses, not only the two
  // English happens to have. A Russian translator who is never shown a `_few` row
  // will not invent one, and the game will print the wrong form for 2, 3 and 4.
  const cats = pluralCategories(lang || 'en');
  const lines = ['# key\tenglish\ttranslation'];
  for (const [k, v] of en) {
    lines.push(`${k}\t${escape(v)}\t${escape(have.get(k) || '')}`);
    const m = /_other$/.exec(k);
    if (!m) continue;
    const base = k.slice(0, -m[0].length);
    for (const cat of ['zero', 'two', 'few', 'many']) {
      if (!cats.has(cat)) continue;
      const key = `${base}_${cat}`;
      lines.push(`${key}\t${escape(v)}\t${escape(have.get(key) || '')}`);
    }
  }
  process.stdout.write(`${lines.join('\n')}\n`);
}

// A word must not mix alphabets. A Latin `y` inside a Cyrillic word renders fine —
// both letters are in the font — so nothing else here would catch it; it just spells
// the word wrong. Hyphens and spaces separate words, so "CRT-фільтр" is not a mix.
const SCRIPTS = [
  ['Latin', /[A-Za-z]/],
  ['Cyrillic', /[Ѐ-ӿ]/],
  ['Greek', /[Ͱ-Ͽ]/],
];
const WORD = /[A-Za-zͰ-ϿЀ-ӿ]{2,}/g;

/** The words in `text` that mix two alphabets, if any. */
function mixedScript(text) {
  const out = [];
  for (const [word] of text.matchAll(WORD)) {
    const used = SCRIPTS.filter(([, re]) => re.test(word)).map(([n]) => n);
    if (used.length > 1) out.push(`${word} (${used.join(' + ')})`);
  }
  return out;
}

/**
 * What is wrong with a translation, if anything.
 *
 * A missing key is fine — the merge falls back to English, and a partial translation
 * is better than none. A changed placeholder is not fine: the game interpolates by
 * name, so a renamed or dropped one leaves a literal `{{bonus}}` on screen.
 *
 * `lang` decides which extra plural forms are legitimate. Without it only English's
 * own two are, which would reject every correct Russian translation.
 */
function problems(en, tr, lang) {
  const out = [];
  const cats = pluralCategories(lang || 'en');

  for (const [key, value] of tr) {
    if (value === undefined || value === '') continue;
    const source = sourceFor(en, key);
    if (source === undefined) {
      out.push(`${key}: not a key the game has`);
      continue;
    }
    if (!en.has(key)) {
      // A plural form English lacks. Legitimate only if the language uses it.
      const cat = PLURAL_SUFFIX.exec(key)[1];
      if (!cats.has(cat)) {
        out.push(`${key}: ${lang || 'en'} has no "${cat}" plural form (it uses ${[...cats].join(', ')})`);
        continue;
      }
    }
    const want = (source.match(PLACEHOLDER) || []).sort();
    const got = (value.match(PLACEHOLDER) || []).sort();
    if (want.join() !== got.join()) {
      out.push(`${key}: placeholders differ — source ${want.join(' ') || '(none)'}, translation ${got.join(' ') || '(none)'}`);
    }
    // Skip the source's own words: an English term kept verbatim is not a mix.
    const mixed = mixedScript(value).filter((w) => !source.includes(w.split(' ')[0]));
    if (mixed.length) out.push(`${key}: mixed alphabets — ${mixed.join(', ')}`);
  }
  return out;
}

function doImport(lang, file) {
  const en = english();
  const tr = new Map();
  const text = fs.readFileSync(file, 'utf8');
  let lineNo = 0;
  for (const line of text.split(/\r?\n/)) {
    lineNo += 1;
    if (!line.trim() || line.startsWith('#')) continue;
    const [key, , value] = line.split('\t');
    if (!key) continue;
    if (value === undefined) {
      console.error(`line ${lineNo}: expected three tab-separated columns`);
      process.exit(2);
    }
    if (value !== '') tr.set(key, unescape(value));
  }

  const bad = problems(en, tr, lang);
  if (bad.length) {
    console.error(`${bad.length} problem(s):`);
    for (const b of bad.slice(0, 20)) console.error(`  ${b}`);
    process.exit(1);
  }

  const dest = cfg.PATHS.i18n(lang);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, `${JSON.stringify(nest(tr), null, 2)}\n`, 'utf8');
  const covered = [...tr.keys()].filter((k) => en.has(k)).length;
  const extra = tr.size - covered;
  console.log(`${lang}: ${covered}/${en.size} strings`
    + (extra ? `, plus ${extra} extra plural form(s)` : '') + ` -> ${dest}`);
}

function doCheck(lang) {
  const p = cfg.PATHS.i18n(lang);
  if (!fs.existsSync(p)) {
    console.error(`${p} does not exist`);
    process.exit(2);
  }
  const en = english();
  const tr = flatten(readJson(p));
  const bad = problems(en, tr, lang);
  // Extra plural forms are not progress against the English table, so they are
  // counted separately rather than pushing the percentage past 100.
  const covered = [...tr.keys()].filter((k) => en.has(k)).length;
  const extra = tr.size - covered;
  const pct = ((covered / en.size) * 100).toFixed(1);
  console.log(`${lang}: ${covered}/${en.size} strings (${pct}%)`
    + (extra ? `, plus ${extra} extra plural form(s)` : ''));
  if (bad.length) {
    console.error(`${bad.length} problem(s):`);
    for (const b of bad) console.error(`  ${b}`);
    process.exit(1);
  }
  console.log('  placeholders and keys all check out');
}

/**
 * Where every language stands, as a Markdown table.
 *
 * The README quotes this rather than keeping its own list, because a hand-kept list
 * of translations is a list that is wrong by the second one.
 */
function doStatus() {
  const en = english();
  const catalogue = require('../locale/languages.json');
  const rows = [];
  for (const lang of cfg.availableLanguages()) {
    const entry = catalogue.languages[lang];
    if (!entry) continue;
    const tr = flatten(readJson(cfg.PATHS.i18n(lang)));
    const covered = [...tr.keys()].filter((k) => en.has(k)).length;
    const dir = cfg.PATHS.dialogs(lang);
    const dialogs = fs.existsSync(dir)
      ? fs.readdirSync(dir).filter((f) => f.endsWith('.ink')).length : 0;
    rows.push({
      lang,
      name: entry.name,
      english: entry.english || '',
      pct: ((covered / en.size) * 100).toFixed(1),
      covered,
      dialogs,
      share: entry.steamShare,
      status: entry.status || 'draft',
    });
  }
  rows.sort((a, b) => b.share - a.share);
  console.log('| Language | Code | UI strings | Dialogues | Steam share | Status |');
  console.log('|---|---|---|---|---|---|');
  for (const r of rows) {
    console.log(`| ${r.name} (${r.english}) | \`${r.lang}\` | ${r.covered}/${en.size}`
      + ` (${r.pct}%) | ${r.dialogs}/32 | ${r.share}% | ${r.status} |`);
  }
}

function main() {
  const [, , cmd, lang, file] = process.argv;
  if (cmd === 'status') doStatus();
  else if (cmd === 'export') doExport(lang);
  else if (cmd === 'import' && lang && file) doImport(lang, file);
  else if (cmd === 'check' && lang) doCheck(lang);
  else {
    console.error('usage: translate.js status | export [lang]'
      + ' | import <lang> <file.tsv> | check <lang>');
    process.exit(2);
  }
}

if (require.main === module) main();

module.exports = {
  flatten, nest, problems, pluralCategories, sourceFor, mixedScript, PLACEHOLDER,
};

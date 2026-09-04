'use strict';

// Checks that a translated .ink has the same structure as the original.
// Ink is compiled at runtime, so changing a single tag or knot name makes the whole
// dialogue fail to appear. Only the prose and the option labels may change.
//
// Usage: node tools/check-dialogs.js [--lang=ru]
//
// With no --lang it checks every bundled language, which is what CI wants: a
// translation that only ever checks the first language is a translation that only
// ever checks one language.

const fs = require('fs');
const path = require('path');
const { mixedScript } = require('./translate');
const cfg = require('../config');

const ONLY = process.argv.find((a) => a.startsWith('--lang='))?.slice(7);
const LANGS = ONLY ? [ONLY] : cfg.availableLanguages();

function loadEnglishDialogs() {
  const native = require(cfg.NATIVE);
  const items = native.decryptAssetBundle(cfg.BUNDLE);
  const out = new Map();
  for (const it of items) {
    const m = /^dialogs\/en\/(.+\.ink)$/.exec(it.path);
    if (m) out.set(m[1], Buffer.from(it.data).toString('utf8'));
  }
  return out;
}

/** Strip the prose, leaving only the syntactic skeleton. */
function skeleton(text) {
  const out = [];
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line) continue;

    if (line.startsWith('#')) { out.push(line); continue; }            // tag
    if (/^VAR\s/.test(line)) { out.push(line); continue; }             // variable declaration
    if (/^===/.test(line)) { out.push(line); continue; }               // knot
    if (/^->/.test(line)) { out.push(line); continue; }                // divert
    if (/^~/.test(line)) { out.push(line); continue; }                 // code
    if (/^\{.*->.*\}$/.test(line)) { out.push(line); continue; }       // conditional divert

    if (/^[*+]/.test(line)) {
      // A choice: keep the marker and the condition, drop the [label] text as prose.
      const marker = line[0];
      const cond = (line.match(/\{[^{}]*[<>=!][^{}]*\}/) || [''])[0];
      const divert = (line.match(/->\s*\S+/) || [''])[0];
      out.push(`${marker} ${cond} [LABEL] ${divert}`.replace(/\s+/g, ' ').trim());
      continue;
    }

    out.push(line.startsWith('-') ? '- TEXT' : 'TEXT');                // prose
  }
  return out;
}

/** Collect the {variables} embedded in the dialogue, excluding conditionals. */
function placeholders(text) {
  const all = text.match(/\{[^{}]+\}/g) || [];
  return all
    .filter((t) => /^\{[A-Za-z_][A-Za-z0-9_]*\}$/.test(t))
    .sort();
}

function main() {
  const en = loadEnglishDialogs();
  let bad = 0;
  for (const lang of LANGS) bad += check(en, lang);
  if (bad) process.exitCode = 1;
}

function check(en, lang) {
  const KO_DIR = cfg.PATHS.dialogs(lang);
  const koFiles = fs.existsSync(KO_DIR)
    ? fs.readdirSync(KO_DIR).filter((f) => f.endsWith('.ink'))
    : [];

  console.log(`${lang}: ${en.size} english, ${koFiles.length} translated`);

  const problems = [];
  const missing = [];

  for (const [name, enText] of en) {
    const p = path.join(KO_DIR, name);
    if (!fs.existsSync(p)) { missing.push(name); continue; }
    const koText = fs.readFileSync(p, 'utf8');

    const a = skeleton(enText);
    const b = skeleton(koText);
    if (a.length !== b.length) {
      problems.push(`${name}: a different number of structural lines (english ${a.length}, translation ${b.length})`);
    } else {
      for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) {
          problems.push(`${name}: structural element ${i + 1} differs\n      english:     ${a[i]}\n      translation: ${b[i]}`);
        }
      }
    }

    const pa = placeholders(enText).join(',');
    const pb = placeholders(koText).join(',');
    if (pa !== pb) problems.push(`${name}: the variables differ\n      english:     ${pa}\n      translation: ${pb}`);

    // A Latin letter inside a Cyrillic word renders perfectly and spells the word
    // wrong. Nothing else here would see it — which is why it is checked.
    koText.split('\n').forEach((line, i) => {
      const t = line.trim();
      if (!t || /^(#|VAR|~|===|->)/.test(t)) return;
      const mixed = mixedScript(t).filter((w) => !enText.includes(w.split(' ')[0]));
      if (mixed.length) problems.push(`${name}:${i + 1}: mixed alphabets - ${mixed.join(', ')}`);
    });
  }

  const extra = koFiles.filter((f) => !en.has(f));

  if (missing.length) console.log(`\n${missing.length} untranslated: ${missing.join(', ')}`);
  if (extra.length) console.log(`\n${extra.length} with no english original: ${extra.join(', ')}`);

  if (problems.length) {
    console.log(`\n${problems.length} problems:`);
    problems.forEach((p) => console.log('  - ' + p));
    process.exitCode = 1;
  } else if (!missing.length) {
    console.log('\nevery dialogue has the same structure as its original.');
  }
}

main();

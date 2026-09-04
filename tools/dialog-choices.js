'use strict';

// Prints the dialogue option-label table the launcher injects, as JSON.
//
// Usage: node tools/dialog-choices.js [lang]   (no argument: every bundled language)
//
// It exists so the Rust launcher's copy can be checked against this one. The two build
// the same table from the same .ink files, and autoplay picks the wrong dialogue option
// in silence if they ever disagree - which is not something a person would notice from
// a log line. tests/bundle.rs reads this through BD_NODE_CHOICES.

const fs = require('fs');
const path = require('path');
const cfg = require('../config');
const ink = require('../lib/ink');

function tableFor(lang) {
  const dir = cfg.language(lang).dialogsDir;
  if (!fs.existsSync(dir)) return {};
  return ink.choiceTable(
    (name) => fs.readFileSync(path.join(dir, name), 'utf8'),
    fs.readdirSync(dir),
  );
}

const only = process.argv.slice(2).find((a) => !a.startsWith('--'));
const out = only
  ? tableFor(only)
  : Object.fromEntries(cfg.availableLanguages().sort().map((l) => [l, tableFor(l)]));

process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);

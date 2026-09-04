'use strict';
// Records the current install as a verified combination.
//
//   node tools/fingerprint.js          show what would be recorded
//   node tools/fingerprint.js --write  append it to generated/fingerprint.json
//
// The Steam buildid changes even when the game version does not. Keeping both is
// what makes "why does it not work on my copy" answerable.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const cfg = require('../config');

const WRITE = process.argv.includes('--write');
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');

function steamBuildId() {
  const acf = path.join(cfg.GAME_DIR, '..', '..', 'appmanifest_3834590.acf');
  try {
    const m = /"buildid"\s+"(\d+)"/.exec(fs.readFileSync(acf, 'utf8'));
    return m ? m[1] : null;
  } catch (_) { return null; }
}

const gamePkg = JSON.parse(
  fs.readFileSync(path.join(cfg.GAME_DIR, 'resources', 'app', 'package.json'), 'utf8'),
);
const items = require(cfg.NATIVE).decryptAssetBundle(cfg.BUNDLE);
const js = items.find((it) => /^assets\/index-.*\.js$/.test(it.path));
const css = items.find((it) => /^assets\/style-.*\.css$/.test(it.path));

const entry = {
  gameVersion: gamePkg.version,
  steamAppId: '3834590',
  steamBuildId: steamBuildId(),
  assetsSha256: sha(fs.readFileSync(cfg.BUNDLE)),
  bundleJs: js && js.path,
  bundleJsSha256: js && sha(Buffer.from(js.data)),
  bundleCss: css && css.path,
  dialogsEn: items.filter((it) => /^dialogs\/en\/.*\.ink$/.test(it.path)).length,
  verifiedAt: new Date().toISOString().slice(0, 10),
};

console.log(JSON.stringify(entry, null, 2));

if (!WRITE) {
  console.log('\nPass --write to record it.');
  process.exit(0);
}

fs.mkdirSync(cfg.PATHS.GENERATED, { recursive: true });
let doc = { supported: [] };
try { doc = JSON.parse(fs.readFileSync(cfg.PATHS.FINGERPRINT, 'utf8')); } catch (_) { /* first time */ }
doc.supported = (doc.supported || []).filter((s) => s.bundleJs !== entry.bundleJs);
doc.supported.push(entry);
doc.supported.sort((a, b) => String(a.gameVersion).localeCompare(String(b.gameVersion)));
fs.writeFileSync(cfg.PATHS.FINGERPRINT, `${JSON.stringify(doc, null, 2)}\n`, 'utf8');
console.log(`\nrecorded in ${cfg.PATHS.FINGERPRINT} (${doc.supported.length} in total)`);

'use strict';
// Builds a diagnosis without launching the game. Paste this output into an issue.
//
//   node tools/doctor.js
//   node tools/doctor.js > doctor.txt
//
// A game update breaks anchors. The point of this tool is that nobody has to work
// out which one died by hand.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const cfg = require('../config');
const { NAMESPACES } = require('../patch/i18n');
const { patchBundle, patchCss } = require('../patch/bundle');

const language = require('../lib/language');

const out = [];
const say = (s = '') => out.push(s);
const row = (k, v) => say(`${k.padEnd(10)} ${v}`);

function sha(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function readJson(p) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (_) { return null; }
}

/** Steam's build number. It changes even when the game version does not. */
function steamBuildId() {
  const acf = path.join(cfg.GAME_DIR, '..', '..', 'appmanifest_3834590.acf');
  try {
    const m = /"buildid"\s+"(\d+)"/.exec(fs.readFileSync(acf, 'utf8'));
    return m ? m[1] : '(unreadable)';
  } catch (_) { return '(not from Steam)'; }
}

// Which language would actually be applied on this machine right now. The report is
// about this computer, so it has to reflect this computer's locale.
const catalogue = readJson(cfg.PATHS.LANGUAGES) || { languages: {} };
const choice = language.resolve(catalogue, {
  locale: cfg.systemLocale(),
  available: cfg.availableLanguages(),
});
const L = choice.lang ? cfg.language(choice.lang) : null;

say('== big-dragon-mod doctor ==');
say();

// ── Environment ────────────────────────────────────────────────
const pkg = readJson(path.join(__dirname, '..', 'package.json')) || {};
row('mod', pkg.version || '(unknown)');
row('Node', `${process.version}  ${process.platform} ${process.arch}`);
row('game path', cfg.GAME_DIR);

const gamePkg = readJson(path.join(cfg.GAME_DIR, 'resources', 'app', 'package.json'));
if (!gamePkg) {
  say();
  say('✘ the game was not found. Set BIG_DRAGON_DIR to point at it.');
  console.log(out.join('\n'));
  process.exit(1);
}
row('game version', `${gamePkg.version}   Steam buildid ${steamBuildId()}`);

// ── Bundle ─────────────────────────────────────────────────────
say();
let files;
try {
  const native = require(cfg.NATIVE);
  files = native.decryptAssetBundle(cfg.BUNDLE);
} catch (e) {
  say(`✘ could not open the asset bundle: ${e.message}`);
  console.log(out.join('\n'));
  process.exit(1);
}

// decryptAssetBundle returns an array of [{path, data}].
const pick = (re) => files.find((it) => re.test(it.path));
const jsItem = pick(/^assets\/index-.*\.js$/);
const cssItem = pick(/^assets\/style-.*\.css$/);
const inkCount = files.filter((it) => /^dialogs\/en\/.*\.ink$/.test(it.path)).length;

const jsName = jsItem && jsItem.path;
const cssName = cssItem && cssItem.path;
const jsBuf = jsItem && Buffer.from(jsItem.data);
const cssBuf = cssItem && Buffer.from(cssItem.data);
row('bundle', jsName
  ? `${jsName}  ${jsBuf.length.toLocaleString()} bytes  sha256 ${sha(jsBuf).slice(0, 16)}…`
  : '✘ not found');
row('CSS', cssName
  ? `${cssName}  ${cssBuf.length.toLocaleString()} bytes  sha256 ${sha(cssBuf).slice(0, 16)}…`
  : '✘ not found');
row('dialogues', `${inkCount} in en`);

// ── Supported? ─────────────────────────────────────────────────
const fp = readJson(cfg.PATHS.FINGERPRINT || path.join(cfg.PATHS.GENERATED, 'fingerprint.json'));
const known = fp && (fp.supported || []).find((s) => s.bundleJs === jsName);
say();
row('supported', known
  ? `✔ a verified combination (game ${known.gameVersion})`
  : '⚠ an unverified combination - read the anchor results below');

// ── Anchors ────────────────────────────────────────────────────
say();
say('anchors');
if (!jsBuf) {
  say('  ✘ no bundle, so nothing can be checked');
} else {
  const src = jsBuf.toString('utf8');
  const ko = (L && readJson(L.i18nPath)) || {};
  let res = null;
  try {
    res = patchBundle(src, ko);
  } catch (e) {
    say(`  ✘ the patch failed: ${e.message}`);
  }
  if (res) {
    const mark = (ok) => (ok ? '✔' : '✘');
    say(`  ${mark(res.replaced.length === NAMESPACES.length)} A1 i18n tables    ${res.replaced.length}/${NAMESPACES.length}`);
    say(`  ${mark(res.timeScale && res.timeScale.patched)} A2 time units`);
    say(`  ${mark(res.stores && res.stores.wrapped)} A3 store factory  ${(res.stores && res.stores.wrapped) || 'not found'}`);
    say(`  ${mark(res.dispatch && res.dispatch.id)} A4 dispatch       ${(res.dispatch && res.dispatch.id) || 'not found (the fiber route takes over)'}`);
    say(`  ${mark(res.statsBridge && res.statsBridge.id)} A5 stat table     ${(res.statsBridge && res.statsBridge.id) || 'not found'}`);
    const slots = res.stores && res.stores.found ? Object.keys(res.stores.found).length : 0;
    say(`  ${mark(slots > 0)} A6 slot registry  ${slots}`);
    say(`  ${mark(res.dungeon.scene)} A11 dungeon scene ${res.dungeon.scene || 'not found'}`);
    say(`  ${mark(res.tree.nodes > 0)} A10 upgrade tree  ${res.tree.nodes ? res.tree.nodes + ' nodes' : 'not found - autoplay stalls at 12 upgrades'}`);
    say();
    row('patched', `${src.length.toLocaleString()} -> ${res.code.length.toLocaleString()} bytes`);
    row('translated', `${res.i18n.translated}/${res.i18n.total} UI strings`);
  }
  if (cssBuf) {
    const c = patchCss(cssBuf.toString('utf8'), L ? L.fonts : [], L ? L.fallback : []);
    row('CSS', `${c.faces} @font-face, ${c.hits} font stacks`);
  }
}

// ── Language assets ────────────────────────────────────────────
say();
say('language assets');
const koDialogs = (L && fs.existsSync(L.dialogsDir))
  ? fs.readdirSync(L.dialogsDir).filter((f) => f.endsWith('.ink')).length : 0;
say(`  dialogues ${koDialogs} of ${inkCount}`);
for (const f of (L ? L.fonts : [])) {
  const p = path.join(cfg.PATHS.FONTS, f.file);
  say(`  ${fs.existsSync(p) ? '✔' : '✘'} ${f.file}`);
}
// OFL requires the licence text to travel with the font, and we ship fonts from
// several projects now, so list whatever is actually there rather than one name.
const ofl = fs.readdirSync(cfg.PATHS.FONTS).filter((f) => f.startsWith('OFL-'));
say(`  ${ofl.length ? '✔' : '✘'} ${ofl.length} licence texts: ${ofl.join(', ') || 'none'}`);

say();
say('Paste this output into your issue as it is.');
console.log(out.join('\n'));

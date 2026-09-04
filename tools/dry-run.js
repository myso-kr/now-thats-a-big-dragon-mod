'use strict';

// Produces the patch result without launching the game, and syntax-checks it.
// Usage: node tools/dry-run.js [output path]

const fs = require('fs');
const path = require('path');
const os = require('os');
const cfg = require('../config');
const { NAMESPACES } = require('../patch/i18n');
const { patchBundle, patchCss } = require('../patch/bundle');

const native = require(cfg.NATIVE);
const items = native.decryptAssetBundle(cfg.BUNDLE);

const js = items.find((it) => /^assets\/index-.*\.js$/.test(it.path));
const css = items.find((it) => /^assets\/style-.*\.css$/.test(it.path));

const language = require('../lib/language');
const catalogue = JSON.parse(fs.readFileSync(cfg.PATHS.LANGUAGES, 'utf8'));
const choice = language.resolve(catalogue, {
  requested: process.argv.find((a) => a.startsWith('--lang='))?.slice(7),
  locale: cfg.systemLocale(),
  available: cfg.availableLanguages(),
});
if (!choice.lang) {
  console.error(`could not settle on a language: ${choice.reason}`);
  process.exit(2);
}
const L = cfg.language(choice.lang);
console.log(`language: ${L.lang} (${L.name}) - ${choice.reason}`);
const ko = JSON.parse(fs.readFileSync(L.i18nPath, 'utf8'));

const src = Buffer.from(js.data).toString('utf8');
const catRaw = JSON.parse(fs.readFileSync(cfg.PATHS.LANGUAGES, 'utf8'));
const def = catRaw.languages[L.lang];
const extras = [];
for (const code of cfg.availableLanguages()) {
  if (code === L.lang) continue;
  const o = cfg.language(code);
  if (!fs.existsSync(o.i18nPath)) continue;
  extras.push({
    code, label: o.name, flagFile: o.flagFile,
    tables: JSON.parse(fs.readFileSync(o.i18nPath, 'utf8')),
  });
}
const out = patchBundle(src, ko, {
  code: L.lang, label: def.name, flagFile: def.flagFile,
}, extras);
console.log(`tables: ${out.replaced.length}`);
console.log(out.added
  ? `languages added: ${out.added.langs.join(', ')} · list ${out.added.supported ? '✔' : '✘'} · flags ${out.added.flag ? '✔' : '✘'} · labels ${out.added.labels} · scale ${out.added.timeScale}/${out.added.langs.length} · fallback ${out.added.fallback ? '✔' : '✘'}`
  : 'fell back to overwriting the en slot');
console.log(`translated: ${out.i18n.translated}/${out.i18n.total} strings`);
console.log(`time units: ${out.timeScale.patched
  ? (out.timeScale.labels ? out.timeScale.labels.join(' / ') : 'a Scale of its own was added')
  : 'none (the English units stay)'}`);
console.log(`store bridge: ${out.stores.wrapped ? 'wrapped ' + out.stores.wrapped + ' factories' : 'failed'}`);
console.log(`upgrade tree: ${out.tree.nodes ? out.tree.nodes + ' nodes in ' + out.tree.branches + ' branches' : 'not found'}`);
console.log(`size: ${src.length.toLocaleString()} -> ${out.code.length.toLocaleString()} bytes`);

const cssOut = patchCss(Buffer.from(css.data).toString('utf8'), L.fonts, L.fallback);
console.log(`CSS fonts: ${cssOut.faces} @font-face, ${cssOut.hits} font stacks`);

// Only a bare argument is the output directory; flags are not paths. Treating
// `--lang=xx` as one wrote the result somewhere nobody would look, while the report
// said everything had worked.
const dir = process.argv.slice(2).find((a) => !a.startsWith('--'))
  || path.join(os.tmpdir(), 'bd-dryrun');
fs.mkdirSync(dir, { recursive: true });
const jsPath = path.join(dir, path.basename(js.path));
const cssPath = path.join(dir, path.basename(css.path));
// The original goes out alongside the patched copy, so the Rust launcher's patch
// can be diffed against this one on the same input. See tests/bundle.rs.
const origPath = path.join(dir, 'original-' + path.basename(js.path));
fs.writeFileSync(origPath, src, 'utf8');
fs.writeFileSync(path.join(dir, 'original-' + path.basename(css.path)),
  Buffer.from(css.data).toString('utf8'), 'utf8');
fs.writeFileSync(jsPath, out.code, 'utf8');
fs.writeFileSync(cssPath, cssOut.code, 'utf8');
console.log(`\nwritten: ${jsPath}\n         ${cssPath}`);
console.log('check the syntax with: node --check ' + JSON.stringify(jsPath));

// A broken required anchor has to reach the exit code. Returning 0 quietly would
// make this worthless on a release checklist and in CI alike.
const required = [
  ['A1 i18n tables', out.replaced.length === NAMESPACES.length],
  ['A3 store factory', !!out.stores.wrapped],
  ['A5 stat table', !!out.statsBridge.id],
  // Without it autoplay can never send the unlock signals, and stalls at 12 of 88.
  ['A10 upgrade tree', out.tree.nodes > 0],
];
const broken = required.filter(([, ok]) => !ok).map(([n]) => n);
if (broken.length) {
  console.error(`\n✘ required anchors failed: ${broken.join(', ')}`);
  console.error('  The game may have updated. `npm run doctor` says more.');
  process.exitCode = 1;
} else {
  console.log('\n✔ every required anchor passed');
}

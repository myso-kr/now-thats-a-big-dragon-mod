'use strict';
// The Node bundle patcher, checked against hand-written fixtures.
//
// The Rust launcher has its own tests over the same logic (src/patch/), and
// tests/bundle.rs checks that the two agree on a real bundle. These cover the Node
// side on its own, which is what the tools under tools/ actually run.

const test = require('node:test');
const assert = require('node:assert');
const scan = require('./scan');
const i18n = require('./i18n');
const bridge = require('./bridge');
const css = require('./css');

// ── scan ─────────────────────────────────────────────────────────────

test('nested braces are counted to the end', () => {
  const s = 'X={a:{b:{c:1}},d:2};';
  const f = scan.findObjectLiteral(s, 'X');
  assert.strictEqual(f.body, '{a:{b:{c:1}},d:2}');
});

test('a closing brace inside a string does not fool the scanner', () => {
  const s = 'X={a:"}}}",b:1};';
  assert.strictEqual(scan.findObjectLiteral(s, 'X').body, '{a:"}}}",b:1}');
});

test('an escaped quote is stepped over', () => {
  const s = 'X={a:"a\\"}",b:1};';
  assert.strictEqual(scan.findObjectLiteral(s, 'X').body, '{a:"a\\"}",b:1}');
});

test('braces inside a template substitution are ignored', () => {
  const s = 'X={a:`${1+1}}`,b:2};';
  assert.strictEqual(scan.findObjectLiteral(s, 'X').body, '{a:`${1+1}}`,b:2}');
});

test('the tail of a longer identifier is not matched', () => {
  const s = 'xENe={wrong:1};ENe={right:1};';
  assert.strictEqual(scan.findObjectLiteral(s, 'ENe').body, '{right:1}');
});

test('unbalanced input finds nothing', () => {
  assert.strictEqual(scan.scanBalanced('{a:1', 0), -1);
  assert.strictEqual(scan.findObjectLiteral('X={a:1', 'X'), null);
});

test('parentheses are matched the same way', () => {
  const s = 'f(a,(b),")")';
  assert.strictEqual(scan.scanParens(s, 1), s.length - 1);
});

// ── i18n ─────────────────────────────────────────────────────────────

const enBlock = (map) => `var L={en:{${Object.entries(map).map(([k, v]) => `${k}:${v}`).join(',')}},fr:{}};`;
const fullMap = Object.fromEntries(i18n.NAMESPACES.map((ns, i) => [ns, `F${i}`]));

test('every namespace is found in the en block', () => {
  const ids = i18n.findEnTableIds(enBlock(fullMap));
  assert.strictEqual(Object.keys(ids).length, i18n.NAMESPACES.length);
  assert.strictEqual(ids.upgrades, 'F0');
});

test('a block with only some namespaces is not matched', () => {
  assert.strictEqual(i18n.findEnTableIds('var L={en:{upgrades:A,common:B}};'), null);
});

test('the JSON.parse form the upgrades table uses is read', () => {
  const v = i18n.evalLiteral('{details:JSON.parse(`{"x":{"title":"T"}}`),other:"o"}');
  assert.strictEqual(v.details.x.title, 'T');
  assert.strictEqual(v.other, 'o');
});

test('korean wins where there is korean, and the original stays otherwise', () => {
  const merged = i18n.deepMerge({ a: 'A', b: { c: 'C' } }, { a: '가' });
  assert.strictEqual(merged.a, '가');
  assert.strictEqual(merged.b.c, 'C');
});

test('a key only the translation has is kept', () => {
  const merged = i18n.deepMerge({ a: 'A' }, { a: '가', extra: '추가' });
  assert.strictEqual(merged.extra, '추가');
});

test('only strings are counted, and only real changes count as translated', () => {
  const n = i18n.countStrings({ s: 'x', n: 1, same: 'y' }, { s: '엑스', same: 'y' });
  assert.strictEqual(n.total, 2, 'the number is not a string');
  assert.strictEqual(n.translated, 1, 'an identical string is not a translation');
});

test('patching replaces every table and reports what it did', () => {
  let src = enBlock(fullMap);
  for (const [ns, id] of Object.entries(fullMap)) src += `${id}={hello:"Hello ${ns}"};`;
  const r = i18n.patch(src, { upgrades: { hello: '안녕' } });
  assert.strictEqual(r.replaced.length, i18n.NAMESPACES.length);
  assert.strictEqual(r.total, i18n.NAMESPACES.length, 'one string per table');
  assert.strictEqual(r.translated, 1);
  assert.ok(r.code.includes('안녕'));
  assert.ok(r.code.includes('Hello common'), 'untranslated tables keep the original');
});

test('a missing en block is an error, not a silent no-op', () => {
  assert.throws(() => i18n.patch('var x=1;', {}), /en i18n tables/);
});

test('the time scale is rewritten from the statistics labels', () => {
  const src = 'new S({seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3})';
  const r = i18n.patchTimeScale(src, {
    statistics: {
      seconds_other: '초', minutes_other: '분', hours_other: '시간',
      days_other: '일', months_other: '개월', years_other: '년',
    },
  });
  assert.strictEqual(r.patched, true);
  assert.ok(r.code.includes('"분":60'));
  assert.ok(!r.code.includes('minutes:60'));
});

test('an incomplete label set leaves the scale alone', () => {
  const src = 'new S({seconds:1,minutes:60,hours:3600,days:86400,months:2592e3,years:31536e3})';
  const r = i18n.patchTimeScale(src, { statistics: { seconds_other: '초' } });
  assert.strictEqual(r.patched, false);
  assert.strictEqual(r.code, src, 'a half-translated scale would be worse than none');
});

// ── bridge ───────────────────────────────────────────────────────────

const app = (id) => `function App(){const[,${id}]=R.useReducer(rd,init);`
  + `return J(C.Provider,{value:${id},children:null});}`;

test('the dispatch handed to a Provider is the one taken', () => {
  const r = bridge.injectDispatchBridge(app('dp'));
  assert.strictEqual(r.id, 'dp');
  assert.ok(r.code.includes('window.__bd_dispatch=dp;'));
});

test('an identifier with a dollar sign is still found', () => {
  // Unescaped, `$` becomes an end anchor and the confirmation never matches.
  assert.strictEqual(bridge.injectDispatchBridge(app('d$p')).id, 'd$p');
  assert.strictEqual(bridge.injectDispatchBridge(app('$')).id, '$');
});

test('a useReducer that does not reach a Provider is skipped', () => {
  const r = bridge.injectDispatchBridge('const[,x]=R.useReducer(a,b);const y=1;');
  assert.strictEqual(r.id, null);
  assert.strictEqual(r.code, 'const[,x]=R.useReducer(a,b);const y=1;');
});

test('the generation table is found and exposed', () => {
  const r = bridge.injectStatsBridge('var Pi={total:{},click:{},warrior:{},wizard:{}};');
  assert.strictEqual(r.id, 'Pi');
  assert.ok(r.code.includes('window.__bd_stats=Pi;'));
});

test('the store factory is wrapped, not replaced', () => {
  const src = 'function mk(o){const s=create(o.savePrefix);return s;}';
  const r = bridge.wrapStoreFactory(src);
  assert.strictEqual(r.wrapped, 'mk');
  assert.ok(r.code.includes('function mk$bd(o){'), 'the original is renamed');
  assert.ok(r.code.includes('function mk(...a)'), 'and a wrapper takes its name');
  assert.ok(r.code.includes('saveKey'));
});

test('the epilogue exposes each store under its own try', () => {
  const src = 'a.getState().setGold(1);b.getState().generators;c.push({store:x,baseKey:"k"});';
  const r = bridge.appendStoreEpilogue(src);
  assert.strictEqual(r.found.currency, 'a');
  assert.strictEqual(r.found.generators, 'b');
  assert.strictEqual(r.found.__slots, 'c');
  assert.strictEqual((r.code.match(/try\{/g) || []).length, 3, 'one try each');
});

test('the epilogue starts on its own line', () => {
  // The bundle's last line can be a //# sourceMappingURL comment; appending to it
  // would comment the whole epilogue out.
  const src = 'a.getState().setGold(1);\n//# sourceMappingURL=x.map';
  const r = bridge.appendStoreEpilogue(src);
  assert.ok(r.code.includes('\n;try{'), 'the epilogue is not on the comment line');
});

test('with no anchors, the epilogue changes nothing', () => {
  const r = bridge.appendStoreEpilogue('var x=1;');
  assert.strictEqual(r.code, 'var x=1;');
});

// ── css ──────────────────────────────────────────────────────────────

const FONTS = [{
  replaces: 'everyday_standard',
  family: 'bd_ko_body',
  url: 'fonts/bd-ko-body.woff2',
  pxPerEm: 8,
  basePxPerEm: 6,
  ascentOverride: 150,
  descentOverride: 50,
}];

test('usages get the fallback, declarations do not', () => {
  const src = '@font-face{font-family:everyday_standard;src:url(a.woff2)}'
    + '.t{font-family:everyday_standard}';
  const r = css.patch(src, FONTS, ['Malgun Gothic', 'sans-serif']);
  assert.strictEqual(r.faces, 1);
  assert.strictEqual(r.hits, 1, 'the declaration is left alone');
  assert.ok(r.code.includes('everyday_standard, bd_ko_body'));
});

test('size-adjust is the grid ratio', () => {
  const r = css.patch('.t{}', FONTS, []);
  assert.ok(r.code.includes('size-adjust:133.3333%'), '8/6');
});

test('metrics are divided by size-adjust so line height is unchanged', () => {
  const r = css.patch('.t{}', FONTS, []);
  assert.ok(r.code.includes('ascent-override:112.5%'), '150 / (8/6)');
});

test('@charset stays on the first line', () => {
  const r = css.patch('@charset "utf-8";.t{color:red}', FONTS, []);
  assert.ok(r.code.startsWith('@charset "utf-8";'));
  assert.ok(r.code.includes('@font-face'));
});

test('a font name needing quotes gets them', () => {
  assert.strictEqual(css.quoteFamily('Malgun Gothic'), "'Malgun Gothic'");
  assert.strictEqual(css.quoteFamily('sans-serif'), 'sans-serif', 'a generic family is a keyword');
  assert.strictEqual(css.quoteFamily('Arial'), 'Arial');
});

test('an entry with no `replaces` ships no CSS', () => {
  const r = css.patch('.t{font-family:everyday_standard}', [{ family: 'x', url: 'y' }], []);
  assert.strictEqual(r.faces, 0);
  assert.strictEqual(r.hits, 0);
});

// ── The prologue in front of the patched bundle ───────────────────
// Three things the injected scripts read off `window`. They used to be injected by the
// Node launcher only, so the Rust launcher - the one that ships - had none of them: the
// cheat widget showed raw ids, and autoplay, with no upgrade tree, could never send the
// unlock signals and stalled at 12 of the 88 upgrades.

const tree = require('./tree');
const { patchBundle } = require('./bundle');

const TREE_SRC = 'n.CarpalCure="carpalCure",n.IronFinger="ironFinger";'
  + 'var t={click:[{id:ge.CarpalCure,children:[ge.IronFinger],subTreeConfig:{unlockAt:1}},'
  + '{id:ge.IronFinger,children:[]}],BUG_HIDE:[{id:ge.CarpalCure}]};';

test('the upgrade tree is read out of the bundle', () => {
  const t = tree.extractTree(TREE_SRC);
  assert.deepStrictEqual(t.click.carpalCure, { children: ['ironFinger'], unlockAt: 1 });
  assert.strictEqual(t.click.ironFinger.unlockAt, 3, "the game's own default");
  assert.strictEqual(t.BUG_HIDE, undefined, 'the hidden debug branch is left out');
  assert.strictEqual(tree.countNodes(t), 2);
});

test('a bundle without the anchor gives no tree rather than throwing', () => {
  // A game update that moves this costs autoplay its unlock signals and nothing else.
  assert.strictEqual(tree.extractTree('var x=1;'), null);
  assert.strictEqual(tree.countNodes(null), 0);
});

test('a name the bundle never defines gives no tree rather than a wrong one', () => {
  const src = 'var t={click:[{id:ge.CarpalCure,children:[ge.NeverDefined]}]};';
  assert.strictEqual(tree.extractTree(src), null);
});

test('branches come out sorted, so both launchers serialise alike', () => {
  const src = 'n.A="a",n.B="b";var t={warrior:[{id:ge.B,children:[]}],'
    + 'click:[{id:ge.A,children:[]}]};';
  assert.deepStrictEqual(Object.keys(tree.extractTree(src)), ['click', 'warrior']);
});

test('a minified leading-dot number does not defeat the tree reader', () => {
  // `.7` for 0.7 is how a minifier writes it, and how the game's tree does.
  const src = 'n.A="a";var t={click:[{id:ge.A,children:[],w:.7}]};';
  assert.deepStrictEqual(tree.extractTree(src).click.a, { children: [], unlockAt: 3 });
});

test('the patched bundle carries the tree and both name tables in front of it', () => {
  const r = patchBundle(TREE_SRC, null);
  assert.ok(r.code.startsWith('window.__bd_upgradeTree='), 'the tree comes first');
  assert.ok(r.code.includes('window.__bd_upgradeNames={};'));
  assert.ok(r.code.includes('window.__bd_levelNames={};'));
  assert.strictEqual(r.tree.nodes, 2);
});

test('with no tree in the bundle the rest of the patch still goes in', () => {
  const r = patchBundle('var x=1;', null);
  assert.ok(!r.code.includes('__bd_upgradeTree'), 'no tree is claimed');
  assert.ok(r.code.includes('window.__bd_upgradeNames={};'));
  assert.ok(r.code.endsWith('var x=1;'), 'the source itself survives');
  assert.strictEqual(r.tree.nodes, 0);
});

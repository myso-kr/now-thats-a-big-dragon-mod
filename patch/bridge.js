'use strict';

// Opens the windows through which the mod reaches game state.
//
// There are three bridges, and they are different in kind:
//   store     wraps the zustand persist factory to expose the per-slot stores
//   dispatch  grabs the React context dispatch (the game's own command path)
//   stats     exposes the per-unit generation table the game already computes
//
// Mirrors src/patch/bridge.rs.

const { scanBalanced, scanParens } = require('./scan');

// ── The stats bridge ─────────────────────────────────────────────────
// The game computes each unit's effective output — damagePerTick, goldGeneration,
// unitsGeneration, with every upgrade and inspiration multiplier already applied —
// into one table. Reading it saves autoplay from reimplementing the DPS formulas.
const STATS_PATTERN = /([A-Za-z0-9_$]+)=\{total:\{\},click:\{\},warrior:\{\}/;

function injectStatsBridge(src) {
  const m = src.match(STATS_PATTERN);
  if (!m) return { code: src, id: null };
  const end = scanBalanced(src, src.indexOf('{', m.index + m[1].length));
  if (end < 0) return { code: src, id: null };
  const code = `,__bd_stats_bridge=(()=>{try{window.__bd_stats=${m[1]};}catch(_bd){}return 0;})()`;
  return { code: src.slice(0, end) + code + src.slice(end), id: m[1] };
}

// ── The dispatch bridge ──────────────────────────────────────────────
// Game commands — buying, firing inspiration, changing level — leave only through
// the React context dispatch. The Provider hands useReducer's dispatch through as
// its value, so we intercept it there and expose it as window.__bd_dispatch. Unlike
// writing the stores directly, this means the game's own events, unlocks and
// achievement side effects all still happen.
const DISPATCH_PATTERN = /\[,([A-Za-z0-9_$]+)\]=[A-Za-z0-9_$]+\.useReducer\(/g;

function injectDispatchBridge(src) {
  DISPATCH_PATTERN.lastIndex = 0;
  let m;
  while ((m = DISPATCH_PATTERN.exec(src)) !== null) {
    const id = m[1];
    // Confirm this is the dispatch handed to a Provider value, not some other
    // useReducer. Minified identifiers commonly contain `$`, so the metacharacters
    // have to be escaped for real — note that inside a template literal neither `\.`
    // nor `\{` is an escape, which is exactly how this went wrong once.
    const esc = id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    if (!new RegExp(`\\.Provider,\\{value:${esc}[,}]`)
      .test(src.slice(m.index, m.index + 900))) continue;

    const open = m.index + m[0].length - 1;      // the '(' of useReducer(
    const close = scanParens(src, open);
    if (close < 0) continue;
    if (src[close + 1] !== ';') continue;        // not a statement end: skip it

    const at = close + 2;
    // The catch parameter is named apart so it cannot shadow the dispatch identifier.
    const code = `try{window.__bd_dispatch=${id};}catch(_bd){}`;
    return { code: src.slice(0, at) + code + src.slice(at), id };
  }
  return { code: src, id: null };
}

// ── The store bridge ─────────────────────────────────────────────────
// The game's real state lives in module-scope zustand stores, not in the
// `global_game_store` exposed on window. That one's `globalVariables` is a mirror
// kept for Ink dialogue: write gold into it and the next tick puts it back. Since
// the bundle passes through our hands anyway, we expose the stores as
// window.__bd_stores.

// Store identifiers, found by meaning rather than by name so minification cannot
// break them.
const STORE_PATTERNS = {
  currency: /([A-Za-z0-9_$]+)\.getState\(\)\.setGold\(/,
  generators: /([A-Za-z0-9_$]+)\.getState\(\)\.generators/,
  upgrades: /([A-Za-z0-9_$]+)\.getState\(\)\.upgrades/,
  dragon: /([A-Za-z0-9_$]+)\.getState\(\)\.sync\(\{dragonHealth/,
  combat: /([A-Za-z0-9_$]+)\.getState\(\)\.enterCombat\(/,
  levels: /([A-Za-z0-9_$]+)\.getState\(\)\.beatenLevels/,
};

// The values actually in play sit in per-slot stores (slot_<slot>_<key>), which the
// game gathers into one `[{store, baseKey}]` array. Taking that array reaches the
// active stores without needing to know the slot name.
const SLOT_REGISTRY_PATTERN = /([A-Za-z0-9_$]+)\.push\(\{store:[A-Za-z0-9_$]+,baseKey:/;

/** Wrap the persist-store factory so each store registers itself by saveKey. */
function wrapStoreFactory(src) {
  const anchor = src.indexOf('savePrefix');
  if (anchor < 0) return { code: src, wrapped: null };

  const head = src.lastIndexOf('function ', anchor);
  if (head < 0) return { code: src, wrapped: null };

  const m = /^function\s+([A-Za-z0-9_$]+)\s*\(([^)]*)\)\s*\{/.exec(src.slice(head, anchor));
  if (!m) return { code: src, wrapped: null };

  const name = m[1];
  const braceAt = head + m[0].length - 1;
  const bodyEnd = scanBalanced(src, braceAt);
  if (bodyEnd < 0) return { code: src, wrapped: null };

  const renamed = `function ${name}$bd(${m[2]}){`;
  const wrapper = `function ${name}(...a){const s=${name}$bd(...a);`
    + `try{const k=a[0]&&a[0].saveKey;if(k){(window.__bd_stores||(window.__bd_stores={}))[k]=s;}}catch(e){}`
    + 'return s;}';

  const code = src.slice(0, head) + renamed + src.slice(braceAt + 1, bodyEnd)
    + wrapper + src.slice(bodyEnd);
  return { code, wrapped: name };
}

/** Export the module-scope store constants onto window at the end of the module. */
function appendStoreEpilogue(src) {
  const found = {};
  const parts = [];

  const reg = src.match(SLOT_REGISTRY_PATTERN);
  if (reg) {
    found.__slots = reg[1];
    parts.push(`try{window.__bd_slotStores=${reg[1]};}catch(e){}`);
  }

  for (const [key, re] of Object.entries(STORE_PATTERNS)) {
    const m = src.match(re);
    if (!m) continue;
    found[key] = m[1];
    // Each gets its own try, so one out-of-scope name cannot take the rest down.
    parts.push(`try{(window.__bd_stores||(window.__bd_stores={})).${key}=${m[1]};}catch(e){}`);
  }
  if (!parts.length) return { code: src, found };
  // The leading newline matters: the bundle's last line may be a `//#` comment, and
  // appending to it would comment the whole epilogue out.
  return { code: `${src}\n;${parts.join('')}\n`, found };
}

function injectStoreBridge(src) {
  const a = wrapStoreFactory(src);
  const b = appendStoreEpilogue(a.code);
  return { code: b.code, wrapped: a.wrapped, found: b.found };
}

// ── The dungeon bridge ───────────────────────────────────────────────
// The dungeon is a Babylon.js scene drawn to a canvas, not a grid of DOM tiles - so
// there is nothing for autoplay to read the way it reads a dialogue. Its walls,
// chests, enemies and exit exist only as meshes in that scene, and the scene itself
// is a `const` inside a React effect: no ref holds it, so no fiber walk reaches it.
//
// So it is handed over at the one place it is knowable. The effect builds an engine
// over the canvas, makes a scene on it, and immediately sets a clear colour:
//
//   const Kt=I.current, Wr=new Ye(Kt,!0), Ci=new _t(Wr); Ci.clearColor=new ke(0,0,0,1);
//
// That whole shape - `new X(canvas,!0)`, then a scene over it, then `.clearColor=` on
// the scene - occurs exactly once in the eight megabytes, while `.clearColor=` alone
// occurs seventeen times. Matching the shape rather than the name is what keeps it
// from binding to a Babylon internal.
const DUNGEON_PATTERN =
  /([A-Za-z0-9_$]+)=new [A-Za-z0-9_$]+\([A-Za-z0-9_$]+,!0\),([A-Za-z0-9_$]+)=new [A-Za-z0-9_$]+\(\1\);\2\.clearColor=/;

/**
 * Expose the dungeon's Babylon scene as `window.__bd_dungeon`.
 *
 * The scene is replaced on every descent, so the handle is refreshed rather than kept:
 * a stale scene still answers, and autoplay would be reading the maze it just left.
 */
function injectDungeonBridge(src) {
  const m = src.match(DUNGEON_PATTERN);
  if (!m) return { code: src, engine: null, scene: null };
  const [engine, scene] = [m[1], m[2]];
  // After the whole clear-colour statement, not inside its expression: the value being
  // assigned is a constructor call, and splicing into it only produced an unbalanced
  // paren and a bundle that would not parse.
  const at = endOfStatement(src, m.index + m[0].length);
  if (at < 0) return { code: src, engine: null, scene: null };
  const set = `window.__bd_dungeon={scene:${scene},engine:${engine},at:Date.now()};`;
  return { code: src.slice(0, at) + set + src.slice(at), engine, scene };
}

/**
 * Just past the `;` that ends the statement starting at `from`.
 *
 * Only depth zero counts - `new ke(0,0,0,1)` has none of its own, but a future
 * expression with a function literal in it would, and a `;` inside a string is not the
 * end of anything.
 */
function endOfStatement(src, from) {
  let depth = 0;
  let quote = null;
  for (let i = from; i < src.length; i += 1) {
    const c = src[i];
    if (quote) {
      if (c === '\\') i += 1;
      else if (c === quote) quote = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { quote = c; continue; }
    if (c === '(' || c === '[' || c === '{') depth += 1;
    else if (c === ')' || c === ']' || c === '}') depth -= 1;
    else if (c === ';' && depth === 0) return i + 1;
    if (depth < 0) return -1;
  }
  return -1;
}

module.exports = {
  injectStatsBridge,
  injectDungeonBridge,
  injectDispatchBridge,
  injectStoreBridge,
  wrapStoreFactory,
  appendStoreEpilogue,
  STATS_PATTERN,
  DISPATCH_PATTERN,
  STORE_PATTERNS,
  SLOT_REGISTRY_PATTERN,
};

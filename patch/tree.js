'use strict';

// The upgrade tree, read out of the bundle.
//
// Unlocking is done by the UI click handler, not the reducer:
//   dispatch(buy_upgrade)
//   purchased === 0                    -> dispatch(show_upgrade,   {children})
//   purchased + 1 === (unlockAt ?? 3)  -> dispatch(unlock_upgrade, {children})
// Autoplay sends only buy_upgrade, which leaves the tree shut forever - 12 of the 88
// upgrades reachable. Sending those two signals ourselves needs each upgrade's
// children and its unlockAt, and that is what this reads.
//
// It used to come from a file that `tools/extract-tree.js` wrote by hand, which had
// two problems: the file is derived from the game and so is not committed, meaning the
// Rust launcher - the one that actually ships - never had it and autoplay stalled at
// twelve upgrades; and a stale file would quietly disagree with the bundle in front of
// it. Reading the bundle both launchers are already patching solves both at once.
//
// `src/patch/tree.rs` is the Rust side; tests/bundle.rs checks they agree.

const { scanBalanced } = require('./scan');

// `click:[{id:ge.CarpalCure` - the first branch of the tree, and the only place in the
// bundle where a tree node literal follows a branch name.
const ANCHOR = 'click:[{id:ge.';
const GE_ENTRY = /n\.([A-Z][A-Za-z0-9]*)="([a-zA-Z][a-zA-Z0-9]*)"/g;
const GE_REF = /ge\.([A-Z][A-Za-z0-9]*)/g;

/** `n.CarpalCure="carpalCure"` throughout the bundle becomes `{CarpalCure: 'carpalCure'}`. */
function upgradeIds(src) {
  const ids = {};
  for (const m of src.matchAll(GE_ENTRY)) {
    if (!(m[1] in ids)) ids[m[1]] = m[2];
  }
  return ids;
}

/**
 * `{ family: { upgrade: { children, unlockAt } } }`, or null when the anchor is gone.
 *
 * Returning null rather than throwing is deliberate: a game update that moves this
 * costs autoplay its unlock signals, and nothing else - the translation, the cheats
 * and everything else in the patch should still go in.
 */
function extractTree(src) {
  const at = src.indexOf(ANCHOR);
  if (at < 0) return null;
  const ids = upgradeIds(src);

  // Walk back to the brace that opens the whole tree, not the nearest one.
  //
  // The nearest `{` before `click:` is the tree's own only while every branch declared
  // ahead of it is empty - which today is true, because `BUG_HIDE:[]` is first and
  // holds nothing. One node in front of `click:` and the nearest `{` would be that
  // node's, and this would quietly return a single upgrade as though it were the tree.
  // So candidates are tried outwards until one parses to an object with a `click`
  // branch in it, which only the tree itself has.
  let tree = null;
  for (let from = at; from >= 0 && !tree; from = src.lastIndexOf('{', from) - 1) {
    const start = src.lastIndexOf('{', from);
    if (start < 0) break;
    const end = scanBalanced(src, start);
    if (end === null || end === undefined || end <= at) continue;

    let unknown = false;
    const literal = src.slice(start, end).replace(GE_REF, (_, k) => {
      if (!(k in ids)) { unknown = true; return 'null'; }
      return JSON.stringify(ids[k]);
    });
    if (unknown) return null;

    let candidate;
    try {
      // A pure object literal with no calls, and every `ge.X` already a string.
      // eslint-disable-next-line no-new-func
      candidate = new Function(`return (${literal})`)();
    } catch (_) {
      continue;
    }
    if (candidate && typeof candidate === 'object' && Array.isArray(candidate.click)) {
      tree = candidate;
    }
  }
  if (!tree) return null;

  const out = {};
  for (const cat of Object.keys(tree).sort()) {
    const list = tree[cat];
    if (!Array.isArray(list) || cat === 'BUG_HIDE') continue;
    const m = {};
    for (const node of list) {
      if (!node || typeof node.id !== 'string') continue;
      m[node.id] = {
        children: Array.isArray(node.children) ? node.children : [],
        // The game's own default, from `subTreeConfig?.unlockAt ?? 3`.
        unlockAt: (node.subTreeConfig && typeof node.subTreeConfig.unlockAt === 'number')
          ? node.subTreeConfig.unlockAt : 3,
      };
    }
    out[cat] = m;
  }
  return Object.keys(out).length ? out : null;
}

/** How many nodes a tree holds, for the log line. */
function countNodes(tree) {
  return Object.values(tree || {}).reduce((n, m) => n + Object.keys(m).length, 0);
}

module.exports = { extractTree, upgradeIds, countNodes, ANCHOR };

'use strict';

// Prints the upgrade tree the launchers read out of the bundle.
//
// Usage: node tools/extract-tree.js <path to an extracted index-*.js>
//
// This is a debugging aid, not a build step. Both launchers extract the tree from the
// bundle they are already patching (patch/tree.js and src/patch/tree.rs), so nothing
// reads a file on disk any more. It used to write one - to a path config.js did not
// read, so what actually shipped was whatever stale copy happened to be there, and the
// Rust launcher had no tree at all.

const fs = require('fs');
const { extractTree, countNodes } = require('../patch/tree');

const SRC = process.argv[2];
if (!SRC || !fs.existsSync(SRC)) {
  console.error('usage: node tools/extract-tree.js <path to an extracted index-*.js>');
  process.exit(1);
}

const tree = extractTree(fs.readFileSync(SRC, 'utf8'));
if (!tree) {
  console.error('no upgrade tree found - the anchor has moved. See docs/ANCHORS.md.');
  process.exit(1);
}

console.error(`${Object.keys(tree).length} branches, ${countNodes(tree)} nodes`);
for (const [cat, m] of Object.entries(tree)) {
  const leaves = Object.values(m).filter((x) => !x.children.length).length;
  console.error(`  ${cat.padEnd(10)} ${String(Object.keys(m).length).padStart(3)} (${leaves} leaves)`);
}
process.stdout.write(`${JSON.stringify(tree, null, 1)}\n`);

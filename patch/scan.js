'use strict';

// Finds balanced bracket spans inside minified JS.
//
// This file knows nothing about what JS means. It only counts pairs without being
// fooled by brackets inside string, template, or regex literals — which is exactly
// why it can be tested apart from the patching logic.
//
// Mirrors src/patch/scan.rs; the two are meant to be read side by side.

/** Index just past the closing quote of the string starting at `i`. */
function skipQuoted(src, i, quote) {
  i += 1;
  while (i < src.length) {
    if (src.charCodeAt(i) === 92) { i += 2; continue; }   // backslash escape
    if (src[i] === quote) return i;
    i += 1;
  }
  return i;
}

/** The same for a template literal, stepping over `${…}` substitutions. */
function skipTemplate(src, i) {
  i += 1;
  while (i < src.length) {
    if (src.charCodeAt(i) === 92) { i += 2; continue; }
    if (src[i] === '`') return i;
    if (src[i] === '$' && src[i + 1] === '{') {
      const close = scanBalanced(src, i + 1);
      if (close < 0) return src.length;
      i = close;
      continue;
    }
    i += 1;
  }
  return i;
}

/** Given `src[open] === '{'`, the index just past its matching `}`, or -1. */
function scanBalanced(src, open) {
  let depth = 0;
  for (let i = open; i < src.length; i += 1) {
    const c = src[i];
    if (c === '"' || c === "'") { i = skipQuoted(src, i, c); continue; }
    if (c === '`') { i = skipTemplate(src, i); continue; }
    if (c === '{') depth += 1;
    else if (c === '}') {
      depth -= 1;
      if (depth === 0) return i + 1;
    }
  }
  return -1;
}

/** The same for parentheses: given `src[open] === '('`, the index of its `)`. */
function scanParens(src, open) {
  let depth = 0;
  for (let i = open; i < src.length; i += 1) {
    const c = src[i];
    if (c === '"' || c === "'") { i = skipQuoted(src, i, c); continue; }
    if (c === '`') { i = skipTemplate(src, i); continue; }
    if (c === '(') depth += 1;
    else if (c === ')') { depth -= 1; if (depth === 0) return i; }
  }
  return -1;
}

/**
 * Locate the object literal that follows `id={`.
 * Checks the preceding character so we do not match the tail of a longer identifier
 * — `ENe` must not be found inside `xENe`.
 */
function findObjectLiteral(src, id) {
  const needle = `${id}={`;
  let from = 0;
  for (;;) {
    const start = src.indexOf(needle, from);
    if (start < 0) return null;

    const prev = start > 0 ? src[start - 1] : '';
    if (/[A-Za-z0-9_$]/.test(prev)) { from = start + 1; continue; }

    const braceStart = start + id.length + 1;
    const end = scanBalanced(src, braceStart);
    if (end < 0) { from = start + 1; continue; }
    return { start: braceStart, end, body: src.slice(braceStart, end) };
  }
}

module.exports = { scanBalanced, scanParens, skipQuoted, skipTemplate, findObjectLiteral };

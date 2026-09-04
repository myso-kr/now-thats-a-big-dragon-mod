---
layout: default
title: "Anchor catalogue"
description: "What the bundle patch keys on, what breaks when the game moves it, and where to fix it."
lang: en
---

# Anchor catalogue

This mod attaches to the game bundle's **internal structure** by regex. A game update
can move that structure and break it. This table collects, in one place, what breaks
and where to fix it.

## Minification preserves most of what we key on

Investigation found that most anchors key on things a minifier **does not touch**.
Only local identifiers get shortened; property names, string literals, and API names
survive intact.

| # | Anchor | Keys on | After minification | Breaks | Fix in |
|---|---|---|---|---|---|
| A1 | i18n tables | 13 namespace names, matched on containment | preserved | every translation | `patch/i18n.rs` · `patch/bundle.js` |
| A2 | time units | `{seconds:1,…,years:31536e3}` | preserved | "minutes" stays English | same |
| A11 | dungeon scene | `new X(canvas,!0)`, a scene on it, then `.clearColor=` | preserved | no dungeon farming | `patch/bridge.rs` · `patch/bridge.js` |
| A10 | upgrade tree | `click:[{id:ge.` + the `n.Xxx="xxx"` name table | preserved | autoplay stalls at 12 of the 88 upgrades | `patch/tree.rs` · `patch/tree.js` |
| A9 | flags and labels | `{en:"us.png",…}` · `languages:{en:"English",…}` | preserved | the settings screen shows no flag or name | `patch/locale.rs` · `patch/locale.js` |
| A3 | store factory | the string `savePrefix` | preserved | resource cheats, autoplay reads | `patch/bridge.rs` · `injectStoreBridge` |
| A4 | dispatch | `.useReducer(` + Provider value | **replaced at runtime** | all of autoplay | see below |
| A5 | stat table | `{total:{},click:{},warrior:{}` | preserved | autoplay decision quality | `patch/bridge.rs` · `injectStatsBridge` |
| A6 | slot registry | `{store:…,baseKey:` | preserved | active-slot detection | `patch/bridge.rs` · `injectStoreBridge` |
| A7 | DOM selectors | `data-testid=dialog-wrapper` etc. | — | dialogue, chapter switching | `web/autoplay/engine/dialog.js` |
| A8 | action names | `buy_generator`, `unlock_upgrade`… | — | buying, unlocking | `web/autoplay/engine.js` |

## A4 no longer depends on minified names

A4's confirmation step was the one place that keyed on a **minified identifier itself**,
and that is where the `$`-escaping bug happened. It now walks the React fiber tree up
from a DOM node and picks the Provider's value with no name involved. The bundle patch
remains only as a fallback.

```
found via fiber      function
found via regex      function
same object?         true      ← measured
```

Autoplay keeps working with `window.__bd_dispatch` deleted.

## There is no source map

The bundle ends with `//# sourceMappingURL=index-C5vCJZoP.js.map`, but the `.map` file
is not shipped — zero hits across all 643 bundle entries. A source map cannot remove
this coupling.

## The real remaining risk

Not name shortening, but **the game changing its shape**. If property names change or
object layouts differ, A1, A3, A5, and A6 break together. A source map would not
prevent that either.

So instead of preventing it, we make it **immediately visible**. Three ways, in
increasing depth:

```
npm run doctor          # all six anchors, ✔ or ✘, and what each failure costs
node tools/dry-run.js   # actually patch the bundle and syntax-check the result
BD_BUNDLE_JS=… cargo test --test bundle   # the same, through the shipped launcher
```

The last one is the one that matters before a release: it patches a real bundle with
the Rust code that actually ships, and checks the translated-string count against the
Node reference implementation. The two agreeing is what says the launcher is doing the
whole job rather than merely running.

The launcher also prints the same checklist at startup, so a broken anchor names
itself on the spot instead of showing up later as the game behaving oddly.

## A7 and A8 cannot be checked statically

They need the game running. Judge them by whether `DLG` and `UNL` lines appear in the
autoplay log. CI cannot see this far — a green CI means "the patch code is not
self-contradictory", not "it works on game 1.0.6".

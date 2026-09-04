---
layout: default
title: "Directory conventions"
description: "Where code goes in this repository and why — one responsibility per file, one place per decision."
lang: en
---

# Directory conventions

Where a file lives should tell you what it is responsible for.
When you are unsure where a new file goes, ask **who edits it** first.

| Directory | Who edits it | Rule |
|---|---|---|
| `locale/` | translators | Korean output only. No code |
| `web/` | developers | JS that runs **in the browser**, injected into the game page |
| `src/` | developers | the **launcher** (Rust). Runs outside the game |
| `patch/` | developers | bundle patching (Node reference implementation) |
| `tools/` | developers | things a human runs by hand |
| `generated/` | **nobody** | produced by `tools/`. Edit it and the next extraction erases you |
| `docs/` | developers | documentation, and the GitHub Pages source |

Most of `generated/` is in `.gitignore`. Anything extracted from the game does not go
in the repository.

## Do not mix code that runs in different places

Three kinds of code live here, and they fail in completely different ways.
Mixed together, you have to re-read a file to know where it even runs.

```
src/     launcher process   — logs to your terminal
web/     game renderer      — a syntax error leaves nothing in the launcher log
tools/   run by hand        — some need the game installed, some don't
```

Files under `web/` run inside the game, so they die silently. That is why CI runs
`node --check` over everything — it is the only net that code has.

## One responsibility per file

If you cannot say what a file does in one sentence, split it.
If the sentence needs an "and", it is already two.

### Launcher (`src/`)

```
main.rs           the entry point: argument reading and the run order. Nothing else
lib.rs            the module list, so tests/ can drive the patcher without the game
log.rs            log formatting
cli.rs            argument parsing
game/locate.rs    find the install, read its version
game/process.rs   detect a running instance, launch
cdp/client.rs     WebSocket, pairing requests with responses
cdp/fetch.rs      the interception loop
patch/scan.rs     brace-balance scanner (knows nothing about JS meaning)
patch/jsval.rs    reads a JS value literal into a serde_json::Value
patch/i18n.rs     find the English tables, merge Korean in
patch/css.rs      inject @font-face
patch/bridge.rs   store / dispatch / stats bridges
patch/mod.rs      assembles those into one bundle patch
assets.rs         what ships inside the binary
watchdog.rs       heartbeat, snapshots
```

`patch/scan.rs` knowing nothing about JS meaning is the point. Counting braces and
deciding what to patch are different jobs; entangled, neither is testable. Split, you
can check "does it get fooled by a `}` inside a string?" in six lines.

`patch/jsval.rs` is the same idea one level up. The i18n tables are object literals,
not JSON — bare keys, single quotes, and one `JSON.parse(`…`)` — and there is no JS
engine here to evaluate them. It refuses anything it does not understand rather than
guessing, because a silently mis-parsed table gets written back into the bundle.

## Testing what only the real bundle can show

The unit tests run against hand-written fixtures, which is the only way to state a
case precisely — and also why none of them would notice the real bundle drifting away
from an anchor. `tests/bundle.rs` closes that gap: it patches an actual decrypted
bundle and checks the translated-string count against the Node reference, every
anchor, and that the result is still valid JavaScript.

The bundle is the game's own code, so it cannot be committed. The test skips itself
unless one is pointed at:

```
node tools/dry-run.js
BD_BUNDLE_JS=%TEMP%/bd-dryrun/original-index-C5vCJZoP.js cargo test --test bundle
```

CI cannot run it. When the game updates, this is what tells you which anchor moved.

### Browser (`web/`)

`autoplay/engine.js` was 1,622 lines and 57 functions — past what one file can carry.
Game interpretation, valuation, self-calibration, planning, execution, dialogue, and
chapters all lived together. It is now 556 lines of wiring and one supervisor loop,
with every decision in a module of its own.

| File | Responsibility | Tests |
|---|---|---|
| `consts.js` | game constants read out of the bundle | — |
| `game.js` | the only code that touches the running game | via the smoke test |
| `action.js` | the one channel actions leave through | 14 |
| `cost.js` | purchase arithmetic | 8 |
| `resource.js` | production, upkeep, runway | 12 |
| `fire.js` | fire-breath casualties and survival | 16 |
| `special.js` | upgrades whose sign misleads the generic formula | 17 |
| `value.js` | what one more of a thing is worth | 14 |
| `calib.js` | prediction against measurement | 14 |
| `plan.js` | the ranked shortlist | 14 |
| `exec.js` | spending against that shortlist | 17 |
| `chapter.js` | chapter switching, repeat, production throttling | 18 |
| `dialog.js` | dialogue policy | 14 |
| `ready.js` | the generation-table latch | 9 |

The cheat widget was split the same way, for the same reason — it had reached 782
lines carrying six unrelated jobs.

| File | Responsibility | Tests |
|---|---|---|
| `widget/css.js` | the panel's stylesheet | — |
| `widget/format.js` | number formatting | 6 |
| `widget/store.js` | reaching the game's real per-slot state | 12 |
| `widget/upgrades.js` | moving upgrade levels | 12 |
| `widget/achievements.js` | keeping cheated progress off Steam | 7 |
| `widget/speed.js` | game speed, and backing off when it cannot keep up | 20 |

`engine.js` keeps only what is genuinely about assembly: handing modules their
dependencies, the three clocks, and the diagnostic surface on `window.__bd_auto`.

The browser has no module system. The launcher reads `web/autoplay/engine/*.js` in
name order and concatenates them ahead of `engine.js`. File boundaries are for humans
to read; they are not runtime boundaries.

Because of that, a module that fails to load produces a `TypeError` in the renderer,
where nothing reaches the launcher log. Two things guard against it: `engine.js` names
the missing files instead of dying, and `engine.smoke.test.js` loads the whole set the
way the launcher does — against a stub browser with no game behind it — which is the
only test that can catch a wiring mistake at all.

### Module rules

Every module **takes all of its dependencies as arguments**. It never reaches for the
game or the DOM directly — that is what makes it testable without the game, and those
tests run in CI.

```js
(function (root) {
  'use strict';
  function create(deps) { /* talks to the outside only through deps */ return { … }; }

  const api = { create };
  // The game runs Electron with node_integration, so `module` exists in the
  // renderer too. The common "if module exists, we're in Node" check is wrong here.
  if (typeof window !== 'undefined') (window.__bd_mod = window.__bd_mod || {}).name = api;
  else (root.__bd_mod = root.__bd_mod || {}).name = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));
```

Anything time-dependent takes `now` as a dependency, so behaviour like "pick the first
option after 30 seconds" can be checked deterministically.

Tests sit next to the module as `*.test.js`. Run them with `npm test`.

## Two implementations, one shape

`patch/` (Node) and `src/patch/` (Rust) do the same job, and their files are named to
match so the two can be read side by side:

```
patch/scan.js     src/patch/scan.rs     brace-balance scanning
patch/i18n.js     src/patch/i18n.rs     the English tables, merged with Korean
patch/bridge.js   src/patch/bridge.rs   store / dispatch / stats bridges
patch/css.js      src/patch/css.rs      @font-face injection
patch/bundle.js   src/patch/mod.rs      assembly, and nothing else
—                 src/patch/jsval.rs    reading a JS value literal
```

The one asymmetry is deliberate. Node has a JS engine, so `i18n.js` evaluates the
table literal; Rust has none, so `jsval.rs` parses it. That is the one place the two
can disagree, which is exactly what `tests/bundle.rs` checks on a real bundle — both
must report the same translated-string count.

## Naming

- File names are **nouns** — the thing the file is about (`process.rs`, `dialog.js`)
- Name it for what it is about, not what it does (`patcher.rs` ✗ → `bundle.rs` ✓)
- Never `utils`, `helpers`, `common`, `misc`. Those mean the responsibility was not decided

## One place per decision

Do not scatter path strings across files. `config.js`'s `PATHS` is the single source on
the Node side; `assets.rs`'s `include_*!` is the one on the Rust side. Moving a
directory should mean editing one file.

The same rule applies to judgements, not just paths. A "can we act right now?" check
was once spread across four call sites; fixing it in one place just moved the blockage
one step down, three times in a row. It is now `playable()`, in one place.

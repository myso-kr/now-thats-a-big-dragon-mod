---
layout: default
lang: "en"
code: "en"
title: "Now THAT'S a Big Dragon! — language patch, cheats, autoplay"
description: "Unofficial mod for the Steam idle game Now THAT'S a Big Dragon! - 22 language translations, an in-game cheat widget, and fully autonomous autoplay. Injected over the Chrome DevTools Protocol; no game files are modified."
native: "English"
english: "English"
share: 0
status: "source"
drawn: true
dialogs: 32
---

# Now THAT'S a Big Dragon! — mod

**[한국어 문서](ko/)** · [GitHub](https://github.com/myso-kr/now-thats-a-big-dragon-mod)

An unofficial mod for the Steam idle game *Now THAT'S a Big Dragon!*.
It does three things, and it does them **without touching a single game file**.

| | |
|---|---|
| **Language patch** | 22 languages, each 620 UI strings and 32 dialogue scripts, with pixel fonts matched to the game's own 6 px/em grid. Languages are *added* to the settings screen, so the choice stays the player's |
| **Cheat widget** (F8) | Resources, upgrades, game speed. Achievement submission is blocked by default |
| **Autoplay** (F9) | Buys units and upgrades, fights, answers dialogue, crawls dungeons and repeats chapters — unattended |

> ## ⚠️ Read this first
>
> **Unofficial fan-made mod.** Not affiliated with, endorsed by, or sponsored by the
> developer or publisher of *Now THAT'S a Big Dragon!*, or by Valve.
> All trademarks and copyrights belong to their respective owners.
>
> **Requires a legitimately purchased copy of the game.** This repository contains no
> original game text or assets. The translation cannot be applied without your own copy.
>
> **No game files are modified.** The launcher rewrites responses in memory only.
> Close it and the game is untouched — Steam's file integrity check passes.
>
> **Your save can break.** Cheats and autoplay can put the game into states it does not
> expect. Back up your save before the first run.
>
> **Steam achievements.** The cheat widget blocks achievement and stat submission by
> default. If you turn that off and use cheats, unearned achievements are permanently
> recorded on your Steam account.
>
> **A remote debugging port is opened.** The game is launched with
> `--remote-debugging-port=9223`. That port has no authentication: any other program on
> the same machine can attach, control the game, and read the screen. Enable it only
> while using the mod.
>
> **No warranty.** Provided as is. This repository will be taken down on request from
> the rights holder. (help@myso.kr)

## Install

Download the latest release, unzip, and run `bigdragon.exe` with the game closed.
There is **no runtime dependency** — you do not need Node.js.

[Latest release →](https://github.com/myso-kr/now-thats-a-big-dragon-mod/releases/latest)

Then, in game: **F8** for cheats, **F9** for autoplay.

## Supported game versions

| Game | Steam buildid | Bundle | Status |
|---|---|---|---|
| 1.1.0 | 25124954 | `index-DQTD9fhz.js` | Verified |
| 1.0.5b | 25111589 | `index-om7GP7rM.js` | Verified |
| 1.0.5 | 25092954 | `index-C5vCJZoP.js` | Verified |
| newer | — | — | Unverified. The launcher warns you |

This mod attaches to the game bundle's **internal structure**, so a game update can
break it. When something stops working, run this first — it diagnoses without
launching the game:

```
npm run doctor
```

It tells you which of the six anchors failed and what that breaks.
Paste its output into an issue and the diagnosis is mostly done.

## How it works

The game reads its own assets over a `gemshell://` custom protocol. The launcher
intercepts those responses at the Chrome DevTools Protocol `Fetch` stage — before the
bundle executes — so from the game's point of view the files were always like that.

```
launcher ──CDP──▶ game renderer
   │                  │
   │  intercepts:     ├─ assets/index-*.js   → i18n tables, flags and labels merged in
   │                  ├─ assets/style-*.css  → @font-face and the font stack injected
   │                  ├─ dialogs/*.ink       → translated dialogue served
   │                  ├─ fonts/bd-*          → font bytes served
   │                  └─ flags/*.png         → flag images served
   │
   └─ injects before document load: cheat widget, autoplay engine
```

Three bridges are patched into the bundle so the mod can read game state and issue
**real game commands** rather than poking at memory: `__bd_stores`, `__bd_dispatch`,
`__bd_stats`. Buying through the game's own dispatch means unlocks, achievements, and
side effects all behave normally.

## For contributors

- [Anchor catalogue](ANCHORS) — what the patch keys on, what breaks when it moves
- [Directory conventions](CONVENTIONS) — where code goes and why
- Tests run without the game: `npm test` (451 unit tests) and `cargo test`
- Translations are written under [`translations/`](https://github.com/myso-kr/now-thats-a-big-dragon-mod/tree/main/translations), one table per language

Translation fixes are welcome. You only need a screenshot — see the issue templates.

## License

Code is MIT. The translations are derivative works of the game's text and carry
**no license grant**; the fonts are CC BY 4.0 and SIL OFL 1.1. See
[NOTICE](https://github.com/myso-kr/now-thats-a-big-dragon-mod/blob/main/NOTICE).

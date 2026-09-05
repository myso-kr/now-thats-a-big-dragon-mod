# Changelog

Follows [Semantic Versioning](https://semver.org/).
Which game versions a release supports is recorded per release under "Supported game
versions" rather than in the version number, because the game and the mod move
independently — a game update that leaves the anchors intact gives the mod no reason
to change, and policy keeps changing while the game stands still.

## [0.5.1] - 2026-09-05

### Supported game versions

Unchanged from 0.5.0: 1.1.0 (25124954), 1.0.5b (25111589), 1.0.5 (25092954).

### Fixed
- **The launcher called a working font patch a failure.** Running the released
  binary is what found it: every other self-check passed while this one printed
  `FAIL fonts - 23/2 faces, 0 stacks`, and the patch it was checking was correct
  all along - in the running game `--font-primary` resolved to
  `everyday_standard, bd_ko_body, 'Malgun Gothic', sans-serif`. Two things had
  been left behind by the move from one language to twenty-two. The wanted count
  was the *active* language's fonts while the faces counted are every carried
  language's, so it compared 2 against 23 - a comparison that could not come out
  true again after the day it was written. And `stacks` was a pass condition, but
  it counts the game's own rules that name a font family directly and have to be
  pointed at the variable instead; a stylesheet that already routes everything
  through `--font-primary` leaves nothing to redirect, so zero is the right
  answer there rather than a fault. Nothing about the patch changed - only what
  the launcher says about it, which now reads
  `ok fonts - 23/23 faces, 22/22 language rules, 0 direct references redirected`

## [0.5.0] - 2026-09-05

### Supported game versions

| Game | Steam buildid | Bundle |
|---|---|---|
| 1.1.0 | 25124954 | `assets/index-DQTD9fhz.js` |
| 1.0.5b | 25111589 | `assets/index-om7GP7rM.js` |
| 1.0.5 | 25092954 | `assets/index-C5vCJZoP.js` |

1.0.5b changed three things — the bundle hash, the version string, and one dungeon
reset function. No anchor moved.

1.1.0 added the save-data screen and dungeon artifacts. It brought 49 new strings, one
of which was a **thirteenth i18n namespace (`artifacts`)** — and that broke the anchor
that had been matching the namespace list whole, right to its end. It now matches on
**containment**, so a fourteenth will not break it. (The Rust side already worked that
way; only the Node reference implementation was brittle.) Nine languages were compared
byte for byte on all three versions.

### Added
- **Multilingual patch** — Korean-only becomes multilingual. Languages are *added* to
  the game's own settings screen, flag, name and time units included. English and the
  five languages the game already ships are left alone
- 21 translations alongside Korean — 简体中文 (23.97%) · Русский (9.90%) ·
  Español (4.53%) · 日本語 (2.50%) · Polski (1.69%) · 繁體中文 (1.31%) · ไทย (0.89%) ·
  Español Latinoamérica (0.81%) · Українська (0.73%) · Italiano (0.61%) ·
  Čeština (0.54%) · Magyar (0.37%) · Tiếng Việt (0.29%) · Svenska (0.26%) ·
  Nederlands (0.25%) · Dansk (0.22%) · Bahasa Indonesia (0.16%) · Suomi (0.14%) ·
  Norsk (0.12%) · Română (0.12%) · Ελληνικά (0.06%). 620 UI strings and 32 dialogues
  each. All but Korean are marked `draft`: machine-written and reviewed against a
  player persona, but not yet read by a native speaker. Twenty-two languages in all,
  51.10% of Steam users
- **`translations/` — each translation's source moves into the repository.** Until now
  every language's table was a throwaway script in a scratch directory and only its
  *output* was committed. The same boilerplate was copied once per language, and in the
  meantime edits made in the exported worksheet were never carried back — so source and
  output had already drifted apart (274 strings in Spanish, 127 in Russian). Now
  `translations/<lang>/strings.py` (a `T` dict) and `dialogs.py` (an `F` dict) are pure
  data, and `tools/build-translation.py` is the only thing that opens a file. Each
  table's opening docstring records the judgements the output alone cannot recover: the
  address form (`tú` vs `usted`, `bạn`), where a speaker's register differs, and which
  punctuation the game's font simply does not have
- `npm run translations:check` — proves each table still reproduces what ships. It runs
  the real importer, compares against the committed JSON byte for byte, restores the
  file, and on a mismatch prints the **key** rather than a byte offset. CI runs it on
  every push
- **`tools/extend-font.py` — extending the game's own fonts.** The game's
  `Everyday_Standard` (6 px/em) and `High_Birth` (9 px/em) are VEXED's, under
  **CC BY 4.0**, so they may be modified and redistributed. The letters they lack are
  added here — 28 for the body face, 52 for the display face, **9 KB** in total,
  replacing two Galmuri files (746 KB). Most marks are taken out of the font itself
  (the ogonek from `ą`, the breve from `ğ`, the ring from `å`): what remains after
  subtracting a base letter from a composed one *is* the mark, and on a pixel grid that
  subtraction is exact. Marks the font has none of are derived from ones it has (a caron
  is a circumflex flipped about its own rows). Nothing is hard-coded to a coordinate, so
  the same rules run at 6 px and at 9 px. Czech, Polish and Hungarian now render in **one
  typeface**
- Mixed-alphabet detection — a Latin letter inside a Cyrillic word (the `y` in `гриндy`)
  is in the font too, so it draws perfectly and is simply the wrong spelling. No other
  check could see it, so `translate.js check` and `check-dialogs.js` now compare word by
  word
- System-font delegation (`systemScripts`) — characters no open pixel font covers, as
  with Thai, are left to the reader's own font. The catalogue records which ranges those
  are, so the checks can tell an agreed delegation from a missing glyph
- `locale/fonts/GAME-COVERAGE.json` — the code points the game's own fonts can draw.
  Without it a Latin-script language cannot be checked at all (Spanish bundles none of
  our fonts, so the only question is whether the game's font has `ñ`)
- 26 flag icons (`locale/flags/`) — one per language in `locale/languages.json`,
  flag-icons 4x3 SVG rasterised to 40×30 PNG. About 5 KB in total
- Fusion Pixel 8px and 10px (`zh_hans`, `zh_hant`, `ja`) — Chinese and Japanese pixel fonts
- `tools/check-fonts.js` — every character a translation uses has to exist in that
  language's font. It reads the woff2 cmap directly, so it runs in CI with no dependencies
- `tools/translate.js status` — per-language progress as a Markdown table; the README uses it
- CLDR plural support — Russian `_few` and `_many`, six forms for Arabic. `export` offers
  a row for every form the language actually uses, and `import` rejects any other
- Settings-screen integration in the Rust launcher — until now only the Node reference had it
- Integration tests comparing Node and Rust output against a real bundle, byte for byte
  (JS and CSS separately)
- **Ελληνικά** — the twenty-second language, and the first to need letters drawn rather
  than borrowed. The game's body font has no Greek and no bundled pixel font draws it on
  its six-pixel grid, so borrowing one would set every Greek word half again as tall as
  the digits beside it. All 67 letters of monotonic Greek were drawn into the game's own
  font instead: fourteen capitals and four lowercase are the same picture as a Latin
  letter and are aliased to it, and the other thirty-one follow Galmuri9's Greek redrawn
  to this font's metrics. Greek headings take Galmuri9, which draws Greek already except
  the seven accented capitals - those are composed the same way the Czech and Polish
  letters are. Twenty-two languages, 51.10% of Steam users
- **A site, in every language the mod speaks** (`docs/`, GitHub Pages). Twenty-three
  pages - English plus one per translation - generated by `tools/build-site.py` from
  `locale/languages.json` and the tables in `tools/site_*.py`, so a page appears exactly
  when its translation does. The chrome is looked up by the page's language the way the
  game's own i18n is, rather than being an English page with a translated headline on
  it, and the four warnings that can cost somebody something - the save, the
  achievements, the open debugging port, the absence of any warranty - are enforced
  present in all twenty-two languages before the build will write anything. Each page
  names every other in its `hreflang` cluster, including itself, so the set is symmetric
  by construction. The design is its own: a torch-lit cellar, with every colour sampled
  from the game's dungeon tiles and every size on the game's 6 px and 9 px type grids -
  `docs/DESIGN.md` records where each value came from
- **The site answers questions as well as ranking for them.** `robots.txt` welcomes the
  crawlers that answer as well as the ones that index; `llms.txt` states the facts worth
  quoting with the numbers generated from the repository; and each page carries
  `SoftwareApplication`, `HowTo` and `FAQPage` structured data whose answers are the
  very sentences the page shows a reader, so a quoted answer and the page cannot disagree
- **The dungeon plays itself, and the plan is one model rather than a pile of rules.**
  The floor is cells; some hold a thing that blocks the way and can be removed - a shut
  chest, a locked door, a monster. The route is planned on the floor with all of them
  gone, because all of them can be, and walked on the real one; wherever the real floor
  blocks the way, the first thing standing in it becomes the job. The order is the one
  that walks least, exact by held-karp up to nine chests, with the way out fixed as the
  end so the last chest is the one nearest home - the torch is a deadline, and an order
  chosen without that in mind finishes in the far corner and pays the width of the maze
  to come back
- Every dungeon run says what it did (`run over: 4/4 chests (golden key taken), 3/3
  doors, 99 actions`), and keeps a tick-by-tick trace of what it saw and what it pressed.
  Every fault below was found by reading one rather than guessing at it

### Fixed
- **The dungeon driver treated three different things as walls, and wrote its own
  targets off as more.** A locked door was in none of its name patterns, so it read as
  bare floor: the driver planned through one, walked into it, and recorded the cell as a
  wall for the rest of the run - and everything behind it, chests included, went quietly
  unreachable. A sleeping monster was skipped entirely, because the game's click handler
  is gated on `inBattle`; a corridor with one asleep in it cut the floor in half. And a
  step that moved nothing was taken as proof of a wall on the first try, so the first
  move of a run failing - which it does, because the game drops input during the entry
  animation - wrote off the one square out of the start
- **It stood in front of things instead of using them.** The click scan accepted chests
  and the way out and nothing else, so a driver that had walked the length of a floor to
  a door reported "nothing to click" and turned on the spot until the torch died. A
  sleeping monster is woken by being looked at, not by being stood beside - the game's
  own `isPlayerFacingEnemy(1.05) && startBattle()`. An opened way out is stepped through,
  not clicked: a run opened every chest, opened the door, and stood in front of it
- **It left dungeons it had just opened.** The game stops the crawl while a dialogue is
  up; the driver, seeing its moves refuse, concluded there was nowhere left to go and
  walked out. It now stands aside for the dialogue and keeps its place
- **The order dropped chests.** Held-karp's walk-back could truncate when a pair had no
  route, and the stops it lost were never looked at again - one run planned a single
  chest out of six and went home with five shut
- **A floor sealed behind a door there is no key for is now recognised, not ground
  against.** The game places doors on random corridor squares and checks nothing, and in
  a perfect maze every corridor square is a bridge - so a door beside the entrance seals
  the floor, and the grey keys that would open it are in the chests behind it. Nobody can
  finish that floor. The golden key is always in the first chest the game builds, so if
  that one is still shut the way out cannot open either: the driver leaves in two actions
  rather than sixty
- **Autoplay could buy only 12 of the 88 upgrades under the launcher that ships.**
  Unlocking is done by the game's UI click handler, not its reducer, so the tree stays
  shut unless `show_upgrade` and `unlock_upgrade` are sent as well - and sending them
  needs each upgrade's children and `unlockAt`. That came from a file
  `tools/extract-tree.js` wrote, and the file is derived from the game, so it is not
  committed: the Rust launcher never had it. Two smaller faults sat behind the same
  thing - the tool wrote to a path `config.js` did not read, so what shipped was
  whatever stale copy happened to be there; and `__bd_upgradeNames` and
  `__bd_levelNames` were injected by Node alone, leaving the Rust launcher's cheat
  widget showing raw ids. All three now ride in front of the patched bundle, and the
  tree is read out of the bundle both launchers are already patching, so it cannot go
  stale and cannot be missing. `A10` in the anchor catalogue; `doctor` and `dry-run`
  report it, and `dry-run` fails on it
- **The JS literal parser could not read a leading-dot number.** `.7` is how a minifier
  writes 0.7, and the upgrade tree contains one - so the whole tree failed to parse in
  Rust. Found by the byte comparison against Node the moment the two were asked to
  produce the same thing
- The upgrade tree was located by walking back to the nearest `{` before the anchor.
  That is the tree's own brace only while every branch declared ahead of `click` is
  empty, which is true today because `BUG_HIDE:[]` is first and holds nothing. One node
  in front of it and both launchers would have returned a single upgrade as though it
  were the whole tree. Candidates are now tried outwards until one has a `click` branch
- **Autoplay answered dialogue correctly in Korean only.** It chose an option by
  looking for a Korean substring, so in the other thirteen languages nothing matched:
  four of the eight branching dialogues held for thirty seconds and then took whatever
  came first, and the invasion silently paid the ransom instead of defending. The
  dialogue *id* was never the problem - the game's `start_dialog` event carries it and
  knows no language. Only the mapping from "the option I want" to "the option on
  screen" did. The option labels are now read out of the .ink files this mod writes,
  for whichever language is in play, and handed to the renderer; a policy names an
  option by its position in the file, which `check-dialogs.js` already guarantees is
  the same in every language. Both launchers build that table and CI compares them.
  The tests now run in five languages rather than one - they were all written in
  Korean too, which is why none of them noticed
- A stray space inside a Chinese option label (`[{resourceAmountLabel} 矿石 ]`). It was
  invisible in game and would have kept autoplay from recognising that option; the
  matcher trims now too, so the next one cannot cost anything either
- **The whole repository speaks English.** The Rust launcher already did; the Node
  launcher, the diagnostics, the cheat widget and the autoplay panel did not, so a
  Russian player got the game in Russian and the widget in Korean. The docs, the CI
  comments and the issue templates followed
- **Launching right after closing the game applied no patch** — a closing game leaves
  the process list before it lets go of the single-instance lock. Launching into that
  window makes the new process hand its arguments to the dying one and exit, so the
  launcher looks successful while waiting for a page that never loads. It now waits for
  the lock to be released
- **Flags rendered as broken images in the settings screen** — the Rust launcher never
  served the flag PNGs at all. The `flags ✔` line meant the entry had been inserted into
  the bundle, not that a file would be served. Node had its own half of this: it served
  only the *selected* language's flag, while the settings list shows every language at once
- **The dialogue box typed "Not found"** — once the game's language became `ko` it asked
  for `dialogs/ko/…`, and the matcher accepted only `en` paths, so the game's own handler
  returned a string that got typed out as dialogue. It now answers for every language
  folder we carry
- The language flag row did not wrap, so the settings window grew wider with each
  language added. `.language-flags` is now injected with `flex-wrap:wrap; min-width:0`
- **Galmuri does not contain simplified Chinese** — its 6,360 Han characters are the
  traditional forms used for Korean hanja, so 269 of the 867 characters the Chinese
  translation uses shipped as empty boxes. CJK languages moved to Fusion Pixel, and
  `check-fonts` went into `npm test` and CI so the same mistake cannot pass silently again
- `check-fonts` only examined characters above U+2000 — which exempted Cyrillic, Greek
  and extended Latin wholesale. It now examines everything outside ASCII
- The CI font step referenced `cfg.KOREAN_FONTS`, which no longer existed
- 18 tests in `lib/language.test.js` were missing from the `npm test` glob and had never run
- `tools/check-dialogs.js` checked only the first language — it now checks all of them
- Rust dropped translation-only keys (Russian `_few` and the like) when merging
- The Rust CSS patcher left the system-font fallback out of any slot with no font of ours
- Rust's `@font-face` declaration order and percentage formatting differed from Node's
- A fresh profile still started in English — it now follows the system language

## [0.4.0] - 2026-09-04

### Supported game versions

| Game | Steam buildid | Bundle |
|---|---|---|
| 1.0.5 | 25092954 | `assets/index-C5vCJZoP.js` |

### Added
- **A single executable** — the Rust launcher. Node is no longer needed (1.3 MB, no dependencies)
- **Tag-driven releases** — `git tag v*` builds the Windows and Linux binaries
- `npm run doctor` — a diagnostic report without starting the game. Paste its output into an issue
- `npm run fingerprint` — records verified game versions and bundle hashes
- `docs/ANCHORS.md` — the anchor catalogue: what dies when one breaks, and where to fix it
- `docs/CONVENTIONS.md` — directory conventions and module rules
- Autoplay chapter repetition (stop / repeat / next chapter, with a chapter to repeat)
- 61 unit tests for the injected scripts — they run without the game

### Fixed
- **dispatch is found through the React fiber** — the one anchor that depended on a
  minified identifier is now a runtime search, and survives a rebuild of the game
- A `$` in a minified identifier made the dispatch bridge miss, killing autoplay entirely
- A duplicate `stats` key in `patchBundle` printed the translation count as `undefined/undefined`
- **Upgrade unlock signals** — `show_upgrade` and `unlock_upgrade` are emitted in the same
  order the UI does. Without them only 12 of the 88 upgrades could be bought
- Affordability is judged by `status`, not `isUnlocked` — the latter is for generators and
  is almost always false on an upgrade
- Running out of a resource no longer halts autoplay; it locks the purchase of consuming
  units only, so the producers stay ungated and the situation recovers itself
- Autoplay stalled forever in a `dialog` context that had no dialogue
- `tools/eval.js` required an undeclared `ws` package

### Housekeeping
- Split the directories into `locale/`, `web/` and `generated/` — divided by who edits them
- Nothing extracted from the game (English source text, the upgrade tree) is committed
- Added `LICENSE` (MIT), `NOTICE` and `THIRD-PARTY.md`

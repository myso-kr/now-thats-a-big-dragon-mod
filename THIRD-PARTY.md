# Third-party components

## Runtime dependencies

**None.**

- The Rust launcher uses only `tungstenite`, `serde`, `serde_json`, `regex` and
  `base64` (see `Cargo.toml`). No async runtime was brought in.
- The Node reference implementation uses only what Node 22+ has built in (WebSocket,
  fetch, `node:*`). `package.json` has no `dependencies`.

## Bundled assets

### Galmuri (갈무리) — Korean

- Files: `locale/fonts/Galmuri7.woff2`, `Galmuri9.woff2`, `Galmuri11.woff2`
- Copyright: Copyright (c) 2019-2025 Lee Minseo (quiple@quiple.dev)
- Licence: SIL Open Font License, Version 1.1
- Full text: `locale/fonts/OFL-Galmuri.txt`
- Source: <https://github.com/quiple/galmuri>
- Version: 2.404 (per the font's own name table)

  ```
  c372bb36f06c35b183216709beea7f0db2e70f09eebff964874c4347520a12de  Galmuri7.woff2
  bea397545086f0d2e3652563746783c679c9f38190a1aecee3c9412c9d6c5d14  Galmuri9.woff2
  8bad9322b3340bfb5cb26cb00f4752bf4c8e7d1b526bb07205f4af458eebed31  Galmuri11.woff2
  ```

These are the complete fonts, not subsets. Coverage as measured with fontTools:

| File | Glyphs | Hangul | Kana | Han |
|---|---|---|---|---|
| Galmuri7 | 20,151 | 11,172 | 187 | 6,360 |
| Galmuri9 | 20,714 | 11,172 | 187 | 6,375 |
| Galmuri11 | 20,968 | 11,172 | 187 | 6,477 |

**Those 6,360 Han characters are the traditional forms used for Korean hanja.** Reading
this table as evidence that one font covers Korean, Chinese and Japanese together was
wrong, and it was written here. There are no simplified characters in it, so 269 of the
867 characters the Simplified Chinese translation uses came out blank — Galmuri is now
used for Korean only. So the same mistake cannot pass silently again,
`tools/check-fonts.js` compares the characters a translation actually uses against the
font's cmap.

`Galmuri11.woff2` is not used by the current defaults. It is kept as an option for
anyone who wants to try a different size.

### Everyday Standard and High Birth (the game's own fonts, extended)

- Files: `locale/fonts/Everyday_Standard-bd.woff2`, `High_Birth-bd.woff2`
- Original copyright: VEXED
- Licence: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
- Full text: <https://creativecommons.org/licenses/by/4.0/>
- Source: <https://v3x3d.itch.io/everyday-standard> · <https://v3x3d.itch.io/high-birth>
- Original version: Everyday_Standard 1.3, High_Birth 1.0 (as bundled in the game's assets)

  ```
  69f8a060cc2e563fed6df33cda8a5844feda87d1676b22ad63c103311c7ee774  Everyday_Standard-bd.woff2
  7b8a74f1c3668a8ac44082fdd567f0ec49c9e54d2da93b81b8e026869c49dff9  High_Birth-bd.woff2
  ```

**Statement of changes (required by CC BY 4.0).** 28 glyphs were *added* to the
original — the ones Czech, Hungarian and Romanian need:
`Č č Ď ď Ě ě Ň ň Ř ř Š š Ť ť Ů ů Ž ž Ő ő Ű ű Ă ă Ș ș Ț ț`.
No existing glyph was touched, and no table beyond metrics, spacing and names was
changed either. The fonts carry a `-bd` suffix in their name to distinguish them from
the originals. `python tools/extend-font.py <the game's font directory>` regenerates
them exactly.

Most marks are taken out of the original itself — the ogonek from `ą`, the breve from
`ğ`, the ring from `å`, the dot from `ż`. What remains after subtracting a composed
character's own base letter *is* the mark, and on a pixel grid that subtraction is
exact. Only two marks had to be made: the caron and the double acute, and both are
derived from the original's circumflex and acute (the caron is a circumflex flipped
about its own rows; the double acute is two upright ticks on the acute's rows). So
nothing drifts away from the original's forms.

**Why not a third-party font.** The game's body font is 6 pixels per em. Matched to it,
LanaPixel (11 px/em) and Galmuri7 (8 px/em) render capitals 17% too large, and Fusion
Pixel 8px renders lowercase 20% too small. Letterforms splitting inside a single word is
a problem only extending the same font makes go away. The two files together are 9 KB,
replacing two Galmuri files at 746 KB.

### Fusion Pixel Font (缝合怪像素字体) — Chinese and Japanese

- Files: `locale/fonts/FusionPixel8-{zh_hans,zh_hant,ja}.woff2`,
  `FusionPixel10-{zh_hans,zh_hant,ja}.woff2`
- Licence: SIL Open Font License, Version 1.1
- Full text: `locale/fonts/OFL-FusionPixel.txt`
- Source: <https://github.com/TakWolf/fusion-pixel-font>
- Version: 2026.09.01

  ```
  6411ee6042b2d9233727927addb701c1503541787f27562c5d4522ed2f5f02d3  FusionPixel8-zh_hans.woff2
  f78faebc3fa256b982b254e6cc856883dedadab030cf4259aec794ce4438d931  FusionPixel8-zh_hant.woff2
  d243592ecf44670926785546a099742697c64bca7aa2893fd1d29e790daa9ce8  FusionPixel8-ja.woff2
  c94825b0a58528af68115a7ede98682a38af53c07e624409a8274082f05b2195  FusionPixel10-zh_hans.woff2
  430de421bed0a9766f9080df0e946327d3432002b236a33e3cb93218d0361f12  FusionPixel10-zh_hant.woff2
  28c5986fd541a12a9db3324f1be295935179a380888cbfe46599060b72ac661a  FusionPixel10-ja.woff2
  ```

Fusion Pixel is itself stitched together from several OFL pixel fonts. The upstream
licence texts are bundled too:

| Upstream | Full text | Source |
|---|---|---|
| Ark Pixel (方舟像素字体) | `locale/fonts/OFL-ArkPixel.txt` | <https://github.com/TakWolf/ark-pixel-font> |
| Boutique Bitmap 9x9 | `locale/fonts/OFL-BoutiqueBitmap.txt` | <https://github.com/scott0107000/BoutiqueBitmap9x9> |
| Galmuri | `locale/fonts/OFL-Galmuri.txt` | see above |

Coverage as measured — `-zh_hans`, `-zh_hant` and `-ja` cover the same characters and
differ only in the regional forms:

| File | Glyphs | Hangul | Kana | Han |
|---|---|---|---|---|
| FusionPixel8-* | 27,689 – 27,693 | 11,224 | 177 | 14,717 |
| FusionPixel10-* | 24,839 – 24,840 | 11,266 | 189 | 10,570 |

The 8px cut is 8 pixels per em and the 10px cut is 10 — the same grids as Galmuri 7 and
9 respectively. So the `pxPerEm` and `ascentOverride` values used for Korean carry over
unchanged and only the file is swapped: neither the letter size nor the line height moves.

### OFL compliance note

The licence texts are bundled, the copyright notices are intact, and the fonts are not
sold on their own. No copyright line declares a Reserved Font Name, so there is no
naming constraint. The CSS names `bd_body` and `bd_heading` are stylesheet aliases and
do not modify the font files themselves. The file names were changed when they were
copied in.

The distribution (the zip on GitHub Releases) carries the `OFL-*.txt` files too — the
release workflow copies them into `licenses/`.

Integrity can be verified with `sha256sum locale/fonts/*.woff2`.

## Identifiers from inside the game, referenced for interoperability

`patch/bundle.js` and `src/patch/` use short fragments of code as regex patterns to
locate particular places in the game's bundle.

| What it matches on | Example |
|---|---|
| Namespace names | `upgrades`, `common`, `statistics` … |
| String literals | `savePrefix` |
| Object property names | `{total:{},click:{},warrior:{}`, `{store:…,baseKey:` |
| Numeric literals | `{seconds:1,…,years:31536e3}` |

These are the minimum functional identifiers interoperability requires; no game code or
text is reproduced. `docs/ANCHORS.md` has the full list.

### flag-icons

- Files: `locale/flags/*.png`
- Licence: MIT
- Source: <https://github.com/lipis/flag-icons> (v7.3.2, `flags/4x3`)
- Changes: the original SVGs were rasterised to 40×30 PNG and quantised to a 64-colour palette

The game's own flags are 40px-wide indexed-palette PNGs, and its CSS displays them at
`width:32px; height:24px; object-fit:cover` — so the ratio that reaches the screen is
4:3. That is why the `4x3` set is used: it crops rather than stretches, so nothing is
distorted.

There are 26 at present, one for every language in `locale/languages.json`, about 5 KB
in total.

`locale/flags/SOURCES.json` records the hash of each original SVG, and
`python tools/make-flags.py` regenerates them exactly (needs `pip install resvg-py
pillow`). The script is not part of the build — a person runs it when a language is added.

A flag marks a language, not a country. Languages and countries are not one to one, so
which flag to use is a judgement rather than a lookup.

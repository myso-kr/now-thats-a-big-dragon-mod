---
layout: default
title: "The site's design"
description: "Where every colour, size and font on this site came from - each one traceable to the game or to this repository."
lang: en
code: en
---

# The site's design, and where every value in it came from

This is the source of truth for `docs/` — the GitHub Pages site. Anything that sets a
colour, a size or a font on that site takes it from here, and every value here is
traceable to something in the game or in this repository. Nothing is chosen because it
is fashionable.

The site exists to be found. It is the mod's front door in twenty-two languages, and
the reason it is worth designing at all is that a player searching in Greek or Polish
for a way to read this game in their own language should land somewhere that is already
in it.

## The motif: the page is the specimen

The mod's whole trade is *letters*. It draws characters into the game's own pixel fonts
so that a Czech `š` and a Greek `Ω` sit on the same six-pixel grid as the digits beside
them — 123 of them added to `Everyday_Standard` alone. The one design nobody else could
make for this project is the one that puts those letters on the page and lets them
argue for themselves.

So the site is set in the fonts the mod ships. A visitor reading the Greek page is
reading letters this repository drew. That is the product, demonstrated rather than
described.

Where a script has no pixel font small enough to bundle — Japanese, Korean, Chinese,
Thai, Vietnamese all need thousands of glyphs and megabytes — the page falls back to
the reader's own system font. That is not a gap to hide: the same honesty is in the
launcher, which tells you when a language is drawn by the system font rather than ours.

## Colour

Taken from the game's own dungeon tiles, sampled with Pillow from
`dungeon-crawler/tiles/*.png` inside the game's asset bundle. It is a torch-lit cellar:
a plum-black ground, violet stone, and one warm light. The neutrals are already biased
towards violet, which is why they read as chosen rather than as a default grey.

| token | value | where it comes from |
|---|---|---|
| `--ground` | `#17111a` | the darkest tile pixel in the set, 1163 of them - the floor of the dungeon |
| `--stone` | `#3b2c4a` | the wall tiles' body |
| `--brick` | `#421f26` | the darker brick course |
| `--brick-lit` | `#662d39` | brick with the torch on it |
| `--mortar` | `#6e516a` | the mortar between stones, and the site's muted text |
| `--pale` | `#aa8c94` | the lightest stone |
| `--parchment` | `#dfcbbf` | body text on dark - the chest's own paper colour |
| `--ember` | `#ae5b39` | the accent's shadow |
| `--torch` | `#e89e56` | **the accent.** The one warm light in a dark corridor |
| `--gold` | `#ffdc6a` | the golden key and the open chest. Reserved for the single most important thing on a page, which is the download |
| `--moss` | `#4a7a47` | four pixels in the whole set. Used only for "yes, this works" |

Two rules keep it from becoming noise:

- **One accent.** `--torch` marks what the reader should do next. `--gold` appears once
  per page at most. Everything else is ground, stone and parchment.
- **Semantic colour is separate from the accent.** `--moss` for a passing check,
  `--brick-lit` for a warning. Neither is used decoratively.

### Both themes

The page renders in the reader's theme. Dark is the design's home - it is a dungeon -
but light is not an afterthought: the same palette inverts around parchment, with
`--ground` becoming the text colour. Every colour is declared as a token on bare
`:root` first, so the un-stamped "system" state (which is most readers) resolves
correctly, and the dark and light blocks only ever *redefine* tokens.

## Type

The two faces are the game's own, extended by `tools/extend-font.py` and shipped in
this repository:

| role | face | grid | crisp at |
|---|---|---|---|
| display | `High_Birth-bd` | 9 px/em | 18px, 27px, 36px, 45px |
| body | `Everyday_Standard-bd` | 6 px/em | 12px, 18px, 24px |

**The type scale is not a taste.** A pixel font drawn on a six-pixel em box is only
sharp at integer multiples of six; at 17px it is a smear. So the body scale is 12 / 18 /
24 and the display scale is 18 / 27 / 36 / 45, and there are no sizes between them.
`font-smooth: never` and `-webkit-font-smoothing: none` keep the renderer from softening
what the grid made sharp.

Line height is a whole number of pixels for the same reason: 18px body text sits on a
24px line, 12px on 18px.

`Everyday_Standard-bd.woff2` is 4 KB and carries Latin, Cyrillic, Greek and the 123
letters this mod added. `High_Birth-bd.woff2` is 5 KB. Two files cover every language on
the site whose script they know, and no page loads a font it cannot use.

## Space

One unit, and it is the em box: **6px**. Everything is a multiple, which is what keeps a
pixel grid from drifting.

`--s1: 6px` · `--s2: 12px` · `--s3: 18px` · `--s4: 24px` · `--s6: 36px` · `--s8: 48px` ·
`--s12: 72px`

Borders are `2px` and square. `border-radius: 0` everywhere - the game's own stylesheet
sets `--default-border-radius: 0`, and a rounded corner on a pixel grid is a lie about
where the pixels are.

## The pages

Twenty-two languages, 51.10% of Steam users. One page each, plus English as the root.

```
docs/index.md          en   x-default
docs/<code>/index.md   the language's own
```

Every page carries, in its `<head>`:

- a **self-referencing** `hreflang` - the page must appear in its own cluster, and the
  commonest hreflang fault is leaving it out
- an `hreflang` for **every** sibling, and they are reciprocal by construction because
  one template writes them all
- `hreflang="x-default"` pointing at the English root
- a canonical that matches the URL the cluster names, because an hreflang set that
  points at non-canonical URLs is ignored

The codes are the ones already in `locale/languages.json`, which are the codes the game
and the mod use: `zh-Hans`, `zh-Hant`, `es-419`, `nb` and the rest. They are valid BCP
47 and they are the same strings the launcher matches on, so there is one list, not two.

### What each page says

The same three things the mod does, in that language, with that language's own numbers:
how many of its strings and dialogues are translated, and which font draws it. A page
that claims a translation should be able to show its own progress.

## What this is not

No gradient hero, no rounded cards, no emoji as section markers, no 100vh opener. The
game is drawn on a grid of squares and so is this. If a choice here cannot be traced to
the game's art, the fonts' metrics, or a documented SEO requirement, it does not belong
in this file.

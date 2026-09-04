# translations/

The source each shipped translation is generated from. One directory per language
code, matching `locale/languages.json`.

| file | defines | generates |
| --- | --- | --- |
| `<lang>/strings.py` | `T` — a flat dict of i18n key to text | `locale/i18n.<lang>.json` |
| `<lang>/dialogs.py` | `F` — a dict of `<name>.ink` to file body | `locale/dialogs/<lang>/` |

Neither file reads arguments, opens anything, or knows where its output goes. That
is `tools/build-translation.py`, which does it once for every language instead of
each script carrying its own copy — which is what they used to do, and how they
drifted apart from the files they were supposed to produce.

```
python tools/build-translation.py vi          # build one language
npm run translations                          # build all of them
npm run translations:check                    # build nothing, report drift
```

`--check` is the part that matters. It runs the table through the real importer,
compares the result against the JSON that ships, restores the file, and fails if they
differ — naming the key, not a byte offset. A string edited in the exported worksheet
and never carried back into the table would otherwise be silently undone by the next
build. CI runs it on every push.

## Adding a language

1. `node tools/translate.js export <lang> > work.tsv` — a worksheet with a row per
   string, including one per plural form *that language* uses, not the two English has.
2. Write `translations/<lang>/strings.py`: a `T` dict keyed by the worksheet's first
   column. Notation-only values (`+`, `%`, `//`, the empty string) are supplied by the
   driver, so leave them out.
3. Copy `locale/dialogs/en/` into `translations/<lang>/dialogs.py` as `F`, and
   translate the prose and the bracketed choice labels only. Tags (`# speaker:`,
   `# pace:`), knots, variables, diverts and `{interpolations}` are the game's own
   and must survive unchanged — `tools/check-dialogs.js` enforces that.
4. `python tools/build-translation.py <lang>`
5. `node tools/check-fonts.js <lang>` — every character used has to exist in the
   font that language ships with. This is not advisory: 269 simplified Chinese
   characters once shipped as blank boxes because nothing checked.
6. `node tools/check-dialogs.js <lang>` and `node tools/translate.js check <lang>`.

## The docstring is part of the source

Each file opens with the decisions a translator made and a reviewer would otherwise
have to reverse-engineer: the address form (`tú` vs `usted`, `ty` vs `wy`, `bạn`),
whether a speaker's register differs from the rest, and which punctuation the game's
6 px/em font simply does not have — no `«»`, no em dash, no curly apostrophe, so
straight quotes and hyphens throughout.

## Languages with no table

`ko`, `es-419`, `zh-Hans` and `zh-Hant` have a `dialogs.py` but no `strings.py`, and
the driver reports `strings: source is the JSON` for them. That is accurate rather
than a gap:

- **ko** was written first and directly, before the worksheet existed.
- **es-419** was derived from the Castilian text — `vosotros` and peninsular
  vocabulary replaced with Latin American forms — not translated again.
- **zh-Hant** was converted from `zh-Hans` with OpenCC's `s2twp`, then read through.

Generating a `strings.py` for these would be a copy of the JSON, not a source: a
second place to edit, with nothing gained. `node tools/translate.js check <lang>`
covers them.

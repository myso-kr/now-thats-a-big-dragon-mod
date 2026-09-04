# -*- coding: utf-8 -*-
"""Cuts each language's webfont down to the characters it actually uses.

    python tools/build-webfonts.py            # every language
    python tools/build-webfonts.py ko vi      # just these
    python tools/build-webfonts.py --check    # rebuild nothing, report drift

Until now every language pointed at the same two URLs - fonts/bd-body.woff2 and
fonts/bd-heading.woff2 - so only one language's font could ever be loaded. Switching
language in the settings screen kept whichever font was there: a Korean player who
switched to Simplified Chinese kept Galmuri, which has none of the simplified
characters, and got 269 empty boxes. Giving each language its own URL is what lets all
fourteen be declared at once and picked by `html[lang]`.

Fourteen whole fonts would be several megabytes. They do not need to be whole: the
translation is written, so exactly which characters it uses is known, and
`tools/check-fonts.js` already computes that set for its own coverage check. Galmuri7
is 309 KB of 20,151 glyphs; Korean uses 655 of them.

The game's own two faces are never subset - they are not ours to cut down, and the
extended ones already carry only the letters that were added.
"""
import argparse
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "locale" / "fonts"
# Beside the sources, so nothing else has to learn a new directory.
OUT = FONTS

# Always kept, whatever the text says it needs. A missing space or digit is not
# something a translation's character list would mention, and the UI is full of both.
ALWAYS = set(" 0123456789.,:;!?()[]%+-/×·…'\"") | {chr(0x00A0)}


def characters(lang):
    """The characters a language's translation uses, from the checker that already knows."""
    out = subprocess.run(
        ["node", "-e", "process.stdout.write(JSON.stringify([...require('./tools/check-fonts')"
         f".charactersOf({json.dumps(lang)})]))"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode:
        sys.exit(out.stderr.strip() or f"could not read the characters {lang} uses")
    return set(json.loads(out.stdout)) | ALWAYS


def catalogue():
    return json.loads(io.open(ROOT / "locale" / "languages.json", encoding="utf-8").read())


def subset(src, dst, chars):
    """Keep only `chars`, and keep the metrics the CSS depends on."""
    from fontTools import subset as fts
    from fontTools.ttLib import TTFont

    font = TTFont(src)
    opts = fts.Options()
    # The layout tables can go; what must not is anything the @font-face metric
    # overrides are computed against, which lives in hhea and OS/2.
    opts.layout_features = []
    opts.name_IDs = ["*"]
    opts.name_legacy = True
    opts.notdef_outline = True
    opts.recalc_bounds = False
    opts.drop_tables += ["GSUB", "GPOS", "GDEF", "kern", "morx"]
    sub = fts.Subsetter(options=opts)
    sub.populate(unicodes=[ord(c) for c in chars])
    sub.subset(font)
    font.flavor = "woff2"
    dst.parent.mkdir(parents=True, exist_ok=True)
    font.save(dst)
    font.close()
    return dst.stat().st_size


def slot_name(lang, replaces):
    """`bd-ko-body.woff2` - one URL per language per slot, which is the whole point."""
    part = "body" if replaces == "everyday_standard" else "heading"
    return f"bd-{lang}-{part}.woff2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*")
    ap.add_argument("--check", action="store_true", help="report what would change")
    args = ap.parse_args()

    cat = catalogue()
    langs = args.langs or [
        c for c in cat["languages"]
        if (ROOT / "locale" / f"i18n.{c}.json").exists()
    ]

    total = 0
    rows = []
    for lang in langs:
        entry = cat["languages"].get(lang)
        if not entry:
            sys.exit(f"no catalogue entry for {lang}")
        fonts = [f for f in entry.get("fonts", []) if f.get("replaces")]
        if not fonts:
            rows.append(f"{lang}: the game's own fonts cover it")
            continue
        chars = characters(lang)
        for f in fonts:
            src = FONTS / f["file"]
            if not src.exists():
                sys.exit(f"{lang}: {src} is missing")
            dst = OUT / slot_name(lang, f["replaces"])
            if args.check:
                rows.append(f"{lang}: {dst.name} <- {f['file']} ({len(chars)} characters)")
                continue
            size = subset(src, dst, chars)
            total += size
            rows.append(f"{lang}: {dst.name} {size // 1024} KB"
                        f" from {f['file']} {src.stat().st_size // 1024} KB"
                        f" ({len(chars)} characters)")

    for r in rows:
        print(r)
    if not args.check:
        print(f"\n{total // 1024} KB in total, into {OUT.relative_to(ROOT)}")


main()

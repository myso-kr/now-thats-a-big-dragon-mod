"""Records which characters the game's own two fonts can draw.

`check-fonts.js` needs this. Without it a Latin-script translation cannot be checked
at all: Spanish ships no font of ours, so the only question is whether the game's own
font has `ñ` and `¿` — and that question has an answer, we just have to write it down.

What is committed is a list of code points, not the fonts. The fonts are the game's;
their coverage is a fact about the game, the same kind of fact as the anchors in
docs/ANCHORS.md.

Run this only when the game updates, against fonts extracted from its asset bundle:

    pip install fonttools
    python tools/make-game-coverage.py <dir with Everyday_Standard.ttf, High_Birth.ttf>
"""

import json
import pathlib
import sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "locale" / "fonts" / "GAME-COVERAGE.json"

# The base family name in the stylesheet -> the file inside the bundle.
FONTS = {
    "everyday_standard": "Everyday_Standard.ttf",
    "high_birth": "High_Birth.ttf",
}


def ranges_of(code_points) -> list:
    """Runs of consecutive code points, which is most of what a font's cmap is."""
    out: list = []
    for c in sorted(code_points):
        if out and c == out[-1][1] + 1:
            out[-1][1] = c
        else:
            out.append([c, c])
    return out


def main() -> int:
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("needs: pip install fonttools", file=sys.stderr)
        return 2

    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    src = pathlib.Path(sys.argv[1])

    out = {
        "_": "What the game's own two fonts can draw. Code points only — the fonts "
             "themselves are the game's and are not redistributed here. Regenerate "
             "with tools/make-game-coverage.py.",
        "game": sys.argv[2] if len(sys.argv) > 2 else "1.0.5",
        "fonts": {},
    }
    for base, name in FONTS.items():
        path = src / name
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            return 1
        cps = list(TTFont(path).getBestCmap())
        r = ranges_of(cps)
        out["fonts"][base] = {"file": name, "chars": len(cps), "ranges": r}
        print(f"{base:20s} {len(cps):5d} chars, {len(r):4d} ranges")

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", "utf-8")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

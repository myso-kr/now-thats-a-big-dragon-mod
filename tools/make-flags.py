"""Builds the flag icons for the languages this mod adds to the game's settings.

The game's own flags are small indexed-palette PNGs 40px wide, and its CSS shows
every one of them at 32x24 with `object-fit: cover` — so 4:3 is the ratio that
actually reaches the screen. flag-icons' 4x3 set matches that exactly, and its SVGs
crop rather than stretch, so nothing is distorted.

Run this only when adding a language. The PNGs it produces are committed; this is
not part of the build.

    pip install resvg-py pillow
    python tools/make-flags.py

Source: https://github.com/lipis/flag-icons (MIT). See THIRD-PARTY.md.
"""

import hashlib
import io
import json
import pathlib
import sys
import urllib.request

VERSION = "7.3.2"
BASE = f"https://cdn.jsdelivr.net/npm/flag-icons@{VERSION}/flags/4x3"

# Which flag each language gets is a judgement call — a language is not a country,
# and the flag is only a recognisable label. That call is recorded once, in
# locale/languages.json, and read from there: adding a language should be one edit,
# not two that can drift apart.
CATALOGUE = pathlib.Path(__file__).resolve().parent.parent / "locale" / "languages.json"


def wanted() -> dict:
    """flag-icons country code -> the language code that uses it."""
    catalogue = json.loads(CATALOGUE.read_text("utf-8"))
    out = {}
    for lang, entry in catalogue["languages"].items():
        f = entry.get("flagFile")
        if f:
            out.setdefault(f.removesuffix(".png"), lang)
    return out


# 40px wide is the game's own convention; 4:3 is what its CSS displays.
WIDTH, HEIGHT = 40, 30

OUT = pathlib.Path(__file__).resolve().parent.parent / "locale" / "flags"


def main() -> int:
    try:
        import resvg_py
        from PIL import Image
    except ImportError:
        print("needs: pip install resvg-py pillow", file=sys.stderr)
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"source": BASE, "license": "MIT", "size": [WIDTH, HEIGHT], "files": {}}

    for code, lang in sorted(wanted().items()):
        url = f"{BASE}/{code}.svg"
        with urllib.request.urlopen(url, timeout=30) as r:
            svg = r.read()

        png = resvg_py.svg_to_bytes(
            svg_string=svg.decode("utf-8"), width=WIDTH, height=HEIGHT
        )
        img = Image.open(io.BytesIO(bytes(png))).convert("RGBA")

        # Flatten onto white: the game's flags have no transparency, and a palette
        # PNG with alpha costs more bytes for nothing.
        flat = Image.new("RGB", img.size, (255, 255, 255))
        flat.paste(img, mask=img.split()[3])

        # An adaptive palette, as the game's own flags use. Small and lossless enough
        # at this size.
        out = flat.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
        path = OUT / f"{code}.png"
        out.save(path, optimize=True)

        data = path.read_bytes()
        manifest["files"][f"{code}.png"] = {
            "language": lang,
            "svgSha256": hashlib.sha256(svg).hexdigest(),
            "pngSha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        }
        print(f"{code}.png  {WIDTH}x{HEIGHT}  {len(data):>5} B  -> {lang}")

    (OUT / "SOURCES.json").write_text(json.dumps(manifest, indent=2) + "\n", "utf-8")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""The social preview card, drawn in the game's own font on the game's own grid.

A link to this project gets pasted into Discord and Slack and a search result, and what
those show is one 1200x630 image. Rendering it in some other typeface would make the one
picture of this project the one place its own rules do not apply.

So it is drawn the way the site is: the palette from `docs/DESIGN.md`, sampled from the
game's dungeon tiles, and the text set in `Everyday_Standard-bd` - the extended copy of
the game's own body face - at exact multiples of its 6 px/em box. The card is composed
at 400x210 and scaled by 3 with nearest-neighbour, so every pixel in the output is a
whole design pixel and no stroke is ever half-lit.

Text is placed by its measured box rather than by eye: at 6 px/em the font's own ascent
sits well above its capitals, so `d.text((x, y))` would leave each line floating a third
of its height below where it was asked for, and the gaps between lines would all be
wrong in different ways.

    python tools/build-og-image.py        writes docs/assets/og.png
"""

import io
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "og.png"

SCALE = 3                      # one design pixel is three screen pixels
W, H = 1200 // SCALE, 630 // SCALE

# docs/DESIGN.md, which sampled these from the game's dungeon tiles.
GROUND = (0x17, 0x11, 0x1A)
SURFACE = (0x1E, 0x16, 0x22)
LINE = (0x2F, 0x23, 0x36)
BRICK = (0x42, 0x1F, 0x26)
STONE = (0x3B, 0x2C, 0x4A)
TORCH = (0xE8, 0x9E, 0x56)
GOLD = (0xFF, 0xDC, 0x6A)
PARCHMENT = (0xDF, 0xCB, 0xBF)
MORTAR = (0x6E, 0x51, 0x6A)
MOSS = (0x4A, 0x7A, 0x47)


def face(px):
    """Our own body font, as something PIL can set type with.

    PIL reads TrueType, not woff2, so the wrapper comes off in memory rather than a
    second copy of the font being committed beside the first. A fresh buffer each call:
    FreeType keeps the handle, and a spent one cannot be read twice.
    """
    from fontTools.ttLib import TTFont

    f = TTFont(ROOT / "locale" / "fonts" / "Everyday_Standard-bd.woff2")
    buf = io.BytesIO()
    f.flavor = None
    f.save(buf)
    buf.seek(0)
    return ImageFont.truetype(buf, px)


def main():
    img = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(img)

    def line(x, top, text, font, fill):
        """Draw `text` with the top of its capitals on row `top`."""
        d.text((x, top - font.getbbox(text)[1]), text, font=font, fill=fill)

    # A cellar wall: courses of brick offset every other row, lit from the torch at the
    # top left so the light falls down and to the right and the far corner stays dark.
    bw, bh = 28, 12
    for row, y in enumerate(range(0, H, bh)):
        off = 0 if row % 2 == 0 else bw // 2
        for x in range(-bw, W + bw, bw):
            far = ((x + off - 34) ** 2 + ((y - 40) * 2.2) ** 2) ** 0.5
            lit = max(0.0, 1.0 - far / 420)
            c = tuple(int(s + (b - s) * (0.2 + 0.8 * lit))
                      for s, b in zip(SURFACE, BRICK))
            d.rectangle([x + off, y, x + off + bw - 3, y + bh - 3], fill=c)

    # The torch, and the pool of light it throws.
    tx, ty = 34, 40
    for r, a in ((46, 0.07), (32, 0.11), (20, 0.17), (10, 0.28)):
        d.ellipse([tx - r, ty - r, tx + r, ty + r],
                  fill=tuple(int(b + (t - b) * a) for b, t in zip(BRICK, TORCH)))
    d.rectangle([tx - 2, ty + 2, tx + 2, ty + 26], fill=STONE)      # the shaft
    d.rectangle([tx - 4, ty - 2, tx + 4, ty + 3], fill=TORCH)       # the flame
    d.rectangle([tx - 2, ty - 8, tx + 2, ty - 1], fill=GOLD)

    title = face(18)
    lede = face(12)
    fact = face(12)

    x = 34
    line(x, 80, "Now THAT'S a Big Dragon!", title, GOLD)
    line(x, 114, "language patch  cheats  autoplay", lede, PARCHMENT)

    for i, (mark, text, ink) in enumerate([
        (TORCH, "22 languages, 51.10% of Steam users", TORCH),
        (MOSS, "no game files are modified", MORTAR),
        (MOSS, "unofficial fan-made mod, MIT", MORTAR),
    ]):
        y = 144 + i * 20
        d.rectangle([x, y + 4, x + 5, y + 9], fill=mark)
        line(x + 13, y, text, fact, ink)

    # The Steam share, drawn rather than only stated.
    d.rectangle([0, H - 5, W, H], fill=LINE)
    d.rectangle([0, H - 5, int(W * 0.5110), H], fill=TORCH)

    img.resize((W * SCALE, H * SCALE), Image.NEAREST).save(OUT, optimize=True)
    print(f"{OUT.relative_to(ROOT)}  {W * SCALE}x{H * SCALE}  {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    sys.exit(main())

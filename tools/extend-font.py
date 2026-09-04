"""Extends the game's own pixel fonts with the letters they are missing.

The game draws its text in Everyday_Standard (6 px/em) and High_Birth (9 px/em), both
by VEXED and both under CC BY 4.0 — so they can be modified and redistributed with
attribution. That matters, because every other option is worse:

    font              grid          matched to the game's body font
    ----------------  ------------  ----------------------------------------
    LanaPixel         11 px/em      capitals +17%, no Thai, no Vietnamese tones
    Galmuri7           8 px/em      capitals +17%
    Fusion Pixel 8     8 px/em      capitals exact, lowercase -20%
    this              same font     exact, because it is the same font

Anything else leaves one word rendered in two faces: Czech "Poškození" would take its
`š` and `í` from the bundled font and everything else from the game's. Extending the
game's own font removes the question.

Most of the marks are already in the font — they just are not attached to the letters
we need. `ą` carries an ogonek, `ğ` a breve, `å` a ring, `ż` a dot: each is harvested
by taking the contours of a precomposed glyph that lie outside its own base letter.
Only the caron and the double acute have to be drawn, and at this size each is three
or four pixels.

    pip install fonttools brotli
    python tools/extend-font.py <dir with Everyday_Standard.ttf, High_Birth.ttf>

Writes locale/fonts/Everyday_Standard-bd.woff2 and High_Birth-bd.woff2.
"""

import pathlib
import sys
import unicodedata

OUT = pathlib.Path(__file__).resolve().parent.parent / "locale" / "fonts"

# The letters to add, by language. Every one decomposes into a base the font already
# has plus a single combining mark.
TARGETS = {
    "cs": "ČčĎďĚěŇňŘřŠšŤťŮůŽž",
    "hu": "ŐőŰű",
    "ro": "ĂăȘșȚț",
    "pl": "ĄąĆćĘęŁł"
           "ŃńŚśŹźŻż",
    "tr": "ĞğİıŞş",
    "da": "ØøÆæÅå",
}

# The marks the font carries nowhere are derived from ones it does, rather than drawn
# to fixed coordinates. That keeps the weight and the height right in both fonts
# without this file knowing that one is 6 px/em and the other 9.
def flip_rows(cells):
    """Mirror a mark about the middle of its own rows: a circumflex becomes a caron."""
    rows = [r for _, r in cells]
    lo, hi = min(rows), max(rows)
    return [(c, lo + hi - r) for c, r in cells]


def double(cells, gap=1):
    """Two upright ticks, spanning the rows the source mark occupies.

    A double acute really is two slanted strokes, but at this size that lands on the
    very cells the font already uses for its tilde — `ő` and `õ` would be the same
    picture. Two upright ticks are unmistakable and still read as a pair.
    """
    rows = sorted({r for _, r in cells})
    lo = min(c for c, _ in cells)
    return [(lo, r) for r in rows] + [(lo + 1 + gap, r) for r in rows]


# name of the mark we need -> (name of the mark to derive it from, how)
DERIVED = {
    "caron": ("circumflexaccent", flip_rows),
    "doubleacuteaccent": ("acuteaccent", double),
    # At six pixels a comma below and a cedilla are the same three cells, and every
    # pixel font settles on one of them. Romanian readers get the cedilla form.
    "commabelow": ("cedilla", lambda c: list(c)),
    # A breve is a caron with a flat bottom. Where the font has no breve to harvest,
    # widening the caron's low row is the closest honest approximation.
    "breve": ("circumflexaccent", lambda c: _flatten(flip_rows(c))),
    # An ogonek and a cedilla are both hooks under the letter; where the font draws
    # only one of them, it is the shape the other has to borrow.
    "ogonek": ("cedilla", lambda c: list(c)),
    # A dot is half a diaeresis. Take the left half and centre it.
    "dotabove": ("diaeresis", lambda c: _half(c)),
}


def _half(cells):
    """The left half of a two-part mark, which is what a single dot is."""
    cols = sorted({c for c, _ in cells})
    if len(cols) < 2:
        return list(cells)
    return [(c, r) for c, r in cells if c <= cols[len(cols) // 2 - 1]]


def _flatten(cells):
    """Spread the lowest row of a mark across the columns between its arms."""
    rows = [r for _, r in cells]
    lo = min(rows)
    cols = sorted({c for c, r in cells if r == lo})
    if len(cols) == 1:
        arms = sorted({c for c, r in cells if r != lo})
        if len(arms) >= 2:
            cols = list(range(min(arms) + 1, max(arms)))
    return [(c, r) for c, r in cells if r != lo] + [(c, lo) for c in cols]

# Czech ď ť Ď Ť put the caron beside the ascender rather than above it: at six pixels
# there is no room over an `d`. A vertical tick after the letter is the form pixel
# fonts settle on, and it costs one pixel of advance.
SIDE_CARON = {"ď": "d", "ť": "t", "Ď": "D", "Ť": "T"}


# Letters that are not a base plus a combining mark, so Unicode gives no recipe. Each
# is built out of its own base glyph's cells rather than drawn to fixed coordinates,
# so the same rule works at 6 px/em and at 9.
def undot(cells, _):
    """`ı` is `i` with the dot taken off: drop everything above the first empty row."""
    rows = {r for _, r in cells}
    hi = max(rows)
    gap = next((r for r in range(hi, min(rows) - 1, -1) if r not in rows), None)
    return [(c, r) for c, r in cells if gap is None or r < gap]


def stroke(cells, _):
    """`ł` is `l` with a bar through the stem. At one pixel wide there is no through
    to draw, so the bar sits beside it — which is what pixel fonts do."""
    rows = [r for _, r in cells]
    lo, hi = min(rows), max(rows)
    col = max(c for c, _ in cells) + 1
    return list(cells) + [(col, lo + (hi - lo) * 2 // 3)]


def slash(cells, _):
    """`ø` is `o` with a stroke across it, corner to corner of its own box."""
    cols = [c for c, _ in cells]
    rows = [r for _, r in cells]
    w = max(cols) - min(cols)
    h = max(rows) - min(rows)
    out = list(cells)
    for i in range(h + 1):
        out.append((min(cols) + round(i * w / h), min(rows) + i))
    return out


COMPOSED = {
    "ı": ("i", undot), "ł": ("l", stroke), "Ł": ("L", stroke),
    "ø": ("o", slash), "Ø": ("O", slash),
}


def load(path):
    from fontTools.ttLib import TTFont

    return TTFont(path)


def cell_size(font):
    """One design pixel, in font units."""
    upm = font["head"].unitsPerEm
    # The fonts are 6 and 9 px/em; both divide their upem exactly.
    for px_per_em in (6, 9, 8, 10, 12):
        if upm % px_per_em == 0:
            step = upm // px_per_em
            # Confirm against a glyph: every coordinate must land on the grid.
            cmap = font.getBestCmap()
            gs = font.getGlyphSet()
            from fontTools.pens.recordingPen import RecordingPen

            pen = RecordingPen()
            gs[cmap[ord("A")]].draw(pen)
            pts = [p for _, a in pen.value for p in a if isinstance(p, tuple)]
            if pts and all(x % step == 0 and y % step == 0 for x, y in pts):
                return step, px_per_em
    raise SystemExit(f"{path}: could not work out the pixel grid")


def cells_of(font, ch, step):
    """A glyph as a set of (column, row) pixel cells."""
    from fontTools.pens.recordingPen import RecordingPen

    cmap = font.getBestCmap()
    gn = cmap.get(ord(ch))
    if not gn:
        return None
    pen = RecordingPen()
    font.getGlyphSet()[gn].draw(pen)
    # Each contour of a pixel font is one axis-aligned rectangle; take its box.
    out = set()
    cur = []
    contours = []
    for op, args in pen.value:
        if op == "moveTo":
            if cur:
                contours.append(cur)
            cur = [args[0]]
        elif op in ("lineTo", "qCurveTo", "curveTo"):
            cur.extend(a for a in args if isinstance(a, tuple))
        elif op == "closePath":
            if cur:
                contours.append(cur)
            cur = []
    if cur:
        contours.append(cur)
    for c in contours:
        xs = [x for x, _ in c]
        ys = [y for _, y in c]
        for col in range(round(min(xs) / step), round(max(xs) / step)):
            for row in range(round(min(ys) / step), round(max(ys) / step)):
                out.add((col, row))
    return out


def harvest_marks(font, step):
    """Mark shapes taken from precomposed letters the font already carries.

    The mark is whatever the composed glyph has that its own base does not — which,
    on a pixel grid, is an exact set difference.
    """
    cmap = font.getBestCmap()
    marks = {}
    for cp in list(cmap):
        ch = chr(cp)
        d = unicodedata.normalize("NFD", ch)
        if len(d) != 2 or not (0x0300 <= ord(d[1]) <= 0x036F):
            continue
        if ord(d[0]) not in cmap:
            continue
        base = cells_of(font, d[0], step)
        whole = cells_of(font, ch, step)
        if base is None or whole is None:
            continue
        extra = whole - base
        if not extra:
            continue
        name = unicodedata.name(d[1]).replace("COMBINING ", "").lower().replace(" ", "")
        # Keep the one taken from a lowercase base: that is the placement new
        # lowercase letters need, and uppercase is the same shape lifted.
        key = (name, d[0].islower())
        if key not in marks:
            marks[key] = extra
    return marks


def build(src, out_name, targets):
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    font = load(src)
    step, px_per_em = cell_size(font)
    cmap = font.getBestCmap()
    marks = harvest_marks(font, step)
    glyf = font["glyf"]
    hmtx = font["hmtx"]

    added, skipped, added_names = [], [], []
    for ch in targets:
        if ord(ch) in cmap:
            continue
        base_ch, mark_cells = plan(ch, font, step, marks)
        if mark_cells is None:
            skipped.append(ch)
            continue
        # A COMPOSED letter comes back with no base: its rule already drew the whole
        # thing, because there is no base-plus-mark decomposition to lean on.
        base_cells = set() if base_ch is None else cells_of(font, base_ch, step)
        if base_cells is None:
            skipped.append(ch)
            continue

        cells = set(base_cells) | set(mark_cells)
        gname = f"uni{ord(ch):04X}"
        pen = TTGlyphPen(None)
        for col, row in sorted(cells):
            x, y = col * step, row * step
            pen.moveTo((x, y))
            pen.lineTo((x + step, y))
            pen.lineTo((x + step, y + step))
            pen.lineTo((x, y + step))
            pen.closePath()
        g = pen.glyph()
        g.recalcBounds(glyf)
        glyf[gname] = g

        adv, lsb = hmtx[cmap[ord(base_ch or COMPOSED[ch][0])]]
        # A side caron, and the bar beside an `l`, need the extra column they sit in.
        if ch in SIDE_CARON or ch in ("ł", "Ł"):
            adv += step
        hmtx[gname] = (adv, lsb)
        for table in font["cmap"].tables:
            if table.isUnicode():
                table.cmap[ord(ch)] = gname
        added.append(ch)
        added_names.append(gname)

    # glyphOrder has to know about the new names before anything recalculates.
    font.setGlyphOrder(font.getGlyphOrder() + [g for g in added_names
                                               if g not in font.getGlyphOrder()])
    font["maxp"].recalc(font)
    name_table = font["name"]
    family = name_table.getDebugName(1)
    for rec in name_table.names:
        if rec.nameID in (1, 3, 4, 6):
            v = rec.toUnicode()
            if "-bd" not in v:
                rec.string = v.replace(family, f"{family}-bd")
    note = (
        f"{family} by VEXED, CC BY 4.0. Modified for the Now THAT'S a Big Dragon! mod: "
        f"{len(added)} letters added for Czech, Hungarian and Romanian. "
        "The original is unchanged; only glyphs were added."
    )
    name_table.setName(note, 10, 3, 1, 0x409)

    dest = OUT / out_name
    font.flavor = "woff2"
    font.save(dest)
    print(f"{out_name}: {px_per_em} px/em, +{len(added)} glyphs {''.join(added)}"
          + (f"  (skipped {''.join(skipped)})" if skipped else ""))
    return dest


def plan(ch, font, step, marks):
    """The base letter and the mark cells for one new glyph."""
    if ch in COMPOSED:
        base, make = COMPOSED[ch]
        base_cells = cells_of(font, base, step)
        if not base_cells:
            return base, None
        # These build the whole letter, base included, so the base is dropped after.
        return None, make(base_cells, step)
    d = unicodedata.normalize("NFD", ch)
    if ch in SIDE_CARON:
        base = SIDE_CARON[ch]
        base_cells = cells_of(font, base, step)
        if not base_cells:
            return base, None
        col = max(c for c, _ in base_cells) + 1
        top = max(r for _, r in base_cells)
        # A tick beside the ascender, hanging from its very top.
        return base, [(col, top), (col, top - 1)]
    if len(d) != 2:
        return ch, None
    base, mark = d[0], d[1]
    name = unicodedata.name(mark).replace("COMBINING ", "").lower().replace(" ", "")
    lower = base.islower()

    got = marks.get((name, lower)) or marks.get((name, not lower))
    if got is not None:
        cells = list(got)
        # A mark harvested from the other case has to move to this one's height.
        if (name, lower) not in marks:
            base_cells = cells_of(font, base, step)
            other = "a" if lower else "A"
            ref = cells_of(font, other, step)
            if base_cells and ref:
                shift = max(r for _, r in base_cells) - max(r for _, r in ref)
                cells = [(c, r + shift) for c, r in cells]
        return base, cells

    recipe = DERIVED.get(name)
    if recipe is None:
        return base, None
    source, make = recipe
    src_cells = marks.get((source, lower)) or marks.get((source, not lower))
    if src_cells is None:
        return base, None
    cells = make(src_cells)
    # If the source came from the other case, lift or drop it to this one's height.
    if (source, lower) not in marks:
        ref = cells_of(font, "a" if lower else "A", step)
        base_cells = cells_of(font, base, step)
        if ref and base_cells:
            shift = max(r for _, r in base_cells) - max(r for _, r in ref)
            cells = [(c, r + shift) for c, r in cells]
    # Centre the mark over the base letter.
    base_cells = cells_of(font, base, step)
    if base_cells:
        bw = max(c for c, _ in base_cells) + 1
        cols = [c for c, _ in cells]
        mw = max(cols) - min(cols) + 1
        cells = [(c - min(cols) + (bw - mw + 1) // 2, r) for c, r in cells]
    return base, cells


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-3], file=sys.stderr)
        return 2
    src = pathlib.Path(sys.argv[1])
    targets = "".join(TARGETS.values())
    for name, out in [
        ("Everyday_Standard.ttf", "Everyday_Standard-bd.woff2"),
        ("High_Birth.ttf", "High_Birth-bd.woff2"),
    ]:
        p = src / name
        if not p.exists():
            print(f"missing: {p}", file=sys.stderr)
            return 1
        build(p, out, targets)
    return 0


if __name__ == "__main__":
    sys.exit(main())

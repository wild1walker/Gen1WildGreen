#!/usr/bin/env python3
"""Draw label.png: the Gen1Wild wordmark with WILD GREEN VERSION under it.

    python3 tools/make_label.py

The label is the picture the launcher puts on the cartridge, so it is the
one place the cart says what it is.  It is the wordmark and the version
line and nothing else -- a cartridge label is read at thumbnail size, and
anything a third element would add is illegible by the time it is drawn.

The wordmark is not redrawn here.  It is `art/gen1wild_wordmark.png`, the
same committed artwork Gen1Wild's own banner and favicon are cut from, so
the cart and the index stay one object rather than two things that have to
be kept looking alike by hand.  The green under it is the shell colour from
tools/palette.py, which is also the colour of the VERSION lettering on the
title screen: the cartridge and the title agree because they read the same
four numbers.

The version line reuses the title ribbon's own 5x7 face, drawn straight out
of tools/make_ribbon.py, for the same reason -- one face, one wording, two
places it appears.

Pillow is required here and only here: the wordmark is a real PNG with
alpha that has to be scaled and composited, which is more than the
hand-rolled writer in make_ribbon.py is for.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from palette import DARK, LIGHT, PAPER, WORDMARK_BLUE  # noqa: E402
import make_ribbon  # noqa: E402

try:
    from PIL import Image
except ImportError:                                    # pragma: no cover
    raise SystemExit("make_label needs Pillow: pip install pillow")

WORDMARK = ROOT / "art" / "gen1wild_wordmark.png"
OUT = ROOT / "label.png"

SIZE = 256          # the launcher draws the label square
MARGIN = 18         # the sticker's border, in label pixels
GAP = 16            # between the wordmark's shadow and the version line
TEXT_SCALE = 2      # the 5x7 face, doubled, so it reads at thumbnail size


def sticker():
    """The green field the wordmark sits on: a flat face inside a darker edge."""
    img = Image.new("RGB", (SIZE, SIZE), DARK)
    edge = tuple(int(round(c * 0.55)) for c in DARK)
    inner = Image.new("RGB", (SIZE - 2 * MARGIN, SIZE - 2 * MARGIN), DARK)
    img.paste(Image.new("RGB", (SIZE, SIZE), edge), (0, 0))
    img.paste(inner, (MARGIN, MARGIN))
    return img


def wordmark(width):
    art = Image.open(WORDMARK).convert("RGBA")
    height = round(art.height * width / art.width)
    return art.resize((width, height), Image.LANCZOS)


def version_line():
    """The ribbon's own lettering, as an RGBA layer keyed on its paper shade."""
    width, grid = make_ribbon.draw(make_ribbon.TEXT)
    shades = {make_ribbon.DARK: PAPER, make_ribbon.LIGHT: LIGHT}
    layer = Image.new("RGBA", (width, make_ribbon.HEIGHT), (0, 0, 0, 0))
    layer.putdata([shades.get(s, (0, 0, 0)) + ((0,) if s == make_ribbon.PAPER
                                               else (255,))
                   for row in grid for s in row])
    return layer.resize((width * TEXT_SCALE, make_ribbon.HEIGHT * TEXT_SCALE),
                        Image.NEAREST)


def main():
    if not WORDMARK.exists():
        raise SystemExit("no wordmark at %s" % WORDMARK)

    label = sticker()

    mark = wordmark(SIZE - 2 * MARGIN - 8)
    line = version_line()
    if line.width > SIZE - 2 * MARGIN:
        raise SystemExit("make_label: the version line does not fit the label")

    # Wordmark and version line are one lockup, centred together.  Centring
    # them separately in half a label each is what makes a label look like
    # two stickers.
    lockup = mark.height + GAP + line.height
    top = (SIZE - lockup) // 2
    label.paste(mark, ((SIZE - mark.width) // 2, top), mark)
    label.paste(line, ((SIZE - line.width) // 2, top + mark.height + GAP),
                line)

    # One pixel of the wordmark's own blue around the sticker, which is what
    # keeps a green label from dissolving into a green shell.
    for x in range(SIZE):
        for y in (MARGIN - 1, SIZE - MARGIN):
            label.putpixel((x, y), WORDMARK_BLUE)
    for y in range(MARGIN - 1, SIZE - MARGIN + 1):
        for x in (MARGIN - 1, SIZE - MARGIN):
            label.putpixel((x, y), WORDMARK_BLUE)

    label.save(OUT, optimize=True)
    print("wrote %s  %dx%d  %d bytes"
          % (OUT.relative_to(ROOT), SIZE, SIZE, OUT.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

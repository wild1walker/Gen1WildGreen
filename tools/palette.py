#!/usr/bin/env python3
"""The Wild Green palette, in one place, for the tools that draw with it.

Four colours for the character, three for the title, and nothing else.

    twin: wild1walker/Gen1MakeItGreen tools/palette.py

## The character ramp

The importer decodes vanilla art to four grey shades (255 / 170 / 85 / 0)
and the palette pass colours them at draw time.  On the player's sprites
those four are, in order: the transparent/white ground, **the skin and the
shirt's white**, **the outfit**, and the black outline and hair.

That second entry is the one that got this wrong the first time.  Recolouring
shades 2 AND 3 green turns the face green too, which is what "all green
instead of just his outfit" looked like in the field.  Only shade 3 is the
outfit, so only shade 3 turns green; shade 2 becomes skin, which is what the
palette pass would have made of it.

## The title ramp

`LOGO1` is the SGB palette the title's version-ribbon band wears, and it is
independent of the character -- the ribbon is lettering on white, not a
sprite.  Both its greens are dark enough to read as green ink on paper at
8px; the first cut used the character's light green and washed out.
"""

# The character, lightest first -- the order ctx.recolor reads.
PAPER = (0xff, 0xff, 0xff)   # shade 1 -- pure white: battle pics matte on it
SKIN = (0xf8, 0xd8, 0xa8)    # shade 2 -- the face, and the shirt's white
OUTFIT = (0x65, 0xba, 0x3f)  # shade 3 -- the cap and clothes; the reference green
INK = (0x00, 0x00, 0x00)     # shade 4 -- outline and hair

RAMP = [PAPER, SKIN, OUTFIT, INK]

# The title ribbon band (LOGO1).  Ink is the lettering; MID is its shadow.
TITLE_MID = (0x2e, 0x8b, 0x3a)
TITLE_INK = (0x14, 0x57, 0x1f)
TITLE_RAMP = [PAPER, TITLE_MID, TITLE_INK, INK]

# The cartridge shell, and the VERSION lettering it matches.
SHELL = "#%02x%02x%02x" % TITLE_INK

# The wordmark's own two colours, lifted from docs/banner.png in Gen1Wild so
# the label and the index banner stay the same object.
WORDMARK_YELLOW = (0xf5, 0xc0, 0x18)
WORDMARK_BLUE = (0x26, 0x47, 0x81)


def hexof(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


if __name__ == "__main__":
    for name in ("PAPER", "SKIN", "OUTFIT", "INK", "TITLE_MID", "TITLE_INK"):
        print("%-10s %s" % (name, hexof(globals()[name])))
    print("%-10s %s" % ("SHELL", SHELL))

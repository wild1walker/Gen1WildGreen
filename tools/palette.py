#!/usr/bin/env python3
"""The Wild Green palette, in one place, for the tools that draw with it.

Four colours and nothing else.  They are the same four the mod's own
`transforms.lua` recolors the player's art to, and the same four the cart's
shell and label are drawn from, because a cart whose lettering and whose
shell disagree about what green it is looks like two carts.

The greens are measured, not invented.  `LIGHT` is sampled off the reference
overworld sprite (#65ba3f, the bright green the character's body reads as);
`DARK` is that green taken down to the weight vanilla's "Red Version"
lettering carries against white (#a01e29, v=0.63), so the ribbon reads the
way the red one does rather than merely being green.

`tools/check.py` fails the build if these drift from the copy in
`mods/wild_green/transforms.lua`, which cannot import anything.
"""

# lightest first, matching the shade order every palette table in the engine
# uses and the order ctx.recolor wants
PAPER = (0xff, 0xff, 0xff)   # shade 1 -- stays pure white: battle pics matte on it
LIGHT = (0x65, 0xba, 0x3f)   # shade 2 -- the reference sprite green
DARK = (0x1e, 0x7a, 0x2b)    # shade 3 -- the VERSION lettering, and the shell
INK = (0x00, 0x00, 0x00)     # shade 4

RAMP = [PAPER, LIGHT, DARK, INK]

SHELL = "#%02x%02x%02x" % DARK

# The wordmark's own two colours, lifted from docs/banner.png in Gen1Wild so
# the label and the index banner stay the same object.
WORDMARK_YELLOW = (0xf5, 0xc0, 0x18)
WORDMARK_BLUE = (0x26, 0x47, 0x81)


def hexof(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


if __name__ == "__main__":
    for name in ("PAPER", "LIGHT", "DARK", "INK"):
        print("%-6s %s" % (name, hexof(globals()[name])))
    print("%-6s %s" % ("SHELL", SHELL))

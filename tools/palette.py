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
SKIN = (0xf0, 0xa3, 0x63)    # shade 2 -- the face and hands; sampled from the reference
OUTFIT = (0x65, 0xba, 0x3f)  # shade 3 -- the cap and clothes; the reference green
MOUTH = (0xec, 0x4d, 0x29)   # the lips; vanilla's own, sampled off red Red
BILL = (0xe6, 0xf4, 0xdc)    # the cap's bill: a green-tinted white
INK = (0x00, 0x00, 0x00)     # shade 4 -- outline and hair

RAMP = [PAPER, SKIN, OUTFIT, INK]

# The trainer art -- the battle back pic, and the front pic Oak's intro, the
# trainer card and the Hall of Fame share -- takes a different four, because
# shade 2 does not mean the same thing there.
#
# On the 16x16 overworld sprite shade 2 is only ever the face.  On the 56x56
# portrait it is the LIGHT for everything: the cap's front, the shading on
# the shirt, the highlight on the knees and the shoes.  Vanilla gets away
# with one shade for both because its ramp is monochrome red -- white, light
# red, red, black -- and light red happens to look like skin.  Painting that
# shade a skin tone put orange blotches on the hat and the knees.
#
# So the portrait gets the same trick in green: white, light green, green,
# black.  The face reads as a pale green rather than as skin, which is
# exactly the compromise vanilla makes in the other direction.
PIC_LIGHT = (0xa8, 0xdd, 0x8a)
PIC_RAMP = [PAPER, PIC_LIGHT, OUTFIT, INK]

# Not shades.  Two parts of the sprite are drawn in a shade that is not their
# own, and are told apart by where they sit rather than by colour.
#
# MOUTH is vanilla's own: red Red's lips are drawn in the CAP's shade, so they
# come out red, and "the default colour" is what they should stay.
#
# BILL is neither.  Vanilla draws it in the FACE's shade, so on red Red it is
# the colour of his cheek and reads as nothing; painting it the cap's green
# merged it into the hat instead.  A green-tinted white gives it an edge
# against both.
# And this one.  Vanilla draws the shadow on the skin -- the ear, the brow,
# the line of the mouth -- in the shade BELOW the skin's, which on a
# monochrome ramp is the same shade as the clothes.  Painting only shade 2
# leaves those as green freckles on an otherwise skin-coloured face, so the
# pieces of shade 3 sealed inside skin take the skin's own shadow instead.
SKIN_DARK = (0xad, 0x75, 0x47)

EXTRA = {"MOUTH": MOUTH, "BILL": BILL, "SKIN_DARK": SKIN_DARK}

# ------- the other eight suits
#
# PLAYER is nine colours now.  Only three values change between them, and
# they are the three above that carry the outfit's hue: OUTFIT itself,
# PIC_LIGHT (the portrait's light shade, which on that art is the highlight
# for the whole figure rather than skin), and BILL (the cap's peak, which is
# told apart from the cap by where it sits and so needs a colour of its own).
#
# SKIN, SKIN_DARK, MOUTH, PAPER and INK do NOT change.  The face is the face
# in every colour -- which is the whole reason the recipe learned to tell
# skin from clothing in the first place, and is what "just the outfit" means.
#
# Green's three are sampled by hand and stay exactly as they were: it is the
# default, it is what the cart is named after, and its files must come out
# byte for byte the same as before this table existed.  The other eight are
# derived from their outfit by the rule green's own values describe:
#
#     PIC_LIGHT = outfit mixed 45% toward white
#     BILL      = outfit mixed 83% toward white
#
# which reproduces green to within five values of 255 on every channel
# (#aad995 against #a8dd8a, #e5f3de against #e6f4dc).  Derived once and
# written out as literals rather than computed here, because these are the
# same three files' worth of hand-checkable numbers as everything else above
# and tools/check.py compares them across all three.
#
# Except for a PALE outfit, where mixing further toward white is the wrong
# direction: a near-white bill on a near-white cap is no edge at all.  Above
# 0.70 relative luminance -- which is YELLOW and WHITE, and which green at
# 0.62 sits under -- the bill goes 35% toward BLACK instead, and reads as the
# peak's own shadow.
#
# WHITE is the one that cannot be made high-contrast and should not be: a
# white outfit on white paper is carried by vanilla's own black outline, the
# way a white shirt is in any four-shade art.  Its outfit is pulled slightly
# off pure so the garment still has a body.
SUIT_ORDER = ["green", "orange", "blue", "purple", "yellow",
              "pink", "black", "white", "grey"]

# name -> (OUTFIT, PIC_LIGHT, BILL)
SUITS = {
    "green":  ((0x65, 0xba, 0x3f), (0xa8, 0xdd, 0x8a), (0xe6, 0xf4, 0xdc)),
    "orange": ((0xe2, 0x68, 0x1c), (0xef, 0xac, 0x82), (0xfa, 0xe5, 0xd8)),
    "blue":   ((0x3f, 0x7b, 0xd8), (0x95, 0xb6, 0xea), (0xde, 0xe9, 0xf8)),
    "purple": ((0x8a, 0x5b, 0xd0), (0xbf, 0xa5, 0xe5), (0xeb, 0xe3, 0xf7)),
    "yellow": ((0xe8, 0xc5, 0x3a), (0xf2, 0xdf, 0x93), (0x97, 0x80, 0x26)),
    "pink":   ((0xee, 0x7b, 0xb8), (0xf6, 0xb6, 0xd8), (0xfc, 0xe9, 0xf3)),
    "black":  ((0x3d, 0x3d, 0x45), (0x94, 0x94, 0x99), (0xde, 0xde, 0xdf)),
    "white":  ((0xcd, 0xd3, 0xda), (0xe4, 0xe9, 0xee), (0x85, 0x89, 0x8e)),
    "grey":   ((0x8b, 0x91, 0x99), (0xbf, 0xc2, 0xc7), (0xeb, 0xec, 0xee)),
}

# green's entry IS the three constants above; the two spellings cannot drift.
assert SUITS["green"] == (OUTFIT, PIC_LIGHT, BILL)
assert sorted(SUIT_ORDER) == sorted(SUITS)


def suit_ramp(name):
    """The overworld four for a suit, lightest first."""
    return [PAPER, SKIN, SUITS[name][0], INK]


def suit_pic_ramp(name):
    """The portrait four for a suit, lightest first."""
    return [PAPER, SUITS[name][1], SUITS[name][0], INK]

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

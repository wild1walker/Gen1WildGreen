#!/usr/bin/env python3
"""Draw the title screen's version ribbon: WILD GREEN VERSION.

    python3 tools/make_ribbon.py

Writes mods/wild_green/assets/title/wild_green_version.png.

This is original art and ships as pixels, which is the whole reason it is
drawn here rather than recolored out of the player's cache: nothing in it
comes from the ROM.  The vanilla ribbon is two fragments the title code
repositions; ours is one continuous strip, which is what `versionRibbon`
(as opposed to the importer's `version`) means to `src/ui/TitleState.lua` --
it centres a full ribbon as one piece at y=64.

The strip is written on the importer's four grey shades (255 / 170 / 85 / 0)
and not in colour, because the title's ribbon band is an SGB palette zone:
`TitleState:sgbPalettes` colours tile rows 8-9 with LOGO1, and the shader
remaps by shade.  Green pixels here would be read as shades and remapped to
something else entirely.  The green arrives from the LOGO1 record the mod
overrides -- see mods/wild_green/main.lua.

The font is a 5x7 all-caps face written out below.  No font file is loaded
and nothing is measured off the host, so a rebuild on any machine produces
a byte-identical PNG.
"""

import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "mods" / "wild_green" / "assets" / "title" / "wild_green_version.png"

TEXT = "WILD GREEN VERSION"

# the importer's four shades (src/import/ImageWriter.lua), lightest first
PAPER, LIGHT, DARK, INK = 255, 170, 85, 0

GLYPH_W, GLYPH_H = 5, 7
GAP = 1          # between glyphs
SPACE = 3        # a word gap, on top of the glyph gap
HEIGHT = 10      # 1 blank row, 7 glyph rows, 1 shadow row, 1 blank row

FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
}


def layout(text):
    """(x, glyph) for every letter, and the width the strip needs."""
    placed, x = [], 0
    for index, ch in enumerate(text):
        if ch == " ":
            x += SPACE
            continue
        glyph = FONT.get(ch)
        if glyph is None:
            raise SystemExit("make_ribbon: no glyph for %r" % ch)
        placed.append((x, glyph))
        x += GLYPH_W + GAP
        del index
    # the trailing gap is not part of the ribbon; the shadow row is
    return placed, x - GAP + 1


def draw(text):
    placed, width = layout(text)
    grid = [[PAPER] * width for _ in range(HEIGHT)]

    def put(x, y, shade):
        if 0 <= x < width and 0 <= y < HEIGHT:
            grid[y][x] = shade

    # The shadow goes down first so the letter sits on top of it rather than
    # having to be drawn around it.  One pixel down and right, in the light
    # green: the vanilla ribbon's word is two-tone too, and a black shadow
    # under a dark letter at this size just thickens the stroke.
    for offset, shade in ((1, LIGHT), (0, DARK)):
        for x0, glyph in placed:
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        put(x0 + col + offset, 1 + row + offset, shade)
    return width, grid


def png_bytes(width, height, grid):
    raw = bytearray()
    for row in grid:
        raw.append(0)
        for shade in row:
            raw += bytes((shade, shade, shade))

    def chunk(tag, body):
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xffffffff))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    width, grid = draw(TEXT)
    if width > 160:
        raise SystemExit("make_ribbon: %d px is wider than the 160 px screen"
                         % width)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(png_bytes(width, HEIGHT, grid))
    print("wrote %s  %dx%d  (centres at x=%d)"
          % (OUT.relative_to(ROOT), width, HEIGHT, (160 - width) // 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

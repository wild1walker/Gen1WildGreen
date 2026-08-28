#!/usr/bin/env python3
"""The WILD GREEN VERSION lettering: a 5x7 face and the strip it draws.

A library, not a command.  Two things set this wording and they are in two
repositories: the title screen's version ribbon, which is an asset in the
Wild Green mod, and the version line on this cart's label.  They are the
same words in the same face because they come from the same file -- so this
file is carried in both, and each repo's tools/check.py fails if the copies
drift.

Everything here is drawn on the importer's four grey shades (255 / 170 / 85
/ 0) rather than in colour, because the title screen's ribbon band is an SGB
palette zone: `TitleState:sgbPalettes` colours tile rows 8-9 with LOGO1 and
the shader remaps by shade.  Green pixels would be read as shades and
remapped to something else entirely.  Callers that want colour -- the label,
which is a picture and not a palette zone -- map the shades themselves.

No font file is loaded and nothing is measured off the host, so a rebuild on
any machine produces byte-identical output.

    twin: wild1walker/Gen1makeitgreen tools/ribbon.py
"""

import struct
import zlib

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
    for ch in text:
        if ch == " ":
            x += SPACE
            continue
        glyph = FONT.get(ch)
        if glyph is None:
            raise SystemExit("ribbon: no glyph for %r" % ch)
        placed.append((x, glyph))
        x += GLYPH_W + GAP
    # the trailing gap is not part of the ribbon; the shadow column is
    return placed, x - GAP + 1


def draw(text=TEXT):
    """The strip as (width, rows of shade values)."""
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
    """An 8-bit RGB PNG of a grid of shade values."""
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

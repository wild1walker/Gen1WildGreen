#!/usr/bin/env python3
"""Draw the title screen's version ribbon: WILD GREEN VERSION.

    python3 tools/make_ribbon.py

Writes assets/title/wild_green_version.png.

This is original art and ships as pixels, which is the whole reason it is
drawn here rather than recolored out of the player's cache: nothing in it
comes from the ROM.  The vanilla ribbon is two fragments the title code
repositions; ours is one continuous strip, which is what `versionRibbon`
(as opposed to the importer's `version`) means to `src/ui/TitleState.lua` --
it centres a full ribbon as one piece at y=64.

The face and the shading are tools/ribbon.py; this only decides where the
file goes and that it fits on the screen.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import ribbon  # noqa: E402

OUT = ROOT / "assets" / "title" / "wild_green_version.png"

SCREEN = 160  # the Game Boy's width, which the ribbon centres in


def main():
    width, grid = ribbon.draw()
    if width > SCREEN:
        raise SystemExit("make_ribbon: %d px is wider than the %d px screen"
                         % (width, SCREEN))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(ribbon.png_bytes(width, ribbon.HEIGHT, grid))
    print("wrote %s  %dx%d  (centres at x=%d)"
          % (OUT.relative_to(ROOT), width, ribbon.HEIGHT,
             (SCREEN - width) // 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

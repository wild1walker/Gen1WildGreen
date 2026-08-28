#!/usr/bin/env python3
"""Draw label.png: the Wild Green cartridge art, scaled to the launcher's size.

    python3 tools/make_label.py

The label is the picture the launcher puts on the cartridge, so it is the
one place the cart says what it is.  It is also what the Gen1Wild index
shows on this cart's card: build_index.py fetches whatever `cart.json`'s
"label" names and writes it in as the listing's thumbnail, so this file and
the card are the same picture by construction rather than by two people
remembering to update both.

The artwork is `art/wild_green_label.png`, committed whole at the size it
was drawn.  Nothing is composited here and no lettering is drawn: the piece
already carries the Gen1Wild wordmark and WILD GREEN VERSION under it, so
scaling it is the entire job.  Earlier revisions of this file assembled the
label out of the wordmark PNG and tools/ribbon.py's 5x7 face; that is what
`git log` has, and it is why ribbon.py no longer needs to be carried here.

No border is drawn round it either.  The old sticker was a green field on a
green shell and needed a keyline to keep the two apart; this art is bright
against `#14571f` and separates on its own.

Pillow is required here and only here: scaling a real PNG is more than the
standard library does.

Determinism: one LANCZOS resize of a committed file, written with a fixed
encoder setting.  tools/check.py re-runs this and compares the bytes, so a
label that no longer matches its source fails CI rather than shipping.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

try:
    from PIL import Image
except ImportError:                                    # pragma: no cover
    raise SystemExit("make_label needs Pillow: pip install pillow")

ART = ROOT / "art" / "wild_green_label.png"
OUT = ROOT / "label.png"

SIZE = 256          # the launcher draws the label square


def main():
    if not ART.exists():
        raise SystemExit("no cartridge art at %s" % ART)

    art = Image.open(ART).convert("RGB")
    if art.width != art.height:
        raise SystemExit("make_label: %s is %dx%d; the label is square"
                         % (ART.name, art.width, art.height))

    art.resize((SIZE, SIZE), Image.LANCZOS).save(OUT, optimize=True)
    print("wrote %s  %dx%d  %d bytes"
          % (OUT.relative_to(ROOT), SIZE, SIZE, OUT.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

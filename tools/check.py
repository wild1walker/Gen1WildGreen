#!/usr/bin/env python3
"""Check the things that can quietly drift apart in here.

    python3 tools/check.py

Three copies of the Wild Green palette exist, and they have to agree:

    tools/palette.py                 what the label and the shell are drawn from
    mods/wild_green/transforms.lua   what the player's art is recolored to
    mods/wild_green/main.lua         what LOGO1 is overridden with

They are copies rather than one file because none of the three can import
from either of the others: the transform runs in a sandbox with no require,
the entry chunk cannot require its own files, and the tools are Python.  So
the duplication is the design, and this is what makes it safe.

Also checked: the generated art is current (a rebuild produces the same
bytes), the ribbon fits the screen, and cart.json still says what the
palette says about the shell.

Exits non-zero on any finding, which is what the release workflow wants.
"""

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from palette import DARK, INK, LIGHT, PAPER, SHELL, hexof  # noqa: E402

MOD = ROOT / "mods" / "wild_green"
EXPECTED = [PAPER, LIGHT, DARK, INK]

# a { 0xff, 0xff, 0xff } row of a Lua colour table
ROW = re.compile(r"\{\s*(0x[0-9a-fA-F]{2})\s*,\s*(0x[0-9a-fA-F]{2})\s*,"
                 r"\s*(0x[0-9a-fA-F]{2})\s*\}")

findings = []


def fail(where, message):
    findings.append("%s: %s" % (where, message))


def lua_ramp(path, marker):
    """The four colours of the table that follows `marker` in a Lua file."""
    text = path.read_text(encoding="utf-8")
    at = text.find(marker)
    if at < 0:
        fail(path.name, "no %r table to check" % marker)
        return None
    rows = ROW.findall(text[at:at + 400])[:4]
    if len(rows) != 4:
        fail(path.name, "the %r table has %d colours, not 4"
             % (marker, len(rows)))
        return None
    return [tuple(int(c, 16) for c in row) for row in rows]


def check_palettes():
    for path, marker in ((MOD / "transforms.lua", "local WILD_GREEN"),
                         (MOD / "main.lua", "local WILD_GREEN")):
        ramp = lua_ramp(path, marker)
        if ramp is None:
            continue
        if ramp != EXPECTED:
            fail(path.name, "the ramp is %s; tools/palette.py says %s"
                 % (" ".join(hexof(c) for c in ramp),
                    " ".join(hexof(c) for c in EXPECTED)))


def check_shell():
    cart = json.loads((ROOT / "cart.json").read_text(encoding="utf-8"))
    if cart.get("shell") != SHELL:
        fail("cart.json", "shell is %s; tools/palette.py says %s"
             % (cart.get("shell"), SHELL))
    label = cart.get("label")
    if label and not (ROOT / label).is_file():
        fail("cart.json", "label %r is not in the cart directory" % label)


def check_generated():
    """A rebuild has to produce the bytes that are committed."""
    for tool, product in (("make_ribbon.py",
                           MOD / "assets" / "title" / "wild_green_version.png"),
                          ("make_label.py", ROOT / "label.png")):
        if not product.is_file():
            fail(tool, "%s is missing; run it" % product.name)
            continue
        before = product.read_bytes()
        run = subprocess.run([sys.executable, str(ROOT / "tools" / tool)],
                             capture_output=True, text=True, cwd=ROOT)
        if run.returncode != 0:
            fail(tool, "exited %d: %s" % (run.returncode, run.stderr.strip()))
            continue
        if product.read_bytes() != before:
            fail(tool, "%s is stale; the committed file is not what the tool "
                       "draws" % product.name)


def main():
    check_palettes()
    check_shell()
    check_generated()
    for finding in findings:
        print("check: %s" % finding)
    if findings:
        return 1
    print("check: palettes agree, cart.json agrees, generated art is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())

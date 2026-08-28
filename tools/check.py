#!/usr/bin/env python3
"""Check the things that can quietly drift apart in the cart.

    python3 tools/check.py

Three of them:

  * `cart.json`'s shell is the palette's `DARK`.  The cartridge is the
    colour of the VERSION lettering because they are the same number, not
    because someone matched them by eye once.
  * `label.png` is what `tools/make_label.py` draws.  A committed PNG that
    the tool no longer produces is a picture nobody can regenerate.
  * `tools/palette.py` and `tools/ribbon.py` still match their twins in the
    mod's tree.  Both files are carried in two repositories -- neither can
    import from the other -- and this is the only thing standing between
    that and a cart whose shell has stopped matching its own title screen.

That last check applies only while `mods/wild_green/` is still here.  Once
the mod moves to its own repository it stops finding the twins and says so
instead of pretending it checked something.

Exits non-zero on any finding, which is what CI wants.
"""

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from palette import SHELL  # noqa: E402

# where the mod's copies live while the two still share a repository
TWIN_ROOT = ROOT / "mods" / "wild_green" / "tools"
TWINS = ("palette.py", "ribbon.py")

findings = []


def fail(where, message):
    findings.append("%s: %s" % (where, message))


def check_shell():
    cart = json.loads((ROOT / "cart.json").read_text(encoding="utf-8"))
    if cart.get("shell") != SHELL:
        fail("cart.json", "shell is %s; tools/palette.py says %s"
             % (cart.get("shell"), SHELL))
    label = cart.get("label")
    if not label:
        fail("cart.json", "no label; the launcher draws a blank cartridge")
    elif not (ROOT / label).is_file():
        fail("cart.json", "label %r is not in the cart directory" % label)


def check_generated():
    """A rebuild has to produce the bytes that are committed."""
    product = ROOT / "label.png"
    if not product.is_file():
        fail("make_label.py", "label.png is missing; run it")
        return
    before = product.read_bytes()
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "make_label.py")],
                         capture_output=True, text=True, cwd=ROOT)
    if run.returncode != 0:
        fail("make_label.py", "exited %d: %s"
             % (run.returncode, run.stderr.strip()))
        return
    if product.read_bytes() != before:
        fail("make_label.py", "label.png is stale; the committed file is not "
                              "what the tool draws")


def check_twins():
    """The files carried in both repositories are still the same file."""
    if not TWIN_ROOT.is_dir():
        print("check: the mod is not in this tree, so its copies of %s are "
              "not checked here -- Gen1makeitgreen checks its own"
              % ", ".join(TWINS))
        return
    for name in TWINS:
        mine, theirs = ROOT / "tools" / name, TWIN_ROOT / name
        if not theirs.is_file():
            fail(name, "no twin at %s" % theirs.relative_to(ROOT))
            continue
        # the docstring names the other repo, so it differs on purpose
        strip = lambda text: text.split('"""', 2)[-1]      # noqa: E731
        if strip(mine.read_text(encoding="utf-8")) != \
                strip(theirs.read_text(encoding="utf-8")):
            fail(name, "has drifted from %s; the two repos must carry the "
                       "same file" % theirs.relative_to(ROOT))


def main():
    check_shell()
    check_generated()
    check_twins()
    for finding in findings:
        print("check: %s" % finding)
    if findings:
        return 1
    print("check: cart.json agrees with the palette, label.png is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check the things that can quietly drift apart in the cart.

    python3 tools/check.py [--online]

Three of them:

  * `cart.json`'s shell is the palette's `DARK`.  The cartridge is the
    colour of the VERSION lettering because they are the same number, not
    because someone matched them by eye once.
  * `label.png` is what `tools/make_label.py` draws from
    `art/wild_green_label.png`.  A committed PNG that the tool no longer
    produces is a picture nobody can regenerate -- and the Gen1Wild index
    serves this same file as the cart's card thumbnail.
  * `tools/palette.py` still matches its twin in the mod's repository.  It
    is carried in two repositories -- neither can import from the other --
    and this is the only thing standing between that and a cart whose shell
    has stopped matching its own title screen.  (`ribbon.py` used to be
    carried here for the same reason; the label no longer letters anything,
    so the mod is now its only home.)

That last one needs the mod's copy, and the mod is not in this tree any
more.  `--online` fetches it from the mod's repository; without the flag
the check says it was skipped rather than pretending it passed.  CI passes
`--online`, so drift is caught there even though a local run is offline --
which is how the two got out of step in the first place: the check went
quiet when the mod moved out, and nothing noticed for eighteen versions.

Exits non-zero on any finding, which is what CI wants.
"""

import json
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from palette import SHELL  # noqa: E402

# the mod's own copies, in the mod's own repository
TWIN_REPO = "wild1walker/Gen1MakeItGreen"
TWIN_RAW = "https://raw.githubusercontent.com/%s/main/tools/%%s" % TWIN_REPO
TWINS = ("palette.py",)

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


def check_twins(online):
    """The files carried in both repositories are still the same file."""
    if not online:
        print("check: --online not given, so %s is not compared against %s"
              % (", ".join(TWINS), TWIN_REPO))
        return
    for name in TWINS:
        mine = (ROOT / "tools" / name).read_text(encoding="utf-8")
        try:
            with urllib.request.urlopen(TWIN_RAW % name, timeout=30) as response:
                theirs = response.read().decode("utf-8")
        except Exception as e:                           # network, 404, ...
            fail(name, "could not read %s's copy: %s" % (TWIN_REPO, e))
            continue
        # the docstring names the other repo, so it differs on purpose
        strip = lambda text: text.split('"""', 2)[-1]      # noqa: E731
        if strip(mine) != strip(theirs):
            fail(name, "has drifted from %s's copy; the two repos must carry "
                       "the same file" % TWIN_REPO)


def main(argv):
    online = "--online" in argv[1:]
    for arg in argv[1:]:
        if arg != "--online":
            print("check: unknown argument %r" % arg)
            return 2
    check_shell()
    check_generated()
    check_twins(online)
    for finding in findings:
        print("check: %s" % finding)
    if findings:
        return 1
    print("check: cart.json agrees with the palette, label.png is current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

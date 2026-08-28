<p align="center">
  <img src="label.png" alt="Wild Green" width="220">
</p>

# Wild Green

**Red, played as its own version.** A [custom cart][carts] for
[gen1recomp][engine]: the [Gen1Wild][index] suite pinned whole, a player who
is green, and a title screen that says `WILD GREEN VERSION`.

A cart is not a mod pack you assemble. It is a named, version-pinned set that
plays as its own game — its own entry in the launcher, its own shell colour
and label, its own save slots. Two people running Wild Green run the same
mods at the same versions.

## What is in it

| | Pinned | What it is |
|---|---|---|
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_qol/thumbnail.png" width="54" alt=""> | **[Gen1WildQOL][qol]** `1.11.1` | The quality-of-life half: sprinting, autosave, auto continue, sound, followers, all 151, EXP share, menu layout, the mod manager and four later-generation conveniences. |
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_ui/thumbnail.png" width="54" alt=""> | **[Gen1WildUI][ui]** `1.12.0` | The visual half: battle backdrops, the battle intro, the Pokédex, the box, the party menu, the bag, item icons and descriptions, the lift panel. |
| | **[Wild Green](mods/wild_green)** `1.0.0` | The version itself: the player in green, and `WILD GREEN VERSION` on the title screen. Written here. |

The seal is **`sealed+`**: the mod set is fixed, and you may switch any of the
three off. That is deliberate — a cart that cannot be taken apart is a cart
you cannot play your own way, and every feature in both bundles already
switches on and off by itself.

The base game is **Red**. The cart carries no game data and no ROM bytes;
you supply your own, exactly as the engine already asks you to.

## Installing it

Download `wild_green-<version>.g1rcart` from
[Releases](https://github.com/wild1walker/Gen1WildGreen/releases) and open it
from the game — **Custom Carts > Import a cart** on desktop, or drop the file
into the `carts` folder of the save directory and the launcher adopts it.

If a pinned mod is missing, the cart's page offers **Install required mods**,
which resolves each pin to its release, checks the archive against the
`sha256` recorded here, and installs it. Reach for that rather than breaking
the seal.

## The green

Four colours, in [`tools/palette.py`](tools/palette.py), and the same four
everywhere they appear — the sprite recolor, the ribbon lettering, the shell
and the label:

| | | |
|---|---|---|
| paper | `#ffffff` | stays pure white: the battle back pic mattes on it |
| light | `#65ba3f` | the reference sprite green |
| dark | `#1e7a2b` | the `VERSION` lettering, **and the cartridge shell** |
| ink | `#000000` | |

The shell is the lettering's own green because they are the same number, not
because they were matched by eye — [`tools/check.py`](tools/check.py) fails
if `cart.json` and the palette ever disagree.

## The label

The [Gen1Wild][index] wordmark with `WILD GREEN VERSION` under it, drawn by
[`tools/make_label.py`](tools/make_label.py). The wordmark is not redrawn: it
is `art/gen1wild_wordmark.png`, the same committed artwork the index's own
banner and favicon are cut from, so the cart and the index stay one object.
The version line reuses the title ribbon's own 5×7 face, so the cartridge and
the title screen are lettered the same way.

## Layout

```
cart.json                  identity, base game, seal, one pin per mod
label.png                  the label the launcher draws        (generated)
art/gen1wild_wordmark.png  the Gen1Wild wordmark, as committed
mods/wild_green/           the mod written here
tools/palette.py           the four colours, once
tools/make_label.py        draws label.png
tools/make_ribbon.py       draws the title ribbon
tools/check.py             the palettes agree; the art is current
tests/                     headless coverage of the mod
```

## Working on it

Everything below is `tools/cartkit.py` from a [gen1recomp][engine] checkout,
pointed at this directory.

```sh
python3 tools/check.py                                  # from this repo
luajit tests/wild_green_test.lua                        # from this repo

python3 /path/to/gen1recomp/tools/cartkit.py validate .          # offline
python3 /path/to/gen1recomp/tools/cartkit.py validate . --online # every pin
python3 /path/to/gen1recomp/tools/cartkit.py pack .              # build it
```

Re-pin a bundle when it cuts a release:

```sh
python3 /path/to/gen1recomp/tools/cartkit.py pin . wild1walker/Gen1WildUI@1.13.0 --id gen1_wild_ui
```

`--id` is not optional. cartkit derives a pin id from the repository name,
which gives `gen1wildui`; the id the loader matches against is the manifest's
`gen1_wild_ui`, and a pin under the wrong id never finds the mod it pinned.

## Releasing

The `wild_green` pin currently carries the placeholder hash, because the mod
it points at has no release yet. Ordering matters, and it is once:

1. Cut the mod's first release, so `wild_green-1.0.0.zip` and its
   `sha256sums.txt` exist.
2. `cartkit pin . wild1walker/<the mod's repo>@1.0.0 --id wild_green`, which
   reads the hash off that release.
3. `cartkit validate . --online --strict` — clean now.
4. Tag `v1.0.0` and push it. [`.github/workflows/cart-release.yml`](.github/workflows/cart-release.yml)
   validates, packs, and attaches `wild_green-1.0.0.g1rcart` with a
   `sha256sums.txt`.

Step 1 needs a decision that is not made here: the stock mod release workflow
and the stock cart release workflow both own the `v*` tag namespace and both
build from the repository root, so the mod and the cart cannot share a
repository without one of them getting a hand-written workflow. See
[CHANGELOG.md](CHANGELOG.md).

Then add an entry under `carts/` in the [Gen1Wild][index] index so the
launcher can find it. The index entry's `repo` names **this** repo, not the
repo of any mod it pins.

## Credits

- **[Gen1Wild][index]** — the suite this is the version of, and the wordmark
  on the label.
- **distilledorion-sketch** — [Crystal Animated Sprites with Shiny
  Visuals][crystal], which Wild Green is meant to sit beside rather than
  replace. It is an optional dependency, not a fork; its art stays its own.
- **[Gen1Recomp][engine]** — the engine, the cart format, and the
  asset-transform sandbox the recolor runs in.
- **pret** — the disassemblies underneath all of it.

## Licence

MIT. See [LICENSE](LICENSE).

[engine]: https://github.com/bryanthaboi/gen1recomp
[carts]: https://github.com/bryanthaboi/gen1recomp/wiki/Guide-Custom-Carts
[index]: https://github.com/wild1walker/Gen1Wild
[ui]: https://github.com/wild1walker/Gen1WildUI
[qol]: https://github.com/wild1walker/Gen1WildQOL
[crystal]: https://github.com/distilledorion-sketch/crystal_animated_sprites_with_shiny_visuals

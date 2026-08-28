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
| | **[Crystal Animated Sprites with Shiny Visuals][crystal]** `2.0.2` | Crystal animated battle sprites, Gen 2-style shiny reveals with the cry held until the sparkle finishes, and swappable trainer portraits. Somebody else's mod, pinned unmodified. |
| | **[Wild Green][mod]** `1.0.0` | The version itself: the player in green, and `WILD GREEN VERSION` on the title screen. Written for this cart. |

The seal is **`sealed+`**: the mod set is fixed, and you may switch any of the
four off. That is deliberate — a cart that cannot be taken apart is a cart
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
tools/palette.py           the four colours
tools/ribbon.py            the WILD GREEN VERSION lettering
tools/make_label.py        draws label.png
tools/check.py             cart.json agrees; the label is current
```

The cart ships no code. The mod that gives it its name lives in
[its own repository][mod], because gen1recomp's stock mod release workflow
and its stock cart release workflow both trigger on `v*` tags and both build
from the repository root, and cartkit resolves a pin only against a
`v<version>` or `<version>` tag whose release carries
`<mod-id>-<version>.zip`. Two artifacts cannot share that namespace.

`tools/palette.py` and `tools/ribbon.py` are carried in [the mod's repo][mod]
too — the cartridge's shell and the title screen's lettering are the same
four numbers and the same 5×7 face, and neither repo can import from the
other. Change one, change both.

## Working on it

Everything below is `tools/cartkit.py` from a [gen1recomp][engine] checkout,
pointed at this directory.

```sh
python3 tools/check.py                                  # the cart's own gate

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

Bump `version` in `cart.json`, tag it `v<version>`, and push the tag.

When the mod cuts a release, re-pin it the same way a bundle is re-pinned:

```sh
python3 /path/to/gen1recomp/tools/cartkit.py pin . \
  wild1walker/Gen1MakeItGreen@1.0.1 --id wild_green
```

Then:

1. `cartkit validate . --online --strict` — every pin resolves and hashes.
2. Tag `v<version>` and push it.
   [`.github/workflows/cart-release.yml`](.github/workflows/cart-release.yml)
   validates, packs, and attaches `wild_green-<version>.g1rcart` with a
   `sha256sums.txt`.

Then add an entry under `carts/` in the [Gen1Wild][index] index so the
launcher can find it. The index entry's `repo` names **this** repo, not the
repo of any mod it pins.

## Credits

- **[Gen1Wild][index]** — the suite this is the version of, and the wordmark
  on the label.
- **distilledorion-sketch** — [Crystal Animated Sprites with Shiny
  Visuals][crystal], pinned here unmodified rather than forked. Wild Green
  sits beside it and does not touch its art or its `PLAYER SPRITE` row.
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
[mod]: https://github.com/wild1walker/Gen1MakeItGreen

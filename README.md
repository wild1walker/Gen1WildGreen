<p align="center">
  <a href="https://wild1walker.github.io/Gen1Wild/"><img src="art/banner.png" alt="Gen1Wild — Wild Green Version. Check out my other mods!" width="880"></a>
</p>

# Wild Green

**Red, played as its own version.** A [custom cart][carts] for
[gen1recomp][engine]: the [Gen1Wild][index] suite pinned whole, a player who
is green, and a title screen that says `WILD GREEN VERSION`.

The suite's two halves are [Gen1WildUI][ui] and [Gen1WildQOL][qol]. This is
not a third half — it is those two, plus one more mod and one more of
somebody else's, fixed at exact versions and given a name. A cart is not a
mod pack you assemble: it is its own entry in the launcher, its own shell
colour and label, its own save slots. Two people running Wild Green run the
same mods at the same versions.

## What is in it

| | Pinned | What it is |
|---|---|---|
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_qol/thumbnail.png" width="54" alt=""> | **[Gen1WildQOL][qol]** | The quality-of-life half: sprinting, autosave, auto continue, sound, followers, all 151, EXP share, remembered moves, menu layout, the mod manager and four later-generation conveniences. |
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_ui/thumbnail.png" width="54" alt=""> | **[Gen1WildUI][ui]** | The visual half: battle backdrops, the battle intro, the Pokédex, the box, the party menu, the bag, item icons and descriptions, the lift panel. |
| | **[Crystal Animated Sprites with Shiny Visuals][crystal]** | Crystal animated battle sprites, Gen 2-style shiny reveals with the cry held until the sparkle finishes, and swappable trainer portraits. Somebody else's mod, pinned unmodified. |
| | **[Wild Green][mod]** | The version itself: the player in green wherever the game draws him, and `WILD GREEN VERSION` on the title screen. Written for this cart. |

Exact versions are in [`cart.json`](cart.json), which is the only place they
are written down. Nothing else in this repository repeats them, because a
second copy is a copy that goes stale.

The seal is **`sealed+`**: the mod set is fixed, and you may switch any of
the four off. That is deliberate — a cart that cannot be taken apart is a
cart you cannot play your own way, and every feature in both bundles already
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

[`tools/palette.py`](tools/palette.py) is where every colour in the version
is written down, and the same file is carried in [the mod's repo][mod] — the
cartridge shell and the title screen's lettering are the same numbers, and
neither repository can import from the other.

| | | |
|---|---|---|
| paper | `#ffffff` | stays pure white: the battle back pic mattes on it |
| skin | `#f0a363` | the face, the ear, the hands |
| outfit | `#65ba3f` | the cap and the jacket — the reference sprite's green |
| ink | `#000000` | |
| lettering | `#2e8b3a` / `#14571f` | `VERSION` on the title screen, **and the cartridge shell** |

The shell is the lettering's own green because it is the same number, not
because the two were matched by eye — [`tools/check.py`](tools/check.py)
fails if `cart.json` and the palette ever disagree, and with `--online` it
also fails if this repository's palette has drifted from the mod's.

## The label

<p align="center">
  <img src="label.png" alt="The Wild Green cartridge label" width="200">
</p>

[`art/wild_green_label.png`](art/wild_green_label.png), scaled to 256×256 by
[`tools/make_label.py`](tools/make_label.py). The artwork already carries the
[Gen1Wild][index] wordmark with `WILD GREEN VERSION` under it, so scaling it
is the whole job — nothing is composited and no lettering is drawn.

The same file is the cart's card in the [Gen1Wild][index] index: the index
fetches whatever `cart.json`'s `label` names and writes it in as the
thumbnail, so the cartridge and the card are one picture rather than two that
have to be kept alike by hand.

## Layout

```
cart.json                     identity, base game, seal, one pin per mod
label.png                     the label the launcher draws     (generated)
art/wild_green_label.png      the cartridge artwork, as committed
art/banner.png                the README's banner; links to the index
tools/palette.py              every colour, twinned with the mod's copy
tools/make_label.py           draws label.png
tools/check.py                cart.json agrees; the label is current
```

The cart ships no code. The mod that gives it its name lives in
[its own repository][mod], because gen1recomp's stock mod release workflow
and its stock cart release workflow both build from the repository root, and
cartkit resolves a pin only against a `v<version>` or `<version>` tag whose
release carries `<mod-id>-<version>.zip`. Two artifacts cannot share that
namespace.

## Working on it

```sh
python3 tools/check.py             # the cart's own gate
python3 tools/check.py --online    # ...and the palette against the mod's
```

Everything else is `tools/cartkit.py` from a [gen1recomp][engine] checkout,
pointed at this directory:

```sh
python3 /path/to/gen1recomp/tools/cartkit.py validate .          # offline
python3 /path/to/gen1recomp/tools/cartkit.py validate . --online # every pin
python3 /path/to/gen1recomp/tools/cartkit.py pack .              # build it
```

Re-pin a mod when it cuts a release:

```sh
python3 /path/to/gen1recomp/tools/cartkit.py pin . \
  wild1walker/Gen1MakeItGreen@1.20.0 --id wild_green
```

`--id` is not optional. cartkit derives a pin id from the repository name,
which gives `gen1makeitgreen`; the id the loader matches against is the
manifest's `wild_green`, and a pin under the wrong id never finds the mod it
pinned.

Never hand-edit a version string in `cart.json`. The `gen1_wild_ui` pin spent
six versions reading `1.13.0` — a version that repository never released,
carrying the digest of `wild_green-1.13.0.zip` — because a script matched the
first `"version"` under `mods` and rewrote the wrong entry. `cartkit pin`
addresses the entry by id, and `validate --online --strict` is what finally
caught it.

## Releasing

**Bump `"version"` in `cart.json` and push to `main`. That is all of it.**

[`.github/workflows/cart-release.yml`](.github/workflows/cart-release.yml)
runs on every push, validates every pin against the real releases, packs the
cart, and publishes `wild_green-<version>.g1rcart` with a `sha256sums.txt` —
creating the `v<version>` tag as it does, so nobody has to push one. A push
whose version is already released resolves it, sees the tag, and stops.

Nothing is tagged before validation passes, so a cart pointing at an
unpublished mod fails the run rather than leaving a stray tag behind. A tag
pushed by hand still works, and is still checked against `cart.json`.

The [Gen1Wild][index] index rebuilds hourly, reads the pins out of this
repository's `cart.json`, and re-fetches `label.png` as the card's thumbnail.
Nothing there needs touching when this releases.

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

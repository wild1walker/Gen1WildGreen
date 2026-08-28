# Changelog

All notable changes to this cart are recorded here, newest first.

## [1.1.1] - unreleased

### Changed

- Wild Green re-pinned to `1.1.1`: the player's skin is a warm tan measured
  off the reference rather than the pale cream 1.1.0 shipped, and the title
  screen's standing figure is left vanilla — `TitleState` bakes the OBJ
  palette onto it and gives it no `trueColor` seam, so recoloured art came
  back white and pink. The ribbon carries that screen on its own.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.0] - 2026-08-28

### Changed

- **The shell is `#14571f`**, not `#1e7a2b`. The cartridge follows the
  `VERSION` lettering, and Wild Green 1.1.0 darkened that lettering because
  the first cut washed out on the title screen. `label.png` is redrawn to
  match; `tools/check.py` would have failed the build if it were not.
- Wild Green re-pinned to `1.1.0`, which fixes the four things 1.0.0 got
  wrong on screen — the player only changing in the overworld, the overworld
  player being green all over instead of green-clothed, the pale title
  lettering, and a `field.boot` double-patch that silently cost the default
  name. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.0.0] - 2026-08-28

### Added

- The Wild Green cart: base `red`, seal `sealed+`, shell `#1e7a2b`, pinning
  Gen1WildQOL `1.11.1`, Crystal Animated Sprites with Shiny Visuals `2.0.2`,
  Gen1WildUI `1.12.0` and Wild Green `1.0.0` in that load order — which is
  their own priority order (100, 980, 1100, 1300), so the cart is not
  fighting the loader about it.
- `label.png` — the Gen1Wild wordmark with `WILD GREEN VERSION` under it, on
  the shell green, drawn by `tools/make_label.py` from the committed wordmark
  and the same 5×7 face the mod letters its title ribbon with.
- `tools/` — the four colours (`palette.py`), the lettering (`ribbon.py`),
  the label generator, and the check that keeps `cart.json`'s shell, the
  committed label and the files shared with the mod's repo honest.
- The `wild_green` pin, at [wild1walker/Gen1MakeItGreen][mod] — the mod that
  makes this a version rather than a mod list. It was staged in this repo
  while it had nowhere else to be; it now lives in its own repository,
  because gen1recomp's stock mod release workflow and its stock cart release
  workflow both trigger on `v*` tags and both build from the repository root,
  and cartkit resolves a pin only against a `v<version>` or `<version>` tag
  whose release carries `<mod-id>-<version>.zip`. Two artifacts cannot share
  that namespace, and a prefixed tag scheme is not a way out of it either.

### Notes

- The two bundle hashes were resolved from each release's own
  `sha256sums.txt` and checked against it a second time by hand:
  `gen1_wild_ui-1.12.0.zip` is `c4015d0b…a4a536`, `gen1_wild_qol-1.11.1.zip`
  is `18959ac0…15f9027`.
- The Crystal Animated Sprites release publishes no `sha256sums.txt`, so its
  pin carries the digest of the asset itself — `59b6204e…1aca86c` over
  `crystal_animated_sprites_with_shiny_visuals_v2.0.2.zip`, 6,044,763 bytes,
  which is what cartkit computes when it falls back to downloading. Its
  archive puts `manifest.json` at the root, so it installs the way the game
  expects. It is pinned unmodified: nothing here forks it or ships its art.
- `ribbon` is frozen on in the cart's pin; `player` deliberately is not, so
  `GREEN` / `RED` stays the player's to choose.
- The greens are sampled from the reference art, not picked: `#65ba3f` is the
  bright green the reference overworld character's body reads as, and
  `#1e7a2b` is that green taken down to the weight vanilla's `Red Version`
  lettering carries against white.

[mod]: https://github.com/wild1walker/Gen1MakeItGreen

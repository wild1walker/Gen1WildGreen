# Changelog

All notable changes to this cart are recorded here, newest first.

## [1.0.0] - unreleased

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
- `mods/wild_green/` — **staged, not home.** A complete repository root for
  the mod: the player in green, recolored from the player's own imported
  cache, and `WILD GREEN VERSION` on the title screen, with its own `tools/`,
  `tests/` (50 headless checks), `LICENSE` and release workflow. It has its
  own [README](mods/wild_green/README.md) and
  [DIFFERENCES](mods/wild_green/DIFFERENCES.md).

### Open

- **The mod has no repository yet.** It belongs in
  `wild1walker/Gen1makeitgreen`, which could not be created from here — the
  integration is not permitted to create repositories. Everything else is
  done: the directory is a repository root, nothing in the cart's tooling
  reaches into it except the twin-file check, and moving it is a copy, a
  push, and a delete. [README.md](README.md#releasing) has the order.

  It needs its own repository rather than a subdirectory because gen1recomp's
  stock mod release workflow and its stock cart release workflow both trigger
  on `v*` tags and both build from the repository root, and cartkit resolves
  a pin only against a `v<version>` or `<version>` tag whose release carries
  `<mod-id>-<version>.zip`. Two artifacts cannot share that namespace, and a
  prefixed tag scheme is not a way out of it either.

- **The `wild_green` pin carries the placeholder hash**, because cartkit
  reads a hash off a release and the mod has none yet. `cartkit validate .`
  passes with a warning; `--strict` does not, which is the release workflow's
  gate and is the correct behaviour until the pin is resolved.

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

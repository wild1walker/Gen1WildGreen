# Changelog

All notable changes to this cart are recorded here, newest first.

## [1.0.0] - unreleased

### Added

- The Wild Green cart: base `red`, seal `sealed+`, shell `#1e7a2b`, pinning
  Gen1WildQOL `1.11.1`, Gen1WildUI `1.12.0` and Wild Green `1.0.0` in that
  load order.
- `mods/wild_green/` — the mod that makes it a version rather than a mod
  list: the player in green, recolored from the player's own imported cache,
  and `WILD GREEN VERSION` on the title screen. It has its own
  [README](mods/wild_green/README.md) and
  [DIFFERENCES](mods/wild_green/DIFFERENCES.md).
- `label.png` — the Gen1Wild wordmark with `WILD GREEN VERSION` under it, on
  the shell green.
- `tools/` — the palette, the two art generators, and the check that keeps
  the three copies of the palette and the two generated PNGs honest.
- `tests/wild_green_test.lua` — 50 headless checks over the mod.

### Open

- **The `wild_green` pin carries the placeholder hash.** It is resolved by
  `cartkit pin` once the mod has a release to read a hash off, which cannot
  happen before the next item is decided. `cartkit validate .` passes with a
  warning; `--strict` does not, which is the release workflow's gate and is
  the correct behaviour until this is closed.
- **The mod needs a home.** gen1recomp's stock mod release workflow and its
  stock cart release workflow both trigger on `v*` tags and both build from
  the repository root, so a cart and a mod cannot share a repository on
  stock tooling. cartkit resolves a pin only against a `v<version>` or
  `<version>` tag whose release carries `<mod-id>-<version>.zip`, so a
  prefixed tag scheme is not a way out of it either. Two ways to close it:

  - give `mods/wild_green/` its own repository, which is the shape the wiki
    describes and the shape Gen1WildUI and Gen1WildQOL already have; or
  - keep one repository and hand-write one of the two workflows.

  Nothing else in here changes either way — the mod's files, the cart's
  fields and the load order are the same in both.

### Notes

- The two bundle hashes were resolved from each release's own
  `sha256sums.txt` and checked against it a second time by hand:
  `gen1_wild_ui-1.12.0.zip` is `c4015d0b…a4a536`, `gen1_wild_qol-1.11.1.zip`
  is `18959ac0…15f9027`.
- `ribbon` is frozen on in the cart's pin; `player` deliberately is not, so
  `GREEN` / `RED` stays the player's to choose.

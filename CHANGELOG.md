# Changelog

All notable changes to this cart are recorded here, newest first.

## [1.7.0] - 2026-08-28

### Fixed

- Wild Green re-pinned to `1.7.0`, which fixes the two things that made
  `1.4.0` and `1.5.0` change nothing on screen:

  - **The title figure's bake never ran.** It read the art with
    `Image:getData`, and under LÖVE 11 a graphics `Image` does not keep the
    `ImageData` it was built from and has no `getData` at all. The call
    failed on the first frame and the failure was cached, so the figure kept
    the red bake from Crystal Animated Sprites. The pixels come off a canvas
    now.
  - **`PORTRAIT SKIN` never fired.** It looked for the face by the eyes
    inside it, and the real card has no such shape — the art is dithered and
    the eyes are part of the outline. The rule now comes from the card's
    real shade map: a patch of at least six pixels with at least two white
    neighbours is skin, which is the face and the hands and not the solid
    19px patch of shading inside the cap.

  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.7.0.zip` is `a27b00df…3df4f06`, from the release's own `sha256sums.txt`.

## [1.5.0] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.5.0`, which adds a **`PORTRAIT SKIN`** row: the
  face on the big pictures is the character's own skin instead of the light
  green, while the cap, the shirt's shading and the knees — all the same
  shade — keep the green. The face is picked out by the eyes inside it
  rather than by its colour, and the rule fails closed: where it does not
  find exactly one face the picture is the flat green of 1.4.0, so the worst
  it can do is nothing.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.5.0.zip` is `83e05b74…3c37a79`, from the release's own
  `sha256sums.txt`.
- `PORTRAIT SKIN` is deliberately **not** frozen in the cart's pin, the same
  way `player` is not: both are the player's to choose.

## [1.4.0] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.4.0`: the title screen's standing figure is
  green under `ADVANCED`, which is the one place he had stayed red through
  every release. `ADVANCED` does not run the SGB zone pass over his
  rectangle, so the `MEWMON` override could never reach him — and Crystal
  Animated Sprites, pinned here, bakes his grey art to Red's own colours
  there. Wild Green now wraps `TitleState.currentSprite` outside that
  wrapper and re-bakes him in the trainer card's ramp.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- This is the first cart tag since `v1.1.0`, so it carries `1.2.0` and
  `1.3.0` with it — the 940 priority fix that reached the large sprites, the
  green-tinted bill, and the trainer art's own ramp. Nothing in the cart
  itself changed across those three but the `wild_green` pin.
- The pin's digest is the one the release's own `sha256sums.txt` publishes,
  checked against the asset's digest a second time:
  `wild_green-1.4.0.zip` is `9ecdc422…5a9c62b`.

## [1.3.0] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.3.0`: the trainer art takes its own ramp —
  white, light green, green, black — instead of the overworld sprite's, so
  the battle back pic, the trainer card, Oak's intro and the Hall of Fame
  come out clean rather than blotched with orange and red. Four more of the
  player's pictures are covered, and the recipe and the hook now share one
  list so a swap can never point at a picture the recipe did not write.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.2.0] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.2.0`, which finally reaches the large sprites.
  Crystal Animated Sprites — pinned here too — wraps `player.sprite` at
  priority 930 and short-circuits the chain, and Wild Green's link took the
  default `0`, so it was never called: the battle back pic, the trainer card,
  Oak's intro and the Hall of Fame stayed red through every release from
  1.0.0 on. It wraps at 940 now.

  The two mods still cooperate everywhere else. The one place they no longer
  do is the player's own portrait: on `PLAYER = GREEN` it is Wild Green's
  recoloured vanilla art, so a portrait chosen in
  `CRYSTAL SPRITES > PLAYER SPRITE` does not reach the player. `PLAYER = RED`
  hands it back.
- The cap's bill is a green-tinted white, and is found by region rather than
  by row. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.4] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.4`: the lips are vanilla's red again rather
  than painted out, and the cap's bill goes with the hat in profile as well
  as facing down. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.3] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.3`: the cap's bill goes with the hat instead
  of taking the face's colour. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.2] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.2`: the player's mouth is skin rather than
  green, and the title screen's standing figure is green again — coloured
  through the `MEWMON` zone palette rather than by swapping the pic, which
  takes the `GAME FREAK` line green with it and is on a `TITLE FIGURE` row of
  its own. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.1] - superseded by 1.7.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.1`: the player's skin is a warm tan measured
  off the reference rather than the pale cream 1.1.0 shipped, and the title
  screen's standing figure is left vanilla — `TitleState` bakes the OBJ
  palette onto it and gives it no `trueColor` seam, so recoloured art came
  back white and pink. The ribbon carries that screen on its own.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

  **That reason is wrong, and 1.4.0 says so.** The white-and-pink figure was
  Crystal Animated Sprites' own luminance bake reading Wild Green's art, not
  the engine's shade buckets.

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

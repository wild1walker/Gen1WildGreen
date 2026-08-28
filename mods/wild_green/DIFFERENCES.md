# Differences from vanilla

In the format of the engine's `docs/known-differences.md`. The base game's
own ledger stays "None currently"; these are this mod's divergences.

## Art

- **The player is green.** The overworld walker, the `BICYCLE` sheet where
  the import wrote one, the battle back pic, the front pic that Oak's intro,
  the trainer card and the Hall of Fame share, and the standing figure on the
  title screen are recolored from the player's own imported cache to the Wild
  Green ramp. `PLAYER = RED` turns all of it off.
- **The title screen reads `WILD GREEN VERSION`.** One continuous ribbon in
  place of the imported pair of fragments. `TITLE RIBBON = OFF` gives back
  the imported art.
- **`LOGO1` is overridden** to the Wild Green ramp. It is the SGB palette the
  title's version-ribbon band wears, and the title screen is the only thing
  that reads it.

## Known limits

- **The green band is a registry record only under SGB.** `PaletteFX.pal`
  (`src/render/PaletteFX.lua`) short-circuits every named palette to the
  boot-ROM pair under `OG RED`, and reads `data/palettes_gbc` under
  `ADVANCED`. In those two display modes the ribbon band keeps that mode's
  own colour, so the lettering still says `WILD GREEN VERSION` but is drawn
  in red. Nothing a mod can reach decides those two.
- **The recolored art is true-colour.** `trueColor` is what keeps the
  overworld's OBP bake from reading our green through the shade buckets it
  reads grey art through. The mono and inverted display modes do not honour
  `trueColor` (`PaletteFX.honorsTrueColor`), so there the player falls back
  to the baked ramp like any other sprite.
- **`PLAYER` takes effect on the next launch.** It decides a `sprites`
  record, and records are settled at load.
- **A cache without one of the five pictures leaves that picture alone.**
  The recipe skips what `ctx.exists` says is not there, and `main.lua` only
  repoints a record whose art it actually recolored — so a partial import
  degrades one picture at a time instead of drawing nothing.

## Not changed

No map, script, encounter, trainer, item, move or battle behaviour. Nothing
here is read by anything but the renderer, and the mod declares no
`permissions` at all.

## Save data

None. The mod stores nothing in the save; its two rows live in the profile's
mod options like any other. Uninstalling it leaves a save that loads exactly
as it did.

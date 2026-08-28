# Wild Green

**The player is green and the title screen says so.** That is the whole mod.

It is the identity half of the [Wild Green](../../README.md) cart: the cart
pins [Gen1WildUI](https://github.com/wild1walker/Gen1WildUI) and
[Gen1WildQOL](https://github.com/wild1walker/Gen1WildQOL) for everything a
playthrough actually does, and this supplies the one thing a pinned mod set
cannot — a game that looks like its own version rather than like Red with
things added.

It works on its own too. Nothing here depends on either bundle.

## What it changes

| | |
|---|---|
| the overworld walker | `SPRITE_RED`, and the `BICYCLE` sheet where the import wrote one |
| the battle back pic | the one drawn at 2x until "Go!" |
| the front pic | Oak's intro, the trainer card, the Hall of Fame |
| the title screen | the standing figure, and the version ribbon |

The ribbon is one continuous strip reading **WILD GREEN VERSION**, where the
vanilla art is two fragments the title code repositions. It is drawn by
[`tools/make_ribbon.py`](../../tools/make_ribbon.py) on the importer's four
grey shades, and the green arrives from the `LOGO1` palette this mod
overrides — the SGB palette the title's ribbon band wears.

## The two rows

In the mod manager, or in `OPTION > MODS`:

```
WILD GREEN
  PLAYER          GREEN     <- or RED
  TITLE RIBBON    ON
```

- **`PLAYER`** is the switch back. `RED` gives you the vanilla character
  everywhere — no recolor is applied at all, and the vanilla art was never
  overwritten to begin with. It decides a `sprites` record, which is settled
  at load, so it takes effect on the next launch.
- **`TITLE RIBBON`** is the branding, and it is independent of `PLAYER`.
  Off gives back the imported ribbon and the imported band colour. On, the
  title says `WILD GREEN VERSION` whichever colour the character is —
  that is the game's name, not the character's outfit.

## No green pixel ships

The player's four pictures are the vanilla ones, so this mod may not ship
them ([Art Pipeline](https://github.com/bryanthaboi/gen1recomp/wiki/Guide-Art-Pipeline),
"The rule"). Derived art travels as a recipe, and the pixels come from your
own imported cache. [`transforms.lua`](transforms.lua) is that recipe: it
runs once on install, and again only when the cache is re-imported or the
recipe changes.

Its outputs go under a `green/` prefix rather than over the cache paths they
were read from. Writing `sprites/red.png` would make the player green
everywhere, always, and would take the `PLAYER` row away — there would be no
red art left to switch back to. Under `green/` they shadow nothing, and both
sets exist the whole time; `main.lua` points the records at one or the other.

## The palette

Four colours, in [`tools/palette.py`](../../tools/palette.py), and the same
four everywhere they appear — the sprite recolor, the ribbon lettering, the
cart's shell and the cart's label:

| | | |
|---|---|---|
| paper | `#ffffff` | stays pure white: the battle back pic mattes on it |
| light | `#65ba3f` | the reference sprite green |
| dark | `#1e7a2b` | the `VERSION` lettering, and the cartridge shell |
| ink | `#000000` | |

They are written out three times — once in Python, twice in Lua — because
none of the three can import from the others: the transform runs in a sandbox
with no `require`, an entry chunk cannot require its own files, and the tools
are Python. [`tools/check.py`](../../tools/check.py) fails the build if they
drift apart.

## Alongside other mods

`crystal_animated_sprites_with_shiny_visuals` is an optional dependency, not
a fork. It ships its own player portraits and its own `PLAYER SPRITE` row;
this mod does not touch them, and with both installed you get its Crystal
artwork with this mod's overworld and title work around it.

More generally, a walker whose art is not the vanilla path is left where it
points. If another mod has already reskinned the player, this one declines
rather than fighting it.

## Tests

```sh
luajit tests/wild_green_test.lua   # from the repository root
```

Stands up the loader's `mod` table and the asset sandbox's `ctx`, runs the
real files against them, and checks everything settled before a pixel is
drawn — including that `PLAYER = RED` writes no character patch at all.

## Credits

- **distilledorion-sketch** — [Crystal Animated Sprites with Shiny
  Visuals](https://github.com/distilledorion-sketch/crystal_animated_sprites_with_shiny_visuals),
  which this is meant to sit beside rather than replace.
- **Gen1Recomp** — the mod API, the asset-transform sandbox this recolor runs
  in, and the title screen it draws on.
- **pret** — the disassemblies underneath all of it.

## Licence

MIT, same as the rest of the suite. See [LICENSE](../../LICENSE).

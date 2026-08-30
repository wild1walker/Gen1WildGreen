<p align="center">
  <a href="https://wild1walker.github.io/Gen1Wild/"><img src="art/banner.png" alt="Gen1Wild — Wild Green Version. Check out my other mods!" width="880"></a>
</p>

# Wild Green

**This is, I think, the definitive way to play Red.**

Every quality-of-life and visual upgrade in the [Gen1Wild][index] suite, in
one cart — and only the ones that still feel like Red. That was the whole
filter. Sprinting, autosave, a Pokédex worth opening, a bag with pockets,
battle backdrops, animated Crystal sprites, a Pokémon walking behind you: none
of it turns this into a different game. It is the game you remember, with the
parts that made you put it down taken out.

**And you can catch every single one of them.** All 151, in one save, on one
version, without trading — the legendaries retryable until you land them, the
trade evolutions handled by an item, Mew waiting behind the Mansion journals
where it always should have been. Every encounter the cartridge already had
still behaves exactly as it always did.

So if you are going for a 100% Kanto dex, or you just want Red to feel like a
game made this decade, Wild Green is the most enjoyable way to do it.

## It is a version, not a mod list

Wild Green is a [custom cart][carts] for [gen1recomp][engine]: a fixed set of
mods that plays as its own game, with its own entry in the launcher, its own
cartridge and label, and its own save slots. Nothing here writes into your
base Red saves. Two people running Wild Green are running the same game.

| | Pinned | What it is |
|---|---|---|
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_qol/thumbnail.png" width="54" alt=""> | **[Gen1WildQOL][qol]** | Everything that makes Red *play* better: sprinting, autosave, auto continue, sound, followers, all 151, EXP share, the move reminder, menu layout, the mod manager and four later-generation conveniences. |
| <img src="https://raw.githubusercontent.com/wild1walker/Gen1Wild/main/mods/Wild@gen1_wild_ui/thumbnail.png" width="54" alt=""> | **[Gen1WildUI][ui]** | Everything that makes Red *look* better: battle backdrops, the battle intro and menus, the Pokédex, the box, the party menu, the bag, item icons and descriptions, the lift panel. |
| | **[Crystal Animated Sprites with Shiny Visuals][crystal]** | Crystal animated battle sprites, Gen 2-style shiny reveals, and swappable trainer portraits. Somebody else's mod, pinned as it is. |
| | **[Wild Green][mod]** | The version itself: the player in green wherever the game draws him, and `WILD GREEN VERSION` on the title screen. Written for this cart. |

The mod set is sealed: these four run exactly as pinned, and nothing can be
added to them or taken out. That is what makes the cart playable online, where
both sides have to be running the same game; the launcher's **ONLINE** tab
lists sealed carts and nothing else. Every feature inside the four is still a
switch you can flip, so the cart is still yours to play your own way.

If you want it with your own mods instead, break the seal on a save slot from
the cart's page. That save loads the pinned four first and then everything else
you have enabled. It is marked modified, and it cannot go online.

The green is derived from Red's own art rather than shipped, so switching back
to `PLAYER = RED` gives you the original character with nothing to reinstall.

The base game is **Red**. The cart carries no game data and no ROM bytes; you
bring your own, exactly as the engine already asks.

## Installing it

Download `wild_green-<version>.g1rcart` from
[Releases](https://github.com/wild1walker/Gen1WildGreen/releases) and open it
from the game — **Custom Carts > Import a cart** on desktop, or drop the file
into the `carts` folder of your save directory and the launcher picks it up.

If a pinned mod is missing, the cart's own page offers **Install required
mods** and fetches them for you. Reach for that rather than breaking the seal.

## If you want to test what is coming

This cart does not move while a change is being worked on. New work goes to a
**nightly** channel instead, and it is a separate thing you install on purpose:

**MODS > FIND MODS**, add `wild1walker/Gen1NightlyIndex`.

The nightly cart is **Wild Green Nightly** — a dark purple cartridge with
`NIGHTLY` under the wordmark, so the two are never confused on a shelf. Every
mod in it carries an id of its own and conflicts with the one here, so running
a nightly cannot touch this cart, its settings or its saves; and because it is
a cart of its own, it has save slots of its own too.

They are test builds and can be broken in ways a release is not. That is the
whole point of them, and it is the only reason to install one.

The index is [Gen1NightlyIndex][nightlyindex] and the source is
[Gen1NightlyMods][nightlymods].

## Credits

- **[Gen1Wild][index]** — the suite this is the version of, and the wordmark
  on the label.
- **distilledorion-sketch** — [Crystal Animated Sprites with Shiny
  Visuals][crystal], pinned here unmodified rather than forked.
- **[Gen1Recomp][engine]** — the engine and the cart format.
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
[nightlyindex]: https://github.com/wild1walker/Gen1NightlyIndex
[nightlymods]: https://github.com/wild1walker/Gen1NightlyMods

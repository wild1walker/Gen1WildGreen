# Changelog

All notable changes to this cart are recorded here, newest first.

## [1.43.2] - 2026-08-31

### Fixed

- **The black square outline around the character on the way into a battle.**
  Reported on the live cart. A full-colour overworld sprite marks a rectangle
  to be re-blitted raw, out of the colorize pass, and that rectangle was
  rounded outward twice — once by the mod, once by the renderer's scissor,
  which rounds every zone outward on purpose so two SGB zones share an edge.
  The margin is background, and background left out of the pass is invisible
  until the ground changes: the battle wipe takes the ground and leaves the
  ring. `ADVANCED` and `LIGHT` only, which is what named the cause.

  Via Gen1Follower 1.6.1 and Gen1WildQOL 1.27.2.

## [1.43.1] - 2026-08-31

### Fixed

- **`DIAGNOSTIC` and `FIELD TEST` are off the arena menu again.** 1.43.0's
  Gen1WildUI was assembled from the nightly channel's fork, which flips
  Gen1Arena's developer gate on purpose — the nightly *is* the developer build.
  The flip came across with everything else, so 1.43.0 put two debug rows in
  front of every player. Gen1WildUI 1.22.1 puts the gate back.

### Changed

- Re-pinned to **Gen1WildUI 1.22.1** and **Gen1WildQOL 1.27.1**, which retire
  the overlays 1.43.0's bundles were carrying. All nine features they overlaid
  have cut releases of their own — Gen1Dex 1.10.0, Gen1Arena 0.22.0,
  Gen1ModernBag 1.12.0, Gen1BattleUI 1.6.0, Gen1BillsBox 1.6.0, Gen1Party
  1.8.0, Gen1MenuManager 0.4.0, Gen1AutoSave 1.18.0, Gen1Follower 1.6.0 — so
  anyone installing those mods standalone gets the same fixes the cart has.

Nothing else a player sees changes: the bundles' `modules/` are byte-identical
to 1.43.0 apart from the gate above and two internals published for testing.

## [1.43.0] - 2026-08-31

### Changed

- The cart picks up everything the nightly channel built, promoted onto the
  stable line: **Gen1WildQOL 1.27.0**, **Gen1WildUI 1.22.0** and **Wild Green
  1.27.0**.
- The headline is **`UI THEME`** — a row on the game's own `OPTION` screen
  giving `LIGHT`, `DARK` or `COLORFUL`. It swaps the four colours the SGB pass
  gives a zone rather than redrawing anything, so it reaches the whole suite
  and the game underneath it: the `START` menu, the bag, dialogue over the
  map, the town map, the battle menus. `COLORFUL` is work in progress and the
  row says so.
- **`INSPECT` on the town map**: stand on a place and ask what lives in it,
  richest share first, read off the live encounter tables. `A` on a row opens
  that POKéMON's `AREA` map.
- **`TRAINER REMATCH`**: talk to a trainer you have beaten, read them out with
  `A`, and fight them again.
- **`ITEM INFO` reaches the mart** — `BUY` and `SELL` get descriptions, icons
  and the ball column.
- **`PLAYER` takes effect where you are standing**, rather than on the next
  launch, and the version ribbon follows the colour it is set to.
- **The dex stops naming POKéMON you have never met** — the evolution rows,
  the `AREA` header and the `AREA` caption alike.

Each mod's own changelog has the full list.

- `tools/palette.py` comes across with Wild Green 1.27.0: `LOGO1`, the title
  ribbon's band, is lettered in the character's own outfit colour now rather
  than always green, so the two copies of that file agree again.

## [1.42.0] - 2026-08-30

### Changed

- **`PLAYER` is the first row in the menu.** The player's own colour is the
  reason this cart is called what it is, and reaching it read
  `WILD GREEN > OTHER MODS > MAKE IT GREEN > PLAYER` — three doors deep,
  behind the repository's name rather than the setting's. It is now
  `WILD GREEN > PLAYER`, above the six cards and above the manager.
  `OTHER MODS` goes back to meaning the mods you installed yourself.

### Fixed

- **The youngster stops hopping his way to Brock's gym.** Two separate faults
  wore the same face, and the second is the one that was actually happening
  on this cart.

  The first: an NPC's tile takes thirty-two frames — NPCs move at half your
  speed in Gen 1 — while the walk cycle was a flat sixteen, so a wandering or
  departing NPC took *two* steps per tile. The cycle is tied to the step now,
  one per tile, foot alternating. That is `NPC WALK`, and it is live.

  The second is the escort, and it is `SPRINT`'s. `stepFramesCur` is the
  engine's "how long is the step in flight", and the escort scripts read it as
  "how fast does the player move" to pin the guide's own step to it. Begin an
  escort with **B held** and the guide was pinned to the *sprinting* length
  while the escort's own scripted steps refused the sprint and ran at the
  *walking* one — so he darted a tile in half the frames and stood frozen for
  the other half, a tile at a time, the whole way there:

  ```
  in step      ...LLLLLLLL...._...LLLLLLLL...._
  pinned to 8  ...LLLL_________LLL...._________
               ( . standing, L stepping, _ arrived and waiting )
  ```

  A sprinted step no longer outlives its step. (Gen1WildQOL 1.26.0,
  Gen1WildUI 1.21.0, Gen1Sprint 0.3.1.)

## [1.41.0] - 2026-08-30

### Added

- **`PLAYER` is ten colours.** `GREEN` and `RED` as before, plus `ORANGE`,
  `BLUE`, `PURPLE`, `YELLOW`, `PINK`, `BLACK`, `WHITE` and `GREY`.

  Only the **outfit** changes between them. The skin, the lips, the paper and
  the black outline are the same in all nine recoloured suits — which is what
  makes a colour a change of clothes rather than a change of person. Every
  picture follows: the overworld walker and the `BICYCLE` sheet, the battle
  back pic, the trainer card, Oak's intro, the credits, the Hall of Fame, the
  town-map marker and the standing figure on the title screen.

  Green is the default and has not moved a pixel: its files come out byte for
  byte as they did before there was a table to look them up in. The title
  ribbon stays green in every suit — that is the game's name, not the
  character's jacket. (Wild Green 1.26.0.)

- **`NPC WALK`.** An NPC who walks you somewhere moved its legs twice as fast
  as it covered ground, which beside a walking player reads as a hop rather
  than a walk. A player's tile takes sixteen frames and the walk cycle is
  sixteen frames long, so one step per tile; an NPC's tile takes thirty-two —
  NPCs move at half the player's speed in Gen 1 — and the cycle was still
  sixteen. The cycle is tied to the step now, so one walk cycle fits whatever
  an entity's own tile length is. (Gen1WildQOL 1.25.0.)

### Fixed

- **Every autosave now lands on a frame nobody can see.** The mod used to pick
  its moments by asking *where* the player was, and each of those places was
  reported in turn: the first frame of a door's fade (where the map is still
  fully drawn, so what freezes is the world), the far end of it (where the
  transition has already popped, so the game arrives somewhere and stops
  dead), and a beat after a menu closes (which is the frame you have been
  waiting for, so the hitch lands in your first stride out of it).

  There is one window now: is the screen a solid colour this frame, and will
  it still be one on the next? That is the last eight frames of a warp fade —
  `GBFadeOutToBlack` is a four-step palette staircase and only the fourth step
  is black — the hold at the front of a battle's return, and the black a
  script fade holds. A pause on any of those changes nothing on screen; the
  black is simply longer. A battle's intro wipe has no veil to ask, so going
  *into* a battle cannot become a window by accident.

  A door also no longer leaves a save owing after its own black has taken one,
  which was the mechanism producing the hiccup it was meant to prevent.
  (Gen1AutoSave 1.17.0.)

## [1.40.0] - 2026-08-29

### Fixed

- **POKeMON evolve again.** Nothing on this cart ever did — not the starter at
  level 16, not anything else — and nothing on screen said why.

  BLACK OUTRO fades a battle out by wrapping the one place a battle ends. But
  the engine calls that place more than once: a battle that levelled somebody
  hands the battle screen to the evolutions and *returns*, coming back a
  second time once they have played. The fade took that first call for the
  ending — it ran the engine's finish at its own midpoint, at full black, so
  the evolution started behind the black, and then, finding the battle still
  up because that call had not left, popped what was on top of it and ended
  the battle for real. What it popped was the evolution.

  The hand-off is a false start, the same as the PAY DAY pickup the fade
  already steps aside for. It steps aside for this one now, so the evolution
  plays on the battle screen where the ROM puts it. (Gen1WildUI 1.20.1.)

- **The follower stops walking out of doors into the building, and stops
  standing on people.** The engine tells its follower routine whether a map is
  being entered — a warp, a door, the boot — or respawned mid-map, and the two
  put the follower in different squares: an entry parks it on the player's own
  cell so it comes out of the doorway behind him, a respawn takes the cell
  behind his facing. That argument was being dropped, so every door read as a
  respawn — and stepping outside, the player faces down, which put the
  follower on the cell he had just come through.

  It also no longer arrives on top of an NPC: the spawn rule asks the map
  whether a cell is walkable, which somebody standing on it does not change,
  so an occupied cell now hands the follower back to the player's own.
  (Gen1WildQOL 1.23.1, Gen1Follower 1.5.1.)

## [1.39.0] - 2026-08-29

### Fixed

- **Your settings survive a reboot, and the cart stays sealed.** Every setting
  in the suite was resetting on the next launch, and `PLAYER` could never take
  effect at all — you would set RED, it would say "RED CHANGED.", and the game
  would come back green with the row reading GREEN again.

  That is what a sealed cart does. The loader rebuilds every pinned mod's
  options on each boot out of what the cart pins and discards what you chose;
  and the overworld walker is a record read at load, which is exactly when the
  choice was being thrown away.

  Unsealing would have fixed it and cost you the arena — online play requires
  the seal, and requires it to be exactly `sealed`. So the suite remembers what
  you chose in its own store, which that rebuild does not touch, and puts it
  back as it loads, before anything reads it. It restores into the same place
  the mod manager reads, so every screen agrees, and it never touches the cart
  file, which is what online matches on.

  The cart's pins are now defaults rather than locks: a pinned value is what
  you get until you choose otherwise.

  Gen1WildQOL 1.22.0 -> 1.23.0, Gen1WildUI 1.19.2 -> 1.20.0. No other pin
  moved.

## [1.38.0] - 2026-08-29

### Fixed

- **`MAP` had two switches and only one of them worked.** The layout editor
  listed `MAP` on the `SELECT` menu, said `ON`, and turning it on did nothing —
  what was actually keeping the row off was a separate option two screens away.
  A row that reads `ON` and is not there is worse than a row you did not ask
  for.

  That option is gone. The town map is offered outdoors like every other row on
  that menu, and the editor is the switch: hide it there and it is gone.

- **A row the menu is not offering no longer reads `ON`.** Switching on `FLY`
  in the editor cannot put `FLY` on the menu when what is keeping it off is the
  game and not the layout — no `FLY` in the party, no repel in the bag,
  daylight. Those read `----` now, the same as a pinned row you have not
  unlocked.

- **The editor's empty page ran off its own box**, and its title carried two
  characters the Game Boy font cannot draw. `NOTHING TO ARRANGE` is exactly
  eighteen glyphs and the box's interior is eighteen tiles, so starting it a
  column in put the last two on the border — which is the overlap on the PC
  page. And `<` and `>` are in no Game Boy charmap, so the arrows drew as
  nothing and only pushed the title right; the page count (`1/3`) says the same
  thing in glyphs the font has.

  Gen1WildQOL 1.21.1 -> 1.22.0, Gen1WildUI 1.19.1 -> 1.19.2
  (Gen1MenuManager 0.3.1 -> 0.3.2). No other pin moved.

## [1.37.1] - 2026-08-29

### Fixed

- **The layout editor drew a hint over its own frame.** 1.37.0 put the
  `< >:MENU` hint on the row below the existing one, which is the box's bottom
  border rather than an interior row, so it came out as a smear across the
  frame. There is one line for hints and it was already full. The arrows are on
  the title now: `< START MENU >`.

- **The `SELECT` menu's editor listed only rows it had already seen.** That
  menu's rows appear only where they are usable — `FLY` outdoors, `FLASH` in
  the dark, a repel while one is in the bag — so arranging `FLY` would have
  meant standing outdoors, with `FLY` in the party, holding the editor open.
  A menu whose editor shows one row is not an editor.

  It now lists every row that menu can *ever* show — `FLY`, `TELEPORT`,
  `FLASH`, `DIG`, `MAP`, a repel, `CANCEL` — whether or not it is usable where
  you are standing, so they can be ordered and switched off in advance the way
  a pinned row is.

  Gen1WildQOL 1.21.0 -> 1.21.1, Gen1WildUI 1.19.0 -> 1.19.1
  (Gen1MenuManager 0.3.0 -> 0.3.1). No other pin moved.

## [1.37.0] - 2026-08-29

### Added

- **`A` on the AREA map flies you there.** The AREA screen *is* the town map.
  If your party can `FLY` and the cursor is over somewhere flyable, closing it
  to open the START menu and pick `FLY` to reach the same picture again is the
  screen being pedantic about which door you came in by. With the hint down,
  `A` over a flyable town is the flight.

  Which towns qualify is the game's own rule — visited, has a fly warp, is a
  fly town — so a town this says yes to is one the `FLY` screen would have
  offered you. No `FLY` in the party, indoors, the cursor on somewhere
  unflyable: any of them and `A` closes the screen the way it always did. New
  row: `FLY FROM AREA`.

- **`MAP ON SELECT`** puts the town map on the `SELECT` field menu, outdoors.
  Off by default — that menu earns its place by being short and by being only
  what is usable where you are standing.

- **The `SELECT` field menu is arrangeable.** `MENU LAYOUT` could arrange the
  START menu and the PC menu; the field menu — `FLY`, `TELEPORT`, `FLASH`,
  `DIG`, a repel, and now `MAP` — was the one menu in front of you it could not
  touch, because that menu is not the game's and has no hook to wrap. It is
  built fresh on every press out of what is usable on this tile, with this
  party, in this bag, so the mod that builds it now hands the rows round and
  the manager takes its turn.

  There are three menus now and one row on the OPTION screen, so **LEFT and
  RIGHT walk between them in the editor**. `CANCEL` is locked on the field
  menu: `B` closes it too, but a way out you can *see* is not the same as one
  you have to know about. New row: `SELECT ROW`, off by default.

  Gen1WildQOL 1.19.0 -> 1.21.0, Gen1WildUI 1.18.0 -> 1.19.0 (Gen1Dex 1.8.0 ->
  1.9.0, Gen1MenuManager 0.2.8 -> 0.3.0). No other pin moved.

## [1.36.0] - 2026-08-29

### Changed

- **FLY is a map, not a list drawn on a map.** The FLY screen already shows the
  whole of Kanto with a bird on the town you have selected — and then walked
  that selection with `UP` and `DOWN` through the fly order. The picture said
  "pick a place"; the controls said "scroll".

  It is steered by direction now, like the other two town maps. Open the map,
  move to the town you want, press `A` to go there.

  Which towns you can reach does not change: that set is the game's own,
  already narrowed to the towns you have visited, so everywhere the cursor can
  reach is somewhere `A` can take you. `B` still closes it, and the name strip
  is still the game's.

  Gen1WildUI 1.17.0 -> 1.18.0 (Gen1Dex 1.7.0 -> 1.8.0). No other pin moved.

## [1.35.0] - 2026-08-29

### Fixed

- **The town map moves by direction instead of cycling a list.** `UP` and
  `DOWN` fell back to the game's own list walk whenever there was nothing in
  the direction you pressed — and a press off any edge of Kanto, of which there
  are four edges' worth, jumped the cursor to wherever the *cursor order* went
  next. That order is the order the towns come up in the story, not where they
  are, so the cursor leapt across the map for reasons nothing on screen could
  explain. A key with nothing in front of it now leaves the cursor where it is.

### Changed

- **The map you open from the bag is steered the same way.** Same screen, same
  picture, and until now a different d-pad: the original walks its cursor along
  the visit order with `UP` and `DOWN` and ignores `LEFT` and `RIGHT` entirely.
  One map should navigate one way however it was opened.

  Only the d-pad. `B` still closes both, the name strip is still the game's own,
  and `FLY` is left alone — its cursor cycles the towns you have visited in fly
  order and `A` flies to the one it is on, so direction is not what that d-pad
  means there.

  Gen1WildUI 1.16.1 -> 1.17.0 (Gen1Dex 1.6.2 -> 1.7.0). No other pin moved.

## [1.34.0] - 2026-08-29

### Changed

- **`AUTO SAVE` no longer writes while a menu is up.** The widest window it had
  was anything over the overworld: a text box while somebody talks, the START
  menu, the bag, the party, a PC, a mart, a Centre's heal. The reasoning was
  that you cannot move under one and the map behind is a still picture, so a
  dropped frame there is a frame nobody sees.

  Nobody sees it. You feel it. A menu is not a pause in the playing — it is the
  part with the most presses per second in it, and a frame lost there is an
  *input* lost there. A stutter mid-stride is ugly; a swallowed `A` press is
  the game not listening.

  The doors are the three they always were: a warp, the end of a battle, and
  actually stopping. The moment a menu *closes* is still one of them — by then
  it is gone and you are standing on the route with nothing pressed. Closing is
  the moment, not opening. Writes that go under a screen you cannot press
  through, like a door's black screen, are unaffected.

  Gen1WildQOL 1.18.0 -> 1.19.0 (Gen1AutoSave 1.14.0 -> 1.15.0). No other pin
  moved.

## [1.33.1] - 2026-08-29

### Fixed

- **The AREA screen ends on the map.** 1.33.0 took the `AREA UNKNOWN` slab down
  while the hint strip was up and put it back the moment `A` dismissed the
  strip — so pressing `A` for a clear look at the map got you a slab across the
  middle of it instead. That was backwards. The route is the dex, then
  `<NAME> UNKNOWN`, then the map, and the map is where it ends. The slab is
  gone from every frame of that screen now.

- **Your marker is on that map.** It lives in the same branch the slab was the
  other half of: with no nests to mark, the original puts the slab up *instead*
  of marking where you are standing. That trade made sense while the slab
  covered the map. With it gone the screen is a plain town map, and a plain
  town map has you on it.

  Gen1WildUI 1.16.0 -> 1.16.1 (Gen1Dex 1.6.0 -> 1.6.2). No other pin moved.

## [1.33.0] - 2026-08-29

### Fixed

- **Your character on the town map wears green, and has his face back.** The
  little figure marking where you are standing — on the AREA map and on FLY —
  was still Red in his red cap, on a cart where the player is green in every
  other frame of the game. His skin and hands were see-through too, with the
  map showing through them.

  The town map does not draw the player. It builds a marker of its own out of
  the sprite record and bakes it through the object-palette path, which asks
  none of the things that make the walker green — and that bake keys the
  lightest colour to fully transparent, the way real hardware treats sprite
  palette index 0. Wild Green's skin sits just over that line, so it was keyed
  away with the background.

  The marker is now the green picture itself, loaded and handed straight to the
  map. No bake, so nothing to key away.

### Changed

- **The `AREA UNKNOWN` slab is gone from the AREA screen.** With no nests to
  mark, the original puts a box across the middle of the map to say so. On this
  cart that was the third thing saying it at once: the line above the map
  already reads `<NAME> UNKNOWN`, and the strip below carries the half worth
  reading — `EVOLVE CHARMELEON AT LV36`, or whichever answer the species has.
  A screen that *has* an answer was covering half its own map to say it has
  none.

  Press `A` to put the strip away for a clear look at the map and the box comes
  back, because then it is the only thing left explaining an empty map. `START`
  brings both back together.

  Gen1WildUI 1.15.1 -> 1.16.0 (Gen1Dex 1.5.3 -> 1.6.0), Wild Green 1.24.0 ->
  1.25.0. No other pin moved.

## [1.32.1] - 2026-08-29

### Fixed

- **The Pokédex side menu has a box again.** Pressing A on a POKéMON you had
  met came up as four bare words -- `DATA`, `CRY`, `AREA` -- floating over the
  list, with `QUIT` printed across the SEEN and OWN counts and past the bottom
  of the screen. Pressing A on one you had *not* met opened a properly framed
  two-row menu, which is what made it look like the discovered entries were the
  broken ones.

  Both were the same omission. The original dex prints those four labels
  permanently into the block down the right of its screen, so the menu itself
  draws only the labels and the cursor -- there is already a block under them.
  The redrawn list has no such block: the right of the screen is where the
  names run, and SEEN / OWN moved into a footer box.

  The menu is now put in a box of the mod's own, sized to fit above the footer,
  and the row it was opened on reads as hollow underneath it the way the
  original list draws it. What the rows do is unchanged -- they are the game's
  own, not copies.

  Gen1WildUI 1.15.0 -> 1.15.1 (Gen1Dex 1.5.2 -> 1.5.3). No other pin moved.

## [1.32.0] - 2026-08-29

### Fixed

- **The black screen plays out when you walk through a door.** For real this
  time, and the last two attempts were fixing the wrong end of it.

  The autosave was writing on `map.entered` -- the moment the new map is in
  place, which is the *end* of the warp's animation, not the start of it. The
  fade to black has already played by then, and the fade back is zero steps
  long: the map simply appears. So the write had the whole cost of a save in
  front of it and no animation left to hide under. Clamping the frame
  afterwards, twice, could not help, because there was nothing after it.

  It now writes on the first frame of the fade it can, with all thirty-two
  steps of the palette walking down to black still to come. The black screen is
  longer by exactly what the save cost, and the animation plays. Entering a map
  is still the fallback for a door whose fade was never writable.

  A second one alongside it: the gate an ordinary due save goes through asked
  whether something was over the overworld before it asked whether that
  something was a transition -- and a transition is something over the
  overworld -- so a save that was merely due could land mid-fade as well.

  Gen1WildQOL 1.17.1 -> 1.18.0 (Gen1AutoSave 1.13.1 -> 1.14.0). No other pin
  moved.

## [1.31.1] - 2026-08-29

### Fixed

- **The black screen plays out when you walk through a door.** 1.30.1 fixed
  half of this and shipped with the other half still in: the autosave was
  treating the warp fade as the quietest frame it could possibly take, which is
  backwards. A fade is an animation -- thirty-two steps of the palette walking
  down to black -- and stopping for a fifth of a second in the middle of one is
  a stall you can watch happen. It now stands off transitions outright, and the
  clamp that stops the frame after a save being paid back as a burst is armed
  properly rather than by a check that never once fired.

  Gen1WildQOL 1.17.0 -> 1.17.1 (Gen1AutoSave 1.13.0 -> 1.13.1). No other pin
  moved.

## [1.31.0] - 2026-08-29

### Changed

- **`OPTIONS > MODS` is now `OPTIONS > WILD GREEN`.** The suite's row used to
  sit next to the game's own `MODS` row. It takes that row's place instead.

  Two rows on one screen that both mean "the mods" is a choice with no right
  answer. `MODS` opens the list of installed mod zips, which is almost never
  what somebody on the OPTION screen is after: with this cart running, nearly
  everything behind that row is this suite's, and what they came for is a
  setting. So the suite's row takes the slot, and it is named after the cart --
  `WILD GREEN`.

  `START > MODS` goes to the same place, so the route you already know still
  works and no longer lands somewhere different from the one on `OPTIONS`.

  The mod list is not gone, it is one press further in: `MOD MANAGER` is the
  last row of the Wild Green menu, and says how many mods are installed.

- **The folder cards are named for what is on them.** `OUT IN THE WORLD`,
  `YOUR POKEMON`, `BATTLES`, `SAVING & SOUND` and `MOD SETUP` are now
  `GENERAL`, `POKEMON`, `BATTLE`, `ITEMS`, `SAVE` and `INTERFACE`. A card is a
  signpost; one written to sound like something is one you have to read twice.
  `AUTO CONTINUE` moves to `SAVE`, where picking up where you left off belongs.

  Nothing that a setting depends on moved. Every switch keeps the value it had.

  Gen1WildQOL 1.16.1 -> 1.17.0, Gen1WildUI 1.14.1 -> 1.15.0. No other pin
  moved.

## [1.30.1] - 2026-08-29

### Fixed

- **Walking through a door no longer skips the fade.** The autosave landing
  under the black screen was cutting it short, so you popped into the new map
  instead of fading in.

  It was not the save being slow. The game advances its logic in whole 1/60
  steps out of an accumulator, so a frame that took an extra 60 ms hands the
  next update a 60 ms `dt`, and the accumulator pays that back as four logic
  steps in a row before anything is drawn again. Four steps of a fade in one
  frame is a cut, not a fade.

  The engine has a remedy for its own hitches and it turns out warps do not use
  it — its own source says so. The autosave now applies it after anything of
  its own that costs a frame, so the loading screen is a little longer and the
  animation plays out properly.

  Gen1WildQOL 1.16.0 -> 1.16.1 (Gen1AutoSave 1.12.0 -> 1.13.0). No other pin
  moved.

## [1.30.0] - 2026-08-29

### Changed

- **Your save now reaches your account as soon as it reaches the disk.**

  The autosave used to pace its uploads: one every five minutes, with every
  other save's upload *thrown away* and the file left for the engine's own
  sweep to collect whenever it next came round. That was written back when a
  sync meant a visible stall — and it bought cheapness at the price of the save
  being current. The newest file could sit on this device for minutes while
  another device was still being handed the old one.

  The stall it was avoiding turned out not to be the sync at all (it was the
  collector burst, fixed in cart 1.28.0), so there is nothing left to avoid.
  The upload now goes with **every** save, and it goes **immediately** rather
  than waiting out the engine's five-second debounce — which only ever moved
  the request off the black screen it could have left from and into the middle
  of the next corridor.

  **The loading screen is slightly longer for it.** That is the trade, and it
  is the right way round: the save you just made is on the server before you
  are walking again.

  Gen1WildQOL 1.15.0 -> 1.16.0 (Gen1AutoSave 1.11.0 -> 1.12.0). No other pin
  moved.

## [1.29.0] - 2026-08-29

### Changed

- **Running between routes no longer autosaves.** Every map change was being
  treated as a door — worth saving for, and a free frame to save in. A route
  seam is neither. The routes are stitched together, so crossing one is
  seamless: the map just scrolls on, and you are mid-stride the whole way
  across. The save was landing in the exact frame the whole design exists to
  avoid, for a crossing that is not progress worth stopping for.

  The engine already labels this and the mod was not asking. Only a real
  warp — a door, stairs, a cave mouth — and FLY have a screen in front of
  them. Those still save. A route seam now neither writes a save nor asks for
  one, and a save that was already waiting simply goes at the next real
  window: the next door, battle, conversation, menu, or a proper stop.

  Gen1WildQOL 1.14.1 -> 1.15.0 (Gen1AutoSave 1.10.0 -> 1.11.0). No other pin
  moved.

## [1.28.0] - 2026-08-29

### Fixed

- **The stutter every time the game autosaves is gone, and it was ours.**

  Not the save itself — the collector burst the autosave fired straight after
  one. It handed the garbage collector up to **48 MB** of work to do, which on
  a heap this game's size is a complete collection cycle, in a single frame,
  after every single save.

  Measured on a 45 MB heap over 30 saves: the frame a save lands in took
  **53 ms** with that burst and **10.5 ms** with the small nudge that replaces
  it — and the twenty seconds *afterwards* are within a few milliseconds either
  way. It was spending forty milliseconds a save to move at most six off some
  later frame, and on a phone every one of those numbers is three to five times
  larger.

  The reasoning behind it was simply wrong: the engine already advances the
  collector a little on every rendered frame, for exactly this purpose, so it
  was never falling behind in the first place.

  Everything else about when a save happens is unchanged — it still waits for a
  door, a battle, a conversation or a real stop.

  Gen1WildQOL 1.14.0 -> 1.14.1 (Gen1AutoSave 1.9.0 -> 1.10.0). No other pin
  moved.

## [1.27.1] - 2026-08-29

### Fixed

- **The player no longer glows in a dark cave.** In Rock Tunnel and every
  other unlit floor he walked around in full daylight colours beside a
  screenful of silhouettes.

  His green art is marked true-colour, which is what stops a lit map's palette
  reading the green through the shade buckets it reads grey art through. The
  catch is that the palette pass that flag opts out of is *also* what blacks a
  cave out — so the one sprite that opted out of being recoloured had opted out
  of being blacked out with it.

  He gives the exemption up in an unlit frame now, and the engine's own path
  darkens him exactly the way it darkens everyone else. Same silhouette, same
  shade, as a player not wearing green.

  Gen1MakeItGreen 1.23.0 -> 1.24.0. No other pin moved.

## [1.27.0] - 2026-08-29

### Changed

- **The autosave now hides itself in the moments you could not move in
  anyway,** and it no longer mistakes a pause for a stop.

  Standing still was one frame of not walking — so letting go of the pad to
  change direction, or lining up on a doorway, counted as standing still, and
  the save landed in the middle of a walk. A stop is three unbroken seconds
  now, or the moment a menu closed or a conversation ended and you have not
  started moving again.

  And there are far more windows than there were. A warp and the end of a
  battle were the only two; now **any moment the game is holding you still** is
  one: a battle starting, a text box while somebody talks, the START menu, the
  bag, the party, a PC, a mart, a Centre's heal. None of those is a named
  special case — anything over the overworld is something you cannot move
  through, so the rule covers the ones nobody thought of too.

  Two are deliberately not windows. Nothing is written **inside** a battle —
  Gen 1 has no save there, and the file would record the overworld the fight
  started from while you are somewhere else — and nothing is written part-way
  through a script, because a cutscene that has set half its flags is not a
  state worth writing down. The moment a script *ends* is a window.

  Finally, the save and the sync take **different** windows rather than sharing
  one. The write is cheap and takes the first opportunity; the sync cycle it
  wakes is expensive and does not arrive for a few seconds, so it takes
  whatever window comes next. You walk out of a door, it saves there, and the
  sync lands at the next door, the next battle, or the next conversation.

  Gen1WildQOL 1.13.2 -> 1.14.0 (Gen1AutoSave 1.8.0 -> 1.9.0). No other pin
  moved.

## [1.26.3] - 2026-08-29

### Fixed

- **The white box behind a POKéMON in battle is gone.** It was two bugs at once,
  and the reason it survived a fix is that neither of them happens on a
  desktop.

  The backdrop mod repairs sprites the cart's own extractor hollowed out, by
  laying the field shade back under them. To decide which sprites need that it
  reads their pixels back off a scratch canvas — and that canvas takes the
  screen's DPI scale unless it is told not to. On a phone that is 3, so it read
  the sprite's top-left *eighteen* pixels blown up three times and answered on
  a corner: few enough colours to look like flat art, empty enough to look
  damaged. The white patch then went down in a box measured off that corner,
  which on the enemy side is a 14x24 block against the right edge of the
  sprite — exactly what the photo showed.

  And the test for "this sprite lost something" was how much of its box is
  empty, which reads an awkward shape as a damaged one. A Crystal Koffing is
  solid on all nine of its animation frames, but the three that put its gas
  plume out score 0.51 against 0.26 for the other six — so the patch blinked on
  and off behind a perfectly healthy sprite once per animation cycle. It now
  measures a hole *through* the mon, which is the thing it exists to fill.

  Gen1WildUI 1.14.0 -> 1.14.1 (Gen1Arena 0.20.2 -> 0.21.0). No other pin moved.

## [1.26.2] - 2026-08-29

### Fixed

- **The stutter a few seconds after a save is gone too.** 1.26.1 stopped the
  save itself landing while you run, and that held. The write is the cheap
  half: the expensive one is the sync cycle it wakes, which arrives a few
  seconds later on network time and decodes every save slot of every game
  version through a character-at-a-time parser. That is the hitch that was
  still showing up "a little after a save".

  `QUIET SYNC` has been holding that out of walking frames all along, and it
  was leaking through the same two holes the write had: it read a flag that
  drops for the single frame between two strides, and it gave up after three
  seconds without ever checking that you had stopped.

  A held direction counts as walking now, and there is no cap — the reply is
  already in hand, the engine's clock stops with the hold, and letting go of
  the pad releases it on the next frame. Any menu, text box, battle or doorway
  releases it immediately as well. The collector work a finished cycle leaves
  behind waits for the same kind of frame.

  Gen1WildQOL 1.13.1 -> 1.13.2 (Gen1AutoSave 1.7.0 -> 1.8.0). No other pin
  moved.

## [1.26.1] - 2026-08-29

### Fixed

- **The autosave hitch while running is gone for real.** 1.26.0 moved the save
  onto the black screens a warp and the end of a battle already put up, and
  that part worked -- but two things in it still let a write land on a moving
  screen, which is the whole thing it was meant to stop.

  A 45-second cap gave up on waiting and wrote on the route without ever
  checking that you had stopped walking. And the check that was supposed to
  keep a write off a moving player read a flag that drops for the single frame
  between two strides, so walking a long route without stopping satisfied it
  several times a second -- which is exactly where a dropped frame shows.

  Standing still is what counts now, and a held direction is not standing
  still. The cap is gone with it: a save that is due waits for a warp, the end
  of a battle, or for you to stop, and there is no fourth way out.

  Gen1WildQOL 1.13.0 -> 1.13.1 (Gen1AutoSave 1.6.0 -> 1.7.0). No other pin
  moved.

## [1.26.0] - 2026-08-29

### Changed

- **Every setting in the cart is one row on the game's own OPTION screen now.**
  It is called `WILD GREEN` -- the cart's own title, read from the cart -- and
  it sits next to `MODS`.

  Before this the settings were at `MODS > GEN1WILD QOL > OPTIONS` and
  `MODS > GEN1WILD UI > OPTIONS`: two lists, three screens deep each, behind
  names that are repositories rather than things, and with a guess about which
  of the two owned the row you wanted. Now there is one door and one list.

  Behind it are folder cards, the same way the game's own OPTION screen nests
  `SPEED`, `VIDEO` and `AUDIO`. `OUT IN THE WORLD`, `YOUR POKEMON`, `BATTLES`,
  `ITEMS AND BAG`, `SAVING AND SOUND`, `MOD SETUP`, and one more:
  **`OTHER MODS`, which holds the rest of what this cart pins** -- Make It
  Green and the animated sprites -- so every pinned mod's settings are on the
  same screen as everything else rather than three screens away in the
  manager.

  Nothing was removed. Every switch that existed still exists, in the same
  place in the tree, with the same stored value.

- **Gen1WildQOL 1.12.0 -> 1.13.0** and **Gen1WildUI 1.13.0 -> 1.14.0.** Those
  two carry the menu above, and between them four fixes that came forward from
  their own mods:

  - `AUTO SAVE` writes during a loading screen -- a warp's fade, a battle's
    return hold -- instead of stuttering in the middle of walking. Loading
    screens are a few frames longer; the hitch on the route is gone.
  - Followers are drawn at the size their art was drawn at. Small species were
    being resampled from 16px down to 11px and coming out as flat two-colour
    blobs.
  - Professor Oak stops hopping on the walk to his lab. Sprint made your step
    length depend on what you were holding, and his was pinned to yours at the
    start of the walk.
  - Pale battle sprites stop turning into a white box over a backdrop.

  No other pin moved.

## [1.25.0] - 2026-08-29

### Changed

- **The seal is `sealed` rather than `sealed+`, so the cart can be taken
  online.** The engine's online mode only ever offers a cart whose seal is
  exactly `sealed`: the launcher's ONLINE tab filters its game list on it
  (`OnlinePanel.sealedCarts`), the arena refuses to build a profile without it
  (`ArenaData.profile`), and the arena loader refuses to boot without it
  (`Loader:_arenaCart`). Under `sealed+` Wild Green did not fail with a
  message, it simply never appeared in the tab.

  What it costs: the four pinned mods can no longer be switched off one by
  one. That is the whole of the difference between the two seals — `sealed+`
  is the same fixed set with every pin handed to the player, `sealed` runs it
  exactly as pinned. Breaking the seal on a save slot is still there for
  playing the cart with your own mods on top, and a save with a broken seal
  cannot go online either way. Every feature switch *inside* the four is
  unaffected, and so is everything else about how the cart plays.

  This is only a seal change. No pin moved.

### Notes

- The version bump is not ceremony. The cart's manifest hash covers `seal`,
  and online play matches players on that hash, so a `sealed` cart still
  calling itself `1.24.0` would be a second, different `1.24.0` in the wild.
- `engine` is left at `>=0.1.37 <2.0.0`. The seal costs an older build
  nothing, and raising the floor to whichever release added the ONLINE tab
  would lock out players who have no use for it.

## [1.24.0] - 2026-08-29

### Fixed

Four bugs you could see, and a tidier option screen. Re-pinned to
`Gen1WildQOL` `1.12.0` and `Gen1WildUI` `1.13.0`.

- **The starter you could not pick.** Oak shows the Pokédex entry for a starter
  before he asks whether you want it, and the script waits for that screen to
  close itself. The entry's `A` key cycled its three pages forever, so pressing
  `A` at the CHARMANDER you had just been offered gave you a third page and
  then the first one back, and nothing ever asked you anything. `A` now walks
  the entry once and leaves it, which is what hands the question back. The
  Safari Zone signs and the S.S. Anne's Snorlax had the same fault.

- **Some POKéMON went invisible in battle.** Gen 1 battle pictures have their
  white flooded away from the edges, and the flood stops only at ink — so
  wherever a POKéMON's own white touches the edge, it pours into the body and
  hollows it out. Against the game's white field you cannot tell; against an
  arena backdrop the hole is a window. Mew's back picture keeps 145 of the 400
  pixels it should have. The new `MON PAPER` row puts the field shade back
  under any picture that actually lost some, and leaves the Crystal sprite
  replacements alone because their transparency is real.

- **The AREA map crashed the game.** Moving the cursor on the Pokédex's `AREA`
  screen called something the engine has never had, so the first d-pad press
  there ended the session. That feature had not worked since it shipped.

- **The save-sync hitch.** A sync cycle's expensive moment is decided by when
  the server answers, so it landed at random — which is why it read as the game
  hiccupping rather than as the game saving. The new `QUIET SYNC` row keeps it
  out of the frames you are mid-step in, where a dropped frame is the one thing
  you would notice.

### Changed

- **The QOL option screen is grouped.** The rows were in the order the mods
  were added, so `SPRINT` was first and `EASY HM USE` was thirteenth, and
  `EXP SHARE` sat below the mod manager. They now run getting around, your
  POKéMON, battles, catching everything, saving, sound, and the furniture last
  — which is where `Gen1WildUI` already put it, so the two halves read the same
  way round. Nothing installs in a different order.

- **The maintenance rows are gone from the options.** `TEST BENCH`,
  `DIAGNOSTIC` and `FIELD TEST` are tools rather than settings, and one of them
  paints every battle flat magenta without the row saying so. They are offered
  in developer mode only, and no longer read outside it, so a value left set by
  an older install cannot strand anyone.

- **The BAG's settings are in the game's voice.** `Opening Pocket`,
  `Hold Scroll Speed` and `Item Icons` were the only rows in the whole cart
  written in Title Case. No stored setting moves.

## [1.23.0] - 2026-08-28

### Fixed

- Wild Green re-pinned to `1.23.0`: the painted pictures — the title figure
  and the battle back pic — are lists of coordinates, and only ever found
  their art sitting exactly where it sat. A cache holding the **same** sprite
  one pixel over, from an importer that pads differently or a rip on a larger
  sheet, failed every check at once and lost its skin with identical pixels
  underneath. They are matched where they were drawn first, and slid over the
  picture only if that fails.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.23.0.zip` is `3eadecd1…b8c55a`, from the release's own
  `sha256sums.txt`, checked against the archive.

## [1.22.0] - 2026-08-28

### Fixed

- Wild Green re-pinned to `1.22.0`: **the player's battle back pic had no
  skin on it at all** — in a battle he was one green shape from the cap to
  the boots. No rule ever reached that picture: the portrait skin pass is
  built around finding a face and gives up the moment it cannot, and there is
  no face on the back of his head, so it fell through to the flat ramp. His
  neck, jaw, hand and forearm are skin now. `PORTRAIT SKIN` is also a real
  switch on that picture for the first time — with nothing painted, the two
  copies the recipe writes were the same picture.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.22.0.zip` is `68b15f31…5cf742`, from the release's own
  `sha256sums.txt`, checked against the archive.

## [1.21.0] - 2026-08-28

### Fixed

- Wild Green re-pinned to `1.21.0`: the `NEW NAME` page offered six names
  rather than three — vanilla's `RED / ASH / JACK` and `BLUE / GARY / JOHN`
  with the mod's own three appended behind them. The field registry appends
  lists rather than replacing them; the mod unsets the key before writing it
  now. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.21.0.zip` is `d6376b2e…8ab17e`, from the release's own
  `sha256sums.txt`.

## [1.20.0] - 2026-08-28

### Changed

- **A new cartridge label.** `art/wild_green_label.png` is finished artwork
  carrying the Gen1Wild wordmark with `WILD GREEN VERSION` under it, so
  `make_label.py` no longer composites the wordmark with `ribbon.py`'s 5×7
  face — it scales the piece to 256×256 and nothing else. No keyline: the old
  sticker was a green field on a green shell and needed one, and this is
  bright against `#14571f`. The Gen1Wild index serves this same file as the
  cart's card, so the card follows on its next hourly rebuild.
- `tools/ribbon.py` and `art/gen1wild_wordmark.png` are gone. Nothing drew
  from them once the label stopped being assembled here; the lettering lives
  in [the mod's repo][mod], which is where the title ribbon is drawn.
- The README is rewritten to the shape the rest of the suite uses, and no
  longer prints the pinned versions in prose — `cart.json` is the only place
  they are written down.
- Wild Green re-pinned to `1.20.0`: the hair no longer flickers black as he
  walks towards the camera. See [its changelog][mod-log].

### Fixed

- **`tools/palette.py` had drifted from the mod's copy and nothing noticed.**
  The twin check only ran while the mod shared this tree, so it went quiet
  when the mod moved out and stayed quiet for eighteen versions; `SKIN` here
  still read `#f8d8a8`, from before the skin tones were worked out, and none
  of the colours added since were here at all. The file is synced, and
  `check.py --online` now fetches the mod's copy and compares — CI passes
  `--online`, so this cannot go quiet again.

### Notes

- `wild_green-1.20.0.zip` is `770f3e5f…2daf25`, from the release's own
  `sha256sums.txt`.
- `v1.19.0` was cut by the workflow itself, from a `cart.json` bump, with no
  tag pushed by hand.

[mod]: https://github.com/wild1walker/Gen1MakeItGreen
[mod-log]: https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md

## [1.19.0] - 2026-08-28

### Changed

- Wild Green re-pinned to `1.19.0`: both lists on the naming screen's
  `NEW NAME` page read as a sentence down the cursor —
  **WILD / GREEN / VERSION** for the player, **Thanks / For / Playing!**
  for the rival. The default name a save takes when the naming step never
  runs is still `GREEN`.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.19.0.zip` is `b36f0ff3…41858d`, from the release's own
  `sha256sums.txt`.
- First cart cut by the automation added in 1.18.0: `v1.18.0` was tagged and
  published by the workflow itself, from a `cart.json` version bump.

## [1.18.0] - 2026-08-28

### Fixed

- Wild Green re-pinned to `1.18.0`: the player's mouth is red when he faces
  left or right, not green. Facing forward the mouth has skin on both sides
  and was already caught; in profile one side is the silhouette's outline, so
  the old rule read it as outfit. It now accepts a mouth with skin on a single
  side, provided there is cheek directly above it and the pixel is not part of
  the cap's brim.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

- The `gen1_wild_ui` pin said `1.13.0`, a version that was never released,
  with a digest that belonged to `wild_green-1.13.0.zip`. The bump script
  that cut cart 1.13.0 matched the first `"version": "1.12.0"` under `mods`
  and rewrote the wrong entry. It is back to `1.12.0` /
  `c4015d0b…a4a536`, which is what Gen1WildUI's newest release actually
  publishes. No released cart carried the bad pin: nothing past `v1.1.0` had
  been tagged.

### Changed

- The cart releases itself. `cart-release.yml` used to wait for a `v*` tag
  pushed by hand; it now runs on every push to `main`, and cuts
  `v<cart.json version>` when that tag does not exist yet. The tag is made by
  `gh release create --target <sha>` rather than a git push, which is how the
  mod's own workflow has always worked. Bumping `"version"` in `cart.json` is
  the whole release ceremony now.
- Nothing is tagged before `cartkit validate . --online --strict` passes, so
  a cart.json pointing at an unpublished mod fails the run instead of leaving
  a tag behind. That check is also what would have caught the `gen1_wild_ui`
  pin above, had anything ever been in a position to run it.

### Notes

- `wild_green-1.18.0.zip` is `84891262…fd6e32`, from the release's own
  `sha256sums.txt`.

## [1.17.0] - superseded by 1.18.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.17.0`: the title screen's figure no longer turns
  purple during the ball phase of the title animation. It was never a stale
  or wrong picture — the rectangle simply was not marked true-colour on those
  frames, so the SGB zone pass repainted it with `MEWMON`.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.17.0.zip` is `776979b2…1bc2ebc`, from the release's own
  `sha256sums.txt`.

## [1.16.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.16.0`: the first launch after an install shows
  the drawn title figure rather than the faceless flat bake. The recipe's
  copy is a file written at install time and that screen is drawn very
  early, so the copy can arrive just after it; the draw kept asking for it
  now instead of taking the first miss as final.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.16.0.zip` is `e75a2104…604af79`, from the release's own
  `sha256sums.txt`.
- Installing a new version over a running game still needs a relaunch to
  load it — mods are loaded once, at boot. That is the engine's behaviour,
  not the cart's.

## [1.15.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.15.0`: the title screen's figure no longer
  flashes back to Crystal's red bake. Holding it from `TitleState.
  currentSprite` alone was not enough — the draw reads the figure into a
  local before it calls `currentSprite`, and skips `currentSprite` entirely
  for one phase of the title animation.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.15.0.zip` is `0caae99d…71e606e`, from the release's own
  `sha256sums.txt`.

## [1.14.0] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.14.0`: the title screen's figure is painted
  from a table authored against the figure itself rather than from the rules
  the other pictures use — fourteen of its skin pixels come from the paper
  shade, which no rule here touches — and the Poké Ball he throws keeps
  vanilla's red instead of going green with his jacket.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.14.0.zip` is `416b0a53…43b9f08`, from the release's own
  `sha256sums.txt`.

## [1.13.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.13.0`: on the big pictures a hand is skin
  again, and only the crease inside the right one is the shadow. `1.12.0`
  shadowed both hands throughout, which reads as a hand in shadow rather
  than as a hand.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.13.0.zip` is `b5d9655c…794d5ac`, from the release's own
  `sha256sums.txt`.

## [1.12.0] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.12.0`: the title screen's standing figure — the
  one holding the ball out — gets the same face, ear and hands as the trainer
  card under `ADVANCED`. He was the last picture of the player still flat
  green, because `main.lua` baked him from the shade buckets at draw time and
  a bake knows nothing about where a face is. He is a cache file like any
  other, so the recipe recolours him now and the draw is handed that copy.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.12.0.zip` is `ad2a44e4…b17f9dd`, from the release's own
  `sha256sums.txt`.
- The mod's `1.11.1` is this same change released without its changelog or
  manifest bump; `1.12.0` is the one pinned here.

## [1.11.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.11.0`: the player's hands take the skin's
  shadow rather than flat skin. They were the only skin on the big pictures
  coloured by the zone that found them instead of by their own shade — and
  they are drawn entirely in the mid shade, which everywhere else on him is
  the shadow. Which skin a pixel gets is now its own shade and nothing else.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.11.0.zip` is `7c0e946e…208964b`, from the release's own
  `sha256sums.txt`.

## [1.10.0] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.10.0`, which finishes the player's skin on the
  big pictures — the temple under the hat brim and the highlight inside his
  hand, the last two things still green — and changes the naming screen's
  own list to **GREEN / WILD / JACK** where vanilla offers RED / ASH / JACK.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.10.0.zip` is `fe7d9c4c…cc3088a`, from the release's own
  `sha256sums.txt`.

## [1.9.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.9.0`: the player's hands and ear are skin on
  the big pictures, and his sleeves are not. Skin on that art is drawn in
  two shades — the hands in the mid shade alone, the same one as the
  trousers and the cap — and every rule before this looked only at the
  light shade, so the hands and the ear were unreachable and what those
  rules found on the arms was the jacket's own shading.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.9.0.zip` is `5349ebe2…c38f497`, from the release's own `sha256sums.txt`.

## [1.8.0] - superseded by 1.17.0, never tagged on its own

### Fixed

- Wild Green re-pinned to `1.8.0`: `PORTRAIT SKIN` had painted a jacket
  highlight and only half of each hand. Separating skin from clothing by
  size and by how much white is against a patch cannot work — on the real
  card a hand and the jacket's shoulder are one pixel apart on size, white,
  outfit and ink alike. It goes by where things sit now: the face is the
  biggest patch high in the figure with paper against it, the hands are the
  patches beside the lower half of the torso, and small pieces of the shade
  below the skin's — the ear, the brow — take the skin's own shadow instead
  of staying green.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

### Notes

- `wild_green-1.8.0.zip` is `c7da33b4…6a701fa`, from the release's own `sha256sums.txt`.

## [1.7.0] - superseded by 1.17.0, never tagged on its own

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

## [1.5.0] - superseded by 1.17.0, never tagged on its own

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

## [1.4.0] - superseded by 1.17.0, never tagged on its own

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

## [1.3.0] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.3.0`: the trainer art takes its own ramp —
  white, light green, green, black — instead of the overworld sprite's, so
  the battle back pic, the trainer card, Oak's intro and the Hall of Fame
  come out clean rather than blotched with orange and red. Four more of the
  player's pictures are covered, and the recipe and the hook now share one
  list so a swap can never point at a picture the recipe did not write.
  See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.2.0] - superseded by 1.17.0, never tagged on its own

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

## [1.1.4] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.4`: the lips are vanilla's red again rather
  than painted out, and the cap's bill goes with the hat in profile as well
  as facing down. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.3] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.3`: the cap's bill goes with the hat instead
  of taking the face's colour. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.2] - superseded by 1.17.0, never tagged on its own

### Changed

- Wild Green re-pinned to `1.1.2`: the player's mouth is skin rather than
  green, and the title screen's standing figure is green again — coloured
  through the `MEWMON` zone palette rather than by swapping the pic, which
  takes the `GAME FREAK` line green with it and is on a `TITLE FIGURE` row of
  its own. See [its changelog](https://github.com/wild1walker/Gen1MakeItGreen/blob/main/CHANGELOG.md).

## [1.1.1] - superseded by 1.17.0, never tagged on its own

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

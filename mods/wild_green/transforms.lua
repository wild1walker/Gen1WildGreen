-- Wild Green -- the recipe that turns the player green.
--
-- The player's four pictures are the vanilla ones, so this mod may not ship
-- them: derived art travels as a recipe and the pixels come from the
-- player's own imported cache (Guide: Art Pipeline, "The rule").  This file
-- is that recipe.  It runs once on install, and again only when the cache is
-- re-imported or this file changes.
--
-- ------- why it writes to green/ and not over the cache path
--
-- A transform's output shadows the cache by relative path: write
-- "sprites/red.png" and every draw of the player is green, everywhere,
-- always.  That is one line shorter and it takes the PLAYER option away --
-- there would be no red art left to switch back to.
--
-- So the outputs go under a "green/" prefix, which matches nothing the
-- importer writes and therefore shadows nothing.  They are still reachable:
-- Assets.resolve rewrites any "assets/generated/<rel>" through
-- save/mod-derived/<id>/<rel> whether or not the cache has a file there
-- (src/render/Assets.lua, derivedPath).  main.lua points the player's
-- records at "assets/generated/green/..." when the option says GREEN and
-- leaves them alone when it says RED, and both sets exist the whole time.
--
-- ------- the sandbox
--
-- No require, no love, no io, no os.  ctx is the entire surface, so the
-- palette below is a copy of tools/palette.py's rather than an import of
-- it; tools/check.py fails if the two ever disagree.

return function(ctx)
  -- lightest first, which is the order ctx.recolor reads.  PAPER stays pure
  -- white on purpose: the battle back pic is matted on shade 0 at draw time,
  -- and a near-white would leave a box around the player.
  local WILD_GREEN = {
    { 0xff, 0xff, 0xff },   -- paper
    { 0x65, 0xba, 0x3f },   -- light  #65ba3f
    { 0x1e, 0x7a, 0x2b },   -- dark   #1e7a2b
    { 0x00, 0x00, 0x00 },   -- ink
  }

  -- Every picture of the player, by its cache-relative path.
  --
  --   sprites/red.png        the overworld walker (SPRITE_RED, 16x96)
  --   sprites/red_bike.png   the same on the BICYCLE, where the import made one
  --   battle/redb.png        the battle back pic, drawn at 2x until "Go!"
  --   trainer_card/red.png   the front pic: Oak's intro, the card, Hall of Fame
  --   title/player.png       the title screen's standing Red
  --
  -- The old man's demo back pic (battle/oldmanb.png) is deliberately absent:
  -- he is not the player and the catch tutorial should not turn green.
  local PICS = {
    "sprites/red.png",
    "sprites/red_bike.png",
    "battle/redb.png",
    "trainer_card/red.png",
    "title/player.png",
  }

  for _, rel in ipairs(PICS) do
    -- A cache that does not carry one of these is a cache from a version or
    -- an import that never made it, not a broken install: skip it and let
    -- main.lua fall back to the vanilla path for that picture.
    if ctx.exists(rel) then
      ctx.writeImage(ctx.recolor(ctx.readImage(rel), WILD_GREEN),
        "green/" .. rel)
    end
  end
end

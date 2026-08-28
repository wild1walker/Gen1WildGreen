-- Wild Green
--
-- The player is green and the title screen says so.  That is the whole mod.
--
-- It is the identity half of the Wild Green cart: the cart pins the two
-- Gen1Wild bundles for everything a playthrough actually does, and this
-- supplies the one thing a pinned mod set cannot -- a game that looks like
-- its own version rather than like Red with things added.
--
-- ------- the three seams it uses, and why each one
--
--   sprites            the overworld walker.  A record, so it is decided at
--                      load: PLAYER takes effect on the next launch.
--   field.playerPics   the battle back pic and the front pic Oak's intro,
--                      the trainer card and the Hall of Fame share.
--   field.boot.title   the title screen's standing Red, and the version
--                      ribbon.  boot.title is the mod-reachable half of
--                      field.title, which the field schema does not expose.
--   palettes LOGO1     the SGB palette the title's ribbon band wears.
--
-- None of the green pixels are here.  Every recolored picture is written by
-- transforms.lua out of the player's own imported cache, under a "green/"
-- prefix that shadows nothing, and this file points records at it.  Read
-- that file first: it explains why the prefix exists and what it buys.
--
-- ------- what PLAYER = RED still changes
--
-- Nothing about the character, which is the point.  The ribbon stays "WILD
-- GREEN VERSION" and the band stays green either way: that is the game's
-- name, not the character's outfit, and a cart called Wild Green that boots
-- to "Red Version" is a cart with the label peeled off.  TITLE RIBBON is
-- the switch for people who want the vanilla ribbon back.

return function(mod)
  local CACHE = "assets/generated/"
  local GREEN = CACHE .. "green/"

  -- The Wild Green four, lightest first.  A copy of the ramp in
  -- transforms.lua, which cannot be imported from -- tools/check.py fails
  -- the build if the two drift apart.  Only shades 2 and 3 are green; 1 and
  -- 4 are the paper and ink every palette in the engine shares.
  local WILD_GREEN = {
    { 0xff, 0xff, 0xff },
    { 0x65, 0xba, 0x3f },
    { 0x1e, 0x7a, 0x2b },
    { 0x00, 0x00, 0x00 },
  }

  -- Exactly the set transforms.lua recolors, keyed the way a record names
  -- them.  A picture that is not in here has no green counterpart on disk,
  -- so pointing a record at one would draw nothing at all.
  local RECOLORED = {
    ["sprites/red.png"] = true,
    ["sprites/red_bike.png"] = true,
    ["battle/redb.png"] = true,
    ["trainer_card/red.png"] = true,
    ["title/player.png"] = true,
  }

  mod.options:define({
    -- The character, and the only thing here a player is likely to want
    -- both ways: GREEN is what the cart is for, RED is the vanilla art
    -- untouched.  A record decides the overworld walker, so this one lands
    -- on the next launch rather than mid-step.
    { key = "player", type = "choice", label = "PLAYER",
      choices = { { "GREEN", "green" }, { "RED", "red" } },
      default = "green" },
    -- The title screen's version ribbon and the band it sits in.  Off gives
    -- back the imported ribbon and the imported band colour, which is to
    -- say the title screen the base game booted to.
    { key = "ribbon", type = "toggle", label = "TITLE RIBBON",
      default = true },
  })

  -- options:get can throw on a profile that has never stored a value for a
  -- row; every mod in the suite reads through a guard like this one.
  local function option(key, fallback)
    local ok, value = pcall(function() return mod.options:get(key) end)
    if not ok or value == nil then return fallback end
    return value
  end

  -- The green twin of a cache path, or nil when there is not one.
  --
  -- The nil is the useful half.  The entry chunk runs before the merge, so
  -- what a registry hands back here is the pristine vanilla record -- but a
  -- record whose art the import never wrote, or that a later mod means to
  -- replace, is one we have no green for and should not touch.
  local function greenOf(path)
    if type(path) ~= "string" then return nil end
    local rel = path:match("^" .. CACHE .. "(.+)$")
    if rel and RECOLORED[rel] then return GREEN .. rel end
    return nil
  end

  -- Registry writes are pcall'd one at a time rather than in a block: a
  -- schema that has moved under us should cost the picture it names and not
  -- the four that were fine.
  local function try(what, fn)
    local ok, problem = pcall(fn)
    if not ok then
      mod.log:warn("%s: %s", what, tostring(problem))
    end
    return ok
  end

  -- ------- the character

  if option("player", "green") == "green" then
    -- Every sprite record drawn from a picture we recolored, which is
    -- SPRITE_RED and -- where the import wrote one -- the BICYCLE sheet.
    -- Found by image rather than by id so a name this mod guessed wrong is
    -- simply not matched instead of being patched into a broken record.
    try("sprites", function()
      for id, def in mod.content.sprites:each() do
        local green = type(def) == "table" and greenOf(def.image)
        if green then
          -- trueColor keeps the overworld's OBP bake off it.  Without it
          -- the palette pass would read our green through the same
          -- red-channel shade buckets it reads grey art through and remap
          -- it to something else; with it, SpriteRenderer:resolveImage
          -- hands the image over as drawn (src/render/SpriteRenderer.lua,
          -- liveTrueColor).
          mod.content.sprites:patch(id, { image = green, trueColor = true })
        end
      end
    end)

    -- The battle back pic and the front pic.  demoBack is the catch
    -- tutorial's old man and oakBack is Oak: neither is the player, and
    -- neither is in RECOLORED, so greenOf declines them on its own.
    try("field.playerPics", function()
      local pics = mod.content.field:get("playerPics")
      if type(pics) ~= "table" then return end
      local patch = {}
      for _, key in ipairs({ "back", "front" }) do
        local green = greenOf(pics[key])
        if green then patch[key] = green end
      end
      if next(patch) then
        mod.content.field:patch("playerPics", patch)
      end
    end)
  end

  -- ------- the title screen

  -- The standing Red on the title is not playerPics; TitleState reads it off
  -- field.title.player and falls back to the cache path.  It follows PLAYER
  -- because it is the character, not the branding.
  local titlePatch = {}
  if option("player", "green") == "green" then
    titlePatch.player = GREEN .. "title/player.png"
  end

  if option("ribbon", true) then
    -- versionRibbon, not version: the importer's key is the vanilla pair of
    -- fragments the draw pass repositions, and ours is one continuous strip.
    -- TitleState centres a versionRibbon whole at y=64 (src/ui/TitleState.lua).
    titlePatch.versionRibbon = mod.assets:path("assets/title/wild_green_version.png")
  end

  if next(titlePatch) then
    try("field.boot.title", function()
      mod.content.field:patch("boot", { title = titlePatch })
    end)
  end

  if option("ribbon", true) then
    -- The ribbon art is grey, because the band it lands in is an SGB
    -- palette zone: TitleState:sgbPalettes colours tile rows 8-9 with
    -- LOGO1 and the shader remaps by shade.  So the green comes from here.
    --
    -- This is the one thing in the mod that does not reach every display
    -- mode.  PaletteFX.pal short-circuits every name to the boot-ROM
    -- palette under OG RED, and reads data/palettes_gbc under ADVANCED, so
    -- in those two the band wears the mode's own colour and the lettering
    -- is red.  It is a registry record only in SGB.  DIFFERENCES.md says so.
    try("palettes.LOGO1", function()
      mod.content.palettes:override("LOGO1", WILD_GREEN)
    end)
  end
end

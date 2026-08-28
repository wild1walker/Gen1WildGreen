-- Headless coverage of the two files that decide what Wild Green does.
--
-- Neither can be exercised in place: main.lua wants the loader's `mod` table
-- and transforms.lua wants the asset sandbox's `ctx`.  Both are small, honest
-- surfaces, so both are stood up here and the real files are run against
-- them.  What is checked is everything settled before a pixel is drawn:
--
--   * the recipe recolors exactly the five player pictures, writes them under
--     green/ where they shadow nothing, and skips a picture the cache has
--     not got rather than failing the run;
--   * PLAYER = GREEN repoints the overworld walker and the BICYCLE sheet and
--     leaves every other sprite -- Oak's included -- alone;
--   * it repoints the battle back pic and the front pic, and does NOT touch
--     the old man's demo back pic;
--   * PLAYER = RED writes no character patch at all, which is the switch the
--     cart promises;
--   * TITLE RIBBON is the only thing that decides the ribbon and LOGO1, and
--     it is independent of PLAYER;
--   * the ramp in main.lua is the ramp in transforms.lua, byte for byte.
--
-- Run:  luajit tests/wild_green_test.lua   (from the mod's root)

local MOD = ""

local passed, failed = 0, 0
local function ok(condition, description)
  if condition then
    passed = passed + 1
  else
    failed = failed + 1
    io.write("  FAIL  ", description, "\n")
  end
end
local function eq(actual, expected, description)
  if actual ~= expected then
    io.write(("  FAIL  %s\n         got %s, wanted %s\n")
      :format(description, tostring(actual), tostring(expected)))
    failed = failed + 1
  else
    passed = passed + 1
  end
end

local function chunk(path)
  local loaded, problem = loadfile(path)
  if not loaded then error(problem, 0) end
  return loaded()
end

-- ------- the asset sandbox

-- Everything the recipe is handed, and nothing else: the real ctx has no
-- require, no love and no io either.
local function fakeCtx(cache)
  local ctx = { written = {}, read = {} }
  function ctx.exists(rel) return cache[rel] == true end
  function ctx.readImage(rel)
    ctx.read[#ctx.read + 1] = rel
    return { image = rel }
  end
  function ctx.recolor(image, shades)
    return { image = image.image, shades = shades }
  end
  function ctx.writeImage(image, rel)
    ctx.written[rel] = image
    return rel
  end
  return ctx
end

local VANILLA = {
  ["sprites/red.png"] = true,
  ["sprites/red_bike.png"] = true,
  ["battle/redb.png"] = true,
  ["trainer_card/red.png"] = true,
  ["title/player.png"] = true,
  -- present in the cache, and none of our business
  ["battle/oldmanb.png"] = true,
  ["sprites/oak.png"] = true,
}

local function runTransform(cache)
  local ctx = fakeCtx(cache)
  chunk(MOD .. "transforms.lua")(ctx)
  return ctx
end

io.write("transforms.lua\n")
do
  local ctx = runTransform(VANILLA)
  local wrote = {}
  local count = 0
  for rel in pairs(ctx.written) do
    wrote[rel] = true
    count = count + 1
  end
  eq(count, 5, "five pictures written")
  for _, rel in ipairs({ "sprites/red.png", "sprites/red_bike.png",
                         "battle/redb.png", "trainer_card/red.png",
                         "title/player.png" }) do
    ok(wrote["green/" .. rel], "green/" .. rel .. " written")
  end
  ok(not wrote["green/battle/oldmanb.png"],
    "the old man's demo back pic is left alone")
  ok(not wrote["green/sprites/oak.png"], "Oak is left alone")

  -- nothing lands on a cache path, which is what keeps the RED switch alive
  for rel in pairs(ctx.written) do
    ok(rel:sub(1, 6) == "green/", rel .. " is under green/")
  end

  local shades = ctx.written["green/sprites/red.png"].shades
  eq(#shades, 4, "the ramp is four colours")
  eq(("%02x%02x%02x"):format(shades[1][1], shades[1][2], shades[1][3]),
    "ffffff", "shade 1 is pure white, so a battle pic still mattes")
  eq(("%02x%02x%02x"):format(shades[2][1], shades[2][2], shades[2][3]),
    "65ba3f", "shade 2 is the reference sprite green")
  eq(("%02x%02x%02x"):format(shades[3][1], shades[3][2], shades[3][3]),
    "1e7a2b", "shade 3 is the ribbon green")
  eq(("%02x%02x%02x"):format(shades[4][1], shades[4][2], shades[4][3]),
    "000000", "shade 4 is ink")
end

do
  -- an import that never wrote a BICYCLE sheet is a cache, not a fault
  local thin = {}
  for rel in pairs(VANILLA) do thin[rel] = true end
  thin["sprites/red_bike.png"] = nil
  local ctx = runTransform(thin)
  ok(ctx.written["green/sprites/red.png"] ~= nil, "the walker is still written")
  ok(ctx.written["green/sprites/red_bike.png"] == nil,
    "a missing BICYCLE sheet is skipped, not invented")
end

-- ------- the loader's mod table

local function fakeRegistry(base, log)
  local registry = { base = base, patches = {}, overrides = {} }
  function registry:get(id) return self.base[id] end
  function registry:each()
    return coroutine.wrap(function()
      for id, def in pairs(self.base) do coroutine.yield(id, def) end
    end)
  end
  function registry:patch(id, partial)
    self.patches[id] = partial
    log[#log + 1] = "patch " .. id
  end
  function registry:override(id, value)
    self.overrides[id] = value
    log[#log + 1] = "override " .. id
  end
  return registry
end

local function fakeMod(options)
  local log = {}
  local mod = { log = {}, calls = log }
  function mod.log:warn(...) log[#log + 1] = "warn " .. select(1, ...) end
  function mod.log:error(...) log[#log + 1] = "error " .. select(1, ...) end

  mod.options = {
    defined = nil,
    define = function(self, rows) self.defined = rows end,
    get = function(_, key) return options[key] end,
  }
  mod.assets = {
    path = function(_, rel) return "mods/wild_green/" .. rel end,
  }

  mod.content = {
    sprites = fakeRegistry({
      SPRITE_RED = { image = "assets/generated/sprites/red.png",
                     frames = 6, walker = true },
      SPRITE_RED_BIKE = { image = "assets/generated/sprites/red_bike.png",
                          frames = 6, walker = true },
      SPRITE_OAK = { image = "assets/generated/sprites/oak.png",
                     frames = 6, walker = true },
      BOULDER = { image = "assets/generated/sprites/boulder.png", frames = 1 },
    }, log),
    field = fakeRegistry({
      playerPics = {
        back = "assets/generated/battle/redb.png",
        front = "assets/generated/trainer_card/red.png",
        demoBack = "assets/generated/battle/oldmanb.png",
      },
      boot = { startMap = "REDS_HOUSE_2F" },
    }, log),
    palettes = fakeRegistry({
      LOGO1 = { { 255, 255, 255 }, { 255, 0, 0 }, { 148, 0, 0 }, { 0, 0, 0 } },
    }, log),
  }
  return mod
end

local function run(options)
  local mod = fakeMod(options)
  chunk(MOD .. "main.lua")(mod)
  return mod
end

io.write("main.lua -- PLAYER = GREEN\n")
do
  local mod = run({ player = "green", ribbon = true })
  local sprites = mod.content.sprites.patches

  ok(sprites.SPRITE_RED ~= nil, "the overworld walker is repointed")
  eq(sprites.SPRITE_RED and sprites.SPRITE_RED.image,
    "assets/generated/green/sprites/red.png", "...at the green path")
  eq(sprites.SPRITE_RED and sprites.SPRITE_RED.trueColor, true,
    "...and true-colour, so the OBP bake leaves it alone")
  ok(sprites.SPRITE_RED_BIKE ~= nil, "the BICYCLE sheet is repointed too")
  ok(sprites.SPRITE_OAK == nil, "Oak is not repainted")
  ok(sprites.BOULDER == nil, "the boulder is not repainted")

  local pics = mod.content.field.patches.playerPics
  ok(pics ~= nil, "the player pics are repointed")
  eq(pics and pics.back, "assets/generated/green/battle/redb.png",
    "...the battle back pic")
  eq(pics and pics.front, "assets/generated/green/trainer_card/red.png",
    "...and the front pic")
  ok(pics and pics.demoBack == nil,
    "the catch tutorial's old man stays as he was")

  local boot = mod.content.field.patches.boot
  ok(boot and boot.title, "field.boot.title is patched")
  eq(boot and boot.title and boot.title.player,
    "assets/generated/green/title/player.png",
    "the title's standing figure is green")
  eq(boot and boot.title and boot.title.versionRibbon,
    "mods/wild_green/assets/title/wild_green_version.png",
    "the ribbon is the mod's own art")
  ok(boot and boot.title and boot.title.version == nil,
    "versionRibbon, not version -- ours is one continuous strip")

  ok(mod.content.palettes.overrides.LOGO1 ~= nil, "LOGO1 is overridden")
  local logo = mod.content.palettes.overrides.LOGO1
  eq(logo and ("%02x%02x%02x"):format(logo[3][1], logo[3][2], logo[3][3]),
    "1e7a2b", "...to the Wild Green ramp")

  -- the rows the manager draws
  local rows = {}
  for _, row in ipairs(mod.options.defined or {}) do rows[row.key] = row end
  ok(rows.player ~= nil, "a PLAYER row is defined")
  eq(rows.player and rows.player.default, "green", "...defaulting to green")
  ok(rows.ribbon ~= nil, "a TITLE RIBBON row is defined")
end

io.write("main.lua -- PLAYER = RED\n")
do
  local mod = run({ player = "red", ribbon = true })
  ok(next(mod.content.sprites.patches) == nil,
    "no sprite is repointed: the character is vanilla again")
  ok(mod.content.field.patches.playerPics == nil,
    "the player pics are vanilla again")

  local boot = mod.content.field.patches.boot
  ok(boot and boot.title and boot.title.player == nil,
    "the title's standing figure is vanilla again")
  eq(boot and boot.title and boot.title.versionRibbon,
    "mods/wild_green/assets/title/wild_green_version.png",
    "the ribbon still says WILD GREEN VERSION -- it is the game's name")
  ok(mod.content.palettes.overrides.LOGO1 ~= nil,
    "...and the band is still green")
end

io.write("main.lua -- TITLE RIBBON off\n")
do
  local mod = run({ player = "green", ribbon = false })
  local boot = mod.content.field.patches.boot
  ok(boot and boot.title and boot.title.versionRibbon == nil,
    "the imported ribbon comes back")
  ok(mod.content.palettes.overrides.LOGO1 == nil,
    "...and so does the imported band colour")
  ok(mod.content.sprites.patches.SPRITE_RED ~= nil,
    "the player is still green: the two rows are independent")
end

io.write("main.lua -- a profile with no stored options\n")
do
  local mod = run({})
  ok(mod.content.sprites.patches.SPRITE_RED ~= nil,
    "an unanswered PLAYER falls back to green")
  ok(mod.content.palettes.overrides.LOGO1 ~= nil,
    "an unanswered TITLE RIBBON falls back to on")
end

io.write("main.lua -- a player already reskinned by another mod\n")
do
  -- greenOf declines a path we have no green for, so a record another mod
  -- has already pointed elsewhere is left where it points
  local mod = fakeMod({ player = "green", ribbon = true })
  mod.content.sprites.base.SPRITE_RED.image = "mods/some_other/hero.png"
  chunk(MOD .. "main.lua")(mod)
  ok(mod.content.sprites.patches.SPRITE_RED == nil,
    "a walker that is not vanilla art is not fought over")
end

io.write(("\n%d passed, %d failed\n"):format(passed, failed))
os.exit(failed == 0 and 0 or 1)

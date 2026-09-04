// Game constants, read out of the bundle. Data only — no behaviour lives here.
//
// Every number in this file was confirmed against the shipped bundle rather than
// inferred from play. When the game updates, this is the first file to re-check.
(function (root) {
  'use strict';

  const RESOURCES = ['food', 'wood', 'ore'];

  // Per-unit resource upkeep. Having this table is what lets us prevent a resource
  // drought by arithmetic instead of by learning from one.
  const UPKEEP = {
    warrior: { ore: 1 }, wizard: { food: 1 }, elf: { wood: 1 },
    thief: { wood: 1 }, bard: { food: 1 }, cleric: { ore: 1 },
    garrison: { food: 3 }, academy: { ore: 3 }, outpost: { food: 1, wood: 3 },
    guild: { ore: 4 }, troupe: { wood: 4 }, seminary: { food: 3 },
    council: { food: 2, wood: 3 }, nexus: { ore: 5 }, forest: { wood: 6, food: 2 },
    congress: { ore: 4, food: 3 }, theater: { wood: 4, food: 3 }, college: { ore: 6, wood: 2 },
    catapult: { ore: 3 }, builder: { wood: 5 }, engineer: { food: 8 },
  };

  // Production chain. Used to fold one child's worth into the parent's score.
  const CHAIN = {
    garrison: 'warrior', academy: 'wizard', outpost: 'elf',
    guild: 'thief', troupe: 'bard', seminary: 'cleric',
    council: 'garrison', nexus: 'academy', forest: 'outpost',
    congress: 'guild', theater: 'troupe', college: 'seminary',
  };

  const RESOURCE_UNITS = { farmer: 'food', lumberjack: 'wood', miner: 'ore' };

  // Of the game's actions, only the ones autoplay may use. Destructive actions are
  // blocked at the channel itself rather than by remembering not to send them.
  // show_upgrade / unlock_upgrade are what the game's own UI emits right after a
  // purchase. The reducer does not do it for us, so we have to send them or the
  // tree never opens.
  const ALLOWED = new Set(['buy_generator', 'buy_upgrade', 'activate_inspiration',
    'change_level', 'show_upgrade', 'unlock_upgrade']);
  const BLOCKED = new Set(['clear_save', 'restart_level', 'reset_state', 'cheats', 'unlock_all']);

  // Never bought. Fixed price of 1 gold with a limit of 200, so any score model puts
  // it first — and its effect is "stuns your army on purchase". Buy it repeatedly and
  // the game effectively stops.
  const UPGRADE_BLACKLIST = new Set(['cacofonix']);

  // Dungeon-only. Worth nothing in main combat, so they return nothing inside the
  // planning horizon.
  const DUNGEON_ONLY = new Set(['dungeonPrecision', 'mazeCrusher', 'lightfoot', 'elvenEyes',
    'lockPick', 'stuffedChests', 'generousLoot', 'divineLight', 'magicFire', 'fullChests',
    'vulnerableFrequencies']);

  // Upgrades that shorten a firing period. Same rule as the game's dp():
  //   effective period = max(1, ticksToGenerate + that upgrade's multiplier)
  // The multiplier starts at 0 and goes negative with each purchase. Taking a thief
  // from 5 ticks to 1 is a 5x output increase.
  const PERIOD_UPGRADE = { thief: 'fastHands' };

  // Direct-damage units used for the cold start. In that phase there are barely any
  // candidates or any gold, so a precise ranking means nothing, and support and
  // production chains have no basis for a valuation yet.
  const OPENING_UNITS = ['warrior', 'wizard', 'elf', 'thief', 'catapult'];

  // A conservative coefficient for converting gold output into damage.
  const GOLD_WEIGHT = 0.5;

  // Each chapter has its own save slot (campaign / dummy / newGamePlus / infinite).
  // Dispatching change_level directly skips the slot save and rehydrate, after which
  // the game sees an inconsistent state and runs a recovery path that puts the boss
  // back to 1 HP. So we drive the game's own UI instead.
  const CHAPTERS = [
    { id: 'campaign', slot: 'campaign', start: 'tutorial', levels: ['tutorial', 'mainGame'] },
    { id: 'dummy', slot: 'dummy', start: 'dummy', levels: ['dummy'], after: 'mainGame' },
    { id: 'newGamePlus', slot: 'newGamePlus', start: 'newGamePlus', levels: ['newGamePlus'], after: 'dummy' },
    { id: 'infinite', slot: 'infinite', start: 'infinite', levels: ['infinite'], after: 'dummy' },
    { id: 'kingBattle', slot: 'infinite', start: 'kingBattle', levels: ['kingBattle'] },
  ];
  const CHAPTER_HP = {
    tutorial: 1e6, mainGame: 25e9, newGamePlus: 25e9,
    dummy: 1e9, infinite: 1e12, kingBattle: 1e9,
  };
  const ALL_LEVELS = CHAPTERS.reduce((a, c) => a.concat(c.levels), []);
  const chapterOf = (lv) => CHAPTERS.find((c) => c.levels.includes(lv));

  const api = {
    RESOURCES, UPKEEP, CHAIN, RESOURCE_UNITS, ALLOWED, BLOCKED,
    UPGRADE_BLACKLIST, DUNGEON_ONLY, PERIOD_UPGRADE, OPENING_UNITS, GOLD_WEIGHT,
    CHAPTERS, CHAPTER_HP, ALL_LEVELS, chapterOf,
  };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).consts = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).consts = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));

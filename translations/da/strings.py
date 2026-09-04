# -*- coding: utf-8 -*-
"""The Danish UI strings.

Address: "du" throughout. Danish dropped "De" for ordinary use long ago, and a game
that used it would sound like a letter from the tax office. The King is grand in tone,
not in pronoun.

Danish has common and neuter gender and the article is glued to the end - "en kriger"
but "et tårn", "krigeren" but "tårnet" - so a noun and its article are written
together wherever one appears.

The game's own body font draws every letter Danish needs; only the display face lacks
the slashed O, so that is the one slot our font fills.
"""

T = {}

T.update({
    "upgrades.upgrades": "Opgraderinger",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Næste niveau",
    "upgrades.currentLevel": "Nuværende",
    "upgrades.newGamePlusOnly": "Kun i kapitlet \"Ressourcestyring\"",
    "upgrades.max": "Maks",
    "upgrades.lockedMessage": "Opgrader {{parentSkill}} mere for at låse denne op",
    "common.wishlistNow": "Sæt den på ønskelisten!",
})

T.update({
    "statistics.section.ttb": "Kamptid",
    "statistics.section.dgps": "Skade og guld i sekundet",
    "statistics.section.resourceBalance": "Ressourcebalance",
    "statistics.lifetime.title": "Samlet statistik",
    "statistics.lifetime.totalPlaytime": "Samlet spilletid",
    "statistics.lifetime.totalGoldEarned": "Guld tjent i alt",
    "statistics.lifetime.totalGoldSpent": "Guld brugt i alt",
    "statistics.lifetime.totalBirdsKilled": "Fugle skudt ned i alt",
    "statistics.lifetime.totalClicks": "Klik i alt",
    "statistics.lifetime.totalHeroesRecruited": "Helte hvervet i alt",
    "statistics.lifetime.heroesPurchased": "Købt",
    "statistics.lifetime.heroesRecruited": "Hvervet",
    "statistics.lifetime.tier1": "Trin 1 hvervet (købt)",
    "statistics.lifetime.tier2": "Trin 2 hvervet (købt)",
    "statistics.lifetime.tier3": "Trin 3 hvervet (købt)",
    "statistics.lifetime.totalDamageDealt": "Skade givet i alt",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Mistet til ildånde",
    "statistics.battleDuration": "Forløbet: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Kan det overhovedet vindes?",
    "statistics.infiniteEstimatedVictory": "Rigtig sejr er umulig!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Du er vores helt!</strong>];"
        " (0-1000000000)[Sejr om <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Klik eller tryk Z for at angribe dragen!</strong>]",
    "statistics.perSec": "/sek",
    "statistics.generationSection": "Produktion",
    "statistics.critSection": "Særligt",
    "statistics.dps": "Troppernes skade: <strong>{{dps}}/sek</strong>",
    "statistics.gps": "Troppernes guld: <strong>{{gps}}/sek</strong>",
    "statistics.dpc": "Skade per klik: <strong>{{dpc}}/klik</strong>",
    "statistics.gpc": "Guld per klik: <strong>{{gpc}}/klik</strong>",
    "statistics.catapultDamage": "Skade: <strong>{{damage}}/skud</strong>",
    "statistics.catapultTimeToShoot": "Til næste skud: <strong>{{time}} sek</strong>",
    "statistics.undo.disabledLine": "Klik inden for 10 sekunder for at fortryde et fejlkøb"
        " og få guldet igen.",
    "statistics.undo.enabledAction": "Klik for at fortryde købet af {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Du får {{refund}} tilbage.",
    "statistics.undo.enabledTimer": "{{seconds}} sekunder tilbage.",
    "statistics.undo.refundGold": "{{amount}} guld",
})

for base, one, many in [
    ("seconds", "sekund", "sekunder"), ("minutes", "minut", "minutter"),
    ("hours", "time", "timer"), ("days", "dag", "dage"),
    ("months", "måned", "måneder"), ("years", "år", "år"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_other"] = many

T.update({
    "generators.generators": "Tropper",
    "generators.buy": "køb {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} sek",
    "generators.ngPlusProductionToggle": "Slå produktion til eller fra",
    "generators.tabs.troops": "Tropper",
    "generators.tabs.support": "Støtte",
    "generators.fireUnitsButton.tooltip": "Afskedig tropper for at bruge færre ressourcer"
        " og alligevel beholde en del af produktionen.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Den magiske kraft bag troldmændenes angreb.",
    "generators.emptyManaDescription": "Køb \"Manastrøm\" for at angribe igen.",
    "generators.inspiration": "Inspiration",
    "generators.inspirationDescription": "Når den er i gang, mangedobles alle heltes styrke.",
    "generators.tabsAriaLabel": "troppefaner",
})

UNITS = {
    "warrior": ("Kriger", "Krigere"),
    "wizard": ("Troldmand", "Troldmænd"),
    "elf": ("Elver", "Elvere"),
    "garrison": ("Garnison", "Garnisoner"),
    "academy": ("Magiakademi", "Magiakademier"),
    "academy_short": ("Akademi", "Akademier"),
    "outpost": ("Bueskyttepost", "Bueskytteposter"),
    "outpost_short": ("Forpost", "Forposter"),
    "council": ("Krigsråd", "Krigsråd"),
    "nexus": ("Ærkemagernes knudepunkt", "Ærkemagernes knudepunkter"),
    "forest": ("Ældgammel skov", "Ældgamle skove"),
    "thief": ("Tyv", "Tyve"),
    "bard": ("Bard", "Barder"),
    "cleric": ("Præst", "Præster"),
    "guild": ("Tyvelaug", "Tyvelaug"),
    "guild_short": ("Laug", "Laug"),
    "troupe": ("Gøglertrup", "Gøglertrupper"),
    "troupe_short": ("Trup", "Trupper"),
    "seminary": ("Helligt seminarium", "Hellige seminarier"),
    "seminary_short": ("Seminarium", "Seminarier"),
    "congress": ("Skyggekonvent", "Skyggekonventer"),
    "theater": ("Stort teater", "Store teatre"),
    "college": ("Kardinalkollegium", "Kardinalkollegier"),
    "catapult": ("Katapult", "Katapulter"),
    "builder": ("Bygmester", "Bygmestre"),
    "engineer": ("Ingeniør", "Ingeniører"),
    "farmer": ("Bonde", "Bønder"),
    "lumberjack": ("Skovhugger", "Skovhuggere"),
    "miner": ("Minearbejder", "Minearbejdere"),
    "apprenticeships": ("Lærlingeplads", "Lærlingepladser"),
    "tradespeople": ("Håndværkere", "Håndværkere"),
}
for base, (one, many) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_other"] = many

T.update({
    "generators.unitDescription.warrior": "Hårdføre nærkampskæmpere.",
    "generators.unitDescription.wizard": "Slår til på mellemafstand, men tåler intet.",
    "generators.unitDescription.elf": "Skyder adræt på lang afstand, uden for dragens rækkevidde.",
    "generators.unitDescription.garrison": "Befæstet base, der hverver krigere.",
    "generators.unitDescription.outpost": "Fjern base, der hverver elvere.",
    "generators.unitDescription.academy": "Skole, der uddanner troldmænd til kamp.",
    "generators.unitDescription.council": "Militær organisation, der opretter garnisoner.",
    "generators.unitDescription.nexus": "Mystisk organisation, der opretter akademier.",
    "generators.unitDescription.forest": "Hellig skov, der opretter forposter.",
    "generators.unitDescription.thief": "Snu: forgifter dragen og stjæler dens guld.",
    "generators.unitDescription.bard": "Kan inspirere dine tropper til at kæmpe hårdere.",
    "generators.unitDescription.cleric": "Beskytter og hverver nye helte til kampen.",
    "generators.unitDescription.guild": "Underjordisk netværk, der hverver tyve.",
    "generators.unitDescription.troupe": "Omrejsende selskab, der hverver barder.",
    "generators.unitDescription.seminary": "Hellig institution, der uddanner præster.",
    "generators.unitDescription.congress": "Organisation i skyggerne, der opretter tyvelaug.",
    "generators.unitDescription.theater": "Vældig institution, der opretter gøglertrupper.",
    "generators.unitDescription.college": "Religiøs organisation, der opretter seminarier.",
    "generators.unitDescription.catapult": "Belejringsvåben, der gør stor skade på dragen.",
    "generators.unitDescription.builder": "Bygger bygninger på andet niveau.",
    "generators.unitDescription.engineer": "Opretter organisationer på højere niveauer.",
    "generators.unitDescription.farmer": "Dyrker mad til kongeriget.",
    "generators.unitDescription.lumberjack": "Fælder træ til byggeriet.",
    "generators.unitDescription.miner": "Bryder malm i bjergene.",
    "generators.unitDescription.apprenticeships": "Uddanner håndværkere.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} skade/{{rate}} sek",
    "wizard": "{{generatorGeneration}} skade/{{rate}} sek",
    "elf": "{{generatorGeneration}} skade/{{rate}} sek",
    "catapult": "{{generatorGeneration}} skade/{{rate}} sek",
    "thief": "+{{generatorGeneration}} guld/{{rate}} sek",
    "bard": "+{{generatorGeneration}} inspiration/{{rate}} sek",
    "cleric": "+{{generatorGeneration}} helte/{{rate}} sek",
    "builder": "+{{generatorGeneration}} bygninger/{{rate}} sek",
    "engineer": "+{{generatorGeneration}} organisationer/{{rate}} sek",
    "farmer": "+{{generatorGeneration}} mad/{{rate}} sek",
    "lumberjack": "+{{generatorGeneration}} træ/{{rate}} sek",
    "miner": "+{{generatorGeneration}} malm/{{rate}} sek",
}
for k, v in GEN_PLAIN.items():
    T[f"generators.generationDescription.{k}"] = v

GEN_NESTED = {
    "garrison": "warrior", "outpost": "elf", "academy": "wizard", "council": "garrison",
    "nexus": "academy_short", "forest": "outpost_short", "guild": "thief",
    "troupe": "bard", "seminary": "cleric", "theater": "troupe_short",
    "college": "seminary_short", "congress": "guild_short",
    "apprenticeships": "tradespeople",
}
for k, ref in GEN_NESTED.items():
    T[f"generators.generationDescription.{k}"] = (
        "+{{generatorGeneration}} $t(" + ref + ', {"count": {{generatorGeneration}} })/{{rate}} sek')

T.update({
    "settings.settings": "Indstillinger",
    "settings.buy_max": "Køb maks",
    "settings.audio": "Musik og lyd",
    "settings.game": "Spil",
    "settings.graphics": "Grafik",
    "settings.offline_progress": "Fremgang offline",
    "settings.wishlist_now": "Sæt på ønskelisten",
    "menus.settings": "Indstillinger",
    "menus.tabs.game": "Spil",
    "menus.tabs.graphics": "Grafik",
    "menus.tabs.audio": "Lyd",
    "menus.tabs.levels": "Kapitler",
    "menus.tabs.credits": "Medvirkende",
    "menus.credits.title": "Medvirkende",
    "menus.credits.developedBy": "Udviklet af",
    "menus.credits.developedWith": "Udviklet med",
    "menus.credits.bigThanksTo": "Stor tak til",
    "menus.credits.theRestOfTheDiscordServer": "alle andre på Discord-serveren",
    "menus.credits.andYou": "og dig!",
    "menus.music": "Musik",
    "menus.sfx": "Lydeffekter",
    "menus.audioSettings": "Lydindstillinger",
    "menus.gameSettings": "Spilindstillinger",
    "menus.graphicsSettings": "Grafikindstillinger",
    "menus.language": "Sprog",
    "menus.languages.en": "Engelsk",
    "menus.languages.fr": "Fransk",
    "menus.languages.de": "Tysk",
    "menus.languages.pt": "Portugisisk",
    "menus.languages.tr": "Tyrkisk",
    "menus.shakeIntensity": "Rysten",
    "menus.largerTextSize": "Større tekst",
    "menus.crtFilter": "CRT-filter",
    "menus.chromaticAberrationSlider": "Farvespredning",
    "menus.chromaticAberration": "Farvespredning",
    "menus.swordSwooshSounds": "Sværd- og kritiske lyde",
    "menus.catSounds": "Kattelyde",
    "menus.fullscreen": "Fuld skærm",
    "menus.resume": "Spil videre",
    "menus.close": "Luk",
    "menus.quitGame": "Afslut spillet",
    "menus.joinDiscord": "Kom med på Discord",
    "menus.clear_save_label": "Slet din fremgang?",
    "menus.zoom_adjustment": "Zoom på brugerfladen",
    "menus.clear_save": "Slet nu",
    "menus.are_you_sure": "Er du sikker?",
    "menus.cannot_be_reversed": "Det kan ikke fortrydes.",
    "menus.yes": "Ja",
    "menus.no": "Nej",
})

T.update({
    "tooltip.inspiration": "Inspiration",
    "tooltip.inspirationDescription": "Når den er i gang, mangedobles alle heltes styrke.",
    "tooltip.maxInspiration": "Højeste multiplikator",
    "tooltip.maxInspirationMultiplier": "Højeste multiplikator",
    "tooltip.statisticsDescription": "Udførlige tal om din fremgang og kampen.",
    "tooltip.hudStopBird": "Stop fuglen",
    "tooltip.hudLifetimeStats": "Samlet statistik",
    "tooltip.hudHideWindows": "Skjul vinduer",
    "tooltip.events.roar": "Lammende brøl",
    "tooltip.events.fire": "Ildånde",
    "tooltip.events.claw": "Kloslag",
    "tooltip.events.dialog": "Særlig begivenhed",
    "tooltip.events.pope_visit": "Et særligt besøg",
    "tooltip.events.dungeon_keys": "En mørk hemmelighed",
    "tooltip.events.missing_king": "Hvor er kongen?",
    "tooltip.events.catapult": "En teknisk prototype",
    "tooltip.events.engineer": "Hjælp i rette tid",
    "tooltip.events.invasion_start": "En invasion er på vej",
    "tooltip.events.invasion_end": "Bud fra tropperne",
    "tooltip.events.apprenticeships_unlock": "Lærlingepladser låst op",
    "tooltip.events.trading": "En omrejsende købmand",
    "tooltip.events.dummy_toy_reveal": "Ikke hvad jeg troede",
})

T.update({
    "infos.banner.events": "Begivenheder",
    "infos.banner.stats": "Statistik",
    "infos.banner.engineering": "Teknik",
    "infos.banner.resources": "Ressourcer",
    "infos.tabs.events": "Begivenheder",
    "infos.tabs.stats": "Statistik",
    "infos.tabs.engineering": "Teknik",
    "infos.tabs.resources": "Ressourcer",
    "infos.tabsAriaLabel": "informationsfaner",
    "game.dummy": "Den store trædukke",
    "game.infiniteBird": "Fuglen der ikke kan fældes",
    "game.king": "Kongen",
    "game.smallDragon": "Tuth'orieth, den spirede",
    "game.bigDragon": "Forth'aarh, som giver og tager liv",
    "dungeon.found": "Fundet",
    "dungeon.giveUp": "Giv op",
    "dungeon.tooltipDescription": "Udforsk fangehullet (niveau {{level}})",
    "dungeon.cooldownMessage": "Fangehullet hviler. Vent {{seconds}} sekunder på at gå ind igen.",
    "dungeon.cooldownShort": "{{seconds}} sek",
    "dungeon.levelLabel": "Niveau",
    "dungeon.levelShort": "Niveau {{level}}",
    "dungeon.keysOwned": "Nøgler",
    "dungeon.giveUpTooltip": "Forlad fangehullet (behold en del af byttet med Gavmildt bytte)",
    "dungeon.moveHint": "WASD eller piletaster for at gå",
    "dungeon.attackHint": "Klik på monstre for at angribe",
    "dungeon.chestCountsTooltip": "{{opened}} af {{total}} kister åbnet",
    "dungeon.exitDirection": "UDGANG",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Vellykket tur",
    "summaries.dungeonLoot.titleFailed": "Mislykket tur",
    "summaries.dungeonLoot.titleStuckRescue": "Sluppet sikkert ud",
    "summaries.dungeonLoot.lootSummarySubtitle": "Oversigt over byttet",
    "summaries.dungeonLoot.body_one": "Fik {{gold}} guld og {{grayKeys}} nøgle",
    "summaries.dungeonLoot.body_other": "Fik {{gold}} guld og {{grayKeys}} nøgler",
    "summaries.dungeonLoot.artifactFound": "Fandt {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Tab til ildånden",
    "summaries.fireBreathCasualties.body": "Mistede {{list}}",
    "summaries.fireBreathCasualties.none": "Ingen tab",
    "summaries.fireBreathBlocked.title": "Ildånden blev stoppet!",
    "summaries.fireBreathBlocked.body": "En røgbombe reddede dine tropper.",
    "summaries.toastLabel": "Spilbesked",
})

T.update({
    "levels.title": "Kapitler",
    "levels.locked": "Låst",
    "levels.active": "I gang",
    "levels.completed": "Gennemført",
    "levels.continue": "Fortsæt",
    "levels.start": "Start",
    "levels.restart": "Spil igen",
    "levels.restart_progress_warning": "Spil igen nu? Du mister den ugemte fremgang i dette kapitel.",
    "levels.names.mainGame": "En stor drage",
    "levels.names.newGamePlus": "Ressourcestyring",
    "levels.names.dummy": "Et magisk legetøj",
    "levels.names.infinite": "Virkelig uendeligt",
    "levels.names.kingBattle": "Kongens sidste kamp",
})

T.update({
    "menus.tabs.saveData": "Gemte data",
    "menus.saveData.title": "Gemte data",
    "menus.saveData.clearChapterTitle": "Kapitlernes fremgang",
    "menus.saveData.clearChapterExplanation": "Sletter guld, tropper, opgraderinger, fremgang"
        " i fangehullet og gennemført-mærker for hvert kapitel. Oplåste kapitler, samlet"
        " statistik, indstillinger og artefakter beholdes.",
    "menus.saveData.clearChapterButton": "Slet kapitlernes fremgang",
    "menus.saveData.clearFullTitle": "Alle gemte data",
    "menus.saveData.clearFullExplanation": "Sletter alt det, kapitelnulstillingen sletter,"
        " og desuden artefakter, oplåste kapitler og samlet statistik. Indstillinger for"
        " lyd, grafik og sprog beholdes.",
    "menus.saveData.clearFullButton": "Slet alle gemte data",
    "menus.saveData.clearFullWarning": "Det kan ikke fortrydes. Du mister artefakter,"
        " oplåste kapitler og samlet statistik.",
})

T.update({
    "artifacts.title": "Artefakter",
    "artifacts.subtitle": "Sjældne artefakter dukker af og til op i særlige kister i"
        " fangehullet. De følger med fra kapitel til kapitel.",
    "artifacts.notYetFound": "(ikke fundet endnu)",
})

ART = {
    "phoenixWhistle": ("Fønikspiben", "En særlig fugl bringer en ny mønt med sig."),
    "emberforgedShield": ("Gløderskjold", "Krigere tager ingen skade af drageild."),
    "moonwellFlask": ("Flaske fra månebrønden", "Troldmænd bruger kun halvt så meget mana."),
    "windstepAnklet": ("Vindtrinets ankelring", "Elvere bliver ikke lammet."),
    "fangSatchel": ("Hugtandstaske", "Mens runden kører, laver tyve en dragetand hvert halve time."),
    "slumberBerries": ("Slumrebær", "Gift forsinker dragens brøl og ild med 10 sekunder."),
    "echoingLute": ("Ekkoende lut", "Barder giver dobbelt inspiration."),
    "blessingCenser": ("Velsignelsens røgelseskar", "Præster hverver altid dobbelt så mange."),
    "victoryTusk": ("Sejrstanden", "Et gennemført niveau giver dobbelt så mange dragetænder."),
    "cartographersLedger": ("Korttegnerens bog", "Viser hvor mange af fangehullets kister der er åbnet."),
    "ironSkeletonKey": ("Dirk af jern", "Låser fangehullet op til niveau 20."),
    "everflameLantern": ("Evigflammens lygte", "Faklen går aldrig ud."),
    "midasCoin": ("Midasmønten", "Dobbelt så meget guld i fangehullet."),
    "harvestIdol": ("Høstgudebilledet", "Ressourcer kommer ind 25 % hurtigere."),
    "titanGauntlet": ("Titanhandsken", "Ti gange så meget skade per klik."),
    "wayfindersCompass": ("Vejviserens kompas", "Peger mod fangehullets udgang."),
    "loadedDice": ("Falske terninger", "Hvert klik er kritisk."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Jernfinger", "+{{bonus}} skade per klik"),
    "featherFinger": ("Fjerfinger", "+{{bonus}} klik i sekundet"),
    "wakeupCall": ("Vækning", "Hvert klik forkorter lammelsen med {{bonus}} sekunder"),
    "electricalFinger": ("Elektrisk finger", "Hvert klik har {{bonus}} % chance for at kalde lynet."),
    "perfectClick": ("Perfekt klik", "+{{bonus}} % chance for kritisk klik"),
    "criticalStrike": ("Kritisk slag", "+{{bonus}}x skade ved kritisk klik"),
    "goldenExplosion": ("Gylden eksplosion", "{{bonus}}x belønning når du klikker på fugle"),
    "naturalLeader": ("Født leder", "Klik fylder inspirationsmåleren med +{{bonus}}/klik"),
    "moneyCursor": ("Guldmarkør", "{{bonus}}x guld per klik"),
    "fullChests": ("Fulde kister", "{{bonus}} % mindre chance for at en kiste i fangehullet er tom"),
    "carpalCure": ("Håndledskur", "Hold museknappen nede for at angribe dragen uden ophør."),
    "shortSword": ("Kortsværd", "+{{bonus}}x skademultiplikator for {{type}}"),
    "longSword": ("Langsværd", "Endnu +{{bonus}}x skademultiplikator for krigere"),
    "twoHandedSword": ("Tohåndssværd", "Yderligere +{{bonus}}x skademultiplikator for krigere"),
    "battleShout": ("Kampråb", "Fylder inspirationsmåleren med +{{bonus}} per slag"),
    "warCry": ("Krigsråb", "Sætter inspirationen i gang af sig selv ved næste tik,"
               " når multiplikatoren er på højeste"),
    "barbarian": ("Barbar", "+{{bonus}} grundskade"),
    "thickArmor": ("Tyk rustning", "{{bonus}} % mindre fysisk skade"),
    "fireArmor": ("Ildrustning", "{{bonus}} % færre tropper dør af ildånden"),
    "heavyRocks": ("Tunge sten", "+{{bonus}} % katapultskade per niveau"),
    "silverBlade": ("Sølvklinge", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenBlade": ("Gylden klinge", "Endnu +{{bonus}}x multiplikator på guld per slag"),
    "loyalMercenaries": ("Trofaste lejesvende", "{{typePlural}} du køber gør +{{bonus}}x skade per niveau"),
    "loyalServants": ("Trofaste tjenere", "{{bonus}} % billigere at hverve {{type}} og alt derover"),
    "teamWork": ("Samarbejde", "Hverver ekstra {{typePlural}} for hver {{type}} du køber"),
    "dungeonPrecision": ("Præcision i dybet", "+{{bonus}} % chance for kritisk træf i fangehullet"),
    "mazeCrusher": ("Labyrintknuseren", "+{{bonus}} kritisk skade i fangehullet"),
    "magicMissile": ("Magisk projektil", "+{{bonus}}x skademultiplikator for {{type}}"),
    "manaSword": ("Manasværd", "Hver troldmand fylder en krigers sværd med mana."
                  " +{{bonus}}x skademultiplikator når manaen er over 90"),
    "magicMouse": ("Magisk mus", "Fylder manamåleren med +{{bonus}} per klik"),
    "manaSurge": ("Manastrøm", "Fylder troldmændenes manamåler"),
    "manaPool": ("Manakilde", "+{{bonus}} % højeste mana"),
    "manaBoost": ("Manastød", "Troldmændenes skade fordobles når manaen er over {{current}}"),
    "weatherForecast": ("Vejrudsigt", "+{{bonus}} % chance for lynnedslag"),
    "lightningStrike": ("Lynnedslag", "Tilføjer et lyn, der gør +{{bonus}}x skade"
                        " af {{type}} for hver købt opgradering"),
    "silverStaff": ("Sølvstav", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenStaff": ("Gylden stav", "Endnu +{{bonus}}x multiplikator på guld per slag"),
    "magicFire": ("Magisk ild", "Faklen brænder +{{bonus}} sekunder længere"),
    "archimage": ("Ærkemager", "+{{bonus}} grundskade"),
    "huntersEye": ("Jægerens øje", "+{{bonus}} % chance for at ramme en fugl inden for rækkevidde hvert tik"),
    "criticalChance": ("Skarpt sigte", "+{{bonus}} % chance for kritisk skud"),
    "criticalDamage": ("Bladskæreren", "+{{bonus}}x skade ved kritisk skud"),
    "huntingSeason": ("Jagtsæson", "Kalder straks en flok fugle frem"),
    "elvenEyes": ("Elverøjne", "Du ser i mørket +{{bonus}} sekunder efter at faklen er gået ud"),
    "multipleShot": ("Flere pile", "Skyder en pil mere per niveau"),
    "silverArrow": ("Sølvpil", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenArrow": ("Gylden pil", "Endnu +{{bonus}}x multiplikator på guld per slag"),
    "iceArrow": ("Ispil", "Forsinker dragens ild med {{bonus}} sekunder"),
    "animalInstinct": ("Dyreinstinkt", "Katapulten skyder katte i stedet for sten,"
                       " og tigre i stedet for katte, ti gange skaden hver gang."),
    "lightningRod": ("Lynafleder", "{{bonus}} % chance for at trække endnu et lyn til,"
                     " når troldmændenes lyn rammer."),
    "recycledArrows": ("Genbrugte pile", "Elvernes angreb koster mindre træ"),
    "lightfoot": ("Let til bens", "+{{bonus}} % hurtigere at gå og dreje i fangehullet"),
    "fastHands": ("Hurtige hænder", "Forkorter tiden til at lave guld med {{bonus}} sekunder"),
    "sharpDagger": ("Snigmorderklinge", "Tyve angriber også, med {{current}} i skade"),
    "poisonDagger": ("Forgiftet dolk", "+{{bonus}} % chance for at forgifte dragen"),
    "blackMamba": ("Sort mamba", "+{{bonus}}x giftskade af tyvenes skade"),
    "lingeringToxin": ("Dvælende gift", "Giften varer +{{bonus}} sekunder længere"),
    "smokeBomb": ("Røgbombe", "Sætter en fælde for dragen med {{current}} % chance for at"
                  " udløses ved næste slag og stoppe det."),
    "catBomb": ("Kattebombe", "Katapultens ladning sprænger ved nedslaget, dobbelt skade."),
    "pickpocket": ("Lommetyv", "+{{bonus}}x multiplikator på det guld {{type}} laver"),
    "lockPick": ("Dirk", "Hver tur begynder med {{bonus}} døre allerede åbne."),
    "midasTouch": ("Midas' berøring", "Endnu +{{bonus}}x multiplikator på det guld {{type}} laver"),
    "stuffedChests": ("Stopfyldte kister", "+{{bonus}} % guld fra fangehullets kister"),
    "tuningFork": ("Stemmegaffel", "+{{bonus}} inspiration samlet"),
    "luteSolo": ("Lutsolo", "+{{bonus}}x højeste inspirationsmultiplikator"),
    "obnoxiousGuitarist": ("Ulidelig guitarist", "Inspirationen varer +{{bonus}} sekunder"),
    "piercedEardrums": ("Sprængte trommehinder", "Dragens brøltæller går {{bonus}} % langsommere"),
    "replay": ("Ekstranummer", "{{bonus}} % chance for at inspirationen begynder forfra når den slutter"),
    "sonicBarrier": ("Lydbarriere", "Dragens ildtæller går {{bonus}} % langsommere"),
    "cacofonix": ("Kakofonix", "Lammer dine egne tropper når du køber ham"),
    "churchChoir": ("Kirkekor", "Hverver 1 seminarium hver gang inspirationen slår til"),
    "encore": ("Dacapo", "Forkorter inspirationens hvile med {{bonus}} sekunder"),
    "lockerRoomSpeech": ("Tale i omklædningsrummet", "Laver inspiration mens spillet er lukket,"
                         " i {{current}} % af takten"),
    "orderInTheUk": ("Orden i kongeriget", "Mens spillet er lukket, får din musik håndværkerne"
                     " til at arbejde over og lave ressourcer i {{current}} % af den sædvanlige takt"),
    "majorKey": ("Durtoneart", "Køber en nøgle til fangehullet. (Ja, ordspillet er elendigt.)"),
    "vulnerableFrequencies": ("Sårbare frekvenser", "Fjender i fangehullet er udødelige"
                              " {{bonus}} millisekunder kortere efter hvert slag"),
    "heroResources": ("Heltepersonalet", "+{{bonus}} % chance for at hverve dobbelt så mange helte"),
    "blessedAura": ("Velsignet aura", "{{bonus}} % færre tropper dør af ildånden"),
    "blessedBird": ("Velsignet fugl", "{{current}} % chance for at en fugl kommer velsignet"
                    " og giver dobbelt guld"),
    "powerTransfer": ("Kraftoverførsel", "Ved hver hvervning fyldes troldmændenes mana med"
                      " 0,5 for hver præst du har"),
    "generousLoot": ("Gavmildt bytte", "Når en tur mislykkes, beholder du alligevel"
                     " {{current}} % af byttet."),
    "divineLight": ("Guddommeligt lys", "+{{bonus}} % chance for at tænde en slukket fakkel igen"),
    "recruitWarriors": ("Hverv krigere", "Lader dig hverve krigere til kampen"),
    "recruitElves": ("Hverv elvere", "Lader dig hverve elvere til kampen"),
    "recruitWizards": ("Hverv troldmænd", "Lader dig hverve troldmænd til kampen"),
    "recruitBards": ("Hverv barder", "Lader dig hverve barder til kampen"),
    "recruitThieves": ("Hverv tyve", "Lader dig hverve tyve til kampen"),
    "recruitClerics": ("Hverv præster", "Lader dig hverve præster til kampen"),
}
for k, (title, desc) in D.items():
    T[f"upgrades.details.{k}.title"] = title
    T[f"upgrades.details.{k}.description"] = desc

SUFFIX = {
    "wakeupCall.suffix": " sek",
    "elvenEyes.suffix": " sek",
    "iceArrow.suffix": " sek",
    "lingeringToxin.suffix": " sek",
    "obnoxiousGuitarist.suffix": " sek",
    "encore.suffix": " sek",
    "manaPool.suffix": " mana",
    "manaBoost.suffix": " mana",
    "huntingSeason.suffix": " fugle",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

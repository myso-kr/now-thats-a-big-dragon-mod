# -*- coding: utf-8 -*-
"""The Swedish UI strings.

Address: "du" throughout, which is what Swedish has used for everyone since the
du-reformen and what every game speaks. The King is formal in tone rather than in
form - he asks and thanks, he does not use "ni".

Swedish has two genders, and the article rides on the noun: "en uppgradering" but
"ett torn". Counted nouns keep the same form in both plural categories the language
uses, so a count of one and a count of many read alike.

The game's own font covers Swedish - a, a-ring, a-diaeresis and o-diaeresis are all in
Everyday_Standard - so nothing of ours ships for it beyond the subset.
"""

T = {}

T.update({
    "upgrades.upgrades": "Uppgraderingar",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Nästa nivå",
    "upgrades.currentLevel": "Nuvarande",
    "upgrades.newGamePlusOnly": "Endast i kapitlet \"Resurshantering\"",
    "upgrades.max": "Max",
    "upgrades.lockedMessage": "Uppgradera {{parentSkill}} mer för att låsa upp den här",
    "common.wishlistNow": "Lägg till i önskelistan!",
})

T.update({
    "statistics.section.ttb": "Stridstid",
    "statistics.section.dgps": "Skada och guld per sekund",
    "statistics.section.resourceBalance": "Resursbalans",
    "statistics.lifetime.title": "Total statistik",
    "statistics.lifetime.totalPlaytime": "Total speltid",
    "statistics.lifetime.totalGoldEarned": "Guld intjänat totalt",
    "statistics.lifetime.totalGoldSpent": "Guld spenderat totalt",
    "statistics.lifetime.totalBirdsKilled": "Fåglar nedskjutna totalt",
    "statistics.lifetime.totalClicks": "Klick totalt",
    "statistics.lifetime.totalHeroesRecruited": "Hjältar värvade totalt",
    "statistics.lifetime.heroesPurchased": "Köpta",
    "statistics.lifetime.heroesRecruited": "Värvade",
    "statistics.lifetime.tier1": "Nivå 1 värvade (köpta)",
    "statistics.lifetime.tier2": "Nivå 2 värvade (köpta)",
    "statistics.lifetime.tier3": "Nivå 3 värvade (köpta)",
    "statistics.lifetime.totalDamageDealt": "Skada gjord totalt",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Förlorade till eldsprutning",
    "statistics.battleDuration": "Förfluten tid: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Går det ens att vinna?",
    "statistics.infiniteEstimatedVictory": "Verklig seger är omöjlig!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Du är vår hjälte!</strong>];"
        " (0-1000000000)[Seger om <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Klicka eller tryck Z för att anfalla draken!</strong>]",
    "statistics.perSec": "/sek",
    "statistics.generationSection": "Produktion",
    "statistics.critSection": "Särskilt",
    "statistics.dps": "Truppernas skada: <strong>{{dps}}/sek</strong>",
    "statistics.gps": "Truppernas guld: <strong>{{gps}}/sek</strong>",
    "statistics.dpc": "Skada per klick: <strong>{{dpc}}/klick</strong>",
    "statistics.gpc": "Guld per klick: <strong>{{gpc}}/klick</strong>",
    "statistics.catapultDamage": "Skada: <strong>{{damage}}/skott</strong>",
    "statistics.catapultTimeToShoot": "Till nästa skott: <strong>{{time}} sek</strong>",
    "statistics.undo.disabledLine": "Klicka inom 10 sekunder för att ångra ett felköp och få tillbaka guldet.",
    "statistics.undo.enabledAction": "Klicka för att ångra köpet av {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Du får tillbaka {{refund}}.",
    "statistics.undo.enabledTimer": "{{seconds}} sekunder kvar.",
    "statistics.undo.refundGold": "{{amount}} guld",
})

for base, one, many in [
    ("seconds", "sekund", "sekunder"), ("minutes", "minut", "minuter"),
    ("hours", "timme", "timmar"), ("days", "dag", "dagar"),
    ("months", "månad", "månader"), ("years", "år", "år"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_other"] = many

T.update({
    "generators.generators": "Trupper",
    "generators.buy": "köp {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} sek",
    "generators.ngPlusProductionToggle": "Slå på eller av produktion",
    "generators.tabs.troops": "Trupper",
    "generators.tabs.support": "Stöd",
    "generators.fireUnitsButton.tooltip": "Avskeda trupper för att dra ner på resurserna"
        " och ändå behålla en del av produktionen.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Den magiska kraft som driver trollkarlarnas anfall.",
    "generators.emptyManaDescription": "Köp \"Manaflöde\" för att anfalla igen.",
    "generators.inspiration": "Inspiration",
    "generators.inspirationDescription": "När den är igång mångdubblas alla hjältars styrka.",
    "generators.tabsAriaLabel": "truppflikar",
})

UNITS = {
    "warrior": ("Krigare", "Krigare"),
    "wizard": ("Trollkarl", "Trollkarlar"),
    "elf": ("Alv", "Alver"),
    "garrison": ("Garnison", "Garnisoner"),
    "academy": ("Magiakademi", "Magiakademier"),
    "academy_short": ("Akademi", "Akademier"),
    "outpost": ("Bågskytteutpost", "Bågskytteutposter"),
    "outpost_short": ("Utpost", "Utposter"),
    "council": ("Krigsråd", "Krigsråd"),
    "nexus": ("Ärkemagikernas nav", "Ärkemagikernas nav"),
    "forest": ("Uråldrig skog", "Uråldriga skogar"),
    "thief": ("Tjuv", "Tjuvar"),
    "bard": ("Barder", "Barder"),
    "cleric": ("Präst", "Präster"),
    "guild": ("Tjuvgille", "Tjuvgillen"),
    "guild_short": ("Gille", "Gillen"),
    "troupe": ("Gycklartrupp", "Gycklartrupper"),
    "troupe_short": ("Trupp", "Trupper"),
    "seminary": ("Heligt seminarium", "Heliga seminarier"),
    "seminary_short": ("Seminarium", "Seminarier"),
    "congress": ("Skuggkonvent", "Skuggkonvent"),
    "theater": ("Stor teater", "Stora teatrar"),
    "college": ("Kardinalskollegium", "Kardinalskollegier"),
    "catapult": ("Katapult", "Katapulter"),
    "builder": ("Byggare", "Byggare"),
    "engineer": ("Ingenjör", "Ingenjörer"),
    "farmer": ("Bonde", "Bönder"),
    "lumberjack": ("Skogshuggare", "Skogshuggare"),
    "miner": ("Gruvarbetare", "Gruvarbetare"),
    "apprenticeships": ("Lärlingsplats", "Lärlingsplatser"),
    "tradespeople": ("Hantverkare", "Hantverkare"),
}
for base, (one, many) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_other"] = many

T.update({
    "generators.unitDescription.warrior": "Tåliga närstridskämpar.",
    "generators.unitDescription.wizard": "Slår på medeldistans, men tål inget.",
    "generators.unitDescription.elf": "Skjuter smidigt på långt håll, utom räckhåll för draken.",
    "generators.unitDescription.garrison": "Befäst bas som värvar krigare.",
    "generators.unitDescription.outpost": "Avlägsen bas som värvar alver.",
    "generators.unitDescription.academy": "Skola som utbildar trollkarlar för strid.",
    "generators.unitDescription.council": "Militär organisation som upprättar garnisoner.",
    "generators.unitDescription.nexus": "Mystisk organisation som upprättar akademier.",
    "generators.unitDescription.forest": "Helig skog som upprättar utposter.",
    "generators.unitDescription.thief": "Slug: förgiftar draken och stjäl dess guld.",
    "generators.unitDescription.bard": "Kan inspirera trupperna att slåss hårdare.",
    "generators.unitDescription.cleric": "Beskyddar och värvar nya hjältar till striden.",
    "generators.unitDescription.guild": "Undre nätverk som värvar tjuvar.",
    "generators.unitDescription.troupe": "Kringresande sällskap som värvar barder.",
    "generators.unitDescription.seminary": "Helig inrättning som utbildar präster.",
    "generators.unitDescription.congress": "Organisation i skuggorna som upprättar tjuvgillen.",
    "generators.unitDescription.theater": "Väldig inrättning som upprättar gycklartrupper.",
    "generators.unitDescription.college": "Religiös organisation som upprättar seminarier.",
    "generators.unitDescription.catapult": "Belägringsvapen som gör stor skada på draken.",
    "generators.unitDescription.builder": "Bygger byggnader på nivå 2.",
    "generators.unitDescription.engineer": "Upprättar organisationer på nivå 3.",
    "generators.unitDescription.farmer": "Odlar mat åt kungariket.",
    "generators.unitDescription.lumberjack": "Fäller trä till bygget.",
    "generators.unitDescription.miner": "Bryter malm i bergen.",
    "generators.unitDescription.apprenticeships": "Utbildar hantverkare.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} skada/{{rate}} sek",
    "wizard": "{{generatorGeneration}} skada/{{rate}} sek",
    "elf": "{{generatorGeneration}} skada/{{rate}} sek",
    "catapult": "{{generatorGeneration}} skada/{{rate}} sek",
    "thief": "+{{generatorGeneration}} guld/{{rate}} sek",
    "bard": "+{{generatorGeneration}} inspiration/{{rate}} sek",
    "cleric": "+{{generatorGeneration}} hjältar/{{rate}} sek",
    "builder": "+{{generatorGeneration}} byggnader/{{rate}} sek",
    "engineer": "+{{generatorGeneration}} organisationer/{{rate}} sek",
    "farmer": "+{{generatorGeneration}} mat/{{rate}} sek",
    "lumberjack": "+{{generatorGeneration}} trä/{{rate}} sek",
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
    "settings.settings": "Inställningar",
    "settings.buy_max": "Köp max",
    "settings.audio": "Musik och ljud",
    "settings.game": "Spel",
    "settings.graphics": "Grafik",
    "settings.offline_progress": "Framsteg offline",
    "settings.wishlist_now": "Lägg till i önskelistan",
    "menus.settings": "Inställningar",
    "menus.tabs.game": "Spel",
    "menus.tabs.graphics": "Grafik",
    "menus.tabs.audio": "Ljud",
    "menus.tabs.levels": "Kapitel",
    "menus.tabs.credits": "Medverkande",
    "menus.credits.title": "Medverkande",
    "menus.credits.developedBy": "Utvecklat av",
    "menus.credits.developedWith": "Utvecklat med",
    "menus.credits.bigThanksTo": "Ett stort tack till",
    "menus.credits.theRestOfTheDiscordServer": "alla andra på Discord-servern",
    "menus.credits.andYou": "och dig!",
    "menus.music": "Musik",
    "menus.sfx": "Ljudeffekter",
    "menus.audioSettings": "Ljudinställningar",
    "menus.gameSettings": "Spelinställningar",
    "menus.graphicsSettings": "Grafikinställningar",
    "menus.language": "Språk",
    "menus.languages.en": "Engelska",
    "menus.languages.fr": "Franska",
    "menus.languages.de": "Tyska",
    "menus.languages.pt": "Portugisiska",
    "menus.languages.tr": "Turkiska",
    "menus.shakeIntensity": "Skakning",
    "menus.largerTextSize": "Större text",
    "menus.crtFilter": "CRT-filter",
    "menus.chromaticAberrationSlider": "Färgspridning",
    "menus.chromaticAberration": "Färgspridning",
    "menus.swordSwooshSounds": "Svärds- och kritiska ljud",
    "menus.catSounds": "Kattljud",
    "menus.fullscreen": "Helskärm",
    "menus.resume": "Fortsätt spela",
    "menus.close": "Stäng",
    "menus.quitGame": "Avsluta spelet",
    "menus.joinDiscord": "Gå med i Discord",
    "menus.clear_save_label": "Radera dina framsteg?",
    "menus.zoom_adjustment": "Gränssnittets zoom",
    "menus.clear_save": "Radera nu",
    "menus.are_you_sure": "Är du säker?",
    "menus.cannot_be_reversed": "Det här går inte att ångra.",
    "menus.yes": "Ja",
    "menus.no": "Nej",
})

T.update({
    "tooltip.inspiration": "Inspiration",
    "tooltip.inspirationDescription": "När den är igång mångdubblas alla hjältars styrka.",
    "tooltip.maxInspiration": "Högsta multiplikator",
    "tooltip.maxInspirationMultiplier": "Högsta multiplikator",
    "tooltip.statisticsDescription": "Utförlig statistik om dina framsteg och striden.",
    "tooltip.hudStopBird": "Stoppa fågeln",
    "tooltip.hudLifetimeStats": "Total statistik",
    "tooltip.hudHideWindows": "Dölj fönster",
    "tooltip.events.roar": "Bedövande vrål",
    "tooltip.events.fire": "Eldsprutning",
    "tooltip.events.claw": "Klohugg",
    "tooltip.events.dialog": "Särskild händelse",
    "tooltip.events.pope_visit": "Ett särskilt besök",
    "tooltip.events.dungeon_keys": "En mörk hemlighet",
    "tooltip.events.missing_king": "Var är kungen?",
    "tooltip.events.catapult": "En teknisk prototyp",
    "tooltip.events.engineer": "Hjälp i rättan tid",
    "tooltip.events.invasion_start": "En invasion är på väg",
    "tooltip.events.invasion_end": "Bud från trupperna",
    "tooltip.events.apprenticeships_unlock": "Lärlingsplatser upplåsta",
    "tooltip.events.trading": "En kringresande handelsman",
    "tooltip.events.dummy_toy_reveal": "Inte vad jag trodde",
})

T.update({
    "infos.banner.events": "Händelser",
    "infos.banner.stats": "Statistik",
    "infos.banner.engineering": "Teknik",
    "infos.banner.resources": "Resurser",
    "infos.tabs.events": "Händelser",
    "infos.tabs.stats": "Statistik",
    "infos.tabs.engineering": "Teknik",
    "infos.tabs.resources": "Resurser",
    "infos.tabsAriaLabel": "informationsflikar",
    "game.dummy": "Den stora trädockan",
    "game.infiniteBird": "Fågeln som inte går att fälla",
    "game.king": "Kungen",
    "game.smallDragon": "Tuth'orieth, den grodde",
    "game.bigDragon": "Forth'aarh, som ger och tar liv",
    "dungeon.found": "Hittat",
    "dungeon.giveUp": "Ge upp",
    "dungeon.tooltipDescription": "Utforska fängelsehålan (nivå {{level}})",
    "dungeon.cooldownMessage": "Fängelsehålan vilar. Vänta {{seconds}} sekunder på att gå in igen.",
    "dungeon.cooldownShort": "{{seconds}} sek",
    "dungeon.levelLabel": "Nivå",
    "dungeon.levelShort": "Nivå {{level}}",
    "dungeon.keysOwned": "Nycklar",
    "dungeon.giveUpTooltip": "Lämna fängelsehålan (behåll en del av bytet med Frikostigt byte)",
    "dungeon.moveHint": "WASD eller piltangenter för att gå",
    "dungeon.attackHint": "Klicka på monster för att anfalla",
    "dungeon.chestCountsTooltip": "{{opened}} av {{total}} kistor öppnade",
    "dungeon.exitDirection": "UTGÅNG",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Lyckad expedition",
    "summaries.dungeonLoot.titleFailed": "Misslyckad expedition",
    "summaries.dungeonLoot.titleStuckRescue": "Räddad ut",
    "summaries.dungeonLoot.lootSummarySubtitle": "Sammanställning av bytet",
    "summaries.dungeonLoot.body_one": "Fick {{gold}} guld och {{grayKeys}} nyckel",
    "summaries.dungeonLoot.body_other": "Fick {{gold}} guld och {{grayKeys}} nycklar",
    "summaries.dungeonLoot.artifactFound": "Hittade {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Förluster till eldsprutningen",
    "summaries.fireBreathCasualties.body": "Förlorade {{list}}",
    "summaries.fireBreathCasualties.none": "Inga förluster",
    "summaries.fireBreathBlocked.title": "Eldsprutningen stoppades!",
    "summaries.fireBreathBlocked.body": "En rökbomb räddade dina trupper.",
    "summaries.toastLabel": "Spelmeddelande",
})

T.update({
    "levels.title": "Kapitel",
    "levels.locked": "Låst",
    "levels.active": "Pågår",
    "levels.completed": "Klarat",
    "levels.continue": "Fortsätt",
    "levels.start": "Börja",
    "levels.restart": "Spela om",
    "levels.restart_progress_warning": "Spela om nu? Du förlorar osparade framsteg i det här kapitlet.",
    "levels.names.mainGame": "En stor drake",
    "levels.names.newGamePlus": "Resurshantering",
    "levels.names.dummy": "En magisk leksak",
    "levels.names.infinite": "Verkligen oändligt",
    "levels.names.kingBattle": "Kungens sista strid",
})

T.update({
    "menus.tabs.saveData": "Sparade data",
    "menus.saveData.title": "Sparade data",
    "menus.saveData.clearChapterTitle": "Kapitlens framsteg",
    "menus.saveData.clearChapterExplanation": "Raderar guld, trupper, uppgraderingar,"
        " framsteg i fängelsehålan och klaratmärken för varje kapitel. Upplåsta kapitel,"
        " total statistik, inställningar och artefakter behålls.",
    "menus.saveData.clearChapterButton": "Radera kapitlens framsteg",
    "menus.saveData.clearFullTitle": "Alla sparade data",
    "menus.saveData.clearFullExplanation": "Raderar allt som kapitelåterställningen gör,"
        " och dessutom artefakter, upplåsta kapitel och total statistik. Inställningar för"
        " ljud, grafik och språk behålls.",
    "menus.saveData.clearFullButton": "Radera alla sparade data",
    "menus.saveData.clearFullWarning": "Det går inte att ångra. Du förlorar artefakter,"
        " upplåsta kapitel och total statistik.",
})

T.update({
    "artifacts.title": "Artefakter",
    "artifacts.subtitle": "Sällsynta artefakter dyker ibland upp i särskilda kistor i"
        " fängelsehålan. De följer med mellan kapitlen.",
    "artifacts.notYetFound": "(inte hittad än)",
})

ART = {
    "phoenixWhistle": ("Fenixvisslan", "En särskild fågel bär med sig ett nytt slags mynt."),
    "emberforgedShield": ("Glödsmidd sköld", "Krigare tar ingen skada av drakeld."),
    "moonwellFlask": ("Månbrunnsflaska", "Trollkarlar förbrukar bara hälften så mycket mana."),
    "windstepAnklet": ("Vindstegets ankelring", "Alver blir inte bedövade."),
    "fangSatchel": ("Huggtandsväska", "Medan omgången pågår gör tjuvar en draktand var trettionde minut."),
    "slumberBerries": ("Sömnbär", "Giftet fördröjer drakens vrål och eld med 10 sekunder."),
    "echoingLute": ("Ekande luta", "Barder ger dubbel inspirationsbelöning."),
    "blessingCenser": ("Välsignelsens rökelsekar", "Präster värvar alltid dubbelt så många."),
    "victoryTusk": ("Segerbetan", "En klarad nivå ger dubbelt så många draktänder."),
    "cartographersLedger": ("Kartritarens bok", "Visar hur många av fängelsehålans kistor som är öppnade."),
    "ironSkeletonKey": ("Dyrk av järn", "Låser upp fängelsehålan till nivå 20."),
    "everflameLantern": ("Evigflammans lykta", "Facklan slocknar aldrig."),
    "midasCoin": ("Midasmyntet", "Dubbelt så mycket guld i fängelsehålan."),
    "harvestIdol": ("Skördeguden", "Resursproduktionen ökar med 25 %."),
    "titanGauntlet": ("Titanhandsken", "Tio gånger så mycket skada per klick."),
    "wayfindersCompass": ("Vägvisarens kompass", "Pekar mot fängelsehålans utgång."),
    "loadedDice": ("Riggade tärningar", "Varje klick blir kritiskt."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Järnfinger", "+{{bonus}} skada per klick"),
    "featherFinger": ("Fjäderfinger", "+{{bonus}} klick per sekund"),
    "wakeupCall": ("Väckning", "Varje klick kortar bedövningen med {{bonus}} sekunder"),
    "electricalFinger": ("Elektriskt finger", "Varje klick har {{bonus}} % chans att kalla på blixten."),
    "perfectClick": ("Perfekt klick", "+{{bonus}} % chans till kritiskt klick"),
    "criticalStrike": ("Kritiskt slag", "+{{bonus}}x skada på kritiska klick"),
    "goldenExplosion": ("Gyllene explosion", "{{bonus}}x belöning när du klickar på fåglar"),
    "naturalLeader": ("Född ledare", "Klick fyller inspirationsmätaren med +{{bonus}}/klick"),
    "moneyCursor": ("Guldmarkör", "{{bonus}}x guld per klick"),
    "fullChests": ("Fulla kistor", "{{bonus}} % mindre chans att en kista i fängelsehålan är tom"),
    "carpalCure": ("Handledskur", "Håll ner musknappen för att anfalla draken utan uppehåll."),
    "shortSword": ("Kortsvärd", "+{{bonus}}x skademultiplikator för {{type}}"),
    "longSword": ("Långsvärd", "+{{bonus}}x skademultiplikator till för krigare"),
    "twoHandedSword": ("Tvåhandssvärd", "Ytterligare +{{bonus}}x skademultiplikator för krigare"),
    "battleShout": ("Stridsrop", "Fyller inspirationsmätaren med +{{bonus}} per slag"),
    "warCry": ("Krigsrop", "Utlöser inspirationen automatiskt vid nästa tick när multiplikatorn är på max"),
    "barbarian": ("Barbar", "+{{bonus}} grundskada"),
    "thickArmor": ("Tjock rustning", "{{bonus}} % mindre fysisk skada"),
    "fireArmor": ("Eldrustning", "{{bonus}} % färre trupper dör av eldsprutningen"),
    "heavyRocks": ("Tunga stenar", "+{{bonus}} % katapultskada per nivå"),
    "silverBlade": ("Silverklinga", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenBlade": ("Gyllene klinga", "Ytterligare +{{bonus}}x multiplikator på guld per slag"),
    "loyalMercenaries": ("Trogna legosoldater", "{{typePlural}} du köper gör +{{bonus}}x skada per nivå"),
    "loyalServants": ("Trogna tjänare", "{{bonus}} % billigare att värva {{type}} och allt över"),
    "teamWork": ("Samarbete", "Värvar ytterligare {{typePlural}} för varje {{type}} du köper"),
    "dungeonPrecision": ("Precision i djupet", "+{{bonus}} % chans till kritisk träff i fängelsehålan"),
    "mazeCrusher": ("Labyrintkrossaren", "+{{bonus}} kritisk skada i fängelsehålan"),
    "magicMissile": ("Magisk projektil", "+{{bonus}}x skademultiplikator för {{type}}"),
    "manaSword": ("Manasvärd", "Varje trollkarl fyller en krigares svärd med mana."
                  " +{{bonus}}x skademultiplikator när manan är över 90"),
    "magicMouse": ("Magisk mus", "Fyller manamätaren med +{{bonus}} per klick"),
    "manaSurge": ("Manaflöde", "Fyller trollkarlarnas manamätare"),
    "manaPool": ("Manakälla", "+{{bonus}} % högsta mana"),
    "manaBoost": ("Manastöt", "Trollkarlarnas skada fördubblas när manan är över {{current}}"),
    "weatherForecast": ("Väderprognos", "+{{bonus}} % chans till blixtnedslag"),
    "lightningStrike": ("Blixtnedslag", "Lägger till en blixt som gör +{{bonus}}x skada"
                        " av {{type}} för varje köpt uppgradering"),
    "silverStaff": ("Silverstav", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenStaff": ("Gyllene stav", "Ytterligare +{{bonus}}x multiplikator på guld per slag"),
    "magicFire": ("Magisk eld", "Facklan brinner +{{bonus}} sekunder längre"),
    "archimage": ("Ärkemagiker", "+{{bonus}} grundskada"),
    "huntersEye": ("Jägarens öga", "+{{bonus}} % chans att träffa en fågel inom räckhåll varje tick"),
    "criticalChance": ("Skarpt sikte", "+{{bonus}} % chans till kritiskt skott"),
    "criticalDamage": ("Lövskäraren", "+{{bonus}}x skada på kritiska skott"),
    "huntingSeason": ("Jaktsäsong", "Kallar genast fram en flock fåglar"),
    "elvenEyes": ("Alvögon", "Du ser i mörkret +{{bonus}} sekunder efter att facklan slocknat"),
    "multipleShot": ("Flera pilar", "Skjuter en pil till per nivå"),
    "silverArrow": ("Silverpil", "+{{bonus}}x multiplikator på guld per slag"),
    "goldenArrow": ("Gyllene pil", "Ytterligare +{{bonus}}x multiplikator på guld per slag"),
    "iceArrow": ("Ispil", "Fördröjer drakens eld med {{bonus}} sekunder"),
    "animalInstinct": ("Djurinstinkt", "Katapulten skjuter katter i stället för stenar,"
                       " och tigrar i stället för katter, tio gånger skadan varje gång."),
    "lightningRod": ("Åskledare", "{{bonus}} % chans att dra till sig en blixt till när"
                     " trollkarlarnas blixt träffar."),
    "recycledArrows": ("Återvunna pilar", "Alvernas anfall kostar mindre trä"),
    "lightfoot": ("Lätt på foten", "+{{bonus}} % snabbare att gå och vända i fängelsehålan"),
    "fastHands": ("Snabba händer", "Kortar tiden att göra guld med {{bonus}} sekunder"),
    "sharpDagger": ("Lönnmördarklinga", "Tjuvar anfaller också, med {{current}} i skada"),
    "poisonDagger": ("Förgiftad dolk", "+{{bonus}} % chans att förgifta draken"),
    "blackMamba": ("Svart mamba", "+{{bonus}}x giftskada av tjuvarnas skada"),
    "lingeringToxin": ("Dröjande gift", "Giftet varar +{{bonus}} sekunder längre"),
    "smokeBomb": ("Rökbomb", "Lägger en fälla för draken med {{current}} % chans att"
                  " utlösas vid nästa slag och stoppa det."),
    "catBomb": ("Kattbomb", "Katapultens ammunition exploderar vid träff, dubbel skada."),
    "pickpocket": ("Ficktjuv", "+{{bonus}}x multiplikator på guldet {{type}} gör"),
    "lockPick": ("Dyrk", "Varje expedition börjar med {{bonus}} dörrar redan olåsta."),
    "midasTouch": ("Midas beröring", "Ytterligare +{{bonus}}x multiplikator på guldet {{type}} gör"),
    "stuffedChests": ("Proppfulla kistor", "+{{bonus}} % guld ur fängelsehålans kistor"),
    "tuningFork": ("Stämgaffel", "+{{bonus}} inspiration samlas"),
    "luteSolo": ("Lutsolo", "+{{bonus}}x högsta inspirationsmultiplikator"),
    "obnoxiousGuitarist": ("Odräglig gitarrist", "Inspirationen varar +{{bonus}} sekunder"),
    "piercedEardrums": ("Spräckta trumhinnor", "Drakens vrålräknare går {{bonus}} % långsammare"),
    "replay": ("Extranummer", "{{bonus}} % chans att inspirationen börjar om när den tar slut"),
    "sonicBarrier": ("Ljudbarriär", "Drakens eldräknare går {{bonus}} % långsammare"),
    "cacofonix": ("Kakofonix", "Bedövar dina egna trupper när du köper den"),
    "churchChoir": ("Kyrkokör", "Värvar 1 seminarium varje gång inspirationen utlöses"),
    "encore": ("Extranummer igen", "Kortar inspirationens vila med {{bonus}} sekunder"),
    "lockerRoomSpeech": ("Tal i omklädningsrummet", "Gör inspiration medan spelet är stängt,"
                         " i {{current}} % av takten"),
    "orderInTheUk": ("Ordning i kungariket", "När spelet är stängt får din musik hantverkarna"
                     " att jobba över och göra resurser i {{current}} % av vanlig takt"),
    "majorKey": ("Durtonart", "Köper en nyckel till fängelsehålan. (Ja, ordvitsen är usel.)"),
    "vulnerableFrequencies": ("Sårbara frekvenser", "Fienderna i fängelsehålan är odödliga"
                              " {{bonus}} millisekunder kortare efter varje slag"),
    "heroResources": ("Hjältepersonalen", "+{{bonus}} % chans att värva dubbelt så många hjältar"),
    "blessedAura": ("Välsignad aura", "{{bonus}} % färre trupper dör av eldsprutningen"),
    "blessedBird": ("Välsignad fågel", "{{current}} % chans att en fågel kommer välsignad"
                    " och ger dubbelt guld"),
    "powerTransfer": ("Kraftöverföring", "Vid varje värvning fyller trollkarlarnas mana på med"
                      " 0,5 för varje präst du har"),
    "generousLoot": ("Frikostigt byte", "När en expedition misslyckas behåller du ändå"
                     " {{current}} % av bytet."),
    "divineLight": ("Gudomligt ljus", "+{{bonus}} % chans att tända en slocknad fackla igen"),
    "recruitWarriors": ("Värva krigare", "Låter dig värva krigare till striden"),
    "recruitElves": ("Värva alver", "Låter dig värva alver till striden"),
    "recruitWizards": ("Värva trollkarlar", "Låter dig värva trollkarlar till striden"),
    "recruitBards": ("Värva barder", "Låter dig värva barder till striden"),
    "recruitThieves": ("Värva tjuvar", "Låter dig värva tjuvar till striden"),
    "recruitClerics": ("Värva präster", "Låter dig värva präster till striden"),
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
    "huntingSeason.suffix": " fåglar",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

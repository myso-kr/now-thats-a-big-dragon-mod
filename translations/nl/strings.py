# -*- coding: utf-8 -*-
"""The Dutch UI strings.

Address: "je" throughout, which is what Dutch games and Dutch software use. "u" would
put the King at a formal distance the English does not have; he is grand in tone, not
in pronoun.

Dutch has two genders and the article follows the noun - "de upgrade" but "het leger" -
so a noun and its article are written together wherever one appears.

The IJ digraph has a single code point of its own, and no pixel font here carries it.
It is written as two letters, which is what Dutch does in practice anyway.

The game's own font draws every letter Dutch needs, so nothing of ours ships for it.
"""

T = {}

T.update({
    "upgrades.upgrades": "Upgrades",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Volgend niveau",
    "upgrades.currentLevel": "Huidig",
    "upgrades.newGamePlusOnly": "Alleen in het hoofdstuk \"Grondstoffenbeheer\"",
    "upgrades.max": "Max",
    "upgrades.lockedMessage": "Upgrade {{parentSkill}} verder om deze vrij te spelen",
    "common.wishlistNow": "Zet op je verlanglijst!",
})

T.update({
    "statistics.section.ttb": "Gevechtstijd",
    "statistics.section.dgps": "Schade en goud per seconde",
    "statistics.section.resourceBalance": "Grondstoffenbalans",
    "statistics.lifetime.title": "Totale statistieken",
    "statistics.lifetime.totalPlaytime": "Totale speeltijd",
    "statistics.lifetime.totalGoldEarned": "Goud verdiend",
    "statistics.lifetime.totalGoldSpent": "Goud uitgegeven",
    "statistics.lifetime.totalBirdsKilled": "Vogels neergehaald",
    "statistics.lifetime.totalClicks": "Kliks",
    "statistics.lifetime.totalHeroesRecruited": "Helden geworven",
    "statistics.lifetime.heroesPurchased": "Gekocht",
    "statistics.lifetime.heroesRecruited": "Geworven",
    "statistics.lifetime.tier1": "Rang 1 geworven (gekocht)",
    "statistics.lifetime.tier2": "Rang 2 geworven (gekocht)",
    "statistics.lifetime.tier3": "Rang 3 geworven (gekocht)",
    "statistics.lifetime.totalDamageDealt": "Schade toegebracht",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Verloren aan vuuradem",
    "statistics.battleDuration": "Verstreken: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Valt dit wel te winnen?",
    "statistics.infiniteEstimatedVictory": "Echt winnen kan niet!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Je bent onze held!</strong>];"
        " (0-1000000000)[Overwinning over <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Klik of druk op Z om de draak aan te vallen!</strong>]",
    "statistics.perSec": "/sec",
    "statistics.generationSection": "Productie",
    "statistics.critSection": "Bijzonder",
    "statistics.dps": "Schade van je troepen: <strong>{{dps}}/sec</strong>",
    "statistics.gps": "Goud van je troepen: <strong>{{gps}}/sec</strong>",
    "statistics.dpc": "Schade per klik: <strong>{{dpc}}/klik</strong>",
    "statistics.gpc": "Goud per klik: <strong>{{gpc}}/klik</strong>",
    "statistics.catapultDamage": "Schade: <strong>{{damage}}/schot</strong>",
    "statistics.catapultTimeToShoot": "Tot het volgende schot: <strong>{{time}} sec</strong>",
    "statistics.undo.disabledLine": "Klik binnen 10 seconden om een miskoop terug te draaien"
        " en je goud terug te krijgen.",
    "statistics.undo.enabledAction": "Klik om de aankoop van {{count}} {{generator}} terug te draaien.",
    "statistics.undo.enabledRefund": "Je krijgt {{refund}} terug.",
    "statistics.undo.enabledTimer": "Nog {{seconds}} seconden.",
    "statistics.undo.refundGold": "{{amount}} goud",
})

for base, one, many in [
    ("seconds", "seconde", "seconden"), ("minutes", "minuut", "minuten"),
    ("hours", "uur", "uur"), ("days", "dag", "dagen"),
    ("months", "maand", "maanden"), ("years", "jaar", "jaar"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_other"] = many

T.update({
    "generators.generators": "Troepen",
    "generators.buy": "koop {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} sec",
    "generators.ngPlusProductionToggle": "Productie aan of uit",
    "generators.tabs.troops": "Troepen",
    "generators.tabs.support": "Steun",
    "generators.fireUnitsButton.tooltip": "Ontsla troepen om minder grondstoffen te"
        " verbruiken en toch een deel van de productie te houden.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "De magische kracht achter de aanvallen van je tovenaars.",
    "generators.emptyManaDescription": "Koop \"Manastroom\" om weer aan te vallen.",
    "generators.inspiration": "Inspiratie",
    "generators.inspirationDescription": "Zodra ze werkt, wordt de kracht van al je helden vermenigvuldigd.",
    "generators.tabsAriaLabel": "troepentabbladen",
})

UNITS = {
    "warrior": ("Krijger", "Krijgers"),
    "wizard": ("Tovenaar", "Tovenaars"),
    "elf": ("Elf", "Elfen"),
    "garrison": ("Garnizoen", "Garnizoenen"),
    "academy": ("Magieacademie", "Magieacademies"),
    "academy_short": ("Academie", "Academies"),
    "outpost": ("Boogschuttersvoorpost", "Boogschuttersvoorposten"),
    "outpost_short": ("Voorpost", "Voorposten"),
    "council": ("Krijgsraad", "Krijgsraden"),
    "nexus": ("Knooppunt der aartsmagiërs", "Knooppunten der aartsmagiërs"),
    "forest": ("Eeuwenoud woud", "Eeuwenoude wouden"),
    "thief": ("Dief", "Dieven"),
    "bard": ("Bard", "Barden"),
    "cleric": ("Priester", "Priesters"),
    "guild": ("Dievengilde", "Dievengilden"),
    "guild_short": ("Gilde", "Gilden"),
    "troupe": ("Troubadoursgezelschap", "Troubadoursgezelschappen"),
    "troupe_short": ("Gezelschap", "Gezelschappen"),
    "seminary": ("Heilig seminarie", "Heilige seminaries"),
    "seminary_short": ("Seminarie", "Seminaries"),
    "congress": ("Schaduwconvent", "Schaduwconventen"),
    "theater": ("Groot theater", "Grote theaters"),
    "college": ("Kardinaalscollege", "Kardinaalscolleges"),
    "catapult": ("Katapult", "Katapulten"),
    "builder": ("Bouwer", "Bouwers"),
    "engineer": ("Ingenieur", "Ingenieurs"),
    "farmer": ("Boer", "Boeren"),
    "lumberjack": ("Houthakker", "Houthakkers"),
    "miner": ("Mijnwerker", "Mijnwerkers"),
    "apprenticeships": ("Leerplaats", "Leerplaatsen"),
    "tradespeople": ("Ambachtslieden", "Ambachtslieden"),
}
for base, (one, many) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_other"] = many

T.update({
    "generators.unitDescription.warrior": "Taaie vechters van dichtbij.",
    "generators.unitDescription.wizard": "Slaan toe op halve afstand, maar zijn kwetsbaar.",
    "generators.unitDescription.elf": "Schieten wendbaar van ver, buiten bereik van de draak.",
    "generators.unitDescription.garrison": "Versterkte basis die krijgers werft.",
    "generators.unitDescription.outpost": "Afgelegen basis die elfen werft.",
    "generators.unitDescription.academy": "School die tovenaars voor de strijd opleidt.",
    "generators.unitDescription.council": "Militaire organisatie die garnizoenen sticht.",
    "generators.unitDescription.nexus": "Mystieke organisatie die academies sticht.",
    "generators.unitDescription.forest": "Heilig woud dat voorposten sticht.",
    "generators.unitDescription.thief": "Sluw: vergiftigt de draak en steelt zijn goud.",
    "generators.unitDescription.bard": "Kan je troepen inspireren om harder te vechten.",
    "generators.unitDescription.cleric": "Beschermt en werft nieuwe helden voor de strijd.",
    "generators.unitDescription.guild": "Ondergronds netwerk dat dieven werft.",
    "generators.unitDescription.troupe": "Rondtrekkend gezelschap dat barden werft.",
    "generators.unitDescription.seminary": "Heilige instelling die priesters opleidt.",
    "generators.unitDescription.congress": "Organisatie in de schaduw die dievengilden sticht.",
    "generators.unitDescription.theater": "Machtige instelling die gezelschappen sticht.",
    "generators.unitDescription.college": "Religieuze organisatie die seminaries sticht.",
    "generators.unitDescription.catapult": "Belegeringswapen dat de draak zwaar raakt.",
    "generators.unitDescription.builder": "Bouwt gebouwen van het tweede niveau.",
    "generators.unitDescription.engineer": "Sticht organisaties van het derde niveau.",
    "generators.unitDescription.farmer": "Verbouwt voedsel voor het koninkrijk.",
    "generators.unitDescription.lumberjack": "Hakt hout om te bouwen.",
    "generators.unitDescription.miner": "Delft erts in de bergen.",
    "generators.unitDescription.apprenticeships": "Leidt ambachtslieden op.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} schade/{{rate}} sec",
    "wizard": "{{generatorGeneration}} schade/{{rate}} sec",
    "elf": "{{generatorGeneration}} schade/{{rate}} sec",
    "catapult": "{{generatorGeneration}} schade/{{rate}} sec",
    "thief": "+{{generatorGeneration}} goud/{{rate}} sec",
    "bard": "+{{generatorGeneration}} inspiratie/{{rate}} sec",
    "cleric": "+{{generatorGeneration}} helden/{{rate}} sec",
    "builder": "+{{generatorGeneration}} gebouwen/{{rate}} sec",
    "engineer": "+{{generatorGeneration}} organisaties/{{rate}} sec",
    "farmer": "+{{generatorGeneration}} voedsel/{{rate}} sec",
    "lumberjack": "+{{generatorGeneration}} hout/{{rate}} sec",
    "miner": "+{{generatorGeneration}} erts/{{rate}} sec",
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
        "+{{generatorGeneration}} $t(" + ref + ', {"count": {{generatorGeneration}} })/{{rate}} sec')

T.update({
    "settings.settings": "Instellingen",
    "settings.buy_max": "Koop max",
    "settings.audio": "Muziek en geluid",
    "settings.game": "Spel",
    "settings.graphics": "Beeld",
    "settings.offline_progress": "Voortgang offline",
    "settings.wishlist_now": "Zet op je verlanglijst",
    "menus.settings": "Instellingen",
    "menus.tabs.game": "Spel",
    "menus.tabs.graphics": "Beeld",
    "menus.tabs.audio": "Geluid",
    "menus.tabs.levels": "Hoofdstukken",
    "menus.tabs.credits": "Met dank aan",
    "menus.credits.title": "Met dank aan",
    "menus.credits.developedBy": "Gemaakt door",
    "menus.credits.developedWith": "Gemaakt met",
    "menus.credits.bigThanksTo": "Veel dank aan",
    "menus.credits.theRestOfTheDiscordServer": "iedereen op de Discord-server",
    "menus.credits.andYou": "en jou!",
    "menus.music": "Muziek",
    "menus.sfx": "Geluidseffecten",
    "menus.audioSettings": "Geluidsinstellingen",
    "menus.gameSettings": "Spelinstellingen",
    "menus.graphicsSettings": "Beeldinstellingen",
    "menus.language": "Taal",
    "menus.languages.en": "Engels",
    "menus.languages.fr": "Frans",
    "menus.languages.de": "Duits",
    "menus.languages.pt": "Portugees",
    "menus.languages.tr": "Turks",
    "menus.shakeIntensity": "Schudden",
    "menus.largerTextSize": "Grotere tekst",
    "menus.crtFilter": "CRT-filter",
    "menus.chromaticAberrationSlider": "Kleurschifting",
    "menus.chromaticAberration": "Kleurschifting",
    "menus.swordSwooshSounds": "Zwaard- en kritieke geluiden",
    "menus.catSounds": "Kattengeluiden",
    "menus.fullscreen": "Volledig scherm",
    "menus.resume": "Verder spelen",
    "menus.close": "Sluiten",
    "menus.quitGame": "Spel afsluiten",
    "menus.joinDiscord": "Kom op Discord",
    "menus.clear_save_label": "Je voortgang wissen?",
    "menus.zoom_adjustment": "Zoom van het scherm",
    "menus.clear_save": "Nu wissen",
    "menus.are_you_sure": "Weet je het zeker?",
    "menus.cannot_be_reversed": "Dit kun je niet terugdraaien.",
    "menus.yes": "Ja",
    "menus.no": "Nee",
})

T.update({
    "tooltip.inspiration": "Inspiratie",
    "tooltip.inspirationDescription": "Zodra ze werkt, wordt de kracht van al je helden vermenigvuldigd.",
    "tooltip.maxInspiration": "Hoogste vermenigvuldiger",
    "tooltip.maxInspirationMultiplier": "Hoogste vermenigvuldiger",
    "tooltip.statisticsDescription": "Uitgebreide cijfers over je voortgang en het gevecht.",
    "tooltip.hudStopBird": "Stop de vogel",
    "tooltip.hudLifetimeStats": "Totale statistieken",
    "tooltip.hudHideWindows": "Vensters verbergen",
    "tooltip.events.roar": "Verdovend gebrul",
    "tooltip.events.fire": "Vuuradem",
    "tooltip.events.claw": "Klauwslag",
    "tooltip.events.dialog": "Bijzondere gebeurtenis",
    "tooltip.events.pope_visit": "Bijzonder bezoek",
    "tooltip.events.dungeon_keys": "Een duister geheim",
    "tooltip.events.missing_king": "Waar is de koning?",
    "tooltip.events.catapult": "Een technisch prototype",
    "tooltip.events.engineer": "Hulp op tijd",
    "tooltip.events.invasion_start": "Er komt een invasie aan",
    "tooltip.events.invasion_end": "Bericht van je troepen",
    "tooltip.events.apprenticeships_unlock": "Leerplaatsen vrijgespeeld",
    "tooltip.events.trading": "Een rondtrekkende koopman",
    "tooltip.events.dummy_toy_reveal": "Niet wat ik dacht",
})

T.update({
    "infos.banner.events": "Gebeurtenissen",
    "infos.banner.stats": "Statistieken",
    "infos.banner.engineering": "Techniek",
    "infos.banner.resources": "Grondstoffen",
    "infos.tabs.events": "Gebeurtenissen",
    "infos.tabs.stats": "Statistieken",
    "infos.tabs.engineering": "Techniek",
    "infos.tabs.resources": "Grondstoffen",
    "infos.tabsAriaLabel": "informatietabbladen",
    "game.dummy": "De grote houten pop",
    "game.infiniteBird": "De vogel die niet valt",
    "game.king": "De koning",
    "game.smallDragon": "Tuth'orieth, de ontsprotene",
    "game.bigDragon": "Forth'aarh, die leven geeft en neemt",
    "dungeon.found": "Gevonden",
    "dungeon.giveUp": "Opgeven",
    "dungeon.tooltipDescription": "Verken de kerker (niveau {{level}})",
    "dungeon.cooldownMessage": "De kerker rust. Wacht {{seconds}} seconden om weer naar binnen te gaan.",
    "dungeon.cooldownShort": "{{seconds}} sec",
    "dungeon.levelLabel": "Niveau",
    "dungeon.levelShort": "Niveau {{level}}",
    "dungeon.keysOwned": "Sleutels",
    "dungeon.giveUpTooltip": "Verlaat de kerker (met Gulle buit houd je een deel van de buit)",
    "dungeon.moveHint": "WASD of pijltjestoetsen om te lopen",
    "dungeon.attackHint": "Klik op monsters om aan te vallen",
    "dungeon.chestCountsTooltip": "{{opened}} van {{total}} kisten geopend",
    "dungeon.exitDirection": "UITGANG",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Geslaagde tocht",
    "summaries.dungeonLoot.titleFailed": "Mislukte tocht",
    "summaries.dungeonLoot.titleStuckRescue": "Veilig eruit",
    "summaries.dungeonLoot.lootSummarySubtitle": "Overzicht van de buit",
    "summaries.dungeonLoot.body_one": "{{gold}} goud en {{grayKeys}} sleutel gekregen",
    "summaries.dungeonLoot.body_other": "{{gold}} goud en {{grayKeys}} sleutels gekregen",
    "summaries.dungeonLoot.artifactFound": "{{artifactName}} gevonden.",
    "summaries.fireBreathCasualties.title": "Verliezen door de vuuradem",
    "summaries.fireBreathCasualties.body": "{{list}} verloren",
    "summaries.fireBreathCasualties.none": "Geen verliezen",
    "summaries.fireBreathBlocked.title": "De vuuradem is tegengehouden!",
    "summaries.fireBreathBlocked.body": "Een rookbom heeft je troepen gered.",
    "summaries.toastLabel": "Spelmelding",
})

T.update({
    "levels.title": "Hoofdstukken",
    "levels.locked": "Op slot",
    "levels.active": "Bezig",
    "levels.completed": "Uitgespeeld",
    "levels.continue": "Verder",
    "levels.start": "Beginnen",
    "levels.restart": "Opnieuw spelen",
    "levels.restart_progress_warning": "Nu opnieuw beginnen? Je verliest de niet-opgeslagen"
        " voortgang in dit hoofdstuk.",
    "levels.names.mainGame": "Een grote draak",
    "levels.names.newGamePlus": "Grondstoffenbeheer",
    "levels.names.dummy": "Een magisch speeltje",
    "levels.names.infinite": "Werkelijk eindeloos",
    "levels.names.kingBattle": "Het laatste gevecht van de koning",
})

T.update({
    "menus.tabs.saveData": "Opgeslagen gegevens",
    "menus.saveData.title": "Opgeslagen gegevens",
    "menus.saveData.clearChapterTitle": "Voortgang van de hoofdstukken",
    "menus.saveData.clearChapterExplanation": "Wist goud, troepen, upgrades, voortgang in de"
        " kerker en uitgespeeld-tekens van elk hoofdstuk. Vrijgespeelde hoofdstukken, totale"
        " statistieken, instellingen en artefacten blijven.",
    "menus.saveData.clearChapterButton": "Voortgang van de hoofdstukken wissen",
    "menus.saveData.clearFullTitle": "Alle opgeslagen gegevens",
    "menus.saveData.clearFullExplanation": "Wist alles wat de hoofdstukreset wist, en"
        " bovendien artefacten, vrijgespeelde hoofdstukken en totale statistieken."
        " Instellingen voor geluid, beeld en taal blijven.",
    "menus.saveData.clearFullButton": "Alle opgeslagen gegevens wissen",
    "menus.saveData.clearFullWarning": "Dit kun je niet terugdraaien. Je verliest artefacten,"
        " vrijgespeelde hoofdstukken en totale statistieken.",
})

T.update({
    "artifacts.title": "Artefacten",
    "artifacts.subtitle": "Zeldzame artefacten liggen soms in bijzondere kisten in de kerker."
        " Ze blijven van hoofdstuk tot hoofdstuk.",
    "artifacts.notYetFound": "(nog niet gevonden)",
})

ART = {
    "phoenixWhistle": ("Feniksfluitje", "Een bijzondere vogel brengt een nieuwe munt mee."),
    "emberforgedShield": ("In sintels gesmeed schild", "Krijgers zijn bestand tegen drakenvuur."),
    "moonwellFlask": ("Fles van de maanbron", "Tovenaars gebruiken maar de helft van de mana."),
    "windstepAnklet": ("Enkelband van de windstap", "Elfen worden niet verdoofd."),
    "fangSatchel": ("Tandentas", "Zolang de ronde loopt, maken dieven elk half uur een drakentand."),
    "slumberBerries": ("Sluimerbessen", "Gif vertraagt het gebrul en het vuur van de draak met 10 seconden."),
    "echoingLute": ("Echoënde luit", "Barden geven dubbele inspiratie."),
    "blessingCenser": ("Wierookvat van de zegen", "Priesters werven altijd het dubbele aantal."),
    "victoryTusk": ("Overwinningstand", "Een uitgespeeld niveau geeft dubbel zoveel drakentanden."),
    "cartographersLedger": ("Boek van de kaartenmaker", "Laat zien hoeveel kisten in de kerker al open zijn."),
    "ironSkeletonKey": ("IJzeren loper", "Speelt de kerker vrij tot niveau 20."),
    "everflameLantern": ("Lantaarn van de eeuwige vlam", "De fakkel gaat nooit uit."),
    "midasCoin": ("Munt van Midas", "Dubbel zoveel goud in de kerker."),
    "harvestIdol": ("Oogstbeeld", "Grondstoffen komen 25% sneller binnen."),
    "titanGauntlet": ("Titanenhandschoen", "Tien keer zoveel schade per klik."),
    "wayfindersCompass": ("Kompas van de wegwijzer", "Wijst naar de uitgang van de kerker."),
    "loadedDice": ("Verzwaarde dobbelstenen", "Elke klik is kritiek."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("IJzeren vinger", "+{{bonus}} schade per klik"),
    "featherFinger": ("Verenvinger", "+{{bonus}} kliks per seconde"),
    "wakeupCall": ("Wekroep", "Elke klik kort de verdoving met {{bonus}} seconden in"),
    "electricalFinger": ("Elektrische vinger", "Elke klik heeft {{bonus}}% kans om de bliksem te roepen."),
    "perfectClick": ("Perfecte klik", "+{{bonus}}% kans op een kritieke klik"),
    "criticalStrike": ("Kritieke slag", "+{{bonus}}x schade bij een kritieke klik"),
    "goldenExplosion": ("Gouden explosie", "{{bonus}}x beloning als je op vogels klikt"),
    "naturalLeader": ("Geboren leider", "Kliks vullen de inspiratiebalk met +{{bonus}}/klik"),
    "moneyCursor": ("Goudcursor", "{{bonus}}x goud per klik"),
    "fullChests": ("Volle kisten", "{{bonus}}% minder kans dat een kist in de kerker leeg is"),
    "carpalCure": ("Polskuur", "Houd de muisknop ingedrukt om de draak onafgebroken aan te vallen."),
    "shortSword": ("Kort zwaard", "+{{bonus}}x schadevermenigvuldiger voor {{type}}"),
    "longSword": ("Lang zwaard", "Nog +{{bonus}}x schadevermenigvuldiger voor krijgers"),
    "twoHandedSword": ("Tweehandig zwaard", "Nogmaals +{{bonus}}x schadevermenigvuldiger voor krijgers"),
    "battleShout": ("Strijdkreet", "Vult de inspiratiebalk met +{{bonus}} per slag"),
    "warCry": ("Oorlogskreet", "Zet inspiratie vanzelf aan bij de volgende tik zodra de"
               " vermenigvuldiger op het hoogste staat"),
    "barbarian": ("Barbaar", "+{{bonus}} basisschade"),
    "thickArmor": ("Dik harnas", "{{bonus}}% minder fysieke schade"),
    "fireArmor": ("Vuurharnas", "{{bonus}}% minder troepen sterven door de vuuradem"),
    "heavyRocks": ("Zware rotsen", "+{{bonus}}% katapultschade per niveau"),
    "silverBlade": ("Zilveren kling", "+{{bonus}}x vermenigvuldiger op goud per slag"),
    "goldenBlade": ("Gouden kling", "Nog +{{bonus}}x vermenigvuldiger op goud per slag"),
    "loyalMercenaries": ("Trouwe huurlingen", "{{typePlural}} die je koopt doen +{{bonus}}x"
                         " schade per niveau"),
    "loyalServants": ("Trouwe dienaren", "{{bonus}}% goedkoper om {{type}} en alles daarboven te werven"),
    "teamWork": ("Samenwerking", "Werft extra {{typePlural}} voor elke {{type}} die je koopt"),
    "dungeonPrecision": ("Nauwkeurigheid in de diepte", "+{{bonus}}% kans op een kritieke treffer in de kerker"),
    "mazeCrusher": ("Doolhofbreker", "+{{bonus}} kritieke schade in de kerker"),
    "magicMissile": ("Magische pijl", "+{{bonus}}x schadevermenigvuldiger voor {{type}}"),
    "manaSword": ("Manazwaard", "Elke tovenaar laadt het zwaard van een krijger met mana."
                  " +{{bonus}}x schadevermenigvuldiger zolang de mana boven 90 staat"),
    "magicMouse": ("Magische muis", "Vult de manabalk met +{{bonus}} per klik"),
    "manaSurge": ("Manastroom", "Vult de manabalk van je tovenaars"),
    "manaPool": ("Manabron", "+{{bonus}}% hoogste mana"),
    "manaBoost": ("Manastoot", "De schade van tovenaars verdubbelt zolang de mana boven {{current}} staat"),
    "weatherForecast": ("Weerbericht", "+{{bonus}}% kans op een blikseminslag"),
    "lightningStrike": ("Blikseminslag", "Voegt een bliksem toe van +{{bonus}}x de schade"
                        " van {{type}} voor elke gekochte upgrade"),
    "silverStaff": ("Zilveren staf", "+{{bonus}}x vermenigvuldiger op goud per slag"),
    "goldenStaff": ("Gouden staf", "Nog +{{bonus}}x vermenigvuldiger op goud per slag"),
    "magicFire": ("Magisch vuur", "De fakkel brandt +{{bonus}} seconden langer"),
    "archimage": ("Aartsmagiër", "+{{bonus}} basisschade"),
    "huntersEye": ("Jagersoog", "+{{bonus}}% kans om elke tik een vogel binnen bereik te raken"),
    "criticalChance": ("Scherp vizier", "+{{bonus}}% kans op een kritiek schot"),
    "criticalDamage": ("Bladsnijder", "+{{bonus}}x schade bij een kritiek schot"),
    "huntingSeason": ("Jachtseizoen", "Roept meteen een zwerm vogels op"),
    "elvenEyes": ("Elfenogen", "Je ziet nog +{{bonus}} seconden in het donker nadat de fakkel uitgaat"),
    "multipleShot": ("Meerdere pijlen", "Schiet per niveau een pijl extra"),
    "silverArrow": ("Zilveren pijl", "+{{bonus}}x vermenigvuldiger op goud per slag"),
    "goldenArrow": ("Gouden pijl", "Nog +{{bonus}}x vermenigvuldiger op goud per slag"),
    "iceArrow": ("IJspijl", "Vertraagt het vuur van de draak met {{bonus}} seconden"),
    "animalInstinct": ("Dierlijk instinct", "De katapult schiet katten in plaats van rotsen,"
                       " en tijgers in plaats van katten, elke keer tien keer de schade."),
    "lightningRod": ("Bliksemafleider", "{{bonus}}% kans om nog een bliksem aan te trekken"
                     " als de bliksem van je tovenaars raakt."),
    "recycledArrows": ("Hergebruikte pijlen", "De aanval van elfen kost minder hout"),
    "lightfoot": ("Lichtvoetig", "+{{bonus}}% sneller lopen en draaien in de kerker"),
    "fastHands": ("Snelle handen", "Kort de tijd om goud te maken met {{bonus}} seconden in"),
    "sharpDagger": ("Sluipmoordenaarskling", "Dieven vallen ook aan, met {{current}} schade"),
    "poisonDagger": ("Vergiftigde dolk", "+{{bonus}}% kans om de draak te vergiftigen"),
    "blackMamba": ("Zwarte mamba", "+{{bonus}}x gifschade van de schade van dieven"),
    "lingeringToxin": ("Nawerkend gif", "Het gif werkt +{{bonus}} seconden langer"),
    "smokeBomb": ("Rookbom", "Zet een val voor de draak met {{current}}% kans dat hij bij de"
                  " volgende slag afgaat en die tegenhoudt."),
    "catBomb": ("Kattenbom", "De lading van de katapult ontploft bij de inslag, dubbele schade."),
    "pickpocket": ("Zakkenroller", "+{{bonus}}x vermenigvuldiger op het goud dat {{type}} maakt"),
    "lockPick": ("Loper", "Elke tocht begint met {{bonus}} deuren die al open zijn."),
    "midasTouch": ("Aanraking van Midas", "Nog +{{bonus}}x vermenigvuldiger op het goud dat {{type}} maakt"),
    "stuffedChests": ("Propvolle kisten", "+{{bonus}}% goud uit de kisten in de kerker"),
    "tuningFork": ("Stemvork", "+{{bonus}} inspiratie verzameld"),
    "luteSolo": ("Luitsolo", "+{{bonus}}x hoogste inspiratievermenigvuldiger"),
    "obnoxiousGuitarist": ("Vervelende gitarist", "Inspiratie duurt +{{bonus}} seconden langer"),
    "piercedEardrums": ("Doorboorde trommelvliezen", "De brulteller van de draak loopt {{bonus}}% trager"),
    "replay": ("Toegift", "{{bonus}}% kans dat de inspiratie opnieuw begint als ze afloopt"),
    "sonicBarrier": ("Geluidsbarrière", "De vuurteller van de draak loopt {{bonus}}% trager"),
    "cacofonix": ("Kakofonix", "Verdooft je eigen troepen zodra je hem koopt"),
    "churchChoir": ("Kerkkoor", "Werft 1 seminarie telkens als de inspiratie aanslaat"),
    "encore": ("Bis", "Kort de rust van de inspiratie met {{bonus}} seconden in"),
    "lockerRoomSpeech": ("Toespraak in de kleedkamer", "Maakt inspiratie terwijl het spel dicht is,"
                         " op {{current}}% van het tempo"),
    "orderInTheUk": ("Orde in het koninkrijk", "Terwijl het spel dicht is, laat je muziek de"
                     " ambachtslieden overwerken en grondstoffen maken op {{current}}% van het gewone tempo"),
    "majorKey": ("Grote terts", "Koopt een sleutel voor de kerker. (Ja, de woordgrap is slecht.)"),
    "vulnerableFrequencies": ("Kwetsbare frequenties", "Vijanden in de kerker zijn na elke slag"
                              " {{bonus}} milliseconden korter onkwetsbaar"),
    "heroResources": ("Personeelszaken voor helden", "+{{bonus}}% kans om dubbel zoveel helden te werven"),
    "blessedAura": ("Gezegende aura", "{{bonus}}% minder troepen sterven door de vuuradem"),
    "blessedBird": ("Gezegende vogel", "{{current}}% kans dat een vogel gezegend verschijnt"
                    " en dubbel goud geeft"),
    "powerTransfer": ("Krachtoverdracht", "Bij elke werving vult de mana van je tovenaars met"
                      " 0,5 per priester die je hebt"),
    "generousLoot": ("Gulle buit", "Als een tocht mislukt, houd je toch {{current}}% van de buit."),
    "divineLight": ("Goddelijk licht", "+{{bonus}}% kans om een gedoofde fakkel weer aan te steken"),
    "recruitWarriors": ("Krijgers werven", "Hiermee kun je krijgers voor de strijd werven"),
    "recruitElves": ("Elfen werven", "Hiermee kun je elfen voor de strijd werven"),
    "recruitWizards": ("Tovenaars werven", "Hiermee kun je tovenaars voor de strijd werven"),
    "recruitBards": ("Barden werven", "Hiermee kun je barden voor de strijd werven"),
    "recruitThieves": ("Dieven werven", "Hiermee kun je dieven voor de strijd werven"),
    "recruitClerics": ("Priesters werven", "Hiermee kun je priesters voor de strijd werven"),
}
for k, (title, desc) in D.items():
    T[f"upgrades.details.{k}.title"] = title
    T[f"upgrades.details.{k}.description"] = desc

SUFFIX = {
    "wakeupCall.suffix": " sec",
    "elvenEyes.suffix": " sec",
    "iceArrow.suffix": " sec",
    "lingeringToxin.suffix": " sec",
    "obnoxiousGuitarist.suffix": " sec",
    "encore.suffix": " sec",
    "manaPool.suffix": " mana",
    "manaBoost.suffix": " mana",
    "huntingSeason.suffix": " vogels",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

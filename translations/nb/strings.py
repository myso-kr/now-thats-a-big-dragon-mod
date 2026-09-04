# -*- coding: utf-8 -*-
"""The Norwegian Bokmål UI strings.

Address: "du" throughout. Norwegian dropped "De" from ordinary use long ago, and a King
who used it would sound like a letter from the tax office. He is grand in tone, not in
pronoun.

Bokmål allows both a masculine and a feminine form for many nouns; the masculine is
used consistently here, which is what most written Bokmål does and what keeps the UI
from looking like two dialects at once.

Only the display face lacks the slashed O, so that is the one slot our font fills.
"""

T = {}

T.update({
    "upgrades.upgrades": "Oppgraderinger",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Neste nivå",
    "upgrades.currentLevel": "Nåværende",
    "upgrades.newGamePlusOnly": "Bare i kapittelet \"Ressursstyring\"",
    "upgrades.max": "Maks",
    "upgrades.lockedMessage": "Oppgrader {{parentSkill}} mer for å låse opp denne",
    "common.wishlistNow": "Legg den på ønskelisten!",
})

T.update({
    "statistics.section.ttb": "Kamptid",
    "statistics.section.dgps": "Skade og gull per sekund",
    "statistics.section.resourceBalance": "Ressursbalanse",
    "statistics.lifetime.title": "Samlet statistikk",
    "statistics.lifetime.totalPlaytime": "Samlet spilletid",
    "statistics.lifetime.totalGoldEarned": "Gull tjent totalt",
    "statistics.lifetime.totalGoldSpent": "Gull brukt totalt",
    "statistics.lifetime.totalBirdsKilled": "Fugler skutt ned totalt",
    "statistics.lifetime.totalClicks": "Klikk totalt",
    "statistics.lifetime.totalHeroesRecruited": "Helter vervet totalt",
    "statistics.lifetime.heroesPurchased": "Kjøpt",
    "statistics.lifetime.heroesRecruited": "Vervet",
    "statistics.lifetime.tier1": "Trinn 1 vervet (kjøpt)",
    "statistics.lifetime.tier2": "Trinn 2 vervet (kjøpt)",
    "statistics.lifetime.tier3": "Trinn 3 vervet (kjøpt)",
    "statistics.lifetime.totalDamageDealt": "Skade påført totalt",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Mistet til ildpust",
    "statistics.battleDuration": "Gått: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Går dette i det hele tatt an å vinne?",
    "statistics.infiniteEstimatedVictory": "Ekte seier er umulig!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Du er helten vår!</strong>];"
        " (0-1000000000)[Seier om <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Klikk eller trykk Z for å angripe dragen!</strong>]",
    "statistics.perSec": "/sek",
    "statistics.generationSection": "Produksjon",
    "statistics.critSection": "Spesielt",
    "statistics.dps": "Troppenes skade: <strong>{{dps}}/sek</strong>",
    "statistics.gps": "Troppenes gull: <strong>{{gps}}/sek</strong>",
    "statistics.dpc": "Skade per klikk: <strong>{{dpc}}/klikk</strong>",
    "statistics.gpc": "Gull per klikk: <strong>{{gpc}}/klikk</strong>",
    "statistics.catapultDamage": "Skade: <strong>{{damage}}/skudd</strong>",
    "statistics.catapultTimeToShoot": "Til neste skudd: <strong>{{time}} sek</strong>",
    "statistics.undo.disabledLine": "Klikk innen 10 sekunder for å angre et feilkjøp"
        " og få gullet tilbake.",
    "statistics.undo.enabledAction": "Klikk for å angre kjøpet av {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Du får {{refund}} tilbake.",
    "statistics.undo.enabledTimer": "{{seconds}} sekunder igjen.",
    "statistics.undo.refundGold": "{{amount}} gull",
})

for base, one, many in [
    ("seconds", "sekund", "sekunder"), ("minutes", "minutt", "minutter"),
    ("hours", "time", "timer"), ("days", "dag", "dager"),
    ("months", "måned", "måneder"), ("years", "år", "år"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_other"] = many

T.update({
    "generators.generators": "Tropper",
    "generators.buy": "kjøp {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} sek",
    "generators.ngPlusProductionToggle": "Slå produksjon på eller av",
    "generators.tabs.troops": "Tropper",
    "generators.tabs.support": "Støtte",
    "generators.fireUnitsButton.tooltip": "Si opp tropper for å bruke færre ressurser"
        " og likevel beholde noe av produksjonen.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Den magiske kraften bak trollmennenes angrep.",
    "generators.emptyManaDescription": "Kjøp \"Manastrøm\" for å angripe igjen.",
    "generators.inspiration": "Inspirasjon",
    "generators.inspirationDescription": "Når den er i gang, mangedobles styrken til alle heltene.",
    "generators.tabsAriaLabel": "troppefaner",
})

UNITS = {
    "warrior": ("Kriger", "Krigere"),
    "wizard": ("Trollmann", "Trollmenn"),
    "elf": ("Alv", "Alver"),
    "garrison": ("Garnison", "Garnisoner"),
    "academy": ("Magiakademi", "Magiakademier"),
    "academy_short": ("Akademi", "Akademier"),
    "outpost": ("Bueskytterpost", "Bueskytterposter"),
    "outpost_short": ("Forpost", "Forposter"),
    "council": ("Krigsråd", "Krigsråd"),
    "nexus": ("Erkemagienes knutepunkt", "Erkemagienes knutepunkter"),
    "forest": ("Eldgammel skog", "Eldgamle skoger"),
    "thief": ("Tyv", "Tyver"),
    "bard": ("Bard", "Barder"),
    "cleric": ("Prest", "Prester"),
    "guild": ("Tyvelaug", "Tyvelaug"),
    "guild_short": ("Laug", "Laug"),
    "troupe": ("Gjøglertropp", "Gjøglertropper"),
    "troupe_short": ("Tropp", "Tropper"),
    "seminary": ("Hellig seminar", "Hellige seminarer"),
    "seminary_short": ("Seminar", "Seminarer"),
    "congress": ("Skyggekonvent", "Skyggekonventer"),
    "theater": ("Stort teater", "Store teatre"),
    "college": ("Kardinalkollegium", "Kardinalkollegier"),
    "catapult": ("Katapult", "Katapulter"),
    "builder": ("Bygger", "Byggere"),
    "engineer": ("Ingeniør", "Ingeniører"),
    "farmer": ("Bonde", "Bønder"),
    "lumberjack": ("Tømmerhogger", "Tømmerhoggere"),
    "miner": ("Gruvearbeider", "Gruvearbeidere"),
    "apprenticeships": ("Læreplass", "Læreplasser"),
    "tradespeople": ("Håndverker", "Håndverkere"),
}
for base, (one, many) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_other"] = many

T.update({
    "generators.unitDescription.warrior": "Seige nærkampsfightere.",
    "generators.unitDescription.wizard": "Slår til på mellomavstand, men tåler lite.",
    "generators.unitDescription.elf": "Skyter smidig på lang avstand, utenfor dragens rekkevidde.",
    "generators.unitDescription.garrison": "Befestet base som verver krigere.",
    "generators.unitDescription.outpost": "Avsidesliggende base som verver alver.",
    "generators.unitDescription.academy": "Skole som utdanner trollmenn til kamp.",
    "generators.unitDescription.council": "Militær organisasjon som oppretter garnisoner.",
    "generators.unitDescription.nexus": "Mystisk organisasjon som oppretter akademier.",
    "generators.unitDescription.forest": "Hellig skog som oppretter forposter.",
    "generators.unitDescription.thief": "Slu: forgifter dragen og stjeler gullet dens.",
    "generators.unitDescription.bard": "Kan inspirere troppene dine til å slåss hardere.",
    "generators.unitDescription.cleric": "Beskytter og verver nye helter til kampen.",
    "generators.unitDescription.guild": "Undergrunnsnettverk som verver tyver.",
    "generators.unitDescription.troupe": "Omreisende selskap som verver barder.",
    "generators.unitDescription.seminary": "Hellig institusjon som utdanner prester.",
    "generators.unitDescription.congress": "Organisasjon i skyggene som oppretter tyvelaug.",
    "generators.unitDescription.theater": "Mektig institusjon som oppretter gjøglertropper.",
    "generators.unitDescription.college": "Religiøs organisasjon som oppretter seminarer.",
    "generators.unitDescription.catapult": "Beleiringsvåpen som gjør stor skade på dragen.",
    "generators.unitDescription.builder": "Bygger bygninger på andre nivå.",
    "generators.unitDescription.engineer": "Oppretter organisasjoner på høyere nivåer.",
    "generators.unitDescription.farmer": "Dyrker mat til kongeriket.",
    "generators.unitDescription.lumberjack": "Feller tømmer til byggingen.",
    "generators.unitDescription.miner": "Bryter malm i fjellene.",
    "generators.unitDescription.apprenticeships": "Lærer opp håndverkere.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} skade/{{rate}} sek",
    "wizard": "{{generatorGeneration}} skade/{{rate}} sek",
    "elf": "{{generatorGeneration}} skade/{{rate}} sek",
    "catapult": "{{generatorGeneration}} skade/{{rate}} sek",
    "thief": "+{{generatorGeneration}} gull/{{rate}} sek",
    "bard": "+{{generatorGeneration}} inspirasjon/{{rate}} sek",
    "cleric": "+{{generatorGeneration}} helter/{{rate}} sek",
    "builder": "+{{generatorGeneration}} bygninger/{{rate}} sek",
    "engineer": "+{{generatorGeneration}} organisasjoner/{{rate}} sek",
    "farmer": "+{{generatorGeneration}} mat/{{rate}} sek",
    "lumberjack": "+{{generatorGeneration}} tømmer/{{rate}} sek",
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
    "settings.settings": "Innstillinger",
    "settings.buy_max": "Kjøp maks",
    "settings.audio": "Musikk og lyd",
    "settings.game": "Spill",
    "settings.graphics": "Grafikk",
    "settings.offline_progress": "Framgang offline",
    "settings.wishlist_now": "Legg på ønskelisten",
    "menus.settings": "Innstillinger",
    "menus.tabs.game": "Spill",
    "menus.tabs.graphics": "Grafikk",
    "menus.tabs.audio": "Lyd",
    "menus.tabs.levels": "Kapitler",
    "menus.tabs.credits": "Medvirkende",
    "menus.credits.title": "Medvirkende",
    "menus.credits.developedBy": "Utviklet av",
    "menus.credits.developedWith": "Utviklet med",
    "menus.credits.bigThanksTo": "Stor takk til",
    "menus.credits.theRestOfTheDiscordServer": "alle andre på Discord-serveren",
    "menus.credits.andYou": "og deg!",
    "menus.music": "Musikk",
    "menus.sfx": "Lydeffekter",
    "menus.audioSettings": "Lydinnstillinger",
    "menus.gameSettings": "Spillinnstillinger",
    "menus.graphicsSettings": "Grafikkinnstillinger",
    "menus.language": "Språk",
    "menus.languages.en": "Engelsk",
    "menus.languages.fr": "Fransk",
    "menus.languages.de": "Tysk",
    "menus.languages.pt": "Portugisisk",
    "menus.languages.tr": "Tyrkisk",
    "menus.shakeIntensity": "Risting",
    "menus.largerTextSize": "Større tekst",
    "menus.crtFilter": "CRT-filter",
    "menus.chromaticAberrationSlider": "Fargespredning",
    "menus.chromaticAberration": "Fargespredning",
    "menus.swordSwooshSounds": "Sverd- og kritiske lyder",
    "menus.catSounds": "Kattelyder",
    "menus.fullscreen": "Fullskjerm",
    "menus.resume": "Spill videre",
    "menus.close": "Lukk",
    "menus.quitGame": "Avslutt spillet",
    "menus.joinDiscord": "Bli med på Discord",
    "menus.clear_save_label": "Slette framgangen din?",
    "menus.zoom_adjustment": "Zoom på grensesnittet",
    "menus.clear_save": "Slett nå",
    "menus.are_you_sure": "Er du sikker?",
    "menus.cannot_be_reversed": "Dette kan ikke angres.",
    "menus.yes": "Ja",
    "menus.no": "Nei",
})

T.update({
    "tooltip.inspiration": "Inspirasjon",
    "tooltip.inspirationDescription": "Når den er i gang, mangedobles styrken til alle heltene.",
    "tooltip.maxInspiration": "Høyeste multiplikator",
    "tooltip.maxInspirationMultiplier": "Høyeste multiplikator",
    "tooltip.statisticsDescription": "Detaljerte tall om framgangen din og kampen.",
    "tooltip.hudStopBird": "Stopp fuglen",
    "tooltip.hudLifetimeStats": "Samlet statistikk",
    "tooltip.hudHideWindows": "Skjul vinduer",
    "tooltip.events.roar": "Lammende brøl",
    "tooltip.events.fire": "Ildpust",
    "tooltip.events.claw": "Kloslag",
    "tooltip.events.dialog": "Spesiell hendelse",
    "tooltip.events.pope_visit": "Et spesielt besøk",
    "tooltip.events.dungeon_keys": "En mørk hemmelighet",
    "tooltip.events.missing_king": "Hvor er kongen?",
    "tooltip.events.catapult": "En teknisk prototyp",
    "tooltip.events.engineer": "Hjelp i rett tid",
    "tooltip.events.invasion_start": "En invasjon er på vei",
    "tooltip.events.invasion_end": "Bud fra troppene",
    "tooltip.events.apprenticeships_unlock": "Læreplasser låst opp",
    "tooltip.events.trading": "En omreisende kjøpmann",
    "tooltip.events.dummy_toy_reveal": "Ikke det jeg trodde",
})

T.update({
    "infos.banner.events": "Hendelser",
    "infos.banner.stats": "Statistikk",
    "infos.banner.engineering": "Teknikk",
    "infos.banner.resources": "Ressurser",
    "infos.tabs.events": "Hendelser",
    "infos.tabs.stats": "Statistikk",
    "infos.tabs.engineering": "Teknikk",
    "infos.tabs.resources": "Ressurser",
    "infos.tabsAriaLabel": "informasjonsfaner",
    "game.dummy": "Den store tredukken",
    "game.infiniteBird": "Fuglen som ikke kan felles",
    "game.king": "Kongen",
    "game.smallDragon": "Tuth'orieth, den spirende",
    "game.bigDragon": "Forth'aarh, som gir og tar liv",
    "dungeon.found": "Funnet",
    "dungeon.giveUp": "Gi opp",
    "dungeon.tooltipDescription": "Utforsk fangehullet (nivå {{level}})",
    "dungeon.cooldownMessage": "Fangehullet hviler. Vent {{seconds}} sekunder på å gå inn igjen.",
    "dungeon.cooldownShort": "{{seconds}} sek",
    "dungeon.levelLabel": "Nivå",
    "dungeon.levelShort": "Nivå {{level}}",
    "dungeon.keysOwned": "Nøkler",
    "dungeon.giveUpTooltip": "Forlat fangehullet (behold noe av byttet med Rundhåndet bytte)",
    "dungeon.moveHint": "WASD eller piltaster for å gå",
    "dungeon.attackHint": "Klikk på monstre for å angripe",
    "dungeon.chestCountsTooltip": "{{opened}} av {{total}} kister åpnet",
    "dungeon.exitDirection": "UTGANG",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Vellykket tur",
    "summaries.dungeonLoot.titleFailed": "Mislykket tur",
    "summaries.dungeonLoot.titleStuckRescue": "Kom trygt ut",
    "summaries.dungeonLoot.lootSummarySubtitle": "Oversikt over byttet",
    "summaries.dungeonLoot.body_one": "Fikk {{gold}} gull og {{grayKeys}} nøkkel",
    "summaries.dungeonLoot.body_other": "Fikk {{gold}} gull og {{grayKeys}} nøkler",
    "summaries.dungeonLoot.artifactFound": "Fant {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Tap til ildpusten",
    "summaries.fireBreathCasualties.body": "Mistet {{list}}",
    "summaries.fireBreathCasualties.none": "Ingen tap",
    "summaries.fireBreathBlocked.title": "Ildpusten ble stoppet!",
    "summaries.fireBreathBlocked.body": "En røykbombe reddet troppene dine.",
    "summaries.toastLabel": "Spillmelding",
})

T.update({
    "levels.title": "Kapitler",
    "levels.locked": "Låst",
    "levels.active": "Pågår",
    "levels.completed": "Fullført",
    "levels.continue": "Fortsett",
    "levels.start": "Start",
    "levels.restart": "Spill om igjen",
    "levels.restart_progress_warning": "Spille om igjen nå?"
        " Du mister ulagret framgang i dette kapittelet.",
    "levels.names.mainGame": "En stor drage",
    "levels.names.newGamePlus": "Ressursstyring",
    "levels.names.dummy": "En magisk leke",
    "levels.names.infinite": "Virkelig uendelig",
    "levels.names.kingBattle": "Kongens siste kamp",
})

T.update({
    "menus.tabs.saveData": "Lagrede data",
    "menus.saveData.title": "Lagrede data",
    "menus.saveData.clearChapterTitle": "Framgangen i kapitlene",
    "menus.saveData.clearChapterExplanation": "Sletter gull, tropper, oppgraderinger, framgang"
        " i fangehullet og fullført-merker for hvert kapittel. Opplåste kapitler, samlet"
        " statistikk, innstillinger og artefakter beholdes.",
    "menus.saveData.clearChapterButton": "Slett framgangen i kapitlene",
    "menus.saveData.clearFullTitle": "Alle lagrede data",
    "menus.saveData.clearFullExplanation": "Sletter alt kapittelnullstillingen sletter,"
        " og i tillegg artefakter, opplåste kapitler og samlet statistikk. Innstillinger for"
        " lyd, grafikk og språk beholdes.",
    "menus.saveData.clearFullButton": "Slett alle lagrede data",
    "menus.saveData.clearFullWarning": "Dette kan ikke angres. Du mister artefakter,"
        " opplåste kapitler og samlet statistikk.",
})

T.update({
    "artifacts.title": "Artefakter",
    "artifacts.subtitle": "Sjeldne artefakter dukker av og til opp i spesielle kister i"
        " fangehullet. De følger med fra kapittel til kapittel.",
    "artifacts.notYetFound": "(ikke funnet ennå)",
})

ART = {
    "phoenixWhistle": ("Føniksfløyten", "En spesiell fugl bringer med seg en ny mynt."),
    "emberforgedShield": ("Glørsmidd skjold", "Krigere tar ingen skade av drageild."),
    "moonwellFlask": ("Flaske fra månebrønnen", "Trollmenn bruker bare halvparten så mye mana."),
    "windstepAnklet": ("Vindstegets ankelring", "Alver blir ikke lammet."),
    "fangSatchel": ("Hoggtannveske", "Mens runden går, lager tyver en dragetann hver halvtime."),
    "slumberBerries": ("Slumrebær", "Gift forsinker dragens brøl og ild med 10 sekunder."),
    "echoingLute": ("Gjenlydende lutt", "Barder gir dobbel inspirasjon."),
    "blessingCenser": ("Velsignelsens røkelseskar", "Prester verver alltid dobbelt så mange."),
    "victoryTusk": ("Seierstannen", "Et fullført nivå gir dobbelt så mange dragetenner."),
    "cartographersLedger": ("Kartteknerens bok", "Viser hvor mange av fangehullets kister som er åpnet."),
    "ironSkeletonKey": ("Dirk av jern", "Låser opp fangehullet til nivå 20."),
    "everflameLantern": ("Evigflammens lykt", "Fakkelen slukner aldri."),
    "midasCoin": ("Midasmynten", "Dobbelt så mye gull i fangehullet."),
    "harvestIdol": ("Innhøstingsgudebildet", "Ressursproduksjonen øker med 25 %."),
    "titanGauntlet": ("Titanhansken", "Ti ganger så mye skade per klikk."),
    "wayfindersCompass": ("Veiviserens kompass", "Peker mot fangehullets utgang."),
    "loadedDice": ("Fusketerninger", "Hvert klikk blir kritisk."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Jernfinger", "+{{bonus}} skade per klikk"),
    "featherFinger": ("Fjærfinger", "+{{bonus}} klikk per sekund"),
    "wakeupCall": ("Vekking", "Hvert klikk forkorter lammelsen med {{bonus}} sekunder"),
    "electricalFinger": ("Elektrisk finger", "Hvert klikk har {{bonus}} % sjanse til å kalle på lynet."),
    "perfectClick": ("Perfekt klikk", "+{{bonus}} % sjanse for kritisk klikk"),
    "criticalStrike": ("Kritisk slag", "+{{bonus}}x skade ved kritisk klikk"),
    "goldenExplosion": ("Gyllen eksplosjon", "{{bonus}}x belønning når du klikker på fugler"),
    "naturalLeader": ("Født leder", "Klikk fyller inspirasjonsmåleren med +{{bonus}}/klikk"),
    "moneyCursor": ("Gullmarkør", "{{bonus}}x gull per klikk"),
    "fullChests": ("Fulle kister", "{{bonus}} % mindre sjanse for at en kiste i fangehullet er tom"),
    "carpalCure": ("Håndleddskur", "Hold museknappen nede for å angripe dragen uten opphold."),
    "shortSword": ("Kortsverd", "+{{bonus}}x skademultiplikator for {{type}}"),
    "longSword": ("Langsverd", "Enda +{{bonus}}x skademultiplikator for krigere"),
    "twoHandedSword": ("Tohåndssverd", "Nok en +{{bonus}}x skademultiplikator for krigere"),
    "battleShout": ("Kamprop", "Fyller inspirasjonsmåleren med +{{bonus}} per slag"),
    "warCry": ("Krigsrop", "Setter i gang inspirasjonen av seg selv ved neste tikk,"
               " når multiplikatoren er på det høyeste"),
    "barbarian": ("Barbar", "+{{bonus}} grunnskade"),
    "thickArmor": ("Tykk rustning", "{{bonus}} % mindre fysisk skade"),
    "fireArmor": ("Ildrustning", "{{bonus}} % færre tropper dør av ildpusten"),
    "heavyRocks": ("Tunge steiner", "+{{bonus}} % katapultskade per nivå"),
    "silverBlade": ("Sølvklinge", "+{{bonus}}x multiplikator på gull per slag"),
    "goldenBlade": ("Gyllen klinge", "Enda +{{bonus}}x multiplikator på gull per slag"),
    "loyalMercenaries": ("Trofaste leiesoldater", "{{typePlural}} du kjøper gjør"
                         " +{{bonus}}x skade per nivå"),
    "loyalServants": ("Trofaste tjenere", "{{bonus}} % billigere å verve {{type}} og alt over"),
    "teamWork": ("Samarbeid", "Verver ekstra {{typePlural}} for hver {{type}} du kjøper"),
    "dungeonPrecision": ("Presisjon i dypet", "+{{bonus}} % sjanse for kritisk treff i fangehullet"),
    "mazeCrusher": ("Labyrintknuseren", "+{{bonus}} kritisk skade i fangehullet"),
    "magicMissile": ("Magisk prosjektil", "+{{bonus}}x skademultiplikator for {{type}}"),
    "manaSword": ("Manasverd", "Hver trollmann fyller sverdet til en kriger med mana."
                  " +{{bonus}}x skademultiplikator når manaen er over 90"),
    "magicMouse": ("Magisk mus", "Fyller manamåleren med +{{bonus}} per klikk"),
    "manaSurge": ("Manastrøm", "Fyller manamåleren til trollmennene"),
    "manaPool": ("Manakilde", "+{{bonus}} % høyeste mana"),
    "manaBoost": ("Manastøt", "Trollmennenes skade dobles når manaen er over {{current}}"),
    "weatherForecast": ("Værmelding", "+{{bonus}} % sjanse for lynnedslag"),
    "lightningStrike": ("Lynnedslag", "Legger til et lyn som gjør +{{bonus}}x skade"
                        " av {{type}} for hver kjøpt oppgradering"),
    "silverStaff": ("Sølvstav", "+{{bonus}}x multiplikator på gull per slag"),
    "goldenStaff": ("Gyllen stav", "Enda +{{bonus}}x multiplikator på gull per slag"),
    "magicFire": ("Magisk ild", "Fakkelen brenner +{{bonus}} sekunder lenger"),
    "archimage": ("Erkemagiker", "+{{bonus}} grunnskade"),
    "huntersEye": ("Jegerens øye", "+{{bonus}} % sjanse for å treffe en fugl innen rekkevidde hvert tikk"),
    "criticalChance": ("Skarpt sikte", "+{{bonus}} % sjanse for kritisk skudd"),
    "criticalDamage": ("Bladskjæreren", "+{{bonus}}x skade ved kritisk skudd"),
    "huntingSeason": ("Jaktsesong", "Kaller straks fram en flokk fugler"),
    "elvenEyes": ("Alveøyne", "Du ser i mørket +{{bonus}} sekunder etter at fakkelen slukner"),
    "multipleShot": ("Flere piler", "Skyter en pil til per nivå"),
    "silverArrow": ("Sølvpil", "+{{bonus}}x multiplikator på gull per slag"),
    "goldenArrow": ("Gyllen pil", "Enda +{{bonus}}x multiplikator på gull per slag"),
    "iceArrow": ("Ispil", "Forsinker dragens ild med {{bonus}} sekunder"),
    "animalInstinct": ("Dyreinstinkt", "Katapulten skyter katter i stedet for steiner,"
                       " og tigre i stedet for katter, ti ganger skaden hver gang."),
    "lightningRod": ("Lynavleder", "{{bonus}} % sjanse for å trekke til seg enda et lyn"
                     " når trollmennenes lyn treffer."),
    "recycledArrows": ("Gjenbrukte piler", "Alvenes angrep koster mindre tømmer"),
    "lightfoot": ("Lett på foten", "+{{bonus}} % raskere å gå og snu i fangehullet"),
    "fastHands": ("Raske hender", "Forkorter tiden det tar å lage gull med {{bonus}} sekunder"),
    "sharpDagger": ("Leiemorderklinge", "Tyver angriper også, med {{current}} i skade"),
    "poisonDagger": ("Forgiftet dolk", "+{{bonus}} % sjanse for å forgifte dragen"),
    "blackMamba": ("Svart mamba", "+{{bonus}}x giftskade av tyvenes skade"),
    "lingeringToxin": ("Dvelende gift", "Giften varer +{{bonus}} sekunder lenger"),
    "smokeBomb": ("Røykbombe", "Setter en felle for dragen med {{current}} % sjanse for å"
                  " utløses ved neste slag og stoppe det."),
    "catBomb": ("Kattebombe", "Katapultens ladning eksploderer ved treff, dobbel skade."),
    "pickpocket": ("Lommetyv", "+{{bonus}}x multiplikator på gullet {{type}} lager"),
    "lockPick": ("Dirk", "Hver tur begynner med {{bonus}} dører allerede åpne."),
    "midasTouch": ("Midas' berøring", "Enda +{{bonus}}x multiplikator på gullet {{type}} lager"),
    "stuffedChests": ("Stappfulle kister", "+{{bonus}} % gull fra fangehullets kister"),
    "tuningFork": ("Stemmegaffel", "+{{bonus}} inspirasjon samles"),
    "luteSolo": ("Luttsolo", "+{{bonus}}x høyeste inspirasjonsmultiplikator"),
    "obnoxiousGuitarist": ("Utålelig gitarist", "Inspirasjonen varer +{{bonus}} sekunder"),
    "piercedEardrums": ("Sprengte trommehinner", "Dragens brøltelleren går {{bonus}} % saktere"),
    "replay": ("Ekstranummer", "{{bonus}} % sjanse for at inspirasjonen begynner på nytt når den tar slutt"),
    "sonicBarrier": ("Lydbarriere", "Dragens ildteller går {{bonus}} % saktere"),
    "cacofonix": ("Kakofoniks", "Lammer dine egne tropper når du kjøper ham"),
    "churchChoir": ("Kirkekor", "Verver 1 seminar hver gang inspirasjonen slår til"),
    "encore": ("Dakapo", "Forkorter inspirasjonens hvile med {{bonus}} sekunder"),
    "lockerRoomSpeech": ("Tale i garderoben", "Lager inspirasjon mens spillet er lukket,"
                         " i {{current}} % av takten"),
    "orderInTheUk": ("Orden i kongeriket", "Mens spillet er lukket, får musikken din håndverkerne"
                     " til å jobbe overtid og lage ressurser i {{current}} % av vanlig takt"),
    "majorKey": ("Durtoneart", "Kjøper en nøkkel til fangehullet. (Ja, ordspillet er elendig.)"),
    "vulnerableFrequencies": ("Sårbare frekvenser", "Fiender i fangehullet er udødelige"
                              " {{bonus}} millisekunder kortere etter hvert slag"),
    "heroResources": ("Heltepersonalet", "+{{bonus}} % sjanse for å verve dobbelt så mange helter"),
    "blessedAura": ("Velsignet aura", "{{bonus}} % færre tropper dør av ildpusten"),
    "blessedBird": ("Velsignet fugl", "{{current}} % sjanse for at en fugl kommer velsignet"
                    " og gir dobbelt gull"),
    "powerTransfer": ("Kraftoverføring", "Ved hver verving fylles trollmennenes mana med"
                      " 0,5 for hver prest du har"),
    "generousLoot": ("Rundhåndet bytte", "Når en tur mislykkes, beholder du likevel"
                     " {{current}} % av byttet."),
    "divineLight": ("Guddommelig lys", "+{{bonus}} % sjanse for å tenne en slukket fakkel igjen"),
    "recruitWarriors": ("Verv krigere", "Lar deg verve krigere til kampen"),
    "recruitElves": ("Verv alver", "Lar deg verve alver til kampen"),
    "recruitWizards": ("Verv trollmenn", "Lar deg verve trollmenn til kampen"),
    "recruitBards": ("Verv barder", "Lar deg verve barder til kampen"),
    "recruitThieves": ("Verv tyver", "Lar deg verve tyver til kampen"),
    "recruitClerics": ("Verv prester", "Lar deg verve prester til kampen"),
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
    "huntingSeason.suffix": " fugler",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

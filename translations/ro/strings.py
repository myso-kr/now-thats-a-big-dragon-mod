# -*- coding: utf-8 -*-
"""The Romanian UI strings.

Address: "tu" throughout, which is what Romanian games use. "dumneavoastră" would make
the King sound like a ministry rather than a monarch.

Romanian has three plural categories, and the third is the one that catches people out:
above nineteen the noun takes "de" - "5 secunde" but "20 de secunde". So `_few` is the
plain plural and `_other` carries the "de", and getting that backwards is a mistake a
reader notices immediately.

Romanian needs the breve and the comma-below, which the game's own fonts lack, so the
extended faces fill both slots. The comma-below letters are Ș/ș and Ț/ț - not the
cedilla forms Ş/ş and Ţ/ţ, which are a different pair of code points that Romanian
typography has moved away from.
"""

T = {}

T.update({
    "upgrades.upgrades": "Îmbunătățiri",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Nivelul următor",
    "upgrades.currentLevel": "Curent",
    "upgrades.newGamePlusOnly": "Doar în capitolul \"Gestionarea resurselor\"",
    "upgrades.max": "Max",
    "upgrades.lockedMessage": "Îmbunătățește {{parentSkill}} mai mult ca să deblochezi asta",
    "common.wishlistNow": "Adaugă pe lista de dorințe!",
})

T.update({
    "statistics.section.ttb": "Timp de luptă",
    "statistics.section.dgps": "Daune și aur pe secundă",
    "statistics.section.resourceBalance": "Balanța resurselor",
    "statistics.lifetime.title": "Statistici totale",
    "statistics.lifetime.totalPlaytime": "Timp total de joc",
    "statistics.lifetime.totalGoldEarned": "Aur câștigat în total",
    "statistics.lifetime.totalGoldSpent": "Aur cheltuit în total",
    "statistics.lifetime.totalBirdsKilled": "Păsări doborâte în total",
    "statistics.lifetime.totalClicks": "Clicuri în total",
    "statistics.lifetime.totalHeroesRecruited": "Eroi recrutați în total",
    "statistics.lifetime.heroesPurchased": "Cumpărați",
    "statistics.lifetime.heroesRecruited": "Recrutați",
    "statistics.lifetime.tier1": "Treapta 1 recrutați (cumpărați)",
    "statistics.lifetime.tier2": "Treapta 2 recrutați (cumpărați)",
    "statistics.lifetime.tier3": "Treapta 3 recrutați (cumpărați)",
    "statistics.lifetime.totalDamageDealt": "Daune produse în total",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Pierduți din cauza suflului de foc",
    "statistics.battleDuration": "Scurs: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Se poate câștiga așa ceva?",
    "statistics.infiniteEstimatedVictory": "O victorie adevărată e imposibilă!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Ești eroul nostru!</strong>];"
        " (0-1000000000)[Victorie în <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Dă clic sau apasă Z ca să ataci dragonul!</strong>]",
    "statistics.perSec": "/sec",
    "statistics.generationSection": "Producție",
    "statistics.critSection": "Special",
    "statistics.dps": "Daunele trupelor: <strong>{{dps}}/sec</strong>",
    "statistics.gps": "Aurul trupelor: <strong>{{gps}}/sec</strong>",
    "statistics.dpc": "Daune pe clic: <strong>{{dpc}}/clic</strong>",
    "statistics.gpc": "Aur pe clic: <strong>{{gpc}}/clic</strong>",
    "statistics.catapultDamage": "Daune: <strong>{{damage}}/lovitură</strong>",
    "statistics.catapultTimeToShoot": "Până la următoarea lovitură: <strong>{{time}} sec</strong>",
    "statistics.undo.disabledLine": "Dă clic în 10 secunde ca să anulezi o cumpărare greșită"
        " și să primești aurul înapoi.",
    "statistics.undo.enabledAction": "Dă clic ca să anulezi cumpărarea a {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Primești înapoi {{refund}}.",
    "statistics.undo.enabledTimer": "Au mai rămas {{seconds}} secunde.",
    "statistics.undo.refundGold": "{{amount}} aur",
})

# `few` is the plain plural (2-19); `other` takes "de" (20 and up). Swapping the two is
# the mistake a Romanian reader notices at once.
for base, one, few, other in [
    ("seconds", "secundă", "secunde", "de secunde"),
    ("minutes", "minut", "minute", "de minute"),
    ("hours", "oră", "ore", "de ore"),
    ("days", "zi", "zile", "de zile"),
    ("months", "lună", "luni", "de luni"),
    ("years", "an", "ani", "de ani"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_few"] = few
    T[f"statistics.{base}_other"] = other

T.update({
    "generators.generators": "Trupe",
    "generators.buy": "cumpără {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} sec",
    "generators.ngPlusProductionToggle": "Pornește sau oprește producția",
    "generators.tabs.troops": "Trupe",
    "generators.tabs.support": "Sprijin",
    "generators.fireUnitsButton.tooltip": "Concediază trupe ca să consumi mai puține resurse"
        " și totuși să păstrezi o parte din producție.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Puterea magică din spatele atacurilor vrăjitorilor.",
    "generators.emptyManaDescription": "Cumpără \"Val de mana\" ca să ataci din nou.",
    "generators.inspiration": "Inspirație",
    "generators.inspirationDescription": "Cât timp e activă, puterea tuturor eroilor se înmulțește.",
    "generators.tabsAriaLabel": "file de trupe",
})

UNITS = {
    "warrior": ("Războinic", "Războinici", "de războinici"),
    "wizard": ("Vrăjitor", "Vrăjitori", "de vrăjitori"),
    "elf": ("Elf", "Elfi", "de elfi"),
    "garrison": ("Garnizoană", "Garnizoane", "de garnizoane"),
    "academy": ("Academie de magie", "Academii de magie", "de academii de magie"),
    "academy_short": ("Academie", "Academii", "de academii"),
    "outpost": ("Avanpost de arcași", "Avanposturi de arcași", "de avanposturi de arcași"),
    "outpost_short": ("Avanpost", "Avanposturi", "de avanposturi"),
    "council": ("Consiliu de război", "Consilii de război", "de consilii de război"),
    "nexus": ("Nexul arhimagilor", "Nexuri ale arhimagilor", "de nexuri ale arhimagilor"),
    "forest": ("Pădure străveche", "Păduri străvechi", "de păduri străvechi"),
    "thief": ("Hoț", "Hoți", "de hoți"),
    "bard": ("Bard", "Barzi", "de barzi"),
    "cleric": ("Preot", "Preoți", "de preoți"),
    "guild": ("Breaslă a hoților", "Bresle ale hoților", "de bresle ale hoților"),
    "guild_short": ("Breaslă", "Bresle", "de bresle"),
    "troupe": ("Trupă de menestreli", "Trupe de menestreli", "de trupe de menestreli"),
    "troupe_short": ("Trupă", "Trupe", "de trupe"),
    "seminary": ("Seminar sfânt", "Seminare sfinte", "de seminare sfinte"),
    "seminary_short": ("Seminar", "Seminare", "de seminare"),
    "congress": ("Adunare din umbră", "Adunări din umbră", "de adunări din umbră"),
    "theater": ("Teatru mare", "Teatre mari", "de teatre mari"),
    "college": ("Colegiu cardinalicesc", "Colegii cardinalicești", "de colegii cardinalicești"),
    "catapult": ("Catapultă", "Catapulte", "de catapulte"),
    "builder": ("Constructor", "Constructori", "de constructori"),
    "engineer": ("Inginer", "Ingineri", "de ingineri"),
    "farmer": ("Fermier", "Fermieri", "de fermieri"),
    "lumberjack": ("Tăietor de lemne", "Tăietori de lemne", "de tăietori de lemne"),
    "miner": ("Miner", "Mineri", "de mineri"),
    "apprenticeships": ("Ucenicie", "Ucenicii", "de ucenicii"),
    "tradespeople": ("Meșteșugar", "Meșteșugari", "de meșteșugari"),
}
for base, (one, few, other) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_few"] = few
    T[f"generators.{base}_other"] = other

T.update({
    "generators.unitDescription.warrior": "Luptători rezistenți în corp la corp.",
    "generators.unitDescription.wizard": "Lovesc de la distanță medie, dar sunt fragili.",
    "generators.unitDescription.elf": "Trag sprinten de departe, din afara razei dragonului.",
    "generators.unitDescription.garrison": "Bază fortificată care recrutează războinici.",
    "generators.unitDescription.outpost": "Bază îndepărtată care recrutează elfi.",
    "generators.unitDescription.academy": "Școală care pregătește vrăjitori pentru luptă.",
    "generators.unitDescription.council": "Organizație militară care înființează garnizoane.",
    "generators.unitDescription.nexus": "Organizație mistică care înființează academii.",
    "generators.unitDescription.forest": "Pădure sfântă care înființează avanposturi.",
    "generators.unitDescription.thief": "Viclean: otrăvește dragonul și îi fură aurul.",
    "generators.unitDescription.bard": "Poate însufleți trupele să lupte mai aprig.",
    "generators.unitDescription.cleric": "Ocrotește și recrutează eroi noi în luptă.",
    "generators.unitDescription.guild": "Rețea subterană care recrutează hoți.",
    "generators.unitDescription.troupe": "Trupă ambulantă care recrutează barzi.",
    "generators.unitDescription.seminary": "Așezământ sfânt care pregătește preoți.",
    "generators.unitDescription.congress": "Organizație din umbră care înființează bresle ale hoților.",
    "generators.unitDescription.theater": "Așezământ măreț care înființează trupe de menestreli.",
    "generators.unitDescription.college": "Organizație religioasă care înființează seminare.",
    "generators.unitDescription.catapult": "Armă de asediu care produce daune mari dragonului.",
    "generators.unitDescription.builder": "Ridică clădiri de nivelul al doilea.",
    "generators.unitDescription.engineer": "Înființează organizații de nivel superior.",
    "generators.unitDescription.farmer": "Cultivă hrană pentru regat.",
    "generators.unitDescription.lumberjack": "Taie lemn pentru construcții.",
    "generators.unitDescription.miner": "Extrage minereu din munți.",
    "generators.unitDescription.apprenticeships": "Pregătește meșteșugari.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} daune/{{rate}} sec",
    "wizard": "{{generatorGeneration}} daune/{{rate}} sec",
    "elf": "{{generatorGeneration}} daune/{{rate}} sec",
    "catapult": "{{generatorGeneration}} daune/{{rate}} sec",
    "thief": "+{{generatorGeneration}} aur/{{rate}} sec",
    "bard": "+{{generatorGeneration}} inspirație/{{rate}} sec",
    "cleric": "+{{generatorGeneration}} eroi/{{rate}} sec",
    "builder": "+{{generatorGeneration}} clădiri/{{rate}} sec",
    "engineer": "+{{generatorGeneration}} organizații/{{rate}} sec",
    "farmer": "+{{generatorGeneration}} hrană/{{rate}} sec",
    "lumberjack": "+{{generatorGeneration}} lemn/{{rate}} sec",
    "miner": "+{{generatorGeneration}} minereu/{{rate}} sec",
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
    "settings.settings": "Setări",
    "settings.buy_max": "Cumpără max",
    "settings.audio": "Muzică și sunet",
    "settings.game": "Joc",
    "settings.graphics": "Grafică",
    "settings.offline_progress": "Progres offline",
    "settings.wishlist_now": "Adaugă pe lista de dorințe",
    "menus.settings": "Setări",
    "menus.tabs.game": "Joc",
    "menus.tabs.graphics": "Grafică",
    "menus.tabs.audio": "Sunet",
    "menus.tabs.levels": "Capitole",
    "menus.tabs.credits": "Distribuție",
    "menus.credits.title": "Distribuție",
    "menus.credits.developedBy": "Dezvoltat de",
    "menus.credits.developedWith": "Dezvoltat cu",
    "menus.credits.bigThanksTo": "Mulțumiri deosebite",
    "menus.credits.theRestOfTheDiscordServer": "tuturor celorlalți de pe serverul Discord",
    "menus.credits.andYou": "și ție!",
    "menus.music": "Muzică",
    "menus.sfx": "Efecte sonore",
    "menus.audioSettings": "Setări de sunet",
    "menus.gameSettings": "Setări de joc",
    "menus.graphicsSettings": "Setări grafice",
    "menus.language": "Limbă",
    "menus.languages.en": "Engleză",
    "menus.languages.fr": "Franceză",
    "menus.languages.de": "Germană",
    "menus.languages.pt": "Portugheză",
    "menus.languages.tr": "Turcă",
    "menus.shakeIntensity": "Zguduire",
    "menus.largerTextSize": "Text mai mare",
    "menus.crtFilter": "Filtru CRT",
    "menus.chromaticAberrationSlider": "Aberație cromatică",
    "menus.chromaticAberration": "Aberație cromatică",
    "menus.swordSwooshSounds": "Sunete de sabie și critice",
    "menus.catSounds": "Sunete de pisică",
    "menus.fullscreen": "Ecran complet",
    "menus.resume": "Continuă jocul",
    "menus.close": "Închide",
    "menus.quitGame": "Ieși din joc",
    "menus.joinDiscord": "Intră pe Discord",
    "menus.clear_save_label": "Ștergi progresul?",
    "menus.zoom_adjustment": "Mărirea interfeței",
    "menus.clear_save": "Șterge acum",
    "menus.are_you_sure": "Ești sigur?",
    "menus.cannot_be_reversed": "Asta nu se poate anula.",
    "menus.yes": "Da",
    "menus.no": "Nu",
})

T.update({
    "tooltip.inspiration": "Inspirație",
    "tooltip.inspirationDescription": "Cât timp e activă, puterea tuturor eroilor se înmulțește.",
    "tooltip.maxInspiration": "Multiplicator maxim",
    "tooltip.maxInspirationMultiplier": "Multiplicator maxim",
    "tooltip.statisticsDescription": "Cifre amănunțite despre progresul tău și despre luptă.",
    "tooltip.hudStopBird": "Oprește pasărea",
    "tooltip.hudLifetimeStats": "Statistici totale",
    "tooltip.hudHideWindows": "Ascunde ferestrele",
    "tooltip.events.roar": "Răget amețitor",
    "tooltip.events.fire": "Suflu de foc",
    "tooltip.events.claw": "Lovitură de gheară",
    "tooltip.events.dialog": "Eveniment deosebit",
    "tooltip.events.pope_visit": "Un oaspete deosebit",
    "tooltip.events.dungeon_keys": "Un secret întunecat",
    "tooltip.events.missing_king": "Unde e regele?",
    "tooltip.events.catapult": "Un prototip tehnic",
    "tooltip.events.engineer": "Ajutor la țanc",
    "tooltip.events.invasion_start": "Se apropie o invazie",
    "tooltip.events.invasion_end": "Vești de la trupe",
    "tooltip.events.apprenticeships_unlock": "Ucenicii deblocate",
    "tooltip.events.trading": "Un negustor ambulant",
    "tooltip.events.dummy_toy_reveal": "Nu e ce credeam",
})

T.update({
    "infos.banner.events": "Evenimente",
    "infos.banner.stats": "Statistici",
    "infos.banner.engineering": "Inginerie",
    "infos.banner.resources": "Resurse",
    "infos.tabs.events": "Evenimente",
    "infos.tabs.stats": "Statistici",
    "infos.tabs.engineering": "Inginerie",
    "infos.tabs.resources": "Resurse",
    "infos.tabsAriaLabel": "file de informații",
    "game.dummy": "Păpușa mare de lemn",
    "game.infiniteBird": "Pasărea care nu poate fi doborâtă",
    "game.king": "Regele",
    "game.smallDragon": "Tuth'orieth, Cel Încolțit",
    "game.bigDragon": "Forth'aarh, Care Dă și Ia Viața",
    "dungeon.found": "Găsit",
    "dungeon.giveUp": "Renunță",
    "dungeon.tooltipDescription": "Explorează temnița (nivelul {{level}})",
    "dungeon.cooldownMessage": "Temnița se odihnește. Așteaptă {{seconds}} secunde ca să intri din nou.",
    "dungeon.cooldownShort": "{{seconds}} sec",
    "dungeon.levelLabel": "Nivel",
    "dungeon.levelShort": "Nivelul {{level}}",
    "dungeon.keysOwned": "Chei",
    "dungeon.giveUpTooltip": "Părăsește temnița (păstrezi o parte din pradă cu Pradă darnică)",
    "dungeon.moveHint": "WASD sau tastele săgeți ca să mergi",
    "dungeon.attackHint": "Dă clic pe monștri ca să ataci",
    "dungeon.chestCountsTooltip": "{{opened}} din {{total}} cufere deschise",
    "dungeon.exitDirection": "IEȘIRE",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Expediție reușită",
    "summaries.dungeonLoot.titleFailed": "Expediție eșuată",
    "summaries.dungeonLoot.titleStuckRescue": "Ieșit teafăr",
    "summaries.dungeonLoot.lootSummarySubtitle": "Bilanțul prăzii",
    "summaries.dungeonLoot.body_one": "Ai primit {{gold}} aur și {{grayKeys}} cheie",
    "summaries.dungeonLoot.body_few": "Ai primit {{gold}} aur și {{grayKeys}} chei",
    "summaries.dungeonLoot.body_other": "Ai primit {{gold}} aur și {{grayKeys}} de chei",
    "summaries.dungeonLoot.artifactFound": "Ai găsit {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Pierderi din suflul de foc",
    "summaries.fireBreathCasualties.body": "Ai pierdut {{list}}",
    "summaries.fireBreathCasualties.none": "Nicio pierdere",
    "summaries.fireBreathBlocked.title": "Suflul de foc a fost oprit!",
    "summaries.fireBreathBlocked.body": "O bombă fumigenă ți-a salvat trupele.",
    "summaries.toastLabel": "Mesaj din joc",
})

T.update({
    "levels.title": "Capitole",
    "levels.locked": "Blocat",
    "levels.active": "În desfășurare",
    "levels.completed": "Terminat",
    "levels.continue": "Continuă",
    "levels.start": "Începe",
    "levels.restart": "Joacă din nou",
    "levels.restart_progress_warning": "Joci din nou acum?"
        " Pierzi progresul nesalvat din acest capitol.",
    "levels.names.mainGame": "Un dragon mare",
    "levels.names.newGamePlus": "Gestionarea resurselor",
    "levels.names.dummy": "O jucărie fermecată",
    "levels.names.infinite": "Cu adevărat fără sfârșit",
    "levels.names.kingBattle": "Ultima luptă a regelui",
})

T.update({
    "menus.tabs.saveData": "Date salvate",
    "menus.saveData.title": "Date salvate",
    "menus.saveData.clearChapterTitle": "Progresul capitolelor",
    "menus.saveData.clearChapterExplanation": "Șterge aurul, trupele, îmbunătățirile, progresul"
        " din temniță și însemnele de terminare pentru fiecare capitol. Capitolele deblocate,"
        " statisticile totale, setările și artefactele rămân.",
    "menus.saveData.clearChapterButton": "Șterge progresul capitolelor",
    "menus.saveData.clearFullTitle": "Toate datele salvate",
    "menus.saveData.clearFullExplanation": "Șterge tot ce șterge resetarea capitolelor, plus"
        " artefactele, capitolele deblocate și statisticile totale. Setările de sunet, grafică"
        " și limbă rămân.",
    "menus.saveData.clearFullButton": "Șterge toate datele salvate",
    "menus.saveData.clearFullWarning": "Asta nu se poate anula. Pierzi artefactele,"
        " capitolele deblocate și statisticile totale.",
})

T.update({
    "artifacts.title": "Artefacte",
    "artifacts.subtitle": "Artefacte rare apar uneori în cufere speciale din temniță."
        " Ele rămân de la un capitol la altul.",
    "artifacts.notYetFound": "(încă negăsit)",
})

ART = {
    "phoenixWhistle": ("Fluierul phoenixului", "O pasăre deosebită aduce o monedă nouă."),
    "emberforgedShield": ("Scut făurit în jar", "Războinicii nu suferă de la focul dragonului."),
    "moonwellFlask": ("Ploscă din fântâna lunii", "Vrăjitorii consumă doar jumătate din mana."),
    "windstepAnklet": ("Brățară a pasului de vânt", "Elfii nu mai sunt amețiți."),
    "fangSatchel": ("Traistă de colți", "Cât ține runda, hoții fac un colț de dragon la fiecare 30 de minute."),
    "slumberBerries": ("Fructe de somn", "Otrava întârzie răgetul și focul dragonului cu 10 secunde."),
    "echoingLute": ("Lăută cu ecou", "Barzii dau inspirație dublă."),
    "blessingCenser": ("Cădelnița binecuvântării", "Preoții recrutează mereu de două ori mai mulți."),
    "victoryTusk": ("Colțul victoriei", "Un nivel terminat dă de două ori mai mulți colți de dragon."),
    "cartographersLedger": ("Registrul cartografului", "Arată câte cufere din temniță au fost deschise."),
    "ironSkeletonKey": ("Șperaclu de fier", "Deblochează temnița până la nivelul 20."),
    "everflameLantern": ("Felinarul flăcării veșnice", "Torța nu se stinge niciodată."),
    "midasCoin": ("Moneda lui Midas", "Aur dublu în temniță."),
    "harvestIdol": ("Idolul recoltei", "Producția de resurse crește cu 25%."),
    "titanGauntlet": ("Mănușa titanului", "Daune de zece ori mai mari pe clic."),
    "wayfindersCompass": ("Busola călăuzei", "Arată ieșirea din temniță."),
    "loadedDice": ("Zaruri măsluite", "Fiecare clic e critic."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Deget de fier", "+{{bonus}} daune pe clic"),
    "featherFinger": ("Deget de pană", "+{{bonus}} clicuri pe secundă"),
    "wakeupCall": ("Deșteptare", "Fiecare clic scurtează amețeala cu {{bonus}} secunde"),
    "electricalFinger": ("Deget electric", "Fiecare clic are {{bonus}}% șanse să cheme fulgerul."),
    "perfectClick": ("Clic perfect", "+{{bonus}}% șanse de clic critic"),
    "criticalStrike": ("Lovitură critică", "+{{bonus}}x daune la clicul critic"),
    "goldenExplosion": ("Explozie aurie", "{{bonus}}x răsplată când dai clic pe păsări"),
    "naturalLeader": ("Lider înnăscut", "Clicurile umplu bara de inspirație cu +{{bonus}}/clic"),
    "moneyCursor": ("Cursor de aur", "{{bonus}}x aur pe clic"),
    "fullChests": ("Cufere pline", "Cu {{bonus}}% mai puține șanse ca un cufăr din temniță să fie gol"),
    "carpalCure": ("Tratament pentru încheietură", "Ține apăsat butonul mouse-ului ca să ataci"
                   " dragonul fără oprire."),
    "shortSword": ("Sabie scurtă", "+{{bonus}}x multiplicator de daune pentru {{type}}"),
    "longSword": ("Spadă lungă", "Încă +{{bonus}}x multiplicator de daune pentru războinici"),
    "twoHandedSword": ("Spadă cu două mâini", "Din nou +{{bonus}}x multiplicator de daune pentru războinici"),
    "battleShout": ("Strigăt de luptă", "Umple bara de inspirație cu +{{bonus}} la fiecare lovitură"),
    "warCry": ("Chemare la arme", "Pornește singură inspirația la următorul tact,"
               " când multiplicatorul e la maximum"),
    "barbarian": ("Barbar", "+{{bonus}} daune de bază"),
    "thickArmor": ("Armură groasă", "Cu {{bonus}}% mai puține daune fizice"),
    "fireArmor": ("Armură de foc", "Cu {{bonus}}% mai puține trupe mor din suflul de foc"),
    "heavyRocks": ("Bolovani grei", "+{{bonus}}% daune de catapultă pe nivel"),
    "silverBlade": ("Tăiș de argint", "+{{bonus}}x multiplicator la aur pe lovitură"),
    "goldenBlade": ("Tăiș de aur", "Încă +{{bonus}}x multiplicator la aur pe lovitură"),
    "loyalMercenaries": ("Mercenari credincioși", "{{typePlural}} pe care îi cumperi produc"
                         " +{{bonus}}x daune pe nivel"),
    "loyalServants": ("Slujitori credincioși", "Cu {{bonus}}% mai ieftin de recrutat {{type}} și tot ce e deasupra"),
    "teamWork": ("Lucru în echipă", "Recrutează {{typePlural}} în plus pentru fiecare {{type}} cumpărat"),
    "dungeonPrecision": ("Precizie în adânc", "+{{bonus}}% șanse de lovitură critică în temniță"),
    "mazeCrusher": ("Zdrobitorul de labirint", "+{{bonus}} daune critice în temniță"),
    "magicMissile": ("Săgeată magică", "+{{bonus}}x multiplicator de daune pentru {{type}}"),
    "manaSword": ("Sabie de mana", "Fiecare vrăjitor încarcă sabia unui războinic cu mana."
                  " +{{bonus}}x multiplicator de daune cât timp mana e peste 90"),
    "magicMouse": ("Șoarece magic", "Umple bara de mana cu +{{bonus}} pe clic"),
    "manaSurge": ("Val de mana", "Umple bara de mana a vrăjitorilor"),
    "manaPool": ("Izvor de mana", "+{{bonus}}% mana maximă"),
    "manaBoost": ("Impuls de mana", "Daunele vrăjitorilor se dublează cât timp mana e peste {{current}}"),
    "weatherForecast": ("Prognoza vremii", "+{{bonus}}% șanse de trăsnet"),
    "lightningStrike": ("Trăsnet", "Adaugă un fulger care produce +{{bonus}}x daunele"
                        " de la {{type}} pentru fiecare îmbunătățire cumpărată"),
    "silverStaff": ("Toiag de argint", "+{{bonus}}x multiplicator la aur pe lovitură"),
    "goldenStaff": ("Toiag de aur", "Încă +{{bonus}}x multiplicator la aur pe lovitură"),
    "magicFire": ("Foc magic", "Torța arde cu +{{bonus}} secunde mai mult"),
    "archimage": ("Arhimag", "+{{bonus}} daune de bază"),
    "huntersEye": ("Ochiul vânătorului", "+{{bonus}}% șanse să nimerești o pasăre din rază la fiecare tact"),
    "criticalChance": ("Ochire ascuțită", "+{{bonus}}% șanse de tragere critică"),
    "criticalDamage": ("Tăietorul de frunze", "+{{bonus}}x daune la tragerea critică"),
    "huntingSeason": ("Sezon de vânătoare", "Cheamă pe loc un stol de păsări"),
    "elvenEyes": ("Ochi de elf", "Vezi în întuneric încă +{{bonus}} secunde după ce se stinge torța"),
    "multipleShot": ("Săgeți multiple", "Trage cu o săgeată în plus pe nivel"),
    "silverArrow": ("Săgeată de argint", "+{{bonus}}x multiplicator la aur pe lovitură"),
    "goldenArrow": ("Săgeată de aur", "Încă +{{bonus}}x multiplicator la aur pe lovitură"),
    "iceArrow": ("Săgeată de gheață", "Întârzie focul dragonului cu {{bonus}} secunde"),
    "animalInstinct": ("Instinct animal", "Catapulta aruncă pisici în loc de bolovani,"
                       " apoi tigri în loc de pisici, de fiecare dată cu daune de zece ori mai mari."),
    "lightningRod": ("Paratrăsnet", "{{bonus}}% șanse să atragi încă un fulger"
                     " când fulgerul vrăjitorilor lovește."),
    "recycledArrows": ("Săgeți refolosite", "Atacul elfilor consumă mai puțin lemn"),
    "lightfoot": ("Pas ușor", "Cu {{bonus}}% mai repede la mers și la întors în temniță"),
    "fastHands": ("Mâini iuți", "Scurtează cu {{bonus}} secunde timpul de a face aur"),
    "sharpDagger": ("Tăișul asasinului", "Hoții atacă și ei, cu {{current}} daune"),
    "poisonDagger": ("Pumnal otrăvit", "+{{bonus}}% șanse să otrăvești dragonul"),
    "blackMamba": ("Mamba neagră", "+{{bonus}}x daune de otravă din daunele hoților"),
    "lingeringToxin": ("Otravă persistentă", "Otrava ține cu +{{bonus}} secunde mai mult"),
    "smokeBomb": ("Bombă fumigenă", "Pune o capcană dragonului, cu {{current}}% șanse să se declanșeze"
                  " la următoarea lovitură și să o oprească."),
    "catBomb": ("Bombă cu pisici", "Proiectilul catapultei explodează la impact, daune duble."),
    "pickpocket": ("Pungaș", "+{{bonus}}x multiplicator la aurul produs de {{type}}"),
    "lockPick": ("Șperaclu", "Fiecare expediție începe cu {{bonus}} uși deja deschise."),
    "midasTouch": ("Atingerea lui Midas", "Încă +{{bonus}}x multiplicator la aurul produs de {{type}}"),
    "stuffedChests": ("Cufere îndesate", "+{{bonus}}% aur din cuferele temniței"),
    "tuningFork": ("Diapazon", "+{{bonus}} inspirație adunată"),
    "luteSolo": ("Solo de lăută", "+{{bonus}}x multiplicatorul maxim de inspirație"),
    "obnoxiousGuitarist": ("Chitarist sâcâitor", "Inspirația ține cu +{{bonus}} secunde mai mult"),
    "piercedEardrums": ("Timpane sparte", "Numărătoarea răgetului dragonului încetinește cu {{bonus}}%"),
    "replay": ("Bis", "{{bonus}}% șanse ca inspirația să înceapă din nou când se termină"),
    "sonicBarrier": ("Barieră sonică", "Numărătoarea focului dragonului încetinește cu {{bonus}}%"),
    "cacofonix": ("Cacofonix", "Îți amețește propriile trupe când îl cumperi"),
    "churchChoir": ("Cor bisericesc", "Recrutează 1 seminar de fiecare dată când pornește inspirația"),
    "encore": ("Encore", "Scurtează pauza inspirației cu {{bonus}} secunde"),
    "lockerRoomSpeech": ("Discurs în vestiar", "Produce inspirație cât timp jocul e închis,"
                         " la {{current}}% din ritm"),
    "orderInTheUk": ("Ordine în regat", "Cât timp jocul e închis, muzica ta îi face pe meșteșugari"
                     " să lucreze peste program și să producă resurse la {{current}}% din ritmul obișnuit"),
    "majorKey": ("Tonalitate majoră", "Cumpără o cheie de temniță. (Da, jocul de cuvinte e slab.)"),
    "vulnerableFrequencies": ("Frecvențe vulnerabile", "Dușmanii din temniță sunt nemuritori"
                              " cu {{bonus}} milisecunde mai puțin după fiecare lovitură"),
    "heroResources": ("Resurse umane pentru eroi", "+{{bonus}}% șanse să recrutezi de două ori mai mulți eroi"),
    "blessedAura": ("Aură binecuvântată", "Cu {{bonus}}% mai puține trupe mor din suflul de foc"),
    "blessedBird": ("Pasăre binecuvântată", "{{current}}% șanse ca o pasăre să apară binecuvântată"
                    " și să dea aur dublu"),
    "powerTransfer": ("Transfer de putere", "La fiecare recrutare, mana vrăjitorilor se umple cu"
                      " 0,5 pentru fiecare preot pe care îl ai"),
    "generousLoot": ("Pradă darnică", "Când o expediție eșuează, tot păstrezi {{current}}% din pradă."),
    "divineLight": ("Lumină divină", "+{{bonus}}% șanse să reaprinzi o torță stinsă"),
    "recruitWarriors": ("Recrutează războinici", "Îți permite să recrutezi războinici în luptă"),
    "recruitElves": ("Recrutează elfi", "Îți permite să recrutezi elfi în luptă"),
    "recruitWizards": ("Recrutează vrăjitori", "Îți permite să recrutezi vrăjitori în luptă"),
    "recruitBards": ("Recrutează barzi", "Îți permite să recrutezi barzi în luptă"),
    "recruitThieves": ("Recrutează hoți", "Îți permite să recrutezi hoți în luptă"),
    "recruitClerics": ("Recrutează preoți", "Îți permite să recrutezi preoți în luptă"),
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
    "huntingSeason.suffix": " păsări",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

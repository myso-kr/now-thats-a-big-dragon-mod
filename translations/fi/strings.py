# -*- coding: utf-8 -*-
"""The Finnish UI strings.

Address: "sinä", which is what Finnish games and software use. The polite plural would
make the King sound like a form letter rather than a monarch.

Finnish inflects rather than using prepositions, so a label is written in the case its
sentence asks for and not word by word from the English. A count above one takes the
partitive singular - "3 soturia", not the plural - which is why every unit name here is
given in that form rather than as a dictionary entry.

The game's own fonts draw every letter Finnish needs, so nothing of ours ships.
"""

T = {}

T.update({
    "upgrades.upgrades": "Parannukset",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Seuraava taso",
    "upgrades.currentLevel": "Nykyinen",
    "upgrades.newGamePlusOnly": "Vain luvussa \"Resurssien hallinta\"",
    "upgrades.max": "Maks",
    "upgrades.lockedMessage": "Paranna {{parentSkill}} lisää avataksesi tämän",
    "common.wishlistNow": "Lisää toivelistalle!",
})

T.update({
    "statistics.section.ttb": "Taisteluaika",
    "statistics.section.dgps": "Vahinko ja kulta sekunnissa",
    "statistics.section.resourceBalance": "Resurssitase",
    "statistics.lifetime.title": "Kokonaistilastot",
    "statistics.lifetime.totalPlaytime": "Peliaika yhteensä",
    "statistics.lifetime.totalGoldEarned": "Kultaa ansaittu yhteensä",
    "statistics.lifetime.totalGoldSpent": "Kultaa käytetty yhteensä",
    "statistics.lifetime.totalBirdsKilled": "Lintuja pudotettu yhteensä",
    "statistics.lifetime.totalClicks": "Napsautuksia yhteensä",
    "statistics.lifetime.totalHeroesRecruited": "Sankareita värvätty yhteensä",
    "statistics.lifetime.heroesPurchased": "Ostettu",
    "statistics.lifetime.heroesRecruited": "Värvätty",
    "statistics.lifetime.tier1": "Taso 1 värvätty (ostettu)",
    "statistics.lifetime.tier2": "Taso 2 värvätty (ostettu)",
    "statistics.lifetime.tier3": "Taso 3 värvätty (ostettu)",
    "statistics.lifetime.totalDamageDealt": "Vahinkoa tehty yhteensä",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Menetetty tulenhenkäykselle",
    "statistics.battleDuration": "Kulunut: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Voiko tämän edes voittaa?",
    "statistics.infiniteEstimatedVictory": "Todellinen voitto on mahdoton!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Olet sankarimme!</strong>];"
        " (0-1000000000)[Voitto <strong>{{count}} {{timePrefix}}</strong> kuluttua];"
        "(1000000001-inf)[<strong class='text-danger'>Napsauta tai paina Z hyökätäksesi lohikäärmeen kimppuun!</strong>]",
    "statistics.perSec": "/s",
    "statistics.generationSection": "Tuotanto",
    "statistics.critSection": "Erikoista",
    "statistics.dps": "Joukkojen vahinko: <strong>{{dps}}/s</strong>",
    "statistics.gps": "Joukkojen kulta: <strong>{{gps}}/s</strong>",
    "statistics.dpc": "Vahinko napsautusta kohti: <strong>{{dpc}}/napsautus</strong>",
    "statistics.gpc": "Kulta napsautusta kohti: <strong>{{gpc}}/napsautus</strong>",
    "statistics.catapultDamage": "Vahinko: <strong>{{damage}}/laukaus</strong>",
    "statistics.catapultTimeToShoot": "Seuraavaan laukaukseen: <strong>{{time}} s</strong>",
    "statistics.undo.disabledLine": "Napsauta 10 sekunnin kuluessa peruaksesi väärän oston"
        " ja saadaksesi kullat takaisin.",
    "statistics.undo.enabledAction": "Napsauta peruaksesi oston: {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Saat takaisin {{refund}}.",
    "statistics.undo.enabledTimer": "{{seconds}} sekuntia jäljellä.",
    "statistics.undo.refundGold": "{{amount}} kultaa",
})

# A count above one takes the partitive singular in Finnish, so "1 sekunti" but
# "3 sekuntia" - the plural would be wrong in both places.
for base, one, many in [
    ("seconds", "sekunti", "sekuntia"), ("minutes", "minuutti", "minuuttia"),
    ("hours", "tunti", "tuntia"), ("days", "päivä", "päivää"),
    ("months", "kuukausi", "kuukautta"), ("years", "vuosi", "vuotta"),
]:
    T[f"statistics.{base}_one"] = one
    T[f"statistics.{base}_other"] = many

T.update({
    "generators.generators": "Joukot",
    "generators.buy": "osta {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} s",
    "generators.ngPlusProductionToggle": "Kytke tuotanto päälle tai pois",
    "generators.tabs.troops": "Joukot",
    "generators.tabs.support": "Tuki",
    "generators.fireUnitsButton.tooltip": "Erota joukkoja kuluttaaksesi vähemmän resursseja"
        " ja säilyttääksesi silti osan tuotannosta.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Taikavoima velhojen hyökkäysten takana.",
    "generators.emptyManaDescription": "Osta \"Manavirta\" hyökätäksesi uudelleen.",
    "generators.inspiration": "Innoitus",
    "generators.inspirationDescription": "Kun se on käynnissä, kaikkien sankarien voima moninkertaistuu.",
    "generators.tabsAriaLabel": "joukkovälilehdet",
})

UNITS = {
    "warrior": ("Soturi", "Soturia"),
    "wizard": ("Velho", "Velhoa"),
    "elf": ("Haltia", "Haltiaa"),
    "garrison": ("Varuskunta", "Varuskuntaa"),
    "academy": ("Taikaopisto", "Taikaopistoa"),
    "academy_short": ("Opisto", "Opistoa"),
    "outpost": ("Jousimiesten etuvartio", "Jousimiesten etuvartiota"),
    "outpost_short": ("Etuvartio", "Etuvartiota"),
    "council": ("Sotaneuvosto", "Sotaneuvostoa"),
    "nexus": ("Arkkimaagien keskus", "Arkkimaagien keskusta"),
    "forest": ("Ikimetsä", "Ikimetsää"),
    "thief": ("Varas", "Varasta"),
    "bard": ("Bardi", "Bardia"),
    "cleric": ("Pappi", "Pappia"),
    "guild": ("Varkaiden kilta", "Varkaiden kiltaa"),
    "guild_short": ("Kilta", "Kiltaa"),
    "troupe": ("Kiertue", "Kiertuetta"),
    "troupe_short": ("Seurue", "Seuruetta"),
    "seminary": ("Pyhä seminaari", "Pyhää seminaaria"),
    "seminary_short": ("Seminaari", "Seminaaria"),
    "congress": ("Varjokokous", "Varjokokousta"),
    "theater": ("Suuri teatteri", "Suurta teatteria"),
    "college": ("Kardinaalikollegio", "Kardinaalikollegiota"),
    "catapult": ("Katapultti", "Katapulttia"),
    "builder": ("Rakentaja", "Rakentajaa"),
    "engineer": ("Insinööri", "Insinööriä"),
    "farmer": ("Maanviljelijä", "Maanviljelijää"),
    "lumberjack": ("Metsuri", "Metsuria"),
    "miner": ("Kaivosmies", "Kaivosmiestä"),
    "apprenticeships": ("Oppisopimus", "Oppisopimusta"),
    "tradespeople": ("Käsityöläinen", "Käsityöläistä"),
}
for base, (one, many) in UNITS.items():
    T[f"generators.{base}_one"] = one
    T[f"generators.{base}_other"] = many

T.update({
    "generators.unitDescription.warrior": "Sitkeitä lähitaistelijoita.",
    "generators.unitDescription.wizard": "Iskee keskimatkalta, mutta kestää vähän.",
    "generators.unitDescription.elf": "Ampuu ketterästi kaukaa, lohikäärmeen ulottumattomissa.",
    "generators.unitDescription.garrison": "Linnoitettu tukikohta, joka värvää sotureita.",
    "generators.unitDescription.outpost": "Syrjäinen tukikohta, joka värvää haltioita.",
    "generators.unitDescription.academy": "Koulu, joka kouluttaa velhoja taisteluun.",
    "generators.unitDescription.council": "Sotilasjärjestö, joka perustaa varuskuntia.",
    "generators.unitDescription.nexus": "Salaperäinen järjestö, joka perustaa opistoja.",
    "generators.unitDescription.forest": "Pyhä metsä, joka perustaa etuvartioita.",
    "generators.unitDescription.thief": "Ovela: myrkyttää lohikäärmeen ja varastaa sen kullat.",
    "generators.unitDescription.bard": "Voi innoittaa joukkosi taistelemaan kovemmin.",
    "generators.unitDescription.cleric": "Suojelee ja värvää uusia sankareita taisteluun.",
    "generators.unitDescription.guild": "Maanalainen verkosto, joka värvää varkaita.",
    "generators.unitDescription.troupe": "Kiertävä seurue, joka värvää bardeja.",
    "generators.unitDescription.seminary": "Pyhä laitos, joka kouluttaa pappeja.",
    "generators.unitDescription.congress": "Varjoissa toimiva järjestö, joka perustaa varkaiden kiltoja.",
    "generators.unitDescription.theater": "Mahtava laitos, joka perustaa kiertueita.",
    "generators.unitDescription.college": "Uskonnollinen järjestö, joka perustaa seminaareja.",
    "generators.unitDescription.catapult": "Piiritysase, joka tekee suurta vahinkoa lohikäärmeeseen.",
    "generators.unitDescription.builder": "Rakentaa toisen tason rakennuksia.",
    "generators.unitDescription.engineer": "Perustaa kolmannen tason järjestöjä.",
    "generators.unitDescription.farmer": "Viljelee ruokaa kuningaskunnalle.",
    "generators.unitDescription.lumberjack": "Kaataa puuta rakentamiseen.",
    "generators.unitDescription.miner": "Louhii malmia vuorilta.",
    "generators.unitDescription.apprenticeships": "Kouluttaa käsityöläisiä.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} vahinkoa/{{rate}} s",
    "wizard": "{{generatorGeneration}} vahinkoa/{{rate}} s",
    "elf": "{{generatorGeneration}} vahinkoa/{{rate}} s",
    "catapult": "{{generatorGeneration}} vahinkoa/{{rate}} s",
    "thief": "+{{generatorGeneration}} kultaa/{{rate}} s",
    "bard": "+{{generatorGeneration}} innoitusta/{{rate}} s",
    "cleric": "+{{generatorGeneration}} sankaria/{{rate}} s",
    "builder": "+{{generatorGeneration}} rakennusta/{{rate}} s",
    "engineer": "+{{generatorGeneration}} järjestöä/{{rate}} s",
    "farmer": "+{{generatorGeneration}} ruokaa/{{rate}} s",
    "lumberjack": "+{{generatorGeneration}} puuta/{{rate}} s",
    "miner": "+{{generatorGeneration}} malmia/{{rate}} s",
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
        "+{{generatorGeneration}} $t(" + ref + ', {"count": {{generatorGeneration}} })/{{rate}} s')

T.update({
    "settings.settings": "Asetukset",
    "settings.buy_max": "Osta maks",
    "settings.audio": "Musiikki ja äänet",
    "settings.game": "Peli",
    "settings.graphics": "Grafiikka",
    "settings.offline_progress": "Edistyminen offline-tilassa",
    "settings.wishlist_now": "Lisää toivelistalle",
    "menus.settings": "Asetukset",
    "menus.tabs.game": "Peli",
    "menus.tabs.graphics": "Grafiikka",
    "menus.tabs.audio": "Äänet",
    "menus.tabs.levels": "Luvut",
    "menus.tabs.credits": "Tekijät",
    "menus.credits.title": "Tekijät",
    "menus.credits.developedBy": "Kehittänyt",
    "menus.credits.developedWith": "Kehitetty käyttäen",
    "menus.credits.bigThanksTo": "Suuret kiitokset",
    "menus.credits.theRestOfTheDiscordServer": "kaikille muille Discord-palvelimella",
    "menus.credits.andYou": "ja sinulle!",
    "menus.music": "Musiikki",
    "menus.sfx": "Äänitehosteet",
    "menus.audioSettings": "Ääniasetukset",
    "menus.gameSettings": "Peliasetukset",
    "menus.graphicsSettings": "Grafiikka-asetukset",
    "menus.language": "Kieli",
    "menus.languages.en": "Englanti",
    "menus.languages.fr": "Ranska",
    "menus.languages.de": "Saksa",
    "menus.languages.pt": "Portugali",
    "menus.languages.tr": "Turkki",
    "menus.shakeIntensity": "Tärinä",
    "menus.largerTextSize": "Suurempi teksti",
    "menus.crtFilter": "CRT-suodatin",
    "menus.chromaticAberrationSlider": "Väripoikkeama",
    "menus.chromaticAberration": "Väripoikkeama",
    "menus.swordSwooshSounds": "Miekan ja kriittisten äänet",
    "menus.catSounds": "Kissan äänet",
    "menus.fullscreen": "Koko näyttö",
    "menus.resume": "Jatka pelaamista",
    "menus.close": "Sulje",
    "menus.quitGame": "Lopeta peli",
    "menus.joinDiscord": "Liity Discordiin",
    "menus.clear_save_label": "Poistetaanko edistymisesi?",
    "menus.zoom_adjustment": "Käyttöliittymän zoomaus",
    "menus.clear_save": "Poista nyt",
    "menus.are_you_sure": "Oletko varma?",
    "menus.cannot_be_reversed": "Tätä ei voi perua.",
    "menus.yes": "Kyllä",
    "menus.no": "Ei",
})

T.update({
    "tooltip.inspiration": "Innoitus",
    "tooltip.inspirationDescription": "Kun se on käynnissä, kaikkien sankarien voima moninkertaistuu.",
    "tooltip.maxInspiration": "Suurin kerroin",
    "tooltip.maxInspirationMultiplier": "Suurin kerroin",
    "tooltip.statisticsDescription": "Tarkat luvut edistymisestäsi ja taistelusta.",
    "tooltip.hudStopBird": "Pysäytä lintu",
    "tooltip.hudLifetimeStats": "Kokonaistilastot",
    "tooltip.hudHideWindows": "Piilota ikkunat",
    "tooltip.events.roar": "Lamauttava karjaisu",
    "tooltip.events.fire": "Tulenhenkäys",
    "tooltip.events.claw": "Kynsi-isku",
    "tooltip.events.dialog": "Erityinen tapahtuma",
    "tooltip.events.pope_visit": "Erityinen vieras",
    "tooltip.events.dungeon_keys": "Synkkä salaisuus",
    "tooltip.events.missing_king": "Missä kuningas on?",
    "tooltip.events.catapult": "Tekninen prototyyppi",
    "tooltip.events.engineer": "Apua oikeaan aikaan",
    "tooltip.events.invasion_start": "Hyökkäys on tulossa",
    "tooltip.events.invasion_end": "Viesti joukoilta",
    "tooltip.events.apprenticeships_unlock": "Oppisopimukset avattu",
    "tooltip.events.trading": "Kiertävä kauppias",
    "tooltip.events.dummy_toy_reveal": "Ei sitä mitä luulin",
})

T.update({
    "infos.banner.events": "Tapahtumat",
    "infos.banner.stats": "Tilastot",
    "infos.banner.engineering": "Tekniikka",
    "infos.banner.resources": "Resurssit",
    "infos.tabs.events": "Tapahtumat",
    "infos.tabs.stats": "Tilastot",
    "infos.tabs.engineering": "Tekniikka",
    "infos.tabs.resources": "Resurssit",
    "infos.tabsAriaLabel": "tietovälilehdet",
    "game.dummy": "Suuri puunukke",
    "game.infiniteBird": "Lintu jota ei saa alas",
    "game.king": "Kuningas",
    "game.smallDragon": "Tuth'orieth, Verso",
    "game.bigDragon": "Forth'aarh, Elämän antaja ja päättäjä",
    "dungeon.found": "Löydetty",
    "dungeon.giveUp": "Luovuta",
    "dungeon.tooltipDescription": "Tutki luolastoa (taso {{level}})",
    "dungeon.cooldownMessage": "Luolasto lepää. Odota {{seconds}} sekuntia päästäksesi takaisin.",
    "dungeon.cooldownShort": "{{seconds}} s",
    "dungeon.levelLabel": "Taso",
    "dungeon.levelShort": "Taso {{level}}",
    "dungeon.keysOwned": "Avaimia",
    "dungeon.giveUpTooltip": "Poistu luolastosta (osa saaliista jää Antelias saalis -parannuksella)",
    "dungeon.moveHint": "WASD tai nuolinäppäimet liikkumiseen",
    "dungeon.attackHint": "Napsauta hirviöitä hyökätäksesi",
    "dungeon.chestCountsTooltip": "{{opened}} / {{total}} arkkua avattu",
    "dungeon.exitDirection": "ULOSKÄYNTI",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Onnistunut retki",
    "summaries.dungeonLoot.titleFailed": "Epäonnistunut retki",
    "summaries.dungeonLoot.titleStuckRescue": "Päästiin turvallisesti ulos",
    "summaries.dungeonLoot.lootSummarySubtitle": "Yhteenveto saaliista",
    "summaries.dungeonLoot.body_one": "Saatiin {{gold}} kultaa ja {{grayKeys}} avain",
    "summaries.dungeonLoot.body_other": "Saatiin {{gold}} kultaa ja {{grayKeys}} avainta",
    "summaries.dungeonLoot.artifactFound": "Löytyi {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Tappiot tulenhenkäyksestä",
    "summaries.fireBreathCasualties.body": "Menetettiin {{list}}",
    "summaries.fireBreathCasualties.none": "Ei tappioita",
    "summaries.fireBreathBlocked.title": "Tulenhenkäys torjuttiin!",
    "summaries.fireBreathBlocked.body": "Savupommi pelasti joukkosi.",
    "summaries.toastLabel": "Pelin ilmoitus",
})

T.update({
    "levels.title": "Luvut",
    "levels.locked": "Lukittu",
    "levels.active": "Käynnissä",
    "levels.completed": "Suoritettu",
    "levels.continue": "Jatka",
    "levels.start": "Aloita",
    "levels.restart": "Pelaa uudelleen",
    "levels.restart_progress_warning": "Aloitetaanko uudelleen nyt?"
        " Menetät tallentamattoman edistymisen tässä luvussa.",
    "levels.names.mainGame": "Yksi suuri lohikäärme",
    "levels.names.newGamePlus": "Resurssien hallinta",
    "levels.names.dummy": "Taikalelu",
    "levels.names.infinite": "Todella loputon",
    "levels.names.kingBattle": "Kuninkaan viimeinen taistelu",
})

T.update({
    "menus.tabs.saveData": "Tallennustiedot",
    "menus.saveData.title": "Tallennustiedot",
    "menus.saveData.clearChapterTitle": "Lukujen edistyminen",
    "menus.saveData.clearChapterExplanation": "Poistaa kullan, joukot, parannukset, luolaston"
        " edistymisen ja suoritusmerkit jokaisesta luvusta. Avatut luvut, kokonaistilastot,"
        " asetukset ja esineet säilyvät.",
    "menus.saveData.clearChapterButton": "Poista lukujen edistyminen",
    "menus.saveData.clearFullTitle": "Kaikki tallennustiedot",
    "menus.saveData.clearFullExplanation": "Poistaa kaiken sen mitä lukujen nollaus poistaa,"
        " sekä lisäksi esineet, avatut luvut ja kokonaistilastot. Ääni-, grafiikka- ja"
        " kieliasetukset säilyvät.",
    "menus.saveData.clearFullButton": "Poista kaikki tallennustiedot",
    "menus.saveData.clearFullWarning": "Tätä ei voi perua. Menetät esineet, avatut luvut"
        " ja kokonaistilastot.",
})

T.update({
    "artifacts.title": "Esineet",
    "artifacts.subtitle": "Harvinaisia esineitä löytyy toisinaan luolaston erikoisarkuista."
        " Ne säilyvät luvusta toiseen.",
    "artifacts.notYetFound": "(ei vielä löydetty)",
})

ART = {
    "phoenixWhistle": ("Feeniksin pilli", "Erityinen lintu tuo mukanaan uuden rahan."),
    "emberforgedShield": ("Hiillostakottu kilpi", "Soturit kestävät lohikäärmeen tulen."),
    "moonwellFlask": ("Kuunlähteen pullo", "Velhot kuluttavat vain puolet manasta."),
    "windstepAnklet": ("Tuulenaskeleen nilkkarengas", "Haltiat eivät lamaannu."),
    "fangSatchel": ("Hammaslaukku", "Kierroksen ajan varkaat tuottavat lohikäärmeenhampaan puolessa tunnissa."),
    "slumberBerries": ("Uinumarjat", "Myrkky hidastaa lohikäärmeen karjaisua ja tulta 10 sekuntia."),
    "echoingLute": ("Kaikuva luuttu", "Bardit antavat kaksinkertaisen innoituksen."),
    "blessingCenser": ("Siunauksen suitsutusastia", "Papit värväävät aina kaksinkertaisen määrän."),
    "victoryTusk": ("Voitonsyöksyhammas", "Suoritettu taso antaa kaksinkertaiset lohikäärmeenhampaat."),
    "cartographersLedger": ("Kartantekijän kirja", "Näyttää kuinka moni luolaston arkku on avattu."),
    "ironSkeletonKey": ("Rautainen tiirikka", "Avaa luolaston tasolle 20 asti."),
    "everflameLantern": ("Ikiliekin lyhty", "Soihtu ei sammu koskaan."),
    "midasCoin": ("Midaan kolikko", "Kaksinkertainen kulta luolastossa."),
    "harvestIdol": ("Sadonjumalan patsas", "Resurssien tuotanto kasvaa 25 %."),
    "titanGauntlet": ("Titaanin rautahanska", "Kymmenkertainen vahinko napsautusta kohti."),
    "wayfindersCompass": ("Tienetsijän kompassi", "Osoittaa luolaston uloskäyntiin."),
    "loadedDice": ("Painotetut nopat", "Jokainen napsautus on kriittinen."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Rautasormi", "+{{bonus}} vahinkoa napsautusta kohti"),
    "featherFinger": ("Höyhensormi", "+{{bonus}} napsautusta sekunnissa"),
    "wakeupCall": ("Herätys", "Jokainen napsautus lyhentää lamaannusta {{bonus}} sekuntia"),
    "electricalFinger": ("Sähkösormi", "Jokaisella napsautuksella on {{bonus}} %:n mahdollisuus kutsua salama."),
    "perfectClick": ("Täydellinen napsautus", "+{{bonus}} % mahdollisuus kriittiseen napsautukseen"),
    "criticalStrike": ("Kriittinen isku", "+{{bonus}}x vahinko kriittisestä napsautuksesta"),
    "goldenExplosion": ("Kultainen räjähdys", "{{bonus}}x palkinto lintuja napsauttaessa"),
    "naturalLeader": ("Syntynyt johtaja", "Napsautukset täyttävät innoituspalkkia +{{bonus}}/napsautus"),
    "moneyCursor": ("Kultaosoitin", "{{bonus}}x kulta napsautusta kohti"),
    "fullChests": ("Täydet arkut", "{{bonus}} % pienempi mahdollisuus, että luolaston arkku on tyhjä"),
    "carpalCure": ("Ranteen hoito", "Pidä hiiren nappi pohjassa hyökätäksesi lohikäärmeeseen tauotta."),
    "shortSword": ("Lyhytmiekka", "+{{bonus}}x vahinkokerroin: {{type}}"),
    "longSword": ("Pitkämiekka", "Vielä +{{bonus}}x vahinkokerroin sotureille"),
    "twoHandedSword": ("Kaksikätinen miekka", "Jälleen +{{bonus}}x vahinkokerroin sotureille"),
    "battleShout": ("Taisteluhuuto", "Täyttää innoituspalkkia +{{bonus}} iskua kohti"),
    "warCry": ("Sotahuuto", "Käynnistää innoituksen itsestään seuraavalla tikillä,"
               " kun kerroin on suurimmillaan"),
    "barbarian": ("Barbaari", "+{{bonus}} perusvahinko"),
    "thickArmor": ("Paksu haarniska", "{{bonus}} % vähemmän fyysistä vahinkoa"),
    "fireArmor": ("Tulihaarniska", "{{bonus}} % vähemmän joukkoja kuolee tulenhenkäykseen"),
    "heavyRocks": ("Raskaat kivet", "+{{bonus}} % katapultin vahinkoa tasoa kohti"),
    "silverBlade": ("Hopeaterä", "+{{bonus}}x kerroin kultaan iskua kohti"),
    "goldenBlade": ("Kultaterä", "Vielä +{{bonus}}x kerroin kultaan iskua kohti"),
    "loyalMercenaries": ("Uskolliset palkkasoturit", "Ostamasi {{typePlural}} tekevät"
                         " +{{bonus}}x vahinkoa tasoa kohti"),
    "loyalServants": ("Uskolliset palvelijat", "{{type}} ja sitä ylemmät ovat {{bonus}} % halvempia värvätä"),
    "teamWork": ("Yhteistyö", "Värvää ylimääräisiä {{typePlural}} jokaista ostamaasi {{type}} kohti"),
    "dungeonPrecision": ("Tarkkuus syvyyksissä", "+{{bonus}} % mahdollisuus kriittiseen osumaan luolastossa"),
    "mazeCrusher": ("Labyrintin murskaaja", "+{{bonus}} kriittistä vahinkoa luolastossa"),
    "magicMissile": ("Taikaohjus", "+{{bonus}}x vahinkokerroin: {{type}}"),
    "manaSword": ("Manamiekka", "Jokainen velho lataa soturin miekan manalla."
                  " +{{bonus}}x vahinkokerroin, kun mana on yli 90"),
    "magicMouse": ("Taikahiiri", "Täyttää manapalkkia +{{bonus}} napsautusta kohti"),
    "manaSurge": ("Manavirta", "Täyttää velhojen manapalkin"),
    "manaPool": ("Manalähde", "+{{bonus}} % suurin mana"),
    "manaBoost": ("Manapurske", "Velhojen vahinko kaksinkertaistuu, kun mana on yli {{current}}"),
    "weatherForecast": ("Sääennuste", "+{{bonus}} % mahdollisuus salamaniskuun"),
    "lightningStrike": ("Salamanisku", "Lisää salaman, joka tekee +{{bonus}}x vahingon"
                        " lähteestä {{type}} jokaista ostettua parannusta kohti"),
    "silverStaff": ("Hopeasauva", "+{{bonus}}x kerroin kultaan iskua kohti"),
    "goldenStaff": ("Kultasauva", "Vielä +{{bonus}}x kerroin kultaan iskua kohti"),
    "magicFire": ("Taikatuli", "Soihtu palaa +{{bonus}} sekuntia pidempään"),
    "archimage": ("Arkkimaagi", "+{{bonus}} perusvahinko"),
    "huntersEye": ("Metsästäjän silmä", "+{{bonus}} % mahdollisuus osua kantaman sisällä olevaan lintuun tikkiä kohti"),
    "criticalChance": ("Tarkka tähtäys", "+{{bonus}} % mahdollisuus kriittiseen laukaukseen"),
    "criticalDamage": ("Lehdenleikkaaja", "+{{bonus}}x vahinko kriittisestä laukauksesta"),
    "huntingSeason": ("Metsästyskausi", "Kutsuu heti lintuparven"),
    "elvenEyes": ("Haltiansilmät", "Näet pimeässä vielä +{{bonus}} sekuntia soihdun sammuttua"),
    "multipleShot": ("Useampi nuoli", "Ampuu yhden nuolen lisää tasoa kohti"),
    "silverArrow": ("Hopeanuoli", "+{{bonus}}x kerroin kultaan iskua kohti"),
    "goldenArrow": ("Kultanuoli", "Vielä +{{bonus}}x kerroin kultaan iskua kohti"),
    "iceArrow": ("Jäänuoli", "Hidastaa lohikäärmeen tulta {{bonus}} sekuntia"),
    "animalInstinct": ("Eläimen vaisto", "Katapultti ampuu kissoja kivien sijaan"
                       " ja tiikereitä kissojen sijaan, joka kerta kymmenkertaisella vahingolla."),
    "lightningRod": ("Ukkosenjohdatin", "{{bonus}} % mahdollisuus vetää vielä yksi salama,"
                     " kun velhojen salama osuu."),
    "recycledArrows": ("Kierrätetyt nuolet", "Haltioiden hyökkäys kuluttaa vähemmän puuta"),
    "lightfoot": ("Kevytjalka", "+{{bonus}} % nopeampi liikkua ja kääntyä luolastossa"),
    "fastHands": ("Nopeat kädet", "Lyhentää kullan tuottamiseen kuluvaa aikaa {{bonus}} sekuntia"),
    "sharpDagger": ("Salamurhaajan terä", "Varkaat hyökkäävät myös, vahingolla {{current}}"),
    "poisonDagger": ("Myrkytetty tikari", "+{{bonus}} % mahdollisuus myrkyttää lohikäärme"),
    "blackMamba": ("Musta mamba", "+{{bonus}}x myrkkyvahinko varkaiden vahingosta"),
    "lingeringToxin": ("Viipyvä myrkky", "Myrkky kestää +{{bonus}} sekuntia pidempään"),
    "smokeBomb": ("Savupommi", "Virittää ansan lohikäärmeelle {{current}} %:n mahdollisuudella"
                  " lauketa seuraavalla iskulla ja torjua se."),
    "catBomb": ("Kissapommi", "Katapultin ammus räjähtää osuessaan, kaksinkertainen vahinko."),
    "pickpocket": ("Taskuvaras", "+{{bonus}}x kerroin kultaan jonka {{type}} tuottaa"),
    "lockPick": ("Tiirikka", "Jokainen retki alkaa {{bonus}} ovea jo auki."),
    "midasTouch": ("Midaan kosketus", "Vielä +{{bonus}}x kerroin kultaan jonka {{type}} tuottaa"),
    "stuffedChests": ("Täyteen ahdetut arkut", "+{{bonus}} % kultaa luolaston arkuista"),
    "tuningFork": ("Ääniraudan", "+{{bonus}} innoitusta kertyy"),
    "luteSolo": ("Luuttusoolo", "+{{bonus}}x suurin innoituskerroin"),
    "obnoxiousGuitarist": ("Sietämätön kitaristi", "Innoitus kestää +{{bonus}} sekuntia pidempään"),
    "piercedEardrums": ("Puhjenneet tärykalvot", "Lohikäärmeen karjaisulaskuri hidastuu {{bonus}} %"),
    "replay": ("Ylimääräinen", "{{bonus}} % mahdollisuus, että innoitus alkaa alusta sen loppuessa"),
    "sonicBarrier": ("Ääniaalto", "Lohikäärmeen tulilaskuri hidastuu {{bonus}} %"),
    "cacofonix": ("Kakofoniks", "Lamauttaa omat joukkosi, kun hänet ostaa"),
    "churchChoir": ("Kirkkokuoro", "Värvää 1 seminaarin joka kerta kun innoitus laukeaa"),
    "encore": ("Encore", "Lyhentää innoituksen taukoa {{bonus}} sekuntia"),
    "lockerRoomSpeech": ("Puhe pukuhuoneessa", "Tuottaa innoitusta pelin ollessa suljettuna,"
                         " {{current}} %:n tahdilla"),
    "orderInTheUk": ("Järjestys kuningaskunnassa", "Pelin ollessa suljettuna musiikkisi saa"
                     " käsityöläiset tekemään ylitöitä ja tuottamaan resursseja"
                     " {{current}} %:n tahdilla tavallisesta"),
    "majorKey": ("Duurisävellaji", "Ostaa yhden luolaston avaimen. (Kyllä, sanaleikki on kehno.)"),
    "vulnerableFrequencies": ("Haavoittuvat taajuudet", "Luolaston viholliset ovat kuolemattomia"
                              " {{bonus}} millisekuntia lyhemmän ajan jokaisen iskun jälkeen"),
    "heroResources": ("Sankarien henkilöstöosasto", "+{{bonus}} % mahdollisuus värvätä kaksinkertainen määrä"),
    "blessedAura": ("Siunattu aura", "{{bonus}} % vähemmän joukkoja kuolee tulenhenkäykseen"),
    "blessedBird": ("Siunattu lintu", "{{current}} % mahdollisuus, että lintu ilmestyy siunattuna"
                    " ja antaa kaksinkertaisen kullan"),
    "powerTransfer": ("Voimansiirto", "Jokaisella värväyksellä velhojen mana täyttyy 0,5"
                      " jokaista pappia kohti"),
    "generousLoot": ("Antelias saalis", "Kun retki epäonnistuu, saat silti pitää"
                     " {{current}} % saaliista."),
    "divineLight": ("Jumalallinen valo", "+{{bonus}} % mahdollisuus sytyttää sammunut soihtu uudelleen"),
    "recruitWarriors": ("Värvää sotureita", "Antaa värvätä sotureita taisteluun"),
    "recruitElves": ("Värvää haltioita", "Antaa värvätä haltioita taisteluun"),
    "recruitWizards": ("Värvää velhoja", "Antaa värvätä velhoja taisteluun"),
    "recruitBards": ("Värvää bardeja", "Antaa värvätä bardeja taisteluun"),
    "recruitThieves": ("Värvää varkaita", "Antaa värvätä varkaita taisteluun"),
    "recruitClerics": ("Värvää pappeja", "Antaa värvätä pappeja taisteluun"),
}
for k, (title, desc) in D.items():
    T[f"upgrades.details.{k}.title"] = title
    T[f"upgrades.details.{k}.description"] = desc

SUFFIX = {
    "wakeupCall.suffix": " s",
    "elvenEyes.suffix": " s",
    "iceArrow.suffix": " s",
    "lingeringToxin.suffix": " s",
    "obnoxiousGuitarist.suffix": " s",
    "encore.suffix": " s",
    "manaPool.suffix": " manaa",
    "manaBoost.suffix": " manaa",
    "huntingSeason.suffix": " lintua",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

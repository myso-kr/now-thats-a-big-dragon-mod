# -*- coding: utf-8 -*-
"""Writes the Hungarian .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: informal "te" throughout, the norm for Hungarian game dialogue. The King is
formal in tone but speaks to the hero directly.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Úgy tűnik, segítség kellene a több erőforrás előállításához...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Vegyél Inasképzést, hogy több földműves, bányász és favágó legyen.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Újra üdv!

# speaker:engineer
Tovább kutattuk az ostromgépedet.

# speaker:engineer
# wait:300
# pace:30
Most már macskákat is tud lőni az ellenségre, és szerintünk ez eldöntheti a harcot.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Úgy hívjuk: "Macs-katapult"

# speaker:engineer
# wait:300
# pace:300
(drámai szünet)

# speaker:engineer
# pace:30
Beruházol az átalakításba, a mostaniakra és a későbbiekre is?

* [Inkább maradok a kőnél]
    -> no_thanks

* [Fizess {catapultCostLabel} aranyat]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Meséld majd el, hogy tetszett!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Meséld majd el, hogy tetszett!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Kár. Azért sok szerencsét.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Az egységeid neked hagyták az utolsó csapást.

# speaker:king
# pace:30
- Itt az esély, hogy végleg leszámolj vele!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
A király kérte, hogy gyakorolj tovább, hátha jön valami nagyobb.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Ezúttal még a seregedet is finanszírozza, hogy kedvedre alakíthasd.

# speaker:princess
# pace:40
# chain_next
# wait:500
De amikor pár hónapja én kértem egy hatalmas szülinapi bulit,

# speaker:princess
# pace:40
# chain_next
# wait:500
csak ennyi volt...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, a királyságnak nincs pénze, lányom!"


# speaker:princess
# pace:37
Bár ez a bábu elég furán néz ki...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Mi? Nem hittem, hogy le lehet győzni.

# speaker:princess
# pace:20
# classes:love
De hát van bármi, amit a hősöm ne győzne le?

# speaker:princess
# events:whistle
# pace:50
Mi, mi az ott fent?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Ez nem egy egyszerű gyakorlóbábu.

# speaker:princess
# pace:30
Úgy néz ki, mint egy varázsjáték. Valami nálunk sokkal nagyobbnak.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hé, te ott...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Megtaláltam ezeket a kulcsokat a vár alatti titkos kazamatához.

# speaker:rogue
# pace:30
# wait:500
Vajon a király tud a létezéséről?

# speaker:rogue
# pace:10
# chain_next
# wait:500
Mindegy is...

# speaker:rogue
# pace:30
A menetek során szép zsákmányt szedtem össze, de legutóbb majdnem kialudt a fáklyám.

# speaker:rogue
# wait:500
Félek újra bemenni és eltévedni a sötétben, úgyhogy neked adom az összes kulcsot, ingyen.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Sok szerencsét,

# speaker:rogue
# pace:100
# events:end_give_keys
és vigyázz magadra.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hé! Én vagyok a fejlesztő.

# pace:40
Bocs, hogy átcsúsztál a falon. Az az én hibám.

# pace:30
Kivezetlek az űrből, és az egész zsákmányod megmarad.

* [Feladom és megtartom a zsákmányt]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Szia!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Üdv, hős!

# speaker:engineer
# pace:30
# events:show_engineering_tab
A harc segítésére Őfelsége elrendelte, hogy a Korona Építészeinek és Mérnökeinek Rendje bocsássa rendelkezésre a tudását.

# speaker:engineer
# pace:30
Háromféleképpen segítünk:

# speaker:engineer
# pace:30
- Ostromkatapultokat építünk.

# speaker:engineer
# pace:30
- Második szintű épületeket emelünk, az építőink kezével.

# speaker:engineer
# pace:30
- Magasabb szintű szervezeteket alapítunk, a mérnökeink kezével.

# speaker:engineer
# pace:30
Ha lesz rá aranyad, a "Mérnökség" fülön találsz minket.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ó, és mit hittél, mit jelent az, hogy "egységek elbocsátása"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Nem volt elég megölnöd? Kérlek, hagyj már békén!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Csip csip, te r*****!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Készen állok játszani az egységeidnek, hogy megsokszorozzam az erejüket.

# speaker:bard_dialog
# pace:35
# wait:400
Kattints a hárfa gombra, és élvezd az átmeneti erőnövekedést!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Segítség!

# speaker:king
# chain_next
# pace:30
# wait:500
Egy óriási sárkány pusztítja a falunkat!

# speaker:king
# wait:300
# pace:30
- Kell egy hős, aki megment minket.

# speaker:king
# pace:30
- Kérlek, öld meg ezt a sárkányt a hatalmas kardoddal, vagyis az egérmutatóddal.

# speaker:king
# pace:30
- És ha lesz elég aranyad, segítséget is toborozhatsz.

# speaker:king
# pace:30
- Sok szerencsét!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Valahogy Forth'aarh visszatért!

# speaker:king
# pace:30
# wait:400
De te elbocsátottad az egységeidet. Most újra kell toboroznod.

# speaker:king
# wait:300
# pace:30
- És az előző támadás tönkretette a gazdaságunkat, így nem tudom eltartani a sereged.

# speaker:king
# pace:40
# chain_next
- Mostantól fogyasztani fognak

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- élelmet, fát és ércet.

# speaker:king
# pace:40
- Jól kell gazdálkodnod az erőforrásokkal.

# speaker:king
# pace:40
- Kapcsold ki-be, melyik egység fogyasszon éppen erőforrást és melyik ne.

# speaker:king
# pace:40
- Vagy "bocsáss el" néhányat: kevesebbet fogyasztanak, de még dolgoznak valamennyit.

# speaker:king
# pace:28
- Sok szerencsét!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Sajnos az egységeink nem voltak elegen az invázió visszaveréséhez.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Mind egy szálig odavesztek, és velük a váltságdíj összege is.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Az egységek nagyszerű hírekkel tértek vissza!

# speaker:king
# pace:30
Minimális veszteséggel verték vissza az inváziót.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Visszavárjuk őket (hogy folytassuk a robotot a sárkány ellen...)

  -> END
"""

F["invasion_start.ink"] = r"""VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
A szomszédos királyság megtámadott minket.

# speaker:king
# pace:30
{ransomCostLabel} aranyat kérnek, hogy leállítsák az inváziót.

# speaker:king
# chain_next
# pace:30
# wait:500
Szerinted mit tegyünk?

* [Fizess {ransomCostLabel} aranyat]
    -> pay_enemy

* { unitsCountFew > 3 } [Védekezz {unitsCountFew} egységgel]
    -> send_few_units

* { unitsCountMany > 3 } [Védekezz {unitsCountMany} egységgel]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Reméljük, elfogadják az ajánlatunkat.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Reméljük, ennyi elég lesz.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Ez biztosan visszaveri a támadásukat.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Legalább... nem szegényen haltam meg.

# speaker:king
# pace:60
# classes:victory
Egyébként gratulálok a játék teljesítéséhez.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
MEGÖLTED AZ APÁMAT!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nem...

# speaker:developer
# pace:100
# classes:vader
Én vagyok az apád!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Fejlesztő?

# speaker:princess
# pace:50
Két Star Wars-utalást tettél a saját játékodba? Komolyan?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Megtaláltál.

# speaker:king
# pace:32
Igen, a sárkány odújából vittem el. Az aranyat a királyságnak. A játékot emlékbe.

# speaker:king
# pace:30
A népünk éhezett. Újra megtenném.

# speaker:king
# pace:30
Fogadd el a kenőpénzt és hallgass, és mindketten tisztán jövünk ki ebből.

# speaker:king
# pace:30
Elárulsz, vagy elfogadod az ajándékomat?

* [Meg kell állítani téged!]
  -> go_against_king

* [Szeretem az aranyat!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Legyen hát!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Akkor vedd el a részed.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Már több aranyat adtam, mint amennyire valaha vágytál.

# speaker:king
# pace:30
Ez volt az alku. Fogd és menj.

* [Nem érdekel, meg kell állítani téged]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Legyen hát!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Az én aranyamon vetted a sereget, amely megölte a kicsinyét.

# speaker:king
# pace:32
Ne tettesd magad ártatlannak.

# speaker:king
# pace:30
Gyere hát.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Szóval eladósodtál a koronánál, mi? Nyugi... a céhnek rengeteg balekja van, aki tartozik nekünk.


# speaker:rogue
# pace:40
# wait:400
Ha nem fizetnek, törünk pár lábat.

# speaker:rogue
# pace:30
# wait:400
Amíg vissza nem kerülsz pluszba, a tolvajaim kétszer olyan keményen gyűjtik neked az aranyat.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Jaj! A manakészletünk elfogyott.

# speaker:wizard_dialog
# pace:35
# wait:400
A titkos esszencia nélkül nem tudom a sárkányra irányítani a varázslataimat.

# speaker:wizard_dialog
# pace:35
# wait:400
Nézz be a fejlesztések menübe, és vedd meg a "Mana feltöltése" elemet, valahányszor kiszáradunk... hogy újra lecsaphassunk a fenevadra!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Látta valaki a királyt? Eltűnt.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Utoljára akkor látták, amikor a vár alatti kazamatákba indult.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Üdvözöllek!

# pace:45
Mook vagyok, az ifjú és igazságos!

# pace:50
A király állított ide, hogy el ne tévedj, és komolyan mondom: szeretek utat mutatni.

# pace:35
Erről a kőlapról nem léphetek le. "Segíts minden utazónak", aztán "ne lépd át azt a vonalat". Azzal nyugtattam magam, hogy ez a szabály. Mostanában... már nem vagyok biztos benne.

# pace:25
De tessék, fogd ezt a fáklyát. Ez az egyetlen segítség, amit még átnyújthatok a vonalon.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Üdvözöllek, én vagyok a pápa.

# speaker:pope
# pace:30
- Ideje ismét bizonyítanod a hitedet, és adakoznod az Egyházunknak.

# speaker:pope
# pace:30
- {contributionCostLabel} aranyra van szükségem a szegények megsegítéséhez.

* [Adj neki {contributionCostLabel} aranyat]
    -> pay_contribution

* [Válts vallást]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Nyerjen jutalmat a lelked a túlvilágon!

# speaker:pope
# pace:30
- Fogadd el ezt a 100 papot az Egyház hálájának jeléül.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Légyen átkozott a lelked a túlvilágon!

# speaker:pope
# pace:30
# chain_next
# wait:500
- És még valami...

# speaker:pope
# pace:30
- Kár lenne, ha azt az óriási gyíkot meggyógyítaná egy felsőbb hatalom...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(gyógyító hangok\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Van élelmem, fám vagy ércem eladó, ennyiért:

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
arany. Melyiket kéred?

* { canAffordTrading > 0 } [Élelem: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Fa: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Érc: {resourceAmountLabel}]
    -> buy_ore

* [Semmit]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== farewell ===

# speaker:salesman
A következő körnél találkozunk.

* [Ég veled]
    -> END

* [Gyere ritkábban]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Értem. Ritkábban jövök majd.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hűha, tényleg sikerült!

# speaker:king
# pace:30
- Nagyon köszönjük, hogy megölted azt a sárkányt. Te vagy a hősünk!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Végre végre...

# speaker:princess
# classes:scared
# pace:200
Mi volt ez a hang?

# speaker:shadow
# pace:200
# classes:angry
MEGÖLTÉTEK A FIAMAT!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Hát

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
EZ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
egy nagy sárkány!

# speaker:princess
# pace:20
# events:resume_game
Jaj ne, ugye segítesz nekünk?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh halott. Megtetted, amit egyetlen sereg sem tudott.

# speaker:king
# pace:28
# classes:victory
Köszönöm. Igazán.

# speaker:princess
# pace:30
# classes:victory
Gyere utánam... Fel kell készülnünk az újabb ellenségekre.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hogy jöhetett vissza?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Nem tudom, hogyan tért vissza.

# speaker:king
# pace:28
- De így felkelni elképesztő akaraterőt kíván.

# speaker:princess
# pace:40
# classes:scared
- És valamiféle bosszúvágyat is...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Tudtad, hogy valahányszor bemész egy kazamatába,

# classes:angry-worker
# pace:30
- NEKEM KELL KÉZZEL FELÉPÍTENEM EGY EGÉSZ ÚJ LABIRINTUST?!?

# chain_next
# pace:50
- Hetekig hordtuk fel a ládákat. Azt mondta, ne kérdezzük, honnan jöttek.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Végre!

# pace:40
- A király azt mondta, végeztem, és visszaadhatom a csákányt, amint befejezem ezt a szintet.

  -> END
"""

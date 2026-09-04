# -*- coding: utf-8 -*-
"""Writes the Romanian .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "tu" throughout. "dumneavoastră" would make the King sound like a ministry
rather than a monarch; he is grand in tone, not in pronoun.

The comma-below letters are Ș/ș and Ț/ț, not the cedilla forms Ş/ş and Ţ/ţ - a
different pair of code points that Romanian typography has moved away from, and the
only ones the extended fonts carry.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Se pare că ai nevoie de ajutor ca să faci mai multe resurse...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Încearcă să cumperi Ucenicii ca să ai mai mulți fermieri, mineri și tăietori de lemne.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ne revedem!

# speaker:engineer
Am continuat să lucrăm la arma ta de asediu.

# speaker:engineer
# wait:300
# pace:30
Acum poate arunca pisici în dușman, și credem că răstoarnă toată lupta.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Îi spunem "Pisicapulta"

# speaker:engineer
# wait:300
# pace:300
(o pauză de efect)

# speaker:engineer
# pace:30
Vrei să plătești îmbunătățirea, și pentru asta, și pentru toate care urmează?

* [Prefer să arunc cu bolovani]
    -> no_thanks

* [Plătește {catapultCostLabel} aur]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Spune-ne ce părere ai!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Spune-ne ce părere ai!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Păcat. Mult noroc oricum.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Trupele tale ți-au păstrat ție lovitura de final.

# speaker:king
# pace:30
- Asta e șansa ta să-i pui capăt pentru totdeauna!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Tata zice să te ții de antrenament, în caz că vine ceva mai mare.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
De data asta chiar îți plătește trupele, așa că le poți așeza cum vrei.

# speaker:princess
# pace:40
# chain_next
# wait:500
Și totuși, când am cerut acum câteva luni o petrecere mare de ziua mea,

# speaker:princess
# pace:40
# chain_next
# wait:500
n-am auzit decât...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, regatul n-are bani, fata mea!"


# speaker:princess
# pace:37
Apropo, păpușa aia de lemn arată ciudat...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Poftim? Nici nu credeam că poate fi doborâtă.

# speaker:princess
# pace:20
# classes:love
Dar ce nu poate face eroul meu?

# speaker:princess
# events:whistle
# pace:50
Ce e aia acolo sus?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Aia nu e o păpușă obișnuită de antrenament.

# speaker:princess
# pace:30
Arată ca o jucărie fermecată. Făcută pentru ceva mult mai mare decât noi.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hei, tu de colo...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Am găsit niște chei de la temnița secretă de sub castel.

# speaker:rogue
# pace:30
# wait:500
Nici nu știu dacă regele are habar că există.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Dar lasă...

# speaker:rogue
# pace:30
Am scos destule de acolo, însă data trecută mai că mi s-a stins torța.

# speaker:rogue
# wait:500
Nu îndrăznesc să cobor iar și să mă rătăcesc în beznă, așa că îți dau cheile. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Mult noroc,

# speaker:rogue
# pace:100
# events:end_give_keys
și ai grijă de tine.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Salut! Eu am făcut jocul ăsta.

# pace:40
Îmi pare rău că ai căzut prin perete. E vina mea.

# pace:30
Te scot din gol, și rămâi cu toată prada.

* [Renunță și păstrează prada]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Pa!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Salutare, eroule!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Ca să ajute în luptă, Majestatea Sa a poruncit Breslei Regale a Arhitecților și Inginerilor să-ți pună priceperea noastră la dispoziție.

# speaker:engineer
# pace:30
Te ajutăm în trei feluri:

# speaker:engineer
# pace:30
- Facem catapulte pentru asediu.

# speaker:engineer
# pace:30
- Ridicăm clădiri de nivelul al doilea, prin constructorii noștri.

# speaker:engineer
# pace:30
- Înființăm organizații de nivel superior, prin inginerii noștri.

# speaker:engineer
# pace:30
Caută-ne la fila "Inginerie" când ai destul aur.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ei, ce credeai că înseamnă "concedierea trupelor"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Nu ți-a ajuns că m-ai ucis? Lasă-mă în pace!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Cip cip, nemern**ule!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Sunt gata să cânt pentru trupele tale și să le trezesc puterea.

# speaker:bard_dialog
# pace:35
# wait:400
Apasă butonul cu harpa și bucură-te de o vreme de putere în plus!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Ajutor!

# speaker:king
# chain_next
# pace:30
# wait:500
Un dragon uriaș ne distruge satul!

# speaker:king
# wait:300
# pace:30
- Avem nevoie de un erou care să ne salveze.

# speaker:king
# pace:30
- Te rog, ucide dragonul cu sabia ta puternică, adică, cu cursorul mouse-ului.

# speaker:king
# pace:30
- Și dacă ai destul aur, poți recruta și pe alții care să te ajute.

# speaker:king
# pace:30
- Mult noroc!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Cumva, Forth'aarh s-a întors!

# speaker:king
# pace:30
# wait:400
Dar tu ți-ai desființat trupele. Acum trebuie să le recrutezi din nou.

# speaker:king
# wait:300
# pace:30
- Iar atacul de data trecută a golit vistieria, așa că nu-ți pot întreține trupele.

# speaker:king
# pace:40
# chain_next
- De acum înainte consumă

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- hrană, lemn și minereu.

# speaker:king
# pace:40
- Va trebui să chibzuiești resursele.

# speaker:king
# pace:40
- Pornește și oprește cine primește resurse și cine nu.

# speaker:king
# pace:40
- Sau "concediază" o parte: consumă mai puțin și tot fac ceva.

# speaker:king
# pace:28
- Mult noroc!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Din păcate, trupele noastre n-au fost de ajuns ca să respingă invazia.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Am pierdut toate trupele, și răscumpărarea pe deasupra.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Trupele noastre s-au întors cu vești bune!

# speaker:king
# pace:30
Au respins invazia cu pierderi mici.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Le primesc înapoi (ca să se întoarcă la dragon...)

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
Regatul vecin ne atacă.

# speaker:king
# pace:30
Cer {ransomCostLabel} aur ca să oprească invazia.

# speaker:king
# chain_next
# pace:30
# wait:500
Tu ce crezi că ar trebui să facem?

* [Plătește {ransomCostLabel} aur]
    -> pay_enemy

* { unitsCountFew > 3 } [Apără-te cu {unitsCountFew} trupe]
    -> send_few_units

* { unitsCountMany > 3 } [Apără-te cu {unitsCountMany} trupe]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Să sperăm că primesc oferta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Să sperăm că e de ajuns.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Atâția îi resping cu siguranță.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Măcar... n-am murit sărac.

# speaker:king
# pace:60
# classes:victory
Apropo, felicitări că ai terminat jocul.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
MI-AI UCIS TATĂL!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nu...

# speaker:developer
# pace:100
# classes:vader
Eu sunt tatăl tău!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Tu, cel care a făcut jocul?

# speaker:princess
# pace:50
Ai pus două replici din Star Wars în propriul tău joc? Pe bune?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Deci m-ai găsit.

# speaker:king
# pace:32
Da, l-am luat din vizuina dragonului. Aurul pentru regat. Jucăria ca amintire.

# speaker:king
# pace:30
Poporul meu flămânzea. Aș face-o din nou.

# speaker:king
# pace:30
Ia o mită și taci, și scăpăm amândoi de necaz.

# speaker:king
# pace:30
Mă trădezi, sau primești darul meu?

* [Cineva trebuie să te oprească!]
  -> go_against_king

* [Și mie îmi place aurul!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Fie și așa!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Atunci ia-ți partea.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Ți-am dat mai mult aur decât ai visat vreodată.

# speaker:king
# pace:30
Asta a fost înțelegerea. Ia-l și pleacă.

* [Nu contează, trebuie oprit]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Fie și așa!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Cu aurul meu ai cumpărat oastea care i-a ucis puiul.

# speaker:king
# pace:32
Nu te mai preface nevinovat.

# speaker:king
# pace:30
Atunci, hai.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Deci ai datorii la regat? Calm... breasla e plină de datornici.


# speaker:rogue
# pace:40
# wait:400
Dacă nu plătești, se rup niște picioare.

# speaker:rogue
# pace:30
# wait:400
Până ieși din minus, hoții mei îți strâng aur de două ori mai mult.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Vai! Rezerva noastră de mana s-a golit.

# speaker:wizard_dialog
# pace:35
# wait:400
Fără puterea aceea tainică nu pot arunca nimic spre dragon.

# speaker:wizard_dialog
# pace:35
# wait:400
Du-te la îmbunătățiri și cumpără "Val de mana" ori de câte ori rămânem fără... ca să lovim iar bestia!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
A văzut cineva regele? Tatăl meu a dispărut.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Ultima dată a fost văzut coborând în temnița de sub castel.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Bine ai venit!

# pace:45
Sunt Mook, tânăr și drept!

# pace:50
Regele m-a pus aici ca să nu te rătăcești, și o spun pe față: îmi place să arăt drumul.

# pace:35
Nu am voie să ies din pătratul ăsta. "Ajută pe oricine trece", și apoi "nu trece de linia aceea". Îmi spun că astea sunt regulile. În ultima vreme... nu mai sunt așa sigur.

# pace:25
Dar uite, ia torța asta. E singurul lucru pe care am voie să-l dau peste linie.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Fii binecuvântat, copile. Eu sunt Papa.

# speaker:pope
# pace:30
- E vremea să-ți arăți din nou credința și să dai un dar Bisericii.

# speaker:pope
# pace:30
- Am nevoie de {contributionCostLabel} aur ca să-i ajut pe săraci.

* [Dă-i {contributionCostLabel} aur]
    -> pay_contribution

* [Schimbă religia]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Fie ca sufletul tău să fie răsplătit pe lumea cealaltă!

# speaker:pope
# pace:30
- Primește acești 100 de preoți ca mulțumire din partea Bisericii.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Fie ca sufletul tău să fie blestemat pe lumea cealaltă!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Și apropo...

# speaker:pope
# pace:30
- Ar fi păcat ca șopârla aceea uriașă să fie vindecată de o putere mai înaltă...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(sunete de vindecare\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Vând hrană, lemn sau minereu cu

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
aur. Ce dorești?

* { canAffordTrading > 0 } [Hrană: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Lemn: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Minereu: {resourceAmountLabel}]
    -> buy_ore

* [Nimic, mulțumesc]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== farewell ===

# speaker:salesman
Ne vedem data viitoare.

* [La revedere]
    -> END

* [Vino mai rar]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Am înțeles. Vin mai rar.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Chiar ai reușit!

# speaker:king
# pace:30
- Îți mulțumesc că ai ucis dragonul. Ești eroul nostru!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
În sfârșit putem...

# speaker:princess
# classes:scared
# pace:200
Ce a fost asta?

# speaker:shadow
# pace:200
# classes:angry
MI-AȚI UCIS PUIUL!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
ĂSTA

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
DA

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
că e un dragon mare!

# speaker:princess
# pace:20
# events:resume_game
Vai, ne ajuți?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh e mort. Ai făcut ce nicio oaste n-a putut.

# speaker:king
# pace:28
# classes:victory
Îți mulțumesc. Din suflet.

# speaker:princess
# pace:30
# classes:victory
Vino cu mine... Trebuie să ne pregătim pentru dușmanii care ar putea urma.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Cum a putut să se întoarcă?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Nu știu cum s-a întors.

# speaker:king
# pace:28
- Dar să te ridici așa din nou cere o voință ieșită din comun.

# speaker:princess
# pace:40
# classes:scared
- Și o sete de răzbunare...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Știi că de fiecare dată când cobori în temniță

# classes:angry-worker
# pace:30
- TREBUIE SĂ RIDIC UN LABIRINT NOU CU MÂNA?!?

# chain_next
# pace:50
- Cărăm cufere de săptămâni întregi. Ne-a zis să nu întrebăm de unde vin.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
În sfârșit gata!

# pace:40
- Regele a zis că am terminat și că pot da târnăcopul înapoi după ce iese nivelul ăsta.

  -> END
"""

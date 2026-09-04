# -*- coding: utf-8 -*-
"""Writes the Swedish .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "du" throughout - Swedish has spoken to everyone that way since the
du-reformen, and "ni" to one person now reads as either archaic or arch. The King is
formal in tone rather than in form: he asks and thanks rather than commands.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Du verkar behöva hjälp att få fram mer resurser...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Prova att köpa Lärlingsplatser för fler bönder, gruvarbetare och skogshuggare.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Vi ses igen!

# speaker:engineer
Vi har forskat vidare på ditt belägringsvapen.

# speaker:engineer
# wait:300
# pace:30
Nu kan den skjuta katter på fienden, och vi tror att den vänder hela striden.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kallar den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en konstpaus)

# speaker:engineer
# pace:30
Vill du bekosta uppgraderingen, för den du har och för alla som kommer?

* [Jag skjuter hellre sten]
    -> no_thanks

* [Betala {catapultCostLabel} guld]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Berätta gärna vad du tycker!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Berätta gärna vad du tycker!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Vad synd. Lycka till ändå.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Dina trupper har sparat det sista slaget åt dig.

# speaker:king
# pace:30
- Här är din chans att göra slut på den för gott!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Far säger att du ska fortsätta träna, ifall något större dyker upp.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Den här gången betalar han till och med för dina trupper, så du får ställa upp dem som du vill.

# speaker:princess
# pace:40
# chain_next
# wait:500
Och ändå, när jag bad om ett riktigt stort födelsedagskalas för några månader sedan,

# speaker:princess
# pace:40
# chain_next
# wait:500
fick jag bara höra...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, kungariket har inga pengar, dotter!"


# speaker:princess
# pace:37
Den där trädockan ser förresten konstig ut...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Va? Jag trodde inte ens att den gick att fälla.

# speaker:princess
# pace:20
# classes:love
Men finns det något min hjälte inte klarar?

# speaker:princess
# events:whistle
# pace:50
Vad är det där uppe?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Det där är ingen vanlig träningsdocka.

# speaker:princess
# pace:30
Den ser ut som en magisk leksak. Gjord för något mycket större än oss.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Du där...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Jag hittade några nycklar till den hemliga fängelsehålan under slottet.

# speaker:rogue
# pace:30
# wait:500
Jag vet inte ens om kungen vet att den finns.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Men strunt i det...

# speaker:rogue
# pace:30
Jag har fått med mig en hel del därifrån, men förra gången höll facklan på att slockna.

# speaker:rogue
# wait:500
Jag vågar inte gå ner och gå vilse i mörkret, så du får nycklarna. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Lycka till,

# speaker:rogue
# pace:100
# events:end_give_keys
och var försiktig.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hej! Det är jag som gjort spelet.

# pace:40
Ledsen att du gick igenom en vägg. Det är mitt fel.

# pace:30
Jag hjälper dig ut ur tomrummet, och du får behålla allt bytet.

* [Ge upp och behåll bytet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Hej då!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
God dag, hjälte!

# speaker:engineer
# pace:30
# events:show_engineering_tab
För att hjälpa till i striden har Hans Majestät befallt Kungliga arkitekt- och ingenjörsgillet att ställa vårt kunnande till ditt förfogande.

# speaker:engineer
# pace:30
Vi hjälper dig på tre sätt:

# speaker:engineer
# pace:30
- Vi bygger katapulter till belägringen.

# speaker:engineer
# pace:30
- Vi reser byggnader på andra nivån, genom våra byggare.

# speaker:engineer
# pace:30
- Vi upprättar organisationer på högre nivåer, genom våra ingenjörer.

# speaker:engineer
# pace:30
Sök upp oss under fliken "Teknik" när du har guld nog.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Nå, vad trodde du att "avskeda trupper" betydde?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Räckte det inte att döda mig? Låt mig vara i fred!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Pip pip, ditt kr**!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Jag är redo att spela för dina trupper och väcka deras kraft.

# speaker:bard_dialog
# pace:35
# wait:400
Tryck på harpknappen och njut av en stunds extra styrka!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Hjälp!

# speaker:king
# chain_next
# pace:30
# wait:500
En jättelik drake förstör vår by!

# speaker:king
# wait:300
# pace:30
- Vi behöver en hjälte som räddar oss.

# speaker:king
# pace:30
- Var snäll och döda draken med ditt mäktiga svärd, jag menar, med din muspekare.

# speaker:king
# pace:30
- Och har du guld nog kan du värva fler som hjälper till.

# speaker:king
# pace:30
- Lycka till!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Forth'aarh är tillbaka, på något vis!

# speaker:king
# pace:30
# wait:400
Men du har upplöst dina trupper. Nu får du värva dem igen.

# speaker:king
# wait:300
# pace:30
- Och förra anfallet ruinerade skattkammaren, så jag kan inte försörja dina trupper.

# speaker:king
# pace:40
# chain_next
- Härefter förbrukar de

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- mat, trä och malm.

# speaker:king
# pace:40
- Du får hushålla med resurserna.

# speaker:king
# pace:40
- Slå av och på för att välja vilka som får resurser och vilka som inte får det.

# speaker:king
# pace:40
- Eller "avskeda" en del: de förbrukar mindre och gör ändå något.

# speaker:king
# pace:28
- Lycka till!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Tyvärr räckte inte våra trupper till för att slå tillbaka invasionen.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jag förlorade alla trupperna, och lösensumman därtill.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Trupperna är tillbaka med goda nyheter!

# speaker:king
# pace:30
De slog tillbaka invasionen med små förluster.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jag tar emot dem (så att de kan gå tillbaka till draken...)

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
Grannriket anfaller oss.

# speaker:king
# pace:30
De begär {ransomCostLabel} guld för att avbryta invasionen.

# speaker:king
# chain_next
# pace:30
# wait:500
Vad tycker du att vi ska göra?

* [Betala {ransomCostLabel} guld]
    -> pay_enemy

* { unitsCountFew > 3 } [Försvara med {unitsCountFew} trupper]
    -> send_few_units

* { unitsCountMany > 3 } [Försvara med {unitsCountMany} trupper]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Låt oss hoppas att de tar erbjudandet.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Låt oss hoppas att det räcker.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Så många slår helt säkert tillbaka dem.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Åtminstone... dog jag inte fattig.

# speaker:king
# pace:60
# classes:victory
Grattis ändå till att du klarat spelet.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
DU DÖDADE MIN FAR!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nej...

# speaker:developer
# pace:100
# classes:vader
Jag är din far!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Du som gjorde spelet?

# speaker:princess
# pace:50
Satte du två Star Wars-repliker i ditt eget spel? På allvar?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Så du hittade mig.

# speaker:king
# pace:32
Ja, jag tog det ur drakens håla. Guldet åt kungariket. Leksaken som minne.

# speaker:king
# pace:30
Mitt folk svälter. Jag skulle göra om det.

# speaker:king
# pace:30
Ta en muta och tig, så slipper vi båda besvär.

# speaker:king
# pace:30
Förråder du mig, eller tar du emot min gåva?

* [Någon måste stoppa dig!]
  -> go_against_king

* [Jag gillar också guld!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Nåväl!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ta då din del.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Jag har gett dig mer guld än du någonsin drömt om.

# speaker:king
# pace:30
Det var uppgörelsen. Ta det och gå.

* [Strunt samma, du måste stoppas]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Nåväl!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Du köpte hären som dödade hennes unge med mitt guld.

# speaker:king
# pace:32
Låtsas inte vara oskyldig.

# speaker:king
# pace:30
Kom an, då.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Så du är skyldig kungariket pengar? Lugn... gillet har gott om gäldenärer.


# speaker:rogue
# pace:40
# wait:400
Betalar du inte går det sönder några ben.

# speaker:rogue
# pace:30
# wait:400
Tills du är på plus igen samlar mina tjuvar dubbelt så mycket guld åt dig.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Ack! Vårt manaförråd är slut.

# speaker:wizard_dialog
# pace:35
# wait:400
Utan den mystiska kraften kan jag inte kasta något mot draken.

# speaker:wizard_dialog
# pace:35
# wait:400
Gå till uppgraderingarna och köp "Manaflöde" när vi är tomma... så slår vi till mot odjuret igen!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Har någon sett kungen? Min far är försvunnen.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Sist han syntes var han på väg ner i fängelsehålan under slottet.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Välkommen!

# pace:45
Jag är Mook, ung och rättrådig!

# pace:50
Kungen satte mig här så att du inte ska gå vilse, och jag säger som det är: jag tycker om att visa vägen.

# pace:35
Jag får inte lämna den här rutan. "Hjälp alla som passerar", och sedan "gå inte över den linjen". Jag säger till mig själv att det är reglerna. På sistone... är jag inte lika säker.

# pace:25
Men här, ta den här facklan. Det är det enda jag får skicka över linjen.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Hälsningar, mitt barn. Jag är påven.

# speaker:pope
# pace:30
- Det är dags att visa din tro igen och ge en gåva till Kyrkan.

# speaker:pope
# pace:30
- Jag behöver {contributionCostLabel} guld för att hjälpa de fattiga.

* [Ge honom {contributionCostLabel} guld]
    -> pay_contribution

* [Byt religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Må din själ bli belönad i nästa liv!

# speaker:pope
# pace:30
- Ta emot dessa 100 präster som Kyrkans tack.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Må din själ bli förbannad i nästa liv!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Och förresten...

# speaker:pope
# pace:30
- Det vore synd om den där jättelika ödlan blev helad av en högre makt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helande ljud\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jag säljer mat, trä eller malm för

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
guld. Vad vill du ha?

* { canAffordTrading > 0 } [Mat: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Trä: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ingenting, tack]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== farewell ===

# speaker:salesman
Vi ses nästa gång.

* [Adjö]
    -> END

* [Kom mer sällan]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Uppfattat. Jag kommer mer sällan.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Du gjorde det verkligen!

# speaker:king
# pace:30
- Tack för att du dödade draken. Du är vår hjälte!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Äntligen kan vi...

# speaker:princess
# classes:scared
# pace:200
Vad var det där?

# speaker:shadow
# pace:200
# classes:angry
NI DÖDADE MITT BARN!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
NU

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ÄR DET

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
en stor drake!

# speaker:princess
# pace:20
# events:resume_game
Åh nej, hjälper du oss?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh är död. Du gjorde det ingen här kunde göra.

# speaker:king
# pace:28
# classes:victory
Tack. Uppriktigt.

# speaker:princess
# pace:30
# classes:victory
Följ med mig... Vi måste rusta oss för de fiender som kan komma härnäst.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hur kunde den komma tillbaka?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Jag vet inte hur den återvände.

# speaker:king
# pace:28
- Men att resa sig igen så där kräver en ovanlig vilja.

# speaker:princess
# pace:40
# classes:scared
- Och en hunger efter hämnd...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Vet du att varje gång du går ner i fängelsehålan

# classes:angry-worker
# pace:30
- FÅR JAG BYGGA EN HEL NY LABYRINT FÖR HAND?!?

# chain_next
# pace:50
- Vi har burit upp kistor i veckor. Han sa åt oss att inte fråga var de kom ifrån.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Äntligen klart!

# pace:40
- Kungen sa att jag är färdig och att jag får lämna tillbaka hackan när den här nivån är klar.

  -> END
"""

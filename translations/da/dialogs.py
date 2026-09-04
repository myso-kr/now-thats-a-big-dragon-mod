# -*- coding: utf-8 -*-
"""Writes the Danish .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "du" throughout. Danish dropped "De" for ordinary use long ago, and a King who
used it would sound like a letter from the tax office rather than a monarch. He is
grand in tone, not in pronoun.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Du kunne vist godt bruge hjælp til at skaffe flere ressourcer...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Prøv at købe Lærlingepladser for at få flere bønder, minearbejdere og skovhuggere.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Der er du igen!

# speaker:engineer
Vi har arbejdet videre på dit belejringsvåben.

# speaker:engineer
# wait:300
# pace:30
Nu kan den skyde katte mod fjenden, og vi tror, den vender hele kampen.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kalder den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en kunstpause)

# speaker:engineer
# pace:30
Vil du betale for forbedringen, både til den her og til alle de næste?

* [Jeg skyder hellere med sten]
    -> no_thanks

* [Betal {catapultCostLabel} guld]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Sig endelig, hvad du synes!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Sig endelig, hvad du synes!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Ærgerligt. Held og lykke alligevel.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Dine tropper har gemt det sidste slag til dig.

# speaker:king
# pace:30
- Her er din chance for at gøre en ende på den for altid!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Far siger, du skal blive ved med at træne, hvis nu der kommer noget større.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Denne gang betaler han endda for dine tropper, så du må stille dem op, som du vil.

# speaker:princess
# pace:40
# chain_next
# wait:500
Og alligevel, da jeg for et par måneder siden bad om en rigtig stor fødselsdagsfest,

# speaker:princess
# pace:40
# chain_next
# wait:500
fik jeg bare at vide...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, kongeriget har ingen penge, datter!"


# speaker:princess
# pace:37
Den trædukke ser i øvrigt underlig ud...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Hvad? Jeg troede ikke engang, den kunne fældes.

# speaker:princess
# pace:20
# classes:love
Men hvad kan min helt egentlig ikke?

# speaker:princess
# events:whistle
# pace:50
Hvad er det deroppe?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Det er ingen almindelig træningsdukke.

# speaker:princess
# pace:30
Den ligner et magisk legetøj. Lavet til noget, der er meget større end os.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hey, dig der...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Jeg har fundet et par nøgler til det hemmelige fangehul under slottet.

# speaker:rogue
# pace:30
# wait:500
Jeg ved ikke engang, om kongen ved, at det findes.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Men pyt...

# speaker:rogue
# pace:30
Jeg har fået en del med derfra, men sidste gang var min fakkel lige ved at gå ud.

# speaker:rogue
# wait:500
Jeg tør ikke ned og fare vild i mørket, så du får nøglerne. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Held og lykke,

# speaker:rogue
# pace:100
# events:end_give_keys
og pas på dig selv.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hej! Det er mig, der har lavet spillet.

# pace:40
Undskyld, du faldt gennem en væg. Det er min skyld.

# pace:30
Jeg får dig ud af tomrummet, og du beholder hele byttet.

* [Giv op og behold byttet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Farvel!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Goddag, helt!

# speaker:engineer
# pace:30
# events:show_engineering_tab
For at hjælpe i kampen har Hans Majestæt befalet Det Kongelige Arkitekt- og Ingeniørlaug at stille vores kunnen til din rådighed.

# speaker:engineer
# pace:30
Vi hjælper dig på tre måder:

# speaker:engineer
# pace:30
- Vi bygger katapulter til belejringen.

# speaker:engineer
# pace:30
- Vi rejser bygninger på andet niveau gennem vores bygmestre.

# speaker:engineer
# pace:30
- Vi opretter organisationer på højere niveauer gennem vores ingeniører.

# speaker:engineer
# pace:30
Find os under fanen "Teknik", når du har guld nok.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Nå, hvad troede du, "afskedig tropper" betød?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Var det ikke nok at slå mig ihjel? Lad mig dog være!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Pip pip, dit r**hul!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Jeg er klar til at spille for dine tropper og vække deres kraft.

# speaker:bard_dialog
# pace:35
# wait:400
Tryk på harpeknappen og nyd et stykke tid med ekstra styrke!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Hjælp!

# speaker:king
# chain_next
# pace:30
# wait:500
En kæmpestor drage ødelægger vores landsby!

# speaker:king
# wait:300
# pace:30
- Vi har brug for en helt, der redder os.

# speaker:king
# pace:30
- Dræb den drage med dit mægtige sværd, altså, med din musemarkør.

# speaker:king
# pace:30
- Og har du guld nok, kan du hverve flere til at hjælpe.

# speaker:king
# pace:30
- Held og lykke!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Forth'aarh er på en eller anden måde tilbage!

# speaker:king
# pace:30
# wait:400
Men du har opløst dine tropper. Nu må du hverve dem igen.

# speaker:king
# wait:300
# pace:30
- Og det sidste angreb ruinerede skatkammeret, så jeg kan ikke forsørge dine tropper.

# speaker:king
# pace:40
# chain_next
- Fra nu af bruger de

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- mad, træ og malm.

# speaker:king
# pace:40
- Du bliver nødt til at holde hus med ressourcerne.

# speaker:king
# pace:40
- Slå til og fra, hvem der får ressourcer, og hvem der ikke gør.

# speaker:king
# pace:40
- Eller "afskedig" nogle af dem: de bruger mindre og laver alligevel noget.

# speaker:king
# pace:28
- Held og lykke!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Desværre var vores tropper ikke nok til at slå invasionen tilbage.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jeg mistede alle tropperne, og løsesummen med.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Vores tropper er tilbage med gode nyheder!

# speaker:king
# pace:30
De slog invasionen tilbage med små tab.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jeg tager imod dem (så de kan komme tilbage til dragen...)

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
Nabokongeriget angriber os.

# speaker:king
# pace:30
De kræver {ransomCostLabel} guld for at standse invasionen.

# speaker:king
# chain_next
# pace:30
# wait:500
Hvad synes du, vi skal gøre?

* [Betal {ransomCostLabel} guld]
    -> pay_enemy

* { unitsCountFew > 3 } [Forsvar med {unitsCountFew} tropper]
    -> send_few_units

* { unitsCountMany > 3 } [Forsvar med {unitsCountMany} tropper]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Lad os håbe, de tager imod tilbuddet.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Lad os håbe, det er nok.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Så mange slår dem helt sikkert tilbage.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Jeg døde da i det mindste... ikke fattig.

# speaker:king
# pace:60
# classes:victory
Tillykke i øvrigt med at have gennemført spillet.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
DU HAR DRÆBT MIN FAR!!!

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
Jeg er din far!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Dig, der har lavet spillet?

# speaker:princess
# pace:50
Har du sat to replikker fra Star Wars ind i dit eget spil? Seriøst?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Så du fandt mig.

# speaker:king
# pace:32
Ja, jeg tog det fra dragens hule. Guldet til kongeriget. Legetøjet som minde.

# speaker:king
# pace:30
Mit folk sultede. Jeg ville gøre det igen.

# speaker:king
# pace:30
Tag en bestikkelse og ti stille, så slipper vi begge for besvær.

# speaker:king
# pace:30
Forråder du mig, eller tager du imod min gave?

* [Nogen må stoppe dig!]
  -> go_against_king

* [Jeg kan også godt lide guld!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så lad gå!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Tag så din del.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Jeg har givet dig mere guld, end du nogensinde har drømt om.

# speaker:king
# pace:30
Det var aftalen. Tag det og gå.

* [Lige meget, du skal stoppes]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så lad gå!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Du købte hæren, der dræbte hendes unge, for mit guld.

# speaker:king
# pace:32
Lad nu være med at spille uskyldig.

# speaker:king
# pace:30
Kom så an.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Så du skylder kongeriget penge? Rolig nu... lauget er fuldt af skyldnere.


# speaker:rogue
# pace:40
# wait:400
Betaler du ikke, går der et par ben.

# speaker:rogue
# pace:30
# wait:400
Indtil du er ude af minus, samler mine tyve dobbelt så meget guld til dig.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Ak! Vores manabeholdning er tom.

# speaker:wizard_dialog
# pace:35
# wait:400
Uden den mystiske kraft kan jeg ikke slynge noget mod dragen.

# speaker:wizard_dialog
# pace:35
# wait:400
Gå til opgraderingerne og køb "Manastrøm", hver gang vi er tomme... så slår vi det udyr igen!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Har nogen set kongen? Min far er forsvundet.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Sidst blev han set på vej ned i fangehullet under slottet.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Velkommen!

# pace:45
Jeg er Mook, ung og retskaffen!

# pace:50
Kongen satte mig her, så du ikke farer vild, og jeg siger det ligeud: jeg kan godt lide at vise vej.

# pace:35
Jeg må ikke forlade det her felt. "Hjælp alle, der kommer forbi", og så "gå ikke over den streg". Jeg siger til mig selv, at det er reglerne. På det seneste... er jeg ikke så sikker længere.

# pace:25
Men her, tag den her fakkel. Det er det eneste, jeg må sende over stregen.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Vær hilset, mit barn. Jeg er paven.

# speaker:pope
# pace:30
- Det er tid til at vise din tro igen og give en gave til Kirken.

# speaker:pope
# pace:30
- Jeg har brug for {contributionCostLabel} guld for at hjælpe de fattige.

* [Giv ham {contributionCostLabel} guld]
    -> pay_contribution

* [Skift religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Måtte din sjæl blive belønnet i det hinsides!

# speaker:pope
# pace:30
- Tag imod disse 100 præster som Kirkens tak.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Måtte din sjæl blive forbandet i det hinsides!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Og for resten...

# speaker:pope
# pace:30
- Det ville være en skam, hvis det kæmpestore firben blev helbredt af en højere magt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helbredende lyde\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jeg sælger mad, træ eller malm for

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
guld. Hvad skal du have?

* { canAffordTrading > 0 } [Mad: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Træ: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ikke noget, tak]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== farewell ===

# speaker:salesman
Vi ses næste gang.

* [Farvel]
    -> END

* [Kom lidt sjældnere]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Forstået. Jeg kommer sjældnere.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Du gjorde det virkelig!

# speaker:king
# pace:30
- Tak, fordi du dræbte den drage. Du er vores helt!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Endelig kan vi...

# speaker:princess
# classes:scared
# pace:200
Hvad var det?

# speaker:shadow
# pace:200
# classes:angry
I HAR DRÆBT MIT BARN!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
DET

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
DER ER

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
en stor drage!

# speaker:princess
# pace:20
# events:resume_game
Åh nej, vil du hjælpe os?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh er død. Du gjorde det, ingen hær kunne.

# speaker:king
# pace:28
# classes:victory
Tak. Oprigtigt.

# speaker:princess
# pace:30
# classes:victory
Følg med mig... Vi må ruste os til de fjender, der måtte komme herefter.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hvordan kunne den komme tilbage?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Jeg ved ikke, hvordan den vendte tilbage.

# speaker:king
# pace:28
- Men at rejse sig sådan igen kræver en usædvanlig vilje.

# speaker:princess
# pace:40
# classes:scared
- Og en sult efter hævn...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Ved du, at hver gang du går ned i fangehullet

# classes:angry-worker
# pace:30
- SKAL JEG BYGGE EN HELT NY LABYRINT I HÅNDEN?!?

# chain_next
# pace:50
- Vi har slæbt kister i ugevis. Han sagde, vi ikke skulle spørge, hvor de kom fra.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Endelig færdig!

# pace:40
- Kongen sagde, jeg er færdig, og at jeg må aflevere hakken, når det her niveau er klart.

  -> END
"""

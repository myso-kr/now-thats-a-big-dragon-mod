# -*- coding: utf-8 -*-
"""Writes the Norwegian Bokmål .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "du" throughout. Norwegian dropped "De" from ordinary use long ago; a King who
used it would sound like a letter from the tax office. He is grand in tone, not in
pronoun.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Du trenger visst hjelp til å skaffe flere ressurser...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Prøv å kjøpe Læreplasser for å få flere bønder, gruvearbeidere og tømmerhoggere.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Der var du igjen!

# speaker:engineer
Vi har jobbet videre med beleiringsvåpenet ditt.

# speaker:engineer
# wait:300
# pace:30
Nå kan den skyte katter mot fienden, og vi tror den snur hele kampen.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kaller den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en kunstpause)

# speaker:engineer
# pace:30
Vil du betale for forbedringen, både til denne og til alle de neste?

* [Jeg skyter heller med stein]
    -> no_thanks

* [Betal {catapultCostLabel} gull]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Si gjerne fra hva du synes!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Si gjerne fra hva du synes!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Synd. Lykke til likevel.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Troppene dine har spart det siste slaget til deg.

# speaker:king
# pace:30
- Her er sjansen din til å gjøre slutt på den for godt!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Far sier du må fortsette å trene, i tilfelle det kommer noe større.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Denne gangen betaler han til og med for troppene dine, så du får stille dem opp som du vil.

# speaker:princess
# pace:40
# chain_next
# wait:500
Og likevel, da jeg for et par måneder siden ba om et skikkelig stort bursdagsselskap,

# speaker:princess
# pace:40
# chain_next
# wait:500
fikk jeg bare høre...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, kongeriket har ingen penger, datter!"


# speaker:princess
# pace:37
Forresten, den tredukken ser rar ut...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Hva? Jeg trodde ikke engang den lot seg felle.

# speaker:princess
# pace:20
# classes:love
Men hva er det egentlig helten min ikke får til?

# speaker:princess
# events:whistle
# pace:50
Hva er det der oppe?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Det der er ingen vanlig treningsdukke.

# speaker:princess
# pace:30
Den ligner en magisk leke. Laget for noe langt større enn oss.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hei, du der...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Jeg fant et par nøkler til det hemmelige fangehullet under slottet.

# speaker:rogue
# pace:30
# wait:500
Jeg vet ikke engang om kongen vet at det finnes.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Men samme det...

# speaker:rogue
# pace:30
Jeg har fått med meg en god del derfra, men sist holdt fakkelen min på å slukne.

# speaker:rogue
# wait:500
Jeg tør ikke ned igjen og gå meg vill i mørket, så du får nøklene. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Lykke til,

# speaker:rogue
# pace:100
# events:end_give_keys
og pass på deg selv.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hei! Det er jeg som har laget spillet.

# pace:40
Beklager at du falt gjennom en vegg. Det er min feil.

# pace:30
Jeg får deg ut av tomrommet, og du beholder hele byttet.

* [Gi opp og behold byttet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Ha det!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
God dag, helt!

# speaker:engineer
# pace:30
# events:show_engineering_tab
For å hjelpe til i kampen har Hans Majestet befalt Det kongelige arkitekt- og ingeniørlauget å stille kunnskapen vår til din rådighet.

# speaker:engineer
# pace:30
Vi hjelper deg på tre måter:

# speaker:engineer
# pace:30
- Vi bygger katapulter til beleiringen.

# speaker:engineer
# pace:30
- Vi reiser bygninger på andre nivå, gjennom byggerne våre.

# speaker:engineer
# pace:30
- Vi oppretter organisasjoner på høyere nivåer, gjennom ingeniørene våre.

# speaker:engineer
# pace:30
Finn oss under fanen "Teknikk" når du har nok gull.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Vel, hva trodde du "å si opp tropper" betydde?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Var det ikke nok å drepe meg? La meg få være i fred!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Pip pip, ditt r**hull!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Jeg er klar til å spille for troppene dine og vekke kraften deres.

# speaker:bard_dialog
# pace:35
# wait:400
Trykk på harpeknappen og nyt en stund med ekstra styrke!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Hjelp!

# speaker:king
# chain_next
# pace:30
# wait:500
En kjempestor drage ødelegger landsbyen vår!

# speaker:king
# wait:300
# pace:30
- Vi trenger en helt som redder oss.

# speaker:king
# pace:30
- Drep den dragen med det mektige sverdet ditt, altså, med musepekeren din.

# speaker:king
# pace:30
- Og har du nok gull, kan du verve flere til å hjelpe.

# speaker:king
# pace:30
- Lykke til!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Forth'aarh er på et eller annet vis tilbake!

# speaker:king
# pace:30
# wait:400
Men du har oppløst troppene dine. Nå må du verve dem på nytt.

# speaker:king
# wait:300
# pace:30
- Og forrige angrep ruinerte skattkammeret, så jeg kan ikke forsørge troppene dine.

# speaker:king
# pace:40
# chain_next
- Fra nå av bruker de

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- mat, tømmer og malm.

# speaker:king
# pace:40
- Du blir nødt til å holde hus med ressursene.

# speaker:king
# pace:40
- Slå av og på hvem som får ressurser og hvem som ikke gjør det.

# speaker:king
# pace:40
- Eller "si opp" noen: de bruker mindre og gjør likevel litt nytte.

# speaker:king
# pace:28
- Lykke til!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Dessverre var ikke troppene våre nok til å slå tilbake invasjonen.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jeg mistet alle troppene, og løsepengene med.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Troppene våre er tilbake med gode nyheter!

# speaker:king
# pace:30
De slo tilbake invasjonen med små tap.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jeg tar imot dem (så de kan komme tilbake til dragen...)

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
Nabokongeriket angriper oss.

# speaker:king
# pace:30
De krever {ransomCostLabel} gull for å stanse invasjonen.

# speaker:king
# chain_next
# pace:30
# wait:500
Hva synes du vi skal gjøre?

* [Betal {ransomCostLabel} gull]
    -> pay_enemy

* { unitsCountFew > 3 } [Forsvar med {unitsCountFew} tropper]
    -> send_few_units

* { unitsCountMany > 3 } [Forsvar med {unitsCountMany} tropper]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- La oss håpe de tar imot tilbudet.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- La oss håpe det holder.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Så mange slår dem helt sikkert tilbake.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Jeg døde da i det minste... ikke fattig.

# speaker:king
# pace:60
# classes:victory
Gratulerer forresten med å ha fullført spillet.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
DU DREPTE FAREN MIN!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nei...

# speaker:developer
# pace:100
# classes:vader
Jeg er faren din!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Du som har laget spillet?

# speaker:princess
# pace:50
Har du satt inn to replikker fra Star Wars i ditt eget spill? Seriøst?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Så du fant meg.

# speaker:king
# pace:32
Ja, jeg tok det fra dragens hule. Gullet til kongeriket. Leken som minne.

# speaker:king
# pace:30
Folket mitt sultet. Jeg ville gjort det igjen.

# speaker:king
# pace:30
Ta en bestikkelse og ti stille, så slipper vi begge bryet.

# speaker:king
# pace:30
Forråder du meg, eller tar du imot gaven min?

* [Noen må stoppe deg!]
  -> go_against_king

* [Jeg liker gull, jeg også!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så får det bli slik!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ta din del, da.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Jeg har gitt deg mer gull enn du noen gang har drømt om.

# speaker:king
# pace:30
Det var avtalen. Ta det og gå.

* [Samme det, du må stoppes]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så får det bli slik!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Du kjøpte hæren som drepte ungen hennes, for gullet mitt.

# speaker:king
# pace:32
Ikke spill uskyldig.

# speaker:king
# pace:30
Kom an, da.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Så du skylder kongeriket penger? Rolig nå... lauget er fullt av skyldnere.


# speaker:rogue
# pace:40
# wait:400
Betaler du ikke, ryker det et par bein.

# speaker:rogue
# pace:30
# wait:400
Til du er ute av minus, samler tyvene mine dobbelt så mye gull til deg.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Å nei! Manabeholdningen vår er tom.

# speaker:wizard_dialog
# pace:35
# wait:400
Uten den mystiske kraften får jeg ikke slynget noe mot dragen.

# speaker:wizard_dialog
# pace:35
# wait:400
Gå til oppgraderingene og kjøp "Manastrøm" hver gang vi er tomme... så slår vi til mot udyret igjen!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Har noen sett kongen? Faren min er forsvunnet.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Sist ble han sett på vei ned i fangehullet under slottet.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Velkommen!

# pace:45
Jeg er Mook, ung og rettskaffen!

# pace:50
Kongen satte meg her så du ikke skal gå deg vill, og jeg sier det rett ut: jeg liker å vise vei.

# pace:35
Jeg får ikke forlate denne ruten. "Hjelp alle som går forbi", og så "ikke gå over den streken". Jeg sier til meg selv at det er reglene. I det siste... er jeg ikke så sikker lenger.

# pace:25
Men her, ta denne fakkelen. Det er det eneste jeg får sende over streken.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Vær hilset, mitt barn. Jeg er paven.

# speaker:pope
# pace:30
- Det er på tide å vise troen din igjen og gi en gave til Kirken.

# speaker:pope
# pace:30
- Jeg trenger {contributionCostLabel} gull for å hjelpe de fattige.

* [Gi ham {contributionCostLabel} gull]
    -> pay_contribution

* [Bytt religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Måtte sjelen din bli belønnet i det hinsidige!

# speaker:pope
# pace:30
- Ta imot disse 100 prestene som Kirkens takk.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Måtte sjelen din bli forbannet i det hinsidige!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Og forresten...

# speaker:pope
# pace:30
- Det ville være synd om den kjempestore øglen ble helbredet av en høyere makt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helbredende lyder\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jeg selger mat, tømmer eller malm for

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
gull. Hva skal du ha?

* { canAffordTrading > 0 } [Mat: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Tømmer: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ingenting, takk]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== farewell ===

# speaker:salesman
Vi ses neste gang.

* [Ha det]
    -> END

* [Kom litt sjeldnere]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Forstått. Jeg kommer sjeldnere.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Du klarte det faktisk!

# speaker:king
# pace:30
- Takk for at du drepte den dragen. Du er helten vår!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Endelig kan vi...

# speaker:princess
# classes:scared
# pace:200
Hva var det?

# speaker:shadow
# pace:200
# classes:angry
DERE DREPTE BARNET MITT!!!

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
Å nei, hjelper du oss?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh er død. Du gjorde det ingen hær fikk til.

# speaker:king
# pace:28
# classes:victory
Takk. Oppriktig.

# speaker:princess
# pace:30
# classes:victory
Bli med meg... Vi må ruste oss mot fiendene som kan komme etter dette.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hvordan kunne den komme tilbake?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Jeg vet ikke hvordan den vendte tilbake.

# speaker:king
# pace:28
- Men å reise seg slik igjen krever en uvanlig vilje.

# speaker:princess
# pace:40
# classes:scared
- Og en sult etter hevn...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Vet du at hver gang du går ned i fangehullet

# classes:angry-worker
# pace:30
- MÅ JEG BYGGE EN HELT NY LABYRINT FOR HÅND?!?

# chain_next
# pace:50
- Vi har slept på kister i ukevis. Han sa vi ikke skulle spørre hvor de kom fra.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Endelig ferdig!

# pace:40
- Kongen sa at jeg er ferdig, og at jeg får levere tilbake hakken når dette nivået er klart.

  -> END
"""

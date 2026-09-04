# -*- coding: utf-8 -*-
"""Writes the Dutch .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "je" throughout. "u" would put the King at a formal distance the English does
not have - he is grand in tone, not in pronoun - and no other speaker here would use it
either.

The IJ digraph is written as two letters, which is what Dutch does in practice and what
keeps the text inside the game's own font.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Je kunt vast wat hulp gebruiken bij het maken van grondstoffen...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Koop Leerplaatsen voor meer boeren, mijnwerkers en houthakkers.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Daar ben je weer!

# speaker:engineer
We hebben doorgewerkt aan je belegeringswapen.

# speaker:engineer
# wait:300
# pace:30
Hij kan nu katten op de vijand schieten, en wij denken dat dat het gevecht kantelt.

# speaker:engineer
# wait:300
# pace:30
# chain_next
We noemen hem de "Kattapult"

# speaker:engineer
# wait:300
# pace:300
(een stilte voor het effect)

# speaker:engineer
# pace:30
Wil je de verbetering betalen, voor deze en voor alle volgende?

* [Ik schiet liever met stenen]
    -> no_thanks

* [Betaal {catapultCostLabel} goud]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Laat ons weten wat je ervan vindt!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Laat ons weten wat je ervan vindt!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Jammer. Toch veel succes.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Je troepen hebben de laatste slag voor jou bewaard.

# speaker:king
# pace:30
- Dit is je kans om er voorgoed een eind aan te maken!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Vader zegt dat je moet blijven oefenen, voor het geval er iets groters komt.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Deze keer betaalt hij zelfs je troepen, dus je mag ze opstellen zoals je wilt.

# speaker:princess
# pace:40
# chain_next
# wait:500
En toch, toen ik een paar maanden geleden om een heel groot verjaardagsfeest vroeg,

# speaker:princess
# pace:40
# chain_next
# wait:500
kreeg ik alleen te horen...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, het koninkrijk heeft geen geld, dochter!"


# speaker:princess
# pace:37
Trouwens, die houten pop ziet er vreemd uit...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Wat? Ik dacht niet eens dat hij om te krijgen was.

# speaker:princess
# pace:20
# classes:love
Maar wat kan mijn held eigenlijk niet?

# speaker:princess
# events:whistle
# pace:50
Wat is dat daarboven?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Dat is geen gewone oefenpop.

# speaker:princess
# pace:30
Het lijkt op een magisch speeltje. Gemaakt voor iets dat veel groter is dan wij.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hé, jij daar...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Ik heb een paar sleutels gevonden van de geheime kerker onder het kasteel.

# speaker:rogue
# pace:30
# wait:500
Ik weet niet eens of de koning weet dat hij bestaat.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Maar goed...

# speaker:rogue
# pace:30
Ik heb er aardig wat uit gehaald, maar de vorige keer ging mijn fakkel bijna uit.

# speaker:rogue
# wait:500
Ik durf niet terug het donker in, dus jij krijgt de sleutels. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Succes,

# speaker:rogue
# pace:100
# events:end_give_keys
en wees voorzichtig.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hoi! Ik heb dit spel gemaakt.

# pace:40
Sorry dat je door een muur bent gezakt. Dat is mijn fout.

# pace:30
Ik haal je uit de leegte, en je houdt al je buit.

* [Opgeven en de buit houden]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Tot ziens!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Gegroet, held!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Om te helpen in de strijd heeft Zijne Majesteit het Koninklijk Gilde van Architecten en Ingenieurs bevolen onze kennis tot je beschikking te stellen.

# speaker:engineer
# pace:30
Wij helpen je op drie manieren:

# speaker:engineer
# pace:30
- Wij bouwen katapulten voor het beleg.

# speaker:engineer
# pace:30
- Wij zetten gebouwen van het tweede niveau neer, via onze bouwers.

# speaker:engineer
# pace:30
- Wij stichten organisaties van hogere niveaus, via onze ingenieurs.

# speaker:engineer
# pace:30
Zoek ons op onder het tabblad "Techniek" zodra je genoeg goud hebt.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Nou, wat dacht je dat "troepen ontslaan" betekende?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Was mij doden niet genoeg? Laat me toch met rust!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Tjilp tjilp, klo**zak!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Ik ben klaar om voor je troepen te spelen en hun kracht te wekken.

# speaker:bard_dialog
# pace:35
# wait:400
Druk op de harpknop en geniet van een tijdje extra kracht!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Help!

# speaker:king
# chain_next
# pace:30
# wait:500
Een reusachtige draak verwoest ons dorp!

# speaker:king
# wait:300
# pace:30
- We hebben een held nodig die ons redt.

# speaker:king
# pace:30
- Dood die draak alsjeblieft met je machtige zwaard, ik bedoel, met je muisaanwijzer.

# speaker:king
# pace:30
- En met genoeg goud kun je anderen werven die je helpen.

# speaker:king
# pace:30
- Succes!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Forth'aarh is op de een of andere manier terug!

# speaker:king
# pace:30
# wait:400
Maar je hebt je troepen ontbonden. Nu moet je ze opnieuw werven.

# speaker:king
# wait:300
# pace:30
- En de vorige aanval heeft de schatkist geruïneerd, dus ik kan je troepen niet onderhouden.

# speaker:king
# pace:40
# chain_next
- Voortaan verbruiken ze

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- voedsel, hout en erts.

# speaker:king
# pace:40
- Je zult met je grondstoffen moeten woekeren.

# speaker:king
# pace:40
- Zet aan en uit wie er grondstoffen krijgt en wie niet.

# speaker:king
# pace:40
- Of "ontsla" er een paar: die verbruiken minder en doen toch nog iets.

# speaker:king
# pace:28
- Succes!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Helaas waren onze troepen niet genoeg om de invasie af te slaan.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ik ben al mijn troepen kwijt, en het losgeld ook.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Onze troepen zijn terug met goed nieuws!

# speaker:king
# pace:30
Ze hebben de invasie afgeslagen met weinig verliezen.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Ik neem ze op (zodat ze weer aan de draak kunnen beginnen...)

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
Het buurkoninkrijk valt ons aan.

# speaker:king
# pace:30
Ze eisen {ransomCostLabel} goud om de invasie te staken.

# speaker:king
# chain_next
# pace:30
# wait:500
Wat vind jij dat we moeten doen?

* [Betaal {ransomCostLabel} goud]
    -> pay_enemy

* { unitsCountFew > 3 } [Verdedig met {unitsCountFew} troepen]
    -> send_few_units

* { unitsCountMany > 3 } [Verdedig met {unitsCountMany} troepen]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Laten we hopen dat ze het aanbod aannemen.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Laten we hopen dat het genoeg is.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Zo veel slaat ze zeker terug.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Ik ben tenminste... niet arm gestorven.

# speaker:king
# pace:60
# classes:victory
Gefeliciteerd trouwens met het uitspelen.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
JE HEBT MIJN VADER GEDOOD!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nee...

# speaker:developer
# pace:100
# classes:vader
Ik ben je vader!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Jij die het spel gemaakt hebt?

# speaker:princess
# pace:50
Heb je twee zinnen uit Star Wars in je eigen spel gezet? Echt waar?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Dus je hebt me gevonden.

# speaker:king
# pace:32
Ja, ik heb het uit het hol van de draak gehaald. Het goud voor het koninkrijk. Het speeltje als aandenken.

# speaker:king
# pace:30
Mijn volk had honger. Ik zou het zo weer doen.

# speaker:king
# pace:30
Neem een omkoopsom en zwijg, dan hebben we er allebei geen last van.

# speaker:king
# pace:30
Verraad je me, of neem je mijn geschenk aan?

* [Iemand moet je tegenhouden!]
  -> go_against_king

* [Ik hou ook wel van goud!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Goed dan!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Neem dan je deel.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Ik heb je meer goud gegeven dan je ooit hebt gedroomd.

# speaker:king
# pace:30
Dat was de afspraak. Neem het en ga.

* [Maakt niet uit, je moet gestopt worden]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Goed dan!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Je hebt met mijn goud het leger gekocht dat haar jong heeft gedood.

# speaker:king
# pace:32
Doe niet alsof je onschuldig bent.

# speaker:king
# pace:30
Kom dan maar.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Dus je hebt schulden bij het koninkrijk? Rustig maar... het gilde zit vol met schuldenaars.


# speaker:rogue
# pace:40
# wait:400
Betaal je niet, dan gaan er een paar benen aan.

# speaker:rogue
# pace:30
# wait:400
Tot je weer uit de rode cijfers bent, halen mijn dieven dubbel zoveel goud voor je op.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Helaas! Onze manavoorraad is op.

# speaker:wizard_dialog
# pace:35
# wait:400
Zonder die mystieke kracht kan ik niets naar de draak slingeren.

# speaker:wizard_dialog
# pace:35
# wait:400
Ga naar de upgrades en koop "Manastroom" telkens als we leeg zijn... dan slaan we dat beest weer!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Heeft iemand de koning gezien? Mijn vader is verdwenen.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Het laatst is hij gezien op weg naar de kerker onder het kasteel.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Welkom!

# pace:45
Ik ben Mook, jong en rechtschapen!

# pace:50
De koning heeft me hier neergezet zodat je niet verdwaalt, en ik zeg het eerlijk: ik wijs graag de weg.

# pace:35
Ik mag dit vak niet verlaten. "Help iedereen die langskomt", en dan "kom niet over die lijn". Ik hou mezelf voor dat het de regels zijn. De laatste tijd... weet ik het niet meer zo zeker.

# pace:25
Maar hier, neem deze fakkel. Dat is het enige wat ik nog over die lijn mag geven.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Gegroet, mijn kind. Ik ben de paus.

# speaker:pope
# pace:30
- Het is tijd om je geloof opnieuw te tonen en de Kerk een gave te doen.

# speaker:pope
# pace:30
- Ik heb {contributionCostLabel} goud nodig om de armen te helpen.

* [Geef hem {contributionCostLabel} goud]
    -> pay_contribution

* [Verander van geloof]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Moge je ziel beloond worden in het hiernamaals!

# speaker:pope
# pace:30
- Neem deze 100 priesters aan als dank van de Kerk.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Moge je ziel vervloekt worden in het hiernamaals!

# speaker:pope
# pace:30
# chain_next
# wait:500
- En trouwens...

# speaker:pope
# pace:30
- Het zou zonde zijn als die reusachtige hagedis door een hogere macht genezen werd...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(genezende geluiden\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Ik verkoop voedsel, hout of erts voor

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
goud. Wat wil je hebben?

* { canAffordTrading > 0 } [Voedsel: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Hout: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Erts: {resourceAmountLabel}]
    -> buy_ore

* [Niets, dank je]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== farewell ===

# speaker:salesman
Tot de volgende keer.

* [Dag]
    -> END

* [Kom wat minder vaak]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Begrepen. Ik kom minder vaak langs.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Je hebt het echt gedaan!

# speaker:king
# pace:30
- Dank je voor het doden van die draak. Je bent onze held!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Eindelijk kunnen we...

# speaker:princess
# classes:scared
# pace:200
Wat was dat?

# speaker:shadow
# pace:200
# classes:angry
JULLIE HEBBEN MIJN KIND GEDOOD!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
DAT

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
IS PAS

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
een grote draak!

# speaker:princess
# pace:20
# events:resume_game
O nee, help je ons?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh is dood. Je hebt gedaan wat geen leger kon.

# speaker:king
# pace:28
# classes:victory
Dank je. Oprecht.

# speaker:princess
# pace:30
# classes:victory
Kom mee... We moeten ons klaarmaken voor de vijanden die hierna kunnen komen.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Hoe kon hij terugkomen?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Ik weet niet hoe hij is teruggekeerd.

# speaker:king
# pace:28
- Maar zo weer opstaan vraagt een buitengewone wil.

# speaker:princess
# pace:40
# classes:scared
- En een honger naar wraak...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Weet je dat ik elke keer dat jij de kerker in gaat

# classes:angry-worker
# pace:30
- EEN HEEL NIEUW DOOLHOF MET DE HAND MOET BOUWEN?!?

# chain_next
# pace:50
- We zeulen al weken met kisten. Hij zei dat we niet moesten vragen waar ze vandaan komen.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Eindelijk klaar!

# pace:40
- De koning zei dat ik klaar ben en dat ik de pikhouweel mag teruggeven zodra dit niveau af is.

  -> END
"""

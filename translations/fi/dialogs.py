# -*- coding: utf-8 -*-
"""Writes the Finnish .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "sinä" throughout. The polite plural would make the King sound like a form
letter rather than a monarch; he is grand in tone, not in pronoun.

Finnish inflects rather than using prepositions, so a line is written in the cases its
sentence asks for rather than word by word from the English.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Näyttää siltä, että tarvitset apua resurssien tuottamisessa...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Kokeile ostaa Oppisopimuksia saadaksesi lisää maanviljelijöitä, kaivosmiehiä ja metsureita.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Taas tavataan!

# speaker:engineer
Olemme jatkaneet piiritysaseesi kehittelyä.

# speaker:engineer
# wait:300
# pace:30
Nyt se ampuu vihollisen niskaan kissoja, ja uskomme sen kääntävän koko taistelun.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Kutsumme sitä nimellä "Kissapultti"

# speaker:engineer
# wait:300
# pace:300
(tehokeino tauko)

# speaker:engineer
# pace:30
Haluatko kustantaa parannuksen, tähän ja kaikkiin tuleviin?

* [Ammun mieluummin kiviä]
    -> no_thanks

* [Maksa {catapultCostLabel} kultaa]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Kerro toki mitä mieltä olet!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Kerro toki mitä mieltä olet!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Harmi. Onnea matkaan silti.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Joukkosi ovat säästäneet viimeisen iskun sinulle.

# speaker:king
# pace:30
- Tässä on tilaisuutesi tehdä siitä loppu lopullisesti!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Isä sanoo, että sinun pitää jatkaa harjoittelua, jos jotain suurempaa sattuu tulemaan.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Tällä kertaa hän jopa maksaa joukkosi, joten saat asettaa ne kuten haluat.

# speaker:princess
# pace:40
# chain_next
# wait:500
Ja silti, kun pari kuukautta sitten pyysin kunnon suuria syntymäpäiviä,

# speaker:princess
# pace:40
# chain_next
# wait:500
sain kuulla vain...

# speaker:princess
# pace:60
# classes:imitating
"Pla, pla, pla, kuningaskunnalla ei ole rahaa, tyttäreni!"


# speaker:princess
# pace:37
Muuten, tuo puunukke näyttää oudolta...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Mitä? En uskonut sitä edes voitavan kaataa.

# speaker:princess
# pace:20
# classes:love
Mutta mitä sankarini ei muka osaisi?

# speaker:princess
# events:whistle
# pace:50
Mikä tuo tuolla ylhäällä on?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Tuo ei ole tavallinen harjoitusnukke.

# speaker:princess
# pace:30
Se näyttää taikalelulta. Tehty jollekin paljon meitä suuremmalle.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hei, sinä siellä...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Löysin muutaman avaimen linnan alla olevaan salaiseen luolastoon.

# speaker:rogue
# pace:30
# wait:500
En tiedä edes tietääkö kuningas sen olevan olemassa.

# speaker:rogue
# pace:10
# chain_next
# wait:500
No, sama se...

# speaker:rogue
# pace:30
Olen saanut sieltä melkoisesti, mutta viime kerralla soihtuni oli sammua.

# speaker:rogue
# wait:500
En uskalla mennä takaisin ja eksyä pimeään, joten saat avaimet. Ilmaiseksi.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Onnea matkaan,

# speaker:rogue
# pace:100
# events:end_give_keys
ja ole varovainen.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Moi! Minä tein tämän pelin.

# pace:40
Anteeksi että putosit seinän läpi. Se on minun vikani.

# pace:30
Vedän sinut pois tyhjyydestä, ja koko saalis jää sinulle.

* [Luovuta ja pidä saalis]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Hei hei!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Tervehdys, sankari!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Auttaakseen taistelussa Hänen Majesteettinsa on käskenyt Kuninkaallisen arkkitehtien ja insinöörien killan asettaa osaamisemme käyttöösi.

# speaker:engineer
# pace:30
Autamme sinua kolmella tavalla:

# speaker:engineer
# pace:30
- Rakennamme katapultteja piiritykseen.

# speaker:engineer
# pace:30
- Pystytämme toisen tason rakennuksia rakentajiemme kautta.

# speaker:engineer
# pace:30
- Perustamme ylempien tasojen järjestöjä insinööriemme kautta.

# speaker:engineer
# pace:30
Etsi meidät välilehdeltä "Tekniikka", kun kultaa on tarpeeksi.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
No, mitä luulit "joukkojen erottamisen" tarkoittavan?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Eikö minun tappamiseni riittänyt? Anna minun olla rauhassa!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Piip piip, senkin p*****e!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Olen valmis soittamaan joukoillesi ja herättämään niiden voiman.

# speaker:bard_dialog
# pace:35
# wait:400
Paina harppupainiketta ja nauti hetken lisävoimasta!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Apua!

# speaker:king
# chain_next
# pace:30
# wait:500
Jättiläismäinen lohikäärme tuhoaa kyläämme!

# speaker:king
# wait:300
# pace:30
- Tarvitsemme sankarin, joka pelastaa meidät.

# speaker:king
# pace:30
- Tapa se lohikäärme mahtavalla miekallasi, siis hiiren osoittimellasi.

# speaker:king
# pace:30
- Ja jos kultaa riittää, voit värvätä muitakin avuksi.

# speaker:king
# pace:30
- Onnea matkaan!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Forth'aarh on jotenkin palannut!

# speaker:king
# pace:30
# wait:400
Mutta hajotit joukkosi. Nyt saat värvätä ne uudestaan.

# speaker:king
# wait:300
# pace:30
- Ja viime hyökkäys tyhjensi aarrekammion, joten en pysty elättämään joukkojasi.

# speaker:king
# pace:40
# chain_next
- Tästä lähtien ne kuluttavat

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- ruokaa, puuta ja malmia.

# speaker:king
# pace:40
- Joudut pitämään resursseista huolta.

# speaker:king
# pace:40
- Kytke päälle ja pois, ketkä saavat resursseja ja ketkä eivät.

# speaker:king
# pace:40
- Tai "erota" osa: ne kuluttavat vähemmän ja tekevät silti jotain.

# speaker:king
# pace:28
- Onnea matkaan!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Valitettavasti joukkomme eivät riittäneet torjumaan hyökkäystä.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Menetin kaikki joukot, ja lunnaat siinä sivussa.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Joukkomme ovat palanneet hyvien uutisten kanssa!

# speaker:king
# pace:30
Ne torjuivat hyökkäyksen vähäisin tappioin.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Otan heidät vastaan (jotta he pääsevät takaisin lohikäärmeen kimppuun...)

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
Naapurikuningaskunta hyökkää kimppuumme.

# speaker:king
# pace:30
He vaativat {ransomCostLabel} kultaa hyökkäyksen lopettamisesta.

# speaker:king
# chain_next
# pace:30
# wait:500
Mitä mieltä olet, mitä meidän pitäisi tehdä?

* [Maksa {ransomCostLabel} kultaa]
    -> pay_enemy

* { unitsCountFew > 3 } [Puolusta {unitsCountFew} joukolla]
    -> send_few_units

* { unitsCountMany > 3 } [Puolusta {unitsCountMany} joukolla]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Toivotaan, että he hyväksyvät tarjouksen.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Toivotaan, että se riittää.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Noin moni torjuu heidät varmasti.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Ainakaan... en kuollut köyhänä.

# speaker:king
# pace:60
# classes:victory
Onnittelut muuten pelin läpäisystä.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
SINÄ TAPOIT ISÄNI!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Ei...

# speaker:developer
# pace:100
# classes:vader
Minä olen isäsi!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Sinäkö, joka teit tämän pelin?

# speaker:princess
# pace:50
Laitoitko omaan peliisi kaksi repliikkiä Tähtien sodasta? Ihanko oikeasti?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Joten löysit minut.

# speaker:king
# pace:32
Kyllä, otin sen lohikäärmeen luolasta. Kullat kuningaskunnalle. Lelun muistoksi.

# speaker:king
# pace:30
Kansani näki nälkää. Tekisin sen uudestaan.

# speaker:king
# pace:30
Ota lahjus ja vaikene, niin kummallekaan ei tule harmia.

# speaker:king
# pace:30
Petätkö minut, vai otatko lahjani vastaan?

* [Jonkun on pysäytettävä sinut!]
  -> go_against_king

* [Minäkin pidän kullasta!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Olkoon sitten!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ota sitten osasi.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Olen antanut sinulle enemmän kultaa kuin osasit uneksia.

# speaker:king
# pace:30
Se oli sopimus. Ota se ja mene.

* [Sama se, sinut on pysäytettävä]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Olkoon sitten!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Ostit minun kullallani armeijan, joka tappoi sen poikasen.

# speaker:king
# pace:32
Älä esitä viatonta.

# speaker:king
# pace:30
Tule sitten.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Eli olet velkaa kuningaskunnalle? Rauhassa... kilta on täynnä velallisia.


# speaker:rogue
# pace:40
# wait:400
Jos et maksa, jokunen jalka katkeaa.

# speaker:rogue
# pace:30
# wait:400
Kunnes olet taas plussalla, varkaani keräävät sinulle kaksinkertaisesti kultaa.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Voi ei! Manavarastomme on tyhjä.

# speaker:wizard_dialog
# pace:35
# wait:400
Ilman sitä salaperäistä voimaa en pysty singahduttamaan mitään lohikäärmeeseen.

# speaker:wizard_dialog
# pace:35
# wait:400
Mene parannuksiin ja osta "Manavirta" aina kun olemme tyhjinä... niin iskemme taas siihen petoon!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Onko kukaan nähnyt kuningasta? Isäni on kadonnut.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Viimeksi hänet nähtiin menossa alas linnan alla olevaan luolastoon.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Tervetuloa!

# pace:45
Olen Mook, nuori ja vanhurskas!

# pace:50
Kuningas asetti minut tähän, ettet eksyisi, ja sanon suoraan: pidän tien näyttämisestä.

# pace:35
En saa poistua tästä ruudusta. "Auta jokaista ohikulkijaa", ja sitten "älä astu tuon viivan yli". Kerron itselleni, että ne ovat säännöt. Viime aikoina... en ole enää ihan varma.

# pace:25
Mutta tässä, ota tämä soihtu. Se on ainoa, jonka saan ojentaa viivan yli.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Tervehdys, lapseni. Olen paavi.

# speaker:pope
# pace:30
- On aika osoittaa uskosi jälleen ja antaa lahja Kirkolle.

# speaker:pope
# pace:30
- Tarvitsen {contributionCostLabel} kultaa auttaakseni köyhiä.

* [Anna hänelle {contributionCostLabel} kultaa]
    -> pay_contribution

* [Vaihda uskontoa]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Palkittakoon sielusi tuonpuoleisessa!

# speaker:pope
# pace:30
- Ota vastaan nämä 100 pappia Kirkon kiitoksena.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Kirottakoon sielusi tuonpuoleisessa!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Ja muuten...

# speaker:pope
# pace:30
- Olisi ikävää, jos tuo jättiläismäinen lisko paranisi korkeamman voiman avulla...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(parantavia ääniä\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Myyn ruokaa, puuta tai malmia hintaan

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
kultaa. Mitä otat?

* { canAffordTrading > 0 } [Ruoka: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Puu: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malmi: {resourceAmountLabel}]
    -> buy_ore

* [En mitään, kiitos]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== farewell ===

# speaker:salesman
Nähdään ensi kerralla.

* [Näkemiin]
    -> END

* [Tule harvemmin]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Selvä. Tulen harvemmin.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Sinä todella teit sen!

# speaker:king
# pace:30
- Kiitos, että tapoit sen lohikäärmeen. Olet sankarimme!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Vihdoinkin voimme...

# speaker:princess
# classes:scared
# pace:200
Mikä tuo oli?

# speaker:shadow
# pace:200
# classes:angry
TE TAPOITTE LAPSENI!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
TUOSSA

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
VASTA ON

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
suuri lohikäärme!

# speaker:princess
# pace:20
# events:resume_game
Voi ei, autathan meitä?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh on kuollut. Teit sen, mihin yksikään armeija ei pystynyt.

# speaker:king
# pace:28
# classes:victory
Kiitos. Vilpittömästi.

# speaker:princess
# pace:30
# classes:victory
Tule mukaani... Meidän on valmistauduttava vihollisiin, joita saattaa tulla seuraavaksi.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Miten se saattoi palata?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- En tiedä, miten se palasi.

# speaker:king
# pace:28
- Mutta noin nouseminen vaatii tavatonta tahtoa.

# speaker:princess
# pace:40
# classes:scared
- Ja koston nälkää...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Tiedätkö, että joka kerta kun menet luolastoon

# classes:angry-worker
# pace:30
- MINUN ON RAKENNETTAVA KOKONAAN UUSI LABYRINTTI KÄSIN?!?

# chain_next
# pace:50
- Olemme raahanneet arkkuja viikkokausia. Hän käski olla kysymättä, mistä ne tulevat.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Vihdoinkin valmis!

# pace:40
- Kuningas sanoi, että olen valmis ja saan palauttaa hakun, kun tämä taso on tehty.

  -> END
"""

# -*- coding: utf-8 -*-
"""Writes the Czech .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: informal "ty" throughout, the norm for Czech game dialogue. The King is
formal in tone but speaks to the hero directly.

The game's fonts have no „" quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Zdá se, že se ti hodí pomoc s výrobou zdrojů...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Zkus koupit Učňovství, ať máš víc farmářů, horníků a dřevorubců.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Zase se vidíme!

# speaker:engineer
Pokračovali jsme ve výzkumu tvého obléhacího stroje.

# speaker:engineer
# wait:300
# pace:30
Teď dokáže po nepřátelích střílet kočky a myslíme, že to zvrátí průběh boje.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Říkáme tomu "Kočko-pult"

# speaker:engineer
# wait:300
# pace:300
(dramatická pauza)

# speaker:engineer
# pace:30
Chceš investovat do přestavby stávajících i budoucích kusů?

* [Radši budu dál střílet balvany]
    -> no_thanks

* [Zaplatit {catapultCostLabel} zlata]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Dej nám vědět, jak se ti to líbilo!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Dej nám vědět, jak se ti to líbilo!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Škoda. Tak ať se ti daří.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Tvé jednotky ti nechaly poslední ránu.

# speaker:king
# pace:30
- Teď máš šanci ho dorazit nadobro!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Král tě žádal, ať dál trénuješ, kdyby náhodou přišlo něco většího.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Tentokrát ti dokonce zaplatí armádu, ať si ji poskládáš po svém.

# speaker:princess
# pace:40
# chain_next
# wait:500
Ale když jsem si já před pár měsíci řekla o obrovskou narozeninovou oslavu,

# speaker:princess
# pace:40
# chain_next
# wait:500
bylo to jen...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, království nemá peníze, dcero!"


# speaker:princess
# pace:37
Ten panák ale vypadá divně...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Cože? Nemyslela jsem, že se dá porazit.

# speaker:princess
# pace:20
# classes:love
Ale je vůbec něco, co by můj hrdina neporazil?

# speaker:princess
# events:whistle
# pace:50
Co, co to je tam nahoře?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Tohle není obyčejný tréninkový panák.

# speaker:princess
# pace:30
Vypadá to jako kouzelná hračka. Pro něco mnohem většího, než jsme my.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hej, ty tam...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Našel jsem tyhle klíče od tajné kobky pod hradem.

# speaker:rogue
# pace:30
# wait:500
Zajímalo by mě, jestli o ní král ví.

# speaker:rogue
# pace:10
# chain_next
# wait:500
No nic...

# speaker:rogue
# pace:30
Při výpravách jsem vynesl slušnou kořist, ale posledně mi málem zhasla pochodeň.

# speaker:rogue
# wait:500
Bojím se jít znovu dovnitř a ztratit se ve tmě, tak ti dám všechny klíče zadarmo.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Hodně štěstí,

# speaker:rogue
# pace:100
# events:end_give_keys
a dávej na sebe pozor.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hej! Tady vývojář.

# pace:40
Promiň, propadl jsi zdí. To je moje chyba.

# pace:30
Vyvedu tě z prázdnoty a celou kořist si necháš.

* [Vzdát se a nechat si kořist]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Měj se!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Zdravím, hrdino!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Aby pomohl v boji, nařídil Jeho Veličenstvo Řádu architektů a inženýrů Koruny propůjčit naše znalosti.

# speaker:engineer
# pace:30
Pomůžeme ti třemi způsoby:

# speaker:engineer
# pace:30
- Postavíme katapulty pro obléhání.

# speaker:engineer
# pace:30
- Postavíme budovy druhé úrovně, rukama našich stavitelů.

# speaker:engineer
# pace:30
- Založíme organizace vyšších úrovní, rukama našich inženýrů.

# speaker:engineer
# pace:30
Až budeš mít zlato, najdeš nás na kartě "Inženýrství".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ale ale, a co sis myslel, že znamená "propustit jednotky"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Nestačilo ti mě zabít? Přestaň mě otravovat, prosím!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Cvrlik cvrlik, ty h*****!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Jsem připraven zahrát tvým jednotkám a povzbudit je k větší síle.

# speaker:bard_dialog
# pace:35
# wait:400
Klikni na tlačítko s harfou a užij si dočasné zesílení!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Pomoc!

# speaker:king
# chain_next
# pace:30
# wait:500
Obrovský drak ničí naši vesnici!

# speaker:king
# wait:300
# pace:30
- Potřebujeme hrdinu, který nás zachrání.

# speaker:king
# pace:30
- Prosím, zabij toho draka svým mocným mečem, tedy kurzorem myši.

# speaker:king
# pace:30
- A pokud budeš mít dost zlata, můžeš najmout i pomoc.

# speaker:king
# pace:30
- Hodně štěstí!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Nějakým způsobem se Forth'aarh vrátil!

# speaker:king
# pace:30
# wait:400
Ale ty jsi své jednotky rozpustil. Teď je budeš muset naverbovat znovu.

# speaker:king
# wait:300
# pace:30
- A předchozí útok zruinoval naši ekonomiku, takže tvou armádu neuživím.

# speaker:king
# pace:40
# chain_next
- Od teď budou spotřebovávat

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- jídlo, dřevo a rudu.

# speaker:king
# pace:40
- Budeš muset se zdroji hospodařit s rozmyslem.

# speaker:king
# pace:40
- Přepínej, která jednotka má právě spotřebovávat zdroje a která ne.

# speaker:king
# pace:40
- Nebo některé "propusť": spotřebují míň, a přesto něco odvedou.

# speaker:king
# pace:28
- Hodně štěstí!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Bohužel naše jednotky na odražení invaze nestačily.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ztratili jsme je do jedné a s nimi i částku výkupného.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Jednotky se vrátily se skvělými zprávami!

# speaker:king
# pace:30
Podařilo se jim odrazit invazi s minimálními ztrátami.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Vítáme je zpět (a jdeme dál dřít na draka...)

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
Sousední království na nás útočí.

# speaker:king
# pace:30
Žádají {ransomCostLabel} zlaťáků, aby invazi zastavili.

# speaker:king
# chain_next
# pace:30
# wait:500
Co myslíš, že bychom měli udělat?

* [Zaplatit {ransomCostLabel} zlaťáků]
    -> pay_enemy

* { unitsCountFew > 3 } [Bránit se s {unitsCountFew} jednotkami]
    -> send_few_units

* { unitsCountMany > 3 } [Bránit se s {unitsCountMany} jednotkami]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Doufejme, že naši nabídku přijmou.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Doufejme, že to bude stačit.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Tohle jejich útok určitě odrazí.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Aspoň... jsem neumřel chudý.

# speaker:king
# pace:60
# classes:victory
Každopádně gratuluji k dohrání hry.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
ZABIL JSI MÉHO OTCE!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Ne...

# speaker:developer
# pace:100
# classes:vader
Já jsem tvůj otec!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Vývojáři?

# speaker:princess
# pace:50
Dal jsi do své hry dva odkazy na Star Wars? Vážně?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Našel jsi mě.

# speaker:king
# pace:32
Ano, vzal jsem to z dračího doupěte. Zlato pro království. Hračku na památku.

# speaker:king
# pace:30
Náš lid hladověl. Udělal bych to znovu.

# speaker:king
# pace:30
Vezmi si úplatek a mlč, a oba z toho vyjdeme čistí.

# speaker:king
# pace:30
Zradíš mě, nebo přijmeš můj dar?

* [Někdo tě musí zastavit!]
  -> go_against_king

* [Zlato mám rád!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Budiž!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Tak si vezmi svůj podíl.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Dal jsem ti už víc zlata, než sis kdy přál.

# speaker:king
# pace:30
Taková byla dohoda. Vezmi si ho a odejdi.

* [Je mi to jedno, musím tě zastavit]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Budiž!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Za mé zlato sis koupil armádu, která zabila jeho mládě.

# speaker:king
# pace:32
Nedělej ze sebe nevinného.

# speaker:king
# pace:30
Tak pojď.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Takže ses zadlužil u koruny, co? Klid... cech má spoustu hlupáků, kteří nám dluží.


# speaker:rogue
# pace:40
# wait:400
Když nezaplatí, zlámeme jim pár nohou.

# speaker:rogue
# pace:30
# wait:400
Dokud se nedostaneš do plusu, budou ti moji zloději shánět zlato dvakrát tvrději.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Běda! Naše zásoby many došly.

# speaker:wizard_dialog
# pace:35
# wait:400
Bez tajemné esence nemohu na draka seslat svá kouzla.

# speaker:wizard_dialog
# pace:35
# wait:400
Zajdi do nabídky vylepšení a kupuj "Doplnit manu", kdykoli vyschneme... ať můžeme na tu bestii znovu udeřit!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Neviděl někdo krále? Zmizel.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Naposledy ho viděli, jak sestupuje do kobek pod hradem.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Vítej!

# pace:45
Jsem Mook, mladý a spravedlivý!

# pace:50
Král mě sem postavil, abys nezabloudil, a myslím to vážně: rád ukazuji cestu.

# pace:35
Nesmím z téhle dlaždice. "Pomáhej každému poutníkovi", a pak "nepřekračuj tu čáru". Říkal jsem si, že je to předpis. Poslední dobou... už si tím nejsem jistý.

# pace:25
Ale tumáš, vezmi si tuhle pochodeň. Jediná pomoc, kterou ještě smím podat za tu čáru.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Zdravím, jsem papež.

# speaker:pope
# pace:30
- Je čas znovu prokázat svou víru a přispět naší Církvi.

# speaker:pope
# pace:30
- Potřebuji {contributionCostLabel} zlaťáků na pomoc chudým.

* [Dát mu {contributionCostLabel} zlaťáků]
    -> pay_contribution

* [Změnit víru]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Ať je tvá duše odměněna na onom světě!

# speaker:pope
# pace:30
- Přijmi těchto 100 kněží jako projev vděku Církve.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Ať je tvá duše zatracena na onom světě!

# speaker:pope
# pace:30
# chain_next
# wait:500
- A ještě...

# speaker:pope
# pace:30
- Byla by škoda, kdyby toho obrovského ještěra uzdravila vyšší moc...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(zvuky uzdravování\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Prodávám jídlo, dřevo nebo rudu za

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
zlata. Co si vybereš?

* { canAffordTrading > 0 } [Jídlo: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Dřevo: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Ruda: {resourceAmountLabel}]
    -> buy_ore

* [Nic]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== farewell ===

# speaker:salesman
Uvidíme se na příští cestě.

* [Sbohem]
    -> END

* [Jezdi míň často]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Rozumím. Budu jezdit řidčeji.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Páni, tobě se to fakt povedlo!

# speaker:king
# pace:30
- Moc děkuji, že jsi toho draka zabil. Jsi náš hrdina!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Konečně můžeme...

# speaker:princess
# classes:scared
# pace:200
Co to bylo za zvuk?

# speaker:shadow
# pace:200
# classes:angry
ZABILI JSTE MÉHO SYNA!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Tohle

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
UŽ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
je velký drak!

# speaker:princess
# pace:20
# events:resume_game
Ale ne, pomůžeš nám, viď?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh je mrtvý. Dokázal jsi, co nezvládla žádná armáda.

# speaker:king
# pace:28
# classes:victory
Děkuji. Opravdu.

# speaker:princess
# pace:30
# classes:victory
Pojď za mnou... Musíme se připravit na nové nepřátele, kdyby přišli.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Jak se mohl vrátit?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Nevím, jak se vrátil.

# speaker:king
# pace:28
- Ale povstat takhle vyžaduje neuvěřitelnou vůli.

# speaker:princess
# pace:40
# classes:scared
- A taky touhu po nějaké pomstě...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Věděl jsi, že pokaždé, když vejdeš do kobky,

# classes:angry-worker
# pace:30
- MUSÍM CELÉ NOVÉ BLUDIŠTĚ POSTAVIT RUČNĚ?!?

# chain_next
# pace:50
- Týdny jsme nahoru tahali truhly. Řekl, ať se neptáme, odkud jsou.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Konečně!

# pace:40
- Král řekl, že mám hotovo a že mu můžu vrátit krumpáč, jakmile dodělám tuhle úroveň.

  -> END
"""

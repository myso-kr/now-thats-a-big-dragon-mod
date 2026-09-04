# -*- coding: utf-8 -*-
"""Writes the Polish .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: informal "ty", which is what Polish game dialogue uses. The King speaks
formally in tone but still addresses the hero directly.

The game's own font has no „" quotes, em dash or curly apostrophe, so this uses
straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Wygląda na to, że przydałaby ci się pomoc w wytwarzaniu zasobów...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Spróbuj kupić Praktyki, żeby mieć więcej rolników, górników i drwali.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Witaj ponownie!

# speaker:engineer
Kontynuowaliśmy prace nad twoją machiną oblężniczą.

# speaker:engineer
# wait:300
# pace:30
Teraz potrafi miotać kotami we wrogów i sądzimy, że przechyli szalę walki.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Nazywamy to "Kota-pulta"

# speaker:engineer
# wait:300
# pace:300
(dramatyczna pauza)

# speaker:engineer
# pace:30
Zainwestujesz w przeróbkę obecnych i przyszłych zakupów?

* [Wolę dalej strzelać głazami]
    -> no_thanks

* [Zapłać {catapultCostLabel} złota]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Daj znać, jak ci się spodobało!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Daj znać, jak ci się spodobało!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Szkoda. W takim razie powodzenia.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Twoje oddziały zostawiły ci ostatni cios.

# speaker:king
# pace:30
- To twoja szansa, by dobić go na dobre!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Król prosił, żebyś dalej ćwiczył, na wypadek gdyby przyszło coś większego.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Tym razem chce nawet sfinansować twoją armię, żebyś ułożył ją po swojemu.

# speaker:princess
# pace:40
# chain_next
# wait:500
A kiedy ja kilka miesięcy temu poprosiłam o wielkie przyjęcie urodzinowe,

# speaker:princess
# pace:40
# chain_next
# wait:500
było tylko...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, królestwo nie ma pieniędzy, córko!"


# speaker:princess
# pace:37
Choć ten manekin dziwnie wygląda...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Co? Nie sądziłam, że da się go pokonać.

# speaker:princess
# pace:20
# classes:love
Ale czy jest coś, czego mój bohater nie pokona?

# speaker:princess
# events:whistle
# pace:50
Co, co to tam w górze?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
To nie jest zwykły manekin treningowy.

# speaker:princess
# pace:30
Wygląda jak magiczna zabawka. Dla czegoś o wiele większego od nas.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hej, ty tam...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Znalazłem te klucze do tajnego lochu pod zamkiem.

# speaker:rogue
# pace:30
# wait:500
Ciekawe, czy król wie o jego istnieniu.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Ale mniejsza z tym...

# speaker:rogue
# pace:30
Z wypraw wynosiłem niezły łup, ale ostatnim razem prawie zgasła mi pochodnia.

# speaker:rogue
# wait:500
Boję się wejść znowu i zabłądzić w ciemności, więc oddaję ci wszystkie klucze za darmo.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Powodzenia,

# speaker:rogue
# pace:100
# events:end_give_keys
i uważaj na siebie.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hej! Tu twórca gry.

# pace:40
Przepraszam, że przeniknąłeś przez ścianę. To mój błąd.

# pace:30
Wyprowadzę cię z pustki, a cały łup zostanie przy tobie.

* [Poddaj się i zachowaj łup]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Na razie!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Witaj, bohaterze!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Aby wesprzeć walkę, Jego Wysokość polecił Zakonowi Architektów i Inżynierów Korony użyczyć naszej wiedzy.

# speaker:engineer
# pace:30
Pomożemy ci na trzy sposoby:

# speaker:engineer
# pace:30
- Budując katapulty do oblężeń.

# speaker:engineer
# pace:30
- Wznosząc budynki drugiego poziomu, rękami naszych budowniczych.

# speaker:engineer
# pace:30
- Zakładając organizacje wyższego poziomu, rękami naszych inżynierów.

# speaker:engineer
# pace:30
Gdy zbierzesz złoto, znajdziesz nas w karcie "Inżynieria".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Och, a co sądziłeś, że znaczy "zwolnić jednostki"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Zabicie mnie ci nie wystarczyło? Przestań mnie dręczyć, proszę!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Ćwir ćwir, ty s**********!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Jestem gotów zagrać dla twoich oddziałów i natchnąć je do zwielokrotnienia sił.

# speaker:bard_dialog
# pace:35
# wait:400
Kliknij przycisk z harfą i ciesz się chwilowym przypływem mocy!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Ratunku!

# speaker:king
# chain_next
# pace:30
# wait:500
Ogromny smok niszczy naszą wioskę!

# speaker:king
# wait:300
# pace:30
- Potrzebujemy bohatera, który nas ocali.

# speaker:king
# pace:30
- Zabij tego smoka swoim potężnym mieczem, to znaczy kursorem myszy.

# speaker:king
# pace:30
- A jeśli starczy ci złota, zdołasz też zwerbować pomoc.

# speaker:king
# pace:30
- Powodzenia!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Jakimś cudem Forth'aarh powrócił!

# speaker:king
# pace:30
# wait:400
Ale rozpuściłeś swoje oddziały. Teraz musisz zwerbować je od nowa.

# speaker:king
# wait:300
# pace:30
- A poprzedni atak zrujnował naszą gospodarkę, więc nie utrzymam twojej armii.

# speaker:king
# pace:40
# chain_next
- Od teraz będą zużywać

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- żywność, drewno i rudę.

# speaker:king
# pace:40
- Będziesz musiał dobrze gospodarować zasobami.

# speaker:king
# pace:40
- Przełączaj, która jednostka ma w danej chwili zużywać zasoby, a która nie.

# speaker:king
# pace:40
- Albo "zwolnij" część z nich: zużyją mniej, a i tak coś zdziałają.

# speaker:king
# pace:28
- Powodzenia!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Niestety nasze jednostki nie zdołały odeprzeć inwazji.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Straciliśmy je co do jednej, a wraz z nimi kwotę okupu.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Oddziały wróciły ze świetnymi wieściami!

# speaker:king
# pace:30
Zdołały odeprzeć inwazję przy minimalnych stratach.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Witamy je z powrotem (i wracamy do mozołu ze smokiem...)

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
Sąsiednie królestwo nas atakuje.

# speaker:king
# pace:30
Żądają {ransomCostLabel} sztuk złota za wstrzymanie inwazji.

# speaker:king
# chain_next
# pace:30
# wait:500
Jak sądzisz, co powinniśmy zrobić?

* [Zapłać {ransomCostLabel} sztuk złota]
    -> pay_enemy

* { unitsCountFew > 3 } [Broń się {unitsCountFew} jednostkami]
    -> send_few_units

* { unitsCountMany > 3 } [Broń się {unitsCountMany} jednostkami]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Miejmy nadzieję, że przyjmą naszą ofertę.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Miejmy nadzieję, że wystarczy.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- To z pewnością odeprze ich atak.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Przynajmniej... nie umarłem biedny.

# speaker:king
# pace:60
# classes:victory
Tak czy inaczej, gratulacje z ukończenia gry.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
ZABIŁEŚ MOJEGO OJCA!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Nie...

# speaker:developer
# pace:100
# classes:vader
Jam jest twój ojciec!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Twórco?

# speaker:princess
# pace:50
Wrzuciłeś do gry dwa nawiązania do Gwiezdnych Wojen? Serio?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Znalazłeś mnie.

# speaker:king
# pace:32
Tak, wziąłem to z legowiska smoka. Złoto dla królestwa. Zabawkę na pamiątkę.

# speaker:king
# pace:30
Nasz lud głodował. Zrobiłbym to znowu.

# speaker:king
# pace:30
Weź łapówkę i milcz, a obaj wyjdziemy z tego cało.

# speaker:king
# pace:30
Zdradzisz mnie czy przyjmiesz mój dar?

* [Trzeba cię powstrzymać!]
  -> go_against_king

* [Lubię złoto!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Niech tak będzie!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Więc weź swoją część.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Dałem ci już więcej złota, niż kiedykolwiek pragnąłeś.

# speaker:king
# pace:30
Taka była umowa. Weź je i odejdź.

* [Nieważne, trzeba cię powstrzymać]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Niech tak będzie!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Za moje złoto kupiłeś armię, która zabiła jego dziecko.

# speaker:king
# pace:32
Nie udawaj niewinnego.

# speaker:king
# pace:30
Chodź więc.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Czyli wpadłeś w długi u korony, co? Spokojnie... gildia ma mnóstwo frajerów, którzy są nam winni pieniądze.


# speaker:rogue
# pace:40
# wait:400
Jak nie płacą, łamiemy parę nóg.

# speaker:rogue
# pace:30
# wait:400
Póki nie wyjdziesz na plus, moi złodzieje będą zbierać dla ciebie złoto dwa razy ostrzej.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Niestety! Nasze zapasy many się wyczerpały.

# speaker:wizard_dialog
# pace:35
# wait:400
Bez arkanicznej esencji nie skieruję zaklęć przeciw smokowi.

# speaker:wizard_dialog
# pace:35
# wait:400
Zajrzyj do menu ulepszeń i kupuj [Uzupełnij manę], ilekroć wyschniemy... byśmy znów mogli uderzyć w bestię!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Czy ktoś widział króla? Zaginął.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Ostatnio widziano go, jak schodził do lochów pod zamkiem.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Witaj!

# pace:45
Jestem Mook, młody i sprawiedliwy!

# pace:50
Król postawił mnie tu, żebyś nie zabłądził, i mówię serio: lubię wskazywać drogę.

# pace:35
Nie wolno mi zejść z tej płytki. "Pomagaj każdemu wędrowcowi", a potem "nie przekraczaj tej linii". Wmawiałem sobie, że to procedura. Ostatnio... już nie jestem taki pewien.

# pace:25
Ale weź tę pochodnię. To jedyna pomoc, jaką wciąż wolno mi podać za linię.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Pozdrawiam, jestem Papieżem.

# speaker:pope
# pace:30
- Nadszedł czas, byś znów dowiódł swojej wiary i wsparł nasz Kościół.

# speaker:pope
# pace:30
- Potrzebuję {contributionCostLabel} sztuk złota, by pomóc ubogim.

* [Daj mu {contributionCostLabel} sztuk złota]
    -> pay_contribution

* [Zmień religię]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Niech twoja dusza zazna nagrody w zaświatach!

# speaker:pope
# pace:30
- Przyjmij tych 100 kapłanów jako wyraz wdzięczności Kościoła.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Niech twoja dusza będzie potępiona w zaświatach!

# speaker:pope
# pace:30
# chain_next
# wait:500
- A także...

# speaker:pope
# pace:30
- Szkoda byłoby, gdyby tego wielkiego jaszczura uzdrowiła wyższa moc...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(odgłosy uzdrawiania\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Mam na sprzedaż żywność, drewno albo rudę za

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
złota. Co wybierasz?

* { canAffordTrading > 0 } [Żywność: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Drewno: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Ruda: {resourceAmountLabel}]
    -> buy_ore

* [Nic]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== farewell ===

# speaker:salesman
Do zobaczenia przy następnym objeździe.

* [Żegnaj]
    -> END

* [Przyjeżdżaj rzadziej]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Rozumiem. Będę wpadał rzadziej.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Wow, naprawdę ci się udało!

# speaker:king
# pace:30
- Ogromne dzięki za zabicie tego smoka. Jesteś naszym bohaterem!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Wreszcie możemy...

# speaker:princess
# classes:scared
# pace:200
Co to był za dźwięk?

# speaker:shadow
# pace:200
# classes:angry
ZABILIŚCIE MOJEGO SYNA!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
A TO

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
DOPIERO

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
wielki smok!

# speaker:princess
# pace:20
# events:resume_game
O nie, pomożesz nam, prawda?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh nie żyje. Dokonałeś tego, czego nie zdołała żadna armia.

# speaker:king
# pace:28
# classes:victory
Dziękuję. Naprawdę.

# speaker:princess
# pace:30
# classes:victory
Chodź za mną... Musimy przygotować się na nowych wrogów, którzy mogą nadejść.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Jak on mógł wrócić?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Nie wiem, jak powrócił.

# speaker:king
# pace:28
- Ale by wstać w taki sposób, trzeba niezwykłej woli.

# speaker:princess
# pace:40
# classes:scared
- I żądzy jakiejś zemsty...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Wiesz, że za każdym razem, gdy wchodzisz do lochu,

# classes:angry-worker
# pace:30
- MUSZĘ ZBUDOWAĆ CAŁY NOWY LABIRYNT RĘCZNIE?!?

# chain_next
# pace:50
- Tygodniami wnosiliśmy te skrzynie. Kazał nie pytać, skąd się wzięły.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Nareszcie!

# pace:40
- Król powiedział, że skończyłem i mogę oddać mu kilof, jak dokończę ten poziom.

  -> END
"""

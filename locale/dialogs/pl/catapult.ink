VAR choosesRock = false
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

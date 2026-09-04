VAR choosesRock = false
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

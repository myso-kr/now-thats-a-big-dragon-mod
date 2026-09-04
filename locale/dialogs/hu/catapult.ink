VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Újra üdv!

# speaker:engineer
Tovább kutattuk az ostromgépedet.

# speaker:engineer
# wait:300
# pace:30
Most már macskákat is tud lőni az ellenségre, és szerintünk ez eldöntheti a harcot.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Úgy hívjuk: "Macs-katapult"

# speaker:engineer
# wait:300
# pace:300
(drámai szünet)

# speaker:engineer
# pace:30
Beruházol az átalakításba, a mostaniakra és a későbbiekre is?

* [Inkább maradok a kőnél]
    -> no_thanks

* [Fizess {catapultCostLabel} aranyat]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Meséld majd el, hogy tetszett!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Meséld majd el, hogy tetszett!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Kár. Azért sok szerencsét.

  -> END

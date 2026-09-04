VAR choosesRock = false
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

VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ne revedem!

# speaker:engineer
Am continuat să lucrăm la arma ta de asediu.

# speaker:engineer
# wait:300
# pace:30
Acum poate arunca pisici în dușman, și credem că răstoarnă toată lupta.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Îi spunem "Pisicapulta"

# speaker:engineer
# wait:300
# pace:300
(o pauză de efect)

# speaker:engineer
# pace:30
Vrei să plătești îmbunătățirea, și pentru asta, și pentru toate care urmează?

* [Prefer să arunc cu bolovani]
    -> no_thanks

* [Plătește {catapultCostLabel} aur]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Spune-ne ce părere ai!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Spune-ne ce părere ai!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Păcat. Mult noroc oricum.

  -> END

VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ci rivediamo!

# speaker:engineer
Abbiamo continuato la ricerca sulla tua macchina d'assedio.

# speaker:engineer
# wait:300
# pace:30
Ora può lanciare gatti contro i nemici, e crediamo che possa cambiare le sorti dello scontro.

# speaker:engineer
# wait:300
# pace:30
# chain_next
La chiamiamo "Gatta-pulta"

# speaker:engineer
# wait:300
# pace:300
(pausa drammatica)

# speaker:engineer
# pace:30
Vuoi investire nella modifica, per questa e per le prossime?

* [Preferisco continuare a lanciare massi]
    -> no_thanks

* [Paga {catapultCostLabel} d'oro]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Facci sapere che te ne pare!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Facci sapere che te ne pare!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Peccato. In bocca al lupo lo stesso.

  -> END

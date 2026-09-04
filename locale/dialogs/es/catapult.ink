VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
¡Hola otra vez!

# speaker:engineer
Hemos seguido investigando tu arma de asedio.

# speaker:engineer
# wait:300
# pace:30
Ahora puede disparar gatos al enemigo, y creemos que puede inclinar la balanza.

# speaker:engineer
# wait:300
# pace:30
# chain_next
La llamamos "Gata-pulta"

# speaker:engineer
# wait:300
# pace:300
(pausa dramática)

# speaker:engineer
# pace:30
¿Quieres invertir en la reforma, para esta y para las próximas?

* [Prefiero seguir disparando rocas]
    -> no_thanks

* [Pagar {catapultCostLabel} de oro]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
¡Ya nos contarás qué te ha parecido!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
¡Ya nos contarás qué te ha parecido!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Qué lástima. Suerte de todos modos.

  -> END

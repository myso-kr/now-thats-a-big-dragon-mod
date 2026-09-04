VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
El reino vecino nos está atacando.

# speaker:king
# pace:30
Piden {ransomCostLabel} monedas de oro para detener su invasión.

# speaker:king
# chain_next
# pace:30
# wait:500
¿Qué crees que deberíamos hacer?

* [Pagar {ransomCostLabel} monedas de oro]
    -> pay_enemy

* { unitsCountFew > 3 } [Defender con {unitsCountFew} unidades]
    -> send_few_units

* { unitsCountMany > 3 } [Defender con {unitsCountMany} unidades]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Esperemos que acepten nuestra oferta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Esperemos que baste.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Con esto seguro que frenamos su ataque.
~ strategyChoice = "send_many_units"

  -> END

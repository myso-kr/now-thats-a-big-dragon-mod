VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Il regno vicino ci sta attaccando.

# speaker:king
# pace:30
Chiedono {ransomCostLabel} monete d'oro per fermare l'invasione.

# speaker:king
# chain_next
# pace:30
# wait:500
Secondo te cosa dovremmo fare?

* [Paga {ransomCostLabel} monete d'oro]
    -> pay_enemy

* { unitsCountFew > 3 } [Difendi con {unitsCountFew} unità]
    -> send_few_units

* { unitsCountMany > 3 } [Difendi con {unitsCountMany} unità]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Speriamo che accettino la nostra offerta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Speriamo che basti.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Con questi respingeremo di certo il loro attacco.
~ strategyChoice = "send_many_units"

  -> END

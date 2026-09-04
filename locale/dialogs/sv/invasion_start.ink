VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Grannriket anfaller oss.

# speaker:king
# pace:30
De begär {ransomCostLabel} guld för att avbryta invasionen.

# speaker:king
# chain_next
# pace:30
# wait:500
Vad tycker du att vi ska göra?

* [Betala {ransomCostLabel} guld]
    -> pay_enemy

* { unitsCountFew > 3 } [Försvara med {unitsCountFew} trupper]
    -> send_few_units

* { unitsCountMany > 3 } [Försvara med {unitsCountMany} trupper]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Låt oss hoppas att de tar erbjudandet.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Låt oss hoppas att det räcker.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Så många slår helt säkert tillbaka dem.
~ strategyChoice = "send_many_units"

  -> END

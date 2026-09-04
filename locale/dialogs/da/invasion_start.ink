VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Nabokongeriget angriber os.

# speaker:king
# pace:30
De kræver {ransomCostLabel} guld for at standse invasionen.

# speaker:king
# chain_next
# pace:30
# wait:500
Hvad synes du, vi skal gøre?

* [Betal {ransomCostLabel} guld]
    -> pay_enemy

* { unitsCountFew > 3 } [Forsvar med {unitsCountFew} tropper]
    -> send_few_units

* { unitsCountMany > 3 } [Forsvar med {unitsCountMany} tropper]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Lad os håbe, de tager imod tilbuddet.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Lad os håbe, det er nok.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Så mange slår dem helt sikkert tilbage.
~ strategyChoice = "send_many_units"

  -> END

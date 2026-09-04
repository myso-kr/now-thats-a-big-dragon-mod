VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Het buurkoninkrijk valt ons aan.

# speaker:king
# pace:30
Ze eisen {ransomCostLabel} goud om de invasie te staken.

# speaker:king
# chain_next
# pace:30
# wait:500
Wat vind jij dat we moeten doen?

* [Betaal {ransomCostLabel} goud]
    -> pay_enemy

* { unitsCountFew > 3 } [Verdedig met {unitsCountFew} troepen]
    -> send_few_units

* { unitsCountMany > 3 } [Verdedig met {unitsCountMany} troepen]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Laten we hopen dat ze het aanbod aannemen.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Laten we hopen dat het genoeg is.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Zo veel slaat ze zeker terug.
~ strategyChoice = "send_many_units"

  -> END

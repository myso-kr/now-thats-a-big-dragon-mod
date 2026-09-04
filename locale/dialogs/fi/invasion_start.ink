VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Naapurikuningaskunta hyökkää kimppuumme.

# speaker:king
# pace:30
He vaativat {ransomCostLabel} kultaa hyökkäyksen lopettamisesta.

# speaker:king
# chain_next
# pace:30
# wait:500
Mitä mieltä olet, mitä meidän pitäisi tehdä?

* [Maksa {ransomCostLabel} kultaa]
    -> pay_enemy

* { unitsCountFew > 3 } [Puolusta {unitsCountFew} joukolla]
    -> send_few_units

* { unitsCountMany > 3 } [Puolusta {unitsCountMany} joukolla]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Toivotaan, että he hyväksyvät tarjouksen.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Toivotaan, että se riittää.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Noin moni torjuu heidät varmasti.
~ strategyChoice = "send_many_units"

  -> END

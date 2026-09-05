VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Το γειτονικό βασίλειο μάς επιτίθεται.

# speaker:king
# pace:30
Ζήτησαν {ransomCostLabel} χρυσά νομίσματα για να σταματήσουν την εισβολή.

# speaker:king
# chain_next
# pace:30
# wait:500
Τι λες να κάνουμε;

* [Πλήρωσε {ransomCostLabel} χρυσά νομίσματα]
    -> pay_enemy

* { unitsCountFew > 3 } [Άμυνα με {unitsCountFew} μονάδες]
    -> send_few_units

* { unitsCountMany > 3 } [Άμυνα με {unitsCountMany} μονάδες]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Ας ελπίσουμε ότι θα δεχτούν την προσφορά μας.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Ας ελπίσουμε ότι φτάνουν.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Σίγουρα αυτό θ' αποκρούσει την επίθεσή τους.
~ strategyChoice = "send_many_units"

  -> END

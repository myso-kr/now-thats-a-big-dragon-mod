VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
A szomszédos királyság megtámadott minket.

# speaker:king
# pace:30
{ransomCostLabel} aranyat kérnek, hogy leállítsák az inváziót.

# speaker:king
# chain_next
# pace:30
# wait:500
Szerinted mit tegyünk?

* [Fizess {ransomCostLabel} aranyat]
    -> pay_enemy

* { unitsCountFew > 3 } [Védekezz {unitsCountFew} egységgel]
    -> send_few_units

* { unitsCountMany > 3 } [Védekezz {unitsCountMany} egységgel]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Reméljük, elfogadják az ajánlatunkat.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Reméljük, ennyi elég lesz.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Ez biztosan visszaveri a támadásukat.
~ strategyChoice = "send_many_units"

  -> END

VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Sąsiednie królestwo nas atakuje.

# speaker:king
# pace:30
Żądają {ransomCostLabel} sztuk złota za wstrzymanie inwazji.

# speaker:king
# chain_next
# pace:30
# wait:500
Jak sądzisz, co powinniśmy zrobić?

* [Zapłać {ransomCostLabel} sztuk złota]
    -> pay_enemy

* { unitsCountFew > 3 } [Broń się {unitsCountFew} jednostkami]
    -> send_few_units

* { unitsCountMany > 3 } [Broń się {unitsCountMany} jednostkami]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Miejmy nadzieję, że przyjmą naszą ofertę.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Miejmy nadzieję, że wystarczy.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- To z pewnością odeprze ich atak.
~ strategyChoice = "send_many_units"

  -> END

VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Kerajaan tetangga menyerang kita.

# speaker:king
# pace:30
Mereka menuntut {ransomCostLabel} emas untuk menghentikan serbuan.

# speaker:king
# chain_next
# pace:30
# wait:500
Menurutmu apa yang harus kita lakukan?

* [Bayar {ransomCostLabel} emas]
    -> pay_enemy

* { unitsCountFew > 3 } [Bertahan dengan {unitsCountFew} pasukan]
    -> send_few_units

* { unitsCountMany > 3 } [Bertahan dengan {unitsCountMany} pasukan]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Semoga mereka menerima tawaran itu.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Semoga itu cukup.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Sebanyak itu pasti menahan mereka.
~ strategyChoice = "send_many_units"

  -> END

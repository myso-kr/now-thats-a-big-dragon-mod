VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Vương quốc láng giềng đang tấn công chúng ta.

# speaker:king
# pace:30
Họ đòi {ransomCostLabel} đồng vàng để dừng cuộc xâm lược.

# speaker:king
# chain_next
# pace:30
# wait:500
Ngươi nghĩ chúng ta nên làm gì?

* [Trả {ransomCostLabel} đồng vàng]
    -> pay_enemy

* { unitsCountFew > 3 } [Phòng thủ với {unitsCountFew} quân]
    -> send_few_units

* { unitsCountMany > 3 } [Phòng thủ với {unitsCountMany} quân]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Mong là họ chấp nhận đề nghị của ta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Mong là chừng đó là đủ.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Chừng này chắc chắn đẩy lui được đòn của họ.
~ strategyChoice = "send_many_units"

  -> END

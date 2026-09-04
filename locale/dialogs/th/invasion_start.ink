VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
อาณาจักรข้างเคียงกำลังโจมตีเรา

# speaker:king
# pace:30
พวกเขาเรียกทอง {ransomCostLabel} เหรียญเพื่อหยุดการรุกราน

# speaker:king
# chain_next
# pace:30
# wait:500
เจ้าคิดว่าเราควรทำอย่างไร?

* [จ่ายทอง {ransomCostLabel} เหรียญ]
    -> pay_enemy

* { unitsCountFew > 3 } [ป้องกันด้วย {unitsCountFew} หน่วย]
    -> send_few_units

* { unitsCountMany > 3 } [ป้องกันด้วย {unitsCountMany} หน่วย]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- หวังว่าพวกเขาจะรับข้อเสนอของเรา
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- หวังว่าเท่านี้จะพอ
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- เท่านี้ต้องต้านการโจมตีของพวกเขาได้แน่
~ strategyChoice = "send_many_units"

  -> END

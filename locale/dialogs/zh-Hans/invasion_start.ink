VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
邻国正在进攻我们。

# speaker:king
# pace:30
他们索要 {ransomCostLabel} 金币来停止入侵。

# speaker:king
# chain_next
# pace:30
# wait:500
你觉得我们该怎么办？

* [支付 {ransomCostLabel} 金币]
    -> pay_enemy

* { unitsCountFew > 3 } [派 {unitsCountFew} 个单位防守]
    -> send_few_units

* { unitsCountMany > 3 } [派 {unitsCountMany} 个单位防守]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 但愿他们肯接受我们的条件。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 但愿这些人够用。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 这下总该能挡住他们的进攻了。
~ strategyChoice = "send_many_units"

  -> END


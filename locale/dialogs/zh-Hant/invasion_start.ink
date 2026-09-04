VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
鄰國正在進攻我們。

# speaker:king
# pace:30
他們索要 {ransomCostLabel} 金幣來停止入侵。

# speaker:king
# chain_next
# pace:30
# wait:500
你覺得我們該怎麼辦？

* [支付 {ransomCostLabel} 金幣]
    -> pay_enemy

* { unitsCountFew > 3 } [派 {unitsCountFew} 個單位防守]
    -> send_few_units

* { unitsCountMany > 3 } [派 {unitsCountMany} 個單位防守]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 但願他們肯接受我們的條件。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 但願這些人夠用。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 這下總該能擋住他們的進攻了。
~ strategyChoice = "send_many_units"

  -> END


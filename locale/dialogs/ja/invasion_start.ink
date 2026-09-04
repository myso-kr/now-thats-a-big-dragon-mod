VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
隣国が攻めてきた。

# speaker:king
# pace:30
侵攻をやめる代わりに金貨{ransomCostLabel}枚を要求しておる。

# speaker:king
# chain_next
# pace:30
# wait:500
どうするのがよいと思う？

* [金貨{ransomCostLabel}枚を払う]
    -> pay_enemy

* { unitsCountFew > 3 } [{unitsCountFew}体で防ぐ]
    -> send_few_units

* { unitsCountMany > 3 } [{unitsCountMany}体で防ぐ]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 受け入れてくれることを願おう。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- これで足りることを願おう。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- これだけあれば必ず退けられよう。
~ strategyChoice = "send_many_units"

  -> END

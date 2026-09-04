VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
またお会いしましたね！

# speaker:engineer
攻城兵器の研究を続けておりました。

# speaker:engineer
# wait:300
# pace:30
今では猫を敵に撃ち出せます。戦いの流れを変えられるかと。

# speaker:engineer
# wait:300
# pace:30
# chain_next
名付けて「キャッタパルト」

# speaker:engineer
# wait:300
# pace:300
（もったいぶった間）

# speaker:engineer
# pace:30
今あるぶんも、これから買うぶんも改修しますか？

* [岩を撃ち続けたい]
    -> no_thanks

* [金貨{catapultCostLabel}を払う]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
感想をぜひ聞かせてください！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
感想をぜひ聞かせてください！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
残念です。ともあれご武運を。

  -> END

VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
又见面了！

# speaker:engineer
我们继续研究了你的攻城武器。

# speaker:engineer
# wait:300
# pace:30
它现在能把猫射向敌人，我们认为这足以扭转战局。

# speaker:engineer
# wait:300
# pace:30
# chain_next
我们管它叫「投猫机」

# speaker:engineer
# wait:300
# pace:300
（意味深长的停顿）

# speaker:engineer
# pace:30
你愿意为现有和今后购买的投石机投资这项改造吗？

* [我还是想继续扔石头]
    -> no_thanks

* [支付 {catapultCostLabel} 金币]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
用后记得告诉我们感想！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
用后记得告诉我们感想！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
真可惜。那也祝你好运。

  -> END


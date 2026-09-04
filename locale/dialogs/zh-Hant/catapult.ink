VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
又見面了！

# speaker:engineer
我們繼續研究了你的攻城武器。

# speaker:engineer
# wait:300
# pace:30
它現在能把貓射向敵人，我們認為這足以扭轉戰局。

# speaker:engineer
# wait:300
# pace:30
# chain_next
我們管它叫「投貓機」

# speaker:engineer
# wait:300
# pace:300
（意味深長的停頓）

# speaker:engineer
# pace:30
你願意為現有和今後購買的投石機投資這項改造嗎？

* [我還是想繼續扔石頭]
    -> no_thanks

* [支付 {catapultCostLabel} 金幣]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
用後記得告訴我們感想！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
用後記得告訴我們感想！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
真可惜。那也祝你好運。

  -> END


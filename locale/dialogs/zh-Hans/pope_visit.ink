VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 你好，我是教皇。

# speaker:pope
# pace:30
- 又到了证明你信仰的时候了，为我们的教会献上一份心意吧。

# speaker:pope
# pace:30
- 我需要 {contributionCostLabel} 金币来救济穷人。

* [付给他 {contributionCostLabel} 金币]
    -> pay_contribution

* [改信别的宗教]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 愿你的灵魂在来世得到嘉奖！

# speaker:pope
# pace:30
- 请收下这 100 名牧师，作为教会的谢礼。

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 愿你的灵魂在来世受到诅咒！

# speaker:pope
# pace:30
# chain_next
# wait:500
- 还有……

# speaker:pope
# pace:30
- 要是那头大蜥蜴被某种更高的力量治愈了，那可就太遗憾了……

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(治疗的声音\)

  -> END

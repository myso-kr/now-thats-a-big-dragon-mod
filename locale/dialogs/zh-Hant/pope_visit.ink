VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 你好，我是教皇。

# speaker:pope
# pace:30
- 又到了證明你信仰的時候了，為我們的教會獻上一份心意吧。

# speaker:pope
# pace:30
- 我需要 {contributionCostLabel} 金幣來救濟窮人。

* [付給他 {contributionCostLabel} 金幣]
    -> pay_contribution

* [改信別的宗教]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 願你的靈魂在來世得到嘉獎！

# speaker:pope
# pace:30
- 請收下這 100 名牧師，作為教會的謝禮。

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 願你的靈魂在來世受到詛咒！

# speaker:pope
# pace:30
# chain_next
# wait:500
- 還有……

# speaker:pope
# pace:30
- 要是那頭大蜥蜴被某種更高的力量治癒了，那可就太遺憾了……

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(治療的聲音\)

  -> END

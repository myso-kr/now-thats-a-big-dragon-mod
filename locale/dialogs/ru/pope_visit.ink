VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Приветствую, я Папа.

# speaker:pope
# pace:30
- Пришло время вновь доказать свою веру и пожертвовать нашей Церкви.

# speaker:pope
# pace:30
- Мне нужно {contributionCostLabel} золотых, чтобы помочь бедным.

* [Дать ему {contributionCostLabel} золотых]
    -> pay_contribution

* [Сменить веру]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Да воздастся душе вашей на том свете!

# speaker:pope
# pace:30
- Примите этих 100 жрецов в знак благодарности Церкви.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Да будет душа ваша проклята на том свете!

# speaker:pope
# pace:30
# chain_next
# wait:500
- И ещё...

# speaker:pope
# pace:30
- Было бы досадно, если бы ту громадную ящерицу исцелила высшая сила...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(звуки исцеления\)

  -> END

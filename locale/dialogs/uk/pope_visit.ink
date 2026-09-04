VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Вітаю, я Папа.

# speaker:pope
# pace:30
- Час знову довести свою віру і пожертвувати нашій Церкві.

# speaker:pope
# pace:30
- Мені потрібно {contributionCostLabel} золотих, щоб допомогти бідним.

* [Дати йому {contributionCostLabel} золотих]
    -> pay_contribution

* [Змінити віру]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Хай душа ваша матиме винагороду на тому світі!

# speaker:pope
# pace:30
- Прийміть цих 100 жерців на знак вдячності Церкви.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Хай душа ваша буде проклята на тому світі!

# speaker:pope
# pace:30
# chain_next
# wait:500
- І ще...

# speaker:pope
# pace:30
- Було б прикро, якби ту величезну ящірку зцілила вища сила...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(звуки зцілення\)

  -> END

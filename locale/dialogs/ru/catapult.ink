VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
И снова здравствуйте!

# speaker:engineer
Мы продолжили работу над вашим осадным орудием.

# speaker:engineer
# wait:300
# pace:30
Теперь оно стреляет котами, и мы думаем, это переломит ход боя.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Мы зовём это "Кот-апульта"

# speaker:engineer
# wait:300
# pace:300
(драматическая пауза)

# speaker:engineer
# pace:30
Вложитесь в переделку - нынешних и будущих орудий?

* [Лучше буду стрелять камнями]
    -> no_thanks

* [Заплатить {catapultCostLabel} золота]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Расскажите потом, как вам!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Расскажите потом, как вам!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Жаль. Что ж, удачи вам.

  -> END

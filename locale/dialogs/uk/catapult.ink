VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
І знову вітаю!

# speaker:engineer
Ми продовжили роботу над вашою облоговою машиною.

# speaker:engineer
# wait:300
# pace:30
Тепер вона стріляє котами, і ми думаємо, це переламає хід бою.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Ми звемо це "Кото-пульта"

# speaker:engineer
# wait:300
# pace:300
(драматична пауза)

# speaker:engineer
# pace:30
Вкладетеся в переробку - нинішніх і майбутніх машин?

* [Краще стрілятиму камінням]
    -> no_thanks

* [Заплатити {catapultCostLabel} золота]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Розкажіть потім, як вам!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Розкажіть потім, як вам!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Шкода. Що ж, щасти вам.

  -> END

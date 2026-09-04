VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Сусіднє королівство напало на нас.

# speaker:king
# pace:30
Вони вимагають {ransomCostLabel} золотих, щоб спинити вторгнення.

# speaker:king
# chain_next
# pace:30
# wait:500
Як гадаєте, що нам робити?

* [Заплатити {ransomCostLabel} золотих]
    -> pay_enemy

* { unitsCountFew > 3 } [Оборона: {unitsCountFew} бійців]
    -> send_few_units

* { unitsCountMany > 3 } [Оборона: {unitsCountMany} бійців]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Сподіваймося, вони приймуть нашу пропозицію.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Сподіваймося, цього вистачить.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Оце вже точно відіб'є їхній натиск.
~ strategyChoice = "send_many_units"

  -> END

VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Соседнее королевство напало на нас.

# speaker:king
# pace:30
Они требуют {ransomCostLabel} золотых, чтобы остановить вторжение.

# speaker:king
# chain_next
# pace:30
# wait:500
Как думаете, что нам делать?

* [Заплатить {ransomCostLabel} золотых]
    -> pay_enemy

* { unitsCountFew > 3 } [Оборона: {unitsCountFew} бойцов]
    -> send_few_units

* { unitsCountMany > 3 } [Оборона: {unitsCountMany} бойцов]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Будем надеяться, они примут наше предложение.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Будем надеяться, этого хватит.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Уж это точно отобьёт их натиск.
~ strategyChoice = "send_many_units"

  -> END

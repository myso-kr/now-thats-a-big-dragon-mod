VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Продаю еду, древесину или руду - по

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
золота. Что желаете взять?

* { canAffordTrading > 0 } [Еда: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Древесина: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Руда: {resourceAmountLabel}]
    -> buy_ore

* [Ничего]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== farewell ===

# speaker:salesman
Увидимся в следующий заход.

* [Прощайте]
    -> END

* [Заходите пореже]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Понял. Буду наведываться реже.

  -> END

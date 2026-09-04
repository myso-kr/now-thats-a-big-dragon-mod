VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Продаю їжу, деревину або руду - по

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
золота. Що бажаєте взяти?

* { canAffordTrading > 0 } [Їжа: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Деревина: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Руда: {resourceAmountLabel}]
    -> buy_ore

* [Нічого]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== farewell ===

# speaker:salesman
Побачимося наступного разу.

* [Прощавайте]
    -> END

* [Заїжджайте рідше]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Зрозумів. Навідуватимуся рідше.

  -> END

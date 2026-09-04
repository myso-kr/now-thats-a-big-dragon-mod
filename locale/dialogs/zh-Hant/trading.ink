VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
我這兒有食物、木材和礦石，售價

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
金幣。你想買哪一樣？

* { canAffordTrading > 0 } [{resourceAmountLabel} 食物]
    -> buy_food

* { canAffordTrading > 0 } [{resourceAmountLabel} 木材]
    -> buy_wood

* { canAffordTrading > 0 } [{resourceAmountLabel} 礦石]
    -> buy_ore

* [都不要]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== farewell ===

# speaker:salesman
下次跑商再見。

* [再會]
    -> END

* [來得少一些吧]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
明白了。我會把來訪間隔拉長些。

  -> END

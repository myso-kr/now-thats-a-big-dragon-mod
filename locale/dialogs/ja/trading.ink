VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
食料、木材、鉱石を売ってるよ。お代は

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
金貨。どれにする？

* { canAffordTrading > 0 } [食料 {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [木材 {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [鉱石 {resourceAmountLabel}]
    -> buy_ore

* [何もいらない]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== farewell ===

# speaker:salesman
次の行商でまた会おう。

* [ではまた]
    -> END

* [来る回数を減らしてくれ]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
承知した。間を空けて回ることにするよ。

  -> END

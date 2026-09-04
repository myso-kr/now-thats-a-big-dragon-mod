VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Vând hrană, lemn sau minereu cu

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
aur. Ce dorești?

* { canAffordTrading > 0 } [Hrană: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Lemn: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Minereu: {resourceAmountLabel}]
    -> buy_ore

* [Nimic, mulțumesc]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Mulțumesc, ne vedem data viitoare.

  -> END


=== farewell ===

# speaker:salesman
Ne vedem data viitoare.

* [La revedere]
    -> END

* [Vino mai rar]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Am înțeles. Vin mai rar.

  -> END

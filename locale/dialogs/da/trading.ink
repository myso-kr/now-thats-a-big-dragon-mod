VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jeg sælger mad, træ eller malm for

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
guld. Hvad skal du have?

* { canAffordTrading > 0 } [Mad: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Træ: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ikke noget, tak]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Tak, vi ses næste gang.

  -> END


=== farewell ===

# speaker:salesman
Vi ses næste gang.

* [Farvel]
    -> END

* [Kom lidt sjældnere]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Forstået. Jeg kommer sjældnere.

  -> END

VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Myyn ruokaa, puuta tai malmia hintaan

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
kultaa. Mitä otat?

* { canAffordTrading > 0 } [Ruoka: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Puu: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malmi: {resourceAmountLabel}]
    -> buy_ore

* [En mitään, kiitos]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Kiitos, nähdään ensi kerralla.

  -> END


=== farewell ===

# speaker:salesman
Nähdään ensi kerralla.

* [Näkemiin]
    -> END

* [Tule harvemmin]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Selvä. Tulen harvemmin.

  -> END

VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jeg selger mat, tømmer eller malm for

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
gull. Hva skal du ha?

* { canAffordTrading > 0 } [Mat: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Tømmer: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ingenting, takk]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Takk, vi ses neste gang.

  -> END


=== farewell ===

# speaker:salesman
Vi ses neste gang.

* [Ha det]
    -> END

* [Kom litt sjeldnere]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Forstått. Jeg kommer sjeldnere.

  -> END

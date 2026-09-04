VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Jag säljer mat, trä eller malm för

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
guld. Vad vill du ha?

* { canAffordTrading > 0 } [Mat: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Trä: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Malm: {resourceAmountLabel}]
    -> buy_ore

* [Ingenting, tack]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Tack, vi ses nästa gång.

  -> END


=== farewell ===

# speaker:salesman
Vi ses nästa gång.

* [Adjö]
    -> END

* [Kom mer sällan]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Uppfattat. Jag kommer mer sällan.

  -> END

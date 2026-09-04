VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Ik verkoop voedsel, hout of erts voor

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
goud. Wat wil je hebben?

* { canAffordTrading > 0 } [Voedsel: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Hout: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Erts: {resourceAmountLabel}]
    -> buy_ore

* [Niets, dank je]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Dank je, tot de volgende keer.

  -> END


=== farewell ===

# speaker:salesman
Tot de volgende keer.

* [Dag]
    -> END

* [Kom wat minder vaak]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Begrepen. Ik kom minder vaak langs.

  -> END

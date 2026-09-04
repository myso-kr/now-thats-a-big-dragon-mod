VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Van élelmem, fám vagy ércem eladó, ennyiért:

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
arany. Melyiket kéred?

* { canAffordTrading > 0 } [Élelem: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Fa: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Érc: {resourceAmountLabel}]
    -> buy_ore

* [Semmit]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Köszönöm, a következő körnél találkozunk.

  -> END


=== farewell ===

# speaker:salesman
A következő körnél találkozunk.

* [Ég veled]
    -> END

* [Gyere ritkábban]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Értem. Ritkábban jövök majd.

  -> END

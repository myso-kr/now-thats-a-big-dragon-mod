VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Prodávám jídlo, dřevo nebo rudu za

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
zlata. Co si vybereš?

* { canAffordTrading > 0 } [Jídlo: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Dřevo: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Ruda: {resourceAmountLabel}]
    -> buy_ore

* [Nic]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Díky, uvidíme se na příští cestě.

  -> END


=== farewell ===

# speaker:salesman
Uvidíme se na příští cestě.

* [Sbohem]
    -> END

* [Jezdi míň často]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Rozumím. Budu jezdit řidčeji.

  -> END

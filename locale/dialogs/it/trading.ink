VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Ho cibo, legname o minerale da vendere per

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
d'oro. Quale vuoi?

* { canAffordTrading > 0 } [Cibo: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Legname: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Minerale: {resourceAmountLabel}]
    -> buy_ore

* [Niente]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== farewell ===

# speaker:salesman
Ci vediamo al prossimo giro.

* [Addio]
    -> END

* [Passa più di rado]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Capito. Dirado le visite.

  -> END

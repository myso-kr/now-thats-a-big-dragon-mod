VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Vendo alimento, madera o mineral por

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
de oro. ¿Cuál quieres llevarte?

* { canAffordTrading > 0 } [Alimento: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Madera: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Mineral: {resourceAmountLabel}]
    -> buy_ore

* [Nada]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== farewell ===

# speaker:salesman
Nos vemos en mi próxima ruta.

* [Adiós]
    -> END

* [Ven menos a menudo]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Entendido. Espaciaré mis visitas.

  -> END

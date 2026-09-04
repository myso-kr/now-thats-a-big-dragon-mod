VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Mam na sprzedaż żywność, drewno albo rudę za

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
złota. Co wybierasz?

* { canAffordTrading > 0 } [Żywność: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Drewno: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Ruda: {resourceAmountLabel}]
    -> buy_ore

* [Nic]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Dzięki, do zobaczenia przy następnym objeździe.

  -> END


=== farewell ===

# speaker:salesman
Do zobaczenia przy następnym objeździe.

* [Żegnaj]
    -> END

* [Przyjeżdżaj rzadziej]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Rozumiem. Będę wpadał rzadziej.

  -> END

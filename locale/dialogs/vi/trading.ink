VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Tôi có lương thực, gỗ hoặc quặng để bán, giá

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
vàng. Bạn muốn lấy thứ nào?

* { canAffordTrading > 0 } [Lương thực: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Gỗ: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Quặng: {resourceAmountLabel}]
    -> buy_ore

* [Không lấy gì]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== farewell ===

# speaker:salesman
Hẹn gặp lại chuyến sau.

* [Tạm biệt]
    -> END

* [Ghé thưa thớt lại]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Hiểu rồi. Tôi sẽ ghé thưa hơn.

  -> END

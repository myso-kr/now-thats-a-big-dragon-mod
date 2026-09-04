VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
식량, 목재, 광석을 팝니다. 가격은

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
금화올시다. 어느 것으로 드릴까요?

* { canAffordTrading > 0 } [식량 {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [목재 {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [광석 {resourceAmountLabel}]
    -> buy_ore

* [사지 않겠소]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== farewell ===

# speaker:salesman
다음 행상 때 또 뵙지요.

* [잘 가시오]
    -> END

* [좀 덜 오시오]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
알겠습니다. 방문 간격을 늘리지요.

  -> END

VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
มีอาหาร ไม้ หรือแร่ ขายในราคา

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
ทอง อยากได้อันไหน?

* { canAffordTrading > 0 } [อาหาร {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [ไม้ {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [แร่ {resourceAmountLabel}]
    -> buy_ore

* [ไม่เอาอะไร]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== farewell ===

# speaker:salesman
เจอกันรอบหน้าที่ผ่านมาทางนี้

* [ลาก่อน]
    -> END

* [มาให้น้อยลงหน่อย]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
เข้าใจแล้ว จะเว้นระยะการมาให้ห่างขึ้น

  -> END

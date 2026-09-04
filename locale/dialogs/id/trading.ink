VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Aku menjual pangan, kayu, atau bijih seharga

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
emas. Kamu mau yang mana?

* { canAffordTrading > 0 } [Pangan: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Kayu: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Bijih: {resourceAmountLabel}]
    -> buy_ore

* [Tidak usah, terima kasih]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== farewell ===

# speaker:salesman
Sampai jumpa lain kali.

* [Selamat tinggal]
    -> END

* [Datanglah lebih jarang]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Mengerti. Aku akan lebih jarang datang.

  -> END

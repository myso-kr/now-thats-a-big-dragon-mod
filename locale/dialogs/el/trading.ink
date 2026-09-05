VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Έχω τροφή, ξύλο ή μετάλλευμα να πουλήσω για

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
χρυσάφι. Ποιο θέλεις ν' αγοράσεις;

* { canAffordTrading > 0 } [{resourceAmountLabel} Τροφή]
    -> buy_food

* { canAffordTrading > 0 } [{resourceAmountLabel} Ξύλο]
    -> buy_wood

* { canAffordTrading > 0 } [{resourceAmountLabel} Μετάλλευμα ]
    -> buy_ore

* [Κανένα]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== farewell ===

# speaker:salesman
Τα λέμε στο επόμενο πέρασμά μου.

* [Στο καλό]
    -> END

* [Να έρχεσαι πιο αραιά]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Κατάλαβα. Θ' αραιώσω τις επισκέψεις μου.

  -> END

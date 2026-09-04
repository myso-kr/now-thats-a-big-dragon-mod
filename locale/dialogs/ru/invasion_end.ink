VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Увы, наших бойцов не хватило, чтобы отбить вторжение.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Мы потеряли всех до единого, а вместе с ними и сумму выкупа.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Войска вернулись с добрыми вестями!

# speaker:king
# pace:30
Им удалось отбить вторжение с минимальными потерями.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Встречаем их дома (и продолжаем гринд против дракона...)

  -> END

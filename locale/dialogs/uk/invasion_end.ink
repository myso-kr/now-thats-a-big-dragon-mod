VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
На жаль, наших бійців не вистачило, щоб відбити вторгнення.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ми втратили всіх до одного, а разом з ними й суму викупу.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Загони повернулися з доброю звісткою!

# speaker:king
# pace:30
Їм вдалося відбити вторгнення з мінімальними втратами.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Зустрічаємо їх удома (і повертаємося до гринду проти дракона...)

  -> END

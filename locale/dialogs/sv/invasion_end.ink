VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Tyvärr räckte inte våra trupper till för att slå tillbaka invasionen.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jag förlorade alla trupperna, och lösensumman därtill.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Trupperna är tillbaka med goda nyheter!

# speaker:king
# pace:30
De slog tillbaka invasionen med små förluster.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jag tar emot dem (så att de kan gå tillbaka till draken...)

  -> END

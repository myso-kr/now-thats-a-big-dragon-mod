VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Desværre var vores tropper ikke nok til at slå invasionen tilbage.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jeg mistede alle tropperne, og løsesummen med.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Vores tropper er tilbage med gode nyheder!

# speaker:king
# pace:30
De slog invasionen tilbage med små tab.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jeg tager imod dem (så de kan komme tilbage til dragen...)

  -> END

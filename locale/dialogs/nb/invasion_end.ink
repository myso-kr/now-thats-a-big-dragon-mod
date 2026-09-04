VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Dessverre var ikke troppene våre nok til å slå tilbake invasjonen.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Jeg mistet alle troppene, og løsepengene med.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Troppene våre er tilbake med gode nyheter!

# speaker:king
# pace:30
De slo tilbake invasjonen med små tap.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Jeg tar imot dem (så de kan komme tilbake til dragen...)

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Purtroppo le nostre unità non sono bastate a respingere l'invasione.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Le abbiamo perse tutte e, con esse, anche la somma del riscatto.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Le truppe sono tornate con ottime notizie!

# speaker:king
# pace:30
Sono riuscite a respingere l'invasione con perdite minime.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Le riaccogliamo (per tornare a macinare contro il drago...)

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Din păcate, trupele noastre n-au fost de ajuns ca să respingă invazia.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Am pierdut toate trupele, și răscumpărarea pe deasupra.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Trupele noastre s-au întors cu vești bune!

# speaker:king
# pace:30
Au respins invazia cu pierderi mici.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Le primesc înapoi (ca să se întoarcă la dragon...)

  -> END

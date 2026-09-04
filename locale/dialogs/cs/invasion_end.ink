VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Bohužel naše jednotky na odražení invaze nestačily.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ztratili jsme je do jedné a s nimi i částku výkupného.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Jednotky se vrátily se skvělými zprávami!

# speaker:king
# pace:30
Podařilo se jim odrazit invazi s minimálními ztrátami.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Vítáme je zpět (a jdeme dál dřít na draka...)

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Helaas waren onze troepen niet genoeg om de invasie af te slaan.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ik ben al mijn troepen kwijt, en het losgeld ook.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Onze troepen zijn terug met goed nieuws!

# speaker:king
# pace:30
Ze hebben de invasie afgeslagen met weinig verliezen.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Ik neem ze op (zodat ze weer aan de draak kunnen beginnen...)

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Valitettavasti joukkomme eivät riittäneet torjumaan hyökkäystä.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Menetin kaikki joukot, ja lunnaat siinä sivussa.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Joukkomme ovat palanneet hyvien uutisten kanssa!

# speaker:king
# pace:30
Ne torjuivat hyökkäyksen vähäisin tappioin.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Otan heidät vastaan (jotta he pääsevät takaisin lohikäärmeen kimppuun...)

  -> END

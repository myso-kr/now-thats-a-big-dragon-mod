VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Sajnos az egységeink nem voltak elegen az invázió visszaveréséhez.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Mind egy szálig odavesztek, és velük a váltságdíj összege is.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Az egységek nagyszerű hírekkel tértek vissza!

# speaker:king
# pace:30
Minimális veszteséggel verték vissza az inváziót.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Visszavárjuk őket (hogy folytassuk a robotot a sárkány ellen...)

  -> END

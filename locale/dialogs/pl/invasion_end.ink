VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Niestety nasze jednostki nie zdołały odeprzeć inwazji.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Straciliśmy je co do jednej, a wraz z nimi kwotę okupu.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Oddziały wróciły ze świetnymi wieściami!

# speaker:king
# pace:30
Zdołały odeprzeć inwazję przy minimalnych stratach.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Witamy je z powrotem (i wracamy do mozołu ze smokiem...)

  -> END

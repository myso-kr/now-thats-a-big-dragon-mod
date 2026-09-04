VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Sayangnya pasukan kita tidak cukup untuk menahan serbuan itu.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Aku kehilangan seluruh pasukan, dan uang tebusannya juga.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Pasukan kita kembali dengan kabar baik!

# speaker:king
# pace:30
Mereka menahan serbuan itu dengan korban yang sedikit.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Aku menyambut mereka (agar bisa kembali menghadapi naga...)

  -> END

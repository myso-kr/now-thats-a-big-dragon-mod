VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Δυστυχώς οι μονάδες μας δεν έφτασαν για ν' αποκρούσουν την εισβολή.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Χάσαμε και την τελευταία μονάδα, και μαζί χάσαμε και το ποσό των λύτρων.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Τα στρατεύματά μας γύρισαν με σπουδαία νέα!

# speaker:king
# pace:30
Κατάφεραν ν' αποκρούσουν την εισβολή με ελάχιστες απώλειες.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Τα καλωσορίζουμε πίσω (για να συνεχίσουν την αγγαρεία με τον δράκο...)

  -> END

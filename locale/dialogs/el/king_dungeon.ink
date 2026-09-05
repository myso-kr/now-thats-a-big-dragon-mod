# speaker:king
# pace:40
Με βρήκες.

# speaker:king
# pace:32
Ναι, πήρα από τη φωλιά του δράκου. Χρυσάφι για το βασίλειο. Κι εκείνο το παιχνίδι για ενθύμιο.

# speaker:king
# pace:30
Ο λαός μας πέθαινε της πείνας. Θα το ξανάκανα.

# speaker:king
# pace:30
Πάρε ένα λάδωμα και σώπα, και φεύγουμε κι οι δυο μας καθαροί.

# speaker:king
# pace:30
Θα με προδώσεις ή θα δεχτείς το δώρο μου;

* [Πρέπει να σε σταματήσω!]
  -> go_against_king

* [Μ' αρέσει το χρυσάφι!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Ας γίνει έτσι!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Πάρε τότε το μερίδιό σου.

  -> END

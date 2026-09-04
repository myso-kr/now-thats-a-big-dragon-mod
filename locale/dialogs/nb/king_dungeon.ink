# speaker:king
# pace:40
Så du fant meg.

# speaker:king
# pace:32
Ja, jeg tok det fra dragens hule. Gullet til kongeriket. Leken som minne.

# speaker:king
# pace:30
Folket mitt sultet. Jeg ville gjort det igjen.

# speaker:king
# pace:30
Ta en bestikkelse og ti stille, så slipper vi begge bryet.

# speaker:king
# pace:30
Forråder du meg, eller tar du imot gaven min?

* [Noen må stoppe deg!]
  -> go_against_king

* [Jeg liker gull, jeg også!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så får det bli slik!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ta din del, da.

  -> END

# speaker:king
# pace:40
Så du fandt mig.

# speaker:king
# pace:32
Ja, jeg tog det fra dragens hule. Guldet til kongeriget. Legetøjet som minde.

# speaker:king
# pace:30
Mit folk sultede. Jeg ville gøre det igen.

# speaker:king
# pace:30
Tag en bestikkelse og ti stille, så slipper vi begge for besvær.

# speaker:king
# pace:30
Forråder du mig, eller tager du imod min gave?

* [Nogen må stoppe dig!]
  -> go_against_king

* [Jeg kan også godt lide guld!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Så lad gå!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Tag så din del.

  -> END

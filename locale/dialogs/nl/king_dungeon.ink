# speaker:king
# pace:40
Dus je hebt me gevonden.

# speaker:king
# pace:32
Ja, ik heb het uit het hol van de draak gehaald. Het goud voor het koninkrijk. Het speeltje als aandenken.

# speaker:king
# pace:30
Mijn volk had honger. Ik zou het zo weer doen.

# speaker:king
# pace:30
Neem een omkoopsom en zwijg, dan hebben we er allebei geen last van.

# speaker:king
# pace:30
Verraad je me, of neem je mijn geschenk aan?

* [Iemand moet je tegenhouden!]
  -> go_against_king

* [Ik hou ook wel van goud!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Goed dan!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Neem dan je deel.

  -> END

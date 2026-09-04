# speaker:king
# pace:40
Deci m-ai găsit.

# speaker:king
# pace:32
Da, l-am luat din vizuina dragonului. Aurul pentru regat. Jucăria ca amintire.

# speaker:king
# pace:30
Poporul meu flămânzea. Aș face-o din nou.

# speaker:king
# pace:30
Ia o mită și taci, și scăpăm amândoi de necaz.

# speaker:king
# pace:30
Mă trădezi, sau primești darul meu?

* [Cineva trebuie să te oprească!]
  -> go_against_king

* [Și mie îmi place aurul!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Fie și așa!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Atunci ia-ți partea.

  -> END

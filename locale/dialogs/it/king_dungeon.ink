# speaker:king
# pace:40
Mi hai trovato.

# speaker:king
# pace:32
Sì, l'ho preso dalla tana del drago. L'oro per il regno. Il giocattolo come ricordo.

# speaker:king
# pace:30
La nostra gente moriva di fame. Lo rifarei.

# speaker:king
# pace:30
Prendi una bustarella e taci, e ne usciremo entrambi puliti.

# speaker:king
# pace:30
Mi tradisci o accetti il mio dono?

* [Bisogna fermarti!]
  -> go_against_king

* [L'oro mi piace eccome!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
E così sia!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Allora prendi la tua parte.

  -> END

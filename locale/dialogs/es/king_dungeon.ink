# speaker:king
# pace:40
Me has encontrado.

# speaker:king
# pace:32
Sí, lo saqué de la guarida del dragón. El oro, para el reino. El juguete, de recuerdo.

# speaker:king
# pace:30
Nuestro pueblo pasaba hambre. Lo volvería a hacer.

# speaker:king
# pace:30
Acepta un soborno y calla, y los dos saldremos de esta.

# speaker:king
# pace:30
¿Me traicionas o aceptas mi regalo?

* [¡Hay que detenerte!]
  -> go_against_king

* [¡Sí que me gusta el oro!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
¡Que así sea!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Entonces toma tu parte.

  -> END

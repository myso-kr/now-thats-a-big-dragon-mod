# speaker:king
# pace:40
Joten löysit minut.

# speaker:king
# pace:32
Kyllä, otin sen lohikäärmeen luolasta. Kullat kuningaskunnalle. Lelun muistoksi.

# speaker:king
# pace:30
Kansani näki nälkää. Tekisin sen uudestaan.

# speaker:king
# pace:30
Ota lahjus ja vaikene, niin kummallekaan ei tule harmia.

# speaker:king
# pace:30
Petätkö minut, vai otatko lahjani vastaan?

* [Jonkun on pysäytettävä sinut!]
  -> go_against_king

* [Minäkin pidän kullasta!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Olkoon sitten!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ota sitten osasi.

  -> END

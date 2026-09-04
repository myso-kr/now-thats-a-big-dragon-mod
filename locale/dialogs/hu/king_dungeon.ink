# speaker:king
# pace:40
Megtaláltál.

# speaker:king
# pace:32
Igen, a sárkány odújából vittem el. Az aranyat a királyságnak. A játékot emlékbe.

# speaker:king
# pace:30
A népünk éhezett. Újra megtenném.

# speaker:king
# pace:30
Fogadd el a kenőpénzt és hallgass, és mindketten tisztán jövünk ki ebből.

# speaker:king
# pace:30
Elárulsz, vagy elfogadod az ajándékomat?

* [Meg kell állítani téged!]
  -> go_against_king

* [Szeretem az aranyat!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Legyen hát!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Akkor vedd el a részed.

  -> END

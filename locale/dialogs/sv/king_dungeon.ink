# speaker:king
# pace:40
Så du hittade mig.

# speaker:king
# pace:32
Ja, jag tog det ur drakens håla. Guldet åt kungariket. Leksaken som minne.

# speaker:king
# pace:30
Mitt folk svälter. Jag skulle göra om det.

# speaker:king
# pace:30
Ta en muta och tig, så slipper vi båda besvär.

# speaker:king
# pace:30
Förråder du mig, eller tar du emot min gåva?

* [Någon måste stoppa dig!]
  -> go_against_king

* [Jag gillar också guld!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Nåväl!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ta då din del.

  -> END

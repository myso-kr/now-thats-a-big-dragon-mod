# pace:35
# chain_next
Hej! Det er mig, der har lavet spillet.

# pace:40
Undskyld, du faldt gennem en væg. Det er min skyld.

# pace:30
Jeg får dig ud af tomrummet, og du beholder hele byttet.

* [Giv op og behold byttet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Farvel!
  -> END

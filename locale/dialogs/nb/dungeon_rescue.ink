# pace:35
# chain_next
Hei! Det er jeg som har laget spillet.

# pace:40
Beklager at du falt gjennom en vegg. Det er min feil.

# pace:30
Jeg får deg ut av tomrommet, og du beholder hele byttet.

* [Gi opp og behold byttet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Ha det!
  -> END

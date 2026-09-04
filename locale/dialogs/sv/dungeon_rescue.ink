# pace:35
# chain_next
Hej! Det är jag som gjort spelet.

# pace:40
Ledsen att du gick igenom en vägg. Det är mitt fel.

# pace:30
Jag hjälper dig ut ur tomrummet, och du får behålla allt bytet.

* [Ge upp och behåll bytet]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Hej då!
  -> END

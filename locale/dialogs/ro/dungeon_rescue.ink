# pace:35
# chain_next
Salut! Eu am făcut jocul ăsta.

# pace:40
Îmi pare rău că ai căzut prin perete. E vina mea.

# pace:30
Te scot din gol, și rămâi cu toată prada.

* [Renunță și păstrează prada]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Pa!
  -> END

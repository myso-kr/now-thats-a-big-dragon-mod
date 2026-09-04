# pace:35
# chain_next
Hej! Tu twórca gry.

# pace:40
Przepraszam, że przeniknąłeś przez ścianę. To mój błąd.

# pace:30
Wyprowadzę cię z pustki, a cały łup zostanie przy tobie.

* [Poddaj się i zachowaj łup]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Na razie!
  -> END

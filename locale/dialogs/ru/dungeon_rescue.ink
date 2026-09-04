# pace:35
# chain_next
Эй! Это я, разработчик.

# pace:40
Извини, ты провалился сквозь стену. Это мой баг.

# pace:30
Я выведу тебя из пустоты, и вся добыча останется при тебе.

* [Сдаться и оставить добычу]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Пока!
  -> END

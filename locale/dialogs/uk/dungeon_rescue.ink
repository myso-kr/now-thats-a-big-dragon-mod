# pace:35
# chain_next
Гей! Це я, розробник.

# pace:40
Вибач, ти провалився крізь стіну. Це мій баг.

# pace:30
Я виведу тебе з порожнечі, і вся здобич лишиться при тобі.

* [Здатися і лишити здобич]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Бувай!
  -> END

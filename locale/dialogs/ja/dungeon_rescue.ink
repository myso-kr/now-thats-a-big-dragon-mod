# pace:35
# chain_next
やあ！ 開発者だよ。

# pace:40
壁をすり抜けさせてごめん。こっちのバグだ。

# pace:30
虚空から出してあげる。戦利品はぜんぶそのままだよ。

* [あきらめて戦利品を持ち帰る]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
じゃあね！
  -> END

# speaker:king
# pace:40
你找到我了。

# speaker:king
# pace:32
没错，我从龙巢里拿了东西。金币是给王国的。那个玩具算个纪念品。

# speaker:king
# pace:30
我们的子民在挨饿。换一次我还会这么做。

# speaker:king
# pace:30
收下这笔封口费，你我都能全身而退。

# speaker:king
# pace:30
是要背叛我，还是收下我的好意？

* [必须有人阻止你！]
  -> go_against_king

* [我确实挺喜欢金币的！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就这样吧！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
那就拿走你那一份。

  -> END

# speaker:king
# pace:40
你找到我了。

# speaker:king
# pace:32
沒錯，我從龍巢裡拿了東西。金幣是給王國的。那個玩具算個紀念品。

# speaker:king
# pace:30
我們的子民在捱餓。換一次我還會這麼做。

# speaker:king
# pace:30
收下這筆封口費，你我都能全身而退。

# speaker:king
# pace:30
是要背叛我，還是收下我的好意？

* [必須有人阻止你！]
  -> go_against_king

* [我確實挺喜歡金幣的！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就這樣吧！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
那就拿走你那一份。

  -> END

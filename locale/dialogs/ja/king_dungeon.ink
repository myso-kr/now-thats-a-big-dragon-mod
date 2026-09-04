# speaker:king
# pace:40
見つかってしまったか。

# speaker:king
# pace:32
そうだ、ドラゴンの巣から持ち出した。金貨は王国のため。あの人形は土産にな。

# speaker:king
# pace:30
民は飢えていた。何度でも同じことをする。

# speaker:king
# pace:30
袖の下を受け取って黙っておれ。それで互いに無事に済む。

# speaker:king
# pace:30
我を裏切るか、贈り物を受けるか。

* [あなたを止めねばならない！]
  -> go_against_king

* [金貨は好きだ！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
ならばよい！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
では、そなたの取り分だ。

  -> END

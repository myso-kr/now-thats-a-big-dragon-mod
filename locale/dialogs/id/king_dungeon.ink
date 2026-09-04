# speaker:king
# pace:40
Jadi kamu menemukanku.

# speaker:king
# pace:32
Ya, aku mengambilnya dari sarang naga. Emasnya untuk kerajaan. Mainannya sebagai kenang-kenangan.

# speaker:king
# pace:30
Rakyatku kelaparan. Aku akan melakukannya lagi.

# speaker:king
# pace:30
Terima suap dan diamlah, biar kita berdua tidak repot.

# speaker:king
# pace:30
Kamu mengkhianatiku, atau menerima pemberianku?

* [Seseorang harus menghentikanmu!]
  -> go_against_king

* [Aku juga suka emas!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Kalau begitu, baiklah!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ambil bagianmu kalau begitu.

  -> END

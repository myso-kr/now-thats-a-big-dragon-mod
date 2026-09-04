# speaker:king
# pace:40
Вы меня нашли.

# speaker:king
# pace:32
Да, я взял это из логова дракона. Золото - королевству. Игрушку - на память.

# speaker:king
# pace:30
Наш народ голодал. Я поступил бы так снова.

# speaker:king
# pace:30
Возьмите отступного и молчите - и мы оба выйдем отсюда целыми.

# speaker:king
# pace:30
Предать меня или принять мой дар?

* [Вас нужно остановить!]
  -> go_against_king

* [Золото я люблю!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Да будет так!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Тогда забирайте свою долю.

  -> END

# speaker:king
# pace:40
Ви мене знайшли.

# speaker:king
# pace:32
Так, я взяв це з драконового лігва. Золото - королівству. Іграшку - на згадку.

# speaker:king
# pace:30
Наш народ голодував. Я вчинив би так знову.

# speaker:king
# pace:30
Візьміть відступне й мовчіть - і ми обидва вийдемо звідси цілими.

# speaker:king
# pace:30
Зрадите мене чи приймете мій дар?

* [Вас треба спинити!]
  -> go_against_king

* [Золото я люблю!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Хай буде так!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Тоді забирайте свою частку.

  -> END

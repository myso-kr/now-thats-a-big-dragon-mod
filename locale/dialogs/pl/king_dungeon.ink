# speaker:king
# pace:40
Znalazłeś mnie.

# speaker:king
# pace:32
Tak, wziąłem to z legowiska smoka. Złoto dla królestwa. Zabawkę na pamiątkę.

# speaker:king
# pace:30
Nasz lud głodował. Zrobiłbym to znowu.

# speaker:king
# pace:30
Weź łapówkę i milcz, a obaj wyjdziemy z tego cało.

# speaker:king
# pace:30
Zdradzisz mnie czy przyjmiesz mój dar?

* [Trzeba cię powstrzymać!]
  -> go_against_king

* [Lubię złoto!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Niech tak będzie!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Więc weź swoją część.

  -> END

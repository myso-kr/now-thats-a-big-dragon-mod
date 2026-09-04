VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
残念だが、我らの兵では侵攻を防ぎきれなかった。

# speaker:king
# pace:20
# events:resume_dialogs_timer
兵は一人残らず失い、身代金の額まで失った。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
部隊が吉報とともに帰ってきた！

# speaker:king
# pace:30
被害を最小限に抑えて侵攻を退けたそうだ。

# speaker:king
# pace:30
# events:resume_dialogs_timer
彼らを迎えよう（そしてまたドラゴンとの果てなき戦いへ……）

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
안타깝게도 우리 병력으로는 침공을 막아내지 못했소.

# speaker:king
# pace:20
# events:resume_dialogs_timer
유닛을 하나도 남김없이 잃었고, 그 결과 몸값으로 낼 돈까지 잃고 말았소.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
부대가 좋은 소식을 가지고 돌아왔소!

# speaker:king
# pace:30
피해를 거의 입지 않고 침공을 막아냈다는군.

# speaker:king
# pace:30
# events:resume_dialogs_timer
그들의 귀환을 환영하오. (다시 드래곤과의 지루한 싸움을 이어가기 위해...)

  -> END

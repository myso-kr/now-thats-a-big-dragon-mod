# speaker:king
# pace:40
날 찾아냈군.

# speaker:king
# pace:32
그렇소, 드래곤의 둥지에서 가져왔소. 금화는 왕국을 위해. 저 장난감은 기념품으로.

# speaker:king
# pace:30
백성이 굶고 있었소. 다시 그때로 돌아가도 똑같이 할 것이오.

# speaker:king
# pace:30
얼마간 받고 입을 다무시오. 그러면 둘 다 무사히 걸어 나갈 수 있소.

# speaker:king
# pace:30
날 배신하겠소, 아니면 내 선물을 받겠소?

* [당신을 여기서 멈춰야겠소!]
  -> go_against_king

* [사실 금화는 좋아하지!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
그렇다면 어쩔 수 없군!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
그럼 그대의 몫을 가져가시오.

  -> END

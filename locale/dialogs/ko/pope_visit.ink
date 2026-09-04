VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 반갑네, 나는 교황일세.

# speaker:pope
# pace:30
- 다시 한번 그대의 믿음을 증명하고 교회에 헌금할 때가 되었네.

# speaker:pope
# pace:30
- 가난한 이들을 돕는 데 금화 {contributionCostLabel}닢이 필요하네.

* [금화 {contributionCostLabel}닢을 바친다]
    -> pay_contribution

* [다른 종교로 개종한다]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 그대의 영혼이 내세에서 보답받기를!

# speaker:pope
# pace:30
- 교회의 감사의 표시로 이 성직자 100명을 받게.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 그대의 영혼이 내세에서 저주받기를!

# speaker:pope
# pace:30
# chain_next
# wait:500
- 그리고 말이야...

# speaker:pope
# pace:30
- 저 거대한 도마뱀이 높으신 분의 힘으로 치유된다면 참으로 유감스럽겠군...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(치유하는 소리\)

  -> END

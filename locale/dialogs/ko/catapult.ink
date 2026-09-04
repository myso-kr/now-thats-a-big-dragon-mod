VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
또 뵙는군요!

# speaker:engineer
당신의 공성 병기를 계속 연구했습니다.

# speaker:engineer
# wait:300
# pace:30
이제 적에게 고양이를 쏠 수 있습니다. 전황을 뒤집을 물건이라고 봅니다.

# speaker:engineer
# wait:300
# pace:30
# chain_next
이름하여 "캣-아-펄트"

# speaker:engineer
# wait:300
# pace:300
(극적인 침묵)

# speaker:engineer
# pace:30
지금 보유한 것과 앞으로 살 것 모두 개조하는 데 투자하시겠습니까?

* [그냥 계속 바위를 쏘겠소]
    -> no_thanks

* [금화 {catapultCostLabel}닢 지불]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
써 보시고 소감을 꼭 들려주십시오!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
써 보시고 소감을 꼭 들려주십시오!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
아쉽군요. 그래도 행운을 빕니다.

  -> END

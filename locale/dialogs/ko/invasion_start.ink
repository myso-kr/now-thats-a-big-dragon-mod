VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
이웃 왕국이 우리를 공격하고 있소.

# speaker:king
# pace:30
침공을 멈추는 대가로 금화 {ransomCostLabel}닢을 요구했소.

# speaker:king
# chain_next
# pace:30
# wait:500
어찌하면 좋겠소?

* [금화 {ransomCostLabel}닢을 지불한다]
    -> pay_enemy

* { unitsCountFew > 3 } [유닛 {unitsCountFew}로 방어한다]
    -> send_few_units

* { unitsCountMany > 3 } [유닛 {unitsCountMany}로 방어한다]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 저들이 우리 제안을 받아들이길 바랄 뿐이오.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 이 정도면 충분하길 바라오.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 이 정도면 저들의 공격쯤은 확실히 막아내겠지.
~ strategyChoice = "send_many_units"

  -> END

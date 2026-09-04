VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Chào con, ta là Giáo hoàng.

# speaker:pope
# pace:30
- Đã đến lúc con chứng tỏ đức tin một lần nữa và dâng góp cho Giáo hội.

# speaker:pope
# pace:30
- Ta cần {contributionCostLabel} đồng vàng để giúp người nghèo.

* [Đưa ngài {contributionCostLabel} đồng vàng]
    -> pay_contribution

* [Đổi sang tôn giáo khác]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Nguyện linh hồn con được ban thưởng ở đời sau!

# speaker:pope
# pace:30
- Hãy nhận 100 tư tế này như lời cảm tạ của Giáo hội.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Nguyện linh hồn con bị nguyền rủa ở đời sau!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Với lại...

# speaker:pope
# pace:30
- Sẽ tiếc lắm nếu con thằn lằn khổng lồ kia được một quyền năng cao hơn chữa lành...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(tiếng chữa lành\)

  -> END

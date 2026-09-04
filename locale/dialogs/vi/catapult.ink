VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Lại gặp bạn rồi!

# speaker:engineer
Chúng tôi đã tiếp tục nghiên cứu vũ khí công thành của bạn.

# speaker:engineer
# wait:300
# pace:30
Giờ nó bắn được mèo vào kẻ địch, và chúng tôi tin nó sẽ xoay chuyển trận đấu.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Chúng tôi gọi nó là "Máy bắn mèo"

# speaker:engineer
# wait:300
# pace:300
(ngừng một nhịp cho kịch tính)

# speaker:engineer
# pace:30
Bạn có muốn đầu tư cải tiến cho cả cái đang có lẫn những cái sau này không?

* [Tôi vẫn muốn bắn đá]
    -> no_thanks

* [Trả {catapultCostLabel} vàng]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Nhớ cho chúng tôi biết cảm nghĩ nhé!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Nhớ cho chúng tôi biết cảm nghĩ nhé!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Tiếc thật. Dù sao cũng chúc bạn may mắn.

  -> END

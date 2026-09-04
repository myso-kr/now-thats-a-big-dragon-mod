VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Tiếc thay, quân ta không đủ để đẩy lui cuộc xâm lược.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ta mất sạch quân, và mất luôn cả khoản tiền chuộc.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Quân ta trở về với tin mừng!

# speaker:king
# pace:30
Họ đã đẩy lui cuộc xâm lược với thiệt hại tối thiểu.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Ta đón họ trở về (để lại tiếp tục cày con rồng...)

  -> END

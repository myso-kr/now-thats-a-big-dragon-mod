VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
很遗憾，我们的兵力不足以挡住这次入侵。

# speaker:king
# pace:20
# events:resume_dialogs_timer
派去的单位全军覆没，赎金那笔钱也一并没了。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
我们的部队带回了好消息！

# speaker:king
# pace:30
他们以极小的损失挡住了这次入侵。

# speaker:king
# pace:30
# events:resume_dialogs_timer
欢迎他们归队（继续和那条龙耗下去……）

  -> END

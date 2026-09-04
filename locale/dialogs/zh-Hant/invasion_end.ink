VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
很遺憾，我們的兵力不足以擋住這次入侵。

# speaker:king
# pace:20
# events:resume_dialogs_timer
派去的單位全軍覆沒，贖金那筆錢也一併沒了。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
我們的部隊帶回了好訊息！

# speaker:king
# pace:30
他們以極小的損失擋住了這次入侵。

# speaker:king
# pace:30
# events:resume_dialogs_timer
歡迎他們歸隊（繼續和那條龍耗下去……）

  -> END

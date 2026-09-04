VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Vi ses igen!

# speaker:engineer
Vi har forskat vidare på ditt belägringsvapen.

# speaker:engineer
# wait:300
# pace:30
Nu kan den skjuta katter på fienden, och vi tror att den vänder hela striden.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kallar den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en konstpaus)

# speaker:engineer
# pace:30
Vill du bekosta uppgraderingen, för den du har och för alla som kommer?

* [Jag skjuter hellre sten]
    -> no_thanks

* [Betala {catapultCostLabel} guld]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Berätta gärna vad du tycker!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Berätta gärna vad du tycker!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Vad synd. Lycka till ändå.

  -> END

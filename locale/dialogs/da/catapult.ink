VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Der er du igen!

# speaker:engineer
Vi har arbejdet videre på dit belejringsvåben.

# speaker:engineer
# wait:300
# pace:30
Nu kan den skyde katte mod fjenden, og vi tror, den vender hele kampen.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kalder den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en kunstpause)

# speaker:engineer
# pace:30
Vil du betale for forbedringen, både til den her og til alle de næste?

* [Jeg skyder hellere med sten]
    -> no_thanks

* [Betal {catapultCostLabel} guld]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Sig endelig, hvad du synes!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Sig endelig, hvad du synes!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Ærgerligt. Held og lykke alligevel.

  -> END

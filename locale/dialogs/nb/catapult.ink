VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Der var du igjen!

# speaker:engineer
Vi har jobbet videre med beleiringsvåpenet ditt.

# speaker:engineer
# wait:300
# pace:30
Nå kan den skyte katter mot fienden, og vi tror den snur hele kampen.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Vi kaller den "Kattapulten"

# speaker:engineer
# wait:300
# pace:300
(en kunstpause)

# speaker:engineer
# pace:30
Vil du betale for forbedringen, både til denne og til alle de neste?

* [Jeg skyter heller med stein]
    -> no_thanks

* [Betal {catapultCostLabel} gull]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Si gjerne fra hva du synes!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Si gjerne fra hva du synes!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Synd. Lykke til likevel.

  -> END

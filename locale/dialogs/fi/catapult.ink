VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Taas tavataan!

# speaker:engineer
Olemme jatkaneet piiritysaseesi kehittelyä.

# speaker:engineer
# wait:300
# pace:30
Nyt se ampuu vihollisen niskaan kissoja, ja uskomme sen kääntävän koko taistelun.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Kutsumme sitä nimellä "Kissapultti"

# speaker:engineer
# wait:300
# pace:300
(tehokeino tauko)

# speaker:engineer
# pace:30
Haluatko kustantaa parannuksen, tähän ja kaikkiin tuleviin?

* [Ammun mieluummin kiviä]
    -> no_thanks

* [Maksa {catapultCostLabel} kultaa]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Kerro toki mitä mieltä olet!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Kerro toki mitä mieltä olet!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Harmi. Onnea matkaan silti.

  -> END

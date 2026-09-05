VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Γεια σου, πάλι!

# speaker:engineer
Συνεχίσαμε την έρευνα πάνω στην πολιορκητική σου μηχανή.

# speaker:engineer
# wait:300
# pace:30
Τώρα μπορεί να εκτοξεύει γάτες στους εχθρούς, και πιστεύουμε ότι γέρνει τη ζυγαριά υπέρ μας.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Τον λέμε "Γατα-πέλτη"

# speaker:engineer
# wait:300
# pace:300
(δραματική παύση)

# speaker:engineer
# pace:30
Θέλεις να επενδύσεις στην αναβάθμιση, για όσους έχεις και για όσους πάρεις;

* [Προτιμώ να ρίχνω βράχια]
    -> no_thanks

* [Πλήρωσε {catapultCostLabel} χρυσάφι]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Πες μας πώς σου φάνηκε!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Πες μας πώς σου φάνηκε!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Κρίμα. Καλή τύχη πάντως.

  -> END

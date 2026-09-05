VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Χαίρετε, είμαι ο Πάπας.

# speaker:pope
# pace:30
- Ήρθε η ώρα ν' αποδείξετε ξανά την πίστη σας και να συνεισφέρετε στην Εκκλησία μας.

# speaker:pope
# pace:30
- Χρειάζομαι {contributionCostLabel} χρυσά νομίσματα για να βοηθήσω τους φτωχούς.

* [Πλήρωσέ του {contributionCostLabel} χρυσά νομίσματα]
    -> pay_contribution

* [Άλλαξε θρήσκευμα]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Είθε η ψυχή σας ν' ανταμειφθεί στη μέλλουσα ζωή!

# speaker:pope
# pace:30
- Πάρτε αυτούς τους 100 ιερείς ως δείγμα ευγνωμοσύνης της Εκκλησίας.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Είθε η ψυχή σας να καταδικαστεί στη μέλλουσα ζωή!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Επίσης...

# speaker:pope
# pace:30
- Θα ήταν κρίμα αν εκείνη η γιγάντια σαύρα θεραπευόταν από μια ανώτερη δύναμη...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(ήχοι θεραπείας\)

  -> END

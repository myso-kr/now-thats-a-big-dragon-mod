VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Zdravím, jsem papež.

# speaker:pope
# pace:30
- Je čas znovu prokázat svou víru a přispět naší Církvi.

# speaker:pope
# pace:30
- Potřebuji {contributionCostLabel} zlaťáků na pomoc chudým.

* [Dát mu {contributionCostLabel} zlaťáků]
    -> pay_contribution

* [Změnit víru]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Ať je tvá duše odměněna na onom světě!

# speaker:pope
# pace:30
- Přijmi těchto 100 kněží jako projev vděku Církve.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Ať je tvá duše zatracena na onom světě!

# speaker:pope
# pace:30
# chain_next
# wait:500
- A ještě...

# speaker:pope
# pace:30
- Byla by škoda, kdyby toho obrovského ještěra uzdravila vyšší moc...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(zvuky uzdravování\)

  -> END

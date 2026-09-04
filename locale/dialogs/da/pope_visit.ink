VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Vær hilset, mit barn. Jeg er paven.

# speaker:pope
# pace:30
- Det er tid til at vise din tro igen og give en gave til Kirken.

# speaker:pope
# pace:30
- Jeg har brug for {contributionCostLabel} guld for at hjælpe de fattige.

* [Giv ham {contributionCostLabel} guld]
    -> pay_contribution

* [Skift religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Måtte din sjæl blive belønnet i det hinsides!

# speaker:pope
# pace:30
- Tag imod disse 100 præster som Kirkens tak.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Måtte din sjæl blive forbandet i det hinsides!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Og for resten...

# speaker:pope
# pace:30
- Det ville være en skam, hvis det kæmpestore firben blev helbredt af en højere magt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helbredende lyde\)

  -> END

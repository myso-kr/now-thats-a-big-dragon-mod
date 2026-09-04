VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Vær hilset, mitt barn. Jeg er paven.

# speaker:pope
# pace:30
- Det er på tide å vise troen din igjen og gi en gave til Kirken.

# speaker:pope
# pace:30
- Jeg trenger {contributionCostLabel} gull for å hjelpe de fattige.

* [Gi ham {contributionCostLabel} gull]
    -> pay_contribution

* [Bytt religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Måtte sjelen din bli belønnet i det hinsidige!

# speaker:pope
# pace:30
- Ta imot disse 100 prestene som Kirkens takk.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Måtte sjelen din bli forbannet i det hinsidige!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Og forresten...

# speaker:pope
# pace:30
- Det ville være synd om den kjempestore øglen ble helbredet av en høyere makt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helbredende lyder\)

  -> END

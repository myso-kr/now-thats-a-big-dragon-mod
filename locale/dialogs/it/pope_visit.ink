VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Salute a te, sono il Papa.

# speaker:pope
# pace:30
- È tempo di dimostrare ancora una volta la tua fede e contribuire alla nostra Chiesa.

# speaker:pope
# pace:30
- Mi servono {contributionCostLabel} monete d'oro per aiutare i poveri.

* [Dagli {contributionCostLabel} monete d'oro]
    -> pay_contribution

* [Cambia religione]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Che la tua anima sia ricompensata nell'aldilà!

# speaker:pope
# pace:30
- Prendi questi 100 chierici come segno della gratitudine della Chiesa.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Che la tua anima sia dannata nell'aldilà!

# speaker:pope
# pace:30
# chain_next
# wait:500
- E poi...

# speaker:pope
# pace:30
- Sarebbe un peccato se quel lucertolone venisse guarito da un potere superiore...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(rumori di guarigione\)

  -> END

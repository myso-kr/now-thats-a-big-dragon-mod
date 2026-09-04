VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Üdvözöllek, én vagyok a pápa.

# speaker:pope
# pace:30
- Ideje ismét bizonyítanod a hitedet, és adakoznod az Egyházunknak.

# speaker:pope
# pace:30
- {contributionCostLabel} aranyra van szükségem a szegények megsegítéséhez.

* [Adj neki {contributionCostLabel} aranyat]
    -> pay_contribution

* [Válts vallást]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Nyerjen jutalmat a lelked a túlvilágon!

# speaker:pope
# pace:30
- Fogadd el ezt a 100 papot az Egyház hálájának jeléül.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Légyen átkozott a lelked a túlvilágon!

# speaker:pope
# pace:30
# chain_next
# wait:500
- És még valami...

# speaker:pope
# pace:30
- Kár lenne, ha azt az óriási gyíkot meggyógyítaná egy felsőbb hatalom...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(gyógyító hangok\)

  -> END

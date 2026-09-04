VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Gegroet, mijn kind. Ik ben de paus.

# speaker:pope
# pace:30
- Het is tijd om je geloof opnieuw te tonen en de Kerk een gave te doen.

# speaker:pope
# pace:30
- Ik heb {contributionCostLabel} goud nodig om de armen te helpen.

* [Geef hem {contributionCostLabel} goud]
    -> pay_contribution

* [Verander van geloof]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Moge je ziel beloond worden in het hiernamaals!

# speaker:pope
# pace:30
- Neem deze 100 priesters aan als dank van de Kerk.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Moge je ziel vervloekt worden in het hiernamaals!

# speaker:pope
# pace:30
# chain_next
# wait:500
- En trouwens...

# speaker:pope
# pace:30
- Het zou zonde zijn als die reusachtige hagedis door een hogere macht genezen werd...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(genezende geluiden\)

  -> END

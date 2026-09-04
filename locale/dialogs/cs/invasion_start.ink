VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Sousední království na nás útočí.

# speaker:king
# pace:30
Žádají {ransomCostLabel} zlaťáků, aby invazi zastavili.

# speaker:king
# chain_next
# pace:30
# wait:500
Co myslíš, že bychom měli udělat?

* [Zaplatit {ransomCostLabel} zlaťáků]
    -> pay_enemy

* { unitsCountFew > 3 } [Bránit se s {unitsCountFew} jednotkami]
    -> send_few_units

* { unitsCountMany > 3 } [Bránit se s {unitsCountMany} jednotkami]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Doufejme, že naši nabídku přijmou.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Doufejme, že to bude stačit.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Tohle jejich útok určitě odrazí.
~ strategyChoice = "send_many_units"

  -> END

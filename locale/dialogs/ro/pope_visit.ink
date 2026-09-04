VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Fii binecuvântat, copile. Eu sunt Papa.

# speaker:pope
# pace:30
- E vremea să-ți arăți din nou credința și să dai un dar Bisericii.

# speaker:pope
# pace:30
- Am nevoie de {contributionCostLabel} aur ca să-i ajut pe săraci.

* [Dă-i {contributionCostLabel} aur]
    -> pay_contribution

* [Schimbă religia]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Fie ca sufletul tău să fie răsplătit pe lumea cealaltă!

# speaker:pope
# pace:30
- Primește acești 100 de preoți ca mulțumire din partea Bisericii.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Fie ca sufletul tău să fie blestemat pe lumea cealaltă!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Și apropo...

# speaker:pope
# pace:30
- Ar fi păcat ca șopârla aceea uriașă să fie vindecată de o putere mai înaltă...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(sunete de vindecare\)

  -> END

VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Saludos, soy el Papa.

# speaker:pope
# pace:30
- Es hora de demostrar tu fe una vez más y contribuir a nuestra Iglesia.

# speaker:pope
# pace:30
- Necesito {contributionCostLabel} monedas de oro para ayudar a los pobres.

* [Darle {contributionCostLabel} monedas de oro]
    -> pay_contribution

* [Cambiar de religión]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- ¡Que tu alma sea recompensada en el más allá!

# speaker:pope
# pace:30
- Toma estos 100 clérigos como muestra de gratitud de la Iglesia.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- ¡Que tu alma sea condenada en el más allá!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Ah, y otra cosa...

# speaker:pope
# pace:30
- Sería una pena que un poder superior curase a ese lagarto gigante...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(ruidos de curación\)

  -> END

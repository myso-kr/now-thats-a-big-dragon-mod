VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Hälsningar, mitt barn. Jag är påven.

# speaker:pope
# pace:30
- Det är dags att visa din tro igen och ge en gåva till Kyrkan.

# speaker:pope
# pace:30
- Jag behöver {contributionCostLabel} guld för att hjälpa de fattiga.

* [Ge honom {contributionCostLabel} guld]
    -> pay_contribution

* [Byt religion]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Må din själ bli belönad i nästa liv!

# speaker:pope
# pace:30
- Ta emot dessa 100 präster som Kyrkans tack.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Må din själ bli förbannad i nästa liv!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Och förresten...

# speaker:pope
# pace:30
- Det vore synd om den där jättelika ödlan blev helad av en högre makt...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(helande ljud\)

  -> END

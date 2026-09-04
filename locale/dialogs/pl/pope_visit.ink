VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Pozdrawiam, jestem Papieżem.

# speaker:pope
# pace:30
- Nadszedł czas, byś znów dowiódł swojej wiary i wsparł nasz Kościół.

# speaker:pope
# pace:30
- Potrzebuję {contributionCostLabel} sztuk złota, by pomóc ubogim.

* [Daj mu {contributionCostLabel} sztuk złota]
    -> pay_contribution

* [Zmień religię]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Niech twoja dusza zazna nagrody w zaświatach!

# speaker:pope
# pace:30
- Przyjmij tych 100 kapłanów jako wyraz wdzięczności Kościoła.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Niech twoja dusza będzie potępiona w zaświatach!

# speaker:pope
# pace:30
# chain_next
# wait:500
- A także...

# speaker:pope
# pace:30
- Szkoda byłoby, gdyby tego wielkiego jaszczura uzdrowiła wyższa moc...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(odgłosy uzdrawiania\)

  -> END

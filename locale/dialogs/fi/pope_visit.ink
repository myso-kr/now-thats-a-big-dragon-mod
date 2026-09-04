VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Tervehdys, lapseni. Olen paavi.

# speaker:pope
# pace:30
- On aika osoittaa uskosi jälleen ja antaa lahja Kirkolle.

# speaker:pope
# pace:30
- Tarvitsen {contributionCostLabel} kultaa auttaakseni köyhiä.

* [Anna hänelle {contributionCostLabel} kultaa]
    -> pay_contribution

* [Vaihda uskontoa]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Palkittakoon sielusi tuonpuoleisessa!

# speaker:pope
# pace:30
- Ota vastaan nämä 100 pappia Kirkon kiitoksena.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Kirottakoon sielusi tuonpuoleisessa!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Ja muuten...

# speaker:pope
# pace:30
- Olisi ikävää, jos tuo jättiläismäinen lisko paranisi korkeamman voiman avulla...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(parantavia ääniä\)

  -> END

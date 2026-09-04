VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Salam, anakku. Akulah Sri Paus.

# speaker:pope
# pace:30
- Sudah waktunya menunjukkan imanmu lagi dan memberi persembahan kepada Gereja.

# speaker:pope
# pace:30
- Aku butuh {contributionCostLabel} emas untuk menolong kaum miskin.

* [Beri dia {contributionCostLabel} emas]
    -> pay_contribution

* [Pindah agama]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Semoga jiwamu diganjar di akhirat!

# speaker:pope
# pace:30
- Terimalah 100 rohaniwan ini sebagai tanda terima kasih Gereja.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Semoga jiwamu terkutuk di akhirat!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Lagi pula...

# speaker:pope
# pace:30
- Sayang sekali kalau kadal raksasa itu disembuhkan oleh kuasa yang lebih tinggi...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(bunyi penyembuhan\)

  -> END

VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ketemu lagi!

# speaker:engineer
Kami sudah meneruskan penelitian senjata pengepungmu.

# speaker:engineer
# wait:300
# pace:30
Sekarang ia bisa melontarkan kucing ke musuh, dan kami yakin itu akan membalik pertempuran.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Kami menyebutnya "Katapel Kucing"

# speaker:engineer
# wait:300
# pace:300
(jeda demi kesan)

# speaker:engineer
# pace:30
Mau membiayai peningkatannya, untuk yang ini dan semua yang berikutnya?

* [Aku lebih suka melontar batu]
    -> no_thanks

* [Bayar {catapultCostLabel} emas]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Beri tahu kami pendapatmu, ya!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Beri tahu kami pendapatmu, ya!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Sayang sekali. Semoga berhasil.

  -> END

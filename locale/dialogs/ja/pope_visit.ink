VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- ごきげんよう、私が教皇です。

# speaker:pope
# pace:30
- 今ひとたび信仰を示し、我らが教会へ喜捨するときです。

# speaker:pope
# pace:30
- 貧しき者を救うため、金貨{contributionCostLabel}枚が必要です。

* [金貨{contributionCostLabel}枚を渡す]
    -> pay_contribution

* [別の宗教に改宗する]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- あなたの魂が来世で報われますように！

# speaker:pope
# pace:30
- 教会の感謝のしるしに、この聖職者100人をお受け取りください。

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- あなたの魂が来世で呪われますように！

# speaker:pope
# pace:30
# chain_next
# wait:500
- それと……

# speaker:pope
# pace:30
- あの巨大なトカゲが高き力に癒やされてしまったら、残念なことですねえ……

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \（癒やしの音）\

  -> END

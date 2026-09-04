VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
Regatul vecin ne atacă.

# speaker:king
# pace:30
Cer {ransomCostLabel} aur ca să oprească invazia.

# speaker:king
# chain_next
# pace:30
# wait:500
Tu ce crezi că ar trebui să facem?

* [Plătește {ransomCostLabel} aur]
    -> pay_enemy

* { unitsCountFew > 3 } [Apără-te cu {unitsCountFew} trupe]
    -> send_few_units

* { unitsCountMany > 3 } [Apără-te cu {unitsCountMany} trupe]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Să sperăm că primesc oferta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Să sperăm că e de ajuns.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Atâția îi resping cu siguranță.
~ strategyChoice = "send_many_units"

  -> END

VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Por desgracia, nuestras unidades no bastaron para repeler la invasión.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Las perdimos todas y, con ellas, también el importe del rescate.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
¡Nuestras tropas vuelven con buenas noticias!

# speaker:king
# pace:30
Han conseguido repeler la invasión con pérdidas mínimas.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Les damos la bienvenida (para seguir con el machaque contra el dragón...)

  -> END

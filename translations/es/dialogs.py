# -*- coding: utf-8 -*-
"""Writes the Spanish .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: informal "tú" throughout, which is what Spanish game localisation uses and
what the UI already speaks. The King is the one exception in tone rather than form —
he asks rather than orders.

The game's own font has no «», em dash or curly apostrophe, so this uses straight
quotes and hyphens. check-fonts.js enforces that.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Parece que te vendría bien ayuda para generar más recursos...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Prueba a comprar Aprendizajes para conseguir más granjeros, mineros y leñadores.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
¡Hola otra vez!

# speaker:engineer
Hemos seguido investigando tu arma de asedio.

# speaker:engineer
# wait:300
# pace:30
Ahora puede disparar gatos al enemigo, y creemos que puede inclinar la balanza.

# speaker:engineer
# wait:300
# pace:30
# chain_next
La llamamos "Gata-pulta"

# speaker:engineer
# wait:300
# pace:300
(pausa dramática)

# speaker:engineer
# pace:30
¿Quieres invertir en la reforma, para esta y para las próximas?

* [Prefiero seguir disparando rocas]
    -> no_thanks

* [Pagar {catapultCostLabel} de oro]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
¡Ya nos contarás qué te ha parecido!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
¡Ya nos contarás qué te ha parecido!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Qué lástima. Suerte de todos modos.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Tus tropas te han dejado el último golpe.

# speaker:king
# pace:30
- ¡Es tu oportunidad de acabar con él para siempre!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
El Rey te ha pedido que sigas entrenando, por si más adelante viene algo más grande.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Esta vez incluso quiere financiar tu ejército para que lo formes a tu gusto.

# speaker:princess
# pace:40
# chain_next
# wait:500
Pero cuando yo le pedí una fiesta de cumpleaños enorme hace unos meses,

# speaker:princess
# pace:40
# chain_next
# wait:500
todo fue...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, el reino no tiene dinero, hija mía"


# speaker:princess
# pace:37
Aunque este muñeco tiene una pinta rara...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
¿Qué? No creía que se pudiera derrotar.

# speaker:princess
# pace:20
# classes:love
Aunque, ¿hay algo que mi héroe no pueda derrotar?

# speaker:princess
# events:whistle
# pace:50
¿Qué, qué es eso de ahí arriba?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Eso no es un simple muñeco de entrenamiento.

# speaker:princess
# pace:30
Parece un juguete mágico. Para algo mucho más grande que nosotros.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Eh, tú, el de ahí...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
He encontrado estas llaves de la mazmorra secreta que hay bajo el castillo.

# speaker:rogue
# pace:30
# wait:500
Me pregunto si el Rey sabrá que existe.

# speaker:rogue
# pace:10
# chain_next
# wait:500
En fin...

# speaker:rogue
# pace:30
He sacado buen botín en mis incursiones, pero en la última casi se me apaga la antorcha.

# speaker:rogue
# wait:500
Me da miedo volver a entrar y perderme a oscuras, así que te doy todas las llaves gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Suerte,

# speaker:rogue
# pace:100
# events:end_give_keys
y ten cuidado.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
¡Eh! Soy el desarrollador.

# pace:40
Perdona, te has colado a través de un muro. El fallo es mío.

# pace:30
Puedo sacarte del vacío y conservarás todo tu botín.

* [Rendirse y conservar el botín]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
¡Adiós!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
¡Hola, héroe!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Para ayudar en la lucha, Su Majestad ha ordenado a la Orden de Arquitectos e Ingenieros de la Corona que preste su experiencia.

# speaker:engineer
# pace:30
Te ayudaremos de tres maneras:

# speaker:engineer
# pace:30
- Construyendo catapultas para el asedio.

# speaker:engineer
# pace:30
- Levantando edificios de segundo nivel, con nuestros constructores.

# speaker:engineer
# pace:30
- Fundando organizaciones de nivel superior, con nuestros ingenieros.

# speaker:engineer
# pace:30
Cuando tengas oro para ello, nos encontrarás en la pestaña "Ingeniería".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Vaya, ¿y qué creías que significaba "despedir unidades"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
¿No te bastó con matarme? ¡Deja de molestarme, por favor!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
¡Pío pío, hijo de p***!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Estoy listo para tocar para tus tropas e inspirarlas a multiplicar su poder.

# speaker:bard_dialog
# pace:35
# wait:400
¡Pulsa el botón del arpa y disfruta del subidón temporal!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
¡Socorro!

# speaker:king
# chain_next
# pace:30
# wait:500
¡Un dragón gigante está destruyendo nuestra aldea!

# speaker:king
# wait:300
# pace:30
- Necesitamos un héroe que nos salve.

# speaker:king
# pace:30
- Por favor, mata a ese dragón con tu poderosa espada, digo, con el cursor.

# speaker:king
# pace:30
- Y si reúnes oro suficiente, quizá puedas reclutar algo de ayuda.

# speaker:king
# pace:30
- ¡Suerte!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
¡De algún modo, Forth'aarh ha vuelto!

# speaker:king
# pace:30
# wait:400
Pero licenciaste a tus tropas. Ahora tendrás que reclutar de nuevo.

# speaker:king
# wait:300
# pace:30
- Y el ataque anterior arruinó nuestra economía, así que no puedo subvencionar tu ejército.

# speaker:king
# pace:40
# chain_next
- A partir de ahora consumirán

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- alimento, madera y mineral.

# speaker:king
# pace:40
- Tendrás que administrar bien tus recursos.

# speaker:king
# pace:40
- Decide en cada momento qué unidades consumen recursos y cuáles no.

# speaker:king
# pace:40
- O "despide" a algunas: consumirán menos y aun así darán algo de trabajo.

# speaker:king
# pace:28
- ¡Suerte!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

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
"""

F["invasion_start.ink"] = r"""VAR ransomCost = 1
VAR ransomCostLabel = "1"
VAR strategyChoice = ""
VAR unitsCountFew = 1
VAR unitsCountMany = 1

# speaker:king
# pace:30
# wait:500
El reino vecino nos está atacando.

# speaker:king
# pace:30
Piden {ransomCostLabel} monedas de oro para detener su invasión.

# speaker:king
# chain_next
# pace:30
# wait:500
¿Qué crees que deberíamos hacer?

* [Pagar {ransomCostLabel} monedas de oro]
    -> pay_enemy

* { unitsCountFew > 3 } [Defender con {unitsCountFew} unidades]
    -> send_few_units

* { unitsCountMany > 3 } [Defender con {unitsCountMany} unidades]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Esperemos que acepten nuestra oferta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Esperemos que baste.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Con esto seguro que frenamos su ataque.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Al menos... no he muerto pobre.

# speaker:king
# pace:60
# classes:victory
Enhorabuena por terminarte el juego, de todos modos.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
¡¡¡HAS MATADO A MI PADRE!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
No...

# speaker:developer
# pace:100
# classes:vader
¡Yo soy tu padre!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
¿Desarrollador?

# speaker:princess
# pace:50
¿Has metido dos referencias a Star Wars en tu juego? ¿En serio?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Me has encontrado.

# speaker:king
# pace:32
Sí, lo saqué de la guarida del dragón. El oro, para el reino. El juguete, de recuerdo.

# speaker:king
# pace:30
Nuestro pueblo pasaba hambre. Lo volvería a hacer.

# speaker:king
# pace:30
Acepta un soborno y calla, y los dos saldremos de esta.

# speaker:king
# pace:30
¿Me traicionas o aceptas mi regalo?

* [¡Hay que detenerte!]
  -> go_against_king

* [¡Sí que me gusta el oro!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
¡Que así sea!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Entonces toma tu parte.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Ya te he dado más oro del que jamás deseaste.

# speaker:king
# pace:30
Ese era el trato. Cógelo y márchate.

* [Me da igual, hay que detenerte]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
¡Que así sea!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Usaste mi oro para comprar el ejército que mató a su cría.

# speaker:king
# pace:32
No finjas ser inocente.

# speaker:king
# pace:30
Ven, pues.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Conque te has endeudado con el reino, ¿eh? Tranquilo... el gremio tiene de sobra a quien le debe dinero.


# speaker:rogue
# pace:40
# wait:400
Si no pagan, les rompemos un par de piernas.

# speaker:rogue
# pace:30
# wait:400
Hasta que vuelvas a estar en números negros, mis ladrones recaudarán el doble para ti.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
¡Ay! Nuestras reservas de maná se han agotado.

# speaker:wizard_dialog
# pace:35
# wait:400
Sin la esencia arcana no puedo canalizar mis hechizos contra el dragón.

# speaker:wizard_dialog
# pace:35
# wait:400
Ve al menú de mejoras y compra [Rellenar maná] cada vez que nos quedemos secos... ¡y volveremos a golpear a la bestia!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
¿Alguien ha visto al Rey? Ha desaparecido.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
La última vez que lo vieron se dirigía a las mazmorras de debajo del castillo.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
¡Bienvenido!

# pace:45
¡Soy Mook, el joven y justo!

# pace:50
El Rey me puso aquí para que no te pierdas, y lo digo en serio: me gusta indicar el camino.

# pace:35
No me dejan salir de esta baldosa. "Ayuda a todo viajero" y luego "no cruces esa línea". Me decía que era el protocolo. Últimamente... ya no lo tengo tan claro.

# pace:25
Pero oye, toma esta antorcha. Es la única ayuda que aún puedo pasar al otro lado de la línea.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

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
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Vendo alimento, madera o mineral por

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
de oro. ¿Cuál quieres llevarte?

* { canAffordTrading > 0 } [Alimento: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Madera: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Mineral: {resourceAmountLabel}]
    -> buy_ore

* [Nada]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Gracias, nos vemos en mi próxima ruta.

  -> END


=== farewell ===

# speaker:salesman
Nos vemos en mi próxima ruta.

* [Adiós]
    -> END

* [Ven menos a menudo]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Entendido. Espaciaré mis visitas.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
¡Vaya, lo has conseguido de verdad!

# speaker:king
# pace:30
- Muchísimas gracias por matar a ese dragón. ¡Eres nuestro héroe!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Por fin podemos...

# speaker:princess
# classes:scared
# pace:200
¿Qué ha sido ese ruido?

# speaker:shadow
# pace:200
# classes:angry
¡¡¡HABÉIS MATADO A MI HIJO!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
¡Eso

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
SÍ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
que es un dragón grande!

# speaker:princess
# pace:20
# events:resume_game
Ay, no, ¿nos vas a ayudar?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh ha muerto. Has hecho lo que ningún ejército pudo.

# speaker:king
# pace:28
# classes:victory
Gracias. De verdad.

# speaker:princess
# pace:30
# classes:victory
Sígueme... Hay que prepararse para los nuevos enemigos que puedan venir.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
¿Cómo ha podido volver?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- No sé cómo ha regresado.

# speaker:king
# pace:28
- Pero hace falta una voluntad asombrosa para volver así.

# speaker:princess
# pace:40
# classes:scared
- Y también ganas de vengarse de algo...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
¿Sabías que cada vez que entras en una mazmorra

# classes:angry-worker
# pace:30
- TENGO QUE CONSTRUIR UN LABERINTO ENTERO A MANO?!?

# chain_next
# pace:50
- Estuvimos semanas subiendo cofres. Dijo que no preguntáramos de dónde salían.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
¡Por fin!

# pace:40
- El rey dice que he terminado y que le devuelva el pico en cuanto acabe este nivel.

  -> END
"""

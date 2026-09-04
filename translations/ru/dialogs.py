# -*- coding: utf-8 -*-
"""Writes the Russian .ink dialogues.

Only the spoken lines and the bracketed choice labels are translated. Directives
(`# speaker:`, `# pace:`), ink structure (`VAR`, `===`, `->`, `~`) and every `{...}`
interpolation are the game's own and are carried across untouched.

Address forms are set per speaker rather than globally: the King is a petitioner
asking his champion for aid and uses «вы»; the Princess is fond of the hero and uses
«ты»; the rogue and the fourth-wall characters are casual.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Похоже, вам нужна помощь с добычей ресурсов...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Попробуйте купить Ученичество, чтобы получать больше фермеров, шахтёров и лесорубов.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
И снова здравствуйте!

# speaker:engineer
Мы продолжили работу над вашим осадным орудием.

# speaker:engineer
# wait:300
# pace:30
Теперь оно стреляет котами, и мы думаем, это переломит ход боя.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Мы зовём это "Кот-апульта"

# speaker:engineer
# wait:300
# pace:300
(драматическая пауза)

# speaker:engineer
# pace:30
Вложитесь в переделку - нынешних и будущих орудий?

* [Лучше буду стрелять камнями]
    -> no_thanks

* [Заплатить {catapultCostLabel} золота]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Расскажите потом, как вам!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Расскажите потом, как вам!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Жаль. Что ж, удачи вам.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Ваши войска оставили последний удар вам.

# speaker:king
# pace:30
- Это ваш шанс покончить с ним раз и навсегда!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Король просил тебя продолжать тренировки - вдруг дальше будет что-то покрупнее.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Он даже готов оплатить твою армию, чтобы ты собрал её по своему вкусу.

# speaker:princess
# pace:40
# chain_next
# wait:500
А когда я пару месяцев назад попросила огромный праздник на день рождения,

# speaker:princess
# pace:40
# chain_next
# wait:500
было только...

# speaker:princess
# pace:60
# classes:imitating
"Бла-бла-бла, у королевства нет денег, дочь моя!"


# speaker:princess
# pace:37
Хотя манекен какой-то странный...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Что? Я не думала, что его вообще можно победить.

# speaker:princess
# pace:20
# classes:love
Впрочем, есть ли что-то, с чем мой герой не справится?

# speaker:princess
# events:whistle
# pace:50
Что, что это там наверху?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Это не простой тренировочный манекен.

# speaker:princess
# pace:30
Похоже на волшебную игрушку. Для кого-то куда крупнее нас.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Эй, ты, там...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Я нашёл эти ключи от тайного подземелья под замком.

# speaker:rogue
# pace:30
# wait:500
Интересно, знает ли о нём король.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Ну да ладно...

# speaker:rogue
# pace:30
За свои вылазки я добыл немало добра, но в последний раз факел чуть не погас.

# speaker:rogue
# wait:500
Боюсь снова идти туда и заблудиться в темноте, так что отдаю тебе все ключи даром.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Удачи,

# speaker:rogue
# pace:100
# events:end_give_keys
и будь осторожнее.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Эй! Это я, разработчик.

# pace:40
Извини, ты провалился сквозь стену. Это мой баг.

# pace:30
Я выведу тебя из пустоты, и вся добыча останется при тебе.

* [Сдаться и оставить добычу]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Пока!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Здравствуйте, герой!

# speaker:engineer
# pace:30
# events:show_engineering_tab
В помощь битве Его Величество повелел Ордену зодчих и инженеров Короны предоставить наш опыт.

# speaker:engineer
# pace:30
Мы поможем вам тремя способами:

# speaker:engineer
# pace:30
- Построим катапульты для осады.

# speaker:engineer
# pace:30
- Возведём здания второго уровня - силами наших строителей.

# speaker:engineer
# pace:30
- Откроем организации высших уровней - силами наших инженеров.

# speaker:engineer
# pace:30
Когда наберёте золота, ищите нас на вкладке "Инженерия".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ох, а вы думали, что значит "уволить бойцов"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Убить меня было мало? Хватит меня донимать, прошу!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Чирик-чирик, тварь ты эта*****!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Я готов сыграть для ваших войск и вдохновить их на новые силы.

# speaker:bard_dialog
# pace:35
# wait:400
Нажмите на кнопку с арфой и насладитесь временным приростом мощи!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
На помощь!

# speaker:king
# chain_next
# pace:30
# wait:500
Огромный дракон разрушает нашу деревню!

# speaker:king
# wait:300
# pace:30
- Нам нужен герой, который нас спасёт.

# speaker:king
# pace:30
- Прошу, сразите этого дракона своим могучим мечом - то есть курсором мыши.

# speaker:king
# pace:30
- А если золота хватит, вы сможете нанять и подмогу.

# speaker:king
# pace:30
- Удачи!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Каким-то образом Форт'аарх вернулся!

# speaker:king
# pace:30
# wait:400
Но вы распустили войска. Теперь придётся набирать заново.

# speaker:king
# wait:300
# pace:30
- А прошлое нападение разорило нашу казну, так что содержать армию я не смогу.

# speaker:king
# pace:40
# chain_next
- Теперь они будут потреблять

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- еду, древесину и руду.

# speaker:king
# pace:40
- Вам придётся с умом распоряжаться ресурсами.

# speaker:king
# pace:40
- Переключайте, кому из бойцов сейчас потреблять ресурсы, а кому нет.

# speaker:king
# pace:40
- Или "увольте" часть из них: будут потреблять меньше, но всё же работать.

# speaker:king
# pace:28
- Удачи!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Увы, наших бойцов не хватило, чтобы отбить вторжение.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Мы потеряли всех до единого, а вместе с ними и сумму выкупа.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Войска вернулись с добрыми вестями!

# speaker:king
# pace:30
Им удалось отбить вторжение с минимальными потерями.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Встречаем их дома (и продолжаем гринд против дракона...)

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
Соседнее королевство напало на нас.

# speaker:king
# pace:30
Они требуют {ransomCostLabel} золотых, чтобы остановить вторжение.

# speaker:king
# chain_next
# pace:30
# wait:500
Как думаете, что нам делать?

* [Заплатить {ransomCostLabel} золотых]
    -> pay_enemy

* { unitsCountFew > 3 } [Оборона: {unitsCountFew} бойцов]
    -> send_few_units

* { unitsCountMany > 3 } [Оборона: {unitsCountMany} бойцов]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Будем надеяться, они примут наше предложение.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Будем надеяться, этого хватит.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Уж это точно отобьёт их натиск.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
По крайней мере... я умер не бедным.

# speaker:king
# pace:60
# classes:victory
И всё же поздравляю с прохождением игры.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
ТЫ УБИЛ МОЕГО ОТЦА!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Нет...

# speaker:developer
# pace:100
# classes:vader
Я твой отец!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Разработчик?

# speaker:princess
# pace:50
Ты вставил в игру две отсылки к "Звёздным войнам"? Серьёзно?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Вы меня нашли.

# speaker:king
# pace:32
Да, я взял это из логова дракона. Золото - королевству. Игрушку - на память.

# speaker:king
# pace:30
Наш народ голодал. Я поступил бы так снова.

# speaker:king
# pace:30
Возьмите отступного и молчите - и мы оба выйдем отсюда целыми.

# speaker:king
# pace:30
Предать меня или принять мой дар?

* [Вас нужно остановить!]
  -> go_against_king

* [Золото я люблю!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Да будет так!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Тогда забирайте свою долю.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Я уже дал вам золота сверх всех ваших желаний.

# speaker:king
# pace:30
Таков был уговор. Берите и уходите.

* [Плевать, вас нужно остановить]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Да будет так!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
На моё золото вы купили армию, которая убила его дитя.

# speaker:king
# pace:32
Не делайте вид, что вы невиновны.

# speaker:king
# pace:30
Что ж, идите сюда.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Значит, влез в долги перед короной? Не переживай... у гильдии полно простофиль, которые должны нам.


# speaker:rogue
# pace:40
# wait:400
Не платят - ломаем пару ног.

# speaker:rogue
# pace:30
# wait:400
Пока не выйдешь в плюс, мои воры будут таскать тебе золото вдвое усерднее.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Увы! Наши запасы маны иссякли.

# speaker:wizard_dialog
# pace:35
# wait:400
Без тайной эссенции я не могу направить заклинания против дракона.

# speaker:wizard_dialog
# pace:35
# wait:400
Загляните в меню улучшений и покупайте [Восполнить ману], как только мы иссякнем... и мы вновь ударим по зверю!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Кто-нибудь видел короля? Он пропал.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
В последний раз его видели, когда он спускался в подземелья под замком.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Добро пожаловать!

# pace:45
Я Мук, юный и справедливый!

# pace:50
Король поставил меня сюда, чтобы ты не заблудился, и я серьёзно: мне нравится указывать путь.

# pace:35
Мне нельзя сходить с этой плитки. "Помогай каждому путнику", а потом "не переступай черту". Я говорил себе, что это устав. В последнее время... уже не уверен.

# pace:25
Но вот, держи факел. Единственная помощь, которую мне ещё можно передать за эту черту.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Приветствую, я Папа.

# speaker:pope
# pace:30
- Пришло время вновь доказать свою веру и пожертвовать нашей Церкви.

# speaker:pope
# pace:30
- Мне нужно {contributionCostLabel} золотых, чтобы помочь бедным.

* [Дать ему {contributionCostLabel} золотых]
    -> pay_contribution

* [Сменить веру]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Да воздастся душе вашей на том свете!

# speaker:pope
# pace:30
- Примите этих 100 жрецов в знак благодарности Церкви.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Да будет душа ваша проклята на том свете!

# speaker:pope
# pace:30
# chain_next
# wait:500
- И ещё...

# speaker:pope
# pace:30
- Было бы досадно, если бы ту громадную ящерицу исцелила высшая сила...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(звуки исцеления\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Продаю еду, древесину или руду - по

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
золота. Что желаете взять?

* { canAffordTrading > 0 } [Еда: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Древесина: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Руда: {resourceAmountLabel}]
    -> buy_ore

* [Ничего]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Благодарю, увидимся в следующий заход.

  -> END


=== farewell ===

# speaker:salesman
Увидимся в следующий заход.

* [Прощайте]
    -> END

* [Заходите пореже]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Понял. Буду наведываться реже.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Ух ты, у тебя правда получилось!

# speaker:king
# pace:30
- Огромное спасибо, что убили этого дракона. Вы наш герой!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Теперь мы наконец-то...

# speaker:princess
# classes:scared
# pace:200
Что это был за звук?

# speaker:shadow
# pace:200
# classes:angry
ВЫ УБИЛИ МОЕГО СЫНА!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Вот

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ЭТО

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
большой дракон!

# speaker:princess
# pace:20
# events:resume_game
О нет, ты ведь нам поможешь?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Форт'аарх мёртв. Ты сделал то, что не смогла ни одна армия.

# speaker:king
# pace:28
# classes:victory
Благодарю. Искренне.

# speaker:princess
# pace:30
# classes:victory
Идём за мной... Надо подготовиться к новым врагам, если они появятся.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Как он вообще вернулся?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Я не знаю, как он вернулся.

# speaker:king
# pace:28
- Но чтобы восстать вот так, нужна поразительная воля.

# speaker:princess
# pace:40
# classes:scared
- И жажда какой-то мести тоже...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
А ты знал, что каждый раз, когда ты входишь в подземелье,

# classes:angry-worker
# pace:30
- Я СОБИРАЮ ЦЕЛЫЙ НОВЫЙ ЛАБИРИНТ ВРУЧНУЮ?!?

# chain_next
# pace:50
- Мы неделями таскали наверх сундуки. Он сказал не спрашивать, откуда они.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Наконец-то!

# pace:40
- Король сказал, что я закончил и отдам ему кирку, как только доделаю этот уровень.

  -> END
"""

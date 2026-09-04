# -*- coding: utf-8 -*-
"""Writes the Ukrainian .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address per speaker: the King is a petitioner asking his champion for aid and uses
«ви»; the Princess is fond of the hero and uses «ти»; the rogue and the fourth-wall
characters are casual. The game's font has no «», em dash or curly apostrophe, so
straight quotes and hyphens throughout.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Схоже, вам потрібна допомога з видобутком ресурсів...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Спробуйте купити Учнівство, щоб мати більше фермерів, шахтарів і лісорубів.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
І знову вітаю!

# speaker:engineer
Ми продовжили роботу над вашою облоговою машиною.

# speaker:engineer
# wait:300
# pace:30
Тепер вона стріляє котами, і ми думаємо, це переламає хід бою.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Ми звемо це "Кото-пульта"

# speaker:engineer
# wait:300
# pace:300
(драматична пауза)

# speaker:engineer
# pace:30
Вкладетеся в переробку - нинішніх і майбутніх машин?

* [Краще стрілятиму камінням]
    -> no_thanks

* [Заплатити {catapultCostLabel} золота]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Розкажіть потім, як вам!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Розкажіть потім, як вам!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Шкода. Що ж, щасти вам.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Ваші загони лишили останній удар вам.

# speaker:king
# pace:30
- Це ваш шанс покінчити з ним назавжди!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Король просив тебе тренуватися далі - раптом далі буде щось більше.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Цього разу він навіть оплатить твоє військо, щоб ти зібрав його на свій смак.

# speaker:princess
# pace:40
# chain_next
# wait:500
А коли я кілька місяців тому попросила величезне свято на день народження,

# speaker:princess
# pace:40
# chain_next
# wait:500
було лише...

# speaker:princess
# pace:60
# classes:imitating
"Бла-бла-бла, у королівства немає грошей, донечко!"


# speaker:princess
# pace:37
Хоча манекен якийсь дивний...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Що? Я не думала, що його взагалі можна подолати.

# speaker:princess
# pace:20
# classes:love
А втім, чи є щось, з чим мій герой не впорається?

# speaker:princess
# events:whistle
# pace:50
Що, що це там угорі?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Це не простий тренувальний манекен.

# speaker:princess
# pace:30
Схоже на чарівну іграшку. Для когось значно більшого за нас.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Гей, ти, там...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Я знайшов ці ключі від таємного підземелля під замком.

# speaker:rogue
# pace:30
# wait:500
Цікаво, чи знає про нього король.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Ну та байдуже...

# speaker:rogue
# pace:30
За свої вилазки я здобув чимало добра, але минулого разу смолоскип ледь не згас.

# speaker:rogue
# wait:500
Боюся знову туди йти й заблукати в темряві, тож віддаю тобі всі ключі задарма.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Щасти,

# speaker:rogue
# pace:100
# events:end_give_keys
і будь обережним.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Гей! Це я, розробник.

# pace:40
Вибач, ти провалився крізь стіну. Це мій баг.

# pace:30
Я виведу тебе з порожнечі, і вся здобич лишиться при тобі.

* [Здатися і лишити здобич]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Бувай!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Вітаю, герою!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Щоб допомогти в бою, Його Величність наказав Ордену зодчих та інженерів Корони надати наш досвід.

# speaker:engineer
# pace:30
Ми допоможемо вам трьома способами:

# speaker:engineer
# pace:30
- Збудуємо катапульти для облоги.

# speaker:engineer
# pace:30
- Зведемо будівлі другого рівня - силами наших будівельників.

# speaker:engineer
# pace:30
- Заснуємо організації вищих рівнів - силами наших інженерів.

# speaker:engineer
# pace:30
Коли зберете золото, шукайте нас на вкладці "Інженерія".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ох, а ви думали, що означає "звільнити бійців"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Убити мене було замало? Годі мене діймати, прошу!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Цвірінь-цвірінь, гад ти *****!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Я готовий заграти вашим загонам і надихнути їх на нові сили.

# speaker:bard_dialog
# pace:35
# wait:400
Натисніть кнопку з арфою і насолодіться тимчасовим приростом сили!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Рятуйте!

# speaker:king
# chain_next
# pace:30
# wait:500
Величезний дракон руйнує наше село!

# speaker:king
# wait:300
# pace:30
- Нам потрібен герой, який нас урятує.

# speaker:king
# pace:30
- Прошу, здолайте цього дракона своїм могутнім мечем - тобто курсором миші.

# speaker:king
# pace:30
- А якщо золота вистачить, зможете найняти й підмогу.

# speaker:king
# pace:30
- Щасти!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Якимось чином Форт'аарх повернувся!

# speaker:king
# pace:30
# wait:400
Але ви розпустили загони. Тепер доведеться набирати заново.

# speaker:king
# wait:300
# pace:30
- А минулий напад зруйнував нашу скарбницю, тож утримувати військо я не зможу.

# speaker:king
# pace:40
# chain_next
- Тепер вони споживатимуть

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- їжу, деревину та руду.

# speaker:king
# pace:40
- Вам доведеться з розумом розпоряджатися ресурсами.

# speaker:king
# pace:40
- Перемикайте, кому з бійців зараз споживати ресурси, а кому ні.

# speaker:king
# pace:40
- Або "звільніть" частину з них: споживатимуть менше, але все ж працюватимуть.

# speaker:king
# pace:28
- Щасти!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
На жаль, наших бійців не вистачило, щоб відбити вторгнення.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ми втратили всіх до одного, а разом з ними й суму викупу.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Загони повернулися з доброю звісткою!

# speaker:king
# pace:30
Їм вдалося відбити вторгнення з мінімальними втратами.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Зустрічаємо їх удома (і повертаємося до гринду проти дракона...)

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
Сусіднє королівство напало на нас.

# speaker:king
# pace:30
Вони вимагають {ransomCostLabel} золотих, щоб спинити вторгнення.

# speaker:king
# chain_next
# pace:30
# wait:500
Як гадаєте, що нам робити?

* [Заплатити {ransomCostLabel} золотих]
    -> pay_enemy

* { unitsCountFew > 3 } [Оборона: {unitsCountFew} бійців]
    -> send_few_units

* { unitsCountMany > 3 } [Оборона: {unitsCountMany} бійців]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Сподіваймося, вони приймуть нашу пропозицію.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Сподіваймося, цього вистачить.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Оце вже точно відіб'є їхній натиск.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Принаймні... я помер не бідним.

# speaker:king
# pace:60
# classes:victory
І все ж вітаю з проходженням гри.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
ТИ ВБИВ МОГО БАТЬКА!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Ні...

# speaker:developer
# pace:100
# classes:vader
Я твій батько!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Розробнику?

# speaker:princess
# pace:50
Ти вставив у гру дві відсилки до "Зоряних воєн"? Серйозно?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Ви мене знайшли.

# speaker:king
# pace:32
Так, я взяв це з драконового лігва. Золото - королівству. Іграшку - на згадку.

# speaker:king
# pace:30
Наш народ голодував. Я вчинив би так знову.

# speaker:king
# pace:30
Візьміть відступне й мовчіть - і ми обидва вийдемо звідси цілими.

# speaker:king
# pace:30
Зрадите мене чи приймете мій дар?

* [Вас треба спинити!]
  -> go_against_king

* [Золото я люблю!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Хай буде так!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Тоді забирайте свою частку.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Я вже дав вам золота понад усі ваші бажання.

# speaker:king
# pace:30
Така була угода. Беріть і йдіть.

* [Байдуже, вас треба спинити]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Хай буде так!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
На моє золото ви купили військо, яке вбило його дитя.

# speaker:king
# pace:32
Не вдавайте невинного.

# speaker:king
# pace:30
Що ж, ідіть сюди.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Отже, заліз у борги перед короною? Не хвилюйся... у гільдії повно простаків, які нам винні.


# speaker:rogue
# pace:40
# wait:400
Не платять - ламаємо пару ніг.

# speaker:rogue
# pace:30
# wait:400
Поки не вийдеш у плюс, мої злодії носитимуть тобі золото вдвічі старанніше.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
На жаль! Наші запаси мани вичерпано.

# speaker:wizard_dialog
# pace:35
# wait:400
Без таємної есенції я не можу спрямувати закляття проти дракона.

# speaker:wizard_dialog
# pace:35
# wait:400
Загляньте в меню покращень і купуйте "Поповнити ману", щойно ми вичерпаємося... і ми знову вдаримо по звірові!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Хтось бачив короля? Він зник.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Востаннє його бачили, коли він спускався в підземелля під замком.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Ласкаво просимо!

# pace:45
Я Мук, юний і справедливий!

# pace:50
Король поставив мене сюди, щоб ти не заблукав, і я серйозно: мені подобається вказувати шлях.

# pace:35
Мені не можна сходити з цієї плитки. "Допомагай кожному подорожньому", а потім "не переступай ту межу". Я казав собі, що це статут. Останнім часом... уже не певен.

# pace:25
Але ось, візьми смолоскип. Єдина допомога, яку мені ще можна передати за цю межу.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Вітаю, я Папа.

# speaker:pope
# pace:30
- Час знову довести свою віру і пожертвувати нашій Церкві.

# speaker:pope
# pace:30
- Мені потрібно {contributionCostLabel} золотих, щоб допомогти бідним.

* [Дати йому {contributionCostLabel} золотих]
    -> pay_contribution

* [Змінити віру]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Хай душа ваша матиме винагороду на тому світі!

# speaker:pope
# pace:30
- Прийміть цих 100 жерців на знак вдячності Церкви.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Хай душа ваша буде проклята на тому світі!

# speaker:pope
# pace:30
# chain_next
# wait:500
- І ще...

# speaker:pope
# pace:30
- Було б прикро, якби ту величезну ящірку зцілила вища сила...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(звуки зцілення\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Продаю їжу, деревину або руду - по

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
золота. Що бажаєте взяти?

* { canAffordTrading > 0 } [Їжа: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Деревина: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Руда: {resourceAmountLabel}]
    -> buy_ore

* [Нічого]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Дякую, побачимося наступного разу.

  -> END


=== farewell ===

# speaker:salesman
Побачимося наступного разу.

* [Прощавайте]
    -> END

* [Заїжджайте рідше]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Зрозумів. Навідуватимуся рідше.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Ого, у тебе справді вийшло!

# speaker:king
# pace:30
- Величезна подяка, що здолали цього дракона. Ви наш герой!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Тепер ми нарешті...

# speaker:princess
# classes:scared
# pace:200
Що це був за звук?

# speaker:shadow
# pace:200
# classes:angry
ВИ ВБИЛИ МОГО СИНА!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Ось

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ЦЕ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
великий дракон!

# speaker:princess
# pace:20
# events:resume_game
О ні, ти ж нам допоможеш?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Форт'аарх мертвий. Ти зробив те, чого не змогло жодне військо.

# speaker:king
# pace:28
# classes:victory
Дякую. Щиро.

# speaker:princess
# pace:30
# classes:victory
Ходімо за мною... Треба підготуватися до нових ворогів, якщо вони з'являться.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Як він узагалі повернувся?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Я не знаю, як він повернувся.

# speaker:king
# pace:28
- Але щоб постати ось так, потрібна разюча воля.

# speaker:princess
# pace:40
# classes:scared
- І жага якоїсь помсти теж...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
А ти знав, що щоразу, коли ти входиш у підземелля,

# classes:angry-worker
# pace:30
- Я СКЛАДАЮ ЦІЛИЙ НОВИЙ ЛАБІРИНТ ВРУЧНУ?!?

# chain_next
# pace:50
- Ми тижнями тягали нагору скрині. Він сказав не питати, звідки вони.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Нарешті!

# pace:40
- Король сказав, що я закінчив і віддам йому кайло, щойно дороблю цей рівень.

  -> END
"""

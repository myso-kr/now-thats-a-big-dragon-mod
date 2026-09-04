# -*- coding: utf-8 -*-
"""Writes the Simplified Chinese .ink dialogues.

Tags, knots, variables and diverts are copied verbatim from the English; only
prose and choice labels are translated. Traditional Chinese is derived from this
with opencc s2twp rather than translated again - see the README.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
看来你需要帮手来产出更多资源……

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
不妨买些学徒制，来培养更多农夫、矿工和伐木工。
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
又见面了！

# speaker:engineer
我们继续研究了你的攻城武器。

# speaker:engineer
# wait:300
# pace:30
它现在能把猫射向敌人，我们认为这足以扭转战局。

# speaker:engineer
# wait:300
# pace:30
# chain_next
我们管它叫「投猫机」

# speaker:engineer
# wait:300
# pace:300
（意味深长的停顿）

# speaker:engineer
# pace:30
你愿意为现有和今后购买的投石机投资这项改造吗？

* [我还是想继续扔石头]
    -> no_thanks

* [支付 {catapultCostLabel} 金币]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
用后记得告诉我们感想！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
用后记得告诉我们感想！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
真可惜。那也祝你好运。

  -> END

"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- 你的部队把最后一击留给了你。

# speaker:king
# pace:30
- 机会来了，亲手了结它吧！

  -> END

"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
国王让你继续练手，以防日后来了更大的家伙。

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
这次他甚至愿意出钱，让你随心所欲地组建军队。

# speaker:princess
# pace:40
# chain_next
# wait:500
可几个月前我求他办一场盛大的生日会时，

# speaker:princess
# pace:40
# chain_next
# wait:500
他却满口……

# speaker:princess
# pace:60
# classes:imitating
「哎呀呀，王国没钱啦，我的女儿！」


# speaker:princess
# pace:37
不过这个木人桩看着有点怪……


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
什么？我还以为它是打不倒的。

# speaker:princess
# pace:20
# classes:love
不过，还有什么是我的英雄打不倒的呢？

# speaker:princess
# events:whistle
# pace:50
等等，上面那是什么？

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
那可不是普通的练习木桩。

# speaker:princess
# pace:30
它看着像个魔法玩具。给比我们大得多的东西玩的。

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
喂，那边那位……

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
我找到了这些通往城堡底下秘密地下城的钥匙。

# speaker:rogue
# pace:30
# wait:500
不知道国王晓不晓得那地方的存在。

# speaker:rogue
# pace:10
# chain_next
# wait:500
不过话说回来……

# speaker:rogue
# pace:30
我几趟下来捞到不少好东西，但上一趟火把差点烧完。

# speaker:rogue
# wait:500
我怕再进去会在黑暗里迷路，所以这些钥匙就全都免费给你了。

# speaker:rogue
# pace:100
# chain_next
# wait: 300
祝你好运，

# speaker:rogue
# pace:100
# events:end_give_keys
千万小心。

  -> END

"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
嘿！我是开发者。

# pace:40
抱歉你穿墙了。这是我这边的 bug。

# pace:30
我可以把你从虚空里带出来，战利品也照样都归你。

* [放弃并保留战利品]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
再见！
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
你好，英雄！

# speaker:engineer
# pace:30
# events:show_engineering_tab
为助你作战，陛下已下令王室建筑师与工程师协会前来提供技术支持。

# speaker:engineer
# pace:30
我们将从三个方面协助你：

# speaker:engineer
# pace:30
- 建造用于攻城的投石机。

# speaker:engineer
# pace:30
- 由我们的建造者兴建二级建筑。

# speaker:engineer
# pace:30
- 由我们的工程师创立更高阶的组织。

# speaker:engineer
# pace:30
等你攒够金币，就到工程标签页找我们吧。

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
噢，你以为「解雇一些单位」是什么意思？

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
杀了我还不够？拜托别再烦我了！

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
叽叽喳喳，你个小杂碎！

-> END
"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
我准备好为你的部队演奏，激励他们把力量放大了。

# speaker:bard_dialog
# pace:35
# wait:400
点击竖琴按钮，享受这段短暂的强化吧！

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
救命！

# speaker:king
# chain_next
# pace:30
# wait:500
一条巨龙正在摧毁我们的村庄！

# speaker:king
# wait:300
# pace:30
- 我们需要一位英雄来拯救大家。

# speaker:king
# pace:30
- 请用你威武的宝剑／鼠标光标斩杀这条巨龙。

# speaker:king
# pace:30
- 如果金币够多，你或许还能招募一些帮手。

# speaker:king
# pace:30
- 祝你好运！

  -> END

"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
不知怎的，弗萨尔又回来了！

# speaker:king
# pace:30
# wait:400
可你已经遣散了部队。现在只能重新招募了。

# speaker:king
# wait:300
# pace:30
- 而且上次的袭击毁了我们的经济，我没法再资助你的军队。

# speaker:king
# pace:40
# chain_next
- 他们现在会消耗

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- 食物、木材和矿石。

# speaker:king
# pace:40
- 你得把资源管好。

# speaker:king
# pace:40
- 自行切换每个单位此刻是否消耗资源。

# speaker:king
# pace:40
- 或者「解雇」一部分，让他们少吃点，但还能干些活。

# speaker:king
# pace:28
- 祝你好运！

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
很遗憾，我们的兵力不足以挡住这次入侵。

# speaker:king
# pace:20
# events:resume_dialogs_timer
派去的单位全军覆没，赎金那笔钱也一并没了。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
我们的部队带回了好消息！

# speaker:king
# pace:30
他们以极小的损失挡住了这次入侵。

# speaker:king
# pace:30
# events:resume_dialogs_timer
欢迎他们归队（继续和那条龙耗下去……）

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
邻国正在进攻我们。

# speaker:king
# pace:30
他们索要 {ransomCostLabel} 金币来停止入侵。

# speaker:king
# chain_next
# pace:30
# wait:500
你觉得我们该怎么办？

* [支付 {ransomCostLabel} 金币]
    -> pay_enemy

* { unitsCountFew > 3 } [派 {unitsCountFew} 个单位防守]
    -> send_few_units

* { unitsCountMany > 3 } [派 {unitsCountMany} 个单位防守]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 但愿他们肯接受我们的条件。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 但愿这些人够用。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 这下总该能挡住他们的进攻了。
~ strategyChoice = "send_many_units"

  -> END

"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
至少……我不是穷死的。

# speaker:king
# pace:60
# classes:victory
不过，恭喜你通关了。

# speaker:king
# events:sigh
# pace:200
……

# speaker:princess
# pace:50
# classes:angry
你杀了我父亲！！！

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
不……

# speaker:developer
# pace:100
# classes:vader
我才是你父亲！

# speaker:princess
# pace:150
……

# speaker:princess
# pace:50
# chain_next
# wait:500
开发者？

# speaker:princess
# pace:50
你在游戏里塞了两个《星球大战》的梗？认真的吗？！？

# events:return_to_infinite
# pace:40
# classes:vader
……


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
你找到我了。

# speaker:king
# pace:32
没错，我从龙巢里拿了东西。金币是给王国的。那个玩具算个纪念品。

# speaker:king
# pace:30
我们的子民在挨饿。换一次我还会这么做。

# speaker:king
# pace:30
收下这笔封口费，你我都能全身而退。

# speaker:king
# pace:30
是要背叛我，还是收下我的好意？

* [必须有人阻止你！]
  -> go_against_king

* [我确实挺喜欢金币的！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就这样吧！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
那就拿走你那一份。

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
我给你的金币已经超出你最大的贪念了。

# speaker:king
# pace:30
说好的就是这样。拿了钱就走吧。

* [不管，必须有人阻止你]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就这样吧！

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
你用我的金币买下了那支杀死他孩子的军队。

# speaker:king
# pace:32
别装作自己是无辜的。

# speaker:king
# pace:30
那就来吧。

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
这么说你欠了王国一屁股债，是吧？别慌……公会里欠我们钱的冤大头多的是。


# speaker:rogue
# pace:40
# wait:400
他们要是不还，我们就打断几条腿。

# speaker:rogue
# pace:30
# wait:400
在你还清之前，我的盗贼们替你收金币的效率会翻倍。

  -> END
"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
唉！我们的法力储备已经见底了。

# speaker:wizard_dialog
# pace:35
# wait:400
没有奥术精华，我无法对巨龙引导法术。

# speaker:wizard_dialog
# pace:35
# wait:400
每当我们枯竭时，请到升级菜单购买[补充法力]……好让我们再次痛击这头野兽！

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
有人见过国王吗？他不见了。

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
最后有人看见他时，他正往城堡底下的地下城走去。

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
欢迎！

# pace:45
我是穆克，年轻又公正！

# pace:50
国王把我放在这儿免得你迷路，说真的；我就喜欢给人指路。

# pace:35
我不能离开这块地砖。先是「帮助每一位旅人」，然后是「别越过那条线」。我一直告诉自己这是规矩。可最近……我不太确定了。

# pace:25
不过嘿，拿上这支火把吧。这是我还被允许递过这条线的唯一一点帮助。
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 你好，我是教皇。

# speaker:pope
# pace:30
- 又到了证明你信仰的时候了，为我们的教会献上一份心意吧。

# speaker:pope
# pace:30
- 我需要 {contributionCostLabel} 金币来救济穷人。

* [付给他 {contributionCostLabel} 金币]
    -> pay_contribution

* [改信别的宗教]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 愿你的灵魂在来世得到嘉奖！

# speaker:pope
# pace:30
- 请收下这 100 名牧师，作为教会的谢礼。

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 愿你的灵魂在来世受到诅咒！

# speaker:pope
# pace:30
# chain_next
# wait:500
- 还有……

# speaker:pope
# pace:30
- 要是那头大蜥蜴被某种更高的力量治愈了，那可就太遗憾了……

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(治疗的声音\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
我这儿有食物、木材和矿石，售价

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
金币。你想买哪一样？

* { canAffordTrading > 0 } [{resourceAmountLabel} 食物]
    -> buy_food

* { canAffordTrading > 0 } [{resourceAmountLabel} 木材]
    -> buy_wood

* { canAffordTrading > 0 } [{resourceAmountLabel} 矿石]
    -> buy_ore

* [都不要]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
多谢，下次跑商再见。

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
多谢，下次跑商再见。

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
多谢，下次跑商再见。

  -> END


=== farewell ===

# speaker:salesman
下次跑商再见。

* [再会]
    -> END

* [来得少一些吧]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
明白了。我会把来访间隔拉长些。

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
哇，你真的做到了！

# speaker:king
# pace:30
- 太感谢你斩杀了那条巨龙。你就是我们的英雄！

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
现在我们终于可以……

# speaker:princess
# classes:scared
# pace:200
那是什么声音？

# speaker:shadow
# pace:200
# classes:angry
你杀了我的孩子！！！

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
这

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
才叫

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
一条大龙！

# speaker:princess
# pace:20
# events:resume_game
不好，求求你再帮帮我们？！？

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- 弗萨尔死了。你做到了千军万马都做不到的事。

# speaker:king
# pace:28
# classes:victory
谢谢你。真心的。

# speaker:princess
# pace:30
# classes:victory
跟我来……我们得为将来可能出现的新敌人做准备。

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
他到底是怎么回来的？

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- 我不知道他是怎么回来的。

# speaker:king
# pace:28
- 但能那样回来，靠的是惊人的意志。

# speaker:princess
# pace:40
# classes:scared
- 还有某种复仇的执念……

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
你知道吗，你每进一次地下城

# classes:angry-worker
# pace:30
- 我就得纯手工重新砌一整座迷宫？！？

# chain_next
# pace:50
- 那些箱子我们搬了好几周。他说别问是哪儿来的。

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
终于！

# pace:40
- 国王说我干完这一层就算完事，可以把镐子还给他了。

  -> END
"""

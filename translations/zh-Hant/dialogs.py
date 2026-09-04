# -*- coding: utf-8 -*-
"""Writes the Traditional Chinese .ink dialogues.

Converted from the Simplified text with opencc's s2twp, which does the Taiwanese
phrase substitutions and not merely the character mapping, then read through.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
看來你需要幫手來產出更多資源……

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
不妨買些學徒制，來培養更多農夫、礦工和伐木工。
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
又見面了！

# speaker:engineer
我們繼續研究了你的攻城武器。

# speaker:engineer
# wait:300
# pace:30
它現在能把貓射向敵人，我們認為這足以扭轉戰局。

# speaker:engineer
# wait:300
# pace:30
# chain_next
我們管它叫「投貓機」

# speaker:engineer
# wait:300
# pace:300
（意味深長的停頓）

# speaker:engineer
# pace:30
你願意為現有和今後購買的投石機投資這項改造嗎？

* [我還是想繼續扔石頭]
    -> no_thanks

* [支付 {catapultCostLabel} 金幣]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
用後記得告訴我們感想！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
用後記得告訴我們感想！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
真可惜。那也祝你好運。

  -> END

"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- 你的部隊把最後一擊留給了你。

# speaker:king
# pace:30
- 機會來了，親手了結它吧！

  -> END

"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
國王讓你繼續練手，以防日後來了更大的傢伙。

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
這次他甚至願意出錢，讓你隨心所欲地組建軍隊。

# speaker:princess
# pace:40
# chain_next
# wait:500
可幾個月前我求他辦一場盛大的生日會時，

# speaker:princess
# pace:40
# chain_next
# wait:500
他卻滿口……

# speaker:princess
# pace:60
# classes:imitating
「哎呀呀，王國沒錢啦，我的女兒！」


# speaker:princess
# pace:37
不過這個木人樁看著有點怪……


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
什麼？我還以為它是打不倒的。

# speaker:princess
# pace:20
# classes:love
不過，還有什麼是我的英雄打不倒的呢？

# speaker:princess
# events:whistle
# pace:50
等等，上面那是什麼？

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
那可不是普通的練習木樁。

# speaker:princess
# pace:30
它看著像個魔法玩具。給比我們大得多的東西玩的。

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
喂，那邊那位……

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
我找到了這些通往城堡底下秘密地下城的鑰匙。

# speaker:rogue
# pace:30
# wait:500
不知道國王曉不曉得那地方的存在。

# speaker:rogue
# pace:10
# chain_next
# wait:500
不過話說回來……

# speaker:rogue
# pace:30
我幾趟下來撈到不少好東西，但上一趟火把差點燒完。

# speaker:rogue
# wait:500
我怕再進去會在黑暗裡迷路，所以這些鑰匙就全都免費給你了。

# speaker:rogue
# pace:100
# chain_next
# wait: 300
祝你好運，

# speaker:rogue
# pace:100
# events:end_give_keys
千萬小心。

  -> END

"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
嘿！我是開發者。

# pace:40
抱歉你穿牆了。這是我這邊的 bug。

# pace:30
我可以把你從虛空裡帶出來，戰利品也照樣都歸你。

* [放棄並保留戰利品]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
再見！
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
你好，英雄！

# speaker:engineer
# pace:30
# events:show_engineering_tab
為助你作戰，陛下已下令王室建築師與工程師協會前來提供技術支援。

# speaker:engineer
# pace:30
我們將從三個方面協助你：

# speaker:engineer
# pace:30
- 建造用於攻城的投石機。

# speaker:engineer
# pace:30
- 由我們的建造者興建二級建築。

# speaker:engineer
# pace:30
- 由我們的工程師創立更高階的組織。

# speaker:engineer
# pace:30
等你攢夠金幣，就到工程標籤頁找我們吧。

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
噢，你以為「解僱一些單位」是什麼意思？

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
殺了我還不夠？拜託別再煩我了！

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
嘰嘰喳喳，你個小雜碎！

-> END
"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
我準備好為你的部隊演奏，激勵他們把力量放大了。

# speaker:bard_dialog
# pace:35
# wait:400
點擊豎琴按鈕，享受這段短暫的強化吧！

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
一條巨龍正在摧毀我們的村莊！

# speaker:king
# wait:300
# pace:30
- 我們需要一位英雄來拯救大家。

# speaker:king
# pace:30
- 請用你威武的寶劍／滑鼠游標斬殺這條巨龍。

# speaker:king
# pace:30
- 如果金幣夠多，你或許還能招募一些幫手。

# speaker:king
# pace:30
- 祝你好運！

  -> END

"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
不知怎的，弗薩爾又回來了！

# speaker:king
# pace:30
# wait:400
可你已經遣散了部隊。現在只能重新招募了。

# speaker:king
# wait:300
# pace:30
- 而且上次的襲擊毀了我們的經濟，我沒法再資助你的軍隊。

# speaker:king
# pace:40
# chain_next
- 他們現在會消耗

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- 食物、木材和礦石。

# speaker:king
# pace:40
- 你得把資源管好。

# speaker:king
# pace:40
- 自行切換每個單位此刻是否消耗資源。

# speaker:king
# pace:40
- 或者「解僱」一部分，讓他們少吃點，但還能幹些活。

# speaker:king
# pace:28
- 祝你好運！

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
很遺憾，我們的兵力不足以擋住這次入侵。

# speaker:king
# pace:20
# events:resume_dialogs_timer
派去的單位全軍覆沒，贖金那筆錢也一併沒了。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
我們的部隊帶回了好訊息！

# speaker:king
# pace:30
他們以極小的損失擋住了這次入侵。

# speaker:king
# pace:30
# events:resume_dialogs_timer
歡迎他們歸隊（繼續和那條龍耗下去……）

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
鄰國正在進攻我們。

# speaker:king
# pace:30
他們索要 {ransomCostLabel} 金幣來停止入侵。

# speaker:king
# chain_next
# pace:30
# wait:500
你覺得我們該怎麼辦？

* [支付 {ransomCostLabel} 金幣]
    -> pay_enemy

* { unitsCountFew > 3 } [派 {unitsCountFew} 個單位防守]
    -> send_few_units

* { unitsCountMany > 3 } [派 {unitsCountMany} 個單位防守]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 但願他們肯接受我們的條件。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 但願這些人夠用。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 這下總該能擋住他們的進攻了。
~ strategyChoice = "send_many_units"

  -> END

"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
至少……我不是窮死的。

# speaker:king
# pace:60
# classes:victory
不過，恭喜你通關了。

# speaker:king
# events:sigh
# pace:200
……

# speaker:princess
# pace:50
# classes:angry
你殺了我父親！！！

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
我才是你父親！

# speaker:princess
# pace:150
……

# speaker:princess
# pace:50
# chain_next
# wait:500
開發者？

# speaker:princess
# pace:50
你在遊戲裡塞了兩個《星球大戰》的梗？認真的嗎？！？

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
沒錯，我從龍巢裡拿了東西。金幣是給王國的。那個玩具算個紀念品。

# speaker:king
# pace:30
我們的子民在捱餓。換一次我還會這麼做。

# speaker:king
# pace:30
收下這筆封口費，你我都能全身而退。

# speaker:king
# pace:30
是要背叛我，還是收下我的好意？

* [必須有人阻止你！]
  -> go_against_king

* [我確實挺喜歡金幣的！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就這樣吧！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
那就拿走你那一份。

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
我給你的金幣已經超出你最大的貪念了。

# speaker:king
# pace:30
說好的就是這樣。拿了錢就走吧。

* [不管，必須有人阻止你]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
那就這樣吧！

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
你用我的金幣買下了那支殺死他孩子的軍隊。

# speaker:king
# pace:32
別裝作自己是無辜的。

# speaker:king
# pace:30
那就來吧。

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
這麼說你欠了王國一屁股債，是吧？別慌……公會里欠我們錢的冤大頭多的是。


# speaker:rogue
# pace:40
# wait:400
他們要是不還，我們就打斷幾條腿。

# speaker:rogue
# pace:30
# wait:400
在你還清之前，我的盜賊們替你收金幣的效率會翻倍。

  -> END
"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
唉！我們的法力儲備已經見底了。

# speaker:wizard_dialog
# pace:35
# wait:400
沒有奧術精華，我無法對巨龍引導法術。

# speaker:wizard_dialog
# pace:35
# wait:400
每當我們枯竭時，請到升級選單購買[補充法力]……好讓我們再次痛擊這頭野獸！

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
有人見過國王嗎？他不見了。

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
最後有人看見他時，他正往城堡底下的地下城走去。

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
歡迎！

# pace:45
我是穆克，年輕又公正！

# pace:50
國王把我放在這兒免得你迷路，說真的；我就喜歡給人指路。

# pace:35
我不能離開這塊地磚。先是「幫助每一位旅人」，然後是「別越過那條線」。我一直告訴自己這是規矩。可最近……我不太確定了。

# pace:25
不過嘿，拿上這支火把吧。這是我還被允許遞過這條線的唯一一點幫助。
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 你好，我是教皇。

# speaker:pope
# pace:30
- 又到了證明你信仰的時候了，為我們的教會獻上一份心意吧。

# speaker:pope
# pace:30
- 我需要 {contributionCostLabel} 金幣來救濟窮人。

* [付給他 {contributionCostLabel} 金幣]
    -> pay_contribution

* [改信別的宗教]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 願你的靈魂在來世得到嘉獎！

# speaker:pope
# pace:30
- 請收下這 100 名牧師，作為教會的謝禮。

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 願你的靈魂在來世受到詛咒！

# speaker:pope
# pace:30
# chain_next
# wait:500
- 還有……

# speaker:pope
# pace:30
- 要是那頭大蜥蜴被某種更高的力量治癒了，那可就太遺憾了……

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(治療的聲音\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
我這兒有食物、木材和礦石，售價

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
金幣。你想買哪一樣？

* { canAffordTrading > 0 } [{resourceAmountLabel} 食物]
    -> buy_food

* { canAffordTrading > 0 } [{resourceAmountLabel} 木材]
    -> buy_wood

* { canAffordTrading > 0 } [{resourceAmountLabel} 礦石]
    -> buy_ore

* [都不要]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
多謝，下次跑商再見。

  -> END


=== farewell ===

# speaker:salesman
下次跑商再見。

* [再會]
    -> END

* [來得少一些吧]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
明白了。我會把來訪間隔拉長些。

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
哇，你真的做到了！

# speaker:king
# pace:30
- 太感謝你斬殺了那條巨龍。你就是我們的英雄！

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
現在我們終於可以……

# speaker:princess
# classes:scared
# pace:200
那是什麼聲音？

# speaker:shadow
# pace:200
# classes:angry
你殺了我的孩子！！！

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
這

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
一條大龍！

# speaker:princess
# pace:20
# events:resume_game
不好，求求你再幫幫我們？！？

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- 弗薩爾死了。你做到了千軍萬馬都做不到的事。

# speaker:king
# pace:28
# classes:victory
謝謝你。真心的。

# speaker:princess
# pace:30
# classes:victory
跟我來……我們得為將來可能出現的新敵人做準備。

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
他到底是怎麼回來的？

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- 我不知道他是怎麼回來的。

# speaker:king
# pace:28
- 但能那樣回來，靠的是驚人的意志。

# speaker:princess
# pace:40
# classes:scared
- 還有某種復仇的執念……

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
你知道嗎，你每進一次地下城

# classes:angry-worker
# pace:30
- 我就得純手工重新砌一整座迷宮？！？

# chain_next
# pace:50
- 那些箱子我們搬了好幾周。他說別問是哪兒來的。

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
終於！

# pace:40
- 國王說我幹完這一層就算完事，可以把鎬子還給他了。

  -> END
"""

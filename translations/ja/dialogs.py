# -*- coding: utf-8 -*-
"""Writes the Japanese .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Voice per speaker rather than one register for all: the King speaks formally and
asks rather than orders (〜ですか / 〜てくれ), the Princess is familiar (〜ね / 〜よ),
the rogue is blunt (〜だ / 〜な), the Pope is archaic-polite, and the developer breaks
the fourth wall in plain casual speech.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
資源をもっと増やす手が要るようですね……

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
徒弟制を買えば、農夫・鉱夫・木こりを増やせますよ。
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
またお会いしましたね！

# speaker:engineer
攻城兵器の研究を続けておりました。

# speaker:engineer
# wait:300
# pace:30
今では猫を敵に撃ち出せます。戦いの流れを変えられるかと。

# speaker:engineer
# wait:300
# pace:30
# chain_next
名付けて「キャッタパルト」

# speaker:engineer
# wait:300
# pace:300
（もったいぶった間）

# speaker:engineer
# pace:30
今あるぶんも、これから買うぶんも改修しますか？

* [岩を撃ち続けたい]
    -> no_thanks

* [金貨{catapultCostLabel}を払う]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
感想をぜひ聞かせてください！

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
感想をぜひ聞かせてください！

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
残念です。ともあれご武運を。

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- 部隊が最後の一撃をそなたに残してくれた。

# speaker:king
# pace:30
- 今こそとどめを刺すときだ！

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
王さまが、もっと大きいのが来るかもしれないから訓練を続けてほしいって。

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
今回はあなたの好きなように軍を組めるよう、費用まで出すそうよ。

# speaker:princess
# pace:40
# chain_next
# wait:500
でも数か月前、私が盛大な誕生日パーティーをねだったときは、

# speaker:princess
# pace:40
# chain_next
# wait:500
こうだったのに……

# speaker:princess
# pace:60
# classes:imitating
「ぶつぶつぶつ、王国に金はないのだ、我が娘よ！」


# speaker:princess
# pace:37
それにしても、変わった人形ね……


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
えっ？ 倒せるものだとは思わなかったわ。

# speaker:princess
# pace:20
# classes:love
でも、私の英雄に倒せないものなんてあるのかしら。

# speaker:princess
# events:whistle
# pace:50
なに、あの上のあれは何？

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
これはただの訓練人形じゃないわ。

# speaker:princess
# pace:30
魔法のおもちゃみたい。私たちよりずっと大きな何かのための。

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
おい、そこのあんた……

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
城の下の隠しダンジョンの鍵を見つけたんだ。

# speaker:rogue
# pace:30
# wait:500
王はその存在を知ってるのかね。

# speaker:rogue
# pace:10
# chain_next
# wait:500
まあ、それはいい……

# speaker:rogue
# pace:30
潜るたびにいい戦利品を持ち帰ったが、この前は松明が消えかけてな。

# speaker:rogue
# wait:500
また入って闇で迷うのが怖い。だから鍵は全部あんたにやるよ、ただでいい。

# speaker:rogue
# pace:100
# chain_next
# wait: 300
幸運を、

# speaker:rogue
# pace:100
# events:end_give_keys
くれぐれも気をつけてな。

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
やあ！ 開発者だよ。

# pace:40
壁をすり抜けさせてごめん。こっちのバグだ。

# pace:30
虚空から出してあげる。戦利品はぜんぶそのままだよ。

* [あきらめて戦利品を持ち帰る]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
じゃあね！
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
こんにちは、英雄殿！

# speaker:engineer
# pace:30
# events:show_engineering_tab
この戦いを助けるため、陛下は王室建築技師団に技術の提供をお命じになりました。

# speaker:engineer
# pace:30
我々は三つの形でお力添えします。

# speaker:engineer
# pace:30
- 攻城用のカタパルトを造ること。

# speaker:engineer
# pace:30
- 建築士による、第二段階の建物を建てること。

# speaker:engineer
# pace:30
- 技師による、上位の組織を興すこと。

# speaker:engineer
# pace:30
金貨が貯まりましたら、「工学」タブにおります。

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
おや、「ユニットを解雇する」とはどういう意味だと思っていた？

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
殺しただけでは足りぬか？ もう放っておいてくれ！

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
チュンチュン、クソ野郎！

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
部隊のために一曲奏でて、力を高める用意ができています。

# speaker:bard_dialog
# pace:35
# wait:400
ハープのボタンを押して、一時の力の高まりをお楽しみください！

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
助けてくれ！

# speaker:king
# chain_next
# pace:30
# wait:500
巨大なドラゴンが村を壊しておる！

# speaker:king
# wait:300
# pace:30
- 我らを救う英雄が要る。

# speaker:king
# pace:30
- どうかその勇ましき剣、いやマウスカーソルでドラゴンを討ってくれ。

# speaker:king
# pace:30
- 金貨が足りていれば、助けを雇うこともできよう。

# speaker:king
# pace:30
- 武運を祈る！

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
どういうわけか、フォルスアールが戻ってきた！

# speaker:king
# pace:30
# wait:400
だがそなたは部隊を解散させた。また集め直さねばならぬ。

# speaker:king
# wait:300
# pace:30
- 先の襲撃で国庫は傾いた。もう軍を養ってはやれぬ。

# speaker:king
# pace:40
# chain_next
- これからは彼らが消費する。

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- 食料、木材、そして鉱石をな。

# speaker:king
# pace:40
- 資源はうまく回さねばならぬ。

# speaker:king
# pace:40
- どのユニットに資源を使わせるか、そのつど切り替えるがよい。

# speaker:king
# pace:40
- あるいは幾人か「解雇」せよ。消費は減るが、いくらかは働く。

# speaker:king
# pace:28
- 武運を祈る！

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
残念だが、我らの兵では侵攻を防ぎきれなかった。

# speaker:king
# pace:20
# events:resume_dialogs_timer
兵は一人残らず失い、身代金の額まで失った。
  -> END

=== send_many_units ===

# speaker:king
# pace:30
部隊が吉報とともに帰ってきた！

# speaker:king
# pace:30
被害を最小限に抑えて侵攻を退けたそうだ。

# speaker:king
# pace:30
# events:resume_dialogs_timer
彼らを迎えよう（そしてまたドラゴンとの果てなき戦いへ……）

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
隣国が攻めてきた。

# speaker:king
# pace:30
侵攻をやめる代わりに金貨{ransomCostLabel}枚を要求しておる。

# speaker:king
# chain_next
# pace:30
# wait:500
どうするのがよいと思う？

* [金貨{ransomCostLabel}枚を払う]
    -> pay_enemy

* { unitsCountFew > 3 } [{unitsCountFew}体で防ぐ]
    -> send_few_units

* { unitsCountMany > 3 } [{unitsCountMany}体で防ぐ]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 受け入れてくれることを願おう。
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- これで足りることを願おう。
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- これだけあれば必ず退けられよう。
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
せめて……貧しいままでは死ななんだ。

# speaker:king
# pace:60
# classes:victory
ともあれ、クリアおめでとう。

# speaker:king
# events:sigh
# pace:200
……

# speaker:princess
# pace:50
# classes:angry
父を殺したわね！！！

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
いいや……

# speaker:developer
# pace:100
# classes:vader
私がお前の父だ！

# speaker:princess
# pace:150
……

# speaker:princess
# pace:50
# chain_next
# wait:500
開発者？

# speaker:princess
# pace:50
自分のゲームにスター・ウォーズのネタを二つも入れたの？ 本気で？！？

# events:return_to_infinite
# pace:40
# classes:vader
……


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
見つかってしまったか。

# speaker:king
# pace:32
そうだ、ドラゴンの巣から持ち出した。金貨は王国のため。あの人形は土産にな。

# speaker:king
# pace:30
民は飢えていた。何度でも同じことをする。

# speaker:king
# pace:30
袖の下を受け取って黙っておれ。それで互いに無事に済む。

# speaker:king
# pace:30
我を裏切るか、贈り物を受けるか。

* [あなたを止めねばならない！]
  -> go_against_king

* [金貨は好きだ！]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
ならばよい！

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
では、そなたの取り分だ。

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
望み以上の金貨はもう与えたはずだ。

# speaker:king
# pace:30
それが約束であった。受け取って去るがよい。

* [関係ない、あなたを止める]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
ならばよい！

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
我が金貨で軍を買い、その子を殺したのはそなただ。

# speaker:king
# pace:32
潔白のふりをするな。

# speaker:king
# pace:30
さあ、来るがよい。

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
王国に借金しちまったのか？ 心配するな……ギルドには借りのある間抜けが山ほどいる。


# speaker:rogue
# pace:40
# wait:400
払わなけりゃ、足の一本や二本は折る。

# speaker:rogue
# pace:30
# wait:400
黒字に戻るまで、うちの盗賊が倍の勢いで金貨を集めてやるよ。

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
ああ！ マナの蓄えが尽きてしまいました。

# speaker:wizard_dialog
# pace:35
# wait:400
秘術の源なくしては、ドラゴンへ呪文を放てません。

# speaker:wizard_dialog
# pace:35
# wait:400
尽きるたびにアップグレード画面で「マナ回復」をお買い求めください……再びあの獣を討てるように！

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
誰か王さまを見なかった？ 行方が分からないの。

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
最後に見た人の話だと、城の下のダンジョンへ向かったそうよ。

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
ようこそ！

# pace:45
おいらはムーク、若くて正しい者！

# pace:50
迷わないようにって王さまがここに置いたんだ。本当だよ、道を教えるのは好きだからね。

# pace:35
このタイルから出ちゃいけないんだ。「旅人はみんな助けなさい」、そのあとに「あの線は越えるな」。規則だと自分に言い聞かせてきた。最近は……どうも自信がないな。

# pace:25
でもほら、この松明を持っていって。線の向こうへ渡せる、たったひとつの助けさ。
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

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
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
食料、木材、鉱石を売ってるよ。お代は

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
金貨。どれにする？

* { canAffordTrading > 0 } [食料 {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [木材 {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [鉱石 {resourceAmountLabel}]
    -> buy_ore

* [何もいらない]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
どうも、次の行商でまた会おう。

  -> END


=== farewell ===

# speaker:salesman
次の行商でまた会おう。

* [ではまた]
    -> END

* [来る回数を減らしてくれ]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
承知した。間を空けて回ることにするよ。

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
すごい、本当にやったのね！

# speaker:king
# pace:30
- ドラゴンを討ってくれて心から感謝する。そなたこそ我らの英雄だ！

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
これでようやく……

# speaker:princess
# classes:scared
# pace:200
今の音は何？

# speaker:shadow
# pace:200
# classes:angry
我が子を殺したな！！！

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
これぞ

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
まさに

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
大きなドラゴン！

# speaker:princess
# pace:20
# events:resume_game
そんな、助けてくれるわよね？！？

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- フォルスアールは倒れた。どの軍にもできなかったことをあなたがやったのよ。

# speaker:king
# pace:28
# classes:victory
礼を言う。心からな。

# speaker:princess
# pace:30
# classes:victory
ついてきて……新しい敵が来ても大丈夫なように備えましょう。

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
どうして戻ってこられたの？

# speaker:princess
# pace:300
# classes:victory
．　．　．

# speaker:king
# pace:30
- どうやって戻ったのかは分からぬ。

# speaker:king
# pace:28
- だがあのように蘇るには、並外れた執念が要る。

# speaker:princess
# pace:40
# classes:scared
- それに、何かへの復讐心も……

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
知ってるか、あんたがダンジョンに入るたびに

# classes:angry-worker
# pace:30
- おれが迷路をまるごと手で組み直してるんだぞ？！？

# chain_next
# pace:50
- 何週間もかけて宝箱を運び上げた。どこから来たかは聞くなと言われてな。

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
やっとだ！

# pace:40
- 王さまが、この階を終えたらつるはしを返して終わりにしていいと言ってくれた。

  -> END
"""

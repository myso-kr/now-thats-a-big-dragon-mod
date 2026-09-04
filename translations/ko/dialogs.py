# -*- coding: utf-8 -*-
"""Writes the Korean .ink dialogues.

The first language done, and the one the others were shaped against. Address is
informal throughout (-요/-야); the King keeps the archaic register a monarch would
(-노라/-거라) while still speaking to the hero directly.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
자원을 더 많이 만들어 낼 손이 필요해 보이는군요...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
견습 제도를 사 보세요. 농부와 광부, 나무꾼을 더 길러낼 수 있습니다.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
또 뵙는군요!

# speaker:engineer
당신의 공성 병기를 계속 연구했습니다.

# speaker:engineer
# wait:300
# pace:30
이제 적에게 고양이를 쏠 수 있습니다. 전황을 뒤집을 물건이라고 봅니다.

# speaker:engineer
# wait:300
# pace:30
# chain_next
이름하여 "캣-아-펄트"

# speaker:engineer
# wait:300
# pace:300
(극적인 침묵)

# speaker:engineer
# pace:30
지금 보유한 것과 앞으로 살 것 모두 개조하는 데 투자하시겠습니까?

* [그냥 계속 바위를 쏘겠소]
    -> no_thanks

* [금화 {catapultCostLabel}닢 지불]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
써 보시고 소감을 꼭 들려주십시오!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
써 보시고 소감을 꼭 들려주십시오!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
아쉽군요. 그래도 행운을 빕니다.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- 그대의 부대가 마지막 일격을 남겨 두었소.

# speaker:king
# pace:30
- 이제 완전히 끝장낼 기회요!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
아버지께서 더 큰 일이 닥칠지 모르니 계속 훈련하라 하셨어요.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
이번엔 군대 자금까지 대주시겠대요. 원하는 대로 꾸려 보라면서요.

# speaker:princess
# pace:40
# chain_next
# wait:500
그런데 몇 달 전에 제가 성대한 생일 파티를 열어 달라고 했을 땐,

# speaker:princess
# pace:40
# chain_next
# wait:500
하시는 말씀이...

# speaker:princess
# pace:60
# classes:imitating
"어쩌고 저쩌고, 왕국엔 돈이 없단다, 내 딸아!"


# speaker:princess
# pace:37
그나저나 저 허수아비, 생김새가 좀 이상한데요...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
네? 저걸 쓰러뜨릴 수 있을 줄은 몰랐어요.

# speaker:princess
# pace:20
# classes:love
제 영웅님이 못 이기는 게 있긴 한가요?

# speaker:princess
# events:whistle
# pace:50
어, 저 위에 저건 뭐죠?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
저건 그냥 훈련용 허수아비가 아니에요.

# speaker:princess
# pace:30
마법 장난감처럼 보이는데요. 우리보다 훨씬 큰 무언가를 위한.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
어이, 거기 당신...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
성 지하의 비밀 던전 열쇠를 손에 넣었소.

# speaker:rogue
# pace:30
# wait:500
왕이 그 존재를 알고는 있을지 모르겠군.

# speaker:rogue
# pace:10
# chain_next
# wait:500
아무튼...

# speaker:rogue
# pace:30
몇 번 들어가서 꽤 괜찮은 걸 챙겼는데, 지난번엔 횃불이 거의 다 타 버렸소.

# speaker:rogue
# wait:500
어둠 속에서 길을 잃을까 무서워 다시는 못 들어가겠소. 그러니 열쇠는 전부 그냥 넘기지.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
행운을 비오,

# speaker:rogue
# pace:100
# events:end_give_keys
부디 조심하시오.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
안녕하세요! 개발자입니다.

# pace:40
벽을 뚫고 나가셨군요. 제 쪽 버그입니다. 죄송합니다.

# pace:30
허공에서 빼내 드릴게요. 챙긴 전리품은 그대로 두셔도 됩니다.

* [포기하고 전리품은 챙기기]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
안녕히!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
안녕하십니까, 영웅이시여!

# speaker:engineer
# pace:30
# events:show_engineering_tab
싸움을 돕기 위해, 폐하께서 왕립 건축가 기술자 협회에 우리의 기술을 빌려주라 명하셨습니다.

# speaker:engineer
# pace:30
저희는 세 가지로 돕겠습니다:

# speaker:engineer
# pace:30
- 공성전을 위한 투석기 건조.

# speaker:engineer
# pace:30
- 건축가를 통한 2단계 건물 건설.

# speaker:engineer
# pace:30
- 기술자를 통한 상위 조직 설립.

# speaker:engineer
# pace:30
자금이 마련되면 공학 탭에서 저희를 찾으십시오.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
아니, '유닛을 해고한다'는 말이 무슨 뜻인 줄 알았소?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
죽인 것으로도 모자라오? 제발 그만 좀 귀찮게 하시오!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
짹짹, 이 자식아!

-> END
"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
부대 앞에서 연주해 그들의 힘을 끌어올릴 준비가 됐습니다.

# speaker:bard_dialog
# pace:35
# wait:400
하프 버튼을 누르고 잠시 동안의 힘 상승을 즐기세요!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
도와주시오!

# speaker:king
# chain_next
# pace:30
# wait:500
거대한 드래곤이 우리 마을을 부수고 있소!

# speaker:king
# wait:300
# pace:30
- 우리를 구해 줄 영웅이 필요하오.

# speaker:king
# pace:30
- 부디 그 위대한 검, 아니 마우스 커서로 저 드래곤을 처치해 주시오.

# speaker:king
# pace:30
- 금화가 넉넉하다면 도와줄 이들을 모을 수도 있을 것이오.

# speaker:king
# pace:30
- 행운을 비오!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
어찌 된 일인지, 포르타르가 돌아왔소!

# speaker:king
# pace:30
# wait:400
헌데 그대는 부대를 해산했지. 이제 다시 모아야 하오.

# speaker:king
# wait:300
# pace:30
- 게다가 지난 공격으로 나라 살림이 거덜 나 군대를 지원할 수가 없소.

# speaker:king
# pace:40
# chain_next
- 이제 그들은

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- 식량과 목재, 광석을 소비할 것이오.

# speaker:king
# pace:40
- 자원을 잘 관리해야 하오.

# speaker:king
# pace:40
- 각 유닛이 언제 자원을 소비할지 켜고 끄시오.

# speaker:king
# pace:40
- 아니면 일부를 '해고'해 소비는 줄이면서 일은 얼마간 시키시오.

# speaker:king
# pace:28
- 행운을 비오!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
안타깝게도 우리 병력으로는 침공을 막아내지 못했소.

# speaker:king
# pace:20
# events:resume_dialogs_timer
유닛을 하나도 남김없이 잃었고, 그 결과 몸값으로 낼 돈까지 잃고 말았소.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
부대가 좋은 소식을 가지고 돌아왔소!

# speaker:king
# pace:30
피해를 거의 입지 않고 침공을 막아냈다는군.

# speaker:king
# pace:30
# events:resume_dialogs_timer
그들의 귀환을 환영하오. (다시 드래곤과의 지루한 싸움을 이어가기 위해...)

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
이웃 왕국이 우리를 공격하고 있소.

# speaker:king
# pace:30
침공을 멈추는 대가로 금화 {ransomCostLabel}닢을 요구했소.

# speaker:king
# chain_next
# pace:30
# wait:500
어찌하면 좋겠소?

* [금화 {ransomCostLabel}닢을 지불한다]
    -> pay_enemy

* { unitsCountFew > 3 } [유닛 {unitsCountFew}로 방어한다]
    -> send_few_units

* { unitsCountMany > 3 } [유닛 {unitsCountMany}로 방어한다]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- 저들이 우리 제안을 받아들이길 바랄 뿐이오.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- 이 정도면 충분하길 바라오.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- 이 정도면 저들의 공격쯤은 확실히 막아내겠지.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
적어도... 가난하게 죽지는 않았군.

# speaker:king
# pace:60
# classes:victory
그나저나, 게임을 끝낸 것 축하하오.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
네가 우리 아버지를 죽였어!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
아니...

# speaker:developer
# pace:100
# classes:vader
내가 네 아비다!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
개발자님?

# speaker:princess
# pace:50
게임에 스타워즈 패러디를 두 개나 넣으셨다고요? 진심이세요?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
날 찾아냈군.

# speaker:king
# pace:32
그렇소, 드래곤의 둥지에서 가져왔소. 금화는 왕국을 위해. 저 장난감은 기념품으로.

# speaker:king
# pace:30
백성이 굶고 있었소. 다시 그때로 돌아가도 똑같이 할 것이오.

# speaker:king
# pace:30
얼마간 받고 입을 다무시오. 그러면 둘 다 무사히 걸어 나갈 수 있소.

# speaker:king
# pace:30
날 배신하겠소, 아니면 내 선물을 받겠소?

* [당신을 여기서 멈춰야겠소!]
  -> go_against_king

* [사실 금화는 좋아하지!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
그렇다면 어쩔 수 없군!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
그럼 그대의 몫을 가져가시오.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
그대가 바라던 것 이상으로 이미 금화를 주었소.

# speaker:king
# pace:30
그것이 거래였소. 받았으면 물러가시오.

* [상관없소, 당신은 멈춰야 하오]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
그렇다면 어쩔 수 없군!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
그대는 내 금화로 군대를 사서 그자의 자식을 죽였소.

# speaker:king
# pace:32
결백한 척은 하지 마시오.

# speaker:king
# pace:30
자, 덤비시오.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
왕국에 빚을 지셨다고? 걱정 마시오... 길드엔 우리한테 돈 빌린 얼간이가 넘쳐나니까.


# speaker:rogue
# pace:40
# wait:400
안 갚으면 다리 몇 개쯤 부러뜨리면 되고.

# speaker:rogue
# pace:30
# wait:400
빚을 다 갚을 때까지, 내 도적들이 당신 몫의 금화를 두 배로 긁어모아 주지.

  -> END
"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
아아! 마나가 바닥나고 말았습니다.

# speaker:wizard_dialog
# pace:35
# wait:400
비전의 정수 없이는 드래곤에게 주문을 펼칠 수 없습니다.

# speaker:wizard_dialog
# pace:35
# wait:400
마나가 마를 때마다 업그레이드 메뉴에서 [마나 충전]을 구매하십시오... 그래야 저 괴물을 다시 칠 수 있습니다!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
혹시 아버지 보신 분 없나요? 사라지셨어요.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
마지막으로 목격됐을 때, 성 아래 던전으로 내려가고 계셨대요.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
어서 오세요!

# pace:45
저는 무크, 어리고 올바른 자입니다!

# pace:50
길을 잃지 마시라고 왕께서 저를 여기 두셨죠. 진심으로 말하는데, 저는 길 알려주는 게 좋아요.

# pace:35
이 타일 밖으로는 나갈 수 없어요. "모든 여행자를 도와라", 그리고 "저 선은 넘지 마라". 규정이려니 했죠. 요즘은... 잘 모르겠어요.

# pace:25
아무튼 이 횃불 받으세요. 이 선 너머로 건넬 수 있는, 제게 아직 허락된 유일한 도움이에요.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- 반갑네, 나는 교황일세.

# speaker:pope
# pace:30
- 다시 한번 그대의 믿음을 증명하고 교회에 헌금할 때가 되었네.

# speaker:pope
# pace:30
- 가난한 이들을 돕는 데 금화 {contributionCostLabel}닢이 필요하네.

* [금화 {contributionCostLabel}닢을 바친다]
    -> pay_contribution

* [다른 종교로 개종한다]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- 그대의 영혼이 내세에서 보답받기를!

# speaker:pope
# pace:30
- 교회의 감사의 표시로 이 성직자 100명을 받게.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- 그대의 영혼이 내세에서 저주받기를!

# speaker:pope
# pace:30
# chain_next
# wait:500
- 그리고 말이야...

# speaker:pope
# pace:30
- 저 거대한 도마뱀이 높으신 분의 힘으로 치유된다면 참으로 유감스럽겠군...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(치유하는 소리\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
식량, 목재, 광석을 팝니다. 가격은

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
금화올시다. 어느 것으로 드릴까요?

* { canAffordTrading > 0 } [식량 {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [목재 {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [광석 {resourceAmountLabel}]
    -> buy_ore

* [사지 않겠소]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
고맙습니다. 다음 행상 때 또 뵙지요.

  -> END


=== farewell ===

# speaker:salesman
다음 행상 때 또 뵙지요.

* [잘 가시오]
    -> END

* [좀 덜 오시오]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
알겠습니다. 방문 간격을 늘리지요.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
와, 정말로 해내셨네요!

# speaker:king
# pace:30
- 저 드래곤을 처치해 주어 정말 고맙소. 그대는 우리의 영웅이오!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
이제 드디어 우리는...

# speaker:princess
# classes:scared
# pace:200
방금 그 소리는 뭐죠?

# speaker:shadow
# pace:200
# classes:angry
네놈이 내 아들을 죽였구나!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
저건

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
진짜

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
거대한 드래곤이잖소!

# speaker:princess
# pace:20
# events:resume_game
안 돼, 제발 우릴 도와주실 거죠?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- 포르타르가 죽었어요. 어떤 군대도 못 한 일을 해내셨어요.

# speaker:king
# pace:28
# classes:victory
고맙소. 진심으로.

# speaker:princess
# pace:30
# classes:victory
따라오세요... 앞으로 닥칠 새로운 적들에 대비해야 해요.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
어떻게 다시 돌아온 거죠?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- 어떻게 돌아왔는지는 나도 모르오.

# speaker:king
# pace:28
- 허나 그렇게 되살아나려면 어마어마한 의지가 필요하지.

# speaker:princess
# pace:40
# classes:scared
- 그리고 어떤 식으로든 복수하려는 마음도요...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
당신이 던전에 들어올 때마다 말이죠

# classes:angry-worker
# pace:30
- 제가 미로를 통째로 손수 새로 지어야 한다는 거 아셨어요?!?

# chain_next
# pace:50
- 몇 주 동안 상자를 날랐어요. 어디서 났는지는 묻지 말라더군요.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
드디어!

# pace:40
- 이 층만 끝내면 다 끝났으니 곡괭이를 돌려줘도 된다고 왕께서 말씀하셨어요.

  -> END
"""

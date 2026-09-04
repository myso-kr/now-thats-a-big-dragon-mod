# -*- coding: utf-8 -*-
"""Writes the Thai .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Register: neutral polite, without ครับ/ค่ะ — those particles would fix each speaker's
gender, and several of them are the player. The King speaks a little more formally
(เจ้า for the hero), the rogue plainly, the Pope in a clerical register.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
ดูเหมือนคุณต้องการความช่วยเหลือในการผลิตทรัพยากรเพิ่ม...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
ลองซื้อการฝึกหัดดูสิ จะได้ชาวนา คนงานเหมือง และคนตัดไม้เพิ่มขึ้น
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
สวัสดีอีกครั้ง!

# speaker:engineer
เราวิจัยอาวุธล้อมเมืองของคุณต่อ

# speaker:engineer
# wait:300
# pace:30
ตอนนี้มันยิงแมวใส่ศัตรูได้แล้ว และเราคิดว่ามันจะพลิกสถานการณ์ได้

# speaker:engineer
# wait:300
# pace:30
# chain_next
เราเรียกมันว่า "แคท-อะ-พัลต์"

# speaker:engineer
# wait:300
# pace:300
(หยุดอย่างมีลีลา)

# speaker:engineer
# pace:30
อยากลงทุนปรับปรุงทั้งที่มีอยู่และที่จะซื้อในอนาคตไหม?

* [ขอยิงหินต่อไปดีกว่า]
    -> no_thanks

* [จ่าย {catapultCostLabel} ทอง]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
บอกเราด้วยว่าคิดยังไง!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
บอกเราด้วยว่าคิดยังไง!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
น่าเสียดาย ยังไงก็ขอให้โชคดี

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- กองกำลังของเจ้าเหลือหมัดสุดท้ายไว้ให้

# speaker:king
# pace:30
- นี่คือโอกาสที่จะจบมันให้สิ้นซาก!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
ราชาขอให้เธอฝึกต่อไป เผื่อว่าจะมีอะไรที่ใหญ่กว่านี้มา

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
คราวนี้ท่านถึงกับจะออกทุนให้กองทัพของเธอ เธอจะจัดยังไงก็ได้

# speaker:princess
# pace:40
# chain_next
# wait:500
แต่ตอนที่ฉันขอปาร์ตี้วันเกิดใหญ่ ๆ เมื่อไม่กี่เดือนก่อน

# speaker:princess
# pace:40
# chain_next
# wait:500
กลับได้แต่...

# speaker:princess
# pace:60
# classes:imitating
"บลา บลา บลา อาณาจักรไม่มีเงิน ลูกสาวของข้า!"


# speaker:princess
# pace:37
แต่หุ่นตัวนี้ดูแปลก ๆ นะ...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
อะไรนะ? ฉันไม่คิดว่าจะเอาชนะมันได้

# speaker:princess
# pace:20
# classes:love
แต่มีอะไรที่วีรบุรุษของฉันเอาชนะไม่ได้บ้างล่ะ?

# speaker:princess
# events:whistle
# pace:50
อะไร นั่นอะไรบนนั้น?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
นั่นไม่ใช่หุ่นฝึกซ้อมธรรมดา

# speaker:princess
# pace:30
ดูเหมือนของเล่นวิเศษ สำหรับอะไรที่ใหญ่กว่าพวกเรามาก

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
เฮ้ย เธอที่อยู่ตรงนั้น...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
ข้าเจอกุญแจดันเจียนลับใต้ปราสาทพวกนี้

# speaker:rogue
# pace:30
# wait:500
สงสัยว่าราชารู้เรื่องมันไหมนะ

# speaker:rogue
# pace:10
# chain_next
# wait:500
เอาเถอะ...

# speaker:rogue
# pace:30
ข้าได้ของดีมาไม่น้อยจากการลงไป แต่ครั้งล่าสุดคบเพลิงเกือบดับ

# speaker:rogue
# wait:500
ข้ากลัวจะเข้าไปแล้วหลงในความมืด เลยยกกุญแจทั้งหมดให้เธอฟรี ๆ

# speaker:rogue
# pace:100
# chain_next
# wait: 300
โชคดี

# speaker:rogue
# pace:100
# events:end_give_keys
แล้วก็ระวังตัวด้วยนะ

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
เฮ้! ผมเป็นคนทำเกมนี้เอง

# pace:40
ขอโทษที่คุณทะลุกำแพงไป เป็นบั๊กของผมเอง

# pace:30
ผมจะพาคุณออกจากความว่างเปล่า และของที่ได้มาจะยังอยู่ครบ

* [ยอมแพ้และเก็บของที่ได้ไว้]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
บ๊ายบาย!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
สวัสดี วีรบุรุษ!

# speaker:engineer
# pace:30
# events:show_engineering_tab
เพื่อช่วยในการต่อสู้ ฝ่าบาททรงมีบัญชาให้คณะสถาปนิกและวิศวกรแห่งราชสำนักมอบความรู้ของเรา

# speaker:engineer
# pace:30
เราจะช่วยคุณสามทาง:

# speaker:engineer
# pace:30
- สร้างเครื่องยิงหินสำหรับการล้อมเมือง

# speaker:engineer
# pace:30
- สร้างอาคารระดับสอง ด้วยมือช่างก่อสร้างของเรา

# speaker:engineer
# pace:30
- ก่อตั้งองค์กรระดับสูงขึ้น ด้วยมือวิศวกรของเรา

# speaker:engineer
# pace:30
เมื่อมีทองพอแล้ว มาหาเราได้ที่แท็บ "วิศวกรรม"

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
อ้าว แล้วเจ้าคิดว่า "ปลดหน่วยออก" หมายถึงอะไรล่ะ?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
ฆ่าข้าแล้วยังไม่พออีกหรือ? เลิกกวนข้าเสียที!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
จิ๊บ จิ๊บ ไอ้*****!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
ข้าพร้อมจะบรรเลงให้กองกำลังของท่าน และปลุกใจให้พลังของพวกเขาทวีขึ้น

# speaker:bard_dialog
# pace:35
# wait:400
กดปุ่มพิณแล้วเพลิดเพลินกับพลังที่เพิ่มขึ้นชั่วคราวได้เลย!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
ช่วยด้วย!

# speaker:king
# chain_next
# pace:30
# wait:500
มังกรยักษ์กำลังทำลายหมู่บ้านของเรา!

# speaker:king
# wait:300
# pace:30
- เราต้องการวีรบุรุษมาช่วยเรา

# speaker:king
# pace:30
- ขอจงสังหารมังกรตัวนี้ด้วยดาบอันทรงพลัง เอ้อ เคอร์เซอร์เมาส์ของเจ้า

# speaker:king
# pace:30
- ถ้ามีทองพอ เจ้าอาจเกณฑ์ผู้ช่วยมาได้ด้วย

# speaker:king
# pace:30
- ขอให้โชคดี!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
ไม่รู้ได้อย่างไร ฟอร์ธอาร์กลับมาแล้ว!

# speaker:king
# pace:30
# wait:400
แต่เจ้าปลดกองกำลังไปหมด ตอนนี้ต้องเกณฑ์ใหม่

# speaker:king
# wait:300
# pace:30
- และการโจมตีครั้งก่อนทำลายเศรษฐกิจของเรา ข้าจึงเลี้ยงกองทัพให้เจ้าไม่ได้

# speaker:king
# pace:40
# chain_next
- ต่อไปพวกเขาจะใช้

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- อาหาร ไม้ และแร่

# speaker:king
# pace:40
- เจ้าต้องบริหารทรัพยากรให้ดี

# speaker:king
# pace:40
- สลับดูว่าหน่วยไหนควรใช้ทรัพยากรตอนนี้ หน่วยไหนไม่ควร

# speaker:king
# pace:40
- หรือ "ปลด" บางหน่วยออก พวกเขาจะใช้น้อยลงแต่ยังทำงานได้บ้าง

# speaker:king
# pace:28
- ขอให้โชคดี!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
น่าเสียดายที่หน่วยของเราไม่พอจะต้านการรุกราน

# speaker:king
# pace:20
# events:resume_dialogs_timer
เราเสียหน่วยไปทุกหน่วย และเสียค่าไถ่ไปพร้อมกัน
  -> END

=== send_many_units ===

# speaker:king
# pace:30
กองกำลังกลับมาพร้อมข่าวดี!

# speaker:king
# pace:30
พวกเขาต้านการรุกรานได้โดยสูญเสียน้อยที่สุด

# speaker:king
# pace:30
# events:resume_dialogs_timer
เราต้อนรับพวกเขากลับมา (เพื่อกลับไปกร่อนมังกรกันต่อ...)

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
อาณาจักรข้างเคียงกำลังโจมตีเรา

# speaker:king
# pace:30
พวกเขาเรียกทอง {ransomCostLabel} เหรียญเพื่อหยุดการรุกราน

# speaker:king
# chain_next
# pace:30
# wait:500
เจ้าคิดว่าเราควรทำอย่างไร?

* [จ่ายทอง {ransomCostLabel} เหรียญ]
    -> pay_enemy

* { unitsCountFew > 3 } [ป้องกันด้วย {unitsCountFew} หน่วย]
    -> send_few_units

* { unitsCountMany > 3 } [ป้องกันด้วย {unitsCountMany} หน่วย]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- หวังว่าพวกเขาจะรับข้อเสนอของเรา
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- หวังว่าเท่านี้จะพอ
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- เท่านี้ต้องต้านการโจมตีของพวกเขาได้แน่
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
อย่างน้อย... ข้าก็ไม่ได้ตายอย่างยากจน

# speaker:king
# pace:60
# classes:victory
ยังไงก็ยินดีด้วยที่เล่นจบเกม

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
เธอฆ่าพ่อของฉัน!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
ไม่...

# speaker:developer
# pace:100
# classes:vader
ข้าคือพ่อของเจ้า!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
คนทำเกม?

# speaker:princess
# pace:50
ใส่มุก Star Wars ลงเกมตัวเองถึงสองครั้งเลยเหรอ? จริงดิ?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
เจ้าเจอข้าจนได้

# speaker:king
# pace:32
ใช่ ข้าเอามาจากรังมังกร ทองเพื่ออาณาจักร ของเล่นเก็บไว้เป็นที่ระลึก

# speaker:king
# pace:30
ผู้คนของเราอดอยาก ข้าจะทำแบบนี้อีกก็ได้

# speaker:king
# pace:30
รับสินบนแล้วเงียบไว้ แล้วเราทั้งคู่จะรอดไปด้วยกัน

# speaker:king
# pace:30
จะทรยศข้า หรือรับของกำนัลของข้า?

* [ต้องมีคนหยุดท่าน!]
  -> go_against_king

* [ข้าก็ชอบทองอยู่นะ!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
ก็ตามใจ!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
งั้นก็รับส่วนของเจ้าไป

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
ข้าให้ทองเจ้าไปมากเกินกว่าที่เจ้าเคยปรารถนาแล้ว

# speaker:king
# pace:30
นั่นคือข้อตกลง รับไปแล้วจากไปเสีย

* [ไม่สนใจ ต้องมีคนหยุดท่าน]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
ก็ตามใจ!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
เจ้าใช้ทองของข้าซื้อกองทัพที่ฆ่าลูกของมัน

# speaker:king
# pace:32
อย่าทำเป็นบริสุทธิ์

# speaker:king
# pace:30
งั้นก็มาเถอะ

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
เป็นหนี้อาณาจักรเข้าแล้วสินะ? ไม่ต้องห่วง... สมาคมมีพวกที่ติดหนี้เราอยู่เพียบ


# speaker:rogue
# pace:40
# wait:400
ถ้าไม่จ่าย เราก็หักขาสักสองข้าง

# speaker:rogue
# pace:30
# wait:400
จนกว่าเธอจะกลับมาเป็นบวก โจรของข้าจะเก็บทองให้เธอหนักเป็นสองเท่า

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
อนิจจา! มานาสำรองของเราหมดแล้ว

# speaker:wizard_dialog
# pace:35
# wait:400
ปราศจากแก่นเวทมนตร์ ข้าไม่อาจร่ายคาถาใส่มังกรได้

# speaker:wizard_dialog
# pace:35
# wait:400
ไปที่เมนูอัปเกรดแล้วซื้อ "เติมมานา" ทุกครั้งที่เราหมด... เราจะได้โจมตีอสูรตัวนั้นอีก!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
มีใครเห็นราชาบ้าง? ท่านหายไป

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
คนสุดท้ายที่เห็นบอกว่าท่านมุ่งหน้าไปยังดันเจียนใต้ปราสาท

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
ยินดีต้อนรับ!

# pace:45
ข้าคือมุก ผู้เยาว์วัยและเที่ยงธรรม!

# pace:50
ราชาให้ข้ามาอยู่ตรงนี้เพื่อไม่ให้เธอหลง และข้าพูดจริง ข้าชอบชี้ทาง

# pace:35
ข้าออกจากช่องนี้ไม่ได้ "ช่วยนักเดินทางทุกคน" แล้วก็ "อย่าข้ามเส้นนั้น" ข้าบอกตัวเองว่ามันคือระเบียบ แต่ช่วงหลัง... ข้าก็ไม่แน่ใจแล้ว

# pace:25
แต่เอานี่ไป คบเพลิงอันนี้ เป็นความช่วยเหลืออย่างเดียวที่ข้ายังส่งข้ามเส้นนี้ได้
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- สวัสดี ข้าคือสันตะปาปา

# speaker:pope
# pace:30
- ถึงเวลาพิสูจน์ศรัทธาของเจ้าอีกครั้ง และถวายแด่ศาสนจักรของเรา

# speaker:pope
# pace:30
- ข้าต้องการทอง {contributionCostLabel} เหรียญเพื่อช่วยคนยากไร้

* [ให้ทองท่าน {contributionCostLabel} เหรียญ]
    -> pay_contribution

* [เปลี่ยนไปนับถือศาสนาอื่น]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- ขอให้วิญญาณของเจ้าได้รับรางวัลในโลกหน้า!

# speaker:pope
# pace:30
- รับนักบวช 100 คนนี้ไว้ เป็นสัญลักษณ์แห่งความขอบคุณของศาสนจักร

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- ขอให้วิญญาณของเจ้าถูกสาปในโลกหน้า!

# speaker:pope
# pace:30
# chain_next
# wait:500
- อีกอย่าง...

# speaker:pope
# pace:30
- คงน่าเสียดายถ้ากิ้งก่ายักษ์ตัวนั้นได้รับการเยียวยาจากอำนาจเบื้องบน...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(เสียงเยียวยา\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
มีอาหาร ไม้ หรือแร่ ขายในราคา

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
ทอง อยากได้อันไหน?

* { canAffordTrading > 0 } [อาหาร {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [ไม้ {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [แร่ {resourceAmountLabel}]
    -> buy_ore

* [ไม่เอาอะไร]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
ขอบคุณ เจอกันรอบหน้าที่ผ่านมาทางนี้

  -> END


=== farewell ===

# speaker:salesman
เจอกันรอบหน้าที่ผ่านมาทางนี้

* [ลาก่อน]
    -> END

* [มาให้น้อยลงหน่อย]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
เข้าใจแล้ว จะเว้นระยะการมาให้ห่างขึ้น

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
ว้าว เธอทำได้จริง ๆ ด้วย!

# speaker:king
# pace:30
- ขอบคุณมากที่สังหารมังกรตัวนั้น เจ้าคือวีรบุรุษของเรา!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
ในที่สุดเราก็...

# speaker:princess
# classes:scared
# pace:200
เสียงอะไรน่ะ?

# speaker:shadow
# pace:200
# classes:angry
พวกเจ้าฆ่าลูกของข้า!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
นี่ต่างหาก

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ที่เรียกว่า

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
มังกรตัวใหญ่!

# speaker:princess
# pace:20
# events:resume_game
ไม่นะ เธอจะช่วยเราใช่ไหม?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- ฟอร์ธอาร์ตายแล้ว เธอทำสิ่งที่ไม่มีกองทัพไหนทำได้

# speaker:king
# pace:28
# classes:victory
ขอบใจ จากใจจริง

# speaker:princess
# pace:30
# classes:victory
ตามฉันมา... เราต้องเตรียมรับศัตรูใหม่ที่อาจมาถึง

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
เขากลับมาได้ยังไงกัน?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- ข้าไม่รู้ว่ามันกลับมาได้อย่างไร

# speaker:king
# pace:28
- แต่การลุกขึ้นมาแบบนั้นต้องใช้เจตจำนงที่น่าทึ่ง

# speaker:princess
# pace:40
# classes:scared
- และความอยากแก้แค้นบางอย่างด้วย...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
รู้ไหมว่าทุกครั้งที่เธอเข้าดันเจียน

# classes:angry-worker
# pace:30
- ข้าต้องสร้างเขาวงกตใหม่ทั้งอันด้วยมือนะ?!?

# chain_next
# pace:50
- เราขนหีบขึ้นมาเป็นสัปดาห์ ท่านบอกว่าอย่าถามว่ามันมาจากไหน

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
ในที่สุด!

# pace:40
- ราชาบอกว่าข้าเสร็จงานแล้ว และคืนอีเต้อให้ท่านได้หลังจบชั้นนี้

  -> END
"""

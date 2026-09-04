# -*- coding: utf-8 -*-
"""Writes the Vietnamese .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Vietnamese picks a pronoun per relationship, so the speakers differ: the King says
"ta"/"ngươi" as a monarch to a subject, the Princess "tôi"/"bạn" warmly, the rogue
"tôi"/"anh" plainly, and the Pope "ta"/"con" as a cleric.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Có vẻ bạn cần giúp để tạo thêm tài nguyên...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Hãy thử mua Học nghề để có thêm nông dân, thợ mỏ và tiều phu.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Lại gặp bạn rồi!

# speaker:engineer
Chúng tôi đã tiếp tục nghiên cứu vũ khí công thành của bạn.

# speaker:engineer
# wait:300
# pace:30
Giờ nó bắn được mèo vào kẻ địch, và chúng tôi tin nó sẽ xoay chuyển trận đấu.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Chúng tôi gọi nó là "Máy bắn mèo"

# speaker:engineer
# wait:300
# pace:300
(ngừng một nhịp cho kịch tính)

# speaker:engineer
# pace:30
Bạn có muốn đầu tư cải tiến cho cả cái đang có lẫn những cái sau này không?

* [Tôi vẫn muốn bắn đá]
    -> no_thanks

* [Trả {catapultCostLabel} vàng]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Nhớ cho chúng tôi biết cảm nghĩ nhé!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Nhớ cho chúng tôi biết cảm nghĩ nhé!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Tiếc thật. Dù sao cũng chúc bạn may mắn.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Quân của ngươi đã để dành đòn cuối cho ngươi.

# speaker:king
# pace:30
- Đây là cơ hội để kết liễu nó vĩnh viễn!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Vua cha bảo bạn hãy tiếp tục luyện tập, phòng khi có thứ gì lớn hơn tới.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Lần này cha còn chi tiền cho quân của bạn, để bạn tùy ý sắp xếp.

# speaker:princess
# pace:40
# chain_next
# wait:500
Vậy mà mấy tháng trước khi tôi xin một bữa tiệc sinh nhật thật lớn,

# speaker:princess
# pace:40
# chain_next
# wait:500
thì chỉ được nghe...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, vương quốc không có tiền, con gái ạ!"


# speaker:princess
# pace:37
Mà cái hình nộm này trông lạ thật đấy...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Gì cơ? Tôi không nghĩ là có thể hạ được nó.

# speaker:princess
# pace:20
# classes:love
Mà có gì mà anh hùng của tôi không hạ được đâu nhỉ?

# speaker:princess
# events:whistle
# pace:50
Gì thế, cái gì trên kia vậy?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Đó không phải hình nộm tập luyện bình thường.

# speaker:princess
# pace:30
Trông như một món đồ chơi phép thuật. Dành cho thứ gì đó lớn hơn chúng ta nhiều.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Ê, anh kia...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Tôi tìm được mấy chìa khóa của hầm ngục bí mật dưới lâu đài.

# speaker:rogue
# pace:30
# wait:500
Không biết nhà vua có biết nó tồn tại không nữa.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Mà thôi kệ...

# speaker:rogue
# pace:30
Mấy chuyến vừa rồi tôi vơ được kha khá, nhưng lần cuối đuốc suýt tắt.

# speaker:rogue
# wait:500
Tôi sợ vào lại rồi lạc trong bóng tối, nên tặng anh hết chỗ chìa khóa này, miễn phí.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Chúc may mắn,

# speaker:rogue
# pace:100
# events:end_give_keys
và nhớ cẩn thận.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Ê! Tôi là người làm ra game này.

# pace:40
Xin lỗi vì bạn lọt qua tường. Đó là lỗi của tôi.

# pace:30
Tôi sẽ đưa bạn ra khỏi khoảng trống, và toàn bộ chiến lợi phẩm vẫn còn nguyên.

* [Bỏ cuộc và giữ chiến lợi phẩm]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Tạm biệt!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Chào anh hùng!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Để trợ giúp trận chiến, Bệ hạ đã lệnh cho Hội Kiến trúc sư và Kỹ sư Hoàng gia đem chuyên môn của chúng tôi ra giúp.

# speaker:engineer
# pace:30
Chúng tôi sẽ giúp bạn theo ba cách:

# speaker:engineer
# pace:30
- Chế tạo máy bắn đá để công thành.

# speaker:engineer
# pace:30
- Dựng công trình bậc hai, qua tay các thợ xây của chúng tôi.

# speaker:engineer
# pace:30
- Lập các tổ chức bậc cao hơn, qua tay các kỹ sư của chúng tôi.

# speaker:engineer
# pace:30
Khi có đủ vàng, hãy tìm chúng tôi ở thẻ "Kỹ thuật".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Ồ, thế ngươi tưởng "sa thải quân" nghĩa là gì?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Giết ta còn chưa đủ sao? Xin hãy thôi quấy rầy ta!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Chíp chíp, đồ kh**!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Tôi đã sẵn sàng tấu nhạc cho quân của bạn và khơi dậy sức mạnh của họ.

# speaker:bard_dialog
# pace:35
# wait:400
Hãy nhấn nút cây đàn hạc và tận hưởng sức mạnh tăng tạm thời!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Cứu với!

# speaker:king
# chain_next
# pace:30
# wait:500
Một con rồng khổng lồ đang phá làng của chúng ta!

# speaker:king
# wait:300
# pace:30
- Chúng ta cần một anh hùng đến cứu.

# speaker:king
# pace:30
- Xin hãy giết con rồng này bằng thanh kiếm hùng mạnh, à không, bằng con trỏ chuột của ngươi.

# speaker:king
# pace:30
- Và nếu đủ vàng, ngươi còn có thể chiêu mộ thêm người giúp sức.

# speaker:king
# pace:30
- Chúc may mắn!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Bằng cách nào đó, Forth'aarh đã trở lại!

# speaker:king
# pace:30
# wait:400
Nhưng ngươi đã giải tán quân rồi. Giờ phải chiêu mộ lại từ đầu.

# speaker:king
# wait:300
# pace:30
- Và trận tấn công lần trước đã phá nát ngân khố, nên ta không nuôi nổi quân của ngươi.

# speaker:king
# pace:40
# chain_next
- Từ nay họ sẽ tiêu thụ

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- lương thực, gỗ và quặng.

# speaker:king
# pace:40
- Ngươi sẽ phải liệu tài nguyên cho khéo.

# speaker:king
# pace:40
- Hãy bật tắt xem đơn vị nào đang được dùng tài nguyên, đơn vị nào không.

# speaker:king
# pace:40
- Hoặc "sa thải" bớt: họ tiêu ít đi mà vẫn làm được chút việc.

# speaker:king
# pace:28
- Chúc may mắn!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Tiếc thay, quân ta không đủ để đẩy lui cuộc xâm lược.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Ta mất sạch quân, và mất luôn cả khoản tiền chuộc.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Quân ta trở về với tin mừng!

# speaker:king
# pace:30
Họ đã đẩy lui cuộc xâm lược với thiệt hại tối thiểu.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Ta đón họ trở về (để lại tiếp tục cày con rồng...)

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
Vương quốc láng giềng đang tấn công chúng ta.

# speaker:king
# pace:30
Họ đòi {ransomCostLabel} đồng vàng để dừng cuộc xâm lược.

# speaker:king
# chain_next
# pace:30
# wait:500
Ngươi nghĩ chúng ta nên làm gì?

* [Trả {ransomCostLabel} đồng vàng]
    -> pay_enemy

* { unitsCountFew > 3 } [Phòng thủ với {unitsCountFew} quân]
    -> send_few_units

* { unitsCountMany > 3 } [Phòng thủ với {unitsCountMany} quân]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Mong là họ chấp nhận đề nghị của ta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Mong là chừng đó là đủ.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Chừng này chắc chắn đẩy lui được đòn của họ.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Ít nhất... ta đã không chết trong nghèo khó.

# speaker:king
# pace:60
# classes:victory
Dù sao cũng chúc mừng ngươi đã phá đảo trò chơi.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
BẠN ĐÃ GIẾT CHA TÔI!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Không...

# speaker:developer
# pace:100
# classes:vader
Ta là cha ngươi!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Người làm game à?

# speaker:princess
# pace:50
Anh nhét hai câu Star Wars vào game của mình luôn à? Thật sao?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Ngươi tìm ra ta rồi.

# speaker:king
# pace:32
Đúng, ta lấy nó từ hang rồng. Vàng cho vương quốc. Món đồ chơi làm kỷ niệm.

# speaker:king
# pace:30
Dân ta đang đói. Ta sẽ làm lại lần nữa.

# speaker:king
# pace:30
Nhận chút hối lộ rồi im lặng, cả hai ta đều yên chuyện.

# speaker:king
# pace:30
Ngươi phản ta, hay nhận món quà của ta?

* [Phải có ai ngăn ngài lại!]
  -> go_against_king

* [Ta cũng thích vàng lắm!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Vậy thì được!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Thế thì nhận phần của ngươi đi.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Ta đã cho ngươi nhiều vàng hơn cả những gì ngươi từng mơ.

# speaker:king
# pace:30
Đó là thỏa thuận. Cầm lấy rồi đi đi.

* [Mặc kệ, phải ngăn ngài lại]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Vậy thì được!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Ngươi dùng vàng của ta mua đội quân đã giết con nó.

# speaker:king
# pace:32
Đừng giả vờ vô tội.

# speaker:king
# pace:30
Vậy thì lại đây.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Vậy là anh mắc nợ vương quốc hả? Yên tâm... hội có cả đống con nợ.


# speaker:rogue
# pace:40
# wait:400
Không trả thì gãy vài cái chân.

# speaker:rogue
# pace:30
# wait:400
Tới khi nào anh về lại số dương, đám đạo tặc của tôi sẽ gom vàng cho anh gấp đôi.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Than ôi! Kho mana của chúng tôi đã cạn.

# speaker:wizard_dialog
# pace:35
# wait:400
Không có tinh chất huyền bí, tôi không thể dồn phép lên con rồng.

# speaker:wizard_dialog
# pace:35
# wait:400
Hãy vào bảng nâng cấp và mua "Hồi mana" mỗi khi chúng tôi cạn... để lại giáng đòn lên con quái đó!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Có ai thấy nhà vua không? Cha tôi mất tích rồi.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Lần cuối người ta thấy, cha đang đi xuống hầm ngục dưới lâu đài.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Chào mừng!

# pace:45
Tôi là Mook, trẻ tuổi và công chính!

# pace:50
Nhà vua đặt tôi ở đây để bạn không lạc đường, và tôi nói thật đấy: tôi thích chỉ đường lắm.

# pace:35
Tôi không được rời khỏi ô này. "Giúp mọi lữ khách", rồi "đừng bước qua vạch đó". Tôi tự nhủ đó là quy định. Dạo này... tôi không còn chắc nữa.

# pace:25
Nhưng này, cầm lấy ngọn đuốc này. Đó là thứ giúp đỡ duy nhất tôi còn được đưa qua vạch.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Chào con, ta là Giáo hoàng.

# speaker:pope
# pace:30
- Đã đến lúc con chứng tỏ đức tin một lần nữa và dâng góp cho Giáo hội.

# speaker:pope
# pace:30
- Ta cần {contributionCostLabel} đồng vàng để giúp người nghèo.

* [Đưa ngài {contributionCostLabel} đồng vàng]
    -> pay_contribution

* [Đổi sang tôn giáo khác]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Nguyện linh hồn con được ban thưởng ở đời sau!

# speaker:pope
# pace:30
- Hãy nhận 100 tư tế này như lời cảm tạ của Giáo hội.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Nguyện linh hồn con bị nguyền rủa ở đời sau!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Với lại...

# speaker:pope
# pace:30
- Sẽ tiếc lắm nếu con thằn lằn khổng lồ kia được một quyền năng cao hơn chữa lành...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(tiếng chữa lành\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Tôi có lương thực, gỗ hoặc quặng để bán, giá

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
vàng. Bạn muốn lấy thứ nào?

* { canAffordTrading > 0 } [Lương thực: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Gỗ: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Quặng: {resourceAmountLabel}]
    -> buy_ore

* [Không lấy gì]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Cảm ơn, hẹn gặp lại chuyến sau.

  -> END


=== farewell ===

# speaker:salesman
Hẹn gặp lại chuyến sau.

* [Tạm biệt]
    -> END

* [Ghé thưa thớt lại]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Hiểu rồi. Tôi sẽ ghé thưa hơn.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Chà, bạn làm được thật rồi!

# speaker:king
# pace:30
- Cảm tạ ngươi đã giết con rồng đó. Ngươi là anh hùng của chúng ta!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Cuối cùng thì chúng ta cũng...

# speaker:princess
# classes:scared
# pace:200
Tiếng gì vậy?

# speaker:shadow
# pace:200
# classes:angry
CÁC NGƯƠI ĐÃ GIẾT CON TA!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Đó

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
MỚI

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
là rồng lớn!

# speaker:princess
# pace:20
# events:resume_game
Ôi không, bạn sẽ giúp chúng tôi chứ?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh đã chết. Bạn làm được điều không đội quân nào làm nổi.

# speaker:king
# pace:28
# classes:victory
Cảm tạ ngươi. Thật lòng.

# speaker:princess
# pace:30
# classes:victory
Đi theo tôi... Chúng ta phải chuẩn bị cho những kẻ thù mới có thể xuất hiện.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Sao nó quay lại được nhỉ?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Ta không biết nó trở lại bằng cách nào.

# speaker:king
# pace:28
- Nhưng đứng dậy được như thế thì phải có ý chí phi thường.

# speaker:princess
# pace:40
# classes:scared
- Và cả lòng khao khát báo thù nữa...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Bạn có biết mỗi lần bạn vào hầm ngục

# classes:angry-worker
# pace:30
- LÀ TÔI PHẢI DỰNG NGUYÊN MỘT MÊ CUNG MỚI BẰNG TAY KHÔNG?!?

# chain_next
# pace:50
- Chúng tôi khiêng rương lên suốt mấy tuần. Ông ấy bảo đừng hỏi chúng từ đâu ra.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Cuối cùng cũng xong!

# pace:40
- Nhà vua bảo tôi làm xong rồi, trả cuốc lại cho ngài sau khi tôi hoàn tất tầng này.

  -> END
"""

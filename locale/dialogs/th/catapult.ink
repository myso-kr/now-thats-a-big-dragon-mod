VAR choosesRock = false
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

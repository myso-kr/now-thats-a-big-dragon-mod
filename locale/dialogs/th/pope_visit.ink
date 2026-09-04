VAR contributionCostLabel = "1"

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

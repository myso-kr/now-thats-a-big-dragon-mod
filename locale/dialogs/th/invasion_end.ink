VAR strategyChoice = ""

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

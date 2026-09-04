# speaker:king
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

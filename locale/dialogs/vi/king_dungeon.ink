# speaker:king
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

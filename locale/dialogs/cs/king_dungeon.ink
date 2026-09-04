# speaker:king
# pace:40
Našel jsi mě.

# speaker:king
# pace:32
Ano, vzal jsem to z dračího doupěte. Zlato pro království. Hračku na památku.

# speaker:king
# pace:30
Náš lid hladověl. Udělal bych to znovu.

# speaker:king
# pace:30
Vezmi si úplatek a mlč, a oba z toho vyjdeme čistí.

# speaker:king
# pace:30
Zradíš mě, nebo přijmeš můj dar?

* [Někdo tě musí zastavit!]
  -> go_against_king

* [Zlato mám rád!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Budiž!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Tak si vezmi svůj podíl.

  -> END

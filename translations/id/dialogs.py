# -*- coding: utf-8 -*-
"""Writes the Indonesian .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "kamu" throughout. "Anda" would put the King at the distance of a bank letter,
and "engkau" reads as scripture; neither is how this game speaks. The King is grand in
tone rather than in pronoun.

The game's font has no curly quotes or em dash, so straight quotes and hyphens.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Sepertinya kamu butuh bantuan untuk menghasilkan lebih banyak sumber daya...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Coba beli Magang untuk menambah petani, penambang, dan penebang kayu.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ketemu lagi!

# speaker:engineer
Kami sudah meneruskan penelitian senjata pengepungmu.

# speaker:engineer
# wait:300
# pace:30
Sekarang ia bisa melontarkan kucing ke musuh, dan kami yakin itu akan membalik pertempuran.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Kami menyebutnya "Katapel Kucing"

# speaker:engineer
# wait:300
# pace:300
(jeda demi kesan)

# speaker:engineer
# pace:30
Mau membiayai peningkatannya, untuk yang ini dan semua yang berikutnya?

* [Aku lebih suka melontar batu]
    -> no_thanks

* [Bayar {catapultCostLabel} emas]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Beri tahu kami pendapatmu, ya!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Beri tahu kami pendapatmu, ya!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Sayang sekali. Semoga berhasil.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Pasukanmu menyisakan pukulan terakhir untukmu.

# speaker:king
# pace:30
- Inilah kesempatanmu untuk mengakhirinya selamanya!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Ayah bilang kamu harus terus berlatih, kalau-kalau ada yang lebih besar datang.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Kali ini ia bahkan membayari pasukanmu, jadi kamu boleh menyusunnya sesukamu.

# speaker:princess
# pace:40
# chain_next
# wait:500
Padahal beberapa bulan lalu, waktu aku minta pesta ulang tahun yang besar,

# speaker:princess
# pace:40
# chain_next
# wait:500
yang kudengar cuma...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, kerajaan tidak punya uang, Nak!"


# speaker:princess
# pace:37
Ngomong-ngomong, boneka kayu itu kelihatan aneh...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Apa? Aku bahkan tidak menyangka itu bisa dijatuhkan.

# speaker:princess
# pace:20
# classes:love
Tapi memangnya ada yang tidak bisa dilakukan pahlawanku?

# speaker:princess
# events:whistle
# pace:50
Apa itu di atas sana?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Itu bukan boneka latihan biasa.

# speaker:princess
# pace:30
Kelihatannya seperti mainan bersihir. Dibuat untuk sesuatu yang jauh lebih besar dari kita.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Hei, kamu...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Aku menemukan beberapa kunci ruang bawah tanah rahasia di bawah istana.

# speaker:rogue
# pace:30
# wait:500
Aku bahkan tidak yakin raja tahu tempat itu ada.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Ah, sudahlah...

# speaker:rogue
# pace:30
Aku sudah membawa banyak dari sana, tapi terakhir kali oborku hampir padam.

# speaker:rogue
# wait:500
Aku tidak berani turun lagi dan tersesat dalam gelap, jadi kunci-kunci ini untukmu. Gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Semoga berhasil,

# speaker:rogue
# pace:100
# events:end_give_keys
dan hati-hati.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Hai! Aku yang membuat gim ini.

# pace:40
Maaf kamu tembus dinding. Itu salahku.

# pace:30
Aku akan mengeluarkanmu dari ruang kosong, dan seluruh jarahanmu tetap utuh.

* [Menyerah dan bawa jarahannya]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Sampai jumpa!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Salam, Pahlawan!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Untuk membantu pertempuran, Baginda memerintahkan Serikat Arsitek dan Insinyur Kerajaan agar menyerahkan keahlian kami kepadamu.

# speaker:engineer
# pace:30
Kami membantumu dengan tiga cara:

# speaker:engineer
# pace:30
- Kami membuat katapel untuk pengepungan.

# speaker:engineer
# pace:30
- Kami mendirikan bangunan tingkat dua, lewat para tukang kami.

# speaker:engineer
# pace:30
- Kami mendirikan organisasi tingkat lebih tinggi, lewat para insinyur kami.

# speaker:engineer
# pace:30
Cari kami di tab "Teknik" begitu emasmu cukup.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Lho, kamu kira "berhentikan pasukan" itu artinya apa?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Membunuhku saja belum cukup? Sudahlah, jangan ganggu aku!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Cuit cuit, dasar b*******n!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Aku siap memainkan lagu untuk pasukanmu dan membangkitkan kekuatan mereka.

# speaker:bard_dialog
# pace:35
# wait:400
Tekan tombol harpa dan nikmati kekuatan tambahan untuk sesaat!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Tolong!

# speaker:king
# chain_next
# pace:30
# wait:500
Naga raksasa menghancurkan desa kami!

# speaker:king
# wait:300
# pace:30
- Kami butuh pahlawan yang menyelamatkan kami.

# speaker:king
# pace:30
- Tolong bunuh naga itu dengan pedangmu yang perkasa, eh, maksudku dengan kursor tetikusmu.

# speaker:king
# pace:30
- Dan kalau emasmu cukup, kamu bisa merekrut orang lain untuk membantu.

# speaker:king
# pace:30
- Semoga berhasil!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Entah bagaimana, Forth'aarh kembali!

# speaker:king
# pace:30
# wait:400
Tapi kamu sudah membubarkan pasukanmu. Sekarang kamu harus merekrut lagi dari awal.

# speaker:king
# wait:300
# pace:30
- Dan serangan lalu menghancurkan perbendaharaan, jadi aku tak sanggup menghidupi pasukanmu.

# speaker:king
# pace:40
# chain_next
- Mulai sekarang mereka memakan

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- pangan, kayu, dan bijih.

# speaker:king
# pace:40
- Kamu harus berhemat dengan sumber daya.

# speaker:king
# pace:40
- Nyalakan dan matikan siapa yang dapat sumber daya dan siapa yang tidak.

# speaker:king
# pace:40
- Atau "berhentikan" sebagian: mereka memakai lebih sedikit tapi tetap berguna.

# speaker:king
# pace:28
- Semoga berhasil!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Sayangnya pasukan kita tidak cukup untuk menahan serbuan itu.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Aku kehilangan seluruh pasukan, dan uang tebusannya juga.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Pasukan kita kembali dengan kabar baik!

# speaker:king
# pace:30
Mereka menahan serbuan itu dengan korban yang sedikit.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Aku menyambut mereka (agar bisa kembali menghadapi naga...)

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
Kerajaan tetangga menyerang kita.

# speaker:king
# pace:30
Mereka menuntut {ransomCostLabel} emas untuk menghentikan serbuan.

# speaker:king
# chain_next
# pace:30
# wait:500
Menurutmu apa yang harus kita lakukan?

* [Bayar {ransomCostLabel} emas]
    -> pay_enemy

* { unitsCountFew > 3 } [Bertahan dengan {unitsCountFew} pasukan]
    -> send_few_units

* { unitsCountMany > 3 } [Bertahan dengan {unitsCountMany} pasukan]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Semoga mereka menerima tawaran itu.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Semoga itu cukup.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Sebanyak itu pasti menahan mereka.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Setidaknya... aku tidak mati miskin.

# speaker:king
# pace:60
# classes:victory
Ngomong-ngomong, selamat sudah menamatkan gimnya.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
KAMU MEMBUNUH AYAHKU!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Tidak...

# speaker:developer
# pace:100
# classes:vader
Akulah ayahmu!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Kamu yang bikin gim ini?

# speaker:princess
# pace:50
Kamu menaruh dua kalimat Star Wars di gimmu sendiri? Serius?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Jadi kamu menemukanku.

# speaker:king
# pace:32
Ya, aku mengambilnya dari sarang naga. Emasnya untuk kerajaan. Mainannya sebagai kenang-kenangan.

# speaker:king
# pace:30
Rakyatku kelaparan. Aku akan melakukannya lagi.

# speaker:king
# pace:30
Terima suap dan diamlah, biar kita berdua tidak repot.

# speaker:king
# pace:30
Kamu mengkhianatiku, atau menerima pemberianku?

* [Seseorang harus menghentikanmu!]
  -> go_against_king

* [Aku juga suka emas!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Kalau begitu, baiklah!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Ambil bagianmu kalau begitu.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Aku sudah memberimu lebih banyak emas daripada yang pernah kamu impikan.

# speaker:king
# pace:30
Itu kesepakatannya. Ambil dan pergilah.

* [Tidak peduli, kamu harus dihentikan]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Kalau begitu, baiklah!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Kamu memakai emasku untuk membeli pasukan yang membunuh anaknya.

# speaker:king
# pace:32
Jangan pura-pura tidak bersalah.

# speaker:king
# pace:30
Kalau begitu, majulah.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Jadi kamu berutang pada kerajaan? Tenang... serikat ini penuh dengan pengutang.


# speaker:rogue
# pace:40
# wait:400
Kalau tidak dibayar, ada kaki yang patah.

# speaker:rogue
# pace:30
# wait:400
Sampai kamu keluar dari minus, para pencuriku mengumpulkan emas dua kali lipat untukmu.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Aduh! Persediaan mana kami habis.

# speaker:wizard_dialog
# pace:35
# wait:400
Tanpa tenaga gaib itu, aku tidak bisa melemparkan apa pun ke naga.

# speaker:wizard_dialog
# pace:35
# wait:400
Buka daftar peningkatan dan beli "Aliran Mana" setiap kali kami kehabisan... biar kita hantam lagi monster itu!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Ada yang melihat raja? Ayahku hilang.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Terakhir ia terlihat menuruni tangga ke ruang bawah tanah di bawah istana.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Selamat datang!

# pace:45
Aku Mook, muda dan lurus hati!

# pace:50
Raja menempatkanku di sini supaya kamu tidak tersesat, dan aku bilang apa adanya: aku suka menunjukkan jalan.

# pace:35
Aku tidak boleh meninggalkan petak ini. "Bantu semua yang lewat", lalu "jangan lewati garis itu". Aku bilang pada diriku itu aturannya. Belakangan ini... aku sendiri tidak begitu yakin.

# pace:25
Tapi ini, ambil obor ini. Cuma itu yang boleh kuberikan melewati garis.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Salam, anakku. Akulah Sri Paus.

# speaker:pope
# pace:30
- Sudah waktunya menunjukkan imanmu lagi dan memberi persembahan kepada Gereja.

# speaker:pope
# pace:30
- Aku butuh {contributionCostLabel} emas untuk menolong kaum miskin.

* [Beri dia {contributionCostLabel} emas]
    -> pay_contribution

* [Pindah agama]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Semoga jiwamu diganjar di akhirat!

# speaker:pope
# pace:30
- Terimalah 100 rohaniwan ini sebagai tanda terima kasih Gereja.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Semoga jiwamu terkutuk di akhirat!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Lagi pula...

# speaker:pope
# pace:30
- Sayang sekali kalau kadal raksasa itu disembuhkan oleh kuasa yang lebih tinggi...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(bunyi penyembuhan\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Aku menjual pangan, kayu, atau bijih seharga

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
emas. Kamu mau yang mana?

* { canAffordTrading > 0 } [Pangan: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Kayu: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Bijih: {resourceAmountLabel}]
    -> buy_ore

* [Tidak usah, terima kasih]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Terima kasih, sampai jumpa lain kali.

  -> END


=== farewell ===

# speaker:salesman
Sampai jumpa lain kali.

* [Selamat tinggal]
    -> END

* [Datanglah lebih jarang]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Mengerti. Aku akan lebih jarang datang.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Kamu benar-benar melakukannya!

# speaker:king
# pace:30
- Terima kasih sudah membunuh naga itu. Kamu pahlawan kami!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Akhirnya kita bisa...

# speaker:princess
# classes:scared
# pace:200
Suara apa itu?

# speaker:shadow
# pace:200
# classes:angry
KALIAN MEMBUNUH ANAKKU!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
NAH

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ITU BARU

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
naga besar!

# speaker:princess
# pace:20
# events:resume_game
Aduh, kamu mau menolong kami, kan?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh sudah mati. Kamu melakukan apa yang tak bisa dilakukan pasukan mana pun.

# speaker:king
# pace:28
# classes:victory
Terima kasih. Sungguh.

# speaker:princess
# pace:30
# classes:victory
Ikut aku... Kita harus bersiap menghadapi musuh yang mungkin datang berikutnya.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Bagaimana bisa ia kembali?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Aku tidak tahu bagaimana ia kembali.

# speaker:king
# pace:28
- Tapi bangkit lagi seperti itu butuh kehendak yang luar biasa.

# speaker:princess
# pace:40
# classes:scared
- Dan haus akan balas dendam...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Kamu tahu tidak, setiap kali kamu turun ke ruang bawah tanah

# classes:angry-worker
# pace:30
- AKU HARUS MEMBANGUN LABIRIN BARU DENGAN TANGAN?!?

# chain_next
# pace:50
- Kami sudah berminggu-minggu mengangkut peti. Katanya jangan tanya dari mana asalnya.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Akhirnya selesai!

# pace:40
- Raja bilang tugasku sudah selesai dan cangkulnya boleh kukembalikan setelah tingkat ini beres.

  -> END
"""

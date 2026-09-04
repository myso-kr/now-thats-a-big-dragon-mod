# -*- coding: utf-8 -*-
"""The Indonesian UI strings.

Address: "kamu" throughout, which is what games use. "Anda" would put the King at the
distance of a bank letter, and "engkau" reads as scripture.

Indonesian marks no number on the noun, so a counted noun is written once and the
language has a single plural category - a count of one and a count of many read the
same. Where English doubles a word for the plural, Indonesian would only do so to mean
"various kinds", which is not what a troop count means.

The game's own fonts draw every letter Indonesian needs, so nothing of ours ships.
"""

T = {}

T.update({
    "upgrades.upgrades": "Peningkatan",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Tingkat berikutnya",
    "upgrades.currentLevel": "Saat ini",
    "upgrades.newGamePlusOnly": "Hanya di bab \"Pengelolaan Sumber Daya\"",
    "upgrades.max": "Maks",
    "upgrades.lockedMessage": "Tingkatkan {{parentSkill}} lagi untuk membuka yang ini",
    "common.wishlistNow": "Tambahkan ke daftar keinginan!",
})

T.update({
    "statistics.section.ttb": "Waktu bertempur",
    "statistics.section.dgps": "Kerusakan dan emas per detik",
    "statistics.section.resourceBalance": "Neraca sumber daya",
    "statistics.lifetime.title": "Statistik total",
    "statistics.lifetime.totalPlaytime": "Total waktu bermain",
    "statistics.lifetime.totalGoldEarned": "Total emas didapat",
    "statistics.lifetime.totalGoldSpent": "Total emas dipakai",
    "statistics.lifetime.totalBirdsKilled": "Total burung dijatuhkan",
    "statistics.lifetime.totalClicks": "Total klik",
    "statistics.lifetime.totalHeroesRecruited": "Total pahlawan direkrut",
    "statistics.lifetime.heroesPurchased": "Dibeli",
    "statistics.lifetime.heroesRecruited": "Direkrut",
    "statistics.lifetime.tier1": "Tingkat 1 direkrut (dibeli)",
    "statistics.lifetime.tier2": "Tingkat 2 direkrut (dibeli)",
    "statistics.lifetime.tier3": "Tingkat 3 direkrut (dibeli)",
    "statistics.lifetime.totalDamageDealt": "Total kerusakan diberikan",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Hilang karena semburan api",
    "statistics.battleDuration": "Berjalan: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Apa ini bisa dimenangkan?",
    "statistics.infiniteEstimatedVictory": "Menang sungguhan itu mustahil!",
    "statistics.estimatedVictory": "(0)[<strong class='text-danger'>Kamu pahlawan kami!</strong>];"
        " (0-1000000000)[Menang dalam <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Klik atau tekan Z untuk menyerang naganya!</strong>]",
    "statistics.perSec": "/dtk",
    "statistics.generationSection": "Produksi",
    "statistics.critSection": "Khusus",
    "statistics.dps": "Kerusakan pasukan: <strong>{{dps}}/dtk</strong>",
    "statistics.gps": "Emas pasukan: <strong>{{gps}}/dtk</strong>",
    "statistics.dpc": "Kerusakan per klik: <strong>{{dpc}}/klik</strong>",
    "statistics.gpc": "Emas per klik: <strong>{{gpc}}/klik</strong>",
    "statistics.catapultDamage": "Kerusakan: <strong>{{damage}}/tembakan</strong>",
    "statistics.catapultTimeToShoot": "Menuju tembakan berikutnya: <strong>{{time}} dtk</strong>",
    "statistics.undo.disabledLine": "Klik dalam 10 detik untuk membatalkan pembelian yang salah"
        " dan mendapatkan emasmu kembali.",
    "statistics.undo.enabledAction": "Klik untuk membatalkan pembelian {{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Kamu akan menerima {{refund}}.",
    "statistics.undo.enabledTimer": "Sisa {{seconds}} detik.",
    "statistics.undo.refundGold": "{{amount}} emas",
})

# Indonesian marks no number on the noun, so both forms are the same word. The
# language itself uses one plural category, but the game's own keys carry `_one` as
# well, and a key left unfilled falls back to English.
for base, word in [
    ("seconds", "detik"), ("minutes", "menit"), ("hours", "jam"),
    ("days", "hari"), ("months", "bulan"), ("years", "tahun"),
]:
    T[f"statistics.{base}_one"] = word
    T[f"statistics.{base}_other"] = word

T.update({
    "generators.generators": "Pasukan",
    "generators.buy": "beli {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}} dtk",
    "generators.ngPlusProductionToggle": "Nyalakan atau matikan produksi",
    "generators.tabs.troops": "Pasukan",
    "generators.tabs.support": "Pendukung",
    "generators.fireUnitsButton.tooltip": "Berhentikan pasukan agar sumber daya lebih hemat"
        " tetapi sebagian produksi tetap jalan.",
    "generators.ownedUnits": "{{unit}}: {{amount}}",
    "generators.mana": "Mana",
    "generators.manaDescription": "Tenaga sihir di balik serangan para penyihir.",
    "generators.emptyManaDescription": "Beli \"Aliran Mana\" untuk menyerang lagi.",
    "generators.inspiration": "Inspirasi",
    "generators.inspirationDescription": "Saat aktif, kekuatan semua pahlawan dilipatgandakan.",
    "generators.tabsAriaLabel": "tab pasukan",
})

UNITS = {
    "warrior": "Prajurit", "wizard": "Penyihir", "elf": "Elf",
    "garrison": "Garnisun", "academy": "Akademi Sihir", "academy_short": "Akademi",
    "outpost": "Pos Pemanah", "outpost_short": "Pos",
    "council": "Dewan Perang", "nexus": "Pusat Arkimagus", "forest": "Hutan Purba",
    "thief": "Pencuri", "bard": "Pujangga", "cleric": "Rohaniwan",
    "guild": "Serikat Pencuri", "guild_short": "Serikat",
    "troupe": "Rombongan Penghibur", "troupe_short": "Rombongan",
    "seminary": "Seminari Suci", "seminary_short": "Seminari",
    "congress": "Sidang Bayangan", "theater": "Teater Besar", "college": "Kolese Kardinal",
    "catapult": "Katapel", "builder": "Tukang Bangunan", "engineer": "Insinyur",
    "farmer": "Petani", "lumberjack": "Penebang Kayu", "miner": "Penambang",
    "apprenticeships": "Magang", "tradespeople": "Pengrajin",
}
for base, word in UNITS.items():
    T[f"generators.{base}_one"] = word
    T[f"generators.{base}_other"] = word

T.update({
    "generators.unitDescription.warrior": "Petarung jarak dekat yang tangguh.",
    "generators.unitDescription.wizard": "Menyerang dari jarak sedang, tetapi rapuh.",
    "generators.unitDescription.elf": "Memanah lincah dari jauh, di luar jangkauan naga.",
    "generators.unitDescription.garrison": "Markas berbenteng yang merekrut prajurit.",
    "generators.unitDescription.outpost": "Markas terpencil yang merekrut elf.",
    "generators.unitDescription.academy": "Sekolah yang melatih penyihir untuk bertempur.",
    "generators.unitDescription.council": "Organisasi militer yang mendirikan garnisun.",
    "generators.unitDescription.nexus": "Organisasi mistis yang mendirikan akademi.",
    "generators.unitDescription.forest": "Hutan suci yang mendirikan pos.",
    "generators.unitDescription.thief": "Licik: meracuni naga dan mencuri emasnya.",
    "generators.unitDescription.bard": "Bisa mengobarkan semangat pasukanmu.",
    "generators.unitDescription.cleric": "Melindungi dan merekrut pahlawan baru ke medan perang.",
    "generators.unitDescription.guild": "Jaringan bawah tanah yang merekrut pencuri.",
    "generators.unitDescription.troupe": "Rombongan keliling yang merekrut pujangga.",
    "generators.unitDescription.seminary": "Lembaga suci yang mendidik rohaniwan.",
    "generators.unitDescription.congress": "Organisasi dalam bayangan yang mendirikan serikat pencuri.",
    "generators.unitDescription.theater": "Lembaga megah yang mendirikan rombongan penghibur.",
    "generators.unitDescription.college": "Organisasi keagamaan yang mendirikan seminari.",
    "generators.unitDescription.catapult": "Senjata pengepung yang melukai naga dengan hebat.",
    "generators.unitDescription.builder": "Membangun bangunan tingkat dua.",
    "generators.unitDescription.engineer": "Mendirikan organisasi tingkat tiga.",
    "generators.unitDescription.farmer": "Menanam pangan untuk kerajaan.",
    "generators.unitDescription.lumberjack": "Menebang kayu untuk membangun.",
    "generators.unitDescription.miner": "Menambang bijih di pegunungan.",
    "generators.unitDescription.apprenticeships": "Melatih pengrajin.",
})

GEN_PLAIN = {
    "warrior": "{{generatorGeneration}} kerusakan/{{rate}} dtk",
    "wizard": "{{generatorGeneration}} kerusakan/{{rate}} dtk",
    "elf": "{{generatorGeneration}} kerusakan/{{rate}} dtk",
    "catapult": "{{generatorGeneration}} kerusakan/{{rate}} dtk",
    "thief": "+{{generatorGeneration}} emas/{{rate}} dtk",
    "bard": "+{{generatorGeneration}} inspirasi/{{rate}} dtk",
    "cleric": "+{{generatorGeneration}} pahlawan/{{rate}} dtk",
    "builder": "+{{generatorGeneration}} bangunan/{{rate}} dtk",
    "engineer": "+{{generatorGeneration}} organisasi/{{rate}} dtk",
    "farmer": "+{{generatorGeneration}} pangan/{{rate}} dtk",
    "lumberjack": "+{{generatorGeneration}} kayu/{{rate}} dtk",
    "miner": "+{{generatorGeneration}} bijih/{{rate}} dtk",
}
for k, v in GEN_PLAIN.items():
    T[f"generators.generationDescription.{k}"] = v

GEN_NESTED = {
    "garrison": "warrior", "outpost": "elf", "academy": "wizard", "council": "garrison",
    "nexus": "academy_short", "forest": "outpost_short", "guild": "thief",
    "troupe": "bard", "seminary": "cleric", "theater": "troupe_short",
    "college": "seminary_short", "congress": "guild_short",
    "apprenticeships": "tradespeople",
}
for k, ref in GEN_NESTED.items():
    T[f"generators.generationDescription.{k}"] = (
        "+{{generatorGeneration}} $t(" + ref + ', {"count": {{generatorGeneration}} })/{{rate}} dtk')

T.update({
    "settings.settings": "Pengaturan",
    "settings.buy_max": "Beli maks",
    "settings.audio": "Musik dan suara",
    "settings.game": "Permainan",
    "settings.graphics": "Grafik",
    "settings.offline_progress": "Kemajuan saat offline",
    "settings.wishlist_now": "Tambahkan ke daftar keinginan",
    "menus.settings": "Pengaturan",
    "menus.tabs.game": "Permainan",
    "menus.tabs.graphics": "Grafik",
    "menus.tabs.audio": "Suara",
    "menus.tabs.levels": "Bab",
    "menus.tabs.credits": "Kredit",
    "menus.credits.title": "Kredit",
    "menus.credits.developedBy": "Dikembangkan oleh",
    "menus.credits.developedWith": "Dikembangkan dengan",
    "menus.credits.bigThanksTo": "Terima kasih besar kepada",
    "menus.credits.theRestOfTheDiscordServer": "semua orang lain di server Discord",
    "menus.credits.andYou": "dan kamu!",
    "menus.music": "Musik",
    "menus.sfx": "Efek suara",
    "menus.audioSettings": "Pengaturan suara",
    "menus.gameSettings": "Pengaturan permainan",
    "menus.graphicsSettings": "Pengaturan grafik",
    "menus.language": "Bahasa",
    "menus.languages.en": "Inggris",
    "menus.languages.fr": "Prancis",
    "menus.languages.de": "Jerman",
    "menus.languages.pt": "Portugis",
    "menus.languages.tr": "Turki",
    "menus.shakeIntensity": "Getaran",
    "menus.largerTextSize": "Teks lebih besar",
    "menus.crtFilter": "Filter CRT",
    "menus.chromaticAberrationSlider": "Aberasi warna",
    "menus.chromaticAberration": "Aberasi warna",
    "menus.swordSwooshSounds": "Suara pedang dan kritis",
    "menus.catSounds": "Suara kucing",
    "menus.fullscreen": "Layar penuh",
    "menus.resume": "Lanjut bermain",
    "menus.close": "Tutup",
    "menus.quitGame": "Keluar dari permainan",
    "menus.joinDiscord": "Gabung Discord",
    "menus.clear_save_label": "Hapus kemajuanmu?",
    "menus.zoom_adjustment": "Perbesaran antarmuka",
    "menus.clear_save": "Hapus sekarang",
    "menus.are_you_sure": "Kamu yakin?",
    "menus.cannot_be_reversed": "Ini tidak bisa dibatalkan.",
    "menus.yes": "Ya",
    "menus.no": "Tidak",
})

T.update({
    "tooltip.inspiration": "Inspirasi",
    "tooltip.inspirationDescription": "Saat aktif, kekuatan semua pahlawan dilipatgandakan.",
    "tooltip.maxInspiration": "Pengali tertinggi",
    "tooltip.maxInspirationMultiplier": "Pengali tertinggi",
    "tooltip.statisticsDescription": "Angka rinci tentang kemajuanmu dan jalannya pertempuran.",
    "tooltip.hudStopBird": "Hentikan burung",
    "tooltip.hudLifetimeStats": "Statistik total",
    "tooltip.hudHideWindows": "Sembunyikan jendela",
    "tooltip.events.roar": "Raungan yang membuat pingsan",
    "tooltip.events.fire": "Semburan api",
    "tooltip.events.claw": "Sabetan cakar",
    "tooltip.events.dialog": "Kejadian khusus",
    "tooltip.events.pope_visit": "Tamu istimewa",
    "tooltip.events.dungeon_keys": "Rahasia yang kelam",
    "tooltip.events.missing_king": "Di mana rajanya?",
    "tooltip.events.catapult": "Purwarupa teknik",
    "tooltip.events.engineer": "Bantuan yang tepat waktu",
    "tooltip.events.invasion_start": "Serbuan sedang mendekat",
    "tooltip.events.invasion_end": "Kabar dari pasukan",
    "tooltip.events.apprenticeships_unlock": "Magang terbuka",
    "tooltip.events.trading": "Pedagang keliling",
    "tooltip.events.dummy_toy_reveal": "Ternyata bukan yang kukira",
})

T.update({
    "infos.banner.events": "Kejadian",
    "infos.banner.stats": "Statistik",
    "infos.banner.engineering": "Teknik",
    "infos.banner.resources": "Sumber daya",
    "infos.tabs.events": "Kejadian",
    "infos.tabs.stats": "Statistik",
    "infos.tabs.engineering": "Teknik",
    "infos.tabs.resources": "Sumber daya",
    "infos.tabsAriaLabel": "tab informasi",
    "game.dummy": "Boneka Kayu Raksasa",
    "game.infiniteBird": "Burung yang tak bisa dijatuhkan",
    "game.king": "Raja",
    "game.smallDragon": "Tuth'orieth, Sang Tunas",
    "game.bigDragon": "Forth'aarh, Pemberi dan Pengakhir Hidup",
    "dungeon.found": "Ditemukan",
    "dungeon.giveUp": "Menyerah",
    "dungeon.tooltipDescription": "Jelajahi ruang bawah tanah (tingkat {{level}})",
    "dungeon.cooldownMessage": "Ruang bawah tanah sedang beristirahat."
        " Tunggu {{seconds}} detik untuk masuk lagi.",
    "dungeon.cooldownShort": "{{seconds}} dtk",
    "dungeon.levelLabel": "Tingkat",
    "dungeon.levelShort": "Tingkat {{level}}",
    "dungeon.keysOwned": "Kunci dimiliki",
    "dungeon.giveUpTooltip": "Tinggalkan ruang bawah tanah"
        " (sebagian jarahan tetap kamu bawa dengan Jarahan Melimpah)",
    "dungeon.moveHint": "WASD atau tombol panah untuk berjalan",
    "dungeon.attackHint": "Klik monster untuk menyerang",
    "dungeon.chestCountsTooltip": "{{opened}} dari {{total}} peti terbuka",
    "dungeon.exitDirection": "KELUAR",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Penjelajahan berhasil",
    "summaries.dungeonLoot.titleFailed": "Penjelajahan gagal",
    "summaries.dungeonLoot.titleStuckRescue": "Berhasil keluar dengan selamat",
    "summaries.dungeonLoot.lootSummarySubtitle": "Ringkasan jarahan",
    "summaries.dungeonLoot.body_one": "Mendapat {{gold}} emas dan {{grayKeys}} kunci",
    "summaries.dungeonLoot.body_other": "Mendapat {{gold}} emas dan {{grayKeys}} kunci",
    "summaries.dungeonLoot.artifactFound": "Menemukan {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Korban semburan api",
    "summaries.fireBreathCasualties.body": "Kehilangan {{list}}",
    "summaries.fireBreathCasualties.none": "Tidak ada korban",
    "summaries.fireBreathBlocked.title": "Semburan api berhasil dihentikan!",
    "summaries.fireBreathBlocked.body": "Sebuah bom asap menyelamatkan pasukanmu.",
    "summaries.toastLabel": "Pemberitahuan permainan",
})

T.update({
    "levels.title": "Bab",
    "levels.locked": "Terkunci",
    "levels.active": "Sedang berjalan",
    "levels.completed": "Selesai",
    "levels.continue": "Lanjut",
    "levels.start": "Mulai",
    "levels.restart": "Main ulang",
    "levels.restart_progress_warning": "Main ulang sekarang?"
        " Kemajuan yang belum tersimpan di bab ini akan hilang.",
    "levels.names.mainGame": "Seekor Naga Besar",
    "levels.names.newGamePlus": "Pengelolaan Sumber Daya",
    "levels.names.dummy": "Mainan Bersihir",
    "levels.names.infinite": "Benar-benar Tak Berujung",
    "levels.names.kingBattle": "Pertempuran Terakhir Sang Raja",
})

T.update({
    "menus.tabs.saveData": "Data simpanan",
    "menus.saveData.title": "Data simpanan",
    "menus.saveData.clearChapterTitle": "Kemajuan tiap bab",
    "menus.saveData.clearChapterExplanation": "Menghapus emas, pasukan, peningkatan, kemajuan"
        " di ruang bawah tanah, dan tanda selesai untuk setiap bab. Bab yang sudah terbuka,"
        " statistik total, pengaturan, dan artefak tetap tersimpan.",
    "menus.saveData.clearChapterButton": "Hapus kemajuan tiap bab",
    "menus.saveData.clearFullTitle": "Seluruh data simpanan",
    "menus.saveData.clearFullExplanation": "Menghapus semua yang dihapus oleh penyetelan ulang"
        " bab, ditambah artefak, bab yang sudah terbuka, dan statistik total. Pengaturan suara,"
        " grafik, dan bahasa tetap tersimpan.",
    "menus.saveData.clearFullButton": "Hapus seluruh data simpanan",
    "menus.saveData.clearFullWarning": "Ini tidak bisa dibatalkan. Kamu akan kehilangan artefak,"
        " bab yang sudah terbuka, dan statistik total.",
})

T.update({
    "artifacts.title": "Artefak",
    "artifacts.subtitle": "Artefak langka kadang muncul di peti khusus dalam ruang bawah tanah."
        " Artefak tetap ada dari bab ke bab.",
    "artifacts.notYetFound": "(belum ditemukan)",
})

ART = {
    "phoenixWhistle": ("Peluit Feniks", "Seekor burung istimewa membawa mata uang baru."),
    "emberforgedShield": ("Perisai Tempaan Bara", "Prajurit kebal terhadap api naga."),
    "moonwellFlask": ("Botol Sumur Bulan", "Penyihir hanya memakai separuh mana."),
    "windstepAnklet": ("Gelang Kaki Langkah Angin", "Elf tidak bisa dibuat pingsan."),
    "fangSatchel": ("Tas Taring", "Selama ronde berjalan, pencuri menghasilkan 1 taring naga tiap 30 menit."),
    "slumberBerries": ("Buah Lelap", "Racun memperlambat raungan dan api naga selama 10 detik."),
    "echoingLute": ("Kecapi Bergema", "Pujangga memberi inspirasi dua kali lipat."),
    "blessingCenser": ("Pedupaan Berkah", "Rohaniwan selalu merekrut dua kali lipat."),
    "victoryTusk": ("Gading Kemenangan", "Menyelesaikan satu tingkat memberi taring naga dua kali lipat."),
    "cartographersLedger": ("Buku Sang Pembuat Peta", "Menunjukkan berapa peti di ruang bawah tanah yang sudah dibuka."),
    "ironSkeletonKey": ("Kunci Induk Besi", "Membuka ruang bawah tanah sampai tingkat 20."),
    "everflameLantern": ("Lentera Api Abadi", "Obor tidak pernah padam."),
    "midasCoin": ("Koin Midas", "Emas di ruang bawah tanah menjadi dua kali lipat."),
    "harvestIdol": ("Arca Panen", "Produksi sumber daya naik 25%."),
    "titanGauntlet": ("Sarung Tangan Titan", "Kerusakan per klik sepuluh kali lipat."),
    "wayfindersCompass": ("Kompas Penunjuk Jalan", "Menunjuk ke arah pintu keluar."),
    "loadedDice": ("Dadu Curang", "Setiap klik menjadi kritis."),
}
for k, (title, desc) in ART.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

D = {
    "ironFinger": ("Jari Besi", "+{{bonus}} kerusakan per klik"),
    "featherFinger": ("Jari Bulu", "+{{bonus}} klik per detik"),
    "wakeupCall": ("Panggilan Bangun", "Setiap klik memperpendek pingsan {{bonus}} detik"),
    "electricalFinger": ("Jari Listrik", "Setiap klik berpeluang {{bonus}}% memanggil petir."),
    "perfectClick": ("Klik Sempurna", "+{{bonus}}% peluang klik kritis"),
    "criticalStrike": ("Serangan Kritis", "+{{bonus}}x kerusakan pada klik kritis"),
    "goldenExplosion": ("Ledakan Emas", "{{bonus}}x imbalan saat mengeklik burung"),
    "naturalLeader": ("Pemimpin Sejati", "Klik mengisi bilah inspirasi +{{bonus}}/klik"),
    "moneyCursor": ("Kursor Emas", "{{bonus}}x emas per klik"),
    "fullChests": ("Peti Penuh", "Peluat peti kosong di ruang bawah tanah berkurang {{bonus}}%"),
    "carpalCure": ("Obat Pergelangan", "Tahan tombol tetikus untuk menyerang naga tanpa henti."),
    "shortSword": ("Pedang Pendek", "+{{bonus}}x pengali kerusakan untuk {{type}}"),
    "longSword": ("Pedang Panjang", "Tambahan +{{bonus}}x pengali kerusakan untuk prajurit"),
    "twoHandedSword": ("Pedang Dua Tangan", "Sekali lagi +{{bonus}}x pengali kerusakan untuk prajurit"),
    "battleShout": ("Teriakan Perang", "Mengisi bilah inspirasi +{{bonus}} tiap pukulan"),
    "warCry": ("Pekik Perang", "Menyalakan inspirasi sendiri pada ketukan berikutnya"
               " saat pengali sudah tertinggi"),
    "barbarian": ("Barbar", "+{{bonus}} kerusakan dasar"),
    "thickArmor": ("Baju Zirah Tebal", "Kerusakan fisik berkurang {{bonus}}%"),
    "fireArmor": ("Zirah Api", "Pasukan yang mati karena semburan api berkurang {{bonus}}%"),
    "heavyRocks": ("Batu Berat", "+{{bonus}}% kerusakan katapel tiap tingkat"),
    "silverBlade": ("Bilah Perak", "+{{bonus}}x pengali emas tiap pukulan"),
    "goldenBlade": ("Bilah Emas", "Tambahan +{{bonus}}x pengali emas tiap pukulan"),
    "loyalMercenaries": ("Tentara Bayaran Setia", "{{typePlural}} yang kamu beli memberi"
                         " +{{bonus}}x kerusakan tiap tingkat"),
    "loyalServants": ("Pelayan Setia", "Biaya merekrut {{type}} dan yang di atasnya turun {{bonus}}%"),
    "teamWork": ("Kerja Sama", "Merekrut {{typePlural}} tambahan untuk setiap {{type}} yang kamu beli"),
    "dungeonPrecision": ("Ketepatan di Kedalaman", "+{{bonus}}% peluang serangan kritis"
                         " di ruang bawah tanah"),
    "mazeCrusher": ("Penghancur Labirin", "+{{bonus}} kerusakan kritis di ruang bawah tanah"),
    "magicMissile": ("Panah Sihir", "+{{bonus}}x pengali kerusakan untuk {{type}}"),
    "manaSword": ("Pedang Mana", "Tiap penyihir mengisi pedang seorang prajurit dengan mana."
                  " +{{bonus}}x pengali kerusakan selama mana di atas 90"),
    "magicMouse": ("Tetikus Sihir", "Mengisi bilah mana +{{bonus}} tiap klik"),
    "manaSurge": ("Aliran Mana", "Mengisi bilah mana para penyihir"),
    "manaPool": ("Kolam Mana", "Mana tertinggi naik {{bonus}}%"),
    "manaBoost": ("Dorongan Mana", "Kerusakan penyihir berlipat dua selama mana di atas {{current}}"),
    "weatherForecast": ("Ramalan Cuaca", "+{{bonus}}% peluang petir menyambar"),
    "lightningStrike": ("Sambaran Petir", "Menambah satu petir sebesar +{{bonus}}x kerusakan"
                        " {{type}} untuk tiap peningkatan yang dibeli"),
    "silverStaff": ("Tongkat Perak", "+{{bonus}}x pengali emas tiap pukulan"),
    "goldenStaff": ("Tongkat Emas", "Tambahan +{{bonus}}x pengali emas tiap pukulan"),
    "magicFire": ("Api Sihir", "Obor menyala +{{bonus}} detik lebih lama"),
    "archimage": ("Arkimagus", "+{{bonus}} kerusakan dasar"),
    "huntersEye": ("Mata Pemburu", "+{{bonus}}% peluang mengenai burung dalam jangkauan tiap ketukan"),
    "criticalChance": ("Bidikan Tajam", "+{{bonus}}% peluang tembakan kritis"),
    "criticalDamage": ("Pemotong Daun", "+{{bonus}}x kerusakan pada tembakan kritis"),
    "huntingSeason": ("Musim Berburu", "Segera memanggil sekawanan burung"),
    "elvenEyes": ("Mata Elf", "Kamu tetap melihat dalam gelap +{{bonus}} detik setelah obor padam"),
    "multipleShot": ("Tembakan Ganda", "Melepas satu panah tambahan tiap tingkat"),
    "silverArrow": ("Panah Perak", "+{{bonus}}x pengali emas tiap pukulan"),
    "goldenArrow": ("Panah Emas", "Tambahan +{{bonus}}x pengali emas tiap pukulan"),
    "iceArrow": ("Panah Es", "Memperlambat api naga {{bonus}} detik"),
    "animalInstinct": ("Naluri Hewan", "Katapel melontarkan kucing menggantikan batu,"
                       " lalu harimau menggantikan kucing, tiap kali sepuluh kali lipat kerusakannya."),
    "lightningRod": ("Penangkal Petir", "Berpeluang {{bonus}}% menarik satu petir lagi"
                     " saat petir penyihir mengenai musuh."),
    "recycledArrows": ("Panah Daur Ulang", "Serangan elf memakai kayu lebih sedikit"),
    "lightfoot": ("Kaki Ringan", "+{{bonus}}% lebih cepat berjalan dan berbelok di ruang bawah tanah"),
    "fastHands": ("Tangan Cepat", "Memperpendek waktu menghasilkan emas {{bonus}} detik"),
    "sharpDagger": ("Bilah Pembunuh", "Pencuri ikut menyerang, dengan kerusakan {{current}}"),
    "poisonDagger": ("Belati Beracun", "+{{bonus}}% peluang meracuni naga"),
    "blackMamba": ("Mamba Hitam", "+{{bonus}}x kerusakan racun dari kerusakan pencuri"),
    "lingeringToxin": ("Racun yang Bertahan", "Racun bertahan +{{bonus}} detik lebih lama"),
    "smokeBomb": ("Bom Asap", "Memasang jebakan untuk naga dengan peluang {{current}}% meledak"
                  " pada pukulan berikutnya dan menahannya."),
    "catBomb": ("Bom Kucing", "Peluru katapel meledak saat mengenai, kerusakan dua kali lipat."),
    "pickpocket": ("Pencopet", "+{{bonus}}x pengali emas yang dihasilkan {{type}}"),
    "lockPick": ("Kawat Pembuka", "Tiap penjelajahan dimulai dengan {{bonus}} pintu sudah terbuka."),
    "midasTouch": ("Sentuhan Midas", "Tambahan +{{bonus}}x pengali emas yang dihasilkan {{type}}"),
    "stuffedChests": ("Peti Sesak", "+{{bonus}}% emas dari peti di ruang bawah tanah"),
    "tuningFork": ("Garpu Tala", "+{{bonus}} inspirasi terkumpul"),
    "luteSolo": ("Solo Kecapi", "+{{bonus}}x pengali inspirasi tertinggi"),
    "obnoxiousGuitarist": ("Gitaris Menyebalkan", "Inspirasi bertahan +{{bonus}} detik lebih lama"),
    "piercedEardrums": ("Gendang Telinga Pecah", "Penghitung raungan naga melambat {{bonus}}%"),
    "replay": ("Ulangan", "Berpeluang {{bonus}}% inspirasi mulai lagi begitu habis"),
    "sonicBarrier": ("Penghalang Suara", "Penghitung api naga melambat {{bonus}}%"),
    "cacofonix": ("Kakofoniks", "Membuat pasukanmu sendiri pingsan begitu dibeli"),
    "churchChoir": ("Paduan Suara Gereja", "Merekrut 1 seminari tiap kali inspirasi menyala"),
    "encore": ("Encore", "Memperpendek jeda inspirasi {{bonus}} detik"),
    "lockerRoomSpeech": ("Pidato Ruang Ganti", "Menghasilkan inspirasi saat permainan ditutup,"
                         " pada {{current}}% dari lajunya"),
    "orderInTheUk": ("Ketertiban di Kerajaan", "Saat permainan ditutup, musikmu membuat pengrajin"
                     " lembur dan menghasilkan sumber daya pada {{current}}% dari laju biasa"),
    "majorKey": ("Nada Mayor", "Membeli satu kunci ruang bawah tanah."
                 " (Ya, permainan katanya memang payah.)"),
    "vulnerableFrequencies": ("Frekuensi Rapuh", "Musuh di ruang bawah tanah kebal"
                              " {{bonus}} milidetik lebih singkat setelah tiap pukulan"),
    "heroResources": ("Bagian Kepegawaian Pahlawan", "+{{bonus}}% peluang merekrut pahlawan dua kali lipat"),
    "blessedAura": ("Aura Berkah", "Pasukan yang mati karena semburan api berkurang {{bonus}}%"),
    "blessedBird": ("Burung Terberkati", "Berpeluang {{current}}% seekor burung muncul terberkati"
                    " dan memberi emas dua kali lipat"),
    "powerTransfer": ("Pemindahan Tenaga", "Tiap kali merekrut, mana penyihir terisi 0,5"
                      " untuk setiap rohaniwan yang kamu punya"),
    "generousLoot": ("Jarahan Melimpah", "Saat penjelajahan gagal, kamu tetap membawa"
                     " {{current}}% jarahan."),
    "divineLight": ("Cahaya Ilahi", "+{{bonus}}% peluang menyalakan kembali obor yang padam"),
    "recruitWarriors": ("Rekrut Prajurit", "Membuatmu bisa merekrut prajurit ke medan perang"),
    "recruitElves": ("Rekrut Elf", "Membuatmu bisa merekrut elf ke medan perang"),
    "recruitWizards": ("Rekrut Penyihir", "Membuatmu bisa merekrut penyihir ke medan perang"),
    "recruitBards": ("Rekrut Pujangga", "Membuatmu bisa merekrut pujangga ke medan perang"),
    "recruitThieves": ("Rekrut Pencuri", "Membuatmu bisa merekrut pencuri ke medan perang"),
    "recruitClerics": ("Rekrut Rohaniwan", "Membuatmu bisa merekrut rohaniwan ke medan perang"),
}
for k, (title, desc) in D.items():
    T[f"upgrades.details.{k}.title"] = title
    T[f"upgrades.details.{k}.description"] = desc

SUFFIX = {
    "wakeupCall.suffix": " dtk",
    "elvenEyes.suffix": " dtk",
    "iceArrow.suffix": " dtk",
    "lingeringToxin.suffix": " dtk",
    "obnoxiousGuitarist.suffix": " dtk",
    "encore.suffix": " dtk",
    "manaPool.suffix": " mana",
    "manaBoost.suffix": " mana",
    "huntingSeason.suffix": " burung",
    "vulnerableFrequencies.suffix": " md",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

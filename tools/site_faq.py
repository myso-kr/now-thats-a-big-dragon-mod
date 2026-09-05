# -*- coding: utf-8 -*-
"""The questions people actually ask, in every language.

Answer engines want a question and a short, direct answer. The answers already exist -
they are the same sentences the page says in its notice - so only the questions are
written here, and `tools/build-site.py` pairs each one with the string that answers it.
That way an answer cannot drift from the page it is quoted out of, because it *is* the
page.

    q_files         -> answered by `files`         does it modify game files?
    q_achievements  -> answered by `achievements`  will my Steam achievements be affected?
    q_copy          -> answered by `copy`          do I need to own the game?
    q_langs         -> answered by `langs_note`    which languages are supported?
    q_save          -> answered by `save`          can it break my save?
"""

Q = {
    "en": dict(
        faq_h='Questions people ask',
        q_files="Does this mod modify the game's files?",
        q_achievements="Will this affect my Steam achievements?",
        q_copy="Do I need to own the game?",
        q_langs="Which languages are supported?",
        q_save="Can it break my save?",
    ),
    "ko": dict(
        faq_h='자주 묻는 질문',
        q_files="이 모드가 게임 파일을 수정하나요?",
        q_achievements="스팀 업적에 영향이 있나요?",
        q_copy="게임을 소유하고 있어야 하나요?",
        q_langs="어떤 언어를 지원하나요?",
        q_save="세이브가 손상될 수 있나요?",
    ),
    "zh-Hans": dict(
        faq_h='常见问题',
        q_files="这个模组会修改游戏文件吗？",
        q_achievements="会影响我的 Steam 成就吗？",
        q_copy="需要先拥有这款游戏吗？",
        q_langs="支持哪些语言？",
        q_save="会弄坏我的存档吗？",
    ),
    "zh-Hant": dict(
        faq_h='常見問題',
        q_files="這個模組會修改遊戲檔案嗎？",
        q_achievements="會影響我的 Steam 成就嗎？",
        q_copy="需要先擁有這款遊戲嗎？",
        q_langs="支援哪些語言？",
        q_save="會弄壞我的存檔嗎？",
    ),
    "ru": dict(
        faq_h='Частые вопросы',
        q_files="Изменяет ли мод файлы игры?",
        q_achievements="Повлияет ли это на достижения Steam?",
        q_copy="Нужно ли иметь купленную игру?",
        q_langs="Какие языки поддерживаются?",
        q_save="Может ли это сломать сохранение?",
    ),
    "es": dict(
        faq_h='Preguntas frecuentes',
        q_files="¿Este mod modifica los archivos del juego?",
        q_achievements="¿Afectará a mis logros de Steam?",
        q_copy="¿Necesito tener el juego?",
        q_langs="¿Qué idiomas están disponibles?",
        q_save="¿Puede romper mi partida guardada?",
    ),
    "ja": dict(
        faq_h='よくある質問',
        q_files="この MOD はゲームのファイルを変更しますか？",
        q_achievements="Steam の実績に影響しますか？",
        q_copy="ゲーム本体を持っている必要がありますか？",
        q_langs="どの言語に対応していますか？",
        q_save="セーブデータが壊れることはありますか？",
    ),
    "pl": dict(
        faq_h='Częste pytania',
        q_files="Czy ten mod modyfikuje pliki gry?",
        q_achievements="Czy wpłynie to na moje osiągnięcia Steam?",
        q_copy="Czy muszę mieć grę?",
        q_langs="Jakie języki są obsługiwane?",
        q_save="Czy może zepsuć mój zapis?",
    ),
    "th": dict(
        faq_h='คำถามที่พบบ่อย',
        q_files="ม็อดนี้แก้ไขไฟล์เกมหรือไม่",
        q_achievements="จะกระทบความสำเร็จบน Steam ของฉันไหม",
        q_copy="ต้องมีเกมก่อนหรือไม่",
        q_langs="รองรับภาษาอะไรบ้าง",
        q_save="ทำให้เซฟเสียหายได้ไหม",
    ),
    "uk": dict(
        faq_h='Часті запитання',
        q_files="Чи змінює мод файли гри?",
        q_achievements="Чи вплине це на мої досягнення Steam?",
        q_copy="Чи потрібно мати куплену гру?",
        q_langs="Які мови підтримуються?",
        q_save="Чи може це зламати збереження?",
    ),
    "it": dict(
        faq_h='Domande frequenti',
        q_files="Questa mod modifica i file del gioco?",
        q_achievements="Influirà sui miei obiettivi Steam?",
        q_copy="Devo possedere il gioco?",
        q_langs="Quali lingue sono supportate?",
        q_save="Può rovinare il mio salvataggio?",
    ),
    "cs": dict(
        faq_h='Časté dotazy',
        q_files="Mění tenhle mod herní soubory?",
        q_achievements="Ovlivní to moje achievementy na Steamu?",
        q_copy="Musím hru vlastnit?",
        q_langs="Které jazyky jsou podporované?",
        q_save="Může to poškodit uloženou hru?",
    ),
    "hu": dict(
        faq_h='Gyakori kérdések',
        q_files="Módosítja ez a mod a játék fájljait?",
        q_achievements="Hatással lesz a Steam-teljesítményeimre?",
        q_copy="Kell hozzá megvennem a játékot?",
        q_langs="Mely nyelvek támogatottak?",
        q_save="Tönkreteheti a mentésemet?",
    ),
    "vi": dict(
        faq_h='Câu hỏi thường gặp',
        q_files="Mod này có sửa tệp của game không?",
        q_achievements="Có ảnh hưởng đến thành tựu Steam của tôi không?",
        q_copy="Tôi có cần sở hữu game không?",
        q_langs="Hỗ trợ những ngôn ngữ nào?",
        q_save="Có thể làm hỏng tệp lưu của tôi không?",
    ),
    "sv": dict(
        faq_h='Vanliga frågor',
        q_files="Ändrar den här moden spelets filer?",
        q_achievements="Påverkar det mina Steam-prestationer?",
        q_copy="Måste jag äga spelet?",
        q_langs="Vilka språk stöds?",
        q_save="Kan den förstöra min sparfil?",
    ),
    "nl": dict(
        faq_h='Veelgestelde vragen',
        q_files="Wijzigt deze mod de bestanden van het spel?",
        q_achievements="Heeft dit gevolgen voor mijn Steam-prestaties?",
        q_copy="Moet ik het spel bezitten?",
        q_langs="Welke talen worden ondersteund?",
        q_save="Kan het mijn savebestand stukmaken?",
    ),
    "da": dict(
        faq_h='Ofte stillede spørgsmål',
        q_files="Ændrer denne mod spillets filer?",
        q_achievements="Påvirker det mine Steam-præstationer?",
        q_copy="Skal jeg eje spillet?",
        q_langs="Hvilke sprog understøttes?",
        q_save="Kan det ødelægge mit gemte spil?",
    ),
    "id": dict(
        faq_h='Pertanyaan umum',
        q_files="Apakah mod ini mengubah berkas gim?",
        q_achievements="Apakah ini memengaruhi pencapaian Steam saya?",
        q_copy="Apakah saya harus memiliki gimnya?",
        q_langs="Bahasa apa saja yang didukung?",
        q_save="Bisakah ini merusak berkas simpan saya?",
    ),
    "fi": dict(
        faq_h='Usein kysyttyä',
        q_files="Muuttaako tämä modi pelin tiedostoja?",
        q_achievements="Vaikuttaako tämä Steam-saavutuksiini?",
        q_copy="Pitääkö minun omistaa peli?",
        q_langs="Mitä kieliä tuetaan?",
        q_save="Voiko se rikkoa tallennukseni?",
    ),
    "ro": dict(
        faq_h='Întrebări frecvente',
        q_files="Acest mod modifică fișierele jocului?",
        q_achievements="Îmi afectează realizările Steam?",
        q_copy="Trebuie să dețin jocul?",
        q_langs="Ce limbi sunt acceptate?",
        q_save="Îmi poate strica salvarea?",
    ),
    "nb": dict(
        faq_h='Vanlige spørsmål',
        q_files="Endrer denne moden spillets filer?",
        q_achievements="Påvirker det Steam-prestasjonene mine?",
        q_copy="Må jeg eie spillet?",
        q_langs="Hvilke språk støttes?",
        q_save="Kan det ødelegge lagringen min?",
    ),
    "el": dict(
        faq_h='Συχνές ερωτήσεις',
        q_files="Αλλάζει αυτό το mod τα αρχεία του παιχνιδιού;",
        q_achievements="Θα επηρεάσει τα επιτεύγματά μου στο Steam;",
        q_copy="Χρειάζεται να έχω το παιχνίδι;",
        q_langs="Ποιες γλώσσες υποστηρίζονται;",
        q_save="Μπορεί να χαλάσει την αποθήκευσή μου;",
    ),
}
Q["es-419"] = dict(Q["es"])
Q["es-419"]["faq_h"] = 'Preguntas frecuentes'

# Which string answers which question. The answer is the page's own sentence, so a
# quoted answer and the page can never disagree.
ANSWERS = {
    "q_files": "files",
    "q_achievements": "achievements",
    "q_copy": "copy",
    "q_langs": "langs_note",
    "q_save": "save",
}

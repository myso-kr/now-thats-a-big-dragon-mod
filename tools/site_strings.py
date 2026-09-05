# -*- coding: utf-8 -*-
"""The site's own UI strings, in every language the mod ships.

`tools/build-site.py` writes these to `docs/_data/i18n.yml`, and the Jekyll layout looks
them up by the page's language with English as the fallback - the same shape as the
game's own i18n, so a page is localised rather than an English page with a translated
headline on it.

Only the chrome is here. Language names, percentages and counts come from
`locale/languages.json` and are the same in every language.

Keys:
    title, description   what search engines read; the game's exact name stays in Latin
    one, two, three      the three things the mod does
    skip                 the keyboard skip link
    download, source     the two buttons
    notice_h             heading for the part people must read
    unofficial, copy, files    the three things that heading covers
    langs_h, langs_note  the language index and what its marks mean
    drawn, system        which font draws this language
    design               the link to the design source of truth
"""

S = {}

S["en"] = dict(
    title="Now THAT'S a Big Dragon! — language patch, cheats, autoplay",
    description="Unofficial mod for the Steam idle game Now THAT'S a Big Dragon! - 22 language "
                "translations, an in-game cheat widget, and fully autonomous autoplay. Injected "
                "over the Chrome DevTools Protocol; no game files are modified.",
    one="Read the game in your own language.",
    two="A cheat widget for resources, upgrades and game speed.",
    three="An autoplay that buys, fights, answers dialogue and crawls dungeons unattended.",
    skip="Skip to content", download="Download", source="Source",
    notice_h="Before you use it",
    unofficial="Unofficial fan-made mod. Not affiliated with, endorsed by, or sponsored by the "
               "developer or publisher of the game, or by Valve. All trademarks and copyrights "
               "belong to their respective owners.",
    copy="Requires a legitimately purchased copy of the game. This repository contains no "
         "original game text or assets. The translation cannot be applied without your own copy.",
    files="No game files are modified. The launcher rewrites responses in memory only. Close it "
          "and the patch is gone.",
    langs_h="Every language",
    langs_note="A page appears here exactly when its translation ships, because both come from "
               "the same catalogue.",
    drawn="drawn here", system="system font",
    design="How this page is designed",
)

S["ko"] = dict(
    title="Now THAT'S a Big Dragon! 한글패치 · 치트 위젯 · 오토플레이",
    description="스팀 방치형 게임 Now THAT'S a Big Dragon! 의 비공식 모드. 22개 언어 번역과 게임 내 "
                "치트 위젯, 완전 자동 플레이를 CDP 로 주입합니다. 게임 파일은 수정하지 않습니다.",
    one="게임을 모국어로 읽으세요.",
    two="자원과 업그레이드, 게임 속도를 다루는 치트 위젯.",
    three="구매·전투·대화·던전 탐험까지 사람 없이 진행하는 오토플레이.",
    skip="본문으로 건너뛰기", download="내려받기", source="소스",
    notice_h="쓰기 전에 읽어주세요",
    unofficial="비공식 팬 제작 모드입니다. 게임의 개발사·퍼블리셔 및 Valve 와 아무 관련이 없고 승인이나 "
               "후원을 받지 않았습니다. 모든 상표와 저작권은 각 권리자에게 있습니다.",
    copy="게임을 정당하게 구매한 분만 쓸 수 있습니다. 이 저장소에는 게임의 원문이나 애셋이 없습니다. "
         "본인의 사본 없이는 번역을 적용할 수 없습니다.",
    files="게임 파일은 수정하지 않습니다. 런처는 메모리 상의 응답만 바꿉니다. 런처를 닫으면 패치도 사라집니다.",
    langs_h="지원 언어",
    langs_note="번역이 실제로 출하될 때에만 이 목록에 나타납니다. 둘 다 같은 카탈로그에서 나오기 때문입니다.",
    drawn="직접 그린 글자", system="시스템 글꼴",
    design="이 페이지의 디자인 근거",
)

S["zh-Hans"] = dict(
    title="Now THAT'S a Big Dragon! 简体中文汉化 · 修改器 · 自动挂机",
    description="Steam 放置游戏 Now THAT'S a Big Dragon! 的非官方模组。22 种语言翻译、游戏内修改器与"
                "全自动挂机，通过 CDP 注入，不修改任何游戏文件。",
    one="用自己的语言读这款游戏。",
    two="资源、升级与游戏速度的修改器。",
    three="自动购买、战斗、应答对话并探索地牢的挂机功能。",
    skip="跳到正文", download="下载", source="源代码",
    notice_h="使用前请阅读",
    unofficial="非官方粉丝模组。与游戏的开发商、发行商及 Valve 无关，未获其认可或赞助。所有商标与著作权"
               "归各自权利人所有。",
    copy="需要合法购买的游戏本体。本仓库不含任何游戏原文或素材，没有你自己的游戏副本就无法应用翻译。",
    files="不修改任何游戏文件。启动器只在内存中改写响应，关掉它补丁就消失了。",
    langs_h="全部语言",
    langs_note="翻译真正发布时，页面才会出现在这里——两者出自同一份目录。",
    drawn="本项目绘制", system="系统字体",
    design="这个页面的设计依据",
)

S["zh-Hant"] = dict(
    title="Now THAT'S a Big Dragon! 繁體中文化 · 修改器 · 自動掛機",
    description="Steam 放置遊戲 Now THAT'S a Big Dragon! 的非官方模組。22 種語言翻譯、遊戲內修改器與"
                "全自動掛機，透過 CDP 注入，不修改任何遊戲檔案。",
    one="用自己的語言讀這款遊戲。",
    two="資源、升級與遊戲速度的修改器。",
    three="自動購買、戰鬥、回應對話並探索地牢的掛機功能。",
    skip="跳到內容", download="下載", source="原始碼",
    notice_h="使用前請閱讀",
    unofficial="非官方粉絲模組。與遊戲的開發商、發行商及 Valve 無關，未獲其認可或贊助。所有商標與著作權"
               "歸各自權利人所有。",
    copy="需要合法購買的遊戲本體。本儲存庫不含任何遊戲原文或素材，沒有你自己的遊戲副本就無法套用翻譯。",
    files="不修改任何遊戲檔案。啟動器只在記憶體中改寫回應，關掉它修補就消失了。",
    langs_h="所有語言",
    langs_note="翻譯真正發布時，頁面才會出現在這裡——兩者出自同一份目錄。",
    drawn="本專案繪製", system="系統字型",
    design="這個頁面的設計依據",
)

S["ru"] = dict(
    title="Now THAT'S a Big Dragon! — русификатор, читы, автоигра",
    description="Неофициальный мод для Steam-игры Now THAT'S a Big Dragon! - перевод на 22 языка, "
                "чит-виджет и полностью автономная автоигра. Внедряется через CDP, файлы игры не "
                "изменяются.",
    one="Читайте игру на своём языке.",
    two="Чит-виджет для ресурсов, улучшений и скорости игры.",
    three="Автоигра: покупает, сражается, отвечает в диалогах и сама проходит подземелья.",
    skip="Перейти к содержимому", download="Скачать", source="Исходный код",
    notice_h="Прочтите перед использованием",
    unofficial="Неофициальный фанатский мод. Не связан с разработчиком и издателем игры или с "
               "Valve, ими не одобрен и не спонсирован. Все товарные знаки и авторские права "
               "принадлежат их владельцам.",
    copy="Нужна легально купленная копия игры. В этом репозитории нет ни оригинального текста, ни "
         "ресурсов игры: без вашей собственной копии перевод применить нельзя.",
    files="Файлы игры не изменяются. Лаунчер переписывает ответы только в памяти. Закройте его - и "
          "патча нет.",
    langs_h="Все языки",
    langs_note="Страница появляется здесь ровно тогда, когда выходит перевод: и то и другое берётся "
               "из одного каталога.",
    drawn="нарисовано здесь", system="системный шрифт",
    design="Как устроен дизайн этой страницы",
)

S["es"] = dict(
    title="Now THAT'S a Big Dragon! — traducción, trucos, juego automático",
    description="Mod no oficial para el juego idle de Steam Now THAT'S a Big Dragon! - traducción "
                "a 22 idiomas, panel de trucos y juego automático. Se inyecta por CDP; no se "
                "modifica ningún archivo del juego.",
    one="Lee el juego en tu propio idioma.",
    two="Un panel de trucos para recursos, mejoras y velocidad de juego.",
    three="Un automático que compra, lucha, responde diálogos y recorre mazmorras solo.",
    skip="Saltar al contenido", download="Descargar", source="Código fuente",
    notice_h="Léelo antes de usarlo",
    unofficial="Mod no oficial hecho por aficionados. Sin relación con la desarrolladora o "
               "distribuidora del juego ni con Valve, y sin su respaldo ni patrocinio. Las marcas "
               "y derechos pertenecen a sus titulares.",
    copy="Requiere una copia del juego comprada legítimamente. Este repositorio no contiene texto "
         "ni recursos originales: sin tu propia copia no se puede aplicar la traducción.",
    files="No se modifica ningún archivo del juego. El lanzador reescribe respuestas solo en "
          "memoria. Ciérralo y el parche desaparece.",
    langs_h="Todos los idiomas",
    langs_note="Una página aparece aquí justo cuando se publica su traducción, porque ambas salen "
               "del mismo catálogo.",
    drawn="dibujado aquí", system="fuente del sistema",
    design="Cómo está diseñada esta página",
)

S["es-419"] = dict(S["es"])
S["es-419"]["title"] = "Now THAT'S a Big Dragon! — español latino, trucos, juego automático"
S["es-419"].update(
    three="Un automático que compra, pelea, responde diálogos y recorre mazmorras solo.",
    download="Descargar",
)

S["ja"] = dict(
    title="Now THAT'S a Big Dragon! 日本語化 · チート · オートプレイ",
    description="Steam の放置ゲーム Now THAT'S a Big Dragon! の非公式 MOD。22 言語の翻訳、ゲーム内"
                "チートウィジェット、完全自動プレイを CDP 経由で注入します。ゲームファイルは変更しません。",
    one="自分の言語でゲームを読む。",
    two="資源・アップグレード・ゲーム速度のチートウィジェット。",
    three="購入、戦闘、会話の応答、ダンジョン探索まで無人で進むオートプレイ。",
    skip="本文へスキップ", download="ダウンロード", source="ソース",
    notice_h="使う前に読んでください",
    unofficial="非公式のファン制作 MOD です。ゲームの開発元・販売元および Valve とは無関係で、承認も"
               "後援も受けていません。商標と著作権はそれぞれの権利者に帰属します。",
    copy="正規に購入したゲーム本体が必要です。このリポジトリにゲームの原文やアセットは含まれておらず、"
         "ご自身のコピーなしに翻訳は適用できません。",
    files="ゲームファイルは変更しません。ランチャーはメモリ上の応答だけを書き換えます。閉じればパッチは"
          "消えます。",
    langs_h="対応言語",
    langs_note="翻訳が実際に出荷されたときにだけ、このページが並びます。どちらも同じカタログから来ている"
               "からです。",
    drawn="ここで描いた字", system="システムフォント",
    design="このページの設計根拠",
)

S["pl"] = dict(
    title="Now THAT'S a Big Dragon! — spolszczenie, cheaty, autoplay",
    description="Nieoficjalny mod do gry idle Now THAT'S a Big Dragon! ze Steam - tłumaczenie na "
                "22 języki, panel cheatów i w pełni automatyczna gra. Wstrzykiwany przez CDP; "
                "żaden plik gry nie jest modyfikowany.",
    one="Czytaj grę we własnym języku.",
    two="Panel cheatów: surowce, ulepszenia i prędkość gry.",
    three="Autoplay, który kupuje, walczy, odpowiada w dialogach i sam przechodzi lochy.",
    skip="Przejdź do treści", download="Pobierz", source="Kod źródłowy",
    notice_h="Przeczytaj przed użyciem",
    unofficial="Nieoficjalny mod fanowski. Bez związku z twórcą ani wydawcą gry, ani z Valve, i bez "
               "ich zgody czy wsparcia. Wszystkie znaki i prawa należą do ich właścicieli.",
    copy="Wymaga legalnie kupionej kopii gry. To repozytorium nie zawiera oryginalnego tekstu ani "
         "zasobów gry - bez własnej kopii nie da się zastosować tłumaczenia.",
    files="Żaden plik gry nie jest modyfikowany. Launcher przepisuje odpowiedzi tylko w pamięci. "
          "Zamknij go, a łatka znika.",
    langs_h="Wszystkie języki",
    langs_note="Strona pojawia się tu dokładnie wtedy, gdy wychodzi jej tłumaczenie - jedno i "
               "drugie pochodzi z tego samego katalogu.",
    drawn="narysowane tutaj", system="czcionka systemowa",
    design="Jak zaprojektowano tę stronę",
)

S["th"] = dict(
    title="Now THAT'S a Big Dragon! — แปลไทย ชุดโกง เล่นอัตโนมัติ",
    description="ม็อดที่ไม่เป็นทางการสำหรับเกม idle บน Steam ชื่อ Now THAT'S a Big Dragon! - แปล 22 ภาษา "
                "ชุดโกงในเกม และการเล่นอัตโนมัติเต็มรูปแบบ ฉีดผ่าน CDP โดยไม่แก้ไขไฟล์เกม",
    one="อ่านเกมในภาษาของคุณเอง",
    two="ชุดโกงสำหรับทรัพยากร การอัปเกรด และความเร็วเกม",
    three="เล่นอัตโนมัติ: ซื้อ ต่อสู้ ตอบบทสนทนา และลุยดันเจียนเอง",
    skip="ข้ามไปยังเนื้อหา", download="ดาวน์โหลด", source="ซอร์สโค้ด",
    notice_h="อ่านก่อนใช้งาน",
    unofficial="ม็อดจากแฟนเกม ไม่เป็นทางการ ไม่มีความเกี่ยวข้องกับผู้พัฒนา ผู้จัดจำหน่าย หรือ Valve และ"
               "ไม่ได้รับการรับรองหรือสนับสนุน เครื่องหมายการค้าและลิขสิทธิ์เป็นของเจ้าของแต่ละราย",
    copy="ต้องมีเกมที่ซื้ออย่างถูกต้อง คลังนี้ไม่มีข้อความหรือทรัพยากรต้นฉบับของเกม จึงใช้คำแปลไม่ได้"
         "หากไม่มีสำเนาของคุณเอง",
    files="ไม่แก้ไขไฟล์เกมใด ๆ ตัวเรียกใช้เขียนทับการตอบสนองในหน่วยความจำเท่านั้น ปิดแล้วแพตช์ก็หายไป",
    langs_h="ทุกภาษา",
    langs_note="หน้าจะปรากฏที่นี่เมื่อคำแปลออกจริง เพราะทั้งสองอย่างมาจากแคตตาล็อกเดียวกัน",
    drawn="วาดที่นี่", system="ฟอนต์ระบบ",
    design="หน้านี้ออกแบบมาอย่างไร",
)

S["uk"] = dict(
    title="Now THAT'S a Big Dragon! — українізатор, чіти, автогра",
    description="Неофіційний мод для Steam-гри Now THAT'S a Big Dragon! - переклад 22 мовами, "
                "чит-віджет і повністю автономна автогра. Впроваджується через CDP, файли гри не "
                "змінюються.",
    one="Читайте гру своєю мовою.",
    two="Чит-віджет для ресурсів, покращень і швидкості гри.",
    three="Автогра: купує, б'ється, відповідає в діалогах і сама проходить підземелля.",
    skip="Перейти до вмісту", download="Завантажити", source="Вихідний код",
    notice_h="Прочитайте перед використанням",
    unofficial="Неофіційний фанатський мод. Не пов'язаний із розробником чи видавцем гри, ані з "
               "Valve, ними не схвалений і не спонсорований. Усі знаки та права належать їхнім "
               "власникам.",
    copy="Потрібна легально придбана копія гри. У цьому репозиторії немає ні оригінального тексту, "
         "ні ресурсів гри: без вашої власної копії переклад застосувати не можна.",
    files="Файли гри не змінюються. Лаунчер переписує відповіді лише в пам'яті. Закрийте його - і "
          "патча немає.",
    langs_h="Усі мови",
    langs_note="Сторінка з'являється тут саме тоді, коли виходить переклад: і те, і те береться з "
               "одного каталогу.",
    drawn="намальовано тут", system="системний шрифт",
    design="Як влаштовано дизайн цієї сторінки",
)

S["it"] = dict(
    title="Now THAT'S a Big Dragon! — traduzione, trucchi, gioco automatico",
    description="Mod non ufficiale per il gioco idle di Steam Now THAT'S a Big Dragon! - "
                "traduzione in 22 lingue, pannello trucchi e gioco completamente automatico. "
                "Iniettato via CDP; nessun file di gioco viene modificato.",
    one="Leggi il gioco nella tua lingua.",
    two="Un pannello trucchi per risorse, potenziamenti e velocità di gioco.",
    three="Un automatico che compra, combatte, risponde ai dialoghi ed esplora i sotterranei.",
    skip="Vai al contenuto", download="Scarica", source="Codice sorgente",
    notice_h="Da leggere prima di usarlo",
    unofficial="Mod non ufficiale creata dai fan. Non affiliata allo sviluppatore o all'editore "
               "del gioco né a Valve, e non approvata né sponsorizzata da loro. Marchi e diritti "
               "appartengono ai rispettivi titolari.",
    copy="Richiede una copia del gioco acquistata regolarmente. Questo repository non contiene "
         "testo o risorse originali: senza la tua copia la traduzione non si può applicare.",
    files="Nessun file di gioco viene modificato. Il launcher riscrive le risposte solo in memoria. "
          "Chiudilo e la patch sparisce.",
    langs_h="Tutte le lingue",
    langs_note="Una pagina compare qui esattamente quando esce la sua traduzione, perché entrambe "
               "vengono dallo stesso catalogo.",
    drawn="disegnato qui", system="carattere di sistema",
    design="Come è progettata questa pagina",
)

S["cs"] = dict(
    title="Now THAT'S a Big Dragon! — čeština, cheaty, automatické hraní",
    description="Neoficiální mod pro idle hru Now THAT'S a Big Dragon! ze Steamu - překlad do 22 "
                "jazyků, panel cheatů a plně automatické hraní. Vkládá se přes CDP; žádný herní "
                "soubor se nemění.",
    one="Čti hru ve svém jazyce.",
    two="Panel cheatů pro suroviny, vylepšení a rychlost hry.",
    three="Automat, který nakupuje, bojuje, odpovídá v dialozích a sám prochází kobky.",
    skip="Přejít na obsah", download="Stáhnout", source="Zdrojový kód",
    notice_h="Přečti si to před použitím",
    unofficial="Neoficiální fanouškovský mod. Nemá vazbu na vývojáře ani vydavatele hry či na "
               "Valve a nemá jejich schválení ani podporu. Ochranné známky a práva patří jejich "
               "vlastníkům.",
    copy="Vyžaduje legálně koupenou kopii hry. Tento repozitář neobsahuje původní text ani "
         "materiály hry - bez vlastní kopie překlad použít nelze.",
    files="Žádný herní soubor se nemění. Launcher přepisuje odpovědi jen v paměti. Zavři ho a "
          "záplata je pryč.",
    langs_h="Všechny jazyky",
    langs_note="Stránka se tu objeví přesně tehdy, když vyjde její překlad - obojí pochází ze "
               "stejného katalogu.",
    drawn="nakresleno zde", system="systémové písmo",
    design="Jak je tahle stránka navržená",
)

S["hu"] = dict(
    title="Now THAT'S a Big Dragon! — magyarítás, csalások, autoplay",
    description="Nem hivatalos mod a Steamen futó Now THAT'S a Big Dragon! idle játékhoz - "
                "fordítás 22 nyelvre, csalópanel és teljesen önálló automatikus játék. CDP-n "
                "keresztül épül be; egyetlen játékfájl sem módosul.",
    one="Olvasd a játékot a saját nyelveden.",
    two="Csalópanel nyersanyagokhoz, fejlesztésekhez és játéksebességhez.",
    three="Automata, amely vásárol, harcol, párbeszédre válaszol és maga járja a kazamatákat.",
    skip="Ugrás a tartalomra", download="Letöltés", source="Forráskód",
    notice_h="Használat előtt olvasd el",
    unofficial="Nem hivatalos, rajongói mod. Nem áll kapcsolatban a játék fejlesztőjével, "
               "kiadójával vagy a Valve-vel, és nem is támogatják. A védjegyek és a szerzői jogok "
               "a jogtulajdonosokat illetik.",
    copy="Jogtisztán megvásárolt játékpéldány szükséges. Ez a tároló nem tartalmaz eredeti "
         "játékszöveget vagy tartalmat - saját példány nélkül a fordítás nem alkalmazható.",
    files="Egyetlen játékfájl sem módosul. Az indító csak a memóriában írja át a válaszokat. Zárd "
          "be, és a javítás eltűnik.",
    langs_h="Minden nyelv",
    langs_note="Egy oldal pontosan akkor jelenik meg itt, amikor a fordítása megjelenik - mindkettő "
               "ugyanabból a katalógusból jön.",
    drawn="itt rajzolva", system="rendszerbetűtípus",
    design="Hogyan készült ennek az oldalnak a terve",
)

S["vi"] = dict(
    title="Now THAT'S a Big Dragon! — Việt hóa, cheat, tự động chơi",
    description="Mod không chính thức cho game idle Now THAT'S a Big Dragon! trên Steam - dịch 22 "
                "ngôn ngữ, bảng cheat trong game và tự động chơi hoàn toàn. Tiêm qua CDP; không "
                "sửa bất kỳ tệp game nào.",
    one="Đọc game bằng ngôn ngữ của bạn.",
    two="Bảng cheat cho tài nguyên, nâng cấp và tốc độ game.",
    three="Tự động mua, chiến đấu, trả lời hội thoại và đi hầm ngục một mình.",
    skip="Bỏ qua đến nội dung", download="Tải xuống", source="Mã nguồn",
    notice_h="Đọc trước khi dùng",
    unofficial="Mod do người hâm mộ làm, không chính thức. Không liên kết với nhà phát triển, nhà "
               "phát hành game hay Valve, và không được họ chứng thực hoặc tài trợ. Mọi nhãn hiệu "
               "và bản quyền thuộc về chủ sở hữu tương ứng.",
    copy="Cần bản game đã mua hợp pháp. Kho này không chứa văn bản hay tài nguyên gốc của game - "
         "không có bản của bạn thì không thể áp dụng bản dịch.",
    files="Không sửa bất kỳ tệp game nào. Trình khởi chạy chỉ ghi đè phản hồi trong bộ nhớ. Đóng nó "
          "lại là bản vá biến mất.",
    langs_h="Tất cả ngôn ngữ",
    langs_note="Một trang xuất hiện ở đây đúng khi bản dịch của nó phát hành, vì cả hai đến từ cùng "
               "một danh mục.",
    drawn="vẽ tại đây", system="phông hệ thống",
    design="Trang này được thiết kế thế nào",
)

S["sv"] = dict(
    title="Now THAT'S a Big Dragon! — översättning, fusk, autospel",
    description="Inofficiell mod till Steam-spelet Now THAT'S a Big Dragon! - översättning till 22 "
                "språk, fuskpanel i spelet och helt självgående autospel. Injiceras via CDP; inga "
                "spelfiler ändras.",
    one="Läs spelet på ditt eget språk.",
    two="En fuskpanel för resurser, uppgraderingar och spelhastighet.",
    three="Ett autospel som köper, slåss, svarar i dialoger och går igenom fängelsehålor.",
    skip="Hoppa till innehåll", download="Ladda ner", source="Källkod",
    notice_h="Läs det här först",
    unofficial="Inofficiell mod gjord av fans. Ingen koppling till spelets utvecklare eller "
               "utgivare, eller till Valve, och varken godkänd eller sponsrad av dem. Varumärken "
               "och upphovsrätt tillhör respektive ägare.",
    copy="Kräver ett lagligt köpt exemplar av spelet. Det här förrådet innehåller ingen "
         "originaltext och inga resurser - utan ditt eget exemplar går översättningen inte att "
         "använda.",
    files="Inga spelfiler ändras. Startprogrammet skriver bara om svar i minnet. Stäng det så är "
          "patchen borta.",
    langs_h="Alla språk",
    langs_note="En sida dyker upp här precis när dess översättning släpps, för båda kommer från "
               "samma katalog.",
    drawn="ritat här", system="systemtypsnitt",
    design="Så är den här sidan formgiven",
)

S["nl"] = dict(
    title="Now THAT'S a Big Dragon! — vertaling, cheats, autoplay",
    description="Onofficiële mod voor het Steam-idlespel Now THAT'S a Big Dragon! - vertaling in "
                "22 talen, een cheatpaneel in het spel en volledig zelfstandige autoplay. "
                "Geïnjecteerd via CDP; er wordt geen spelbestand gewijzigd.",
    one="Lees het spel in je eigen taal.",
    two="Een cheatpaneel voor grondstoffen, upgrades en spelsnelheid.",
    three="Een autoplay die koopt, vecht, dialogen beantwoordt en zelf kerkers doorloopt.",
    skip="Naar de inhoud", download="Downloaden", source="Broncode",
    notice_h="Lees dit eerst",
    unofficial="Onofficiële fanmod. Geen band met de ontwikkelaar of uitgever van het spel of met "
               "Valve, en niet door hen goedgekeurd of gesponsord. Alle merken en rechten liggen "
               "bij de rechthebbenden.",
    copy="Vereist een legaal gekocht exemplaar van het spel. Deze repository bevat geen originele "
         "tekst of assets - zonder je eigen exemplaar is de vertaling niet toe te passen.",
    files="Er wordt geen spelbestand gewijzigd. De launcher herschrijft antwoorden alleen in het "
          "geheugen. Sluit hem en de patch is weg.",
    langs_h="Alle talen",
    langs_note="Een pagina verschijnt hier precies wanneer de vertaling uitkomt, omdat beide uit "
               "dezelfde catalogus komen.",
    drawn="hier getekend", system="systeemlettertype",
    design="Hoe deze pagina is ontworpen",
)

S["da"] = dict(
    title="Now THAT'S a Big Dragon! — oversættelse, snyd, autospil",
    description="Uofficiel mod til Steam-idlespillet Now THAT'S a Big Dragon! - oversættelse til "
                "22 sprog, et snydepanel i spillet og fuldt selvkørende autospil. Injiceres via "
                "CDP; ingen spilfiler ændres.",
    one="Læs spillet på dit eget sprog.",
    two="Et snydepanel til ressourcer, opgraderinger og spilhastighed.",
    three="Et autospil, der køber, kæmper, svarer i dialoger og selv går gennem fangehuller.",
    skip="Spring til indhold", download="Hent", source="Kildekode",
    notice_h="Læs det her først",
    unofficial="Uofficiel fanlavet mod. Ingen forbindelse til spillets udvikler eller udgiver eller "
               "til Valve, og hverken godkendt eller sponsoreret af dem. Varemærker og rettigheder "
               "tilhører deres respektive ejere.",
    copy="Kræver et lovligt købt eksemplar af spillet. Dette lager indeholder ingen original tekst "
         "eller assets - uden dit eget eksemplar kan oversættelsen ikke bruges.",
    files="Ingen spilfiler ændres. Starteren omskriver kun svar i hukommelsen. Luk den, og patchen "
          "er væk.",
    langs_h="Alle sprog",
    langs_note="En side dukker op her præcis når dens oversættelse udkommer, for begge kommer fra "
               "det samme katalog.",
    drawn="tegnet her", system="systemskrift",
    design="Sådan er siden formgivet",
)

S["id"] = dict(
    title="Now THAT'S a Big Dragon! — terjemahan, cheat, main otomatis",
    description="Mod tidak resmi untuk gim idle Steam Now THAT'S a Big Dragon! - terjemahan 22 "
                "bahasa, panel cheat dalam gim, dan main otomatis sepenuhnya. Disuntikkan lewat "
                "CDP; tidak ada berkas gim yang diubah.",
    one="Baca gim dalam bahasamu sendiri.",
    two="Panel cheat untuk sumber daya, peningkatan, dan kecepatan gim.",
    three="Main otomatis yang membeli, bertarung, menjawab dialog, dan menjelajah penjara bawah tanah.",
    skip="Lompat ke konten", download="Unduh", source="Kode sumber",
    notice_h="Baca dulu sebelum dipakai",
    unofficial="Mod buatan penggemar, tidak resmi. Tidak berafiliasi dengan pengembang atau "
               "penerbit gim maupun Valve, dan tidak didukung atau disponsori mereka. Semua merek "
               "dan hak cipta milik pemiliknya masing-masing.",
    copy="Perlu salinan gim yang dibeli secara sah. Repositori ini tidak memuat teks atau aset asli "
         "gim - tanpa salinanmu sendiri, terjemahan tidak bisa diterapkan.",
    files="Tidak ada berkas gim yang diubah. Peluncur hanya menulis ulang respons di memori. Tutup "
          "peluncurnya dan tambalan itu hilang.",
    langs_h="Semua bahasa",
    langs_note="Halaman muncul di sini tepat ketika terjemahannya dirilis, karena keduanya berasal "
               "dari katalog yang sama.",
    drawn="digambar di sini", system="fon sistem",
    design="Bagaimana halaman ini dirancang",
)

S["fi"] = dict(
    title="Now THAT'S a Big Dragon! — käännös, huijaukset, automaattipeli",
    description="Epävirallinen modi Steamin idle-peliin Now THAT'S a Big Dragon! - käännös 22 "
                "kielelle, pelinsisäinen huijauspaneeli ja täysin itsenäinen automaattipeli. "
                "Syötetään CDP:n kautta; pelitiedostoja ei muuteta.",
    one="Lue peli omalla kielelläsi.",
    two="Huijauspaneeli resursseille, päivityksille ja pelinopeudelle.",
    three="Automaatti, joka ostaa, taistelee, vastaa dialogeissa ja kiertää luolastot itse.",
    skip="Siirry sisältöön", download="Lataa", source="Lähdekoodi",
    notice_h="Lue tämä ensin",
    unofficial="Epävirallinen fanien tekemä modi. Ei yhteyttä pelin kehittäjään, julkaisijaan tai "
               "Valveen, eikä näiden hyväksymä tai tukema. Tavaramerkit ja oikeudet kuuluvat "
               "omistajilleen.",
    copy="Vaatii laillisesti ostetun pelin. Tässä repositoriossa ei ole pelin alkuperäistä tekstiä "
         "eikä aineistoa - ilman omaa kappalettasi käännöstä ei voi ottaa käyttöön.",
    files="Pelitiedostoja ei muuteta. Käynnistin kirjoittaa vastaukset uusiksi vain muistissa. "
          "Sulje se, ja paikkaus on poissa.",
    langs_h="Kaikki kielet",
    langs_note="Sivu ilmestyy tänne juuri silloin kun sen käännös julkaistaan, koska molemmat "
               "tulevat samasta luettelosta.",
    drawn="piirretty täällä", system="järjestelmän kirjasin",
    design="Miten tämä sivu on suunniteltu",
)

S["ro"] = dict(
    title="Now THAT'S a Big Dragon! — traducere, trișare, joc automat",
    description="Mod neoficial pentru jocul idle de pe Steam Now THAT'S a Big Dragon! - traducere "
                "în 22 de limbi, panou de trișare în joc și joc complet automat. Este injectat "
                "prin CDP; niciun fișier al jocului nu este modificat.",
    one="Citește jocul în limba ta.",
    two="Un panou de trișare pentru resurse, îmbunătățiri și viteza jocului.",
    three="Un automat care cumpără, luptă, răspunde în dialoguri și străbate singur temnițele.",
    skip="Sari la conținut", download="Descarcă", source="Cod sursă",
    notice_h="Citește înainte de a-l folosi",
    unofficial="Mod neoficial făcut de fani. Fără legătură cu dezvoltatorul sau editorul jocului "
               "ori cu Valve și fără aprobarea sau sponsorizarea lor. Mărcile și drepturile aparțin "
               "titularilor lor.",
    copy="Necesită un exemplar al jocului cumpărat legal. Acest depozit nu conține text sau "
         "resurse originale - fără exemplarul tău, traducerea nu poate fi aplicată.",
    files="Niciun fișier al jocului nu este modificat. Lansatorul rescrie răspunsurile doar în "
          "memorie. Închide-l și peticul dispare.",
    langs_h="Toate limbile",
    langs_note="O pagină apare aici exact când îi apare traducerea, pentru că amândouă vin din "
               "același catalog.",
    drawn="desenat aici", system="fontul sistemului",
    design="Cum e proiectată pagina asta",
)

S["nb"] = dict(
    title="Now THAT'S a Big Dragon! — oversettelse, juks, autospill",
    description="Uoffisiell mod til Steam-idlespillet Now THAT'S a Big Dragon! - oversettelse til "
                "22 språk, et juksepanel i spillet og helt selvgående autospill. Injiseres via "
                "CDP; ingen spillfiler endres.",
    one="Les spillet på ditt eget språk.",
    two="Et juksepanel for ressurser, oppgraderinger og spillhastighet.",
    three="Et autospill som kjøper, slåss, svarer i dialoger og går gjennom fangehull selv.",
    skip="Hopp til innhold", download="Last ned", source="Kildekode",
    notice_h="Les dette først",
    unofficial="Uoffisiell mod laget av fans. Ingen tilknytning til spillets utvikler eller utgiver "
               "eller til Valve, og verken godkjent eller sponset av dem. Varemerker og rettigheter "
               "tilhører sine eiere.",
    copy="Krever et lovlig kjøpt eksemplar av spillet. Dette lageret inneholder ingen "
         "originaltekst eller ressurser - uten ditt eget eksemplar kan ikke oversettelsen brukes.",
    files="Ingen spillfiler endres. Starteren skriver bare om svar i minnet. Lukk den, og oppdateringen "
          "er borte.",
    langs_h="Alle språk",
    langs_note="En side dukker opp her akkurat når oversettelsen slippes, fordi begge kommer fra "
               "den samme katalogen.",
    drawn="tegnet her", system="systemskrift",
    design="Slik er denne siden utformet",
)

S["el"] = dict(
    title="Now THAT'S a Big Dragon! — μετάφραση, κόλπα, αυτόματο παιχνίδι",
    description="Ανεπίσημο mod για το idle παιχνίδι του Steam Now THAT'S a Big Dragon! - μετάφραση "
                "σε 22 γλώσσες, πίνακας κόλπων μέσα στο παιχνίδι και πλήρως αυτόνομο αυτόματο "
                "παιχνίδι. Εισάγεται μέσω CDP· κανένα αρχείο του παιχνιδιού δεν αλλάζει.",
    one="Διάβασε το παιχνίδι στη γλώσσα σου.",
    two="Ένας πίνακας κόλπων για πόρους, αναβαθμίσεις και ταχύτητα παιχνιδιού.",
    three="Ένα αυτόματο που αγοράζει, πολεμά, απαντά σε διαλόγους και εξερευνά μπουντρούμια μόνο του.",
    skip="Μετάβαση στο περιεχόμενο", download="Λήψη", source="Πηγαίος κώδικας",
    notice_h="Διάβασέ το πριν το χρησιμοποιήσεις",
    unofficial="Ανεπίσημο mod φτιαγμένο από θαυμαστές. Δεν σχετίζεται με τον δημιουργό ή τον εκδότη "
               "του παιχνιδιού ούτε με τη Valve, και δεν έχει την έγκριση ή τη χορηγία τους. Τα "
               "σήματα και τα δικαιώματα ανήκουν στους κατόχους τους.",
    copy="Χρειάζεται νόμιμα αγορασμένο αντίτυπο του παιχνιδιού. Αυτό το αποθετήριο δεν περιέχει "
         "πρωτότυπο κείμενο ή υλικό - χωρίς το δικό σου αντίτυπο η μετάφραση δεν εφαρμόζεται.",
    files="Κανένα αρχείο του παιχνιδιού δεν αλλάζει. Ο εκκινητής ξαναγράφει τις απαντήσεις μόνο στη "
          "μνήμη. Κλείσ' τον και η επιδιόρθωση χάνεται.",
    langs_h="Όλες οι γλώσσες",
    langs_note="Μια σελίδα εμφανίζεται εδώ ακριβώς όταν βγαίνει η μετάφρασή της, γιατί και τα δύο "
               "βγαίνουν από τον ίδιο κατάλογο.",
    drawn="σχεδιασμένα εδώ", system="γραμματοσειρά συστήματος",
    design="Πώς σχεδιάστηκε αυτή η σελίδα",
)

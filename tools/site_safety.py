# -*- coding: utf-8 -*-
"""The four warnings that can cost somebody something, in every language.

These are kept apart from the rest of the site's copy on purpose. A marketing line going
stale is untidy; one of these going missing means a reader was not told their save can
break, that unearned achievements land on their Steam account for good, or that the
launcher opens an unauthenticated debugging port on their machine. They are reviewed as
a set, and `tools/build-site.py` refuses to write a page whose language is missing one.

The English and Korean pages carried these as hand-written prose. An earlier version of
the generator replaced both pages with a stub and took the warnings with them; this file
is why that cannot happen again.

    save          cheats and autoplay can corrupt a save
    achievements  turning off the block writes unearned achievements to Steam for good
    port          --remote-debugging-port=9223 has no authentication
    warranty      as-is, and where to write to have this taken down
"""

CONTACT = "help@myso.kr"

SAFETY = {}

SAFETY["en"] = dict(
    save="Your save can break. Cheats and autoplay can put the game into states it does "
         "not expect. Back it up before the first run.",
    achievements="The cheat widget blocks Steam achievement and stat submission by "
                 "default. Turn that off and use cheats, and unearned achievements are "
                 "recorded on your account permanently.",
    port="A remote debugging port is opened. The game is launched with "
         "--remote-debugging-port=9223, which has no authentication: any program on the "
         "same machine can attach and control it. Enable it only while using the mod.",
    warranty="Provided as is, with no warranty. This repository will be taken down on "
             "request from the rights holder: " + CONTACT,
)

SAFETY["ko"] = dict(
    save="세이브가 깨질 수 있습니다. 치트와 오토플레이는 게임이 예상하지 못한 상태를 만들 수 "
         "있습니다. 처음 실행하기 전에 백업하세요.",
    achievements="치트 위젯은 스팀 업적·통계 전송을 기본으로 차단합니다. 이를 끄고 치트를 쓰면 "
                 "얻지 않은 업적이 계정에 영구히 기록됩니다.",
    port="원격 디버깅 포트가 열립니다. 게임은 --remote-debugging-port=9223 으로 실행되며 인증이 "
         "없습니다. 같은 컴퓨터의 어떤 프로그램이든 붙어서 조작할 수 있으니, 모드를 쓰는 동안에만 "
         "켜세요.",
    warranty="있는 그대로 제공되며 어떠한 보증도 없습니다. 권리자의 요청이 있으면 이 저장소는 "
             "내려갑니다: " + CONTACT,
)

SAFETY["zh-Hans"] = dict(
    save="存档可能损坏。修改器和自动挂机会让游戏进入它没预料到的状态，首次运行前请先备份。",
    achievements="修改器默认屏蔽 Steam 成就与统计上报。关掉它再用修改器，未获得的成就会永久记入你的账号。",
    port="会开启远程调试端口。游戏以 --remote-debugging-port=9223 启动，该端口没有任何认证："
         "同一台机器上的任何程序都能接入并操控它。只在使用模组时开启。",
    warranty="按现状提供，不作任何担保。若权利人提出要求，本仓库将被下架：" + CONTACT,
)

SAFETY["zh-Hant"] = dict(
    save="存檔可能損壞。修改器和自動掛機會讓遊戲進入它沒預料到的狀態，首次執行前請先備份。",
    achievements="修改器預設封鎖 Steam 成就與統計回報。關掉它再用修改器，未取得的成就會永久記入你的帳號。",
    port="會開啟遠端偵錯連接埠。遊戲以 --remote-debugging-port=9223 啟動，該連接埠沒有任何驗證："
         "同一台機器上的任何程式都能接入並操控它。只在使用模組時開啟。",
    warranty="按現狀提供，不作任何擔保。若權利人提出要求，本儲存庫將被下架：" + CONTACT,
)

SAFETY["ru"] = dict(
    save="Сохранение может сломаться. Читы и автоигра приводят игру в состояния, которых "
         "она не ждёт. Сделайте резервную копию до первого запуска.",
    achievements="Чит-виджет по умолчанию блокирует отправку достижений и статистики в "
                 "Steam. Отключите это, используя читы, и незаработанные достижения "
                 "навсегда останутся на аккаунте.",
    port="Открывается порт удалённой отладки. Игра запускается с "
         "--remote-debugging-port=9223, и он без аутентификации: любая программа на той "
         "же машине может подключиться и управлять игрой. Включайте только на время "
         "работы с модом.",
    warranty="Предоставляется как есть, без гарантий. Репозиторий будет удалён по "
             "требованию правообладателя: " + CONTACT,
)

SAFETY["es"] = dict(
    save="Tu partida puede romperse. Los trucos y el juego automático llevan al juego a "
         "estados que no espera. Haz una copia antes de la primera ejecución.",
    achievements="El panel de trucos bloquea por defecto el envío de logros y estadísticas "
                 "a Steam. Si lo desactivas y usas trucos, los logros no ganados quedan en "
                 "tu cuenta para siempre.",
    port="Se abre un puerto de depuración remota. El juego se lanza con "
         "--remote-debugging-port=9223, sin autenticación: cualquier programa de la misma "
         "máquina puede conectarse y controlarlo. Actívalo solo mientras uses el mod.",
    warranty="Se ofrece tal cual, sin garantía. Este repositorio se retirará a petición "
             "del titular de los derechos: " + CONTACT,
)

SAFETY["es-419"] = dict(SAFETY["es"])

SAFETY["ja"] = dict(
    save="セーブが壊れることがあります。チートとオートプレイはゲームが想定しない状態を作ります。"
         "初回実行の前にバックアップしてください。",
    achievements="チートウィジェットは既定で Steam の実績・統計の送信を遮断します。これを切って"
                 "チートを使うと、獲得していない実績がアカウントに永久に記録されます。",
    port="リモートデバッグポートが開きます。ゲームは --remote-debugging-port=9223 で起動し、この"
         "ポートに認証はありません。同じ PC 上のどのプログラムも接続して操作できます。MOD を使う"
         "間だけ有効にしてください。",
    warranty="現状のまま提供され、いかなる保証もありません。権利者の要請があればこのリポジトリは"
             "取り下げます: " + CONTACT,
)

SAFETY["pl"] = dict(
    save="Zapis może się zepsuć. Cheaty i autoplay wprowadzają grę w stany, których nie "
         "przewiduje. Zrób kopię przed pierwszym uruchomieniem.",
    achievements="Panel cheatów domyślnie blokuje wysyłanie osiągnięć i statystyk do "
                 "Steam. Wyłącz to i użyj cheatów, a niezdobyte osiągnięcia zostaną na "
                 "koncie na stałe.",
    port="Otwiera się port zdalnego debugowania. Gra startuje z "
         "--remote-debugging-port=9223, bez uwierzytelniania: każdy program na tym samym "
         "komputerze może się podłączyć i nią sterować. Włączaj tylko na czas korzystania "
         "z moda.",
    warranty="Udostępniane tak jak jest, bez gwarancji. Repozytorium zostanie usunięte na "
             "żądanie właściciela praw: " + CONTACT,
)

SAFETY["th"] = dict(
    save="เซฟอาจเสียหาย ชุดโกงและการเล่นอัตโนมัติทำให้เกมเข้าสู่สถานะที่ไม่ได้คาดไว้ สำรองข้อมูลก่อนรันครั้งแรก",
    achievements="ชุดโกงปิดกั้นการส่งความสำเร็จและสถิติไปยัง Steam โดยค่าเริ่มต้น หากปิดสิ่งนี้แล้วใช้โกง "
                 "ความสำเร็จที่ไม่ได้ทำจริงจะถูกบันทึกในบัญชีอย่างถาวร",
    port="จะเปิดพอร์ตดีบักระยะไกล เกมถูกเรียกด้วย --remote-debugging-port=9223 ซึ่งไม่มีการยืนยันตัวตน "
         "โปรแกรมใดในเครื่องเดียวกันก็เชื่อมต่อและควบคุมได้ เปิดเฉพาะตอนใช้ม็อดเท่านั้น",
    warranty="ให้ตามสภาพ ไม่มีการรับประกัน คลังนี้จะถูกนำลงหากผู้ถือสิทธิ์ร้องขอ: " + CONTACT,
)

SAFETY["uk"] = dict(
    save="Збереження може зламатися. Чити й автогра доводять гру до станів, яких вона не "
         "очікує. Зробіть резервну копію до першого запуску.",
    achievements="Чит-віджет типово блокує надсилання досягнень і статистики в Steam. "
                 "Вимкніть це й скористайтеся читами — незароблені досягнення назавжди "
                 "залишаться на акаунті.",
    port="Відкривається порт віддаленого налагодження. Гра запускається з "
         "--remote-debugging-port=9223 без автентифікації: будь-яка програма на цьому ж "
         "комп'ютері може під'єднатися й керувати нею. Вмикайте лише на час роботи з модом.",
    warranty="Надається як є, без гарантій. Репозиторій буде вилучено на вимогу "
             "правовласника: " + CONTACT,
)

SAFETY["it"] = dict(
    save="Il salvataggio può rompersi. Trucchi e gioco automatico portano il gioco in "
         "stati che non prevede. Fai una copia prima del primo avvio.",
    achievements="Il pannello trucchi blocca per impostazione predefinita l'invio di "
                 "obiettivi e statistiche a Steam. Disattivalo e usa i trucchi, e gli "
                 "obiettivi non guadagnati restano sull'account per sempre.",
    port="Viene aperta una porta di debug remoto. Il gioco parte con "
         "--remote-debugging-port=9223, senza autenticazione: qualunque programma sulla "
         "stessa macchina può collegarsi e controllarlo. Attivala solo mentre usi la mod.",
    warranty="Fornito così com'è, senza garanzia. Il repository sarà rimosso su richiesta "
             "del titolare dei diritti: " + CONTACT,
)

SAFETY["cs"] = dict(
    save="Uložená hra se může poškodit. Cheaty a automatické hraní dostanou hru do stavů, "
         "které nečeká. Zálohuj ji před prvním spuštěním.",
    achievements="Panel cheatů ve výchozím stavu blokuje odesílání achievementů a "
                 "statistik na Steam. Vypni to a použij cheaty a nezasloužené achievementy "
                 "zůstanou na účtu natrvalo.",
    port="Otevře se port pro vzdálené ladění. Hra se spouští s "
         "--remote-debugging-port=9223 bez ověřování: připojit se a ovládat ji může "
         "jakýkoli program na témže počítači. Zapínej ho jen po dobu používání modu.",
    warranty="Poskytováno tak, jak je, bez záruky. Repozitář bude na žádost držitele práv "
             "stažen: " + CONTACT,
)

SAFETY["hu"] = dict(
    save="A mentés tönkremehet. A csalások és az automatikus játék olyan állapotba viszik "
         "a játékot, amelyre nincs felkészülve. Készíts másolatot az első indítás előtt.",
    achievements="A csalópanel alapból blokkolja a Steam-teljesítmények és statisztikák "
                 "beküldését. Ha ezt kikapcsolod és csalsz, a meg nem szerzett "
                 "teljesítmények véglegesen a fiókodon maradnak.",
    port="Távoli hibakeresési port nyílik. A játék --remote-debugging-port=9223 "
         "kapcsolóval indul, hitelesítés nélkül: ugyanazon a gépen bármelyik program "
         "csatlakozhat és vezérelheti. Csak a mod használatának idejére kapcsold be.",
    warranty="Ahogy van, garancia nélkül. A tárolót a jogtulajdonos kérésére eltávolítjuk: "
             + CONTACT,
)

SAFETY["vi"] = dict(
    save="Tệp lưu có thể hỏng. Cheat và tự động chơi đưa game vào những trạng thái nó "
         "không lường trước. Hãy sao lưu trước lần chạy đầu tiên.",
    achievements="Bảng cheat mặc định chặn gửi thành tựu và thống kê lên Steam. Tắt nó đi "
                 "rồi dùng cheat, thành tựu chưa đạt sẽ nằm vĩnh viễn trên tài khoản bạn.",
    port="Một cổng gỡ lỗi từ xa được mở. Game khởi chạy với --remote-debugging-port=9223, "
         "không có xác thực: bất kỳ chương trình nào trên cùng máy đều có thể kết nối và "
         "điều khiển. Chỉ bật khi đang dùng mod.",
    warranty="Cung cấp nguyên trạng, không bảo hành. Kho này sẽ bị gỡ theo yêu cầu của chủ "
             "sở hữu quyền: " + CONTACT,
)

SAFETY["sv"] = dict(
    save="Sparfilen kan gå sönder. Fusk och autospel försätter spelet i lägen det inte "
         "väntar sig. Ta en kopia före första körningen.",
    achievements="Fuskpanelen blockerar som standard att prestationer och statistik "
                 "skickas till Steam. Stänger du av det och fuskar hamnar oförtjänta "
                 "prestationer permanent på kontot.",
    port="En port för fjärrfelsökning öppnas. Spelet startas med "
         "--remote-debugging-port=9223, utan autentisering: vilket program som helst på "
         "samma dator kan ansluta och styra det. Slå på det bara när du använder moden.",
    warranty="Tillhandahålls i befintligt skick, utan garanti. Förrådet tas ned på begäran "
             "av rättighetsinnehavaren: " + CONTACT,
)

SAFETY["nl"] = dict(
    save="Je savebestand kan stukgaan. Cheats en autoplay brengen het spel in toestanden "
         "die het niet verwacht. Maak een kopie vóór de eerste keer.",
    achievements="Het cheatpaneel blokkeert standaard het versturen van prestaties en "
                 "statistieken naar Steam. Zet je dat uit en cheat je, dan staan "
                 "onverdiende prestaties permanent op je account.",
    port="Er wordt een remote-debuggingpoort geopend. Het spel start met "
         "--remote-debugging-port=9223, zonder authenticatie: elk programma op dezelfde "
         "machine kan verbinden en het besturen. Zet het alleen aan terwijl je de mod "
         "gebruikt.",
    warranty="Geleverd zoals het is, zonder garantie. Deze repository wordt op verzoek van "
             "de rechthebbende offline gehaald: " + CONTACT,
)

SAFETY["da"] = dict(
    save="Dit gemte spil kan gå i stykker. Snyd og autospil bringer spillet i tilstande, "
         "det ikke forventer. Tag en kopi før første kørsel.",
    achievements="Snydepanelet blokerer som standard indsendelse af præstationer og "
                 "statistik til Steam. Slår du det fra og snyder, ligger uindtjente "
                 "præstationer permanent på kontoen.",
    port="Der åbnes en fjernfejlfindingsport. Spillet startes med "
         "--remote-debugging-port=9223 uden godkendelse: ethvert program på samme maskine "
         "kan koble sig på og styre det. Slå det kun til, mens du bruger moddet.",
    warranty="Leveres som det er, uden garanti. Lageret tages ned på anmodning fra "
             "rettighedshaveren: " + CONTACT,
)

SAFETY["id"] = dict(
    save="Berkas simpanmu bisa rusak. Cheat dan main otomatis membawa gim ke keadaan yang "
         "tidak diantisipasinya. Cadangkan sebelum menjalankannya pertama kali.",
    achievements="Panel cheat secara bawaan memblokir pengiriman pencapaian dan statistik "
                 "ke Steam. Matikan itu lalu pakai cheat, dan pencapaian yang tidak diraih "
                 "akan tercatat permanen di akunmu.",
    port="Sebuah porta debug jarak jauh dibuka. Gim dijalankan dengan "
         "--remote-debugging-port=9223 tanpa autentikasi: program mana pun di mesin yang "
         "sama bisa terhubung dan mengendalikannya. Nyalakan hanya selama memakai mod.",
    warranty="Disediakan apa adanya, tanpa jaminan. Repositori ini akan diturunkan atas "
             "permintaan pemegang hak: " + CONTACT,
)

SAFETY["fi"] = dict(
    save="Tallennus voi rikkoutua. Huijaukset ja automaattipeli vievät pelin tiloihin, "
         "joita se ei odota. Ota varmuuskopio ennen ensimmäistä ajoa.",
    achievements="Huijauspaneeli estää oletuksena saavutusten ja tilastojen lähettämisen "
                 "Steamiin. Jos otat sen pois ja huijaat, ansaitsemattomat saavutukset "
                 "jäävät tilillesi pysyvästi.",
    port="Etävianetsintäportti avataan. Peli käynnistetään valitsimella "
         "--remote-debugging-port=9223 ilman tunnistautumista: mikä tahansa saman koneen "
         "ohjelma voi liittyä ja ohjata sitä. Pidä se päällä vain modia käyttäessäsi.",
    warranty="Toimitetaan sellaisenaan, ilman takuuta. Repositorio poistetaan "
             "oikeudenhaltijan pyynnöstä: " + CONTACT,
)

SAFETY["ro"] = dict(
    save="Salvarea se poate strica. Trișările și jocul automat duc jocul în stări la care "
         "nu se așteaptă. Fă o copie înainte de prima rulare.",
    achievements="Panoul de trișare blochează implicit trimiterea realizărilor și a "
                 "statisticilor către Steam. Dezactivează asta și trișează, iar "
                 "realizările necâștigate rămân permanent în cont.",
    port="Se deschide un port de depanare la distanță. Jocul pornește cu "
         "--remote-debugging-port=9223, fără autentificare: orice program de pe același "
         "calculator se poate conecta și îl poate controla. Activează-l doar cât "
         "folosești modul.",
    warranty="Oferit ca atare, fără garanție. Depozitul va fi retras la cererea "
             "titularului de drepturi: " + CONTACT,
)

SAFETY["nb"] = dict(
    save="Lagringen kan bli ødelagt. Juks og autospill setter spillet i tilstander det "
         "ikke venter seg. Ta en kopi før første kjøring.",
    achievements="Juksepanelet blokkerer som standard innsending av prestasjoner og "
                 "statistikk til Steam. Slår du det av og jukser, ligger ufortjente "
                 "prestasjoner permanent på kontoen.",
    port="En port for fjernfeilsøking åpnes. Spillet startes med "
         "--remote-debugging-port=9223 uten autentisering: ethvert program på samme maskin "
         "kan koble seg til og styre det. Slå det på bare mens du bruker moden.",
    warranty="Leveres som det er, uten garanti. Lageret tas ned på forespørsel fra "
             "rettighetshaveren: " + CONTACT,
)

SAFETY["el"] = dict(
    save="Η αποθήκευση μπορεί να χαλάσει. Τα κόλπα και το αυτόματο παιχνίδι φέρνουν το "
         "παιχνίδι σε καταστάσεις που δεν περιμένει. Κράτα αντίγραφο πριν την πρώτη "
         "εκτέλεση.",
    achievements="Ο πίνακας κόλπων μπλοκάρει εξ ορισμού την αποστολή επιτευγμάτων και "
                 "στατιστικών στο Steam. Αν το κλείσεις και χρησιμοποιήσεις κόλπα, "
                 "επιτεύγματα που δεν κέρδισες μένουν μόνιμα στον λογαριασμό σου.",
    port="Ανοίγει θύρα απομακρυσμένης αποσφαλμάτωσης. Το παιχνίδι ξεκινά με "
         "--remote-debugging-port=9223, χωρίς έλεγχο ταυτότητας: οποιοδήποτε πρόγραμμα στο "
         "ίδιο μηχάνημα μπορεί να συνδεθεί και να το ελέγξει. Ενεργοποίησέ το μόνο όσο "
         "χρησιμοποιείς το mod.",
    warranty="Παρέχεται ως έχει, χωρίς εγγύηση. Το αποθετήριο θα αποσυρθεί κατόπιν "
             "αιτήματος του δικαιούχου: " + CONTACT,
)

# -*- coding: utf-8 -*-
"""The Greek UI strings.

Address: singular "εσύ" throughout. The plural is the polite form in Greek, and a game
that calls you "εσείς" sounds like a bank. The King is grand in tone, not in pronoun.

Monotonic Greek: one accent, no breathings. A capital keeps its accent at the start of
a word (Έμπνευση, Όταν) but loses it when the whole word is capitalised, which is why
the dungeon's exit sign is ΕΞΟΔΟΣ and not ΈΞΟΔΟΣ.

The Greek question mark is the semicolon, so `Σίγουρα;` is a question and not a run-on.
That collides with i18next: `statistics.estimatedVictory` separates its intervals with
`;` as well, so nothing inside its brackets may ask a question. It states instead.

Decimals take a comma - "0,5 ανά Ιερέα" - which is what a Greek reader expects and what
the rest of the numbers in the UI already look like once the game formats them.

The font has no guillemets, and «» is what Greek normally quotes with. Straight double
quotes stand in, the same way every other language here handles the punctuation the
6 px/em font does not carry.
"""

T = {}

T.update({
    "upgrades.upgrades": "Αναβαθμίσεις",
    "upgrades.multiplier": "+{{multi}}",
    "upgrades.nextLevel": "Επόμενο επίπεδο",
    "upgrades.currentLevel": "Τρέχον",
    "upgrades.newGamePlusOnly": "Μόνο στο κεφάλαιο \"Διαχείριση πόρων\"",
    "upgrades.max": "Μέγ.",
    "upgrades.lockedMessage": "Αναβάθμισε κι άλλο το {{parentSkill}} για να το ξεκλειδώσεις",
    "common.wishlistNow": "Βάλ' το στη λίστα επιθυμιών!",
})

# (title, description) for every upgrade, expanded below.
D = {
    # Click.
    "ironFinger": ("Σιδερένιο δάχτυλο", "Ζημιά από επιθέσεις με κλικ +{{bonus}}"),
    "featherFinger": ("Φτερένιο δάχτυλο", "Αριθμός κλικ ανά δευτερόλεπτο +{{bonus}}"),
    "wakeupCall": ("Αφύπνιση", "Κάθε κλικ μειώνει τη διάρκεια της ζάλης κατά {{bonus}} δευτ."),
    "electricalFinger": ("Ηλεκτρικό δάχτυλο",
                         "Έχει {{bonus}}% πιθανότητα να ρίξει κεραυνό σε κάθε κλικ."),
    "perfectClick": ("Τέλειο κλικ", "Πιθανότητα για κρίσιμο κλικ +{{bonus}}%"),
    "criticalStrike": ("Κρίσιμο χτύπημα", "Αυξάνει τη ζημιά του κρίσιμου κλικ κατά +{{bonus}}x"),
    "goldenExplosion": ("Χρυσή έκρηξη",
                        "Αυξάνει την ανταμοιβή από τα πουλιά κατά {{bonus}}x"),
    "naturalLeader": ("Γεννημένος ηγέτης",
                      "Τα κλικ γεμίζουν τον μετρητή Έμπνευσης κατά +{{bonus}}/κλικ"),
    "moneyCursor": ("Χρυσός δείκτης",
                    "Αυξάνει το χρυσάφι από τις επιθέσεις με κλικ κατά {{bonus}}x"),
    "fullChests": ("Γεμάτα σεντούκια",
                   "Μειώνει την πιθανότητα να είναι άδεια τα σεντούκια κατά {{bonus}}%"),
    "carpalCure": ("Θεραπεία καρπού",
                   "Κρατώντας πατημένο το ποντίκι χτυπάς συνεχώς τον δράκο."),

    # Warrior.
    "shortSword": ("Κοντό σπαθί", "Πολλαπλασιαστής ζημιάς {{type}} +{{bonus}}x"),
    "longSword": ("Μακρύ σπαθί",
                  "Επιπλέον πολλαπλασιαστής στη ζημιά του Πολεμιστή +{{bonus}}x"),
    "twoHandedSword": ("Δίχειρο σπαθί",
                       "Κι άλλος πολλαπλασιαστής στη ζημιά του Πολεμιστή +{{bonus}}x"),
    "battleShout": ("Ιαχή μάχης",
                    "Βοηθά να γεμίσει ο μετρητής Έμπνευσης +{{bonus}} ανά επίθεση"),
    "warCry": ("Πολεμική κραυγή",
               "Ενεργοποιεί αυτόματα την Έμπνευση στον επόμενο κύκλο, μόλις φτάσει "
               "στον μέγιστο πολλαπλασιαστή"),
    "barbarian": ("Βάρβαρος", "Αυξάνει τη βασική ζημιά κατά +{{bonus}}"),
    "thickArmor": ("Χοντρή πανοπλία",
                   "Μειώνει τη σωματική ζημιά που δέχεσαι κατά {{bonus}}%"),
    "fireArmor": ("Πύρινη πανοπλία",
                  "Μειώνει τους θανάτους από τη φλογοβολία κατά {{bonus}}%"),
    "heavyRocks": ("Βαριά βράχια",
                   "Αυξάνει τη ζημιά του καταπέλτη κατά {{bonus}}% ανά επίπεδο"),
    "silverBlade": ("Ασημένια λεπίδα",
                    "Προσθέτει πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "goldenBlade": ("Χρυσή λεπίδα",
                    "Προσθέτει κι άλλον πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "loyalMercenaries": ("Πιστοί μισθοφόροι",
                         "Οι {{typePlural}} που αγοράζεις κάνουν +{{bonus}}x περισσότερη "
                         "ζημιά ανά επίπεδο"),
    "loyalServants": ("Πιστοί υπηρέτες",
                      "Το κόστος στρατολόγησης για {{type}} και ανώτερες βαθμίδες "
                      "μειώνεται κατά {{bonus}}%"),
    "teamWork": ("Ομαδική δουλειά",
                 "Στρατολογείς επιπλέον {{typePlural}} για κάθε {{type}} που αγοράζεις"),
    "dungeonPrecision": ("Ακρίβεια στο μπουντρούμι",
                         "Αυξάνει την πιθανότητα κρίσιμης ζημιάς μέσα στα μπουντρούμια "
                         "κατά {{bonus}}%"),
    "mazeCrusher": ("Θραύστης λαβυρίνθου",
                    "Αυξάνει το μπόνους κρίσιμης ζημιάς μέσα στο μπουντρούμι κατά {{bonus}}"),

    # Wizard.
    "magicMissile": ("Μαγική βολή", "Πολλαπλασιαστής ζημιάς {{type}} +{{bonus}}x"),
    "manaSword": ("Σπαθί μάνα",
                  "Κάθε Μάγος εμποτίζει 1 σπαθί Πολεμιστή με Μάνα. Ο πολλαπλασιαστής "
                  "ζημιάς αυξάνεται κατά +{{bonus}}x όταν η Μάνα είναι πάνω από 90"),
    "magicMouse": ("Μαγικό ποντίκι", "Γεμίζει τη μπάρα μάνα κατά +{{bonus}} ανά κλικ"),
    "manaSurge": ("Αναπλήρωση Μάνα", "Γεμίζει τον μετρητή Μάνα του Μάγου"),
    "manaPool": ("Δεξαμενή μάνα", "Αυξάνει τη μέγιστη Μάνα κατά {{bonus}}%"),
    "manaBoost": ("Ώθηση μάνα",
                  "Η ζημιά του Μάγου διπλασιάζεται όταν η Μάνα είναι πάνω από {{current}}"),
    "weatherForecast": ("Πρόγνωση καιρού",
                        "Αυξάνει τις πιθανότητες για κεραυνό κατά {{bonus}}%"),
    "lightningStrike": ("Κεραυνοβόλημα",
                        "Επιπλέον επίθεση με κεραυνό που προκαλεί +{{bonus}}x της ζημιάς "
                        "του {{type}} ανά αναβάθμιση που έχεις αγοράσει"),
    "silverStaff": ("Ασημένιο ραβδί",
                    "Προσθέτει πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "goldenStaff": ("Χρυσό ραβδί",
                    "Προσθέτει κι άλλον πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "magicFire": ("Μαγική φωτιά",
                  "Αυξάνει τη διάρκεια του πυρσού κατά +{{bonus}} δευτερόλεπτα"),
    "archimage": ("Αρχιμάγος", "Αυξάνει τη βασική ζημιά κατά +{{bonus}}"),

    # Elf.
    "huntersEye": ("Μάτι κυνηγού",
                   "Αυξάνει την πιθανότητα να χτυπήσεις 1 πουλί σε εμβέλεια σε κάθε "
                   "κύκλο κατά +{{bonus}}%"),
    "criticalChance": ("Οξυδερκής στόχευση", "Πιθανότητα για κρίσιμη βολή +{{bonus}}%"),
    "criticalDamage": ("Κόφτης φύλλων",
                       "Αυξάνει τη ζημιά της κρίσιμης βολής κατά +{{bonus}}x"),
    "huntingSeason": ("Κυνηγετική περίοδος", "Εμφανίζει αμέσως ένα κοπάδι πουλιά"),
    "elvenEyes": ("Ξωτικά μάτια",
                  "Όταν σβήσει ο πυρσός σου, βλέπεις ακόμη στο σκοτάδι για "
                  "+{{bonus}} δευτερόλεπτα"),
    "multipleShot": ("Πολλαπλές βολές", "Ρίχνει ένα επιπλέον βέλος ανά επίπεδο"),
    "silverArrow": ("Ασημένιο βέλος",
                    "Προσθέτει πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "goldenArrow": ("Χρυσό βέλος",
                    "Προσθέτει κι άλλον πολλαπλασιαστή {{bonus}}x στο χρυσάφι ανά επίθεση"),
    "iceArrow": ("Παγωμένο βέλος",
                 "Επιβραδύνει την πύρινη επίθεση του δράκου κατά {{bonus}} δευτ."),
    "animalInstinct": ("Ζωώδες ένστικτο",
                       "Αναβαθμίζει τα βλήματα του καταπέλτη από βράχια σε γάτες και "
                       "μετά σε τίγρεις, δεκαπλασιάζοντας τη ζημιά κάθε φορά."),
    "lightningRod": ("Αλεξικέραυνο",
                     "Έχει {{bonus}}% πιθανότητα να τραβήξει έναν επιπλέον κεραυνό όταν "
                     "ο κεραυνός του Μάγου βρει τον εχθρό."),
    "recycledArrows": ("Ανακυκλωμένα βέλη",
                       "Ξοδεύει λιγότερο ξύλο στις επιθέσεις των ξωτικών"),
    "lightfoot": ("Ελαφροπάτητος",
                  "Αυξάνει την ταχύτητα κίνησης και στροφής στα μπουντρούμια κατά {{bonus}}%"),

    # Thief.
    "fastHands": ("Γρήγορα χέρια",
                  "Μειώνει τον χρόνο παραγωγής χρυσού κατά {{bonus}} δευτερόλεπτα"),
    "sharpDagger": ("Λεπίδα δολοφόνου",
                    "Ο Κλέφτης επιτίθεται κι αυτός, με ζημιά {{current}}"),
    "poisonDagger": ("Δηλητηριασμένο στιλέτο",
                     "Αυξάνει την πιθανότητα να δηλητηριαστεί ο δράκος κατά +{{bonus}}%"),
    "blackMamba": ("Μαύρη μάμπα",
                   "Πολλαπλασιαστής ζημιάς δηλητηρίου +{{bonus}}x της ζημιάς του Κλέφτη"),
    "lingeringToxin": ("Επίμονη τοξίνη",
                       "Αυξάνει τη διάρκεια του δηλητηρίου κατά +{{bonus}} δευτερόλεπτο"),
    "smokeBomb": ("Καπνογόνο",
                  "Στήνει παγίδα για τον δράκο με {{current}}% πιθανότητα να "
                  "ενεργοποιηθεί στην επόμενη επίθεση, σταματώντας την."),
    "catBomb": ("Εκρηκτικές γάτες",
                "Τα βλήματα του καταπέλτη εκρήγνυνται με την επαφή, διπλασιάζοντας "
                "τη ζημιά τους."),
    "pickpocket": ("Πορτοφολάς",
                   "Προσθέτει πολλαπλασιαστή {{bonus}}x στην παραγωγή χρυσού του {{type}}"),
    "lockPick": ("Αντικλείδι",
                 "{{bonus}} επιπλέον πόρτες του μπουντρουμιού είναι ανοιχτές στην αρχή "
                 "κάθε εξερεύνησης."),
    "midasTouch": ("Άγγιγμα του Μίδα",
                   "Προσθέτει κι άλλον πολλαπλασιαστή {{bonus}}x στην παραγωγή χρυσού "
                   "του {{type}}"),
    "stuffedChests": ("Παραγεμισμένα σεντούκια",
                      "Αυξάνει το χρυσάφι από τα σεντούκια του μπουντρουμιού κατά {{bonus}}%"),

    # Bard.
    "tuningFork": ("Διαπασών", "Αυξάνει την παραγωγή έμπνευσης κατά +{{bonus}}"),
    "luteSolo": ("Σόλο λαούτου",
                 "Αυξάνει τον μέγιστο πολλαπλασιαστή έμπνευσης κατά +{{bonus}}x"),
    "obnoxiousGuitarist": ("Ενοχλητικός κιθαρίστας",
                           "Διάρκεια μπόνους έμπνευσης +{{bonus}} δευτερόλεπτο"),
    "piercedEardrums": ("Τρυπημένα τύμπανα",
                        "Η ταχύτητα του βρυχηθμού του δράκου μειώνεται κατά {{bonus}}%"),
    "replay": ("Επανάληψη",
               "Έχει {{bonus}}% πιθανότητα να ξαναρχίσει η Έμπνευση όταν τελειώσει"),
    "sonicBarrier": ("Ηχητικό φράγμα",
                     "Η ταχύτητα της φλογοβολίας του δράκου μειώνεται κατά {{bonus}}%"),
    "cacofonix": ("Κακοφωνίξ", "Ζαλίζει τις μονάδες σου μόλις τον αγοράσεις"),
    "churchChoir": ("Εκκλησιαστική χορωδία",
                    "Στρατολογεί 1 Σεμινάριο κάθε φορά που ενεργοποιείται η Έμπνευση"),
    "encore": ("Ανκόρ",
               "Μειώνει τον χρόνο αναμονής της Έμπνευσης κατά {{bonus}} δευτερόλεπτα"),
    "lockerRoomSpeech": ("Λόγος στα αποδυτήρια",
                         "Παράγει Έμπνευση όσο το παιχνίδι είναι κλειστό, με ρυθμό "
                         "{{current}}%"),
    "orderInTheUk": ("Τάξη στο βασίλειο",
                     "Όσο το παιχνίδι είναι κλειστό, η μουσική σου βάζει τους τεχνίτες "
                     "να δουλεύουν εκτός ωραρίου, παράγοντας πόρους στο {{current}}% "
                     "του κανονικού ρυθμού"),
    "majorKey": ("Κλειδί του Ντο",
                 "Αγόρασε ένα κλειδί μπουντρουμιού. (Ναι, το λογοπαίγνιο ήταν "
                 "εσκεμμένο.)"),
    "vulnerableFrequencies": ("Ευάλωτες συχνότητες",
                              "Μειώνει την ατρωσία των εχθρών του μπουντρουμιού μετά "
                              "από κάθε χτύπημα κατά {{bonus}} ms"),

    # Cleric.
    "heroResources": ("Ανθρώπινο δυναμικό",
                      "Η πιθανότητα να διπλασιαστούν οι ήρωες που στρατολογείς "
                      "αυξάνεται κατά +{{bonus}}%"),
    "blessedAura": ("Ευλογημένη αύρα",
                    "Μειώνει τους θανάτους από τη φλογοβολία κατά -{{bonus}}%"),
    "blessedBird": ("Ευλογημένο πουλί",
                    "Τα πουλιά έχουν {{current}}% πιθανότητα να εμφανιστούν ευλογημένα, "
                    "διπλασιάζοντας το χρυσάφι που δίνουν"),
    "powerTransfer": ("Μεταφορά δύναμης",
                      "Όταν στρατολογείς, η μάνα των Μάγων αποκαθίσταται κι αυτή κατά "
                      "0,5 ανά Ιερέα που έχεις"),
    "generousLoot": ("Γενναιόδωρη λεία",
                     "Όταν μια εξερεύνηση αποτύχει, κρατάς το {{current}}% της λείας σου."),
    "divineLight": ("Θείο φως",
                    "Αυξάνει κατά {{bonus}}% την πιθανότητα να ξανανάψεις τον πυρσό "
                    "αφού σβήσει"),
    "recruitWarriors": ("Στρατολόγηση Πολεμιστών",
                        "Σου επιτρέπει να στρατολογείς Πολεμιστές στη μάχη"),
    "recruitElves": ("Στρατολόγηση Ξωτικών",
                     "Σου επιτρέπει να στρατολογείς Ξωτικά στη μάχη"),
    "recruitWizards": ("Στρατολόγηση Μάγων",
                       "Σου επιτρέπει να στρατολογείς Μάγους στη μάχη"),
    "recruitBards": ("Στρατολόγηση Βάρδων",
                     "Σου επιτρέπει να στρατολογείς Βάρδους στη μάχη"),
    "recruitThieves": ("Στρατολόγηση Κλεφτών",
                       "Σου επιτρέπει να στρατολογείς Κλέφτες στη μάχη"),
    "recruitClerics": ("Στρατολόγηση Ιερέων",
                       "Σου επιτρέπει να στρατολογείς Ιερείς στη μάχη"),
}
for k, (title, desc) in D.items():
    T[f"upgrades.details.{k}.title"] = title
    T[f"upgrades.details.{k}.description"] = desc

# The units after a number. The rest of the prefixes and suffixes are notation - `+`,
# `x`, `%`, `k`, `ms` - and the driver supplies those unchanged.
SUFFIX = {
    "wakeupCall.suffix": " δευτ.",
    "elvenEyes.suffix": " δευτ.",
    "iceArrow.suffix": " δευτ.",
    "lingeringToxin.suffix": " δευτ.",
    "obnoxiousGuitarist.suffix": " δευτ.",
    "encore.suffix": " δευτ.",
    "manaPool.suffix": " μάνα",
    "manaBoost.suffix": " μάνα",
    "huntingSeason.suffix": " πουλιά",
    "vulnerableFrequencies.suffix": " ms",
}
T.update({f"upgrades.details.{k}": v for k, v in SUFFIX.items()})

T.update({
    "statistics.section.ttb": "Χρόνος μάχης",
    "statistics.section.dgps": "Ζημιά & χρυσάφι ανά δευτερόλεπτο",
    "statistics.section.resourceBalance": "Ισοζύγιο πόρων",
    "statistics.lifetime.title": "Συνολικά στατιστικά",
    "statistics.lifetime.totalPlaytime": "Συνολικός χρόνος παιχνιδιού",
    "statistics.lifetime.totalGoldEarned": "Συνολικό χρυσάφι που κέρδισες",
    "statistics.lifetime.totalGoldSpent": "Συνολικό χρυσάφι που ξόδεψες",
    "statistics.lifetime.totalBirdsKilled": "Συνολικά πουλιά που έριξες",
    "statistics.lifetime.totalClicks": "Συνολικά κλικ",
    "statistics.lifetime.totalHeroesRecruited": "Συνολικοί ήρωες που στρατολογήθηκαν",
    "statistics.lifetime.heroesPurchased": "Αγορασμένοι",
    "statistics.lifetime.heroesRecruited": "Στρατολογημένοι",
    "statistics.lifetime.tier1": "Βαθμίδα 1, στρατολογημένοι (αγορασμένοι)",
    "statistics.lifetime.tier2": "Βαθμίδα 2, στρατολογημένοι (αγορασμένοι)",
    "statistics.lifetime.tier3": "Βαθμίδα 3, στρατολογημένοι (αγορασμένοι)",
    "statistics.lifetime.totalDamageDealt": "Συνολική ζημιά που έκανες",
    "statistics.lifetime.totalUnitsDeadByFireBreath": "Μονάδες που χάθηκαν στη φλογοβολία",
    "statistics.battleDuration": "Πέρασαν: <strong>{{time}} {{timePrefix}}</strong>",
    "statistics.dummyEstimatedVictory": "Είναι καν δυνατή η νίκη;",
    "statistics.infiniteEstimatedVictory": "Η νίκη είναι όντως αδύνατη!",
    # The `;` here separates i18next intervals, so nothing inside the brackets may be a
    # question - in Greek that would be the same character.
    "statistics.estimatedVictory":
        "(0)[<strong class='text-danger'>Είσαι ο ήρωάς μας!</strong>]; "
        "(0-1000000000)[Νίκη σε <strong>{{count}} {{timePrefix}}</strong>];"
        "(1000000001-inf)[<strong class='text-danger'>Κάνε κλικ ή πάτα Z για να "
        "χτυπήσεις τον δράκο!</strong>]",
    "statistics.perSec": "/δευτ.",
    "statistics.generationSection": "Παραγωγή",
    "statistics.critSection": "Ειδικά",
    "statistics.dps": "Ζημιά μονάδων: <strong>{{dps}}/δευτ.</strong>",
    "statistics.gps": "Χρυσάφι μονάδων: <strong>{{gps}}/δευτ.</strong>",
    "statistics.dpc": "Ζημιά κλικ: <strong>{{dpc}}/κλικ</strong>",
    "statistics.gpc": "Χρυσάφι κλικ: <strong>{{gpc}}/κλικ</strong>",
    "statistics.catapultDamage": "Ζημιά: <strong>{{damage}}/βολή</strong>",
    "statistics.catapultTimeToShoot": "Χρόνος βολής: <strong>{{time}} δευτ.</strong>",
    "statistics.seconds_one": "δευτερόλεπτο",
    "statistics.seconds_other": "δευτερόλεπτα",
    "statistics.minutes_one": "λεπτό",
    "statistics.minutes_other": "λεπτά",
    "statistics.hours_one": "ώρα",
    "statistics.hours_other": "ώρες",
    "statistics.days_one": "μέρα",
    "statistics.days_other": "μέρες",
    "statistics.months_one": "μήνας",
    "statistics.months_other": "μήνες",
    "statistics.years_one": "χρόνος",
    "statistics.years_other": "χρόνια",
    "statistics.undo.disabledLine":
        "Κάνε κλικ μέσα στα 10 δευτ. για να αναιρέσεις μονάδες που αγόρασες κατά λάθος "
        "και να πάρεις πίσω τα λεφτά σου.",
    "statistics.undo.enabledAction": "Κάνε κλικ για να αναιρέσεις την αγορά "
                                     "{{count}} {{generator}}.",
    "statistics.undo.enabledRefund": "Θα σου επιστραφούν {{refund}}.",
    "statistics.undo.enabledTimer": "Απομένουν {{seconds}} δευτ.",
    "statistics.undo.refundGold": "{{amount}} χρυσάφι",
})

# Unit names. The short forms are what fits in a tooltip; the long ones name the thing.
UNITS = {
    "warrior": ("Πολεμιστής", "Πολεμιστές"),
    "wizard": ("Μάγος", "Μάγοι"),
    "elf": ("Ξωτικό", "Ξωτικά"),
    "garrison": ("Φρουρά", "Φρουρές"),
    "academy": ("Ακαδημία Μαγείας", "Ακαδημίες Μαγείας"),
    "academy_short": ("Ακαδημία", "Ακαδημίες"),
    "outpost": ("Φυλάκιο Τοξοτών", "Φυλάκια Τοξοτών"),
    "outpost_short": ("Φυλάκιο", "Φυλάκια"),
    "council": ("Πολεμικό Συμβούλιο", "Πολεμικά Συμβούλια"),
    "nexus": ("Κόμβος Αρχιμάγου", "Κόμβοι Αρχιμάγου"),
    "forest": ("Αρχαίο Δάσος", "Αρχαία Δάση"),
    "thief": ("Κλέφτης", "Κλέφτες"),
    "bard": ("Βάρδος", "Βάρδοι"),
    "cleric": ("Ιερέας", "Ιερείς"),
    "guild": ("Συντεχνία Κλεφτών", "Συντεχνίες Κλεφτών"),
    "guild_short": ("Συντεχνία", "Συντεχνίες"),
    "troupe": ("Θίασος Καλλιτεχνών", "Θίασοι Καλλιτεχνών"),
    "troupe_short": ("Θίασος", "Θίασοι"),
    "seminary": ("Ιερό Σεμινάριο", "Ιερά Σεμινάρια"),
    "seminary_short": ("Σεμινάριο", "Σεμινάρια"),
    "congress": ("Συνέδριο των Σκιών", "Συνέδρια των Σκιών"),
    "theater": ("Μεγάλο Θέατρο", "Μεγάλα Θέατρα"),
    "college": ("Καρδιναλικό Κολέγιο", "Καρδιναλικά Κολέγια"),
    "catapult": ("Καταπέλτης", "Καταπέλτες"),
    "builder": ("Χτίστης", "Χτίστες"),
    "engineer": ("Μηχανικός", "Μηχανικοί"),
    "farmer": ("Αγρότης", "Αγρότες"),
    "lumberjack": ("Ξυλοκόπος", "Ξυλοκόποι"),
    "miner": ("Μεταλλωρύχος", "Μεταλλωρύχοι"),
    "apprenticeships": ("Μαθητεία", "Μαθητείες"),
    "tradespeople": ("Τεχνίτης", "Τεχνίτες"),
}
for k, (one, other) in UNITS.items():
    T[f"generators.{k}_one"] = one
    T[f"generators.{k}_other"] = other

T.update({
    "generators.generators": "Στρατεύματα",
    "generators.buy": "αγορά {{amount}}",
    "generators.ngPlusUpkeep.perCycle": "/{{rate}}δευτ.",
    "generators.ngPlusProductionToggle": "Εναλλαγή παραγωγής",
    "generators.tabs.troops": "Στρατεύματα",
    "generators.tabs.support": "Υποστήριξη",
    "generators.fireUnitsButton.tooltip":
        "Απόλυσε μονάδες για να κόψεις την κατανάλωση πόρων κρατώντας λίγη παραγωγή.",
    "generators.ownedUnits": "{{unit}} που έχεις: {{amount}}",
    "generators.mana": "Μάνα",
    "generators.manaDescription": "Μαγική ενέργεια που τροφοδοτεί τις επιθέσεις των Μάγων.",
    "generators.emptyManaDescription":
        "Αγόρασε [Αναπλήρωση Μάνα] για να συνεχίσεις να επιτίθεσαι.",
    "generators.inspiration": "Έμπνευση",
    "generators.inspirationDescription":
        "Όταν ενεργοποιηθεί, οι δυνάμεις όλων των ηρώων πολλαπλασιάζονται κατά ένα ποσό.",
    "generators.tabsAriaLabel": "καρτέλες στρατευμάτων",
})

DESCRIPTIONS = {
    "warrior": "Ανθεκτικοί μαχητές σώμα με σώμα.",
    "wizard": "Μαγικές επιθέσεις μεσαίας εμβέλειας, αλλά εύθραυστη κράση.",
    "elf": "Ευέλικτοι στις επιθέσεις από απόσταση, μακριά από τον δράκο.",
    "garrison": "Οχυρωμένη βάση που στρατολογεί πολεμιστές.",
    "outpost": "Απομακρυσμένη βάση που στρατολογεί ξωτικά.",
    "academy": "Σχολή που εκπαιδεύει μάγους για τη μάχη.",
    "council": "Στρατιωτική οργάνωση που ιδρύει φρουρές.",
    "nexus": "Απόκρυφη οργάνωση που ιδρύει ακαδημίες.",
    "forest": "Ιερό άλσος που ιδρύει φυλάκια.",
    "thief": "Ύπουλος, δηλητηριάζει τον δράκο και του κλέβει χρυσάφι.",
    "bard": "Μπορεί να εμπνεύσει τα στρατεύματα να πολεμήσουν πιο σκληρά.",
    "cleric": "Προσφέρει προστασία και στρατολογεί νέους ήρωες στη μάχη.",
    "guild": "Κρυφό δίκτυο που στρατολογεί κλέφτες.",
    "troupe": "Περιοδεύων θίασος που στρατολογεί βάρδους.",
    "seminary": "Ιερό ίδρυμα που εκπαιδεύει ιερείς.",
    "congress": "Οργάνωση των σκιών που ιδρύει συντεχνίες κλεφτών.",
    "theater": "Μεγάλο ίδρυμα που ιδρύει θιάσους καλλιτεχνών.",
    "college": "Θρησκευτική οργάνωση που ιδρύει σεμινάρια.",
    "catapult": "Πολιορκητική μονάδα που κάνει μεγάλη ζημιά στον δράκο.",
    "builder": "Χτίζει κτίρια επιπέδου 2.",
    "engineer": "Δημιουργεί οργανώσεις επιπέδου 3.",
    "farmer": "Καλλιεργεί τροφή για το βασίλειο.",
    "lumberjack": "Κόβει ξύλα για την οικοδομή.",
    "miner": "Εξορύσσει μετάλλευμα από τα βουνά.",
    "apprenticeships": "Εκπαιδεύει τεχνίτες.",
}
T.update({f"generators.unitDescription.{k}": v for k, v in DESCRIPTIONS.items()})

# What a unit makes, per cycle. The `$t(...)` lookups are the game's own and are copied
# across untouched - only the words around them are Greek.
GENERATION = {
    "warrior": "{{generatorGeneration}} ζημιά/{{rate}}δευτ.",
    "wizard": "{{generatorGeneration}} ζημιά/{{rate}}δευτ.",
    "elf": "{{generatorGeneration}} ζημιά/{{rate}}δευτ.",
    "catapult": "{{generatorGeneration}} ζημιά/{{rate}}δευτ.",
    "garrison": '+{{generatorGeneration}} $t(warrior, {"count": {{generatorGeneration}} })'
                "/{{rate}}δευτ.",
    "outpost": '+{{generatorGeneration}} $t(elf, {"count": {{generatorGeneration}} })'
               "/{{rate}}δευτ.",
    "academy": '+{{generatorGeneration}} $t(wizard, {"count": {{generatorGeneration}} })'
               "/{{rate}}δευτ.",
    "council": '+{{generatorGeneration}} $t(garrison, {"count": {{generatorGeneration}} })'
               "/{{rate}}δευτ.",
    "nexus": '+{{generatorGeneration}} $t(academy_short, {"count": {{generatorGeneration}} })'
             "/{{rate}}δευτ.",
    "forest": '+{{generatorGeneration}} $t(outpost_short, {"count": {{generatorGeneration}} })'
              "/{{rate}}δευτ.",
    "guild": '+{{generatorGeneration}} $t(thief, {"count": {{generatorGeneration}} })'
             "/{{rate}}δευτ.",
    "troupe": '+{{generatorGeneration}} $t(bard, {"count": {{generatorGeneration}} })'
              "/{{rate}}δευτ.",
    "seminary": '+{{generatorGeneration}} $t(cleric, {"count": {{generatorGeneration}} })'
                "/{{rate}}δευτ.",
    "theater": '+{{generatorGeneration}} $t(troupe_short, {"count": {{generatorGeneration}} })'
               "/{{rate}}δευτ.",
    "college": '+{{generatorGeneration}} $t(seminary_short, {"count": {{generatorGeneration}} })'
               "/{{rate}}δευτ.",
    "congress": '+{{generatorGeneration}} $t(guild_short, {"count": {{generatorGeneration}} })'
                "/{{rate}}δευτ.",
    "apprenticeships": '+{{generatorGeneration}} $t(tradespeople, '
                       '{"count": {{generatorGeneration}} })/{{rate}}δευτ.',
    "thief": "+{{generatorGeneration}} χρυσάφι/{{rate}}δευτ.",
    "bard": "+{{generatorGeneration}} έμπνευση/{{rate}}δευτ.",
    "cleric": "+{{generatorGeneration}} ήρωας/{{rate}}δευτ.",
    "builder": "+{{generatorGeneration}} κτίριο/{{rate}}δευτ.",
    "engineer": "+{{generatorGeneration}} οργάνωση/{{rate}}δευτ.",
    "farmer": "+{{generatorGeneration}} τροφή/{{rate}}δευτ.",
    "lumberjack": "+{{generatorGeneration}} ξύλο/{{rate}}δευτ.",
    "miner": "+{{generatorGeneration}} μετάλλευμα/{{rate}}δευτ.",
}
T.update({f"generators.generationDescription.{k}": v for k, v in GENERATION.items()})

T.update({
    "settings.settings": "Ρυθμίσεις",
    "settings.buy_max": "Αγορά μέγιστου",
    "settings.audio": "Μουσική/Ήχοι",
    "settings.game": "Παιχνίδι",
    "settings.graphics": "Γραφικά",
    "settings.offline_progress": "Πρόοδος εκτός παιχνιδιού",
    "settings.wishlist_now": "Λίστα επιθυμιών",
})

T.update({
    "menus.settings": "Ρυθμίσεις",
    "menus.tabs.game": "Παιχνίδι",
    "menus.tabs.graphics": "Γραφικά",
    "menus.tabs.audio": "Ήχος",
    "menus.tabs.levels": "Κεφάλαια",
    "menus.tabs.saveData": "Αποθήκευση",
    "menus.tabs.credits": "Συντελεστές",
    "menus.credits.title": "Συντελεστές",
    "menus.credits.developedBy": "Ανάπτυξη",
    "menus.credits.developedWith": "Αναπτύχθηκε με",
    "menus.credits.bigThanksTo": "Ιδιαίτερες ευχαριστίες",
    "menus.credits.theRestOfTheDiscordServer": "και στους υπόλοιπους του Discord",
    "menus.credits.andYou": "και σε σένα!",
    "menus.music": "Μουσική",
    "menus.sfx": "Ηχητικά εφέ",
    "menus.audioSettings": "Ρυθμίσεις ήχου",
    "menus.gameSettings": "Ρυθμίσεις παιχνιδιού",
    "menus.graphicsSettings": "Ρυθμίσεις γραφικών",
    "menus.language": "Γλώσσα",
    "menus.languages.en": "Αγγλικά",
    "menus.languages.fr": "Γαλλικά",
    "menus.languages.de": "Γερμανικά",
    "menus.languages.pt": "Πορτογαλικά",
    "menus.languages.tr": "Τουρκικά",
    "menus.shakeIntensity": "Ένταση δόνησης",
    "menus.largerTextSize": "Μεγαλύτερα γράμματα",
    "menus.crtFilter": "Φίλτρο CRT",
    "menus.chromaticAberrationSlider": "Χρωματική εκτροπή",
    "menus.chromaticAberration": "Χρωματική εκτροπή",
    "menus.swordSwooshSounds": "Ήχοι σπαθιού & κρίσιμων",
    "menus.catSounds": "Ήχοι γάτας",
    "menus.fullscreen": "Πλήρης οθόνη",
    "menus.resume": "Συνέχεια παιχνιδιού",
    "menus.close": "Κλείσιμο",
    "menus.quitGame": "Έξοδος από το παιχνίδι",
    "menus.joinDiscord": "Μπες στο Discord",
    "menus.clear_save_label": "Να σβηστεί η πρόοδός σου;",
    "menus.zoom_adjustment": "Ζουμ διεπαφής",
    "menus.clear_save": "Σβήσε τώρα",
    "menus.are_you_sure": "Σίγουρα;",
    "menus.cannot_be_reversed": "Αυτή η ενέργεια δεν αναιρείται.",
    "menus.yes": "Ναι",
    "menus.no": "Όχι",
    "menus.saveData.title": "Δεδομένα αποθήκευσης",
    "menus.saveData.clearChapterTitle": "Πρόοδος κεφαλαίων",
    "menus.saveData.clearChapterExplanation":
        "Σβήνει χρυσάφι, μονάδες, αναβαθμίσεις, πρόοδο στα μπουντρούμια και σήματα "
        "ολοκλήρωσης για κάθε κεφάλαιο. Τα ξεκλειδωμένα κεφάλαια, τα συνολικά "
        "στατιστικά, οι ρυθμίσεις και τα κειμήλια μένουν.",
    "menus.saveData.clearChapterButton": "Σβήσε την πρόοδο των κεφαλαίων",
    "menus.saveData.clearFullTitle": "Όλα τα δεδομένα του παιχνιδιού",
    "menus.saveData.clearFullExplanation":
        "Σβήνει ό,τι και η επαναφορά κεφαλαίων, συν τα κειμήλια, τα ξεκλειδωμένα "
        "κεφάλαια και τα συνολικά στατιστικά. Οι ρυθμίσεις ήχου, γραφικών και γλώσσας "
        "μένουν.",
    "menus.saveData.clearFullButton": "Σβήσε όλα τα δεδομένα",
    "menus.saveData.clearFullWarning":
        "Αυτό δεν αναιρείται. Θα χάσεις κειμήλια, ξεκλειδωμένα κεφάλαια και συνολικά "
        "στατιστικά.",
})

T.update({
    "tooltip.inspiration": "Έμπνευση",
    "tooltip.inspirationDescription":
        "Όταν ενεργοποιηθεί, οι δυνάμεις όλων των ηρώων πολλαπλασιάζονται κατά ένα ποσό.",
    "tooltip.maxInspiration": "Μέγιστος πολλαπλασιαστής",
    "tooltip.maxInspirationMultiplier": "Μέγιστος πολλαπλασιαστής",
    "tooltip.statisticsDescription":
        "Αναλυτικά στατιστικά για την πρόοδο και την απόδοσή σου στη μάχη.",
    "tooltip.hudStopBird": "Σταμάτα το πουλί",
    "tooltip.hudLifetimeStats": "Συνολικά στατιστικά",
    "tooltip.hudHideWindows": "Κρύψε τα παράθυρα",
    "tooltip.events.roar": "Εκκωφαντικός βρυχηθμός",
    "tooltip.events.fire": "Φλογοβολία",
    "tooltip.events.claw": "Επίθεση με νύχια",
    "tooltip.events.dialog": "Ειδικό γεγονός",
    "tooltip.events.pope_visit": "Ένας ξεχωριστός επισκέπτης",
    "tooltip.events.dungeon_keys": "Ένα σκοτεινό μυστικό",
    "tooltip.events.missing_king": "Πού είναι ο Βασιλιάς;",
    "tooltip.events.catapult": "Πρωτότυπο μηχανικής",
    "tooltip.events.engineer": "Μια ευπρόσδεκτη βοήθεια",
    "tooltip.events.invasion_start": "Πλησιάζει εισβολή",
    "tooltip.events.invasion_end": "Νέα από τα στρατεύματά μας",
    "tooltip.events.apprenticeships_unlock": "Διαθέσιμες μαθητείες",
    "tooltip.events.trading": "Περιπλανώμενος έμπορος",
    "tooltip.events.dummy_toy_reveal": "Δεν το περίμενα αυτό",
})

T.update({
    "infos.banner.events": "Γεγονότα",
    "infos.banner.stats": "Στατιστικά",
    "infos.banner.engineering": "Μηχανική",
    "infos.banner.resources": "Πόροι",
    "infos.tabs.events": "Γεγον.",
    "infos.tabs.stats": "Στατ.",
    "infos.tabs.engineering": "Μηχ.",
    "infos.tabs.resources": "Πόροι",
    "infos.tabsAriaLabel": "καρτέλες πληροφοριών",
})

T.update({
    "game.dummy": "Μεγάλο Ομοίωμα",
    "game.infiniteBird": "Το Αβύθιστο Πουλί",
    "game.king": "Ο Βασιλιάς",
    # The dragons' own names are the game's, and stay as they are; only the epithets
    # are Greek.
    "game.smallDragon": "Tuth'orieth, ο Ανθίζων",
    "game.bigDragon": "Forth'aarh, ο Ζωοδότης και Τερματιστής",
})

T.update({
    "dungeon.found": "Βρέθηκε",
    "dungeon.giveUp": "Παραιτούμαι",
    "dungeon.tooltipDescription": "Ξεκίνα μια εξερεύνηση μπουντρουμιού (Επ. {{level}})",
    "dungeon.cooldownMessage":
        "Το μπουντρούμι είναι σε αναμονή. Περίμενε {{seconds}} δευτ. για να ξαναμπείς.",
    "dungeon.cooldownShort": "{{seconds}}δ",
    "dungeon.levelLabel": "Επίπεδο",
    "dungeon.levelShort": "Επ.{{level}}",
    "dungeon.keysOwned": "Κλειδιά που έχεις",
    "dungeon.giveUpTooltip":
        "Βγες από το μπουντρούμι (κρατάς μέρος της λείας αν έχεις Γενναιόδωρη λεία)",
    "dungeon.moveHint": "WASD ή βελάκια για κίνηση",
    "dungeon.attackHint": "Κάνε κλικ στο τέρας για επίθεση",
    "dungeon.chestCountsTooltip": "{{opened}} από {{total}} σεντούκια ανοιχτά",
    # All capitals, so the accent comes off - ΕΞΟΔΟΣ, never ΈΞΟΔΟΣ.
    "dungeon.exitDirection": "ΕΞΟΔΟΣ",
})

T.update({
    "summaries.dungeonLoot.titleSuccess": "Επιτυχής εξερεύνηση",
    "summaries.dungeonLoot.titleFailed": "Αποτυχημένη εξερεύνηση",
    "summaries.dungeonLoot.titleStuckRescue": "Ασφαλής έξοδος",
    "summaries.dungeonLoot.lootSummarySubtitle": "Σύνοψη λείας",
    "summaries.dungeonLoot.body_one": "Κέρδισες {{gold}} χρυσάφι και {{grayKeys}} κλειδί",
    "summaries.dungeonLoot.body_other": "Κέρδισες {{gold}} χρυσάφι και {{grayKeys}} κλειδιά",
    "summaries.dungeonLoot.artifactFound": "Βρήκες: {{artifactName}}.",
    "summaries.fireBreathCasualties.title": "Απώλειες από τη φλογοβολία",
    "summaries.fireBreathCasualties.body": "Έχασες {{list}}",
    "summaries.fireBreathCasualties.none": "Καμία απώλεια",
    "summaries.fireBreathBlocked.title": "Η φλογοβολία μπλοκαρίστηκε!",
    "summaries.fireBreathBlocked.body": "Ένα καπνογόνο έσωσε τα στρατεύματά σου.",
    "summaries.toastLabel": "Ειδοποίηση παιχνιδιού",
})

T.update({
    "levels.title": "Κεφάλαια",
    "levels.locked": "Κλειδωμένο",
    "levels.active": "Σε εξέλιξη",
    "levels.completed": "Ολοκληρώθηκε",
    "levels.continue": "Συνέχεια",
    "levels.start": "Έναρξη",
    "levels.restart": "Από την αρχή",
    "levels.restart_progress_warning":
        "Να ξεκινήσει από την αρχή; Θα χάσεις όση πρόοδο δεν αποθηκεύτηκε σε αυτό το "
        "κεφάλαιο.",
    "levels.names.mainGame": "Ένας Μεγάλος Δράκος",
    # Has to read the same as upgrades.newGamePlusOnly, which quotes it.
    "levels.names.newGamePlus": "Διαχείριση πόρων",
    "levels.names.dummy": "Το Μαγικό Παιχνίδι",
    "levels.names.infinite": "Πραγματικά Ατελείωτο",
    "levels.names.kingBattle": "Η Τελευταία Στάση του Βασιλιά",
})

T.update({
    "artifacts.title": "Κειμήλια",
    "artifacts.subtitle":
        "Σπάνια κειμήλια βρίσκονται πού και πού σε ειδικά σεντούκια των μπουντρουμιών. "
        "Παραμένουν σε όλα τα κεφάλαια.",
    "artifacts.notYetFound": "(δεν βρέθηκε ακόμη)",
})

ARTIFACTS = {
    "phoenixWhistle": ("Σφυρίχτρα του Φοίνικα",
                       "Ένα ξεχωριστό πουλί κουβαλά ένα νέο νόμισμα."),
    "emberforgedShield": ("Ασπίδα από Χόβολη",
                          "Οι Πολεμιστές είναι άτρωτοι στη φωτιά του δράκου."),
    "moonwellFlask": ("Φιάλη Σεληνοπηγής",
                      "Η μάνα των Μάγων καταναλώνεται με τον μισό ρυθμό."),
    "windstepAnklet": ("Περισφύριο Ανεμοβήματος", "Τα Ξωτικά δεν ζαλίζονται."),
    "fangSatchel": ("Σακίδιο Δοντιών",
                    "Οι Κλέφτες παράγουν 1 δόντι δράκου κάθε 30 λεπτά όσο τρέχει μια "
                    "παρτίδα."),
    "slumberBerries": ("Μούρα του Ύπνου",
                       "Οι επιθέσεις με δηλητήριο καθυστερούν τον βρυχηθμό και τη φωτιά "
                       "του δράκου κατά 10 δευτερόλεπτα."),
    "echoingLute": ("Λαούτο της Ηχούς", "Ο βάρδος διπλασιάζει το μπόνους Έμπνευσης."),
    "blessingCenser": ("Θυμιατό της Ευλογίας",
                       "Ο ιερέας στρατολογεί πάντα διπλάσιες μονάδες."),
    "victoryTusk": ("Χαυλιόδοντας της Νίκης",
                    "Η ολοκλήρωση ενός επιπέδου διπλασιάζει την ανταμοιβή σε δόντια "
                    "δράκου."),
    "cartographersLedger": ("Κατάστιχο του Χαρτογράφου",
                            "Δείχνει πόσα σεντούκια άνοιξες και πόσα υπάρχουν συνολικά."),
    "ironSkeletonKey": ("Σιδερένιο Αντικλείδι",
                        "Ξεκλειδώνει το μπουντρούμι ως το επίπεδο 20."),
    "everflameLantern": ("Φανάρι της Αιώνιας Φλόγας", "Ο πυρσός δεν σβήνει ποτέ."),
    "midasCoin": ("Νόμισμα του Μίδα", "Διπλάσιο χρυσάφι στα μπουντρούμια."),
    "harvestIdol": ("Είδωλο της Σοδειάς", "Η παραγωγή πόρων αυξάνεται κατά 25%."),
    "titanGauntlet": ("Γάντι του Τιτάνα", "Ζημιά από κλικ x10."),
    "wayfindersCompass": ("Πυξίδα του Οδοιπόρου",
                          "Δείχνει προς ποια μεριά είναι η έξοδος του μπουντρουμιού."),
    "loadedDice": ("Πειραγμένα Ζάρια", "Τα κλικ είναι πάντα κρίσιμα."),
}
for k, (title, desc) in ARTIFACTS.items():
    T[f"artifacts.details.{k}.title"] = title
    T[f"artifacts.details.{k}.description"] = desc

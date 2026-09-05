# -*- coding: utf-8 -*-
"""Writes the Greek .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: "εσύ" throughout, and the King with it. The plural is the polite form in
Greek and would make him sound like a ministry; he is grand in tone, not in pronoun.
The Pope keeps the plural, because a Pope addressing a stranger really would.

Two puns survive intact. "Cat-a-pult" becomes "Γατα-πέλτης" - καταπέλτης with γάτα
inside it, which is the same joke in the same place. The censored bird keeps its
asterisks.

The game's font has no curly quotes, no em dash and no guillemets, so straight quotes
and hyphens throughout - and the ellipsis is three dots, not one character.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Φαίνεται πως χρειάζεσαι βοήθεια για να βγάζεις περισσότερους πόρους...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Δοκίμασε ν' αγοράσεις Μαθητείες, για να έχεις κι άλλους αγρότες, μεταλλωρύχους και ξυλοκόπους.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Γεια σου, πάλι!

# speaker:engineer
Συνεχίσαμε την έρευνα πάνω στην πολιορκητική σου μηχανή.

# speaker:engineer
# wait:300
# pace:30
Τώρα μπορεί να εκτοξεύει γάτες στους εχθρούς, και πιστεύουμε ότι γέρνει τη ζυγαριά υπέρ μας.

# speaker:engineer
# wait:300
# pace:30
# chain_next
Τον λέμε "Γατα-πέλτη"

# speaker:engineer
# wait:300
# pace:300
(δραματική παύση)

# speaker:engineer
# pace:30
Θέλεις να επενδύσεις στην αναβάθμιση, για όσους έχεις και για όσους πάρεις;

* [Προτιμώ να ρίχνω βράχια]
    -> no_thanks

* [Πλήρωσε {catapultCostLabel} χρυσάφι]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Πες μας πώς σου φάνηκε!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Πες μας πώς σου φάνηκε!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Κρίμα. Καλή τύχη πάντως.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Τα στρατεύματά σου σου άφησαν το τελευταίο χτύπημα.

# speaker:king
# pace:30
- Είναι η ευκαιρία σου να το ρίξεις κάτω μια για πάντα!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Ο Βασιλιάς σού ζήτησε να συνεχίσεις την εξάσκηση, μήπως και έρθει κάτι μεγαλύτερο.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Αυτή τη φορά θέλει μάλιστα να χρηματοδοτήσει τον στρατό σου, να τον φτιάξεις όπως θες.

# speaker:princess
# pace:40
# chain_next
# wait:500
Όταν όμως του ζήτησα ένα τεράστιο πάρτι γενεθλίων πριν λίγους μήνες,

# speaker:princess
# pace:40
# chain_next
# wait:500
ήταν όλο...

# speaker:princess
# pace:60
# classes:imitating
"Μπλα, μπλα, μπλα, το βασίλειο δεν έχει λεφτά, κόρη μου!"


# speaker:princess
# pace:37
Πάντως, παράξενο μου φαίνεται αυτό το ομοίωμα...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Τι; Δεν πίστευα ότι γινόταν να νικηθεί.

# speaker:princess
# pace:20
# classes:love
Υπάρχει τίποτα που να μην μπορεί να νικήσει ο ήρωάς μου;

# speaker:princess
# events:whistle
# pace:50
Τι, τι είναι αυτό εκεί πάνω;

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Αυτό δεν είναι ένα απλό ομοίωμα εξάσκησης.

# speaker:princess
# pace:30
Μοιάζει με μαγικό παιχνίδι. Για κάτι πολύ μεγαλύτερο από εμάς.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Ε, εσύ εκεί πέρα...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Βρήκα αυτά τα κλειδιά για το μυστικό μπουντρούμι κάτω από το κάστρο.

# speaker:rogue
# pace:30
# wait:500
Αναρωτιέμαι αν ο Βασιλιάς ξέρει καν ότι υπάρχει.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Τέλος πάντων...

# speaker:rogue
# pace:30
Έπιασα καλή λεία στις εξερευνήσεις μου, αλλά στην τελευταία παραλίγο να μου σβήσει ο πυρσός.

# speaker:rogue
# wait:500
Φοβάμαι να ξαναμπώ και να χαθώ στο σκοτάδι, οπότε σου δίνω όλα τα κλειδιά τζάμπα.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Καλή τύχη,

# speaker:rogue
# pace:100
# events:end_give_keys
και πρόσεχε, σε παρακαλώ.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Γεια! Είμαι ο προγραμματιστής.

# pace:40
Συγγνώμη που πέρασες μέσα από τοίχο. Δικό μου το σφάλμα.

# pace:30
Μπορώ να σε βγάλω από το κενό, και θα κρατήσεις όλη σου τη λεία.

* [Παραιτούμαι και κρατάω τη λεία μου]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Γεια σου!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Γεια σου, Ήρωα!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Για να βοηθήσει στη μάχη, η Αυτού Μεγαλειότης διέταξε το Τάγμα Αρχιτεκτόνων και Μηχανικών του Στέμματος να προσφέρει τις γνώσεις μας.

# speaker:engineer
# pace:30
Θα σε βοηθήσουμε με τρεις τρόπους:

# speaker:engineer
# pace:30
- Χτίζοντας καταπέλτες για την πολιορκία.

# speaker:engineer
# pace:30
- Χτίζοντας κτίρια δεύτερης βαθμίδας, μέσω των Χτιστών μας.

# speaker:engineer
# pace:30
- Ιδρύοντας οργανώσεις ανώτερης βαθμίδας, μέσω των Μηχανικών μας.

# speaker:engineer
# pace:30
Όταν έχεις το χρυσάφι, θα μας βρεις στην καρτέλα Μηχανική.

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Α, τι νόμιζες ότι σήμαινε το "απόλυσε μερικές μονάδες";

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Δεν σου έφτασε που με σκότωσες; Σταμάτα να με ενοχλείς, σε παρακαλώ!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Τσίου τσίου, ρε καθ*****!

-> END
"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Είμαι έτοιμος να παίξω για τα στρατεύματά σου και να τα εμπνεύσω, να δυναμώσουν οι δυνάμεις τους.

# speaker:bard_dialog
# pace:35
# wait:400
Πάτα το κουμπί με την άρπα και χάρου την προσωρινή ενίσχυση!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Βοήθεια!

# speaker:king
# chain_next
# pace:30
# wait:500
Ένας γιγάντιος δράκος καταστρέφει το χωριό μας!

# speaker:king
# wait:300
# pace:30
- Χρειαζόμαστε έναν ήρωα να μας σώσει.

# speaker:king
# pace:30
- Σκότωσε αυτόν τον δράκο με το κραταιό σου σπαθί/δείκτη ποντικιού.

# speaker:king
# pace:30
- Ίσως μπορέσεις και να στρατολογήσεις βοήθεια, αν έχεις αρκετό χρυσάφι.

# speaker:king
# pace:30
- Καλή τύχη!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
Κάπως, ο Forth'aarh γύρισε!

# speaker:king
# pace:30
# wait:400
Εσύ όμως διέλυσες τα στρατεύματά σου. Τώρα πρέπει να στρατολογήσεις καινούργια.

# speaker:king
# wait:300
# pace:30
- Και η προηγούμενη επίθεση ρήμαξε την οικονομία μας, οπότε δεν μπορώ να χρηματοδοτήσω τον στρατό σου.

# speaker:king
# pace:40
# chain_next
- Από δω και πέρα θα καταναλώνουν

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- τροφή, ξύλο και μετάλλευμα.

# speaker:king
# pace:40
- Θα πρέπει να διαχειρίζεσαι καλά τους πόρους σου.

# speaker:king
# pace:40
- Άλλαζε πότε η κάθε μονάδα καταναλώνει πόρους και πότε όχι.

# speaker:king
# pace:40
- Ή απόλυσε μερικές, να καταναλώνουν λιγότερα αλλά να βγάζουν κάποια δουλειά.

# speaker:king
# pace:28
- Καλή τύχη!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Δυστυχώς οι μονάδες μας δεν έφτασαν για ν' αποκρούσουν την εισβολή.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Χάσαμε και την τελευταία μονάδα, και μαζί χάσαμε και το ποσό των λύτρων.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Τα στρατεύματά μας γύρισαν με σπουδαία νέα!

# speaker:king
# pace:30
Κατάφεραν ν' αποκρούσουν την εισβολή με ελάχιστες απώλειες.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Τα καλωσορίζουμε πίσω (για να συνεχίσουν την αγγαρεία με τον δράκο...)

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
Το γειτονικό βασίλειο μάς επιτίθεται.

# speaker:king
# pace:30
Ζήτησαν {ransomCostLabel} χρυσά νομίσματα για να σταματήσουν την εισβολή.

# speaker:king
# chain_next
# pace:30
# wait:500
Τι λες να κάνουμε;

* [Πλήρωσε {ransomCostLabel} χρυσά νομίσματα]
    -> pay_enemy

* { unitsCountFew > 3 } [Άμυνα με {unitsCountFew} μονάδες]
    -> send_few_units

* { unitsCountMany > 3 } [Άμυνα με {unitsCountMany} μονάδες]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Ας ελπίσουμε ότι θα δεχτούν την προσφορά μας.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Ας ελπίσουμε ότι φτάνουν.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Σίγουρα αυτό θ' αποκρούσει την επίθεσή τους.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Τουλάχιστον... δεν πέθανα φτωχός.

# speaker:king
# pace:60
# classes:victory
Συγχαρητήρια πάντως που τερμάτισες το παιχνίδι.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
ΣΚΟΤΩΣΕΣ ΤΟΝ ΠΑΤΕΡΑ ΜΟΥ!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
Όχι...

# speaker:developer
# pace:100
# classes:vader
Εγώ είμαι ο πατέρας σου!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Προγραμματιστή;

# speaker:princess
# pace:50
Έβαλες 2 αναφορές στον Πόλεμο των Άστρων μέσα στο παιχνίδι σου; Σοβαρά;!;

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Με βρήκες.

# speaker:king
# pace:32
Ναι, πήρα από τη φωλιά του δράκου. Χρυσάφι για το βασίλειο. Κι εκείνο το παιχνίδι για ενθύμιο.

# speaker:king
# pace:30
Ο λαός μας πέθαινε της πείνας. Θα το ξανάκανα.

# speaker:king
# pace:30
Πάρε ένα λάδωμα και σώπα, και φεύγουμε κι οι δυο μας καθαροί.

# speaker:king
# pace:30
Θα με προδώσεις ή θα δεχτείς το δώρο μου;

* [Πρέπει να σε σταματήσω!]
  -> go_against_king

* [Μ' αρέσει το χρυσάφι!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
Ας γίνει έτσι!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Πάρε τότε το μερίδιό σου.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Σου έδωσα ήδη χρυσάφι πέρα από τις πιο μεγάλες σου επιθυμίες.

# speaker:king
# pace:30
Αυτή ήταν η συμφωνία. Πάρ' το και φύγε.

* [Δεν με νοιάζει, πρέπει να σε σταματήσω]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
Ας γίνει έτσι!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Με το χρυσάφι μου αγόρασες τον στρατό που σκότωσε το παιδί του.

# speaker:king
# pace:32
Μην κάνεις τον αθώο.

# speaker:king
# pace:30
Έλα, λοιπόν.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Ώστε χρωστάς στο βασίλειο, ε; Μη σκας... η συντεχνία έχει ένα σωρό κορόιδα που μας χρωστάνε.


# speaker:rogue
# pace:40
# wait:400
Αν δεν πληρώσουν, σπάμε κανένα πόδι.

# speaker:rogue
# pace:30
# wait:400
Μέχρι να ισιώσεις τα χρέη σου, οι κλέφτες μου θα σου μαζεύουν χρυσάφι με διπλάσια όρεξη.

  -> END
"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Αλίμονο! Τα αποθέματά μας σε μάνα στέρεψαν.

# speaker:wizard_dialog
# pace:35
# wait:400
Δίχως την απόκρυφη ουσία, δεν μπορώ να διοχετεύσω τα ξόρκια μου στον δράκο.

# speaker:wizard_dialog
# pace:35
# wait:400
Πήγαινε στο μενού Αναβαθμίσεις και αγόρασε την [Αναπλήρωση Μάνα] όποτε στερεύουμε... για να χτυπήσουμε ξανά το θηρίο!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Είδε κανείς τον Βασιλιά; Έχει εξαφανιστεί.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
Τελευταία φορά τον είδαν να κατεβαίνει στα μπουντρούμια κάτω από το κάστρο.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Καλώς ήρθες!

# pace:45
Είμαι ο Μουκ, ο νέος και δίκαιος!

# pace:50
Ο Βασιλιάς μ' έβαλε εδώ για να μη χάνεσαι, και το εννοώ; μ' αρέσει να δείχνω τον δρόμο.

# pace:35
Δεν επιτρέπεται να φύγω απ' αυτό το πλακάκι. "Βοήθα κάθε ταξιδιώτη", και μετά "μην περνάς εκείνη τη γραμμή". Έλεγα στον εαυτό μου πως ήταν το πρωτόκολλο. Τελευταία... δεν είμαι και τόσο σίγουρος.

# pace:25
Πάρε πάντως αυτόν τον πυρσό. Η μία βοήθεια που μου επιτρέπεται ακόμη να δώσω πέρα απ' τη γραμμή.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Χαίρετε, είμαι ο Πάπας.

# speaker:pope
# pace:30
- Ήρθε η ώρα ν' αποδείξετε ξανά την πίστη σας και να συνεισφέρετε στην Εκκλησία μας.

# speaker:pope
# pace:30
- Χρειάζομαι {contributionCostLabel} χρυσά νομίσματα για να βοηθήσω τους φτωχούς.

* [Πλήρωσέ του {contributionCostLabel} χρυσά νομίσματα]
    -> pay_contribution

* [Άλλαξε θρήσκευμα]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Είθε η ψυχή σας ν' ανταμειφθεί στη μέλλουσα ζωή!

# speaker:pope
# pace:30
- Πάρτε αυτούς τους 100 ιερείς ως δείγμα ευγνωμοσύνης της Εκκλησίας.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Είθε η ψυχή σας να καταδικαστεί στη μέλλουσα ζωή!

# speaker:pope
# pace:30
# chain_next
# wait:500
- Επίσης...

# speaker:pope
# pace:30
- Θα ήταν κρίμα αν εκείνη η γιγάντια σαύρα θεραπευόταν από μια ανώτερη δύναμη...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(ήχοι θεραπείας\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Έχω τροφή, ξύλο ή μετάλλευμα να πουλήσω για

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
χρυσάφι. Ποιο θέλεις ν' αγοράσεις;

* { canAffordTrading > 0 } [{resourceAmountLabel} Τροφή]
    -> buy_food

* { canAffordTrading > 0 } [{resourceAmountLabel} Ξύλο]
    -> buy_wood

* { canAffordTrading > 0 } [{resourceAmountLabel} Μετάλλευμα ]
    -> buy_ore

* [Κανένα]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Ευχαριστώ, τα λέμε στο επόμενο πέρασμά μου.

  -> END


=== farewell ===

# speaker:salesman
Τα λέμε στο επόμενο πέρασμά μου.

* [Στο καλό]
    -> END

* [Να έρχεσαι πιο αραιά]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Κατάλαβα. Θ' αραιώσω τις επισκέψεις μου.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Πω πω, τα κατάφερες στ' αλήθεια!

# speaker:king
# pace:30
- Ευχαριστούμε πολύ που σκότωσες αυτόν τον δράκο. Είσαι ο ήρωάς μας!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Τώρα επιτέλους μπορούμε να...

# speaker:princess
# classes:scared
# pace:200
Τι ήταν αυτός ο ήχος;

# speaker:shadow
# pace:200
# classes:angry
ΣΚΟΤΩΣΕΣ ΤΟΝ ΓΙΟ ΜΟΥ!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Αυτός

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
ΝΑΙ ΠΟΥ ΕΙΝΑΙ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
Μεγάλος Δράκος!

# speaker:princess
# pace:20
# events:resume_game
Ωχ όχι, θα μας βοηθήσεις σε παρακαλώ;!;

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Ο Forth'aarh είναι νεκρός. Έκανες αυτό που δεν μπόρεσε κανένας στρατός.

# speaker:king
# pace:28
# classes:victory
Σ' ευχαριστούμε. Ειλικρινά.

# speaker:princess
# pace:30
# classes:victory
Ακολούθησέ με... Πρέπει να ετοιμαστούμε για όποιον νέο εχθρό μας βρει.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Πώς γύρισε;

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Δεν ξέρω πώς επέστρεψε.

# speaker:king
# pace:28
- Χρειάζεται όμως απίστευτη θέληση για να γυρίσει κανείς έτσι.

# speaker:princess
# pace:40
# classes:scared
- Και μια δίψα για κάποιου είδους εκδίκηση...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Ήξερες ότι κάθε φορά που μπαίνεις σε μπουντρούμι

# classes:angry-worker
# pace:30
- ΠΡΕΠΕΙ ΝΑ ΧΤΙΣΩ ΟΛΟΚΑΙΝΟΥΡΓΙΟ ΛΑΒΥΡΙΝΘΟ ΣΤΟ ΧΕΡΙ;!;

# chain_next
# pace:50
- Κουβαλούσαμε σεντούκια βδομάδες. Είπε να μη ρωτάμε από πού ήρθαν.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Επιτέλους!

# pace:40
- Ο βασιλιάς είπε ότι τελείωσα και θα του δώσω την αξίνα μόλις τελειώσω αυτό το επίπεδο.

  -> END
"""

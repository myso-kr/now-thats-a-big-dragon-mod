# -*- coding: utf-8 -*-
"""Writes the Italian .ink dialogues.

Only spoken lines and bracketed choice labels are translated; directives, ink
structure and every {interpolation} are the game's own.

Address: informal "tu" throughout, which is what Italian game dialogue uses. The King
is formal in tone but still speaks to the hero directly.

The game's own font has à è é ì ò ù but no «», em dash or curly apostrophe, so the
accents are real and the quotes are straight.
"""

F = {}

F["apprenticeships_unlock.ink"] = r"""# speaker:engineer
# pace:30
# events:show_apprenticeships
Sembra che ti serva una mano a produrre più risorse...

# speaker:engineer
# events:schedule_trading,resume_dialogs_timer
Prova a comprare degli Apprendistati per avere più contadini, minatori e boscaioli.
  -> END
"""

F["catapult.ink"] = r"""VAR choosesRock = false
VAR catapultCost = 1
VAR catapultCostLabel = "1"

# speaker:engineer
# chain_next
# wait:500
Ci rivediamo!

# speaker:engineer
Abbiamo continuato la ricerca sulla tua macchina d'assedio.

# speaker:engineer
# wait:300
# pace:30
Ora può lanciare gatti contro i nemici, e crediamo che possa cambiare le sorti dello scontro.

# speaker:engineer
# wait:300
# pace:30
# chain_next
La chiamiamo "Gatta-pulta"

# speaker:engineer
# wait:300
# pace:300
(pausa drammatica)

# speaker:engineer
# pace:30
Vuoi investire nella modifica, per questa e per le prossime?

* [Preferisco continuare a lanciare massi]
    -> no_thanks

* [Paga {catapultCostLabel} d'oro]
    -> pay_for_catapult_with_cats


=== pay_for_catapult_with_cats ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer,shoot_cats
Facci sapere che te ne pare!

  -> END

=== pay_for_catapult ===

# speaker:engineer
# pace:30
# events:pay_for_catapult,resume_dialogs_timer
Facci sapere che te ne pare!

  -> END

=== no_thanks ===

# speaker:engineer
# pace:30
# events:resume_dialogs_timer
Peccato. In bocca al lupo lo stesso.

  -> END
"""

F["coup_de_grace.ink"] = r"""# speaker:king
# pace:30
- Le tue truppe ti hanno lasciato l'ultimo colpo.

# speaker:king
# pace:30
- È la tua occasione per finirlo una volta per tutte!

  -> END
"""

F["dummy.ink"] = r"""# speaker:princess
# pace:30
Il Re ti ha chiesto di continuare ad allenarti, casomai arrivasse qualcosa di più grosso.

# speaker:princess
# pace:20
# events:dummy_funding
# classes:victory
Stavolta vuole persino finanziare il tuo esercito, così potrai formarlo a modo tuo.

# speaker:princess
# pace:40
# chain_next
# wait:500
Ma quando io, qualche mese fa, ho chiesto una festa di compleanno enorme,

# speaker:princess
# pace:40
# chain_next
# wait:500
è stato solo...

# speaker:princess
# pace:60
# classes:imitating
"Bla, bla, bla, il regno non ha soldi, figlia mia!"


# speaker:princess
# pace:37
Però questo manichino ha un aspetto strano...


  -> END
"""

F["dummy_death.ink"] = r"""# speaker:princess
# pace:30
Cosa? Non pensavo si potesse sconfiggere.

# speaker:princess
# pace:20
# classes:love
Ma c'è qualcosa che il mio eroe non riesca a sconfiggere?

# speaker:princess
# events:whistle
# pace:50
Cosa, cos'è quello lassù?

  -> END
"""

F["dummy_toy.ink"] = r"""# speaker:princess
# pace:30
Quello non è un semplice manichino da allenamento.

# speaker:princess
# pace:30
Sembra un giocattolo magico. Per qualcosa di molto più grande di noi.

  -> END
"""

F["dungeon_keys.ink"] = r"""# speaker:rogue
# pace:30
Ehi, tu, laggiù...

# speaker:rogue
# pace:30
# wait:500
# events:give_keys
Ho trovato queste chiavi del sotterraneo segreto sotto il castello.

# speaker:rogue
# pace:30
# wait:500
Chissà se il Re ne conosce l'esistenza.

# speaker:rogue
# pace:10
# chain_next
# wait:500
Comunque sia...

# speaker:rogue
# pace:30
Nelle mie incursioni ho tirato su un bel bottino, ma l'ultima volta la torcia si è quasi spenta.

# speaker:rogue
# wait:500
Ho paura di rientrare e perdermi al buio, così ti do tutte le chiavi gratis.

# speaker:rogue
# pace:100
# chain_next
# wait: 300
Buona fortuna,

# speaker:rogue
# pace:100
# events:end_give_keys
e mi raccomando, sta' attento.

  -> END
"""

F["dungeon_rescue.ink"] = r"""# pace:35
# chain_next
Ehi! Sono lo sviluppatore.

# pace:40
Scusa se sei finito dentro un muro. È un bug mio.

# pace:30
Ti tiro fuori dal vuoto e terrai tutto il bottino.

* [Arrenditi e tieni il bottino]
  -> confirm_give_up

=== confirm_give_up ===

# pace:10
# events:dungeon_stuck_give_up
Ciao!
  -> END
"""

F["engineer.ink"] = r"""# speaker:engineer
# chain_next
# wait:500
Salve, eroe!

# speaker:engineer
# pace:30
# events:show_engineering_tab
Per aiutare nella battaglia, Sua Maestà ha ordinato all'Ordine degli Architetti e Ingegneri della Corona di offrire la nostra competenza.

# speaker:engineer
# pace:30
Ti aiuteremo in tre modi:

# speaker:engineer
# pace:30
- Costruendo catapulte per l'assedio.

# speaker:engineer
# pace:30
- Erigendo edifici di secondo livello, con i nostri costruttori.

# speaker:engineer
# pace:30
- Fondando organizzazioni di livello superiore, con i nostri ingegneri.

# speaker:engineer
# pace:30
Quando avrai l'oro, ci trovi nella scheda "Ingegneria".

  -> END
"""

F["fire_units_reveal.ink"] = r"""# speaker:king
# pace:35
Oh, e cosa pensavi volesse dire "licenziare le unità"?

  -> END
"""

F["ghost_king_annoyed.ink"] = r"""# speaker:ghost_king
# pace:50
Uccidermi non ti è bastato? Smettila di tormentarmi, ti prego!

-> END
"""

F["infinite.ink"] = r"""# pace:80
# classes:angry
Cip cip, brutto f******!

-> END"""

F["inspiration_ready.ink"] = r"""# speaker:bard_dialog
# pace:35
# wait:400
Sono pronto a suonare per le tue truppe e a ispirarle ad amplificare i loro poteri.

# speaker:bard_dialog
# pace:35
# wait:400
Premi il pulsante con l'arpa e goditi l'aumento temporaneo di potenza!

  -> END
"""

F["intro.ink"] = r"""# speaker:king
# chain_next
# pace:25
# wait:800
Aiuto!

# speaker:king
# chain_next
# pace:30
# wait:500
Un drago gigante sta distruggendo il nostro villaggio!

# speaker:king
# wait:300
# pace:30
- Ci serve un eroe che ci salvi.

# speaker:king
# pace:30
- Ti prego, uccidi questo drago con la tua possente spada, cioè con il cursore del mouse.

# speaker:king
# pace:30
- E se avrai oro a sufficienza, potrai reclutare qualche aiuto.

# speaker:king
# pace:30
- Buona fortuna!

  -> END
"""

F["intro_newGamePlus.ink"] = r"""# speaker:king
# pace:30
# wait:500
In qualche modo, Forth'aarh è tornato!

# speaker:king
# pace:30
# wait:400
Ma hai congedato le tue truppe. Ora dovrai reclutarne di nuove.

# speaker:king
# wait:300
# pace:30
- E l'attacco precedente ha rovinato la nostra economia, quindi non posso mantenere il tuo esercito.

# speaker:king
# pace:40
# chain_next
- D'ora in poi consumeranno

# speaker:king
# pace:150
# chain_next
# classes:highlight-text
# wait:300
- cibo, legname e minerale.

# speaker:king
# pace:40
- Dovrai gestire bene le tue risorse.

# speaker:king
# pace:40
- Decidi di volta in volta quali unità devono consumare risorse e quali no.

# speaker:king
# pace:40
- Oppure "licenziane" qualcuna: consumeranno meno, ma faranno comunque qualcosa.

# speaker:king
# pace:28
- Buona fortuna!

  -> END
"""

F["invasion_end.ink"] = r"""VAR strategyChoice = ""

{strategyChoice == "send_few_units": -> send_few_units }
{strategyChoice == "send_many_units": -> send_many_units }

=== send_few_units ===

# speaker:king
# pace:20
Purtroppo le nostre unità non sono bastate a respingere l'invasione.

# speaker:king
# pace:20
# events:resume_dialogs_timer
Le abbiamo perse tutte e, con esse, anche la somma del riscatto.
  -> END

=== send_many_units ===

# speaker:king
# pace:30
Le truppe sono tornate con ottime notizie!

# speaker:king
# pace:30
Sono riuscite a respingere l'invasione con perdite minime.

# speaker:king
# pace:30
# events:resume_dialogs_timer
Le riaccogliamo (per tornare a macinare contro il drago...)

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
Il regno vicino ci sta attaccando.

# speaker:king
# pace:30
Chiedono {ransomCostLabel} monete d'oro per fermare l'invasione.

# speaker:king
# chain_next
# pace:30
# wait:500
Secondo te cosa dovremmo fare?

* [Paga {ransomCostLabel} monete d'oro]
    -> pay_enemy

* { unitsCountFew > 3 } [Difendi con {unitsCountFew} unità]
    -> send_few_units

* { unitsCountMany > 3 } [Difendi con {unitsCountMany} unità]
    -> send_many_units


=== pay_enemy ===

# speaker:king
# pace:30
# events:pay_enemy,resume_dialogs_timer
- Speriamo che accettino la nostra offerta.
~ strategyChoice = "pay_enemy"

  -> END

=== send_few_units ===

# speaker:king
# pace:30
# events:send_few_units,resume_dialogs_timer
- Speriamo che basti.
~ strategyChoice = "send_few_units"

  -> END

=== send_many_units ===

# speaker:king
# pace:30
# events:send_many_units,resume_dialogs_timer
- Con questi respingeremo di certo il loro attacco.
~ strategyChoice = "send_many_units"

  -> END
"""

F["king_death.ink"] = r"""# speaker:king
# pace:120
Almeno... non sono morto povero.

# speaker:king
# pace:60
# classes:victory
Comunque, complimenti per aver finito il gioco.

# speaker:king
# events:sigh
# pace:200
...

# speaker:princess
# pace:50
# classes:angry
HAI UCCISO MIO PADRE!!!

# speaker:developer
# pace:100
# events:vader
# classes:vader
# wait:600
# chain_next
No...

# speaker:developer
# pace:100
# classes:vader
Io sono tuo padre!

# speaker:princess
# pace:150
...

# speaker:princess
# pace:50
# chain_next
# wait:500
Sviluppatore?

# speaker:princess
# pace:50
Hai messo due riferimenti a Star Wars nel tuo gioco? Davvero?!?

# events:return_to_infinite
# pace:40
# classes:vader
...


  -> END
"""

F["king_dungeon.ink"] = r"""# speaker:king
# pace:40
Mi hai trovato.

# speaker:king
# pace:32
Sì, l'ho preso dalla tana del drago. L'oro per il regno. Il giocattolo come ricordo.

# speaker:king
# pace:30
La nostra gente moriva di fame. Lo rifarei.

# speaker:king
# pace:30
Prendi una bustarella e taci, e ne usciremo entrambi puliti.

# speaker:king
# pace:30
Mi tradisci o accetti il mio dono?

* [Bisogna fermarti!]
  -> go_against_king

* [L'oro mi piace eccome!]
  -> take_bribe


=== go_against_king ===

# speaker:king
# events:start_king_battle
E così sia!

  -> END

=== take_bribe ===

# speaker:king
# events:take_bribe
Allora prendi la tua parte.

  -> END
"""

F["king_dungeon_2.ink"] = r"""# speaker:king
# pace:32
Ti ho già dato più oro di quanto tu abbia mai desiderato.

# speaker:king
# pace:30
Era questo il patto. Prendilo e vattene.

* [Non mi interessa, bisogna fermarti]
  -> go_against_king


=== go_against_king ===

# speaker:king
# events:start_king_battle
E così sia!

  -> END
"""

F["king_level_intro.ink"] = r"""# speaker:king
# pace:35
Col mio oro hai comprato l'esercito che ha ucciso suo figlio.

# speaker:king
# pace:32
Non fingerti innocente.

# speaker:king
# pace:30
Vieni, allora.

  -> END
"""

F["mafia.ink"] = r"""# speaker:rogue
# pace:30
Quindi ti sei indebitato con il regno, eh? Tranquillo... la gilda ha un sacco di polli che ci devono dei soldi.


# speaker:rogue
# pace:40
# wait:400
Se non pagano, spezziamo qualche gamba.

# speaker:rogue
# pace:30
# wait:400
Finché non torni in attivo, i miei ladri raccoglieranno oro per te il doppio più in fretta.

  -> END"""

F["mana_out.ink"] = r"""# speaker:wizard_dialog
# pace:35
Ahimè! Le nostre riserve di mana si sono esaurite.

# speaker:wizard_dialog
# pace:35
# wait:400
Senza l'essenza arcana non posso incanalare i miei incantesimi contro il drago.

# speaker:wizard_dialog
# pace:35
# wait:400
Vai al menu dei potenziamenti e compra "Ricarica mana" ogni volta che restiamo a secco... così potremo colpire di nuovo la bestia!

  -> END
"""

F["missing_king.ink"] = r"""# speaker:princess
# pace:30
Qualcuno ha visto il Re? È scomparso.

# speaker:princess
# pace:30
# wait:500
# events:resume_dialogs_timer
L'ultima volta che l'hanno visto stava scendendo nei sotterranei sotto il castello.

-> END
"""

F["mookie.ink"] = r"""# pace:35
# chain_next
Benvenuto!

# pace:45
Sono Mook, il giovane e giusto!

# pace:50
Il Re mi ha messo qui perché tu non ti perda, e dico sul serio: mi piace indicare la strada.

# pace:35
Non posso uscire da questa mattonella. "Aiuta ogni viandante", e poi "non oltrepassare quella linea". Mi dicevo che era il regolamento. Ultimamente... non ne sono più tanto sicuro.

# pace:25
Ma tieni, prendi questa torcia. È l'unico aiuto che mi è ancora concesso passare oltre la linea.
  -> END
"""

F["pope_visit.ink"] = r"""VAR contributionCostLabel = "1"

# speaker:pope
# pace:20
# wait:800
- Salute a te, sono il Papa.

# speaker:pope
# pace:30
- È tempo di dimostrare ancora una volta la tua fede e contribuire alla nostra Chiesa.

# speaker:pope
# pace:30
- Mi servono {contributionCostLabel} monete d'oro per aiutare i poveri.

* [Dagli {contributionCostLabel} monete d'oro]
    -> pay_contribution

* [Cambia religione]
    -> dont_pay


=== pay_contribution ===

# speaker:pope
# pace:30
# events:pay_contribution,resume_dialogs_timer
- Che la tua anima sia ricompensata nell'aldilà!

# speaker:pope
# pace:30
- Prendi questi 100 chierici come segno della gratitudine della Chiesa.

  -> END

=== dont_pay ===

# speaker:pope
# pace:30
- Che la tua anima sia dannata nell'aldilà!

# speaker:pope
# pace:30
# chain_next
# wait:500
- E poi...

# speaker:pope
# pace:30
- Sarebbe un peccato se quel lucertolone venisse guarito da un potere superiore...

# speaker:pope
# pace:100
# events:pope_heal_dragon,resume_dialogs_timer
- \(rumori di guarigione\)

  -> END
"""

F["trading.ink"] = r"""VAR tradingCost = 1
VAR tradingCostLabel = "1"
VAR resourceAmountLabel = "1"
VAR canAffordTrading = -1

# speaker:salesman
# pace:30
# chain_next
Ho cibo, legname o minerale da vendere per

# speaker:salesman
# pace:30
# classes:highlight-text
# chain_next
{tradingCostLabel}

# speaker:salesman
# pace:30
d'oro. Quale vuoi?

* { canAffordTrading > 0 } [Cibo: {resourceAmountLabel}]
    -> buy_food

* { canAffordTrading > 0 } [Legname: {resourceAmountLabel}]
    -> buy_wood

* { canAffordTrading > 0 } [Minerale: {resourceAmountLabel}]
    -> buy_ore

* [Niente]
    -> farewell


=== buy_food ===

# speaker:salesman
# pace:30
# events:buy_trading_food,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== buy_wood ===

# speaker:salesman
# pace:30
# events:buy_trading_wood,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== buy_ore ===

# speaker:salesman
# pace:30
# events:buy_trading_ore,resume_dialogs_timer
Grazie, ci vediamo al prossimo giro.

  -> END


=== farewell ===

# speaker:salesman
Ci vediamo al prossimo giro.

* [Addio]
    -> END

* [Passa più di rado]
    -> farewell_come_less_often


=== farewell_come_less_often ===

# speaker:salesman
# pace:30
# events:trading_come_less_often,resume_dialogs_timer
Capito. Dirado le visite.

  -> END
"""

F["victory.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Wow, ce l'hai fatta davvero!

# speaker:king
# pace:30
- Grazie di cuore per aver ucciso quel drago. Sei il nostro eroe!

# speaker:king
# chain_next
# wait:300
# event:bigger_dragon
Finalmente possiamo...

# speaker:princess
# classes:scared
# pace:200
Cos'era quel rumore?

# speaker:shadow
# pace:200
# classes:angry
AVETE UCCISO MIO FIGLIO!!!

# speaker:king
# chain_next
# wait:300
# pace:150
# classes:text-shadow
Questo

# speaker:king
# chain_next
# classes:big-text
# pace:250
# event:thats
SÌ

# speaker:king
# wait:300
# pace:150
# classes:text-shadow
che è un drago grosso!

# speaker:princess
# pace:20
# events:resume_game
Oh no, ci aiuterai, vero?!?

-> END
"""

F["victory_main.ink"] = r"""# speaker:princess
# pace:30
- Forth'aarh è morto. Hai fatto ciò che nessun esercito è riuscito a fare.

# speaker:king
# pace:28
# classes:victory
Grazie. Davvero.

# speaker:princess
# pace:30
# classes:victory
Seguimi... Dobbiamo prepararci ai nuovi nemici che potrebbero arrivare.

  -> END
"""

F["victory_plus.ink"] = r"""# speaker:princess
# pace:30
# classes:victory
Come ha fatto a tornare?

# speaker:princess
# pace:300
# classes:victory
.  .  .

# speaker:king
# pace:30
- Non so come sia tornato.

# speaker:king
# pace:28
- Ma per rialzarsi così serve una volontà straordinaria.

# speaker:princess
# pace:40
# classes:scared
- E anche una gran voglia di vendetta...

  -> END
"""

F["worker.ink"] = r"""# chain_next
# pace:50
# wait:300
Lo sapevi che ogni volta che entri in un sotterraneo

# classes:angry-worker
# pace:30
- DEVO COSTRUIRE UN LABIRINTO NUOVO A MANO?!?

# chain_next
# pace:50
- Abbiamo portato su forzieri per settimane. Ha detto di non chiedere da dove venissero.

  -> END
"""

F["worker_final.ink"] = r"""# wait:300
Finalmente!

# pace:40
- Il re ha detto che ho finito e che posso ridargli il piccone appena completo questo livello.

  -> END
"""

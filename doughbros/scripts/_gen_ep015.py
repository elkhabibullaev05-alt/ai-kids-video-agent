"""Generator for EP15 (Storm night, Gulpzilla). Run: python3 scripts/_gen_ep015.py"""
import json, os

D = os.path.dirname(os.path.abspath(__file__))


def L(who, en, es, de, fr, it, pt, **kw):
    b = {"say": who, "en": en, "es": es, "de": de, "fr": fr, "it": it, "pt": pt}
    b.update(kw)
    return b


def mv(who, to, speed="run", **kw):
    b = {"move": who, "to": to, "speed": speed}; b.update(kw); return b


def act(who, do, **kw):
    b = {"act": who if isinstance(who, list) else [who], "do": do}; b.update(kw); return b


def mood(who, is_, **kw):
    b = {"mood": who if isinstance(who, list) else [who], "is": is_}; b.update(kw); return b


def V(what, **kw):
    b = {"villain": what}; b.update(kw); return b


def F(**kw):
    b = {"flash": 1}; b.update(kw); return b


A = True
ALL5 = ["bup", "pim", "zeek", "lolly", "crispy"]

long_scenes = [
    # 1 cold open: attic, lightning, Gulpzilla
    {"bg": "attic", "music": "heartbeat", "heroes": {"bup": 330, "pim": 560, "zeek": 790, "lolly": 1010},
     "moods": {"pim": "scared"}, "villain": {"type": "vacuum", "x": 1500, "state": "awake", "scale": 0.9}, "tail": 0.1,
     "beats": [
         V("lunge", to=1250),
         L("villain", "MINE! Every crumb is MINE!", "¡MÍO! ¡Cada miga es MÍA!", "MEINS! Jeder Krümel ist MEINS!",
           "À MOI ! Chaque miette est À MOI !", "MIO! Ogni briciola è MIA!", "MEU! Cada migalha é MINHA!", and_=1),
         act(["bup", "pim", "zeek", "lolly"], "jump", and_=1), mood(["bup", "zeek", "lolly"], "scared", and_=1),
         act("pim", "scream"), {"shake": 0.8, "power": 30, "and": A}, F(and_=1),
         L("narr", "A thunderstorm. The lights are out. And the attic is NOT empty.",
           "Una tormenta. Sin luz. Y el ático NO está vacío.",
           "Ein Gewitter. Kein Licht. Und der Dachboden ist NICHT leer.",
           "Un orage. Plus de lumière. Et le grenier n'est PAS vide.",
           "Un temporale. Niente luce. E la soffitta NON è vuota.",
           "Uma tempestade. Sem luz. E o sótão NÃO está vazio."),
         F(),
         L("bup", "Team! Down the stairs! GO GO GO!", "¡Equipo! ¡Escaleras abajo! ¡VAMOS!",
           "Team! Die Treppe runter! LOS LOS LOS!", "L'équipe ! Descendez ! VITE VITE !",
           "Squadra! Giù per le scale! VIA VIA!", "Equipe! Escada abaixo! VAI VAI VAI!"),
         mv("bup", "off_left", and_=1), mv("pim", "off_left", and_=1), mv("zeek", "off_left", and_=1),
         mv("lolly", "off_left", and_=1), V("lunge", to=900, and_=1),
     ]},
    # 2 pantry hideout
    {"bg": "pantry", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 420, "pim": 640, "zeek": 880, "lolly": 1120, "crispy": 2200}, "moods": {"pim": "scared", "bup": "scared"}, "tail": 0.1,
     "beats": [
         act(["bup", "pim", "zeek", "lolly"], "shake"),
         L("zeek", "My calculations say the storm cut the power. He can't follow us!",
           "Mis cálculos dicen que la tormenta cortó la luz. ¡No puede seguirnos!",
           "Meine Berechnungen sagen: Der Sturm hat den Strom gekappt. Er kann uns nicht folgen!",
           "Mes calculs disent que l'orage a coupé le courant. Il ne peut pas nous suivre !",
           "I miei calcoli dicono che il temporale ha tolto la corrente. Non può seguirci!",
           "Meus cálculos dizem que a tempestade cortou a luz. Ele não pode seguir a gente!"),
         {"sfx": "rattle", "wait": 0.4},
         L("pim", "Th-then why do I still hear SLURPING?", "¿E-entonces por qué sigo oyendo SORBER?",
           "W-warum höre ich dann immer noch SCHLÜRFEN?", "A-alors pourquoi j'entends encore ASPIRER ?",
           "A-allora perché sento ancora RISUCCHIARE?", "E-então por que eu ainda ouço SUGANDO?"),
         mv("crispy", 1450, "walk", and_=0),
         L("crispy", "Batteries.", "Pilas.", "Batterien.", "Des piles.", "Le batterie.", "Pilhas."),
         act(["bup", "pim", "zeek", "lolly"], "jump", and_=1), {"sfx": "sting", "and": A},
         act("pim", "faint"),
         L("lolly", "Crispy! Stop appearing out of NOWHERE!", "¡Crispy! ¡Deja de aparecer de la NADA!",
           "Crispy! Hör auf, aus dem NICHTS aufzutauchen!", "Crispy ! Arrête de surgir de NULLE PART !",
           "Crispy! Smettila di spuntare dal NULLA!", "Crispy! Para de aparecer do NADA!"),
     ]},
    # 3 pantry: the plan
    {"bg": "pantry", "music": "drone", "cut": True,
     "heroes": {"bup": 420, "pim": 640, "zeek": 880, "lolly": 1120, "crispy": 1400}, "moods": {"pim": "scared"}, "tail": 0.1,
     "beats": [
         L("crispy", "Mr. Pot gave him a battery. It lasts until sunrise.",
           "Mr. Pot le dio una pila. Dura hasta el amanecer.",
           "Mr. Pot hat ihm eine Batterie gegeben. Sie hält bis Sonnenaufgang.",
           "Mr. Pot lui a donné une pile. Elle tient jusqu'à l'aube.",
           "Mr. Pot gli ha dato una batteria. Dura fino all'alba.",
           "O Mr. Pot deu uma pilha pra ele. Dura até o amanhecer."),
         L("crispy", "Only one thing stops him early. A bag so full... he BURPS.",
           "Solo una cosa lo detiene antes. Una bolsa tan llena... que ERUCTA.",
           "Nur eins stoppt ihn früher. Ein Beutel so voll... dass er RÜLPST.",
           "Une seule chose l'arrête avant. Un sac si plein... qu'il ROTE.",
           "Solo una cosa lo ferma prima. Un sacchetto così pieno... che RUTTA.",
           "Só uma coisa para ele antes. Um saco tão cheio... que ele ARROTA."),
         act("pim", "jump", and_=1),
         L("bup", "Sunrise is SIX hours away!", "¡Faltan SEIS horas para el amanecer!",
           "Bis Sonnenaufgang sind es SECHS Stunden!", "L'aube, c'est dans SIX heures !",
           "All'alba mancano SEI ore!", "Faltam SEIS horas pro amanhecer!"),
         act("bup", "shake", and_=1),
         act("zeek", "jump"),
         L("zeek", "Unless... we make him use his battery FASTER!",
           "A menos que... ¡le hagamos gastar la pila MÁS RÁPIDO!",
           "Außer... wir lassen ihn die Batterie SCHNELLER leer machen!",
           "Sauf si... on lui fait vider sa pile PLUS VITE !",
           "A meno che... non gli facciamo scaricare la batteria PIÙ IN FRETTA!",
           "A não ser que... a gente faça ele gastar a pilha MAIS RÁPIDO!"),
         mood("bup", "happy"),
         L("bup", "Okay team, here's the plan. We make him CHASE us. In circles.",
           "Bien, equipo, este es el plan. Hacemos que nos PERSIGA. En círculos.",
           "Okay Team, hier ist der Plan. Er soll uns JAGEN. Im Kreis.",
           "OK l'équipe, voilà le plan. Il nous POURSUIT. En rond.",
           "Ok squadra, ecco il piano. Ci facciamo INSEGUIRE. In tondo.",
           "Beleza, equipe, o plano é esse. Ele CORRE atrás da gente. Em círculos."),
         act(["bup", "zeek", "lolly"], "bounce"),
         L("pim", "N-n-nope! Circles make me dizzy!", "¡N-n-no! ¡Los círculos me marean!",
           "N-n-nein! Von Kreisen wird mir schwindlig!", "N-n-non ! Les cercles me donnent le tournis !",
           "N-n-no! I cerchi mi fanno girare la testa!", "N-n-não! Círculo me deixa tonto!"),
         act("pim", "spin", and_=1),
     ]},
    # 4 kitchen: Lolly bait
    {"bg": "kitchen", "music": "drone", "cut": True,
     "heroes": {"lolly": 700, "bup": -300, "zeek": -300}, "villain": {"type": "vacuum", "x": 1500, "state": "awake", "scale": 0.85},
     "tail": 0.1,
     "beats": [
         F(),
         L("lolly", "Yoo-hoo! Tasty crumbs over HERE, mister vacuum!",
           "¡Yu-ju! ¡Migas ricas por AQUÍ, señor aspiradora!",
           "Huhu! Leckere Krümel HIER drüben, Herr Staubsauger!",
           "Youhou ! Des bonnes miettes par ICI, monsieur l'aspirateur !",
           "Iuu-uu! Briciole buone QUI, signor aspirapolvere!",
           "Uhuu! Migalhas gostosas AQUI, seu aspirador!"),
         act("lolly", "bounce", and_=1),
         V("roar"),
         L("villain", "Crumbs?! MINE! *SLURP!*", "¿Migas? ¡MÍAS! *¡SLURP!*", "Krümel?! MEINS! *SCHLÜRF!*",
           "Des miettes ?! À MOI ! *SLURP !*", "Briciole?! MIE! *SLURP!*", "Migalhas?! MINHAS! *SLURP!*", and_=1),
         V("lunge", to=1000),
         mv("lolly", "off_left", and_=1), mood("lolly", "scared", and_=1),
         mv("bup", 500, and_=1),
         L("bup", "This way, dust-breath! Catch me if you can!",
           "¡Por aquí, aliento de polvo! ¡Atrápame si puedes!",
           "Hier lang, Staubatem! Fang mich doch!",
           "Par ici, haleine de poussière ! Attrape-moi si tu peux !",
           "Di qua, alito di polvere! Prendimi se ci riesci!",
           "Por aqui, bafo de poeira! Me pega se puder!"),
         mv("bup", "off_right"), V("lunge", to=1400, and_=1),
     ]},
    # 5 kitchen: chase loop, battery check
    {"bg": "kitchen", "music": "heartbeat", "cut": True,
     "heroes": {"zeek": 400, "pim": 650, "bup": -300}, "moods": {"pim": "scared"},
     "villain": {"type": "vacuum", "x": 1500, "state": "awake", "scale": 0.85}, "tail": 0.1,
     "beats": [
         mv("bup", 1000, and_=0), V("lunge", to=1250, and_=1),
         L("zeek", "Keep running! His battery is at... ninety-nine percent.",
           "¡Sigue corriendo! Su pila está al... noventa y nueve por ciento.",
           "Lauf weiter! Seine Batterie ist bei... neunundneunzig Prozent.",
           "Continue à courir ! Sa pile est à... quatre-vingt-dix-neuf pour cent.",
           "Continua a correre! La sua batteria è al... novantanove per cento.",
           "Continua correndo! A pilha dele está em... noventa e nove por cento."),
         L("bup", "NINETY-NINE?!", "¿¡NOVENTA Y NUEVE!?", "NEUNUNDNEUNZIG?!", "QUATRE-VINGT-DIX-NEUF ?!",
           "NOVANTANOVE?!", "NOVENTA E NOVE?!"),
         act("bup", "jump", and_=1), F(and_=1),
         V("roar"),
         act("pim", "faint", and_=1),
         L("narr", "Pim fainted. Again.", "Pim se desmayó. Otra vez.", "Pim fiel in Ohnmacht. Schon wieder.",
           "Pim s'est évanoui. Encore.", "Pim è svenuto. Di nuovo.", "O Pim desmaiou. De novo."),
         L("zeek", "Ninety-EIGHT! It's working! Slowly. Very... slowly.",
           "¡Noventa y OCHO! ¡Funciona! Despacio. Muy... despacio.",
           "Achtund-NEUNZIG! Es klappt! Langsam. Sehr... langsam.",
           "Quatre-vingt-DIX-HUIT ! Ça marche ! Lentement. Très... lentement.",
           "Novantotto! Funziona! Piano. Molto... piano.",
           "Noventa e OITO! Tá funcionando! Devagar. Bem... devagar."),
     ]},
    # 6 attic: Pim gets slurped
    {"bg": "attic", "music": "heartbeat", "cut": True,
     "heroes": {"pim": 900, "bup": 350, "lolly": 600}, "moods": {"pim": "scared", "bup": "scared", "lolly": "scared"},
     "villain": {"type": "vacuum", "x": 1500, "state": "awake", "scale": 0.9}, "tail": 0.1,
     "beats": [
         F(),
         L("villain", "Little red bean... come to Gulpzilla!", "Frijolito rojo... ¡ven con Gulpzilla!",
           "Kleine rote Bohne... komm zu Gulpzilla!", "Petit haricot rouge... viens voir Gulpzilla !",
           "Fagiolino rosso... vieni da Gulpzilla!", "Feijãozinho vermelho... vem pro Gulpzilla!", and_=1),
         V("lunge", to=1250, and_=1),
         L("pim", "N-n-nope! Not the dust bag! ANYTHING but the dust bag!",
           "¡N-n-no! ¡La bolsa de polvo no! ¡TODO menos la bolsa!",
           "N-n-nein! Nicht der Staubbeutel! ALLES, nur nicht der Staubbeutel!",
           "N-n-non ! Pas le sac à poussière ! TOUT sauf le sac !",
           "N-n-no! Non il sacchetto! TUTTO tranne il sacchetto!",
           "N-n-não! O saco de pó não! TUDO menos o saco!"),
         act("pim", "shake", and_=1),
         {"sfx": "whoosh", "and": A}, mv("pim", 1180, and_=1),
         act("pim", "hide"), {"sfx": "pop", "and": A}, {"shake": 0.6, "power": 26, "and": A},
         act(["bup", "lolly"], "scream"),
         L("bup", "He SLURPED Pim!", "¡Se SORBIÓ a Pim!", "Er hat Pim AUFGESAUGT!", "Il a ASPIRÉ Pim !",
           "Ha RISUCCHIATO Pim!", "Ele SUGOU o Pim!"),
     ]},
    # 7 attic: Lolly snaps
    {"bg": "attic", "music": "drone", "cut": True,
     "heroes": {"bup": 350, "lolly": 700}, "moods": {"lolly": "angry"},
     "villain": {"type": "vacuum", "x": 1450, "state": "awake", "scale": 0.9}, "tail": 0.1,
     "beats": [
         L("lolly", "Excuse me, mister Gulpzilla. Could you please give him back?",
           "Disculpe, señor Gulpzilla. ¿Podría devolverlo, por favor?",
           "Entschuldigung, Herr Gulpzilla. Könnten Sie ihn bitte zurückgeben?",
           "Excusez-moi, monsieur Gulpzilla. Vous pourriez le rendre, s'il vous plaît ?",
           "Mi scusi, signor Gulpzilla. Potrebbe ridarcelo, per favore?",
           "Com licença, seu Gulpzilla. Pode devolver ele, por favor?"),
         L("villain", "Finders keepers! MINE! *burp*", "¡El que lo encuentra se lo queda! ¡MÍO! *eructo*",
           "Wer's findet, dem gehört's! MEINS! *rülps*", "Qui trouve garde ! À MOI ! *rot*",
           "Chi trova tiene! MIO! *ruttino*", "Achado não é roubado! MEU! *arroto*"),
         act("lolly", "shake"), V("rage", level=0.4, and_=1),
         L("lolly", "Give. Him. BACK!", "¡Devuélvelo. AHORA!", "Gib. Ihn. ZURÜCK!", "Rends. Le. MOI !",
           "Ridammelo. SUBITO!", "Devolve. Ele. AGORA!"),
         mv("lolly", 1050, and_=1), {"shake": 0.9, "power": 34, "and": A}, F(and_=1),
         V("lunge", to=1650),
         L("bup", "Whoa. Remind me never to make Lolly angry.",
           "Uf. Recuérdenme nunca enfadar a Lolly.",
           "Wow. Erinnert mich daran, Lolly nie wütend zu machen.",
           "Ouah. Rappelez-moi de ne jamais énerver Lolly.",
           "Wow. Ricordatemi di non far mai arrabbiare Lolly.",
           "Uau. Me lembrem de nunca deixar a Lolly brava."),
     ]},
    # 8 inside the dust bag
    {"bg": "pantry", "music": "music_box", "cut": True,
     "heroes": {"pim": 700}, "moods": {"pim": "scared"}, "tail": 0.1,
     "beats": [
         {"card": "INSIDE THE DUST BAG...", "es": "DENTRO DE LA BOLSA DE POLVO...", "dur": 1.8},
         L("narr", "Inside the bag, it looked a lot like the pantry. Gulpzilla had swallowed half of it.",
           "Dentro de la bolsa parecía la despensa. Gulpzilla se había tragado la mitad.",
           "Im Beutel sah es aus wie die Speisekammer. Gulpzilla hatte die Hälfte verschluckt.",
           "Dans le sac, on aurait dit le garde-manger. Gulpzilla en avait avalé la moitié.",
           "Dentro il sacchetto sembrava la dispensa. Gulpzilla ne aveva ingoiato metà.",
           "Dentro do saco parecia a despensa. O Gulpzilla tinha engolido metade dela."),
         mv("pim", 950, "walk", and_=1),
         L("pim", "A b-button... a lost sock... and a... MAP?",
           "Un b-botón... un calcetín perdido... ¿y un... MAPA?",
           "Ein K-Knopf... eine verlorene Socke... und eine... KARTE?",
           "Un b-bouton... une chaussette perdue... et une... CARTE ?",
           "Un b-bottone... un calzino perso... e una... MAPPA?",
           "Um b-botão... uma meia perdida... e um... MAPA?"),
         act("pim", "jump"),
         L("pim", "'The Golden Crumb.' Signed... Mr. POT?!", "'La Miga Dorada.' Firmado... ¿¡Mr. POT!?",
           "'Der Goldene Krümel.' Unterschrift... Mr. POT?!", "'La Miette d'Or.' Signé... Mr. POT ?!",
           "'La Briciola d'Oro.' Firmato... Mr. POT?!", "'A Migalha Dourada.' Assinado... Mr. POT?!"),
         act("pim", "shake", and_=1), {"sfx": "sting", "and": A},
     ]},
    # 9 inside the bag: Pim's idea
    {"bg": "pantry", "music": "heartbeat", "cut": True,
     "heroes": {"pim": 950}, "moods": {"pim": "scared"}, "tail": 0.1,
     "beats": [
         {"sfx": "rattle", "wait": 0.3}, {"shake": 0.5, "power": 18, "and": A},
         L("pim", "Crispy said a FULL bag makes him burp. So I just have to make it fuller!",
           "Crispy dijo que una bolsa LLENA lo hace eructar. ¡Solo tengo que llenarla más!",
           "Crispy sagte, ein VOLLER Beutel lässt ihn rülpsen. Ich muss ihn nur voller machen!",
           "Crispy a dit qu'un sac PLEIN le fait roter. Je dois juste le remplir encore plus !",
           "Crispy ha detto che un sacchetto PIENO lo fa ruttare. Devo solo riempirlo di più!",
           "O Crispy disse que saco CHEIO faz ele arrotar. Só preciso encher mais!"),
         mood("pim", "happy"), act("pim", "bounce"),
         L("pim", "Bounce, bounce, BOUNCE! I'm brave! I'm... a little brave!",
           "¡Salta, salta, SALTA! ¡Soy valiente! Soy... un poco valiente.",
           "Hüpf, hüpf, HÜPF! Ich bin mutig! Ich bin... ein bisschen mutig!",
           "Saute, saute, SAUTE ! Je suis courageux ! Je suis... un peu courageux !",
           "Salta, salta, SALTA! Sono coraggioso! Sono... un pochino coraggioso!",
           "Pula, pula, PULA! Eu sou corajoso! Eu sou... meio corajoso!"),
         act("pim", "bounce", and_=1), {"sfx": "boing", "and": A},
         act("pim", "jump"), {"shake": 0.6, "power": 24, "and": A},
     ]},
    # 10 attic: outside, battery low, biggest slurp
    {"bg": "attic", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 330, "zeek": 560, "lolly": 790}, "moods": {"lolly": "angry"},
     "villain": {"type": "vacuum", "x": 1450, "state": "awake", "scale": 0.95}, "tail": 0.1,
     "beats": [
         V("rage", level=0.7), {"shake": 0.7, "power": 22, "and": A},
         L("zeek", "His bag is bulging! And the battery is at... TWO percent!",
           "¡Su bolsa está a reventar! Y la pila está al... ¡DOS por ciento!",
           "Sein Beutel platzt gleich! Und die Batterie ist bei... ZWEI Prozent!",
           "Son sac va exploser ! Et la pile est à... DEUX pour cent !",
           "Il sacchetto sta scoppiando! E la batteria è al... DUE per cento!",
           "O saco tá estufando! E a pilha está em... DOIS por cento!"),
         act("zeek", "jump", and_=1),
         L("bup", "One more slurp! Give him the BIGGEST thing up here!",
           "¡Un sorbo más! ¡Denle lo MÁS GRANDE de aquí!",
           "Noch ein Schlürfer! Gebt ihm das GRÖSSTE Ding hier oben!",
           "Encore une aspiration ! Donnez-lui le PLUS GROS truc d'ici !",
           "Un'altra risucchiata! Dategli la cosa PIÙ GRANDE quassù!",
           "Mais uma sugada! Deem pra ele a coisa MAIOR daqui!"),
         L("lolly", "Hey Gulpzilla! Bet you can't slurp this whole PILLOW!",
           "¡Oye Gulpzilla! ¡A que no puedes sorber esta ALMOHADA entera!",
           "Hey Gulpzilla! Wetten, du schaffst dieses ganze KISSEN nicht!",
           "Hé Gulpzilla ! Parie que tu n'aspires pas cet OREILLER entier !",
           "Ehi Gulpzilla! Scommetto che non riesci a risucchiare tutto questo CUSCINO!",
           "Ei Gulpzilla! Duvido você sugar esse TRAVESSEIRO inteiro!"),
         act("lolly", "bounce", and_=1),
         L("villain", "Nobody says can't to Gulpzilla! *SLUUURP!*", "¡Nadie le dice no puedes a Gulpzilla! *¡SLUUURP!*",
           "Niemand sagt 'schaffst du nicht' zu Gulpzilla! *SCHLUUURF!*",
           "Personne ne dit 'tu peux pas' à Gulpzilla ! *SLUUURP !*",
           "Nessuno dice 'non ci riesci' a Gulpzilla! *SLUUURP!*",
           "Ninguém diz 'duvido' pro Gulpzilla! *SLUUURP!*"),
         V("lunge", to=1150, and_=1), {"sfx": "whoosh", "and": A},
     ]},
    # 11 attic: the burp, Pim free
    {"bg": "attic", "music": "drone", "cut": True,
     "heroes": {"bup": 330, "zeek": 560, "lolly": 790, "pim": 1150}, "moods": {"pim": "happy"},
     "villain": {"type": "vacuum", "x": 1450, "state": "awake", "scale": 0.95}, "tail": 0.1,
     "beats": [
         act("pim", "hide"),
         L("villain", "Too... full... uh-oh...", "Demasiado... lleno... ay, no...", "Zu... voll... oh-oh...",
           "Trop... plein... oh oh...", "Troppo... pieno... oh-oh...", "Cheio... demais... ih..."),
         V("rage", level=1.0, and_=1), {"shake": 0.6, "power": 16, "and": A},
         {"sfx": "pop", "wait": 0.1}, {"shake": 1.0, "power": 40, "and": A}, F(thunder=False, and_=1),
         act("pim", "show"), mv("pim", 1000, and_=1), act("pim", "jump"),
         L("narr", "The biggest burp in the history of Table Land.",
           "El eructo más grande de la historia de Table Land.",
           "Der größte Rülpser in der Geschichte von Table Land.",
           "Le plus gros rot de l'histoire de Table Land.",
           "Il rutto più grande della storia di Table Land.",
           "O maior arroto da história de Table Land."),
         L("pim", "I'm OUT! And I've got Mr. Pot's MAP!", "¡Estoy FUERA! ¡Y tengo el MAPA de Mr. Pot!",
           "Ich bin DRAUSSEN! Und ich hab Mr. Pots KARTE!", "Je suis SORTI ! Et j'ai la CARTE de Mr. Pot !",
           "Sono FUORI! E ho la MAPPA di Mr. Pot!", "Eu SAÍ! E tô com o MAPA do Mr. Pot!"),
         mood(["bup", "zeek", "lolly"], "happy", and_=1), act(["bup", "zeek", "lolly", "pim"], "bounce", and_=1),
         L("villain", "Battery... low... still... mine... zzz.", "Pila... baja... sigue... siendo mío... zzz.",
           "Batterie... leer... trotzdem... meins... zzz.", "Pile... faible... quand même... à moi... zzz.",
           "Batteria... scarica... comunque... mio... zzz.", "Pilha... fraca... ainda... meu... zzz."),
         V("sleep", and_=1),
     ]},
    # 12 kitchen: the map
    {"bg": "kitchen", "music": "music_box", "cut": True,
     "heroes": {"bup": 330, "pim": 560, "zeek": 790, "lolly": 1020, "crispy": 1300}, "tail": 0.1,
     "beats": [
         F(thunder=False),
         L("crispy", "The Golden Crumb. Mr. Pot's oldest secret.", "La Miga Dorada. El secreto más antiguo de Mr. Pot.",
           "Der Goldene Krümel. Mr. Pots ältestes Geheimnis.", "La Miette d'Or. Le plus vieux secret de Mr. Pot.",
           "La Briciola d'Oro. Il segreto più antico di Mr. Pot.", "A Migalha Dourada. O segredo mais antigo do Mr. Pot."),
         L("zeek", "According to the map... it's hidden under the ice. In the FREEZER.",
           "Según el mapa... está escondida bajo el hielo. En el CONGELADOR.",
           "Laut Karte... liegt er unter dem Eis versteckt. Im GEFRIERSCHRANK.",
           "D'après la carte... elle est cachée sous la glace. Dans le CONGÉLATEUR.",
           "Secondo la mappa... è nascosta sotto il ghiaccio. Nel CONGELATORE.",
           "Segundo o mapa... está escondida debaixo do gelo. No CONGELADOR."),
         L("bup", "Then that's where we go next. Who's with me?", "Entonces allí vamos. ¿Quién viene conmigo?",
           "Dann gehen wir als Nächstes dahin. Wer ist dabei?", "Alors on y va. Qui vient avec moi ?",
           "Allora è lì che andiamo. Chi viene con me?", "Então é pra lá que a gente vai. Quem vem comigo?"),
         act(["bup", "zeek", "lolly"], "jump"),
         L("pim", "N-n-nope. But... okay. A little bit yes.", "N-n-no. Pero... vale. Un poquito sí.",
           "N-n-nein. Aber... okay. Ein bisschen ja.", "N-n-non. Mais... d'accord. Un petit peu oui.",
           "N-n-no. Però... va bene. Un pochino sì.", "N-n-não. Mas... tá. Um pouquinho sim."),
         act("pim", "bounce", and_=1),
     ]},
    # 13 freezer: cliffhanger
    {"bg": "freezer", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 380, "pim": 620}, "moods": {"pim": "scared"},
     "villain": {"type": "frost", "x": 1450, "state": "hidden", "scale": 0.9}, "tail": 2.8,
     "beats": [
         {"sfx": "ice", "wait": 0.6}, {"sfx": "creak", "wait": 0.6},
         L("pim", "B-Bup? Why is my breath making little clouds?", "¿B-Bup? ¿Por qué mi aliento hace nubecitas?",
           "B-Bup? Warum macht mein Atem kleine Wolken?", "B-Bup ? Pourquoi mon souffle fait des petits nuages ?",
           "B-Bup? Perché il mio respiro fa delle nuvolette?", "B-Bup? Por que meu bafo está fazendo nuvenzinhas?"),
         act("pim", "shake", and_=1),
         V("show"), {"sfx": "sting", "and": A}, act(["bup", "pim"], "jump", and_=1), mood("bup", "scared", and_=1),
         L("villain", "Stay... forever... COLD...", "Quedaos... para siempre... FRÍOS...", "Bleibt... für immer... KALT...",
           "Restez... pour toujours... GLACÉS...", "Restate... per sempre... GELATI...", "Fiquem... para sempre... GELADOS..."),
         V("lunge", to=1150, and_=1), {"shake": 0.8, "power": 30, "and": A},
         act("pim", "scream"),
     ]},
]


VAC = {"type": "vacuum", "x": 1500, "state": "awake", "scale": 0.85}
# extra scenes (inserted to reach ~4 min)
zeek_gadget = {"bg": "pantry", "music": "drone", "cut": True,
     "heroes": {"bup": 420, "pim": 640, "zeek": 880, "lolly": 1120, "crispy": 1400}, "moods": {"zeek": "happy"}, "tail": 0.1,
     "beats": [
         act("zeek", "bounce"),
         L("zeek", "Or... we use my Battery-Drainer 3000! One button, and his battery is EMPTY!",
           "O... ¡usamos mi Descargador 3000! ¡Un botón y su pila queda VACÍA!",
           "Oder... wir nehmen meinen Batterie-Leerer 3000! Ein Knopf, und seine Batterie ist LEER!",
           "Ou... on utilise mon Vide-Pile 3000 ! Un bouton, et sa pile est VIDE !",
           "Oppure... usiamo il mio Scarica-Batterie 3000! Un pulsante e la batteria è VUOTA!",
           "Ou... a gente usa meu Descarregador 3000! Um botão, e a pilha dele fica VAZIA!"),
         {"sfx": "clank", "wait": 0.3}, {"sfx": "ding", "wait": 0.4},
         {"sfx": "pop", "wait": 0.1}, act("zeek", "jump", and_=1), {"shake": 0.5, "power": 20, "and": A},
         mood("zeek", "scared"),
         L("zeek", "Hmm. It drained MY flashlight instead.", "Mmm. Descargó MI linterna en su lugar.",
           "Hm. Er hat stattdessen MEINE Taschenlampe geleert.", "Hum. Il a vidé MA lampe de poche à la place.",
           "Mmh. Ha scaricato la MIA torcia invece.", "Hmm. Ele descarregou a MINHA lanterna."),
         L("lolly", "Zeek. Sweetie. Please stop inventing things during emergencies.",
           "Zeek. Cariño. Por favor, deja de inventar cosas en emergencias.",
           "Zeek. Schätzchen. Bitte hör auf, in Notfällen Dinge zu erfinden.",
           "Zeek. Mon chou. Arrête d'inventer des trucs pendant les urgences.",
           "Zeek. Tesoro. Smettila di inventare cose durante le emergenze.",
           "Zeek. Querido. Para de inventar coisa em emergência, por favor."),
         act("lolly", "shake", and_=1),
         L("crispy", "Running it is, then.", "Entonces, a correr.", "Dann eben rennen.", "Alors on court.",
           "Allora si corre.", "Então é correr mesmo."),
     ]}

garden_chase = {"bg": "garden", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 450, "lolly": 700, "zeek": -300}, "moods": {"bup": "scared"},
     "villain": dict(VAC, x=1550), "tail": 0.1,
     "beats": [
         F(),
         L("narr", "Round and round they ran. Out the door. Into the storm.",
           "Corrieron en círculos. Por la puerta. Hacia la tormenta.",
           "Sie rannten im Kreis. Zur Tür hinaus. In den Sturm.",
           "Ils couraient en rond. Par la porte. Sous l'orage.",
           "Correvano in tondo. Fuori dalla porta. Dentro il temporale.",
           "Eles correram em círculos. Porta afora. Pra dentro da tempestade."),
         mv("bup", 300, and_=1), mv("lolly", 550, and_=1), V("lunge", to=1200, and_=1),
         L("villain", "Wet... crumbs... STILL MINE!", "Migas... mojadas... ¡SIGUEN SIENDO MÍAS!",
           "Nasse... Krümel... TROTZDEM MEINS!", "Miettes... mouillées... TOUJOURS À MOI !",
           "Briciole... bagnate... SEMPRE MIE!", "Migalhas... molhadas... AINDA MINHAS!"),
         V("rage", level=0.5, and_=1),
         mv("zeek", 850, and_=0), act("zeek", "jump"),
         L("zeek", "Ninety... FIVE! The mud is slowing his wheels!",
           "Noventa y... ¡CINCO! ¡El barro frena sus ruedas!",
           "Fünfund... NEUNZIG! Der Matsch bremst seine Räder!",
           "Quatre-vingt... QUINZE ! La boue freine ses roues !",
           "Novanta... CINQUE! Il fango rallenta le ruote!",
           "Noventa e... CINCO! A lama está travando as rodas dele!"),
         F(and_=1),
         L("bup", "Back inside! Up to the attic! Make him climb!",
           "¡Adentro! ¡Al ático! ¡Que tenga que subir!",
           "Wieder rein! Hoch auf den Dachboden! Er soll klettern!",
           "On rentre ! Au grenier ! Qu'il grimpe !",
           "Dentro! Su in soffitta! Fatelo arrampicare!",
           "Pra dentro! Pro sótão! Faz ele subir!"),
         mv("bup", "off_left", and_=1), mv("lolly", "off_left", and_=1), mv("zeek", "off_left", and_=1),
     ]}

crispy_save = {"bg": "kitchen", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 800, "crispy": -300}, "moods": {"bup": "scared"},
     "villain": dict(VAC, x=1450), "tail": 0.1,
     "beats": [
         V("lunge", to=1100), act("bup", "shake", and_=1),
         L("villain", "Stale bread! Crunchy and DUSTY! My favorite!", "¡Pan duro! ¡Crujiente y POLVORIENTO! ¡Mi favorito!",
           "Altes Brot! Knusprig und STAUBIG! Mein Lieblingsessen!", "Du pain rassis ! Croustillant et POUSSIÉREUX ! Mon préféré !",
           "Pane raffermo! Croccante e POLVEROSO! Il mio preferito!", "Pão velho! Crocante e EMPOEIRADO! Meu favorito!", and_=1),
         L("bup", "My foot's stuck! Somebody? ANYBODY?", "¡Mi pie está atascado! ¿Alguien? ¿¡QUIEN SEA!?",
           "Mein Fuß steckt fest! Irgendwer? IRGENDWER?", "Mon pied est coincé ! Quelqu'un ? N'IMPORTE QUI ?",
           "Ho il piede incastrato! Qualcuno? CHIUNQUE?", "Meu pé tá preso! Alguém? QUALQUER UM?"),
         mv("crispy", 600, "run"), {"sfx": "whoosh", "and": A},
         L("crispy", "Hey, dust-bag. I'm the crunchiest crumb in the house.",
           "Oye, bolsa de polvo. Soy la miga más crujiente de la casa.",
           "Hey, Staubbeutel. Ich bin der knusprigste Krümel im Haus.",
           "Hé, sac à poussière. Je suis la miette la plus croustillante de la maison.",
           "Ehi, sacco di polvere. Sono la briciola più croccante della casa.",
           "Ei, saco de pó. Eu sou a migalha mais crocante da casa."),
         V("roar"), mv("crispy", "off_left", and_=1), mv("bup", "off_left", and_=1), V("lunge", to=700, and_=1),
     ]}

rescue_talk = {"bg": "attic", "music": "drone", "cut": True,
     "heroes": {"bup": 350, "zeek": 600, "lolly": 850}, "moods": {"lolly": "angry"},
     "villain": dict(VAC, x=1550, scale=0.9), "tail": 0.1,
     "beats": [
         L("zeek", "We can't pull him out. The bag only opens from the INSIDE.",
           "No podemos sacarlo. La bolsa solo se abre desde DENTRO.",
           "Wir kriegen ihn nicht raus. Der Beutel geht nur von INNEN auf.",
           "On ne peut pas le sortir. Le sac ne s'ouvre que de L'INTÉRIEUR.",
           "Non possiamo tirarlo fuori. Il sacchetto si apre solo da DENTRO.",
           "A gente não consegue tirar ele. O saco só abre por DENTRO."),
         L("bup", "Then Pim has to save himself. Our Pim. Who faints at his own shadow.",
           "Entonces Pim tiene que salvarse solo. Nuestro Pim. Que se desmaya con su sombra.",
           "Dann muss Pim sich selbst retten. Unser Pim. Der vor seinem Schatten umkippt.",
           "Alors Pim doit se sauver tout seul. Notre Pim. Qui s'évanouit devant son ombre.",
           "Allora Pim deve salvarsi da solo. Il nostro Pim. Che sviene davanti alla sua ombra.",
           "Então o Pim tem que se salvar sozinho. Nosso Pim. Que desmaia com a própria sombra."),
         act("bup", "shake", and_=1),
         mood("lolly", "normal"),
         L("lolly", "He's braver than he thinks. PIM! You can DO it!",
           "Es más valiente de lo que cree. ¡PIM! ¡Tú PUEDES!",
           "Er ist mutiger, als er denkt. PIM! Du SCHAFFST das!",
           "Il est plus courageux qu'il ne le croit. PIM ! Tu PEUX le faire !",
           "È più coraggioso di quanto pensi. PIM! Ce la PUOI fare!",
           "Ele é mais corajoso do que pensa. PIM! Você CONSEGUE!"),
         act(["bup", "zeek", "lolly"], "jump", and_=1), F(thunder=True, and_=1),
     ]}

freezer_warn = {"bg": "kitchen", "music": "drone", "cut": True,
     "heroes": {"bup": 330, "pim": 560, "zeek": 790, "lolly": 1020, "crispy": 1300}, "tail": 0.1,
     "beats": [
         L("crispy", "Careful. The last dough who opened that freezer came back... very, very cold.",
           "Cuidado. La última masa que abrió ese congelador volvió... muy, muy fría.",
           "Vorsicht. Der letzte Teig, der den Gefrierschrank öffnete, kam... sehr, sehr kalt zurück.",
           "Attention. La dernière pâte qui a ouvert ce congélateur est revenue... très, très froide.",
           "Attenti. L'ultimo impasto che ha aperto quel congelatore è tornato... molto, molto freddo.",
           "Cuidado. A última massinha que abriu aquele congelador voltou... muito, muito gelada."),
         mood(["pim", "zeek"], "scared", and_=1), act("pim", "shake", and_=1),
         L("lolly", "Then we'll bring blankets. Lots of blankets.", "Entonces llevaremos mantas. Muchas mantas.",
           "Dann nehmen wir Decken mit. Viele Decken.", "Alors on prendra des couvertures. Plein de couvertures.",
           "Allora porteremo coperte. Tante coperte.", "Então a gente leva cobertor. Muitos cobertores."),
         act("lolly", "bounce", and_=1),
     ]}

pim_wakes = {"bg": "attic", "music": "heartbeat", "cut": True,
     "heroes": {"pim": 800}, "moods": {"pim": "scared"},
     "villain": {"type": "vacuum", "x": 1450, "state": "hidden", "scale": 0.9}, "tail": 0.1,
     "beats": [
         act("pim", "shake"),
         L("pim", "Wh-where am I? Guys? Why is it so QUIET?", "¿D-dónde estoy? ¿Chicos? ¿Por qué hay tanto SILENCIO?",
           "W-wo bin ich? Leute? Warum ist es so STILL?", "O-où je suis ? Les gars ? Pourquoi c'est si CALME ?",
           "D-dove sono? Ragazzi? Perché c'è così SILENZIO?", "O-onde eu tô? Gente? Por que tá tão QUIETO?"),
         {"sfx": "creak", "wait": 0.5},
         L("pim", "Okay. Nothing is behind me. Nothing is EVER behind me.",
           "Vale. No hay nada detrás de mí. NUNCA hay nada detrás de mí.",
           "Okay. Nichts ist hinter mir. NIE ist etwas hinter mir.",
           "D'accord. Il n'y a rien derrière moi. Il n'y a JAMAIS rien derrière moi.",
           "Ok. Non c'è niente dietro di me. Non c'è MAI niente dietro di me.",
           "Tá. Não tem nada atrás de mim. NUNCA tem nada atrás de mim."),
         F(), V("show", and_=1), V("lunge", to=1200, and_=1),
         L("villain", "Boo. *slurp*", "Bu. *slurp*", "Buh. *schlürf*", "Bouh. *slurp*", "Bu. *slurp*", "Bu. *slurp*", and_=1),
         act("pim", "scream"), {"shake": 0.8, "power": 30, "and": A},
     ]}

# order: 1 attic, 2 pantry, 3 plan, gadget, 4 lolly bait, 5 chase, crispy_save, garden, 6 slurp, 7 lolly snaps,
#        rescue_talk, 8 bag, 9 bag idea, 10 biggest slurp, 11 burp, 12 map, freezer_warn, 13 freezer
s = long_scenes
long_scenes = s[0:3] + [zeek_gadget] + s[3:5] + [crispy_save, garden_chase, pim_wakes] + s[5:7] + [rescue_talk] + s[7:12] + [freezer_warn] + s[12:]


def fix(o):
    if isinstance(o, list):
        return [fix(x) for x in o]
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            if k == "and_":
                if v:
                    r["and"] = True
                continue
            r[k] = fix(v)
        return r
    return o


LONG_TITLE = "It Got CLOSER With Every Flash?! ⚡ | EP 15"
long = {
    "id": "ep015_long", "format": "long", "title": LONG_TITLE,
    "hook": "IT'S IN THE ATTIC!", "hook_dur": 3.5,
    "description": ("A thunderstorm knocks the power out, and the Dough Bros hide in the attic... where Gulpzilla the "
                    "vacuum is waiting with a battery from Mr. Pot. The plan: make him chase them in circles until it dies. "
                    "But then Gulpzilla slurps Pim, and inside the dust bag Pim finds Mr. Pot's map to the Golden Crumb. "
                    "Can one tiny bean make a vacuum burp? And what is waiting in the freezer?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #gulpzilla"),
    "tags": ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "gulpzilla", "storm night", "vacuum monster", "pim", "lolly", "zeek", "crispy",
             "golden crumb"],
    "thumbnail": {"bg": "attic", "villain": "vacuum", "heroes": ["pim"], "text": "IT'S BEHIND YOU!"},
    "scenes": fix(long_scenes),
}

# ---------------- Short: Zeek's crumb decoy (loops) ----------------
SH = {"type": "vacuum", "x": 1250, "state": "awake", "scale": 0.85}
short_scenes = [
    {"bg": "attic", "music": "heartbeat", "heroes": {"zeek": 850}, "moods": {"zeek": "scared"},
     "villain": dict(SH), "tail": 0.05,
     "beats": [
         V("lunge", to=1080), act("zeek", "jump", and_=1), {"shake": 0.8, "power": 34, "and": A}, act("zeek", "shake", and_=1),
         L("villain", "A crunchy NERD! MINE!", "¡Un CEREBRITO crujiente! ¡MÍO!", "Ein knuspriger STREBER! MEINS!",
           "Un INTELLO croustillant ! À MOI !", "Un SECCHIONE croccante! MIO!", "Um NERD crocante! MEU!", and_=1),
         L("zeek", "Stay back! I have a GENIUS plan!", "¡Atrás! ¡Tengo un plan GENIAL!", "Bleib zurück! Ich hab einen GENIALEN Plan!",
           "Recule ! J'ai un plan GÉNIAL !", "Stai indietro! Ho un piano GENIALE!", "Para trás! Eu tenho um plano GENIAL!"),
     ]},
    {"bg": "kitchen", "music": "drone", "cut": True, "heroes": {"zeek": 600}, "moods": {"zeek": "happy"}, "tail": 0.05,
     "beats": [
         act("zeek", "bounce"),
         L("zeek", "A fake crumb! Vacuums can't resist crumbs.", "¡Una miga falsa! Las aspiradoras no resisten las migas.",
           "Ein falscher Krümel! Staubsauger können Krümeln nicht widerstehen.",
           "Une fausse miette ! Les aspirateurs adorent les miettes.",
           "Una briciola finta! Gli aspirapolvere non resistono alle briciole.",
           "Uma migalha falsa! Aspirador não resiste a migalha.", and_=1),
     ]},
    {"bg": "attic", "music": "heartbeat", "cut": True, "heroes": {"zeek": 650}, "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         {"sfx": "whoosh", "wait": 0.1}, mv("zeek", 800, "run", and_=1), F(and_=1),
         L("zeek", "Throw it... NOW!", "Lánzala... ¡YA!", "Werfen... JETZT!", "Je la lance... MAINTENANT !",
           "La lancio... ORA!", "Joga... AGORA!", and_=1),
         V("roar"), {"shake": 0.7, "power": 26, "and": A},
     ]},
    {"bg": "attic", "music": "heartbeat", "cut": True, "heroes": {"zeek": 750}, "moods": {"zeek": "scared"},
     "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         V("lunge", to=1100), {"sfx": "pop", "and": A}, act("zeek", "spin", and_=1),
         L("villain", "Mmm... crunchy GLASSES! MINE!", "Mmm... ¡GAFAS crujientes! ¡MÍAS!", "Mmm... knusprige BRILLE! MEINS!",
           "Mmm... des LUNETTES croustillantes ! À MOI !", "Mmm... OCCHIALI croccanti! MIEI!",
           "Hmm... ÓCULOS crocantes! MEUS!", and_=1),
     ]},
    {"bg": "attic", "music": "heartbeat", "cut": True, "heroes": {"zeek": 700}, "moods": {"zeek": "scared"},
     "villain": dict(SH, x=1200), "tail": 0.05,
     "beats": [
         act("zeek", "shake"),
         L("zeek", "My glasses! I threw my GLASSES! Where's the crumb?!", "¡Mis gafas! ¡Lancé mis GAFAS! ¿¡Y la miga!?",
           "Meine Brille! Ich hab meine BRILLE geworfen! Wo ist der Krümel?!",
           "Mes lunettes ! J'ai lancé mes LUNETTES ! Où est la miette ?!",
           "I miei occhiali! Ho lanciato gli OCCHIALI! Dov'è la briciola?!",
           "Meus óculos! Eu joguei meus ÓCULOS! Cadê a migalha?!", and_=1),
     ]},
    {"bg": "kitchen", "music": "drone", "cut": True, "heroes": {"zeek": 600, "pim": 900}, "moods": {"pim": "scared"},
     "tail": 0.05,
     "beats": [
         act("pim", "jump"),
         L("pim", "Z-Zeek... you're holding it. And that's not a crumb. That's ME.",
           "Z-Zeek... la tienes en la mano. Y eso no es una miga. Soy YO.",
           "Z-Zeek... du hältst ihn noch. Und das ist kein Krümel. Das bin ICH.",
           "Z-Zeek... tu la tiens encore. Et ce n'est pas une miette. C'est MOI.",
           "Z-Zeek... ce l'hai in mano. E quella non è una briciola. Sono IO.",
           "Z-Zeek... tá na sua mão. E isso não é migalha. Sou EU.", and_=1),
         act("zeek", "faint"),
     ]},
    {"bg": "attic", "music": "heartbeat", "cut": True, "heroes": {"zeek": 850}, "moods": {"zeek": "scared"},
     "villain": dict(SH), "tail": 0.05,
     "beats": [
         V("lunge", to=1080), {"shake": 0.8, "power": 34, "and": A},
         L("villain", "More snacks?! MINE!", "¿¡Más comida!? ¡MÍA!", "Noch mehr Snacks?! MEINS!", "Encore à manger ?! À MOI !",
           "Altri spuntini?! MIEI!", "Mais lanche?! MEU!", and_=1),
         act("zeek", "jump", and_=1),
     ]},
]
SHORT_TITLE = "Zeek Threw His GLASSES at a Vacuum?! 🤓 #shorts"
short = {
    "id": "ep015_short1", "format": "short", "title": SHORT_TITLE, "hook": "ZEEK'S GENIUS PLAN?!",
    "description": ("Zeek has a genius plan to stop Gulpzilla: a fake crumb. What could go wrong? "
                    'Full episode: "' + LONG_TITLE.replace(" ⚡", "") + '" {LONG_URL} — more on https://www.youtube.com/@DoughBrosTV '
                    "#shorts #animation #cartoon #doughbros #funnycartoon"),
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "zeek", "gulpzilla", "vacuum monster", "storm night"],
    "thumbnail": {"bg": "attic", "villain": "vacuum", "heroes": ["zeek"], "text": "WRONG THROW!"},
    "scenes": fix(short_scenes),
}

for s in (long, short):
    json.dump(s, open(os.path.join(D, s["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print("wrote", s["id"])

"""Builds the EP9 pack (1 long + 1 short). Run: python3 scripts/_build_ep009.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
src = (OUT / "_build_ep003.py").read_text(encoding="utf-8").split("ALL4 =")[0]
ns = {"__file__": str(OUT / "_build_ep003.py")}
exec(src, ns)
S, _mv, act, mood = ns["S"], ns["mv"], ns["act"], ns["mood"]


def mv(who, to, speed="walk", both=False):
    if isinstance(who, list):
        return [_mv(w, to, speed, both or i > 0) for i, w in enumerate(who)]
    return _mv(who, to, speed, both)


def A(beat):
    """start this beat together with the previous one"""
    return {**beat, "and": True}


def flat(beats):
    out = []
    for b in beats:
        out.extend(b if isinstance(b, list) else [b])
    return out


LONG_TITLE = "Can You Solve 3 Scarecrow Riddles? 🎃 | EP 9"
CHANNEL = "https://www.youtube.com/@DoughBrosTV"
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "halloween", "scarecrow", "riddles", "sir stuffing"]
SHORT_TAGS = ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon",
              "horror comedy", "animated series"]

long_ = {
    "id": "ep009_long", "format": "long",
    "title": LONG_TITLE,
    "hook": "ANSWER... OR STAY FOREVER!", "hook_dur": 3.5,
    "description": ("Halloween night in the garden: Sir Stuffing the scarecrow has trapped Pim in the mud. "
                    "Answer three riddles before midnight... or Pim stays in the garden FOREVER. "
                    "Zeek's riddle machine says 'banana', Crispy finds footprints in the flour, and a secret letter "
                    "shows who is really behind it all. Can YOU solve the riddles before the Dough Bros do?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #halloween"),
    "tags": TAGS + ["episode 9", "pim", "mr pot", "halloween cartoon"],
    "thumbnail": {"bg": "garden", "villain": "scarecrow", "heroes": ["pim"], "text": "STUCK FOREVER?"},
    "scenes": [
        {   # 1 cold open: the scarecrow moves (hook from frame 1)
            "bg": "garden", "music": "heartbeat",
            "heroes": {"pim": 380, "bup": 640, "zeek": 880},
            "moods": {"pim": "scared", "bup": "scared", "zeek": "scared"},
            "villain": {"type": "scarecrow", "x": 1500, "state": "awake", "scale": 0.9},
            "beats": [
                act("pim", "shake"),
                A(S("pim", "Guys... the scarecrow just MOVED!|Chicos... ¡el espantapájaros se MOVIÓ!|Leute... die Vogelscheuche hat sich BEWEGT!|"
                    "Les gars... l'épouvantail a BOUGÉ !|Ragazzi... lo spaventapasseri si è MOSSO!|Gente... o espantalho se MEXEU!")),
                A({"villain": "lunge", "to": 1380}),
                {"sfx": "thump", "wait": 0.3},
                A({"shake": 0.5, "power": 16}),
                S("villain", "Answer my three riddles... or stay in my garden FOREVER!|Respondan mis tres acertijos... ¡o quédense en mi jardín PARA SIEMPRE!|"
                  "Löst meine drei Rätsel... oder bleibt für IMMER in meinem Garten!|Résolvez mes trois énigmes... ou restez dans mon jardin POUR TOUJOURS !|"
                  "Risolvete i miei tre indovinelli... o restate nel mio giardino PER SEMPRE!|Respondam minhas três charadas... ou fiquem no meu jardim PARA SEMPRE!"),
                act(["pim", "bup", "zeek"], "scream"),
                S("pim", "I c-can't move! My feet are stuck in the MUD!|¡N-no me puedo mover! ¡Mis pies están atrapados en el BARRO!|"
                  "Ich k-kann mich nicht bewegen! Meine Füße stecken im SCHLAMM!|J-je ne peux pas bouger ! Mes pieds sont coincés dans la BOUE !|"
                  "N-non riesco a muovermi! I miei piedi sono bloccati nel FANGO!|E-eu não consigo me mexer! Meus pés estão presos na LAMA!"),
                mood("bup", "angry"),
                S("bup", "Okay team, here's the plan. We answer. Then we run.|Bien, equipo, este es el plan. Respondemos. Luego corremos.|"
                  "Okay, Team, hier ist der Plan. Wir antworten. Dann rennen wir.|OK l'équipe, voici le plan. On répond. Puis on court.|"
                  "Ok squadra, ecco il piano. Rispondiamo. Poi corriamo.|Certo, equipe, o plano é esse. A gente responde. Depois corre."),
                {"villain": "rage", "level": 0.5},
                S("villain", "Riddle one. I have eyes, but I cannot see. I sleep in the dirt until you dig me up.|"
                  "Acertijo uno. Tengo ojos, pero no veo. Duermo en la tierra hasta que me desentierras.|"
                  "Rätsel eins. Ich habe Augen, doch ich sehe nicht. Ich schlafe in der Erde, bis du mich ausgräbst.|"
                  "Énigme un. J'ai des yeux, mais je ne vois pas. Je dors dans la terre jusqu'à ce qu'on me déterre.|"
                  "Indovinello uno. Ho gli occhi, ma non vedo. Dormo nella terra finché non mi scavi.|"
                  "Charada um. Tenho olhos, mas não enxergo. Durmo na terra até você me desenterrar."),
                mood("zeek", "happy"),
                act("zeek", "bounce"),
                A(S("zeek", "Easy! A potato! Potatoes have eyes. Science!|¡Fácil! ¡Una papa! Las papas tienen ojos. ¡Ciencia!|"
                    "Einfach! Eine Kartoffel! Kartoffeln haben Augen. Wissenschaft!|Facile ! Une pomme de terre ! Elles ont des yeux. La science !|"
                    "Facile! Una patata! Le patate hanno gli occhi. Scienza!|Fácil! Uma batata! Batatas têm olhos. Ciência!")),
                {"villain": "rage", "level": 0.9},
                A({"sfx": "sting", "wait": 0.2}),
                S("villain", "Hmph. Correct.|Hmph. Correcto.|Hmpf. Richtig.|Hmph. Exact.|Hmph. Esatto.|Hmpf. Correto."),
                S("villain", "Riddle two. The more you take... the more you leave behind.|Acertijo dos. Cuanto más tomas... más dejas atrás.|"
                  "Rätsel zwei. Je mehr du nimmst... desto mehr lässt du zurück.|Énigme deux. Plus tu en prends... plus tu en laisses derrière toi.|"
                  "Indovinello due. Più ne prendi... più ne lasci indietro.|Charada dois. Quanto mais você pega... mais deixa para trás."),
                S("bup", "Cookies! ...No. Wait. Not cookies.|¡Galletas! ...No. Espera. Galletas no.|Kekse! ...Nein. Moment. Keine Kekse.|"
                  "Des cookies ! ...Non. Attends. Pas des cookies.|Biscotti! ...No. Aspetta. Niente biscotti.|Biscoitos! ...Não. Espera. Biscoito não."),
                {"villain": "roar"},
                S("villain", "Bring me the answer before midnight... or the bean is MINE!|Tráiganme la respuesta antes de medianoche... ¡o el frijol es MÍO!|"
                  "Bringt mir die Antwort vor Mitternacht... oder die Bohne gehört MIR!|Apportez-moi la réponse avant minuit... ou le haricot est À MOI !|"
                  "Portatemi la risposta prima di mezzanotte... o il fagiolo è MIO!|Tragam a resposta antes da meia-noite... ou o feijão é MEU!"),
                act("pim", "faint"),
                mv(["bup", "zeek"], "off_right", "run"),
            ],
            "tail": 0.3,
        },
        {   # 2 pantry: Zeek's riddle machine fails, Crispy appears
            "bg": "pantry", "music": "music_box",
            "heroes": {"lolly": 340, "zeek": 600, "bup": 860, "crispy": 2200},
            "beats": [
                S("zeek", "Behold! The Riddle-Matic Five Thousand! It knows EVERY answer!|¡Contemplen! ¡El Acertijo-Mático Cinco Mil! ¡Sabe TODAS las respuestas!|"
                  "Seht her! Der Rätsel-Matik Fünftausend! Er kennt JEDE Antwort!|Voici le Devinette-Matic Cinq Mille ! Il connaît TOUTES les réponses !|"
                  "Ecco l'Indovinel-Matic Cinquemila! Conosce TUTTE le risposte!|Contemplem! O Charada-Mático Cinco Mil! Ele sabe TODAS as respostas!"),
                {"sfx": "clank", "wait": 0.4},
                {"sfx": "pop", "wait": 0.3},
                A({"shake": 0.4, "power": 12}),
                act("zeek", "jump"),
                S("zeek", "It says the answer is... 'banana.' It's never wrong. Except now.|Dice que la respuesta es... 'plátano'. Nunca se equivoca. Excepto ahora.|"
                  "Er sagt, die Antwort ist... 'Banane'. Er irrt sich nie. Außer jetzt.|Il dit que la réponse est... 'banane'. Il ne se trompe jamais. Sauf maintenant.|"
                  "Dice che la risposta è... 'banana'. Non sbaglia mai. Tranne adesso.|Ele diz que a resposta é... 'banana'. Nunca erra. Menos agora."),
                S("lolly", "The more you take, the more you leave behind... Hmm.|Cuanto más tomas, más dejas atrás... Mmm.|"
                  "Je mehr du nimmst, desto mehr lässt du zurück... Hmm.|Plus tu en prends, plus tu en laisses... Hmm.|"
                  "Più ne prendi, più ne lasci indietro... Mmm.|Quanto mais você pega, mais deixa para trás... Hmm."),
                {"sfx": "creak", "wait": 0.3},
                mv("crispy", 1150, "walk"),
                act(["lolly", "zeek", "bup"], "jump"),
                S("crispy", "Footsteps.|Pasos.|Schritte.|Des pas.|Passi.|Passos."),
                S("bup", "Crispy! Stop DOING that! ...Wait. Footsteps?|¡Crispy! ¡Deja de HACER eso! ...Espera. ¿Pasos?|"
                  "Crispy! Hör auf DAMIT! ...Moment. Schritte?|Crispy ! Arrête de FAIRE ça ! ...Attends. Des pas ?|"
                  "Crispy! Smettila di FARLO! ...Aspetta. Passi?|Crispy! Para de FAZER isso! ...Espera. Passos?"),
                S("crispy", "Take a step, leave a footprint. And look... someone left prints in the flour.|"
                  "Das un paso, dejas una huella. Y miren... alguien dejó huellas en la harina.|"
                  "Ein Schritt, ein Fußabdruck. Und seht... jemand hat Abdrücke im Mehl hinterlassen.|"
                  "Un pas, une empreinte. Et regardez... quelqu'un a laissé des traces dans la farine.|"
                  "Fai un passo, lasci un'impronta. E guardate... qualcuno ha lasciato impronte nella farina.|"
                  "Deu um passo, deixou uma pegada. E olhem... alguém deixou marcas na farinha."),
                S("zeek", "Round prints. Big ones. Something heavy went up to the attic.|Huellas redondas. Grandes. Algo pesado subió al ático.|"
                  "Runde Abdrücke. Große. Etwas Schweres ist auf den Dachboden gegangen.|Des traces rondes. Énormes. Quelque chose de lourd est monté au grenier.|"
                  "Impronte rotonde. Grandi. Qualcosa di pesante è salito in soffitta.|Marcas redondas. Grandes. Algo pesado subiu para o sótão."),
                mood("lolly", "angry"),
                S("lolly", "Then we go to the attic. NOBODY keeps our Pim.|Entonces vamos al ático. NADIE se queda con nuestro Pim.|"
                  "Dann gehen wir auf den Dachboden. NIEMAND behält unseren Pim.|Alors on monte au grenier. PERSONNE ne garde notre Pim.|"
                  "Allora andiamo in soffitta. NESSUNO si tiene il nostro Pim.|Então vamos ao sótão. NINGUÉM fica com o nosso Pim."),
                mv(["lolly", "zeek", "bup", "crispy"], "off_right", "run"),
            ],
            "tail": 0.3,
        },
        {   # 3 attic: the secret letter (twist)
            "bg": "attic", "music": "drone",
            "heroes": {"bup": 400, "zeek": 640, "lolly": 880, "crispy": 1120},
            "beats": [
                {"sfx": "thump", "wait": 0.2},
                A({"shake": 0.6, "power": 18}),
                act(["bup", "zeek", "lolly"], "jump"),
                S("zeek", "The round prints stop here. Right next to... a letter!|Las huellas redondas terminan aquí. Justo al lado de... ¡una carta!|"
                  "Die runden Abdrücke enden hier. Direkt neben... einem Brief!|Les traces rondes s'arrêtent ici. Juste à côté... d'une lettre !|"
                  "Le impronte rotonde finiscono qui. Proprio accanto a... una lettera!|As marcas redondas param aqui. Bem ao lado de... uma carta!"),
                S("bup", "'Dear Sir Stuffing. Keep the bean until midnight. I need all five.'|'Querido Sir Relleno. Guarda al frijol hasta medianoche. Necesito a los cinco.'|"
                  "'Lieber Sir Stroh. Behalte die Bohne bis Mitternacht. Ich brauche alle fünf.'|'Cher Sir Rembourré. Garde le haricot jusqu'à minuit. J'ai besoin des cinq.'|"
                  "'Caro Sir Imbottito. Tieni il fagiolo fino a mezzanotte. Mi servono tutti e cinque.'|'Querido Sir Recheio. Fique com o feijão até a meia-noite. Preciso dos cinco.'"),
                S("bup", "'Signed... Mister Pot.'|'Firmado... Señor Olla.'|'Gezeichnet... Herr Topf.'|'Signé... Monsieur Marmite.'|'Firmato... Signor Pentola.'|'Assinado... Senhor Panela.'"),
                mood(["bup", "zeek", "lolly"], "scared"),
                {"sfx": "sting", "wait": 0.3},
                S("lolly", "Mr. Pot! He's using the scarecrow!|¡El Señor Olla! ¡Está usando al espantapájaros!|Herr Topf! Er benutzt die Vogelscheuche!|"
                  "Monsieur Marmite ! Il se sert de l'épouvantail !|Il Signor Pentola! Sta usando lo spaventapasseri!|O Senhor Panela! Ele está usando o espantalho!"),
                S("crispy", "Round prints... the bottom of a pot. He was here. Tonight.|Huellas redondas... el fondo de una olla. Estuvo aquí. Esta noche.|"
                  "Runde Abdrücke... der Boden eines Topfes. Er war hier. Heute Nacht.|Des traces rondes... le fond d'une marmite. Il était ici. Ce soir.|"
                  "Impronte rotonde... il fondo di una pentola. Era qui. Stanotte.|Marcas redondas... o fundo de uma panela. Ele esteve aqui. Hoje à noite."),
                {"sfx": "ding", "wait": 0.3},
                act("zeek", "jump"),
                S("zeek", "My calculations say it's eleven fifty. Ten minutes to midnight!|Mis cálculos dicen que son las once y cincuenta. ¡Diez minutos para medianoche!|"
                  "Laut meinen Berechnungen ist es elf Uhr fünfzig. Zehn Minuten bis Mitternacht!|Selon mes calculs, il est onze heures cinquante. Minuit dans dix minutes !|"
                  "I miei calcoli dicono che sono le undici e cinquanta. Dieci minuti a mezzanotte!|Meus cálculos dizem que são onze e cinquenta. Dez minutos para a meia-noite!"),
                mood("bup", "angry"),
                S("bup", "Then we RUN. Everybody, to the garden!|¡Entonces CORREMOS! ¡Todos, al jardín!|Dann RENNEN wir. Alle in den Garten!|"
                  "Alors on COURT. Tout le monde, au jardin !|Allora CORRIAMO. Tutti in giardino!|Então a gente CORRE. Todo mundo pro jardim!"),
                mv(["bup", "zeek", "lolly", "crispy"], "off_left", "run"),
            ],
            "tail": 0.3,
        },
        {   # 4 garden: riddle two answered, riddle three, Pim's brave moment
            "bg": "garden", "music": "heartbeat",
            "heroes": {"pim": 380, "bup": -200, "zeek": -400, "lolly": -600},
            "moods": {"pim": "scared"},
            "villain": {"type": "scarecrow", "x": 1420, "state": "awake", "scale": 0.9},
            "beats": [
                S("villain", "Tick... tock... little bean. Midnight is coming.|Tic... tac... frijolito. La medianoche se acerca.|"
                  "Tick... tack... kleine Bohne. Mitternacht kommt.|Tic... tac... petit haricot. Minuit approche.|"
                  "Tic... tac... fagiolino. Arriva la mezzanotte.|Tique... taque... feijãozinho. A meia-noite está chegando."),
                act("pim", "shake"),
                S("pim", "P-please hurry, guys... please, please hurry...|P-por favor, apúrense... por favor, por favor...|"
                  "B-bitte beeilt euch... bitte, bitte beeilt euch...|D-dépêchez-vous, les gars... s'il vous plaît...|"
                  "V-vi prego, sbrigatevi... vi prego, vi prego...|P-por favor, corram... por favor, por favor..."),
                mv("bup", 640, "run"), mv("zeek", 880, "run", True), mv("lolly", 160, "run", True),
                S("bup", "We have your answer! FOOTSTEPS!|¡Tenemos tu respuesta! ¡PASOS!|Wir haben die Antwort! SCHRITTE!|"
                  "On a ta réponse ! DES PAS !|Abbiamo la risposta! PASSI!|Temos sua resposta! PASSOS!"),
                {"villain": "rage", "level": 1.0},
                A({"shake": 0.6, "power": 20}),
                S("villain", "NOOO! ...Correct.|¡NOOO! ...Correcto.|NEEEIN! ...Richtig.|NOOON ! ...Exact.|NOOO! ...Esatto.|NÃÃÃO! ...Correto."),
                {"villain": "rage", "level": 0.4},
                S("villain", "Fine. Riddle THREE. What can you give away... and still keep?|Bien. Acertijo TRES. ¿Qué puedes regalar... y aun así conservar?|"
                  "Gut. Rätsel DREI. Was kannst du verschenken... und trotzdem behalten?|Bien. Énigme TROIS. Que peux-tu donner... et quand même garder ?|"
                  "Bene. Indovinello TRE. Cosa puoi regalare... e tenere lo stesso?|Certo. Charada TRÊS. O que você pode dar... e mesmo assim manter?"),
                S("zeek", "A cold? A sock? My calculations are... empty.|¿Un resfriado? ¿Un calcetín? Mis cálculos están... vacíos.|"
                  "Eine Erkältung? Eine Socke? Meine Berechnungen sind... leer.|Un rhume ? Une chaussette ? Mes calculs sont... vides.|"
                  "Un raffreddore? Un calzino? I miei calcoli sono... vuoti.|Um resfriado? Uma meia? Meus cálculos estão... vazios."),
                {"sfx": "ding", "wait": 0.3},
                act("pim", "jump"),
                S("pim", "I know it! A p-p-promise! You give your word... and you keep it!|¡Lo sé! ¡Una p-p-promesa! Das tu palabra... ¡y la cumples!|"
                  "Ich weiß es! Ein V-V-Versprechen! Du gibst dein Wort... und hältst es!|Je sais ! Une p-p-promesse ! Tu donnes ta parole... et tu la tiens !|"
                  "Lo so! Una p-p-promessa! Dai la tua parola... e la mantieni!|Eu sei! Uma p-p-promessa! Você dá sua palavra... e cumpre!"),
                mood("lolly", "happy"),
                act("lolly", "bounce"),
                A(S("lolly", "Pim! That's my brave little bean!|¡Pim! ¡Ese es mi frijolito valiente!|Pim! Das ist meine tapfere kleine Bohne!|"
                    "Pim ! C'est mon petit haricot courageux !|Pim! Ecco il mio fagiolino coraggioso!|Pim! Esse é o meu feijãozinho corajoso!")),
                {"villain": "roar"},
                S("villain", "Nobody EVER solved all three! ...The garden lets you go.|¡NADIE resolvió jamás los tres! ...El jardín te deja ir.|"
                  "NIEMAND hat je alle drei gelöst! ...Der Garten lässt dich gehen.|PERSONNE n'a jamais résolu les trois ! ...Le jardin te libère.|"
                  "NESSUNO li ha mai risolti tutti e tre! ...Il giardino ti lascia andare.|NINGUÉM nunca resolveu as três! ...O jardim deixa você ir."),
                mood("pim", "happy"),
                act("pim", "bounce"),
                A(S("pim", "My feet! I'm free! I'm FREE!|¡Mis pies! ¡Soy libre! ¡Soy LIBRE!|Meine Füße! Ich bin frei! Ich bin FREI!|"
                    "Mes pieds ! Je suis libre ! LIBRE !|I miei piedi! Sono libero! LIBERO!|Meus pés! Estou livre! LIVRE!")),
                {"villain": "rage", "level": 1.0},
                S("villain", "But Mr. Pot promised me a pumpkin crown... and I WANT IT!|Pero el Señor Olla me prometió una corona de calabaza... ¡y la QUIERO!|"
                  "Aber Herr Topf hat mir eine Kürbiskrone versprochen... und ich WILL SIE!|Mais Monsieur Marmite m'a promis une couronne de citrouille... et je la VEUX !|"
                  "Ma il Signor Pentola mi ha promesso una corona di zucca... e la VOGLIO!|Mas o Senhor Panela me prometeu uma coroa de abóbora... e eu QUERO!"),
                {"villain": "lunge", "to": 1150},
                act(["pim", "bup", "zeek", "lolly"], "scream"),
                mv(["pim", "bup", "zeek", "lolly"], "off_left", "run"),
            ],
            "tail": 0.3,
        },
        {   # 5 kitchen: door slam, Pim faints from being brave
            "bg": "kitchen", "music": "music_box",
            "heroes": {"pim": 2100, "bup": 2300, "zeek": 2500, "lolly": 2700, "crispy": 260},
            "beats": [
                mv("pim", 500, "run"), mv("bup", 740, "run", True), mv("zeek", 980, "run", True), mv("lolly", 1220, "run", True),
                S("bup", "Door! Close the DOOR!|¡La puerta! ¡Cierren la PUERTA!|Die Tür! Macht die TÜR zu!|La porte ! Fermez la PORTE !|La porta! Chiudete la PORTA!|A porta! Fecha a PORTA!"),
                {"sfx": "thump", "wait": 0.4},
                A({"shake": 0.5, "power": 18}),
                mood(["pim", "bup", "zeek", "lolly"], "happy"),
                S("lolly", "Closed. And locked. With a cookie-sized lock!|Cerrada. Y con llave. ¡Con un candado tamaño galleta!|"
                  "Zu. Und abgeschlossen. Mit einem keksgroßen Schloss!|Fermée. Et verrouillée. Avec un cadenas taille cookie !|"
                  "Chiusa. E sprangata. Con un lucchetto formato biscotto!|Fechada. E trancada. Com um cadeado do tamanho de um biscoito!"),
                S("zeek", "Straw slips on kitchen tiles. He can't follow us in here. Science!|La paja resbala en las baldosas. No puede seguirnos aquí. ¡Ciencia!|"
                  "Stroh rutscht auf Küchenfliesen. Er kann uns hier nicht folgen. Wissenschaft!|La paille glisse sur le carrelage. Il ne peut pas nous suivre ici. La science !|"
                  "La paglia scivola sulle piastrelle. Non può seguirci qui. Scienza!|Palha escorrega no piso da cozinha. Ele não pode nos seguir aqui. Ciência!"),
                act("pim", "bounce"),
                A(S("pim", "I solved a riddle! Me! The bean! I'm a HERO!|¡Resolví un acertijo! ¡Yo! ¡El frijol! ¡Soy un HÉROE!|"
                    "Ich habe ein Rätsel gelöst! Ich! Die Bohne! Ich bin ein HELD!|J'ai résolu une énigme ! Moi ! Le haricot ! Je suis un HÉROS !|"
                    "Ho risolto un indovinello! Io! Il fagiolo! Sono un EROE!|Eu resolvi uma charada! Eu! O feijão! Sou um HERÓI!")),
                act("pim", "faint"),
                S("crispy", "...He fainted from being brave.|...Se desmayó de tanto valor.|...Er ist vor lauter Mut umgekippt.|...Il s'est évanoui de courage.|...È svenuto per il troppo coraggio.|...Ele desmaiou de tanta coragem."),
                S("bup", "Okay team. Hot cocoa, then bed. Long night.|Bien, equipo. Chocolate caliente y a la cama. Larga noche.|"
                  "Okay, Team. Heiße Schokolade, dann ins Bett. Lange Nacht.|OK l'équipe. Chocolat chaud, puis au lit. Longue nuit.|"
                  "Ok squadra. Cioccolata calda, poi a letto. Lunga notte.|Certo, equipe. Chocolate quente e cama. Noite longa."),
            ],
            "tail": 0.2,
        },
        {   # 6 cliffhanger: Mr. Pot himself
            "bg": "kitchen", "music": "drone",
            "heroes": {"pim": 300, "bup": 520, "zeek": 740, "lolly": 960, "crispy": 1140},
            "villain": {"type": "pot", "x": 1520, "state": "hidden", "scale": 0.9},
            "beats": [
                {"sfx": "creak", "wait": 0.4},
                mood(["bup", "zeek", "lolly", "pim"], "scared"),
                S("lolly", "Um... why is the oven light on?|Eh... ¿por qué está encendida la luz del horno?|Ähm... warum ist das Ofenlicht an?|"
                  "Euh... pourquoi la lumière du four est allumée ?|Ehm... perché la luce del forno è accesa?|Hã... por que a luz do forno está acesa?"),
                {"villain": "show"},
                {"villain": "wake"},
                S("villain", "Fresh... dough...|Masa... fresca...|Frischer... Teig...|Pâte... fraîche...|Pasta... fresca...|Massa... fresca..."),
                act(["pim", "bup", "zeek", "lolly"], "scream"),
                S("villain", "The kettle failed. The vacuum failed. The ghost and the scarecrow failed.|La tetera falló. La aspiradora falló. El fantasma y el espantapájaros fallaron.|"
                  "Der Kessel hat versagt. Der Staubsauger hat versagt. Der Geist und die Vogelscheuche haben versagt.|La bouilloire a échoué. L'aspirateur a échoué. Le fantôme et l'épouvantail aussi.|"
                  "Il bollitore ha fallito. L'aspirapolvere ha fallito. Il fantasma e lo spaventapasseri hanno fallito.|A chaleira falhou. O aspirador falhou. O fantasma e o espantalho falharam."),
                S("crispy", "Pot. We meet again.|Olla. Nos volvemos a ver.|Topf. Wir sehen uns wieder.|Marmite. On se retrouve.|Pentola. Ci rivediamo.|Panela. Nos encontramos de novo."),
                {"villain": "rage", "level": 1.0},
                S("villain", "So tonight... I do it MYSELF. Time to FRY!|Así que esta noche... lo hago YO MISMO. ¡Hora de FREÍR!|"
                  "Also mache ich es heute Nacht... SELBST. Zeit zum BRATEN!|Alors ce soir... je m'en occupe MOI-MÊME. L'heure de FRIRE !|"
                  "Allora stanotte... lo faccio IO. È ora di FRIGGERE!|Então hoje à noite... eu mesmo faço. Hora de FRITAR!"),
                {"villain": "roar"},
                {"villain": "lunge", "to": 1250},
                act("pim", "faint"),
            ],
            "tail": 0.6,
        },
    ],
}

short1 = {
    "id": "ep009_short1", "format": "short",
    "title": "Who's Standing Behind Pim? 😱 #shorts",
    "hook": "DON'T LOOK BEHIND YOU",
    "description": ("Pim is SURE someone is standing behind him in the dark garden... and he's right. Twice. "
                    "Watch the full episode where the scarecrow asks 3 riddles: "
                    f"\"{LONG_TITLE}\" on {CHANNEL} #shorts #animation #cartoon #doughbros #halloween"),
    "tags": SHORT_TAGS + ["crispy", "pim", "scarecrow", "jump scare", "halloween"],
    "thumbnail": {"bg": "garden", "villain": "scarecrow", "heroes": ["pim"], "text": "BEHIND YOU!"},
    "scenes": [{
        "bg": "garden", "music": "heartbeat",
        "heroes": {"pim": 520, "bup": 820, "crispy": -300},
        "moods": {"pim": "scared"},
        "villain": {"type": "scarecrow", "x": 1450, "state": "hidden", "scale": 0.85},
        "beats": [
            act("pim", "shake"),
            A(S("pim", "Bup... is someone standing BEHIND me?|Bup... ¿hay alguien DETRÁS de mí?|Bup... steht jemand HINTER mir?|"
                "Bup... il y a quelqu'un DERRIÈRE moi ?|Bup... c'è qualcuno DIETRO di me?|Bup... tem alguém ATRÁS de mim?")),
            S("bup", "Nope. Just you and the dark garden.|No. Solo tú y el jardín oscuro.|Nö. Nur du und der dunkle Garten.|"
              "Non. Juste toi et le jardin noir.|No. Solo tu e il giardino buio.|Não. Só você e o jardim escuro."),
            mv("crispy", 270, "walk"),
            A({"sfx": "creak", "wait": 0.2}),
            S("crispy", "Hello.|Hola.|Hallo.|Salut.|Ciao.|Olá."),
            act("pim", "scream"),
            act("pim", "jump"),
            S("pim", "CRISPY! Stop DOING that!|¡CRISPY! ¡Deja de HACER eso!|CRISPY! Hör auf DAMIT!|CRISPY ! Arrête de FAIRE ça !|CRISPY! Smettila di FARLO!|CRISPY! Para de FAZER isso!"),
            S("crispy", "I was here the whole time.|Estuve aquí todo el tiempo.|Ich war die ganze Zeit hier.|J'étais là depuis le début.|Ero qui tutto il tempo.|Eu estava aqui o tempo todo."),
            {"sfx": "creak", "wait": 0.3},
            {"villain": "show"},
            S("villain", "Answer my riddle...|Responde mi acertijo...|Löse mein Rätsel...|Résous mon énigme...|Risolvi il mio indovinello...|Responda minha charada..."),
            mood("crispy", "scared"),
            act("crispy", "scream"),
            S("crispy", "Okay. THAT one scares me too.|Vale. ESE también me asusta.|Okay. DER macht mir auch Angst.|OK. LUI, il me fait peur aussi.|Ok. QUELLO spaventa anche me.|Tá. ESSE me assusta também."),
            act("crispy", "faint"),
            {"villain": "hide"},
            A({"sfx": "whoosh", "wait": 0.2}),
            mv("crispy", "off_left", "run"),
            mood("pim", "scared"),
            S("pim", "Bup... is—|Bup... ¿hay—|Bup... steht—|Bup... il y a—|Bup... c'è—|Bup... tem—"),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    for sc in s["scenes"]:
        sc["beats"] = flat(sc["beats"])
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"], len(s["title"]))

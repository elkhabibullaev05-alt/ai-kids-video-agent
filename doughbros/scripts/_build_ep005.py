"""Builds the EP5 scripts (long + 3 shorts). Run: python3 scripts/_build_ep005.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
src = (OUT / "_build_ep003.py").read_text(encoding="utf-8").split("ALL4 =")[0]
ns = {"__file__": str(OUT / "_build_ep003.py")}
exec(src, ns)
S, mv, act, mood = ns["S"], ns["mv"], ns["act"], ns["mood"]

ALL4 = ["bup", "pim", "zeek", "lolly"]
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "mr pot", "crispy"]

long_ = {
    "id": "ep005_long", "format": "long",
    "title": "Dough Bros vs MR. POT 🔥 | Animation EP 5",
    "description": ("Mr. Pot lunges for Crispy in the dark oven... and Crispy finally tells the truth. "
                    "Why was he burnt? Why does Mr. Pot want him back? And what does it have to do with Bup? "
                    "Then the team runs to the one place Mr. Pot hates most: the freezing-cold fridge.\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy"),
    "tags": TAGS + ["episode 5", "crispy's secret"],
    "thumbnail": {"bg": "oven", "villain": "pot", "heroes": ["crispy", "bup", "pim"], "text": "CRISPY'S SECRET!"},
    "scenes": [
        {   # 1 cold open: the lunge
            "bg": "oven", "music": "drone",
            "heroes": {"bup": 640, "zeek": 380, "crispy": 880},
            "moods": {"bup": "scared", "zeek": "scared"},
            "villain": {"type": "pot", "x": 1450, "state": "awake", "scale": 0.95},
            "beats": [
                {"villain": "lunge", "to": 1250},
                act(["bup", "zeek"], "scream"),
                {"shake": 0.6, "power": 20},
                S("villain", "Crispy... my favorite little mistake. Come back to the pot!|Crispy... mi pequeño error favorito. ¡Vuelve a la olla!|"
                  "Crispy... mein liebster kleiner Fehler. Zurück in den Topf!|Crispy... ma petite erreur préférée. Reviens dans la marmite !|"
                  "Crispy... il mio piccolo errore preferito. Torna nella pentola!|Crispy... meu errinho favorito. Volte para a panela!"),
                S("crispy", "Not tonight.|Esta noche no.|Nicht heute Nacht.|Pas ce soir.|Non stanotte.|Hoje não."),
                act("crispy", "spin"),
                {"sfx": "whoosh", "wait": 0.3, "and": True},
                {"shake": 0.4, "power": 10},
                S("narr", "Crispy shakes his embers. The oven fills with thick black smoke.|Crispy sacude sus brasas. El horno se llena de humo negro.|"
                  "Crispy schüttelt seine Glut. Der Ofen füllt sich mit schwarzem Rauch.|Crispy secoue ses braises. Le four se remplit de fumée noire.|"
                  "Crispy scuote le sue braci. Il forno si riempie di fumo nero.|Crispy sacode suas brasas. O forno se enche de fumaça preta."),
                {"villain": "rage", "level": 0.9},
                S("villain", "I can't see! Where are you?!|¡No veo nada! ¿¡Dónde están!?|Ich sehe nichts! Wo seid ihr?!|"
                  "Je ne vois rien ! Où êtes-vous ?!|Non vedo niente! Dove siete?!|Não consigo ver! Cadê vocês?!"),
                S("crispy", "Run. To the attic. Now.|Corran. Al ático. Ya.|Lauft. Auf den Dachboden. Sofort.|"
                  "Courez. Au grenier. Maintenant.|Correte. In soffitta. Subito.|Corram. Para o sótão. Agora."),
                mv("bup", "off_left", "run"), mv("zeek", "off_left", "run", True), mv("crispy", "off_left", "run", True),
                S("villain", "You can't hide forever, Crispy!|¡No puedes esconderte para siempre, Crispy!|Du kannst dich nicht ewig verstecken, Crispy!|"
                  "Tu ne pourras pas te cacher pour toujours, Crispy !|Non puoi nasconderti per sempre, Crispy!|Você não pode se esconder para sempre, Crispy!"),
                {"villain": "roar"},
            ],
            "tail": 0.4,
        },
        {   # 2 attic: the question
            "bg": "attic", "music": "music_box",
            "heroes": {"lolly": 700, "pim": 460, "bup": -300, "zeek": -500, "crispy": -700},
            "moods": {"pim": "scared"},
            "beats": [
                {"card": "UP IN THE ATTIC...", "es": "ARRIBA EN EL ÁTICO...", "dur": 2.0},
                S("pim", "They've been gone too long. Something's w-wrong. I just KNOW it.|Tardan demasiado. Algo va m-mal. Lo SÉ.|"
                  "Sie sind zu lange weg. Etwas stimmt n-nicht. Ich WEISS es.|Ils sont partis depuis trop longtemps. Quelque chose ne v-va pas.|"
                  "Sono via da troppo. Qualcosa non va. Lo SO.|Eles estão demorando demais. Tem algo e-errado. Eu SEI."),
                S("lolly", "Shh, Pim. Bup always comes back.|Shh, Pim. Bup siempre vuelve.|Psst, Pim. Bup kommt immer zurück.|"
                  "Chut, Pim. Bup revient toujours.|Shh, Pim. Bup torna sempre.|Psiu, Pim. O Bup sempre volta."),
                mv("bup", 960, "run"), mv("zeek", 240, "run", True),
                act("pim", "jump"),
                S("bup", "We're back! And we're not alone.|¡Volvimos! Y no estamos solos.|Wir sind zurück! Und wir sind nicht allein.|"
                  "On est revenus ! Et on n'est pas seuls.|Siamo tornati! E non siamo soli.|Voltamos! E não estamos sozinhos."),
                mv("crispy", 1180, "walk"),
                act("pim", "faint"),
                S("lolly", "Oh, he fainted again. Hello, Crispy!|Ay, se desmayó otra vez. ¡Hola, Crispy!|Oh, er ist wieder ohnmächtig. Hallo, Crispy!|"
                  "Oh, il s'est encore évanoui. Bonsoir, Crispy !|Oh, è svenuto di nuovo. Ciao, Crispy!|Ah, ele desmaiou de novo. Oi, Crispy!"),
                mood("bup", "angry"),
                S("bup", "Crispy. Mr. Pot called you his 'favorite mistake'. Why?|Crispy. El Señor Olla te llamó su 'error favorito'. ¿Por qué?|"
                  "Crispy. Herr Topf nannte dich seinen 'liebsten Fehler'. Warum?|Crispy. Monsieur Marmite t'a appelé son « erreur préférée ». Pourquoi ?|"
                  "Crispy. Il Signor Pentola ti ha chiamato il suo 'errore preferito'. Perché?|Crispy. O Senhor Panela te chamou de 'erro favorito'. Por quê?"),
                S("zeek", "My calculations say you owe us the truth.|Mis cálculos dicen que nos debes la verdad.|Meine Berechnungen sagen: Du schuldest uns die Wahrheit.|"
                  "Mes calculs disent que tu nous dois la vérité.|I miei calcoli dicono che ci devi la verità.|Meus cálculos dizem que você nos deve a verdade."),
                {"wait": 0.8},
                S("crispy", "...Fine. But you won't like it.|...Está bien. Pero no les va a gustar.|...Gut. Aber es wird euch nicht gefallen.|"
                  "...D'accord. Mais ça ne va pas vous plaire.|...Va bene. Ma non vi piacerà.|...Tudo bem. Mas vocês não vão gostar."),
            ],
            "tail": 0.4,
        },
        {   # 3 attic: the secret (flashback told by Crispy)
            "bg": "attic", "music": "music_box",
            "heroes": {"crispy": 1000, "bup": 760, "lolly": 520, "zeek": 280},
            "beats": [
                {"card": "LONG, LONG AGO...", "es": "HACE MUCHO, MUCHO TIEMPO...", "dur": 2.2},
                S("crispy", "Once, I was not a rock. I was a soft, golden dough roll.|Antes no era una roca. Era un pancito dorado y suave.|"
                  "Früher war ich kein Stein. Ich war ein weiches, goldenes Brötchen.|Avant, je n'étais pas un caillou. J'étais un petit pain doré.|"
                  "Una volta non ero una pietra. Ero un panino morbido e dorato.|Antes eu não era uma pedra. Eu era um pãozinho dourado e macio."),
                S("lolly", "Aww! Golden Crispy!|¡Ay! ¡Crispy dorado!|Ach! Goldener Crispy!|Ooh ! Crispy doré !|Oh! Crispy dorato!|Own! Crispy dourado!"),
                S("crispy", "One night, Mr. Pot caught a tiny baby loaf. Fresh. Soft. Crying.|Una noche, el Señor Olla atrapó a un bebé pan. Fresco. Suave. Llorando.|"
                  "Eines Nachts fing Herr Topf ein winziges Babybrot. Frisch. Weich. Weinend.|Une nuit, Monsieur Marmite attrapa un bébé pain. Frais. Mou. En pleurs.|"
                  "Una notte, il Signor Pentola prese un piccolo pane neonato. Fresco. Morbido. In lacrime.|Uma noite, o Senhor Panela pegou um bebê pão. Fresco. Macio. Chorando."),
                S("crispy", "I jumped in. I pushed the baby out. And I fell into the fire.|Salté. Empujé al bebé afuera. Y caí al fuego.|"
                  "Ich sprang hinein. Ich schubste das Baby raus. Und fiel ins Feuer.|J'ai sauté. J'ai poussé le bébé dehors. Et je suis tombé dans le feu.|"
                  "Sono saltato dentro. Ho spinto fuori il piccolo. E sono caduto nel fuoco.|Eu pulei. Empurrei o bebê para fora. E caí no fogo."),
                {"sfx": "sting", "wait": 0.6},
                mood(["lolly", "zeek"], "scared"),
                S("zeek", "That's why you're... charcoal.|Por eso eres... carbón.|Deshalb bist du... Kohle.|C'est pour ça que tu es... du charbon.|Ecco perché sei... carbone.|É por isso que você é... carvão."),
                S("bup", "And the baby? What happened to the baby?|¿Y el bebé? ¿Qué pasó con el bebé?|Und das Baby? Was wurde aus dem Baby?|"
                  "Et le bébé ? Qu'est-il arrivé au bébé ?|E il piccolo? Che fine ha fatto?|E o bebê? O que aconteceu com o bebê?"),
                mv("crispy", 920, "walk"),
                S("crispy", "He grew up. Stale. Clumsy. Brave. With mismatched eyes.|Creció. Duro. Torpe. Valiente. Con ojos desiguales.|"
                  "Er wuchs auf. Altbacken. Tollpatschig. Mutig. Mit ungleichen Augen.|Il a grandi. Rassis. Maladroit. Courageux. Avec des yeux dépareillés.|"
                  "È cresciuto. Raffermo. Goffo. Coraggioso. Con gli occhi diversi.|Ele cresceu. Duro. Desajeitado. Corajoso. Com olhos diferentes."),
                {"wait": 0.8},
                mood("bup", "scared"),
                S("bup", "Wait... that baby... was ME?|Espera... ese bebé... ¿era YO?|Moment... dieses Baby... war ICH?|Attends... ce bébé... c'était MOI ?|Aspetta... quel piccolo... ero IO?|Espera... aquele bebê... era EU?"),
                act(["lolly", "zeek"], "jump"),
                S("crispy", "Mr. Pot never forgot. He wants to finish what he started. With both of us.|El Señor Olla nunca olvidó. Quiere terminar lo que empezó. Con los dos.|"
                  "Herr Topf hat es nie vergessen. Er will es zu Ende bringen. Mit uns beiden.|Monsieur Marmite n'a jamais oublié. Il veut finir ce qu'il a commencé. Avec nous deux.|"
                  "Il Signor Pentola non ha mai dimenticato. Vuole finire ciò che ha iniziato. Con tutti e due.|O Senhor Panela nunca esqueceu. Quer terminar o que começou. Com nós dois."),
                mood("bup", "happy"),
                S("bup", "Crispy... you saved my life. Thank you.|Crispy... me salvaste la vida. Gracias.|Crispy... du hast mir das Leben gerettet. Danke.|"
                  "Crispy... tu m'as sauvé la vie. Merci.|Crispy... mi hai salvato la vita. Grazie.|Crispy... você salvou minha vida. Obrigado."),
                S("crispy", "Don't thank me yet. Listen.|No me agradezcas todavía. Escucha.|Dank mir noch nicht. Hör mal.|Ne me remercie pas encore. Écoute.|Non ringraziarmi ancora. Ascolta.|Não me agradeça ainda. Escute."),
                {"sfx": "clank", "wait": 0.5},
                {"sfx": "thump", "wait": 0.5},
            ],
            "tail": 0.3,
        },
        {   # 4 attic: Mr. Pot arrives
            "bg": "attic", "music": "heartbeat",
            "heroes": {"pim": 300, "zeek": 520, "lolly": 740, "bup": 960, "crispy": -400},
            "moods": {"pim": "scared", "zeek": "scared", "lolly": "scared", "bup": "scared"},
            "villain": {"type": "pot", "x": 1500, "state": "hidden", "scale": 0.9},
            "beats": [
                {"sfx": "creak", "wait": 0.5},
                S("pim", "I woke up. Why is the floor b-bubbling?|Me desperté. ¿Por qué el suelo b-burbujea?|Ich bin wach. Warum b-blubbert der Boden?|"
                  "Je me suis réveillé. Pourquoi le sol fait des b-bulles ?|Mi sono svegliato. Perché il pavimento fa le b-bolle?|Acordei. Por que o chão está b-borbulhando?"),
                {"villain": "show"},
                {"villain": "roar"},
                act(ALL4, "scream"),
                S("villain", "Fresh... dough... Found you, little loaf!|Masa... fresca... ¡Te encontré, panecito!|Frischer... Teig... Hab dich, kleines Brot!|"
                  "De la pâte... fraîche... Trouvé, petit pain !|Impasto... fresco... Trovato, panino!|Massa... fresca... Achei você, pãozinho!"),
                mood("zeek", "happy"),
                S("zeek", "Stand back! My Steam-Blaster 2000 will push him away!|¡Atrás! ¡Mi Lanzavapor 2000 lo empujará!|"
                  "Zurück! Mein Dampf-Blaster 2000 schiebt ihn weg!|Reculez ! Mon Souffle-Vapeur 2000 va le repousser !|"
                  "Indietro! Il mio Spara-Vapore 2000 lo respingerà!|Para trás! Meu Jato-de-Vapor 2000 vai empurrá-lo!"),
                {"sfx": "pop", "wait": 0.4},
                {"sfx": "boing", "wait": 0.4},
                mood("zeek", "scared"),
                S("zeek", "...It made a bubble. One small bubble.|...Hizo una burbuja. Una burbujita.|...Es hat eine Blase gemacht. Eine kleine Blase.|"
                  "...Ça a fait une bulle. Une seule petite bulle.|...Ha fatto una bolla. Una piccola bolla.|...Fez uma bolha. Uma bolhinha."),
                {"villain": "lunge", "to": 1300},
                mood("lolly", "angry"),
                act("lolly", "jump"),
                S("lolly", "That's ENOUGH! Nobody fries my friends! NOBODY!|¡YA BASTA! ¡Nadie fríe a mis amigos! ¡NADIE!|"
                  "JETZT REICHT'S! Niemand brät meine Freunde! NIEMAND!|ÇA SUFFIT ! Personne ne fait frire mes amis ! PERSONNE !|"
                  "ADESSO BASTA! Nessuno frigge i miei amici! NESSUNO!|CHEGA! Ninguém frita meus amigos! NINGUÉM!"),
                {"shake": 0.5, "power": 14},
                {"villain": "rage", "level": 0.4},
                S("villain", "Ooh. Scary cookie. I'm SO frightened. Ha ha ha!|Uy. Galleta aterradora. Qué MIEDO. ¡Ja ja ja!|"
                  "Oh. Gruseliger Keks. Ich hab SO Angst. Ha ha ha!|Oh. Biscuit effrayant. J'ai SI peur. Ha ha ha !|"
                  "Oh. Biscotto spaventoso. Ho TANTA paura. Ah ah ah!|Ui. Biscoito assustador. Que MEDO. Ha ha ha!"),
                mv("crispy", 1100, "run"),
                S("crispy", "Remember his weak spot? COLD. Everyone, to the fridge!|¿Recuerdan su punto débil? El FRÍO. ¡Todos a la nevera!|"
                  "Wisst ihr seine Schwachstelle? KÄLTE. Alle zum Kühlschrank!|Vous vous souvenez de son point faible ? Le FROID. Tous au frigo !|"
                  "Ricordate il suo punto debole? Il FREDDO. Tutti al frigo!|Lembram do ponto fraco dele? FRIO. Todos para a geladeira!"),
                mv("pim", "off_left", "run"), mv("zeek", "off_left", "run", True), mv("lolly", "off_left", "run", True),
                mv("bup", "off_left", "run", True), mv("crispy", "off_left", "run", True),
                {"villain": "roar"},
            ],
            "tail": 0.3,
        },
        {   # 5 fridge: the cold trick
            "bg": "fridge", "music": "heartbeat",
            "heroes": {"pim": 280, "zeek": 500, "lolly": 720, "bup": 940, "crispy": 1120},
            "moods": {"pim": "scared"},
            "villain": {"type": "pot", "x": 2300, "state": "awake", "scale": 0.85},
            "beats": [
                {"card": "INSIDE THE FRIDGE...", "es": "DENTRO DE LA NEVERA...", "dur": 2.0},
                {"sfx": "ice", "wait": 0.4},
                S("pim", "C-c-cold! It's s-so c-cold! My bean is f-freezing!|¡F-f-frío! ¡Qué f-frío! ¡Mi frijol se c-congela!|"
                  "K-k-kalt! So k-kalt! Meine Bohne g-gefriert!|F-f-froid ! Si f-froid ! Mon haricot g-gèle !|"
                  "F-f-freddo! Che f-freddo! Il mio fagiolo si c-congela!|F-f-frio! Muito f-frio! Meu feijão está c-congelando!"),
                S("bup", "Good. Cold is good. Cold is our friend tonight.|Bien. El frío es bueno. Esta noche el frío es nuestro amigo.|"
                  "Gut. Kälte ist gut. Kälte ist heute unser Freund.|Bien. Le froid, c'est bien. Ce soir, le froid est notre ami.|"
                  "Bene. Il freddo è buono. Stanotte il freddo è nostro amico.|Bom. Frio é bom. Hoje o frio é nosso amigo."),
                {"move": "villain", "to": 1500, "speed": "walk"},
                S("villain", "A fridge? You think a little chill can stop ME?|¿Una nevera? ¿Creen que un poco de frío me detiene?|"
                  "Ein Kühlschrank? Ihr glaubt, ein bisschen Kälte hält MICH auf?|Un frigo ? Vous croyez qu'un peu de froid va M'arrêter ?|"
                  "Un frigo? Pensate che un po' di freddo possa fermare ME?|Uma geladeira? Acham que um friozinho vai ME parar?"),
                S("zeek", "Wait for it... three... two... one...|Esperen... tres... dos... uno...|Wartet... drei... zwei... eins...|"
                  "Attendez... trois... deux... un...|Aspettate... tre... due... uno...|Esperem... três... dois... um..."),
                {"sfx": "ice", "wait": 0.6},
                S("villain", "So... cold... so... sleepy...|Tanto... frío... tanto... sueño...|So... kalt... so... müde...|"
                  "Si... froid... si... fatigué...|Che... freddo... che... sonno...|Tanto... frio... tanto... sono..."),
                {"villain": "sleep"},
                {"wait": 0.8},
                mood(ALL4, "happy"),
                act(["lolly", "zeek"], "bounce"),
                S("lolly", "He's snoring! We did it!|¡Está roncando! ¡Lo logramos!|Er schnarcht! Wir haben's geschafft!|Il ronfle ! On a réussi !|Sta russando! Ce l'abbiamo fatta!|Ele está roncando! Conseguimos!"),
                S("bup", "Crispy, you were right! Crispy...?|¡Crispy, tenías razón! ¿Crispy...?|Crispy, du hattest recht! Crispy...?|"
                  "Crispy, tu avais raison ! Crispy... ?|Crispy, avevi ragione! Crispy...?|Crispy, você tinha razão! Crispy...?"),
                act("crispy", "shake"),
                S("crispy", "Cold... is my weak spot too... My fire... is going out...|El frío... también es mi punto débil... Mi fuego... se apaga...|"
                  "Kälte... ist auch meine Schwachstelle... Mein Feuer... geht aus...|Le froid... est aussi mon point faible... Mon feu... s'éteint...|"
                  "Il freddo... è anche il mio punto debole... Il mio fuoco... si spegne...|O frio... é meu ponto fraco também... Meu fogo... está apagando..."),
                mood("bup", "scared"),
                S("bup", "No! Hold on, Crispy! We'll get you somewhere warm!|¡No! ¡Aguanta, Crispy! ¡Te llevaremos a un lugar cálido!|"
                  "Nein! Halt durch, Crispy! Wir bringen dich ins Warme!|Non ! Tiens bon, Crispy ! On t'emmène au chaud !|"
                  "No! Resisti, Crispy! Ti portiamo al caldo!|Não! Aguenta, Crispy! Vamos te levar para um lugar quente!"),
                act("crispy", "faint"),
                {"sfx": "sting", "wait": 0.6},
            ],
            "tail": 0.5,
        },
        {   # 6 kitchen: the next villain wakes
            "bg": "kitchen", "music": "drone",
            "heroes": {"bup": 700, "pim": 460, "lolly": -300},
            "moods": {"bup": "scared", "pim": "scared"},
            "villain": {"type": "kettle", "x": 1450, "state": "asleep", "scale": 0.8},
            "beats": [
                {"card": "BACK IN THE KITCHEN...", "es": "DE VUELTA EN LA COCINA...", "dur": 2.0},
                S("bup", "Something warm... we need something warm, fast!|Algo caliente... ¡necesitamos algo caliente, rápido!|"
                  "Etwas Warmes... wir brauchen schnell etwas Warmes!|Quelque chose de chaud... vite, il faut du chaud !|"
                  "Qualcosa di caldo... ci serve qualcosa di caldo, presto!|Algo quente... precisamos de algo quente, rápido!"),
                S("pim", "Th-that kettle is warm. But it's... b-breathing.|E-esa tetera está caliente. Pero está... r-respirando.|"
                  "D-der Kessel ist warm. Aber er... a-atmet.|C-cette bouilloire est chaude. Mais elle... r-respire.|"
                  "Q-quel bollitore è caldo. Ma sta... r-respirando.|E-essa chaleira está quente. Mas está... r-respirando."),
                {"sfx": "whoosh", "wait": 0.4},
                {"villain": "wake"},
                {"villain": "rage", "level": 1.0},
                S("villain", "Ssssilence! Who dares wake Old Hissy? I'm BOILING!|¡Ssssilencio! ¿Quién despierta al Viejo Hissy? ¡Estoy HIRVIENDO!|"
                  "Ruuuhe! Wer weckt den alten Hissy? Ich KOCHE!|Ssssilence ! Qui ose réveiller le Vieux Hissy ? Je BOUS !|"
                  "Ssssilenzio! Chi osa svegliare il Vecchio Hissy? Sto BOLLENDO!|Ssssilêncio! Quem ousa acordar o Velho Hissy? Estou FERVENDO!"),
                act(["bup", "pim"], "scream"),
                {"shake": 0.8, "power": 22},
            ],
            "tail": 0.8,
        },
    ],
}

short1 = {
    "id": "ep005_short1", "format": "short",
    "title": "Bup's plan lasted 3 SECONDS 😅 #shorts",
    "hook": "Bup has a PLAN...",
    "description": "Okay team, here's the plan. Step one... oh no. #shorts #animation #cartoon #doughbros #funny",
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "bup", "jump scare"],
    "thumbnail": {"bg": "attic", "villain": "pot", "heroes": ["bup", "pim"], "text": "PLAN FAILED!"},
    "scenes": [{
        "bg": "attic", "music": "heartbeat",
        "heroes": {"bup": 700, "pim": 420},
        "moods": {"pim": "scared"},
        "villain": {"type": "pot", "x": 1480, "state": "asleep", "scale": 0.85},
        "beats": [
            S("bup", "Okay team, here's the plan. Step one: be VERY quiet.|Bien, equipo, este es el plan. Paso uno: MUCHO silencio.|"
              "Okay Team, hier ist der Plan. Schritt eins: GANZ leise sein.|Bon, l'équipe, voici le plan. Étape un : TRÈS silencieux.|"
              "Ok squadra, ecco il piano. Primo: fare MOLTO silenzio.|Certo, equipe, o plano é este. Passo um: MUITO silêncio."),
            mv("bup", 960, "walk"),
            {"sfx": "clank", "wait": 0.3},
            act("bup", "jump"),
            {"villain": "wake"},
            {"villain": "roar"},
            act(["bup", "pim"], "scream"),
            S("pim", "What's step two?!|¡¿Cuál es el paso dos?!|Was ist Schritt zwei?!|C'est quoi l'étape deux ?!|Qual è il passo due?!|Qual é o passo dois?!"),
            S("bup", "Step two: RUN!|Paso dos: ¡CORRAN!|Schritt zwei: RENNT!|Étape deux : COUREZ !|Passo due: CORRETE!|Passo dois: CORRAM!"),
            mv("bup", "off_left", "run"), mv("pim", "off_left", "run", True),
            {"villain": "lunge", "to": 1100},
        ],
        "tail": 0.8,
    }],
}

short2 = {
    "id": "ep005_short2", "format": "short",
    "title": "Would YOU trust Crispy? 👇 #shorts",
    "hook": "Can you trust HIM?",
    "description": "Crispy has a secret. Pim says run. Lolly says hug. What would YOU do? Comment YES or NO! #shorts #animation #cartoon #doughbros",
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "crispy", "would you"],
    "thumbnail": {"bg": "pantry", "villain": "pot", "heroes": ["crispy", "lolly"], "text": "TRUST HIM?"},
    "scenes": [{
        "bg": "pantry", "music": "drone",
        "heroes": {"pim": 300, "lolly": 560, "crispy": 2300},
        "moods": {"pim": "scared"},
        "beats": [
            mv("crispy", 1000, "walk"),
            {"sfx": "sting", "wait": 0.3},
            S("pim", "He's a burnt rock with GLOWING eyes! Run!|¡Es una roca quemada con ojos BRILLANTES! ¡Corre!|"
              "Er ist ein verbrannter Stein mit LEUCHTENDEN Augen! Lauf!|C'est un caillou brûlé aux yeux QUI BRILLENT ! Cours !|"
              "È una pietra bruciata con occhi LUMINOSI! Scappa!|Ele é uma pedra queimada com olhos BRILHANTES! Corre!"),
            mood("lolly", "happy"),
            S("lolly", "He saved Bup's life! I'm giving him a hug!|¡Salvó la vida de Bup! ¡Le voy a dar un abrazo!|"
              "Er hat Bup das Leben gerettet! Ich umarme ihn!|Il a sauvé la vie de Bup ! Je vais lui faire un câlin !|"
              "Ha salvato la vita a Bup! Gli do un abbraccio!|Ele salvou a vida do Bup! Vou dar um abraço nele!"),
            S("crispy", "...Please don't. I'm still a little bit on fire.|...Por favor, no. Todavía estoy un poco en llamas.|"
              "...Bitte nicht. Ich brenne noch ein bisschen.|...S'il te plaît, non. Je suis encore un peu en feu.|"
              "...Per favore no. Sto ancora un po' bruciando.|...Por favor, não. Ainda estou um pouco pegando fogo."),
            act("pim", "faint"),
            S("narr", "Would YOU trust Crispy? Comment YES or NO!|¿Confiarías en Crispy? ¡Comenta SÍ o NO!|"
              "Würdest DU Crispy vertrauen? Kommentiere JA oder NEIN!|Ferais-TU confiance à Crispy ? Commente OUI ou NON !|"
              "TU ti fideresti di Crispy? Commenta SÌ o NO!|VOCÊ confiaria no Crispy? Comente SIM ou NÃO!"),
        ],
        "tail": 1.0,
    }],
}

short3 = {
    "id": "ep005_short3", "format": "short",
    "title": "Mr. Pot came back for HIM 😱 #shorts",
    "hook": "He never forgot...",
    "description": "Mr. Pot has been waiting a long time for this. Full episode on the channel! #shorts #animation #cartoon #doughbros",
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "horror comedy",
             "animated series", "mr pot", "crispy", "jump scare"],
    "thumbnail": {"bg": "oven", "villain": "pot", "heroes": ["crispy", "bup"], "text": "HE'S BACK!"},
    "scenes": [{
        "bg": "oven", "music": "drone",
        "heroes": {"bup": 600, "crispy": 880},
        "moods": {"bup": "scared"},
        "villain": {"type": "pot", "x": 1450, "state": "asleep", "scale": 0.95},
        "beats": [
            {"sfx": "thump", "wait": 0.4},
            {"villain": "wake"},
            S("villain", "Crispy... my favorite little mistake.|Crispy... mi pequeño error favorito.|Crispy... mein liebster kleiner Fehler.|"
              "Crispy... ma petite erreur préférée.|Crispy... il mio piccolo errore preferito.|Crispy... meu errinho favorito."),
            S("bup", "Mistake? What is he talking about?!|¿Error? ¿¡De qué habla!?|Fehler? Wovon redet er?!|Erreur ? De quoi il parle ?!|Errore? Di cosa parla?!|Erro? Do que ele está falando?!"),
            S("villain", "Come back to the pot... BOTH of you!|Vuelvan a la olla... ¡LOS DOS!|Zurück in den Topf... IHR BEIDE!|"
              "Revenez dans la marmite... TOUS LES DEUX !|Tornate nella pentola... TUTTI E DUE!|Voltem para a panela... OS DOIS!"),
            {"villain": "lunge", "to": 1200},
            act("bup", "scream"),
            {"shake": 0.7, "power": 20},
            S("narr", "Full episode on the channel!|¡Episodio completo en el canal!|Ganze Folge auf dem Kanal!|Épisode complet sur la chaîne !|Episodio completo sul canale!|Episódio completo no canal!"),
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")

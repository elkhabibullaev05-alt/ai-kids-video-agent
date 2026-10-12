"""Builds Hollowmere EP1 scripts. Run: python3 scripts/_build_ep001.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["horror animation", "scary stories", "animated horror", "creepy", "hollowmere", "gothic", "dark fairy tale",
        "horror story", "spooky", "lantern"]

long_ = {
    "id": "ep001_long", "format": "long",
    "title": "Never Answer the Woods | Hollowmere Tales EP 1",
    "description": ("In Hollowmere there is one rule older than the trees: never answer when the woods call your name. "
                    "Tonight Odo, the last lantern-bearer, and his moth spirit Mothwick must cross the forest before the light runs out... "
                    "and something out there is using his lost sister's voice.\n\n"
                    "New tale every day. Keep your lantern lit and subscribe.\n\n#horror #animation #scarystories #hollowmere"),
    "tags": TAGS + ["episode 1", "pale shepherd"],
    "thumbnail": {"bg": "forest", "seed": 3, "creature": "gloamhound", "text": "NEVER ANSWER"},
    "shots": [
        {   # 1 cold open
            "bg": "forest", "seed": 3, "music": "drone", "eyes": 14, "lantern": 0.0, "ambient": 0.36,
            "cam": {"from": [960, 560, 1.0], "to": [960, 590, 1.18]},
            "beats": [
                {"sfx": "howl", "wait": 1.2},
                S("narr", "In Hollowmere, there is one rule older than the trees.|En Hollowmere hay una regla más antigua que los árboles.|"
                  "In Hollowmere gibt es eine Regel, die älter ist als die Bäume.|À Hollowmere, il existe une règle plus ancienne que les arbres.|"
                  "A Hollowmere c'è una regola più antica degli alberi.|Em Hollowmere existe uma regra mais antiga que as árvores."),
                {"eyes": "open"},
                S("narr", "Never answer when the woods call your name.|Nunca respondas cuando el bosque diga tu nombre.|"
                  "Antworte nie, wenn der Wald deinen Namen ruft.|Ne réponds jamais quand la forêt appelle ton nom.|"
                  "Non rispondere mai quando il bosco chiama il tuo nome.|Nunca responda quando a floresta chamar o seu nome."),
                {"wait": 0.6},
                S("wren", "Odo...|Odo...|Odo...|Odo...|Odo...|Odo..."),
                {"wait": 0.8},
                {"card": "NEVER ANSWER THE WOODS", "dur": 2.8},
            ],
            "tail": 0.2,
        },
        {   # 2 village edge
            "bg": "village", "seed": 2, "music": "lullaby", "eyes": 0, "ambient": 0.45,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [820, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 690, "y": 650}},
            "beats": [
                S("narr", "Odo was the last lantern-bearer of the village at the edge of the woods.|Odo era el último portador de farol de la aldea al borde del bosque.|"
                  "Odo war der letzte Laternenträger des Dorfes am Waldrand.|Odo était le dernier porteur de lanterne du village à l'orée des bois.|"
                  "Odo era l'ultimo portatore di lanterna del villaggio ai margini del bosco.|Odo era o último portador de lanterna da vila à beira da floresta."),
                S("narr", "Every night, someone had to carry the flame to the old stones, and back.|Cada noche, alguien debía llevar la llama hasta las piedras antiguas, y volver.|"
                  "Jede Nacht musste jemand die Flamme zu den alten Steinen tragen, und zurück.|Chaque nuit, quelqu'un devait porter la flamme jusqu'aux vieilles pierres, et revenir.|"
                  "Ogni notte qualcuno doveva portare la fiamma alle vecchie pietre, e tornare.|Toda noite, alguém precisava levar a chama até as pedras antigas, e voltar."),
                S("odo", "Mothwick... the lantern is getting low.|Mothwick... el farol se está apagando.|Mothwick... die Laterne wird schwach.|"
                  "Mothwick... la lanterne faiblit.|Mothwick... la lanterna si sta spegnendo.|Mothwick... a lanterna está fraca."),
                S("moth", "Then we walk faster. And whatever we hear, we don't stop.|Entonces caminamos más rápido. Y oigamos lo que oigamos, no paramos.|"
                  "Dann gehen wir schneller. Und egal was wir hören, wir bleiben nicht stehen.|Alors on marche plus vite. Et quoi qu'on entende, on ne s'arrête pas.|"
                  "Allora camminiamo più veloci. E qualunque cosa sentiamo, non ci fermiamo.|Então andamos mais rápido. E não importa o que ouvirmos, não paramos."),
                S("odo", "Whatever we hear?|¿Oigamos lo que oigamos?|Egal was wir hören?|Quoi qu'on entende ?|Qualunque cosa sentiamo?|Não importa o que ouvirmos?"),
                S("moth", "Especially then.|Sobre todo entonces.|Gerade dann.|Surtout à ce moment-là.|Soprattutto allora.|Principalmente aí."),
                {"move": "odo", "to": 1250, "speed": "walk"},
                {"move": "moth", "to": 1400, "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 3 the forest: the voice and the hounds
            "bg": "forest", "seed": 5, "music": "heartbeat", "eyes": 10, "ambient": 0.40,
            "cam": {"from": [800, 600, 1.12], "to": [960, 620, 1.2]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1480, "state": "hidden"},
                          "h2": {"type": "gloamhound", "x": 1760, "state": "hidden", "scale": 0.85}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "walk"},
                {"move": "moth", "to": 720, "speed": "walk", "and": True},
                {"sfx": "snap", "wait": 0.8},
                S("narr", "The deeper they walked, the quieter the forest became.|Cuanto más se adentraban, más callado quedaba el bosque.|"
                  "Je tiefer sie gingen, desto stiller wurde der Wald.|Plus ils avançaient, plus la forêt devenait silencieuse.|"
                  "Più si addentravano, più il bosco diventava silenzioso.|Quanto mais fundo caminhavam, mais quieta a floresta ficava."),
                S("wren", "Odo... it's me. It's Wren.|Odo... soy yo. Soy Wren.|Odo... ich bin's. Wren.|Odo... c'est moi. C'est Wren.|Odo... sono io. Sono Wren.|Odo... sou eu. Sou a Wren."),
                {"act": "odo", "do": "scared"},
                S("odo", "Wren? My sister went into the woods a year ago...|¿Wren? Mi hermana entró al bosque hace un año...|"
                  "Wren? Meine Schwester ging vor einem Jahr in den Wald...|Wren ? Ma sœur est partie dans les bois il y a un an...|"
                  "Wren? Mia sorella è entrata nel bosco un anno fa...|Wren? Minha irmã entrou na floresta há um ano..."),
                S("moth", "Odo. Don't. Answer.|Odo. No. Respondas.|Odo. Nicht. Antworten.|Odo. Ne. Réponds. Pas.|Odo. Non. Rispondere.|Odo. Não. Responda."),
                {"light": "dim"},
                {"show": "h1"},
                {"show": "h2", "and": True},
                {"growl": "h1"},
                S("narr", "Gloamhounds. Shadows with teeth, that only step into the light when it begins to fail.|Gloamhounds. Sombras con dientes, que solo entran en la luz cuando empieza a fallar.|"
                  "Gloamhounds. Schatten mit Zähnen, die nur ins Licht treten, wenn es schwächer wird.|Les Gloamhounds. Des ombres à crocs, qui n'entrent dans la lumière que lorsqu'elle faiblit.|"
                  "I Gloamhound. Ombre con i denti, che entrano nella luce solo quando comincia a spegnersi.|Gloamhounds. Sombras com dentes, que só entram na luz quando ela começa a falhar."),
                {"move": "h1", "to": 1250, "speed": "creep"},
                {"move": "h2", "to": 1520, "speed": "creep", "and": True},
                {"act": "odo", "do": "shake"},
                S("moth", "Lift the lantern! Higher! Make it burn!|¡Levanta el farol! ¡Más alto! ¡Haz que arda!|Heb die Laterne! Höher! Lass sie brennen!|"
                  "Lève la lanterne ! Plus haut ! Fais-la brûler !|Alza la lanterna! Più in alto! Falla ardere!|Levante a lanterna! Mais alto! Faça ela queimar!"),
                {"light": "flare"},
                {"sfx": "whoosh", "and": True},
                {"growl": "h1"},
                {"hide": "h1", "dur": 0.6},
                {"hide": "h2", "dur": 0.6, "and": True},
                {"eyes": "close"},
                S("odo", "They're gone...|Se han ido...|Sie sind weg...|Ils sont partis...|Se ne sono andati...|Eles foram embora..."),
                S("moth", "No. They're waiting. Keep walking.|No. Están esperando. Sigue caminando.|Nein. Sie warten. Geh weiter.|"
                  "Non. Ils attendent. Continue de marcher.|No. Stanno aspettando. Continua a camminare.|Não. Eles estão esperando. Continue andando."),
                {"move": "odo", "to": 2100, "speed": "run"},
                {"move": "moth", "to": 2200, "speed": "run", "and": True},
            ],
            "tail": 0.2,
        },
        {   # 3b the black mere: wick-eaters and a riddle
            "bg": "swamp", "seed": 6, "music": "drone", "eyes": 6, "ambient": 0.40,
            "cam": {"from": [900, 600, 1.12], "to": [1000, 610, 1.18]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 640}},
            "creatures": {"w1": {"type": "wickeater", "x": 1180, "state": "hidden", "scale": 1.1, "face": -1},
                          "w2": {"type": "wickeater", "x": 1400, "state": "hidden", "scale": 0.9, "face": -1}},
            "beats": [
                {"move": "odo", "to": 620, "speed": "walk"},
                {"move": "moth", "to": 780, "speed": "walk", "and": True},
                S("narr", "Beyond the trees lay the Black Mere, where little things live that eat light.|Tras los árboles estaba la Ciénaga Negra, donde viven cositas que comen luz.|"
                  "Hinter den Bäumen lag der Schwarze Pfuhl, wo kleine Dinger leben, die Licht fressen.|Derrière les arbres s'étendait le Marais Noir, où vivent de petites choses qui mangent la lumière.|"
                  "Oltre gli alberi c'era la Palude Nera, dove vivono piccole cose che mangiano la luce.|Além das árvores ficava o Pântano Negro, onde vivem coisinhas que comem luz."),
                {"show": "w1", "dur": 0.5},
                {"show": "w2", "dur": 0.5},
                S("w1", "Ooh! A lantern! Shiny, shiny, hungry!|¡Uy! ¡Un farol! ¡Brillante, brillante, hambre!|Ooh! Eine Laterne! Glänzend, glänzend, hungrig!|"
                  "Oh ! Une lanterne ! Brillante, brillante, j'ai faim !|Ooh! Una lanterna! Lucente, lucente, fame!|Ooh! Uma lanterna! Brilhante, brilhante, fome!"),
                {"light": "dim"},
                {"move": "w1", "to": 1000, "speed": "creep"},
                S("moth", "Wick-eaters! They can't resist a riddle. Ask them one!|¡Comemechas! No resisten un acertijo. ¡Hazles uno!|"
                  "Dochtfresser! Sie können keinem Rätsel widerstehen. Stell ihnen eins!|Des Mange-Mèches ! Ils ne résistent pas à une énigme. Poses-en une !|"
                  "Mangiastoppini! Non resistono a un indovinello. Fagliene uno!|Come-pavios! Eles não resistem a uma charada. Faça uma!"),
                S("odo", "What disappears the moment you say its name?|¿Qué desaparece en cuanto dices su nombre?|Was verschwindet, sobald man seinen Namen sagt?|"
                  "Qu'est-ce qui disparaît dès qu'on dit son nom ?|Cosa sparisce nel momento in cui dici il suo nome?|O que desaparece no momento em que você diz o nome dele?"),
                S("w2", "Easy! It's... it's... hmm.|¡Fácil! Es... es... mmm.|Einfach! Es ist... es ist... hmm.|Facile ! C'est... c'est... hmm.|Facile! È... è... mmm.|Fácil! É... é... hmm."),
                S("w1", "Don't tell him! Let ME think!|¡No se lo digas! ¡Déjame pensar a MÍ!|Sag's ihm nicht! Lass MICH nachdenken!|"
                  "Ne lui dis pas ! Laisse-MOI réfléchir !|Non dirglielo! Fammi pensare IO!|Não conta pra ele! Deixa EU pensar!"),
                S("narr", "And while they argued, Odo slipped away into the dark.|Y mientras discutían, Odo se escabulló en la oscuridad.|"
                  "Und während sie stritten, schlüpfte Odo davon in die Dunkelheit.|Et pendant qu'ils se disputaient, Odo s'éclipsa dans le noir.|"
                  "E mentre litigavano, Odo scivolò via nel buio.|E enquanto eles discutiam, Odo escapou para o escuro."),
                {"light": "on"},
                {"move": "odo", "to": "off_left", "speed": "run"},
                {"move": "moth", "to": "off_left", "speed": "run", "and": True},
                S("moth", "The answer is silence.|La respuesta es el silencio.|Die Antwort ist Stille.|La réponse, c'est le silence.|La risposta è il silenzio.|A resposta é o silêncio."),
            ],
            "tail": 0.3,
        },
        {   # 4 the stones: the Pale Shepherd
            "bg": "clearing", "seed": 4, "music": "choir", "eyes": 8, "ambient": 0.40,
            "lights": [{"kind": "fire", "x": 960, "y": 905, "r": 620}],
            "cam": {"from": [960, 600, 1.12], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": 620}, "moth": {"x": 760, "y": 660}},
            "creatures": {"pale": {"type": "shepherd", "x": 1460, "state": "hidden"}},
            "beats": [
                S("narr", "At the old stones, Odo gave the dying lantern to the fire, and the fire grew.|En las piedras antiguas, Odo dio el farol al fuego, y el fuego creció.|"
                  "An den alten Steinen gab Odo die Laterne ans Feuer, und das Feuer wuchs.|Aux vieilles pierres, Odo offrit la lanterne au feu, et le feu grandit.|"
                  "Alle vecchie pietre, Odo diede la lanterna al fuoco, e il fuoco crebbe.|Nas pedras antigas, Odo deu a lanterna ao fogo, e o fogo cresceu."),
                {"light": "on"},
                S("moth", "Listen to me. Things in Hollowmere can borrow voices. Any voice they have ever heard.|Escúchame. Las cosas de Hollowmere pueden robar voces. Cualquier voz que hayan oído.|"
                  "Hör zu. Dinge in Hollowmere können Stimmen leihen. Jede Stimme, die sie je gehört haben.|Écoute-moi. Les choses de Hollowmere peuvent emprunter des voix. Toutes celles qu'elles ont entendues.|"
                  "Ascoltami. Le cose di Hollowmere possono rubare le voci. Qualsiasi voce abbiano mai sentito.|Me escute. As coisas de Hollowmere podem pegar vozes emprestadas. Qualquer voz que já ouviram."),
                {"wait": 0.5},
                S("wren", "Odo... I'm so cold. Can I sit by your fire?|Odo... tengo tanto frío. ¿Puedo sentarme junto a tu fuego?|"
                  "Odo... mir ist so kalt. Darf ich an dein Feuer?|Odo... j'ai si froid. Je peux m'asseoir près de ton feu ?|"
                  "Odo... ho così freddo. Posso sedermi vicino al tuo fuoco?|Odo... estou com tanto frio. Posso sentar perto do seu fogo?"),
                {"act": "odo", "do": "scared"},
                S("odo", "W... Wr...|W... Wr...|W... Wr...|W... Wr...|W... Wr...|W... Wr...", gap=0.1),
                S("moth", "ODO!|¡ODO!|ODO!|ODO !|ODO!|ODO!"),
                {"flash": True},
                {"show": "pale", "dur": 0.2, "and": True},
                {"shake": 0.6, "power": 16},
                S("pale", "Such a bright little flame.|Qué llamita tan brillante.|Was für eine helle kleine Flamme.|Quelle jolie petite flamme brillante.|Che piccola fiamma luminosa.|Que chamazinha tão brilhante."),
                S("pale", "It would look lovely... in my collection.|Quedaría preciosa... en mi colección.|Sie würde wunderschön aussehen... in meiner Sammlung.|"
                  "Elle serait ravissante... dans ma collection.|Starebbe benissimo... nella mia collezione.|Ficaria linda... na minha coleção."),
                S("narr", "The Pale Shepherd. He never runs. He never hurries. He simply... waits.|El Pastor Pálido. Nunca corre. Nunca tiene prisa. Simplemente... espera.|"
                  "Der Bleiche Hirte. Er rennt nie. Er eilt nie. Er wartet einfach.|Le Berger Pâle. Il ne court jamais. Il ne se presse jamais. Il attend... simplement.|"
                  "Il Pastore Pallido. Non corre mai. Non ha mai fretta. Semplicemente... aspetta.|O Pastor Pálido. Ele nunca corre. Nunca se apressa. Ele simplesmente... espera."),
                {"act": "odo", "do": "shake"},
                S("odo", "You can't have it!|¡No puedes tenerla!|Du bekommst sie nicht!|Tu ne l'auras pas !|Non puoi averla!|Você não vai ficar com ela!"),
                {"act": "pale", "do": "rise", "level": 1.0},
                S("pale", "Everyone answers... in the end.|Todos responden... al final.|Jeder antwortet... am Ende.|Tout le monde répond... à la fin.|Tutti rispondono... alla fine.|Todos respondem... no fim."),
                {"sfx": "bell", "wait": 1.2},
                {"act": "pale", "do": "rise", "level": 0.0, "and": True},
                S("narr", "Far away, a bell rang. A bell nobody had rung in a hundred years.|A lo lejos sonó una campana. Una que nadie había tocado en cien años.|"
                  "Weit weg läutete eine Glocke. Eine, die seit hundert Jahren niemand geläutet hatte.|Au loin, une cloche sonna. Une cloche que personne n'avait sonnée depuis cent ans.|"
                  "Lontano suonò una campana. Una che nessuno suonava da cent'anni.|Ao longe, um sino tocou. Um sino que ninguém tocava há cem anos."),
                {"hide": "pale", "dur": 1.6},
                {"eyes": "close", "and": True},
            ],
            "tail": 0.4,
        },
        {   # 5 chapel: cliffhanger
            "bg": "chapel", "seed": 1, "music": "lullaby", "eyes": 4, "ambient": 0.42,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [760, 640, 1.24]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "beats": [
                S("odo", "The chapel... Who rang the bell?|La capilla... ¿Quién tocó la campana?|Die Kapelle... Wer hat die Glocke geläutet?|"
                  "La chapelle... Qui a sonné la cloche ?|La cappella... Chi ha suonato la campana?|A capela... Quem tocou o sino?"),
                S("moth", "Nobody lives there, Odo. Nobody alive.|Nadie vive allí, Odo. Nadie vivo.|Dort wohnt niemand, Odo. Niemand Lebendiges.|"
                  "Personne n'habite là, Odo. Personne de vivant.|Lì non vive nessuno, Odo. Nessuno di vivo.|Ninguém mora lá, Odo. Ninguém vivo."),
                {"wait": 0.8},
                S("wren", "The bell was me, Odo. Come and find me.|La campana fui yo, Odo. Ven a buscarme.|Die Glocke war ich, Odo. Komm und finde mich.|"
                  "La cloche, c'était moi, Odo. Viens me trouver.|La campana ero io, Odo. Vieni a cercarmi.|O sino fui eu, Odo. Venha me encontrar."),
                {"act": "odo", "do": "turn"},
                {"eyes": "open"},
                S("narr", "And for the first time... Odo wasn't sure the voice was lying.|Y por primera vez... Odo no estaba seguro de que la voz mintiera.|"
                  "Und zum ersten Mal... war sich Odo nicht sicher, ob die Stimme log.|Et pour la première fois... Odo n'était pas sûr que la voix mentait.|"
                  "E per la prima volta... Odo non era sicuro che la voce mentisse.|E pela primeira vez... Odo não tinha certeza de que a voz mentia."),
                {"sfx": "caw", "wait": 0.6},
                {"card": "TO BE CONTINUED...", "dur": 2.8},
            ],
            "tail": 0.2,
        },
    ],
}

short1 = {   # the rule
    "id": "ep001_short1", "format": "short",
    "title": "Never answer the woods at night 🕯️ #shorts",
    "hook": "NEVER ANSWER THE WOODS",
    "description": "Rule #1 of Hollowmere: never answer when the woods call your name. #shorts #horror #animation #scarystories #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "forest", "seed": 5, "creature": "gloamhound", "text": "DON'T ANSWER"},
    "shots": [{
        "bg": "forest", "seed": 5, "music": "heartbeat", "eyes": 12, "ambient": 0.40, "focus": "odo",
        "chars": {"odo": {"x": 760}},
        "creatures": {"h1": {"type": "gloamhound", "x": 1150, "state": "hidden"}},
        "beats": [
            {"sfx": "howl", "wait": 1.4},
            S("narr", "Rule one of Hollowmere: never answer when the woods call your name.|Regla uno de Hollowmere: nunca respondas cuando el bosque diga tu nombre.|"
              "Regel eins von Hollowmere: Antworte nie, wenn der Wald deinen Namen ruft.|Règle numéro un de Hollowmere : ne réponds jamais quand la forêt appelle ton nom.|"
              "Regola uno di Hollowmere: non rispondere mai quando il bosco chiama il tuo nome.|Regra um de Hollowmere: nunca responda quando a floresta chamar seu nome."),
            S("wren", "Odo... over here...|Odo... aquí...|Odo... hier drüben...|Odo... par ici...|Odo... qui...|Odo... aqui..."),
            {"act": "odo", "do": "turn"},
            S("odo", "...Hello?|...¿Hola?|...Hallo?|...Allô ?|...Ciao?|...Olá?"),
            {"light": "out"},
            {"lunge": "h1", "to": 980, "and": True},
            {"flash": True, "and": True},
            {"wait": 0.8},
            S("narr", "He answered.|Él respondió.|Er hat geantwortet.|Il a répondu.|Ha risposto.|Ele respondeu."),
        ],
        "tail": 1.8,
    }],
}

short2 = {   # would you
    "id": "ep001_short2", "format": "short",
    "title": "Would YOU sit by this fire? 🔥 #shorts",
    "hook": "WOULD YOU STAY?",
    "description": "A tall figure in a white mask stands across your campfire. Would you stay or run? Comment STAY or RUN 👇 #shorts #horror #animation #hollowmere",
    "tags": ["shorts"] + TAGS[:8] + ["would you rather"],
    "thumbnail": {"bg": "clearing", "seed": 4, "creature": "shepherd", "text": "STAY OR RUN"},
    "shots": [{
        "bg": "clearing", "seed": 4, "music": "choir", "eyes": 6, "ambient": 0.40,
        "lights": [{"kind": "fire", "x": 960, "y": 905, "r": 600}],
        "chars": {"odo": {"x": 760}},
        "creatures": {"pale": {"type": "shepherd", "x": 1170, "state": "hidden"}},
        "focus": ["odo", "pale"],
        "beats": [
            S("narr", "You are lost in the woods. You find a warm fire.|Estás perdido en el bosque. Encuentras un fuego cálido.|"
              "Du hast dich im Wald verirrt. Du findest ein warmes Feuer.|Tu es perdu dans les bois. Tu trouves un feu bien chaud.|"
              "Ti sei perso nel bosco. Trovi un fuoco caldo.|Você está perdido na floresta. Encontra uma fogueira quente."),
            {"show": "pale", "dur": 2.0},
            S("narr", "Then you notice someone standing on the other side.|Entonces notas a alguien de pie al otro lado.|"
              "Dann bemerkst du jemanden auf der anderen Seite.|Puis tu remarques quelqu'un debout de l'autre côté.|"
              "Poi noti qualcuno in piedi dall'altra parte.|Então você percebe alguém de pé do outro lado."),
            S("pale", "Sit. Stay. Forever.|Siéntate. Quédate. Para siempre.|Setz dich. Bleib. Für immer.|Assieds-toi. Reste. Pour toujours.|Siediti. Resta. Per sempre.|Sente. Fique. Para sempre."),
            {"act": "odo", "do": "shake"},
            S("narr", "Would YOU stay by the fire, or run into the dark? Comment STAY or RUN.|¿TÚ te quedarías junto al fuego o correrías a la oscuridad? Comenta QUEDARME o CORRER.|"
              "Würdest DU am Feuer bleiben oder in die Dunkelheit rennen? Schreib BLEIBEN oder RENNEN.|Et TOI, tu resterais près du feu ou tu fuirais dans le noir ? Écris RESTER ou FUIR.|"
              "TU resteresti accanto al fuoco o correresti nel buio? Scrivi RESTO o SCAPPO.|VOCÊ ficaria perto do fogo ou correria para o escuro? Comente FICAR ou CORRER."),
        ],
        "tail": 1.2,
    }],
}

short3 = {   # scariest moment
    "id": "ep001_short3", "format": "short",
    "title": "The hounds only come when the light fails 🐺 #shorts",
    "hook": "KEEP THE LANTERN LIT",
    "description": "In Hollowmere, the Gloamhounds only step into the light when it starts to fail. Full story on the channel. #shorts #horror #animation #hollowmere",
    "tags": ["shorts"] + TAGS + ["gloamhound"],
    "thumbnail": {"bg": "forest", "seed": 5, "creature": "gloamhound", "text": "KEEP IT LIT"},
    "shots": [{
        "bg": "forest", "seed": 5, "music": "heartbeat", "eyes": 10, "ambient": 0.40,
        "chars": {"odo": {"x": 700}, "moth": {"x": 820, "y": 650}},
        "creatures": {"h1": {"type": "gloamhound", "x": 1250, "state": "hidden"}},
        "focus": ["odo", "h1"],
        "beats": [
            S("narr", "In Hollowmere, the shadows have teeth.|En Hollowmere, las sombras tienen dientes.|In Hollowmere haben die Schatten Zähne.|À Hollowmere, les ombres ont des crocs.|A Hollowmere, le ombre hanno i denti.|Em Hollowmere, as sombras têm dentes."),
            {"light": "dim"},
            {"show": "h1"},
            {"growl": "h1"},
            S("moth", "Lift the lantern! Make it burn!|¡Levanta el farol! ¡Haz que arda!|Heb die Laterne! Lass sie brennen!|Lève la lanterne ! Fais-la brûler !|Alza la lanterna! Falla ardere!|Levante a lanterna! Faça ela queimar!"),
            {"act": "odo", "do": "shake"},
            {"light": "flare"},
            {"hide": "h1", "dur": 0.5},
            S("odo", "They're gone...|Se han ido...|Sie sind weg...|Ils sont partis...|Se ne sono andati...|Eles foram embora..."),
            {"lunge": "h1", "to": 1000},
            {"show": "h1", "dur": 0.1, "and": True},
            S("narr", "Full story on the channel.|Historia completa en el canal.|Die ganze Geschichte auf dem Kanal.|L'histoire complète sur la chaîne.|Storia completa sul canale.|História completa no canal."),
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

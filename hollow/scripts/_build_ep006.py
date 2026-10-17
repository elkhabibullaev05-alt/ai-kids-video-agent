"""Builds Hollowmere EP6 (recorded legend: the Bell Witch, Robertson County, Tennessee, 1817-1821). Run: python3 scripts/_build_ep006.py
Retention rules (2026-10-16): frame 1 = motion + big text hook (no fade, no title card), narration from 0 s mid-tension,
something new every 4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to its first frame.
Facts from Wikipedia / Mental Floss / World History Encyclopedia; the whole tale rests mainly on M. V. Ingram's 1894 book,
so it is told as a legend ("the story says"), the Jackson visit is flagged as unproven, John Bell's death is left out."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Bell Witch", "Tennessee", "Adams Tennessee",
        "Robertson County", "1817", "American legend", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Bell_Witch",
           "https://www.mentalfloss.com/article/12828/bell-witch-tennessee",
           "https://www.worldhistory.org/article/2810/the-bell-witch/"]

long_ = {
    "id": "ep006_long", "format": "long",
    "title": "Who Was Talking Inside the Walls?",
    "hook": "DON'T ANSWER THE VOICE", "hook_dur": 4.5,
    "description": ("Based on real records and a famous American legend. From 1817 to 1821, the Bell family farm near the Red River "
                    "in Robertson County, Tennessee (near today's Adams) was troubled by knocking in the walls, scratching, "
                    "gnawing on the bedposts and, at last, a voice that spoke, sang and called the family by name. "
                    "It was called 'Kate'. The fullest account was written down by M. V. Ingram in 1894; many details are legend, "
                    "and sceptics think someone in the house faked it. No one ever proved how.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #bellwitch #tennessee #legend #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 6", "voice in the walls", "haunted farm"],
    "thumbnail": {"bg": "manor", "seed": 3, "creature": "ghost", "text": "WHO'S THERE?"},
    "shots": [
        {   # 1 cold open: no fade, motion + hook text from frame 1, narration from 0 s
            "bg": "manor", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 3, "lantern": 1.0, "ambient": 0.40, "fade": False,
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 480}],
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "beats": [
                {"move": "odo", "to": 640, "speed": "creep"},
                {"move": "moth", "to": 780, "speed": "creep", "and": True},
                S("narr", "Something was knocking inside the walls of this farmhouse... and then it started to talk.|Algo golpeaba dentro de las paredes de esta granja... y luego empezó a hablar.|"
                  "Etwas klopfte in den Wänden dieses Farmhauses... und dann begann es zu sprechen.|Quelque chose frappait dans les murs de cette ferme... puis ça s'est mis à parler.|"
                  "Qualcosa bussava dentro i muri di questa fattoria... e poi iniziò a parlare.|Algo batia dentro das paredes desta casa... e depois começou a falar.", **{"and": True}),
                {"sfx": "thump", "wait": 0.2},
                {"sfx": "thump", "wait": 0.2},
                {"act": "odo", "do": "scared"},
                S("narr", "This is a real legend from Tennessee, 1817. It was first written down in full in 1894.|Es una leyenda real de Tennessee, 1817. Se escribió completa en 1894.|"
                  "Das ist eine echte Legende aus Tennessee, 1817. Ganz aufgeschrieben wurde sie 1894.|C'est une vraie légende du Tennessee, 1817. Écrite en entier en 1894.|"
                  "È una leggenda vera del Tennessee, 1817. Fu scritta per intero nel 1894.|É uma lenda real do Tennessee, 1817. Foi escrita por inteiro em 1894."),
                {"sfx": "creak", "and": True},
                S("odo", "Mothwick... did the wall just knock back at me?|Mothwick... ¿la pared me acaba de responder?|"
                  "Mothwick... hat die Wand gerade zurückgeklopft?|Mothwick... le mur vient de me répondre ?|"
                  "Mothwick... il muro ha appena bussato?|Mothwick... a parede acabou de bater de volta?"),
                {"eyes": "open", "and": True},
                S("moth", "Whatever it says... don't answer it.|Diga lo que diga... no le contestes.|Was es auch sagt... antworte nicht.|"
                  "Quoi qu'il dise... ne réponds pas.|Qualsiasi cosa dica... non rispondere.|O que quer que diga... não responda."),
                {"sfx": "sting", "and": True},
            ],
            "tail": 0.2,
        },
        {   # 2 the farm and the first strange animals
            "bg": "forest", "seed": 4, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.44,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"john": {"type": "figure", "x": 1050, "seed": 0, "face": 1, "state": "hidden"},
                          "h1": {"type": "gloamhound", "x": 1520, "state": "hidden", "face": -1, "scale": 0.8},
                          "c1": {"type": "crow", "x": 1350, "y": 420, "state": "hidden", "fly": 1, "scale": 1.3}},
            "beats": [
                S("narr", "A farmer named John Bell lived near the Red River with his wife Lucy and their children.|Un granjero, John Bell, vivía junto al río Red con su esposa Lucy y sus hijos.|"
                  "Ein Farmer namens John Bell lebte am Red River mit seiner Frau Lucy und den Kindern.|Un fermier, John Bell, vivait près de la Red River avec sa femme Lucy et leurs enfants.|"
                  "Un contadino, John Bell, viveva vicino al Red River con la moglie Lucy e i figli.|Um fazendeiro, John Bell, vivia perto do rio Red com a esposa Lucy e os filhos."),
                {"show": "john", "dur": 0.8, "and": True},
                S("narr", "In 1817, he saw a strange animal in his field. Like a dog... but wrong.|En 1817 vio un animal extraño en su campo. Como un perro... pero raro.|"
                  "1817 sah er ein seltsames Tier auf seinem Feld. Wie ein Hund... aber falsch.|En 1817, il vit une bête étrange dans son champ. Comme un chien... mais pas tout à fait.|"
                  "Nel 1817 vide uno strano animale nel campo. Come un cane... ma sbagliato.|Em 1817 viu um animal estranho no campo. Como um cão... mas errado."),
                {"show": "h1", "dur": 0.5},
                {"growl": "h1", "and": True},
                S("narr", "He fired his gun at it. The creature simply vanished.|Le disparó con su escopeta. La criatura simplemente desapareció.|"
                  "Er schoss darauf. Das Wesen verschwand einfach.|Il tira dessus. La créature disparut, tout simplement.|"
                  "Gli sparò. La creatura svanì e basta.|Ele atirou nela. A criatura simplesmente sumiu."),
                {"flash": True},
                {"hide": "h1", "dur": 0.2, "and": True},
                {"act": "odo", "do": "jump"},
                S("narr", "His son Drew saw a bird of enormous size sitting on a fence.|Su hijo Drew vio un pájaro enorme posado en una cerca.|"
                  "Sein Sohn Drew sah einen riesigen Vogel auf einem Zaun sitzen.|Son fils Drew vit un oiseau énorme posé sur une clôture.|"
                  "Suo figlio Drew vide un uccello enorme su uno steccato.|O filho Drew viu um pássaro enorme pousado numa cerca."),
                {"show": "c1", "dur": 0.4},
                {"sfx": "caw", "and": True},
                S("odo", "That's no ordinary crow. It's watching the house.|Ese no es un cuervo normal. Está mirando la casa.|"
                  "Das ist keine normale Krähe. Sie beobachtet das Haus.|Ce n'est pas un corbeau normal. Il surveille la maison.|"
                  "Non è un corvo normale. Sta guardando la casa.|Isso não é um corvo comum. Está vigiando a casa."),
                {"hide": "c1", "dur": 0.6},
                {"hide": "john", "dur": 0.8, "and": True},
            ],
            "tail": 0.3,
        },
        {   # 3 the noises in the house
            "bg": "manor", "seed": 5, "music": "heartbeat", "wind": True, "eyes": 4, "ambient": 0.36,
            "lights": [{"kind": "window", "x": 1200, "y": 620, "r": 480}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "beats": [
                S("narr", "Then the noises came indoors. Knocking along the doors and the walls.|Luego los ruidos entraron en la casa. Golpes en puertas y paredes.|"
                  "Dann kamen die Geräusche ins Haus. Klopfen an Türen und Wänden.|Puis les bruits entrèrent dans la maison. Des coups le long des portes et des murs.|"
                  "Poi i rumori entrarono in casa. Colpi lungo porte e muri.|Depois os barulhos entraram na casa. Batidas nas portas e paredes."),
                {"sfx": "thump", "and": True},
                {"sfx": "thump", "wait": 0.3},
                S("narr", "Scratching. Gnawing, like teeth on the bedposts. The sound of chains on the floor.|Arañazos. Roídos en las patas de la cama. Ruido de cadenas en el suelo.|"
                  "Kratzen. Nagen an den Bettpfosten. Das Geräusch von Ketten auf dem Boden.|Des grattements. Des dents rongeant les lits. Un bruit de chaînes au sol.|"
                  "Graffi. Qualcosa che rosicchia i letti. Rumore di catene sul pavimento.|Arranhões. Roeduras nos pés da cama. Barulho de correntes no chão."),
                {"sfx": "creak", "and": True},
                {"act": "odo", "do": "shake"},
                S("narr", "The story says the children felt their blankets pulled off in the dark.|Dicen que los niños sentían cómo les quitaban las mantas a oscuras.|"
                  "Man erzählt, den Kindern wurden im Dunkeln die Decken weggezogen.|On raconte que les enfants sentaient leurs couvertures tirées dans le noir.|"
                  "Si racconta che ai bambini venivano tirate via le coperte al buio.|Dizem que as crianças sentiam os cobertores puxados no escuro."),
                {"light": "dim"},
                {"sfx": "whisper", "and": True},
                S("narr", "The youngest daughter, Betsy, was troubled most of all.|La hija menor, Betsy, fue la más atormentada.|"
                  "Die jüngste Tochter, Betsy, traf es am schlimmsten.|La plus jeune fille, Betsy, fut la plus tourmentée.|"
                  "La figlia più piccola, Betsy, fu la più tormentata.|A filha mais nova, Betsy, foi a mais atormentada."),
                S("moth", "Every night it came back. And every night it was closer.|Cada noche volvía. Y cada noche más cerca.|"
                  "Jede Nacht kam es zurück. Und jede Nacht war es näher.|Chaque nuit il revenait. Et chaque nuit plus près.|"
                  "Ogni notte tornava. E ogni notte più vicino.|Toda noite voltava. E toda noite mais perto."),
                {"light": "on"},
                {"eyes": "close", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 4 the voice
            "bg": "manor", "seed": 8, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.34,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": 540}, "moth": {"x": 700, "y": 650}},
            "creatures": {"kate": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.85}},
            "beats": [
                S("narr", "At first it was only a faint singing, like an old woman, too soft to understand.|Al principio solo era un canto débil, como de una anciana.|"
                  "Zuerst war es nur ein leiser Gesang, wie von einer alten Frau.|D'abord, ce n'était qu'un chant faible, comme une vieille femme.|"
                  "All'inizio era solo un canto debole, come di una vecchia.|No começo era só um canto fraco, como de uma velha."),
                {"sfx": "whisper", "and": True},
                S("narr", "Then the voice grew louder. It sang hymns. It quoted scripture.|Luego la voz creció. Cantaba himnos. Citaba la Biblia.|"
                  "Dann wurde die Stimme lauter. Sie sang Lieder. Sie zitierte die Bibel.|Puis la voix devint plus forte. Elle chantait des cantiques, citait la Bible.|"
                  "Poi la voce si fece più forte. Cantava inni. Citava la Bibbia.|Depois a voz ficou mais alta. Cantava hinos. Citava a Bíblia."),
                {"show": "kate", "dur": 1.2},
                S("narr", "And it called every person in the house by name.|Y llamaba a cada persona de la casa por su nombre.|"
                  "Und sie rief jeden im Haus beim Namen.|Et elle appelait chaque personne de la maison par son nom.|"
                  "E chiamava per nome ogni persona della casa.|E chamava cada pessoa da casa pelo nome."),
                {"act": "odo", "do": "scared"},
                S("kate", "I was once very happy.|Una vez fui muy feliz.|Ich war einmal sehr glücklich.|J'ai été très heureuse, autrefois.|"
                  "Un tempo ero molto felice.|Um dia eu fui muito feliz."),
                {"sfx": "bell", "and": True},
                S("narr", "Asked who it was, it said it was a spirit. The family called it Kate.|Le preguntaron quién era: dijo que un espíritu. La familia la llamó Kate.|"
                  "Gefragt, wer es sei, sagte es: ein Geist. Die Familie nannte es Kate.|À la question qui es-tu, elle répondit : un esprit. On l'appela Kate.|"
                  "Interrogata, disse di essere uno spirito. La famiglia la chiamò Kate.|Perguntada quem era, disse que era um espírito. A família a chamou de Kate."),
                {"hide": "kate", "dur": 0.4},
                S("odo", "People came from miles away just to hear it talk.|La gente venía de lejos solo para oírla hablar.|"
                  "Leute kamen von weit her, nur um es sprechen zu hören.|Des gens venaient de loin juste pour l'entendre parler.|"
                  "La gente veniva da lontano solo per sentirla parlare.|Gente vinha de longe só para ouvi-la falar."),
            ],
            "tail": 0.3,
        },
        {   # 5 the Andrew Jackson legend
            "bg": "forest", "seed": 9, "music": "drone", "wind": True, "eyes": 5, "ambient": 0.38,
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"gen": {"type": "figure", "x": 1380, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "One famous tale says that General Andrew Jackson rode out to see the witch.|Un relato famoso dice que el general Andrew Jackson fue a ver a la bruja.|"
                  "Eine berühmte Geschichte sagt, General Andrew Jackson ritt hin, um die Hexe zu sehen.|Un récit célèbre dit que le général Andrew Jackson vint voir la sorcière.|"
                  "Un racconto famoso dice che il generale Andrew Jackson andò a vedere la strega.|Uma história famosa diz que o general Andrew Jackson foi ver a bruxa."),
                {"show": "gen", "dur": 1.0},
                {"sfx": "step", "and": True},
                S("narr", "Near the farm, his wagon stopped. The horses pulled. It would not move.|Cerca de la granja su carreta se paró. Los caballos tiraban. No se movía.|"
                  "Nahe der Farm blieb sein Wagen stehen. Die Pferde zogen. Er rührte sich nicht.|Près de la ferme, son chariot s'arrêta. Les chevaux tiraient. Rien.|"
                  "Vicino alla fattoria il carro si fermò. I cavalli tiravano. Non si muoveva.|Perto da fazenda a carroça parou. Os cavalos puxavam. Nada se movia."),
                {"sfx": "creak", "and": True},
                {"eyes": "open"},
                S("narr", "Then a woman's voice told them they could go on... and she would see them tonight.|Entonces una voz de mujer dijo que siguieran... y que los vería esa noche.|"
                  "Dann sagte eine Frauenstimme, sie dürften weiter... und sie sehe sie heute Nacht.|Alors une voix de femme dit qu'ils pouvaient repartir... et qu'elle les verrait cette nuit.|"
                  "Poi una voce di donna disse che potevano andare... e che li avrebbe visti stanotte.|Então uma voz de mulher disse que podiam seguir... e que os veria à noite."),
                {"sfx": "whisper", "and": True},
                {"act": "odo", "do": "shake"},
                S("narr", "But careful: there is no proof Jackson ever visited. This part may be only legend.|Pero ojo: no hay prueba de que Jackson fuera. Quizá sea solo leyenda.|"
                  "Aber Vorsicht: Es gibt keinen Beweis, dass Jackson dort war. Vielleicht nur Legende.|Mais attention : rien ne prouve que Jackson soit venu. C'est peut-être une légende.|"
                  "Ma attenzione: non c'è prova che Jackson ci sia mai andato. Forse è solo leggenda.|Mas cuidado: não há prova de que Jackson foi lá. Talvez seja só lenda."),
                {"hide": "gen", "dur": 0.8},
                {"eyes": "close", "and": True},
                S("moth", "Legend or not... the horses believed it.|Leyenda o no... los caballos se lo creyeron.|Legende oder nicht... die Pferde glaubten es.|"
                  "Légende ou pas... les chevaux, eux, y ont cru.|Leggenda o no... i cavalli ci credettero.|Lenda ou não... os cavalos acreditaram."),
            ],
            "tail": 0.3,
        },
        {   # 6 Betsy, the goodbye and the promise
            "bg": "chapel", "seed": 4, "music": "lullaby", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "window", "x": 1200, "y": 600, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"betsy": {"type": "figure", "x": 1250, "seed": 2, "face": -1, "state": "hidden"},
                          "kate": {"type": "ghost", "x": 1550, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "Betsy grew up and wanted to marry a young man named Joshua Gardner.|Betsy creció y quiso casarse con un joven llamado Joshua Gardner.|"
                  "Betsy wurde älter und wollte einen jungen Mann, Joshua Gardner, heiraten.|Betsy grandit et voulut épouser un jeune homme, Joshua Gardner.|"
                  "Betsy crebbe e volle sposare un giovane di nome Joshua Gardner.|Betsy cresceu e quis casar com um jovem chamado Joshua Gardner."),
                {"show": "betsy", "dur": 1.0, "and": True},
                S("narr", "The voice warned her again and again: do not marry him.|La voz le advirtió una y otra vez: no te cases con él.|"
                  "Die Stimme warnte sie immer wieder: Heirate ihn nicht.|La voix la mit en garde encore et encore : ne l'épouse pas.|"
                  "La voce la avvertì più e più volte: non sposarlo.|A voz a avisou de novo e de novo: não case com ele."),
                {"show": "kate", "dur": 0.6},
                {"sfx": "whisper", "and": True},
                S("narr", "In 1821, Betsy broke off the engagement. And the voice said goodbye.|En 1821 Betsy rompió el compromiso. Y la voz se despidió.|"
                  "1821 löste Betsy die Verlobung. Und die Stimme verabschiedete sich.|En 1821, Betsy rompit ses fiançailles. Et la voix fit ses adieux.|"
                  "Nel 1821 Betsy ruppe il fidanzamento. E la voce si congedò.|Em 1821 Betsy rompeu o noivado. E a voz se despediu."),
                {"hide": "betsy", "dur": 1.0},
                S("kate", "I will come back... in seven years.|Volveré... dentro de siete años.|Ich komme wieder... in sieben Jahren.|"
                  "Je reviendrai... dans sept ans.|Tornerò... tra sette anni.|Eu voltarei... daqui a sete anos."),
                {"sfx": "bell", "and": True},
                {"act": "odo", "do": "scared"},
                S("narr", "The story says that in 1828, right on time... it came back.|La historia dice que en 1828, puntual... volvió.|"
                  "Die Geschichte sagt: 1828, pünktlich... kam es zurück.|L'histoire dit qu'en 1828, à l'heure... elle revint.|"
                  "La storia dice che nel 1828, puntuale... tornò.|A história diz que em 1828, pontual... ela voltou."),
                {"flash": True},
                {"hide": "kate", "dur": 0.2, "and": True},
            ],
            "tail": 0.3,
        },
        {   # 7 cliffhanger: the knock answers
            "bg": "manor", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.34,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"kate": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.95}},
            "beats": [
                S("narr", "Some say a person in the house faked it all. But no one ever proved how.|Algunos dicen que alguien de la casa lo fingió todo. Nadie probó cómo.|"
                  "Manche sagen, jemand im Haus hat alles vorgetäuscht. Niemand bewies, wie.|Certains disent qu'un habitant de la maison a tout simulé. Personne n'a prouvé comment.|"
                  "Alcuni dicono che qualcuno in casa finse tutto. Nessuno provò come.|Alguns dizem que alguém da casa fingiu tudo. Ninguém provou como."),
                {"sfx": "whoosh", "and": True},
                S("narr", "And people near Adams, Tennessee, still tell of strange voices in the dark.|Y cerca de Adams, en Tennessee, aún hablan de voces extrañas en la oscuridad.|"
                  "Und bei Adams in Tennessee erzählt man noch heute von seltsamen Stimmen im Dunkeln.|Et près d'Adams, au Tennessee, on parle encore de voix étranges dans le noir.|"
                  "E vicino ad Adams, in Tennessee, si parla ancora di voci strane nel buio.|E perto de Adams, no Tennessee, ainda se fala de vozes estranhas no escuro."),
                {"sfx": "thump", "wait": 0.3},
                {"sfx": "thump", "wait": 0.3},
                {"act": "odo", "do": "turn"},
                S("odo", "Mothwick... it's knocking again. Right behind this wall.|Mothwick... está golpeando otra vez. Justo detrás de esta pared.|"
                  "Mothwick... es klopft wieder. Direkt hinter dieser Wand.|Mothwick... ça frappe encore. Juste derrière ce mur.|"
                  "Mothwick... bussa di nuovo. Proprio dietro questo muro.|Mothwick... está batendo de novo. Bem atrás desta parede."),
                {"light": "dim"},
                {"show": "kate", "dur": 0.3},
                S("kate", "Odo... I know your name.|Odo... sé cómo te llamas.|Odo... ich kenne deinen Namen.|Odo... je connais ton nom.|"
                  "Odo... conosco il tuo nome.|Odo... eu sei o seu nome."),
                {"light": "out"},
                {"shake": 0.6, "power": 16, "and": True},
                {"card": "WHO KNOWS YOUR NAME?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}

short1 = {   # the rule / scariest moment; ends on the opening frame so it loops
    "id": "ep006_short1", "format": "short",
    "title": "Would you answer the voice in the wall? 👻 #shorts",
    "hook": "DON'T ANSWER THE VOICE",
    "description": "Tennessee, 1817: the Bell family heard knocking in the walls, then a voice that called every one of them by name. A real American legend, first written in full in 1894. Full story on the channel. #shorts #bellwitch #truestory #legend #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "manor", "seed": 3, "creature": "ghost", "text": "DON'T ANSWER"},
    "shots": [{
        "bg": "manor", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 3, "ambient": 0.40, "focus": "odo", "fade": False,
        "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 480}],
        "chars": {"odo": {"x": 700}},
        "creatures": {"kate": {"type": "ghost", "x": 1120, "state": "hidden", "face": -1, "scale": 0.9}},
        "beats": [
            {"move": "odo", "to": 760, "speed": "creep"},
            S("narr", "Tennessee, 1817. The Bell family heard knocking inside their walls.|Tennessee, 1817. Los Bell oían golpes dentro de sus paredes.|"
              "Tennessee, 1817. Familie Bell hörte Klopfen in ihren Wänden.|Tennessee, 1817. Les Bell entendaient frapper dans leurs murs.|"
              "Tennessee, 1817. I Bell sentivano bussare dentro i muri.|Tennessee, 1817. Os Bell ouviam batidas dentro das paredes.", **{"and": True}),
            {"sfx": "thump", "and": True},
            S("narr", "Then a voice began to talk. It knew every name in the house.|Luego una voz empezó a hablar. Sabía todos los nombres de la casa.|"
              "Dann sprach eine Stimme. Sie kannte jeden Namen im Haus.|Puis une voix se mit à parler. Elle connaissait chaque nom de la maison.|"
              "Poi una voce iniziò a parlare. Conosceva ogni nome della casa.|Então uma voz começou a falar. Sabia todos os nomes da casa."),
            {"sfx": "whisper", "and": True},
            {"act": "odo", "do": "scared"},
            {"light": "dim"},
            {"show": "kate", "dur": 0.2},
            {"flash": True, "and": True},
            S("kate", "Odo...|Odo...|Odo...|Odo...|Odo...|Odo..."),
            {"hide": "kate", "dur": 0.3},
            {"light": "on", "and": True},
            {"act": "odo", "do": "calm", "and": True},
            {"move": "odo", "to": 700, "speed": "walk", "and": True},
            S("narr", "Something was knocking inside the walls...|Algo golpeaba dentro de las paredes...|Etwas klopfte in den Wänden...|"
              "Quelque chose frappait dans les murs...|Qualcosa bussava dentro i muri...|Algo batia dentro das paredes..."),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

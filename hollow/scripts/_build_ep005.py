"""Builds Hollowmere EP5 (true story: the Devil's Footprints, Devon, February 1855). Run: python3 scripts/_build_ep005.py
Retention rules (2026-10-16): frame 1 = motion + big text hook (no fade, no title card), narration from 0 s mid-tension,
something new every 4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to its first frame."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Devil's Footprints", "Devon", "Topsham",
        "Exe estuary", "1855", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://www.bitesizedbritain.co.uk/the-devils-footprints-of-1855/",
           "https://www.ancientpages.com/2017/02/08/on-this-day-in-history-devils-footprints-appeared-in-devon-england-feb-89-1855/",
           "https://www.davidcastleton.net/devils-footprints-devon-snow-england-hoofmarks-hoofprints/"]

long_ = {
    "id": "ep005_long", "format": "long",
    "title": "What Walked Over the Rooftops in 1855?",
    "hook": "DON'T FOLLOW THE TRACKS", "hook_dur": 4.5,
    "description": ("A true story. On the night of 8 to 9 February 1855, after a snowfall, the people of south Devon woke up "
                    "to a line of small hoof-shaped prints running through towns around the Exe estuary: Topsham, Lympstone, "
                    "Exmouth, Dawlish, Teignmouth. The tracks went over walls and roofs, stopped at a haystack and went on beyond it. "
                    "No one ever found what made them.\n\n"
                    "Told from the accounts of 1855; theories are marked as theories.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #unsolvedmystery #devilsfootprints #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 5", "hoofprints in the snow", "Victorian mystery"],
    "thumbnail": {"bg": "village", "seed": 7, "creature": "gloamhound", "text": "WHAT WALKED HERE?"},
    "shots": [
        {   # 1 cold open: no fade, motion + hook text from frame 1, narration from 0 s
            "bg": "village", "seed": 7, "music": "heartbeat", "wind": True, "eyes": 4, "lantern": 1.0, "ambient": 0.40, "fade": False,
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "beats": [
                {"move": "odo", "to": 640, "speed": "creep"},
                {"move": "moth", "to": 780, "speed": "creep", "and": True},
                S("narr", "Something walked through this town in the night... and it walked over the rooftops.|Algo cruzó este pueblo de noche... y caminó sobre los tejados.|"
                  "Etwas ging in der Nacht durch diese Stadt... und es lief über die Dächer.|Quelque chose a traversé la ville cette nuit... en marchant sur les toits.|"
                  "Qualcosa ha attraversato il paese di notte... e ha camminato sui tetti.|Algo atravessou esta cidade à noite... e andou sobre os telhados.", **{"and": True}),
                {"sfx": "step", "wait": 0.3},
                {"act": "odo", "do": "scared"},
                S("narr", "This is a true story. Devon, England. February 1855.|Esta es una historia real. Devon, Inglaterra. Febrero de 1855.|"
                  "Dies ist eine wahre Geschichte. Devon, England. Februar 1855.|Ceci est une histoire vraie. Devon, Angleterre. Février 1855.|"
                  "Questa è una storia vera. Devon, Inghilterra. Febbraio 1855.|Esta é uma história real. Devon, Inglaterra. Fevereiro de 1855."),
                {"sfx": "creak", "and": True},
                S("odo", "Mothwick... those marks in the snow. They go right up the wall!|Mothwick... esas marcas en la nieve. ¡Suben por la pared!|"
                  "Mothwick... die Spuren im Schnee. Sie gehen die Wand hinauf!|Mothwick... ces traces dans la neige. Elles montent le long du mur !|"
                  "Mothwick... quelle impronte nella neve. Salgono sul muro!|Mothwick... essas marcas na neve. Elas sobem pela parede!"),
                {"eyes": "open", "and": True},
                S("moth", "Then don't follow them. Not yet.|Entonces no las sigas. Todavía no.|Dann folg ihnen nicht. Noch nicht.|"
                  "Alors ne les suis pas. Pas encore.|Allora non seguirle. Non ancora.|Então não as siga. Ainda não."),
                {"sfx": "sting", "and": True},
            ],
            "tail": 0.2,
        },
        {   # 2 the snowfall, the morning of 9 February
            "bg": "village", "seed": 3, "music": "lullaby", "eyes": 0, "ambient": 0.46,
            "lights": [{"kind": "window", "x": 1250, "y": 640, "r": 520}],
            "cam": {"from": [880, 600, 1.12], "to": [1020, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"farmer": {"type": "figure", "x": 1420, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "That winter was bitterly cold. On the night of the eighth of February, snow fell.|Aquel invierno fue muy frío. La noche del ocho de febrero, nevó.|"
                  "Jener Winter war bitterkalt. In der Nacht zum neunten Februar fiel Schnee.|Cet hiver-là fut glacial. La nuit du huit février, il neigea.|"
                  "Quell'inverno fu gelido. La notte dell'otto febbraio, nevicò.|Aquele inverno foi gelado. Na noite de oito de fevereiro, nevou."),
                {"sfx": "whoosh", "wait": 0.2},
                {"show": "farmer", "dur": 1.0},
                S("narr", "At dawn, people opened their doors around the river Exe.|Al amanecer, la gente abrió sus puertas junto al río Exe.|"
                  "Im Morgengrauen öffneten die Leute am Fluss Exe ihre Türen.|À l'aube, les gens ouvrirent leurs portes autour de l'Exe.|"
                  "All'alba, la gente aprì le porte lungo il fiume Exe.|Ao amanhecer, as pessoas abriram as portas perto do rio Exe."),
                S("narr", "Topsham. Lympstone. Exmouth. Dawlish. Teignmouth.|Topsham. Lympstone. Exmouth. Dawlish. Teignmouth.|"
                  "Topsham. Lympstone. Exmouth. Dawlish. Teignmouth.|Topsham. Lympstone. Exmouth. Dawlish. Teignmouth.|"
                  "Topsham. Lympstone. Exmouth. Dawlish. Teignmouth.|Topsham. Lympstone. Exmouth. Dawlish. Teignmouth."),
                {"sfx": "bell", "and": True},
                S("narr", "And in every town, they found the same thing in the snow.|Y en cada pueblo encontraron lo mismo en la nieve.|"
                  "Und in jedem Ort fanden sie dasselbe im Schnee.|Et dans chaque ville, ils trouvèrent la même chose dans la neige.|"
                  "E in ogni paese trovarono la stessa cosa nella neve.|E em cada cidade encontraram a mesma coisa na neve."),
                {"act": "odo", "do": "jump"},
                S("narr", "A line of small prints, shaped like hooves.|Una fila de pequeñas huellas con forma de pezuña.|"
                  "Eine Reihe kleiner Abdrücke, geformt wie Hufe.|Une ligne de petites empreintes en forme de sabot.|"
                  "Una fila di piccole impronte a forma di zoccolo.|Uma fila de pequenas pegadas em forma de casco."),
                S("odo", "Just a horse... or a donkey. Right?|Solo un caballo... o un burro. ¿Verdad?|Nur ein Pferd... oder ein Esel. Oder?|"
                  "Juste un cheval... ou un âne. Hein ?|Solo un cavallo... o un asino. Vero?|Só um cavalo... ou um burro. Né?"),
                {"hide": "farmer", "dur": 1.0},
            ],
            "tail": 0.3,
        },
        {   # 3 the strange details
            "bg": "village", "seed": 5, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "creatures": {"c1": {"type": "crow", "x": 1350, "y": 380, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Each print was about four inches long and three inches wide.|Cada huella medía unas cuatro pulgadas de largo y tres de ancho.|"
                  "Jeder Abdruck war etwa zehn Zentimeter lang und acht breit.|Chaque empreinte faisait environ dix centimètres de long sur huit.|"
                  "Ogni impronta era lunga circa dieci centimetri e larga otto.|Cada pegada tinha uns dez centímetros de comprimento e oito de largura."),
                S("narr", "But they were not in pairs. They ran in one single line.|Pero no iban en pares. Corrían en una sola fila.|"
                  "Aber sie waren nicht paarweise. Sie liefen in einer einzigen Linie.|Mais elles n'allaient pas par paires. Une seule ligne.|"
                  "Ma non erano a coppie. Correvano in un'unica fila.|Mas não estavam em pares. Seguiam numa única fila."),
                {"show": "c1", "dur": 0.5},
                {"sfx": "caw", "and": True},
                S("narr", "As if whatever made them walked on just one leg.|Como si lo que las hizo caminara sobre una sola pata.|"
                  "Als ginge das, was sie machte, auf nur einem Bein.|Comme si la chose marchait sur une seule patte.|"
                  "Come se ciò che le aveva fatte camminasse su una zampa sola.|Como se aquilo andasse numa perna só."),
                {"act": "odo", "do": "shake"},
                S("narr", "The tracks climbed up walls and crossed over snowy roofs.|Las huellas subían por los muros y cruzaban los tejados nevados.|"
                  "Die Spuren stiegen Mauern hinauf und liefen über verschneite Dächer.|Les traces montaient les murs et traversaient les toits enneigés.|"
                  "Le tracce salivano i muri e attraversavano i tetti innevati.|As pegadas subiam muros e cruzavam telhados nevados."),
                {"sfx": "thump", "and": True},
                S("narr", "At one haystack, they stopped on one side... and went on from the other.|En un pajar se detenían de un lado... y seguían del otro.|"
                  "An einem Heuhaufen hörten sie auf... und gingen auf der anderen Seite weiter.|Devant une meule de foin, elles s'arrêtaient... et reprenaient de l'autre côté.|"
                  "A un covone si fermavano da un lato... e riprendevano dall'altro.|Num palheiro, paravam de um lado... e continuavam do outro."),
                S("narr", "The hay was not disturbed at all.|El heno no estaba removido en absoluto.|Das Heu war überhaupt nicht berührt.|"
                  "Le foin n'avait pas bougé du tout.|Il fieno non era stato toccato.|O feno não tinha sido mexido."),
                {"hide": "c1", "dur": 0.6},
                S("moth", "Nothing walks through hay without moving it.|Nada atraviesa el heno sin moverlo.|Nichts geht durch Heu, ohne es zu bewegen.|"
                  "Rien ne traverse le foin sans le bouger.|Niente attraversa il fieno senza smuoverlo.|Nada atravessa o feno sem mexer nele."),
            ],
            "tail": 0.3,
        },
        {   # 4 the hunt into the woods
            "bg": "forest", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 6, "ambient": 0.34,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 0.9}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", "and": True},
                S("narr", "Men followed the tracks for miles. Some carried guns and sticks.|Hombres siguieron las huellas durante millas. Algunos llevaban armas y palos.|"
                  "Männer folgten den Spuren meilenweit. Manche trugen Gewehre und Stöcke.|Des hommes suivirent les traces sur des kilomètres, armés de fusils et de bâtons.|"
                  "Uomini seguirono le tracce per miglia. Alcuni avevano fucili e bastoni.|Homens seguiram as pegadas por quilômetros. Alguns levavam armas e paus."),
                {"sfx": "step", "and": True},
                S("narr", "Near Dawlish, a hunt sent its hounds into a wood after the trail.|Cerca de Dawlish, una cacería mandó a sus perros al bosque tras el rastro.|"
                  "Bei Dawlish schickte eine Jagd ihre Hunde der Spur nach in einen Wald.|Près de Dawlish, une chasse lança ses chiens dans un bois sur la piste.|"
                  "Vicino a Dawlish, una caccia mandò i cani nel bosco sulla pista.|Perto de Dawlish, uma caçada mandou os cães para a mata atrás do rastro."),
                {"sfx": "howl", "wait": 0.4},
                {"eyes": "open", "and": True},
                S("narr", "The story says the dogs came running back out, howling and terrified.|Dicen que los perros volvieron corriendo, aullando y aterrados.|"
                  "Man erzählt, die Hunde kamen heulend und verängstigt zurück.|On raconte que les chiens revinrent en courant, hurlant de peur.|"
                  "Si racconta che i cani tornarono di corsa, ululando, terrorizzati.|Dizem que os cães voltaram correndo, uivando, apavorados."),
                {"light": "dim"},
                {"show": "h1", "dur": 0.4, "and": True},
                {"growl": "h1"},
                S("odo", "What could scare a pack of hunting dogs?|¿Qué podría asustar a una jauría de caza?|Was kann eine Meute Jagdhunde erschrecken?|"
                  "Qu'est-ce qui peut effrayer une meute de chiens de chasse ?|Cosa può spaventare una muta di cani da caccia?|O que assustaria uma matilha de cães de caça?"),
                {"flash": True},
                {"hide": "h1", "dur": 0.2, "and": True},
                {"light": "on"},
                {"eyes": "close", "and": True},
                S("moth", "No one ever saw what made the tracks. Not one person.|Nadie vio nunca qué hizo las huellas. Ni una sola persona.|"
                  "Niemand hat je gesehen, was die Spuren machte. Kein einziger.|Personne n'a jamais vu ce qui a laissé les traces. Personne.|"
                  "Nessuno vide mai cosa lasciò le tracce. Nessuno.|Ninguém jamais viu o que deixou as pegadas. Ninguém."),
                {"move": "odo", "to": "off_right", "speed": "run"},
                {"move": "moth", "to": "off_right", "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 5 the chapel: whispers and the vicar's kangaroo
            "bg": "chapel", "seed": 4, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1200, "y": 600, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"vicar": {"type": "figure", "x": 1400, "seed": 2, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "Frightened people whispered that the Devil himself had walked through Devon.|La gente asustada susurraba que el mismo Diablo había cruzado Devon.|"
                  "Verängstigte Leute flüsterten, der Teufel selbst sei durch Devon gegangen.|Les gens effrayés murmuraient que le Diable en personne avait traversé le Devon.|"
                  "La gente spaventata sussurrava che il Diavolo in persona fosse passato per il Devon.|O povo assustado sussurrava que o próprio Diabo tinha passado por Devon."),
                {"sfx": "whisper", "and": True},
                {"show": "vicar", "dur": 1.0},
                S("narr", "In Lympstone, the Reverend Musgrave told his church: perhaps it was a kangaroo.|En Lympstone, el reverendo Musgrave dijo: quizá fue un canguro.|"
                  "In Lympstone sagte Pfarrer Musgrave seiner Gemeinde: vielleicht ein Känguru.|À Lympstone, le révérend Musgrave déclara : c'était peut-être un kangourou.|"
                  "A Lympstone, il reverendo Musgrave disse: forse era un canguro.|Em Lympstone, o reverendo Musgrave disse: talvez fosse um canguru."),
                S("odo", "A kangaroo? In England? In the snow?|¿Un canguro? ¿En Inglaterra? ¿En la nieve?|Ein Känguru? In England? Im Schnee?|"
                  "Un kangourou ? En Angleterre ? Dans la neige ?|Un canguro? In Inghilterra? Nella neve?|Um canguru? Na Inglaterra? Na neve?"),
                S("narr", "Later he admitted he said it only to calm his frightened people.|Luego admitió que lo dijo solo para calmar a su gente asustada.|"
                  "Später gab er zu, er sagte es nur, um die Leute zu beruhigen.|Plus tard, il avoua l'avoir dit pour calmer ses fidèles.|"
                  "Più tardi ammise di averlo detto solo per calmare la gente.|Depois admitiu que disse aquilo só para acalmar o povo."),
                {"sfx": "bell", "and": True},
                S("narr", "A famous scientist, Richard Owen, blamed badgers. Others said birds, rats, even a balloon.|El científico Richard Owen culpó a los tejones. Otros dijeron aves, ratas, un globo.|"
                  "Der Forscher Richard Owen tippte auf Dachse. Andere sagten Vögel, Ratten, ein Ballon.|Le savant Richard Owen accusa les blaireaux. D'autres, des oiseaux, des rats, un ballon.|"
                  "Lo scienziato Richard Owen accusò i tassi. Altri dissero uccelli, ratti, un pallone.|O cientista Richard Owen culpou texugos. Outros falaram em aves, ratos, um balão."),
                S("narr", "No answer explained all of it. Not the roofs. Not the haystack.|Ninguna respuesta lo explicaba todo. Ni los tejados. Ni el pajar.|"
                  "Keine Antwort erklärte alles. Nicht die Dächer. Nicht den Heuhaufen.|Aucune réponse n'expliquait tout. Ni les toits. Ni la meule.|"
                  "Nessuna risposta spiegava tutto. Né i tetti. Né il covone.|Nenhuma resposta explicava tudo. Nem os telhados. Nem o palheiro."),
                {"hide": "vicar", "dur": 1.0},
            ],
            "tail": 0.3,
        },
        {   # 6 the drainpipe
            "bg": "village", "seed": 9, "music": "heartbeat", "wind": True, "eyes": 3, "ambient": 0.36,
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "Two witnesses said the prints went into a narrow pipe, only six inches wide.|Dos testigos dijeron que las huellas entraban en un tubo de solo quince centímetros.|"
                  "Zwei Zeugen sagten, die Spuren führten in ein Rohr, nur fünfzehn Zentimeter breit.|Deux témoins dirent que les traces entraient dans un tuyau de quinze centimètres.|"
                  "Due testimoni dissero che le impronte entravano in un tubo largo quindici centimetri.|Duas testemunhas disseram que as pegadas entravam num cano de quinze centímetros."),
                {"sfx": "snap", "and": True},
                S("narr", "...and came out of the other end, as if nothing had happened.|...y salían por el otro extremo, como si nada.|"
                  "...und kamen am anderen Ende wieder heraus, als wäre nichts gewesen.|...et ressortaient de l'autre côté, comme si de rien n'était.|"
                  "...e uscivano dall'altra parte, come se niente fosse.|...e saíam do outro lado, como se nada fosse."),
                {"act": "odo", "do": "scared"},
                S("narr", "Some said the trail even crossed the frozen river.|Algunos dijeron que el rastro incluso cruzaba el río helado.|"
                  "Manche sagten, die Spur ging sogar über den gefrorenen Fluss.|Certains dirent que la piste traversait même la rivière.|"
                  "Alcuni dissero che la pista attraversava perfino il fiume.|Alguns disseram que o rastro até cruzava o rio."),
                {"light": "out"},
                {"show": "g1", "dur": 0.3, "and": True},
                {"sfx": "whisper", "and": True},
                S("odo", "Mothwick... the lantern. Something is breathing on it.|Mothwick... la linterna. Algo está soplando en ella.|"
                  "Mothwick... die Laterne. Etwas atmet sie an.|Mothwick... la lanterne. Quelque chose souffle dessus.|"
                  "Mothwick... la lanterna. Qualcosa ci respira sopra.|Mothwick... a lanterna. Tem algo soprando nela."),
                {"flash": True},
                {"hide": "g1", "dur": 0.2, "and": True},
                {"light": "flare"},
                S("moth", "Only the wind. Keep walking. Don't look back.|Solo el viento. Sigue andando. No mires atrás.|"
                  "Nur der Wind. Geh weiter. Schau nicht zurück.|Juste le vent. Continue. Ne te retourne pas.|"
                  "Solo il vento. Continua. Non voltarti.|Só o vento. Continue andando. Não olhe para trás."),
                {"eyes": "close"},
            ],
            "tail": 0.3,
        },
        {   # 7 the graveyard: cliffhanger
            "bg": "graveyard", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1520, "state": "hidden", "face": -1, "scale": 1.0}},
            "beats": [
                S("narr", "The snow melted. The tracks vanished. The people of Devon tried to forget.|La nieve se derritió. Las huellas desaparecieron. Devon intentó olvidar.|"
                  "Der Schnee schmolz. Die Spuren verschwanden. Devon versuchte zu vergessen.|La neige fondit. Les traces disparurent. Le Devon tenta d'oublier.|"
                  "La neve si sciolse. Le tracce sparirono. Il Devon cercò di dimenticare.|A neve derreteu. As pegadas sumiram. Devon tentou esquecer."),
                {"sfx": "whoosh", "and": True},
                S("narr", "Some say the whole trail stretched forty miles. Some say a hundred.|Algunos dicen que el rastro medía cuarenta millas. Otros, cien.|"
                  "Manche sagen, die Spur war vierzig Meilen lang. Andere sagen hundert.|Certains disent que la piste faisait soixante kilomètres. D'autres, cent soixante.|"
                  "Alcuni dicono che la pista fosse lunga quaranta miglia. Altri, cento.|Uns dizem que o rastro tinha quarenta milhas. Outros, cem."),
                S("narr", "Then, on the thirteenth of February, someone walked into Topsham churchyard...|Entonces, el trece de febrero, alguien entró en el cementerio de Topsham...|"
                  "Dann, am dreizehnten Februar, ging jemand auf den Friedhof von Topsham...|Puis, le treize février, quelqu'un entra dans le cimetière de Topsham...|"
                  "Poi, il tredici febbraio, qualcuno entrò nel cimitero di Topsham...|Então, em treze de fevereiro, alguém entrou no cemitério de Topsham..."),
                {"sfx": "step", "wait": 0.4},
                {"act": "odo", "do": "turn"},
                S("narr", "...and found new prints in the snow.|...y encontró huellas nuevas en la nieve.|...und fand neue Abdrücke im Schnee.|"
                  "...et trouva de nouvelles empreintes dans la neige.|...e trovò nuove impronte nella neve.|...e encontrou pegadas novas na neve."),
                {"show": "h1", "dur": 0.3},
                {"growl": "h1", "and": True},
                S("odo", "Mothwick... they're fresh. They lead right to us.|Mothwick... son recientes. Vienen directo hacia nosotros.|"
                  "Mothwick... sie sind frisch. Sie führen direkt zu uns.|Mothwick... elles sont fraîches. Elles mènent droit vers nous.|"
                  "Mothwick... sono fresche. Portano dritte a noi.|Mothwick... são novas. Vêm direto até nós."),
                {"lunge": "h1", "to": 1150},
                {"light": "out", "and": True},
                {"card": "WHAT WALKED THROUGH DEVON?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}

short1 = {   # the scariest true detail; ends on the opening frame so it loops
    "id": "ep005_short1", "format": "short",
    "title": "Who left these tracks on the roof? 👣 #shorts",
    "hook": "DON'T FOLLOW THE TRACKS",
    "description": "True story: Devon, England, 9 February 1855. After a snowfall, a line of hoof-shaped prints ran over walls and roofs through town after town. No one ever saw what made them. Full true story on the channel. #shorts #truestory #unsolvedmystery #devilsfootprints #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "village", "seed": 7, "creature": "gloamhound", "text": "DON'T FOLLOW"},
    "shots": [{
        "bg": "village", "seed": 7, "music": "heartbeat", "wind": True, "eyes": 3, "ambient": 0.40, "focus": "odo", "fade": False,
        "chars": {"odo": {"x": 700}},
        "creatures": {"h1": {"type": "gloamhound", "x": 1150, "state": "hidden", "face": -1, "scale": 0.9}},
        "beats": [
            {"move": "odo", "to": 760, "speed": "creep"},
            S("narr", "True story. Devon, 1855. Hoof prints in the snow, one single line.|Historia real. Devon, 1855. Huellas de pezuña en la nieve, en una sola fila.|"
              "Wahre Geschichte. Devon, 1855. Hufspuren im Schnee, in einer einzigen Linie.|Histoire vraie. Devon, 1855. Des traces de sabot dans la neige, en une seule ligne.|"
              "Storia vera. Devon, 1855. Impronte di zoccolo nella neve, in un'unica fila.|História real. Devon, 1855. Pegadas de casco na neve, numa fila só.", **{"and": True}),
            {"sfx": "step", "and": True},
            S("narr", "They went up walls. Over the rooftops. Through town after town.|Subían muros. Sobre los tejados. Pueblo tras pueblo.|"
              "Sie gingen Mauern hinauf. Über die Dächer. Durch Ort um Ort.|Elles montaient les murs. Sur les toits. De ville en ville.|"
              "Salivano sui muri. Sopra i tetti. Paese dopo paese.|Subiam muros. Pelos telhados. Cidade após cidade."),
            {"sfx": "thump", "and": True},
            {"act": "odo", "do": "scared"},
            S("narr", "No one ever saw what made them.|Nadie vio nunca qué las hizo.|Niemand sah je, was sie machte.|"
              "Personne n'a jamais vu ce qui les a faites.|Nessuno vide mai cosa le fece.|Ninguém jamais viu o que as fez."),
            {"light": "out"},
            {"show": "h1", "dur": 0.1, "and": True},
            {"flash": True, "and": True},
            {"growl": "h1"},
            {"hide": "h1", "dur": 0.3},
            {"light": "on", "and": True},
            {"act": "odo", "do": "calm", "and": True},
            {"move": "odo", "to": 700, "speed": "walk", "and": True},
            S("narr", "Something walked through town last night...|Algo cruzó el pueblo anoche...|Etwas ging letzte Nacht durch den Ort...|"
              "Quelque chose a traversé la ville cette nuit...|Qualcosa ha attraversato il paese stanotte...|Algo atravessou a cidade ontem à noite..."),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

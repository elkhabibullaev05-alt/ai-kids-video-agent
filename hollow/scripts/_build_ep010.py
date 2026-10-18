"""Builds Hollowmere EP10 (true story: the dancing plague of 1518, Strasbourg, Alsace; Frau Troffea from 14 July 1518;
guild halls + stages in the horse and grain markets, paid musicians; music/drum ban; red shoes at the shrine of
St Vitus, Saverne; ergot vs. Waller's mass-psychogenic theory).
Run: python3 scripts/_build_ep010.py
Retention rules (2026-10-16): frame 1 = motion + big text hook, narration from 0 s mid-tension, something new every
4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to the first frame.
Pack 3 of 2026-10-19 -> 1 long + 1 Short. Deaths are disputed (no contemporary Strasbourg source mentions them) and
are not told (true_stories.md rule 4)."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


A = {"and": True}
TAGS = ["true story", "unsolved mystery", "real horror story", "dancing plague", "dancing plague of 1518", "Strasbourg",
        "1518", "Alsace", "France", "dancing mania", "St Vitus dance", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://publicdomainreview.org/essay/the-dancing-plague-of-1518/",
           "https://en.wikipedia.org/wiki/Dancing_plague_of_1518",
           "https://www.britannica.com/event/dancing-plague-of-1518"]

WOMAN = lambda x=1450, sc=1.0: {"type": "figure", "x": x, "seed": 2, "face": -1, "state": "hidden", "scale": sc}
MAN = lambda x=1300, sd=0, sc=0.95: {"type": "figure", "x": x, "seed": sd, "face": -1, "state": "hidden", "scale": sc}
GHOST = lambda x=1450, sc=0.8: {"type": "ghost", "x": x, "state": "hidden", "face": -1, "scale": sc}


def JIG(who, a, b):
    """quick side-to-side steps + a shake = a dancer who can't stop"""
    return [{"move": who, "to": a, "speed": "run"}, {"act": who, "do": "reach", **A}, {"move": who, "to": b, "speed": "run"}]


long_ = {
    "id": "ep010_long", "format": "long",
    "title": "Why Couldn't Strasbourg Stop Dancing?",
    "hook": "DON'T START DANCING", "hook_dur": 4.5,
    "description": ("A true story, written down in 1518. On 14 July 1518, a woman the chronicles call Frau Troffea began to dance "
                    "in a street in Strasbourg (then in the Holy Roman Empire, today in France) — with no music — and could not stop. "
                    "Within days more than thirty people were dancing; by August, chroniclers counted between 50 and 400. "
                    "The city's physicians called it 'overheated blood' and said the cure was more dancing: guild halls were turned "
                    "into dance floors, stages were built in the horse market and the grain market, and musicians were paid to play. "
                    "It only spread. The council then banned drums and public dancing, and sent the dancers to the shrine of Saint Vitus "
                    "at Saverne, where priests gave them small crosses and red shoes marked with holy oil. By September it was over. "
                    "Ergot poisoning and mass psychogenic illness have both been suggested — no one knows for certain.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #dancingplague #strasbourg #1518 #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 10", "Frau Troffea", "Saint Vitus", "mass hysteria", "true story history"],
    "thumbnail": {"bg": "village", "seed": 6, "creature": "figure", "text": "DON'T DANCE"},
    "shots": [
        {   # 1 cold open: a woman dancing in a silent street, motion + hook from frame 1
            "bg": "village", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 3, "lantern": 1.0, "ambient": 0.38, "fade": False,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"w": WOMAN(1450)},
            "beats": [
                {"show": "w", "dur": 0.05},
                {"flash": True, "dur": 0.8, **A},
                {"move": "odo", "to": 620, "speed": "creep", **A},
                {"move": "moth", "to": 760, "speed": "creep", **A},
                {"sfx": "whoosh", **A},
                S("narr", "One woman stepped into the street... and could not stop dancing.|Una mujer salió a la calle... y no pudo dejar de bailar.|"
                  "Eine Frau trat auf die Gasse... und konnte nicht aufhören zu tanzen.|Une femme sortit dans la rue... et ne put plus s'arrêter de danser.|"
                  "Una donna uscì in strada... e non riuscì più a smettere di ballare.|Uma mulher saiu à rua... e não conseguiu parar de dançar.", **A),
                {"move": "w", "to": 1300, "speed": "run", **A},
                {"shake": 0.5, "power": 10, **A},
                {"move": "w", "to": 1500, "speed": "run"},
                {"sfx": "step", **A},
                S("narr", "This is a true story from Strasbourg, written down in 1518.|Esta es una historia real de Estrasburgo, escrita en 1518.|"
                  "Dies ist eine wahre Geschichte aus Straßburg, aufgeschrieben 1518.|Ceci est une histoire vraie de Strasbourg, écrite en 1518.|"
                  "Questa è una storia vera di Strasburgo, scritta nel 1518.|Esta é uma história real de Estrasburgo, escrita em 1518."),
                {"move": "w", "to": 1320, "speed": "run", **A},
                {"flash": True, "dur": 1.0},
                {"act": "odo", "do": "scared", **A},
                S("odo", "Mothwick... why is she dancing? There's no music at all.|Mothwick... ¿por qué baila? No hay ninguna música.|"
                  "Mothwick... warum tanzt sie? Da ist gar keine Musik.|Mothwick... pourquoi elle danse ? Il n'y a aucune musique.|"
                  "Mothwick... perché balla? Non c'è nessuna musica.|Mothwick... por que ela dança? Não há música nenhuma."),
                {"eyes": "open", **A},
                {"move": "w", "to": 1480, "speed": "run", **A},
                S("moth", "Then whatever you hear tonight... don't start dancing.|Entonces, oigas lo que oigas esta noche... no empieces a bailar.|"
                  "Dann, was du heute Nacht auch hörst... fang nicht an zu tanzen.|Alors, quoi que tu entendes ce soir... ne commence pas à danser.|"
                  "Allora, qualunque cosa senti stanotte... non iniziare a ballare.|Então, ouça o que ouvir esta noite... não comece a dançar."),
                {"sfx": "sting", **A},
                {"hide": "w", "dur": 0.4, **A},
            ],
            "tail": 0.2,
        },
        {   # 2 Strasbourg, 14 July 1518: Frau Troffea
            "bg": "village", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"w": WOMAN(1420), "hus": MAN(1250, 0),
                          "c1": {"type": "crow", "x": 1250, "y": 330, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Strasbourg sits on the River Rhine. Today it is part of France.|Estrasburgo está junto al Rin. Hoy forma parte de Francia.|"
                  "Straßburg liegt am Rhein. Heute gehört es zu Frankreich.|Strasbourg est sur le Rhin. Aujourd'hui, c'est la France.|"
                  "Strasburgo è sul Reno. Oggi fa parte della Francia.|Estrasburgo fica no rio Reno. Hoje faz parte da França."),
                {"sfx": "bell", **A},
                {"show": "w", "dur": 0.6},
                S("narr", "On the 14th of July, 1518, a woman called Frau Troffea began to dance.|El 14 de julio de 1518, una mujer llamada Frau Troffea empezó a bailar.|"
                  "Am 14. Juli 1518 begann eine Frau namens Frau Troffea zu tanzen.|Le 14 juillet 1518, une femme nommée Frau Troffea se mit à danser.|"
                  "Il 14 luglio 1518, una donna chiamata Frau Troffea iniziò a ballare.|Em 14 de julho de 1518, uma mulher chamada Frau Troffea começou a dançar.", **A),
                *JIG("w", 1300, 1460),
                {"show": "hus", "dur": 0.4},
                {"sfx": "whoosh", **A},
                S("narr", "Her husband begged her to stop. She danced until the sky went black.|Su marido le rogó que parara. Bailó hasta que el cielo se oscureció.|"
                  "Ihr Mann flehte sie an aufzuhören. Sie tanzte, bis der Himmel schwarz war.|Son mari la supplia d'arrêter. Elle dansa jusqu'à la nuit noire.|"
                  "Il marito la pregò di smettere. Ballò finché il cielo divenne nero.|O marido implorou que parasse. Ela dançou até o céu escurecer.", **A),
                {"move": "w", "to": 1550, "speed": "run", **A},
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                {"flash": True, "dur": 1.2},
                S("narr", "The next morning, she got up on swollen feet... and danced again.|A la mañana siguiente, se levantó con los pies hinchados... y volvió a bailar.|"
                  "Am nächsten Morgen stand sie auf geschwollenen Füßen auf... und tanzte weiter.|Le lendemain, elle se leva sur ses pieds enflés... et dansa encore.|"
                  "Il mattino dopo si alzò sui piedi gonfi... e ballò ancora.|Na manhã seguinte, levantou-se com os pés inchados... e dançou de novo.", **A),
                *JIG("w", 1380, 1500),
                {"act": "odo", "do": "shake"},
                S("odo", "For how long? Someone must have stopped her!|¿Cuánto tiempo? ¡Alguien tuvo que pararla!|"
                  "Wie lange? Irgendwer muss sie doch aufgehalten haben!|Pendant combien de temps ? Quelqu'un a dû l'arrêter !|"
                  "Per quanto? Qualcuno l'avrà fermata!|Por quanto tempo? Alguém deve tê-la parado!"),
                {"hide": "hus", "dur": 0.5, **A},
                S("moth", "Nobody could. The records say she danced for nearly a week.|Nadie pudo. Los registros dicen que bailó casi una semana.|"
                  "Niemand konnte es. Laut den Berichten tanzte sie fast eine Woche.|Personne n'a pu. Les récits disent qu'elle dansa près d'une semaine.|"
                  "Nessuno ci riuscì. I documenti dicono che ballò quasi una settimana.|Ninguém conseguiu. Os registros dizem que ela dançou quase uma semana."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 3 it spreads: the watchers join in
            "bg": "village", "seed": 8, "music": "heartbeat", "wind": True, "eyes": 2, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"w": WOMAN(1500), "m1": MAN(1200, 0), "m2": MAN(1330, 1)},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", **A},
                S("narr", "Crowds came to watch: porters, beggars, pilgrims, priests and nuns.|Llegaron multitudes a mirar: porteadores, mendigos, peregrinos, curas y monjas.|"
                  "Menschen kamen, um zuzusehen: Träger, Bettler, Pilger, Priester und Nonnen.|La foule vint regarder : porteurs, mendiants, pèlerins, prêtres et nonnes.|"
                  "Arrivò la folla a guardare: facchini, mendicanti, pellegrini, preti e suore.|Multidões vieram olhar: carregadores, mendigos, peregrinos, padres e freiras.", **A),
                {"show": "m1", "dur": 0.4},
                {"show": "m2", "dur": 0.4, **A},
                {"show": "w", "dur": 0.4, **A},
                {"flash": True, "dur": 1.2},
                S("narr", "Then some of the watchers began to dance too.|Entonces algunos de los que miraban empezaron a bailar también.|"
                  "Dann begannen einige der Zuschauer ebenfalls zu tanzen.|Puis certains spectateurs se mirent à danser eux aussi.|"
                  "Poi alcuni di quelli che guardavano iniziarono a ballare anche loro.|Então alguns dos que assistiam começaram a dançar também.", **A),
                {"move": "m1", "to": 1100, "speed": "run", **A},
                {"move": "m2", "to": 1420, "speed": "run", **A},
                {"sfx": "whisper", **A},
                {"move": "m1", "to": 1240, "speed": "run"},
                {"move": "m2", "to": 1300, "speed": "run", **A},
                S("narr", "Within days, more than thirty people were dancing in the streets.|En pocos días, más de treinta personas bailaban en las calles.|"
                  "Nach wenigen Tagen tanzten über dreißig Menschen in den Gassen.|En quelques jours, plus de trente personnes dansaient dans les rues.|"
                  "In pochi giorni, più di trenta persone ballavano per le strade.|Em poucos dias, mais de trinta pessoas dançavam nas ruas.", **A),
                {"shake": 0.6, "power": 12, **A},
                {"eyes": "open"},
                S("narr", "By August, chroniclers counted between fifty and four hundred dancers.|En agosto, los cronistas contaron entre cincuenta y cuatrocientos.|"
                  "Im August zählten Chronisten zwischen fünfzig und vierhundert Tänzer.|En août, les chroniqueurs comptaient de cinquante à quatre cents danseurs.|"
                  "Ad agosto, i cronisti contavano tra cinquanta e quattrocento ballerini.|Em agosto, cronistas contavam entre cinquenta e quatrocentos dançarinos.", **A),
                {"sfx": "step", **A},
                *JIG("w", 1380, 1560),
                {"act": "odo", "do": "jump"},
                S("odo", "Four hundred? Day and night? Why didn't anyone stop it?|¿Cuatrocientos? ¿Día y noche? ¿Por qué nadie lo detuvo?|"
                  "Vierhundert? Tag und Nacht? Warum hat das keiner beendet?|Quatre cents ? Jour et nuit ? Pourquoi personne n'a arrêté ça ?|"
                  "Quattrocento? Giorno e notte? Perché nessuno l'ha fermato?|Quatrocentos? Dia e noite? Por que ninguém parou isso?"),
                {"eyes": "close"},
                S("moth", "They tried. And what they tried made it so much worse.|Lo intentaron. Y lo que intentaron lo empeoró mucho.|"
                  "Sie versuchten es. Und das machte alles noch viel schlimmer.|Ils ont essayé. Et ce qu'ils ont fait a tout aggravé.|"
                  "Ci provarono. E ciò che fecero peggiorò tutto.|Eles tentaram. E o que tentaram piorou tudo."),
                {"sfx": "sting", **A},
                {"hide": "m1", "dur": 0.3, **A},
                {"hide": "m2", "dur": 0.3, **A},
                {"hide": "w", "dur": 0.3, **A},
            ],
            "tail": 0.3,
        },
        {   # 4 the cure that backfired: guild halls, stages, paid musicians
            "bg": "village", "seed": 4, "music": "lullaby", "wind": True, "eyes": 0, "ambient": 0.44,
            "lights": [{"kind": "fire", "x": 1300, "y": 900, "r": 600}],
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"m1": MAN(1200, 1), "w": WOMAN(1350), "m2": MAN(1520, 0)},
            "beats": [
                S("narr", "The city's doctors said it was hot blood. And the cure? More dancing.|Los médicos dijeron que era sangre caliente. ¿La cura? Más baile.|"
                  "Die Ärzte sagten, es sei überhitztes Blut. Die Heilung? Noch mehr Tanz.|Les médecins parlèrent de sang trop chaud. Le remède ? Encore danser.|"
                  "I medici dissero che era sangue surriscaldato. La cura? Ballare ancora.|Os médicos disseram que era sangue quente. A cura? Mais dança."),
                {"sfx": "bell", **A},
                {"light": "flare"},
                {"show": "m1", "dur": 0.3, **A},
                {"show": "w", "dur": 0.3, **A},
                {"show": "m2", "dur": 0.3, **A},
                S("narr", "The council turned guild halls into dance floors.|El consejo convirtió los salones de los gremios en pistas de baile.|"
                  "Der Rat machte aus Zunfthäusern Tanzböden.|Le conseil transforma les maisons des corporations en salles de danse.|"
                  "Il consiglio trasformò le sale delle corporazioni in sale da ballo.|O conselho transformou os salões das guildas em pistas de dança.", **A),
                {"move": "m1", "to": 1100, "speed": "run", **A},
                {"move": "m2", "to": 1600, "speed": "run", **A},
                {"flash": True, "dur": 1.0},
                S("narr", "Stages went up in the horse market and the grain market.|Montaron tarimas en el mercado de caballos y en el de grano.|"
                  "Bühnen entstanden auf dem Pferdemarkt und dem Kornmarkt.|Des estrades furent dressées au marché aux chevaux et au marché aux grains.|"
                  "Furono montati palchi nel mercato dei cavalli e in quello del grano.|Ergueram palcos no mercado de cavalos e no de grãos.", **A),
                *JIG("w", 1250, 1420),
                {"sfx": "snap", **A},
                S("narr", "Musicians were paid to play drums, fiddles, pipes and horns.|Pagaron a músicos para tocar tambores, violines, flautas y cuernos.|"
                  "Musiker wurden bezahlt für Trommeln, Fiedeln, Pfeifen und Hörner.|On paya des musiciens : tambours, violes, flûtes et cors.|"
                  "Pagarono musicisti per suonare tamburi, violini, flauti e corni.|Pagaram músicos para tocar tambores, rabecas, flautas e trompas."),
                {"shake": 0.5, "power": 10, **A},
                {"move": "m1", "to": 1240, "speed": "run", **A},
                {"move": "m2", "to": 1480, "speed": "run", **A},
                S("narr", "But the more the music played, the more people joined the dance.|Pero cuanto más sonaba la música, más gente se unía al baile.|"
                  "Doch je mehr Musik spielte, desto mehr Menschen tanzten mit.|Mais plus la musique jouait, plus les gens rejoignaient la danse.|"
                  "Ma più la musica suonava, più gente si univa al ballo.|Mas quanto mais a música tocava, mais gente entrava na dança."),
                {"sfx": "whisper", **A},
                {"act": "odo", "do": "scared"},
                S("odo", "They made it louder?! That's like feeding a fire!|¿¡Lo hicieron más fuerte!? ¡Es como alimentar un fuego!|"
                  "Sie machten es lauter?! Das ist, als würde man ein Feuer füttern!|Ils ont mis plus fort ?! C'est comme nourrir un feu !|"
                  "L'hanno reso più forte?! È come alimentare un fuoco!|Deixaram mais alto?! É como alimentar um fogo!"),
                {"light": "dim"},
                {"hide": "m1", "dur": 0.3, **A},
                {"hide": "m2", "dur": 0.3, **A},
                {"hide": "w", "dur": 0.3, **A},
                S("moth", "So in the end, they did the opposite. They banned the music.|Así que al final hicieron lo contrario. Prohibieron la música.|"
                  "Am Ende taten sie das Gegenteil. Sie verboten die Musik.|Alors, à la fin, ils firent l'inverse. Ils interdirent la musique.|"
                  "Alla fine fecero il contrario. Vietarono la musica.|Então, no fim, fizeram o contrário. Proibiram a música."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 5 the ban + Saint Vitus, red shoes at Saverne
            "bg": "chapel", "seed": 5, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "window", "x": 1200, "y": 560, "r": 600}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"pr": MAN(1450, 2, 1.0), "w": WOMAN(1250, 0.95), "g1": GHOST(1350)},
            "beats": [
                S("narr", "The stages came down. Drums and public dancing were banned.|Desmontaron las tarimas. Prohibieron los tambores y el baile público.|"
                  "Die Bühnen wurden abgerissen. Trommeln und Tanz wurden verboten.|Les estrades furent démontées. Tambours et danse furent interdits.|"
                  "I palchi furono smontati. Tamburi e balli pubblici vietati.|Os palcos foram desmontados. Tambores e dança pública, proibidos."),
                {"sfx": "thump", **A},
                {"flash": True, "dur": 1.0},
                S("narr", "Many believed Saint Vitus himself had cursed them to dance.|Muchos creían que el mismo San Vito los había maldecido a bailar.|"
                  "Viele glaubten, der heilige Veit selbst habe sie zum Tanzen verflucht.|Beaucoup croyaient que saint Guy lui-même les avait maudits.|"
                  "Molti credevano che San Vito in persona li avesse maledetti.|Muitos acreditavam que o próprio São Vito os amaldiçoara a dançar.", **A),
                {"show": "pr", "dur": 0.6, **A},
                {"sfx": "bell", "wait": 0.3},
                S("narr", "So the dancers were taken by wagon to his shrine at Saverne.|Así que llevaron a los bailarines en carretas a su santuario de Saverne.|"
                  "Also brachte man die Tänzer mit Wagen zu seinem Heiligtum in Zabern.|On emmena donc les danseurs en charrette à son sanctuaire de Saverne.|"
                  "Così i ballerini furono portati su carri al suo santuario di Saverne.|Então levaram os dançarinos de carroça ao santuário dele em Saverne."),
                {"show": "w", "dur": 0.4, **A},
                *JIG("w", 1150, 1280),
                {"light": "flare"},
                S("narr", "There, priests put small crosses in their hands, and red shoes on their feet.|Allí, los curas les dieron crucecitas y les pusieron zapatos rojos.|"
                  "Dort gaben Priester ihnen kleine Kreuze und rote Schuhe.|Là, des prêtres leur mirent de petites croix en main et des souliers rouges.|"
                  "Lì i preti diedero loro piccole croci e scarpe rosse.|Lá, padres puseram pequenas cruzes nas mãos deles e sapatos vermelhos nos pés.", **A),
                {"sfx": "whisper", **A},
                S("narr", "The shoes were marked with crosses of holy oil.|Los zapatos llevaban cruces pintadas con óleo santo.|"
                  "Die Schuhe wurden mit Kreuzen aus heiligem Öl bemalt.|Les souliers étaient marqués de croix d'huile sainte.|"
                  "Le scarpe erano segnate con croci d'olio santo.|Os sapatos eram marcados com cruzes de óleo santo."),
                {"shake": 0.4, "power": 8, **A},
                S("narr", "By early September, the dancing faded away.|A principios de septiembre, el baile se apagó.|"
                  "Anfang September ebbte das Tanzen ab.|Début septembre, la danse s'éteignit.|"
                  "A inizio settembre, il ballo svanì.|No começo de setembro, a dança foi sumindo."),
                {"hide": "w", "dur": 0.6, **A},
                {"hide": "pr", "dur": 0.6, **A},
                {"light": "dim"},
                {"show": "g1", "dur": 0.4},
                {"act": "odo", "do": "hide"},
                S("odo", "So the red shoes worked? Then who is still dancing by the altar?|¿Funcionaron los zapatos rojos? ¿Y quién sigue bailando junto al altar?|"
                  "Die roten Schuhe halfen also? Wer tanzt dann noch am Altar?|Les souliers rouges ont marché ? Alors qui danse encore près de l'autel ?|"
                  "Le scarpe rosse funzionarono? Allora chi balla ancora vicino all'altare?|Os sapatos vermelhos funcionaram? Então quem ainda dança perto do altar?"),
                {"growl": "g1", **A},
                {"hide": "g1", "dur": 0.2},
                {"light": "on", **A},
                {"act": "odo", "do": "unhide"},
                S("moth", "No one knows what ended it, Odo. Or what started it.|Nadie sabe qué lo terminó, Odo. Ni qué lo empezó.|"
                  "Niemand weiß, was es beendet hat, Odo. Oder was es begann.|Personne ne sait ce qui l'a arrêté, Odo. Ni ce qui l'a commencé.|"
                  "Nessuno sa cosa lo fermò, Odo. O cosa lo iniziò.|Ninguém sabe o que acabou com isso, Odo. Nem o que começou."),
            ],
            "tail": 0.3,
        },
        {   # 6 what caused it? the theories
            "bg": "forest", "seed": 3, "music": "drone", "wind": True, "eyes": 2, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": GHOST(1450), "c1": {"type": "crow", "x": 1250, "y": 320, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Some blame ergot, a mould on rye bread that can cause twitching.|Algunos culpan al cornezuelo, un moho del pan de centeno que causa espasmos.|"
                  "Manche geben dem Mutterkorn die Schuld, einem Pilz im Roggenbrot.|Certains accusent l'ergot, une moisissure du seigle qui fait trembler.|"
                  "Alcuni incolpano la segale cornuta, una muffa del pane di segale.|Alguns culpam o esporão, um mofo do pão de centeio que causa espasmos."),
                {"flash": True, "dur": 1.2, **A},
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "But historian John Waller says ergot victims could never dance for days.|Pero el historiador John Waller dice que con cornezuelo nadie bailaría días.|"
                  "Doch der Historiker John Waller sagt: Damit könnte niemand tagelang tanzen.|Mais l'historien John Waller dit qu'avec l'ergot, on ne danse pas des jours.|"
                  "Ma lo storico John Waller dice che così nessuno ballerebbe per giorni.|Mas o historiador John Waller diz que assim ninguém dançaria por dias."),
                {"sfx": "snap", **A},
                S("narr", "He thinks fear did it: hunger, sickness, and belief in the curse.|Él cree que fue el miedo: hambre, enfermedad y la fe en la maldición.|"
                  "Er glaubt, es war Angst: Hunger, Krankheit und der Glaube an den Fluch.|Il pense que c'était la peur : faim, maladie et foi en la malédiction.|"
                  "Lui pensa che fu la paura: fame, malattia e fede nella maledizione.|Ele acha que foi o medo: fome, doença e a crença na maldição."),
                {"shake": 0.5, "power": 10, **A},
                {"act": "odo", "do": "calm"},
                S("narr", "Strasbourg's own records agree that people danced. None of them say why.|Los registros de Estrasburgo coinciden en que bailaron. Ninguno dice por qué.|"
                  "Straßburgs Akten bestätigen das Tanzen. Keine sagt, warum.|Les archives de Strasbourg confirment la danse. Aucune ne dit pourquoi.|"
                  "I documenti di Strasburgo confermano il ballo. Nessuno dice perché.|Os registros de Estrasburgo confirmam a dança. Nenhum diz por quê."),
                {"light": "out"},
                {"show": "g1", "dur": 0.3, **A},
                {"sfx": "whisper", **A},
                {"act": "odo", "do": "shake"},
                S("odo", "Mothwick... my feet. They're tapping all on their own.|Mothwick... mis pies. Se mueven solos.|"
                  "Mothwick... meine Füße. Sie tippen ganz von allein.|Mothwick... mes pieds. Ils tapent tout seuls.|"
                  "Mothwick... i miei piedi. Battono da soli.|Mothwick... meus pés. Estão batendo sozinhos."),
                {"flash": True, "dur": 1.2},
                {"hide": "g1", "dur": 0.2, **A},
                {"light": "flare"},
                S("moth", "Hold still, Odo. Whatever you hear... don't start dancing.|Quieto, Odo. Oigas lo que oigas... no empieces a bailar.|"
                  "Halt still, Odo. Was du auch hörst... fang nicht an zu tanzen.|Reste immobile, Odo. Quoi que tu entendes... ne danse pas.|"
                  "Stai fermo, Odo. Qualunque cosa senti... non iniziare a ballare.|Fique parado, Odo. Ouça o que ouvir... não comece a dançar."),
                {"eyes": "close"},
            ],
            "tail": 0.3,
        },
        {   # 7 the square: cliffhanger
            "bg": "village", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"w": WOMAN(1520, 1.05), "c1": {"type": "crow", "x": 1300, "y": 320, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Before 1518, more than ten dancing plagues broke out along the Rhine.|Antes de 1518, hubo más de diez plagas de baile junto al Rin.|"
                  "Vor 1518 brachen am Rhein mehr als zehn Tanzwut-Seuchen aus.|Avant 1518, plus de dix épidémies de danse éclatèrent le long du Rhin.|"
                  "Prima del 1518, oltre dieci epidemie di ballo scoppiarono lungo il Reno.|Antes de 1518, mais de dez pragas de dança surgiram ao longo do Reno."),
                {"sfx": "whoosh", **A},
                S("narr", "And no one has ever fully explained a single one of them.|Y nadie ha explicado nunca del todo ni una sola.|"
                  "Und keine einzige wurde je ganz erklärt.|Et personne n'en a jamais vraiment expliqué une seule.|"
                  "E nessuno ne ha mai spiegata davvero una sola.|E ninguém jamais explicou de verdade nenhuma delas."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", **A},
                {"hide": "c1", "dur": 0.4},
                S("odo", "Mothwick... do you hear drums? Coming from the square...|Mothwick... ¿oyes tambores? Vienen de la plaza...|"
                  "Mothwick... hörst du Trommeln? Vom Marktplatz her...|Mothwick... tu entends des tambours ? Ça vient de la place...|"
                  "Mothwick... senti i tamburi? Vengono dalla piazza...|Mothwick... está ouvindo tambores? Vêm da praça..."),
                {"eyes": "open", **A},
                {"sfx": "thump", "wait": 0.3},
                {"sfx": "thump", "wait": 0.3},
                {"flash": True, "dur": 1.0},
                {"eyes": "close"},
                {"act": "odo", "do": "turn"},
                S("moth", "The square is empty, Odo... but something out there is dancing.|La plaza está vacía, Odo... pero algo ahí fuera está bailando.|"
                  "Der Platz ist leer, Odo... aber da draußen tanzt etwas.|La place est vide, Odo... mais quelque chose danse là-bas.|"
                  "La piazza è vuota, Odo... ma qualcosa là fuori sta ballando.|A praça está vazia, Odo... mas algo lá fora está dançando."),
                {"sfx": "step", "wait": 0.4},
                {"show": "w", "dur": 0.3},
                *JIG("w", 1380, 1500),
                {"growl": "w", **A},
                {"lunge": "w", "to": 1150},
                {"light": "out", **A},
                {"card": "WHO STARTS THE DANCE?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}


def L(*parts):
    return "|".join(parts)


def SHOT(bg, seed, beats, odo=700, amb=0.48, eyes=0, lights=None, creatures=None, tail=0.05, music="heartbeat"):
    sh = {"bg": bg, "seed": seed, "music": music, "wind": True, "eyes": eyes, "ambient": amb, "focus": "odo", "fade": False,
          "chars": {"odo": {"x": odo}}, "creatures": creatures or {}, "beats": beats, "tail": tail}
    if lights:
        sh["lights"] = lights
    return sh


WIN = [{"kind": "window", "x": 900, "y": 640, "r": 520}]
FIRE = [{"kind": "fire", "x": 900, "y": 900, "r": 600}]

# Short: hard cuts + flashes -> something new every 2-4 s; one scare (the dancer's lunge);
# the last shot repeats shot 1's set-up so the final frame loops back to frame 1.
short1 = {   # the rule / scariest true detail
    "id": "ep010_short1", "format": "short",
    "title": "Why Couldn't Strasbourg Stop Dancing? #shorts",
    "hook": "DON'T START DANCING",
    "description": "Strasbourg, July 1518: one woman began to dance in the street — with no music — and could not stop. Within weeks, chroniclers counted 50 to 400 dancers. The city's cure? Hire musicians. Full true story on the channel. #shorts #dancingplague #strasbourg #1518 #truestory #hollowmere",
    "tags": ["shorts"] + TAGS[:11],
    "thumbnail": {"bg": "village", "seed": 6, "creature": "figure", "text": "DON'T DANCE"},
    "shots": [
        SHOT("village", 6, [
            {"show": "w", "dur": 0.05}, {"flash": True, **A}, {"shake": 0.4, "power": 14, "and": True},
            {"move": "w", "to": 820, "speed": "run", **A},
            S("narr", L("1518. One woman starts dancing. No music.", "1518. Una mujer empieza a bailar. Sin música.",
                        "1518. Eine Frau beginnt zu tanzen. Ohne Musik.", "1518. Une femme se met à danser. Sans musique.",
                        "1518. Una donna inizia a ballare. Senza musica.", "1518. Uma mulher começa a dançar. Sem música."), **A),
            {"move": "w", "to": 960, "speed": "run"},
        ], odo=560, amb=0.55, lights=WIN, creatures={"w": WOMAN(960, 0.9)}),
        SHOT("village", 8, [
            {"show": "m1", "dur": 0.2}, {"show": "m2", "dur": 0.2, **A},
            S("narr", L("She can't stop. Then the watchers join in. Hundreds.", "No puede parar. Luego se unen los mirones. Cientos.",
                        "Sie kann nicht aufhören. Dann tanzen die Zuschauer mit. Hunderte.", "Elle ne peut s'arrêter. Puis les badauds suivent. Des centaines.",
                        "Non riesce a fermarsi. Poi si uniscono gli altri. Centinaia.", "Ela não consegue parar. Depois os curiosos entram. Centenas."), **A),
            {"move": "m1", "to": 640, "speed": "run", **A},
            {"move": "m2", "to": 900, "speed": "run", **A},
            {"flash": True},
        ], odo=420, eyes=2, lights=WIN, creatures={"m1": MAN(760, 0, 0.85), "m2": MAN(1000, 1, 0.85)}),
        SHOT("village", 4, [
            {"act": "odo", "do": "scared"},
            S("narr", L("The city's cure? Hire musicians. It only spread.", "¿La cura de la ciudad? Contratar músicos. Solo empeoró.",
                        "Die Heilung der Stadt? Musiker anheuern. Es breitete sich aus.", "Le remède de la ville ? Des musiciens. Ça s'est propagé.",
                        "La cura? Assumere musicisti. Si diffuse ancora.", "A cura da cidade? Contratar músicos. Só piorou."), **A),
            {"sfx": "thump", **A},
            {"light": "out"},
            {"show": "w", "dur": 0.1, **A},
            {"lunge": "w", "to": 820, **A},
            {"flash": True, "and": True},
        ], odo=560, lights=FIRE, creatures={"w": WOMAN(950, 1.0)}),
        SHOT("village", 6, [
            {"move": "odo", "to": 560, "speed": "walk"},
            S("narr", L("So if your feet start tapping tonight...", "Así que si tus pies empiezan a moverse esta noche...",
                        "Wenn deine Füße heute Nacht zu tippen beginnen...", "Alors si tes pieds se mettent à taper ce soir...",
                        "Quindi se stanotte i tuoi piedi iniziano a battere...", "Então, se seus pés começarem a bater esta noite..."), **A),
            {"show": "w", "dur": 0.05}, {"flash": True, **A},
        ], odo=640, amb=0.55, lights=WIN, tail=0.0, creatures={"w": WOMAN(820, 0.9)}),
    ],
}

short1["shots"][0]["focus"] = ["odo", "w"]
short1["shots"][1]["focus"] = ["odo", "m1"]
short1["shots"][2]["cam"] = {"x": 740}

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

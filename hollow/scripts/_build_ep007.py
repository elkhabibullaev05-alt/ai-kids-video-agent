"""Builds Hollowmere EP7 (recorded legend: the Jersey Devil, Pine Barrens legend from 1735; the sightings week of 16-23 January 1909).
Run: python3 scripts/_build_ep007.py
Retention rules (2026-10-16): frame 1 = motion + big text hook (no fade, no title card), narration from 0 s mid-tension,
something new every 4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to its first frame."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Jersey Devil", "Leeds Devil", "Pine Barrens",
        "New Jersey", "1909", "American legend", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Jersey_Devil",
           "https://www.nj.gov/nj/about/famous/nj_devil.shtml",
           "https://www.inquirer.com/news/new-jersey/jersey-devil-history-fake-news-norman-jeffries-20190123.html",
           "https://weirdnj.com/stories/jersey-devil"]

long_ = {
    "id": "ep007_long", "format": "long",
    "title": "What Was Screaming in the Pine Barrens?",
    "hook": "DON'T LOOK UP", "hook_dur": 4.5,
    "description": ("Based on real newspaper reports and a famous American legend. The story says that in 1735, at Leeds Point "
                    "in the New Jersey Pine Barrens, Mother Leeds' thirteenth child turned into a winged creature and flew up the chimney. "
                    "Then, in the week of 16 to 23 January 1909, newspapers across South Jersey and Philadelphia printed hundreds of reports: "
                    "strange tracks in the snow that crossed fences and rooftops, a winged thing with a horse-like head, police firing at shadows. "
                    "Schools closed, people stayed home, hunters searched the pines. Historians call it a famous case of mass panic, and some "
                    "tracks were hoaxes. No creature was ever caught.\n\n"
                    "Sources:\n" + "\n".join(SOURCES[:3]) + "\n\n#truestory #jerseydevil #pinebarrens #legend #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 7", "1909 sightings", "cryptid", "Leeds Point"],
    "thumbnail": {"bg": "swamp", "seed": 4, "creature": "gloamhound", "text": "DON'T LOOK UP"},
    "shots": [
        {   # 1 cold open: motion + hook text from frame 1, narration from 0 s mid-tension
            "bg": "swamp", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 5, "lantern": 1.0, "ambient": 0.38, "fade": False,
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"c1": {"type": "crow", "x": 1300, "y": 360, "state": "hidden", "fly": 1}},
            "beats": [
                {"move": "odo", "to": 640, "speed": "creep"},
                {"move": "moth", "to": 780, "speed": "creep", "and": True},
                S("narr", "Something screamed over the pine trees... and then the whole state was afraid.|Algo gritó sobre los pinos... y todo el estado tuvo miedo.|"
                  "Etwas schrie über den Kiefern... und dann hatte der ganze Staat Angst.|Quelque chose hurla au-dessus des pins... et tout l'État eut peur.|"
                  "Qualcosa urlò sopra i pini... e tutto lo stato ebbe paura.|Algo gritou sobre os pinheiros... e o estado inteiro teve medo.", **{"and": True}),
                {"sfx": "flutter", "wait": 0.2},
                {"show": "c1", "dur": 0.3, "and": True},
                {"act": "odo", "do": "scared"},
                S("narr", "This is a real American legend. New Jersey. The Pine Barrens.|Esta es una leyenda real de América. Nueva Jersey. Los Pine Barrens.|"
                  "Dies ist eine echte amerikanische Legende. New Jersey. Die Pine Barrens.|Ceci est une vraie légende américaine. New Jersey. Les Pine Barrens.|"
                  "Questa è una vera leggenda americana. New Jersey. I Pine Barrens.|Esta é uma lenda americana real. Nova Jersey. Os Pine Barrens."),
                {"hide": "c1", "dur": 0.5, "and": True},
                S("odo", "Mothwick... something big just flew over us.|Mothwick... algo grande acaba de volar sobre nosotros.|"
                  "Mothwick... gerade ist etwas Großes über uns geflogen.|Mothwick... quelque chose de grand vient de passer au-dessus de nous.|"
                  "Mothwick... qualcosa di grande ci è appena volato sopra.|Mothwick... algo grande acabou de voar sobre nós."),
                {"eyes": "open", "and": True},
                S("moth", "Then whatever you do... don't look up.|Entonces, hagas lo que hagas... no mires arriba.|Dann, was du auch tust... schau nicht nach oben.|"
                  "Alors, quoi que tu fasses... ne lève pas les yeux.|Allora, qualunque cosa accada... non guardare in alto.|Então, aconteça o que acontecer... não olhe para cima."),
                {"sfx": "sting", "and": True},
            ],
            "tail": 0.2,
        },
        {   # 2 the 1735 legend at Leeds Point
            "bg": "manor", "seed": 3, "music": "lullaby", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1250, "y": 640, "r": 520}],
            "cam": {"from": [880, 600, 1.12], "to": [1020, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"mother": {"type": "figure", "x": 1420, "seed": 2, "face": -1, "state": "hidden"},
                          "c1": {"type": "crow", "x": 1250, "y": 330, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "The legend begins in 1735, on a stormy night at Leeds Point.|La leyenda empieza en 1735, en una noche de tormenta en Leeds Point.|"
                  "Die Legende beginnt 1735, in einer Sturmnacht in Leeds Point.|La légende commence en 1735, une nuit d'orage à Leeds Point.|"
                  "La leggenda inizia nel 1735, in una notte di tempesta a Leeds Point.|A lenda começa em 1735, numa noite de tempestade em Leeds Point."),
                {"sfx": "thump", "and": True},
                {"show": "mother", "dur": 1.0},
                S("narr", "A woman called Mother Leeds was having her thirteenth child.|Una mujer llamada Madre Leeds iba a tener su hijo número trece.|"
                  "Eine Frau namens Mutter Leeds bekam ihr dreizehntes Kind.|Une femme, la Mère Leeds, attendait son treizième enfant.|"
                  "Una donna chiamata Madre Leeds aspettava il suo tredicesimo figlio.|Uma mulher chamada Mãe Leeds esperava o seu décimo terceiro filho."),
                S("narr", "Tired and angry, the story says, she cried: let this one be a devil!|Cansada y furiosa, dice la historia, gritó: ¡que este sea un diablo!|"
                  "Müde und wütend, so heißt es, rief sie: Soll dieses doch ein Teufel sein!|Épuisée, raconte-t-on, elle cria : que celui-ci soit un diable !|"
                  "Stanca e arrabbiata, si dice, gridò: che questo sia un diavolo!|Cansada e furiosa, diz a história, gritou: que este seja um diabo!"),
                {"sfx": "sting", "and": True},
                {"act": "odo", "do": "jump"},
                S("narr", "The baby looked normal. Then it grew wings, hooves and a tail...|El bebé parecía normal. Luego le salieron alas, pezuñas y cola...|"
                  "Das Baby sah normal aus. Dann wuchsen ihm Flügel, Hufe und ein Schwanz...|Le bébé semblait normal. Puis lui poussèrent des ailes, des sabots, une queue...|"
                  "Il bambino sembrava normale. Poi gli crebbero ali, zoccoli e una coda...|O bebê parecia normal. Depois cresceram asas, cascos e um rabo..."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", "and": True},
                S("narr", "...and with a shriek, it flew up the chimney into the pines.|...y con un chillido, voló por la chimenea hacia los pinos.|"
                  "...und mit einem Schrei flog es durch den Kamin in die Kiefern.|...et dans un cri, il s'envola par la cheminée vers les pins.|"
                  "...e con uno strillo volò su per il camino, tra i pini.|...e com um grito voou pela chaminé para os pinheiros."),
                {"hide": "c1", "dur": 0.4},
                {"hide": "mother", "dur": 0.8, "and": True},
                S("moth", "That part is only a legend. What came next was in the newspapers.|Eso es solo leyenda. Lo que vino después salió en los periódicos.|"
                  "Das ist nur Legende. Was danach kam, stand in den Zeitungen.|Ça, c'est la légende. La suite était dans les journaux.|"
                  "Questa è solo leggenda. Quello che venne dopo finì sui giornali.|Isso é só lenda. O que veio depois saiu nos jornais."),
            ],
            "tail": 0.3,
        },
        {   # 3 January 1909: tracks in the snow
            "bg": "village", "seed": 5, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "creatures": {"man": {"type": "figure", "x": 1400, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "January 1909. One week of snow and fear across South Jersey.|Enero de 1909. Una semana de nieve y miedo en el sur de Nueva Jersey.|"
                  "Januar 1909. Eine Woche voller Schnee und Angst in South Jersey.|Janvier 1909. Une semaine de neige et de peur dans le sud du New Jersey.|"
                  "Gennaio 1909. Una settimana di neve e paura nel sud del New Jersey.|Janeiro de 1909. Uma semana de neve e medo no sul de Nova Jersey."),
                {"sfx": "bell", "and": True},
                {"show": "man", "dur": 1.0},
                S("narr", "People woke up and found strange hoof prints in the snow.|La gente despertó y encontró extrañas huellas de pezuña en la nieve.|"
                  "Die Leute wachten auf und fanden seltsame Hufspuren im Schnee.|Les gens trouvèrent au réveil d'étranges traces de sabots dans la neige.|"
                  "La gente si svegliò e trovò strane impronte di zoccoli nella neve.|As pessoas acordaram e acharam estranhas pegadas de casco na neve."),
                S("narr", "The tracks went over fences, through backyards... and across rooftops.|Las huellas pasaban vallas, patios... y cruzaban los tejados.|"
                  "Die Spuren gingen über Zäune, durch Gärten... und über die Dächer.|Les traces franchissaient les clôtures, les jardins... et les toits.|"
                  "Le tracce scavalcavano recinti, cortili... e attraversavano i tetti.|As pegadas passavam cercas, quintais... e cruzavam os telhados."),
                {"sfx": "step", "and": True},
                {"act": "odo", "do": "shake"},
                S("narr", "In Hammonton, it was said, the bloodhounds refused to follow the trail.|En Hammonton, se decía, los sabuesos se negaron a seguir el rastro.|"
                  "In Hammonton, hieß es, wollten die Spürhunde der Spur nicht folgen.|À Hammonton, disait-on, les chiens refusèrent de suivre la piste.|"
                  "A Hammonton, si diceva, i segugi si rifiutarono di seguire la pista.|Em Hammonton, diziam, os cães farejadores se recusaram a seguir o rastro."),
                {"sfx": "howl", "and": True},
                S("odo", "Dogs that won't follow a trail? What were they smelling?|¿Perros que no siguen un rastro? ¿Qué olían?|"
                  "Hunde, die keiner Spur folgen? Was haben sie gerochen?|Des chiens qui refusent une piste ? Qu'ont-ils senti ?|"
                  "Cani che non seguono una pista? Cosa sentivano?|Cães que não seguem um rastro? O que eles farejaram?"),
                {"hide": "man", "dur": 0.8},
            ],
            "tail": 0.3,
        },
        {   # 4 the sightings
            "bg": "forest", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 6, "ambient": 0.34,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 0.9},
                          "c1": {"type": "crow", "x": 1200, "y": 300, "state": "hidden", "fly": 1}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", "and": True},
                S("narr", "Then the newspapers printed hundreds of sightings.|Entonces los periódicos publicaron cientos de avistamientos.|"
                  "Dann druckten die Zeitungen Hunderte von Sichtungen.|Puis les journaux publièrent des centaines de témoignages.|"
                  "Poi i giornali pubblicarono centinaia di avvistamenti.|Então os jornais publicaram centenas de avistamentos.", **{"and": True}),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", "and": True},
                S("narr", "Witnesses described wings... a head like a horse... glowing eyes.|Los testigos hablaban de alas... cabeza de caballo... ojos brillantes.|"
                  "Zeugen sprachen von Flügeln... einem Kopf wie ein Pferd... glühenden Augen.|Les témoins parlaient d'ailes... d'une tête de cheval... d'yeux luisants.|"
                  "I testimoni parlavano di ali... una testa di cavallo... occhi che brillavano.|Testemunhas falavam de asas... cabeça de cavalo... olhos brilhando."),
                {"hide": "c1", "dur": 0.3},
                {"eyes": "open", "and": True},
                S("narr", "And a scream so loud it woke whole streets.|Y un grito tan fuerte que despertaba calles enteras.|"
                  "Und ein Schrei, so laut, dass ganze Straßen erwachten.|Et un cri si fort qu'il réveillait des rues entières.|"
                  "E un urlo così forte da svegliare strade intere.|E um grito tão alto que acordava ruas inteiras."),
                {"light": "dim"},
                {"show": "h1", "dur": 0.4, "and": True},
                {"growl": "h1"},
                S("narr", "Police in Camden, and in Bristol, Pennsylvania, said they fired at it.|La policía de Camden y de Bristol, Pensilvania, dijo que le disparó.|"
                  "Polizisten in Camden und in Bristol, Pennsylvania, sagten, sie hätten geschossen.|La police de Camden et de Bristol, en Pennsylvanie, dit avoir tiré.|"
                  "La polizia di Camden e di Bristol, in Pennsylvania, disse di aver sparato.|A polícia de Camden e de Bristol, Pensilvânia, disse que atirou."),
                {"flash": True},
                {"hide": "h1", "dur": 0.2, "and": True},
                S("narr", "Nothing happened. It simply flew away.|No pasó nada. Simplemente se fue volando.|Nichts geschah. Es flog einfach davon.|"
                  "Rien. La chose s'envola, tout simplement.|Niente. Volò semplicemente via.|Nada aconteceu. Simplesmente voou para longe."),
                {"light": "on"},
                {"eyes": "close", "and": True},
                {"move": "odo", "to": "off_right", "speed": "run"},
                {"move": "moth", "to": "off_right", "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 5 the panic: schools close, posses, reward
            "bg": "village", "seed": 8, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1200, "y": 600, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"hunter": {"type": "figure", "x": 1400, "seed": 1, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "The fear spread fast. Some schools closed. Workers stayed at home.|El miedo se extendió. Algunas escuelas cerraron. Obreros se quedaron en casa.|"
                  "Die Angst breitete sich aus. Schulen schlossen. Arbeiter blieben zu Hause.|La peur se répandit. Des écoles fermèrent. Des ouvriers restèrent chez eux.|"
                  "La paura si diffuse. Alcune scuole chiusero. Gli operai restarono a casa.|O medo se espalhou. Escolas fecharam. Trabalhadores ficaram em casa."),
                {"sfx": "bell", "and": True},
                {"show": "hunter", "dur": 1.0},
                S("narr", "Groups of hunters went into the pines with guns and lanterns.|Grupos de cazadores entraron en los pinares con armas y faroles.|"
                  "Jäger zogen mit Gewehren und Laternen in die Kiefernwälder.|Des groupes de chasseurs partirent dans les pins, fusils et lanternes en main.|"
                  "Gruppi di cacciatori entrarono nelle pinete con fucili e lanterne.|Grupos de caçadores entraram nos pinhais com armas e lanternas."),
                {"sfx": "step", "and": True},
                S("narr", "The Philadelphia Zoo, it was reported, offered ten thousand dollars to catch it.|El zoo de Filadelfia, se dijo, ofreció diez mil dólares por atraparlo.|"
                  "Der Zoo von Philadelphia bot angeblich zehntausend Dollar für den Fang.|Le zoo de Philadelphie aurait offert dix mille dollars pour sa capture.|"
                  "Lo zoo di Filadelfia, si disse, offrì diecimila dollari per catturarlo.|O zoológico da Filadélfia, dizia-se, ofereceu dez mil dólares pela captura."),
                S("odo", "Ten thousand dollars... and nobody caught anything?|Diez mil dólares... ¿y nadie atrapó nada?|Zehntausend Dollar... und niemand fing etwas?|"
                  "Dix mille dollars... et personne n'a rien attrapé ?|Diecimila dollari... e nessuno prese niente?|Dez mil dólares... e ninguém pegou nada?"),
                {"act": "odo", "do": "scared"},
                S("moth", "Nobody. Not then. Not ever.|Nadie. Ni entonces. Ni nunca.|Niemand. Nicht damals. Niemals.|"
                  "Personne. Ni alors. Ni jamais.|Nessuno. Né allora. Né mai.|Ninguém. Nem naquela época. Nem nunca."),
                {"sfx": "sting", "and": True},
                {"hide": "hunter", "dur": 1.0},
            ],
            "tail": 0.3,
        },
        {   # 6 the explanations: hoaxes and panic
            "bg": "chapel", "seed": 4, "music": "drone", "wind": True, "eyes": 2, "ambient": 0.38,
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "Later, some of the tracks turned out to be fakes, made as a prank.|Más tarde, algunas huellas resultaron ser falsas, hechas como broma.|"
                  "Später stellten sich manche Spuren als Fälschungen heraus, ein Streich.|Plus tard, certaines traces se révélèrent fausses, une farce.|"
                  "Più tardi, alcune tracce si rivelarono false, uno scherzo.|Depois, algumas pegadas se revelaram falsas, feitas como brincadeira."),
                {"sfx": "snap", "and": True},
                S("narr", "Historians call that week a famous case of mass panic.|Los historiadores llaman a esa semana un famoso caso de pánico colectivo.|"
                  "Historiker nennen jene Woche einen berühmten Fall von Massenpanik.|Les historiens y voient un célèbre cas de panique collective.|"
                  "Gli storici la chiamano un famoso caso di panico collettivo.|Historiadores chamam aquela semana de famoso caso de pânico coletivo."),
                {"act": "odo", "do": "calm"},
                S("narr", "But hundreds of people swore they saw or heard something.|Pero cientos de personas juraron haber visto u oído algo.|"
                  "Aber Hunderte schworen, etwas gesehen oder gehört zu haben.|Mais des centaines de gens jurèrent avoir vu ou entendu quelque chose.|"
                  "Ma centinaia di persone giurarono di aver visto o sentito qualcosa.|Mas centenas de pessoas juraram ter visto ou ouvido algo."),
                {"light": "out"},
                {"show": "g1", "dur": 0.3, "and": True},
                {"sfx": "whisper", "and": True},
                S("odo", "Mothwick... the lantern went out. Something is on the roof.|Mothwick... la linterna se apagó. Hay algo en el tejado.|"
                  "Mothwick... die Laterne ist aus. Etwas ist auf dem Dach.|Mothwick... la lanterne s'est éteinte. Il y a quelque chose sur le toit.|"
                  "Mothwick... la lanterna si è spenta. C'è qualcosa sul tetto.|Mothwick... a lanterna apagou. Tem algo no telhado."),
                {"sfx": "thump", "wait": 0.3},
                {"flash": True},
                {"hide": "g1", "dur": 0.2, "and": True},
                {"light": "flare"},
                S("moth", "Only the wind. Keep walking. And don't look up.|Solo el viento. Sigue andando. Y no mires arriba.|"
                  "Nur der Wind. Geh weiter. Und schau nicht hoch.|Juste le vent. Continue. Et ne lève pas les yeux.|"
                  "Solo il vento. Continua. E non guardare in alto.|Só o vento. Continue andando. E não olhe para cima."),
                {"eyes": "close"},
            ],
            "tail": 0.3,
        },
        {   # 7 the swamp: cliffhanger
            "bg": "swamp", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1520, "state": "hidden", "face": -1, "scale": 1.0},
                          "c1": {"type": "crow", "x": 1300, "y": 320, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "The snow melted. The newspapers moved on. But the reports never fully stopped.|La nieve se derritió. Los periódicos siguieron. Pero los relatos nunca pararon.|"
                  "Der Schnee schmolz. Die Zeitungen schrieben über anderes. Doch die Berichte hörten nie ganz auf.|La neige fondit. Les journaux passèrent à autre chose. Mais les récits ne cessèrent jamais.|"
                  "La neve si sciolse. I giornali cambiarono notizia. Ma i racconti non finirono mai.|A neve derreteu. Os jornais mudaram de assunto. Mas os relatos nunca pararam."),
                {"sfx": "whoosh", "and": True},
                S("narr", "Even today, people in the Pine Barrens say they hear a scream at night.|Aún hoy, en los Pine Barrens dicen oír un grito de noche.|"
                  "Noch heute sagen Leute in den Pine Barrens, sie hören nachts einen Schrei.|Aujourd'hui encore, dans les Pine Barrens, on dit entendre un cri la nuit.|"
                  "Ancora oggi, nei Pine Barrens, si dice di sentire un urlo di notte.|Até hoje, nos Pine Barrens, dizem ouvir um grito à noite."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", "and": True},
                {"hide": "c1", "dur": 0.4},
                {"act": "odo", "do": "turn"},
                S("odo", "Mothwick... there are hoof prints here. In the mud. Fresh ones.|Mothwick... hay huellas de pezuña aquí. En el barro. Recientes.|"
                  "Mothwick... hier sind Hufspuren. Im Schlamm. Ganz frisch.|Mothwick... il y a des traces de sabots ici. Dans la boue. Toutes fraîches.|"
                  "Mothwick... ci sono impronte di zoccoli qui. Nel fango. Fresche.|Mothwick... tem pegadas de casco aqui. Na lama. Recentes."),
                {"sfx": "step", "wait": 0.4},
                S("moth", "They don't lead away, Odo... they stop right behind us.|No se alejan, Odo... se detienen justo detrás de nosotros.|"
                  "Sie führen nicht weg, Odo... sie enden direkt hinter uns.|Elles ne partent pas, Odo... elles s'arrêtent juste derrière nous.|"
                  "Non portano via, Odo... si fermano proprio dietro di noi.|Elas não vão embora, Odo... param bem atrás de nós."),
                {"show": "h1", "dur": 0.3},
                {"growl": "h1", "and": True},
                {"lunge": "h1", "to": 1150},
                {"light": "out", "and": True},
                {"card": "WHAT LIVES IN THE PINES?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}

short1 = {   # the scariest true detail; ends on the opening frame so it loops
    "id": "ep007_short1", "format": "short",
    "title": "Would YOU walk these woods at night? 🦇 #shorts",
    "hook": "DON'T LOOK UP",
    "description": "New Jersey, January 1909: hoof prints across the rooftops, a scream over the pines, police firing at something with wings. Schools closed. Nobody caught it. Full story on the channel. #shorts #jerseydevil #truestory #legend #hollowmere",
    "tags": ["shorts"] + TAGS[:9],
    "thumbnail": {"bg": "swamp", "seed": 4, "creature": "gloamhound", "text": "DON'T LOOK UP"},
    "shots": [{
        "bg": "swamp", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 3, "ambient": 0.40, "focus": "odo", "fade": False,
        "chars": {"odo": {"x": 700}},
        "creatures": {"h1": {"type": "gloamhound", "x": 1150, "state": "hidden", "face": -1, "scale": 0.9},
                      "c1": {"type": "crow", "x": 900, "y": 420, "state": "hidden", "fly": 1}},
        "beats": [
            {"move": "odo", "to": 760, "speed": "creep"},
            S("narr", "New Jersey, 1909. Hoof prints across the rooftops.|Nueva Jersey, 1909. Huellas de pezuña sobre los tejados.|"
              "New Jersey, 1909. Hufspuren über die Dächer.|New Jersey, 1909. Des traces de sabots sur les toits.|"
              "New Jersey, 1909. Impronte di zoccoli sui tetti.|Nova Jersey, 1909. Pegadas de casco nos telhados.", **{"and": True}),
            {"sfx": "step", "and": True},
            {"show": "c1", "dur": 0.2},
            {"sfx": "flutter", "and": True},
            S("narr", "Police fired at something with wings. Schools closed.|La policía disparó a algo con alas. Cerraron escuelas.|"
              "Polizisten schossen auf etwas mit Flügeln. Schulen schlossen.|La police tira sur une chose ailée. Les écoles fermèrent.|"
              "La polizia sparò a qualcosa con le ali. Le scuole chiusero.|A polícia atirou em algo com asas. Escolas fecharam."),
            {"hide": "c1", "dur": 0.3},
            {"act": "odo", "do": "scared"},
            S("narr", "Would you walk the pines tonight?|¿Caminarías por los pinos esta noche?|Würdest du heute Nacht durch die Kiefern gehen?|"
              "Marcherais-tu dans les pins ce soir ?|Cammineresti tra i pini stanotte?|Você andaria pelos pinheiros esta noite?"),
            {"light": "out"},
            {"show": "h1", "dur": 0.1, "and": True},
            {"flash": True, "and": True},
            {"growl": "h1"},
            {"hide": "h1", "dur": 0.3},
            {"light": "on", "and": True},
            {"act": "odo", "do": "calm", "and": True},
            {"move": "odo", "to": 700, "speed": "walk", "and": True},
            S("narr", "Something screamed over the pines...|Algo gritó sobre los pinos...|Etwas schrie über den Kiefern...|"
              "Quelque chose hurla au-dessus des pins...|Qualcosa urlò sopra i pini...|Algo gritou sobre os pinheiros..."),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

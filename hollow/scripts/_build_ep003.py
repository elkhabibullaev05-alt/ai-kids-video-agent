"""Builds Hollowmere EP3 (true story: the Lost Colony of Roanoke, 1587-1590). Run: python3 scripts/_build_ep003.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Roanoke", "lost colony", "Croatoan",
        "North Carolina", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Roanoke_Colony",
           "https://www.nps.gov/fora/learn/historyculture/1590-voyage.htm",
           "https://www.dncr.nc.gov/blog/2016/08/18/origins-lost-colony-mystery"]

long_ = {
    "id": "ep003_long", "format": "long",
    "title": "The Colony That Vanished | True Story | Hollowmere Tales EP 3",
    "description": ("A true story. In 1587 about 115 English settlers, men, women and children, landed on Roanoke Island. "
                    "Their governor John White sailed home for supplies, and war kept him away for three years. "
                    "When he returned on August 18, 1590, his granddaughter Virginia Dare's third birthday, the colony was gone. "
                    "All that was left: \"CRO\" carved on a tree, and \"CROATOAN\" carved on a post.\n\n"
                    "Told from the historical records; theories are marked as theories.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #unsolvedmystery #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 3", "Virginia Dare", "John White"],
    "thumbnail": {"bg": "forest", "seed": 7, "creature": "figure", "text": "CROATOAN"},
    "shots": [
        {   # 1 cold open
            "bg": "forest", "seed": 7, "music": "drone", "wind": True, "eyes": 0, "lantern": 0.0, "ambient": 0.36,
            "cam": {"from": [960, 560, 1.0], "to": [960, 590, 1.18]},
            "beats": [
                {"sfx": "creak", "wait": 1.0},
                S("narr", "This is a true story, told from the records of 1587 to 1590.|Esta es una historia real, contada a partir de los registros de 1587 a 1590.|Dies ist eine wahre Geschichte, nach den Aufzeichnungen von 1587 bis 1590.|Ceci est une histoire vraie, tirée des archives de 1587 à 1590.|Questa è una storia vera, tratta dagli archivi dal 1587 al 1590.|Esta é uma história real, contada a partir dos registros de 1587 a 1590."),
                S("narr", "In 1587, about one hundred and fifteen English settlers landed on Roanoke Island.|"
                  "En 1587, unos ciento quince colonos ingleses llegaron a la isla de Roanoke.|"
                  "1587 landeten etwa hundertfünfzehn englische Siedler auf Roanoke Island.|"
                  "En 1587, environ cent quinze colons anglais débarquèrent sur l'île de Roanoke.|"
                  "Nel 1587, circa centoquindici coloni inglesi sbarcarono sull'isola di Roanoke.|"
                  "Em 1587, cerca de cento e quinze colonos ingleses desembarcaram na ilha de Roanoke."),
                S("narr", "Three years later, every one of them was gone.|Tres años después, todos ellos habían desaparecido.|"
                  "Drei Jahre später war jeder Einzelne von ihnen verschwunden.|Trois ans plus tard, tous avaient disparu.|"
                  "Tre anni dopo, erano spariti tutti.|Três anos depois, todos eles tinham sumido."),
                S("narr", "They left behind just one word, carved into a wooden post.|Solo dejaron una palabra, tallada en un poste de madera.|"
                  "Sie hinterließen nur ein Wort, in einen Holzpfosten geschnitzt.|Ils ne laissèrent qu'un mot, gravé dans un poteau de bois.|"
                  "Lasciarono solo una parola, incisa su un palo di legno.|Deixaram apenas uma palavra, entalhada num poste de madeira."),
                {"sfx": "snap", "wait": 0.6},
                {"card": "CROATOAN", "dur": 2.8},
            ],
            "tail": 0.2,
        },
        {   # 2 the colony and Virginia Dare
            "bg": "village", "seed": 3, "music": "lullaby", "eyes": 0, "ambient": 0.46,
            "lights": [{"kind": "fire", "x": 1100, "y": 900, "r": 600}],
            "cam": {"from": [900, 600, 1.12], "to": [1000, 620, 1.2]},
            "chars": {"odo": {"x": 480}, "moth": {"x": 640, "y": 650}},
            "creatures": {"white": {"type": "figure", "x": 1400, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "They settled on the coast of what is now North Carolina. Men, women, and children.|Se asentaron en la costa de lo que hoy es Carolina del Norte. Hombres, mujeres y niños.|"
                  "Sie siedelten an der Küste des heutigen North Carolina. Männer, Frauen und Kinder.|Ils s'installèrent sur la côte de l'actuelle Caroline du Nord. Hommes, femmes et enfants.|"
                  "Si stabilirono sulla costa dell'attuale Carolina del Nord. Uomini, donne e bambini.|Eles se instalaram na costa da atual Carolina do Norte. Homens, mulheres e crianças."),
                S("narr", "On August 18, 1587, a baby girl was born there. Her name was Virginia Dare.|El 18 de agosto de 1587 nació allí una niña. Se llamaba Virginia Dare.|"
                  "Am 18. August 1587 wurde dort ein Mädchen geboren. Ihr Name war Virginia Dare.|Le 18 août 1587, une petite fille y naquit. Elle s'appelait Virginia Dare.|"
                  "Il 18 agosto 1587 vi nacque una bambina. Si chiamava Virginia Dare.|Em 18 de agosto de 1587, nasceu ali uma menina. Seu nome era Virginia Dare."),
                {"show": "white", "dur": 1.2},
                S("narr", "Her grandfather, John White, was the governor of the colony.|Su abuelo, John White, era el gobernador de la colonia.|"
                  "Ihr Großvater, John White, war der Gouverneur der Kolonie.|Son grand-père, John White, était le gouverneur de la colonie.|"
                  "Suo nonno, John White, era il governatore della colonia.|O avô dela, John White, era o governador da colônia."),
                S("narr", "The settlers persuaded him to sail back to England, to bring help and supplies.|Los colonos lo convencieron de volver a Inglaterra a buscar ayuda y provisiones.|"
                  "Die Siedler überredeten ihn, nach England zu segeln und Hilfe und Vorräte zu holen.|Les colons le persuadèrent de rentrer en Angleterre chercher de l'aide et des vivres.|"
                  "I coloni lo convinsero a tornare in Inghilterra per portare aiuti e provviste.|Os colonos o convenceram a voltar à Inglaterra para buscar ajuda e suprimentos."),
                S("odo", "He left his family behind?|¿Dejó atrás a su familia?|Er hat seine Familie zurückgelassen?|Il a laissé sa famille derrière lui ?|Ha lasciato indietro la sua famiglia?|Ele deixou a família para trás?"),
                S("moth", "He promised to come back. Everyone thought it would take a few months.|Prometió volver. Todos pensaban que tardaría unos meses.|"
                  "Er versprach zurückzukommen. Alle dachten, es dauert ein paar Monate.|Il a promis de revenir. Tout le monde pensait que ça prendrait quelques mois.|"
                  "Promise di tornare. Tutti pensavano che ci sarebbero voluti pochi mesi.|Ele prometeu voltar. Todos achavam que levaria alguns meses."),
                S("narr", "Before he left, they agreed on a secret sign.|Antes de irse, acordaron una señal secreta.|"
                  "Bevor er ging, vereinbarten sie ein geheimes Zeichen.|Avant son départ, ils convinrent d'un signe secret.|"
                  "Prima che partisse, concordarono un segnale segreto.|Antes de ele partir, combinaram um sinal secreto."),
                S("narr", "If they moved, they would carve where they had gone. If in danger, a cross.|Si se mudaban, tallarían adónde habían ido. Si había peligro, una cruz.|"
                  "Wenn sie fortzogen, würden sie das Ziel einschnitzen. Bei Gefahr ein Kreuz.|S'ils partaient, ils graveraient où ils allaient. En cas de danger, une croix.|"
                  "Se si spostavano, avrebbero inciso dove erano andati. In caso di pericolo, una croce.|Se mudassem, entalhariam para onde foram. Se em perigo, uma cruz."),
                {"hide": "white", "dur": 1.2},
            ],
            "tail": 0.3,
        },
        {   # 3 three years away
            "bg": "sea", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
            "cam": {"from": [960, 600, 1.1], "to": [1040, 610, 1.2]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "beats": [
                S("narr", "But England went to war with Spain, and ships could not be spared.|Pero Inglaterra entró en guerra con España, y no se podían prestar barcos.|"
                  "Doch England zog gegen Spanien in den Krieg, und Schiffe wurden gebraucht.|Mais l'Angleterre entra en guerre contre l'Espagne, et les navires étaient réquisitionnés.|"
                  "Ma l'Inghilterra entrò in guerra con la Spagna, e le navi non potevano partire.|Mas a Inglaterra entrou em guerra com a Espanha, e não havia navios livres."),
                {"shake": 0.6, "power": 8},
                S("narr", "In 1588 White tried again, but his ships were robbed at sea.|En 1588 White lo intentó de nuevo, pero sus barcos fueron asaltados en el mar.|"
                  "1588 versuchte White es erneut, doch seine Schiffe wurden auf See ausgeraubt.|En 1588, White réessaya, mais ses navires furent pillés en mer.|"
                  "Nel 1588 White ci riprovò, ma le sue navi furono derubate in mare.|Em 1588, White tentou de novo, mas seus navios foram roubados no mar."),
                S("narr", "It took him three long years to get back.|Tardó tres largos años en volver.|Es dauerte drei lange Jahre, bis er zurückkam.|"
                  "Il lui fallut trois longues années pour revenir.|Gli ci vollero tre lunghi anni per tornare.|Ele levou três longos anos para voltar."),
                S("odo", "Three years... His granddaughter wouldn't even know him.|Tres años... Su nieta ni siquiera lo conocería.|Drei Jahre... Seine Enkelin würde ihn nicht einmal kennen.|"
                  "Trois ans... Sa petite-fille ne le reconnaîtrait même pas.|Tre anni... Sua nipote non lo conoscerebbe nemmeno.|Três anos... A neta nem o conheceria."),
                S("moth", "He was hoping she'd be there to meet him at all.|Él esperaba que, al menos, ella estuviera allí.|"
                  "Er hoffte, dass sie überhaupt noch da war.|Il espérait simplement qu'elle serait encore là.|"
                  "Sperava solo che lei fosse ancora lì.|Ele só esperava que ela ainda estivesse lá."),
            ],
            "tail": 0.3,
        },
        {   # 4 landing, 18 August 1590
            "bg": "forest", "seed": 4, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1080, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"c1": {"type": "crow", "x": 1400, "y": 460, "state": "hidden"}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "walk"},
                {"move": "moth", "to": 720, "speed": "walk", "and": True},
                S("narr", "On August 18, 1590, Virginia's third birthday, White landed on Roanoke again.|El 18 de agosto de 1590, el tercer cumpleaños de Virginia, White desembarcó otra vez en Roanoke.|"
                  "Am 18. August 1590, Virginias drittem Geburtstag, landete White wieder auf Roanoke.|Le 18 août 1590, jour des trois ans de Virginia, White débarqua de nouveau à Roanoke.|"
                  "Il 18 agosto 1590, terzo compleanno di Virginia, White sbarcò di nuovo a Roanoke.|Em 18 de agosto de 1590, terceiro aniversário de Virginia, White desembarcou de novo em Roanoke."),
                S("narr", "Days before, his ships had seen smoke rising from the island.|Días antes, sus barcos habían visto humo saliendo de la isla.|"
                  "Tage zuvor hatten seine Schiffe Rauch über der Insel gesehen.|Quelques jours plus tôt, ses navires avaient vu de la fumée sur l'île.|"
                  "Giorni prima, le sue navi avevano visto del fumo salire dall'isola.|Dias antes, seus navios tinham visto fumaça subindo da ilha."),
                S("narr", "His men found fresh tracks. But nobody came to meet them.|Sus hombres encontraron huellas frescas. Pero nadie salió a recibirlos.|"
                  "Seine Männer fanden frische Spuren. Doch niemand kam ihnen entgegen.|Ses hommes trouvèrent des traces fraîches. Mais personne ne vint à leur rencontre.|"
                  "I suoi uomini trovarono tracce fresche. Ma nessuno venne loro incontro.|Seus homens acharam pegadas frescas. Mas ninguém veio recebê-los."),
                {"sfx": "snap", "wait": 0.8},
                {"act": "odo", "do": "scared"},
                {"show": "c1", "dur": 0.6},
                {"sfx": "caw", "and": True},
                S("narr", "Then, on a tree, they found three letters carved into the bark.|Entonces, en un árbol, encontraron tres letras talladas en la corteza.|"
                  "Dann fanden sie an einem Baum drei Buchstaben, in die Rinde geschnitzt.|Puis, sur un arbre, ils trouvèrent trois lettres gravées dans l'écorce.|"
                  "Poi, su un albero, trovarono tre lettere incise nella corteccia.|Então, numa árvore, acharam três letras entalhadas na casca."),
                {"wait": 0.5},
                S("odo", "C... R... O...|C... R... O...|C... R... O...|C... R... O...|C... R... O...|C... R... O..."),
                S("moth", "That's not a word. It's the beginning of one.|Eso no es una palabra. Es el comienzo de una.|"
                  "Das ist kein Wort. Das ist der Anfang von einem.|Ce n'est pas un mot. C'est le début d'un mot.|"
                  "Non è una parola. È l'inizio di una.|Isso não é uma palavra. É o começo de uma."),
                {"move": "odo", "to": "off_right", "speed": "walk"},
                {"move": "moth", "to": "off_right", "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 5 the empty fort
            "bg": "village", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 620, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1},
                          "g2": {"type": "ghost", "x": 1620, "state": "hidden", "face": -1, "scale": 0.7}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", "and": True},
                S("narr", "Inside the fort, the houses had been taken down. The boats were gone.|Dentro del fuerte, las casas habían sido desmontadas. Los botes ya no estaban.|"
                  "Im Fort waren die Häuser abgebaut. Die Boote waren fort.|Dans le fort, les maisons avaient été démontées. Les bateaux avaient disparu.|"
                  "Dentro il forte, le case erano state smontate. Le barche erano sparite.|Dentro do forte, as casas tinham sido desmontadas. Os barcos tinham sumido."),
                S("narr", "Buried chests had been dug up and looted. Three were White's own.|Unos baúles enterrados habían sido desenterrados y saqueados. Tres eran del propio White.|"
                  "Vergrabene Truhen waren ausgegraben und geplündert. Drei gehörten White selbst.|Des coffres enterrés avaient été déterrés et pillés. Trois appartenaient à White.|"
                  "Dei bauli sepolti erano stati dissotterrati e saccheggiati. Tre erano di White.|Baús enterrados tinham sido desenterrados e saqueados. Três eram do próprio White."),
                S("narr", "There was no sign of a fight. No sign of a hurried escape.|No había señales de lucha. Ni de una huida apresurada.|"
                  "Es gab keine Spur eines Kampfes. Keine Spur einer hastigen Flucht.|Aucun signe de combat. Aucun signe de fuite précipitée.|"
                  "Nessun segno di lotta. Nessun segno di una fuga affrettata.|Nenhum sinal de luta. Nenhum sinal de fuga apressada."),
                {"sfx": "creak", "wait": 0.8},
                {"flash": True},
                S("narr", "And on a post of the palisade, one word: CROATOAN.|Y en un poste de la empalizada, una palabra: CROATOAN.|"
                  "Und auf einem Pfosten der Palisade ein Wort: CROATOAN.|Et sur un poteau de la palissade, un mot : CROATOAN.|"
                  "E su un palo della palizzata, una parola: CROATOAN.|E num poste da paliçada, uma palavra: CROATOAN."),
                {"wait": 0.6},
                S("narr", "There was no cross.|No había ninguna cruz.|Es gab kein Kreuz.|Il n'y avait pas de croix.|Non c'era nessuna croce.|Não havia cruz."),
                S("odo", "No cross... So they weren't in danger?|Sin cruz... ¿Entonces no estaban en peligro?|Kein Kreuz... Also waren sie nicht in Gefahr?|"
                  "Pas de croix... Donc ils n'étaient pas en danger ?|Nessuna croce... Quindi non erano in pericolo?|Sem cruz... Então eles não estavam em perigo?"),
                S("moth", "That's what White believed. That's what he had to believe.|Eso creyó White. Eso necesitaba creer.|"
                  "Das glaubte White. Das musste er glauben.|C'est ce que White crut. C'est ce qu'il avait besoin de croire.|"
                  "È ciò che credette White. Ciò che doveva credere.|Foi o que White acreditou. O que ele precisava acreditar."),
                {"show": "g1", "dur": 1.6},
                {"show": "g2", "dur": 1.6, "and": True},
                {"wait": 1.0},
                {"hide": "g1", "dur": 1.2},
                {"hide": "g2", "dur": 1.2, "and": True},
            ],
            "tail": 0.3,
        },
        {   # 6 the storm and the unanswered question
            "bg": "sea", "seed": 5, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [760, 640, 1.24]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "beats": [
                S("narr", "Croatoan was an island to the south, home of the Croatoan people.|Croatoan era una isla al sur, hogar del pueblo croatoan.|"
                  "Croatoan war eine Insel im Süden, Heimat des Volkes der Croatoan.|Croatoan était une île au sud, foyer du peuple croatoan.|"
                  "Croatoan era un'isola a sud, terra del popolo croatoan.|Croatoan era uma ilha ao sul, lar do povo croatoan."),
                S("narr", "White wanted to sail there at once. But a storm came.|White quiso navegar allí de inmediato. Pero llegó una tormenta.|"
                  "White wollte sofort dorthin segeln. Doch ein Sturm zog auf.|White voulut y naviguer aussitôt. Mais une tempête arriva.|"
                  "White voleva salpare subito. Ma arrivò una tempesta.|White quis navegar para lá na hora. Mas veio uma tempestade."),
                {"shake": 0.8, "power": 14},
                {"sfx": "whoosh", "and": True},
                S("narr", "An anchor cable snapped, and his ships could not stay to search.|Se rompió un cable del ancla, y sus barcos no pudieron quedarse a buscar.|"
                  "Ein Ankertau riss, und seine Schiffe konnten nicht bleiben, um zu suchen.|Un câble d'ancre céda, et ses navires ne purent rester chercher.|"
                  "Si spezzò un cavo dell'ancora, e le sue navi non poterono restare a cercare.|Um cabo da âncora arrebentou, e os navios não puderam ficar para procurar."),
                S("narr", "John White sailed away. He never saw Roanoke again.|John White zarpó. Nunca volvió a ver Roanoke.|"
                  "John White segelte davon. Er sah Roanoke nie wieder.|John White repartit. Il ne revit jamais Roanoke.|"
                  "John White salpò. Non rivide mai più Roanoke.|John White partiu. Nunca mais viu Roanoke."),
                S("narr", "Today, archaeologists are still digging. Some think the settlers joined the Croatoan people.|Hoy, los arqueólogos siguen excavando. Algunos creen que los colonos se unieron a los croatoan.|"
                  "Heute graben Archäologen noch immer. Manche glauben, die Siedler lebten bei den Croatoan.|Aujourd'hui, les archéologues fouillent encore. Certains pensent que les colons rejoignirent les Croatoans.|"
                  "Oggi gli archeologi scavano ancora. Alcuni pensano che i coloni si unirono ai croatoan.|Hoje, arqueólogos ainda escavam. Alguns acham que os colonos se juntaram aos croatoan."),
                S("narr", "Others found English pottery far inland. Nothing has been proven.|Otros hallaron cerámica inglesa tierra adentro. Nada se ha demostrado.|"
                  "Andere fanden englische Keramik weit im Landesinneren. Nichts ist bewiesen.|D'autres ont trouvé de la poterie anglaise loin dans les terres. Rien n'est prouvé.|"
                  "Altri hanno trovato ceramiche inglesi nell'entroterra. Niente è stato provato.|Outros acharam cerâmica inglesa terra adentro. Nada foi provado."),
                S("odo", "And Virginia?|¿Y Virginia?|Und Virginia?|Et Virginia ?|E Virginia?|E Virginia?"),
                {"wait": 0.8},
                S("narr", "Over a hundred people, and a little girl of three... never seen again.|Más de cien personas, y una niña de tres años... nunca más vistas.|"
                  "Über hundert Menschen und ein dreijähriges Mädchen... nie wieder gesehen.|Plus de cent personnes, et une fillette de trois ans... jamais revues.|"
                  "Più di cento persone, e una bimba di tre anni... mai più viste.|Mais de cem pessoas, e uma menina de três anos... nunca mais vistas."),
                {"sfx": "bell", "wait": 0.8},
                {"card": "A TRUE STORY. STILL UNSOLVED.", "dur": 3.0},
            ],
            "tail": 0.2,
        },
    ],
}

short1 = {   # the real fact
    "id": "ep003_short1", "format": "short",
    "title": "115 people vanished. They left one word. 🪓 #shorts",
    "hook": "THEY LEFT ONE WORD",
    "description": "True story: in 1590, John White returned to the Roanoke colony. Everyone was gone. Only one word was carved on a post: CROATOAN. #shorts #truestory #unsolvedmystery #roanoke #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "forest", "seed": 7, "creature": "ghost", "text": "CROATOAN"},
    "shots": [{
        "bg": "forest", "seed": 7, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.38, "focus": "odo",
        "chars": {"odo": {"x": 760}},
        "creatures": {"g1": {"type": "ghost", "x": 1150, "state": "hidden", "face": -1}},
        "beats": [
            {"sfx": "creak", "wait": 0.8},
            S("narr", "True story. 1590. A governor returns to his colony after three years.|Historia real. 1590. Un gobernador vuelve a su colonia tras tres años.|"
              "Wahre Geschichte. 1590. Ein Gouverneur kehrt nach drei Jahren zu seiner Kolonie zurück.|Histoire vraie. 1590. Un gouverneur revient dans sa colonie après trois ans.|"
              "Storia vera. 1590. Un governatore torna alla sua colonia dopo tre anni.|História real. 1590. Um governador volta à sua colônia depois de três anos."),
            S("narr", "About a hundred and fifteen people are gone. No sign of a fight.|Unas ciento quince personas han desaparecido. Ni rastro de lucha.|"
              "Etwa hundertfünfzehn Menschen sind fort. Keine Spur eines Kampfes.|Environ cent quinze personnes ont disparu. Aucune trace de combat.|"
              "Circa centoquindici persone sono sparite. Nessun segno di lotta.|Cerca de cento e quinze pessoas sumiram. Nenhum sinal de luta."),
            S("narr", "Only one word, carved into a post: CROATOAN.|Solo una palabra, tallada en un poste: CROATOAN.|"
              "Nur ein Wort, in einen Pfosten geschnitzt: CROATOAN.|Un seul mot, gravé dans un poteau : CROATOAN.|"
              "Solo una parola, incisa su un palo: CROATOAN.|Só uma palavra, entalhada num poste: CROATOAN."),
            {"act": "odo", "do": "turn"},
            {"light": "out"},
            {"flash": True, "and": True},
            {"show": "g1", "dur": 0.1, "and": True},
            {"wait": 0.8},
            S("narr", "They were never seen again.|Nunca se les volvió a ver.|Man sah sie nie wieder.|On ne les revit jamais.|Non furono mai più visti.|Nunca mais foram vistos."),
        ],
        "tail": 1.6,
    }],
}

short2 = {   # would you
    "id": "ep003_short2", "format": "short",
    "title": "Would YOU stay in the colony? ⛵ #shorts",
    "hook": "STAY OR SAIL?",
    "description": "It's 1587. The governor sails home and promises to be back in months. It takes three years, and everyone who stayed is gone. Would you stay or sail? Comment STAY or SAIL 👇 #shorts #truestory #roanoke #hollowmere",
    "tags": ["shorts"] + TAGS[:8] + ["would you rather"],
    "thumbnail": {"bg": "village", "seed": 3, "creature": "figure", "text": "STAY OR SAIL"},
    "shots": [{
        "bg": "village", "seed": 3, "music": "drone", "eyes": 0, "ambient": 0.42,
        "lights": [{"kind": "fire", "x": 960, "y": 905, "r": 600}],
        "chars": {"odo": {"x": 760}},
        "creatures": {"white": {"type": "figure", "x": 1170, "seed": 0, "state": "hidden", "face": -1}},
        "focus": ["odo", "white"],
        "beats": [
            S("narr", "It is 1587. A ship is leaving the new colony for England.|Es 1587. Un barco sale de la nueva colonia hacia Inglaterra.|"
              "Es ist 1587. Ein Schiff verlässt die neue Kolonie Richtung England.|Nous sommes en 1587. Un navire quitte la nouvelle colonie pour l'Angleterre.|"
              "È il 1587. Una nave lascia la nuova colonia per l'Inghilterra.|É 1587. Um navio deixa a nova colônia rumo à Inglaterra."),
            {"show": "white", "dur": 1.5},
            S("narr", "The governor promises to return in a few months. It will take three years.|El gobernador promete volver en unos meses. Tardará tres años.|"
              "Der Gouverneur verspricht, in ein paar Monaten zurückzukehren. Es werden drei Jahre.|Le gouverneur promet de revenir dans quelques mois. Il mettra trois ans.|"
              "Il governatore promette di tornare in pochi mesi. Ci vorranno tre anni.|O governador promete voltar em poucos meses. Vai levar três anos."),
            S("narr", "When he comes back, everyone who stayed is gone.|Cuando regresa, todos los que se quedaron han desaparecido.|"
              "Als er zurückkommt, sind alle, die blieben, verschwunden.|À son retour, tous ceux qui sont restés ont disparu.|"
              "Quando torna, tutti quelli che sono rimasti sono spariti.|Quando ele volta, todos que ficaram sumiram."),
            {"act": "odo", "do": "shake"},
            S("narr", "Would YOU stay in the colony, or sail home? Comment STAY or SAIL.|¿TÚ te quedarías en la colonia o volverías? Comenta QUEDARME o ZARPAR.|"
              "Würdest DU bleiben oder heimsegeln? Schreib BLEIBEN oder SEGELN.|Et TOI, tu resterais ou tu rentrerais ? Écris RESTER ou PARTIR.|"
              "TU resteresti nella colonia o torneresti a casa? Scrivi RESTO o PARTO.|VOCÊ ficaria na colônia ou voltaria? Comente FICAR ou PARTIR."),
        ],
        "tail": 1.2,
    }],
}

short3 = {   # scariest moment
    "id": "ep003_short3", "format": "short",
    "title": "Three letters carved on a tree... C R O 🌲 #shorts",
    "hook": "C... R... O...",
    "description": "August 18, 1590: fresh tracks, nobody there, and three letters carved on a tree. Full true story on the channel. #shorts #truestory #roanoke #unsolvedmystery #hollowmere",
    "tags": ["shorts"] + TAGS,
    "thumbnail": {"bg": "forest", "seed": 4, "creature": "ghost", "text": "C R O"},
    "shots": [{
        "bg": "forest", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
        "chars": {"odo": {"x": 700}, "moth": {"x": 820, "y": 650}},
        "creatures": {"g1": {"type": "ghost", "x": 1250, "state": "hidden", "face": -1}},
        "focus": ["odo", "g1"],
        "beats": [
            S("narr", "August 18, 1590. Smoke had been seen. Fresh tracks on the island.|18 de agosto de 1590. Se había visto humo. Huellas frescas en la isla.|"
              "18. August 1590. Man hatte Rauch gesehen. Frische Spuren auf der Insel.|18 août 1590. On avait vu de la fumée. Des traces fraîches sur l'île.|"
              "18 agosto 1590. Si era visto del fumo. Tracce fresche sull'isola.|18 de agosto de 1590. Tinham visto fumaça. Pegadas frescas na ilha."),
            S("narr", "But nobody answers. Then, on a tree, three carved letters.|Pero nadie responde. Entonces, en un árbol, tres letras talladas.|"
              "Doch niemand antwortet. Dann, an einem Baum, drei geschnitzte Buchstaben.|Mais personne ne répond. Puis, sur un arbre, trois lettres gravées.|"
              "Ma nessuno risponde. Poi, su un albero, tre lettere incise.|Mas ninguém responde. Então, numa árvore, três letras entalhadas."),
            {"act": "odo", "do": "scared"},
            S("odo", "C... R... O...|C... R... O...|C... R... O...|C... R... O...|C... R... O...|C... R... O..."),
            {"lunge": "g1", "to": 1000},
            {"show": "g1", "dur": 0.1, "and": True},
            S("narr", "Full true story on the channel.|Historia real completa en el canal.|Die ganze wahre Geschichte auf dem Kanal.|L'histoire vraie complète sur la chaîne.|Storia vera completa sul canale.|História real completa no canal."),
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

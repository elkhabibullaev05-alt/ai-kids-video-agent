"""Builds Hollowmere EP12 (recorded legend: the Green Children of Woolpit, Suffolk, England, 12th century).
Sources: William of Newburgh, Historia rerum Anglicarum (c.1189-98) dates it to the reign of King Stephen (1135-1154);
Ralph of Coggeshall, Chronicon Anglicanum (c.1220) names Sir Richard de Calne of Wykes as host. At harvest time, two
children - brother and sister - were found by one of the wolf pits that gave Woolpit its name; green skin, strange
clothes, unknown language. They refused food for days until they saw raw broad beans; lived on beans for months, then
learned to eat bread and lost the green colour. The boy grew sickly and did not live long; the girl learned English:
a land of twilight where the sun never shone, called St Martin's Land (William), where everything was green (Ralph);
they had been herding their father's flocks, heard a loud sound like bells (William: like the bells of Bury St
Edmunds) / went through a cavern with ringing bells (Ralph), and came out by the pit. She worked for the knight and is
said to have married a man from King's Lynn. Theories: Flemish orphans of the Anarchy, 'green sickness' from hunger.
Run: python3 scripts/_build_ep012.py
Retention rules (2026-10-16): frame 1 = motion + big text hook, narration from 0 s mid-tension, something new every
4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to the first frame.
Pack 2 of 2026-10-20 -> 1 long + 1 Short. Children are drawn with figure seeds 10/11 (green-skinned figure, engine)."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    assert len(parts[0].split()) <= 16, parts[0]
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


A = {"and": True}
TAGS = ["true story", "unsolved mystery", "real horror story", "green children of Woolpit", "Woolpit", "Suffolk",
        "English folklore", "medieval mystery", "St Martin's Land", "12th century", "horror animation",
        "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Green_children_of_Woolpit",
           "https://woolpitparishcouncil.gov.uk/information-2/a-short-history",
           "https://www.historic-uk.com/CultureUK/The-Green-Children-of-Woolpit/"]

KID = lambda x=1350, sd=10, sc=0.62: {"type": "figure", "x": x, "seed": sd, "face": -1, "state": "hidden", "scale": sc}
MAN = lambda x=1400, sd=0, sc=0.95: {"type": "figure", "x": x, "seed": sd, "face": -1, "state": "hidden", "scale": sc}
GHOST = lambda x=1450, sc=0.62: {"type": "ghost", "x": x, "state": "hidden", "face": -1, "scale": sc}
CROW = lambda x=1250, y=330: {"type": "crow", "x": x, "y": y, "state": "hidden", "fly": 1}
MOON = [{"kind": "moon", "x": 1450, "y": 220, "r": 900}]
FIRE = [{"kind": "fire", "x": 1250, "y": 900, "r": 560}]

long_ = {
    "id": "ep012_long", "format": "long",
    "title": "Where Did the Green Children Come From?",
    "hook": "THEY CAME FROM BELOW", "hook_dur": 4.5,
    "description": ("A medieval mystery from England, written down by two chroniclers in the 1100s. At harvest time, "
                    "in the Suffolk village of Woolpit, reapers found two children - a brother and a sister - beside one of "
                    "the old wolf pits that gave the village its name. Their skin was green. Their clothes were strange, "
                    "and no one could understand a word they said. They were taken to the house of Sir Richard de Calne, "
                    "where they refused all food for days - until they saw raw broad beans. Slowly they learned to eat bread, "
                    "and the green faded from their skin. The boy grew weak and did not live long, but the girl learned English "
                    "and said they came from a land of twilight, where the sun never shone: St Martin's Land. They had been "
                    "herding their father's animals, heard a sound like ringing bells, and came out by the pit. "
                    "William of Newburgh and Ralph of Coggeshall both recorded the story. Were they lost Flemish children, "
                    "sick from hunger? Or did they come from somewhere else? No one knows.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #woolpit #greenchildren #folklore #medieval #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 12", "William of Newburgh", "Ralph of Coggeshall", "wolf pit", "true story history"],
    "thumbnail": {"bg": "village", "seed": 2, "creature": "figure", "cseed": 11, "text": "GREEN CHILDREN"},
    "shots": [
        {   # 1 cold open: two small shapes climb out of the pit; motion + hook from frame 1
            "bg": "forest", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 2, "lantern": 1.0, "ambient": 0.40, "fade": False,
            "lights": MOON,
            "cam": {"from": [920, 600, 1.22], "to": [1080, 620, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"boy": KID(1330, 10), "girl": KID(1470, 11, 0.66)},
            "beats": [
                {"show": "boy", "dur": 0.05},
                {"show": "girl", "dur": 0.05, **A},
                {"flash": True, "dur": 0.8, **A},
                {"move": "odo", "to": 620, "speed": "creep", **A},
                {"move": "moth", "to": 760, "speed": "creep", **A},
                {"sfx": "bell", **A},
                S("narr", "Two children climbed out of a pit. And their skin was green.|Dos niños salieron de un foso. Y su piel era verde.|"
                  "Zwei Kinder kletterten aus einer Grube. Und ihre Haut war grün.|Deux enfants sortirent d'une fosse. Et leur peau était verte.|"
                  "Due bambini uscirono da una fossa. E la loro pelle era verde.|Duas crianças saíram de um poço. E a pele delas era verde.", **A),
                {"shake": 0.5, "power": 10, **A},
                {"sfx": "whisper"},
                S("narr", "This is a legend written down in England more than 800 years ago.|Es una leyenda escrita en Inglaterra hace más de 800 años.|"
                  "Dies ist eine Legende, vor über 800 Jahren in England aufgeschrieben.|C'est une légende écrite en Angleterre il y a plus de 800 ans.|"
                  "È una leggenda scritta in Inghilterra più di 800 anni fa.|É uma lenda escrita na Inglaterra há mais de 800 anos."),
                {"move": "boy", "to": 1250, "speed": "creep", **A},
                {"flash": True, "dur": 1.0},
                {"act": "odo", "do": "scared"},
                S("odo", "Mothwick... those children are looking at us. Their faces are green!|Mothwick... esos niños nos miran. ¡Sus caras son verdes!|"
                  "Mothwick... die Kinder sehen uns an. Ihre Gesichter sind grün!|Mothwick... ces enfants nous regardent. Leurs visages sont verts !|"
                  "Mothwick... quei bambini ci guardano. Hanno la faccia verde!|Mothwick... aquelas crianças estão nos olhando. Os rostos são verdes!"),
                {"sfx": "bell", **A},
                {"hide": "boy", "dur": 0.3},
                {"hide": "girl", "dur": 0.3, **A},
                S("moth", "Then listen for the bells, Odo. That's how they came.|Entonces escucha las campanas, Odo. Así llegaron ellos.|"
                  "Dann hör auf die Glocken, Odo. So sind sie gekommen.|Alors écoute les cloches, Odo. C'est ainsi qu'ils sont venus.|"
                  "Allora ascolta le campane, Odo. È così che sono arrivati.|Então escute os sinos, Odo. Foi assim que eles vieram."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.2,
        },
        {   # 2 Woolpit and the wolf pits
            "bg": "village", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.44,
            "lights": MOON,
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"c1": CROW(), "h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 0.9}},
            "beats": [
                S("narr", "The village is called Woolpit, in Suffolk, in the east of England.|El pueblo se llama Woolpit, en Suffolk, al este de Inglaterra.|"
                  "Das Dorf heißt Woolpit, in Suffolk, im Osten Englands.|Le village s'appelle Woolpit, dans le Suffolk, à l'est de l'Angleterre.|"
                  "Il villaggio si chiama Woolpit, nel Suffolk, nell'est dell'Inghilterra.|A vila se chama Woolpit, em Suffolk, no leste da Inglaterra."),
                {"show": "c1", "dur": 0.2, **A},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "Its name comes from the old wolf pits: deep holes dug to trap wolves.|Su nombre viene de los fosos para lobos: hoyos hondos para atraparlos.|"
                  "Der Name kommt von alten Wolfsgruben: tiefe Löcher, um Wölfe zu fangen.|Son nom vient des fosses à loups : des trous profonds pour piéger les loups.|"
                  "Il nome viene dalle fosse per lupi: buche profonde per catturarli.|O nome vem dos fossos de lobos: buracos fundos para prender lobos.", **A),
                {"show": "h1", "dur": 0.3},
                {"growl": "h1", **A},
                {"hide": "h1", "dur": 0.4},
                S("narr", "Two monks wrote the story down: William of Newburgh and Ralph of Coggeshall.|Dos monjes la escribieron: Guillermo de Newburgh y Ralph de Coggeshall.|"
                  "Zwei Mönche schrieben sie auf: William of Newburgh und Ralph of Coggeshall.|Deux moines l'ont écrite : Guillaume de Newburgh et Raoul de Coggeshall.|"
                  "Due monaci la scrissero: Guglielmo di Newburgh e Ralph di Coggeshall.|Dois monges a escreveram: William de Newburgh e Ralph de Coggeshall.", **A),
                {"flash": True, "dur": 1.0},
                S("narr", "William says it happened when King Stephen ruled, between 1135 and 1154.|Guillermo dice que pasó bajo el rey Esteban, entre 1135 y 1154.|"
                  "William sagt, es geschah unter König Stephan, zwischen 1135 und 1154.|Guillaume dit que c'était sous le roi Étienne, entre 1135 et 1154.|"
                  "Guglielmo dice che accadde sotto re Stefano, tra il 1135 e il 1154.|William diz que foi no reinado de Estêvão, entre 1135 e 1154.", **A),
                {"act": "odo", "do": "shake"},
                S("odo", "Wolf pits? I'm not walking anywhere near a wolf pit.|¿Fosos de lobos? No pienso acercarme a un foso de lobos.|"
                  "Wolfsgruben? Ich gehe nicht in die Nähe einer Wolfsgrube.|Des fosses à loups ? Je n'approche pas d'une fosse à loups.|"
                  "Fosse per lupi? Non mi avvicino a una fossa per lupi.|Fossos de lobos? Eu não chego perto de um fosso de lobos."),
                {"sfx": "step", **A},
                S("moth", "Too late, Odo. You're standing on the edge of one.|Demasiado tarde, Odo. Estás al borde de uno.|"
                  "Zu spät, Odo. Du stehst am Rand von einer.|Trop tard, Odo. Tu es au bord de l'une d'elles.|"
                  "Troppo tardi, Odo. Sei sul bordo di una.|Tarde demais, Odo. Você está na beira de um."),
                {"act": "odo", "do": "jump"},
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 3 harvest day: the children are found
            "bg": "clearing", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.46,
            "lights": MOON,
            "cam": {"from": [960, 600, 1.1], "to": [1080, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"reap": MAN(1150, 2, 0.95), "boy": KID(1380, 10), "girl": KID(1520, 11, 0.66)},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", **A},
                S("narr", "One summer, at harvest time, the reapers were working in the fields.|Un verano, en tiempo de cosecha, los segadores trabajaban en el campo.|"
                  "In einem Sommer, zur Erntezeit, arbeiteten die Schnitter auf den Feldern.|Un été, à la moisson, les moissonneurs travaillaient aux champs.|"
                  "Un'estate, al tempo del raccolto, i mietitori lavoravano nei campi.|Num verão, na colheita, os ceifeiros trabalhavam nos campos.", **A),
                {"show": "reap", "dur": 0.4},
                {"sfx": "snap", **A},
                {"flash": True, "dur": 1.0},
                {"show": "boy", "dur": 0.2, **A},
                {"show": "girl", "dur": 0.2, **A},
                S("narr", "Beside one of the wolf pits stood two children. A boy and his sister.|Junto a un foso de lobos había dos niños. Un niño y su hermana.|"
                  "Neben einer Wolfsgrube standen zwei Kinder. Ein Junge und seine Schwester.|Près d'une fosse à loups se tenaient deux enfants. Un garçon et sa sœur.|"
                  "Accanto a una fossa per lupi c'erano due bambini. Un bambino e sua sorella.|Ao lado de um fosso de lobos havia duas crianças. Um menino e a irmã.", **A),
                {"shake": 0.5, "power": 10, **A},
                S("narr", "Their skin was green all over. Ralph wrote: green like leeks.|Su piel era toda verde. Ralph escribió: verde como el puerro.|"
                  "Ihre Haut war ganz grün. Ralph schrieb: grün wie Lauch.|Leur peau était toute verte. Raoul écrivit : vert comme le poireau.|"
                  "La loro pelle era tutta verde. Ralph scrisse: verde come il porro.|A pele era toda verde. Ralph escreveu: verde como alho-poró."),
                {"sfx": "whisper", **A},
                {"move": "reap", "to": 1050, "speed": "walk", **A},
                S("narr", "Their clothes were made of cloth no one had ever seen.|Su ropa era de una tela que nadie había visto nunca.|"
                  "Ihre Kleidung war aus einem Stoff, den niemand je gesehen hatte.|Leurs habits étaient d'une étoffe que personne n'avait jamais vue.|"
                  "I loro vestiti erano di una stoffa mai vista.|As roupas eram de um pano que ninguém jamais tinha visto."),
                {"light": "flare"},
                S("narr", "And when they spoke, not one person in Woolpit understood a word.|Y cuando hablaban, nadie en Woolpit entendía ni una palabra.|"
                  "Und wenn sie sprachen, verstand in Woolpit niemand ein Wort.|Et quand ils parlaient, personne à Woolpit ne comprenait un mot.|"
                  "E quando parlavano, nessuno a Woolpit capiva una parola.|E quando falavam, ninguém em Woolpit entendia uma palavra.", **A),
                {"sfx": "whisper", **A},
                {"act": "odo", "do": "scared"},
                S("odo", "Where did they come from? There's nothing out here but fields!|¿De dónde salieron? ¡Aquí solo hay campos!|"
                  "Woher kamen sie? Hier gibt es nur Felder!|D'où venaient-ils ? Il n'y a que des champs ici !|"
                  "Da dove venivano? Qui ci sono solo campi!|De onde vieram? Aqui só tem campos!"),
                {"hide": "reap", "dur": 0.4, **A},
                S("moth", "Not fields, Odo. The pit. They came up out of the ground.|No los campos, Odo. El foso. Salieron de debajo de la tierra.|"
                  "Nicht die Felder, Odo. Die Grube. Sie kamen aus der Erde.|Pas les champs, Odo. La fosse. Ils sont sortis de sous la terre.|"
                  "Non i campi, Odo. La fossa. Sono usciti da sottoterra.|Não os campos, Odo. O fosso. Eles saíram de debaixo da terra."),
                {"sfx": "sting", **A},
                {"hide": "boy", "dur": 0.4, **A},
                {"hide": "girl", "dur": 0.4, **A},
            ],
            "tail": 0.3,
        },
        {   # 4 the knight's hall: the beans
            "bg": "manor", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "window", "x": 1250, "y": 600, "r": 520}],
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"kn": MAN(1180, 0, 1.0), "boy": KID(1400, 10), "girl": KID(1530, 11, 0.66)},
            "beats": [
                S("narr", "The children were taken to the house of a knight, Sir Richard de Calne.|Llevaron a los niños a casa de un caballero, Sir Richard de Calne.|"
                  "Die Kinder kamen ins Haus eines Ritters, Sir Richard de Calne.|On conduisit les enfants chez un chevalier, Sir Richard de Calne.|"
                  "I bambini furono portati a casa di un cavaliere, Sir Richard de Calne.|As crianças foram levadas à casa de um cavaleiro, Sir Richard de Calne."),
                {"show": "kn", "dur": 0.4, **A},
                {"sfx": "creak", **A},
                {"show": "boy", "dur": 0.3},
                {"show": "girl", "dur": 0.3, **A},
                S("narr", "He offered them bread and meat. They would not eat. They only cried.|Les ofreció pan y carne. No comían. Solo lloraban.|"
                  "Er bot ihnen Brot und Fleisch an. Sie aßen nicht. Sie weinten nur.|Il leur offrit pain et viande. Ils refusaient. Ils pleuraient.|"
                  "Offrì loro pane e carne. Non mangiavano. Piangevano soltanto.|Ofereceu pão e carne. Elas não comiam. Só choravam.", **A),
                {"flash": True, "dur": 1.0},
                S("narr", "Days went by. Then a servant carried in fresh bean plants from the field.|Pasaron días. Luego un criado trajo plantas de habas del campo.|"
                  "Tage vergingen. Dann trug ein Diener frische Bohnenpflanzen herein.|Des jours passèrent. Puis un serviteur apporta des plants de fèves.|"
                  "Passarono giorni. Poi un servo portò piante di fave dai campi.|Dias passaram. Então um criado trouxe pés de fava do campo.", **A),
                {"sfx": "step", **A},
                {"move": "boy", "to": 1300, "speed": "run"},
                {"move": "girl", "to": 1420, "speed": "run", **A},
                S("narr", "The children grabbed them, but they opened the stalks, not the pods.|Los niños las agarraron, pero abrían los tallos, no las vainas.|"
                  "Die Kinder griffen danach, doch sie öffneten die Stängel, nicht die Schoten.|Les enfants s'en saisirent, mais ouvraient les tiges, pas les cosses.|"
                  "I bambini le afferrarono, ma aprivano gli steli, non i baccelli.|As crianças pegaram, mas abriam os talos, não as vagens.", **A),
                {"shake": 0.4, "power": 8, **A},
                S("narr", "Someone showed them the beans inside. They ate them raw, and nothing else.|Alguien les mostró las habas. Las comieron crudas, y nada más.|"
                  "Jemand zeigte ihnen die Bohnen. Sie aßen sie roh, und sonst nichts.|Quelqu'un leur montra les fèves. Ils les mangèrent crues, et rien d'autre.|"
                  "Qualcuno mostrò loro le fave. Le mangiarono crude, e nient'altro.|Alguém mostrou as favas. Comeram cruas, e mais nada."),
                {"sfx": "snap", **A},
                {"act": "odo", "do": "shake"},
                S("odo", "Only raw beans? For how long?|¿Solo habas crudas? ¿Durante cuánto tiempo?|"
                  "Nur rohe Bohnen? Wie lange?|Seulement des fèves crues ? Pendant combien de temps ?|"
                  "Solo fave crude? Per quanto tempo?|Só favas cruas? Por quanto tempo?"),
                {"hide": "kn", "dur": 0.4, **A},
                S("moth", "For months, Odo. Then, slowly, they learned to eat bread.|Durante meses, Odo. Luego, poco a poco, aprendieron a comer pan.|"
                  "Monatelang, Odo. Dann lernten sie langsam, Brot zu essen.|Pendant des mois, Odo. Puis, peu à peu, ils apprirent à manger du pain.|"
                  "Per mesi, Odo. Poi, piano piano, impararono a mangiare il pane.|Por meses, Odo. Depois, aos poucos, aprenderam a comer pão."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 5 the green fades; the boy fades; the girl speaks
            "bg": "manor", "seed": 4, "music": "lullaby", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": FIRE,
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"boy": KID(1330, 10), "girl": KID(1480, 11, 0.66), "g1": GHOST(1330, 0.6)},
            "beats": [
                {"show": "boy", "dur": 0.3},
                {"show": "girl", "dur": 0.3, **A},
                S("narr", "As they ate bread, the green slowly faded from their skin.|Al comer pan, el verde se fue borrando de su piel.|"
                  "Mit dem Brot verblasste das Grün langsam auf ihrer Haut.|En mangeant du pain, le vert quitta peu à peu leur peau.|"
                  "Mangiando pane, il verde svanì piano dalla loro pelle.|Comendo pão, o verde foi sumindo da pele deles.", **A),
                {"sfx": "whoosh", **A},
                S("narr", "But the boy grew weaker and weaker. He did not live long.|Pero el niño se debilitó cada vez más. No vivió mucho.|"
                  "Doch der Junge wurde immer schwächer. Er lebte nicht lange.|Mais le garçon s'affaiblit de plus en plus. Il ne vécut pas longtemps.|"
                  "Ma il bambino si indebolì sempre di più. Non visse a lungo.|Mas o menino foi ficando mais fraco. Não viveu muito."),
                {"hide": "boy", "dur": 1.2, **A},
                {"light": "dim", **A},
                S("narr", "His sister lived. She learned English, and people asked her everything.|Su hermana vivió. Aprendió inglés y todos le preguntaban.|"
                  "Seine Schwester lebte. Sie lernte Englisch, und alle fragten sie aus.|Sa sœur survécut. Elle apprit l'anglais, et on la questionna sans fin.|"
                  "Sua sorella visse. Imparò l'inglese, e tutti la interrogavano.|A irmã sobreviveu. Aprendeu inglês, e todos lhe perguntavam tudo."),
                {"light": "on", **A},
                {"move": "girl", "to": 1380, "speed": "creep", **A},
                {"flash": True, "dur": 1.0},
                S("narr", "She said they came from a land where the sun never shone.|Dijo que venían de una tierra donde nunca brillaba el sol.|"
                  "Sie sagte, sie kämen aus einem Land, wo nie die Sonne schien.|Elle dit qu'ils venaient d'un pays où le soleil ne brillait jamais.|"
                  "Disse che venivano da una terra dove il sole non splendeva mai.|Disse que vinham de uma terra onde o sol nunca brilhava.", **A),
                {"sfx": "bell", **A},
                S("narr", "Only a dim light, like twilight. And everything there was green.|Solo una luz tenue, como el crepúsculo. Y allí todo era verde.|"
                  "Nur ein trübes Licht, wie Dämmerung. Und alles dort war grün.|Juste une faible lueur, comme le crépuscule. Et tout y était vert.|"
                  "Solo una luce fioca, come il crepuscolo. E là tutto era verde.|Só uma luz fraca, como o crepúsculo. E lá tudo era verde."),
                {"eyes": "open", **A},
                S("narr", "She called it St Martin's Land.|Lo llamó la Tierra de San Martín.|"
                  "Sie nannte es Sankt-Martins-Land.|Elle l'appelait la Terre de Saint-Martin.|"
                  "La chiamava Terra di San Martino.|Ela chamava de Terra de São Martinho."),
                {"eyes": "close"},
                {"act": "odo", "do": "hide"},
                {"show": "g1", "dur": 0.3, **A},
                S("odo", "Mothwick... who is standing there, next to her?|Mothwick... ¿quién está ahí, a su lado?|"
                  "Mothwick... wer steht da, neben ihr?|Mothwick... qui est là, à côté d'elle ?|"
                  "Mothwick... chi c'è lì, accanto a lei?|Mothwick... quem está ali, ao lado dela?"),
                {"growl": "g1", **A},
                {"lunge": "g1", "to": 1100},
                {"hide": "g1", "dur": 0.2},
                {"act": "odo", "do": "unhide", **A},
                S("moth", "Nobody, Odo. Just a shadow from the fire.|Nadie, Odo. Solo una sombra del fuego.|"
                  "Niemand, Odo. Nur ein Schatten vom Feuer.|Personne, Odo. Juste une ombre du feu.|"
                  "Nessuno, Odo. Solo un'ombra del fuoco.|Ninguém, Odo. Só uma sombra do fogo."),
            ],
            "tail": 0.3,
        },
        {   # 6 how they arrived: the bells and the cavern; theories
            "bg": "forest", "seed": 2, "music": "choir", "wind": True, "eyes": 3, "ambient": 0.38,
            "lights": MOON,
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"girl": KID(1400, 11, 0.66), "c1": CROW(1250, 320)},
            "beats": [
                S("narr", "How did they get to Woolpit? She said they were watching their father's animals.|¿Cómo llegaron? Dijo que cuidaban los animales de su padre.|"
                  "Wie kamen sie her? Sie sagte, sie hüteten die Tiere ihres Vaters.|Comment sont-ils arrivés ? Elle dit qu'ils gardaient les bêtes de leur père.|"
                  "Come arrivarono? Disse che badavano agli animali del padre.|Como chegaram? Ela disse que cuidavam dos animais do pai."),
                {"show": "girl", "dur": 0.4, **A},
                {"sfx": "bell", "wait": 0.3},
                S("narr", "Then they heard a great sound, like the ringing of church bells.|Entonces oyeron un gran sonido, como campanas de iglesia.|"
                  "Dann hörten sie einen lauten Klang, wie Kirchenglocken.|Puis ils entendirent un grand bruit, comme des cloches d'église.|"
                  "Poi sentirono un grande suono, come campane di chiesa.|Então ouviram um som forte, como sinos de igreja.", **A),
                {"shake": 0.5, "power": 10, **A},
                {"sfx": "bell"},
                S("narr", "Ralph wrote that they followed the sound into a cave, and walked a long way.|Ralph escribió que siguieron el sonido a una cueva y caminaron mucho.|"
                  "Ralph schrieb, sie folgten dem Klang in eine Höhle, einen langen Weg.|Raoul écrivit qu'ils suivirent le son dans une grotte, très longtemps.|"
                  "Ralph scrisse che seguirono il suono in una grotta, camminando a lungo.|Ralph escreveu que seguiram o som numa caverna e andaram muito.", **A),
                {"move": "girl", "to": 1300, "speed": "creep", **A},
                {"flash": True, "dur": 1.0},
                S("narr", "When they came out, the sun blinded them. They were by the wolf pit.|Al salir, el sol los cegó. Estaban junto al foso de lobos.|"
                  "Als sie herauskamen, blendete sie die Sonne. Sie waren an der Wolfsgrube.|En sortant, le soleil les aveugla. Ils étaient près de la fosse à loups.|"
                  "Usciti, il sole li accecò. Erano accanto alla fossa per lupi.|Ao sair, o sol os cegou. Estavam junto ao fosso de lobos.", **A),
                {"light": "flare", **A},
                {"hide": "girl", "dur": 0.5},
                {"show": "c1", "dur": 0.2, **A},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "Some historians think they were lost Flemish children, sick from hunger.|Algunos historiadores creen que eran niños flamencos perdidos, enfermos de hambre.|"
                  "Manche Historiker glauben, es waren verirrte flämische Kinder, krank vor Hunger.|Certains historiens pensent à des enfants flamands perdus, malades de faim.|"
                  "Alcuni storici pensano a bambini fiamminghi perduti, malati di fame.|Alguns historiadores acham que eram crianças flamengas perdidas, doentes de fome.", **A),
                {"sfx": "whoosh", **A},
                S("narr", "But no one has ever found St Martin's Land on any map.|Pero nadie ha encontrado jamás la Tierra de San Martín en un mapa.|"
                  "Doch niemand hat Sankt-Martins-Land je auf einer Karte gefunden.|Mais personne n'a jamais trouvé la Terre de Saint-Martin sur une carte.|"
                  "Ma nessuno ha mai trovato la Terra di San Martino su una mappa.|Mas ninguém jamais achou a Terra de São Martinho num mapa."),
                {"act": "odo", "do": "scared"},
                S("odo", "And the girl? Did she ever go back home?|¿Y la niña? ¿Volvió alguna vez a casa?|"
                  "Und das Mädchen? Ging sie je nach Hause zurück?|Et la fille ? Est-elle rentrée chez elle ?|"
                  "E la bambina? Tornò mai a casa?|E a menina? Ela voltou para casa algum dia?"),
                {"light": "dim"},
                S("moth", "Never. They say she grew up, married, and stayed. But she never forgot the bells.|Nunca. Dicen que creció, se casó y se quedó. Pero no olvidó las campanas.|"
                  "Nie. Sie wuchs auf, heiratete und blieb. Doch die Glocken vergaß sie nie.|Jamais. On dit qu'elle grandit, se maria et resta. Sans oublier les cloches.|"
                  "Mai. Dicono che crebbe, si sposò e rimase. Ma non dimenticò le campane.|Nunca. Dizem que cresceu, casou e ficou. Mas nunca esqueceu os sinos."),
                {"sfx": "bell", **A},
            ],
            "tail": 0.3,
        },
        {   # 7 cliffhanger: bells ring under the ground at the pit
            "bg": "forest", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": MOON,
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": KID(1420, 11, 0.66), "g2": KID(1300, 10)},
            "beats": [
                S("narr", "Today the green children are painted on the Woolpit village sign.|Hoy los niños verdes están pintados en el letrero de Woolpit.|"
                  "Heute sind die grünen Kinder auf dem Ortsschild von Woolpit gemalt.|Aujourd'hui, les enfants verts sont peints sur le panneau de Woolpit.|"
                  "Oggi i bambini verdi sono dipinti sull'insegna di Woolpit.|Hoje as crianças verdes estão pintadas na placa de Woolpit."),
                {"sfx": "whoosh", **A},
                S("narr", "And no one knows where they really came from.|Y nadie sabe de dónde vinieron realmente.|"
                  "Und niemand weiß, woher sie wirklich kamen.|Et personne ne sait d'où ils venaient vraiment.|"
                  "E nessuno sa da dove venissero davvero.|E ninguém sabe de onde vieram de verdade."),
                {"sfx": "bell", "wait": 0.3},
                S("odo", "Mothwick... do you hear that? Bells. Under the ground.|Mothwick... ¿oyes eso? Campanas. Bajo tierra.|"
                  "Mothwick... hörst du das? Glocken. Unter der Erde.|Mothwick... tu entends ? Des cloches. Sous la terre.|"
                  "Mothwick... senti? Campane. Sottoterra.|Mothwick... está ouvindo? Sinos. Debaixo da terra."),
                {"eyes": "open", **A},
                {"sfx": "bell", "wait": 0.3},
                {"flash": True, "dur": 1.0},
                {"eyes": "close"},
                {"act": "odo", "do": "turn"},
                S("moth", "Don't follow them, Odo. The last children who did never went home.|No las sigas, Odo. Los últimos niños que lo hicieron nunca volvieron.|"
                  "Folge ihnen nicht, Odo. Die letzten Kinder, die es taten, kamen nie heim.|Ne les suis pas, Odo. Les derniers enfants qui l'ont fait ne sont jamais rentrés.|"
                  "Non seguirle, Odo. Gli ultimi bambini che lo fecero non tornarono mai.|Não siga, Odo. As últimas crianças que seguiram nunca voltaram."),
                {"sfx": "step", "wait": 0.4},
                {"show": "g2", "dur": 0.3},
                {"show": "g1", "dur": 0.3, **A},
                {"move": "g1", "to": 1250, "speed": "creep", **A},
                {"growl": "g2"},
                {"lunge": "g2", "to": 1100},
                {"light": "out", **A},
                {"card": "WHAT RINGS BELOW?", "dur": 2.4},
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


# Short: hard cuts + flashes -> something new every 2-4 s; one scare; the last shot repeats shot 1's set-up
# (same bg/seed/positions, hook beat) so the final frame loops back to frame 1.
short1 = {   # the rule / scariest true detail
    "id": "ep012_short1", "format": "short",
    "title": "Who Rang the Bells Under Woolpit? #shorts",
    "hook": "DON'T FOLLOW THE BELLS",
    "description": "Woolpit, England, 12th century: two green-skinned children appeared by a wolf pit, speaking a language no one knew. The girl later said they had followed the sound of bells through a cave from a land where the sun never shone. Full true story on the channel. #shorts #woolpit #greenchildren #folklore #truestory #hollowmere",
    "tags": ["shorts"] + TAGS[:10],
    "thumbnail": {"bg": "forest", "seed": 4, "creature": "ghost", "text": "DON'T FOLLOW"},
    "shots": [
        SHOT("forest", 4, [
            {"show": "girl", "dur": 0.05}, {"flash": True, **A}, {"shake": 0.4, "power": 14, **A},
            {"sfx": "bell", **A},
            {"move": "girl", "to": 740, "speed": "creep", **A},
            S("narr", L("England, 800 years ago. Two green children climb out of a pit.", "Inglaterra, hace 800 años. Dos niños verdes salen de un foso.",
                        "England, vor 800 Jahren. Zwei grüne Kinder steigen aus einer Grube.", "Angleterre, il y a 800 ans. Deux enfants verts sortent d'une fosse.",
                        "Inghilterra, 800 anni fa. Due bambini verdi escono da una fossa.", "Inglaterra, 800 anos atrás. Duas crianças verdes saem de um poço."), **A),
        ], odo=560, amb=0.52, lights=MOON, creatures={"girl": KID(800, 11, 0.7)}),
        SHOT("village", 2, [
            {"show": "boy", "dur": 0.2}, {"flash": True, **A},
            S("narr", L("No one understands their words. They eat only raw beans.", "Nadie entiende su idioma. Solo comen habas crudas.",
                        "Niemand versteht sie. Sie essen nur rohe Bohnen.", "Personne ne les comprend. Ils ne mangent que des fèves crues.",
                        "Nessuno li capisce. Mangiano solo fave crude.", "Ninguém entende a língua deles. Só comem favas cruas."), **A),
            {"shake": 0.6, "power": 12, **A},
            {"sfx": "whisper"},
        ], odo=420, eyes=2, lights=MOON, creatures={"boy": KID(640, 10, 0.7)}),
        SHOT("forest", 2, [
            {"act": "odo", "do": "scared"},
            S("narr", L("The girl said: we followed the sound of bells... into the dark.", "La niña dijo: seguimos el sonido de campanas... hacia la oscuridad.",
                        "Das Mädchen sagte: Wir folgten den Glocken... ins Dunkel.", "La fille dit : on a suivi le son des cloches... dans le noir.",
                        "La bambina disse: seguimmo le campane... nel buio.", "A menina disse: seguimos o som dos sinos... no escuro."), **A),
            {"sfx": "bell", **A},
            {"light": "out"},
            {"show": "g1", "dur": 0.1, **A},
            {"lunge": "g1", "to": 740, **A},
            {"flash": True, "and": True},
        ], odo=560, lights=[{"kind": "fire", "x": 900, "y": 900, "r": 600}], creatures={"g1": KID(880, 10, 0.75)}),
        SHOT("forest", 4, [
            {"move": "odo", "to": 560, "speed": "walk"},
            S("narr", L("So if you hear bells under the ground tonight...", "Así que si esta noche oyes campanas bajo tierra...",
                        "Wenn du heute Nacht Glocken unter der Erde hörst...", "Alors si tu entends des cloches sous terre ce soir...",
                        "Quindi se stanotte senti campane sottoterra...", "Então, se ouvir sinos debaixo da terra esta noite..."), **A),
            {"show": "girl", "dur": 0.05}, {"flash": True, **A},
        ], odo=640, amb=0.52, lights=MOON, tail=0.0, creatures={"girl": KID(800, 11, 0.7)}),
    ],
}
short1["shots"][0]["focus"] = ["odo", "girl"]
short1["shots"][1]["focus"] = ["odo", "boy"]
short1["shots"][2]["cam"] = {"x": 700}
short1["shots"][3]["focus"] = ["odo", "girl"]

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

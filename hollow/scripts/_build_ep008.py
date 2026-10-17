"""Builds Hollowmere EP8 (recorded legend: Black Shuck, the black dog of Bungay and Blythburgh, Suffolk, Sunday 4 August 1577;
told in Abraham Fleming's pamphlet 'A Straunge and Terrible Wunder', 1577).
Run: python3 scripts/_build_ep008.py
Retention rules (2026-10-16): frame 1 = motion + big text hook (no fade, no title card), narration from 0 s mid-tension,
something new every 4-6 s, long ends on a cliffhanger, Shorts 15-25 s with one scare and a loop back to the first frame.
Harm in the 1577 account is kept vague ("people were hurt") per true_stories.md rule 4 (no injuries/deaths described)."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Black Shuck", "black dog legend", "Bungay", "Blythburgh",
        "Suffolk", "1577", "English folklore", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Black_Shuck",
           "https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/A00943/A00943.html?sequence=5",
           "https://www.suffolklive.com/news/history/black-shuck-blythburgh-church-suffolk-5767807",
           "https://onlinelibrary.wiley.com/doi/full/10.1111/1467-9809.13099"]

long_ = {
    "id": "ep008_long", "format": "long",
    "title": "What Burst Through the Church Door in 1577?",
    "hook": "DON'T OPEN THE DOOR", "hook_dur": 4.5,
    "description": ("Based on a real 1577 record and a famous English legend. On Sunday 4 August 1577, a violent storm of rain, "
                    "lightning and thunder hit Bungay in Suffolk, England. In a pamphlet printed that year, Abraham Fleming wrote that "
                    "while people prayed in St Mary's Church, a black dog appeared among them with flashes of fire and ran down the church. "
                    "The same day, the story says, it burst into Holy Trinity Church at Blythburgh, where the spire fell through the roof. "
                    "The north door there still has dark scorch marks that locals call 'the Devil's fingerprints'. Historians point to a fierce "
                    "lightning storm and to Fleming's habit of turning news into sermons; sceptics say the marks were made by candles. "
                    "The legend of Black Shuck has never left East Anglia.\n\n"
                    "Sources:\n" + "\n".join(SOURCES[:3]) + "\n\n#truestory #blackshuck #suffolk #legend #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 8", "devil's fingerprints", "hellhound", "A Straunge and Terrible Wunder"],
    "thumbnail": {"bg": "chapel", "seed": 3, "creature": "gloamhound", "text": "DON'T OPEN IT"},
    "shots": [
        {   # 1 cold open: storm, the door bangs, motion + hook text from frame 1
            "bg": "chapel", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 4, "lantern": 1.0, "ambient": 0.38, "fade": False,
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 0.9}},
            "beats": [
                {"move": "odo", "to": 620, "speed": "creep"},
                {"move": "moth", "to": 760, "speed": "creep", "and": True},
                S("narr", "Thunder shook the church... and then the doors flew open.|Un trueno sacudió la iglesia... y las puertas se abrieron de golpe.|"
                  "Donner erschütterte die Kirche... und dann flogen die Türen auf.|Le tonnerre secoua l'église... puis les portes s'ouvrirent d'un coup.|"
                  "Il tuono scosse la chiesa... e poi le porte si spalancarono.|O trovão sacudiu a igreja... e então as portas se escancararam.", **{"and": True}),
                {"flash": True, "dur": 1.2, "and": True},
                {"sfx": "creak", "wait": 0.2},
                {"flash": True, "dur": 1.2},
                {"show": "h1", "dur": 0.3},
                {"growl": "h1", "and": True},
                {"act": "odo", "do": "scared"},
                S("narr", "This is a real English legend, first printed in 1577.|Esta es una leyenda inglesa real, impresa por primera vez en 1577.|"
                  "Dies ist eine echte englische Legende, zuerst gedruckt im Jahr 1577.|Ceci est une vraie légende anglaise, imprimée pour la première fois en 1577.|"
                  "Questa è una vera leggenda inglese, stampata per la prima volta nel 1577.|Esta é uma lenda inglesa real, impressa pela primeira vez em 1577."),
                {"hide": "h1", "dur": 0.4, "and": True},
                S("odo", "Mothwick... something black just ran past the door.|Mothwick... algo negro acaba de pasar junto a la puerta.|"
                  "Mothwick... gerade ist etwas Schwarzes an der Tür vorbeigerannt.|Mothwick... quelque chose de noir vient de passer devant la porte.|"
                  "Mothwick... qualcosa di nero è appena passato davanti alla porta.|Mothwick... algo preto acabou de passar pela porta."),
                {"eyes": "open", "and": True},
                S("moth", "Then whatever you hear tonight... don't open the door.|Entonces, oigas lo que oigas esta noche... no abras la puerta.|"
                  "Dann, was du heute Nacht auch hörst... öffne nicht die Tür.|Alors, quoi que tu entendes ce soir... n'ouvre pas la porte.|"
                  "Allora, qualunque cosa senti stanotte... non aprire la porta.|Então, ouça o que ouvir esta noite... não abra a porta."),
                {"sfx": "sting", "and": True},
            ],
            "tail": 0.2,
        },
        {   # 2 who is Black Shuck
            "bg": "forest", "seed": 7, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1450, "state": "hidden", "face": -1, "scale": 0.8},
                          "c1": {"type": "crow", "x": 1250, "y": 330, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "In East Anglia, in eastern England, people tell of a huge black dog.|En East Anglia, al este de Inglaterra, hablan de un enorme perro negro.|"
                  "In East Anglia, im Osten Englands, erzählt man von einem riesigen schwarzen Hund.|En East Anglia, à l'est de l'Angleterre, on parle d'un énorme chien noir.|"
                  "Nell'East Anglia, nell'est dell'Inghilterra, si parla di un enorme cane nero.|Em East Anglia, no leste da Inglaterra, falam de um enorme cão preto."),
                {"sfx": "howl", "and": True},
                {"flash": True, "dur": 1.2},
                {"show": "h1", "dur": 1.0},
                S("narr", "They call him Black Shuck. Some say the name meant demon.|Lo llaman Black Shuck. Algunos dicen que el nombre significaba demonio.|"
                  "Man nennt ihn Black Shuck. Manche sagen, der Name bedeutete Dämon.|On l'appelle Black Shuck. Certains disent que ce nom voulait dire démon.|"
                  "Lo chiamano Black Shuck. Alcuni dicono che il nome significasse demonio.|Chamam-no de Black Shuck. Dizem que o nome significava demônio."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", "and": True},
                S("narr", "The stories say he walks the coast roads and the churchyards at night.|Las historias dicen que recorre los caminos de la costa y los cementerios de noche.|"
                  "Es heißt, er streift nachts über Küstenwege und Friedhöfe.|On dit qu'il rôde la nuit sur les routes côtières et dans les cimetières.|"
                  "Si dice che di notte vaghi per le strade della costa e i cimiteri.|Dizem que ele anda à noite pelas estradas da costa e pelos cemitérios."),
                {"hide": "c1", "dur": 0.4},
                {"act": "odo", "do": "shake"},
                S("odo", "A dog as big as a calf... with eyes like fire?|¿Un perro grande como un ternero... con ojos de fuego?|"
                  "Ein Hund so groß wie ein Kalb... mit Augen wie Feuer?|Un chien grand comme un veau... aux yeux de feu ?|"
                  "Un cane grande come un vitello... con gli occhi di fuoco?|Um cão do tamanho de um bezerro... com olhos de fogo?"),
                {"flash": True, "dur": 1.2},
                {"growl": "h1", "and": True},
                S("moth", "That's the legend. But one night, people wrote it down.|Esa es la leyenda. Pero una noche, alguien lo escribió.|"
                  "Das ist die Legende. Aber eines Nachts schrieb man es auf.|Ça, c'est la légende. Mais une nuit, on l'a écrit.|"
                  "Questa è la leggenda. Ma una notte, qualcuno lo scrisse.|Essa é a lenda. Mas uma noite, alguém escreveu tudo."),
                {"hide": "h1", "dur": 0.8, "and": True},
            ],
            "tail": 0.3,
        },
        {   # 3 Bungay, Sunday 4 August 1577, the storm
            "bg": "village", "seed": 4, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "creatures": {"man": {"type": "figure", "x": 1420, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "Sunday, the 4th of August, 1577. The town of Bungay, in Suffolk.|Domingo, 4 de agosto de 1577. El pueblo de Bungay, en Suffolk.|"
                  "Sonntag, der 4. August 1577. Die Stadt Bungay in Suffolk.|Dimanche 4 août 1577. La ville de Bungay, dans le Suffolk.|"
                  "Domenica 4 agosto 1577. La cittadina di Bungay, nel Suffolk.|Domingo, 4 de agosto de 1577. A cidade de Bungay, em Suffolk."),
                {"sfx": "bell", "and": True},
                {"show": "man", "dur": 1.0},
                S("narr", "People gathered in St Mary's Church for the morning prayers.|La gente se reunió en la iglesia de Santa María para rezar.|"
                  "Die Leute versammelten sich zum Gebet in der Kirche St. Mary.|Les gens s'étaient réunis pour prier dans l'église Sainte-Marie.|"
                  "La gente si riunì nella chiesa di Santa Maria per pregare.|As pessoas se reuniram na igreja de Santa Maria para rezar."),
                {"flash": True, "dur": 1.2},
                S("narr", "Then a storm broke. Rain, lightning, thunder, like few had ever seen.|Entonces estalló una tormenta. Lluvia, rayos, truenos, como pocos habían visto.|"
                  "Dann brach ein Sturm los. Regen, Blitz, Donner, wie kaum je gesehen.|Puis l'orage éclata. Pluie, éclairs, tonnerre, comme rarement vu.|"
                  "Poi scoppiò una tempesta. Pioggia, fulmini, tuoni, come pochi ne avevano visti.|Então caiu uma tempestade. Chuva, raios, trovões, como poucos já viram."),
                {"shake": 0.8, "power": 14, "and": True},
                {"light": "dim"},
                {"act": "odo", "do": "jump"},
                S("narr", "The church went so dark, the record says, people could barely see.|La iglesia se oscureció tanto, dice el relato, que apenas se veía.|"
                  "Die Kirche wurde so dunkel, heißt es, dass man kaum etwas sah.|L'église devint si sombre, dit le récit, qu'on n'y voyait presque rien.|"
                  "La chiesa divenne così buia, dice il racconto, che quasi non si vedeva.|A igreja ficou tão escura, diz o relato, que mal se enxergava."),
                {"flash": True, "dur": 1.2},
                {"hide": "man", "dur": 0.8},
                S("odo", "In the dark... I hear claws on the stone floor.|En la oscuridad... oigo garras en el suelo de piedra.|"
                  "Im Dunkeln... höre ich Krallen auf dem Steinboden.|Dans le noir... j'entends des griffes sur les dalles.|"
                  "Nel buio... sento artigli sul pavimento di pietra.|No escuro... ouço garras no chão de pedra."),
                {"sfx": "step", "and": True},
                {"light": "on"},
            ],
            "tail": 0.3,
        },
        {   # 4 the black dog in St Mary's (Fleming's pamphlet)
            "bg": "chapel", "seed": 5, "music": "heartbeat", "wind": True, "eyes": 3, "ambient": 0.34,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 1.0}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", "and": True},
                S("narr", "A writer named Abraham Fleming printed what people told of that day.|Un escritor, Abraham Fleming, publicó lo que la gente contó de aquel día.|"
                  "Ein Schreiber namens Abraham Fleming druckte, was man von jenem Tag erzählte.|Un auteur, Abraham Fleming, imprima ce qu'on racontait de ce jour-là.|"
                  "Uno scrittore, Abraham Fleming, stampò ciò che si raccontava di quel giorno.|Um escritor, Abraham Fleming, publicou o que contavam daquele dia.", **{"and": True}),
                {"flash": True, "dur": 1.2},
                {"show": "h1", "dur": 0.3, "and": True},
                S("narr", "In the flashes of fire, a black dog appeared among the people.|Entre destellos de fuego, un perro negro apareció entre la gente.|"
                  "Im Feuerschein erschien ein schwarzer Hund mitten unter den Leuten.|Dans des éclairs de feu, un chien noir apparut parmi les gens.|"
                  "Tra lampi di fuoco, un cane nero apparve in mezzo alla gente.|Entre clarões de fogo, um cão preto apareceu no meio do povo."),
                {"growl": "h1"},
                {"eyes": "open", "and": True},
                S("narr", "It ran down the church with great swiftness, he wrote.|Corrió por la iglesia a gran velocidad, escribió él.|"
                  "Es rannte mit großer Schnelligkeit durch die Kirche, schrieb er.|Il traversa l'église à toute vitesse, écrivit-il.|"
                  "Corse lungo la chiesa a grande velocità, scrisse.|Correu pela igreja com grande rapidez, escreveu ele."),
                {"lunge": "h1", "to": 1250},
                S("narr", "Fleming says people were hurt that day. He blamed the devil himself.|Fleming dice que hubo heridos ese día. Culpó al mismo diablo.|"
                  "Fleming sagt, an jenem Tag wurden Menschen verletzt. Er gab dem Teufel die Schuld.|Fleming dit que des gens furent blessés. Il accusa le diable en personne.|"
                  "Fleming dice che quel giorno ci furono feriti. Diede la colpa al diavolo.|Fleming diz que houve feridos naquele dia. Culpou o próprio diabo."),
                {"hide": "h1", "dur": 0.2},
                {"light": "flare", "and": True},
                S("odo", "And then... where did it go?|Y luego... ¿adónde fue?|Und dann... wohin ist er verschwunden?|"
                  "Et ensuite... où est-il allé ?|E poi... dove è andato?|E depois... para onde ele foi?"),
                {"eyes": "close"},
                {"move": "odo", "to": "off_right", "speed": "run"},
                {"move": "moth", "to": "off_right", "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 5 Blythburgh: the spire falls, the scorched north door
            "bg": "chapel", "seed": 8, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.38,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 0.9},
                          "c1": {"type": "crow", "x": 1200, "y": 300, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "The story says that the same morning, it reached Blythburgh, miles away.|La historia dice que esa misma mañana llegó a Blythburgh, a millas de allí.|"
                  "Es heißt, am selben Morgen erreichte er Blythburgh, meilenweit entfernt.|On dit que le même matin, il atteignit Blythburgh, à des lieues de là.|"
                  "Si dice che la stessa mattina arrivò a Blythburgh, a miglia di distanza.|Dizem que na mesma manhã ele chegou a Blythburgh, a quilômetros dali."),
                {"sfx": "whoosh", "and": True},
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", "and": True},
                S("narr", "It burst into Holy Trinity Church with a clap of thunder.|Irrumpió en la iglesia de la Santísima Trinidad con un trueno.|"
                  "Mit einem Donnerschlag brach er in die Kirche Holy Trinity ein.|Il fit irruption dans l'église de la Trinité dans un coup de tonnerre.|"
                  "Irruppe nella chiesa della Santissima Trinità con un tuono.|Ele invadiu a igreja da Santíssima Trindade com um trovão."),
                {"hide": "c1", "dur": 0.3},
                {"flash": True, "dur": 1.2, "and": True},
                {"shake": 1.0, "power": 18},
                S("narr", "The church spire came crashing down through the roof.|La aguja de la iglesia se desplomó atravesando el tejado.|"
                  "Die Turmspitze krachte durch das Dach der Kirche.|La flèche de l'église s'effondra à travers le toit.|"
                  "La guglia della chiesa crollò attraverso il tetto.|A torre da igreja desabou atravessando o telhado."),
                {"sfx": "thump", "and": True},
                {"act": "odo", "do": "hide"},
                {"show": "h1", "dur": 0.4},
                S("narr", "And as it left by the north door, it left marks... burned into the wood.|Y al salir por la puerta norte, dejó marcas... quemadas en la madera.|"
                  "Und als er durch die Nordtür ging, hinterließ er Spuren... ins Holz gebrannt.|Et en sortant par la porte nord, il laissa des marques... brûlées dans le bois.|"
                  "E uscendo dalla porta nord, lasciò dei segni... bruciati nel legno.|E ao sair pela porta norte, deixou marcas... queimadas na madeira."),
                {"hide": "h1", "dur": 0.6},
                {"act": "odo", "do": "unhide"},
                S("odo", "Mothwick... the marks are still here. Look at the door.|Mothwick... las marcas siguen aquí. Mira la puerta.|"
                  "Mothwick... die Spuren sind noch da. Sieh dir die Tür an.|Mothwick... les marques sont encore là. Regarde la porte.|"
                  "Mothwick... i segni ci sono ancora. Guarda la porta.|Mothwick... as marcas ainda estão aqui. Olhe a porta."),
                S("moth", "People call them the Devil's fingerprints. You can see them today.|Las llaman las huellas del diablo. Aún hoy se pueden ver.|"
                  "Man nennt sie die Fingerabdrücke des Teufels. Man sieht sie noch heute.|On les appelle les empreintes du diable. On les voit encore aujourd'hui.|"
                  "Le chiamano le impronte del diavolo. Si vedono ancora oggi.|Chamam de impressões digitais do diabo. Dá para vê-las até hoje."),
                {"sfx": "sting", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 6 the explanations
            "bg": "village", "seed": 2, "music": "lullaby", "wind": True, "eyes": 2, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1200, "y": 600, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "Historians say a fierce lightning storm really did strike that day.|Los historiadores dicen que ese día sí cayó una feroz tormenta eléctrica.|"
                  "Historiker sagen, an jenem Tag tobte wirklich ein heftiges Gewitter.|Les historiens disent qu'un violent orage a vraiment frappé ce jour-là.|"
                  "Gli storici dicono che quel giorno colpì davvero un violento temporale.|Historiadores dizem que uma forte tempestade de raios caiu mesmo naquele dia."),
                {"flash": True, "dur": 1.2, "and": True},
                S("narr", "Lightning can start fires and bring down a spire.|Un rayo puede provocar incendios y derribar una torre.|"
                  "Ein Blitz kann Feuer legen und eine Turmspitze stürzen.|La foudre peut allumer des feux et abattre une flèche.|"
                  "Un fulmine può appiccare fuochi e abbattere una guglia.|Um raio pode causar incêndios e derrubar uma torre."),
                {"act": "odo", "do": "calm"},
                S("narr", "Sceptics say the marks on the door were made by candles.|Los escépticos dicen que las marcas las hicieron velas.|"
                  "Skeptiker sagen, die Spuren an der Tür stammen von Kerzen.|Les sceptiques disent que les marques viennent de bougies.|"
                  "Gli scettici dicono che i segni sulla porta li fecero le candele.|Os céticos dizem que as marcas na porta foram feitas por velas."),
                {"sfx": "snap", "and": True},
                S("narr", "But to this day, Bungay's town sign shows a black dog on a bolt of lightning.|Pero aún hoy, el escudo de Bungay muestra un perro negro sobre un rayo.|"
                  "Doch bis heute zeigt Bungays Stadtzeichen einen schwarzen Hund auf einem Blitz.|Mais aujourd'hui encore, l'emblème de Bungay montre un chien noir sur un éclair.|"
                  "Ma ancora oggi lo stemma di Bungay mostra un cane nero su un fulmine.|Mas até hoje o brasão de Bungay mostra um cão preto sobre um raio."),
                {"light": "out"},
                {"show": "g1", "dur": 0.3, "and": True},
                {"sfx": "whisper", "and": True},
                S("odo", "Mothwick... the lantern went out. Something is breathing behind me.|Mothwick... la linterna se apagó. Algo respira detrás de mí.|"
                  "Mothwick... die Laterne ist aus. Hinter mir atmet etwas.|Mothwick... la lanterne s'est éteinte. Quelque chose respire derrière moi.|"
                  "Mothwick... la lanterna si è spenta. Qualcosa respira dietro di me.|Mothwick... a lanterna apagou. Tem algo respirando atrás de mim."),
                {"sfx": "growl", "wait": 0.3},
                {"flash": True, "dur": 1.2},
                {"hide": "g1", "dur": 0.2, "and": True},
                {"light": "flare"},
                S("moth", "Only the wind. Keep walking. And don't turn around.|Solo el viento. Sigue andando. Y no te des la vuelta.|"
                  "Nur der Wind. Geh weiter. Und dreh dich nicht um.|Juste le vent. Continue. Et ne te retourne pas.|"
                  "Solo il vento. Continua. E non voltarti.|Só o vento. Continue andando. E não se vire."),
                {"eyes": "close"},
            ],
            "tail": 0.3,
        },
        {   # 7 the coast road: cliffhanger
            "bg": "forest", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"h1": {"type": "gloamhound", "x": 1520, "state": "hidden", "face": -1, "scale": 1.05},
                          "c1": {"type": "crow", "x": 1300, "y": 320, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "The storm passed. But the black dog never left the stories.|La tormenta pasó. Pero el perro negro nunca dejó las historias.|"
                  "Der Sturm zog vorbei. Doch der schwarze Hund verließ die Geschichten nie.|L'orage passa. Mais le chien noir ne quitta jamais les récits.|"
                  "La tempesta passò. Ma il cane nero non lasciò mai i racconti.|A tempestade passou. Mas o cão preto nunca saiu das histórias."),
                {"sfx": "whoosh", "and": True},
                S("narr", "People on the coast roads still say they hear paws behind them at night.|En los caminos de la costa aún dicen oír patas detrás de noche.|"
                  "An den Küstenwegen hört man nachts noch Pfoten hinter sich, sagen die Leute.|Sur les routes côtières, on dit encore entendre des pattes derrière soi la nuit.|"
                  "Sulle strade della costa dicono ancora di sentire zampe dietro di sé di notte.|Nas estradas da costa ainda dizem ouvir patas atrás de si à noite."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", "and": True},
                {"hide": "c1", "dur": 0.4},
                {"sfx": "step", "wait": 0.3},
                {"act": "odo", "do": "turn"},
                S("odo", "Mothwick... there are paw prints in the mud. Big ones. Still warm.|Mothwick... hay huellas de patas en el barro. Grandes. Aún tibias.|"
                  "Mothwick... da sind Pfotenspuren im Schlamm. Riesige. Noch warm.|Mothwick... il y a des traces de pattes dans la boue. Énormes. Encore tièdes.|"
                  "Mothwick... ci sono impronte di zampe nel fango. Grandi. Ancora calde.|Mothwick... tem pegadas de patas na lama. Enormes. Ainda quentes."),
                {"sfx": "step", "wait": 0.4},
                S("moth", "They don't lead away, Odo... they circle us.|No se alejan, Odo... nos rodean.|Sie führen nicht weg, Odo... sie kreisen um uns.|"
                  "Elles ne s'éloignent pas, Odo... elles tournent autour de nous.|Non si allontanano, Odo... ci girano intorno.|Elas não vão embora, Odo... elas nos cercam."),
                {"show": "h1", "dur": 0.3},
                {"growl": "h1", "and": True},
                {"lunge": "h1", "to": 1150},
                {"light": "out", "and": True},
                {"card": "WHAT WALKS THE COAST ROAD?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}

def L(*parts):
    return "|".join(parts)


def SHOT(bg, seed, beats, odo=700, amb=0.48, eyes=0, lights=None, creatures=None, tail=0.05):
    sh = {"bg": bg, "seed": seed, "music": "heartbeat", "wind": True, "eyes": eyes, "ambient": amb, "focus": "odo", "fade": False,
          "chars": {"odo": {"x": odo}}, "creatures": creatures or {}, "beats": beats, "tail": tail}
    if lights:
        sh["lights"] = lights
    return sh


MOON = [{"kind": "moon", "x": 900, "y": 300, "r": 900}]
WIN = [{"kind": "window", "x": 900, "y": 640, "r": 520}]
DOG = lambda x=1150: {"h1": {"type": "gloamhound", "x": x, "state": "hidden", "face": -1, "scale": 0.9}}

# Shorts: several hard-cut shots (no fades) + lightning flashes -> a new thing every 2-4 s;
# the last shot repeats the first shot's set-up so the final frame loops back to frame 1.
short1 = {   # the rule / scariest true detail
    "id": "ep008_short1", "format": "short",
    "title": "Who burned these marks on the door? 🔥 #shorts",
    "hook": "DON'T OPEN THE DOOR",
    "description": "Suffolk, England, 4 August 1577: a storm, a black dog in the church, and burn marks on the north door that you can still see today. A real English legend. Full story on the channel. #shorts #blackshuck #truestory #legend #hollowmere",
    "tags": ["shorts"] + TAGS[:9],
    "thumbnail": {"bg": "chapel", "seed": 3, "creature": "gloamhound", "text": "DON'T OPEN IT"},
    "shots": [
        SHOT("chapel", 3, [
            {"wait": 0.5}, {"flash": True}, {"shake": 0.4, "power": 16, "and": True},
            {"move": "odo", "to": 760, "speed": "creep", "and": True},
            S("narr", L("1577. A storm.", "1577. Una tormenta.", "1577. Ein Sturm.", "1577. Un orage.", "1577. Una tempesta.", "1577. Uma tempestade."), **{"and": True}),
            {"sfx": "thump"},
        ], amb=0.55, lights=MOON),
        SHOT("village", 4, [
            {"act": "odo", "do": "jump"},
            S("narr", L("The church doors burst open.", "Las puertas de la iglesia se abren de golpe.", "Die Kirchentüren fliegen auf.",
                        "Les portes de l'église s'ouvrent d'un coup.", "Le porte della chiesa si spalancano.", "As portas da igreja se escancaram."), **{"and": True}),
            {"sfx": "creak", "and": True},
            {"flash": True},
        ], odo=560, lights=WIN),
        SHOT("chapel", 5, [
            {"show": "h1", "dur": 0.3},
            S("narr", L("A black dog ran through, the old record says.", "Un perro negro la atravesó, dice el viejo relato.",
                        "Ein schwarzer Hund rannte hindurch, sagt der alte Bericht.", "Un chien noir la traversa, dit le vieux récit.",
                        "Un cane nero la attraversò, dice l'antico racconto.", "Um cão preto passou correndo, diz o velho relato."), **{"and": True}),
            {"growl": "h1", "and": True},
            {"lunge": "h1", "to": 950},
            {"flash": True, "and": True},
        ], odo=520, eyes=3, creatures=DOG(1250)),
        SHOT("chapel", 8, [
            {"act": "odo", "do": "scared"},
            S("narr", L("It left burn marks on the door. They are still there.", "Dejó marcas quemadas en la puerta. Siguen ahí.",
                        "Es hinterließ Brandspuren an der Tür. Sie sind noch da.", "Il laissa des brûlures sur la porte. Elles y sont encore.",
                        "Lasciò bruciature sulla porta. Ci sono ancora.", "Deixou marcas de queimado na porta. Ainda estão lá."), **{"and": True}),
            {"move": "odo", "to": 640, "speed": "creep", "and": True},
            {"light": "out"},
            {"show": "h1", "dur": 0.1, "and": True},
            {"flash": True, "and": True},
            {"growl": "h1"},
        ], odo=760, lights=MOON, creatures=DOG(1100)),
        SHOT("chapel", 3, [
            {"move": "odo", "to": 700, "speed": "walk"},
            S("narr", L("So if you hear thunder tonight...", "Así que si oyes truenos esta noche...", "Wenn du heute Nacht Donner hörst...",
                        "Alors si tu entends le tonnerre ce soir...", "Quindi se senti tuonare stanotte...", "Então, se ouvir trovões esta noite..."), **{"and": True}),
        ], odo=820, amb=0.55, lights=MOON, tail=0.2),
    ],
}

short2 = {   # Would YOU...?
    "id": "ep008_short2", "format": "short",
    "title": "Would YOU open the church door? ⛈️ #shorts",
    "hook": "WOULD YOU OPEN IT?",
    "description": "Bungay, Suffolk, 1577: in a wild storm, people said a huge black dog ran through the church. The legend of Black Shuck lives on. Would you open the door? Full story on the channel. #shorts #blackshuck #truestory #legend #hollowmere",
    "tags": ["shorts"] + TAGS[:9],
    "thumbnail": {"bg": "chapel", "seed": 5, "creature": "gloamhound", "text": "WOULD YOU?"},
    "shots": [
        SHOT("chapel", 5, [
            {"wait": 0.5}, {"flash": True}, {"shake": 0.4, "power": 16, "and": True},
            {"move": "odo", "to": 700, "speed": "creep", "and": True},
            S("narr", L("Knock. Knock.", "Toc. Toc.", "Klopf. Klopf.", "Toc. Toc.", "Toc. Toc.", "Toc. Toc."), **{"and": True}),
            {"sfx": "thump", "and": True},
            {"sfx": "thump", "wait": 0.3},
        ], odo=640, amb=0.55, lights=MOON),
        SHOT("village", 2, [
            {"act": "odo", "do": "shake"},
            S("narr", L("Something is at the church door.", "Hay algo en la puerta de la iglesia.", "Etwas ist an der Kirchentür.",
                        "Quelque chose est à la porte de l'église.", "C'è qualcosa alla porta della chiesa.", "Tem algo na porta da igreja."), **{"and": True}),
            {"sfx": "thump", "and": True},
            {"flash": True},
        ], odo=560, lights=WIN),
        SHOT("chapel", 8, [
            {"show": "h1", "dur": 0.3},
            S("narr", L("In 1577, people said a giant black dog came through it.", "En 1577 decían que un enorme perro negro entró por ella.",
                        "1577 sagte man, ein riesiger schwarzer Hund kam hindurch.", "En 1577, on disait qu'un chien noir géant l'avait franchie.",
                        "Nel 1577 si disse che un enorme cane nero entrò da lì.", "Em 1577 diziam que um cão preto gigante entrou por ela."), **{"and": True}),
            {"growl": "h1", "and": True},
            {"lunge": "h1", "to": 950},
            {"flash": True, "and": True},
        ], odo=520, eyes=3, lights=MOON, creatures=DOG(1250)),
        SHOT("forest", 7, [
            {"eyes": "open"},
            S("narr", L("Would you open it?", "¿La abrirías?", "Würdest du sie öffnen?", "L'ouvrirais-tu ?", "La apriresti?", "Você abriria?"), **{"and": True}),
            {"move": "odo", "to": 760, "speed": "creep", "and": True},
            {"light": "out"},
            {"show": "h1", "dur": 0.1, "and": True},
            {"flash": True, "and": True},
            {"growl": "h1"},
        ], odo=680, eyes=4, creatures=DOG(1100)),
        SHOT("chapel", 5, [
            {"move": "odo", "to": 640, "speed": "walk"},
            S("narr", L("Listen...", "Escucha...", "Hör zu...", "Écoute...", "Ascolta...", "Escute..."), **{"and": True}),
        ], odo=760, amb=0.55, lights=MOON, tail=0.3),
    ],
}

for s in (long_, short1, short2):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

"""Builds Hollowmere EP9 (true record + legend: the children of Hamelin, Lower Saxony, Germany, 26 June 1284;
the c.1300 church window (destroyed 1660), the Lueneburg manuscript c.1440-50, the rats added c.1559, Bungelosenstrasse).
Run: python3 scripts/_build_ep009.py
Retention rules (2026-10-16): frame 1 = motion + big text hook (no fade, no title card), narration from 0 s mid-tension,
something new every 4-6 s, long ends on a cliffhanger, Shorts 15-25 s with one scare and a loop back to the first frame.
Pack 2 of 2026-10-19 -> 1 long + 1 Short. The children are only 'never seen again' (true_stories.md rule 4); the
death theories are not dwelt on."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


A = {"and": True}
TAGS = ["true story", "unsolved mystery", "real horror story", "Pied Piper", "Hamelin", "Hameln", "1284",
        "Germany", "German legend", "lost children", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Pied_Piper_of_Hamelin",
           "https://www.mentalfloss.com/history/enduring-legacy-pied-piper-hamelin",
           "https://museumhameln.de/?p=1080"]

PIPER = lambda x=1450, sc=1.0: {"type": "figure", "x": x, "seed": 2, "face": -1, "state": "hidden", "scale": sc}
KID = lambda x, sd=0: {"type": "ghost", "x": x, "state": "hidden", "face": -1, "scale": 0.55}

long_ = {
    "id": "ep009_long", "format": "long",
    "title": "Where Did Hamelin's 130 Children Go?",
    "hook": "DON'T FOLLOW THE MUSIC", "hook_dur": 4.5,
    "description": ("Based on real records and a famous German legend. A note written into a manuscript at Lüneburg around 1440-50 says: "
                    "'In the year of 1284, on the day of Saints John and Paul, on June 26, by a piper clothed in many kinds of colours, "
                    "130 children born in Hamelin were seduced, and lost at the place of execution near the Koppen.' "
                    "The oldest known record was a stained-glass window placed in Hamelin's church around 1300; it was destroyed in 1660. "
                    "The rats were only added to the story around 1559. On Hamelin's Bungelosenstrasse, the street where the children were "
                    "last seen, music and dancing are still not allowed. Historians suggest the young people may have left to settle new "
                    "lands in the east, joined a pilgrimage, or were caught in a dancing mania — but no one knows.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #piedpiper #hamelin #legend #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 9", "Bungelosenstrasse", "Pied Piper of Hamelin", "true story behind the legend"],
    "thumbnail": {"bg": "village", "seed": 4, "creature": "figure", "text": "DON'T FOLLOW"},
    "shots": [
        {   # 1 cold open: the tune in the dark street, motion + hook from frame 1
            "bg": "village", "seed": 4, "music": "lullaby", "wind": True, "eyes": 3, "lantern": 1.0, "ambient": 0.38, "fade": False,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [900, 600, 1.22], "to": [1060, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"p": PIPER(1500), "k1": KID(1250), "k2": KID(1340)},
            "beats": [
                {"wait": 0.3},
                {"flash": True, "dur": 0.8},
                {"move": "odo", "to": 620, "speed": "creep", **A},
                {"move": "moth", "to": 760, "speed": "creep", **A},
                {"sfx": "whoosh", **A},
                S("narr", "A strange tune drifted down the street... and the children followed it.|Una extraña melodía bajó por la calle... y los niños la siguieron.|"
                  "Eine seltsame Melodie zog durch die Gasse... und die Kinder folgten ihr.|Un air étrange descendit la rue... et les enfants le suivirent.|"
                  "Una strana melodia scese per la strada... e i bambini la seguirono.|Uma melodia estranha desceu a rua... e as crianças a seguiram.", **A),
                {"shake": 0.5, "power": 10, **A},
                {"flash": True, "dur": 1.2},
                {"show": "p", "dur": 0.3, **A},
                {"show": "k1", "dur": 0.5, **A},
                {"show": "k2", "dur": 0.5, **A},
                {"sfx": "whisper", **A},
                {"act": "odo", "do": "scared"},
                S("narr", "This is a true record from Hamelin, Germany, written down long ago.|Este es un registro real de Hamelín, Alemania, escrito hace siglos.|"
                  "Dies ist eine echte Aufzeichnung aus Hameln, vor langer Zeit niedergeschrieben.|Ceci est un vrai récit de Hamelin, en Allemagne, écrit il y a longtemps.|"
                  "Questo è un vero documento di Hamelin, in Germania, scritto molto tempo fa.|Este é um registro real de Hamelin, na Alemanha, escrito há muito tempo."),
                {"move": "k1", "to": "off_right", "speed": "walk", **A},
                {"move": "k2", "to": "off_right", "speed": "walk", **A},
                {"hide": "p", "dur": 0.8},
                S("odo", "Mothwick... every bed in the village is empty.|Mothwick... todas las camas del pueblo están vacías.|"
                  "Mothwick... jedes Bett im Dorf ist leer.|Mothwick... tous les lits du village sont vides.|"
                  "Mothwick... tutti i letti del villaggio sono vuoti.|Mothwick... todas as camas da vila estão vazias."),
                {"eyes": "open", **A},
                S("moth", "Then whatever you hear tonight... don't follow the music.|Entonces, oigas lo que oigas esta noche... no sigas la música.|"
                  "Dann, was du heute Nacht auch hörst... folge nicht der Musik.|Alors, quoi que tu entendes ce soir... ne suis pas la musique.|"
                  "Allora, qualunque cosa senti stanotte... non seguire la musica.|Então, ouça o que ouvir esta noite... não siga a música."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.2,
        },
        {   # 2 Hamelin, 26 June 1284
            "bg": "village", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"man": {"type": "figure", "x": 1420, "seed": 0, "face": -1, "state": "hidden"},
                          "c1": {"type": "crow", "x": 1250, "y": 330, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Hamelin is a small town on the River Weser, in northern Germany.|Hamelín es un pequeño pueblo junto al río Weser, en el norte de Alemania.|"
                  "Hameln ist eine kleine Stadt an der Weser, im Norden Deutschlands.|Hamelin est une petite ville sur la Weser, dans le nord de l'Allemagne.|"
                  "Hamelin è una cittadina sul fiume Weser, nel nord della Germania.|Hamelin é uma pequena cidade no rio Weser, no norte da Alemanha."),
                {"sfx": "bell", **A},
                {"show": "man", "dur": 1.0},
                S("narr", "The year is 1284. The 26th of June, the day of Saints John and Paul.|Es el año 1284. El 26 de junio, día de San Juan y San Pablo.|"
                  "Es ist das Jahr 1284. Der 26. Juni, der Tag von Johannes und Paul.|Nous sommes en 1284. Le 26 juin, jour des saints Jean et Paul.|"
                  "È l'anno 1284. Il 26 giugno, giorno dei santi Giovanni e Paolo.|É o ano de 1284. 26 de junho, dia de São João e São Paulo."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "On that day, the old records say, Hamelin lost its children.|Ese día, dicen los viejos registros, Hamelín perdió a sus niños.|"
                  "An jenem Tag, sagen die alten Aufzeichnungen, verlor Hameln seine Kinder.|Ce jour-là, disent les vieux récits, Hamelin perdit ses enfants.|"
                  "Quel giorno, dicono i vecchi documenti, Hamelin perse i suoi bambini.|Naquele dia, dizem os velhos registros, Hamelin perdeu suas crianças."),
                {"flash": True, "dur": 1.2, **A},
                {"hide": "man", "dur": 0.6},
                {"act": "odo", "do": "shake"},
                S("odo", "Lost them? How do you lose a whole town of children?|¿Perderlos? ¿Cómo se pierden los niños de todo un pueblo?|"
                  "Verloren? Wie verliert man die Kinder einer ganzen Stadt?|Perdus ? Comment perd-on les enfants de toute une ville ?|"
                  "Persi? Come si perdono i bambini di un'intera città?|Perdeu? Como se perdem as crianças de uma cidade inteira?"),
                {"sfx": "whoosh", **A},
                S("moth", "Nobody knows. But someone wrote down exactly how many.|Nadie lo sabe. Pero alguien anotó exactamente cuántos.|"
                  "Niemand weiß es. Aber jemand schrieb genau auf, wie viele.|Personne ne sait. Mais quelqu'un a noté combien exactement.|"
                  "Nessuno lo sa. Ma qualcuno scrisse esattamente quanti.|Ninguém sabe. Mas alguém anotou exatamente quantas."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 3 the Lueneburg manuscript: the piper in many colours, 130 children
            "bg": "forest", "seed": 7, "music": "lullaby", "wind": True, "eyes": 2, "ambient": 0.38,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"p": PIPER(1500), "k1": KID(1180), "k2": KID(1270), "k3": KID(1360)},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", **A},
                S("narr", "Around 1450, a note was written into a book at Lüneburg.|Hacia 1450, alguien escribió una nota en un libro en Luneburgo.|"
                  "Um 1450 schrieb jemand in Lüneburg eine Notiz in ein Buch.|Vers 1450, une note fut écrite dans un livre à Lunebourg.|"
                  "Verso il 1450, una nota fu scritta in un libro a Luneburgo.|Por volta de 1450, uma nota foi escrita num livro em Luneburgo.", **A),
                {"flash": True, "dur": 1.2},
                {"show": "p", "dur": 0.4, **A},
                S("narr", "It tells of a piper, clothed in many kinds of colours.|Habla de un flautista, vestido de muchos colores.|"
                  "Sie erzählt von einem Pfeifer, gekleidet in vielerlei Farben.|Elle parle d'un joueur de flûte, vêtu de mille couleurs.|"
                  "Parla di un pifferaio, vestito di molti colori.|Ela fala de um flautista, vestido de muitas cores."),
                {"sfx": "whisper", **A},
                {"show": "k1", "dur": 0.4},
                {"show": "k2", "dur": 0.4, **A},
                {"show": "k3", "dur": 0.4, **A},
                S("narr", "One hundred and thirty children born in Hamelin followed him.|Ciento treinta niños nacidos en Hamelín lo siguieron.|"
                  "Hundertdreißig Kinder, in Hameln geboren, folgten ihm.|Cent trente enfants nés à Hamelin le suivirent.|"
                  "Centotrenta bambini nati a Hamelin lo seguirono.|Cento e trinta crianças nascidas em Hamelin o seguiram."),
                {"eyes": "open", **A},
                {"move": "p", "to": "off_right", "speed": "walk"},
                {"move": "k1", "to": "off_right", "speed": "walk", **A},
                {"move": "k2", "to": "off_right", "speed": "walk", **A},
                {"move": "k3", "to": "off_right", "speed": "walk", **A},
                S("narr", "They were lost, it says, near a hill called the Koppen.|Se perdieron, dice, cerca de una colina llamada Koppen.|"
                  "Sie gingen verloren, heißt es, nahe einem Hügel namens Koppen.|Ils furent perdus, dit-on, près d'une colline appelée le Koppen.|"
                  "Furono persi, dice, vicino a una collina chiamata Koppen.|Foram perdidas, diz, perto de uma colina chamada Koppen."),
                {"shake": 0.6, "power": 12, **A},
                {"act": "odo", "do": "jump"},
                S("odo", "And then? Did anyone ever see them again?|¿Y luego? ¿Alguien volvió a verlos?|Und dann? Hat sie je jemand wiedergesehen?|"
                  "Et après ? Quelqu'un les a-t-il revus ?|E poi? Qualcuno li ha mai rivisti?|E depois? Alguém voltou a vê-las?"),
                {"eyes": "close"},
                S("moth", "Never. Not one of them.|Nunca. Ni uno solo.|Nie. Kein einziges.|Jamais. Pas un seul.|Mai. Nemmeno uno.|Nunca. Nenhuma delas."),
                {"sfx": "sting", **A},
                {"flash": True, "dur": 1.0},
                S("narr", "Later versions say a few children stayed behind, too slow to keep up.|Versiones posteriores dicen que unos pocos niños se quedaron atrás, demasiado lentos.|"
                  "Spätere Fassungen sagen, einige Kinder blieben zurück, zu langsam.|Des versions plus tardives disent que quelques enfants, trop lents, restèrent.|"
                  "Versioni successive dicono che pochi bambini rimasero indietro, troppo lenti.|Versões posteriores dizem que algumas crianças ficaram para trás, lentas demais.", **A),
                {"act": "odo", "do": "shake"},
                S("odo", "So someone was left to tell what they saw...|Así que alguien quedó para contar lo que vio...|"
                  "Also blieb jemand zurück, um zu erzählen, was er sah...|Alors quelqu'un est resté pour raconter ce qu'il a vu...|"
                  "Quindi qualcuno rimase a raccontare ciò che vide...|Então alguém ficou para contar o que viu..."),
            ],
            "tail": 0.3,
        },
        {   # 4 the church window c.1300 (destroyed 1660)
            "bg": "chapel", "seed": 5, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "window", "x": 1200, "y": 560, "r": 600}],
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"p": PIPER(1480, 0.95), "g1": {"type": "ghost", "x": 1300, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "Even older proof once hung in Hamelin's church.|Una prueba aún más antigua colgaba en la iglesia de Hamelín.|"
                  "Ein noch älterer Beweis hing einst in Hamelns Kirche.|Une preuve plus ancienne était dans l'église de Hamelin.|"
                  "Una prova ancora più antica era nella chiesa di Hamelin.|Uma prova ainda mais antiga ficava na igreja de Hamelin."),
                {"sfx": "bell", **A},
                {"light": "flare"},
                S("narr", "Around 1300, a stained-glass window showed the piper and the children.|Hacia 1300, una vidriera mostraba al flautista y a los niños.|"
                  "Um 1300 zeigte ein Kirchenfenster den Pfeifer und die Kinder.|Vers 1300, un vitrail montrait le joueur de flûte et les enfants.|"
                  "Verso il 1300, una vetrata mostrava il pifferaio e i bambini.|Por volta de 1300, um vitral mostrava o flautista e as crianças."),
                {"show": "p", "dur": 0.6, **A},
                {"sfx": "whisper", "wait": 0.4},
                S("narr", "People who saw it were alive soon after that summer day.|Quienes la vieron vivieron poco después de aquel día de verano.|"
                  "Wer es sah, lebte kurz nach jenem Sommertag.|Ceux qui le voyaient vivaient peu après ce jour d'été.|"
                  "Chi la vide visse poco dopo quel giorno d'estate.|Quem o viu viveu pouco depois daquele dia de verão."),
                {"hide": "p", "dur": 0.5},
                {"flash": True, "dur": 1.2, **A},
                S("narr", "In 1660, the window was destroyed. Only drawings of it remain.|En 1660, la vidriera fue destruida. Solo quedan dibujos.|"
                  "1660 wurde das Fenster zerstört. Nur Zeichnungen sind geblieben.|En 1660, le vitrail fut détruit. Seuls des dessins subsistent.|"
                  "Nel 1660 la vetrata fu distrutta. Ne restano solo disegni.|Em 1660, o vitral foi destruído. Restam só desenhos."),
                {"sfx": "snap", **A},
                S("narr", "But around 1602, a new house in Hamelin was built with the old date on its wall.|Pero hacia 1602, una casa nueva en Hamelín llevó la vieja fecha en su muro.|"
                  "Doch um 1602 bekam ein neues Haus in Hameln das alte Datum an die Wand.|Mais vers 1602, une maison neuve de Hamelin porta la vieille date sur son mur.|"
                  "Ma verso il 1602, una casa nuova di Hamelin portò la vecchia data sul muro.|Mas por volta de 1602, uma casa nova em Hamelin trouxe a velha data na parede."),
                {"shake": 0.5, "power": 10, **A},
                S("narr", "1284. People still call it the Pied Piper's House.|1284. La gente aún la llama la Casa del Flautista.|"
                  "1284. Man nennt es bis heute das Rattenfängerhaus.|1284. On l'appelle encore la Maison du joueur de flûte.|"
                  "1284. La chiamano ancora la Casa del Pifferaio.|1284. Ainda a chamam de Casa do Flautista."),
                {"sfx": "bell", **A},
                {"light": "dim"},
                {"show": "g1", "dur": 0.4},
                {"act": "odo", "do": "hide"},
                S("odo", "Mothwick... who is that standing by the window?|Mothwick... ¿quién está junto a la ventana?|"
                  "Mothwick... wer steht da am Fenster?|Mothwick... qui est là, près du vitrail ?|"
                  "Mothwick... chi c'è vicino alla finestra?|Mothwick... quem está ali perto da janela?"),
                {"growl": "g1", **A},
                {"hide": "g1", "dur": 0.2},
                {"light": "on", **A},
                {"act": "odo", "do": "unhide"},
                S("moth", "No one. Just the moonlight. Let's keep moving.|Nadie. Solo la luz de la luna. Sigamos.|"
                  "Niemand. Nur das Mondlicht. Gehen wir weiter.|Personne. Juste la lune. Continuons.|"
                  "Nessuno. Solo la luna. Andiamo avanti.|Ninguém. Só o luar. Vamos continuar."),
            ],
            "tail": 0.3,
        },
        {   # 5 the rats came later + Bungelosenstrasse
            "bg": "village", "seed": 8, "music": "drone", "wind": True, "eyes": 2, "ambient": 0.38,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"p": PIPER(1500), "c1": {"type": "crow", "x": 1200, "y": 300, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "You may know the version with the rats. That part came much later.|Quizá conozcas la versión de las ratas. Esa parte llegó mucho después.|"
                  "Du kennst vielleicht die Version mit den Ratten. Die kam viel später.|Tu connais peut-être la version des rats. Elle est venue bien plus tard.|"
                  "Forse conosci la versione dei topi. Quella parte arrivò molto dopo.|Talvez conheça a versão dos ratos. Essa parte veio bem depois."),
                {"sfx": "flutter", **A},
                {"show": "c1", "dur": 0.2, **A},
                S("narr", "The rats first appear in a telling from around 1559.|Las ratas aparecen por primera vez en un relato de hacia 1559.|"
                  "Die Ratten tauchen erst in einer Fassung um 1559 auf.|Les rats apparaissent pour la première fois vers 1559.|"
                  "I topi compaiono per la prima volta in un racconto del 1559 circa.|Os ratos aparecem pela primeira vez num relato de cerca de 1559."),
                {"hide": "c1", "dur": 0.3},
                {"flash": True, "dur": 1.2, **A},
                S("narr", "But one rule in Hamelin is much older, and still kept.|Pero una regla de Hamelín es mucho más antigua, y se sigue cumpliendo.|"
                  "Doch eine Regel in Hameln ist viel älter und gilt noch.|Mais une règle de Hamelin est bien plus ancienne, et toujours suivie.|"
                  "Ma una regola di Hamelin è molto più antica, e vale ancora.|Mas uma regra de Hamelin é bem mais antiga, e ainda vale."),
                {"shake": 0.6, "power": 12, **A},
                {"move": "odo", "to": 720, "speed": "creep"},
                {"move": "moth", "to": 860, "speed": "creep", **A},
                S("narr", "On the street where the children were last seen, no music may play.|En la calle donde vieron a los niños por última vez, no suena música.|"
                  "In der Gasse, wo man die Kinder zuletzt sah, darf keine Musik spielen.|Dans la rue où l'on vit les enfants pour la dernière fois, pas de musique.|"
                  "Nella via dove i bambini furono visti l'ultima volta, niente musica.|Na rua onde as crianças foram vistas pela última vez, não se toca música."),
                {"sfx": "bell", **A},
                S("narr", "Its name is Bungelosenstrasse. No drums. No dancing. Even today.|Se llama Bungelosenstrasse. Sin tambores. Sin baile. Aún hoy.|"
                  "Sie heißt Bungelosenstraße. Keine Trommeln. Kein Tanz. Bis heute.|Elle s'appelle Bungelosenstrasse. Ni tambour. Ni danse. Encore aujourd'hui.|"
                  "Si chiama Bungelosenstrasse. Niente tamburi. Niente balli. Ancora oggi.|Chama-se Bungelosenstrasse. Sem tambores. Sem dança. Até hoje."),
                {"show": "p", "dur": 0.3},
                {"sfx": "whisper", **A},
                {"act": "odo", "do": "scared"},
                S("odo", "Then why do I hear a pipe playing right now?|Entonces, ¿por qué oigo una flauta ahora mismo?|"
                  "Warum höre ich dann gerade eine Flöte spielen?|Alors pourquoi j'entends une flûte en ce moment ?|"
                  "Allora perché sento un flauto proprio adesso?|Então por que estou ouvindo uma flauta agora?"),
                {"hide": "p", "dur": 0.3},
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 6 what really happened? the theories
            "bg": "forest", "seed": 3, "music": "lullaby", "wind": True, "eyes": 2, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"k1": KID(1200), "k2": KID(1300), "g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1, "scale": 0.8}},
            "beats": [
                S("narr", "So what really happened? Historians have argued for centuries.|¿Qué pasó de verdad? Los historiadores discuten desde hace siglos.|"
                  "Was geschah wirklich? Historiker streiten seit Jahrhunderten.|Que s'est-il vraiment passé ? Les historiens en débattent depuis des siècles.|"
                  "Cosa accadde davvero? Gli storici ne discutono da secoli.|O que aconteceu de verdade? Historiadores discutem há séculos."),
                {"flash": True, "dur": 1.2, **A},
                {"show": "k1", "dur": 0.5},
                {"show": "k2", "dur": 0.5, **A},
                S("narr", "Some think young people left to settle new lands far to the east.|Algunos creen que los jóvenes se fueron a poblar tierras lejanas al este.|"
                  "Manche glauben, junge Leute zogen fort, um Land im Osten zu besiedeln.|Certains pensent que des jeunes partirent s'installer loin à l'est.|"
                  "Alcuni pensano che i giovani partirono per abitare terre lontane a est.|Alguns acham que os jovens partiram para povoar terras distantes no leste."),
                {"move": "k1", "to": "off_right", "speed": "walk"},
                {"move": "k2", "to": "off_right", "speed": "walk", **A},
                S("narr", "Others think of a pilgrimage, or a strange dancing sickness.|Otros piensan en una peregrinación, o en una extraña fiebre del baile.|"
                  "Andere denken an eine Pilgerfahrt oder eine seltsame Tanzwut.|D'autres pensent à un pèlerinage, ou à une étrange folie de la danse.|"
                  "Altri pensano a un pellegrinaggio, o a una strana mania del ballo.|Outros pensam numa peregrinação, ou numa estranha febre da dança."),
                {"sfx": "snap", **A},
                {"act": "odo", "do": "calm"},
                S("narr", "In 1237, children really did dance all the way from Erfurt to Arnstadt.|En 1237, unos niños sí fueron bailando de Erfurt a Arnstadt.|"
                  "1237 tanzten Kinder tatsächlich den ganzen Weg von Erfurt nach Arnstadt.|En 1237, des enfants ont vraiment dansé d'Erfurt jusqu'à Arnstadt.|"
                  "Nel 1237 dei bambini ballarono davvero da Erfurt fino ad Arnstadt.|Em 1237, crianças foram mesmo dançando de Erfurt até Arnstadt."),
                {"shake": 0.5, "power": 10, **A},
                S("narr", "But for Hamelin, no record says where the children went.|Pero de Hamelín, ningún registro dice adónde fueron los niños.|"
                  "Doch für Hameln sagt kein Dokument, wohin die Kinder gingen.|Mais pour Hamelin, aucun récit ne dit où allèrent les enfants.|"
                  "Ma per Hamelin, nessun documento dice dove andarono i bambini.|Mas sobre Hamelin, nenhum registro diz para onde as crianças foram."),
                {"light": "out"},
                {"show": "g1", "dur": 0.3, **A},
                {"sfx": "whisper", **A},
                S("odo", "Mothwick... the lantern's out. Someone is humming that tune.|Mothwick... la linterna se apagó. Alguien tararea esa melodía.|"
                  "Mothwick... die Laterne ist aus. Jemand summt diese Melodie.|Mothwick... la lanterne est éteinte. Quelqu'un fredonne cet air.|"
                  "Mothwick... la lanterna è spenta. Qualcuno canticchia quella melodia.|Mothwick... a lanterna apagou. Alguém está cantarolando essa melodia."),
                {"flash": True, "dur": 1.2},
                {"hide": "g1", "dur": 0.2, **A},
                {"light": "flare"},
                S("moth", "Cover your ears, Odo. Whatever you do... don't follow it.|Tápate los oídos, Odo. Pase lo que pase... no la sigas.|"
                  "Halt dir die Ohren zu, Odo. Was auch passiert... folge ihr nicht.|Bouche-toi les oreilles, Odo. Quoi qu'il arrive... ne la suis pas.|"
                  "Tappati le orecchie, Odo. Qualunque cosa accada... non seguirla.|Tape os ouvidos, Odo. Aconteça o que acontecer... não a siga."),
                {"eyes": "close"},
            ],
            "tail": 0.3,
        },
        {   # 7 the hill: cliffhanger
            "bg": "forest", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"p": PIPER(1520, 1.05), "c1": {"type": "crow", "x": 1300, "y": 320, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "Over seven hundred years later, Hamelin still tells the story every summer.|Más de setecientos años después, Hamelín aún cuenta la historia cada verano.|"
                  "Über siebenhundert Jahre später erzählt Hameln die Geschichte jeden Sommer.|Plus de sept cents ans après, Hamelin raconte encore l'histoire chaque été.|"
                  "Oltre settecento anni dopo, Hamelin racconta ancora la storia ogni estate.|Mais de setecentos anos depois, Hamelin ainda conta a história todo verão."),
                {"sfx": "whoosh", **A},
                S("narr", "But the piper's name, his face, his tune... were never written down.|Pero el nombre del flautista, su cara, su melodía... nunca se escribieron.|"
                  "Doch Name, Gesicht und Melodie des Pfeifers... wurden nie aufgeschrieben.|Mais le nom du joueur, son visage, son air... ne furent jamais écrits.|"
                  "Ma il nome del pifferaio, il suo volto, la sua melodia... non furono mai scritti.|Mas o nome do flautista, seu rosto, sua melodia... nunca foram escritos."),
                {"show": "c1", "dur": 0.2},
                {"sfx": "flutter", **A},
                {"hide": "c1", "dur": 0.4},
                S("odo", "Mothwick... can you hear it? A pipe... up on the hill.|Mothwick... ¿lo oyes? Una flauta... arriba en la colina.|"
                  "Mothwick... hörst du das? Eine Flöte... oben auf dem Hügel.|Mothwick... tu entends ? Une flûte... là-haut sur la colline.|"
                  "Mothwick... lo senti? Un flauto... su sulla collina.|Mothwick... está ouvindo? Uma flauta... lá em cima na colina."),
                {"eyes": "open", **A},
                {"flash": True, "dur": 1.0},
                {"eyes": "close"},
                {"sfx": "step", "wait": 0.3},
                {"act": "odo", "do": "turn"},
                S("odo", "Mothwick... there are small footprints in the mud. Lots of them.|Mothwick... hay huellas pequeñas en el barro. Muchísimas.|"
                  "Mothwick... da sind kleine Fußspuren im Schlamm. Ganz viele.|Mothwick... il y a de petites traces de pas dans la boue. Des dizaines.|"
                  "Mothwick... ci sono piccole impronte nel fango. Tantissime.|Mothwick... tem pegadas pequenas na lama. Muitas."),
                {"sfx": "step", "wait": 0.4},
                S("moth", "They all walk up the hill, Odo... and none come back.|Todas suben la colina, Odo... y ninguna vuelve.|"
                  "Sie führen alle den Hügel hinauf, Odo... und keine zurück.|Elles montent toutes la colline, Odo... et aucune ne revient.|"
                  "Salgono tutte sulla collina, Odo... e nessuna torna indietro.|Todas sobem a colina, Odo... e nenhuma volta."),
                {"show": "p", "dur": 0.3},
                {"growl": "p", **A},
                {"lunge": "p", "to": 1150},
                {"light": "out", **A},
                {"card": "WHO WAS THE PIPER?", "dur": 2.4},
            ],
            "tail": 0.1,
        },
    ],
}


def L(*parts):
    return "|".join(parts)


def SHOT(bg, seed, beats, odo=700, amb=0.48, eyes=0, lights=None, creatures=None, tail=0.05, music="lullaby"):
    sh = {"bg": bg, "seed": seed, "music": music, "wind": True, "eyes": eyes, "ambient": amb, "focus": "odo", "fade": False,
          "chars": {"odo": {"x": odo}}, "creatures": creatures or {}, "beats": beats, "tail": tail}
    if lights:
        sh["lights"] = lights
    return sh


MOON = [{"kind": "moon", "x": 900, "y": 300, "r": 900}]
WIN = [{"kind": "window", "x": 900, "y": 640, "r": 520}]

# Short: hard-cut shots (no fades) + flashes -> a new thing every 2-4 s; one scare (the piper's lunge);
# the last shot repeats the first shot's set-up so the final frame loops back to frame 1.
short1 = {   # the rule / scariest true detail
    "id": "ep009_short1", "format": "short",
    "title": "Why Did 130 Children Follow This Tune? #shorts",
    "hook": "DON'T FOLLOW THE MUSIC",
    "description": "Hamelin, Germany, 26 June 1284: an old record says a piper dressed in many colours led 130 children away. They were never seen again — and on the street where they were last seen, music is still not allowed. Full true story on the channel. #shorts #piedpiper #hamelin #truestory #hollowmere",
    "tags": ["shorts"] + TAGS[:10],
    "thumbnail": {"bg": "village", "seed": 4, "creature": "figure", "text": "DON'T FOLLOW"},
    "shots": [
        SHOT("village", 4, [
            {"wait": 0.4}, {"flash": True}, {"shake": 0.4, "power": 14, "and": True},
            {"move": "odo", "to": 760, "speed": "creep", "and": True},
            S("narr", L("1284. A tune in the street.", "1284. Una melodía en la calle.", "1284. Eine Melodie in der Gasse.",
                        "1284. Un air dans la rue.", "1284. Una melodia per strada.", "1284. Uma melodia na rua."), **A),
            {"sfx": "whisper", **A},
        ], amb=0.55, lights=WIN),
        SHOT("forest", 7, [
            {"show": "p", "dur": 0.3},
            {"show": "k1", "dur": 0.3, **A}, {"show": "k2", "dur": 0.3, **A},
            S("narr", L("A piper in bright colours. 130 children followed him.", "Un flautista de colores. Lo siguieron 130 niños.",
                        "Ein bunter Pfeifer. 130 Kinder folgten ihm.", "Un joueur de flûte bariolé. 130 enfants le suivirent.",
                        "Un pifferaio colorato. Lo seguirono 130 bambini.", "Um flautista colorido. 130 crianças o seguiram."), **A),
            {"move": "k1", "to": "off_right", "speed": "walk", **A},
            {"move": "k2", "to": "off_right", "speed": "walk", **A},
            {"flash": True},
        ], odo=420, eyes=2, lights=MOON, creatures={"p": PIPER(900, 0.85), "k1": KID(640), "k2": KID(740)}),
        SHOT("village", 8, [
            {"act": "odo", "do": "scared"},
            S("narr", L("They were never seen again. Today, that street bans all music.", "Nunca más se les vio. Hoy, esa calle prohíbe la música.",
                        "Man sah sie nie wieder. Heute ist Musik in dieser Gasse verboten.", "On ne les revit jamais. Aujourd'hui, la musique y est interdite.",
                        "Non furono mai più visti. Oggi in quella via la musica è vietata.", "Nunca mais foram vistas. Hoje, a música é proibida nessa rua."), **A),
            {"sfx": "bell", **A},
            {"light": "out"},
            {"show": "p", "dur": 0.1, **A},
            {"lunge": "p", "to": 820, **A},
            {"flash": True, "and": True},
        ], odo=560, lights=WIN, creatures={"p": PIPER(950, 1.0)}),
        SHOT("village", 4, [
            {"move": "odo", "to": 700, "speed": "walk"},
            S("narr", L("So if you hear a pipe tonight...", "Así que si oyes una flauta esta noche...", "Wenn du heute Nacht eine Flöte hörst...",
                        "Alors si tu entends une flûte ce soir...", "Quindi se senti un flauto stanotte...", "Então, se ouvir uma flauta esta noite..."), **A),
        ], odo=820, amb=0.55, lights=WIN, tail=0.2),
    ],
}

short1["shots"][1]["focus"] = ["odo", "p"]   # keep the piper + children inside the vertical frame
short1["shots"][2]["cam"] = {"x": 740}

for s in (long_, short1):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

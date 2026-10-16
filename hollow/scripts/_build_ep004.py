"""Builds Hollowmere EP4 (true story: the Mary Celeste, 1872). Run: python3 scripts/_build_ep004.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Mary Celeste", "ghost ship",
        "Azores", "Atlantic Ocean", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/",
           "https://www.history.com/this-day-in-history/December-5/the-mystery-of-the-mary-celeste",
           "https://www.ebsco.com/research-starters/social-sciences-and-humanities/mary-celeste-mystery"]

long_ = {
    "id": "ep004_long", "format": "long",
    "title": "The Ship Found With No One Aboard | True Story | Hollowmere Tales EP 4",
    "description": ("A true story. On December 5, 1872, the crew of the Dei Gratia found the brigantine Mary Celeste "
                    "drifting near the Azores under sail. Food, water and the crew's belongings were still aboard. "
                    "The only lifeboat was gone. Captain Benjamin Briggs, his wife Sarah, their two-year-old daughter Sophia "
                    "and seven crewmen were never seen again.\n\n"
                    "Told from the historical records; theories are marked as theories.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #unsolvedmystery #ghostship #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 4", "Benjamin Briggs", "Dei Gratia"],
    "thumbnail": {"bg": "sea", "seed": 8, "creature": "ship", "text": "NO ONE ABOARD"},
    "shots": [
        {   # 1 cold open
            "bg": "sea", "seed": 8, "music": "drone", "wind": True, "eyes": 0, "lantern": 0.0, "ambient": 0.36,
            "cam": {"from": [960, 560, 1.0], "to": [960, 590, 1.18]},
            "creatures": {"mc": {"type": "ship", "x": 1350, "y": 680, "scale": 0.6, "state": "hidden", "face": -1}},
            "beats": [
                {"sfx": "creak", "wait": 1.0},
                S("narr", "This is a true story, told from the records of 1872.|Esta es una historia real, contada a partir de los registros de 1872.|"
                  "Dies ist eine wahre Geschichte, nach den Aufzeichnungen von 1872.|Ceci est une histoire vraie, tirée des archives de 1872.|"
                  "Questa è una storia vera, tratta dagli archivi del 1872.|Esta é uma história real, contada a partir dos registros de 1872."),
                {"show": "mc", "dur": 2.0},
                S("narr", "A ship was found sailing across the Atlantic, its sails still set.|Un barco fue hallado navegando por el Atlántico, con las velas aún izadas.|"
                  "Ein Schiff wurde mitten im Atlantik gefunden, die Segel noch gesetzt.|Un navire fut trouvé en plein Atlantique, voiles encore hissées.|"
                  "Una nave fu trovata in mezzo all'Atlantico, con le vele ancora spiegate.|Um navio foi encontrado no Atlântico, ainda com as velas içadas."),
                S("narr", "There was food in the galley. There was fresh water.|Había comida en la cocina. Había agua dulce.|"
                  "In der Kombüse lag Essen. Es gab frisches Wasser.|Il y avait de la nourriture en cuisine. Il y avait de l'eau douce.|"
                  "C'era cibo in cambusa. C'era acqua dolce.|Havia comida na cozinha. Havia água doce."),
                S("narr", "But there was no one aboard.|Pero no había nadie a bordo.|Aber es war niemand an Bord.|Mais il n'y avait personne à bord.|"
                  "Ma a bordo non c'era nessuno.|Mas não havia ninguém a bordo."),
                {"sfx": "bell", "wait": 0.6},
                {"card": "THE MARY CELESTE", "dur": 2.8},
            ],
            "tail": 0.2,
        },
        {   # 2 New York, November 1872
            "bg": "village", "seed": 5, "music": "lullaby", "eyes": 0, "ambient": 0.46,
            "lights": [{"kind": "window", "x": 1200, "y": 640, "r": 500}],
            "cam": {"from": [900, 600, 1.12], "to": [1000, 620, 1.2]},
            "chars": {"odo": {"x": 480}, "moth": {"x": 640, "y": 650}},
            "creatures": {"briggs": {"type": "figure", "x": 1400, "seed": 1, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "On November 7, 1872, the Mary Celeste left New York for Genoa, in Italy.|El 7 de noviembre de 1872, el Mary Celeste salió de Nueva York hacia Génova, en Italia.|"
                  "Am 7. November 1872 verließ die Mary Celeste New York Richtung Genua in Italien.|Le 7 novembre 1872, le Mary Celeste quitta New York pour Gênes, en Italie.|"
                  "Il 7 novembre 1872, la Mary Celeste lasciò New York diretta a Genova.|Em 7 de novembro de 1872, o Mary Celeste deixou Nova York rumo a Gênova, na Itália."),
                {"show": "briggs", "dur": 1.2},
                S("narr", "Her captain was Benjamin Briggs, an experienced seaman from Massachusetts.|Su capitán era Benjamin Briggs, un marino experimentado de Massachusetts.|"
                  "Ihr Kapitän war Benjamin Briggs, ein erfahrener Seemann aus Massachusetts.|Son capitaine était Benjamin Briggs, un marin expérimenté du Massachusetts.|"
                  "Il capitano era Benjamin Briggs, un marinaio esperto del Massachusetts.|O capitão era Benjamin Briggs, um marinheiro experiente de Massachusetts."),
                S("narr", "He brought his wife, Sarah, and their two-year-old daughter, Sophia.|Llevó a su esposa, Sarah, y a su hija de dos años, Sophia.|"
                  "Er nahm seine Frau Sarah und ihre zweijährige Tochter Sophia mit.|Il emmena sa femme, Sarah, et leur fille de deux ans, Sophia.|"
                  "Portò con sé la moglie, Sarah, e la figlia di due anni, Sophia.|Ele levou a esposa, Sarah, e a filha de dois anos, Sophia."),
                S("narr", "Seven crewmen sailed with them. Ten people in all.|Siete marineros iban con ellos. Diez personas en total.|"
                  "Sieben Seeleute fuhren mit. Zehn Menschen insgesamt.|Sept marins les accompagnaient. Dix personnes en tout.|"
                  "Sette marinai erano con loro. Dieci persone in tutto.|Sete tripulantes iam com eles. Dez pessoas ao todo."),
                S("narr", "In the hold: about seventeen hundred barrels of alcohol.|En la bodega: unos mil setecientos barriles de alcohol.|"
                  "Im Laderaum: etwa siebzehnhundert Fässer Alkohol.|Dans la cale : environ mille sept cents barils d'alcool.|"
                  "Nella stiva: circa millesettecento barili di alcol.|No porão: cerca de mil e setecentos barris de álcool."),
                S("odo", "A whole family on one ship?|¿Una familia entera en un barco?|Eine ganze Familie auf einem Schiff?|"
                  "Une famille entière sur un seul navire ?|Un'intera famiglia su una nave?|Uma família inteira num navio?"),
                S("moth", "Captains often took their families. The sea was their home.|Los capitanes solían llevar a sus familias. El mar era su hogar.|"
                  "Kapitäne nahmen oft ihre Familien mit. Das Meer war ihr Zuhause.|Les capitaines emmenaient souvent leur famille. La mer était leur maison.|"
                  "I capitani portavano spesso la famiglia. Il mare era la loro casa.|Capitães muitas vezes levavam a família. O mar era o lar deles."),
                {"hide": "briggs", "dur": 1.2},
            ],
            "tail": 0.3,
        },
        {   # 3 the last log entry, Santa Maria
            "bg": "lighthouse", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.1], "to": [1040, 610, 1.2]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "creatures": {"c1": {"type": "crow", "x": 1400, "y": 420, "state": "hidden", "fly": 1}},
            "beats": [
                S("narr", "On November 25, at five in the morning, someone wrote in the ship's log.|El 25 de noviembre, a las cinco de la mañana, alguien escribió en el diario del barco.|"
                  "Am 25. November, um fünf Uhr morgens, schrieb jemand ins Logbuch.|Le 25 novembre, à cinq heures du matin, quelqu'un écrivit dans le journal de bord.|"
                  "Il 25 novembre, alle cinque del mattino, qualcuno scrisse nel diario di bordo.|Em 25 de novembro, às cinco da manhã, alguém escreveu no diário de bordo."),
                S("narr", "The island of Santa Maria, in the Azores, was in sight.|La isla de Santa María, en las Azores, estaba a la vista.|"
                  "Die Insel Santa Maria auf den Azoren war in Sicht.|L'île de Santa Maria, aux Açores, était en vue.|"
                  "L'isola di Santa Maria, nelle Azzorre, era in vista.|A ilha de Santa Maria, nos Açores, estava à vista."),
                {"show": "c1", "dur": 0.6},
                {"sfx": "caw", "and": True},
                S("narr", "It is the last thing anyone aboard ever wrote.|Es lo último que alguien a bordo escribió jamás.|"
                  "Es ist das Letzte, was je jemand an Bord schrieb.|C'est la dernière chose que quiconque à bord ait jamais écrite.|"
                  "È l'ultima cosa che qualcuno a bordo abbia mai scritto.|É a última coisa que alguém a bordo escreveu."),
                {"act": "odo", "do": "scared"},
                S("odo", "What happened after that?|¿Qué pasó después?|Was ist danach passiert?|Que s'est-il passé ensuite ?|Cosa successe dopo?|O que aconteceu depois?"),
                S("moth", "Nobody knows. The ship kept sailing on, all alone.|Nadie lo sabe. El barco siguió navegando, solo.|"
                  "Niemand weiß es. Das Schiff segelte allein weiter.|Personne ne sait. Le navire continua seul sa route.|"
                  "Nessuno lo sa. La nave continuò a navigare, da sola.|Ninguém sabe. O navio seguiu navegando, sozinho."),
                {"hide": "c1", "dur": 0.8},
            ],
            "tail": 0.3,
        },
        {   # 4 the Dei Gratia boards her
            "bg": "sea", "seed": 4, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.38,
            "cam": {"from": [900, 600, 1.12], "to": [1080, 610, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"mc": {"type": "ship", "x": 1400, "y": 670, "scale": 0.7, "state": "hidden", "face": -1}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "walk"},
                {"move": "moth", "to": 720, "speed": "walk", "and": True},
                S("narr", "On December 5, a British ship, the Dei Gratia, saw sails on the horizon.|El 5 de diciembre, un barco británico, el Dei Gratia, vio velas en el horizonte.|"
                  "Am 5. Dezember sah ein britisches Schiff, die Dei Gratia, Segel am Horizont.|Le 5 décembre, un navire britannique, le Dei Gratia, aperçut des voiles à l'horizon.|"
                  "Il 5 dicembre una nave britannica, la Dei Gratia, vide delle vele all'orizzonte.|Em 5 de dezembro, um navio britânico, o Dei Gratia, viu velas no horizonte."),
                {"show": "mc", "dur": 1.6},
                S("narr", "The ship was moving strangely. No one stood at the wheel.|El barco se movía de forma extraña. Nadie estaba al timón.|"
                  "Das Schiff bewegte sich seltsam. Niemand stand am Steuer.|Le navire avançait bizarrement. Personne n'était à la barre.|"
                  "La nave si muoveva in modo strano. Nessuno era al timone.|O navio se movia de um jeito estranho. Ninguém estava ao leme."),
                S("narr", "Her captain, David Morehouse, sent men across in a small boat.|Su capitán, David Morehouse, envió hombres en un bote.|"
                  "Ihr Kapitän, David Morehouse, schickte Männer in einem Beiboot hinüber.|Son capitaine, David Morehouse, envoya des hommes en canot.|"
                  "Il capitano, David Morehouse, mandò degli uomini con una scialuppa.|O capitão, David Morehouse, enviou homens num bote."),
                {"sfx": "creak", "wait": 0.8},
                S("narr", "They called out. Nobody answered.|Llamaron. Nadie respondió.|Sie riefen. Niemand antwortete.|Ils appelèrent. Personne ne répondit.|"
                  "Chiamarono. Nessuno rispose.|Eles chamaram. Ninguém respondeu."),
                {"act": "odo", "do": "shake"},
                S("narr", "It was the Mary Celeste, about four hundred miles east of the Azores.|Era el Mary Celeste, a unas cuatrocientas millas al este de las Azores.|"
                  "Es war die Mary Celeste, etwa vierhundert Meilen östlich der Azoren.|C'était le Mary Celeste, à environ quatre cents milles à l'est des Açores.|"
                  "Era la Mary Celeste, circa quattrocento miglia a est delle Azzorre.|Era o Mary Celeste, a cerca de quatrocentas milhas a leste dos Açores."),
                {"move": "odo", "to": "off_right", "speed": "walk"},
                {"move": "moth", "to": "off_right", "speed": "walk", "and": True},
            ],
            "tail": 0.3,
        },
        {   # 5 below deck
            "bg": "manor", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.34,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 620, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1},
                          "g2": {"type": "ghost", "x": 1620, "state": "hidden", "face": -1, "scale": 0.6}},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", "and": True},
                S("narr", "Below deck, the crew's clothes and belongings were still in their places.|Bajo cubierta, la ropa y las cosas de la tripulación seguían en su sitio.|"
                  "Unter Deck lagen Kleidung und Habe der Mannschaft noch an ihrem Platz.|Sous le pont, les vêtements et affaires de l'équipage étaient encore là.|"
                  "Sottocoperta, vestiti e oggetti dell'equipaggio erano ancora al loro posto.|Sob o convés, as roupas e coisas da tripulação ainda estavam no lugar."),
                S("narr", "There was food and water for six months.|Había comida y agua para seis meses.|Es gab Essen und Wasser für sechs Monate.|"
                  "Il y avait de quoi manger et boire pour six mois.|C'erano cibo e acqua per sei mesi.|Havia comida e água para seis meses."),
                S("narr", "About three feet of water sloshed in the hold. One pump had been taken apart.|Había casi un metro de agua en la bodega. Una bomba estaba desmontada.|"
                  "Knapp ein Meter Wasser stand im Laderaum. Eine Pumpe war zerlegt.|Près d'un mètre d'eau dans la cale. Une pompe avait été démontée.|"
                  "C'era quasi un metro d'acqua nella stiva. Una pompa era smontata.|Havia quase um metro de água no porão. Uma bomba estava desmontada."),
                {"sfx": "creak", "wait": 0.6},
                S("narr", "The cargo was almost untouched. But the ship's only lifeboat was gone.|La carga estaba casi intacta. Pero el único bote salvavidas no estaba.|"
                  "Die Ladung war fast unberührt. Doch das einzige Rettungsboot fehlte.|La cargaison était presque intacte. Mais l'unique canot de sauvetage avait disparu.|"
                  "Il carico era quasi intatto. Ma l'unica scialuppa era sparita.|A carga estava quase intacta. Mas o único bote salva-vidas tinha sumido."),
                {"flash": True},
                {"show": "g1", "dur": 1.6, "and": True},
                {"show": "g2", "dur": 1.6, "and": True},
                S("odo", "They left a ship that could still float... for a tiny boat?|¿Dejaron un barco que aún flotaba... por un botecito?|"
                  "Sie verließen ein Schiff, das noch schwamm... für ein winziges Boot?|Ils ont quitté un navire qui flottait encore... pour un petit canot ?|"
                  "Hanno lasciato una nave che galleggiava ancora... per una barchetta?|Eles deixaram um navio que ainda flutuava... por um botinho?"),
                S("moth", "Something made them believe they had to. Right then.|Algo les hizo creer que debían hacerlo. En ese momento.|"
                  "Etwas ließ sie glauben, dass sie mussten. Sofort.|Quelque chose leur a fait croire qu'ils le devaient. Sur-le-champ.|"
                  "Qualcosa li convinse che dovevano farlo. Subito.|Algo os fez acreditar que precisavam. Naquela hora."),
                {"wait": 0.8},
                {"hide": "g1", "dur": 1.2},
                {"hide": "g2", "dur": 1.2, "and": True},
            ],
            "tail": 0.3,
        },
        {   # 6 Gibraltar and the theories
            "bg": "manor", "seed": 2, "music": "drone", "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "window", "x": 1250, "y": 620, "r": 520}],
            "cam": {"from": [960, 600, 1.1], "to": [900, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"judge": {"type": "figure", "x": 1400, "seed": 0, "face": -1, "state": "hidden"}},
            "beats": [
                S("narr", "The Dei Gratia sailed the empty ship to Gibraltar. A court asked what happened.|El Dei Gratia llevó el barco vacío a Gibraltar. Un tribunal investigó.|"
                  "Die Dei Gratia brachte das leere Schiff nach Gibraltar. Ein Gericht ermittelte.|Le Dei Gratia mena le navire vide à Gibraltar. Un tribunal enquêta.|"
                  "La Dei Gratia portò la nave vuota a Gibilterra. Un tribunale indagò.|O Dei Gratia levou o navio vazio a Gibraltar. Um tribunal investigou."),
                {"show": "judge", "dur": 1.2},
                S("narr", "Some suspected foul play. No proof of it was ever found.|Algunos sospecharon un crimen. Nunca se halló prueba alguna.|"
                  "Manche vermuteten ein Verbrechen. Ein Beweis wurde nie gefunden.|Certains soupçonnèrent un crime. Aucune preuve ne fut jamais trouvée.|"
                  "Alcuni sospettarono un crimine. Nessuna prova fu mai trovata.|Alguns suspeitaram de crime. Nenhuma prova foi encontrada."),
                S("narr", "Nine of the barrels were empty. Today many think the captain feared the fumes.|Nueve barriles estaban vacíos. Hoy muchos creen que el capitán temió los vapores.|"
                  "Neun Fässer waren leer. Heute glauben viele, der Kapitän fürchtete die Dämpfe.|Neuf barils étaient vides. Beaucoup pensent que le capitaine craignit les vapeurs.|"
                  "Nove barili erano vuoti. Oggi molti pensano che il capitano temesse i vapori.|Nove barris estavam vazios. Hoje muitos acham que o capitão temeu os vapores."),
                S("narr", "Perhaps he ordered everyone into the lifeboat, just for a while.|Quizá ordenó a todos subir al bote, solo por un rato.|"
                  "Vielleicht befahl er allen ins Rettungsboot, nur für eine Weile.|Peut-être ordonna-t-il à tous de monter dans le canot, juste un moment.|"
                  "Forse ordinò a tutti di salire sulla scialuppa, solo per un po'.|Talvez ele mandou todos para o bote, só por um tempo."),
                S("narr", "But that is a theory. Nothing has ever been proven.|Pero es una teoría. Nunca se ha demostrado nada.|"
                  "Doch das ist eine Theorie. Bewiesen wurde nie etwas.|Mais ce n'est qu'une théorie. Rien n'a jamais été prouvé.|"
                  "Ma è una teoria. Niente è mai stato provato.|Mas é uma teoria. Nada jamais foi provado."),
                {"hide": "judge", "dur": 1.2},
            ],
            "tail": 0.3,
        },
        {   # 7 ending
            "bg": "sea", "seed": 5, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [760, 640, 1.24]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"mc": {"type": "ship", "x": 1450, "y": 680, "scale": 0.5, "state": "hidden", "face": -1}},
            "beats": [
                {"show": "mc", "dur": 1.6},
                S("narr", "The Mary Celeste sailed for thirteen more years, with a cursed name.|El Mary Celeste navegó trece años más, con un nombre maldito.|"
                  "Die Mary Celeste segelte noch dreizehn Jahre, mit einem verfluchten Namen.|Le Mary Celeste navigua encore treize ans, avec un nom maudit.|"
                  "La Mary Celeste navigò altri tredici anni, con un nome maledetto.|O Mary Celeste navegou mais treze anos, com um nome amaldiçoado."),
                S("narr", "In the end, her last owner ran her aground off Haiti, on purpose.|Al final, su último dueño la hizo encallar a propósito frente a Haití.|"
                  "Am Ende ließ ihr letzter Besitzer sie vor Haiti absichtlich auflaufen.|À la fin, son dernier propriétaire l'échoua exprès au large d'Haïti.|"
                  "Alla fine, l'ultimo proprietario la fece arenare apposta al largo di Haiti.|No fim, o último dono a encalhou de propósito perto do Haiti."),
                {"shake": 0.6, "power": 10},
                {"sfx": "whoosh", "and": True},
                S("narr", "The lifeboat was never found. Neither were the ten people in it.|El bote nunca fue hallado. Tampoco las diez personas que iban en él.|"
                  "Das Rettungsboot wurde nie gefunden. Die zehn Menschen darin auch nicht.|Le canot ne fut jamais retrouvé. Ni les dix personnes à bord.|"
                  "La scialuppa non fu mai trovata. Né le dieci persone a bordo.|O bote nunca foi encontrado. Nem as dez pessoas nele."),
                S("odo", "And little Sophia?|¿Y la pequeña Sophia?|Und die kleine Sophia?|Et la petite Sophia ?|E la piccola Sophia?|E a pequena Sophia?"),
                {"wait": 0.8},
                S("moth", "Somewhere out there, the sea is still keeping its secret.|En algún lugar, el mar sigue guardando su secreto.|"
                  "Irgendwo da draußen hütet das Meer noch immer sein Geheimnis.|Quelque part, la mer garde encore son secret.|"
                  "Da qualche parte, il mare custodisce ancora il suo segreto.|Em algum lugar, o mar ainda guarda seu segredo."),
                {"hide": "mc", "dur": 2.0},
                {"sfx": "bell", "wait": 0.8},
                {"card": "A TRUE STORY. STILL UNSOLVED.", "dur": 3.0},
            ],
            "tail": 0.2,
        },
    ],
}

short1 = {   # the real fact
    "id": "ep004_short1", "format": "short",
    "title": "Food on board. Sails up. Nobody there. ⛵ #shorts",
    "hook": "NO ONE ABOARD",
    "description": "True story: on December 5, 1872, sailors found the Mary Celeste drifting near the Azores. Food, water, belongings, all there. Ten people gone. #shorts #truestory #unsolvedmystery #maryceleste #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "sea", "seed": 8, "creature": "ship", "text": "NO ONE ABOARD"},
    "shots": [{
        "bg": "sea", "seed": 8, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.38, "focus": "odo",
        "chars": {"odo": {"x": 760}},
        "creatures": {"g1": {"type": "ghost", "x": 1150, "state": "hidden", "face": -1}},
        "beats": [
            {"sfx": "creak", "wait": 0.8},
            S("narr", "True story. 1872. A ship is found drifting in the Atlantic.|Historia real. 1872. Un barco aparece a la deriva en el Atlántico.|"
              "Wahre Geschichte. 1872. Ein Schiff treibt im Atlantik.|Histoire vraie. 1872. Un navire dérive dans l'Atlantique.|"
              "Storia vera. 1872. Una nave va alla deriva nell'Atlantico.|História real. 1872. Um navio é achado à deriva no Atlântico."),
            S("narr", "Food for six months. Clothes still folded. Sails still up.|Comida para seis meses. Ropa doblada. Velas izadas.|"
              "Essen für sechs Monate. Kleidung gefaltet. Segel gesetzt.|De quoi manger six mois. Habits pliés. Voiles hissées.|"
              "Cibo per sei mesi. Vestiti piegati. Vele spiegate.|Comida para seis meses. Roupas dobradas. Velas içadas."),
            S("narr", "Ten people had been aboard. Now there was no one.|Iban diez personas a bordo. Ahora no había nadie.|"
              "Zehn Menschen waren an Bord gewesen. Jetzt war niemand da.|Dix personnes étaient à bord. Il n'y avait plus personne.|"
              "A bordo c'erano dieci persone. Ora non c'era nessuno.|Dez pessoas estavam a bordo. Agora não havia ninguém."),
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
    "id": "ep004_short2", "format": "short",
    "title": "Would YOU board the empty ship? 🌊 #shorts",
    "hook": "WOULD YOU BOARD?",
    "description": "December 1872. A ship drifts toward you with its sails up and no one at the wheel. You call out. Nobody answers. Would you board it? Comment YES or NO 👇 #shorts #truestory #maryceleste #hollowmere",
    "tags": ["shorts"] + TAGS[:8] + ["would you rather"],
    "thumbnail": {"bg": "sea", "seed": 4, "creature": "ship", "text": "WOULD YOU BOARD"},
    "shots": [{
        "bg": "sea", "seed": 4, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.40,
        "chars": {"odo": {"x": 760}},
        "creatures": {"mc": {"type": "ship", "x": 1150, "y": 680, "scale": 0.6, "state": "hidden", "face": -1}},
        "focus": ["odo", "mc"],
        "beats": [
            S("narr", "It is December 1872. A ship drifts toward you on the open sea.|Es diciembre de 1872. Un barco se acerca a la deriva en alta mar.|"
              "Es ist Dezember 1872. Ein Schiff treibt auf offener See auf dich zu.|Décembre 1872. Un navire dérive vers toi en pleine mer.|"
              "È dicembre 1872. Una nave va alla deriva verso di te in mare aperto.|É dezembro de 1872. Um navio vem à deriva em alto-mar."),
            {"show": "mc", "dur": 1.5},
            S("narr", "Its sails are up. No one is at the wheel. You call out. Silence.|Velas izadas. Nadie al timón. Llamas. Silencio.|"
              "Die Segel sind gesetzt. Niemand am Steuer. Du rufst. Stille.|Voiles hissées. Personne à la barre. Tu appelles. Silence.|"
              "Vele spiegate. Nessuno al timone. Chiami. Silenzio.|Velas içadas. Ninguém ao leme. Você chama. Silêncio."),
            {"act": "odo", "do": "shake"},
            S("narr", "Would YOU climb aboard? Comment YES or NO.|¿Subirías TÚ a bordo? Comenta SÍ o NO.|"
              "Würdest DU an Bord gehen? Schreib JA oder NEIN.|Et TOI, tu monterais à bord ? Écris OUI ou NON.|"
              "TU saliresti a bordo? Scrivi SÌ o NO.|VOCÊ subiria a bordo? Comente SIM ou NÃO."),
        ],
        "tail": 1.2,
    }],
}

short3 = {   # scariest moment
    "id": "ep004_short3", "format": "short",
    "title": "The lifeboat was gone. So were they. 🚣 #shorts",
    "hook": "THE LIFEBOAT WAS GONE",
    "description": "Below deck on the Mary Celeste: belongings in place, water in the hold, and the only lifeboat gone. Full true story on the channel. #shorts #truestory #maryceleste #unsolvedmystery #hollowmere",
    "tags": ["shorts"] + TAGS,
    "thumbnail": {"bg": "manor", "seed": 6, "creature": "ghost", "text": "GONE"},
    "shots": [{
        "bg": "manor", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
        "chars": {"odo": {"x": 700}, "moth": {"x": 820, "y": 650}},
        "creatures": {"g1": {"type": "ghost", "x": 1250, "state": "hidden", "face": -1}},
        "focus": ["odo", "g1"],
        "beats": [
            S("narr", "December 5, 1872. Sailors climb aboard the silent Mary Celeste.|5 de diciembre de 1872. Unos marineros suben al silencioso Mary Celeste.|"
              "5. Dezember 1872. Seeleute klettern auf die stille Mary Celeste.|5 décembre 1872. Des marins montent à bord du Mary Celeste silencieux.|"
              "5 dicembre 1872. Dei marinai salgono sulla silenziosa Mary Celeste.|5 de dezembro de 1872. Marinheiros sobem no silencioso Mary Celeste."),
            S("narr", "Belongings in their places. Water in the hold. And the lifeboat... gone.|Las cosas en su sitio. Agua en la bodega. Y el bote... desaparecido.|"
              "Alles an seinem Platz. Wasser im Laderaum. Und das Rettungsboot... fort.|Les affaires à leur place. De l'eau dans la cale. Et le canot... disparu.|"
              "Oggetti al loro posto. Acqua nella stiva. E la scialuppa... sparita.|Coisas no lugar. Água no porão. E o bote... sumiu."),
            {"act": "odo", "do": "scared"},
            S("odo", "Hello? Is anyone here?|¿Hola? ¿Hay alguien?|Hallo? Ist hier jemand?|Il y a quelqu'un ?|C'è qualcuno?|Olá? Tem alguém aqui?"),
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

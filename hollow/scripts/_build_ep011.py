"""Builds Hollowmere EP11 (true story: the Carroll A. Deering, five-masted schooner built 1919 in Bath, Maine;
hailed the Cape Lookout lightship in late January 1921 - a red-haired man with a foreign accent said they had lost
their anchors; found aground with all sails set on Diamond Shoals off Cape Hatteras at dawn, 31 January 1921, by
surfman C. P. Brady; boarded 4 February: crew, lifeboats, log, navigation gear and personal things gone, food being
prepared in the galley; dynamited in March 1921; bottle note found by Christopher Columbus Gray in April - later
shown to be a fake; theories: pirates, mutiny, rum-runners, storms; the bell is in the Graveyard of the Atlantic
Museum). Sources disagree on the lightship date (28 or 29 Jan) -> told as "two days before".
Run: python3 scripts/_build_ep011.py
Retention rules (2026-10-16): frame 1 = motion + big text hook, narration from 0 s mid-tension, something new every
4-6 s, long ends on a cliffhanger, Short 15-25 s with one scare and a loop back to the first frame.
Pack 1 of 2026-10-20 -> 1 long + 2 Shorts. No one is accused: mutiny is told only as one of the theories."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    assert len(parts[0].split()) <= 16, parts[0]
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


A = {"and": True}
TAGS = ["true story", "unsolved mystery", "real horror story", "ghost ship", "Carroll A. Deering", "Cape Hatteras",
        "Outer Banks", "North Carolina", "Diamond Shoals", "Graveyard of the Atlantic", "1921", "horror animation",
        "scary stories", "hollowmere"]
SOURCES = ["https://www.nps.gov/caha/learn/historyculture/theghostship.htm",
           "https://www.dncr.nc.gov/blog/2016/01/31/carroll-deering-ghost-ship",
           "https://en.wikipedia.org/wiki/Carroll_A._Deering"]

MAN = lambda x=1400, sd=1, sc=0.95: {"type": "figure", "x": x, "seed": sd, "face": -1, "state": "hidden", "scale": sc}
GHOST = lambda x=1450, sc=0.8: {"type": "ghost", "x": x, "state": "hidden", "face": -1, "scale": sc}
SHIP = lambda x=1450, y=680, sc=0.6: {"type": "ship", "x": x, "y": y, "state": "hidden", "face": -1, "scale": sc}
CROW = lambda x=1250, y=330: {"type": "crow", "x": x, "y": y, "state": "hidden", "fly": 1}
MOON = [{"kind": "moon", "x": 1450, "y": 220, "r": 900}]

long_ = {
    "id": "ep011_long", "format": "long",
    "title": "Why Was This Ship Found With No Crew?",
    "hook": "NO ONE WAS ABOARD", "hook_dur": 4.5,
    "description": ("A true story from the Outer Banks of North Carolina, 1921. The Carroll A. Deering was a huge five-masted "
                    "schooner, built in 1919 in Bath, Maine. Coming home from Brazil in January 1921, she passed the Cape Lookout "
                    "lightship, and a red-haired man with a foreign accent shouted that the ship had lost her anchors. "
                    "Two days later, at dawn on 31 January 1921, a Coast Guard surfman saw her stuck on Diamond Shoals off "
                    "Cape Hatteras — every sail set, and no one on deck. When rescuers finally climbed aboard on 4 February, "
                    "the crew, both lifeboats, the logbook, the navigation instruments and the sailors' belongings were gone, "
                    "and food had been left in the galley. A note in a bottle blaming pirates was later shown to be a fake. "
                    "Pirates, mutiny, rum-runners and storms have all been suggested. No one knows what happened to the crew.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #ghostship #outerbanks #capehatteras #1921 #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 11", "Cape Lookout lightship", "schooner", "ghost ship mystery", "true story history"],
    "thumbnail": {"bg": "sea", "seed": 3, "creature": "ghost", "text": "NO ONE ABOARD"},
    "shots": [
        {   # 1 cold open: the empty ship on the shoals, motion + hook from frame 1
            "bg": "sea", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 0, "lantern": 1.0, "ambient": 0.38, "fade": False,
            "lights": MOON,
            "cam": {"from": [900, 600, 1.22], "to": [1080, 610, 1.08]},
            "chars": {"odo": {"x": 380}, "moth": {"x": 520, "y": 650}},
            "creatures": {"sh": SHIP(1450, 670, 0.7), "g1": GHOST(1300, 0.7)},
            "beats": [
                {"show": "sh", "dur": 0.05},
                {"flash": True, "dur": 0.8, **A},
                {"move": "odo", "to": 620, "speed": "creep", **A},
                {"move": "moth", "to": 760, "speed": "creep", **A},
                {"sfx": "whoosh", **A},
                S("narr", "Every sail was up. Dinner was on the stove. So where was the crew?|Todas las velas izadas. La cena en el fogón. ¿Y dónde estaba la tripulación?|"
                  "Alle Segel gesetzt. Das Essen auf dem Herd. Wo war die Mannschaft?|Toutes voiles dehors. Le dîner sur le feu. Mais où était l'équipage ?|"
                  "Tutte le vele issate. La cena sul fuoco. Dov'era l'equipaggio?|Todas as velas içadas. O jantar no fogão. Onde estava a tripulação?", **A),
                {"shake": 0.5, "power": 10, **A},
                {"sfx": "creak"},
                S("narr", "This is a true story from North Carolina, in the winter of 1921.|Esta es una historia real de Carolina del Norte, del invierno de 1921.|"
                  "Dies ist eine wahre Geschichte aus North Carolina, Winter 1921.|Ceci est une histoire vraie de Caroline du Nord, hiver 1921.|"
                  "Questa è una storia vera della Carolina del Nord, inverno 1921.|Esta é uma história real da Carolina do Norte, inverno de 1921."),
                {"show": "g1", "dur": 0.2, **A},
                {"flash": True, "dur": 1.0},
                {"hide": "g1", "dur": 0.2, **A},
                {"act": "odo", "do": "scared"},
                S("odo", "Mothwick... somebody waved from that ship. I saw a hand!|Mothwick... alguien saludó desde ese barco. ¡Vi una mano!|"
                  "Mothwick... jemand hat von dem Schiff gewinkt. Ich sah eine Hand!|Mothwick... quelqu'un a fait signe du bateau. J'ai vu une main !|"
                  "Mothwick... qualcuno ha salutato da quella nave. Ho visto una mano!|Mothwick... alguém acenou daquele navio. Eu vi uma mão!"),
                {"sfx": "bell", **A},
                S("moth", "Then don't wave back, Odo. That ship has been empty for days.|Entonces no devuelvas el saludo, Odo. Ese barco lleva días vacío.|"
                  "Dann wink nicht zurück, Odo. Das Schiff ist seit Tagen leer.|Alors ne réponds pas, Odo. Ce bateau est vide depuis des jours.|"
                  "Allora non rispondere, Odo. Quella nave è vuota da giorni.|Então não acene de volta, Odo. Esse navio está vazio há dias."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.2,
        },
        {   # 2 the ship and the voyage
            "bg": "sea", "seed": 1, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": MOON,
            "cam": {"from": [880, 600, 1.12], "to": [1040, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"sh": SHIP(1400, 680, 0.55), "c1": CROW()},
            "beats": [
                S("narr", "Her name was the Carroll A. Deering. Five masts, built in Maine in 1919.|Se llamaba Carroll A. Deering. Cinco mástiles, construido en Maine en 1919.|"
                  "Sie hieß Carroll A. Deering. Fünf Masten, 1919 in Maine gebaut.|Il s'appelait le Carroll A. Deering. Cinq mâts, construit dans le Maine en 1919.|"
                  "Si chiamava Carroll A. Deering. Cinque alberi, costruita nel Maine nel 1919.|Chamava-se Carroll A. Deering. Cinco mastros, construído no Maine em 1919."),
                {"show": "sh", "dur": 0.6, **A},
                {"sfx": "creak", **A},
                {"move": "sh", "to": 1250, "speed": "walk"},
                S("narr", "One of the last great wooden sailing ships of America.|Uno de los últimos grandes veleros de madera de América.|"
                  "Eines der letzten großen hölzernen Segelschiffe Amerikas.|L'un des derniers grands voiliers en bois d'Amérique.|"
                  "Uno degli ultimi grandi velieri di legno d'America.|Um dos últimos grandes veleiros de madeira da América.", **A),
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "In 1920 she carried coal from Virginia all the way to Rio de Janeiro.|En 1920 llevó carbón desde Virginia hasta Río de Janeiro.|"
                  "1920 brachte sie Kohle von Virginia bis nach Rio de Janeiro.|En 1920, il porta du charbon de Virginie jusqu'à Rio de Janeiro.|"
                  "Nel 1920 portò carbone dalla Virginia fino a Rio de Janeiro.|Em 1920 levou carvão da Virgínia até o Rio de Janeiro.", **A),
                {"flash": True, "dur": 1.0},
                S("narr", "Her captain fell ill, so a new captain took her: Willis Wormell.|Su capitán enfermó, así que la tomó otro: Willis Wormell.|"
                  "Ihr Kapitän wurde krank, ein neuer übernahm: Willis Wormell.|Son capitaine tomba malade ; un autre le remplaça : Willis Wormell.|"
                  "Il capitano si ammalò, e ne prese il posto un altro: Willis Wormell.|O capitão adoeceu, e outro assumiu: Willis Wormell.", **A),
                {"act": "odo", "do": "shake"},
                S("odo", "So they made it to Brazil? Then what went wrong?|¿Entonces llegaron a Brasil? ¿Y qué salió mal?|"
                  "Sie kamen also bis Brasilien? Was ging dann schief?|Ils sont arrivés au Brésil ? Alors, qu'est-ce qui a mal tourné ?|"
                  "Quindi arrivarono in Brasile? Cosa andò storto?|Então chegaram ao Brasil? O que deu errado?"),
                {"move": "sh", "to": 1450, "speed": "walk", **A},
                S("moth", "Nothing, yet. The trouble began on the way home.|Nada, todavía. El problema empezó en el viaje de vuelta.|"
                  "Noch nichts. Der Ärger begann auf dem Heimweg.|Rien, encore. Les ennuis ont commencé au retour.|"
                  "Niente, ancora. I guai iniziarono sulla via del ritorno.|Nada, ainda. O problema começou na volta."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 3 the lightship and the red-haired man
            "bg": "lighthouse", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
            "lights": [{"kind": "window", "x": 1250, "y": 600, "r": 520}],
            "cam": {"from": [960, 600, 1.1], "to": [1080, 600, 1.22]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "creatures": {"jac": MAN(1200, 0, 0.95), "red": MAN(1480, 1, 1.0), "sh": SHIP(1500, 690, 0.45)},
            "beats": [
                {"move": "odo", "to": 560, "speed": "creep"},
                {"move": "moth", "to": 720, "speed": "creep", **A},
                S("narr", "Late in January 1921, she sailed past the Cape Lookout lightship.|A finales de enero de 1921, pasó junto al buque faro de Cape Lookout.|"
                  "Ende Januar 1921 segelte sie am Feuerschiff von Cape Lookout vorbei.|Fin janvier 1921, il passa près du bateau-phare de Cape Lookout.|"
                  "A fine gennaio 1921 passò accanto alla nave faro di Cape Lookout.|No fim de janeiro de 1921, passou pelo navio-farol de Cape Lookout.", **A),
                {"show": "sh", "dur": 0.4},
                {"show": "jac", "dur": 0.4, **A},
                {"flash": True, "dur": 1.0},
                S("narr", "A man on deck shouted through a megaphone. He had red hair.|Un hombre en cubierta gritó por un megáfono. Tenía el pelo rojo.|"
                  "Ein Mann an Deck rief durch ein Sprachrohr. Er hatte rote Haare.|Un homme sur le pont cria dans un porte-voix. Il était roux.|"
                  "Un uomo sul ponte gridò con un megafono. Aveva i capelli rossi.|Um homem no convés gritou por um megafone. Tinha cabelo ruivo.", **A),
                {"show": "red", "dur": 0.3},
                {"sfx": "whoosh", **A},
                {"move": "red", "to": 1400, "speed": "walk", **A},
                S("red", "We lost our anchors in a storm! Tell our owners!|¡Perdimos las anclas en una tormenta! ¡Avisen a los dueños!|"
                  "Wir haben im Sturm die Anker verloren! Sagt es den Eignern!|On a perdu nos ancres dans la tempête ! Prévenez les armateurs !|"
                  "Abbiamo perso le ancore in una tempesta! Avvisate gli armatori!|Perdemos as âncoras numa tempestade! Avisem os donos!"),
                {"shake": 0.6, "power": 12, **A},
                S("narr", "The keeper said the man did not look or act like an officer.|El guardián dijo que aquel hombre no parecía ni actuaba como un oficial.|"
                  "Der Wärter sagte, der Mann sah nicht aus wie ein Offizier.|Le gardien dit que l'homme n'avait rien d'un officier.|"
                  "Il guardiano disse che quell'uomo non sembrava affatto un ufficiale.|O guarda disse que o homem não parecia nem agia como oficial."),
                {"sfx": "step", **A},
                S("narr", "And the captain was nowhere to be seen.|Y al capitán no se le veía por ninguna parte.|"
                  "Und vom Kapitän keine Spur.|Et le capitaine était introuvable.|"
                  "E del capitano nessuna traccia.|E do capitão, nem sinal."),
                {"hide": "red", "dur": 0.3, **A},
                {"act": "odo", "do": "jump"},
                S("odo", "Why didn't the keeper call for help on the radio?|¿Por qué el guardián no pidió ayuda por radio?|"
                  "Warum hat der Wärter nicht per Funk Hilfe gerufen?|Pourquoi le gardien n'a pas appelé à l'aide par radio ?|"
                  "Perché il guardiano non chiamò aiuto via radio?|Por que o guarda não pediu ajuda pelo rádio?"),
                {"hide": "jac", "dur": 0.3, **A},
                S("moth", "His radio was broken. Nobody heard the message.|Su radio estaba rota. Nadie oyó el mensaje.|"
                  "Sein Funkgerät war kaputt. Niemand hörte die Nachricht.|Sa radio était cassée. Personne n'a reçu le message.|"
                  "La sua radio era rotta. Nessuno sentì il messaggio.|O rádio dele estava quebrado. Ninguém ouviu a mensagem."),
                {"sfx": "sting", **A},
                {"hide": "sh", "dur": 0.4, **A},
            ],
            "tail": 0.3,
        },
        {   # 4 dawn, 31 January: aground on Diamond Shoals
            "bg": "sea", "seed": 4, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.44,
            "lights": MOON,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 610, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 650}},
            "creatures": {"sh": SHIP(1420, 680, 0.7), "c1": CROW(1300, 320)},
            "beats": [
                S("narr", "Two days later, at dawn on the 31st of January, a surfman looked out.|Dos días después, al amanecer del 31 de enero, un vigía miró al mar.|"
                  "Zwei Tage später, im Morgengrauen des 31. Januar, blickte ein Wachmann hinaus.|Deux jours plus tard, à l'aube du 31 janvier, un sauveteur regarda la mer.|"
                  "Due giorni dopo, all'alba del 31 gennaio, una vedetta guardò il mare.|Dois dias depois, ao amanhecer de 31 de janeiro, um vigia olhou o mar."),
                {"sfx": "bell", **A},
                {"light": "flare"},
                {"show": "sh", "dur": 0.4, **A},
                S("narr", "The Deering was stuck fast on Diamond Shoals, off Cape Hatteras.|El Deering estaba encallado en los bajíos de Diamond Shoals, frente a Cabo Hatteras.|"
                  "Die Deering saß fest auf den Diamond Shoals vor Cape Hatteras.|Le Deering était échoué sur les hauts-fonds de Diamond Shoals, au large du cap Hatteras.|"
                  "La Deering era incagliata sulle secche di Diamond Shoals, al largo di Capo Hatteras.|O Deering estava encalhado nos baixios de Diamond Shoals, perto do Cabo Hatteras.", **A),
                {"shake": 0.7, "power": 14, **A},
                {"flash": True, "dur": 1.0},
                S("narr", "Sailors call these waters the Graveyard of the Atlantic.|Los marinos llaman a estas aguas el Cementerio del Atlántico.|"
                  "Seeleute nennen diese Gewässer den Friedhof des Atlantiks.|Les marins appellent ces eaux le Cimetière de l'Atlantique.|"
                  "I marinai chiamano queste acque il Cimitero dell'Atlantico.|Os marinheiros chamam estas águas de Cemitério do Atlântico.", **A),
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "Her sails were all set. Waves broke over her deck. No one was in sight.|Velas izadas. Olas sobre la cubierta. Nadie a la vista.|"
                  "Alle Segel gesetzt. Wellen über Deck. Niemand zu sehen.|Toutes voiles dehors. Des vagues sur le pont. Personne en vue.|"
                  "Vele tutte issate. Onde sul ponte. Nessuno in vista.|Velas içadas. Ondas no convés. Ninguém à vista."),
                {"sfx": "creak", **A},
                S("narr", "The sea was so rough that no boat could reach her for four days.|El mar estaba tan bravo que ningún bote llegó en cuatro días.|"
                  "Die See war so rau, dass vier Tage kein Boot hinkam.|La mer était si forte qu'aucun bateau ne l'atteignit pendant quatre jours.|"
                  "Il mare era così mosso che nessuna barca la raggiunse per quattro giorni.|O mar estava tão bravo que nenhum barco chegou lá por quatro dias."),
                {"act": "odo", "do": "scared"},
                S("odo", "Four days? Someone could still be hiding on board!|¿Cuatro días? ¡Alguien podría seguir escondido a bordo!|"
                  "Vier Tage? Da könnte sich noch jemand an Bord verstecken!|Quatre jours ? Quelqu'un pourrait encore se cacher à bord !|"
                  "Quattro giorni? Qualcuno potrebbe ancora nascondersi a bordo!|Quatro dias? Alguém ainda podia estar escondido a bordo!"),
                {"light": "dim"},
                S("moth", "That's what the rescuers hoped too, Odo.|Eso esperaban también los rescatadores, Odo.|"
                  "Das hofften die Retter auch, Odo.|C'est ce qu'espéraient aussi les sauveteurs, Odo.|"
                  "È quello che speravano anche i soccorritori, Odo.|Era o que os resgatadores esperavam também, Odo."),
                {"sfx": "sting", **A},
            ],
            "tail": 0.3,
        },
        {   # 5 4 February: on board
            "bg": "sea", "seed": 5, "music": "choir", "wind": True, "eyes": 2, "ambient": 0.36,
            "lights": [{"kind": "fire", "x": 1250, "y": 900, "r": 520}],
            "cam": {"from": [960, 600, 1.12], "to": [880, 620, 1.2]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"cap": MAN(1450, 0, 1.0), "g1": GHOST(1300)},
            "beats": [
                S("narr", "On the 4th of February, a salvage captain finally climbed aboard.|El 4 de febrero, un capitán de rescate subió por fin a bordo.|"
                  "Am 4. Februar kletterte endlich ein Bergungskapitän an Bord.|Le 4 février, un capitaine de sauvetage monta enfin à bord.|"
                  "Il 4 febbraio, un capitano di recupero salì finalmente a bordo.|Em 4 de fevereiro, um capitão de resgate enfim subiu a bordo."),
                {"show": "cap", "dur": 0.6, **A},
                {"sfx": "step", "wait": 0.3},
                {"move": "cap", "to": 1350, "speed": "creep", **A},
                S("narr", "Both lifeboats were gone. So was the logbook.|Los dos botes salvavidas no estaban. Ni el cuaderno de bitácora.|"
                  "Beide Rettungsboote waren weg. Auch das Logbuch.|Les deux canots avaient disparu. Le journal de bord aussi.|"
                  "Entrambe le scialuppe erano sparite. Anche il giornale di bordo.|Os dois botes salva-vidas tinham sumido. O diário de bordo também.", **A),
                {"flash": True, "dur": 1.0},
                S("narr", "The navigation tools, the sailors' clothes and bags: all gone.|Los instrumentos, la ropa y las bolsas de los marinos: todo había desaparecido.|"
                  "Navigationsgeräte, Kleidung, Seesäcke der Matrosen: alles weg.|Instruments de navigation, vêtements, sacs des marins : tout avait disparu.|"
                  "Strumenti di navigazione, vestiti e sacche dei marinai: tutto sparito.|Instrumentos, roupas e sacolas dos marinheiros: tudo sumido.", **A),
                {"sfx": "creak", **A},
                {"shake": 0.4, "power": 8},
                S("narr", "The wheel was smashed. The rudder had come loose.|El timón estaba destrozado. La pala del timón, suelta.|"
                  "Das Steuerrad war zertrümmert. Das Ruder hatte sich gelöst.|La barre était brisée. Le gouvernail s'était détaché.|"
                  "La ruota del timone era distrutta. Il timone si era staccato.|O leme estava destruído. A porta do leme, solta.", **A),
                {"light": "flare"},
                S("narr", "But in the galley, food had been left out, as if for the next meal.|Pero en la cocina había comida preparada, como para la próxima comida.|"
                  "Doch in der Kombüse lag Essen bereit, wie für die nächste Mahlzeit.|Mais dans la cuisine, des vivres attendaient, comme pour le prochain repas.|"
                  "Ma in cambusa c'era cibo pronto, come per il pasto seguente.|Mas na cozinha havia comida separada, como para a próxima refeição."),
                {"sfx": "whisper", **A},
                {"hide": "cap", "dur": 0.5},
                {"light": "dim", **A},
                {"show": "g1", "dur": 0.4},
                {"act": "odo", "do": "hide"},
                S("odo", "Then who is sitting at that table in the dark?|¿Entonces quién está sentado a esa mesa en la oscuridad?|"
                  "Wer sitzt dann im Dunkeln an diesem Tisch?|Alors qui est assis à cette table dans le noir ?|"
                  "Allora chi è seduto a quel tavolo nel buio?|Então quem está sentado naquela mesa no escuro?"),
                {"growl": "g1", **A},
                {"lunge": "g1", "to": 1100},
                {"hide": "g1", "dur": 0.2},
                {"light": "on", **A},
                {"act": "odo", "do": "unhide"},
                S("moth", "No one, Odo. Just the wind... and an empty chair.|Nadie, Odo. Solo el viento... y una silla vacía.|"
                  "Niemand, Odo. Nur der Wind... und ein leerer Stuhl.|Personne, Odo. Juste le vent... et une chaise vide.|"
                  "Nessuno, Odo. Solo il vento... e una sedia vuota.|Ninguém, Odo. Só o vento... e uma cadeira vazia."),
            ],
            "tail": 0.3,
        },
        {   # 6 the bottle, the theories, the dynamite
            "bg": "lighthouse", "seed": 3, "music": "drone", "wind": True, "eyes": 2, "ambient": 0.40,
            "lights": MOON,
            "cam": {"from": [960, 600, 1.12], "to": [1060, 620, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"fis": MAN(1400, 2, 0.95), "c1": CROW(1250, 320), "sh": SHIP(1500, 690, 0.45)},
            "beats": [
                S("narr", "In April, a local man said he found a bottle on the beach.|En abril, un hombre del lugar dijo haber hallado una botella en la playa.|"
                  "Im April sagte ein Mann, er habe am Strand eine Flasche gefunden.|En avril, un homme du coin dit avoir trouvé une bouteille sur la plage.|"
                  "Ad aprile, un uomo del posto disse di aver trovato una bottiglia sulla spiaggia.|Em abril, um morador disse ter achado uma garrafa na praia."),
                {"show": "fis", "dur": 0.5, **A},
                {"flash": True, "dur": 1.0},
                S("narr", "Inside, a note: the Deering had been captured by pirates.|Dentro, una nota: piratas habían capturado el Deering.|"
                  "Darin ein Zettel: Piraten hätten die Deering gekapert.|Dedans, un mot : des pirates avaient capturé le Deering.|"
                  "Dentro, un biglietto: dei pirati avevano catturato la Deering.|Dentro, um bilhete: piratas tinham capturado o Deering.", **A),
                {"sfx": "snap", **A},
                {"show": "c1", "dur": 0.2},
                {"sfx": "caw", **A},
                {"hide": "c1", "dur": 0.4},
                S("narr", "Months later, the note was shown to be a fake.|Meses después, se demostró que la nota era falsa.|"
                  "Monate später stellte sich der Zettel als Fälschung heraus.|Des mois plus tard, le mot se révéla être un faux.|"
                  "Mesi dopo, si scoprì che il biglietto era falso.|Meses depois, provaram que o bilhete era falso."),
                {"hide": "fis", "dur": 0.4, **A},
                {"shake": 0.5, "power": 10, **A},
                S("narr", "U.S. government agents came to investigate. They found no answer.|Agentes del gobierno de EE. UU. investigaron. No hallaron respuesta.|"
                  "US-Regierungsagenten ermittelten. Sie fanden keine Antwort.|Des agents du gouvernement américain enquêtèrent. Sans réponse.|"
                  "Agenti del governo USA indagarono. Non trovarono risposte.|Agentes do governo dos EUA investigaram. Não acharam resposta.", **A),
                {"show": "sh", "dur": 0.4},
                S("narr", "Pirates? Mutiny? Rum smugglers? A storm? Every idea has holes.|¿Piratas? ¿Motín? ¿Contrabandistas de ron? ¿Una tormenta? Ninguna idea encaja.|"
                  "Piraten? Meuterei? Rumschmuggler? Ein Sturm? Jede Idee hat Lücken.|Des pirates ? Une mutinerie ? Des contrebandiers ? Une tempête ? Rien ne colle.|"
                  "Pirati? Ammutinamento? Contrabbandieri di rum? Una tempesta? Ogni idea ha buchi.|Piratas? Motim? Contrabandistas de rum? Uma tempestade? Nada fecha."),
                {"sfx": "whoosh", **A},
                {"act": "odo", "do": "calm"},
                S("narr", "In March 1921, the wreck was blown apart with dynamite.|En marzo de 1921, volaron el casco con dinamita.|"
                  "Im März 1921 wurde das Wrack mit Dynamit gesprengt.|En mars 1921, l'épave fut détruite à la dynamite.|"
                  "Nel marzo 1921 il relitto fu fatto saltare con la dinamite.|Em março de 1921, o casco foi explodido com dinamite."),
                {"flash": True, "dur": 1.2},
                {"hide": "sh", "dur": 0.2, **A},
                {"shake": 0.8, "power": 18, **A},
                S("odo", "So nothing is left? No ship, no crew, no answer?|¿Entonces no queda nada? ¿Ni barco, ni tripulación, ni respuesta?|"
                  "Also ist nichts mehr übrig? Kein Schiff, keine Mannschaft, keine Antwort?|Il ne reste rien ? Ni bateau, ni équipage, ni réponse ?|"
                  "Quindi non resta niente? Né nave, né equipaggio, né risposta?|Então não sobrou nada? Nem navio, nem tripulação, nem resposta?"),
                {"light": "flare"},
                S("moth", "One thing is left, Odo. Her bell. It sits in a museum on Hatteras.|Queda una cosa, Odo. Su campana. Está en un museo de Hatteras.|"
                  "Eines blieb, Odo. Ihre Glocke. Sie steht in einem Museum auf Hatteras.|Il reste une chose, Odo. Sa cloche. Elle est dans un musée à Hatteras.|"
                  "Resta una cosa, Odo. La sua campana. È in un museo a Hatteras.|Restou uma coisa, Odo. O sino dele. Está num museu em Hatteras."),
                {"sfx": "bell", **A},
            ],
            "tail": 0.3,
        },
        {   # 7 cliffhanger: the bell rings by itself
            "bg": "sea", "seed": 3, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.36,
            "lights": MOON,
            "cam": {"from": [900, 600, 1.12], "to": [1120, 640, 1.25]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"sh": SHIP(1450, 670, 0.7), "red": MAN(1450, 1, 1.05)},
            "beats": [
                S("narr", "The crew of the Carroll A. Deering was never found.|La tripulación del Carroll A. Deering nunca apareció.|"
                  "Die Mannschaft der Carroll A. Deering wurde nie gefunden.|L'équipage du Carroll A. Deering ne fut jamais retrouvé.|"
                  "L'equipaggio della Carroll A. Deering non fu mai ritrovato.|A tripulação do Carroll A. Deering nunca foi encontrada."),
                {"sfx": "whoosh", **A},
                S("narr", "Not one of them. And no one knows who the red-haired man was.|Ni uno solo. Y nadie sabe quién era el hombre pelirrojo.|"
                  "Kein Einziger. Und niemand weiß, wer der rothaarige Mann war.|Pas un seul. Et personne ne sait qui était l'homme roux.|"
                  "Nemmeno uno. E nessuno sa chi fosse l'uomo dai capelli rossi.|Nem um só. E ninguém sabe quem era o homem ruivo."),
                {"show": "sh", "dur": 0.3},
                {"sfx": "bell", "wait": 0.3},
                S("odo", "Mothwick... do you hear a bell? Out there, on the water...|Mothwick... ¿oyes una campana? Ahí fuera, en el agua...|"
                  "Mothwick... hörst du eine Glocke? Da draußen, auf dem Wasser...|Mothwick... tu entends une cloche ? Là-bas, sur l'eau...|"
                  "Mothwick... senti una campana? Là fuori, sull'acqua...|Mothwick... está ouvindo um sino? Lá fora, na água..."),
                {"eyes": "open", **A},
                {"sfx": "bell", "wait": 0.3},
                {"flash": True, "dur": 1.0},
                {"eyes": "close"},
                {"act": "odo", "do": "turn"},
                S("moth", "That bell is in a museum, Odo... so who is ringing it?|Esa campana está en un museo, Odo... ¿entonces quién la toca?|"
                  "Die Glocke steht im Museum, Odo... wer läutet sie dann?|Cette cloche est dans un musée, Odo... alors qui la sonne ?|"
                  "Quella campana è in un museo, Odo... allora chi la suona?|Esse sino está num museu, Odo... então quem está tocando?"),
                {"sfx": "step", "wait": 0.4},
                {"show": "red", "dur": 0.3},
                S("red", "We lost our anchors! Tell our owners!|¡Perdimos las anclas! ¡Avisen a los dueños!|"
                  "Wir haben die Anker verloren! Sagt es den Eignern!|On a perdu nos ancres ! Prévenez les armateurs !|"
                  "Abbiamo perso le ancore! Avvisate gli armatori!|Perdemos as âncoras! Avisem os donos!", **A),
                {"growl": "red"},
                {"lunge": "red", "to": 1150},
                {"light": "out", **A},
                {"card": "WHO WAS ON DECK?", "dur": 2.4},
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

# Shorts: hard cuts + flashes -> something new every 2-4 s; one scare; the last shot repeats shot 1's set-up
# (same bg/seed/positions, hook beat) so the final frame loops back to frame 1.
short1 = {   # the rule / scariest true detail
    "id": "ep011_short1", "format": "short",
    "title": "Who Shouted From This Ghost Ship? #shorts",
    "hook": "DON'T WAVE BACK",
    "description": "North Carolina, January 1921: a red-haired man shouted from the schooner Carroll A. Deering that she had lost her anchors. Two days later she was found on Diamond Shoals, every sail set, and no one aboard. The crew was never found. Full true story on the channel. #shorts #ghostship #outerbanks #1921 #truestory #hollowmere",
    "tags": ["shorts"] + TAGS[:11],
    "thumbnail": {"bg": "sea", "seed": 3, "creature": "ghost", "text": "NO ONE ABOARD"},
    "shots": [
        SHOT("sea", 3, [
            {"show": "red", "dur": 0.05}, {"flash": True, **A}, {"shake": 0.4, "power": 14, "and": True},
            {"move": "red", "to": 860, "speed": "walk", **A},
            S("narr", L("1921. A man on a ship shouts: we lost our anchors!", "1921. Un hombre en un barco grita: ¡perdimos las anclas!",
                        "1921. Ein Mann auf einem Schiff ruft: Anker verloren!", "1921. Un homme crie d'un bateau : on a perdu nos ancres !",
                        "1921. Un uomo su una nave grida: perse le ancore!", "1921. Um homem num navio grita: perdemos as âncoras!"), **A),
        ], odo=560, amb=0.55, lights=MOON, creatures={"red": MAN(960, 1, 0.9)}),
        SHOT("sea", 4, [
            {"show": "sh", "dur": 0.2}, {"flash": True, **A},
            S("narr", L("Two days later, the ship is found. Every sail up. No one aboard.", "Dos días después hallan el barco. Velas izadas. Nadie a bordo.",
                        "Zwei Tage später: das Schiff. Alle Segel gesetzt. Niemand an Bord.", "Deux jours après, on trouve le bateau. Voiles hautes. Personne.",
                        "Due giorni dopo, la nave. Vele issate. Nessuno a bordo.", "Dois dias depois, o navio. Velas içadas. Ninguém a bordo."), **A),
            {"shake": 0.6, "power": 12, **A},
            {"sfx": "creak"},
        ], odo=420, eyes=2, lights=MOON, creatures={"sh": SHIP(900, 700, 0.5)}),
        SHOT("sea", 5, [
            {"act": "odo", "do": "scared"},
            S("narr", L("The crew was never found. And the red-haired man?", "La tripulación nunca apareció. ¿Y el pelirrojo?",
                        "Die Mannschaft blieb verschwunden. Und der Rothaarige?", "L'équipage ne fut jamais retrouvé. Et l'homme roux ?",
                        "L'equipaggio mai ritrovato. E l'uomo dai capelli rossi?", "A tripulação nunca apareceu. E o ruivo?"), **A),
            {"sfx": "bell", **A},
            {"light": "out"},
            {"show": "red", "dur": 0.1, **A},
            {"lunge": "red", "to": 820, **A},
            {"flash": True, "and": True},
        ], odo=560, lights=[{"kind": "fire", "x": 900, "y": 900, "r": 600}], creatures={"red": MAN(950, 1, 1.0)}),
        SHOT("sea", 3, [
            {"move": "odo", "to": 560, "speed": "walk"},
            S("narr", L("So if a ship waves at you tonight...", "Así que si un barco te saluda esta noche...",
                        "Wenn dir heute Nacht ein Schiff zuwinkt...", "Alors si un bateau te fait signe ce soir...",
                        "Quindi se stanotte una nave ti saluta...", "Então, se um navio acenar pra você esta noite..."), **A),
            {"show": "red", "dur": 0.05}, {"flash": True, **A},
        ], odo=640, amb=0.55, lights=MOON, tail=0.0, creatures={"red": MAN(860, 1, 0.9)}),
    ],
}
short1["shots"][0]["focus"] = ["odo", "red"]
short1["shots"][1]["focus"] = ["odo", "sh"]
short1["shots"][2]["cam"] = {"x": 740}

short2 = {   # Would YOU...?
    "id": "ep011_short2", "format": "short",
    "title": "Would YOU Board This Ghost Ship? #shorts",
    "hook": "WOULD YOU GO ABOARD?",
    "description": "February 1921, Cape Hatteras: rescuers climbed aboard the Carroll A. Deering. Lifeboats gone, logbook gone, the crew gone, food left in the galley. Would YOU go aboard? Comment YES or NO. Full true story on the channel. #shorts #ghostship #capehatteras #truestory #hollowmere",
    "tags": ["shorts"] + TAGS[:11],
    "thumbnail": {"bg": "sea", "seed": 5, "creature": "ghost", "text": "WOULD YOU?"},
    "shots": [
        SHOT("sea", 5, [
            {"show": "g1", "dur": 0.05}, {"flash": True, **A}, {"shake": 0.4, "power": 14, **A},
            S("narr", L("The ship is empty. The lifeboats are gone.", "El barco está vacío. Los botes no están.",
                        "Das Schiff ist leer. Die Rettungsboote sind weg.", "Le bateau est vide. Les canots ont disparu.",
                        "La nave è vuota. Le scialuppe sono sparite.", "O navio está vazio. Os botes sumiram."), **A),
            {"hide": "g1", "dur": 0.3},
        ], odo=560, amb=0.5, lights=[{"kind": "fire", "x": 900, "y": 900, "r": 560}], creatures={"g1": GHOST(900, 0.75)}),
        SHOT("sea", 1, [
            {"sfx": "creak"},
            S("narr", L("But food is still waiting in the galley.", "Pero aún hay comida esperando en la cocina.",
                        "Doch in der Kombüse wartet noch Essen.", "Mais des vivres attendent encore en cuisine.",
                        "Ma in cambusa il cibo aspetta ancora.", "Mas ainda há comida esperando na cozinha."), **A),
            {"move": "odo", "to": 620, "speed": "creep", **A},
            {"flash": True},
            {"sfx": "whisper", **A},
            S("narr", L("And the ship's wheel is smashed to pieces.", "Y el timón está hecho pedazos.",
                        "Und das Steuerrad ist zertrümmert.", "Et la barre est en morceaux.",
                        "E la ruota del timone è in pezzi.", "E o leme está em pedaços."), **A),
            {"shake": 0.5, "power": 12, **A},
        ], odo=420, eyes=3, lights=WIN, creatures={}),
        SHOT("sea", 4, [
            {"act": "odo", "do": "scared"},
            S("narr", L("Would YOU climb aboard alone? Comment YES or NO.", "¿Subirías TÚ solo a bordo? Comenta SÍ o NO.",
                        "Würdest DU allein an Bord gehen? Schreib JA oder NEIN.", "Monterais-TU seul à bord ? Écris OUI ou NON.",
                        "Saliresti TU a bordo da solo? Scrivi SÌ o NO.", "VOCÊ subiria a bordo sozinho? Comente SIM ou NÃO."), **A),
            {"light": "out"},
            {"show": "g1", "dur": 0.1, **A},
            {"lunge": "g1", "to": 760, **A},
            {"flash": True, **A},
        ], odo=560, lights=MOON, creatures={"g1": GHOST(950, 0.85)}),
        SHOT("sea", 5, [
            {"move": "odo", "to": 560, "speed": "walk"},
            {"show": "g1", "dur": 0.05}, {"flash": True, **A},
        ], odo=640, amb=0.5, lights=[{"kind": "fire", "x": 900, "y": 900, "r": 560}], tail=0.4, creatures={"g1": GHOST(900, 0.75)}),
    ],
}
short2["shots"][0]["focus"] = ["odo", "g1"]
short2["shots"][2]["cam"] = {"x": 740}

for s in (long_, short1, short2):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

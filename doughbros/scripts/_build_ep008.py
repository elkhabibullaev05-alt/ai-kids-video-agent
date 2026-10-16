"""Builds the EP8 pack (1 long + 2 shorts). Run: python3 scripts/_build_ep008.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
src = (OUT / "_build_ep003.py").read_text(encoding="utf-8").split("ALL4 =")[0]
ns = {"__file__": str(OUT / "_build_ep003.py")}
exec(src, ns)
S, _mv, act, mood = ns["S"], ns["mv"], ns["act"], ns["mood"]


def mv(who, to, speed="walk", both=False):
    if isinstance(who, list):
        return [_mv(w, to, speed, both or i > 0) for i, w in enumerate(who)]
    return _mv(who, to, speed, both)


def flat(beats):
    out = []
    for b in beats:
        out.extend(b if isinstance(b, list) else [b])
    return out

LONG_TITLE = "Can 5 Dough Bros Stop THE BIG FREEZE? ❄️ | EP 8"
CHANNEL = "https://www.youtube.com/@DoughBrosTV"
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "frostbite", "big freeze", "freezer ghost"]
SHORT_TAGS = ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon",
              "horror comedy", "animated series"]

long_ = {
    "id": "ep008_long", "format": "long",
    "title": LONG_TITLE,
    "description": ("Mr. Pot left the freezer door wide open, and now it is SNOWING inside the kitchen. "
                    "Frostbite wants to turn all of Table Land into ice before sunrise. Zeek's heater explodes, "
                    "the bathroom is a skating rink, and the freezer door is too heavy to close... until Lolly gets angry. "
                    "But who is waiting in the night garden?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy"),
    "tags": TAGS + ["episode 8", "lolly", "pim", "sir stuffing"],
    "thumbnail": {"bg": "freezer", "villain": "frost", "heroes": ["pim"], "text": "FROZEN SOLID!"},
    "scenes": [
        {   # 1 cold open: it's snowing inside (hook in first 3 s)
            "bg": "kitchen", "music": "drone",
            "heroes": {"pim": 300, "bup": 560, "zeek": 820},
            "moods": {"pim": "scared", "bup": "scared", "zeek": "scared"},
            "villain": {"type": "frost", "x": 1450, "state": "awake", "scale": 0.9},
            "beats": [
                {"villain": "roar"},
                {"sfx": "ice", "wait": 0.2, "and": True},
                act(["pim", "bup", "zeek"], "scream"),
                S("pim", "Why is it SNOWING inside the kitchen?!|¡¿Por qué está NEVANDO dentro de la cocina?!|"
                  "Warum SCHNEIT es in der Küche?!|Pourquoi il NEIGE dans la cuisine ?!|"
                  "Perché NEVICA dentro la cucina?!|Por que está NEVANDO dentro da cozinha?!"),
                S("villain", "The BIG FREEZE has begun, little dough.|La GRAN HELADA ha comenzado, masita.|"
                  "Der GROSSE FROST hat begonnen, kleiner Teig.|Le GRAND GEL a commencé, petite pâte.|"
                  "Il GRANDE GELO è cominciato, piccola pasta.|O GRANDE CONGELAMENTO começou, massinha."),
                S("villain", "Mr. Pot opened my door wide. By sunrise, all of Table Land is ice.|"
                  "El Señor Olla abrió mi puerta. Al amanecer, toda la Tierra de la Mesa será hielo.|"
                  "Herr Topf hat meine Tür geöffnet. Bei Sonnenaufgang ist das ganze Tischland Eis.|"
                  "Monsieur Marmite a ouvert ma porte. À l'aube, tout le Pays de la Table sera glace.|"
                  "Il Signor Pentola ha aperto la mia porta. All'alba, tutta la Terra del Tavolo sarà ghiaccio.|"
                  "O Senhor Panela abriu minha porta. Ao amanhecer, toda a Terra da Mesa vira gelo."),
                act("pim", "shake"),
                S("zeek", "My calculations say we have until sunrise. About four hours.|Mis cálculos dicen que tenemos hasta el amanecer. Unas cuatro horas.|"
                  "Laut meinen Berechnungen bleibt uns bis Sonnenaufgang. Etwa vier Stunden.|Selon mes calculs, on a jusqu'à l'aube. Environ quatre heures.|"
                  "I miei calcoli dicono che abbiamo fino all'alba. Circa quattro ore.|Meus cálculos dizem que temos até o amanhecer. Umas quatro horas."),
                mood("bup", "angry"),
                S("bup", "Okay team, here's the plan. We close that freezer door. Tonight.|Bien, equipo, este es el plan. Cerramos esa puerta del congelador. Esta noche.|"
                  "Okay, Team, hier ist der Plan. Wir schließen die Gefriertür. Heute Nacht.|OK l'équipe, voici le plan. On ferme la porte du congélateur. Cette nuit.|"
                  "Ok squadra, ecco il piano. Chiudiamo la porta del congelatore. Stanotte.|Certo, equipe, o plano é esse. Fechamos a porta do freezer. Hoje à noite."),
                S("villain", "Stay... forever... cold...|Quédense... para siempre... fríos...|Bleibt... für immer... kalt...|"
                  "Restez... pour toujours... froids...|Restate... per sempre... freddi...|Fiquem... para sempre... frios..."),
                {"villain": "hide"},
                {"sfx": "whoosh", "wait": 0.3, "and": True},
                mv("pim", "off_left", "run"),
                S("bup", "Pim! The door is THAT way!|¡Pim! ¡La puerta está POR ALLÁ!|Pim! Die Tür ist DA lang!|"
                  "Pim ! La porte, c'est PAR LÀ !|Pim! La porta è DI LÀ!|Pim! A porta é PRA LÁ!"),
            ],
            "tail": 0.5,
        },
        {   # 2 table: Zeek's heater fails, Crispy joins
            "bg": "table", "music": "music_box",
            "heroes": {"zeek": 620, "lolly": 360, "bup": 880, "crispy": 2200},
            "beats": [
                {"card": "THE TABLE, 2 A.M.", "es": "LA MESA, 2 A.M.", "dur": 2.0},
                S("zeek", "Behold! The Defrost-o-Tron Nine Thousand! A straw, a match, and courage.|¡Contemplen! ¡El Descongela-Tron Nueve Mil! Una pajita, un fósforo y valor.|"
                  "Seht her! Der Auftau-o-Tron Neuntausend! Ein Strohhalm, ein Streichholz und Mut.|Voici le Dégivro-Tron Neuf Mille ! Une paille, une allumette et du courage.|"
                  "Ecco il Disgela-Tron Novemila! Una cannuccia, un fiammifero e coraggio.|Contemplem! O Descongela-Tron Nove Mil! Um canudo, um fósforo e coragem."),
                {"sfx": "clank", "wait": 0.4},
                {"sfx": "pop", "wait": 0.3},
                {"shake": 0.4, "power": 12, "and": True},
                act("zeek", "jump"),
                S("zeek", "...It made it colder. Fascinating. And terrible.|...Lo hizo más frío. Fascinante. Y terrible.|"
                  "...Es ist jetzt kälter. Faszinierend. Und furchtbar.|...Il fait encore plus froid. Fascinant. Et terrible.|"
                  "...Ha fatto ancora più freddo. Affascinante. E terribile.|...Ficou mais frio. Fascinante. E terrível."),
                S("lolly", "We need something warm. Something really, really warm!|¡Necesitamos algo caliente! ¡Algo muy, muy caliente!|"
                  "Wir brauchen etwas Warmes. Etwas richtig, richtig Warmes!|Il nous faut quelque chose de chaud. De vraiment, vraiment chaud !|"
                  "Ci serve qualcosa di caldo. Qualcosa di davvero, davvero caldo!|Precisamos de algo quente. Algo muito, muito quente!"),
                {"sfx": "creak", "wait": 0.4},
                mv("crispy", 1200, "walk"),
                act(["lolly", "zeek", "bup"], "jump"),
                S("crispy", "You called...?|¿Me llamaron...?|Ihr habt gerufen...?|Vous m'avez appelé... ?|Mi avete chiamato...?|Vocês chamaram...?"),
                S("bup", "Crispy! How do you always DO that?|¡Crispy! ¿Cómo HACES siempre eso?|Crispy! Wie MACHST du das immer?|"
                  "Crispy ! Comment tu FAIS ça à chaque fois ?|Crispy! Come FAI ogni volta?|Crispy! Como você SEMPRE FAZ isso?"),
                S("crispy", "Old Hissy relit my ember. It is small... but it is enough to lead you.|El Viejo Hissy encendió mi brasa. Es pequeña... pero basta para guiarlos.|"
                  "Der alte Hissy hat meine Glut neu entfacht. Sie ist klein... aber sie reicht, um euch zu führen.|Le Vieux Hissy a rallumé ma braise. Elle est petite... mais assez pour vous guider.|"
                  "Il Vecchio Hissy ha riacceso la mia brace. È piccola... ma basta per guidarvi.|O Velho Hissy reacendeu minha brasa. É pequena... mas basta para guiar vocês."),
                S("crispy", "The cold comes through the pipes. We go through the bathroom.|El frío viene por las tuberías. Iremos por el baño.|"
                  "Die Kälte kommt durch die Rohre. Wir gehen durchs Badezimmer.|Le froid passe par les tuyaux. On passe par la salle de bain.|"
                  "Il freddo arriva dai tubi. Passiamo dal bagno.|O frio vem pelos canos. Vamos pelo banheiro."),
                mood("lolly", "happy"),
                S("lolly", "And where is Pim?|¿Y dónde está Pim?|Und wo ist Pim?|Et où est Pim ?|E dov'è Pim?|E cadê o Pim?"),
                mv(["bup", "zeek", "lolly", "crispy"], "off_right", "run"),
            ],
            "tail": 0.4,
        },
        {   # 3 bathroom: skating rink + Frostbite's offer
            "bg": "bathroom", "music": "heartbeat",
            "heroes": {"pim": 900, "bup": -200, "lolly": -400, "zeek": -600, "crispy": -800},
            "moods": {"pim": "scared"},
            "villain": {"type": "frost", "x": 1500, "state": "hidden", "scale": 0.85},
            "beats": [
                act("pim", "spin"),
                {"sfx": "ice", "wait": 0.2, "and": True},
                S("pim", "Help! The floor is ICE! I can't STOP!|¡Ayuda! ¡El suelo es HIELO! ¡No puedo PARAR!|Hilfe! Der Boden ist EIS! Ich kann nicht ANHALTEN!|"
                  "Au secours ! Le sol, c'est de la GLACE ! Je ne peux pas M'ARRÊTER !|Aiuto! Il pavimento è GHIACCIO! Non riesco a FERMARMI!|Socorro! O chão é GELO! Não consigo PARAR!"),
                mv("bup", 380, "run"), mv("lolly", 160, "run", True),
                act("bup", "spin"),
                {"sfx": "thump", "wait": 0.3},
                S("bup", "Totally... part of the plan.|Totalmente... parte del plan.|Völlig... Teil des Plans.|Totalement... prévu dans le plan.|Assolutamente... parte del piano.|Totalmente... parte do plano."),
                {"sfx": "creak", "wait": 0.5},
                {"villain": "show"},
                {"villain": "wake"},
                act("pim", "scream"),
                act("pim", "faint"),
                S("villain", "Why do you run from me? Stay. Be my friends... forever.|¿Por qué huyen de mí? Quédense. Sean mis amigos... para siempre.|"
                  "Warum lauft ihr weg? Bleibt. Seid meine Freunde... für immer.|Pourquoi vous me fuyez ? Restez. Soyez mes amis... pour toujours.|"
                  "Perché scappate da me? Restate. Siate miei amici... per sempre.|Por que vocês fogem de mim? Fiquem. Sejam meus amigos... para sempre."),
                S("lolly", "Friends don't turn friends into ice cubes!|¡Los amigos no convierten a sus amigos en cubitos de hielo!|"
                  "Freunde machen Freunde nicht zu Eiswürfeln!|Les amis ne transforment pas leurs amis en glaçons !|"
                  "Gli amici non trasformano gli amici in cubetti di ghiaccio!|Amigos não transformam amigos em cubos de gelo!"),
                S("villain", "Mr. Pot promised... if I freeze the kitchen, I will never be alone again.|El Señor Olla prometió... si congelo la cocina, nunca volveré a estar solo.|"
                  "Herr Topf hat versprochen... wenn ich die Küche einfriere, bin ich nie wieder allein.|Monsieur Marmite a promis... si je gèle la cuisine, je ne serai plus jamais seul.|"
                  "Il Signor Pentola ha promesso... se congelo la cucina, non sarò mai più solo.|O Senhor Panela prometeu... se eu congelar a cozinha, nunca mais fico sozinho."),
                S("bup", "He's tricking you! Mr. Pot only wants dinner!|¡Te está engañando! ¡El Señor Olla solo quiere la cena!|"
                  "Er trickst dich aus! Herr Topf will nur Abendessen!|Il te piège ! Monsieur Marmite veut juste son dîner !|"
                  "Ti sta ingannando! Il Signor Pentola vuole solo la cena!|Ele está te enganando! O Senhor Panela só quer o jantar!"),
                {"villain": "rage", "level": 1.0},
                {"shake": 0.6, "power": 20, "and": True},
                S("villain", "LIAR! Stay... COLD!|¡MENTIROSO! ¡Quédate... FRÍO!|LÜGNER! Bleib... KALT!|MENTEUR ! Reste... FROID !|BUGIARDO! Resta... FREDDO!|MENTIROSO! Fique... FRIO!"),
                {"villain": "lunge", "to": 1150},
                mv(["bup", "lolly", "pim"], "off_left", "run"),
            ],
            "tail": 0.4,
        },
        {   # 4 fridge: the door that won't close
            "bg": "fridge", "music": "heartbeat",
            "heroes": {"zeek": 300, "crispy": 520, "bup": 760, "lolly": 1000, "pim": 1240},
            "moods": {"pim": "scared"},
            "beats": [
                {"card": "THE FREEZER DOOR", "es": "LA PUERTA DEL CONGELADOR", "dur": 2.0},
                S("zeek", "The hinge is frozen. We need heat AND muscle.|La bisagra está congelada. Necesitamos calor Y músculos.|"
                  "Das Scharnier ist eingefroren. Wir brauchen Hitze UND Muskeln.|La charnière est gelée. Il faut de la chaleur ET des muscles.|"
                  "Il cardine è congelato. Servono calore E muscoli.|A dobradiça está congelada. Precisamos de calor E músculos."),
                S("crispy", "Then take my ember. All of it.|Entonces tomen mi brasa. Toda.|Dann nehmt meine Glut. Alles davon.|"
                  "Alors prenez ma braise. Toute entière.|Allora prendete la mia brace. Tutta.|Então peguem minha brasa. Toda ela."),
                S("pim", "N-no! You'll go out again! I just got used to you!|¡N-no! ¡Te apagarás otra vez! ¡Me acabo de acostumbrar a ti!|"
                  "N-nein! Du gehst wieder aus! Ich hab mich gerade an dich gewöhnt!|N-non ! Tu vas encore t'éteindre ! Je commençais à m'habituer à toi !|"
                  "N-no! Ti spegnerai di nuovo! Mi ero appena abituato a te!|N-não! Você vai apagar de novo! Eu acabei de me acostumar com você!"),
                S("bup", "Nobody goes out. We push together. On three!|Nadie se apaga. Empujamos juntos. ¡A la de tres!|"
                  "Keiner geht aus. Wir drücken zusammen. Auf drei!|Personne ne s'éteint. On pousse ensemble. À trois !|"
                  "Nessuno si spegne. Spingiamo insieme. Al tre!|Ninguém apaga. Empurramos juntos. No três!"),
                act(["zeek", "crispy", "bup", "lolly", "pim"], "shake"),
                {"sfx": "creak", "wait": 0.6},
                {"sfx": "clank", "wait": 0.3},
                S("pim", "It won't BUDGE!|¡No se MUEVE!|Sie RÜHRT sich nicht!|Elle ne BOUGE pas !|Non si MUOVE!|Não SE MEXE!"),
                S("zeek", "My calculations say we need one more... very angry push.|Mis cálculos dicen que falta un empujón más... muy enojado.|"
                  "Laut meinen Berechnungen brauchen wir noch einen... sehr wütenden Schubs.|Selon mes calculs, il faut une poussée de plus... très en colère.|"
                  "I miei calcoli dicono che serve un'altra spinta... molto arrabbiata.|Meus cálculos dizem que falta mais um empurrão... bem bravo."),
                mood(["zeek", "crispy", "bup", "pim"], "scared"),
                mood("lolly", "angry"),
                S("lolly", "Everybody. Move. Aside.|Todos. A. Un lado.|Alle. Zur. Seite.|Tout le monde. Pousse. Toi.|Tutti. Da. Parte.|Todo mundo. Sai. Da frente."),
                {"shake": 0.8, "power": 26},
                act("lolly", "jump"),
                {"sfx": "thump", "wait": 0.4, "and": True},
                S("lolly", "CLOSE! THIS! DOOR!|¡CIÉRRATE! ¡YA! ¡PUERTA!|GEH! JETZT! ZU!|FERME-TOI ! SALE ! PORTE !|CHIUDITI! SUBITO! PORTA!|FECHA! ESSA! PORTA!"),
                {"sfx": "thump", "wait": 0.6},
                {"shake": 0.5, "power": 18, "and": True},
                mood("lolly", "happy"),
                S("lolly", "Oh! It closed. How lovely!|¡Oh! Se cerró. ¡Qué bonito!|Oh! Sie ist zu. Wie schön!|Oh ! Elle s'est fermée. C'est charmant !|Oh! Si è chiusa. Che bello!|Oh! Fechou. Que lindo!"),
                act("pim", "faint"),
            ],
            "tail": 0.5,
        },
        {   # 5 freezer: Frostbite's lonely side + a promise
            "bg": "freezer", "music": "music_box",
            "heroes": {"lolly": 520, "bup": 300, "crispy": 760},
            "villain": {"type": "frost", "x": 1400, "state": "awake", "scale": 0.8},
            "beats": [
                {"card": "INSIDE THE FREEZER...", "es": "DENTRO DEL CONGELADOR...", "dur": 2.0},
                {"sfx": "ice", "wait": 0.4},
                S("villain", "The door is shut. Now I am alone... again.|La puerta está cerrada. Ahora estoy solo... otra vez.|"
                  "Die Tür ist zu. Jetzt bin ich allein... schon wieder.|La porte est fermée. Me voilà seul... encore.|"
                  "La porta è chiusa. Ora sono solo... di nuovo.|A porta está fechada. Agora estou sozinho... de novo."),
                mv("lolly", 900, "walk"),
                S("lolly", "Not alone. We'll visit you every night. With a blanket!|No estás solo. Te visitaremos cada noche. ¡Con una manta!|"
                  "Nicht allein. Wir besuchen dich jede Nacht. Mit einer Decke!|Pas seul. On viendra te voir chaque nuit. Avec une couverture !|"
                  "Non sei solo. Ti verremo a trovare ogni notte. Con una coperta!|Não está sozinho. Vamos te visitar toda noite. Com um cobertor!"),
                {"villain": "rage", "level": 0.1},
                S("villain", "A... blanket? For me? Nobody ever gave me a blanket.|¿Una... manta? ¿Para mí? Nadie me dio nunca una manta.|"
                  "Eine... Decke? Für mich? Niemand hat mir je eine Decke gegeben.|Une... couverture ? Pour moi ? Personne ne m'en a jamais donné.|"
                  "Una... coperta? Per me? Nessuno mi ha mai dato una coperta.|Um... cobertor? Pra mim? Ninguém nunca me deu um cobertor."),
                S("bup", "Then stop the Big Freeze, and you've got four friends.|Entonces detén la Gran Helada, y tendrás cuatro amigos.|"
                  "Dann stopp den Großen Frost, und du hast vier Freunde.|Alors arrête le Grand Gel, et tu auras quatre amis.|"
                  "Allora ferma il Grande Gelo, e avrai quattro amici.|Então pare o Grande Congelamento, e você ganha quatro amigos."),
                S("crispy", "Five.|Cinco.|Fünf.|Cinq.|Cinque.|Cinco."),
                {"sfx": "ding", "wait": 0.4},
                S("villain", "Deal. The snow will stop. But listen, little dough...|Trato hecho. La nieve se detendrá. Pero escucha, masita...|"
                  "Abgemacht. Der Schnee hört auf. Aber hör zu, kleiner Teig...|Marché conclu. La neige va s'arrêter. Mais écoute, petite pâte...|"
                  "Affare fatto. La neve si fermerà. Ma ascolta, piccola pasta...|Combinado. A neve vai parar. Mas escuta, massinha..."),
                S("villain", "Mr. Pot is not in the kitchen. He went outside. To the garden.|El Señor Olla no está en la cocina. Salió. Al jardín.|"
                  "Herr Topf ist nicht in der Küche. Er ist rausgegangen. In den Garten.|Monsieur Marmite n'est pas dans la cuisine. Il est sorti. Au jardin.|"
                  "Il Signor Pentola non è in cucina. È uscito. In giardino.|O Senhor Panela não está na cozinha. Ele saiu. Para o jardim."),
                mood(["bup", "lolly"], "scared"),
                S("crispy", "The garden... where the pumpkins whisper.|El jardín... donde susurran las calabazas.|Der Garten... wo die Kürbisse flüstern.|"
                  "Le jardin... là où les citrouilles chuchotent.|Il giardino... dove sussurrano le zucche.|O jardim... onde as abóboras sussurram."),
            ],
            "tail": 0.5,
        },
        {   # 6 kitchen: warm again, Pim wakes up
            "bg": "kitchen", "music": "music_box",
            "heroes": {"pim": 300, "zeek": 560, "bup": 820, "lolly": 1080},
            "moods": {"pim": "happy", "zeek": "happy", "bup": "happy", "lolly": "happy"},
            "beats": [
                {"card": "SUNRISE... ALMOST", "es": "EL AMANECER... CASI", "dur": 2.0},
                S("pim", "I-is it over? Did I miss the scary part?|¿Y-ya terminó? ¿Me perdí la parte de miedo?|"
                  "I-ist es vorbei? Hab ich den gruseligen Teil verpasst?|C-c'est fini ? J'ai raté le moment qui fait peur ?|"
                  "È-è finita? Mi sono perso la parte paurosa?|A-acabou? Perdi a parte assustadora?"),
                S("zeek", "You fainted three times. A new record!|Te desmayaste tres veces. ¡Un nuevo récord!|Du bist dreimal ohnmächtig geworden. Neuer Rekord!|"
                  "Tu t'es évanoui trois fois. Nouveau record !|Sei svenuto tre volte. Nuovo record!|Você desmaiou três vezes. Novo recorde!"),
                act("pim", "bounce"),
                S("pim", "Yes! Wait... is that good?|¡Sí! Espera... ¿eso es bueno?|Ja! Moment... ist das gut?|Ouais ! Attends... c'est bien ?|Sì! Aspetta... è una cosa buona?|Isso! Peraí... isso é bom?"),
                S("bup", "Snow's gone. Kitchen's warm. Good work, team.|Ya no hay nieve. La cocina está cálida. Buen trabajo, equipo.|"
                  "Der Schnee ist weg. Die Küche ist warm. Gute Arbeit, Team.|Plus de neige. La cuisine est chaude. Beau travail, l'équipe.|"
                  "La neve è sparita. La cucina è calda. Ottimo lavoro, squadra.|A neve sumiu. A cozinha está quente. Bom trabalho, equipe."),
                {"sfx": "creak", "wait": 0.8},
                mood(["pim", "zeek", "bup", "lolly"], "scared"),
                S("lolly", "Um... who opened the garden door?|Eh... ¿quién abrió la puerta del jardín?|Ähm... wer hat die Gartentür geöffnet?|"
                  "Euh... qui a ouvert la porte du jardin ?|Ehm... chi ha aperto la porta del giardino?|Hum... quem abriu a porta do jardim?"),
                mv(["pim", "zeek", "bup", "lolly"], "off_right", "walk"),
            ],
            "tail": 0.3,
        },
        {   # 7 garden: cliffhanger
            "bg": "garden", "music": "drone",
            "heroes": {"bup": 360, "pim": 600},
            "moods": {"bup": "scared", "pim": "scared"},
            "villain": {"type": "scarecrow", "x": 1400, "state": "hidden", "scale": 0.9},
            "beats": [
                {"sfx": "creak", "wait": 0.6},
                S("narr", "In the night garden, a pumpkin begins to glow.|En el jardín nocturno, una calabaza empieza a brillar.|"
                  "Im nächtlichen Garten beginnt ein Kürbis zu leuchten.|Dans le jardin de nuit, une citrouille se met à briller.|"
                  "Nel giardino notturno, una zucca comincia a brillare.|No jardim à noite, uma abóbora começa a brilhar."),
                {"villain": "show"},
                {"villain": "wake"},
                S("villain", "Answer my riddle... or stay forever.|Responde mi acertijo... o quédate para siempre.|Beantworte mein Rätsel... oder bleib für immer.|"
                  "Réponds à mon énigme... ou reste pour toujours.|Rispondi al mio indovinello... o resta per sempre.|Responda meu enigma... ou fique para sempre."),
                act("pim", "scream"),
                {"villain": "roar"},
                S("villain", "I am Sir Stuffing. And Mr. Pot... sends his regards.|Soy Sir Stuffing. Y el Señor Olla... te manda saludos.|"
                  "Ich bin Sir Stuffing. Und Herr Topf... lässt grüßen.|Je suis Sir Stuffing. Et Monsieur Marmite... vous salue.|"
                  "Sono Sir Stuffing. E il Signor Pentola... vi saluta.|Eu sou Sir Stuffing. E o Senhor Panela... manda lembranças."),
                {"sfx": "sting", "wait": 0.6},
            ],
            "tail": 1.0,
        },
    ],
}

short1 = {
    "id": "ep008_short1", "format": "short",
    "title": "3 Heroes, 1 Door... and an ANGRY Cookie 😡 #shorts",
    "hook": "It won't BUDGE!",
    "description": ("The freezer door is stuck and the Big Freeze is coming. The boys push. Nothing. Then Lolly gets angry... "
                    f"Full episode: \"{LONG_TITLE}\" on {CHANNEL} #shorts #animation #cartoon #doughbros"),
    "tags": SHORT_TAGS + ["lolly", "freezer", "angry cookie"],
    "thumbnail": {"bg": "fridge", "heroes": ["lolly"], "text": "SHE SNAPPED!"},
    "scenes": [{
        "bg": "fridge", "music": "heartbeat",
        "heroes": {"pim": 520, "bup": 740, "zeek": 960, "lolly": 1180},
        "moods": {"pim": "scared"},
        "beats": [
            act(["pim", "bup", "zeek"], "shake"),
            {"sfx": "creak", "wait": 0.2, "and": True},
            S("pim", "It won't BUDGE!|¡No se MUEVE!|Sie RÜHRT sich nicht!|Elle ne BOUGE pas !|Non si MUOVE!|Não SE MEXE!"),
            S("zeek", "Physics says we need one more... very angry push.|La física dice que falta un empujón más... muy enojado.|"
              "Die Physik sagt, wir brauchen noch einen... sehr wütenden Schubs.|La physique dit qu'il faut une poussée de plus... très en colère.|"
              "La fisica dice che serve un'altra spinta... molto arrabbiata.|A física diz que falta mais um empurrão... bem bravo."),
            mood(["pim", "bup", "zeek"], "scared"),
            mood("lolly", "angry"),
            S("lolly", "Boys. Move. Aside.|Chicos. A. Un lado.|Jungs. Zur. Seite.|Les garçons. Poussez. Vous.|Ragazzi. Da. Parte.|Meninos. Sai. Da frente."),
            {"shake": 0.8, "power": 26},
            act("lolly", "jump"),
            {"sfx": "thump", "wait": 0.4, "and": True},
            S("lolly", "CLOSE! THIS! DOOR!|¡CIÉRRATE! ¡YA! ¡PUERTA!|GEH! JETZT! ZU!|FERME-TOI ! SALE ! PORTE !|CHIUDITI! SUBITO! PORTA!|FECHA! ESSA! PORTA!"),
            mood("lolly", "happy"),
            S("lolly", "There! All done. How lovely!|¡Listo! Ya está. ¡Qué bonito!|So! Fertig. Wie schön!|Voilà ! C'est fait. Charmant !|Ecco! Fatto. Che bello!|Pronto! Feito. Que lindo!"),
            act("pim", "faint"),
            {"sfx": "creak", "wait": 0.5},
            mood("lolly", "normal"),
            S("bup", "Uh... it opened again.|Eh... se abrió otra vez.|Äh... sie ist wieder auf.|Euh... elle s'est rouverte.|Ehm... si è riaperta.|Hã... abriu de novo."),
        ],
        "tail": 0.3,
    }],
}

short2 = {
    "id": "ep008_short2", "format": "short",
    "title": "Would YOU Be Friends With a Ghost? 👻 #shorts",
    "hook": "Will you... be my friend?",
    "description": ("Frostbite has been alone in the freezer for a very long time. Lolly says yes. Pim says NOPE. "
                    "Would YOU be his friend? Comment YES or NO! "
                    f"Full episode: \"{LONG_TITLE}\" on {CHANNEL} #shorts #animation #cartoon #doughbros"),
    "tags": SHORT_TAGS + ["frostbite", "ghost", "would you", "lolly", "pim"],
    "thumbnail": {"bg": "freezer", "villain": "frost", "heroes": ["pim"], "text": "BE MY FRIEND?"},
    "scenes": [{
        "bg": "freezer", "music": "drone",
        "heroes": {"pim": 300, "lolly": 600},
        "moods": {"pim": "scared"},
        "villain": {"type": "frost", "x": 1400, "state": "awake", "scale": 0.85},
        "beats": [
            S("villain", "Will you... be my friend?|¿Quieres... ser mi amigo?|Willst du... mein Freund sein?|Veux-tu... être mon ami ?|Vuoi... essere mio amico?|Quer... ser meu amigo?"),
            act("pim", "shake"),
            S("pim", "N-nope! He's a GHOST! In a FREEZER!|¡N-no! ¡Es un FANTASMA! ¡En un CONGELADOR!|N-nö! Er ist ein GEIST! In einem GEFRIERSCHRANK!|"
              "N-non ! C'est un FANTÔME ! Dans un CONGÉLATEUR !|N-no! È un FANTASMA! In un CONGELATORE!|N-não! Ele é um FANTASMA! Num FREEZER!"),
            mood("lolly", "happy"),
            S("lolly", "Aww, he's just lonely! I brought him a blanket!|¡Aww, solo está solito! ¡Le traje una manta!|"
              "Ohh, er ist nur einsam! Ich hab ihm eine Decke mitgebracht!|Ohh, il est juste seul ! Je lui ai apporté une couverture !|"
              "Ooh, è solo solo! Gli ho portato una coperta!|Own, ele só está sozinho! Eu trouxe um cobertor pra ele!"),
            {"villain": "rage", "level": 0.8},
            {"sfx": "ice", "wait": 0.2, "and": True},
            {"shake": 0.4, "power": 14},
            act("pim", "jump"),
            S("pim", "My bandage just FROZE!|¡Mi venda se CONGELÓ!|Mein Pflaster ist GEFROREN!|Mon pansement a GELÉ !|Il mio cerotto si è CONGELATO!|Meu curativo CONGELOU!"),
            {"villain": "rage", "level": 0.1},
            S("narr", "Would YOU be friends with Frostbite? Comment YES or NO!|¿Serías TÚ amigo de Frostbite? ¡Comenta SÍ o NO!|"
              "Wärst DU mit Frostbite befreundet? Schreib JA oder NEIN!|Et TOI, tu serais ami avec Frostbite ? Écris OUI ou NON !|"
              "E TU saresti amico di Frostbite? Scrivi SÌ o NO!|VOCÊ seria amigo do Frostbite? Comente SIM ou NÃO!"),
            S("villain", "Will you...?|¿Quieres...?|Willst du...?|Veux-tu... ?|Vuoi...?|Quer...?"),
        ],
        "tail": 0.3,
    }],
}

for s in (long_, short1, short2):
    for sc in s["scenes"]:
        sc["beats"] = flat(sc["beats"])
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"], len(s["title"]))

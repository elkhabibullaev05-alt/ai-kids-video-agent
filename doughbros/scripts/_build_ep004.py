"""Builds the EP4 scripts (long + 3 shorts). Run: python3 scripts/_build_ep004.py"""
import json, pathlib, importlib.util

OUT = pathlib.Path(__file__).parent
# reuse helpers without re-writing EP3 files
src = (OUT / "_build_ep003.py").read_text(encoding="utf-8").split("ALL4 =")[0]
ns = {"__file__": str(OUT / "_build_ep003.py")}
exec(src, ns)
S, mv, act, mood = ns["S"], ns["mv"], ns["act"], ns["mood"]

ALL4 = ["bup", "pim", "zeek", "lolly"]
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "whisker", "mr pot"]

long_ = {
    "id": "ep004_long", "format": "long",
    "title": "Dough Bros vs WHISKER 🌀 | Animation EP 4",
    "description": ("WHISKER, the giggling hand mixer, spins into the kitchen and mixes up everything in sight. "
                    "Lolly has a crazy plan: challenge him to a spinning contest! But deep in the oven, Mr. Pot "
                    "is counting his new army... and he wants Crispy.\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy"),
    "tags": TAGS + ["episode 4"],
    "thumbnail": {"bg": "kitchen", "villain": "mixer", "heroes": ["pim", "lolly", "bup"], "text": "STOP SPINNING!"},
    "scenes": [
        {   # 1 cold open
            "bg": "kitchen", "music": "drone",
            "heroes": {"bup": 880, "lolly": 660, "zeek": 440, "pim": 230},
            "moods": {"bup": "scared", "lolly": "scared", "zeek": "scared", "pim": "scared"},
            "villain": {"type": "mixer", "x": 1450, "state": "awake", "scale": 0.8},
            "beats": [
                {"sfx": "whoosh", "wait": 0.3},
                S("villain", "Hee hee! Who wants to be a smoothie first?|¡Ji ji! ¿Quién quiere ser batido primero?|"
                  "Hihi! Wer will zuerst ein Smoothie sein?|Hi hi ! Qui veut être un smoothie en premier ?|"
                  "Ih ih! Chi vuole diventare un frullato per primo?|Hi hi! Quem quer virar vitamina primeiro?"),
                {"villain": "lunge", "to": 1250},
                act(ALL4, "scream"),
                {"shake": 0.5, "power": 16},
                S("narr", "Whisker. The fastest, silliest, most dangerous mixer in Table Land.|Whisker. La batidora más rápida, tonta y peligrosa de la Tierra de la Mesa.|"
                  "Whisker. Der schnellste, albernste, gefährlichste Mixer in Tischland.|Whisker. Le batteur le plus rapide, idiot et dangereux du Pays de la Table.|"
                  "Whisker. Lo sbattitore più veloce, sciocco e pericoloso della Terra della Tavola.|Whisker. A batedeira mais rápida, boba e perigosa da Terra da Mesa."),
                S("villain", "Spin, spin, SPIN! Mr. Pot wants you all mixed!|¡Gira, gira, GIRA! ¡El Señor Olla los quiere mezclados!|"
                  "Dreh, dreh, DREH! Herr Topf will euch alle vermixt!|Tourne, tourne, TOURNE ! Monsieur Marmite vous veut mélangés !|"
                  "Gira, gira, GIRA! Il Signor Pentola vi vuole frullati!|Gira, gira, GIRA! O Senhor Panela quer vocês misturados!"),
                {"villain": "rage", "level": 0.8},
                S("bup", "RUN! To the table! Now!|¡CORRAN! ¡A la mesa! ¡Ya!|LAUFT! Zum Tisch! Sofort!|"
                  "COUREZ ! Vers la table ! Maintenant !|CORRETE! Al tavolo! Subito!|CORRAM! Para a mesa! Já!"),
                mv("bup", "off_left", "run", True), mv("lolly", "off_left", "run", True),
                mv("zeek", "off_left", "run", True), mv("pim", "off_left", "run", True),
                {"sfx": "whoosh", "wait": 0.4},
            ],
            "tail": 0.3,
        },
        {   # 2 table: the plan
            "bg": "table", "music": "music_box",
            "heroes": {"bup": 880, "lolly": 660, "zeek": 440, "pim": 230},
            "moods": {"pim": "scared"},
            "beats": [
                {"card": "ON THE DINNER TABLE...", "es": "EN LA MESA...", "dur": 2.0},
                S("pim", "I'm d-dizzy just from LOOKING at him!|¡Me m-mareo solo de MIRARLO!|Mir wird s-schwindelig, nur vom HINSEHEN!|"
                  "J'ai le t-tournis rien qu'en le REGARDANT !|Mi g-gira la testa solo a GUARDARLO!|Fico t-tonto só de OLHAR pra ele!"),
                S("zeek", "He spins at three thousand turns a minute. We can't outrun him.|Gira a tres mil vueltas por minuto. No podemos escapar.|"
                  "Er dreht sich dreitausendmal pro Minute. Wir sind zu langsam.|Il tourne à trois mille tours par minute. Impossible de le semer.|"
                  "Gira a tremila giri al minuto. Non possiamo seminarlo.|Ele gira a três mil voltas por minuto. Não dá pra fugir."),
                S("lolly", "And he'll be here any second!|¡Y llegará en cualquier momento!|Und er ist gleich hier!|"
                  "Et il sera là d'une seconde à l'autre !|E arriverà da un momento all'altro!|E ele vai chegar a qualquer segundo!"),
                S("bup", "Then we don't run. We think. Ideas?|Entonces no corremos. Pensamos. ¿Ideas?|Dann laufen wir nicht. Wir denken. Ideen?|"
                  "Alors on ne court pas. On réfléchit. Des idées ?|Allora non scappiamo. Pensiamo. Idee?|Então não vamos correr. Vamos pensar. Ideias?"),
                mood("lolly", "happy"),
                act("lolly", "bounce"),
                S("lolly", "Ooh! He LOVES spinning. So let's have a spinning contest!|¡Oh! Le ENCANTA girar. ¡Hagamos un concurso de giros!|"
                  "Oh! Er LIEBT es, sich zu drehen. Machen wir einen Drehwettbewerb!|Oh ! Il ADORE tourner. Faisons un concours de toupie !|"
                  "Oh! ADORA girare. Facciamo una gara di giravolte!|Ah! Ele AMA girar. Vamos fazer um concurso de giro!"),
                S("zeek", "Brilliant! Nobody can spin forever. He'll get dizzy!|¡Brillante! Nadie puede girar para siempre. ¡Se mareará!|"
                  "Genial! Niemand kann ewig drehen. Ihm wird schwindelig!|Génial ! Personne ne peut tourner pour toujours. Il aura le tournis !|"
                  "Geniale! Nessuno può girare per sempre. Gli girerà la testa!|Genial! Ninguém consegue girar para sempre. Ele vai ficar tonto!"),
                S("bup", "And who spins against him?|¿Y quién gira contra él?|Und wer dreht gegen ihn?|Et qui tourne contre lui ?|E chi gira contro di lui?|E quem gira contra ele?"),
                {"wait": 0.5},
                mood(["bup", "lolly", "zeek"], "happy"),
                act("pim", "shake"),
                S("pim", "Why is everyone looking at me AGAIN?!|¿¡Por qué todos me miran OTRA VEZ!?|Warum schauen mich alle SCHON WIEDER an?!|"
                  "Pourquoi tout le monde me regarde ENCORE ?!|Perché mi guardano tutti DI NUOVO?!|Por que todo mundo está olhando pra mim DE NOVO?!"),
                S("lolly", "Because you shake so much, you're already halfway spinning!|¡Porque tiemblas tanto que ya estás medio girando!|"
                  "Weil du so zitterst, drehst du dich schon halb!|Parce que tu trembles tellement que tu tournes déjà à moitié !|"
                  "Perché tremi così tanto che stai già mezzo girando!|Porque você treme tanto que já está meio girando!"),
                S("pim", "That... is weirdly true.|Eso... es raramente cierto.|Das... stimmt komischerweise.|C'est... bizarrement vrai.|Questo... è stranamente vero.|Isso... é estranhamente verdade."),
            ],
            "tail": 0.5,
        },
        {   # 3 the contest
            "bg": "table", "music": "heartbeat",
            "heroes": {"pim": 760, "bup": 480, "lolly": 260, "zeek": -300},
            "villain": {"type": "mixer", "x": 1450, "state": "hidden", "scale": 0.8},
            "beats": [
                {"sfx": "whoosh", "wait": 0.4},
                {"villain": "show"},
                S("villain", "Found you! Hee hee! Ready to be MIXED?|¡Los encontré! ¡Ji ji! ¿Listos para ser MEZCLADOS?|"
                  "Gefunden! Hihi! Bereit, VERMIXT zu werden?|Trouvés ! Hi hi ! Prêts à être MÉLANGÉS ?|"
                  "Trovati! Ih ih! Pronti a essere FRULLATI?|Achei vocês! Hi hi! Prontos para serem MISTURADOS?"),
                mood("pim", "angry"),
                S("pim", "W-wait! I challenge you... to a SPINNING CONTEST!|¡E-espera! Te reto... ¡a un CONCURSO DE GIROS!|"
                  "W-warte! Ich fordere dich heraus... zu einem DREHWETTBEWERB!|A-attends ! Je te défie... à un CONCOURS DE TOUPIE !|"
                  "A-aspetta! Ti sfido... a una GARA DI GIRAVOLTE!|E-espera! Eu te desafio... para um CONCURSO DE GIRO!"),
                {"villain": "rage", "level": 0.3},
                S("villain", "A contest? Ooh, I LOVE contests! Hee hee! Go!|¿Un concurso? ¡Me ENCANTAN los concursos! ¡Ji ji! ¡Ya!|"
                  "Ein Wettbewerb? Oh, ich LIEBE Wettbewerbe! Hihi! Los!|Un concours ? J'ADORE les concours ! Hi hi ! Partez !|"
                  "Una gara? Oh, ADORO le gare! Ih ih! Via!|Um concurso? Eu AMO concursos! Hi hi! Já!"),
                act("pim", "spin"),
                {"sfx": "whoosh", "wait": 0.3, "and": True},
                act("pim", "spin"),
                S("narr", "Round one. Pim spins. Whisker spins faster.|Primera ronda. Pim gira. Whisker gira más rápido.|"
                  "Runde eins. Pim dreht sich. Whisker dreht sich schneller.|Premier tour. Pim tourne. Whisker tourne plus vite.|"
                  "Primo round. Pim gira. Whisker gira più veloce.|Primeira rodada. Pim gira. Whisker gira mais rápido."),
                {"villain": "rage", "level": 1.0},
                {"shake": 0.6, "power": 12},
                act("pim", "spin"),
                S("narr", "Round two. Pim spins. Whisker spins even faster.|Segunda ronda. Pim gira. Whisker gira aún más rápido.|"
                  "Runde zwei. Pim dreht sich. Whisker noch schneller.|Deuxième tour. Pim tourne. Whisker encore plus vite.|"
                  "Secondo round. Pim gira. Whisker ancora più veloce.|Segunda rodada. Pim gira. Whisker ainda mais rápido."),
                S("villain", "Hee hee! I'm the best! The fastest! The... the... whoa...|¡Ji ji! ¡Soy el mejor! ¡El más rápido! El... el... uy...|"
                  "Hihi! Ich bin der Beste! Der Schnellste! Der... der... uiii...|Hi hi ! Je suis le meilleur ! Le plus rapide ! Le... le... oh là...|"
                  "Ih ih! Sono il migliore! Il più veloce! Il... il... oddio...|Hi hi! Eu sou o melhor! O mais rápido! O... o... opa..."),
                {"sfx": "boing", "wait": 0.3},
                {"villain": "sleep"},
                S("villain", "Why are there... five tables?|¿Por qué hay... cinco mesas?|Warum gibt es... fünf Tische?|"
                  "Pourquoi il y a... cinq tables ?|Perché ci sono... cinque tavoli?|Por que tem... cinco mesas?"),
                mood(["bup", "lolly"], "happy"),
                act(["bup", "lolly"], "jump"),
                S("bup", "He's dizzy! Pim, you did it!|¡Está mareado! ¡Pim, lo lograste!|Ihm ist schwindelig! Pim, du hast es geschafft!|"
                  "Il a le tournis ! Pim, tu as réussi !|Gli gira la testa! Pim, ce l'hai fatta!|Ele está tonto! Pim, você conseguiu!"),
                mood("pim", "happy"),
                S("pim", "I did? I won? I... WON!|¿Sí? ¿Gané? ¡GANÉ!|Echt? Ich hab gewonnen? Ich hab... GEWONNEN!|Vraiment ? J'ai gagné ? J'ai... GAGNÉ !|Davvero? Ho vinto? Ho... VINTO!|Sério? Eu ganhei? Eu... GANHEI!"),
                act("pim", "faint"),
                S("lolly", "And... he fainted from happiness.|Y... se desmayó de felicidad.|Und... er ist vor Freude umgekippt.|"
                  "Et... il s'est évanoui de bonheur.|E... è svenuto dalla felicità.|E... ele desmaiou de felicidade."),
            ],
            "tail": 0.6,
        },
        {   # 3b kitchen: where is Crispy
            "bg": "kitchen", "music": "music_box",
            "heroes": {"bup": 880, "lolly": 660, "zeek": 440, "pim": 230},
            "moods": {"pim": "happy"},
            "beats": [
                {"card": "BACK IN THE KITCHEN...", "es": "DE VUELTA EN LA COCINA...", "dur": 2.0},
                S("pim", "Pim the Champion! Pim the Spinner! Pim the... dizzy.|¡Pim el Campeón! ¡Pim el Giratorio! Pim el... mareado.|"
                  "Pim der Champion! Pim der Kreisel! Pim der... Schwindlige.|Pim le Champion ! Pim la Toupie ! Pim le... étourdi.|"
                  "Pim il Campione! Pim la Trottola! Pim il... confuso.|Pim, o Campeão! Pim, o Pião! Pim, o... tonto."),
                act("pim", "spin"),
                S("lolly", "We should celebrate! Where's Crispy? He loves... well, he likes nothing.|¡Hay que celebrar! ¿Y Crispy? A él le encanta... bueno, nada.|"
                  "Wir sollten feiern! Wo ist Crispy? Er liebt... na ja, nichts.|Il faut fêter ça ! Où est Crispy ? Il adore... bon, rien.|"
                  "Dobbiamo festeggiare! Dov'è Crispy? Lui adora... beh, niente.|Vamos comemorar! Cadê o Crispy? Ele adora... bom, nada."),
                S("zeek", "Strange. My Crispy-Detector shows him... in the oven.|Qué raro. Mi Detector de Crispy lo muestra... en el horno.|"
                  "Seltsam. Mein Crispy-Detektor zeigt ihn... im Ofen.|Étrange. Mon Détecteur de Crispy le montre... dans le four.|"
                  "Strano. Il mio Rileva-Crispy lo segnala... nel forno.|Estranho. Meu Detector de Crispy mostra ele... no forno."),
                mood(ALL4, "scared"),
                S("bup", "The oven? That's Mr. Pot's home!|¿El horno? ¡Es la casa del Señor Olla!|Der Ofen? Das ist das Zuhause von Herrn Topf!|"
                  "Le four ? C'est la maison de Monsieur Marmite !|Il forno? È la casa del Signor Pentola!|O forno? É a casa do Senhor Panela!"),
                S("pim", "Nope. No. Absolutely not. I just won a contest!|No. Nop. De ninguna manera. ¡Acabo de ganar un concurso!|"
                  "Nö. Nein. Auf keinen Fall. Ich hab gerade gewonnen!|Non. Non. Absolument pas. Je viens de gagner un concours !|"
                  "No. No. Assolutamente no. Ho appena vinto una gara!|Não. Nada disso. De jeito nenhum. Acabei de ganhar um concurso!"),
                S("zeek", "Statistically, nobody comes back from the oven.|Estadísticamente, nadie vuelve del horno.|Statistisch kommt niemand aus dem Ofen zurück.|"
                  "Statistiquement, personne ne revient du four.|Statisticamente, nessuno torna dal forno.|Estatisticamente, ninguém volta do forno."),
                S("lolly", "Crispy always helps us. Now it's our turn to help him.|Crispy siempre nos ayuda. Ahora nos toca ayudarlo.|"
                  "Crispy hilft uns immer. Jetzt helfen wir ihm.|Crispy nous aide toujours. À notre tour de l'aider.|"
                  "Crispy ci aiuta sempre. Ora tocca a noi aiutarlo.|O Crispy sempre ajuda a gente. Agora é a nossa vez."),
                S("bup", "Lolly's right. Zeek, you're with me. Lolly, watch Pim.|Lolly tiene razón. Zeek, conmigo. Lolly, cuida a Pim.|"
                  "Lolly hat recht. Zeek, du kommst mit. Lolly, pass auf Pim auf.|Lolly a raison. Zeek, avec moi. Lolly, surveille Pim.|"
                  "Lolly ha ragione. Zeek, vieni con me. Lolly, bada a Pim.|A Lolly tem razão. Zeek, comigo. Lolly, cuida do Pim."),
                mood("bup", "angry"),
                mv("bup", "off_right", "walk", False), mv("zeek", "off_right", "walk", True),
            ],
            "tail": 0.3,
        },
        {   # 4 Mr. Pot's lair
            "bg": "oven", "music": "drone",
            "heroes": {"bup": 640, "zeek": 380, "crispy": -400},
            "moods": {"bup": "scared", "zeek": "scared"},
            "villain": {"type": "pot", "x": 1450, "state": "asleep", "scale": 0.95},
            "beats": [
                {"card": "MEANWHILE... IN THE OVEN", "es": "MIENTRAS TANTO... EN EL HORNO", "dur": 2.2},
                S("zeek", "Shh. If Whisker came from here, Mr. Pot must be close.|Shh. Si Whisker vino de aquí, el Señor Olla está cerca.|"
                  "Psst. Wenn Whisker von hier kam, ist Herr Topf nah.|Chut. Si Whisker vient d'ici, Monsieur Marmite n'est pas loin.|"
                  "Shh. Se Whisker è venuto da qui, il Signor Pentola è vicino.|Psiu. Se o Whisker veio daqui, o Senhor Panela está perto."),
                {"sfx": "thump", "wait": 0.6},
                {"villain": "wake"},
                S("villain", "Fresh... dough... I can smell you.|Masa... fresca... Puedo olerlos.|Frischer... Teig... Ich rieche euch.|"
                  "De la pâte... fraîche... Je vous sens.|Impasto... fresco... Vi sento.|Massa... fresca... Eu sinto o cheiro de vocês."),
                act(["bup", "zeek"], "shake"),
                S("villain", "Frostbite. Toastmaw. Whisker. My army grows every night.|Frostbite. Toastmaw. Whisker. Mi ejército crece cada noche.|"
                  "Frostbite. Toastmaw. Whisker. Meine Armee wächst jede Nacht.|Frostbite. Toastmaw. Whisker. Mon armée grandit chaque nuit.|"
                  "Frostbite. Toastmaw. Whisker. Il mio esercito cresce ogni notte.|Frostbite. Toastmaw. Whisker. Meu exército cresce toda noite."),
                S("zeek", "He's counting his army...|Está contando su ejército...|Er zählt seine Armee...|Il compte son armée...|Sta contando il suo esercito...|Ele está contando o exército dele..."),
                S("villain", "And soon... the kettle. The vacuum. The jelly. ALL of them!|Y pronto... la tetera. La aspiradora. La gelatina. ¡TODOS!|"
                  "Und bald... der Wasserkocher. Der Staubsauger. Der Wackelpudding. ALLE!|Et bientôt... la bouilloire. L'aspirateur. La gelée. TOUS !|"
                  "E presto... il bollitore. L'aspirapolvere. La gelatina. TUTTI!|E logo... a chaleira. O aspirador. A gelatina. TODOS!"),
                S("bup", "That's... every appliance in the house.|Eso es... cada aparato de la casa.|Das ist... jedes Gerät im Haus.|"
                  "C'est... tous les appareils de la maison.|Sono... tutti gli elettrodomestici della casa.|Isso é... todo aparelho da casa."),
                S("bup", "What do you want from us?!|¿¡Qué quieres de nosotros!?|Was willst du von uns?!|Qu'est-ce que tu nous veux ?!|Cosa vuoi da noi?!|O que você quer da gente?!"),
                {"villain": "rage", "level": 0.7},
                S("villain", "Not you, little loaf. I want the one I burned long ago.|Tú no, panecito. Quiero al que quemé hace mucho tiempo.|"
                  "Nicht dich, kleines Brot. Ich will den, den ich vor langer Zeit verbrannt habe.|Pas toi, petit pain. Je veux celui que j'ai brûlé il y a longtemps.|"
                  "Non te, pagnottina. Voglio quello che ho bruciato tanto tempo fa.|Não você, pãozinho. Eu quero aquele que queimei há muito tempo."),
                S("zeek", "He means... Crispy.|Se refiere a... Crispy.|Er meint... Crispy.|Il parle de... Crispy.|Intende... Crispy.|Ele quer dizer... o Crispy."),
                S("bup", "Crispy? What did you do to him?|¿Crispy? ¿Qué le hiciste?|Crispy? Was hast du ihm angetan?|"
                  "Crispy ? Qu'est-ce que tu lui as fait ?|Crispy? Cosa gli hai fatto?|Crispy? O que você fez com ele?"),
                S("villain", "I made him... CRISPY. Ha ha ha!|Lo dejé... CRUJIENTE. ¡Ja ja ja!|Ich hab ihn... KNUSPRIG gemacht. Ha ha ha!|"
                  "Je l'ai rendu... CROUSTILLANT. Ha ha ha !|L'ho reso... CROCCANTE. Ah ah ah!|Eu deixei ele... CROCANTE. Ha ha ha!"),
                {"sfx": "creak", "wait": 0.6},
                mv("crispy", 150, "walk"),
                S("crispy", "You called, old Pot?|¿Me llamaste, vieja Olla?|Du hast gerufen, alter Topf?|Tu m'as appelé, vieille Marmite ?|Mi hai chiamato, vecchia Pentola?|Você chamou, velha Panela?"),
                {"villain": "roar"},
                S("villain", "At last. Come closer, Crispy. Time to FRY... again!|Por fin. Acércate, Crispy. ¡Hora de FREÍR... otra vez!|"
                  "Endlich. Komm näher, Crispy. Zeit zum BRATEN... schon wieder!|Enfin. Approche, Crispy. L'heure de FRIRE... encore !|"
                  "Finalmente. Avvicinati, Crispy. È ora di FRIGGERE... di nuovo!|Finalmente. Chegue mais perto, Crispy. Hora de FRITAR... de novo!"),
                {"villain": "lunge", "to": 1200},
                act(["bup", "zeek"], "scream"),
                {"shake": 0.9, "power": 24},
                S("crispy", "Run, Bup. This fight is mine.|Corre, Bup. Esta pelea es mía.|Lauf, Bup. Das ist mein Kampf.|"
                  "Cours, Bup. Ce combat est le mien.|Corri, Bup. Questa battaglia è mia.|Corre, Bup. Essa luta é minha."),
                S("bup", "Dough Bros never leave a friend behind!|¡Los Dough Bros nunca abandonan a un amigo!|Dough Bros lassen nie einen Freund zurück!|"
                  "Les Dough Bros n'abandonnent jamais un ami !|I Dough Bros non lasciano mai indietro un amico!|Os Dough Bros nunca abandonam um amigo!"),
                {"villain": "rage", "level": 1.0},
                S("villain", "Then ALL of you... will be my dinner!|Entonces TODOS ustedes... ¡serán mi cena!|Dann werdet IHR ALLE... mein Abendessen!|"
                  "Alors VOUS TOUS... serez mon dîner !|Allora TUTTI voi... sarete la mia cena!|Então TODOS vocês... serão o meu jantar!"),

                {"villain": "roar"},
                act(["bup", "zeek", "crispy"], "scream"),
            ],
            "tail": 2.0,
        },
    ],
}

short1 = {  # character moment: Crispy
    "id": "ep004_short1", "format": "short",
    "title": "Crispy appears from NOWHERE 👀 #shorts",
    "hook": "Where did HE come from?",
    "description": "Bup and Pim think they're alone in the attic. They're not. #shorts #animation #cartoon #doughbros #funny",
    "tags": ["shorts"] + TAGS[:7] + ["crispy", "jump scare"],
    "thumbnail": {"bg": "attic", "villain": "pot", "heroes": ["crispy", "pim"], "text": "BEHIND YOU!"},
    "scenes": [{
        "bg": "attic", "music": "heartbeat",
        "heroes": {"bup": 360, "pim": 640, "crispy": 2300},
        "moods": {"pim": "scared"},
        "beats": [
            S("pim", "Is anyone here? Hello? ...Good. Nobody. We're alone.|¿Hay alguien? ¿Hola? ...Bien. Nadie. Estamos solos.|"
              "Ist hier jemand? Hallo? ...Gut. Niemand. Wir sind allein.|Il y a quelqu'un ? Allô ? ...Bien. Personne. On est seuls.|"
              "C'è qualcuno? Ciao? ...Bene. Nessuno. Siamo soli.|Tem alguém aqui? Oi? ...Ótimo. Ninguém. Estamos sozinhos."),
            S("bup", "See? Nothing to be scared of, Pim.|¿Ves? No hay nada que temer, Pim.|Siehst du? Nichts, wovor man Angst haben muss, Pim.|"
              "Tu vois ? Rien à craindre, Pim.|Visto? Niente di cui aver paura, Pim.|Viu? Nada a temer, Pim."),
            mv("crispy", 920, "walk"),
            S("crispy", "Wrong.|Error.|Falsch.|Faux.|Sbagliato.|Errado."),
            act(["bup", "pim"], "scream"),
            {"shake": 0.6, "power": 18},
            act("pim", "faint"),
            S("crispy", "...I just wanted to say good night.|...Solo quería decir buenas noches.|...Ich wollte nur gute Nacht sagen.|"
              "...Je voulais juste dire bonne nuit.|...Volevo solo dire buonanotte.|...Eu só queria dar boa noite."),
        ],
        "tail": 1.0,
    }],
}

short2 = {  # question
    "id": "ep004_short2", "format": "short",
    "title": "Which villain is SCARIER? 👇 #shorts",
    "hook": "Pot or Mixer?",
    "description": "Mr. Pot or Whisker the mixer: who is scarier? Comment POT or MIXER! #shorts #animation #cartoon #doughbros",
    "tags": ["shorts"] + TAGS + ["which is scarier"],
    "thumbnail": {"bg": "kitchen", "villain": "pot", "heroes": ["zeek", "lolly"], "text": "WHO WINS?"},
    "scenes": [{
        "bg": "kitchen", "music": "drone",
        "heroes": {"zeek": 320, "lolly": 600},
        "villain": {"type": "mixer", "x": 1400, "state": "awake", "scale": 0.8},
        "beats": [
            S("villain", "Hee hee! I spin three thousand times a minute!|¡Ji ji! ¡Giro tres mil veces por minuto!|Hihi! Ich drehe mich dreitausendmal pro Minute!|"
              "Hi hi ! Je tourne trois mille fois par minute !|Ih ih! Giro tremila volte al minuto!|Hi hi! Eu giro três mil vezes por minuto!"),
            {"villain": "rage", "level": 1.0},
            act(["zeek", "lolly"], "scream"),
            S("zeek", "Okay, he's scary. But Mr. Pot has THREE eyes.|Vale, da miedo. Pero el Señor Olla tiene TRES ojos.|"
              "Okay, er ist gruselig. Aber Herr Topf hat DREI Augen.|D'accord, il fait peur. Mais Monsieur Marmite a TROIS yeux.|"
              "Ok, fa paura. Ma il Signor Pentola ha TRE occhi.|Tá, ele dá medo. Mas o Senhor Panela tem TRÊS olhos."),
            S("lolly", "So who's scarier? The Pot or the Mixer?|¿Entonces quién da más miedo? ¿La Olla o la Batidora?|"
              "Also, wer ist gruseliger? Der Topf oder der Mixer?|Alors, qui fait le plus peur ? La Marmite ou le Batteur ?|"
              "Allora, chi fa più paura? La Pentola o lo Sbattitore?|Então, quem dá mais medo? A Panela ou a Batedeira?"),
            S("narr", "You decide! Comment POT or MIXER!|¡Tú decides! ¡Comenta OLLA o BATIDORA!|Du entscheidest! Schreib TOPF oder MIXER!|"
              "À toi de décider ! Écris MARMITE ou BATTEUR !|Decidi tu! Scrivi PENTOLA o SBATTITORE!|Você decide! Comente PANELA ou BATEDEIRA!"),
        ],
        "tail": 1.0,
    }],
}

short3 = {  # teaser
    "id": "ep004_short3", "format": "short",
    "title": "The SPINNING contest 🌀 #shorts",
    "hook": "Pim vs the MIXER",
    "description": "Pim challenges Whisker the mixer to a spinning contest. Who gets dizzy first? Full episode on the channel! #shorts #animation #cartoon #doughbros",
    "tags": ["shorts"] + TAGS + ["contest"],
    "thumbnail": {"bg": "table", "villain": "mixer", "heroes": ["pim"], "text": "SPIN OFF!"},
    "scenes": [{
        "bg": "table", "music": "heartbeat",
        "heroes": {"pim": 600},
        "moods": {"pim": "angry"},
        "villain": {"type": "mixer", "x": 1400, "state": "awake", "scale": 0.8},
        "beats": [
            S("pim", "I challenge you... to a SPINNING CONTEST!|Te reto... ¡a un CONCURSO DE GIROS!|Ich fordere dich heraus... zu einem DREHWETTBEWERB!|"
              "Je te défie... à un CONCOURS DE TOUPIE !|Ti sfido... a una GARA DI GIRAVOLTE!|Eu te desafio... para um CONCURSO DE GIRO!"),
            S("villain", "Ooh, I LOVE contests! Hee hee! Go!|¡Me ENCANTAN los concursos! ¡Ji ji! ¡Ya!|Oh, ich LIEBE Wettbewerbe! Hihi! Los!|"
              "J'ADORE les concours ! Hi hi ! Partez !|Oh, ADORO le gare! Ih ih! Via!|Eu AMO concursos! Hi hi! Já!"),
            act("pim", "spin"),
            {"villain": "rage", "level": 1.0},
            {"shake": 0.6, "power": 12},
            act("pim", "spin"),
            S("villain", "I'm the fastest! The... the... whoa...|¡Soy el más rápido! El... el... uy...|Ich bin der Schnellste! Der... der... uiii...|"
              "Je suis le plus rapide ! Le... le... oh là...|Sono il più veloce! Il... il... oddio...|Eu sou o mais rápido! O... o... opa..."),
            {"sfx": "boing", "wait": 0.3},
            {"villain": "sleep"},
            S("narr", "Round two...|Segunda ronda...|Runde zwei...|Deuxième tour...|Secondo round...|Segunda rodada..."),
            S("narr", "Who won? Full episode on the channel!|¿Quién ganó? ¡Episodio completo en el canal!|Wer hat gewonnen? Ganze Folge auf dem Kanal!|"
              "Qui a gagné ? Épisode complet sur la chaîne !|Chi ha vinto? Episodio completo sul canale!|Quem ganhou? Episódio completo no canal!"),
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

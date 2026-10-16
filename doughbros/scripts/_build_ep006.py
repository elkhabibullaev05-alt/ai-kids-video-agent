"""Builds the EP6 scripts (long + 3 shorts). Run: python3 scripts/_build_ep006.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
src = (OUT / "_build_ep003.py").read_text(encoding="utf-8").split("ALL4 =")[0]
ns = {"__file__": str(OUT / "_build_ep003.py")}
exec(src, ns)
S, mv, act, mood = ns["S"], ns["mv"], ns["act"], ns["mood"]

TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "old hissy", "kettle"]

long_ = {
    "id": "ep006_long", "format": "long",
    "title": "Dough Bros vs OLD HISSY ♨️ | Animation EP 6",
    "description": ("Crispy's fire has gone out, and the only warm thing left in the kitchen is Old Hissy, "
                    "the grumpiest, loudest kettle in Table Land. He screams, he steams... but is he really a monster, "
                    "or just lonely? And what is that hungry thing waiting in the closet?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy"),
    "tags": TAGS + ["episode 6", "crispy", "gulpzilla"],
    "thumbnail": {"bg": "bathroom", "villain": "kettle", "heroes": ["pim", "lolly", "bup"], "text": "HE'S BOILING!"},
    "scenes": [
        {   # 1 cold open: Old Hissy screams
            "bg": "kitchen", "music": "drone",
            "heroes": {"lolly": 240, "pim": 460, "bup": 680, "crispy": 900},
            "moods": {"bup": "scared", "pim": "scared", "lolly": "scared"},
            "villain": {"type": "kettle", "x": 1450, "state": "awake", "scale": 0.85},
            "beats": [
                {"villain": "rage", "level": 1.0},
                {"shake": 0.6, "power": 20, "and": True},
                S("villain", "WHO touched my lid?! I'm BOILING!|¡¿QUIÉN tocó mi tapa?! ¡Estoy HIRVIENDO!|"
                  "WER hat meinen Deckel angefasst?! Ich KOCHE!|QUI a touché mon couvercle ?! Je BOUS !|"
                  "CHI ha toccato il mio coperchio?! Sto BOLLENDO!|QUEM mexeu na minha tampa?! Estou FERVENDO!"),
                act(["bup", "pim", "lolly"], "scream"),
                act("crispy", "faint"),
                S("bup", "Please, Old Hissy! Our friend is freezing. He needs your heat.|¡Por favor, Viejo Hissy! Nuestro amigo se congela. Necesita tu calor.|"
                  "Bitte, alter Hissy! Unser Freund erfriert. Er braucht deine Wärme.|S'il te plaît, Vieux Hissy ! Notre ami gèle. Il a besoin de ta chaleur.|"
                  "Ti prego, Vecchio Hissy! Il nostro amico si congela. Gli serve il tuo calore.|Por favor, Velho Hissy! Nosso amigo está congelando. Ele precisa do seu calor."),
                S("villain", "My heat? HA! Nobody wants my heat anymore.|¿Mi calor? ¡JA! Ya nadie quiere mi calor.|"
                  "Meine Wärme? HA! Niemand will mehr meine Wärme.|Ma chaleur ? HA ! Plus personne ne veut ma chaleur.|"
                  "Il mio calore? AH! Nessuno vuole più il mio calore.|Meu calor? HA! Ninguém quer mais o meu calor."),
                S("pim", "W-we do! We really, really do!|¡N-nosotros sí! ¡De verdad, de verdad!|"
                  "W-wir schon! Wirklich, wirklich!|N-nous, si ! Vraiment, vraiment !|N-noi sì! Davvero, davvero!|N-nós queremos! De verdade, de verdade!"),
                S("villain", "Fifty years on this stove. Not one cup of tea. Not one thank you.|Cincuenta años en esta estufa. Ni una taza de té. Ni un gracias.|"
                  "Fünfzig Jahre auf diesem Herd. Keine Tasse Tee. Kein einziges Danke.|Cinquante ans sur ce feu. Pas une tasse de thé. Pas un merci.|"
                  "Cinquant'anni su questo fornello. Nemmeno un tè. Nemmeno un grazie.|Cinquenta anos neste fogão. Nem uma xícara de chá. Nem um obrigado."),
                mood("lolly", "normal"),
                S("lolly", "Oh, that's so sad... Would you help us? Pretty please?|Oh, qué triste... ¿Nos ayudarías? ¿Por favor?|"
                  "Oh, wie traurig... Hilfst du uns? Bitte, bitte?|Oh, c'est si triste... Tu veux bien nous aider ? S'il te plaît ?|"
                  "Oh, che tristezza... Ci aiuteresti? Per favore?|Ah, que triste... Você ajuda a gente? Por favorzinho?"),
                {"villain": "rage", "level": 0.7},
                S("villain", "Leave me ALONE! I'm going where the pipes still sing!|¡Déjenme EN PAZ! ¡Me voy donde las tuberías aún cantan!|"
                  "Lasst mich IN RUHE! Ich gehe dahin, wo die Rohre noch singen!|Laissez-moi TRANQUILLE ! Je vais là où les tuyaux chantent encore !|"
                  "Lasciatemi IN PACE! Vado dove i tubi cantano ancora!|Me deixem EM PAZ! Vou para onde os canos ainda cantam!"),
                mv("villain", "off_right", "walk"),
                S("bup", "He's going to the bathroom. Zeek! We need a wagon!|Va al baño. ¡Zeek! ¡Necesitamos un carrito!|"
                  "Er geht ins Badezimmer. Zeek! Wir brauchen einen Wagen!|Il va dans la salle de bain. Zeek ! Il nous faut un chariot !|"
                  "Va in bagno. Zeek! Ci serve un carretto!|Ele vai para o banheiro. Zeek! Precisamos de um carrinho!"),
            ],
            "tail": 0.5,
        },
        {   # 2 table: Zeek's invention fails
            "bg": "table", "music": "music_box",
            "heroes": {"crispy": 440, "zeek": 700, "bup": -300, "pim": -500},
            "moods": {"crispy": "scared"},
            "beats": [
                {"card": "MEANWHILE, ON THE TABLE...", "es": "MIENTRAS TANTO, EN LA MESA...", "dur": 2.2},
                S("zeek", "My calculations say Crispy's ember has three minutes left.|Mis cálculos dicen que a la brasa de Crispy le quedan tres minutos.|"
                  "Laut meinen Berechnungen hat Crispys Glut noch drei Minuten.|Selon mes calculs, la braise de Crispy tiendra encore trois minutes.|"
                  "I miei calcoli dicono che alla brace di Crispy restano tre minuti.|Meus cálculos dizem que a brasa do Crispy tem três minutos."),
                mv("bup", 960, "run"), mv("pim", 1220, "run", True),
                S("pim", "Th-three minutes?! That's barely a sandwich!|¡¿T-tres minutos?! ¡Eso no da ni para un sándwich!|"
                  "D-drei Minuten?! Das reicht kaum für ein Sandwich!|T-trois minutes ?! C'est à peine un sandwich !|"
                  "T-tre minuti?! Basta appena per un panino!|T-três minutos?! Não dá nem pra um sanduíche!"),
                S("zeek", "Behold! The Toasty-Matic Five Thousand! A spoon, a candle, and hope.|¡Contemplen! ¡La Tostadora-Matic Cinco Mil! Una cuchara, una vela y esperanza.|"
                  "Seht her! Der Toasty-Matic Fünftausend! Ein Löffel, eine Kerze und Hoffnung.|Voici le Toasty-Matic Cinq Mille ! Une cuillère, une bougie et de l'espoir.|"
                  "Ecco a voi il Toasty-Matic Cinquemila! Un cucchiaio, una candela e speranza.|Contemplem! O Toasty-Matic Cinco Mil! Uma colher, uma vela e esperança."),
                {"sfx": "clank", "wait": 0.4},
                {"sfx": "pop", "wait": 0.4},
                {"shake": 0.4, "power": 10},
                S("narr", "The Toasty-Matic makes one tiny spark... and falls apart.|La Tostadora-Matic hace una chispa diminuta... y se desarma.|"
                  "Der Toasty-Matic macht einen winzigen Funken... und fällt auseinander.|Le Toasty-Matic fait une minuscule étincelle... et tombe en morceaux.|"
                  "Il Toasty-Matic fa una scintilla minuscola... e cade a pezzi.|O Toasty-Matic solta uma faisquinha... e se desmancha."),
                act("zeek", "jump"),
                S("zeek", "Hmm. Hope was not enough.|Hmm. La esperanza no fue suficiente.|Hmm. Hoffnung hat nicht gereicht.|"
                  "Hmm. L'espoir ne suffisait pas.|Mmh. La speranza non è bastata.|Hmm. A esperança não bastou."),
                S("crispy", "So... cold...|Tanto... frío...|So... kalt...|Si... froid...|Che... freddo...|Tanto... frio..."),
                S("bup", "Hang on, Crispy. We're taking you to a kettle.|Aguanta, Crispy. Te llevamos con una tetera.|"
                  "Halte durch, Crispy. Wir bringen dich zu einem Kessel.|Tiens bon, Crispy. On t'emmène voir une bouilloire.|"
                  "Resisti, Crispy. Ti portiamo da un bollitore.|Aguenta, Crispy. Vamos te levar até uma chaleira."),
                mood("pim", "scared"),
                S("pim", "A kettle that HATES us. G-great plan, Bup.|Una tetera que nos ODIA. G-gran plan, Bup.|"
                  "Ein Kessel, der uns HASST. T-toller Plan, Bup.|Une bouilloire qui nous DÉTESTE. S-super plan, Bup.|"
                  "Un bollitore che ci ODIA. G-gran piano, Bup.|Uma chaleira que ODEIA a gente. Ó-ótimo plano, Bup."),
                mv("bup", "off_right", "run"), mv("pim", "off_right", "run", True),
                mv("zeek", "off_right", "run", True), mv("crispy", "off_right", "walk", True),
            ],
            "tail": 0.4,
        },
        {   # 3 bathroom: the lonely kettle, Lolly snaps
            "bg": "bathroom", "music": "heartbeat",
            "heroes": {"lolly": 300, "bup": 540, "pim": -300},
            "villain": {"type": "kettle", "x": 1450, "state": "asleep", "scale": 0.85},
            "beats": [
                {"sfx": "creak", "wait": 0.5},
                S("narr", "In the steamy bathroom, Old Hissy sits by the warm pipes, humming alone.|En el baño lleno de vapor, el Viejo Hissy se sienta junto a las tuberías, tarareando solo.|"
                  "Im dampfigen Bad sitzt der alte Hissy an den warmen Rohren und summt allein.|Dans la salle de bain pleine de vapeur, le Vieux Hissy fredonne seul près des tuyaux.|"
                  "Nel bagno pieno di vapore, il Vecchio Hissy siede vicino ai tubi caldi, canticchiando da solo.|No banheiro cheio de vapor, o Velho Hissy fica perto dos canos, cantarolando sozinho."),
                S("villain", "Hmm-hmm... nobody listens... nobody sips...|Mm-mm... nadie escucha... nadie bebe...|"
                  "Hmm-hmm... niemand hört zu... niemand trinkt...|Hum-hum... personne n'écoute... personne ne boit...|"
                  "Mm-mm... nessuno ascolta... nessuno beve...|Hum-hum... ninguém escuta... ninguém bebe..."),
                S("lolly", "Look at him. He's not scary. He's lonely.|Míralo. No da miedo. Está solo.|Schau ihn an. Er ist nicht gruselig. Er ist einsam.|"
                  "Regarde-le. Il ne fait pas peur. Il est seul.|Guardalo. Non fa paura. È solo.|Olha só. Ele não é assustador. Ele está sozinho."),
                S("bup", "Okay team, here's the plan. We say thank you. Really loud.|Bien, equipo, este es el plan. Decimos gracias. Muy fuerte.|"
                  "Okay Team, hier ist der Plan. Wir sagen danke. Ganz laut.|Bon, l'équipe, voici le plan. On dit merci. Très fort.|"
                  "Ok squadra, ecco il piano. Diciamo grazie. Molto forte.|Certo, equipe, o plano é este. A gente diz obrigado. Bem alto."),
                mv("pim", 800, "run"),
                S("pim", "I'm here! I c-came to help! Wait... is that STEAM?|¡Llegué! ¡V-vine a ayudar! Espera... ¿eso es VAPOR?|"
                  "Ich bin da! Ich w-will helfen! Moment... ist das DAMPF?|Je suis là ! J-je viens aider ! Attends... c'est de la VAPEUR ?|"
                  "Sono qui! S-sono venuto ad aiutare! Aspetta... quello è VAPORE?|Cheguei! E-eu vim ajudar! Espera... isso é VAPOR?"),
                {"villain": "wake"},
                {"villain": "roar"},
                S("villain", "YOU AGAIN?! Out, before I whistle your crusts off!|¡¿USTEDES OTRA VEZ?! ¡Fuera, antes de que les silbe la corteza!|"
                  "IHR SCHON WIEDER?! Raus, bevor ich euch die Kruste wegpfeife!|ENCORE VOUS ?! Dehors, avant que je siffle vos croûtes !|"
                  "ANCORA VOI?! Fuori, prima che vi fischi via la crosta!|VOCÊS DE NOVO?! Fora, antes que eu apite suas cascas!"),
                act("pim", "scream"),
                act("pim", "faint"),
                {"villain": "lunge", "to": 1200},
                mood("lolly", "angry"),
                {"shake": 0.5, "power": 14},
                S("lolly", "EXCUSE me! We came to say THANK YOU. Now SIT DOWN!|¡DISCULPA! Vinimos a decir GRACIAS. ¡Ahora SIÉNTATE!|"
                  "ENTSCHULDIGUNG! Wir wollen DANKE sagen. Jetzt SETZ DICH!|PARDON ! On est venus dire MERCI. Maintenant ASSIEDS-TOI !|"
                  "SCUSA! Siamo venuti a dire GRAZIE. Ora SIEDITI!|COM LICENÇA! Viemos dizer OBRIGADO. Agora SENTA!"),
                {"villain": "rage", "level": 0.1},
                S("villain", "...Th-thank you? For me?|...¿G-gracias? ¿A mí?|...D-danke? Für mich?|...M-merci ? Pour moi ?|...G-grazie? A me?|...O-obrigado? Pra mim?"),
                mood("lolly", "happy"),
                S("lolly", "For fifty years of hot water. And for being so loud and brave.|Por cincuenta años de agua caliente. Y por ser tan fuerte y valiente.|"
                  "Für fünfzig Jahre heißes Wasser. Und dafür, so laut und mutig zu sein.|Pour cinquante ans d'eau chaude. Et pour être si fort et si courageux.|"
                  "Per cinquant'anni di acqua calda. E per essere così forte e coraggioso.|Por cinquenta anos de água quente. E por ser tão barulhento e corajoso."),
                S("villain", "Nobody ever said that before... sniff.|Nadie me había dicho eso antes... snif.|Das hat noch nie jemand gesagt... schnief.|"
                  "Personne ne m'a jamais dit ça... snif.|Nessuno me l'aveva mai detto... snif.|Ninguém nunca me disse isso... snif."),
                act("pim", "jump"),
                S("pim", "Did... did the scary kettle just CRY?|¿La... la tetera aterradora acaba de LLORAR?|Hat... hat der gruselige Kessel gerade GEWEINT?|"
                  "Est-ce que... la bouilloire effrayante vient de PLEURER ?|Il... il bollitore spaventoso ha appena PIANTO?|A... a chaleira assustadora acabou de CHORAR?"),
                S("villain", "Steam in my eye. Now. Where is your cold little friend?|Vapor en el ojo. Bueno. ¿Dónde está su amiguito frío?|"
                  "Dampf im Auge. Also. Wo ist euer kalter kleiner Freund?|De la vapeur dans l'œil. Bon. Où est votre petit ami tout froid ?|"
                  "Vapore nell'occhio. Allora. Dov'è il vostro amichetto freddo?|Vapor no olho. Bom. Cadê o amiguinho gelado de vocês?"),
            ],
            "tail": 0.5,
        },
        {   # 4 kitchen: Crispy is saved
            "bg": "kitchen", "music": "heartbeat",
            "heroes": {"bup": 260, "zeek": 500, "crispy": 760},
            "moods": {"crispy": "scared", "zeek": "scared"},
            "villain": {"type": "kettle", "x": 2300, "state": "awake", "scale": 0.85},
            "beats": [
                {"card": "BACK IN THE KITCHEN...", "es": "DE VUELTA EN LA COCINA...", "dur": 2.0},
                S("zeek", "One minute left! His ember is almost gone!|¡Queda un minuto! ¡Su brasa casi se apaga!|"
                  "Noch eine Minute! Seine Glut ist fast weg!|Plus qu'une minute ! Sa braise est presque éteinte !|"
                  "Manca un minuto! La sua brace è quasi spenta!|Falta um minuto! A brasa dele está quase apagando!"),
                mv("villain", 1150, "walk"),
                S("villain", "Step aside, little crumbs. Hissy is on duty.|Apártense, migajitas. Hissy está de turno.|"
                  "Zur Seite, kleine Krümel. Hissy hat Dienst.|Poussez-vous, petites miettes. Hissy est de service.|"
                  "Fatevi da parte, briciole. Hissy è in servizio.|Saiam da frente, migalhinhas. O Hissy está de plantão."),
                S("narr", "Old Hissy takes a deep breath, and puffs warm, gentle steam.|El Viejo Hissy respira hondo y sopla un vapor tibio y suave.|"
                  "Der alte Hissy holt tief Luft und pustet warmen, sanften Dampf.|Le Vieux Hissy prend une grande inspiration et souffle une vapeur douce et tiède.|"
                  "Il Vecchio Hissy fa un respiro profondo e soffia un vapore caldo e gentile.|O Velho Hissy respira fundo e solta um vapor morno e suave."),
                {"sfx": "whoosh", "wait": 0.3},
                {"villain": "rage", "level": 0.5, "and": True},
                {"shake": 0.3, "power": 8},
                S("villain", "Not too hot... not too cold... just right.|Ni muy caliente... ni muy frío... perfecto.|"
                  "Nicht zu heiß... nicht zu kalt... genau richtig.|Pas trop chaud... pas trop froid... parfait.|"
                  "Né troppo caldo... né troppo freddo... perfetto.|Nem quente demais... nem frio demais... na medida."),
                {"wait": 1.0},
                act("crispy", "jump"),
                mood("crispy", "happy"),
                S("crispy", "I'm... warm. My fire... is back.|Estoy... tibio. Mi fuego... volvió.|Mir ist... warm. Mein Feuer... ist zurück.|"
                  "J'ai... chaud. Mon feu... est revenu.|Sono... caldo. Il mio fuoco... è tornato.|Estou... quente. Meu fogo... voltou."),
                mood(["bup", "zeek"], "happy"),
                act(["bup", "zeek"], "bounce"),
                S("bup", "Crispy! You're glowing brighter than ever!|¡Crispy! ¡Brillas más que nunca!|Crispy! Du leuchtest heller als je zuvor!|"
                  "Crispy ! Tu brilles plus que jamais !|Crispy! Brilli più che mai!|Crispy! Você está brilhando mais do que nunca!"),
                S("crispy", "Thank you, old kettle. I owe you one.|Gracias, vieja tetera. Te debo una.|Danke, alter Kessel. Ich schulde dir was.|"
                  "Merci, vieille bouilloire. Je t'en dois une.|Grazie, vecchio bollitore. Te ne devo una.|Obrigado, velha chaleira. Fico te devendo."),
                S("villain", "Hmph. Don't get mushy. ...Come back for tea sometime.|Hmpf. No se pongan cursis. ...Vengan a tomar té algún día.|"
                  "Hmpf. Nicht so rührselig. ...Kommt mal auf einen Tee vorbei.|Pff. Pas de sentiments. ...Revenez prendre le thé un jour.|"
                  "Uff. Niente smancerie. ...Tornate per un tè, qualche volta.|Hunf. Nada de melação. ...Voltem para um chá qualquer dia."),
            ],
            "tail": 0.5,
        },
        {   # 5 table: tea party + warning
            "bg": "table", "music": "music_box",
            "heroes": {"pim": 240, "lolly": 460, "bup": 680, "crispy": 900},
            "moods": {"pim": "happy", "lolly": "happy"},
            "villain": {"type": "kettle", "x": 1450, "state": "awake", "scale": 0.8},
            "beats": [
                S("narr", "That night, the Dough Bros throw a tea party for their grumpy new friend.|Esa noche, los Dough Bros hacen una fiesta de té para su nuevo amigo gruñón.|"
                  "In dieser Nacht feiern die Dough Bros eine Teeparty für ihren grummeligen neuen Freund.|Cette nuit-là, les Dough Bros organisent un goûter pour leur nouvel ami grognon.|"
                  "Quella notte, i Dough Bros danno un tè per il loro nuovo amico brontolone.|Naquela noite, os Dough Bros fazem um chá para o novo amigo rabugento."),
                S("lolly", "A cup for everyone! Hissy, you pour!|¡Una taza para todos! ¡Hissy, tú sirves!|Eine Tasse für alle! Hissy, du schenkst ein!|"
                  "Une tasse pour tout le monde ! Hissy, c'est toi qui sers !|Una tazza per tutti! Hissy, versi tu!|Uma xícara pra todo mundo! Hissy, você serve!"),
                {"sfx": "ding", "wait": 0.4},
                S("villain", "Fine. But only because I'm VERY good at it.|Bien. Pero solo porque soy MUY bueno en esto.|"
                  "Na gut. Aber nur, weil ich darin SEHR gut bin.|D'accord. Mais seulement parce que je suis TRÈS doué.|"
                  "Va bene. Ma solo perché sono MOLTO bravo.|Tá bom. Mas só porque eu sou MUITO bom nisso."),
                S("pim", "This is the b-best night ever. Nothing can go wrong!|Es la m-mejor noche de todas. ¡Nada puede salir mal!|"
                  "Das ist die b-beste Nacht überhaupt. Nichts kann schiefgehen!|C'est la m-meilleure nuit de ma vie. Rien ne peut mal tourner !|"
                  "È la m-migliore notte di sempre. Niente può andare storto!|É a m-melhor noite de todas. Nada pode dar errado!"),
                S("crispy", "Never say that.|Nunca digas eso.|Sag das niemals.|Ne dis jamais ça.|Non dirlo mai.|Nunca diga isso."),
                {"sfx": "creak", "wait": 0.8},
                mood(["pim", "lolly", "bup"], "scared"),
                {"villain": "rage", "level": 0.6},
                S("villain", "Listen. Mr. Pot asked me to join his army. I said no.|Escuchen. Mr. Pot me pidió unirme a su ejército. Dije que no.|"
                  "Hört zu. Mr. Pot wollte mich in seiner Armee. Ich sagte nein.|Écoutez. Mr. Pot m'a demandé de rejoindre son armée. J'ai dit non.|"
                  "Ascoltate. Mr. Pot mi ha chiesto di entrare nel suo esercito. Ho detto no.|Escutem. O Mr. Pot me chamou pro exército dele. Eu disse não."),
                S("bup", "His ARMY? Who else did he ask?|¿Su EJÉRCITO? ¿A quién más se lo pidió?|Seine ARMEE? Wen hat er noch gefragt?|"
                  "Son ARMÉE ? Qui d'autre a-t-il recruté ?|Il suo ESERCITO? Chi altro ha chiesto?|O EXÉRCITO dele? Quem mais ele chamou?"),
                S("villain", "The one in the closet. The one who is ALWAYS hungry.|Al del armario. Al que SIEMPRE tiene hambre.|"
                  "Den im Schrank. Den, der IMMER hungrig ist.|Celui du placard. Celui qui a TOUJOURS faim.|"
                  "Quello nell'armadio. Quello che ha SEMPRE fame.|O do armário. Aquele que está SEMPRE com fome."),
                act(["pim", "lolly"], "shake"),
            ],
            "tail": 0.5,
        },
        {   # 6 kitchen: Gulpzilla cliffhanger
            "bg": "kitchen", "music": "drone",
            "heroes": {"lolly": 260, "bup": 500, "pim": 760},
            "moods": {"pim": "happy"},
            "villain": {"type": "vacuum", "x": 1500, "state": "hidden", "scale": 0.9},
            "beats": [
                {"card": "LATER THAT NIGHT...", "es": "MÁS TARDE ESA NOCHE...", "dur": 2.0},
                S("pim", "Just one more cookie... all by myself... totally not scared.|Solo una galleta más... yo solito... nada de miedo.|"
                  "Nur noch ein Keks... ganz allein... überhaupt keine Angst.|Juste un dernier biscuit... tout seul... même pas peur.|"
                  "Solo un altro biscotto... tutto da solo... zero paura.|Só mais um biscoito... sozinho... nem um pouco de medo."),
                mv("pim", 1080, "walk"),
                {"sfx": "creak", "wait": 0.8},
                {"villain": "show"},
                {"villain": "wake"},
                {"villain": "roar"},
                S("villain", "MINE! All mine! Slurrrp!|¡MÍO! ¡Todo mío! ¡Sluuurp!|MEINS! Alles meins! Schlüüürf!|"
                  "À MOI ! Tout à moi ! Slurrrp !|MIO! Tutto mio! Slurrrp!|MEU! Tudo meu! Slurrrp!"),
                act("pim", "scream"),
                {"villain": "lunge", "to": 1200},
                {"sfx": "whoosh", "wait": 0.2, "and": True},
                act("pim", "hide"),
                mood(["bup", "lolly"], "scared"),
                act(["bup", "lolly"], "scream"),
                S("bup", "PIM! NOOO!|¡PIM! ¡NOOO!|PIM! NEEEIN!|PIM ! NOOON !|PIM! NOOO!|PIM! NÃÃÃO!"),
                S("villain", "Tell Mr. Pot... I got the first one. Hee hee... BURP!|Díganle a Mr. Pot... que tengo al primero. Ji ji... ¡BURP!|"
                  "Sagt Mr. Pot... ich habe den Ersten. Hi hi... RÜLPS!|Dites à Mr. Pot... que j'ai eu le premier. Hi hi... BURP !|"
                  "Dite a Mr. Pot... che ho preso il primo. Ih ih... BURP!|Digam ao Mr. Pot... que eu peguei o primeiro. Hi hi... ARROTO!"),
                mv("villain", "off_right", "run"),
                {"shake": 0.6, "power": 18},
            ],
            "tail": 0.8,
        },
    ],
}

SHORT_TAGS = ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy", "animated series"]

short1 = {
    "id": "ep006_short1", "format": "short",
    "title": "Pim says he's NOT scared 😂 #shorts",
    "hook": "Pim is SO brave...",
    "description": "Pim is not scared of anything. Not even a sleepy old kettle. Right? #shorts #animation #cartoon #doughbros #funny",
    "tags": SHORT_TAGS + ["pim", "jump scare"],
    "thumbnail": {"bg": "bathroom", "villain": "kettle", "heroes": ["pim"], "text": "SO BRAVE!"},
    "scenes": [{
        "bg": "bathroom", "music": "heartbeat",
        "heroes": {"pim": 600},
        "villain": {"type": "kettle", "x": 1450, "state": "asleep", "scale": 0.85},
        "beats": [
            S("pim", "I'm not scared. Not even a little. Watch this.|No tengo miedo. Ni un poquito. Mira esto.|"
              "Ich habe keine Angst. Kein bisschen. Pass auf.|Je n'ai pas peur. Même pas un peu. Regarde.|"
              "Non ho paura. Neanche un po'. Guarda qua.|Eu não tenho medo. Nem um pouquinho. Olha só."),
            mv("pim", 1000, "walk"),
            S("pim", "See? Just a sleepy old kettle. Hello, kettle!|¿Ves? Solo una vieja tetera dormida. ¡Hola, tetera!|"
              "Siehst du? Nur ein schläfriger alter Kessel. Hallo, Kessel!|Tu vois ? Juste une vieille bouilloire endormie. Salut, bouilloire !|"
              "Visto? Solo un vecchio bollitore addormentato. Ciao, bollitore!|Viu? Só uma chaleira velha dormindo. Oi, chaleira!"),
            {"sfx": "ding", "wait": 0.2},
            {"villain": "wake"},
            {"villain": "rage", "level": 1.0},
            {"shake": 0.6, "power": 22, "and": True},
            S("villain", "SSSSSS! I'm BOILING!|¡SSSSSS! ¡Estoy HIRVIENDO!|SSSSSS! Ich KOCHE!|SSSSSS ! Je BOUS !|SSSSSS! Sto BOLLENDO!|SSSSSS! Estou FERVENDO!"),
            act("pim", "scream"),
            act("pim", "faint"),
            {"villain": "rage", "level": 0.2},
            S("villain", "...Was it something I said?|...¿Fue algo que dije?|...Lag es an etwas, das ich gesagt habe?|"
              "...C'est quelque chose que j'ai dit ?|...Ho detto qualcosa di male?|...Foi algo que eu disse?"),
        ],
        "tail": 0.8,
    }],
}

short2 = {
    "id": "ep006_short2", "format": "short",
    "title": "Would YOU hug a BOILING kettle? 👇 #shorts",
    "hook": "Hug him... or RUN?",
    "description": "Old Hissy hasn't had a hug in fifty years. Lolly wants to help. Bup says no way. Would YOU hug him? Comment YES or NO! #shorts #animation #cartoon #doughbros",
    "tags": SHORT_TAGS + ["old hissy", "lolly", "would you"],
    "thumbnail": {"bg": "table", "villain": "kettle", "heroes": ["lolly", "bup"], "text": "HUG HIM?"},
    "scenes": [{
        "bg": "table", "music": "music_box",
        "heroes": {"bup": 320, "lolly": 600},
        "moods": {"lolly": "happy"},
        "villain": {"type": "kettle", "x": 1400, "state": "awake", "scale": 0.85},
        "beats": [
            S("villain", "Nobody has hugged me in fifty years. Sniff.|Nadie me ha abrazado en cincuenta años. Snif.|"
              "Niemand hat mich seit fünfzig Jahren umarmt. Schnief.|Personne ne m'a serré dans ses bras depuis cinquante ans. Snif.|"
              "Nessuno mi abbraccia da cinquant'anni. Snif.|Ninguém me abraça há cinquenta anos. Snif."),
            S("lolly", "Aww! I'll hug you!|¡Aww! ¡Yo te abrazo!|Ohh! Ich umarme dich!|Ohh ! Moi, je vais te faire un câlin !|Ooh! Ti abbraccio io!|Own! Eu te abraço!"),
            mv("lolly", 1000, "walk"),
            mood("bup", "scared"),
            S("bup", "Lolly, STOP! He's two hundred degrees!|¡Lolly, ALTO! ¡Está a doscientos grados!|Lolly, STOPP! Er hat zweihundert Grad!|"
              "Lolly, ARRÊTE ! Il fait deux cents degrés !|Lolly, FERMA! È a duecento gradi!|Lolly, PARA! Ele está a duzentos graus!"),
            {"villain": "rage", "level": 0.9},
            {"sfx": "whoosh", "wait": 0.2, "and": True},
            {"shake": 0.5, "power": 14},
            act("lolly", "jump"),
            S("lolly", "Ouch! Hot hot hot! ...Still worth it.|¡Ay! ¡Quema, quema! ...Valió la pena.|Autsch! Heiß, heiß! ...Trotzdem gut.|"
              "Aïe ! Chaud, chaud ! ...Ça valait le coup.|Ahia! Scotta, scotta! ...Ne valeva la pena.|Ai! Quente, quente! ...Valeu a pena."),
            S("narr", "Would YOU hug Old Hissy? Comment YES or NO!|¿Abrazarías TÚ al Viejo Hissy? ¡Comenta SÍ o NO!|"
              "Würdest DU den alten Hissy umarmen? Schreib JA oder NEIN!|Et TOI, tu ferais un câlin au Vieux Hissy ? Écris OUI ou NON !|"
              "E TU abbracceresti il Vecchio Hissy? Scrivi SÌ o NO!|VOCÊ abraçaria o Velho Hissy? Comente SIM ou NÃO!"),
        ],
        "tail": 1.0,
    }],
}

short3 = {
    "id": "ep006_short3", "format": "short",
    "title": "Something in the closet is HUNGRY 😱 #shorts",
    "hook": "Don't go for the cookie...",
    "description": "Pim just wanted one more cookie. The closet had other plans. Full episode on the channel! #shorts #animation #cartoon #doughbros",
    "tags": SHORT_TAGS + ["gulpzilla", "pim", "jump scare"],
    "thumbnail": {"bg": "kitchen", "villain": "vacuum", "heroes": ["pim", "bup"], "text": "IT'S HUNGRY!"},
    "scenes": [{
        "bg": "kitchen", "music": "drone",
        "heroes": {"bup": 300, "pim": 640},
        "moods": {"pim": "happy"},
        "villain": {"type": "vacuum", "x": 1450, "state": "hidden", "scale": 0.9},
        "beats": [
            S("pim", "Just one more cookie... totally not scared.|Solo una galleta más... nada de miedo.|Nur noch ein Keks... überhaupt keine Angst.|"
              "Juste un dernier biscuit... même pas peur.|Solo un altro biscotto... zero paura.|Só mais um biscoito... nem um pouco de medo."),
            mv("pim", 1000, "walk"),
            {"sfx": "creak", "wait": 0.6},
            {"villain": "show"},
            {"villain": "wake"},
            {"villain": "roar"},
            S("villain", "MINE! All mine! Slurrrp!|¡MÍO! ¡Todo mío! ¡Sluuurp!|MEINS! Alles meins! Schlüüürf!|"
              "À MOI ! Tout à moi ! Slurrrp !|MIO! Tutto mio! Slurrrp!|MEU! Tudo meu! Slurrrp!"),
            act("pim", "scream"),
            {"villain": "lunge", "to": 1150},
            {"sfx": "whoosh", "wait": 0.2, "and": True},
            act("pim", "hide"),
            mood("bup", "scared"),
            S("bup", "PIM?! Where did he GO?!|¡¿PIM?! ¡¿Adónde SE FUE?!|PIM?! Wo ist er HIN?!|PIM ?! Où est-il PASSÉ ?!|PIM?! Dov'è FINITO?!|PIM?! Pra onde ele FOI?!"),
            {"shake": 0.6, "power": 18},
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

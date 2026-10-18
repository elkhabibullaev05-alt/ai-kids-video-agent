"""Generator for EP16 (Treasure map, Frostbite). Run: python3 scripts/_gen_ep016.py"""
import json, os

D = os.path.dirname(os.path.abspath(__file__))


def L(who, en, es, de, fr, it, pt, **kw):
    b = {"say": who, "en": en, "es": es, "de": de, "fr": fr, "it": it, "pt": pt}
    b.update(kw)
    return b


def mv(who, to, speed="run", **kw):
    b = {"move": who, "to": to, "speed": speed}; b.update(kw); return b


def act(who, do, **kw):
    b = {"act": who if isinstance(who, list) else [who], "do": do}; b.update(kw); return b


def mood(who, is_, **kw):
    b = {"mood": who if isinstance(who, list) else [who], "is": is_}; b.update(kw); return b


def V(what, **kw):
    b = {"villain": what}; b.update(kw); return b


def F(**kw):
    b = {"flash": 0.8, "thunder": False}; b.update(kw); return b


def SFX(name, wait=0.3, **kw):
    b = {"sfx": name, "wait": wait}; b.update(kw); return b


A = True
FR = {"type": "frost", "x": 1450, "state": "awake", "scale": 0.9}

long_scenes = [
    # 1 cold open: freezer, Frostbite rises (motion + line at 0 s)
    {"bg": "freezer", "music": "heartbeat", "heroes": {"bup": 330, "pim": 560, "zeek": 790, "lolly": 1010},
     "moods": {"pim": "scared", "zeek": "scared"}, "villain": dict(FR), "tail": 0.1,
     "beats": [
         V("lunge", to=1250),
         L("villain", "Stay... forever... COLD!", "Quedaos... para siempre... ¡FRÍOS!", "Bleibt... für immer... KALT!",
           "Restez... pour toujours... FROIDS !", "Restate... per sempre... FREDDI!", "Fiquem... para sempre... GELADOS!", and_=1),
         act(["bup", "pim", "zeek", "lolly"], "jump", and_=1), mood(["bup", "lolly"], "scared", and_=1),
         {"shake": 0.8, "power": 30, "and": A}, SFX("ice", 0.1, and_=1),
         act("pim", "scream"),
         L("pim", "M-my breath is making CLOUDS!", "¡M-mi aliento hace NUBES!", "M-mein Atem macht WOLKEN!",
           "M-mon souffle fait des NUAGES !", "Il m-mio fiato fa le NUVOLE!", "M-meu bafo tá fazendo NUVEM!"),
         L("narr", "The map led them here. The Golden Crumb is under the ice... and so is HE.",
           "El mapa los trajo aquí. La Miga Dorada está bajo el hielo... y ÉL también.",
           "Die Karte führte sie hierher. Der Goldene Krümel liegt unter dem Eis... und ER auch.",
           "La carte les a menés ici. La Miette d'Or est sous la glace... et LUI aussi.",
           "La mappa li ha portati qui. La Briciola d'Oro è sotto il ghiaccio... e anche LUI.",
           "O mapa trouxe eles até aqui. A Migalha Dourada está sob o gelo... e ELE também."),
         V("lunge", to=1100), {"shake": 0.6, "power": 24, "and": A},
         L("bup", "Back to the kitchen! RUN!", "¡A la cocina! ¡CORRED!", "Zurück in die Küche! LAUFT!",
           "Retour à la cuisine ! COUREZ !", "Torniamo in cucina! CORRETE!", "De volta pra cozinha! CORRE!"),
         mv("bup", "off_left", and_=1), mv("pim", "off_left", and_=1), mv("zeek", "off_left", and_=1),
         mv("lolly", "off_left", and_=1),
     ]},
    # 2 kitchen: map + Crispy appears
    {"bg": "kitchen", "music": "drone", "cut": True,
     "heroes": {"bup": 380, "pim": 600, "zeek": 830, "lolly": 1060, "crispy": 2200},
     "moods": {"pim": "scared"}, "tail": 0.1,
     "beats": [
         act(["bup", "pim", "zeek", "lolly"], "shake"),
         L("zeek", "My calculations say the X is right under Frostbite's ice.",
           "Mis cálculos dicen que la X está justo bajo el hielo de Frostbite.",
           "Meine Berechnungen sagen: Das X liegt genau unter Frostbites Eis.",
           "Mes calculs disent que le X est juste sous la glace de Frostbite.",
           "I miei calcoli dicono che la X è proprio sotto il ghiaccio di Frostbite.",
           "Meus cálculos dizem que o X está bem embaixo do gelo do Frostbite."),
         L("lolly", "Then we need something warm. Really, really warm.",
           "Entonces necesitamos algo caliente. Muy, muy caliente.",
           "Dann brauchen wir etwas Warmes. Richtig, richtig warm.",
           "Alors il nous faut quelque chose de chaud. Très, très chaud.",
           "Allora ci serve qualcosa di caldo. Molto, molto caldo.",
           "Então a gente precisa de algo quente. Muito, muito quente."),
         mv("crispy", 1350, "walk"),
         L("crispy", "Something... like me?", "¿Algo... como yo?", "Etwas... wie mich?", "Quelque chose... comme moi ?",
           "Qualcosa... come me?", "Algo... tipo eu?"),
         act(["bup", "pim", "zeek", "lolly"], "jump", and_=1), SFX("sting", 0.1, and_=1),
         act("pim", "faint"),
         L("bup", "Crispy! Your fire went out in the fridge!", "¡Crispy! ¡Tu fuego se apagó en la nevera!",
           "Crispy! Dein Feuer ist im Kühlschrank ausgegangen!", "Crispy ! Ton feu s'est éteint dans le frigo !",
           "Crispy! Il tuo fuoco si è spento nel frigo!", "Crispy! Seu fogo apagou na geladeira!"),
         L("crispy", "Almost. One spark left. Enough for one hole in the ice.",
           "Casi. Me queda una chispa. Suficiente para un agujero en el hielo.",
           "Fast. Ein Funke ist übrig. Genug für ein Loch im Eis.",
           "Presque. Il me reste une étincelle. Assez pour un trou dans la glace.",
           "Quasi. Mi resta una scintilla. Basta per un buco nel ghiaccio.",
           "Quase. Sobrou uma faísca. Dá pra um buraco no gelo."),
     ]},
    # 3 table: the plan
    {"bg": "table", "music": "music_box", "cut": True,
     "heroes": {"bup": 360, "pim": 600, "zeek": 840, "lolly": 1080, "crispy": 1320}, "tail": 0.1,
     "beats": [
         act("bup", "bounce"),
         L("bup", "Okay team, here's the plan. Lolly keeps Frostbite busy.",
           "Vale, equipo, este es el plan. Lolly distrae a Frostbite.",
           "Okay Team, hier ist der Plan. Lolly lenkt Frostbite ab.",
           "OK l'équipe, voici le plan. Lolly occupe Frostbite.",
           "Ok squadra, ecco il piano. Lolly tiene occupato Frostbite.",
           "Beleza, equipe, o plano é esse. A Lolly distrai o Frostbite."),
         L("bup", "Crispy melts the ice. Zeek grabs the crumb.", "Crispy derrite el hielo. Zeek agarra la miga.",
           "Crispy schmilzt das Eis. Zeek schnappt sich den Krümel.", "Crispy fait fondre la glace. Zeek attrape la miette.",
           "Crispy scioglie il ghiaccio. Zeek prende la briciola.", "O Crispy derrete o gelo. O Zeek pega a migalha."),
         L("pim", "A-and me?", "¿Y-y yo?", "U-und ich?", "E-et moi ?", "E-e io?", "E-e eu?"),
         L("bup", "You... hold the map.", "Tú... sujetas el mapa.", "Du... hältst die Karte.", "Toi... tu tiens la carte.",
           "Tu... tieni la mappa.", "Você... segura o mapa."),
         mood("pim", "happy"), act("pim", "jump", and_=1),
         L("pim", "Best. Job. EVER.", "Mejor. Trabajo. DEL MUNDO.", "Bester. Job. ALLER ZEITEN.", "Meilleur. Boulot. DU MONDE.",
           "Miglior. Lavoro. DI SEMPRE.", "Melhor. Trabalho. DO MUNDO."),
     ]},
    # 4 Zeek's gadget backfires
    {"bg": "kitchen", "music": "drone", "cut": True,
     "heroes": {"zeek": 760, "lolly": 1080}, "moods": {"zeek": "happy"}, "tail": 0.1,
     "beats": [
         act("zeek", "bounce"),
         L("zeek", "Backup plan! My new Thaw-O-Matic! Three... two... one... THAW!",
           "¡Plan B! ¡Mi nuevo Descongelatrón! Tres... dos... uno... ¡YA!",
           "Plan B! Mein neuer Auftau-O-Mat! Drei... zwei... eins... TAU!",
           "Plan B ! Mon nouveau Dégel-O-Matic ! Trois... deux... un... DÉGÈLE !",
           "Piano B! Il mio nuovo Scongela-Matic! Tre... due... uno... VIA!",
           "Plano B! Meu novo Descongela-Tron! Três... dois... um... JÁ!"),
         SFX("pop", 0.1), act("zeek", "spin", and_=1), SFX("ice", 0.3, and_=1), mood("zeek", "scared"),
         L("zeek", "It made... ice cubes. Hundreds of ice cubes.", "Hizo... cubitos de hielo. Cientos de cubitos.",
           "Er hat... Eiswürfel gemacht. Hunderte Eiswürfel.", "Il a fait... des glaçons. Des centaines de glaçons.",
           "Ha fatto... cubetti di ghiaccio. Centinaia di cubetti.", "Ele fez... cubos de gelo. Centenas de cubos."),
         L("lolly", "Zeek, sweetie. You pressed the FREEZE button.", "Zeek, cielo. Pulsaste el botón de CONGELAR.",
           "Zeek, Schätzchen. Du hast den GEFRIER-Knopf gedrückt.", "Zeek, mon chou. Tu as appuyé sur CONGELER.",
           "Zeek, tesoro. Hai premuto il tasto CONGELA.", "Zeek, querido. Você apertou o botão de CONGELAR."),
         act("zeek", "faint"),
     ]},
    # 5 freezer: Lolly sings
    {"bg": "freezer", "music": "music_box", "cut": True,
     "heroes": {"lolly": 700}, "moods": {"lolly": "happy"},
     "villain": dict(FR, state="asleep"), "tail": 0.1,
     "beats": [
         mv("lolly", 900, "walk"),
         L("lolly", "Hellooo, Mister Frostbite! I brought you a song!", "¡Holaaa, señor Frostbite! ¡Le traje una canción!",
           "Halloo, Herr Frostbite! Ich hab dir ein Lied mitgebracht!", "Coucouuu, monsieur Frostbite ! Je vous ai apporté une chanson !",
           "Ciaooo, signor Frostbite! Ti ho portato una canzone!", "Oláaa, senhor Frostbite! Eu trouxe uma música!"),
         V("wake"), SFX("ice", 0.2, and_=1),
         L("villain", "A song? Nobody... sings... to me.", "¿Una canción? Nadie... me... canta.",
           "Ein Lied? Niemand... singt... für mich.", "Une chanson ? Personne... ne me... chante.",
           "Una canzone? Nessuno... canta... per me.", "Uma música? Ninguém... canta... pra mim."),
         act("lolly", "bounce"),
         L("lolly", "La la la, the ice is nice, the snow is slow, la la LA!",
           "La la la, el hielo es bello, la nieve es leve, ¡la la LA!",
           "La la la, das Eis ist leis, der Schnee tut nicht weh, la la LA!",
           "La la la, la glace est sympa, la neige me protège, la la LA !",
           "La la la, il ghiaccio è un abbraccio, la neve è lieve, la la LA!",
           "Lá lá lá, o gelo é belo, a neve é leve, lá lá LÁ!"),
         L("villain", "Again... sing it... AGAIN.", "Otra vez... cántala... OTRA VEZ.", "Nochmal... sing es... NOCHMAL.",
           "Encore... chante-la... ENCORE.", "Ancora... cantala... ANCORA.", "De novo... canta... DE NOVO."),
     ]},
    # 6 freezer, ice: Crispy melts
    {"bg": "freezer", "music": "heartbeat", "cut": True,
     "heroes": {"crispy": 520, "zeek": 820, "pim": 1100}, "moods": {"pim": "scared"}, "tail": 0.1,
     "beats": [
         mv("crispy", 640, "walk", and_=0), mv("zeek", 900, "walk", and_=1), mv("pim", 1160, "walk", and_=1),
         L("crispy", "Stand back. This spark is all I have.", "Atrás. Esta chispa es todo lo que tengo.",
           "Zurück. Dieser Funke ist alles, was ich habe.", "Reculez. Cette étincelle, c'est tout ce qui me reste.",
           "State indietro. Questa scintilla è tutto ciò che ho.", "Pra trás. Essa faísca é tudo que eu tenho."),
         F(), act("crispy", "shake", and_=1), SFX("creak", 0.4), SFX("ice", 0.3),
         L("zeek", "It's working! I can see GOLD down there!", "¡Funciona! ¡Veo ORO ahí abajo!",
           "Es klappt! Ich sehe da unten GOLD!", "Ça marche ! Je vois de l'OR là-dessous !",
           "Funziona! Vedo dell'ORO là sotto!", "Tá funcionando! Eu tô vendo OURO lá embaixo!"),
         act("pim", "shake"),
         L("pim", "Ah... ah... AH...", "Ah... ah... AH...", "Ha... ha... HA...", "Ah... ah... AH...", "Ah... ah... AH...",
           "Ah... ah... AH..."),
         L("zeek", "Pim. Don't. You. DARE.", "Pim. Ni. Se. Te. OCURRA.", "Pim. Wag. Es. NICHT.", "Pim. N'ose. Pas. ÇA.",
           "Pim. Non. Ti. AZZARDARE.", "Pim. Nem. Pensa. NISSO."),
         act("pim", "jump"), SFX("pop", 0.1, and_=1),
         L("pim", "ACHOO!", "¡ACHÍS!", "HATSCHI!", "ATCHOUM !", "ETCIÙ!", "ATCHIM!", and_=1),
         {"shake": 0.5, "power": 20, "and": A},
     ]},
    # 7 freezer: Frostbite roars
    {"bg": "freezer", "music": "heartbeat", "cut": True,
     "heroes": {"lolly": 520, "zeek": 780, "pim": 1000}, "moods": {"lolly": "scared", "zeek": "scared", "pim": "scared"},
     "villain": dict(FR, x=1500), "tail": 0.1,
     "beats": [
         V("roar"), {"shake": 0.9, "power": 32, "and": A}, act(["lolly", "zeek", "pim"], "jump", and_=1),
         L("villain", "THIEVES! You came for my CRUMB!", "¡LADRONES! ¡Vinisteis por mi MIGA!",
           "DIEBE! Ihr wolltet meinen KRÜMEL!", "VOLEURS ! Vous êtes venus pour ma MIETTE !",
           "LADRI! Siete venuti per la mia BRICIOLA!", "LADRÕES! Vocês vieram pela minha MIGALHA!"),
         L("lolly", "Run! The song is OVER!", "¡Corred! ¡Se acabó la canción!", "Lauft! Das Lied ist AUS!",
           "Courez ! La chanson est FINIE !", "Correte! La canzone è FINITA!", "Corre! A música ACABOU!"),
         mv("lolly", "off_left", and_=1), mv("zeek", "off_left", and_=1), mv("pim", "off_left", and_=1),
         V("lunge", to=900, and_=1),
     ]},
    # 8 fridge chase: Pim frozen, Lolly snaps
    {"bg": "fridge", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 330, "lolly": 560, "pim": 820}, "moods": {"bup": "scared", "pim": "scared"},
     "villain": dict(FR, x=1550), "tail": 0.1,
     "beats": [
         L("bup", "Into the fridge! Hide behind the jam!", "¡A la nevera! ¡Detrás de la mermelada!",
           "In den Kühlschrank! Hinter die Marmelade!", "Dans le frigo ! Derrière la confiture !",
           "Nel frigo! Dietro la marmellata!", "Pra geladeira! Atrás da geleia!"),
         V("lunge", to=1250), SFX("ice", 0.2, and_=1), act("pim", "shake", and_=1),
         L("pim", "I c-can't move! My f-feet are FROZEN!", "¡N-no puedo moverme! ¡Tengo los p-pies CONGELADOS!",
           "Ich k-kann mich nicht bewegen! Meine F-Füße sind GEFROREN!", "J-je ne peux plus bouger ! Mes p-pieds sont GELÉS !",
           "N-non riesco a muovermi! I miei p-piedi sono GELATI!", "N-não consigo mexer! Meus p-pés CONGELARAM!"),
         L("villain", "One little bean... forever COLD.", "Un frijolito... FRÍO para siempre.",
           "Eine kleine Bohne... für immer KALT.", "Un petit haricot... FROID pour toujours.",
           "Un fagiolino... FREDDO per sempre.", "Um feijãozinho... GELADO pra sempre."),
         mood("lolly", "angry"), act("lolly", "shake", and_=1), V("rage", level=0.0, and_=1),
         L("lolly", "Excuse me. NOBODY freezes my friends!", "Disculpa. ¡NADIE congela a mis amigos!",
           "Entschuldigung. NIEMAND friert meine Freunde ein!", "Pardon. PERSONNE ne gèle mes amis !",
           "Scusa. NESSUNO congela i miei amici!", "Com licença. NINGUÉM congela meus amigos!"),
         mv("lolly", 1000, "run"), {"shake": 0.7, "power": 28, "and": A}, V("lunge", to=1550, and_=1),
         L("villain", "The cookie... is... TERRIFYING.", "La galleta... da... MIEDO.", "Der Keks... ist... FURCHTERREGEND.",
           "Le biscuit... est... TERRIFIANT.", "Il biscotto... è... TERRIFICANTE.", "A bolacha... é... ASSUSTADORA."),
         mood("pim", "happy"), act("pim", "jump", and_=1),
     ]},
    # 8b table: where's the map?
    {"bg": "table", "music": "drone", "cut": True,
     "heroes": {"bup": 420, "pim": 680, "lolly": 940}, "moods": {"bup": "scared", "pim": "scared"}, "tail": 0.1,
     "beats": [
         act(["bup", "pim", "lolly"], "shake"),
         L("bup", "Okay. Everyone's here. Pim, where's the map?", "Vale. Estamos todos. Pim, ¿dónde está el mapa?",
           "Okay. Alle da. Pim, wo ist die Karte?", "OK. Tout le monde est là. Pim, où est la carte ?",
           "Ok. Ci siamo tutti. Pim, dov'è la mappa?", "Beleza. Tá todo mundo aqui. Pim, cadê o mapa?"),
         L("pim", "I... might have sneezed on it.", "Puede que... le haya estornudado encima.",
           "Ich... hab vielleicht draufgeniest.", "J'ai... peut-être éternué dessus.",
           "Potrei... averci starnutito sopra.", "Eu... talvez tenha espirrado nele."),
         SFX("ice", 0.3),
         L("pim", "Now it's a map-sicle.", "Ahora es un mapa-polo.", "Jetzt ist es ein Karten-Eis am Stiel.",
           "Maintenant c'est une carte glacée.", "Adesso è un ghiacciolo-mappa.", "Agora é um mapa-picolé."),
         mood("lolly", "happy"), act("lolly", "bounce", and_=1),
         L("lolly", "Don't worry. Zeek and Crispy are still in there!", "Tranquilos. ¡Zeek y Crispy siguen ahí dentro!",
           "Keine Sorge. Zeek und Crispy sind noch drin!", "Pas de panique. Zeek et Crispy sont encore dedans !",
           "Tranquilli. Zeek e Crispy sono ancora lì dentro!", "Calma. O Zeek e o Crispy ainda tão lá dentro!"),
         mood(["bup", "pim"], "scared"), act(["bup", "pim"], "jump", and_=1),
         L("bup", "Wait. They're STILL in there?!", "Espera. ¿¡SIGUEN ahí dentro!?", "Moment. Die sind NOCH da drin?!",
           "Attends. Ils sont ENCORE dedans ?!", "Aspetta. Sono ANCORA lì dentro?!", "Peraí. Eles AINDA tão lá dentro?!"),
     ]},
    # 9 freezer: crumb comes free, Crispy fades
    {"bg": "freezer", "music": "drone", "cut": True,
     "heroes": {"crispy": 560, "zeek": 860}, "tail": 0.1,
     "beats": [
         F(), SFX("ice", 0.2, and_=1), SFX("ding", 0.3),
         L("zeek", "Got it! The GOLDEN CRUMB! It's... warm!", "¡La tengo! ¡La MIGA DORADA! ¡Está... calentita!",
           "Hab ihn! Der GOLDENE KRÜMEL! Er ist... warm!", "Je l'ai ! La MIETTE D'OR ! Elle est... chaude !",
           "Presa! La BRICIOLA D'ORO! È... calda!", "Peguei! A MIGALHA DOURADA! Ela tá... quentinha!"),
         act("zeek", "jump"),
         L("crispy", "Good. Because I... am... not.", "Bien. Porque yo... no... lo estoy.", "Gut. Denn ich... bin... es nicht.",
           "Bien. Parce que moi... je ne... le suis pas.", "Bene. Perché io... non... lo sono.", "Ótimo. Porque eu... não... tô."),
         act("crispy", "faint"),
         L("zeek", "Crispy! Hold on, buddy! Let's get you warm!", "¡Crispy! ¡Aguanta, amigo! ¡Vamos a calentarte!",
           "Crispy! Halt durch, Kumpel! Wir wärmen dich auf!", "Crispy ! Tiens bon, mon pote ! On va te réchauffer !",
           "Crispy! Resisti, amico! Ti scaldiamo noi!", "Crispy! Aguenta, amigão! Vamos te esquentar!"),
     ]},
    # 10 kitchen: crumb warms Crispy, Frostbite sad
    {"bg": "kitchen", "music": "music_box", "cut": True,
     "heroes": {"bup": 330, "pim": 560, "zeek": 790, "lolly": 1020, "crispy": 1250},
     "moods": {"bup": "happy"}, "tail": 0.1,
     "beats": [
         SFX("ding", 0.3), F(), act("crispy", "show", and_=1), act("crispy", "jump"),
         L("narr", "The Golden Crumb glowed... and Crispy's ember came back to life.",
           "La Miga Dorada brilló... y la brasa de Crispy volvió a la vida.",
           "Der Goldene Krümel leuchtete... und Crispys Glut erwachte wieder.",
           "La Miette d'Or a brillé... et la braise de Crispy s'est rallumée.",
           "La Briciola d'Oro brillò... e la brace di Crispy tornò in vita.",
           "A Migalha Dourada brilhou... e a brasa do Crispy voltou à vida."),
         L("crispy", "I'm... warm. I haven't been warm in years.", "Tengo... calor. Hace años que no tenía calor.",
           "Mir ist... warm. Seit Jahren war mir nicht mehr warm.", "J'ai... chaud. Ça faisait des années.",
           "Ho... caldo. Erano anni che non avevo caldo.", "Eu tô... quente. Faz anos que eu não ficava quente."),
         act(["bup", "pim", "zeek", "lolly"], "bounce"),
         L("pim", "Group hug! Careful, he's HOT now!", "¡Abrazo de grupo! ¡Cuidado, ahora QUEMA!",
           "Gruppenumarmung! Vorsicht, er ist jetzt HEISS!", "Câlin collectif ! Attention, il BRÛLE maintenant !",
           "Abbraccio di gruppo! Attenti, ora SCOTTA!", "Abraço coletivo! Cuidado, agora ele QUEIMA!"),
         SFX("sting", 0.1), mood(["pim", "zeek"], "scared", and_=1),
         L("zeek", "Wait. Look at the crumb. It's pointing somewhere.", "Esperad. Mirad la miga. Señala a algún sitio.",
           "Moment. Seht euch den Krümel an. Er zeigt irgendwohin.", "Attendez. Regardez la miette. Elle montre quelque chose.",
           "Aspettate. Guardate la briciola. Indica un posto.", "Espera. Olha a migalha. Ela tá apontando pra algum lugar."),
         L("lolly", "It's pointing at... the oven.", "Señala... al horno.", "Er zeigt... auf den Ofen.",
           "Elle montre... le four.", "Indica... il forno.", "Ela aponta... pro forno."),
         L("bup", "Mr. Pot's oven. Of course it is.", "El horno del señor Pot. Claro que sí.",
           "Mr. Pots Ofen. Natürlich.", "Le four de Mr. Pot. Évidemment.", "Il forno di Mr. Pot. Ovviamente.",
           "O forno do Mr. Pot. Claro que é."),
     ]},
    # 11 freezer: Frostbite alone
    {"bg": "freezer", "music": "music_box", "cut": True,
     "heroes": {"lolly": 700}, "villain": dict(FR, x=1400), "tail": 0.1,
     "beats": [
         L("villain", "My crumb... was the only warm thing... I ever had.",
           "Mi miga... era lo único caliente... que tenía.", "Mein Krümel... war das einzig Warme... das ich je hatte.",
           "Ma miette... était la seule chose chaude... que j'avais.", "La mia briciola... era l'unica cosa calda... che avevo.",
           "Minha migalha... era a única coisa quente... que eu tinha."),
         mv("lolly", 900, "walk"),
         L("lolly", "Then come sing with us sometimes. Songs are warm too.",
           "Entonces ven a cantar con nosotros. Las canciones también dan calor.",
           "Dann komm manchmal mit uns singen. Lieder wärmen auch.",
           "Alors viens chanter avec nous. Les chansons, ça réchauffe aussi.",
           "Allora vieni a cantare con noi. Anche le canzoni scaldano.",
           "Então vem cantar com a gente às vezes. Música também esquenta."),
         V("sleep"), SFX("ice", 0.4, and_=1),
         L("villain", "Maybe... la la... la...", "Quizás... la la... la...", "Vielleicht... la la... la...",
           "Peut-être... la la... la...", "Forse... la la... la...", "Talvez... lá lá... lá..."),
     ]},
    # 12 oven: cliffhanger
    {"bg": "oven", "music": "heartbeat", "cut": True,
     "heroes": {"bup": 330, "pim": 560, "zeek": 790, "crispy": 1020}, "moods": {"pim": "scared"},
     "villain": {"type": "pot", "x": 1500, "state": "asleep", "scale": 0.9}, "tail": 0.2,
     "beats": [
         mv("bup", 420, "walk"), mv("crispy", 1080, "walk", and_=1),
         L("bup", "The oven is cold. Mr. Pot is still asleep. We're safe.",
           "El horno está frío. El señor Pot sigue dormido. Estamos a salvo.",
           "Der Ofen ist kalt. Mr. Pot schläft noch. Wir sind sicher.",
           "Le four est froid. Mr. Pot dort encore. On est en sécurité.",
           "Il forno è freddo. Mr. Pot dorme ancora. Siamo al sicuro.",
           "O forno tá frio. O Mr. Pot ainda tá dormindo. Estamos seguros."),
         L("crispy", "No. A sleeping pot doesn't SMILE.", "No. Una olla dormida no SONRÍE.",
           "Nein. Ein schlafender Topf LÄCHELT nicht.", "Non. Une marmite endormie ne SOURIT pas.",
           "No. Una pentola che dorme non SORRIDE.", "Não. Panela dormindo não SORRI."),
         SFX("sting", 0.2), V("wake"), {"shake": 0.6, "power": 22, "and": A},
         L("villain", "Thank you, little doughs. You found my Golden Crumb...",
           "Gracias, masitas. Encontrasteis mi Miga Dorada...", "Danke, kleine Teiglinge. Ihr habt meinen Goldenen Krümel gefunden...",
           "Merci, petites pâtes. Vous avez trouvé ma Miette d'Or...", "Grazie, piccoli impasti. Avete trovato la mia Briciola d'Oro...",
           "Obrigado, massinhas. Vocês acharam minha Migalha Dourada..."),
         mood(["bup", "zeek"], "scared"),
         V("lunge", to=1200), V("roar", and_=1), {"shake": 1.0, "power": 36, "and": A},
         L("villain", "...and brought it right to my FIRE!", "...¡y me la trajisteis a mi FUEGO!",
           "...und ihn direkt in mein FEUER gebracht!", "...et vous l'avez apportée dans mon FEU !",
           "...e me l'avete portata nel mio FUOCO!", "...e trouxeram direto pro meu FOGO!", and_=1),
         act(["bup", "pim", "zeek", "crispy"], "jump", and_=1), act("pim", "scream"),
     ]},
]


def fix(o):
    if isinstance(o, list):
        return [fix(x) for x in o]
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            if k == "and_":
                if v:
                    r["and"] = True
                continue
            r[k] = fix(v)
        return r
    return o


LONG_TITLE = "What's Hidden Under the Freezer Ice?! 🧊 | EP 16"
long = {
    "id": "ep016_long", "format": "long", "title": LONG_TITLE,
    "hook": "IT'S UNDER THE ICE!", "hook_dur": 3.5,
    "description": ("Mr. Pot's map leads the Dough Bros into the freezer, where the Golden Crumb lies under Frostbite's ice. "
                    "The plan: Lolly sings, Crispy melts the ice with his very last spark, Pim holds the map... and must NOT sneeze. "
                    "But the Golden Crumb hides a secret, and someone in the oven has been waiting for it.\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #frostbite"),
    "tags": ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "frostbite", "treasure map", "golden crumb", "freezer ghost", "lolly", "crispy",
             "mr pot", "pim"],
    "thumbnail": {"bg": "freezer", "villain": "frost", "heroes": ["pim"], "text": "UNDER THE ICE!"},
    "scenes": fix(long_scenes),
}

# ---------------- Short: Lolly vs Frostbite (loops back to frame 1) ----------------
SH = {"type": "frost", "x": 1300, "state": "awake", "scale": 0.85}
OPEN = [
    V("lunge", to=1120), SFX("ice", 0.0, and_=1), act("lolly", "jump", and_=1), {"shake": 0.7, "power": 30, "and": A},
    L("villain", "Your icing... is MINE! Frozen FOREVER!", "Tu glaseado... ¡es MÍO! ¡Congelado PARA SIEMPRE!",
      "Dein Zuckerguss... ist MEINS! Für IMMER gefroren!", "Ton glaçage... est À MOI ! Gelé POUR TOUJOURS !",
      "La tua glassa... è MIA! Congelata PER SEMPRE!", "Sua cobertura... é MINHA! Congelada PRA SEMPRE!", and_=1),
]
short_scenes = [
    {"bg": "freezer", "music": "heartbeat", "heroes": {"lolly": 800}, "moods": {"lolly": "scared"},
     "villain": dict(SH), "tail": 0.05, "beats": [b for b in OPEN]},
    {"bg": "freezer", "music": "music_box", "cut": True, "heroes": {"lolly": 760}, "moods": {"lolly": "happy"},
     "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         act("lolly", "bounce"),
         L("lolly", "Oh my! Could you un-freeze it? Pretty please?", "¡Ay! ¿Podrías descongelarlo? ¿Porfa?",
           "Oh je! Könntest du ihn auftauen? Bitte, bitte?", "Oh là là ! Tu peux le dégeler ? S'il te plaît ?",
           "Oh cielo! Potresti scongelarla? Per favore?", "Ai! Pode descongelar? Por favorzinho?", and_=1),
     ]},
    {"bg": "freezer", "music": "heartbeat", "cut": True, "heroes": {"lolly": 760}, "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         V("roar"), {"shake": 0.5, "power": 20, "and": A},
         L("villain", "NO. And your sprinkles too!", "NO. ¡Y tus virutas también!", "NEIN. Und deine Streusel auch!",
           "NON. Et tes vermicelles aussi !", "NO. E anche i tuoi codini!", "NÃO. E seus granulados também!", and_=1),
         SFX("ice", 0.2),
     ]},
    {"bg": "freezer", "music": "heartbeat", "cut": True, "heroes": {"lolly": 760}, "moods": {"lolly": "angry"},
     "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         act("lolly", "shake"), {"shake": 0.9, "power": 34, "and": A}, F(and_=1),
         L("lolly", "You froze... my... SPRINKLES?!", "¿Congelaste... mis... VIRUTAS?!", "Du hast... meine... STREUSEL eingefroren?!",
           "Tu as gelé... mes... VERMICELLES ?!", "Hai congelato... i miei... CODINI?!", "Você congelou... meus... GRANULADOS?!", and_=1),
     ]},
    {"bg": "freezer", "music": "heartbeat", "cut": True, "heroes": {"lolly": 900}, "moods": {"lolly": "angry"},
     "villain": dict(SH, x=1250), "tail": 0.05,
     "beats": [
         mv("lolly", 1020, "run"), V("lunge", to=1500, and_=1), SFX("whoosh", 0.0, and_=1), F(and_=1),
         L("villain", "She's... HOT?! The ice is MELTING!", "¿¡Está... ARDIENDO!? ¡El hielo se DERRITE!",
           "Sie ist... HEISS?! Das Eis SCHMILZT!", "Elle est... BRÛLANTE ?! La glace FOND !",
           "Lei è... BOLLENTE?! Il ghiaccio si SCIOGLIE!", "Ela tá... FERVENDO?! O gelo tá DERRETENDO!", and_=1),
     ]},
    {"bg": "kitchen", "music": "drone", "cut": True, "heroes": {"pim": 600, "zeek": 900}, "moods": {"pim": "scared"}, "tail": 0.05,
     "beats": [
         act(["pim", "zeek"], "jump"), SFX("creak", 0.0, and_=1),
         L("pim", "Th-three seconds. She melted a FREEZER in three seconds.",
           "T-tres segundos. Derritió un CONGELADOR en tres segundos.",
           "D-drei Sekunden. Sie hat einen GEFRIERSCHRANK in drei Sekunden geschmolzen.",
           "T-trois secondes. Elle a fait fondre un CONGÉLATEUR en trois secondes.",
           "T-tre secondi. Ha sciolto un CONGELATORE in tre secondi.",
           "T-três segundos. Ela derreteu um CONGELADOR em três segundos.", and_=1),
         act("zeek", "faint"),
     ]},
    {"bg": "freezer", "music": "music_box", "cut": True, "heroes": {"lolly": 800}, "moods": {"lolly": "happy"},
     "villain": dict(SH, x=1450), "tail": 0.05,
     "beats": [
         act("lolly", "bounce"),
         L("lolly", "Thank you SO much! Have a lovely night!", "¡Muchísimas gracias! ¡Que tengas buena noche!",
           "Vielen, vielen Dank! Schöne Nacht noch!", "Merci BEAUCOUP ! Bonne nuit !",
           "Grazie MILLE! Buona notte!", "Muito obrigada! Tenha uma ótima noite!", and_=1),
     ]},
    {"bg": "freezer", "music": "heartbeat", "cut": True, "heroes": {"lolly": 800}, "moods": {"lolly": "scared"},
     "villain": dict(SH), "tail": 0.05,
     "beats": [
         V("lunge", to=1120), SFX("ice", 0.0, and_=1), act("lolly", "jump", and_=1), {"shake": 0.7, "power": 30, "and": A},
         L("villain", "Your icing...", "Tu glaseado...", "Dein Zuckerguss...", "Ton glaçage...", "La tua glassa...",
           "Sua cobertura...", and_=1),
     ]},
]
SHORT_TITLE = "Lolly Melted a Freezer in 3 Seconds 😡 #shorts"
short = {
    "id": "ep016_short1", "format": "short", "title": SHORT_TITLE, "hook": "DON'T FREEZE HER!",
    "description": ("Frostbite froze Lolly's sprinkles. Big mistake. "
                    'Full episode: "' + LONG_TITLE.replace(" 🧊", "") + '" {LONG_URL} — more on https://www.youtube.com/@DoughBrosTV '
                    "#shorts #animation #cartoon #doughbros #funnycartoon"),
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "lolly", "frostbite", "freezer ghost", "angry cookie"],
    "thumbnail": {"bg": "freezer", "villain": "frost", "heroes": ["lolly"], "text": "SHE'S MAD!"},
    "scenes": fix(short_scenes),
}

for s in (long, short):
    json.dump(s, open(os.path.join(D, s["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print("wrote", s["id"])

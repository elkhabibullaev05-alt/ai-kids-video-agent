"""Builds ep013_long.json + ep013_short1.json (Body swap / mix-up, Whisker). Run from doughbros/."""
import json

LANG = ("en", "es", "de", "fr", "it", "pt")


def S(who, *tr, **kw):
    b = {"say": who}
    b.update(dict(zip(LANG, tr)))
    b.update(kw)
    return b


A = {"and": True}
MIX = {"type": "mixer", "x": 1450, "state": "awake", "scale": 0.9}

long_scenes = [
    # 1 cold open: Whisker already spinning at frame 1
    {"bg": "kitchen", "music": "heartbeat", "heroes": {"bup": 420, "pim": 720},
     "moods": {"bup": "normal", "pim": "scared"}, "villain": dict(MIX), "tail": 0.2,
     "beats": [
        {"villain": "lunge", "to": 1100},
        S("villain", "Let's MIX it up! Hee hee!", "¡A MEZCLAR! ¡Ji ji!", "Jetzt wird GEMIXT! Hihi!",
          "On MÉLANGE tout ! Hi hi !", "Si MESCOLA! Ih ih!", "Vamos MISTURAR! Hi hi!", **A),
        {"shake": 0.6, "power": 26, "and": True},
        {"villain": "rage", "level": 1.0},
        {"act": ["bup", "pim"], "do": "spin", "and": True},
        {"sfx": "whoosh", "wait": 0.2, "and": True},
        {"act": ["bup", "pim"], "do": "scream"},
        S("villain", "Mr. Pot ordered one brave bread and one scared bean. MIXED!",
          "Mr. Pot pidió un pan valiente y una judía miedosa. ¡MEZCLADOS!",
          "Mr. Pot hat ein mutiges Brot und eine ängstliche Bohne bestellt. GEMIXT!",
          "Mr. Pot a commandé un pain courageux et un haricot peureux. MÉLANGÉS !",
          "Mr. Pot ha ordinato un pane coraggioso e un fagiolo fifone. MESCOLATI!",
          "O Mr. Pot pediu um pão corajoso e um feijão medroso. MISTURADOS!"),
        {"sfx": "pop", "wait": 0.2},
        {"shake": 0.8, "power": 30, "and": True},
        S("narr", "And just like that... something was VERY wrong.", "Y así, sin más... algo iba MUY mal.",
          "Und einfach so... war etwas SEHR falsch.", "Et comme ça... quelque chose clochait VRAIMENT.",
          "E così, all'improvviso... qualcosa non andava PER NIENTE.", "E assim, do nada... algo estava MUITO errado."),
     ]},
    # 2 hard cut: kitchen, the swap is revealed
    {"cut": True, "bg": "kitchen", "music": "music_box", "heroes": {"pim": 350, "bup": 600, "zeek": 850},
     "moods": {"pim": "happy", "bup": "scared", "zeek": "normal"}, "tail": 0.2,
     "beats": [
        {"act": "pim", "do": "jump"},
        S("pim", "Okay team, here's the plan.", "Vale, equipo, este es el plan.", "Okay, Team, hier ist der Plan.",
          "Ok l'équipe, voilà le plan.", "Ok squadra, ecco il piano.", "Certo, equipe, o plano é este.", **A),
        S("zeek", "Pim? Since when do YOU make plans?", "¿Pim? ¿Desde cuándo haces TÚ planes?", "Pim? Seit wann machst DU Pläne?",
          "Pim ? Depuis quand c'est TOI qui fais des plans ?", "Pim? Da quando fai TU i piani?", "Pim? Desde quando VOCÊ faz planos?"),
        {"act": "bup", "do": "shake"},
        S("bup", "N-n-nope! Let's go home! I want my b-blanket!", "¡N-n-no! ¡Vámonos a casa! ¡Quiero mi m-mantita!",
          "N-n-nein! Ab nach Hause! Ich will meine D-Decke!", "N-n-non ! On rentre ! Je veux ma c-couverture !",
          "N-n-no! Andiamo a casa! Voglio la mia c-copertina!", "N-n-não! Vamos pra casa! Eu quero meu c-cobertor!", **A),
        S("zeek", "Bup is stuttering. Pim is bossy. My calculations say...", "Bup tartamudea. Pim da órdenes. Mis cálculos dicen...",
          "Bup stottert. Pim kommandiert. Meine Berechnungen sagen...", "Bup bégaie. Pim donne des ordres. Mes calculs disent...",
          "Bup balbetta. Pim comanda. I miei calcoli dicono...", "O Bup gagueja. O Pim manda. Meus cálculos dizem..."),
        {"mood": "zeek", "is": "scared"},
        S("zeek", "Whisker mixed up your BRAVERY!", "¡Whisker os ha mezclado la VALENTÍA!", "Whisker hat euren MUT vertauscht!",
          "Whisker a échangé votre COURAGE !", "Whisker vi ha scambiato il CORAGGIO!", "O Whisker trocou a CORAGEM de vocês!"),
        S("pim", "Great. Then I'll go beat that mixer myself!", "Genial. ¡Entonces venceré yo solo a esa batidora!",
          "Super. Dann besiege ich diesen Mixer eben selbst!", "Parfait. Alors je vais battre ce batteur tout seul !",
          "Perfetto. Allora batto quel frullino da solo!", "Ótimo. Então eu mesmo vou vencer essa batedeira!"),
        {"move": "pim", "to": "off_right", "speed": "run"},
        S("bup", "Pim, w-wait! Mixers are SO spinny!", "¡Pim, e-espera! ¡Las batidoras dan MUCHAS vueltas!",
          "Pim, w-warte! Mixer drehen sich SO doll!", "Pim, a-attends ! Les batteurs tournent TROP vite !",
          "Pim, a-aspetta! I frullini girano TANTISSIMO!", "Pim, e-espera! Batedeiras giram DEMAIS!", **A),
        {"act": "bup", "do": "faint"},
     ]},
    # 3 hard cut: lunchbox, brave Pim charges
    {"cut": True, "bg": "lunchbox", "music": "drone", "heroes": {"pim": 300, "lolly": 580, "bup": 860},
     "moods": {"pim": "angry", "lolly": "normal", "bup": "scared"},
     "villain": {"type": "mixer", "x": 1450, "state": "hidden", "scale": 0.9}, "tail": 0.2,
     "beats": [
        {"act": "pim", "do": "bounce"},
        S("narr", "Five minutes later. Inside the lunchbox.", "Cinco minutos después. Dentro de la fiambrera.",
          "Fünf Minuten später. In der Brotdose.", "Cinq minutes plus tard. Dans la boîte à goûter.",
          "Cinque minuti dopo. Dentro il portapranzo.", "Cinco minutos depois. Dentro da lancheira.", **A),
        S("pim", "Whisker! Come out and fight, you giant eggbeater!", "¡Whisker! ¡Sal y pelea, batidor gigante!",
          "Whisker! Komm raus und kämpfe, du Riesen-Schneebesen!", "Whisker ! Sors et bats-toi, espèce de fouet géant !",
          "Whisker! Esci e combatti, frusta gigante!", "Whisker! Sai e luta, batedor gigante!"),
        S("lolly", "Pim, sweetie... you're shouting at a sandwich.", "Pim, cielo... le estás gritando a un sándwich.",
          "Pim, Schätzchen... du schreist ein Sandwich an.", "Pim, mon chou... tu cries sur un sandwich.",
          "Pim, tesoro... stai urlando contro un panino.", "Pim, querido... você tá gritando com um sanduíche."),
        {"act": "bup", "do": "shake"},
        S("bup", "C-can we be quieter? The sandwich might w-wake up.", "¿P-podemos hablar más bajo? El sándwich podría d-despertarse.",
          "K-können wir leiser sein? Das Sandwich könnte a-aufwachen.", "On p-peut parler moins fort ? Le sandwich pourrait se r-réveiller.",
          "P-possiamo fare più piano? Il panino potrebbe s-svegliarsi.", "A gente p-pode falar baixo? O sanduíche pode a-acordar."),
        {"sfx": "creak", "wait": 0.3},
        {"villain": "show"},
        {"villain": "lunge", "to": 1150, "and": True},
        {"shake": 0.7, "power": 26, "and": True},
        S("villain", "Hee hee! The brave bean wants to DANCE?", "¡Ji ji! ¿La judía valiente quiere BAILAR?",
          "Hihi! Die mutige Bohne will TANZEN?", "Hi hi ! Le haricot courageux veut DANSER ?",
          "Ih ih! Il fagiolo coraggioso vuole BALLARE?", "Hi hi! O feijão corajoso quer DANÇAR?"),
        {"mood": "pim", "is": "scared"},
        S("pim", "Yes! No! Wait... how do I actually fight?", "¡Sí! ¡No! Espera... ¿cómo se pelea de verdad?",
          "Ja! Nein! Moment... wie kämpft man eigentlich?", "Oui ! Non ! Attends... on se bat comment, en fait ?",
          "Sì! No! Aspetta... come si combatte davvero?", "Sim! Não! Espera... como é que se luta mesmo?"),
        {"villain": "rage", "level": 0.8},
        {"act": "pim", "do": "spin", "and": True},
        {"sfx": "whoosh", "wait": 0.2, "and": True},
        {"act": "bup", "do": "scream"},
        S("lolly", "Everybody, RUN!", "¡Todos, CORRED!", "Alle, LAUFT!", "Tout le monde, COUREZ !", "Tutti, CORRETE!", "Todo mundo, CORRE!"),
        {"move": "bup", "to": "off_left", "speed": "run"},
        {"move": "lolly", "to": "off_left", "speed": "run", "and": True},
        {"move": "pim", "to": "off_left", "speed": "run", "and": True},
     ]},
    # 4 hard cut: pantry, Crispy from nowhere
    {"cut": True, "bg": "pantry", "music": "heartbeat", "heroes": {"pim": 300, "bup": 520, "zeek": 740, "crispy": 2200},
     "moods": {"pim": "happy", "bup": "scared", "zeek": "normal", "crispy": "normal"}, "tail": 0.2,
     "beats": [
        {"act": "zeek", "do": "bounce"},
        S("zeek", "I studied his beaters. Whisker spins LEFT when he giggles.", "Estudié sus varillas. Whisker gira a la IZQUIERDA cuando se ríe.",
          "Ich habe seine Rührstäbe studiert. Whisker dreht LINKS, wenn er kichert.", "J'ai étudié ses fouets. Whisker tourne à GAUCHE quand il rigole.",
          "Ho studiato le sue fruste. Whisker gira a SINISTRA quando ridacchia.", "Eu estudei os batedores dele. O Whisker gira pra ESQUERDA quando ri.", **A),
        {"sfx": "sting", "wait": 0.1},
        {"move": "crispy", "to": 980, "speed": "walk", "and": True},
        S("crispy", "And RIGHT... when he's angry.", "Y a la DERECHA... cuando se enfada.", "Und RECHTS... wenn er wütend ist.",
          "Et à DROITE... quand il est fâché.", "E a DESTRA... quando è arrabbiato.", "E pra DIREITA... quando fica bravo."),
        {"act": ["pim", "bup", "zeek"], "do": "jump"},
        {"act": "bup", "do": "scream", "and": True},
        S("bup", "Wh-where did you COME from?!", "¿D-de dónde has SALIDO?", "W-wo kommst DU denn her?!",
          "D-d'où tu SORS, toi ?!", "D-da dove SEI sbucato?!", "D-de onde você SAIU?!"),
        S("crispy", "The shadows. Always the shadows.", "De las sombras. Siempre de las sombras.", "Aus den Schatten. Immer aus den Schatten.",
          "Des ombres. Toujours des ombres.", "Dalle ombre. Sempre dalle ombre.", "Das sombras. Sempre das sombras."),
        S("zeek", "Of course! Spin them the OTHER way and the bravery switches back!", "¡Claro! ¡Si giran al REVÉS, la valentía vuelve a su sitio!",
          "Natürlich! Andersrum DREHEN und der Mut tauscht zurück!", "Bien sûr ! On les fait tourner dans l'AUTRE sens et le courage revient !",
          "Certo! Se girano al CONTRARIO, il coraggio torna al suo posto!", "Claro! Girando pro OUTRO lado, a coragem volta pro lugar!"),
        S("pim", "So we have to make a mixer ANGRY?", "¿Así que tenemos que hacer ENFADAR a una batidora?", "Also müssen wir einen Mixer WÜTEND machen?",
          "Donc il faut mettre un batteur en COLÈRE ?", "Quindi dobbiamo far ARRABBIARE un frullino?", "Então a gente tem que deixar uma batedeira BRAVA?"),
        S("crispy", "Nobody makes things angry... like Lolly.", "Nadie hace enfadar a nadie... como Lolly.", "Niemand macht jemanden so wütend... wie Lolly.",
          "Personne ne met en colère... comme Lolly.", "Nessuno fa arrabbiare... come Lolly.", "Ninguém deixa alguém bravo... como a Lolly."),
        {"act": "bup", "do": "shake"},
        S("bup", "D-don't tell her I nodded.", "N-no le digas que asentí.", "S-sag ihr nicht, dass ich genickt habe.",
          "N-ne lui dis pas que j'ai hoché la tête.", "N-non dirle che ho annuito.", "N-não conta pra ela que eu concordei.", **A),
     ]},
    # 5 hard cut: table, Lolly vs Whisker
    {"cut": True, "bg": "table", "music": "drone", "heroes": {"pim": 300, "bup": 540, "lolly": 800},
     "moods": {"pim": "happy", "bup": "scared", "lolly": "happy"}, "villain": dict(MIX), "tail": 0.2,
     "beats": [
        {"villain": "lunge", "to": 1250},
        S("villain", "Batter time! Mr. Pot is waiting!", "¡Hora de la masa! ¡Mr. Pot está esperando!", "Teigzeit! Mr. Pot wartet!",
          "C'est l'heure de la pâte ! Mr. Pot attend !", "È ora della pastella! Mr. Pot aspetta!", "Hora da massa! O Mr. Pot tá esperando!", **A),
        {"shake": 0.5, "power": 22, "and": True},
        {"move": "lolly", "to": 1000, "speed": "walk"},
        S("lolly", "Mister Whisker, your giggle is lovely.", "Señor Whisker, su risita es preciosa.", "Herr Whisker, Ihr Kichern ist reizend.",
          "Monsieur Whisker, votre petit rire est charmant.", "Signor Whisker, la sua risatina è deliziosa.", "Senhor Whisker, sua risadinha é linda.", **A),
        S("villain", "Hee hee! Thank you!", "¡Ji ji! ¡Gracias!", "Hihi! Danke!", "Hi hi ! Merci !", "Ih ih! Grazie!", "Hi hi! Obrigado!"),
        S("lolly", "It's just a little bit... ANNOYING.", "Solo que es un poquito... MOLESTA.", "Es ist nur ein kleines bisschen... NERVIG.",
          "C'est juste un tout petit peu... AGAÇANT.", "È solo un pochino... FASTIDIOSA.", "Só é um pouquinho... IRRITANTE."),
        {"mood": "lolly", "is": "angry", "and": True},
        {"shake": 0.4, "power": 18, "and": True},
        {"villain": "rage", "level": 0.5},
        S("villain", "ANNOYING?! My giggle is PERFECT!", "¿MOLESTA? ¡Mi risita es PERFECTA!", "NERVIG?! Mein Kichern ist PERFEKT!",
          "AGAÇANT ?! Mon rire est PARFAIT !", "FASTIDIOSA?! La mia risatina è PERFETTA!", "IRRITANTE?! Minha risadinha é PERFEITA!", **A),
        S("lolly", "Annoying. Squeaky. Like a rusty spoon.", "Molesta. Chillona. Como una cuchara oxidada.", "Nervig. Quietschig. Wie ein rostiger Löffel.",
          "Agaçant. Grinçant. Comme une cuillère rouillée.", "Fastidiosa. Stridula. Come un cucchiaio arrugginito.", "Irritante. Esganiçada. Igual colher enferrujada."),
        {"villain": "rage", "level": 1.0},
        {"shake": 1.0, "power": 30, "and": True},
        {"sfx": "whoosh", "wait": 0.2, "and": True},
        {"act": ["bup", "pim"], "do": "spin"},
        S("narr", "The beaters spun the OTHER way...", "Las varillas giraron al REVÉS...", "Die Rührstäbe drehten sich ANDERSHERUM...",
          "Les fouets tournèrent dans l'AUTRE sens...", "Le fruste girarono al CONTRARIO...", "Os batedores giraram pro OUTRO lado...", **A),
        {"sfx": "pop", "wait": 0.2},
        {"mood": "bup", "is": "happy"},
        {"mood": "pim", "is": "scared", "and": True},
        S("bup", "Okay team... I'm BACK!", "Vale, equipo... ¡he VUELTO!", "Okay, Team... ich bin ZURÜCK!",
          "Ok l'équipe... je suis DE RETOUR !", "Ok squadra... sono TORNATO!", "Certo, equipe... VOLTEI!"),
        {"act": "bup", "do": "bounce", "and": True},
        S("pim", "Did I just... yell at a MIXER?", "¿Acabo de... gritarle a una BATIDORA?", "Hab ich gerade... einen MIXER angeschrien?",
          "Est-ce que je viens de... crier sur un BATTEUR ?", "Ho appena... urlato contro un FRULLINO?", "Eu acabei de... gritar com uma BATEDEIRA?"),
        {"act": "pim", "do": "faint"},
        S("villain", "Too... dizzy... I'm telling Mr. Pot!", "Qué... mareo... ¡Se lo diré a Mr. Pot!", "So... schwindelig... Ich sag's Mr. Pot!",
          "Trop... la tête qui tourne... Je le dis à Mr. Pot !", "Che... giramento... Lo dico a Mr. Pot!", "Que... tontura... Vou contar pro Mr. Pot!"),
        {"move": "villain", "to": "off_right", "speed": "run"},
     ]},
    # 6 hard cut: kitchen, the recipe card
    {"cut": True, "bg": "kitchen", "music": "music_box", "heroes": {"pim": 300, "bup": 520, "zeek": 740, "lolly": 960},
     "moods": {"pim": "scared", "bup": "normal", "zeek": "normal", "lolly": "happy"}, "tail": 0.2,
     "beats": [
        {"sfx": "clank", "wait": 0.1},
        {"act": "zeek", "do": "jump", "and": True},
        S("zeek", "He dropped something. A recipe card!", "Se le cayó algo. ¡Una tarjeta de receta!", "Er hat etwas verloren. Eine Rezeptkarte!",
          "Il a fait tomber quelque chose. Une fiche recette !", "Gli è caduto qualcosa. Una scheda ricetta!", "Ele deixou cair algo. Um cartão de receita!", **A),
        S("zeek", "Step one: a hot oven. Step two: the batter.", "Paso uno: un horno caliente. Paso dos: la masa.",
          "Schritt eins: ein heißer Ofen. Schritt zwei: der Teig.", "Étape un : un four chaud. Étape deux : la pâte.",
          "Primo passo: un forno caldo. Secondo passo: la pastella.", "Passo um: um forno quente. Passo dois: a massa."),
        S("bup", "And step three?", "¿Y el paso tres?", "Und Schritt drei?", "Et l'étape trois ?", "E il passo tre?", "E o passo três?"),
        {"mood": "zeek", "is": "scared"},
        S("zeek", "Step three... the pot. With all five of us INSIDE.", "Paso tres... la olla. Con los cinco DENTRO.",
          "Schritt drei... der Topf. Mit uns allen fünf DRIN.", "Étape trois... la marmite. Avec nous cinq DEDANS.",
          "Passo tre... la pentola. Con tutti e cinque DENTRO.", "Passo três... a panela. Com nós cinco DENTRO.", **A),
        S("lolly", "Who writes a recipe with US in it?", "¿Quién escribe una receta con NOSOTROS dentro?", "Wer schreibt ein Rezept mit UNS drin?",
          "Qui écrit une recette avec NOUS dedans ?", "Chi scrive una ricetta con NOI dentro?", "Quem escreve uma receita com A GENTE dentro?"),
        {"mood": "lolly", "is": "angry", "and": True},
        S("bup", "Mr. Pot. He even drew little hearts on it.", "Mr. Pot. Hasta dibujó corazoncitos.", "Mr. Pot. Er hat sogar kleine Herzen draufgemalt.",
          "Mr. Pot. Il a même dessiné des petits cœurs.", "Mr. Pot. Ci ha perfino disegnato dei cuoricini.", "O Mr. Pot. Ele até desenhou coraçõezinhos."),
        {"act": "pim", "do": "shake"},
        S("lolly", "Then we stay together. Pim? Where are you?", "Entonces nos quedamos juntos. ¿Pim? ¿Dónde estás?",
          "Dann bleiben wir zusammen. Pim? Wo bist du?", "Alors on reste ensemble. Pim ? Tu es où ?",
          "Allora restiamo insieme. Pim? Dove sei?", "Então a gente fica junto. Pim? Cadê você?"),
        {"act": "pim", "do": "hide"},
        S("pim", "Hiding inside my own bandage. It's f-fine.", "Escondido dentro de mi propia venda. Estoy b-bien.",
          "Ich verstecke mich in meinem eigenen Pflaster. Alles g-gut.", "Caché dans mon propre pansement. Tout va b-bien.",
          "Nascosto dentro la mia benda. Va t-tutto bene.", "Escondido dentro do meu curativo. Tá t-tudo bem."),
        {"act": "pim", "do": "show"},
        S("bup", "Good to have you back, buddy.", "Me alegra tenerte de vuelta, colega.", "Schön, dass du wieder du bist, Kumpel.",
          "Content de te retrouver, mon pote.", "Bello riaverti, amico.", "Que bom ter você de volta, parceiro."),
        {"sfx": "rattle", "wait": 0.3},
        {"mood": ["bup", "zeek", "lolly"], "is": "scared", "and": True},
        S("lolly", "Wait. Does anyone else hear... rattling?", "Esperad. ¿Alguien más oye... un traqueteo?", "Moment. Hört noch jemand... ein Klappern?",
          "Attendez. Quelqu'un d'autre entend... un cliquetis ?", "Aspettate. Qualcun altro sente... un tintinnio?", "Espera. Mais alguém tá ouvindo... um chacoalhar?"),
     ]},
    # 7 hard cut: kitchen, Mr. Pot cliffhanger
    {"cut": True, "bg": "kitchen", "music": "heartbeat", "heroes": {"bup": 400, "pim": 650},
     "moods": {"bup": "scared", "pim": "scared"}, "villain": {"type": "pot", "x": 1450, "state": "hidden", "scale": 0.9}, "tail": 0.6,
     "beats": [
        {"sfx": "rattle", "wait": 0.2},
        {"shake": 0.6, "power": 24, "and": True},
        {"villain": "show"},
        {"villain": "wake"},
        {"villain": "lunge", "to": 1200},
        S("villain", "Fresh... dough... I heard you got MIXED.", "Masa... fresca... Me han dicho que os MEZCLARON.",
          "Frischer... Teig... Ich hörte, ihr wurdet GEMIXT.", "Pâte... fraîche... Il paraît qu'on vous a MÉLANGÉS.",
          "Pasta... fresca... Ho sentito che vi hanno MESCOLATI.", "Massa... fresca... Ouvi dizer que misturaram vocês.", **A),
        S("bup", "We're un-mixed now! So... no thank you!", "¡Ya estamos desmezclados! Así que... ¡no, gracias!",
          "Wir sind wieder entmixt! Also... nein danke!", "On est démélangés maintenant ! Donc... non merci !",
          "Ora siamo smescolati! Quindi... no grazie!", "A gente já desmisturou! Então... não, obrigado!"),
        S("villain", "Good. Un-mixed dough fries even BETTER.", "Bien. La masa desmezclada se fríe aún MEJOR.",
          "Gut. Entmixter Teig frittiert sich noch BESSER.", "Parfait. La pâte démélangée frit encore MIEUX.",
          "Bene. La pasta smescolata si frigge ancora MEGLIO.", "Ótimo. Massa desmisturada frita ainda MELHOR."),
        {"villain": "roar"},
        {"act": ["bup", "pim"], "do": "scream", "and": True},
        S("narr", "Mr. Pot is awake. And the oven is already hot...", "Mr. Pot está despierto. Y el horno ya está caliente...",
          "Mr. Pot ist wach. Und der Ofen ist schon heiß...", "Mr. Pot est réveillé. Et le four est déjà chaud...",
          "Mr. Pot è sveglio. E il forno è già caldo...", "O Mr. Pot acordou. E o forno já está quente..."),
     ]},
]


EXTRA = {
    # inserted after scene 2: Zeek's gadget fails (bathroom)
    2: {"cut": True, "bg": "bathroom", "music": "music_box", "heroes": {"zeek": 380, "bup": 640, "pim": 900},
        "moods": {"zeek": "happy", "bup": "scared", "pim": "happy"}, "tail": 0.2,
        "beats": [
            {"act": "zeek", "do": "jump"},
            S("zeek", "Behold! The Un-Mixer 3000! Made from a toothbrush!", "¡Contemplad! ¡El Desmezclador 3000! ¡Hecho con un cepillo de dientes!",
              "Seht her! Der Ent-Mixer 3000! Aus einer Zahnbürste!", "Admirez ! Le Démélangeur 3000 ! Fait avec une brosse à dents !",
              "Ammirate! Lo Smescolatore 3000! Fatto con uno spazzolino!", "Contemplem! O Desmisturador 3000! Feito de escova de dente!", **A),
            S("pim", "Does it work?", "¿Funciona?", "Funktioniert es?", "Ça marche ?", "Funziona?", "Funciona?"),
            S("zeek", "Ninety percent sure. Hold still, Bup!", "Al noventa por ciento. ¡Quieto, Bup!", "Zu neunzig Prozent. Stillhalten, Bup!",
              "Sûr à quatre-vingt-dix pour cent. Bouge pas, Bup !", "Sicuro al novanta per cento. Fermo, Bup!", "Noventa por cento de certeza. Fica parado, Bup!"),
            {"sfx": "clank", "wait": 0.1},
            {"act": "zeek", "do": "spin", "and": True},
            {"shake": 0.5, "power": 22, "and": True},
            S("zeek", "Ninety percent sure... it spins ME.", "Al noventa por ciento... me hace girar A MÍ.", "Zu neunzig Prozent... dreht es MICH.",
              "Sûr à quatre-vingt-dix pour cent... que ça me fait tourner MOI.", "Sicuro al novanta per cento... che fa girare ME.", "Noventa por cento de certeza... que gira EU."),
            {"act": "zeek", "do": "faint"},
            S("bup", "Z-Zeek? Your glasses are upside d-down!", "¿Z-Zeek? ¡Tus gafas están del r-revés!", "Z-Zeek? Deine Brille steht auf dem K-Kopf!",
              "Z-Zeek ? Tes lunettes sont à l'e-envers !", "Z-Zeek? Hai gli occhiali al c-contrario!", "Z-Zeek? Seus óculos tão de c-cabeça pra baixo!"),
            S("pim", "Forget gadgets. We find Whisker. NOW.", "Olvidad los inventos. Buscamos a Whisker. YA.", "Vergesst Erfindungen. Wir finden Whisker. SOFORT.",
              "Oubliez les gadgets. On trouve Whisker. TOUT DE SUITE.", "Lasciate perdere i gadget. Troviamo Whisker. SUBITO.", "Esquece invenção. A gente acha o Whisker. AGORA."),
            {"move": "pim", "to": "off_right", "speed": "run"},
        ]},
    # inserted after the lunchbox chase: garden
    3: {"cut": True, "bg": "garden", "music": "heartbeat", "heroes": {"bup": 380, "lolly": 640, "pim": 900},
        "moods": {"bup": "scared", "lolly": "scared", "pim": "happy"},
        "villain": {"type": "mixer", "x": 1500, "state": "hidden", "scale": 0.8}, "tail": 0.2,
        "beats": [
            {"move": "bup", "to": 300, "speed": "run"},
            S("bup", "A m-moth! A giant moth! Hide me, Lolly!", "¡Una p-polilla! ¡Una polilla gigante! ¡Escóndeme, Lolly!",
              "Eine M-Motte! Eine Riesenmotte! Versteck mich, Lolly!", "Un p-papillon de nuit ! Un géant ! Cache-moi, Lolly !",
              "Una f-falena! Una falena gigante! Nascondimi, Lolly!", "Uma m-mariposa! Uma mariposa gigante! Me esconde, Lolly!", **A),
            S("lolly", "Bup, that's a leaf. A very small leaf.", "Bup, eso es una hoja. Una hoja muy pequeña.", "Bup, das ist ein Blatt. Ein sehr kleines Blatt.",
              "Bup, c'est une feuille. Une toute petite feuille.", "Bup, è una foglia. Una foglia piccolissima.", "Bup, isso é uma folha. Uma folha bem pequena."),
            {"sfx": "whoosh", "wait": 0.1},
            {"villain": "show"},
            {"villain": "lunge", "to": 1200, "and": True},
            S("villain", "Hee hee! Peekaboo, little batter!", "¡Ji ji! ¡Cucú, masita!", "Hihi! Kuckuck, kleiner Teig!",
              "Hi hi ! Coucou, petite pâte !", "Ih ih! Cucù, pastellina!", "Hi hi! Achou, massinha!"),
            {"act": "bup", "do": "scream"},
            {"act": "bup", "do": "hide", "and": True},
            S("pim", "Stand back! I've got a plan!", "¡Atrás! ¡Tengo un plan!", "Zurück! Ich hab einen Plan!",
              "Reculez ! J'ai un plan !", "Indietro! Ho un piano!", "Pra trás! Eu tenho um plano!"),
            S("lolly", "What's the plan, Pim?", "¿Cuál es el plan, Pim?", "Was ist der Plan, Pim?", "C'est quoi le plan, Pim ?", "Qual è il piano, Pim?", "Qual é o plano, Pim?"),
            {"mood": "pim", "is": "scared"},
            S("pim", "I... didn't get that far.", "Eh... no llegué tan lejos.", "Ich... bin noch nicht so weit.",
              "Je... n'en suis pas encore là.", "Io... non ci ho ancora pensato.", "Eu... não pensei até aí."),
            {"villain": "rage", "level": 0.7},
            {"shake": 0.6, "power": 24, "and": True},
            {"act": "bup", "do": "show"},
            {"move": "bup", "to": "off_left", "speed": "run"},
            {"move": "lolly", "to": "off_left", "speed": "run", "and": True},
            {"move": "pim", "to": "off_left", "speed": "run", "and": True},
        ]},
}

# keep villain-less talk scenes moving: the speaker bounces on every 2nd line
for sc in long_scenes:
    if sc.get("villain"):
        continue
    out, n = [], 0
    for b in sc["beats"]:
        out.append(b)
        if b.get("say") in sc["heroes"]:
            n += 1
            if n % 2 == 0:
                out.append({"act": b["say"], "do": "bounce", "and": True})
    sc["beats"] = out

for i in sorted(EXTRA, reverse=True):
    long_scenes.insert(i, EXTRA[i])
long_script = {
    "id": "ep013_long",
    "format": "long",
    "title": "Whisker Swapped Bup and Pim?! 🌀 | EP 13",
    "hook": "WHO IS WHO?!",
    "hook_dur": 3.5,
    "description": ("One spin from Whisker and the bravest bread is suddenly scared of everything... while Pim wants to fight a mixer. "
                    "Zeek finds the trick, Crispy appears from nowhere, and only Lolly can make Whisker angry enough to spin it all back. "
                    "But what is step three of Mr. Pot's recipe?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #whisker"),
    "tags": ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy", "animated series",
             "whisker", "body swap", "personality swap", "mixer", "bup", "pim", "lolly", "mr pot"],
    "thumbnail": {"bg": "kitchen", "villain": "mixer", "heroes": ["pim", "bup"], "text": "WHO IS WHO?!"},
    "scenes": long_scenes,
}


# ---------------- Short: scared Bup screams 5 times (loops) ----------------
def sh(bg, heroes, moods, beats, villain=None, cut=True, tail=0.1):
    s = {"bg": bg, "music": "heartbeat", "heroes": heroes, "moods": moods, "beats": beats, "tail": tail}
    if villain:
        s["villain"] = villain
    if cut:
        s["cut"] = True
    return s


M = lambda **k: dict({"type": "mixer", "x": 1450, "state": "awake", "scale": 0.9}, **k)
short_scenes = [
    sh("kitchen", {"bup": 1100}, {"bup": "normal"}, [
        {"villain": "rage", "level": 1.0},
        {"shake": 0.5, "power": 28, "and": True},
        {"act": "bup", "do": "spin", "and": True},
        S("villain", "Let's MIX it up!", "¡A MEZCLAR!", "Jetzt wird GEMIXT!", "On MÉLANGE tout !", "Si MESCOLA!", "Vamos MISTURAR!", **A),
        {"sfx": "pop", "wait": 0.1},
        {"mood": "bup", "is": "scared", "and": True},
    ], villain=M(x=1400), cut=False),
    sh("kitchen", {"bup": 700, "zeek": 1050}, {"bup": "scared", "zeek": "normal"}, [
        S("zeek", "Bup? You okay?", "¿Bup? ¿Estás bien?", "Bup? Alles okay?", "Bup ? Ça va ?", "Bup? Tutto bene?", "Bup? Tá tudo bem?"),
        {"act": "bup", "do": "scream"},
        {"act": "bup", "do": "jump", "and": True},
        S("bup", "AAH! Oh. It's y-you.", "¡AAH! Ah. Eres t-tú.", "AAH! Ach. Du b-bist es.", "AAH ! Ah. C'est t-toi.", "AAH! Ah. Sei t-tu.", "AAH! Ah. É v-você."),
    ]),
    sh("pantry", {"bup": 700, "lolly": 1050}, {"bup": "scared", "lolly": "happy"}, [
        S("lolly", "Hi, Bup!", "¡Hola, Bup!", "Hallo, Bup!", "Coucou, Bup !", "Ciao, Bup!", "Oi, Bup!"),
        {"act": "bup", "do": "scream"},
        {"shake": 0.3, "power": 16, "and": True},
        S("bup", "A COOKIE! ...a n-nice cookie.", "¡Una GALLETA! ...una galleta m-maja.", "Ein KEKS! ...ein n-netter Keks.",
          "Un BISCUIT ! ...un g-gentil biscuit.", "Un BISCOTTO! ...un b-biscotto gentile.", "Um BISCOITO! ...um biscoito l-legal."),
        S("lolly", "Bup. You've known me for YEARS.", "Bup. Me conoces desde hace AÑOS.", "Bup. Du kennst mich seit JAHREN.",
          "Bup. Tu me connais depuis des ANNÉES.", "Bup. Mi conosci da ANNI.", "Bup. Você me conhece há ANOS."),
    ]),
    sh("table", {"bup": 800}, {"bup": "scared"}, [
        {"act": "bup", "do": "shake"},
        S("bup", "My SHADOW is following me!", "¡Mi SOMBRA me está siguiendo!", "Mein SCHATTEN verfolgt mich!",
          "Mon OMBRE me suit !", "La mia OMBRA mi segue!", "Minha SOMBRA tá me seguindo!", **A),
        {"act": "bup", "do": "scream"},
        {"move": "bup", "to": 1300, "speed": "run", "and": True},
        S("bup", "It's FASTER than me!", "¡Es más RÁPIDA que yo!", "Er ist SCHNELLER als ich!", "Elle est plus RAPIDE que moi !", "È più VELOCE di me!", "Ela é mais RÁPIDA que eu!"),
    ]),
    sh("lunchbox", {"bup": 700, "pim": 1050}, {"bup": "scared", "pim": "happy"}, [
        S("pim", "Relax. I'll protect you.", "Tranquilo. Yo te protejo.", "Ganz ruhig. Ich beschütze dich.",
          "Du calme. Je vais te protéger.", "Tranquillo. Ti proteggo io.", "Relaxa. Eu te protejo."),
        {"act": "pim", "do": "bounce", "and": True},
        {"act": "bup", "do": "scream"},
        S("bup", "Pim is BRAVE?! That's the scariest part!", "¿Pim es VALIENTE? ¡Eso es lo que más miedo da!",
          "Pim ist MUTIG?! Das ist das Gruseligste!", "Pim est COURAGEUX ?! C'est le plus effrayant !",
          "Pim è CORAGGIOSO?! È la cosa più spaventosa!", "O Pim tá CORAJOSO?! Isso é o mais assustador!"),
    ]),
    sh("kitchen", {"bup": 1100}, {"bup": "scared"}, [
        {"villain": "rage", "level": 0.8},
        S("villain", "Hee hee! Want to go AGAIN?", "¡Ji ji! ¿Otra VEZ?", "Hihi! Nochmal?", "Hi hi ! On RECOMMENCE ?", "Ih ih! Di NUOVO?", "Hi hi! De NOVO?", **A),
        {"act": "bup", "do": "scream"},
        {"act": "bup", "do": "spin", "and": True},
    ], villain=M(x=1400)),
]

short_script = {
    "id": "ep013_short1",
    "format": "short",
    "title": "Why Did Bup Scream 5 Times? 😱 #shorts",
    "hook": "BUP IS... SCARED?!",
    "description": ("One spin from Whisker and the bravest bread screams at EVERYTHING. Count them! "
                    "Full episode: \"Whisker Swapped Bup and Pim?! 🌀 | EP 13\" {LONG_URL} — more on https://www.youtube.com/@DoughBrosTV "
                    "#shorts #animation #cartoon #doughbros #funnycartoon"),
    "tags": ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
             "animated series", "bup", "pim", "whisker", "body swap"],
    "thumbnail": {"bg": "kitchen", "villain": "mixer", "heroes": ["bup"], "text": "5 SCREAMS"},
    "scenes": short_scenes,
}

for s in (long_script, short_script):
    with open(f"scripts/{s['id']}.json", "w") as f:
        json.dump(s, f, indent=1, ensure_ascii=False)
print("ok")

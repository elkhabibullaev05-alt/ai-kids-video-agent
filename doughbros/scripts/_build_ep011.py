"""Builds the EP11 pack (1 long + 1 short). Run: python3 scripts/_build_ep011.py"""
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


def A(beat):
    """start this beat together with the previous one"""
    return {**beat, "and": True}


def flat(beats):
    out = []
    for b in beats:
        out.extend(b if isinstance(b, list) else [b])
    return out


LONG_TITLE = "Would YOU Trust a Jelly Babysitter? 🟢 | EP 11"
CHANNEL = "https://www.youtube.com/@DoughBrosTV"
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "wobblor", "jelly monster", "fake hero"]
SHORT_TAGS = ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon",
              "horror comedy", "animated series"]

long_ = {
    "id": "ep011_long", "format": "long",
    "title": LONG_TITLE,
    "hook": "HE ATE PIM?!", "hook_dur": 3.5,
    "description": ("Wobblor the giant jelly says Mr. Pot sent him to BABYSIT the Dough Bros. He is soft, giggly "
                    "and SO friendly... until Pim disappears inside him. Zeek's jelly-melter fails, Crispy knows the "
                    "truth, and Lolly asks an old enemy for help. But what did Pim find inside the jelly?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #wobblor"),
    "tags": TAGS + ["episode 11", "pim", "lolly", "old hissy", "toastmaw"],
    "thumbnail": {"bg": "fridge", "villain": "jelly", "heroes": ["pim"], "text": "HE'S NOT NICE!"},
    "scenes": [
        {   # 1 cold open: Wobblor lunges and swallows Pim (motion + line at 0 s)
            "bg": "fridge", "music": "drone",
            "heroes": {"pim": 760, "bup": 300, "lolly": 520},
            "moods": {"pim": "scared", "bup": "scared", "lolly": "scared"},
            "villain": {"type": "jelly", "x": 1450, "state": "awake", "scale": 0.9},
            "beats": [
                {"villain": "lunge", "to": 1200},
                A(S("pim", "It's GIGGLING! The jelly is GIGGLING at me!|¡Se RÍE! ¡La gelatina se RÍE de mí!|Es KICHERT! Der Wackelpudding KICHERT mich an!|"
                    "Elle GLOUSSE ! La gelée me GLOUSSE dessus !|RIDACCHIA! La gelatina RIDACCHIA di me!|Está RINDO! A gelatina está RINDO de mim!")),
                A({"shake": 0.6, "power": 18}),
                S("villain", "Hee hee! Just one little hug, bean!|¡Ji ji! ¡Solo un abracito, frijol!|Hihi! Nur eine kleine Umarmung, Bohne!|"
                  "Hi hi ! Juste un petit câlin, haricot !|Ih ih! Solo un abbraccino, fagiolo!|Hi hi! Só um abracinho, feijão!"),
                mv("pim", 1080, "run"),
                {"sfx": "pop", "wait": 0.2},
                A({"shake": 0.8, "power": 22}),
                act("pim", "hide"),
                act(["bup", "lolly"], "scream"),
                S("narr", "And just like that... Pim was INSIDE the jelly.|Y así, sin más... Pim estaba DENTRO de la gelatina.|"
                  "Und einfach so... war Pim IM Wackelpudding.|Et comme ça... Pim était DANS la gelée.|"
                  "E così... Pim era DENTRO la gelatina.|E assim, do nada... Pim estava DENTRO da gelatina."),
                mood("bup", "angry"),
                S("bup", "Hey! Give him BACK!|¡Oye! ¡DEVUÉLVELO!|Hey! Gib ihn ZURÜCK!|Hé ! RENDS-le !|Ehi! RIDACCELO!|Ei! DEVOLVE ele!"),
                {"villain": "rage", "level": 0.5},
                S("villain", "Relax! I'm not a monster. I'm your BABYSITTER!|¡Tranquilos! No soy un monstruo. ¡Soy su NIÑERO!|"
                  "Ruhig! Ich bin kein Monster. Ich bin euer BABYSITTER!|Du calme ! Je ne suis pas un monstre. Je suis votre BABY-SITTER !|"
                  "Calma! Non sono un mostro. Sono il vostro BABYSITTER!|Calma! Eu não sou um monstro. Sou a BABÁ de vocês!"),
            ],
            "tail": 0.3,
        },
        {   # 2 the fake hero: Wobblor acts friendly, Pim's voice from inside
            "bg": "fridge", "music": "music_box",
            "heroes": {"bup": 300, "lolly": 520, "zeek": -300, "pim": 1350},
            "moods": {"bup": "scared", "lolly": "scared", "pim": "scared"},
            "villain": {"type": "jelly", "x": 1350, "state": "awake", "scale": 0.9},
            "beats": [
                act("pim", "hide"),
                S("villain", "Pim is fine! He's warm, he's cozy, he's... a little sticky.|¡Pim está bien! Calentito, cómodo... un poco pegajoso.|"
                  "Pim geht's gut! Warm, gemütlich... ein bisschen klebrig.|Pim va bien ! Au chaud, douillet... un peu collant.|"
                  "Pim sta bene! Al caldo, comodo... un po' appiccicoso.|O Pim está bem! Quentinho, confortável... meio grudento."),
                S("pim", "M-mmf! It's s-squishy in here!|¡M-mmf! ¡Aquí d-dentro está b-blandito!|M-mmpf! Hier drin ist es m-matschig!|"
                  "M-mmf ! C'est t-tout mou là-dedans !|M-mmf! Qui d-dentro è m-molliccio!|M-mmf! Aqui d-dentro é m-molenga!"),
                mv("zeek", 740, "run"),
                act("zeek", "bounce"),
                A(S("zeek", "My calculations say jelly is ninety percent hug!|¡Mis cálculos dicen que la gelatina es noventa por ciento abrazo!|"
                    "Meine Berechnungen sagen: Wackelpudding ist neunzig Prozent Umarmung!|Mes calculs disent que la gelée, c'est quatre-vingt-dix pour cent de câlin !|"
                    "I miei calcoli dicono che la gelatina è al novanta per cento abbraccio!|Meus cálculos dizem que gelatina é noventa por cento abraço!")),
                mood("lolly", "angry"),
                S("lolly", "Zeek. Sweetie. He just ATE our friend.|Zeek. Cariño. Se acaba de COMER a nuestro amigo.|"
                  "Zeek. Schätzchen. Er hat gerade unseren Freund GEFRESSEN.|Zeek. Mon chou. Il vient de MANGER notre ami.|"
                  "Zeek. Tesoro. Si è appena MANGIATO il nostro amico.|Zeek. Querido. Ele acabou de COMER nosso amigo."),
                S("villain", "Not ate! SAVED! It's dangerous out there. Come inside, all of you!|¡No comido! ¡SALVADO! Afuera es peligroso. ¡Entren todos!|"
                  "Nicht gefressen! GERETTET! Draußen ist es gefährlich. Kommt alle rein!|Pas mangé ! SAUVÉ ! Dehors c'est dangereux. Entrez tous !|"
                  "Non mangiato! SALVATO! Fuori è pericoloso. Entrate tutti!|Não comido! SALVO! Lá fora é perigoso. Entrem todos!"),
                mood("bup", "angry"),
                S("bup", "Then spit him OUT, babysitter!|¡Entonces escúpelo, niñero!|Dann spuck ihn AUS, Babysitter!|"
                  "Alors recrache-le, baby-sitter !|Allora sputalo FUORI, babysitter!|Então cospe ele, babá!"),
                S("villain", "Can't! Rule number one: never let go of the little ones!|¡No puedo! Regla número uno: ¡nunca soltar a los pequeños!|"
                  "Geht nicht! Regel Nummer eins: die Kleinen nie loslassen!|Impossible ! Règle numéro un : ne jamais lâcher les petits !|"
                  "Non posso! Regola numero uno: mai lasciare i piccoli!|Não posso! Regra número um: nunca soltar os pequenos!"),
                {"villain": "lunge", "to": 1150},
                A({"shake": 0.5, "power": 16}),
                act(["bup", "zeek", "lolly"], "jump"),
                {"sfx": "sting", "wait": 0.3},
            ],
            "tail": 0.2,
        },
        {   # 3 lunchbox hideout: Crispy reveals the truth, Zeek's melter fails
            "bg": "lunchbox", "music": "heartbeat",
            "heroes": {"bup": 300, "zeek": 540, "lolly": 780, "crispy": 2100},
            "moods": {"bup": "scared", "zeek": "scared", "lolly": "scared"},
            "beats": [
                S("narr", "The heroes hid in the lunchbox to think.|Los héroes se escondieron en la lonchera para pensar.|"
                  "Die Helden versteckten sich in der Brotdose, um nachzudenken.|Les héros se sont cachés dans la boîte à goûter pour réfléchir.|"
                  "Gli eroi si nascosero nel portapranzo per pensare.|Os heróis se esconderam na lancheira para pensar."),
                mv("crispy", 1040, "walk"),
                act(["bup", "zeek", "lolly"], "jump"),
                A(S("bup", "Crispy! Stop appearing from NOWHERE!|¡Crispy! ¡Deja de aparecer de la NADA!|Crispy! Hör auf, aus dem NICHTS aufzutauchen!|"
                    "Crispy ! Arrête d'apparaître de NULLE PART !|Crispy! Smettila di spuntare dal NULLA!|Crispy! Para de aparecer do NADA!")),
                S("crispy", "Listen. Jelly does not babysit. Jelly keeps things... fresh.|Escuchen. La gelatina no cuida niños. La gelatina mantiene las cosas... frescas.|"
                  "Hört zu. Wackelpudding passt nicht auf. Wackelpudding hält Dinge... frisch.|Écoutez. La gelée ne garde pas les enfants. La gelée garde les choses... fraîches.|"
                  "Ascoltate. La gelatina non fa la babysitter. La gelatina tiene le cose... fresche.|Escutem. Gelatina não é babá. Gelatina mantém as coisas... frescas."),
                S("crispy", "Fresh and soft. Ready for Mr. Pot's golden pie.|Frescas y suaves. Listas para el pastel dorado del Señor Olla.|"
                  "Frisch und weich. Bereit für den goldenen Kuchen von Herrn Topf.|Fraîches et molles. Prêtes pour la tourte dorée de Monsieur Marmite.|"
                  "Fresche e morbide. Pronte per la torta dorata del Signor Pentola.|Frescas e macias. Prontas pra torta dourada do Senhor Panela."),
                {"sfx": "sting", "wait": 0.3},
                S("lolly", "So Wobblor is the helper. The one more helper!|Entonces Wobblor es el ayudante. ¡El ayudante que faltaba!|"
                  "Also ist Wobblor der Helfer. Der letzte Helfer!|Donc Wobblor est le complice. Le dernier complice !|"
                  "Quindi Wobblor è l'aiutante. L'ultimo aiutante!|Então o Wobblor é o ajudante. O ajudante que faltava!"),
                mood("zeek", "happy"),
                act("zeek", "bounce"),
                A(S("zeek", "Fear not! Behold my Jelly-Melter Three Thousand!|¡No teman! ¡Contemplen mi Derrite-Gelatinas Tres Mil!|"
                    "Keine Angst! Seht her: mein Wackel-Schmelzer Dreitausend!|N'ayez crainte ! Voici mon Fond-Gelée Trois Mille !|"
                    "Niente paura! Ecco il mio Scioglie-Gelatina Tremila!|Não temam! Contemplem meu Derrete-Gelatina Três Mil!")),
                {"sfx": "ding", "wait": 0.3},
                {"sfx": "pop", "wait": 0.2},
                A({"shake": 0.3, "power": 10}),
                mood("zeek", "scared"),
                S("zeek", "Hmm. It's a flashlight. I built a very warm... flashlight.|Mmm. Es una linterna. Construí una linterna... muy tibia.|"
                  "Hmm. Das ist eine Taschenlampe. Eine sehr warme... Taschenlampe.|Hmm. C'est une lampe torche. Une lampe très... tiède.|"
                  "Mmh. È una torcia. Ho costruito una torcia... molto tiepida.|Hum. É uma lanterna. Eu fiz uma lanterna... bem morninha."),
                mood("bup", "angry"),
                S("bup", "Warm! That's it! Jelly HATES warm!|¡Tibio! ¡Eso es! ¡La gelatina ODIA el calor!|Warm! Das ist es! Wackelpudding HASST Wärme!|"
                  "Chaud ! C'est ça ! La gelée DÉTESTE la chaleur !|Caldo! Ecco! La gelatina ODIA il caldo!|Quente! É isso! Gelatina ODEIA calor!"),
                S("bup", "And who is the warmest guy we know?|¿Y quién es el más calentito que conocemos?|Und wer ist der Wärmste, den wir kennen?|"
                  "Et qui est le plus chaud qu'on connaisse ?|E chi è il più caldo che conosciamo?|E quem é o cara mais quente que a gente conhece?"),
                mood("lolly", "happy"),
                S("lolly", "Old Hissy! He owes us a favor. I'll ask nicely.|¡El Viejo Siseo! Nos debe un favor. Se lo pediré amablemente.|"
                  "Der alte Zischer! Er schuldet uns was. Ich frage nett.|Le Vieux Siffleur ! Il nous doit un service. Je demanderai gentiment.|"
                  "Il Vecchio Sibilo! Ci deve un favore. Glielo chiedo con gentilezza.|O Velho Chiado! Ele nos deve um favor. Vou pedir com jeitinho."),
                mv(["bup", "zeek", "lolly", "crispy"], "off_right", "run"),
            ],
            "tail": 0.2,
        },
        {   # 4 bathroom: Lolly is the bait, the steam trap
            "bg": "bathroom", "music": "heartbeat",
            "heroes": {"lolly": 600, "pim": 1400},
            "moods": {"lolly": "happy", "pim": "scared"},
            "villain": {"type": "jelly", "x": 2300, "state": "awake", "scale": 0.9},
            "beats": [
                act("pim", "hide"),
                A(act("lolly", "shake")),
                A(S("lolly", "Oh no! I'm all alone! I need a babysitter!|¡Ay, no! ¡Estoy solita! ¡Necesito un niñero!|"
                    "Oh nein! Ich bin ganz allein! Ich brauche einen Babysitter!|Oh non ! Je suis toute seule ! Il me faut un baby-sitter !|"
                    "Oh no! Sono tutta sola! Mi serve una babysitter!|Ai, não! Estou sozinha! Preciso de uma babá!")),
                {"sfx": "creak", "wait": 0.3},
                {"villain": "lunge", "to": 1400},
                A({"shake": 0.5, "power": 16}),
                S("villain", "Did somebody say BABYSITTER? Hee hee hee!|¿Alguien dijo NIÑERO? ¡Ji ji ji!|Hat da jemand BABYSITTER gesagt? Hihihi!|"
                  "Quelqu'un a dit BABY-SITTER ? Hi hi hi !|Qualcuno ha detto BABYSITTER? Ih ih ih!|Alguém falou BABÁ? Hi hi hi!"),
                S("villain", "Such a sweet cookie... you'll be SO soft in the pie.|Qué galletita tan dulce... estarás TAN suave en el pastel.|"
                  "So ein süßer Keks... du wirst SO weich im Kuchen sein.|Quel biscuit si doux... tu seras SI moelleux dans la tourte.|"
                  "Che biscotto dolce... sarai COSÌ morbido nella torta.|Que biscoito doce... você vai ficar TÃO macio na torta."),
                S("pim", "L-Lolly, RUN! It's a t-trap!|¡L-Lolly, CORRE! ¡Es una t-trampa!|L-Lolly, LAUF! Das ist eine F-Falle!|"
                  "L-Lolly, COURS ! C'est un p-piège !|L-Lolly, SCAPPA! È una t-trappola!|L-Lolly, CORRE! É uma a-armadilha!"),
                S("lolly", "I know, sweetie. It's MY trap.|Lo sé, cariño. Es MI trampa.|Ich weiß, Schätzchen. Es ist MEINE Falle.|"
                  "Je sais, mon chou. C'est MON piège.|Lo so, tesoro. È la MIA trappola.|Eu sei, querido. A armadilha é MINHA."),
                mood("lolly", "angry"),
                S("lolly", "Old Hissy... NOW, PLEASE!|Viejo Siseo... ¡AHORA, POR FAVOR!|Alter Zischer... JETZT, BITTE!|"
                  "Vieux Siffleur... MAINTENANT, S'IL TE PLAÎT !|Vecchio Sibilo... ORA, PER FAVORE!|Velho Chiado... AGORA, POR FAVOR!"),
                {"sfx": "whoosh", "wait": 0.2},
                A({"shake": 0.9, "power": 22}),
                S("narr", "Old Hissy blew the hottest steam of his whole life.|El Viejo Siseo sopló el vapor más caliente de su vida.|"
                  "Der alte Zischer blies den heißesten Dampf seines Lebens.|Le Vieux Siffleur a soufflé la vapeur la plus chaude de sa vie.|"
                  "Il Vecchio Sibilo soffiò il vapore più caldo della sua vita.|O Velho Chiado soprou o vapor mais quente da vida dele."),
                {"villain": "rage", "level": 1.0},
                S("villain", "Too warm! TOO WARM! I'm getting RUNNY!|¡Qué calor! ¡DEMASIADO! ¡Me estoy DERRITIENDO!|Zu warm! ZU WARM! Ich werde FLÜSSIG!|"
                  "Trop chaud ! TROP CHAUD ! Je deviens LIQUIDE !|Troppo caldo! TROPPO! Mi sto SCIOGLIENDO!|Quente demais! QUENTE DEMAIS! Estou DERRETENDO!"),
                {"sfx": "pop", "wait": 0.2},
                A({"shake": 0.6, "power": 18}),
                act("pim", "show"),
                mv("pim", 1000, "run"),
                mood("pim", "happy"),
                S("pim", "I'm OUT! I'm free! I'm... very sticky!|¡SALÍ! ¡Soy libre! ¡Estoy... muy pegajoso!|Ich bin DRAUSSEN! Frei! Und... sehr klebrig!|"
                  "Je suis SORTI ! Libre ! Et... très collant !|Sono FUORI! Libero! E... molto appiccicoso!|SAÍ! Estou livre! E... muito grudento!"),
                {"villain": "lunge", "to": 1700},
                S("villain", "This isn't over, little dough! Mr. Pot will hear about this!|¡Esto no acaba aquí, masita! ¡El Señor Olla se enterará!|"
                  "Das ist noch nicht vorbei, kleiner Teig! Herr Topf wird davon hören!|Ce n'est pas fini, petite pâte ! Monsieur Marmite va l'apprendre !|"
                  "Non è finita, piccola pasta! Il Signor Pentola lo saprà!|Isso não acabou, massinha! O Senhor Panela vai ficar sabendo!"),
                {"villain": "hide"},
                A({"sfx": "whoosh", "wait": 0.3}),
                mv(["pim", "lolly"], "off_left", "run"),
            ],
            "tail": 0.2,
        },
        {   # 5 kitchen: celebration + the twist (Pim's discovery inside the jelly)
            "bg": "kitchen", "music": "music_box",
            "heroes": {"pim": 300, "bup": 540, "zeek": 780, "lolly": 1020, "crispy": 1260},
            "moods": {"pim": "happy", "bup": "happy", "zeek": "happy", "lolly": "happy"},
            "beats": [
                act(["bup", "zeek", "lolly"], "bounce"),
                A(S("bup", "Team, we did it! Nobody got baked today!|¡Equipo, lo logramos! ¡Hoy nadie terminó horneado!|"
                    "Team, geschafft! Heute wurde keiner gebacken!|L'équipe, on a réussi ! Personne n'a été cuit aujourd'hui !|"
                    "Squadra, ce l'abbiamo fatta! Oggi nessuno è finito in forno!|Equipe, conseguimos! Ninguém foi assado hoje!")),
                S("lolly", "And I said please. Twice. Manners matter.|Y dije por favor. Dos veces. Los modales importan.|"
                  "Und ich hab bitte gesagt. Zweimal. Manieren sind wichtig.|Et j'ai dit s'il te plaît. Deux fois. La politesse compte.|"
                  "E ho detto per favore. Due volte. Le buone maniere contano.|E eu disse por favor. Duas vezes. Educação importa."),
                S("zeek", "My flashlight helped too. Emotionally.|Mi linterna también ayudó. Emocionalmente.|Meine Taschenlampe hat auch geholfen. Emotional.|"
                  "Ma lampe a aidé aussi. Moralement.|Anche la mia torcia ha aiutato. Emotivamente.|Minha lanterna ajudou também. Emocionalmente."),
                S("crispy", "Don't celebrate yet. Jelly always comes back.|No celebren todavía. La gelatina siempre vuelve.|"
                  "Feiert noch nicht. Wackelpudding kommt immer zurück.|Ne fêtez pas trop vite. La gelée revient toujours.|"
                  "Non festeggiate ancora. La gelatina torna sempre.|Não comemorem ainda. Gelatina sempre volta."),
                mood("pim", "scared"),
                act("pim", "shake"),
                S("pim", "G-guys... inside the jelly, I f-found something.|Ch-chicos... dentro de la gelatina, en-encontré algo.|"
                  "L-Leute... im Wackelpudding hab ich was g-gefunden.|L-les gars... dans la gelée, j'ai t-trouvé un truc.|"
                  "R-ragazzi... dentro la gelatina ho t-trovato una cosa.|G-gente... dentro da gelatina, eu a-achei uma coisa."),
                {"sfx": "sting", "wait": 0.3},
                mood(["bup", "zeek", "lolly"], "scared"),
                S("pim", "A page from Mr. Pot's recipe book!|¡Una página del recetario del Señor Olla!|Eine Seite aus dem Rezeptbuch von Herrn Topf!|"
                  "Une page du livre de recettes de Monsieur Marmite !|Una pagina del ricettario del Signor Pentola!|Uma página do livro de receitas do Senhor Panela!"),
                S("lolly", "It's all wet and wobbly. Ew. Read it anyway!|Está toda mojada y temblorosa. Puaj. ¡Léela igual!|"
                  "Sie ist ganz nass und wabbelig. Igitt. Lies trotzdem!|Elle est toute mouillée et tremblotante. Beurk. Lis quand même !|"
                  "È tutta bagnata e tremolante. Bleah. Leggila lo stesso!|Está toda molhada e mole. Eca. Lê assim mesmo!"),
                S("zeek", "What does it say, Pim?|¿Qué dice, Pim?|Was steht da, Pim?|Qu'est-ce que ça dit, Pim ?|Cosa dice, Pim?|O que diz, Pim?"),
                S("pim", "Step one: five fresh doughs. Step two: one VERY hot oven.|Paso uno: cinco masas frescas. Paso dos: un horno MUY caliente.|"
                  "Schritt eins: fünf frische Teige. Schritt zwei: ein SEHR heißer Ofen.|Étape un : cinq pâtes fraîches. Étape deux : un four TRÈS chaud.|"
                  "Primo passo: cinque impasti freschi. Secondo passo: un forno MOLTO caldo.|Passo um: cinco massas frescas. Passo dois: um forno MUITO quente."),
                S("crispy", "The oven has been cold for years. Only one thing can wake it.|El horno lleva años frío. Solo una cosa puede despertarlo.|"
                  "Der Ofen ist seit Jahren kalt. Nur eins kann ihn wecken.|Le four est froid depuis des années. Une seule chose peut le réveiller.|"
                  "Il forno è freddo da anni. Solo una cosa può svegliarlo.|O forno está frio há anos. Só uma coisa pode acordá-lo."),
                act("pim", "faint"),
                S("bup", "Then we guard that oven. Tonight. All of us.|Entonces vigilamos ese horno. Esta noche. Todos.|"
                  "Dann bewachen wir den Ofen. Heute Nacht. Alle zusammen.|Alors on garde ce four. Cette nuit. Tous ensemble.|"
                  "Allora sorvegliamo quel forno. Stanotte. Tutti insieme.|Então a gente vigia esse forno. Hoje à noite. Todos nós."),
            ],
            "tail": 0.2,
        },
        {   # 6 cliffhanger: the oven clicks on — Toastmaw is back
            "bg": "oven", "music": "drone",
            "heroes": {"pim": 320, "bup": 560, "zeek": 800},
            "moods": {"pim": "scared", "bup": "scared", "zeek": "scared"},
            "villain": {"type": "toaster", "x": 1450, "state": "hidden", "scale": 0.9},
            "beats": [
                {"sfx": "ding", "wait": 0.4},
                S("narr", "At midnight, something went DING inside the oven.|A medianoche, algo hizo DING dentro del horno.|"
                  "Um Mitternacht machte etwas DING im Ofen.|À minuit, quelque chose a fait DING dans le four.|"
                  "A mezzanotte, qualcosa fece DING dentro il forno.|À meia-noite, algo fez DING dentro do forno."),
                act("zeek", "shake"),
                S("zeek", "My calculations say... ovens don't go DING.|Mis cálculos dicen... que los hornos no hacen DING.|"
                  "Meine Berechnungen sagen... Öfen machen kein DING.|Mes calculs disent... que les fours ne font pas DING.|"
                  "I miei calcoli dicono... che i forni non fanno DING.|Meus cálculos dizem... que forno não faz DING."),
                S("pim", "B-but TOASTERS do!|¡P-pero las TOSTADORAS sí!|A-aber TOASTER schon!|M-mais les GRILLE-PAIN, si !|M-ma i TOSTAPANE sì!|M-mas TORRADEIRAS fazem!"),
                S("bup", "Okay team... nobody touch the oven door.|Bien, equipo... nadie toque la puerta del horno.|"
                  "Okay, Team... keiner fasst die Ofentür an.|OK l'équipe... personne ne touche la porte du four.|"
                  "Ok squadra... nessuno tocchi lo sportello del forno.|Certo, equipe... ninguém encosta na porta do forno."),
                {"sfx": "creak", "wait": 0.4},
                A({"shake": 0.3, "power": 10}),
                {"villain": "show"},
                {"villain": "wake"},
                {"shake": 0.6, "power": 18},
                S("villain", "Remember me, little dough? Mr. Pot hired me... to heat the oven.|¿Me recuerdan, masitas? El Señor Olla me contrató... para calentar el horno.|"
                  "Erinnert ihr euch, kleiner Teig? Herr Topf hat mich angeheuert... um den Ofen zu heizen.|Vous vous souvenez de moi ? Monsieur Marmite m'a engagé... pour chauffer le four.|"
                  "Vi ricordate di me, piccola pasta? Il Signor Pentola mi ha assunto... per scaldare il forno.|Lembram de mim, massinha? O Senhor Panela me contratou... pra esquentar o forno."),
                S("zeek", "Toastmaw! The angry toaster from the trap!|¡Tostamaw! ¡La tostadora furiosa de la trampa!|"
                  "Toastmaw! Der wütende Toaster aus der Falle!|Toastmaw ! Le grille-pain furieux du piège !|"
                  "Toastmaw! Il tostapane arrabbiato della trappola!|Toastmaw! A torradeira furiosa da armadilha!"),
                {"villain": "rage", "level": 1.0},
                S("villain", "Preheating to three hundred and fifty. You're TOAST!|Precalentando a ciento ochenta. ¡Están TOSTADOS!|"
                  "Vorheizen auf zweihundert Grad. Ihr seid TOAST!|Préchauffage à deux cents degrés. Vous êtes GRILLÉS !|"
                  "Preriscaldamento a duecento gradi. Siete TOSTATI!|Preaquecendo a duzentos graus. Vocês viraram TORRADA!"),
                act(["pim", "bup", "zeek"], "scream"),
                {"villain": "lunge", "to": 1150},
                A({"shake": 0.8, "power": 22}),
            ],
            "tail": 0.6,
        },
    ],
}


short1 = {
    "id": "ep011_short1", "format": "short",
    "title": "Lolly Said PLEASE 3 Times... 😡 #shorts",
    "hook": "NEVER MAKE HER ASK TWICE",
    "description": ("Lolly is the most polite cookie in Table Land. She will say please. Once. Twice. "
                    "Do NOT make her say it a third time. "
                    f"Full episode: \"{LONG_TITLE}\" {{LONG_URL}} — more on {CHANNEL} "
                    "#shorts #animation #cartoon #doughbros #funnycartoon"),
    "tags": SHORT_TAGS + ["lolly", "angry cookie", "wobblor", "jelly monster"],
    "thumbnail": {"bg": "fridge", "villain": "jelly", "heroes": ["lolly"], "text": "PLEASE #3"},
    "scenes": [{
        "bg": "fridge", "music": "heartbeat",
        "heroes": {"lolly": 640, "pim": 330},
        "moods": {"lolly": "happy", "pim": "scared"},
        "villain": {"type": "jelly", "x": 1450, "state": "awake", "scale": 0.85},
        "beats": [
            {"villain": "lunge", "to": 1250},
            A(S("villain", "Hee hee! Come inside me, little cookie!|¡Ji ji! ¡Entra en mí, galletita!|Hihi! Komm in mich rein, kleiner Keks!|"
                "Hi hi ! Viens en moi, petit biscuit !|Ih ih! Vieni dentro di me, biscottino!|Hi hi! Entra em mim, biscoitinho!")),
            A({"shake": 0.4, "power": 14}),
            S("lolly", "No, thank you. Please leave us alone.|No, gracias. Por favor, déjanos en paz.|Nein, danke. Bitte lass uns in Ruhe.|"
              "Non, merci. S'il te plaît, laisse-nous tranquilles.|No, grazie. Per favore, lasciaci in pace.|Não, obrigada. Por favor, deixa a gente em paz."),
            {"villain": "lunge", "to": 1100},
            A(act("pim", "shake")),
            S("lolly", "I said PLEASE. That's two.|Dije POR FAVOR. Van dos.|Ich sagte BITTE. Das ist zwei.|J'ai dit S'IL TE PLAÎT. Ça fait deux.|Ho detto PER FAVORE. Siamo a due.|Eu disse POR FAVOR. Já são duas."),
            S("villain", "Hee hee! Say it AGAIN!|¡Ji ji! ¡Dilo OTRA VEZ!|Hihi! Sag es NOCHMAL!|Hi hi ! Redis-le !|Ih ih! Dillo ANCORA!|Hi hi! Fala DE NOVO!"),
            S("pim", "Oh n-no. Not number THREE!|¡Ay n-no! ¡El número TRES no!|Oh n-nein. Nicht Nummer DREI!|Oh n-non. Pas le numéro TROIS !|Oh n-no. Non il numero TRE!|Ai n-não. O número TRÊS não!"),
            mood("lolly", "angry"),
            {"sfx": "sting", "wait": 0.1},
            S("lolly", "PLEEEASE!|¡POR FAVOOOR!|BIIIITTE!|S'IL TE PLAÎÎÎT !|PER FAVOOORE!|POR FAVOOOR!"),
            A({"shake": 0.9, "power": 24}),
            {"villain": "rage", "level": 1.0},
            A(act("pim", "faint")),
            {"villain": "hide"},
            A({"sfx": "whoosh", "wait": 0.2}),
            mood("lolly", "happy"),
            S("lolly", "Manners, sweetie. They always work.|Modales, cariño. Siempre funcionan.|Manieren, Schätzchen. Die wirken immer.|"
              "La politesse, mon chou. Ça marche toujours.|Buone maniere, tesoro. Funzionano sempre.|Educação, querido. Sempre funciona."),
            S("pim", "You... you scared a JELLY!|¡Tú... asustaste a una GELATINA!|Du... du hast einen WACKELPUDDING verjagt!|"
              "Tu... tu as fait peur à une GELÉE !|Tu... hai spaventato una GELATINA!|Você... você assustou uma GELATINA!"),
            mood("pim", "scared"),
            {"sfx": "creak", "wait": 0.1},
            {"villain": "show"},
            A({"villain": "wake"}),
            S("villain", "Hee hee... I'm BACK!|Ji ji... ¡VOLVÍ!|Hihi... ich bin WIEDER DA!|Hi hi... je suis DE RETOUR !|Ih ih... sono TORNATO!|Hi hi... VOLTEI!"),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    for sc in s["scenes"]:
        sc["beats"] = flat(sc["beats"])
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"], len(s["title"]))

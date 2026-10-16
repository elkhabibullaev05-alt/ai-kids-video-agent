"""Builds the EP10 pack (1 long + 1 short). Run: python3 scripts/_build_ep010.py"""
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


LONG_TITLE = "5 Heroes, 1 Shelf, NO Way Down 😱 | EP 10"
CHANNEL = "https://www.youtube.com/@DoughBrosTV"
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "mr pot", "great escape", "cursed cauldron"]
SHORT_TAGS = ["shorts", "animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon",
              "horror comedy", "animated series"]
FIVE = ["pim", "bup", "zeek", "lolly", "crispy"]

long_ = {
    "id": "ep010_long", "format": "long",
    "title": LONG_TITLE,
    "hook": "HE'S RIGHT BELOW US!", "hook_dur": 3.5,
    "description": ("Mr. Pot finally came himself. The Dough Bros escape to the top shelf of the pantry... "
                    "but a pot can wait FOREVER. Zeek's napkin parachute lasts two seconds, Crispy reveals the secret "
                    "way down he used the night Mr. Pot burnt him, and Lolly gets VERY angry. "
                    "But why does Mr. Pot need all FIVE of them?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy #mrpot"),
    "tags": TAGS + ["episode 10", "crispy", "lolly", "wobblor"],
    "thumbnail": {"bg": "pantry", "villain": "pot", "heroes": ["pim"], "text": "NO WAY DOWN!"},
    "scenes": [
        {   # 1 cold open: Mr. Pot lunges (motion + line at 0 s)
            "bg": "kitchen", "music": "drone",
            "heroes": {"pim": 300, "bup": 520, "zeek": 740, "lolly": 960, "crispy": 1140},
            "moods": {"pim": "scared", "bup": "scared", "zeek": "scared", "lolly": "scared"},
            "villain": {"type": "pot", "x": 1520, "state": "awake", "scale": 0.9},
            "beats": [
                {"villain": "lunge", "to": 1360},
                A(S("villain", "Time to FRY, little dough!|¡Hora de FREÍR, masita!|Zeit zum BRATEN, kleiner Teig!|"
                    "C'est l'heure de FRIRE, petite pâte !|È ora di FRIGGERE, piccola pasta!|Hora de FRITAR, massinha!")),
                A({"shake": 0.6, "power": 18}),
                act(["pim", "bup", "zeek", "lolly"], "scream"),
                mood("bup", "angry"),
                S("bup", "UP! Everybody climb the shelf! NOW!|¡ARRIBA! ¡Todos a la repisa! ¡YA!|HOCH! Alle aufs Regal! SOFORT!|"
                  "EN HAUT ! Tout le monde sur l'étagère ! VITE !|SU! Tutti sulla mensola! ORA!|PARA CIMA! Todo mundo na prateleira! JÁ!"),
                mv(["pim", "bup", "zeek", "lolly"], "off_left", "run"),
                S("crispy", "Run, my friends. I know this pot.|Corran, amigos. Conozco a esta olla.|Lauft, Freunde. Ich kenne diesen Topf.|"
                  "Courez, mes amis. Je connais cette marmite.|Correte, amici. Conosco questa pentola.|Corram, amigos. Eu conheço essa panela."),
                {"villain": "rage", "level": 0.8},
                S("villain", "Crispy... my burnt little mistake. Still alive?|Crispy... mi pequeño error quemado. ¿Sigues vivo?|"
                  "Crispy... mein verbrannter kleiner Fehler. Noch am Leben?|Crispy... ma petite erreur brûlée. Toujours là ?|"
                  "Crispy... il mio piccolo errore bruciato. Ancora vivo?|Crispy... meu errinho queimado. Ainda vivo?"),
                mv("crispy", "off_left", "walk"),
                {"villain": "roar"},
            ],
            "tail": 0.3,
        },
        {   # 2 top shelf: the pot waits, Zeek's parachute fails
            "bg": "pantry", "music": "heartbeat",
            "heroes": {"pim": 300, "bup": 520, "zeek": 740, "lolly": 960, "crispy": 1160},
            "moods": {"pim": "scared"},
            "villain": {"type": "pot", "x": 1560, "state": "awake", "scale": 0.7},
            "beats": [
                act("pim", "shake"),
                A(S("narr", "The top shelf. Safe... for now.|La repisa de arriba. A salvo... por ahora.|Das oberste Regal. Sicher... vorerst.|"
                    "L'étagère du haut. En sécurité... pour l'instant.|La mensola più alta. Al sicuro... per ora.|A prateleira de cima. Seguros... por enquanto.")),
                S("villain", "I'll wait right here. You have to come down... eventually.|Esperaré aquí mismo. Tendrán que bajar... tarde o temprano.|"
                  "Ich warte genau hier. Irgendwann müsst ihr runterkommen.|J'attends ici. Vous devrez bien descendre... un jour.|"
                  "Aspetterò proprio qui. Prima o poi dovrete scendere.|Vou esperar bem aqui. Vocês vão ter que descer... uma hora."),
                mood("bup", "angry"),
                S("bup", "Okay team, here's the plan. Step one: nobody panics.|Bien, equipo, este es el plan. Paso uno: nadie entra en pánico.|"
                  "Okay, Team, hier ist der Plan. Schritt eins: keiner gerät in Panik.|OK l'équipe, voici le plan. Étape un : personne ne panique.|"
                  "Ok squadra, ecco il piano. Primo passo: nessuno va nel panico.|Certo, equipe, o plano é esse. Passo um: ninguém entra em pânico."),
                act("pim", "shake"),
                S("pim", "T-too late! I'm p-panicking a LOT!|¡D-demasiado tarde! ¡Estoy en p-pánico TOTAL!|Z-zu spät! Ich bin in t-totaler PANIK!|"
                  "T-trop tard ! Je p-panique ÉNORMÉMENT !|T-troppo tardi! Sono in p-panico TOTALE!|T-tarde demais! Estou em p-pânico TOTAL!"),
                S("pim", "H-how long can a pot w-wait?|¿C-cuánto puede esperar una olla?|W-wie lange kann ein Topf w-warten?|"
                  "C-combien de temps une marmite peut a-attendre ?|Q-quanto può aspettare una pentola?|Q-quanto tempo uma panela consegue e-esperar?"),
                S("crispy", "Forever. He once waited a whole winter for me.|Para siempre. Una vez me esperó un invierno entero.|"
                  "Für immer. Er hat einmal einen ganzen Winter auf mich gewartet.|Pour toujours. Il m'a attendu tout un hiver.|"
                  "Per sempre. Una volta mi ha aspettato un inverno intero.|Para sempre. Uma vez ele me esperou um inverno inteiro."),
                mood("zeek", "happy"),
                act("zeek", "bounce"),
                A(S("zeek", "Fear not! My napkin parachute will float us gently down!|¡No teman! ¡Mi paracaídas de servilleta nos bajará suavemente!|"
                    "Keine Angst! Mein Serviettenfallschirm bringt uns sanft hinunter!|N'ayez crainte ! Mon parachute-serviette va nous poser en douceur !|"
                    "Niente paura! Il mio paracadute di tovagliolo ci farà scendere piano!|Não temam! Meu paraquedas de guardanapo vai nos descer devagar!")),
                {"sfx": "whoosh", "wait": 0.2},
                act("zeek", "spin"),
                {"sfx": "pop", "wait": 0.3},
                {"sfx": "thump", "wait": 0.3},
                A({"shake": 0.5, "power": 16}),
                mood("zeek", "scared"),
                S("zeek", "Small problem. Napkins are... not parachutes.|Pequeño problema. Las servilletas... no son paracaídas.|"
                  "Kleines Problem. Servietten sind... keine Fallschirme.|Petit problème. Les serviettes... ne sont pas des parachutes.|"
                  "Piccolo problema. I tovaglioli... non sono paracadute.|Probleminha. Guardanapos... não são paraquedas."),
                act("pim", "faint"),
                S("lolly", "Zeek, sweetie... please stop inventing things.|Zeek, cariño... por favor, deja de inventar cosas.|"
                  "Zeek, Schätzchen... bitte hör auf, Dinge zu erfinden.|Zeek, mon chou... arrête d'inventer des trucs, s'il te plaît.|"
                  "Zeek, tesoro... per favore smetti di inventare cose.|Zeek, querido... por favor, pare de inventar coisas."),
                {"villain": "roar"},
                S("villain", "Hungry... so HUNGRY! Come down, come DOWN!|Hambre... ¡tanta HAMBRE! ¡Bajen, BAJEN!|Hunger... so viel HUNGER! Kommt runter, RUNTER!|"
                  "Faim... tellement FAIM ! Descendez, DESCENDEZ !|Fame... che FAME! Scendete, SCENDETE!|Fome... tanta FOME! Desçam, DESÇAM!"),
            ],
            "tail": 0.3,
        },
        {   # 3 Crispy's secret way down
            "bg": "pantry", "music": "music_box",
            "heroes": {"pim": 300, "bup": 540, "zeek": 780, "lolly": 1020, "crispy": 1300},
            "beats": [
                S("crispy", "There is another way down. Behind the honey jar.|Hay otra forma de bajar. Detrás del frasco de miel.|"
                  "Es gibt noch einen Weg nach unten. Hinter dem Honigglas.|Il y a un autre chemin. Derrière le pot de miel.|"
                  "C'è un'altra via per scendere. Dietro il barattolo di miele.|Tem outro jeito de descer. Atrás do pote de mel."),
                mv("bup", 900, "walk"),
                S("bup", "Wait. How do YOU know that?|Espera. ¿Cómo sabes TÚ eso?|Moment. Woher weißt DU das?|Attends. Comment TU sais ça ?|Aspetta. Come lo sai TU?|Espera. Como VOCÊ sabe disso?"),
                mood(["bup", "zeek", "lolly"], "scared"),
                {"sfx": "sting", "wait": 0.3},
                S("crispy", "Because I used it... the night Mr. Pot burnt me.|Porque lo usé... la noche que el Señor Olla me quemó.|"
                  "Weil ich ihn benutzt habe... in der Nacht, als Herr Topf mich verbrannte.|Parce que je l'ai pris... la nuit où Monsieur Marmite m'a brûlé.|"
                  "Perché l'ho usata... la notte in cui il Signor Pentola mi ha bruciato.|Porque eu usei... na noite em que o Senhor Panela me queimou."),
                S("crispy", "I was fresh dough once. Soft. Golden. Just like you.|Una vez fui masa fresca. Suave. Dorada. Igual que ustedes.|"
                  "Ich war auch mal frischer Teig. Weich. Golden. Genau wie ihr.|J'étais une pâte fraîche, avant. Douce. Dorée. Comme vous.|"
                  "Una volta ero pasta fresca. Morbida. Dorata. Proprio come voi.|Eu já fui massa fresca. Macia. Dourada. Igual a vocês."),
                act("pim", "jump"),
                S("pim", "Y-you were... GOLDEN?|¿E-eras... DORADO?|D-du warst... GOLDEN?|T-tu étais... DORÉ ?|E-eri... DORATO?|V-você era... DOURADO?"),
                mood("lolly", "happy"),
                S("lolly", "Oh, Crispy... that's so sad. Come here, you need a hug.|Ay, Crispy... qué triste. Ven aquí, necesitas un abrazo.|"
                  "Oh, Crispy... das ist so traurig. Komm her, du brauchst eine Umarmung.|Oh, Crispy... c'est si triste. Viens là, il te faut un câlin.|"
                  "Oh, Crispy... è così triste. Vieni qui, ti serve un abbraccio.|Ah, Crispy... que triste. Vem cá, você precisa de um abraço."),
                S("crispy", "No hugs. Be FAST. He can hear us.|Nada de abrazos. Sean RÁPIDOS. Nos puede oír.|Keine Umarmungen. Seid SCHNELL. Er hört uns.|"
                  "Pas de câlins. Soyez RAPIDES. Il nous entend.|Niente abbracci. Siate VELOCI. Ci sente.|Nada de abraços. Sejam RÁPIDOS. Ele está ouvindo."),
                {"sfx": "clank", "wait": 0.3},
                A({"shake": 0.5, "power": 16}),
                act(["pim", "zeek", "lolly"], "jump"),
                S("zeek", "My calculations say... that was the pot CLIMBING!|Mis cálculos dicen... ¡que esa fue la olla TREPANDO!|"
                  "Meine Berechnungen sagen... das war der Topf, der KLETTERT!|Mes calculs disent... que c'était la marmite qui GRIMPE !|"
                  "I miei calcoli dicono... che era la pentola che si ARRAMPICA!|Meus cálculos dizem... que foi a panela SUBINDO!"),
                mood("bup", "angry"),
                S("bup", "Behind the jar! Go, go, GO!|¡Detrás del frasco! ¡Vamos, vamos, YA!|Hinter das Glas! Los, los, LOS!|"
                  "Derrière le pot ! Allez, allez, ALLEZ !|Dietro il barattolo! Via, via, VIA!|Atrás do pote! Vai, vai, VAI!"),
                mv(["pim", "bup", "zeek", "lolly", "crispy"], "off_right", "run"),
            ],
            "tail": 0.3,
        },
        {   # 4 dinner table: the chase, Lolly slams the lid
            "bg": "table", "music": "heartbeat",
            "heroes": {"pim": -200, "bup": -420, "zeek": -640, "lolly": -860},
            "villain": {"type": "pot", "x": 1550, "state": "hidden", "scale": 0.85},
            "beats": [
                mv("pim", 560, "run"), mv("bup", 340, "run", True), mv("zeek", 160, "run", True), mv("lolly", 760, "run", True),
                mood("pim", "happy"),
                act("pim", "bounce"),
                A(S("pim", "We made it! The dinner table! We're SAFE!|¡Lo logramos! ¡La mesa! ¡Estamos A SALVO!|Geschafft! Der Esstisch! Wir sind SICHER!|"
                    "On a réussi ! La table ! On est SAUVÉS !|Ce l'abbiamo fatta! La tavola! Siamo SALVI!|Conseguimos! A mesa de jantar! Estamos SALVOS!")),
                {"sfx": "creak", "wait": 0.4},
                {"villain": "show"},
                {"villain": "wake"},
                S("villain", "Did you really think... you could slide away from ME?|¿De verdad creyeron... que podían escaparse de MÍ?|"
                  "Habt ihr wirklich gedacht... ihr könnt MIR entwischen?|Vous pensiez vraiment... pouvoir m'échapper, à MOI ?|"
                  "Pensavate davvero... di scivolare via da ME?|Vocês acharam mesmo... que iam escapar de MIM?"),
                mood(["pim", "bup", "zeek", "lolly"], "scared"),
                act(["pim", "bup", "zeek", "lolly"], "scream"),
                {"villain": "lunge", "to": 1300},
                A({"shake": 0.5, "power": 16}),
                S("bup", "Plan B! Everybody split UP!|¡Plan B! ¡Todos SEPÁRENSE!|Plan B! Alle VERTEILEN!|Plan B ! Tout le monde se SÉPARE !|Piano B! Tutti SEPARATI!|Plano B! Todo mundo se SEPARA!"),
                mv("bup", 120, "run"), mv("zeek", -300, "run", True), mv("pim", 1040, "run", True),
                S("lolly", "Pim! That's the WRONG way!|¡Pim! ¡Por AHÍ no!|Pim! Das ist die FALSCHE Richtung!|Pim ! C'est le MAUVAIS côté !|Pim! È la direzione SBAGLIATA!|Pim! É o lado ERRADO!"),
                act("pim", "shake"),
                S("villain", "One little bean... coming right to me. How polite.|Un frijolito... viene directo a mí. Qué educado.|"
                  "Eine kleine Bohne... kommt direkt zu mir. Wie höflich.|Un petit haricot... qui vient droit vers moi. Quelle politesse.|"
                  "Un fagiolino... che viene dritto da me. Che gentile.|Um feijãozinho... vindo direto pra mim. Que educado."),
                mood("lolly", "angry"),
                S("lolly", "Hey! NOBODY cooks our Pim!|¡Oye! ¡NADIE cocina a nuestro Pim!|Hey! NIEMAND kocht unseren Pim!|"
                  "Hé ! PERSONNE ne cuisine notre Pim !|Ehi! NESSUNO cucina il nostro Pim!|Ei! NINGUÉM cozinha o nosso Pim!"),
                mv("lolly", 1180, "run"),
                {"sfx": "clank", "wait": 0.2},
                A({"shake": 0.8, "power": 22}),
                {"villain": "rage", "level": 1.0},
                S("narr", "Lolly slammed the lid down on Mr. Pot. HARD.|Lolly le cerró la tapa al Señor Olla. FUERTE.|"
                  "Lolly knallte Herrn Topf den Deckel drauf. FEST.|Lolly a claqué le couvercle sur Monsieur Marmite. FORT.|"
                  "Lolly ha sbattuto il coperchio sul Signor Pentola. FORTE.|Lolly bateu a tampa no Senhor Panela. COM FORÇA."),
                {"sfx": "rattle", "wait": 0.3},
                S("villain", "Mmmf! Let me OUT! This is MY lid!|¡Mmmf! ¡Déjenme SALIR! ¡Es MI tapa!|Mmmpf! Lasst mich RAUS! Das ist MEIN Deckel!|"
                  "Mmmf ! Laissez-moi SORTIR ! C'est MON couvercle !|Mmmf! Fatemi USCIRE! È il MIO coperchio!|Mmmf! Me deixem SAIR! Essa é a MINHA tampa!"),
                {"villain": "sleep"},
                mood("pim", "happy"),
                S("pim", "Lolly... you SAVED me!|Lolly... ¡me SALVASTE!|Lolly... du hast mich GERETTET!|Lolly... tu m'as SAUVÉ !|Lolly... mi hai SALVATO!|Lolly... você me SALVOU!"),
                S("lolly", "Run now, sweetie. Thank me later!|Corre ahora, cariño. ¡Me agradeces después!|Lauf jetzt, Schätzchen. Danken kannst du später!|"
                  "Cours, mon chou. Tu me remercieras plus tard !|Corri ora, tesoro. Mi ringrazi dopo!|Corre agora, querido. Me agradece depois!"),
                mv(["lolly", "pim"], "off_left", "run"),
            ],
            "tail": 0.3,
        },
        {   # 5 kitchen: celebration + the twist (the five-dough pie)
            "bg": "kitchen", "music": "music_box",
            "heroes": {"pim": 300, "bup": 540, "zeek": 780, "lolly": 1020, "crispy": 1260},
            "moods": {"pim": "happy", "bup": "happy", "zeek": "happy", "lolly": "happy"},
            "beats": [
                act("zeek", "bounce"),
                A(S("zeek", "A cookie sitting on a lid. Weight beats heat. Science!|Una galleta sentada en una tapa. El peso gana al calor. ¡Ciencia!|"
                    "Ein Keks auf einem Deckel. Gewicht schlägt Hitze. Wissenschaft!|Un biscuit assis sur un couvercle. Le poids bat la chaleur. La science !|"
                    "Un biscotto seduto su un coperchio. Il peso batte il calore. Scienza!|Um biscoito sentado na tampa. Peso vence calor. Ciência!")),
                S("pim", "Lolly, you're t-terrifying. And I love you.|Lolly, das m-miedo. Y te quiero.|Lolly, du bist f-furchterregend. Und ich hab dich lieb.|"
                  "Lolly, tu es t-terrifiante. Et je t'adore.|Lolly, sei t-terrificante. E ti voglio bene.|Lolly, você é a-assustadora. E eu te amo."),
                S("lolly", "Aww, thank you, sweetie!|¡Aww, gracias, cariño!|Ooh, danke, Schätzchen!|Ooh, merci, mon chou !|Ooh, grazie, tesoro!|Own, obrigada, querido!"),
                mood("bup", "normal"),
                mv("bup", 640, "walk"),
                S("bup", "But why does he want ALL five of us? Why five?|Pero ¿por qué nos quiere a los CINCO? ¿Por qué cinco?|"
                  "Aber warum will er uns ALLE fünf? Warum fünf?|Mais pourquoi il nous veut TOUS les cinq ? Pourquoi cinq ?|"
                  "Ma perché vuole TUTTI e cinque? Perché cinque?|Mas por que ele quer os CINCO? Por que cinco?"),
                {"sfx": "sting", "wait": 0.3},
                S("crispy", "Because of the old recipe. Five doughs... one golden pie.|Por la vieja receta. Cinco masas... un pastel dorado.|"
                  "Wegen des alten Rezepts. Fünf Teige... ein goldener Kuchen.|À cause de la vieille recette. Cinq pâtes... une tourte dorée.|"
                  "Per la vecchia ricetta. Cinque impasti... una torta dorata.|Por causa da receita antiga. Cinco massas... uma torta dourada."),
                mood(["pim", "bup", "zeek", "lolly"], "scared"),
                S("zeek", "A pie? He wants to bake us into a PIE?!|¿Un pastel? ¡¿Quiere hornearnos en un PASTEL?!|Ein Kuchen? Er will uns zu einem KUCHEN backen?!|"
                  "Une tourte ? Il veut faire de nous une TOURTE ?!|Una torta? Vuole cuocerci in una TORTA?!|Uma torta? Ele quer assar a gente numa TORTA?!"),
                act("pim", "scream"),
                act("pim", "faint"),
                S("crispy", "And he only needs one more helper to do it.|Y solo necesita un ayudante más para hacerlo.|Und er braucht nur noch einen Helfer dafür.|"
                  "Et il ne lui manque plus qu'un seul complice.|E gli serve solo un altro aiutante per farlo.|E ele só precisa de mais um ajudante pra isso."),
                mood("bup", "angry"),
                S("bup", "Then we stop him BEFORE he finds that helper.|Entonces lo detenemos ANTES de que encuentre a ese ayudante.|"
                  "Dann halten wir ihn auf, BEVOR er diesen Helfer findet.|Alors on l'arrête AVANT qu'il trouve ce complice.|"
                  "Allora lo fermiamo PRIMA che trovi quell'aiutante.|Então a gente para ele ANTES que ache esse ajudante."),
                mood(["lolly", "zeek"], "happy"),
                act(["bup", "zeek", "lolly", "crispy"], "bounce"),
                A(S("lolly", "Together. All five of us. Always.|Juntos. Los cinco. Siempre.|Zusammen. Alle fünf. Immer.|Ensemble. Tous les cinq. Toujours.|Insieme. Tutti e cinque. Sempre.|Juntos. Os cinco. Sempre.")),
                S("zeek", "Tomorrow. After a nap. Science says heroes need sleep.|Mañana. Después de una siesta. La ciencia dice que los héroes duermen.|"
                  "Morgen. Nach einem Nickerchen. Die Wissenschaft sagt, Helden brauchen Schlaf.|Demain. Après une sieste. La science dit que les héros dorment.|"
                  "Domani. Dopo un pisolino. La scienza dice che gli eroi dormono.|Amanhã. Depois de um cochilo. A ciência diz que herói precisa dormir."),
            ],
            "tail": 0.3,
        },
        {   # 6 cliffhanger: the fridge giggles (Wobblor)
            "bg": "fridge", "music": "drone",
            "heroes": {"pim": 320, "bup": 560, "lolly": 800},
            "moods": {"pim": "scared", "bup": "scared", "lolly": "scared"},
            "villain": {"type": "jelly", "x": 1450, "state": "hidden", "scale": 0.9},
            "beats": [
                {"sfx": "creak", "wait": 0.4},
                S("narr", "That night, the fridge light turned on... by itself.|Esa noche, la luz del refri se encendió... sola.|"
                  "In dieser Nacht ging das Kühlschranklicht an... von allein.|Cette nuit-là, la lumière du frigo s'est allumée... toute seule.|"
                  "Quella notte, la luce del frigo si accese... da sola.|Naquela noite, a luz da geladeira acendeu... sozinha."),
                act("pim", "shake"),
                S("pim", "G-guys... did the fridge just... GIGGLE?|C-chicos... ¿el refri acaba de... REÍRSE?|L-Leute... hat der Kühlschrank gerade... GEKICHERT?|"
                  "L-les gars... le frigo vient de... GLOUSSER ?|R-ragazzi... il frigo ha appena... RIDACCHIATO?|G-gente... a geladeira acabou de... DAR RISADINHA?"),
                {"villain": "show"},
                {"villain": "wake"},
                S("villain", "Hee hee... Mr. Pot asked me to look after you.|Ji ji... el Señor Olla me pidió que los cuidara.|"
                  "Hihi... Herr Topf hat mich gebeten, auf euch aufzupassen.|Hi hi... Monsieur Marmite m'a demandé de vous surveiller.|"
                  "Ih ih... il Signor Pentola mi ha chiesto di badare a voi.|Hi hi... o Senhor Panela me pediu pra cuidar de vocês."),
                {"villain": "rage", "level": 0.8},
                S("villain", "Come inside me, little dough... it's SO comfy.|Entren en mí, masita... es TAN cómodo.|Kommt in mich hinein, kleiner Teig... es ist SO gemütlich.|"
                  "Venez en moi, petite pâte... c'est SI confortable.|Entrate dentro di me, piccola pasta... è COSÌ comodo.|Entrem em mim, massinha... é TÃO confortável."),
                act(["pim", "bup", "lolly"], "scream"),
                {"villain": "lunge", "to": 1150},
                A({"shake": 0.7, "power": 20}),
            ],
            "tail": 0.6,
        },
    ],
}

short1 = {
    "id": "ep010_short1", "format": "short",
    "title": "Zeek's Parachute Lasted 2 Seconds 🪂 #shorts",
    "hook": "TRUST ME, I'M A GENIUS",
    "description": ("Zeek's napkin parachute is PERFECT. His calculations say so. Gravity says no. "
                    f"Full episode: \"{LONG_TITLE}\" {{LONG_URL}} — more on {CHANNEL} "
                    "#shorts #animation #cartoon #doughbros #funnycartoon"),
    "tags": SHORT_TAGS + ["zeek", "parachute", "invention fail", "mr pot"],
    "thumbnail": {"bg": "pantry", "villain": "pot", "heroes": ["zeek"], "text": "GRAVITY WINS"},
    "scenes": [{
        "bg": "pantry", "music": "heartbeat",
        "heroes": {"zeek": 700, "bup": 330, "pim": -300},
        "moods": {"zeek": "happy"},
        "villain": {"type": "pot", "x": 1500, "state": "hidden", "scale": 0.8},
        "beats": [
            act("zeek", "bounce"),
            A(S("zeek", "Trust me. I'm a genius. Napkin parachute, GO!|Confíen en mí. Soy un genio. ¡Paracaídas de servilleta, YA!|"
                "Vertraut mir. Ich bin ein Genie. Serviettenfallschirm, LOS!|Faites-moi confiance. Je suis un génie. Parachute-serviette, GO !|"
                "Fidatevi. Sono un genio. Paracadute di tovagliolo, VIA!|Confiem em mim. Sou um gênio. Paraquedas de guardanapo, JÁ!")),
            {"sfx": "whoosh", "wait": 0.1},
            act("zeek", "spin"),
            {"sfx": "pop", "wait": 0.2},
            {"sfx": "thump", "wait": 0.2},
            A({"shake": 0.5, "power": 18}),
            mood("zeek", "scared"),
            S("bup", "Zeek? ZEEK! Did it work?|¿Zeek? ¡ZEEK! ¿Funcionó?|Zeek? ZEEK! Hat es funktioniert?|Zeek ? ZEEK ! Ça a marché ?|Zeek? ZEEK! Ha funzionato?|Zeek? ZEEK! Funcionou?"),
            act("zeek", "shake"),
            S("zeek", "Two seconds of flight. A new record!|Dos segundos de vuelo. ¡Un nuevo récord!|Zwei Sekunden Flug. Ein neuer Rekord!|"
              "Deux secondes de vol. Un nouveau record !|Due secondi di volo. Un nuovo record!|Dois segundos de voo. Um novo recorde!"),
            {"sfx": "creak", "wait": 0.2},
            {"villain": "show"},
            A({"villain": "wake"}),
            S("villain", "Fresh... dough... dropped right into my kitchen.|Masa... fresca... caída justo en mi cocina.|"
              "Frischer... Teig... direkt in meine Küche gefallen.|Pâte... fraîche... tombée pile dans ma cuisine.|"
              "Pasta... fresca... caduta proprio nella mia cucina.|Massa... fresca... caiu direto na minha cozinha."),
            act(["zeek", "bup"], "scream"),
            {"villain": "lunge", "to": 1250},
            A({"shake": 0.5, "power": 16}),
            mv("zeek", 330, "run"),
            A(mv("bup", -300, "run")),
            {"villain": "hide"},
            A({"sfx": "whoosh", "wait": 0.2}),
            S("bup", "Zeek, we need to go UP. Fast!|Zeek, hay que SUBIR. ¡Rápido!|Zeek, wir müssen HOCH. Schnell!|Zeek, il faut REMONTER. Vite !|Zeek, dobbiamo SALIRE. Svelto!|Zeek, a gente tem que SUBIR. Rápido!"),
            mood("zeek", "happy"),
            mv("zeek", 700, "walk"),
            A(mv("bup", 330, "run")),
            S("zeek", "No problem. Version two. Trust—|Sin problema. Versión dos. Confíen—|Kein Problem. Version zwei. Vertraut—|"
              "Pas de souci. Version deux. Faites—|Nessun problema. Versione due. Fidatevi—|Sem problema. Versão dois. Confiem—"),
        ],
        "tail": 0.1,
    }],
}

for s in (long_, short1):
    for sc in s["scenes"]:
        sc["beats"] = flat(sc["beats"])
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"], len(s["title"]))

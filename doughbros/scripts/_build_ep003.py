"""Builds the EP3 scripts (long + 3 shorts). Run: python3 scripts/_build_ep003.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts))}


def mv(who, to, speed="walk", both=False):
    b = {"move": who, "to": to, "speed": speed}
    if both:
        b["and"] = True
    return b


def act(who, do):
    return {"act": who, "do": do}


def mood(who, is_):
    return {"mood": who, "is": is_}


ALL4 = ["bup", "pim", "zeek", "lolly"]
TAGS = ["animation", "cartoon", "dough bros", "spooky cartoon", "funny cartoon", "horror comedy",
        "animated series", "toastmaw", "evil toaster"]

long_ = {
    "id": "ep003_long",
    "format": "long",
    "title": "Dough Bros vs TOASTMAW 🍞 | Animation EP 3",
    "description": ("The ice from the freezer is melting, and now the angriest appliance in the kitchen is awake: "
                    "TOASTMAW, the old chrome toaster who shoots burning toast. Zeek builds the perfect trap... "
                    "but who will it catch? And what is Crispy hiding in the shadows?\n\n"
                    "New episodes every day. Subscribe so you don't miss who wakes up next!\n\n"
                    "#animation #cartoon #doughbros #spookycartoon #horrorcomedy"),
    "tags": TAGS + ["episode 3"],
    "thumbnail": {"bg": "oven", "villain": "toaster", "heroes": ["pim", "zeek", "bup"], "text": "YOU'RE TOAST!"},
    "scenes": [
        {   # 1. cold open
            "bg": "oven", "music": "drone",
            "heroes": {"bup": -250, "pim": -500, "zeek": -750, "lolly": -1000},
            "villain": {"type": "toaster", "x": 1450, "state": "asleep", "scale": 0.9},
            "beats": [
                {"sfx": "clank", "wait": 0.6},
                {"villain": "wake"},
                S("villain", "Who woke me up? WHO? You're TOAST!|¿Quién me despertó? ¿QUIÉN? ¡Están TOSTADOS!|"
                  "Wer hat mich geweckt? WER? Ihr seid TOAST!|Qui m'a réveillé ? QUI ? Vous êtes GRILLÉS !|"
                  "Chi mi ha svegliato? CHI? Siete TOSTATI!|Quem me acordou? QUEM? Vocês estão TORRADOS!"),
                {"sfx": "pop", "wait": 0.3},
                {"shake": 0.5, "power": 16},
                S("narr", "Last time, the heroes stole ice from the freezer.|La última vez, los héroes robaron hielo del congelador.|"
                  "Letztes Mal stahlen die Helden Eis aus dem Gefrierschrank.|La dernière fois, les héros ont volé de la glace au congélateur.|"
                  "L'ultima volta, gli eroi hanno rubato il ghiaccio dal congelatore.|Da última vez, os heróis roubaram gelo do freezer."),
                S("narr", "But the ice melts at sunrise. And now... the toaster is awake.|Pero el hielo se derrite al amanecer. Y ahora... la tostadora está despierta.|"
                  "Aber das Eis schmilzt bei Sonnenaufgang. Und jetzt... ist der Toaster wach.|Mais la glace fond à l'aube. Et maintenant... le grille-pain est réveillé.|"
                  "Ma il ghiaccio si scioglie all'alba. E ora... il tostapane è sveglio.|Mas o gelo derrete ao amanhecer. E agora... a torradeira está acordada."),
                mv("bup", 900, "run", True), mv("lolly", 660, "run", True), mv("zeek", 430, "run", True), mv("pim", 220, "run", True),
                S("pim", "W-why is it so HOT in here?|¿P-por qué hace tanto CALOR aquí?|W-warum ist es hier so HEISS?|"
                  "P-pourquoi il fait si CHAUD ici ?|P-perché fa così CALDO qui?|P-por que está tão QUENTE aqui?"),
                mood(ALL4, "scared"),
                {"villain": "roar"},
                S("villain", "Crumbs in my tray! Crumbs everywhere! I hate CRUMBS!|¡Migas en mi bandeja! ¡Migas por todas partes! ¡Odio las MIGAS!|"
                  "Krümel in meiner Schale! Überall Krümel! Ich hasse KRÜMEL!|Des miettes dans mon plateau ! Partout ! Je déteste les MIETTES !|"
                  "Briciole nel mio cassetto! Ovunque! Odio le BRICIOLE!|Migalhas na minha bandeja! Por todo lado! Eu odeio MIGALHAS!"),
                S("zeek", "Technically... we ARE made of crumbs.|Técnicamente... nosotros SOMOS de migas.|Technisch gesehen... SIND wir aus Krümeln.|"
                  "Techniquement... nous SOMMES faits de miettes.|Tecnicamente... NOI siamo fatti di briciole.|Tecnicamente... nós SOMOS feitos de migalhas."),
                {"villain": "lunge", "to": 1250},
                {"sfx": "whoosh", "wait": 0.2},
                act(ALL4, "scream"),
                mv("bup", "off_left", "run", True), mv("lolly", "off_left", "run", True),
                mv("zeek", "off_left", "run", True), mv("pim", "off_left", "run", True),
            ],
            "tail": 0.4,
        },
        {   # 2. kitchen: the plan
            "bg": "kitchen", "music": "music_box",
            "heroes": {"bup": 880, "lolly": 640, "zeek": 410, "pim": 200},
            "moods": {"pim": "scared"},
            "beats": [
                {"card": "BACK IN THE KITCHEN...", "es": "DE VUELTA EN LA COCINA...", "dur": 2.0},
                S("bup", "Okay team. We can't run from a toaster forever.|Bien, equipo. No podemos huir de una tostadora para siempre.|"
                  "Okay, Team. Wir können nicht ewig vor einem Toaster weglaufen.|Bon, l'équipe. On ne peut pas fuir un grille-pain pour toujours.|"
                  "Ok, squadra. Non possiamo scappare da un tostapane per sempre.|Certo, equipe. Não dá pra fugir de uma torradeira para sempre."),
                S("pim", "Sure we can. Watch me. I'm very good at running.|Claro que podemos. Mírenme. Soy muy bueno corriendo.|"
                  "Klar können wir. Schaut her. Ich bin super im Weglaufen.|Bien sûr qu'on peut. Regardez. Je cours très bien.|"
                  "Certo che possiamo. Guardate. Sono bravissimo a scappare.|Claro que dá. Olhem só. Eu sou ótimo em correr."),
                S("lolly", "And the ice is melting! We only have until sunrise!|¡Y el hielo se derrite! ¡Solo tenemos hasta el amanecer!|"
                  "Und das Eis schmilzt! Wir haben nur bis Sonnenaufgang!|Et la glace fond ! On n'a que jusqu'à l'aube !|"
                  "E il ghiaccio si scioglie! Abbiamo solo fino all'alba!|E o gelo está derretendo! Só temos até o amanhecer!"),
                mood("zeek", "happy"),
                act("zeek", "jump"),
                S("zeek", "Fear not! I have built... the Crumb-Catcher 3000!|¡No teman! He construido... ¡el Atrapamigas 3000!|"
                  "Keine Angst! Ich habe gebaut... den Krümelfänger 3000!|N'ayez crainte ! J'ai construit... l'Attrape-Miettes 3000 !|"
                  "Niente paura! Ho costruito... l'Acchiappabriciole 3000!|Não temam! Eu construí... o Pega-Migalhas 3000!"),
                S("zeek", "A cookie for bait. A bread bag. A spring. SNAP!|Una galleta de cebo. Una bolsa de pan. Un resorte. ¡ZAS!|"
                  "Ein Keks als Köder. Eine Brottüte. Eine Feder. SCHNAPP!|Un biscuit comme appât. Un sac à pain. Un ressort. CLAC !|"
                  "Un biscotto come esca. Un sacchetto del pane. Una molla. SNAP!|Um biscoito de isca. Um saco de pão. Uma mola. PLAFT!"),
                S("lolly", "Does it work?|¿Funciona?|Funktioniert sie?|Ça marche ?|Funziona?|Funciona?"),
                S("zeek", "In theory, yes. In practice... we will find out.|En teoría, sí. En la práctica... ya veremos.|"
                  "Theoretisch ja. Praktisch... werden wir sehen.|En théorie, oui. En pratique... on verra.|"
                  "In teoria, sì. In pratica... lo scopriremo.|Na teoria, sim. Na prática... vamos descobrir."),
                {"sfx": "clank", "wait": 0.4},
                S("bup", "I like it. Simple. Who's the bait?|Me gusta. Simple. ¿Quién es el cebo?|Gefällt mir. Einfach. Wer ist der Köder?|"
                  "J'aime bien. Simple. Qui sert d'appât ?|Mi piace. Semplice. Chi fa l'esca?|Gostei. Simples. Quem é a isca?"),
                {"wait": 0.5},
                mood(["bup", "lolly", "zeek"], "happy"),
                S("lolly", "Pim is the smallest... and the fastest runner!|¡Pim es el más pequeño... y el que corre más rápido!|"
                  "Pim ist der Kleinste... und der schnellste Läufer!|Pim est le plus petit... et le plus rapide !|"
                  "Pim è il più piccolo... e il più veloce!|O Pim é o menor... e o que corre mais rápido!"),
                act("pim", "shake"),
                S("pim", "I take it back. I'm terrible at running. The worst!|Lo retiro. Soy pésimo corriendo. ¡El peor!|"
                  "Ich nehm's zurück. Ich bin schrecklich im Rennen. Der Schlechteste!|Je retire tout. Je cours très mal. Le pire !|"
                  "Ritiro tutto. Sono pessimo a correre. Il peggiore!|Retiro o que eu disse. Sou péssimo correndo. O pior!"),
                act("pim", "faint"),
                S("zeek", "He agrees. Wonderful.|Está de acuerdo. Maravilloso.|Er ist einverstanden. Wunderbar.|"
                  "Il est d'accord. Merveilleux.|È d'accordo. Meraviglioso.|Ele concorda. Maravilha."),
            ],
            "tail": 0.6,
        },
        {   # 3. pantry: the trap
            "bg": "pantry", "music": "heartbeat",
            "heroes": {"pim": 820, "bup": 520, "zeek": 250, "lolly": -300},
            "moods": {"pim": "scared"},
            "villain": {"type": "toaster", "x": 1500, "state": "hidden", "scale": 0.85},
            "beats": [
                S("narr", "The pantry. Midnight. The trap is ready.|La despensa. Medianoche. La trampa está lista.|"
                  "Die Speisekammer. Mitternacht. Die Falle ist bereit.|Le garde-manger. Minuit. Le piège est prêt.|"
                  "La dispensa. Mezzanotte. La trappola è pronta.|A despensa. Meia-noite. A armadilha está pronta."),
                S("pim", "H-here, toasty toaster! Yummy cookie! Please don't eat me!|¡A-aquí, tostadorcita! ¡Galleta rica! ¡Por favor no me comas!|"
                  "H-hier, lieber Toaster! Leckerer Keks! Bitte friss mich nicht!|I-ici, gentil grille-pain ! Bon biscuit ! Ne me mange pas !|"
                  "Q-qui, tostapane carino! Biscotto buono! Non mangiarmi, ti prego!|A-aqui, torradeira fofinha! Biscoito gostoso! Por favor, não me come!"),
                S("bup", "Everyone hide behind the flour. Pim, don't move.|Todos detrás de la harina. Pim, no te muevas.|"
                  "Alle hinter das Mehl. Pim, beweg dich nicht.|Tout le monde derrière la farine. Pim, ne bouge pas.|"
                  "Tutti dietro la farina. Pim, non muoverti.|Todo mundo atrás da farinha. Pim, não se mexe."),
                S("lolly", "You're doing great, Pim! So brave!|¡Lo haces genial, Pim! ¡Qué valiente!|Du machst das super, Pim! So mutig!|"
                  "Tu es génial, Pim ! Si courageux !|Stai andando alla grande, Pim! Che coraggio!|Você está indo muito bem, Pim! Que coragem!"),
                S("pim", "I'm doing terrible. My legs are made of jelly.|Lo hago fatal. Mis piernas son de gelatina.|"
                  "Ich mach das schrecklich. Meine Beine sind aus Wackelpudding.|Je suis nul. Mes jambes sont en gelée.|"
                  "Sto andando malissimo. Ho le gambe di gelatina.|Estou indo péssimo. Minhas pernas são de gelatina."),
                {"sfx": "step", "wait": 0.4},
                {"sfx": "step", "wait": 0.4},
                {"villain": "show"},
                S("villain", "A cookie? In MY pantry? Full of CRUMBS?|¿Una galleta? ¿En MI despensa? ¿Llena de MIGAS?|"
                  "Ein Keks? In MEINER Kammer? Voller KRÜMEL?|Un biscuit ? Dans MON garde-manger ? Plein de MIETTES ?|"
                  "Un biscotto? Nella MIA dispensa? Pieno di BRICIOLE?|Um biscoito? Na MINHA despensa? Cheio de MIGALHAS?"),
                {"villain": "rage", "level": 0.6},
                S("zeek", "Steady... steady... wait for it...|Quietos... quietos... esperen...|Ruhig... ruhig... wartet...|"
                  "Doucement... doucement... attendez...|Fermi... fermi... aspettate...|Calma... calma... esperem..."),
                mv("bup", 620, "walk"),
                S("bup", "Zeek, which button is the trap?|Zeek, ¿qué botón es la trampa?|Zeek, welcher Knopf ist die Falle?|"
                  "Zeek, quel bouton déclenche le piège ?|Zeek, quale pulsante fa scattare la trappola?|Zeek, qual botão é a armadilha?"),
                S("zeek", "The red one. Don't step on the red one!|El rojo. ¡No pises el rojo!|Der rote. Tritt nicht auf den roten!|"
                  "Le rouge. Ne marche pas sur le rouge !|Quello rosso. Non pestare quello rosso!|O vermelho. Não pise no vermelho!"),
                {"sfx": "ding", "wait": 0.3},
                {"wait": 0.4},
                S("bup", "...Was it red?|...¿Era rojo?|...War er rot?|...Il était rouge ?|...Era rosso?|...Era vermelho?"),
                {"sfx": "clank", "wait": 0.1},
                {"shake": 0.7, "power": 22},
                act(["bup", "zeek", "pim"], "scream"),
                mood(["bup", "zeek", "pim"], "scared"),
                S("narr", "The trap worked perfectly. On the wrong team.|La trampa funcionó perfecto. Con el equipo equivocado.|"
                  "Die Falle funktionierte perfekt. Beim falschen Team.|Le piège a parfaitement marché. Sur la mauvaise équipe.|"
                  "La trappola ha funzionato benissimo. Sulla squadra sbagliata.|A armadilha funcionou perfeitamente. No time errado."),
                {"villain": "rage", "level": 1.0},
                S("villain", "Three crumbs in a bag. How convenient. You're TOAST!|Tres migas en una bolsa. Qué práctico. ¡Están TOSTADOS!|"
                  "Drei Krümel in einer Tüte. Wie praktisch. Ihr seid TOAST!|Trois miettes dans un sac. Pratique. Vous êtes GRILLÉS !|"
                  "Tre briciole in un sacchetto. Che comodo. Siete TOSTATI!|Três migalhas num saco. Que prático. Vocês estão TORRADOS!"),
                {"villain": "lunge", "to": 1150},
            ],
            "tail": 0.3,
        },
        {   # 4. Lolly snaps, Crispy appears
            "bg": "pantry", "music": "drone",
            "heroes": {"pim": 860, "bup": 620, "zeek": 200, "lolly": -300, "crispy": 2200},
            "moods": {"pim": "scared", "bup": "scared", "zeek": "scared"},
            "villain": {"type": "toaster", "x": 1150, "state": "awake", "scale": 0.85},
            "beats": [
                mv("lolly", 410, "run"),
                S("lolly", "Excuse me, Mister Toaster. Could you please let my friends go?|Disculpe, señor Tostadora. ¿Podría soltar a mis amigos, por favor?|"
                  "Entschuldigung, Herr Toaster. Würden Sie bitte meine Freunde freilassen?|Excusez-moi, Monsieur Grille-pain. Pourriez-vous libérer mes amis ?|"
                  "Mi scusi, signor Tostapane. Potrebbe liberare i miei amici, per favore?|Com licença, senhor Torradeira. Pode soltar meus amigos, por favor?"),
                S("villain", "No. Go away, sprinkle face.|No. Vete, cara de chispitas.|Nein. Hau ab, Streuselgesicht.|"
                  "Non. Va-t'en, tête de vermicelles.|No. Vattene, faccia di zuccherini.|Não. Vai embora, cara de granulado."),
                {"wait": 0.6},
                mood("lolly", "angry"),
                {"shake": 0.4, "power": 10},
                S("lolly", "What. Did. You. Call. ME?!|¿Cómo. Me. Llamaste. A. MÍ?!|Wie. Hast. Du. MICH. Genannt?!|"
                  "Comment. Tu. M'as. Appelée ?!|Come. Mi. Hai. Chiamata?!|Do. Que. Você. Me. Chamou?!"),
                act("lolly", "jump"),
                {"villain": "rage", "level": 0.2},
                S("villain", "Nobody yells at ME! I'm... I'm a very scary toaster!|¡Nadie me grita a MÍ! Soy... ¡soy una tostadora muy temible!|"
                  "Niemand schreit MICH an! Ich bin... ein sehr gruseliger Toaster!|Personne ne crie sur MOI ! Je suis... un grille-pain très effrayant !|"
                  "Nessuno urla a ME! Io sono... un tostapane molto spaventoso!|Ninguém grita COMIGO! Eu sou... uma torradeira muito assustadora!"),
                mv("villain", 1350, "walk"),
                {"sfx": "creak", "wait": 0.5},
                mv("crispy", 1070, "walk"),
                S("crispy", "Toasters fear only one thing. A full crumb tray.|Las tostadoras solo temen una cosa. Una bandeja llena de migas.|"
                  "Toaster fürchten nur eins. Eine volle Krümelschale.|Les grille-pains ne craignent qu'une chose. Un plateau plein de miettes.|"
                  "I tostapane temono una sola cosa. Un cassetto pieno di briciole.|Torradeiras só temem uma coisa. Uma bandeja cheia de migalhas."),
                S("pim", "C-Crispy! Where did you come from?!|¡C-Crispy! ¿¡De dónde saliste!?|K-Crispy! Wo kommst du denn her?!|"
                  "C-Crispy ! D'où tu sors ?!|C-Crispy! Da dove sei sbucato?!|C-Crispy! De onde você saiu?!"),
                S("crispy", "The shadows. Always the shadows.|De las sombras. Siempre de las sombras.|Aus den Schatten. Immer aus den Schatten.|"
                  "Des ombres. Toujours des ombres.|Dalle ombre. Sempre dalle ombre.|Das sombras. Sempre das sombras."),
                {"sfx": "rattle", "wait": 0.6},
                S("narr", "Crispy shook the bread bag. A thousand crumbs fell out.|Crispy sacudió la bolsa de pan. Cayeron mil migas.|"
                  "Crispy schüttelte die Brottüte. Tausend Krümel fielen heraus.|Crispy secoua le sac à pain. Mille miettes tombèrent.|"
                  "Crispy scosse il sacchetto del pane. Caddero mille briciole.|Crispy sacudiu o saco de pão. Mil migalhas caíram."),
                {"villain": "rage", "level": 1.0},
                S("villain", "CRUMBS! On my floor! I must... clean... everything!|¡MIGAS! ¡En mi suelo! Debo... limpiar... ¡todo!|"
                  "KRÜMEL! Auf meinem Boden! Ich muss... alles... putzen!|DES MIETTES ! Sur mon sol ! Je dois... tout... nettoyer !|"
                  "BRICIOLE! Sul mio pavimento! Devo... pulire... tutto!|MIGALHAS! No meu chão! Preciso... limpar... tudo!"),
                mv("villain", "off_right", "run"),
                mood(["bup", "pim", "zeek"], "happy"),
                act(["bup", "pim", "zeek"], "bounce"),
            ],
            "tail": 0.5,
        },
        {   # 5. twist + cliffhanger
            "bg": "kitchen", "music": "drone",
            "heroes": {"bup": 880, "lolly": 660, "zeek": 440, "pim": 230, "crispy": 1120},
            "villain": {"type": "mixer", "x": 1500, "state": "hidden", "scale": 0.8},
            "beats": [
                S("bup", "Crispy, thanks. You saved us. Again.|Crispy, gracias. Nos salvaste. Otra vez.|Crispy, danke. Du hast uns gerettet. Schon wieder.|"
                  "Crispy, merci. Tu nous as sauvés. Encore.|Crispy, grazie. Ci hai salvati. Di nuovo.|Crispy, valeu. Você nos salvou. De novo."),
                S("zeek", "Note to self: make the trap button... not red.|Nota mental: que el botón de la trampa... no sea rojo.|"
                  "Notiz an mich: der Fallenknopf... nicht rot.|Note pour moi : le bouton du piège... pas rouge.|"
                  "Nota per me: il pulsante della trappola... non rosso.|Lembrete: o botão da armadilha... não vermelho."),
                S("pim", "Great. Can we go home now?|Genial. ¿Ya podemos ir a casa?|Super. Können wir jetzt nach Hause?|"
                  "Super. On peut rentrer maintenant ?|Bene. Possiamo tornare a casa adesso?|Ótimo. Podemos ir pra casa agora?"),
                S("bup", "Pim... this IS home.|Pim... esta ES nuestra casa.|Pim... das IST unser Zuhause.|"
                  "Pim... c'EST notre maison.|Pim... questa È casa nostra.|Pim... aqui É a nossa casa."),
                S("lolly", "And the ice? Zeek, how much is left?|¿Y el hielo? Zeek, ¿cuánto queda?|Und das Eis? Zeek, wie viel ist noch übrig?|"
                  "Et la glace ? Zeek, il en reste combien ?|E il ghiaccio? Zeek, quanto ne resta?|E o gelo? Zeek, quanto sobrou?"),
                S("zeek", "One cube. Melting. My calculations say... five hours.|Un cubo. Derritiéndose. Mis cálculos dicen... cinco horas.|"
                  "Ein Würfel. Er schmilzt. Meine Berechnungen sagen... fünf Stunden.|Un glaçon. Il fond. Mes calculs disent... cinq heures.|"
                  "Un cubetto. Si sta sciogliendo. I miei calcoli dicono... cinque ore.|Um cubo. Derretendo. Meus cálculos dizem... cinco horas."),
                S("crispy", "Toastmaw wasn't hunting you. He was hunting for Mr. Pot.|Toastmaw no los cazaba. Cazaba para el Señor Olla.|"
                  "Toastmaw jagte nicht euch. Er jagte für Herrn Topf.|Toastmaw ne vous chassait pas. Il chassait pour Monsieur Marmite.|"
                  "Toastmaw non dava la caccia a voi. Cacciava per il Signor Pentola.|O Toastmaw não caçava vocês. Caçava para o Senhor Panela."),
                mood(ALL4, "scared"),
                S("lolly", "Mr. Pot is collecting appliances... like an army!|El Señor Olla está reuniendo aparatos... ¡como un ejército!|"
                  "Herr Topf sammelt Geräte... wie eine Armee!|Monsieur Marmite rassemble des appareils... comme une armée !|"
                  "Il Signor Pentola sta radunando elettrodomestici... come un esercito!|O Senhor Panela está juntando aparelhos... como um exército!"),
                S("crispy", "And the next one... is already here.|Y el siguiente... ya está aquí.|Und der Nächste... ist schon hier.|"
                  "Et le suivant... est déjà là.|E il prossimo... è già qui.|E o próximo... já está aqui."),
                {"sfx": "whoosh", "wait": 0.4},
                {"villain": "show"},
                {"villain": "wake"},
                S("villain", "Hee hee hee! Let's MIX it up!|¡Ji ji ji! ¡Vamos a MEZCLARLO todo!|Hihihi! Lasst uns alles VERMIXEN!|"
                  "Hi hi hi ! On va tout MÉLANGER !|Ih ih ih! MESCOLIAMO tutto!|Hi hi hi! Vamos MISTURAR tudo!"),
                act(ALL4, "scream"),
                {"shake": 0.8, "power": 20},
                act("pim", "faint"),
                S("villain", "Mr. Pot says hello! Spin, spin, SPIN!|¡El Señor Olla les manda saludos! ¡Gira, gira, GIRA!|"
                  "Herr Topf lässt grüßen! Dreh, dreh, DREH!|Monsieur Marmite vous salue ! Tourne, tourne, TOURNE !|"
                  "Il Signor Pentola vi saluta! Gira, gira, GIRA!|O Senhor Panela mandou um oi! Gira, gira, GIRA!"),
            ],
            "tail": 0.8,
        },
    ],
}

short1 = {  # funny character moment: Lolly
    "id": "ep003_short1", "format": "short",
    "title": "Never make Lolly ANGRY 😡 #shorts",
    "hook": "Lolly is SO sweet...",
    "description": "Lolly is the sweetest cookie in Table Land. Until someone calls her a name. #shorts #animation #cartoon #doughbros #funny",
    "tags": ["shorts"] + TAGS[:7] + ["lolly"],
    "thumbnail": {"bg": "pantry", "villain": "toaster", "heroes": ["lolly"], "text": "SHE SNAPPED!"},
    "scenes": [{
        "bg": "pantry", "music": "music_box",
        "heroes": {"lolly": 520},
        "villain": {"type": "toaster", "x": 1400, "state": "awake", "scale": 0.8},
        "beats": [
            S("lolly", "Excuse me, Mister Toaster. Could you please be a little quieter?|Disculpe, señor Tostadora. ¿Podría hacer menos ruido, por favor?|"
              "Entschuldigung, Herr Toaster. Könnten Sie bitte etwas leiser sein?|Excusez-moi, Monsieur Grille-pain. Pourriez-vous faire moins de bruit ?|"
              "Mi scusi, signor Tostapane. Potrebbe fare un po' meno rumore?|Com licença, senhor Torradeira. Pode fazer menos barulho, por favor?"),
            S("villain", "No. Go away, sprinkle face.|No. Vete, cara de chispitas.|Nein. Hau ab, Streuselgesicht.|"
              "Non. Va-t'en, tête de vermicelles.|No. Vattene, faccia di zuccherini.|Não. Vai embora, cara de granulado."),
            {"wait": 0.7},
            mood("lolly", "angry"),
            {"shake": 0.5, "power": 14},
            S("lolly", "SPRINKLE. FACE?!|¿¡CARA. DE. CHISPITAS!?|STREUSEL. GESICHT?!|TÊTE. DE. VERMICELLES ?!|FACCIA. DI. ZUCCHERINI?!|CARA. DE. GRANULADO?!"),
            act("lolly", "jump"),
            {"villain": "sleep"},
            S("villain", "...I'm asleep. I was always asleep.|...Estoy dormida. Siempre estuve dormida.|...Ich schlafe. Ich hab immer geschlafen.|"
              "...Je dors. J'ai toujours dormi.|...Sto dormendo. Ho sempre dormito.|...Estou dormindo. Sempre estive dormindo."),
            mood("lolly", "happy"),
            S("lolly", "Thank you SO much! Sweet dreams!|¡Muchísimas gracias! ¡Dulces sueños!|Vielen DANK! Süße Träume!|"
              "Merci BEAUCOUP ! Fais de beaux rêves !|Grazie MILLE! Sogni d'oro!|Muito OBRIGADA! Bons sonhos!"),
        ],
        "tail": 0.8,
    }],
}

short2 = {  # question
    "id": "ep003_short2", "format": "short",
    "title": "Would YOU touch the toaster? 🍞 #shorts",
    "hook": "Pim's biggest dare...",
    "description": "Bup dares Pim to touch Toastmaw. Would YOU do it? Comment YES or NO! #shorts #animation #cartoon #doughbros #dare",
    "tags": ["shorts"] + TAGS[:7] + ["dare", "would you rather"],
    "thumbnail": {"bg": "oven", "villain": "toaster", "heroes": ["pim", "bup"], "text": "TOUCH IT?"},
    "scenes": [{
        "bg": "oven", "music": "heartbeat",
        "heroes": {"bup": 360, "pim": 620},
        "moods": {"pim": "scared"},
        "villain": {"type": "toaster", "x": 1400, "state": "asleep", "scale": 0.8},
        "beats": [
            S("bup", "I dare you. Touch the toaster. Just one poke.|Te reto. Toca la tostadora. Solo un toque.|Ich wette, du traust dich nicht. Ein Stups.|"
              "Je te défie. Touche le grille-pain. Juste un doigt.|Ti sfido. Tocca il tostapane. Solo un colpetto.|Te desafio. Toca na torradeira. Só uma cutucada."),
            S("pim", "Okay. I'm brave. I'm very brave. Here I go...|Bueno. Soy valiente. Muy valiente. Allá voy...|Okay. Ich bin mutig. Sehr mutig. Los geht's...|"
              "D'accord. Je suis brave. Très brave. J'y vais...|Ok. Sono coraggioso. Molto coraggioso. Vado...|Tá. Sou corajoso. Muito corajoso. Lá vou eu..."),
            mv("pim", 1100, "walk"),
            {"sfx": "ding", "wait": 0.3},
            {"villain": "wake"},
            S("villain", "You're TOAST!|¡Estás TOSTADO!|Du bist TOAST!|Tu es GRILLÉ !|Sei TOSTATO!|Você está TORRADO!"),
            act(["pim", "bup"], "scream"),
            mv("pim", "off_left", "run"),
            S("narr", "Would YOU touch the toaster? Comment YES or NO!|¿TÚ tocarías la tostadora? ¡Comenta SÍ o NO!|"
              "Würdest DU den Toaster anfassen? Schreib JA oder NEIN!|Et TOI, tu toucherais le grille-pain ? Écris OUI ou NON !|"
              "TU toccheresti il tostapane? Scrivi SÌ o NO!|VOCÊ tocaria na torradeira? Comente SIM ou NÃO!"),
        ],
        "tail": 1.0,
    }],
}

short3 = {  # teaser
    "id": "ep003_short3", "format": "short",
    "title": "The trap caught the WRONG team 😱 #shorts",
    "hook": "The perfect trap...",
    "description": "Zeek's Crumb-Catcher 3000 works perfectly. On the wrong team. Full episode on the channel! #shorts #animation #cartoon #doughbros",
    "tags": ["shorts"] + TAGS + ["trap"],
    "thumbnail": {"bg": "pantry", "villain": "toaster", "heroes": ["bup", "zeek"], "text": "IT'S A TRAP!"},
    "scenes": [{
        "bg": "pantry", "music": "heartbeat",
        "heroes": {"zeek": 300, "bup": 640},
        "villain": {"type": "toaster", "x": 1400, "state": "awake", "scale": 0.8},
        "beats": [
            S("narr", "Zeek built the perfect toaster trap...|Zeek construyó la trampa perfecta...|Zeek baute die perfekte Toasterfalle...|"
              "Zeek a construit le piège parfait...|Zeek ha costruito la trappola perfetta...|Zeek construiu a armadilha perfeita..."),
            S("zeek", "Don't step on the red button!|¡No pises el botón rojo!|Tritt nicht auf den roten Knopf!|"
              "Ne marche pas sur le bouton rouge !|Non pestare il pulsante rosso!|Não pise no botão vermelho!"),
            {"sfx": "ding", "wait": 0.4},
            S("bup", "...Was it red?|...¿Era rojo?|...War er rot?|...Il était rouge ?|...Era rosso?|...Era vermelho?"),
            {"sfx": "clank", "wait": 0.1},
            {"shake": 0.7, "power": 22},
            act(["bup", "zeek"], "scream"),
            mood(["bup", "zeek"], "scared"),
            {"villain": "rage", "level": 1.0},
            S("villain", "Two crumbs in a bag. You're TOAST!|Dos migas en una bolsa. ¡Están TOSTADOS!|Zwei Krümel in einer Tüte. Ihr seid TOAST!|"
              "Deux miettes dans un sac. Vous êtes GRILLÉS !|Due briciole in un sacchetto. Siete TOSTATI!|Duas migalhas num saco. Vocês estão TORRADOS!"),
            {"villain": "lunge", "to": 1100},
            S("narr", "Full episode on the channel!|¡Episodio completo en el canal!|Ganze Folge auf dem Kanal!|"
              "Épisode complet sur la chaîne !|Episodio completo sul canale!|Episódio completo no canal!"),
        ],
        "tail": 0.8,
    }],
}

for s in (long_, short1, short2, short3):
    (OUT / f"{s['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", s["id"])

"""Builds Hollowmere EP2 (true story: the Flannan Isles lighthouse keepers, 1900). Run: python3 scripts/_build_ep002.py"""
import json, pathlib

OUT = pathlib.Path(__file__).parent
LANGS = ["en", "es", "de", "fr", "it", "pt"]


def S(who, text, **kw):
    parts = [p.strip() for p in text.split("|")]
    assert len(parts) == 6, (who, text)
    return {"say": who, **dict(zip(LANGS, parts)), **kw}


TAGS = ["true story", "unsolved mystery", "real horror story", "Flannan Isles", "Eilean Mor", "lighthouse mystery",
        "Scotland", "horror animation", "scary stories", "hollowmere"]
SOURCES = ["https://en.wikipedia.org/wiki/Flannan_Isles_Lighthouse",
           "https://nrscotland.gov.uk/learning-and-events/for-the-safety-of-all-scotlands-lighthouses/the-flannan-islands-lighthouse-a-disappearance/",
           "https://www.history.co.uk/articles/the-flannan-isle-mystery-the-three-lighthouse-keepers-who-vanished"]

long_ = {
    "id": "ep002_long", "format": "long",
    "title": "The Lighthouse Keepers Who Vanished | True Story | Hollowmere Tales EP 2",
    "description": ("A true story. In December 1900, the new lighthouse on Eilean Mor in Scotland's Flannan Isles went dark. "
                    "When the relief boat finally arrived, the three keepers, James Ducat, Thomas Marshall and Donald McArthur, were gone. "
                    "The lamps were ready, the clock had stopped, one set of oilskins still hung inside... and they were never found.\n\n"
                    "Told from the official records, with the later legends clearly marked.\n\n"
                    "Sources:\n" + "\n".join(SOURCES) + "\n\n#truestory #unsolvedmystery #horror #animation #hollowmere"),
    "tags": TAGS + ["episode 2", "vanished", "Hebrides"],
    "thumbnail": {"bg": "lighthouse", "seed": 2, "creature": "ghost", "text": "THEY VANISHED"},
    "shots": [
        {   # 1 cold open: the dark light
            "bg": "lighthouse", "seed": 2, "music": "drone", "wind": True, "eyes": 0, "lantern": 0.0, "ambient": 0.36,
            "cam": {"from": [960, 560, 1.0], "to": [960, 590, 1.16]},
            "creatures": {"archtor": {"type": "ship", "x": 1500, "y": 680, "scale": 0.5, "state": "hidden"}},
            "beats": [
                {"sfx": "creak", "wait": 1.0},
                S("narr", "This is a true story, taken from the records of Scotland.|Esta es una historia real, tomada de los archivos de Escocia.|"
                  "Dies ist eine wahre Geschichte aus den Akten Schottlands.|Ceci est une histoire vraie, tirée des archives de l'Écosse.|"
                  "Questa è una storia vera, presa dagli archivi della Scozia.|Esta é uma história real, tirada dos registros da Escócia."),
                {"show": "archtor", "dur": 1.5},
                S("narr", "On the fifteenth of December 1900, a steamer called the Archtor passed the Flannan Isles.|El quince de diciembre de 1900, un vapor llamado Archtor pasó junto a las islas Flannan.|"
                  "Am fünfzehnten Dezember 1900 fuhr ein Dampfer namens Archtor an den Flannan-Inseln vorbei.|Le quinze décembre 1900, un vapeur nommé l'Archtor passa près des îles Flannan.|"
                  "Il quindici dicembre 1900, un piroscafo chiamato Archtor passò accanto alle isole Flannan.|Em quinze de dezembro de 1900, um vapor chamado Archtor passou pelas ilhas Flannan."),
                S("narr", "The weather was bad. And her crew noticed the new lighthouse was dark.|El tiempo era malo. Y su tripulación notó que el faro nuevo estaba apagado.|"
                  "Das Wetter war schlecht. Und die Mannschaft bemerkte: Der neue Leuchtturm war dunkel.|Le temps était mauvais. Et l'équipage remarqua que le nouveau phare était éteint.|"
                  "Il tempo era brutto. E l'equipaggio notò che il faro nuovo era spento.|O tempo estava ruim. E a tripulação notou que o farol novo estava apagado."),
                {"move": "archtor", "to": "off_right", "speed": "walk"},
                {"wait": 0.6},
                {"card": "THE KEEPERS WHO VANISHED", "dur": 2.8},
            ],
            "tail": 0.2,
        },
        {   # 2 the island and the three keepers
            "bg": "lighthouse", "seed": 3, "music": "lullaby", "wind": True, "eyes": 0, "ambient": 0.44,
            "lights": [{"kind": "moon", "x": 1450, "y": 220, "r": 900}],
            "cam": {"from": [900, 600, 1.12], "to": [820, 620, 1.2]},
            "chars": {"odo": {"x": -150}, "moth": {"x": -60, "y": 650}},
            "beats": [
                {"move": "odo", "to": 540, "speed": "walk"},
                {"move": "moth", "to": 700, "speed": "walk", "and": True},
                S("narr", "The lighthouse on Eilean Mor was barely a year old.|El faro de Eilean Mor apenas tenía un año.|"
                  "Der Leuchtturm auf Eilean Mor war kaum ein Jahr alt.|Le phare d'Eilean Mor avait à peine un an.|"
                  "Il faro di Eilean Mor aveva appena un anno.|O farol de Eilean Mor tinha apenas um ano."),
                S("narr", "Three keepers lived on the island: James Ducat, Thomas Marshall, and Donald McArthur.|Tres fareros vivían en la isla: James Ducat, Thomas Marshall y Donald McArthur.|"
                  "Drei Wärter lebten auf der Insel: James Ducat, Thomas Marshall und Donald McArthur.|Trois gardiens vivaient sur l'île : James Ducat, Thomas Marshall et Donald McArthur.|"
                  "Tre guardiani vivevano sull'isola: James Ducat, Thomas Marshall e Donald McArthur.|Três faroleiros viviam na ilha: James Ducat, Thomas Marshall e Donald McArthur."),
                S("narr", "A fourth keeper, Joseph Moore, was waiting on shore for his turn.|Un cuarto farero, Joseph Moore, esperaba su turno en tierra.|"
                  "Ein vierter Wärter, Joseph Moore, wartete an Land auf seine Schicht.|Un quatrième gardien, Joseph Moore, attendait son tour à terre.|"
                  "Un quarto guardiano, Joseph Moore, aspettava il suo turno a terra.|Um quarto faroleiro, Joseph Moore, esperava sua vez em terra."),
                S("odo", "Three men alone, out here in the middle of the sea?|¿Tres hombres solos, aquí en medio del mar?|Drei Männer allein, hier mitten im Meer?|"
                  "Trois hommes seuls, ici au milieu de la mer ?|Tre uomini soli, qui in mezzo al mare?|Três homens sozinhos, aqui no meio do mar?"),
                S("moth", "Someone had to keep the light burning, Odo. Just like you.|Alguien tenía que mantener la luz encendida, Odo. Como tú.|"
                  "Jemand musste das Licht am Brennen halten, Odo. Genau wie du.|Il fallait bien que quelqu'un garde la lumière allumée, Odo. Comme toi.|"
                  "Qualcuno doveva tenere accesa la luce, Odo. Proprio come te.|Alguém precisava manter a luz acesa, Odo. Igual a você."),
                {"sfx": "caw", "wait": 0.6},
                S("narr", "But that December, the light on Eilean Mor stayed dark.|Pero aquel diciembre, la luz de Eilean Mor siguió apagada.|"
                  "Doch in jenem Dezember blieb das Licht auf Eilean Mor dunkel.|Mais ce décembre-là, la lumière d'Eilean Mor resta éteinte.|"
                  "Ma quel dicembre, la luce di Eilean Mor rimase spenta.|Mas naquele dezembro, a luz de Eilean Mor continuou apagada."),
            ],
            "tail": 0.3,
        },
        {   # 3 the Hesperus arrives
            "bg": "sea", "seed": 4, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
            "cam": {"from": [960, 600, 1.1], "to": [1040, 610, 1.2]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "beats": [
                S("narr", "Storms kept the relief boat, the Hesperus, stuck in harbour for days.|Las tormentas dejaron al barco de relevo, el Hesperus, atrapado en puerto durante días.|"
                  "Stürme hielten das Versorgungsschiff Hesperus tagelang im Hafen fest.|Les tempêtes retinrent le bateau de relève, l'Hesperus, au port pendant des jours.|"
                  "Le tempeste tennero la nave di soccorso, la Hesperus, bloccata in porto per giorni.|As tempestades prenderam o barco de troca, o Hesperus, no porto por dias."),
                {"shake": 0.6, "power": 8},
                S("narr", "She finally reached the island at noon on the twenty-sixth of December.|Por fin llegó a la isla al mediodía del veintiséis de diciembre.|"
                  "Erst am sechsundzwanzigsten Dezember, mittags, erreichte sie die Insel.|Il atteignit enfin l'île à midi, le vingt-six décembre.|"
                  "Raggiunse finalmente l'isola a mezzogiorno del ventisei dicembre.|Ele finalmente chegou à ilha ao meio-dia de vinte e seis de dezembro."),
                S("narr", "No flag flew on the pole. Nobody came down to the landing.|Ninguna bandera ondeaba en el mástil. Nadie bajó al embarcadero.|"
                  "Keine Flagge wehte am Mast. Niemand kam zur Anlegestelle herunter.|Aucun drapeau ne flottait au mât. Personne ne descendit au débarcadère.|"
                  "Nessuna bandiera sventolava sul pennone. Nessuno scese all'approdo.|Nenhuma bandeira no mastro. Ninguém desceu até o cais."),
                {"sfx": "whoosh", "wait": 0.4},
                {"flash": True},
                S("narr", "The captain blew the ship's whistle and fired a flare.|El capitán hizo sonar la sirena y disparó una bengala.|"
                  "Der Kapitän ließ die Pfeife ertönen und schoss eine Leuchtrakete ab.|Le capitaine fit siffler le navire et tira une fusée éclairante.|"
                  "Il capitano suonò la sirena e sparò un razzo di segnalazione.|O capitão tocou o apito do navio e disparou um sinalizador."),
                {"wait": 1.2},
                S("narr", "Nothing answered.|Nada respondió.|Nichts antwortete.|Rien ne répondit.|Nulla rispose.|Nada respondeu."),
                {"act": "odo", "do": "scared"},
                S("odo", "Maybe they just didn't hear it...|Quizá simplemente no lo oyeron...|Vielleicht haben sie es nur nicht gehört...|"
                  "Peut-être qu'ils ne l'ont pas entendu...|Forse non l'hanno sentito...|Talvez eles só não tenham ouvido..."),
                S("moth", "On an island that small? They heard. Or they weren't there.|¿En una isla tan pequeña? Lo oyeron. O no estaban allí.|"
                  "Auf so einer kleinen Insel? Sie haben es gehört. Oder sie waren nicht da.|Sur une île si petite ? Ils ont entendu. Ou ils n'étaient plus là.|"
                  "Su un'isola così piccola? L'hanno sentito. Oppure non c'erano.|Numa ilha tão pequena? Eles ouviram. Ou não estavam lá."),
            ],
            "tail": 0.3,
        },
        {   # 4 Joseph Moore climbs up
            "bg": "lighthouse", "seed": 5, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.40,
            "cam": {"from": [960, 600, 1.12], "to": [1100, 600, 1.22]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 660, "y": 650}},
            "creatures": {"moore": {"type": "figure", "x": 1700, "seed": 1, "face": 1, "state": "hidden"},
                          "c1": {"type": "crow", "x": 1350, "y": 420, "fly": 1, "state": "hidden"}},
            "beats": [
                {"show": "moore", "dur": 1.0},
                S("narr", "Joseph Moore, the relief keeper, climbed up to the lighthouse.|Joseph Moore, el farero de relevo, subió hasta el faro.|"
                  "Joseph Moore, der Ablösewärter, stieg zum Leuchtturm hinauf.|Joseph Moore, le gardien de relève, monta jusqu'au phare.|"
                  "Joseph Moore, il guardiano di cambio, salì fino al faro.|Joseph Moore, o faroleiro de troca, subiu até o farol."),
                {"move": "moore", "to": 1350, "speed": "walk"},
                S("narr", "The entrance gate was closed. The main door was closed.|La verja de entrada estaba cerrada. La puerta principal, también.|"
                  "Das Eingangstor war geschlossen. Die Haupttür war geschlossen.|Le portail était fermé. La porte principale était fermée.|"
                  "Il cancello era chiuso. La porta principale era chiusa.|O portão estava fechado. A porta principal estava fechada."),
                {"sfx": "creak", "wait": 0.8},
                S("narr", "Inside, the beds were unmade, and the clock had stopped.|Dentro, las camas estaban deshechas y el reloj se había parado.|"
                  "Drinnen waren die Betten ungemacht, und die Uhr war stehen geblieben.|À l'intérieur, les lits étaient défaits et l'horloge s'était arrêtée.|"
                  "Dentro, i letti erano disfatti e l'orologio si era fermato.|Lá dentro, as camas estavam desfeitas e o relógio tinha parado."),
                S("narr", "Yet the lamps were cleaned and refilled, ready for another night.|Pero las lámparas estaban limpias y llenas, listas para otra noche.|"
                  "Doch die Lampen waren geputzt und nachgefüllt, bereit für eine weitere Nacht.|Pourtant, les lampes étaient nettoyées et remplies, prêtes pour une autre nuit.|"
                  "Eppure le lampade erano pulite e riempite, pronte per un'altra notte.|Mas as lâmpadas estavam limpas e cheias, prontas para outra noite."),
                S("narr", "And one set of oilskins was still hanging inside.|Y un impermeable seguía colgado dentro.|"
                  "Und ein Ölzeug hing noch drinnen.|Et un ciré était encore accroché à l'intérieur.|"
                  "E un'incerata era ancora appesa dentro.|E uma capa de chuva ainda estava pendurada lá dentro."),
                S("moth", "Someone went out into a winter storm without his coat.|Alguien salió a una tormenta de invierno sin su abrigo.|"
                  "Jemand ging ohne Mantel hinaus in einen Wintersturm.|Quelqu'un est sorti dans une tempête d'hiver sans son manteau.|"
                  "Qualcuno è uscito in una tempesta d'inverno senza cappotto.|Alguém saiu numa tempestade de inverno sem o casaco."),
                S("odo", "Why would anyone do that?|¿Por qué haría alguien eso?|Warum sollte jemand so etwas tun?|Pourquoi quelqu'un ferait ça ?|Perché qualcuno dovrebbe farlo?|Por que alguém faria isso?"),
                {"show": "c1", "dur": 0.4},
                {"sfx": "caw", "and": True},
                {"move": "c1", "to": "off_left", "speed": "run"},
                S("narr", "Moore searched the whole island. The three keepers were nowhere.|Moore registró toda la isla. Los tres fareros no estaban en ninguna parte.|"
                  "Moore durchsuchte die ganze Insel. Die drei Wärter waren nirgends.|Moore fouilla toute l'île. Les trois gardiens n'étaient nulle part.|"
                  "Moore perlustrò tutta l'isola. I tre guardiani non c'erano da nessuna parte.|Moore vasculhou a ilha inteira. Os três faroleiros não estavam em lugar nenhum."),
            ],
            "tail": 0.3,
        },
        {   # 5 the west landing
            "bg": "lighthouse", "seed": 6, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.38,
            "cam": {"from": [900, 600, 1.12], "to": [1100, 620, 1.22]},
            "chars": {"odo": {"x": 560}, "moth": {"x": 720, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1450, "state": "hidden", "face": -1},
                          "g2": {"type": "ghost", "x": 1600, "state": "hidden", "face": -1, "scale": 0.9},
                          "g3": {"type": "ghost", "x": 1300, "state": "hidden", "face": -1, "scale": 0.95}},
            "beats": [
                S("narr", "At the west landing, iron railings were bent, and turf was torn from the cliff.|En el embarcadero oeste, las barandillas de hierro estaban dobladas y la hierba arrancada del acantilado.|"
                  "Am Westanleger waren Eisengeländer verbogen, und Grasnarbe war von der Klippe gerissen.|Au débarcadère ouest, les rambardes de fer étaient tordues, l'herbe arrachée de la falaise.|"
                  "All'approdo ovest, le ringhiere di ferro erano piegate e l'erba strappata dalla scogliera.|No cais oeste, as grades de ferro estavam tortas e a grama arrancada do penhasco."),
                {"shake": 0.8, "power": 12},
                {"sfx": "whoosh", "and": True},
                S("narr", "A box kept high up on the cliff had been smashed apart.|Una caja guardada muy arriba en el acantilado estaba hecha pedazos.|"
                  "Eine Kiste hoch oben an der Klippe war zertrümmert.|Une caisse rangée haut sur la falaise avait été fracassée.|"
                  "Una cassa tenuta in alto sulla scogliera era stata distrutta.|Uma caixa guardada no alto do penhasco tinha sido despedaçada."),
                S("narr", "Superintendent Robert Muirhead studied everything, and wrote his conclusion.|El superintendente Robert Muirhead lo estudió todo y escribió su conclusión.|"
                  "Superintendent Robert Muirhead prüfte alles und schrieb seinen Schluss nieder.|Le surintendant Robert Muirhead examina tout et rédigea sa conclusion.|"
                  "Il sovrintendente Robert Muirhead esaminò tutto e scrisse la sua conclusione.|O superintendente Robert Muirhead examinou tudo e escreveu sua conclusão."),
                S("narr", "The men had gone down to secure their gear, and an enormous sea swept them away.|Los hombres bajaron a asegurar su equipo, y una ola enorme se los llevó.|"
                  "Die Männer waren hinuntergegangen, um ihr Gerät zu sichern, und eine riesige See riss sie fort.|Les hommes étaient descendus protéger leur matériel, et une mer énorme les emporta.|"
                  "Gli uomini erano scesi a mettere al sicuro l'attrezzatura, e un mare enorme li portò via.|Os homens desceram para prender o equipamento, e um mar enorme os levou."),
                {"show": "g1", "dur": 1.2},
                {"show": "g2", "dur": 1.2, "and": True},
                {"show": "g3", "dur": 1.2, "and": True},
                {"act": "odo", "do": "shake"},
                S("narr", "But no one was ever found. Not one of the three.|Pero nunca se encontró a nadie. Ni a uno de los tres.|"
                  "Doch man fand nie jemanden. Keinen der drei.|Mais on ne retrouva jamais personne. Aucun des trois.|"
                  "Ma nessuno fu mai ritrovato. Nessuno dei tre.|Mas ninguém foi encontrado. Nenhum dos três."),
                {"hide": "g1", "dur": 1.4},
                {"hide": "g2", "dur": 1.4, "and": True},
                {"hide": "g3", "dur": 1.4, "and": True},
                S("odo", "A wave? That's all?|¿Una ola? ¿Eso es todo?|Eine Welle? Das ist alles?|Une vague ? C'est tout ?|Un'onda? Tutto qui?|Uma onda? Só isso?"),
                S("moth", "That's what the records say. The legends say much more.|Eso dicen los archivos. Las leyendas dicen mucho más.|"
                  "So steht es in den Akten. Die Legenden erzählen viel mehr.|C'est ce que disent les archives. Les légendes en disent bien plus.|"
                  "Così dicono gli archivi. Le leggende dicono molto di più.|É o que dizem os registros. As lendas dizem muito mais."),
            ],
            "tail": 0.3,
        },
        {   # 6 legend vs record, ending
            "bg": "lighthouse", "seed": 2, "music": "choir", "wind": True, "eyes": 0, "ambient": 0.42,
            "lights": [{"kind": "moon", "x": 1500, "y": 220, "r": 900}],
            "cam": {"from": [960, 600, 1.12], "to": [760, 640, 1.24]},
            "chars": {"odo": {"x": 520}, "moth": {"x": 680, "y": 640}},
            "creatures": {"g1": {"type": "ghost", "x": 1500, "state": "hidden", "face": -1}},
            "beats": [
                S("narr", "Years later, a poem from 1912 told of a meal left on the table.|Años después, un poema de 1912 habló de una comida servida en la mesa.|"
                  "Jahre später erzählte ein Gedicht von 1912 von einem Essen auf dem Tisch.|Des années plus tard, un poème de 1912 parla d'un repas laissé sur la table.|"
                  "Anni dopo, una poesia del 1912 parlò di un pasto lasciato sulla tavola.|Anos depois, um poema de 1912 falou de uma refeição deixada na mesa."),
                S("narr", "And a chair knocked over, as if someone had leapt up in fright.|Y de una silla volcada, como si alguien se hubiera levantado de un salto.|"
                  "Und von einem umgestoßenen Stuhl, als wäre jemand erschrocken aufgesprungen.|Et d'une chaise renversée, comme si quelqu'un avait bondi de peur.|"
                  "E di una sedia rovesciata, come se qualcuno fosse balzato in piedi per lo spavento.|E de uma cadeira caída, como se alguém tivesse pulado de susto."),
                S("narr", "Moore's real report says the kitchen was clean. Those details were legend.|El informe real de Moore dice que la cocina estaba limpia. Eso era leyenda.|"
                  "Moores echter Bericht sagt: Die Küche war sauber. Das war Legende.|Le vrai rapport de Moore dit que la cuisine était propre. C'était la légende.|"
                  "Il vero rapporto di Moore dice che la cucina era pulita. Quella era leggenda.|O relatório real de Moore diz que a cozinha estava limpa. Isso era lenda."),
                S("narr", "People spoke of sea serpents, of a phantom boat, of strangers.|La gente habló de serpientes marinas, de un barco fantasma, de extraños.|"
                  "Man sprach von Seeschlangen, von einem Geisterboot, von Fremden.|On parla de serpents de mer, d'un bateau fantôme, d'étrangers.|"
                  "Si parlò di serpenti marini, di una barca fantasma, di stranieri.|Falaram de serpentes marinhas, de um barco fantasma, de estranhos."),
                S("narr", "None of it was ever proven.|Nada de eso se demostró jamás.|Nichts davon wurde je bewiesen.|Rien de tout cela ne fut jamais prouvé.|Niente di tutto questo fu mai provato.|Nada disso jamais foi provado."),
                S("odo", "So what really happened to them?|¿Entonces qué les pasó de verdad?|Was ist ihnen dann wirklich passiert?|Alors, que leur est-il vraiment arrivé ?|Allora cosa gli è successo davvero?|Então o que realmente aconteceu com eles?"),
                S("moth", "That's the trouble with true stories, Odo. Some of them never end.|Ese es el problema de las historias reales, Odo. Algunas nunca terminan.|"
                  "Das ist das Problem mit wahren Geschichten, Odo. Manche enden nie.|C'est le problème des histoires vraies, Odo. Certaines ne finissent jamais.|"
                  "È questo il guaio delle storie vere, Odo. Alcune non finiscono mai.|Esse é o problema das histórias reais, Odo. Algumas nunca terminam."),
                {"wait": 0.6},
                {"show": "g1", "dur": 2.0},
                S("narr", "Three keepers walked out into the storm. And the island kept their secret.|Tres fareros salieron a la tormenta. Y la isla guardó su secreto.|"
                  "Drei Wärter gingen hinaus in den Sturm. Und die Insel bewahrte ihr Geheimnis.|Trois gardiens sortirent dans la tempête. Et l'île garda leur secret.|"
                  "Tre guardiani uscirono nella tempesta. E l'isola custodì il loro segreto.|Três faroleiros saíram para a tempestade. E a ilha guardou o segredo deles."),
                {"hide": "g1", "dur": 1.5},
                {"sfx": "bell", "wait": 0.8},
                {"card": "A TRUE STORY. NEVER SOLVED.", "dur": 3.0},
            ],
            "tail": 0.2,
        },
    ],
}

short1 = {   # the real rule / chilling fact
    "id": "ep002_short1", "format": "short",
    "title": "The lighthouse went dark. Three men were gone. 🕯️ #shorts",
    "hook": "THE LIGHT WENT DARK",
    "description": "True story: in December 1900, three lighthouse keepers vanished from Eilean Mor, Scotland. They were never found. #shorts #truestory #unsolvedmystery #horror #hollowmere",
    "tags": ["shorts"] + TAGS[:8],
    "thumbnail": {"bg": "lighthouse", "seed": 2, "creature": "ghost", "text": "GONE"},
    "shots": [{
        "bg": "lighthouse", "seed": 2, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.38, "focus": "odo",
        "chars": {"odo": {"x": 760}},
        "creatures": {"g1": {"type": "ghost", "x": 1150, "state": "hidden", "face": -1}},
        "beats": [
            {"sfx": "creak", "wait": 0.8},
            S("narr", "True story. Scotland, December 1900. A ship passes a lighthouse. The light is out.|Historia real. Escocia, diciembre de 1900. Un barco pasa junto a un faro. La luz está apagada.|"
              "Wahre Geschichte. Schottland, Dezember 1900. Ein Schiff passiert einen Leuchtturm. Das Licht ist aus.|Histoire vraie. Écosse, décembre 1900. Un navire passe un phare. La lumière est éteinte.|"
              "Storia vera. Scozia, dicembre 1900. Una nave passa davanti a un faro. La luce è spenta.|História real. Escócia, dezembro de 1900. Um navio passa por um farol. A luz está apagada."),
            S("narr", "When help arrives, the lamps are full. The clock has stopped.|Cuando llega la ayuda, las lámparas están llenas. El reloj se ha parado.|"
              "Als Hilfe kommt, sind die Lampen voll. Die Uhr steht still.|Quand les secours arrivent, les lampes sont pleines. L'horloge s'est arrêtée.|"
              "Quando arrivano i soccorsi, le lampade sono piene. L'orologio è fermo.|Quando a ajuda chega, as lâmpadas estão cheias. O relógio parou."),
            S("narr", "One coat is still hanging inside. And all three keepers are gone.|Un abrigo sigue colgado dentro. Y los tres fareros han desaparecido.|"
              "Ein Mantel hängt noch drinnen. Und alle drei Wärter sind verschwunden.|Un manteau est encore accroché. Et les trois gardiens ont disparu.|"
              "Un cappotto è ancora appeso dentro. E i tre guardiani sono spariti.|Um casaco ainda está pendurado. E os três faroleiros sumiram."),
            {"act": "odo", "do": "turn"},
            {"light": "out"},
            {"flash": True, "and": True},
            {"show": "g1", "dur": 0.1, "and": True},
            {"wait": 0.8},
            S("narr", "They were never found.|Nunca los encontraron.|Man hat sie nie gefunden.|On ne les a jamais retrouvés.|Non furono mai ritrovati.|Eles nunca foram encontrados."),
        ],
        "tail": 1.6,
    }],
}

short2 = {   # would you
    "id": "ep002_short2", "format": "short",
    "title": "Would YOU keep this lighthouse? 🌊 #shorts",
    "hook": "WOULD YOU TAKE THE JOB?",
    "description": "A tiny island, the open Atlantic, two other keepers and weeks of storms. In 1900 three keepers vanished from here. Would you take the job? Comment YES or NO 👇 #shorts #truestory #horror #hollowmere",
    "tags": ["shorts"] + TAGS[:8] + ["would you rather"],
    "thumbnail": {"bg": "lighthouse", "seed": 3, "creature": "ghost", "text": "YES OR NO"},
    "shots": [{
        "bg": "lighthouse", "seed": 3, "music": "drone", "wind": True, "eyes": 0, "ambient": 0.42,
        "lights": [{"kind": "moon", "x": 1300, "y": 260, "r": 800}],
        "chars": {"odo": {"x": 760}},
        "creatures": {"g1": {"type": "ghost", "x": 1170, "state": "hidden", "face": -1}},
        "focus": ["odo", "g1"],
        "beats": [
            S("narr", "A tiny island far out in the Atlantic. Just you, two other keepers, and the light.|Una isla diminuta en pleno Atlántico. Solo tú, otros dos fareros y la luz.|"
              "Eine winzige Insel weit draußen im Atlantik. Nur du, zwei andere Wärter und das Licht.|Une île minuscule au large de l'Atlantique. Toi, deux autres gardiens, et la lumière.|"
              "Un'isola minuscola in pieno Atlantico. Solo tu, altri due guardiani e la luce.|Uma ilha minúscula no meio do Atlântico. Só você, outros dois faroleiros e a luz."),
            S("narr", "Storms can cut you off for weeks. No one can reach you.|Las tormentas pueden aislarte durante semanas. Nadie puede llegar.|"
              "Stürme können dich wochenlang abschneiden. Niemand erreicht dich.|Les tempêtes peuvent t'isoler des semaines. Personne ne peut venir.|"
              "Le tempeste possono isolarti per settimane. Nessuno può raggiungerti.|As tempestades podem te isolar por semanas. Ninguém consegue chegar."),
            {"show": "g1", "dur": 2.0},
            S("narr", "In 1900, three keepers vanished from this island without a trace.|En 1900, tres fareros desaparecieron de esta isla sin dejar rastro.|"
              "1900 verschwanden drei Wärter spurlos von dieser Insel.|En 1900, trois gardiens ont disparu de cette île sans laisser de trace.|"
              "Nel 1900, tre guardiani scomparvero da quest'isola senza lasciare traccia.|Em 1900, três faroleiros sumiram desta ilha sem deixar rastro."),
            {"act": "odo", "do": "shake"},
            S("narr", "Would YOU take the job? Comment YES or NO.|¿TÚ aceptarías el trabajo? Comenta SÍ o NO.|Würdest DU den Job annehmen? Schreib JA oder NEIN.|"
              "Et TOI, tu accepterais le poste ? Écris OUI ou NON.|TU accetteresti il lavoro? Scrivi SÌ o NO.|VOCÊ aceitaria o trabalho? Comente SIM ou NÃO."),
        ],
        "tail": 1.2,
    }],
}

short3 = {   # scariest moment
    "id": "ep002_short3", "format": "short",
    "title": "They fired a flare. Nothing answered. 🚩 #shorts",
    "hook": "NOTHING ANSWERED",
    "description": "December 26, 1900: the relief boat reaches the Flannan Isles lighthouse. No flag. No keepers. Full true story on the channel. #shorts #truestory #unsolvedmystery #hollowmere",
    "tags": ["shorts"] + TAGS,
    "thumbnail": {"bg": "sea", "seed": 4, "creature": "ghost", "text": "NO ONE"},
    "shots": [{
        "bg": "lighthouse", "seed": 5, "music": "heartbeat", "wind": True, "eyes": 0, "ambient": 0.40,
        "chars": {"odo": {"x": 700}, "moth": {"x": 820, "y": 650}},
        "creatures": {"g1": {"type": "ghost", "x": 1250, "state": "hidden", "face": -1}},
        "focus": ["odo", "g1"],
        "beats": [
            S("narr", "December 26, 1900. The relief boat finally reaches the lighthouse.|26 de diciembre de 1900. El barco de relevo llega por fin al faro.|"
              "26. Dezember 1900. Das Versorgungsschiff erreicht endlich den Leuchtturm.|26 décembre 1900. Le bateau de relève atteint enfin le phare.|"
              "26 dicembre 1900. La nave di soccorso raggiunge finalmente il faro.|26 de dezembro de 1900. O barco de troca finalmente chega ao farol."),
            S("narr", "No flag. No one at the landing. The captain fires a flare.|Sin bandera. Nadie en el embarcadero. El capitán dispara una bengala.|"
              "Keine Flagge. Niemand am Anleger. Der Kapitän schießt eine Leuchtrakete.|Pas de drapeau. Personne au débarcadère. Le capitaine tire une fusée.|"
              "Nessuna bandiera. Nessuno all'approdo. Il capitano spara un razzo.|Sem bandeira. Ninguém no cais. O capitão dispara um sinalizador."),
            {"flash": True},
            {"wait": 1.0},
            S("moth", "Nothing answered.|Nada respondió.|Nichts antwortete.|Rien ne répondit.|Nulla rispose.|Nada respondeu."),
            {"act": "odo", "do": "shake"},
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

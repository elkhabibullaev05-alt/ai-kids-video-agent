"""Milo Survives ep003: 100 days trapped in Antarctica — real cold-survival facts (wind, wet, hypothermia, frostbite, CO, whiteout)."""
import json
import os


def G(x, pose="stand", face="neutral", look=1, extras=(), s=1.0, y=900, at=0, **kw):
    d = {"guy": {"pose": pose, "face": face, "look": look, "extras": list(extras)}, "x": x, "y": y, "s": s, "at": at}
    for k in ("walk", "shirt", "label"):
        if k in kw:
            d["guy"][k] = kw.pop(k)
    d.update(kw)
    return d


def P(name, x, y=900, s=1.0, at=0, **kw):
    d = {"prop": name, "x": x, "y": y, "s": s, "at": at}
    if "in_" in kw:
        kw["in"] = kw.pop("in_")
    d.update(kw)
    return d


def T(text, x, y, size=90, color="black", at=0, **kw):
    d = {"text": text, "x": x, "y": y, "size": size, "color": color, "at": at, "outline": "white"}
    d.update(kw)
    return d


def M(x, pose="stand", face="neutral", look=1, **kw):  # Milo: glasses + yellow raincoat
    return G(x, pose, face, look, extras=["glasses"], shirt="yellow", **kw)


def A(x, pose="stand", face="neutral", look=-1, **kw):  # Dr. Ana, the glaciologist
    return G(x, pose, face, look, extras=["bun", "cap"], shirt="red", **kw)


ANA = "bf_emma"
RADIO = "bm_george"
S = []


def sc(day, say, *items, **kw):
    d = {"say": say, "items": list(items), "bg": kw.pop("bg", "sky")}
    if day is not None:
        d["day"] = day
    d.update(kw)
    S.append(d)


SNOW = lambda: P("snow", 960, 1000, 1.0, in_="none")  # noqa: E731
HUT = lambda x=1350, s=1.0, **k: P("hut", x, 900, s, **k)  # noqa: E731

# COLD OPEN ---------------------------------------------------------------
sc(1, "Four ten in the afternoon. A tiny field hut on the Antarctic ice. The wind is screaming at one hundred fifty kilometres an hour. And the door just ripped open.",
   HUT(960, 1.4, anim="shake"), SNOW(), T("DAY 1", 960, 260, 190, "red", at=0.15, anim="pulse"),
   cam={"from": [960, 540, 1.2], "to": [960, 600, 1.0]}, bg="grey")
sc(1, "Your plane just left. The next one is supposed to come in a week. It will not come for one hundred days.",
   P("skiplane", 600, 420, 0.8, move=[1900, 300]), SNOW(), T("100 DAYS", 1300, 300, 140, "red", at=0.5), bg="grey")
sc(1, "Milo is the camp cook. Big glasses, yellow raincoat over four other layers. He grabs the door with both hands.",
   HUT(1400, 1.1), M(800, "panic", "scream", anim="shake"), SNOW(), T("THE COOK", 700, 330, 80, "dark", at=0.4), bg="grey")
sc(1, "Close it! Close it! Every second that door is open, we lose the heat we worked all day for!",
   A(1200, "point", "angry", anim="shake", label="Dr. Ana"), M(650, "panic", "scream"), SNOW(), voice=ANA, bg="grey")
sc(1, "That's Doctor Ana, a glaciologist. She studies ice. Right now, the ice is studying them.",
   A(960, "hips", "smug", look=1), T("ICE SCIENTIST", 960, 260, 100, "blue", at=0.2), P("iceberg", 1500, 900, 0.7, at=0.5),
   P("magnifier", 450, 700, 0.9, at=0.6), bg="sky")
sc(1, "A storm has grounded every flight on the continent. The main station is three hundred kilometres away. So, can two people survive one hundred days out here?",
   P("globe", 600, 620, 1.2), {"arrow": [[760, 560], [1250, 560]], "at": 0.3}, T("300 KM", 1010, 460, 80, "red", at=0.4),
   HUT(1450, 0.7, at=0.5), T("100 DAYS?", 960, 230, 130, "red", at=0.7), bg="yellow", ground=False, chapter="Day 1: The door")

# PART 1: WIND ------------------------------------------------------------
sc(1, "First, how cold is cold? The lowest temperature ever measured on Earth was in Antarctica. Minus eighty nine point two degrees Celsius, at Vostok station, in nineteen eighty three.",
   P("thermo", 600, 860, 1.6, color="blue"), T("-89.2", 1200, 420, 200, "blue", at=0.3), T("VOSTOK 1983", 1200, 620, 80, "dark", at=0.6), bg="sky")
sc(1, "Where they are, it's around minus thirty. That's survivable. What makes it deadly is the wind.",
   P("thermo", 500, 860, 1.2, color="blue"), T("-30", 500, 380, 140, "blue"), {"arrow": [[800, 560], [1500, 560]], "at": 0.4},
   T("+ WIND", 1300, 400, 120, "red", at=0.5), bg="sky")
sc(1, "Australia's Antarctic program says cold air pours down off the high ice sheet toward the coast. These katabatic winds can gust above two hundred kilometres an hour.",
   P("iceberg", 600, 900, 1.6), {"arrow": [[700, 500], [1500, 800]], "color": "blue", "at": 0.2}, {"arrow": [[700, 400], [1500, 700]], "color": "blue", "at": 0.35},
   T("200+ KM/H", 1350, 340, 110, "red", at=0.6), bg="sky")
sc(1, "Wind strips the thin layer of warm air off your skin, again and again. The CDC says high wind makes your body lose heat much faster. That's wind chill.",
   M(800, "cry", "tired", anim="shake"), SNOW(), T("WIND CHILL", 1350, 300, 110, "blue", at=0.3), P("fan", 1500, 700, 1.0, at=0.5), bg="grey")
sc(1, "So rule one on the ice: get out of the wind. A wall, a hut, a snow trench. Anything.",
   T("RULE 1", 960, 200, 140, "red"), HUT(700, 0.9, at=0.2), M(1300, "pointup", "neutral", look=-1, at=0.4),
   T("OUT OF THE WIND", 960, 420, 90, "dark", at=0.6), bg="yellow")

# PART 2: WET -------------------------------------------------------------
sc(2, "Day two. The storm is still raging. Milo shovels snow away from the door for an hour, and he's proud of himself.",
   HUT(1350, 1.0), M(700, "hold", "grin"), SNOW(), chapter="Day 2: Sweat", bg="grey")
sc(2, "Then he sits down, and the shivering starts. Why? He's wet. Not from snow. From his own sweat.",
   M(960, "cry", "worried", anim="shake"), T("SWEAT", 960, 280, 140, "blue", at=0.4), bg="sky")
sc(2, "Take off a layer before you work hard, not after. If you sweat into your clothes, they stop trapping warm air.",
   M(700, "hold", "neutral"), P("backpack", 1300, 820, 1.2, at=0.3), T("LAYER OFF FIRST", 1150, 360, 90, "red", at=0.5), bg="yellow")
sc(2, "The CDC's cold weather advice is simple: wear layers, and stay dry. In the cold, wet is the enemy.",
   T("CDC", 960, 200, 110, "blue"), T("LAYERS", 650, 450, 100, "dark", at=0.3), T("STAY DRY", 1300, 450, 100, "red", at=0.5),
   M(960, "present", "happy", s=0.8, at=0.6), bg="yellow", ground=False)
sc(2, "Ana hangs his damp socks inside her jacket, close to her body, so they dry overnight. A real polar trick.",
   A(800, "hold", "smug", look=1), {"box": [1150, 560, 200, 120], "color": "white", "at": 0.3}, T("SOCKS", 1250, 620, 50, "dark", at=0.4),
   M(1500, "facepalm", "tired", look=-1, at=0.5))

# PART 3: SNOW = WATER? ---------------------------------------------------
sc(3, "Day three. They're surrounded by frozen water, and they're thirsty. Antarctica is basically a desert. The air is incredibly dry.",
   SNOW(), M(800, "cry", "tired"), T("DESERT?", 1350, 300, 130, "orange", at=0.3), P("sun", 1500, 600, 0.7, at=0.5), chapter="Day 3: Thirst")
sc(3, "Milo grabs a handful of snow and starts eating it.",
   M(960, "hold", "happy"), SNOW(), T("?!", 1300, 380, 170, "red", at=0.6))
sc(3, "Don't! Your body has to burn heat to melt that. You'll only get colder. Melt it on the stove first.",
   A(1200, "point", "angry"), M(650, "panic", "shock", at=0.3), voice=ANA)
sc(3, "Survival manuals agree: eating snow lowers your core temperature. Melt it, then drink it, warm if you can.",
   P("pot", 960, 880, 1.4), T("MELT FIRST", 960, 260, 130, "blue", at=0.3), bg="yellow")
sc(3, "But melting snow eats fuel. A full pot of snow gives you only a small amount of water. So Ana sets a rule: fuel is life. Count every can.",
   P("pot", 600, 880, 1.0), {"arrow": [[700, 700], [1100, 700]], "at": 0.3}, P("bottle", 1250, 820, 0.6, at=0.4),
   P("barrel", 1600, 880, 0.9, at=0.6), T("FUEL = LIFE", 1100, 300, 110, "red", at=0.7), bg="yellow")
sc(4, "Day four. They count the supplies. Fuel for about four months if they're careful. Food for three, if they're very careful.",
   P("barrel", 500, 880, 1.0), P("bread", 1000, 860, 1.0, at=0.2), P("clipboard", 1450, 820, 1.0, at=0.4),
   T("4 MONTHS FUEL", 960, 260, 90, "dark", at=0.5), T("3 MONTHS FOOD", 960, 380, 90, "red", at=0.7), bg="yellow")
sc(4, "And in the cold, your body burns a lot more food just to stay warm. Expedition teams often eat over four thousand calories a day.",
   M(700, "hold", "grin"), P("bread", 1200, 820, 1.4, at=0.2), T("4,000+", 1300, 360, 140, "orange", at=0.4), bg="yellow")

# PART 4: SNOW BLINDNESS ---------------------------------------------------
sc(9, "Day nine. The storm finally stops. The sun comes out, low and blinding, bouncing off endless white.",
   P("sun", 1500, 300, 1.5, anim="pulse"), SNOW(), M(700, "wave", "happy"), chapter="Day 9: Too bright", bg="sky")
sc(9, "Milo spends all afternoon outside fixing the radio antenna. He leaves his goggles inside. They're foggy, and annoying.",
   P("satellite", 1300, 760, 1.0), M(700, "hold", "neutral"), {"cross": [1600, 400, 60], "at": 0.5}, T("NO GOGGLES", 1300, 280, 80, "red", at=0.5))
sc(10, "Day ten. His eyes feel full of sand. They burn. He can barely open them.",
   M(960, "facepalm", "cry", anim="shake"), T("BURNING", 960, 260, 120, "red", at=0.3), bg="grey")
sc(10, "That's snow blindness. Snow reflects a lot of sunlight, and the ultraviolet light burns the surface of your eyes. Basically a sunburn on your eyeballs.",
   P("eye", 960, 560, 2.0), P("sun", 1550, 260, 0.9, at=0.2), {"arrow": [[1450, 330], [1100, 500]], "color": "orange", "at": 0.4},
   T("SUNBURNED EYES", 960, 220, 100, "red", at=0.6), bg="yellow", ground=False)
sc(10, "It usually heals in a day or two, in the dark. But out here you need your eyes. Wear sunglasses or goggles, even on cloudy days.",
   M(960, "fist", "neutral"), T("GOGGLES ON", 960, 280, 120, "blue", at=0.4), bg="yellow")

# PART 5: THE DARK --------------------------------------------------------
sc(30, "Day thirty. Every day the sun sets earlier. Every night is longer. Soon it won't rise at all.",
   P("sun", 960, 700, 1.4, move=[960, 1000]), HUT(500, 0.7), T("DAY 30", 1400, 300, 110, "white", at=0.4), bg="navy", chapter="Day 30: The dark")
sc(30, "This is the polar night. At the South Pole, the sun sets once a year and stays down for about six months.",
   P("globe", 960, 620, 1.6), T("6 MONTHS DARK", 960, 230, 110, "white", at=0.3), bg="navy", ground=False)
sc(30, "Darkness messes with your sleep and your mood. Winter crews in Antarctica fight back with routine. Same wake-up time. Same jobs. Same meals.",
   M(700, "stand", "tired"), P("calendar", 1300, 760, 1.0, at=0.3), T("ROUTINE", 1300, 380, 110, "yellow", at=0.5), bg="navy")
sc(31, "So Milo makes a schedule. Seven a.m., check the radio. Noon, shovel the vents. Six p.m., hot dinner, no matter what.",
   P("clipboard", 600, 820, 1.2), T("7:00 RADIO", 1250, 340, 70, "white", at=0.2), T("12:00 VENTS", 1250, 470, 70, "white", at=0.4),
   T("18:00 DINNER", 1250, 600, 70, "white", at=0.6), bg="navy", ground=False)
sc(31, "Main station to field hut. We hear you. Weather is closed. No flights until it clears. Keep calling every morning.",
   P("satellite", 960, 760, 1.2, anim="pulse"), T("RADIO", 960, 260, 100, "yellow"), voice=RADIO, bg="navy")

# PART 6: CARBON MONOXIDE -------------------------------------------------
sc(41, "Day forty one. A new storm buries the hut. Snow piles up over the roof. Inside, the little heater runs all night.",
   HUT(960, 1.3), SNOW(), P("snow", 960, 700, 1.0), T("BURIED", 960, 230, 140, "white", at=0.4), bg="navy", chapter="Day 41: The headache")
sc(42, "In the morning, both of them have a pounding headache. Milo feels sick and dizzy. Ana can't think straight.",
   M(700, "facepalm", "tired", anim="shake"), A(1250, "cry", "confused", at=0.2), T("HEADACHE", 960, 260, 100, "red", at=0.4))
sc(42, "Wait. Headache. Dizzy. Confused. Both of us at once. Milo, open the door. Now!",
   A(1100, "point", "shock", anim="shake"), M(600, "panic", "shock", at=0.3), voice=ANA)
sc(42, "Carbon monoxide. The snow blocked the heater's vent. The CDC warns this gas has no colour and no smell. You can't see it coming.",
   T("CO", 960, 300, 220, "grey"), {"cross": [960, 300, 150], "color": "red", "at": 0.7}, T("NO COLOUR. NO SMELL.", 960, 600, 90, "red", at=0.4),
   bg="yellow", ground=False)
sc(42, "Its symptoms are headache, dizziness, weakness, an upset stomach, and confusion. If several people get them together, think carbon monoxide and get fresh air.",
   T("HEADACHE", 600, 360, 70, "red", at=0.1), T("DIZZY", 1300, 360, 70, "red", at=0.25), T("WEAK", 600, 520, 70, "red", at=0.4),
   T("SICK", 1300, 520, 70, "red", at=0.55), T("CONFUSED", 960, 680, 70, "red", at=0.7), bg="yellow", ground=False)
sc(42, "They dig out the vent and air the hut. Within hours, they feel better. That's why Milo's schedule says: shovel the vents. Every single day.",
   HUT(960, 1.1), M(500, "hold", "tired", at=0.2), {"arrow": [[1300, 600], [1600, 300]], "color": "green", "at": 0.4},
   T("CLEAR THE VENTS", 1300, 250, 90, "green", at=0.6))
sc(42, "And a real-life rule: never run a stove, heater or generator in a closed space without fresh air coming in.",
   P("pot", 700, 880, 1.2), {"cross": [700, 700, 140], "at": 0.3}, T("FRESH AIR", 1300, 400, 110, "blue", at=0.5), bg="yellow")

# PART 7: WHITEOUT --------------------------------------------------------
sc(53, "Day fifty three. The fuel is stored in a second shed, just fifty metres away. Milo goes to get a can.",
   HUT(500, 0.8), P("barrel", 1450, 880, 0.9), T("50 M", 960, 500, 110, "dark", at=0.3), M(800, "run", "neutral", walk=True, move=[800, 1100]),
   chapter="Day 53: Fifty metres", bg="grey")
sc(53, "Halfway there, the wind kicks up. In seconds, everything turns white. No ground. No sky. No hut.",
   SNOW(), P("snow", 960, 800, 1.3), M(960, "panic", "scream", anim="shake"), T("WHITEOUT", 960, 260, 140, "white", at=0.4), bg="grey", ground=False)
sc(53, "People have died in whiteouts a few steps from a door. You lose all sense of direction, and you start walking in circles.",
   P("footprint", 960, 760, 2.0), {"ring": [960, 620, 260], "at": 0.3}, T("CIRCLES", 960, 240, 120, "red", at=0.5), bg="sky", ground=False)
sc(53, "But Milo's hand is on the rope. On day one, Ana tied a rope line from the hut to the fuel shed.",
   P("rope", 960, 760, 1.5), M(800, "hold", "worried", at=0.2), T("THE ROPE", 960, 280, 130, "orange", at=0.5), bg="grey")
sc(53, "Antarctic stations really do this. In bad weather, you clip on, or keep a hand on the line, and never let go.",
   P("rope", 960, 780, 1.5), HUT(1650, 0.6), M(400, "hold", "neutral", s=0.8), T("NEVER LET GO", 960, 300, 110, "red", at=0.5))
sc(53, "Hand over hand, he follows it back. It takes twenty minutes to cover fifty metres.",
   P("rope", 960, 780, 1.5), M(500, "hold", "tired", walk=True, move=[500, 1300]), P("stopwatch", 1600, 400, 0.9, at=0.3),
   T("20 MIN", 1600, 230, 90, "red", at=0.5), SNOW(), bg="grey")

# PART 8: HYPOTHERMIA -----------------------------------------------------
sc(53, "When he falls through the door, something is wrong. He's stopped shivering. He's mumbling. He drops his cup twice.",
   HUT(1450, 0.9), M(800, "cry", "confused", anim="shake"), P("coffee", 1100, 900, 0.8, at=0.4), chapter="Day 53: Too cold", bg="navy")
sc(53, "The CDC lists the warning signs of hypothermia: shivering, exhaustion, confusion, fumbling hands, memory loss, slurred speech, drowsiness.",
   T("SHIVERING", 600, 300, 64, "red", at=0.05), T("EXHAUSTED", 1320, 300, 64, "red", at=0.2), T("CONFUSED", 600, 440, 64, "red", at=0.35),
   T("FUMBLING", 1320, 440, 64, "red", at=0.5), T("SLURRED", 600, 580, 64, "red", at=0.65), T("DROWSY", 1320, 580, 64, "red", at=0.8),
   bg="yellow", ground=False)
sc(53, "Hypothermia means your body temperature has dropped below thirty five degrees Celsius. Your brain slows down, so the person often can't tell they're in trouble.",
   P("thermo", 700, 860, 1.6, color="blue"), T("BELOW 35 °C", 1250, 380, 120, "blue", at=0.3), M(1350, "think", "confused", s=0.7, at=0.5), bg="sky")
sc(53, "Wet clothes off. Into the sleeping bag. Warm the middle of his body first, the chest and neck. Not his hands and feet.",
   A(1250, "point", "worried"), M(650, "cry", "tired", at=0.2), voice=ANA, bg="navy")
sc(53, "That's the CDC's advice too. Warm the centre of the body first. Dry blankets, skin to skin contact if needed, and warm, sweet drinks once the person is awake enough to swallow. No alcohol.",
   T("CENTRE FIRST", 960, 240, 110, "red"), {"ring": [960, 620, 120], "at": 0.3}, M(960, "stand", "tired", s=0.9, at=0.1),
   P("coffee", 1500, 820, 1.0, at=0.6), bg="yellow")
sc(54, "By morning, Milo is shivering again. Annoying, but shivering is a good sign. His body is fighting back.",
   M(800, "shrug", "tired", anim="shake"), T("SHIVER = GOOD", 1300, 320, 100, "green", at=0.4), A(1500, "hips", "happy", look=-1, at=0.5))

# PART 9: FROSTBITE -------------------------------------------------------
sc(55, "But two of his fingertips look strange. White and greyish. Hard and waxy. He can't feel them.",
   M(700, "hold", "worried"), {"ring": [1150, 560, 80], "color": "red", "at": 0.3}, T("NUMB", 1450, 320, 120, "grey", at=0.5),
   chapter="Day 55: Frostbite", bg="navy")
sc(55, "That's frostbite. The CDC says watch for white or grayish yellow skin that feels unusually firm or waxy, and numbness.",
   T("FROSTBITE", 960, 230, 140, "blue"), T("WHITE / GREY", 960, 430, 80, "dark", at=0.3), T("WAXY", 960, 550, 80, "dark", at=0.5),
   T("NUMB", 960, 670, 80, "dark", at=0.7), bg="yellow", ground=False)
sc(55, "Milo wants to rub them. Ana stops him. Rubbing frozen skin damages it more.",
   M(700, "hold", "neutral"), A(1250, "point", "angry", at=0.2), {"cross": [960, 500, 90], "at": 0.5}, T("DON'T RUB", 960, 260, 110, "red", at=0.5))
sc(55, "Instead, she warms them in lukewarm water. Not hot. Numb skin can't feel a burn, so a stove or a heater can hurt him without him noticing.",
   P("pot", 960, 880, 1.2), T("WARM, NOT HOT", 960, 280, 110, "orange", at=0.3), {"cross": [1550, 700, 90], "at": 0.6}, P("fire", 1550, 880, 0.6, at=0.5))
sc(55, "In real life, frostbite needs a doctor. Milo tells the radio. The station's doctor talks Ana through it every morning.",
   P("satellite", 600, 780, 1.0, anim="pulse"), A(1300, "hold", "neutral"), T("CALL A DOCTOR", 960, 260, 100, "red", at=0.4))
sc(60, "Two weeks later, his fingers have healed. Lucky. From now on, mittens over gloves, always.",
   M(960, "wave", "grin"), T("MITTENS", 960, 280, 120, "blue", at=0.3), A(1500, "hips", "smug", look=-1, at=0.5))

# PART 10: HUDDLE ---------------------------------------------------------
sc(70, "Day seventy. Mid-winter. The food is getting thin. The fuel is getting low. They turn the heater down and sleep back to back.",
   M(700, "stand", "tired"), A(1250, "stand", "tired", at=0.2), P("barrel", 1650, 880, 0.6, at=0.4), T("LOW", 1650, 600, 90, "red", at=0.5),
   chapter="Day 70: Huddle", bg="navy")
sc(70, "Out on the sea ice, the toughest animals on the continent do the same thing. Emperor penguins raise their chicks in the middle of winter.",
   P("penguin", 600, 900, 1.4), P("penguin", 900, 900, 1.2, at=0.2), P("penguin", 1200, 900, 1.4, at=0.3), P("penguin", 1500, 900, 1.2, at=0.4), SNOW(), bg="navy")
sc(70, "They huddle in thousands, and they keep shuffling, so the ones freezing on the outside get their turn in the warm middle.",
   P("penguin", 960, 880, 1.4), P("penguin", 760, 900, 1.2), P("penguin", 1160, 900, 1.2), {"ring": [960, 760, 300], "color": "orange", "at": 0.3},
   T("TAKE TURNS", 960, 280, 110, "white", at=0.5), bg="navy")
sc(71, "Fun fact Ana tells every night. In nineteen fifteen, the ship Endurance was crushed by sea ice. All twenty eight men survived.",
   P("ship", 960, 820, 1.2, anim="shake"), P("iceberg", 500, 900, 0.8), P("iceberg", 1450, 900, 0.8), T("1915", 960, 260, 150, "white", at=0.3),
   T("28 / 28", 960, 420, 100, "yellow", at=0.6), bg="navy")
sc(71, "Teamwork, routine, and refusing to give up. That's what kept them alive.",
   M(700, "fist", "neutral"), A(1250, "fist", "smug", at=0.2), T("TEAM", 960, 280, 150, "orange", at=0.4), bg="navy")

# PART 11: THE WINDOW -----------------------------------------------------
sc(96, "Day ninety six. On the radio, finally, good news.",
   P("satellite", 960, 780, 1.2, anim="pulse"), M(600, "think", "shock"), chapter="Day 96: The window", bg="navy")
sc(96, "Field hut, this is main station. A ski plane can try for you on day one hundred, if the weather window holds. Have a runway marked.",
   P("skiplane", 960, 560, 1.1), T("DAY 100?", 960, 260, 120, "yellow", at=0.4), voice=RADIO, bg="navy")
sc(96, "Winter flights in Antarctica are rare and risky. But they have happened. In twenty sixteen, planes flew into the South Pole in mid winter to evacuate sick workers.",
   P("skiplane", 600, 420, 0.8, move=[1500, 420]), T("2016", 960, 640, 140, "white", at=0.4), P("globe", 1500, 800, 0.7, at=0.6), bg="navy")
sc(97, "Milo and Ana spend three days stamping a flat strip in the snow and lining it with fuel cans and flags, so the pilot can see it in the dark.",
   P("rope", 960, 780, 1.6), P("barrel", 450, 900, 0.5), P("barrel", 1470, 900, 0.5, at=0.2), M(800, "hold", "tired", at=0.3),
   A(1200, "hold", "tired", at=0.4), T("RUNWAY", 960, 260, 120, "orange", at=0.6), bg="navy")
sc(99, "Day ninety nine. The wind is back. Ana watches the sky all night.",
   SNOW(), A(960, "think", "worried"), HUT(1500, 0.7), bg="navy")
sc(100, "Day one hundred. The wind drops. A faint humming in the dark.",
   P("skiplane", 1700, 300, 0.4, move=[1300, 380]), M(700, "pointup", "shock"), A(1000, "pointup", "shock", at=0.2), bg="navy")
sc(100, "Lights on! Every flare we've got!",
   A(960, "panic", "scream", anim="shake"), P("fire", 500, 900, 0.8, at=0.2), P("fire", 1420, 900, 0.8, at=0.3), voice=ANA, bg="navy")
sc(100, "The plane touches down on the strip they built with their own hands. Skis hissing on the snow.",
   P("skiplane", 400, 760, 1.2, move=[1200, 760]), P("barrel", 500, 900, 0.4), P("barrel", 1500, 900, 0.4), bg="navy")
sc(100, "Day one hundred. Thinner, frostnipped, and very much alive.",
   M(700, "fist", "grin"), A(1250, "fist", "happy"), T("DAY 100", 960, 270, 180, "red", anim="pulse", at=0.2), bg="sky")

# RECAP --------------------------------------------------------------------
sc(None, "So, could you survive one hundred days in Antarctica? Here's what kept Milo and Ana alive.",
   T("WHAT WORKED", 960, 220, 130, "red"), M(1500, "present", "happy", look=-1, at=0.3), bg="yellow", chapter="What kept them alive")
sc(None, "One. Get out of the wind. Two. Stay dry, and take a layer off before you sweat.",
   T("1. OUT OF THE WIND", 960, 380, 90, "blue"), T("2. STAY DRY", 960, 540, 90, "orange", at=0.5), bg="yellow", ground=False)
sc(None, "Three. Melt snow, don't eat it. Four. Clear the vents, because carbon monoxide has no smell.",
   T("3. MELT, DON'T EAT", 960, 380, 90, "blue"), T("4. CLEAR THE VENTS", 960, 540, 90, "red", at=0.5), bg="yellow", ground=False)
sc(None, "Five. In a whiteout, never let go of the rope. Six. Warm the body's centre first, and never rub frostbite.",
   T("5. HOLD THE ROPE", 960, 380, 90, "orange"), T("6. CENTRE FIRST", 960, 540, 90, "red", at=0.5), bg="yellow", ground=False)
sc(None, "Next time, Milo wakes up somewhere hot and green. One hundred days lost in the Amazon jungle. Subscribe so you don't miss it.",
   T("NEXT: AMAZON", 1150, 300, 110, "green", at=0.2), M(1400, "panic", "shock", look=-1, at=0.5), P("palm", 600, 900, 1.2), bg="sky")

script = {
    "id": "ep003",
    "title": "Can You Survive 100 Days Trapped in Antarctica?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "A storm grounds every flight, and Milo and Dr. Ana are stuck in a tiny field hut on the Antarctic ice for 100 days. "
        "A hand-drawn survival story with real cold-weather facts: wind chill, why sweat is dangerous, why you should melt snow instead of eating it, "
        "snow blindness, the polar night, carbon monoxide from blocked vents, whiteouts and rope lines, hypothermia and frostbite warning signs, "
        "and how emperor penguins huddle.\n\n"
        "The story is fiction; the survival facts are real. This is not medical advice — in a real emergency, contact emergency services.\n\n"
        "Next episode: 100 Days in the Amazon Jungle.\n\n"
        "Sources:\n"
        "CDC — Preventing hypothermia and frostbite https://www.cdc.gov/disasters/psa/hypothermia-frostbite.html\n"
        "CDC — Carbon monoxide poisoning basics https://www.cdc.gov/carbon-monoxide/about/index.html\n"
        "Australian Antarctic Division — Antarctic weather https://www.antarctica.gov.au/about-antarctica/weather-and-climate/weather/\n\n"
        "#survival #antarctica #animation #storytime"
    ),
    "tags": "survival, antarctica, 100 days, survival story, animated story, how to survive, cold survival, survival tips, milo survives, frostbite, hypothermia",
    "thumbnail": {"bg": "sky", "text": "DAY 53|WHITEOUT", "size": 200, "color": "red",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["glasses"], "shirt": "yellow"}, "guy_x": 1450,
                  "items": [{"prop": "snow", "x": 960, "y": 1000, "s": 1.2}, {"prop": "penguin", "x": 450, "y": 1000, "s": 1.6}]},
    "scenes": S,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep003.json")
json.dump(script, open(out, "w"), indent=1)
words = sum(len(s["say"].split()) for s in S)
print(out, len(S), "scenes", words, "words")

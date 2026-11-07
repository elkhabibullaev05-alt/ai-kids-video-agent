"""Milo Survives ep004: 100 days trapped in an abandoned metro station — real facts (earthquake, dust, live rail, water, rats, time, signalling)."""
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


def V(x, pose="stand", face="neutral", look=-1, **kw):  # Vera, retired metro engineer
    return G(x, pose, face, look, extras=["bun", "hardhat"], shirt="teal", **kw)


VERA = "bf_isabella"
RADIO = "bm_george"
S = []


def sc(day, say, *items, **kw):
    d = {"say": say, "items": list(items), "bg": kw.pop("bg", "sky")}
    if day is not None:
        d["day"] = day
    d.update(kw)
    S.append(d)


DUST = lambda: P("rubble", 960, 1000, 1.0, in_="none")  # noqa: E731
TORCH = lambda x=1300, y=640, s=1.0, **k: P("torch", x, y, s, **k)  # noqa: E731

# COLD OPEN ---------------------------------------------------------------
sc(1, "Eleven fifty two p.m. A ghost station, forty metres under the city. The lights go out. Then the ground starts to shake.",
   P("tunnel", 960, 900, 1.3, anim="shake"), DUST(), T("DAY 1", 960, 220, 190, "red", at=0.12, anim="pulse"),
   cam={"from": [960, 540, 1.25], "to": [960, 600, 1.0]}, bg="navy")
sc(1, "Behind you, the only staircase to the street collapses into a wall of concrete. You are sealed in. For one hundred days.",
   P("stairs", 700, 900, 1.2), P("rubble", 760, 900, 1.3, at=0.3, anim="shake"), T("100 DAYS", 1400, 300, 150, "red", at=0.55), bg="navy")
sc(1, "Milo was only here for a night tour of the old closed station. Big glasses, yellow raincoat, one phone at eight percent.",
   M(800, "panic", "scream", anim="shake"), P("phone", 1350, 700, 0.9, at=0.3), T("8%", 1350, 420, 130, "red", at=0.5), bg="navy")
sc(1, "Down! Get down, cover your head, and hold on to something solid until it stops!",
   V(1250, "point", "angry", anim="shake", label="Vera"), M(650, "cry", "scream"), DUST(), voice=VERA, bg="navy")
sc(1, "That's Vera, the tour guide. She spent forty years as a metro engineer. She knows every pipe down here.",
   V(960, "hips", "smug", look=1), T("METRO ENGINEER", 960, 250, 100, "teal", at=0.2), P("pipe", 960, 520, 0.9, at=0.5), bg="grey")
sc(1, "So, can two people survive one hundred days in a tunnel nobody uses anymore? Let's find out, day by day.",
   P("tunnel", 600, 900, 0.9), T("100 DAYS?", 1250, 300, 140, "red", at=0.3), M(1350, "think", "worried", look=-1, at=0.5),
   bg="yellow", chapter="Day 1: The quake")

# PART 1: QUAKE + DUST ----------------------------------------------------
sc(1, "Vera is doing exactly what the US emergency agency Ready dot gov teaches. Drop to your hands and knees. Cover your head and neck. Hold on.",
   T("DROP", 500, 330, 120, "red", at=0.1), T("COVER", 960, 330, 120, "orange", at=0.35), T("HOLD ON", 1420, 330, 120, "blue", at=0.6),
   M(960, "cry", "worried", s=0.8, at=0.2), bg="yellow")
sc(1, "Don't run in the dark. Most injuries in an earthquake come from things falling on you, or from you falling over things.",
   M(800, "run", "shock", walk=True), {"cross": [800, 650, 160], "at": 0.4}, DUST(), T("DON'T RUN", 1350, 300, 110, "red", at=0.5), bg="navy")
sc(1, "The shaking stops. The air is thick with concrete dust. Milo starts coughing, and then he starts yelling for help.",
   M(900, "panic", "scream", anim="shake"), DUST(), P("rubble", 960, 700, 0.8, at=0.2), bg="grey")
sc(1, "Stop shouting. You're breathing in that dust. Pull your shirt over your mouth.",
   V(1200, "point", "angry"), M(650, "facepalm", "tired", at=0.3), voice=VERA, bg="grey")
sc(1, "That's real advice too. If you are trapped, cover your mouth with your shirt. And instead of shouting, use a whistle, or bang on a pipe or wall.",
   P("whistle", 600, 640, 1.6), P("pipe", 1300, 820, 0.7, at=0.3), T("NO SHOUTING", 960, 250, 110, "red", at=0.5), bg="yellow")
sc(1, "Shouting wears you out and fills your lungs with dust. A whistle or a metal pipe carries sound much further.",
   P("pipe", 960, 760, 1.2, anim="shake"), T("CLANG!", 960, 360, 150, "orange", at=0.2, anim="pulse"), bg="grey")

# PART 2: LIGHT -----------------------------------------------------------
sc(2, "Day two. It's completely dark. Not night dark. Underground dark. You can't see your own hand.",
   M(960, "stand", "worried", s=0.9, alpha=0.4), T("TOTAL DARK", 960, 260, 130, "white", at=0.3), bg="black", chapter="Day 2: Darkness")
sc(2, "They have one flashlight, two spare batteries, and Milo's dying phone. Vera's first rule: light is food. Never waste it.",
   TORCH(700, 640, 1.2), P("battery", 1200, 850, 0.8, at=0.2), P("battery", 1350, 850, 0.8, at=0.3), T("LIGHT = FOOD", 1050, 260, 110, "yellow", at=0.5), bg="navy")
sc(2, "The phone goes off, to save it for later. The flashlight is only switched on to move, to cook, or to check something. Then off again.",
   P("phone", 600, 720, 1.0), {"cross": [600, 600, 110], "at": 0.3}, TORCH(1250, 640, 1.0, at=0.4), T("ON. OFF.", 1250, 280, 110, "white", at=0.6), bg="navy")
sc(2, "Vera finds the old station office. Inside, a dusty cupboard with emergency supplies, left from the days this station was a shelter.",
   P("building", 600, 900, 0.8), P("tins", 1300, 900, 1.2, at=0.3), T("SHELTER STORE", 960, 260, 100, "yellow", at=0.5), bg="navy")
sc(2, "That part is real history. During the Blitz, Londoners slept in the Underground to escape the bombs. On one night in September nineteen forty, about one hundred seventy seven thousand people sheltered down there.",
   P("train", 960, 860, 1.0), M(500, "stand", "tired", s=0.6, at=0.2), V(1450, "stand", "tired", s=0.6, look=-1, at=0.3),
   T("1940", 960, 230, 130, "red", at=0.4), T("177,000", 960, 400, 120, "dark", at=0.6), bg="tan")

# PART 3: AIR -------------------------------------------------------------
sc(3, "Day three. Milo has a terrible thought. What if the air runs out?",
   M(960, "think", "shock"), T("AIR?", 960, 260, 160, "red", at=0.3), bg="navy", chapter="Day 3: Air")
sc(3, "Vera wets a finger and holds it up. Cool on one side. There's a draft. Air is moving, so somewhere, a ventilation shaft is still open.",
   V(800, "pointup", "smug", look=1), {"arrow": [[1600, 400], [1200, 400]], "color": "blue", "at": 0.3}, T("DRAFT", 1400, 260, 110, "blue", at=0.5), bg="navy")
sc(3, "Metros are built with ventilation shafts, to pull fresh air in and push stale air and heat out. They follow the draft, and find a grate. A thin grey light falls from far above.",
   P("vent", 960, 1000, 1.2), M(700, "pointup", "happy", at=0.4), T("VENT SHAFT", 1350, 300, 100, "white", at=0.5), bg="navy")
sc(3, "It's too narrow and too high to climb. But it means air. And this spot becomes their camp.",
   P("vent", 960, 1000, 1.0), P("tent", 960, 900, 0.8, at=0.3), T("CAMP", 960, 230, 120, "yellow", at=0.5), bg="navy")

# PART 4: LIVE RAIL -------------------------------------------------------
sc(4, "Day four. Milo wants to walk down the tunnel to the next station. Vera grabs his arm before he steps onto the track.",
   P("tunnel", 1300, 900, 1.0), M(700, "run", "neutral", walk=True), V(400, "point", "shock", look=1, at=0.4),
   chapter="Day 4: The rail", bg="navy")
sc(4, "See that rail on the side? That's the third rail. It powers the trains. If the main line still has power, it can kill you in a second.",
   P("rails", 960, 900, 1.3), T("THIRD RAIL", 960, 300, 130, "red", at=0.3, anim="pulse"), voice=VERA, bg="navy")
sc(4, "Many metros feed their trains through a third rail carrying six hundred to seven hundred fifty volts. You can't see if it's live. So you treat every rail as live.",
   P("rails", 960, 900, 1.2), T("600-750 V", 960, 280, 140, "red", at=0.2), T("ALWAYS LIVE", 960, 460, 100, "dark", at=0.6), bg="yellow")
sc(4, "And never touch it with anything. Not a foot, not a stick, not a wet shoe.",
   P("rails", 960, 900, 1.2), {"cross": [960, 650, 160], "at": 0.3}, M(1500, "facepalm", "worried", look=-1, s=0.8, at=0.4), bg="yellow")
sc(4, "Vera checks the next tunnel with the flashlight anyway. It's blocked by rock after two hundred metres. There's no way out on foot.",
   P("tunnel", 800, 900, 1.0), P("rubble", 800, 900, 0.9, at=0.3), TORCH(1350, 640, 0.9), T("BLOCKED", 800, 250, 120, "red", at=0.5), bg="navy")

# PART 5: WATER -----------------------------------------------------------
sc(5, "Day five. The shelter cupboard had a few bottles of water. They're almost gone. Thirst is the next enemy.",
   P("bottle", 700, 860, 1.4), P("bottle", 900, 880, 1.0, at=0.2), T("ALMOST GONE", 1350, 300, 100, "red", at=0.4), M(1450, "cry", "tired", look=-1, at=0.5),
   chapter="Day 5: Water", bg="navy")
sc(5, "But tunnels leak. Water seeps through the walls, and old stations have pumps to stop them flooding. Vera finds a steady drip from a crack.",
   P("pipe", 960, 520, 1.0), {"arrow": [[960, 560], [960, 760]], "color": "blue", "at": 0.3}, P("pot", 960, 900, 1.0, at=0.4), bg="navy")
sc(5, "Milo wants to drink it straight. Vera says no. That water ran through soil, rubble, and who knows what else.",
   M(700, "hold", "happy"), V(1250, "point", "angry", at=0.3), {"cross": [960, 500, 100], "at": 0.5}, bg="navy")
sc(5, "The CDC says boiling kills germs, including viruses, bacteria, and parasites. Bring clear water to a rolling boil for one minute.",
   P("pot", 960, 880, 1.4), P("fire", 960, 960, 0.6), T("1 MINUTE", 960, 260, 140, "blue", at=0.3), T("ROLLING BOIL", 960, 420, 90, "dark", at=0.6), bg="yellow")
sc(5, "First they strain it through a cloth to get the grit out. Then they boil it on the old camping stove from the cupboard, right under the vent, where the fumes can escape.",
   P("pot", 700, 880, 1.0), P("vent", 1300, 1000, 0.8), {"arrow": [[800, 600], [1250, 400]], "color": "grey", "at": 0.4}, T("UNDER THE VENT", 960, 250, 90, "red", at=0.6), bg="navy")

# PART 6: FOOD ------------------------------------------------------------
sc(7, "Day seven. They count the food. Forty two tins of beans and fish. Crackers. A bag of sugar. Vera does the math out loud.",
   P("tins", 700, 900, 1.3), P("bread", 1200, 880, 0.9, at=0.2), P("clipboard", 1550, 820, 0.8, at=0.4), T("42 TINS", 960, 250, 130, "dark", at=0.5),
   chapter="Day 7: Rations", bg="navy")
sc(7, "Half a tin each, every day. That gives us about six weeks. After that, we eat less.",
   V(960, "hold", "neutral"), T("6 WEEKS", 960, 260, 140, "red", at=0.4), voice=VERA, bg="navy")
sc(7, "A healthy adult can survive weeks with little food, but only days without water. That's why water came first.",
   T("WATER: DAYS", 960, 340, 110, "blue"), T("FOOD: WEEKS", 960, 520, 110, "orange", at=0.4), bg="yellow", ground=False)
sc(7, "So every bit of energy counts. They stop exploring for fun. They rest, keep warm, and move slowly.",
   M(700, "stand", "tired"), V(1250, "stand", "tired", at=0.2), T("SAVE ENERGY", 960, 260, 110, "green", at=0.4), bg="navy")

# PART 7: RATS ------------------------------------------------------------
sc(12, "Day twelve. Milo wakes up to scratching. Something is eating through the cracker bag.",
   P("rat", 1100, 880, 1.6), P("bread", 1300, 880, 0.8), M(600, "panic", "scream", anim="shake", at=0.3), chapter="Day 12: Rats", bg="navy")
sc(12, "Rats. Dozens of them. Metros are full of them, and they're hungry too.",
   P("rat", 500, 900, 1.2), P("rat", 900, 900, 1.4, at=0.1), P("rat", 1300, 900, 1.2, at=0.2), P("rat", 1600, 900, 1.0, at=0.3), T("RATS", 960, 260, 160, "red", at=0.4), bg="navy")
sc(12, "The bites are bad. But the CDC warns about something sneakier. Rat urine in water and soil can spread a disease called leptospirosis.",
   P("rat", 700, 880, 1.5), T("LEPTOSPIROSIS", 1200, 330, 90, "red", at=0.3), P("bottle", 1300, 760, 0.8, at=0.5), bg="yellow")
sc(12, "It gets in through cuts in your skin, or water you swallow. So they cover every cut, boil every drop, and never wade in the puddles.",
   P("bandage", 600, 760, 1.2), P("pot", 1000, 880, 0.9, at=0.2), {"cross": [1450, 700, 100], "at": 0.4}, T("COVER CUTS", 960, 250, 110, "red", at=0.5), bg="yellow")
sc(12, "And they do what the CDC says: keep food, water and trash in closed containers. They hang the food bag from a pipe, out of reach.",
   P("pipe", 960, 420, 1.0), {"box": [880, 470, 160, 150], "color": "tan", "at": 0.3}, P("rat", 960, 900, 1.0), T("CLOSED + HIGH", 960, 230, 100, "green", at=0.5), bg="navy")

# PART 8: TIME ------------------------------------------------------------
sc(20, "Day twenty. Or is it? Milo argues it's day fifteen. Vera says day twenty three. With no sun, they've lost track of time.",
   M(700, "shrug", "confused"), V(1250, "point", "angry", at=0.2), T("15?", 700, 280, 110, "orange", at=0.3), T("23?", 1250, 280, 110, "orange", at=0.5),
   chapter="Day 20: Lost time", bg="navy")
sc(20, "This happens to real people. In nineteen sixty two, French scientist Michel Siffre lived alone in a cave with no clock for about two months.",
   P("tunnel", 960, 900, 1.0), M(960, "think", "tired", s=0.6, at=0.3), T("1962", 960, 230, 140, "red", at=0.4), bg="tan")
sc(20, "When his team told him it was over, he was shocked. He thought it was about a month earlier. His body clock had drifted.",
   P("calendar", 700, 760, 1.2), T("-1 MONTH", 1250, 330, 120, "red", at=0.3), P("stopwatch", 1300, 700, 0.8, at=0.5), bg="tan")
sc(21, "So Vera fixes it. The light from the vent is their clock. When it turns grey, it's day. Each morning, Milo scratches a line on the wall.",
   P("vent", 600, 1000, 0.9), {"box": [1100, 380, 420, 300], "color": "grey", "at": 0.2}, T("IIII IIII IIII", 1310, 530, 70, "dark", at=0.4), bg="navy")
sc(21, "Routine keeps your mind steady. Same wake up. Same jobs. Water, rations, signal, sleep.",
   P("clipboard", 700, 820, 1.2), T("WATER", 1300, 330, 70, "blue", at=0.1), T("RATIONS", 1300, 450, 70, "orange", at=0.3),
   T("SIGNAL", 1300, 570, 70, "red", at=0.5), T("SLEEP", 1300, 690, 70, "dark", at=0.7), bg="navy", ground=False)

# PART 9: SIGNAL ----------------------------------------------------------
sc(22, "Signal is the most important job. Three times a day, Milo bangs the big water pipe with a wrench. Three hits. Pause. Three hits.",
   P("pipe", 960, 520, 1.3, anim="shake"), M(700, "fist", "neutral"), T("BANG BANG BANG", 1200, 300, 90, "orange", at=0.3), chapter="Day 22: The pipe", bg="navy")
sc(22, "Three of anything is a common distress signal. Three whistles, three flashes, three bangs. A pattern tells rescuers it's a person, not falling rocks.",
   T("3", 960, 400, 300, "red"), P("whistle", 500, 700, 1.0, at=0.3), TORCH(1400, 700, 0.8, at=0.5), bg="yellow", ground=False)
sc(22, "And the pipe runs all the way up to the street. Metal carries sound a long way.",
   P("pipe", 960, 700, 1.4), {"arrow": [[600, 600], [1500, 300]], "color": "orange", "at": 0.3}, P("building", 1600, 420, 0.5, at=0.5), bg="navy")
sc(23, "Nobody answers. Not that day. Not that week.",
   P("pipe", 960, 470, 1.2), M(960, "cry", "sad"), bg="navy")

# PART 10: FLOOD ----------------------------------------------------------
sc(38, "Day thirty eight. Milo wakes up with his feet wet. The track bed is filling with water.",
   P("rails", 960, 900, 1.2), {"box": [0, 860, 1920, 220], "color": "sea", "at": 0.3}, M(900, "panic", "shock", anim="shake"), chapter="Day 38: The flood", bg="navy")
sc(38, "Up top, it must be raining hard. And down here, the pumps have no power.",
   P("cloud", 960, 300, 1.2), {"arrow": [[960, 400], [960, 760]], "color": "blue", "at": 0.3}, T("NO PUMPS", 960, 560, 100, "red", at=0.5), bg="grey")
sc(38, "Real metros pump enormous amounts of water every day just to stay dry. When the power goes, low tunnels fill fast.",
   P("tunnel", 960, 900, 1.0), {"box": [500, 760, 920, 160], "color": "sea", "at": 0.4}, T("PUMPS 24/7", 960, 240, 110, "blue", at=0.5), bg="yellow")
sc(38, "Get everything onto the platform. High ground. And stay out of that water.",
   V(1250, "point", "worried"), M(650, "hold", "tired", at=0.3), voice=VERA, bg="navy")
sc(38, "Floodwater is never clean. Ready dot gov warns it can carry chemicals, sewage and debris. And it might be touching a live rail.",
   T("CHEMICALS", 600, 340, 80, "red", at=0.1), T("SEWAGE", 1320, 340, 80, "red", at=0.3), T("DEBRIS", 600, 520, 80, "red", at=0.5),
   T("LIVE RAIL?", 1320, 520, 80, "red", at=0.7), bg="yellow", ground=False)
sc(40, "Two days later, the water stops rising, half a metre below the platform edge. They sleep in shifts, watching it.",
   P("stairs", 600, 900, 0.8), {"box": [0, 880, 1920, 200], "color": "sea"}, M(1100, "stand", "tired", at=0.2), V(1450, "stand", "tired", at=0.3), bg="navy")

# PART 11: LOW POINT ------------------------------------------------------
sc(55, "Day fifty five. The flashlight is on its last battery. The rations are cut to a third of a tin a day. Milo stops talking.",
   P("battery", 700, 850, 1.2), P("tins", 1300, 900, 0.7), M(1000, "stand", "sad", at=0.3), chapter="Day 55: The low point", bg="black")
sc(55, "Vera gives him a job. Every day, write down one thing that went right. Clean water. A dry blanket. One less rat.",
   V(1250, "present", "happy"), P("clipboard", 700, 800, 1.0, at=0.3), T("1 GOOD THING", 960, 250, 100, "yellow", at=0.5), bg="navy")
sc(55, "Survivors of long ordeals often say the same: small goals, and someone to talk to, keep you going.",
   M(700, "stand", "tired"), V(1250, "stand", "happy", at=0.2), T("SMALL GOALS", 960, 260, 110, "green", at=0.4), bg="navy")
sc(70, "Day seventy. An aftershock. Dust pours from the roof. This time Milo doesn't run. Drop. Cover. Hold on.",
   M(960, "cry", "worried", anim="shake"), DUST(), T("DROP. COVER. HOLD ON.", 960, 260, 80, "red", at=0.3), bg="grey")
sc(70, "Ready dot gov says to expect aftershocks after the main quake, and to protect yourself the same way every time.",
   T("AFTERSHOCKS", 960, 300, 120, "red"), T("SAME RULES", 960, 480, 100, "dark", at=0.4), bg="yellow", ground=False)

# PART 12: RESCUE ---------------------------------------------------------
sc(94, "Day ninety four. Milo bangs the pipe, three and three, like every day. And then, very faintly, the pipe bangs back.",
   P("pipe", 960, 520, 1.3, anim="shake"), M(700, "fist", "shock"), T("...BANG BANG BANG", 1250, 300, 80, "green", at=0.6), chapter="Day 94: The answer", bg="navy")
sc(94, "Again! Three more! Let them know we're both alive!",
   V(1250, "panic", "scream", anim="shake"), M(650, "fist", "grin", at=0.3), voice=VERA, bg="navy")
sc(95, "This is the rescue team. We hear you. We are digging from the street. Keep signalling every hour.",
   P("vent", 960, 1000, 1.1), T("WE HEAR YOU", 960, 230, 110, "yellow", at=0.3), voice=RADIO, bg="navy")
sc(96, "The voice comes down the ventilation shaft. Crews were clearing the main line, and an engineer heard the pattern in the pipes.",
   P("vent", 700, 1000, 0.9), P("heli", 1400, 400, 0.6, at=0.3), T("THE PATTERN", 1350, 650, 90, "orange", at=0.5), bg="navy")
sc(99, "Day ninety nine. Drilling, closer every hour. They stay back from the wall and keep their mouths covered from the dust.",
   P("rubble", 960, 900, 1.3, anim="shake"), M(500, "stand", "worried"), V(1500, "stand", "worried", at=0.2), T("STAY BACK", 960, 250, 110, "red", at=0.4), bg="grey")
sc(100, "Day one hundred. A crack of white light breaks through the concrete.",
   P("sun", 960, 520, 1.2, anim="pulse"), P("rubble", 960, 900, 1.2), M(600, "pointup", "shock", at=0.3), V(1350, "pointup", "shock", at=0.4), bg="grey")
sc(100, "Thinner, paler, squinting like moles, and very much alive.",
   M(700, "fist", "grin"), V(1250, "fist", "happy"), T("DAY 100", 960, 270, 180, "red", anim="pulse", at=0.2), bg="sky")

# RECAP -------------------------------------------------------------------
sc(None, "So, could you survive one hundred days in an abandoned metro? Here's what kept Milo and Vera alive.",
   T("WHAT WORKED", 960, 220, 130, "red"), M(1500, "present", "happy", look=-1, at=0.3), bg="yellow", chapter="What kept them alive")
sc(None, "One. Drop, cover, hold on, and use a shirt over your mouth in the dust. Two. Signal with a whistle or a pipe, not your voice.",
   T("1. DROP COVER HOLD", 960, 380, 85, "blue"), T("2. BANG, DON'T SHOUT", 960, 540, 85, "orange", at=0.5), bg="yellow", ground=False)
sc(None, "Three. Every rail is live. Four. Boil water for one minute, and cover your cuts.",
   T("3. EVERY RAIL IS LIVE", 960, 380, 85, "red"), T("4. BOIL 1 MINUTE", 960, 540, 85, "blue", at=0.5), bg="yellow", ground=False)
sc(None, "Five. Ration light like food. Six. Keep a routine, so you don't lose track of time, or hope.",
   T("5. RATION LIGHT", 960, 380, 85, "orange"), T("6. KEEP A ROUTINE", 960, 540, 85, "green", at=0.5), bg="yellow", ground=False)
sc(None, "Next time, Milo wakes up on a cruise ship that is slowly sinking. Subscribe so you don't miss it.",
   T("NEXT: SINKING SHIP", 1150, 300, 100, "blue", at=0.2), P("ship", 600, 860, 1.1, anim="shake"), M(1450, "panic", "shock", look=-1, at=0.5), bg="sky")

script = {
    "id": "ep004",
    "title": "Can You Survive 100 Days in an Abandoned Metro?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "An earthquake seals Milo and Vera, a retired metro engineer, inside a closed ghost station deep under the city — for 100 days. "
        "A hand-drawn survival story with real facts: Drop, Cover and Hold On, why you should bang on a pipe instead of shouting, "
        "the deadly third rail, how to make water safe by boiling, rats and leptospirosis, how people lose track of time underground, "
        "and why floodwater is dangerous.\n\n"
        "The story is fiction; the survival facts are real. This is not medical advice — in a real emergency, contact emergency services.\n\n"
        "Next episode: 100 Days on a Sinking Cruise Ship.\n\n"
        "Sources:\n"
        "Ready.gov — Earthquakes https://www.ready.gov/earthquakes\n"
        "CDC — Water treatment options (boiling) https://www.cdc.gov/drinking-water/prevention/water-treatment-hiking-camping-traveling.html\n"
        "CDC — Preventing leptospirosis https://www.cdc.gov/leptospirosis/prevention/index.html\n"
        "London Museum — Blitz Underground https://www.londonmuseum.org.uk/blog/blitz-underground-how-war-artists-saw-tube-shelters/\n\n"
        "#survival #metro #animation #storytime"
    ),
    "tags": "survival, metro, subway, 100 days, survival story, animated story, how to survive, earthquake survival, survival tips, milo survives, trapped underground",
    "thumbnail": {"bg": "navy", "text": "DAY 1|TRAPPED", "size": 200, "color": "red",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["glasses"], "shirt": "yellow"}, "guy_x": 1450,
                  "items": [{"prop": "tunnel", "x": 520, "y": 1000, "s": 1.3}, {"prop": "rat", "x": 900, "y": 1040, "s": 1.6}]},
    "scenes": S,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep004.json")
json.dump(script, open(out, "w"), indent=1)
words = sum(len(s["say"].split()) for s in S)
print(out, len(S), "scenes", words, "words")

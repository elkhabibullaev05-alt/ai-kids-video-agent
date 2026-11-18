"""Milo Survives ep007: trapped in a flooding city, Day 1 to Day 100 — real flood-safety facts.
Written on 2026-11-18 because cloud/queue/milo was empty (worker: queue_empty); ep006 promised this place as next.
Output: cloud/queue/milo/ep007.json (the laptop maker renders + uploads it)."""
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


def R(x, pose="stand", face="neutral", look=-1, **kw):  # Rosa, retired nurse, top-floor neighbour
    return G(x, pose, face, look, extras=["bun"], shirt="purple", label="Rosa", **kw)


def D(x, pose="stand", face="neutral", look=-1, **kw):  # Dev, rescue boat crew
    return G(x, pose, face, look, extras=["hardhat"], shirt="orange", label="Dev", **kw)


ROSA = "bf_emma"
DEV = "bm_george"
S = []


def sc(day, say, *items, **kw):
    d = {"say": say, "items": list(items), "bg": kw.pop("bg", "sky")}
    if day is not None:
        d["day"] = day
    d.update(kw)
    S.append(d)


# COLD OPEN ---------------------------------------------------------------
sc(1, "Three twelve a.m. Milo steps out of bed, straight into cold water. It's already up to his ankles. And it's rising.",
   M(900, "panic", "scream", anim="shake"), P("wave", 960, 1000, 1.4, in_="none"), T("DAY 1", 960, 220, 190, "red", at=0.15, anim="pulse"),
   cam={"from": [960, 600, 1.3], "to": [960, 540, 1.0]}, bg="navy", chapter="Day 1: The water")
sc(1, "His phone screams on the table. Flash flood warning. The river levee upstream has broken. The whole low town is going under.",
   P("phone", 700, 750, 1.1, anim="shake"), T("FLASH FLOOD", 1250, 300, 120, "red", at=0.3), P("wave", 1300, 950, 0.9, at=0.5), bg="navy")
sc(1, "Milo lives on the ground floor of an old building in Port Halden, a river city. Big glasses, yellow raincoat, no plan.",
   P("building", 960, 900, 1.3), M(1450, "shrug", "worried", at=0.3), bg="navy")
sc(1, "His hand goes to the light switch. Then a voice from the stairs shouts one word. Don't.",
   M(800, "point", "confused"), T("DON'T!", 1300, 300, 170, "red", at=0.4, anim="shake"), bg="navy")
sc(1, "You're standing in water. Never touch a switch, a plug or anything electric when you're wet or in water.",
   R(1200, "point", "angry", anim="shake"), P("powerline", 650, 900, 0.9, at=0.2), T("NO SWITCHES", 960, 250, 110, "red", at=0.5),
   voice=ROSA, bg="navy")
sc(1, "That's Rosa, a retired nurse from the top floor, with a torch, a whistle and a ready packed bag.",
   R(1100, "present", "smug"), P("torch", 650, 750, 0.9, at=0.2), P("whistle", 850, 650, 0.7, at=0.3), P("backpack", 1500, 900, 0.8, at=0.4), bg="navy")
sc(1, "Rule one in a flood: go up. Not out into the street. Up, to the highest floor you can reach.",
   P("stairs", 960, 950, 1.1), M(700, "run", "worried", walk=True, at=0.2), T("GO UP", 960, 250, 160, "red", at=0.4), bg="navy")
sc(1, "Milo grabs what matters. Phone, charger, all the bottled water he owns, and a plastic bag for his passport.",
   P("bottle", 600, 850, 0.9), P("phone", 850, 780, 0.8, at=0.2), P("envelope", 1100, 780, 0.9, at=0.4), M(1450, "hold", "worried", at=0.1), bg="navy")
sc(1, "By the time he reaches the second step, the water in his flat is at his knees.",
   M(960, "run", "scream", walk=True, anim="shake"), P("wave", 960, 1000, 1.3, in_="none", move=[960, 900]), bg="navy")

# THE STREET --------------------------------------------------------------
sc(1, "From the top floor window, the street is a brown river. Cars float past like toys.",
   P("car", 600, 850, 1.0, anim="bob", move=[1400, 850]), P("wave", 960, 1000, 1.3, in_="none"), M(1500, "pointup", "shock", at=0.2), bg="grey",
   chapter="Day 1: The street")
sc(1, "That's real. Just twelve inches of rushing water, thirty centimetres, can carry away most cars. Two feet can carry trucks.",
   P("car", 700, 850, 0.9, anim="bob"), T("12 IN", 700, 350, 140, "red", at=0.2), P("truck", 1300, 850, 0.9, at=0.4, anim="bob"), T("2 FT", 1300, 350, 140, "red", at=0.6))
sc(1, "And six inches of fast water, the height of a pencil, can knock an adult off their feet.",
   G(960, "panic", "scream", extras=["hair"], anim="shake"), T("6 IN", 960, 250, 160, "red", at=0.3), P("wave", 960, 1000, 1.0, in_="none"))
sc(1, "Below them, a man in the next building is getting into his car. He wants to drive out.",
   G(700, "point", "neutral", extras=["cap"], label="Neighbour"), P("car", 1250, 880, 1.0, at=0.2), bg="grey")
sc(1, "Rosa bangs on the glass. More than half of flood drownings happen in vehicles. Turn around, don't drown.",
   R(1300, "fist", "angry", anim="shake"), T("TURN AROUND", 800, 250, 110, "red", at=0.3), T("DON'T DROWN", 800, 380, 110, "red", at=0.5), voice=ROSA)

# NIGHT 1 ----------------------------------------------------------------
sc(1, "Then the power dies. The whole city goes black. The only light is Rosa's torch and the rain.",
   P("torch", 960, 750, 1.1, anim="pulse"), P("cloud", 600, 300, 1.0), P("cloud", 1350, 280, 0.9, at=0.2), bg="navy",
   chapter="Day 1: Blackout")
sc(1, "Milo wants to call his mum. Rosa says text instead. Phone lines jam in disasters, but short texts often get through.",
   P("phone", 800, 750, 1.0), T("TEXT", 1300, 300, 140, "red", at=0.3), R(1500, "point", "neutral", at=0.2), voice=ROSA, bg="navy")
sc(1, "Then low power mode. That battery might be your only way to call for help tomorrow.",
   P("battery", 960, 750, 1.1, anim="pulse"), T("SAVE IT", 960, 280, 130, "red", at=0.4), bg="navy")
sc(1, "Rosa turns on a wind up radio. Emergency radio works when the internet and power don't.",
   R(900, "hold", "neutral"), P("tv", 1350, 750, 0.8, at=0.2), T("RADIO", 1350, 400, 120, "dark", at=0.4), bg="navy")

# DAY 2: HIGHER ----------------------------------------------------------
sc(2, "Day two. The water has swallowed the ground floor and is creeping up the second.",
   P("building", 960, 900, 1.2), P("wave", 960, 950, 1.5, in_="none", move=[960, 800]), T("DAY 2", 960, 200, 150, "red", at=0.3),
   chapter="Day 2: Higher")
sc(2, "Milo spots a hatch in the ceiling. The attic. Highest place in the building, right?",
   M(800, "pointup", "grin"), P("lock", 1300, 300, 0.8, at=0.3), T("ATTIC?", 1300, 550, 120, "dark", at=0.4))
sc(2, "Rosa grabs his arm. Never climb into a closed attic in a flood. If the water follows you up, there's no way out.",
   R(1200, "point", "angry", anim="shake"), M(700, "hold", "shock"), {"cross": [960, 400, 180], "at": 0.4}, voice=ROSA)
sc(2, "Official advice is clear: get to the highest level. Go onto the roof only if you must, and then signal for help.",
   P("house", 960, 900, 1.2), {"arrow": [[960, 700], [960, 380]], "color": "red", "at": 0.2}, T("ROOF = LAST", 960, 250, 120, "red", at=0.4))
sc(2, "Then signals. A white bed sheet with HELP in huge letters, hung from the top window for boats and helicopters.",
   P("flag", 960, 900, 1.3, text="HELP"), M(500, "point", "grin", at=0.3), T("HELP", 1400, 300, 150, "red", at=0.5))
sc(2, "And the whistle. Three short blasts means distress. A whistle carries further than a voice.",
   P("whistle", 960, 650, 1.2, anim="pulse"), T("3 BLASTS", 960, 280, 130, "red", at=0.3), M(1450, "hold", "neutral", at=0.2))

# DAY 3: WATER -----------------------------------------------------------
sc(3, "Day three. Here's the cruel joke of a flood. Water everywhere, and none of it safe to drink.",
   P("wave", 960, 1000, 1.4, in_="none"), P("drop", 960, 500, 1.2, at=0.2), {"cross": [960, 500, 170], "at": 0.4}, bg="grey",
   chapter="Day 3: Water")
sc(3, "Floodwater mixes sewage, fuel and rubbish. It carries germs, chemicals and hidden debris. Don't drink it. Don't wade in it.",
   P("barrel", 650, 880, 0.9), P("rat", 1000, 900, 0.8, at=0.2), P("pipe", 1350, 850, 0.8, at=0.4), T("DIRTY", 960, 250, 140, "red", at=0.5))
sc(3, "The radio says the city's tap water is now unsafe too. Boil water notice. The pipes may be broken and contaminated.",
   P("tv", 800, 750, 0.9), T("BOIL WATER", 1250, 300, 120, "red", at=0.3), bg="grey")
sc(3, "Plan at least one gallon per person per day, about four litres. Milo and Rosa have twelve litres.",
   P("bottle", 650, 850, 1.0), P("bottle", 850, 850, 1.0, at=0.1), P("bottle", 1050, 850, 1.0, at=0.2), T("4 L / DAY", 1400, 300, 120, "red", at=0.4))
sc(3, "Twelve litres, two people. That's a day and a half. Unless they make more safe water.",
   M(700, "think", "worried"), R(1250, "think", "neutral", at=0.2), T("1.5 DAYS", 960, 250, 140, "red", at=0.4, anim="pulse"))
sc(3, "Rosa has a camping stove. She uses it outside on the roof, never indoors. Stoves make carbon monoxide.",
   P("fire", 960, 900, 1.0), R(1350, "point", "neutral", at=0.2), T("OUTSIDE ONLY", 960, 250, 120, "red", at=0.4), voice=ROSA)
sc(3, "They catch rain in a clean pot, then bring it to a rolling boil for one full minute. Let it cool. Now it's drinkable.",
   P("pot", 960, 850, 1.1), P("cloud", 960, 300, 0.9, at=0.1), T("1 MIN", 1450, 350, 140, "red", at=0.4))

# DAY 4: THE SHOP -------------------------------------------------------
sc(4, "Day four. Food is low. There's a corner shop across the street. Only forty metres. Milo can swim.",
   P("building", 1350, 900, 0.9, text="SHOP"), M(600, "point", "grin"), T("40 M", 960, 300, 140, "dark", at=0.3),
   chapter="Day 4: Forty metres")
sc(4, "Rosa doesn't even look up. She just points at the water.",
   R(960, "point", "tired"), P("wave", 960, 1000, 1.2, in_="none", at=0.2))
sc(4, "Under that surface: open manholes, broken glass, sunken cars. You can't see your feet. One step can be a hole.",
   P("wave", 960, 950, 1.3, in_="none"), P("car", 600, 1020, 0.7, at=0.2), P("rubble", 1300, 1030, 0.8, at=0.4), T("HIDDEN", 960, 250, 140, "red", at=0.5), voice=ROSA)
sc(4, "And downed power lines can electrify floodwater.",
   P("powerline", 960, 900, 1.2, anim="shake"), T("LIVE WIRE", 960, 250, 140, "red", at=0.3, anim="pulse"), bg="grey")
sc(4, "A fridge drifts past. Then a garden shed. The current is faster than it looks.",
   P("barrel", 500, 880, 0.9, move=[1500, 880]), P("house", 1100, 880, 0.7, at=0.3, move=[1700, 880]), M(1550, "hold", "shock", at=0.2))

# DAY 5: THE BOAT -------------------------------------------------------
sc(5, "Day five. A motor. Engines, somewhere down the flooded street.",
   T("BRRRRM...", 960, 300, 120, "dark"), M(800, "pointup", "shock", at=0.2), chapter="Day 5: The boat")
sc(5, "Milo blows the whistle. Three blasts. Again. Rosa waves the torch from the window.",
   P("whistle", 700, 650, 1.0, anim="pulse"), P("torch", 1250, 650, 0.9, at=0.2, anim="shake"), T("3 BLASTS", 960, 250, 120, "red", at=0.4))
sc(5, "A rescue boat turns the corner and pulls up to the window.",
   P("ship", 960, 900, 1.1), D(1300, "wave", "happy", at=0.3), bg="sky")
sc(5, "Anyone hurt? Elderly first. Life jacket on before you step in. Slowly.",
   D(1200, "point", "neutral"), P("ship", 700, 900, 0.9), T("LIFE JACKET", 960, 250, 120, "red", at=0.4), voice=DEV)
sc(5, "That's Dev. Volunteer boat crew. He's been on the water for thirty hours.",
   D(1000, "hips", "tired"), T("30 H", 1450, 300, 130, "dark", at=0.3))
sc(5, "Rosa goes first. Milo hands down the bags, then climbs out of the window.",
   R(700, "hold", "worried"), M(1200, "run", "worried", at=0.2), P("ship", 960, 950, 1.0, at=0.1))
sc(5, "Dev steers wide of a bridge. Stay off bridges over fast water. Floods can wash them away without warning.",
   P("ship", 700, 900, 0.9, move=[1100, 900]), P("barrier", 1450, 880, 0.9, at=0.2), T("NO BRIDGES", 960, 250, 120, "red", at=0.4), voice=DEV)

# SHELTER ---------------------------------------------------------------
sc(5, "The boat drops them at a school on the hill. An emergency shelter. Cots, blankets, a queue for soup.",
   P("school", 960, 900, 1.2), M(500, "stand", "tired", at=0.2), R(1450, "stand", "tired", at=0.3), chapter="Day 5: The shelter")
sc(5, "Milo registers his name, so his family can find him. His mum gets a message an hour later.",
   P("clipboard", 800, 750, 1.0), P("phone", 1300, 750, 0.8, at=0.3), T("SAFE", 1300, 400, 130, "green", at=0.5))
sc(6, "Day six. A rumour spreads. The water is going down. People start packing to go home.",
   G(600, "point", "grin", extras=["hair"]), G(1000, "wave", "happy", extras=["cap"], at=0.2), M(1450, "hold", "confused", at=0.3))
sc(6, "Rosa shakes her head. Go home only when authorities say it's safe. Lower is not the same as safe.",
   R(1000, "point", "angry"), T("WAIT", 960, 250, 150, "red", at=0.3), voice=ROSA)
sc(9, "Day nine. A second storm. The river rises again and floods streets that were dry yesterday.",
   P("storm", 960, 550, 1.4, anim="shake"), T("DAY 9", 960, 200, 140, "red", at=0.2), bg="grey", chapter="Day 9: Again")
sc(9, "Flash floods can come with almost no warning. The people who stayed at the shelter are fine.",
   P("school", 960, 900, 1.0), P("wave", 960, 1030, 1.2, in_="none", at=0.2), T("STAYED = SAFE", 960, 250, 110, "red", at=0.4), bg="grey")
sc(14, "Day fourteen. Mosquitoes. The flood left a thousand puddles, and every puddle is a nursery.",
   P("lake", 960, 950, 1.0), T("BZZZ", 1300, 400, 130, "dark", at=0.2, anim="shake"), M(600, "facepalm", "tired", at=0.1),
   chapter="Day 14: Bites")
sc(14, "So: repellent with DEET or picaridin, long sleeves, and tip out every bucket of standing water.",
   P("bottle", 700, 850, 1.0), T("LONG SLEEVES", 1250, 280, 110, "red", at=0.3), T("NO PUDDLES", 1250, 420, 110, "dark", at=0.5))

# GOING HOME ------------------------------------------------------------
sc(21, "Day twenty one. Finally, the radio says it. Residents may return to their streets. In daylight. With care.",
   P("tv", 800, 750, 0.9), M(1300, "fist", "grin", at=0.2), T("GO HOME", 960, 250, 140, "green", at=0.4), bg="yellow",
   chapter="Day 21: Going home")
sc(21, "The street is unrecognisable. Mud on everything. A car on a fence. A line on every wall where the water stopped.",
   P("car", 700, 750, 0.9), P("barrier", 700, 900, 1.0), P("building", 1350, 900, 1.0, at=0.2), T("MUD", 960, 250, 140, "brown", at=0.4))
sc(21, "Before you go in, look. Cracks, a sagging roof, a smell of gas? Then you don't go in.",
   R(1200, "point", "neutral"), P("house", 650, 900, 1.0), P("magnifier", 900, 650, 0.8, at=0.3), voice=ROSA)
sc(21, "The power to the building has to stay off until an electrician checks it. Wet wiring can kill.",
   P("powerline", 700, 900, 1.0), T("OFF", 1300, 300, 160, "red", at=0.3), bg="yellow")
sc(21, "Inside, wear rubber boots, thick gloves and a mask. Flood mud hides germs and mould.",
   M(960, "present", "neutral"), T("BOOTS", 500, 300, 100, "red", at=0.2), T("GLOVES", 960, 220, 100, "red", at=0.4), T("MASK", 1420, 300, 100, "red", at=0.6))
sc(21, "Milo's flat is a swamp. His sofa is a sponge. His fridge floated for weeks.",
   M(960, "cry", "sad"), P("desk", 600, 900, 0.8, at=0.2), P("barrel", 1400, 880, 0.8, at=0.3), bg="grey")
sc(21, "Food that touched floodwater goes in the bin. When in doubt, throw it out.",
   P("tins", 800, 850, 1.0), P("bread", 1150, 820, 0.9, at=0.2), T("THROW IT OUT", 960, 250, 120, "red", at=0.4))

sc(23, "Day twenty three. Milo drags out a soaked carpet, and something goes straight through his trainer. A rusty nail.",
   M(900, "panic", "scream", anim="shake"), T("NAIL!", 1400, 300, 150, "red", at=0.3, anim="pulse"), chapter="Day 23: The nail")
sc(23, "Rosa is already there. Wash the wound with soap and clean water. Cover it. And when was your last tetanus shot?",
   R(1200, "hold", "worried"), P("bandage", 750, 700, 1.0, at=0.2), T("TETANUS?", 960, 250, 130, "red", at=0.4), voice=ROSA)
sc(23, "Milo has no idea. So it's straight to the clinic for a booster. Puncture wounds in floods need a doctor.",
   M(800, "hold", "tired"), P("building", 1350, 900, 0.9, text="CLINIC", at=0.2), T("SEE A DOCTOR", 960, 220, 110, "red", at=0.4))

# GENERATOR -------------------------------------------------------------
sc(30, "Day thirty. The power is still off in Milo's block. But the man next door has bought a petrol generator.",
   G(1100, "present", "smug", extras=["cap"], label="Neighbour"), P("barrel", 650, 880, 0.9, text="GEN", at=0.2),
   chapter="Day 30: The silent gas")
sc(30, "He runs it in his garage, door half open, to keep the rain off. It seems smart. It's deadly.",
   P("house", 960, 900, 1.1), P("barrel", 960, 880, 0.6, at=0.2, anim="shake"), T("GARAGE", 960, 250, 120, "dark", at=0.3), bg="grey")
sc(30, "Generators make carbon monoxide. You can't see it or smell it. Indoors, it builds up fast.",
   P("cloud", 960, 600, 1.2), T("CO", 960, 350, 200, "red", at=0.3, anim="pulse"), T("INVISIBLE", 960, 800, 110, "dark", at=0.5), bg="grey")
sc(30, "That evening, his wife knocks. Her husband has a headache, he's dizzy, and he's being sick.",
   G(1100, "cry", "worried", extras=["hair"], label="Neighbour"), M(600, "hold", "shock", at=0.2), bg="navy")
sc(30, "Headache, dizziness, nausea, near a generator: that can be carbon monoxide poisoning. Everyone out into fresh air. Now.",
   R(1200, "point", "angry", anim="shake"), T("FRESH AIR", 800, 250, 130, "red", at=0.3), voice=ROSA, bg="navy")
sc(30, "Milo calls emergency services. Nobody goes back inside until firefighters say so.",
   P("phone", 700, 750, 1.0), P("truck", 1300, 880, 1.0, at=0.3, text="FIRE"), bg="navy")
sc(30, "The neighbour recovers. The rule: generators only outside, far from doors and windows. Never in a garage.",
   P("barrel", 1500, 880, 0.8, text="GEN"), P("house", 600, 900, 0.9), {"arrow": [[800, 700], [1400, 700]], "color": "red", "at": 0.3}, T("FAR AWAY", 1000, 250, 130, "red", at=0.5))

# MOULD -----------------------------------------------------------------
sc(40, "Day forty. Little black dots on Milo's wall. In a week they're a cloud the size of a door.",
   P("building", 960, 900, 1.0), T(". . . :: ::", 960, 500, 120, "dark", at=0.2), T("MOULD", 960, 250, 150, "red", at=0.4),
   chapter="Day 40: The black wall")
sc(40, "Mould loves wet walls. It can trigger coughing, wheezing and asthma.",
   M(960, "cry", "tired"), T("COUGH", 1450, 350, 120, "red", at=0.3))
sc(40, "Soaked things that can't be cleaned go out. Carpets. Wet plasterboard. The mattress. Then fans and open windows.",
   P("fan", 700, 850, 1.0), P("rubble", 1300, 950, 0.9, at=0.2), T("DRY IT", 960, 250, 140, "red", at=0.4))
sc(40, "Hard surfaces get soap and water. And never mix bleach with ammonia or other cleaners. It makes toxic gas.",
   P("bottle", 700, 850, 1.0), P("bottle", 1250, 850, 1.0, at=0.2), {"cross": [960, 650, 200], "at": 0.4}, T("NEVER MIX", 960, 250, 130, "red", at=0.5))

# DAY 52-75: LIFE + NEXT STORM -----------------------------------------
sc(52, "Day fifty two. Rosa asks Milo one question: if it happens again tonight, what do you grab?",
   R(1200, "think", "neutral"), M(700, "hold", "confused", at=0.2), T("TONIGHT?", 960, 250, 130, "red", at=0.4), voice=ROSA,
   chapter="Day 52: The bag")
sc(52, "So Milo packs a go bag. Water and food for three days. Torch, batteries, radio, medicine, charger, whistle.",
   P("backpack", 960, 850, 1.2), P("torch", 600, 750, 0.7, at=0.2), P("battery", 1350, 750, 0.7, at=0.3), P("whistle", 1550, 650, 0.6, at=0.4))
sc(52, "And copies of his documents in a waterproof bag.",
   P("envelope", 960, 750, 1.1), T("WATERPROOF", 960, 300, 120, "red", at=0.3))
sc(52, "Rosa adds the last piece. A plan. Where we meet, who we text, which road leads uphill.",
   R(1000, "present", "smug"), P("clipboard", 600, 750, 0.9, at=0.2), {"arrow": [[1250, 800], [1600, 450]], "color": "red", "at": 0.4})

sc(60, "Day sixty. The radio says flood watch. Milo panics. Rosa explains the difference.",
   P("tv", 700, 750, 0.9), M(1300, "panic", "worried", at=0.2), T("WATCH", 960, 250, 140, "orange", at=0.3), chapter="Day 60: Watch or warning")
sc(60, "A flood watch means flooding is possible. Get ready. A flood warning means it's happening or about to. Act now.",
   T("WATCH = GET READY", 960, 300, 100, "orange"), T("WARNING = ACT NOW", 960, 480, 100, "red", at=0.4), R(1600, "pointup", "neutral", at=0.2), voice=ROSA, ground=False)

sc(75, "Day seventy five. Milo is driving home in heavy rain. A dip in the road ahead is full of water.",
   P("car", 700, 880, 1.0, move=[1000, 880]), P("cloud", 1300, 300, 1.0), P("wave", 1450, 1000, 0.9, in_="none", at=0.3), bg="grey",
   chapter="Day 75: The dip")
sc(75, "It doesn't look deep. Other cars made it. His foot hovers over the pedal.",
   M(960, "think", "worried"), P("stopwatch", 1450, 650, 0.9, at=0.2, anim="pulse"), bg="grey")
sc(75, "Then he remembers the levee. You can't see if the road under the water is still there.",
   P("wave", 960, 1000, 1.3, in_="none"), P("rubble", 960, 1050, 0.9, at=0.3), T("NO ROAD?", 960, 300, 130, "red", at=0.4), bg="grey")
sc(75, "Milo turns the car around and takes the long way. It costs him forty minutes. It costs him nothing else.",
   P("car", 1200, 880, 1.0, move=[600, 880]), T("TURN AROUND", 960, 250, 130, "red", at=0.3), T("+40 MIN", 1450, 450, 100, "dark", at=0.5))
sc(75, "Rule of thumb: if water covers the road, don't drive into it. Never drive around a barrier. A car is not a boat.",
   P("barrier", 960, 900, 1.2), P("car", 500, 880, 0.8, at=0.2), {"cross": [960, 600, 200], "at": 0.4}, bg="yellow")

# ENDING ----------------------------------------------------------------
sc(88, "Day eighty eight. Electricians sign off the building. The lights click on, and the street cheers.",
   P("building", 960, 900, 1.2), T("CLICK", 1400, 300, 140, "gold", at=0.3), M(500, "fist", "grin", at=0.2), bg="yellow",
   chapter="Day 88: Lights")
sc(88, "The boil notice is lifted. Until that official word, the one minute rule stayed in charge.",
   P("pot", 800, 850, 1.0), T("BOIL NOTICE: OFF", 1150, 300, 100, "green", at=0.3), bg="yellow")
sc(95, "Day ninety five. Dev from the rescue boat drops by. He's heard Milo is moving upstairs.",
   D(1250, "present", "happy"), M(700, "wave", "happy", at=0.2), chapter="Day 95: Dev")
sc(95, "Good choice. Keep that bag by the door. Most people I pulled out had nothing ready.",
   D(1100, "point", "grin"), P("backpack", 650, 880, 0.9, at=0.3), voice=DEV)
sc(100, "Day one hundred. Milo carries his last box up to the third floor. The river below is calm, brown and patient.",
   M(800, "hold", "happy"), P("lake", 1350, 950, 1.0, at=0.2), T("DAY 100", 960, 220, 170, "red", at=0.3, anim="pulse"), bg="yellow",
   chapter="Day 100: Upstairs")
sc(100, "Rosa knocks with a cake. Milo asks her how she knew all of this. She shrugs. Nurses read the boring leaflets.",
   R(1250, "present", "smug"), M(700, "hold", "grin", at=0.2), P("bread", 960, 750, 0.8, at=0.3), bg="yellow")

# RECAP ------------------------------------------------------------------
sc(None, "So, could you survive a flooding city? Go up, not out. Don't touch anything electric in water. No closed attics.",
   T("GO UP", 960, 200, 110, "red"), T("NO SWITCHES", 960, 320, 110, "red", at=0.2), T("NO ATTIC", 960, 440, 110, "red", at=0.4),
   M(960, "pointup", "neutral", y=950), bg="yellow", ground=False)
sc(None, "Six inches of moving water knocks you down. Twelve carries a car. Turn around, don't drown.",
   T("6 IN", 600, 300, 140, "red"), T("12 IN", 1300, 300, 140, "red", at=0.3), T("TURN AROUND", 960, 520, 110, "dark", at=0.5),
   M(960, "point", "neutral", y=950), bg="yellow", ground=False)
sc(None, "Boil water until officials say it's safe. Generators only outside. Boots, gloves, a mask, and a go bag by the door.",
   T("BOIL", 960, 200, 110, "dark"), T("GEN OUTSIDE", 960, 320, 110, "dark", at=0.2), T("GO BAG", 960, 440, 110, "red", at=0.4),
   M(960, "fist", "grin", y=950), bg="yellow", ground=False)
sc(None, "Next time: Milo is trapped in a tornado alley town. Day one to day one hundred. Subscribe so you don't miss it.",
   M(800, "point", "grin"), P("storm", 1350, 600, 1.0), T("NEXT: TORNADO ALLEY", 960, 220, 100, "red", at=0.3), bg="sky")

DESC = """3:12 a.m. The levee breaks and Milo wakes up standing in floodwater. With his neighbour Rosa, a retired nurse, he has to go up, signal for help, make safe water — and then survive the weeks after the flood: a rusty nail, a generator in a garage, black mould and a road that might not be there. Day 1 to Day 100.

The story is fiction; the survival facts are real. This is not professional safety training — in a real emergency, call your local emergency number and follow official instructions.

Sources:
Ready.gov (FEMA) — Floods: before, during and after https://www.ready.gov/floods
NOAA/NWS — Turn Around Don't Drown (6 in knocks you down, 12 in carries cars) https://www.weather.gov/safety/flood-turn-around-dont-drown
CDC — Floods: safety, tetanus, mosquitoes, cleanup https://www.cdc.gov/floods/safety/index.html
CDC — Make water safe in an emergency (boiling 1 minute) https://www.cdc.gov/water-emergency/about/how-to-create-safe-drinking-water.html

#survival #story #animation

Next episode: Trapped in Tornado Alley"""

ep = {
    "id": "ep007",
    "title": "Trapped in a Flooding City: Day 1 to 100",
    "voice": "am_michael",
    "speed": 1.0,
    "hook": "3:12 a.m. Milo steps out of bed into floodwater.",
    "description": DESC,
    "tags": ["survival story", "flood survival", "flooding city", "day 1 to 100", "100 days", "flood safety",
             "survival story animated", "how to survive a flood", "turn around dont drown", "milo survives", "animated story"],
    "thumbnail": {"bg": "sky", "text": "DAY 1|FLOODED", "size": 200, "color": "red",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["glasses"], "shirt": "yellow"},
                  "guy_x": 1450, "items": [{"prop": "building", "x": 560, "y": 900, "s": 1.3},
                                           {"prop": "wave", "x": 760, "y": 1000, "s": 1.6}]},
    "shorts": [],
    "scenes": S,
}

# Shorts: cold open + the generator moment (start estimated from narration length: am_michael ~2.8 words/s + 0.28 s gap, measured with --check 2026-11-18)
t = 0.0
starts = []
for s in S:
    starts.append(t)
    t += len(s["say"].split()) / 2.8 + 0.28
# 386 s = real start of "Day 30: The silent gas" from the TTS timeline (--check 2026-11-18)
i_co = next(i for i, s in enumerate(S) if s.get("chapter") == "Day 30: The silent gas")
ep["shorts"] = [
    {"start": 0, "dur": 35, "top": "3 a.m. The floor is under water.", "title": "Could You Survive a City Flood at 3 A.M.?"},
    {"start": 386 if len(S) == 93 else int(starts[i_co]), "dur": 40, "top": "The flood is over. This is still deadly.", "title": "The Flood Danger Nobody Sees Coming"},
]

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = os.path.join(root, "cloud", "queue", "milo", "ep007.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(ep, open(out, "w"), indent=1, ensure_ascii=False)
    words = sum(len(s["say"].split()) for s in S)
    over = [i for i, s in enumerate(S) if len(s["say"].split()) > 30]
    print(out, len(S), "scenes", words, "words", f"~{t / 60:.1f} min est", "title len", len(ep["title"]), "over30", over)

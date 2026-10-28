"""Milo Survives ep002: 100 days on a desert island — real survival priorities (water, shade, signals, first aid)."""
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


def R(x, pose="stand", face="neutral", look=-1, **kw):  # Rosa, the skipper
    return G(x, pose, face, look, extras=["bun", "cap"], shirt="teal", **kw)


ROSA = "af_bella"
RADIO = "bm_george"
S = []


def sc(day, say, *items, **kw):
    d = {"say": say, "items": list(items), "bg": kw.pop("bg", "sky")}
    if day is not None:
        d["day"] = day
    d.update(kw)
    S.append(d)


BEACH = lambda: P("island", 960, 960, 2.4, in_="none")  # noqa: E731

# COLD OPEN ---------------------------------------------------------------
sc(1, "Six forty in the morning, somewhere in the South Pacific. Your boat is upside down. And the only land you can see is a strip of sand.",
   P("wave", 960, 980, 2.4), P("ship", 700, 860, 0.5, anim="shake", move=[700, 960]), P("island", 1500, 760, 0.6, at=0.6),
   T("DAY 1", 960, 300, 190, "red", at=0.15, anim="pulse"), cam={"from": [960, 540, 1.15], "to": [1100, 600, 1.0]}, ground=False)
sc(1, "No phone signal. No fresh water. Nobody knows exactly where you are. Can you survive one hundred days here?",
   BEACH(), M(760, "panic", "scream", anim="shake"), {"cross": [1300, 420, 70], "at": 0.2}, P("phone", 1300, 520, 0.8, at=0.1),
   T("100 DAYS?", 1350, 260, 130, "red", at=0.6))
sc(1, "Milo is about to find out. He just crawled out of the surf, still in his yellow raincoat, and he is not alone.",
   BEACH(), P("wave", 960, 1040, 2.4), M(700, "cry", "tired", walk=True, move=[880, 900]), R(1350, "facepalm", "tired", at=0.5, label="Rosa"))
sc(1, "Okay. Okay. The boat is gone, the radio is gone, and I think I swallowed half the ocean.",
   BEACH(), R(1150, "hold", "worried"), P("ship", 1650, 980, 0.4, anim="shake", at=0.3), M(600, "shrug", "worried", at=0.1), voice=ROSA)
sc(1, "That's Rosa, the skipper. She has one dry bag. Inside: a lighter, a plastic sheet, a small pot, and one bottle of water.",
   P("backpack", 960, 800, 1.3), P("pot", 520, 600, 0.6, at=0.25), P("bottle", 820, 560, 0.7, text="1L", at=0.4),
   {"box": [1150, 420, 260, 150], "color": "white", "at": 0.55},
   T("SHEET", 1280, 500, 54, "dark", at=0.6), P("fire", 1600, 640, 0.6, at=0.75), bg="yellow", ground=False, chapter="Day 1: The rule of three")

# PART 1: PRIORITIES ------------------------------------------------------
sc(1, "Survival experts use a simple rule of three. You can last about three minutes without air,",
   T("RULE OF 3", 960, 200, 140, "red"), T("3 MINUTES", 600, 500, 90, "dark", at=0.5), T("AIR", 600, 600, 70, "blue", at=0.6),
   M(1500, "pointup", "neutral", look=-1, at=0.2), bg="yellow")
sc(1, "about three hours in harsh weather without shelter, three days without water, and three weeks without food.",
   T("3 HOURS = SHELTER", 960, 360, 80, "orange", at=0.05), T("3 DAYS = WATER", 960, 500, 80, "blue", at=0.35),
   T("3 WEEKS = FOOD", 960, 640, 80, "green", at=0.65), bg="yellow", ground=False)
sc(1, "These are rough numbers, not a countdown. But they tell you the order. Shelter and water first. Food comes way later.",
   {"arrow": [[400, 500], [800, 500]], "at": 0.3}, P("shelter", 300, 700, 0.8), P("bottle", 1000, 680, 0.9, at=0.4),
   P("coconut", 1500, 700, 1.0, at=0.7), T("LATER", 1500, 460, 70, "grey", at=0.8), bg="yellow")
sc(1, "So Milo does what every movie hero does first. He tries to drink the ocean.",
   BEACH(), P("wave", 960, 1040, 2.4), M(900, "hold", "happy", at=0), T("?!", 1250, 400, 170, "red", at=0.6))
sc(1, "Milo, stop! Salt water makes you thirstier. Spit it out!",
   BEACH(), R(1250, "point", "angry", anim="shake"), M(700, "panic", "shock", at=0.3), voice=ROSA)
sc(1, "She's right. According to the U.S. ocean agency NOAA, your kidneys can only make urine that is less salty than sea water.",
   P("wave", 960, 980, 2.4), T("NOAA", 960, 220, 120, "blue"), {"box": [560, 380, 800, 260], "color": "white", "at": 0.3},
   T("SEA WATER = TOO SALTY", 960, 520, 70, "red", at=0.5), ground=False, bg="sea")
sc(1, "So to get rid of all that salt, your body has to pee out more water than you drank. You end up drier than before.",
   M(500, "cry", "sad"), P("bottle", 1000, 760, 1.0, text="IN", at=0.2), {"arrow": [[1080, 640], [1300, 640]], "at": 0.4},
   P("bottle", 1450, 760, 1.4, text="OUT", color="red", at=0.55), bg="yellow")
sc(1, "Rule one on any island. Never drink sea water. Not a sip, not mixed in, not when you're desperate.",
   P("wave", 960, 960, 2.0), {"cross": [960, 520, 220], "at": 0.3}, T("RULE 1", 960, 180, 130, "red", at=0.1), ground=False, bg="yellow")

# PART 2: SHADE ------------------------------------------------------------
sc(2, "Day two. The sun is the first thing trying to kill them. By noon the sand is hot enough to hurt bare feet.",
   P("sun", 1500, 260, 1.6, anim="pulse"), BEACH(), M(700, "panic", "tired", anim="shake"), P("thermo", 1100, 820, 1.0, color="red", at=0.5),
   chapter="Day 2: Shade")
sc(2, "Sweating in direct sun can drain a lot of water from your body every hour. So shade is not comfort. Shade is water you don't lose.",
   P("sun", 1550, 260, 1.4), M(600, "stand", "tired"), P("bottle", 1000, 760, 1.0, text="-", move=[1000, 820], at=0.3),
   T("SHADE = WATER", 1100, 420, 100, "blue", at=0.6))
sc(2, "Milo and Rosa lean driftwood against a palm, lay palm fronds on top, and crawl under during the hottest hours.",
   BEACH(), P("palm", 600, 900, 1.2), P("shelter", 1100, 900, 1.2, at=0.3), M(1500, "hold", "neutral", look=-1, at=0.6))
sc(2, "They move at dawn and dusk, when it's cool. In the middle of the day, they rest. Boring? Yes. Smart? Also yes.",
   P("sun", 400, 300, 0.9), P("cloud", 900, 260, 0.9, at=0.2), P("shelter", 1100, 900, 1.0), M(1100, "stand", "tired", s=0.7, at=0.5),
   T("REST 11 to 3", 1500, 420, 80, "dark", at=0.6))
sc(2, "And they build it above the line of dried seaweed on the sand. That line shows how high the tide comes.",
   BEACH(), P("wave", 960, 1040, 2.4), {"arrow": [[600, 820], [1400, 820]], "color": "green", "at": 0.3},
   T("HIGH TIDE LINE", 960, 700, 70, "green", at=0.4), P("shelter", 1550, 860, 0.8, at=0.6))

# PART 3: WATER ------------------------------------------------------------
sc(3, "Day three. The bottle is empty. Milo has a headache, his lips are cracked, and his pee is dark.",
   T("EMPTY", 960, 250, 120, "red"), P("bottle", 600, 820, 1.0, color="grey"), M(1200, "facepalm", "tired", at=0.3),
   chapter="Day 3: Water", bg="yellow")
sc(3, "Those are classic warning signs of dehydration. Headache, dizziness, dark urine, feeling confused. Water is now the only job.",
   T("HEADACHE", 600, 360, 70, "red", at=0.1), T("DIZZY", 1300, 360, 70, "red", at=0.3), T("DARK PEE", 600, 560, 70, "red", at=0.5),
   T("CONFUSED", 1300, 560, 70, "red", at=0.7), M(960, "cry", "confused", s=0.8), bg="yellow")
sc(3, "Then, at four in the afternoon, the sky turns grey.",
   P("cloud", 700, 260, 1.4), P("cloud", 1250, 300, 1.6, at=0.3), BEACH(), M(960, "pointup", "shock"), bg="grey")
sc(3, "The sheet! Spread the sheet! Every drop counts!",
   P("storm", 960, 240, 1.2), R(600, "panic", "scream"), M(1300, "run", "worried", at=0.3), voice=ROSA, bg="grey")
sc(3, "They stretch the plastic sheet between two sticks so it sags in the middle, and the rain runs into the pot.",
   P("storm", 960, 200, 1.0), {"box": [700, 520, 520, 40], "color": "white"}, P("pot", 960, 900, 0.9, at=0.3),
   {"arrow": [[960, 580], [960, 760]], "color": "blue", "at": 0.5}, bg="grey")
sc(3, "Fresh rain caught on a clean surface is one of the best water sources a castaway can get.",
   P("pot", 960, 900, 1.2), T("RAIN = GOLD", 960, 300, 130, "blue", at=0.3), M(1500, "fist", "grin", look=-1, at=0.5))
sc(4, "Day four. They find green coconuts. The water inside a young coconut is safe to drink, and it helps. In moderation.",
   P("palm", 600, 900, 1.3), P("coconut", 1100, 860, 1.4, at=0.3), M(1500, "hold", "happy", look=-1, at=0.5))
sc(4, "But a stream they find in the jungle is a different story. Clear water can still carry germs you can't see.",
   P("wave", 960, 900, 1.4, color="blue"), P("magnifier", 1100, 640, 1.1, at=0.3), T("GERMS?", 1400, 360, 100, "red", at=0.6),
   M(500, "think", "worried"))
sc(4, "So they boil it. The CDC says bring water to a rolling boil for one minute, or three minutes at high altitude.",
   P("pot", 960, 900, 1.4), T("CDC", 960, 200, 110, "blue"), T("1 MINUTE", 960, 380, 120, "red", at=0.4),
   P("stopwatch", 1500, 800, 1.0, at=0.6))
sc(4, "That lighter in the dry bag just became the most valuable object on the island.",
   P("fire", 960, 900, 1.6), T("MVP", 960, 300, 150, "gold", at=0.4), R(500, "hips", "smug", look=1, at=0.2))

# PART 4: SIGNALS ----------------------------------------------------------
sc(5, "Day five. A plane. Tiny, very high, very fast. Milo jumps and waves and screams. The plane does not care.",
   P("plane", 600, 240, 0.5, move=[1500, 220]), BEACH(), M(960, "wave", "scream", anim="bob"), chapter="Day 5: Be seen")
sc(5, "From the air, one person on a beach looks like a dot. You have to make the island itself shout for help.",
   P("island", 960, 640, 1.2), {"ring": [960, 560, 40], "at": 0.3}, T("THIS IS YOU", 960, 300, 90, "red", at=0.5), ground=False)
sc(5, "Rescue groups like AdventureSmart teach this: three of anything means distress. Three fires, three whistle blasts, three piles of rocks.",
   P("fire", 500, 860, 0.9), P("fire", 960, 860, 0.9, at=0.25), P("fire", 1420, 860, 0.9, at=0.5), T("3 = HELP", 960, 300, 150, "red", at=0.65),
   bg="yellow")
sc(5, "So they build three fire piles in a triangle, ready to light. Dry wood underneath, green leaves on top for thick smoke.",
   BEACH(), P("fire", 700, 900, 0.7), P("fire", 1220, 900, 0.7, at=0.2), P("fire", 960, 760, 0.7, at=0.4),
   T("SMOKE BY DAY", 600, 300, 70, "dark", at=0.6), T("FLAME BY NIGHT", 1350, 300, 70, "orange", at=0.75))
sc(6, "Day six. Huge letters on the sand. S O S, made from dark rocks and seaweed so it stands out against the white beach.",
   P("sos", 960, 820, 2.0), M(1650, "present", "grin", look=-1, at=0.4))
sc(6, "Big letters, sharp contrast, straight lines. Nature doesn't make straight lines, so pilots notice them.",
   P("sos", 960, 820, 1.6), {"arrow": [[300, 300], [700, 600]], "at": 0.3}, P("plane", 260, 260, 0.4, at=0.2),
   T("STRAIGHT LINES", 1300, 330, 80, "red", at=0.6))
sc(6, "And Milo's secret weapon? His glasses case has a tiny mirror. A flash of sunlight can be seen much farther away than you can shout.",
   P("mirror", 700, 820, 1.4), {"arrow": [[780, 700], [1500, 260]], "color": "yellow", "at": 0.4}, P("plane", 1600, 240, 0.5, at=0.5),
   M(400, "point", "smug", at=0.2))

# PART 5: FIRST AID --------------------------------------------------------
sc(9, "Day nine. Rosa slips on the rocks. Sharp coral slices her shin.",
   R(960, "cry", "scream", anim="shake"), P("wave", 960, 1040, 2.2), T("OUCH", 1400, 380, 140, "red", at=0.3), chapter="Day 9: Small cuts, big danger")
sc(9, "It's just a scratch. I'll rinse it in the sea and forget about it.",
   R(800, "shrug", "smug"), P("wave", 1300, 960, 1.2, at=0.2), {"cross": [1300, 760, 90], "at": 0.7}, voice=ROSA)
sc(9, "On an island, small cuts are a big deal. Sea water and sand can carry bacteria, and there's no doctor for a hundred miles.",
   P("magnifier", 960, 700, 1.3), T("BACTERIA", 960, 300, 110, "red", at=0.3), M(1500, "think", "worried", look=-1, at=0.5), bg="yellow")
sc(9, "So Milo cleans the cut with boiled water that has cooled down, and covers it with a clean strip of his raincoat lining.",
   P("pot", 600, 900, 0.9), {"arrow": [[700, 650], [1000, 650]], "at": 0.3}, P("bandage", 1200, 760, 1.4, at=0.5),
   M(1600, "hold", "neutral", look=-1, at=0.2))
sc(10, "Then they watch it every day. Spreading redness, heat, pus or a fever are signs of infection that need real medical help.",
   T("REDNESS", 560, 360, 70, "red"), T("HEAT", 1360, 360, 70, "red", at=0.2), T("PUS", 560, 560, 70, "red", at=0.4),
   T("FEVER", 1360, 560, 70, "red", at=0.6), R(960, "stand", "worried", s=0.8), bg="yellow")
sc(12, "Day twelve. The cut is healing. Rosa owes Milo one. She does not say so out loud.",
   R(700, "hips", "smug"), M(1200, "shrug", "grin", look=-1, at=0.3), P("bandage", 960, 520, 0.8, at=0.5))

# PART 6: FOOD -------------------------------------------------------------
sc(14, "Day fourteen. Their stomachs are loud. And the jungle is full of bright berries.",
   P("palm", 500, 900, 1.2), {"box": [1100, 560, 300, 200], "color": "green"}, T("BERRIES?", 1250, 460, 80, "purple", at=0.4),
   M(800, "think", "happy"), chapter="Day 14: Food")
sc(14, "This is where many survival stories go wrong. Never eat a plant, berry or mushroom you can't identify for certain.",
   {"cross": [1250, 660, 160], "at": 0.2}, T("UNKNOWN = NO", 960, 260, 120, "red", at=0.4), M(500, "panic", "shock", at=0.5), bg="yellow")
sc(14, "Some poisonous plants look exactly like safe ones. And remember the rule of three. You can go weeks without food. Poison can end things in hours.",
   T("WEEKS", 600, 420, 120, "green"), T("vs", 960, 420, 80, "dark", at=0.3), T("HOURS", 1320, 420, 120, "red", at=0.5),
   M(960, "shrug", "worried", s=0.8, at=0.6), bg="yellow")
sc(15, "So they stick to the sea. Rosa knows fish. They wade in shallow water at low tide and trap small fish in a ring of rocks.",
   P("wave", 960, 980, 2.0), {"ring": [960, 860, 150], "at": 0.3}, R(1500, "point", "happy"), ground=False)
sc(15, "Crabs at night, too. Everything gets cooked all the way through on the fire. Raw seafood can make you seriously sick.",
   P("crab", 700, 880, 1.2, anim="bob"), P("fire", 1250, 900, 1.0, at=0.3), T("COOK IT", 1250, 400, 110, "orange", at=0.55))
sc(15, "This crab is looking at me. I feel bad. I'm still eating it.",
   P("crab", 1300, 880, 1.5, anim="shake"), M(600, "think", "confused"), T("...", 1300, 520, 120, "dark", at=0.6))

# PART 7: STORM ------------------------------------------------------------
sc(21, "Day twenty one. The wind changes. Clouds pile up on the horizon like a dark wall.",
   P("storm", 960, 300, 2.0), P("wave", 960, 1000, 2.4, anim="shake"), chapter="Day 21: The storm", bg="grey", ground=False)
sc(21, "Grab the pot, the sheet, the lighter. Everything that matters goes to high ground, right now!",
   R(700, "run", "scream", walk=True, move=[1100, 900]), P("pot", 1500, 860, 0.7, at=0.3), P("storm", 960, 240, 1.0), voice=ROSA, bg="grey")
sc(21, "In a tropical storm, the danger is not just wind. It's water. Waves and storm surge can wash over a low beach.",
   P("wave", 960, 860, 2.4, anim="shake"), {"arrow": [[600, 760], [1400, 560]], "color": "red", "at": 0.3}, T("STORM SURGE", 960, 260, 110, "red", at=0.5),
   ground=False, bg="grey")
sc(21, "They wait it out behind a big rock on the highest point of the island, away from tall trees that can drop branches and coconuts.",
   {"box": [700, 620, 360, 280], "color": "grey"}, M(1100, "cry", "worried", s=0.8), R(1250, "cry", "worried", s=0.8, at=0.1),
   P("palm", 300, 900, 0.9, anim="shake"), P("coconut", 300, 480, 0.6, move=[340, 880], at=0.5), bg="grey")
sc(22, "Morning. The shelter is gone. The SOS is half buried. But the lighter is dry, and they're both alive.",
   P("sun", 1550, 260, 1.0), BEACH(), P("sos", 960, 820, 1.2, color="grey"), M(600, "facepalm", "tired"), R(1350, "hips", "tired", at=0.4))

# PART 8: THE LONG MIDDLE --------------------------------------------------
sc(30, "Day thirty. Here's a part nobody shows in movies. The hardest enemy now is not the island. It's the boredom and the fear.",
   P("calendar", 960, 820, 1.4, text="DAY 30"), M(500, "think", "sad", at=0.3), T("BORED. SCARED.", 1400, 360, 80, "dark", at=0.6),
   chapter="Day 30: The mind")
sc(30, "Survival trainers say a routine helps. Water at dawn. Fishing at low tide. Fix the signals. Rest at noon. Fire at dusk.",
   T("DAWN: WATER", 960, 260, 70, "blue"), T("LOW TIDE: FISH", 960, 380, 70, "teal", at=0.2), T("MORNING: SIGNALS", 960, 500, 70, "red", at=0.4),
   T("NOON: REST", 960, 620, 70, "orange", at=0.6), T("DUSK: FIRE", 960, 740, 70, "orange", at=0.8), bg="yellow", ground=False)
sc(30, "Milo scratches a line on a palm trunk every morning. It's a calendar. It's also proof that he's still in charge.",
   P("palm", 960, 900, 1.6), T("IIII IIII IIII", 960, 620, 60, "dark", at=0.3), M(1400, "point", "neutral", look=-1, at=0.2))
sc(38, "Rosa, rate my sand castle. Be honest. Actually no, be nice.",
   {"box": [1100, 700, 300, 200], "color": "tan"}, M(700, "present", "grin"), R(1600, "think", "smug", at=0.4), T("6/10", 1600, 380, 100, "dark", at=0.7))
sc(38, "Six out of ten. The tower is leaning.",
   R(1300, "hips", "smug"), M(700, "cry", "sad", at=0.3), T("6/10", 960, 300, 140, "red", at=0.1), voice=ROSA)
sc(47, "Day forty seven. While Milo is wading for fish, a grey fin cuts through the water.",
   P("fin", 1200, 900, 1.6), P("wave", 960, 980, 2.4), M(600, "panic", "scream", anim="shake", at=0.4), chapter="Day 47: Fin", ground=False)
sc(47, "Calm. Don't splash. Back out slowly, face it, and get out of the water.",
   P("fin", 1300, 900, 1.2), R(500, "point", "worried", look=1), M(900, "stand", "worried", move=[700, 900], at=0.3), voice=ROSA, ground=False)
sc(47, "Shark bites are very rare. But wildlife experts advise avoiding murky water and swimming at dawn and dusk, when many sharks feed.",
   T("VERY RARE", 960, 260, 110, "green"), T("AVOID DAWN + DUSK", 960, 480, 90, "red", at=0.4), P("fin", 960, 860, 1.0, at=0.6), bg="yellow")
sc(47, "From that day on, Milo fishes only in the shallows, in daylight, and never alone.",
   P("wave", 960, 980, 2.0), M(700, "hold", "neutral"), R(1250, "hold", "neutral", at=0.2), T("SHALLOW. DAYLIGHT. TOGETHER.", 960, 300, 70, "dark", at=0.5),
   ground=False)

# PART 9: HEAT ILLNESS ----------------------------------------------------
sc(61, "Day sixty one. A brutal heat wave. No rain for a week. Now Rosa is the one who looks wrong.",
   P("sun", 1500, 260, 1.8, anim="pulse"), R(800, "cry", "tired"), P("thermo", 1200, 800, 1.0, color="red", at=0.4), chapter="Day 61: Heat")
sc(61, "She stopped sweating. Her skin is hot and dry. She's talking nonsense. Those can be signs of heat stroke, a real emergency.",
   T("HOT, DRY SKIN", 960, 300, 80, "red"), T("NO SWEAT", 960, 430, 80, "red", at=0.3), T("CONFUSED", 960, 560, 80, "red", at=0.6),
   R(400, "cry", "confused", s=0.8), bg="yellow")
sc(61, "The CDC's advice is to cool the person fast. Milo drags her into deep shade, soaks her clothes, and fans her with a palm frond.",
   P("shelter", 700, 900, 1.2), R(700, "stand", "tired", s=0.6), M(1200, "hold", "worried", look=-1, at=0.3), P("fan", 1500, 700, 0.9, at=0.5),
   T("COOL HER DOWN", 1300, 300, 80, "blue", at=0.6))
sc(62, "By night, she's sitting up, sipping coconut water. She's okay. They ration every drop after that.",
   P("fire", 960, 900, 0.9), R(600, "stand", "tired"), M(1300, "stand", "happy", look=-1, at=0.3), P("coconut", 960, 560, 0.7, at=0.5))

# PART 10: THE MISS -------------------------------------------------------
sc(88, "Day eighty eight. A ship. A real ship, on the horizon.",
   P("ship", 1500, 700, 0.4, anim="bob"), P("wave", 960, 900, 2.4), M(600, "pointup", "shock", at=0.3), chapter="Day 88: So close", ground=False)
sc(88, "The fires! Light the fires! Where is the lighter?",
   R(700, "panic", "scream", anim="shake"), M(1200, "panic", "scream", at=0.2), P("ship", 1650, 640, 0.3), voice=ROSA)
sc(88, "But the wood is damp from the night. By the time the smoke rises, the ship is gone.",
   P("fire", 960, 900, 0.6), P("ship", 1500, 700, 0.3, move=[1950, 700]), M(500, "cry", "cry", at=0.4), T("GONE", 1300, 360, 140, "dark", at=0.7))
sc(88, "Lesson learned the hard way. Signal fires only work if they're ready in seconds. Keep dry tinder covered and the lighter in your pocket.",
   T("READY IN SECONDS", 960, 260, 100, "red"), P("fire", 700, 860, 1.0, at=0.3), {"box": [1150, 640, 300, 220], "color": "tan", "at": 0.5},
   T("DRY TINDER", 1300, 590, 50, "dark", at=0.6), bg="yellow")
sc(89, "From now on, Milo sleeps with the lighter. Rosa covers the tinder with the plastic sheet every single night.",
   P("fire", 960, 900, 0.6), M(600, "stand", "tired", s=0.9), R(1300, "hold", "neutral", at=0.3), P("stopwatch", 1600, 520, 0.7, at=0.6))

# PART 11: RESCUE ---------------------------------------------------------
sc(99, "Day ninety nine. A low humming sound from the north. Milo knows that sound.",
   P("cloud", 600, 260, 1.0), P("heli", 1650, 280, 0.5, at=0.3, anim="bob"), M(800, "think", "shock", at=0.1), chapter="Day 99: The sound")
sc(99, "Rosa lights all three fires in under a minute. Green leaves on top. Three thick columns of smoke.",
   P("fire", 600, 900, 1.0), P("fire", 960, 900, 1.0, at=0.2), P("fire", 1320, 900, 1.0, at=0.4),
   P("cloud", 600, 500, 0.8, color="grey", at=0.5), P("cloud", 960, 460, 0.8, color="grey", at=0.6), P("cloud", 1320, 500, 0.8, color="grey", at=0.7))
sc(99, "Milo aims the mirror. Flash. Flash. Flash. Three flashes, again and again.",
   P("mirror", 600, 820, 1.4, anim="pulse"), {"arrow": [[700, 700], [1500, 300]], "color": "yellow", "at": 0.3}, P("heli", 1600, 280, 0.6, at=0.4),
   T("FLASH x3", 1100, 640, 90, "gold", at=0.6))
sc(99, "The helicopter turns. It circles once. It's coming down.",
   P("heli", 960, 260, 1.0, move=[960, 480], anim="bob"), BEACH(), M(500, "wave", "grin", s=0.8, anim="bob"), R(1450, "wave", "happy", s=0.8, anim="bob"))
sc(100, "Coast guard. We saw your smoke and the S O S. Is anyone hurt?",
   P("heli", 1300, 600, 1.1), G(900, "point", "neutral", look=1, extras=["hardhat"], shirt="orange", label="Coast guard"), voice=RADIO)
sc(100, "Day one hundred. Sunburned, skinny, and very alive.",
   M(700, "fist", "grin"), R(1250, "fist", "happy"), T("DAY 100", 960, 280, 180, "red", anim="pulse", at=0.2), P("sun", 1650, 260, 0.8))

# RECAP --------------------------------------------------------------------
sc(None, "So, could you survive one hundred days on a desert island? Here's what kept Milo and Rosa alive.",
   T("WHAT WORKED", 960, 220, 130, "red"), M(1500, "present", "happy", look=-1, at=0.3), bg="yellow", chapter="What kept them alive")
sc(None, "One. Never drink sea water. Two. Shade before anything, because sweat is water you lose.",
   T("1. NO SEA WATER", 960, 380, 90, "blue"), T("2. SHADE FIRST", 960, 540, 90, "orange", at=0.5), bg="yellow", ground=False)
sc(None, "Three. Catch rain, and boil other water for a full minute. Four. Three of anything means help, and signals must be ready in seconds.",
   T("3. RAIN + BOIL 1 MIN", 960, 380, 90, "blue"), T("4. THREES = HELP", 960, 540, 90, "red", at=0.5), bg="yellow", ground=False)
sc(None, "Five. Treat small cuts like big problems. And never eat anything you can't identify. Hunger is slow. Poison is fast.",
   T("5. CLEAN EVERY CUT", 960, 380, 90, "green"), T("6. UNKNOWN FOOD = NO", 960, 540, 90, "red", at=0.5), bg="yellow", ground=False)
sc(None, "Next time, Milo wakes up somewhere much colder. One hundred days in Antarctica. Subscribe so you don't miss it.",
   P("thermo", 700, 860, 1.2, color="blue"), T("NEXT: ANTARCTICA", 1150, 300, 100, "blue", at=0.2), M(1400, "panic", "shock", look=-1, at=0.5),
   T("-40", 700, 420, 110, "blue", at=0.6), bg="sky")

script = {
    "id": "ep002",
    "title": "Can You Survive 100 Days on a Desert Island?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Milo and Rosa wash up on a tiny island in the South Pacific with one dry bag. Can they last 100 days? "
        "A hand-drawn survival story with real survival facts: why you can never drink sea water, why shade saves water, "
        "how to catch rain and boil water, the 'three of anything' distress signal, treating small cuts, avoiding unknown plants, "
        "heat stroke warning signs, and staying ready to signal.\n\n"
        "The story is fiction; the survival facts are real. This is not medical advice — in a real emergency, contact emergency services.\n\n"
        "Next episode: 100 Days in Antarctica.\n\n"
        "Sources:\n"
        "NOAA — Why can't people drink seawater? https://oceanservice.noaa.gov/facts/drinksw.html\n"
        "CDC — Boil water advisory (rolling boil 1 minute) https://www.cdc.gov/natural-disasters/psa-toolkit/boil-water-advisory.html\n"
        "CDC — Heat-related illnesses https://www.cdc.gov/niosh/heat-stress/about/illnesses.html\n"
        "AdventureSmart — Communication & signalling https://www.adventuresmart.ca/communication-signaling/\n\n"
        "#survival #desertisland #animation #storytime"
    ),
    "tags": "survival, desert island, 100 days, survival story, animated story, how to survive, castaway, survival tips, milo survives, island survival",
    "thumbnail": {"bg": "sky", "text": "DAY 99…|NO WATER", "size": 200, "color": "red",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["glasses"]}, "guy_x": 1450,
                  "items": [{"prop": "island", "x": 1300, "y": 1000, "s": 2.2}, {"prop": "fin", "x": 500, "y": 980, "s": 1.6}]},
    "scenes": S,
}
# Milo's coat on the thumbnail
script["thumbnail"]["guy"]["shirt"] = "yellow"

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep002.json")
json.dump(script, open(out, "w"), indent=1)
words = sum(len(s["say"].split()) for s in S)
print(out, len(S), "scenes", words, "words")

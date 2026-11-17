"""Milo Survives ep006: trapped in the Sahara after a plane crash, Day 1 to Day 100 — real desert-survival facts.
Written by the channel watchdog on 2026-11-17 because cloud/queue/milo was empty (worker: queue_empty).
Output: cloud/queue/milo/ep006.json (the laptop maker renders + uploads it)."""
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


def A(x, pose="stand", face="neutral", look=-1, **kw):  # Amira, the pilot
    return G(x, pose, face, look, extras=["bun", "cap"], shirt="navy", label="Amira", **kw)


AMIRA = "bf_isabella"
RADIO = "bm_george"
S = []


def sc(day, say, *items, **kw):
    d = {"say": say, "items": list(items), "bg": kw.pop("bg", "tan")}
    if day is not None:
        d["day"] = day
    d.update(kw)
    S.append(d)



# COLD OPEN ---------------------------------------------------------------
sc(1, "Two forty one p.m. Somewhere over the Sahara. The engine coughs. Then it stops. And the ground is coming up fast.",
   P("plane", 960, 600, 1.4, anim="shake", move=[960, 950]), T("DAY 1", 960, 220, 190, "red", at=0.15, anim="pulse"),
   cam={"from": [960, 540, 1.25], "to": [960, 600, 1.0]}, bg="yellow", chapter="Day 1: The crash")
sc(1, "A bang, a long scrape across the sand, then silence. You are alive. You are also two hundred kilometres from the nearest road.",
   P("plane", 960, 950, 1.3, anim="shake"), T("200 KM", 1450, 320, 150, "red", at=0.4), T("NO ROAD", 500, 320, 110, "dark", at=0.6), bg="yellow")
sc(1, "Milo was the only passenger on a small cargo flight. Big glasses, yellow raincoat, and absolutely no idea what to do next.",
   M(800, "panic", "scream", anim="shake"), P("backpack", 1350, 900, 0.9, at=0.3), bg="yellow")
sc(1, "Get out. Check yourself. Can't move? Don't. Everything works? Then check the person next to you.",
   M(700, "point", "worried"), A(1250, "cry", "tired", at=0.3), T("CHECK", 960, 250, 120, "red", at=0.5))
sc(1, "The pilot is Amira. Cut on her arm, but awake. She says the one sentence that will save both of you.",
   A(1150, "point", "angry", anim="shake"), M(650, "hold", "shock", at=0.2))
sc(1, "Stay with the plane. A plane is huge, shiny and easy to spot from the air. Two people walking in the sand are a dot.",
   A(1250, "point", "neutral"), P("plane", 700, 950, 1.0, at=0.2), T("STAY", 700, 300, 150, "red", at=0.5), voice=AMIRA)
sc(1, "That is real advice. Survival manuals say almost the same thing: if rescuers know your route, the wreck is your best signal. Walking away is how people vanish.",
   P("plane", 600, 950, 0.9), M(1100, "pointup", "neutral"), P("eye", 1500, 400, 0.9, at=0.3), T("WRECK = SIGNAL", 960, 220, 100, "dark", at=0.5))

# HEAT --------------------------------------------------------------------
sc(1, "But it's forty six degrees. The metal of the plane is hot enough to burn skin. You need shade, and you need it now.",
   P("sun", 1500, 280, 1.4, anim="pulse"), P("thermo", 500, 600, 1.1, at=0.2), T("46°C", 500, 300, 160, "red", at=0.4), bg="yellow",
   chapter="Day 1: Shade")
sc(1, "Rule one of the desert: ration sweat, not water. Rest in the shade, move slowly, and keep your clothes on.",
   M(800, "pointup", "neutral"), P("bottle", 1300, 850, 1.0, at=0.2), T("RATION SWEAT", 960, 250, 120, "red", at=0.4), T("NOT WATER", 960, 400, 110, "dark", at=0.6))
sc(1, "Wait, clothes on? Yes. Loose clothes trap a thin layer of cooler air and stop the sun from pulling water out of your skin.",
   M(900, "hold", "confused"), T("CLOTHES ON", 960, 250, 120, "red", at=0.3), bg="yellow")
sc(1, "And never sit straight on the sand. The ground can be much hotter than the air. Even thirty centimetres up makes a difference.",
   M(900, "point", "worried", y=780), P("arrowup", 1400, 700, 1.0, at=0.3), T("+30 CM", 1400, 350, 120, "red", at=0.5))
sc(1, "So they drag a wing panel off the wreck, prop it on two seats, and crawl under it. A roof. The first good thing all day.",
   P("shelter", 960, 900, 1.3), M(700, "hold", "tired", at=0.2), A(1250, "stand", "tired", at=0.3), bg="yellow")
sc(1, "Water check. Four bottles, a broken cooler, and a tin of dates. Amira does the maths out loud.",
   P("bottle", 600, 850, 1.0), P("bottle", 800, 850, 1.0, at=0.1), P("bottle", 1000, 850, 1.0, at=0.2), P("bottle", 1200, 850, 1.0, at=0.3),
   T("4 L", 960, 300, 160, "red", at=0.5))
sc(1, "In this heat a resting person can lose several litres of sweat a day. Four litres for two people is not a plan. It's a countdown.",
   A(1200, "point", "worried"), P("stopwatch", 650, 700, 1.1, at=0.2, anim="pulse"), voice=AMIRA)

# NIGHT ------------------------------------------------------------------
sc(1, "Then the sun goes down and something nobody warned Milo about happens. The desert gets cold. Really cold.",
   P("thermo", 700, 650, 1.1), T("8°C", 700, 300, 160, "dark", at=0.3), M(1200, "hold", "shock", at=0.2), bg="navy",
   chapter="Day 1: Night")
sc(1, "Dry air can't hold heat. After a day at forty six, the night can drop below ten. The raincoat finally earns its place.",
   M(900, "hold", "tired"), P("cloud", 1450, 300, 0.9, at=0.3), bg="navy")
sc(2, "Night is also when the desert is kindest. Survivors work at dawn and dusk, and rest through the hottest hours.",
   P("sun", 960, 1000, 1.2), M(700, "point", "neutral", at=0.2), T("WORK AT DAWN", 960, 250, 110, "red", at=0.4), bg="grey")

# SIGNALS ------------------------------------------------------------------
sc(2, "Day two. The radio is dead, but Amira filed a flight plan. Somebody knows roughly where to look. Now they have to be seen.",
   A(1150, "point", "neutral"), P("phone", 650, 750, 0.9, at=0.2), T("NO SIGNAL", 650, 420, 100, "red", at=0.4), {"cross": [650, 420, 160], "at": 0.6},
   chapter="Day 2: Be seen")
sc(2, "They stamp three huge letters into the sand, each one taller than a person. S. O. S. Then they line the letters with dark rocks.",
   P("sos", 960, 900, 1.4), M(500, "point", "grin", at=0.3), T("SOS", 960, 250, 170, "red", at=0.5))
sc(2, "Big, and with contrast. From an airplane, a small mark on yellow sand is invisible. A dark shape ten metres long is not.",
   P("plane", 1400, 300, 0.7, move=[700, 300]), P("sos", 960, 950, 1.0), T("BIG + DARK", 960, 550, 110, "dark", at=0.4))
sc(2, "Then Amira pulls the best tool on board out of the first aid kit. A tiny signal mirror.",
   A(1100, "present", "smug"), P("mirror", 700, 700, 1.0, at=0.2, anim="pulse"))
sc(2, "On a sunny day, a mirror flash can be seen many kilometres away. Aim it with two fingers, sweep the horizon, and keep doing it.",
   P("mirror", 600, 700, 1.0), P("sun", 1500, 250, 1.0), T("FLASH", 1100, 500, 120, "red", at=0.3), {"arrow": [[700, 650], [1500, 300]], "color": "red", "at": 0.4}, voice=AMIRA)

# DAY 4-12 -----------------------------------------------------------------
sc(4, "Day four. A plane. High, tiny, going the wrong way. Milo flashes until his arm burns. It doesn't turn.",
   P("plane", 1500, 250, 0.5, move=[300, 200]), M(800, "pointup", "scream", at=0.1), P("mirror", 950, 650, 0.7),
   chapter="Day 4: The first plane")
sc(4, "It hurts. But it tells them something: there is traffic up there. They are close to a route. Stay. Keep signalling.",
   M(800, "cry", "sad"), A(1250, "hold", "neutral", at=0.3))
sc(6, "Day six. The last bottle is half empty. Milo wants to save it. Amira says no. Drink it when you're thirsty.",
   P("bottle", 960, 850, 1.2), M(650, "hold", "worried"), A(1300, "point", "angry", at=0.2), chapter="Day 6: Drink it")
sc(6, "That surprises a lot of people. But water in your body works better than water in a bottle. People have died of thirst with water still in their pack.",
   P("bottle", 700, 850, 1.0), P("drop", 1250, 600, 1.0, at=0.3), T("BODY > BOTTLE", 960, 250, 110, "red", at=0.5), voice=AMIRA, bg="yellow")
sc(6, "And no eating if you have almost no water. Digesting food, especially protein, uses water you can't spare. The dates can wait.",
   P("bread", 700, 800, 0.9), T("NO WATER", 1250, 300, 110, "red", at=0.2), T("NO FOOD", 1250, 450, 110, "dark", at=0.4))
sc(7, "Day seven, at dawn, Milo sees birds. Three of them, flying low, all in the same direction. Toward a line of rock.",
   P("cloud", 600, 300, 0.8), T("> > >", 960, 300, 120, "dark", at=0.2), M(700, "pointup", "shock", at=0.3), bg="grey",
   chapter="Day 7: Birds")
sc(7, "Birds circling or flying low at dawn and dusk often head to water. It's a clue, not a promise. But it's the only clue they've got.",
   M(800, "think", "neutral"), P("drop", 1350, 600, 1.0, at=0.3))
sc(7, "They argue. Leaving the plane breaks rule one. Staying with no water breaks every rule. They choose a middle path.",
   M(650, "point", "angry", anim="shake"), A(1250, "point", "angry", at=0.2, anim="shake"))
sc(7, "Arrows. Big ones, made of rocks, pointing from the wreck toward the rocks. And a note on the plane door with the date and direction.",
   P("plane", 500, 950, 0.8), T("→ → →", 1150, 900, 120, "dark", at=0.2), P("clipboard", 1450, 650, 0.8, at=0.4))
sc(7, "Then they walk. At night, under the stars, following the birds' line. Slowly. Ration sweat.",
   M(700, "run", "tired", walk=True), A(1100, "run", "tired", walk=True, at=0.1), P("footprint", 1450, 1000, 1.0, at=0.3), bg="navy")

# OASIS ------------------------------------------------------------------
sc(9, "Day nine. Below the rock there's a dry riverbed, a wadi. And in the shade of a cliff, a muddy pool. Water.",
   P("lake", 960, 950, 1.2), P("palm", 600, 850, 1.1, at=0.2), M(1300, "fist", "happy", at=0.3), bg="yellow",
   chapter="Day 9: The pool")
sc(9, "Milo wants to drink it right away. Amira stops him. Dirty water can make you sick, and diarrhoea in the desert can kill faster than thirst.",
   A(1150, "point", "angry", anim="shake"), M(650, "hold", "shock"), T("BOIL IT", 960, 250, 140, "red", at=0.4), voice=AMIRA)
sc(9, "So they filter it through cloth, then boil it in a tin from the plane over a fire of dry brush. One full minute at a rolling boil.",
   P("fire", 900, 950, 1.0), P("pot", 900, 820, 0.9, at=0.2), T("1 MIN", 1400, 350, 140, "red", at=0.4))
sc(9, "And they don't camp in the riverbed itself. A wadi is a river that's only resting. One storm far away can fill it in minutes.",
   P("wave", 960, 1000, 1.3, in_="none"), T("FLASH FLOOD", 960, 300, 120, "red", at=0.3), M(1400, "point", "worried", y=780))
sc(10, "So the camp goes up on the higher bank. A tent from the wing fabric, and a new SOS in rocks above the pool.",
   P("tent", 800, 900, 1.2), P("sos", 1350, 950, 0.8, at=0.3), bg="yellow")

# MIDDLE -----------------------------------------------------------------
sc(21, "Day twenty one. Food. Dates are gone. Amira knows a few safe things, but she sets a hard rule: if you don't know a plant, you don't eat it.",
   A(1100, "pointup", "neutral"), T("UNKNOWN = NO", 960, 250, 120, "red", at=0.3), chapter="Day 21: Food")
sc(21, "They catch lizards in the cool morning and cook them all the way through. Not delicious. Very alive.",
   P("fire", 960, 950, 1.0), M(650, "hold", "confused"), A(1300, "hips", "smug", at=0.2))
sc(28, "Day twenty eight. Milo stops sweating, gets a pounding headache, and starts talking nonsense. Amira knows exactly what this is.",
   M(900, "facepalm", "tired", anim="shake"), P("thermo", 1400, 650, 1.0, at=0.2), chapter="Day 28: Heat stroke")
sc(28, "Hot skin, confusion, no sweat: those are warning signs of heat stroke. It's an emergency. Cool the body fast.",
   T("HOT SKIN", 960, 220, 100, "red"), T("CONFUSED", 960, 340, 100, "red", at=0.2), T("NO SWEAT", 960, 460, 100, "red", at=0.4), M(960, "cry", "tired", y=950), voice=AMIRA)
sc(28, "Into the deepest shade. Wet cloth on his neck, armpits and head. Fan him. Small sips. By night, Milo's eyes are clear again.",
   A(1200, "hold", "worried"), M(700, "cry", "tired", y=950), P("drop", 900, 600, 0.8, at=0.3), bg="grey")

sc(40, "Day forty. The sky turns brown. A wall of sand, a kilometre high, rolling toward the camp.",
   P("storm", 960, 600, 1.5, anim="shake"), T("SANDSTORM", 960, 220, 140, "red", at=0.3, anim="pulse"), bg="grey",
   chapter="Day 40: The wall")
sc(40, "Don't run. Don't drive into it. Get low, turn your back to the wind, and cover your nose and mouth with cloth.",
   M(800, "hold", "scream", y=950, anim="shake"), A(1200, "hold", "worried", y=950, anim="shake"), T("GET LOW", 960, 250, 130, "red", at=0.4), bg="grey")
sc(40, "Wet the cloth if you can. Close your eyes. Wait. Three hours later the world is silent and everything is buried.",
   P("rubble", 960, 1000, 1.2, in_="none"), T("3 HOURS", 960, 300, 140, "dark", at=0.3), bg="grey")
sc(41, "Including the SOS. Rescue signals don't last. Every morning, Milo now walks out and fixes the letters. Signals are a daily job.",
   P("sos", 960, 950, 1.1), M(500, "point", "neutral", at=0.2), T("EVERY DAY", 1400, 300, 110, "red", at=0.4))

sc(55, "Day fifty five. The pool is shrinking. Milo digs a hole on the outside bend of the dry riverbed, where water stays longest underground.",
   P("lake", 700, 980, 0.7), M(1200, "hold", "tired"), P("arrowdown", 1200, 650, 0.9, at=0.3), chapter="Day 55: Digging")
sc(55, "Half a metre down, the sand is damp. An hour later, a little brown water seeps in. Filter it. Boil it. Every drop.",
   P("drop", 960, 700, 1.2, anim="pulse"), P("pot", 1350, 850, 0.8, at=0.3))
sc(63, "Day sixty three. The worst enemy isn't heat any more. It's the waiting. Milo stops talking. Amira notices.",
   M(800, "cry", "sad"), A(1300, "stand", "worried", at=0.2), bg="grey", chapter="Day 63: The mind")
sc(63, "She gives him jobs. Fix the SOS. Count the birds. Mark one stone for every day. Survivors say routine and a goal keep panic away.",
   A(1150, "point", "neutral"), P("calendar", 700, 650, 1.0, at=0.2), T("ROUTINE", 960, 250, 120, "red", at=0.4), voice=AMIRA)
sc(63, "Sixty three stones in a row. Milo starts counting forward instead of backward.",
   T("| | | | | | | | | |", 960, 700, 90, "dark"), M(1450, "stand", "neutral", at=0.3))

# LATE -------------------------------------------------------------------
sc(77, "Day seventy seven. A camel train on the far ridge. Too far to shout. They run for the mirror.",
   P("sun", 1500, 250, 0.9), M(700, "pointup", "shock", anim="shake"), T("CAMELS?", 1200, 600, 110, "dark", at=0.3),
   chapter="Day 77: The ridge")
sc(77, "Flash, flash, flash. The camels keep walking. And then one rider stops. Turns. And starts riding down.",
   P("mirror", 700, 700, 0.9, anim="pulse"), T("FLASH", 960, 400, 130, "red", at=0.2), M(500, "fist", "grin", at=0.4))
sc(77, "The traders share bread and water. Their phone has no signal either, but their route ends at an oasis town with a radio, eight days away.",
   G(1300, "present", "happy", extras=["cap"], shirt="tan", label="Trader"), M(700, "hold", "happy"), P("bread", 1000, 750, 0.8, at=0.3))
sc(77, "Amira can't ride that far with her arm. So they make a plan: the traders carry a note with their exact position. Milo and Amira stay.",
   P("clipboard", 960, 700, 1.1), A(1350, "point", "neutral", at=0.2), T("STAY. AGAIN.", 960, 280, 120, "red", at=0.4))

sc(88, "Day eighty eight. Nothing. Day ninety. Nothing. Day ninety five, a storm takes the tent.",
   T("88", 450, 500, 160, "dark"), T("90", 960, 500, 160, "dark", at=0.2), T("95", 1470, 500, 160, "red", at=0.4), bg="grey",
   chapter="Day 88: Waiting")
sc(95, "Milo wants to walk out. Amira points at the stones. Ninety five days alive, because they did not walk into the desert.",
   M(700, "point", "angry", anim="shake"), A(1250, "point", "neutral", at=0.2))

# RESCUE -----------------------------------------------------------------
sc(99, "Day ninety nine. A low thump on the horizon. Not thunder. Rotor blades.",
   P("heli", 1500, 300, 0.8, move=[1100, 350]), M(700, "pointup", "shock"), chapter="Day 99: The sound")
sc(99, "Three fires. Amira lights them in a triangle, the international sign for distress. Milo throws green brush on top for thick white smoke.",
   P("fire", 600, 950, 0.9), P("fire", 960, 800, 0.9, at=0.2), P("fire", 1320, 950, 0.9, at=0.4), T("3 FIRES", 960, 250, 130, "red", at=0.5))
sc(99, "And the mirror. Straight at the cockpit. One flash, two, three. The helicopter tilts. And turns toward them.",
   P("mirror", 600, 700, 0.9, anim="pulse"), P("heli", 1350, 350, 1.0), T("SEEN!", 1000, 550, 150, "red", at=0.4, anim="pulse"))
sc(100, "Day one hundred. A hospital bed, an IV in Milo's arm and a nurse who says one word: lucky. Amira laughs. Not luck. Rules.",
   M(800, "cry", "happy", y=950), A(1300, "fist", "grin", at=0.2), T("DAY 100", 960, 220, 170, "red", at=0.3, anim="pulse"), bg="sky",
   chapter="Day 100: Out")

# RECAP ------------------------------------------------------------------
sc(None, "So, could you survive? Stay with the wreck. Ration sweat, not water. Shade and height by day, work at dawn and dusk.",
   T("STAY", 960, 200, 110, "red"), T("SHADE", 960, 320, 110, "red", at=0.2), T("DAWN + DUSK", 960, 440, 100, "red", at=0.4), M(960, "pointup", "neutral", y=950), bg="yellow", ground=False)
sc(None, "Boil your water, don't camp in a wadi, know heat stroke, and make yourself huge, bright and flashing. Signals save lives.",
   T("BOIL", 960, 200, 110, "dark"), T("NO WADI", 960, 320, 110, "dark", at=0.2), T("SIGNAL", 960, 440, 110, "red", at=0.4), M(960, "fist", "grin", y=950), bg="yellow", ground=False)
sc(None, "Next time: Milo is trapped in a city that is slowly flooding. Day one to day one hundred. Subscribe so you don't miss it.",
   M(800, "point", "grin"), P("wave", 1350, 950, 1.0, in_="none"), T("NEXT: FLOOD CITY", 960, 250, 110, "red", at=0.3), bg="sky")

DESC = """A small cargo plane goes down in the Sahara. Milo and pilot Amira have 4 litres of water, a wrecked plane and one mirror. Day 1 to Day 100: shade, signals, a muddy pool, heat stroke, a sandstorm and three fires.

The story is fiction; the survival facts are real. This is not professional safety training — in a real emergency, call for help and follow rescuers.

Next episode: Trapped in a Flooding City.

Sources:
U.S. Army Field Manual FM 21-76, Survival — Desert survival (ration sweat, not water; shade; travel at night) https://archive.org/details/FM21-76SurvivalManual
CDC NIOSH — Heat stress: heat stroke and heat exhaustion https://www.cdc.gov/niosh/heat-stress/about/illnesses.html
CDC — Make water safe in an emergency (boiling 1 minute) https://www.cdc.gov/water-emergency/about/how-to-create-safe-drinking-water.html
NOAA/NWS — Flash flood safety https://www.weather.gov/safety/flood

#survival #story #animation"""

ep = {
    "id": "ep006",
    "title": "Trapped in the Sahara After a Crash: Day 1 to 100",
    "voice": "am_michael",
    "speed": 1.0,
    "hook": "The engine stops. The desert is coming up fast.",
    "description": DESC,
    "tags": ["survival story", "desert survival", "plane crash survival", "day 1 to 100", "100 days", "sahara survival",
             "survival story animated", "how to survive", "heat stroke", "milo survives", "animated story"],
    "thumbnail": {"bg": "yellow", "text": "DAY 1|STRANDED", "size": 200, "color": "red",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["glasses"], "shirt": "yellow"},
                  "guy_x": 1450, "items": [{"prop": "plane", "x": 560, "y": 900, "s": 1.5}, {"prop": "sun", "x": 400, "y": 300, "s": 1.2}]},
    "shorts": [],
    "scenes": S,
}

# Shorts: cold open + the heat-stroke moment (start estimated from narration length, ~2.5 words/s)
t = 0.0
starts = []
for s in S:
    starts.append(t)
    t += max(3.0, len(s["say"].split()) / 2.5)
i_hs = next(i for i, s in enumerate(S) if s.get("chapter") == "Day 28: Heat stroke")
ep["shorts"] = [
    {"start": 0, "dur": 35, "top": "The engine just stopped. Over the Sahara.", "title": "Your Plane Goes Down in the Sahara"},
    {"start": int(starts[i_hs]), "dur": 35, "top": "He stopped sweating. That's bad.", "title": "Day 28 in the Desert: The Silent Killer"},
]

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = os.path.join(root, "cloud", "queue", "milo", "ep006.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(ep, open(out, "w"), indent=1, ensure_ascii=False)
    words = sum(len(s["say"].split()) for s in S)
    print(out, len(S), "scenes", words, "words", f"~{t / 60:.1f} min est", "title len", len(ep["title"]))

"""Hollowmere Tales EP 18 (3D) — the Winchester Mystery House. Writes scripts3d/ep018.json.
Documented record + legend (sources: historyhit.com/facts-about-the-winchester-mystery-house/,
thehistorygirl.com/2016/06/08/winchester-mystery-house-san-jose-ca/):
Sarah Winchester's infant daughter Annie died in 1866; her husband William Wirt Winchester (treasurer of the Winchester
rifle company) died of tuberculosis in 1881; she inherited his fortune. 1884: bought an unfinished eight-room farmhouse
in the Santa Clara Valley (San Jose, California) and kept building for about 38 years, until her death on 5 September 1922,
with no architect. About 160 rooms, 40 bedrooms, 2 ballrooms, 47 fireplaces, 6 kitchens, about 10,000 window panes,
2,000 doorways. Stairs that run into the ceiling; a switchback staircase of 7 flights / 44 steps rising only about 9 feet;
a second-floor door that opens onto a drop to the garden ("door to nowhere"); doors that open onto walls.
The number 13: 13-pane windows, 13 bathrooms, chandeliers with 13 candles, drain covers with 13 holes, a will in 13 parts.
1906 earthquake: the seven-storey tower collapsed; she was trapped in her bedroom for hours; the front 30 rooms were boarded up.
LEGEND (not documented): a Boston medium told her to move west and never stop building for the spirits, or she would die.
Historians say she may simply have loved building. Opened to visitors months after her death; National landmark 1974.
Short 1 = the door to nowhere + stairs to the ceiling (beats 14-19)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-5, 6])
chars["moth"] = dict(chars["moth"], home=[-2.5, 5])
chars["sarah"] = {"name": "Sarah", "voice": "af_nicole", "speed": 0.85, "pitch": -2, "color": [0.06, 0.05, 0.07],
                  "kind": "lady", "ghost": True, "up": True, "size": 0.95, "home": [5, 12]}
chars["builder"] = {"name": "Carpenter", "voice": "am_michael", "speed": 1.05, "pitch": -1, "color": [0.35, 0.25, 0.15],
                    "kind": "human", "size": 1.0, "home": [-10, 11]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big text hook + voice mid-danger at frame 1
    L(N, "Don't open that door. Behind it there is no room. Only a drop into the dark.", "wide",
      [["door", "spin"], ["odo", "shake"], ["moth", "eyes_big"]], text="DON'T OPEN THE DOOR"),
    L("moth", "Odo, stop! Your foot is over the edge!", "close:moth", [["moth", "shake"]], sfx="alarm"),
    L("odo", "There's nothing there. The floor just ends!", "close:odo", [["odo", "eyes_big"]], text="THE FLOOR ENDS"),
    L(N, "Behind them on the Brown Lady's stairs, a door had opened. They stepped through. And fell.", "overhead",
      [["sarah", "rise"]], sfx="suspicious", text="THEY FELL THROUGH"),
    L(N, "This is a true story, from real records. A house in San Jose, California.", "wide",
      [["odo", "turn:sarah"]], text="SAN JOSE, CALIFORNIA"),
    L(N, "A house where the building never stopped. Day and night. For thirty-eight years.", "close:builder",
      [["builder", "enter:left"]], sfx="suspicious", text="38 YEARS OF BUILDING"),
    # ---- who was she ----
    L(N, "It belonged to Sarah Winchester. Her baby daughter died in 1866.", "close:sarah",
      [["sarah", "sad"]], text="SARAH WINCHESTER"),
    L(N, "Fifteen years later, her husband died too. He ran the family's famous rifle company.", "two:sarah,odo",
      [["sarah", "turn:front"]], text="1881: ALONE"),
    L(N, "She was left with a huge fortune. And she moved all the way west.", "wide",
      [["sarah", "to:3,10"]], text="ALL THE WAY WEST"),
    L("moth", "Why would anyone move so far away?", "close:moth", [["moth", "turn:sarah"]]),
    # ---- the house ----
    L(N, "In 1884 she bought a small farmhouse with eight rooms. Then she started building.", "prop:door",
      [["builder", "jump"]], text="1884: EIGHT ROOMS"),
    L("builder", "More rooms. Always more rooms. We never get a day off!", "close:builder", [["builder", "shake"]]),
    L(N, "No architect. No final plan. Rooms were built, torn down, and built again.", "two:builder,odo",
      [["builder", "to:-6,10"]], sfx="suspicious", text="NO PLAN"),
    L(N, "By the end, the house had about one hundred sixty rooms. And ten thousand windows.", "wide",
      [["odo", "spin"]], text="160 ROOMS"),
    # ---- doors to nowhere (Short 1 segment) ----
    L(N, "Some stairs climb up and stop at the ceiling. They lead nowhere at all.", "wide",
      [["moth", "turn:front"]], text="STAIRS TO THE CEILING"),
    L(N, "One door on the second floor opens onto thin air. A drop straight down to the garden.", "prop:door",
      [["door", "spin"], ["odo", "shake"]], sfx="alarm", text="A DOOR TO NOWHERE"),
    L("odo", "Who builds a door that opens onto nothing?", "close:odo", [["odo", "eyes_big"]]),
    L(N, "Other doors open onto solid walls. And windows look into other rooms.", "two:odo,moth",
      [["moth", "eyes_big"]], text="DOORS INTO WALLS"),
    L(N, "And the number thirteen is everywhere. Thirteen bathrooms. Windows with thirteen panes.", "prop:clock",
      [["clock", "show"], ["clock", "spin"]], sfx="suspicious", text="13. EVERYWHERE."),
    L("moth", "Thirteen? Odo, don't count the steps. Please.", "close:moth", [["moth", "shake"]]),
    # ---- the legend ----
    L(N, "Why did she build like this? The records don't say. But a legend does.", "close:sarah",
      [["sarah", "rise"], ["clock", "vanish"]], text="THE LEGEND"),
    L(N, "The legend says a spirit medium told her: keep building, and never stop.", "two:sarah,moth",
      [["sarah", "to:1,9"]], sfx="suspicious", text="NEVER STOP BUILDING"),
    L("sarah", "If the hammers stop... they will find me.", "close:sarah", [["sarah", "turn:front"]], text="THEY WILL FIND ME"),
    L(N, "Some say the twisting halls were made to confuse the spirits. So they could never find her.", "overhead",
      [["odo", "to:-2,9"], ["moth", "spin"]], text="A MAZE FOR GHOSTS?"),
    L(N, "But many historians say she simply loved building. Nobody knows for sure.", "wide",
      [["sarah", "dive"]], text="NOBODY KNOWS"),
    # ---- 1906 earthquake ----
    L(N, "Then came April 1906. The great earthquake shook the whole house.", "wide",
      [["all", "shake"], ["moth", "shake"]], sfx="alarm", text="APRIL 1906"),
    L(N, "Her seven-storey tower fell. Sarah was trapped in her bedroom for hours.", "close:builder",
      [["builder", "shake"]], text="TRAPPED FOR HOURS"),
    L(N, "Afterwards, she had thirty rooms at the front boarded up. Closed forever.", "prop:door",
      [["door", "bounce"]], sfx="suspicious", text="30 ROOMS SEALED"),
    L("odo", "What did she lock inside those rooms?", "close:odo", [["odo", "turn:moth"]]),
    # ---- the end ----
    L(N, "In September 1922, Sarah died. And for the first time in thirty-eight years, the hammers stopped.", "two:builder,odo",
      [["builder", "exit"]], text="THE HAMMERS STOPPED"),
    L(N, "Today, visitors walk its halls. Some say they still hear footsteps where nobody is.", "close:moth",
      [["moth", "eyes_big"]], sfx="suspicious", text="FOOTSTEPS"),
    # ---- cliffhanger ----
    L(N, "Then, in the silent house, Odo heard it. A hammer. Knock. Knock. Knock.", "overhead",
      [["odo", "shake"]], sfx="alarm", text="KNOCK. KNOCK. KNOCK."),
    L("moth", "Odo... it's coming from the room that was sealed.", "close:moth", [["moth", "eyes_big"], ["all", "look:sarah"]]),
    L("sarah", "You opened my door. Now you must help me build.", "close:sarah", [["sarah", "rise"], ["sarah", "to:4,8"]], text="HELP ME BUILD"),
    L(N, "Who is still building in the sealed rooms? Subscribe. Don't miss the next door.", "wide",
      [["door", "spin"], ["odo", "eyes_big"]], text="WHO IS STILL BUILDING?"),
]

stairs = []
for i in range(6):  # stairs that climb into a ceiling beam
    stairs.append({"id": f"st{i}", "type": "box", "color": [0.2, 0.13, 0.08], "at": [7.5, 13 + i * 1.0, -0.6 + i * 0.55], "scale": 1.0})

sc = {
    "title": "Don't Open the Door to Nowhere",
    "description": "Don't open that door. Behind it there is no room. Only a drop into the dark.",
    "lead_in": 0.05,
    "set": {"place": "village", "fog": 0.06, "eyes": 3, "moonlight": 2.4},
    "chars": chars,
    "props": stairs + [
        {"id": "ceiling", "type": "box", "color": [0.12, 0.08, 0.05], "at": [7.5, 17, 3.6], "scale": 2.2},
    ] + [{"id": f"door{k}", "type": "box", "color": [0.4, 0.22, 0.1], "at": [-9.5, 9, -0.05 + k * 0.94], "scale": 0.8, "glow": 0.25} for k in range(3)] + [
        {"id": "clock", "type": "star", "color": "gold", "at": [0, 9, 2.0], "visible": False, "scale": 0.9},
    ],
    "beats": beats,
}
# the door is three stacked blocks: every door action drives all three; camera "prop:door" looks at the middle one
for b in beats:
    if "do" in b:
        nd = []
        for t_, a_ in b["do"]:
            nd += [[f"door{k}", a_] for k in range(3)] if t_ == "door" else [[t_, a_]]
        b["do"] = nd
    if b["cam"] == "prop:door": b["cam"] = "prop:door1"
json.dump(sc, open(os.path.join(HERE, "ep018.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats), "words", sum(len(b["say"].split()) for b in beats))

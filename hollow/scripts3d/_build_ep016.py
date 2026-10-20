"""Hollowmere Tales EP 16 (3D) — Loch Ness. Writes scripts3d/ep016.json.
Documented record + legend: Adomnan's Life of St Columba (written about a century after the event) tells how in 565 AD
Columba, at the River Ness, ordered a "water beast" rushing at a swimmer to go back, and it fled.
Loch Ness: about 23 miles (37 km) long, up to about 230 m deep, more fresh water than all the lakes of England and Wales together.
1933: a new road along the north shore opened up the view. April 1933 Aldie Mackay and her husband saw a whale-like creature
rolling in the water; the Inverness Courier reported it on 2 May 1933 and called it a "monster". July 1933: George Spicer and his
wife said a long-necked creature crossed the road in front of their car. 1934: the "Surgeon's Photograph" (Daily Mail) - head and
neck rising from the water; revealed in 1994 as a hoax: a toy submarine with a model head and neck about a foot tall (Wetherell).
1987 Operation Deepscan: a line of boats swept the loch with sonar; some unexplained contacts, no monster.
2018: Prof. Neil Gemmell (University of Otago) - about 250 water samples, no reptile DNA, a lot of eel DNA.
More than a thousand sightings are on the Official Loch Ness Monster Sightings Register.
Short 1 = the 1933 Mackay sighting segment (beats marked below)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 5])
chars["moth"] = dict(chars["moth"], home=[-3.5, 4.5])
chars["beast"] = {"name": "The shape", "voice": "am_onyx", "speed": 0.8, "pitch": -5, "color": [0.05, 0.11, 0.08],
                  "kind": "lochbeast", "size": 1.25, "home": [4, 14]}
chars["columba"] = {"name": "Columba", "voice": "bm_lewis", "speed": 0.95, "pitch": -1, "color": [0.32, 0.24, 0.16],
                    "kind": "human", "size": 1.0, "home": [-11, 9]}
chars["swimmer"] = {"name": "Swimmer", "voice": "am_puck", "speed": 1.05, "pitch": 1, "color": [0.7, 0.6, 0.45],
                    "kind": "human", "size": 0.8, "home": [1, 10]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big hook + voice at frame 1
    L(N, "Something huge is moving under this water. And people have seen it for fourteen hundred years.", "wide",
      [["beast", "rise"], ["odo", "shake"], ["moth", "eyes_big"]], text="DON'T LOOK IN THE WATER"),
    L("odo", "Mothwick, back away from the edge. Slowly.", "close:odo", [["odo", "turn:beast"]], sfx="suspicious"),
    L(N, "Last night the ghost legion marched past them, and melted into the fog over a lake.", "two:odo,moth",
      [["beast", "dive"], ["moth", "turn:odo"]], text="WHERE ARE WE?"),
    L("moth", "Odo... this isn't our swamp. This is Loch Ness.", "close:moth", [["moth", "shake"]], text="LOCH NESS, SCOTLAND"),
    L(N, "This is a true story, from real records. Loch Ness is about twenty-three miles long.", "overhead", text="23 MILES LONG"),
    L(N, "In places it is deeper than two hundred meters. Dark as tea. You cannot see the bottom.", "wide",
      [["odo", "to:-4,7"]], sfx="suspicious", text="DARK AS TEA"),
    L(N, "It holds more fresh water than all the lakes of England and Wales put together.", "close:odo", [["odo", "eyes_big"]]),
    L("odo", "So something big could hide down there.", "close:odo", [["odo", "turn:front"]]),
    # ---- 565: St Columba ----
    L(N, "The first story is very old. It was written down by a monk named Adomnan.", "close:columba",
      [["columba", "enter:left"]], text="THE FIRST RECORD"),
    L(N, "He wrote that in the year 565, a holy man called Columba came to the River Ness.", "two:columba,swimmer",
      [["swimmer", "enter:right"]], text="AD 565"),
    L(N, "A man was swimming across. Then the water began to boil behind him.", "close:swimmer",
      [["swimmer", "shake"], ["beast", "rise"]], sfx="suspicious", text="THE WATER BOILED"),
    L(N, "A water beast rushed at him with a great roar, its mouth wide open.", "two:swimmer,beast",
      [["beast", "to:3,11"], ["swimmer", "eyes_big"]], text="A WATER BEAST"),
    L("columba", "Go no further! Go back at once!", "close:columba", [["columba", "jump"]]),
    L(N, "The record says the beast turned and fled, as if pulled back by ropes.", "wide",
      [["beast", "dive"], ["swimmer", "exit"]], text="IT FLED"),
    L("moth", "Was that real, or a story?", "close:moth", [["columba", "exit"]]),
    L(N, "Nobody knows. It was written about a hundred years after it happened.", "two:odo,moth", [["odo", "sad"]], text="NOBODY KNOWS"),
    # ---- 1933: the Mackays (Short 1 segment: beats 16-19) ----
    L(N, "April 1933. A couple driving beside Loch Ness saw the water explode.", "wide",
      [["beast", "rise"], ["odo", "shake"]], sfx="suspicious", text="THE WATER EXPLODED"),
    L(N, "Something huge rolled up out of the loch. Like a whale. In a lake.", "close:beast",
      [["beast", "to:2,10"]], text="LIKE A WHALE"),
    L("moth", "Odo... it's looking right at us.", "close:moth", [["moth", "eyes_big"], ["all", "look:beast"]]),
    L(N, "Then it sank in a boiling mass of foam. And the water went still. Too still.", "close:beast",
      [["beast", "dive"]], text="TOO STILL"),
    # ---- the monster is born ----
    L(N, "The local newspaper printed their story. It called the thing a monster.", "overhead", text="1933: A MONSTER"),
    L(N, "A new road had just opened along the shore. Now thousands could watch the water.", "two:odo,moth", [["odo", "turn:front"]]),
    L(N, "That summer, another couple said a long-necked creature crossed the road in front of their car.", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="IT CROSSED THE ROAD"),
    L("odo", "On land? It came out of the water?", "close:odo", [["odo", "shake"]]),
    # ---- the photograph ----
    L(N, "In 1934, a newspaper printed a photo. A long neck. A small head. Rising from the loch.", "prop:photo",
      [["photo", "show"], ["photo", "spin"]], text="THE FAMOUS PHOTO"),
    L(N, "For sixty years, it was the most famous picture of the monster.", "prop:photo", [["photo", "bounce"]]),
    L(N, "Then, in 1994, the truth came out. It was a toy submarine with a model head.", "prop:sub",
      [["photo", "vanish"], ["sub", "show"]], text="IT WAS A TOY"),
    L("moth", "A toy? About as tall as a ruler?", "close:moth", [["sub", "bounce"]]),
    L(N, "But the photo was fake. The sightings did not stop.", "wide", [["sub", "vanish"]], sfx="suspicious", text="THE SIGHTINGS DIDN'T STOP"),
    # ---- science ----
    L(N, "In 1987, a line of boats swept the whole loch with sonar.", "overhead", text="1987: SONAR"),
    L(N, "They found some strange moving shapes deep down that no one could explain.", "close:beast",
      [["beast", "rise"]], sfx="suspicious", text="SHAPES IN THE DEEP"),
    L(N, "In 2018, scientists tested the water itself, for traces of everything living in it.", "prop:eel",
      [["beast", "dive"], ["eel", "show"]], text="2018: DNA TEST"),
    L(N, "No reptile DNA at all. But a surprising amount of eel DNA.", "prop:eel", [["eel", "spin"]], text="EELS. LOTS OF EELS."),
    L("odo", "How big can an eel get?", "close:odo", [["eel", "vanish"], ["odo", "turn:moth"]]),
    L(N, "Nobody knows what people really saw. More than a thousand sightings are on record.", "two:odo,moth",
      [["moth", "turn:odo"]], text="1,000+ SIGHTINGS"),
    # ---- ending + cliffhanger ----
    L("moth", "Odo, your lantern. Look at the reflection.", "close:moth", [["moth", "eyes_big"]], sfx="suspicious"),
    L(N, "In the black water, under their own reflection, two green eyes opened.", "close:beast",
      [["beast", "rise"]], text="TWO EYES OPENED"),
    L("odo", "Mothwick... that's not one shape. There are two.", "close:odo", [["odo", "shake"], ["moth", "shake"], ["beast", "to:-1,9"]]),
    L(N, "What is waiting at the bottom of Loch Ness? The next tale begins right here.", "wide",
      [["all", "look:beast"], ["odo", "eyes_big"]], text="WHAT'S DOWN THERE? SUBSCRIBE!"),
]

sc = {
    "title": "1,400 Years of Sightings. What's in Loch Ness?",
    "description": "Something huge is moving under this water. And people have seen it for fourteen hundred years.",
    "lead_in": 0.05,
    "set": {"place": "swamp", "fog": 0.05, "eyes": 3, "moonlight": 2.6},
    "chars": chars,
    "props": [
        {"id": "photo", "type": "box", "color": "white", "at": [0, 9, 1.6], "visible": False, "scale": 0.9},
        {"id": "sub", "type": "banana", "color": [0.12, 0.12, 0.12], "at": [0, 9, 1.4], "visible": False, "scale": 1.2},
        {"id": "eel", "type": "banana", "color": [0.2, 0.3, 0.12], "at": [0, 9, 1.4], "visible": False, "scale": 1.5},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep016.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats))

"""Hollowmere Tales EP 28 (3D) - the Kelly-Hopkinsville encounter, Christian County, Kentucky, 21-22 August 1955. Writes scripts3d/ep028.json.
Recorded encounter (sources: en.wikipedia.org/wiki/Kelly%E2%80%93Hopkinsville_encounter,
ufology.patrickgross.org/htm/kelly55tim.htm (timeline from the 1955 press + Blue Book files),
ufology.patrickgross.org/htm/kentuckynewera30dec2002.htm (Kentucky New Era retrospective)):
- 21 Aug 1955, about 7 pm, the Sutton farmhouse near Kelly, Kentucky. Billy Ray Taylor went out to the well and saw a bright
  light streak across the sky and vanish beyond the tree line. Nobody believed him.
- The farm dog barked, then hid under the house. A small glowing figure came toward the house.
- Witnesses: about 3.5 ft tall (2-4 ft), a large round head, huge pointed ears, big glowing yellow eyes, long thin arms,
  talon-like hands, spindly legs, shimmering like bright metal ("like a 5 gallon gasoline can with a head on it" - Glennie Lankford).
  They peered in the windows and the doorway, climbed onto the roof; when hit they seemed to float down, not fall.
- The men tried to drive them off for about 3-4 hours. About 11 pm the families (5 adults, 7 children reached the station)
  drove to the Hopkinsville police station.
- Police, state troopers, deputies and military police from Fort Campbell searched: broken window, holes in screens, no footprints
  in the hard soil, no creature. Police chief found no sign of drinking. A trooper saw meteor-like flashes on the road.
- After the police left (about 2:15 am) the figures came back to the windows until shortly before sunrise.
- Explanations: great horned owls (yellow eyes, silent flight, ~2 ft tall); meteors for the light. Blue Book: hoax.
  Today Kelly holds the 'Little Green Men Days' festival (early reports did NOT say green).
No injuries. No guns on screen. Continues EP 27 (the Pale Shepherd: 'I am already at the top.')."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
GOB = {"voice": "bm_lewis", "speed": 0.9, "pitch": 4, "color": [0.62, 0.66, 0.7], "kind": "demon", "size": 0.46}
chars["gob"] = dict(GOB, name="The little visitor", home=[0.5, 14.6])
chars["gob2"] = dict(GOB, name="Another visitor", home=[30, 30])
chars["gob3"] = dict(GOB, name="A third visitor", home=[-30, 30])
chars["billy"] = {"name": "Billy Ray", "voice": "am_michael", "speed": 1.05, "pitch": 0, "color": [0.3, 0.35, 0.5],
                  "kind": "human", "size": 0.9, "home": [-8, 11]}
chars["glennie"] = {"name": "Mrs Lankford", "voice": "af_sarah", "speed": 1.0, "pitch": 0, "color": [0.45, 0.25, 0.3],
                    "kind": "human", "size": 0.85, "home": [-10, 11.5]}
chars["lucky"] = {"name": "Lucky Sutton", "voice": "am_adam", "speed": 1.05, "pitch": -1, "color": [0.35, 0.3, 0.2],
                  "kind": "human", "size": 0.95, "home": [-11.5, 10.5]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

# the farmhouse wall: dark boards + one glowing window
WALL = {"type": "box", "color": [0.2, 0.15, 0.11], "visible": True}
props = [dict(WALL, id=f"w{r}{i}", at=[-4.2 + i * 1.4, 16.0, r * 1.42], scale=1.2) for r in range(2) for i in range(7)]
props += [{"type": "box", "id": "win", "color": [1.0, 0.7, 0.3], "glow": 2.5, "visible": True, "scale": 0.8, "at": [0.6, 15.3, 1.3]}]
props += [{"type": "ball", "id": "fire", "color": [1.0, 0.85, 0.4], "glow": 25, "visible": False, "scale": 0.6, "at": [-22, 30, 18]}]
props += [{"type": "ball", "id": "flash", "color": [0.7, 0.85, 1.0], "glow": 18, "visible": False, "scale": 0.5, "at": [12, 22, 6]}]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (a small figure slides up to the lit window, Odo jumps back) + text hook + voice mid-danger
    L(N, "Something was looking in the window. Two huge yellow eyes. And it was only three feet tall.", "close:gob",
      [["gob", "to:0.6,14.4,0"], ["odo", "jump"], ["gob", "turn:front"]], sfx="alarm", text="DON'T LOOK AT THE WINDOW"),
    L("moth", "Odo! It's pressing its face against the glass!", "close:moth",
      [["moth", "shake"]], text="IT'S AT THE GLASS"),
    L("odo", "Look at the ears, Mothwick. Huge and pointed. And its hands are like claws.", "close:gob",
      [["gob", "shake"]], sfx="suspicious", text="POINTED EARS. CLAWS."),
    L(N, "This is a true story, from police and newspaper reports of nineteen fifty-five.", "wide",
      [["gob", "to:2.5,14.4,0"]], text="A TRUE STORY"),
    L(N, "A farmhouse near Kelly, Kentucky. Two families were inside, and many children.", "overhead",
      [["odo", "turn:front"]], text="KENTUCKY, 1955"),
    # ---- the light ----
    L(N, "August the twenty-first, about seven in the evening. Billy Ray went out to the well.", "wide",
      [["billy", "enter:left"], ["gob", "to:30,30,0"]], text="7 PM. THE WELL"),
    L(N, "Then a bright light streaked across the sky, and dropped behind the trees.", "wide",
      [["fire", "show"], ["fire", "drift:20,40,1"]], sfx="horn", text="A LIGHT FELL"),
    L("billy", "Did you see that? A flying saucer! It came down past the field!", "close:billy",
      [["billy", "jump"], ["fire", "vanish"]], text="A FLYING SAUCER?"),
    L("lucky", "A saucer? You've been in the sun too long, Billy Ray.", "two:billy,lucky",
      [["lucky", "enter:left"], ["lucky", "turn:billy"]]),
    L("moth", "Nobody ever believes the first one who sees it. That's always how it starts.", "close:moth",
      [["moth", "eyes_big"]], sfx="suspicious"),
    # ---- the dog ----
    L(N, "Nobody believed him. But an hour later, the farm dog started barking.", "close:odo",
      [["odo", "turn:moth"]], text="THE DOG BARKED"),
    L(N, "Then the dog stopped barking, and crawled under the house. It would not come out.", "wide",
      [["all", "shake"]], sfx="alarm", text="THEN IT HID"),
    L(N, "Out of the dark field came a small, glowing figure, walking straight toward the house.", "wide",
      [["gob", "to:5,13,0"], ["gob", "turn:front"]], sfx="horn", text="SOMETHING GLOWING"),
    L("lucky", "Get inside! Everybody get inside, and shut the door!", "close:lucky",
      [["lucky", "shake"], ["billy", "to:-6,13,0"]], text="SHUT THE DOOR!"),
    # ---- the description ----
    L(N, "It was about three and a half feet tall, with a big round head.", "close:gob",
      [["gob", "eyes_big"]], text="3 1/2 FEET TALL"),
    L(N, "Its eyes were huge and glowing yellow. Its ears stood up like points.", "close:gob",
      [["gob", "shake"]], sfx="suspicious", text="GLOWING YELLOW EYES"),
    L(N, "It had long, thin arms that almost reached the ground, and hands like talons.", "close:gob",
      [["gob", "to:3,14,0"]], text="HANDS LIKE TALONS"),
    L("glennie", "It shines like silver. Like a gasoline can, with a head on it!", "close:glennie",
      [["glennie", "enter:left"], ["glennie", "shake"]], text="SHINING LIKE METAL"),
    # ---- the siege ----
    L(N, "Then there was another one. And another. At the windows. At the door.", "wide",
      [["gob2", "to:-1.5,14.4,0"], ["gob3", "to:4,14.2,0"], ["flash", "show"]], sfx="alarm", text="THERE WERE MORE"),
    L("moth", "Odo, there's one on the roof! I can hear it walking up there!", "close:moth",
      [["moth", "shake"], ["gob2", "to:-1.5,15.2,2.6"]], text="ONE ON THE ROOF"),
    L(N, "The men tried everything to scare them off. But the figures did not fall.", "close:gob2",
      [["gob2", "to:-1.5,14.6,0"], ["flash", "vanish"]], sfx="horn", text="THEY DIDN'T FALL"),
    L(N, "They floated. Slowly down, over the fence, and back into the dark.", "wide",
      [["gob2", "to:-6,22,1.5"], ["gob3", "to:10,22,1.5"]], sfx="suspicious", text="THEY FLOATED"),
    L(N, "Then they came back. Again, and again, for nearly four hours.", "close:gob",
      [["gob", "to:0.6,14.4,0"], ["gob", "turn:front"]], text="4 HOURS"),
    L("glennie", "Children, into the car. All of you. We are going to the police. Now!", "close:glennie",
      [["glennie", "jump"], ["all", "shake"]], sfx="alarm", text="RUN TO THE CAR"),
    # ---- the rule ----
    L("odo", "That's the rule, Mothwick. If the dog hides, never open the door to see why.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="IF THE DOG HIDES..."),
    # ---- the police ----
    L(N, "At eleven o'clock, two families burst into the Hopkinsville police station.", "wide",
      [["billy", "exit"], ["lucky", "exit"], ["glennie", "exit"]], text="11 PM. POLICE"),
    L(N, "Police officers, state troopers, and soldiers from Fort Campbell drove out to the farm.", "overhead",
      [["flash", "show"], ["flash", "drift:-6,18,4"]], sfx="horn", text="SOLDIERS CAME TOO"),
    L(N, "On the road, a trooper saw strange flashes, like meteors, in the sky.", "wide",
      [["flash", "drift:-20,40,10"]], text="STRANGE FLASHES"),
    L(N, "They found a broken window and torn screens. But no footprints. No creature.", "close:odo",
      [["flash", "vanish"], ["gob", "to:30,30,0"]], text="NO FOOTPRINTS"),
    L(N, "The police chief checked. Nobody in the house had been drinking. They were terrified.", "two:odo,moth",
      [["moth", "eyes_big"]], text="THEY WERE TERRIFIED"),
    # ---- they came back ----
    L(N, "At a quarter past two, the police left. And the little figures came back.", "close:gob",
      [["gob", "to:0.6,14.4,0"], ["gob", "turn:front"], ["all", "shake"]], sfx="alarm", text="THEY CAME BACK"),
    L("moth", "Back to the same window. They were waiting for the police to go!", "close:moth",
      [["moth", "shake"], ["moth", "to:-5,7,1.5"]], text="THEY WAITED"),
    L(N, "They stayed at the windows until just before sunrise. Then they were gone.", "overhead",
      [["gob", "to:30,30,0"]], sfx="suspicious", text="UNTIL SUNRISE"),
    # ---- explanations ----
    L(N, "Some experts say they were great horned owls. Owls have yellow eyes, and fly without a sound.", "wide",
      [["odo", "turn:front"]], text="OWLS?"),
    L(N, "But the families never changed their story. Not once, for the rest of their lives.", "two:odo,moth",
      [["odo", "turn:moth"]], sfx="horn", text="THEY NEVER CHANGED IT"),
    L(N, "So, would YOU open the door, if your dog was hiding under the house?", "close:odo",
      [["odo", "eyes_big"]], sfx="alarm", text="WOULD YOU OPEN IT?"),
    L("moth", "Never. I would turn off the lantern and hide under the table.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the window glowed again. A pale hand was tapping on the glass.", "close:odo",
      [["shepherd", "to:3,14.6,0"], ["all", "shake"]], sfx="alarm", text="TAP. TAP. TAP."),
    L("shepherd", "Lock every door you like, lantern-bearer. I am already inside.", "close:shepherd",
      [["shepherd", "turn:front"]], sfx="suspicious", text="IT'S ALREADY INSIDE"),
    L(N, "Who let it in? Subscribe, so you don't miss the next true tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="horn", text="WHO LET IT IN?"),
]

sc = {
    "title": "Kentucky, 1955: Who Was at the Window?",
    "description": "In 1955, two families in Kelly, Kentucky said small glowing figures came to their farmhouse windows all night.",
    "lead_in": 0.05,
    "set": {"place": "village", "fog": 0.04, "eyes": 2, "moonlight": 8},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep028.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

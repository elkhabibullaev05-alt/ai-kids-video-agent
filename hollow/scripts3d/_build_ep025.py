"""Hollowmere Tales EP 25 (3D) - the Dover Demon, Dover, Massachusetts, April 1977. Writes scripts3d/ep025.json.
Recorded sightings, clearly labelled (sources: en.wikipedia.org/wiki/Dover_Demon,
wbsm.com/dover-demon-massachusetts-45-years-later (2022), cbsnews.com/boston (2025), wcvb.com (2026)):
- 21 April 1977, about 10:30 p.m.: Bill Bartlett (17), driving north on Farm Street with two friends (Mike Mazzocca,
  Andy Brodie, both 17), saw something on a low, tumbledown stone wall in his headlights. First thought: a cat or a dog.
  It was 3-4 feet tall, a big watermelon/egg-shaped head, glowing orange eyes ("like two orange marbles"), no visible
  nose or mouth, thin body, long thin arms and legs, long fingers, hairless peach-coloured skin. He drew a sketch.
- About midnight: John Baxter (15), walking home on Miller Hill Road (~1 mile away), saw a small figure walking upright
  ahead of him, with a big head; it ran off and he saw it standing by a tree, gripping it with long fingers. Also drew it.
- Next night, 22 April: Abby Brabham (15), driven by Will Taintor (18) on Springdale Avenue, saw a thin, hairless
  creature on all fours by the road; she said its eyes glowed GREEN. About the size of a goat.
- Investigator Loren Coleman interviewed the witnesses and named it "the Dover Demon". Nobody has explained it; it was
  never seen again. Some suggested a young animal (a moose calf), others a prank; the witnesses kept their story.
Continues EP 24 (the Pale Shepherd: 'You saw my light. Now I see yours.' Odo: 'Run.').
Short 1 (the rule / scariest moment) = hook beat 0 + Bartlett on the wall + 'no mouth' + loop line."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
chars["demon"] = {"name": "The Dover Demon", "voice": "am_onyx", "speed": 0.8, "pitch": -4, "color": [0.86, 0.66, 0.52],
                  "kind": "demon", "size": 0.8, "home": [3, 13]}
chars["bill"] = {"name": "Bill, 17", "voice": "am_eric", "speed": 1.05, "pitch": 1, "color": [0.15, 0.3, 0.55],
                 "kind": "human", "size": 0.9, "home": [-9, 9]}
chars["john"] = {"name": "John, 15", "voice": "am_puck", "speed": 1.05, "pitch": 2, "color": [0.5, 0.35, 0.12],
                 "kind": "human", "size": 0.8, "home": [-12, 13]}
chars["abby"] = {"name": "Abby, 15", "voice": "af_nicole", "speed": 1.05, "pitch": 1, "color": [0.55, 0.12, 0.35],
                 "kind": "human", "size": 0.8, "home": [-14, 8]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

STONE = {"type": "box", "color": [0.36, 0.35, 0.33], "visible": True}
props = [dict(STONE, id=f"w{i}", at=[-1.5 + i * 1.05, 13.6 + (i % 2) * 0.15, 0.0], scale=0.85 - (i % 3) * 0.08)
         for i in range(8)]
props += [dict(STONE, id="wt1", at=[0.6, 13.65, 0.95], scale=0.6), dict(STONE, id="wt2", at=[4.8, 13.7, 0.9], scale=0.55)]
HL = {"type": "ball", "color": [1.0, 0.97, 0.85], "glow": 14, "visible": False, "scale": 0.4}
props += [dict(HL, id="hl1", at=[-9, 6, 1.2]), dict(HL, id="hl2", at=[-7.6, 6, 1.2])]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (Odo and Mothwick skid to a stop, the demon rises on the wall) + big text hook + voice mid-danger
    L(N, "Two orange eyes were watching them from the stone wall. And they did not blink.", "wide",
      [["odo", "to:-6,9,0"], ["moth", "to:-4,9.5,2"], ["demon", "to:2.5,13.6,1.15"]], sfx="alarm",
      text="WHAT'S ON THE WALL?"),
    L("moth", "Odo, we ran from the Shepherd... straight into THAT?", "close:moth",
      [["moth", "shake"]], text="WHAT IS THAT?"),
    L("odo", "Don't move, Mothwick. It has no mouth. But it is looking right at us.", "close:demon",
      [["demon", "turn:front"]], sfx="suspicious", text="IT HAS NO MOUTH"),
    L(N, "This is a true story. Four teenagers saw this creature, in two nights.", "overhead",
      [["demon", "eyes_big"]], text="A TRUE STORY"),
    L(N, "Dover, Massachusetts. April 1977. A quiet town of old stone walls.", "close:odo",
      [["odo", "turn:front"]], text="DOVER, 1977"),
    # ---- sighting 1: Bill Bartlett ----
    L(N, "The night of April twenty-first. Half past ten. Bill was seventeen.", "close:bill",
      [["bill", "enter:left"], ["hl1", "show"], ["hl2", "show"]], sfx="suspicious", text="10:30 PM"),
    L(N, "He was driving down Farm Street with two friends, when his headlights hit the wall.", "wide",
      [["hl1", "drift:-4,10,1.2"], ["hl2", "drift:-2.6,10,1.2"], ["bill", "to:-5,10"]], text="FARM STREET"),
    L("bill", "There's something on the wall! Is that a cat? A dog?", "close:bill",
      [["bill", "jump"]], sfx="alarm"),
    L(N, "It was not a cat. And it was not a dog.", "close:demon",
      [["demon", "turn:front"], ["demon", "eyes_big"]], text="NOT A CAT"),
    L(N, "It was about four feet tall, with a huge head shaped like a watermelon.", "two:odo,demon",
      [["demon", "bounce"]], text="A WATERMELON HEAD"),
    L(N, "Its eyes glowed orange, like two marbles. Bill saw no nose and no mouth.", "close:demon",
      [["demon", "turn:front"]], sfx="suspicious", text="ORANGE EYES"),
    L(N, "Its arms and legs were long and thin. Its fingers wrapped around the stones.", "overhead",
      [["demon", "shake"]], text="LONG FINGERS"),
    L("bill", "Did you see it? Tell me you saw that thing!", "close:bill",
      [["bill", "shake"], ["hl1", "vanish"], ["hl2", "vanish"]]),
    L(N, "His friends had missed it. So when Bill got home, he drew what he saw.", "two:bill,odo",
      [["bill", "sad"]], text="HE DREW IT"),
    L("moth", "Odo, it's climbing down. Why is it climbing down?", "close:moth",
      [["demon", "to:3,11,0"], ["moth", "to:-5,7,1.5"], ["bill", "exit"]], sfx="alarm", text="IT'S CLIMBING DOWN"),
    # ---- sighting 2: John Baxter ----
    L(N, "Two hours later, about one mile away, a boy named John was walking home.", "close:john",
      [["john", "enter:left"]], text="MIDNIGHT"),
    L(N, "He was fifteen. On the dark road ahead, a small shape was walking toward him.", "wide",
      [["demon", "to:-6,15,0"], ["john", "to:-10,13"]], sfx="suspicious", text="A SMALL SHAPE"),
    L("john", "Hello? Who's there? Is that you, Mike?", "close:john",
      [["john", "turn:front"]]),
    L(N, "It was not Mike. It ran off the road, and stopped beside a tree.", "close:demon",
      [["demon", "to:-3,19,0"], ["demon", "turn:front"]], sfx="alarm", text="IT WAS NOT MIKE"),
    L(N, "John said it held the tree with long fingers. Its big head was turned toward him.", "overhead",
      [["john", "eyes_big"]], text="IT HELD THE TREE"),
    L("john", "I'm not staying here. I'm going home. Right now!", "close:john",
      [["john", "exit"]]),
    L(N, "John drew a picture too. And it looked just like Bill's.", "overhead",
      [["demon", "to:3,13.6,1.15"]], text="THE SAME DRAWING"),
    # ---- the rule ----
    L("odo", "Mothwick, the rule is simple. If it has no mouth, don't wait to hear it speak.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="DON'T WAIT"),
    # ---- sighting 3: Abby Brabham ----
    L(N, "The next night, fifteen-year-old Abby was riding home with a friend.", "close:abby",
      [["abby", "enter:left"], ["hl1", "show"], ["hl2", "show"]], text="THE NEXT NIGHT"),
    L(N, "On Springdale Avenue, she saw something crouching by the road.", "wide",
      [["hl1", "drift:-3,11,1.2"], ["hl2", "drift:-1.6,11,1.2"], ["demon", "to:1,12,0"]], sfx="alarm",
      text="BY THE ROAD"),
    L("abby", "Stop... no, don't stop! Keep driving! Its eyes are glowing!", "close:abby",
      [["abby", "shake"]]),
    L(N, "But Abby said its eyes glowed green. Not orange. Green.", "close:demon",
      [["demon", "eyes_big"]], sfx="suspicious", text="GREEN EYES?"),
    L("moth", "Orange eyes, green eyes... Odo, are there TWO of them?", "close:moth",
      [["moth", "shake"], ["abby", "exit"], ["hl1", "vanish"], ["hl2", "vanish"]], text="ARE THERE TWO?"),
    # ---- the investigator / no answer ----
    L(N, "An investigator named Loren Coleman talked to every witness. He called it the Dover Demon.", "overhead",
      [["demon", "turn:front"]], text="THE DOVER DEMON"),
    L(N, "Some people said it was a young animal, lost in the dark. Others said a joke.", "two:odo,moth",
      [["odo", "turn:moth"]], text="AN ANIMAL? A JOKE?"),
    L(N, "But the teenagers never changed their story. And no one ever proved what it was.", "close:demon",
      [["demon", "bounce"]], sfx="alarm", text="NEVER EXPLAINED"),
    L(N, "After those two nights, it was never seen again.", "wide",
      [["demon", "to:3,13.6,1.15"]], text="NEVER SEEN AGAIN"),
    # ---- Would YOU ----
    L(N, "So, would YOU drive down Farm Street at night, and look at the wall?", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="WOULD YOU LOOK?"),
    L("moth", "Not me. I would close my eyes and fly very, very fast.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the creature lifted one long finger. And it pointed behind them.", "close:demon",
      [["demon", "turn:front"], ["demon", "shake"]], sfx="alarm", text="IT POINTED"),
    L(N, "Odo's lantern flickered. Something tall was coming up the road.", "wide",
      [["shepherd", "to:8,17,0"], ["all", "shake"]], sfx="suspicious", text="SOMETHING TALL"),
    L("shepherd", "Lantern-bearer. Even the little ones warn you now.", "close:shepherd",
      [["shepherd", "turn:front"]], text="IT FOUND US"),
    L(N, "Was the Dover Demon a warning? Subscribe, so you don't miss the next tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="alarm", text="WHAT WAS IT?"),
]

sc = {
    "title": "Dover, 1977: What Was on the Stone Wall?",
    "description": "In April 1977, four teenagers in Dover, Massachusetts saw a creature with a huge head and glowing eyes.",
    "lead_in": 0.05,
    "set": {"place": "forest", "fog": 0.06, "eyes": 2, "moonlight": 2.4},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep025.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

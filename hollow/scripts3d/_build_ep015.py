"""Hollowmere Tales EP 15 (3D) — The lost Ninth Legion. Writes scripts3d/ep015.json.
Documented history + recorded ghost story: Legio IX Hispana (about 5,000 men), based at York (Eboracum);
mauled in a night attack by the Caledonians in 82 AD (Tacitus); last record in Britain = York inscription of 108 AD;
by 122 AD the Sixth Legion held York; a list of legions made in Rome around 165 AD no longer names the Ninth.
Theories: destroyed in northern Britain / moved to the Rhine (Nijmegen roof tile stamped by the Ninth, found 1959, c. 125 AD) /
lost in the East (132-135 or 161 AD). Silchester eagle: wingless bronze eagle found 9 Oct 1866 by Rev. J. G. Joyce,
inspired Rosemary Sutcliff's 'The Eagle of the Ninth' (1954). Treasurer's House, York, 1953: Harry Martindale (18, apprentice
plumber) heard a trumpet in the cellar, saw a soldier in a plumed helmet come out of the wall, a horse and pairs of Roman
soldiers visible only from the knees up, walking on the buried Roman road; he fell from his ladder. Nobody knows who they were."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 6])
chars["moth"] = dict(chars["moth"], home=[-3.5, 5])
chars["harry"] = {"name": "Harry", "voice": "am_puck", "speed": 1.05, "pitch": 1, "color": [0.15, 0.22, 0.35],
                  "kind": "human", "size": 0.95, "home": [3, 7]}
RED = [0.55, 0.06, 0.05]
for i, (x, y) in enumerate([(1, 10), (3.5, 10), (1, 13), (3.5, 13)]):  # the living legion
    chars[f"l{i+1}"] = {"name": "Legionary", "voice": "bm_daniel", "speed": 0.95, "pitch": -2, "color": RED,
                        "kind": "soldier", "size": 1.0, "home": [x, y]}
for i, (x, y) in enumerate([(2, 9), (4.5, 9), (2, 12), (4.5, 12), (2, 15)]):  # ghosts, cut off at the knees
    chars[f"g{i+1}"] = {"name": "Ghost soldier", "voice": "bm_daniel", "speed": 0.9, "pitch": -3, "color": [0.5, 0.8, 0.8],
                        "kind": "soldier", "ghost": True, "size": 1.0, "home": [x, y]}
L4 = ["l1", "l2", "l3", "l4"]; G5 = ["g1", "g2", "g3", "g4", "g5"]

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big hook + voice at frame 1
    L(N, "Five thousand Roman soldiers marched north. Then they vanished from history.", "wide",
      [[k, "to:%s" % xy] for k, xy in zip(L4, ("0,7.5", "2.5,7.5", "0,10.5", "2.5,10.5"))] + [["odo", "shake"]], text="5,000 SOLDIERS VANISHED"),
    L(N, "And in 1953, a boy in York saw soldiers walk out of a wall.", "close:odo", [["odo", "eyes_big"]], sfx="suspicious", text="OUT OF THE WALL"),
    L("odo", "Mothwick... do you hear marching?", "close:odo", [["odo", "turn:l1"]]),
    L("moth", "Soldiers don't march at midnight, Odo. Not anymore.", "close:moth", [["moth", "shake"]]),
    L(N, "This is a true story. They were the Ninth Legion of Rome.", "two:l1,l2", [["l1", "jump"], ["l2", "jump"]], text="THE NINTH LEGION"),
    L(N, "Almost two thousand years ago, their great fortress stood where York is today.", "overhead", text="YORK, ENGLAND"),
    L(N, "In the year 82, enemies from the north attacked their camp at night.", "close:l1", [["l1", "shake"], ["l3", "shake"]], sfx="suspicious", text="AD 82"),
    L(N, "The legion held on. And it kept marching.", "wide", [[k, "to:%s" % xy] for k, xy in zip(L4, ("1,16", "3.5,16", "1,19", "3.5,19"))]),
    L(N, "The last words they left in Britain were carved in stone, at York, in the year 108.", "close:l2", [["l2", "turn:front"]], text="THE LAST STONE: 108"),
    L(N, "After that, silence. No battle. No goodbye. Nothing.", "wide", [[k, "exit"] for k in L4], text="THEN... NOTHING"),
    L("odo", "Where did they go?", "close:odo", [["odo", "turn:front"]]),
    L(N, "By the year 122, a different legion was living in their fortress.", "overhead", sfx="suspicious"),
    L(N, "And on a list of Rome's legions made around 165, the Ninth was simply gone.", "close:moth", [["moth", "eyes_big"]], text="ERASED FROM THE LIST"),
    # ---- the theories ----
    L(N, "Some said they were wiped out in the misty hills of the north.", "wide", text="LOST IN THE MIST?"),
    L("odo", "Five thousand soldiers can't just disappear.", "close:odo", [["odo", "eyes_big"]]),
    L(N, "But in 1959, diggers in the Netherlands found a roof tile stamped with the Ninth's name.", "prop:tile", [["tile", "show"]], text="1959"),
    L("moth", "So some of them crossed the sea?", "close:moth", [["tile", "bounce"]]),
    L(N, "Maybe. Others think the legion was sent far to the east, and never came back.", "prop:tile", [["tile", "vanish"]], text="SENT EAST?"),
    L(N, "Nobody knows how the Ninth ended. Not one record tells us.", "two:odo,moth", [["odo", "sad"]], text="NOBODY KNOWS"),
    L("moth", "Then their story isn't finished.", "close:moth", [["moth", "turn:odo"]]),
    L(N, "In 1866, a priest digging in an old Roman town found a bronze eagle. Its wings were gone.", "prop:eagle",
      [["eagle", "show"], ["eagle", "spin"]], sfx="suspicious", text="THE WINGLESS EAGLE"),
    L(N, "A writer, Rosemary Sutcliff, imagined it was the lost eagle of the Ninth. She wrote a famous book.", "prop:eagle", [["eagle", "bounce"]]),
    L(N, "But the ghost story is even stranger. And it is written down too.", "wide", [["eagle", "vanish"]], sfx="suspicious"),
    # ---- Short 1 segment (the scariest moment) ----
    L(N, "1953. An eighteen-year-old plumber, Harry Martindale, was alone in a cellar in York.", "close:harry",
      [["harry", "enter:left"], ["harry", "turn:front"]], text="ALONE IN THE CELLAR"),
    L(N, "Then he heard a trumpet. Far away. Getting louder.", "close:harry", [["harry", "eyes_big"]], sfx="suspicious", text="A TRUMPET... LOUDER"),
    L(N, "A soldier in a plumed helmet walked straight out of the wall.", "two:harry,g1", [["g1", "enter:right"], ["harry", "shake"]], text="OUT OF THE WALL"),
    L(N, "Then more. Pairs of Roman soldiers. But he could only see them from the knees up.", "wide",
      [[k, "enter:right"] for k in G5[1:]] + [["harry", "turn:g1"]], text="NO LEGS"),
    L("harry", "They were walking on a road I couldn't see!", "close:harry", [["harry", "shake"]], sfx="suspicious"),
    L(N, "Deep under the cellar floor ran an old Roman road. The ghosts were marching on it.", "two:harry,g1",
      [[k, "to:%s" % xy] for k, xy in zip(G5, ("-14,9", "-11.5,9", "-14,12", "-11.5,12", "-14,15"))], text="THE BURIED ROAD"),
    # ---- ending + cliffhanger ----
    L(N, "Harry fell off his ladder. He told the story for the rest of his life.", "close:harry", [["harry", "exit"]]),
    L(N, "Later, experts said the clothes he described matched Roman soldiers from a later time.", "overhead", text="THE CLOTHES MATCHED"),
    L(N, "Were they the lost Ninth? Or later soldiers? No one can say.", "two:odo,moth", [["moth", "turn:odo"]], text="WHO WERE THEY?"),
    L("odo", "Mothwick... the ground is shaking.", "close:odo", [["odo", "shake"], ["moth", "shake"]], sfx="suspicious"),
    L("moth", "That's not the ground. That's feet. Lots of feet.", "close:moth", [["moth", "eyes_big"]]),
    L(N, "Out of the fog, the legion turned. And marched straight toward them.", "wide",
      [[k, "to:%s" % xy] for k, xy in zip(G5, ("-6,10", "-3.5,10", "-6,13", "-3.5,13", "-5,16"))] + [["all", "look:odo"]], text="THEY'RE COMING"),
    L(N, "Who is leading the lost legion? The next tale begins right here.", "close:g1", [["g1", "turn:odo"], ["odo", "shake"]], text="WHO LEADS THEM? SUBSCRIBE!"),
]

sc = {
    "title": "Where Did Rome's 5,000 Soldiers Go?",
    "description": "Five thousand Roman soldiers marched north. Then they vanished from history.",
    "lead_in": 0.05,
    "set": {"place": "village", "fog": 0.04, "eyes": 5, "moonlight": 2.6},
    "chars": chars,
    "props": [
        {"id": "tile", "type": "box", "color": [0.6, 0.3, 0.18], "at": [0, 9, 1.4], "visible": False, "scale": 0.7},
        {"id": "eagle", "type": "star", "color": "gold", "at": [0, 9, 1.6], "visible": False, "scale": 0.8},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep015.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats))

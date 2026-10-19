"""Hollowmere Tales EP 13 (3D) — The Real Sleepy Hollow. Writes scripts3d/ep013.json.
Recorded legend: Washington Irving, 'The Legend of Sleepy Hollow' (1820); Old Dutch Church c.1685;
anonymous Hessian soldier killed by a cannonball at the Battle of White Plains (1776), burial never recorded;
Irving buried in Sleepy Hollow Cemetery (1859); North Tarrytown renamed Sleepy Hollow (1996)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 6])
chars["moth"] = dict(chars["moth"], home=[-3.5, 5])
chars["rider"] = {"name": "The Headless Horseman", "voice": "am_onyx", "speed": 0.8, "pitch": -5, "color": [0.02, 0.02, 0.03],
                  "kind": "horseman", "size": 1.0, "home": [6, 13]}
chars["ichabod"] = {"name": "Ichabod Crane", "voice": "bm_lewis", "speed": 1.05, "pitch": 1, "color": [0.35, 0.28, 0.18],
                    "kind": "human", "size": 1.05, "home": [-4, 11]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big hook + voice at frame 1
    L(N, "What gallops through this graveyard every night... with no head at all?", "close:rider", [["rider", "shake"], ["odo", "shake"]], text="HE HAS NO HEAD"),
    L(N, "This place is real. Sleepy Hollow, New York. Its stone church was built around 1685.", "two:odo,moth", [["odo", "eyes_big"]], text="A REAL PLACE"),
    L("odo", "Mothwick... did you hear hooves?", "close:odo", [["odo", "turn:rider"]]),
    L("moth", "Hooves. And no breathing.", "close:moth", [["moth", "shake"]]),
    L(N, "The legend was first written down in 1820, by a writer named Washington Irving.", "overhead", text="WRITTEN DOWN IN 1820"),
    L(N, "As a boy, Irving explored these hills and listened to the old ghost stories.", "wide", [["moth", "to:-5,9"]]),
    L(N, "And the scariest story was about a rider. A soldier from a war long ago.", "close:rider", [["rider", "turn:front"]], sfx="suspicious"),
    L(N, "The tale says a cannonball took his head in battle. So every night, he rides out to find it.", "close:rider", [["rider", "shake"]]),
    L(N, "Here is the strange part. There is a real record from the Battle of White Plains, in 1776.", "overhead", text="1776"),
    L(N, "A soldier lost his head to a cannonball there. Nobody ever wrote down where he was buried.", "wide", sfx="suspicious"),
    L("moth", "So he could be under any of these stones.", "close:moth", [["odo", "eyes_big"]]),
    L("odo", "Please don't say that.", "close:odo", [["odo", "shake"]]),
    L(N, "Irving's story follows a schoolteacher named Ichabod Crane. Tall, skinny, and scared of everything.", "close:ichabod", [["ichabod", "enter:left"]]),
    L("ichabod", "Ghosts? Nonsense! I am a learned man. I fear nothing.", "close:ichabod", [["ichabod", "happy"]]),
    L(N, "One autumn night, Ichabod rode home alone from a party, right past this churchyard.", "wide", [["ichabod", "to:0,12"]]),
    L(N, "Then, in the dark, he saw a huge shape standing very still beside the road.", "two:ichabod,rider", [["rider", "turn:ichabod"]], sfx="suspicious", text="SOMETHING IS WAITING"),
    L("ichabod", "Who... who is there?", "close:ichabod", [["ichabod", "shake"]]),
    L(N, "It did not answer. It just began to follow him. Clip. Clop. Faster and faster.", "close:rider", [["rider", "to:4,11"]]),
    L(N, "Then the moonlight showed him the truth. The rider had no head.", "close:rider", [["ichabod", "eyes_big"]], text="NO HEAD"),
    L(N, "And on its shoulders sat something round... and glowing.", "prop:pumpkin", [["pumpkin", "show"]], sfx="suspicious"),
    # ---- Short 1 segment (the rule) ----
    L(N, "The legend has one rule. He cannot cross the bridge by the old church.", "wide", [["ichabod", "to:-1,7.5"]], text="THE ONE RULE"),
    L("ichabod", "The bridge! I just need to reach the bridge!", "close:ichabod", [["ichabod", "jump"]]),
    L(N, "Ichabod crossed it. He looked back. The rider rose up...", "close:rider", [["rider", "jump"]]),
    L(N, "and threw his glowing head right at him!", "two:ichabod,rider", [["pumpkin", "vanish"], ["thrown", "show"]], sfx="alarm"),
    L(N, "So reach the bridge. But never, ever look back.", "close:odo", [["odo", "eyes_big"]], text="NEVER LOOK BACK"),
    # ---- aftermath ----
    L(N, "The next morning, the villagers searched the road by the bridge.", "wide", [["ichabod", "exit"], ["thrown", "vanish"]]),
    L(N, "They found his horse. They found his hat. And beside it, a smashed pumpkin.", "prop:hat", [["hat", "show"], ["smashed", "show"]], text="A SMASHED PUMPKIN"),
    L(N, "Ichabod Crane was never seen in Sleepy Hollow again.", "prop:smashed", sfx="suspicious", text="NEVER SEEN AGAIN"),
    L("moth", "A pumpkin. Odo... was it really just a pumpkin?", "close:moth", [["moth", "turn:odo"]]),
    L("odo", "I am not staying to find out.", "close:odo", [["odo", "shake"]]),
    L(N, "Washington Irving is buried here too, in Sleepy Hollow Cemetery, since 1859.", "overhead"),
    L(N, "And in 1996, the town next to the church changed its name to Sleepy Hollow. On purpose.", "wide", text="RENAMED IN 1996"),
    L(N, "Some say the Headless Horseman still rides here on autumn nights, looking for what he lost.", "close:rider", [["rider", "to:2,12"]]),
    L("odo", "Mothwick... the hoofbeats stopped.", "close:odo", [["odo", "turn:rider"]]),
    L("moth", "That means he found something.", "close:moth", [["moth", "eyes_big"]]),
    L(N, "Then, right behind them, something round rolled out of the dark.", "two:odo,moth", [["head", "show"], ["all", "look:odo"]], sfx="suspicious"),
    L(N, "It was glowing. And it was not a pumpkin. The next tale begins right there.", "prop:head", [["head", "bounce"]], text="WHO IS BEHIND YOU?"),
]

sc = {
    "title": "What Rides Through Sleepy Hollow at Night?",
    "description": "This place is real. A legend first written down in 1820, a real record from 1776, and a rider with no head.",
    "lead_in": 0.05,
    "set": {"place": "graveyard", "fog": 0.03, "eyes": 10, "moonlight": 2.0},
    "chars": chars,
    "props": [
        {"id": "pumpkin", "type": "ball", "color": "orange", "on": "rider", "visible": False, "scale": 0.5, "glow": 6},
        {"id": "thrown", "type": "ball", "color": "orange", "at": [-1.2, 6.2, 1.6], "visible": False, "scale": 0.5, "glow": 6},
        {"id": "hat", "type": "box", "color": [0.05, 0.04, 0.04], "at": [-1.8, 6.4, 0.15], "visible": False, "scale": 0.45},
        {"id": "smashed", "type": "ball", "color": "orange", "at": [-0.4, 6.0, 0.15], "visible": False, "scale": 0.45},
        {"id": "head", "type": "ball", "color": "orange", "at": [-4.8, 3.4, 0.45], "visible": False, "scale": 0.5, "glow": 6},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep013.json"), "w"), indent=1)
print("beats", len(beats))

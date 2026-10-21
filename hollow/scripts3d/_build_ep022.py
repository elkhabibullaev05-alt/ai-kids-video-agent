"""Hollowmere Tales EP 22 (3D) - the Mothman of Point Pleasant. Writes scripts3d/ep022.json.
Recorded sightings + folklore, clearly labelled (sources: en.wikipedia.org/wiki/Mothman,
history.com/articles/mothman-legend (15 Oct 2026), npr.org/2025/10/01/g-s1-90648/mothman-festival-point-pleasant-west-virginia):
- November 1966: a group of gravediggers near Clendenin, West Virginia, reported a man-like winged figure gliding
  over the trees (History.com: 'a 6-foot-tall winged creature soaring through the trees').
- 15 Nov 1966, near midnight: two young couples, Roger and Linda Scarberry and Steve and Mary Mallette, driving past the
  'TNT area' - an abandoned World War II munitions plant about 7 miles north of Point Pleasant - told police they saw a
  large creature whose eyes 'glowed red', standing by the road (Wikipedia). Linda: about seven feet tall, with wings.
  They sped away; the creature flew after the car, making a screeching sound (Wikipedia); 'like a record player at high
  speed' (History.com). Roger: 'there were four of us who saw it' (History.com).
- 16 Nov 1966, Point Pleasant Register: 'Couples See Man-Sized Bird ... Creature ... Something!'
- A newspaper editor (The Athens Messenger) named it 'Mothman'. About 100 sightings were reported over the years.
- Sceptics: in 1966 a snowy owl with a nearly five-foot wingspan was found near Point Pleasant; some say a big owl explains it
  (Wikipedia; the bird's fate is left out). The only red-eye report some researchers accept is second-hand (Radford).
- Today the town has a statue and a festival every September (NPR).
- LEFT OUT: the December 1967 bridge collapse (mass casualties - channel rule).
Continues EP 21 (Mothwick vanished when the red ghost ship came to shore).
Short 1 = hook (beat 0) + the TNT-area chase (beats 9-15) - loops back to beat 0."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-8, 5])
chars["moth"] = dict(chars["moth"], home=[-5.5, 4.5])
chars["mm"] = {"name": "The Winged Figure", "voice": "am_onyx", "speed": 0.8, "pitch": -5, "color": [0.42, 0.42, 0.46],
               "kind": "winged", "up": True, "size": 1.0, "home": [6, 20]}
chars["roger"] = {"name": "Roger Scarberry", "voice": "am_michael", "speed": 1.0, "pitch": 0, "color": [0.15, 0.25, 0.45],
                  "kind": "human", "size": 0.9, "home": [-11, 7]}
chars["linda"] = {"name": "Linda Scarberry", "voice": "af_bella", "speed": 1.0, "pitch": 0, "color": [0.55, 0.15, 0.2],
                  "kind": "human", "size": 0.85, "home": [-9, 8]}

# ---- the car: body boxes + cabin + glowing headlights / red tail lights; moves as one ----
CAR0 = (-3.0, 11.0)
parts = []
for i, dx in enumerate((-1.2, 0.0, 1.2)):
    parts.append(("car%d" % i, "box", [0.4, 0.06, 0.05], 0.25, (dx, 0, 0.0), 1.0))
parts.append(("cab", "box", [0.25, 0.25, 0.3], 0.15, (-0.2, 0, 1.0), 0.85))
for k, dy in enumerate((-0.4, 0.4)):
    parts.append(("head%d" % k, "ball", [1.0, 0.95, 0.7], 18, (1.85, dy, 0.6), 0.2))
    parts.append(("tail%d" % k, "ball", [1.0, 0.05, 0.03], 10, (-1.85, dy, 0.6), 0.14))
EYE = ("careye", (0.0, -5.0, 1.6))  # invisible camera target in front of the car


def car_props():
    out = [{"id": pid, "type": typ, "color": col, "glow": glow, "at": [CAR0[0] + dx, CAR0[1] + dy, z], "scale": s}
           for pid, typ, col, glow, (dx, dy, z), s in parts]
    out.append({"id": EYE[0], "type": "ball", "color": "white", "at": [CAR0[0] + EYE[1][0], CAR0[1] + EYE[1][1], EYE[1][2]],
                "scale": 0.1, "visible": False})
    return out


def car(x, y):
    return [[pid, "to:%.2f,%.2f,%.2f" % (x + dx, y + dy, z)] for pid, _, _, _, (dx, dy, z), _ in parts] + \
        [[EYE[0], "to:%.2f,%.2f,%.2f" % (x + EYE[1][0], y + EYE[1][1], EYE[1][2])]]


def car_do(act):
    return [[pid, act] for pid, *_ in parts]


N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion + big text hook + voice mid-tension at frame 1 (car speeding, red eyes in the dark)
    L(N, "Four people saw red eyes by the road. Then it chased their car.", "prop:careye",
      car(5, 11) + [["mm", "to:1,18,1"]], text="DON'T STOP THE CAR"),
    L("odo", "Mothwick! Mothwick, where are you? The ship is gone!", "close:odo", [["odo", "shake"]], sfx="alarm",
      text="WHERE IS MOTHWICK?"),
    L("moth", "Up here, Odo! The wind dropped me in these trees!", "two:odo,moth", [["moth", "rise"], ["odo", "jump"]],
      text="SHE'S BACK"),
    L("moth", "But Odo... something up here is bigger than me. Much bigger.", "close:moth", [["moth", "eyes_big"]] + car(-14, 11)),
    L(N, "This is a true story, from real police reports and newspapers.", "wide", [["mm", "to:6,15,4"]],
      sfx="suspicious", text="A TRUE STORY"),
    L(N, "Point Pleasant, West Virginia. November, 1966.", "overhead", [["mm", "spin"]], text="NOVEMBER 1966"),
    L(N, "First, a group of men digging graves near Clendenin looked up.", "close:odo", [["odo", "turn:mm"]]),
    L(N, "Something shaped like a man glided over the trees. With wings.", "close:mm",
      [["mm", "to:2,14,5"]], sfx="alarm", text="A MAN WITH WINGS"),
    L("odo", "A man can't fly. Can he, Mothwick?", "two:odo,moth", [["moth", "shake"]]),
    L("moth", "Not without wings. And this one had very big wings.", "close:moth", [["moth", "eyes_big"]]),
    # ---- the TNT area chase (Short 1 segment) ----
    L(N, "Three days later, near midnight, two young couples went driving.", "prop:careye",
      car(-10, 11) + [["roger", "enter:left"], ["linda", "enter:left"]], text="NEAR MIDNIGHT"),
    L(N, "Roger and Linda Scarberry. Steve and Mary Mallette.", "two:roger,linda", [["roger", "turn:front"]],
      text="FOUR WITNESSES"),
    L(N, "They passed the TNT area. An old war factory, seven miles out of town.", "overhead",
      car(-4, 11) + [["roger", "exit"], ["linda", "exit"]], text="THE TNT AREA"),
    L(N, "There, by the side of the road, something stood up.", "close:mm", [["mm", "to:-1,12,0"], ["mm", "eyes_big"]],
      sfx="alarm", text="SOMETHING STOOD UP"),
    L("linda", "It was like a man. Seven feet tall. With wings. And the eyes!", "close:linda",
      [["linda", "enter:left"], ["linda", "shake"]], text="7 FEET TALL"),
    L(N, "They told police its eyes glowed red.", "close:mm", [["mm", "turn:front"]], sfx="suspicious",
      text="ITS EYES GLOWED RED"),
    L(N, "Linda said she could not see its face. Only those eyes.", "close:linda", [["linda", "eyes_big"]],
      text="ONLY THE EYES"),
    L(N, "They raced away. And it flew after the car, screeching.", "prop:careye",
      car(9, 11) + [["mm", "to:5,12,4"], ["linda", "exit"]], sfx="alarm", text="IT FLEW AFTER THEM"),
    L(N, "Its cry, they said, sounded like a record spinning much too fast.", "close:mm", [["mm", "shake"]],
      sfx="suspicious", text="A SCREECH"),
    L("roger", "If I had seen it by myself, I wouldn't have said anything. But there were four of us.", "close:roger",
      [["roger", "enter:left"], ["roger", "shake"]], text="FOUR OF US SAW IT"),
    L("odo", "Four people. All the same story.", "close:odo", [["odo", "eyes_big"], ["roger", "exit"]]),
    # ---- the newspapers ----
    L(N, "The next day, the town newspaper printed it.", "wide", car(18, 11), text="NOVEMBER 16, 1966"),
    L(N, "Couples see man-sized bird. Creature. Something!", "close:moth", [["moth", "spin"]], sfx="suspicious",
      text="MAN-SIZED BIRD?"),
    L(N, "Another newspaper gave it a name. Mothman.", "close:mm", [["mm", "rise"]], text="MOTHMAN"),
    L("moth", "Mothman? Odo, I am a moth. I promise it's not me!", "close:moth", [["moth", "jump"]]),
    L(N, "Over the years, people reported about a hundred sightings.", "overhead",
      [["mm", "to:-4,15,5"], ["mm", "spin"]], text="ABOUT 100 SIGHTINGS"),
    L(N, "On roads. Over fields. Even near the old factory, again and again.", "close:mm", [["mm", "to:3,13,3"]],
      sfx="alarm", text="AGAIN AND AGAIN"),
    L(N, "People said it rose straight up from the ground. It chased cars. It even followed airplanes.", "overhead",
      [["mm", "to:-3,14,7"]], text="IT ROSE FROM THE GROUND"),
    L("moth", "Odo, your lantern. It's looking at your lantern.", "close:moth", [["moth", "shake"]]),
    L("odo", "Mothwick, hide your light. Right now.", "two:odo,moth", [["moth", "sad"]]),
    # ---- what is real ----
    L(N, "Some scientists say it was an owl. A very big owl.", "wide", [["mm", "to:7,16,2"]], text="AN OWL?"),
    L(N, "That year, a snowy owl was found nearby. Its wings were nearly five feet wide.", "close:odo",
      [["odo", "turn:front"]], text="5-FOOT WINGS"),
    L(N, "But an owl is not seven feet tall. And it does not chase a car.", "close:mm",
      [["mm", "turn:odo"]], sfx="suspicious", text="NOT AN OWL?"),
    L(N, "Nobody has ever proved what the four friends saw that night.", "overhead", [["mm", "spin"]],
      text="NEVER PROVED"),
    L(N, "Today, Point Pleasant has a silver statue of it. And a festival every year.", "wide",
      [["odo", "laugh"]], text="A STATUE AND A FESTIVAL"),
    # ---- Would YOU ----
    L(N, "So, would YOU stop the car on that road at midnight?", "close:odo", [["odo", "eyes_big"]],
      sfx="suspicious", text="WOULD YOU STOP?"),
    L("moth", "Never. I'd fly home so fast my wings would smoke.", "close:moth", [["moth", "spin"]]),
    # ---- cliffhanger ----
    L(N, "Then, behind them, two red lights opened in the dark.", "close:mm",
      [["mm", "to:-1,9,0"], ["all", "shake"]], sfx="alarm", text="BEHIND YOU"),
    L("mm", "Little moth. Come to the light.", "close:mm", [["mm", "turn:moth"]], text="COME TO THE LIGHT"),
    L("moth", "Odo... I can't stop my wings. I can't stop!", "close:moth", [["moth", "to:-1,8,4"]]),
    L("odo", "Mothwick! Don't look at its eyes!", "close:odo", [["odo", "shake"]], text="DON'T LOOK"),
    L(N, "Where is it taking her? Subscribe, so you don't miss the next tale.", "close:mm",
      [["mm", "to:2,16,6"], ["moth", "to:2,15,6"]], sfx="alarm", text="WHERE IS IT GOING?"),
]

sc = {
    "title": "Four Saw Red Eyes. Then It Chased Them.",
    "description": "Four people saw red eyes by the road. Then it chased their car.",
    "lead_in": 0.05,
    "set": {"place": "forest", "fog": 0.07, "eyes": 2, "moonlight": 2.2},
    "chars": chars,
    "props": car_props(),
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep022.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

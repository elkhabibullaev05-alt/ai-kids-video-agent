"""Hollowmere Tales EP 24 (3D) - the Paulding Light, Michigan. Writes scripts3d/ep024.json.
Recorded sightings + folklore + a scientific test, clearly labelled (sources: en.wikipedia.org/wiki/Paulding_Light,
npr.org/transcripts/748565575 (NPR 2019), miningjournal.net 2016 'mysterious light draws thrill seekers to Paulding forest'):
- A light seen in a valley outside Paulding, in Michigan's Upper Peninsula, near Watersmeet; viewing spot off US 45 on
  Robbins Pond Road. Reports go back to the 1960s; first recorded sighting 1966, when a group of teenagers reported it
  to the local sheriff. Said to appear nearly every night; several times on a typical night (NPR).
- Legends: the lantern of a railroad brakeman who died trying to stop a train from hitting stopped railway cars;
  the ghost of a mail carrier; a grandparent searching for a lost grandchild with a lantern.
- Visitors: it seems to move up and down, red lights appear (NPR). Thousands of visitors; the local store sells
  Paulding Light souvenirs and says the "mystery is still unsolved".
- Science: October 1990 investigators (telescope, spectroscope, travel times) and in 2010 Michigan Tech students
  (telescope; recreated colours with police flashers and high/low beams) concluded it is the head- and tail-lights of
  cars on US 45, nearly five miles away, bent over the hills by a stable layer of air. Some residents were angry; many
  still don't believe it.
Continues EP 23 (the Pale Shepherd: 'Next time, the hunt rides for your light').
Short 1 (the rule / scariest moment) = hook beat 0 + beats about 'every night since 1966' + the red light."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-5, 5])
chars["moth"] = dict(chars["moth"], home=[-2.5, 4.5])
chars["brake"] = {"name": "The Brakeman", "voice": "bm_lewis", "speed": 0.85, "pitch": -3, "color": [0.12, 0.16, 0.3],
                  "kind": "human", "size": 1.0, "home": [2.5, 45]}
chars["teen"] = {"name": "A Teenager, 1966", "voice": "am_eric", "speed": 1.05, "pitch": 1, "color": [0.55, 0.12, 0.1],
                 "kind": "human", "size": 0.85, "home": [-9, 9]}
chars["sheriff"] = {"name": "The Sheriff", "voice": "am_michael", "speed": 0.95, "pitch": -1, "color": [0.35, 0.3, 0.2],
                    "kind": "human", "size": 1.0, "home": [-13, 12]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 18], size=0.85)

GL = {"type": "ball", "color": [1.0, 0.97, 0.85], "glow": 14}
props = [
    dict(GL, id="pl", at=[1.5, 21, 3.4], scale=0.85, visible=True),           # the Paulding Light, far in the valley
    dict(GL, id="pr", at=[7, 34, 3.0], scale=0.5, visible=False, color=[1, 0.08, 0.05]),  # the red light
    dict(GL, id="lan", on="brake", scale=0.35, visible=False, color=[1, 0.75, 0.35], glow=10),  # brakeman's lantern
    dict(GL, id="hl1", at=[-30, 44, 2.0], scale=0.4, visible=False),       # car headlights (the 2010 test)
    dict(GL, id="hl2", at=[-28.6, 44, 2.0], scale=0.4, visible=False),
]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (Odo and Mothwick run, the light rushes toward them) + big text hook + voice mid-danger at frame 1
    L(N, "A light was coming through the trees. And it was not Odo's lantern.", "wide",
      [["odo", "to:-3,7,0"], ["moth", "to:-1,7,2"], ["pl", "drift:1,14,2.8"]], sfx="alarm", text="DON'T FOLLOW THE LIGHT"),
    L("moth", "Odo, stop! Is that the hunt? Is it coming for your light?", "close:moth",
      [["moth", "shake"]], text="IS IT THE HUNT?"),
    L("odo", "No hooves. No horns. Just a light... floating over the road.", "close:odo",
      [["odo", "turn:front"], ["pl", "bounce"]], sfx="suspicious"),
    L(N, "This is a true story. People have watched this light for almost sixty years.", "overhead",
      [["pl", "drift:6,30,3.4"]], text="A TRUE STORY"),
    L(N, "Paulding, Michigan. A tiny place, deep in the northern woods.", "close:odo",
      [["odo", "turn:pl"]], text="PAULDING, MICHIGAN"),
    L(N, "At the end of a dark forest road, there is a valley.", "wide",
      [["odo", "to:-2,8,0"], ["moth", "to:0,8,2"]], sfx="suspicious", text="THE VALLEY"),
    L(N, "And almost every night, a light appears in it.", "two:odo,moth",
      [["pl", "bounce"], ["moth", "eyes_big"]], text="EVERY NIGHT"),
    L(N, "The first report we know of came in 1966.", "close:teen",
      [["teen", "enter:left"]], text="1966"),
    L(N, "A group of teenagers saw it, and they went to the sheriff.", "two:teen,sheriff",
      [["sheriff", "enter:left"], ["teen", "turn:sheriff"]], sfx="alarm", text="THEY TOLD THE SHERIFF"),
    L("teen", "Sheriff, there's a light out in the valley! It moves, and it glows!", "close:teen",
      [["teen", "jump"]], text="IT MOVES"),
    L("sheriff", "A light? Out there? There's nothing out there but trees.", "close:sheriff",
      [["sheriff", "turn:pl"]]),
    L(N, "But the light came back the next night. And the next. And the next.", "overhead",
      [["pl", "drift:2,26,4"], ["teen", "exit"], ["sheriff", "exit"]], sfx="suspicious", text="IT CAME BACK"),
    L(N, "People say it rises and falls. It grows bright, then fades away.", "wide",
      [["pl", "drift:2,26,1.5"]], text="BRIGHT... THEN GONE"),
    L(N, "And sometimes, a second light shows up beside it. A red one.", "close:moth",
      [["pr", "show"], ["moth", "eyes_big"]], sfx="alarm", text="A RED LIGHT"),
    L("moth", "Odo, there are two now. One of them is red. Why is it red?", "two:odo,moth",
      [["moth", "shake"], ["pr", "drift:4,26,2.2"]]),
    L(N, "So who carries the light? The old tales give three answers.", "close:odo",
      [["odo", "turn:front"], ["brake", "to:2.5,12"]], text="WHO CARRIES IT?"),
    # ---- the legends ----
    L(N, "The first tale: a railroad brakeman, long ago.", "close:brake",
      [["brake", "turn:front"], ["lan", "show"]], sfx="suspicious", text="THE BRAKEMAN"),
    L(N, "The story says he tried to stop a train before it crashed into cars on the track.", "wide",
      [["brake", "shake"]], text="STOP THE TRAIN"),
    L("brake", "Stop! Stop the train! There are cars on the line!", "close:brake",
      [["brake", "jump"]], sfx="alarm"),
    L(N, "He never came home. The legend says he still swings his lantern in the valley.", "overhead",
      [["brake", "to:9,26,0"]], text="HE NEVER CAME HOME"),
    L(N, "The second tale says it is a mail carrier, still riding his lonely route.", "close:odo",
      [["odo", "sad"]], text="THE MAIL CARRIER"),
    L(N, "And the third tale: a grandparent with a lantern, searching for a lost grandchild.", "two:odo,moth",
      [["moth", "sad"]], sfx="suspicious", text="STILL SEARCHING"),
    L("moth", "Searching every night? For sixty years? That's the saddest light in the world.", "close:moth",
      [["moth", "sad"]]),
    # ---- the rule / scariest moment (Short 1) ----
    L("odo", "Mothwick, if a light calls you into the dark, you never follow it.", "close:odo",
      [["odo", "shake"], ["pl", "drift:1,16,2.6"]], text="NEVER FOLLOW IT"),
    L(N, "Then the white light stopped. And it began to come closer.", "wide",
      [["pl", "drift:0,13,2.4"], ["brake", "exit"]], sfx="alarm", text="IT CAME CLOSER"),
    L("moth", "Odo, it's looking at us. Hide your lantern!", "close:moth",
      [["moth", "to:-3,5,1"], ["moth", "shake"]], text="HIDE YOUR LANTERN"),
    # ---- the science ----
    L(N, "In 2010, students from Michigan Tech came to test it.", "overhead",
      [["pl", "drift:3,24,3"], ["pr", "drift:5,26,2.2"]], text="2010: THE TEST"),
    L(N, "They pointed a telescope at the light. And they saw something very surprising.", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="A TELESCOPE"),
    L(N, "Cars! Headlights on a highway, nearly five miles away, over the hills.", "wide",
      [["hl1", "show"], ["hl2", "show"], ["hl1", "drift:-6,44,2"], ["hl2", "drift:-4.6,44,2"]],
      sfx="alarm", text="HEADLIGHTS?"),
    L(N, "They drove a car down that road, and flashed the lights. The valley light flashed too.", "two:odo,moth",
      [["pl", "bounce"], ["hl1", "vanish"], ["hl2", "vanish"]], text="IT FLASHED TOO"),
    L(N, "Red tail-lights made the red one, they said. Cold air bends the light over the hills.", "close:moth",
      [["pr", "bounce"]], text="TAIL-LIGHTS"),
    L("odo", "So the ghost light is just cars? Then why do I still have goosebumps?", "close:odo",
      [["odo", "shake"]]),
    L(N, "Many people in Paulding still don't believe it. Some say the mystery is not solved.", "overhead",
      [["pl", "drift:2,28,3.6"]], sfx="suspicious", text="NOT SOLVED?"),
    L(N, "Thousands still drive out there at night, to wait for the light.", "wide",
      [["pr", "vanish"]], text="THOUSANDS WAIT"),
    # ---- Would YOU ----
    L(N, "So, would YOU stand on that dark road and wait for it?", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="WOULD YOU WAIT?"),
    L("moth", "Only if Odo holds the lantern. And only for one minute.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the white light went out. And Odo's lantern flickered.", "wide",
      [["pl", "vanish"], ["shepherd", "to:6,14,0"], ["all", "shake"]], sfx="alarm", text="IT WENT OUT"),
    L(N, "Something tall was standing where the light had been.", "close:shepherd",
      [["shepherd", "turn:odo"]], sfx="suspicious", text="SOMETHING TALL"),
    L("shepherd", "Lantern-bearer. You saw my light. Now I see yours.", "close:shepherd",
      [["shepherd", "to:2,10,0"]], text="NOW I SEE YOURS"),
    L("odo", "Mothwick... run. Don't look back.", "two:odo,moth", [["odo", "shake"], ["moth", "eyes_big"]]),
    L(N, "Will the Shepherd take Odo's lantern? Subscribe, so you don't miss the next tale.", "close:shepherd",
      [["shepherd", "spin"]], sfx="alarm", text="WHO TAKES THE LIGHT?"),
]

sc = {
    "title": "Paulding's Ghost Light: Why Won't It Stop?",
    "description": "Since 1966, a light has appeared almost every night in a Michigan valley.",
    "lead_in": 0.05,
    "set": {"place": "forest", "fog": 0.05, "eyes": 2, "moonlight": 2.4},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep024.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

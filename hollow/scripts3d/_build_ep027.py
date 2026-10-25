"""Hollowmere Tales EP 27 (3D) - the Flatwoods Monster, Braxton County, West Virginia, 12 September 1952. Writes scripts3d/ep027.json.
Recorded sighting (sources: wvencyclopedia.org/entries/2127, history.com/news/flatwoods-monster-west-virginia,
ufology.patrickgross.org/press/washingtondailynews15sep1952.htm - United Press story, Washington Daily News, 15 Sep 1952):
- 12 Sep 1952, dusk, Flatwoods (a village of fewer than 300 people). Boys playing football saw a pulsing red light / fireball
  streak across the sky and come down beyond a hill on a farm.
- Seven people climbed the hill: Mrs Kathleen May, her sons Ed (13) and Freddie (12), Gene Lemon (17, National Guard, with a
  flashlight), Tommy Hyer (10) and other boys; a dog ran with them. Mist on the hilltop; a pulsating light.
- Gene saw "a pair of bright eyes" in a tree and turned the flashlight on it: a figure "about 11 or 12 feet high", a red face,
  a head shaped like the ace of spades, green clothing hanging in folds below the waist, claw-like hands. It floated toward
  them. A sickening, metallic smell. Gene fell backward; the dog ran with its tail between its legs; everyone ran down the hill.
- Next morning newspaper man A. Lee Stewart found the grass trampled, two skid-like marks and the smell still there.
- The Air Force said bright meteors crossed the sky that night and the figure was "likely an owl". It was never seen again.
  Today the town calls itself the home of the Green Monster (museum in Sutton).
No injuries. Continues EP 26 (the Pale Shepherd: 'Every wall in this town is mine.')."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
chars["fw"] = {"name": "The figure on the hill", "voice": "bm_lewis", "speed": 0.85, "pitch": -3, "color": [0.05, 0.28, 0.08],
               "kind": "flatwoods", "size": 0.8, "home": [2, 12.5]}
chars["gene"] = {"name": "Gene, 17", "voice": "am_michael", "speed": 1.05, "pitch": 0, "color": [0.25, 0.3, 0.2],
                 "kind": "human", "size": 0.9, "home": [-8, 11]}
chars["kmay"] = {"name": "Mrs May", "voice": "af_sarah", "speed": 1.0, "pitch": 0, "color": [0.5, 0.2, 0.3],
                 "kind": "human", "size": 0.9, "home": [-10, 11.5]}
chars["ed"] = {"name": "Ed, 13", "voice": "am_puck", "speed": 1.08, "pitch": 2, "color": [0.2, 0.3, 0.55],
               "kind": "human", "size": 0.7, "home": [-11.5, 10]}
chars["tommy"] = {"name": "Tommy, 10", "voice": "am_adam", "speed": 1.1, "pitch": 3, "color": [0.6, 0.45, 0.15],
                  "kind": "human", "size": 0.6, "home": [-12.5, 11]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

FIRE = {"type": "ball", "color": [1.0, 0.15, 0.05], "glow": 25, "visible": False, "scale": 0.7}
props = [dict(FIRE, id="fire", at=[-22, 30, 18])]
props += [{"type": "ball", "id": "beam1", "color": [1.0, 0.95, 0.7], "glow": 14, "visible": False, "scale": 0.18, "at": [-4.3, 11.4, 2.3]}]
props += [{"type": "box", "id": f"sk{i}", "color": [0.12, 0.1, 0.06], "visible": False, "scale": 0.5, "at": [x, 13.5, 0.02]} for i, x in enumerate((1.0, 4.0))]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (the figure glides out of the mist, Odo stumbles back) + big text hook + voice mid-danger
    L(N, "Seven people climbed the hill. At the top, something twelve feet tall was waiting.", "wide",
      [["fw", "to:0.5,11,0"], ["odo", "to:-6,9,0"], ["moth", "to:-4,9.5,2"]], sfx="alarm",
      text="IT WAS 12 FEET TALL"),
    L("moth", "Odo! It's floating! Its feet aren't even touching the grass!", "close:moth",
      [["moth", "shake"]], text="IT'S FLOATING"),
    L("odo", "Don't look at the eyes, Mothwick. Look at that head. It's shaped like a spade.", "close:fw",
      [["fw", "turn:front"]], sfx="suspicious", text="A SPADE-SHAPED HEAD"),
    L(N, "This is a true story, from newspaper reports of nineteen fifty-two. They called it the Flatwoods Monster.", "overhead",
      [["fw", "shake"]], text="THE FLATWOODS MONSTER"),
    L(N, "Flatwoods, West Virginia. A tiny village, with fewer than three hundred people.", "close:odo",
      [["odo", "turn:front"], ["fw", "to:3,16,0"]], text="WEST VIRGINIA, 1952"),
    # ---- the light in the sky ----
    L(N, "September the twelfth. At dusk, some boys were playing football near the school.", "wide",
      [["ed", "enter:left"], ["tommy", "enter:left"]], text="SEPTEMBER 12"),
    L(N, "Then a pulsing red light streaked across the sky.", "wide",
      [["fire", "show"], ["fire", "drift:12,30,2"]], sfx="horn", text="A RED LIGHT"),
    L("tommy", "Did you see that? It came down behind the hill!", "close:tommy",
      [["tommy", "jump"], ["fire", "vanish"]], text="IT CAME DOWN"),
    L("ed", "Let's go and look! Maybe it's a crashed plane!", "two:ed,tommy",
      [["ed", "bounce"]]),
    L("moth", "No, no, no. You never follow a falling light. Everybody knows that.", "close:moth",
      [["moth", "eyes_big"]], sfx="suspicious"),
    # ---- the climb ----
    L(N, "Ed was thirteen. His brother Freddie was twelve. Tommy was only ten.", "two:ed,tommy",
      [["ed", "to:-9,12,0"], ["tommy", "to:-10.5,12.5,0"]], text="AGES 10 TO 17"),
    L(N, "Their mother, Kathleen May, came too. So did Gene, seventeen, with a flashlight.", "close:kmay",
      [["kmay", "enter:left"], ["gene", "enter:left"]], text="7 PEOPLE + A DOG"),
    L("kmay", "Stay close to me, boys. Nobody runs ahead in the dark.", "close:kmay",
      [["kmay", "turn:front"]]),
    L(N, "A dog ran up the hill with them. The air turned thick with mist.", "wide",
      [["gene", "to:-5,12,0"], ["kmay", "to:-7,12.5,0"], ["all", "shake"]], sfx="alarm", text="THE MIST CAME"),
    L(N, "At the top, a light was pulsing in the grass. On, and off. On, and off.", "overhead",
      [["fire", "show"], ["fire", "drift:6,22,0.6"]], text="ON... AND OFF"),
    # ---- the eyes ----
    L(N, "Then Gene saw a pair of bright eyes, shining in a tree.", "close:gene",
      [["gene", "turn:fw"]], sfx="suspicious", text="BRIGHT EYES"),
    L("gene", "Something's up there! I'll shine the light on it!", "close:gene",
      [["gene", "shake"], ["beam1", "show"]], text="SHINE THE LIGHT"),
    L(N, "In the flashlight beam stood a figure, eleven or twelve feet tall.", "close:fw",
      [["fw", "to:2,13,0"], ["fw", "turn:front"]], sfx="horn", text="12 FEET TALL"),
    L(N, "It had a blood-red face, and a dark hood shaped like the ace of spades.", "close:fw",
      [["fw", "eyes_big"]], text="A RED FACE"),
    L(N, "Below the waist hung green folds, like a long skirt. Its hands looked like claws.", "close:fw",
      [["fw", "shake"]], sfx="alarm", text="CLAWS FOR HANDS"),
    L("tommy", "It's moving! It's coming toward us!", "close:tommy",
      [["tommy", "shake"], ["fw", "to:-1,12,0"]], text="IT'S COMING"),
    L(N, "It made no footsteps. It just floated across the grass.", "two:gene,fw",
      [["beam1", "vanish"]], sfx="suspicious", text="NO FOOTSTEPS"),
    L(N, "And then came a smell. Hot, metallic and sickening.", "close:kmay",
      [["kmay", "shake"]], text="A SICKENING SMELL"),
    L("kmay", "Run! All of you, run down the hill! Now!", "close:kmay",
      [["kmay", "jump"], ["all", "shake"]], sfx="alarm", text="RUN!"),
    L(N, "Gene fell over backwards. The dog ran with its tail between its legs.", "wide",
      [["gene", "exit"], ["ed", "exit"], ["tommy", "exit"], ["kmay", "exit"]], text="EVERYONE RAN"),
    # ---- the rule ----
    L("odo", "That is the rule, Mothwick. If a light falls from the sky, never climb the hill at night.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="NEVER CLIMB THE HILL"),
    # ---- the next morning ----
    L(N, "The next morning, a newspaper man named Lee Stewart climbed the hill himself.", "overhead",
      [["fw", "to:3,16,0"]], text="THE NEXT MORNING"),
    L(N, "The grass was trampled flat. There were two long marks, like skids, on the ground.", "wide",
      [["sk0", "show"], ["sk1", "show"]], sfx="horn", text="TWO STRANGE MARKS"),
    L(N, "And the strange smell was still there.", "close:moth",
      [["moth", "eyes_big"]], text="STILL THERE"),
    L("moth", "Odo, the smell is here too. Right now. Can you smell it?", "close:moth",
      [["moth", "shake"], ["moth", "to:-5,7,1.5"]], sfx="suspicious", text="CAN YOU SMELL IT?"),
    # ---- explanations ----
    L(N, "The Air Force said bright meteors crossed the sky that night.", "overhead",
      [["fire", "show"], ["fire", "drift:20,40,1"]], text="METEORS?"),
    L(N, "And the twelve-foot monster? They said it was most likely an owl.", "close:fw",
      [["fire", "vanish"], ["fw", "turn:front"]], sfx="horn", text="AN OWL?"),
    L(N, "But seven people saw it. And none of them ever forgot it. It was never seen again.", "two:odo,moth",
      [["odo", "turn:moth"]], sfx="suspicious", text="NEVER SEEN AGAIN"),
    # ---- Would YOU ----
    L(N, "So, would YOU climb the hill, if you saw a red light fall behind it?", "close:odo",
      [["odo", "eyes_big"]], sfx="alarm", text="WOULD YOU CLIMB IT?"),
    L("moth", "Never. I would hide under my blanket with the lantern off.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the figure turned its glowing eyes toward the forest, and pointed.", "close:fw",
      [["fw", "turn:front"], ["fw", "shake"]], sfx="suspicious", text="IT POINTED"),
    L(N, "The mist split open. Something pale was walking out of the trees.", "wide",
      [["shepherd", "to:8,19,0"], ["all", "shake"]], sfx="alarm", text="SOMETHING PALE"),
    L("shepherd", "Fly, run, climb any hill you like, lantern-bearer. I am already at the top.", "close:shepherd",
      [["shepherd", "turn:front"]], text="IT'S AT THE TOP"),
    L(N, "What waits on the next hill? Subscribe, so you don't miss the next true tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="horn", text="WHAT'S NEXT?"),
]

sc = {
    "title": "1952: What Waited at the Top of the Hill?",
    "description": "In 1952, seven people in Flatwoods, West Virginia climbed a hill after a red light fell from the sky.",
    "lead_in": 0.05,
    "set": {"place": "hill", "fog": 0.05, "eyes": 2, "moonlight": 9},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep027.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

"""Hollowmere Tales EP 14 (3D) — The Will-o'-the-Wisp. Writes scripts3d/ep014.json.
Recorded folklore + documented history: will-o'-the-wisp / ignis fatuus ('foolish fire', Latin coined 16th c.),
'wisp' = bundle of sticks used as a torch; Will the Smith (Shropshire tale), Stingy Jack + carved turnip (Ireland);
Alessandro Volta 1776 (spark + marsh gas); Major Louis Blesson 1832 field experiments in a German marsh (flame retreated
as he advanced); Irish Folklore Commission Schools' Collection 1938 (Co. Kildare, a boy followed a rolling red ball of fire);
2025 PNAS study begun at Stanford (Zare lab): microlightning between methane bubbles; sightings faded as swamps were drained."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 6])
chars["moth"] = dict(chars["moth"], home=[-3.5, 5])
chars["trav"] = {"name": "The Traveller", "voice": "am_michael", "speed": 1.05, "pitch": 0, "color": [0.3, 0.22, 0.14],
                 "kind": "human", "size": 1.0, "home": [-3, 10]}
chars["blesson"] = {"name": "Major Blesson", "voice": "bm_fable", "speed": 1.0, "pitch": -1, "color": [0.12, 0.16, 0.3],
                    "kind": "human", "size": 1.05, "home": [4, 9]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big hook + voice at frame 1
    L(N, "A light is floating over the bog. It wants you to follow it. Don't.", "close:odo",
      [["w1", "drift:-3,9,2.0"], ["odo", "shake"]], text="DON'T FOLLOW THE LIGHT"),
    L(N, "For hundreds of years, people in England and Ireland wrote down the same warning.", "two:odo,moth", [["moth", "shake"]], text="A REAL WARNING"),
    L("odo", "Mothwick... that light just moved closer.", "close:odo", [["odo", "turn:moth"], ["w1", "drift:-4.5,8,1.9"]]),
    L("moth", "Lights don't move on their own, Odo. Do they?", "close:moth", [["moth", "eyes_big"]]),
    L(N, "They called it the will-o'-the-wisp. A wisp was a bundle of sticks, burned as a torch.", "overhead", text="WILL-O'-THE-WISP"),
    L(N, "Scholars gave it a Latin name, ignis fatuus. The foolish fire.", "prop:w1", [["w1", "bounce"]], text="THE FOOLISH FIRE"),
    L(N, "And every story says the same thing. The light leads travellers off the path.", "close:trav", [["trav", "enter:left"]], sfx="suspicious"),
    # ---- Short 2 segment (would you follow it?) ----
    L("trav", "A lantern! Someone's out there. Hello? Wait for me!", "close:trav", [["trav", "turn:front"], ["w2", "show"]]),
    L(N, "But every time he stepped closer, the light floated farther away.", "wide", [["trav", "to:0,11"], ["w2", "drift:5,16,1.8"]]),
    L(N, "Closer. Farther. Closer. Farther. Until the ground under his feet turned to water.", "close:trav",
      [["trav", "to:3,13"], ["w2", "drift:9,21,1.6"], ["trav", "shake"]], sfx="suspicious", text="THE GROUND IS WATER"),
    L("moth", "That is why you never follow it.", "close:moth", [["moth", "turn:odo"]]),
    # ---- legends ----
    L(N, "In Shropshire, England, they told of a wicked blacksmith called Will.", "overhead", [["trav", "exit"], ["w2", "vanish"], ["w1", "vanish"]]),
    L(N, "The tale says even the Devil sent him away, and threw him one burning coal.", "prop:coal", [["coal", "show"]], sfx="suspicious"),
    L(N, "So Will wanders the marshes forever, using that coal to lure people into the mud.", "prop:coal", [["coal", "bounce"]], text="WILL WANDERS FOREVER"),
    L(N, "In Ireland, the light had another name. Jack-o'-lantern.", "wide", [["coal", "vanish"], ["w3", "show"]], text="JACK-O'-LANTERN"),
    L(N, "Stingy Jack tricked the Devil twice. He carried his glowing ember inside a carved turnip.", "prop:turnip", [["turnip", "show"]]),
    L("odo", "A turnip? Not a pumpkin?", "close:odo", [["odo", "eyes_big"]]),
    L("moth", "The pumpkins came later. In America.", "close:moth", [["turnip", "vanish"]]),
    # ---- the science ----
    L(N, "Here is the strange part. Real scientists tried to catch the light.", "wide", [["w3", "drift:-2,14,2.4"]], text="SCIENTISTS TRIED"),
    L(N, "In 1776, Alessandro Volta said a spark might set the swamp gas on fire.", "overhead", text="1776"),
    L(N, "Gas from rotting plants bubbles up out of the mud. Maybe it burns with a cold, blue flame.", "prop:w3", [["w3", "bounce"]], sfx="suspicious"),
    L(N, "And in 1832, a German officer, Major Louis Blesson, walked into a marsh at night.", "close:blesson", [["blesson", "enter:right"]], text="1832"),
    L("blesson", "There. A flame over the water. I shall get closer.", "close:blesson", [["blesson", "turn:front"], ["w4", "show"]]),
    L(N, "He wrote that as he came near, the flame moved away from him.", "two:blesson,odo", [["blesson", "to:2,12"], ["w4", "drift:4,19,1.7"]], text="IT MOVED AWAY"),
    L(N, "He blamed the air he pushed as he walked. But the light kept running, just like the stories said.", "wide", [["w4", "drift:7,24,1.9"]]),
    L(N, "Even in 1938, an Irish schoolboy wrote that his father once followed a rolling red ball of fire.", "close:moth", [["blesson", "exit"], ["w4", "vanish"], ["moth", "shake"]], text="1938"),
    # ---- Short 1 segment (the rule) ----
    L(N, "So the old rule is simple. If a light floats over the bog at night...", "wide", [["w5", "show"], ["w5", "drift:-1,10,2"]], text="THE ONE RULE"),
    L(N, "Do not follow it. Stay on the path. And never wave back.", "close:odo", [["odo", "eyes_big"]], text="NEVER FOLLOW IT"),
    L("odo", "Mothwick... I think I waved.", "close:odo", [["odo", "shake"], ["w5", "drift:-4,7.5,1.6"]], sfx="suspicious"),
    # ---- ending + cliffhanger ----
    L(N, "In 2025, scientists made tiny sparks jump between bubbles of swamp gas. Maybe that is the light.", "overhead", [["w5", "vanish"]], text="2025"),
    L(N, "But no one has ever caught a will-o'-the-wisp out in the wild. Not one.", "wide", text="NEVER CAUGHT"),
    L(N, "And when the old swamps were drained, people stopped seeing the lights.", "two:odo,moth"),
    L("moth", "Then why are there five of them around us?", "close:moth",
      [["w1", "show"], ["w1", "drift:-9,8,2"], ["w2", "show"], ["w3", "show"], ["w4", "show"], ["w5", "show"]], sfx="suspicious"),
    L(N, "One by one, the lights drifted closer. And the path behind them was gone.", "wide",
      [["w2", "drift:-2,8,1.8"], ["w3", "drift:-8,10,2.2"], ["w4", "drift:-5,11,2"], ["w5", "drift:-3,7,1.5"], ["all", "look:odo"]], text="THE PATH IS GONE"),
    L(N, "Who lit them? The next tale begins right there.", "prop:w5", [["w5", "bounce"], ["odo", "shake"]], text="WHO LIT THEM? SUBSCRIBE!"),
]

WISP = [0.45, 0.85, 1.0]
sc = {
    "title": "Would You Follow the Light in the Bog?",
    "description": "A light floats over the bog. It wants you to follow it. Don't.",
    "lead_in": 0.05,
    "set": {"place": "swamp", "fog": 0.035, "eyes": 6, "moonlight": 1.8},
    "chars": chars,
    "props": [
        {"id": "w1", "type": "ball", "color": WISP, "at": [0, 13, 2.4], "visible": True, "scale": 0.3, "glow": 2.5},
        {"id": "w2", "type": "ball", "color": WISP, "at": [2, 13, 1.8], "visible": False, "scale": 0.3, "glow": 2.5},
        {"id": "w3", "type": "ball", "color": [0.55, 1.0, 0.75], "at": [3, 15, 2.2], "visible": False, "scale": 0.3, "glow": 2.5},
        {"id": "w4", "type": "ball", "color": WISP, "at": [6, 14, 1.7], "visible": False, "scale": 0.3, "glow": 2.5},
        {"id": "w5", "type": "ball", "color": [0.55, 1.0, 0.75], "at": [3, 12, 2.0], "visible": False, "scale": 0.3, "glow": 2.5},
        {"id": "coal", "type": "ball", "color": "orange", "at": [0, 9, 1.4], "visible": False, "scale": 0.35, "glow": 8},
        {"id": "turnip", "type": "ball", "color": [0.85, 0.75, 0.55], "at": [0, 9, 1.2], "visible": False, "scale": 0.5, "glow": 3},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep014.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats))

"""Hollowmere Tales EP 30 (3D) - the Oak Island Money Pit, Nova Scotia, Canada, 1795 onward. Writes scripts3d/ep030.json.
Documented record + legend (sources: en.wikipedia.org/wiki/Oak_Island_mystery,
www.heritagedaily.com/2024/04/the-history-of-the-oak-island-money-pit/151722,
people.howstuffworks.com/oak-island.htm):
- Legend (first printed in the 1850s-1860s): in 1795 young Daniel McGinnis found a round, saucer-shaped dip in the ground
  on Oak Island, Mahone Bay, Nova Scotia. With John Smith and Anthony Vaughan he dug: flagstones about 2 ft down,
  layers of logs; they stopped at about 30 ft.
- The Onslow Company (early 1800s, no original papers survive) said it dug to about 90 ft: log platforms about every
  10 ft, charcoal, putty, coconut fibre, and near 90 ft a stone with strange symbols. Overnight the pit filled with water;
  a second shaft flooded too.
- The Truro Company (1849): re-dug, flooded again, drilled; at about 98 ft the drill went through wood (they reported
  'metal in pieces'). They saw the water rise and fall with the tide and believed in a flood tunnel from the sea.
- 1909: a young Franklin D. Roosevelt joined a treasure company there and followed the mystery for the rest of his life.
- 1931 Chappell shaft: at 127 ft an axe, an anchor and a miner's pick (old tools).
- Theories: pirate Captain Kidd, Templars... Scientists: a natural sinkhole; 1995 Woods Hole tests said the flooding is
  natural (fresh water + tides). More than 200 years; no treasure has ever been confirmed.
No accidents, no deaths, no curse deaths mentioned. Continues EP 29 (the Pale Shepherd: 'this flock is mine.')."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
chars["dan"] = {"name": "Daniel McGinnis", "voice": "am_puck", "speed": 1.05, "pitch": 1, "color": [0.55, 0.32, 0.18],
                "kind": "human", "size": 0.75, "home": [0.5, 11.0]}
chars["smith"] = {"name": "John Smith", "voice": "am_michael", "speed": 1.0, "pitch": 0, "color": [0.25, 0.35, 0.25],
                  "kind": "human", "size": 0.8, "home": [7.5, 11.5]}
chars["digger"] = {"name": "A digger", "voice": "bm_lewis", "speed": 1.0, "pitch": -1, "color": [0.45, 0.4, 0.3],
                   "kind": "human", "size": 0.9, "home": [-30, 30]}
chars["fdr"] = {"name": "Young Franklin Roosevelt", "voice": "am_eric", "speed": 1.0, "pitch": 0, "color": [0.2, 0.22, 0.35],
                "kind": "human", "size": 0.9, "home": [-30, 30]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

PIT = [4.0, 11.0]
props = [
    # the round dip / the pit: a dark earth mound ring + a black hole cap
    {"type": "ball", "id": "pit", "color": [0.05, 0.04, 0.03], "visible": True, "scale": 2.0, "at": [PIT[0], PIT[1], -1.55]},
    # flagstones, logs, the strange stone, the sea water, a gold glint, the moon
    {"type": "box", "id": "flag", "color": [0.45, 0.45, 0.48], "visible": False, "scale": 0.5, "at": [PIT[0] - 2.0, PIT[1] - 1.8, 0.0]},
    {"type": "box", "id": "log", "color": [0.35, 0.2, 0.08], "visible": False, "scale": 0.5, "at": [PIT[0] + 2.0, PIT[1] - 1.8, 0.0]},
    {"type": "box", "id": "stone", "color": [0.55, 0.6, 0.65], "glow": 0.8, "visible": False, "scale": 0.45, "at": [PIT[0], PIT[1] - 2.0, 0.1]},
    {"type": "ball", "id": "water", "color": [0.1, 0.35, 0.8], "glow": 3, "visible": True, "scale": 1.9, "at": [PIT[0], PIT[1], -4.0]},
    {"type": "ball", "id": "gold", "color": "gold", "glow": 6, "visible": False, "scale": 0.35, "at": [PIT[0], PIT[1], 0.6]},
    {"type": "ball", "id": "mark", "color": [0, 0, 0], "visible": False, "scale": 0.1, "at": [PIT[0], PIT[1], 0.6]},
    {"type": "ball", "id": "moon", "color": [0.95, 0.9, 0.75], "glow": 12, "visible": False, "scale": 1.4, "at": [14, 40, 16]},
]

N = "narr"
WATER_UP = [["water", f"drift:{PIT[0]},{PIT[1]},-1.45"]]
WATER_DOWN = [["water", f"drift:{PIT[0]},{PIT[1]},-4.0"]]


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion + big text hook + voice mid-tension
    L(N, "Thirty feet under the ground, the three young men dropped their shovels and climbed out.", "wide",
      [["dan", "jump"], ["smith", "jump"], ["odo", "shake"]], sfx="alarm", text="DON'T DIG DEEPER"),
    L("moth", "Odo, why did they stop? What's down there?", "close:moth",
      [["moth", "shake"], ["odo", "turn:moth"]], text="WHAT'S DOWN THERE?"),
    L("odo", "Nobody knows, Mothwick. People have been digging here for two hundred years.", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="200 YEARS OF DIGGING"),
    L(N, "This is a true story, and a legend first written down in the eighteen sixties.", "wide",
      [["moon", "show"]], text="A TRUE STORY"),
    L(N, "Oak Island, Nova Scotia, Canada. The year is seventeen ninety-five.", "wide",
      [["dan", "to:-6,15,0"], ["smith", "to:7,16,0"]], text="OAK ISLAND, 1795"),
    # ---- the dip ----
    L(N, "The story says a young man, Daniel McGinnis, found a strange round dip in the ground.", "prop:mark",
      [["dan", "to:0.5,11,0"], ["dan", "turn:front"]], text="A ROUND DIP"),
    L("dan", "Somebody dug here a long time ago. And then they filled it back in.", "close:dan",
      [["dan", "eyes_big"]], text="SOMEBODY DUG HERE"),
    L(N, "He came back with two friends, John Smith and Anthony Vaughan, and three shovels.", "wide",
      [["smith", "to:7.5,11.5,0"], ["smith", "turn:dan"]], sfx="horn", text="THREE SHOVELS"),
    L(N, "Two feet down, they hit a layer of flat stones.", "prop:flag",
      [["flag", "show"], ["dan", "jump"]], text="FLAT STONES"),
    L("smith", "Stones don't line up like that on their own. Keep digging!", "close:smith",
      [["smith", "jump"]], text="KEEP DIGGING!"),
    L(N, "Deeper down, there were layers of logs, laid across the hole like floors.", "prop:log",
      [["log", "show"], ["smith", "shake"]], sfx="suspicious", text="LOG FLOORS"),
    L(N, "At about thirty feet, they stopped. The old story says they were simply too afraid.", "two:dan,smith",
      [["dan", "shake"], ["smith", "turn:front"]], text="TOO AFRAID"),
    L("moth", "Too afraid of a hole? Okay, I get it. It's a very dark hole.", "close:moth",
      [["moth", "eyes_big"]]),
    # ---- the Onslow Company ----
    L(N, "Years later, a company of treasure hunters came with ropes, buckets and money.", "wide",
      [["dan", "exit"], ["smith", "exit"], ["digger", "to:0.5,11,0"], ["digger", "turn:front"]], sfx="horn", text="TREASURE HUNTERS"),
    L(N, "They said they found a log floor about every ten feet. Charcoal. Putty. Even coconut fibre.", "close:digger",
      [["log", "bounce"], ["digger", "jump"]], text="EVERY 10 FEET"),
    L("odo", "Coconut fibre? Mothwick, no coconuts grow anywhere near Nova Scotia.", "close:odo",
      [["odo", "turn:moth"]], sfx="suspicious", text="NO COCONUTS HERE"),
    L(N, "Then, ninety feet down, they found a stone carved with strange symbols.", "prop:stone",
      [["stone", "show"], ["all", "look:digger"]], sfx="alarm", text="90 FEET DOWN"),
    L("digger", "Look at these marks. It's a message. Something is buried below us!", "close:digger",
      [["digger", "eyes_big"]], text="A SECRET MESSAGE?"),
    L(N, "They went to bed dreaming of gold. By morning, the pit was full of water.", "prop:mark",
      WATER_UP + [["stone", "vanish"]], sfx="alarm", text="BY MORNING: WATER"),
    L("moth", "Wait. The water came back by itself? Overnight?", "close:moth",
      [["moth", "shake"]], text="BY ITSELF?"),
    L(N, "They dug a second shaft right beside it. That one filled with water too.", "wide",
      [["digger", "shake"], ["water", "bounce"]], text="FLOODED AGAIN"),
    # ---- the rule ----
    L("odo", "That's the rule, Mothwick. If the ground sounds hollow, don't dig deeper.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="IF THE GROUND IS HOLLOW..."),
    L("moth", "Don't dig. Don't even poke it. Got it.", "close:moth", [["moth", "jump"]]),
    # ---- Truro ----
    L(N, "In eighteen forty-nine, new diggers pumped the water out and brought a giant drill.", "wide",
      WATER_DOWN + [["digger", "to:1,10,0"]], sfx="horn", text="1849: A GIANT DRILL"),
    L(N, "Near ninety-eight feet, the drill broke through wood. They said it brought up bits of metal.", "prop:mark",
      [["gold", "show"], ["gold", "spin"]], text="BITS OF METAL"),
    L(N, "Then they noticed something worse. The water in the pit went up and down with the sea.", "prop:mark",
      WATER_UP + [["gold", "vanish"]], sfx="alarm", text="IT MOVES WITH THE SEA"),
    L("digger", "There must be a tunnel from the beach. Somebody built a trap!", "close:digger",
      [["digger", "eyes_big"]], text="A TRAP?"),
    # ---- the famous digger ----
    L(N, "In nineteen oh nine, a young man named Franklin Roosevelt joined the treasure hunt.", "wide",
      [["digger", "exit"], ["fdr", "to:0.5,11,0"], ["fdr", "turn:front"]], text="1909: ROOSEVELT"),
    L(N, "Years later he became President of the United States. He never forgot Oak Island.", "close:fdr",
      [["fdr", "jump"]], text="A FUTURE PRESIDENT"),
    L("fdr", "If anything is down there, I'd like to know who put it there.", "close:fdr",
      [["fdr", "turn:front"]], text="WHO PUT IT THERE?"),
    L(N, "In nineteen thirty-one, diggers found an old axe, an anchor and a miner's pick, far underground.", "prop:mark",
      [["fdr", "exit"], ["log", "bounce"], ["flag", "bounce"]], sfx="suspicious", text="AN AXE. AN ANCHOR."),
    # ---- the mystery ----
    L(N, "Pirate gold? Lost jewels? Or just a deep natural hole in the rock?", "two:odo,moth",
      [["odo", "turn:moth"]], text="PIRATE GOLD?"),
    L(N, "Scientists say the island sits on caves, and the sea water gets in naturally.", "wide",
      [["water", "bounce"]], text="CAVES UNDER THE ISLAND"),
    L(N, "But after more than two hundred years, nobody has found the bottom of the mystery.", "close:odo",
      [["odo", "eyes_big"]], sfx="alarm", text="STILL NO BOTTOM"),
    L(N, "So, would YOU climb down into the Money Pit tonight?", "close:moth",
      [["moth", "eyes_big"]], text="WOULD YOU GO DOWN?"),
    L("moth", "Not for all the pirate gold in the world. I'd stay up here.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the water in the pit began to bubble. And a pale hand reached up out of it.", "prop:mark",
      [["shepherd", "to:4,11.6,0"], ["water", "bounce"], ["all", "shake"]], sfx="alarm", text="SOMETHING CAME UP"),
    L("shepherd", "Dig all you like, lantern-bearer. Everything down here is mine.", "close:shepherd",
      [["shepherd", "turn:front"]], sfx="suspicious", text="EVERYTHING DOWN HERE IS MINE"),
    L(N, "What is the Shepherd hiding under the island? Subscribe, and find out in the next true tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="horn", text="WHAT IS IT HIDING?"),
]

sc = {
    "title": "Oak Island: 200 Years and No Bottom?",
    "description": "In 1795, three young men on Oak Island, Nova Scotia, started digging a strange round dip. More than 200 years later, nobody has reached the bottom of the mystery.",
    "lead_in": 0.05,
    "set": {"place": "clearing", "fog": 0.04, "eyes": 3, "moonlight": 14},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep030.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

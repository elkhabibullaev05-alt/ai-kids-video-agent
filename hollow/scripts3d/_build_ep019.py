"""Hollowmere Tales EP 19 (3D) — Borley Rectory, 'the most haunted house in England'. Writes scripts3d/ep019.json.
Documented record + legend (sources: en.wikipedia.org/wiki/Borley_Rectory, psi-encyclopedia.spr.ac.uk/articles/borley-rectory,
foxearth.org.uk/TheHauntedRectory.html):
Built 1862 by Rev. Henry Dawson Ellis Bull next to Borley church (Essex), a wing added for his 14 children.
LEGEND: a nun of a nearby monastery, linked with a monk; debunked 1938, possibly made up by the Bull children.
28 July 1900: four Bull daughters saw a nun-like figure about 40 yards away at dusk; it vanished as one approached ("Nun's Walk").
2 Oct 1928 Rev. Guy Eric Smith and wife moved in: footsteps, bells, lights. Daily Mirror story 10 June 1929; Harry Price
visited 12 June 1929; Smiths left July 1929. 16 Oct 1930 Rev. Lionel Foyster and wife Marianne moved in (to Oct 1935):
bell ringing, stones/bottles thrown, writing on walls and paper (messages addressed to Marianne). Marianne later said she saw
no apparitions and some noises were wind, visitors or her own pranks. Price called it "the most haunted house in England".
27 Feb 1939 an overturned oil lamp - fire; demolished 1944. 1956 SPR report: many phenomena faked or natural.
Short 1 = the wall writing (beats 22-26)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-5, 6])
chars["moth"] = dict(chars["moth"], home=[-2.5, 5])
chars["nun"] = {"name": "The Nun", "voice": "bf_emma", "speed": 0.82, "pitch": -2, "color": [0.07, 0.07, 0.09],
                "kind": "lady", "ghost": True, "up": True, "size": 0.95, "home": [6, 13]}
chars["price"] = {"name": "Harry Price", "voice": "bm_lewis", "speed": 1.0, "pitch": -1, "color": [0.22, 0.2, 0.18],
                  "kind": "human", "size": 1.0, "home": [-10, 11]}
chars["marianne"] = {"name": "Marianne", "voice": "af_sarah", "speed": 0.95, "pitch": 0, "color": [0.45, 0.12, 0.15],
                     "kind": "human", "size": 0.9, "home": [2.5, 10]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big text hook + voice mid-tension at frame 1
    L(N, "Words are appearing on the wall. And nobody is holding the pencil.", "wide",
      [["pencil", "spin"], ["odo", "shake"], ["moth", "eyes_big"]], text="WHO WROTE ON THE WALL?"),
    L("moth", "Odo, look! The letters are still moving!", "prop:pencil", [["moth", "shake"], ["pencil", "bounce"]], sfx="alarm"),
    L("odo", "It's a name. Marianne. Who is Marianne?", "close:odo", [["odo", "eyes_big"]], text="MARIANNE..."),
    L(N, "Sarah's sealed door had slammed behind them. Now they stood in a different house.", "overhead",
      [["nun", "rise"]], sfx="suspicious", text="A DIFFERENT HOUSE"),
    L(N, "This is a true story, from real records. Borley Rectory, in a village in Essex, England.", "wide",
      [["odo", "turn:nun"]], text="BORLEY, ENGLAND"),
    L(N, "One ghost hunter called it the most haunted house in England.", "close:nun",
      [["nun", "turn:front"]], sfx="suspicious", text="MOST HAUNTED HOUSE"),
    # ---- the house and the legend ----
    L(N, "A vicar, Henry Bull, built it in 1862, right beside the old village church.", "two:odo,moth",
      [["moth", "turn:front"]], text="BUILT IN 1862"),
    L(N, "He had fourteen children. So he added a whole new wing.", "wide",
      [["odo", "jump"]], text="14 CHILDREN"),
    L(N, "And in that house, people told a story. A story about a nun.", "close:nun",
      [["nun", "rise"]], sfx="suspicious", text="THE NUN"),
    L(N, "The legend said she was locked away near here, long ago. And she never left.", "two:nun,moth",
      [["nun", "to:4,11"]], text="SHE NEVER LEFT"),
    L("moth", "Locked away? Odo, I really don't like this story.", "close:moth", [["moth", "shake"]]),
    L(N, "Historians say the legend was probably made up. But then came one summer evening.", "wide",
      [["nun", "dive"]], text="LEGEND... OR NOT?"),
    # ---- 1900 ----
    L(N, "July the twenty-eighth, 1900. Four of the Bull sisters walked in the garden at dusk.", "overhead",
      [["odo", "to:-3,8"]], text="28 JULY 1900"),
    L(N, "About forty yards away, they saw a dark figure. A nun, gliding over the grass.", "close:nun",
      [["nun", "rise"], ["nun", "to:2,12"]], sfx="alarm", text="A NUN IN THE GARDEN"),
    L("odo", "Did they run away?", "close:odo", [["odo", "eyes_big"]]),
    L(N, "One sister walked toward her. And the nun was gone.", "wide",
      [["nun", "dive"]], sfx="suspicious", text="GONE"),
    L(N, "From then on, that path had a name. The Nun's Walk.", "two:odo,moth",
      [["moth", "turn:odo"]], text="THE NUN'S WALK"),
    # ---- 1928-1929 ----
    L(N, "In 1928, a new vicar, Guy Smith, moved in with his wife.", "wide",
      [["nun", "rise"], ["bell", "show"]], text="1928"),
    L(N, "They heard footsteps in empty rooms. Bells rang by themselves.", "prop:bell",
      [["bell", "bounce"], ["moth", "shake"]], sfx="alarm", text="BELLS RANG BY THEMSELVES"),
    L(N, "In 1929, a London newspaper printed the story. And a ghost hunter came. Harry Price.", "close:price",
      [["price", "enter:left"]], text="THE GHOST HUNTER"),
    L("price", "Ring again, bells. I am writing everything down.", "two:price,odo", [["price", "turn:front"], ["bell", "spin"]]),
    L(N, "The Smiths moved out that same summer.", "wide",
      [["price", "to:-7,10"], ["bell", "vanish"]], sfx="suspicious", text="THEY LEFT"),
    # ---- 1930-1935: Marianne (Short 1 segment) ----
    L(N, "In 1930, a vicar named Lionel Foyster moved in. With his young wife, Marianne.", "close:marianne",
      [["marianne", "turn:front"]], text="MARIANNE"),
    L(N, "Now it got worse. Stones and bottles flew. Bells rang. Doors locked by themselves.", "wide",
      [["all", "shake"], ["pencil", "spin"]], sfx="alarm", text="STONES FLEW"),
    L(N, "Then pencil writing appeared on the walls. Messages. Asking Marianne for help.", "prop:pencil",
      [["pencil", "bounce"], ["marianne", "eyes_big"]], sfx="suspicious", text="MARIANNE, PLEASE HELP"),
    L("marianne", "Who keeps writing my name on the wall?", "close:marianne", [["marianne", "shake"]], text="WHO WROTE IT?"),
    L("odo", "Moth... our wall said Marianne too.", "close:odo", [["odo", "turn:moth"], ["moth", "eyes_big"]]),
    # ---- what was real ----
    L(N, "Later, investigators said many events were tricks, wind, or visitors.", "two:price,marianne",
      [["price", "jump"]], text="TRICKS?"),
    L(N, "Marianne herself said some noises were her own pranks. But not everything was explained.", "close:marianne",
      [["marianne", "turn:odo"]], text="NOT EVERYTHING"),
    L(N, "Then, on February the twenty-seventh, 1939, an oil lamp fell over. The rectory burned.", "overhead",
      [["all", "shake"]], sfx="alarm", text="1939: FIRE"),
    L(N, "Five years later, the ruins were pulled down. Today, nothing of the house remains.", "wide",
      [["marianne", "exit"], ["price", "exit"]], text="NOTHING REMAINS"),
    L(N, "Was it a haunting, or the most famous trick in England? Nobody knows for sure.", "two:odo,moth",
      [["moth", "spin"]], sfx="suspicious", text="NOBODY KNOWS"),
    # ---- cliffhanger ----
    L(N, "Then, in the dark, the pencil moved again. All by itself.", "prop:pencil",
      [["pencil", "spin"], ["odo", "shake"]], sfx="alarm", text="THE PENCIL MOVED"),
    L("moth", "It's writing a new name, Odo. It's writing... yours.", "close:moth", [["moth", "eyes_big"], ["all", "look:nun"]]),
    L("nun", "Odo. Please. Help me get out.", "close:nun", [["nun", "rise"], ["nun", "to:3,8"]], text="HELP ME GET OUT"),
    L(N, "Who is writing on the wall? Subscribe. Don't miss what she writes next.", "wide",
      [["pencil", "spin"], ["odo", "eyes_big"]], text="WHO IS WRITING?"),
]

wall = []
for i in range(5):
    for j in range(3):
        wall.append({"id": f"w{i}{j}", "type": "box", "color": [0.45, 0.36, 0.3], "at": [-2.4 + i * 1.2, 15, j * 1.2], "scale": 1.0})
letters = [{"id": f"l{k}", "type": "box", "color": [0.95, 0.92, 0.85], "glow": 1.5,
            "at": [-2.0 + k * 0.45, 14.2, 2.3 + (0.12 if k % 2 else 0)], "scale": 0.18} for k in range(8)]
sc = {
    "title": "Who Wrote on the Walls at Borley?",
    "description": "Words are appearing on the wall. And nobody is holding the pencil.",
    "lead_in": 0.05,
    "set": {"place": "chapel", "fog": 0.06, "eyes": 3, "moonlight": 2.4},
    "chars": chars,
    "props": wall + letters + [
        {"id": "pencil", "type": "cone", "color": "gold", "at": [1.8, 14.0, 2.0], "scale": 0.6},
        {"id": "bell", "type": "cone", "color": "gold", "at": [-6, 12, 4.5], "visible": False, "scale": 0.8},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep019.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats), "words", sum(len(b["say"].split()) for b in beats))

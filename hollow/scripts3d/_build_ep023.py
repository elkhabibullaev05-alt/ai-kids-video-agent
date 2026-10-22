"""Hollowmere Tales EP 23 (3D) - the Wild Hunt of Peterborough, 1127. Writes scripts3d/ep023.json.
Recorded chronicle entry + folklore, clearly labelled (sources: en.wikipedia.org/wiki/Wild_Hunt,
strangehistory.net/2018/01/28/wild-hunt-1127 (Peterborough Chronicle text), norse-mythology.org/the-wild-hunt):
- Peterborough Chronicle (Anglo-Saxon Chronicle, Peterborough manuscript), entry for 1127: right after the new abbot
  Henry (of Poitou / d'Angely) came to Peterborough, many men saw and heard a great hunt. The huntsmen were black, huge
  and loathsome; they rode black horses and black he-goats; their hounds were jet black.
- Seen in the deer park of Peterborough and in all the woods from that town to Stamford; the monks heard the horns
  blowing at night. Truthful men keeping watch said there might be about twenty or thirty horn-blowers.
- It went on all Lent, right up to Easter (Wikipedia: about nine weeks).
- Folklore (Wikipedia, norse-mythology.org): across Europe the Wild Hunt; in Scandinavia/Germany led by Odin/Wodan, rides
  in midwinter storms; a witness could be carried away and dropped miles off; safety: stand in the middle of the road,
  lie flat on the ground (Odin rides no lower than an ox's yoke), a girl covered her head with her apron so as not to see.
- Some historians read the entry as the monks' comment on the unpopular new abbot ("some think").
Continues EP 22 (the winged figure was pulling Mothwick toward its red eyes).
Short 1 (the rule) = hook (beat 0) + lie flat (beats 24-27). Short 2 = 'Would YOU' (beats 33-34)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 5])
chars["moth"] = dict(chars["moth"], home=[-3.5, 4.5])
chars["mm"] = {"name": "The Winged Figure", "voice": "am_onyx", "speed": 0.8, "pitch": -5, "color": [0.42, 0.42, 0.46],
               "kind": "winged", "up": True, "size": 0.8, "home": [1, 15]}
for i, (hx, hy) in enumerate(((7, 11), (11, 13), (15, 15))):
    chars["h%d" % (i + 1)] = {"name": "Black Hunter", "voice": "bm_george", "speed": 0.8, "pitch": -4,
                              "color": [0.03, 0.03, 0.04], "kind": "horseman", "rider": True, "size": 0.9 - 0.05 * i,
                              "home": [hx, hy]}
chars["d1"] = dict(cast["hound"], home=[-11, 10], size=0.8)
chars["d2"] = dict(cast["hound"], home=[-14, 12], size=0.75)
chars["monk"] = {"name": "A Monk of Peterborough", "voice": "bm_lewis", "speed": 0.95, "pitch": -1, "color": [0.3, 0.2, 0.12],
                 "kind": "human", "size": 0.95, "home": [-10, 8]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 18], size=0.85)

N = "narr"
RIDE_UP = [["h1", "to:3,11,1.2"], ["h2", "to:0,13,1.8"], ["h3", "to:-3,15,2.4"]]
RIDE_ON = [["h1", "to:16,13,2"], ["h2", "to:15,15,2.5"], ["h3", "to:14,17,3"]]
RIDE_BACK = [["h1", "to:-2,11,1"], ["h2", "to:-5,13,1.5"], ["h3", "to:-8,15,2"]]
RIDE_LOW = [["h1", "to:9,7,1.5"], ["h2", "to:7,9,2"], ["h3", "to:5,11,2.5"]]


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (riders gallop up into the sky, Mothwick pulled up) + big text hook + voice mid-tension at frame 1
    L(N, "Horns blew across the night sky. Then black riders came out of the clouds.", "wide",
      RIDE_UP + [["moth", "to:-1,10,3"], ["mm", "to:2,15,2.2"]], sfx="horn", text="THEY RIDE THE SKY"),
    L("moth", "Odo! Its red eyes won't let me go! Help me!", "close:moth", [["moth", "shake"]], text="HELP ME!"),
    L("odo", "Hold on, Mothwick! Something is coming through the trees!", "close:odo",
      [["odo", "shake"], ["d1", "to:-4,9,0"], ["d2", "to:-7,11,0"]], sfx="alarm"),
    L(N, "Black hounds burst from the woods, and the riders turned toward the red eyes.", "wide",
      [["d1", "to:1,11,0"], ["d2", "to:-1,12,0"]] + RIDE_ON, sfx="horn", text="BLACK HOUNDS"),
    L(N, "This is a true story. A monk wrote it down nearly nine hundred years ago.", "overhead",
      [["mm", "spin"]], sfx="suspicious", text="A TRUE STORY"),
    L(N, "Peterborough, England. The year 1127.", "close:odo", [["odo", "turn:front"]], text="ENGLAND, 1127"),
    L(N, "A new abbot named Henry had just arrived at the great abbey.", "close:monk",
      [["monk", "enter:left"]], text="A NEW ABBOT"),
    L(N, "Right after he came, many men saw something strange in the deer park.", "two:monk,odo",
      [["monk", "turn:h1"]], sfx="suspicious"),
    L(N, "A hunt. But the hunters were black, and huge, and hideous.", "close:h1",
      RIDE_BACK, sfx="horn", text="BLACK HUNTERS"),
    L(N, "They rode black horses. And black goats.", "wide", [["h1", "shake"], ["h2", "shake"]],
      text="BLACK HORSES"),
    L(N, "Their hounds were all jet black, with wide, staring eyes.", "close:d1",
      [["d1", "eyes_big"], ["monk", "exit"]], text="STARING EYES"),
    L("odo", "Mothwick... I can hear hooves. Lots of hooves.", "two:odo,moth", [["odo", "eyes_big"]]),
    L("moth", "Black goats? Odo, who rides a goat across the sky?", "close:moth", [["moth", "spin"]]),
    L(N, "They rode through the woods, from the town all the way to Stamford.", "overhead",
      RIDE_ON, sfx="alarm", text="ALL THE WAY TO STAMFORD"),
    L(N, "And at night, the monks heard the horns blowing.", "close:odo", [["odo", "turn:h2"]],
      sfx="horn", text="THE MONKS HEARD HORNS"),
    L("monk", "Truthful men kept watch. They counted twenty or thirty horn-blowers.", "close:monk",
      [["monk", "enter:left"], ["monk", "shake"]], text="20 OR 30 RIDERS"),
    L(N, "It happened again and again. All through spring, right up to Easter.", "wide",
      RIDE_BACK + [["monk", "exit"]], sfx="suspicious", text="UNTIL EASTER"),
    L(N, "The chronicle says it went on for about nine weeks.", "close:h3", [["h3", "turn:odo"]], text="9 WEEKS"),
    L("moth", "Nine weeks of that? Odo, I would never sleep again.", "close:moth", [["moth", "sad"]]),
    L(N, "All over Europe, people told of this ride. They called it the Wild Hunt.", "overhead",
      [["h1", "spin"], ["d1", "to:-3,10,0"]], sfx="horn", text="THE WILD HUNT"),
    L(N, "In Germany and Scandinavia, some said Odin led it, through the storms of midwinter.", "close:h1",
      [["h1", "turn:front"]], text="MIDWINTER STORMS"),
    L(N, "Old tales say anyone it caught could be carried off, and dropped miles from home.", "wide",
      RIDE_UP, sfx="alarm", text="CARRIED AWAY"),
    # ---- the rule (Short 1 segment) ----
    L("odo", "Then how do you stay safe from it?", "close:odo", [["odo", "shake"]], text="HOW DO YOU HIDE?"),
    L(N, "One old tale says: stand right in the middle of the road.", "two:odo,moth", [["moth", "to:-4,6,1"]],
      text="STAY ON THE ROAD"),
    L(N, "Another says: lie flat on the ground. Let it pass over you.", "close:odo", [["odo", "eyes_big"]],
      sfx="suspicious", text="LIE FLAT"),
    L(N, "In one story, a girl hid her head under her apron, so she wouldn't see it.", "close:moth",
      [["moth", "shake"]], text="DON'T SEE IT"),
    L("odo", "Mothwick, get down! Lie flat! Don't look up!", "two:odo,moth",
      [["moth", "to:-4,5,0.3"], ["odo", "jump"]], text="DON'T LOOK UP"),
    L(N, "The riders thundered over them, so low the branches bent.", "wide",
      RIDE_LOW + [["all", "shake"]], sfx="horn", text="THEY PASSED OVER"),
    L(N, "And the hounds went after the winged thing with red eyes. It fled into the clouds.", "close:mm",
      [["d1", "to:3,13,0"], ["d2", "to:1,14,0"], ["mm", "to:14,22,9"]], sfx="alarm", text="IT FLED"),
    L("moth", "It let go! Odo, I'm free! I can move my wings again!", "close:moth",
      [["moth", "to:-3.5,4.5,0"], ["moth", "spin"]], text="FREE!"),
    # ---- what is real ----
    L(N, "Nobody knows what the people of Peterborough really saw.", "overhead", RIDE_ON, text="NEVER EXPLAINED"),
    L(N, "Some historians think the monks wrote it to show how unwelcome the new abbot was.", "close:odo",
      [["odo", "turn:front"]], text="A WARNING?"),
    L(N, "But the chronicle says it plainly. Many men saw it. And many heard it.", "close:h2",
      [["h2", "turn:odo"]], sfx="suspicious", text="MANY MEN SAW IT"),
    # ---- Would YOU (Short 2 segment) ----
    L(N, "So, would YOU look up when the horns blow over your house tonight?", "close:odo",
      [["odo", "eyes_big"]], sfx="horn", text="WOULD YOU LOOK UP?"),
    L("moth", "Not even once. I'd keep my face in the mud until Easter.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the last rider stopped. And slowly turned back.", "wide",
      [["shepherd", "to:5,13,0"], ["all", "shake"]], sfx="alarm", text="THE LAST RIDER"),
    L(N, "Under its hood was a pale, cracked mask.", "close:shepherd", [["shepherd", "turn:odo"]],
      sfx="suspicious", text="A PALE MASK"),
    L("shepherd", "Lantern-bearer. Next time, the hunt rides for your light.", "close:shepherd",
      [["shepherd", "to:1,10,0"]], text="IT WANTS THE LANTERN"),
    L("odo", "Mothwick... it knows me. Run!", "two:odo,moth", [["odo", "shake"], ["moth", "eyes_big"]]),
    L(N, "Will the hunt take Odo's lantern? Subscribe, so you don't miss the next tale.", "close:shepherd",
      [["d1", "to:0,8,0"], ["d2", "to:-2,9,0"]], sfx="horn", text="WHO DOES IT HUNT?"),
]

sc = {
    "title": "1127: Who Rode Across the Night Sky?",
    "description": "Monks wrote that black riders hunted through the sky for nine weeks.",
    "lead_in": 0.05,
    "set": {"place": "forest", "fog": 0.08, "eyes": 2, "moonlight": 2.4},
    "chars": chars,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep023.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

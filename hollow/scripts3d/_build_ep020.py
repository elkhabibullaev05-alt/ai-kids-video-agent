"""Hollowmere Tales EP 20 (3D) — the Lady in Black of Fort Warren (Georges Island, Boston Harbor). Writes scripts3d/ep020.json.
Recorded LEGEND, clearly labelled (sources: legendsofamerica.com/fort-warren-massachusetts,
historicaldigression.com/2012/10/17/fort-warrens-lady-in-black-debunked, bostonharborislands.org/blog/october-ghost-stories,
home.nps.gov/articles/000/history-of-fort-warren.htm):
Fort Warren built 1833-1861 on Georges Island at the entrance to Boston Harbor; in the Civil War a prison for Confederate soldiers.
LEGEND (first printed by Edward Rowe Snow, The Romance of Boston Bay, 1944): early 1862 Melanie Lanier, newlywed wife of a
prisoner (Samuel / Andrew Lanier), came to Hull, rowed about a mile to the island at night dressed as a man, whistled a song,
heard it whistled back, was pulled over the wall; they were caught; the pistol went off and her husband was lost; she was
sentenced as a spy and asked to wear a dress - only black robes (theatre costumes) were found. Sightings since: a woman in black,
a voice in the "Corridor of Dungeons", a stone rolling across a room during a card game, footprints in the snow that come from
nowhere and go nowhere (Snow: five of them), soldiers who shot at a figure in black or fled their posts.
Historians: no record of any woman tried or hanged at Fort Warren; earliest printed version is Snow's 1944 book.
No death on screen: the husband is "lost", her fate is "the legend says she never left the island".
Short 1 = hook (beat 0-1) + footprints (beats 24-27). Short 2 = 'Would YOU' (beats 32-33)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-5, 6])
chars["moth"] = dict(chars["moth"], home=[-2.5, 5])
chars["lady"] = {"name": "The Lady in Black", "voice": "bf_emma", "speed": 0.82, "pitch": -2, "color": [0.08, 0.08, 0.11],
                 "kind": "lady", "ghost": True, "up": True, "size": 1.0, "home": [6, 13]}
chars["guard"] = {"name": "The Guard", "voice": "am_adam", "speed": 1.0, "pitch": -1, "color": [0.12, 0.16, 0.35],
                  "kind": "human", "size": 1.0, "home": [-10, 11]}
chars["snow"] = {"name": "Edward Rowe Snow", "voice": "bm_lewis", "speed": 1.0, "pitch": -1, "color": [0.3, 0.26, 0.2],
                 "kind": "human", "size": 0.95, "home": [2.5, 10]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big text hook + voice mid-tension at frame 1
    L(N, "Five footprints in the snow. They came from nowhere. And they went nowhere.", "wide",
      [["f0", "bounce"], ["odo", "shake"], ["moth", "eyes_big"]], text="DON'T FOLLOW THE FOOTPRINTS"),
    L("moth", "Odo, stop! Something is still walking. Right next to us!", "prop:f2", [["moth", "shake"], ["f3", "show"]], sfx="alarm"),
    L("odo", "That voice from Borley... it pulled us through the wall. Where are we?", "close:odo", [["odo", "eyes_big"]],
      text="WHERE ARE WE?"),
    L(N, "A cold stone fort, on an island. And somewhere inside, a lady in black.", "overhead",
      [["lady", "rise"]], sfx="suspicious", text="THE LADY IN BLACK"),
    L(N, "This is a real place, and a legend first printed in 1944. Fort Warren, in Boston Harbor.", "wide",
      [["odo", "turn:lady"]], text="FORT WARREN, BOSTON"),
    L(N, "Soldiers built it from granite, from 1833 until 1861.", "two:odo,moth",
      [["moth", "turn:front"]], text="BUILT 1833-1861"),
    L(N, "Then war came. And the fort became a prison for captured Southern soldiers.", "close:guard",
      [["guard", "enter:left"]], sfx="alarm", text="A PRISON ON AN ISLAND"),
    L("guard", "Lanterns out! Nobody leaves this island tonight.", "two:guard,odo", [["guard", "turn:front"], ["lamp", "spin"]]),
    # ---- the legend ----
    L(N, "The legend says one prisoner had just married. His wife's name was Melanie Lanier.", "close:lady",
      [["lady", "turn:front"]], text="MELANIE LANIER"),
    L(N, "In early 1862, she came north to a little town called Hull, across the water.", "wide",
      [["lady", "to:4,11"]], text="1862"),
    L(N, "One foggy night, dressed as a man, she rowed about a mile to the island. Alone.", "prop:boat",
      [["boat", "bounce"], ["moth", "shake"]], sfx="suspicious", text="SHE ROWED ALONE"),
    L("moth", "Alone? In the dark? On the sea? Odo, I'd never do that.", "close:moth", [["moth", "shake"]]),
    L(N, "Under the wall, she whistled a song. And from inside, someone whistled back.", "close:lady",
      [["lady", "rise"]], sfx="alarm", text="SOMEONE WHISTLED BACK"),
    L("odo", "Moth... I can hear whistling. Right now.", "close:odo", [["odo", "eyes_big"], ["all", "look:lady"]]),
    L(N, "The legend says she was pulled over the wall. They began to dig a way out.", "overhead",
      [["lady", "to:2,12"]], text="DIGGING OUT"),
    L(N, "But the guards found them. There was a struggle. A shot went wrong.", "two:guard,lady",
      [["guard", "jump"], ["all", "shake"]], sfx="alarm", text="CAUGHT"),
    L(N, "And her husband was lost. She was taken prisoner herself.", "wide",
      [["lady", "sad"], ["lamp", "vanish"]], text="SHE WAS TAKEN"),
    L(N, "She asked for a dress. The only one they found was old black robes.", "close:lady",
      [["lady", "turn:odo"]], sfx="suspicious", text="BLACK ROBES"),
    L(N, "And the legend says she never left the island again.", "two:odo,moth",
      [["odo", "sad"], ["moth", "sad"]], text="SHE NEVER LEFT"),
    # ---- the sightings ----
    L(N, "Soon, soldiers saw a woman in black on the walls at night.", "close:guard",
      [["guard", "turn:lady"], ["lady", "rise"]], sfx="alarm", text="A WOMAN IN BLACK"),
    L("guard", "Who goes there? Answer me! Answer me!", "two:guard,lady", [["guard", "shake"]]),
    L(N, "Stories say some guards fired at her. One ran from his post, and was punished for it.", "wide",
      [["guard", "exit"], ["lady", "dive"]], text="HE RAN"),
    L(N, "People heard a voice in a dark hall they called the Corridor of Dungeons.", "overhead",
      [["lady", "rise"], ["moth", "eyes_big"]], sfx="suspicious", text="CORRIDOR OF DUNGEONS"),
    L(N, "Soldiers playing cards watched a stone roll across the floor. Nobody touched it.", "prop:stone",
      [["stone", "spin"], ["odo", "jump"]], sfx="alarm", text="NOBODY TOUCHED IT"),
    # ---- footprints (Short 1 segment) ----
    L(N, "And one winter, they found footprints in the snow outside the fort.", "prop:f2",
      [["f1", "show"], ["f2", "show"], ["moth", "shake"]], text="FOOTPRINTS"),
    L(N, "Five small steps. Coming from nowhere. Going nowhere.", "overhead",
      [["f4", "show"], ["f0", "bounce"]], sfx="alarm", text="FROM NOWHERE"),
    L("moth", "Odo... there's a sixth footprint now. Right behind you.", "close:moth", [["moth", "eyes_big"], ["f5", "show"]],
      text="RIGHT BEHIND YOU"),
    L("odo", "Who is walking next to us?", "close:odo", [["odo", "shake"], ["all", "look:lady"]], text="WHO IS WALKING?"),
    # ---- what is real ----
    L("snow", "I'm Edward Rowe Snow. I wrote this story down in 1944.", "close:snow",
      [["snow", "enter:left"]], text="WRITTEN IN 1944"),
    L(N, "But historians found no record of any woman held or punished at Fort Warren.", "two:snow,odo",
      [["snow", "turn:odo"]], sfx="suspicious", text="NO RECORD"),
    L(N, "Melanie Lanier may never have existed at all. And still, people say they see her.", "close:lady",
      [["lady", "rise"]], text="NEVER EXISTED?"),
    L(N, "Today, visitors take a ferry to the island. Rangers tell her story at the Dark Arch.", "wide",
      [["snow", "exit"]], text="THE DARK ARCH"),
    # ---- Would YOU (Short 2 segment) ----
    L(N, "So, would YOU walk the Corridor of Dungeons alone, at night?", "overhead",
      [["lady", "to:3,9"], ["moth", "shake"]], sfx="alarm", text="WOULD YOU GO IN?"),
    L("moth", "Not me. Not ever. Not even for a hundred cookies.", "close:moth", [["moth", "spin"]]),
    # ---- cliffhanger ----
    L(N, "Then the whistling started again. Very close. The same old song.", "close:lady",
      [["lady", "rise"], ["odo", "shake"]], sfx="suspicious", text="THE WHISTLING"),
    L("lady", "You are not him. But you can still help me leave.", "close:lady", [["lady", "to:2,8"]], text="HELP ME LEAVE"),
    L("odo", "Moth... the footprints. They're walking toward the sea.", "two:odo,moth", [["f5", "bounce"], ["moth", "eyes_big"]]),
    L(N, "Where is she taking them? Subscribe. Don't miss what waits across the water.", "wide",
      [["f0", "bounce"], ["odo", "eyes_big"]], text="WHERE IS SHE GOING?"),
]

walls = []
for i in range(6):
    for j in range(2):
        walls.append({"id": f"w{i}{j}", "type": "box", "color": [0.36, 0.36, 0.38], "at": [-3.0 + i * 1.2, 16, j * 1.2], "scale": 1.0})
prints = [{"id": f"f{k}", "type": "box", "color": [0.92, 0.95, 1.0], "glow": 1.6,
           "at": [-1.6 + k * 0.75, 8.0 + (0.35 if k % 2 else 0), 0.03], "scale": 0.3,
           **({} if k == 0 else {"visible": False})} for k in range(6)]
sc = {
    "title": "5 Footprints in the Snow. Nobody There.",
    "description": "Five footprints in the snow. They came from nowhere. And they went nowhere.",
    "lead_in": 0.05,
    "set": {"place": "chapel", "fog": 0.07, "eyes": 2, "moonlight": 2.4},
    "chars": chars,
    "props": walls + prints + [
        {"id": "boat", "type": "box", "color": [0.35, 0.22, 0.12], "at": [5.5, 9.5, 0.2], "scale": 0.7},
        {"id": "lamp", "type": "ball", "color": "gold", "glow": 2.0, "at": [-7.5, 10, 1.6], "scale": 0.3},
        {"id": "stone", "type": "ball", "color": [0.4, 0.4, 0.42], "at": [0.5, 7.5, 0.3], "scale": 0.3},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep020.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats), "words", sum(len(b["say"].split()) for b in beats))

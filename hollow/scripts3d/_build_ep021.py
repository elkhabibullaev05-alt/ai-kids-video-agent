"""Hollowmere Tales EP 21 (3D) — the Flying Dutchman. Writes scripts3d/ep021.json.
Recorded LEGEND + a documented sighting, clearly labelled (sources: britannica.com/topic/Flying-Dutchman,
en.wikipedia.org/wiki/Flying_Dutchman, archive.org 'The Cruise of Her Majesty's Ship Bacchante 1879-1882' (1886),
historycollection.com/the-truth-behind-the-legends-of-the-flying-dutchman/2, mainsailcafe.com/history/july-11):
- European sea legend: a ship doomed to sail forever and never make port; seeing her is a sign of bad luck (Britannica).
- First known print mention 1790, John MacDonald's Travels: 'The weather was so stormy that the sailors said they saw the
  Flying Dutchman' - a Dutch ship that came to the Cape in a storm, could not get into harbour, was lost; since then, in bad
  weather, her vision appears.
- Blackwood's Edinburgh Magazine, May 1821: captain Hendrick Van der Decken swore to round the Cape of Good Hope even if it
  took until doomsday; the ship offers letters addressed to people long dead; taking them brings misfortune.
- Another version: Captain Falkenberg sails the North Sea forever, playing dice with the devil (Britannica).
- Wagner's opera Der fliegende Hollaender, 1843.
- 11 July 1881, 4 a.m., between Melbourne and Sydney: the journal of Princes Albert Victor and George (later King George V),
  published 1886: 'A strange red light as of a phantom ship all aglow ... a brig 200 yards distant'; the midshipman sent
  forward found 'no vestige ... of any material ship', night clear, sea calm; 'Thirteen persons altogether saw her';
  Tourmaline and Cleopatra flashed to ask about the strange red light.
  (The seaman's fall later that day is left out - no death on screen / in narration.)
Continues EP 20 (the Lady in Black's footprints walked toward the sea).
Short 1 = hook (beat 0) + the 1881 sighting (beats 21-27): '13 men saw a ship that was not there' - loops back to beat 0."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 5])
chars["moth"] = dict(chars["moth"], home=[-3.5, 4.5])
chars["capt"] = {"name": "Captain Van der Decken", "voice": "bm_george", "speed": 0.85, "pitch": -3, "color": [0.45, 0.8, 0.75],
                 "kind": "human", "size": 1.1, "home": [4, 12]}
chars["lady"] = {"name": "The Lady in Black", "voice": "bf_emma", "speed": 0.82, "pitch": -2, "color": [0.08, 0.08, 0.11],
                 "kind": "lady", "ghost": True, "up": True, "size": 1.0, "home": [-9, 9]}
chars["prince"] = {"name": "Prince George", "voice": "bm_lewis", "speed": 1.0, "pitch": 0, "color": [0.08, 0.12, 0.3],
                   "kind": "human", "size": 0.9, "home": [-11, 7]}

# ---- the ghost ship: hull blocks + masts + sails (cones), all glowing red; moves as one by drifting every part ----
SHIP0 = (5.0, 18.0)
parts = []
for i in range(5):
    parts.append(("hull%d" % i, "box", [0.16, 0.05, 0.04], 0.6, (-2.4 + i * 1.2, 0, 0.0), 0.95))
for m, mx in enumerate((-1.6, 0.0, 1.6)):
    for k in range(3):
        parts.append((f"mast{m}{k}", "box", [0.2, 0.08, 0.05], 0.4, (mx, 0, 1.2 + k * 0.45), 0.35))
    parts.append((f"sail{m}a", "cone", [1.0, 0.25, 0.2], 2.6, (mx, 0, 1.3), 0.9))
    parts.append((f"sail{m}b", "cone", [1.0, 0.3, 0.25], 2.6, (mx, 0, 2.3), 0.7))
    parts.append((f"sail{m}c", "cone", [1.0, 0.35, 0.3], 2.6, (mx, 0, 3.1), 0.45))
EYE = ("shipeye", (0.0, -6.0, 2.6))  # invisible camera target in front of the ship: "prop:shipeye" frames the whole ship

def ship_props(visible=True):
    out = []
    for pid, typ, col, glow, (dx, dy, z), s in parts:
        out.append({"id": pid, "type": typ, "color": col, "glow": glow, "at": [SHIP0[0] + dx, SHIP0[1] + dy, z], "scale": s,
                    **({} if visible else {"visible": False})})
    out.append({"id": EYE[0], "type": "ball", "color": "white", "at": [SHIP0[0] + EYE[1][0], SHIP0[1] + EYE[1][1], EYE[1][2]],
                "scale": 0.1, "visible": False})
    return out

def ship(act_x, act_y):
    """drift every ship part so the whole ship sails to (act_x, act_y)"""
    return [[pid, "to:%.2f,%.2f,%.2f" % (act_x + dx, act_y + dy, z)] for pid, _, _, _, (dx, dy, z), _ in parts] + \
        [[EYE[0], "to:%.2f,%.2f,%.2f" % (act_x + EYE[1][0], act_y + EYE[1][1], EYE[1][2])]]

def ship_do(act):
    return [[pid, act] for pid, *_ in parts]

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big text hook + voice mid-tension at frame 1
    L(N, "Thirteen men saw a ship glowing red. Then it was gone.", "prop:shipeye",
      ship(3.5, 15.5) + [["odo", "shake"], ["moth", "eyes_big"]], text="13 MEN SAW HER"),
    L("moth", "Odo! The footprints stop right here, at the water!", "two:odo,moth", [["moth", "shake"]], sfx="alarm",
      text="THE FOOTPRINTS STOP"),
    L("lady", "Across the water... a ship is waiting.", "close:lady", [["lady", "rise"], ["odo", "turn:lady"]], text="A SHIP IS WAITING"),
    L(N, "This is a true legend of the sea. Sailors call her the Flying Dutchman.", "wide",
      [["lady", "dive"], ["capt", "rise"]], sfx="suspicious", text="THE FLYING DUTCHMAN"),
    L(N, "A ghost ship that can never reach a harbour. Never. Not in a hundred years.", "prop:shipeye",
      ship(6, 19), text="SHE NEVER REACHES PORT"),
    L("odo", "A ship that sails forever? With nobody to bring it home?", "close:odo", [["odo", "eyes_big"]]),
    # ---- the legend ----
    L(N, "The story was first written down in 1790, by a traveller named John MacDonald.", "two:odo,moth",
      [["moth", "turn:front"]], text="WRITTEN IN 1790"),
    L(N, "In a terrible storm, he wrote, the sailors said they saw the Flying Dutchman.", "overhead",
      ship(4, 17) + [["moth", "shake"]], sfx="alarm", text="IN A TERRIBLE STORM"),
    L(N, "The common story said a Dutch ship came to the Cape of Good Hope in a storm.", "prop:shipeye",
      ship_do("bounce"), text="CAPE OF GOOD HOPE"),
    L(N, "She could not get into the harbour. And she was lost.", "wide", ship(7, 21) + [["odo", "sad"]], text="SHE WAS LOST"),
    L(N, "Ever since, in very bad weather, people say her shape comes back.", "prop:shipeye",
      ship(4.5, 17), sfx="suspicious", text="SHE COMES BACK"),
    L("moth", "Bad weather? Odo, the wind is getting stronger. Right now!", "close:moth", [["moth", "spin"]]),
    L(N, "In 1821, a magazine gave the captain a name. Hendrick Van der Decken.", "close:capt",
      [["capt", "turn:front"]], text="VAN DER DECKEN"),
    L("capt", "I will sail around this Cape, even if it takes me until the end of time!", "close:capt",
      [["capt", "jump"], ["all", "shake"]], sfx="alarm", text="UNTIL THE END OF TIME"),
    L(N, "That was his promise, the story says. And so the sea kept him. Forever.", "overhead",
      ship(3, 16) + [["capt", "to:3,11"]], text="FOREVER"),
    # ---- the letters ----
    L(N, "And the strangest part. The ghost ship tries to hand you letters.", "prop:let0",
      [["let0", "show"], ["let1", "show"], ["let2", "show"]], sfx="suspicious", text="IT HANDS YOU LETTERS"),
    L(N, "Letters for people who have been gone for a very, very long time.", "close:capt",
      [["capt", "turn:odo"], ["let0", "bounce"]], text="FOR PEOPLE LONG GONE"),
    L("capt", "Take them, little one. Take them home for me.", "two:capt,odo", [["let0", "give:odo"], ["capt", "to:odo"]],
      text="TAKE THEM HOME"),
    L(N, "Sailors said: never take them. Taking them brings bad luck to your ship.", "close:odo",
      [["odo", "shake"], ["let0", "vanish"]], sfx="alarm", text="NEVER TAKE THEM"),
    L("moth", "Drop it, Odo! Drop it! Don't touch the letters!", "close:moth", [["moth", "jump"], ["let1", "vanish"], ["let2", "vanish"]]),
    L(N, "Another tale says a Captain Falkenberg sails the North Sea, playing dice with the devil.", "wide",
      [["capt", "spin"]], text="DICE WITH THE DEVIL"),
    # ---- the 1881 sighting (Short 1 segment) ----
    L(N, "But one night is written in a real journal. July eleventh, 1881.", "close:prince",
      [["prince", "enter:left"]], sfx="suspicious", text="JULY 11, 1881"),
    L(N, "Two young princes were sailing between Melbourne and Sydney. One later became King.", "two:prince,odo",
      [["prince", "turn:front"]], text="A FUTURE KING"),
    L("prince", "Four in the morning. A strange red light, on our left side!", "close:prince", [["prince", "eyes_big"]],
      text="4 A.M."),
    L(N, "A ship all aglow. Masts, spars and sails of a brig, two hundred yards away.", "prop:shipeye",
      ship(2, 14) + [["moth", "shake"]], sfx="alarm", text="200 YARDS AWAY"),
    L(N, "An officer ran forward to look. And there was nothing. No ship at all.", "wide",
      ship_do("vanish") + [["odo", "jump"]], text="NOTHING THERE"),
    L(N, "The night was clear. The sea was calm. Thirteen people saw her.", "two:prince,odo",
      [["prince", "turn:odo"]], sfx="suspicious", text="13 PEOPLE SAW HER"),
    L("prince", "Two other ships signalled us. They saw the red light too.", "close:prince", [["prince", "shake"]],
      text="THEY SAW IT TOO"),
    # ---- what is real ----
    L(N, "Scientists say a mirage can lift a far-away ship above the sea, glowing.", "overhead",
      ship_do("show") + [["prince", "exit"]], text="A MIRAGE?"),
    L(N, "But nobody can explain the ship those thirteen sailors saw.", "prop:shipeye",
      ship(5, 18), sfx="alarm", text="NO EXPLANATION"),
    L(N, "In 1843, Richard Wagner even wrote an opera about her.", "wide", [["capt", "laugh"]], text="AN OPERA, 1843"),
    # ---- Would YOU ----
    L(N, "So, would YOU take a letter from a ship that isn't there?", "close:odo",
      [["odo", "eyes_big"], ["let0", "show"]], sfx="suspicious", text="WOULD YOU TAKE IT?"),
    L("moth", "No. Never. I would run all the way back to Hollowmere.", "close:moth", [["moth", "spin"]]),
    # ---- cliffhanger ----
    L(N, "Then the red ship turned. And came straight toward the shore.", "prop:shipeye",
      ship(0, 10) + [["all", "shake"]], sfx="alarm", text="IT'S COMING"),
    L("capt", "One of you will sail with me tonight.", "close:capt", [["capt", "to:-2,8"]], text="SAIL WITH ME"),
    L("odo", "Moth... where did you go? Moth? MOTH!", "close:odo", [["moth", "exit"], ["odo", "shake"]], text="WHERE IS MOTH?"),
    L(N, "Who is on board that ship now? Subscribe. Don't miss the next tale.", "prop:shipeye",
      ship(4, 17) + [["odo", "eyes_big"]], text="WHO IS ON BOARD?"),
]

letters = [{"id": f"let{k}", "type": "box", "color": "white", "glow": 0.8, "at": [1.8 + k * 0.6, 9.5, 1.4 + k * 0.3],
            "scale": 0.22, "visible": False} for k in range(3)]
sc = {
    "title": "Never Take the Ghost Ship's Letters",
    "description": "Thirteen men saw a ship glowing red. Then it was gone.",
    "lead_in": 0.05,
    "set": {"place": "swamp", "fog": 0.06, "eyes": 3, "moonlight": 2.4},
    "chars": chars,
    "props": ship_props() + letters,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep021.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats), "words", sum(len(b["say"].split()) for b in beats))

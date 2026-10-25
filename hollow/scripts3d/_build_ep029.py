"""Hollowmere Tales EP 29 (3D) - the Beast of Gevaudan, France, 1764-1767. Writes scripts3d/ep029.json.
Documented history + legend (sources: en.wikipedia.org/wiki/Beast_of_G%C3%A9vaudan,
www.smithsonianmag.com/history/beast-gevaudan-terrorized-france-countryside-180963820,
www.britannica.com/today-in-history/September-21-The-Day-a-Beast-of-Gevaudan-Was-Killed,
en.wikipedia.org/wiki/Fran%C3%A7ois_Antoine):
- From June 1764 to June 1767 a creature called 'the Beast' haunted the hills and woods of the Gevaudan (today Lozere),
  southern France. Shepherds, many of them children, tended flocks alone on the hills.
- Witnesses: like a wolf but as big as a calf, reddish fur, a dark stripe down its back, a big head, a long tail.
- King Louis XV sent Captain Duhamel and his dragoons (1764-65); then the Norman wolf hunters d'Enneval, father and son,
  (the father said he had already killed 1,200 wolves); then in June 1765 his gun-bearer Francois Antoine.
- 20/21 Sept 1765 Antoine shot a huge wolf (the 'wolf of Chazes'); it was taken to Versailles; the king rewarded him.
- But from December 1765 the reports began again, until June 1767.
- 19 June 1767, local hunter Jean Chastel shot a large animal on the slopes of Mont Mouchet. After that, the Beast was gone.
- More than 100 wolves were killed in the region; nobody knows for sure what the Beast was (big wolf, several wolves, other theories).
No attack details, no injuries, no blood on screen. Continues EP 28 (the Pale Shepherd: 'I am already inside.')."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
chars["beast"] = dict(cast["hound"], name="The Beast", color=[0.45, 0.2, 0.09], size=1.5, home=[1.5, 15])
chars["girl"] = {"name": "A shepherd girl", "voice": "af_heart", "speed": 1.05, "pitch": 1, "color": [0.55, 0.3, 0.25],
                 "kind": "human", "size": 0.7, "home": [2.5, 10]}
chars["duhamel"] = {"name": "Captain Duhamel", "voice": "bm_daniel", "speed": 1.0, "pitch": 0, "color": [0.15, 0.25, 0.55],
                    "kind": "soldier", "size": 0.95, "home": [-11, 10.5]}
chars["antoine"] = {"name": "Francois Antoine", "voice": "bm_fable", "speed": 0.95, "pitch": -1, "color": [0.35, 0.28, 0.2],
                    "kind": "human", "size": 0.95, "home": [-30, 30]}
chars["chastel"] = {"name": "Jean Chastel", "voice": "am_adam", "speed": 0.95, "pitch": -2, "color": [0.3, 0.32, 0.22],
                    "kind": "human", "size": 0.95, "home": [-30, 30]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

# sheep on the hill (white balls), a royal banner, a lantern flash
props = [{"type": "ball", "id": f"sh{i}", "color": [0.92, 0.9, 0.85], "visible": True, "scale": 0.55,
          "at": [-3 + i * 1.6, 12 + (i % 2) * 1.2, 0.5]} for i in range(5)]
props += [{"type": "box", "id": "banner", "color": [0.15, 0.25, 0.7], "glow": 1.5, "visible": False, "scale": 0.7, "at": [-12, 13, 2.2]}]
props += [{"type": "ball", "id": "flash", "color": [1.0, 0.85, 0.45], "glow": 20, "visible": False, "scale": 0.45, "at": [-4, 13, 1.6]}]
props += [{"type": "ball", "id": "moon", "color": [0.95, 0.9, 0.75], "glow": 12, "visible": False, "scale": 1.4, "at": [14, 40, 16]}]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


SHEEP_RUN = [[f"sh{i}", f"drift:{-14 + i},{24 + i},0"] for i in range(5)]

beats = [
    # 0 s: motion (the beast steps out of the trees, the sheep scatter) + text hook + voice mid-danger
    L(N, "The sheep were running. Something red was coming out of the trees.", "wide",
      [["beast", "to:1.5,13,0"]] + SHEEP_RUN, sfx="alarm", text="DON'T STAY ON THE HILL"),
    L("moth", "Odo! It's as big as a calf! That's no wolf!", "close:moth",
      [["moth", "shake"], ["odo", "jump"]], text="BIGGER THAN A WOLF"),
    L("odo", "Look at its back, Mothwick. A black stripe, all the way to the tail.", "close:beast",
      [["beast", "turn:front"], ["beast", "eyes_big"]], sfx="suspicious", text="A BLACK STRIPE"),
    L(N, "This is a true story, from the records of France, in seventeen sixty-four.", "wide",
      [["beast", "to:6,18,0"]], text="A TRUE STORY"),
    L(N, "The Gevaudan. Cold hills, dark woods, and children watching sheep alone.", "wide",
      [["girl", "enter:left"], ["girl", "turn:front"]], text="FRANCE, 1764"),
    # ---- the beast ----
    L(N, "That summer, the shepherds began to whisper about a beast.", "close:girl",
      [["girl", "turn:odo"]], text="THE BEAST"),
    L("girl", "It has red fur and a huge head. And it isn't afraid of people.", "close:girl",
      [["girl", "shake"]], sfx="suspicious", text="NOT AFRAID OF PEOPLE"),
    L(N, "Wolves usually ran from people. This one came closer.", "close:beast",
      [["beast", "to:2,13.5,0"], ["beast", "turn:front"]], sfx="horn", text="IT CAME CLOSER"),
    L("moth", "Odo, why is it looking at us like that?", "close:moth",
      [["moth", "eyes_big"]]),
    L(N, "Soon nobody wanted to go up the hills. Families locked their doors at sunset.", "wide",
      [["beast", "to:12,22,0"], ["girl", "exit"]], text="DOORS LOCKED AT SUNSET"),
    # ---- the king's men ----
    L(N, "The news reached Paris, and King Louis the Fifteenth himself.", "wide",
      [["banner", "show"]], sfx="horn", text="THE KING HEARD"),
    L(N, "First he sent Captain Duhamel, with dozens of soldiers on horseback.", "wide",
      [["duhamel", "enter:left"], ["duhamel", "turn:front"]], text="SOLDIERS CAME"),
    L("duhamel", "Search every wood. The Beast will not escape the King's dragoons.", "close:duhamel",
      [["duhamel", "jump"]], text="SEARCH EVERY WOOD"),
    L(N, "They searched for months. The Beast was always one hill away.", "wide",
      [["beast", "to:14,26,0"], ["duhamel", "to:-2,12,0"]], sfx="suspicious", text="ALWAYS ONE HILL AWAY"),
    L(N, "Next came two famous wolf hunters. The father said he had killed twelve hundred wolves.", "close:duhamel",
      [["duhamel", "exit"]], text="1,200 WOLVES"),
    L(N, "They caught ordinary wolves. But the Beast was still out there.", "wide",
      [["beast", "to:5,17,0"], ["beast", "turn:front"]], sfx="alarm", text="STILL OUT THERE"),
    # ---- the rule ----
    L("odo", "That's the rule, Mothwick. If the flock runs, don't stay to count them.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="IF THE FLOCK RUNS..."),
    L("moth", "Run first. Count later. I can do that.", "close:moth", [["moth", "jump"]]),
    # ---- Antoine ----
    L(N, "In June seventeen sixty-five, the King sent his own gun-bearer, Francois Antoine.", "wide",
      [["antoine", "to:0,10.5,0"], ["antoine", "turn:front"], ["banner", "show"]], text="THE KING'S GUN-BEARER"),
    L(N, "In September, in the woods near Chazes, Antoine shot a huge wolf.", "close:antoine",
      [["flash", "show"], ["beast", "to:30,30,0"]], sfx="horn", text="A HUGE WOLF"),
    L("antoine", "It is done. Take it to Versailles. Tell the King the Beast is dead.", "close:antoine",
      [["flash", "vanish"], ["antoine", "jump"]], text="THE BEAST IS DEAD?"),
    L(N, "The wolf was carried to the palace. Antoine got a reward. Everyone was relieved.", "wide",
      [["antoine", "exit"], ["banner", "vanish"]], text="THE KING CHEERED"),
    L("moth", "So it's over? We can go home?", "two:odo,moth", [["moth", "turn:odo"]]),
    # ---- it came back ----
    L(N, "Then, in December, the shepherds saw it again. Red fur. The black stripe.", "close:beast",
      [["beast", "to:2,13,0"], ["beast", "turn:front"], ["all", "shake"]], sfx="alarm", text="IT CAME BACK"),
    L("odo", "The King said it was dead. Nobody told the Beast.", "close:odo",
      [["odo", "eyes_big"]], sfx="suspicious", text="NOBODY TOLD THE BEAST"),
    L(N, "For eighteen more months, the hills of the Gevaudan were afraid again.", "wide",
      [["beast", "to:-3,15,0"]] + SHEEP_RUN, text="18 MORE MONTHS"),
    # ---- Chastel ----
    L(N, "June the nineteenth, seventeen sixty-seven. A local hunter, Jean Chastel, waited on Mont Mouchet.", "wide",
      [["chastel", "to:-1,10.5,0"], ["chastel", "turn:beast"], ["moon", "show"]], text="MONT MOUCHET, 1767"),
    L(N, "The Beast walked out of the trees, straight toward him.", "close:beast",
      [["beast", "to:-3,12.5,0"], ["beast", "turn:front"]], sfx="horn", text="STRAIGHT TOWARD HIM"),
    L(N, "One shot. And after that night, the Beast was never seen again.", "close:chastel",
      [["flash", "show"], ["beast", "to:30,30,0"], ["all", "shake"]], sfx="alarm", text="ONE SHOT"),
    L("chastel", "It is gone. The children can go up the hills again.", "close:chastel",
      [["flash", "vanish"], ["chastel", "turn:front"]], text="IT IS GONE"),
    # ---- the mystery ----
    L(N, "More than a hundred wolves were killed in those years. So which one was the Beast?", "two:odo,moth",
      [["odo", "turn:moth"]], text="100 WOLVES. WHICH ONE?"),
    L(N, "Some say a giant wolf. Some say a pack. Nobody knows for sure.", "wide",
      [["moth", "eyes_big"]], sfx="suspicious", text="NOBODY KNOWS"),
    L(N, "So, would YOU watch the sheep alone on the Gevaudan hills tonight?", "close:odo",
      [["odo", "eyes_big"]], sfx="alarm", text="WOULD YOU GO UP THERE?"),
    L("moth", "Not for all the King's gold. I'd stay by the fire.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then the sheep ran again. And a tall pale figure walked out of the trees.", "wide",
      [["shepherd", "to:1.5,14,0"], ["all", "shake"]] + SHEEP_RUN, sfx="alarm", text="THE SHEEP RAN AGAIN"),
    L("shepherd", "Every flock needs a shepherd, lantern-bearer. And this one is mine.", "close:shepherd",
      [["shepherd", "turn:front"]], sfx="suspicious", text="THIS FLOCK IS MINE"),
    L(N, "What did the Shepherd send into the hills? Subscribe, so you don't miss the next true tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="horn", text="WHAT DID IT SEND?"),
]

sc = {
    "title": "1764: What Hunted the Hills of France?",
    "description": "From 1764 to 1767, a red beast haunted the hills of the Gevaudan in France. The King sent his soldiers. It came back.",
    "lead_in": 0.05,
    "set": {"place": "hill", "fog": 0.04, "eyes": 2, "moonlight": 14},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep029.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

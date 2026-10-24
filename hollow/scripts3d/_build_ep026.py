"""Hollowmere Tales EP 26 (3D) - Spring-heeled Jack, London, 1837-1838 (+ later sightings to 1904). Writes scripts3d/ep026.json.
Recorded accounts / Victorian legend, clearly labelled (sources: en.wikipedia.org/wiki/Spring-heeled_Jack,
thecollector.com/spring-heeled-jack-victorian-england, theundergroundmap.substack.com/p/the-tale-of-spring-heeled-jack):
- From late 1837 Londoners told of a figure who sprang out of the dark and leapt away; one story says after jumping in front
  of a carriage it sprang over a nine-foot wall, cackling - hence "Spring-heeled Jack". (Mary Stevens, Clapham Common,
  Oct 1837 - known only from much later retellings.)
- 9 January 1838: Lord Mayor Sir John Cowan read out at the Mansion House an anonymous letter from "a resident of Peckham":
  a man disguised as a ghost, a bear and a devil was frightening people for a bet.
- 19 February 1838: Jane Alsop (East London, her father's house; Bearbinder Lane / Old Ford) opened the door to a man who said
  he was a policeman: "we have caught Spring-heeled Jack here in the lane" - bring a light. He threw off his cloak: big
  helmet, tight white oilskin-like clothes, eyes like "red balls of fire", blue and white flame from his mouth, metal-like
  claws; he grabbed at her, her sister pulled her away and he fled.
- 28 February 1838: Lucy Scales (18), Green Dragon Alley, Limehouse: a tall thin figure in a cloak sprayed blue flame at
  her face, said nothing and walked away.
- A man who boasted he was Jack (Thomas Millbank) was let go: he could not breathe fire.
- Later: Aldershot 1877 (sentries; it vanished "with astonishing bounds"), Everton, Liverpool (~1888 church roof, 1904
  William Henry Street, the last report). Never caught; pranksters, panic or something else - nobody knows.
No injuries described. Continues EP 25 (the Pale Shepherd came up the road: 'Even the little ones warn you now.')."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 7])
chars["moth"] = dict(chars["moth"], home=[-4, 7])
chars["jack"] = {"name": "Spring-heeled Jack", "voice": "bm_lewis", "speed": 0.85, "pitch": -3, "color": [0.05, 0.03, 0.06],
                 "kind": "jack", "size": 0.95, "home": [3, 14]}
chars["jane"] = {"name": "Jane Alsop", "voice": "bf_emma", "speed": 1.0, "pitch": 1, "color": [0.45, 0.32, 0.5],
                 "kind": "human", "size": 0.85, "home": [-7, 11]}
chars["sister"] = {"name": "Jane's sister", "voice": "bf_alice", "speed": 1.05, "pitch": 1, "color": [0.3, 0.42, 0.3],
                   "kind": "human", "size": 0.8, "home": [-9.5, 11.5]}
chars["lucy"] = {"name": "Lucy, 18", "voice": "af_nicole", "speed": 1.0, "pitch": 1, "color": [0.55, 0.15, 0.2],
                 "kind": "human", "size": 0.85, "home": [-8, 9]}
chars["mayor"] = {"name": "The Lord Mayor", "voice": "bm_fable", "speed": 0.95, "pitch": -1, "color": [0.55, 0.08, 0.08],
                  "kind": "human", "size": 1.0, "home": [-8, 13]}
chars["shepherd"] = dict(cast["shepherd"], home=[30, 30], size=0.85)

STONE = {"type": "box", "color": [0.3, 0.26, 0.24], "visible": True}
props = [dict(STONE, id=f"w{r}{i}", at=[-2.2 + i * 1.4, 16.0 + (i % 2) * 0.05, r * 1.42], scale=1.2) for r in range(1) for i in range(6)]  # the wall
FL = {"type": "ball", "color": [0.35, 0.6, 1.0], "glow": 18, "visible": False, "scale": 0.45}
props += [dict(FL, id="fl1", at=[-4.2, 9.4, 3.3]), dict(FL, id="fl2", at=[-5.6, 8.6, 3.2])]
props += [{"type": "ball", "id": "cand", "color": [1.0, 0.8, 0.4], "glow": 10, "visible": False, "scale": 0.22, "at": [-6.2, 10.6, 2.4]}]

N = "narr"


def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b


beats = [
    # 0 s: motion (Jack lands on the wall, Odo skids back) + big text hook + voice mid-danger
    L(N, "Someone is knocking. He says he is a policeman. Do not open the door.", "wide",
      [["jack", "to:2.5,15.6,1.45"], ["odo", "to:-6,9,0"], ["moth", "to:-4,9.5,2"]], sfx="alarm",
      text="DON'T OPEN THE DOOR"),
    L("moth", "Odo! Something jumped right over that wall. That wall is taller than a house!", "close:moth",
      [["moth", "shake"]], text="IT JUMPED THE WALL"),
    L("odo", "Shh. Look at its eyes, Mothwick. They are burning red.", "close:jack",
      [["jack", "turn:front"]], sfx="suspicious", text="RED EYES"),
    L(N, "This is a true legend, from the records of old London. They called him Spring-heeled Jack.", "overhead",
      [["jack", "jump"]], text="SPRING-HEELED JACK"),
    L(N, "London, eighteen thirty-seven. The streets were dark, lit only by gas lamps.", "close:odo",
      [["odo", "turn:front"]], text="LONDON, 1837"),
    # ---- the name ----
    L(N, "People said a figure sprang out of the dark, in front of a carriage.", "wide",
      [["jack", "to:0,12,0"]], sfx="alarm", text="OUT OF THE DARK"),
    L(N, "Then it leapt over a nine-foot wall. And it was laughing.", "close:jack",
      [["jack", "to:2.5,15.6,1.45"], ["jack", "jump"]], sfx="horn", text="A 9-FOOT WALL"),
    L("moth", "Nobody can jump that high. Nobody with normal feet.", "close:moth", [["moth", "eyes_big"]]),
    L(N, "So the newspapers gave him a name. Jack, with springs in his heels.", "two:odo,jack",
      [["jack", "bounce"]], text="SPRINGS IN HIS HEELS"),
    # ---- the Lord Mayor ----
    L(N, "January eighteen thirty-eight. The Lord Mayor of London stood up with a letter.", "close:mayor",
      [["mayor", "enter:left"]], sfx="suspicious", text="JANUARY 1838"),
    L("mayor", "A man is frightening people at night, dressed as a ghost, a bear, and a devil!", "close:mayor",
      [["mayor", "shake"]]),
    L(N, "The letter said he did it for a bet. But nobody could catch him.", "overhead",
      [["mayor", "exit"], ["jack", "jump"]], text="NOBODY CAUGHT HIM"),
    # ---- Jane Alsop ----
    L(N, "February the nineteenth. A girl named Jane Alsop heard a knock at her door.", "close:jane",
      [["jane", "enter:left"]], sfx="alarm", text="A KNOCK AT THE DOOR"),
    L("jack", "I am a policeman. Bring me a light. We have caught Spring-heeled Jack in the lane!", "close:jack",
      [["jack", "to:-4,10,0"], ["jack", "turn:front"]], text="\"BRING A LIGHT\""),
    L(N, "So Jane brought a candle. And she opened the door.", "two:jane,jack",
      [["cand", "show"], ["jane", "to:-6.6,11"]], sfx="suspicious", text="SHE OPENED IT"),
    L(N, "The man threw off his cloak. He wore a big helmet and tight white clothes.", "close:jack",
      [["jack", "shake"]], text="A BIG HELMET"),
    L(N, "Jane said his eyes were like red balls of fire.", "close:jack",
      [["jack", "eyes_big"]], sfx="alarm", text="BALLS OF FIRE"),
    L(N, "And from his mouth came blue and white flames.", "close:jack",
      [["fl1", "show"], ["fl1", "drift:-6.2,10.6,3"]], sfx="horn", text="BLUE FLAMES"),
    L("jane", "Help me! His hands are like cold metal claws!", "close:jane",
      [["jane", "shake"], ["fl1", "vanish"]]),
    L("sister", "Jane! Get inside! Shut the door!", "two:jane,sister",
      [["sister", "enter:left"], ["sister", "jump"]]),
    L(N, "Her sister pulled her inside. And the creature ran into the night.", "wide",
      [["cand", "vanish"], ["jack", "to:2.5,15.6,1.45"], ["jane", "exit"], ["sister", "exit"]], text="IT RAN"),
    # ---- the rule ----
    L("odo", "That is the rule, Mothwick. If a stranger at night asks you for a light, keep the door shut.", "close:odo",
      [["odo", "shake"]], sfx="suspicious", text="KEEP IT SHUT"),
    # ---- Lucy Scales ----
    L(N, "Nine days later, in a dark lane called Green Dragon Alley, eighteen-year-old Lucy was walking home.", "close:lucy",
      [["lucy", "enter:left"]], text="GREEN DRAGON ALLEY"),
    L(N, "A tall, thin figure in a cloak stepped out. A flash of blue flame lit her face.", "wide",
      [["jack", "to:-4.5,10,0"], ["fl2", "show"]], sfx="alarm", text="A FLASH OF BLUE"),
    L("lucy", "I can't see! Who are you? Why won't you answer?", "close:lucy",
      [["lucy", "shake"], ["fl2", "vanish"]]),
    L(N, "He did not say a single word. He simply turned, and walked away.", "close:jack",
      [["jack", "turn:front"], ["jack", "to:2.5,15.6,1.45"], ["lucy", "exit"]], text="NOT ONE WORD"),
    L("moth", "Odo, it's looking at us now. Why is it looking at us?", "close:moth",
      [["moth", "shake"], ["moth", "to:-5,7,1.5"]], sfx="suspicious", text="IT'S LOOKING AT US"),
    # ---- never caught ----
    L(N, "One man bragged that he was Jack. But he could not breathe fire, so he was let go.", "overhead",
      [["jack", "bounce"]], text="HE COULDN'T BREATHE FIRE"),
    L(N, "Forty years later, soldiers on guard saw a figure bound away in giant leaps.", "wide",
      [["jack", "to:-2,13,0"], ["jack", "jump"]], sfx="horn", text="40 YEARS LATER"),
    L(N, "The last report came in nineteen-oh-four, in Liverpool. Then he was gone.", "close:jack",
      [["jack", "to:2.5,15.6,1.45"]], text="1904: THE LAST"),
    L(N, "Was he a prankster in a costume? Was it panic in the dark? No one ever found out.", "two:odo,moth",
      [["odo", "turn:moth"]], sfx="suspicious", text="NEVER CAUGHT"),
    # ---- Would YOU ----
    L(N, "So, would YOU open the door, if someone knocked and asked for a light?", "close:odo",
      [["odo", "eyes_big"]], sfx="alarm", text="WOULD YOU OPEN IT?"),
    L("moth", "Never. I would hide under the bed with my lantern off.", "close:moth", [["moth", "shake"]]),
    # ---- cliffhanger ----
    L(N, "Then Jack crouched on the wall, and pointed down the dark street.", "close:jack",
      [["jack", "turn:front"], ["jack", "shake"]], sfx="suspicious", text="HE POINTED"),
    L(N, "The gas lamps went out, one by one. Something pale was walking toward them.", "wide",
      [["shepherd", "to:8,17,0"], ["all", "shake"]], sfx="alarm", text="THE LAMPS WENT OUT"),
    L("shepherd", "Run all you like, lantern-bearer. Every wall in this town is mine.", "close:shepherd",
      [["shepherd", "turn:front"]], text="IT FOUND US"),
    L(N, "Who will open the next door? Subscribe, so you don't miss the next tale.", "close:odo",
      [["odo", "shake"], ["moth", "eyes_big"]], sfx="horn", text="WHO KNOCKS NEXT?"),
]

sc = {
    "title": "Spring-heeled Jack: Don't Open the Door",
    "description": "In 1838, London was terrified of a leaping figure with fiery eyes who knocked on doors at night.",
    "lead_in": 0.05,
    "set": {"place": "village", "fog": 0.04, "eyes": 2, "moonlight": 7},
    "chars": chars,
    "props": props,
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep026.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats),
      "words", sum(len(b["say"].split()) for b in beats))

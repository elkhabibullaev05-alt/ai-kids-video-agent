"""Build scripts3d/ep043.json - the Croglin Grange 'vampire', Cumberland, England (told by Captain Edward Fisher
to Augustus Hare in 1874, printed in Hare's Story of My Life, 1896-1900). Standalone recorded legend.
python3 scripts3d/_build_ep043.py"""
import json
H = lambda name, voice, sp, pi, col, home, size=0.85, kind="human", **kw: dict(name=name, voice=voice, speed=sp, pitch=pi, color=col, kind=kind, size=size, home=home, **kw)
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.92, "pitch": -1},
 "sister": H("The sister", "bf_emma", 0.97, 0, [0.55, 0.5, 0.6], [-2.2, 8.6], 0.78),
 "bro1": H("Her elder brother", "bm_lewis", 0.97, -1, [0.15, 0.18, 0.3], [-30, 32], 0.9),
 "bro2": H("Her younger brother", "am_adam", 1.02, 0, [0.3, 0.16, 0.1], [-34, 34], 0.88),
 "thing": H("The thing", "bm_daniel", 0.78, -5, [0.22, 0.14, 0.07], [9, 22], 0.98),
 "writer": H("Charles Harper", "am_michael", 0.98, -1, [0.2, 0.2, 0.22], [-38, 40], 0.86),
 "girl": H("A girl", "af_sarah", 1.06, 2, [0.4, 0.3, 0.45], [-42, 44], 0.62),
}
P = lambda t, i, col, sc, at, vis=True, glow=0: dict(type=t, id=i, color=col, glow=glow, visible=vis, scale=sc, at=at)
props = [
 P("box", "window", [0.12, 0.14, 0.2], 0.55, [1.4, 10.6, 1.0], True, 0),
 P("box", "pane", [0.75, 0.85, 1.0], 0.2, [1.4, 10.2, 1.25], True, 2),
 P("ball", "eyeL", [1.0, 0.35, 0.05], 0.12, [7.6, 21, 2.2], True, 6),
 P("ball", "eyeR", [1.0, 0.35, 0.05], 0.12, [8.2, 21, 2.2], True, 6),
 P("box", "wall", [0.3, 0.3, 0.28], 1.6, [6, 15, 0]),
 P("box", "vault", [0.22, 0.21, 0.2], 2.2, [-5.5, 14, 0], False),
 P("box", "coffin", [0.2, 0.13, 0.08], 0.8, [-4.5, 11.5, 0], False),
 P("cone", "candle", [1.0, 0.85, 0.5], 0.3, [-1.0, 9.3, 1.4], True, 4),
 P("ball", "moon", [0.8, 0.85, 1.0], 1.6, [10, 40, 14], True, 4),
 P("box", "book", [0.5, 0.12, 0.1], 0.45, [-3.5, 8.5, 1.4], False, 1),
]
B = []
def b(who, say, cam, do, sfx, text): B.append(dict(who=who, say=say, cam=cam, do=do, sfx=sfx, text=text))
# 0-5 s: hook on frame 1, danger already happening
b("sister", "Something is scratching at my window. And it is picking the glass out.", "two:sister,thing", [["thing", "to:2.7,11.8,0"], ["pane", "spin"], ["sister", "eyes_big"]], "alarm", "IT'S AT THE WINDOW")
b("narr", "Scratch. Scratch. A long fingernail, pulling the lead from around one little pane.", "prop:pane", [["pane", "bounce"], ["window", "bounce"]], "crunch", "SCRATCH. SCRATCH.")
b("narr", "This story was told as true by a captain in eighteen seventy-four. Cumberland, England.", "wide", [["thing", "to_home"], ["moon", "bounce"]], "horn", "CUMBERLAND, ENGLAND")
b("narr", "The writer Augustus Hare wrote it down. People still argue about it today.", "prop:book", [["book", "show"], ["book", "spin"]], "dun", "TOLD AS TRUE")
b("narr", "The house was called Croglin Grange. One storey, low and old, beside a churchyard.", "wide", [["book", "hide"], ["wall", "bounce"]], "whoosh", "CROGLIN GRANGE")
b("narr", "Two brothers and their sister rented it. They loved how quiet it was.", "two:sister,bro1", [["bro1", "to:-5,9.6,0"], ["bro2", "to:-6.8,10.4,0"], ["bro1", "turn:sister"]], "chime", "SO QUIET")
b("bro1", "No neighbours, no noise. Only the church and the graves next door.", "close:bro1", [["bro1", "happy"], ["bro2", "laugh"]], "pop", "ONLY THE GRAVES")
b("narr", "One hot summer night, the sister could not sleep. She sat up by her window.", "close:sister", [["bro1", "to_home"], ["bro2", "to_home"], ["sister", "turn:front"]], "suspicious", "SHE COULDN'T SLEEP")
b("narr", "Far off, between the trees and the churchyard, she saw two little lights.", "prop:eyeL", [["eyeL", "bounce"], ["eyeR", "bounce"]], "rumble", "TWO LIGHTS")
b("sister", "Lanterns? At this hour? Who walks among the graves at midnight?", "close:sister", [["sister", "eyes_big"]], "suspicious", "WHO WALKS THERE?")
b("narr", "The lights came closer. They were not lanterns. They were eyes.", "prop:eyeR", [["eyeL", "spin"], ["eyeR", "spin"], ["thing", "to:6,17,0"]], "alarm", "THEY WERE EYES")
b("narr", "A dark figure was crossing the grass. Straight towards her window.", "two:sister,thing", [["thing", "to:3,14,0"], ["eyeL", "hide"], ["eyeR", "hide"]], "dun", "COMING CLOSER")
b("narr", "She jumped from her chair and ran for the door. It was locked from the inside.", "close:sister", [["sister", "to:-4.5,8.2,0"], ["sister", "shake"]], "whoosh", "THE DOOR WON'T OPEN")
b("narr", "Her fingers shook. The key would not turn. Behind her, the scratching began.", "prop:window", [["window", "bounce"], ["thing", "to:2.7,11.8,0"]], "crunch", "SCRATCHING")
b("narr", "Then the little pane fell inside. A hand reached through and turned the catch.", "prop:pane", [["pane", "hide"], ["window", "spin"]], "alarm", "A HAND CAME THROUGH")
b("narr", "The window swung open. The thing climbed into her room.", "two:sister,thing", [["thing", "to:-1.5,10.2,0"], ["candle", "spin"]], "dun", "IT CAME IN")
b("narr", "Its face was brown and dried, like old leather. Its eyes burned like fire.", "close:thing", [["thing", "turn:sister"], ["thing", "eyes_big"]], "rumble", "EYES LIKE FIRE")
b("sister", "Help me! Somebody, help me!", "close:sister", [["sister", "shake"], ["sister", "eyes_big"]], "alarm", "HELP ME!")
b("narr", "Her brothers broke down the door. The creature fled over the wall into the churchyard.", "wide", [["bro1", "to:-4,9.4,0"], ["bro2", "to:-5.6,10,0"], ["thing", "to:6,17,0"], ["wall", "bounce"]], "whoosh", "OVER THE WALL")
b("bro2", "It's gone! Into the graves! I lost it in the dark!", "close:bro2", [["bro2", "shake"], ["thing", "to_home"]], "suspicious", "INTO THE GRAVES")
b("narr", "The sister was hurt and frightened, but she lived. The doctors sent her far away to rest.", "close:sister", [["sister", "sad"], ["bro1", "turn:sister"]], "chime", "SHE LIVED")
b("narr", "If you like true legends like this one, subscribe. Because the family came back.", "wide", [["moon", "bounce"]], "pop", "SUBSCRIBE")
b("narr", "Months later, they returned to Croglin. The sister said she was not afraid.", "two:sister,bro1", [["bro1", "to:-4.5,9.6,0"], ["sister", "turn:bro1"]], "horn", "THEY CAME BACK")
b("sister", "Lightning does not strike twice. But please, sleep in the room next to mine.", "close:sister", [["sister", "turn:front"]], "suspicious", "SLEEP NEXT DOOR")
b("narr", "Her brothers slept next door, ready, with the window always in sight.", "two:bro1,bro2", [["bro2", "to:-6,10.6,0"], ["bro1", "turn:front"], ["bro2", "turn:front"]], "dun", "READY")
b("narr", "For a long time, nothing came. Then, one cold night in March...", "prop:window", [["candle", "spin"]], "rumble", "ONE NIGHT IN MARCH")
b("narr", "Scratch. Scratch. Scratch.", "prop:pane", [["pane", "show"], ["pane", "bounce"], ["thing", "to:2.7,11.8,0"]], "crunch", "IT CAME BACK")
b("bro1", "It's here! At the window! Quick!", "close:bro1", [["bro1", "jump"], ["bro1", "eyes_big"]], "alarm", "IT'S HERE!")
b("narr", "The brothers rushed out. The creature ran across the grass, limping, and vanished.", "wide", [["thing", "to:-5.5,14.5,0"], ["bro1", "to:-2,12,0"], ["bro2", "to:-3,12.6,0"]], "whoosh", "IT RAN")
b("narr", "It vanished into an old family vault in the churchyard. Nobody had opened it in years.", "prop:vault", [["vault", "show"], ["thing", "to_home"]], "dun", "THE OLD VAULT")
b("narr", "The next morning, the brothers opened the vault. Every coffin had been broken open, except one.", "prop:coffin", [["coffin", "show"], ["vault", "bounce"]], "rumble", "EXCEPT ONE")
b("narr", "Inside lay a dried, brown figure. The same face. And a fresh wound in its leg.", "close:bro2", [["bro2", "eyes_big"], ["coffin", "shake"]], "alarm", "THE SAME FACE")
b("narr", "So the story says, they burned it. And the thing never came back.", "wide", [["coffin", "hide"], ["candle", "spin"]], "dun", "NEVER CAME BACK")
b("narr", "Fifty years later, the writer Charles Harper went looking for Croglin Grange.", "close:writer", [["writer", "to:-2.5,9.2,0"], ["writer", "turn:front"], ["vault", "hide"]], "whoosh", "1924: THE SEARCH")
b("writer", "There is no Croglin Grange here. And the church has no record of any vault.", "close:writer", [["writer", "shake"]], "suspicious", "NO SUCH HOUSE?")
b("narr", "Some say the captain made it up. Some say the names were changed. Nobody knows.", "wide", [["writer", "to_home"], ["wall", "bounce"]], "dun", "NOBODY KNOWS")
b("narr", "So remember the rule of Croglin. If you see two lights in the trees, close your shutters.", "prop:window", [["eyeL", "show"], ["eyeR", "show"]], "alarm", "CLOSE YOUR SHUTTERS")
b("narr", "Tonight, a girl is staying in an old farmhouse near Croglin. She cannot sleep.", "close:girl", [["girl", "to:-2.2,8.8,0"], ["girl", "turn:front"]], "rumble", "TONIGHT...")
b("girl", "Two little lights, out in the trees. Lanterns, I suppose.", "close:girl", [["girl", "happy"], ["eyeL", "bounce"], ["eyeR", "bounce"]], "suspicious", "TWO LITTLE LIGHTS")
b("narr", "The lights blink. Then, very softly, something scratches at her window.", "two:girl,thing", [["thing", "to:2.7,11.8,0"], ["pane", "spin"], ["girl", "eyes_big"]], "alarm", "SCRATCH...")
b("narr", "What do you think happens next? Tell me in the comments.", "two:girl,thing", [["girl", "shake"], ["thing", "turn:girl"]], "dun", "WHAT HAPPENS NEXT?")
sc = dict(title="Who Picked the Glass From Her Window?",
          description="A recorded English legend: the Croglin Grange 'vampire' of Cumberland, told as true in 1874 and written down by Augustus Hare. What do you think happens next? Tell me in the comments.",
          lead_in=0.0, set={"place": "graveyard", "fog": 0.05, "eyes": 0, "moonlight": 16}, chars=chars, props=props, beats=B)
json.dump(sc, open(__file__.replace("_build_ep043.py", "ep043.json"), "w"), indent=1)
print(len(B), "beats", sum(len(x["say"].split()) for x in B), "words", len(sc["title"]), "title chars")

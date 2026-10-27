"""Ep 34 - the Drummer of Tedworth (Tidworth, Wiltshire, 1662-1663). Builds scripts3d/ep034.json from ep033's cast."""
import json, copy, os
H = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(H, "ep033.json")))
ch = {k: copy.deepcopy(base["chars"][k]) for k in ("odo", "moth", "narr", "shepherd", "dog", "wren")}
ch["odo"]["home"] = [-6, 7]; ch["moth"]["home"] = [-4.5, 7]; ch["dog"]["home"] = [-2.5, 8]
ch["mom"] = {"name": "John Mompesson", "voice": "bm_lewis", "speed": 0.95, "pitch": -1, "color": [0.15, 0.12, 0.25], "kind": "human", "size": 0.85, "home": [-30, 30]}
ch["wife"] = {"name": "Mrs Mompesson", "voice": "bf_emma", "speed": 0.95, "pitch": 0, "color": [0.35, 0.15, 0.2], "kind": "human", "size": 0.8, "home": [-30, 32]}
ch["drummer"] = {"name": "William Drury", "voice": "am_adam", "speed": 1.0, "pitch": -1, "color": [0.4, 0.3, 0.1], "kind": "human", "size": 0.85, "home": [30, 34]}
ch["glanvill"] = {"name": "Joseph Glanvill", "voice": "am_michael", "speed": 0.95, "pitch": 0, "color": [0.05, 0.05, 0.06], "kind": "human", "size": 0.85, "home": [-30, 36]}
props = [
    {"type": "cake", "id": "drum", "color": [0.55, 0.1, 0.08], "glow": 3, "visible": True, "scale": 0.7, "at": [1.5, 9.5, 0.3]},
    {"type": "ball", "id": "lamp", "color": [1.0, 0.75, 0.35], "glow": 10, "visible": True, "scale": 0.15, "at": [-1.5, 10.5, 1.8]},
    {"type": "ball", "id": "lamp2", "color": [1.0, 0.75, 0.35], "glow": 10, "visible": True, "scale": 0.15, "at": [4.0, 10.5, 1.8]},
    {"type": "box", "id": "bed", "color": [0.35, 0.3, 0.25], "visible": False, "scale": 1.3, "at": [5.0, 11.0, 0]},
    {"type": "box", "id": "paper", "color": [0.92, 0.88, 0.75], "glow": 1, "visible": False, "scale": 0.35, "at": [-1.0, 8.5, 1.2]},
    {"type": "ball", "id": "pdark", "color": [0.9, 0.1, 0.05], "glow": 6, "visible": False, "scale": 0.1, "at": [0.0, 15.0, 1.4]},
]
B = []
def b(who, say, cam, do=(), sfx=None, text=None):
    x = {"who": who, "say": say, "cam": cam, "do": [list(d) for d in do]}
    if sfx: x["sfx"] = sfx
    if text: x["text"] = text
    B.append(x)
# hook at 0 s: danger + motion + big text
b("narr", "Nobody touched the drum. But every night, it played.", "prop:drum", [("drum", "bounce"), ("drum", "spin"), ("odo", "shake")], "alarm", "IT PLAYS ITSELF")
b("moth", "Odo! It's moving! Nobody's holding the sticks!", "close:moth", [("moth", "jump"), ("drum", "bounce")], "crunch", "NOBODY'S THERE")
b("narr", "New episode every day. Subscribe so you don't miss what happens next.", "two:odo,moth", [("odo", "turn:front"), ("moth", "turn:front")], None, "SUBSCRIBE")
b("narr", "Last night the black dog led them into the sealed passage. Together.", "close:dog", [("dog", "to:-1,9,0"), ("dog", "turn:odo")], "whoosh", "NEVER ALONE")
b("odo", "Wren's voice came from down here. Wren? Are you here?", "close:odo", [("odo", "to:-4,8,0"), ("pdark", "show")], "suspicious", "WREN?")
b("moth", "The tunnel ends in a house. A table. And a drum on it.", "wide", [("moth", "to:-3,8,0"), ("drum", "bounce")], "pop", "A DRUM")
b("narr", "This drum comes from a true story, recorded in the sixteen sixties.", "prop:drum", [("drum", "spin")], "horn", "A TRUE STORY")
b("narr", "Tedworth, a town in Wiltshire, England. Today it's called Tidworth.", "wide", [("lamp", "bounce"), ("lamp2", "bounce")], None, "TEDWORTH, ENGLAND")
b("narr", "A landowner named John Mompesson was visiting nearby Ludgershall.", "close:mom", [("mom", "to:3,9,0"), ("mom", "turn:front")], None, "JOHN MOMPESSON")
b("narr", "There, a wandering drummer, William Drury, was asking for money.", "close:drummer", [("drummer", "to:6,10,0"), ("drummer", "turn:mom")], "rumble", "THE DRUMMER")
b("mom", "Your papers are false, drummer. That pass is forged.", "close:mom", [("mom", "turn:drummer")], "alarm", "FORGED PAPERS")
b("narr", "Drury was arrested and later let go. But his drum was taken from him.", "two:mom,drummer", [("drum", "to:3.5,9.5,0.3"), ("drummer", "shake")], "crunch", "THEY TOOK HIS DRUM")
b("drummer", "Give me back my drum! That drum is mine!", "close:drummer", [("drummer", "jump")], None, "GIVE IT BACK")
b("narr", "The drum was sent to Mompesson's house. And that's when it started.", "prop:drum", [("drummer", "exit"), ("drum", "to:1.5,9.5,0.3")], "rumble", "THEN IT STARTED")
b("wife", "Someone is in the house! I hear knocking! Thumping on the roof!", "close:wife", [("wife", "to:5,9.5,0"), ("wife", "turn:front"), ("wife", "shake")], "crunch", "KNOCKING IN THE NIGHT")
b("narr", "Mompesson heard it too. Drumming, on top of the house, in the dark.", "close:mom", [("mom", "eyes_big"), ("lamp", "vanish")], "alarm", "DRUMMING ON THE ROOF")
b("moth", "Drumming on the roof? Who drums on a roof at night?", "close:moth", [("moth", "eyes_big"), ("odo", "turn:moth")], None, "WHO DRUMS AT NIGHT?")
b("narr", "It began when the lights went out. And it came from the room with the drum.", "prop:drum", [("lamp2", "vanish"), ("drum", "bounce")], "suspicious", "WHEN THE LIGHTS GO OUT")
b("mom", "I'll sleep in that room myself. Then we'll see who plays it.", "close:mom", [("mom", "to:2.5,9,0")], None, "I'LL WATCH IT")
b("narr", "He watched. No one came in. And still, the drum beat.", "prop:drum", [("drum", "bounce"), ("mom", "shake")], "crunch", "NO ONE CAME IN")
b("odo", "Mothwick. The rule here: never take what isn't yours.", "close:odo", [("odo", "shake")], "suspicious", "NEVER TAKE WHAT ISN'T YOURS")
b("moth", "I didn't take anything! Well, one crumb. Does a crumb count?", "close:moth", [("moth", "jump")])
b("narr", "When Mrs Mompesson had a baby, the noise stopped for three weeks.", "close:wife", [("lamp", "show"), ("lamp2", "show")], "pop", "THREE QUIET WEEKS")
b("narr", "Then it came back. Louder. Into the children's room.", "prop:bed", [("bed", "show"), ("bed", "bounce"), ("lamp", "vanish")], "alarm", "IT CAME BACK")
b("wife", "The beds! Something is shaking the children's beds!", "close:wife", [("wife", "shake"), ("bed", "bounce")], "rumble", "THE BEDS SHOOK")
b("narr", "In December sixteen sixty-two, Mompesson wrote a letter about it.", "prop:paper", [("paper", "show"), ("paper", "spin")], "pop", "HIS OWN LETTER")
b("mom", "A supernatural beating of drums. Every night. In my own house.", "close:mom", [("mom", "turn:front")], None, "EVERY NIGHT")
b("narr", "In January sixteen sixty-three, a clergyman came to see: Joseph Glanvill.", "close:glanvill", [("glanvill", "to:4.5,10,0"), ("glanvill", "turn:front")], "horn", "A WITNESS CAME")
b("glanvill", "Scratching. In the girls' room. Behind the bed. I searched. Nothing there.", "close:glanvill", [("glanvill", "eyes_big"), ("bed", "bounce")], "suspicious", "NOTHING THERE")
b("narr", "Glanvill later put it in his book, printed in sixteen eighty-one.", "prop:paper", [("paper", "bounce")], None, "1681: THE BOOK")
b("narr", "And the drummer? In prison, people said, he bragged about it.", "close:drummer", [("drummer", "to:6,10,0"), ("drummer", "turn:front")], "rumble", "HE BRAGGED")
b("drummer", "I have plagued him. He'll never be quiet until he pays me for my drum.", "close:drummer", [("drummer", "shake")], "alarm", "NEVER QUIET")
b("narr", "He was tried for witchcraft. The court did not find him guilty.", "two:mom,drummer", [("mom", "turn:drummer")], "crunch", "NOT GUILTY")
b("narr", "Some said it was a trick. Nobody ever proved who beat the drum.", "prop:drum", [("drummer", "exit"), ("mom", "exit"), ("wife", "exit"), ("glanvill", "exit")], "rumble", "NO ONE KNOWS")
b("moth", "So it's just an old drum. Old drums don't play. Right, Odo?", "close:moth", [("moth", "to:0.5,9,0"), ("moth", "bounce")], None, "JUST A DRUM?")
b("narr", "Mothwick's wing brushed the drum. It beat. Once.", "prop:drum", [("drum", "bounce"), ("moth", "jump")], "crunch", "BOOM")
b("narr", "And outside, in the fog, another drum answered.", "wide", [("pdark", "bounce"), ("dog", "turn:front")], "alarm", "SOMETHING ANSWERED")
b("odo", "Mothwick. Don't. Touch. Anything.", "close:odo", [("odo", "eyes_big")], None, "DON'T TOUCH IT")
b("narr", "The black dog growled at the window. A tall shape stood in the fog.", "close:shepherd", [("shepherd", "to:-7,13,0"), ("shepherd", "turn:front"), ("dog", "shake")], "rumble", "AT THE WINDOW")
b("shepherd", "That drum isn't yours, lantern-bearer. Give it to me.", "close:shepherd", [("shepherd", "shake")], "alarm", "GIVE IT TO ME")
b("wren", "Odo, don't give him the drum! It's the only thing he's afraid of!", "prop:pdark", [("pdark", "bounce"), ("odo", "jump")], "crunch", "HE'S AFRAID OF IT")
b("odo", "Wren? Where are you? Wren!", "close:odo", [("odo", "to:-1,11,0"), ("moth", "jump")], None, "WHERE ARE YOU?")
b("narr", "Then the drum began to play by itself. Faster. And faster.", "prop:drum", [("drum", "spin"), ("drum", "bounce"), ("dog", "turn:odo")], "alarm", "FASTER...")
b("narr", "What do you think happens in the next part? Tell me in the comments.", "close:odo", [("odo", "shake"), ("moth", "eyes_big")], "horn", "WHAT HAPPENS NEXT?")
out = {"title": "Ep 34 · 1662: Who Beat the Drum at Night?", "description": base["description"], "lead_in": 0.05,
       "set": {"place": "village", "fog": 0.05, "eyes": 3, "moonlight": 10}, "chars": ch, "props": props, "beats": B}
json.dump(out, open(os.path.join(H, "ep034.json"), "w"), indent=1, ensure_ascii=False)
print(len(B), "beats", sum(len(x["say"].split()) for x in B), "words")

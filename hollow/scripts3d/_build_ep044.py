"""Build scripts3d/ep044.json - the vanished camp of Angikuni Lake (then Northwest Territories, today Nunavut, Canada),
reported by Emmett E. Kelleher in Nov 1930 (trapper Joe Labelle: 6 tents, ~25 people gone, food over the fire, a half-sewn
garment with the needle in it, a rifle left behind); RCMP Sgt J. Nelson (The Pas) called it a hoax in Jan 1931 (old RCMP photo,
Labelle worked elsewhere); revived by Frank Edwards' Stranger than Science (1959); later versions grew (1,000+ people, lights in
the sky). Standalone recorded mystery / newspaper legend. python3 scripts3d/_build_ep044.py"""
import json
H = lambda name, voice, sp, pi, col, home, size=0.85, kind="human", **kw: dict(name=name, voice=voice, speed=sp, pitch=pi, color=col, kind=kind, size=size, home=home, **kw)
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.92, "pitch": -1},
 "labelle": H("Joe Labelle", "am_michael", 0.98, -1, [0.35, 0.18, 0.1], [-3.2, 8.4], 0.88),
 "kelleher": H("Emmett Kelleher", "am_adam", 1.04, 0, [0.18, 0.2, 0.3], [-30, 32], 0.84),
 "nelson": H("Sergeant Nelson", "bm_lewis", 0.96, -1, [0.55, 0.08, 0.08], [-34, 34], 0.9),
 "edwards": H("Frank Edwards", "bm_daniel", 1.0, -1, [0.22, 0.22, 0.24], [-38, 40], 0.86),
 "boy": H("A young trapper", "am_puck", 1.04, 1, [0.25, 0.3, 0.2], [-42, 44], 0.7),
}
P = lambda t, i, col, sc, at, vis=True, glow=0: dict(type=t, id=i, color=col, glow=glow, visible=vis, scale=sc, at=at)
props = [
 P("cone", "tent1", [0.22, 0.19, 0.16], 1.5, [-4.5, 14.5, 0], True, 0),
 P("cone", "tent2", [0.25, 0.21, 0.17], 1.7, [2.5, 15.5, 0], True, 0),
 P("cone", "tent3", [0.2, 0.18, 0.15], 1.4, [6.5, 18, 0], True, 0),
 P("cone", "fire", [1.0, 0.45, 0.08], 0.4, [0.6, 11.2, 0], True, 5),
 P("ball", "pot", [0.12, 0.12, 0.13], 0.35, [0.6, 11.2, 0.8], False, 0),
 P("box", "shirt", [0.75, 0.68, 0.55], 0.5, [-0.6, 12.8, 0.3], False, 0),
 P("cone", "needle", [0.85, 0.9, 1.0], 0.12, [-0.4, 12.5, 0.7], False, 3),
 P("box", "rifle", [0.25, 0.16, 0.08], 0.35, [-3.4, 13.0, 0.6], False, 0),
 P("box", "paper", [0.85, 0.83, 0.75], 0.55, [-1.2, 9.4, 1.3], False, 1),
 P("box", "photo", [0.55, 0.52, 0.45], 0.4, [1.2, 9.6, 1.4], False, 1),
 P("box", "book", [0.5, 0.12, 0.1], 0.45, [-1.0, 9.2, 1.4], False, 1),
 P("ball", "light", [0.7, 1.0, 0.8], 0.6, [3, 30, 9], False, 8),
 P("ball", "moon", [0.8, 0.85, 1.0], 1.6, [10, 40, 14], True, 4),
]
B = []
def b(who, say, cam, do, sfx, text): B.append(dict(who=who, say=say, cam=cam, do=do, sfx=sfx, text=text))
# 0-5 s: hook on frame 1 - he is already walking into the empty camp
b("labelle", "Hello? Is anyone here? The fire is still burning, and the whole camp is empty!", "close:labelle", [["labelle", "to:-1.2,9.8,0"], ["fire", "spin"], ["labelle", "eyes_big"]], "alarm", "THE WHOLE CAMP IS GONE")
b("narr", "Six tents. Twenty-five men, women and children. And not one of them answered.", "prop:tent2", [["tent1", "bounce"], ["tent2", "bounce"], ["tent3", "bounce"]], "dun", "25 PEOPLE GONE")
b("narr", "This story was printed in the newspapers as true, in November nineteen thirty.", "wide", [["moon", "bounce"], ["labelle", "to_home"]], "horn", "NOVEMBER 1930")
b("narr", "Angikuni Lake, far in the frozen north of Canada. Today it is part of Nunavut.", "wide", [["tent3", "bounce"]], "whoosh", "ANGIKUNI LAKE, CANADA")
b("narr", "The trapper was called Joe Labelle. He said he had stayed in this camp before.", "close:labelle", [["labelle", "turn:front"]], "chime", "JOE LABELLE")
b("labelle", "Good people live here. Always a warm fire and a hot meal for a tired trapper.", "close:labelle", [["labelle", "happy"]], "pop", "A WARM WELCOME")
b("narr", "But that night, no dogs barked. No children came running out to meet him.", "prop:tent1", [["labelle", "to:-4.2,10.2,0"], ["tent1", "shake"]], "suspicious", "NO DOGS BARKING")
b("labelle", "Hello! It's Joe! Joe Labelle!", "close:labelle", [["labelle", "jump"], ["labelle", "eyes_big"]], "alarm", "HELLO?")
b("narr", "Only the wind answered. He pulled back the flap of the first tent.", "prop:tent1", [["tent1", "bounce"]], "rumble", "ONLY THE WIND")
b("narr", "A pot of food still hung over the fire pit. Nobody had eaten it.", "prop:pot", [["pot", "show"], ["pot", "bounce"], ["fire", "spin"]], "dun", "FOOD ON THE FIRE")
b("labelle", "They left their supper? Nobody leaves good food out here. Not in winter.", "close:labelle", [["labelle", "eyes_big"]], "suspicious", "THEY LEFT THEIR SUPPER")
b("narr", "Nearby lay a half-sewn piece of clothing. The needle was still stuck in it.", "prop:shirt", [["shirt", "show"], ["needle", "show"], ["needle", "spin"]], "crunch", "THE NEEDLE WAS STILL IN IT")
b("narr", "Someone had put down her sewing, and simply never come back for it.", "prop:needle", [["needle", "bounce"], ["shirt", "bounce"]], "dun", "NEVER CAME BACK")
b("narr", "A rifle stood by a tent door. Out here, a hunter does not leave his rifle.", "prop:rifle", [["rifle", "show"], ["rifle", "bounce"]], "alarm", "HE LEFT HIS RIFLE")
b("labelle", "Where did they go? Twenty-five people cannot just vanish!", "close:labelle", [["labelle", "shake"]], "rumble", "WHERE DID THEY GO?")
b("narr", "He searched along the shore of the lake. He found no sign of where they went.", "wide", [["labelle", "to:4,12.5,0"], ["labelle", "turn:front"]], "whoosh", "NO SIGN")
b("narr", "Joe Labelle hurried south to tell people. And the newspapers loved his story.", "prop:paper", [["labelle", "to_home"], ["paper", "show"], ["paper", "spin"]], "horn", "THE NEWSPAPERS")
b("narr", "If you like true mysteries like this one, subscribe. Because the story was not finished.", "wide", [["moon", "bounce"], ["paper", "hide"]], "pop", "SUBSCRIBE")
b("narr", "A reporter named Emmett Kelleher wrote it up. A whole village had vanished, he said.", "close:kelleher", [["kelleher", "to:-1.6,9.2,0"], ["kelleher", "turn:front"]], "dun", "VANISHED!")
b("kelleher", "Twenty-five people, gone without a trace! The North has a new mystery!", "close:kelleher", [["kelleher", "happy"], ["paper", "show"], ["paper", "bounce"]], "alarm", "GONE WITHOUT A TRACE")
b("narr", "Papers as far away as Virginia printed it. Readers were frightened and fascinated.", "prop:paper", [["paper", "spin"], ["kelleher", "to_home"]], "whoosh", "PRINTED FAR AWAY")
b("narr", "Then the Royal Canadian Mounted Police began to ask questions.", "close:nelson", [["paper", "hide"], ["nelson", "to:-1.4,9.4,0"], ["nelson", "turn:front"]], "rumble", "THE MOUNTIES")
b("narr", "Sergeant Nelson, at The Pas in Manitoba, looked into the story.", "close:nelson", [["nelson", "eyes_big"]], "suspicious", "SERGEANT NELSON")
b("nelson", "That photograph in the paper. I know it. It is an old one, from our own files.", "prop:photo", [["photo", "show"], ["photo", "spin"]], "crunch", "AN OLD PHOTO")
b("narr", "Nobody in the north had heard of a missing camp. Not trappers. Not missionaries.", "wide", [["photo", "hide"], ["tent2", "bounce"]], "dun", "NOBODY HAD HEARD")
b("nelson", "And Joe Labelle does not even work in that area. This story is a hoax.", "close:nelson", [["nelson", "shake"]], "alarm", "A HOAX?")
b("narr", "In January nineteen thirty-one, his report said the whole thing was made up.", "prop:paper", [["paper", "show"], ["paper", "shake"]], "dun", "JANUARY 1931")
b("narr", "Then, in nineteen fifty-nine, a radio man named Frank Edwards put it in a book.", "close:edwards", [["paper", "hide"], ["nelson", "to_home"], ["edwards", "to:-1.5,9.4,0"], ["edwards", "turn:front"], ["book", "show"]], "horn", "1959: THE BOOK")
b("edwards", "Stranger than Science! A whole village, vanished without a trace!", "close:edwards", [["edwards", "happy"], ["book", "spin"]], "alarm", "STRANGER THAN SCIENCE")
b("narr", "With every retelling, the story grew. Some later books said a thousand people were gone.", "wide", [["book", "hide"], ["tent1", "bounce"], ["tent2", "bounce"], ["tent3", "bounce"]], "whoosh", "THE STORY GREW")
b("narr", "Others added strange glowing lights in the sky above the lake.", "prop:light", [["light", "show"], ["light", "spin"], ["edwards", "to_home"]], "rumble", "LIGHTS IN THE SKY?")
b("narr", "Today the Mounted Police call it a legend. They say there is no evidence it ever happened.", "wide", [["light", "hide"], ["moon", "bounce"]], "dun", "JUST A LEGEND?")
b("narr", "But the old newspaper story is real. And Joe Labelle was a real man. So what did he see?", "prop:paper", [["paper", "show"], ["paper", "bounce"]], "suspicious", "WHAT DID HE SEE?")
b("narr", "A camp that simply moved on? A tall tale told by a lonely fire? Nobody knows for sure.", "wide", [["paper", "hide"], ["fire", "spin"]], "dun", "NOBODY KNOWS")
b("narr", "So remember the rule of Angikuni. If a camp is silent, do not step inside.", "prop:tent2", [["tent2", "shake"]], "alarm", "DON'T STEP INSIDE")
b("narr", "Tonight, a young trapper is crossing the same frozen land. He sees six tents.", "close:boy", [["boy", "to:-2,9,0"], ["boy", "turn:front"], ["pot", "hide"]], "rumble", "TONIGHT...")
b("boy", "Tents, and a fire! Thank goodness. Hello? Can I come in and get warm?", "close:boy", [["boy", "happy"], ["boy", "jump"]], "suspicious", "CAN I COME IN?")
b("narr", "Nobody answers. Then, from inside the dark tent, something softly calls his name.", "prop:tent1", [["tent1", "shake"], ["boy", "eyes_big"]], "alarm", "IT CALLS HIS NAME")
b("narr", "What do you think happens next? Tell me in the comments.", "close:boy", [["boy", "shake"]], "dun", "WHAT HAPPENS NEXT?")
d = {"title": "25 People Vanished. Can You Explain It?",
     "description": "A newspaper mystery from 1930: the empty camp at Angikuni Lake, northern Canada. What do you think happens next? Tell me in the comments.",
     "lead_in": 0.0, "set": {"place": "tundra", "fog": 0.035, "eyes": 0, "moonlight": 5}, "chars": chars, "props": props, "beats": B}
json.dump(d, open("scripts3d/ep044.json", "w"), indent=1, ensure_ascii=False)
print(len(B), "beats,", sum(len(x["say"].split()) for x in B), "words")

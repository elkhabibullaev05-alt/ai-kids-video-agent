"""Build scripts3d/ep041.json — the tomb of Squire Richard Cabell, Buckfastleigh, Devon (died 5 July 1677)."""
import json
H = lambda name, voice, sp, pi, col, home, size=0.85, kind="human": dict(name=name, voice=voice, speed=sp, pitch=pi, color=col, kind=kind, size=size, home=home)
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.92, "pitch": -1},
 "boy": H("A village boy", "am_echo", 1.05, 1, [0.3, 0.24, 0.16], [-3.0, 8.6], 0.7),
 "friend": H("His friend", "af_sarah", 1.05, 1, [0.25, 0.3, 0.4], [-6.0, 9.4], 0.68),
 "squire": H("Squire Richard Cabell", "bm_daniel", 0.9, -3, [0.06, 0.05, 0.07], [-30, 34], 0.95),
 "parson": H("A villager", "am_michael", 0.95, -1, [0.28, 0.22, 0.16], [-30, 30], 0.85),
 "hound1": H("Hound", "am_onyx", 0.8, -5, [0, 0, 0], [-34, 40], 0.9, "gloamhound"),
 "hound2": H("Hound", "am_onyx", 0.8, -5, [0, 0, 0], [-38, 42], 0.8, "gloamhound"),
 "hound3": H("Hound", "am_onyx", 0.8, -5, [0, 0, 0], [-42, 44], 0.85, "gloamhound"),
}
P = lambda t, i, col, sc, at, vis=True, glow=0: dict(type=t, id=i, color=col, glow=glow, visible=vis, scale=sc, at=at)
props = [
 P("box", "tomb", [0.32, 0.31, 0.3], 2.6, [2.2, 11.5, 0]),
 P("box", "door", [0.16, 0.1, 0.06], 0.9, [2.2, 10.1, 0.4]),
 P("ball", "keyhole", [1.0, 0.75, 0.35], 0.07, [2.2, 9.6, 1.1], True, 3),
 P("box", "stone", [0.4, 0.4, 0.38], 1.2, [-5, 12, 0], False),
 P("box", "book", [0.5, 0.12, 0.1], 0.45, [-3.5, 8.5, 1.4], False, 1),
 P("cone", "lamp", [1.0, 0.8, 0.45], 0.18, [0.3, 9.9, 2.4], True, 4),
 P("ball", "moon", [0.8, 0.85, 1.0], 1.6, [10, 40, 14], True, 4),
]
B = []
def b(who, say, cam, do, sfx, text): B.append(dict(who=who, say=say, cam=cam, do=do, sfx=sfx, text=text))
# cold open: the dare, mid-tension
b("boy", "Eleven. Twelve. Thirteen times round the tomb. Now the finger in the keyhole.", "two:boy,friend", [["boy", "to:0.8,9.3,0"], ["keyhole", "bounce"]], "alarm", "DON'T TOUCH THE KEYHOLE")
b("friend", "Don't do it! They say the Squire bites!", "close:friend", [["friend", "shake"], ["friend", "eyes_big"]], "suspicious", "THE SQUIRE BITES")
b("narr", "Behind that iron door lies a man the whole town was afraid of. Even after he died.", "prop:tomb", [["tomb", "bounce"], ["lamp", "spin"]], "dun", "LOCKED IN HIS TOMB")
b("narr", "This is a true legend, from a real churchyard. Buckfastleigh, Devon, England.", "wide", [["moon", "bounce"], ["boy", "to_home"]], "horn", "DEVON, ENGLAND")
b("narr", "The tomb on this hill belongs to Squire Richard Cabell, of Brook Manor.", "prop:tomb", [["door", "bounce"]], "chime", "SQUIRE RICHARD CABELL")
b("narr", "In the sixteen hundreds he owned land all across the south of Dartmoor.", "close:squire", [["squire", "to:-1,10.5,0"], ["squire", "turn:front"]], "whoosh", "THE 1600s")
b("narr", "He loved one thing more than anything. Hunting on the moor, with his pack of hounds.", "two:squire,hound1", [["hound1", "to:3,12,0"], ["hound2", "to:5,13.5,0"], ["squire", "turn:hound1"]], "rumble", "HIS HOUNDS")
b("squire", "Faster, my hounds! Nobody on this moor escapes me.", "close:squire", [["squire", "laugh"], ["hound1", "jump"]], "alarm", "NOBODY ESCAPES")
b("narr", "People whispered that he was cruel. Some even said he sold his soul to the Devil.", "close:squire", [["squire", "eyes_big"], ["lamp", "spin"]], "suspicious", "HE SOLD HIS SOUL?")
b("parson", "Shut the doors at night. The Squire is out riding again.", "close:parson", [["parson", "to:-5,10,0"], ["parson", "shake"]], "dun", "SHUT THE DOORS")
b("narr", "Then, on the fifth of July, sixteen seventy-seven, Richard Cabell died.", "wide", [["squire", "sad"], ["hound1", "to_home"], ["hound2", "to_home"]], "horn", "5 JULY 1677")
b("narr", "And that is when the strange part began.", "prop:tomb", [["squire", "to_home"], ["tomb", "spin"]], "whoosh", "THEN IT BEGAN")
b("narr", "The night he was buried, a pack of black hounds came racing across the moor.", "wide", [["hound1", "to:-2,13,0"], ["hound2", "to:5.5,14,0"], ["hound3", "to:-6,15,0"]], "rumble", "BLACK HOUNDS CAME")
b("narr", "Nobody owned them. Nobody knew where they came from. Their eyes burned red.", "close:hound1", [["hound1", "turn:front"], ["hound1", "eyes_big"]], "alarm", "EYES OF FIRE")
b("parson", "Listen! They're howling at his grave!", "close:parson", [["parson", "eyes_big"], ["parson", "turn:hound1"]], "suspicious", "HOWLING AT HIS GRAVE")
b("narr", "All night long they circled the churchyard, howling. Round and round the grave.", "two:hound2,hound3", [["hound2", "to:6,9,0"], ["hound3", "to:-2,9.5,0"], ["hound1", "spin"]], "rumble", "ROUND AND ROUND")
b("narr", "If you love true legends like this, subscribe now. It gets stranger.", "wide", [["moon", "bounce"]], "pop", "SUBSCRIBE")
b("narr", "The people of Buckfastleigh were terrified he would not stay in his grave.", "close:parson", [["parson", "shake"]], "dun", "HE WON'T STAY DOWN")
b("narr", "So they buried him deep, and laid a heavy stone on top of him.", "prop:stone", [["stone", "show"], ["stone", "bounce"]], "crunch", "A HEAVY STONE")
b("narr", "Then they built a little stone house over the grave. With iron bars on the windows.", "prop:tomb", [["stone", "hide"], ["tomb", "bounce"], ["door", "bounce"]], "whoosh", "IRON BARS")
b("parson", "There. Locked in. Now he can never get out.", "prop:door", [["parson", "to:-0.5,9.6,0"], ["parson", "happy"]], "chime", "LOCKED IN")
b("narr", "But the stories say it did not work.", "close:parson", [["parson", "turn:front"], ["lamp", "spin"]], "dun", "IT DID NOT WORK")
b("narr", "On the night he died, every year, the Squire rides out again, leading his phantom pack.", "two:squire,hound1", [["squire", "to:-3,13,0"], ["hound1", "to:0,14,0"], ["hound2", "to:3,15,0"]], "rumble", "HE RIDES AGAIN")
b("squire", "Out, my hounds. Out onto the moor.", "close:squire", [["squire", "turn:front"], ["hound3", "jump"]], "alarm", "OUT ONTO THE MOOR")
b("narr", "And when the pack is not hunting, people say it waits around his tomb, howling.", "prop:tomb", [["squire", "to_home"], ["hound1", "to:0,9,0"], ["hound2", "to:5,10,0"]], "suspicious", "THEY WAIT AT THE TOMB")
b("narr", "Over two hundred years later, in nineteen-oh-one, a famous writer came to Dartmoor.", "wide", [["hound1", "to_home"], ["hound2", "to_home"], ["hound3", "to_home"], ["book", "show"]], "horn", "1901")
b("narr", "Arthur Conan Doyle heard the legends of the Squire and his black dogs.", "prop:book", [["book", "spin"]], "chime", "ARTHUR CONAN DOYLE")
b("narr", "Soon he wrote one of the most famous mysteries ever. The Hound of the Baskervilles.", "prop:book", [["book", "bounce"]], "whoosh", "THE HOUND")
b("narr", "And the children of Buckfastleigh had a dare of their own.", "two:boy,friend", [["book", "hide"], ["boy", "to:-1.5,8.8,0"]], "suspicious", "THE DARE")
b("narr", "Walk round the tomb thirteen times. Then put your finger in the keyhole.", "prop:keyhole", [["keyhole", "bounce"], ["boy", "to:0.8,9.3,0"]], "dun", "13 TIMES ROUND")
b("narr", "Some say seven times. And the Squire, or the Devil, will bite your finger.", "close:boy", [["boy", "eyes_big"]], "alarm", "HE WILL BITE")
b("narr", "In nineteen ninety-two, a fire burned the old church to a shell. The tomb still stands.", "prop:tomb", [["lamp", "spin"], ["tomb", "shake"]], "rumble", "THE TOMB STILL STANDS")
b("narr", "So here is the rule of Buckfastleigh. Never walk round Cabell's tomb thirteen times.", "prop:tomb", [["door", "bounce"]], "dun", "NEVER WALK ROUND IT")
b("narr", "Tonight, the boy has already walked round twelve times.", "two:boy,friend", [["boy", "to:4.2,9.6,0"], ["friend", "to:-2,9.2,0"]], "whoosh", "TWELVE TIMES")
b("friend", "Stop! Can't you hear that? Something is howling on the moor!", "close:friend", [["friend", "shake"], ["hound1", "to:-6,16,0"], ["hound2", "to:7,17,0"]], "alarm", "SOMETHING IS HOWLING")
b("boy", "Thirteen. It's just an old story.", "close:boy", [["boy", "to:0.8,9.3,0"], ["boy", "happy"]], "suspicious", "THIRTEEN")
b("narr", "He slides his finger into the keyhole. Inside the tomb, something moves.", "prop:keyhole", [["keyhole", "spin"], ["door", "shake"], ["tomb", "shake"]], "dun", "SOMETHING MOVES")
b("squire", "Who woke me?", "close:squire", [["squire", "to:4.5,10.4,0"], ["squire", "turn:boy"], ["boy", "eyes_big"]], "alarm", "WHO WOKE ME?")
b("narr", "What do you think happens next? Tell me in the comments.", "two:boy,squire", [["hound1", "to:0,12,0"], ["boy", "shake"], ["squire", "turn:front"]], "horn", "WHAT HAPPENS NEXT?")
sc = dict(title="Never Walk Round This Tomb 13 Times (Ep 41)",
          description="A true legend from Buckfastleigh, Devon: the tomb of Squire Richard Cabell (1677) and his phantom hounds. What do you think happens next? Tell me in the comments.",
          lead_in=0.0, set={"place": "graveyard", "fog": 0.03, "eyes": 6, "moonlight": 20}, chars=chars, props=props, beats=B)
json.dump(sc, open(__file__.replace("_build_ep041.py", "ep041.json"), "w"), indent=1)
print(len(B), "beats", len(sc["title"]), "title chars")

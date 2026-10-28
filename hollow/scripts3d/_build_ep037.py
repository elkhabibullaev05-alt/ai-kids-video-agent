# builds scripts3d/ep037.json (run from hollow/) — The Hairy Hands of Dartmoor (standalone story, no serial references)
# Sources: en.wikipedia.org/wiki/Hairy_Hands ; skeptic.org.uk (2022, Daily Mail 14 Oct 1921 clipping, Theo Brown) ;
#          wearesouthdevon.com/dartmoors-hairy-hands-evolving-myth ; bitesizedbritain.co.uk (26 Aug 1921 army captain)
import json
src = json.load(open('scripts3d/ep036.json'))
ch = {'narr': src['chars']['narr']}
def H(name, voice, pitch, col, home, size=0.85):
    return {"name": name, "voice": voice, "speed": 0.95, "pitch": pitch, "color": col, "kind": "human", "size": size, "home": home}
ch['driver'] = H("The driver", "am_michael", 0, [0.3, 0.22, 0.14], [5.5, 7.5])
ch['car'] = {"name": "Car", "voice": "am_eric", "speed": 1.0, "pitch": 0, "color": [0.08, 0.1, 0.09], "kind": "car", "size": 1.0, "home": [1.5, 11]}
ch['hands'] = {"name": "The Hairy Hands", "voice": "bm_daniel", "speed": 0.8, "pitch": -4, "color": [0.2, 0.13, 0.09], "kind": "hands", "size": 1.1, "home": [1.5, 8.2], "up": True}
ch['doctor'] = H("A prison doctor", "am_eric", 0, [0.15, 0.15, 0.2], [-30, 30], 0.85)
ch['captain'] = H("An army captain", "am_adam", -1, [0.25, 0.28, 0.16], [-30, 32], 0.9)
ch['woman'] = H("A woman in a caravan", "bf_emma", 0, [0.35, 0.12, 0.1], [-30, 34], 0.8)
P = lambda t, i, c, at, sc, vis=False, glow=0: {"type": t, "id": i, "color": c, "glow": glow, "visible": vis, "scale": sc, "at": at}
props = [P("box", "caravan", [0.5, 0.46, 0.38], [-7, 16, 0], 3.0, False, 0),
         P("box", "window", [0.95, 0.62, 0.3], [-7, 14.0, 1.6], 0.8, False, 1.2),
         P("box", "paper", [0.9, 0.88, 0.8], [-3.5, 8.5, 1.4], 0.45, False, 1),
         P("star", "cross", [0.95, 0.9, 0.7], [-7, 13.2, 2.6], 0.45, False, 5),
         P("ball", "moon", [0.8, 0.85, 1.0], [10, 40, 14], 1.6, True, 4)]
B = []
def b(who, say, cam, do=(), sfx=None, text=None):
    x = {"who": who, "say": say, "cam": cam, "do": [list(d) for d in do]}
    if sfx: x["sfx"] = sfx
    if text: x["text"] = text
    B.append(x)
# cold open: the scariest moment first (motion + big text on frame 1)
b("narr", "Two hairy hands just grabbed your steering wheel. And they will not let go.", "close:hands", [("hands", "shake"), ("car", "shake")], "alarm", "LET GO OF THE WHEEL")
b("driver", "That's not my hand! Something is pulling the wheel!", "close:driver", [("driver", "shake"), ("driver", "eyes_big")], "dun", "NOT MY HAND!")
b("narr", "This is a real legend from a lonely road on Dartmoor, in Devon, England.", "wide", [("car", "shake"), ("moon", "bounce")], "horn", "DARTMOOR, ENGLAND")
b("narr", "The stretch between Postbridge and Two Bridges. Today it is called the B3212.", "close:car", [("car", "turn:front")], "engine", "THE B3212")
b("narr", "From around nineteen ten, drivers and riders had strange accidents here.", "wide", [("hands", "dive"), ("car", "shake")], "rumble", "SINCE 1910")
b("narr", "Their cars jerked to the side. As if someone else had taken control.", "close:car", [("car", "shake")], "crunch", "SOMEONE ELSE STEERED")
b("driver", "It's the road. It has to be the road. Right?", "close:driver", [("driver", "turn:car")], "suspicious", "JUST THE ROAD?")
b("narr", "June, nineteen twenty-one. A doctor from Dartmoor Prison rode this road on his motorcycle.", "close:doctor", [("doctor", "to:-4,8,0"), ("doctor", "turn:front")], "engine", "JUNE 1921")
b("narr", "Two children sat in the sidecar. He knew this road very well.", "close:doctor", [("doctor", "turn:car")], "suspicious", "TWO CHILDREN")
b("doctor", "Hold on tight. Something is wrong with the handlebars!", "close:doctor", [("doctor", "shake")], "alarm", "SOMETHING IS WRONG")
b("narr", "Suddenly the motorcycle swerved and left the road. The children were thrown clear.", "wide", [("doctor", "exit"), ("car", "shake")], "crunch", "IT SWERVED")
b("narr", "No one could say why. The road was straight. The night was calm.", "close:car", [("moon", "bounce")], "rumble", "NO REASON")
b("narr", "And then, in August that year, an army captain came forward.", "close:captain", [("captain", "to:-4,8,0"), ("captain", "turn:front")], "horn", "AUGUST 1921")
b("captain", "A pair of hairy hands closed over mine. They pushed me off the road!", "close:captain", [("captain", "shake"), ("hands", "rise")], "alarm", "HAIRY HANDS")
b("narr", "He said he fought them with all his strength. The hands were stronger.", "close:hands", [("hands", "shake")], "crunch", "THEY WERE STRONGER")
b("narr", "London papers printed the story. In October, one wrote of three curious accidents since March.", "prop:paper", [("paper", "show"), ("paper", "spin"), ("captain", "exit")], "pop", "3 ACCIDENTS")
b("narr", "Now the whole country knew the name. The Hairy Hands of Dartmoor.", "close:hands", [("paper", "hide"), ("hands", "shake")], "rumble", "THE HAIRY HANDS")
b("narr", "If you like true stories that have no answer, subscribe now. The worst part is next.", "wide", [("hands", "dive")], "pop", "SUBSCRIBE")
b("narr", "Nineteen twenty-four. A couple slept in a caravan on the moor, near that road.", "wide", [("caravan", "show"), ("window", "show"), ("woman", "to:-7,12.3,0")], "suspicious", "1924: A CARAVAN")
b("narr", "The woman woke up in the night. Something was moving on the window.", "prop:window", [("window", "bounce")], "dun", "SOMETHING ON THE GLASS")
b("woman", "A hand. A huge hairy hand, crawling up the glass.", "close:woman", [("woman", "eyes_big"), ("woman", "shake"), ("hands", "to:-5.6,12.9,0")], "alarm", "CRAWLING UP THE GLASS")
b("narr", "She said it wanted to get in. She felt it meant harm.", "prop:window", [("window", "spin")], "rumble", "IT WANTED IN")
b("narr", "She made the sign of the cross and prayed. And the hand was gone.", "prop:cross", [("cross", "show"), ("cross", "bounce"), ("hands", "dive")], "chime", "THEN IT WAS GONE")
b("narr", "That woman was the mother of Theo Brown, a well known folklore writer.", "close:woman", [("woman", "sad")], "suspicious", "A FOLKLORIST'S MOTHER")
b("narr", "Theo wrote it down decades later, in her book Devon Ghosts.", "close:woman", [("cross", "hide"), ("window", "hide")], "pop", "DEVON GHOSTS")
b("driver", "So the hands don't only grab steering wheels. They come to the window too?", "close:driver", [("driver", "shake"), ("woman", "exit"), ("caravan", "hide"), ("hands", "to:1.5,8.2,0")], "alarm", "THEY CAME TO THE WINDOW")
b("narr", "So what is really out there? People have argued for a hundred years.", "wide", [("car", "turn:front")], "rumble", "100 YEARS")
b("narr", "Engineers pointed at the road. Its steep camber tilted fast cars toward the edge.", "close:car", [("car", "shake")], "engine", "A TILTED ROAD")
b("narr", "Skeptics say the caravan hand was a dream, between sleep and waking.", "close:driver", [("driver", "sleep")], "suspicious", "A WAKING DREAM?")
b("narr", "Others say an old spirit of the moor guards this road. Nobody knows whose hands they are.", "close:hands", [("hands", "rise"), ("hands", "shake")], "alarm", "WHOSE HANDS?")
b("driver", "I'll drive slowly. Both hands on the wheel. My hands.", "close:driver", [("driver", "to:4.5,8,0"), ("driver", "turn:car")], "engine", "BOTH HANDS ON THE WHEEL")
b("narr", "So here is the rule of the B3212. Never take your hands off the wheel.", "close:car", [("hands", "dive")], "crunch", "NEVER LET GO")
b("narr", "The driver set off across the moor. The fog came down. The road went quiet.", "wide", [("car", "shake"), ("moon", "bounce")], "whoosh", "THE FOG CAME DOWN")
b("driver", "Okay. Postbridge is behind me. Nearly there. Nothing happened.", "close:driver", [("driver", "happy")], "suspicious", "NEARLY THERE")
b("narr", "Then the wheel went cold. Colder than ice.", "close:car", [("car", "shake")], "dun", "THE WHEEL WENT COLD")
b("driver", "Wait. I'm holding the wheel with both hands. So whose hands are these?", "close:driver", [("driver", "eyes_big"), ("hands", "rise")], "alarm", "WHOSE HANDS ARE THESE?")
b("narr", "Because there were four hands on that wheel. And only two of them were the driver's.", "close:hands", [("hands", "shake"), ("car", "shake")], "rumble", "FOUR HANDS")
b("narr", "What do you think happens next? Tell me in the comments.", "two:driver,hands", [("driver", "shake"), ("hands", "shake")], "horn", "WHAT HAPPENS NEXT?")
s = {"title": "Who Grabbed the Wheel on This Road? (Ep 37)",
     "description": "A real Dartmoor legend: the Hairy Hands of the B3212. What do you think happens next? Tell me in the comments.",
     "lead_in": 0.0, "set": {"place": "moor", "fog": 0.05, "eyes": 0, "moonlight": 12}, "chars": ch, "props": props, "beats": B}
json.dump(s, open('scripts3d/ep037.json', 'w'), indent=1, ensure_ascii=False)
print(len(B), sum(len(x['say'].split()) for x in B), len(s['title']), max(len(x['say'].split()) for x in B))

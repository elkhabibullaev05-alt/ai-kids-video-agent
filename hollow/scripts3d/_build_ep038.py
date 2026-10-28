# builds scripts3d/ep038.json (run from hollow/) — The Jewel House ghost, Tower of London, October 1817 (standalone story)
# Sources: strangehistory.net/2015/07/15/the-cylinder-monster-1-the-witness-account (Swifte, Notes and Queries 1860) ;
#          hrp.org.uk/blog/the-jewel-house-keepers-ghost (Historic Royal Palaces: Gregory 1851, sentry + bear, Hereford Journal 1789) ;
#          en.wikipedia.org/wiki/Edmund_Lenthal_Swifte
import json
src = json.load(open('scripts3d/ep037.json'))
ch = {'narr': src['chars']['narr']}
def H(name, voice, pitch, col, home, size=0.85):
    return {"name": name, "voice": voice, "speed": 0.95, "pitch": pitch, "color": col, "kind": "human", "size": size, "home": home}
ch['swifte'] = H("Edmund Swifte", "bm_lewis", -1, [0.16, 0.13, 0.12], [-3.2, 8.2], 0.9)
ch['wife'] = H("His wife", "bf_emma", 0, [0.35, 0.12, 0.16], [3.2, 8.2], 0.8)
ch['sentry'] = H("The sentry", "am_adam", 0, [0.45, 0.07, 0.06], [-30, 32], 0.9)
ch['bear'] = {"name": "The shape", "voice": "bm_daniel", "speed": 0.8, "pitch": -4, "color": [0.12, 0.08, 0.05], "kind": "gloamhound", "size": 1.0, "home": [-30, 36]}
P = lambda t, i, c, at, sc, vis=False, glow=0: {"type": t, "id": i, "color": c, "glow": glow, "visible": vis, "scale": sc, "at": at}
props = [P("box", "table", [0.22, 0.14, 0.08], [0, 9.5, 0], 2.2, True, 0),
         P("tube", "tube", [0.55, 0.78, 1.0], [0, 9.5, 3.4], 1.0, True, 1.4),
         P("cone", "candle", [1.0, 0.85, 0.5], [-0.8, 9.2, 1.4], 0.35, True, 4),
         P("box", "chair", [0.3, 0.2, 0.1], [-3.2, 6.8, 0], 0.8, False, 0),
         P("box", "door", [0.25, 0.18, 0.1], [-6, 12, 0], 2.4, False, 0),
         P("box", "paper", [0.9, 0.88, 0.8], [3.5, 8.5, 1.4], 0.45, False, 1),
         P("ball", "moon", [0.8, 0.85, 1.0], [10, 40, 14], 1.6, True, 4)]
B = []
def b(who, say, cam, do=(), sfx=None, text=None):
    x = {"who": who, "say": say, "cam": cam, "do": [list(d) for d in do]}
    if sfx: x["sfx"] = sfx
    if text: x["text"] = text
    B.append(x)
# cold open: the scariest moment first (motion + big text on frame 1)
b("wife", "Oh, it has seized me! Something has seized me!", "close:wife", [("wife", "shake"), ("tube", "to:3.2,8.6,3.0")], "alarm", "IT SEIZED ME")
b("narr", "A glowing glass tube is floating over a dinner table. And it just stopped behind her.", "prop:tube", [("tube", "spin"), ("wife", "eyes_big")], "dun", "WHAT IS THAT?")
b("narr", "This is a true account, from inside the Tower of London. October, eighteen seventeen.", "wide", [("moon", "bounce"), ("tube", "to:0,9.5,3.4")], "horn", "TOWER OF LONDON, 1817")
b("narr", "The man at the table was Edmund Swifte, Keeper of the Crown Jewels.", "close:swifte", [("swifte", "turn:front")], "suspicious", "KEEPER OF THE JEWELS")
b("swifte", "A quiet Saturday supper. My wife, our little boy, her sister. Nothing more.", "close:swifte", [("swifte", "happy")], "chime", "A QUIET SUPPER")
b("narr", "They ate in the Jewel House, in the old Martin Tower. The doors were shut.", "wide", [("candle", "bounce")], "rumble", "THE DOORS WERE SHUT")
b("narr", "Near midnight, his wife lifted a glass of wine and water to her lips.", "close:wife", [("wife", "turn:front")], "suspicious", "NEAR MIDNIGHT")
b("wife", "Good God! What is that?", "close:wife", [("wife", "eyes_big"), ("wife", "shake")], "alarm", "WHAT IS THAT?")
b("narr", "Above the table hung a shape like a glass tube. As thick as a man's arm.", "prop:tube", [("tube", "bounce")], "dun", "A GLASS TUBE")
b("narr", "Inside it, a thick liquid swirled. White and pale blue, turning and turning.", "prop:tube", [("tube", "spin")], "whoosh", "WHITE AND PALE BLUE")
b("swifte", "It hung there two minutes. Between the ceiling and the table.", "close:swifte", [("swifte", "turn:wife")], "rumble", "2 MINUTES")
b("narr", "Then it began to move. Slowly, around the edge of the table.", "wide", [("tube", "to:2,7.5,3.2")], "whoosh", "THEN IT MOVED")
b("narr", "It passed the sister. It passed the little boy. It passed Swifte himself.", "close:swifte", [("tube", "to:-3.2,8.6,3.2"), ("swifte", "shake")], "dun", "IT PASSED HIM")
b("narr", "Then it glided behind his wife, and stopped over her right shoulder.", "close:wife", [("tube", "to:3.2,8.8,3.0"), ("wife", "eyes_big")], "alarm", "OVER HER SHOULDER")
b("wife", "It has seized me! Edmund, it has seized me!", "close:wife", [("wife", "shake")], "alarm", "IT HAS SEIZED ME!")
b("narr", "Swifte grabbed his chair and swung it hard at the thing behind her.", "close:swifte", [("chair", "show"), ("chair", "to:3,8.8,2.2"), ("swifte", "to:1.5,8,0")], "crunch", "HE SWUNG THE CHAIR")
b("narr", "The chair struck the wooden wall. The shape slid away, toward the window.", "prop:tube", [("chair", "hide"), ("tube", "to:0,13,3.4")], "whoosh", "TOWARD THE WINDOW")
b("narr", "And then it was gone. Only two of the four had seen it.", "wide", [("tube", "hide"), ("swifte", "to_home")], "pop", "ONLY 2 SAW IT")
b("narr", "If you love true stories with no answer, subscribe now. The worst part is next.", "wide", [("candle", "bounce")], "pop", "SUBSCRIBE")
b("narr", "Because that same night, a guard stood alone outside the Jewel Office door.", "close:sentry", [("sentry", "to:-4.5,10.5,0"), ("door", "show"), ("sentry", "turn:front")], "suspicious", "THE SAME NIGHT")
b("sentry", "Quiet watch. Nobody gets past this door. Nobody.", "close:sentry", [("sentry", "turn:front")], "engine", "NOBODY GETS PAST")
b("narr", "Then something came out from under the door. Something large and dark.", "prop:door", [("bear", "to:-6,10.6,0"), ("door", "bounce")], "rumble", "UNDER THE DOOR")
b("sentry", "A bear? A bear, loose in the Tower?", "close:sentry", [("sentry", "eyes_big"), ("bear", "rise")], "alarm", "A BEAR?")
b("narr", "It stood up on its hind legs, like a bear. And it came toward him.", "close:bear", [("bear", "rise"), ("bear", "shake")], "crunch", "IT STOOD UP")
b("narr", "The guard thrust his bayonet at it. The blade went through, and stuck in the door.", "prop:door", [("sentry", "shake"), ("door", "bounce")], "crunch", "STUCK IN THE DOOR")
b("narr", "The shape was gone. The guard fell to the floor in shock.", "close:sentry", [("bear", "exit"), ("sentry", "sleep")], "dun", "HE FELL")
b("narr", "Another guard swore he was not asleep, and not drunk. Records say he never recovered.", "close:sentry", [("sentry", "sad")], "rumble", "NOT ASLEEP. NOT DRUNK.")
b("swifte", "I saw that guard the next day. He was shaking. He had seen something.", "close:swifte", [("swifte", "sad"), ("sentry", "exit")], "suspicious", "HE SAW SOMETHING")
b("narr", "Swifte kept quiet for over forty years. In eighteen sixty, he finally wrote it all down.", "prop:paper", [("paper", "show"), ("paper", "spin"), ("door", "hide")], "pop", "43 YEARS LATER")
b("narr", "He was a lawyer and a careful man. He said he could not explain it.", "close:swifte", [("paper", "hide")], "suspicious", "NO EXPLANATION")
b("narr", "Skeptics say candle smoke, or a trick of the light on the glass.", "wide", [("candle", "bounce")], "whoosh", "A TRICK OF LIGHT?")
b("narr", "But a trick of light does not grab a woman. And it does not leave a bayonet in a door.", "close:wife", [("wife", "shake")], "alarm", "IT GRABBED HER")
b("narr", "So here is the rule of the Jewel House. Never sit with your back to the window.", "wide", [("wife", "turn:swifte")], "dun", "NEVER TURN YOUR BACK")
b("narr", "Years later, a new family sat down to supper in that same room.", "wide", [("swifte", "exit"), ("candle", "bounce")], "chime", "YEARS LATER")
b("wife", "It's only a story, dear. Pass the bread. Nothing ever happens here.", "close:wife", [("wife", "happy")], "suspicious", "ONLY A STORY")
b("narr", "Then the candle flickered. And the air above the table began to swirl.", "prop:tube", [("tube", "show"), ("tube", "spin")], "whoosh", "THE AIR SWIRLED")
b("wife", "Who is standing behind my chair?", "close:wife", [("wife", "eyes_big"), ("tube", "to:3.2,8.8,3.0"), ("bear", "to:5.5,10,0")], "alarm", "WHO IS BEHIND ME?")
b("narr", "Behind her, something white and blue was waiting. And something dark stood up beside it.", "two:wife,bear", [("bear", "rise"), ("tube", "spin")], "rumble", "IT'S BACK")
b("narr", "What do you think happens next? Tell me in the comments.", "two:wife,bear", [("wife", "shake"), ("bear", "shake")], "horn", "WHAT HAPPENS NEXT?")
s = {"title": "What Floated Over Her Dinner Table? (Ep 38)",
     "description": "A true account from the Tower of London, 1817: the Jewel House ghost. What do you think happens next? Tell me in the comments.",
     "lead_in": 0.0, "set": {"place": "village", "fog": 0.05, "eyes": 0, "moonlight": 12}, "chars": ch, "props": props, "beats": B}
json.dump(s, open('scripts3d/ep038.json', 'w'), indent=1, ensure_ascii=False)
print(len(B), sum(len(x['say'].split()) for x in B), len(s['title']), max(len(x['say'].split()) for x in B))

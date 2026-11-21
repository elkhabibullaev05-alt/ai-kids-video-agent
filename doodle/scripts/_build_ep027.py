"""ep027 — What If You Could See Who Misses You?  (queue refill 2026-11-21: cloud/queue/doodle was empty)
First-person What If story, 12-16 min (AGENT.md "WHAT IF" format, owner 2026-11-14).
Writes the worker job to cloud/queue/doodle/ep027.json.  Run: python3 doodle/scripts/_build_ep027.py
"""
import json, os, random

random.seed(27)
CH = {  # speaker -> (voice, guy look)
    "nora": ("af_bella", {"extras": ["bun"], "shirt": "purple"}),
    "dad": ("am_adam", {"extras": ["glasses"], "shirt": "grey"}),
    "grandpa": ("bm_george", {"extras": ["cap"], "shirt": "brown"}),
    "marcus": (None, {"extras": ["hair"], "shirt": "green"}),  # no lines of his own, narrator tells his part
}
ME = {"extras": ["hair"], "shirt": "blue"}
BGS = {"room": "navy", "home": "sky", "school": "yellow", "grandpa": "green", "road": "tan", "river": "teal",
       "drama": "purple", "bad": "dark"}
SETS = {
    "room": [{"prop": "desk", "x": 260, "y": 900, "s": 0.85}, {"prop": "laptop", "x": 1700, "y": 780, "s": 0.7}],
    "home": [{"prop": "coffee", "x": 250, "y": 860, "s": 0.9}, {"prop": "calendar", "x": 1690, "y": 300, "s": 0.75}],
    "school": [{"prop": "chalkboard", "x": 300, "y": 640, "s": 0.9}, {"prop": "backpack", "x": 1720, "y": 900, "s": 0.8}],
    "grandpa": [{"prop": "house", "x": 230, "y": 900, "s": 0.9}, {"prop": "sun", "x": 1680, "y": 200, "s": 0.7}],
    "road": [{"prop": "car", "x": 300, "y": 900, "s": 0.9}, {"prop": "sign", "x": 1700, "y": 900, "s": 0.8}],
    "river": [{"prop": "lake", "x": 1550, "y": 900, "s": 0.9}, {"prop": "cloud", "x": 350, "y": 200, "s": 0.8}],
    "drama": [],
    "bad": [],
}
CAMS = [((960, 540, 1.0), (960, 540, 1.07)), ((930, 540, 1.07), (990, 530, 1.0)), ((990, 550, 1.0), (930, 525, 1.06)),
        ((960, 565, 1.13), (960, 540, 1.0)), ((890, 540, 1.0), (1030, 540, 1.05))]
FACES = {"sad", "shock", "happy", "angry", "worried", "confused", "grin", "neutral", "cry", "tired", "smug", "scream"}
POSES = ["stand", "point", "shrug", "hips", "think", "wave", "present", "hold"]

scenes = []
place = "room"
chapter = None


def guy(who, face="neutral", pose=None, x=1150, look=-1, s=1.0, at=0, label=None):
    if face not in FACES:
        face = "neutral"
    g = dict(ME if who == "me" else CH[who][1])
    g.update(pose=pose or random.choice(POSES), face=face, look=look)
    if label:
        g["label"] = label
    return {"guy": g, "x": x, "y": 900, "s": s, "at": at}


def num(a, b, x=1150, y=320, at=0.35, size=130, dur=1.6, color="blue", anim=None):
    """the ability: a glowing blue 'times missed' counter above a head"""
    d = {"count": [a, b], "fmt": "{:,.0f}", "x": x, "y": y, "size": size, "color": color, "outline": "white",
         "dur": dur, "at": at}
    if anim:
        d["anim"] = anim
    return d


def sc(say, items, who=None, cam=None, **kw):
    d = {"say": say, "items": [dict(i) for i in SETS[place]] + list(items), "bg": BGS[place], "whoosh": False}
    a, b = cam or random.choice(CAMS)
    d["cam"] = {"from": list(a), "to": list(b)}
    if who and who in CH and CH[who][0]:
        d["voice"] = CH[who][0]
    if chapter:
        d["chapter"] = chapter
    d.update(kw)
    scenes.append(d)


def talk(who, line, face="neutral", other=None, extra=(), pose=None):
    """a character speaks: speaker right (or left if it's me), optional listener opposite"""
    it = [guy(who, face, pose=pose, x=1150 if who != "me" else 760, look=-1 if who != "me" else 1)]
    if other:
        it.append(guy(other[0], other[1], x=650 if who != "me" else 1250, look=1 if who != "me" else -1, at=0.15))
    it += list(extra)
    sc(line, it, who=who)


def call(who, line, face="neutral", extra=(), narr=False):
    """a video call: the other person inside a phone-screen frame, me holding the phone (narr=True: narrator speaks)"""
    it = [{"box": [930, 150, 820, 780], "color": "white", "at": 0},
          {"text": "VIDEO CALL", "x": 1340, "y": 200, "size": 44, "color": "grey", "at": 0},
          guy(who, face, x=1340, look=-1, s=0.85), guy("me", "neutral", pose="hold", x=480, look=1, at=0.1)]
    sc(line, it + list(extra), who=None if narr else who)


def text_msg(line, msg, who=None, color="white", tcolor="dark"):
    """a text message on screen"""
    sc(line, [{"prop": "phone", "x": 420, "y": 820, "s": 1.6},
              {"box": [760, 330, 1000, 260], "color": color, "at": 0.1},
              {"text": msg, "x": 1260, "y": 470, "size": 58, "color": tcolor, "at": 0.25}], who=who)


def say(line, *items, cam=None, **kw):
    sc(line, list(items), cam=cam, **kw)


def banner(big, line, color="red"):
    sc(line, [{"box": [210, 330, 1500, 300], "color": color, "at": 0},
              {"text": big, "x": 960, "y": 480, "size": 96, "color": "white", "at": 0}], whoosh=True)


def fact(line, big, color="yellow"):
    sc(line, [{"box": [360, 250, 1200, 380], "color": "dark", "at": 0},
              {"text": big, "x": 960, "y": 440, "size": 120, "color": color, "at": 0.15}], whoosh=True)


def me(line, face="neutral", *extra, pose=None):
    if ":" in face:  # "face:pose" shorthand
        face, pose = face.split(":")
    sc(line, [guy("me", face, pose=pose, x=960, look=1)] + list(extra))


def big(word, color="blue", y=300, at=0.4, size=110, x=960):
    return {"text": word, "x": x, "y": y, "size": size, "color": color, "outline": "white", "at": at}


# =============== COLD OPEN (dialogue at 0 s, number appears ~25 s) ===============
place = "room"
call("nora", "Leo, I'm so sorry, I have to run. Practice. We'll talk tomorrow, okay?", "worried")
talk("me", "Yeah. Sure. Tomorrow.", "sad", pose="hold")
call("nora", "Don't do the sad voice, Leo. I mean it this time. Tomorrow, for real. Pinky promise.", "smug")
say("Tomorrow. That's what she said last Tuesday. And the Tuesday before that. I was about to toss my phone onto the bed.",
    guy("me", "tired", pose="hold", x=760, look=1), {"prop": "phone", "x": 1250, "y": 760, "s": 1.4, "anim": "shake"},
    {"text": "TOMORROW?", "x": 1250, "y": 330, "size": 90, "color": "white", "at": 0.4})
call("nora", "Then, right above Nora's frozen face on my screen, a blue number faded in. Two hundred and twelve.", "neutral",
     [num(0, 212, x=1340, y=320, at=0.45, size=140, anim="pulse"), {"ring": [1340, 320, 130], "at": 0.8}], narr=True)
say("It glowed like a sticker someone had stuck on the glass. I rubbed the screen with my sleeve. It didn't move.",
    {"prop": "phone", "x": 960, "y": 820, "s": 2.4}, num(212, 212, x=960, y=420, at=0, size=150, anim="pulse"),
    guy("me", "shock", pose="panic", x=400, look=1, at=0.3))
me("I'm Leo. I'm seventeen. Four months ago, Dad and I moved six hundred miles away for his new job.", "neutral",
   {"text": "600 MILES", "x": 960, "y": 250, "size": 110, "color": "yellow", "outline": "dark", "at": 0.5},
   {"arrow": [[300, 560], [1620, 560]], "color": "yellow", "at": 0.3})
me("And I was pretty sure everyone back home had already forgotten me.", "sad",
   {"text": "FORGOTTEN?", "x": 960, "y": 280, "size": 110, "color": "white", "outline": "dark", "at": 0.4})

# =============== DAY 1 ===============
chapter = "Day 1"
place = "home"
talk("dad", "Morning, champ. Eggs or cereal? I'm making eggs either way.", "happy", ("me", "tired"))
say("Dad was at the stove in his work vest, humming. Above his head, nothing. No number. Just the kitchen light.",
    guy("dad", "happy", x=1100, pose="hold"), {"text": "?", "x": 1100, "y": 320, "size": 140, "color": "grey", "at": 0.5},
    guy("me", "confused", x=600, look=1, at=0.1))
me("So it wasn't everybody. Or my brain had finally melted from too much screen time.", "confused:think",
   {"prop": "phone", "x": 1450, "y": 700, "s": 0.9, "at": 0.3})
place = "school"
say("At school I tested it. Hallway. Cafeteria. Gym. Hundreds of heads. Not one single number.",
    guy("marcus", "neutral", x=420), guy("nora", "neutral", x=820), guy("dad", "neutral", x=1220),
    guy("grandpa", "neutral", x=1600), {"cross": [960, 420, 340], "at": 0.7})
say("Which honestly made sense. Four months is not long. Most of these people didn't know my last name.",
    guy("me", "neutral", x=960, look=1), {"text": "NEW KID", "x": 960, "y": 290, "size": 100, "color": "red", "outline": "white", "at": 0.4})
fact("There's a researcher in Kansas, Jeffrey Hall, who measured this. It takes around fifty hours together to turn a stranger into a casual friend.",
     "50 HOURS")
fact("About ninety hours to become actual friends. More than two hundred for a close friend. I'd spent maybe three hours talking to anyone here.",
     "200+ HOURS", "orange")
say("Except Marcus. My lab partner. Quiet. Draws robots on everything, including our actual lab report.",
    guy("marcus", "neutral", x=1150, pose="type"), guy("me", "neutral", x=650, look=1),
    {"prop": "robot", "x": 1500, "y": 700, "s": 0.8, "at": 0.5})
say("No number over Marcus either. Of course not. You can't miss somebody you've known for two weeks.",
    guy("marcus", "neutral", x=1150), {"text": "0", "x": 1150, "y": 320, "size": 120, "color": "grey", "at": 0.5})
place = "room"
say("That night I ran an experiment. I texted Nora one word. Hey.",
    guy("me", "think", x=600, look=1), {"prop": "phone", "x": 1200, "y": 760, "s": 1.5},
    {"text": "hey", "x": 1200, "y": 400, "size": 90, "color": "white", "at": 0.5})
text_msg("Thirty seconds later. Hey you! Crazy week, call Sunday? And next to her contact photo, the number ticked up.",
         "Hey you! Call Sunday?")
say("Two hundred and thirteen.", {"prop": "phone", "x": 960, "y": 820, "s": 2.2},
    num(212, 213, x=960, y=380, at=0.1, size=170, dur=0.6, anim="pulse"))
me("She'd missed me. Just now. Again. While typing a message that sounded like she barely had time for me.", "confused",
   pose="think")
place = "drama"
banner("THE RULE", "So here was the rule, as far as I could tell. The number shows how many times someone has missed you since you were last together.",
       "navy")
say("Not liked. Not thought about. Missed. That exact ache when you turn to tell someone something, and they're not there.",
    guy("nora", "sad", x=600, pose="point", look=1), {"box": [1000, 600, 320, 300], "color": "grey", "at": 0.4},
    {"text": "...", "x": 1160, "y": 520, "size": 120, "color": "white", "at": 0.6})
place = "room"
me("Two hundred and thirteen times. In four months. I sat on my floor and did the math. Almost twice a day.", "shock",
   big("~2 / DAY", "yellow", 260, 0.5, 120))

# =============== WEEK 1 ===============
chapter = "Week 1"
place = "home"
talk("dad", "Your grandpa called again. Pick up next time, okay? He likes hearing your voice.", "worried", ("me", "neutral"),
     [{"prop": "phone", "x": 1450, "y": 740, "s": 0.9, "at": 0.3}])
talk("me", "He calls every Sunday, Dad. He's just bored. He'll talk about tomatoes for an hour.", "tired", ("dad", "sad"))
say("That's what I said. But Sunday came, the phone buzzed, and Grandpa Walt's face filled the screen.",
    {"prop": "phone", "x": 960, "y": 800, "s": 2.0, "anim": "shake"},
    {"text": "GRANDPA", "x": 960, "y": 280, "size": 100, "color": "green", "outline": "white", "at": 0.4})
place = "room"
call("grandpa", "There he is! The famous Leo! I was starting to think you'd run off and joined the circus.", "grin")
call("grandpa", "And above his head, the number was so big I had to tilt the phone. One thousand and forty.", "happy",
     [num(0, 1040, x=1340, y=320, at=0.4, size=130, dur=2.2, anim="pulse")], narr=True)
me("One thousand and forty. In four months. Grandpa was missing me more than eight times a day.", "shock:panic",
   big("1,040", "blue", 280, 0.3, 150))
call("grandpa", "Oh, I'm fine. Busy, busy. Tomatoes, the crossword, the usual. Don't you worry about an old man.", "grin",
     [num(1040, 1040, x=1340, y=320, at=0, size=110)])
call("grandpa", "And while he said busy, busy, the number went up. One thousand forty-one. Forty-two.", "neutral",
     [num(1040, 1042, x=1340, y=320, at=0.3, size=120, dur=2.0, anim="pulse")], narr=True)
say("Grandpa has lived alone since Grandma passed. Before we moved, I stopped by his place every single day after school.",
    guy("grandpa", "neutral", x=1150, pose="stand"), guy("me", "happy", x=650, look=1, at=0.2),
    {"prop": "house", "x": 1550, "y": 900, "s": 0.8, "at": 0.1})
say("I never once wondered what happened at three-thirty, when nobody knocked anymore.",
    {"prop": "house", "x": 960, "y": 900, "s": 1.3}, {"text": "3:30", "x": 960, "y": 300, "size": 130, "color": "white", "outline": "dark", "at": 0.3},
    {"text": "no knock", "x": 1400, "y": 500, "size": 60, "color": "grey", "at": 0.7})
fact("The US Surgeon General put out a warning about this in 2023. About half of American adults say they feel lonely.",
     "1 IN 2")
fact("The same report said a lack of connection can hurt your health about as much as smoking up to fifteen cigarettes a day.",
     "= 15 / DAY", "red")
call("grandpa", "I swallowed and said the only thing I could think of. Grandpa, tell me about the tomatoes.", "confused", narr=True)
call("grandpa", "Really? Well. You are not going to believe what the big one did this week.", "grin",
     [{"text": "THE BIG ONE", "x": 1340, "y": 320, "size": 60, "color": "red", "at": 0.5}])
say("We talked for an hour and ten minutes. And the whole time, the number didn't move. Not once.",
    {"prop": "stopwatch", "x": 600, "y": 700, "s": 1.2}, {"text": "1:10:00", "x": 600, "y": 380, "size": 90, "color": "white", "at": 0.3},
    num(1042, 1042, x=1350, y=450, at=0.2, size=140))
me("That's when I got it. While you're with someone, you can't miss them. The counter just pauses.", "think:think",
   big("PAUSED", "green", 280, 0.5, 120))

# =============== WEEK 2 ===============
chapter = "Week 2"
place = "drama"
banner("WEEK 2", "And then, and I'm not proud of this, I started playing with it.", "purple")
place = "room"
me("If being together paused the number, being apart made it grow. So I tested it on Nora.", "smug:think",
   {"arrow": [[1250, 700], [1250, 300]], "color": "blue", "at": 0.5})
say("I stopped replying fast. I left her on read for a day. Then two.",
    {"prop": "phone", "x": 700, "y": 800, "s": 1.6}, {"text": "Read 2 days ago", "x": 1250, "y": 450, "size": 64, "color": "grey", "at": 0.4},
    guy("me", "smug", x=1500, look=-1, at=0.2))
say("Two twenty. Two thirty-one. Two forty-one. Every time I checked, it was higher. And every time, it felt amazing.",
    num(213, 241, x=960, y=380, at=0.05, size=170, dur=4.0, anim="pulse"), guy("me", "grin", pose="fist", x=960, look=1, at=0.6))
me("Somebody, somewhere, needed me. I had proof. A glowing blue number of proof.", "grin:present",
   big("PROOF", "blue", 280, 0.4, 130))
text_msg("Then her message came in.", "Leo? You okay? You went quiet.", who=None)
say("I typed back. Fine, just busy. Busy, busy. Exactly like Grandpa. I didn't even notice I'd borrowed his line.",
    {"prop": "phone", "x": 700, "y": 800, "s": 1.6}, {"text": "fine. busy.", "x": 1250, "y": 450, "size": 80, "color": "white", "at": 0.3},
    {"text": "busy, busy", "x": 1250, "y": 620, "size": 60, "color": "green", "at": 0.7})
place = "school"
say("Meanwhile, Marcus asked if I wanted to join the robotics club after school. I said maybe. I meant no.",
    guy("marcus", "happy", x=1150, pose="present"), guy("me", "neutral", x=650, look=1),
    {"prop": "robot", "x": 1500, "y": 720, "s": 0.8}, {"text": "MAYBE", "x": 650, "y": 320, "size": 90, "color": "grey", "at": 0.6})
me("Why build something new here, when my old life came with numbers on it?", "smug", pose="shrug")
place = "home"
say("At dinner, Dad tried. He always tried.",
    {"prop": "desk", "x": 960, "y": 900, "s": 1.2}, guy("dad", "happy", x=1350), guy("me", "tired", x=570, look=1))
talk("dad", "So. Any friends yet? Anybody you sit with at lunch?", "happy", ("me", "tired"))
talk("me", "Dad. Can I just eat? Please.", "angry", ("dad", "sad"))
say("I took my plate to my room. Headphones on. Door closed. Same as every night since the move.",
    {"box": [700, 300, 520, 600], "color": "brown", "at": 0.3}, {"text": "CLOSED", "x": 960, "y": 560, "size": 80, "color": "white", "at": 0.6},
    guy("dad", "sad", x=1450, at=0.1))

# =============== WEEK 3 — the twist at home ===============
chapter = "Week 3"
place = "drama"
banner("WEEK 3", "Then, one Thursday, something happened that made no sense at all.", "red")
place = "home"
say("I walked into the kitchen for water. Dad was at the table with a pile of bills. And above his head, there was a number.",
    guy("dad", "tired", x=1150, pose="think"), {"prop": "envelope", "x": 1450, "y": 760, "s": 0.8},
    guy("me", "neutral", x=600, look=1, at=0.1))
say("Ninety-six.", guy("dad", "tired", x=960, pose="think"), num(0, 96, x=960, y=320, at=0.05, size=180, dur=1.2, anim="pulse"),
    cam=((960, 430, 1.25), (960, 470, 1.1)))
talk("me", "That's impossible. I see him every day. We live in the same apartment. We share a bathroom!", "shock",
     extra=[big("96", "blue", 300, 0.2, 110, 1300)], pose="panic")
say("I stood there and watched. Ninety-seven. He was looking at a photo on the fridge. Me at eight, on his shoulders, at a baseball game.",
    {"box": [1250, 250, 380, 300], "color": "white", "at": 0.1}, {"prop": "baseball", "x": 1440, "y": 420, "s": 0.7, "at": 0.3},
    guy("dad", "sad", x=800, look=1), num(96, 97, x=800, y=320, at=0.3, size=120, dur=0.8))
talk("dad", "Oh. Hey, bud. Didn't hear you come in. You need something?", "happy", ("me", "shock"),
     [num(97, 97, x=1150, y=320, at=0, size=110)])
talk("me", "No. Just water.", "sad", ("dad", "neutral"))
say("Ninety-eight. I was standing six feet away from him, and he was missing me. Right then. To my face.",
    guy("dad", "sad", x=1250), guy("me", "sad", x=650, look=1), num(97, 98, x=1250, y=320, at=0.2, size=130, dur=0.8),
    {"arrow": [[760, 560], [1140, 560]], "color": "red", "at": 0.5}, {"text": "6 FEET", "x": 950, "y": 480, "size": 60, "color": "red", "at": 0.55})
place = "room"
me("I went back to my room, lay on the bed and stared at the ceiling for a long time.", "sad", pose="stand")
place = "drama"
banner("SAME ROOM", "Turns out you can miss someone who's in the same room. They just have to stop really being there.", "navy")
place = "room"
me("Since the move, I'd been a ghost in my own home. A closed door. A guy who said fine.", "sad",
   big("GHOST", "white", 280, 0.4, 120))
me("The rule was never about miles.", "neutral:think",
   {"text": "600 MILES", "x": 960, "y": 260, "size": 100, "color": "grey", "at": 0.2}, {"cross": [960, 260, 200], "at": 0.6})

# =============== MONTH 1 — the big problem ===============
chapter = "Month 1"
place = "drama"
banner("MONTH 1", "And right when I started to understand that, everything with Nora fell apart.", "red")
place = "room"
say("One night I checked her contact photo, ready for my little dose of being missed. Two hundred and ninety. Okay.",
    {"prop": "phone", "x": 960, "y": 820, "s": 2.2}, num(241, 290, x=960, y=380, at=0.3, size=160, dur=1.4))
say("Next day. Two hundred and ninety.", {"prop": "phone", "x": 960, "y": 820, "s": 2.2}, num(290, 290, x=960, y=380, at=0, size=160),
    {"text": "DAY 2", "x": 1500, "y": 250, "size": 80, "color": "white", "at": 0.2})
say("The day after that. Two hundred and ninety. The number had frozen.",
    {"prop": "phone", "x": 960, "y": 820, "s": 2.2}, num(290, 290, x=960, y=380, at=0, size=160),
    {"stamp": "FROZEN", "x": 1450, "y": 420, "size": 80, "w": 300, "at": 0.6})
talk("me", "No, no, no. Come on. Go up. Go up!", "scream", extra=[{"prop": "phone", "x": 1300, "y": 740, "s": 1.2, "anim": "shake"}],
     pose="panic")
say("A whole week went by. Still two ninety. Nora hadn't missed me once. Not one time in seven days.",
    {"prop": "calendar", "x": 960, "y": 520, "s": 1.6}, {"text": "7 DAYS: 0", "x": 960, "y": 250, "size": 110, "color": "red", "outline": "white", "at": 0.5})
say("I scrolled through our messages. Her side: long paragraphs, photos of our spot by the river, a voice note of her singing our dumb song.",
    {"box": [460, 200, 1000, 640], "color": "white", "at": 0},
    {"text": "Remember this?!", "x": 960, "y": 300, "size": 60, "color": "purple", "at": 0.15},
    {"prop": "lake", "x": 960, "y": 620, "s": 0.9, "at": 0.35},
    {"text": "voice note 0:42", "x": 960, "y": 760, "size": 50, "color": "purple", "at": 0.6})
say("My side. k. lol. busy. Over and over. Like a broken vending machine.",
    {"box": [460, 200, 1000, 640], "color": "white", "at": 0},
    {"text": "k", "x": 960, "y": 320, "size": 70, "color": "grey", "at": 0.1}, {"text": "lol", "x": 960, "y": 450, "size": 70, "color": "grey", "at": 0.3},
    {"text": "busy", "x": 960, "y": 580, "size": 70, "color": "grey", "at": 0.5}, {"text": "k", "x": 960, "y": 710, "size": 70, "color": "grey", "at": 0.7})
me("I'd been so busy watching the number go up that I never asked why it was going up.", "worried", pose="facepalm")
me("It went up because she kept reaching out, and I didn't reach back. I made her miss me on purpose. And it worked. Until she stopped.", "cry",
   big("ON PURPOSE", "red", 260, 0.5, 110))
say("I called her. It rang five times.", {"prop": "phone", "x": 960, "y": 780, "s": 2.0, "anim": "shake"},
    {"text": "RING", "x": 500, "y": 300, "size": 70, "color": "white", "at": 0.1}, {"text": "RING", "x": 1420, "y": 360, "size": 70, "color": "white", "at": 0.35},
    {"text": "RING", "x": 600, "y": 560, "size": 70, "color": "white", "at": 0.6})
call("nora", "Hey. What's up?", "neutral", [num(290, 290, x=1340, y=320, at=0, size=100)])
say("Her voice was flat. Polite. The way you talk to a cashier.",
    guy("nora", "neutral", x=1150, pose="stand"), {"prop": "cart", "x": 650, "y": 900, "s": 0.9},
    {"text": "polite.", "x": 1150, "y": 330, "size": 80, "color": "grey", "at": 0.5})
call("nora", "I asked her if she was mad at me.", "neutral", narr=True)
call("nora", "I'm not mad. I'm just done waiting for you to text back. It's easier if I don't think about you so much.", "sad")
me("There it was. She hadn't forgotten me. She'd made herself stop. Because missing me had started to hurt.", "cry", pose="cry")
call("nora", "I have to go. Really, this time.", "sad")
say("The screen went dark. Two hundred and ninety, just sitting there like a scoreboard after everyone's gone home.",
    {"box": [600, 220, 720, 560], "color": "dark", "at": 0}, num(290, 290, x=960, y=500, at=0.2, size=150),
    {"prop": "scoreboard", "x": 1600, "y": 520, "s": 0.6, "at": 0.6})
place = "bad"
me("That was the worst night since the move. Worse than the first night in our empty apartment.", "cry", pose="stand")
fact("There's an idea from a scientist named Robin Dunbar. Our brains can only keep up with about a hundred and fifty real relationships.",
     "~150")
fact("And the very closest circle is only about five people. Five. I had just pushed one of mine out. On purpose.",
     "TOP 5", "red")

# =============== MONTH 2 — fixing it ===============
chapter = "Month 2"
place = "home"
say("In the morning, I did something I hadn't done in four months. I knocked on Dad's door before he left for work.",
    {"box": [1100, 300, 400, 600], "color": "brown"}, {"text": "KNOCK", "x": 1300, "y": 250, "size": 80, "color": "white", "outline": "dark", "at": 0.5},
    guy("me", "worried", x=700, look=1))
talk("me", "Dad. Can I come with you on Saturday? Wherever. The store. I don't care where.", "worried", ("dad", "shock"))
talk("dad", "You want to come to the hardware store? With me? On purpose?", "shock", ("me", "neutral"),
     [num(99, 99, x=1150, y=320, at=0, size=100)])
talk("me", "Yeah. On purpose.", "happy", ("dad", "happy"))
say("His number stopped at ninety-nine. And for the first time, I saw it do something new. It flickered.",
    guy("dad", "happy", x=960), num(99, 99, x=960, y=320, at=0, size=150, anim="pulse"),
    {"text": "flicker", "x": 1350, "y": 420, "size": 60, "color": "teal", "at": 0.6})
place = "school"
say("Saturday we wandered the hardware store for two hours. Dad explained screws like it was a museum tour. I didn't mind.",
    guy("dad", "grin", x=1150, pose="present"), guy("me", "happy", x=650, look=1),
    {"prop": "pricetag", "x": 1550, "y": 600, "s": 0.8, "text": "SCREWS", "at": 0.3})
say("We got burgers. He told me he'd taken the night shifts so I could stay in the good school district. I never knew.",
    {"prop": "desk", "x": 960, "y": 900, "s": 1.1}, guy("dad", "neutral", x=1350), guy("me", "shock", x=570, look=1),
    {"text": "NIGHT SHIFTS", "x": 960, "y": 300, "size": 90, "color": "navy", "outline": "white", "at": 0.5})
talk("dad", "I figured you hated it here. Hated me a little, too, for dragging you away.", "sad", ("me", "sad"))
talk("me", "I never hated you. I just didn't know how to be the new kid.", "sad", ("dad", "sad"))
place = "home"
say("When we got home, Dad's number had rolled all the way back down. Zero.",
    guy("dad", "happy", x=960), num(99, 0, x=960, y=320, at=0.15, size=170, dur=1.8, color="green"))
me("Zero. The best number I had ever seen. Zero means you're here. Zero means nobody's waiting for you.", "happy",
   big("0", "green", 270, 0.3, 200))
place = "school"
say("On Monday, I told Marcus yes. Robotics club. After school.",
    guy("marcus", "happy", x=1150, pose="fist"), guy("me", "happy", x=650, look=1, pose="wave"),
    {"text": "YES", "x": 650, "y": 320, "size": 100, "color": "green", "at": 0.5})
say("His robot was called Toaster. It could not toast. It could barely turn left. We spent three weeks fixing one wheel.",
    {"prop": "robot", "x": 960, "y": 820, "s": 1.6, "anim": "shake"}, {"text": "TOASTER", "x": 960, "y": 280, "size": 100, "color": "orange", "outline": "white", "at": 0.2},
    {"arrow": [[1250, 700], [1450, 600]], "color": "red", "at": 0.6})
me("Fifty hours to a casual friend, I thought. Only about forty-four to go.", "grin",
   {"count": [50, 44], "fmt": "{:.0f} HRS", "x": 960, "y": 280, "size": 120, "color": "teal", "outline": "white", "dur": 1.4, "at": 0.4})

# =============== MONTH 3 — Grandpa ===============
chapter = "Month 3"
place = "drama"
banner("MONTH 3", "Then Grandpa's number did something that scared me.", "red")
place = "room"
call("grandpa", "Sunday call. He answered late. He looked tired. And the number had jumped. Two thousand and six.", "tired",
     [num(1042, 2006, x=1340, y=320, at=0.4, size=120, dur=2.0, color="red")], narr=True)
me("That's not eight times a day anymore. That's way more. Like he was missing me every hour he was awake.", "worried",
   big("EVERY HOUR", "red", 270, 0.5, 110))
call("grandpa", "Just a little cold, kiddo. Doctor says rest. I'm fine.", "tired")
me("I didn't need a superpower for that one. I knew Grandpa. Fine meant he'd been sitting alone. A lot.", "sad", pose="think")
place = "home"
talk("me", "Dad. Grandpa's birthday is next Saturday.", "worried", ("dad", "neutral"))
talk("dad", "I know. I was going to send him a card.", "neutral", ("me", "worried"), [{"prop": "envelope", "x": 1450, "y": 720, "s": 0.9}])
talk("me", "What if we sent us instead?", "grin", ("dad", "shock"))
say("Dad looked at me for a long second. Then he grabbed his phone and asked his boss for Friday night off.",
    guy("dad", "grin", x=1150, pose="hold"), {"prop": "phone", "x": 1350, "y": 700, "s": 0.8},
    {"text": "FRIDAY: OFF", "x": 1150, "y": 300, "size": 90, "color": "green", "outline": "white", "at": 0.6})

# =============== THE DRIVE ===============
chapter = "The Drive"
place = "road"
say("Nine hours of highway. Gas station snacks. Dad's terrible playlist from the nineties, which I will never admit I sang along to.",
    {"prop": "car", "x": 960, "y": 880, "s": 1.6, "move": [1100, 880]}, {"text": "9 HOURS", "x": 960, "y": 260, "size": 110, "color": "white", "outline": "dark", "at": 0.3},
    {"text": "LA LA LA", "x": 1400, "y": 500, "size": 90, "color": "purple", "at": 0.6, "anim": "bob"})
say("Somewhere around hour six, Dad said I was easier to talk to in the car. Something about not having to look at each other.",
    guy("dad", "happy", x=1150, pose="stand"), guy("me", "neutral", x=750, look=-1),
    {"text": "HOUR 6", "x": 960, "y": 260, "size": 90, "color": "white", "outline": "dark", "at": 0.3})
me("He was right. We talked more on that drive than in four months of dinners.", "happy",
   {"text": "4 MONTHS < 9 HOURS", "x": 960, "y": 280, "size": 80, "color": "dark", "outline": "white", "at": 0.5})
place = "grandpa"
say("We pulled up to Grandpa's house at noon. I could see the tomato plants through the fence. Brown now, for winter.",
    {"prop": "car", "x": 1500, "y": 900, "s": 1.0}, {"text": "HOME", "x": 600, "y": 300, "size": 90, "color": "white", "outline": "dark", "at": 0.5})
say("I knocked our old knock, even though it was noon. Two fast, one slow.",
    {"box": [800, 380, 320, 520], "color": "brown"}, {"text": "KNOCK KNOCK", "x": 700, "y": 300, "size": 70, "color": "dark", "at": 0.2},
    {"text": "...KNOCK", "x": 1350, "y": 300, "size": 70, "color": "dark", "at": 0.6}, guy("me", "worried", x=1400, look=-1))
say("The door opened. Grandpa, in his cardigan. His number said two thousand one hundred and nineteen.",
    guy("grandpa", "shock", x=960, pose="stand"), num(2006, 2119, x=960, y=320, at=0.4, size=140, dur=1.2, color="red"))
talk("grandpa", "Well, I'll be. Is that the circus?", "happy", ("me", "grin"))
say("Then he hugged me, and I watched the number over his shoulder. It rolled down like a slot machine in reverse.",
    guy("grandpa", "cry", x=1020, pose="hold"), guy("me", "happy", x=880, look=1, pose="hold"),
    num(2119, 0, x=960, y=300, at=0.25, size=150, dur=3.0))
say("Zero.", guy("grandpa", "happy", x=960, pose="hold"), big("0", "green", 300, 0.1, 230),
    cam=((960, 450, 1.2), (960, 500, 1.05)))
talk("grandpa", "You didn't have to drive all this way for an old man.", "cry", ("me", "happy"))
talk("me", "I didn't. I drove all this way for my grandpa.", "happy", ("grandpa", "cry"))
say("We stayed four days. I fixed his porch light. He beat me at cards every single night and cheated at least twice.",
    guy("grandpa", "smug", x=1150, pose="hold"), guy("me", "confused", x=650, look=1),
    {"text": "GRANDPA 4 - LEO 0", "x": 960, "y": 280, "size": 80, "color": "dark", "outline": "white", "at": 0.5})
say("Before we left, I set up a video call on his tablet. Every Sunday. Three-thirty. Same time as the old knock.",
    {"prop": "laptop", "x": 960, "y": 800, "s": 1.4}, {"text": "SUNDAY 3:30", "x": 960, "y": 280, "size": 100, "color": "green", "outline": "white", "at": 0.4})

# =============== THE BENCH — Nora ===============
chapter = "The Bench"
place = "river"
me("There was one more person in that town I had to see. And she didn't even know I was there.", "worried", pose="think")
say("The river spot. Our spot. A bench with our initials scratched underneath, where no adult would ever look.",
    {"box": [600, 700, 720, 40], "color": "brown"}, {"box": [640, 740, 30, 160], "color": "brown"}, {"box": [1250, 740, 30, 160], "color": "brown"},
    {"text": "L + N", "x": 960, "y": 640, "size": 70, "color": "dark", "at": 0.5})
text_msg("I texted her. Not lol. Not k. A real message.", "I'm at the bench. Sorry.")
text_msg("I was counting instead of calling. I'll wait as long as you want.", "I'll wait.")
say("Forty minutes. Cold. Wind off the river. I almost left twice.",
    guy("me", "tired", x=960, look=1, pose="hips"), {"count": [0, 40], "fmt": "{:.0f} MIN", "x": 960, "y": 280, "size": 110,
                                                       "color": "white", "outline": "dark", "dur": 2.5, "at": 0.1})
say("Then footsteps on the gravel. Nora. Hands in her pockets. And above her head, the number.",
    guy("nora", "neutral", x=1300, look=-1, pose="stand"), guy("me", "shock", x=650, look=1, at=0.1),
    {"text": "crunch crunch", "x": 1550, "y": 800, "size": 50, "color": "dark", "at": 0.2})
say("Two hundred and ninety-one.", guy("nora", "neutral", x=960, pose="stand"),
    num(290, 291, x=960, y=320, at=0.2, size=180, dur=0.8, anim="pulse"), cam=((960, 430, 1.22), (960, 480, 1.05)))
me("It had moved. One more time. Just now, on the walk over.", "cry", big("+1", "blue", 280, 0.4, 150))
talk("nora", "You're an idiot. You know that, right?", "angry", ("me", "sad"))
talk("me", "Yeah. I know.", "sad", ("nora", "angry"))
talk("nora", "I stopped letting myself miss you, because it felt like I was the only one doing it.", "cry", ("me", "sad"))
talk("me", "You weren't. I just hid it really, really well.", "cry", ("nora", "sad"))
say("She sat down. Nobody said anything for a while. And the number went down, slowly, all the way to zero.",
    guy("nora", "sad", x=1080, pose="stand"), guy("me", "sad", x=840, look=1), num(291, 0, x=1080, y=300, at=0.2, size=130, dur=3.5, color="green"))
talk("nora", "So. How many times did you miss me?", "smug", ("me", "confused"))
say("And here's the thing. I never saw my own number. Not in mirrors. Not in windows. Only other people's.",
    {"box": [760, 220, 400, 620], "color": "sky"}, guy("me", "confused", x=960, look=1), {"text": "?", "x": 960, "y": 300, "size": 140, "color": "grey", "at": 0.5})
talk("me", "I don't know. A lot. More than two hundred ninety-one, probably.", "grin", ("nora", "smug"))
talk("nora", "Probably?", "smug", ("me", "grin"))
talk("me", "Definitely.", "happy", ("nora", "happy"))
say("She laughed. The real laugh, the one that sounds like a happy seal. I had missed that laugh more than I ever told anyone.",
    guy("nora", "happy", x=1150, pose="wave"), guy("me", "happy", x=750, look=1),
    {"text": "HA HA HA", "x": 1150, "y": 320, "size": 80, "color": "purple", "outline": "white", "at": 0.3, "anim": "bob"})

# =============== SPRING ===============
chapter = "Spring"
place = "school"
say("We drove back the next day. Monday, I walked into robotics club. Marcus looked up from Toaster.",
    guy("marcus", "neutral", x=1150, pose="type"), {"prop": "robot", "x": 1500, "y": 760, "s": 0.8}, guy("me", "neutral", x=600, look=1, pose="wave"))
say("And above his head, small and blue and a little shaky, there was a number. One.",
    guy("marcus", "happy", x=960, pose="wave"), num(0, 1, x=960, y=320, at=0.4, size=200, dur=0.6, anim="pulse"),
    cam=((960, 440, 1.2), (960, 500, 1.04)))
me("I'd been gone one week. And somebody in this new town had missed me. Once.", "happy", big("ONCE", "blue", 280, 0.4, 130))
me("One isn't two thousand. But every number starts at one. Even Grandpa's did.", "grin",
   {"text": "1 ... 2,119", "x": 960, "y": 280, "size": 100, "color": "teal", "outline": "white", "at": 0.4})
place = "home"
say("A few weeks later I woke up and the numbers were just gone. Over Dad, on Nora's photo, on Grandpa's Sunday call. Nothing.",
    guy("dad", "happy", x=500), guy("nora", "happy", x=960), guy("grandpa", "happy", x=1420),
    {"cross": [500, 320, 70], "at": 0.3}, {"cross": [960, 320, 70], "at": 0.5}, {"cross": [1420, 320, 70], "at": 0.7})
me("I wasn't even upset. I didn't need them anymore. I knew what to do with the feeling now.", "happy", pose="hips")
place = "drama"
say("Here's what I learned. Missing someone is a message. It's your heart telling you to go knock on a door.",
    {"box": [360, 300, 1200, 360], "color": "dark"},
    {"text": "MISSING SOMEONE", "x": 960, "y": 420, "size": 80, "color": "white", "at": 0.1},
    {"text": "= GO KNOCK", "x": 960, "y": 540, "size": 80, "color": "yellow", "at": 0.5}, whoosh=True)
say("And the people who miss you most are usually the ones saying fine, busy, don't worry about me.",
    guy("grandpa", "neutral", x=500, pose="stand"), guy("dad", "neutral", x=960, pose="stand"), guy("nora", "neutral", x=1420, pose="stand"),
    {"text": "fine", "x": 500, "y": 320, "size": 70, "color": "white", "at": 0.2}, {"text": "busy", "x": 960, "y": 320, "size": 70, "color": "white", "at": 0.4},
    {"text": "I'm okay", "x": 1420, "y": 320, "size": 70, "color": "white", "at": 0.6})
me("They can't see your number either. So tell them.", "happy:point", big("TELL THEM", "yellow", 280, 0.4, 120))
place = "room"
me("If you could see who misses you, whose number would you check first? Tell me in the comments. Then go text them.", "grin",
   {"text": "WHO?", "x": 960, "y": 280, "size": 120, "color": "yellow", "outline": "dark", "at": 0.3},
   num(0, 1, x=1500, y=480, at=0.75, size=110, dur=0.5), pose="point")


# =============== JOB ===============
def est_start(idx):
    """rough voice-time estimate (~2.6 spoken words/s + 0.28 s gap per scene) to place Short 2"""
    return sum(len(s["say"].split()) / 2.6 + 0.28 for s in scenes[:idx])


twist = next(i for i, s in enumerate(scenes) if s["say"] == "Ninety-six.") - 1  # walking into the kitchen
job = {
    "id": "ep027",
    "title": "What If You Could See Who Misses You?",
    "voice": "am_michael",
    "speed": 1.0,
    "hook": "A number showed how many times she missed me",
    "description": ("Leo moved six hundred miles away and was sure everyone back home forgot him. Then a blue number "
                    "appears above people's heads: how many times they've missed him. His best friend, his grandpa, and "
                    "even his dad, who lives in the same apartment. But when Leo starts playing with the numbers, he "
                    "learns what happens when someone stops missing you. An original animated story about distance, "
                    "family and showing up.\n\n"
                    "Facts in this story: Jeffrey Hall (University of Kansas, 2018) estimated it takes about 50 hours "
                    "together to become casual friends, about 90 hours to become friends and more than 200 hours to "
                    "become close friends; the 2023 US Surgeon General advisory on loneliness says about half of US "
                    "adults report feeling lonely, and that a lack of social connection can harm health about as much as "
                    "smoking up to 15 cigarettes a day; and anthropologist Robin Dunbar's research suggests people keep "
                    "about 150 meaningful relationships, with about 5 in the closest circle.\n\n#whatif #story #animation"),
    "tags": ["what if", "what if you could", "who misses you", "see who misses you", "moving away", "long distance friendship",
             "animated story", "2d animation", "story time", "grandpa", "best friend", "life lesson", "the doodle desk"],
    "thumbnail": {"bg": "dark", "text": "GRANDPA|MISSED ME", "size": 160, "color": "yellow",
                  "guy": {"pose": "panic", "face": "shock", "look": -1, "extras": ["hair"], "shirt": "blue"},
                  "guy_x": 1450, "guy_y": 1250, "guy_s": 2.2,
                  "items": [{"text": "1,040", "x": 1450, "y": 170, "size": 200, "color": "sky", "outline": "white"}]},
    "scenes": scenes,
    "shorts": [{"start": 0, "dur": 34, "top": "A number appeared above her head", "title": "A Blue Number Appeared Above My Best Friend's Head"},
               {"start": 317, "dur": 32,  # measured: render.py --check timeline puts the kitchen scene (index `twist`) at 317.0 s
                 "top": "My dad missed me. From 6 feet away.",
                "title": "My Dad Was Missing Me While I Stood Right There"}],
}

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
qdir = os.path.join(root, "cloud", "queue", "doodle")
os.makedirs(qdir, exist_ok=True)
out = os.path.join(qdir, job["id"] + ".json")
json.dump(job, open(out, "w"), indent=1, ensure_ascii=False)
words = sum(len(s["say"].split()) for s in scenes)
print(out, len(scenes), "scenes,", words, "words, ~%.1f min est" % (est_start(len(scenes)) / 60),
      "| short2 start ~%ds" % job["shorts"][1]["start"], "| ability at ~%.0fs" % est_start(4))

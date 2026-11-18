"""ep025 — What If You Could Hear Every Lie?  (watchdog 2026-11-18: doodle queue was empty, channel silent 17 Nov)
First-person What If story, 8-12 min (STYLE.md 2026-11-15 rule). Run: python3 scripts/_build_ep025.py
"""
import json, os, random

random.seed(25)
N = None  # narrator (top-level voice)
CH = {  # speaker -> (voice, guy look)
    "ruby": ("af_bella", {"extras": ["bun"], "shirt": "pink"}),
    "theo": ("am_adam", {"extras": ["cap"], "shirt": "green"}),
    "mom": ("af_nicole", {"extras": ["hair"], "shirt": "teal"}),
    "coach": ("bm_george", {"extras": ["hardhat"], "shirt": "navy"}),
}
ME = {"extras": ["hair"], "shirt": "orange"}
BGS = {"home": "sky", "school": "yellow", "night": "navy", "field": "teal", "drama": "purple", "bad": "dark"}
SETS = {
    "home": [{"prop": "house", "x": 230, "y": 900, "s": 0.9}, {"prop": "coffee", "x": 1700, "y": 860, "s": 0.9}],
    "school": [{"prop": "chalkboard", "x": 300, "y": 640, "s": 0.9}, {"prop": "backpack", "x": 1720, "y": 900, "s": 0.8}],
    "night": [{"prop": "building", "x": 220, "y": 900, "s": 0.9}, {"prop": "cloud", "x": 1600, "y": 220, "s": 0.9}],
    "field": [{"prop": "scoreboard", "x": 1650, "y": 520, "s": 0.8}, {"prop": "football", "x": 300, "y": 880, "s": 0.8}],
    "drama": [{"prop": "desk", "x": 260, "y": 900, "s": 0.85}, {"prop": "clipboard", "x": 1700, "y": 760, "s": 0.8}],
    "bad": [],
}
CAMS = [((960, 540, 1.0), (960, 540, 1.06)), ((940, 540, 1.06), (980, 530, 1.0)), ((980, 550, 1.0), (940, 520, 1.07)),
        ((960, 560, 1.12), (960, 540, 1.0)), ((900, 540, 1.0), (1020, 540, 1.04))]
FACES = {"lie": "smug", "sad": "sad", "shock": "shock", "happy": "happy", "angry": "angry", "worried": "worried",
         "confused": "confused", "grin": "grin", "neutral": "neutral", "cry": "cry", "tired": "tired"}
POSES = ["stand", "point", "shrug", "hips", "think", "wave", "present", "hold", "facepalm"]

scenes = []
place = "home"
chapter = None


def guy(who, face="neutral", pose=None, x=1150, look=-1, label=None, s=1.0, at=0):
    if face not in FACES and pose is None:  # a pose name passed in the face slot ("facepalm", "think", ...)
        pose, face = face, {"facepalm": "tired", "think": "confused"}.get(face, "neutral")
    elif face not in FACES:
        face = "neutral"
    g = dict(ME if who == "me" else CH[who][1])
    g.update(pose=pose or random.choice(POSES), face=FACES.get(face, face), look=look)
    if label:
        g["label"] = label
    return {"guy": g, "x": x, "y": 900, "s": s, "at": at}


def sc(say, items, who=None, cam=None, **kw):
    global chapter
    d = {"say": say, "items": [dict(i) for i in SETS[place]] + items, "bg": BGS[place], "whoosh": False}
    a, b = cam or random.choice(CAMS)
    d["cam"] = {"from": list(a), "to": list(b)}
    if who and who in CH:
        d["voice"] = CH[who][0]
    if chapter:
        d["chapter"] = chapter
    d.update(kw)
    scenes.append(d)


def talk(who, say, face="neutral", other=None, extra=()):
    """a character speaks; the speaker stands right, optional listener left"""
    it = [guy(who, face, x=1150 if who != "me" else 760, look=-1 if who != "me" else 1)]
    if other:
        it.append(guy(other[0], other[1], x=650 if who != "me" else 1250, look=1 if who != "me" else -1, at=0.15))
    it += list(extra)
    sc(say, it, who=who)


def lie(who, say, x=1150, sound="BZZT"):
    """someone lies: red LIE above the head + buzz text"""
    sc(say, [guy(who, "lie", x=x), {"text": "LIE", "x": x, "y": 330, "size": 120, "color": "red", "outline": "white",
                                    "at": 0.45, "anim": "shake"},
             {"text": sound, "x": x + 380, "y": 420, "size": 70, "color": "orange", "at": 0.5}], who=who)


def say(text, *items, cam=None):
    sc(text, list(items), cam=cam)


def banner(text, color="red"):
    sc(text[1], [{"box": [210, 330, 1500, 300], "color": color, "at": 0},
                 {"text": text[0], "x": 960, "y": 480, "size": 96, "color": "white", "at": 0}], whoosh=True)


def fact(text, big, color="yellow"):
    sc(text, [{"box": [360, 250, 1200, 380], "color": "dark", "at": 0},
              {"text": big, "x": 960, "y": 440, "size": 120, "color": color, "at": 0.15}], whoosh=True)


def me(text, face="neutral", *extra):
    sc(text, [guy("me", face, x=960, look=1)] + list(extra))


# ---------------- COLD OPEN (dialogue at 0 s) ----------------
place = "home"
talk("ruby", "I did not take your headphones, Sam. I swear on my life.", "lie", ("me", "angry"))
sc("And that's when I heard it. A buzz, like a fly trapped inside my skull. And one red word above my sister's head.",
   [guy("ruby", "lie", x=1150), guy("me", "shock", x=650, look=1, at=0.1),
    {"text": "LIE", "x": 1150, "y": 330, "size": 130, "color": "red", "outline": "white", "at": 0.5, "anim": "shake"},
    {"text": "BZZZT", "x": 500, "y": 300, "size": 90, "color": "orange", "at": 0.35}])
talk("me", "Ruby. Your bag. Now.", "angry", ("ruby", "worried"))
sc("My headphones were in her bag. Wrapped in a sock. Like that was going to fool anybody.",
   [{"prop": "backpack", "x": 800, "y": 880, "s": 1.3}, {"text": "FOUND", "x": 800, "y": 420, "size": 110, "color": "green", "at": 0.5},
    guy("ruby", "facepalm", x=1300)])
me("My name is Sam. I'm sixteen. And on a normal Tuesday in October, I started hearing every lie anyone told me.", "confused",
   {"text": "DAY 1", "x": 960, "y": 220, "size": 110, "color": "white", "outline": "dark", "at": 0.5})

# ---------------- DAY 1 ----------------
chapter = "Day 1"
talk("mom", "Breakfast is ready, sweetie. And no, I didn't burn the toast.", "lie", ("me", "neutral"),
     [{"text": "LIE", "x": 1150, "y": 330, "size": 110, "color": "red", "outline": "white", "at": 0.6, "anim": "shake"},
      {"prop": "bread", "x": 1500, "y": 760, "s": 1.0, "color": "dark", "at": 0.3}])
say("The toast was black. Fine. That one was harmless. Mom scraped it into the sink and smiled at me like nothing happened.",
    guy("mom", "grin", x=1150), {"prop": "bread", "x": 700, "y": 760, "s": 1.1, "color": "dark"})
place = "school"
say("At school it got loud. Really loud. Every hallway sounded like a beehive.",
    guy("theo", "grin", x=500, pose="wave"), guy("coach", "neutral", x=1000), guy("ruby", "neutral", x=1450),
    {"text": "BZZT", "x": 500, "y": 330, "size": 70, "color": "red", "at": 0.2},
    {"text": "BZZT", "x": 1000, "y": 300, "size": 70, "color": "red", "at": 0.45},
    {"text": "BZZT", "x": 1450, "y": 340, "size": 70, "color": "red", "at": 0.7})
say("I did my homework. Love the haircut. I'm almost there. Five more minutes. Buzz, buzz, buzz, buzz.",
    {"text": "I did my homework", "x": 560, "y": 300, "size": 54, "color": "dark", "at": 0},
    {"text": "Love the haircut", "x": 1360, "y": 420, "size": 54, "color": "dark", "at": 0.25},
    {"text": "I'm almost there", "x": 600, "y": 560, "size": 54, "color": "dark", "at": 0.5},
    {"text": "Five more minutes", "x": 1300, "y": 700, "size": 54, "color": "dark", "at": 0.7},
    {"cross": [960, 500, 360], "at": 0.85})
fact("And here's the weird part. Scientists have actually counted this. In one famous diary study, college students told about two lies a day.",
     "2 LIES / DAY")
fact("Most of them tiny. The kind we tell to be polite. I just never knew how many there were until I could hear them.",
     "TINY LIES", "orange")
talk("theo", "Dude, you look like you've seen a ghost.", "worried", ("me", "shock"))
sc("Theo. My best friend since we were seven. No buzz. Nothing. I almost hugged him for telling me the truth about my face.",
   [guy("theo", "happy", x=1150), guy("me", "happy", x=700, look=1, at=0.1),
    {"text": "TRUTH", "x": 1150, "y": 330, "size": 100, "color": "green", "outline": "white", "at": 0.5}])
talk("me", "Theo, say something false. Anything. Tell me the sky is green.", "grin", ("theo", "confused"))
lie("theo", "Okay. The sky is green.")
me("Buzz. Clear as a fire alarm. It worked on anyone. On purpose, on accident, it didn't matter.", "grin",
   {"prop": "sky" if False else "cloud", "x": 1500, "y": 260, "s": 1.0},
   {"text": "IT'S REAL", "x": 960, "y": 220, "size": 100, "color": "red", "outline": "white", "at": 0.5})

# ---------------- WEEK 1 ----------------
place = "field"
chapter = "Week 1"
banner(("WEEK 1", "By the end of the week I thought I'd won the lottery."), "green")
talk("coach", "Tryouts are fair, boys. I haven't picked anybody yet.", "lie", ("me", "neutral"),
     [{"text": "LIE", "x": 1150, "y": 330, "size": 110, "color": "red", "outline": "white", "at": 0.55, "anim": "shake"},
      {"prop": "clipboard", "x": 1450, "y": 720, "s": 1.0, "at": 0.3}])
say("Coach Brandt had already picked the team. The list was on his clipboard. And I knew it before anyone else did.",
    {"prop": "clipboard", "x": 960, "y": 650, "s": 1.8}, {"text": "TEAM LIST", "x": 960, "y": 260, "size": 90, "color": "dark", "at": 0.3})
place = "school"
say("Card games at lunch? I never lost. Who's bluffing? Buzz. Easy money. Four dollars and a bag of chips.",
    guy("me", "grin", x=700, look=1), {"prop": "dollar", "x": 1200, "y": 700, "s": 1.2, "at": 0.4},
    {"count": [0, 4], "fmt": "${:.0f}", "x": 1200, "y": 400, "size": 120, "color": "money", "at": 0.5, "dur": 1.5})
talk("ruby", "Mom says you have to drive me to the mall.", "lie", ("me", "smug"),
     [{"text": "LIE", "x": 1150, "y": 330, "size": 110, "color": "red", "outline": "white", "at": 0.55, "anim": "shake"}])
talk("me", "No, she didn't. Nice try.", "smug", ("ruby", "shock"))
say("My sister stared at me like I was a witch. Honestly, it felt amazing. For about six days.",
    guy("ruby", "shock", x=1150), guy("me", "smug", x=700, look=1),
    {"text": "WITCH?", "x": 1150, "y": 300, "size": 90, "color": "purple", "at": 0.5})
fact("Because here's the thing nobody tells you. Normal people are terrible at spotting lies. In big lab studies, we guess right only about fifty-four percent of the time.",
     "54%")
fact("That's barely better than flipping a coin. So when you suddenly become one hundred percent right, people stop trusting you.",
     "100%", "red")
say("But I didn't know that yet. I was too busy feeling like a superhero with a really annoying power.",
    guy("me", "grin", x=960, look=1, pose="fist"), {"text": "SUPER?", "x": 960, "y": 300, "size": 110, "color": "gold", "outline": "dark", "at": 0.4})
talk("ruby", "Sam, does this shirt look okay? Be honest.", "worried", ("me", "neutral"))
talk("me", "It looks great.", "grin", ("ruby", "happy"),
     [{"text": "LIE", "x": 760, "y": 330, "size": 110, "color": "red", "outline": "white", "at": 0.55, "anim": "shake"}])
say("Buzz. My own lie, ringing in my ears. Ruby smiled and walked out the door, and I felt weird about it all day.",
    guy("me", "confused", x=960, look=1), {"text": "BZZT", "x": 1400, "y": 380, "size": 90, "color": "red", "at": 0.3})
say("Was that bad? Or was it kind? I honestly couldn't tell anymore. That question would follow me for a year.",
    {"prop": "scale", "x": 960, "y": 800, "s": 1.4}, {"text": "BAD", "x": 700, "y": 420, "size": 80, "color": "red", "at": 0.3},
    {"text": "KIND", "x": 1220, "y": 420, "size": 80, "color": "green", "at": 0.55})

# ---------------- WEEK 2: the problem ----------------
chapter = "Week 2"
place = "drama"
banner(("THE PROBLEM", "And then I started using it. Out loud. On everybody."))
talk("theo", "How did you know Jake was lying about the party? You weren't even there.", "confused", ("me", "worried"))
talk("me", "I just... have a feeling for these things.", "worried", ("theo", "confused"))
sc("Buzz. My own lie. I could hear those too. Right inside my own head, louder than anyone else's.",
   [guy("me", "shock", x=960, look=1), {"text": "LIE", "x": 960, "y": 300, "size": 140, "color": "red", "outline": "white",
                                         "at": 0.3, "anim": "shake"},
    {"text": "BZZZZT", "x": 1500, "y": 420, "size": 90, "color": "orange", "at": 0.4}])
say("I called out a teacher in front of the whole class. She said the test would be easy. Buzz. I said so. Out loud.",
    {"prop": "chalkboard", "x": 960, "y": 560, "s": 1.3}, {"text": "EASY TEST", "x": 960, "y": 500, "size": 80, "color": "white"},
    {"cross": [960, 520, 260], "at": 0.6})
say("The test was not easy. Half the class failed. And somehow, they were mad at me, not at her.",
    {"stamp": "F", "x": 700, "y": 450, "size": 120, "w": 220, "at": 0.3}, {"stamp": "F", "x": 1200, "y": 500, "size": 120, "w": 220, "at": 0.5},
    guy("me", "confused", x=960, look=1))
say("Detention. Two days. Worth it, I thought.",
    {"stamp": "DETENTION", "x": 960, "y": 450, "size": 90, "w": 520, "at": 0.2}, guy("me", "tired", x=600, look=1))
say("I told Priya her boyfriend wasn't really sick on Friday. I told Marcus his cousin didn't really play in college.",
    guy("me", "point", x=700, look=1), guy("ruby", "cry", x=1250),
    {"text": "NOT SICK", "x": 1250, "y": 330, "size": 70, "color": "red", "at": 0.4})
say("Every time I was right. And every time, the room got a little colder around me.",
    guy("me", "neutral", x=960, look=1), {"prop": "thermo", "x": 1500, "y": 760, "s": 1.1, "at": 0.3},
    {"prop": "arrowdown", "x": 1720, "y": 700, "s": 0.9, "color": "blue", "at": 0.6})
place = "school"
talk("theo", "People are calling you the lie detector. Not in a good way, man.", "worried", ("me", "shrug"))
talk("me", "So? I'm helping them. They deserve the truth.", "hips", ("theo", "sad"))
talk("theo", "Do they? Or do you just like being right?", "sad", ("me", "angry"))
say("No buzz. He meant every word. That hurt more than any lie I'd heard all week.",
    guy("theo", "sad", x=1150), guy("me", "sad", x=700, look=1),
    {"text": "TRUTH", "x": 1150, "y": 330, "size": 100, "color": "green", "outline": "white", "at": 0.5})

# ---------------- MONTH 1: the big problem ----------------
chapter = "Month 1"
place = "night"
banner(("MONTH 1", "By November, I was eating lunch alone."), "dark")
say("Nobody wanted to talk to me. Who wants a friend who checks every single word you say?",
    guy("me", "sad", x=960, look=1), {"box": [1300, 700, 300, 40], "color": "brown"},
    {"text": "EMPTY", "x": 1450, "y": 640, "size": 60, "color": "grey", "at": 0.5})
fact("Researchers found something else. Most people tell almost no lies on a normal day. A small group of heavy liars tells most of them.",
     "FEW LIARS", "orange")
say("And that's what I'd forgotten. Most of the buzzes I heard were tiny. Kind. Scared. People protecting each other.",
    guy("mom", "happy", x=500), guy("ruby", "happy", x=960), guy("theo", "happy", x=1420),
    {"text": "KIND", "x": 500, "y": 330, "size": 70, "color": "pink", "at": 0.2},
    {"text": "SCARED", "x": 960, "y": 330, "size": 70, "color": "blue", "at": 0.45},
    {"text": "SHY", "x": 1420, "y": 330, "size": 70, "color": "purple", "at": 0.7})
place = "home"
say("Then one night I heard a lie that I really wasn't ready for.",
    {"prop": "house", "x": 960, "y": 900, "s": 1.4}, {"prop": "cloud", "x": 400, "y": 250, "s": 0.8})
talk("me", "Mom, is everything okay? You've been on the phone a lot.", "worried", ("mom", "tired"))
lie("mom", "Everything's fine, honey. Just work stuff. Go to bed.")
say("Buzz. The loudest one yet. And I couldn't stop thinking about it.",
    guy("me", "worried", x=960, look=1),
    {"text": "BZZZZZT", "x": 960, "y": 320, "size": 130, "color": "red", "outline": "white", "anim": "shake"})
say("For three days I asked questions. Is it money? Buzz-free. No. Is somebody sick? Silence.",
    {"prop": "moneybag", "x": 600, "y": 760, "s": 1.0}, {"cross": [600, 700, 140], "at": 0.3},
    {"prop": "thermo", "x": 1300, "y": 760, "s": 1.0, "at": 0.5}, {"text": "?", "x": 1300, "y": 460, "size": 140, "color": "red", "at": 0.7})
say("I checked her phone. I listened at doors. I turned into exactly the kind of person I hated.",
    {"prop": "phone", "x": 800, "y": 700, "s": 1.3}, guy("me", "worried", x=1300, pose="think"),
    {"prop": "eye", "x": 800, "y": 380, "s": 1.0, "at": 0.5})
banner(("THE TRUTH", "And then I found out. And I wish I'd waited."), "red")
talk("mom", "I lost my job, Sam. Six weeks ago. I didn't want you two to worry over Christmas.", "cry", ("me", "shock"))
say("No buzz. Just the truth. Six weeks of getting dressed every morning and pretending to drive to work. For us.",
    guy("mom", "cry", x=1150), {"prop": "car", "x": 600, "y": 860, "s": 1.0},
    {"count": [0, 6], "fmt": "{:.0f} WEEKS", "x": 960, "y": 300, "size": 100, "color": "white", "at": 0.3, "dur": 2.0})
say("She wasn't lying to hurt me. She was lying to carry something heavy so I didn't have to.",
    guy("mom", "sad", x=1150, pose="hold"), {"prop": "moneybag", "x": 1150, "y": 600, "s": 1.0, "at": 0.4},
    {"text": "PROTECT", "x": 1150, "y": 320, "size": 90, "color": "green", "at": 0.6})
say("And I had spent three days spying on her like she was a criminal. I couldn't even look at her.",
    guy("me", "cry", x=700, look=1, pose="facepalm"), guy("mom", "sad", x=1250),
    {"text": "SPY", "x": 700, "y": 320, "size": 100, "color": "red", "at": 0.5})
talk("me", "You could have told us. We would've helped.", "cry", ("mom", "sad"))
talk("mom", "I know. I'm sorry. I just wanted one more normal month for you.", "cry", ("me", "cry"))
say("Ruby came down the stairs in her pajamas. She'd heard everything. She didn't say a word. She just sat between us.",
    guy("mom", "cry", x=600), guy("ruby", "sad", x=960, look=-1), guy("me", "cry", x=1320),
    {"text": "FAMILY", "x": 960, "y": 300, "size": 100, "color": "pink", "outline": "white", "at": 0.6})
say("That night, for the first time since the buzzing started, the house was completely quiet. No lies at all.",
    {"prop": "house", "x": 960, "y": 900, "s": 1.5}, {"text": "QUIET", "x": 960, "y": 260, "size": 110, "color": "white", "at": 0.5})

# ---------------- MONTH 2: fixing it ----------------
chapter = "Month 2"
place = "school"
banner(("MONTH 2", "So I made a rule. A real one. I wrote it on my hand."), "green")
say("Hear the lie. Ask why. Then shut up.",
    {"box": [460, 330, 1000, 300], "color": "white"},
    {"text": "HEAR. ASK WHY.", "x": 960, "y": 430, "size": 86, "color": "dark", "at": 0.1},
    {"text": "SHUT UP.", "x": 960, "y": 540, "size": 86, "color": "red", "at": 0.5})
talk("me", "Theo, I owe you an apology. A real one. You were right about me.", "sad", ("theo", "neutral"))
talk("theo", "I'm not mad. I'm just tired of being checked like a math test.", "tired", ("me", "sad"))
say("No buzz. I nodded. For the first time in a month I didn't say anything smart back.",
    guy("me", "neutral", x=700, look=1), guy("theo", "neutral", x=1200),
    {"text": "...", "x": 700, "y": 400, "size": 100, "color": "grey", "at": 0.5})
lie("theo", "By the way, I'm totally fine about not making the team.")
say("Buzz. Old me would've said, that's a lie, Theo. New me asked why.",
    guy("me", "think", x=700, look=1), {"text": "WHY?", "x": 700, "y": 330, "size": 110, "color": "green", "at": 0.5},
    guy("theo", "sad", x=1250))
talk("theo", "Because my dad played. And I'm not him. And I didn't want you to see me care.", "sad", ("me", "sad"))
say("We sat on the bleachers until it got dark. That lie wasn't a crime. It was a door. And he finally let me in.",
    {"prop": "scoreboard", "x": 1600, "y": 520, "s": 0.8}, guy("me", "happy", x=700, look=1), guy("theo", "happy", x=1100, look=-1),
    {"prop": "sun", "x": 400, "y": 250, "s": 0.8, "at": 0.4})
place = "home"
say("At home we made a family budget on the fridge. Ruby gave up her phone upgrade without being asked.",
    {"box": [600, 320, 700, 460], "color": "white"}, {"text": "BUDGET", "x": 950, "y": 390, "size": 80, "color": "dark"},
    {"bars": {"values": [5, 3, 2], "labels": ["food", "rent", "fun"], "colors": ["green", "blue", "pink"], "fmt": "{}", "w": 500, "h": 260},
     "x": 950, "y": 740, "at": 0.4})
lie("ruby", "I didn't even want the new phone anyway.", x=1150)
say("Buzz. I didn't say a word. I just gave her my old headphones. The ones from the sock.",
    guy("me", "happy", x=700, look=1, pose="hold"), {"prop": "backpack", "x": 960, "y": 760, "s": 0.8, "at": 0.3},
    guy("ruby", "happy", x=1250), {"text": "GIFT", "x": 960, "y": 450, "size": 90, "color": "pink", "at": 0.6})

# ---------------- YEAR 1 ----------------
chapter = "Year 1"
place = "drama"
banner(("ONE YEAR LATER", "A year later, the buzzing hasn't stopped. But I hear it differently."), "purple")
say("Mom found a new job in March. Better hours. When she told us, there was no buzz at all.",
    guy("mom", "happy", x=1150, pose="present"), {"prop": "building", "x": 500, "y": 900, "s": 0.9},
    {"text": "HIRED", "x": 1150, "y": 320, "size": 100, "color": "green", "outline": "white", "at": 0.5})
say("I still hear about two lies a day from almost everyone. Most are tiny. I'm fine. Love it. On my way.",
    {"text": "I'm fine", "x": 600, "y": 380, "size": 70, "color": "dark", "at": 0},
    {"text": "Love it", "x": 1300, "y": 450, "size": 70, "color": "dark", "at": 0.3},
    {"text": "On my way", "x": 900, "y": 620, "size": 70, "color": "dark", "at": 0.6})
say("But now, when I hear one, I don't ask, is this person bad? I ask, what is this person scared of?",
    guy("me", "think", x=960, look=1), {"text": "SCARED OF?", "x": 960, "y": 300, "size": 100, "color": "blue", "outline": "white", "at": 0.5})
say("Coach Brandt came to me in the spring. He said he'd been unfair at tryouts, and he wanted to fix it. No buzz.",
    guy("coach", "sad", x=1150, pose="shrug"), guy("me", "neutral", x=700, look=1),
    {"text": "SORRY", "x": 1150, "y": 320, "size": 90, "color": "green", "at": 0.5})
say("Theo made the team in the second round. He scored in his first game. I screamed so loud I lost my voice.",
    {"prop": "scoreboard", "x": 960, "y": 520, "s": 1.1}, {"count": [0, 7], "fmt": "{:.0f}", "x": 960, "y": 500, "size": 120, "color": "yellow", "at": 0.3, "dur": 1.5},
    guy("theo", "happy", x=400, pose="fist"), guy("me", "grin", x=1500, pose="fist", look=-1))
say("And the kids who stopped talking to me? Some came back. Some didn't. I said sorry to all of them anyway.",
    guy("me", "neutral", x=960, look=1), guy("ruby", "neutral", x=500), guy("theo", "happy", x=1420),
    {"text": "SORRY", "x": 960, "y": 300, "size": 100, "color": "yellow", "outline": "dark", "at": 0.5})
talk("theo", "Be honest. Do you ever miss being the human lie detector?", "grin", ("me", "smug"))
talk("me", "Nope. Not even a little.", "grin", ("theo", "grin"))
sc("Buzz. Okay. Maybe a little.",
   [guy("me", "grin", x=760, look=1), guy("theo", "happy", x=1250, look=-1),
    {"text": "LIE", "x": 760, "y": 330, "size": 120, "color": "red", "outline": "white", "at": 0.4, "anim": "shake"}])
place = "night"
say("Here's what I learned. The truth matters. But how you use it matters more.",
    {"box": [360, 300, 1200, 360], "color": "dark"},
    {"text": "THE TRUTH MATTERS", "x": 960, "y": 420, "size": 80, "color": "white", "at": 0.1},
    {"text": "HOW YOU USE IT", "x": 960, "y": 540, "size": 80, "color": "yellow", "at": 0.5})
say("A lie can be a wall. But a lot of the time, it's just someone holding something heavy, hoping nobody asks.",
    guy("mom", "neutral", x=500, pose="hold"), guy("theo", "neutral", x=960, pose="hold"), guy("ruby", "neutral", x=1420, pose="hold"),
    {"prop": "moneybag", "x": 500, "y": 600, "s": 0.7, "at": 0.3}, {"prop": "football", "x": 960, "y": 620, "s": 0.7, "at": 0.45},
    {"prop": "phone", "x": 1420, "y": 620, "s": 0.8, "at": 0.6})
say("So now I ask. Gently. And I wait.",
    guy("me", "happy", x=960, look=1), {"text": "ASK. WAIT.", "x": 960, "y": 300, "size": 110, "color": "green", "outline": "white", "at": 0.4})
say("If you could hear every lie, would you want to? Tell me in the comments. And be honest. I'll know.",
    guy("me", "grin", x=960, look=1, pose="point"),
    {"text": "WOULD YOU?", "x": 960, "y": 280, "size": 110, "color": "yellow", "outline": "dark", "at": 0.3},
    {"text": "BZZT", "x": 1500, "y": 500, "size": 70, "color": "red", "at": 0.8})

job = {
    "id": "ep025",
    "title": "What If You Could Hear Every Lie?",
    "voice": "am_michael",
    "speed": 1.0,
    "hook": "Every lie made a buzz in my head",
    "description": ("One Tuesday, Sam starts hearing a buzz every time anyone lies to him. His sister, his coach, his best "
                    "friend, even his mom. At first it's a superpower. Then it costs him everyone. An original animated "
                    "story about truth, kindness and the lies people tell to protect each other.\n\n"
                    "Facts in this story: in a well-known 1996 diary study (DePaulo et al.), college students reported "
                    "about two lies a day; across many lab studies people spot lies only about 54% of the time "
                    "(Bond & DePaulo, 2006); and a 2010 survey (Serota et al.) found most lies are told by a small "
                    "number of prolific liars.\n\n#whatif #story #animation"),
    "tags": ["what if", "what if you could", "hear every lie", "lie detector", "animated story", "2d animation",
             "story time", "best friend", "family story", "life lesson", "the doodle desk"],
    "thumbnail": {"bg": "dark", "text": "MY MOM|LIED", "size": 170, "color": "yellow",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["hair"], "shirt": "orange"},
                  "guy_x": 1450, "guy_y": 1250, "guy_s": 2.2,
                  "items": [{"text": "LIE", "x": 1450, "y": 170, "size": 230, "color": "red", "outline": "white"}]},
    "scenes": scenes,
    "shorts": [{"start": 0, "dur": 35, "top": "Every lie made a buzz in my head", "title": "I Could Hear Every Lie. Even My Sister's."},
               {"start": 300, "dur": 35, "top": "Then my MOM lied to me", "title": "The Loudest Lie I Ever Heard"}],
}
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "ep025.json")
json.dump(job, open(out, "w"), indent=1, ensure_ascii=False)
words = sum(len(s["say"].split()) for s in scenes)
print(out, len(scenes), "scenes,", words, "words, ~%.1f min" % (words / 150))

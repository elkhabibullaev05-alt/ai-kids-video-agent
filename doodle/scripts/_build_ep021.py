"""Episode 21: 41 local data center ballot measures on Nov 3, 2026 -- voters limited data centers in 40 of 41 (Trenton OH 1,000 MW Amazon plan blocked)."""
import json
import os


def G(x, pose="stand", face="neutral", look=1, extras=(), s=1.0, y=900, at=0, **kw):
    d = {"guy": {"pose": pose, "face": face, "look": look, "extras": list(extras)}, "x": x, "y": y, "s": s, "at": at}
    for k in ("walk", "shirt", "label"):
        if k in kw:
            d["guy"][k] = kw.pop(k)
    d.update(kw)
    return d


def P(name, x, y=900, s=1.0, at=0, **kw):
    d = {"prop": name, "x": x, "y": y, "s": s, "at": at}
    d.update(kw)
    return d


def T(text, x, y, size=90, color="black", at=0, **kw):
    d = {"text": text, "x": x, "y": y, "size": size, "color": color, "at": at}
    d.update(kw)
    return d


def C(a, b, x, y, fmt="{:,.0f}", size=150, color="red", at=0, dur=1.8, **kw):
    d = {"count": [a, b], "fmt": fmt, "x": x, "y": y, "size": size, "color": color, "at": at, "dur": dur}
    d.update(kw)
    return d


DAVE = ["hair"]
ECON = ["glasses", "tie"]
LINDA = ["bun"]
RES = dict(extras=["cap"], shirt="green")          # generic resident
RES2 = dict(extras=["hair"], shirt="orange")
RES3 = dict(extras=["bun"], shirt="purple")
DEV = dict(extras=["tie", "briefcase"], shirt="grey")  # generic developer
OFF = dict(extras=["tie"], shirt="navy")              # generic official
JUDGE = dict(extras=["glasses"], shirt="dark")
BANK = dict(extras=["tie", "tophat"], shirt="grey")

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


def CROWD(x0, x1, at=0, face="happy", pose="fist", n=6, s=0.5):
    kinds = [RES, RES2, RES3]
    out = []
    step = (x1 - x0) // (n - 1)
    for i in range(n):
        out.append(G(x0 + i * step, pose, face, look=1 if i % 2 else -1, s=s, y=900,
                     at=(at + 0.04 * i) if at < 1 else at, **kinds[i % 3]))
    return out


def DC(x=1300, s=1.0, at=0, text=None, **kw):
    d = P("datacenter", x, 900, s, at=at, **kw)
    if text:
        d["text"] = text
    return d


def RESULT(town, pct, x=960, y=420, at=0, color="green"):
    return [T(town, x, y - 140, 80, "dark", at=at), C(0, pct, x, y, fmt="{:.0f}%", size=170, color=color, at=at + 0.1)]


# COLD OPEN ------------------------------------------------------------------
sc("This is a data center. It's the size of a few football fields, it hums all night, and it wanted to move in next to Dave.",
   DC(1250, 1.3, text="COMING SOON"), G(450, "stand", "worried", extras=DAVE, at=0.4), T("hmmmmm", 1250, 330, 70, "grey", at=0.6, anim="shake"), bg="yellow")
sc("Dave did not write an angry post. Dave did something much more boring. He signed a petition, and then he voted.",
   G(500, "hold", "neutral", extras=DAVE), P("clipboard", 900, 860, 0.9, text="PETITION", at=0.2), P("ballot", 1400, 860, 1.0, at=0.55))
sc("On Tuesday, November third, about forty-one towns, cities and counties held the same kind of vote. Here's the scoreboard.",
   P("calendar", 600, 860, 1.0, text="NOV 3"), C(0, 41, 1300, 430, fmt="{:.0f} votes", size=170, color="navy", at=0.3))
sc("Data centers: one. Neighbors: forty, according to the New York Times count.",
   P("scoreboard", 960, 760, 1.1, text="DATA CENTERS 1|NEIGHBORS 40", at=0), {"stamp": "40 OF 41", "x": 1550, "y": 330, "size": 80, "w": 420, "at": 0.6}, bg="yellow")
S.append({"say": "So here's today's question. How did a bunch of small towns beat one of the richest industries on Earth, and does it actually stop anything?",
          "items": [*CROWD(250, 850, face="smug", pose="hips", n=4, s=0.6), T("vs", 1050, 500, 120, "red", at=0.3), DC(1500, 0.9, at=0.4), T("?", 1500, 300, 200, "red", at=0.7)],
          "chapter": "Today's question"})
sc("We'll look at what was on the ballot, the numbers, why people voted the way they did, what the industry says, and what happens next.",
   P("ballot", 350, 860, 0.8), P("chart", 750, 900, 0.8, at=0.15), P("drop", 1100, 880, 0.6, at=0.3), P("speech", 1430, 860, 0.8, at=0.45), P("calendar", 1720, 860, 0.7, text="NEXT", at=0.6))

# PART 1: WHAT WAS ON THE BALLOT ---------------------------------------------
sc("First, what a data center is. It's a warehouse full of computers. Every chatbot answer, every video stream, every cloud photo lives in one somewhere.",
   DC(1300, 1.1), P("phone", 450, 860, 0.8), {"arrow": [[600, 620], [950, 620]], "color": "red", "at": 0.4}, chapter="Part 1: What was on the ballot")
sc("And artificial intelligence needs a lot more of them. Bigger ones, too. Which means they need land, electricity, and often water for cooling.",
   P("robot", 450, 900, 0.9), DC(1100, 0.7, at=0.2), P("powerline", 1550, 900, 0.8, at=0.45), P("drop", 1800, 880, 0.5, at=0.6))
sc("Usually, a city council or a county board decides whether one gets built. Voters don't get a say.",
   P("desk", 960, 900, 1.0), G(700, "present", "neutral", **OFF, label="council"), G(1250, "stand", "neutral", look=-1, **DEV, label="developer", at=0.3))
sc("This year, that changed in a lot of places. Ballotpedia, which tracks every measure, counted at least fifty local data center votes in thirteen states in twenty twenty-six.",
   C(0, 50, 650, 430, fmt="{:.0f}", size=220, color="navy"), T("local votes", 650, 620, 70, "dark", at=0.2), C(0, 13, 1350, 430, fmt="{:.0f}", size=220, color="navy", at=0.4), T("states", 1350, 620, 70, "dark", at=0.5))
sc("Forty-one of them landed on the same day as the midterm elections, in ten states. That's the largest wave of data center votes on record.",
   P("calendar", 500, 860, 1.0, text="NOV 3"), C(0, 41, 1100, 430, fmt="{:.0f}", size=240, color="red", at=0.2), {"stamp": "RECORD", "x": 1550, "y": 600, "size": 80, "w": 320, "at": 0.6})
sc("And most of them weren't put there by politicians. In Ballotpedia's September count, thirty-one of thirty-eight came from citizen petitions.",
   {"bars": {"values": [31, 7], "labels": ["petitions", "councils"], "colors": ["green", "grey"], "fmt": "{}", "w": 640, "h": 400}, "x": 700, "y": 860},
   G(1450, "hold", "smug", **RES, label="resident", at=0.5), P("clipboard", 1650, 860, 0.6, at=0.6))
sc("Neighbors with clipboards, standing outside grocery stores, asking strangers to sign. The least glamorous way to fight a trillion-dollar technology boom.",
   P("cart", 450, 900, 0.8), G(900, "hold", "happy", **RES3), P("clipboard", 1060, 830, 0.5, at=0.1), G(1350, "stand", "confused", look=-1, extras=DAVE, at=0.35))
sc("The questions weren't all the same. Some were outright bans. Some added rules. Some were advisory, basically asking: would you like one of these here? Yes or no.",
   T("BAN", 450, 420, 110, "red"), T("RULES", 960, 420, 110, "orange", at=0.25), T("YES / NO?", 1500, 420, 110, "navy", at=0.5), P("ballot", 960, 880, 0.8, at=0.6))
sc("That makes counting tricky. In twenty-eight of them, voting yes limited data centers. In thirteen, voting yes supported them.",
   {"bars": {"values": [28, 13], "labels": ["yes = limit", "yes = allow"], "colors": ["red", "green"], "fmt": "{}", "w": 640, "h": 400}, "x": 700, "y": 860},
   G(1450, "think", "confused", look=-1, extras=ECON, at=0.5))
sc("So the honest way to score it is by which side won, not by yes or no. Linda insisted on this. Linda always insists on this.",
   G(700, "point", "neutral", extras=LINDA, label="Linda"), P("scale", 1300, 900, 1.0, at=0.3), bg="sky")

# PART 2: THE NUMBERS ---------------------------------------------------------
sc("So, the numbers. By Wednesday evening, thirty-nine of the forty-one had been called. Thirty-eight went against data center development.",
   C(0, 38, 650, 430, fmt="{:.0f}", size=260, color="red"), T("of 39 called", 650, 640, 70, "dark", at=0.3), P("arrowdown", 1350, 880, 1.0, at=0.5),
   chapter="Part 2: The scoreboard")
sc("CNBC, using Ballotpedia's data, reported that voters sided against data centers in every measure except one. The Times later put it at forty of forty-one.",
   P("tv", 600, 880, 1.0, text="40 / 41"), G(1300, "shrug", "neutral", look=-1, extras=ECON, at=0.4))
sc("And the six votes held earlier this year? All six also went against data centers, by margins of sixty-six to ninety percent.",
   *[P("ballot", 360 + i * 240, 600, 0.5, at=0.06 * i) for i in range(6)], T("66% - 90%", 960, 330, 120, "red", at=0.55))
sc("Ohio had the most of any state: eighteen towns and cities voted on data center measures. They all went the same way.",
   T("OHIO", 600, 330, 150, "navy"), C(0, 18, 600, 560, fmt="{:.0f} places", size=110, color="red", at=0.2), *CROWD(1100, 1700, face="happy", pose="fist", n=4, at=0.4))
sc("In Urbana, Ohio, a ban passed with seventy-seven percent. Two thousand nine hundred seventy-eight votes to eight hundred seventy-seven.",
   *RESULT("Urbana, OH", 77, 650), {"bars": {"values": [2978, 877], "labels": ["yes", "no"], "colors": ["green", "grey"], "fmt": "{:,}", "w": 520, "h": 380}, "x": 1400, "y": 860, "at": 0.4})
sc("In Upper Sandusky, also seventy-seven percent. In Defiance, sixty-five. In Sunbury, seventy-nine.",
   *RESULT("Upper Sandusky", 77, 450), *RESULT("Defiance", 65, 960, at=0.3), *RESULT("Sunbury", 79, 1480, at=0.6))
sc("In Ashville, voters rejected a deal the village had worked out with a data center company. Eighty-two percent said no.",
   G(500, "hold", "smug", **DEV, label="developer"), P("clipboard", 680, 830, 0.5), {"cross": [690, 760, 120], "at": 0.4}, *RESULT("Ashville, OH", 82, 1350, at=0.3, color="red"))
sc("In Wilmington, around eighty percent rejected rezoning land for a data center. They had to vote on it four separate times, once per parcel of land.",
   *[P("ballot", 450 + i * 330, 640, 0.6, at=0.1 * i) for i in range(4)], T("x4", 1700, 400, 140, "red", at=0.5), C(0, 80, 960, 330, fmt="~{:.0f}%", size=120, color="red", at=0.6))
sc("And in the village of Monroeville, an advisory question asked if people wanted data centers at all. Eighty-seven point seven five percent said no.",
   C(0, 87.75, 700, 430, fmt="{:.2f}%", size=170, color="red"), T("NO", 700, 640, 120, "red", at=0.4), G(1400, "facepalm", "tired", look=-1, **DEV, label="developer", at=0.5))
sc("It wasn't just Ohio. In Alhambra, California, a ban passed with eighty-two percent. In Edgewater, Florida, seventy-seven.",
   *RESULT("Alhambra, CA", 82, 600), *RESULT("Edgewater, FL", 77, 1350, at=0.4))
sc("In Emporia, Kansas, a ban on large data centers passed four thousand three hundred forty-six to two thousand eight hundred ninety-one. About sixty percent.",
   {"bars": {"values": [4346, 2891], "labels": ["ban", "no ban"], "colors": ["green", "grey"], "fmt": "{:,}", "w": 600, "h": 400}, "x": 700, "y": 860}, *RESULT("Emporia, KS", 60, 1450, at=0.4))
sc("In Madison County, Illinois, four townships said no to data centers. In Chouteau Township, eighty-three percent.",
   T("Madison County, IL", 960, 300, 90, "navy"), *[P("house", 450 + i * 340, 900, 0.6, at=0.1 * i) for i in range(4)], C(0, 83, 960, 520, fmt="{:.0f}%", size=130, color="red", at=0.5))
sc("The woman who led that signature drive, Heather Groetecke, told St. Louis Public Radio: I am so stunned by the numbers.",
   G(700, "panic", "shock", **RES3, label="petition organizer"), {"box": [1050, 320, 700, 200], "color": "white", "at": 0.3},
   T("\"I am so stunned", 1400, 390, 60, "dark", at=0.35), T("by the numbers.\"", 1400, 460, 60, "dark", at=0.4))
sc("Dave was also stunned. Mostly because he has never, in his life, agreed with eighty-three percent of anyone about anything.",
   G(900, "shrug", "shock", extras=DAVE), C(0, 83, 1400, 400, fmt="{:.0f}%", size=150, color="red", at=0.3), bg="yellow")

# PART 3: THE ONE EXCEPTION ---------------------------------------------------
sc("Now, the one exception. Harwood, North Dakota.",
   T("HARWOOD, ND", 960, 380, 130, "navy"), P("flag", 960, 900, 0.9, at=0.3), chapter="Part 3: The one exception")
sc("Harwood voted on a charter amendment that would have required extra independent review of big industrial projects, including data centers.",
   P("magnifier", 600, 860, 1.0), DC(1300, 0.8, at=0.3), T("extra review?", 960, 300, 90, "dark", at=0.5))
sc("Seventy-five percent voted no. So that counts as a win for development.",
   C(0, 75, 700, 430, fmt="{:.0f}%", size=220, color="green"), T("NO to extra review", 700, 640, 70, "dark", at=0.3), G(1400, "fist", "grin", look=-1, **DEV, at=0.5))
sc("But even that one is small. Route Fifty noted it would not have affected the big data center campus already approved there.",
   DC(1100, 0.9, text="ALREADY APPROVED"), {"stamp": "UNCHANGED", "x": 1400, "y": 330, "size": 70, "w": 380, "at": 0.5}, G(450, "shrug", "neutral", extras=ECON, at=0.3))
sc("So, depending on how you count, the industry's best result of the night was a vote that left everything exactly where it already was.",
   P("scoreboard", 960, 760, 1.0, text="NIGHT'S BEST|NO CHANGE"), G(1550, "think", "tired", look=-1, **DEV, at=0.4))

# PART 4: TRENTON -------------------------------------------------------------
sc("To see what's really at stake, look at one town. Trenton, Ohio, in Butler County, between Cincinnati and Dayton.",
   T("TRENTON, OHIO", 960, 330, 130, "navy"), P("house", 600, 900, 0.8, at=0.3), P("house", 900, 900, 0.7, at=0.35), P("house", 1200, 900, 0.8, at=0.4),
   chapter="Part 4: One town, up close")
sc("A local group called the Woodsdale and Trenton Environmental Resistance gathered signatures for Issue Seventeen: a ban on data centers above twenty-five megawatts.",
   *CROWD(300, 900, face="happy", pose="hold", n=4, s=0.6), P("clipboard", 1350, 860, 0.9, text="ISSUE 17", at=0.3), T("> 25 MW", 1350, 330, 110, "red", at=0.5))
sc("Then, in August, the city council voted not to certify the petition. So it wasn't going on the ballot.",
   G(700, "hips", "smug", **OFF, label="city council"), P("clipboard", 1250, 860, 0.9, text="ISSUE 17"), {"cross": [1250, 720, 150], "at": 0.4})
sc("The residents went to the Ohio Supreme Court. The court found the council had disregarded the law and ordered it to certify the petition.",
   G(960, "point", "neutral", look=-1, **JUDGE, label="Ohio Supreme Court"), P("scale", 1450, 900, 0.9, at=0.2), {"stamp": "CERTIFY IT", "x": 500, "y": 400, "size": 70, "w": 380, "at": 0.55})
sc("On Tuesday, Issue Seventeen passed with eighty percent of the vote.",
   C(0, 80, 960, 430, fmt="{:.0f}%", size=300, color="green"), *CROWD(400, 1520, face="grin", pose="fist", n=6, at=0.5))
sc("Here's why that matters. According to WVXU, the ban blocks plans for Trenton to annex land for a one thousand megawatt Amazon data center.",
   DC(1250, 1.2, text="1,000 MW"), C(0, 1000, 500, 400, fmt="{:,.0f} MW", size=130, color="red", at=0.3), {"cross": [1250, 720, 260], "at": 0.7})
sc("One thousand megawatts is forty times the new limit. That's not a building, that's a small power-plant-sized appetite.",
   {"bars": {"values": [25, 1000], "labels": ["limit", "planned"], "colors": ["green", "red"], "fmt": "{} MW", "w": 640, "h": 440}, "x": 700, "y": 860},
   T("x40", 1450, 450, 200, "red", at=0.5), P("powerline", 1600, 900, 0.6, at=0.6))
sc("It also puts a question mark over a two hundred fifty megawatt facility already being built by the company Prologis in the city's industrial park.",
   P("building", 700, 900, 0.9, text="250 MW"), T("?", 1300, 450, 300, "red", at=0.4), P("truck", 1500, 900, 0.6, at=0.5))
sc("Barry Blankenship, a leader of the group, told WVXU: It's a sigh of relief. When people go to bed tonight, they can actually sleep.",
   G(550, "stand", "happy", **RES, label="resident group leader"), {"box": [900, 330, 900, 220], "color": "white", "at": 0.3},
   T("\"It's a sigh of relief.\"", 1350, 400, 58, "dark", at=0.35), T("\"...they can actually sleep.\"", 1350, 480, 52, "dark", at=0.45))
sc("Dave, meanwhile, has started going to bed at nine. Not because of a data center. He just likes saying it's for civic reasons.",
   P("house", 960, 900, 1.2), P("sun", 1500, 400, 0.6, at=0.2), T("zzz", 1100, 450, 90, "navy", at=0.5, anim="bob"), bg="purple")

# subscribe line (value)
sc("Quick pause. If you like news explained without anyone yelling at you, subscribe. We draw it, we count it, we let you decide.",
   G(960, "wave", "happy", extras=DAVE), T("SUBSCRIBE?", 960, 320, 110, "red", at=0.3), bg="yellow")

# PART 5: WHY --------------------------------------------------------------------
sc("So why did people vote like this? Reporters heard the same three reasons again and again.",
   T("WHY?", 960, 400, 200, "red"), chapter="Part 5: Why people voted no")
sc("Reason one: electricity bills. Big data centers draw huge amounts of power, and people worry the cost of new power lines and plants lands on their bill.",
   P("powerline", 500, 900, 1.0), P("dollar", 1000, 860, 1.0, at=0.3), P("arrowup", 1400, 880, 0.9, at=0.5), G(1700, "panic", "worried", look=-1, extras=DAVE, s=0.8, at=0.6))
sc("In a June Reuters slash Ipsos poll, cited by Newsweek, seventy-seven percent of respondents said they worried data centers could raise their electricity rates.",
   C(0, 77, 700, 430, fmt="{:.0f}%", size=240, color="red"), T("worried about rates", 700, 650, 70, "dark", at=0.3), P("chart", 1400, 900, 0.9, at=0.5))
sc("Reason two: water, used for cooling. In Grove City, Ohio, voters now get a say on any big project using more than half a million gallons.",
   P("drop", 500, 880, 1.1, text="H2O"), C(0, 500000, 1200, 430, fmt="{:,.0f} gal", size=110, color="blue", at=0.3), T("Grove City: 55% yes", 1200, 620, 70, "dark", at=0.5))
sc("Reason three: the deals. Route Fifty reported that voters pointed to secretive agreements between local officials and developers, often with tax breaks attached.",
   G(650, "hold", "smug", **OFF), G(1050, "hold", "smug", look=-1, **DEV, at=0.15), P("envelope", 850, 650, 0.6, at=0.3), P("lock", 1500, 860, 0.8, at=0.5))
sc("In the village of Perry, Ohio, eighty-seven percent voted that developers seeking tax breaks must give the village financial guarantees.",
   *RESULT("Perry, OH", 87, 700), P("moneybag", 1400, 880, 1.0, at=0.4), T("guarantees", 1400, 450, 70, "dark", at=0.5))
sc("And there's a fourth thing that isn't on any ballot: the feeling of being steamrolled.",
   P("truck", 900, 900, 1.4, move=[1300, 900]), G(400, "panic", "shock", extras=DAVE, at=0.3))
sc("Blankenship put it this way: city governments and these big businesses want to come into these little communities and roll over us.",
   G(600, "point", "angry", **RES, label="resident group leader"), {"box": [950, 350, 850, 180], "color": "white", "at": 0.3},
   T("\"...come into these little", 1375, 410, 54, "dark", at=0.35), T("communities and roll over us\"", 1375, 470, 54, "dark", at=0.4))

# PART 6: THE OTHER SIDE ----------------------------------------------------------
sc("Now the other side, because there is one. The industry says the fears about bills are wrong.",
   DC(960, 1.0), G(1500, "present", "neutral", look=-1, **DEV, label="industry", at=0.3), chapter="Part 6: What the industry says")
sc("The Data Center Coalition, the main trade group, says data centers don't cause higher bills. In July, it said the industry is committed to paying our full energy costs.",
   G(600, "present", "neutral", **DEV, label="trade group"), {"box": [950, 330, 820, 170], "color": "white", "at": 0.3},
   T("\"paying our full", 1360, 390, 60, "dark", at=0.35), T("energy costs\"", 1360, 450, 60, "dark", at=0.4))
sc("Its president, Josh Levi, told E and E News the industry's own research found the buildout had not raised costs for other customers.",
   G(600, "point", "neutral", **DEV, label="trade group president"), P("chart", 1300, 900, 1.0, text="their research", at=0.3))
sc("He also admitted they hadn't made that case loudly enough. Quote: the absence of really leaning forward with those facts leaves a vacuum.",
   G(600, "shrug", "worried", **DEV, label="trade group president"), {"box": [950, 330, 860, 170], "color": "white", "at": 0.3},
   T("\"...leaves a vacuum\"", 1380, 415, 64, "dark", at=0.35))
sc("There's also money on the table for towns. In Emporia, the local paper reported a warning that the vote signals to investors the city is narrowing its opportunities.",
   P("moneybag", 600, 880, 1.1), {"arrow": [[800, 640], [1200, 640]], "color": "red", "at": 0.3}, P("arrowdown", 1450, 880, 0.9, at=0.5))
sc("And the city itself said the votes do not resolve the legal questions. Some of these bans may be challenged in court.",
   P("scale", 700, 900, 1.0), G(1300, "think", "neutral", look=-1, **JUDGE, label="courts?", at=0.3))
sc("So depending on who you ask, these votes protected people's bills and water, or scared off jobs and tax money. We just count the facts.",
   P("scale", 960, 900, 1.2), T("bills & water", 520, 400, 70, "green", at=0.2), T("jobs & taxes", 1400, 400, 70, "orange", at=0.35), bg="sky")

# PART 7: DOES IT STOP ANYTHING? -------------------------------------------------
sc("Back to the big question. Does any of this actually stop the AI buildout?",
   P("robot", 700, 900, 1.0), T("STOP?", 1300, 450, 160, "red", at=0.3), chapter="Part 7: Does it stop anything?")
sc("Not directly. These are local votes. A company blocked in one town can look in the next county, or the next state.",
   DC(500, 0.6, text="NO"), {"arrow": [[750, 600], [1150, 600]], "color": "red", "at": 0.3}, DC(1450, 0.6, at=0.5, text="MAYBE?"))
sc("But money is paying attention. Semafor reported that banks and asset managers backing the buildout have started treating local opposition as a credit risk.",
   G(600, "think", "worried", **BANK, label="lender"), P("clipboard", 1000, 860, 0.7, text="RISK", at=0.3), T("local opposition", 1450, 400, 70, "red", at=0.5))
sc("Translation: if a project might get voted out, the loan for it gets harder or more expensive. Petitions are now a line on a spreadsheet.",
   P("laptop", 700, 880, 1.0), P("clipboard", 1250, 860, 0.8, text="PETITION", at=0.3), {"arrow": [[1000, 600], [850, 650]], "color": "red", "at": 0.5})
sc("And more votes are coming. On December first, Clarksville, Arkansas, votes on bonds for data center projects, up to fifty billion dollars and five billion dollars.",
   P("calendar", 500, 860, 1.0, text="DEC 1"), C(0, 50, 1200, 430, fmt="${:.0f}B", size=180, color="money", at=0.3), T("+ $5B", 1200, 620, 90, "money", at=0.55))
sc("On December fifteenth, Mandan, North Dakota, votes on banning data centers of twenty-five megawatts or more.",
   P("calendar", 600, 860, 1.0, text="DEC 15"), T("Mandan, ND", 1300, 380, 100, "navy", at=0.3), T("> 25 MW?", 1300, 540, 100, "red", at=0.5))
sc("And the biggest test may be in Ohio in twenty twenty-seven. Backers of a statewide ban on large data centers need four hundred thirteen thousand four hundred eighty-seven valid signatures.",
   T("OHIO 2027", 960, 300, 120, "navy"), C(0, 413487, 960, 520, fmt="{:,.0f}", size=150, color="red", at=0.3), P("clipboard", 1650, 880, 0.7, at=0.6))
sc("They missed this year's deadline, and say they're aiming for the November twenty twenty-seven ballot. That would be all of Ohio voting, not just one town.",
   P("calendar", 600, 860, 1.0, text="NOV 2027"), *CROWD(1000, 1700, face="neutral", pose="stand", n=5, s=0.45, at=0.4))

# RECAP ---------------------------------------------------------------------------
sc("Let's recap. On November third, forty-one local votes on data centers happened in ten states, mostly started by residents with petitions.",
   P("clipboard", 600, 860, 1.0, text="41 VOTES"), P("ballot", 1300, 860, 1.0, at=0.3), chapter="Recap")
sc("Almost every one went against data centers. The single exception, Harwood, North Dakota, didn't change the project already approved there.",
   P("scoreboard", 960, 760, 1.0, text="DATA CENTERS 1|NEIGHBORS 40"), T("Harwood: unchanged", 960, 300, 70, "dark", at=0.5))
sc("The industry says it pays its own way and costs nobody else. Voters weren't convinced. Next up: December, then maybe all of Ohio.",
   DC(600, 0.7), T("vs", 960, 500, 100, "red", at=0.3), *CROWD(1200, 1700, face="smug", pose="hips", n=3, s=0.5, at=0.4))
sc("Meanwhile, Dave's town didn't get the data center. Dave celebrated by streaming three movies, uploading two hundred photos to the cloud, and asking a chatbot for a cake recipe.",
   G(600, "type", "happy", extras=DAVE), P("laptop", 950, 860, 0.8), P("tv", 1350, 880, 0.7, at=0.3), P("phone", 1650, 860, 0.6, at=0.5), bg="yellow")
sc("All of which, of course, happened in a data center. Somewhere else.",
   DC(1100, 1.2, text="SOMEWHERE ELSE"), G(450, "facepalm", "confused", extras=DAVE, at=0.4), bg="yellow")
sc("Your turn. Should your town get a vote on a data center, or should that be up to the council? Tell us in the comments.",
   G(700, "point", "happy", extras=LINDA, label="Linda"), P("ballot", 1250, 860, 0.9, at=0.3), T("vote or council?", 1250, 380, 80, "navy", at=0.4))
sc("If this helped, subscribe for calm, stick-figure explainers. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), T("THE DOODLE DESK", 960, 330, 110, "dark", at=0.3))


script = {
    "id": "ep021",
    "title": "41 Small Towns vs. Big Tech: Who Won the Data Center Vote?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Nov 3, 2026, the same day as the US midterms, voters decided 41 local ballot measures on data centers in 10 states, the largest wave of such votes on record. "
        "Most were put on the ballot by residents' petitions. Almost every one went against data center development; the one exception, Harwood, North Dakota, did not affect the campus already approved there. "
        "We go through what was on the ballot, the results (Urbana 77%, Trenton 80%, Monroeville 87.75%, Alhambra 82%, Emporia 4,346-2,891), "
        "the Trenton, Ohio fight over a planned 1,000 MW Amazon data center, why people voted no (power bills, water, secret deals), what the industry says, and what comes next "
        "(Clarksville, AR on Dec 1, Mandan, ND on Dec 15, a possible Ohio statewide vote in 2027). "
        "Real people appear only as generic labelled stick figures; quotes are as reported. Results are unofficial until certified.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "CNBC, Voters rebuff data centers in every ballot measure except one (Nov 4, 2026): https://www.cnbc.com/2026/11/04/data-center-ballot-measures-2026-midterm.html\n"
        "Duane Morris Government Strategies / Ballotpedia data, Data Centers on the Ballot: Where Things Stand (Nov 4, 2026): https://statecapitallobbyist.com/artificial-intelligence-ai/data-centers/data-centers-on-the-ballot-where-things-stand/\n"
        "WVXU (NPR Cincinnati), Trenton votes to ban data centers (Nov 3, 2026): https://www.wvxu.org/environment/2026-11-03/trenton-votes-to-ban-data-centers\n"
        "Cincinnati Enquirer, Ohioans overwhelmingly pass data center bans (Nov 4, 2026): https://www.cincinnati.com/story/news/politics/2026/11/04/see-how-ohioan-voted-on-data-center-bans/92479076007/\n"
        "Emporia Gazette, Emporia voters approve data center bans (Nov 3, 2026): https://www.emporiagazette.com/free/article_36632afb-2bdf-4a1e-9d12-8c8e2239f7c0.html\n"
        "New York Times, Voters Rejected A.I. in the Midterms (Nov 4, 2026): https://www.nytimes.com/2026/11/04/technology/midterm-elections-ai-data-centers.html\n"
        "BreezyScroll, Data centers lost 37 of 38 local ballot votes counted so far (Nov 4, 2026), citing St. Louis Public Radio, Route Fifty, Semafor, E&E News: https://www.breezyscroll.com/technology-news/data-center-ballot-measures-voters-reject\n\n"
        "#datacenters #ai #election #ohio #electricity #localnews #explained #stickfigure"
    ),
    "tags": ["data centers", "data center ballot measures", "data center ban", "trenton ohio", "amazon data center", "ai data centers", "electricity bills",
             "midterms 2026", "ballot measures", "local elections", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "TOWNS|SAID NO", "size": 190, "color": "black",
                  "guy": {"pose": "stand", "face": "smug", "look": -1, "extras": ["cap"], "shirt": "green"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "datacenter", "x": 400, "y": 1050, "s": 1.0}, {"cross": [400, 900, 230], "color": "red"}, {"arrow": [[700, 760], [1000, 600]], "color": "red"}]},
    "scenes": [s for s in S if s],
}
_CYC = ["paper", "sky", "paper", "teal", "paper", "purple"]
for _i, _s in enumerate(script["scenes"]):
    if _s.get("bg") not in ("yellow", "sky", "purple"):
        _s["bg"] = _CYC[_i % len(_CYC)]
for s in script["scenes"]:
    for it in list(s["items"]):
        g = it.get("guy")
        if g and g.get("label"):
            sz = it.get("s", 1.0)
            s["items"].append({"text": g.pop("label"), "x": it["x"], "y": it.get("y", 900) - int(430 * sz), "size": 44,
                               "color": "dark", "at": it.get("at", 0)})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep021.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

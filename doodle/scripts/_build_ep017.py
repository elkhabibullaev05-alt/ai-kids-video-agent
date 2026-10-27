"""Episode 17: Alaska Senate race — two Dan Sullivans on one ballot, and a DOJ lawsuit to block certification if the incumbent loses. Explained with stick figures."""
import json
import os

# helpers -------------------------------------------------------------------
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



def SIGN(x, text, s=1.0, at=0):
    """Protest placard: pole + white board + big word (the engine's 'sign' prop is a speed-limit sign)."""
    w, h = int(260 * s), int(150 * s)
    top = 900 - int(400 * s)
    return [{"box": [x - int(6 * s), top + h, int(12 * s), 900 - top - h], "color": "brown", "at": at},
            {"box": [x - w // 2, top, w, h], "color": "white", "at": at},
            {"text": text, "x": x, "y": top + h // 2, "size": min(int(70 * s), int(1.6 * w / max(1, len(text)))), "color": "dark", "at": at}]


DAVE = ["hair"]
ECON = ["glasses", "tie"]
OFF = ["tie", "briefcase"]
LINDA = ["bun"]
PRES = dict(extras=["tie"], shirt="navy")                  # generic head of government stick figure
MIN = dict(extras=["tie", "briefcase"], shirt="grey")       # generic minister
LEFT = dict(extras=["tie"], shirt="red")                    # generic left-wing politician
RIGHT = dict(extras=["tie"], shirt="blue")                  # generic right-wing politician
STU = dict(extras=["hair"], shirt="orange")             # generic student protester
STU2 = dict(extras=["cap"], shirt="teal")
GRAN = dict(extras=["bun", "glasses"], shirt="purple")      # generic pensioner
COP = dict(extras=["cap"], shirt="navy")                    # generic police officer
PROF = dict(extras=["glasses"], shirt="brown")              # generic professor

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


SEN = dict(extras=["tie"], shirt="blue", label="Sen. Dan S. Sullivan")      # generic incumbent senator
DAN2 = dict(extras=["glasses", "cap"], shirt="green", label="Daniel J. Sullivan Jr.")   # generic retired teacher
PEL = dict(extras=["bun"], shirt="red", label="Mary Peltola")              # generic challenger
DOJ = dict(extras=["tie", "briefcase"], shirt="grey", label="Justice Dept.")
PRES = dict(extras=["tie"], shirt="navy", label="the President")
JUDGE = dict(extras=["glasses"], shirt="dark", label="judge")
PROF = dict(extras=["glasses"], shirt="brown", label="law professor")
ELEC = dict(extras=["cap"], shirt="teal", label="election officials")


def NAMECARD(x, y, text, color="white", w=560, h=110, at=0, size=50):
    return [{"box": [x - w // 2, y - h // 2, w, h], "color": color, "at": at},
            {"text": text, "x": x, "y": y, "size": size, "color": "dark", "at": at}]


def BALLOT(x, y, rows, at=0, w=900, mark=None):
    """Big paper ballot with name rows; mark = index of row with a filled bubble."""
    h = 110 * len(rows) + 120
    out = [{"box": [x - w // 2, y, w, h], "color": "white", "at": at},
           {"text": "U.S. SENATE", "x": x, "y": y + 55, "size": 54, "color": "navy", "at": at}]
    for i, r in enumerate(rows):
        yy = y + 160 + i * 110
        out.append({"ring": [x - w // 2 + 60, yy, 26], "at": at})
        out.append({"text": r, "x": x + 50, "y": yy, "size": 40, "color": "dark", "at": at + 0.08 * (i + 1) if at < 1 else at})
    if mark is not None:
        out.append({"cross": [x - w // 2 + 60, y + 160 + mark * 110, 22], "at": 0.7, "color": "blue"})
    return out


ROWS = ["Heikes, Gerald", "Peltola, Mary", "Sullivan, Dan S (Rep.) Incumbent", "Sullivan, Daniel J Jr"]

# COLD OPEN --------------------------------------------------------------------
sc("Picture it. You're in a voting booth in Alaska. You find the candidate you came for. Then you look one line down. And there he is again.",
   P("booth", 520, 900, 1.1), G(520, "stand", "neutral", extras=DAVE, s=0.9, at=0.1), *BALLOT(1300, 260, ["Sullivan, Dan", "Sullivan, Dan"], at=0.35),
   cam={"from": [1300, 500, 1.3], "to": [960, 540, 1.0]}, bg="sky")
sc("Two Dan Sullivans. Same name, same state, same Senate race. Dave has been staring at this ballot for eleven minutes.",
   G(600, "think", "confused", extras=DAVE), P("stopwatch", 1000, 700, 1.0, at=0.3), C(0, 11, 1450, 420, fmt="{:.0f} min", size=170, color="red", at=0.45), bg="yellow")
sc("And now the federal government has gone to court about it. It wants the power to freeze the result, but only if one of the Dans loses.",
   P("capitol", 520, 900, 0.9), {"arrow": [[760, 600], [1060, 600]], "at": 0.3}, P("scale", 1350, 880, 1.2, at=0.4), {"stamp": "FREEZE?", "x": 1350, "y": 330, "size": 80, "w": 340, "at": 0.65})
S.append({"say": "Today's question: can a name stop an election? Who are these two men, what does the lawsuit actually ask, and what do both sides say?",
          "items": [G(450, "stand", "smug", look=1, **SEN), G(1450, "stand", "neutral", look=-1, **DAN2, at=0.2), T("vs.", 960, 450, 160, "red", at=0.4),
                    T("TODAY", 960, 200, 90, "dark", at=0.6)],
          "chapter": "Today's question"})

# PART 1: MEET THE DANS --------------------------------------------------------
sc("Dan number one. Dan S. Sullivan, the Republican senator. First elected in twenty fourteen, re-elected in twenty twenty, now asking for a third six-year term.",
   G(600, "present", "neutral", **SEN), P("calendar", 1150, 860, 0.9, text="2014", at=0.3), P("calendar", 1500, 860, 0.9, text="2020", at=0.5),
   chapter="Part 1: Meet the Dans")
sc("Before that, he was Alaska's attorney general and its commissioner of natural resources. A long résumé. A very common name.",
   G(500, "stand", "smug", **SEN), P("clipboard", 1050, 860, 1.1, text="CV", at=0.3), T("Dan Sullivan", 1450, 360, 90, "navy", at=0.55))
sc("Dan number two. Daniel J. Sullivan Junior. A retired elementary school teacher and former Forest Service worker from Petersburg, a small town in southeast Alaska.",
   G(560, "wave", "happy", **DAN2), P("chalkboard", 1250, 860, 0.9, text="A B C", at=0.35), P("house", 1650, 900, 0.7, at=0.6))
sc("He entered the race at the end of May. He's registered as a Republican too. Because of course he is.",
   G(560, "shrug", "neutral", **DAN2), P("calendar", 1150, 860, 1.0, text="MAY", at=0.3), T("REPUBLICAN", 1500, 380, 70, "blue", at=0.55))
sc("Republicans say he's a plant, put in the race to pull votes away from the senator. He says he decided to run on his own.",
   G(450, "point", "angry", extras=["tie"], shirt="blue", label="Republicans"), P("speech", 960, 420, 1.3, text="a plant!", at=0.25),
   G(1500, "hips", "neutral", look=-1, **DAN2, at=0.5), P("speech", 1500, 280, 0.9, text="my idea", at=0.7))
sc("And then there's the person both Dans are trying to beat: Mary Peltola, a Democrat and former congresswoman.",
   G(960, "wave", "grin", **PEL), G(450, "stand", "neutral", s=0.8, **SEN, at=0.3), G(1470, "stand", "neutral", s=0.8, look=-1, **DAN2, at=0.4))
sc("In twenty twenty-two, she became the first Alaska Native elected to the U.S. House. She served one term.",
   G(600, "present", "happy", **PEL), P("capitol", 1300, 900, 0.9, at=0.3), {"stamp": "FIRST", "x": 1300, "y": 300, "size": 80, "w": 280, "at": 0.6})
sc("There's also a fourth candidate, Gerald Heikes. He'd like you to know he exists. Nobody has the same name as him.",
   G(960, "wave", "neutral", extras=["hair"], shirt="purple", label="Gerald Heikes"), T("(unique name)", 960, 300, 70, "grey", at=0.45))

# PART 2: THE NUMBERS ----------------------------------------------------------
sc("Now the numbers. Alaska held its open primary in August. Everyone runs on one list, and the top four go through.",
   P("calendar", 600, 860, 1.0, text="AUG"), T("TOP 4", 1300, 420, 160, "navy", at=0.35), chapter="Part 2: The numbers")
sc("Mary Peltola came first, with forty-nine point five four percent.",
   C(0, 49.54, 960, 420, fmt="{:.2f}%", size=230, color="red"), G(1650, "fist", "grin", look=-1, **PEL, at=0.5))
sc("Senator Sullivan: forty-one point four zero percent. More than sixty-eight thousand votes.",
   C(0, 41.40, 960, 400, fmt="{:.2f}%", size=230, color="blue"), T("68,000+ votes", 960, 600, 80, "dark", at=0.5), G(1650, "stand", "worried", look=-1, **SEN, at=0.4))
sc("And the other Dan Sullivan: four thousand one hundred and seven votes. Two point four seven percent.",
   C(0, 4107, 900, 400, fmt="{:,.0f}", size=220, color="green"), T("2.47%", 900, 600, 110, "green", at=0.5), G(1600, "shrug", "happy", look=-1, **DAN2, at=0.4))
sc("Two and a half percent sounds tiny. Hold that thought. In a close race, tiny can be the whole story.",
   {"bars": {"values": [49.54, 41.40, 2.47], "labels": ["Peltola", "Sen. Sullivan", "Daniel J."], "colors": ["red", "blue", "green"], "fmt": "{}%", "w": 900, "h": 440}, "x": 860, "y": 830},
   {"ring": [1180, 760, 90], "at": 0.6})
sc("Why does it matter nationally? Republicans hold fifty-three of the hundred Senate seats. Democrats, plus two independents who vote with them, hold forty-seven.",
   {"bars": {"values": [53, 47], "labels": ["Republicans", "Dems + 2 ind."], "colors": ["blue", "red"], "fmt": "{}", "w": 700, "h": 420}, "x": 760, "y": 830},
   P("capitol", 1550, 900, 0.8, at=0.4))
sc("Democrats need a net gain of four seats to take control. So every single seat gets watched like a pot of coffee at six a.m.",
   C(0, 4, 650, 420, fmt="+{:.0f}", size=250, color="red"), P("coffee", 1350, 860, 1.3, at=0.35, anim="shake"), G(1700, "think", "tired", look=-1, extras=DAVE, at=0.5))
sc("For context, Alaska has only about seven hundred and thirty-eight thousand people. But it still gets two senators, same as California.",
   C(0, 738000, 900, 420, fmt="{:,.0f}", size=190, color="navy"), T("people", 900, 600, 80, "dark", at=0.4), P("globe", 1600, 860, 0.8, at=0.5))

# PART 3: THE FIGHT OVER THE BALLOT --------------------------------------------
sc("So how did two Dans end up on one ballot? It started in June, when Alaska's Division of Elections removed the second Dan.",
   P("calendar", 600, 860, 1.0, text="JUNE 15"), G(1250, "point", "angry", **ELEC, at=0.3), {"cross": [1650, 500, 110], "at": 0.6},
   chapter="Part 3: The ballot fight")
sc("According to Alaska's News Source, officials gave four reasons. First: the name choice itself was meant to confuse voters.",
   *NAMECARD(960, 300, "1. the name"), G(500, "point", "neutral", **ELEC, at=0.2), G(1450, "shrug", "confused", look=-1, **DAN2, at=0.4))
sc("Second, his party choice. Third, campaign imagery that looked like the senator's. Fourth, he used a consultant who had backed Peltola.",
   *NAMECARD(700, 280, "2. party", w=420), *NAMECARD(1250, 280, "3. imagery", w=420, at=0.3), *NAMECARD(960, 450, "4. consultant", w=500, at=0.55),
   G(960, "think", "worried", extras=LINDA, at=0.1, s=0.8))
sc("He fought back in court. A superior court sided with him. Then Alaska's Supreme Court agreed and put him back on the ballot.",
   G(500, "fist", "grin", **DAN2), P("scale", 1050, 880, 1.1, at=0.3), G(1550, "stand", "neutral", look=-1, **JUDGE, at=0.5), {"stamp": "BACK ON", "x": 1050, "y": 330, "size": 80, "w": 340, "at": 0.7})
sc("The timing was tight. The ruling came one day before the state's deadline to print ballots. Somewhere, a printer sighed with relief.",
   P("calendar", 600, 860, 1.0, text="DEADLINE"), C(0, 1, 1150, 420, fmt="{:.0f} day", size=200, color="red", at=0.3), P("envelope", 1600, 860, 1.1, at=0.55, anim="bob"))
sc("At a hearing, the chief justice asked whether the state really had to list him as a Republican. Another justice answered: but he's registered.",
   G(500, "think", "neutral", **JUDGE), P("speech", 960, 380, 1.2, text="as Republican?", at=0.25), G(1450, "point", "neutral", look=-1, extras=["bun", "glasses"], shirt="dark", label="justice", at=0.5),
   P("speech", 1500, 250, 0.9, text="he's registered", at=0.7))
sc("So here is what the ballot says now. The senator: Sullivan, Dan S, Registered Republican, Incumbent.",
   *BALLOT(960, 160, ROWS, at=0), {"arrow": [[1750, 540], [1440, 540]], "at": 0.5, "color": "blue"})
sc("The other one: Sullivan, Daniel J Junior. No party label at all. He's the only candidate on that list without one.",
   *BALLOT(960, 160, ROWS, at=0), {"arrow": [[1750, 650], [1440, 650]], "at": 0.4, "color": "green"})
sc("One political scientist at the University of Alaska Southeast, Glenn Wright, told Al Jazeera the ballots are, quote, super, super, super clear.",
   G(500, "present", "smug", extras=["glasses"], shirt="brown", label="Glenn Wright"), T("\"super, super,", 1250, 360, 80, "dark", at=0.3), T("super clear\"", 1250, 480, 80, "dark", at=0.45))
sc("Another, Forrest Nabors at the University of Alaska Anchorage, said the similar names could swing a close race. Depending on who you ask.",
   G(500, "think", "worried", extras=["glasses", "tie"], shirt="tan", label="Forrest Nabors"), P("scale", 1300, 880, 1.2, at=0.3, anim="shake"))

# PART 4: HOW RANKED-CHOICE WORKS ----------------------------------------------
sc("To understand the lawsuit, you need one more thing: Alaska doesn't just pick one name. Voters rank the candidates. First choice, second, third.",
   *NAMECARD(700, 300, "1st", w=220), *NAMECARD(960, 300, "2nd", w=220, at=0.25), *NAMECARD(1220, 300, "3rd", w=220, at=0.5),
   G(960, "present", "neutral", extras=LINDA, at=0.1), chapter="Part 4: Ranked choice")
sc("If nobody gets more than half the first choices, the last-place candidate is knocked out.",
   T("50%+ ?", 700, 380, 150, "navy"), G(1350, "stand", "worried", s=0.8, extras=["hair"], shirt="purple", label="last place", at=0.3), {"cross": [1350, 700, 140], "at": 0.6})
sc("Their ballots then move to each voter's next choice. Repeat, until two candidates are left, and one wins.",
   P("ballot", 500, 880, 1.0), {"arrow": [[700, 600], [1000, 600]], "at": 0.25}, P("ballot", 1200, 880, 1.0, at=0.35), {"arrow": [[1400, 600], [1650, 600]], "at": 0.5},
   P("trophy", 1780, 880, 0.8, at=0.65))
sc("You don't have to rank everyone. So if you only pick one name, and that name gets knocked out, your ballot stops counting in later rounds.",
   P("ballot", 700, 880, 1.2), T("ONLY 1 NAME", 1300, 360, 90, "dark", at=0.3), P("stopwatch", 1350, 700, 0.9, at=0.55), T("stops", 1350, 520, 70, "red", at=0.7))
sc("Here's the key point for our two Dans. A Republican voter can rank the senator first and the other Dan second, or the other way around.",
   *NAMECARD(800, 300, "1. Dan S.", w=420, color="sky"), *NAMECARD(1300, 300, "2. Daniel J.", w=420, at=0.35), G(960, "think", "happy", extras=DAVE, at=0.1))
sc("Either way, if the other Dan is eliminated, those ballots flow on to the next choice. Ranked choice was supposed to remove the spoiler effect.",
   {"arrow": [[600, 500], [1300, 500]], "color": "green"}, T("SPOILER?", 960, 300, 110, "red", at=0.3), {"cross": [960, 300, 200], "at": 0.6})
sc("The catch: that only works if voters actually rank more than one name. Otherwise a mistaken vote for the wrong Dan simply ends with him.",
   G(500, "facepalm", "tired", extras=DAVE), P("ballot", 1100, 880, 1.1, at=0.3), T("wrong Dan", 1500, 360, 90, "red", at=0.5))
sc("The senator's campaign has even posted a video explaining how to rank. Dave watched it twice. Then rewound the part with his own name in it.",
   P("tv", 1150, 780, 1.1, text="HOW TO RANK"), G(550, "type", "grin", extras=DAVE, at=0.3), P("phone", 1600, 820, 1.0, at=0.55), bg="yellow")

# PART 5: THE LAWSUIT ----------------------------------------------------------
sc("Now, the lawsuit. On Thursday, October twenty-second, the U.S. Justice Department sued the state of Alaska and its election officials in federal court.",
   G(500, "point", "neutral", **DOJ), {"arrow": [[760, 600], [1060, 600]], "at": 0.3}, P("building", 1400, 900, 0.9, text="ALASKA", at=0.4),
   chapter="Part 5: The lawsuit")
sc("Its stated goal, in its own words: quote, to protect the integrity of the twenty twenty-six Senate election in Alaska.",
   P("clipboard", 600, 860, 1.3, text="COMPLAINT"), T("\"protect the integrity\"", 1250, 380, 80, "navy", at=0.35))
sc("What does it ask? Don't certify the result if the senator loses, and if the votes for the other Dan would have changed who won.",
   {"stamp": "NO CERTIFY", "x": 560, "y": 350, "size": 70, "w": 420}, T("IF", 1250, 350, 120, "red", at=0.3), T("Dan S. loses", 1450, 500, 70, "blue", at=0.45),
   T("+ Daniel J. matters", 1450, 620, 60, "green", at=0.6))
sc("And then: investigate whether people who voted for Daniel J. Sullivan actually meant to vote for Dan S. Sullivan.",
   P("magnifier", 900, 700, 1.6), P("ballot", 1300, 880, 0.9, at=0.3), G(500, "think", "neutral", **DOJ, at=0.1))
sc("Which raises a fun puzzle. How exactly do you ask a secret ballot what it meant? Dave suggests a séance.",
   P("ballot", 800, 880, 1.2), T("???", 800, 420, 130, "purple", at=0.3), G(1400, "pointup", "grin", look=-1, extras=DAVE, at=0.5), bg="purple")
sc("The case leans on the National Voter Registration Act, specifically its findings and purposes section.",
   P("clipboard", 800, 860, 1.2, text="NVRA"), T("findings & purposes", 1300, 380, 70, "dark", at=0.35))
sc("The President said he ordered it. He told reporters, quote, I'm the one that said do it.",
   G(600, "point", "neutral", **PRES), P("speech", 1250, 420, 1.5, text="\"I'm the one that said do it\"", at=0.3))
sc("Before that, he posted that powerful legal options were being considered to remove, his words, the fraudulent Daniel J. Sullivan Junior from the ballot.",
   P("phone", 600, 820, 1.2), T("\"powerful legal options\"", 1250, 380, 70, "navy", at=0.3), G(1550, "shrug", "worried", look=-1, s=0.8, **DAN2, at=0.55))
sc("The Justice Department also points to Alaska's own election officials, who had found that the second Dan's campaign was an attempt to mislead voters.",
   G(500, "point", "neutral", **DOJ), {"arrow": [[760, 600], [1060, 600]], "at": 0.3}, G(1350, "stand", "neutral", look=-1, **ELEC, at=0.4),
   T("\"mislead\"", 1350, 300, 90, "red", at=0.6))
sc("Attorney General Todd Blanche said it was not the department's intention to, quote, improperly interfere with elections or the state certification process.",
   G(600, "stand", "neutral", extras=["tie"], shirt="grey", label="Attorney General"), T("\"not our intention\"", 1300, 380, 80, "navy", at=0.35))
sc("He said the department would be unlikely to interfere outside of, quote, extreme circumstances.",
   G(600, "shrug", "neutral", extras=["tie"], shirt="grey", label="Attorney General"), {"stamp": "EXTREME ONLY", "x": 1300, "y": 400, "size": 70, "w": 480, "at": 0.35})
sc("Note the timing. The case was filed less than two weeks before Election Day, after ballots were printed, and after tens of thousands of Alaskans had already voted early.",
   P("calendar", 500, 860, 1.0, text="NOV 3"), P("envelope", 1000, 860, 1.0, at=0.25), P("envelope", 1250, 860, 1.0, at=0.35), P("envelope", 1500, 860, 1.0, at=0.45),
   T("already voted", 1250, 380, 80, "dark", at=0.6))

# PART 6: WHAT EVERYONE SAYS ---------------------------------------------------
sc("So, the reactions. And yes, every side gets a turn at the microphone.",
   P("podium", 960, 900, 1.1), P("megaphone", 1450, 700, 1.0, at=0.3), chapter="Part 6: What they say", bg="sky")
sc("The second Dan called the lawsuit a, quote, gross misuse of the Justice Department, and said the courts had already settled it.",
   G(600, "point", "angry", **DAN2), P("speech", 1250, 420, 1.5, text="\"gross misuse\"", at=0.3))
sc("He also said the Division of Elections did, his words, a notable job of differentiating the two candidates.",
   G(600, "present", "neutral", **DAN2), *NAMECARD(1300, 360, "Dan S.  /  Daniel J.", w=620, at=0.35))
sc("Peltola's spokesperson called it a despicable political threat to overturn an election. The Democratic Senate campaign committee called it a sham.",
   G(500, "point", "angry", extras=["tie"], shirt="red", label="Peltola camp"), T("\"despicable\"", 1250, 340, 90, "red", at=0.3), T("\"sham\"", 1250, 500, 90, "red", at=0.5))
sc("The senator's own campaign kept it short: quote, we'll let the DOJ complaint run its course. It didn't say whether he supports it.",
   G(600, "shrug", "neutral", **SEN), P("speech", 1300, 420, 1.5, text="\"run its course\"", at=0.3))
sc("Alaska's other senator, Lisa Murkowski, also a Republican, said the department should never have filed this lawsuit.",
   G(600, "hips", "neutral", extras=["bun", "glasses"], shirt="blue", label="Sen. Murkowski (R)"), T("\"never\"", 1300, 380, 140, "red", at=0.35))
sc("Legal scholars are sceptical. Notre Dame law professor Derek Muller called the argument, quote, so absurdly thin, and said the court will likely dismiss it.",
   G(600, "present", "smug", extras=["glasses"], shirt="brown", label="Derek Muller"), T("\"so absurdly thin\"", 1300, 380, 80, "dark", at=0.35))
sc("Nabors, at the University of Alaska Anchorage, called federal intervention unusual, but said it could be justified if an election is run unfairly.",
   G(600, "think", "neutral", extras=["glasses", "tie"], shirt="tan", label="Forrest Nabors"), P("scale", 1300, 880, 1.2, at=0.3))
sc("And it's not the first strange Alaska Senate race. In twenty ten, Murkowski won a write-in campaign by more than ten thousand votes.",
   P("calendar", 600, 860, 1.0, text="2010"), C(0, 10000, 1250, 420, fmt="{:,.0f}+", size=190, color="navy", at=0.3), T("write-in", 1250, 600, 80, "dark", at=0.5))
sc("Two sides, then. One says: two near-identical names can trick voters, so check before you certify. The other says: the ballot is clear, the courts ruled, let the count stand.",
   P("scale", 960, 880, 1.6), T("CHECK FIRST", 500, 350, 70, "blue", at=0.3), T("COUNT STANDS", 1420, 350, 70, "red", at=0.5))
sc("We don't pick a winner here. We just count the facts.",
   P("clipboard", 960, 860, 1.3, text="FACTS"), G(500, "stand", "neutral", extras=LINDA, at=0.2), bg="paper")

# PART 7: WHAT'S NEXT -----------------------------------------------------------
sc("So what happens next? Election Day is Tuesday, November third. In Alaska, the full ranked-choice count can take weeks.",
   P("calendar", 600, 860, 1.1, text="NOV 3"), {"arrow": [[820, 640], [1180, 640]], "at": 0.3}, T("WEEKS", 1450, 420, 140, "navy", at=0.45),
   chapter="Part 7: What's next")
sc("A judge will decide whether the lawsuit goes anywhere. Muller expects it to be dismissed next month. No court has ordered Alaska to pause anything.",
   G(700, "think", "neutral", **JUDGE), P("scale", 1300, 880, 1.2, at=0.3), {"stamp": "NO ORDER", "x": 1300, "y": 330, "size": 80, "w": 360, "at": 0.6})
sc("The Justice Department can ask a court to step in. It cannot stop certification on its own.",
   G(600, "point", "neutral", **DOJ), {"cross": [1300, 500, 150], "at": 0.4}, T("on its own", 1300, 300, 80, "dark", at=0.3))
sc("And if the race isn't close? Then the whole question probably goes away. The lawsuit only matters if the other Dan's votes are bigger than the gap.",
   T("GAP", 600, 400, 160, "red"), T("vs.", 960, 400, 110, "dark", at=0.3), T("Daniel J. votes", 1400, 400, 80, "green", at=0.45))
sc("There's also a ballot question in Alaska that would repeal ranked-choice voting itself. So the counting system is on the ballot too.",
   P("ballot", 700, 880, 1.2), T("REPEAL?", 1300, 380, 120, "red", at=0.35), G(1650, "facepalm", "tired", look=-1, extras=DAVE, at=0.55))

# RECAP ------------------------------------------------------------------------
sc("Quick recap. Two men named Dan Sullivan are on Alaska's Senate ballot. One is the senator. One is a retired teacher. The courts let both run.",
   G(450, "stand", "smug", s=0.8, **SEN), G(900, "wave", "happy", s=0.8, **DAN2, at=0.2), P("scale", 1450, 880, 1.0, at=0.4), chapter="Recap", bg="paper")
sc("The Justice Department now asks a court to hold the result if the senator loses narrowly. Critics, including a Republican senator, call that wrong.",
   G(500, "point", "neutral", **DOJ), {"stamp": "HOLD?", "x": 1100, "y": 380, "size": 80, "w": 300, "at": 0.3}, G(1550, "hips", "neutral", look=-1, extras=["bun", "glasses"], shirt="blue", label="Sen. Murkowski", at=0.5))
sc("Voters decide on November third. Then the counting, and maybe the court, decide the rest.",
   P("calendar", 600, 860, 1.0, text="NOV 3"), P("ballot", 1100, 880, 1.0, at=0.3), P("scale", 1550, 880, 1.0, at=0.55))
sc("As for Dave, he's finally ranked his choices. He then filled in a name-tag for himself, just in case there's another Dave on his street.",
   G(650, "fist", "smug", extras=DAVE), *NAMECARD(1300, 360, "DAVE (the real one)", w=620, at=0.35), bg="yellow")
sc("Your turn. Should ballots add more details, like a photo or a hometown, when two candidates share a name? Tell us in the comments.",
   G(600, "think", "neutral", extras=LINDA), P("speech", 1300, 450, 1.4, text="YOUR TAKE?", at=0.35), bg="yellow")
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, at=0.4, text="SUBSCRIBE"), bg="yellow")


script = {
    "id": "ep017",
    "title": "Dan Sullivan vs. Dan Sullivan: Can a Name Stop an Election?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Alaska's 2026 U.S. Senate ballot has two candidates named Dan Sullivan: Republican Sen. Dan S. Sullivan and Daniel J. Sullivan Jr., "
        "a retired teacher from Petersburg. State election officials removed the second Dan in June; Alaska's courts put him back. "
        "Now the U.S. Justice Department has sued Alaska, asking that the result not be certified if the senator loses and votes for the other Dan "
        "could have changed the outcome. We explain the August primary numbers (Peltola 49.54%, Sen. Sullivan 41.40%, Daniel J. Sullivan 2.47%), "
        "how Alaska's ranked-choice voting works, what the lawsuit asks, and what each side says.\n\n"
        "We don't pick political sides. We just count the facts.\n\n"
        "Sources:\n"
        "Al Jazeera, Dan Sullivan vs Dan Sullivan: Why is Trump's DOJ suing in Alaska? (Oct 24, 2026): https://www.aljazeera.com/news/2026/10/24/dan-sullivan-vs-dan-sullivan-why-is-trumps-doj-suing-in-alaska\n"
        "AP via PBS NewsHour, Trump says he ordered DOJ lawsuit over Alaska Senate race (Oct 23, 2026): https://www.pbs.org/newshour/politics/trump-administration-files-lawsuit-to-block-possible-democratic-win-in-alaska-senate-race\n"
        "Alaska's News Source, Trump sues to disqualify votes for Petersburg's Dan Sullivan (Oct 23, 2026): https://www.alaskasnewssource.com/2026/10/23/trump-sues-disqualify-votes-petersburgs-dan-sullivan/\n"
        "Reason, Justice Department targets Alaska's 2026 U.S. Senate election (Oct 26, 2026): https://reason.com/2026/10/26/justice-department-targets-alaska-senate-election/\n"
        "CNBC, Blanche defends Trump-ordered lawsuit over Alaska Senate election certification (Oct 25, 2026): https://www.cnbc.com/2026/10/25/blanche-doj-alaska-senate-certification-lawsuit.html\n\n"
        "#alaska #senate #election #midterms #explained #stickfigure #news"
    ),
    "tags": ["alaska senate race", "dan sullivan", "two dan sullivans", "alaska election 2026", "mary peltola", "ranked choice voting",
             "justice department lawsuit", "midterms 2026", "election explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "TWO DAN|SULLIVANS?", "size": 190, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["hair"]}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": []},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep017.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

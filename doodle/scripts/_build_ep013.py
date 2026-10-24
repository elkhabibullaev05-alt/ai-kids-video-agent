"""Episode 13: Wedgewood Polls admits its election surveys were fabricated (Oct 20, 2026), explained with stick figures."""
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


DAVE = ["hair"]
ECON = ["glasses", "tie"]
OFF = ["tie", "briefcase"]
LINDA = ["bun"]
KEV = dict(extras=["cap"], shirt="orange")                                 # Dave's nephew, made-up character
POLL = dict(extras=["glasses", "tie"], shirt="purple")                     # generic pollster
SLEUTH = dict(extras=["glasses"], shirt="teal")                            # generic data analyst
CAND = dict(extras=["tie"], shirt="blue")                                  # generic candidate
CAND2 = dict(extras=["tie"], shirt="red")
REG = dict(extras=["tie", "briefcase"], shirt="grey")                      # generic regulator
PROF = dict(extras=["glasses", "tie"], shirt="brown")

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN --------------------------------------------------------------------
sc("Meet Kevin. Dave's nephew. Twelve years old. Kevin has opened a lemonade stand, and he has a sign.",
   P("booth", 1150, 900, 1.2, text="KEVIN'S|LEMONADE"), G(600, "present", "grin", **KEV, at=0.35),
   cam={"from": [1000, 600, 1.3], "to": [960, 540, 1.0]})
sc("The sign says: voted best lemonade in town. Ninety-seven percent approval.",
   P("booth", 700, 900, 0.9, text="KEVIN'S|LEMONADE"), C(0, 97, 1350, 380, fmt="{:.0f}%", size=230, color="green", at=0.25),
   T("BEST IN TOWN", 1350, 560, 80, "dark", at=0.55))
sc("Dave is impressed. Dave buys three cups. Then Dave asks a dangerous question: who voted?",
   G(500, "hold", "happy", extras=DAVE), T("x3", 800, 520, 110, "green", at=0.25), G(1400, "think", "confused", look=-1, extras=DAVE, at=0.55),
   T("WHO VOTED?", 1400, 330, 100, "red", at=0.7))
sc("Kevin says: I did. Ninety-seven times. The other three times I was thirsty.",
   G(650, "hips", "smug", **KEV), P("speech", 1300, 520, 1.4, text="me. 97 times.", at=0.3), G(1650, "facepalm", "tired", look=-1, extras=DAVE, s=0.8, at=0.6))
sc("Dave laughs. Kevin is twelve. Then Dave opens the news and learns that a grown-up polling company did basically the same thing.",
   G(500, "stand", "grin", extras=DAVE), P("phone", 1000, 860, 1.0, at=0.3), G(1450, "panic", "shock", look=-1, extras=DAVE, at=0.55), bg="yellow")
sc("Except its numbers ended up in the New York Times.",
   P("tv", 960, 800, 1.3, text="NEWS"), {"stamp": "FAKE", "x": 960, "y": 420, "size": 110, "w": 360, "at": 0.4}, anim="shake")
S.append({"say": "Today: how did a fake pollster fool the political world before the midterms, who did it hurt, and how do you tell a real poll from a Kevin?",
          "items": [P("tv", 980, 800, 1.4, text="FAKE POLLS?"), G(330, "think", "confused", extras=DAVE, at=0.4), P("calendar", 1650, 860, 0.7, text="NOV 3", at=0.6)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED ----------------------------------------------------------
sc("The company was called Wedgewood Polls. Since the spring, it had been publishing surveys about the big races in this year's midterm elections.",
   P("building", 650, 900, 0.9, text="WEDGEWOOD"), P("clipboard", 1150, 860, 0.8, text="POLL", at=0.3), P("clipboard", 1450, 860, 0.8, text="POLL", at=0.45),
   P("clipboard", 1750, 860, 0.8, text="POLL", at=0.6), chapter="Part 1: What happened")
sc("Senate races. Governor races. Swing states and safe states. It looked busy and serious.",
   G(600, "present", "neutral", **POLL, label="Wedgewood"), P("chart", 1300, 880, 1.1, at=0.35), T("SERIOUS.", 1300, 330, 100, "dark", at=0.6))
sc("Then, on Tuesday, October twentieth, it posted a statement. Almost all of its election surveys, it said, were fabricated.",
   P("calendar", 550, 860, 1.0, text="OCT 20"), P("laptop", 1250, 900, 1.2, text="STATEMENT", at=0.3),
   {"stamp": "FABRICATED", "x": 1250, "y": 420, "size": 80, "w": 520, "at": 0.6})
sc("Fabricated means made up. Not a bad sample. Not a wrong guess. Invented. Like Kevin, but with a logo.",
   T("FABRICATED = MADE UP", 960, 330, 100, "red"), G(600, "hips", "smug", **KEV, at=0.35), P("booth", 1350, 900, 0.8, text="KEVIN'S", at=0.55))
sc("Wedgewood called it an experimental project to show, quote, the vulnerabilities, lack of oversight, and overall low barrier to entry in the polling industry.",
   G(560, "present", "smug", **POLL, label="Wedgewood"), P("speech", 1300, 480, 1.5, text="\"experiment\"", at=0.35))
sc("It said the project was never intended to sway an election. It called it a wake-up call.",
   P("speech", 650, 500, 1.3, text="no swaying!"), P("phone", 1300, 860, 1.0, text="ALARM", anim="shake", at=0.4))
sc("It described itself as a fictional entity run by a small group of industry veterans. A pretend company, run by real people.",
   P("building", 700, 900, 0.9, text="FICTIONAL"), G(1250, "hips", "smug", **POLL, at=0.35), G(1550, "hips", "smug", **POLL, at=0.5))
sc("Their conclusion, as reported by several outlets: getting taken seriously was far too easy.",
   T("\"far too easy\"", 960, 380, 150, "red"), G(1600, "facepalm", "tired", look=-1, extras=DAVE, at=0.5))
sc("The firm's account on X has since disappeared. TIME magazine tried emailing it. The email bounced.",
   P("laptop", 700, 900, 1.1, text="ACCOUNT GONE"), P("envelope", 1350, 820, 1.0, at=0.35, move=[1600, 600]),
   {"cross": [1350, 700, 90], "at": 0.7})

# PART 2: WHERE THE NUMBERS WENT -------------------------------------------------
sc("These polls didn't stay in a corner of the internet. They travelled.",
   P("globe", 960, 820, 1.2, anim="spin"), P("clipboard", 600, 600, 0.6, text="POLL", move=[350, 450]), P("clipboard", 1300, 600, 0.6, text="POLL", at=0.3, move=[1600, 450]),
   chapter="Part 2: Where they went")
sc("According to TIME, the New York Times cited about fifteen Wedgewood polls between June and October. It has since removed them.",
   P("tv", 650, 800, 0.9, text="NYT"), C(0, 15, 1300, 380, fmt="{:.0f} polls", size=150, color="red", at=0.35), {"cross": [1300, 380, 160], "at": 0.75})
sc("Decision Desk HQ, which runs election forecasts, removed seventeen. Newsweek, Politico and MS NOW had also reported Wedgewood numbers.",
   C(0, 17, 600, 380, fmt="{:.0f}", size=200, color="red"), P("tv", 1150, 800, 0.6, text="NEWSWEEK", at=0.3), P("tv", 1450, 800, 0.6, text="POLITICO", at=0.45),
   P("tv", 1750, 800, 0.6, text="MS NOW", at=0.6))
sc("Poll averages and forecast sites had pulled them in too, including FiftyPlusOne, the Silver Bulletin, VoteHub and 270toWin.",
   P("chart", 600, 880, 0.9), P("chart", 1000, 880, 0.9, at=0.2), P("chart", 1400, 880, 0.9, at=0.4), P("chart", 1750, 880, 0.9, at=0.6), T("AVERAGES", 1150, 330, 100, "dark", at=0.3))
sc("So what did the fake polls say? Many showed Democrats doing surprisingly well in Republican-held states, according to Fox News and others.",
   P("scoreboard", 960, 900, 1.1, text="SURPRISE!"), T("?", 1500, 400, 200, "red", at=0.5))
sc("In Mississippi, Wedgewood had Republican Senator Cindy Hyde-Smith up only fifty-two to forty-eight. Trump carried the state comfortably in twenty twenty-four.",
   {"bars": {"values": [52, 48], "labels": ["Republican", "Democrat"], "colors": ["red", "blue"], "fmt": "{}%", "w": 640, "h": 440}, "x": 800, "y": 860},
   T("MISSISSIPPI", 800, 300, 80, "dark", at=0.2), {"stamp": "FAKE", "x": 1550, "y": 500, "size": 90, "w": 300, "at": 0.6})
sc("The Democrat's campaign promoted that poll, and Newsweek wrote about it. Remember: invented numbers.",
   G(600, "point", "happy", **CAND, label="a campaign"), P("megaphone", 1050, 700, 1.0, at=0.3), P("tv", 1550, 800, 0.8, text="NEWS", at=0.55))
sc("In Michigan's Senate race this month: Democrat Abdul El-Sayed ahead of Republican Mike Rogers, fifty-three to forty-seven. Also fictional.",
   {"bars": {"values": [53, 47], "labels": ["Democrat", "Republican"], "colors": ["blue", "red"], "fmt": "{}%", "w": 640, "h": 440}, "x": 800, "y": 860},
   T("MICHIGAN", 800, 300, 80, "dark", at=0.2), {"stamp": "FAKE", "x": 1550, "y": 500, "size": 90, "w": 300, "at": 0.6})
sc("In Texas, a July Wedgewood poll had Democrat James Talarico leading Ken Paxton among Hispanic voters, sixty-four to thirty.",
   C(0, 64, 650, 380, fmt="{:.0f}%", size=200, color="blue"), C(0, 30, 1250, 380, fmt="{:.0f}%", size=200, color="red", at=0.35),
   T("TEXAS", 960, 600, 90, "dark", at=0.55))
sc("Other invented surveys made Democrats look competitive in Kansas and Ohio. The only real survey, according to reports, was in Nebraska.",
   T("KANSAS", 550, 380, 90, "dark"), T("OHIO", 1000, 380, 90, "dark", at=0.25), {"cross": [770, 380, 260], "at": 0.45},
   T("NEBRASKA = REAL", 1450, 640, 70, "green", at=0.65))
sc("And the firm asked the public for money. A GoFundMe for its Nebraska polling raised five hundred dollars toward a five-thousand-dollar goal.",
   P("moneybag", 650, 880, 1.0), C(0, 500, 1250, 360, fmt="${:,.0f}", size=170, color="money", at=0.3), T("of $5,000", 1250, 520, 80, "dark", at=0.55))
sc("Dave once donated to Kevin's lemonade expansion fund. Dave would now like a word with Kevin.",
   G(600, "hips", "angry", extras=DAVE), G(1350, "shrug", "grin", look=-1, **KEV, s=0.8, at=0.35), P("wallet", 1700, 860, 0.7, at=0.55))

# PART 3: HOW IT WAS CAUGHT ------------------------------------------------------
sc("So who caught them? An election data site called FiftyPlusOne, run by analyst G. Elliott Morris.",
   P("magnifier", 960, 700, 1.4, text="?"), G(1550, "think", "neutral", look=-1, **SLEUTH, label="FiftyPlusOne"), chapter="Part 3: How it was caught")
sc("At first, FiftyPlusOne says, nothing looked unusual. It asked Wedgewood who ran it, and got two names and a methods statement.",
   G(600, "point", "neutral", **SLEUTH, label="FiftyPlusOne"), P("clipboard", 1150, 860, 0.9, text="2 NAMES", at=0.3), P("clipboard", 1500, 860, 0.9, text="METHODS", at=0.5))
sc("Pollsters leaving big firms and starting their own, sometimes paying for surveys themselves, is normal. So it was let in.",
   P("building", 600, 900, 0.8, text="BIG FIRM"), G(1050, "stand", "happy", **POLL, walk=True, at=0.25, move=[1450, 900]), P("house", 1650, 900, 0.6, at=0.5))
sc("On October fifteenth, Wedgewood handed over the raw data from a survey, which one report says was the Mississippi Senate poll.",
   P("calendar", 550, 860, 1.0, text="OCT 15"), P("laptop", 1200, 900, 1.2, text="RAW DATA", at=0.35))
sc("Raw data is the list behind the headline: every person who supposedly answered, one row each.",
   P("laptop", 700, 900, 1.2, text="1 row = 1 person"), G(1450, "think", "confused", look=-1, extras=DAVE, at=0.4))
sc("According to one account of the investigation, the respondent ID codes were checked against real records from Pollfish, the survey platform. They didn't fit.",
   P("clipboard", 600, 860, 1.0, text="IDs"), {"arrow": [[800, 650], [1150, 650]], "at": 0.3}, P("clipboard", 1350, 860, 1.0, text="PLATFORM", at=0.4),
   {"cross": [980, 500, 80], "at": 0.7})
sc("In other words, the people in the spreadsheet looked like people who had never existed.",
   G(600, "stand", "neutral", extras=DAVE), G(960, "stand", "neutral", extras=LINDA, at=0.2), G(1320, "stand", "neutral", extras=DAVE, at=0.4),
   T("NOBODY", 960, 300, 130, "red", at=0.6))
sc("On October twentieth, FiftyPlusOne asked Wedgewood to comment before publishing. Wedgewood didn't answer the question. It posted its confession instead.",
   P("envelope", 600, 820, 1.0, text="COMMENT?"), {"arrow": [[800, 640], [1150, 640]], "at": 0.3}, P("laptop", 1400, 900, 1.1, text="CONFESSION", at=0.5))
sc("And it accused the aggregators of not vetting it. FiftyPlusOne calls that claim false.",
   G(600, "point", "smug", **POLL, label="Wedgewood"), G(1350, "point", "angry", look=-1, **SLEUTH, label="FiftyPlusOne", at=0.35), T("FALSE", 1350, 300, 110, "red", at=0.6))
sc("Morris wrote that the social experiment story was a cover for fraud. Former Obama staffer Tommy Vietor called it lying and fraud.",
   T("\"cover for fraud\"", 960, 360, 120, "red"), G(400, "facepalm", "tired", **SLEUTH, at=0.4))

# PART 4: WHO GOT HURT ----------------------------------------------------------
sc("Now, did any of this matter? One candidate says it mattered a lot.",
   P("scale", 960, 900, 1.3), T("DID IT MATTER?", 960, 300, 110, "dark", at=0.3), chapter="Part 4: Who got hurt")
sc("Michigan state senator Mallory McMorrow was running in the Democratic primary for the U.S. Senate.",
   G(700, "wave", "happy", **CAND, label="a Senate candidate"), P("capitol", 1400, 900, 0.8, at=0.35))
sc("On June twenty-ninth, a Wedgewood poll gave her nine percent among registered voters.",
   P("calendar", 550, 860, 0.9, text="JUN 29"), C(0, 9, 1250, 380, fmt="{:.0f}%", size=240, color="red", at=0.3))
sc("To be fair to the numbers: real polls from other firms also had her in single digits around then, with lots of voters undecided.",
   {"bars": {"values": [9, 9, 8], "labels": ["Wedgewood", "Susquehanna", "Quantus"], "colors": ["red", "grey", "grey"], "fmt": "{}%", "w": 820, "h": 420},
    "x": 900, "y": 860}, G(1650, "think", "neutral", look=-1, extras=ECON, at=0.6))
sc("Still, McMorrow says that after the Wedgewood numbers spread, donations dried up and reporters kept asking when she'd quit.",
   P("moneybag", 600, 880, 1.0), P("arrowdown", 900, 880, 0.8, at=0.25), P("megaphone", 1400, 700, 1.0, text="QUIT?", at=0.45))
sc("She suspended her campaign on July fifth, about a month before the primary.",
   P("calendar", 600, 860, 1.0, text="JUL 5"), {"stamp": "SUSPENDED", "x": 1250, "y": 450, "size": 80, "w": 480, "at": 0.4})
sc("A strategist who ran a group backing her says donors pointed to that poll to pull money, while the campaign was outspent by eighty million dollars.",
   G(560, "present", "worried", extras=LINDA, shirt="green", label="a strategist"), C(0, 80, 1250, 380, fmt="${:.0f}M", size=190, color="red", at=0.35))
sc("McMorrow wrote that the whole thing was treated like a game, and called for a big shake-up of campaign money rules.",
   P("scoreboard", 700, 900, 0.9, text="GAME?"), G(1400, "fist", "angry", look=-1, **CAND, at=0.4))
sc("And Wedgewood wasn't the first this year. In August, a firm called Median Strategies admitted its polls were fake too, calling them a social experiment.",
   P("building", 600, 900, 0.8, text="WEDGEWOOD"), P("building", 1300, 900, 0.8, text="MEDIAN", at=0.35), T("x2", 1700, 400, 150, "red", at=0.6))
sc("Median claimed one candidate led Wisconsin's Democratic governor primary by twenty points. Her rival actually won, by a razor-thin margin.",
   C(0, 20, 700, 380, fmt="+{:.0f}", size=220, color="red"), T("REAL: razor-thin", 1350, 420, 80, "dark", at=0.45), {"cross": [700, 380, 150], "at": 0.7})
sc("It also claimed Los Angeles mayor Karen Bass led by twelve points, from five hundred sixty residents. In the real primary she led by five.",
   C(0, 12, 650, 360, fmt="+{:.0f}", size=200, color="red"), C(0, 5, 1300, 360, fmt="+{:.0f}", size=200, color="green", at=0.4),
   T("FAKE", 650, 520, 70, "red", at=0.2), T("REAL", 1300, 520, 70, "green", at=0.5))

# PART 5: WHY IT'S SO EASY ------------------------------------------------------
sc("So how is it this easy? First, quick lesson: how a real poll works.",
   P("chalkboard", 960, 900, 1.2, text="HOW POLLS|WORK"), chapter="Part 5: Why it's so easy")
sc("You can't ask every voter. So you ask a sample, maybe several hundred to a thousand people, chosen to look like the whole state.",
   P("cart", 600, 900, 0.9), G(1000, "stand", "neutral", s=0.5, at=0.2), G(1150, "stand", "happy", extras=LINDA, s=0.5, at=0.3),
   G(1300, "stand", "neutral", extras=DAVE, s=0.5, at=0.4), G(1450, "stand", "worried", extras=ECON, s=0.5, at=0.5))
sc("Then you add a margin of error, the wiggle room. Median's fake LA poll even came with one: four point one percent. Very official.",
   T("+/- 4.1%", 960, 380, 190, "dark"), {"stamp": "VERY OFFICIAL", "x": 1450, "y": 640, "size": 60, "w": 440, "at": 0.5})
sc("Here's the problem. A finished poll is just a few numbers and a nice chart. Anyone with a laptop can make a nice chart.",
   P("laptop", 700, 900, 1.2, text="%%%"), P("chart", 1300, 880, 1.1, at=0.35), G(1700, "type", "smug", look=-1, **KEV, s=0.8, at=0.55))
sc("Aggregators can check methods and track records, but a brand new firm has no record yet. They mostly have to trust what they're told.",
   G(600, "shrug", "worried", **SLEUTH, label="an aggregator"), P("building", 1300, 900, 0.8, text="NEW FIRM", at=0.35), T("TRUST?", 1300, 320, 100, "red", at=0.6))
sc("And polls aren't just scores. Researchers say they change behaviour. A twenty twenty-three study found polls demobilize the minority and mobilize the majority.",
   G(560, "present", "neutral", **PROF, label="researchers"), P("arrowdown", 1150, 880, 0.8, at=0.35), P("arrowup", 1500, 880, 0.8, at=0.5))
sc("Translation: if you think your side is losing, you might stay home. If you think it's winning, you show up.",
   P("house", 600, 900, 0.8), G(900, "cry", "sad", s=0.7, at=0.2), P("ballot", 1350, 880, 1.0, at=0.45), G(1650, "fist", "happy", extras=DAVE, s=0.7, at=0.6))
sc("A nineteen ninety-six experiment found people shown a made-up poll before a primary were more likely to back the candidate it favoured.",
   P("calendar", 560, 860, 0.9, text="1996"), P("clipboard", 1050, 860, 0.9, text="FAKE POLL", at=0.3), {"arrow": [[1250, 640], [1500, 640]], "at": 0.5},
   P("ballot", 1650, 880, 0.9, at=0.6))
sc("Donors read polls too. Reporters build stories on them. One bad number can decide who gets money, airtime, and the dreaded question: are you dropping out?",
   P("moneybag", 500, 880, 0.9), P("tv", 960, 800, 0.8, text="AIRTIME", at=0.3), P("megaphone", 1450, 700, 1.0, text="DROPPING OUT?", at=0.55))

# PART 6: WHAT BOTH SIDES SAY ---------------------------------------------------
sc("So what are officials saying? This one, at least, upset people in both parties, though not always about the same thing.",
   G(600, "point", "angry", **CAND, label="Democrats"), G(1350, "point", "angry", look=-1, **CAND2, label="Republicans", at=0.3), chapter="Part 6: What they say")
sc("Notice the pattern: many fake polls flattered Democrats in red states, but the most damaging one, by her account, hurt a Democrat.",
   P("scale", 960, 900, 1.3, anim="bob"), T("HELPED?", 600, 330, 90, "blue", at=0.3), T("HURT?", 1350, 330, 90, "blue", at=0.5))
sc("The chair of the Federal Communications Commission, Republican Brendan Carr, pointed to a significant surge in fake polls, without naming cases.",
   G(600, "present", "neutral", **REG, label="FCC chair (R)"), T("\"significant surge\"", 1300, 400, 90, "red", at=0.35))
sc("He blamed news outlets for airing them without regard, he said, to basic journalistic ethics.",
   P("tv", 960, 800, 1.2, text="NEWS"), {"cross": [960, 650, 140], "at": 0.5})
sc("Democratic commissioner Anna Gomez answered: pollsters who intentionally mislead the public should answer for it.",
   G(600, "point", "neutral", **REG, label="FCC commissioner (D)"), P("speech", 1300, 500, 1.4, text="answer for it", at=0.35))
sc("But she added that broadcasters reporting polls in good faith shouldn't be punished when a poll turns out wrong.",
   P("tv", 700, 800, 1.0, text="GOOD FAITH"), P("scale", 1350, 900, 1.0, at=0.4))
sc("Democratic strategist Mike Nellis told Fox News the people responsible should be prosecuted, and asked whether donors would get their money back.",
   G(600, "fist", "angry", extras=ECON, shirt="blue", label="a strategist"), P("moneybag", 1300, 880, 1.0, at=0.4), T("REFUND?", 1300, 560, 90, "green", at=0.5))
sc("Decision Desk HQ, for its part, said removing its seventeen fake polls didn't change its Senate and House forecasts at all.",
   P("chart", 700, 880, 1.1), {"stamp": "NO CHANGE", "x": 1300, "y": 450, "size": 90, "w": 440, "at": 0.4})
sc("Michael Traugott, a former president of the polling researchers' association, called two cases in such a short time very troubling.",
   G(600, "think", "worried", **PROF, label="polling researcher"), T("x2 = troubling", 1300, 400, 100, "red", at=0.4))
sc("So one side stresses the media. Another stresses the fraudsters. Everyone stresses the polls. We just count the facts.",
   T("MEDIA", 500, 380, 90, "dark"), T("FRAUDSTERS", 960, 380, 90, "dark", at=0.25), T("POLLS", 1420, 380, 90, "dark", at=0.5),
   P("clipboard", 960, 860, 0.9, text="FACTS", at=0.7))

# PART 7: HOW TO READ A POLL ----------------------------------------------------
sc("The midterms are on November third. You'll see a lot of polls before then. So here's Linda's practical guide to not getting Kevined.",
   P("calendar", 550, 860, 1.0, text="NOV 3"), G(1300, "present", "neutral", extras=LINDA, at=0.35), chapter="Part 7: Don't get Kevined")
sc("Rule one: never trust one poll. Look at the average of many. One wild poll is usually just a wild poll.",
   P("clipboard", 600, 860, 0.8, text="1"), {"cross": [600, 700, 110], "at": 0.3}, P("chart", 1250, 880, 1.2, text="AVG", at=0.5))
sc("Rule two: who did the poll? Have you heard of them? Do they have a track record from past elections?",
   P("magnifier", 700, 700, 1.2, text="WHO?"), P("calendar", 1350, 860, 0.8, text="PAST", at=0.4))
sc("Rule three: does it say how many people, how they were reached, and the margin of error? No details, no trust.",
   P("clipboard", 600, 860, 0.9, text="HOW MANY?"), P("phone", 1100, 860, 0.8, at=0.3), T("+/- ?", 1550, 420, 120, "dark", at=0.5))
sc("Rule four: if a poll is exactly what your side was hoping for, be extra suspicious. That goes for every side.",
   G(700, "fist", "happy", extras=DAVE), T("TOO GOOD?", 1300, 380, 110, "red", at=0.4))
sc("Rule five: remember that even honest polls can miss. Polls struggle to measure turnout and enthusiasm, and in tight races they can pick the wrong winner.",
   G(600, "shrug", "neutral", extras=ECON, label="Pew Research"), P("ballot", 1300, 880, 1.0, at=0.35), T("?", 1600, 420, 180, "red", at=0.55))
sc("Polls are a weather forecast, not the weather. The only poll that counts is the one on election day.",
   P("cloud", 700, 450, 1.0), P("sun", 1000, 400, 0.8, at=0.2), {"arrow": [[1150, 600], [1350, 600]], "at": 0.4}, P("ballot", 1550, 880, 1.2, at=0.55))

# RECAP --------------------------------------------------------------------------
sc("Recap. A firm called Wedgewood Polls admitted on October twentieth that almost all its election surveys were made up.",
   P("building", 700, 900, 0.8, text="WEDGEWOOD"), {"stamp": "MADE UP", "x": 1300, "y": 450, "size": 90, "w": 420, "at": 0.35}, chapter="Recap")
sc("Its numbers reached the New York Times and forecast sites, which have pulled them, and one Senate candidate says they helped end her campaign.",
   P("tv", 650, 800, 0.8, text="NYT"), P("chart", 1100, 880, 0.9, at=0.3), G(1550, "cry", "sad", **CAND, at=0.55))
sc("Both parties' officials are angry, just at different people. And everyone is checking their polls a lot more carefully.",
   G(600, "point", "angry", **REG), G(1350, "point", "angry", look=-1, **REG, at=0.3), P("magnifier", 960, 600, 1.0, at=0.55))
sc("Back at the stand, Kevin has updated his sign. It now says: ninety-seven percent approval. Source: Kevin. Sample size: Kevin.",
   P("booth", 1000, 900, 1.2, text="SOURCE: KEVIN|SAMPLE: 1"), G(450, "hips", "grin", **KEV, at=0.3), G(1600, "facepalm", "tired", look=-1, extras=DAVE, at=0.55))
sc("Dave says that's the most honest poll he's seen all week. He buys another lemonade.",
   G(700, "hold", "happy", extras=DAVE), P("dollar", 1250, 760, 0.9, at=0.3), G(1550, "wave", "grin", look=-1, **KEV, s=0.8, at=0.5))
sc("Your turn. Do you still trust election polls? More, less, or never did? Tell us in the comments. We read them all. All ninety-seven.",
   P("tv", 980, 800, 1.3, text="COMMENTS"), G(330, "point", "grin", extras=DAVE, at=0.4), T("?", 1650, 400, 200, "red", at=0.6))
sc("If this helped, subscribe for calm, stick-figure news, twice a week or more. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, text="SUBSCRIBE", at=0.4), bg="yellow")

script = {
    "id": "ep013",
    "title": "Why Did a Pollster Fake Its Own Polls?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On October 20, 2026, Wedgewood Polls admitted that almost all of its election surveys were fabricated, calling it an \"experimental project\" "
        "to expose the low barrier to entry in political polling. Its numbers had been cited by the New York Times (about 15 polls, now removed), "
        "Decision Desk HQ (17 removed), Newsweek, Politico and poll aggregators. We go through what happened, where the fake numbers went, "
        "how the election-data site FiftyPlusOne caught it, who says they were hurt (Michigan Senate candidate Mallory McMorrow), the earlier "
        "Median Strategies case, why fake polls are so easy to make, what officials in both parties said, and five rules for reading polls before the Nov 3 midterms.\n\n"
        "Kevin, Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported. "
        "We don't take sides: we just count the facts.\n\n"
        "Sources:\n"
        "TIME, How a Fake Pollster May Have Hurt Real Candidates (Oct 23, 2026): https://time.com/article/2026/10/23/what-fake-wedgewood-polls-scandal-reveals-about-election-polling/\n"
        "Fox News, Wedgewood Polling admits fabricating data as Democrats erupt: https://www.foxnews.com/politics/democrats-furious-pollster-boosting-far-left-candidates-admits-fabricating-surveys-absolute-scumbags\n"
        "FiftyPlusOne, FiftyPlusOne just caught a pollster faking data: https://blog.fiftyplusone.news/p/fiftyplusone-just-caught-a-pollster\n"
        "Hungarian Conservative, Wedgewood Admits Fabricating Polls (Oct 21, 2026): https://www.hungarianconservative.com/articles/current/wedgewood-polling-fake-social-experiment-midterm/\n"
        "The National Desk, Polling firm closes after releasing fake election surveys for 'social experiment': https://okcfox.com/news/nation-world/polling-firm-closes-after-releasing-fake-election-surveys-for-social-experiment-los-angeles-mayoral-race-wisconsin-democratic-gubernatorial-primary-karen-bass-francesca-hong\n\n"
        "#polls #midterms #election2026 #explained #stickfigure #news"
    ),
    "tags": ["fake polls", "wedgewood polls", "polling scandal", "midterms 2026", "election polls", "how polls work", "fiftyplusone",
             "median strategies", "mallory mcmorrow", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "THE POLLS|LIED?", "size": 210, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["hair"]}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": []},
    "scenes": [s for s in S if s],
}
_CYC = ["paper", "sky", "paper", "teal", "paper", "purple"]
for _i, _s in enumerate(script["scenes"]):
    if _s.get("bg") not in ("yellow", "sky"):
        _s["bg"] = _CYC[_i % len(_CYC)]
for s in script["scenes"]:
    for it in list(s["items"]):
        g = it.get("guy")
        if g and g.get("label"):
            sz = it.get("s", 1.0)
            s["items"].append({"text": g.pop("label"), "x": it["x"], "y": it.get("y", 900) - int(430 * sz), "size": 44,
                               "color": "dark", "at": it.get("at", 0)})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep013.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

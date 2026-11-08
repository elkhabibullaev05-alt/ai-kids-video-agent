"""Episode 22: East Texas A&M 68-64 Oklahoma (Nov 2, 2026, 28.5-pt underdog) and Valparaiso 83-80 Purdue 2OT (Nov 6, 2026): underdogs vs college basketball money."""
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
OU = dict(shirt="red")            # generic Oklahoma player
ET = dict(shirt="blue")           # generic East Texas A&M player
PU = dict(shirt="dark")           # generic Purdue player
VA = dict(shirt="gold")           # generic Valparaiso player
COACH = dict(extras=["tie"], shirt="grey")
REF = dict(extras=["cap"], shirt="white")

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


def BALL(x, y=900, s=0.6, at=0, **kw):
    return P("basketball", x, y, s, at=at, **kw)


def HOOP(x, s=1.0, at=0, **kw):
    return P("hoop", x, 900, s, at=at, **kw)


def SCORE(text, x=960, y=760, s=1.1, at=0):
    return P("scoreboard", x, y, s, text=text, at=at)


def TEAM(x0, x1, kind, face="happy", pose="fist", n=4, s=0.55, at=0):
    out = []
    step = (x1 - x0) // max(1, n - 1)
    for i in range(n):
        out.append(G(x0 + i * step, pose, face, look=1 if i % 2 else -1, s=s, at=(at + 0.04 * i) if at < 1 else at, **kind))
    return out


# COLD OPEN ------------------------------------------------------------------
sc("Two overtimes. Four seconds left. About fifteen thousand Purdue fans, and one kid from a school they barely knew was on the schedule.",
   HOOP(1500, 1.0), G(700, "hold", "neutral", **VA, label="Valparaiso"), BALL(800, 640, 0.4, at=0.2), P("stopwatch", 300, 860, 0.7, text="0:04", at=0.5), bg="yellow")
sc("He shoots from way out by the right sideline, over a taller defender. The buzzer goes. Then a referee goes to look at a replay.",
   G(500, "pointup", "worried", **VA), G(800, "fist", "angry", look=-1, s=1.15, **PU), BALL(1200, 420, 0.45, at=0.2, move=[1500, 360]), HOOP(1600, 0.9, at=0.1), P("tv", 300, 880, 0.6, text="REVIEW", at=0.7))
sc("The ball left his hand a split second before time ran out. Valparaiso eighty-three, Purdue eighty.",
   SCORE("VALPO 83|PURDUE 80"), {"stamp": "GOOD", "x": 1550, "y": 330, "size": 80, "w": 300, "at": 0.55}, bg="yellow")
sc("And four days earlier, a school picked to finish last in its league had gone into Oklahoma and done something even less likely.",
   P("calendar", 500, 860, 0.9, text="4 DAYS"), {"arrow": [[700, 640], [1100, 640]], "color": "red", "at": 0.3}, T("LAST?", 1400, 450, 160, "red", at=0.5))
S.append({"say": "So here's today's question. How does a team nobody picked beat a giant with more money, more size and a home crowd, twice in one week?",
          "items": [G(450, "shrug", "smug", s=0.8, **ET), G(700, "shrug", "smug", s=0.8, **VA, at=0.1), T("vs", 1000, 500, 120, "red", at=0.3),
                    G(1450, "panic", "shock", s=1.4, **OU, at=0.4), T("?", 1750, 300, 200, "red", at=0.7)],
          "chapter": "Today's question"})
sc("And by the end, we'll answer the bigger one. Does all that money even guarantee a win in college basketball? Spoiler: it guarantees a lot of things.",
   P("moneybag", 600, 900, 1.1), T("= WIN?", 1100, 520, 150, "navy", at=0.3), G(1550, "think", "confused", look=-1, extras=ECON, at=0.5))

# PART 1: MONDAY IN NORMAN ---------------------------------------------------
sc("Let's start on Monday, November second. Lloyd Noble Center, Norman, Oklahoma. Season opener.",
   P("calendar", 500, 860, 1.0, text="NOV 2"), P("building", 1250, 900, 1.1, text="NORMAN, OK", at=0.3), chapter="Part 1: Monday in Norman")
sc("Home team: Oklahoma, from the Southeastern Conference, the league that basically runs college sports' money machine.",
   *TEAM(350, 950, OU, face="smug", pose="hips"), P("moneybag", 1450, 900, 1.2, text="SEC", at=0.4))
sc("Visitors: East Texas A&M, the Lions. In the Southland Conference's preseason poll, they were ranked twelfth. Out of twelve.",
   *TEAM(350, 950, ET, face="neutral", pose="stand"), C(1, 12, 1450, 430, fmt="#{:.0f}", size=220, color="red", at=0.3), T("of 12", 1450, 620, 80, "dark", at=0.5))
sc("The betting line made Oklahoma a twenty-eight and a half point favorite. That's not a prediction of a close game. That's a prediction of a polite blowout.",
   C(0, 28.5, 700, 430, fmt="{:.1f}", size=240, color="navy"), T("points", 700, 620, 80, "dark", at=0.2), G(1400, "shrug", "smug", look=-1, extras=ECON, at=0.4))
sc("Quick lesson. A point spread is the bookmakers' guess at the gap. Bet on Oklahoma, and they had to win by twenty-nine for you to collect.",
   P("chalkboard", 800, 880, 1.0, text="WIN BY 29"), G(1400, "present", "neutral", look=-1, extras=ECON, label="the Economist", at=0.3), bg="sky")
sc("Then the game started, and East Texas A&M took a thirteen to twelve lead with twelve fifty-nine left in the first half.",
   P("stopwatch", 500, 860, 0.8, text="12:59"), SCORE("LIONS 13|OU 12", 1200, 760, 1.0, at=0.3))
sc("According to the Associated Press, they never trailed again. For more than thirty minutes.",
   C(0, 30, 800, 430, fmt="{:.0f}+ min", size=200, color="blue"), T("never behind", 800, 620, 80, "dark", at=0.3), G(1450, "fist", "grin", look=-1, **ET, at=0.5))
sc("Oklahoma tied it at fifty-eight, and again at sixty with two minutes fifty-one to go. Oklahoma fans' pulses went back to normal.",
   SCORE("60 - 60"), P("stopwatch", 400, 860, 0.7, text="2:51", at=0.2), G(1550, "stand", "happy", look=-1, **OU, at=0.5))
sc("They should not have. With three seconds left, Bo Aldridge made two free throws to seal it. Sixty-eight, sixty-four.",
   G(600, "hold", "neutral", **ET, label="Bo Aldridge"), BALL(720, 640, 0.4), HOOP(1250, 0.9), SCORE("LIONS 68|OU 64", 1650, 500, 0.7, at=0.6))
sc("Aldridge finished with twenty-two points on eight of twelve shooting. Mohamed Diakite and Alonzo Dodd added fifteen each.",
   {"bars": {"values": [22, 15, 15], "labels": ["Aldridge", "Diakite", "Dodd"], "colors": ["blue", "teal", "teal"], "fmt": "{}", "w": 760, "h": 420}, "x": 960, "y": 860})
sc("How rare is this? ESPN looked at point spreads for more than one hundred thousand Division One games over thirty years.",
   C(0, 100000, 960, 420, fmt="{:,.0f}+", size=200, color="navy"), T("games checked", 960, 610, 80, "dark", at=0.3), P("magnifier", 1600, 900, 0.8, at=0.4))
sc("This was the second-largest upset in that whole span. Only one was bigger: Eastern Illinois over Iowa in twenty twenty-two, as a thirty and a half point underdog.",
   {"bars": {"values": [30.5, 28.5], "labels": ["EIU 2022", "Lions 2026"], "colors": ["grey", "blue"], "fmt": "{}", "w": 680, "h": 420}, "x": 750, "y": 860},
   {"stamp": "#2 EVER*", "x": 1500, "y": 400, "size": 80, "w": 360, "at": 0.6}, bg="yellow")
sc("It was also, by a mile, the biggest win in East Texas A&M's program history. And it ended Oklahoma's thirty-game home winning streak outside its conference.",
   P("trophy", 600, 900, 1.2, at=0), C(30, 0, 1300, 430, fmt="{:.0f}", size=220, color="red", at=0.3, dur=2.0), T("home streak", 1300, 620, 80, "dark", at=0.4))
sc("Oklahoma's coach, Porter Moser, didn't dodge it. He told reporters: The only thing I know to do is apologize to the fan base and get better.",
   G(700, "stand", "sad", **COACH, label="OU coach"), P("speech", 1250, 700, 1.0, text="SORRY, FANS", at=0.3))
sc("He also said: It was not good enough, and that's on me. You can debate a lot of things in sport. That's a pretty rare sentence.",
   G(700, "facepalm", "tired", **COACH), T("\"that's on me\"", 1300, 450, 100, "navy", at=0.3))
sc("And the winning coach, Jaret von Rosenberg, said the scary part out loud: that's not the best this team can play.",
   G(700, "fist", "grin", **COACH, label="Lions coach"), P("speech", 1250, 700, 1.0, text="NOT OUR BEST", at=0.3), G(1650, "panic", "shock", look=-1, s=0.8, **OU, at=0.6))

# PART 2: FRIDAY IN WEST LAFAYETTE -------------------------------------------
sc("Now, Friday, November sixth. Mackey Arena, West Lafayette, Indiana. Purdue, of the Big Ten, against Valparaiso of the Missouri Valley Conference.",
   P("calendar", 450, 860, 0.9, text="NOV 6"), P("building", 1050, 900, 1.0, text="MACKEY", at=0.2), T("BIG TEN vs MVC", 1500, 330, 90, "dark", at=0.5),
   chapter="Part 2: Friday in West Lafayette")
sc("Some history first. Valparaiso had not beaten Purdue since nineteen sixty-five. That's sixty-one years ago.",
   C(1965, 2026, 800, 430, fmt="{:.0f}", size=240, color="navy", dur=2.5), P("tv", 1450, 880, 0.9, text="1965", at=0.4))
sc("They had also lost nineteen straight games to Big Ten teams, across twenty-two seasons. Their last Big Ten win was over Penn State in two thousand four.",
   C(0, 19, 700, 430, fmt="{:.0f}", size=240, color="red"), T("straight losses", 700, 620, 70, "dark", at=0.2), P("calendar", 1400, 860, 0.9, text="2004", at=0.5))
sc("And Purdue had not lost at home to a Missouri Valley team since November twenty-seventh, nineteen seventy-eight. Against Indiana State and a young Larry Bird.",
   P("calendar", 600, 860, 1.0, text="1978"), {"arrow": [[800, 640], [1200, 640]], "color": "red", "at": 0.3}, T("48 years", 1450, 450, 130, "red", at=0.5))
sc("For the first half, history looked very comfortable. Purdue went up nineteen to four.",
   SCORE("PURDUE 19|VALPO 4"), G(1600, "hips", "smug", look=-1, **PU, at=0.5))
sc("At halftime, thirty-two to twenty. Valpo were down fifteen at one point. Dave, watching at home, turned the channel to a cooking show.",
   SCORE("32 - 20", 700, 760, 0.9), G(1300, "stand", "tired", look=-1, extras=DAVE), P("tv", 1600, 880, 0.7, text="COOKING", at=0.5))
sc("Dave made a mistake. Valparaiso came all the way back, and a Justus McNair jumper with a minute and three seconds left tied it at fifty-eight.",
   G(600, "pointup", "grin", **VA, label="McNair"), SCORE("58 - 58", 1300, 760, 1.0, at=0.3), P("stopwatch", 1700, 860, 0.6, text="1:03", at=0.5))
sc("Overtime one. Purdue led sixty-eight to sixty-two with seventy-three seconds left. In basketball terms, that's usually a nap.",
   SCORE("PURDUE 68|VALPO 62"), P("stopwatch", 400, 860, 0.7, text="1:13", at=0.3), T("zzz", 1600, 400, 120, "grey", at=0.5, anim="bob"))
sc("Then Bruno Alocen's three-point play cut it to one. Purdue made two free throws. And Rakim Chaney hit a three to tie it at seventy.",
   SCORE("70 - 70"), G(450, "fist", "grin", **VA, label="Chaney", at=0.3), BALL(1600, 500, 0.5, at=0.5, move=[1700, 380]))
sc("Overtime two. JT Pettigrew's three put Valpo up eighty to seventy-eight with under twenty-five seconds left.",
   SCORE("VALPO 80|PURDUE 78"), P("stopwatch", 400, 860, 0.7, text="0:24.7", at=0.3))
sc("Purdue's Daniel Jacobsen answered with a jumper with four point four seconds left. Eighty all. Mackey Arena exhales.",
   G(700, "fist", "happy", s=1.15, **PU, label="Jacobsen"), SCORE("80 - 80", 1350, 760, 1.0, at=0.3), P("stopwatch", 1750, 860, 0.5, text="0:04.4", at=0.5))
sc("By now, Chaney had fouled out after a career-best thirty-five points. So after a timeout, the last shot went to McNair.",
   C(0, 35, 700, 430, fmt="{:.0f} pts", size=200, color="gold"), T("fouled out", 700, 620, 80, "red", at=0.3), G(1450, "stand", "worried", look=-1, **VA, at=0.5))
sc("And you know the rest. Three-pointer, buzzer, replay, good. McNair finished with seventeen.",
   HOOP(1300, 1.0), BALL(700, 500, 0.5, move=[1300, 380]), {"stamp": "GOOD", "x": 600, "y": 300, "size": 80, "w": 300, "at": 0.6}, bg="yellow")
sc("Purdue fell to oh and two. According to Field Level Media, that's its first oh and two start since the nineteen seventy-six season.",
   SCORE("0 - 2"), P("calendar", 1500, 860, 0.9, text="1976", at=0.4))
sc("The NCAA's own website found the best detail. About twenty years ago, Valpo's coach Roger Powell prayed with friends who were hoping to have a baby.",
   G(600, "stand", "happy", **COACH, label="Valpo coach"), P("house", 1300, 900, 1.0, at=0.3), T("~2006", 1300, 380, 110, "navy", at=0.5))
sc("That baby was Justus McNair. After the game, Powell said: I was praying for this win I guess all the way back then.",
   G(600, "fist", "grin", **COACH), G(1100, "wave", "happy", **VA, label="McNair", at=0.3), P("speech", 1550, 650, 0.8, text="20 YEARS", at=0.5))
sc("McNair's dad called it destiny. We count facts here, not destinies, so let's go count the money.",
   G(700, "shrug", "smug", extras=LINDA, label="Linda"), P("moneybag", 1300, 900, 1.0, at=0.4))

# PART 3: THE MONEY GAP -------------------------------------------------------
sc("Here's the backdrop. College sports changed a lot recently, and the biggest change was a court settlement called House versus the NCAA.",
   P("scale", 960, 900, 1.2), T("HOUSE v. NCAA", 960, 330, 110, "navy", at=0.3), chapter="Part 3: The money gap")
sc("Since the twenty twenty-five season, schools can pay athletes directly. Front Office Sports reported the cap was twenty point five million dollars per school, per year.",
   C(0, 20.5, 960, 430, fmt="${:.1f}M", size=220, color="money"), T("per school, per year", 960, 620, 80, "dark", at=0.3), P("moneybag", 1650, 900, 0.8, at=0.5))
sc("That's across the whole athletic department, and it rises every year. Most big schools planned to give seventy to seventy-five percent of it to football.",
   {"bars": {"values": [75, 25], "labels": ["football", "everyone else"], "colors": ["brown", "grey"], "fmt": "{}%", "w": 640, "h": 400}, "x": 750, "y": 860},
   P("football", 1500, 900, 0.9, at=0.5))
sc("Power conference schools, like Oklahoma and Purdue, had to take part. Everyone else could choose. Three hundred and ten schools opted in for the first year.",
   C(0, 310, 960, 430, fmt="{:.0f}", size=240, color="navy"), T("schools opted in", 960, 630, 80, "dark", at=0.3))
sc("So how much do East Texas A&M and Valparaiso spend on their players? We looked. We couldn't find a reliable number, so we won't make one up.",
   P("magnifier", 700, 900, 1.0), T("? ? ?", 1300, 450, 160, "grey", at=0.3), G(1650, "point", "neutral", look=-1, extras=LINDA, at=0.5))
sc("What we can say: they are not in the SEC or the Big Ten, the two richest leagues, and their games don't come with the same TV money.",
   P("tv", 600, 880, 1.0, text="SEC / BIG TEN"), P("tv", 1350, 880, 0.6, text="MVC", at=0.3), P("arrowdown", 1650, 880, 0.6, at=0.5))
sc("Which is exactly why these games exist. The giant wants a home game it should win. The small school gets a trip, a payday, and a lottery ticket.",
   P("building", 600, 900, 1.0), P("moneybag", 1100, 900, 0.8, at=0.3), P("pricetag", 1550, 880, 0.8, text="TICKET", at=0.5))
sc("Usually, the lottery ticket loses. This week, two of them paid out.",
   P("pricetag", 700, 880, 1.0, text="WIN!"), P("pricetag", 1200, 880, 1.0, text="WIN!", at=0.3), bg="yellow")

# subscribe line (value)
sc("Quick pause. If you like the news drawn, counted and explained without anyone yelling, subscribe.",
   G(960, "wave", "happy", extras=DAVE), T("SUBSCRIBE", 960, 330, 120, "red", at=0.3))

# PART 4: HOW DOES THE SMALL TEAM WIN? ----------------------------------------
sc("So, how does the small team actually win? Let's look at what the numbers in these two games say.",
   T("HOW?", 960, 420, 220, "red"), G(1500, "think", "confused", look=-1, extras=ECON), chapter="Part 4: How the little team wins")
sc("Reason one: the three-point line. In Norman, East Texas A&M hit forty-one percent from three. Oklahoma hit twenty-five.",
   {"bars": {"values": [41, 25], "labels": ["Lions", "Oklahoma"], "colors": ["blue", "red"], "fmt": "{}%", "w": 640, "h": 420}, "x": 750, "y": 860},
   T("3PT", 1500, 400, 140, "navy", at=0.5))
sc("In West Lafayette, Purdue made five of twenty-eight threes. And one of fifteen across the second half and both overtimes.",
   C(0, 5, 700, 430, fmt="{:.0f} / 28", size=200, color="dark"), C(0, 1, 1350, 430, fmt="{:.0f} / 15", size=200, color="red", at=0.4), T("2nd half + OT", 1350, 620, 70, "dark", at=0.5))
sc("A three is worth fifty percent more than a two. So if the little team gets hot and the big team goes cold, a twenty-point gap can shrink fast.",
   T("3 > 2", 700, 450, 200, "navy"), {"arrow": [[1100, 450], [1500, 450]], "color": "red", "at": 0.3}, T("-20", 1700, 450, 140, "red", at=0.5))
sc("The Economist calls this variance. Dave calls it the ball going in. They're describing the same thing.",
   G(600, "present", "neutral", extras=ECON, label="variance"), G(1350, "fist", "grin", look=-1, extras=DAVE, label="ball go in", at=0.3), bg="sky")
sc("Reason two: free throws and mistakes. Moser said his team had fifteen turnovers and fifteen missed free throws.",
   C(0, 15, 700, 430, fmt="{:.0f}", size=220, color="red"), T("turnovers", 700, 620, 70, "dark", at=0.2), C(0, 15, 1300, 430, fmt="{:.0f}", size=220, color="red", at=0.4), T("missed FTs", 1300, 620, 70, "dark", at=0.5))
sc("Oklahoma made only fifty-three percent of its free throws. Those are the shots with nobody guarding you, nobody moving, and a crowd on your side.",
   C(0, 53, 800, 430, fmt="{:.0f}%", size=240, color="red"), HOOP(1450, 0.8, at=0.3), G(1650, "stand", "worried", look=-1, s=0.7, **OU, at=0.5))
sc("Reason three: the calendar. Both upsets came in the first week, when teams are still figuring each other out. Depending on who you ask, that matters a lot.",
   P("calendar", 700, 860, 1.0, text="WEEK 1"), T("?", 1250, 450, 180, "red", at=0.3), G(1600, "shrug", "neutral", look=-1, extras=ECON, at=0.5))
sc("Others say it barely matters, and that a twenty-eight point favorite should win in week one, week ten, or on a Tuesday in a parking lot.",
   G(600, "hips", "angry", extras=LINDA), P("car", 1300, 900, 0.9, at=0.3), T("STILL WIN", 1300, 400, 110, "dark", at=0.5))
sc("Oklahoma's coach mostly agreed with that second group. He said they played on their heels all night, and should have found a way to win.",
   G(700, "stand", "sad", **COACH, label="OU coach"), P("speech", 1250, 700, 1.0, text="SHOULD HAVE", at=0.3))
sc("And reason four, the boring one: the small teams were good. Not lucky-for-a-minute good. Forty minutes, and in Valpo's case fifty, good.",
   C(0, 50, 900, 430, fmt="{:.0f} min", size=220, color="gold"), T("2 overtimes", 900, 620, 70, "dark", at=0.3), *TEAM(1350, 1750, VA, n=3, s=0.5, at=0.4))
sc("Money buys height, depth and the right to host. It doesn't make the ball go through the hoop. Somebody still has to do that.",
   P("moneybag", 500, 900, 1.0), {"cross": [1100, 650, 140], "at": 0.3}, BALL(1100, 720, 0.6), HOOP(1600, 0.8, at=0.4))

# PART 5: WHO IT HITS ---------------------------------------------------------
sc("Who does this hit? Oklahoma lost a season opener for only the second time in twenty-four seasons. Purdue is oh and two before Thanksgiving.",
   C(0, 2, 700, 430, fmt="{:.0f}", size=240, color="red"), T("in 24 seasons", 700, 620, 70, "dark", at=0.3), SCORE("PURDUE 0-2", 1450, 760, 0.8, at=0.5), chapter="Part 5: Who it hits")
sc("McNair's mom said it would be a night she wouldn't go to sleep. That might be the most accurate sports quote of the year.",
   G(700, "wave", "happy", extras=LINDA, shirt="gold", label="a mom"), T("zzz? NO", 1350, 450, 120, "navy", at=0.3))
sc("And for Dave? Dave had bet his office pool on the favorites. Dave is now buying coffee for the entire office.",
   G(600, "cry", "cry", extras=DAVE), *[P("coffee", 1000 + i * 180, 900, 0.6, at=0.1 * i) for i in range(4)])
sc("Even-handed reminder: Oklahoma and Purdue are still big programs with a long season ahead. One week doesn't make a season. Ask Dave about his office pool.",
   P("scale", 960, 900, 1.1), T("1 WEEK, NOT 1 SEASON", 960, 330, 100, "dark", at=0.3))

# PART 6: WHAT'S NEXT ---------------------------------------------------------
sc("What happens next? The season is about four months long. Both the Lions and the Beacons now have targets on their backs.",
   P("calendar", 600, 860, 1.0, text="NOV-MAR"), G(1300, "stand", "worried", **VA), {"ring": [1300, 650, 110], "color": "red", "at": 0.4}, chapter="Part 6: What's next")
sc("For the giants, the fix is the dull stuff. Make free throws, protect the ball, make a few more threes. Moser's word for it was simple: get better.",
   HOOP(700, 0.9), T("FREE THROWS", 700, 300, 90, "dark", at=0.3), G(1400, "present", "neutral", look=-1, **COACH, at=0.5))
sc("And the bigger story keeps going. College sports is spending more on players than ever. This week was a reminder that the scoreboard doesn't read bank statements.",
   P("moneybag", 600, 900, 1.0), SCORE("SCORE, NOT $", 1300, 760, 1.0, at=0.3))

# RECAP ------------------------------------------------------------------------
sc("Recap. On November second, East Texas A&M beat Oklahoma sixty-eight to sixty-four as twenty-eight and a half point underdogs.",
   SCORE("LIONS 68|OU 64"), chapter="Recap")
sc("ESPN says that's the second-biggest upset by point spread in thirty years. On November sixth, Valparaiso beat Purdue eighty-three to eighty in double overtime on a buzzer-beater.",
   {"stamp": "#2 IN 30 YRS", "x": 600, "y": 450, "size": 70, "w": 460}, SCORE("VALPO 83|PURDUE 80", 1350, 760, 1.0, at=0.4))
sc("Money buys a lot in college basketball. Not, it turns out, made threes, made free throws, or the last four seconds.",
   P("moneybag", 600, 900, 1.0), {"cross": [600, 760, 140], "at": 0.3}, P("stopwatch", 1350, 860, 0.9, text="0:04", at=0.5))
sc("Your turn. What's the biggest upset you've ever seen, in any sport? Tell us in the comments. We read them all.",
   T("YOUR UPSET?", 960, 400, 140, "red"), P("speech", 960, 850, 0.9, at=0.3))
sc("This has been The Doodle Desk. We draw it, we count it, and we never bet against the team with nothing to lose.",
   G(960, "wave", "happy", extras=DAVE), T("THE DOODLE DESK", 960, 330, 110, "dark", at=0.3))


script = {
    "id": "ep022",
    "title": "Picked Last, Beat a Giant: College Hoops' Wildest Week",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Two college basketball giants lost to schools almost nobody picked in the first week of the 2026-27 season. "
        "On Nov 2, 2026, East Texas A&M, picked 12th of 12 in the Southland preseason poll, beat Oklahoma 68-64 in Norman as a 28.5-point underdog: "
        "per ESPN Research, the second-largest Division I upset by point spread in 30 years (only Eastern Illinois over Iowa in 2022 was bigger). "
        "On Nov 6, Valparaiso beat Purdue 83-80 in double overtime at Mackey Arena on Justus McNair's buzzer-beating three, its first win over Purdue since 1965. "
        "We go through both games, the history, the money gap after the House v. NCAA settlement ($20.5M revenue-sharing cap per school in 2025-26), "
        "and the reasons small teams win: three-point shooting, free throws and turnovers, early-season timing, and simply playing well. "
        "Real people appear only as generic labelled stick figures; quotes are as reported by the sources below.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "AP via News 9, Oklahoma stunned by East Texas A&M in 68-64 season-opening loss (Nov 2, 2026): https://www.news9.com/sports/university-of-oklahoma/oklahoma-stunned-by-east-texas-a-m-in-68-64-season-opening-loss\n"
        "ClutchPoints, Porter Moser apologizes after loss to East Texas A&M (Nov 3, 2026): https://clutchpoints.com/ncaa-basketball/oklahoma-basketball-news-porter-moser-forced-apologize-loss-east-texas-am-28-5-point-favorite\n"
        "Yardbarker, We already have our first stunning upset of the season (Nov 3, 2026): https://www.yardbarker.com/college_basketball/articles/we_already_have_our_first_stunning_upset_of_the_2026_27_college_basketball_season/s1_13132_44510412\n"
        "Field Level Media via Yardbarker, Valparaiso shocks Purdue on buzzer-beater in 2nd OT (Nov 6, 2026): https://www.yardbarker.com/college_basketball/articles/valparaiso_shocks_purdue_on_buzzer_beater_in_2nd_ot/s1_17048_44526859\n"
        "NCAA.com, 21 years in the making: How a prayer led to Valparaiso's historic win over Purdue (Nov 7, 2026): https://www.ncaa.com/news/basketball-men/article/2026-11-07/21-years-making-how-prayer-led-valparaiso-mens-basketballs-historic-win-over\n"
        "Purdue Boilermakers On SI via Yahoo Sports, 5 takeaways from Purdue's stunning 83-80 loss to Valparaiso (Nov 7, 2026): https://sports.yahoo.com/articles/5-takeaways-purdues-stunning-83-023319783.html\n"
        "Front Office Sports, The year schools paid their players: https://frontofficesports.com/the-year-schools-paid-their-players/\n\n"
        "#collegebasketball #upset #underdog #marchmadness #ncaa #valparaiso #purdue #oklahoma #explained #stickfigure"
    ),
    "tags": ["college basketball", "biggest upset", "underdog", "east texas a&m", "oklahoma sooners", "valparaiso", "purdue",
             "buzzer beater", "point spread", "ncaa", "house settlement", "revenue sharing", "sports explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "LOST|TO WHO?", "size": 200, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["sweat"], "shirt": "red"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "basketball", "x": 400, "y": 1000, "s": 1.6}, {"arrow": [[650, 820], [1000, 640]], "color": "red"}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep022.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

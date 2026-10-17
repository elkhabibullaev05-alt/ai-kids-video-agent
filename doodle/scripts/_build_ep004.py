"""Episode 4: The small-budget Brewers sweep the $339M Dodgers (NLCS, Oct 15, 2026)."""
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


DAVE = ["hair"]
ECON = ["glasses", "tie"]
FED = ["glasses", "tie", "briefcase"]

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


LINDA = ["bun"]
MIL = dict(extras=["cap"], shirt="navy")
LA = dict(extras=["cap"], shirt="blue")


def money(v, x, y, size=150, color="money", at=0, dur=2.0, **kw):
    d = {"count": [0, v], "fmt": "${:.0f}M", "x": x, "y": y, "size": size, "color": color, "at": at, "dur": dur}
    d.update(kw)
    return d


# COLD OPEN -------------------------------------------------------------------
sc("Two teams walk onto a baseball field.",
   G(560, "stand", "smug", look=1, **LA), G(1360, "stand", "neutral", look=-1, **MIL, at=0.3),
   P("baseball", 960, 520, 0.8, at=0.55, anim="spin"), cam={"from": [960, 560, 1.15], "to": [960, 540, 1.0]}, bg="sky")
sc("One team paid its players about three hundred thirty nine million dollars this year.",
   G(560, "hips", "smug", look=1, **LA), P("moneybag", 860, 900, 1.3, text="$", at=0.2),
   money(339, 700, 300, color="money", at=0.35), bg="sky")
sc("The other team paid about one hundred forty six million. Less than half.",
   G(1360, "shrug", "neutral", look=-1, **MIL), P("wallet", 1060, 760, 1.1, at=0.2),
   money(146, 1250, 300, color="dark", at=0.35), bg="sky")
sc("Normally, this is where the expensive team wins, and everyone goes home.",
   G(560, "fist", "grin", look=1, **LA), P("trophy", 820, 700, 1.2, at=0.3, anim="bob"),
   G(1360, "cry", "sad", look=-1, **MIL, at=0.5), bg="sky")
sc("Except this week, the cheap team won. Four games to zero. Not one loss.",
   {"cross": [820, 560, 120], "at": 0.1}, G(1360, "fist", "grin", look=-1, **MIL, anim="bob", at=0.2),
   P("scoreboard", 960, 640, 0.9, text="4 - 0", at=0.4), G(560, "facepalm", "shock", look=1, **LA, at=0.3), bg="sky")
sc("And somewhere in Milwaukee, Dave, who has waited forty four years for this, cannot feel his legs.",
   G(960, "panic", "scream", extras=["hair", "cap"], shirt="navy", anim="shake"), T("44 YEARS", 960, 260, 130, "red", at=0.4),
   P("tv", 1550, 800, 0.9, text="WORLD SERIES!", at=0.2))
sc("So today's question: how did a team with a small budget knock out baseball's most expensive champions?",
   G(380, "think", "confused", extras=["hair"]), T("HOW?", 1150, 380, 220, "red", at=0.35),
   P("scale", 1150, 900, 1.0, at=0.55), chapter="Today's question")
sc("And why are the people who run baseball watching this so closely, with a big money fight coming in December?",
   P("calendar", 620, 860, 1.1, text="DEC 1"), G(1250, "hold", "worried", extras=["glasses", "tie"], label="baseball officials", at=0.35),
   P("lock", 1650, 900, 0.8, at=0.65))
sc("We'll stick to the scores, the money, and what both sides say. No team colours. Well, a few team colours.",
   P("clipboard", 760, 900, 1.1, text="FACTS"), G(1300, "present", "neutral", extras=LINDA, at=0.4))

# PART 1: WHAT HAPPENED ------------------------------------------------------
sc("Thursday night, October fifteenth, Los Angeles. Game four of the National League Championship Series.",
   P("calendar", 520, 860, 1.1, text="OCT 15"), P("building", 1250, 900, 1.0, text="DODGER STADIUM", at=0.3),
   chapter="Part 1: What happened", bg="paper")
sc("Quick guide: two leagues each crown a champion, and those two meet in the World Series.",
   {"box": [260, 300, 520, 200], "color": "white"}, T("NATIONAL", 520, 410, 70, "blue"),
   {"box": [1140, 300, 520, 200], "color": "white", "at": 0.25}, T("AMERICAN", 1400, 410, 70, "red", at=0.25),
   {"arrow": [[600, 560], [900, 760]], "at": 0.5}, {"arrow": [[1320, 560], [1020, 760]], "at": 0.55},
   P("trophy", 960, 980, 0.9, at=0.7), ground=False)
sc("The Milwaukee Brewers had already won the first three games. One more win and they were in.",
   P("scoreboard", 960, 760, 1.0, text="MIL 3|LA 0"), G(400, "fist", "grin", look=1, **MIL, at=0.35),
   G(1520, "stand", "worried", look=-1, **LA, at=0.5))
sc("The Los Angeles Dodgers were the champions of the last two years, trying to win a third in a row.",
   P("trophy", 760, 640, 0.8), P("trophy", 960, 640, 0.8, at=0.2), P("trophy", 1160, 640, 0.8, at=0.45, color="grey"),
   T("?", 1160, 420, 110, "red", at=0.6), G(1600, "hips", "smug", look=-1, **LA))
sc("Only one team in history has pulled off that three-in-a-row: the New York Yankees, from 1998 to 2000.",
   T("1998  1999  2000", 960, 360, 110, "navy"), P("trophy", 960, 860, 1.0, at=0.35),
   G(400, "point", "neutral", extras=ECON, at=0.5))
sc("And for a while, it looked like the Dodgers might keep going. They took a four to nothing lead by the second inning.",
   P("scoreboard", 960, 760, 1.0, text="LA 4|MIL 0"), G(1550, "fist", "grin", look=-1, **LA, at=0.4))
sc("Their superstar Shohei Ohtani hit a three run home run, his first home run of these playoffs. Forty nine thousand fans went loud.",
   P("baseball", 500, 440, 0.6, move=[1500, 200], at=0.1), P("bat", 380, 900, 1.0),
   {"count": [0, 49104], "fmt": "{:,.0f}", "x": 1250, "y": 640, "size": 120, "color": "blue", "at": 0.5, "dur": 1.6},
   T("fans", 1250, 760, 60, "dark", at=0.55))
sc("Back in Milwaukee, Dave quietly put his snacks down.",
   G(800, "stand", "tired", extras=["hair", "cap"], shirt="navy"), P("tv", 1350, 800, 0.9, text="LA 4  MIL 0"),
   P("bread", 560, 760, 0.6, at=0.4, in_="drop"))
sc("Then the comeback. In the fourth inning, two Brewers hit back-to-back doubles. Four to two.",
   P("scoreboard", 960, 760, 1.0, text="LA 4|MIL 2"), G(400, "run", "grin", look=1, **MIL, at=0.3),
   P("arrowup", 1550, 760, 0.9, color="green", at=0.5))
sc("In the fifth, the Dodgers' relief pitchers walked four batters. A walk means the batter gets a free trip to first base.",
   G(560, "shrug", "worried", look=1, **LA), {"count": [0, 4], "fmt": "{:.0f} WALKS", "x": 1250, "y": 420, "size": 120, "color": "red", "at": 0.3, "dur": 1.2},
   G(1350, "stand", "happy", look=-1, **MIL, walk=True, at=0.5, move=[1650, 900]))
sc("Free things in a playoff game are bad. Four to four.",
   P("pricetag", 700, 700, 1.1, text="FREE", color="yellow"), P("scoreboard", 1350, 760, 1.0, text="LA 4|MIL 4", at=0.4))
sc("Sixth inning. Outfielder Garrett Mitchell falls behind, no balls and two strikes. One more strike and he's out.",
   G(700, "hold", "worried", look=1, **MIL), P("bat", 820, 900, 0.9), T("0 - 2", 1350, 380, 150, "red", at=0.4))
sc("He fights back to a full count, and hits the ball four hundred nine feet over the centre field wall.",
   P("baseball", 760, 500, 0.6, move=[1650, 160]), {"count": [0, 409], "fmt": "{:.0f} FT", "x": 1150, "y": 640, "size": 150, "color": "navy", "at": 0.35, "dur": 1.6},
   G(450, "fist", "grin", look=1, **MIL, at=0.4))
sc("Five to four, Milwaukee. Afterwards, Mitchell said: It's absolutely surreal.",
   P("scoreboard", 600, 760, 0.9, text="MIL 5|LA 4"), G(1250, "present", "happy", look=-1, **MIL, label="Garrett Mitchell"),
   P("speech", 1600, 520, 1.1, text="surreal", at=0.4))
sc("Then, in the ninth, their number nine hitter David Hamilton, who hit four home runs in the whole regular season, hits another.",
   G(600, "hold", "neutral", look=1, **MIL, label="David Hamilton"), P("bat", 720, 900, 0.9),
   T("4 HR all season", 1300, 380, 90, "dark", at=0.3), P("baseball", 760, 560, 0.5, move=[1700, 200], at=0.6))
sc("Six to four. The Brewers' bullpen held on, and Milwaukee was going to the World Series.",
   P("scoreboard", 960, 700, 1.1, text="MIL 6|LA 4"), G(400, "fist", "grin", look=1, **MIL, anim="bob", at=0.4),
   G(1520, "fist", "grin", look=-1, **MIL, anim="bob", at=0.5))

# PART 2: THE RECORDS ---------------------------------------------------------
sc("Now, some numbers, because this wasn't just a win. It was a pile of history.",
   P("clipboard", 960, 880, 1.2, text="HISTORY"), G(420, "present", "neutral", extras=ECON),
   chapter="Part 2: The numbers", bg="yellow")
sc("It's Milwaukee's first trip to the World Series since 1982, and only the second ever.",
   {"count": [1982, 2026], "fmt": "{:.0f}", "x": 960, "y": 380, "size": 200, "color": "navy", "dur": 2.2},
   P("calendar", 1550, 860, 0.9, text="44 YRS", at=0.5), bg="yellow")
sc("In 1982 they were in the other league, and they lost the World Series to St. Louis in seven games.",
   P("calendar", 560, 860, 1.0, text="1982"), T("lost in 7", 1250, 420, 110, "red", at=0.35),
   G(1300, "cry", "sad", look=-1, **MIL, at=0.5, s=0.85), bg="yellow")
sc("So this is also their first National League pennant. A pennant is the league title. Also a small flag. Baseball loves a small flag.",
   T("PENNANT", 960, 330, 130, "navy"), {"arrow": [[960, 420], [960, 600]], "at": 0.5},
   {"box": [860, 620, 300, 120], "color": "gold", "at": 0.55}, G(1550, "shrug", "neutral", extras=LINDA, at=0.7), bg="yellow")
sc("They won a hundred and three games in the regular season, the most of any team in the majors.",
   {"count": [0, 103], "fmt": "{:.0f} WINS", "x": 960, "y": 420, "size": 180, "color": "green", "dur": 2.0},
   P("trophy", 1600, 800, 0.9, at=0.5), bg="yellow")
sc("They're the first team to sweep a seven game playoff series while trailing at some point in every single game.",
   P("scoreboard", 960, 720, 1.0, text="BEHIND x4|WON x4"), G(1600, "think", "confused", extras=["hair"], at=0.5), bg="yellow")
sc("And one more. Last year, the Dodgers swept the Brewers in this exact same round. Zero wins for Milwaukee.",
   P("calendar", 520, 860, 1.0, text="2025"), P("scoreboard", 1250, 720, 0.9, text="LA 4|MIL 0", at=0.3), bg="yellow")
sc("This year Milwaukee returned the favour, four to zero. No team had ever been swept by someone and swept them right back the next year.",
   P("calendar", 520, 860, 1.0, text="2026"), P("scoreboard", 1250, 720, 0.9, text="MIL 4|LA 0", at=0.3),
   {"stamp": "FIRST EVER", "x": 620, "y": 380, "size": 70, "w": 340, "at": 0.65}, bg="yellow")
sc("Their pitcher Aaron Ashby, who got the last outs, said the team played with a chip on its shoulder.",
   G(700, "fist", "angry", look=1, **MIL, label="Aaron Ashby"), P("speech", 1300, 520, 1.2, text="chip on our shoulder", at=0.35))
sc("Brewers manager Pat Murphy said: We weren't coming in to play patty-cake.",
   G(600, "point", "smug", look=1, extras=["cap"], shirt="navy", label="manager Pat Murphy"),
   P("speech", 1250, 520, 1.3, text="no patty-cake", at=0.3), {"cross": [1550, 780, 80], "at": 0.7})
sc("He also said: They may have a bunch of Hall of Famers, but we've got a bunch of gamers.",
   G(500, "present", "grin", look=1, extras=["cap"], shirt="navy", label="Pat Murphy"),
   T("HALL OF FAMERS", 1250, 360, 80, "blue", at=0.3), T("vs", 1250, 470, 70, "dark", at=0.45), T("GAMERS", 1250, 580, 100, "navy", at=0.55))
sc("Dodgers manager Dave Roberts, to his credit, said the Brewers played flawless, and that he's not used to giving consolation speeches.",
   G(1300, "shrug", "tired", look=-1, extras=["cap"], shirt="blue", label="manager Dave Roberts"),
   P("speech", 650, 520, 1.2, text="they played flawless", at=0.35))
sc("After two titles in a row, fair. He hasn't had much practice.",
   P("trophy", 700, 700, 0.8), P("trophy", 900, 700, 0.8), G(1350, "think", "neutral", look=-1, extras=["cap"], shirt="blue", at=0.3))

# PART 3: THE MONEY -----------------------------------------------------------
sc("Okay. Now the part everybody is really talking about. The money.",
   P("moneybag", 960, 900, 1.6, text="$", anim="pulse"), chapter="Part 3: The money", bg="paper")
sc("In baseball, there's no limit on how much a team can spend on players. Rich teams can spend a lot. Some do.",
   {"box": [560, 300, 800, 160], "color": "white"}, T("SPENDING LIMIT: NONE", 960, 380, 70, "dark"),
   G(1550, "hips", "smug", look=-1, extras=["tophat"], at=0.4), P("moneybag", 420, 900, 1.0, at=0.6))
sc("Here are the payrolls of the last four teams standing, as reported by the Sporting News, using Spotrac data.",
   P("clipboard", 960, 880, 1.1, text="PAYROLLS"), G(420, "present", "neutral", extras=ECON, at=0.3))
sc("The Dodgers: three hundred thirty nine million dollars. Second highest in baseball.",
   {"bars": {"values": [339], "labels": ["Dodgers"], "colors": ["blue"], "fmt": "${}M", "w": 260, "h": 520}, "x": 960, "y": 860},
   T("#2", 1350, 420, 120, "blue", at=0.5))
sc("The Brewers: one hundred forty six million. Nineteenth out of thirty.",
   {"bars": {"values": [339, 146], "labels": ["Dodgers", "Brewers"], "colors": ["blue", "navy"], "fmt": "${}M", "w": 560, "h": 520}, "x": 960, "y": 860},
   T("#19", 1450, 420, 120, "navy", at=0.5))
sc("Their American League rivals, the Tampa Bay Rays: about ninety six million. Twenty eighth.",
   {"bars": {"values": [339, 146, 96], "labels": ["Dodgers", "Brewers", "Rays"], "colors": ["blue", "navy", "teal"], "fmt": "${}M", "w": 820, "h": 520}, "x": 960, "y": 860},
   T("#28", 1600, 420, 110, "teal", at=0.5))
sc("And the Cleveland Guardians: about seventy four million. Dead last. Thirtieth out of thirty.",
   {"bars": {"values": [339, 146, 96, 74], "labels": ["Dodgers", "Brewers", "Rays", "Guardians"], "colors": ["blue", "navy", "teal", "red"], "fmt": "${}M", "w": 1060, "h": 520}, "x": 960, "y": 860},
   T("#30", 1650, 420, 110, "red", at=0.5))
sc("Put that together, and the Dodgers' payroll was bigger than the other three teams combined.",
   P("moneybag", 560, 900, 1.6, text="LA"), T(">", 960, 600, 160, "red", at=0.5),
   P("wallet", 1250, 700, 0.7, at=0.35), P("wallet", 1450, 700, 0.7, at=0.4), P("wallet", 1650, 700, 0.7, at=0.45))
sc("Here's another one. In February, the Dodgers gave one new player, Kyle Tucker, a fifty four million dollar signing bonus.",
   G(560, "hold", "grin", look=1, **LA, label="Kyle Tucker"), P("moneybag", 900, 900, 1.2, text="$54M", at=0.3),
   P("calendar", 1500, 860, 0.9, text="FEB", at=0.5))
sc("That one bonus is only about twenty million dollars less than Cleveland's entire team.",
   P("moneybag", 600, 900, 1.3, text="$54M"), T("vs", 960, 560, 90, "dark", at=0.25), P("moneybag", 1350, 900, 1.5, text="$74M", at=0.4),
   G(1700, "facepalm", "shock", extras=LINDA, at=0.6))
sc("Linda in Cleveland is asking a very reasonable question: wait, so what are we paying for?",
   G(960, "hips", "angry", extras=LINDA, look=1), T("?", 1350, 380, 180, "red", at=0.4))
sc("Of the fourteen semi-final players earning fifteen million dollars or more, not counting Tucker, eleven were Dodgers.",
   {"count": [0, 11], "fmt": "{:.0f} of 14", "x": 960, "y": 420, "size": 180, "color": "blue", "dur": 1.6},
   G(1600, "shrug", "smug", look=-1, **LA, at=0.5))
sc("All of this is within the rules. Teams that spend past a set line pay a luxury tax. It's not a cap. It's more of a fee.",
   {"box": [460, 300, 1000, 160], "color": "white"}, T("LUXURY TAX = A FEE", 960, 380, 70, "dark"),
   G(1600, "hold", "neutral", look=-1, **LA, at=0.4), P("dollar", 380, 820, 0.9, at=0.6))

# PART 4: HOW MILWAUKEE DOES IT -----------------------------------------------
sc("So how does a small team keep up? Milwaukee is often described as the smallest market in the majors. Fewer people, less TV money.",
   P("building", 600, 900, 0.6, text="MIL"), P("building", 1350, 900, 1.3, text="LA", at=0.3),
   chapter="Part 4: How Milwaukee does it", bg="paper")
sc("And yet, by last year, they had made the playoffs seven of the previous eight seasons. This isn't one lucky year.",
   {"bars": {"values": [1, 1, 1, 1, 1, 0, 1, 1], "labels": ["", "", "", "", "", "", "", ""], "colors": ["green"] * 5 + ["grey"] + ["green"] * 2, "fmt": "", "w": 900, "h": 300}, "x": 960, "y": 760},
   T("7 OF 8", 960, 300, 150, "green", at=0.5))
sc("Sports writers point to a few habits. One: they grow their own players. Several of their regulars were their own draft picks.",
   T("1. GROW YOUR OWN", 960, 300, 90, "navy"), G(700, "hold", "happy", look=1, extras=["hardhat"], at=0.3),
   G(1250, "stand", "happy", look=-1, **MIL, s=0.6, at=0.5))
sc("Two: they trade stars before they get too expensive. They traded away pitchers like Corbin Burnes and Josh Hader before free agency.",
   T("2. TRADE BEFORE IT HURTS", 960, 300, 80, "navy"), G(600, "wave", "sad", look=1, **MIL), {"arrow": [[760, 640], [1200, 640]], "at": 0.4},
   P("moneybag", 1450, 900, 1.0, at=0.55))
sc("Fans hate that part. Dave still has the jersey. Dave will always have the jersey.",
   G(960, "cry", "cry", extras=["hair"], shirt="navy"), T("#?", 960, 560, 60, "white", at=0.3))
sc("Three: they pick up players other teams gave up on, and somehow those players get better in Milwaukee.",
   T("3. SECOND CHANCES", 960, 300, 90, "navy"), G(500, "shrug", "sad", look=1, extras=["cap"], shirt="grey"),
   {"arrow": [[700, 640], [1150, 640]], "at": 0.35}, G(1350, "fist", "grin", look=-1, **MIL, at=0.5))
sc("A CBS Sports writer put it like this: the Brewers machine is much bigger than any one player or person.",
   G(500, "present", "neutral", extras=["glasses"], label="CBS Sports columnist"), P("speech", 1200, 520, 1.3, text="the machine", at=0.35))
sc("Which they've tested. Their top executive left for the Mets. Their old manager left for the Cubs. They kept winning anyway.",
   P("building", 500, 900, 0.7, text="METS"), P("building", 1420, 900, 0.7, text="CUBS", at=0.25),
   G(960, "hips", "smug", look=1, **MIL, at=0.5))
sc("Honest bit, though: money still matters. The Dodgers won the two titles before this one with that payroll.",
   P("scale", 960, 900, 1.3), P("moneybag", 760, 640, 0.6, at=0.3), P("trophy", 1160, 620, 0.6, at=0.4))
sc("One sweep doesn't prove money is useless. It proves money isn't a guarantee. That's a smaller claim, but it's the true one.",
   {"cross": [600, 420, 90], "at": 0.1}, T("useless", 600, 420, 70, "dark"), {"ring": [1300, 420, 140], "at": 0.4},
   T("not a guarantee", 1300, 420, 60, "green"))

# PART 5: THE BIG MONEY FIGHT -------------------------------------------------
sc("And that's exactly why this matters off the field. Baseball's labour deal, the contract between owners and players, ends on December first.",
   P("calendar", 960, 860, 1.4, text="DEC 1", anim="pulse"), chapter="Part 5: The money fight", bg="yellow")
sc("That deal is called the collective bargaining agreement. It sets the rules for how teams pay players.",
   P("clipboard", 960, 880, 1.2, text="THE DEAL"), G(450, "point", "neutral", extras=ECON, at=0.35), bg="yellow")
sc("This summer, Fox News reported that the owners proposed a salary cap. A hard limit on what each team can spend on players.",
   G(560, "present", "neutral", extras=["tie", "tophat"], label="the owners"), P("lock", 1200, 900, 1.0, text="CAP", at=0.35), bg="yellow")
sc("It's the owners' first salary cap proposal since 1994. That's the year a players' strike cancelled the World Series.",
   P("calendar", 600, 860, 1.0, text="1994"), P("trophy", 1250, 700, 0.9, at=0.3), {"cross": [1250, 560, 120], "at": 0.55}, bg="yellow")
sc("Commissioner Rob Manfred said: I have an ownership group that is more united than any group in my entire time in baseball.",
   G(560, "present", "neutral", extras=["glasses", "tie"], label="the Commissioner"), P("speech", 1250, 520, 1.3, text="more united than ever", at=0.3),
   bg="yellow")
sc("The case for a cap: it would stop a few rich teams from simply outspending everybody else, the way some say the Dodgers have.",
   T("FOR A CAP", 960, 280, 100, "dark"), P("scale", 960, 900, 1.2, at=0.2), P("moneybag", 760, 660, 0.5, at=0.4),
   P("wallet", 1160, 640, 0.5, at=0.45), bg="yellow")
sc("The players' union says no. Its interim leader Bruce Meyer said: Salary cap is the ultimate excuse not to compete.",
   G(1300, "point", "angry", look=-1, extras=["hair"], label="players' union"), P("speech", 650, 520, 1.3, text="the ultimate excuse", at=0.3),
   bg="yellow")
sc("The players want the opposite. A minimum every team has to spend, and no maximum.",
   T("AGAINST A CAP", 960, 280, 100, "dark"), P("arrowup", 760, 800, 0.9, text="FLOOR", color="green", at=0.25),
   {"cross": [1200, 640, 90], "at": 0.5}, T("MAX", 1200, 640, 70, "dark", at=0.45), bg="yellow")
sc("And here's where this week gets awkward for both sides.",
   G(560, "shrug", "confused", extras=["tie", "tophat"]), G(1360, "shrug", "confused", extras=["hair"], look=-1, at=0.2), bg="yellow")
sc("Cap opponents can say: look, the cheap teams made it. You don't need a cap.",
   G(700, "point", "smug", extras=["hair"]), T("NO CAP NEEDED", 1300, 400, 90, "green", at=0.3), bg="yellow")
sc("Cap supporters can say: look, those teams had to sell off their stars to survive. That's not a fair fight. Depending on who you ask, both are right.",
   G(1200, "point", "smug", extras=["tie", "tophat"], look=-1), T("NOT FAIR", 600, 400, 110, "red", at=0.3), bg="yellow")
sc("ESPN and CNN both ran pieces this week asking what this final four says about that fight.",
   P("tv", 700, 800, 0.9, text="ESPN"), P("tv", 1250, 800, 0.9, text="CNN", at=0.25), bg="yellow")
sc("If no deal is reached, owners can lock the players out. The last lockout, in 2021 and 2022, lasted ninety nine days.",
   P("lock", 600, 900, 1.2, text="LOCKOUT"), {"count": [0, 99], "fmt": "{:.0f} DAYS", "x": 1300, "y": 420, "size": 160, "color": "red", "at": 0.4, "dur": 1.8},
   bg="yellow")
sc("The players' union has said it expects another lockout. Nobody has said it's certain. We'll see. We just count the facts.",
   P("calendar", 700, 860, 1.0, text="DEC 2?"), T("?", 1250, 420, 220, "red", at=0.3), G(1600, "think", "neutral", extras=LINDA, at=0.5),
   bg="yellow")

# PART 6: WHAT'S NEXT --------------------------------------------------------
sc("Back to the fun part. The World Series begins Friday, October twenty third, in Milwaukee.",
   P("calendar", 600, 860, 1.1, text="OCT 23"), P("building", 1300, 900, 1.0, text="MILWAUKEE", at=0.3),
   chapter="Part 6: What's next", bg="sky")
sc("The Brewers get about a week off. Players call that rest. Fans call it the longest week of their lives.",
   G(500, "stand", "happy", **MIL, look=1), P("stopwatch", 1350, 900, 1.0, anim="shake", at=0.4),
   G(1650, "panic", "worried", extras=["hair"], shirt="navy", look=-1, at=0.5), bg="sky")
sc("Their opponent is still being decided. Cleveland led Tampa Bay two games to one in the American League series when we made this.",
   P("scoreboard", 960, 720, 1.0, text="CLE 2|TB 1"), T("?", 1600, 380, 180, "red", at=0.5), bg="sky")
sc("Which means one thing is already certain. Whoever wins, the World Series will be played by two teams from the bottom half of the payroll list.",
   {"bars": {"values": [146, 96, 74], "labels": ["Brewers", "Rays", "Guardians"], "colors": ["navy", "teal", "red"], "fmt": "${}M", "w": 760, "h": 380}, "x": 900, "y": 840},
   {"stamp": "NO GIANTS", "x": 1600, "y": 300, "size": 70, "w": 320, "at": 0.6}, bg="sky")
sc("Brewers owner Mark Attanasio thanked two Milwaukee legends, former owner Bud Selig and broadcaster Bob Uecker, saying the team is standing on their shoulders.",
   G(700, "present", "happy", extras=["tie"], label="owner Mark Attanasio"), P("speech", 1350, 520, 1.2, text="standing on shoulders", at=0.35), bg="sky")
sc("Nice. Though Dave is standing on his couch, which is less poetic.",
   G(960, "fist", "scream", extras=["hair", "cap"], shirt="navy", y=760, anim="bob"), {"box": [700, 760, 520, 140], "color": "brown"}, bg="sky")

# RECAP -----------------------------------------------------------------------
sc("So, the recap. The Brewers came back from four runs down and swept the two-time champion Dodgers to reach their first World Series since 1982.",
   P("scoreboard", 960, 720, 1.0, text="MIL 4|LA 0"), chapter="Recap", bg="paper")
sc("They did it with a payroll of about one hundred forty six million dollars, less than half of the Dodgers' three hundred thirty nine.",
   {"bars": {"values": [339, 146], "labels": ["Dodgers", "Brewers"], "colors": ["blue", "navy"], "fmt": "${}M", "w": 560, "h": 460}, "x": 960, "y": 860})
sc("And it lands right before owners and players fight over a salary cap, with the current deal ending December first.",
   P("calendar", 700, 860, 1.0, text="DEC 1"), P("lock", 1300, 900, 1.0, text="CAP?", at=0.3))
sc("Money buys a lot in baseball. It just doesn't buy the last out.",
   P("moneybag", 700, 900, 1.2, text="$"), {"arrow": [[880, 640], [1180, 640]], "at": 0.3}, T("?", 1350, 600, 160, "red", at=0.5),
   P("baseball", 1350, 860, 0.5, at=0.6))
sc("Meanwhile, Dave has finally picked his snacks back up, and has already bought a ticket he absolutely cannot afford.",
   G(700, "hold", "grin", extras=["hair", "cap"], shirt="navy"), P("pricetag", 1250, 700, 1.1, text="$$$$", at=0.35, anim="pulse"),
   P("wallet", 1600, 800, 0.8, text=":(", at=0.6, anim="shake"))
sc("Your turn: should baseball have a salary cap, or did this week prove it doesn't need one? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), T("CAP?", 1050, 380, 140, "red", at=0.3), T("NO CAP?", 1450, 560, 110, "navy", at=0.5))
sc("And if stick figures explaining the news is your kind of thing, subscribe. We'll keep counting the facts. And the money.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=["hair"], at=0.3), hold=1.2)

script = {
    "id": "ep004",
    "title": "How Did a Cheap Team Beat Baseball's $339M Giant?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "The Milwaukee Brewers, with a payroll of about $146 million, just swept the two-time champion Los Angeles Dodgers "
        "(about $339 million) to reach their first World Series since 1982. How does a small-budget team do that, and why does it "
        "matter for baseball's coming fight over a salary cap? Explained with stick figures.\n\n"
        "Chapters are in the video timeline.\n\n"
        "Payroll figures: The Sporting News (Spotrac data), Oct 12, 2026. Quotes are attributed to the people who said them, as reported.\n\n"
        "Sources:\n"
        "AP via ABC News, Brewers sweep the Dodgers to reach first World Series since 1982: https://abcnews.com/Sports/wireStory/brewers-sweep-dodgers-nlcs-reach-world-series-time-137309462\n"
        "NBC Los Angeles, Brewers sweep Dodgers in NLCS: https://www.nbclosangeles.com/news/sports/dodgers-brewers-nlcs-game-4/3956918/\n"
        "NBC Sports: https://www.nbcsports.com/mlb/news/brewers-sweep-the-dodgers-in-the-nlcs-to-reach-the-world-series-for-the-first-time-since-1982\n"
        "The Sporting News via Yahoo Sports, MLB payrolls for 4 remaining playoff teams: https://sports.yahoo.com/articles/mlb-payrolls-4-remaining-playoff-213607502.html\n"
        "Bleacher Report, Dodgers payroll vs Brewers, Rays and Guardians: https://bleacherreport.com/articles/25509046-wild-stat-how-dodgers-payroll-compares-brewers-rays-and-guardians-amid-world-series-bracket\n"
        "CBS Sports, How small-market Brewers find a way: https://www.cbssports.com/mlb/news/how-small-market-brewers-find-a-way-despite-front-office-roster-turnover-milwaukee-keeps-winning\n"
        "Fox News, MLB lockout looms as CBA expires and salary cap talks stall: https://www.foxnews.com/sports/inside-mlb-cba-negotiations-manfred-players-union-exec-discuss-issues-sides-attempt-save-2027-season\n"
        "CNN, Four teams left and MLB's future: https://www.cnn.com/2026/10/14/sport/mlb-salary-cap-debate-analysis\n"
        "ESPN, What this year's final four says about MLB's labor battle: https://www.espn.com/mlb/story/_/id/50166698/mlb-playoffs-2026-nlcs-alcs-dodgers-brewers-rays-guardians-payroll-cba-labor\n"
        "NBC Chicago, ALCS/NLCS schedule: https://www.nbcchicago.com/mlb/nlcs-alcs-schedule-bracket-playoffs-2026/\n"
        "NESN, MLB lockout ends after 99 days (2022): https://nesn.com/2022/03/mlb-owners-ratify-new-cba-officially-ending-lockout-99-days\n\n"
        "#brewers #dodgers #worldseries #mlb #salarycap #explained #stickfigure"
    ),
    "tags": ["brewers", "dodgers", "world series 2026", "nlcs", "mlb payroll", "salary cap", "mlb lockout", "milwaukee brewers",
             "baseball explained", "news explained", "stick figure animation", "sports business"],
    "thumbnail": {"bg": "yellow", "text": "CHEAP TEAM|WINS?!", "size": 190, "color": "black",
                  "guy": {"pose": "fist", "face": "smug", "look": -1, "extras": ["cap"], "shirt": "navy"},
                  "items": [{"prop": "moneybag", "x": 1700, "y": 860, "s": 1.3, "text": "$"}, {"prop": "baseball", "x": 1720, "y": 420, "s": 0.8}], "guy_x": 1330},
    "scenes": [s for s in S if s],
}
# rek-ball pacing: every scene gets a different background tint from the one before -> a clear visual cut
_CYC = ["paper", "blue", "paper", "teal", "paper", "purple"]
for _i, _s in enumerate(script["scenes"]):
    _s["bg"] = _CYC[_i % len(_CYC)]
for s in script["scenes"]:
    for it in list(s["items"]):
        g = it.get("guy")
        if g and g.get("label"):
            sz = it.get("s", 1.0)
            s["items"].append({"text": g.pop("label"), "x": it["x"], "y": it.get("y", 900) - int(430 * sz), "size": 44,
                               "color": "dark", "at": it.get("at", 0)})
    for it in s["items"]:
        if "in_" in it:
            it["in"] = it.pop("in_")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep004.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

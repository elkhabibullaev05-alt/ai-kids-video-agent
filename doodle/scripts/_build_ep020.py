"""Episode 20: Como (city of ~83,000, Serie D in 2017) beat Lens 9-1 away in the Champions League (Nov 4, 2026). Underdog or billionaire project?"""
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
COMO = dict(extras=["hair"], shirt="blue")          # generic Como player
COMO2 = dict(extras=[], shirt="blue")
LENS = dict(extras=["hair"], shirt="red")           # generic Lens player
LENS2 = dict(extras=[], shirt="red")
GK = dict(extras=["cap"], shirt="yellow")            # generic Lens goalkeeper
COACH = dict(extras=["glasses"], shirt="navy")       # generic coach
OWN = dict(extras=["tie", "tophat"], shirt="grey")   # generic owner
FAN = dict(extras=["cap"], shirt="blue")
LFAN = dict(extras=["cap"], shirt="red")
KID = dict(extras=["hair"], shirt="sky")

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


def PITCH(at=0):
    return [{"box": [0, 760, 1920, 320], "color": "green", "at": at},
            {"box": [0, 755, 1920, 10], "color": "white", "at": at}]


def CROWD(x0, x1, at=0, face="happy", pose="fist", kind=None, n=6):
    kind = kind or FAN
    out = []
    step = (x1 - x0) // (n - 1)
    for i in range(n):
        out.append(G(x0 + i * step, pose, face, look=1 if i % 2 else -1, s=0.5, y=900, at=at + 0.04 * i if at < 1 else at, **kind))
    return out


def BOARD(text, x=960, y=760, s=1.0, at=0, **kw):
    return P("scoreboard", x, y, s, at=at, text=text, **kw)


# COLD OPEN ------------------------------------------------------------------
sc("Nine.",
   C(0, 9, 960, 470, fmt="{:.0f}", size=420, color="red", dur=1.0), bg="yellow")
sc("That's how many goals a football club from a lake town of eighty-three thousand people scored on Wednesday night. Away from home. In the Champions League.",
   P("lake", 520, 900, 1.0, text="COMO"), C(0, 83000, 520, 300, fmt="{:,.0f}", size=90, color="navy", at=0.25),
   P("football", 1250, 820, 0.8, at=0.5, anim="spin"), P("trophy", 1600, 860, 1.1, at=0.65))
sc("Final score: Lens one, Como nine. No away team had ever scored nine in a Champions League match.",
   BOARD("LENS 1|COMO 9", 700), {"stamp": "NEVER BEFORE", "x": 1450, "y": 450, "size": 80, "w": 560, "at": 0.55})
sc("Nine years ago, this same club was in Serie D, Italy's fourth division, after going bankrupt.",
   P("calendar", 600, 860, 1.0, text="2017"), T("SERIE D", 600, 330, 110, "dark", at=0.25), G(1350, "cry", "sad", look=-1, **COMO, at=0.45))
sc("Dave checked the score at half time, then again at full time, then refreshed the page four more times, because he assumed it was a typo.",
   G(600, "type", "confused", extras=DAVE), P("laptop", 950, 860, 0.9), T("9 - 1 ???", 1450, 400, 120, "red", at=0.45, anim="shake"), bg="yellow")
S.append({"say": "So here's today's question. Is Como the greatest underdog story in football right now, or a billionaire project that was always going to get here?",
          "items": [G(550, "fist", "grin", **COMO, label="underdog?"), T("or", 960, 520, 120, "red", at=0.3), P("moneybag", 1400, 860, 1.5, at=0.45), T("?", 1400, 330, 200, "red", at=0.6)],
          "chapter": "Today's question"})
sc("Depending on who you ask, it's both. We'll go through the night, the records, the money, and what comes next.",
   P("football", 450, 800, 0.7), P("stopwatch", 800, 860, 0.8, at=0.15), P("moneybag", 1150, 860, 0.9, at=0.3), P("clipboard", 1500, 860, 0.9, at=0.45, text="NEXT"))

# PART 1: THE NIGHT -----------------------------------------------------------
sc("First, what happened. Wednesday, November fourth, Stade Bollaert-Delelis in Lens, northern France. Matchday four of the Champions League league phase.",
   *PITCH(), G(600, "stand", "neutral", **LENS, label="Lens"), T("vs", 960, 450, 120, "red", at=0.2), G(1320, "stand", "neutral", look=-1, **COMO, label="Como", at=0.3),
   chapter="Part 1: The night in Lens")
sc("Before kickoff, Lens had three points from three games. Como had six. Nobody was predicting anything unusual.",
   {"bars": {"values": [3, 6], "labels": ["Lens", "Como"], "colors": ["red", "blue"], "fmt": "{} pts", "w": 600, "h": 380}, "x": 700, "y": 840},
   G(1450, "shrug", "neutral", look=-1, extras=ECON, at=0.5))
sc("Seventh minute. Como's Greek striker, Tasos Douvikas, scores. One nil.",
   *PITCH(), P("goal", 1450, 900, 1.0), P("football", 700, 700, 0.5, move=[1450, 780]), G(600, "point", "grin", **COMO, label="striker", at=0.1),
   BOARD("0 - 1", 400, 600, 0.5, at=0.7))
sc("Thirty-second minute. Douvikas again. Two nil.",
   *PITCH(), P("goal", 1450, 900, 1.0), P("football", 700, 700, 0.5, move=[1450, 780]), G(600, "fist", "grin", **COMO, at=0.1), BOARD("0 - 2", 400, 600, 0.5, at=0.6))
sc("Fortieth minute. A powerful strike from the Argentine midfielder Nico Paz. Three nil at half time.",
   *PITCH(), G(500, "point", "angry", **COMO2, label="midfielder"), P("football", 650, 700, 0.5, move=[1450, 720], at=0.2), P("goal", 1450, 900, 1.0), BOARD("0 - 3", 960, 500, 0.6, at=0.6))
sc("A three goal lead at half time is big. It is not historic. Teams come back from three down. Lens fans had every reason to stay.",
   T("HALF TIME", 960, 300, 110, "navy"), *CROWD(560, 1360, at=0.3, face="worried", pose="stand", kind=LFAN), bg="sky")
sc("Then the second half happened. Forty-seventh minute: Lucas Da Cunha. Four nil.",
   *PITCH(), P("goal", 1450, 900, 1.0), P("football", 600, 700, 0.5, move=[1450, 780]), BOARD("0 - 4", 400, 600, 0.5, at=0.5))
sc("Fifty-third minute: a header from the defender Marc-Oliver Kempf. Five nil.",
   *PITCH(), G(900, "pointup", "grin", **COMO2, label="defender"), P("football", 900, 380, 0.5, move=[1450, 780], at=0.3), P("goal", 1450, 900, 1.0), BOARD("0 - 5", 400, 600, 0.5, at=0.6))
sc("Fifty-seventh minute: Douvikas completes his hat trick. Six nil. He has now scored in all four of Como's Champions League games.",
   G(600, "fist", "grin", **COMO, label="striker"), *[P("football", 1100 + i * 200, 420, 0.45, at=0.15 + 0.1 * i) for i in range(3)], T("HAT TRICK", 1300, 650, 100, "red", at=0.55))
sc("Sixty-second minute: Mattia Liberali, who had come on as a substitute four minutes earlier, pokes it in. Seven nil.",
   G(500, "run", "grin", **COMO2, label="sub", walk=True), P("stopwatch", 1000, 860, 0.8, text="+4 min"), BOARD("0 - 7", 1500, 760, 0.8, at=0.5))
sc("Sixty-fifth minute: Lens finally score. Ruben Aguilar. Seven one. The home crowd gets one goal to cheer for.",
   *PITCH(), G(600, "fist", "happy", **LENS, label="Lens"), P("football", 700, 700, 0.5, move=[1450, 780], at=0.2), P("goal", 1450, 900, 1.0), BOARD("1 - 7", 400, 560, 0.5, at=0.6))
sc("Four minutes later, Croatia midfielder Martin Baturina makes it eight.",
   BOARD("1 - 8", 700, 760, 0.9), G(1400, "point", "smug", look=-1, **COMO, label="midfielder", at=0.4))
sc("And in stoppage time, an eighteen-year-old from Como's youth team, Matteo Papaccioli, scores the ninth. He hasn't even played a game in Serie A yet.",
   G(600, "panic", "grin", **KID, label="18 years old"), BOARD("1 - 9", 1350, 760, 0.9, at=0.3), T("0 Serie A games", 1350, 330, 70, "red", at=0.6))
sc("Nine different moments. Seven different Como scorers. Let's count them again, slowly, for the people of Lens.",
   *[P("football", 260 + i * 175, 500, 0.5, at=0.06 * i) for i in range(9)], C(0, 7, 960, 760, fmt="{:.0f} scorers", size=120, color="navy", at=0.6))
sc("Lens fans, to their credit, mostly kept supporting their team, according to ESPN's live commentary. Only occasional boos.",
   *CROWD(500, 1420, face="sad", pose="stand", kind=LFAN), T("occasional boos", 960, 320, 80, "dark", at=0.5), bg="sky")

# PART 2: THE RECORDS -------------------------------------------------------------
sc("Now, why is nine one such a big deal? Because of the records it touches.",
   T("RECORDS", 960, 420, 180, "red"), P("trophy", 960, 900, 1.0, at=0.4), chapter="Part 2: The record book")
sc("Record one: biggest winning margin. Eight goals. Before Wednesday, only two matches in Champions League history had ended with an eight-goal gap.",
   C(0, 8, 600, 430, fmt="+{:.0f}", size=260, color="red"), T("goal margin", 600, 640, 70, "dark", at=0.3), P("calendar", 1400, 860, 0.9, text="2007 / 2015", at=0.5))
sc("Liverpool eight, Besiktas nil, in two thousand seven. Real Madrid eight, Malmo nil, in two thousand fifteen. Both at home. Como did it away.",
   {"bars": {"values": [8, 8, 8], "labels": ["LIV 2007", "RMA 2015", "COMO 2026"], "colors": ["grey", "grey", "blue"], "fmt": "+{}", "w": 900, "h": 400}, "x": 960, "y": 860},
   {"stamp": "AWAY", "x": 1450, "y": 330, "size": 80, "w": 300, "at": 0.7})
sc("Record two: according to the Associated Press, Como are the first away team ever to score nine goals in a Champions League match.",
   G(600, "present", "smug", **COMO, label="away team"), C(0, 9, 1350, 430, fmt="{:.0f}", size=280, color="red", at=0.3))
sc("The previous best by a team not at home was Bayern Munich's eight-two against Barcelona in twenty twenty, at a neutral ground in Lisbon.",
   BOARD("BAR 2|BAY 8", 600, 760, 0.9), T("Lisbon, 2020", 1350, 400, 90, "navy", at=0.4), P("globe", 1350, 860, 0.7, at=0.5))
sc("Record three: only one other team has ever scored nine in a single Champions League game. Bayern again, nine-two against Dinamo Zagreb in twenty twenty-four.",
   C(0, 2, 600, 430, fmt="{:.0f} teams", size=170, color="navy"), T("ever scored 9", 600, 610, 70, "dark", at=0.3), G(1400, "shrug", "neutral", look=-1, extras=ECON, at=0.5))
sc("So the list of clubs to score nine is now Bayern Munich, one of the richest clubs on earth, and a team that was playing amateur football nine years ago.",
   P("building", 600, 900, 1.0, text="BAYERN"), T("&", 960, 520, 130, "red", at=0.3), P("lake", 1400, 900, 0.7, at=0.45, text="COMO"))
sc("The result lifted Como to fourth in the thirty-six team table. Lens dropped to thirty-third.",
   {"bars": {"values": [33, 4], "labels": ["Lens", "Como"], "colors": ["red", "blue"], "fmt": "#{}", "w": 600, "h": 400}, "x": 700, "y": 840},
   {"arrow": [[1250, 400], [1250, 700]], "color": "red", "at": 0.5}, T("lower is better", 1500, 330, 55, "dark", at=0.6))
sc("Quick note: if this kind of calm, numbers-first explainer is useful to you, subscribing is how we know to keep making them. Back to the money.",
   G(960, "wave", "happy", extras=DAVE), T("SUBSCRIBE?", 960, 320, 110, "red", at=0.3), bg="yellow")

# PART 3: WHERE COMO CAME FROM ---------------------------------------------------
sc("To understand the argument, you need Como's back story. The club was founded in nineteen-oh-seven, in a bar in the town.",
   P("calendar", 600, 860, 1.0, text="1907"), P("coffee", 1300, 860, 1.0, at=0.35), chapter="Part 3: From Serie D")
sc("Como sits on the shore of Lake Como, the one in the travel brochures. Famous for villas, boats, and celebrities on holiday. Not for football.",
   P("lake", 960, 900, 1.2), P("ship", 1300, 860, 0.5, at=0.4), P("house", 600, 760, 0.5, at=0.5))
sc("The club bounced between divisions for decades. It went bankrupt in two thousand four, and again in two thousand sixteen.",
   P("arrowdown", 600, 860, 1.0), P("calendar", 1050, 860, 0.8, text="2004"), P("calendar", 1500, 860, 0.8, text="2016", at=0.4), {"stamp": "BANKRUPT", "x": 1280, "y": 330, "size": 70, "w": 420, "at": 0.6})
sc("In twenty seventeen, a new company restarted it in Serie D. That's the level where some players have day jobs.",
   G(600, "hold", "tired", **COMO, label="Serie D"), P("clipboard", 1050, 860, 0.9, text="DAY JOB"), T("Level 4", 1450, 400, 110, "dark", at=0.4))
sc("In April twenty nineteen, a London-based media company called SENT Entertainment bought the club. Its owners: the Indonesian brothers Robert Budi and Michael Bambang Hartono.",
   P("building", 600, 900, 0.9, text="SENT"), G(1250, "present", "smug", look=-1, **OWN, label="owner", at=0.3), G(1550, "present", "smug", look=-1, **OWN, label="owner", at=0.4))
sc("The price, according to an ownership analysis published this week by the football finance blog The Esk, was about two hundred thousand euros.",
   C(0, 200000, 960, 420, fmt="€{:,.0f}", size=150, color="navy"), T("for a whole club", 960, 600, 70, "dark", at=0.4))
sc("That is less than some of the houses on the lake. Dave's reaction was to start checking if his local club is for sale.",
   G(600, "think", "grin", extras=DAVE), P("house", 1100, 900, 0.8, at=0.3), P("pricetag", 1500, 860, 0.9, text="€200k?", at=0.5), bg="yellow")
sc("It isn't. And even if it was, the purchase price turned out to be the cheapest part.",
   G(600, "facepalm", "sad", extras=DAVE), T("the cheap part", 1300, 420, 90, "red", at=0.35))
sc("Then the climb was fast. Three promotions in six seasons, BBC Sport counts. In twenty twenty-four, Como reached Serie A for the first time in twenty-one years.",
   *[P("arrowup", 450 + i * 300, 860, 0.8, at=0.15 * i) for i in range(3)], C(0, 21, 1500, 420, fmt="{:.0f} yrs", size=150, color="navy", at=0.5))
sc("Last May, Como finished fourth in Serie A, winning four one at Cremonese on the final day. Their first ever Champions League place.",
   BOARD("CRE 1|COMO 4", 600, 760, 0.9), C(0, 4, 1400, 420, fmt="#{:.0f}", size=240, color="blue", at=0.4), T("in Serie A", 1400, 600, 60, "dark", at=0.5))
sc("A lifelong fan, Michela Trombetta, told UEFA that qualifying for the Champions League was never something we imagined.",
   G(600, "present", "happy", extras=["bun"], shirt="blue", label="lifelong fan"), T("\"never something", 1300, 360, 70, "navy", at=0.3), T("we imagined\"", 1300, 450, 70, "navy", at=0.3))

# PART 4: THE MONEY ------------------------------------------------------------
sc("Now the other half of the story. The money. Because the Hartono brothers are not ordinary club owners.",
   P("moneybag", 960, 860, 1.6, anim="pulse"), chapter="Part 4: The money")
sc("Forbes put them first on its Indonesia rich list last December, with a combined fortune of forty-three point eight billion dollars.",
   C(0, 43.8, 960, 420, fmt="${:.1f}B", size=200, color="money"), T("Forbes, Dec 2025", 960, 620, 60, "dark", at=0.4))
sc("Most of that comes from a controlling stake in Bank Central Asia, Indonesia's largest private bank. The family business started out in cigarettes.",
   P("building", 600, 900, 1.0, text="BANK"), P("pricetag", 1300, 860, 1.0, at=0.4, text="DJARUM"))
sc("They have put real money into Como. Football Italia reports the club spent almost a hundred and twenty-seven million euros on new players last season.",
   C(0, 127, 960, 420, fmt="€{:.0f}M", size=200, color="red"), T("on new signings, 2025-26", 960, 610, 60, "dark", at=0.4))
sc("Only four Serie A clubs spent more: Juventus, Inter, Napoli and Roma. Those are some of the most famous names in Italian football.",
   *[G(450 + i * 340, "hips", "smug", look=1, extras=["tie"], shirt=c, s=0.8, at=0.12 * i) for i, c in enumerate(["dark", "navy", "sky", "orange"])],
   G(1750, "hips", "smug", look=-1, **COMO, s=0.8, at=0.6))
sc("And The Esk's analysis of the company accounts says that in twenty twenty-three, the owners put in fifty-seven million pounds, while the business brought in twelve point eight million.",
   {"bars": {"values": [57, 12.8], "labels": ["owners in", "revenue"], "colors": ["money", "grey"], "fmt": "£{}M", "w": 700, "h": 420}, "x": 900, "y": 860})
sc("So if you're asking whether Como is a poor team that got lucky, the answer is no. This is one of the best-funded projects in Italy.",
   G(600, "shrug", "neutral", extras=ECON), {"cross": [1350, 450, 160], "at": 0.3}, T("poor + lucky", 1350, 450, 70, "dark"))
sc("But here's the twist the other side points to. Spending on transfers is one thing. Wages are another.",
   G(600, "pointup", "think", extras=LINDA), P("wallet", 1350, 860, 1.1, at=0.4))
sc("By Football Italia's figures, Como had only the eleventh highest wage bill in Serie A. About forty-seven million euros.",
   C(0, 47, 960, 420, fmt="€{:.0f}M", size=200, color="blue"), T("#11 in Serie A", 960, 610, 80, "dark", at=0.4))
sc("Inter's was a hundred and thirty-nine million. Juventus, a hundred and twenty-nine. Como finished above clubs paying their players two or three times as much.",
   {"bars": {"values": [139, 129, 47], "labels": ["Inter", "Juve", "Como"], "colors": ["navy", "dark", "blue"], "fmt": "€{}M", "w": 900, "h": 440}, "x": 960, "y": 880})
sc("The reason: Como bought young players, who are cheaper to pay, and hoped they'd get better. So far, a lot of them have.",
   G(500, "point", "happy", **KID, s=0.8), G(800, "point", "happy", **KID, s=0.8, at=0.15), P("arrowup", 1300, 860, 1.0, at=0.4), T("young + cheap(er)", 1300, 360, 70, "navy", at=0.55))
sc("Linda's summary: they didn't win the lottery. They bought a lot of tickets, but they picked the numbers well.",
   G(960, "hips", "smug", extras=LINDA), P("pricetag", 1450, 860, 0.9, text="TICKETS", at=0.4), bg="yellow")

# PART 5: THE COACH -------------------------------------------------------------
sc("The other big piece is the coach. Cesc Fabregas, a former Arsenal, Barcelona and Chelsea midfielder, and a World Cup winner with Spain.",
   G(800, "present", "smug", **COACH, label="coach"), P("trophy", 1350, 860, 0.9, at=0.4), chapter="Part 5: The coach and the kids")
sc("He made his coaching debut with Como in Serie B in twenty twenty-four. He has also had a big say in which players the club signs.",
   P("clipboard", 600, 860, 1.0, text="SIGNINGS"), G(1300, "point", "think", look=-1, **COACH, at=0.3))
sc("After Wednesday's game, his verdict was short, as reported by AP: today everything went our way. A great night for Como and our fans.",
   G(600, "present", "happy", **COACH, label="coach"), T("\"Today everything", 1300, 360, 70, "navy", at=0.3), T("went our way.\"", 1300, 450, 70, "navy", at=0.3))
sc("Which is the most modest possible way to describe a nine one away win. Dave describes his good parking spots with more excitement.",
   G(600, "fist", "grin", extras=DAVE), P("car", 1250, 900, 1.0, at=0.3), T("PERFECT SPOT!", 1250, 450, 80, "red", at=0.5), bg="yellow")
sc("The football journalist Julien Laurens told the BBC that the owners invested a lot of money but without taking away the spirit the club had for years.",
   G(600, "think", "neutral", extras=ECON, label="journalist"), P("moneybag", 1150, 860, 0.8, at=0.3), T("+ spirit", 1500, 450, 90, "blue", at=0.5))
sc("The striker Douvikas now leads the whole Champions League with six goals. More than anyone else in the competition so far.",
   C(0, 6, 600, 430, fmt="{:.0f}", size=260, color="red"), T("goals, #1", 600, 630, 70, "dark", at=0.3), G(1400, "fist", "grin", look=-1, **COMO, label="striker", at=0.45))
sc("The substitute Liberali came on in the fifty-eighth minute and finished with a goal and two assists in about half an hour.",
   P("stopwatch", 600, 860, 1.0, text="58'"), T("1 goal + 2 assists", 1300, 430, 80, "navy", at=0.4))
sc("And the eighteen-year-old who scored the ninth goal came through Como's own youth team. That part, at least, money didn't buy.",
   G(700, "fist", "grin", **KID, label="youth team"), P("school", 1350, 900, 0.8, at=0.4))

# PART 6: THE OTHER TEAM ------------------------------------------------------------
sc("Now, the team on the other end of this. Because Lens is an underdog story too.",
   G(960, "stand", "sad", **LENS), chapter="Part 6: The other underdog")
sc("Lens is a former coal-mining town in northern France. Its stadium holds about thirty-eight thousand people. That's more people than live in Lens.",
   P("building", 600, 900, 0.9, text="MINE"), C(0, 38223, 1350, 420, fmt="{:,.0f}", size=150, color="red", at=0.3), T("seats", 1350, 580, 60, "dark", at=0.4))
sc("The fans are famous in France. The club doesn't use the number twelve shirt, because the supporters are treated as the twelfth player.",
   P("pricetag", 600, 860, 1.0, text="#12"), {"cross": [600, 760, 120], "at": 0.3}, *CROWD(1000, 1700, at=0.4, kind=LFAN))
sc("Lens started this Champions League campaign well: a three two win away in Prague, in September.",
   BOARD("SLA 2|LENS 3", 700, 760, 0.9), G(1400, "fist", "happy", look=-1, **LENS, at=0.4))
sc("Then came losses to Sporting and Club Brugge. And then Wednesday. Twelve goals conceded in the last three games combined, nine of them in one night.",
   BOARD("0 - 2", 450, 700, 0.6), BOARD("0 - 3", 960, 700, 0.6, at=0.2), BOARD("1 - 9", 1470, 700, 0.6, at=0.4), C(0, 14, 960, 300, fmt="{:.0f} conceded", size=90, color="red", at=0.6))
sc("Correction from our fact-checker, Linda: that's fourteen. Two, three and nine. She'd like it noted that she always checks the maths.",
   G(700, "point", "smug", extras=LINDA), T("2 + 3 + 9 = 14", 1300, 420, 100, "navy", at=0.3), bg="yellow")
sc("The Lens goalkeeper faced eleven shots on target. That's ESPN's count. He wasn't the problem. He was simply very, very busy.",
   *PITCH(), P("goal", 960, 900, 1.0), G(960, "panic", "scream", **GK, at=0.1), *[P("football", 300 + i * 250, 450 + (i % 2) * 100, 0.4, at=0.1 * i) for i in range(6)])
sc("So one way to see Wednesday: one small town having the best night of its life, against another small town having its worst.",
   P("lake", 550, 900, 0.7, text="COMO"), T("vs", 960, 520, 120, "red", at=0.3), P("building", 1400, 900, 0.8, text="LENS", at=0.4))

# PART 7: BOTH SIDES / WHAT'S NEXT -----------------------------------------------
sc("So, underdog or billionaire project? Here's the case each side makes.",
   G(500, "point", "angry", **COMO, label="underdog"), G(1420, "point", "angry", look=-1, **OWN, label="project", at=0.2), chapter="Part 7: Underdog or project?")
sc("The underdog case: nine years ago this was a fourth division club. The city has eighty-three thousand people. The stadium holds about eleven thousand for Champions League games.",
   P("calendar", 450, 860, 0.8, text="2017"), C(0, 83000, 960, 420, fmt="{:,.0f}", size=110, color="navy", at=0.3), C(0, 11000, 1450, 420, fmt="{:,.0f} seats", size=90, color="blue", at=0.5))
sc("And money alone doesn't guarantee this. Plenty of rich owners have spent big and stayed stuck in mid-table.",
   P("moneybag", 600, 860, 1.0), P("arrowdown", 1000, 860, 0.8, at=0.3), G(1450, "shrug", "sad", look=-1, **OWN, at=0.5))
sc("The project case: the owners are among Asia's richest people. The Esk's analysis of the accounts shows them putting in far more than the club earns.",
   C(0, 43.8, 600, 420, fmt="${:.1f}B", size=150, color="money"), {"bars": {"values": [57, 12.8], "labels": ["in", "earned"], "colors": ["money", "grey"], "fmt": "£{}M", "w": 500, "h": 360}, "x": 1350, "y": 860, "at": 0.4})
sc("And the Esk's analysis estimates that even good Champions League prize money, thirty to fifty million euros for a first-timer, won't cover the club's losses yet.",
   T("€30-50M", 600, 420, 130, "money"), T("prize money", 600, 580, 60, "dark", at=0.2), G(1400, "think", "worried", look=-1, extras=ECON, at=0.4), T("< losses", 1400, 330, 80, "red", at=0.55))
sc("Depending on who you ask, Como is either proof that smart spending beats big spending, or proof that you need a very rich owner to even start.",
   P("scale", 960, 900, 1.3), T("SMART", 650, 380, 80, "blue", at=0.3), T("RICH", 1270, 380, 80, "money", at=0.4))
sc("We just count the facts. And the facts include this: Como lost three two to Feyenoord in October. They are good, not unbeatable.",
   BOARD("FEY 3|COMO 2", 700, 760, 0.9), G(1400, "shrug", "neutral", look=-1, **COMO, at=0.4))
sc("What's next? Under this format, the top eight teams after eight games go straight into the round of sixteen. Teams ninth to twenty-fourth go into a playoff.",
   {"box": [400, 320, 520, 140], "color": "green"}, T("1-8: last 16", 660, 390, 60, "dark"), {"box": [1000, 320, 520, 140], "color": "yellow", "at": 0.4}, T("9-24: playoff", 1260, 390, 60, "dark", at=0.4),
   chapter="What's next")
sc("Como play AEK Athens at home on November twenty-fourth, then Real Betis in December.",
   P("calendar", 600, 860, 1.0, text="NOV 24"), P("calendar", 1300, 860, 1.0, text="DEC 9", at=0.4))
sc("Then the hard part: Paris Saint-Germain at home in January, and a final trip to Barcelona on January twenty-seventh.",
   P("calendar", 600, 860, 1.0, text="JAN 20"), P("calendar", 1300, 860, 1.0, text="JAN 27", at=0.3), G(960, "panic", "worried", **COMO, s=0.7, at=0.5))
sc("Lens, meanwhile, still have Leipzig, Bodo Glimt, Manchester City and Liverpool to come. Thirty-third isn't the end, but they need points fast.",
   P("calendar", 500, 860, 0.8, text="4 LEFT"), G(1300, "fist", "worried", look=-1, **LENS, at=0.4))

# RECAP ---------------------------------------------------------------------
sc("Recap. Como beat Lens nine one away, the first away team to score nine in the Champions League, matching the biggest winning margin ever.",
   BOARD("LENS 1|COMO 9", 960, 760, 1.1), chapter="Recap")
sc("Nine years ago they were bankrupt and in Serie D. Since twenty nineteen, Indonesia's richest family has paid for the climb.",
   P("calendar", 600, 860, 0.9, text="2017"), {"arrow": [[800, 600], [1150, 600]], "color": "red", "at": 0.3}, P("moneybag", 1400, 860, 1.0, at=0.5))
sc("But they got here with young players, a first-time coach and only the eleventh biggest wage bill in Italy.",
   G(500, "fist", "grin", **KID, s=0.8), G(960, "present", "smug", **COACH, s=0.9, at=0.2), T("#11 wages", 1450, 420, 90, "blue", at=0.4))
sc("Somewhere in Lens, a goalkeeper is still seeing footballs when he closes his eyes. We wish him a quiet week.",
   G(960, "stand", "tired", **GK), *[P("football", 500 + i * 230, 330, 0.35, at=0.15 * i, anim="bob") for i in range(5)], bg="sky")
sc("Your turn. Is Como an underdog story or a billionaire project? Or can it be both? Tell us in the comments.",
   T("UNDERDOG or PROJECT?", 960, 380, 100, "red"), G(960, "think", "neutral", extras=LINDA, at=0.4))
sc("If this helped, subscribe for calm, stick-figure explainers. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), T("THE DOODLE DESK", 960, 330, 100, "navy", at=0.3))

CUT = ["A three goal lead at half time", "Nine different moments.", "So the list of clubs to score nine", "Como sits on the shore",
       "It isn't. And even if", "And The Esk's analysis of the company accounts", "He made his coaching debut", "The substitute Liberali",
       "Lens, meanwhile, still have"]
S[:] = [x for x in S if not any(x["say"].startswith(c) for c in CUT)]

script = {
    "id": "ep020",
    "title": "Como Scored 9 in the Champions League. Underdog or Not?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Nov 4, 2026 Como, a club from a lake town of about 83,000 people, beat Lens 9-1 away in the UEFA Champions League. It is the first away team "
        "ever to score nine in the competition, and it matched the biggest winning margin in Champions League history. Nine years ago, Como was bankrupt and in Serie D. "
        "We go through the night goal by goal, the records, the club's climb since Indonesia's Hartono family bought it in 2019, the money "
        "(about EUR 127M on signings last season, but only the 11th-highest wage bill in Serie A), coach Cesc Fabregas, the other underdog (Lens), and what comes next. "
        "Real people appear only as generic labelled stick figures; quotes are as reported.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "AP via Newsday, Como becomes 1st away team to score 9 goals in a Champions League match (Nov 4, 2026): https://www.newsday.com/sports/soccer/como-champions-league-n97509\n"
        "UEFA.com, Biggest Champions League wins: Lens 1-9 Como: https://www.uefa.com/uefachampionsleague/news/0240-0e935cdfe0e3-72b3c5cde380-1000--biggest-champions-league-wins-liverpool-8-0-besiktas-rea/\n"
        "UEFA.com, Champions League round-up, Nov 5, 2026: https://www.uefa.com/uefachampionsleague/news/02ab-21fe508a035b-5eed0199e0b2-1000--champions-league-highlights-and-round-up-como-equal-bigges/\n"
        "ESPN, Lens 1-9 Como match page and commentary: https://www.espn.com/soccer/match/_/gameId/401915305/como-lens\n"
        "UEFA.com, Como's remarkable road to the Champions League: https://www.uefa.com/uefachampionsleague/news/02a9-217ee7d71634-0271b4ccb49a-1000--como-s-remarkable-road-to-the-champions-league/\n"
        "BBC Sport, Como 4-1 RB Leipzig: https://www.bbc.co.uk/sport/football/live/cm4g56rwxew2t\n"
        "Football Italia, Como qualify for Champions League with 11th wage bill in Serie A (May 25, 2026): https://football-italia.net/como-qualify-champions-league-11th-wage-bill\n"
        "The Esk, Como 1907 ownership and owner funding analysis (Nov 3, 2026): https://theesk.org/2026/11/03/the-analysis-series-como-1907-ownership-owner-funding-2025-26/\n\n"
        "#championsleague #como #lens #football #soccer #underdog #explained #stickfigure"
    ),
    "tags": ["como", "como 1907", "lens vs como", "como 9-1", "champions league", "champions league record", "fabregas", "hartono",
             "football underdog", "serie a", "football explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "SERIE D|TO 9-1", "size": 190, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["hair"], "shirt": "red"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "football", "x": 380, "y": 1000, "s": 2.0}, {"arrow": [[600, 760], [980, 600]], "color": "red"}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep020.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

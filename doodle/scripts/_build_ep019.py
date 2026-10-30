"""Episode 19: Milwaukee Brewers, MLB's smallest market, win their first World Series (beat Rays 4-1 in five games, Oct 28, 2026)."""
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



MIL = dict(extras=["cap"], shirt="navy")          # generic Brewers player
TB = dict(extras=["cap"], shirt="teal")           # generic Rays player
MGR = dict(extras=["cap", "glasses"], shirt="navy")
FAN = dict(extras=["cap"], shirt="gold")
OWN = dict(extras=["tie", "tophat"], shirt="grey")


def STADIUM(x=960, at=0, label=None):
    out = [{"box": [x - 700, 560, 1400, 340], "color": "grey", "at": at},
           {"box": [x - 640, 600, 1280, 60], "color": "white", "at": at},
           {"box": [x - 640, 700, 1280, 60], "color": "white", "at": at},
           {"box": [x - 640, 800, 1280, 60], "color": "white", "at": at}]
    if label:
        out.append({"text": label, "x": x, "y": 520, "size": 60, "color": "navy", "outline": "white", "at": at})
    return out


def CROWD(x0, x1, at=0, face="happy", pose="fist", **kw):
    out = []
    step = (x1 - x0) // 5
    for i in range(6):
        out.append(G(x0 + i * step, pose, face, look=1 if i % 2 else -1, s=0.55, y=900, at=at + 0.04 * i if at < 1 else at, **FAN))
    return out


def MAP(at=0):
    return [P("globe", 960, 760, 1.0, at=at)]


# COLD OPEN ------------------------------------------------------------------
sc("On Wednesday night, thirty-one thousand people filled a baseball stadium in Milwaukee.",
   *STADIUM(label="MILWAUKEE"), *CROWD(560, 1360, at=0.3), cam={"from": [960, 640, 1.3], "to": [960, 540, 1.0]}, bg="sky")
sc("The game was in Florida.",
   P("tv", 960, 520, 1.6), T("FLORIDA", 960, 480, 70, "teal", at=0.3), *CROWD(560, 1360, face="worried", pose="stand"), bg="sky")
sc("They paid to sit in their own ballpark and watch a screen, more than a thousand miles from the actual game.",
   P("tv", 600, 520, 1.1), {"arrow": [[820, 520], [1250, 520]], "color": "red", "at": 0.3}, C(0, 1000, 1500, 420, fmt="{:,.0f}+ mi", size=110, color="navy", at=0.45))
sc("Then, at eleven thirteen p.m., a ground ball to second base. The Milwaukee Brewers won the World Series. The first title in the team's history.",
   P("baseball", 500, 500, 0.6, move=[900, 860]), G(1100, "fist", "grin", **MIL, at=0.35), P("trophy", 1500, 760, 1.3, at=0.55, anim="bob"))
sc("Milwaukee is the smallest TV market in Major League Baseball. Thirtieth out of thirty.",
   C(30, 30, 700, 420, fmt="#{:.0f}", size=260, color="red", dur=0.1), T("of 30 markets", 700, 640, 70, "dark", at=0.3), G(1450, "shrug", "smug", look=-1, extras=DAVE, at=0.5))
S.append({"say": "So here's the puzzle. In a sport with no salary cap, where the rich can outspend everyone, how does the smallest city win the whole thing?",
          "items": [P("moneybag", 500, 860, 1.5), T("vs", 960, 520, 140, "red", at=0.3), P("house", 1450, 900, 0.8, at=0.45), T("?", 1450, 360, 200, "red", at=0.6)],
          "chapter": "Today's question"})
sc("We'll go through the five games, the money, the trades, the other team's strange year, and the fight about to start in December.",
   P("scoreboard", 500, 760, 0.8, text="5"), P("dollar", 960, 640, 1.0, at=0.25), P("calendar", 1450, 860, 0.9, text="DEC 1", at=0.5))

# PART 1: FIVE GAMES ----------------------------------------------------------
sc("First, what happened. The Brewers played the Tampa Bay Rays. Two teams that finished with the best records in their leagues.",
   G(600, "stand", "neutral", **MIL, label="Brewers"), T("vs", 960, 450, 120, "red", at=0.2), G(1320, "stand", "neutral", look=-1, **TB, label="Rays", at=0.3),
   chapter="Part 1: Five games")
sc("Milwaukee won a hundred and three games this season. A franchise record, and the best in baseball.",
   C(0, 103, 700, 420, fmt="{:.0f}", size=260, color="navy"), T("wins", 700, 640, 80, "dark", at=0.3), {"stamp": "RECORD", "x": 1400, "y": 420, "size": 90, "w": 380, "at": 0.55})
sc("Game one, in Milwaukee: Brewers three, Rays two. Decided on the last pitch.",
   P("scoreboard", 960, 760, 1.0, text="MIL 3|TB 2"), G(450, "fist", "grin", **MIL, at=0.4), G(1500, "facepalm", "sad", look=-1, **TB, at=0.4))
sc("Game two: the Rays led four to nothing. Milwaukee chipped away and won by one run again.",
   P("scoreboard", 700, 760, 0.9, text="TB 4|MIL 0"), {"arrow": [[1000, 600], [1250, 600]], "color": "red", "at": 0.4}, T("MIL by 1", 1500, 520, 100, "navy", at=0.55))
sc("Game three, in Florida, was the strange one. In the fifth inning, with two outs, Milwaukee scored eight runs.",
   P("scoreboard", 600, 760, 0.9, text="2 OUTS"), C(0, 8, 1350, 420, fmt="+{:.0f} runs", size=170, color="red", at=0.35))
sc("Seven hits in a row, all with two outs. According to the AP, no World Series team had ever scored eight two-out runs in one inning.",
   *[P("baseball", 380 + i * 190, 420, 0.45, at=0.06 * i) for i in range(7)], {"stamp": "NEVER BEFORE", "x": 960, "y": 720, "size": 80, "w": 600, "at": 0.6})
sc("Final score: ten to one. A Brewers rookie pitcher said that normally it's thirty-five thousand against nine, but that night they had twenty thousand people behind them.",
   P("scoreboard", 600, 760, 0.9, text="MIL 10|TB 1"), G(1400, "present", "grin", look=-1, **MIL, label="rookie pitcher", at=0.3), T("\"20,000 behind us\"", 1400, 300, 60, "navy", at=0.5))
sc("Game four went twelve innings. Milwaukee was three outs from the title. The Rays came back and won it at the very end.",
   C(0, 12, 600, 420, fmt="{:.0f} inn.", size=200, color="dark"), G(1300, "fist", "grin", look=-1, **TB, at=0.4), G(1650, "cry", "sad", look=-1, **MIL, at=0.5))
sc("Dave watched that one from his couch. He says he aged three years. His wife says it was more like five.",
   G(600, "panic", "scream", extras=DAVE), P("tv", 1150, 560, 0.9), G(1550, "hips", "tired", look=-1, extras=LINDA, at=0.5), bg="yellow")
sc("Game five, back in Florida: Brewers four, Rays one.",
   P("scoreboard", 960, 760, 1.1, text="MIL 4|TB 1"), P("trophy", 1550, 760, 1.0, at=0.4, anim="bob"))
sc("Their starting pitcher threw fifty-one fastballs at a hundred miles an hour or faster, according to the AP, before a calf cramp ended his night.",
   G(500, "point", "angry", **MIL, label="starter"), P("baseball", 650, 600, 0.5, move=[1500, 600]), C(0, 51, 1350, 380, fmt="{:.0f}", size=200, color="red", at=0.4), T("pitches 100+ mph", 1350, 560, 60, "dark", at=0.6))
sc("Three relievers finished the job. Final out: a ground ball to second. That's the one the people in Milwaukee watched on the big screen.",
   G(500, "fist", "grin", **MIL), G(800, "fist", "grin", **MIL, at=0.15), G(1100, "fist", "grin", **MIL, at=0.3), P("tv", 1550, 520, 0.9, at=0.5))
sc("Over five games, the Brewers outhit Tampa Bay fifty-one to thirty and outscored them twenty-five to twelve.",
   {"bars": {"values": [51, 30], "labels": ["MIL hits", "TB hits"], "colors": ["navy", "teal"], "fmt": "{}", "w": 600, "h": 400}, "x": 600, "y": 840},
   {"bars": {"values": [25, 12], "labels": ["MIL runs", "TB runs"], "colors": ["navy", "teal"], "fmt": "{}", "w": 600, "h": 400}, "x": 1350, "y": 840, "at": 0.4})

# PART 2: THE STARS -----------------------------------------------------------
sc("The series MVP was the catcher, William Contreras. Eight hits in twenty-one at-bats.",
   G(600, "fist", "grin", extras=["cap", "hardhat"], shirt="navy", label="catcher, MVP"), T("8 / 21", 1350, 420, 180, "navy", at=0.35), chapter="Part 2: The stars nobody paid for")
sc("A rookie shortstop, Cooper Pratt, hit four twenty-one in the series and set a rookie record: hits in six straight World Series at-bats.",
   G(550, "hold", "smug", **MIL, label="rookie"), P("bat", 680, 900, 0.9), C(0, 0.421, 1300, 380, fmt="{:.3f}", size=170, color="navy", at=0.3), T("6 straight hits", 1300, 580, 80, "red", at=0.55))
sc("He didn't play his first big-league game until June sixteenth. Four months later, he's in the record book.",
   P("calendar", 600, 860, 1.0, text="JUN 16"), {"arrow": [[800, 600], [1150, 600]], "color": "red", "at": 0.3}, P("trophy", 1450, 760, 1.0, at=0.5))
sc("And the captain, Christian Yelich, who arrived in twenty eighteen, said it felt like a movie.",
   G(700, "present", "happy", **MIL, label="captain"), T("\"It felt like a movie.\"", 1300, 380, 80, "navy", at=0.3), P("tv", 1350, 700, 0.6, at=0.55))
sc("Their manager, Pat Murphy, said, we came in with a spirit about us, and we weren't going to be denied.",
   G(600, "point", "grin", **MGR, label="manager"), T("\"we weren't going to", 1300, 360, 64, "navy", at=0.3), T("be denied\"", 1300, 460, 64, "navy", at=0.4))
sc("Notice something about this list? Almost nobody on it is a superstar who signed for a fortune.",
   G(500, "stand", "neutral", **MIL), G(800, "stand", "neutral", **MIL), G(1100, "stand", "neutral", **MIL), P("moneybag", 1550, 860, 1.1, at=0.4), {"cross": [1550, 760, 160], "at": 0.6})

# PART 3: THE MONEY -----------------------------------------------------------
sc("Now the money. Major League Baseball has no salary cap. Each team spends what its owner wants to spend.",
   P("moneybag", 500, 860, 1.4), P("moneybag", 900, 860, 0.9, at=0.2), P("moneybag", 1250, 860, 0.5, at=0.4), T("NO CAP", 1550, 400, 120, "red", at=0.55), chapter="Part 3: The money")
sc("According to SB Nation's figures, Milwaukee's payroll is about a hundred forty-six million dollars. Nineteenth in the league.",
   C(0, 146, 700, 420, fmt="${:.0f}M", size=220, color="navy"), T("#19", 1400, 420, 200, "dark", at=0.4))
sc("Tampa Bay's is about ninety-five million. Depending on which list you use, somewhere between twenty-fifth and twenty-eighth.",
   C(0, 95, 700, 420, fmt="${:.0f}M", size=220, color="teal"), T("#25 - #28", 1400, 420, 130, "dark", at=0.4))
sc("For comparison, the same article estimates the Los Angeles Dodgers' payroll at about four hundred twelve million.",
   {"bars": {"values": [412, 146, 95], "labels": ["Dodgers", "Brewers", "Rays"], "colors": ["red", "navy", "teal"], "fmt": "${}M", "w": 1000, "h": 480}, "x": 960, "y": 860})
sc("Put the two finalists together, and CBS Sports says their payroll rankings are the lowest ever for a World Series.",
   G(600, "shrug", "grin", **MIL), G(1300, "shrug", "grin", look=-1, **TB, at=0.2), {"stamp": "LOWEST EVER", "x": 960, "y": 360, "size": 90, "w": 560, "at": 0.45})
sc("And the smallest combined market for a World Series since nineteen eighty-five.",
   P("house", 700, 900, 0.8), P("house", 1200, 900, 0.8, at=0.2), T("since 1985", 960, 380, 130, "navy", at=0.4))
sc("Both teams also receive more money from baseball's revenue sharing than they pay in. CBS says that can cover most or all of a low-payroll team's cash payroll.",
   P("moneybag", 500, 860, 1.2), {"arrow": [[700, 600], [1200, 600]], "color": "green", "at": 0.3}, G(1450, "hold", "happy", look=-1, **MIL, at=0.5))
sc("Which is a polite way of saying part of the bill was paid by richer teams. Those teams will be bringing that up.",
   G(600, "point", "angry", **OWN, label="big-market owner"), P("envelope", 1100, 650, 0.9, at=0.3), G(1500, "shrug", "smug", look=-1, **MIL, at=0.5), bg="yellow")
sc("Quick one. If ten calm minutes of stick figures beat an hour of shouting sports radio for you, subscribe. That's the whole service.",
   G(700, "wave", "happy", extras=DAVE), T("SUBSCRIBE", 1350, 420, 120, "red", at=0.3), P("tv", 1350, 720, 0.6, at=0.5))

# PART 4: HOW THEY BUILT IT ----------------------------------------------------
sc("So how do you build a champion on a medium budget? Mostly, you trade.",
   P("clipboard", 600, 860, 1.2, text="TRADES"), {"arrow": [[850, 500], [1150, 500]], "color": "navy", "at": 0.3}, {"arrow": [[1150, 620], [850, 620]], "color": "teal", "at": 0.45},
   chapter="Part 4: How you build it cheap")
sc("CBS Sports counted twenty-two players on Milwaukee's forty-man roster who came by trade. Tampa Bay had twenty-four, the most in baseball.",
   C(0, 22, 600, 420, fmt="{:.0f}", size=230, color="navy"), C(0, 24, 1350, 420, fmt="{:.0f}", size=230, color="teal", at=0.35), T("MOST", 1350, 640, 80, "red", at=0.6))
sc("Their MVP catcher came in a trade. So did the captain, back in twenty eighteen.",
   G(600, "stand", "happy", extras=["cap", "hardhat"], shirt="navy"), {"arrow": [[800, 500], [1150, 500]], "color": "red", "at": 0.3}, G(1400, "stand", "happy", look=-1, **MIL, label="captain", at=0.4))
sc("The other half is growing your own. Players Milwaukee drafted and developed produced just over half of the team's value this season, by one common stat.",
   P("chart", 600, 860, 1.0), C(0, 50, 1350, 420, fmt="{:.0f}%+", size=220, color="green", at=0.35), T("homegrown", 1350, 620, 70, "dark", at=0.55))
sc("CBS says both teams share a style. Hitters who make contact instead of swinging for the moon. Pitchers who throw hard. Big scouting departments.",
   P("bat", 500, 900, 1.0), P("baseball", 900, 500, 0.6, at=0.2), P("magnifier", 1350, 650, 1.0, at=0.4), G(1650, "think", "neutral", look=-1, extras=ECON, at=0.55))
sc("And they're cousins. Milwaukee's head of baseball operations spent nine years in Tampa Bay's front office before moving north.",
   G(600, "hold", "neutral", extras=["tie", "glasses"], shirt="navy", label="Brewers boss"), P("calendar", 1100, 860, 0.8, text="9 YEARS", at=0.3), G(1500, "wave", "happy", look=-1, extras=["tie"], shirt="teal", label="Rays office", at=0.45))
sc("So the World Series was, in a way, the student against the school.",
   P("school", 1250, 900, 1.0), G(600, "point", "smug", extras=["tie", "glasses"], shirt="navy"), T("student vs school", 960, 300, 90, "navy", at=0.4))
sc("The trick is not secret. It's just hard. You have to judge young players in other teams' systems better than those teams do.",
   P("magnifier", 600, 650, 1.2), G(1100, "stand", "neutral", s=0.7, **TB), G(1350, "stand", "neutral", s=0.7, **MIL), G(1600, "stand", "happy", s=0.7, extras=["cap"], shirt="red", at=0.4))
sc("Dave tried this method on his fantasy league. He traded his best player for three teenagers. He is now in last place, but he says the future is bright.",
   G(600, "present", "smug", extras=DAVE), C(0, 12, 1350, 420, fmt="#{:.0f}", size=200, color="red", at=0.35), T("of 12", 1350, 600, 70, "dark", at=0.5), bg="yellow")

# PART 5: FORTY-FOUR YEARS -------------------------------------------------------
sc("Now, why this hit Milwaukee so hard. This was the team's fifty-seventh season in the city.",
   C(0, 57, 960, 420, fmt="{:.0f}th", size=240, color="navy"), T("season", 960, 640, 80, "dark", at=0.3), chapter="Part 5: Forty-four years")
sc("Their only other World Series was in nineteen eighty-two. They lost it in game seven.",
   P("calendar", 600, 860, 1.0, text="1982"), P("scoreboard", 1300, 760, 0.9, text="GAME 7", at=0.3), {"cross": [1300, 620, 150], "at": 0.6})
sc("And the city's last championship of any kind in baseball was in nineteen fifty-seven, by a different team, the Milwaukee Braves, who later left town.",
   P("trophy", 600, 760, 1.0, color="grey"), T("1957", 600, 400, 130, "dark", at=0.2), P("truck", 1350, 900, 1.0, at=0.4, move=[1800, 900]))
sc("Before Wednesday, five current teams had never won a World Series. Now it's four. The Rays are still on that list, along with San Diego, Colorado and Seattle.",
   C(5, 4, 700, 420, fmt="{:.0f}", size=280, color="red", dur=1.0), T("never won", 700, 650, 70, "dark", at=0.3), G(1400, "stand", "sad", look=-1, **TB, at=0.45))
sc("One more stat. CBS says this is the first time since at least nineteen ninety-five that the team with the better record won every single playoff series.",
   T("since 1995", 960, 380, 150, "navy"), G(1500, "shrug", "confused", look=-1, extras=ECON, at=0.45))
sc("In other words, in a sport famous for chaos, the best team simply won. Somewhere, a statistician is checking his spreadsheet twice.",
   P("chart", 600, 860, 1.0), G(1300, "panic", "shock", look=-1, extras=ECON, at=0.3), bg="yellow")
sc("Milwaukee went eleven and two in the playoffs, and outscored opponents fifty-nine to thirty-two.",
   C(0, 11, 600, 420, fmt="{:.0f}-2", size=220, color="navy"), C(0, 59, 1350, 420, fmt="{:.0f}-32", size=180, color="dark", at=0.4))
sc("Along the way, they swept the Los Angeles Dodgers, the two-time defending champions, who had knocked Milwaukee out three times in the previous eight years.",
   P("scoreboard", 700, 760, 0.9, text="4 - 0"), G(1400, "facepalm", "sad", look=-1, extras=["cap"], shirt="blue", label="Dodgers", at=0.4))

# PART 6: THE OTHER SIDE ----------------------------------------------------------
sc("Now the Rays, because their year was strange in a completely different way.",
   G(960, "stand", "neutral", **TB, label="Rays"), chapter="Part 6: The team without a roof")
sc("In October twenty twenty-four, Hurricane Milton badly damaged the roof of their stadium in St. Petersburg.",
   P("building", 700, 900, 1.0), P("cloud", 900, 300, 1.2, at=0.2, anim="shake"), P("calendar", 1450, 860, 0.9, text="OCT 2024", at=0.45))
sc("They spent all of twenty twenty-five playing in a spring training ballpark that belongs to the New York Yankees.",
   *STADIUM(label="BORROWED"), G(960, "shrug", "tired", **TB, at=0.4))
sc("They came home this April after a renovation of nearly sixty million dollars, with new owners, and a deal for a brand-new thirty-one-thousand-seat ballpark in Tampa, due in twenty twenty-nine.",
   C(0, 60, 600, 420, fmt="${:.0f}M", size=180, color="money"), P("building", 1300, 900, 1.0, at=0.35), T("2029", 1300, 340, 120, "teal", at=0.55))
sc("And then they won ninety-eight games and the American League pennant. That's not a team that failed. That's a team that ran out of October.",
   C(0, 98, 700, 420, fmt="{:.0f}", size=240, color="teal"), T("wins", 700, 640, 70, "dark", at=0.3), P("trophy", 1400, 760, 1.0, at=0.5, color="teal"))
sc("A detail from game five: the CBS live blog says the grounds crew had to repair the pitcher's mound at least four times, because the clay kept breaking up.",
   G(600, "hold", "tired", extras=["cap"], shirt="green", label="grounds crew"), C(0, 4, 1300, 420, fmt="{:.0f}x", size=220, color="red", at=0.4))
sc("Rays outfielder Chandler Simpson told the AP he was definitely disappointed in how it ended, but that the team can be proud of its season.",
   G(700, "stand", "sad", **TB, label="outfielder"), T("\"definitely disappointed\"", 1300, 420, 70, "teal", at=0.35))
sc("Their manager, Kevin Cash, said he remains excited about the players and people they have coming.",
   G(700, "present", "neutral", extras=["cap", "glasses"], shirt="teal", label="Rays manager"), P("arrowup", 1350, 700, 1.2, color="teal", at=0.4))

# PART 7: THE DECEMBER FIGHT -----------------------------------------------------
sc("Now, the part that isn't about baseball at all. Baseball's labor deal between owners and players expires on December first.",
   P("calendar", 960, 860, 1.4, text="DEC 1"), G(500, "hold", "worried", **OWN, at=0.3), G(1450, "hold", "worried", look=-1, extras=["cap"], shirt="red", label="players", at=0.4),
   chapter="Part 7: The December fight")
sc("One of the biggest questions in those talks is whether baseball should have a salary cap. A limit on spending, and maybe a minimum too.",
   T("CAP?", 600, 400, 200, "red"), T("FLOOR?", 1350, 400, 180, "navy", at=0.35))
sc("So everybody is now using this World Series as evidence. Depending on who you ask, it proves opposite things.",
   G(600, "point", "angry", extras=["tie"], shirt="red"), P("scoreboard", 960, 760, 0.7, text="MIL 4|TB 1"), G(1320, "point", "angry", look=-1, extras=["tie"], shirt="blue", at=0.3))
sc("One side says: look, smart teams can win without a cap. Spend wisely, trade well, develop players, and you can beat anyone.",
   G(600, "present", "smug", extras=["tie"], shirt="blue"), P("trophy", 1200, 760, 1.0, at=0.3), P("house", 1550, 900, 0.7, at=0.45))
sc("The other side points to the numbers. An SB Nation writer counted only three champions since two thousand with payrolls outside the top fifteen.",
   G(600, "present", "neutral", extras=["tie"], shirt="red"), C(0, 3, 1300, 420, fmt="{:.0f}", size=260, color="red", at=0.35), T("since 2000", 1300, 640, 70, "dark", at=0.5))
sc("The two thousand three Marlins, the twenty fifteen Royals and the twenty seventeen Astros. Meanwhile, top-five payroll teams won ten times.",
   T("2003  2015  2017", 960, 340, 100, "navy"), {"bars": {"values": [10, 3], "labels": ["top-5 payroll", "outside top 15"], "colors": ["red", "navy"], "fmt": "{}", "w": 760, "h": 380}, "x": 960, "y": 860, "at": 0.35})
sc("His argument: one small-market World Series doesn't change the need for a cap and a floor.",
   G(700, "point", "neutral", extras=["glasses"], shirt="red", label="columnist"), T("1 October", 1300, 380, 90, "dark", at=0.3), T("≠ a trend", 1300, 520, 90, "red", at=0.5))
sc("A CBS power rankings column took the other view, and its headline said it was time to finally stop talking about market size.",
   G(700, "point", "smug", extras=["glasses"], shirt="blue", label="columnist"), P("speech", 1300, 450, 1.0, text="STOP", at=0.35))
sc("Both can be true at once. Smart teams can win. And money still makes winning a lot easier, more often. We don't pick a side here. We just count.",
   P("scale", 960, 860, 1.4), P("moneybag", 700, 520, 0.6, at=0.3), P("magnifier", 1220, 560, 0.6, at=0.45))
sc("If the talks go badly, there could be a work stoppage. Nobody knows yet. We'll cover it when there are facts, not guesses.",
   P("lock", 700, 650, 1.0), P("calendar", 1300, 860, 0.9, text="2027?", at=0.35), G(1650, "think", "worried", look=-1, extras=DAVE, at=0.5))

# WHAT'S NEXT ---------------------------------------------------------------------
sc("What's next, short term: a parade. Friday at ten a.m. Central time, through downtown Milwaukee, ending at the Summerfest grounds.",
   *CROWD(450, 1450, at=0.2), P("calendar", 960, 400, 0.8, text="FRI 10AM"), chapter="What's next")
sc("The manager is up for a third straight Manager of the Year award next month. The AP says the game-five starter is on track for the Cy Young.",
   P("trophy", 600, 760, 1.0), P("trophy", 1300, 760, 1.0, at=0.35), T("Nov.", 960, 360, 130, "navy", at=0.5))
sc("If he wins it, he'd be the first Cy Young winner to also clinch a title in the same year since nineteen eighty-eight.",
   C(2026, 1988, 960, 420, fmt="{:.0f}", size=240, color="red", dur=1.5), G(1550, "fist", "grin", look=-1, **MIL, at=0.5))
sc("And Dave? Dave has booked the day off. He has also booked the next day off, which his boss described as optimistic.",
   G(600, "fist", "grin", extras=DAVE), P("calendar", 1150, 860, 0.9, text="OFF x2", at=0.3), G(1550, "hips", "tired", look=-1, extras=["tie"], label="boss", at=0.5), bg="yellow")

# RECAP ---------------------------------------------------------------------------
sc("Recap. The smallest market in baseball beat Tampa Bay four games to one for its first World Series title.",
   P("trophy", 960, 760, 1.4, anim="bob"), T("4 - 1", 960, 330, 150, "navy", at=0.3), chapter="Recap")
sc("It did it with a middle-of-the-pack payroll, a lot of trades, and players it grew itself.",
   P("clipboard", 500, 860, 1.0, text="TRADES"), P("dollar", 960, 650, 0.9, at=0.25), G(1450, "stand", "happy", look=-1, **MIL, at=0.45))
sc("And now owners and players will argue about what it proves, with a December first deadline.",
   P("calendar", 960, 860, 1.2, text="DEC 1"), G(500, "point", "angry", **OWN, at=0.3), G(1450, "point", "angry", look=-1, extras=["cap"], shirt="red", at=0.4))
sc("Meanwhile, thirty-one thousand people in Milwaukee have proven that you don't need the team in the building to throw a party in it.",
   *STADIUM(label="MILWAUKEE"), P("tv", 960, 430, 0.9), *CROWD(560, 1360, at=0.3), bg="sky")
sc("Your turn. Does this World Series prove baseball doesn't need a salary cap, or is it the exception? Tell us in the comments.",
   T("CAP or NO CAP?", 960, 380, 130, "red"), G(960, "think", "neutral", extras=LINDA, at=0.4))
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), T("THE DOODLE DESK", 960, 330, 100, "navy", at=0.3))

script = {
    "id": "ep019",
    "title": "MLB's Smallest Market Just Won It All. How?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Milwaukee is the smallest TV market in Major League Baseball, and on Oct 28, 2026 the Brewers beat the Tampa Bay Rays 4-1 in Game 5 "
        "to win the first World Series in franchise history. We go through the five games (including a record eight two-out runs in one inning), "
        "the payrolls (Brewers about $146M, Rays about $95M, Dodgers about $412M by SB Nation's figures), how both teams build rosters through trades "
        "and homegrown players, the Rays' year after Hurricane Milton, and why both sides of baseball's Dec 1 labor fight now point to this series. "
        "Real players appear only as generic labelled stick figures; quotes are as reported.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "MLB.com, Brewers beat Rays in Game 5 to win first World Series in franchise history (Oct 28, 2026): https://www.mlb.com/news/brewers-beat-rays-game-5-win-2026-world-series\n"
        "AP via Yahoo Sports, Milwaukee Brewers beat Tampa Bay Rays for first World Series title (Oct 29, 2026): https://sports.yahoo.com/articles/milwaukee-brewers-beat-tampa-bay-040709329.html\n"
        "AP via WUNC, Brewers rout the Rays 10-1 (Oct 27, 2026): https://www.wunc.org/2026-10-27/brewers-rout-the-rays-10-1-to-move-within-a-win-of-their-first-world-series-title\n"
        "CBS Sports, Game 5 live updates: https://www.cbssports.com/mlb/news/world-series-game-5-score-live-updates-brewers-rays/live/\n"
        "CBS Sports, How the Rays and Brewers were made: https://www.cbssports.com/mlb/news/2026-world-series-rays-brewers-rosters-payroll/\n"
        "SB Nation via Yahoo Sports, World Series matchup doesn't change need for salary cap/floor system (Oct 28, 2026): https://sports.yahoo.com/articles/world-series-matchup-doesn-t-184836793.html\n"
        "FanSided via Yahoo Sports, A small-market World Series gives these 6 MLB teams reason to believe (Oct 22, 2026): https://sports.yahoo.com/articles/small-market-world-series-gives-182625938.html\n"
        "TSN (AP), Rays proved their brand of baseball can overcome a low payroll: https://www.tsn.ca/mlb/article/rays-proved-their-brand-of-baseball-can-overcome-a-low-payroll/\n\n"
        "#worldseries #brewers #rays #mlb #baseball #explained #stickfigure"
    ),
    "tags": ["world series 2026", "brewers", "milwaukee brewers", "brewers world series", "tampa bay rays", "small market", "mlb payroll",
             "salary cap", "mlb labor talks", "baseball explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "44 YEARS|LATER", "size": 190, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["cap"], "shirt": "navy"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "trophy", "x": 380, "y": 980, "s": 1.6}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep019.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

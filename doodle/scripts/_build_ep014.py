"""Episode 14: the Fed meets Oct 28, 2026 with inflation at 3.7% — will it raise rates again? Explained with stick figures."""
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
CHAIR = dict(extras=["tie", "glasses"], shirt="navy")       # generic Fed chair stick figure
HAWK = dict(extras=["tie"], shirt="red")                    # generic Fed official: worried about prices
DOVE = dict(extras=["tie"], shirt="blue")                   # generic Fed official: worried about jobs
BANKER = dict(extras=["tie"], shirt="teal")
PROF = dict(extras=["glasses"], shirt="brown")              # generic survey researcher

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN --------------------------------------------------------------------
sc("Dave has found his dream house. Small. Blue door. A tree that only drops leaves on the neighbour's side.",
   P("house", 1150, 900, 1.4, text="DREAM"), G(550, "present", "grin", extras=DAVE, at=0.3), P("sun", 1700, 330, 0.7, at=0.6),
   cam={"from": [1100, 620, 1.3], "to": [960, 540, 1.0]})
sc("Dave goes to the bank. Linda, the loan officer, types his numbers into the computer.",
   G(500, "stand", "happy", extras=DAVE), P("desk", 1100, 900, 1.0, at=0.25), G(1450, "type", "neutral", look=-1, extras=LINDA, label="Linda", at=0.4))
sc("A year ago, she says, your mortgage rate would have been about six point two percent.",
   C(0, 6.19, 960, 380, fmt="{:.2f}%", size=230, color="green"), T("A YEAR AGO", 960, 580, 80, "dark", at=0.5))
sc("Today it's seven point three two. Dave asks if that's a lot. Linda turns the screen around.",
   C(6.19, 7.32, 960, 380, fmt="{:.2f}%", size=240, color="red"), G(400, "think", "worried", extras=DAVE, at=0.4),
   G(1550, "present", "neutral", look=-1, extras=LINDA, at=0.6))
sc("Dave reads the monthly payment. Dave sits down on the floor, which is not a chair, but is very stable.",
   G(960, "cry", "shock", extras=DAVE, y=960, anim="shake"), P("laptop", 1450, 900, 0.9, text="$$$$", at=0.3), bg="yellow")
sc("Then Linda adds: and on Wednesday, the Federal Reserve might decide whether to make borrowing even more expensive.",
   G(700, "point", "smug", extras=LINDA), P("calendar", 1300, 860, 1.0, text="WED OCT 28", at=0.35), G(1700, "facepalm", "tired", look=-1, extras=DAVE, s=0.8, at=0.6))
S.append({"say": "Today: why is America's central bank thinking about raising interest rates while people already feel broke? And what does it mean for your wallet?",
          "items": [P("building", 980, 900, 1.0, text="THE FED"), G(330, "think", "confused", extras=DAVE, at=0.4), P("wallet", 1650, 860, 1.0, at=0.6)],
          "chapter": "Today's question"})

# PART 1: WHAT IS THE FED ---------------------------------------------------------
sc("First, the Fed. The Federal Reserve is America's central bank. It doesn't give you a loan. It sets the price of borrowing for everyone else.",
   P("building", 700, 900, 1.0, text="THE FED"), P("pricetag", 1350, 760, 1.2, text="BORROWING", at=0.4), chapter="Part 1: The thermostat")
sc("Think of it as a thermostat for the economy. When things run too hot, prices climb fast. When things run too cold, people lose jobs.",
   P("thermo", 960, 900, 1.6), T("TOO HOT", 1350, 380, 90, "red", at=0.3), T("TOO COLD", 1350, 720, 90, "blue", at=0.6))
sc("Its main dial is a short-term interest rate, the federal funds rate. Right now it sits between three point seven five and four percent.",
   T("3.75% - 4%", 960, 380, 190, "navy"), T("federal funds rate", 960, 560, 70, "dark", at=0.4), G(1650, "point", "neutral", look=-1, **CHAIR, at=0.6))
sc("Turn the dial up, and loans for houses, cars and businesses get pricier. People borrow less, spend less, and prices, in theory, calm down.",
   {"arrow": [[300, 700], [300, 350]], "color": "red"}, P("house", 650, 900, 0.6, at=0.2), P("car", 1050, 900, 0.7, at=0.35),
   P("building", 1450, 900, 0.6, text="BIZ", at=0.5), T("calm down?", 1450, 330, 80, "dark", at=0.7))
sc("Turn it down, and borrowing gets cheaper. More spending, more hiring, but also a risk of prices running hot again.",
   {"arrow": [[300, 350], [300, 700]], "color": "blue"}, P("cart", 750, 900, 1.0, at=0.2), G(1250, "fist", "happy", extras=DAVE, at=0.4), P("fire", 1650, 900, 0.6, at=0.65))
sc("The Fed's target is simple: inflation of two percent a year. Not zero. Two.",
   C(0, 2, 960, 420, fmt="{:.0f}%", size=280, color="green"), T("THE TARGET", 960, 640, 90, "dark", at=0.5))
sc("The Fed is also run by a committee, not one person. Twelve voting officials. They meet eight times a year and argue politely in suits.",
   G(500, "present", "neutral", **HAWK), G(800, "think", "neutral", **CHAIR, at=0.15), G(1100, "shrug", "neutral", **DOVE, at=0.3),
   G(1400, "point", "neutral", **HAWK, at=0.45), T("12 VOTES", 960, 260, 90, "navy", at=0.6))
sc("The chair, since May, is Kevin Warsh. Here he's a generic stick figure in a tie, because we don't draw real people.",
   G(960, "stand", "neutral", **CHAIR, s=1.2, label="the Fed Chair"), T("since May 2026", 960, 300, 70, "dark", at=0.5))

# PART 2: THE NUMBER -----------------------------------------------------------------
sc("So why is the dial even being discussed? Because of this number.",
   T("?", 960, 450, 300, "red", anim="pulse"), chapter="Part 2: The number")
sc("In September, consumer prices were three point seven percent higher than a year earlier. That's up from three point four in August.",
   {"bars": {"values": [3.4, 3.7], "labels": ["Aug", "Sep"], "colors": ["grey", "red"], "fmt": "{}%", "w": 700, "h": 420}, "x": 900, "y": 820},
   P("thermo", 1600, 900, 1.2, at=0.5))
sc("In just one month, prices rose point six percent. Do that every month for a year and you're above seven.",
   C(0, 0.6, 700, 400, fmt="+{:.1f}%", size=200, color="red"), T("in ONE month", 700, 580, 70, "dark", at=0.4), T("x12 = 7%+", 1400, 420, 120, "red", at=0.6))
sc("The target is two. Inflation has now been above two percent for five years, according to a Forbes analysis.",
   C(0, 2, 600, 400, fmt="{:.0f}%", size=200, color="green"), C(0, 3.7, 1300, 400, fmt="{:.1f}%", size=200, color="red", at=0.3),
   T("5 YEARS ABOVE", 960, 650, 90, "dark", at=0.6))
sc("The biggest driver is energy. Since the Iran war began in late February, the average gallon of gas is up about forty-three percent, according to AAA via ABC News.",
   P("gaspump", 650, 900, 1.2, text="$4.29"), C(0, 43, 1350, 400, fmt="+{:.0f}%", size=220, color="red", at=0.35), T("since Feb", 1350, 580, 70, "dark", at=0.6))
sc("Today's average is four dollars twenty-nine. And on Friday, ABC reported, oil crossed one hundred sixteen dollars a barrel, a six-month high.",
   P("gaspump", 500, 900, 0.9, text="$4.29"), P("barrel", 1050, 900, 1.1, at=0.3), C(90, 116, 1550, 400, fmt="${:.0f}", size=200, color="red", at=0.45))
sc("Dave's car now has a fuel gauge with only two settings: empty, and recently empty.",
   P("car", 900, 900, 1.3), G(1500, "facepalm", "tired", look=-1, extras=DAVE, at=0.4), T("E / E", 900, 420, 120, "red", at=0.6))

# PART 3: WHAT THE FED ALREADY DID -------------------------------------------------
sc("Here's the twist. A year ago, the Fed was cutting. At the end of twenty twenty-five, it lowered rates by three quarters of a percentage point.",
   {"arrow": [[600, 350], [600, 700]], "color": "blue"}, T("-0.75", 1150, 450, 200, "blue", at=0.3), T("end of 2025", 1150, 640, 70, "dark", at=0.5),
   chapter="Part 3: The U-turn")
sc("Then prices heated up. In July, three Fed officials dissented. They wanted a hike. The majority said: not yet.",
   G(500, "fist", "angry", **HAWK), G(750, "fist", "angry", **HAWK, at=0.15), G(1000, "fist", "angry", **HAWK, at=0.3),
   G(1500, "shrug", "neutral", look=-1, **CHAIR, at=0.5), T("NOT YET", 1500, 330, 90, "dark", at=0.65))
sc("On September sixteenth, the Fed raised rates by a quarter point. Its first hike in more than three years.",
   P("calendar", 600, 860, 1.0, text="SEP 16"), T("+0.25", 1250, 420, 220, "red", at=0.3), {"stamp": "FIRST IN 3 YEARS", "x": 1250, "y": 680, "size": 60, "w": 560, "at": 0.6})
sc("At that meeting, most officials pencilled in one more hike this year. A handful pencilled in two.",
   P("clipboard", 700, 860, 1.1, text="+1 MORE"), P("clipboard", 1250, 860, 0.8, text="+2", at=0.4), G(1650, "think", "neutral", look=-1, **CHAIR, at=0.55))
sc("Forbes points out that those pencil marks are already out of date, because the inflation numbers since then came in hotter.",
   P("clipboard", 800, 860, 1.1, text="SEPT PLAN"), P("fire", 1300, 900, 0.8, at=0.35), {"cross": [800, 650, 160], "at": 0.6})
sc("It's like planning a picnic on Tuesday, then seeing Wednesday's forecast is a hailstorm. The plan is still on the fridge. It's just wrong.",
   P("calendar", 600, 860, 0.9, text="PICNIC"), P("cloud", 1250, 400, 1.2, anim="shake", at=0.3), G(1600, "shrug", "worried", look=-1, extras=LINDA, at=0.55))

# PART 4: WHAT HAPPENS WEDNESDAY ----------------------------------------------------
sc("So, Wednesday, October twenty-eighth. Will the Fed raise rates again?",
   P("calendar", 960, 860, 1.3, text="OCT 28"), T("HIKE?", 960, 300, 140, "red", at=0.4), chapter="Part 4: Wednesday")
sc("Probably not, according to markets. On Friday, futures traders priced only about an eight percent chance of an October hike, according to Charles Schwab.",
   C(0, 8, 960, 400, fmt="{:.0f}%", size=260, color="grey"), T("chance of a hike Wednesday", 960, 600, 70, "dark", at=0.4))
sc("But ask about the whole rest of the year, and the odds of a hike jump to about eighty-four percent.",
   C(8, 84, 960, 400, fmt="{:.0f}%", size=280, color="red"), T("hike before year-end", 960, 620, 70, "dark", at=0.4), P("arrowup", 1600, 800, 1.0, at=0.6))
sc("The date most people are circling is December ninth. That's the next meeting, when officials also update their forecasts.",
   P("calendar", 700, 860, 1.2, text="DEC 9"), {"ring": [700, 680, 200], "at": 0.3, "color": "red"}, P("chart", 1350, 880, 1.0, at=0.5))
sc("J.P. Morgan Wealth Management strategists expect about half a percentage point of hikes in total before the Fed stops. Timing: unclear.",
   T("+0.50", 800, 420, 200, "red"), T("total, eventually", 800, 600, 70, "dark", at=0.4), P("stopwatch", 1500, 860, 1.0, at=0.55))
sc("And bond markets are already pricing more hikes into early twenty twenty-seven, with short-term rates possibly reaching around five percent.",
   C(4, 5, 960, 420, fmt="~{:.1f}%", size=240, color="red"), T("2027?", 960, 620, 100, "dark", at=0.5))
sc("New York Fed President John Williams has said officials may have, quote, no need for urgency. Which is Fed for: we're watching, we're not panicking.",
   G(600, "stand", "neutral", **DOVE, label="NY Fed President"), P("speech", 1300, 480, 1.5, text="\"no need for urgency\"", at=0.35))
sc("One thing makes this harder to guess. Chair Warsh has moved away from forward guidance, meaning the Fed hints less about what's coming next.",
   G(700, "shrug", "neutral", **CHAIR, label="the Fed Chair"), P("lock", 1300, 800, 1.0, at=0.35), T("FEWER HINTS", 1300, 380, 100, "dark", at=0.55))
sc("Markets used to get a trailer before the movie. Now they get a poster with the title blacked out.",
   P("tv", 700, 800, 1.0, text="TRAILER"), {"cross": [700, 640, 150], "at": 0.3}, P("sign", 1350, 900, 1.0, text="????", at=0.5))

# PART 5: BOTH SIDES -----------------------------------------------------------------
sc("Now, the argument inside the Fed. Depending on who you ask, there are two very different worries.",
   G(500, "point", "angry", **HAWK, label="worry #1"), G(1450, "point", "worried", look=-1, **DOVE, label="worry #2", at=0.3), P("scale", 960, 900, 1.0, at=0.5),
   chapter="Part 5: Both sides")
sc("Worry number one: prices. Inflation at three point seven percent is well over target, and it's been over target for years.",
   G(600, "fist", "angry", **HAWK), C(0, 3.7, 1250, 400, fmt="{:.1f}%", size=220, color="red", at=0.3), P("thermo", 1700, 900, 1.0, at=0.5))
sc("If people start expecting high prices to last, they ask for bigger raises, shops raise prices to match, and the fever feeds itself.",
   G(500, "hold", "worried", extras=DAVE), {"arrow": [[700, 600], [1000, 600]], "at": 0.25}, P("building", 1200, 900, 0.6, text="SHOP", at=0.35),
   {"arrow": [[1400, 600], [1650, 600]], "at": 0.5}, P("pricetag", 1750, 760, 0.8, text="$$$", at=0.6))
sc("And people are starting to expect that. Americans now expect about three point five percent inflation over the next five years, up from three point two in March.",
   C(3.2, 3.5, 960, 400, fmt="{:.1f}%", size=240, color="red"), T("expected, 5 years out", 960, 600, 70, "dark", at=0.4))
sc("That's from the University of Michigan survey. Its director, Joanne Hsu, wrote that, quote, consumers broadly expect inflation to accelerate.",
   G(600, "present", "neutral", **PROF, label="survey director"), P("speech", 1300, 480, 1.5, text="\"expect inflation|to accelerate\"", at=0.35))
sc("Worry number two: jobs. In September, employers added only twenty-nine thousand jobs. In August it was one hundred sixty-two thousand.",
   {"bars": {"values": [162, 29], "labels": ["Aug", "Sep"], "colors": ["grey", "blue"], "fmt": "{}k", "w": 700, "h": 420}, "x": 850, "y": 820},
   G(1600, "think", "worried", look=-1, **DOVE, at=0.5))
sc("Raise rates into a cooling job market, this side says, and you risk turning a slowdown into layoffs.",
   G(600, "point", "worried", **DOVE), P("building", 1200, 900, 0.8, text="JOBS", at=0.3), P("arrowdown", 1650, 800, 1.0, at=0.55))
sc("They also note this inflation is mostly energy. Core inflation, which leaves out food and fuel, was two point six percent. Much closer to target.",
   C(0, 2.6, 960, 400, fmt="{:.1f}%", size=240, color="orange"), T("core: no food, no fuel", 960, 600, 70, "dark", at=0.4))
sc("And here's the awkward part: a higher interest rate can't open a shipping lane or make an oil tanker sail faster.",
   P("tanker", 800, 900, 1.2), P("strait", 1450, 900, 0.9, at=0.3), {"cross": [1100, 500, 120], "at": 0.6})
sc("The other side answers: true, but energy costs leak into everything. Forbes notes higher energy prices may already be spreading to other goods and services.",
   P("barrel", 500, 900, 0.9), {"arrow": [[700, 700], [950, 700]], "at": 0.25}, P("bread", 1100, 880, 0.9, at=0.35), P("cart", 1450, 900, 0.8, at=0.5),
   P("coffee", 1750, 880, 0.8, at=0.65))
sc("Both sides have a point. That's why the room argues. We just count the facts.",
   P("scale", 960, 900, 1.3, anim="bob"), G(450, "shrug", "neutral", **HAWK, at=0.3), G(1500, "shrug", "neutral", look=-1, **DOVE, at=0.45))

# PART 6: YOUR WALLET ------------------------------------------------------------------
sc("So what does this mean for you? Start with houses.",
   P("house", 960, 900, 1.4), P("wallet", 1550, 860, 0.9, at=0.4), chapter="Part 6: Your wallet")
sc("Freddie Mac says the average thirty-year mortgage fell to seven point three two percent this week, from seven point four zero. Its first dip since August.",
   C(7.40, 7.32, 960, 400, fmt="{:.2f}%", size=240, color="orange"), P("arrowdown", 1600, 760, 0.9, at=0.5))
sc("Freddie Mac's chief economist called it, quote, some relief to prospective homebuyers. Some. Like a single ice cube in July.",
   P("speech", 750, 480, 1.4, text="\"some relief\""), P("sun", 1450, 380, 0.9, at=0.4), P("coffee", 1450, 860, 0.6, text="ICE", at=0.6))
sc("A year ago, that rate was six point one nine. On a big loan, that difference adds hundreds of dollars a month.",
   {"bars": {"values": [6.19, 7.32], "labels": ["a year ago", "now"], "colors": ["green", "red"], "fmt": "{}%", "w": 700, "h": 420}, "x": 900, "y": 820},
   G(1600, "facepalm", "tired", look=-1, extras=DAVE, at=0.5))
sc("Mortgages follow long-term bond yields more than the Fed's dial directly. The ten-year Treasury yield was near five percent on Friday, at four point nine six.",
   P("chart", 700, 880, 1.1), C(4.5, 4.96, 1350, 400, fmt="{:.2f}%", size=200, color="red", at=0.3), T("10-year yield", 1350, 580, 70, "dark", at=0.55))
sc("Credit cards are different. Their rates move almost directly with the Fed. Another hike, and carrying a balance gets more expensive, quickly.",
   P("wallet", 650, 860, 1.2), {"arrow": [[900, 650], [1150, 450]], "color": "red", "at": 0.3}, T("CARDS", 1450, 400, 120, "red", at=0.5))
sc("Car loans and small business loans sit somewhere in between. They feel it, just with a delay.",
   P("car", 700, 900, 1.0), P("building", 1300, 900, 0.7, text="SMALL BIZ", at=0.3), P("stopwatch", 1700, 860, 0.7, at=0.55))
sc("There is one winner. Savers. Higher rates usually mean better interest on savings accounts.",
   G(960, "fist", "grin", extras=LINDA, label="a saver"), P("moneybag", 1450, 880, 0.9, anim="bob", at=0.35))
sc("Linda has a savings account. Linda is quietly delighted. Linda will not be telling Dave this.",
   G(700, "hips", "smug", extras=LINDA), G(1400, "cry", "sad", look=-1, extras=DAVE, at=0.4), T("shh.", 700, 380, 90, "dark", at=0.6))

# PART 7: HOW PEOPLE FEEL --------------------------------------------------------------
sc("Meanwhile, Americans already feel squeezed. The University of Michigan's sentiment index came in at forty-eight in October.",
   C(0, 48, 960, 400, fmt="{:.0f}", size=280, color="red"), T("consumer sentiment", 960, 600, 70, "dark", at=0.4), chapter="Part 7: The mood")
sc("That's the second-lowest final reading in the survey's seventy-four year history. The record low, forty-four point eight, was set this May.",
   {"bars": {"values": [44.8, 48.0], "labels": ["May (record)", "October"], "colors": ["dark", "red"], "fmt": "{}", "w": 700, "h": 420}, "x": 900, "y": 820},
   T("74 YEARS", 1600, 380, 90, "dark", at=0.5))
sc("Sentiment is now ten percent below a year ago, and fifteen percent below February, just before the Iran conflict, Hsu said.",
   C(0, -10, 650, 420, fmt="{:.0f}%", size=200, color="red"), C(0, -15, 1300, 420, fmt="{:.0f}%", size=200, color="red", at=0.35),
   T("vs a year ago", 650, 590, 60, "dark", at=0.2), T("vs February", 1300, 590, 60, "dark", at=0.5))
sc("Her summary, quote: purchasing power continues to dominate consumer views of the economy. Translation: stuff costs too much.",
   P("speech", 750, 480, 1.5, text="\"purchasing power\""), P("cart", 1450, 900, 1.0, at=0.4), T("= stuff costs too much", 960, 830, 60, "dark", at=0.65))
sc("Prices worry people across the spectrum. Since January, the share of Republicans citing inflation pressures rose fifty-two percent, independents twenty-seven, Democrats fifteen.",
   {"bars": {"values": [52, 27, 15], "labels": ["Rep", "Ind", "Dem"], "colors": ["red", "purple", "blue"], "fmt": "+{}%", "w": 800, "h": 420}, "x": 960, "y": 820})
sc("And there's an election. The midterms are on November third, and ABC reports affordability is a top concern for voters.",
   P("ballot", 700, 880, 1.1), P("calendar", 1300, 860, 1.0, text="NOV 3", at=0.3), P("pricetag", 1700, 760, 0.8, text="$$", at=0.55))
sc("The Fed is meant to be independent of elections. Whatever it does next week, expect both sides to have a strong opinion about it.",
   P("building", 960, 900, 0.9, text="THE FED"), G(450, "point", "angry", **HAWK, at=0.3), G(1500, "point", "angry", look=-1, **DOVE, at=0.45))

# PART 8: WHAT'S NEXT ---------------------------------------------------------------------
sc("What to watch. Wednesday: the decision itself, and whether any officials dissent in favour of a hike. That would hint at December.",
   P("calendar", 600, 860, 1.0, text="WED"), G(1250, "fist", "angry", **HAWK, at=0.3), T("dissent?", 1250, 330, 90, "red", at=0.5), chapter="Part 8: What's next")
sc("Thursday: the economy's growth number for the summer, plus the Fed's favourite inflation gauge, called P C E.",
   P("calendar", 600, 860, 1.0, text="THU"), P("chart", 1150, 880, 0.9, at=0.3), T("GDP + PCE", 1500, 400, 110, "navy", at=0.5))
sc("Then oil. If tankers move freely again and energy falls, the pressure for hikes eases. If oil keeps climbing, it doesn't.",
   P("tanker", 650, 900, 1.0, move=[900, 900]), P("barrel", 1350, 900, 1.0, at=0.35), P("arrowup", 1700, 760, 0.8, at=0.55))
sc("And December ninth: the meeting the markets think matters most.",
   P("calendar", 960, 860, 1.4, text="DEC 9"), {"ring": [960, 660, 230], "at": 0.4, "color": "red"})

# RECAP -----------------------------------------------------------------------------------
sc("Quick recap. Prices are rising at three point seven percent, mostly because of energy. The Fed already hiked once in September.",
   C(0, 3.7, 650, 420, fmt="{:.1f}%", size=200, color="red"), T("+0.25 in Sept", 1350, 420, 100, "red", at=0.35), chapter="Recap")
sc("Markets expect a pause on Wednesday and another hike by December. Officials are split between fighting prices and protecting jobs.",
   P("calendar", 550, 860, 0.8, text="OCT 28"), P("calendar", 950, 860, 0.8, text="DEC 9", at=0.25), P("scale", 1450, 900, 1.0, at=0.45))
sc("For you: mortgages near seven and a third percent, pricier credit cards, and slightly happier savers.",
   P("house", 550, 900, 0.7), P("wallet", 1000, 860, 0.8, at=0.25), P("moneybag", 1450, 880, 0.8, at=0.45))
sc("Back at the bank, Dave has a new plan. He'll wait for rates to fall, then buy the dream house.",
   G(700, "think", "happy", extras=DAVE), P("house", 1350, 900, 1.0, text="DREAM", at=0.4))
sc("Linda points out the house has already sold. To a cash buyer. Who is, it turns out, a saver.",
   P("house", 1100, 900, 1.0, text="SOLD"), G(600, "point", "smug", extras=LINDA, at=0.3), G(1650, "cry", "cry", look=-1, extras=DAVE, s=0.8, at=0.55), bg="yellow")
sc("Your turn. If you were on the Fed's committee on Wednesday, would you raise rates, hold, or cut? Tell us in the comments. Show your thermostat.",
   P("thermo", 980, 900, 1.3), G(330, "point", "grin", extras=DAVE, at=0.4), T("?", 1650, 400, 200, "red", at=0.6))
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, text="SUBSCRIBE", at=0.4), bg="yellow")

script = {
    "id": "ep014",
    "title": "Why Is the Fed About to Raise Rates Again?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "The Federal Reserve meets on Wednesday, October 28, 2026, with US inflation at 3.7% (September CPI) and the fed funds rate at 3.75%-4% "
        "after September's first hike in more than three years. Markets price only about an 8% chance of a hike this week but about 84% before year-end, "
        "with December 9 the date to watch. We explain how the Fed's 'thermostat' works, why energy prices after the Iran war pushed inflation up, "
        "the argument inside the Fed (prices vs. jobs: September added just 29,000 jobs), what it means for mortgages (7.32% this week), credit cards and savers, "
        "and why consumer sentiment (48.0) is near its lowest in 74 years.\n\n"
        "Dave and Linda are made-up characters. Real officials are shown as generic labelled stick figures; quotes are attributed as reported. "
        "Not financial advice. We don't take sides: we just count the facts.\n\n"
        "Sources:\n"
        "Forbes, What To Look For From The Fed's October Meeting (Oct 19, 2026): https://www.forbes.com/sites/simonmoore/2026/10/19/what-to-look-for-from-the-feds-october-meeting/\n"
        "J.P. Morgan / Chase, Will the Fed hike rates in October?: https://www.chase.com/personal/investments/learning-and-insights/article/will-the-federal-reserve-hike-rates-at-october-2026-fomc-meeting\n"
        "Charles Schwab, market update (Oct 23, 2026): https://www.schwab.com/learn/story/stock-market-update-open\n"
        "ABC News, Consumer sentiment nears all-time low ahead of midterms: https://abcnews.com/Business/consumer-sentiment-nears-time-low-ahead-midterms/story?id=137507935\n"
        "Al Jazeera, US consumer sentiment hits a near-record low (Oct 23, 2026): https://www.aljazeera.com/economy/2026/10/23/us-consumer-sentiment-hits-a-near-record-low-before-midterm-elections\n"
        "Freddie Mac, Mortgage Rates Decrease to 7.32% (Oct 22, 2026): https://www.globenewswire.com/news-release/2026/10/22/3386709/0/en/mortgage-rates-decrease-to-7-32.html\n\n"
        "#federalreserve #interestrates #inflation #mortgage #explained #stickfigure #news"
    ),
    "tags": ["federal reserve", "fed rate hike", "interest rates", "fomc october 2026", "inflation", "mortgage rates", "consumer sentiment",
             "kevin warsh", "economy explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "RATES|GOING|UP?", "size": 200, "color": "black",
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep014.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

"""Episode 23: DraftKings Q3 2026 (results Nov 5, stock -21.3% on Nov 6, 2026) after raising its prediction-markets spend to $650-700M;
the Kalshi/Polymarket challenge and the states-vs-CFTC court split heading to the Supreme Court."""
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


def ST(text, x, y, size=80, w=320, at=0, **kw):
    d = {"stamp": text, "x": x, "y": y, "size": size, "w": w, "at": at}
    d.update(kw)
    return d


def AR(a, b, color="red", at=0):
    return {"arrow": [list(a), list(b)], "color": color, "at": at}


def BARS(values, labels, colors, fmt, x=900, y=840, w=700, h=420, at=0):
    return {"bars": {"values": values, "labels": labels, "colors": colors, "fmt": fmt, "w": w, "h": h}, "x": x, "y": y, "at": at}


DAVE = ["hair"]
ECON = ["glasses", "tie"]
LINDA = ["bun"]
OFF = ["tie", "briefcase"]
GIANT = dict(shirt="green", extras=["tie"])      # generic "the sportsbook giant"
UPSTART = dict(shirt="purple", extras=["cap"])   # generic "the prediction market"
JUDGE = dict(shirt="dark", extras=["glasses"])

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN ------------------------------------------------------------------
sc("Dave wants ten dollars on Sunday's game. His phone shows two buttons. One says bet. The other says buy a contract.",
   G(500, "hold", "confused", extras=DAVE), P("phone", 1150, 700, 1.3, at=0.2), T("BET", 780, 300, 90, "green", at=0.45), T("CONTRACT", 1600, 300, 90, "purple", at=0.65), bg="yellow")
sc("Same game, same ten dollars. One button is gambling. The other, depending on who you ask, is a financial product.",
   P("football", 960, 820, 1.2), T("GAMBLING", 520, 360, 90, "green", at=0.3), T("FINANCE?", 1400, 360, 90, "purple", at=0.55), AR((700, 440), (1200, 440), "grey", at=0.45))
sc("That second button has a giant scared. And on Friday, November sixth, the giant's stock fell twenty-one percent in one day.",
   G(700, "panic", "shock", look=1, s=1.3, **GIANT, label="the giant"), C(0, -21.3, 1400, 400, "{:.1f}%", 180, at=0.4), P("arrowdown", 1400, 820, 1.2, color="red", at=0.6), bg="yellow")
sc("The giant is DraftKings. The thing scaring it is called a prediction market. And this fight is heading for the Supreme Court.",
   T("DRAFTKINGS", 600, 330, 90, "green"), T("vs", 960, 330, 70, "grey", at=0.3), T("PREDICTION|MARKETS", 1350, 330, 80, "purple", at=0.45), P("scale", 960, 880, 1.1, at=0.6))
sc("Today's question: why would the company that won the betting war spend up to seven hundred million dollars on this, and is it working?",
   T("TODAY'S QUESTION", 960, 250, 90, "dark"), P("moneybag", 700, 880, 1.5, text="$700M", at=0.3), T("WORTH IT?", 1350, 600, 120, "red", at=0.6), bg="sky")
sc("Thursday, November fifth. After the stock market closed, DraftKings published its results for July to September.",
   P("calendar", 500, 860, 1.0, text="NOV 5"), P("building", 1300, 900, 1.0, text="DRAFTKINGS", at=0.3), P("envelope", 1300, 420, 0.8, at=0.6), chapter="Part 1: The Worst Friday")
sc("On paper, the business grew. Revenue was one point three three billion dollars, up sixteen percent from a year earlier.",
   C(0, 1.33, 960, 360, "${:.2f}B", 170, "green"), P("arrowup", 960, 820, 1.1, color="green", at=0.5), T("+16%", 1350, 600, 100, "green", at=0.6))
sc("Analysts surveyed by Bloomberg expected one point three nine billion. In stock-market land, growing less than expected counts as shrinking.",
   BARS([1.33, 1.39], ["actual", "expected"], ["green", "grey"], "${}B", 800, 860, 620, 400), G(1500, "shrug", "confused", extras=DAVE, at=0.5))
sc("Then came the loss. On the profit measure DraftKings uses most, it lost three hundred seventeen million dollars in the quarter.",
   C(0, 317, 960, 380, "-${:,.0f}M", 170), G(500, "facepalm", "sad", **GIANT, at=0.5), P("fire", 1450, 880, 0.9, at=0.6))
sc("A year earlier, that same quarter lost one hundred twenty-six million. So the hole got about two and a half times deeper.",
   BARS([126, 317], ["2025", "2026"], ["grey", "red"], "-${}M", 900, 860, 640, 420))
sc("Look at one line. Sales and marketing jumped from three hundred sixty million to six hundred six million dollars.",
   P("megaphone", 600, 820, 1.2), C(360, 606, 1300, 420, "${:,.0f}M", 160, "red", dur=2.2), T("ADS. PROMOS.", 1300, 700, 70, "dark", at=0.6))
sc("And the company's letter points to one new product as the reason. DraftKings calls it Predictions.",
   P("phone", 960, 760, 1.4, text="PREDICTIONS"), ST("NEW", 1450, 380, 80, 240, at=0.4))
sc("And the forecast for the whole year? DraftKings had promised seven hundred to nine hundred million dollars of that profit measure.",
   T("BEFORE", 600, 330, 80, "grey"), T("$700M - $900M", 600, 500, 90, "green", at=0.2), P("calendar", 1400, 860, 0.9, text="2026", at=0.4))
sc("The new forecast: one hundred seventy-five to two hundred seventy-five million. Nearly three quarters of the expected profit, gone with one press release.",
   T("NOW", 1300, 330, 80, "red"), T("$175M - $275M", 1300, 500, 90, "red", at=0.2), {"cross": [600, 500, 260], "at": 0.5}, T("$700M - $900M", 600, 500, 90, "grey"))
sc("The reason: planned spending on Predictions this year rose to six hundred fifty to seven hundred million dollars.",
   P("clipboard", 600, 860, 1.0, text="LETTER"), P("moneybag", 1300, 880, 1.2, text="$650-700M", at=0.4))
sc("The earlier plan, per one market newsletter, was two to three hundred million. The bill more than doubled.",
   BARS([250, 675], ["old plan", "new plan"], ["grey", "red"], "${}M", 900, 860, 640, 420), T("x2+", 1500, 400, 120, "red", at=0.6))
sc("Friday morning, investors answered. The stock touched sixteen dollars fifty-five, its lowest in more than three years.",
   G(500, "panic", "scream", extras=["sweat"], shirt="blue"), P("arrowdown", 1250, 860, 1.3, color="red", at=0.2), C(23.5, 16.55, 1250, 330, "${:.2f}", 150, at=0.3))
sc("It closed at eighteen dollars fifty-one, down twenty-one point three percent. That leaves it down about half for the year.",
   P("tv", 700, 880, 1.0, text="-21.3%"), T("-50% THIS YEAR", 1350, 450, 90, "red", at=0.5))
sc("Its main rival, Flutter, which owns FanDuel, fell around eight percent in Friday morning trading. When the giant flinches, its twin flinches too.",
   G(650, "panic", "worried", **GIANT, label="DraftKings"), G(1250, "panic", "worried", look=-1, shirt="blue", extras=["tie"], label="FanDuel owner", at=0.4), T("-8%", 1250, 260, 90, "red", at=0.6))

# PART 2 -----------------------------------------------------------------------
sc("So what is a prediction market, and why is it worth seven hundred million dollars to fight one?",
   P("magnifier", 960, 820, 1.3), T("WHAT IS IT?", 960, 350, 120, "purple", at=0.3), chapter="Part 2: The Little Button", bg="purple")
sc("Here's the idea. You buy a contract that pays one dollar if something happens, and zero if it doesn't.",
   P("pricetag", 600, 820, 1.6, text="CONTRACT"), T("YES = $1", 1300, 400, 110, "green", at=0.3), T("NO = $0", 1300, 600, 110, "grey", at=0.55))
sc("Say the contract 'Chiefs win on Sunday' costs sixty cents. That price means the crowd thinks the chance is about sixty percent.",
   C(0, 0.6, 700, 380, "${:.2f}", 170, "purple"), T("= 60% CHANCE", 1300, 380, 90, "dark", at=0.5), P("football", 1300, 800, 0.9, at=0.3))
sc("If they win, Dave gets a dollar and keeps forty cents of profit. If they lose, his sixty cents is gone.",
   G(500, "fist", "grin", extras=DAVE), T("+$0.40", 500, 300, 100, "green", at=0.2), G(1400, "cry", "cry", extras=DAVE, at=0.5), T("-$0.60", 1400, 300, 100, "red", at=0.6))
sc("If that sounds a lot like a bet, you're not alone. Courts are thinking the same thing. We'll get there.",
   G(960, "think", "confused", extras=LINDA), T("...a bet?", 960, 330, 100, "grey", at=0.4))
sc("The difference is who's in charge. Sportsbooks are regulated state by state. Legal in some, not in others.",
   P("globe", 600, 860, 1.0), P("clipboard", 1300, 860, 1.0, text="STATE RULES", at=0.4))
sc("DraftKings' sportsbook is live in thirty states, plus Washington DC and Puerto Rico. That still leaves big gaps, like California and Texas.",
   C(0, 30, 700, 380, "{:.0f} STATES", 150, "green"), T("CALIFORNIA? NO", 1350, 520, 70, "red", at=0.4), T("TEXAS? NO", 1350, 650, 70, "red", at=0.55))
sc("Prediction markets say their contracts are federal financial products, overseen by the CFTC, the agency for things like wheat futures.",
   G(600, "present", "smug", **UPSTART, label="prediction market"), P("building", 1350, 900, 0.9, text="CFTC", at=0.3), P("bread", 1350, 420, 0.7, at=0.6))
sc("And if it's federal, the argument goes, it should work in all fifty states at once, no state licence required.",
   C(0, 50, 960, 380, "{:.0f} STATES", 180, "purple"), P("arrowup", 960, 820, 1.0, color="purple", at=0.5))
sc("One appeals court noted that Kalshi, one of the two biggest, advertised itself as the first app for legal sports betting in all fifty states.",
   P("phone", 600, 760, 1.2), T("\"legal sports betting|in all 50 states\"", 1300, 420, 64, "purple", at=0.3), T("- Kalshi ad, quoted by the 9th Circuit", 1300, 650, 40, "grey", at=0.5))
sc("Yes, a company arguing that it's not betting advertised itself as betting. The judges noticed that too.",
   G(960, "facepalm", "tired", **JUDGE, label="a judge"), T("hmm.", 1450, 380, 90, "grey", at=0.4))

# PART 3 -----------------------------------------------------------------------
sc("Here's the twist in the underdog story. DraftKings itself started in two thousand twelve as a scrappy daily fantasy sports startup.",
   P("calendar", 500, 860, 0.9, text="2012"), G(1200, "fist", "happy", s=0.7, **GIANT, label="tiny DraftKings", at=0.3), chapter="Part 3: The Giant Was Once Small")
sc("After the Supreme Court let states legalise sports betting in twenty eighteen, it grew fast. Along with FanDuel, it came out on top.",
   G(700, "hips", "smug", s=1.3, **GIANT), P("trophy", 1350, 880, 1.1, at=0.3), P("calendar", 1650, 400, 0.6, text="2018", at=0.5))
sc("Then the new upstarts showed up. Kalshi and Polymarket, offering a different button for the same games.",
   G(500, "hips", "smug", s=1.3, **GIANT), G(1200, "wave", "grin", s=0.7, **UPSTART, label="Kalshi"), G(1550, "wave", "grin", s=0.7, **UPSTART, label="Polymarket", at=0.3))
sc("Kalshi isn't small anymore, by the way. One industry outlet puts its valuation at twenty-two billion dollars.",
   G(1100, "hips", "smug", s=1.25, **UPSTART, label="Kalshi"), C(0, 22, 600, 400, "${:.0f}B", 170, "purple", at=0.3))
sc("So the giant built its own version. DraftKings Predictions runs mainly in states with no legal online sportsbook.",
   G(600, "type", "neutral", **GIANT), P("laptop", 900, 860, 0.9), P("phone", 1400, 760, 1.2, text="PREDICTIONS", at=0.4))
sc("The company says more than one point six million customers have tried it this year.",
   C(0, 1.6, 960, 400, "{:.1f}M", 190, "green"), T("customers", 960, 600, 70, "dark", at=0.5))
sc("And DraftKings says the spending pays for itself. It expects this year's new customers to earn back their cost in about twenty months.",
   P("stopwatch", 650, 860, 1.0, text="20 MO"), P("moneybag", 1300, 880, 1.0, at=0.3), AR((850, 640), (1150, 640), "green", at=0.4))
sc("Next year it forecasts about seven hundred million dollars of Predictions revenue. This year, it says, promotions eat almost all of it.",
   BARS([0, 700], ["2026", "2027"], ["grey", "green"], "${}M", 900, 860, 620, 420), T("forecast", 1500, 400, 60, "grey", at=0.5))
sc("The chief executive put it this way: the third quarter marked a pivotal moment, as the Predictions offering is now powering meaningful growth.",
   G(600, "present", "happy", extras=OFF, label="the CEO"), T("\"a pivotal moment\"", 1300, 400, 80, "dark", at=0.3), T("- DraftKings CEO, Nov 5", 1300, 560, 44, "grey", at=0.5))

# PART 4 -----------------------------------------------------------------------
sc("So who's right? The company, or the people who sold its stock on Friday? Let's hear both sides, fairly.",
   P("scale", 960, 880, 1.2), T("BOTH SIDES", 960, 330, 110, "dark", at=0.3), chapter="Part 4: Bull vs Bear", bg="sky")
sc("The worried side first. Analysts expected one point one two billion of profit next year. DraftKings guided eight hundred million to one billion.",
   BARS([1.12, 0.9], ["expected", "guided (mid)"], ["grey", "red"], "${}B", 900, 860, 640, 420))
sc("A Stifel analyst called it a shocking quarter, but kept a buy rating. Jefferies cut its target from forty-four to twenty-eight dollars.",
   T("\"a shocking quarter\"", 960, 300, 80, "red"), T("- Stifel analyst", 960, 420, 44, "grey", at=0.2), C(44, 28, 960, 640, "${:.0f} target", 120, "dark", at=0.5))
sc("The hopeful side: the old business is fine. Sportsbook revenue grew thirty-six percent, and the amount bet grew twelve.",
   C(0, 36, 650, 400, "+{:.0f}%", 160, "green"), C(0, 12, 1300, 400, "+{:.0f}%", 160, "green", at=0.4), T("revenue", 650, 560, 60, "dark"), T("bets", 1300, 560, 60, "dark", at=0.4))
sc("In its own words, prediction market operators are having, quote, no discernible impact on its sportsbook business.",
   T("\"no discernible impact\"", 960, 380, 90, "green"), T("- DraftKings letter", 960, 520, 44, "grey", at=0.3))
sc("Which raises Linda's question. If the rivals aren't hurting you, why spend seven hundred million fighting them?",
   G(960, "hips", "smug", extras=LINDA), T("then why $700M?", 960, 330, 90, "red", at=0.4))
sc("The company's answer: it follows the data. It says these new customers stay and trade about as much as its sportsbook customers do.",
   G(600, "point", "happy", **GIANT), P("globe", 1300, 860, 1.0, at=0.3), T("NEW STATES", 1300, 400, 80, "green", at=0.5))
sc("Not everyone is following. Penn Entertainment's digital boss said, we're not getting sucked into the noise of prediction markets.",
   G(1100, "hips", "neutral", shirt="orange", extras=["tie"], label="Penn exec"), T("\"not getting sucked|into the noise\"", 600, 400, 64, "dark", at=0.3))
sc("FanDuel's owner went the other way. Its finance chief said it expects to keep investing at similar or higher levels.",
   G(800, "point", "grin", shirt="blue", extras=["tie"], label="Flutter CFO"), P("arrowup", 1350, 820, 1.1, color="green", at=0.4), T("\"similar or higher\"", 1350, 380, 70, "dark", at=0.5))
sc("Quick pause. If you like the news explained calmly, with doodles instead of shouting, subscribe. That's the whole pitch.",
   G(960, "wave", "happy", extras=DAVE), T("SUBSCRIBE?", 960, 330, 110, "red", at=0.3), bg="yellow")

# PART 5 -----------------------------------------------------------------------
sc("Now the real cliffhanger. Is a sports event contract a financial swap, or is it just a bet wearing a suit?",
   G(960, "stand", "smug", s=1.2, shirt="purple", extras=["tie", "tophat"]), T("SWAP or BET?", 960, 300, 120, "dark", at=0.4), chapter="Part 5: The Courtroom Coin Flip")
sc("If it's a swap, federal law may override the states. If it's a bet, states can regulate it or ban it.",
   T("SWAP = FEDERAL", 600, 400, 80, "purple"), T("BET = STATES", 1350, 400, 80, "green", at=0.4), P("scale", 960, 880, 1.0, at=0.2))
sc("In April, a federal appeals court covering New Jersey sided with Kalshi, and said its sports contracts are swaps.",
   G(600, "point", "neutral", **JUDGE, label="3rd Circuit"), ST("KALSHI WINS", 1350, 420, 70, 420, at=0.4), P("calendar", 1350, 800, 0.7, text="APRIL", at=0.2))
sc("In August, the court covering Nevada said the opposite. It found a contract on which team wins is fundamentally a sports bet.",
   G(600, "point", "neutral", **JUDGE, label="9th Circuit"), ST("STATES WIN", 1350, 420, 70, 420, at=0.4), P("calendar", 1350, 800, 0.7, text="AUG 28", at=0.2))
sc("In September, the court covering Ohio and Tennessee agreed with the states. Courts disagreeing like this is a circuit split.",
   G(450, "point", "neutral", s=0.8, **JUDGE, label="6th Circuit"), ST("STATES", 1000, 420, 70, 300, at=0.3), T("CIRCUIT SPLIT", 1450, 700, 90, "red", at=0.6))
sc("New Jersey has asked the Supreme Court to step in. Ohio, thirty-eight other states and DC filed a brief backing it.",
   C(0, 39, 700, 380, "{:.0f} STATES", 150, "green"), T("+ DC", 700, 540, 70, "green", at=0.5), P("envelope", 1350, 820, 1.0, at=0.3))
sc("On November fourth, the Nevada court refused to rehear Kalshi's case. Kalshi now has until February second to go to the Supreme Court.",
   P("stopwatch", 600, 860, 1.0, text="90 DAYS"), P("calendar", 1300, 860, 1.0, text="FEB 2", at=0.4))
sc("California's attorney general has joined eleven of these briefs. His words: prediction markets cannot use federal loopholes to bypass state gambling laws.",
   G(600, "point", "angry", extras=OFF, label="California AG"), T("\"federal loopholes\"", 1300, 400, 80, "green", at=0.3), C(0, 11, 1300, 620, "{:.0f} briefs", 100, "dark", at=0.5))
sc("Kalshi's side, from its filing: it is now exposed to civil and criminal liability, even though it is abiding by federal law.",
   G(1300, "shrug", "worried", **UPSTART, label="Kalshi"), T("\"abiding by|federal law\"", 600, 400, 74, "purple", at=0.3))
sc("And the regulator backs Kalshi. On October ninth, the CFTC proposed rules calling sports, politics and weather contracts swaps.",
   P("building", 600, 900, 0.9, text="CFTC"), P("clipboard", 1300, 860, 0.9, text="NEW RULE", at=0.3), P("calendar", 1650, 420, 0.6, text="NOV 18", at=0.6))
sc("A federal agency on one side, dozens of states on the other, judges split. Depending on who you ask, both are defending the law.",
   P("building", 450, 900, 0.8, text="CFTC"), P("scale", 960, 880, 1.1, at=0.3), P("capitol", 1450, 900, 0.8, text="STATES", at=0.2))

# PART 6 -----------------------------------------------------------------------
sc("Who gets hit meanwhile? Shareholders, first. The stock is down about half this year.",
   G(600, "cry", "sad", extras=DAVE), P("wallet", 1300, 860, 1.0, text="-50%", at=0.3), chapter="Part 6: Who Pays", bg="teal")
sc("DraftKings' plan assumes a Supreme Court ruling around mid twenty twenty-eight. It says it will adjust spending if the rules change.",
   P("calendar", 600, 860, 1.0, text="MID-2028"), P("moneybag", 1300, 880, 1.0, at=0.3), {"cross": [1300, 760, 160], "at": 0.6})
sc("Then there are states. Legal sportsbooks need a state licence. States say contracts that skip that licence also skip their consumer protections.",
   P("capitol", 650, 900, 1.0, text="STATE"), P("dollar", 1300, 760, 1.0, text="TAX", at=0.3), AR((850, 640), (1150, 640), "green", at=0.5))
sc("California's attorney general says it's about people: he warns these markets fuel gambling addiction and wants young people protected.",
   T("ADDICTION", 960, 330, 110, "red"), T("YOUNG USERS", 960, 520, 90, "dark", at=0.4))
sc("Prediction market companies answer that they're regulated too, just by Washington, and that they follow the rules their federal regulator sets.",
   G(960, "present", "neutral", **UPSTART), P("building", 1500, 900, 0.8, text="CFTC", at=0.3))
sc("And Dave. If betting stops being fun, free help is one call away. In the US: one eight hundred GAMBLER.",
   G(600, "think", "neutral", extras=DAVE), T("1-800-GAMBLER", 1300, 420, 90, "dark", at=0.3), P("phone", 1300, 760, 0.9, at=0.4))

# PART 7 -----------------------------------------------------------------------
sc("What happens next? Three dates to watch.",
   P("calendar", 960, 860, 1.2, text="NEXT"), T("3 DATES", 960, 330, 120, "red", at=0.3), chapter="Part 7: What's Next", bg="sky")
sc("One: November eighteenth, when comments close on the CFTC's new rules.",
   P("calendar", 700, 860, 1.0, text="NOV 18"), P("clipboard", 1300, 860, 0.9, text="CFTC RULE", at=0.3))
sc("Two: early December, when Kalshi argues in a New York state court over subpoenas from the state's gaming commission.",
   P("calendar", 700, 860, 1.0, text="DEC"), P("envelope", 1300, 800, 1.0, text="SUBPOENA", at=0.3))
sc("Three: February second, Kalshi's deadline to petition the Supreme Court, unless it gets more time.",
   P("calendar", 700, 860, 1.0, text="FEB 2"), P("building", 1300, 900, 0.9, text="SUPREME COURT", at=0.3))
sc("Bull case: customers keep trading, courts side with the CFTC, and Friday looks like a bargain.",
   G(600, "fist", "grin", extras=ECON), P("arrowup", 1300, 820, 1.1, color="green", at=0.3), T("BULL CASE", 1300, 380, 80, "green", at=0.5))
sc("Bear case: the Supreme Court sides with the states, and much of that seven hundred million bought customers it can't keep.",
   G(600, "facepalm", "worried", extras=ECON), P("arrowdown", 1300, 820, 1.1, color="red", at=0.3), T("BEAR CASE", 1300, 380, 80, "red", at=0.5))
sc("Nobody knows which one it'll be. Not the analysts, not the judges, and definitely not Dave. We just count the facts.",
   G(500, "shrug", "confused", extras=ECON), G(960, "shrug", "neutral", **JUDGE), G(1420, "shrug", "confused", extras=DAVE), T("NOBODY KNOWS", 960, 280, 100, "dark", at=0.4))

# RECAP ------------------------------------------------------------------------
sc("Recap. On November sixth, DraftKings fell twenty-one point three percent after raising prediction-market spending to up to seven hundred million.",
   C(0, -21.3, 650, 400, "{:.1f}%", 150), P("moneybag", 1350, 880, 1.0, text="$700M", at=0.3), chapter="Recap")
sc("Prediction markets say sports contracts are federal financial products. Dozens of states say they're bets. The appeals courts are split.",
   T("FEDERAL?", 600, 400, 90, "purple"), T("BETS?", 1350, 400, 90, "green", at=0.3), P("scale", 960, 860, 1.0, at=0.5))
sc("And the Supreme Court will probably have the final word, which, ironically, makes the whole thing a prediction market of its own.",
   P("building", 960, 900, 1.2, text="SUPREME COURT"), P("pricetag", 1550, 500, 0.8, text="YES 50c?", at=0.5))
sc("Dave skipped both buttons and just watched the game. Somehow, he's the only one who didn't lose money this week.",
   G(700, "hips", "smug", extras=DAVE), P("tv", 1300, 880, 1.1, text="GAME ON", at=0.3), P("coffee", 1650, 880, 0.6, at=0.5), bg="yellow")
sc("Your turn. Is a sports contract a bet or a financial product? Tell us in the comments.",
   T("BET or CONTRACT?", 960, 400, 120, "red"), P("speech", 960, 850, 0.9, at=0.3))
sc("This has been The Doodle Desk. We draw it, we count it, and we never bet the house on a court date.",
   G(960, "wave", "happy", extras=DAVE), T("THE DOODLE DESK", 960, 330, 110, "dark", at=0.3))


script = {
    "id": "ep023",
    "title": "The Betting Giant Made a $700M Bet. Wall Street Ran.",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Nov 6, 2026, DraftKings stock fell 21.3% to $18.51 (intraday low $16.55, a three-year low) after its Q3 report: "
        "revenue $1.33B (+16%, vs ~$1.39B expected), an adjusted EBITDA loss of $317M (vs $126M a year earlier), and a cut to its 2026 adjusted EBITDA outlook "
        "from $700M-$900M to $175M-$275M, mainly because it raised its spending on DraftKings Predictions to $650M-$700M. "
        "We explain what a prediction market is, why Kalshi and Polymarket say sports event contracts are federal financial products (CFTC) while dozens of states say they're bets, "
        "how the appeals courts split (3rd Circuit for Kalshi; 9th, 6th and 2nd Circuits for the states), and what comes next: CFTC comments close Nov 18, "
        "Kalshi's Supreme Court deadline is Feb 2, 2027. Both sides are given in their own sourced words; real people appear only as generic labelled stick figures.\n\n"
        "This video is an explainer, not betting or investment advice. If gambling stops being fun, call 1-800-GAMBLER (US).\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "DraftKings Q3 2026 shareholder letter (Nov 5, 2026): https://s21.q4cdn.com/869500724/files/doc_earnings/2026/q3/generic/BU-Q3-26.pdf\n"
        "24/7 Wall St., DraftKings plunges on weak 2027 forecast and prediction-market spending (Nov 6, 2026): https://247wallst.com/investing/2026/11/06/draftkings-plunges-27-on-weak-2027-forecast-and-prediction-market-spending-flutter-sinks-8-penn-entertainment-drops-4/\n"
        "Stocktwits, Why did DKNG, SOUN, ORCL stocks plunge to 52-week lows (Nov 9, 2026): https://stocktwits.com/news-articles/markets/equity/why-did-dkng-soun-orcl-stocks-plunge-to-52-week-lows-last-week/cNGAv0oR9I6\n"
        "Big Moves newsletter, Nov 6, 2026: https://bigmoves.substack.com/p/big-moves-november-6-2026\n"
        "Boston Globe, DraftKings stock tumbles after disclosing big spending on prediction markets (Nov 6, 2026): https://www.bostonglobe.com/2026/11/06/business/draftkings-prediction-markets-stock-expenses/\n"
        "Foley & Lardner, Prediction markets overview: regulation, litigation and the road to the Supreme Court (Nov 2026): https://www.foley.com/insights/publications/2026/11/prediction-markets-overview-regulation-litigation-and-the-road-to-the-supreme-court\n"
        "CDC Gaming, Appeals court denies Kalshi's petition for rehearing in Nevada case (Nov 4, 2026): https://cdcgaming.com/u-s-appeals-court-denies-kalshis-petition-for-rehearing-in-nevada-case/\n"
        "California Attorney General, Bonta defends state gambling laws against Kalshi, again (Nov 6, 2026): https://oag.ca.gov/news/press-releases/attorney-general-bonta-defends-state-gambling-laws-against-kalshi-again\n"
        "Sports Betting Dime, Second Circuit denies Kalshi, Coinbase injunction motion (Nov 3, 2026): https://www.sportsbettingdime.com/news/industry/second-circuit-denies-kalshi-coinbase-injunction-motion-in-new-york-and-connecticut/\n"
        "Ninth Circuit opinion, KalshiEX v. Assad (Aug 28, 2026): https://cdn.ca9.uscourts.gov/datastore/opinions/2026/08/28/25-7516.pdf\n\n"
        "#draftkings #predictionmarkets #kalshi #stockmarket #explained #business #supremecourt #stickfigure"
    ),
    "tags": ["draftkings", "prediction markets", "kalshi", "polymarket", "draftkings stock", "fanduel", "sports betting", "cftc",
             "supreme court", "stock market news", "business explained", "event contracts", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "-21%|IN A DAY", "size": 200, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["sweat", "tie"], "shirt": "green"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "moneybag", "x": 400, "y": 1050, "s": 1.5, "text": "$700M"}, {"arrow": [[650, 820], [1000, 640]], "color": "red"}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep023.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

"""Episode 6: the AI chip-stock rout, week of Oct 12-16, 2026."""
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
BOSS = dict(extras=["tie"], shirt="dark")       # generic tech-company boss
TRADER = dict(extras=["cap"], shirt="green")     # generic investor
FED = dict(extras=["glasses", "tie"], shirt="navy")

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN -------------------------------------------------------------------
sc("This is a balloon.",
   P("balloon", 960, 980, 1.5, text="AI", color="red", anim="bob"), cam={"from": [960, 560, 1.4], "to": [960, 540, 1.05]})
sc("It is very big. It is very shiny.",
   P("balloon", 960, 1000, 1.8, text="AI", color="red", anim="pulse"), T("$$$", 1500, 300, 140, "money", at=0.4))
sc("And this week, a lot of people started staring at it, wondering where they left the pin.",
   P("balloon", 700, 1000, 1.4, text="AI", color="red"), G(1350, "think", "worried", extras=DAVE, look=-1, at=0.3),
   T("?", 1500, 380, 160, "red", at=0.6))
sc("Meet Dave. Dave doesn't own a data center. Dave owns a retirement account and a phone with an app on it.",
   G(700, "hold", "neutral", extras=DAVE), P("phone", 1250, 860, 1.1, text="401(k)", at=0.35))
sc("On Friday evening, Dave opened the app.",
   P("phone", 960, 900, 1.6, text="LOADING..."), G(450, "hold", "neutral", extras=DAVE, at=0.2))
sc("The Nasdaq, home of most big tech stocks, finished the week down about four and a half percent.",
   C(0, -4.5, 960, 420, fmt="{:.1f}%", size=260, color="red", dur=1.6), P("arrowdown", 1550, 800, 1.2, color="red", at=0.5))
sc("Its worst week since June.",
   P("calendar", 700, 860, 1.1, text="JUNE"), {"stamp": "WORST WEEK", "x": 1250, "y": 450, "size": 80, "w": 420, "at": 0.3})
sc("Dave made a noise only dogs could hear.",
   G(960, "panic", "scream", extras=DAVE, anim="shake"), P("phone", 1450, 820, 0.8, text="-4.5%", at=0.1), bg="yellow")
sc("Today's question: is the A.I. stock boom running out of money? And does any of this matter if you've never bought a single chip?",
   G(420, "think", "confused", extras=DAVE), T("RUNNING OUT", 1180, 330, 120, "red", at=0.3), T("OF MONEY?", 1180, 470, 120, "red", at=0.4),
   P("chip", 1180, 900, 0.7, text="AI", at=0.55), chapter="Today's question")
sc("We'll go through what fell, how far, the two big reasons why, who it hits, and what both the worried and the calm people say.",
   P("clipboard", 760, 900, 1.1, text="FACTS"), G(1300, "present", "neutral", extras=LINDA, at=0.35))
sc("Quick note: we're stick figures, not financial advisers. Nothing here tells you to buy or sell anything.",
   G(960, "hips", "smug", extras=LINDA), {"stamp": "NOT ADVICE", "x": 1450, "y": 380, "size": 70, "w": 380, "at": 0.35})

# PART 1 --------------------------------------------------------------------
sc("Let's start with the scoreboard for the week of October twelfth to sixteenth.",
   P("scoreboard", 960, 900, 1.2, text="OCT 12-16"), chapter="Part 1: What fell")
sc("The S&P 500, the big index of five hundred large American companies, fell about two percent for the week.",
   C(0, -2.0, 700, 420, fmt="{:.1f}%", size=200, color="red"), P("building", 1400, 900, 0.9, text="S&P 500", at=0.4))
sc("It closed Friday at 7,659. And here's the twist: just one week earlier, it had set an all-time high.",
   C(7000, 7659, 700, 400, fmt="{:,.0f}", size=170, color="navy"), {"stamp": "RECORD", "x": 1400, "y": 400, "size": 80, "w": 300, "at": 0.45})
sc("So the whole of last week's gains? Gone. Like a sandcastle meeting a Tuesday.",
   P("chart", 960, 900, 1.2, text="+  -", color="red"), {"cross": [960, 560, 230], "at": 0.4})
sc("The Nasdaq composite closed at 26,140, down about four and a half percent on the week.",
   C(27000, 26140, 960, 400, fmt="{:,.0f}", size=190, color="red"), P("arrowdown", 1550, 820, 1.0, color="red", at=0.5))
sc("The Dow, which has fewer tech stocks, mostly shrugged. On Friday it slipped just a third of a percent.",
   G(960, "shrug", "neutral", extras=OFF, label="the Dow"), T("-0.3%", 1450, 420, 120, "orange", at=0.4))
sc("But the real crater was in chips. The Philadelphia Semiconductor Index fell eleven point four percent in one week.",
   P("chip", 700, 900, 1.0, text="SOX"), C(0, -11.4, 1300, 420, fmt="{:.1f}%", size=220, color="red", at=0.3))
sc("That's its worst week since April 2025.",
   P("calendar", 960, 860, 1.2, text="APR 2025"), P("arrowdown", 1450, 820, 0.9, color="red", at=0.4))
sc("And by Thursday, chip stocks had fallen for eight days in a row, a losing streak Yahoo Finance said was the longest since October 2008.",
   *[P("arrowdown", 300 + k * 190, 760, 0.6, color="red", at=0.07 * k) for k in range(8)], T("8 DAYS", 960, 280, 130, "red", at=0.6))
sc("October 2008 is when Lehman Brothers had just collapsed. Not a month anyone wants to be compared to.",
   P("calendar", 600, 860, 1.0, text="OCT 2008"), G(1250, "facepalm", "tired", extras=ECON, at=0.3))
sc("On Friday alone, all but seven of the seventy five tech stocks in the S&P 500 closed lower, according to the Associated Press.",
   *[P("arrowdown", 200 + k * 110, 700, 0.35, color="red", at=0.02 * k) for k in range(15)], C(0, 68, 960, 300, fmt="{:.0f} of 75", size=130, color="red", at=0.4))

# PART 2 --------------------------------------------------------------------
sc("So where did it start? Not in America. It started in memory chips.",
   P("chip", 960, 900, 1.3, text="MEMORY"), chapter="Part 2: The memory-chip crash")
sc("Memory chips are what let your phone, laptop, and every A.I. server remember things. Very boring. Very profitable.",
   P("phone", 500, 900, 0.9), P("laptop", 960, 900, 0.8, at=0.2), P("robot", 1450, 900, 0.9, at=0.4))
sc("Three companies make most of them: Micron in the US, and Samsung and S.K. Hynix in South Korea.",
   P("chip", 450, 900, 0.7, text="MICRON"), P("chip", 960, 900, 0.7, text="SAMSUNG", at=0.25), P("chip", 1470, 900, 0.7, text="HYNIX", at=0.5))
sc("Early in the week, investors got nervous after reports that a Chinese company, ChangXin Memory Technologies, had made big advances.",
   P("globe", 600, 880, 1.0), P("chip", 1250, 900, 0.8, text="CXMT", color="red", at=0.3), T("NEW RIVAL?", 1250, 300, 90, "red", at=0.5))
sc("There were also worries that so many new factories are being built, the world could have too many memory chips by around 2029.",
   *[P("chip", 350 + k * 250, 900, 0.5, at=0.08 * k) for k in range(6)], P("calendar", 960, 380, 0.8, text="2029?", at=0.6))
sc("Then, on Thursday, South Korea's main stock index, the Kospi, dropped seven point seven percent in a single day.",
   C(0, -7.7, 960, 420, fmt="{:.1f}%", size=260, color="red"), P("globe", 1550, 860, 0.7, at=0.4))
sc("For a whole country's stock market, that's not a bad day. That's a fire drill with real fire.",
   P("fire", 960, 900, 1.4, anim="pulse"), G(1500, "run", "scream", extras=TRADER["extras"], shirt="green", at=0.3), bg="yellow")
sc("Samsung fell nine and a half percent that day. S.K. Hynix fell eleven point four.",
   {"bars": {"values": [9.5, 11.4], "labels": ["Samsung", "SK Hynix"], "colors": ["orange", "red"], "fmt": "-{}%", "w": 700, "h": 420}, "x": 960, "y": 820})
sc("Over the whole week, according to Investing.com, citing Reuters, it was Micron down fourteen point six percent, Samsung down seventeen point eight, and S.K. Hynix down twenty four point three.",
   {"bars": {"values": [14.6, 17.8, 24.3], "labels": ["Micron", "Samsung", "SK Hynix"], "colors": ["orange", "red", "red"], "fmt": "-{}%", "w": 820, "h": 440}, "x": 960, "y": 830})
sc("In June the Kospi had crossed nine thousand points. On Thursday it closed around fifty five hundred.",
   C(9000, 5549, 960, 420, fmt="{:,.0f}", size=200, color="red", dur=2.2), P("arrowdown", 1550, 820, 1.0, color="red", at=0.5))
sc("Japan's Nikkei fell four point eight percent the same day. SoftBank, a big investor in OpenAI, fell nine point four.",
   T("NIKKEI -4.8%", 650, 400, 100, "red"), T("SOFTBANK -9.4%", 1300, 600, 100, "red", at=0.4))
sc("Then the wave crossed the Pacific, and Nvidia, the world's most valuable company, lost more than two hundred fourteen billion dollars of value in one day.",
   P("ship", 600, 900, 0.9), {"arrow": [[800, 600], [1250, 600]], "at": 0.2}, C(0, 214, 1450, 400, fmt="${:.0f}B", size=160, color="red", at=0.4))

# PART 3 --------------------------------------------------------------------
sc("So why now? Reason number one is boring, but it's the big one. Inflation.",
   T("REASON #1", 960, 300, 130, "navy"), P("thermo", 960, 900, 1.1, text="3.7%", color="red", at=0.3), chapter="Part 3: Reason one, inflation")
sc("On Wednesday, the government said consumer prices were up three point seven percent from a year earlier. In August it was three point four.",
   {"bars": {"values": [3.4, 3.7], "labels": ["Aug", "Sep"], "colors": ["grey", "red"], "fmt": "{}%", "w": 640, "h": 420}, "x": 960, "y": 820})
sc("Economists had expected less. Wholesale prices, what businesses pay, rose at the fastest pace since 2022.",
   G(600, "panic", "shock", extras=ECON), P("pricetag", 1300, 880, 1.1, text="2022", color="red", at=0.35))
sc("Here's why inflation hurts tech stocks. When prices run hot, the Federal Reserve tends to keep interest rates high, or raise them.",
   P("thermo", 600, 900, 1.0, text="HOT", color="red"), P("building", 1300, 900, 0.9, text="THE FED", at=0.35))
sc("Last month the Fed already raised rates by a quarter point, to between three point seven five and four percent. Its first increase in three years.",
   C(3.5, 3.75, 700, 420, fmt="{:.2f}%", size=170, color="red"), T("to 4.00%", 1350, 420, 100, "red", at=0.4), P("arrowup", 1350, 800, 0.9, color="red", at=0.5))
sc("And the ten-year U.S. government bond is paying about five point one percent. That's high for borrowing anything.",
   C(4.0, 5.1, 960, 420, fmt="{:.1f}%", size=240, color="navy"), T("10-YEAR YIELD", 960, 620, 70, "dark", at=0.4))
sc("The Fed chair spoke at a meeting of finance leaders in Bangkok this week. He gave no fresh signal about the next move.",
   G(800, "present", "neutral", **FED, label="the Fed chair"), P("podium", 800, 900, 0.8), P("speech", 1350, 450, 1.0, text="...", at=0.4))
sc("One market strategist, Michael O'Rourke of Jones Trading, put it simply.",
   G(960, "present", "neutral", extras=ECON, label="strategist"))
sc("Quote: hot inflation data suggests interest rates will remain higher for longer, and investors are repositioning defensively.",
   P("speech", 960, 500, 1.6, text="HIGHER|FOR LONGER"), T("— Michael O'Rourke, Jones Trading", 960, 880, 50, "dark", at=0.4))

# PART 4 --------------------------------------------------------------------
sc("Reason number two is the one people are really whispering about: debt.",
   T("REASON #2", 960, 300, 130, "navy"), P("moneybag", 960, 900, 1.1, text="IOU", color="red", at=0.3), chapter="Part 4: Reason two, debt")
sc("Building A.I. is wildly expensive. Data centers, power, cooling, and many thousands of chips.",
   P("building", 500, 900, 0.9, text="DATA"), P("fan", 960, 900, 0.8, at=0.2), P("chip", 1450, 900, 0.7, at=0.4))
sc("A lot of that has been paid for with borrowed money. The Associated Press reports companies have leaned on debt markets to fund the spree.",
   G(600, "hold", "grin", **BOSS, label="AI company"), P("moneybag", 1000, 880, 0.8, text="LOAN", at=0.3), P("building", 1500, 900, 0.8, text="BANK", at=0.5))
sc("Borrowing is easy when money is cheap. With bond yields at their highest in years, it isn't cheap anymore.",
   P("pricetag", 700, 880, 1.1, text="LOAN: $"), P("pricetag", 1250, 880, 1.4, text="LOAN: $$$", color="red", at=0.4))
sc("The poster child this week was CoreWeave, a so-called neocloud. It rents out A.I. computing power to other companies.",
   P("building", 960, 900, 1.0, text="COREWEAVE"), T("NEOCLOUD", 960, 260, 90, "teal", at=0.4))
sc("Think of it as a landlord for A.I. chips. Very popular landlord. Very large mortgage.",
   P("house", 700, 900, 1.0, text="CHIPS"), G(1300, "hips", "smug", **BOSS, label="landlord", at=0.3), T("MORTGAGE", 1300, 280, 80, "red", at=0.55))
sc("On Wednesday, CoreWeave's stock fell fifteen percent, its worst day since February.",
   C(0, -15, 960, 420, fmt="{:.0f}%", size=260, color="red"), P("arrowdown", 1550, 820, 1.0, color="red", at=0.5))
sc("By Thursday, the price of insurance against CoreWeave defaulting hit a record. Bloomberg data implied roughly sixty percent odds of a default within five years.",
   P("lock", 600, 900, 1.0, text="INSURANCE"), C(0, 60, 1300, 420, fmt="{:.0f}%", size=230, color="red", at=0.3), T("odds, 5 years", 1300, 600, 60, "dark", at=0.5))
sc("Some of its bonds traded at about eighty one cents on the dollar, with a yield over fifteen percent.",
   P("dollar", 700, 900, 1.2, text="$1"), T("= 81¢", 1300, 450, 160, "red", at=0.35))
sc("CoreWeave pushed back. In a statement it said the market sometimes misunderstands new kinds of companies and acts irrationally, and that it's confident in its business model.",
   G(960, "fist", "neutral", **BOSS, label="CoreWeave"), P("speech", 1450, 420, 0.9, text="CONFIDENT", at=0.4))
sc("And Nvidia's chief executive, Jensen Huang, whose company backs CoreWeave, said, quote, I'm optimistic. Their cost of capital is actually decreasing.",
   G(800, "present", "happy", extras=["tie"], shirt="dark", label="Nvidia CEO"), P("speech", 1350, 420, 1.0, text="OPTIMISTIC", at=0.35))
sc("The stock bounced back on Thursday. Then on Friday it fell almost twelve percent again. A yo-yo with a balance sheet.",
   P("arrowup", 600, 820, 0.9, color="green"), P("arrowdown", 1000, 820, 0.9, color="red", at=0.35), T("-11.9%", 1450, 420, 130, "red", at=0.55))
sc("A Baird strategist, Ted Mortonson, said the sell-off is increasingly about who needs financing, and what that financing costs.",
   G(700, "think", "neutral", extras=ECON, label="Baird strategist"), P("clipboard", 1300, 900, 1.0, text="WHO NEEDS|MONEY?", at=0.35))
sc("Even good news didn't help. Taiwan's TSMC reported a record profit, its sixth record quarter in a row. Its stock fell anyway.",
   P("trophy", 600, 900, 1.0, text="RECORD"), P("arrowdown", 1250, 820, 1.0, color="red", at=0.4))
sc("That's like winning the race and being booed for not winning it faster.",
   G(700, "fist", "grin", extras=["cap"], shirt="green"), P("trophy", 1000, 880, 0.6, at=0.1), G(1450, "point", "angry", extras=DAVE, look=-1, at=0.4))

# PART 5 --------------------------------------------------------------------
sc("So who does this actually hit? Start with Dave.",
   G(960, "shrug", "worried", extras=DAVE), chapter="Part 5: Who it hits")
sc("Most retirement funds track big indexes. A few tech giants now make up a huge share of those indexes. So when they drop, Dave drops too.",
   P("phone", 600, 880, 1.0, text="401(k)"), {"arrow": [[800, 600], [1200, 600]], "at": 0.3}, G(1450, "cry", "sad", extras=DAVE, at=0.4))
sc("Linda, meanwhile, owns a fund full of toothpaste and medicine companies. Her week was fine.",
   G(700, "hips", "smug", extras=LINDA), P("cart", 1300, 900, 0.9, text="STAPLES", at=0.35))
sc("Because money doesn't vanish. It moves. Healthcare stocks opened at a record on Thursday, and consumer staples flew.",
   {"arrow": [[500, 600], [1400, 600]], "color": "green"}, P("chip", 450, 900, 0.6), P("cart", 1450, 900, 0.8, text="HEALTH", at=0.4))
sc("A retail fund gained more than three percent that day. Some investors left chips and went shopping. Literally.",
   P("cart", 960, 900, 1.2, text="+3%", color="green"), G(1500, "run", "grin", extras=["cap"], shirt="green", at=0.3))
sc("Then there's Apple. Apple hasn't spent billions building its own A.I. data centers. And this week its value crossed five trillion dollars, for the second time.",
   P("phone", 700, 900, 1.0, text="APPLE"), C(0, 5, 1300, 420, fmt="${:.0f} TRILLION", size=110, color="green", at=0.35))
sc("Sometimes the best investment strategy is not being invited to the party.",
   G(960, "stand", "smug", extras=["glasses"], shirt="grey"), P("balloon", 1450, 900, 0.6, text="AI", at=0.3))
sc("Bonds won too. Investors piled into U.S. government debt, and Treasury yields dropped from their highs. Homebuilder stocks rallied.",
   P("house", 960, 900, 1.0, text="HOMES"), P("arrowup", 1450, 820, 0.9, color="green", at=0.4))
sc("And in South Korea, Samsung and S.K. Hynix are such a big slice of the market that their bad week becomes the whole country's bad week.",
   P("globe", 600, 860, 0.9), G(1200, "cry", "sad", extras=["cap"], shirt="blue", at=0.3), P("chip", 1550, 900, 0.5, text="SAMSUNG", at=0.4))

# PART 6 --------------------------------------------------------------------
sc("Now, is this the bubble popping? Depending on who you ask, you get two very different answers.",
   P("balloon", 960, 1000, 1.3, text="AI"), T("POP?", 1500, 300, 140, "red", at=0.4), chapter="Part 6: Bubble or bump?")
sc("The worried camp says: chips are being built faster than anyone can use them, debts are piling up, and money is getting expensive.",
   G(600, "panic", "worried", extras=ECON, label="worried camp"), P("chip", 1150, 900, 0.5), P("chip", 1350, 900, 0.5, at=0.2), P("moneybag", 1600, 900, 0.6, text="DEBT", at=0.4))
sc("Investing.com, citing Reuters, reported fears that twenty twenty six could mark the peak for earnings growth.",
   P("chart", 960, 900, 1.2, text="PEAK?"), {"ring": [960, 520, 160], "at": 0.4})
sc("And a few companies carry the load. Nvidia, Micron, and Google are expected to make up about a third of this year's earnings growth.",
   P("chip", 500, 900, 0.6, text="NVDA"), P("chip", 900, 900, 0.6, text="MU", at=0.2), P("chip", 1300, 900, 0.6, text="GOOG", at=0.35), C(0, 33, 1650, 420, fmt="~{:.0f}%", size=130, color="red", at=0.5))
sc("The calm camp says: demand for A.I. chips is real. TSMC just had a record quarter. Companies keep reporting big orders.",
   G(1300, "hips", "happy", extras=["tie"], shirt="green", label="calm camp"), P("trophy", 650, 900, 0.9, text="RECORD", at=0.3))
sc("They also point out the S&P 500 was at an all-time high just a week ago. A two percent drop from a record is still, well, near a record.",
   C(0, 2, 700, 420, fmt="-{:.0f}%", size=200, color="orange"), {"stamp": "NEAR RECORD", "x": 1350, "y": 450, "size": 70, "w": 420, "at": 0.4})
sc("And markets bounce. On Thursday, the Dow jumped nearly six hundred points. One week rarely tells you the ending.",
   C(0, 600, 960, 420, fmt="+{:.0f}", size=220, color="green"), P("arrowup", 1550, 820, 1.0, color="green", at=0.4))
sc("We don't pick a team. We just count the facts.",
   P("scale", 960, 900, 1.2), G(1500, "stand", "neutral", extras=LINDA, at=0.3))

# PART 7 --------------------------------------------------------------------
sc("So what's next? Three things to watch.",
   P("eye", 960, 800, 1.2), chapter="Part 7: What's next")
sc("One: earnings season. It only began in earnest this week, and the A.P. says expectations for profits are high. A.I. giants report in the coming weeks.",
   T("1", 400, 400, 200, "navy"), P("calendar", 960, 860, 1.0, text="EARNINGS", at=0.3), P("chip", 1450, 900, 0.6, at=0.5))
sc("Two: the Fed. Hot prices push toward another rate hike. A falling stock market pushes the other way. The Fed has to pick.",
   T("2", 400, 400, 200, "navy"), P("scale", 1050, 900, 1.2, at=0.3), T("HIKE?", 1400, 300, 90, "red", at=0.5))
sc("Three: the debt. Watch whether companies like CoreWeave can keep borrowing at a price that makes sense.",
   T("3", 400, 400, 200, "navy"), P("moneybag", 1050, 880, 1.0, text="IOU", at=0.3), T("?", 1450, 380, 160, "red", at=0.5))
sc("Yahoo Finance put it neatly: watch whether the company's debt starts recovering alongside its shares. That's the real sign the fear is easing.",
   P("chart", 700, 900, 1.0, text="STOCK"), P("chart", 1300, 900, 1.0, text="DEBT", at=0.3), {"arrow": [[900, 450], [1100, 450]], "at": 0.5})
sc("And Dave? Dave's plan is to close the app and not open it until Christmas.",
   G(800, "hold", "tired", extras=DAVE), P("phone", 1250, 880, 0.8, text="CLOSED", at=0.3), P("calendar", 1600, 860, 0.7, text="DEC 25", at=0.5))

# RECAP --------------------------------------------------------------------
sc("Recap. Tech stocks had their worst week since June. Chip stocks lost eleven percent. Memory chipmakers lost far more.",
   T("-4.5%", 500, 420, 140, "red"), T("-11.4%", 1000, 420, 140, "red", at=0.25), T("-24%", 1500, 420, 140, "red", at=0.5), chapter="Recap")
sc("The reasons: inflation hotter than expected, which means expensive money, and a mountain of debt behind the A.I. building boom.",
   P("thermo", 600, 900, 0.9, text="3.7%", color="red"), P("moneybag", 1300, 900, 1.0, text="DEBT", at=0.35))
sc("The worried say bubble. The calm say bump. The next few weeks of earnings and one Fed decision will say a lot more than any of us.",
   P("balloon", 600, 1000, 0.9, text="BUBBLE?"), T("vs", 960, 500, 110, "dark", at=0.2), P("chart", 1350, 900, 0.9, text="BUMP?", at=0.4))
sc("Meanwhile, somewhere in Silicon Valley, a very large balloon is being very carefully patched.",
   P("balloon", 960, 1000, 1.6, text="AI", color="red", anim="bob"), G(1550, "hold", "worried", **BOSS, at=0.3), T("PATCH", 960, 260, 80, "dark", at=0.55), bg="yellow")
sc("Your turn: do you think A.I. stocks are a bubble, or just having a bad week? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("balloon", 1250, 950, 0.9, text="?", at=0.3))
sc("And if calm stick figures explaining the news is your kind of thing, subscribe. We'll keep counting the facts.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep006",
    "title": "Is the AI Stock Boom Running Out of Money?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "In the week of October 12-16, 2026, tech stocks had their worst week since June: the Nasdaq fell about 4.5%, chip stocks "
        "lost 11.4%, South Korea's Kospi dropped 7.7% in one day and memory chipmakers lost up to 24%. Why? Hotter-than-expected "
        "inflation (3.7%), higher interest rates and growing worries about the debt behind the AI building boom. Who it hits, what "
        "the worried and the calm camps say, and what to watch next. Explained with stick figures, facts only. Not financial advice.\n\n"
        "Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported.\n\n"
        "Sources:\n"
        "AP via Hartford Courant, US markets weighed down by extended sell-off in the tech sector (Oct 16, 2026): https://www.courant.com/2026/10/16/stock-market\n"
        "AP via Yahoo Finance, Deepening tech sell-off drags stocks lower as major markets slide (Oct 15, 2026): https://finance.yahoo.com/markets/stocks/articles/deepening-tech-sell-off-drags-041902749.html\n"
        "Yahoo Finance live blog, Oct 15, 2026 (CoreWeave, Apple, yields, quotes): https://finance.yahoo.com/markets/live/stock-market-today-dow-sp-500-rise-nasdaq-trims-losses-as-treasury-yields-sink-153611834.html\n"
        "Investing.com / Reuters, Nasdaq notches worst week since late June with a 4.5% slide: https://www.investing.com/news/stock-market-news/nasdaq-futures-edge-lower-as-ai-spending-fed-rate-concerns-weigh-4952930\n"
        "The Telegraph, Global AI stocks sell-off spreads to Wall Street (Oct 15, 2026): https://www.telegraph.co.uk/business/2026/10/15/asian-markets-plunge-amid-tech-sell-off\n"
        "CNBC, AI stocks tumble in global tech rout on AI funding worries (Oct 15, 2026): https://www.cnbc.com/2026/10/15/sk-hynix-samsung-softbank-stocks-asia-tech-rout-ai-funding-worries.html\n"
        "WSJ, Warsh Avoids Signal on October Rate Move: https://www.wsj.com/economy/central-banking/warsh-avoids-signal-on-october-rate-move-a176b0d5\n\n"
        "#ai #stocks #nvidia #stockmarket #explained #stickfigure #news"
    ),
    "tags": ["ai stocks", "ai bubble", "tech stocks sell off", "nasdaq worst week", "chip stocks", "nvidia stock", "coreweave",
             "kospi crash", "stock market news", "news explained", "stick figure animation"],
    "thumbnail": {"bg": "yellow", "text": "AI BUBBLE|POPPING?", "size": 180, "color": "black",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["hair"]},
                  "items": [{"prop": "balloon", "x": 1690, "y": 980, "s": 1.0, "text": "AI", "color": "red"}], "guy_x": 1300},
    "scenes": [s for s in S if s],
}
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep006.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

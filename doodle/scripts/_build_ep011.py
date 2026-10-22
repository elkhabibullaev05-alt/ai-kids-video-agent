"""Episode 11: SpaceX and Tesla form special committees to explore a merger (Oct 20-21, 2026), explained with stick figures."""
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
SHIP = dict(extras=["cap"], shirt="navy")         # generic ship captain
TRUCK = dict(extras=["cap"], shirt="orange")      # generic trucker
TRADER = dict(extras=["cap"], shirt="green")     # generic oil trader
FED = dict(extras=["glasses", "tie"], shirt="navy")

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


CEO = dict(extras=["tie"], shirt="dark", label="the CEO of both")          # generic, role label only
CMTE_T = dict(extras=["glasses", "tie"], shirt="red", label="Tesla committee")
CMTE_S = dict(extras=["glasses", "tie"], shirt="navy", label="SpaceX committee")
ANALYST = dict(extras=["glasses"], shirt="green", label="an analyst")
FUND = dict(extras=["tie", "briefcase"], shirt="purple", label="a pension fund")
INV = dict(extras=["cap"], shirt="teal")

# COLD OPEN --------------------------------------------------------------------
sc("Saturday morning. Dave has two prized possessions: a sensible used car, and a model rocket he built with his nephew.",
   P("car", 600, 900, 1.2), P("rocket", 1350, 900, 1.0, at=0.4), G(1700, "hips", "happy", extras=DAVE, s=0.8, at=0.6),
   cam={"from": [700, 640, 1.3], "to": [960, 540, 1.0]})
sc("Dave has an idea. What if the car and the rocket were one thing? He gets the duct tape.",
   G(500, "think", "grin", extras=DAVE), T("CAR + ROCKET", 1200, 330, 120, "red", at=0.35), P("clipboard", 1350, 860, 0.9, text="TAPE", at=0.6))
sc("Linda, from the porch, asks what problem this solves. Dave says: synergy. Linda goes back inside.",
   G(500, "point", "grin", extras=DAVE), P("speech", 950, 420, 1.0, text="SYNERGY!", at=0.3), G(1450, "facepalm", "tired", look=-1, extras=LINDA, at=0.55))
sc("Dave's idea is a joke. But on Tuesday night, the boss of a rocket company and a car company said something similar. About companies worth trillions.",
   P("rocket", 600, 900, 1.0), P("sportscar", 1350, 900, 1.0, at=0.3), T("$ TRILLIONS", 960, 300, 120, "money", at=0.55), bg="yellow")
sc("SpaceX and Tesla have formed special committees to look at merging. Put the two together at today's prices, and you get roughly three point five trillion dollars.",
   C(0, 3.5, 960, 360, fmt="${:.1f} trillion", size=170, color="money", dur=2.0), P("moneybag", 1650, 900, 0.9, at=0.5))
S.append({"say": "So today's question: why would anyone glue a rocket company to a car company, who decides, and who gets nervous about it? Facts only. Stick figures, obviously.",
          "items": [P("tv", 980, 800, 1.4, text="WHY MERGE?"), G(330, "think", "confused", extras=DAVE, at=0.4)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED ----------------------------------------------------------
sc("Tuesday, October twentieth. SpaceX reports its third-quarter results. On the call with investors, the merger question comes up.",
   P("calendar", 600, 860, 1.1, text="OCT 20"), P("phone", 1300, 880, 1.1, text="CALL", at=0.4), chapter="Part 1: What happened")
sc("The man running both companies, shown here as a generic stick figure, said both boards had formed special committees to discuss the idea.",
   G(700, "present", "neutral", **CEO), P("building", 1350, 900, 0.8, text="SPACEX", at=0.35), P("building", 1650, 900, 0.8, text="TESLA", at=0.5))
sc("Then he added, quote: Because I'm a conflicted party, I can't actually be in the discussions of the special committees.",
   G(600, "shrug", "neutral", **CEO), T("\"I'm a conflicted party\"", 1200, 330, 80, "dark", at=0.3), {"box": [1450, 500, 300, 330], "color": "grey", "at": 0.5})
sc("Which makes sense. He runs SpaceX. He runs Tesla. If he negotiated, he would be haggling with himself.",
   G(560, "point", "angry", look=1, **CEO), G(1360, "point", "angry", look=-1, **CEO), T("vs", 960, 500, 120, "red", at=0.4))
sc("So two rooms of independent directors talk instead. He called it, quote, an odd kabuki dance where two groups of people are talking.",
   G(450, "type", "neutral", **CMTE_T), G(1470, "type", "neutral", look=-1, **CMTE_S), {"arrow": [[700, 520], [1220, 520]], "color": "dark", "at": 0.4},
   {"arrow": [[1220, 600], [700, 600]], "color": "dark", "at": 0.55})
sc("Does he like the idea? Asked directly, he said: Do I think it would be a good idea? Yes.",
   G(600, "pointup", "grin", **CEO), {"stamp": "YES", "x": 1300, "y": 420, "size": 110, "w": 300, "at": 0.45})
sc("But he also warned against treating it as done. Calling a deal certain, he said, would be overstating it.",
   G(600, "think", "neutral", **CEO), {"stamp": "NOT A DEAL", "x": 1300, "y": 420, "size": 70, "w": 420, "at": 0.4})
sc("TechCrunch reports the committees haven't agreed on any terms yet. No price, no structure, no date. Just two rooms and a whiteboard.",
   P("chalkboard", 960, 880, 1.2, text="TERMS: ?"), T("?", 1550, 400, 200, "red", at=0.5))
sc("Wall Street got excited anyway. SpaceX stock closed Tuesday at about a hundred forty-eight dollars. Before markets opened Wednesday, it was about a hundred fifty-eight.",
   C(147.79, 158.30, 960, 360, fmt="${:.2f}", size=170, color="green", dur=2.0), P("arrowup", 1600, 880, 1.0, at=0.5))
sc("That's a jump of about seven percent, partly the merger talk, partly very strong quarterly results.",
   C(0, 7, 900, 360, fmt="+{:.0f}%", size=220, color="green"), P("chart", 1500, 900, 1.0, at=0.4))

# PART 2: THE NUMBERS ------------------------------------------------------------
sc("Let's meet the two companies, with numbers. First, SpaceX. It went public in June at a hundred thirty-five dollars a share.",
   P("rocket", 600, 900, 1.2), C(0, 135, 1250, 380, fmt="${:.0f}", size=180, color="dark", at=0.35), chapter="Part 2: Meet the two companies")
sc("Today the market values it at more than two trillion dollars. That's bigger than the whole economy of most countries.",
   C(0, 2.1, 960, 360, fmt="${:.1f}T", size=200, color="money"), P("globe", 1600, 900, 0.9, at=0.5))
sc("According to CBS News, citing World Bank data, only nineteen countries have an economy above one trillion dollars a year.",
   C(0, 19, 700, 380, fmt="{:.0f}", size=220, color="red"), T("countries", 700, 520, 80, "dark", at=0.3), P("globe", 1350, 900, 1.0, at=0.5))
sc("SpaceX's third quarter: revenue of fourteen point six billion dollars. That's up a hundred sixty-one percent on a year earlier.",
   C(0, 14.6, 700, 360, fmt="${:.1f}B", size=160, color="money"), C(0, 161, 1350, 360, fmt="+{:.0f}%", size=160, color="green", at=0.45))
sc("But here's the surprise. The biggest slice is no longer rockets, and it isn't Starlink internet either. It's artificial intelligence.",
   P("rocket", 450, 900, 0.8), {"cross": [450, 700, 110], "at": 0.3}, P("satellite", 960, 700, 0.6, at=0.35), {"cross": [960, 600, 110], "at": 0.5},
   P("robot", 1450, 900, 1.0, at=0.65))
sc("Earlier this year SpaceX bought xAI, the artificial intelligence company behind the Grok chatbot. That unit is now called Super Intelligence.",
   P("robot", 600, 900, 1.1, text="xAI"), {"arrow": [[800, 600], [1150, 600]], "color": "dark", "at": 0.35}, P("rocket", 1350, 900, 1.0, at=0.45))
sc("Fortune reports AI brought in seven point five six billion dollars this quarter. Starlink and connectivity: five point two five billion. Rockets and space: one point seven seven.",
   {"bars": {"values": [7.56, 5.25, 1.77], "labels": ["AI", "Starlink", "Space"], "colors": ["purple", "teal", "grey"], "fmt": "${}B", "w": 820, "h": 460},
    "x": 960, "y": 860})
sc("Net profit: four point four billion dollars. Spending on equipment, mostly for AI: nineteen point six billion. In three months.",
   C(0, 4.4, 650, 360, fmt="+${:.1f}B", size=150, color="green"), C(0, 19.6, 1300, 360, fmt="-${:.1f}B", size=150, color="red", at=0.45))
sc("Now Tesla. Worth about one and a half trillion dollars. It reported its own results on Wednesday.",
   P("sportscar", 600, 900, 1.2), C(0, 1.5, 1300, 380, fmt="${:.1f}T", size=180, color="money", at=0.35))
sc("Revenue: twenty-eight point zero five billion. Basically flat. Deliveries: four hundred eighty-six thousand cars, down two percent.",
   C(0, 28.05, 650, 360, fmt="${:.2f}B", size=140, color="dark"), C(0, 486532, 1300, 360, fmt="{:,.0f}", size=130, color="red", at=0.45),
   P("car", 1300, 900, 0.7, at=0.6))
sc("And net profit: seven hundred eighty-seven million dollars. That's forty-three percent less than a year earlier.",
   C(0, 787, 700, 360, fmt="${:.0f}M", size=170, color="dark"), C(0, 43, 1350, 360, fmt="-{:.0f}%", size=170, color="red", at=0.4),
   P("arrowdown", 1650, 880, 0.8, at=0.6))
sc("Tesla says battery supply was the limit on how many cars it could make, and that its order backlog is the biggest in four years.",
   P("clipboard", 600, 860, 1.1, text="BACKLOG"), T("4 YEARS", 1300, 380, 140, "teal", at=0.4))
sc("So, side by side: one company growing at rocket speed, one making less profit than last year but promising robots and robotaxis.",
   P("rocket", 550, 900, 1.0, anim="bob"), P("arrowup", 800, 880, 0.7, at=0.2), P("sportscar", 1300, 900, 0.9, at=0.4), P("robot", 1700, 900, 0.7, at=0.6))

# PART 3: WHY MERGE --------------------------------------------------------------
sc("Okay. Why would anyone want to combine them? Supporters give three main reasons.",
   G(960, "present", "neutral", **ANALYST), T("3 REASONS", 960, 280, 130, "dark", at=0.4), chapter="Part 3: Why merge?")
sc("Reason one: they already work together. The two companies run a joint chip-making project called Terafab.",
   P("chip", 960, 880, 1.2, text="TERAFAB"), P("rocket", 500, 900, 0.8, at=0.3), P("car", 1450, 900, 0.8, at=0.4))
sc("SpaceX also has a plan called Starmind, for AI data centers in orbit. And Tesla's cars and robots run on AI too.",
   P("satellite", 700, 650, 0.8, text="STARMIND"), P("robot", 1350, 900, 1.0, at=0.4), P("sun", 1700, 300, 0.6, at=0.2))
sc("The CEO said there's a lot to be gained from cooperating on AI, chips, robotics and connectivity. One company, one plan, fewer meetings.",
   G(600, "point", "grin", **CEO), P("chip", 1200, 880, 0.8, at=0.3), P("robot", 1600, 900, 0.8, at=0.5))
sc("Reason two: money flowing between them. Fortune reports Tesla did over five hundred seventy-three million dollars of business with Musk-controlled companies last year.",
   C(0, 573, 960, 360, fmt="${:.0f}M+", size=170, color="money"), {"arrow": [[600, 700], [1300, 700]], "color": "green", "at": 0.4})
sc("For example, about four hundred thirty million in Tesla Megapack batteries sold to xAI, and a hundred forty-three million in Cybertrucks sold to SpaceX.",
   {"bars": {"values": [430, 143], "labels": ["Batteries", "Cybertrucks"], "colors": ["teal", "grey"], "fmt": "${}M", "w": 640, "h": 440},
    "x": 900, "y": 860}, P("truck", 1600, 900, 0.7, at=0.5))
sc("Tesla's audit committee judged those deals fair, at arm's length. But every deal like that raises the question: is everyone getting a fair price?",
   G(600, "think", "neutral", extras=["glasses", "tie"], shirt="grey", label="audit committee"), P("scale", 1300, 900, 1.1, at=0.4))
sc("One merged company would make those questions disappear, because it would just be paying itself.",
   P("wallet", 700, 860, 1.0), {"arrow": [[850, 600], [1150, 600]], "color": "green", "at": 0.3}, P("wallet", 1300, 860, 1.0, at=0.5))
sc("Reason three: Wall Street seems to expect it. Barclays analyst Dan Levy wrote that a tie-up has increasingly become the consensus expectation.",
   G(600, "present", "neutral", **ANALYST), P("chart", 1300, 900, 1.0, at=0.4))
sc("Analyst Gene Munster went further. He puts the chance of a deal within two years at ninety-five percent.",
   G(500, "pointup", "grin", **ANALYST), C(0, 95, 1250, 380, fmt="{:.0f}%", size=220, color="green", at=0.3))
sc("Dave, meanwhile, rates his car-rocket at ninety-five percent too. Ninety-five percent duct tape.",
   P("car", 700, 900, 1.0), P("rocket", 1000, 900, 0.7, at=0.2), T("95% TAPE", 1450, 380, 120, "red", at=0.45), G(1600, "hips", "smug", extras=DAVE, s=0.8, at=0.6))

# PART 4: WHO DECIDES -----------------------------------------------------------
sc("So who actually decides? This is where it gets interesting. And it's all about votes.",
   P("ballot", 960, 880, 1.3), T("WHO VOTES?", 960, 280, 130, "dark", at=0.4), chapter="Part 4: Who decides?")
sc("At SpaceX, the boss owns a bit under half the company. But his special shares carry ten votes each.",
   {"bars": {"values": [45, 55], "labels": ["His shares", "Everyone else"], "colors": ["dark", "grey"], "fmt": "{}%", "w": 700, "h": 420},
    "x": 900, "y": 860})
sc("Fortune and Barclays put his voting power at SpaceX around eighty-two percent. So SpaceX's side of any vote is, let's say, predictable.",
   C(0, 82, 900, 360, fmt="{:.0f}%", size=220, color="dark"), T("of the votes", 900, 520, 80, "dark", at=0.3), {"stamp": "PREDICTABLE", "x": 1550, "y": 420, "size": 55, "w": 420, "at": 0.6})
sc("Tesla is different. He owns about twenty percent of it. And a merger would need a majority of all Tesla shares. Not just the ones that vote.",
   C(0, 20, 650, 360, fmt="{:.0f}%", size=200, color="dark"), T("needs > 50% of ALL shares", 1250, 360, 70, "red", at=0.4))
sc("He called that, quote, quite a high hurdle. Because shareholders who don't vote count, in effect, as a no.",
   P("ballot", 600, 880, 1.0), T("SILENT = NO", 1250, 380, 120, "red", at=0.4))
sc("This has happened before. In November twenty twenty-five, Tesla shareholders voted on investing in xAI.",
   P("calendar", 600, 860, 1.0, text="NOV 2025"), P("robot", 1300, 900, 0.9, text="xAI", at=0.4))
sc("More shares voted for than against. About one point oh six billion yes, nine hundred sixteen million no.",
   {"bars": {"values": [1060, 916], "labels": ["Yes", "No"], "colors": ["green", "red"], "fmt": "{}M", "w": 620, "h": 440}, "x": 960, "y": 860})
sc("But more than four hundred seventy-three million abstained. Under Tesla's rules, abstentions counted as no. So the measure failed.",
   C(0, 473, 800, 360, fmt="{:.0f}M", size=170, color="grey"), T("= NO", 1400, 360, 140, "red", at=0.45), {"stamp": "FAILED", "x": 1400, "y": 600, "size": 70, "w": 320, "at": 0.65})
sc("Two months later, Tesla put two billion dollars into xAI anyway. Days after that, SpaceX bought xAI.",
   C(0, 2, 700, 360, fmt="${:.0f}B", size=180, color="money"), P("rocket", 1350, 900, 0.9, at=0.45), P("robot", 1650, 900, 0.7, at=0.6))
sc("So how might a deal work? Barclays expects SpaceX to buy Tesla with its own shares. Roughly zero point seven SpaceX shares for each Tesla share, before any premium.",
   P("building", 600, 900, 0.9, text="TESLA"), {"arrow": [[780, 600], [1150, 600]], "color": "dark", "at": 0.3}, T("× 0.7", 1400, 380, 150, "teal", at=0.5))
sc("By Barclays' math, the boss would own about thirty-seven percent of the combined company, with about fifty-six percent of the votes.",
   {"bars": {"values": [37, 56], "labels": ["Owns", "Votes"], "colors": ["grey", "dark"], "fmt": "{}%", "w": 620, "h": 440}, "x": 960, "y": 860})
sc("Barclays sees Tesla's annual meeting as the likely place for a vote. Under SEC rules, Tesla must hold it by December sixth.",
   P("calendar", 960, 860, 1.3, text="DEC 6"), P("ballot", 1550, 880, 0.8, at=0.4))
sc("Dave tries the same idea at home. He announces a family vote on merging the car and the rocket.",
   G(600, "present", "grin", extras=DAVE), P("ballot", 1200, 880, 0.9, at=0.35))
sc("The nephew votes yes. Linda abstains. Under Tesla rules, Dave loses.",
   G(450, "fist", "happy", s=0.6, extras=["cap"]), G(960, "hips", "smug", extras=LINDA, at=0.3), G(1450, "cry", "cry", extras=DAVE, at=0.55))

# PART 5: BOTH SIDES -------------------------------------------------------------
sc("So what do people think? Depending on who you ask, this is either smart housekeeping or a big test of who's in charge.",
   P("scale", 960, 900, 1.4, anim="bob"), chapter="Part 5: What each side says")
sc("Supporters say the companies already share chips, AI and money, so combining them is simply honest bookkeeping.",
   G(600, "point", "happy", **ANALYST), P("clipboard", 1300, 860, 1.0, text="ONE BOOK", at=0.4))
sc("Munster put it plainly on X: Believe me, shareholders would support this.",
   G(600, "pointup", "grin", **ANALYST), P("speech", 1250, 420, 1.0, text="SUPPORT", at=0.35))
sc("Critics focus on control. In May, big public pension funds, including California's CalPERS and the New York City and State comptrollers, wrote a letter about SpaceX.",
   G(600, "hold", "worried", **FUND), P("envelope", 1300, 860, 1.1, text="LETTER", at=0.4))
sc("They said its setup would be the most management-favorable governance ever brought to U.S. markets at this scale.",
   G(600, "point", "worried", **FUND), T("MOST BOSS-FRIENDLY", 1200, 360, 90, "red", at=0.35))
sc("Fortune notes SpaceX skips some usual rules, like needing a majority-independent board, because one person controls most of the votes.",
   P("clipboard", 600, 860, 1.0, text="RULES"), {"cross": [600, 700, 120], "at": 0.35}, C(0, 82, 1300, 380, fmt="{:.0f}% votes", size=110, color="dark", at=0.5))
sc("Their worry: after a merger, Tesla's outside shareholders would have less of a say than they do today.",
   G(600, "shrug", "worried", **INV), P("arrowdown", 1250, 880, 1.0, at=0.4))
sc("Supporters answer that every big decision still goes through independent committees and a shareholder vote. That's exactly what's happening now.",
   G(450, "type", "neutral", **CMTE_T), G(1470, "type", "neutral", look=-1, **CMTE_S), P("ballot", 960, 880, 0.8, at=0.45))
sc("And investors who disagree can vote no, or sell. Which is also how the stock market works.",
   G(700, "shrug", "neutral", **INV), P("pricetag", 1300, 860, 1.0, text="SELL", at=0.4))
sc("We're not picking a side here. We just count the facts.",
   P("scale", 960, 900, 1.3), T("FACTS", 960, 300, 120, "dark", at=0.4), bg="sky")

# PART 6: WHAT IT MEANS FOR YOU ---------------------------------------------------
sc("So does any of this matter if you're not a billionaire? A little, yes.",
   G(960, "think", "confused", extras=DAVE), chapter="Part 6: What it means for you")
sc("Lots of ordinary people own both companies without knowing it, through index funds and pension plans. Tesla is in the S and P five hundred.",
   P("wallet", 600, 860, 1.1, text="401(k)"), P("chart", 1300, 900, 1.0, at=0.4))
sc("So if you have a retirement account, there's a fair chance a small piece of you will be voting on this, through your fund.",
   G(600, "point", "shock", extras=DAVE), P("ballot", 1300, 880, 1.0, at=0.4))
sc("For Tesla drivers, nothing changes tomorrow. Your car still drives. It still does not fly.",
   P("car", 960, 900, 1.3), T("STILL A CAR", 960, 300, 120, "dark", at=0.4))
sc("And there's the AI angle. If AI is now SpaceX's biggest business, a merger would make one giant bet on AI. Bets can win, and they can lose.",
   P("robot", 700, 900, 1.0), P("scale", 1300, 900, 1.0, at=0.4, anim="bob"))
sc("By the way, Tesla's own results call on Wednesday had a rule: no merger questions. The head of investor relations said so right at the start.",
   P("phone", 600, 880, 1.0, text="CALL"), {"stamp": "NO MERGER Qs", "x": 1300, "y": 420, "size": 60, "w": 440, "at": 0.4})
sc("When one came up anyway, the CEO said: I think I said everything that should be said yesterday, tap dancing through a minefield there.",
   G(960, "wave", "worried", **CEO), P("bomb", 500, 900, 0.6, at=0.3), P("bomb", 1450, 900, 0.6, at=0.45))
sc("Tesla's stock slipped about two percent after hours on Wednesday, to about three hundred seventy-eight dollars.",
   C(386.47, 377.88, 960, 360, fmt="${:.2f}", size=170, color="red", dur=1.8), P("arrowdown", 1600, 880, 0.9, at=0.5))

# PART 7: WHAT'S NEXT -------------------------------------------------------------
sc("So what's next? Three things to watch.",
   P("calendar", 960, 860, 1.2, text="NEXT"), chapter="Part 7: What's next")
sc("One: whether the two committees agree on a price. Right now there is no deal on the table.",
   G(450, "think", "neutral", **CMTE_T), G(1470, "think", "neutral", look=-1, **CMTE_S), T("PRICE?", 960, 340, 120, "red", at=0.4))
sc("Two: Tesla's annual meeting, due by December sixth. Barclays thinks that's the likely stage for a vote.",
   P("calendar", 700, 860, 1.1, text="DEC 6"), P("ballot", 1300, 880, 1.0, at=0.4))
sc("Three: whether enough Tesla shareholders actually show up and say yes. Remember, silence counts as no.",
   P("ballot", 600, 880, 1.0), T("SHOW UP", 1250, 380, 130, "teal", at=0.4))
sc("Quick recap. SpaceX and Tesla have formed committees to look at merging into a company worth around three and a half trillion dollars.",
   P("rocket", 650, 900, 0.9), T("+", 960, 600, 140, "dark", at=0.3), P("sportscar", 1300, 900, 0.9, at=0.4))
sc("Supporters say they already share chips, AI and money. Critics say one person would control too much of the vote.",
   P("scale", 960, 900, 1.3, anim="bob"))
sc("And nothing happens unless a majority of all Tesla shares say yes.",
   P("ballot", 960, 880, 1.3), C(0, 50, 1500, 380, fmt=">{:.0f}%", size=150, color="red", at=0.4))
sc("Back at Dave's house, the car-rocket is finished. He turns the key. Nothing happens. Then the rocket engine rolls off and lands in the flower bed.",
   P("car", 700, 900, 1.1), P("rocket", 1100, 900, 0.7, at=0.3, move=[1400, 900]), G(1600, "facepalm", "tired", extras=DAVE, s=0.8, at=0.6))
sc("Linda says some mergers need a special committee. Dave says he'll form one. It's just him, in two different chairs.",
   G(500, "hips", "smug", extras=LINDA), G(1150, "type", "neutral", extras=DAVE, at=0.35), G(1550, "type", "neutral", look=-1, extras=DAVE, at=0.5))
sc("Your turn: should one person run two giant companies at once, or should they just become one? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("ballot", 1250, 880, 1.2, text="?", at=0.3))
sc("And if calm stick figures explaining loud news is your kind of thing, subscribe. No duct tape required.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep011",
    "title": "Why Would Tesla and SpaceX Become One Company?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On October 20, 2026, Elon Musk said on SpaceX's earnings call that SpaceX and Tesla have each formed special committees of independent "
        "directors to discuss a possible merger. Together they are worth roughly $3.5 trillion at current market values. No terms have been agreed. "
        "We go through what was said, SpaceX's Q3 numbers (AI is now its biggest business), Tesla's Q3 results, why supporters like the idea, "
        "why pension funds and critics worry about control, how a Tesla shareholder vote would work, and what happens next. Stick figures, facts only.\n\n"
        "Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported. Not financial advice.\n\n"
        "Sources:\n"
        "TechCrunch, SpaceX and Tesla boards form special committees to review merger (Oct 20, 2026): https://techcrunch.com/2026/10/20/spacex-and-tesla-boards-form-special-committees-to-review-merger/\n"
        "Axios, SpaceX, Tesla explore merger, Elon Musk confirms (Oct 20, 2026): https://www.axios.com/2026/10/20/spacex-tesla-merger-talks\n"
        "Fortune, SpaceX posts first operating profit as public company as AI revenue nearly triples (Oct 20, 2026): https://fortune.com/2026/10/20/spacex-q3-profit-ai-si-elon-musk/\n"
        "Fortune, Musk's $3.5 trillion Tesla-SpaceX merger talks put his accountability to the test (Oct 21, 2026): https://fortune.com/2026/10/21/elon-musk-trillionaire-spacex-tesla-merger-corporate-accountability/\n"
        "Yahoo Finance, Musk backs SpaceX-Tesla merger idea as both boards form special committees: https://finance.yahoo.com/markets/stocks/article/musk-backs-spacex-tesla-merger-idea-as-both-boards-form-special-committees-113219080.html\n"
        "Electrek, Tesla Q3 2026 financial results (Oct 21, 2026): https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/\n"
        "Investing.com, Tesla Q3 2026 earnings call transcript: https://www.investing.com/news/transcripts/earnings-call-transcript-tesla-beats-q3-2026-estimates-as-stock-slips-after-hours-93CH-4964365\n\n"
        "#tesla #spacex #merger #explained #stickfigure #news"
    ),
    "tags": ["tesla spacex merger", "spacex", "tesla", "elon musk", "tesla earnings", "spacex earnings", "merger explained",
             "stock market news", "business news explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "ROCKET|+ CAR?", "size": 210, "color": "black",
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep011.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

"""Episode 18: FTC + 20 states sue Dollar General over shelf-vs-register overcharges (filed Oct 26, 2026). Explained with stick figures."""
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


FTC = dict(extras=["tie", "briefcase"], shirt="grey", label="FTC")
STATES = dict(extras=["tie"], shirt="purple", label="20 states")
DG = dict(extras=["tie"], shirt="gold", label="the chain")
INSP = dict(extras=["cap", "glasses"], shirt="teal", label="inspector")
CLERK = dict(extras=["cap"], shirt="gold", label="store worker")
JUDGE = dict(extras=["glasses"], shirt="dark", label="federal court")


def TAG(x, y, price, at=0, color="white", s=1.0):
    """Shelf price tag: white label with a price."""
    w, h = int(300 * s), int(150 * s)
    return [{"box": [x - w // 2, y - h // 2, w, h], "color": color, "at": at},
            {"text": "SHELF", "x": x, "y": y - int(40 * s), "size": int(36 * s), "color": "grey", "at": at},
            {"text": price, "x": x, "y": y + int(22 * s), "size": int(80 * s), "color": "dark", "at": at}]


def REG(x, price, at=0, color="red"):
    """Checkout register: counter + screen with the rung-up price."""
    return [{"box": [x - 230, 700, 460, 200], "color": "brown", "at": at},
            {"box": [x - 120, 470, 240, 230], "color": "dark", "at": at},
            {"box": [x - 100, 490, 200, 120], "color": "white", "at": at},
            {"text": price, "x": x, "y": 550, "size": 70, "color": color, "at": at},
            {"text": "REGISTER", "x": x, "y": 800, "size": 40, "color": "white", "at": at}]


def RECEIPT(x, y, lines, at=0, w=420):
    h = 90 + 64 * len(lines)
    out = [{"box": [x - w // 2, y, w, h], "color": "white", "at": at},
           {"text": "RECEIPT", "x": x, "y": y + 45, "size": 40, "color": "grey", "at": at}]
    for i, (ln, col) in enumerate(lines):
        out.append({"text": ln, "x": x, "y": y + 110 + i * 64, "size": 44, "color": col,
                    "at": (at + 0.1 * (i + 1)) if at < 1 else at})
    return out


def STORE(x, s=1.0, at=0):
    return [P("building", x, 900, s, at=at), {"text": "DOLLAR STORE", "x": x, "y": 900 - int(330 * s), "size": int(46 * s), "color": "gold", "outline": "dark", "at": at}]


# COLD OPEN --------------------------------------------------------------------
sc("A shopper picks up a box of snack cakes. The shelf tag says two dollars fifty.",
   G(480, "hold", "happy", extras=LINDA), *TAG(1250, 450, "$2.50", at=0.3), cam={"from": [1250, 450, 1.4], "to": [960, 540, 1.0]}, bg="yellow")
sc("At the register, it rings up three dollars fifty.",
   G(480, "stand", "shock", extras=LINDA), *REG(1250, "$3.50", at=0.15), {"arrow": [[700, 400], [1050, 520]], "color": "red", "at": 0.5}, bg="yellow")
sc("We didn't invent that. A shopper reported it, and it's quoted in a new federal lawsuit against America's biggest dollar-store chain.",
   P("clipboard", 600, 860, 1.2, text="LAWSUIT"), *RECEIPT(1300, 260, [("cakes  $3.50", "red"), ("shelf  $2.50", "dark")], at=0.3))
sc("On Monday, the Federal Trade Commission and twenty states sued Dollar General. They say this kept happening for years, in thousands of stores.",
   G(420, "point", "angry", **FTC), G(760, "point", "angry", **STATES, at=0.15), *STORE(1450, 1.0, at=0.35), C(0, 20, 760, 250, fmt="{:.0f} states", size=110, color="purple", at=0.4))
S.append({"say": "So here's the mystery. How does a price change in the few steps between the shelf and the register? And who keeps the difference?",
          "items": [*TAG(450, 450, "$2.50"), {"arrow": [[680, 450], [1150, 450]], "color": "red", "at": 0.25}, T("?", 960, 330, 200, "red", at=0.4),
                    *REG(1450, "$3.50", at=0.3)],
          "chapter": "Today's question"})
sc("Let's go through what the lawsuit claims, the numbers, how a price goes wrong, what the company says, and what you can do at checkout.",
   P("clipboard", 500, 860, 1.1, text="1 2 3"), P("magnifier", 1000, 700, 1.0, at=0.3), G(1500, "present", "neutral", extras=ECON, look=-1, at=0.5))

# PART 1: THE GIANT -----------------------------------------------------------
sc("First, the giant. According to the FTC, Dollar General runs more than twenty-one thousand stores.",
   *STORE(500, 0.8), C(0, 21000, 1200, 400, fmt="{:,.0f}+", size=200, color="gold", at=0.3), chapter="Part 1: The giant and its shoppers")
sc("The lawsuit says about eighty percent of them are in towns of twenty thousand people or fewer.",
   C(0, 80, 700, 420, fmt="{:.0f}%", size=230, color="red"), P("house", 1350, 900, 0.7, at=0.3), P("house", 1650, 900, 0.6, at=0.45), T("small towns", 1500, 330, 70, "dark", at=0.55))
sc("And roughly three in four Americans live within five miles of one.",
   P("globe", 600, 760, 1.0), T("3 in 4", 1250, 380, 170, "navy", at=0.3), T("within 5 miles", 1250, 580, 70, "dark", at=0.55))
sc("It's built to be the store down the road. Not a giant supermarket out by the highway. The little yellow one next to the gas station.",
   *STORE(650, 0.8), P("gaspump", 1100, 900, 1.0, at=0.3), P("car", 1550, 900, 0.9, at=0.5, anim="bob"), bg="sky")
sc("Who shops there? The lawsuit says households earning thirty-five thousand dollars a year or less make up sixty percent of the company's revenue.",
   P("wallet", 550, 800, 1.2), T("under $35,000/yr", 550, 450, 64, "dark", at=0.25), C(0, 60, 1350, 430, fmt="{:.0f}%", size=230, color="red", at=0.45))
sc("The chain sells around two thousand items for a dollar or less.",
   P("dollar", 600, 700, 1.3), C(0, 2000, 1300, 420, fmt="{:,.0f}", size=200, color="money", at=0.3), T("items at $1 or less", 1300, 600, 60, "dark", at=0.55))
sc("The complaint quotes the company's own chief executive describing core customers as people who run out of money before the month runs out.",
   G(500, "present", "neutral", extras=["tie"], shirt="gold", label="the CEO"), P("calendar", 1150, 860, 1.0, text="DAY 24"), P("wallet", 1550, 820, 0.9, at=0.5, text="$0"))
sc("So a price that's wrong by fifty cents isn't a rounding error. For a lot of these shoppers, it's part of tomorrow's bread.",
   T("+ 50¢", 600, 420, 180, "red"), {"arrow": [[850, 450], [1150, 600]], "color": "red", "at": 0.35}, P("bread", 1400, 800, 1.3, at=0.45))

# PART 2: THE UNDERCOVER SHOPPING TRIP ---------------------------------------
sc("How did the government check? It went shopping. Between January and April this year, FTC investigators made undercover purchases.",
   G(600, "hold", "neutral", extras=["cap", "glasses"], shirt="grey", label="FTC shopper"), P("cart", 1150, 900, 1.1, at=0.3), P("eye", 1550, 420, 0.8, at=0.55), chapter="Part 2: The undercover shopping trip")
sc("Four stores, in Ohio, Missouri, Pennsylvania and Maryland. About sixty items each time. Paid by card. Kept every receipt.",
   T("OHIO", 450, 300, 70, "navy"), T("MISSOURI", 1450, 300, 70, "navy", at=0.15), T("PENNSYLVANIA", 520, 520, 64, "navy", at=0.3), T("MARYLAND", 1450, 520, 70, "navy", at=0.45),
   C(0, 60, 960, 760, fmt="~{:.0f} items", size=100, color="dark", at=0.6))
sc("The result, according to the lawsuit: every single trip ended with an overcharge. Every one.",
   {"stamp": "4 OUT OF 4", "x": 960, "y": 450, "size": 110, "w": 640}, G(1650, "facepalm", "tired", look=-1, extras=DAVE, at=0.5))
sc("Cleveland, Ohio: thirteen out of fifty-eight items rang up with a different price than the label. That's an error rate of twenty-two point four percent.",
   T("13 / 58", 600, 380, 150, "dark"), C(0, 22.4, 1350, 420, fmt="{:.1f}%", size=210, color="red", at=0.4))
sc("To be fair, some errors went the other way. Five items were cheaper at the register. Eight were more expensive.",
   {"bars": {"values": [5, 8], "labels": ["cheaper", "pricier"], "colors": ["green", "red"], "fmt": "{}", "w": 700, "h": 420}, "x": 900, "y": 830}, G(1650, "shrug", "neutral", look=-1, extras=ECON, at=0.5))
sc("Net result for that one basket: three dollars and twenty-five cents extra.",
   P("cart", 600, 900, 1.2), C(0, 3.25, 1300, 430, fmt="+${:.2f}", size=220, color="red", at=0.3))
sc("Springfield, Missouri: four dollars and seven cents extra. Sharpsburg, Pennsylvania: two dollars sixty.",
   *RECEIPT(600, 250, [("Springfield", "dark"), ("+$4.07", "red")]), *RECEIPT(1300, 250, [("Sharpsburg", "dark"), ("+$2.60", "red")], at=0.45))
sc("Baltimore: three dollars sixty-five. Five errors, and not one of them in the shopper's favour.",
   *RECEIPT(700, 250, [("Baltimore", "dark"), ("+$3.65", "red"), ("errors for you: 0", "grey")]), G(1450, "cry", "sad", look=-1, extras=["cap", "glasses"], shirt="grey", at=0.5))
sc("Three or four dollars doesn't sound like much. Now picture it across a lot of baskets, every week.",
   P("cart", 450, 900, 0.7), P("cart", 750, 900, 0.7, at=0.15), P("cart", 1050, 900, 0.7, at=0.3), P("cart", 1350, 900, 0.7, at=0.45), P("cart", 1650, 900, 0.7, at=0.6),
   T("x every week", 1050, 350, 100, "red", at=0.7))
sc("Dave now takes a calculator to buy toothpaste. The cashier calls him The Auditor. He has decided to take it as a compliment.",
   G(650, "type", "smug", extras=DAVE), T("THE AUDITOR", 1350, 380, 100, "navy", at=0.35), G(1500, "stand", "tired", look=-1, **CLERK, at=0.5), bg="yellow")

# PART 3: THE COMPLAINT WALL -------------------------------------------------
sc("The lawsuit also lists shoppers' complaints. In Ohio, milk marked three ninety-five rang up at four twenty-five.",
   *TAG(600, 450, "$3.95"), {"arrow": [[800, 450], [1100, 450]], "color": "red", "at": 0.35}, *REG(1400, "$4.25", at=0.4), chapter="Part 3: The complaint wall")
sc("In Massachusetts, trail mix advertised at two seventy-five scanned at five dollars. The shopper said the wrong sign was still up the next week.",
   *TAG(600, 450, "$2.75"), *REG(1400, "$5.00", at=0.35), P("calendar", 960, 860, 0.8, text="+1 WEEK", at=0.65))
sc("In Alabama, a promotion said three six-packs of soda for eight dollars. The shopper said the deal never applied. She noticed at home.",
   T("3 for $8", 600, 380, 140, "green"), P("house", 1350, 900, 0.9, at=0.4), G(1650, "facepalm", "sad", look=-1, extras=LINDA, at=0.55))
sc("In Michigan, buy one, get one. The shopper said she was charged full price for both. Also noticed at home.",
   T("BUY 1 GET 1", 600, 380, 110, "green"), *RECEIPT(1350, 280, [("item 1  FULL", "red"), ("item 2  FULL", "red")], at=0.4))
sc("Notice the pattern? A lot of these people find out in the kitchen, not at the counter.",
   P("house", 600, 900, 1.2), P("magnifier", 1150, 650, 1.1, at=0.3), *RECEIPT(1500, 300, [("???", "red")], at=0.5))
sc("The lawsuit says that from January twenty twenty-three to March this year, the company logged twenty-nine thousand two hundred sixty-five complaints in a category called Did Not Honor Marked Price.",
   C(0, 29265, 960, 380, fmt="{:,.0f}", size=220, color="red"), T("'Did Not Honor Marked Price'", 960, 620, 66, "dark", at=0.5))
sc("Those complaints came from all forty-eight states where it has stores.",
   P("globe", 700, 760, 1.0), C(0, 48, 1300, 420, fmt="{:.0f} / 48", size=200, color="navy", at=0.3))

# PART 4: THE INSPECTORS -----------------------------------------------------
sc("It's not just the FTC. States send their own inspectors with scanners, and most use one simple rule.",
   G(600, "hold", "neutral", **INSP), P("phone", 900, 650, 0.8, at=0.25), *TAG(1450, 450, "$?.??", at=0.45), chapter="Part 4: The inspectors")
sc("Thirty-three states follow a procedure from NIST, the National Institute of Standards and Technology. If more than two percent of the items checked are wrong, the store fails.",
   C(0, 2, 700, 420, fmt="{:.0f}%", size=260, color="red"), {"stamp": "FAIL", "x": 1400, "y": 420, "size": 110, "w": 340, "at": 0.6})
sc("In a check of fifty items, that means one mistake can slide. Two, and you fail.",
   T("50 items", 600, 330, 100, "dark"), T("1 wrong = pass", 1300, 330, 70, "green", at=0.3), T("2 wrong = FAIL", 1300, 520, 80, "red", at=0.55))
sc("Kentucky inspected Dollar General stores two hundred forty-two times in twenty twenty-three. They failed almost twenty-four percent.",
   T("KENTUCKY", 600, 300, 90, "navy"), T("242 checks", 600, 480, 80, "dark", at=0.2), C(0, 23.97, 1350, 420, fmt="{:.2f}%", size=200, color="red", at=0.4))
sc("At one store in Glasgow, Kentucky, twenty of fifty products were priced wrong. Forty percent.",
   *STORE(600, 0.8), C(0, 40, 1350, 420, fmt="{:.0f}%", size=240, color="red", at=0.35), T("20 of 50", 1350, 620, 80, "dark", at=0.55))
sc("Kansas, from twenty twenty-three to this March: more than thirty-nine percent of inspections failed. One store failed forty-four of them.",
   T("KANSAS", 600, 300, 90, "navy"), C(0, 39, 600, 520, fmt="{:.0f}%+", size=160, color="red", at=0.2), C(0, 44, 1350, 420, fmt="{:.0f} fails", size=170, color="red", at=0.5))
sc("Forty-four. At that point the inspector probably knows the staff's birthdays.",
   G(600, "wave", "tired", **INSP), P("calendar", 1100, 860, 0.9, text="VISIT 44", at=0.3), G(1550, "wave", "grin", look=-1, **CLERK, at=0.45), bg="yellow")
sc("New Mexico, January to April this year: fifty-three percent failed. In Nephi, Utah, one store failed fifteen of nineteen checks, including ten in a row.",
   T("NEW MEXICO 53%", 960, 300, 100, "red"), T("NEPHI, UTAH", 700, 520, 70, "navy", at=0.4), T("10 in a row", 1350, 520, 80, "red", at=0.6))
sc("Here's a sample of the failure rates the lawsuit lists.",
   {"bars": {"values": [10, 20.1, 23.97, 39, 45, 53], "labels": ["TN", "AR", "KY", "KS", "UT", "NM"], "colors": ["grey", "orange", "orange", "red", "red", "red"], "fmt": "{}%", "w": 1100, "h": 460}, "x": 960, "y": 860})
sc("Wisconsin scanned seven thousand three hundred forty-four products in twenty twenty-three. Six hundred sixty-two rang up too high, on average seventeen percent above the label.",
   C(0, 7344, 600, 380, fmt="{:,.0f}", size=150, color="dark"), C(0, 662, 1350, 380, fmt="{:,.0f} too high", size=110, color="red", at=0.35), T("avg +17%", 1350, 600, 110, "red", at=0.65))
sc("Louisiana stores failed one hundred forty-four audits and paid one hundred seventy-six thousand eight hundred fifty dollars in fines.",
   T("LOUISIANA", 600, 320, 90, "navy"), C(0, 144, 600, 520, fmt="{:.0f} fails", size=120, color="red", at=0.2), C(0, 176850, 1350, 430, fmt="${:,.0f}", size=150, color="money", at=0.5))
sc("And the lawsuit says that since twenty nineteen the company has settled seven earlier cases with six states, paying more than six million dollars.",
   P("moneybag", 600, 880, 1.3, text="$6M+"), T("7 settlements", 1350, 350, 100, "dark", at=0.3), T("6 states", 1350, 520, 100, "navy", at=0.5))
sc("Vermont, one point seven five million. New Jersey, one point two million. Ohio, one million. So the problem isn't new. The question is why it keeps coming back.",
   {"bars": {"values": [1.75, 1.2, 1.0], "labels": ["VT", "NJ", "OH"], "colors": ["navy", "navy", "navy"], "fmt": "${}M", "w": 800, "h": 420}, "x": 850, "y": 830},
   T("again?", 1600, 330, 100, "red", at=0.6))
sc("Quick one. If turning a ninety-five page lawsuit into ten minutes of stick figures saves you time, subscribe. That's the whole job here.",
   G(600, "present", "happy", extras=DAVE), P("clipboard", 1100, 860, 1.0, text="95 pages", at=0.25), P("tv", 1550, 800, 0.7, text="SUBSCRIBE", at=0.5), bg="yellow")

# PART 5: HOW A PRICE GOES WRONG ---------------------------------------------
sc("So how does a price actually go wrong? The lawsuit describes the weekly routine inside a store.",
   *STORE(960, 1.0), P("magnifier", 1500, 650, 1.0, at=0.4), chapter="Part 5: How a price goes wrong")
sc("Dollar General usually changes prices every week. Headquarters sends the new prices into the register system.",
   P("building", 500, 900, 1.0), {"arrow": [[700, 500], [1150, 500]], "color": "red", "at": 0.3}, *REG(1450, "NEW", at=0.45))
sc("It also sends stores sheets of peel-and-stick labels, sorted by aisle.",
   P("envelope", 600, 700, 1.2), {"box": [1100, 350, 500, 380], "color": "white", "at": 0.3}, T("$1.25  $2.00  $3.50", 1350, 450, 50, "dark", at=0.4), T("$0.95  $4.75  $1.50", 1350, 560, 50, "dark", at=0.5))
sc("Each store is supposed to schedule a five-hour shift called Compliance Tuesday. Someone walks every aisle, sticking on the new tags.",
   P("calendar", 500, 860, 1.0, text="TUE"), C(0, 5, 960, 380, fmt="{:.0f} hours", size=150, color="navy", at=0.3), G(1500, "hold", "tired", look=-1, **CLERK, at=0.5))
sc("Here's the catch. Once the new price is in the system, the register charges it, whether or not the shelf tag has been changed.",
   *TAG(500, 450, "$2.50"), *REG(1400, "$3.50", at=0.3), {"cross": [500, 450, 160], "at": 0.6})
sc("The lawsuit says most of these changes are increases. So when a tag is late, the shelf shows the old, lower price. The register charges the new one.",
   P("arrowup", 600, 800, 1.3), *TAG(1050, 450, "OLD $2.50", s=0.9, at=0.3), *REG(1550, "NEW $3.50", at=0.5))
sc("In other words, the register lives in the future, and the shelf lives in last week.",
   P("rocket", 550, 800, 0.9), P("calendar", 1350, 860, 1.0, text="LAST WEEK", at=0.35), bg="purple")
sc("Why would tags be late? The complaint cites a Guardian report: a former Louisiana employee said she sometimes threw away new tags to keep herself or colleagues out of trouble.",
   G(600, "shrug", "worried", **CLERK), P("envelope", 1100, 800, 0.9, at=0.3), {"arrow": [[1250, 700], [1500, 850]], "color": "red", "at": 0.5}, {"box": [1450, 760, 160, 140], "color": "grey", "at": 0.55}, T("bin", 1530, 830, 50, "white", at=0.6))
sc("Then there's the checkout itself. The lawsuit says in one undercover trip, the main screen faced the employee. The shopper could only see a small display.",
   *REG(800, "$?", at=0), G(1350, "stand", "confused", look=-1, extras=["cap", "glasses"], shirt="grey", at=0.3), P("eye", 1350, 330, 0.7, at=0.55))
sc("Prices flash by fast. You're holding a bag, a kid, and your keys. Who reads every line?",
   G(700, "panic", "worried", extras=LINDA), P("backpack", 1100, 750, 0.8, at=0.25), T("$1.25 $3.50 $2.00 $0.95", 1350, 350, 60, "red", at=0.4, anim="shake"))
sc("One Nebraska shopper complained it happened at two different stores in one week.",
   *STORE(500, 0.7), *STORE(1000, 0.7, at=0.25), P("calendar", 1550, 860, 0.9, text="1 WEEK", at=0.5))
sc("And a Florida shopper said staff told him they weren't allowed to override the register price.",
   G(600, "point", "angry", extras=["hair"], shirt="orange"), G(1350, "shrug", "worried", look=-1, **CLERK, at=0.3), {"stamp": "NO OVERRIDE", "x": 960, "y": 300, "size": 70, "w": 480, "at": 0.55})

# PART 6: WHAT EACH SIDE SAYS ------------------------------------------------
sc("Now both sides. Christopher Mufarrige, who heads the FTC's Bureau of Consumer Protection, said Dollar General has betrayed the trust of millions of American consumers.",
   G(600, "point", "angry", extras=["tie", "briefcase"], shirt="grey", label="FTC consumer chief"), P("speech", 1300, 420, 1.4, text="betrayed the trust", at=0.35), chapter="Part 6: What each side says")
sc("Nebraska's attorney general, Mike Hilgers, said Nebraskans expect to be charged the prices that are advertised.",
   G(600, "present", "neutral", extras=["tie"], shirt="navy", label="Nebraska AG"), *TAG(1350, 450, "= PRICE PAID", at=0.4))
sc("The twenty states are a mix: Alabama and Oklahoma, California and New Jersey, Ohio and Wisconsin. This one isn't red versus blue.",
   T("AL  OK  CA  NJ", 960, 330, 110, "purple"), T("OH  WI  FL  IL ...", 960, 520, 100, "purple", at=0.3), T("red + blue", 960, 720, 80, "dark", at=0.6))
sc("Dollar General disputes the claims. In a statement reported by Fortune, it said its goal is one hundred percent accuracy between shelf and register prices in every store.",
   G(600, "present", "neutral", **DG), C(0, 100, 1350, 420, fmt="{:.0f}%", size=230, color="green", at=0.35), T("goal", 1350, 620, 80, "dark", at=0.55))
sc("It said occasional price discrepancies can happen, and that when they do, store employees are expected to make it right for the customer.",
   G(600, "shrug", "neutral", **DG), G(1350, "wave", "happy", look=-1, **CLERK, at=0.35), P("dollar", 1000, 650, 0.8, at=0.55))
sc("The company also said it cooperated with the investigation, discussed possible fixes with regulators before the suit was filed, and will defend itself while staying open to a resolution.",
   G(500, "hips", "neutral", **DG), P("desk", 1050, 900, 1.0, at=0.25), G(1550, "stand", "neutral", look=-1, **FTC, at=0.45))
sc("And remember: these are allegations. Nothing has been proven in court yet.",
   P("scale", 960, 880, 1.4), {"stamp": "NOT PROVEN YET", "x": 960, "y": 280, "size": 70, "w": 560, "at": 0.4})
sc("Also fair to say: on the FTC's own test trips, some items were cheaper at the register. Errors run both ways. The lawsuit says most run one way.",
   {"arrow": [[600, 500], [300, 500]], "color": "green"}, {"arrow": [[1300, 500], [1700, 500]], "color": "red", "at": 0.2}, T("cheaper", 450, 400, 60, "green", at=0.1), T("pricier", 1500, 400, 70, "red", at=0.3),
   G(960, "shrug", "neutral", extras=ECON, at=0.5))
sc("One more unusual detail. The lawsuit also uses a nineteen ninety-nine banking privacy law, the Gramm-Leach-Bliley Act.",
   P("lock", 600, 750, 1.2), T("1999", 1300, 350, 160, "navy", at=0.3), T("Gramm-Leach-Bliley", 1300, 560, 70, "dark", at=0.5))
sc("The argument: if you show a false price and then take someone's card or check details to pay it, that's getting their financial information under false pretences.",
   *TAG(500, 450, "$2.50"), P("wallet", 1050, 800, 1.0, at=0.3), {"arrow": [[1200, 700], [1450, 600]], "color": "red", "at": 0.5}, *REG(1600, "$3.50", at=0.5))

# PART 7: WHAT HAPPENS NEXT ---------------------------------------------------
sc("So what happens next? The case was filed in federal court in Tennessee, the company's home state.",
   G(960, "stand", "neutral", **JUDGE), P("scale", 1500, 880, 1.0, at=0.3), T("TENNESSEE", 500, 330, 90, "navy", at=0.45), chapter="Part 7: What happens next")
sc("The FTC and the states want a court order to stop the practice, money back for shoppers, and penalties under state laws.",
   {"stamp": "STOP", "x": 450, "y": 400, "size": 90, "w": 300}, P("moneybag", 960, 880, 1.0, at=0.3, text="REFUNDS"), P("scale", 1500, 880, 1.0, at=0.55))
sc("How much money? The lawsuit says millions of dollars, but some of its numbers are blacked out in the public version.",
   {"box": [500, 300, 900, 60], "color": "dark"}, {"box": [500, 420, 700, 60], "color": "dark", "at": 0.2}, {"box": [500, 540, 820, 60], "color": "dark", "at": 0.35}, T("$ millions", 1550, 450, 90, "red", at=0.55))
sc("Cases like this often end in a settlement. That could take months, or longer.",
   P("calendar", 600, 860, 1.0, text="2027?"), P("stopwatch", 1150, 700, 1.0, at=0.3), T("?", 1550, 400, 200, "red", at=0.55))
sc("Meanwhile, the boring superpower: check your receipt before you leave the store.",
   G(600, "hold", "smug", extras=LINDA), *RECEIPT(1300, 260, [("cakes  $3.50", "red"), ("shelf  $2.50", "green")], at=0.3), bg="sky")
sc("Snap a quick photo of the shelf tag or sale sign. If the register disagrees, you've got proof.",
   P("phone", 600, 700, 1.2), *TAG(1250, 450, "$2.50", at=0.3), {"ring": [1250, 450, 200], "at": 0.6})
sc("And in some states, Wisconsin for example, the law says the store has to refund the difference.",
   T("WISCONSIN", 650, 330, 90, "navy"), P("dollar", 1300, 700, 1.0, at=0.3), T("refund the difference", 1300, 400, 64, "green", at=0.5))
sc("Linda has done this for years. She calls it reading the sequel to the shelf.",
   G(700, "hips", "smug", extras=LINDA), *RECEIPT(1350, 250, [("THE SEQUEL", "navy")], at=0.4), bg="yellow")

# RECAP ------------------------------------------------------------------------
sc("Quick recap. The FTC and twenty states say Dollar General charged more at the register than on the shelf, for years, in thousands of stores.",
   G(450, "point", "neutral", s=0.8, **FTC), G(800, "point", "neutral", s=0.8, **STATES, at=0.15), *TAG(1250, 450, "$2.50", s=0.8, at=0.3), *REG(1620, "$3.50", at=0.45), chapter="Recap")
sc("Inspectors in state after state found failure rates from about ten percent to over fifty. The company says it aims for one hundred percent accuracy and will defend itself.",
   {"bars": {"values": [10, 53], "labels": ["low", "high"], "colors": ["orange", "red"], "fmt": "{}%", "w": 600, "h": 400}, "x": 700, "y": 830}, G(1500, "present", "neutral", look=-1, **DG, at=0.45))
sc("Now it's up to a federal court in Tennessee. We just count the facts.",
   G(800, "stand", "neutral", **JUDGE), P("scale", 1350, 880, 1.1, at=0.3))
sc("As for Dave, he's at the register with a calculator, a clipboard, a photo of the shelf, and eleven people waiting behind him.",
   G(450, "type", "smug", extras=DAVE), P("clipboard", 750, 860, 0.8, at=0.15), P("phone", 950, 650, 0.6, at=0.25),
   *[G(1150 + i * 110, "stand", "tired", look=-1, s=0.7, extras=["hair"] if i % 2 else ["cap"], at=0.35 + 0.04 * i) for i in range(6)], bg="yellow")
sc("Your turn. Have you ever caught a price that changed between the shelf and the register? What was it? Tell us in the comments.",
   G(600, "think", "neutral", extras=LINDA), P("speech", 1300, 450, 1.4, text="YOUR STORY?", at=0.35), bg="yellow")
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, at=0.4, text="SUBSCRIBE"), bg="yellow")


script = {
    "id": "ep018",
    "title": "20 States vs. Dollar General: Who Pays the Extra Dollar?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "The shelf says $2.50. The register says $3.50. On Oct 26, 2026, the Federal Trade Commission and 20 states sued Dollar General, "
        "alleging the chain routinely charged shoppers more at the register than the prices on its shelves, tags and ads. "
        "We walk through the FTC's undercover shopping trips (every one ended in an overcharge), state inspection failure rates "
        "(Kentucky 23.97%, Kansas 39%+, New Mexico 53%), the 29,265 'Did Not Honor Marked Price' complaints, how weekly price changes "
        "and late shelf tags create the gap, what Dollar General says in response, and what you can do at checkout. "
        "These are allegations; nothing has been proven in court.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "FTC press release, FTC and State Partners Sue Dollar General (Oct 26, 2026): https://www.ftc.gov/news-events/news/press-releases/2026/10/ftc-state-partners-sue-dollar-general-charging-consumers-more-advertised-many-products\n"
        "FTC complaint, FTC et al. v. Dollar General Corp., M.D. Tenn. (Oct 26, 2026): https://www.ftc.gov/system/files/ftc_gov/pdf/DollarGeneral-Complaint.pdf\n"
        "CBS News, Dollar General overcharged millions at checkout for years, FTC and 20 states allege (Oct 26, 2026): https://www.cbsnews.com/news/dollar-general-sued-ftc-overcharging-prices\n"
        "Fortune, FTC and 20 states sue Dollar General (Oct 28, 2026): https://fortune.com/2026/10/28/dollar-general-ftc-lawsuit-overcharging-shelf-prices\n"
        "ConsumerAffairs, FTC and 20 states sue Dollar General over alleged overcharges (Oct 27, 2026): https://www.consumeraffairs.com/news/ftc-and-20-states-sue-dollar-general-over-alleged-overcharges-102726.html\n\n"
        "#dollargeneral #ftc #prices #shopping #explained #stickfigure #news"
    ),
    "tags": ["dollar general", "dollar general lawsuit", "ftc lawsuit", "dollar general overcharging", "shelf price register price",
             "price accuracy", "consumer protection", "check your receipt", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "SHELF $2.50|PAID $3.50", "size": 150, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["bun"]}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "arrowup", "x": 1130, "y": 780, "s": 2.2, "color": "red"}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep018.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

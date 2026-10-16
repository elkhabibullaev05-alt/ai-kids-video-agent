"""Episode 1: September 2026 US inflation report, explained with stick figures."""
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


# COLD OPEN --------------------------------------------------------------------
sc("Meet Dave. Dave just put gas in his car, and Dave is not okay.",
   P("gaspump", 1250, s=1.2), P("car", 1620, s=0.9), G(800, "panic", "scream", extras=DAVE, anim="shake", at=0.35),
   T("$4.33", 1250, 330, 130, "red", at=0.45), cam={"from": [960, 540, 1.12], "to": [1050, 560, 1.0]})
sc("A few months ago the same gallon cost two dollars and ninety eight cents.",
   {"count": [2.98, 4.33], "fmt": "${:.2f}", "x": 960, "y": 330, "size": 180, "color": "red", "at": 0.25, "dur": 2.4},
   G(560, "facepalm", "tired", extras=DAVE), P("wallet", 1400, 760, 1.3, text=":(", anim="shake", at=0.5))
sc("And it's not just gas. Groceries, plane tickets, the guy who fixes your sink. Everything has that look again.",
   P("cart", 420, 900, 1.0, at=0.05), P("plane", 1000, 420, 0.9, at=0.35, anim="bob"), G(1450, "hips", "smug", extras=["hardhat"], at=0.6),
   P("pricetag", 1650, 560, 1.1, text="$$$", at=0.75, anim="pulse"))
S.append({"say": "So today, let's figure out what is actually going on with prices, in plain English, with stick figures.",
          "items": [P("tv", 980, 800, 1.4, text="INFLATION, EXPLAINED"), G(330, "wave", "happy", extras=DAVE, at=0.4)],
          "chapter": "Today's question"})

# PART 1: THE NUMBER ------------------------------------------------------------
sc("Every month, the government checks the price of a giant imaginary shopping basket.",
   G(520, "hold", "neutral", extras=ECON, label="Government counter"), P("cart", 1150, 900, 1.3, at=0.3),
   T("THE BASKET", 1150, 520, 70, "dark", at=0.5), chapter="Part 1: The number", bg="paper")
sc("Food, rent, gas, haircuts, used cars, airline seats. Thousands of prices, all in one basket.",
   P("bread", 420, 520, 0.8, at=0.05), P("house", 760, 600, 0.6, at=0.2), P("gaspump", 1060, 640, 0.6, at=0.35),
   P("car", 1360, 640, 0.6, at=0.5), P("plane", 1650, 440, 0.55, at=0.65), P("cart", 960, 960, 0.8, at=0.8), ground=False)
sc("Then they compare that basket to a year ago. That number is called the Consumer Price Index, or CPI.",
   P("calendar", 520, 820, 1.2, text="2025"), P("calendar", 1400, 820, 1.2, text="2026", at=0.3),
   {"arrow": [[700, 640], [1220, 640]], "at": 0.45}, T("CPI", 960, 300, 150, "blue", at=0.7))
sc("In September, prices were three point seven percent higher than a year earlier.",
   {"count": [0, 3.7], "fmt": "{:.1f}%", "x": 960, "y": 420, "size": 260, "color": "red", "dur": 1.8},
   G(1500, "panic", "shock", extras=DAVE, at=0.55))
sc("For the two months before that, it was three point four. Economists had guessed three point six.",
   {"bars": {"values": [3.4, 3.4, 3.7], "labels": ["July", "August", "September"], "colors": ["grey", "grey", "red"], "fmt": "{}%",
             "w": 900, "h": 420}, "x": 900, "y": 820},
   G(1650, "think", "confused", extras=ECON, at=0.6))
sc("So inflation didn't just stay high. It sped up, and it beat the experts' guess.",
   P("arrowup", 960, 760, 1.6, text="FASTER", color="red", anim="pulse"), G(420, "facepalm", "tired", extras=ECON, at=0.4))
sc("One market analyst put it like this: the report was clearly hot, and there aren't many ways to sugarcoat it.",
   G(560, "present", "worried", extras=ECON, label="Adam Crisafulli, Vital Knowledge"),
   P("speech", 1250, 520, 1.5, text="no sugarcoating", at=0.35), {"cross": [1520, 760, 70], "at": 0.7},
   T("SUGAR", 1520, 760, 50, "dark", at=0.6))
sc("When a finance person says there's no way to sugarcoat it, that's finance for: please sit down.",
   G(700, "panic", "scream", extras=DAVE), P("desk", 1300, 900, 1.0, text="SIT", at=0.4))

# PART 2: WHY GAS ------------------------------------------------------------
sc("So what's driving it? Mostly one thing you can smell from the parking lot. Gasoline.",
   P("gaspump", 960, 900, 1.6, anim="pulse"), T("?", 1300, 300, 220, "red", at=0.3), chapter="Part 2: The gas problem")
sc("Gas prices jumped nine point one percent in a single month, from August to September.",
   {"count": [0, 9.1], "fmt": "+{:.1f}%", "x": 960, "y": 380, "size": 220, "color": "red"},
   P("calendar", 520, 900, 0.9, text="AUG", at=0.4), {"arrow": [[640, 760], [1240, 760]], "at": 0.5},
   P("calendar", 1400, 900, 0.9, text="SEP", at=0.6))
sc("That one item was responsible for more than half of the whole monthly rise in prices.",
   {"bars": {"values": [55, 45], "labels": ["gasoline", "everything else"], "colors": ["red", "grey"], "fmt": "{}%", "w": 700, "h": 440},
    "x": 820, "y": 820}, G(1550, "point", "shock", extras=DAVE, look=-1, at=0.6))
sc("Compared with a year ago, gasoline is up thirty four percent. Energy overall is up about twenty percent.",
   P("arrowup", 640, 760, 1.4, text="GAS +34%", color="red"), P("arrowup", 1280, 760, 1.1, text="ENERGY +20%", color="orange", at=0.45))
sc("And diesel, the fuel that moves trucks, hit a record six dollars and twenty nine cents a gallon in late September.",
   P("truck", 1000, 900, 1.5, text="FOOD", in_="slide_l"), T("$6.29", 1000, 300, 150, "red", at=0.5),
   {"stamp": "RECORD", "x": 1550, "y": 420, "at": 0.75, "size": 80, "w": 260})
sc("Here's why that matters even if you never drive a truck. Almost everything you buy rode on one.",
   P("truck", 640, 900, 1.0, in_="slide_l"), {"arrow": [[900, 760], [1260, 760]], "at": 0.4},
   P("cart", 1500, 900, 1.0, at=0.55), G(1820, "shrug", "confused", extras=DAVE, look=-1, s=0.8, at=0.7))
sc("When diesel costs more, delivery costs more. And delivery costs sneak into the price of bread, eggs and everything on the shelf.",
   P("bread", 600, 700, 1.2, text="+", at=0.3), P("egg", 1000, 700, 1.4, text="+", at=0.5), P("coffee", 1380, 700, 1.0, text="+", at=0.7),
   G(1720, "cry", "cry", extras=DAVE, look=-1, at=0.8))

# PART 3: WHY ENERGY --------------------------------------------------------
sc("So why is energy so expensive? According to the reporting, the big reasons are two wars.",
   P("barrel", 960, 900, 1.6, anim="shake"), T("WHY?", 960, 300, 150, "red", at=0.3), chapter="Part 3: Why energy?")
sc("The war with Iran, and Russia's war in Ukraine. Both happen in places that matter a lot for oil and gas.",
   P("globe", 960, 900, 2.2, anim="spin"), {"ring": [760, 520, 90], "at": 0.3}, {"ring": [1080, 330, 80], "at": 0.6})
sc("Take the Strait of Hormuz. It's a narrow strip of water next to Iran that tankers have to squeeze through.",
   P("strait", 960, 900, 1.6, text="STRAIT OF HORMUZ"), P("ship", 960, 600, 0.45, anim="bob", at=0.4))
sc("Normally about a fifth of the world's oil passes through there. So when ships there get attacked, the whole world feels it.",
   P("strait", 960, 900, 1.6), P("ship", 820, 620, 0.4, anim="shake", at=0.3), P("fire", 820, 560, 0.6, at=0.5),
   T("1/5 OF THE WORLD'S OIL", 960, 140, 80, "red", at=0.15))
sc("This week two cargo ships sank near the strait after being hit by unknown projectiles.",
   P("ship", 700, 820, 0.6, move=[700, 1000], anim="shake"), P("ship", 1300, 820, 0.6, move=[1300, 1020], anim="shake", at=0.3),
   G(1700, "panic", "scream", extras=DAVE, look=-1, s=0.8, at=0.6))
sc("The UN is worried about food, too. A third of the world's fertilizer shipments normally pass through that same strait.",
   P("strait", 960, 900, 1.4), T("FERTILIZER", 960, 300, 100, "green", at=0.3), P("bread", 1550, 780, 0.9, at=0.6),
   G(380, "think", "worried", extras=["glasses"], label="the UN", at=0.5))
sc("Fun fact: you can't eat oil. But you also can't grow wheat cheaply without fuel and fertilizer. Economics is just everything touching everything.",
   G(560, "think", "confused", extras=DAVE), P("barrel", 1000, 900, 0.9, at=0.3), {"arrow": [[1080, 700], [1300, 700]], "at": 0.5},
   P("bread", 1500, 860, 1.0, at=0.6))

# PART 4: NOT JUST GAS ------------------------------------------------------
sc("Now, economists also look at something called core inflation. That's prices without food and energy.",
   G(500, "present", "neutral", extras=ECON), {"box": [900, 380, 760, 420], "color": "white", "at": 0.3},
   T("CORE = no gas, no food", 1280, 590, 64, "blue", at=0.5), chapter="Part 4: Is it spreading?")
sc("Why throw those out? Because gas and food bounce around like a cat on caffeine.",
   P("gaspump", 700, 900, 0.9, anim="shake"), P("bread", 1200, 760, 0.9, anim="bob"), T("BOING", 960, 300, 110, "orange", at=0.4))
sc("Core inflation rose to two point six percent, up from two point four in August.",
   {"bars": {"values": [2.4, 2.6], "labels": ["August", "September"], "colors": ["grey", "blue"], "fmt": "{}%", "w": 600, "h": 400},
    "x": 800, "y": 820}, G(1500, "think", "worried", extras=ECON, look=-1, at=0.5))
sc("That's smaller, but it's going the wrong way. It means expensive energy is starting to leak into other prices.",
   P("barrel", 560, 900, 1.0), {"arrow": [[680, 700], [1100, 700]], "at": 0.3}, P("house", 1350, 900, 0.7, at=0.5),
   P("car", 1720, 900, 0.6, at=0.65))
sc("Shelter costs and used car prices pushed core inflation up. And plane tickets? Up twenty two percent from a year ago.",
   P("house", 520, 900, 0.8), P("car", 980, 900, 0.8, at=0.25), P("plane", 1450, 520, 0.9, at=0.5, anim="bob"),
   T("+22%", 1450, 760, 120, "red", at=0.65))
sc("So if your family trip suddenly costs more than the hotel, the plane did that.",
   P("plane", 960, 520, 1.3, anim="bob"), G(600, "cry", "cry", extras=DAVE), G(1350, "hips", "angry", extras=["bun"], look=-1, at=0.3))

# PART 5: YOUR PAYCHECK ----------------------------------------------------------
sc("Here's the part Dave really cares about. Did his paycheck keep up?",
   G(700, "hold", "worried", extras=DAVE), P("dollar", 1200, 600, 1.2, anim="bob", at=0.3), chapter="Part 5: Your paycheck")
sc("Wages rose about three percent over the past year. Prices rose three point seven.",
   {"bars": {"values": [3.0, 3.7], "labels": ["paychecks", "prices"], "colors": ["green", "red"], "fmt": "{}%", "w": 650, "h": 440},
    "x": 860, "y": 820}, G(1550, "shrug", "sad", extras=DAVE, look=-1, at=0.6))
sc("When prices run faster than pay, your money buys a little less each month, even if the number on your paycheck went up.",
   P("scale", 960, 900, 1.3), P("dollar", 790, 520, 0.6, at=0.3), P("pricetag", 1130, 560, 0.7, text="$$$", at=0.4))
sc("It's like getting a raise from your boss, and then the universe quietly taking it back.",
   G(560, "wave", "grin", extras=DAVE), P("dollar", 900, 560, 0.8, move=[1500, 300], at=0.4),
   P("cloud", 1500, 280, 1.2, at=0.3))
sc("And people notice. In a recent CBS News poll, nine out of ten Americans said prices are the biggest thing shaping how they feel about the economy.",
   T("9 out of 10", 960, 260, 150, "red"),
   *[G(260 + i * 165, ["stand", "facepalm", "shrug", "cry", "hips", "think", "panic", "shrug", "facepalm", "stand"][i],
       ["tired", "tired", "sad", "cry", "angry", "worried", "scream", "confused", "tired", "happy"][i], s=0.55, at=0.2 + i * 0.05) for i in range(10)])

# PART 6: THE FED -----------------------------------------------------------
sc("So who's supposed to fix this? Meet the Federal Reserve, America's central bank.",
   P("building", 960, 900, 1.5, text="THE FED"), G(1550, "present", "smug", extras=FED, look=-1, at=0.4), chapter="Part 6: The Fed")
sc("The Fed's main tool is interest rates. Think of it as the economy's thermostat.",
   P("thermo", 960, 900, 1.5, text="rates"), G(500, "hold", "neutral", extras=FED, at=0.3))
sc("Raise rates, and borrowing gets more expensive. People buy fewer houses and cars, and prices cool down. Eventually.",
   P("arrowup", 520, 760, 1.2, text="RATES", color="red"), P("house", 1050, 900, 0.7, at=0.3), P("car", 1500, 900, 0.7, at=0.45),
   P("arrowdown", 1280, 520, 0.8, text="buying", color="blue", at=0.6))
sc("In September the Fed raised its rate for the first time since twenty twenty three, to between three point seven five and four percent.",
   T("3.75% to 4%", 960, 380, 150, "red"), P("calendar", 1500, 860, 1.0, text="SEP", at=0.4), G(500, "fist", "angry", extras=FED, at=0.3))
sc("After this report, markets saw about a fifty fifty chance of another hike at the next meeting, on October twenty seventh and twenty eighth.",
   P("calendar", 700, 860, 1.1, text="OCT 27"), T("50 / 50", 1300, 420, 160, "blue", at=0.35), P("scale", 1300, 950, 0.8, at=0.5))
sc("Which is awkward, because higher rates also make Dave's credit card more expensive. The medicine tastes terrible.",
   G(600, "facepalm", "tired", extras=DAVE), P("wallet", 1150, 760, 1.2, text="CARD", anim="shake", at=0.3),
   T("APR", 1550, 400, 110, "red", at=0.6))

# PART 7: POLITICS -----------------------------------------------------------
sc("And yes, this is also politics. This was the last inflation report before the November midterm elections.",
   P("ballot", 960, 900, 1.5), P("calendar", 1500, 860, 1.0, text="NOV", at=0.4), chapter="Part 7: The politics")
sc("Depending on who you ask, the blame goes to the war, to tariffs, to Russia, or to whoever is on the other team.",
   G(400, "point", "angry", look=1, extras=["cap"]), G(1520, "point", "angry", look=-1, extras=["tie"]),
   P("speech", 960, 380, 1.3, text="IT'S THEIR FAULT", at=0.35))
sc("The economists in this report mostly point at energy. Politicians mostly point at each other.",
   G(500, "point", "neutral", extras=ECON), P("barrel", 900, 900, 0.9, at=0.2),
   G(1300, "point", "angry", look=1, extras=["tie"], at=0.5), G(1650, "point", "angry", look=-1, extras=["cap"], at=0.5))
sc("We're not picking a team here. We're just counting the prices. And the prices don't care who you vote for.",
   P("pricetag", 960, 560, 1.6, text="$$$", anim="pulse"), G(500, "shrug", "neutral", extras=DAVE, at=0.3))

# WRAP UP ------------------------------------------------------------------
sc("So, quick recap. Prices are up three point seven percent from a year ago, and they sped up in September.",
   T("RECAP", 960, 200, 120, "blue"), T("prices +3.7%", 960, 420, 100, "red", at=0.2), chapter="Recap")
sc("Gasoline did most of the damage, thanks to wars near the world's oil routes. Diesel hit a record.",
   T("gas +34% in a year", 960, 420, 90, "red"), P("gaspump", 500, 900, 0.8, at=0.3), P("truck", 1450, 900, 0.8, at=0.4))
sc("It's starting to spread to other prices, paychecks are running behind, and the Fed might raise rates again.",
   P("arrowup", 500, 760, 0.9, color="red", text="core"), P("scale", 960, 900, 0.9, at=0.3), P("thermo", 1450, 900, 0.9, text="Fed", at=0.5))
sc("What happens next mostly depends on oil, and on whether those shipping lanes calm down.",
   P("strait", 960, 900, 1.4), P("ship", 960, 620, 0.45, anim="bob", at=0.4))
sc("As for Dave, he has decided to walk to work. It's very healthy. He hates it.",
   G(500, "stand", "tired", extras=DAVE, walk=True, move=[1500, 900]), P("car", 300, 900, 0.7, at=0.1),
   T("+10,000 steps", 1300, 330, 80, "green", at=0.6))
sc("What's the price that's driving you crazy right now? Tell us in the comments, and subscribe so you don't miss what happens at the Fed meeting.",
   P("speech", 960, 460, 1.8, text="your price?"), G(400, "wave", "happy", extras=DAVE, at=0.4), P("pricetag", 1500, 800, 1.0, text="???", at=0.6))

script = {
    "id": "ep001",
    "title": "Why Is Everything Expensive AGAIN? (Inflation Explained)",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Gas jumped to $4.33 a gallon, diesel hit a record and US inflation sped up to 3.7% in September 2026. "
        "Here's what actually happened, explained with stick figures: the CPI, why gasoline did most of the damage, "
        "the Strait of Hormuz, core inflation, your paycheck, and what the Federal Reserve may do next.\n\n"
        "We don't pick political sides. We just count the prices.\n\n"
        "Sources:\n"
        "CBS News, September CPI report: https://www.cbsnews.com/news/september-cpi-report-inflation-energy-costs/\n"
        "CNN, last inflation report before the midterms: https://www.cnn.com/2026/10/14/economy/us-cpi-inflation-september\n"
        "Democracy Now headlines Oct 15, 2026 (wages, Strait of Hormuz shipping, fertilizer): https://www.democracynow.org/2026/10/15/headlines\n\n"
        "#inflation #economy #explained #news #stickfigure"
    ),
    "tags": ["inflation", "cpi", "inflation explained", "gas prices", "why is everything so expensive", "economy explained",
             "federal reserve", "interest rates", "strait of hormuz", "diesel prices", "news explained", "stick figure animation"],
    "thumbnail": {"bg": "yellow", "text": "WHY IS|GAS $4.33?!", "size": 190, "color": "black",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["hair"]},
                  "items": [{"prop": "gaspump", "x": 1700, "y": 1060, "s": 1.4, "text": "$4.33"}], "guy_x": 1250},
    "scenes": [s for s in S if s],
}
# strip helper keys that are not part of the format
for s in script["scenes"]:
    for it in s["items"]:
        if "in_" in it:
            it["in"] = it.pop("in_")
    s.pop("anim_dummy", None)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep001.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")

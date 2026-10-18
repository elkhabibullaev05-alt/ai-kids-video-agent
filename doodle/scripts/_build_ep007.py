"""Episode 7: Brent oil touches $110 as Hormuz attacks surge (Oct 16, 2026)."""
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


# COLD OPEN -------------------------------------------------------------------
# COLD OPEN -------------------------------------------------------------------
sc("Picture the busiest doorway on Earth.",
   P("strait", 960, 900, 1.6, text="THE DOORWAY"), cam={"from": [960, 700, 1.5], "to": [960, 560, 1.05]})
sc("Before this year, about a hundred and twenty five big ships walked through it every single day.",
   *[P("tanker", 260 + k * 350, 880 - (k % 2) * 160, 0.45, at=0.08 * k) for k in range(5)], C(0, 125, 960, 260, fmt="{:.0f} a day", size=120, color="navy", at=0.3))
sc("About a fifth of the world's crude oil and liquefied gas supplies went through it.",
   P("globe", 650, 880, 1.1), C(0, 20, 1350, 420, fmt="~{:.0f}%", size=220, color="red", at=0.3))
sc("This week, ships trying to get through were being shot at.",
   P("strait", 960, 900, 1.3, text="HORMUZ"), {"stamp": "DANGER", "x": 960, "y": 300, "size": 90, "w": 360, "at": 0.4})
sc("And thousands of miles away, Dave was just trying to fill up his truck.",
   P("truck", 650, 900, 1.2), G(1300, "hold", "neutral", extras=DAVE, at=0.25), P("gaspump", 1600, 900, 0.9, text="$4.31", at=0.5))
sc("On Friday, the world's main oil price, Brent crude, touched one hundred and ten dollars a barrel.",
   C(72, 110, 960, 420, fmt="${:.0f}", size=280, color="red", dur=2.0), P("barrel", 1600, 900, 1.2, at=0.5))
sc("Dave doesn't buy barrels. But he's about to find out that barrels buy Dave.",
   G(700, "shrug", "confused", extras=DAVE), P("barrel", 1300, 900, 1.6, anim="bob", at=0.3), T("?", 1300, 420, 160, "red", at=0.6), bg="yellow")
sc("Today's question: why is oil back above a hundred dollars, and why does one strip of water have so much power over your wallet?",
   P("strait", 700, 900, 0.9), P("wallet", 1350, 880, 1.2, at=0.3), {"arrow": [[950, 650], [1180, 650]], "color": "red", "at": 0.5}, chapter="Today's question")
sc("We'll cover what happened, the numbers, why the doorway matters, who pays, what each side says, and what comes next.",
   P("clipboard", 760, 900, 1.1, text="FACTS"), G(1300, "present", "neutral", extras=LINDA, at=0.35))
sc("A quick note. This is a real war, and real people have died. We'll state those facts plainly. The jokes are only about money.",
   G(960, "stand", "neutral", extras=LINDA), T("FACTS FIRST", 960, 300, 100, "dark", at=0.3))

# PART 1 --------------------------------------------------------------------
sc("First, the scoreboard for Friday, October sixteenth.",
   P("scoreboard", 960, 900, 1.2, text="FRI OCT 16"), chapter="Part 1: The $110 Friday")
sc("Brent touched one hundred and ten dollars during the day, for the first time since May, according to Reuters.",
   T("$110", 700, 420, 220, "red"), P("calendar", 1400, 860, 1.0, text="SINCE MAY", at=0.4))
sc("It settled at one hundred and nine dollars and eighty six cents. Up almost four dollars in one day. That's three point seven percent.",
   C(105.92, 109.86, 960, 380, fmt="${:.2f}", size=200, color="red"), T("+3.7%", 960, 620, 120, "red", at=0.5))
sc("America's own benchmark, called W.T.I., closed at one hundred and one dollars and forty one cents. Its highest since September seventeenth.",
   C(97.97, 101.41, 700, 400, fmt="${:.2f}", size=170, color="navy"), P("calendar", 1450, 860, 1.0, text="SEP 17", at=0.4))
sc("Over the whole week, Brent rose four point nine percent. W.T.I. rose ten point four.",
   {"bars": {"values": [4.9, 10.4], "labels": ["Brent", "WTI"], "colors": ["orange", "red"], "fmt": "+{}%", "w": 700, "h": 420}, "x": 960, "y": 820})
sc("For comparison: before the war, a barrel cost about seventy two dollars. That's according to Tamas Varga at the broker P.V.M.",
   C(110, 72, 700, 420, fmt="${:.0f}", size=220, color="green"), G(1350, "present", "neutral", extras=ECON, label="oil analyst", at=0.3))
sc("So oil costs about half again what it did in February. Imagine your rent doing that. Actually, don't.",
   P("barrel", 600, 900, 0.9), P("barrel", 900, 900, 0.9, at=0.2), P("barrel", 900, 765, 0.6, at=0.35), G(1500, "facepalm", "tired", extras=DAVE, at=0.5))
sc("A barrel is forty two gallons. Refineries turn it into gasoline, diesel, jet fuel and plastic. So one price moves many others.",
   P("barrel", 450, 900, 1.0), {"arrow": [[600, 700], [900, 500]], "at": 0.2}, P("gaspump", 1050, 900, 0.7, at=0.3), P("plane", 1450, 700, 0.7, at=0.45), P("truck", 1500, 950, 0.6, at=0.6))

# PART 2 --------------------------------------------------------------------
sc("So what happened? Let's rewind to February twenty eighth, when the U.S. and Israel went to war with Iran.",
   P("calendar", 960, 860, 1.3, text="FEB 28"), chapter="Part 2: How we got here")
sc("Iran responded by effectively closing the Strait of Hormuz, the doorway between the Persian Gulf and the rest of the world's oceans.",
   P("strait", 960, 900, 1.4), P("barrier", 960, 760, 0.8, at=0.4))
sc("In late March, Brent peaked at around one hundred and eighteen dollars.",
   C(72, 118, 960, 420, fmt="${:.0f}", size=240, color="red"), {"stamp": "PEAK", "x": 1500, "y": 380, "size": 80, "w": 260, "at": 0.5})
sc("A ceasefire was announced on April eighth. But ship traffic through the strait stayed far below normal.",
   P("calendar", 600, 860, 1.0, text="APR 8"), P("tanker", 1300, 880, 0.6, at=0.3), T("STILL SLOW", 1300, 380, 90, "orange", at=0.5))
sc("By early July, oil had slid to around seventy dollars. Everyone exhaled. Dave bought a slightly bigger coffee.",
   C(118, 70, 700, 420, fmt="${:.0f}", size=200, color="green"), G(1300, "hold", "happy", extras=DAVE, at=0.3), P("coffee", 1500, 820, 0.8, at=0.5))
sc("Then it bounced above a hundred in late July, wobbled through August, and hit about a hundred and nine in early September.",
   P("chart", 960, 900, 1.3, text="JUL  AUG  SEP"), P("arrowup", 1500, 820, 0.9, color="red", at=0.5))
sc("By September, things were healing. Gulf oil flows, not counting Iran's, were back above eighty one percent of pre-war levels, says the tracking firm Kpler.",
   C(0, 81, 960, 420, fmt="{:.0f}%", size=240, color="green"), P("tanker", 1550, 880, 0.5, at=0.4))
sc("Part of the trick: about forty percent of the region's oil exports now go around the strait instead of through it.",
   P("strait", 700, 900, 0.8), P("pipeline", 1300, 900, 0.7, text="AROUND", at=0.3), C(0, 40, 1300, 400, fmt="~{:.0f}%", size=130, color="teal", at=0.5))
sc("Saudi Arabia pumps crude through a long pipeline across the country to Yanbu, a port on the Red Sea. A back door.",
   P("pipeline", 960, 760, 1.1, text="EAST  >>>  WEST"), P("tanker", 1550, 950, 0.45, at=0.4), T("YANBU", 1550, 560, 70, "navy", at=0.5))
sc("And in the Gulf, a lot of oil is passed from tanker to tanker offshore, like a very slow, very expensive bucket brigade.",
   P("tanker", 650, 880, 0.55), P("tanker", 1250, 880, 0.55, at=0.2), {"arrow": [[820, 600], [1080, 600]], "color": "dark", "at": 0.4}, T("PASS IT ON", 960, 300, 80, "dark", at=0.55))

# PART 3 --------------------------------------------------------------------
sc("Then October arrived, and the attacks came back.",
   P("calendar", 960, 860, 1.3, text="OCTOBER", color="red"), chapter="Part 3: The attacks")
sc("Since October second, Britain's maritime security office has reported at least one attack a day in the Strait of Hormuz or the Gulf of Aden.",
   *[P("calendar", 330 + k * 210, 860, 0.45, text="!", at=0.06 * k) for k in range(7)], T("1+ A DAY", 960, 300, 120, "red", at=0.5))
sc("On October first, a Kuwaiti tanker was struck and caught fire. Five people were rescued.",
   P("tanker", 960, 900, 0.8, text="KAZIMAH III"), T("5 RESCUED", 960, 330, 90, "navy", at=0.5))
sc("A few days later, India's foreign ministry said twelve crew on a Panama-flagged tanker were injured by an unknown projectile.",
   P("tanker", 700, 900, 0.6), C(0, 12, 1400, 420, fmt="{:.0f} injured", size=120, color="dark", at=0.4))
sc("On Wednesday, a Singapore-flagged container ship, the G.F.S. Pride, was hit by an Iranian projectile, according to U.S. Central Command. It sank while being towed.",
   P("ship", 960, 900, 0.9), T("GFS PRIDE", 960, 380, 90, "dark", at=0.4))
sc("The International Maritime Organization says more than twenty civilian sailors have been killed in Iranian attacks on shipping since February.",
   C(0, 20, 960, 420, fmt="{:.0f}+", size=240, color="dark"), T("civilian sailors killed", 960, 640, 70, "dark", at=0.4))
sc("Those are people with families, on ships carrying the stuff the rest of us use. Worth remembering when we talk about prices.",
   G(960, "stand", "sad", extras=LINDA), P("ship", 1550, 900, 0.5, at=0.3))
sc("The tracking firm Kpler says that in the week to October thirteenth, oil flows through the strait fell to eleven point six million barrels a day.",
   C(17.15, 11.62, 960, 420, fmt="{:.2f}M", size=220, color="red", dur=2.0), T("barrels a day", 960, 620, 70, "dark", at=0.4))
sc("The normal baseline is about seventeen point two million. So roughly a third of the doorway's traffic just went missing.",
   {"bars": {"values": [17.15, 11.62], "labels": ["normal", "this week"], "colors": ["grey", "red"], "fmt": "{}M", "w": 700, "h": 420}, "x": 960, "y": 820})
sc("Then on Friday, a Saudi-led coalition said it intercepted a ballistic missile aimed at Yanbu. That's the back door.",
   P("pipeline", 700, 900, 0.8, text="YANBU"), {"ring": [700, 760, 260], "color": "red", "at": 0.3}, {"cross": [1400, 450, 120], "at": 0.5})
sc("Rapidan Energy said early reports showed no damage. But traders heard 'missile' and 'back door' in one sentence, and that was enough.",
   G(700, "panic", "scream", **TRADER, label="oil trader", anim="shake"), P("chart", 1350, 900, 1.0, text="BUY!", color="red", at=0.3), bg="yellow")

# PART 4 --------------------------------------------------------------------
sc("And it wasn't only the Middle East. On Thursday, Ukraine struck a Russian oil refinery.",
   P("globe", 960, 880, 1.2), P("fire", 1450, 900, 0.8, at=0.4), chapter="Part 4: The second fire")
sc("Ukraine's president said Kyiv was abandoning an energy-site ceasefire that the U.S. president had announced.",
   G(650, "stand", "neutral", extras=["tie"], label="Ukraine's president"), G(1300, "stand", "neutral", extras=["tie"], shirt="navy", label="the U.S. president", look=-1, at=0.3))
sc("Two industry sources told Reuters that Russia's Ryazan refinery stopped one of its main crude units after a drone attack.",
   P("building", 960, 900, 1.0, text="REFINERY"), T("PAUSED", 960, 300, 100, "red", at=0.4))
sc("Dennis Kissler of BOK Financial told Reuters it's questionable how much diesel Russia can deliver. That's two supply worries at once.",
   G(600, "think", "worried", extras=ECON, label="analyst"), T("WORRY x2", 1300, 420, 120, "red", at=0.4))
sc("Then the weather. Hurricanes shut some U.S. production, and U.S. crude stocks fell eight and a half million barrels in one week.",
   P("cloud", 600, 500, 1.0), C(0, -8.56, 1300, 420, fmt="{:.2f}M", size=180, color="red", at=0.3), P("barrel", 1300, 900, 0.8, at=0.5))

# PART 5 --------------------------------------------------------------------
sc("So who pays? Let's follow the barrel.",
   P("barrel", 960, 900, 1.3, anim="bob"), chapter="Part 5: Who pays")
sc("At the pump: AAA's national average for regular gas was four dollars and thirty one cents on Saturday.",
   P("gaspump", 700, 900, 1.3, text="$4.31"), G(1250, "hold", "tired", extras=DAVE, at=0.3))
sc("That's slightly lower than last week, because pump prices lag behind crude. Think of it as the bill arriving after dinner.",
   P("gaspump", 600, 900, 0.9, text="$4.31"), P("clipboard", 1200, 900, 1.0, text="BILL", at=0.3), P("arrowup", 1550, 820, 0.8, color="red", at=0.55))
sc("Then there's diesel, which moves almost every truck, train and tractor. When diesel rises, the cost of moving stuff rises.",
   P("truck", 650, 900, 1.1, text="DIESEL"), G(1350, "hold", "worried", **TRUCK, label="trucker", at=0.3))
sc("Bread, bananas, your new phone. They all ride on diesel to the shelf.",
   P("bread", 500, 880, 1.0), P("cart", 960, 900, 1.0, at=0.25), P("phone", 1400, 880, 0.9, at=0.45))
sc("Airlines buy jet fuel. After the war began, North American jet fuel prices rose ninety five percent.",
   P("plane", 800, 600, 1.2), C(0, 95, 1400, 420, fmt="+{:.0f}%", size=180, color="red", at=0.4))
sc("And shipping itself got pricey. There aren't enough tankers, so freight rates hit records.",
   P("tanker", 700, 900, 0.7), P("pricetag", 1350, 800, 1.0, text="RECORD", at=0.3))
sc("Chris Beauchamp at the trading firm I.G. put it simply: Ships don't get built overnight.",
   G(700, "present", "neutral", extras=ECON, label="markets analyst"), T("“Ships don't get built", 1300, 380, 70, "navy", at=0.3), T("overnight.”", 1300, 470, 70, "navy", at=0.4))
sc("Europe feels it in heating. The Dutch gas price that Europe watches was near a four-year high this week.",
   P("house", 700, 900, 1.0), P("thermo", 1300, 900, 1.0, text="GAS", color="red", at=0.3))
sc("For Dave: his truck, his groceries, his Christmas flight to see his mum. All a bit pricier. None of it his fault.",
   G(500, "shrug", "tired", extras=DAVE), P("truck", 1000, 900, 0.6, at=0.2), P("cart", 1300, 900, 0.6, at=0.35), P("plane", 1600, 650, 0.5, at=0.5))
sc("Saudi Aramco's chief executive, Amin Nasser, said this month that nearly three billion barrels of supply have been lost since the conflict began.",
   G(600, "present", "neutral", extras=["tie"], label="Aramco CEO"), C(0, 3, 1300, 420, fmt="~{:.0f} BILLION", size=120, color="red", at=0.3))
sc("He said rebuilding the world's oil stockpiles could take up to two years. His words: The system is already straining.",
   P("calendar", 700, 860, 1.0, text="2 YEARS"), T("“The system is", 1300, 380, 70, "navy", at=0.3), T("already straining.”", 1300, 470, 70, "navy", at=0.4))

# PART 6 --------------------------------------------------------------------
sc("Now, what does each side say? Depending on who you ask, the strait is either open or closed.",
   P("strait", 960, 900, 1.1), T("OPEN?", 600, 330, 100, "green", at=0.3), T("CLOSED?", 1350, 330, 100, "red", at=0.45), chapter="Part 6: What each side says")
sc("U.S. Central Command spokesman Captain Tim Hawkins told Fox News: The strait is open, it is available for transit.",
   G(650, "point", "neutral", extras=["cap"], shirt="navy", label="U.S. military spokesman"), T("“The strait is open”", 1300, 400, 70, "navy", at=0.3))
sc("He said about ninety seven percent of ships that tried to cross did so without being hit.",
   C(0, 97, 960, 420, fmt="{:.0f}%", size=260, color="green"), P("tanker", 1550, 880, 0.5, at=0.4))
sc("Central Command's commander said about four hundred merchant ships crossed in the past seven days.",
   C(0, 400, 960, 420, fmt="{:.0f}", size=240, color="navy"), T("ships in 7 days", 960, 620, 70, "dark", at=0.4))
sc("The U.S. president has repeatedly claimed credit for the rise in oil flows, and says America controls the strait.",
   G(960, "present", "smug", extras=["tie"], shirt="navy", label="the U.S. president"), P("podium", 960, 900, 0.9))
sc("Iran tells a different story. It says it's stepping up strikes in response to the U.S. blockade of its ports and tougher sanctions from last month.",
   G(960, "point", "angry", extras=["tie"], shirt="green", label="Iran's government", look=-1), P("barrier", 1500, 900, 0.7, text="BLOCKADE", at=0.3))
sc("Iran also disputes that flows have recovered, calling the amount getting through negligible, and says it still has effective control of the strait.",
   G(700, "hips", "neutral", extras=["tie"], shirt="green", label="Iran's government"), T("“negligible”", 1350, 420, 90, "red", at=0.35))
sc("One side counts the ships that made it. The other counts what didn't. Both numbers are real.",
   P("scale", 960, 900, 1.3), T("97% made it", 560, 340, 70, "green", at=0.3), T("1/3 flow gone", 1380, 340, 70, "red", at=0.45))
sc("We don't pick a team. We just count the facts.",
   P("clipboard", 760, 900, 1.0, text="FACTS"), G(1300, "stand", "neutral", extras=LINDA, at=0.3))

# PART 7 --------------------------------------------------------------------
sc("So what are governments doing about the price? Mostly, opening the emergency cupboard.",
   P("house", 960, 900, 1.1, text="RESERVE"), chapter="Part 7: The emergency cupboard")
sc("Back in March, the International Energy Agency agreed a plan to release four hundred million barrels from countries' emergency reserves.",
   C(0, 400, 960, 420, fmt="{:.0f}M", size=240, color="navy"), P("barrel", 1550, 900, 0.8, at=0.4))
sc("America agreed to lend one hundred seventy two million barrels of that from its Strategic Petroleum Reserve.",
   C(0, 172, 960, 420, fmt="{:.0f}M", size=220, color="navy"), T("USA", 960, 640, 80, "dark", at=0.4))
sc("On Thursday, the agency agreed to release over twenty million barrels of fuel. On Friday, the U.S. offered up to seventeen million more barrels of crude.",
   T("20M+", 600, 420, 150, "teal"), T("+17M", 1300, 420, 150, "teal", at=0.4))
sc("Sounds like a lot. But at normal flows, the strait moves about seventeen million barrels a day. So that's roughly one day of the doorway.",
   C(0, 1, 960, 420, fmt="~{:.0f} DAY", size=200, color="orange"), P("strait", 1550, 900, 0.5, at=0.4))
sc("It's like filling a bathtub with an eye dropper while someone's still pulling the plug.",
   P("eye", 700, 700, 0.8), P("barrel", 1250, 900, 1.0, at=0.3), G(1600, "facepalm", "tired", extras=DAVE, at=0.5), bg="yellow")
sc("The U.S. is also reportedly weighing easing sanctions on some 'shadow fleet' tankers, which carry sanctioned oil, to ease the shortage.",
   P("tanker", 960, 880, 0.8, color="grey", text="SHADOW FLEET"), T("?", 1500, 400, 160, "red", at=0.4))
sc("Analysts at the Dutch bank I.N.G. questioned whether those tankers are actually available, since they're already busy carrying oil.",
   G(700, "think", "confused", extras=ECON, label="bank analysts"), P("tanker", 1350, 880, 0.5, color="grey", text="BUSY", at=0.3))

# PART 8 --------------------------------------------------------------------
sc("So, what's next? Three things to watch.",
   P("eye", 960, 800, 1.2), chapter="Part 8: What's next")
sc("One: the attacks. Tamas Varga says the recovery in flows is sustainable, unless attacks on ships, shipping lanes or the pipeline resume.",
   T("1", 400, 400, 200, "navy"), P("tanker", 1000, 880, 0.6, at=0.3), P("pipeline", 1450, 900, 0.5, at=0.45))
sc("Which, this week, they did.",
   P("calendar", 960, 860, 1.2, text="THIS WEEK", color="red"), {"ring": [960, 740, 220], "at": 0.4})
sc("Two: the back door. If Yanbu and the Saudi pipeline stay safe, a lot of oil keeps flowing around the problem.",
   T("2", 400, 400, 200, "navy"), P("pipeline", 1100, 850, 0.9, text="YANBU", at=0.3))
sc("Three: a deal. I.N.G. says markets are pricing in a significant risk premium, and removing it fully needs some kind of agreement between the U.S. and Iran.",
   T("3", 400, 400, 200, "navy"), G(950, "stand", "neutral", extras=["tie"], shirt="navy", at=0.2), G(1450, "stand", "neutral", extras=["tie"], shirt="green", look=-1, at=0.3), P("speech", 1200, 420, 0.8, text="DEAL?", at=0.5))
sc("Kpler expects a slower, uneven recovery in flows without a comprehensive political deal.",
   P("chart", 960, 900, 1.2, text="SLOW + BUMPY"), P("tanker", 1600, 900, 0.4, at=0.4))
sc("And Dave? Dave now plans his errands like a heist. One trip. Six stops. No mercy.",
   G(600, "think", "smug", extras=DAVE), P("clipboard", 1200, 900, 1.0, text="1 TRIP", at=0.3), P("truck", 1600, 900, 0.5, at=0.5))

# RECAP --------------------------------------------------------------------
sc("Recap. Brent oil touched one hundred and ten dollars on Friday, its highest since May, after a surge in attacks around the Strait of Hormuz.",
   T("$110", 600, 420, 170, "red"), P("strait", 1350, 900, 0.7, at=0.3), chapter="Recap")
sc("A third of the strait's oil flow went missing, a Russian refinery was hit, and Saudi Arabia's back door got a scare.",
   T("-1/3", 450, 420, 130, "red"), P("fire", 960, 900, 0.7, at=0.25), P("pipeline", 1500, 900, 0.5, at=0.45))
sc("The U.S. says the strait is open. Iran says it's in control. Prices say: nobody's relaxing yet.",
   T("OPEN", 500, 400, 110, "green"), T("CONTROL", 960, 400, 110, "red", at=0.25), P("chart", 1500, 900, 0.8, text="$$$", color="red", at=0.45))
sc("Meanwhile, in the busiest doorway on Earth, the ships are still lining up, very politely, very slowly.",
   *[P("tanker", 300 + k * 330, 880, 0.4, at=0.08 * k) for k in range(5)], P("strait", 960, 520, 0.6, at=0.5), bg="yellow")
sc("Your turn: has the price of fuel changed how you drive, shop or travel this year? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("gaspump", 1250, 900, 0.9, text="?", at=0.3))
sc("And if calm stick figures explaining the news is your kind of thing, subscribe. We'll keep counting the facts. And the barrels.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep007",
    "title": "Oil Just Hit $110 Again. Why Does One Strait Matter?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Friday, October 16, 2026, Brent crude touched $110 a barrel for the first time since May and settled at $109.86, "
        "after a surge in attacks on shipping around the Strait of Hormuz, a missile aimed at Saudi Arabia's Red Sea port of Yanbu "
        "and a Ukrainian strike on a Russian refinery. Why one narrow strip of water moves the price of your gas, groceries and "
        "flights, what the U.S. and Iran each say, what governments are doing and what to watch next. Explained with stick figures, "
        "facts only.\n\n"
        "Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported.\n\n"
        "Sources:\n"
        "Reuters via Yahoo Finance, Oil touches $110 a barrel for first time since May (Oct 16, 2026): https://finance.yahoo.com/energy/articles/oil-edges-down-investors-weigh-010642305.html\n"
        "Oilprice.com, Oil Prices Head for Weekly Gain as Hormuz Attacks Rattle Markets (Oct 16, 2026): https://oilprice.com/Latest-Energy-News/World-News/Oil-Prices-Head-for-Weekly-Gain-as-Hormuz-Attacks-Rattle-Markets.html\n"
        "Al Jazeera, Hormuz ship attacks surge: Are increased oil exports sustainable? (Oct 6, 2026): https://www.aljazeera.com/news/2026/10/6/hormuz-ship-attacks-surge-are-increased-oil-exports-sustainable\n"
        "Fox News, 'Vast majority' of Iran's attempted attacks on Strait of Hormuz are unsuccessful, CENTCOM spokesman says (Oct 17, 2026): https://www.foxnews.com/world/vast-majority-irans-attempted-attacks-strait-hormuz-unsuccessful-centcom-spokesman-says\n"
        "Euronews / AP, Oil prices rise after reported attacks on ships in Strait of Hormuz (Oct 14, 2026): https://www.euronews.com/2026/10/14/oil-prices-rise-after-reported-attacks-on-ships-in-strait-of-hormuz\n"
        "AAA national gas price average: https://gasprices.aaa.com/\n"
        "Wikipedia, 2026 Iran war fuel crisis (background, price history): https://en.wikipedia.org/wiki/2026_Iran_war_fuel_crisis\n\n"
        "#oil #oilprice #hormuz #gasprices #explained #stickfigure #news"
    ),
    "tags": ["oil price", "brent crude 110", "strait of hormuz", "oil prices explained", "gas prices", "diesel prices",
             "iran tanker attacks", "oil news", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "OIL $110|AGAIN?!", "size": 190, "color": "black",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["hair"]},
                  "items": [{"prop": "barrel", "x": 1700, "y": 900, "s": 1.6, "text": "OIL", "color": "dark"}], "guy_x": 1300},
    "scenes": [s for s in S if s],
}
_CYC = ["paper", "sky", "paper", "teal", "paper", "purple"]
for _i, _s in enumerate(script["scenes"]):
    if _s.get("bg") != "yellow":
        _s["bg"] = _CYC[_i % len(_CYC)]
for s in script["scenes"]:
    for it in list(s["items"]):
        g = it.get("guy")
        if g and g.get("label"):
            sz = it.get("s", 1.0)
            s["items"].append({"text": g.pop("label"), "x": it["x"], "y": it.get("y", 900) - int(430 * sz), "size": 44,
                               "color": "dark", "at": it.get("at", 0)})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep007.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

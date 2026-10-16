"""Episode 2: Tesla unveils the long-delayed second-generation Roadster (Oct 15, 2026), explained with stick figures."""
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
CEO = ["tie"]
LINDA = ["bun"]
ENG = ["hardhat"]

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN --------------------------------------------------------------------
sc("This is Dave in twenty seventeen. Dave just put down money for a car that does not exist yet.",
   P("calendar", 1450, 860, 1.1, text="2017"), G(650, "fist", "grin", extras=DAVE), P("moneybag", 1000, 900, 0.9, text="$", at=0.45),
   cam={"from": [960, 540, 1.12], "to": [1000, 560, 1.0]})
sc("This is Dave nine years later. Different job, different phone, same reservation.",
   P("calendar", 1450, 860, 1.1, text="2026"), G(650, "stand", "tired", extras=DAVE + ["sweat"]),
   {"count": [2017, 2026], "fmt": "{:.0f}", "x": 960, "y": 300, "size": 150, "color": "red", "dur": 2.0, "at": 0.2})
sc("And on Thursday night, the car finally showed up. Then it did a kickflip.",
   P("sportscar", 980, 700, 1.5, anim="spin", at=0.15), G(400, "panic", "scream", extras=DAVE, look=1, at=0.4),
   T("KICKFLIP?!", 1400, 260, 110, "red", at=0.6), bg="sky")
sc("Tesla has revealed the new Roadster. A sports car with rocket style thrusters, built with help from SpaceX.",
   P("sportscar", 760, 900, 1.3), P("rocket", 1450, 900, 1.0, at=0.35), {"arrow": [[1300, 600], [980, 700]], "at": 0.5},
   T("+", 1120, 420, 140, "dark", at=0.45))
S.append({"say": "So today: can this car really fly, when can anyone actually buy it, and why is a car company borrowing parts from a rocket company?",
          "items": [P("tv", 980, 800, 1.4, text="THE FLYING CAR?"), G(330, "think", "confused", extras=DAVE, at=0.4),
                    T("?", 1650, 330, 200, "red", at=0.7)],
          "chapter": "Today's question"})

# PART 1: THE LONG WAIT ----------------------------------------------------------
sc("To understand why people care, we need to go back. All the way back to November twenty seventeen.",
   P("calendar", 960, 860, 1.4, text="NOV 2017"), G(1500, "point", "neutral", extras=LINDA, look=-1, at=0.4),
   chapter="Part 1: The long wait")
sc("Tesla held an event for a big electric truck. At the end, a surprise guest appeared: a new sports car.",
   P("truck", 750, 900, 1.4), P("sportscar", 1450, 900, 0.8, in_="slide_l", at=0.45), T("SURPRISE", 1450, 330, 90, "orange", at=0.6))
sc("The promises were huge. Zero to sixty miles per hour in one point nine seconds.",
   P("stopwatch", 700, 900, 1.3, text="1.9s"), {"count": [0, 60], "fmt": "{:.0f} mph", "x": 1350, "y": 420, "size": 150, "dur": 1.9, "at": 0.3})
sc("A range of six hundred and twenty miles on one charge. A top speed above two hundred and fifty miles per hour.",
   T("620 miles", 600, 380, 120, "green"), T("250+ mph", 1350, 380, 120, "red", at=0.4), P("sportscar", 960, 900, 1.0, at=0.2))
sc("Four seats. Two in the front, two small ones in the back. And production in twenty twenty.",
   *[G(560 + i * 260, "stand", "happy", s=0.6, at=0.1 + i * 0.12) for i in range(4)], P("calendar", 1650, 860, 0.9, text="2020", at=0.7))
sc("Buyers could reserve one with a fifty thousand dollar deposit. The first one thousand cars, called the Founders Series, cost two hundred and fifty thousand, paid up front.",
   {"count": [0, 50000], "fmt": "${:,.0f}", "x": 620, "y": 380, "size": 120, "color": "green", "dur": 1.6},
   T("Founders: $250,000", 1300, 640, 80, "red", at=0.5), P("moneybag", 1650, 900, 0.8, at=0.6))
sc("Then twenty twenty came and went. So did a lot of other dates.",
   P("calendar", 500, 860, 0.9, text="2020"), {"cross": [500, 740, 90], "at": 0.3},
   P("calendar", 1000, 860, 0.9, text="2024", at=0.4), {"cross": [1000, 740, 90], "at": 0.55},
   P("calendar", 1500, 860, 0.9, text="2025", at=0.65), {"cross": [1500, 740, 90], "at": 0.8})
sc("This year alone, the unveiling was promised for April, then late April, then about a month after a spring earnings call.",
   P("calendar", 520, 860, 0.9, text="APR"), P("calendar", 960, 860, 0.9, text="LATE APR", at=0.3),
   P("calendar", 1400, 860, 0.9, text="MAY?", at=0.6), G(1750, "facepalm", "tired", extras=DAVE, look=-1, s=0.8, at=0.75))
sc("Then August. Then October first, which was pushed back because of the weather. Then, finally, October fifteenth.",
   P("calendar", 500, 860, 0.9, text="AUG"), P("cloud", 960, 400, 1.1, at=0.3), P("calendar", 960, 860, 0.9, text="OCT 1", at=0.3),
   P("calendar", 1450, 860, 1.1, text="OCT 15", at=0.65), {"ring": [1450, 740, 130], "at": 0.8})
sc("For comparison, in the time Dave waited, he could have grown a beard, lost interest in the beard, and grown it back.",
   G(700, "stand", "tired", extras=DAVE), {"count": [0, 9], "fmt": "{:.0f} years", "x": 1300, "y": 400, "size": 130, "color": "red", "dur": 2},
   P("calendar", 1300, 900, 0.8, at=0.5))

# PART 2: THE REVEAL -------------------------------------------------------------
sc("So, Thursday night. The show took place at SpaceX's rocket testing site near Waco, Texas, and was streamed online.",
   P("rocket", 600, 900, 1.2), P("tv", 1350, 820, 1.2, text="LIVE", at=0.4), T("WACO, TEXAS", 960, 180, 80, "dark", at=0.2),
   chapter="Part 2: The reveal", bg="sky")
sc("Out came the car. Tesla says the new look borrows from its angular Cybertruck, and from famous military jets.",
   P("sportscar", 960, 900, 1.6, in_="slide_l"), G(300, "present", "smug", extras=CEO, label="Tesla's CEO", at=0.5))
sc("It has hidden headlights, one long taillight, and a white paint that Tesla says borrows from coatings used to protect rockets.",
   P("sportscar", 960, 900, 1.4, color="white"), {"ring": [700, 790, 60], "at": 0.25}, {"ring": [1260, 800, 60], "at": 0.5},
   T("ROCKET PAINT", 960, 300, 90, "blue", at=0.7))
sc("Inside: a yoke instead of a round steering wheel, a touchscreen, and a seat that doesn't move, to save weight.",
   P("desk", 960, 900, 1.0, text="YOKE"), G(500, "think", "confused", extras=DAVE, at=0.3),
   T("seat: fixed", 1450, 420, 80, "dark", at=0.6))
sc("The body uses magnesium, titanium and carbon fiber. Basically, the periodic table's luxury aisle.",
   T("Mg", 500, 420, 150, "grey"), T("Ti", 960, 420, 150, "blue", at=0.25), T("C", 1420, 420, 150, "dark", at=0.5),
   G(1700, "hips", "smug", extras=LINDA, look=-1, s=0.8, at=0.7))
sc("And then came the stunts. On the livestream, the car flipped through the air like a skateboard.",
   P("sportscar", 960, 640, 1.3, anim="spin"), G(400, "panic", "shock", extras=DAVE), G(1550, "panic", "scream", extras=LINDA, look=-1, at=0.3))
sc("Tesla posted the stunt clip online afterwards. It did not post many technical details about how it was done.",
   P("tv", 760, 820, 1.2, text="CLIP"), P("speech", 1400, 480, 1.3, text="details?", at=0.4), T("?", 1400, 760, 140, "red", at=0.7))

# PART 3: HOW DOES A CAR FLY ------------------------------------------------------
sc("So, can it fly? Short answer: not like a plane. More like a very expensive jump.",
   P("plane", 600, 420, 0.9), {"cross": [600, 420, 120], "at": 0.3}, P("sportscar", 1300, 760, 1.0, move=[1300, 600], at=0.4),
   chapter="Part 3: How does a car fly?")
sc("The trick is something called cold gas thrusters. You fill tanks with gas under high pressure, then let it blast out of nozzles.",
   P("tank", 600, 900, 1.2, text="GAS"), {"arrow": [[700, 760], [1100, 760]], "at": 0.35}, T("WHOOSH", 1400, 760, 120, "blue", at=0.5))
sc("Push gas one way, and the car gets pushed the other way. It's the same idea as letting go of a balloon.",
   {"arrow": [[1000, 600], [500, 600]], "color": "blue"}, {"arrow": [[1100, 600], [1600, 600]], "color": "red", "at": 0.35},
   P("sportscar", 1050, 900, 1.0, at=0.1))
sc("No flames, no fuel burning. Just squeezed gas. That's why it's called cold.",
   P("fire", 600, 900, 1.0), {"cross": [600, 760, 110], "at": 0.3}, P("tank", 1300, 900, 1.0, text="COLD", color="sky", at=0.5))
sc("According to Tesla's engineering vice president, Lars Moravy, the demo car had ten thrusters.",
   G(500, "present", "neutral", extras=ENG, label="Lars Moravy, Tesla"),
   {"count": [0, 10], "fmt": "{:.0f} thrusters", "x": 1250, "y": 420, "size": 120, "color": "red", "dur": 1.5, "at": 0.4})
sc("They were fed by six hundred liters of compressed air. That's about one hundred and fifty nine gallons, and it can be refilled.",
   P("tank", 700, 900, 1.0, text="600 L"), P("tank", 900, 900, 1.0, at=0.2), P("tank", 1100, 900, 1.0, at=0.3),
   T("= 159 gallons", 1500, 420, 90, "blue", at=0.6))
sc("Tesla says the tanks are stuffed into almost every empty space in the car. More gas means more flight time.",
   P("sportscar", 960, 900, 1.6), P("tank", 700, 700, 0.35, at=0.2), P("tank", 960, 680, 0.35, at=0.35), P("tank", 1220, 700, 0.35, at=0.5),
   T("more gas = more air time", 960, 250, 70, "dark", at=0.7))
sc("Here's the clever part. Normal fast cars are limited by their tires. Push too hard, and the tires just spin.",
   P("car", 900, 900, 1.2), T("SPIN SPIN SPIN", 900, 450, 80, "orange", at=0.3, anim="shake"))
sc("Tesla claims the thrusters push four to five times harder than the tires could handle. So it simply goes around that limit.",
   {"bars": {"values": [1, 4.5], "labels": ["tires", "thrusters"], "colors": ["grey", "red"], "fmt": "{}x", "w": 650, "h": 420},
    "x": 860, "y": 820}, G(1550, "pointup", "shock", extras=DAVE, look=-1, at=0.6))
sc("There's also a fan system that sucks air from under the car. Tesla says it's strong enough to hold the car upside down, even standing still.",
   P("fan", 960, 760, 1.2), P("sportscar", 960, 300, 1.0, at=0.3), T("upside down?", 1550, 520, 70, "red", at=0.6))
sc("Which means, in theory, this is a car that could park on the ceiling. Please do not try this in a hospital car park.",
   G(600, "think", "worried", extras=LINDA), P("building", 1350, 900, 1.1, text="P", at=0.3), P("sportscar", 1350, 330, 0.5, at=0.55))
sc("In track mode, it lowers itself and pops out wings. Tesla says the downforce is approaching Formula One levels.",
   P("sportscar", 960, 900, 1.4, move=[960, 920]), {"arrow": [[960, 400], [960, 640]], "at": 0.4}, T("F1?", 1500, 360, 120, "red", at=0.6))

# PART 4: THREE VERSIONS ---------------------------------------------------------
sc("Now, the important fine print. There isn't one Roadster. There are three.",
   P("sportscar", 450, 900, 0.8), P("sportscar", 960, 900, 0.8, at=0.25), P("sportscar", 1470, 900, 0.8, at=0.5),
   chapter="Part 4: The fine print", bg="paper")
sc("The Performance version has two seats and goes from zero to sixty in under one point six seconds.",
   P("sportscar", 760, 900, 1.2, text="PERFORMANCE"), P("stopwatch", 1500, 900, 1.0, text="1.6s", at=0.4))
sc("The Thrust version adds thrusters at the back, and Tesla claims zero to sixty in under point nine seconds. It's a limited release.",
   P("sportscar", 760, 900, 1.2, text="THRUST"), P("stopwatch", 1500, 900, 1.0, text="0.9s", at=0.4), {"stamp": "LIMITED", "x": 760, "y": 450, "size": 70, "w": 260, "at": 0.7})
sc("And the Rocket version. One seat. Thrusters all around. Zero to sixty in under point five nine seconds, and over two hundred and thirty miles per hour.",
   P("sportscar", 760, 900, 1.2, text="ROCKET"), P("stopwatch", 1500, 900, 1.0, text="0.59s", at=0.3), T("230+ mph", 1500, 300, 90, "red", at=0.6))
sc("Point five nine seconds. You'd still be saying zero when it's already at sixty.",
   {"count": [0, 60], "fmt": "{:.0f}", "x": 960, "y": 420, "size": 260, "color": "red", "dur": 0.6}, G(1550, "panic", "shock", extras=DAVE, look=-1, at=0.4))
sc("But the Rocket is invite only. And Tesla's own Roadster page says it is not approved for public roads.",
   {"stamp": "INVITE ONLY", "x": 650, "y": 420, "size": 70, "w": 380}, {"stamp": "NOT FOR ROADS", "x": 1300, "y": 640, "size": 70, "w": 420, "at": 0.45},
   G(1700, "hips", "smug", extras=LINDA, look=-1, s=0.8, at=0.6))
sc("Tesla says all three can go more than three hundred miles on a charge.",
   {"count": [0, 300], "fmt": "{:.0f}+ miles", "x": 960, "y": 400, "size": 150, "color": "green", "dur": 1.8}, P("sportscar", 960, 900, 1.0, at=0.3))
sc("And on stage, Elon Musk said something unusually honest for a car launch: this is not necessarily a safety optimized car.",
   G(560, "present", "neutral", extras=CEO, label="Tesla's CEO"), P("speech", 1250, 480, 1.4, text="safety?", at=0.3), T("\"not necessarily a safety-optimized car\"", 1150, 200, 56, "red", at=0.45))
sc("Most car ads show a family laughing in the rain. This one showed a car doing a flip and said, maybe don't.",
   G(450, "wave", "happy", s=0.7), G(620, "wave", "happy", s=0.55), P("cloud", 540, 380, 1.0), {"cross": [540, 650, 160], "at": 0.4},
   P("sportscar", 1350, 700, 1.0, anim="spin", at=0.5))

# PART 5: PROMISES VS REALITY ----------------------------------------------------
sc("So how does the twenty twenty six car compare with what was promised in twenty seventeen? Let's put them side by side.",
   P("calendar", 600, 860, 1.0, text="2017"), T("vs", 960, 600, 120, "dark", at=0.3), P("calendar", 1320, 860, 1.0, text="2026", at=0.4),
   chapter="Part 5: Promise vs reality")
sc("Acceleration got better. The promise was one point nine seconds. Now even the basic version claims under one point six.",
   {"bars": {"values": [1.9, 1.6], "labels": ["2017 promise", "2026 claim"], "colors": ["grey", "green"], "fmt": "{}s", "w": 700, "h": 420},
    "x": 860, "y": 820}, G(1600, "fist", "grin", extras=DAVE, look=-1, at=0.6))
sc("Range went the other way. Six hundred and twenty miles became a bit over three hundred. Roughly half.",
   {"bars": {"values": [620, 300], "labels": ["2017 promise", "2026 claim"], "colors": ["grey", "red"], "fmt": "{} mi", "w": 700, "h": 420},
    "x": 860, "y": 820}, G(1600, "facepalm", "sad", extras=DAVE, look=-1, at=0.6))
sc("Top speed went from above two fifty to above two thirty. And four seats became two, or one.",
   T("250+ to 230+ mph", 960, 300, 90, "dark"), *[G(600 + i * 240, "stand", "happy", s=0.6, at=0.3) for i in range(4)],
   {"cross": [1200, 760, 110], "at": 0.6}, {"cross": [1440, 760, 110], "at": 0.7})
sc("So, depending on who you ask, this is either a promise beaten or a promise shrunk.",
   G(450, "fist", "grin", extras=["cap"]), G(1500, "hips", "angry", extras=LINDA, look=-1),
   P("scale", 960, 900, 1.1, at=0.3))
sc("Fred Lambert, at the electric car site Electrek, wrote: the engineering here is real.",
   G(560, "present", "neutral", extras=["glasses"], label="Fred Lambert, Electrek"), P("speech", 1250, 480, 1.5, text="real engineering", at=0.35))
sc("But he also pointed out that the wildest stunts belong to versions that are limited, invite only, or not road legal.",
   {"stamp": "LIMITED", "x": 500, "y": 420, "size": 60, "w": 260}, {"stamp": "INVITE ONLY", "x": 960, "y": 560, "size": 60, "w": 340, "at": 0.3},
   {"stamp": "NOT ROAD LEGAL", "x": 1420, "y": 700, "size": 60, "w": 420, "at": 0.6})
sc("He also guessed that using the stunt features would probably void the warranty. Which is fair. No warranty covers kickflips.",
   P("pricetag", 700, 700, 1.8, text="WARRANTY"), {"cross": [700, 600, 120], "at": 0.4}, P("sportscar", 1400, 650, 0.9, anim="spin", at=0.5))
sc("For the record, Lambert disclosed that he himself is waiting for a Roadster. So nobody here is neutral about this car. Not even the critics.",
   G(560, "stand", "tired", extras=["glasses"]), P("calendar", 1200, 860, 1.0, text="WAITING"), T("disclosure", 1200, 300, 80, "blue", at=0.5))

# PART 6: THE MONEY ---------------------------------------------------------------
sc("Now the question Dave actually cares about. What does it cost?",
   G(650, "hold", "worried", extras=DAVE), P("wallet", 1200, 760, 1.3, anim="shake", at=0.3), chapter="Part 6: The money")
sc("The answer: nobody knows. Tesla did not announce a price for any version.",
   P("pricetag", 960, 700, 1.8, text="$ ???"), G(1600, "shrug", "confused", extras=DAVE, look=-1, at=0.4))
sc("What Tesla did announce is how to reserve one. Five thousand dollars right away, which Tesla calls fully refundable.",
   {"count": [0, 5000], "fmt": "${:,.0f}", "x": 960, "y": 380, "size": 170, "color": "green", "dur": 1.4}, P("wallet", 960, 900, 1.0, at=0.4))
sc("Then forty five thousand more within ten days, or the reservation gets canceled.",
   {"count": [5000, 50000], "fmt": "${:,.0f}", "x": 960, "y": 380, "size": 170, "color": "red", "dur": 1.8},
   P("calendar", 1550, 860, 0.9, text="10 DAYS", at=0.4), G(450, "panic", "scream", extras=DAVE, at=0.5))
sc("That's fifty thousand dollars in total. Exactly the same deposit as in twenty seventeen. Prices on everything else went up, but not the deposit.",
   T("$50,000", 960, 300, 150, "dark"), P("calendar", 650, 860, 0.9, text="2017", at=0.3), T("=", 960, 700, 140, "dark", at=0.45),
   P("calendar", 1270, 860, 0.9, text="2026", at=0.5))
sc("One report says the more extreme Thrust version takes a two hundred and fifty thousand dollar reservation.",
   T("$250,000", 960, 380, 160, "red"), P("sportscar", 960, 900, 1.0, text="THRUST", at=0.4))
sc("And when can you drive it? Asked about production, Musk said: twenty twenty eight, actually.",
   G(560, "present", "neutral", extras=CEO, label="Tesla's CEO"), P("speech", 1200, 480, 1.4, text="2028, actually", at=0.3),
   P("calendar", 1650, 860, 0.9, text="2028", at=0.6))
sc("So if you reserve today, you'll have about two years to think about what you've done.",
   G(650, "think", "worried", extras=DAVE), {"count": [0, 2], "fmt": "~{:.0f} years", "x": 1300, "y": 420, "size": 130, "color": "blue", "dur": 1.5})
sc("Will it make Tesla a lot of money? Even Musk was careful. He said he's not sure it moves the needle massively on revenue.",
   P("chart", 960, 900, 1.2), G(400, "shrug", "neutral", extras=CEO, label="Tesla's CEO", at=0.3), T("needle?", 1550, 360, 90, "dark", at=0.6))
sc("A hypercar is a bit like a fancy bakery cake in the window. It doesn't pay the rent. It gets people through the door.",
   P("bread", 700, 860, 1.4, text="CAKE"), P("house", 1350, 900, 0.9, at=0.4), {"arrow": [[900, 700], [1180, 700]], "at": 0.5})

# PART 7: WHY SPACEX? --------------------------------------------------------------
sc("Which brings us to the last question. Why was a car launched at a rocket site?",
   P("sportscar", 700, 900, 1.0), P("rocket", 1300, 900, 1.2, at=0.3), T("?", 1000, 320, 180, "red", at=0.6), chapter="Part 7: Why SpaceX?")
sc("Tesla and SpaceX are separate companies. But the same person runs both.",
   P("building", 600, 900, 1.0, text="TESLA"), P("building", 1320, 900, 1.0, text="SPACEX", at=0.3),
   G(960, "shrug", "smug", extras=CEO, label="CEO of both", at=0.55))
sc("According to the reports, the thrusters were developed by SpaceX. Musk called the car the result of Tesla and SpaceX engineers working closely together.",
   G(560, "type", "happy", extras=ENG, label="Tesla"), G(1360, "type", "happy", extras=ENG, label="SpaceX", look=-1, at=0.2),
   P("tank", 960, 900, 0.9, text="thruster", at=0.5))
sc("That has fueled talk that the two companies could one day merge. CNBC reported the reveal added to that speculation.",
   P("building", 600, 900, 0.9, text="TESLA"), P("building", 1320, 900, 0.9, text="SPACEX"),
   {"arrow": [[760, 600], [1150, 600]], "at": 0.4}, T("merge?", 960, 300, 110, "blue", at=0.5))
sc("To be clear, nothing like that has been announced. For now, it's a car with some rocket parts, and a lot of people reading tea leaves.",
   {"stamp": "NOT ANNOUNCED", "x": 960, "y": 380, "size": 80, "w": 520}, P("coffee", 1500, 900, 1.0, text="tea", at=0.4),
   G(500, "think", "confused", extras=LINDA, at=0.5))
sc("Fans see it as engineering nobody else has tried. Skeptics see a marketing show for a car most people will never buy. We just count the facts.",
   G(450, "fist", "grin", extras=["cap"]), G(1500, "hips", "angry", extras=["glasses"], look=-1), P("scale", 960, 900, 1.1, at=0.3))

# WRAP UP --------------------------------------------------------------------
sc("Quick recap. After nine years of delays, Tesla showed its new Roadster on October fifteenth, with SpaceX built thrusters that let it jump and flip.",
   T("RECAP", 960, 200, 120, "blue"), P("sportscar", 960, 800, 1.1, anim="spin", at=0.3), chapter="Recap")
sc("It's faster than promised, but with roughly half the promised range, and the wildest versions are limited, invite only, or not road legal.",
   T("faster", 600, 420, 100, "green"), T("half the range", 1350, 420, 100, "red", at=0.35), P("sportscar", 960, 900, 0.9, at=0.5))
sc("There's no price yet, a fifty thousand dollar reservation, and production promised for twenty twenty eight.",
   P("pricetag", 500, 760, 1.0, text="???"), T("$50,000", 960, 420, 100, "dark", at=0.3), P("calendar", 1450, 860, 0.9, text="2028", at=0.6))
sc("As for Dave, he has decided to keep waiting. He's already waited nine years. What's two more?",
   G(700, "stand", "tired", extras=DAVE + ["sweat"]), P("calendar", 1300, 860, 1.0, text="2028"), T("zzz", 1000, 400, 90, "blue", at=0.5, anim="bob"))
sc("Meanwhile, Linda bought a bicycle. It goes zero to sixty in about never. It was available the same day.",
   G(500, "hips", "smug", extras=LINDA), P("wallet", 1000, 760, 0.8, at=0.3), T("0 to 60: never", 1400, 380, 80, "dark", at=0.5),
   G(1500, "facepalm", "tired", extras=DAVE, look=-1, s=0.8, at=0.7))
sc("Would you put fifty thousand dollars down on a car that flips? Tell us in the comments, and subscribe so you'll know when it actually ships.",
   P("speech", 960, 460, 1.8, text="would you?"), G(400, "wave", "happy", extras=DAVE, at=0.4), P("sportscar", 1500, 900, 0.8, at=0.6))

script = {
    "id": "ep002",
    "title": "Tesla's Roadster Finally Arrived. Can It Really Fly?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Nine years after it was first shown, Tesla revealed the new Roadster on October 15, 2026, at SpaceX's test site near Waco, Texas. "
        "It uses SpaceX-developed cold-gas thrusters to jump and even kickflip. Here's what was actually shown, explained with stick figures: "
        "the 2017 promises, how a car 'flies', the three versions, promise vs reality, the $50,000 reservation, the 2028 production date, "
        "and why everyone is talking about SpaceX.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "CNBC, Tesla unveils long-delayed Roadster developed with SpaceX: https://www.cnbc.com/2026/10/15/tesla-roadster-reveal-what-to-know-about-the-delayed-ev.html\n"
        "Electrek, Tesla unveils Cyberfied new Roadster: https://electrek.co/2026/10/15/tesla-unveils-cyberfied-new-roadster-kickflip/\n"
        "The Detroit News, Tesla Roadster second generation: https://www.detroitnews.com/story/business/autos/2026/10/15/tesla-roadster-second-generation-revealed/92272421007/\n"
        "The EV Report, Tesla unveils production Roadster with SpaceX cold-gas thrusters: https://theevreport.com/tesla-roadster-unveil-spacex-cold-gas-thrusters\n"
        "Wikipedia, Tesla Roadster (second generation), 2017 background: https://en.wikipedia.org/wiki/Tesla_Roadster_(second_generation)\n\n"
        "#tesla #roadster #explained #news #stickfigure"
    ),
    "tags": ["tesla roadster", "tesla", "roadster reveal", "flying car", "cold gas thrusters", "spacex", "electric car",
             "tesla news", "news explained", "stick figure animation", "hypercar", "elon musk"],
    "thumbnail": {"bg": "yellow", "text": "IT CAN|FLY?!", "size": 210, "color": "black",
                  "guy": {"pose": "panic", "face": "scream", "look": 1, "extras": ["hair"]},
                  "items": [{"prop": "sportscar", "x": 1550, "y": 760, "s": 1.3, "text": "9 YEARS LATE"}], "guy_x": 1150},
    "scenes": [s for s in S if s],
}
for s in script["scenes"]:
    for it in list(s["items"]):
        g = it.get("guy")
        if g and g.get("label"):  # draw labels above the head so they never collide with subtitles
            sz = it.get("s", 1.0)
            s["items"].append({"text": g.pop("label"), "x": it["x"], "y": it.get("y", 900) - int(430 * sz), "size": 44,
                               "color": "dark", "at": it.get("at", 0)})
    for it in s["items"]:
        if "in_" in it:
            it["in"] = it.pop("in_")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep002.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

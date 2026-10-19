"""Episode 8: Starlink / Starshield speed limit on Ukraine (Oct 14-18, 2026), explained with stick figures."""
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



PRES_UA = dict(extras=["tie"], shirt="blue")      # Ukraine's president (generic)
PRES_US = dict(extras=["tie"], shirt="navy")      # the U.S. president (generic)
SEC = dict(extras=["tie", "briefcase"], shirt="grey")
BOSS = dict(extras=["cap"], shirt="dark")         # SpaceX's founder (generic)
SOLDIER = dict(extras=["hardhat"], shirt="green")

# COLD OPEN --------------------------------------------------------------------
sc("Dave bought a satellite dish for his car roof. Internet from space, anywhere. Dave is thrilled.",
   P("car", 900, 900, 1.3), P("dish", 900, 735, 0.6, at=0.2), G(1450, "fist", "grin", extras=DAVE, at=0.4),
   P("satellite", 400, 420, 0.7, at=0.55, anim="bob"), cam={"from": [960, 600, 1.25], "to": [960, 540, 1.0]})
sc("Dave hits the highway. Sixty miles an hour. Video call: perfect. Eighty: perfect. Ninety-nine: perfect.",
   P("car", 700, 900, 1.0, move=[1100, 900]), C(60, 99, 1400, 360, fmt="{:.0f} mph", size=150, color="dark", dur=2.6))
sc("One hundred and one miles an hour. The call freezes. Dave's face is stuck, mid-sneeze, forever.",
   T("101 mph", 1400, 300, 150, "red"), P("laptop", 900, 860, 1.1, text="RECONNECTING...", at=0.25),
   G(1500, "panic", "scream", extras=DAVE, anim="shake", at=0.5), bg="yellow")
sc("A speed limit. On internet from space. That sounds made up. This week, Ukraine says it happened to its drones.",
   P("sign", 600, 900, 1.2, text="100"), P("satellite", 1100, 420, 0.7, at=0.25), P("drone", 1500, 700, 1.0, at=0.5, anim="bob"))
S.append({"say": "So today's question: who put a speed limit on space internet, and why does it matter so much? Facts only, stick figures included.",
          "items": [P("tv", 980, 800, 1.4, text="WHO SET THE LIMIT?"), G(330, "wave", "happy", extras=DAVE, at=0.4)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED -----------------------------------------------------------
sc("Tuesday night, October thirteenth into the fourteenth. Ukrainian officials say satellite terminals moving fast suddenly started losing their connection.",
   P("calendar", 600, 860, 1.1, text="OCT 14"), P("dish", 1300, 900, 1.0, at=0.3), {"cross": [1300, 700, 110], "at": 0.6},
   chapter="Part 1: What happened")
sc("The cut-off point, they say, was about one hundred and sixty kilometers an hour. That's roughly one hundred miles an hour.",
   C(0, 160, 700, 420, fmt="{:.0f} km/h", size=170, color="red"), P("sign", 1450, 900, 1.0, text="100", at=0.45))
sc("Before that, Ukrainian officials say, the same systems worked on drones flying at up to four hundred kilometers an hour.",
   {"bars": {"values": [400, 160], "labels": ["before", "after"], "colors": ["green", "red"], "fmt": "{} km/h", "w": 760, "h": 440},
    "x": 900, "y": 830}, P("drone", 1600, 520, 0.8, at=0.5, anim="bob"))
sc("Serhiy Beskrestnov, a defence technology adviser in Ukraine, said the limit arrived with no warning.",
   G(600, "present", "worried", extras=ECON, label="Ukrainian tech adviser"), P("envelope", 1300, 820, 1.1, text="NO WARNING", at=0.35),
   {"cross": [1300, 700, 120], "at": 0.6})
sc("Parked terminals kept working. Slow ones kept working. Only the fast-moving ones dropped out.",
   P("dish", 450, 900, 0.8), T("OK", 450, 560, 90, "green", at=0.1), P("car", 960, 900, 0.8, at=0.25), T("OK", 960, 560, 90, "green", at=0.35),
   P("drone", 1500, 700, 0.9, at=0.5), T("DROP", 1500, 420, 90, "red", at=0.65))
sc("And in this war, the fast-moving things are often drones.",
   *[P("drone", 400 + k * 380, 500 + (k % 2) * 160, 0.6, at=0.1 * k, anim="bob") for k in range(4)], ground=False)

# PART 2: STARLINK VS STARSHIELD ----------------------------------------------------
sc("First, a quick vocabulary lesson, because two very similar names are doing a lot of work here.",
   P("chalkboard", 960, 900, 1.2, text="WORDS"), G(400, "point", "neutral", extras=LINDA, at=0.3), chapter="Part 2: Two names")
sc("Starlink is the commercial service from SpaceX. You buy a dish, point it at the sky, and get internet from satellites.",
   T("STARLINK", 960, 260, 120, "blue"), P("dish", 650, 900, 1.0, at=0.2), P("satellite", 1300, 560, 0.8, at=0.4, anim="bob"))
sc("Around ten thousand Starlink satellites are now in orbit, according to Reuters. That's a lot of very small, very fast neighbours.",
   C(0, 10000, 960, 360, fmt="~{:,.0f}", size=200, color="navy"), *[P("satellite", 300 + k * 330, 720, 0.35, at=0.3 + 0.07 * k) for k in range(5)],
   ground=False, bg="sky")
sc("In Ukraine, there are around fifty thousand Starlink terminals, according to Germany's DW. Soldiers on the front line use them, and so do civilians.",
   C(0, 50000, 960, 380, fmt="~{:,.0f}", size=200, color="blue"), G(500, "stand", "neutral", **SOLDIER, at=0.35), P("house", 1450, 900, 0.7, at=0.5))
sc("Starshield is the military version. Same idea, extra security, built for governments.",
   T("STARSHIELD", 960, 260, 120, "dark"), P("satellite", 960, 720, 1.0, color="dark", at=0.25), P("lock", 1450, 880, 0.7, at=0.5))
sc("And here's the important part. SpaceX's founder wrote on X that Starshield is owned and controlled by the U.S. government.",
   G(600, "present", "neutral", **BOSS, label="SpaceX's founder"), P("phone", 1300, 880, 1.1, text="POST", at=0.35))
sc("His words: any limits on speed or usage are decided by the U.S. military, and ultimately the president.",
   P("speech", 960, 600, 1.7, text="\"ultimately POTUS\""), G(400, "point", "neutral", **BOSS, at=0.2), G(1550, "stand", "confused", **PRES_US, look=-1, at=0.5))
sc("So, two products. One belongs to a company. One, he says, is steered by the government. Hold that thought. It matters later.",
   T("COMPANY", 600, 400, 100, "blue"), T("GOVERNMENT", 1350, 400, 100, "dark", at=0.3), {"arrow": [[800, 560], [1150, 560]], "color": "grey", "at": 0.5})

# PART 3: WHY SPEED MATTERS --------------------------------------------------------
sc("Why would a speed limit matter so much? Because of what Ukraine's drones are chasing.",
   P("stopwatch", 960, 900, 1.1), G(450, "think", "confused", extras=DAVE, at=0.3), chapter="Part 3: Why speed matters")
sc("Russia sends attack drones toward Ukrainian cities. Some newer ones, called Shaheds, are jet-powered, and they are fast.",
   P("drone", 1400, 450, 0.9, color="red", move=[700, 500]), T("JET-POWERED", 960, 250, 90, "red", at=0.4), ground=False, bg="sky")
sc("Ukraine fights back with interceptor drones, small hunters steered by an operator on the ground, often through Starlink.",
   G(450, "type", "neutral", **SOLDIER), P("dish", 800, 900, 0.7, at=0.2), {"arrow": [[900, 640], [1300, 460]], "color": "dark", "at": 0.4},
   P("drone", 1450, 450, 0.8, at=0.5, anim="bob"))
sc("To catch something fast, you have to go fast. And Ukraine's president said that at about one hundred and sixty one kilometers an hour, the link simply dropped.",
   G(600, "present", "worried", **PRES_UA, label="Ukraine's president"), T("161 km/h", 1350, 360, 140, "red", at=0.3), P("drone", 1350, 760, 0.7, at=0.5))
sc("When the link drops, the operator loses control. The hunter keeps flying, but nobody is driving it anymore.",
   P("drone", 1300, 500, 0.9, anim="spin"), P("laptop", 600, 900, 0.9, text="NO SIGNAL", at=0.3), ground=False)
sc("Axios reported that the restrictions hampered Ukraine's ability to intercept Russian attack drones for about twenty four hours.",
   C(0, 24, 960, 400, fmt="{:.0f} hours", size=200, color="red"), P("calendar", 1550, 880, 0.8, text="24H", at=0.4))
sc("Several deadly Russian strikes hit Ukraine on Tuesday, after the network slowed down.",
   P("calendar", 960, 860, 1.1, text="TUESDAY", color="grey"), bg="paper")
sc("Ukraine says the limits also affected supply drones that carry food and water to positions vehicles can't reach.",
   P("drone", 900, 480, 0.9, text="FOOD + WATER", at=0.0, anim="bob"), G(1450, "stand", "worried", **SOLDIER, at=0.4))

# PART 4: THE ROAD TEST --------------------------------------------------------------
sc("Now, SpaceX told Ukraine this was a technical problem, according to a Ukrainian official. Ukraine decided to test that, in a very practical way.",
   P("clipboard", 600, 900, 1.0, text="TEST"), G(1300, "think", "smug", extras=LINDA, at=0.35), chapter="Part 4: The road test")
sc("Ukraine's president said they sent a couple of Starlink-equipped vehicles into countries of the European Union.",
   P("car", 600, 900, 0.9), P("dish", 600, 770, 0.4, at=0.1), P("car", 1200, 900, 0.9, at=0.2), P("dish", 1200, 770, 0.4, at=0.3),
   T("EU", 1600, 400, 160, "blue", at=0.45))
sc("They drove at one hundred and eighty kilometers an hour. Starlink kept working.",
   P("car", 400, 900, 1.0, move=[1500, 900]), C(0, 180, 960, 330, fmt="{:.0f} km/h", size=170, color="green", dur=2.0), T("ONLINE", 960, 520, 90, "green", at=0.6))
sc("So, his conclusion: the restrictions apply on Ukrainian territory. In his words, it is a planned operation.",
   G(600, "point", "angry", **PRES_UA, label="Ukraine's president"), P("speech", 1300, 560, 1.6, text="\"planned operation\"", at=0.3))
sc("Somewhere, a very fast test driver is still explaining to his insurance company that it was for national security.",
   G(700, "shrug", "grin", extras=["cap"], at=0), P("clipboard", 1300, 900, 1.0, text="CLAIM", at=0.35), bg="yellow")
sc("By Wednesday, Axios reported, service was partially restored. A day later, defence ministry sources told the Ukrainian outlet Babel it was working again.",
   P("calendar", 600, 860, 1.0, text="OCT 14-15"), P("dish", 1250, 900, 1.0, at=0.3), T("BACK?", 1250, 520, 100, "green", at=0.5))
sc("But on Friday and Saturday, Ukraine's president said the restrictions were still in place. So, depending on who you ask, it's fixed, or it isn't.",
   T("FIXED", 600, 400, 120, "green"), T("NOT FIXED", 1350, 400, 120, "red", at=0.3), G(960, "shrug", "confused", extras=DAVE, at=0.5))

# PART 5: WHO DID IT? -----------------------------------------------------------------
sc("And now the real mystery. Who actually flipped the switch?",
   P("lock", 960, 900, 1.3, text="?"), chapter="Part 5: Who flipped the switch?", cam={"from": [960, 640, 1.3], "to": [960, 540, 1.0]})
sc("A Ukrainian official gave Axios a summary that sounds like a very bad customer service call.",
   P("phone", 700, 900, 1.2, text="HOLD..."), G(1300, "facepalm", "tired", extras=ECON, label="Ukrainian official", at=0.3))
sc("Quote: SpaceX tells us it is a technical problem. But our contacts in the company say it is coming from the White House.",
   T("SpaceX: \"technical\"", 960, 360, 90, "blue"), {"arrow": [[700, 560], [1220, 560]], "color": "dark", "at": 0.5}, T("WHITE HOUSE", 1350, 700, 80, "dark", at=0.6))
sc("When we ask the White House, they say it is Elon. End quote.",
   T("WHITE HOUSE: \"Elon\"", 960, 400, 90, "dark"), P("capitol", 600, 900, 0.7, at=0.2), {"arrow": [[900, 600], [1400, 600]], "at": 0.45})
sc("SpaceX's founder, as we heard, said limits on Starshield are decided by the military and ultimately the president. So everyone is pointing.",
   G(450, "point", "neutral", **BOSS, label="SpaceX"), G(960, "point", "neutral", **PRES_US, label="White House", at=0.2),
   G(1470, "point", "neutral", **PRES_UA, look=-1, label="Ukraine", at=0.4))
sc("It's a perfect triangle of pointing. Geometry teachers everywhere are quietly delighted.",
   {"arrow": [[600, 450], [900, 300]], "color": "red"}, {"arrow": [[1050, 300], [1350, 450]], "color": "red", "at": 0.2},
   {"arrow": [[1300, 600], [650, 600]], "color": "red", "at": 0.4}, G(1600, "hips", "smug", extras=["glasses"], label="geometry teacher", at=0.6), bg="yellow")
sc("Then on Thursday, Reuters reported that the order to limit Starshield for Ukraine came from inside the White House.",
   P("envelope", 700, 860, 1.1, text="ORDER"), P("capitol", 1350, 900, 0.8, at=0.3))
sc("Reuters cited two U.S. officials and one Western official. They said Pentagon leaders got a message that the service for Ukraine needed to be slowed.",
   *[G(450 + k * 300, "stand", "neutral", extras=["tie"], s=0.75, at=0.1 * k) for k in range(3)], P("envelope", 1500, 820, 0.9, text="SLOW IT", at=0.45))
sc("On Friday, Britain's Telegraph went further. Citing four sources, it reported that SpaceX's founder suggested the speed limits, and the president agreed.",
   C(0, 4, 600, 420, fmt="{:.0f} sources", size=130, color="dark"), G(1100, "present", "neutral", **BOSS, at=0.3), G(1550, "stand", "neutral", **PRES_US, look=-1, at=0.45))
sc("The other side says the opposite. On Friday, the president told reporters: I just checked this morning, it wasn't us.",
   G(700, "present", "neutral", **PRES_US, label="the U.S. president"), P("speech", 1350, 560, 1.6, text="\"it wasn't us\"", at=0.3))
sc("He also said: it wasn't me, and I don't think it was Elon. And from what I understand, it's the same as it's always been.",
   P("speech", 960, 520, 1.8, text="\"it wasn't me\""), G(1600, "shrug", "neutral", **PRES_US, look=-1, at=0.3))
sc("This weekend, Secretary of State Marco Rubio said nobody ordered the slowdown. It wasn't deliberate, he said. It sort of happened.",
   G(650, "present", "neutral", **SEC, label="Secretary of State"), P("speech", 1300, 560, 1.6, text="\"sort of happened\"", at=0.35))
sc("He added that, as he understood it, the speed was restored and back to where it was before.",
   P("dish", 960, 900, 1.0), T("RESTORED?", 960, 480, 110, "green", at=0.3))
sc("He also said Ukraine doesn't currently have access to Starshield, and that Kyiv has asked for it for long-range strikes. That, he said, is still being discussed.",
   P("lock", 700, 900, 1.0, text="STARSHIELD"), T("UNDER DISCUSSION", 1300, 420, 80, "orange", at=0.4))
sc("So: anonymous sources on one side, named officials denying it on the other. We can't tell you who's right. We just count the claims.",
   P("scale", 960, 900, 1.2), T("SOURCES", 600, 380, 80, "dark", at=0.2), T("DENIALS", 1320, 380, 80, "dark", at=0.35))

# PART 6: THE BACKGROUND --------------------------------------------------------------
sc("Why would anyone want to slow Ukraine down? There's no confirmed answer. But here's the background reporters keep pointing to.",
   P("globe", 960, 880, 1.2), G(450, "think", "neutral", extras=LINDA, at=0.3), chapter="Part 6: The background")
sc("Ukraine has been striking Russian oil refineries. And days earlier, Axios reported, the U.S. agreed to lift sanctions on Russian oil sales.",
   P("fire", 600, 900, 0.8), P("barrel", 1300, 900, 0.9, text="RUSSIAN OIL", at=0.3), {"cross": [1300, 760, 120], "color": "green", "at": 0.5})
sc("Ukraine's president criticised that decision. Washington and Kyiv have been at odds since.",
   G(650, "point", "angry", **PRES_UA), G(1300, "hips", "angry", **PRES_US, look=-1, at=0.3), T("TENSION", 960, 300, 100, "red", at=0.5))
sc("Critics see the slowdown as payback. The White House says it had nothing to do with it. Both claims are out there. Neither has been proven.",
   T("PAYBACK?", 600, 420, 110, "red"), T("NOTHING TO DO WITH IT", 1300, 420, 70, "dark", at=0.3), P("scale", 960, 900, 0.9, at=0.5))

# PART 7: EUROPE'S BACKUP PLAN -----------------------------------------------------------
sc("Meanwhile, money noticed. On Wednesday, shares in Eutelsat, a European satellite company, jumped twenty three percent.",
   C(0, 23, 960, 380, fmt="+{:.0f}%", size=230, color="green"), P("chart", 1550, 900, 0.8, text="EUTELSAT", at=0.4), chapter="Part 7: Europe's backup plan")
sc("Reuters said it was the stock's biggest one-day gain in sixteen months. Investors bet that Europe might want its own space internet.",
   P("arrowup", 700, 860, 1.2, color="green"), T("16 MONTHS", 1350, 420, 100, "dark", at=0.3))
sc("Eutelsat runs OneWeb, the only other company with this kind of low-orbit internet service. Its network has more than six hundred satellites.",
   T("ONEWEB", 960, 260, 110, "purple"), C(0, 600, 960, 480, fmt="{:.0f}+", size=170, color="purple", at=0.2), ground=False, bg="sky")
sc("Starlink has around ten thousand. That's like a corner shop competing with a supermarket that's also on the moon.",
   {"bars": {"values": [600, 10000], "labels": ["OneWeb", "Starlink"], "colors": ["purple", "blue"], "fmt": "{:,}", "w": 760, "h": 440},
    "x": 900, "y": 830}, G(1650, "facepalm", "tired", extras=DAVE, at=0.5))
sc("And you can't just switch. A satellite consultant told Reuters that moving over would need large numbers of new terminals on the ground.",
   P("dish", 500, 900, 0.8), {"arrow": [[700, 700], [1200, 700]], "color": "dark", "at": 0.3}, P("dish", 1400, 900, 0.8, color="purple", at=0.4), T("NEW KIT", 960, 380, 90, "orange", at=0.6))
sc("Europe is also arguing about the radio waves themselves. The European Commission proposed reserving part of the spectrum for European companies.",
   P("building", 700, 900, 0.9, text="EU"), T("RADIO WAVES", 1350, 400, 90, "blue", at=0.3), {"ring": [1350, 400, 220], "color": "blue", "at": 0.5})
sc("According to the Financial Times, the U.S. ambassador to the EU called that protectionism. SpaceX warned it could hurt connectivity in Ukraine.",
   G(650, "point", "angry", **SEC, label="U.S. ambassador to the EU"), P("speech", 1350, 560, 1.5, text="\"protectionism\"", at=0.35))
sc("The Commission says companies from outside the EU could still operate. It just wants more European providers in the market.",
   G(700, "present", "neutral", extras=["glasses", "tie"], label="the Commission"), P("building", 1350, 900, 0.8, text="MORE CHOICE", at=0.35))
sc("And Ukraine's president says Ukraine is developing its own satellite system, while Europe works on an alternative.",
   P("rocket", 700, 900, 1.0, text="UA", anim="bob"), P("rocket", 1250, 900, 1.0, text="EU", at=0.3, anim="bob"), ground=True)

# PART 8: WHY THIS MATTERS -------------------------------------------------------------
sc("So why should Dave, sitting at home with his car parked, care about any of this?",
   P("house", 960, 900, 0.9), G(500, "stand", "confused", extras=DAVE, at=0.3), P("car", 1450, 900, 0.7, at=0.4), chapter="Part 8: Why it matters")
sc("Because this is a story about one company's network becoming the backbone of a whole country at war.",
   P("satellite", 960, 400, 1.0), *[{"arrow": [[960, 480], [400 + k * 370, 820]], "color": "grey", "at": 0.2 + 0.1 * k} for k in range(4)], ground=False)
sc("When a single switch can change how a military fights, the question of who holds that switch becomes very, very important.",
   P("lock", 960, 880, 1.3, text="SWITCH"), {"ring": [960, 720, 230], "color": "red", "at": 0.4})
sc("Governments everywhere are watching. If your phones, your banks or your army run on someone else's network, you start asking for a backup.",
   P("phone", 500, 900, 0.8), P("building", 960, 900, 0.7, text="BANK", at=0.2), G(1450, "stand", "worried", **SOLDIER, at=0.4))
sc("Linda's version: never keep your only spare key in somebody else's pocket.",
   G(700, "hips", "smug", extras=LINDA), P("lock", 1300, 880, 0.9, text="KEY", at=0.3), bg="yellow")

# WHAT'S NEXT ---------------------------------------------------------------------------
sc("What happens next? Three things to watch.",
   T("WHAT'S NEXT", 960, 400, 140, "dark"), chapter="What's next")
sc("One: whether Ukraine's drones really get their full speed back. Kyiv and Washington are giving different answers.",
   T("1", 400, 400, 200, "blue"), P("drone", 1100, 600, 1.0, anim="bob"), P("stopwatch", 1600, 900, 0.7, at=0.4))
sc("Two: whether Ukraine gets the access to Starshield it is asking for. Rubio says that's under discussion.",
   T("2", 400, 400, 200, "blue"), P("lock", 1100, 900, 1.0, text="STARSHIELD", at=0.2))
sc("Three: whether Europe really builds its own space internet, and how long that takes. Satellites don't grow overnight.",
   T("3", 400, 400, 200, "blue"), P("rocket", 1100, 900, 1.0, at=0.2, anim="bob"), P("calendar", 1600, 860, 0.7, text="2030?", at=0.45))

# RECAP --------------------------------------------------------------------------------
sc("Recap. This week, Ukraine says satellite terminals on fast-moving drones started dropping out above about one hundred and sixty kilometers an hour.",
   T("160 km/h", 700, 420, 160, "red"), P("drone", 1450, 650, 0.9, anim="bob"), chapter="Recap")
sc("Reuters and the Telegraph reported the order came from the White House. The president and his Secretary of State deny it. SpaceX's founder says it's the government's call.",
   P("capitol", 600, 900, 0.7), T("REPORTED", 600, 380, 80, "dark", at=0.2), T("DENIED", 1350, 380, 100, "red", at=0.4))
sc("And Europe's satellite company had its best day in sixteen months, because suddenly everyone wants a backup.",
   T("+23%", 600, 420, 160, "green"), P("satellite", 1350, 600, 0.9, color="purple", at=0.3, anim="bob"))
sc("Meanwhile, Dave has a new rule. On the highway, he drives at ninety nine miles an hour. Not a single mile more. For the internet.",
   P("car", 600, 900, 1.0, move=[1100, 900]), P("dish", 600, 770, 0.45, move=[1100, 770]), P("sign", 1600, 900, 1.0, text="99", at=0.3), bg="yellow")
sc("Linda would like everyone to know that Dave's actual speed limit is sixty five. She's checked.",
   G(700, "hips", "smug", extras=LINDA), P("sign", 1300, 900, 1.0, text="65", at=0.3))
sc("Your turn: should any single company control internet a whole country depends on? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("satellite", 1250, 600, 1.0, text="?", at=0.3, anim="bob"))
sc("And if calm stick figures explaining the news is your kind of thing, subscribe. We'll keep counting the facts, at a sensible speed.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep008",
    "title": "Why Does Ukraine's Space Internet Have a Speed Limit?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "This week Ukraine said its Starlink and Starshield satellite terminals started dropping out when moving faster than about "
        "160 km/h (100 mph), which hit the interceptor drones it uses against fast Russian attack drones. Who ordered it? SpaceX's "
        "founder says Starshield limits are decided by the U.S. military and ultimately the president; Reuters and the Telegraph "
        "reported the order came from the White House; the President and the Secretary of State deny it. Plus: why Europe's "
        "Eutelsat jumped 23%, and what to watch next. Explained with stick figures, facts only.\n\n"
        "Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported.\n\n"
        "Sources:\n"
        "Axios, Zelensky says Musk-owned satellite system still restricted in Ukraine (Oct 17, 2026): https://www.axios.com/2026/10/17/zelensky-starlink-elon-musk-trump\n"
        "Axios, Trump: White House didn't impede satellite system in Ukraine (Oct 16, 2026): https://www.axios.com/2026/10/16/trump-starlink-musk-ukraine-zelensky\n"
        "Reuters, Order to limit Starshield for Ukraine came from inside White House, sources say (Oct 15, 2026): https://www.reuters.com/world/europe/order-limit-starshield-ukraine-came-inside-white-house-sources-say-2026-10-15\n"
        "Reuters via Euronext, Eutelsat shares jump as Ukraine flags curbs on Starlink military-grade service (Oct 14, 2026): https://live.euronext.com/en/financial-news/eutelsat-shares-jump-ukraine-flags-curbs-starlink-military-grade-service\n"
        "CNBC, Trump denies Musk claim he ordered Starlink restrictions in Ukraine (Oct 16, 2026): https://www.cnbc.com/2026/10/16/trump-denies-musk-claim-he-ordered-starlink-restrictions-in-ukraine.html\n"
        "Mediaite (citing The Telegraph), Musk pitched cuts to Ukraine's Starshield to Trump (Oct 16, 2026): https://www.mediaite.com/media/news/musk-pitched-cuts-to-ukraines-starshield-direct-to-trump-who-then-agreed-report/\n"
        "RBC-Ukraine, Zelenskyy calls Starlink restrictions a planned operation (Oct 17, 2026): https://newsukraine.rbc.ua/news/zelenskyy-calls-starlink-restrictions-in-1792243118.html\n"
        "Babel, Rubio says White House did not order restrictions (Oct 18, 2026): https://babel.ua/en/news/131058-the-us-secretary-of-state-says-white-house-did-not-order-restrictions-on-starlink-operations-in-ukraine-and-ukraine-never-had-access-to-starshield\n"
        "DW, Why Starlink matters in Ukrainian warfare (Oct 18, 2026): https://www.dw.com/en/why-starlink-is-so-important-for-ukraine/a-79689729\n"
        "RBC-Ukraine (citing the Financial Times), US fears Starlink restrictions in Europe (Oct 18, 2026): https://newsukraine.rbc.ua/news/us-fears-starlink-restrictions-in-europe-1792352863.html\n\n"
        "#starlink #ukraine #spacex #starshield #explained #stickfigure #news"
    ),
    "tags": ["starlink", "starshield", "starlink ukraine", "starlink speed limit", "spacex", "ukraine drones", "eutelsat",
             "oneweb", "satellite internet", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "SPACE|SPEED|LIMIT?", "size": 190, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["hair"]}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
                  "items": [{"prop": "satellite", "x": 1460, "y": 330, "s": 0.85}]},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep008.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

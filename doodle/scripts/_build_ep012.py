"""Episode 12: About 3.2 million Medicare Advantage members must find new plans for 2027 (Humana/UnitedHealthcare cuts, Oct 2026), explained with stick figures."""
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
RUTH = dict(extras=["bun", "glasses"], shirt="purple")                     # Linda's mum, made-up character
INS = dict(extras=["tie", "briefcase"], shirt="navy", label="an insurer")   # generic insurer
GOV = dict(extras=["tie", "briefcase"], shirt="grey", label="Medicare agency")
WATCH = dict(extras=["glasses", "tie"], shirt="green", label="a watchdog")
EXPERT = dict(extras=["glasses"], shirt="teal", label="an economist")
KFF = dict(extras=["glasses"], shirt="orange", label="a KFF researcher")

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN --------------------------------------------------------------------
sc("Meet Ruth. Seventy-three. Linda's mum. Ruth has a system: the same chair, the same doctor, the same pharmacy, and the same health plan since twenty nineteen.",
   G(560, "hips", "happy", **RUTH), P("house", 1350, 900, 0.9, at=0.3), P("clipboard", 1700, 860, 0.7, text="SYSTEM", at=0.55),
   cam={"from": [600, 600, 1.3], "to": [960, 540, 1.0]})
sc("This week a letter arrives. Ruth reads it twice. Then she reads it with her other glasses.",
   P("envelope", 700, 820, 1.3, anim="shake"), G(1350, "think", "confused", look=-1, **RUTH, at=0.35))
sc("It says, in very polite words, that her plan will not exist next year.",
   P("envelope", 600, 820, 1.0), T("YOUR PLAN:", 1250, 330, 100, "dark", at=0.3), {"stamp": "GONE IN 2027", "x": 1250, "y": 520, "size": 70, "w": 520, "at": 0.55})
sc("Ruth calls Linda. Linda calls Dave, because Dave once read a pamphlet. Dave has never read a pamphlet.",
   P("phone", 450, 860, 0.9), G(960, "shrug", "worried", extras=LINDA, at=0.3), G(1500, "panic", "shock", look=-1, extras=DAVE, at=0.55))
sc("Ruth is not alone. About three point two million people will get a letter like that for twenty twenty-seven.",
   C(0, 3.2, 960, 380, fmt="{:.1f} million", size=170, color="red", dur=2.0), P("envelope", 1650, 860, 0.8, at=0.5), bg="yellow")
S.append({"say": "So today's question: why are millions of seniors losing their health plans, who is cutting, and what can they actually do before December seventh? Facts only. Stick figures, obviously.",
          "items": [P("tv", 980, 800, 1.4, text="WHY?"), G(330, "think", "confused", extras=DAVE, at=0.4), P("calendar", 1650, 860, 0.7, text="DEC 7", at=0.6)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED ----------------------------------------------------------
sc("On Thursday, CBS News reported that two of the biggest insurers, Humana and UnitedHealthcare, are ending some Medicare Advantage plans from next year.",
   P("building", 650, 900, 0.9, text="HUMANA"), P("building", 1300, 900, 0.9, text="UNITED", at=0.35), P("tv", 1700, 800, 0.6, text="CBS", at=0.6),
   chapter="Part 1: What happened")
sc("Humana told CBS, quote: we anticipate plan exits for twenty twenty-seven will impact approximately six hundred thousand members.",
   G(560, "present", "neutral", **INS), C(0, 600000, 1250, 380, fmt="{:,.0f}", size=150, color="red", at=0.35))
sc("UnitedHealthcare is closing one plan with roughly three hundred ninety thousand members. Together, that's about one million people.",
   C(0, 390000, 700, 360, fmt="{:,.0f}", size=140, color="red"), T("+ 600,000", 1350, 360, 110, "red", at=0.35), T("= ~1 MILLION", 1050, 560, 130, "dark", at=0.6))
sc("Both companies say most of those people will be offered another plan. But a different plan can mean different doctors, different drug lists and different bills.",
   P("clipboard", 500, 860, 1.0, text="NEW PLAN"), P("building", 1050, 900, 0.7, text="CLINIC", at=0.3), P("pricetag", 1550, 860, 1.0, text="$?", at=0.55))
sc("And it's not just those two. An analysis by Jared Strock of Medicare Market Insights counts nearly three point two million people whose plans are discontinued.",
   G(560, "present", "neutral", extras=["glasses"], shirt="dark", label="an analyst"), C(0, 3.2, 1250, 380, fmt="{:.1f}M", size=190, color="red", at=0.35))
sc("That's about eleven percent of people in individual Medicare Advantage plans. Roughly one in nine.",
   C(0, 11, 700, 380, fmt="{:.0f}%", size=220, color="red"), T("1 in 9", 1350, 380, 160, "dark", at=0.4))
sc("And it keeps growing. Two million lost their plans for twenty twenty-five. Just under three million for twenty twenty-six. Now three point two.",
   {"bars": {"values": [2.0, 2.9, 3.2], "labels": ["2025", "2026", "2027"], "colors": ["grey", "orange", "red"], "fmt": "{}M", "w": 760, "h": 460},
    "x": 960, "y": 860})
sc("Ruth's letter, it turns out, is part of a third year of turmoil. Ruth would like the turmoil to happen to someone younger.",
   P("envelope", 600, 820, 0.9), G(1300, "hips", "angry", look=-1, **RUTH, at=0.35), T("3rd YEAR", 1300, 300, 110, "red", at=0.55))

# PART 2: WHAT IS MEDICARE ADVANTAGE ---------------------------------------------
sc("Quick basics. Medicare is America's health insurance for people sixty-five and older. When you join, you pick one of two roads.",
   G(960, "present", "neutral", extras=ECON), T("65+", 960, 280, 150, "dark", at=0.3), chapter="Part 2: Two roads")
sc("Road one: traditional Medicare, run by the federal government. You can see most doctors who take Medicare, but you usually add separate plans for drugs and extra costs.",
   P("capitol", 600, 900, 0.9), T("ROAD 1", 600, 300, 100, "navy", at=0.2), P("clipboard", 1300, 860, 0.8, text="+ DRUGS", at=0.45), P("clipboard", 1650, 860, 0.8, text="+ EXTRA", at=0.6))
sc("Road two: Medicare Advantage. A private insurer gets paid by the government and bundles it all into one plan, often with extras like dental or glasses.",
   P("building", 600, 900, 0.9, text="INSURER"), T("ROAD 2", 600, 300, 100, "teal", at=0.2), P("moneybag", 1150, 880, 0.8, at=0.4), P("eye", 1600, 700, 0.7, at=0.6))
sc("The catch: most Advantage plans have a network. Your doctor has to be in it. Leave the network, and the bill can get exciting.",
   {"ring": [960, 600, 330], "color": "teal"}, G(960, "stand", "happy", extras=DAVE, s=0.7, at=0.2), G(1550, "panic", "shock", look=-1, extras=DAVE, s=0.7, at=0.55))
sc("Road two has become very popular. According to KFF, about thirty-five point two million people are in Medicare Advantage this year.",
   C(0, 35.2, 960, 380, fmt="{:.1f} million", size=170, color="teal", dur=2.0), P("arrowup", 1650, 880, 0.8, at=0.5))
sc("That's fifty-five percent of everyone eligible. More than half of Medicare now runs through private insurers.",
   {"bars": {"values": [55, 45], "labels": ["Advantage", "Traditional"], "colors": ["teal", "navy"], "fmt": "{}%", "w": 680, "h": 440}, "x": 960, "y": 860})
sc("And two companies dominate. UnitedHealth covers about twenty-six percent of Advantage members. Humana about twenty percent.",
   C(0, 26, 650, 360, fmt="{:.0f}%", size=180, color="navy"), C(0, 20, 1300, 360, fmt="{:.0f}%", size=180, color="green", at=0.4),
   T("UnitedHealth", 650, 520, 60, "dark", at=0.2), T("Humana", 1300, 520, 60, "dark", at=0.5))
sc("How much does the government pay a plan per person? MedPAC, which advises Congress, expects about sixteen thousand two hundred forty-two dollars a year.",
   G(500, "think", "neutral", **WATCH), C(0, 16242, 1250, 380, fmt="${:,.0f}", size=160, color="money", at=0.35))

# PART 3: WHY ARE INSURERS CUTTING -----------------------------------------------
sc("So if this is such a big business, why are insurers walking away from millions of customers?",
   G(960, "shrug", "confused", extras=DAVE), T("WHY CUT?", 960, 280, 140, "red", at=0.35), chapter="Part 3: Why cut plans?")
sc("Reason one, according to the insurers: care is costing more. UnitedHealthcare blamed higher costs and people using their plans more.",
   G(560, "present", "worried", **INS), P("arrowup", 1150, 880, 0.9, at=0.3), P("building", 1550, 900, 0.7, text="CLINIC", at=0.5))
sc("Rice University health economist Vivian Ho says seniors are using more medical care, and quote: for insurers, it's less profit for them.",
   G(560, "point", "neutral", **EXPERT), T("\"less profit\"", 1250, 380, 110, "dark", at=0.4))
sc("Reason two: the rules about payments changed. Jeannie Fuglesten Biniek of the health research group KFF says the main driver is recent federal changes.",
   G(560, "present", "neutral", **KFF), P("capitol", 1350, 900, 0.8, at=0.35))
sc("Those changes reduce how much private insurers get paid. Less money in, same costs out. You can guess the rest.",
   P("moneybag", 600, 880, 1.0), P("arrowdown", 850, 880, 0.7, at=0.25), P("pricetag", 1350, 860, 1.0, text="COSTS", at=0.45), P("arrowup", 1600, 880, 0.7, at=0.6))
sc("Reason three: profit margins. Healthcare Dive says insurers want them back, and for a second year are willing to lose members to do it.",
   {"bars": {"values": [100, 70], "labels": ["Members", "Margins?"], "colors": ["grey", "money"], "fmt": "{}", "w": 640, "h": 440}, "x": 800, "y": 860},
   G(1550, "hips", "smug", look=-1, **INS, at=0.5))
sc("Plans for people with special needs, like serious chronic illness, are growing. They tend to earn more per member. Plans for everyone else are shrinking.",
   P("arrowup", 600, 880, 0.9), T("SPECIAL NEEDS", 600, 360, 70, "green", at=0.2), P("arrowdown", 1350, 880, 0.9, at=0.45), T("EVERYONE ELSE", 1350, 360, 70, "red", at=0.55))
sc("Some insurers are leaving whole counties. Healthcare Dive counts Centene pulling out of three hundred forty-four, and CVS out of a hundred three.",
   C(0, 344, 700, 380, fmt="{:.0f}", size=200, color="red"), C(0, 103, 1300, 380, fmt="{:.0f}", size=200, color="red", at=0.4),
   T("Centene", 700, 540, 60, "dark", at=0.2), T("CVS", 1300, 540, 60, "dark", at=0.5))
sc("Dave summarises: some companies leave, some arrive, and the map looks like a game of musical chairs where the chairs are hospitals.",
   P("desk", 500, 900, 0.7), P("desk", 900, 900, 0.7, at=0.2), P("desk", 1300, 900, 0.7, at=0.35), G(1650, "run", "worried", look=-1, extras=DAVE, s=0.8, at=0.5))

# PART 4: WHO IS RIGHT ABOUT THE MONEY -------------------------------------------
sc("Now the argument underneath all this. Is the government paying insurers too little, or too much? Depending on who you ask, both.",
   P("scale", 960, 900, 1.4, anim="bob"), T("TOO LITTLE?", 500, 330, 90, "navy", at=0.3), T("TOO MUCH?", 1420, 330, 90, "red", at=0.5),
   chapter="Part 4: Too little, or too much?")
sc("The insurance industry has long argued that federal payments haven't kept up with what care actually costs.",
   G(600, "point", "worried", **INS), P("pricetag", 1300, 860, 1.0, text="CARE", at=0.35), P("arrowup", 1600, 880, 0.7, at=0.5))
sc("Critics see it the other way. MedPAC estimates Medicare will spend about fourteen percent more on Advantage members than on similar people in traditional Medicare.",
   G(500, "present", "neutral", **WATCH), C(0, 14, 1250, 380, fmt="+{:.0f}%", size=220, color="red", at=0.35))
sc("That gap: about seventy-six billion dollars this year. MedPAC says it raises Part B premiums for all Medicare members by about eleven billion.",
   C(0, 76, 700, 360, fmt="${:.0f}B", size=180, color="red"), C(0, 11, 1350, 360, fmt="${:.0f}B", size=160, color="orange", at=0.45),
   T("Part B premiums", 1350, 520, 55, "dark", at=0.5))
sc("So one side says: we're paid too little. The other says: you were paid too much. Both point at the same numbers. We just count the facts.",
   G(500, "point", "angry", **INS), G(1420, "point", "angry", look=-1, **WATCH, at=0.25), T("SAME NUMBERS", 960, 300, 100, "dark", at=0.55))
sc("And the government's view? The Centers for Medicare and Medicaid Services, the agency that runs Medicare, calls the outlook stable.",
   G(700, "present", "happy", **GOV), {"stamp": "STABLE", "x": 1350, "y": 420, "size": 100, "w": 380, "at": 0.4})
sc("It says more than ninety-nine percent of people will have at least one Advantage plan available, and ninety-seven percent will have ten or more.",
   C(0, 99, 700, 380, fmt="{:.0f}%", size=200, color="green"), C(0, 97, 1300, 380, fmt="{:.0f}%", size=200, color="green", at=0.4),
   T("1+ plan", 700, 540, 60, "dark", at=0.2), T("10+ plans", 1300, 540, 60, "dark", at=0.5))
sc("It also says about eight in ten members can stay in their current plan at the same or a lower premium.",
   T("8 in 10", 960, 380, 200, "green"), P("wallet", 1600, 860, 0.8, at=0.5))
sc("And the agency expects the average Advantage premium to fall, from fourteen dollars thirty-seven a month to twelve dollars.",
   C(14.37, 12.00, 960, 380, fmt="${:.2f}", size=200, color="green", dur=2.0), P("arrowdown", 1600, 880, 0.8, at=0.5))
sc("But that average includes the special-needs plans. Medicare Market Insights says premiums for regular plans rise about twenty-three percent, to fourteen eighty a month.",
   C(0, 14.80, 700, 380, fmt="${:.2f}", size=170, color="red"), C(0, 23, 1350, 380, fmt="+{:.0f}%", size=170, color="red", at=0.4))
sc("Two true numbers, two very different headlines. Ruth would like one headline, in large print.",
   T("$12.00", 600, 380, 130, "green"), T("$14.80", 1300, 380, 130, "red", at=0.3), G(1700, "facepalm", "tired", look=-1, **RUTH, s=0.7, at=0.55))

# PART 5: WHO IT HITS ------------------------------------------------------------
sc("So who feels this the most? Three groups.",
   T("WHO GETS HIT?", 960, 300, 130, "dark"), G(960, "think", "worried", extras=DAVE, at=0.4), chapter="Part 5: Who gets hit")
sc("Group one: rural areas. Vivian Ho says rural seniors, quote, are going to be the ones who are going to have the hardest time finding a Medicare Advantage plan.",
   P("house", 600, 900, 0.8), P("sun", 1500, 300, 0.7, at=0.2), G(1150, "think", "worried", extras=["cap"], shirt="brown", at=0.4))
sc("KFF counts about one hundred ninety-three counties with no Advantage drug plan for general enrollment next year. Up from one hundred twenty-three.",
   C(123, 193, 960, 380, fmt="{:.0f}", size=220, color="red", dur=2.0), T("counties", 960, 540, 80, "dark", at=0.3))
sc("About six hundred thirty-eight thousand people on Medicare live in those counties, up from three hundred ninety-nine thousand.",
   {"bars": {"values": [399, 638], "labels": ["2026", "2027"], "colors": ["orange", "red"], "fmt": "{}K", "w": 640, "h": 440}, "x": 960, "y": 860})
sc("Group two: people who need a lot of care. The average cap on what you pay for in-network care rises nine percent, to six thousand six hundred three dollars.",
   C(0, 6603, 960, 380, fmt="${:,.0f}", size=190, color="red"), T("+9%", 1600, 380, 120, "red", at=0.45))
sc("Group three: anyone who takes prescriptions. The average drug deductible in Advantage plans rises twenty-three percent, to five hundred nine dollars.",
   P("pricetag", 600, 860, 1.1, text="PILLS"), C(0, 509, 1300, 380, fmt="${:.0f}", size=200, color="red", at=0.35))
sc("For drug plans in general, the yearly out-of-pocket cap rises from twenty-one hundred dollars to twenty-four hundred.",
   C(2100, 2400, 960, 380, fmt="${:,.0f}", size=210, color="red", dur=2.0), T("yearly drug cap", 960, 540, 70, "dark", at=0.3))
sc("KFF says no standalone drug plan will have a zero-dollar premium next year for people without low-income help. And over a million must pick a new one.",
   {"stamp": "NO $0 PLANS", "x": 700, "y": 400, "size": 70, "w": 480}, C(0, 1, 1350, 380, fmt="{:.0f}M+", size=180, color="red", at=0.45))
sc("And extras? Nearly seventy percent of health plan leaders surveyed by HealthScape Advisors expect less generous benefits, like higher specialist copays and less dental.",
   C(0, 70, 700, 380, fmt="~{:.0f}%", size=200, color="orange"), P("clipboard", 1350, 860, 1.0, text="DENTAL", at=0.4), {"cross": [1350, 760, 130], "at": 0.6})
sc("Dave asks if less dental means he can stop flossing. Linda says that is not how teeth work.",
   G(600, "pointup", "grin", extras=DAVE), G(1350, "facepalm", "tired", look=-1, extras=LINDA, at=0.4))

# PART 6: WHAT CAN YOU DO ---------------------------------------------------------
sc("Okay. What can Ruth actually do? This is general information, not personal advice. But the dates are the same for everyone.",
   G(960, "present", "neutral", extras=ECON), {"stamp": "INFO, NOT ADVICE", "x": 960, "y": 300, "size": 60, "w": 560, "at": 0.4},
   chapter="Part 6: What can you do?")
sc("Step one: read the letter. Plans had to send them by early October. It says whether your plan ends or just changes.",
   P("envelope", 700, 820, 1.2), {"ring": [700, 760, 200], "at": 0.3}, T("READ ME", 1350, 380, 120, "red", at=0.5))
sc("Step two: the main window. Medicare open enrollment started October fifteenth and closes December seventh. A new plan starts January first.",
   P("calendar", 550, 860, 1.0, text="OCT 15"), {"arrow": [[750, 600], [1150, 600]], "color": "dark", "at": 0.3}, P("calendar", 1350, 860, 1.0, text="DEC 7", at=0.4),
   T("→ JAN 1", 1700, 400, 80, "green", at=0.6))
sc("If your plan is ending, you also get a bonus window, from December eighth to the end of February. But waiting can leave gaps, so most people don't.",
   P("calendar", 700, 860, 1.0, text="DEC 8"), P("calendar", 1250, 860, 1.0, text="FEB 28", at=0.35), P("stopwatch", 1650, 860, 0.7, at=0.6))
sc("Step three: compare more than the premium. Check your doctors are in the network, your drugs are on the list, and what a full year would cost.",
   P("clipboard", 550, 860, 1.0, text="DOCTORS"), P("clipboard", 1000, 860, 1.0, text="DRUGS", at=0.25), P("clipboard", 1450, 860, 1.0, text="TOTAL $", at=0.5))
sc("What if Ruth does nothing? She doesn't lose Medicare. She lands back in traditional Medicare automatically.",
   G(600, "shrug", "neutral", **RUTH), P("capitol", 1350, 900, 0.9, at=0.4), {"arrow": [[800, 600], [1150, 600]], "color": "green", "at": 0.3})
sc("But traditional Medicare has no drug coverage built in. Go sixty-three days in a row without it, and there can be a late penalty.",
   P("pricetag", 600, 860, 1.0, text="PILLS"), {"cross": [600, 760, 140], "at": 0.3}, C(0, 63, 1300, 380, fmt="{:.0f} days", size=150, color="red", at=0.45))
sc("One more door people miss. When an Advantage plan ends, there's a window to buy a Medigap policy without health questions.",
   T("MEDIGAP", 960, 330, 140, "teal"), {"stamp": "NO HEALTH QUIZ", "x": 960, "y": 560, "size": 60, "w": 520, "at": 0.4})
sc("It opens sixty days before the old plan ends and closes sixty-three days after. Miss it, and an insurer can charge more or say no.",
   C(0, 60, 650, 380, fmt="-{:.0f} days", size=130, color="dark"), C(0, 63, 1300, 380, fmt="+{:.0f} days", size=130, color="dark", at=0.4),
   P("lock", 960, 860, 0.8, at=0.6))
sc("And for free help: Medicare dot gov has a plan finder, and every state has a free counselling program for Medicare questions, called SHIP.",
   P("laptop", 650, 880, 1.0, text="MEDICARE.GOV"), P("phone", 1300, 860, 0.9, text="SHIP", at=0.4))
sc("Ruth books an appointment with a counsellor. She brings a folder, three pens, and a list of questions in alphabetical order.",
   G(600, "hold", "smug", **RUTH), P("clipboard", 1150, 860, 0.9, text="A-Z", at=0.35), G(1600, "stand", "shock", look=-1, extras=ECON, at=0.55))

# PART 7: WHAT'S NEXT ------------------------------------------------------------
sc("So what's next? Insurers expect Advantage enrollment to fall by about two million next year, to around thirty-four million.",
   C(35.2, 34, 960, 380, fmt="{:.1f}M", size=200, color="dark", dur=2.0), P("arrowdown", 1600, 880, 0.8, at=0.5), chapter="Part 7: What's next")
sc("If that happens, Advantage could cover less than half of Medicare for the first time since twenty twenty-three. The agency says projections like that usually come in too low.",
   T("< 50%?", 700, 380, 170, "orange"), G(1400, "present", "neutral", **GOV, at=0.4))
sc("The questions to watch: how many people switch by December seventh, what happens to payment rules for twenty twenty-eight, and whether more insurers leave.",
   P("calendar", 500, 860, 0.9, text="DEC 7"), P("clipboard", 960, 860, 0.9, text="2028 RULES", at=0.3), P("building", 1450, 900, 0.7, text="EXIT?", at=0.55))

# RECAP ----------------------------------------------------------------------
sc("Quick recap. About three point two million Medicare Advantage members must find new plans for twenty twenty-seven, including about a million from Humana and UnitedHealthcare.",
   C(0, 3.2, 960, 380, fmt="{:.1f}M", size=200, color="red"), P("envelope", 1600, 860, 0.8, at=0.5), chapter="Recap")
sc("Insurers point to rising costs and lower payments. Critics point to MedPAC's estimate that Advantage is still paid about fourteen percent more.",
   P("scale", 960, 900, 1.3, anim="bob"), T("costs", 500, 380, 90, "navy", at=0.3), T("+14%", 1420, 380, 90, "red", at=0.5))
sc("And the deadline that matters most for most people: December seventh.",
   P("calendar", 960, 860, 1.4, text="DEC 7", anim="pulse"))
sc("Back at Ruth's. She has picked a new plan. Same doctor, different pharmacy, and a premium she calls, quote, rude but survivable.",
   G(560, "hips", "smug", **RUTH), P("clipboard", 1150, 860, 0.9, text="NEW PLAN", at=0.3), T("RUDE BUT OK", 1500, 380, 80, "dark", at=0.55))
sc("Dave asks if he should start preparing now. He is forty-one. Ruth hands him the folder and says: yes.",
   G(500, "point", "grin", extras=DAVE), G(1150, "hold", "smug", look=-1, **RUTH, at=0.3), P("clipboard", 1550, 860, 0.8, text="YOURS", at=0.55))
sc("Your turn: has your family had to switch plans this year? Tell us in the comments. Without names, please.",
   G(500, "point", "neutral", extras=LINDA), P("envelope", 1250, 820, 1.1, text="?", at=0.3))
sc("And if calm stick figures explaining stressful news is your kind of thing, subscribe. We never change our plan.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep012",
    "title": "Why Are 3 Million Seniors Losing Their Health Plans?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Nearly 3.2 million Americans in Medicare Advantage must pick a new plan for 2027 because their plan is being discontinued, "
        "including about 1 million from Humana (about 600,000) and UnitedHealthcare (about 390,000), as CBS News reported on October 23, 2026. "
        "We go through what Medicare Advantage is, why insurers say they are cutting (higher costs, more use of care, lower federal payments), "
        "why critics say the program is still overpaid (MedPAC: about 14% more than traditional Medicare), what the Medicare agency (CMS) says, "
        "who is hit hardest (rural counties, people with high costs, prescriptions), and the key dates: open enrollment Oct 15 - Dec 7, "
        "a special window to the end of February if your plan ends, and the Medigap guaranteed-issue window.\n\n"
        "General information only, not medical, legal or financial advice. Check medicare.gov or your state's free SHIP counselling program for your own situation. "
        "Ruth, Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; quotes are attributed as reported.\n\n"
        "Sources:\n"
        "CBS News, Humana, UnitedHealthcare ending Medicare Advantage plans for 1 million seniors (Oct 23, 2026): https://www.cbsnews.com/news/humana-unitedhealthcare-end-medicare-advantage-plans/\n"
        "Healthcare Dive, Here's how much insurers are cutting Medicare Advantage plans for 2027: https://www.healthcaredive.com/news/medicare-advantage-cuts-2027-cms-landscape/831563/\n"
        "Marketplace, As Medicare open enrollment begins, millions of seniors will have to pick a new plan (Oct 14, 2026): https://www.marketplace.org/story/2026/10/14/why-some-insurers-are-dropping-medicare-advantage-plans\n"
        "24/7 Wall St., 3.2 million seniors will lose their Medicare Advantage plans in 2027 (Oct 19, 2026; citing CNN, KFF, Medicare Market Insights): https://247wallst.com/health-and-healthcare/2026/10/19/3-2-million-seniors-will-lose-their-medicare-advantage-plans-in-2027-and-their-replacement-options-are-shrinking/\n"
        "Straight Arrow News, Medicare open enrollment begins as millions face fewer plans, higher costs: https://san.com/cc/medicare-open-enrollment-begins-as-millions-face-fewer-plans-higher-costs/\n"
        "KFF, Medicare Advantage in 2026: Enrollment Update and Key Trends: https://www.kff.org/medicare/fact-sheet/medicare-advantage/\n"
        "MedPAC, March 2026 report press release: https://www.medpac.gov/wp-content/uploads/2026/03/March_2026_MedPAC_Report_Press_Release_SEC.pdf\n"
        "Money Talks News, Your Medicare Advantage plan won't be back in 2027? The Medigap window: https://www.moneytalksnews.com/your-medicare-advantage-plan-wont-be-back-in-a-cpa-on-the-medigap-window-that-protects-you/\n\n"
        "#medicare #medicareadvantage #openenrollment #explained #stickfigure #news"
    ),
    "tags": ["medicare advantage", "medicare advantage 2027", "medicare open enrollment", "humana", "unitedhealthcare", "medicare plan ending",
             "medigap", "seniors health insurance", "health insurance explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "MY PLAN|GONE?", "size": 210, "color": "black",
                  "guy": {"pose": "stand", "face": "shock", "look": -1, "extras": ["bun", "glasses"], "shirt": "purple"}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep012.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

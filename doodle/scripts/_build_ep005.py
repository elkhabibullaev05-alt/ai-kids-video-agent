"""Episode 5: France's student-led protests reach ~550,000 people on Oct 17, 2026."""
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
TEEN = dict(extras=["cap"], shirt="blue")      # Theo, a made-up French student
TEACH = dict(extras=["glasses"], shirt="green")  # a teacher
COP = dict(extras=["cap"], shirt="navy")

S = []
def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)


# COLD OPEN -------------------------------------------------------------------
sc("Forty degrees.",
   P("thermo", 960, 950, 1.6, text="40°C", color="red", anim="shake"), cam={"from": [960, 620, 1.35], "to": [960, 560, 1.1]})
sc("Thirty five students.",
   C(0, 35, 960, 420, fmt="{:.0f}", size=320, color="red", dur=0.8))
sc("And no teacher.",
   P("chalkboard", 960, 950, 1.3, text="ABSENT"), {"cross": [960, 560, 220], "at": 0.3})
sc("Welcome to Theo's classroom. Theo is sixteen, French, and made up. His classroom is very real.",
   G(960, "wave", "neutral", **TEEN), P("backpack", 1350, 900, 0.8, at=0.4), T("THEO, 16", 960, 330, 90, "blue", at=0.2),
   cam={"from": [960, 600, 1.2], "to": [960, 540, 1.0]})
sc("Thirty four other students. One chair each. Mostly.",
   *[G(260 + k * 200, "stand", "tired", look=1, s=0.6, at=0.05 * k) for k in range(8)],
   C(0, 35, 960, 260, size=170, color="red", at=0.1))
sc("The thermometer on the wall says forty degrees. That's a hundred and four Fahrenheit. In a maths lesson.",
   P("thermo", 500, 900, 1.3, text="40°C", color="red", anim="pulse"), G(1100, "panic", "scream", **TEEN, at=0.3),
   P("sun", 1600, 330, 0.9, at=0.5, anim="spin"), bg="yellow")
sc("And the teacher? The teacher is absent. Again. Nobody was sent to replace them.",
   P("chalkboard", 960, 900, 1.0, text="TEACHER:|ABSENT"), G(1550, "shrug", "confused", **TEEN, at=0.4),
   P("desk", 520, 900, 0.9, at=0.2))
sc("So Theo did what thousands of French teenagers did this autumn. He pushed some bins in front of the school gate.",
   P("school", 600, 900, 1.0, text="LYCEE"), P("barrier", 1200, 900, 0.9, at=0.3), G(1600, "hips", "smug", **TEEN, at=0.5))
sc("Fast forward a month, and on Saturday, October seventeenth, France's Interior Ministry counted about five hundred fifty thousand people marching.",
   P("calendar", 420, 860, 1.0, text="OCT 17"), C(0, 550000, 1150, 380, size=170, color="red", at=0.25, dur=2.2),
   T("marching", 1150, 520, 70, "dark", at=0.5))
sc("The organisers say eight hundred thousand. Protest maths is always a little bit French.",
   T("550,000", 600, 420, 120, "navy"), T("800,000", 1320, 420, 120, "red", at=0.3),
   G(600, "point", "neutral", extras=OFF, label="ministry", at=0.1), G(1320, "fist", "grin", extras=["cap"], label="organisers", at=0.4))
sc("Today's question: why are French high school students shutting down their own schools? And how did it get this big?",
   G(380, "think", "confused", extras=DAVE), T("WHY?", 1150, 380, 220, "red", at=0.3), P("school", 1150, 900, 0.8, at=0.5),
   chapter="Today's question")
sc("We'll go through what happened, the numbers, what students want, what the government says, and what comes next.",
   P("clipboard", 760, 900, 1.1, text="FACTS"), G(1300, "present", "neutral", extras=LINDA, at=0.35))
sc("One rule first: some people were badly hurt in this story. We'll state that plainly. The jokes stay in the classroom.",
   G(960, "stand", "neutral", extras=LINDA), {"box": [560, 220, 800, 140], "color": "white", "at": 0.3},
   T("FACTS FIRST", 960, 300, 80, "navy", at=0.3))

# PART 1: HOW IT STARTED -------------------------------------------------------
sc("It started in mid September, in Créteil, a suburb just south east of Paris.",
   P("globe", 500, 860, 1.0), {"ring": [1250, 520, 120], "at": 0.3}, T("CRETEIL", 1250, 520, 70, "red", at=0.3),
   T("PARIS", 1080, 360, 50, "dark", at=0.5), chapter="Part 1: How it started", bg="paper")
sc("Teachers held a strike day. Soon after, students at one high school, the Lycée Saint Exupéry, started a blockade.",
   G(500, "fist", "angry", **TEACH), P("megaphone", 760, 760, 0.7, at=0.2), P("school", 1350, 900, 0.9, text="ST-EXUPERY", at=0.4))
sc("A blockade, French style: you pile up bins and barriers at the school gate so nobody can get in. Including you.",
   P("barrier", 700, 900, 1.0), P("barrier", 1150, 900, 1.0, at=0.2), P("school", 1600, 900, 0.7, at=0.1),
   G(350, "hips", "smug", **TEEN, at=0.4))
sc("Within days, about a dozen schools nearby were blocked. Then it went national.",
   C(0, 12, 700, 420, fmt="{:.0f} schools", size=110, color="navy"), P("arrowup", 1350, 800, 1.2, color="red", at=0.4))
sc("By October first, the Interior Ministry said more than one thousand high schools were affected, and two hundred twenty two were fully blockaded.",
   C(0, 1027, 650, 380, size=170, color="red"), T("affected", 650, 500, 60, "dark", at=0.2),
   C(0, 222, 1300, 380, size=170, color="navy", at=0.35), T("blockaded", 1300, 500, 60, "dark", at=0.45))
sc("For scale, France has about three thousand seven hundred lycées. That's more than one in four.",
   {"bars": {"values": [3700, 1027], "labels": ["all lycées", "affected"], "colors": ["grey", "red"], "fmt": "{}", "w": 640, "h": 440},
    "x": 960, "y": 860})
sc("The next day, about four hundred were simply closed by local authorities, and gatherings outside them were banned.",
   P("school", 600, 900, 0.9, text="CLOSED"), P("lock", 600, 640, 0.6, at=0.3),
   C(0, 400, 1300, 420, size=160, color="red", at=0.4), T("closed", 1300, 540, 60, "dark", at=0.5))
sc("University students joined. Teachers' unions joined. Parents joined. By October sixth, more than two hundred fifty thousand people were in the streets.",
   G(300, "fist", "angry", **TEEN), G(620, "fist", "worried", **TEACH, at=0.2), G(940, "fist", "neutral", extras=LINDA, at=0.35),
   C(0, 250000, 1450, 380, size=140, color="red", at=0.5))
sc("And it crossed borders: student protests popped up in Belgium, in cities like Liège and Brussels.",
   P("globe", 700, 860, 1.0), {"arrow": [[850, 520], [1250, 420]], "at": 0.3}, T("BELGIUM", 1450, 400, 90, "red", at=0.45))
sc("Meanwhile Dave, who has never been to France, read all of this in one evening and now thinks he is a lycée expert.",
   G(800, "type", "smug", extras=DAVE), P("laptop", 1100, 900, 0.8), T("EXPERT", 1500, 380, 90, "gold", at=0.5, anim="pulse"),
   bg="paper")

# PART 2: WHAT STUDENTS WANT --------------------------------------------------
sc("So what do the students actually want? Their union listed four things.",
   P("clipboard", 960, 900, 1.2, text="4 DEMANDS"), G(450, "point", "neutral", **TEEN, at=0.3),
   chapter="Part 2: What students want", bg="sky")
sc("One: missing staff. Not just teachers, but school nurses, social workers and education assistants.",
   T("1", 300, 380, 200, "red"), G(800, "stand", "neutral", **TEACH, at=0.2), {"cross": [800, 650, 160], "at": 0.4},
   T("NURSE?", 1400, 450, 90, "dark", at=0.6))
sc("When a teacher is absent, students say a replacement often never comes. The class just sits there. Or goes home.",
   P("chalkboard", 800, 900, 0.9, text="NO CLASS"), G(1450, "shrug", "tired", **TEEN, at=0.3, walk=True, move=[1750, 900]))
sc("Two: old, run down buildings. And in the recent heatwaves, classrooms of thirty five to forty degrees.",
   T("2", 300, 380, 200, "red"), P("school", 850, 900, 0.9, text="OLD", at=0.15),
   P("thermo", 1450, 900, 1.1, text="35-40°C", color="red", at=0.4, anim="pulse"))
sc("That's Celsius. In Fahrenheit, that's somewhere between a sauna and a very bad idea.",
   P("thermo", 700, 900, 1.2, color="red"), P("fire", 1250, 900, 0.8, at=0.3), G(1600, "panic", "shock", **TEEN, at=0.5))
sc("Three: big classes and long days. Many classes have thirty two to thirty five pupils, and the timetable is packed.",
   T("3", 300, 380, 200, "red"), C(0, 35, 900, 420, fmt="{:.0f} pupils", size=120, color="navy", at=0.2),
   P("calendar", 1450, 860, 1.0, text="LONG DAY", at=0.45))
sc("Four: Parcoursup. That's the national website that decides which university you can go to.",
   T("4", 300, 380, 200, "red"), P("laptop", 900, 900, 1.2, text="Parcoursup"), G(1450, "type", "worried", **TEEN, at=0.4))
sc("Imagine your whole future loading on a progress bar. That's the stress students describe.",
   {"box": [460, 380, 1000, 110], "color": "white"}, {"box": [460, 380, 120, 110], "color": "green", "at": 0.3},
   T("LOADING YOUR FUTURE...", 960, 300, 70, "dark"), G(1650, "stand", "worried", **TEEN, anim="shake", at=0.4))
sc("Students in poorer suburbs also say they get less than schools in central Paris.",
   P("school", 600, 900, 0.8, text="SUBURB"), P("school", 1300, 900, 1.1, text="PARIS", color="gold", at=0.3),
   P("scale", 960, 600, 0.7, at=0.5))
sc("A sixteen year old named Olympe told Al Jazeera: Teachers are absent, and compared with schools in Paris, we don't have the same resources.",
   G(600, "present", "neutral", extras=["bun"], shirt="pink", label="Olympe, 16"),
   P("speech", 1250, 560, 1.4, text="same resources?", at=0.3))
sc("None of these complaints is new. Students protested over similar things in 1990, 2005 and 2018.",
   T("1990", 520, 400, 110, "grey"), T("2005", 960, 400, 110, "grey", at=0.2), T("2018", 1400, 400, 110, "grey", at=0.4),
   T("2026", 960, 640, 150, "red", at=0.6, anim="pulse"))
sc("Back in 1990, the education minister answered with an emergency plan and more money. Students today would quite like a sequel.",
   G(600, "present", "neutral", extras=OFF, label="1990 minister"), P("moneybag", 1150, 900, 1.1, text="€", at=0.35),
   P("arrowup", 1550, 800, 0.9, color="green", at=0.55))
sc("Linda, who has been a teacher for twenty years, says this list sounds like every staffroom she has ever been in.",
   G(800, "hips", "tired", extras=LINDA), P("coffee", 1150, 900, 0.8, at=0.3), P("clipboard", 1500, 900, 0.9, text="SAME LIST", at=0.5),
   bg="sky")

# PART 3: WHEN IT TURNED ROUGH ------------------------------------------------
sc("Now the hard part. Most of the protests have been peaceful. But not all of them.",
   G(960, "stand", "neutral", extras=LINDA), chapter="Part 3: When it turned rough", bg="paper")
sc("Some blockades turned into clashes. Bins were set on fire, and some school buildings too. The education minister said twenty four schools were burned or ransacked.",
   P("fire", 600, 900, 1.0), P("school", 1150, 900, 0.9, at=0.2), C(0, 24, 1600, 420, fmt="{:.0f}", size=170, color="red", at=0.45),
   T("schools", 1600, 540, 60, "dark", at=0.5))
sc("Police used tear gas, rubber bullets and stun grenades. Arrests climbed fast.",
   G(700, "stand", "neutral", **COP, label="police"), P("cloud", 1250, 500, 1.0, color="grey", at=0.3),
   P("barrier", 1400, 900, 0.8, at=0.4))
sc("More than six thousand people have been arrested. About eighty five percent of them were under eighteen. Most were later released.",
   C(0, 6000, 650, 380, fmt="{:,.0f}+", size=160, color="red"), T("arrested", 650, 500, 60, "dark", at=0.2),
   C(0, 85, 1350, 380, fmt="{:.0f}%", size=160, color="navy", at=0.4), T("under 18", 1350, 500, 60, "dark", at=0.5))
sc("The Prime Minister's latest injury count since the start: nine hundred thirty seven police officers and gendarmes.",
   G(450, "present", "neutral", extras=OFF, label="the Prime Minister"), P("podium", 450, 900, 0.9),
   C(0, 937, 1250, 420, size=170, color="navy", at=0.35), T("police & gendarmes", 1250, 540, 54, "dark", at=0.45))
sc("And two hundred forty eight students, plus one hundred forty nine school staff. He called it the highest number the Education Ministry has ever recorded.",
   {"bars": {"values": [937, 248, 149], "labels": ["police", "students", "staff"], "colors": ["navy", "red", "green"], "fmt": "{}",
             "w": 760, "h": 440}, "x": 960, "y": 860})
sc("Two teenagers suffered life changing injuries. One reportedly lost a hand to a police stun grenade, another reportedly lost an eye.",
   G(960, "stand", "sad", extras=LINDA), T("UNDER INVESTIGATION", 960, 300, 80, "dark", at=0.3))
sc("Both cases are under investigation. The government suspended some types of stun grenade after one of them.",
   P("clipboard", 700, 900, 1.0, text="INQUIRY"), P("lock", 1250, 900, 0.9, text="SUSPENDED", at=0.4))
sc("The Interior Minister told the Senate that thirty six investigations into alleged police violence have been opened.",
   G(500, "present", "neutral", extras=OFF, label="Interior Minister"), C(0, 36, 1250, 420, size=180, color="red", at=0.3),
   T("investigations", 1250, 550, 60, "dark", at=0.4))
sc("Rights groups, including Amnesty International, say the force used against minors was disproportionate.",
   G(600, "point", "worried", extras=["glasses"], label="rights groups"), P("scale", 1250, 900, 1.0, at=0.35))
sc("And here's the twist nobody expected: one of France's biggest police unions says it will file a complaint against the state, too.",
   G(600, "fist", "angry", **COP, label="police union"), P("envelope", 1150, 760, 1.0, text="COMPLAINT", at=0.3),
   P("capitol", 1600, 900, 0.8, at=0.5))
sc("Their complaint: contradictory orders that left officers exposed. So the students and some of the police both feel the government left them alone.",
   G(500, "shrug", "worried", **TEEN), G(1400, "shrug", "worried", **COP, look=-1, at=0.3),
   P("capitol", 960, 900, 0.7, at=0.5), T("?", 960, 420, 140, "red", at=0.6))

# PART 4: SATURDAY ------------------------------------------------------------
sc("Which brings us to Saturday, October seventeenth. A national day of protest.",
   P("calendar", 960, 860, 1.3, text="OCT 17"), chapter="Part 4: Saturday", bg="yellow")
sc("This time, students were joined by trade unions and by the yellow vests, the movement that first appeared in 2018 over fuel prices.",
   G(400, "fist", "angry", **TEEN), G(800, "fist", "neutral", extras=["hardhat"], at=0.25, label="unions"),
   G(1200, "fist", "angry", extras=["hair"], shirt="yellow", at=0.45, label="yellow vests"), P("gaspump", 1600, 900, 0.9, at=0.6))
sc("The adults brought their own list: the cost of living, and fuel prices pushed up by the war involving Iran.",
   P("gaspump", 600, 900, 1.1, text="€€€"), P("cart", 1150, 900, 0.9, at=0.3), P("arrowup", 1600, 800, 1.0, color="red", at=0.5))
sc("The Interior Ministry counted about five hundred fifty thousand protesters nationwide, about one hundred ten thousand of them in Paris.",
   C(0, 550000, 650, 380, size=130, color="red"), T("France", 650, 490, 60, "dark", at=0.2),
   C(0, 110000, 1350, 380, size=130, color="navy", at=0.4), T("Paris", 1350, 490, 60, "dark", at=0.5))
sc("Shops boarded up their windows. Thousands of police and riot units were deployed.",
   P("building", 600, 900, 0.9, text="CLOSED"), P("barrier", 1150, 900, 0.9, at=0.3),
   *[G(1450 + k * 120, "stand", "neutral", s=0.6, at=0.4 + 0.05 * k, **COP) for k in range(3)])
sc("In Marseille, protesters rammed the town hall door with security barriers. Bins burned. In Paris, dozens were detained after clashes.",
   P("building", 600, 900, 1.0, text="TOWN HALL"), P("barrier", 1100, 900, 0.8, at=0.3, move=[900, 900]),
   P("fire", 1550, 900, 0.8, at=0.5))
sc("One demonstrator shouted: we're taking the Bastille. That's the fortress stormed in 1789. It hasn't been standing for a long time.",
   G(600, "fist", "scream", extras=["hair"]), P("speech", 1050, 520, 1.1, text="BASTILLE!", at=0.2),
   T("1789", 1550, 420, 120, "grey", at=0.5))
sc("Dave, watching from his sofa, has started saying 'ah, the French', as if he understands anything at all.",
   G(800, "hold", "smug", extras=DAVE), P("tv", 1350, 800, 0.9, text="FRANCE", at=0.2), P("coffee", 520, 900, 0.6, at=0.4),
   bg="paper")

# PART 5: WHAT THE GOVERNMENT SAYS --------------------------------------------
sc("So what does the government say? Let's hear from the top.",
   P("capitol", 960, 900, 1.1), chapter="Part 5: What each side says", bg="paper")
sc("On Friday, the President said the right to protest is fully respected, but it must come with respect for people and property. He called for calm.",
   G(600, "present", "neutral", extras=OFF, label="the President"), P("scale", 1250, 900, 1.0, at=0.3),
   T("CALM", 1250, 380, 110, "blue", at=0.5))
sc("Earlier, the Prime Minister said the schools' problems must be heard, while condemning violence. More recently, he warned the movement was turning into a wave of urban violence.",
   G(500, "point", "worried", extras=OFF, label="the Prime Minister"), P("speech", 1050, 480, 1.1, text="must be heard", at=0.2),
   P("speech", 1550, 640, 1.0, text="urban violence", at=0.55))
sc("His office also says far left groups, especially the party France Unbowed, are organising and steering the protests.",
   G(600, "point", "angry", extras=OFF), {"arrow": [[800, 600], [1200, 600]], "at": 0.3},
   G(1400, "shrug", "neutral", extras=["glasses"], look=-1, label="France Unbowed", at=0.4))
sc("France Unbowed's leader urged people to stand up to police brutality, then later said he backed peaceful methods. Critics say his party is exploiting teenagers.",
   G(500, "fist", "angry", extras=["glasses"], label="party leader"), P("megaphone", 800, 760, 0.7, at=0.2),
   G(1400, "point", "angry", extras=OFF, look=-1, label="critics", at=0.5))
sc("A Le Figaro poll found sixty two percent of French people think the students' movement is justified.",
   C(0, 62, 700, 420, fmt="{:.0f}%", size=200, color="green"), T("justified", 700, 560, 70, "dark", at=0.3),
   P("chart", 1400, 900, 0.9, at=0.4))
sc("But in the same poll, seventy eight percent said France Unbowed was using it politically. So people can like the cause and dislike the politics.",
   C(0, 78, 700, 420, fmt="{:.0f}%", size=200, color="red"), T("used politically", 700, 560, 60, "dark", at=0.3),
   G(1400, "shrug", "confused", extras=DAVE, at=0.4))
sc("So, depending on who you ask, this is a youth movement about broken schools, a cover for riots, or a political operation. Possibly all three, on different streets.",
   P("school", 450, 900, 0.7), P("fire", 960, 900, 0.7, at=0.3), P("ballot", 1470, 900, 0.8, at=0.55),
   T("?", 960, 360, 160, "red", at=0.7))
sc("We don't pick a side. We just count the facts.",
   P("clipboard", 960, 900, 1.2, text="FACTS"), G(500, "stand", "neutral", extras=LINDA, at=0.3))

# PART 6: THE MONEY -----------------------------------------------------------
sc("Here's the problem underneath everything: money. The government is trying to pass a tight budget through a divided parliament.",
   P("moneybag", 700, 900, 1.2, text="€"), P("capitol", 1350, 900, 0.9, at=0.3), chapter="Part 6: The money problem", bg="sky")
sc("France's public debt is about one hundred nineteen percent of its whole yearly economy.",
   C(0, 119.3, 960, 420, fmt="{:.1f}%", size=200, color="red"), T("debt vs economy", 960, 570, 70, "dark", at=0.3))
sc("In plain words: France owes more than everything the country produces in a year.",
   {"bars": {"values": [100, 119], "labels": ["one year of economy", "debt"], "colors": ["green", "red"], "fmt": "{}%", "w": 680, "h": 440},
    "x": 960, "y": 860})
sc("So students want more teachers, more nurses and new buildings, and the government is looking for things to cut.",
   G(500, "fist", "angry", **TEEN), P("arrowup", 760, 760, 0.8, color="green", at=0.2),
   G(1400, "hold", "worried", extras=OFF, look=-1, at=0.35), P("arrowdown", 1150, 760, 0.8, color="red", at=0.5))
sc("It's like asking your landlord to fix the roof while he's selling the furniture.",
   P("house", 700, 900, 1.0), P("desk", 1300, 900, 0.8, at=0.3, move=[1700, 900]), G(400, "facepalm", "tired", extras=DAVE, at=0.4))
sc("To be fair to the government, it has made offers. On October second, it announced a five point plan.",
   P("clipboard", 960, 900, 1.1, text="5 POINTS"), G(500, "present", "neutral", extras=OFF, at=0.3))
sc("Students said it wasn't enough. So the Prime Minister asked ministers for proposals by the end of October.",
   G(500, "shrug", "angry", **TEEN), {"cross": [1200, 600, 140], "at": 0.3}, P("calendar", 1550, 860, 0.9, text="END OCT", at=0.5))
sc("On the list: replacing absent teachers, looking at how long the school day is, and repairing older buildings.",
   P("chalkboard", 560, 900, 0.8, text="TEACHERS"), P("calendar", 1050, 860, 0.8, text="HOURS", at=0.25),
   P("school", 1550, 900, 0.8, text="REPAIRS", at=0.5))
sc("Which, you'll notice, is roughly what the students asked for. The question is whether the money will be there.",
   P("moneybag", 960, 900, 1.2, text="€?"), T("?", 1350, 420, 160, "red", at=0.4, anim="pulse"))

# PART 7: WHAT'S NEXT ---------------------------------------------------------
sc("So what happens next? Three things to watch.",
   G(500, "point", "neutral", extras=LINDA), T("3 THINGS", 1200, 420, 140, "navy", at=0.3), chapter="Part 7: What's next", bg="paper")
sc("One: the government's proposals at the end of October. If students think they're real, blockades could fade.",
   T("1", 300, 380, 200, "red"), P("calendar", 900, 860, 1.0, text="END OCT"), P("arrowdown", 1450, 800, 0.9, color="green", at=0.4))
sc("Two: the investigations into police violence. Their findings could calm things down, or fire them back up.",
   T("2", 300, 380, 200, "red"), P("clipboard", 900, 900, 1.0, text="INQUIRY"), P("scale", 1450, 900, 0.9, at=0.4))
sc("Three: politics. France elects a new president in April 2027, and every party is reading these crowds very carefully.",
   T("3", 300, 380, 200, "red"), P("ballot", 900, 900, 1.0), P("calendar", 1450, 860, 1.0, text="APR 2027", at=0.4))
sc("A sixteen year old named Rose told Al Jazeera: If nothing changes, we'll keep going for much longer.",
   G(600, "fist", "neutral", extras=["bun"], shirt="purple", label="Rose, 16"),
   P("speech", 1250, 560, 1.3, text="keep going", at=0.3))

# RECAP -----------------------------------------------------------------------
sc("Quick recap. French high school students started blocking schools in September over missing teachers, crowded classes and crumbling buildings.",
   P("school", 600, 900, 0.9), P("barrier", 1200, 900, 0.8, at=0.3), chapter="Recap", bg="yellow")
sc("It grew into one of the biggest youth movements in years, with thousands of arrests, hundreds injured on all sides, and investigations into police force.",
   C(0, 6000, 650, 400, fmt="{:,.0f}+", size=130, color="red"), C(0, 937, 1300, 400, size=130, color="navy", at=0.3),
   T("arrests", 650, 510, 54, "dark"), T("police injured", 1300, 510, 54, "dark", at=0.3))
sc("On October seventeenth, unions and yellow vests joined, and around half a million people marched. Now everyone waits for the government's offer.",
   C(0, 550000, 960, 400, size=150, color="red"), P("calendar", 960, 860, 0.9, text="END OCT", at=0.5))
sc("And Theo? His teacher is back. The thermometer still says thirty one. That's progress, French style.",
   G(700, "stand", "happy", **TEEN), G(1150, "present", "neutral", **TEACH, look=-1, at=0.2),
   P("thermo", 1550, 900, 1.0, text="31°C", color="orange", at=0.45))
sc("Your turn: if you could fix one thing in your old school, what would it be? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("chalkboard", 1250, 900, 0.9, text="FIX ONE|THING?", at=0.3))
sc("And if stick figures explaining the news is your kind of thing, subscribe. We'll keep counting the facts. Calmly.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep005",
    "title": "Why Are French Teens Shutting Down Their Schools?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Since September, French high school students have been blockading their own schools over missing teachers, crowded "
        "classes, crumbling buildings and university-admission stress. On October 17, 2026, unions and yellow vests joined them "
        "and France's Interior Ministry counted about 550,000 protesters. What do the students want, what does the government "
        "say, and what happens next? Explained with stick figures, facts only, no sides.\n\n"
        "Chapters are in the video timeline. Theo, Dave and Linda are made-up characters. Officials are shown as generic stick "
        "figures; quotes are attributed to the people who said them, as reported.\n\n"
        "Sources:\n"
        "Euronews, Dozens arrested as protesters clash with security forces in Paris (Oct 17, 2026): https://www.euronews.com/2026/10/17/france-braces-for-tense-protests-as-security-concerns-take-centre-stage\n"
        "France 24, live coverage of the Oct 17 protests: https://www.france24.com/en/france/20261017-live-france-s-yellow-vests-throw-their-weight-behind-mounting-student-protests\n"
        "Al Jazeera, France's student protesters in their own words (Oct 7, 2026): https://www.aljazeera.com/news/2026/10/7/were-short-of-resources-frances-student-protesters-in-their-own-words\n"
        "TIME, Why is France Burning? (Oct 16, 2026): https://time.com/article/2026/10/16/france-student-protests-macron/\n"
        "Wikipedia, 2026 French lycée protests (timeline, ministry figures, poll): https://en.wikipedia.org/wiki/2026_French_lyc%C3%A9e_protests\n"
        "Democracy Now!, headlines Oct 16, 2026: https://www.democracynow.org/2026/10/16/headlines\n\n"
        "#france #protests #students #paris #explained #stickfigure #news"
    ),
    "tags": ["france protests", "french student protests", "lycee protests", "paris protests", "october 17 protest",
             "yellow vests", "france news", "news explained", "stick figure animation", "world news explained"],
    "thumbnail": {"bg": "yellow", "text": "SCHOOLS|BLOCKED?!", "size": 180, "color": "black",
                  "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["cap"], "shirt": "blue"},
                  "items": [{"prop": "school", "x": 1690, "y": 900, "s": 0.8, "text": "LYCEE"},
                            {"prop": "barrier", "x": 1700, "y": 420, "s": 0.6}], "guy_x": 1300},
    "scenes": [s for s in S if s],
}
# rek-ball pacing: every scene gets a different background tint from the one before -> a clear visual cut
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
    for it in s["items"]:
        if "in_" in it:
            it["in"] = it.pop("in_")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep005.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

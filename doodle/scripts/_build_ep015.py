"""Episode 15: cost-of-living protests across Europe on Saturday Oct 24, 2026 (France, Italy, Spain, Portugal, Albania) — why now? Explained with stick figures."""
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


# COLD OPEN --------------------------------------------------------------------
sc("Dave has saved for two years. He is finally taking the big trip: a grand tour of Europe. Five countries. One suitcase. Zero French.",
   P("plane", 1150, 450, 1.3, anim="bob"), G(550, "fist", "grin", extras=DAVE, at=0.3), P("globe", 1600, 880, 0.8, at=0.6),
   cam={"from": [1100, 600, 1.3], "to": [960, 540, 1.0]})
sc("Stop one: Paris. Saturday. Dave walks to the Louvre with his ticket. The Louvre is closed.",
   P("building", 1100, 900, 1.2, text="LOUVRE"), G(500, "hold", "happy", extras=DAVE, at=0.2), {"stamp": "CLOSED", "x": 1100, "y": 520, "size": 90, "w": 380, "at": 0.65})
sc("So is the Musée d'Orsay. So are at least twenty-four metro stations. So is Art Basel's weekend programme.",
   C(0, 24, 700, 420, fmt="{:.0f}", size=260, color="red"), T("metro stations shut", 700, 610, 70, "dark", at=0.3),
   *SIGN(1450, "CLOSED", 1.0, at=0.5))
sc("Dave flies to Milan for pasta. Truckers had been blockading over fuel costs, and some pasta production, CNN reported, was halted.",
   P("truck", 650, 900, 1.0), P("barrier", 1050, 900, 1.0, at=0.25), P("dish", 1500, 880, 1.0, text="PASTA?", at=0.5), G(1750, "shrug", "confused", look=-1, extras=DAVE, s=0.8, at=0.7))
sc("Madrid: a tent camp in the main square. Lisbon: people marching with house keys. Tirana: tear gas.",
   T("MADRID", 400, 300, 70, "orange"), P("booth", 400, 900, 0.7, text="TENTS"), T("LISBON", 960, 300, 70, "green", at=0.3),
   *SIGN(960, "KEYS", 0.8, at=0.3), T("TIRANA", 1520, 300, 70, "red", at=0.6), P("cloud", 1520, 650, 0.9, at=0.6))
sc("Dave looks at his itinerary. Dave did not book a holiday. Dave booked a tour of the news.",
   P("clipboard", 750, 860, 1.2, text="TOUR?"), G(1350, "facepalm", "tired", look=-1, extras=DAVE, at=0.4), bg="yellow")
S.append({"say": "Today: why did so many European countries hit the streets on the same Saturday? Is it one movement, or many? And what happens next?",
          "items": [P("globe", 960, 880, 1.3), G(350, "think", "confused", extras=DAVE, at=0.35), T("ONE? MANY?", 1550, 350, 90, "red", at=0.6)],
          "chapter": "Today's question"})

# PART 1: SATURDAY -------------------------------------------------------------------
sc("First, what happened. On Saturday, October twenty-fourth, there were protests in France, Italy, Spain, Portugal, Albania and Belgium.",
   P("calendar", 500, 860, 1.0, text="SAT OCT 24"), C(0, 6, 1300, 420, fmt="{:.0f}", size=280, color="red", at=0.3), T("countries", 1300, 610, 80, "dark", at=0.5),
   chapter="Part 1: One Saturday")
sc("The biggest crowds were in France. The Interior Ministry counted four hundred ten thousand people nationwide, including one hundred ten thousand in Paris.",
   C(0, 410000, 960, 400, fmt="{:,.0f}", size=200, color="navy"), T("official count", 960, 580, 70, "dark", at=0.4), P("megaphone", 1700, 880, 0.8, at=0.55))
sc("The CGT union says it was nearly double. Organisers said close to eight hundred thousand.",
   {"bars": {"values": [410, 800], "labels": ["government", "organisers"], "colors": ["navy", "red"], "fmt": "{}k", "w": 700, "h": 420}, "x": 900, "y": 820},
   G(1650, "shrug", "neutral", look=-1, extras=LINDA, at=0.5))
sc("This happens at every protest, everywhere. The police count with a calculator. The organisers count with their hearts.",
   P("laptop", 600, 880, 0.9, text="410k"), P("speech", 1350, 450, 1.3, text="800k!", at=0.4), T("same march", 960, 830, 60, "dark", at=0.65))
sc("Security was huge. More than seventy thousand police officers and gendarmes, twenty percent more than the weekend before, according to Interior Minister Laurent Nuñez.",
   C(0, 70000, 800, 400, fmt="{:,.0f}+", size=190, color="navy"), G(1500, "stand", "neutral", look=-1, **COP), G(1700, "stand", "neutral", look=-1, **COP, at=0.2),
   T("+20%", 800, 580, 100, "red", at=0.5))
sc("Protests were banned in the centres of several cities, including Lyon, Nice, Montpellier and Rouen. In Paris, the march was moved to the edge of the city.",
   P("barrier", 600, 900, 1.1), *SIGN(1000, "NO MARCH", 0.8, at=0.25), {"arrow": [[1250, 650], [1700, 650]], "at": 0.5}, T("to the edge", 1500, 450, 70, "dark", at=0.6))
sc("Most marchers were peaceful. Near the end, authorities said about five hundred people they called rioters clashed with police. Officers used tear gas and water cannon.",
   G(500, "stand", "neutral", **STU), G(750, "stand", "neutral", **STU2, at=0.1), P("cloud", 1350, 600, 1.0, at=0.4), T("500", 1350, 330, 120, "red", at=0.55))
sc("By evening, the minister said, quote: we are at nearly one thousand arrests. That's a lot. But fewer than the weekend before.",
   G(600, "stand", "neutral", **MIN, label="Interior Minister"), P("speech", 1300, 480, 1.4, text="\"nearly 1,000|arrests\"", at=0.35))

# PART 2: HOW IT STARTED ---------------------------------------------------------------
sc("To understand Saturday, rewind to mid-September. It started with French high school students.",
   P("calendar", 600, 860, 1.0, text="SEPT"), P("school", 1300, 900, 1.0, at=0.35), chapter="Part 2: It started at school")
sc("They blockaded their schools over crumbling buildings, missing teachers, and a university admissions system called Parcoursup that they say is unfair.",
   P("school", 600, 900, 1.0), P("barrier", 1000, 900, 0.8, at=0.25), G(1350, "fist", "angry", look=-1, **STU, at=0.4), G(1600, "fist", "angry", look=-1, **STU2, at=0.55))
sc("Their slogan, roughly: schools that don't fall on our heads. Which is a low bar, and also a fair one.",
   P("school", 900, 900, 1.2), P("arrowdown", 900, 420, 0.8, anim="shake", at=0.35), T("LOW BAR", 1550, 400, 90, "dark", at=0.6))
sc("Then unions joined, including the big CGT. So did what's left of the yellow vest movement. And the topic got bigger: prices, inequality, the government itself.",
   G(450, "fist", "angry", **STU), G(800, "fist", "neutral", extras=["hardhat"], shirt="red", at=0.25, label="unions"),
   G(1150, "fist", "angry", extras=["hair"], shirt="yellow", at=0.45, label="yellow vests"), T("PRICES", 1600, 400, 90, "red", at=0.65))
sc("The weekend before, October seventeenth, more than half a million people marched. That day turned into looting and vandalism in several cities.",
   P("calendar", 600, 860, 1.0, text="OCT 17"), C(0, 500000, 1300, 400, fmt="{:,.0f}+", size=170, color="red", at=0.3))
sc("Thousands of businesses were damaged or looted. More than two thousand people were taken into custody. The historic town hall in Limoges, built in 1883, was largely destroyed by fire.",
   P("building", 700, 900, 1.0, text="TOWN HALL"), P("fire", 700, 520, 0.8, at=0.3), C(0, 2000, 1400, 420, fmt="{:,.0f}+", size=170, color="dark", at=0.5))
sc("That's why Paris looked like a fortress this Saturday. Shops boarded up windows. Even in Brussels, luxury shops did the same.",
   P("building", 600, 900, 0.9, text="SHOP"), {"box": [430, 640, 340, 160], "color": "brown", "at": 0.3}, P("building", 1350, 900, 0.9, text="BRUSSELS", at=0.5),
   {"box": [1180, 640, 340, 160], "color": "brown", "at": 0.65})

# PART 3: THE NUMBER ---------------------------------------------------------------------
sc("Now, the number underneath all of it.",
   T("?", 960, 450, 300, "red", anim="pulse"), chapter="Part 3: The number")
sc("In September, prices in the eurozone were three point eight percent higher than a year earlier, according to Eurostat. In August it was three point two.",
   {"bars": {"values": [3.2, 3.8], "labels": ["Aug", "Sep"], "colors": ["grey", "red"], "fmt": "{}%", "w": 700, "h": 420}, "x": 900, "y": 820},
   P("thermo", 1650, 900, 1.1, at=0.5))
sc("The European Central Bank aims for two. So prices are now rising almost twice as fast as the target.",
   C(0, 2, 650, 420, fmt="{:.0f}%", size=220, color="green"), C(0, 3.8, 1300, 420, fmt="{:.1f}%", size=220, color="red", at=0.3), T("target vs reality", 960, 640, 70, "dark", at=0.55))
sc("The big driver is energy. Energy prices were up eighteen point eight percent in a year.",
   P("gaspump", 650, 900, 1.2), C(0, 18.8, 1300, 400, fmt="+{:.1f}%", size=220, color="red", at=0.3), T("energy", 1300, 590, 80, "dark", at=0.5))
sc("Much of that traces back to the Iran war and the fight over shipping through the Strait of Hormuz, which pushed up oil and fuel worldwide.",
   P("strait", 700, 900, 1.0), P("tanker", 1200, 900, 0.9, at=0.3), P("arrowup", 1650, 760, 0.9, at=0.55))
sc("Strip out food and energy, and core inflation is two point five percent. Much calmer. But nobody fills their car with core inflation.",
   C(0, 2.5, 700, 420, fmt="{:.1f}%", size=220, color="orange"), T("core", 700, 610, 80, "dark", at=0.3), P("car", 1400, 900, 0.9, at=0.5), P("gaspump", 1750, 900, 0.7, at=0.6))
sc("And it's uneven. Germany three point three. France three point four. Italy above four. Spain five.",
   {"bars": {"values": [3.3, 3.4, 4.1, 5.0], "labels": ["Germany", "France", "Italy", "Spain"], "colors": ["grey", "navy", "green", "red"], "fmt": "{}%", "w": 900, "h": 420},
    "x": 960, "y": 820})
sc("Dave, back in Paris, buys a coffee and a croissant. He checks the receipt twice. Then he checks it a third time, in case it changes its mind.",
   G(600, "hold", "worried", extras=DAVE), P("coffee", 1000, 880, 0.8, at=0.25), P("bread", 1250, 880, 0.8, at=0.35), P("clipboard", 1600, 860, 0.9, text="€€€", at=0.55))

# PART 4: COUNTRY BY COUNTRY --------------------------------------------------------------
sc("But here's the key point. This isn't one coordinated movement. Each country has its own reasons, and they overlap.",
   P("globe", 960, 880, 1.1), T("NOT ONE MOVEMENT", 960, 280, 90, "red", at=0.35), chapter="Part 4: Many reasons")
sc("Spain. The spark was housing. The eviction of an eighty-seven-year-old woman in Madrid, who later died in hospital, set off weeks of protest, AP reported.",
   P("house", 800, 900, 1.1), T("SPAIN", 800, 300, 90, "orange", at=0.2), G(1400, "stand", "sad", look=-1, **GRAN, at=0.4))
sc("Since then, a tent camp has filled Madrid's Puerta del Sol square.",
   P("booth", 600, 900, 0.8, text="TENT"), P("booth", 1000, 900, 0.8, text="TENT", at=0.2), P("booth", 1400, 900, 0.8, text="TENT", at=0.4), T("Puerta del Sol", 1000, 330, 80, "dark", at=0.55))
sc("The numbers explain why. Spain's minimum wage is twelve hundred twenty-one euros a month. Average rent for an eighty-square-metre flat: about eleven hundred thirty.",
   {"bars": {"values": [1221, 1130], "labels": ["min wage", "avg rent"], "colors": ["green", "red"], "fmt": "€{}", "w": 700, "h": 420}, "x": 900, "y": 820},
   P("wallet", 1650, 860, 0.9, at=0.5))
sc("That leaves about ninety euros for everything else. Food. Bus. Phone. Joy.",
   C(1221, 91, 960, 420, fmt="€{:,.0f}", size=260, color="red"), T("left over", 960, 620, 80, "dark", at=0.5))
sc("A twenty-year-old waitress at the camp told AP, quote: most of my paycheck goes to the rent.",
   G(600, "stand", "tired", extras=LINDA, shirt="pink", label="waitress, 20"), P("speech", 1300, 480, 1.5, text="\"most of my paycheck|goes to the rent\"", at=0.35))
sc("In Madrid on Saturday, pensioners also marched. They want pensions tied to real inflation, and a minimum pension as high as the minimum wage.",
   G(550, "fist", "angry", **GRAN), G(850, "fist", "neutral", extras=["glasses"], shirt="grey", at=0.2), *SIGN(1400, "PENSIONS", 1.0, at=0.4))
sc("Spain's government did approve affordable housing measures, but they lacked support in parliament. The Prime Minister then called an early election for November.",
   P("capitol", 700, 900, 0.9), {"cross": [700, 650, 140], "at": 0.3}, P("ballot", 1350, 880, 1.0, at=0.5), T("NOV", 1350, 400, 100, "navy", at=0.6))
sc("Portugal: also housing. In Lisbon, marchers held up house keys. They want caps on rent hikes and a new eviction law reversed.",
   T("PORTUGAL", 960, 260, 90, "green"), *SIGN(700, "KEYS", 1.0, at=0.2), P("house", 1300, 900, 0.9, at=0.4), P("pricetag", 1650, 760, 0.8, text="RENT CAP", at=0.6))
sc("Italy: students, wages, and war. Rome students occupied a high school on October seventh, and wrote in their statement: like in France.",
   T("ITALY", 960, 260, 90, "green"), P("school", 650, 900, 0.9, at=0.2), P("speech", 1350, 520, 1.3, text="\"like in France\"", at=0.45))
sc("Italian inflation was above four percent in September. One Rome student told CNN she commuted one hundred twenty kilometres to save on rent.",
   C(0, 4.1, 650, 420, fmt="{:.1f}%", size=220, color="red"), P("car", 1300, 900, 0.8, move=[1650, 900], at=0.3), T("120 km", 1400, 420, 110, "dark", at=0.5))
sc("On Saturday there were marches in six Italian cities. Police said nine arrests and three hundred seventy-one people briefly detained, one hundred ten of them minors.",
   C(0, 371, 960, 400, fmt="{:,.0f}", size=230, color="navy"), T("briefly detained", 960, 590, 70, "dark", at=0.35), T("110 minors", 960, 700, 70, "red", at=0.55))
sc("Albania is different again. There, the anger is mainly about corruption. Students, artists and opposition parties want the Prime Minister to resign.",
   T("ALBANIA", 960, 260, 90, "red"), G(700, "fist", "angry", **STU, at=0.2), G(1250, "hips", "neutral", look=-1, **PRES, label="the Prime Minister", at=0.4))
sc("Police used tear gas in Tirana. Authorities said more than three hundred protesters and police were injured.",
   P("cloud", 800, 600, 1.1), C(0, 300, 1400, 420, fmt="{:.0f}+", size=220, color="dark", at=0.35), T("injured", 1400, 610, 70, "dark", at=0.55))
sc("Same Saturday. Different lists. Some want cheaper rent, some want new schools, some want a new government. Like six people ordering at one restaurant.",
   P("clipboard", 450, 860, 0.8, text="RENT"), P("clipboard", 850, 860, 0.8, text="SCHOOLS", at=0.15), P("clipboard", 1250, 860, 0.8, text="PENSIONS", at=0.3),
   P("clipboard", 1650, 860, 0.8, text="NEW GOV", at=0.45))

# PART 5: WHY YOUNG PEOPLE ------------------------------------------------------------------
sc("One thing many of these protests share: they're led by young people. CNN calls it Gen Z's protest wave.",
   G(600, "fist", "angry", **STU), G(900, "fist", "angry", **STU2, at=0.15), P("phone", 1450, 880, 1.0, at=0.4), chapter="Part 5: Why the young")
sc("Sociologist María Silvestre told AP young Europeans feel, quote, a strong sense of uncertainty and a lack of control.",
   G(600, "present", "neutral", **PROF, label="sociologist"), P("speech", 1300, 480, 1.5, text="\"uncertainty and a|lack of control\"", at=0.35))
sc("And then, in her words, a spark suddenly ignites.",
   P("fire", 960, 880, 1.3, anim="pulse"), T("SPARK", 960, 330, 130, "orange", at=0.4))
sc("Think about the deal they were promised. Study hard, get a job, rent a flat, eventually buy one.",
   P("school", 450, 900, 0.7), {"arrow": [[650, 700], [850, 700]], "at": 0.2}, P("laptop", 1000, 880, 0.7, at=0.3), {"arrow": [[1150, 700], [1350, 700]], "at": 0.45},
   P("house", 1550, 900, 0.7, at=0.55))
sc("Now the school building leaks, the job pays what the rent costs, and the house is a picture on a phone.",
   P("school", 450, 900, 0.7), {"cross": [450, 700, 100], "at": 0.2}, P("pricetag", 960, 760, 0.8, text="RENT = PAY", at=0.35), P("phone", 1500, 880, 0.9, text="HOUSE", at=0.55))
sc("A French student leader put it simply, quote: people are just tired of waiting for an answer.",
   G(600, "point", "angry", **STU, label="student union"), P("speech", 1300, 480, 1.4, text="\"tired of waiting\"", at=0.35))
sc("And protests spread online the way memes do. A Rome school writes like in France, and suddenly France is a verb.",
   P("phone", 650, 880, 1.0), {"arrow": [[850, 650], [1150, 650]], "at": 0.3}, P("phone", 1350, 880, 1.0, at=0.4), T("#LIKEINFRANCE", 1000, 330, 80, "purple", at=0.6))

# PART 6: WHAT OFFICIALS SAY ------------------------------------------------------------------
sc("So what do the people in charge say? Depending on who you ask, you get very different explanations.",
   G(500, "point", "neutral", **PRES), G(960, "point", "angry", **LEFT, at=0.2), G(1420, "point", "angry", look=-1, **RIGHT, at=0.4), chapter="Part 6: Who's to blame?")
sc("France's President met student representatives on Friday, for the first time since the protests began. He promised more teachers and a deep overhaul of Parcoursup.",
   G(600, "present", "neutral", **PRES, label="the French President"), P("desk", 1100, 900, 0.9, at=0.25), G(1500, "stand", "neutral", look=-1, **STU, at=0.4))
sc("The students said that wasn't enough, and called for more protests until they see concrete action.",
   G(800, "shrug", "neutral", **STU), P("clipboard", 1350, 860, 1.0, text="PROMISES", at=0.3), T("NOT ENOUGH", 1350, 380, 90, "red", at=0.55))
sc("After the looting the week before, the President blamed far-left activists, and said those who looted will have to pay for the damage.",
   G(650, "point", "angry", **PRES), P("speech", 1300, 480, 1.4, text="\"will have to pay\"", at=0.35))
sc("A left-wing presidential candidate accused the police of provoking the disorder, and TV channels of only showing the clashes.",
   G(650, "point", "angry", **LEFT, label="left-wing candidate"), P("tv", 1300, 800, 1.0, at=0.3), G(1700, "stand", "neutral", look=-1, **COP, s=0.8, at=0.5))
sc("In America, President Trump wrote online that, quote, the migrants have taken over France. AP notes French authorities and police have not blamed immigrants for the violence.",
   G(600, "point", "angry", **RIGHT, label="the US President"), P("phone", 1150, 880, 0.9, at=0.3), T("no link found", 1500, 400, 80, "dark", at=0.6))
sc("Italy's Prime Minister thanked police, and wrote that the right to protest must be guaranteed, but so must people's right to live safely in their cities.",
   G(600, "present", "neutral", extras=["tie"], shirt="green", label="Italy's Prime Minister"), P("scale", 1300, 900, 1.0, at=0.35))
sc("Albania's Prime Minister refused to resign, and blamed his political opponents, saying the protests threaten Albania's path into the European Union.",
   G(700, "hips", "smug", **PRES, label="Albania's Prime Minister"), P("building", 1350, 900, 0.7, text="EU", at=0.3), T("EU?", 1350, 380, 100, "navy", at=0.5))
sc("So: the left blames the police and inequality, the right blames migration and radicals, governments blame troublemakers. We just count the facts.",
   P("scale", 960, 900, 1.3, anim="bob"), G(450, "shrug", "neutral", **LEFT, at=0.3), G(1500, "shrug", "neutral", look=-1, **RIGHT, at=0.45))

# PART 7: WHAT'S NEXT ----------------------------------------------------------------------------
sc("What comes next? A calendar that looks like a to-do list from a very angry personal assistant.",
   P("calendar", 960, 860, 1.4, text="NEXT"), G(1600, "point", "smug", look=-1, extras=LINDA, at=0.4), chapter="Part 7: What's next")
sc("October thirty-first: a youth group in Germany has called nationwide protests. This Saturday: French protesters say they'll march again.",
   P("calendar", 600, 860, 1.0, text="OCT 31"), T("GERMANY", 600, 360, 80, "dark", at=0.2), P("calendar", 1300, 860, 1.0, text="SAT", at=0.4), T("FRANCE", 1300, 360, 80, "navy", at=0.55))
sc("November fifth: a general strike by France's major unions. November eleventh: a general strike in Spain, its first in fourteen years, according to AP.",
   P("calendar", 600, 860, 1.0, text="NOV 5"), P("calendar", 1300, 860, 1.0, text="NOV 11", at=0.35), T("14 YEARS", 1300, 380, 90, "red", at=0.6))
sc("November twentieth: student unions in Britain and Italy plan a day of action. And in Spain, that early election.",
   P("calendar", 650, 860, 1.0, text="NOV 20"), P("ballot", 1300, 880, 1.0, at=0.4))
sc("France also elects a new president in about six months. The current one can't run again. So every party is watching these streets very closely.",
   P("ballot", 700, 880, 1.1), T("~6 MONTHS", 1350, 400, 110, "navy", at=0.3), P("eye", 1350, 700, 1.0, at=0.55))
sc("The big unknown is energy. If oil and fuel prices fall, some of the pressure fades. If they keep rising, the lists of demands probably get longer.",
   P("barrel", 650, 900, 1.0), P("arrowdown", 1050, 760, 0.8, at=0.3), P("arrowup", 1400, 760, 0.8, at=0.5), P("clipboard", 1750, 860, 0.7, text="+++", at=0.65))

# RECAP --------------------------------------------------------------------------------------------
sc("Quick recap. On one Saturday, people marched in at least six European countries. France counted four hundred ten thousand, and nearly a thousand arrests.",
   C(0, 6, 600, 420, fmt="{:.0f}", size=220, color="red"), C(0, 410000, 1300, 420, fmt="{:,.0f}", size=150, color="navy", at=0.3), chapter="Recap")
sc("The fuel is prices: eurozone inflation of three point eight percent, energy up almost nineteen, rents eating whole paycheques.",
   P("thermo", 600, 900, 1.0), P("gaspump", 1000, 900, 0.8, at=0.25), P("house", 1450, 900, 0.8, at=0.45))
sc("But the sparks are local: schools in France, housing in Spain and Portugal, corruption in Albania. And strikes are already scheduled for November.",
   P("school", 450, 900, 0.7), P("house", 900, 900, 0.7, at=0.2), P("building", 1350, 900, 0.6, text="GOV", at=0.4), P("calendar", 1750, 860, 0.7, text="NOV", at=0.6))
sc("And Dave? Dave flies home, happy to be back in normal life. He opens his energy bill.",
   P("plane", 700, 450, 1.0), G(1300, "hold", "happy", look=-1, extras=DAVE, at=0.35), P("envelope", 1600, 820, 0.8, at=0.6))
sc("Dave makes a little sign. Dave stands on his doorstep. Dave is now a movement of one.",
   G(800, "fist", "angry", extras=DAVE), *SIGN(1300, "WHY?!", 1.0, at=0.35), P("house", 1700, 900, 0.7, at=0.55), bg="yellow")
sc("Your turn. What costs too much where you live: rent, food, or fuel? Tell us in the comments. Dave is collecting signatures.",
   P("clipboard", 980, 860, 1.2, text="RENT?"), G(330, "point", "grin", extras=DAVE, at=0.4), T("?", 1650, 400, 200, "red", at=0.6))
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, text="SUBSCRIBE", at=0.4), bg="yellow")

script = {
    "id": "ep015",
    "title": "Why Is Half of Europe Protesting at the Same Time?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Saturday, October 24, 2026, people marched in France, Italy, Spain, Portugal, Albania and Belgium. France's Interior Ministry counted 410,000 "
        "protesters (organisers said nearly 800,000), with more than 70,000 police deployed and nearly 1,000 arrests. Is it one movement or many? "
        "We explain how it started with French high school students in September, the number underneath it all (eurozone inflation 3.8%, energy +18.8%), "
        "the local sparks (housing in Spain and Portugal, schools in France and Italy, corruption in Albania), what governments and their critics say, "
        "and what's next: strikes on November 5 (France) and November 11 (Spain).\n\n"
        "Dave and Linda are made-up characters. Real officials are shown as generic labelled stick figures; quotes are attributed as reported. "
        "We don't take sides: we just count the facts.\n\n"
        "Sources:\n"
        "Euronews, Protests sweep across Europe from France to Albania, Italy, Spain and Portugal (Oct 24, 2026): https://www.euronews.com/2026/10/24/protests-sweep-across-europe-from-france-to-albania-italy-spain-and-portugal\n"
        "Al Jazeera, Hundreds of thousands protest in France amid heightened police security (Oct 24, 2026): https://www.aljazeera.com/news/2026/10/24/france-braces-for-another-day-of-mass-protests-as-security-on-high-alert\n"
        "AP via Fortune, Europe's Gen Z takes to the streets (Oct 20, 2026): https://fortune.com/2026/10/20/europe-france-spain-albania-protests-young-people/\n"
        "CNN, Gen Z are leading the European protests. Here's why they're angry (Oct 24, 2026): https://www.cnn.com/2026/10/24/europe/gen-z-protests-europe-explainer-intl\n"
        "Open Magazine / ANI, Protests erupt across Europe over cost of living, pensions and housing: https://openthemagazine.com/world/cost-of-living-pensions-housing-fuel-protests-across-europe\n"
        "Eurostat flash estimate via GMK Center, Eurozone inflation 3.8% in September: https://gmk.center/en/news/inflation-in-the-eurozone-accelerated-to-3-8-in-september/\n\n"
        "#europe #protests #costofliving #france #spain #explained #stickfigure #news"
    ),
    "tags": ["europe protests", "france protests", "cost of living", "gen z protests", "spain housing", "italy protests", "albania protests",
             "eurozone inflation", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "EUROPE|IS|ANGRY?", "size": 200, "color": "black",
                  "guy": {"pose": "stand", "face": "scream", "look": -1, "extras": ["hair"]}, "guy_x": 1450, "guy_y": 2050, "guy_s": 5.0,
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep015.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

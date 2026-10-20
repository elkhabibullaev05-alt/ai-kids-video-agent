"""Episode 9: Brazil's presidential runoff (Oct 25, 2026) after the first Lula vs Flávio Bolsonaro debate (Oct 18), explained with stick figures."""
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




PRES = dict(extras=["tie"], shirt="orange", label="the President")      # Lula (generic, role label)
SEN = dict(extras=["tie"], shirt="teal", label="the Senator")           # Flávio Bolsonaro (generic, role label)
VOTER = dict(extras=["cap"], shirt="green")
POLL = dict(extras=["glasses"], shirt="purple", label="a pollster")
COP = dict(extras=["cap"], shirt="navy", label="federal police")

# COLD OPEN --------------------------------------------------------------------
sc("Dave has a new pen pal in Brazil. Her name is Ana. Her letter says: Sunday, I have to vote. Have to.",
   P("envelope", 700, 860, 1.3), G(1350, "hold", "confused", extras=DAVE, at=0.3), P("flag", 1500, 900, 0.8, at=0.55),
   cam={"from": [900, 640, 1.3], "to": [960, 540, 1.0]})
sc("In Brazil, voting is mandatory for most adults aged eighteen to seventy. Dave gasps. Dave has skipped three elections and a dentist.",
   T("MANDATORY", 960, 260, 130, "red"), G(600, "panic", "shock", extras=DAVE, at=0.35), P("calendar", 1400, 860, 1.0, text="SKIP x3", at=0.6))
sc("So what's the punishment for not voting? Normally a fine of three reais and fifty-one centavos.",
   P("wallet", 700, 880, 1.2, at=0.1), C(0, 3.51, 1300, 380, fmt="R${:.2f}", size=170, color="red", at=0.3, dur=1.6))
sc("That's about seventy US cents. Dave has paid more than that to park for eleven minutes.",
   T("≈ $0.70", 650, 360, 150, "green"), P("sign", 1350, 900, 1.0, text="P", at=0.3), P("stopwatch", 1650, 860, 0.8, text="11 min", at=0.6))
sc("And yet this Sunday, about a hundred and fifty-nine million registered voters choose the next leader of a country of two hundred and fourteen million.",
   C(0, 158.7, 960, 330, fmt="{:.1f} million", size=140, color="dark", dur=2.2), P("ballot", 960, 880, 1.2, at=0.5), bg="yellow")
sc("The choice: an eighty-year-old president going for a fourth term, or the eldest son of a former president who is serving a prison sentence.",
   G(600, "stand", "neutral", look=1, **PRES), T("VS", 960, 520, 140, "red", at=0.4), G(1320, "stand", "neutral", look=-1, at=0.6, **SEN))
S.append({"say": "So today's question: why is Brazil's election Lula versus another Bolsonaro, and why is it this close? Facts only. Stick figures, obviously.",
          "items": [P("tv", 980, 800, 1.4, text="WHY SO CLOSE?"), G(330, "think", "confused", extras=DAVE, at=0.4)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED ----------------------------------------------------------
sc("Rewind to Sunday, October the fourth. First round. Twelve candidates on the ballot.",
   P("calendar", 600, 860, 1.1, text="OCT 4"), T("12 candidates", 1250, 380, 110, "dark", at=0.4), chapter="Part 1: Round one")
sc("Flávio Bolsonaro, a senator from the conservative Liberal Party, got just over fifty-six million votes. That's forty-seven percent.",
   G(450, "fist", "grin", **SEN), C(0, 47.03, 1200, 360, fmt="{:.2f}%", size=170, color="teal", at=0.3))
sc("President Luiz Inácio Lula da Silva, of the left-wing Workers' Party, got almost fifty-four million. Forty-five percent.",
   G(450, "stand", "neutral", **PRES), C(0, 45.16, 1200, 360, fmt="{:.2f}%", size=170, color="orange", at=0.3))
sc("Ten other candidates shared the rest, just under eight percent. The best of them, Augusto Cury, got under three.",
   {"bars": {"values": [47.0, 45.2, 2.9, 2.2, 2.2], "labels": ["Flávio", "Lula", "Cury", "Santos", "Caiado"],
             "colors": ["teal", "orange", "grey", "grey", "grey"], "fmt": "{}%", "w": 900, "h": 460}, "x": 960, "y": 860})
sc("To win in round one, you need more than half of the valid votes. Nobody got there.",
   P("scale", 960, 900, 1.3), T("50% + 1", 960, 260, 140, "red", at=0.3), {"cross": [960, 560, 160], "at": 0.7})
sc("So the top two go to a runoff. Sunday, October twenty-fifth. Winner takes everything.",
   P("calendar", 700, 860, 1.1, text="OCT 25"), P("trophy", 1300, 880, 1.2, at=0.4, anim="bob"))
sc("Polls before round one had Lula ahead by about three points. He ended up two behind. Pollsters did some quiet sweating.",
   G(600, "stand", "worried", at=0, **POLL), P("clipboard", 900, 860, 0.9, text="+3?", at=0.3), T("−2", 1400, 380, 170, "red", at=0.6))
sc("More than one in five registered voters didn't vote at all. Seventy cents, remember? Some people decided it was worth it.",
   T("1 in 5", 700, 380, 170, "red"), P("wallet", 1300, 880, 1.0, text="$0.70", at=0.4), G(1650, "shrug", "neutral", extras=DAVE, at=0.6))
sc("Congress voted too. The Senator's Liberal Party won a hundred and twenty-one of five hundred and thirteen lower house seats. Lula's Workers' Party won seventy.",
   P("capitol", 960, 900, 1.2), {"bars": {"values": [121, 70], "labels": ["Liberal", "Workers'"], "colors": ["teal", "orange"],
   "fmt": "{}", "w": 520, "h": 360}, "x": 1500, "y": 820, "at": 0.4})

# PART 2: WHO ARE THEY -------------------------------------------------------------
sc("Meet the candidates. First, Lula. He's eighty. He already ran Brazil for eight years, starting in two thousand three.",
   G(600, "wave", "happy", **PRES), P("calendar", 1300, 860, 1.0, text="8 YEARS", at=0.4), chapter="Part 2: The candidates")
sc("His government is credited with helping lift around forty million Brazilians out of poverty. His supporters mention this. Often.",
   C(0, 40, 960, 360, fmt="{:.0f} million", size=160, color="green"), G(1550, "point", "happy", extras=VOTER, at=0.5))
sc("He also spent time in jail, from twenty eighteen to twenty nineteen, on corruption and money laundering charges.",
   P("calendar", 700, 860, 1.0, text="2018-19"), P("lock", 1250, 860, 1.2, at=0.4))
sc("Those convictions were later annulled by Brazil's Supreme Court in twenty twenty-one. He ran again in twenty twenty-two, and won.",
   P("scale", 600, 900, 1.1), {"stamp": "ANNULLED", "x": 1250, "y": 420, "size": 70, "w": 380, "at": 0.3}, P("trophy", 1550, 880, 0.9, at=0.65))
sc("If he wins Sunday, it's his fourth term, though not all in a row. Like a band that keeps announcing a farewell tour.",
   T("TERM 4", 960, 360, 160, "orange"), P("calendar", 600, 860, 0.9, text="1 2 _ 3", at=0.4), P("arrowup", 1450, 880, 0.9, at=0.6))
sc("Now, the challenger. Flávio Bolsonaro is forty-five, a senator, and the eldest son of former President Jair Bolsonaro.",
   G(1300, "hips", "smug", look=-1, **SEN), T("45", 600, 380, 170, "teal", at=0.3))
sc("His father was sentenced in twenty twenty-five to twenty-seven years for plotting a coup after losing the twenty twenty-two election.",
   C(0, 27, 700, 380, fmt="{:.0f} years", size=160, color="red"), P("scale", 1350, 900, 1.1, at=0.4))
sc("So the father can't run. He can't even vote. But a lot of people voting are thinking about him.",
   {"cross": [700, 560, 150]}, P("ballot", 700, 880, 1.0), G(1350, "think", "neutral", extras=VOTER, at=0.4), P("speech", 1500, 500, 0.8, text="...him?", at=0.6))
sc("The family business, it turns out, is now politics. Flávio's stepmother and two brothers also won seats this month.",
   P("house", 600, 900, 1.1, text="FAMILY"), P("capitol", 1300, 900, 1.0, at=0.35), T("+3 seats", 1350, 300, 110, "teal", at=0.6))
sc("Dave's family business is a lawn mower his uncle won't return. Different scale.",
   G(600, "facepalm", "tired", extras=DAVE), P("fan", 1250, 880, 0.9, text="MOWER", at=0.4))

# PART 3: THE POLLS ---------------------------------------------------------------
sc("So who's ahead? A Datafolha poll from October sixth and seventh: Flávio forty-nine, Lula forty-five.",
   G(400, "present", "neutral", **POLL), {"bars": {"values": [49, 45], "labels": ["Flávio", "Lula"], "colors": ["teal", "orange"],
   "fmt": "{}%", "w": 620, "h": 420}, "x": 1150, "y": 840, "at": 0.3}, chapter="Part 3: The polls")
sc("Count only valid votes, and that's fifty-two to forty-eight. Margin of error: two points either way.",
   T("52 – 48", 960, 360, 190, "dark"), T("± 2", 1550, 620, 110, "red", at=0.5))
sc("Then Quaest, October tenth to thirteenth: forty-six to forty-four. Pollsters call that a statistical tie. Everyone else calls it a coin toss.",
   T("46 – 44", 700, 360, 170, "dark"), P("dollar", 1350, 860, 1.0, at=0.4, anim="spin"), T("TIE?", 1350, 380, 120, "red", at=0.6))
sc("Here's the weird part. Fifty-four percent say they'd never vote for Flávio. Fifty-three percent say they'd never vote for Lula.",
   C(0, 54, 600, 380, fmt="{:.0f}%", size=170, color="teal"), C(0, 53, 1320, 380, fmt="{:.0f}%", size=170, color="orange", at=0.4),
   T("NEVER", 960, 640, 110, "red", at=0.7))
sc("Add those up and you get a hundred and seven. A lot of Brazilians aren't voting for someone. They're voting against someone.",
   T("107%", 960, 360, 200, "red", anim="pulse"), G(500, "shock", "shock", extras=DAVE, at=0.4), bg="yellow")
sc("And minds are made up. Ninety-one percent say their choice is final. Only nine percent might change.",
   C(0, 91, 700, 380, fmt="{:.0f}%", size=180, color="dark"), P("lock", 1350, 860, 1.1, at=0.4))

# PART 4: THE MAP ---------------------------------------------------------------------
sc("Brazil is huge, and it doesn't vote as one block. In the Northeast, Datafolha has Lula ahead sixty-one to thirty-five.",
   P("globe", 500, 880, 1.1), {"bars": {"values": [61, 35], "labels": ["Lula", "Flávio"], "colors": ["orange", "teal"], "fmt": "{}%",
   "w": 560, "h": 400}, "x": 1250, "y": 830, "at": 0.3}, chapter="Part 4: Who votes for whom")
sc("In the South, it flips: Flávio fifty-eight, Lula thirty-five.",
   {"bars": {"values": [58, 35], "labels": ["Flávio", "Lula"], "colors": ["teal", "orange"], "fmt": "{}%", "w": 560, "h": 400}, "x": 960, "y": 830},
   P("arrowdown", 1550, 880, 0.8, at=0.4))
sc("The Southeast, home to forty-two percent of voters, leans Flávio, fifty to forty-two. That's where Sunday is probably decided.",
   P("building", 600, 900, 1.1), P("building", 820, 900, 0.8, at=0.15), C(0, 42, 1350, 380, fmt="{:.0f}% of voters", size=110, color="dark", at=0.35))
sc("Evangelical Christians, about twenty-eight percent of voters, back Flávio sixty-nine to twenty-five.",
   G(500, "stand", "neutral", shirt="blue"), C(0, 69, 1250, 380, fmt="{:.0f}%", size=170, color="teal", at=0.3))
sc("The poorest forty-seven percent of voters back Lula, fifty-two to forty-one.",
   P("wallet", 600, 880, 1.1), C(0, 52, 1250, 380, fmt="{:.0f}%", size=170, color="orange", at=0.3))
sc("And the people who stayed home in round one? Quaest says they lean slightly toward Lula. Which explains his strategy.",
   P("house", 600, 900, 1.1), G(1100, "stand", "tired", extras=DAVE, at=0.3), P("megaphone", 1550, 820, 1.0, at=0.55))
sc("One analyst, Oliver Stuenkel of the FGV university in São Paulo, said Lula must mobilise non-voters, not just win over other candidates' fans.",
   G(500, "think", "neutral", extras=ECON, label="an analyst"), P("megaphone", 1100, 820, 1.0, at=0.35), P("house", 1550, 900, 0.9, at=0.6))
sc("Translation: Lula's campaign needs to knock on the doors of people who already ignored one election. Good luck to the doorbells.",
   P("house", 900, 900, 1.3), G(1450, "point", "worried", extras=VOTER, at=0.3), T("DING DONG?", 900, 300, 100, "dark", at=0.6))

# PART 5: THE DEBATE -----------------------------------------------------------------
sc("Which brings us to this Sunday night. The first head-to-head debate, on Band TV, one week before the vote.",
   P("tv", 960, 820, 1.4, text="LIVE"), P("podium", 450, 900, 0.9, at=0.3), P("podium", 1470, 900, 0.9, at=0.3),
   chapter="Part 5: The debate")
sc("It lasted about two hours. Analysts hoped for detailed plans aimed at undecided voters.",
   P("stopwatch", 700, 860, 1.1, text="2 h"), G(1300, "hold", "happy", extras=ECON, label="an analyst", at=0.3), P("clipboard", 1450, 760, 0.7, text="PLANS", at=0.5))
sc("The Associated Press says they got barbs, accusations and insults. Exchanges often involved family members, and were sometimes inaudible.",
   G(1300, "facepalm", "tired", extras=ECON, label="an analyst"), P("speech", 500, 420, 0.9, text="!!!"), P("speech", 800, 360, 0.8, text="?!", at=0.3),
   P("speech", 600, 600, 0.7, text="#@!", at=0.55))
sc("The Senator's message, as reported by AP: the economy gets better if you remove Lula from office and fight corruption.",
   P("podium", 700, 900, 1.0), G(700, "point", "angry", y=760, s=0.8, at=0.2, **SEN), P("arrowup", 1350, 880, 1.0, text="ECONOMY", at=0.5))
sc("He called Brazil's public debt a negative record, put it at eleven trillion reais, and promised to free up more than two hundred billion.",
   C(0, 11, 700, 380, fmt="R${:.0f} trillion", size=130, color="red"), C(0, 200, 1300, 640, fmt="R${:.0f} billion", size=110, color="green", at=0.5))
sc("Lula's message: look at my record. Welfare programs. Two investment-grade credit ratings in his earlier governments.",
   P("podium", 1200, 900, 1.0), G(1200, "present", "neutral", look=-1, y=760, s=0.8, at=0.2, **PRES), P("clipboard", 600, 860, 1.0, text="RECORD", at=0.4))
sc("He said Brazil paid off a thirty-billion-dollar debt to the IMF and now holds two hundred and seventy billion in reserves.",
   C(0, 30, 650, 360, fmt="${:.0f}B paid", size=120, color="dark"), C(0, 270, 1300, 600, fmt="${:.0f}B saved", size=120, color="green", at=0.45),
   P("moneybag", 1650, 900, 0.9, at=0.6))
sc("He also asked if Flávio would borrow Milei's chainsaw. That's a reference to Argentina's president, who campaigned on deep spending cuts.",
   P("speech", 700, 450, 1.0, text="CHAINSAW?"), P("globe", 1350, 880, 0.9, text="ARGENTINA", at=0.4))
sc("According to the Rio Times, Flávio didn't answer that one directly. Debates are where questions go to be politely ignored.",
   G(800, "shrug", "neutral", look=1, **SEN), P("speech", 1350, 450, 0.8, text="...", at=0.4))
sc("The tensest moment: Lula challenged both candidates to open their personal finances to the authorities before the runoff.",
   P("wallet", 960, 860, 1.4, anim="shake"), T("OPEN THE BOOKS", 960, 280, 110, "red", at=0.3), bg="yellow")

# PART 6: BOTH SIDES' PROBLEMS --------------------------------------------------------
sc("Why that challenge? Because corruption accusations are flying in both directions. Let's take them one at a time, same treatment for both.",
   P("scale", 960, 900, 1.4), T("SAME RULES", 960, 260, 110, "dark", at=0.3), chapter="Part 6: The accusations")
sc("On Sunday, Brazil's federal police asked the Supreme Court to open an investigation into Flávio over a money laundering accusation involving a lawyer close to him.",
   G(500, "hold", "neutral", **COP), P("envelope", 750, 760, 0.7, at=0.2), P("building", 1400, 900, 1.0, text="COURT", at=0.4))
sc("He's already under investigation over links to Daniel Vorcaro, a disgraced former banker who financed a movie about his father's life.",
   P("moneybag", 700, 900, 1.0), P("tv", 1300, 820, 1.0, text="THE MOVIE", at=0.4))
sc("Flávio denies any wrongdoing in both cases.",
   G(960, "stand", "neutral", **SEN), {"stamp": "DENIES", "x": 1450, "y": 420, "size": 70, "w": 300, "at": 0.3})
sc("On the other side, a pension-system fraud of more than a billion dollars has been linked to Lula's son. That scandal came up in the debate too.",
   P("clipboard", 600, 860, 1.1, text="PENSIONS"), C(0, 1, 1250, 380, fmt="${:.0f} billion+", size=130, color="red", at=0.35))
sc("So both camps say the other side is the corruption problem. Depending on who you ask, this election is a cleanup, or a comeback, or both.",
   P("scale", 960, 900, 1.3, anim="bob"), G(450, "point", "angry", look=1, **PRES), G(1470, "point", "angry", look=-1, **SEN))
sc("We don't pick a team here. We just count the facts.",
   T("WE COUNT FACTS", 960, 400, 130, "dark"), G(1500, "hips", "smug", extras=LINDA, at=0.3))

# PART 7: WHAT VOTERS WANT ------------------------------------------------------------
sc("So what do actual voters care about? In a September Quaest survey, twenty-eight percent named violence as Brazil's main problem.",
   C(0, 28, 700, 380, fmt="{:.0f}%", size=170, color="red"), P("barrier", 1350, 900, 1.0, at=0.4), chapter="Part 7: What voters want")
sc("Thirty-three percent said their income didn't go up at all in the past year. Another twenty-one percent said it rose slower than prices.",
   P("cart", 600, 900, 1.1), C(0, 33, 1150, 330, fmt="{:.0f}%", size=130, color="dark", at=0.25), C(0, 21, 1450, 620, fmt="{:.0f}%", size=120, color="red", at=0.55))
sc("Dave knows this feeling. His salary goes up by the stairs. His groceries take the elevator.",
   P("cart", 700, 900, 1.1, at=0, anim="bob"), G(1300, "cry", "cry", extras=DAVE, at=0.3), P("arrowup", 1650, 880, 0.8, at=0.5))
sc("Flávio's crime plan has twelve points. It would label criminal gangs narcoterrorist organisations and build maximum-security prisons modeled on El Salvador's.",
   P("clipboard", 600, 860, 1.1, text="12 POINTS"), P("lock", 1150, 860, 1.0, at=0.35), P("building", 1550, 900, 0.9, text="MAX", at=0.6))
sc("On the economy, he promises lower inflation, less government spending and a ceiling on public debt.",
   P("arrowdown", 600, 880, 1.0, text="INFLATION"), P("arrowdown", 1000, 880, 1.0, text="SPENDING", at=0.25), P("barrier", 1450, 900, 1.0, text="DEBT", at=0.5))
sc("He has also said he'd seek an amnesty for his father and others convicted over the January twenty twenty-three riots, or a pardon if that fails.",
   P("envelope", 700, 860, 1.1, text="AMNESTY"), P("calendar", 1300, 860, 1.0, text="JAN 2023", at=0.4))
sc("Lula promises more of the same, with extra focus on reducing inequality, growing industry and sustainability.",
   P("scale", 600, 900, 1.0), P("building", 1050, 900, 0.9, at=0.25), P("sun", 1500, 400, 0.8, at=0.5))

# PART 8: WHY THE WORLD CARES ----------------------------------------------------------
sc("Why should someone in Ohio or Manchester care? Brazil is about thirty-one percent of the whole economy of Latin America and the Caribbean.",
   P("globe", 700, 880, 1.2), C(0, 31, 1300, 380, fmt="{:.0f}%", size=180, color="green", at=0.3), chapter="Part 8: Why the world watches")
sc("And this vote is also a choice of direction. AP reports Flávio is an ally of President Trump. A win would increase U.S. influence in the region.",
   P("flag", 600, 900, 1.0), P("arrowup", 1100, 880, 0.9, at=0.3), P("globe", 1500, 880, 0.9, text="USA", at=0.5))
sc("A Lula win, AP says, would keep Brazil at a distance from Washington and deepen ties with China.",
   P("flag", 600, 900, 1.0), P("arrowup", 1100, 880, 0.9, at=0.3), P("globe", 1500, 880, 0.9, text="CHINA", at=0.5))
sc("Lula has called U.S. tariffs on Brazil political interference. Flávio says he'd stay pragmatic with China, but rethink Brazil's place in the BRICS group.",
   P("pricetag", 600, 860, 1.1, text="TARIFF"), P("clipboard", 1350, 860, 1.0, text="BRICS?", at=0.45))
sc("So for exporters, investors and coffee drinkers everywhere, Sunday matters. Brazil grows a lot of the world's coffee. Dave would like that noted.",
   P("coffee", 900, 880, 1.4, anim="bob"), G(1450, "hold", "grin", extras=DAVE, at=0.3))

# PART 9: WHAT'S NEXT -----------------------------------------------------------------
sc("What's next? One more debate, this Friday, on TV Globo. Then the runoff on Sunday, October twenty-fifth.",
   P("calendar", 600, 860, 1.0, text="FRI"), P("tv", 1000, 820, 0.9, text="ROUND 2", at=0.3), P("calendar", 1450, 860, 1.0, text="OCT 25", at=0.55),
   chapter="Part 9: What's next")
sc("Both sides held big rallies this weekend. Lula's supporters on Copacabana Beach in Rio, Flávio's on Paulista Avenue in São Paulo.",
   G(450, "fist", "happy", extras=VOTER), G(650, "wave", "happy", shirt="orange", at=0.15), G(1300, "fist", "happy", shirt="teal", at=0.35),
   G(1500, "wave", "happy", extras=["cap"], shirt="teal", at=0.45))
sc("Whoever wins, they'll face a split country. One academic, Vinicius de Carvalho of King's College London, said a Lula win would still need to answer some demands of the right.",
   P("scale", 960, 900, 1.2, anim="bob"), G(500, "think", "neutral", extras=ECON, label="an academic", at=0.3))
sc("And a Flávio win would come with a Congress where his party is the biggest, but far from a majority on its own.",
   P("capitol", 960, 900, 1.1), T("121 / 513", 960, 300, 120, "teal", at=0.4))
sc("Prediction markets lean Flávio. Polls say it's within the margin of error. And Brazilians have surprised the polls once already this month.",
   P("chart", 600, 880, 1.0), T("± 2", 1100, 400, 140, "red", at=0.3), P("clipboard", 1500, 860, 0.9, text="OOPS", at=0.6))

# RECAP / OUTRO -------------------------------------------------------------------------
sc("Quick recap. Round one: Flávio forty-seven, Lula forty-five, nobody over half.",
   T("47 – 45", 960, 380, 190, "dark"), chapter="Recap")
sc("The polls call it a near tie, and most voters strongly reject one of the two. Both camps trade corruption accusations, and both deny wrongdoing.",
   P("scale", 960, 900, 1.3, anim="bob"), T("TOO CLOSE", 960, 260, 110, "red", at=0.4))
sc("Sunday decides who runs a country of two hundred and fourteen million, and which way it leans: Washington, or Beijing.",
   P("globe", 960, 880, 1.3), P("arrowup", 600, 880, 0.8, text="USA", at=0.3), P("arrowup", 1320, 880, 0.8, text="CHINA", at=0.45))
sc("Dave, meanwhile, has written back to Ana. He told her he'd happily pay seventy cents to skip voting.",
   P("envelope", 700, 860, 1.2), G(1300, "type", "smug", extras=DAVE, at=0.3))
sc("Ana replied that she's voting anyway, because she has opinions. Dave sent her seventy cents. Linda says that's not how any of this works.",
   G(500, "panic", "shock", extras=DAVE), G(1400, "hips", "tired", extras=LINDA, at=0.4), {"cross": [900, 600, 120], "at": 0.6})
sc("Your turn: should voting be mandatory where you live? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("ballot", 1250, 880, 1.2, text="?", at=0.3))
sc("And if calm stick figures explaining loud news is your kind of thing, subscribe. We'll be counting the facts on Sunday night.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep009",
    "title": "Brazil Votes Sunday. Why Is It Lula vs. Another Bolsonaro?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "Brazil picks its president on Sunday, October 25, 2026: 80-year-old President Lula da Silva against Senator Flávio Bolsonaro, "
        "45, eldest son of former President Jair Bolsonaro, who is serving a 27-year sentence for plotting a coup. Round one ended 47% to 45%, "
        "the polls call it a near tie, and the first debate (Band TV, October 18) was mostly barbs. We go through the numbers, who votes for whom, "
        "both sides' corruption accusations and denials, the plans, and why the rest of the world is watching. Explained with stick figures, facts only.\n\n"
        "Dave, Linda and Ana are made-up characters. Real people are shown as generic labelled stick figures; statements are attributed as reported.\n\n"
        "Sources:\n"
        "AP, Brazil's Lula and Flávio Bolsonaro trade barbs in 1st debate only days before presidential runoff (Oct 18, 2026): https://www.clickorlando.com/news/2026/10/19/brazils-lula-and-flavio-bolsonaro-trade-barbs-in-1st-debate-only-days-before-presidential-runoff/\n"
        "Council on Foreign Relations, Brazil's 2026 Election: What to Know About the Lula-Bolsonaro Runoff: https://www.cfr.org/articles/brazils-2026-election-what-to-know-and-whats-at-stake\n"
        "Al Jazeera, Bolsonaro favourite to win: What Brazil's first round of elections tells us (Oct 5, 2026): https://www.aljazeera.com/news/2026/10/5/bolsonaro-favourite-to-win-what-brazils-first-round-of-election-tells-us\n"
        "The Rio Times, Lula and Flávio Clash in First Runoff Debate (Oct 2026): https://www.riotimesonline.com/lula-flavio-bolsonaro-band-runoff-debate-economy-2026/\n"
        "The Rio Times, Datafolha Runoff Poll Puts Flávio Bolsonaro Ahead of Lula (Oct 8, 2026): https://www.riotimesonline.com/brazil-datafolha-runoff-poll-flavio-lula-2026/\n"
        "The Rio Times, Quaest Poll Puts Flávio at 46%, Lula at 44% (Oct 14, 2026): https://www.riotimesonline.com/brazil-quaest-poll-flavio-46-lula-44-2026/\n"
        "Wikipedia (TSE results), 2026 Brazilian general election: https://en.wikipedia.org/wiki/2026_Brazilian_general_election\n"
        "Catholic World Report, Lula's convictions nullified (Mar 10, 2021): https://www.catholicworldreport.com/2021/03/10/lula-brazilian-ex-president-thanks-pope-francis-for-solidarity-after-convictions-nullified/\n\n"
        "#brazil #election #lula #bolsonaro #explained #stickfigure #news"
    ),
    "tags": ["brazil election", "brazil runoff", "lula", "flavio bolsonaro", "bolsonaro", "brazil 2026", "brazil debate",
             "latin america", "election explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "WHO|RUNS|BRAZIL?", "size": 190, "color": "black",
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep009.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

"""Episode 10: Alberta's Oct 19, 2026 referendum on whether to start a separation process (75% remain), explained with stick figures."""
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

PREM = dict(extras=["tie"], shirt="blue", label="the Premier")             # Alberta premier (generic, role label)
PM = dict(extras=["tie"], shirt="red", label="the Prime Minister")         # Canada PM (generic, role label)
SEP = dict(extras=["cap"], shirt="teal", label="a separatist leader")
UNI = dict(extras=["glasses"], shirt="red", label="a unity campaigner")
VOTER = dict(extras=["cap"], shirt="green")
JUDGE = dict(extras=["glasses"], shirt="dark", label="a judge")
COW = dict(extras=["cap"], shirt="brown")                                   # generic rancher

# COLD OPEN --------------------------------------------------------------------
sc("Dave's office calendar, Monday morning. Nine a.m.: a meeting to decide whether to have a meeting.",
   P("calendar", 700, 860, 1.3, text="9:00 ?"), G(1350, "think", "confused", extras=DAVE, at=0.35),
   cam={"from": [760, 640, 1.35], "to": [960, 540, 1.0]})
sc("Dave thinks this is the most pointless thing a grown-up can do. Then he turns on the news.",
   G(600, "facepalm", "tired", extras=DAVE), P("tv", 1300, 820, 1.2, text="NEWS", at=0.45))
sc("On the very same Monday, the Canadian province of Alberta held a vote on whether to hold a vote. About leaving Canada.",
   P("ballot", 600, 880, 1.2), T("A VOTE", 1250, 330, 120, "dark", at=0.3), T("ABOUT A VOTE", 1250, 500, 100, "red", at=0.55), bg="yellow")
sc("Not a meeting room. A whole province. Ten questions, roughly ten million paper ballots, every single one counted by hand.",
   C(0, 10, 960, 330, fmt="~{:.0f} million ballots", size=120, color="dark", dur=2.0), P("clipboard", 600, 860, 1.0, at=0.4),
   P("clipboard", 1350, 860, 1.0, at=0.55))
sc("And the answer came back loud. Roughly three out of four voters said: no thanks, we're staying.",
   C(0, 75, 960, 360, fmt="{:.0f}%", size=220, color="red", dur=1.8), P("canflag", 1500, 900, 1.0, at=0.5))
S.append({"say": "So today's question: why did Alberta vote on leaving Canada at all, and why did one in four say let's at least talk about it? Facts only. Stick figures, obviously.",
          "items": [P("tv", 980, 800, 1.4, text="WHY VOTE?"), G(330, "think", "confused", extras=DAVE, at=0.4)],
          "chapter": "Today's question"})

# PART 1: WHAT HAPPENED ----------------------------------------------------------
sc("Monday, October nineteenth. Albertans got a ballot with ten questions on it. The big one was number ten.",
   P("calendar", 600, 860, 1.1, text="OCT 19"), T("Q10", 1300, 380, 180, "red", at=0.4), chapter="Part 1: The vote")
sc("It asked: should Alberta remain a province of Canada, or should the government start the legal process to hold a binding referendum on separating?",
   P("sign", 520, 900, 1.1, text="REMAIN"), T("or", 960, 520, 100, "dark", at=0.35), P("sign", 1400, 900, 1.1, text="START", at=0.5))
sc("Read that twice. Even a win for the separation side would not have meant leaving. It would have meant another vote. Later.",
   T("NOT LEAVING", 960, 330, 150, "red"), P("calendar", 700, 860, 1.0, text="LATER", at=0.4), P("ballot", 1300, 880, 1.0, at=0.6))
sc("A voter in Edmonton, also named Dave, no relation, called it a referendum on a referendum. Our Dave feels seen.",
   G(500, "shrug", "neutral", extras=VOTER), G(1400, "point", "grin", extras=DAVE, at=0.4), T("Dave²", 960, 320, 110, "dark", at=0.6))
sc("With more than one point eight million votes counted, about seventy-five percent chose remain. About twenty-five percent chose to start the process.",
   {"bars": {"values": [75, 25], "labels": ["Remain", "Start process"], "colors": ["red", "teal"], "fmt": "{}%", "w": 760, "h": 460},
    "x": 960, "y": 860})
sc("Those numbers are unofficial. Elections Alberta says official results come on October twenty-ninth.",
   {"stamp": "UNOFFICIAL", "x": 700, "y": 420, "size": 70, "w": 420}, P("calendar", 1350, 860, 1.0, text="OCT 29", at=0.4))
sc("Voting day had hiccups. A hundred and six of about fourteen hundred polling stations opened late, mostly by ten to fifteen minutes.",
   C(0, 106, 650, 360, fmt="{:.0f}", size=180, color="red"), P("stopwatch", 1300, 860, 1.1, text="+15", at=0.4))

# PART 2: HOW WE GOT HERE --------------------------------------------------------
sc("So how does a province end up voting on whether to vote? It starts with a rule change.",
   P("clipboard", 960, 860, 1.3, text="RULES"), T("?", 1400, 400, 200, "red", at=0.4), chapter="Part 2: How we got here")
sc("In May twenty twenty-five, Alberta's government made it much easier for citizens to force a referendum with a petition.",
   P("calendar", 600, 860, 1.0, text="MAY 2025"), P("envelope", 1250, 860, 1.1, text="PETITION", at=0.35))
sc("Before: you needed signatures from twenty percent of all eligible voters. After: ten percent of the votes cast in the last election.",
   {"bars": {"values": [20, 10], "labels": ["Before", "After"], "colors": ["grey", "teal"], "fmt": "{}%", "w": 620, "h": 420},
    "x": 960, "y": 850}, P("arrowdown", 1550, 880, 0.9, at=0.5))
sc("And the time to collect them went from ninety days to a hundred and twenty.",
   C(90, 120, 960, 380, fmt="{:.0f} days", size=180, color="teal", dur=1.6), P("stopwatch", 1550, 860, 0.9, at=0.4))
sc("Both sides got busy. A unity petition, led by former deputy premier Thomas Lukaszuk, had more than four hundred thousand signatures verified.",
   G(500, "hold", "happy", **UNI), C(0, 404293, 1250, 380, fmt="{:,.0f}", size=130, color="red", at=0.3))
sc("A separatist petition from a group called Stay Free Alberta was checked too. Almost two hundred and twenty-three thousand valid signatures.",
   G(500, "hold", "neutral", **SEP), C(0, 223000, 1250, 380, fmt="~{:,.0f}", size=130, color="teal", at=0.3))
sc("But in May twenty twenty-six, an Alberta court struck that petition down.",
   G(600, "stand", "neutral", **JUDGE), P("scale", 1250, 900, 1.2, at=0.3), {"cross": [1250, 640, 160], "at": 0.65})
sc("The reason: First Nations had not been properly consulted, and separation would affect their treaty rights, which are protected by Canada's constitution.",
   P("clipboard", 600, 860, 1.1, text="TREATY"), P("scale", 1300, 900, 1.1, at=0.35), T("CONSULT FIRST", 960, 280, 100, "dark", at=0.6))
sc("The Premier disagreed with the ruling. A week later, in a televised address, she put a remain-or-start question on the October ballot anyway.",
   G(1100, "present", "neutral", look=-1, **PREM), P("tv", 520, 820, 1.0, text="LIVE", at=0.3), P("ballot", 1600, 880, 0.8, at=0.6))
sc("Here's the twist. The Premier herself opposes independence. She voted to stay.",
   G(960, "point", "neutral", **PREM), {"stamp": "VOTED REMAIN", "x": 1450, "y": 420, "size": 60, "w": 420, "at": 0.4}, bg="sky")
sc("AP reports she called the vote under pressure from separatists inside her own United Conservative Party. She said the goal was to understand the will of Albertans, and move on.",
   G(700, "shrug", "worried", **PREM), P("speech", 1250, 420, 1.0, text="MOVE ON", at=0.35), G(1550, "fist", "angry", extras=["cap"], shirt="blue", at=0.6))
sc("Critics on both sides were unhappy. Separatists said she wasn't on their team. Federalists said she shouldn't have held the vote at all.",
   G(450, "point", "angry", look=1, **SEP), G(960, "facepalm", "tired", look=1, **PREM), G(1470, "point", "angry", look=-1, **UNI))
sc("Opposition figures put the cost somewhere between a hundred and thirty and two hundred million Canadian dollars. The exact bill isn't known yet.",
   P("moneybag", 600, 900, 1.1), T("$130M – $200M ?", 1250, 380, 110, "red", at=0.35))

# PART 3: WHY ANGRY --------------------------------------------------------------
sc("Now the big why. Why would anyone in Alberta want to leave one of the world's richest countries?",
   P("globe", 960, 880, 1.3), T("WHY LEAVE?", 960, 280, 130, "red", at=0.4), chapter="Part 3: Why Alberta is annoyed")
sc("Start with the ground. AP says Alberta has the world's fourth-largest proven oil reserves.",
   P("barrel", 600, 900, 1.2), C(0, 4, 1250, 380, fmt="#{:.0f}", size=220, color="dark", at=0.3, dur=1.2), P("barrel", 800, 900, 0.9, at=0.5))
sc("Most of the anger is about who controls that oil. Many Albertans feel Ottawa, the national capital, makes the rules for an industry it doesn't depend on.",
   P("capitol", 1350, 900, 1.1, text="OTTAWA"), P("barrel", 500, 900, 1.0, at=0.3), {"arrow": [[680, 640], [1150, 640]], "color": "red", "at": 0.5})
sc("This feud is old. In nineteen eighty, the federal government's National Energy Program added price controls and a new tax on oil and gas revenue.",
   P("calendar", 600, 860, 1.1, text="1980"), P("pricetag", 1250, 860, 1.1, text="TAX", at=0.35))
sc("Alberta's premier back then answered by cutting crude output by sixty thousand barrels. A province-sized slammed door.",
   C(0, 60000, 960, 360, fmt="-{:,.0f} bbl", size=140, color="red"), P("barrel", 1550, 900, 0.9, at=0.4, anim="shake"))
sc("Then there's money. Albertans pay more in federal taxes than Ottawa spends back in the province. Statistics Canada put the gap at twenty-seven billion dollars in twenty fifteen.",
   P("wallet", 600, 880, 1.1), C(0, 27, 1250, 380, fmt="${:.0f} billion", size=140, color="red", at=0.3))
sc("The current Premier blames the previous prime minister, Justin Trudeau, accusing him of trying to crush oil production for his climate agenda.",
   G(600, "point", "angry", **PREM), P("barrel", 1150, 900, 0.9, at=0.3), P("arrowdown", 1500, 880, 0.9, at=0.5))
sc("His supporters saw those policies as cutting emissions. Depending on who you ask, it was climate policy or an attack on Alberta. Often both, in the same family dinner.",
   P("sun", 600, 400, 0.9), P("barrel", 1350, 900, 1.0, at=0.3), P("dish", 960, 880, 1.0, at=0.55), G(1650, "shrug", "worried", extras=DAVE, at=0.7))
sc("Former premier Jason Kenney says separatist parties usually got just one to two percent of the vote. So what changed?",
   T("1–2%", 960, 360, 200, "teal"), G(1500, "think", "neutral", extras=ECON, at=0.4))
sc("According to Kenney, anger over COVID-19 restrictions brought many activists into politics, and some later joined the separatist movement.",
   P("clipboard", 600, 860, 1.0, text="RULES"), G(1100, "fist", "angry", extras=["cap"], shirt="teal", at=0.3), G(1350, "fist", "angry", shirt="teal", at=0.45))
sc("Then, in twenty twenty-five, the federal Liberals won a fourth election in a row. AP says that's when the pressure for a referendum took off.",
   T("4 in a row", 960, 360, 140, "red"), P("ballot", 600, 880, 1.0, at=0.3), P("arrowup", 1450, 880, 1.0, at=0.5))
sc("Dave can relate. His in-laws also won four Christmas hosting duties in a row. Nobody voted on that either.",
   P("house", 600, 900, 1.1, text="XMAS x4"), G(1300, "cry", "cry", extras=DAVE, at=0.35))

# PART 4: THE AMERICAN ANGLE -----------------------------------------------------
sc("Then add the neighbour. Canada and the United States are in a long trade war.",
   P("canflag", 600, 900, 1.0), P("pricetag", 960, 860, 1.0, text="TARIFF", at=0.3), P("sign", 1360, 900, 1.0, text="USA", at=0.5),
   chapter="Part 4: The neighbour")
sc("AP notes President Trump has repeatedly talked about making Canada the fifty-first U.S. state.",
   T("51st?", 960, 360, 200, "red", anim="pulse"), P("capitol", 1550, 900, 0.9, at=0.4))
sc("In January, U.S. Treasury Secretary Scott Bessent called Alberta a natural partner for America. Elon Musk posted that Alberta should separate.",
   G(550, "present", "neutral", extras=["tie"], shirt="navy", label="a U.S. official"), P("phone", 1150, 860, 1.0, text="POST", at=0.4),
   P("speech", 1500, 420, 0.9, text="SEPARATE!", at=0.6))
sc("The Alberta Prosperity Project, a separatist group, met U.S. State Department officials three times. Those talks were described as routine, with no commitments.",
   P("building", 1300, 900, 1.0, text="STATE DEPT"), G(600, "wave", "happy", **SEP), T("x3", 1300, 300, 130, "dark", at=0.5))
sc("And here's the odd effect. AP says Trump's threats actually helped the Prime Minister gain support in Alberta, where Liberal prime ministers are usually unpopular.",
   G(960, "fist", "grin", **PM), P("arrowup", 1450, 880, 1.0, at=0.4), bg="yellow")
sc("Nothing unites a family like a neighbour leaning over the fence saying, nice house, I'll take it.",
   P("house", 600, 900, 1.2), G(1100, "hips", "angry", extras=LINDA, at=0.3), G(1600, "point", "smug", extras=["cap"], shirt="grey", at=0.5))
sc("The Prime Minister grew up in Alberta. He partnered with the Premier on a new pipeline to ship more oil sands crude overseas, something that went nowhere under his predecessor.",
   G(330, "stand", "happy", **PM), P("pipeline", 960, 900, 0.85, at=0.3), G(1620, "stand", "happy", look=-1, at=0.5, **PREM))

# PART 5: WHAT EACH SIDE SAYS -----------------------------------------------------
sc("So what does each side say now? Same treatment for everyone. Let's start with the winners.",
   P("scale", 960, 900, 1.4), T("SAME RULES", 960, 260, 110, "dark", at=0.3), chapter="Part 5: What each side says")
sc("The Prime Minister wrote: Albertans chose Canada. He said the result is absolutely clear.",
   G(700, "wave", "happy", **PM), P("speech", 1300, 420, 1.0, text="CLEAR", at=0.35))
sc("But he also said the quarter who voted to start the process shouldn't all be seen as separatists. Some were sending a message to Ottawa.",
   T("25%", 700, 360, 190, "teal"), P("envelope", 1300, 860, 1.1, text="OTTAWA", at=0.4))
sc("The Premier said Albertans have voted for a stronger Alberta in a united Canada. CBC reports she pledged not to hold a second separation referendum.",
   G(960, "present", "happy", **PREM), {"cross": [1500, 600, 120], "at": 0.5}, P("ballot", 1500, 880, 0.9, at=0.4))
sc("Unity campaigner Thomas Lukaszuk said Canada is a solid country, united from coast to coast to coast. Canada has three coasts. It likes to mention this.",
   G(600, "fist", "happy", **UNI), T("COAST x3", 1300, 380, 130, "red", at=0.4), P("ship", 1350, 880, 0.8, at=0.6))
sc("Now the other side. Jeffrey Rath of the Alberta Prosperity Project said: we're not going anywhere. He'd said he'd be thrilled with thirty percent.",
   G(600, "fist", "angry", **SEP), T("30%?", 1300, 360, 170, "teal", at=0.45))
sc("He wants the Premier replaced as party leader, and said the movement could form a new pro-independence party.",
   G(600, "point", "angry", **SEP), G(1350, "stand", "worried", look=-1, at=0.3, **PREM), P("sign", 1650, 900, 0.8, text="NEW?", at=0.6))
sc("Keith Wilson of Let Alberta Decide said it's fair to say at least a quarter of Albertans feel Alberta needs to be treated better.",
   G(600, "stand", "neutral", extras=["glasses"], shirt="teal", label="a separatist leader"), C(0, 25, 1300, 380, fmt="{:.0f}%", size=180, color="teal", at=0.35))
sc("So: one side says the matter is settled. The other says it has only just begun. We don't pick a team here. We just count the facts.",
   P("scale", 960, 900, 1.3, anim="bob"), G(450, "hips", "smug", look=1, **UNI), G(1470, "fist", "angry", look=-1, **SEP),
   T("WE COUNT FACTS", 960, 260, 110, "dark", at=0.6))

# PART 6: THE OTHER NINE QUESTIONS -------------------------------------------------
sc("Remember, there were nine other questions. Mostly about immigration and about who's in charge, Alberta or Ottawa.",
   T("Q1 – Q9", 960, 360, 180, "dark"), P("clipboard", 1550, 860, 0.9, at=0.4), chapter="Part 6: The other nine questions")
sc("Early counts, still unofficial: about fifty-nine percent said yes to Alberta taking more control over immigration.",
   C(0, 59, 700, 380, fmt="{:.0f}% yes", size=150, color="green"), P("plane", 1400, 500, 1.0, at=0.4))
sc("About fifty-seven percent backed limiting provincial health care, schools and social services to citizens, permanent residents and approved immigrants.",
   C(0, 57, 700, 380, fmt="{:.0f}% yes", size=150, color="green"), P("school", 1400, 900, 0.9, at=0.4))
sc("About sixty-three percent said yes to requiring proof of citizenship to vote in provincial elections.",
   C(0, 63, 700, 380, fmt="{:.0f}% yes", size=150, color="green"), P("ballot", 1400, 880, 1.1, at=0.4))
sc("The constitutional ones were coin tosses. Letting provinces pick some judges: fifty point seven percent yes. Provincial laws beating federal ones: just under fifty-one.",
   {"bars": {"values": [50.7, 50.9], "labels": ["Judges", "Law priority"], "colors": ["green", "green"], "fmt": "{}%", "w": 620, "h": 420},
    "x": 800, "y": 850}, P("dollar", 1550, 860, 0.9, at=0.5, anim="spin"))
sc("And opting out of federal programs while keeping the federal money? About fifty-two percent said no. Even voters have limits on having cake and eating it.",
   C(0, 52, 700, 380, fmt="{:.0f}% no", size=150, color="red"), P("moneybag", 1350, 900, 1.0, at=0.4), {"cross": [1350, 760, 130], "at": 0.7})
sc("Supporters say these votes strengthen Alberta's hand with Ottawa. Critics note several need other provinces to agree. Both can be true.",
   P("scale", 960, 900, 1.2), G(450, "point", "happy", extras=["cap"], shirt="blue", at=0.3), G(1470, "think", "worried", extras=ECON, at=0.45))

# PART 7: COULD A PROVINCE EVEN LEAVE ---------------------------------------------
sc("Big question: could a Canadian province actually leave, even if it wanted to?",
   P("globe", 960, 880, 1.3), T("CAN IT?", 960, 280, 130, "red", at=0.4), chapter="Part 7: Could it even leave?")
sc("Canada's constitution has no button for one province to leave on its own. It would take a constitutional amendment, following a law called the Clarity Act.",
   P("clipboard", 600, 860, 1.1, text="CLARITY ACT"), P("lock", 1300, 860, 1.1, at=0.4))
sc("Translation: years of negotiations, a clear question, and a clear majority. Not a long weekend.",
   P("calendar", 600, 860, 1.0, text="YEARS"), P("calendar", 900, 860, 0.8, text="YEARS", at=0.2), P("calendar", 1150, 860, 0.6, text="YEARS", at=0.35),
   G(1550, "stand", "tired", extras=DAVE, at=0.5))
sc("Canada has been here before. Quebec voted on leaving twice, in nineteen eighty and nineteen ninety-five.",
   P("calendar", 600, 860, 1.0, text="1980"), P("calendar", 1300, 860, 1.0, text="1995", at=0.35))
sc("Nineteen ninety-five was a nail-biter. No won with fifty point five eight percent. Alberta's result is not that.",
   C(0, 50.58, 700, 380, fmt="{:.2f}%", size=160, color="dark"), T("vs 75%", 1350, 600, 140, "red", at=0.5), bg="yellow")
sc("And money matters. Economist Trevor Tombe estimated separation would cut Alberta's economic activity by about twenty billion dollars. Roughly thirty-nine hundred per Albertan.",
   G(500, "present", "neutral", extras=ECON, label="an economist"), C(0, 3900, 1250, 380, fmt="${:,.0f} each", size=130, color="red", at=0.35))
sc("Separatists dispute that kind of estimate. They argue an independent Alberta would keep far more of its own oil money.",
   G(600, "point", "angry", **SEP), P("barrel", 1150, 900, 1.0, at=0.3), G(1550, "shrug", "neutral", extras=ECON, at=0.5))

# PART 8: WHAT'S NEXT --------------------------------------------------------------
sc("What's next? Official results on October twenty-ninth. Results for the other nine questions are being confirmed this week.",
   P("calendar", 700, 860, 1.1, text="OCT 29"), P("clipboard", 1300, 860, 1.0, text="Q1-Q9", at=0.4), chapter="Part 8: What's next")
sc("And polling from the Angus Reid Institute found most Albertans believe the separatist movement will never really go away.",
   G(500, "present", "neutral", extras=["glasses"], shirt="purple", label="a pollster"), T("NEVER ENDS?", 1250, 380, 120, "teal", at=0.4))
sc("So the question is settled for now. The feelings behind it are not.",
   T("SETTLED?", 960, 360, 160, "dark"), {"stamp": "FOR NOW", "x": 1350, "y": 560, "size": 70, "w": 340, "at": 0.4})

# RECAP / OUTRO -------------------------------------------------------------------------
sc("Quick recap. Alberta voted on whether to start the process for a real separation vote. About three in four said no.",
   T("75 – 25", 960, 380, 190, "dark"), chapter="Recap")
sc("The anger is old: oil, taxes, and a feeling that Ottawa doesn't listen. A trade war and annexation talk next door pulled many people the other way.",
   P("barrel", 600, 900, 1.0), P("capitol", 1000, 900, 0.9, at=0.25), P("canflag", 1400, 900, 0.9, at=0.45))
sc("The winners say it's over. The separatists say they're not going anywhere. Official results arrive October twenty-ninth.",
   P("scale", 960, 900, 1.3, anim="bob"), P("calendar", 1550, 860, 0.8, text="OCT 29", at=0.4))
sc("Dave, inspired, cancels his nine a.m. meeting about whether to have a meeting.",
   P("calendar", 700, 860, 1.1, text="9:00"), {"cross": [700, 780, 120], "at": 0.3}, G(1350, "fist", "grin", extras=DAVE, at=0.4))
sc("His boss schedules a ten a.m. meeting about why he cancelled the nine a.m. Linda says that's democracy, at a smaller scale.",
   P("calendar", 600, 860, 1.0, text="10:00"), G(1050, "cry", "cry", extras=DAVE, at=0.3), G(1500, "hips", "smug", extras=LINDA, at=0.5))
sc("Your turn: should a region be able to vote on leaving its country? And if yes, how big a majority should it need? Tell us in the comments.",
   G(500, "point", "neutral", extras=LINDA), P("ballot", 1250, 880, 1.2, text="?", at=0.3))
sc("And if calm stick figures explaining loud news is your kind of thing, subscribe. No meeting required.",
   P("tv", 1150, 800, 1.3, text="SUBSCRIBE"), G(420, "wave", "happy", extras=DAVE, at=0.3), hold=1.2)

script = {
    "id": "ep010",
    "title": "Alberta Voted on a Vote About Leaving Canada. Why?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Monday, October 19, 2026, Alberta held its first-ever vote on separation: not on leaving Canada, but on whether to START the legal process "
        "for a binding separation referendum. With more than 1.8 million votes counted, about 75% chose to remain (unofficial; official results Oct 29). "
        "We go through how the vote got on the ballot, why many Albertans are angry with Ottawa (oil, taxes, history), the U.S. trade war and "
        "'51st state' talk, what each side says now, the nine other questions, and whether a province could even leave. Stick figures, facts only.\n\n"
        "Dave and Linda are made-up characters. Real people are shown as generic labelled stick figures; statements are attributed as reported.\n\n"
        "Sources:\n"
        "AP via PBS NewsHour, Alberta voters reject independence from Canada in victory for Carney (Oct 20, 2026): https://www.pbs.org/newshour/world/alberta-voters-reject-independence-from-canada-in-victory-for-carney\n"
        "Al Jazeera, Alberta voters reject separation from Canada, early results show (Oct 20, 2026): https://www.aljazeera.com/news/2026/10/20/alberta-voters-reject-separation-from-canada-early-results-show\n"
        "Axios, Alberta referendum results: Voters reject push for independence from Canada (Oct 20, 2026): https://www.axios.com/2026/10/20/alberta-canada-referendum-results-remain\n"
        "CTV News / CP24 live updates (Oct 20, 2026): https://www.cp24.com/news/canada/2026/10/20/albertans-reject-separation-in-historic-vote-ctv-news-projects-live-updates/\n"
        "Global News, Albertans mixed on other referendum questions after rejecting separation: https://globalnews.ca/news/12109093/alberta-referendum-separation-other-results/\n"
        "Wikipedia, 2026 Alberta independence referendum / Alberta separatism (background, petitions, polls): https://en.wikipedia.org/wiki/2026_Alberta_independence_referendum\n"
        "Elections Québec, 1995 referendum results: https://www.electionsquebec.qc.ca/en/results-and-statistics/1995-referendum-on-quebecs-accession-to-sovereignty/\n\n"
        "#alberta #canada #referendum #explained #stickfigure #news"
    ),
    "tags": ["alberta referendum", "alberta separation", "alberta independence", "canada", "alberta", "referendum explained",
             "canada news", "carney", "danielle smith", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "VOTE TO|VOTE?", "size": 210, "color": "black",
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep010.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

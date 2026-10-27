"""Episode 16: Serbia snap election Oct 25, 2026 — the Student List wins a majority, Vucic concedes. Explained with stick figures."""
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


def SFLAG(x, y=900, s=1.0, at=0):
    """Plain red-blue-white tricolour on a pole (no coat of arms)."""
    w, h = int(300 * s), int(66 * s)
    top = y - int(420 * s)
    return [{"box": [x - int(5 * s), top, int(10 * s), y - top], "color": "dark", "at": at},
            {"box": [x, top, w, h], "color": "red", "at": at},
            {"box": [x, top + h, w, h], "color": "blue", "at": at},
            {"box": [x, top + 2 * h, w, h], "color": "white", "at": at}]


LEADER = dict(extras=["tie"], shirt="navy", label="Serbia's leader")
STUL = dict(extras=["glasses"], shirt="orange")
OBS = dict(extras=["glasses", "cap"], shirt="green")

# COLD OPEN --------------------------------------------------------------------
sc("Sunday night. Belgrade. A man in a suit walks up to a microphone, and says five words that politicians almost never practise.",
   P("podium", 960, 900, 1.2), G(960, "stand", "neutral", look=1, at=0.3, **LEADER), P("cloud", 1600, 260, 0.8, at=0.6),
   cam={"from": [960, 600, 1.35], "to": [960, 540, 1.0]}, bg="purple")
sc("Quote: it is clear that we have lost these elections.",
   P("podium", 700, 900, 1.1), G(700, "facepalm", "tired", look=1, **LEADER), P("speech", 1350, 430, 1.6, text="\"we have lost\"", at=0.3))
sc("The man is Aleksandar Vučić. In one job or another, his party has run Serbia since 2012. Fourteen years.",
   G(560, "stand", "neutral", **LEADER), C(2012, 2026, 1300, 420, fmt="{:.0f}", size=220, color="navy", at=0.3), T("14 years", 1300, 620, 90, "red", at=0.7))
sc("And who beat him? Not a famous rival. Not a big party. A list of two hundred and fifty mostly unknown people, started by students.",
   G(450, "fist", "grin", **STU), G(700, "fist", "happy", **STU2, at=0.15), G(950, "wave", "happy", **PROF, at=0.3),
   C(0, 250, 1500, 420, fmt="{:.0f}", size=240, color="orange", at=0.45), T("unknowns", 1500, 600, 80, "dark", at=0.7))
sc("Doctors. Professors. Actors. Farmers. Imagine a job interview where the job is: run a country.",
   G(400, "stand", "neutral", extras=["glasses"], shirt="white", label="doctor"), G(760, "present", "neutral", **PROF, at=0.2, label="professor"),
   G(1120, "wave", "grin", extras=["hair"], shirt="pink", at=0.4, label="actor"), G(1480, "hold", "neutral", extras=["cap"], shirt="brown", at=0.6, label="farmer"))
sc("Meanwhile, Dave is in his kitchen, reading the news, and asking the only sensible question.",
   P("coffee", 1250, 860, 1.2), G(700, "think", "confused", extras=DAVE, at=0.2), T("SERBIA?", 1300, 380, 110, "red", at=0.55), bg="yellow")
S.append({"say": "Today: how did a student protest turn into a governing majority in two years? What do the numbers say? And what happens next?",
          "items": [*SFLAG(820, 900, 1.2), G(380, "think", "confused", extras=DAVE, at=0.3), T("HOW?", 1500, 380, 160, "red", at=0.6)],
          "chapter": "Today's question"})

# PART 1: THE NUMBERS -----------------------------------------------------------
sc("First, the result. Serbia's parliament has two hundred and fifty seats. To govern alone, you need one hundred and twenty six.",
   P("capitol", 700, 900, 1.0), C(0, 250, 1350, 360, fmt="{:.0f}", size=200, color="navy"), T("majority: 126", 1350, 560, 90, "red", at=0.55),
   chapter="Part 1: The numbers")
sc("On Monday, the election commission published figures from eight thousand and seventy-seven of eight thousand three hundred ninety-two polling stations.",
   P("clipboard", 650, 860, 1.2, text="8,077"), T("of 8,392", 1150, 330, 110, "dark", at=0.35), P("booth", 1550, 900, 0.8, at=0.6))
sc("The Student List: fifty-two point five four percent of the vote.",
   C(0, 52.54, 960, 420, fmt="{:.2f}%", size=240, color="orange"), G(1600, "fist", "grin", look=-1, **STU, at=0.5))
sc("United Serbia, the list led by Vučić's Serbian Progressive Party: thirty-nine point two nine percent.",
   C(0, 39.29, 960, 420, fmt="{:.2f}%", size=240, color="navy"), G(1600, "stand", "worried", look=-1, **LEADER, at=0.5))
sc("In seats, that's projected at one hundred and forty for the students, and one hundred and three for United Serbia.",
   {"bars": {"values": [140, 103, 7], "labels": ["Student List", "United Serbia", "others"], "colors": ["orange", "navy", "grey"], "fmt": "{}", "w": 900, "h": 440}, "x": 860, "y": 830},
   T("126 needed", 1650, 300, 70, "red", at=0.5))
sc("The last seven seats go to lists representing minorities: Hungarians in Vojvodina, Albanians, Bosniaks and others.",
   C(0, 7, 700, 420, fmt="{:.0f}", size=260, color="grey"), T("minority lists", 700, 620, 80, "dark", at=0.3), P("ballot", 1400, 880, 1.0, at=0.5))
sc("These are not final official results. But the man who lost has already said he lost, which usually settles the suspense.",
   {"stamp": "NOT FINAL", "x": 700, "y": 450, "size": 80, "w": 420}, G(1350, "shrug", "tired", look=-1, **LEADER, at=0.45))
sc("Then there's turnout. Sixty-eight point seven eight percent of voters showed up. About six and a half million people were eligible.",
   C(0, 68.78, 900, 400, fmt="{:.2f}%", size=230, color="green"), T("turnout", 900, 580, 80, "dark", at=0.4), P("booth", 1600, 900, 0.9, at=0.5))
sc("That is the highest turnout since Yugoslavia broke up in the early nineties. More than thirty years.",
   P("calendar", 600, 860, 1.1, text="1992"), {"arrow": [[820, 640], [1180, 640]], "at": 0.3}, P("calendar", 1400, 860, 1.1, text="2026", at=0.45),
   {"stamp": "RECORD", "x": 1000, "y": 330, "size": 80, "w": 330, "at": 0.7})
sc("When that many people turn up, it's not a normal election. People had something to say.",
   *[G(260 + i * 200, "stand", "neutral", extras=(["hair"], ["bun"], ["cap"], ["glasses"], ["hair"], ["bun"], ["cap"], ["hair"])[i], s=0.7, at=i * 0.08, walk=True) for i in range(8)],
   T("LINE", 960, 330, 120, "dark", at=0.7))

# PART 2: HOW IT STARTED ---------------------------------------------------------
sc("To understand Sunday, go back almost two years, to the city of Novi Sad.",
   P("calendar", 700, 860, 1.1, text="NOV 2024"), T("NOVI SAD", 1350, 420, 110, "dark", at=0.35), chapter="Part 2: How it started", bg="paper")
sc("On November first, twenty twenty-four, the concrete canopy at the town's railway station collapsed. Sixteen people were killed.",
   P("building", 960, 900, 1.2, text="STATION"), T("16 killed", 960, 300, 110, "dark", at=0.4), bg="paper")
sc("People wanted to know who was responsible, and why. That question never went away.",
   P("building", 600, 900, 1.0, text="STATION"), P("magnifier", 1250, 700, 1.2, at=0.3), T("WHO? WHY?", 1350, 330, 100, "dark", at=0.55), bg="paper")
sc("Protests began, and students led them. Universities became the centre of the movement.",
   P("school", 600, 900, 1.0), P("barrier", 1000, 900, 0.8, at=0.3), G(1350, "stand", "neutral", look=-1, **STU, at=0.45), G(1600, "stand", "neutral", look=-1, **STU2, at=0.6))
sc("Over time, the anger grew from one disaster into something bigger: accusations of corruption, and of a government with too much control.",
   T("ONE DISASTER", 600, 380, 80, "dark"), {"arrow": [[900, 380], [1150, 380]], "at": 0.3},
   T("CORRUPTION?", 1450, 330, 80, "red", at=0.45), T("CONTROL?", 1450, 460, 80, "red", at=0.6), G(960, "think", "worried", extras=LINDA, at=0.7))
sc("Vučić and his party deny those accusations. He called the demonstrators blockaders, and accused them of trying to destabilise the country.",
   G(600, "point", "angry", **LEADER), P("speech", 1250, 450, 1.5, text="\"blockaders\"", at=0.3), *SIGN(1650, "NO!", 0.7, at=0.6))
sc("He also described the movement as a foreign-led attempt to remove him. The students say they are just Serbian students. Depending on who you ask.",
   G(500, "point", "angry", **LEADER), P("globe", 960, 880, 0.9, at=0.25), G(1450, "shrug", "neutral", look=-1, **STU, at=0.5, label="students"))
sc("The protests lasted almost two years. Along the way, some opposition parties stopped running their own candidates and backed the students instead.",
   *SIGN(400, "16", 0.8), *SIGN(750, "JUSTICE", 0.8, at=0.15), G(1150, "fist", "angry", **STU, at=0.3), G(1550, "wave", "happy", extras=["tie"], shirt="grey", look=-1, at=0.55, label="opposition"))
sc("Picture the opposition parties as bands who agree to let the new kid sing lead. Rare. Slightly humbling. Apparently effective.",
   P("megaphone", 900, 700, 1.3), G(500, "hold", "grin", **STU), G(1300, "shrug", "smug", look=-1, extras=["tie"], shirt="grey", at=0.3),
   G(1600, "shrug", "tired", look=-1, extras=["tie"], shirt="red", at=0.45))

# PART 3: WHY AN EARLY ELECTION ---------------------------------------------------
sc("So why was there an election at all? Vučić was president, with a term that ran until twenty twenty-seven.",
   P("calendar", 700, 860, 1.1, text="2027"), G(1350, "stand", "neutral", look=-1, **LEADER, at=0.3), chapter="Part 3: Why vote now?")
sc("In late September, he resigned as president, called a snap parliamentary election, and ran to become prime minister instead.",
   P("desk", 600, 900, 1.0, text="PRESIDENT"), {"arrow": [[850, 640], [1150, 640]], "at": 0.3}, P("desk", 1400, 900, 1.0, text="PM?", at=0.45),
   G(1400, "run", "neutral", look=1, at=0.6, **LEADER))
sc("Al Jazeera describes Serbia's presidency as largely ceremonial. The prime minister runs the government day to day.",
   G(600, "stand", "neutral", extras=["tie"], shirt="navy", label="president"), P("scale", 960, 900, 1.0, at=0.3),
   G(1350, "type", "neutral", look=-1, extras=["tie", "briefcase"], shirt="grey", at=0.5, label="prime minister"))
sc("In effect, he moved the fight from the streets to the ballot box: let the voters decide who speaks for Serbia.",
   P("scale", 960, 900, 1.2), T("BET", 960, 330, 150, "red", at=0.35), G(500, "think", "smug", **LEADER, at=0.5))
sc("He campaigned on higher pensions, higher public sector wages and more investment.",
   P("arrowup", 500, 800, 1.0, text="PENSIONS"), P("arrowup", 960, 800, 1.0, text="WAGES", at=0.25), P("arrowup", 1420, 800, 1.0, text="INVEST", at=0.5))
sc("And his supporters had real numbers to point to. Unemployment fell from about twenty-six percent to around eight or nine.",
   {"bars": {"values": [26, 8.5], "labels": ["2012", "now"], "colors": ["grey", "green"], "fmt": "{}%", "w": 700, "h": 420}, "x": 900, "y": 820},
   G(1650, "present", "happy", look=-1, extras=ECON, at=0.5, label="supporters"), chapter="Part 4: The case for him")
sc("The economy, measured in euros, nearly tripled, to around ninety billion.",
   C(30, 90, 900, 420, fmt="€{:.0f}bn", size=220, color="green"), P("chart", 1550, 880, 1.0, at=0.4))
sc("And foreign investment jumped from about eight hundred million euros in twenty twelve to a record five point two billion in twenty twenty-four.",
   {"bars": {"values": [0.8, 5.2], "labels": ["2012", "2024"], "colors": ["grey", "green"], "fmt": "€{}bn", "w": 700, "h": 420}, "x": 900, "y": 820},
   P("moneybag", 1600, 880, 1.0, at=0.5))
sc("Critics answer that living costs and public debt went up too. Both of these things can be true at the same time.",
   G(500, "shrug", "worried", extras=LINDA, label="critics"), P("pricetag", 960, 600, 1.1, text="COSTS", at=0.3), P("arrowup", 1400, 800, 1.0, text="DEBT", at=0.5))
sc("So the vote wasn't economy versus nothing. It was roughly: growth and stability, versus accountability and change. Voters picked.",
   P("scale", 960, 900, 1.3), T("GROWTH", 600, 330, 80, "green", at=0.3), T("CHANGE", 1320, 330, 80, "orange", at=0.5), P("ballot", 960, 450, 0.7, at=0.75))

# PART 5: ELECTION DAY -------------------------------------------------------------
sc("Election day was Sunday, October twenty-fifth. Eighteen lists were on the ballot.",
   P("calendar", 600, 860, 1.1, text="SUN OCT 25"), C(0, 18, 1350, 420, fmt="{:.0f}", size=260, color="dark", at=0.3), T("lists", 1350, 620, 80, "dark", at=0.5),
   chapter="Part 5: Election day")
sc("It wasn't spotless. A watchdog called CRTA said its observers saw pressure on voters or election workers at almost a third of the five hundred polling stations it watched.",
   G(500, "hold", "worried", **OBS, label="CRTA observers"), P("clipboard", 900, 860, 1.0, text="1 in 3", at=0.3), C(0, 500, 1450, 420, fmt="{:.0f}", size=200, color="dark", at=0.5),
   T("stations watched", 1450, 600, 60, "dark", at=0.6))
sc("It also reported failures to protect the secrecy of the ballot.",
   P("booth", 800, 900, 1.0), P("eye", 1300, 450, 1.0, at=0.35), P("lock", 1600, 800, 0.8, at=0.55))
sc("Another monitor, CeSID, had about two hundred and sixty reports of possible problems by five p.m.: photographed ballots, group voting, ID checks.",
   C(0, 260, 700, 420, fmt="{:.0f}", size=240, color="red"), P("phone", 1250, 820, 1.0, at=0.35), T("by 5 pm", 700, 600, 70, "dark", at=0.5))
sc("Those reports didn't change the outcome. But they're part of the record, and the new government will be asked about them too.",
   P("clipboard", 800, 860, 1.2, text="RECORD"), G(1350, "think", "neutral", look=-1, extras=LINDA, at=0.4))
sc("Polls closed at eight p.m. Within hours, a projection based on a sample count showed the students well ahead.",
   P("stopwatch", 650, 820, 1.1, text="8 PM"), P("chart", 1300, 880, 1.0, at=0.35), T("SAMPLE", 1300, 380, 90, "orange", at=0.55))
sc("Then came the concession. Vučić said the Student List had won, with between one hundred thirty-five and one hundred forty seats, and his side around one hundred five.",
   P("podium", 600, 900, 1.0), G(600, "stand", "tired", **LEADER), T("135-140", 1300, 380, 130, "orange", at=0.35), T("105", 1300, 580, 130, "navy", at=0.55))
sc("He added, quote: no one else has entered parliament. Which is a very complete sentence.",
   G(600, "shrug", "neutral", **LEADER), P("speech", 1300, 450, 1.5, text="\"no one else\"", at=0.3))
sc("A concession this fast matters. It means no weeks of arguing over who really won, and fewer reasons for anyone to take to the streets.",
   P("stopwatch", 600, 820, 1.0), {"cross": [1300, 560, 120], "at": 0.4}, T("WEEKS?", 1300, 560, 80, "dark", at=0.3))

# PART 6: THE NIGHT ------------------------------------------------------------------
sc("In Belgrade, people poured into the streets. Cars honked. Fireworks went off. Students shouted victory.",
   G(450, "fist", "grin", **STU), G(750, "wave", "happy", **STU2, at=0.15), P("car", 1200, 900, 0.8, at=0.3), P("sun", 1550, 300, 0.6, at=0.5, anim="spin"),
   chapter="Part 6: The night after", bg="purple")
sc("Tens of thousands filled the main roads. In one central park, loyalists of the governing party had been camping in tents for more than a year.",
   P("booth", 900, 900, 1.0, text="TENTS"), T("1 year+", 1450, 380, 110, "dark", at=0.4), G(400, "stand", "neutral", extras=["tie"], shirt="navy", at=0.2, s=0.8))
sc("That night, crowds took the tents down. The longest camping trip in Serbian politics ended without a campfire song.",
   P("booth", 900, 900, 1.0, text="TENTS"), {"cross": [900, 700, 160], "at": 0.35}, G(1450, "shrug", "smug", look=-1, extras=DAVE, at=0.55))
sc("Police in riot gear stood near the election commission. City prosecutors asked everyone involved to avoid violence.",
   G(600, "stand", "neutral", **COP), G(850, "stand", "neutral", **COP, at=0.1), P("building", 1400, 900, 0.9, text="ELECTION HQ", at=0.35))
sc("One student candidate, Belgrade University professor Radomir Saičić, said, quote: tonight we celebrate victory. Tomorrow we build the future.",
   G(550, "present", "happy", **PROF, label="student list candidate"), P("speech", 1250, 460, 1.6, text="\"tomorrow we|build the future\"", at=0.35))
sc("Linda, who has organised exactly one school bake sale, knows the hard part of any party is the morning after.",
   G(600, "hips", "smug", extras=LINDA), P("bread", 1100, 860, 0.8, at=0.3), P("clipboard", 1450, 860, 1.0, text="CLEAN UP", at=0.5), bg="yellow")

# PART 7: WHAT NEXT -------------------------------------------------------------------
sc("So, what happens next? First, the official final results. Then the new parliament must meet within thirty days of those results.",
   P("calendar", 600, 860, 1.1, text="+30 DAYS"), P("capitol", 1350, 900, 1.0, at=0.35), chapter="Part 7: What happens next")
sc("Then a government has to be formed within ninety days. With a clear majority, the students don't need long coalition talks.",
   P("calendar", 600, 860, 1.1, text="+90 DAYS"), C(0, 140, 1350, 420, fmt="{:.0f}", size=220, color="orange", at=0.3), T("> 126", 1350, 600, 100, "green", at=0.5))
sc("The big question: who becomes prime minister? The list didn't name a candidate in the campaign. It deliberately avoided putting one face in front.",
   G(960, "shrug", "confused", **STU), T("PM = ?", 960, 280, 160, "red", at=0.35), P("desk", 1500, 900, 0.9, text="EMPTY", at=0.5))
sc("The most likely name, Al Jazeera reports, is Ilija Srdanović, a cardiologist and medical professor from Novi Sad who led the list during the campaign.",
   G(700, "stand", "neutral", extras=["glasses"], shirt="white", label="likely PM: a cardiologist"), P("thermo", 1300, 820, 0.9, at=0.35), T("?", 1600, 380, 160, "red", at=0.5))
sc("A heart doctor taking over a country. At least he'll know how to check if it still has a pulse.",
   G(700, "hold", "smug", extras=["glasses"], shirt="white"), P("capitol", 1350, 900, 0.9, at=0.3), T("pulse: OK", 1350, 380, 90, "green", at=0.55))
sc("Who gets the ministries for police, money and justice is also unclear. Analysts expect big changes of personnel in the police, the security services and the ministries.",
   P("desk", 450, 900, 0.8, text="POLICE"), P("desk", 960, 900, 0.8, text="MONEY", at=0.2), P("desk", 1470, 900, 0.8, text="JUSTICE", at=0.4),
   T("? ? ?", 960, 330, 140, "red", at=0.6))
sc("Then there's the presidency, now empty. The speaker of parliament, Ana Brnabić, is acting president. A presidential election must be held by December twenty-seventh.",
   P("desk", 600, 900, 1.0, text="PRESIDENT"), G(1100, "stand", "neutral", extras=["bun"], shirt="navy", at=0.25, label="acting president"),
   P("calendar", 1600, 860, 1.0, text="DEC 27", at=0.5))
sc("So Serbia may be heading to the polls again before Christmas. Voters, please keep your ID handy.",
   P("booth", 800, 900, 1.0), G(1350, "facepalm", "tired", look=-1, extras=DAVE, at=0.35), P("calendar", 1650, 860, 0.8, text="AGAIN", at=0.6))

# PART 8: THE WORLD -------------------------------------------------------------------
sc("Now, why should Dave in his kitchen care? Because Serbia sits between three big partners.",
   P("globe", 960, 880, 1.2), G(400, "think", "confused", extras=DAVE, at=0.3), C(0, 3, 1500, 400, fmt="{:.0f}", size=240, color="red", at=0.5),
   chapter="Part 8: Serbia and the world")
sc("The European Union is Serbia's largest trading partner. Serbia is also a candidate to join the EU.",
   P("globe", 600, 880, 1.0, text="EU"), P("ship", 1300, 900, 0.9, at=0.3), T("#1 trade", 1300, 380, 90, "blue", at=0.5))
sc("Russia is a traditional ally and Serbia's main supplier of natural gas. Russia's president had endorsed Vučić.",
   P("pipeline", 900, 880, 1.1), P("fire", 1500, 700, 0.7, at=0.35), T("GAS", 900, 380, 120, "dark", at=0.5))
sc("And China is a major investor. Three partners, three very different expectations.",
   P("building", 600, 900, 0.9, text="FACTORY"), P("truck", 1150, 900, 0.9, at=0.3), P("moneybag", 1550, 880, 0.9, at=0.55))
sc("The European Commission's president said the EU stands ready to support reforms on the rule of law, media freedom and the fight against corruption.",
   G(600, "present", "happy", extras=["bun"], shirt="blue", label="EU Commission"), P("speech", 1300, 450, 1.5, text="\"ready to support\"", at=0.35))
sc("The students have said much more about corruption and schools than about foreign policy. So the balancing act between Brussels, Moscow and Beijing is, for now, an open question.",
   P("scale", 960, 900, 1.3), T("EU", 520, 330, 90, "blue", at=0.2), T("RUSSIA", 960, 260, 90, "red", at=0.4), T("CHINA", 1420, 330, 90, "dark", at=0.6))
sc("Think of it as starting a new job on day one, and finding three very important phones ringing at once.",
   P("phone", 500, 700, 0.9, anim="shake"), P("phone", 960, 600, 0.9, anim="shake", at=0.2), P("phone", 1420, 700, 0.9, anim="shake", at=0.4),
   G(960, "panic", "shock", extras=["glasses"], shirt="white", at=0.6))

# PART 9: BOTH SIDES NOW -----------------------------------------------------------------
sc("And what about the side that lost? It still holds about a hundred and three seats. That's a big opposition, not a footnote.",
   C(0, 103, 900, 420, fmt="{:.0f}", size=260, color="navy"), G(1550, "hips", "neutral", look=-1, **LEADER, at=0.4), chapter="Part 9: What each side faces")
sc("Vučić's own future is unclear. His party will have to rebuild in opposition, for the first time since twenty twelve.",
   P("house", 700, 900, 1.0, text="REBUILD"), G(1300, "think", "worried", look=-1, **LEADER, at=0.35), P("calendar", 1650, 860, 0.8, text="2012", at=0.55))
sc("Supporters of the old government will be watching for one thing: whether the stable growth they valued survives the change.",
   G(600, "hold", "worried", extras=ECON, label="supporters"), P("chart", 1300, 880, 1.0, at=0.35), P("magnifier", 1600, 600, 0.8, at=0.55))
sc("And the students will be judged by the promises they made: cleaner institutions, independent courts and public media, and better schools.",
   G(500, "present", "neutral", **STU), P("clipboard", 1000, 860, 1.1, text="PROMISES", at=0.3), P("school", 1500, 900, 0.8, at=0.5))
sc("Many of the new members of parliament have never held office. That's the pitch. It's also, eventually, the challenge.",
   G(700, "shrug", "confused", **STU2), P("desk", 1300, 900, 1.0, text="DAY 1", at=0.35))
sc("Protest movements are good at saying no. Governments have to say yes, every day, to budgets. We just count the facts.",
   *SIGN(600, "NO", 0.9), {"arrow": [[800, 600], [1150, 600]], "at": 0.3}, P("clipboard", 1400, 860, 1.1, text="BUDGET", at=0.45))

# RECAP ----------------------------------------------------------------------------------
sc("So, the recap. A deadly accident in Novi Sad led to almost two years of student-led protests about accountability and corruption.",
   P("building", 500, 900, 0.8, text="STATION"), {"arrow": [[700, 600], [1000, 600]], "at": 0.3}, *SIGN(1300, "PROTEST", 0.8, at=0.4), chapter="Recap", bg="paper")
sc("Vučić called an early election to settle it. Record turnout. The Student List took about fifty-two and a half percent and a projected one hundred forty seats.",
   T("68.78%", 600, 380, 120, "green"), T("52.54%", 1300, 380, 120, "orange", at=0.3), T("140 seats", 960, 640, 110, "orange", at=0.55))
sc("He conceded the same night. Now comes the hard part: picking a prime minister, building a government, and holding a presidential vote by late December.",
   P("podium", 500, 900, 0.9), P("desk", 1050, 900, 0.9, text="PM?", at=0.3), P("calendar", 1550, 860, 0.9, text="DEC 27", at=0.55))
sc("Back in his kitchen, Dave has learned where Serbia is, what a snap election is, and that a cardiologist might run a country.",
   P("coffee", 1250, 860, 1.0), G(700, "point", "grin", extras=DAVE), P("globe", 1600, 880, 0.8, at=0.4), bg="yellow")
sc("He has also decided to apply for prime minister of his own kitchen. The coffee machine has not conceded.",
   P("coffee", 1300, 860, 1.4, anim="shake"), G(650, "fist", "smug", extras=DAVE), T("NO CONCESSION", 1300, 360, 80, "red", at=0.5), bg="yellow")
sc("Your turn. Should a protest movement turn itself into a political party? Or should it stay outside government and keep watching? Tell us in the comments.",
   G(600, "think", "neutral", extras=LINDA), P("speech", 1300, 450, 1.4, text="YOUR TAKE?", at=0.35), bg="yellow")
sc("If this helped, subscribe for calm, stick-figure news. See you at the next one.",
   G(960, "wave", "happy", extras=DAVE), P("tv", 1550, 800, 0.7, at=0.4, text="SUBSCRIBE"), bg="yellow")


script = {
    "id": "ep016",
    "title": "Serbia's Students Beat a 14-Year Government. How?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "On Sunday, October 25, 2026, Serbia held a snap parliamentary election, and the student-led Student List won a majority. "
        "Election commission figures from 8,077 of 8,392 polling stations: Student List 52.54% (projected 140 of 250 seats), "
        "United Serbia, led by Aleksandar Vučić's Serbian Progressive Party, 39.29% (103 seats). Turnout 68.78%, the highest in more than 30 years. "
        "Vučić conceded the same night. We explain how the movement began after the Novi Sad station canopy collapse in November 2024, "
        "the case each side made, what election observers reported, and what happens next: a prime minister, a government, and a presidential vote by December 27.\n\n"
        "We don't pick political sides. We just count the facts.\n\n"
        "Sources:\n"
        "Al Jazeera, Serbia's Vucic concedes election defeat to student-led movement (Oct 25, 2026): https://www.aljazeera.com/news/2026/10/25/serbia-voter-turnout-highest-in-decades-as-students-oppose-longtime-leader\n"
        "Al Jazeera, Serbia after Vucic: Who will be PM and when will a government be formed? (Oct 26, 2026): https://www.aljazeera.com/news/2026/10/26/serbia-after-vucic-who-will-be-pm-and-when-will-a-government-be-formed\n"
        "Al Jazeera, Aleksandar Vucic, the Serbian leader brought down by students (Oct 26, 2026): https://www.aljazeera.com/news/2026/10/26/aleksandar-vucic-the-serbian-leader-brought-down-by-students\n"
        "ABC News (Australia), Serbian president concedes defeat to student-led movement (Oct 26, 2026): https://www.abc.net.au/news/2026-10-26/serbia-election-vucic-defeat-student-protest/107307808\n"
        "Euronews, Student List wins Serbian election as Vučić concedes defeat (Oct 25, 2026): https://www.euronews.com/2026/10/25/vucic-concedes-defeat-in-pivotal-serbian-elections-says-student-movement-has-won\n\n"
        "#serbia #election #students #europe #explained #stickfigure #news"
    ),
    "tags": ["serbia election", "serbia election 2026", "student list", "vucic concedes", "serbia protests", "novi sad",
             "belgrade", "europe news", "election explained", "news explained", "stick figure animation", "the doodle desk"],
    "thumbnail": {"bg": "yellow", "text": "STUDENTS|WON|SERBIA?", "size": 190, "color": "black",
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep016.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

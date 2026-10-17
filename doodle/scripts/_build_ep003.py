"""Episode 3: 404 Media finds how ChatGPT targets ads (Oct 15, 2026), explained with stick figures."""
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
OFF = ["tie", "briefcase"]
LINDA = ["bun"]
ENG = ["hardhat"]

S = []


def sc(say, *items, **kw):
    d = {"say": say, "items": list(items)}
    d.update(kw)
    S.append(d)




def chat(x, y, s, q, a=None, ad=None, at=0):
    """A phone-style chat window built from boxes and text (centre x, top y)."""
    w, h = int(640 * s), int(520 * s)
    out = [{"box": [x - w // 2, y, w, h], "color": "white", "at": at},
           {"box": [x - w // 2, y, w, int(60 * s)], "color": "teal", "at": at},
           T("ChatBot", x, y + int(30 * s), int(40 * s), "white", at=at),
           {"box": [x - w // 2 + int(140 * s), y + int(90 * s), int(470 * s), int(90 * s)], "color": "sky", "at": at},
           T(q, x + int(70 * s), y + int(135 * s), int(36 * s), "dark", at=at)]
    if a:
        out += [{"box": [x - w // 2 + int(30 * s), y + int(210 * s), int(470 * s), int(110 * s)], "color": "paper", "at": at + 0.15},
                T(a, x - int(70 * s), y + int(265 * s), int(34 * s), "dark", at=at + 0.15)]
    if ad:
        adat = ad[1] if isinstance(ad, tuple) else at + 0.35
        txt = ad[0] if isinstance(ad, tuple) else ad
        out += [{"box": [x - w // 2 + int(30 * s), y + int(350 * s), int(580 * s), int(130 * s)], "color": "yellow", "at": adat},
                T("Sponsored", x - w // 2 + int(110 * s), y + int(375 * s), int(26 * s), "dark", at=adat),
                T(txt, x, y + int(430 * s), int(36 * s), "black", at=adat)]
    return out


# COLD OPEN --------------------------------------------------------------------
sc("Meet Dave. Dave's front door squeaks. So Dave does what a billion people do now. He asks the chatbot.",
   P("house", 1450, 900, 1.0), T("SQUEEEAK", 1450, 330, 80, "orange", anim="shake", at=0.2), G(500, "type", "tired", extras=DAVE, at=0.1),
   P("laptop", 820, 900, 0.8, at=0.4), cam={"from": [960, 560, 1.12], "to": [960, 540, 1.0]})
sc("The chatbot tells him to oil the hinge. Helpful. And right underneath, a little box appears.",
   *chat(960, 160, 1.15, "my door squeaks", "Try oiling the hinge.", ("SQUEAK-B-GONE  $9.99", 0.55)))
sc("An ad. For hinge oil. Dave looks at the door. The door looks at Dave. Somebody, somewhere, knew.",
   G(500, "shrug", "shock", extras=DAVE), P("house", 1400, 900, 0.9, at=0.2), P("eye", 960, 420, 1.2, at=0.55, anim="pulse"))
sc("This week, a news site paid for ads inside ChatGPT, just to see how the targeting really works. What they found has people talking.",
   P("phone", 700, 900, 1.3, text="AD"), T("ADS IN THE CHAT", 1300, 300, 100, "red", at=0.3),
   P("megaphone", 1350, 880, 1.0, at=0.55), bg="yellow")
sc("So today's question: how does ChatGPT decide which ads to show you? What does the advertiser get? And can you switch it off?",
   P("tv", 960, 800, 1.4, text="WHO PICKS THE AD?"), G(330, "think", "confused", extras=DAVE, at=0.4),
   T("?", 1650, 330, 200, "red", at=0.7), chapter="Today's question")
sc("We'll stick to what was reported, what OpenAI says, and what its critics say. You decide what to make of it.",
   G(560, "present", "neutral", extras=LINDA), P("scale", 1300, 900, 1.2, at=0.3))

# PART 1: HOW THE ADS GOT HERE -------------------------------------------------
sc("First, a quick rewind. For years, ChatGPT had no ads at all. You asked, it answered, nobody tried to sell you a lamp.",
   P("calendar", 520, 860, 1.0, text="BEFORE"), *chat(1250, 220, 0.9, "hi", "Hello!"), chapter="Part 1: How the ads got here")
sc("Then, in January twenty twenty six, OpenAI launched a cheaper plan called ChatGPT Go. In the US it costs eight dollars a month.",
   P("calendar", 520, 860, 1.0, text="JAN 2026"),
   {"count": [0, 8], "fmt": "${:.0f}/month", "x": 1250, "y": 420, "size": 130, "color": "green", "dur": 1.5, "at": 0.4})
sc("In the same announcement, OpenAI said it planned to begin testing ads in the free tier and in Go, in the US, soon.",
   P("podium", 700, 900, 1.0), G(700, "present", "neutral", extras=OFF, s=0.8, y=700, label="OpenAI", at=0.1),
   P("speech", 1350, 460, 1.4, text="ads: soon", at=0.45))
sc("Its reasoning, in its own words: ads support its commitment to making AI accessible to everyone.",
   T("“Ads support our commitment to", 960, 360, 64, "dark"), T("making AI accessible to everyone.”", 960, 450, 64, "dark", at=0.2),
   T("— OpenAI, Jan 2026", 1300, 560, 44, "grey", at=0.5), G(300, "think", "neutral", extras=DAVE, s=0.8, at=0.6))
sc("Running a chatbot for this many people isn't cheap. OpenAI said its free plans need significant infrastructure and ongoing investment.",
   P("building", 600, 900, 1.2, text="SERVERS"), P("building", 950, 900, 1.0, at=0.2), P("moneybag", 1450, 900, 1.1, text="$$$", at=0.45))
sc("On February ninth, the ads arrived. Free users and Go users in the United States started seeing them.",
   P("calendar", 520, 860, 1.0, text="FEB 9"), {"ring": [520, 740, 130], "at": 0.3},
   P("phone", 1150, 900, 1.0, text="AD", at=0.4), P("phone", 1450, 900, 1.0, text="AD", at=0.55))
sc("If you pay for Plus, Pro, or a business, enterprise or education plan, you don't get ads. Paying more buys you a quiet chat.",
   T("Plus", 450, 380, 80, "green"), T("Pro", 800, 380, 80, "green", at=0.1), T("Business", 1180, 380, 80, "green", at=0.2),
   T("Enterprise / Edu", 1550, 380, 70, "green", at=0.3), T("NO ADS", 960, 600, 120, "dark", at=0.55),
   G(1700, "hips", "smug", extras=LINDA, s=0.8, look=-1, at=0.7))
sc("In August, ads expanded to India. And in October, OpenAI announced picture ads that appear next to images you ask it to make.",
   P("calendar", 450, 860, 0.9, text="AUG"), P("globe", 800, 900, 0.9, at=0.15),
   P("calendar", 1200, 860, 0.9, text="OCT", at=0.45), {"box": [1400, 330, 300, 240], "color": "yellow", "at": 0.6},
   T("picture ad", 1550, 450, 50, "dark", at=0.65))
sc("Why does that matter? TechCrunch reports ChatGPT has about one point two billion weekly users. That's a lot of eyeballs.",
   {"count": [0, 1.2], "fmt": "{:.1f} billion", "x": 960, "y": 330, "size": 150, "color": "red", "dur": 2.0},
   *[P("eye", 450 + i * 340, 760, 0.55, at=0.4 + i * 0.08) for i in range(4)])
sc("For an advertiser, that's like finding a shop where everybody walks in and tells the shopkeeper exactly what they need.",
   P("building", 600, 900, 1.1, text="SHOP"), G(1000, "point", "happy", extras=DAVE, s=0.8, look=-1),
   G(1350, "think", "grin", extras=CEO, s=0.8, look=-1, label="advertiser", at=0.45))

# PART 2: THE EXPERIMENT -------------------------------------------------------
sc("Now, the news. On October fifteenth, the tech news site 404 Media published an investigation by reporter Joseph Cox.",
   P("calendar", 520, 860, 1.0, text="OCT 15"), P("laptop", 1250, 900, 1.1, text="404 Media", at=0.35),
   chapter="Part 2: The experiment")
sc("Instead of just reading OpenAI's rules, 404 Media did something simple. It became an advertiser and bought two ad campaigns inside ChatGPT.",
   G(600, "hold", "smug", extras=["glasses"], label="reporter"), P("wallet", 760, 760, 0.7, at=0.3),
   {"count": [0, 2], "fmt": "{:.0f} campaigns", "x": 1350, "y": 420, "size": 120, "color": "blue", "dur": 1.2, "at": 0.45})
sc("According to MobileSyrup, the test ads had a cheeky message: that ChatGPT isn't private, because humans are hired to read chats.",
   {"box": [560, 300, 800, 220], "color": "yellow"}, T("Sponsored", 680, 335, 34, "dark"),
   T("ChatGPT isn't private...", 960, 430, 60, "black", at=0.2), G(1650, "facepalm", "tired", extras=DAVE, look=-1, s=0.8, at=0.6))
sc("Earlier, 404 Media had reported that prompts may be reviewed by humans. So yes, it was an ad about ads, on the platform selling the ads.",
   {"arrow": [[600, 400], [1300, 400]], "color": "red"}, {"arrow": [[1300, 600], [600, 600]], "color": "red", "at": 0.3},
   T("AD", 450, 500, 110, "dark", at=0.1), T("AD", 1450, 500, 110, "dark", at=0.4), T("inception?", 960, 780, 70, "purple", at=0.7))
sc("Once inside, they looked at every option an advertiser gets. And they found two main ways to aim an ad at someone.",
   P("clipboard", 700, 900, 1.2), T("1", 1250, 400, 150, "teal", at=0.4), T("2", 1550, 400, 150, "orange", at=0.6))

# PART 3: TWO WAYS TO AIM ------------------------------------------------------
sc("Way number one is called context hints. The advertiser describes the topics where their product might fit.",
   T("1. CONTEXT HINTS", 960, 220, 100, "teal"), P("clipboard", 600, 900, 1.0, text="topics", at=0.3),
   T("door, hinge, squeak", 1300, 600, 70, "dark", at=0.5), chapter="Part 3: Two ways to aim an ad")
sc("So the hinge oil company might write: squeaky doors, home repair, hinges. Then, if your chat is about that, their ad may show up.",
   *chat(1200, 230, 0.95, "squeaky door help", None, ("SQUEAK-B-GONE", 0.5)), G(450, "point", "smug", extras=CEO, label="oil company"))
sc("OpenAI says these hints are not exact triggers. They guide the matching, but don't guarantee an ad appears in any one chat.",
   T("NOT exact triggers", 960, 300, 100, "dark"), P("robot", 700, 900, 1.0, at=0.3), T("maybe?", 1300, 650, 90, "purple", at=0.55))
sc("One newsletter, The Neuron, compared it to keyword ads on search engines, but looser. Think fishing net, not harpoon.",
   T("search ads", 600, 350, 80, "dark"), {"arrow": [[800, 350], [1100, 350]], "at": 0.3}, T("but looser", 1350, 350, 80, "teal", at=0.35),
   P("eye", 960, 800, 0.6, at=0.6))
sc("This part ties ads to what you're talking about right now. Ask about running shoes, and you may get a shoe ad.",
   *chat(1250, 220, 0.95, "best running shoes?", "Here are a few...", ("ZOOM SHOES 20% OFF", 0.4)), G(450, "run", "happy", extras=DAVE))
sc("Way number two is the one that made headlines. It's called custom audiences.",
   T("2. CUSTOM AUDIENCES", 960, 300, 100, "orange"), P("clipboard", 960, 900, 1.1, text="LIST", at=0.35, anim="pulse"))
sc("The advertiser uploads a list of people. Customers, newsletter readers, anyone they have contact details for.",
   P("clipboard", 600, 900, 1.2, text="names"), {"arrow": [[780, 600], [1150, 600]], "at": 0.35}, P("robot", 1400, 900, 1.0, at=0.4))
sc("The list can include email addresses, phone numbers, scrambled versions of both, or the advertising ID that comes with every Android phone.",
   P("envelope", 450, 700, 0.8), P("phone", 900, 900, 0.8, text="555-...", at=0.25),
   T("#a9f3...", 1300, 560, 70, "grey", at=0.45), P("phone", 1650, 900, 0.8, text="AD ID", at=0.65))
sc("Those scrambled versions are called hashes. A hash turns your email into a jumble of letters that's hard to turn back.",
   T("dave@mail.com", 600, 400, 70, "dark"), {"arrow": [[880, 400], [1100, 400]], "at": 0.3}, T("7f3a9c...", 1350, 400, 70, "grey", at=0.4),
   P("lock", 960, 860, 0.9, at=0.6))
sc("ChatGPT then checks which of those people have a ChatGPT account. The ones that match become eligible to see that advertiser's ads.",
   P("clipboard", 500, 900, 1.0), P("robot", 960, 900, 1.0, at=0.2),
   T("match", 1400, 450, 80, "green", at=0.45), T("match", 1500, 600, 80, "green", at=0.55), T("no", 1350, 750, 70, "grey", at=0.65))
sc("So in theory, a shop that has your email from a past purchase could follow you into your chatbot.",
   P("cart", 500, 900, 1.0), P("envelope", 900, 650, 0.6, at=0.25, move=[1350, 650]), P("laptop", 1450, 900, 0.9, at=0.4),
   G(1750, "panic", "shock", extras=DAVE, s=0.8, look=-1, at=0.6))
sc("Here's the number OpenAI points to: twenty five thousand. A list needs at least that many matched users to be used for targeting.",
   {"count": [0, 25000], "fmt": "{:,.0f}", "x": 960, "y": 380, "size": 180, "color": "red", "dur": 2.0}, T("minimum matched users", 960, 560, 60, "dark", at=0.5))
sc("The idea: you can't type in one person's email and stalk them with ads. You have to bring a crowd.",
   P("envelope", 500, 800, 0.8), {"cross": [500, 700, 120], "at": 0.3},
   *[G(1000 + i * 120, "stand", "neutral", s=0.45, at=0.45 + i * 0.04) for i in range(7)])
sc("Smaller lists can still be used the other way round: to exclude people. For example, don't show this ad to people who already bought it.",
   P("clipboard", 600, 900, 1.0, text="small list"), T("EXCLUDE", 1300, 380, 110, "grey", at=0.35), {"cross": [1300, 650, 110], "at": 0.6})
sc("Is this new? Not really. The Neuron notes that targeting by customer lists is standard across advertising. What's new is where it's happening.",
   T("standard practice", 960, 300, 90, "dark"), P("tv", 700, 830, 0.9, text="AD"), P("phone", 1250, 900, 0.9, text="AD", at=0.2),
   P("laptop", 1600, 900, 0.8, text="AD", at=0.35))
sc("Because people don't talk to a chatbot like a search box. They tell it about their jobs, their money worries, their squeaky doors.",
   P("speech", 600, 400, 1.1, text="my job..."), P("speech", 1000, 300, 1.1, text="my rent...", at=0.25),
   P("speech", 1400, 420, 1.1, text="my door...", at=0.5), G(960, "shrug", "worried", extras=DAVE, at=0.1))

# PART 4: WHAT OPENAI SAYS -----------------------------------------------------
sc("So what does OpenAI say? Quite a lot, actually. Let's go through its side properly.",
   G(700, "present", "neutral", extras=OFF, label="OpenAI"), P("clipboard", 1300, 900, 1.1, text="RULES", at=0.4),
   chapter="Part 4: What OpenAI says")
sc("First, OpenAI says the advertiser is not told who matched. The shop never learns that Dave, specifically, uses ChatGPT.",
   P("clipboard", 500, 900, 1.0), P("robot", 960, 900, 1.0), {"arrow": [[1080, 600], [1350, 600]], "at": 0.3},
   T("???", 1500, 600, 100, "grey", at=0.45), G(1750, "hips", "smug", extras=DAVE, s=0.8, look=-1, at=0.6))
sc("Second, OpenAI says uploaded files are usually deleted within twenty four hours of being processed.",
   P("clipboard", 650, 900, 1.0), {"count": [0, 24], "fmt": "{:.0f} hours", "x": 1300, "y": 420, "size": 130, "color": "blue", "dur": 1.5, "at": 0.3},
   P("stopwatch", 1300, 900, 0.8, at=0.5))
sc("Third, it told 404 Media that being on an advertiser's list does not, by itself, cause an ad to be shown.",
   T("“being on an advertiser's list does not,", 960, 360, 58, "dark"), T("by itself, cause an ad to be shown”", 960, 440, 58, "dark", at=0.2),
   T("— OpenAI", 1350, 540, 44, "grey", at=0.45), P("clipboard", 960, 900, 0.8, at=0.6))
sc("Back in February, OpenAI set out more rules. Ads only go to logged in adults. It says it doesn't plan to show ads to minors.",
   T("18+", 600, 450, 180, "red"), P("lock", 1300, 900, 1.0, at=0.4), T("adults only", 1300, 380, 70, "dark", at=0.5))
sc("Ads are not shown on sensitive topics, like health, mental health or politics. Ask about your rash, and there should be no rash cream ad.",
   T("health", 450, 400, 70, "dark"), T("mental health", 960, 400, 70, "dark", at=0.15), T("politics", 1450, 400, 70, "dark", at=0.3),
   T("NO ADS", 960, 620, 130, "green", at=0.5))
sc("OpenAI says ads do not influence ChatGPT's answers. Ads are labelled sponsored, and kept separate from the answer itself.",
   *chat(960, 200, 1.1, "best lawn mower?", "It depends on your lawn...", ("labelled, separate", 0.5)))
sc("And advertisers, it says, get only totals: how many people saw the ad and how many clicked. Not your chats. Not your personal information.",
   P("chart", 700, 900, 1.1), T("views: 10,000", 1300, 420, 70, "dark", at=0.3), T("clicks: 120", 1300, 520, 70, "dark", at=0.4),
   T("(example numbers)", 1300, 610, 44, "grey", at=0.5), {"cross": [1550, 780, 80], "at": 0.7}, P("speech", 1550, 860, 0.9, text="chats", at=0.6))
sc("You can also dismiss an ad, give feedback, see why you got it, delete your ad data, and turn personalization off.",
   P("phone", 960, 900, 1.3, text="ad controls"), T("hide", 500, 380, 70, "dark", at=0.2), T("why?", 800, 280, 70, "dark", at=0.3),
   T("delete", 1150, 280, 70, "dark", at=0.4), T("off", 1450, 380, 70, "dark", at=0.5))
sc("From OpenAI's point of view, ads are how the free plans stay free, for people who can't or won't pay for a subscription.",
   P("moneybag", 600, 900, 1.0, text="ADS"), {"arrow": [[760, 700], [1150, 700]], "at": 0.3}, T("FREE", 1400, 500, 130, "green", at=0.45))

# PART 5: WHAT CRITICS SAY -----------------------------------------------------
sc("Now the other side. Critics say the problem isn't one big scandal. It's a lot of small steps.",
   G(700, "think", "worried", extras=["glasses"], label="privacy critic"), P("clipboard", 1300, 900, 1.0, text="concerns", at=0.4),
   chapter="Part 5: What critics say")
sc("Zach Edwards of DecryptAds, quoted by 404 Media, called OpenAI's approach “boiling the frog”.",
   G(600, "point", "neutral", extras=["glasses"], label="Zach Edwards, DecryptAds"), T("“boiling the frog”", 1300, 420, 90, "dark", at=0.3),
   P("fire", 1300, 900, 0.7, at=0.5))
sc("Meaning: you change things slowly, so people don't notice how much is changing. First no ads. Then text ads. Then picture ads. Then lists.",
   T("no ads", 400, 600, 60, "grey"), T("text ads", 750, 500, 60, "dark", at=0.2), T("picture ads", 1150, 400, 60, "orange", at=0.4),
   T("lists", 1550, 300, 70, "red", at=0.6), {"arrow": [[400, 700], [1600, 360]], "color": "red", "at": 0.1})
sc("Second concern: 404 Media said it's unclear whether OpenAI scrambles the raw emails and phone numbers that advertisers upload.",
   T("dave@mail.com", 700, 420, 80, "dark"), T("hashed?", 1350, 420, 90, "red", at=0.35), T("?", 1350, 650, 160, "red", at=0.55))
sc("OpenAI hadn't said. It does say it deletes the files, usually within a day. 404 Media said the unclear part could leave data exposed.",
   P("calendar", 600, 860, 1.0, text="24 h"), G(1300, "shrug", "neutral", extras=["glasses"], s=0.9, look=-1, at=0.3))
sc("Third, and this one surprised a lot of people: the off switch doesn't switch everything off.",
   P("phone", 960, 900, 1.3, text="OFF"), T("OFF?", 960, 250, 120, "red", at=0.4, anim="shake"))
sc("Turning off ad personalization stops ChatGPT using your past chats, activity and preferences to pick ads.",
   T("past chats", 500, 380, 70, "dark"), T("activity", 960, 380, 70, "dark", at=0.15), T("preferences", 1420, 380, 70, "dark", at=0.3),
   {"cross": [500, 380, 90], "at": 0.5}, {"cross": [960, 380, 90], "at": 0.55}, {"cross": [1420, 380, 90], "at": 0.6})
sc("But OpenAI's own setting says, quote, ads may still be based on your current chat. So you still see ads. Just less personal ones.",
   T("“Ads may still be based on", 960, 350, 66, "dark"), T("your current chat.”", 960, 440, 66, "dark", at=0.2),
   T("— OpenAI's settings page", 1300, 540, 44, "grey", at=0.45), G(350, "facepalm", "tired", extras=DAVE, s=0.8, at=0.6))
sc("And Gizmodo noted the opt-out doesn't appear to stop targeting by that unique phone identifier. Gizmodo asked OpenAI for details and hadn't heard back by publication.",
   P("phone", 600, 900, 1.0, text="AD ID"), P("envelope", 1250, 700, 0.8, text="to OpenAI", at=0.35),
   T("...", 1600, 500, 140, "grey", at=0.6, anim="pulse"))
sc("Meanwhile, the ads are piling up. One outside project, the ChatGPT Ad Library, says it has collected over forty three thousand different ads.",
   {"count": [0, 43410], "fmt": "{:,.0f} ads", "x": 960, "y": 340, "size": 150, "color": "orange", "dur": 2.0},
   T("one project's own sample", 960, 500, 50, "grey", at=0.5))
sc("Seen in over four hundred and fifteen thousand places. That's its own sample, not an official OpenAI figure, but it gives you a sense of scale.",
   {"count": [0, 415289], "fmt": "{:,.0f} placements", "x": 960, "y": 340, "size": 120, "color": "red", "dur": 2.0},
   *[P("phone", 450 + i * 250, 900, 0.5, text="AD", at=0.4 + i * 0.06) for i in range(5)])

# PART 6: WHAT YOU CAN DO ------------------------------------------------------
sc("So what can a normal person actually do? Linda has a list.",
   G(500, "hold", "smug", extras=LINDA), P("clipboard", 1150, 900, 1.2, text="LINDA'S LIST", at=0.3),
   chapter="Part 6: What you can actually do")
sc("Option one: pay. Plus, Pro and the business plans have no ads. The catch, of course, is that you're paying.",
   T("1. PAY", 960, 260, 110, "green"), P("wallet", 700, 800, 0.9, at=0.3), T("no ads", 1300, 600, 80, "dark", at=0.5))
sc("Option two: go into the ad settings and switch personalization off. It won't remove ads, but it narrows what's used to pick them.",
   T("2. SETTINGS", 960, 260, 110, "blue"), P("phone", 960, 900, 1.1, text="ads: OFF", at=0.3))
sc("Option three: when an ad looks oddly specific, tap the button that shows why you got it. You can also dismiss it or delete your ad data.",
   T("3. ASK WHY", 960, 260, 110, "orange"), *chat(960, 360, 0.9, "door squeaks", None, ("why this ad?", 0.4)))
sc("Option four, the cheapest: think of the chat like a search box. What you type can shape the ads you see.",
   T("4. THINK FIRST", 960, 260, 110, "purple"), P("laptop", 700, 900, 1.0, at=0.3), P("eye", 1350, 700, 0.8, at=0.5))
sc("That doesn't mean panic. It means the same habits you already use everywhere else online.",
   G(600, "stand", "neutral", extras=LINDA), G(1300, "stand", "tired", extras=DAVE, look=-1, at=0.3), T("calm down, Dave", 960, 300, 70, "dark", at=0.55))
sc("Dave, meanwhile, has decided to only ask the chatbot about things he'd be happy to see ads for. So far: pizza.",
   G(600, "type", "grin", extras=DAVE), P("laptop", 950, 900, 0.8), T("PIZZA", 1450, 400, 120, "orange", at=0.5))

# PART 7: WHAT'S NEXT ----------------------------------------------------------
sc("What's next? Picture ads were due to start appearing later this month, in the US only for now.",
   P("calendar", 600, 860, 1.0, text="OCT"), {"box": [1150, 330, 400, 300], "color": "yellow", "at": 0.35}, T("picture ad", 1350, 480, 60, "dark", at=0.4),
   chapter="Part 7: What happens next")
sc("TechCrunch reports OpenAI also added tools that help advertisers measure whether their ads led to clicks and sales.",
   P("chart", 960, 900, 1.3), T("did it work?", 960, 260, 90, "dark", at=0.4))
sc("And if ads roll out globally, advertisers could eventually reach all those one point two billion weekly users.",
   P("globe", 960, 850, 1.4, anim="spin"), T("1.2 billion", 960, 220, 110, "red", at=0.4))
sc("Supporters say that keeps the free version free. Critics worry that many users don't realise they can be targeted with data an advertiser uploaded.",
   G(600, "present", "happy", extras=OFF, label="supporters"), G(1350, "think", "worried", extras=["glasses"], look=-1, label="critics", at=0.3),
   P("scale", 960, 900, 0.9, at=0.5))
sc("Both can be true at once. Free things have to be paid for somehow. And people like to know how.",
   P("scale", 960, 900, 1.3), T("free", 700, 420, 80, "green", at=0.3), T("clear", 1220, 420, 80, "blue", at=0.45))
sc("Which side has it right depends on who you ask. We don't pick sides. We just count the facts.",
   T("we just count the facts", 960, 400, 100, "dark"), P("clipboard", 960, 900, 0.9, at=0.4))

# RECAP --------------------------------------------------------------------------
sc("Quick recap. ChatGPT has shown ads to free and Go users in the US since February.",
   P("calendar", 600, 860, 1.0, text="FEB 9"), P("phone", 1300, 900, 1.1, text="AD", at=0.3), chapter="Recap")
sc("Advertisers can aim by topic, or by uploading lists of emails, phone numbers and phone IDs, with a minimum of twenty five thousand matches.",
   T("topics", 600, 380, 90, "teal"), T("lists", 1300, 380, 90, "orange", at=0.3), T("25,000+", 960, 600, 130, "red", at=0.55))
sc("OpenAI says advertisers can't see who matched or what you chat about. And turning personalization off still leaves ads based on your current chat.",
   P("lock", 600, 900, 1.0), P("phone", 1300, 900, 1.0, text="OFF", at=0.4), T("still ads", 1300, 300, 80, "dark", at=0.6))
sc("As for Dave, he fixed the door with some cooking oil he already had. The ad never stood a chance.",
   P("house", 1350, 900, 0.9), G(600, "fist", "grin", extras=DAVE), T("silence.", 1350, 300, 90, "dark", at=0.55))
sc("Then he asked the chatbot for a pizza recipe. He's now been shown three pizza ovens.",
   P("laptop", 700, 900, 0.9), {"count": [0, 3], "fmt": "{:.0f} ovens", "x": 1350, "y": 420, "size": 130, "color": "orange", "dur": 1.5, "at": 0.3},
   G(1650, "facepalm", "tired", extras=DAVE, look=-1, s=0.8, at=0.6))
sc("Would you pay to get rid of the ads, or is free with ads a fair deal? Tell us in the comments, and subscribe for the next one.",
   P("speech", 960, 460, 1.8, text="pay or ads?"), G(400, "wave", "happy", extras=DAVE, at=0.4), P("phone", 1500, 900, 0.9, text="AD", at=0.6))

script = {
    "id": "ep003",
    "title": "ChatGPT Has Ads Now. How Do They Know What You Want?",
    "voice": "am_michael",
    "speed": 1.0,
    "description": (
        "ChatGPT has shown ads to Free and Go users in the US since February 9, 2026. On October 15, 404 Media bought two ad campaigns "
        "inside ChatGPT to see how the targeting works. Here's what it found, explained with stick figures: context hints, custom audiences "
        "built from emails, phone numbers and Android ad IDs, the 25,000-match minimum, what OpenAI says about privacy, what critics say, "
        "what the ad-personalization switch does and doesn't do, and what you can do about it.\n\n"
        "We don't pick sides. We just count the facts.\n\n"
        "Sources:\n"
        "404 Media, How ChatGPT Targets Ads To You Based On Your Prompts, Phone Number, and Email: https://www.404media.co/how-chatgpt-targets-ads-to-you-based-on-your-prompts-phone-number-and-email/\n"
        "Gizmodo, Here's How ChatGPT Is Targeting You With Ads: https://gizmodo.com/heres-how-chatgpt-is-targeting-you-with-ads-2000826457\n"
        "Yahoo Tech, ChatGPT Can Target Ads With Your Prompts, Email, and Phone: https://tech.yahoo.com/ai/chatgpt/articles/chatgpt-target-ads-prompts-email-170013093.html\n"
        "MobileSyrup, ChatGPT lets advertisers target you based on your personal info: https://mobilesyrup.com/2026/10/16/chatgpt-openai-targeted-ads-personal-data\n"
        "The Neuron, Oct 16: https://www.theneurondaily.com/p/october-16-friday-1362\n"
        "TechCrunch, OpenAI launches visual ads: https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/\n"
        "MacRumors, ChatGPT Now Has Ads for Free and Go Tier Users: https://www.macrumors.com/2026/02/09/chatgpt-now-has-ads/\n"
        "OpenAI, Introducing ChatGPT Go: https://openai.com/blog/introducing-chatgpt-go\n"
        "Superpower Daily (ChatGPT Ad Library figures): https://superpowerdaily.com/posts/404-media-finds-chatgpt-ad-targeting-uses-prompts-and-uploaded-contact-details\n\n"
        "#chatgpt #openai #privacy #ads #explained #news #stickfigure"
    ),
    "tags": ["chatgpt ads", "chatgpt", "openai", "ad targeting", "privacy", "custom audiences", "404 media", "ai news",
             "news explained", "stick figure animation", "chatgpt privacy", "online ads"],
    "thumbnail": {"bg": "yellow", "text": "ADS|IN YOUR|CHAT?!", "size": 200, "color": "black",
                  "guy": {"pose": "panic", "face": "shock", "look": 1, "extras": ["hair"]},
                  "items": [{"prop": "phone", "x": 1700, "y": 820, "s": 1.5, "text": "AD"}], "guy_x": 1330},
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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep003.json")
json.dump(script, open(out, "w"), indent=1)
print(out, len(script["scenes"]), "scenes", sum(len(s["say"].split()) for s in script["scenes"]), "words")
print("max words/scene", max(len(s["say"].split()) for s in script["scenes"]))

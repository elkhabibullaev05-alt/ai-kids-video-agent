import json
cast = json.load(open("scripts3d/cast.json"))
chars = {k: v for k, v in cast.items() if not k.startswith("_") and k != "pot"}
chars["hissy"] = {"name": "Old Hissy", "voice": "bm_daniel", "speed": 0.9, "pitch": -2, "color": [0.8, 0.3, 0.2], "kind": "kettle", "size": 1.35, "home": [3, 14], "brows": 16}
B = []
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); B.append(b)
def T(text, cam, hold=1.2, sfx="alarm", do=None):
    b = {"text": text, "cam": cam, "hold": hold, "sfx": sfx}
    if do: b["do"] = do
    B.append(b)
# cold open: hook at 0 s
L("pim", "The kettle SCREAMED! Why did the kettle scream?!", "close:pim", [["pim", "jump"], ["hissy", "shake"]], text="THE KETTLE IS AWAKE!", sfx="alarm")
L("hissy", "Ssssilence! Who dares to tiptoe into MY pantry?", "close:hissy", [["hissy", "eyes_big"], ["all", "look:hissy"]])
L("bup", "Everyone freeze. Don't move. Don't even breathe.", "two:bup,hissy", [["bup", "turn:hissy"]])
L("narr", "Midnight is coming. Mr. Pot has Crispy. And the Golden Crumb led the Dough Bros into the pantry.", "overhead", [["crumb", "spin"]], text="MIDNIGHT IS COMING")
L("lolly", "The key is pulling us behind that kettle. There's a little door back there!", "prop:crumb", [["crumb", "bounce"]])
L("zeek", "A secret tunnel. My calculations say it goes straight to Mr. Pot's oven.", "close:zeek", [["zeek", "eyes_big"]])
L("hissy", "Mr. Pot told me. Nobody passes. Nobody makes a SOUND. I hate noise!", "close:hissy", [["hissy", "jump"]], sfx="suspicious")
L("pim", "He hates noise? I'm made of noise! I'm basically one big scream!", "close:pim", [["pim", "shake"]])
L("bup", "Okay team, here's the plan. We get past him quietly. Very quietly.", "wide", [["bup", "to:-2,8"], ["lolly", "to:5,7"]])
# problem 2: Zeek's trap
L("zeek", "Better plan! Behold, the Sticky-Trap 3000! Pure honey. It catches anything!", "close:zeek", [["zeek", "spin"], ["trap", "show"]], text="THE STICKY-TRAP 3000")
L("lolly", "Zeek, sweetie, are you sure it catches kettles?", "two:lolly,zeek", [["lolly", "turn:zeek"]])
L("zeek", "Absolutely. Eighty percent. Okay, it caught a raisin once.", "close:zeek", [["zeek", "sad"]])
L("narr", "Zeek hides the trap on the cutting board. Now they need bait.", "prop:trap", [["trap", "bounce"]])
L("bup", "Old Hissy! Over here! Come and get us!", "close:bup", [["bup", "to:-9,12"], ["bup", "jump"]])
L("hissy", "NOISE! I'll boil you all into soup!", "wide", [["hissy", "to:-6,12"], ["all", "shake"]], sfx="alarm")
L("bup", "Wait, why are my feet sticky? Why are my feet SO sticky?!", "close:bup", [["bup", "squash"], ["bup", "eyes_big"]])
T("THE TRAP CAUGHT BUP!", "prop:trap", 1.2, "alarm", [["bup", "shake"]])
L("pim", "I'll save you, Bup! Hold on! Oh no. Oh no, no, no. I'm stuck too!", "close:pim", [["pim", "to:-9,11"], ["pim", "shake"]])
L("zeek", "Don't worry! I know how to switch it off. Step one, I walk over here...", "close:zeek", [["zeek", "to:-11,11"]])
L("zeek", "...and step two, I am now also stuck. Wonderful.", "close:zeek", [["zeek", "flat_roof"]])
T("3 HEROES. 1 TRAP.", "wide", 1.3, "suspicious", [["hissy", "laugh"]])
L("hissy", "Ha! Three sticky buns! Mr. Pot will be SO pleased with me.", "close:hissy", [["hissy", "laugh"]])
L("hissy", "And now... a little steam. Just to keep you warm.", "close:hissy", [["hissy", "eyes_big"]], sfx="suspicious")
L("lolly", "Don't you dare! Those are my brothers!", "close:lolly", [["lolly", "flat_roof"], ["lolly", "to:-3,9"]])
L("hissy", "A tiny cookie? Go home, cookie. Ssssilence!", "two:lolly,hissy", [["hissy", "turn:lolly"]])
# plan / turn
L("pim", "Wait. He hates noise. And the steam makes the honey melt. Bup, look! It's melting!", "close:pim", [["pim", "eyes_big"]], text="THE HONEY IS MELTING!")
L("bup", "Pim, that's genius! The louder we are, the hotter he gets!", "close:bup", [["bup", "happy"]])
L("bup", "New plan. Everybody... make... NOISE!", "wide", [["all", "jump"]], sfx="alarm")
L("pim", "AAAAAAH! AAAAAAH! I've been practicing this my whole life!", "close:pim", [["pim", "jump"], ["pim", "shake"]])
L("zeek", "La la la! Loud equations! Two plus two is FOUR!", "close:zeek", [["zeek", "spin"]])
L("lolly", "And I'll sing the loudest song in Table Land! LA LA LAAAA!", "close:lolly", [["lolly", "spin"]])
L("hissy", "Ssstop! Sssstop it! I'm boiling! I'm BOILING OVER!", "close:hissy", [["hissy", "shake"], ["hissy", "jump"]], sfx="alarm")
T("HE'S BOILING OVER!", "close:hissy", 1.2, "alarm", [["hissy", "spin"]])
L("narr", "Steam pours over the trap. The honey melts... and the sticky heroes slide free.", "prop:trap", [["trap", "vanish"], ["bup", "to_home"], ["pim", "to_home"], ["zeek", "to_home"]])
L("hissy", "My water... it's all gone. I'm... so... empty.", "close:hissy", [["hissy", "sad"]])
L("zeek", "Fascinating. He boiled himself dry. My trap worked. Technically.", "close:zeek", [["zeek", "happy"]])
L("lolly", "Sorry, Mister Hissy. We'll be quiet now. Very quiet.", "two:lolly,hissy", [["lolly", "turn:hissy"]])
L("hissy", "Go... before Mr. Pot hears you. The tunnel... is behind me.", "close:hissy", [["hissy", "sleep"]])
# twist
L("narr", "Bup holds up the Golden Crumb. The little door clicks open.", "prop:crumb", [["crumb", "spin"], ["bup", "to:2,12"]], text="THE DOOR OPENS...")
L("bup", "Crispy, hold on. We're coming.", "close:bup", [["bup", "turn:front"]])
L("pim", "It's dark. It's so dark. Why is the tunnel warm? Tunnels should NOT be warm!", "close:pim", [["pim", "shake"]])
L("zeek", "Because we are right under the oven. Eleven fifty-five. Five minutes left.", "close:zeek", [["zeek", "eyes_big"]], text="5 MINUTES LEFT")
L("narr", "Then, from deep in the tunnel, a voice calls out.", "overhead", [["all", "look:bup"]], sfx="suspicious")
L("crispy", "Friends... is that you? Don't come any closer.", "close:crispy", [["crispy", "enter"], ["crispy", "eyes_big"]])
L("lolly", "Crispy! You're okay! We came to take you home!", "close:lolly", [["lolly", "jump"], ["lolly", "happy"]])
L("crispy", "No. Listen. It's a trap. Mr. Pot is not alone anymore.", "close:crispy", [["crispy", "turn:front"]], sfx="alarm")
T("WHO ELSE IS HERE?", "close:crispy", 1.3, "suspicious", [["crispy", "shake"]])
L("pim", "Not alone? What does not alone mean? I don't like not alone!", "close:pim", [["pim", "jump"]])
L("narr", "Behind them, in the dark, something goes click, click, click. And it smells like burning toast.", "wide", [["all", "shake"]], text="TO BE CONTINUED...")
sc = {"title": "Zeek's Trap Caught the Wrong 3 Dough Bros",
      "description": "Mr. Pot has Crispy, midnight is coming, and the only way to the oven is past Old Hissy, the kettle who hates noise. Zeek's honey trap catches the wrong three heroes. Can the loudest bean in Table Land save them?",
      "set": {"place": "pantry", "time": "night"}, "chars": chars,
      "props": [{"id": "crumb", "type": "key", "color": "gold", "on": "bup", "visible": True, "scale": 0.8},
                {"id": "trap", "type": "box", "color": [0.95, 0.65, 0.1], "on": "podium", "visible": False, "scale": 1.6}],
      "beats": B}
json.dump(sc, open("scripts3d/ep021.json", "w"), indent=1, ensure_ascii=False)
print(len(B), "beats")

# builds scripts3d/ep036.json (run from hollow/) — The Dark Watchers of Big Sur (standalone story, no serial references)
import json
src = json.load(open('scripts3d/ep035.json'))
ch = {'narr': src['chars']['narr']}
def H(name, voice, pitch, col, home, size=0.85):
    return {"name": name, "voice": voice, "speed": 0.95, "pitch": pitch, "color": col, "kind": "human", "size": size, "home": home}
def W(home, size=1.25):
    return {"name": "Dark Watcher", "voice": "bm_daniel", "speed": 0.8, "pitch": -4, "color": [0.012, 0.012, 0.016], "kind": "watcher", "size": size, "home": home}
ch['hiker'] = H("The hiker", "am_michael", 0, [0.42, 0.3, 0.16], [-3, 8])
ch['w1'] = W([-7, 26]); ch['w2'] = W([1.5, 28], 1.35); ch['w3'] = W([9, 25])
ch['w4'] = W([30, 40], 1.3)
ch['mother'] = H("A mother", "bf_emma", 0, [0.35, 0.12, 0.1], [-30, 30], 0.8)
ch['tom'] = H("A boy", "am_puck", 2, [0.2, 0.3, 0.45], [-30, 32], 0.55)
ch['gran'] = H("Grandmother", "bf_alice", 0, [0.3, 0.25, 0.32], [-30, 34], 0.75)
ch['principal'] = H("A hiker in the 1960s", "am_eric", 0, [0.25, 0.25, 0.3], [-30, 36], 0.85)
P = lambda t, i, c, at, sc, vis=False, glow=0: {"type": t, "id": i, "color": c, "glow": glow, "visible": vis, "scale": sc, "at": at}
props = [P("box", "rock", [0.3, 0.3, 0.32], [6, 20, 0.9], 1.8, True, 0),
         P("box", "book", [0.45, 0.12, 0.08], [-1.5, 9.5, 1.4], 0.4, False, 1),
         P("ball", "fruit", [0.9, 0.45, 0.1], [-4.5, 10, 0.5], 0.3, False, 2),
         P("star", "shell", [0.95, 0.9, 0.82], [-3.5, 10, 0.5], 0.35, False, 2),
         P("ball", "sun", [1.0, 0.55, 0.25], [-12, 34, 3.0], 2.2, False, 6),
         P("ball", "moon", [0.8, 0.85, 1.0], [10, 40, 14], 1.6, True, 4)]
B = []
def b(who, say, cam, do=(), sfx=None, text=None):
    x = {"who": who, "say": say, "cam": cam, "do": [list(d) for d in do]}
    if sfx: x["sfx"] = sfx
    if text: x["text"] = text
    B.append(x)
b("narr", "Something tall is standing on that ridge. And it is watching you.", "close:w2", [("w2", "turn:front"), ("w1", "to:-5,25,0"), ("w2", "shake")], "alarm", "DON'T LOOK AT THE RIDGE")
b("hiker", "Who's up there? Hello? Can you hear me?", "close:hiker", [("hiker", "shake"), ("hiker", "turn:w2")], "suspicious", "HELLO?")
b("narr", "This is a real legend from the Santa Lucia Mountains, in Big Sur, California.", "wide", [("moon", "bounce"), ("w3", "turn:hiker")], "horn", "BIG SUR, CALIFORNIA")
b("narr", "People call them the Dark Watchers.", "close:w1", [("w1", "turn:front")], "rumble", "THE DARK WATCHERS")
b("narr", "Tall black shapes. No faces. Some wear a wide hat. Some carry a stick.", "close:w3", [("w3", "turn:front"), ("w3", "shake")], "crunch", "NO FACES")
b("narr", "They stand on the ridges at dusk and at dawn. And they only watch.", "wide", [("w2", "turn:hiker"), ("w1", "turn:hiker")], "suspicious", "THEY ONLY WATCH")
b("hiker", "I'm going closer. I want to see its face.", "close:hiker", [("hiker", "to:0,15,0")], "whoosh", "GOING CLOSER")
b("narr", "Here is the strange part. No one has ever seen one up close.", "close:w2", [("w2", "turn:hiker")], "suspicious", "NOBODY GETS CLOSE")
b("narr", "Walk toward them, the legend says, and they vanish.", "close:w2", [("w2", "exit")], "whoosh", "THEY VANISH")
b("hiker", "It's gone! It was right there a second ago!", "close:hiker", [("hiker", "eyes_big"), ("hiker", "jump")], "alarm", "GONE!")
b("narr", "The stories are old. Writers say Spanish settlers called them Los Vigilantes Oscuros.", "wide", [("hiker", "to:-3,9,0"), ("moon", "bounce")], "horn", "LOS VIGILANTES OSCUROS")
b("narr", "But no old record of those stories has ever been found.", "close:w1", [("w1", "shake")], "rumble", "NO OLD RECORD")
b("narr", "The first writing we can read comes from two famous writers.", "prop:book", [("book", "show"), ("book", "spin")], "pop", "TWO FAMOUS WRITERS")
b("narr", "In nineteen thirty-seven, the poet Robinson Jeffers wrote of watchers in these hills.", "prop:book", [("book", "bounce")], "suspicious", "1937: A POEM")
b("narr", "One year later, John Steinbeck wrote a story called Flight.", "prop:book", [("book", "spin")], "pop", "1938: STEINBECK")
b("narr", "In it, a mother warns her son before he rides into the mountains.", "close:mother", [("mother", "to:-1,10,0"), ("mother", "turn:front"), ("book", "hide")], "whoosh", "A MOTHER'S WARNING")
b("mother", "If you see the dark watching men up there, do not go near them.", "close:mother", [("mother", "shake")], "rumble", "DO NOT GO NEAR THEM")
b("narr", "Better to ignore them, the story says. Don't look. Don't follow.", "close:w1", [("mother", "exit"), ("w1", "turn:front")], "crunch", "DON'T LOOK. DON'T FOLLOW.")
b("narr", "Steinbeck's son Thomas grew up near these mountains.", "close:tom", [("tom", "to:-2,9,0"), ("tom", "turn:front")], "pop", "HIS SON, THOMAS")
b("narr", "Thomas Steinbeck said he saw the watchers himself, when he was a child.", "close:tom", [("tom", "eyes_big"), ("tom", "turn:w3")], "alarm", "HE SAW THEM")
b("narr", "He said his grandmother left fruit and nuts out for them.", "prop:fruit", [("gran", "to:-5,10.5,0"), ("fruit", "show")], "pop", "GIFTS FOR THE WATCHERS")
b("narr", "And in return, she found shells and feathers left behind.", "prop:shell", [("shell", "show"), ("shell", "spin"), ("fruit", "hide")], "suspicious", "SOMETHING GAVE BACK")
b("hiker", "Shells? On a mountain? Who carries shells up a mountain?", "close:hiker", [("hiker", "shake"), ("hiker", "turn:front")], "crunch", "WHO LEFT THEM?")
b("narr", "If this gave you chills, subscribe. A new real legend every day.", "two:hiker,tom", [("tom", "exit"), ("gran", "exit"), ("shell", "hide")], "pop", "SUBSCRIBE")
b("narr", "In the nineteen sixties, a newspaper told of a former school principal out hiking.", "close:principal", [("principal", "to:2,12,0"), ("principal", "turn:front")], "horn", "1960s: A HIKE")
b("narr", "He saw a dark figure, standing still on top of a rock.", "prop:rock", [("w3", "to:6,21.5,0"), ("w3", "turn:principal")], "rumble", "A FIGURE ON A ROCK")
b("principal", "Look! Up there, on the rock! Do you see it?", "close:principal", [("principal", "turn:w3"), ("principal", "jump")], "alarm", "LOOK!")
b("narr", "He called out to the other hikers. They turned to look.", "two:principal,hiker", [("hiker", "turn:w3")], "whoosh", "THEY TURNED")
b("narr", "The figure was gone.", "prop:rock", [("w3", "exit")], "crunch", "GONE")
b("narr", "Would you climb up to that rock? Yes or no? Tell me in the comments.", "prop:rock", [("rock", "bounce")], "suspicious", "WOULD YOU CLIMB IT?")
b("narr", "So what are they? Scientists have an idea.", "wide", [("principal", "exit"), ("sun", "show")], "pop", "WHAT ARE THEY?")
b("narr", "When the sun is low, your shadow can fall on a bank of fog or cloud.", "prop:sun", [("sun", "bounce")], "whoosh", "THE SUN IS LOW")
b("narr", "It looks like a giant dark person. It's called a Brocken spectre.", "close:w1", [("w1", "turn:front"), ("w1", "shake")], "rumble", "A BROCKEN SPECTRE")
b("narr", "Others say tired hikers, alone in the hills, simply see things.", "close:hiker", [("hiker", "sad"), ("sun", "hide")], "suspicious", "TIRED EYES?")
b("hiker", "My own shadow? Then why does it move when I'm standing still?", "close:hiker", [("hiker", "shake"), ("w1", "to:-4,24,0")], "alarm", "IT MOVED")
b("narr", "No one has caught a watcher on camera. And no one has proved they aren't there.", "wide", [("w2", "to:1.5,28,0"), ("w2", "turn:hiker")], "rumble", "NO PROOF EITHER WAY")
b("narr", "So here is the rule of the Santa Lucias. Never walk toward the Dark Watchers.", "close:w2", [("w2", "shake")], "crunch", "NEVER WALK TOWARD THEM")
b("hiker", "Okay. I'm turning around. And I am not looking back.", "close:hiker", [("hiker", "turn:front"), ("hiker", "to:-3,7,0")], "whoosh", "DON'T LOOK BACK")
b("narr", "The sun went down. The fog came in. The hiker counted the ridge, one last time.", "wide", [("w3", "to:9,25,0"), ("w3", "turn:hiker")], "suspicious", "COUNT THEM")
b("hiker", "One. Two. Three. There were three before. Now there are four.", "close:hiker", [("hiker", "eyes_big"), ("w4", "to:-1,11,0")], "alarm", "FOUR?")
b("narr", "Because the fourth one was not on the ridge. It was right behind the hiker.", "close:w4", [("w4", "turn:hiker"), ("w4", "shake")], "rumble", "RIGHT BEHIND YOU")
b("narr", "What do you think happens next? Tell me in the comments.", "two:hiker,w4", [("hiker", "shake"), ("w4", "turn:front")], "horn", "WHAT HAPPENS NEXT?")
s = {"title": "Big Sur's Dark Watchers: Would You Go Closer?",
     "description": "A real California legend: the Dark Watchers of the Santa Lucia Mountains. What do you think happens next? Tell me in the comments.",
     "lead_in": 0.0, "set": {"place": "hill", "fog": 0.05, "eyes": 0, "moonlight": 12}, "chars": ch, "props": props, "beats": B}
json.dump(s, open('scripts3d/ep036.json', 'w'), indent=1, ensure_ascii=False)
print(len(B), sum(len(x['say'].split()) for x in B), len(s['title']), max(len(x['say'].split()) for x in B))

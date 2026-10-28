# builds scripts3d/ep039.json (run from hollow/) — the vanishing of Owen Parfitt, Shepton Mallet, Somerset, June 1768 (standalone story)
# Sources: historicmysteries.com/owen-parfitt (porch chair, storm, farmworkers, 1813 skeleton = young woman) ;
#          history.co.uk/articles/more-historys-most-famous-unsolved-disappearances (June 1768, some say 1763; Susannah Snook; devil / pirate rumours) ;
#          shows.acast.com/mysteries-at-bedtime/episodes/the-man-who-vanished-from-his-chair (aged ~69, paralysed, greatcoat left, ~7 pm, farm hands a dozen yards away)
import json
src = json.load(open('scripts3d/ep038.json'))
ch = {'narr': src['chars']['narr']}
def H(name, voice, pitch, col, home, size=0.85, speed=0.95):
    return {"name": name, "voice": voice, "speed": speed, "pitch": pitch, "color": col, "kind": "human", "size": size, "home": home}
ch['owen'] = H("Owen Parfitt", "bm_daniel", -2, [0.42, 0.30, 0.20], [0, 9.2], 0.85, 0.85)
ch['sister'] = H("His sister", "bf_isabella", -1, [0.55, 0.35, 0.50], [-4.2, 8.4], 0.8)
ch['neigh'] = H("The neighbour", "af_sarah", 1, [0.75, 0.50, 0.20], [4.2, 8.4], 0.8, 1.0)
ch['farm'] = H("A farm worker", "am_michael", 0, [0.25, 0.30, 0.15], [-13, 19], 0.9, 1.0)
P = lambda t, i, c, at, sc, vis=False, glow=0: {"type": t, "id": i, "color": c, "glow": glow, "visible": vis, "scale": sc, "at": at}
props = [P("box", "chair", [0.50, 0.32, 0.16], [0, 10.4, 0], 0.9, True, 0),
         P("box", "coat", [0.20, 0.22, 0.38], [0, 10.3, 1.05], 0.55, True, 0),
         P("box", "door", [0.25, 0.18, 0.10], [0, 13.2, 0], 2.4, True, 0),
         P("cone", "lamp", [1.0, 0.8, 0.45], [-2.6, 12.4, 2.6], 0.3, True, 4),
         P("box", "bones", [0.85, 0.82, 0.72], [6, 11, 0], 0.5, False, 1),
         P("box", "paper", [0.9, 0.88, 0.8], [-3, 9, 1.4], 0.45, False, 1),
         P("ball", "moon", [0.8, 0.85, 1.0], [10, 40, 14], 1.6, True, 4)]
B = []
def b(who, say, cam, do=(), sfx=None, text=None):
    x = {"who": who, "say": say, "cam": cam, "do": [list(d) for d in do]}
    if sfx: x["sfx"] = sfx
    if text: x["text"] = text
    B.append(x)
# cold open at 0 s: the empty chair, motion + big text on frame 1
b("sister", "Owen? Owen! Where are you? You cannot even walk!", "prop:chair", [("sister", "to:-1.6,8.6,0"), ("coat", "bounce"), ("owen", "dive")], "alarm", "HE CAN'T WALK")
b("narr", "His chair is still here. His coat is still here. But the man is gone.", "prop:coat", [("coat", "spin"), ("sister", "eyes_big")], "dun", "THE CHAIR IS EMPTY")
b("narr", "This is a true story. Shepton Mallet, England. A June evening in seventeen sixty-eight.", "wide", [("moon", "bounce"), ("coat", "home")], "horn", "ENGLAND, 1768")
b("narr", "Minutes earlier, an old man named Owen Parfitt sat in that chair by the door.", "close:owen", [("owen", "rise")], "suspicious", "MINUTES EARLIER")
b("owen", "Put me by the door, sister. I want to watch the evening.", "close:owen", [("owen", "turn:sister")], "chime", "BY THE DOOR")
b("narr", "Owen was about seventy. He was paralysed. He could not stand up on his own.", "close:owen", [("owen", "sad")], "rumble", "HE COULD NOT STAND")
b("narr", "His elderly sister and a young neighbour carried him out, chair and all.", "two:sister,neigh", [("sister", "to:-2.2,8.8,0"), ("neigh", "to:2.2,8.8,0")], "whoosh", "THEY CARRIED HIM OUT")
b("neigh", "There you are, Mister Parfitt. Your greatcoat is right behind you.", "close:neigh", [("coat", "bounce"), ("neigh", "happy")], "pop", "HIS GREATCOAT")
b("narr", "People said Owen had sailed the seas when he was young. Some whispered he had been a pirate.", "close:owen", [("owen", "laugh")], "horn", "A PIRATE?")
b("owen", "I have seen things out there, girl. Things you would not believe.", "close:owen", [("owen", "turn:neigh"), ("neigh", "eyes_big")], "suspicious", "THINGS OUT THERE")
b("narr", "Across the road, farm workers were busy in the field. Just a few yards away.", "close:farm", [("farm", "turn:owen")], "engine", "A FEW YARDS AWAY")
b("narr", "Then the sky went dark. A storm was rolling in.", "wide", [("moon", "hide"), ("lamp", "bounce")], "rumble", "A STORM IS COMING")
b("sister", "Rain is coming. Let us get his bed ready, then bring him in.", "close:sister", [("sister", "turn:neigh")], "chime", "BRING HIM IN")
b("narr", "The two women stepped inside the house. Only for a few minutes.", "prop:door", [("sister", "to:-1,12.6,0"), ("neigh", "to:1,12.6,0"), ("door", "bounce")], "whoosh", "ONLY A FEW MINUTES")
b("narr", "Owen sat alone by the open door. The wind began to blow.", "close:owen", [("owen", "turn:front"), ("lamp", "spin")], "rumble", "ALONE")
b("narr", "Nobody knows what he saw next. Nobody ever will.", "close:owen", [("owen", "eyes_big"), ("owen", "shake")], "dun", "WHAT DID HE SEE?")
b("narr", "The women came back out. And the chair was empty.", "prop:chair", [("owen", "dive"), ("sister", "to:-1.6,8.6,0"), ("neigh", "to:1.6,8.6,0")], "alarm", "THE CHAIR WAS EMPTY")
b("neigh", "He cannot walk! How can he be gone?", "close:neigh", [("neigh", "eyes_big"), ("neigh", "shake")], "alarm", "HOW?")
b("narr", "His greatcoat still lay on the chair, exactly where they had left it.", "prop:coat", [("coat", "bounce")], "dun", "THE COAT STAYED")
b("narr", "If you love true stories with no answer, subscribe now. It gets stranger.", "wide", [("lamp", "bounce")], "pop", "SUBSCRIBE")
b("sister", "You men! Did someone take my brother? Did you see anyone?", "close:sister", [("sister", "to:-6,12,0"), ("farm", "to:-9,15,0")], "alarm", "DID YOU SEE ANYONE?")
b("farm", "Nobody passed this road. We saw nothing. We heard nothing.", "close:farm", [("farm", "shake")], "suspicious", "WE SAW NOTHING")
b("narr", "A man who could not walk had vanished in minutes, in plain sight of the road.", "wide", [("farm", "turn:sister")], "rumble", "GONE IN MINUTES")
b("narr", "The whole town searched through the storm. Fields, ditches, wells, the woods.", "wide", [("sister", "to:6,16,0"), ("neigh", "to:-6,16,0"), ("farm", "to:0,18,0")], "whoosh", "THE TOWN SEARCHED")
b("neigh", "Owen! Owen Parfitt! Can you hear us?", "close:neigh", [("neigh", "turn:front")], "alarm", "CAN YOU HEAR US?")
b("narr", "They searched for days. They found no footprint, no button, no trace at all.", "prop:chair", [("coat", "spin")], "dun", "NO TRACE")
b("narr", "Some in the town said the Devil came for him that night.", "close:sister", [("sister", "sad")], "rumble", "THE DEVIL?")
b("narr", "Others said old pirate friends carried him off, to show them buried treasure.", "close:farm", [("farm", "eyes_big")], "horn", "OLD PIRATE FRIENDS?")
b("narr", "Forty-five years later, in eighteen thirteen, builders dug up bones near the town.", "prop:bones", [("bones", "show"), ("bones", "bounce")], "crunch", "1813: BONES FOUND")
b("narr", "Everyone said, it is Owen at last. But doctors said they belonged to a young woman.", "prop:bones", [("bones", "spin")], "dun", "NOT OWEN")
b("narr", "Owen Parfitt was never seen again. No one has ever explained it.", "close:sister", [("bones", "hide"), ("sister", "to_home")], "suspicious", "NEVER SEEN AGAIN")
b("narr", "So here is the rule of Shepton Mallet. Never leave anyone alone by the door when a storm comes.", "prop:door", [("door", "bounce")], "dun", "NEVER LEAVE THEM ALONE")
b("narr", "Many years later, a new family moved into that same house.", "wide", [("neigh", "to_home"), ("farm", "exit"), ("moon", "show")], "chime", "YEARS LATER")
b("neigh", "It's only an old story. I'll just leave Grandpa by the door for one minute.", "close:neigh", [("neigh", "happy")], "suspicious", "ONLY ONE MINUTE")
b("narr", "She turned her back. The wind rose. And the old chair began to creak.", "prop:chair", [("lamp", "spin"), ("chair", "bounce")], "whoosh", "THE CHAIR CREAKED")
b("neigh", "Grandpa? Who is that standing in our doorway?", "close:neigh", [("neigh", "eyes_big"), ("owen", "rise")], "alarm", "WHO IS IN THE DOOR?")
b("narr", "In the doorway stood an old man in a sailor's coat. And he was smiling.", "two:neigh,owen", [("owen", "turn:neigh"), ("owen", "laugh")], "rumble", "HE CAME BACK")
b("narr", "What do you think happens next? Tell me in the comments.", "two:neigh,owen", [("neigh", "shake"), ("owen", "shake")], "horn", "WHAT HAPPENS NEXT?")
s = {"title": "Who Took the Old Man From His Chair? (Ep 39)",
     "description": "A true story from Shepton Mallet, England, 1768: the vanishing of Owen Parfitt. What do you think happens next? Tell me in the comments.",
     "lead_in": 0.0, "set": {"place": "village", "fog": 0.025, "eyes": 0, "moonlight": 22}, "chars": ch, "props": props, "beats": B}
json.dump(s, open('scripts3d/ep039.json', 'w'), indent=1, ensure_ascii=False)
print(len(B), sum(len(x['say'].split()) for x in B), len(s['title']), max(len(x['say'].split()) for x in B))

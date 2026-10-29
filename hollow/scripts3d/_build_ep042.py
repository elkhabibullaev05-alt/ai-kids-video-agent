"""Build scripts3d/ep042.json - Hinton Ampner, Hampshire (Ricketts haunting, 1765-1771). Standalone true story.
python3 scripts3d/_build_ep042.py"""
import json, os

H = os.path.dirname(os.path.abspath(__file__))

def ch(name, voice, speed, pitch, color=None, kind=None, size=None, home=None, **kw):
    c = {"name": name, "voice": voice, "speed": speed, "pitch": pitch}
    if kind:
        c.update(color=color, kind=kind, size=size, home=home)
    c.update(kw)
    return c

def prop(t, pid, color, glow, vis, scale, at):
    return {"type": t, "id": pid, "color": color, "glow": glow, "visible": vis, "scale": scale, "at": at}

def B(who, say, cam, do, sfx, text):
    return {"who": who, "say": say, "cam": cam, "do": do, "sfx": sfx, "text": text}

chars = {
    "narr": ch("Narrator", "bm_george", 0.92, -1),
    "mary": ch("Mary Ricketts", "bf_emma", 0.95, 0, [0.32, 0.2, 0.3], "human", 0.8, [-3.2, 8.2]),
    "nurse": ch("The nurse", "bf_isabella", 1.0, 0, [0.5, 0.48, 0.42], "human", 0.78, [3.2, 8.2]),
    "jervis": ch("Captain John Jervis", "bm_lewis", 0.95, -1, [0.08, 0.1, 0.25], "human", 0.92, [-30, 32]),
    "lutt": ch("Captain Luttrell", "am_adam", 1.0, 0, [0.3, 0.1, 0.08], "human", 0.9, [-34, 34]),
    "drab": ch("The man in brown", "bm_daniel", 0.8, -4, [0.2, 0.15, 0.09], "human", 0.95, [-36, 40]),
    "silk": ch("The woman in silk", "bf_alice", 0.9, -1, [0.75, 0.75, 0.8], "lady", 0.85, [36, 40], ghost=True),
    "girl": ch("A little girl", "af_sarah", 1.08, 2, [0.4, 0.3, 0.45], "human", 0.6, [-40, 44]),
}

props = [
    prop("box", "door", [0.25, 0.17, 0.1], 0, True, 2.4, [-6, 12, 0]),
    prop("box", "bed", [0.55, 0.45, 0.2], 0, True, 0.9, [1.8, 11.0, 0]),
    prop("cone", "candle", [1.0, 0.85, 0.5], 4, True, 0.35, [-0.8, 9.2, 1.4]),
    prop("box", "floorbox", [0.18, 0.12, 0.07], 0, False, 0.6, [3.5, 8.0, 0]),
    prop("ball", "skull", [0.92, 0.9, 0.82], 1, False, 0.3, [3.5, 8.0, 0.9]),
    prop("box", "letter", [0.9, 0.88, 0.8], 1, False, 0.45, [-3.5, 8.5, 1.4]),
    prop("ball", "moon", [0.8, 0.85, 1.0], 4, True, 1.6, [10, 40, 14]),
]

beats = [
    # 0-5 s: hook at frame 1 (danger, mid-tension)
    B("mary", "Footsteps. Heavy footsteps, right beside my bed. And there is nobody there.", "close:mary",
      [["mary", "eyes_big"], ["drab", "to:-0.5,10.4,0"], ["candle", "spin"]], "alarm", "SOMEONE IS IN MY ROOM"),
    B("narr", "For six years, this English manor would not let its family sleep.", "wide",
      [["bed", "bounce"], ["drab", "to_home"]], "dun", "6 YEARS. NO SLEEP."),
    B("narr", "This is a true story. Hinton Ampner, Hampshire, England. The year, seventeen sixty-five.", "wide",
      [["moon", "bounce"]], "horn", "HAMPSHIRE, 1765"),
    B("narr", "Mary Ricketts rented the old manor house with her husband, three children and their servants.", "two:mary,nurse",
      [["mary", "turn:front"], ["nurse", "turn:mary"]], "chime", "A NEW HOME"),
    B("mary", "Such a fine old house, and so peaceful. The children will love it here.", "close:mary",
      [["mary", "happy"]], "pop", "SO PEACEFUL"),
    B("narr", "In the daytime it was peaceful. At night, the doors began to slam.", "prop:door",
      [["door", "bounce"], ["mary", "jump"]], "crunch", "DOORS SLAMMING"),
    B("narr", "The servants searched every room. Every lock was closed. They found no one.", "wide",
      [["nurse", "to:-5,11,0"], ["nurse", "turn:front"]], "suspicious", "NOBODY THERE"),
    B("nurse", "Madam! A man just walked into your bedroom. A man in dull brown clothes!", "close:nurse",
      [["nurse", "shake"], ["drab", "to:-6,12.5,0"]], "alarm", "A MAN IN BROWN"),
    B("narr", "They ran after him into the Yellow Room, her bedroom. It was empty.", "prop:door",
      [["drab", "to_home"], ["mary", "to:-4.5,11,0"]], "whoosh", "THE YELLOW ROOM"),
    B("narr", "Other servants saw a woman in a rustling silk dress, gliding along the passage.", "close:silk",
      [["silk", "to:4.5,12,0"], ["silk", "turn:front"]], "suspicious", "A WOMAN IN SILK"),
    B("narr", "Then came the moans. Low, dismal moans in the dark, night after night.", "wide",
      [["silk", "to_home"], ["candle", "spin"], ["nurse", "to_home"]], "rumble", "THE MOANS"),
    B("narr", "In seventeen sixty-nine, her husband sailed far away to Jamaica, on business.", "close:mary",
      [["mary", "to_home"], ["mary", "sad"]], "whoosh", "SHE WAS ALONE"),
    B("mary", "So now it is only me, my children, and whatever walks these halls.", "close:mary",
      [["mary", "sad"], ["moon", "bounce"]], "dun", "WHAT WALKS THESE HALLS?"),
    B("narr", "One night, heavy plodding footsteps crossed her room and stopped beside her bed.", "two:mary,drab",
      [["drab", "to:0.2,10.2,0"], ["bed", "bounce"]], "dun", "PLOD. PLOD. PLOD."),
    B("mary", "Who is there? Answer me!", "close:mary",
      [["mary", "shake"], ["mary", "eyes_big"]], "alarm", "WHO IS THERE?"),
    B("narr", "Nothing answered. The footsteps simply stopped.", "wide",
      [["drab", "to_home"]], "suspicious", "SILENCE"),
    B("narr", "Then the voices began. A murmur inside the walls, moving from room to room.", "prop:door",
      [["door", "spin"], ["candle", "bounce"]], "rumble", "VOICES IN THE WALLS"),
    B("narr", "Sometimes the murmur turned into real words. Nobody could ever say whose.", "close:mary",
      [["mary", "turn:front"], ["mary", "eyes_big"]], "suspicious", "WHOSE VOICE?"),
    B("narr", "And sometimes a rushing sound fell on a room, as fast and hard as a falling wall.", "wide",
      [["candle", "spin"], ["bed", "jump"], ["mary", "jump"]], "whoosh", "A RUSHING SOUND"),
    B("narr", "If you like true stories like this one, subscribe. Because now, her brother arrives.", "wide",
      [["jervis", "to:-5,9.5,0"]], "chime", "SUBSCRIBE"),
    B("narr", "Mary's brother was Captain John Jervis of the Royal Navy, later a famous admiral.", "close:jervis",
      [["jervis", "turn:front"]], "horn", "HER BROTHER, THE CAPTAIN"),
    B("jervis", "Ghosts? Nonsense, sister. I will catch whoever is playing these tricks.", "two:jervis,mary",
      [["jervis", "laugh"], ["mary", "to:-1.5,9,0"]], "pop", "I WILL CATCH IT"),
    B("narr", "He and his friend, Captain Luttrell, sat up night after night, armed and waiting.", "two:jervis,lutt",
      [["lutt", "to:-2.5,11,0"], ["lutt", "turn:front"], ["jervis", "turn:front"]], "suspicious", "ARMED AND WAITING"),
    B("narr", "They heard groans. Banging. Dragging footsteps in the empty rooms.", "prop:door",
      [["door", "bounce"], ["candle", "spin"]], "rumble", "GROANS. BANGING."),
    B("lutt", "There! In the passage! Someone is running!", "close:lutt",
      [["lutt", "jump"], ["drab", "to:-7,13,0"]], "alarm", "THERE!"),
    B("narr", "They ran out with candles. The passage was empty. Nobody was ever caught.", "wide",
      [["jervis", "to:-6,12,0"], ["lutt", "to:-5,12.6,0"], ["drab", "to_home"]], "whoosh", "EMPTY"),
    B("narr", "Once, Jervis even heard a gunshot inside the house. Nobody had fired.", "close:jervis",
      [["jervis", "eyes_big"], ["jervis", "shake"]], "crunch", "A GUNSHOT?"),
    B("jervis", "Sister, pack your things. You are not staying here one more night.", "two:jervis,mary",
      [["jervis", "turn:mary"], ["mary", "sad"]], "dun", "LEAVE. NOW."),
    B("narr", "In seventeen seventy-one, Mary Ricketts gave up the house and left for good.", "wide",
      [["mary", "to_home"], ["jervis", "to_home"], ["lutt", "to_home"]], "horn", "SHE LEFT, 1771"),
    B("narr", "Years later, one writer claimed a maid had played tricks. Mary never believed it.", "close:mary",
      [["mary", "turn:front"]], "suspicious", "A TRICK?"),
    B("narr", "No maid could explain the voices, the rushing sound, or the man in brown.", "prop:door",
      [["door", "bounce"]], "dun", "NO ANSWER"),
    B("narr", "In seventeen ninety-three, the old house was pulled down.", "wide",
      [["door", "hide"], ["bed", "hide"]], "crunch", "PULLED DOWN, 1793"),
    B("narr", "Under the floor, the workmen found a box. Inside it was a small skull.", "prop:floorbox",
      [["floorbox", "show"], ["skull", "show"]], "alarm", "A SKULL UNDER THE FLOOR"),
    B("narr", "Some said it was a monkey's skull. Nobody ever found out why it was there.", "prop:skull",
      [["skull", "spin"]], "suspicious", "WHY WAS IT THERE?"),
    B("narr", "A new house was built a short walk away. It still stands today.", "wide",
      [["skull", "hide"], ["floorbox", "hide"], ["moon", "bounce"]], "chime", "IT STILL STANDS"),
    B("narr", "So remember the rule of Hinton Ampner. Never answer the voices in the walls.", "wide",
      [["candle", "spin"]], "dun", "NEVER ANSWER THE WALLS"),
    B("narr", "Years later, a little girl lies awake in the dark.", "close:girl",
      [["girl", "to:-1.5,9.5,0"], ["bed", "show"]], "rumble", "YEARS LATER..."),
    B("girl", "Hello? Is somebody there?", "close:girl",
      [["girl", "eyes_big"], ["girl", "shake"]], "suspicious", "HELLO?"),
    B("narr", "Plod. Plod. Plod. The footsteps stop beside her bed. And something answers.", "two:girl,drab",
      [["drab", "to:0.2,10.2,0"], ["girl", "jump"]], "alarm", "IT ANSWERED"),
    B("drab", "Yes. I have always been here.", "close:drab",
      [["drab", "turn:girl"], ["candle", "spin"]], "dun", "I HAVE ALWAYS BEEN HERE"),
    B("narr", "What do you think happens next? Tell me in the comments.", "two:girl,drab",
      [["girl", "shake"]], "suspicious", "WHAT HAPPENS NEXT?"),
]

sc = {
    "title": "She Heard Footsteps by Her Bed. Who? (Ep 42)",
    "description": "A true haunting from Hinton Ampner, Hampshire (1765-1771): footsteps, voices in the walls and a man in brown. What do you think happens next? Tell me in the comments.",
    "lead_in": 0.0,
    "set": {"place": "village", "fog": 0.05, "eyes": 0, "moonlight": 12},
    "chars": chars, "props": props, "beats": beats,
}
json.dump(sc, open(os.path.join(H, "ep042.json"), "w"), indent=1, ensure_ascii=False)
print("ok", len(beats), "beats", sum(len(b["say"].split()) for b in beats), "words")

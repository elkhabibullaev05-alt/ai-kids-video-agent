"""Build scripts3d/ep045.json — the ghost ship Baychimo (Alaska, 1931-1969). Run: python3 scripts3d/_build_ep045.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.92, "pitch": -1},
 "cornwell": {"name": "Captain Cornwell", "voice": "bm_lewis", "speed": 0.96, "pitch": -1, "color": [0.12, 0.14, 0.25], "kind": "human", "size": 0.9, "home": [-3.0, 8.4]},
 "sailor": {"name": "A sailor", "voice": "am_michael", "speed": 1.0, "pitch": 0, "color": [0.45, 0.2, 0.12], "kind": "human", "size": 0.84, "home": [-30, 32]},
 "hunter": {"name": "A seal hunter", "voice": "am_adam", "speed": 0.98, "pitch": -1, "color": [0.4, 0.3, 0.2], "kind": "human", "size": 0.86, "home": [-34, 34]},
 "polson": {"name": "Captain Polson", "voice": "bm_daniel", "speed": 0.98, "pitch": -1, "color": [0.2, 0.25, 0.22], "kind": "human", "size": 0.88, "home": [-38, 40]},
 "boy": {"name": "A young sailor", "voice": "am_puck", "speed": 1.04, "pitch": 1, "color": [0.25, 0.3, 0.42], "kind": "human", "size": 0.7, "home": [-42, 44]},
}
props = [
 {"type": "ship", "id": "ship", "color": [0.07, 0.07, 0.08], "glow": 0, "visible": True, "scale": 0.95, "at": [3.0, 19.0, 0]},
 {"type": "ship", "id": "ghost", "color": [0.1, 0.12, 0.16], "glow": 0.15, "lit": True, "visible": False, "scale": 0.95, "at": [-6.0, 24.0, 0]},
 {"type": "box", "id": "hut", "color": [0.28, 0.18, 0.1], "glow": 0, "visible": True, "scale": 1.6, "at": [-6.5, 12.5, 0]},
 {"type": "cone", "id": "fire", "color": [1.0, 0.45, 0.08], "glow": 5, "visible": True, "scale": 0.4, "at": [0.6, 11.2, 0]},
 {"type": "box", "id": "furs", "color": [0.35, 0.22, 0.12], "glow": 0, "visible": False, "scale": 0.5, "at": [-1.0, 10.2, 0.0]},
 {"type": "box", "id": "paper", "color": [0.85, 0.83, 0.75], "glow": 1, "visible": False, "scale": 0.55, "at": [-1.2, 9.4, 1.3]},
 {"type": "ball", "id": "lamp", "color": [1.0, 0.8, 0.4], "glow": 8, "visible": False, "scale": 0.3, "at": [-4.4, 23.5, 1.25]},
 {"type": "ball", "id": "moon", "color": [0.8, 0.85, 1.0], "glow": 4, "visible": True, "scale": 1.6, "at": [10, 40, 14]},
]
B = lambda who, say, cam, do, sfx, text: {"who": who, "say": say, "cam": cam, "do": do, "sfx": sfx, "text": text}
beats = [
 B("narr", "Don't climb aboard. This ship has had no crew for thirty-eight years.", "prop:ship", [["ship", "shake"], ["moon", "bounce"]], "alarm", "DON'T BOARD THAT SHIP"),
 B("sailor", "Captain! She's gone! The ice is empty! The ship is gone!", "close:sailor", [["sailor", "to:-1.5,9.4,0"], ["sailor", "eyes_big"], ["ship", "hide"]], "rumble", "THE SHIP IS GONE"),
 B("narr", "This is a true story. Her name was the Baychimo.", "wide", [["sailor", "to_home"], ["ship", "show"]], "dun", "A TRUE STORY"),
 B("narr", "New episode every day. Subscribe so you don't miss what happens next.", "prop:hut", [["hut", "bounce"]], "pop", "SUBSCRIBE"),
 B("narr", "She was a steel cargo steamer, built in Sweden in nineteen fourteen.", "prop:ship", [["ship", "bounce"]], "horn", "BUILT 1914"),
 B("narr", "The Hudson's Bay Company used her to carry furs from the Arctic.", "prop:furs", [["furs", "show"], ["furs", "bounce"]], "whoosh", "A CARGO OF FURS"),
 B("narr", "In October nineteen thirty-one, near Barrow in Alaska, the sea froze around her.", "wide", [["furs", "hide"], ["moon", "bounce"]], "rumble", "OCTOBER 1931"),
 B("cornwell", "We're stuck fast. The ice has her. We wait for spring.", "close:cornwell", [["cornwell", "turn:front"], ["cornwell", "sad"]], "dun", "TRAPPED IN THE ICE"),
 B("narr", "Captain Sydney Cornwell had no choice. Airplanes came to fly most of the crew away.", "close:cornwell", [["cornwell", "turn:front"]], "whoosh", "22 MEN FLOWN OUT"),
 B("narr", "Fifteen men stayed behind. They built a wooden hut on the shore.", "prop:hut", [["hut", "bounce"]], "crunch", "15 MEN STAYED"),
 B("sailor", "Every day we walk out and chip the ice off her. She won't escape us.", "close:sailor", [["sailor", "to:-1.6,9.6,0"], ["sailor", "happy"]], "pop", "EVERY DAY"),
 B("narr", "Then, late in November, a terrible blizzard came howling across the ice.", "wide", [["sailor", "to_home"], ["ship", "shake"], ["hut", "shake"]], "rumble", "THE BLIZZARD"),
 B("narr", "For days, the men could not even step outside their hut.", "prop:hut", [["hut", "shake"], ["fire", "spin"]], "suspicious", "SNOWED IN"),
 B("narr", "When the storm ended, they looked out. The ship was not there.", "prop:ship", [["ship", "hide"]], "alarm", "SHE WAS GONE"),
 B("cornwell", "She must have broken up and sunk. There's nothing left to find.", "close:cornwell", [["cornwell", "shake"]], "dun", "SUNK?"),
 B("narr", "But a few days later, a seal hunter came to the hut with strange news.", "close:hunter", [["hunter", "to:-1.4,9.4,0"], ["hunter", "turn:front"]], "whoosh", "STRANGE NEWS"),
 B("hunter", "I saw your ship. Forty-five miles from here. Sailing in the ice, with no one aboard.", "close:hunter", [["hunter", "eyes_big"], ["ghost", "show"]], "alarm", "45 MILES AWAY"),
 B("narr", "The men hurried there. It was true. The Baychimo was afloat, all alone.", "prop:ghost", [["ghost", "bounce"], ["hunter", "to_home"]], "rumble", "ALL ALONE"),
 B("narr", "They took the furs from her hold. Then they left her for the last time.", "prop:furs", [["furs", "show"], ["furs", "bounce"]], "crunch", "LEFT FOR GOOD"),
 B("narr", "The company gave her up as lost. But the Baychimo did not stay lost.", "prop:ghost", [["furs", "hide"], ["ghost", "shake"]], "dun", "SHE CAME BACK"),
 B("narr", "Months later, she was seen three hundred miles to the east. Still drifting. Still empty.", "wide", [["ghost", "bounce"], ["moon", "bounce"]], "whoosh", "300 MILES EAST"),
 B("narr", "In March nineteen thirty-three, a group of Inupiat hunters climbed aboard.", "close:hunter", [["hunter", "to:-1.6,9.8,0"], ["hunter", "turn:front"]], "horn", "MARCH 1933"),
 B("hunter", "Then the storm came. We could not leave. We waited ten days inside her.", "close:hunter", [["hunter", "shake"], ["ghost", "shake"]], "rumble", "TRAPPED 10 DAYS"),
 B("narr", "Ten days, aboard a ship that steers herself. Would YOU climb aboard?", "prop:ghost", [["lamp", "show"], ["lamp", "bounce"], ["hunter", "to_home"]], "suspicious", "WOULD YOU CLIMB ABOARD?"),
 B("narr", "That summer, more visitors boarded her. The next day, she had drifted away again.", "prop:ghost", [["lamp", "hide"], ["ghost", "bounce"]], "whoosh", "GONE AGAIN"),
 B("narr", "In November nineteen thirty-nine, Captain Hugh Polson tried to bring her home.", "close:polson", [["polson", "to:-1.5,9.4,0"], ["polson", "turn:front"]], "horn", "NOVEMBER 1939"),
 B("polson", "She's still sound! Tie a line to her. We'll tow her out of here!", "close:polson", [["polson", "happy"], ["polson", "jump"]], "pop", "TOW HER HOME!"),
 B("narr", "But the ice closed in around them. Polson had to let her go.", "prop:ghost", [["ghost", "shake"], ["polson", "to_home"]], "rumble", "THE ICE CLOSED IN"),
 B("narr", "That was the last time anyone set foot on the Baychimo.", "wide", [["ghost", "bounce"]], "dun", "THE LAST BOARDING"),
 B("narr", "Year after year, people saw her. In March nineteen sixty-two, Inuit hunters saw her drifting.", "prop:ghost", [["moon", "bounce"]], "whoosh", "STILL SEEN IN 1962"),
 B("narr", "And in nineteen sixty-nine, she was seen again, frozen in the ice. Thirty-eight years alone.", "prop:ghost", [["ghost", "shake"]], "alarm", "38 YEARS ALONE"),
 B("narr", "Then, nothing. No wreck has ever been found.", "wide", [["ghost", "hide"]], "dun", "NO WRECK FOUND"),
 B("narr", "In two thousand six, Alaska began searching for her. She has never been found.", "prop:paper", [["paper", "show"], ["paper", "spin"]], "suspicious", "NEVER FOUND"),
 B("narr", "Most experts think she sank at last. But no one has ever seen her sink.", "wide", [["paper", "hide"], ["moon", "bounce"]], "rumble", "DID SHE SINK?"),
 B("narr", "So remember the rule of the Arctic. If an empty ship comes back, never go aboard.", "prop:hut", [["hut", "shake"]], "alarm", "NEVER GO ABOARD"),
 B("narr", "Tonight, a young sailor walks out across the same frozen sea.", "close:boy", [["boy", "to:-2,9,0"], ["boy", "turn:front"]], "rumble", "TONIGHT..."),
 B("boy", "A ship! Out here, in the ice? And a lamp is burning on her deck!", "prop:ghost", [["ghost", "show"], ["lamp", "show"], ["boy", "eyes_big"]], "suspicious", "A LAMP ON DECK"),
 B("narr", "Nobody should be aboard. But someone on deck lifts the lamp, and waves him closer.", "close:boy", [["lamp", "bounce"], ["boy", "shake"]], "alarm", "SOMEONE WAVES"),
 B("narr", "What do you think happens in the next part? Tell me in the comments.", "prop:ghost", [["ghost", "shake"]], "dun", "WHAT HAPPENS NEXT?"),
]
sc = {"title": "This Ship Sailed Alone for 38 Years. Why?",
      "description": "A true story from the Arctic: the ghost ship Baychimo, Alaska, 1931-1969. What do you think happens in the next part? Tell me in the comments.",
      "lead_in": 0.0, "set": {"place": "tundra", "fog": 0.035, "eyes": 0, "moonlight": 5}, "chars": chars, "props": props, "beats": beats}
for b in beats:
    assert len(b["say"].split()) <= 18, b["say"]
json.dump(sc, open(os.path.join(H, "ep045.json"), "w"), indent=1, ensure_ascii=False)
print("beats", len(beats))

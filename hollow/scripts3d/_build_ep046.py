"""Build scripts3d/ep046.json - the moving coffins of the Chase Vault, Christ Church, Oistins, Barbados
(burials 1807-1819, last opening April 1820; first printed by J. E. Alexander, Transatlantic Sketches, 1833).
Standalone recorded legend. python3 scripts3d/_build_ep046.py"""
import json
H = lambda name, voice, sp, pi, col, home, size=0.85, kind="human", **kw: dict(name=name, voice=voice, speed=sp, pitch=pi, color=col, kind=kind, size=size, home=home, **kw)
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.95, "pitch": -1},
 "worker": H("A workman", "am_michael", 1.02, 0, [0.42, 0.28, 0.16], [-3.6, 7.6], 0.86),
 "comber": H("Lord Combermere", "bm_lewis", 0.96, -1, [0.45, 0.08, 0.08], [-30, 32], 0.9),
 "lucas": H("Nathan Lucas", "bm_daniel", 0.97, -1, [0.15, 0.17, 0.22], [-34, 34], 0.88),
 "boy": H("A boy", "am_puck", 1.05, 1, [0.25, 0.32, 0.45], [-38, 40], 0.66),
}
P = lambda t, i, col, sc, at, vis=True, glow=0: dict(type=t, id=i, color=col, glow=glow, visible=vis, scale=sc, at=at)
WOOD, LEAD = [0.2, 0.13, 0.08], [0.24, 0.25, 0.27]
props = [
 P("box", "vault", [0.22, 0.21, 0.2], 2.2, [6.4, 16.0, 0]),
 P("box", "door", [0.32, 0.31, 0.29], 1.1, [5.8, 13.2, 0]),
 # neat row of coffins (c*) and the same coffins thrown about (s*)
 P("box", "c1", WOOD, 0.6, [0.4, 11.6, 0], False), P("box", "c2", WOOD, 0.5, [1.4, 11.6, 0], False),
 P("box", "c3", WOOD, 0.5, [2.4, 11.6, 0], False), P("box", "c4", LEAD, 0.75, [3.6, 11.6, 0], False),
 P("box", "s1", WOOD, 0.6, [0.0, 10.6, 0.9], False), P("box", "s2", WOOD, 0.5, [2.9, 12.6, 1.1], False),
 P("box", "s3", WOOD, 0.5, [1.6, 10.2, 0], False), P("box", "s4", LEAD, 0.75, [4.4, 10.8, 0.7], False),
 P("box", "sand", [0.85, 0.78, 0.6], 0.45, [1.8, 9.6, 0], False, 1),
 P("ball", "seal", [0.75, 0.08, 0.06], 0.22, [-0.6, 11.8, 1.2], False, 3),
 P("cone", "lamp", [1.0, 0.8, 0.4], 0.3, [-2.4, 9.0, 1.2], True, 5),
 P("box", "paper", [0.85, 0.83, 0.75], 0.5, [0.8, 9.4, 1.3], False, 1),
 P("ball", "moon", [0.8, 0.85, 1.0], 1.6, [10, 40, 14], True, 4),
]
NEAT = [["c1", "show"], ["c2", "show"], ["c3", "show"], ["c4", "show"], ["s1", "hide"], ["s2", "hide"], ["s3", "hide"], ["s4", "hide"]]
MESS = [["c1", "hide"], ["c2", "hide"], ["c3", "hide"], ["c4", "hide"], ["s1", "show"], ["s2", "show"], ["s3", "show"], ["s4", "show"]]
B = []
def b(who, say, cam, do, sfx, text): B.append(dict(who=who, say=say, cam=cam, do=do, sfx=sfx, text=text))
# 0-5 s: frame 1 = the thrown-about coffins + shaking vault + big text; narration mid-tension
b("narr", "The vault was sealed shut. Nobody went in. So who moved the coffins?", "prop:s4", MESS + [["s4", "shake"], ["vault", "shake"]], "alarm", "WHO MOVED THE COFFINS?")
b("worker", "Sir! The coffins! They're thrown all over the vault!", "close:worker", [["worker", "eyes_big"], ["s1", "spin"]], "rumble", "THROWN ALL OVER")
b("narr", "This story was first printed in eighteen thirty-three. Barbados, in the Caribbean.", "wide", [["s2", "bounce"], ["moon", "bounce"]], "horn", "BARBADOS")
b("narr", "Subscribe so you don't miss the next true story.", "prop:lamp", [["lamp", "bounce"]], "pop", "SUBSCRIBE")
b("narr", "In the churchyard of Christ Church, near Oistins, stood a stone family vault.", "prop:vault", [["vault", "bounce"]] + [[x, "hide"] for x in ("s1", "s2", "s3", "s4")], "whoosh", "A STONE VAULT")
b("narr", "Half under the ground, it was closed by a huge slab of stone.", "prop:door", [["door", "bounce"]], "crunch", "A GIANT STONE DOOR")
b("narr", "In eighteen-oh-seven, a woman named Thomasina Goddard was laid to rest inside.", "prop:c2", [["c1", "show"], ["c1", "bounce"]], "dun", "1807")
b("narr", "Then two young girls of the Chase family. Mary Ann, and later her sister Dorcas.", "prop:c4", [["c2", "show"], ["c3", "show"], ["c3", "bounce"]], "dun", "THE CHASE FAMILY")
b("narr", "In late eighteen twelve, the vault was opened for their father, Thomas Chase.", "wide", [["door", "shake"]], "horn", "LATE 1812")
b("worker", "Heave! Push the slab! Bring the lamp in here!", "close:worker", [["worker", "turn:front"], ["door", "shake"]], "crunch", "OPEN THE VAULT")
b("narr", "The men raised their lamps, and froze. Something was very wrong.", "close:worker", [["worker", "eyes_big"], ["lamp", "bounce"]], "suspicious", "SOMETHING WAS WRONG")
b("narr", "The coffins had left their places. One stood on its end. One lay upside down.", "prop:s2", MESS + [["s2", "spin"]], "alarm", "THEY HAD MOVED")
b("worker", "Who did this? The door was shut tight! Nobody could get in!", "close:worker", [["worker", "shake"]], "rumble", "NOBODY COULD GET IN")
b("narr", "Nothing was stolen. So the men set the coffins back in a row, and sealed the door.", "prop:c2", NEAT + [["worker", "to_home"]], "dun", "PUT BACK IN A ROW")
b("narr", "The story says Thomas Chase's coffin was lined with lead. It took eight men to lift.", "prop:c4", [["c4", "bounce"]], "crunch", "8 MEN TO LIFT IT")
b("narr", "In eighteen sixteen, the vault was opened for a baby boy. Again, the coffins had moved.", "prop:s4", MESS + [["s4", "shake"]], "alarm", "1816: MOVED AGAIN")
b("narr", "Weeks later it was opened once more. Again, everything was thrown about.", "wide", [["s1", "spin"], ["vault", "shake"]], "whoosh", "AND AGAIN")
b("worker", "I'm not going in there again. Not for any money!", "close:worker", NEAT + [["worker", "shake"], ["worker", "turn:front"]], "rumble", "NOT AGAIN")
b("narr", "In eighteen nineteen, it was opened for Thomasina Clarke. The coffins had moved again.", "prop:s3", MESS + [["s3", "spin"]], "alarm", "1819")
b("narr", "Then the governor of Barbados came himself. Lord Combermere wanted the truth.", "close:comber", [["comber", "to:-3.4,7.8,0"], ["comber", "turn:front"]], "horn", "THE GOVERNOR CAME")
b("comber", "Tap every wall. Search the floor. There must be a secret way in.", "close:comber", [["comber", "shake"], ["vault", "bounce"]], "suspicious", "A SECRET WAY IN?")
b("narr", "They found no tunnel. No crack. No hidden door. The walls were solid stone.", "prop:vault", NEAT + [["vault", "bounce"]], "dun", "NO WAY IN")
b("comber", "Spread fine sand on the floor. Any footprint will show.", "close:comber", [["sand", "show"], ["sand", "bounce"]], "whoosh", "SAND ON THE FLOOR")
b("narr", "Then they cemented the door shut, and pressed their own seals into the wet cement.", "prop:seal", [["seal", "show"], ["seal", "bounce"]], "crunch", "SEALED SHUT")
b("comber", "Now nobody goes in, and nobody comes out. We shall see.", "close:comber", [["comber", "turn:front"]], "dun", "WE SHALL SEE")
b("narr", "Months passed. In April eighteen twenty, the governor ordered the vault opened.", "wide", [["comber", "to_home"], ["door", "shake"]], "horn", "APRIL 1820")
b("narr", "The seals were not broken. The cement had not been touched.", "prop:seal", [["seal", "bounce"]], "suspicious", "SEALS NOT BROKEN")
b("worker", "Look at the sand! There's not one footprint! Not one!", "close:worker", [["worker", "turn:front"], ["worker", "eyes_big"], ["sand", "bounce"]], "alarm", "NO FOOTPRINTS")
b("narr", "But the heavy coffins had been thrown about the vault, once again.", "prop:s4", MESS + [["s4", "shake"], ["s2", "spin"]], "alarm", "THROWN ABOUT AGAIN")
b("lucas", "I was there. I saw it with my own eyes. Nobody could have done it.", "close:lucas", [["lucas", "to:-3.4,7.8,0"], ["lucas", "turn:front"], ["worker", "to_home"]], "dun", "I SAW IT")
b("narr", "Would YOU spend one night alone inside the Chase vault?", "prop:vault", [["lamp", "bounce"], ["lucas", "to_home"]], "suspicious", "WOULD YOU GO IN?")
b("narr", "The coffins were taken out and buried apart. The vault was left empty.", "prop:vault", [[x, "hide"] for x in ("s1", "s2", "s3", "s4", "sand", "seal")], "dun", "LEFT EMPTY")
b("narr", "But here is the strangest part.", "wide", [["moon", "bounce"]], "suspicious", "THE STRANGEST PART")
b("narr", "No newspaper of the time wrote about moving coffins. The first account came years later.", "prop:paper", [["paper", "show"], ["paper", "spin"]], "whoosh", "NO REPORT AT THE TIME")
b("narr", "Some say flood water moved them. Some say it never happened. Nobody knows.", "wide", [["paper", "hide"], ["vault", "bounce"]], "dun", "NOBODY KNOWS")
b("narr", "The empty vault is still there today, in the churchyard near the sea.", "prop:vault", [["door", "bounce"]], "rumble", "STILL THERE TODAY")
b("narr", "So remember the rule of the Chase vault. If the coffins move, never go inside.", "prop:door", [["door", "shake"]], "alarm", "NEVER GO INSIDE")
b("narr", "Tonight, a boy sneaks into the churchyard to see the old vault for himself.", "close:boy", [["boy", "to:-3.4,7.8,0"], ["boy", "turn:front"]], "rumble", "TONIGHT...")
b("boy", "Ha. It's just an empty room. There's nothing in here at all.", "close:boy", [["boy", "happy"], ["lamp", "bounce"]], "pop", "JUST AN EMPTY ROOM")
b("narr", "Then, behind him, the heavy stone door begins to slide shut.", "prop:door", [["door", "shake"], ["vault", "shake"]], "rumble", "THE DOOR IS CLOSING")
b("narr", "And from the dark corner comes a slow scrape. Something heavy is moving.", "close:boy", [["boy", "eyes_big"], ["s4", "show"], ["s4", "shake"]], "alarm", "SOMETHING IS MOVING")
b("narr", "What do you think happens next? Tell me in the comments.", "prop:s4", [["boy", "shake"], ["s4", "spin"]], "dun", "WHAT HAPPENS NEXT?")
sc = dict(title="Who Moved the Coffins in the Sealed Vault?",
          description="A recorded legend from Barbados: the moving coffins of the Chase Vault, Christ Church, 1812-1820. What do you think happens next? Tell me in the comments.",
          lead_in=0.0, set={"place": "graveyard", "fog": 0.05, "eyes": 0, "moonlight": 16}, chars=chars, props=props, beats=B)
for x in B:
    assert len(x["say"].split()) <= 18, x["say"]
json.dump(sc, open(__file__.replace("_build_ep046.py", "ep046.json"), "w"), indent=1)
print(len(B), "beats", sum(len(x["say"].split()) for x in B), "words", len(sc["title"]), "title chars")

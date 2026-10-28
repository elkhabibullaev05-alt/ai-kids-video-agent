"""Build scripts3d/ep040.json — the vanishing of Benjamin Bathurst, Perleberg, 25 Nov 1809."""
import json
H = lambda name, voice, sp, pi, col, home, size=0.85, kind="human": dict(name=name, voice=voice, speed=sp, pitch=pi, color=col, kind=kind, size=size, home=home)
chars = {
 "narr": {"name": "Narrator", "voice": "bm_george", "speed": 0.92, "pitch": -1},
 "bath": H("Benjamin Bathurst", "bm_daniel", 1.0, 0, [0.35, 0.36, 0.4], [-1.5, 9.4]),
 "krause": H("Krause, his courier", "am_michael", 1.0, 0, [0.3, 0.22, 0.14], [-4.0, 9.0]),
 "coach": H("The carriage", "am_michael", 1.0, 0, [0.08, 0.07, 0.1], [5.0, 13.0], 0.8, "coach"),
 "oldw": H("An old woman", "bf_emma", 0.95, -1, [0.4, 0.3, 0.32], [-11, 19], 0.8),
 "wife": H("Phillida, his wife", "bf_isabella", 0.95, 0, [0.5, 0.2, 0.3], [-9, 20], 0.8),
 "trav": H("A traveller", "af_sarah", 1.0, 0, [0.2, 0.4, 0.5], [11, 19], 0.8),
}
P = lambda t, i, col, sc, at, vis=True, glow=0: dict(type=t, id=i, color=col, glow=glow, visible=vis, scale=sc, at=at)
props = [
 P("box", "inn", [0.25, 0.18, 0.1], 2.4, [-4.5, 15, 0]),
 P("cone", "lamp", [1.0, 0.8, 0.45], 0.3, [-6.8, 14, 2.6], glow=4),
 P("box", "coat", [0.35, 0.25, 0.15], 0.55, [-7.5, 11.5, 0], False),
 P("box", "trousers", [0.55, 0.55, 0.58], 0.5, [-6.5, 17, 0], False, 1),
 P("box", "letter", [0.9, 0.88, 0.8], 0.4, [-3, 9, 1.4], False, 1),
 P("ball", "moon", [0.8, 0.85, 1.0], 1.6, [10, 40, 14], glow=4),
]
B = []
def b(who, say, cam, do, sfx, text): B.append(dict(who=who, say=say, cam=cam, do=do, sfx=sfx, text=text))
b("krause", "Sir? Mister Bathurst? Sir, where are you?", "close:coach", [["bath", "dive"], ["krause", "to:-1.5,9.2,0"], ["krause", "eyes_big"]], "alarm", "WHERE DID HE GO?")
b("narr", "He stepped out to the horses. Seconds later, he was gone. Forever.", "close:krause", [["krause", "shake"], ["lamp", "spin"]], "dun", "GONE IN SECONDS")
b("narr", "This is a true story. Perleberg, Prussia. November the twenty-fifth, eighteen-oh-nine.", "wide", [["moon", "bounce"], ["krause", "to_home"]], "horn", "PRUSSIA, 1809")
b("narr", "Hours earlier, a carriage rolled into this little town on the road from Berlin.", "close:coach", [["bath", "rise"], ["coach", "bounce"]], "whoosh", "HOURS EARLIER")
b("narr", "Inside sat Benjamin Bathurst. Twenty-five years old. A British diplomat.", "close:bath", [["bath", "turn:front"]], "chime", "A BRITISH ENVOY")
b("narr", "He was rushing home to England from Vienna, in the middle of Napoleon's wars.", "close:bath", [["bath", "turn:krause"]], "rumble", "NAPOLEON'S WARS")
b("bath", "Remember, Krause. Here I am Mister Koch, a simple merchant. Nobody must know.", "two:bath,krause", [["krause", "turn:bath"]], "suspicious", "A FALSE NAME")
b("krause", "Yes, sir. I will order fresh horses at the post house.", "close:krause", [["krause", "happy"]], "pop", "FRESH HORSES")
b("narr", "Bathurst was afraid. He believed enemy agents were following him.", "close:bath", [["bath", "eyes_big"]], "dun", "HE WAS AFRAID")
b("narr", "They waited at a little inn called the White Swan, by the old town gate.", "prop:inn", [["inn", "bounce"], ["lamp", "bounce"]], "chime", "THE WHITE SWAN")
b("bath", "Keep the candles burning, Krause. And keep watching the street.", "close:bath", [["bath", "turn:front"]], "suspicious", "WATCH THE STREET")
b("narr", "For hours he sat inside, writing letter after letter.", "prop:letter", [["letter", "show"], ["letter", "spin"]], "whoosh", "LETTER AFTER LETTER")
b("narr", "At nine o'clock the fresh horses were ready. The carriage waited in the dark.", "close:coach", [["letter", "hide"], ["coach", "bounce"]], "horn", "NINE O'CLOCK")
b("krause", "The carriage is ready, sir. I will bring the bags.", "close:krause", [["krause", "turn:coach"]], "pop", "THE CARRIAGE IS READY")
b("narr", "Bathurst stepped outside first. He walked toward the horses.", "two:bath,coach", [["bath", "to:2.8,9.6,0"]], "whoosh", "HE STEPPED OUTSIDE")
b("narr", "Krause followed just a few steps behind him. Only a few seconds.", "close:krause", [["krause", "to:-0.5,9.2,0"]], "suspicious", "A FEW SECONDS")
b("narr", "He walked around the front of the horses. And he never came back.", "close:coach", [["bath", "to:4.2,8.4,0"], ["bath", "dive"], ["lamp", "spin"]], "alarm", "HE NEVER CAME BACK")
b("krause", "Sir? Mister Bathurst? Sir!", "close:krause", [["krause", "eyes_big"], ["krause", "shake"]], "alarm", "SIR?!")
b("narr", "The horses stood still. The lanterns burned. But Benjamin Bathurst was gone.", "close:coach", [["coach", "shake"]], "dun", "GONE")
b("narr", "If you love true stories with no answer, subscribe now. It gets stranger.", "wide", [["moon", "bounce"]], "pop", "SUBSCRIBE")
b("narr", "Soldiers searched every street that night. They even dragged the river.", "wide", [["krause", "to:-6,15,0"], ["oldw", "to:-8,17,0"]], "rumble", "THEY DRAGGED THE RIVER")
b("narr", "The next day they searched the town, house after house.", "prop:inn", [["inn", "bounce"]], "whoosh", "HOUSE AFTER HOUSE")
b("narr", "In an outhouse behind one family's home, they found his expensive fur coat.", "prop:coat", [["coat", "show"], ["coat", "bounce"]], "crunch", "HIS COAT")
b("krause", "That is his coat! But where is he?", "close:krause", [["krause", "to:-6,12,0"], ["krause", "eyes_big"]], "alarm", "WHERE IS HE?")
b("narr", "Three weeks later, two old women went into the woods near Quitzow, gathering sticks.", "close:oldw", [["coat", "hide"], ["oldw", "to:-7,16,0"]], "chime", "3 WEEKS LATER")
b("oldw", "Look, by the path. Somebody's trousers, turned inside out.", "prop:trousers", [["trousers", "show"], ["oldw", "eyes_big"]], "suspicious", "INSIDE OUT")
b("narr", "They were Bathurst's grey trousers. Two bullet holes. But no blood at all.", "prop:trousers", [["trousers", "spin"]], "dun", "NO BLOOD")
b("narr", "In the pocket was a wet, half-finished letter to his wife.", "prop:letter", [["letter", "show"], ["letter", "bounce"]], "whoosh", "A LETTER")
b("narr", "He wrote that he feared he would never see England again.", "prop:letter", [["letter", "spin"]], "rumble", "NEVER SEE ENGLAND")
b("narr", "His young wife, Phillida, crossed war-torn Europe to search for him herself.", "close:wife", [["letter", "hide"], ["trousers", "hide"], ["wife", "to:-3,11,0"]], "horn", "HIS WIFE SEARCHED")
b("wife", "Benjamin! Somebody in this town must know where you are!", "close:wife", [["wife", "shake"]], "alarm", "SOMEBODY KNOWS")
b("narr", "She found rumours, and letters, and lies. She never found her husband.", "close:wife", [["wife", "sad"]], "dun", "NEVER FOUND")
b("narr", "Benjamin Bathurst was never seen again. Nobody knows what happened behind those horses.", "close:coach", [["wife", "to_home"], ["oldw", "to_home"], ["krause", "to_home"]], "suspicious", "NOBODY KNOWS")
b("narr", "So here is the rule of Perleberg. Never walk around the horses alone at night.", "close:coach", [["coach", "bounce"]], "dun", "NEVER WALK ALONE")
b("narr", "Many years later, a traveller waits by that same old gate. At nine o'clock.", "wide", [["trav", "to:1.5,9.4,0"], ["moon", "show"]], "chime", "YEARS LATER")
b("trav", "It's only an old story. I'll just check behind the carriage.", "close:trav", [["trav", "happy"]], "suspicious", "ONLY A STORY")
b("narr", "She steps around the horses. The lanterns flicker. Someone is breathing behind her.", "two:trav,coach", [["trav", "to:3.6,8.6,0"], ["lamp", "spin"]], "whoosh", "SOMEONE IS BREATHING")
b("trav", "Who's there? Mister... Bathurst?", "close:trav", [["trav", "eyes_big"], ["bath", "rise"], ["bath", "to:5.2,8.6,0"]], "alarm", "WHO'S THERE?")
b("narr", "A young man in a grey coat leans close and whispers: they are still watching.", "two:trav,bath", [["bath", "turn:trav"], ["trav", "shake"]], "rumble", "THEY'RE STILL WATCHING")
b("narr", "What do you think happens next? Tell me in the comments.", "two:trav,bath", [["bath", "shake"], ["trav", "turn:front"]], "horn", "WHAT HAPPENS NEXT?")
sc = dict(title="He Stepped Outside. Where Did He Go? (Ep 40)",
          description="A true story from Perleberg, Prussia, 1809: the vanishing of Benjamin Bathurst. What do you think happens next? Tell me in the comments.",
          lead_in=0.0, set={"place": "village", "fog": 0.025, "eyes": 0, "moonlight": 22}, chars=chars, props=props, beats=B)
json.dump(sc, open(__file__.replace("_build_ep040.py", "ep040.json"), "w"), indent=1)
print(len(B), "beats", len(sc["title"]), "title chars")

"""Hollowmere Tales EP 17 (3D) — the Brown Lady of Raynham Hall. Writes scripts3d/ep017.json.
Recorded legend + famous photograph (sources: en.wikipedia.org/wiki/Brown_Lady_of_Raynham_Hall, hoaxes.org/raynham.html):
Raynham Hall, Norfolk, England. Legend: Lady Dorothy Walpole (1686-1726), sister of Robert Walpole, second wife of
Charles Townshend, 2nd Viscount Townshend; the story says he kept her shut in her rooms; she died at Raynham of smallpox in 1726.
Christmas 1835: Colonel Loftus and a guest named Hawkins said they saw a lady in a brown dress on the way to bed; Loftus saw her
again the next night; some staff left. 1836: novelist Captain Frederick Marryat stayed in the haunted room; his daughter
Florence wrote (1891) that he met the figure in a corridor carrying a lamp and fired a pistol; the bullet went through her into a door.
1926: Lady Townshend said her son and his friend saw the ghost on the staircase and matched her to Dorothy's portrait.
19 September 1936: Country Life photographers Captain Hubert Provand and Indre Shira were photographing the hall. Shira saw a
veiled figure coming down the stairs and called out; the flash was fired. Published in Country Life (December 1936) and Life (1937).
Harry Price: "I could not shake their story". Sceptics: double exposure, grease on the lens, someone walking on the stairs.
Short 1 = the 1936 photo segment (beats 22-28); Short 2 = the Marryat "would YOU stay" segment (beats 13-18)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cast = json.load(open(os.path.join(HERE, "cast.json")))
chars = {k: cast[k] for k in ("odo", "moth", "narr")}
chars["odo"] = dict(chars["odo"], home=[-6, 6])
chars["moth"] = dict(chars["moth"], home=[-3.5, 5])
chars["lady"] = {"name": "The Brown Lady", "voice": "bf_emma", "speed": 0.8, "pitch": -3, "color": [0.42, 0.27, 0.14],
                 "kind": "lady", "ghost": True, "up": True, "size": 1.1, "home": [3, 12]}
chars["shira"] = {"name": "Shira", "voice": "bm_lewis", "speed": 1.05, "pitch": 0, "color": [0.25, 0.25, 0.3],
                  "kind": "human", "size": 1.0, "home": [-9, 10]}
chars["marryat"] = {"name": "Captain Marryat", "voice": "bm_daniel", "speed": 0.95, "pitch": -2, "color": [0.1, 0.15, 0.35],
                    "kind": "human", "size": 1.05, "home": [9, 9]}

N = "narr"
def L(who, say, cam, do=None, **kw):
    b = {"who": who, "say": say, "cam": cam}
    if do: b["do"] = do
    b.update(kw); return b

beats = [
    # 0 s: motion + big hook + voice at frame 1
    L(N, "Someone is walking down these stairs. And she has been dead for three hundred years.", "wide",
      [["lady", "to:1,9"], ["odo", "shake"], ["moth", "eyes_big"]], text="DON'T LOOK AT THE STAIRS"),
    L("moth", "Odo! Blow out the lantern. She can see the light!", "close:moth", [["moth", "shake"]], sfx="suspicious"),
    L(N, "The shapes in Loch Ness pulled them under. They woke up here, in a dark old house.", "two:odo,moth",
      [["lady", "dive"], ["odo", "turn:moth"]], text="WHERE ARE WE?"),
    L("odo", "This isn't the loch. These are stairs. Old, creaking stairs.", "close:odo", [["odo", "eyes_big"]], text="RAYNHAM HALL, ENGLAND"),
    L(N, "This is a true story, from real records. Raynham Hall stands in Norfolk, England.", "overhead", text="A TRUE STORY"),
    L(N, "For two hundred years, people say a lady in brown walks its halls.", "close:lady",
      [["lady", "rise"]], sfx="suspicious", text="THE BROWN LADY"),
    # ---- the legend ----
    L(N, "The legend says she is Lady Dorothy Walpole. She lived here three hundred years ago.", "two:lady,odo",
      [["odo", "turn:lady"]], text="LADY DOROTHY, 1726"),
    L(N, "The story says her husband had a terrible temper, and kept her shut inside her rooms.", "close:lady", [["lady", "sad"]], text="LOCKED IN HER ROOMS"),
    L(N, "She died in this house in 1726, of smallpox. But the legend says she never left.", "wide",
      [["lady", "dive"], ["moth", "eyes_big"]], text="SHE NEVER LEFT"),
    L("moth", "Never left? Then where is she now?", "close:moth", [["moth", "turn:front"]]),
    # ---- Christmas 1835 ----
    L(N, "Christmas, 1835. The house was full of guests. Two men were walking up to bed.", "two:odo,moth",
      [["odo", "to:-4,8"]], text="CHRISTMAS 1835"),
    L(N, "On the landing stood a lady in a rich brown dress. Watching them.", "close:lady", [["lady", "rise"]], sfx="suspicious", text="WATCHING THEM"),
    L(N, "The next night, one of the men saw her again. Some servants were so scared they left for good.", "wide",
      [["odo", "shake"], ["lady", "dive"]], text="THE SERVANTS FLED"),
    # ---- 1836 Marryat (Short 2 segment: beats 13-18) ----
    L(N, "Would YOU spend one night in the haunted room? In 1836, one famous writer said yes.", "close:marryat",
      [["marryat", "enter:right"]], text="WOULD YOU STAY?"),
    L("marryat", "Ghosts? Nonsense. I shall sleep in that room and prove it.", "close:marryat", [["marryat", "jump"]]),
    L(N, "His name was Captain Frederick Marryat, a sea captain and a writer of adventure books.", "two:marryat,odo",
      [["marryat", "turn:odo"]], text="CAPTAIN MARRYAT"),
    L(N, "His daughter wrote what happened. In a dark corridor, a lady came toward him, carrying a lamp.", "close:lady",
      [["lady", "rise"], ["lady", "to:5,9"]], sfx="suspicious", text="SHE CAME CLOSER"),
    L(N, "He fired his pistol. Bang! The bullet went straight through her, into the door behind.", "two:marryat,lady",
      [["marryat", "shake"], ["lady", "dive"]], sfx="alarm", text="STRAIGHT THROUGH HER"),
    L("moth", "Straight through? Would you stay one more night, Odo?", "close:moth", [["moth", "eyes_big"], ["marryat", "exit"]]),
    L("odo", "Not even one more minute.", "close:odo", [["odo", "shake"]]),
    # ---- 1926 ----
    L(N, "1926. Two boys on the staircase saw her too. Later they saw an old painting.", "prop:portrait",
      [["portrait", "show"], ["portrait", "spin"]], text="1926: TWO BOYS"),
    L(N, "It was Lady Dorothy's portrait. They said that was the face they had seen.", "prop:portrait",
      [["portrait", "bounce"]], sfx="suspicious", text="THAT WAS HER"),
    # ---- 1936 photograph (Short 1 segment: beats 22-28) ----
    L(N, "September 1936. Two photographers came to take pictures of the great staircase.", "close:shira",
      [["portrait", "vanish"], ["shira", "enter:left"]], text="SEPTEMBER 1936"),
    L(N, "One aimed the camera up the stairs. The other was standing right beside him.", "two:shira,odo",
      [["camera", "show"]], text="AIM AT THE STAIRS"),
    L("shira", "Quick! There's something coming down the stairs!", "close:shira", [["shira", "shake"]], sfx="suspicious"),
    L(N, "A pale shape in a veil. Gliding down. Step by step.", "close:lady",
      [["lady", "rise"], ["lady", "to:2,9"]], text="A SHAPE IN A VEIL"),
    L(N, "Flash! The picture was taken. But the photographer looking through the camera saw nothing at all.", "wide",
      [["camera", "spin"], ["lady", "dive"]], sfx="alarm", text="FLASH!"),
    L(N, "Then they printed the photo. And there she was. A ghostly lady on the stairs.", "prop:photo",
      [["camera", "vanish"], ["photo", "show"], ["photo", "bounce"]], text="SHE WAS IN THE PHOTO"),
    L("moth", "The camera saw her. The man didn't. Odo, what is she?", "close:moth", [["moth", "eyes_big"]]),
    # ---- what people think ----
    L(N, "That December, a famous magazine printed it. It became the most famous ghost photo in the world.", "prop:photo",
      [["photo", "spin"]], text="WORLD FAMOUS"),
    L(N, "A ghost hunter questioned both men. He said he could not shake their story.", "close:shira",
      [["shira", "turn:front"]], text="THEY STUCK TO IT"),
    L(N, "Others say it was a trick of the camera. Two pictures on top of each other.", "two:odo,moth",
      [["photo", "vanish"], ["odo", "turn:moth"]], text="A TRICK?"),
    L(N, "Or a smudge on the lens. Or a person walking down the stairs. Nobody has ever proved it.", "wide",
      [["shira", "exit"]], text="NOBODY KNOWS"),
    # ---- ending + cliffhanger ----
    L(N, "Then the lantern began to flicker. And a cold wind came down the staircase.", "overhead",
      [["moth", "shake"]], text="THE LANTERN FLICKERED"),
    L("lady", "You... should not be on my stairs.", "close:lady", [["lady", "rise"], ["lady", "to:-1,8"]], text="SHE SPOKE"),
    L("moth", "Odo... she isn't looking at us. She's looking behind us.", "close:moth", [["moth", "eyes_big"], ["all", "look:lady"]]),
    L(N, "What is standing behind Odo and Mothwick? Subscribe. The next tale begins on these stairs.", "wide",
      [["odo", "shake"], ["odo", "eyes_big"]], text="WHAT'S BEHIND THEM? SUBSCRIBE!"),
]

stairs = []
for i in range(5):
    for x in (6.4, 7.6):
        stairs.append({"id": f"st{i}{int(x)}", "type": "box", "color": [0.16, 0.1, 0.06], "at": [x, 13 + i * 1.2, -0.6 + i * 0.6], "scale": 1.0})

sc = {
    "title": "She Walked Down the Stairs. The Camera Saw.",
    "description": "Someone is walking down these stairs. And she has been dead for three hundred years.",
    "lead_in": 0.05,
    "set": {"place": "village", "fog": 0.05, "eyes": 3, "moonlight": 2.4},
    "chars": chars,
    "props": stairs + [
        {"id": "portrait", "type": "box", "color": [0.45, 0.3, 0.15], "at": [0, 9, 1.6], "visible": False, "scale": 0.9},
        {"id": "camera", "type": "box", "color": [0.05, 0.05, 0.05], "at": [-6, 8, 1.6], "visible": False, "scale": 0.6},
        {"id": "photo", "type": "box", "color": "white", "at": [0, 9, 1.6], "visible": False, "scale": 0.9},
    ],
    "beats": beats,
}
json.dump(sc, open(os.path.join(HERE, "ep017.json"), "w"), indent=1)
print("beats", len(beats), "max words", max(len(b["say"].split()) for b in beats), "words", sum(len(b["say"].split()) for b in beats))

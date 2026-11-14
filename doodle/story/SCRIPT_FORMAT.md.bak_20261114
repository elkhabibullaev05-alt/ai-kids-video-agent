# Doodle Desk script format (JSON)

One file = one long video (1920x1080). Render:
```bash
python3 engine/render.py scripts/ep002.json --check        # voices it, prints scenes/words/minutes
python3 engine/render.py scripts/ep002.json --preview 6    # stills of every 6th scene -> out/ep002/preview_*.png
python3 engine/render.py scripts/ep002.json                # full render (~3 min of CPU for 10 min of video, TTS ~1 s per word on 2 cores the first time)
```
Output in `out/<id>/`: `<id>.mp4`, `thumbnail.png` (1280x720), `subs_en.srt`, `upload.txt`.
Write scripts with a `scripts/_build_epNNN.py` (helpers G/P/T/sc — copy `_build_ep001.py`).

## Top level
`id` (ep002), `title` (≤ 60 chars, curiosity/question), `voice` ("am_michael"), `speed` (1.0), `description` (with a "Sources:" list of real URLs), `tags`, `thumbnail`, `scenes`.
`thumbnail`: `{"bg": "yellow", "text": "LINE ONE|LINE TWO", "size": 190, "guy": {"pose": "panic", "face": "scream", "look": -1, "extras": ["hair"]}, "guy_x": 1250, "items": [<prop item>]}` — 2–5 words, huge.

## Scene
`{"say": "one or two sentences (≤ 30 words)", "items": [...], "chapter": "Part 2: ...", "bg": "paper|yellow|sky|...", "cam": {"from": [cx, cy, zoom], "to": [cx, cy, zoom]}, "ground": true, "hold": 0.28}`
Every scene gets a new picture. A new item should appear every 2–4 seconds (`at`).

## Items (positions in 1920x1080; ground line y = 900–905)
| item | example |
|---|---|
| stick figure | `{"guy": {"pose": "shrug", "face": "worried", "look": 1, "extras": ["hair"], "label": "the UN", "walk": false}, "x": 600, "y": 900, "s": 1.0}` |
| prop | `{"prop": "gaspump", "x": 1200, "y": 900, "s": 1.2, "text": "$4.33", "color": "red"}` |
| text | `{"text": "$4.33", "x": 960, "y": 300, "size": 130, "color": "red", "outline": "white"}` |
| counter | `{"count": [2.98, 4.33], "fmt": "${:.2f}", "x": 960, "y": 330, "size": 180, "dur": 2.0}` |
| arrow | `{"arrow": [[700, 640], [1220, 640]], "color": "red"}` |
| bar chart | `{"bars": {"values": [3.4, 3.7], "labels": ["Aug", "Sep"], "colors": ["grey", "red"], "fmt": "{}%", "w": 700, "h": 420}, "x": 900, "y": 820}` |
| red X / ring / stamp / box | `{"cross": [x, y, r]}` · `{"ring": [x, y, r]}` · `{"stamp": "RECORD", "x": 1500, "y": 400, "size": 80, "w": 260}` · `{"box": [x, y, w, h], "color": "white"}` |
Common keys: `at` (0–1 = fraction of the scene, >1 = seconds), `until`, `in` (`pop` default, `slide_l`, `slide_r`, `drop`, `none`), `anim` (`bob`, `shake`, `pulse`, `spin`), `move` ([x, y] glide during the scene).

Poses: stand, point, pointup, shrug, panic, think, hold, wave, cry, facepalm, present, fist, hips, type, run.
Faces: happy, grin, sad, worried, shock, angry, neutral, smug, confused, tired, cry, scream.
Extras: hair, bun, tie, glasses, tophat, cap, hardhat, crown, briefcase, sweat. Shirt colour: `"shirt": "blue"`.
Props: gaspump car truck ship barrel dollar wallet cart plane building chart thermo globe house coffee bread fire sun cloud desk tv strait calendar ballot moneybag scale arrowup arrowdown pricetag egg podium speech bomb capitol.
Colours: red orange yellow green teal blue navy purple pink brown tan grey dark white black gold sky sea money.
Need a new prop? Add a small function to `engine/ink.py` (`PROPS`), keep it simple shapes + `p.text`.

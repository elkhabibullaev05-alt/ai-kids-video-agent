# Inspector Bolt — episode script format (`scripts/epNNN.json`)

One JSON file drives everything: voices (`engine/voices.py`), 3D animation (`engine/story.py`), sound (`engine/soundtrack.py`), subtitles (`engine/subs.py`). Look at `scripts/ep001.json` as the reference.

```json
{
 "title": "YouTube title (≤ 70 chars)",
 "description": "2–3 sentences for YouTube",
 "set":   {"press": true, "podium": true, "time": "day | sunset | night"},
 "chars": { "<id>": {"name","voice","speed","pitch","color":[r,g,b],"kind":"car|bus|truck|small","size","hat":bool,"home":[x,y]}, "narr": {"name":"Narrator","voice":"am_fenrir","speed":1.0,"pitch":0} },
 "props": [ {"id":"wheel","type":"wheel","color":"gold","on":"podium|<char id>|null","visible":true,"scale":1.0} ],
 "beats": [ {"who":"bolt","say":"…","cam":"close:bolt","do":[["turbo","jump"]]},
            {"sfx":"alarm","cam":"podium","hold":1.2,"text":"BIG TITLE CARD","do":[["wheel","vanish"]]} ]
}
```

## Cast (keep these; voices/colours are the brand)
| id | who | voice | kind | home |
|---|---|---|---|---|
| bolt | Inspector Bolt, calm British detective, brown hat | bm_george 0.95 | car | [6, 9] |
| bertha | Big Bertha, loud kind school bus | af_bella 1.05, pitch −1 | bus | [−9, 18] |
| turbo | Turbo, fast show-off red sports car | am_puck 1.2, pitch +1 | car 0.95 | [3, 12] |
| grumpy | Grumpy, grey tow truck, deadpan | am_onyx 0.9, pitch −2 | truck | [−1, 15.5] |
| pip | Pip, tiny pink car, brave | af_sky 1.05, pitch +4 | small 0.65 | [−15.5, 8] |
| narr | Narrator (off-screen) | am_fenrir 1.0 | — | — |
New guest characters are allowed (max 2 per episode): pick an unused Kokoro voice (am_eric, am_michael, af_nicole, af_sarah, bf_emma, bm_lewis…), a new colour, a free `home` (x −16…16, y 6…20, ≥ 4 apart from others).

## Beats
- A beat is either a line (`who` + `say`) or a silent card (`sfx` and/or `text`, `hold` seconds).
- `say`: short, spoken English for kids 4–9; ≤ 20 words per line; every main character speaks.
- `text`: big title card burned in (CAPS, ≤ 6 words). `sfx`: `alarm` | `suspicious`.
- `cam` (camera for this beat; consecutive beats with the same cam are one shot):
  `wide`, `press`, `podium`, `overhead`, `prop:<prop id>`, `two:<a>,<b>`, `close:<char>`.
  Change the camera at least every 2 beats (fast cuts = retention).
- `do`: list of `[target, action]`, all start when the beat starts.

### Character actions (`[<char id>|"all", action]`)
`enter` / `enter:left` (drives in to home), `exit`, `to_press`, `to_home`, `to:<char>` / `to:x,y`, `turn:<char>` / `turn:front`,
`jump`, `laugh`, `shake`, `spin`, `eyes_big` (lying!), `sad`, `happy`, `sleep`, `flat_roof`, `squash`, `hat_give:<char>` (only from a char with `"hat": true`).
`["all", "look:<char>"]` — everyone turns to look at one character. `["all", "laugh"]` etc. applies to everyone.
### Prop actions (`[<prop id>, action]`)
`show`/`appear`, `hide`/`vanish`, `spin`, `bounce`, `drop:<char>` (falls out of that char), `give:<char>`/`to:<char>`, `home`.
Prop types: wheel, ball, banana, cone, star, trophy, cake, key, box, gift. Colours: gold, red, blue, green, … or [r,g,b].
### The Truth Press (`["press", …]`) and effects
`rise`, `sink`, `clap`, `squeeze:<char>` (squeezes whoever is at the press — send them there with `to_press` first).
`["fx", "tracks:<from>-<to>"]` — clue tracks on the ground between two characters (or a char and the podium area).

## Checks before rendering
`python3 engine/voices.py …` prints the total length — a long episode must be **4:00–5:00** (rek-ball gives full length points only from 4:00), a Short source beat 20–45 s.
Render 5 test frames with `--frames` and look at them (nobody blocking the camera, the prop visible, faces in frame).

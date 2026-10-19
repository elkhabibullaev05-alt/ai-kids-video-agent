# 3D animation pipeline (owner's rule, 2026-10-19)

Since 2026-10-19 **Dough Bros, Hollowmere Tales and Max the Curious Cat** are made in 3D, like Inspector Bolt.
Each channel has its own `engine3d/` (Blender 4.2 EEVEE, same engine as `bolt/engine`, only `world.py` differs: the set, the lights and the character shapes).

| channel | folder | world places (`set.place`) | character kinds |
|---|---|---|---|
| Dough Bros | `doughbros/engine3d` | kitchen, freezer, pantry, table, garden | loaf, bean, triangle, star, rock, pot, toaster, kettle, jelly, ghost |
| Hollowmere | `hollow/engine3d` | forest, clearing, graveyard, swamp, village, chapel (+ `fog`, `eyes`, `moonlight`) | odo, moth, gloamhound, rootwraith, shepherd, crow, wickeater, hollowmother, human |
| Max | `maxcat/engine3d` | garden, park, house, beach, snow (+ `time` day/sunset) | cat, mouse, dog, bird, grandma |

Ready casts (copy into every script's `chars`): `<channel>/scripts3d/cast.json`.

## Daily target per channel: 3 long + 4 Shorts
Each run makes **one long (3:00–3:40)** and cuts **1–2 Shorts** from it (first pack of the UTC day: 2 Shorts, the others: 1; plus the 4th Short from the best moment of the day's 2nd long). Three runs per day per channel, in parallel sessions. Render budget: ~4.7 s/frame at 854 px, 12 fps → a 3:20 long ≈ 2.6 h. Never make a long longer than 3:40.

## Steps (in the channel folder)
```bash
bash ../bolt/setup.sh                                   # Blender 4.2.3 + Kokoro (once per container)
python3 engine3d/voices.py scripts3d/epNNN.json out3d/epNNN 12      # TOTAL must be 180–220 s
BL=/opt/bl/blender-4.2.3-linux-x64/blender
$BL -b --factory-startup -P engine3d/story.py -- --tl out3d/epNNN/timeline.json --out out3d/epNNN/frames --res 854 --samples 2 --frames 30,600,1200,1800,2300   # look at them
setsid nohup $BL -b --factory-startup -P engine3d/story.py -- --tl out3d/epNNN/timeline.json --out out3d/epNNN/frames --res 854 --samples 2 > /tmp/r.log 2>&1 &   # resumable
python3 engine3d/soundtrack.py out3d/epNNN && bash engine3d/assemble_long.sh out3d/epNNN out3d/epNNN.mp4
python3 engine3d/thumb.py out3d/epNNN/frames/f_XXXX.png out3d/epNNN_thumb.jpg "2-4 WORDS"
python3 ../tools/make_short.py out3d/epNNN.mp4 out3d/epNNN_s1.mp4 --start S --dur 20-35 --top "HOOK" --bottom "Full episode on the channel"
```
Script format = `bolt/story/SCRIPT_FORMAT.md` (same beats, cameras and actions; there is no Truth Press outside Bolt, so don't use `press`/`to_press`). Use `set` = `{"place": ..., ...}` from the table. Every channel keeps its own story bible, tone, titles, Made-for-kids setting, upload flow and release slots — only the renderer changed.
Then: rek-ball gate (≥ 85), upload (channel's UPLOAD.md), translations (`tools/TRANSLATE.md`), log, hub update.

## Ready stories (2026-10-19)
Before writing a new script, look in `cloud/queue/<channel>/` (bolt, doughbros, hollow, maxcat). If a job file is there, use the oldest one: its `script` is the episode script, `long` has the title/description/tags/thumb text and the 7-language `localizations`, `shorts` has the Short cut points (`beat` index) and texts. Then `git mv` it to `cloud/done/<channel>/` in your final commit. Still check it differs from the last 10 episodes; if not, write a new one.

# Dough Bros script format (JSON)

One file = one video. Render with:

```bash
python3 engine/render.py scripts/ep002_long.json --check      # validate + time it, no video
python3 engine/render.py scripts/ep002_long.json --preview 5 20 # still frames only
python3 engine/render.py scripts/ep002_long.json                # full render -> out/<id>/
```

Output in `out/<id>/`: `<id>.mp4` (English voices, Spanish subtitles burned in), `subs_es|de|fr|it|pt.srt`, `thumbnail.png` (1280x720), `upload.txt` (title, description, tags).

## Top level

| key | required | meaning |
|---|---|---|
| `id` | yes | `ep002_long`, `ep002_short1` ... (also the output file name) |
| `format` | yes | `"long"` (16:9, 1920x1080) or `"short"` (9:16, 1080x1920) |
| `title` | yes | YouTube title. Long: `Dough Bros vs THE TOASTER 😱 \| Animation EP 2`. Short: end with `#shorts` |
| `hook` | shorts | Big text on top of the Short for the whole video (max ~28 chars) |
| `description`, `tags` | yes | English. Include `#shorts` in shorts description |
| `thumbnail` | yes | `{"bg": "...", "villain": "...", "heroes": ["bup","pim"], "text": "MAX 3 WORDS!"}` |
| `scenes` | yes | list of scenes (below) |
| `end_card` | no | long only. `{"en": "TO BE CONTINUED...", "es": "CONTINUARÁ..."}` (default) or `false` |

## Scene

```json
{
  "bg": "kitchen | freezer | pantry | oven | table | bathroom | garden | attic | fridge | lunchbox",
  "music": "drone | heartbeat | music_box | none",
  "heroes": {"bup": 700, "pim": -300},          // starting x. Stage is 0..1920. <0 or >1920 = off screen
  "moods": {"pim": "scared"},                     // optional start mood: normal|scared|happy|angry
  "villain": {"type": "pot | frost | toaster | mixer | vacuum | jelly | kettle | scarecrow", "x": 1450, "state": "asleep | awake | hidden", "scale": 0.8},
  "beats": [ ... ],
  "tail": 0.6                                     // seconds to hold after the last beat
}
```

Good x positions: heroes 250–1000, villain 1300–1550. Keep heroes ≥ 200 px apart.
Only characters listed in `heroes` (and the scene `villain`) may be used in that scene's beats.

## Beats (run one after another; add `"and": true` to start a beat at the same time as the previous one)

| beat | example | notes |
|---|---|---|
| say | `{"say": "bup", "en": "Did you hear that?", "es": "...", "de": "...", "fr": "...", "it": "...", "pt": "..."}` | speaker: hero id, `"villain"`, or `"narr"` (narrator). **All 5 translations required.** Keep lines short (≤ 14 words) |
| move | `{"move": "pim", "to": 900, "speed": "walk"}` | `to`: number, `"off_left"`, `"off_right"`. `speed`: walk/run. Also works for `"villain"` |
| act | `{"act": ["bup","pim"], "do": "scream"}` | do: `jump`, `shake`, `scream` (auto voice), `faint`, `spin`, `bounce`, `hide`, `show` |
| mood | `{"mood": ["bup","zeek"], "is": "scared"}` | normal / scared / happy / angry. Instant |
| villain | `{"villain": "wake"}` | `wake`, `sleep`, `roar`, `lunge` (+`"to": x`), `rage` (+`"level": 0..1`), `show`, `hide` |
| sfx | `{"sfx": "thump", "wait": 0.6}` | thump, clank, rattle, whoosh, roar, boing, pop, creak, ice, ding, sting, step |
| wait | `{"wait": 1.0}` | pause |
| shake | `{"shake": 0.8, "power": 20}` | camera shake |
| card | `{"card": "MEANWHILE...", "es": "MIENTRAS TANTO...", "dur": 2.5}` | full-screen black title card |

Automatic: footsteps on move, boing on jump, roar sound + shake on roar, lip-sync, characters look at whoever speaks, scared heroes look at the villain.

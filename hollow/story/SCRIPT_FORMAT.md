# Hollowmere script format (JSON)

One file = one video. Render:
```bash
python3 engine/render.py scripts/ep001_long.json --check          # validate + duration, no video
python3 engine/render.py scripts/ep001_long.json --preview 5 30    # still frames only (out/<id>/preview_*.png)
python3 engine/render.py scripts/ep001_long.json                   # full render (~1 s of CPU per frame; 4 min ≈ 45 min on 2 cores)
```
Output in `out/<id>/`: `<id>.mp4` (English voices + English subtitles burned in), `subs_en/es/de/fr/it/pt.srt`, `thumbnail.png`, `upload.txt`.

## Top level
| key | meaning |
|---|---|
| `id` | `ep001_long`, `ep001_short1` … |
| `format` | `"long"` (1920x1080) or `"short"` (1080x1920) |
| `title` | YouTube title. Shorts end with `#shorts` |
| `hook` | shorts only: big gothic text at the top for the whole Short (≤ 28 chars) |
| `description`, `tags` | English |
| `thumbnail` | `{"bg": "forest", "seed": 2, "creature": "gloamhound", "text": "DON'T LOOK"}` |
| `shots` | list of shots (below) |

## Shot
```json
{
  "bg": "forest | clearing | swamp | graveyard | chapel | mill | village | cave",
  "seed": 3,                          // background variation (same seed = same trees)
  "music": "drone | heartbeat | lullaby | choir | none",
  "wind": true,
  "ambient": 0.42,                    // darkness: 0.3 very dark … 0.6 brighter
  "eyes": 8,                          // pairs of red eyes in the dark (0 = none)
  "lantern": 1.0,                     // starting lantern level (0 = out)
  "lights": [{"kind": "fire", "x": 960, "y": 900, "r": 600}],   // fire | moon | window
  "cam": {"from": [960, 600, 1.12], "to": [1000, 620, 1.2]},     // centre x, centre y, zoom (1.0–1.25); long only
  "focus": "odo",                     // shorts: who the vertical camera follows when nobody talks
  "chars": {"odo": {"x": 600, "face": 1}, "moth": {"x": 760, "y": 640}},
  "creatures": {"h1": {"type": "gloamhound", "x": 1500, "state": "hidden", "face": -1, "scale": 1.0}},
  "beats": [ ... ],
  "tail": 0.6
}
```
Ground is at y≈905. Good x: Odo 450–900, creatures 1250–1600 (x is the creature's feet/centre). `hollowmother` uses `y` ≈ 480–560 (body centre) and starts hanging high: use `act` `drop` to lower it.
Creature types: `gloamhound`, `rootwraith`, `crow` (add `"fly": 1` for flying; y ≈ 300–600), `hollowmother`, `wickeater`, `shepherd`.
Creature ids are your own names (`h1`, `wraith`, `pale`) — use them in beats and as speakers.

## Beats (one after another; `"and": true` = start together with the previous beat)
| beat | example | notes |
|---|---|---|
| say | `{"say": "narr", "en": "...", "es": "...", "de": "...", "fr": "...", "it": "...", "pt": "..."}` | speaker: `narr`, `odo`, `moth`, a creature id, or `grandma`/`stranger`. All 6 languages. ≤ 16 words |
| move | `{"move": "odo", "to": 900, "speed": "walk"}` | walk / run / creep; `"off_left"` / `"off_right"`; works for creatures too |
| show / hide | `{"show": "h1"}` / `{"hide": "h1", "dur": 0.5}` | creature fades in/out |
| growl | `{"growl": "h1"}` | jaw opens + growl sound |
| lunge | `{"lunge": "h1", "to": 1100}` | jump scare: fast move + boom + shake |
| act | `{"act": "odo", "do": "shake"}` | odo/moth: shake, scared, calm, jump, fall, hide, unhide, turn · creatures: reach, rise, drop (`"level": 0..1`) |
| light | `{"light": "dim"}` | lantern: on / dim / out / flare |
| eyes | `{"eyes": "open"}` / `{"eyes": "close"}` | the red eyes in the dark appear (with whispers) / vanish |
| flash | `{"flash": true}` | white flash + boom (jump scare) |
| sfx | `{"sfx": "howl", "wait": 1.0}` | howl, growl, whisper, bell, caw, snap, flutter, hit, creak, step, whoosh, thump, sting |
| wait | `{"wait": 1.2}` | pause |
| shake | `{"shake": 0.8, "power": 18}` | camera shake |
| card | `{"card": "NEVER ANSWER THE WOODS", "dur": 2.6}` | full-screen black title card with a bell |

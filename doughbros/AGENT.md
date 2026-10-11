# Daily Dough Bros run — instructions for Claude

Goal every day: **1 long episode (3–5 min) + 3 Shorts**, rendered as finished MP4s with thumbnails, subtitles and upload text, delivered to the user. Work fully unattended: never wait for answers; decide and note decisions in the final message.

The user speaks **Uzbek** — the final message to the user must be in Uzbek. Video content is in English.

## 1. Setup (≈2 min)
```bash
cd <repo>/doughbros
bash setup.sh            # installs python deps + downloads the TTS model from GitHub releases
```

## 2. Read
- `story/bible.md` — characters, villains, tone, rules (kid-safe, original only).
- `story/SCRIPT_FORMAT.md` — the JSON format.
- `story/log.json` — every published episode. Continue from the **last cliffhanger**.
- `story/themes.md` — pick today's theme; it must differ from the last 14 days, and the villain from yesterday's.
- Look at `scripts/ep001_long.json` and one short as style examples.

## 3. Write 4 scripts
Next episode number N = last `episode` in log.json + 1 (3 digits: `ep002`).
- `scripts/epNNN_long.json` — follow the long-episode structure in the bible. **Target 180–300 s.** Run `--check` and if shorter than 180 s add scenes/lines.
- `scripts/epNNN_short1.json` (teaser of today's episode), `epNNN_short2.json` (character moment), `epNNN_short3.json` (question/cliffhanger). 15–45 s each.
- Every `say` line needs `en` + `es`, `de`, `fr`, `it`, `pt`. Natural kid-friendly translations.
- Rotate backgrounds and villains vs. the last 2 episodes in the log.

## 4. Validate, then render
```bash
for f in scripts/epNNN_*.json; do python3 engine/render.py "$f" --check || echo FIX "$f"; done
python3 engine/render.py scripts/epNNN_long.json --preview 3 30 90   # look at the PNGs in out/epNNN_long/
for f in scripts/epNNN_*.json; do python3 engine/render.py "$f"; done   # ~4-5 min of render per minute of video
```
Fix any reported problems before the full render. Use generous command timeouts (long render can take 20+ min; run it in the background and poll the log if needed).

## 5. Check the results
For each MP4: `ffprobe` the duration; extract 3 frames (`ffmpeg -ss T -i file -frames:v 1 x.png`) and look at them: characters visible, subtitles readable, nothing cut off. Re-render if something is clearly broken.

## 6. Save progress
Append to `story/log.json` → `episodes`:
```json
{"episode": N, "date": "YYYY-MM-DD", "theme": "...", "title": "...", "villain": "...", "bg": ["..."], "summary": "2 sentences", "cliffhanger": "...", "shorts": ["title1", "title2", "title3"]}
```
Then commit the 4 scripts + log.json (NOT the out/ folder) and `git push`. If push fails, still continue and mention it.

## 7. Upload to YouTube
Follow `UPLOAD.md`: schedule all four videos on the Dough Bros channel through the Claude app's built-in browser on the user's computer. If the computer or browser can't be reached, skip this step and say so.

## 8. Deliver
Send with SendUserFile (status "proactive"): the 4 MP4s, the 4 thumbnail.png files, and the 4 upload.txt files. The .srt files for the long video too (subs_de/fr/it/pt/es).
Then a short Uzbek message:
- EP number and title; one-sentence story summary.
- Which videos were uploaded and their scheduled times (or, if upload failed, the suggested schedule: long → 01:00 (15:00 New York); Shorts → 19:00, 22:00, 04:00 (09:00, 12:00, 18:00 New York). From November to mid-March (US winter time) add +1 hour to the Bishkek times. Easiest: in YouTube Studio set the schedule time zone to New York.)
- Reminders: "Made for kids = Yes", upload .srt files in YouTube Studio → Subtitles.
- Any problems (failed push, re-renders).

## Never
- Never upload anywhere except scheduling the day's 4 videos on the Dough Bros channel (@DoughBrosTV) as described in UPLOAD.md. Never type passwords or change account settings.
- Never use real brands, existing characters, songs, games or memes.
- Never put gore, blood, weapons or real-world danger in scripts.

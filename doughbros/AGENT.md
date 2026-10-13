# Daily Dough Bros run — instructions for Claude

Goal every day: **1 long episode (3–5 min) + 3 Shorts**, rendered as finished MP4s with thumbnails, subtitles and upload text, delivered to the user. Work fully unattended: never wait for answers; decide and note decisions in the final message.

The user speaks **Uzbek** — the final message to the user must be in Uzbek. Video content is in English.

## 0. Buffer check FIRST (this task fires several times a day)
The task runs 4× a day (08:54, 13:54, 18:54, 22:54 Bishkek) so that it catches up whenever the user's laptop is on. Videos are **scheduled ahead on YouTube**, so they publish even when the laptop is off.
1. Read `story/log.json` (after `git pull`). Collect every `uploads[].publish_at` → the set of **New York dates** that already have videos scheduled ("covered days").
2. Target = the next **2 New York days after today** (NY time now = UTC−4, Nov–mid-March UTC−5). Today counts too only if its 09:00 NY slot is still ≥ 90 min away.
3. If all target days are covered → **stop right here**: no render, no files; reply with one Uzbek line ("Bufer to'la: videolar DD.MM gacha rejalashtirilgan.").
4. Otherwise make **one episode per uncovered day, at most 2 per run**, earliest day first. Each episode's 4 videos go to that day's slots (09:00, 12:00, 15:00 long, 18:00 NY). Use that day as the episode's `date` in log.json.
5a. If the last episodes have `pending_uploads` (e.g. YouTube's daily upload limit was hit), schedule those first (files on the `uploads` branch, or re-render from the saved script), move them into `uploads`, and remove `pending_uploads`. If Studio says "Загрузка недоступна… через 24 часа", stop uploading for this run — never do the phone verification it offers.
5. If the computer/browser can't be reached for uploading, still render and push the scripts + log (without `uploads`) — the next run will see the episode has no uploads and must re-render it from the saved script (`python3 engine/render.py scripts/epNNN_*.json`) and upload it, instead of writing a new episode.

## 1. Setup (≈2 min)
```bash
cd <repo>/doughbros
bash setup.sh            # installs python deps + downloads the TTS model from GitHub releases
```

## 2. Read
- `story/bible.md` — characters, villains, tone, rules (general audience 13+, family-friendly but not child-directed, original only).
- `story/SCRIPT_FORMAT.md` — the JSON format.
- `story/log.json` — every published episode. Continue from the **last cliffhanger**.
- `story/themes.md` — pick today's theme; it must differ from the last 14 days, and the villain from yesterday's.
- Look at `scripts/ep001_long.json` and one short as style examples.

## 3. Write 4 scripts
Next episode number N = last `episode` in log.json + 1 (3 digits: `ep002`).
- `scripts/epNNN_long.json` — follow the long-episode structure in the bible. **Target 180–300 s.** Run `--check` and if shorter than 180 s add scenes/lines.
- `scripts/epNNN_short1.json` (funny character moment — the main Short), `epNNN_short2.json` (viewer question/dare), `epNNN_short3.json` (teaser of today's episode). 15–45 s each. See `story/themes.md` → Shorts.
- Every `say` line needs `en` + `es`, `de`, `fr`, `it`, `pt`. Natural, simple translations.
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
{"episode": N, "date": "YYYY-MM-DD", "theme": "...", "title": "...", "villain": "...", "bg": ["..."], "summary": "2 sentences", "cliffhanger": "...", "shorts": ["title1", "title2", "title3"],
 "uploads": [{"title": "...", "publish_at": "2026-10-12T13:00:00Z"}]}
```
`uploads` = the videos actually scheduled on YouTube (UTC times); fill it in after step 7 and push again. The user's "Agentlar markazi" desktop app reads this file to show Dough Bros status.
Then commit the 4 scripts + log.json (NOT the out/ folder) and `git push`. If push fails, still continue and mention it.

## 7. Upload to YouTube
Follow `UPLOAD.md`: schedule all four videos on the Dough Bros channel through the Claude app's built-in browser on the user's computer. If the computer or browser can't be reached, skip this step and say so.

## 8. Deliver
Send with SendUserFile (status "proactive"): the 4 MP4s, the 4 thumbnail.png files, and the 4 upload.txt files. The .srt files for the long video too (subs_de/fr/it/pt/es).
Then a short Uzbek message:
- EP number and title; one-sentence story summary.
- Which videos were uploaded and their scheduled times (or, if upload failed, the suggested schedule: long → 01:00 (15:00 New York); Shorts → 19:00, 22:00, 04:00 (09:00, 12:00, 18:00 New York). From November to mid-March (US winter time) add +1 hour to the Bishkek times. Easiest: in YouTube Studio set the schedule time zone to New York.)
- Reminders: audience = "Not made for kids", upload .srt files in YouTube Studio → Subtitles.
- Any problems (failed push, re-renders).

## Never
- Never upload anywhere except scheduling the day's 4 videos on the Dough Bros channel (@DoughBrosTV) as described in UPLOAD.md. Never type passwords or change account settings.
- Never use real brands, existing characters, songs, games or memes.
- Never put gore, blood, weapons or real-world danger in scripts.

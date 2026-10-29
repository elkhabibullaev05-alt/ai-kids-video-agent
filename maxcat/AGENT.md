# Max the Curious Cat — 3D production run (instructions for Claude)

Since 2026-10-19 Max is made in **3D in the cloud** (the old 2D agent on the owner's computer only finishes its queued uploads). Target: **3 long (3:00–3:40) + 4 Shorts per UTC day**, one long per run. User speaks Uzbek (final message in Uzbek); videos are English. Read `story/bible.md`, `../tools/ANIM3D.md` and `../bolt/story/SCRIPT_FORMAT.md` first.

## 0. Buffer check
Same as `../bolt/AGENT.md` step 0 (lock in `story/log.json`, lock `until` = now + 5 h, computer check, pending uploads first). Count long uploads for today and tomorrow (UTC): both have 3 → stop.

## 1. Make
`bash ../bolt/setup.sh`. Write `scripts3d/epNNN.json` (Bolt format, `chars` from `scripts3d/cast.json`, `set` = `{"place": ..., "time": "day"|"sunset"}`), then follow `../tools/ANIM3D.md` (voices → 5 test frames → render → soundtrack → assemble → thumbnail → 1–2 Shorts).

## 2. Gate, upload, translate, log
Rek-ball ≥ 85 (`../tools/rek_ball.py`). Upload with `UPLOAD.md` — **Made for Kids = YES**. Slots (UTC): long 13:15–14:45, 17:15–18:45, 21:15–22:45; Shorts 11:45, 16:15, 19:45, 23:45 (±30 min, minutes :15/:45). Then `../tools/TRANSLATE.md` (7 languages + subtitles). Log the episode in `story/log.json` (`episode, date, activity, place, title, minutes, uploads[]`), unlock, commit, push. Update hub doc `agents/max` only by appending to its `activity` (the computer's hub also writes this doc).

## 3. Deliver
SendUserFile: 1080p preview, thumbnail, Shorts; short Uzbek message with titles, scores and Bishkek times.

Never type passwords, never add accounts, never change channel settings; upload only to Max the Curious Cat.

## Studio AI 2026-10-29 (Ask Studio, rebuilt from the daily analysis — the run's own patch could not be pushed) — applies from the next run
- Titles never start with the channel name ("Max the Curious Cat | …"). Start with the story hook; the channel name may follow later or stay out.

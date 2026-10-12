# Hollowmere Tales — daily run (instructions for Claude)

Goal: keep the YouTube channel **Hollowmere Tales** (@HollowmereTalesTV, channel id `UCiOfdnuWUlHj5bPi6H5scgA`) supplied with **1 long episode (3–5 min) + 3 Shorts per day**, scheduled ahead so they publish even when the user's laptop is off. Work fully unattended. The user speaks **Uzbek** — the final message must be in Uzbek. Video content is English.

## 0. Buffer check FIRST (this task fires several times a day)
1. `git pull`, read `story/log.json`; collect every `uploads[].publish_at` → the set of **New York dates** already covered.
2. Target = the next **2 New York days after today** (NY = UTC−4, Nov–mid-March UTC−5). Today counts only if its 11:00 NY slot is still ≥ 90 min away.
3. All target days covered **and** no episode with missing uploads (step 5) → **stop**: no render; one Uzbek line ("Bufer to'la: videolar DD.MM gacha rejalashtirilgan.").
4. Otherwise make **one episode per uncovered day, at most 2 per run**, earliest day first; that day is the episode's `date`.
5. If an episode in log.json has fewer than 4 `uploads` (or a `pending_uploads` list), first re-render the missing videos from its saved scripts (`scripts/epNNN_*.json`) and upload them (to the `publish_at` in `pending_uploads`; if that time is already past, use the same slot on the next free day), move them into `uploads`, delete `pending_uploads`. Then continue with step 4.

## 1. Setup
```bash
cd <repo>/hollow && bash setup.sh
```

## 2. Read
`story/bible.md` (world, characters, creatures, rules, structure), `story/SCRIPT_FORMAT.md`, `story/themes.md`, `story/log.json` (continue from the last cliffhanger), and `scripts/_build_ep001.py` as the style example.

## 3. Write the scripts
N = last episode + 1 (3 digits). Write `scripts/_build_epNNN.py` (same helper style as `_build_ep001.py`) producing:
- `epNNN_long.json` — 5–7 shots, **180–300 s** (`--check`; add shots/lines if shorter). Title `<Scary title> | Hollowmere Tales EP <n>`.
- `epNNN_short1.json` (the rule), `epNNN_short2.json` (Would YOU…?), `epNNN_short3.json` (scariest moment). 15–45 s each, `hook` set.
- Every line has `en es de fr it pt`. Keep lines ≤ 16 words.
- Place characters/creatures per SCRIPT_FORMAT (ground y≈905; Odo 450–900; creatures 1250–1600).

## 4. Validate, preview, render
```bash
python3 scripts/_build_epNNN.py
for f in scripts/epNNN_*.json; do python3 engine/render.py "$f" --check || echo FIX "$f"; done
python3 engine/render.py scripts/epNNN_long.json --preview 5 40 90 150    # look at the PNGs
for s in short1 short2 short3 long; do python3 engine/render.py scripts/epNNN_$s.json; done   # long ≈ 45–60 min on 2 cores
```
Run the full render in the background (`setsid nohup … &`) and poll the log; it is slow (~1 s CPU per frame).

## 5. Check
`ffprobe` durations; extract 3 frames per video and look: characters visible, creatures readable, subtitles readable, nothing cut off.

## 6. Upload (UPLOAD.md) and log
Schedule the 4 videos on Hollowmere Tales via the Claude app's built-in browser (see `UPLOAD.md`). Then append to `story/log.json` → `episodes`:
```json
{"episode": N, "date": "YYYY-MM-DD", "theme": "...", "rule": "...", "title": "...", "creature": "...", "bg": ["..."],
 "summary": "2 sentences", "cliffhanger": "...", "shorts": ["t1","t2","t3"],
 "uploads": [{"title": "...", "publish_at": "2026-10-13T15:00:00Z"}]}
```
Commit the build script + 4 JSON scripts + log.json (NOT `out/`) and `git push` (on rejection: `git pull --rebase` and push again).

## 7. Deliver
SendUserFile (status "proactive"): the long MP4, its thumbnail, and the 3 Shorts. Then a short Uzbek message: EP number + title, one-line story, scheduled Bishkek times, problems.

## Never
- Upload only to Hollowmere Tales (channel id above). Never type passwords, never change account settings, never touch the old private videos on the channel.
- No gore, blood, injuries, death on screen, real brands/characters/games/memes. Original stories only.

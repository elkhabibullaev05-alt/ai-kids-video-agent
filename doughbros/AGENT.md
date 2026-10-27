# Daily Dough Bros run — instructions for Claude

> **Owner rule 2026-10-26 (overrides older lines below):** follow `cloud/WRITER.md` sections "Real-life stories", "Serial format like @d.pommikox.world" and "Bolt, Hollowmere, Dough Bros — Pommi-style serial": numbered continuing serial, forest/village/market-feel places, Shorts cut from the long, Narrator subscribe line after the hook and "What do you think happens in the next part? Tell me in the comments." at the end.


> **3D since 2026-10-19 (owner's rule — overrides the renderer, formats and daily counts below):** every video is now a 3D animation made with `engine3d/` (same engine as Inspector Bolt). Read `../tools/ANIM3D.md` first: write `scripts3d/epNNN.json` in the Bolt script format using `scripts3d/cast.json`, render with Blender, **3 long (3:00–3:40) + 4 Shorts per UTC day**, one long per run. The story bible, tone, titles, audience setting, upload flow, slots, rek-ball gate and translations stay as written below. The old 2D `engine/` is no longer used.


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

**Rek-ball gate (owner's rule — never skip):** before uploading, score every MP4:
`python3 <repo>/tools/rek_ball.py <file>.mp4 "<YouTube title>"` → JSON with `ball` (0–100), `qism` (parts) and `muammo` (problems, Uzbek).
A video with **ball < 85 is NOT uploaded**. First try the automatic edit: `python3 <repo>/tools/rek_ball.py <file>.mp4 "<title>" --kuchaytir` (punch-in zoom rhythm + loudness fix, writes `<file>_d.mp4`; upload that file if it scores ≥ 85 and its frames look right). Otherwise fix what `muammo` names (stronger first 3 s, faster changes, no still stretch, louder audio, better title) by editing that script and re-rendering, then score again — at most 2 fix rounds per video per run. If it still scores < 85, do not upload it: record it in `story/log.json → rejected` as `{"date","title","ball","muammo"}` and make a new video instead in the next run (the buffer check counts only uploaded videos). Report each video's score in the final message.

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

## Retention notes 2026-10-18 (owner-approved, from the hub's view counts)
Views come almost only from Shorts. Last 12 uploads: "Would YOU open this closet? 👇" got **580** views; character-gag Shorts got 0–3; long episodes got 0–24.
- **short2 (question/dare) is the main Short now.** Build it around ONE object the viewer can picture (a closet, a freezer door, a jar) and a direct "Would YOU…?" question in the title and the first 2 s. Title pattern that worked: `Would YOU <verb> this <object>? 👇 #shorts`; vary verb and object every day, never repeat one from the last 14 days.
- short1 (character moment): open on the scare or the punch itself in frame 1, not on the set-up; title must say what happens, not who it is ("The closet BREATHED at Pim 😱", not "Pim says he's NOT scared").
- short3 (teaser): use the scariest single beat and end on an open question, not "TO BE CONTINUED".
- Long title as a question the viewer can answer in their head (like EP 9 "Can You Solve 3 Scarecrow Riddles?", the best long at 24 views), not "Dough Bros vs <VILLAIN>".
- End every Short with a 1-line spoken + on-screen "Follow for part 2" / subscribe prompt in the last 2 s.

## 19-okt reja (owner-approved) — OVERRIDES the rules above where they conflict
Long episodes are watched only 0:36–0:56 (20–31%) and get 0–1 views; the "Would YOU…?" Shorts work (closet 580).
- **Stop the long episode.** Do not render or upload the 3–5 min long video. Each episode = **3 Shorts** (short2 "Would YOU…?" stays the main one). Keep writing the episode story as before so the Shorts have a plot, but only the Shorts are rendered and uploaded.
- Buffer check: a day is "covered" when its 3 Shorts are scheduled (09:00, 12:00, 18:00 NY); the 15:00 long slot stays empty. The freed upload limit goes to Shorts and `pending_uploads`.
- Shorts length **20–35 s**. Frame 1 = the scare/punch or the object of the question, with big on-screen text of 3–6 words ("WOULD YOU OPEN THIS?"); no logo, no intro, no set-up shot.
- **Loop:** the last line leads back into the first beat, so the Short replays smoothly.
- Never reuse a Short title from the last 30 days (log.json).

## Never
- Never upload anywhere except scheduling the day's 4 videos on the Dough Bros channel (@DoughBrosTV) as described in UPLOAD.md. Never type passwords or change account settings.
- Never use real brands, existing characters, songs, games or memes.
- Never put gore, blood, weapons or real-world danger in scripts.

## Translations (owner's rule, 2026-10-19 — never skip)
Every uploaded video gets its title and description in **es, pt, ar, fr, ja, ko, de** (a viewer in Japan sees Japanese, in the US the English original), and long/voiced videos get English + translated subtitles. Follow `../tools/TRANSLATE.md` right after the uploads are scheduled; first finish any `translations_pending` from earlier runs. Report the languages added in the final message.

## Safety notes 2026-10-20
- Title template: the last 10 titles all end in `?!` + one emoji. Vary the form — at most 1 in 3 titles may end in `?!`; also use statements, "How…", character names, no emoji on some. Vary the first spoken line of each script (no repeated opening phrase across the last 5 episodes).
- Audience: the owner's 2026-10-19 safety routine lists Dough Bros as a kids channel, but this file and `cloud/channels.json` say "Not made for kids" (13+). Do NOT change the flag on your own — the owner decides. Until then keep content clearly 13+ in tone and never target kids in titles/tags (no "for kids", nursery words).
- (2026-10-21) Each Short gets its own title and first line — never a rephrase of its long episode's title (duplicate metadata reads as repetitive content). Before uploading, compare the day's titles: no two may share the same hook word or end the same way.


## Studio AI 2026-10-27 (overrides older title rules)
Titles: hook/mystery first, episode number only at the END ("… (Ep 32)"), never "Ep 32 · …" at the start; unique, < 50 chars. Frame 1 = motion + shock line in big text, no fade/title card. See cloud/WRITER.md "Studio AI findings 2026-10-27" and cloud/growth/ask_studio_2026-10-27.md.


## Growth plan 2026-10-28 — see cloud/growth/PLAN.md (Dough Bros section)
- More "Would YOU…?" dare Shorts (78–87 % viewed); never "Trust X or Y?" openers (29 %).
- Long episodes = 8–10 min compilations of the best mini-stories (kids watch longer compilations).
- Keep Made for Kids = Yes.

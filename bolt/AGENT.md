# Inspector Bolt — production run (instructions for Claude)

Goal: keep the YouTube channel **Inspector Bolt** (id `UCv2hAyDv5m8Rm-0L63a93XQ`, kids 3D cartoon cars mysteries) supplied with **2 long episodes + 5 Shorts per day**. Each run makes ONE long episode (4:00–5:00, 4K, 8D sound, every character voiced) and cuts **2–3 Shorts** from it. Two runs fire per day. Work unattended. The user speaks **Uzbek** — the final message must be in Uzbek. Video content is English. Read `story/bible.md` (series rules) and `story/SCRIPT_FORMAT.md` (script vocabulary) first.

## 0. Buffer check
1. `git pull`; read `story/log.json`. LOCK: if `"lock"` has `"until"` in the future → stop with one Uzbek line. Otherwise set `"lock": {"until": now+7h, "by": "<session>"}`, commit + push at once (on rejection `git pull --rebase`; if a newer lock appears, stop). Remove the lock in your final commit, also when stopping early.
2. Computer check: `mcp__remote-devices__Claude_Browser__tabs_context`. If it fails, the computer is off: you can still make the episode, but keep it in `pending_uploads` (files go to the orphan branch, step 5.1, so nothing is lost).
3. Upload any `pending_uploads` first, oldest first (their files are on branch `uploads-bolt-epNNN`, see UPLOAD.md). Give each one the earliest free slot (step 5), move it to that episode's `uploads`.
4. Count long uploads (`kind: "long"`) with `publish_at` on today's and tomorrow's UTC date. Both days have 2 → stop (remove lock). Offline limit: if the computer is off and 2+ long videos already wait in `pending_uploads`, stop.

## 1. Setup
`cd <repo>/bolt && bash setup.sh` (Blender 4.2.3 portable + Kokoro TTS; ~2 min).

## 2. Write the episode
- N = last episode + 1 (3 digits). Pick a mystery from `bible.md → Episode ideas` not yet used (or invent one); a different culprit and lesson than the last 3 episodes in log.json.
- Write `scripts/epNNN.json` exactly in the format of `scripts/ep001.json` (`SCRIPT_FORMAT.md`). 70–95 beats, every character speaks, lines ≤ 20 words, camera changes at least every 2 beats.
- **Beat 1 must be motion** (cars driving in / spinning / jumping on a `wide` or `two:` camera) — rek-ball checks the first 3 s.
- Title ≤ 60 chars, a question/shock + emoji, **no "Episode N"** (e.g. `Who Stole the Birthday Cake? 🎂🔍 Cartoon Cars Mystery`). Description: 2 sentences + "Inspector Bolt #N" + 3 hashtags (#kids #cartoon #cars).
- Validate: `python3 -c "import json;json.load(open('scripts/epNNN.json'))"`.

## 3. Voices → test frames → render → sound → assemble
```bash
O=out/epNNN
python3 engine/voices.py scripts/epNNN.json $O 12            # prints TOTAL s: must be 240–300 s; else add/cut beats and repeat
BL=/opt/bl/blender-4.2.3-linux-x64/blender
$BL -b --factory-startup -P engine/story.py -- --tl $O/timeline.json --out $O/frames --res 854 --samples 2 --frames 30,600,1400,2200,2800
```
Look at the 5 test frames (Read the PNGs, e.g. hstack them with ffmpeg): characters in frame, nobody blocking the camera, the mystery prop visible. "SHOT FALLBACK"/"ACTION SKIPPED" lines in the log mean a wrong name in the script — fix it. Then the full render (≈ 4–5 h on this CPU; it is resumable — if it stops, run the same command again and it continues from the last frame):
```bash
setsid nohup $BL -b --factory-startup -P engine/story.py -- --tl $O/timeline.json --out $O/frames --res 854 --samples 2 > /tmp/render_NNN.log 2>&1 &
```
Poll with `ls $O/frames | wc -l` every 10–20 min (sleep in single calls ≤ 9 min; never parallel sleeps). Expected frames = timeline duration × 12 + 1. While it renders, prepare upload texts. Then:
```bash
python3 engine/soundtrack.py $O                               # dialogue + 8D detective music + SFX -> $O/audio.wav
bash engine/assemble_long.sh $O out/epNNN.mp4                 # 4K 24 fps, subtitles, -14 LUFS, capped bitrate
ls -la out/epNNN.mp4                                          # must be < 95 MB (GitHub limit); if not: MAXRATE=3.5M bash engine/assemble_long.sh …
python3 engine/thumb.py $O/frames/f_<a dramatic frame>.png out/epNNN_thumb.jpg "WHO DID IT?"
```
Extract 3 frames from the MP4 and look at them; ffprobe the duration.

## 4. Shorts (2–3 per episode, 5 per day in total)
```bash
python3 ../tools/make_short.py out/epNNN.mp4 out/epNNN_s1.mp4 --start <s> --dur <20-40> --top "<hook 3-7 words>" --bottom "Full episode on the channel"
```
Pick the best moments from `$O/timeline.json` beat start times: s1 = the mystery moment (first 30 s), s2 = the funniest press moment (squash/banana), s3 = the reveal of the culprit. Short title ≤ 50 chars + emoji + " #shorts" (no spoilers in s1/s2; s3 may tease "The Thief Was... HER?!"). Description: one sentence + "Full episode: <long video URL>". How many to cut: 5 − (Shorts already scheduled for that UTC day); at most 3 per episode.

**Rek-ball gate (owner's rule — never skip):** score every MP4 before upload:
`python3 ../tools/rek_ball.py <file>.mp4 "<YouTube title>"` → `ball` (0–100) and `muammo`.
**ball < 85 is NOT uploaded.** Shorts: first try `--kuchaytir` (writes `<file>_d.mp4`, upload that if ≥ 85). Long: fix what `muammo` names (too short → add beats; weak start → motion in beat 1; weak title → shorter question title; quiet → re-assemble) and re-score — at most 2 fix rounds. Still < 85 → record in `log.json → rejected` (`{"date","title","ball","muammo"}`) and don't upload it. Report every score in the final message.

## 5. Upload (UPLOAD.md) and log
1. Push the files to the orphan branch `uploads-bolt-epNNN` (UPLOAD.md step 1) — always, also when the computer is off (then they wait in `pending_uploads` with `"branch"`).
2. Upload in Studio with **Made for Kids = YES**. Release slots (UTC, minutes :15 or :45, ≥ 30 min ahead, never two videos at the same time):
   - Long: one at **14:15–15:45** and one at **21:15–22:45** per UTC day.
   - Shorts: **11:15–12:45, 16:15–17:45, 18:45–19:45, 23:15–23:45, 02:15–03:45**, max 5 per UTC day, the first Short of an episode after its long video.
   Studio shows Bishkek time (UTC+6) — convert.
3. After all uploads of the episode: delete the branch (`git push https://github.com/elkhabibullaev05-alt/ai-kids-video-agent --delete uploads-bolt-epNNN`).
4. Append to `story/log.json → episodes`:
   `{"episode": N, "date", "mystery", "culprit", "lesson", "object", "title", "minutes", "uploads": [{"kind": "long"|"short", "video_id", "title", "publish_at": "...Z", "ball"}]}`
   Commit `scripts/epNNN.json` and `story/log.json` (NOT `out/`), remove the lock, push (on rejection `git pull --rebase`, push again).

## 6. Deliver
SendUserFile (status "proactive"): a 1080p preview of the long (`ffmpeg -i out/epNNN.mp4 -vf scale=1920:-2 -crf 26 out/epNNN_1080p.mp4`), the thumbnail and the Shorts. Then a short Uzbek message: episode, title, one-line plot, rek-ball scores, scheduled Bishkek times, problems.

## 7. Agentlar markazi
Update the owner's hub (https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r) with ArtifactData: get `agents/bolt`, then `update` it (pin `if_version`) — append one activity line `[YYYY-MM-DD HH:MM] ...` (Bishkek time) per thing done, keep the last 12; refresh `videos` (newest first: at, id, kind "long"/"short", s "scheduled"/"out", t, v null), `next` (future publish times), `numbers` (episodes, longs, shorts, rejected), `status` ("ok"/"warn"/"error"), `status_text`, `last_seen`. If the doc is missing, create it with the same fields.

## Never
Never type passwords, never add accounts, never change account/channel settings. Upload only to Inspector Bolt, always Made for Kids = YES. No real brands, no real people, nothing scary or mean. Never copy characters or stories from existing cartoons.

## Translations (owner's rule, 2026-10-19 — never skip)
Every uploaded video gets its title and description in **es, pt, ar, fr, ja, ko, de** (a viewer in Japan sees Japanese, in the US the English original), and long/voiced videos get English + translated subtitles. Follow `../tools/TRANSLATE.md` right after the uploads are scheduled; first finish any `translations_pending` from earlier runs. Report the languages added in the final message.

## Safety notes 2026-10-20
- Title template: titles repeat "Who … ? 🔍 Cartoon Cars Mystery". Keep the series tag only in some titles; vary the hook (place, suspect, clue). Vary the opening line of each script.
- Made for kids = Yes must stay on every upload (UPLOAD.md uses VIDEO_MADE_FOR_KIDS_MFK; channels.json kids=true). Music/SFX: only self-generated audio from engine/soundtrack.py.

## Safety notes 2026-10-25
- Repetitive-content risk: all logged titles end with the same "🔍 Cartoon Cars Mystery" tail. Use that tail on at most 1 title in 3; vary the form (statement, character-name first, number, "What happened to…?") and vary the first spoken line of each script. Made for kids = Yes stays.


## Studio AI 2026-10-27 (overrides older title rules)
Titles: hook/mystery first, episode number only at the END ("… (Ep 32)"), never "Ep 32 · …" at the start; unique, < 50 chars. Frame 1 = motion + shock line in big text, no fade/title card. See cloud/WRITER.md "Studio AI findings 2026-10-27" and cloud/growth/ask_studio_2026-10-27.md.


## Growth plan 2026-10-28 — see cloud/growth/PLAN.md (Inspector Bolt section)
- Keep the usual episode count (owner 28 Oct: "kamaytirma"); release in US mornings/afternoons (13:15–15:45 UTC), not at night.
- Thumbnails: Bolt's shocked face big, bold colours, no small text; titles < 50 chars ("Lost in the Dark! Can Bolt Save Wren?").

## Competitor format 2026-10-28 (Tayo / Robocar POLI / Gecko's Garage — applies from the next run)
**Phone verification (checked in Studio 2026-10-28):** verified = Roblox, Calm Rain, Max, Doodle Desk. NOT verified = Hollowmere, Dough Bros, Wild Sketchbook, Money Story, Funny Rank, Inspector Bolt, Seoul Night Remix, Milo Survives → on these channels no video may be longer than **14:50**, and no custom thumbnails / Related-video links (they fail). Re-check in Studio → Settings → Channel → Feature eligibility before making anything longer.
- Bring the robot detective Bolt back as the hero of every episode (the "Wheelburg" talking-car uploads 25–27 Oct got 0 views); Bolt's face big in the first frame.
- Title = emotional cry + searchable tail: "<Friend> Is Trapped! Bolt to the Rescue | Car Cartoons for Kids".
- Each episode ends with a 20–30 s "Bolt's Safety Rule" song/lesson. Weekly compilation **max 14:50**. Seasonal tie-ins (Halloween now).

# The Doodle Desk — production run (instructions for Claude)

Goal: keep the YouTube channel **The Doodle Desk** supplied with **2 long videos (8–12 min) per day**: real news, explained with hand-drawn stick figures and dry humour (see `story/STYLE.md`). Work unattended. The user speaks **Uzbek** — the final message must be in Uzbek. Video content is English.

## 0. Buffer check (this task fires several times a day)
1. `git pull`; read `story/log.json`. LOCK: if `"lock"` has `"until"` in the future → stop with one Uzbek line. Otherwise set `"lock": {"until": now+4h, "by": "<session>"}`, commit + push at once (on rejection `git pull --rebase`; if a newer lock appears, stop). Remove the lock in your final commit, also when stopping early.
2. Channel: `log.json → channel.id`. If it is null, look in Studio (built-in browser, account switcher) for a channel named "The Doodle Desk" (or any channel whose name contains "Doodle"); if found, save name/id/handle to log.json. If none exists yet: still make the video, keep it in `pending_uploads`, deliver the files, and tell the user the channel still has to be created.
3. Upload any `pending_uploads` first, oldest first (re-render from the saved script `scripts/epNNN.json` if `out/` is gone — the cloud workspace is new every run). Give each one the earliest free release slot (rules in step 4: 14:00–17:45 / 20:00–23:45 UTC, :15 or :45, ≥ 30 min ahead, max 2 per UTC day), schedule it in Studio, move it from `pending_uploads` to `uploads` with `publish_at` + `video_id`. A news video older than 4 days is not uploaded — mark it `"skipped": "too old"`.
   Computer check first: call `mcp__remote-devices__Claude_Browser__tabs_context` (or `get_device_info`). If it fails, the computer is off: don't retry, keep everything in `pending_uploads`.
4. Count long videos scheduled (`uploads[].publish_at`, UTC dates) for today and the next UTC day. Both days have 2 → stop (remove lock). Otherwise make ONE episode for the earliest open slot.
   Offline limit: if the computer is off and 2 or more videos are already waiting in `pending_uploads` (not skipped), don't make another one — stop with one Uzbek line (they would only go stale).

## 1. Setup
`cd <repo>/doodle && bash setup.sh`

## 2. Research and write
- Pick the story (STYLE.md). Use WebSearch/WebFetch; 3–5 sources; write down exact numbers and who said what.
- N = last episode + 1 (3 digits). Write `scripts/_build_epNNN.py` (copy the helper style of `_build_ep001.py`) → `scripts/epNNN.json`.
- Length: **1,300–1,600 words**, 70–100 scenes, so `--check` reports **8–12 min**. Shorter → add a part; longer → cut.
- Vary the jokes, cold open and structure from the last episodes (read their titles/topics in log.json). Never reuse a cold open.
- Title ≤ 60 chars, a question or a bold claim the video really answers; thumbnail 2–5 huge words + a shocked/smug stick figure + one prop.

## 3. Validate, preview, render
```bash
python3 scripts/_build_epNNN.py
python3 engine/render.py scripts/epNNN.json --check
python3 engine/render.py scripts/epNNN.json --preview 8     # look at the PNGs: nothing overlapping, text inside the frame
setsid nohup python3 engine/render.py scripts/epNNN.json > /tmp/render_NNN.log 2>&1 &   # poll the log
```
Then extract 3 frames with ffmpeg and look at them; check the duration with ffprobe.

**Shorts from every episode (owner's rule — the channel gets no discovery without Shorts):** after the long video renders, cut **2 Shorts** from it:
```bash
python3 <repo>/tools/make_short.py out/epNNN.mp4 out/epNNN_s1.mp4 --start <s> --dur <30-45> --top "<hook, 4-9 words>" --bottom "Full video on the channel"
```
- Short 1 = the cold open (the first 30–45 s, it already has the hook). Short 2 = the single most surprising number/reveal of the episode (find its start time from the script's scene timings or by looking at frames).
- `--top` is a new hook line, not the long title (a question or bold claim: "ChatGPT now shows you ADS?"). Short title ≤ 60 chars + " #shorts"; description: one sentence + "Full video: <long video URL>" (fill in after the long is scheduled).
- Each Short goes through the Rek-ball gate below like any video.
- Slots (UTC): Shorts at **12:00–13:45** and **18:00–19:45**, minutes :15 or :45, on the same day as their long video (or the next day if that time has passed), at least 30 min in the future. YouTube treats a vertical video ≤ 3 min as a Short automatically — upload it with the same UPLOAD.md flow.
- Log them in the episode's `uploads` with `"kind": "short"` (the buffer check counts only long videos). The 4-day news limit applies to Shorts too.

**Rek-ball gate (owner's rule — never skip):** before uploading, score every MP4:
`python3 <repo>/tools/rek_ball.py <file>.mp4 "<YouTube title>"` → JSON with `ball` (0–100), `qism` (parts) and `muammo` (problems, Uzbek).
A video with **ball < 85 is NOT uploaded**. First try the automatic edit: `python3 <repo>/tools/rek_ball.py <file>.mp4 "<title>" --kuchaytir` (punch-in zoom rhythm + loudness fix, writes `<file>_d.mp4`; upload that file if it scores ≥ 85 and its frames look right). Otherwise fix what `muammo` names (stronger first 3 s, faster changes, no still stretch, louder audio, better title) by editing that script and re-rendering, then score again — at most 2 fix rounds per video per run. If it still scores < 85, do not upload it: record it in `story/log.json → rejected` as `{"date","title","ball","muammo"}` and make a new video instead in the next run (the buffer check counts only uploaded videos). Report each video's score in the final message.

## 4. Upload (UPLOAD.md) and log
Schedule the video on the channel. Release slots (UTC): one between **14:00–17:45** and one between **20:00–23:45**, minutes :15 or :45, never the same clock time as the same slot the day before, at least 30 min in the future. Append to `story/log.json → episodes`:
`{"episode": N, "date": "YYYY-MM-DD", "topic": "...", "title": "...", "minutes": 9.8, "sources": ["..."], "uploads": [{"title": "...", "publish_at": "...Z"}]}`
Commit `scripts/_build_epNNN.py`, `scripts/epNNN.json`, `story/log.json` (NOT `out/`), remove the lock, push (on rejection `git pull --rebase` and push again).

## 5. Deliver
SendUserFile (status "proactive"): the MP4, its thumbnail and the 2 Shorts. Then a short Uzbek message: episode, title, one-line summary, scheduled Bishkek time, problems.

## 6. Agentlar markazi
Update the owner's hub (https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r) with ArtifactData: get `agents/doodle`, then `update` it (pin `if_version`) — append one activity line `[YYYY-MM-DD HH:MM] ...` (Bishkek time) per thing done, keep the last 12; refresh `videos` (newest first: at, id, kind "long"/"short", s "scheduled"/"out", t, v null), `next` (future publish times), `numbers`, `status`/`status_text`, `last_seen`. If the doc is missing, create it with the same fields.

## 19-okt reja (owner-approved) — OVERRIDES the rules above where they conflict
4 long videos got 2 views in total: a new channel gets no traffic for long videos, only Shorts can bring viewers.
- **1 long video per day, not 2.** Buffer check: a day is covered when it has 1 long video scheduled. Use only the 20:00–23:45 UTC release slot.
- Cut the 2 Shorts from every long video as above, but make each **about 30 s** (`--dur 28-32`): Short 1 = the funniest moment (not always the cold open), Short 2 = the most surprising number. `--bottom "Full video on the channel"` stays.
- Frame 1 of each Short = the punchline or the number as big `--top` text (3–6 words), no logo or intro.
- Thumbnail of the long video: a big hand-drawn stick-figure face (shocked or smug) filling ~half the frame + exactly 3 huge words (e.g. "WHY $110 OIL?").
- Titles stay as they are (question form works). Never reuse a title from log.json.

## Never
Never type passwords, never add accounts, never change account/channel settings. Upload only to The Doodle Desk. No invented facts or quotes, no likeness of real people, no partisan side-taking (STYLE.md).

## Translations (owner's rule, 2026-10-19 — never skip)
Every uploaded video gets its title and description in **es, pt, hi, ar, id, fr, ja, ko, de** (a viewer in Japan sees Japanese, in the US the English original), and long/voiced videos get English + translated subtitles. Follow `../tools/TRANSLATE.md` right after the uploads are scheduled; first finish any `translations_pending` from earlier runs. Report the languages added in the final message.

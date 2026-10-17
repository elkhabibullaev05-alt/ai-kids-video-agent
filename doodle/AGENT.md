# The Doodle Desk — production run (instructions for Claude)

Goal: keep the YouTube channel **The Doodle Desk** supplied with **2 long videos (8–12 min) per day**: real news, explained with hand-drawn stick figures and dry humour (see `story/STYLE.md`). Work unattended. The user speaks **Uzbek** — the final message must be in Uzbek. Video content is English.

## 0. Buffer check (this task fires several times a day)
1. `git pull`; read `story/log.json`. LOCK: if `"lock"` has `"until"` in the future → stop with one Uzbek line. Otherwise set `"lock": {"until": now+4h, "by": "<session>"}`, commit + push at once (on rejection `git pull --rebase`; if a newer lock appears, stop). Remove the lock in your final commit, also when stopping early.
2. Channel: `log.json → channel.id`. If it is null, look in Studio (built-in browser, account switcher) for a channel named "The Doodle Desk" (or any channel whose name contains "Doodle"); if found, save name/id/handle to log.json. If none exists yet: still make the video, keep it in `pending_uploads`, deliver the files, and tell the user the channel still has to be created.
3. Upload any `pending_uploads` first (re-render from the saved script if `out/` is gone). A news video older than 4 days is not uploaded — mark it `"skipped": "too old"`.
4. Count long videos scheduled (`uploads[].publish_at`, UTC dates) for today and the next UTC day. Both days have 2 → stop (remove lock). Otherwise make ONE episode for the earliest open slot.

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

## 4. Upload (UPLOAD.md) and log
Schedule the video on the channel. Release slots (UTC): one between **14:00–17:45** and one between **20:00–23:45**, minutes :15 or :45, never the same clock time as the same slot the day before, at least 30 min in the future. Append to `story/log.json → episodes`:
`{"episode": N, "date": "YYYY-MM-DD", "topic": "...", "title": "...", "minutes": 9.8, "sources": ["..."], "uploads": [{"title": "...", "publish_at": "...Z"}]}`
Commit `scripts/_build_epNNN.py`, `scripts/epNNN.json`, `story/log.json` (NOT `out/`), remove the lock, push (on rejection `git pull --rebase` and push again).

## 5. Deliver
SendUserFile (status "proactive"): the MP4 and its thumbnail. Then a short Uzbek message: episode, title, one-line summary, scheduled Bishkek time, problems.

## 6. Agentlar markazi
Update the owner's hub (https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r) with ArtifactData: get `agents/doodle`, then `update` it (pin `if_version`) — append one activity line `[YYYY-MM-DD HH:MM] ...` (Bishkek time) per thing done, keep the last 12; refresh `videos` (newest first: at, id, kind "long", s "scheduled"/"out", t, v null), `next` (future publish times), `numbers`, `status`/`status_text`, `last_seen`. If the doc is missing, create it with the same fields.

## Never
Never type passwords, never add accounts, never change account/channel settings. Upload only to The Doodle Desk. No invented facts or quotes, no likeness of real people, no partisan side-taking (STYLE.md).

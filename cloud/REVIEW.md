# Daily review of the cloud servers (Claude)

Once a day, all channels. Final message in Uzbek, short.

1. `git pull`. For each CH in `cloud/channels.json`:
   - `cloud/results/CH/status.json`: older than 6 h (and stage not `idle`) → the server is down or stuck; stage `error` → read `error`; `quota_wait` → YouTube API daily limit hit.
   - New results since yesterday (`cloud/results/CH/*.json`): long + Shorts uploaded? `ball` values, `seconds`, publish times. Look at the small thumbnails `cloud/results/CH/<id>.jpg` (Read them) — dark, empty, characters off-frame or showing their backs = a renderer problem to fix in `<CH engine>/world.py` or `story.py`.
   - `cloud/rejected/CH/*.reason.json` from the last day: why. Several rejects for the same reason → fix the cause (writer rule in `cloud/WRITER.md` or the engine).
   - Variety: compare the last 9 uploaded titles/plots of the channel. If two look alike, note it and tighten the next writer run (add the pair to `cloud/AVOID.md` under the channel name; the writer reads it).
   - Queue: fewer than `per_day.long` jobs left → say the writer must run.
2. Update the hub (Artifact DB `agents/<CH>`): append to `activity`, set `status` ok/warn/error.
3. Fix small problems directly (engine bug, wrong slot, bad job) and push. Anything needing the owner (server unpaid/off, token expired → "invalid_grant", quota) → tell him exactly what to do, in Uzbek.

# Browser upload — the API-quota overflow

The owner asked (2026-11-07) that when a channel's **API daily quota (≈6 uploads)** is full, the rest of that day's
videos still go out — uploaded through his **Chrome** (YouTube Studio UI) instead of the API. The API stays the fast
primary; this is the no-limit overflow.

## How a video gets here

When `cloud/worker.py` hits the API quota, `browser_handoff()` (same file) for each still-pending video:
- pushes the MP4 (+ thumbnail) to its own throwaway orphan branch `up-<slug>` on GitHub (temporary host),
- writes a manifest `cloud/browser_queue/<ch>/<slug>.json`,
- reserves the publish slot in the worker's state so nothing double-books it.

So a manifest is a video that is **ready and waiting for a browser upload**. Channels & authuser: `cloud/growth/CHANNELS.md`.

## Manifest fields

```
{"ch","channel_id","job","kind":"long"|"short","title","description","tags":[...],
 "kids":true|false,"category":"<number>","synthetic":true|false,"localizations":{...}|null,
 "publish_at":"YYYY-MM-DDThh:mm:ssZ (UTC)","branch":"up-...","mp4_url":"raw.githubusercontent…","thumb_url":…|null,"queued_at":…}
```

## What this run does

1. Make sure the repo `elkhabibullaev05-alt/ai-kids-video-agent` is in the session (add_repo, push access) and clone it.
2. List every `cloud/browser_queue/*/*.json`. If none, stop with one Uzbek line ("Brauzer navbati bo'sh"). Otherwise group the manifests by `ch`, oldest `queued_at` first. Cap at ~8 uploads per run so it stays under ~2 hours; the rest wait for the next run.
3. Browser = the owner's **Chrome** via the Claude in Chrome tools (`mcp__claude-in-chrome__*`: load tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool, get_page_text, find, tabs_close_mcp in ONE ToolSearch call). Own new tab; close it at the end. Never type a password; if Google asks to sign in, stop and tell the owner. Keep each javascript_tool call short (they time out ~45 s).
4. Reuse the Studio JS helpers already written in `doodle/UPLOAD.md` section 3 (`window.__new/__open/__fill/__thumb/__pickDay/__pickTime/__sched/__done`). They are channel-agnostic except the three differences below — adapt `__fill` per manifest.

### Per channel
- Open `https://studio.youtube.com/channel/<channel_id>/videos/upload?authuser=<N>` (N from CHANNELS.md), wait ~6 s, confirm the page shows that channel (`#entity-name` or `location.href`). If it lands on the wrong channel, re-check authuser with `https://studio.youtube.com/?authuser=N`. Wrong channel or a sign-in page → skip that channel, leave its manifests, report it.

### Per manifest (video)
1. Fetch the blobs into the page from `mp4_url` (and `thumb_url` if set) — the same `fetch()`→`window.__dl[name]` trick as doodle/UPLOAD.md section 2, using the manifest's raw URLs. Poll until the sizes are there.
2. `await window.__open('<mp4 name>')`.
3. Fill title, description and tags from the manifest. In `__fill`, set **Made for kids** from `manifest.kids`:
   - `kids:true`  → click `tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_MFK]`
   - `kids:false` → click `tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]`
   Delete the default tag chips first, then add ours.
4. **Category** (under "Show more"/"Batafsil" → Category): pick the one whose number matches `manifest.category` (1=Film&Animation, 10=Music, 15=Pets&Animals, 22=People&Blogs, 23=Comedy, 24=Entertainment, 25=News&Politics, 27=Education). Only set it if the manifest has a category and the field is reachable; if not sure, leave the default.
5. **Altered/synthetic content**: if `manifest.synthetic` is true, in the "Altered content" step choose **Yes** (AI-generated/altered). Otherwise **No**.
6. Thumbnail: if `thumb_url` was set, `window.__thumb('<thumb name>')`.
7. Schedule: convert `publish_at` (UTC) to **Bishkek time (UTC+6)**, then `await window.__sched(DAY, 'HH:MM')` (minutes are on the :00/:15/:30/:45 list). Confirm it echoes the day and time you asked for.
8. `await window.__done()`. A short gets "scheduled"; a long may show a "still processing" dialog with the date — read it and close it.

### After each successful upload
- Read the new video id if the share dialog or URL shows it (optional).
- Record it in `cloud/results/<ch>/<job>.json`: load it (or start `{}`), then for `kind:"long"` set `"long": {"video":id|"", "publish_at":publish_at, "title":title}`, for `kind:"short"` append the same shape to `"shorts"`. Keep existing fields.
- Delete the manifest `cloud/browser_queue/<ch>/<slug>.json`.
- Delete the throwaway branch: `git push https://github.com/elkhabibullaev05-alt/ai-kids-video-agent --delete <branch>` (ignore "remote ref does not exist").

### Rules
- Never type passwords, never add accounts, never change account/channel/Studio **settings**, never touch tokens.
- Never delete or edit already-published videos.
- Keep the made-for-kids flag exactly as the manifest says (it comes from the channel config).
- If an upload fails or is stuck, leave its manifest and branch for the next run, and say so.

## Commit and report

- Commit and push `cloud/results/**` and the removed `cloud/browser_queue/**` manifests (`git pull --rebase` on rejection).
- Final Uzbek message, 3–6 lines: per channel how many videos the browser uploaded and their Bishkek times, how many still wait in the queue, and anything the owner must do (e.g. a channel that showed a sign-in page).

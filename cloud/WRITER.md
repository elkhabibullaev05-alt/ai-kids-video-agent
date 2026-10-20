# Story writer (Claude) — the only Claude part of cloud production

Owner's rule (2026-10-19): every channel renders and uploads **on its own cloud server without Claude** (`cloud/worker.py`).
Claude only **writes the stories** into the queue and **reviews** the results (`cloud/REVIEW.md`). The owner speaks Uzbek: the final message is in Uzbek. Videos are English.

## One run = one channel (`CH` = bolt | doughbros | hollow | maxcat | roblox)
1. `git pull`. Read `cloud/channels.json → CH` (`per_day`, `seconds`, `kids`), the channel's story bible (`<dir>/story/bible.md`, or the top of `<dir>/AGENT.md`), `bolt/story/SCRIPT_FORMAT.md`, `tools/ANIM3D.md`, and the cast `<dir>/scripts3d/cast.json` (Bolt: `bolt/scripts/ep001.json` chars).
2. Server state: `cloud/results/CH/status.json`. If it is missing or older than 24 h, the server is not running — write at most what is needed to fill the queue to **2 jobs** and say so in the final message.
3. Fill the queue: jobs waiting in `cloud/queue/CH/` must be ≥ `per_day.long × 2`. Write the missing ones (at most `per_day.long × 2` per run).
4. Read `cloud/rejected/CH/*.reason.json` from the last 3 days and `cloud/AVOID.md` (section CH) — never repeat what got a job rejected or flagged.
5. Commit only `cloud/queue/CH/`, push (`git pull --rebase` and retry on conflict). Stop.

## Never two look-alike videos (owner's rule)
Before writing, list the last 40 jobs of this channel (`cloud/done/CH/*.json` + `cloud/queue/CH/*.json`: `long.title`, `plot`, `script.set.place`, the main characters). Every new job must differ from **each** of them in at least 3 of: place, main problem/mystery, the two lead characters, the twist/ending, the title pattern (question / shock / "Who…" / number / dare), the time of day. Also differ from the other new jobs written in this run. No reused jokes or catch-phrases from the last 10 jobs. Vary the shot plan (`cam`) too. The worker auto-rejects titles that are ≥ 78 % similar to an old title and dialogue that shares > 25 % of its 5-word phrases with an old job.

## Job file: `cloud/queue/CH/<YYYYMMDD>-<n>-<slug>.json` (the sorted name order = render order)
```json
{
 "id": "20261021-1-lost-crown",
 "plot": "one sentence: who wants what, what goes wrong, how it ends",
 "script": { "title": "…", "set": {"place": "…"}, "chars": {…cast…}, "beats": [ … ] },
 "long": {
   "title": "≤ 60 chars, hook + emoji, never 'Episode N'",
   "description": "2–3 sentences + 3 hashtags",
   "tags": ["…"],
   "thumb_text": "2-4 WORDS",
   "thumb_beat": 14,
   "localizations": {"es": {"title": "…", "description": "…"}, "pt": {…}, "ar": {…}, "fr": {…}, "ja": {…}, "ko": {…}, "de": {…}}
 },
 "shorts": [
   {"beat": 2, "dur": 30, "top": "HOOK TEXT", "title": "≤ 50 chars + emoji #shorts", "description": "One sentence. Full episode: {LONG_URL}",
    "tags": ["shorts"], "localizations": {"es": {"title": "…", "description": "… {LONG_URL}"}, …}}
 ]
}
```
- `script` = the Bolt script format (beats, `cam`, `do`), using this channel's `set.place` values and cast kinds from `tools/ANIM3D.md`. Spoken length must land inside `seconds` (≈ 2.4 words per second + 0.35 s per line). Bolt: 4:00–5:00; other channels: 3:00–3:40. **Renders come out shorter than this estimate** (2026-10-20: maxcat 2:18, doughbros 2:49 — both under the 3:00 minimum), so count with 2.0 words per second and aim for the middle of the range (≈ 400–440 spoken words for 3:00–3:40 channels, ≈ 560–600 for Bolt).
- `thumb_beat` = a beat whose `cam` frames the main character's face (a character close-up or two-shot, facing camera), never a `prop:` / wide cam and never a beat where something `vanish`es — the big text covers the lower half, so the face must sit in the upper half (2026-10-20 maxcat thumb on a `prop:castle` beat showed Dog's head cut off and Max hidden).
- Shorts per job: spread `per_day.short` over the day's `per_day.long` jobs (bolt 3+2, the others 2+1+1). `beat` = index of the beat the Short starts at; pick a hook moment, 20–35 s, no spoiler in the first Short.
- **Translations**: write the 7 `localizations` yourself (es, pt, ar, fr, ja, ko, de — not hi, not id), natural, same emoji, keep `{LONG_URL}` untouched. The worker uploads them; YouTube shows each viewer their language, and auto-dubbing (already on for the channels) does the audio.
- `kids` channels (bolt, maxcat, roblox): gentle, no scary/violent content, no asking for comments. Not-for-kids channels may ask a question in the description.
- Validate before committing: `python3 -c "import json,sys;[json.load(open(f)) for f in sys.argv[1:]]" cloud/queue/CH/*.json`, and every `beats[i].who` exists in `chars`.

The worker picks the oldest job, renders it (~2.5–3 h), checks rek-ball ≥ 85, uploads to the next free slot in `channels.json`, and writes `cloud/results/CH/<id>.json`.

## Ask Studio advice (2026-10-20) — read `cloud/growth/ask_studio_*.md` (newest) before writing

**maxcat**
- CTR is 0.93%, the main problem.
- Titles:
  - Stop using the "Max's X! 🐱 | Funny Cat Stories for Kids" template.
  - Put the exciting part or a question in the first 4–5 words, e.g. "Can Max Stop the Giant Cake Explosion?".
  - Move the keyword tail to the end.
- Every episode starts in media res: a funny sound, a mishap or a surprise in the first 5 s, before any title card.
- Themed 8–10 min compilations (4–5 stories on one theme) are the top performers. Keep making them.
- Thumbnails: Max's big, expressive face with one clear emotion, a bright solid background, 2–3 focal points, no small text.

**All channels:** the newest `ask_studio_<date>.md` has each channel's own numbers and plan. Apply it unless it breaks the rules above.

## Rek-ball rejections to avoid (2026-10-20)

- `doughbros/20261020-2-zero-crumb-party` was rejected with long rek-ball 83:
  - "boshlanishi sust" — weak motion in the first seconds;
  - "uzun video uchun qisqa" — under 3 minutes.
- So, for every long episode:
  - beat 1 starts in motion at 0 s (running, falling, chasing), with dialogue at 0 s;
  - write enough beats for **3:10 or more**.

## roblox (Blocky Quest 3D, added 2026-10-20)
- Bible: `roblox/story/bible.md`; cast `roblox/scripts3d/cast.json`; places obby | lava | tower | tycoon | city | lobby, time day | night.
- Our own blocky designs only: never "Roblox" in titles or thumb_text, no logo, no official avatars/items/maps, never claim real gameplay.
- Made for Kids: gentle peril only (lava = a funny respawn), no comment requests.
- Put `"lead_in": 0` in `script`; beat 1 is in motion with a `text` card.
- 3:10–3:40: about 560 spoken words (measured 2026-10-20: 572 words = 3:23).
- Shorts slots are 2 per day: give each job 1–2 Shorts.

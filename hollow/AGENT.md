# Hollowmere Tales — daily run (instructions for Claude)

> **Owner rule 2026-10-26 (overrides older lines below):** follow `cloud/WRITER.md` sections "Real-life stories", "Serial format like @d.pommikox.world" and "Bolt, Hollowmere, Dough Bros — Pommi-style serial": numbered continuing serial, forest/village/market-feel places, Shorts cut from the long, Narrator subscribe line after the hook and "What do you think happens in the next part? Tell me in the comments." at the end.


> **3D since 2026-10-19 (owner's rule — overrides the renderer, formats and daily counts below):** every video is now a 3D animation made with `engine3d/` (same engine as Inspector Bolt). Read `../tools/ANIM3D.md` first: write `scripts3d/epNNN.json` in the Bolt script format using `scripts3d/cast.json`, render with Blender, **3 long (3:00–3:40) + 4 Shorts per UTC day**, one long per run. The story bible, tone, titles, audience setting, upload flow, slots, rek-ball gate and translations stay as written below. The old 2D `engine/` is no longer used.


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
**From EP 2 the channel tells TRUE STORIES** — real events, documented mysteries and recorded legends from Europe and North America. Read `story/true_stories.md` first (rules + story bank), pick a story not used in the last 30 episodes, then **research it with web search (2–4 reliable sources) before writing**. No invented facts; keep `sources` (URLs) in log.json and put 2–3 of them under "Sources:" in the long video's description.
`story/bible.md` (world, characters, creatures, rules, structure), `story/SCRIPT_FORMAT.md`, `story/themes.md`, `story/log.json` (continue from the last cliffhanger), and `scripts/_build_ep001.py` as the style example.

## 3. Write the scripts
N = last episode + 1 (3 digits). Write `scripts/_build_epNNN.py` (same helper style as `_build_ep001.py`) producing:
- `epNNN_long.json` — 5–7 shots, **180–300 s** (`--check`; add shots/lines if shorter). Title `<Hook> | True Story | Hollowmere Tales EP <n>`. The Narrator tells the real story ("This is a true story…"); Odo and Mothwick walk through the places as silent witnesses / short reactions — never claim they were part of the real event. Use `figure` (historical people, `seed` picks hat style), `ghost`, `ship`, `crow`, `gloamhound` (for beasts) and the backgrounds `lighthouse`, `sea`, `manor`, `village`, `forest`, `swamp`, `chapel`.
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

**Rek-ball gate (owner's rule — never skip):** before uploading, score every MP4:
`python3 <repo>/tools/rek_ball.py <file>.mp4 "<YouTube title>"` → JSON with `ball` (0–100), `qism` (parts) and `muammo` (problems, Uzbek).
A video with **ball < 85 is NOT uploaded**. First try the automatic edit: `python3 <repo>/tools/rek_ball.py <file>.mp4 "<title>" --kuchaytir` (punch-in zoom rhythm + loudness fix, writes `<file>_d.mp4`; upload that file if it scores ≥ 85 and its frames look right). Otherwise fix what `muammo` names (stronger first 3 s, faster changes, no still stretch, louder audio, better title) by editing that script and re-rendering, then score again — at most 2 fix rounds per video per run. If it still scores < 85, do not upload it: record it in `story/log.json → rejected` as `{"date","title","ball","muammo"}` and make a new video instead in the next run (the buffer check counts only uploaded videos). Report each video's score in the final message.

## 6. Upload (UPLOAD.md) and log
Schedule the 4 videos on Hollowmere Tales via the Claude app's built-in browser (see `UPLOAD.md`). Then append to `story/log.json` → `episodes`:
```json
{"episode": N, "date": "YYYY-MM-DD", "theme": "...", "rule": "...", "title": "...", "creature": "...", "bg": ["..."],
 "summary": "2 sentences", "cliffhanger": "...", "shorts": ["t1","t2","t3"],
 "sources": ["https://..."], "uploads": [{"title": "...", "publish_at": "2026-10-13T15:00:00Z"}]}
```
Commit the build script + 4 JSON scripts + log.json (NOT `out/`) and `git push` (on rejection: `git pull --rebase` and push again).

## 7. Deliver
SendUserFile (status "proactive"): the long MP4, its thumbnail, and the 3 Shorts. Then a short Uzbek message: EP number + title, one-line story, scheduled Bishkek times, problems.

## Retention notes 2026-10-18 (owner-approved, from the hub's view counts)
Views come almost only from Shorts; long episodes got 0–6 views. Best Shorts open on a hard fact with a number: "115 people vanished. They left one word." **288**, "The lighthouse went dark. Three men were gone." **230**, "Would YOU board the empty ship?" **196**. Vague mood lines got 3–6 ("Food on board. Sails up. Nobody there.", "Three letters carved on a tree... C R O").
- Every Short's first line and title = the single strangest documented fact, with a number or a count (people, days, years), in ≤ 9 words. The Narrator says it in the first 2 s; no slow fade-in.
- Keep one "Would YOU…?" Short per episode (short2) — it works here too.
- Long title: a plain question about the real mystery ("Where Did the 3 Lighthouse Keepers Go?") — keep that style, and put the strongest fact in the first 10 s of the long video.
- End every Short with a 1-line spoken + on-screen "Follow for the full story" / subscribe prompt in the last 2 s.

## 19-okt reja (owner-approved) — OVERRIDES the rules above where they conflict
Long episodes got 0–6 views; every view comes from Shorts. Until the owner says otherwise:
- **No long video.** Do not write, render or upload `epNNN_long.json`. Each episode = **3 Shorts only** (short1 the rule/strangest fact, short2 "Would YOU…?", short3 scariest moment). Keep researching the true story as before; the facts go into the Shorts and their descriptions (2 sources under "Sources:").
- Buffer check: a day is "covered" when it has 3 Shorts scheduled. Slots: the existing Shorts slots of that day; the old long slot stays empty.
- **Slow down while the upload limit blocks:** if `pending_uploads` across all episodes holds **6 or more** videos, do not make a new episode — only try to upload pending ones, then stop with one Uzbek line.
- Shorts length **20–35 s** (`--check`; cut lines if longer). Frame 1 = the strangest fact as big on-screen text, 3–6 words with a number ("115 PEOPLE VANISHED"); no fade-in, no logo, no title card.
- **Loop:** the last line points back to the first ("…and nobody knows where the 115 went."), so the Short flows into its own start.
- Never reuse a Short title from any earlier episode in log.json.

## Never
- Upload only to Hollowmere Tales (channel id above). Never type passwords, never change account settings, never touch the old private videos on the channel.
- No gore, blood, injuries, death on screen, real brands/characters/games/memes. Original stories only.

## Translations (owner's rule, 2026-10-19 — never skip)
Every uploaded video gets its title and description in **es, pt, ar, fr, ja, ko, de** (a viewer in Japan sees Japanese, in the US the English original), and long/voiced videos get English + translated subtitles. Follow `../tools/TRANSLATE.md` right after the uploads are scheduled; first finish any `translations_pending` from earlier runs. Report the languages added in the final message.

## Studio advice 2026-10-20 (Ask Studio, from this channel's own analytics)

- Shorts: only 4–13.5% stay; 86–96% swipe away.
  - Start at 0 s in media res with a stake, e.g. "115 settlers vanished without a trace—leaving only one word carved into wood".
  - No fades, silences or title cards. Length 20–30 s.
- Long videos: retention fell from 91.7% to 16.7% within 4.5 s on EP 3, because it opened with dates and records.
  - Open with the eerie climax in the first 5 s; give context after.
  - Add sound or visual shifts every 20–30 s. Keep long videos 3–5 min for now.
- Titles: no "EP N", no channel name, under 50 characters, e.g. "115 Settlers Vanished. They Left One Word."
- Thumbnails: CTR is 0.92%; target over 4%. One hero subject with 2–3 bold teasing words ("NO BODIES FOUND").
- Schedule: don't flood. 1–2 long videos a week and 1 Short a day, spaced out.

## Safety notes 2026-10-20
- Title template: the last 10 titles all follow "What/Why/Where … ?". Vary the form (statements, place/name first, year first) — at most half the titles in a day may be a Wh-question. Vary the first spoken line of each script.
- Real-history episodes: name the historical sources in the description ("Sources: …") so they read as researched storytelling, not mass-produced content.
- (2026-10-22) The Wh-question template was replaced by a new one: 4 of the last 5 titles are imperatives ("Don't Open…", "Don't Follow…", "Never Take…", "Don't Stop…"). At most 1 title per day may start with "Don't"/"Never"; mix in place/name-first statements, year-first titles and plain questions. No two titles in a day may share their first word.


## Studio AI 2026-10-27 (overrides older title rules)
Titles: hook/mystery first, episode number only at the END ("… (Ep 32)"), never "Ep 32 · …" at the start; unique, < 50 chars. Frame 1 = motion + shock line in big text, no fade/title card. See cloud/WRITER.md "Studio AI findings 2026-10-27" and cloud/growth/ask_studio_2026-10-27.md.


## Growth plan 2026-10-28 (owner: "hammasini qil") — overrides the pack schedule above where they conflict
Model: Mr Nightmare (7.2M subs): 20–30 min compilations "3 TRUE … Stories", relatable settings, 99 % long videos.
1. **Halloween (one-time, before 2026-10-31 21:00 UTC):** make ONE 12–14:50 min compilation (channel NOT phone-verified: max 14:50) "3 TRUE Halloween Stories That Still Have No Answer" — re-use 3 strongest finished episodes (rendered files or re-render from their scripts), add a 15 s cold-open hook and short narration bridges, new title card-free start, own thumbnail (scared face + "NO ANSWER"). Schedule it 2026-10-31 between 18:15–21:45 UTC. Log it as `"kind":"compilation"`. Do this before any new pack.
2. From then on: every week 1–2 compilations "3 TRUE <setting> Stories" (night shift, new house, highway, school, hospital) max 14:50, on top of the normal packs at their usual count (owner 28 Oct: never lower uploads, raise quality).
3. Titles never start with "Ep N ·"; thumbnail one face/doorway + 2 words. Full plan: `cloud/growth/PLAN.md`.

## Competitor format 2026-10-28 (owner: "raqiblar qanday yasasa, shunday" — applies from the next run)
**Phone verification (checked in Studio 2026-10-28):** verified = Roblox, Calm Rain, Max, Doodle Desk. NOT verified = Hollowmere, Dough Bros, Wild Sketchbook, Money Story, Funny Rank, Inspector Bolt, Seoul Night Remix, Milo Survives → on these channels no video may be longer than **14:50**, and no custom thumbnails / Related-video links (they fail). Re-check in Studio → Settings → Channel → Feature eligibility before making anything longer.
- The Halloween compilation and all "3 TRUE …" compilations: **max 14:50** until the channel is verified (not 15–25 min).
- Format = Mr Nightmare / Mortis Media: title "3 Terrifying TRUE <setting> Mysteries" (or "… To Fall Asleep To"), never "Ep N ·". Each story standalone (no references to earlier episodes). Open each story with a date + place + the strangest fact in the first 5 s; ambient sound, no title card. Subscribe line in the middle, never before the story.
- Visual style for new scenes: dark, realistic, desaturated (fog, window at night, shape in a doorway). No cartoon bobble-head characters in the first frame or thumbnail frame.
- Shorts: open on the shock line at 0 s, end "Full story on the channel".

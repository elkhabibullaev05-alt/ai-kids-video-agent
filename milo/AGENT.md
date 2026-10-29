# Milo Survives — production run (instructions for Claude)

Channel: **Milo Survives** — @MiloSurvivesDaily — Studio id `UCiaE4voy2yYUHOTDr2wfC5A` — Google account eldorbekhabibullaev6 (built-in browser `authuser=5` as of 2026-10-27). Not made for kids. Owner speaks Uzbek; video content is English.

## Format (from the channel's first video, "I Survived 100 Days in a Zombie Hospital")
2D hand-drawn explainer, cream background, **Milo** = small cartoon guy with big round glasses and a yellow raincoat, calm narrator, burned-in captions, a red "DAY N" tag top right, big hand-lettered numbers ("3 DAYS / 3 WEEKS"). Each episode: **"I Survived 100 Days in/on <dangerous place>"** — a survival story told day by day, teaching REAL survival facts (water before food, shelter, signalling, first aid…). Fiction for the story, facts must be true (cite 2–3 reliable sources in the description: Red Cross, CDC, national park services, survival manuals).
Places rotate, never repeat within 15 episodes: zombie hospital (done), desert island, Antarctica, Amazon jungle, Sahara, sinking ship, deep cave, Mars base, frozen Siberian forest, abandoned mall, volcano island, Everest, open ocean raft, haunted subway, tornado alley…

Use the Doodle Desk engine — it draws exactly this style: `doodle/engine/render.py` (+ `ink.py`), script format `doodle/story/SCRIPT_FORMAT.md`, helper style `doodle/scripts/_build_ep001.py`. Add Milo as a cast member in your script (glasses + yellow raincoat colours) — do not change the Doodle Desk cast or its files; put Milo's scripts in `milo/scripts/`, renders in `milo/out/` (not committed).

## Studio AI advice for this channel (2026-10-27) — follow it
- CTR was 1.66% and half the viewers left by 0:18. **First 3 s:** open on the danger ("Day 1. 1 HP. No water. Something is scratching the door.") — no intro, no title card.
- **Title:** tension/curiosity, < 55 chars ("100 Days Trapped in an Infected Hospital", "Can You Survive 100 Days on a Desert Island?").
- **Thumbnail:** Milo in clear danger + 2–3 huge words ("DAY 99…", "TRAPPED!"), high contrast, not text-heavy.
- **Shorts:** cut 2–3 Shorts (30–45 s) from every long video (the scariest/most surprising moment, the best survival fact); title = a hook; description links the long video.
- **Pace:** something changes every 3–5 s; a "DAY N" jump every 30–60 s.

## Schedule
- **1 long video (7–10 min) every 2 days + 2 Shorts from it.** Long at 20:15–23:45 UTC (US evening), Shorts at 13:15–15:45 and 17:15–19:45 UTC the next days, minutes :15/:45, ≥ 30 min ahead.
- `milo/story/log.json` holds `{"lock", "episodes":[{n, date, place, title, sources, uploads:[{kind,title,publish_at,id}]}], "pending_uploads":[]}`. Lock rules as in `doodle/AGENT.md` §0.

## Per run
1. Lock; if a long video is already scheduled within the next 2 days, only upload `pending_uploads` and stop.
2. Pick the next place; research 2–3 sources for the survival facts; write `milo/scripts/_build_epNNN.py` → `milo/scripts/epNNN.json` (1,000–1,400 words, 60–90 scenes, a DAY tag in most scenes).
3. `--check`, `--preview`, render (as in `doodle/AGENT.md` §3); look at 3 frames; Rek-ball gate (`tools/rek_ball.py`, ≥ 85, `--kuchaytir` allowed).
4. Cut the Shorts with `tools/make_short.py` (`--top` = a hook line, `--bottom "Full story on the channel"`).
5. Upload with the `doodle/UPLOAD.md` flow but channel `UCiaE4voy2yYUHOTDr2wfC5A`, branch `uploads-milo`, file names `milo_epNNN*.mp4`; check the page shows "Milo Survives"; Not made for kids; altered content: No (hand-drawn). If the channel has an old "upload defaults" title/description/tags, replace them.
6. Log, unlock, push (scripts + log only). Update the hub `agents/milo` (ArtifactData https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r, pin if_version; activity line, videos, next, status "ok").
7. Final message in Uzbek, 2–3 lines: episode title, Bishkek release times, Rek-ball scores, problems.

## Never
Real people's likeness, gore, self-harm methods, dangerous "how to" that could hurt a viewer (no foraging advice that could poison, no fake medical claims), passwords, account/Studio settings, deleting anything.


## Growth plan 2026-10-28 — see cloud/growth/PLAN.md (Milo section). Structure like Bright Side / Infographics Show: open with the question, answer step by step with pictures.

## Competitor format 2026-10-28 (Beanie Survives 828K, One More Day — applies from the next run)
**Phone verification (checked in Studio 2026-10-28):** verified = Roblox, Calm Rain, Max, Doodle Desk. NOT verified = Hollowmere, Dough Bros, Wild Sketchbook, Money Story, Funny Rank, Inspector Bolt, Seoul Night Remix, Milo Survives → on these channels no video may be longer than **14:50**, and no custom thumbnails / Related-video links (they fail). Re-check in Studio → Settings → Channel → Feature eligibility before making anything longer.
- Cold open: the most dangerous moment, second person, exact time/place ("4:52 p.m., gate B16. The lights go out."). Day 1 starts within 5 s. Never "My name is Milo… stay till the end".
- Series titles "<Story> Ep. N: <moment> (Day X)"; ~10–14 min (max 14:50); named side characters with their own voices; end screen line pointing to the next episode.
- Thumbnail frame: huge red "DAY X", the threat filling the frame, or a "DAY 1 | DAY N" split.

## Studio AI 2026-10-29 (Ask Studio, rebuilt from the daily analysis — the run's own patch could not be pushed) — applies from the next run
- Thumbnail: a huge red "DAY N" and the threat filling half of the frame.

## Auto catch-up when the computer comes back (owner 2026-10-29)
- If this run ends with anything left in `pending_uploads` because the computer was off or disconnected, write a flag to the hub database before finishing: ArtifactData `set` collection `catchup`, doc_id `milo`, data `{"agent": "milo", "at": "<ISO now>", "pending": <count>}` (url https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r; if the doc exists, get it and pin if_version). The hourly hub runner fires this task again as soon as the computer is reachable.
- When a run is a catch-up (the extra message says so): only upload `pending_uploads` (for an interrupted upload, look in Studio for the partial video id first and finish it instead of uploading again), do not make a new video, then delete `catchup/milo` (pin if_version) if nothing is left pending.


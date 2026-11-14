# The Doodle Desk — editorial rules ("What If…" format, owner 2026-11-14)

The old news-explainer rules are in `STYLE.md.bak_20261114` — no longer used.

Format: long, flat-2D, first-person **"What If…" story**, English, **12–16 minutes** (not a Short). Fully original stories and art — similar genre to ConChaser-type channels, but nothing copied (no their titles, characters, lines or art).
Audience: teens and young adults. **Not made for kids** (upload flag stays "No, not made for kids").

## Title formula (≤ 60 chars, every topic new — check `log.json`, never repeat a topic or title)
- `What If You Could See [a hidden thing about people]?` — who likes you, how much money people have, who is lying, who talks behind your back, people's future, IQ, who misses you…
- `What If You [unusual situation]?` — went back 10 years, could hear thoughts for a day, …
- "time left to live"-type topics: keep it gentle and non-graphic — no death scenes, no self-harm, no gore.

## Script (WRITER rule)
- First person ("I"), an ordinary teenager or young adult; setting school / work / family.
- Second 0 = the middle of a scene, in **dialogue**. No hello, no intro, no logo, no "welcome back".
- 20–40 s: the ability appears (a word/number becomes visible above people's heads).
- Every 2–3 minutes a new twist or secret; a big problem in the middle; an emotional resolution and a clear lesson at the end.
- Every story complete and unique: own characters, own names, own twists — no template sentences reused between episodes (YouTube "inauthentic/repetitious content" rule). Vary the opening line, the twist order and the ending of every episode.
- Length ≈ **1,900–2,400 words**, 120–170 scenes, so `render.py --check` reports 12–16 min.
- Clean language, no sexual content, no real people or brands, no bullying shown as funny without consequence.

## Visuals (engine: `engine/render.py` + `engine/ink.py`)
- Simple flat 2D: flat stick/silhouette people (`guy`), simple backgrounds (classroom, kitchen, street) built from `box`/props, a new shot every **3–5 s** (one scene ≈ 1–2 sentences, use `cam` moves + `at` timings).
- Big on-screen title banners for story beats, e.g. `{"box": [...], "color": "dark"}` + `{"text": "THE PRETTIEST GIRL IN SCHOOL", "size": 90, "color": "white"}`.
- The ability visual: a coloured word/number above a head (`guy.label`, or a `text`/`count` item placed above the figure, e.g. "LIAR" in red, "$2,400,000" in green, "73%" etc.).

## Voices and sound
- One main narrator (the "I" character, top-level `voice`, e.g. `am_michael`) + **2–3 other voices** for other characters, set per scene with `"voice"` (`af_bella`, `af_nicole`, `am_adam`, `bf_emma`, `bm_george`). Keep each character on the same voice for the whole episode.
- Light background music (the engine's own music bed, ducked under the voice).

## Thumbnail
One character + a big word/number above their head + 2–4 huge words of text; high contrast (dark bg + bright text or yellow bg + black text). Text adds to the title, never repeats it.

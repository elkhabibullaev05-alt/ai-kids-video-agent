# Ink writer — Wild Sketchbook

> **OWNER FORMAT 2026-11-14 — "Survival: Day 1 to Day 100" (overrides every older format, topic and length rule below; the JSON format, image, honesty and check.py rules still apply).**
> Proof: DoodleSurvivals (opened 14 Oct 2026, 7 videos) — "Zombie Outbreak Survival: Trapped In a Farm Day 1 To Day 100" 1.4M views.
> - **One long story per day**, English, **12:00–14:40** (channel is NOT phone-verified → hard max 14:50; 20 min only after the owner verifies). = **1,900–2,250 words** in `scenes`, 90–140 scenes. One Short per script as before.
> - **First person ("I")** — the narrator lives through it. Title: `I Survived 100 Days <situation>` or `<Situation> Survival: Day 1 to Day 100` (zombie farm, stranded in the desert, ice age, alone on an island, animal world; animal angles welcome: "I Survived 100 Days as a Wolf"). Every title a new situation — never repeat one from `cloud/ink/animals/`.
> - **0 s = the most dangerous moment** (hook ≤ 5 words, first sentence ≤ 14 words, in the middle of the action), then jump back: "Day 1." and tell it in order to **Day 100** at the end.
> - **Big on-screen day counters:** put `"num": "DAY 1"`, `"num": "DAY 37"` … `"num": "DAY 100"` on the first scene of each day block (the renderer stamps it top-left). 12–20 day blocks per video.
> - **A new danger or twist every 1–2 minutes** (≈ every 200–300 words): storm, injury scare, food runs out, a stranger, an animal, the shelter fails. Escalate to the end; Day 100 = rescue/escape/new beginning + a one-line lesson + a comment question.
> - Each story fully its own — no template sentences reused between scripts (YouTube "inauthentic content" rule). Survival facts (water, fire, cold, animal behaviour) must still be real and sourced in `sources`; the story itself is clearly fiction ("what if"). No gore, no animal cruelty, no harmful how-to.
> - Visuals: the existing ink/2D sketch style; change `img` often so the picture changes every 3–5 s (10+ different Wikipedia images: "Barn", "Desert", "Wolf", "Snow", "Campfire", "Island"…).
> - Short: the 0-s danger moment as a 45–59 s loop ending "full story on my channel".
> - The old animal fact-explainer queue is stopped: scripts 021–024 were moved to `cloud/hold/ufc_old_explainers/` (not deleted). Number new scripts from 025.

## Older rules (still valid where the 2026-11-14 format does not override them)

Each run writes **one** new script to `cloud/ink/animals/NNN-slug.json` (next free number) and pushes it to `main`.
The PC agent (`ufctube`) downloads it within 3 hours. From each script it renders one long video (1920x1080, ink/sketch style) and one Short (1080x1920 with word-by-word captions).

## 1. Pick a topic that is hot *right now*

1. Search the web before writing.
   - Find animal news from the last 7 days: viral sightings, new studies, records, attacks, discoveries.
   - Check YouTube/Shorts trending pages (for example youtube.trends24.in/shorts).
   - Check which "what happens if / why do / who would win" animal questions people are searching.
2. Prefer topics that do all three:
   - **Hook a fear or a wonder:** danger, records, "impossible" abilities, mysteries.
   - **Have one hard, surprising number** from a real source.
   - **Have a twist** to save for the end.
3. Proven formats, best first:
   - "What happens if…" (Zack D. Films style)
   - "N secrets of X — #1 is the strangest"
   - "Why X is more dangerous than Y"
   - "The animal that…"
4. Never repeat a topic or animal pair already used in `cloud/ink/animals/`. Read the existing titles first.

## 2. Retention rules (the renderer supports all of these)

- **First scene = hook.** Its `hook` field (max 6 words) is a question or bold claim shown big on screen. The first sentence must pay it off or deepen it within 3 seconds. No "hello", no channel intro.
- **Open loop by scene 3.** Promise the best thing for the end, e.g. "and the last one explains why…". Then deliver it last.
- **List countdown.** For list videos, put `"num": "#5"` … `"#1"` on the first scene of each section. The number badge keeps people counting to the end.
- **One idea per scene.** Each `say` is 1–2 sentences, 12–30 words. The camera punches in every ~2.3 s, so a long scene still moves.
- **Escalate.** Each section must be more surprising than the one before. Put the strongest fact last.
- **Re-hook every ~60 s.** Use a "but here's the twist" or a direct question to the viewer.
- **End.** Ask a comment question ("Which one surprised you?"). No long outro.
- **Short (`short.scenes`).** Write 5–7 scenes, 110–140 words (45–60 s; this length gets the most engagement). The first scene has a `hook`. The **last sentence must flow straight back into the first sentence**, so the Short loops. Use the **same `img`** in the first and last scene.

## 2b. Sound like a live person (owner's rule, 2026-10-19)

- **First 3 seconds decide everything.**
  - `hook` ≤ 7 words.
  - First sentence ≤ 14 words, talking to "you" or making an almost-unbelievable claim.
  - No greeting, no channel name.
  - The renderer starts the voice at 0.0 s and slams the first picture in.
- **Conversational.** Write like a friend telling a story: contractions, short sentences (6–20 words), questions, "okay, so", "here's the thing", "think about that". Never write encyclopedia prose.
- **The picture changes every 2–3 s.** Keep `say` short (1–2 sentences) and use 10+ different images.
- **Ending.** The agent adds the subscribe scene (the button gets clicked on screen) to long videos, and a "full story on my channel" banner to the end of Shorts. The Short's description links to the long video automatically. Your last long scene should ask a comment question.

## 2c. Viewer score — must pass 85/100

- Run `python3 cloud/ink/check.py cloud/ink/animals/NNN-slug.json`. It must print `O'TDI`, with long and short both ≥ 85.
- Then review once more by hand with `cloud/ink/tomoshabin-bahosi/SKILL.md`, as a bored phone viewer. Rewrite every line where you would swipe.
- The PC agent re-scores after rendering. It refuses to upload anything under 85.

## 3. Length

- The long video needs **1,250–1,600 words** in `scenes`. That is about 8–11 minutes; 8+ minutes allows mid-roll ads.
- Use 45–70 scenes.

## 4. Facts and honesty (non-negotiable)

- Every number must come from a source you actually read in this run. List them in `sources` with a URL or DOI.
- Hedge where science is unsure ("researchers estimate", "up to").
- Never invent studies, quotes or numbers.
- No gore descriptions, no cruelty, nothing that encourages harming animals.

## 5. Images

- `img` = exact English Wikipedia article title. The agent uses that article's lead photo, and only if it is CC/public-domain licensed. It redraws the photo as an ink sketch.
- Use common article titles that have good photos, for example "Lion", "Spotted hyena", "Great white shark", "Full moon".
- Avoid titles whose lead image is a map or diagram.
- Reuse an image across consecutive scenes; the camera moves anyway.
- 8–15 different images per video is ideal.

## 6. JSON format

```json
{"id": "NNN-slug", "title": "≤70 chars, curiosity + clear subject", "thumb_text": "2-3 WORDS",
 "description": "2-3 sentence hook paragraph", "tags": ["..."], "sources": ["Author (year) Title — URL"],
 "scenes": [{"img": "Lion", "hook": "What happens here after dark?", "say": "..."},
            {"img": "Lion", "label": "Up to 20 hours", "say": "..."},
            {"img": "Hippopotamus", "num": "#5", "label": "...", "say": "..."}],
 "short": {"title": "≤60 chars", "header": "short topic line", "description": "...",
           "scenes": [{"img": "Full moon", "hook": "...", "say": "..."}, {"img": "...", "say": "..."}]}}
```

Optional `label` (2–5 words) is handwritten under the picture in the long video.

## 7. Checklist before pushing

- `python3 cloud/ink/check.py <file>` prints O'TDI.

- The file parses: `python3 -c "import json;json.load(open(F))"`.
- Word counts are in range. The `id` matches the filename.
- The commit contains only the new file. Push it to `main`.

## Ask Studio advice (2026-10-20, from this channel's old Shorts)

- 67% of viewers swiped away within 2 s. The first frame and the first sentence are everything.
- First frame: high contrast; `hook` is **≤ 5 words** if you can (e.g. "NOT FRIENDS?", "WHO WINS?").
- Titles: curiosity or tension, with the animal names in the first 40 characters.
- Shorts: every Short ends with a CTA. The renderer keeps captions and banners out of the bottom 20% and the right edge, where YouTube's UI covers them.
- Subscriber conversion was only 0.05%. Give viewers a reason to come back: a series feel ("Part of the Wild Sketchbook"), and a question that the next video answers.


## Growth plan 2026-10-28 — see cloud/growth/PLAN.md (Wild Sketchbook section)
- Move weight from "X vs Y: who would win?" fights to curiosity explainers ("This Animal…", "What Happens If…") — fights risk YouTube's July 2026 "distressing content" rule.
- Short: key fact at frame 0 + bold subtitle; every title unique; mid-video CTA "subscribe for one animal secret a day".

## Competitor format 2026-10-28 (KO MATION 9.8M, Creature Challenge — applies from the next script)
**Phone verification (checked in Studio 2026-10-28):** verified = Roblox, Calm Rain, Max, Doodle Desk. NOT verified = Hollowmere, Dough Bros, Wild Sketchbook, Money Story, Funny Rank, Inspector Bolt, Seoul Night Remix, Milo Survives → on these channels no video may be longer than **14:50**, and no custom thumbnails / Related-video links (they fail). Re-check in Studio → Settings → Channel → Feature eligibility before making anything longer.
- Long ink videos: weekly 4–8 min "tournament / battle royale" with an 8–16 animal bracket (famous animals: lion, tiger, gorilla, grizzly, hippo, croc, great white, orca), max 14:50. Not fact explainers (0 views).
- Strong angle in titles: "…Is A LIE", "NOT EVEN CLOSE". First frame: both animals charging + "WHO WINS?".

## Studio AI 2026-10-29 (Ask Studio, rebuilt from the daily analysis — the run's own patch could not be pushed) — applies from the next run
- Shorts: frame 0 already shows the fact or the number (no build-up), and every title is checked against the channel's existing titles so none is repeated.

## Competitor lessons 2026-11-07 (daily competitor run — cloud/growth/competitors/2026-11-07.md) — applies from the next script
- **"N animals that could beat ONE famous animal"** list is this week's fastest drawn-animal format (68k-sub channel: 73k views in 2 days, 8 min). Write one per week as the long: famous animal in the title's first 25 chars + a number ("6 Animals That Could Beat a Gorilla — and Why"). Compare by real measurements (bite force, weight, speed) — no blood, no injury close-ups.
- Frame 0 / first scene = a **grid of all the inked animals with a 1-word label under each** + 3–4 caps words ("GORILLA vs 6?"). It reads at phone size and matches our ink style.
- Give the explainers a **numbered series name** in the description's first line and the playlist ("Animal Secrets #12"), not in the title (Ask Studio 2026-11-07 says title formulas confuse viewers). Count from the existing titles in `cloud/ink/animals/`.
- **Ask Studio 2026-11-07 (Wild Sketchbook, 28 days: CTR 1.45 % on 20.9k impressions, long avg view 1:02 = 13 %, +5 subs from 70 uploads):** NO title tails like "#1 Is New" / "#1 Is in You" — write one clear curiosity title ("How Crocodiles Survived the Asteroid That Wiped Out the Dinosaurs"). Shorts titles must each be a different hook — never "The #1 Secret: X | Topic" again. First 5 s of the long = the main visual + the promise; no slow context.
- "What if <animal> evolved…?" speculative stories also get pushed (56k-sub channel, 55k in 6 days) — allowed once a week, clearly framed as "what if" (not as fact).

## Competitor lessons 2026-11-08 (cloud/growth/competitors/2026-11-08.md)
- **Second-person "What if YOU could…?" questions** are the fastest drawn-animal outlier this week (916-sub channel: 49k views in ~1.5 days, 15 min). Once a week the "what if" long is written to the viewer: "What If You Could <power> With <animals>?" — clearly framed as imagination, our own animals and scenes.
- Tags for that video = 5–7 wordings of the same question ("what if you could …", "if animals could …", "<animals> …"), not generic "animals".
- Frame 0 for it: our inked scene + **2 caps words as a command or reaction** (e.g. "RUN NOW!"), not the title repeated.

## Safety notes 2026-11-07
- No restrictions on any video. Risk o'rta only for sameness: Shorts titles "The #1 Secret: X | Topic" repeat — every Short title must be a different sentence shape (repetitive-content rule).

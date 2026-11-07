# Daily YouTube Studio analysis: "why are videos not shown" + Ask Studio + fixes

The owner asked for this on 2026-10-27/28 and extended it on 2026-11-07:
- Check every channel every day.
- Find what to change and why videos are not being shown.
- Apply the fixes without asking him.
- Put the results in his "Agentlar markazi" app.

Channels, browser and hard rules: see `cloud/growth/CHANNELS.md`.

**Goal:** get as many channels as honestly possible into the YouTube Partner Program before ~15 Jan 2027 (the thresholds double on 1 Feb 2027).

**Biggest risk:** YouTube's July 2026 "inauthentic content" rule. Template-like, near-identical, mass-produced videos are not monetized.

## Step 0: read first

- cloud/growth/PLAN.md
- the newest cloud/growth/ask_studio_<date>.md
- the newest cloud/growth/competitors/<date>.md (the competitor research runs at 07:17 Bishkek)
- cloud/results/*/status.json and the result files

## Step 1: why videos are not shown (every channel)

1. Open Studio Analytics:
   - `https://studio.youtube.com/channel/<ID>/analytics/tab-reach_viewers/period-default?authuser=<n>`
   - `.../tab-content/period-default`

   Switch between Videos and Shorts where the page offers it.
2. Read with get_page_text, for the last 28 days and the last 7 days:
   - impressions
   - impressions click-through rate
   - traffic sources (Browse, Suggested, Shorts feed, Search, External, Channel pages)
   - top YouTube search terms
   - for Shorts: "stayed to watch" / "viewed vs swiped away"
   - average view duration and % viewed
   - subscribers gained per video
3. Open the analytics of the 3 newest videos (`.../video/<VIDEO_ID>/analytics/tab-reach_viewers/period-default`) and compare them with the channel's typical video.
4. Diagnose the cause in plain words:

   | What the numbers show | Likely cause |
   |---|---|
   | Few impressions (YouTube is not testing the video) | topic, title, tags, first frame, or irregular uploads |
   | Impressions but low CTR | thumbnail or title |
   | Clicks but low retention | hook, pacing or length |
   | Shorts swiped away | weak hook in frame 0 |
   | Other cases | only one traffic source; search terms we don't target; video still processing or restricted; Made for Kids limiting reach |

Never invent numbers. If a page does not load, say so.

## Step 2: Ask Studio (every channel)

1. Open `https://studio.youtube.com/channel/<ID>?authuser=<n>`, wait ~6 s, and check `#entity-name`.
2. Click the button whose aria-label is "Ask Studio" (Russian UI: "Спросить у Студии") with JavaScript, then wait ~3 s.
3. Focus the contenteditable question box. Type with the computer tool's `type` action and press Enter (never ctrl+a).
4. Wait ~30–35 s, then read the answer from `document.body.innerText` after the question.

The question is always the same:

"What problems is my channel having right now? Look at my analytics for the last 28 days and list the top 3 problems that hurt my views, watch time and subscribers (with the numbers), why my recent videos get few impressions, and tell me exactly what to fix first in my videos, titles, thumbnails, Shorts and upload schedule. Answer in English."

If there is no Ask Studio button (Dough Bros), use the Analytics numbers only. Never invent an answer.

## Step 3: save

1. Write `cloud/growth/ask_studio_<YYYY-MM-DD>.md`. For each channel include:
   - key numbers
   - the "nega ko'rinmayapti" diagnosis
   - top 3 problems
   - fixes
2. Compare with the previous file and with today's competitor research.
3. Commit and push.

## Step 4: fix (every channel gets attention every day)

For each channel, make at least one change that targets today's diagnosis. It can also come from an open PLAN.md item or a competitor lesson.

Priority-1 channels (funny, roblox, hollow, ufc) get up to 3 changes a day.

Each change must be small and safe, made in one of:
- maker code
- writer rules
- AGENT.md
- title, description, tag or thumbnail rules
- hook rules
- slot times in cloud/channels.json

After each change:
1. Run `python3 -m py_compile` on every edited Python file.
2. Tick the item in PLAN.md as `- [x] … (done YYYY-MM-DD: what, file)`.
3. Add new `- [ ]` items for new problems.

Then commit and push (`git pull --rebase` on rejection). The laptop worker pulls automatically.

## Step 5: hub report

Use ArtifactData with url https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r.

1. Get `analysis/latest` (pin if_version).
2. Set it to the object below. Keep the other existing fields, such as `competitors`.

```
{"at": ISO now, "date": "YYYY-MM-DD", "goal": 95, "summary": "<3–4 Uzbek (Latin) sentences>", "revenue_total": n|null, "studio_note": "<one Uzbek line>",
 "channels": {"<key>": {"name", "views7", "impressions7", "imp_ctr", "traffic": "<top sources>", "viewed_pct", "avg_pct", "ctr", "watch_hours", "subs", "revenue", "per_day",
   "why_not_shown": "<one Uzbek sentence>", "verdict": "<one Uzbek sentence>", "problems": [], "fixes": ["what changed today"],
   "studio_ai": {"date", "problems": [], "fix": []}, "plan_left": n}},
 "actions": ["<each change, Uzbek, with file>", "Siz: <owner to-do>"]}
```

3. Also set `analysis/<date>`.
4. Add `history/<YYYY-MM-DD>` = `{"date", "at", "ch": {<key>: {"subs", "views", "videos"}}}` if it does not exist yet. Take the numbers from Studio.

## Final message

A short Uzbek message for the owner's phone, 4–8 lines:
- One line per priority-1 channel: the number vs yesterday, why it is or isn't shown, and what was done.
- One line for the rest together.
- Studio AI's biggest problem today.
- Only if needed: what the owner must do himself.

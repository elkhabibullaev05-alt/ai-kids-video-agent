---
name: video-retention
description: Predict how far people will watch a video before it is uploaded. Gives a second-by-second retention curve, average % viewed, Shorts "stayed to watch" (did not swipe), and a verdict on whether YouTube is likely to recommend it, with timestamped reasons and the exact settings to change. Use for every Short or long video before upload, when the owner asks "nechchi foiz ko'riladi", "recommend chiqadimi", "qayerda tashlab ketishadi", "retention", "stayed to watch", or when Studio shows low views.
---

# Video Retention: will people watch it, and will YouTube push it?

YouTube decides whether to recommend a video mostly from two numbers:
- **Shorts:** *Stayed to watch* (the share of people who did not swipe away in the
  first moments) and *average % viewed* (loops count, so a good Short can be over 100%).
- **Long videos:** *average % viewed* / average view duration and how flat the curve is
  in the first 30–60 seconds, plus click-through rate on the thumbnail.

This skill estimates those numbers **before** upload by looking at what a viewer gets
every second: is something moving, did the shot change, is this footage repeated, is it
silent, is it too quiet. It is a heuristic predictor, not YouTube data. Say so in
reports. Calibrate it against real Studio numbers (section 5).

## 1. Run it

```bash
python3 <skill_dir>/scripts/retention.py VIDEO.mp4 --title "Max sees SNOW for the first time" \
        --json /tmp/ret.json --png /tmp/ret.png [--kind short|long] [--calib cloud/growth/retention_calib.json]
```
- `--kind` is auto: vertical and ≤ 3 min is treated as a Short.
- Read `/tmp/ret.png` (the curve) with the Read tool, and run the **video-watch** skill on
  the same file so you can see *why* the curve drops where it does.

Output fields:
| Field | Meaning | Good Short | Good long video |
|---|---|---|---|
| `stayed_to_watch_pct` | estimated % who don't swipe at the start | ≥ 70 | n/a (≈ "first 30 s" retention) |
| `avg_viewed_pct` | average % of the video watched, one pass | ≥ 80 | ≥ 45 |
| `avg_viewed_pct_with_loops` | with some re-watches for loopable Shorts ≤ 60 s | ≥ 90 | — |
| `retention_at` | % still watching at 3 s, 5 s, 10 s … | 3 s ≥ 70 | 30 s ≥ 70, 60 s ≥ 60 |
| `score_0_100` | combined | ≥ 85 | ≥ 85 |
| `verdict` | RECOMMEND CHIQISHI EHTIMOLI YUQORI / O'RTA / RECOMMEND CHIQMAYDI (+ reason) | | |
| `problems` | timestamped causes: repeats, frozen frames, silence, low volume, static start, wrong aspect | | |

The thresholds are creator rules of thumb for 2026, not official YouTube numbers.

## 2. Think like the viewer, then decide

Numbers are the start, not the answer. For every drop in the curve:
1. Look at the frames at that time (video-watch sheets).
2. Ask: "As a <target viewer> on a phone, why would I leave right here?"
3. Write the fix as a concrete edit (what to cut, add or reorder, at which second).

Decision rule before upload:
- `verdict` RECOMMEND… YUQORI and score ≥ 85 → upload.
- O'RTA → fix the top 1–2 problems (usually the hook or a repeat), re-render and re-run.
- RECOMMEND CHIQMAYDI → do not upload as is. Fix it, or log it in
  `cloud/rejected/<ch>/<job>.reason.json` with the problems list.

## 3. Fix table: symptom → setting to change

| Problem in report | What viewers feel | Fix (where) |
|---|---|---|
| static start / no sound at 0:00 | "nothing's happening" → swipe | Start mid-action. Voice at 0.0 s. Put a 3–5 word text hook on frame 1 (maker's hook/beat-1 settings). |
| `takroriy kadrlar` | "I've seen this" → swipe; also YouTube's repetitive-content risk | Remove the repeated range (`video-polish --cut A-B`) or replace it with a new beat. Shorts: never pad a 5 s clip to 15 s. |
| `qotib qolgan kadr` (still) | boredom | New visual every 2–3 s (Shorts) / 4–6 s (long): punch-in zoom, cutaway, number badge. |
| `sukut` | dead air feels broken | `video-polish --trim-silence`, or add narration/SFX there. |
| `ovoz past` | viewer turns it off | `video-polish` normalises to about −14 LUFS. |
| Short not 9:16 | small, letterboxed | Re-render 1080×1920, or `video-polish` (blurred-fill, no stretching). |
| long video curve falls fast in 0–30 s | the intro is slow | Cut the intro, show the payoff first, and promise the best part for the end. |
| curve OK but ends low | the ending drags | End right after the payoff. For a Short, make the last frame flow into the first so it loops. |
| title > 60 chars | weaker click | Short curious title ≤ 50 chars, a question or a number. |

## 4. Worked examples (real files in the repo, 2026-11-11)

**A. `cloud/ready/maxcat/20261026-first-snow.mp4`, Short, 15 s**
```
stayed_to_watch 70% | avg viewed 57% | score 70 | RECOMMEND CHIQMAYDI (oxirigacha ko'rishmaydi)
problems: 0:05-0:15 takroriy kadrlar
```
Viewer view: the first 5 s are lovely, then the same clip plays again with "Watch his
face again…". I leave at about 0:07. Fix tested: `video-polish --cut 5-15.2 --look warm`
gives a 5 s loopable Short, avg viewed 57% → 68% (84% with loops), score 70 → 83,
verdict O'RTA. To reach "yuqori", the second half needs a new beat instead of the
replay (a snowflake lands on his nose and he sneezes).

**B. `cloud/ready/maxcat/20261026-ep1-market.mp4`, Short, 23 s**
```
stayed 70% | avg 62% (75% with loops) | score 79 | O'RTA
problems: 0:21-0:24 deyarli qotib qolgan kadr, 0:21-0:24 sukut
```
Fix: the last 3 s are a frozen, silent end card. Trimming them (`--cut 21-23.2`) only
moved the score 79 → 80, because the main loss is the steady drift through the
middle. The real fix is a stronger re-hook around 0:10 (new place, new problem) plus a
last frame that loops to the first.

**C. `cloud/ready/grind/20261026-most-satisfying.mp4`, Short, 45 s**
```
stayed 70% | avg 36% | score 59 | RECOMMEND CHIQMAYDI
problems: three repeated ranges (0:05-0:15, 0:20-0:30, 0:35-0:46), silence at 0:20, audio −35 dB
```
After `video-polish --trim-silence --cut 35-46 --look vivid`: 34.5 s, −15 LUFS, avg
viewed 43%. Better, but still repeats, so it needs new clips, not only polish. Also
note the visible "PixVerse.ai" watermark: a reused-content and branding risk.

## 5. Calibrate with real Studio numbers (makes it smarter every week)

After a video has been live 48 h, open Studio → the video → Analytics → Engagement and
note *Stayed to watch* (Shorts) or *Average percentage viewed*. Compare with the
prediction you saved in `cloud/results/<ch>/<job>.json` (`pred_stayed`, `pred_avg`).
Keep `cloud/growth/retention_calib.json` per channel or globally:
```json
{"swipe_mult": 1.0, "hazard_mult": 1.0, "n": 0, "updated": "2026-11-11"}
```
- If real stayed-to-watch is lower than predicted by more than 5 points on average over
  ≥ 5 videos, raise `swipe_mult` by 0.1 (lower it if real is higher).
- If real avg % viewed is lower than predicted, raise `hazard_mult` by 0.1 (and the
  other way round).
- Never change both by more than 0.2 per week. Write what you changed and why in the file.

## 6. Report format (Uzbek, for the owner's phone)

```
📈 <file>: ~<avg>% ko'riladi (loop bilan ~<x>%), swipe qilmay qoladi ~<stayed>% — <verdict>
Tashlab ketish joylari: 0:05 (takror), 0:21 (qotib qolgan kadr)
Sozlash: 1) --cut 5-15  2) birinchi kadrga "WAIT FOR IT" matni  3) ovoz -14 LUFS
(Bu bashorat; haqiqiy raqam 48 soatdan keyin Studio'da.)
```

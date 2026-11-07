# Ask Studio — 2026-11-07 (scheduled run)

**Result: not asked on any channel.** This run started in the cloud with no link to the owner's computer, so the Claude in Chrome tools
(the owner's signed-in Chrome) were not available. Ask Studio and Studio Analytics both need that browser. No answers or numbers were invented.

All 12 channels (roblox, sleep, max, ufc, seoul, milo, hollow, dough, doodle, bolt, money, funny): not asked.
4th scheduled run in a row without Studio access (2026-10-31, 11-01, 11-06, 11-07). Latest real Studio answers: `ask_studio_2026-10-27.md` (+ 10-29 notes in PLAN.md).
Compare the next real run against those.

## What the repo shows instead (cloud/results, 2026-11-07 ~02:45 UTC)
- funny: quota_wait, 3 pending uploads · ufc: quota_wait, 1 pending · bolt: quota_wait, 3 pending — YouTube daily upload quota is the bottleneck.
- hollow: **queue empty** (writer has not refilled it).
- roblox: idle (pack done) · sleep: uploading 1 · money: 4 queued · maxcat: 2 queued · doughbros: 1 queued.
- grind (Grind_video): error "no token" since 2026-11-06.
- Hollowmere titles still carried "(Ep N)" against Studio's 10-29 advice — fixed in the worker today.

## Fix
Open this scheduled task in the Claude desktop app on the new laptop and turn on "Require this computer", so the run can use Chrome.

---
# Update — same day, laptop run with the owner's Chrome (~08:40 UTC): priority-1 channels done

Numbers from Studio Analytics, last 28 days (9 Oct – 5 Nov). Ask Studio question as in STUDIO_DAILY.md.

## roblox — Roblox Top 10 Daily
- 38K views (+107 %), +48 subs. Shorts = 89.5 % of views; Shorts feed 81.2 %, search 17.7 %; stayed to watch 38.5 %.
- Long videos: 98K impressions, **CTR 2.5 %**, 4.4K views, **avg view 0:38** (12 %).
- Nega ko'rinmayapti: long videos ARE shown (98K) but few click and viewers leave in 30–40 s; Shorts lose 61 % in the first seconds.
- Studio AI top 3: low long CTR 2.45 %; drop-off (0:38, "Top 20" holds 28 s of 11 min); Shorts 38 % stayed. Fix: no "#36"/episode titles, curiosity titles, 2–4 big words + one character on thumbnail, payoff stated in 5 s, Shorts 15–25 s, separate long and Shorts uploads, audience peak 13:00–18:00 MSK → post long ~12:00–13:00 MSK.
- Changed: long slot 17:45 → 09:45 UTC (channels.json); angle titles (competitor run). PLAN: Shorts 15–25 s.

## funny — Funny Rank Daily
- 83.2K views, 32.7K engaged, +66 subs. Shorts feed 95.4 %, search 4.1 %; stayed to watch 37 %. Top: "Ranking Crazy Trampoline Fails" 6.7K.
- Ask Studio: **not asked** — Studio showed a "prove it's you" identity check on this account; Claude does not do sign-in checks. Owner must pass it once.
- Nega ko'rinmayapti: Shorts feed tests them, but 63 % swipe away → frame 0 / first words.
- Changed: outcome-first titles + tags (competitor run).

## ufc — Wild Sketchbook
- 9.6K views, 3.1K engaged, +6 subs. Shorts feed 84.2 %, search 15.1 %; stayed 33 %.
- Studio AI: CTR 1.45 % on 20,851 impressions (long 1.70 %); long avg 1:02 of 7–8 min (13.3 %), 2 h 33 m long watch time; 70 uploads → +5 subs. Newest long: 6 impressions, 0 clicks in 10 h. Fix: one clear focal point + 2–4 words on thumbnail; drop "#1 Is New" title tails; hook in 5 s; distinct Shorts titles; link Shorts to longs; fewer uploads (1 long/week + 2–3 Shorts); audience peak 14:00–19:00 local, Saturdays.
- Changed: WRITER_INK.md (no "#1 Is…" tails, distinct Shorts hooks, series name in description). Fewer uploads → owner question (never cut automatically).

## hollow — Hollowmere Tales
- 6,395 views (Shorts 6.3K = 97.9 %, long 134), +3 net subs, 839 new / 4 returning viewers. Traffic: Shorts feed 93 %, search 5 %.
- Long: 7.2K impressions, **CTR 1.0 %**, avg view **0:18–0:23** of 3–4 min (~10 %). Shorts stayed 7–19 %.
- Studio AI: long CTR 0.98 %; retention drops to 15 % by second 12 ("Where Did Hamelin's 130 Children Go?"); 4 returning viewers. Bursts (5 long + 6 Shorts on 5–7 Nov) compete. Fix: steady schedule (1–2 long/week, 1 Short/day), thumbnails without 8–12 words of subtitle text, no episode numbers, mystery in first 40 chars, hook in 5 s, end with a bridge to another story, link Shorts to longs.
- Changed: WRITER.md title tail " | True Story Animated" + search tags (competitor run). PLAN: subtitle-free auto-frame / phone verification. Fewer uploads → owner question.

## Other 8 channels
Not checked today (time) — next run. Part C (SAFETY_DAILY.md) also left for the next run, as COMPETITORS.md allows.

---
# Update 2 — same day ~10:00 UTC (owner: "hamma narsani sen qil, hozir"): the other 8 channels + Funny Ask Studio

## funny — Ask Studio now worked (no identity check this time)
- 83,284 views, 155 h, +50 subs (1 per 1,665 views). Stayed 37 % (Duck Moments 24.5 %, Zipline 26 %); best "Ranking Crazy Trampoline Fails" 60 % stayed, **18 s long**. Avg 14 s of 31 s (52 %).
- Fix: Shorts 15–20 s; no title card; titles less formulaic ("Ranking … (Wait for #1)"); on-screen/pinned question "Which was worse: #3 or #1?".
- Changed: `cloud/makers/funny/fr_render.py` — #5–#3 shots 3.0 s, #2 3.6 s, slow-mo replay only on #1 → ~21 s instead of ~31 s (rek_ball still gives full length score 15–45 s). Could not render-test here (no kokoro TTS in the cloud box) — the laptop worker's self-check gates it.

## sleep — Calm Rain for Sleep
- Shorts 1.9K views (77 %), long 592; 230 h watch time; +3 subs; impressions 5.6K, CTR 2.9–3.1 %, avg 4:59 from impressions; Shorts stayed 12 %.
- Studio AI: dark, identical thumbnails; repeated titles; Shorts lose 90 % in 1–2 s; uploads clustered; best video "Gentle Night Rain… 60 Minutes" avg 32 min.
- Changed: `cloud/makers/sleep.py` thumbnail brighter/more contrast and the badge names this video's scene (not "RAIN FOR SLEEP" every time). Fewer uploads → owner.

## max — Max the Curious Cat
- 186.3K impressions, CTR 0.9 %, avg 0:34 (12.6 %); 4,114 views, +3 subs; Shorts 14 % stayed. 97 % of impressions from Suggested.
- Changed: worker strips "(Ep N)" for maxcat too (`cloud/worker.py studio_title`); WRITER.md: one emoji, start inside the problem, Max's face ≥ 1/3 of thumb, Shorts 15–20 s.

## seoul — Seoul Night Remix
- 622 views, 5.2 h, +1 sub, 9 uploads; long CTR 3.49 % on 6,272 impressions; Shorts 15 % stayed.
- Changed: `seoul/AGENT.md` title order [Vibe/Setting] • [Genre] (Song), neon thumbnails, Shorts start on the hook.

## milo — Milo Survives (since 22 Oct)
- 2.3K views, 0 subs; long 1,902 impressions, CTR 1.74 %; "Zombie Hospital" avg 1:03 of 7:46, 37 % lost by 20 s.
- Changed: `milo/AGENT.md` danger in first 3 s, first-person titles ≤ 55 chars.

## dough — Dough Bros (no Ask Studio button; Analytics only)
- Shorts 9.9K views, long 4K; +21 subs; 147.8K impressions, CTR 2.0 %, avg 0:34.
- Changed: WRITER.md note (object + problem in second 1).

## doodle — The Doodle Desk
- Shorts 3.6K, long 649; +2 subs; long 12K impressions, CTR 1.37 % (Suggested 0.98 %); avg 1:47–2:07 of 10 min.
- Changed: `doodle/AGENT.md` stakes-not-names titles, conflict in 10 s.

## bolt — Inspector Bolt
- 2,797 impressions, CTR 1.36 %, 67 views, avg 0:15 (7 %), 0 subs (since 18 Oct).
- Changed: WRITER.md bolt note (problem in second 1, one big face).

## money — Money Story Daily
- 2,125 views (all Shorts), 0 subs, 35 uploads; Shorts 11 % stayed; avg 17 s of 40–55 s; drop between s4–s8.
- Changed: `cloud/makers/money/WRITER.md` punchline number first, 25–30 s scripts, subscribe line at the end.

**Studio AI's message on almost every channel: post less (1–2 long/week).** Not applied — owner's rule: never lower per_day automatically.

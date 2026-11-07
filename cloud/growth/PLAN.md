# Growth plan — every channel, 28 Oct → 31 Jan 2027 (owner: "hammasini qil, hammasiga alohida e'tibor")

Source: the owner's guide (Claude Docs, 28 Oct 2026), YouTube Studio AI answers of 27 Oct (`ask_studio_2026-10-27.md`), competitor research.
**Deadline: apply for YPP before ~15 Jan 2027** (thresholds double on 1 Feb 2027: 8,000 h or 20M Shorts views).
**Owner 2026-10-28 02:14: "kamaytirma, vdni sifatini yaxshila" — never lower the number of uploads; keep the old daily counts and put the effort into quality.**
**Owner 2026-10-28 02:18: if Studio AI says to upload fewer videos, do NOT cut anything yourself — put it in the report as "Studio: <kanal> uchun videoni kamaytirishni tavsiya qilyapti (<raqamlar>) — qaror sizda" and the owner decides. Every other Studio fix (titles, thumbnails, hooks, quality, timing) is applied automatically as usual.**
**Phone verification (checked in Studio 2026-10-28):** verified = Roblox, Calm Rain, Max, Doodle Desk. NOT verified = Hollowmere, Dough Bros, Wild Sketchbook, Money Story, Funny Rank, Inspector Bolt, Seoul Night Remix, Milo Survives → on these channels no video may be longer than **14:50**, and no custom thumbnails / Related-video links (they fail). Re-check in Studio → Settings → Channel → Feature eligibility before making anything longer.
**Biggest risk:** YouTube's July 2026 "inauthentic content" rule — template-like, near-identical, mass-produced videos are not monetized. Every channel: same number of videos, each clearly different and better made; a human layer in each (own commentary/narration, chapters, story).

The daily Studio analysis run reads this file, works on **every channel every day** (at least one item each), ticks items off here (`- [x] … (done YYYY-MM-DD: what)`), and adds new items when Studio finds new problems. Weekly review measures each channel against its target.

Shared rules for every video: frame 1 = motion + big text hook (no logo/fade/title card); title < 50 chars, unique, no "Ep N ·"/channel-name prefix; thumbnail = one face/subject 35–50 % of frame + ≤ 3 words; something changes every 3–5 s; Shorts 15–45 s cut from a long video, loop ending, linked to the long ("Related video" once the account is phone-verified, until then "Full video:" link in description); Shorts ≈ 25–40 % of uploads; uploads spread 6–8 h apart; AI disclosure on when AI visuals/music are used.

---

## Priority 1 — Funny Rank Daily (`funny`, local `funnyrank`)
Now: 40 subs, ~2,000 views/day, Shorts stayed 35 %. Target 31 Jan: 1,000 subs + 10M Shorts views (90 d) → full YPP.
- [x] ~~Titles: challenge/curiosity patterns~~ — superseded 28 Oct by competitor data: "Ranking Best <object> Fails" wins (see below).
- [ ] Frame 1: the peak of the funniest clip + bold question on top; cuts between clips < 0.2 s; last 2 s "#1 or #2? Comment" / "Subscribe for daily rankings".
- [ ] Own commentary layer on every video (ranking reason captions per clip) — reused-content protection; CC BY credits stay.
- [ ] Keep 3 Shorts/day (config per_day 3), spread evenly through the day (no bursts).
- [ ] Weekly 8–10 min horizontal "Funniest moments of the week" compilation (long watch hours) — start this week, not 7 Nov.
- [ ] (competitors 28 Oct) Clip fills the full 1080 width (no blurred side panels) — like BananaComedy/Snap Ranks (13M/46M-view rankers).
- [x] (competitors 28 Oct) Drop the AI voice-over over clips (or only "Number 3…"); keep the clip's own audio/laughs. (done 2026-11-07: voice now only says "Number three!"/"And number one!"; reaction line stays as on-screen caption, clip audio carries the rest — cloud/makers/funny/fr_themes.py script())
- [x] (competitors 28 Oct) Empty 1–5 list that fills on each reveal, #1 last ("Wait for #1"); total 25–35 s; first clip at 0 s. (done 2026-11-07: verified in cloud/makers/funny/fr_render.py — intro = #1 peak with "WAIT FOR #1", list fills #5→#1, end "#1 OR #2?")
- [x] (competitors 28 Oct) Titles: "Ranking Best <specific object> Fails" (trampoline, pool, treadmill) — our "Ranking…" titles already win; drop "Which…". (done 2026-11-07: verified — cloud/makers/funny/fr_themes.py TITLE_PATTERNS are all "Ranking …", no "Which…")

- [x] Retention fix 28 Oct 18:40 (owner "ishla shu ustida"): rank.py now rejects off-topic clips (a "how to draw a cat" tutorial was #4 in "Cat Fails"), needs a funny/fail word in the clip title, prefers 720p+ and 2016+ clips, no duplicate labels ("Cat Chaos" x3). Backup rank.py.bak_20261028d.
- [ ] Next: measure "stayed to watch" for Shorts made after 28 Oct 19:00 vs before (Studio → Content → Shorts) in the daily run.

## Priority 1 — Roblox Top 10 Daily (`roblox`, local `robloxtube` + repo `roblox/` Blocky Quest)
Now: 94 subs, ~1,400 views/day, long AVD 38 s, 142 near-identical titles in 28 days. Target: 1,000 subs + 4,000 h.
- [ ] Long videos start at 0:00 in gameplay with the #20 entry (no intro/title card); 25–30 s per entry with on-screen stats.
- [x] Kill the templates "Best Roblox Games to Play Right Now", "Is X Worth Playing in 2026?", "Have You Played X?"; use this-week angles ("Did Steal An Egg Just Pass MM2?"). (done 2026-11-07: long titles now try day-specific angles first — "Can B Beat A?…", "A Just Took #1…", "Why Is <climber> Suddenly Blowing Up…" — template list only as fallback; cloud/makers/roblox/rbx_text.py long_titles())
- [ ] Thumbnails: A-vs-B split or one high-contrast moment + 2–4 words ("NEW #1?").
- [x] Volume stays 1 long + 5 Shorts/day (owner 28 Oct: "kamaytirma") — every Short a different game/angle, no repeated title template.
- [x] Black/OBS backgrounds fixed 28 Oct (news.py no longer reads ~/Videos OBS recordings); 7 broken scheduled videos made private; ep0034 re-made with game images (checked frames OK).
- [ ] Long intro card: "BORED? 20 ROBLOX GAMES TO PLAY" wraps into the subtitle line — shorten to f"BORED? TOP {n_long} ROBLOX GAMES" in agent/news.py (title_card call). Do it only when state.json "pending" is empty (no upload running — a restart mid-upload risks duplicates).
- [x] 29 Oct (owner): Blocky Quest kids 3D STOPPED on this channel for good — worker `ready_only`, kids=false, queue moved to cloud/hold/roblox, its 3 uploads (oi9Cfu6D1Q4, 6Xb5U6n5FFk, kVwK2l79GqI) listed in channels.json `unpublish` → made private as soon as the roblox token is re-made with cloud/auth.py.
- [ ] Teen/adult only (13+, Made for Kids = NO on every upload and as the channel default in Studio → Settings → Channel → Advanced). On the PC check robloxtube config/uploader: made_for_kids false, and Studio default audience = "No, it's not made for kids".
- [x] (competitors 28 Oct) Hook names a pain point ("Bored of the Roblox homepage?"), game #1 within 10 s — like FrostyBlox (1.1M) / HoneySaw. (done 2026-11-07: "Stay to the end…" hook replaced by "Not sure what to play on Roblox today?…"; all non-gainers hooks now open on a pain point or the #1 number — rbx_text.py hook_script())
- [ ] (competitors 28 Oct) Real gameplay/trailer clips per game + one line on what you DO in it (not still images + visit counts).
- [ ] (competitors 28 Oct) Evergreen long series "N Roblox Games To Play When Bored (2026)", N rising each time; Shorts "The SCARIEST/most FUN Roblox Game To Play With Friends".
- [x] (competitors 28 Oct) Thumbnail: sad/shocked avatar + one huge word ("BORED?") or big #1/#3/#10 over game shots. (done 2026-11-07: added "BORED? / PLAY THESE" to the thumbnail word sets next to the big #1 icon — cloud/makers/roblox/rbx_long.py thumbnail())

## Priority 1 — Hollowmere Tales (`hollow`, repo `hollow/`)
Now: 3 subs, ~540 views/day, long CTR 1 %, Shorts stayed 13.6 %. Model: Mr Nightmare (7.2M subs, 20–30 min "3 TRUE … Stories" compilations, 99 % long).
- [x] Halloween: a 14:50-max compilation "3 TRUE Halloween Stories That Still Have No Answer" (channel not verified) published by 31 Oct 21:00 UTC (re-cut from existing episodes + narration bridges). (done 2026-10-28: "4 TRUE Halloween Stories With No Answer", 13:59, eps 26/32/34/35 + cold open + bridges, chapters, scheduled 31 Oct 20:15 UTC, id cSM2-ob1xyM)
- [ ] Every week 1–2 compilations "3 TRUE <setting> Stories" (night shift, new house, highway, school) 15–25 min — the long-watch-hours engine.
- [x] Titles without "Ep N ·"; thumbnail = one scared face / dark doorway + 2 words. (done 2026-11-07: the writer still added "(Ep 50)" to every title; worker now strips it for hollow (cloud/worker.py studio_title) + cloud/WRITER.md "hollow — overrides 2026-11-07")
- [ ] Shorts open on the shock line; each points to its compilation.
- [ ] (competitors 28 Oct) Titles "3 Terrifying TRUE <setting> Mysteries" / "… To Fall Asleep To" (Mr Nightmare 1.4M, Mortis Media) — no serial "Ep N".
- [ ] (competitors 28 Oct) Thumbnails dark realistic image (fog, window, shape in doorway) + 2–4 big words; no cartoon bobble-head figures (reads as kids, CTR 1 %).
- [x] (competitors 28 Oct) Stories standalone (no "last night the pale shepherd…" dependency); open with date + place + strangest fact; subscribe line mid-video, not at start. (done 2026-11-07: cloud/WRITER.md hollow override — standalone, no "next part" question, year+place+fact first line, subscribe mid-video)
- [ ] (competitors 28 Oct) Compilations 25–60 min.

## Priority 1 — Wild Sketchbook (`ufc`, local `ufctube` + repo `cloud/ink`)
Now: 5 subs, ~940 views/day, Shorts stayed 32 %, ~1 sub / 2,100 views. Education RPM ($9–15 CPM).
- [ ] Shift weight from "X vs Y: who would win?" fights (risk: "distressing content") to ink explainers: "This Animal …", "What Happens If …" — 8–10 min long + 2 Shorts each.
- [ ] Shorts open on the key fact/comparison at frame 0 + bold subtitle; every title unique.
- [ ] Mid-video value CTA ("subscribe for one animal secret a day").
- [ ] Keep 4/day (config per_day 4); if uploadLimit errors appear, owner phone-verifies the account (no cutting).
- [ ] (competitors 28 Oct) Shorts frame 1 = both animals charging in ink + "WHO WINS?"; stats as quick pop-ups during the fight; one bold verdict (no "one point each").
- [ ] (competitors 28 Oct) Famous/debated matchups (lion vs tiger, gorilla, chimp, grizzly vs hippo); strong angle ("NOT EVEN CLOSE", "…Is A LIE") — Creature Challenge, KO MATION (9.8M).
- [ ] (competitors 28 Oct) Thumbnails: colour-washed ink faces of both animals on a red/blue split + 2–4 bold words (not pale sketch + tiny caption). (partly done 2026-11-07: thumbnail text max 4 words and never the full title, channel-name tag removed, no duplicate title text on the no-photo fallback — cloud/makers/ufc.py + cloud/makers/ufc/art.py; red/blue split still open)
- [ ] (competitors 28 Oct) Long videos: weekly 4–6 min ink "tournament / battle royale" with 8–16 animal brackets (explainers got 0 views).

- [x] 28 Oct: outro shows the verdict on screen ("MY PICK: BEAR" in the winner's colour + "AGREE? COMMENT 1 OR 2") instead of "WHO WINS? 1=… 2=…" (fight.py/animals.py, backups .bak_20261028d).

## Priority 2 — Money Story Daily (`money`, local `moneytube`)
Now: 0 subs, ~36 views/day, Shorts stayed 9.8 %. Highest RPM niche (finance $15–25 CPM).
- [x] Switch the format to concrete number breakdowns ("How Noah Splits a $3,200 Paycheck" 87 % viewed, "The Easiest Budget in the World" 70 %), drop "[Name] Got a Raise and Stayed Broke" story template. (done 2026-11-07: verified — cloud/makers/money/WRITER.md bans the template; today's queue is all number breakdowns)
- [ ] Conflict in 0–2 s; something changes every 2–3 s; loop ending; last 3 s CTA.
- [ ] Start 1 long video/week (8 min "Where $5,000 a Month Really Goes") — long-form finance pays the most.
- [ ] No AI persona/presenter giving financial advice (July 2026 rule); general education only, no personalized advice.
- [x] (competitors 28 Oct) One series on our winning format: "$X Paycheck at Every Level ($2k → $20k)" (Arnie Finance / LITTLE BIT BETTER series style); the "Got a Raise and Stayed Broke" template is copied by dozens of AI channels. (done 2026-11-07: "Every Level" series slot every Mon+Thu — cloud/makers/money/WRITER.md)
- [ ] (competitors 28 Oct) Weekly 10–15 min long video stitched from 6–8 breakdown Shorts, with chapters.
- [ ] (competitors 28 Oct) Thumbnail = one huge number/word ("$3,200") on one bold colour.

## Priority 2 — Calm Rain for Sleep (`sleep`, local `sleeptube`) — real rain recordings only, no AI video
Now: 2 subs, ~90 views/day, long viewers stay ~20 min. Competitors: 4–14 h videos, black-screen versions, "No Ads Between", Vol. series.
- [ ] Lengths 3–10 h (watch hours engine); one black-screen version per week.
- [ ] Unique title per video: setting + sound + length ("Rain on a Tin Roof at Midnight | 8 Hours, No Thunder").
- [ ] Thumbnail: warm window light vs dark rain, 0–3 words; "Vol. N" series names.
- [ ] Shorts: crisp rain at frame 1 + "Put on headphones…", linked to the long.
- [ ] Fix the resumable upload bug in the other local agents too (done in sleeptube 27 Oct).
- [ ] (competitors 28 Oct) Long videos 8–10 h (leaders: 10 h / 48 h; our 1–3 h get 0–2 views) + a "screen fades to black" version.
- [x] (competitors 28 Oct) Title words: "Heavy Rain for Insomnia | Black Screen | 10 Hours (Real Rain, No AI)". (done 2026-11-07: first title variants now "<scene> for Insomnia | N Hours (Real Rain, No AI)" — cloud/makers/sleep.py; black-screen version still open)
- [ ] (competitors 28 Oct) 24/7 rain livestream looping our recordings (owner to approve live streaming); Shorts point to it.

## Priority 2 — Seoul Night Remix (`seoul`, repo `seoul/`)
Now: 0 subs, 1 Pro song. Daily love-song remix + Short, 30/60-min mixes.
- [ ] Every song a different girl look/outfit/place (AGENT.md); chapters + lyric line in description (human layer). (updated 2026-11-07: song 1 "Neon Rain" still has no Short — seoul/AGENT.md open item: make it first)
- [ ] First 30-min mix after song 10; first 1-h mix after song 20.
- [ ] Before YPP: make the old free-plan songs private (owner approval).
- [ ] Watch Content ID: re-generate any song that gets a claim.
- [ ] (competitors 28 Oct) Weekly "[Playlist] … | Seoul night drive" 30–45 min mix with chapters (essential; 1.5M style), situation framing (after work, rainy night).
- [ ] (competitors 28 Oct) Bright thumbnail with one lyric/mood line (ours is dark, small text, waveform).
- [ ] (competitors 28 Oct) Looping animated background (rain/neon) + on-screen Korean + English lyrics (static image risks the inauthentic-content rule).

## Priority 2 — Milo Survives (`milo`, repo `milo/`)
Now: 0 subs, 1 video, CTR 1.66 %, half gone by 0:18. Model: Bright Side / Infographics Show structure.
- [ ] "I Survived 100 Days …" every 2 days + 2 Shorts; danger in the first 3 s; DAY tags. (updated 2026-11-07: only 1 episode since 22 Oct — milo/AGENT.md restart note + 5-episode backlog so the next run starts straight away)
- [ ] Thumbnail: Milo in clear danger + "DAY 99…"/"TRAPPED!".
- [ ] (competitors 28 Oct) Cold open on the most dangerous moment, second person, exact time/place; Day 1 within 5 s (our 19-s "My name is Milo… stay till the end" preamble = half gone by 0:18). Beanie Survives (828K) / One More Day style.
- [ ] (competitors 28 Oct) Thumbnail: huge red "DAY X", threat fills the frame, "DAY 1 | DAY N" split (ours mostly blank white).
- [ ] (competitors 28 Oct) Series "<Story> Ep. N (Day X)" ~10 min, end screen to the next episode; named side characters with their own voices.

## Priority 3 — The Doodle Desk (`doodle`, repo `doodle/`)
Now: 18 subs, ~180 views/day, long CTR 1.39 %. Best title: "How Did a Cheap Team Beat Baseball's $339M Giant?" (2.31 %).
- [ ] Every title a clear conflict / David-vs-Goliath question; thumbnail text adds to the title. (updated 2026-11-07: the question form became its own template (6/6 end in "?") — doodle/AGENT.md "Title form 2026-11-07": max 1 of 3 titles with "?" or "vs.")
- [ ] State the mystery in the first 15 s; mid-video value CTA.
- [ ] 1 long/day + 2 Shorts each (unchanged).
- [ ] (competitors 28 Oct) Channel drifted to daily news explainers (Fed, polls, Medicare) — 1–5 views each; go back to evergreen underdog/money stories: "How a $X <small> Beat a $Y <giant>".
- [ ] (competitors 28 Oct) Thumbnail: one real recognisable object/place + ≤ 3 huge words + red arrow (not yellow bg + stick figure).
- [ ] (competitors 28 Oct) Long videos 12–15 min in list / year-by-year structure (Paint Explainer, Infographics Show).

## Priority 3 — Dough Bros (`dough`, repo `doughbros/`, 13+ per bible — flag as UPLOAD.md)
Now: 15 subs, ~540 views/day; "Would YOU…?" Shorts 78–87 % viewed. Agent log stale since 21 Oct — check why.
- [ ] Find and fix why the hub shows no new episode since 21 Oct.
- [x] More "Would YOU…?" dare Shorts; drop "Trust X or Y?" openers (29 %). (done 2026-11-07: only 5/23 recent Shorts were "Would YOU…?" — cloud/WRITER.md doughbros rule: every job's first Short is a "Would YOU…?" dare)
- [ ] Long episodes: 8–10 min compilations of the best mini-stories.
- [ ] (competitors 28 Oct) Every Short = "Would YOU eat…? A or B" with both choices on screen in the first second (For Kids TV food-choice Shorts 30–49K).
- [ ] (competitors 28 Oct) Weekly 20–30 min compilation; seasonal event series; end each episode on a cliffhanger.
- [ ] (competitors 28 Oct) Thumbnails: sharp close-up of the character's big face (ours are blurry stills with small text).

## Priority 3 — Max the Curious Cat (`max`, local `maxtube` + repo `maxcat`, kids)
Now: 3 subs, ~150 views/day, CTR 0.88 % on 185k impressions, long videos only ~2 min.
- [ ] Thumbnails: Max's face with a big emotion 35–40 % of frame, orange on deep blue/green.
- [x] Titles lead with the hook, no "Max the Curious Cat |" prefix. (done 2026-11-07: verified on the last 4 done jobs; + worker now prefers a clean close-up of Max for the thumbnail frame — cloud/worker.py safe_thumb_beat)
- [ ] Long videos 8–10 min compilations (not 2-min "long" videos); upload count unchanged.
- [ ] (competitors 28 Oct) Weekly 20–30 min themed compilations ("Max's Spooky Adventures 🎃 | 25 Min") — Simon's Cat, Talking Tom, Kitty's Games all live on compilations.
- [ ] (competitors 28 Oct) One fixed thumbnail template: Max's face close-up with emotion + one prop + logo badge + ≤ 3 words; seasonal packaging.

## Priority 4 — Inspector Bolt (`bolt`, repo `bolt/`, kids)
Now: 0 subs, 6 views total, no new episode since 20 Oct.
- [ ] Check why it stopped and restart it at its usual count.
- [ ] Better thumbnails/titles (Bolt's shocked face big, < 50 chars). (partly done 2026-11-07: worker now picks a clean close-up of Bolt himself for the thumbnail (was Pip/Turbo) — cloud/worker.py safe_thumb_beat)
- [ ] (competitors 28 Oct) Channel is uploading (15 uploads 25–27 Oct as "Wheelburg" talking cars) but 0 views — bring the robot detective hero back into titles/thumbnails.
- [ ] (competitors 28 Oct) Searchable title tail "| Car Cartoons for Kids"; hero face close-up + logo thumbnail (Tayo, Robocar POLI, Gecko's Garage).
- [ ] (competitors 28 Oct) Weekly 30–60 min compilation; a short song or "Bolt's Safety Rule" lesson per episode; seasonal tie-ins.

## Quality upgrades done 2026-10-28 (owner: "sifatini yaxshila")
- [x] Upload counts restored to pre-28-Oct values: funny 3/day (6 time slots), roblox 1 long + 5 Shorts, money 2/day, Wild Sketchbook 4/day (config.yaml from .bak_20261028).
- [x] Sharper render: funnyrank source clips up to 1080p (was 720p) + x264 fast/crf 19; robloxtube editor fast/crf 19; moneytube + maxtube animation fast/crf 18; sleeptube Shorts fast/crf 19 (backups *.bak_20261028q).
- [ ] Daily run: one quality item per channel per day (hook in frame 1, unique title, better thumbnail, commentary layer, cleaner audio) — never cut the count.

## Owner decision (competitor research suggested fewer uploads — owner rule: never cut automatically)
- [ ] Wild Sketchbook, Max, Roblox, Doodle: leaders post less but better; research suggested fewer uploads. Owner decides; until then counts stay.

## Owner to-do (Claude cannot do these)
- [ ] Phone-verify the accounts (custom thumbnails, Related video links, more uploads/day). One number = 2 accounts/year: first eldorbekkhabibulaev (Funny, Money) and eldorbekkhabibullaev44 (Roblox, Calm Rain).
- [ ] Run `1_YOUTUBE_ULASH.bat` once in each local agent folder showing "YouTube ulanmagan".
- [ ] Approve making Seoul's old free-plan songs private before the YPP application.

## 2026-10-29 Ask Studio
- Main problem on every channel: Shorts are swiped away in the first 1–2 s (Funny 35 %, Roblox 40 %, Calm Rain 9 % stay). Fix = the hook/fact in frame 0, no intro.
- Cloud-channel rules from today's run were rebuilt into hollow, doodle, bolt, doughbros, maxcat, ink (Wild Sketchbook), seoul, milo AGENT files (the run's push got 403).
- Roblox (local robloxtube agent): drop dates like "(October 27)" from titles — they make the video look old.
- Studio suggests fewer uploads for Hollowmere and Roblox — owner decides (rule above).

## 2026-11-07 daily run (no Studio access — cloud run without the owner's Chrome)
- [ ] Hollowmere: cloud queue is EMPTY (status queue_empty since 7 Nov 01:49) while per_day is 3 long + 4 Shorts — the hollow writer must refill `cloud/queue/hollow/` (WRITER.md) before anything else.
- [ ] Grind_video (`grind`) worker: "no token for Grind_video" since 6 Nov — owner must connect that channel's token (cloud/auth.py) or remove it from channels.json.
- [ ] Wild Sketchbook thumbnail: red/blue split with both animals (art.thumbnail) — still open.
- [ ] Calm Rain: one black-screen long per week — still open (needs a dark-video variant in sleep.py).

## 2026-11-07 competitor run (cloud/growth/competitors/2026-11-07.md) — bigger engine work
- [ ] Hollowmere: weekly compilation long "3 True Stories Animated" ≤ 14:50 (stitch 3 finished longs + new intro/outro) — competitors' true-horror compilations get 75k–135k in 2–3 days.
- [ ] Roblox: a weekly 10–14 min "I ranked every <genre> Roblox game" long (data + verdict), series "Part N" — the 3.5-min daily list does not match the 13–25 min winners.
- [ ] Funny: numbered series in titles ("Fails Ranked #N") — needs a counter in fr_themes.make_title read from past titles.
- [ ] Wild Sketchbook: grid-of-animals first frame (art.py) for the "N animals vs X" format.

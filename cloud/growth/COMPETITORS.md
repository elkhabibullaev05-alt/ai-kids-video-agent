# Daily competitor research: every channel, every day

The owner asked for this on 2026-11-07, in his words: "konkurentlar nima qilyapti, qanday obrochka, qanday tag... hamma kanalda shu instrument ishlasin".

For each of his channels, find which competitor videos get **recommended fastest** and which bring **the most subscribers**. Learn why from their:
- titles
- thumbnails
- tags
- length
- hooks
- series format
- upload time and frequency

Apply the lessons to that channel's agent the same day.

## Channels and niches (search terms to start from; refine them over time in the log below)

| key | channel | niche / audience | start searches |
|---|---|---|---|
| roblox | Roblox Top 10 Daily | Roblox news, rankings, horror games; teen/adult, NOT kids | "roblox top 10", "best roblox games", "roblox horror", "roblox news" |
| funny | Funny Rank Daily | fail/funny compilations ranked (CC BY clips) | "funny fails ranked", "try not to laugh fails", "fails of the week" |
| ufc | Wild Sketchbook | animal facts, "what if" animal battles, drawn/ink style | "animal facts", "what if animals", "strongest animal", "animal vs animal" |
| hollow | Hollowmere Tales | true-story gothic/creepy tales, 13+ | "true scary stories animated", "unsolved mysteries animated", "creepy true story" |
| money | Money Story Daily | personal-finance story Shorts (debt, salary, subscriptions) | "money story shorts", "how much he earns", "debt story", "finance shorts" |
| sleep | Calm Rain for Sleep | real rain sounds for sleep, long | "rain sounds for sleeping", "heavy rain 10 hours", "rain on window sleep" |
| max | Max the Curious Cat | 3D kids cartoon, CoComelon-style (Made for Kids) | "kids cartoon cat", "cocomelon", "3d cartoon for kids" |
| dough | Dough Bros | creepy-cute kitchen comedy cartoon serial | "food cartoon", "animated food comedy", "pommi" style serials |
| bolt | Inspector Bolt | gentle car-detective kids cartoon (Made for Kids) | "car cartoon for kids", "kids detective cartoon" |
| doodle | The Doodle Desk | news explained with stick figures | "news explained animated", "stick figure explainer" |
| seoul | Seoul Night Remix | K-pop style love-song remixes (Suno), AI visuals | "kpop remix", "korean love song remix", "kpop nightcore" |
| milo | Milo Survives | survival story animation | "survival story animated", "how to survive animated" |

## Method (owner's Chrome, Claude in Chrome tools)

1. **Fresh winners.** For each channel, run 2–3 searches on `https://www.youtube.com/results?search_query=<q>&sp=CAMSAhAB` (sorted by view count) and also add the filter "This week" (`&sp=EgQIAxAB`). For Shorts niches, also open `https://www.youtube.com/results?search_query=<q>&sp=EgIYAQ%253D%253D`. Read the results with get_page_text or short JavaScript on `ytd-video-renderer` / `ytm-shorts-lockup-view-model` elements. Note for each result:
   - title
   - channel
   - views
   - age
   - length
2. **Outliers = recommended fast.** Open the channel of the 5 best results (`/@handle/videos` and `/shorts`). Note:
   - subscribers
   - upload frequency
   - the channel's usual views

   An **outlier** is a video with views ≥ 3× the channel's usual views, or ≥ 50k views in under 7 days on a channel under 100k subscribers. Outliers are what the algorithm is pushing. Write down for each outlier:
   - Title pattern (length, numbers, emoji, question vs. statement, curiosity gap).
   - Thumbnail: take a screenshot and zoom on it. Note the face/character, number of words, colours, contrast, arrows/circles, and close-up vs. wide shot.
   - Tags: JavaScript on the watch page: `ytInitialPlayerResponse.videoDetails.keywords`. Also note the hashtags in the description.
   - Description: first 2 lines, chapters, links to series or playlists.
   - Length, and whether it is part of a series ("Part 2", "Ep", or a recurring character).
   - Publish weekday and hour (convert to Bishkek, UTC+6).
3. **Subscriber drivers.** On those channels, note what the most-viewed long videos and series have in common. Videos that make people subscribe are usually:
   - series with cliffhangers
   - a recurring character
   - a strong channel promise in the first 10 s
   - end screens pointing to the next part
4. **Compare with our last 10 videos** (titles in `cloud/results/<ch>/*.json` or the channel's log). List the 3 biggest differences.

## Apply the same day (small, safe changes)

For each channel, change at most 3 things where it really helps. Change them in the place its agent reads them:
- cloud/makers/<key>.py and its helper folder (funny, money, roblox, ufc, sleep)
- cloud/WRITER.md sections (maxcat, doughbros, hollow, bolt)
- cloud/ink/WRITER_INK.md (ufc scripts)
- <channel>/AGENT.md (doodle, milo, seoul)
- cloud/channels.json (slots; never lower per_day)

Allowed changes:
- title rules and examples
- tag/hashtag lists
- thumbnail rules (text size, colours, face/character close-up, word count)
- hook line rules
- description template
- series naming
- release slot times

Run `python3 -m py_compile` on any edited Python file.

Rules:
- Never copy a competitor's title word for word, their thumbnail, their footage, music or characters. Learn the pattern only.
- Never put other channels' or creators' names in our tags, titles or descriptions. Tags must describe our own video.
- No misleading clickbait the video does not deliver.
- No fake engagement.
- Kids channels (max, dough, bolt) stay Made for Kids. roblox is never for kids.
- Calm Rain: real rain only, no AI video.
- Never lower a channel's daily upload count. If competitors suggest fewer uploads, write it as a question for the owner.

## Output

- `cloud/growth/competitors/<YYYY-MM-DD>.md`, one section per channel:
  - table of 3–5 outliers (title pattern, views, age, subs, length, tags, thumbnail notes)
  - "Nima ishlayapti" (3 bullets)
  - "Biz bilan farq" (3 bullets)
  - "Bugun o'zgartirildi" (file + change)
- Add new `- [ ]` items to cloud/growth/PLAN.md for anything that needs bigger engine work.
- Commit and push (`git pull --rebase` on rejection).
- Hub (ArtifactData, https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r):
  - Set `analysis/competitors_<date>` to `{"at", "channels": {<key>: {"winners": [{"title","views","age","channel","why"}], "works": [...], "diff": [...], "changed": [...]}}}`.
  - Get `analysis/latest` (pin if_version). Set its `competitors` field to `{date, channels: {<key>: {"works": [...], "changed": [...]}}}` and append the changes to `actions`. Keep all other fields.

## Same run, after the competitor research: Studio analysis and safety check (owner, 2026-11-07: "hamma narsani sen qil")

This task is the one that runs on the owner's laptop with his Chrome. So, after the competitor part, continue in the same run:
- **Part B:** follow `cloud/growth/STUDIO_DAILY.md` completely: "why videos are not shown" analytics, Ask Studio, fixes for every channel, hub report.
- **Part C:** follow `cloud/growth/SAFETY_DAILY.md` (quick risk check of every channel).

Then send ONE combined final Uzbek message, 6–10 lines:
- competitor lessons
- why videos are not shown
- what was changed
- any risks
- what the owner must do himself

If time runs short, finish Part B for the priority-1 channels first, then the others, and leave Part C for the next day.

## Log of good search terms and competitor channels (update as you learn)
- (empty: first run 2026-11-07)

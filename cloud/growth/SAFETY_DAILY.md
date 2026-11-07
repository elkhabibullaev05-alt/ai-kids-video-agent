# Daily safety / risk check (no strikes, no demonetization, no termination)

The owner asked for this on 2026-10-19 and later extended it to all his channels.

Channels, browser and hard rules: see `cloud/growth/CHANNELS.md`.

This check **reads and reports**. It may only make the small guidance fixes listed below. Never:
- appeal or dispute anything
- delete videos, or make them private or public
- change any setting
- install or suggest anything that hides links between accounts

## For each channel (keep it quick, ~2 min per channel)

1. **Strikes and claims.** Read:
   - `https://studio.youtube.com/channel/<ID>/copyright?authuser=N`
   - the Studio dashboard notices
   - the Content list "Restrictions" column (Videos and Shorts tabs)

   Record every:
   - copyright claim or strike
   - Community Guidelines warning or strike
   - age restriction
   - limited-ads icon
   - Made-for-kids restriction
   - monetization message, including "reused or repetitive content"
2. **Repetitive content.** Compare the last 10 titles and thumbnails. Flag the channel if its videos look template-identical.
3. **Kids flag.** Check the Audience setting of 3 recent videos:
   - max, dough, bolt: Made for kids = Yes
   - roblox: No on every video
   - all other channels: No
4. **Risk level.** "past" / "o'rta" / "yuqori", plus one Uzbek sentence explaining why.

## Fixes allowed

Add a short dated "Safety notes <date>" section to the channel's guidance file (the files are listed in CHANNELS.md). Anything about an already published video goes to the owner's to-do list instead.

## Report

1. Set `analysis/safety_<YYYY-MM-DD>` = `{"at", "channels": {<key>: {"risk", "notes": [], "fixes": []}}, "owner_todo": []}`.
2. In `analysis/latest`:
   - For each channel with risk "o'rta" or "yuqori", append "⚠ Xavf (<risk>): <reason>" to `channels.<key>.problems`.
   - Append the owner_todo lines to `actions`, each prefixed "Siz: ".
   - Keep all other fields.

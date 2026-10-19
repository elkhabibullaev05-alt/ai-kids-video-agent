# Phonk channel — production run (instructions for Claude)

Status: **channel not created yet** (owner will open it). Until `story/log.json → channel.id` is set, a run only refreshes the preview page (https://claude.ai/artifact/Ev1eqFRjqQZSbEu7Zqyioz) and the hub doc `agents/phonk`, then stops.

Goal once the channel exists: **2 long + 3 Shorts per day** of original drift phonk. Everything is made by us — music (`engine/phonk.py`), cover (`engine/cover.py`), video — never a downloaded or "slowed" copy of someone else's track (copyright claims take the revenue and strikes end the channel). User speaks Uzbek; titles are English + translations.

## Per run (one long + 1–2 Shorts)
1. `git pull`, lock in `story/log.json` (same lock rules as `bolt/AGENT.md`), pick a new name (2 words, CAPS, never used before — check log), a seed never used before.
2. Music: long single = `python3 engine/phonk.py out/NAME.wav --seed S --bars 96` (~3 min); 1-hour mix = 18–20 tracks with new seeds, crossfaded with ffmpeg `acrossfade=d=4`. Loudness -14 LUFS (`loudnorm=I=-14:TP=-1.5`).
3. Cover: `python3 engine/cover.py out/NAME.jpg "NAME" --seed S` (16:9) and `--w 1080 --h 1920` for Shorts.
4. Video: cover with slow centre zoom + `showcqt` bars at the bottom (see `/tmp` demo command in the repo history), 1920×1080 30 fps; Shorts = the 30 s around the first drop (`*.json → drops`), vertical cover.
5. Rek-ball gate: `python3 ../tools/rek_ball.py FILE "TITLE" ambient` for the long, `short` for Shorts; < 85 → not uploaded (Shorts may use `--kuchaytir`).
6. Upload through the built-in browser (flow as in `bolt/UPLOAD.md`), **not** made for kids. Slots UTC: long 14:15–15:45 and 21:15–22:45; Shorts 12:15, 17:45, 23:45 (±30 min, :15/:45).
7. **Translations (owner's rule):** title + description in **es, pt, ar, fr, ja, ko, de** via Studio → video → Subtitles/Languages (`../tools/TRANSLATE.md`). No subtitles needed (instrumental).
8. Log, unlock, push. Update `agents/phonk` in the hub (videos, next, numbers, status "ok").

Title patterns: `NAME 🏎️ Aggressive Drift Phonk (1 Hour)`, `NAME 👻 Dark Night Drift Phonk`, Shorts `NAME 🔥 #phonk #shorts`. Description says the music is original to the channel.

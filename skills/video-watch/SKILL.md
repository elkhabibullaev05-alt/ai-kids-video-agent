---
name: video-watch
description: Watch a video the way a real viewer does: frames, cuts, sound, captions, repeats. Then judge it as a person would (would I keep watching? did I feel anything?). Use whenever the owner asks to look at, watch, check, review or rate a video (an MP4 in the GitHub repo elkhabibullaev05-alt/ai-kids-video-agent, a raw/blob GitHub link, an uploaded file or a rendered file in the workspace), before uploading a new video, or when a channel's retention is low and you need to know why. Triggers - "videoni ko'r", "izle", "видеону көр", "watch this video", "check the render", "nega ko'rishmayapti".
---

# Video Watch: watch a video like a person does

Claude cannot play a video. It can see still images and read text. This skill
turns a video into those: timestamped frames on contact sheets, the first
frame at full size, scene cuts, repeated footage, silences and loudness, and a
transcript when speech-to-text is available. Then you watch it twice. First
you watch it as an ordinary viewer and say what you felt. Then you watch it as
an editor and say what to fix.

Never say you "watched" a video unless you actually read its sheets with the
Read tool. If something could not be checked (no transcript, download failed),
say so plainly.

## 1. Get the video and break it down

```bash
python3 <skill_dir>/scripts/watch.py <SOURCE> --out /tmp/watch_<name>
```

`<SOURCE>` can be:
- a local path, e.g. `cloud/ready/maxcat/20261026-first-snow.mp4` in a clone of the repo
- a GitHub link: `https://github.com/<owner>/<repo>/blob/<branch>/<path>.mp4`
- the short form `owner/repo:branch:path`, e.g.
  `elkhabibullaev05-alt/ai-kids-video-agent:main:cloud/ready/maxcat/20261026-first-snow.mp4`

Where videos live in the owner's repo: `cloud/ready/<channel>/*.mp4` (rendered,
waiting) and `cloud/ready/<channel>/done/`. Upload branches such as
`uploads-seoul` and orphan branches hold the rest. List them with
`git ls-files | grep -iE '\.(mp4|mov|webm)$'` or
`git ls-tree -r --name-only origin/<branch> | grep mp4`. If the file is a Git
LFS pointer, the script tells you; fetch it from
`https://media.githubusercontent.com/media/<owner>/<repo>/<branch>/<path>`.

Options: `--every 1` sets one frame per second (default is about 36 frames
spread over the video). `--lang en` forces the speech language.
`--no-audio` skips audio. For a long video (over 3 min), use `--every 3`.
Then look closer at the hook (0–30 s) with a second run on a trimmed copy:
`ffmpeg -t 30 -i in.mp4 -c copy hook.mp4`.

What it writes to the `--out` folder:
| File / field | What it tells you |
|---|---|
| `first_frame.jpg` | The exact frame a scrolling viewer sees first. It decides the swipe. |
| `sheet_01.jpg …` | 12 frames per sheet (3×4) with a yellow timestamp on each. |
| `report.json → info` | Duration, size, vertical or horizontal, fps, audio present. |
| `scene_cuts`, `longest_no_cut_s` | When the picture changes. Long gaps with no cut mean viewers get bored. |
| `repeated_frames`, `repeated_pct`, `repeat_examples` | The same footage shown again ([later_s, earlier_s]). This is the "reused / repetitive content" risk. |
| `still_stretches` | Moments where almost nothing moves. |
| `silences`, `mean_volume`, `max_volume` | Dead air, too-quiet or clipping sound. |
| `transcript.txt` | `[start-end] text` for every spoken line, if speech-to-text worked. |

If `transcript_error` appears (the model download is blocked in the cloud), the
words cannot be heard. In that case use the script/JSON the video was built
from (e.g. `scripts/epNNN.json`, the queue job's `narration`/`lines`) as the
words, and say "transcript from the script, not from the audio".

## 2. Look at it, in order, with the Read tool

1. `first_frame.jpg` at full size.
2. Every `sheet_*.jpg`, in order. Do not skip sheets of a long video. Read them
   all and keep notes per timestamp.
3. `transcript.txt` (or the script), lined up with the timestamps.
4. `report.json`.

While reading, write short notes like a person thinking aloud:
`0:00 ginger cat on windowsill, snow outside, big caption "Max sees SNOW" → cute, I'd stop scrolling`
`0:05 cut back to the same window shot, caption changes to "Watch his face again…" → wait, I just saw this`

## 3. First pass: watch as a viewer (feel it)

Answer these honestly, as the target viewer (a 5-year-old for kids channels,
a teen for Roblox, an adult for Doodle Desk or Money Story), not as the maker:

1. **The first 1 second.** Would my thumb stop? What exactly is on screen, and
   is there motion, a face, a question, or danger?
2. **The first 3 seconds.** Do I know what this is about and why I should wait?
3. **Where would I swipe away?** Give the timestamp and the reason (nothing new
   happened, slow talk, confusing, repeat, ugly frame).
4. **What did I feel, and when?** Laughed, was scared, curious, "aww", bored, or
   annoyed. One line per feeling with its timestamp.
5. **The ending.** Did it pay off the hook? Does a Short loop cleanly back to
   frame 1? Does a long video leave me wanting the next one?
6. **Would I like, comment, share or subscribe?** Why or why not?
7. **Does it look like a real creator made it, or like a template/AI factory?**
   This matters because YouTube's July 2026 "inauthentic content" rule demonetizes
   template-like, near-identical videos.

## 4. Second pass: watch as an editor (check it)

Go through the checklist. Each item is OK / problem + timestamp:

- **Hook frame:** motion plus big bold 3–5 word text at 0.0 s; no logo, fade-in or title card.
- **Pace:** something new (cut, sound, reveal, text) every 4–6 s for Shorts and every
  10–15 s for long videos. Compare `longest_no_cut_s` and `still_stretches`.
- **Repeats:** `repeated_pct` over 15% in a Short, or the same shot shown twice
  with no new information, is a problem. Name the repeated ranges.
- **Captions:** readable on a phone (big, high contrast, inside safe area, not
  covered by the YouTube UI at the bottom-right), spelled right, matching the words.
- **Picture quality:** AI glitches (extra fingers/paws, melting faces, wrong
  number of legs, text gibberish), flicker, black frames, wrong aspect ratio, blur.
- **Sound:** speech starts at 0 s; no silences over ~1 s in Shorts; mean volume
  roughly −14 to −20 dB; `max_volume` near 0 dB can mean clipping; music not louder than voice.
- **Story:** clear beginning → problem → payoff; characters consistent between shots.
- **Channel rules:** kids channels (max, dough, bolt) contain nothing scary or
  unsafe; Roblox is never a kids video; Calm Rain has no AI video; Seoul is marked
  synthetic; Funny Rank credits CC BY creators. See `cloud/growth/CHANNELS.md`.
- **Title/thumbnail promise:** does the video actually show what the title promises?

## 5. Write the verdict

Write it in the owner's language (Uzbek Latin by default), short:

```
🎬 <file> (<duration>, <vertical/horizontal>)
Tomoshabin sifatida: <2–3 sentences on what I felt and where I'd swipe>
Baho: <score>/10. Qolib ko'radimi: <ha / yo'q, <time>da ketadi>
Muammolar:
- <time> <problem> → <concrete fix>
Yaxshi tomoni: <one line>
```

Scoring guide: 9–10 means I'd share it. 7–8 means I'd watch to the end. 5–6
means I'd swipe halfway. 3–4 means I'd swipe in the first 3 s. 1–2 means it is
broken (glitches, silence, wrong format).

If the user asked you to fix the video, follow the verdict by changing the maker
code/script (not the published video), re-render, and run this skill again on
the new file. Report before → after.

## Worked example (real file from the repo, 2026-11-11)

`cloud/ready/maxcat/20261026-first-snow.mp4` (Max the Curious Cat, kids Short).

report.json (abridged): duration 15.1 s, 1080×1920, audio yes, scene_cuts [5.03],
longest_no_cut_s 10.07, repeated_pct 33, repeat_examples [[5.0, 0.0], [5.5, 0.0], …],
mean_volume −18.4 dB, max −1.5 dB.

Notes from the sheets:
```
0:00 ginger tabby on a kitchen windowsill, snow falling outside, caption
     "Max sees SNOW / for the first time!" → warm, cosy, clear topic. Good hook frame.
0:02 paw reaches up to a snowflake on the glass → the cute moment, I smile
0:04 close-up of Max's face, wide eyes → payoff, great
0:05 CUT back to the 0:00 wide shot, caption "Watch his face again…"
     → this is the same 5 s clip again; I already saw it
0:05–0:15 the same paw/face moment replays, slightly different crop → I swipe around 0:07
```

Verdict:
```
🎬 20261026-first-snow.mp4 (15 s, vertikal)
Tomoshabin sifatida: birinchi 5 soniya juda yoqimli — Max qorni panjasi bilan
ushlamoqchi bo'ladi, yuzi hayron. Lekin 0:05 dan keyin xuddi shu kadr qayta
ko'rsatiladi, men 0:07 da o'tib ketaman.
Baho: 6/10. Qolib ko'radimi: yo'q, 0:07 da ketadi.
Muammolar:
- 0:05–0:15 bir xil 5 soniyalik klip takrorlanadi (33% takroriy kadr) → ikkinchi
  yarmiga yangi voqea qo'shing (qor parchasi burniga tushadi, Max aksiradi) yoki Shortni 6–8 s ga qisqartiring.
- Ovozli gap yo'q (transkript yo'q) → 0 s dan bitta qisqa ovozli savol: "What is THIS?!"
- Takroriy kontent qoidasi xavfi → har bir Short o'z yangi lahzasiga ega bo'lsin.
Yaxshi tomoni: birinchi kadr va 0:04 dagi yuz yaqin plani juda kuchli.
```

## Example 2: a long video (8–12 min, The Doodle Desk)

```
python3 watch.py doodle_ep014.mp4 --out /tmp/w14 --every 4      # whole video, ~150 frames, 13 sheets
ffmpeg -t 30 -i doodle_ep014.mp4 -c copy /tmp/hook.mp4
python3 watch.py /tmp/hook.mp4 --out /tmp/w14hook --every 0.5   # the hook in detail
```
Read all 13 sheets. Note the minute where drawings stop changing
(`still_stretches`) and match it with the transcript. That is usually the place
where the audience-retention graph drops. A good note looks like:
`3:40–4:30 same chart drawing for 50 s while narrator lists numbers → add 3 new
doodles (one per number) or cut the list to one number.`

## Example 3: checking a render before upload (inside a channel agent)

After rendering and before uploading, run the skill on the MP4. Block the upload
(and log the reason in `cloud/rejected/<ch>/<job>.reason.json`) if any of these is true:
- the first frame is black, blank or a title card;
- a Short has `repeated_pct` > 30, or a silence of 2 s or more;
- the video's aspect ratio is wrong for its type (a Short must be 9:16);
- you see a clear AI glitch on a main character's face or hands.

## Limits (say them when they matter)
- Frames are samples. Something that lasts less than the frame interval can be
  missed; use a smaller `--every` for fast action.
- Without a transcript you hear only loudness and silence, not the words.
- Music mood is guessed from the script/genre, not heard.
- Feelings are judged as the target viewer would likely feel them. That is an
  informed guess, not real audience data; compare with Studio retention when you can.

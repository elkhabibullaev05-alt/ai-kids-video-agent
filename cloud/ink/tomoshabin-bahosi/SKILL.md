---
name: tomoshabin-bahosi
description: Review a YouTube video script (or a rendered video's frames) the way a real viewer would, second by second, and score it out of 100. Use before publishing any long video or Short; only 85+ may be published. Trigger on "tomoshabin bahosi", "videoni baholash", "85 baldan o'tadimi", "would people watch this to the end", "retention check".
---

# Tomoshabin bahosi — viewer-eye review (100 points, pass at 85)

Act as an ordinary viewer who is scrolling on a phone, bored, with a thumb ready to swipe. Do not act as an editor. For every moment, ask: "Is there a reason to stay for the next 3 seconds?"

## How to run it

1. Read the script (JSON `scenes[].say/hook/label/num/img` and `short.scenes`). If a rendered video exists, look at a frame every 2 s for the first 10 s and at the last 10 s.
2. If the repo has `cloud/ink/check.py`, run `python3 cloud/ink/check.py <script.json>` first. That is the mechanical score; the rubric below is the human pass on top of it.
3. Walk through the video in your head second by second. Note the first moment you would swipe, and why.
4. Score each part below and list concrete fixes. Rewrite the weak lines yourself, then score again. Never publish under 85.

## Rubric

**A. First 3 seconds — 30 points**
- Something big and moving is on screen at frame 0: no blank, no logo, no title card. The hook question is on screen, ≤ 7 words. (8)
- The voice starts immediately, with no greeting, no "in this video", no channel name. (6+5)
- The first sentence is ≤ 14 words and talks to "you", or makes a claim that sounds almost wrong. (6+5)

**B. Holding attention — 35 points**
- An open loop by scene 3: the best thing is promised for the end, and it is delivered at the end. (7)
- The picture changes at least every 2–3 seconds: a new image, a punch-in, a number badge, or text. (8)
- Sentences sound like a person talking: short (6–20 words), contractions, questions, "here's the thing", "okay, so". Nothing that reads like an encyclopedia. (6)
- At least one hard number or specific fact every ~minute (long) or 2+ (Short). (6)
- Long videos: a re-hook every ~60 s ("but here's the twist…") plus a #N countdown. Shorts: word-by-word captions and a last line that flows back into the first line, so it loops. (8)

**C. Ending — 15 points**
- Long: a subscribe moment (the button is clicked on screen, with a voice line) plus a comment question. (8+4)
- Short: points to the full video ("full story on my channel"); the description links to it. (8+4)
- The video ends right after the payoff, without a dragging outro. (3)

**D. Length and trust — 20 points**
- Long: 8–12 minutes (mid-roll ads start at 8:00). Short: 40–60 s. (10)
- At least 2 real sources. The title (≤ 70 chars) creates curiosity, and the video delivers it. (5+5)

## Hard fails (score = 0, do not publish)

- Any invented fact, number, study or quote.
- A title or thumbnail promise the video does not deliver.
- Gore, cruelty, or anything that encourages harming animals or people.
- Copyrighted footage or music without a license.

## Output

```
Tomoshabin bahosi: NN/100 (A nn, B nn, C nn, D nn) — O'TDI / O'TMADI
Swipe moments: 0:0x — reason …
Fixes: 1) … 2) … (with the rewritten lines)
```

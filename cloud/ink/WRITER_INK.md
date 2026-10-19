# Ink explainer writer — animals channel (Fight Stats Daily → animal channel)

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

- The file parses: `python3 -c "import json;json.load(open(F))"`.
- Word counts are in range. The `id` matches the filename.
- The commit contains only the new file. Push it to `main`.

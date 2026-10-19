# Translations for every video (owner's rule, 2026-10-19)

Goal: a viewer in Japan sees the title and description in Japanese, a viewer in the US sees the English original, and so on. YouTube shows the version matching the viewer's language automatically.
Languages: **es, pt, ar, fr, ja, ko, de** (Spanish, Portuguese, Arabic, French, Japanese, Korean, German). Hindi and Indonesian were removed by the owner on 2026-10-19 — do not add them.

## What to make (you translate it yourself — natural, short, same meaning and hook; keep emojis, #hashtags, @handles and URLs unchanged)
- Every video (long and Short): translated **title** (≤ 100 chars, no `<` `>`) and **description**.
- Long videos and voiced Shorts: an English subtitle file `subs_en.srt` (from the script/timeline timings) and the same file translated into the 7 languages (`subs_<lang>.srt`, identical timings). Write them while the render runs, so translation never delays the upload.
- Save them next to the video: `translations.json` = `{"<lang>": {"title": "...", "description": "..."}}` (keep it out of git like the other outputs).

## Adding them in YouTube Studio (after the video is scheduled)
Open `https://studio.youtube.com/video/<VIDEO_ID>/translations` (Studio: video → **Subtitrlar / Subtitles**). Make sure the video language is **English** (if Studio asks, set it to English — this is the video's own field, not a channel setting).
For each language:
1. **Til qo'shish / Add language** → pick the language.
2. In its row: **Nom va tavsif / Title & description → Qo'shish / Add** → paste title and description → **Nashr qilish / Publish**.
3. In its row: **Subtitrlar / Subtitles → Qo'shish / Add → Faylni yuklash / Upload file → With timing** → the `subs_<lang>.srt` file (put the files on the same orphan upload branch and load them into the page as blobs, exactly like the video file in UPLOAD.md; set them on the file input with DataTransfer) → **Nashr qilish / Publish**.
Also upload `subs_en.srt` for English.
Keep each javascript_tool call short (45 s limit) and check the row status after each language.
Time limit: at most ~15 minutes per run for translations. Whatever is not finished goes into the log as `"translations_pending": [{"video_id", "langs": [...]}]` and is done first in the next run.

## Log
In the episode's `uploads[]` entry add `"translations": ["es", ...]` (languages actually published) and `"subs": ["en", "es", ...]`.

Dubbed audio tracks are NOT made by us: YouTube's own automatic dubbing (Studio setting, owner decides) creates them.

## Old videos (owner's request, 2026-10-19)
The channel's already published videos get translations too: after the current run's own videos (and any `translations_pending`) are done, add title + description translations (no subtitles needed) to up to **5 older videos per run**, most-viewed first (Studio Content list sorted by views). Keep the list of finished ones in the agent's `story/log.json → "translated_old": ["<video_id>", ...]` so none is done twice. Stay inside the ~15-minute translation budget.

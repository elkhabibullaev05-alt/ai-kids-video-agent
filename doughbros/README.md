# Dough Bros — daily spooky cartoon generator

Original 2D animated series (English voices, Spanish subtitles, + DE/FR/IT/PT .srt) rendered entirely from JSON scripts:
SVG characters → PNG frames (cairosvg) → MP4 (ffmpeg), voices from the offline Kokoro TTS model, synthesized sound effects and music.

```bash
bash setup.sh
python3 engine/render.py scripts/ep001_long.json     # -> out/ep001_long/ep001_long.mp4
```

- `engine/` — renderer (`render.py`), characters, villains, backgrounds, audio
- `story/bible.md` — characters and rules · `story/SCRIPT_FORMAT.md` — script format · `story/log.json` — episode history
- `scripts/` — one JSON per video
- `AGENT.md` — the daily procedure a scheduled Claude session follows (1 long + 3 Shorts per day)

Nothing is uploaded automatically; videos are reviewed and published by hand.

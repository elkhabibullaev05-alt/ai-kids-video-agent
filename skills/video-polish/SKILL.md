---
name: video-polish
description: Make a finished video look and sound as good as possible for YouTube - Full HD 1080p (or 1440p/4K), sharper picture, cleaner colour grade, loud and even sound (-14 LUFS), dead air and repeated footage cut out, correct 9:16 / 16:9 frame without stretching, optional burned-in captions, and a YouTube-ready high-bitrate encode, with a before/after report. Use when the owner asks to make a video "chiroyli", "sifatli", "Full HD", "montaj qil", "ovozini to'g'rila", "takrorini kes", or after video-retention lists fixable problems.
---

# Video Polish: Full HD, beautiful, clean edit

Polishing cannot invent detail that isn't there. It can make a video *look* and
*sound* professional: correct size, crisp edges, pleasing colour, even loudness, no dead
air, no repeated footage. Always run **video-retention** before and after polishing, and
look at a before/after frame. Never claim it is better without that check.

## 1. Run it

```bash
python3 <skill_dir>/scripts/polish.py IN.mp4 OUT.mp4 \
   [--res 1080|1440|2160] [--look natural|vivid|warm|cinematic|none] \
   [--trim-silence] [--cut 5-15 21-24] [--captions subs.srt] [--fps 30|60] [--denoise] [--fast]
```

What it does, in order:
1. **Cuts** the `--cut` ranges and, with `--trim-silence`, every silence over 0.7 s (it
   keeps 0.25 s of breath on each side). Audio and video stay in sync.
2. **Frames** to 1080×1920 (vertical) or 1920×1080 (horizontal). Picture of the wrong
   shape is fitted onto a blurred copy of itself, never stretched or cropped off.
3. **Upscales** with Lanczos when the source is smaller, then gently sharpens (`unsharp`).
4. **Grades** colour with the `--look`:
   - `natural`: small contrast and saturation lift (default, safe for everything)
   - `vivid`: punchy colours for kids cartoons, food, satisfying clips
   - `warm`: cosy, golden (stories, Max the Curious Cat, Dough Bros)
   - `cinematic`: teal/orange, slight vignette (Hollowmere horror, Milo Survives)
   - `none`: keep the colours
5. **Sound**: high-pass at 60 Hz, gentle compressor, loudness about −14 LUFS (YouTube's
   playback level), true-peak −1 dB, 48 kHz AAC 256 kbps.
6. **Encode**: H.264 High, CRF 17, BT.709 colour tags, keyframe every 0.5 s, `+faststart`.
   YouTube then gives it a better-quality transcode. `--res 1440` or `2160` makes YouTube use
   the VP9/AV1 high-quality path even for viewers watching in 1080p. This is the classic
   "upload in 1440p to look sharper" trick. It costs more upload time.
7. Prints before/after: resolution, fps, bitrate, loudness (LUFS), sharpness, seconds removed.

`--fast` uses a fast preset for previews. Use the default (slow) for the real upload.

## 2. Recipes per channel

| Channel | Command |
|---|---|
| Max / Dough Bros / Inspector Bolt (kids 3D) | `--look warm --trim-silence` (keep Made-for-Kids flags unchanged) |
| Hollowmere Tales / Milo Survives | `--look cinematic --denoise` (don't trim silence: horror pauses are intentional; cut only real dead air with `--cut`) |
| The Doodle Desk (stick figures) | `--look none --res 1440` (flat white art: colour lift isn't needed; 1440 keeps line edges crisp) |
| Funny Rank / Roblox (clips) | `--look vivid --trim-silence --res 1440` |
| Calm Rain for Sleep | `--look none --lufs -20` (sleep audio must be soft and even, no compressor pumping; never trim silence) |
| Seoul Night Remix | `--look cinematic --res 1440` (music: no `--trim-silence`) |

## 3. Editing (montaj) moves you can do with it

- **Remove repeats** found by video-retention: `--cut 5-15`.
- **Kill a dead ending** or frozen end card: `--cut 21-24`.
- **Tighten talking**: `--trim-silence`. This gives a jump-cut style that keeps Shorts moving.
- **Captions**: make an `.srt` from the script's narration lines and timings (or from the
  transcript when speech-to-text works) and pass `--captions`. Captions are big, white with
  a black outline, and sit above the YouTube UI.
- **A different hook**: cut the strongest 2–3 s from later in the video, put it first with
  `ffmpeg -ss A -t 3 -i in.mp4 hook.mp4` + concat, then polish the result.
- **Shorts from a long video**: the repo already has `tools/make_short.py`. Polish its output.

## 4. Check the result (always)

1. `python3 ../video-retention/scripts/retention.py OUT.mp4`: the score must not go down.
2. Extract the same moment from before and after and look at them side by side:
   ```bash
   ffmpeg -v error -ss 8 -i IN.mp4 -frames:v 1 -vf scale=360:-2 b.jpg
   ffmpeg -v error -ss 8 -i OUT.mp4 -frames:v 1 -vf scale=360:-2 a.jpg
   ffmpeg -v error -i b.jpg -i a.jpg -filter_complex hstack ba.jpg   # then Read ba.jpg
   ```
   Look for over-sharpening halos, skin or fur turned orange, crushed blacks, or text cut off.
   If you see one, go back to `--look natural`.
3. Loudness after must be −13 to −16 LUFS (sleep: about −20).

## Worked example (real, 2026-11-11)

`cloud/ready/grind/20261026-most-satisfying.mp4` → `--look vivid --trim-silence --cut 35-46`
```
before: 1080x1920 30fps 45.3 s, 1.6 Mbps, −24.9 LUFS, sharpness 374
after : 1080x1920 30fps 34.5 s, 7.9 Mbps, −15.1 LUFS, sharpness 490 (+31%)
removed: 35–46 (repeat) + two short silences
retention: avg viewed 36% → 43%, still "chiqmaydi" because two more repeats remain
```
Lesson: polishing improves quality and sound, but it cannot fix a weak edit. Repeats
need new footage.

## Rules
- Never change a published video. Polish the file before upload, or re-upload only if the owner asks.
- Never stretch faces or crop off captions, logos-in-frame credits, or CC BY attribution text.
- Do not remove other creators' watermarks from footage you don't own. If a watermark is
  there (e.g. "PixVerse.ai"), report it as a risk instead.
- Kids videos stay calm: no flashing, no loudness above −14 LUFS.

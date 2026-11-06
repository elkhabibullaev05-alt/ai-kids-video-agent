# Makers — channels whose old PC agent was lost (2026-11-06)

The owner's old laptop broke on ~30 Oct 2026. Five channels were made by agents that lived only on that laptop
(funnyrank, moneytube, robloxtube, ufctube, sleeptube). They are rebuilt here as **makers**: one Python script per
channel that the existing worker (`cloud/worker.py`, run every 20 min by `cloud/run_all.sh` in WSL Ubuntu 24.04 on the
owner's new laptop "KOMPUTER", RTX 5050, 20 CPU) calls when the channel needs more videos.

## Contract

```
python3 cloud/makers/<ch>.py --out DIR --home HOME --repo ROOT --titles TITLES.json --need-long 0|1 --need-short 0|1
```

- Write finished videos into `DIR`: `<name>.mp4` + `<name>.json` (and optional `<name>.jpg` thumbnail, 1280x720).
- JSON: `{"file": "<name>.mp4", "kind": "short"|"long", "title": "...", "description": "...", "tags": [...],
  "thumb": "<name>.jpg"?, "pack": "<id>"?, "queue_file": "cloud/queue/<ch>/<file>.json"?}`
  - `pack`: give a long video and the Shorts cut from it the same value. Name the files so the long sorts first
    (`<pack>-0-long.json`, `<pack>-1-short.json` …). A Short's description may contain `{LONG_URL}` (replaced with the long's link).
  - `queue_file`: if the video was made from a script that a Claude writer task put in `cloud/queue/<ch>/`, the worker moves it to `cloud/done/<ch>/`.
- One run = one "pack" (e.g. 1 long + 1–2 Shorts, or 1–3 Shorts). Keep a run under ~2 hours on that laptop.
- Exit 0 = made something. Exit 3 = nothing to make right now (e.g. empty queue). Other = error (message on stderr).
- `TITLES.json` = the channel's last ~200 titles; never reuse one.
- Every MP4 is scored by `tools/rek_ball.py` (must be ≥ 85) by the worker. Make videos that pass: hook in frame 0,
  big readable text, voice from 0.0 s, no silence, -14 LUFS-ish loudness, 1080x1920 30 fps Shorts (≤ 59 s), 1920x1080 longs.
- Available in WSL: python3, ffmpeg, numpy, pillow, scipy, soundfile, kokoro-onnx (models in /opt/kokoro: `kokoro.onnx`,
  `voices.bin`; see maxcat/engine3d/voices.py), Blender 4.2.3 (/opt/bl/...), fonts-dejavu-core, google-api-python-client
  (`youtube_up.client(token_path)` for read calls with the channel's token at HOME/token.json, scope youtube.readonly +
  youtube.upload). Internet access is normal (home connection). pip installs: add them to `cloud/makers/setup.sh`.
- Never upload yourself (the worker uploads). Never touch tokens beyond reading. No copyrighted material except
  sources whose license allows reuse (CC BY with credit in the description, CC0, public domain, official APIs/thumbnails used as news).
- Channels are NOT phone-verified (except Roblox, Calm Rain): no long video over 14:50; custom thumbnails may fail — always also make the first frame strong.

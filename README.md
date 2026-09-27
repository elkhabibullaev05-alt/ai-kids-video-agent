# AI Kids Video Agent

A local Python workflow that turns recent news into a source-linked English YouTube Short. It collects RSS/Atom headlines, creates a simple-English summary and a 30–45 second script, synthesizes spoken English narration, renders a 3D news presenter with mouth movement timed to the narration, then assembles everything into a vertical MP4.

On Windows, narration uses the built-in Speech API (default voice: Microsoft Zira; override with `--voice "Microsoft David Desktop"` or `NEWS_SHORTS_VOICE`). The workflow does not upload or publish videos. Review the source and generated script before publishing.

## Requirements

- Python 3.10 or newer
- Internet access for public news feeds
- Blender to render 3D scenes (install Blender and add it to `PATH`, or set `BLENDER_PATH`)
- FFmpeg to assemble the video (on `PATH` or via the optional `render` extra)
- Windows Speech voices for offline narration
- Optional: an OpenAI-compatible API key for generated summaries and scripts. Without a key, a clearly labeled local template uses only the headline and feed summary.

## Install

```bash
python -m pip install -e ".[render]"
```

The `render` extra supplies a Windows-compatible FFmpeg executable through `imageio-ffmpeg`. You can also use your own installation on `PATH` or point `FFMPEG_PATH` at its executable. The provided `ffmpeg-9.0.2.tar.xz` is the FFmpeg **source code** (not a ready-to-run Windows executable); the pipeline does not need to compile it.

## Daily hologram aquarium channel

The separate `ocean-shorts` agent creates original, silent 20-second 3D hologram animations of rotating ocean animals, with on-screen English titles and its own gentle synthesized ambient music. Channel brand: **Ocean Glow**. It uses no voiceover, other people's footage, or downloaded music. It can schedule three Shorts for **09:00, 14:00, and 18:00 America/New_York** every day. Windows Task Scheduler starts the job early that morning so all three videos can be rendered and uploaded ahead of their release times. Keep the PC on and connected to the internet around the scheduled run. Preview videos locally without uploading:

```powershell
python -m ai_kids_video_agent.ocean_cli preview
```

### Animated New York serial

Create episode one of **The Borough File**, an original, open-ended illustrated mystery about Maya (17) and Noah (16) in Astoria, Queens. They speak in separate English voices over dialogue captions. The episode ends on a cliffhanger; the series story bible and script are saved alongside the video. On Windows, the workflow uses the installed Microsoft Zira and David voices with light pitch adjustments. Those are adult system voices, not actual teen voice actors. No upload occurs.

```powershell
python -m pip install -e ".[render,automation]"
borough-file
```

The MP4 and series files are written to `output/borough-file/`. Review the voices, dialogue, and visuals before publishing. The first episode is a pilot foundation; each future episode still needs an authored continuation.

### Connect your own YouTube channel

The agent cannot create a Google account/channel or accept Google's terms on your behalf. Create/sign in to the channel yourself at [youtube.com/create](https://www.youtube.com/create), then:

1. Open [Google Cloud Console](https://console.cloud.google.com/), create a project, enable **YouTube Data API v3**, configure OAuth consent, and create an **OAuth client ID → Desktop app**. Download its JSON file.
2. Save that file locally as `%LOCALAPPDATA%\ai-kids-video-agent\client_secret.json`. Never share the Google password, OAuth token, or client JSON in a chat, commit them, or place them in the repository.
3. From this project folder, run `python -m pip install -e ".[render,publish]"`, then `python -m ai_kids_video_agent.ocean_cli authorize`. A Google sign-in page opens; sign in with the channel's Google account and approve video uploads.
4. Run `python -m ai_kids_video_agent.ocean_cli preview` and review the generated video. Then install the daily task with `python -m ai_kids_video_agent.ocean_cli install-schedule`. Check it with `python -m ai_kids_video_agent.ocean_cli schedule-status`; stop automatic uploads with `python -m ai_kids_video_agent.ocean_cli remove-schedule`.

Uploads are initially **private scheduled posts**, set to release publicly at the three selected Eastern times. All videos are marked as not made for kids, consistent with this channel's general-audience setting. Google/YouTube may require the API project to be verified/compliance-audited before API uploads can become public; an unverified project's uploaded videos can remain private. The channel owner must complete any Google review or verification. A VPN is not required and does not make a Short reach American viewers; the videos use English metadata and Eastern-time scheduling. Shorts reach depends on viewer response and retention; no view count or monetization outcome is guaranteed.

### Free GitHub Actions fact-Short workflow

An alternative spoken English-fact workflow is available as `main.py` and `.github/workflows/free_fact_shorts.yml`. It makes 36-second, vertical 1080×1920 videos from original title cards with gentle camera motion, using the free `espeak-ng` US-English system voice. It schedules three Shorts per day for 09:00, 14:00, and 18:00 America/New_York. Facts are selected from the small reviewed library in `src/ai_kids_video_agent/free_shorts.py` and each description contains source links. It does not call GPT, ElevenLabs, or Creatomate, and it cannot promise viral views or income. No US proxy is configured: an upload IP does not determine recommendations and a proxy would require a separately managed credential.

To enable it on GitHub:

1. Push/merge this workflow and source code to the repository's **default branch**. GitHub only runs scheduled workflows from that branch.
2. Open **Settings → Secrets and variables → Actions → New repository secret**. Add `YOUTUBE_TOKEN_JSON` with the full contents of your authorized local `%LOCALAPPDATA%\ai-kids-video-agent\token.json`. Do not commit that file or send it in chat. The workflow also accepts `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets for Telegram notifications; use a newly rotated bot token because tokens shared in chat must be considered compromised.
3. In **Actions → Free English Fact Shorts → Run workflow**, keep **Preview** selected first and choose a slot. This generates an artifact without accessing YouTube. Review it. Only when you are ready to upload, run again with **Publish** selected; this uploads one video and schedules it, so it is not a dry run.
4. Only after that test works, disable the old Windows Task Scheduler job with `python -m ai_kids_video_agent.ocean_cli remove-schedule`. Do not run both schedules against the same channel or the channel can receive duplicate daily uploads.

Scheduled runs start one hour before the target release and use GitHub-hosted Linux runners. GitHub Actions usage is subject to the repository's included-minutes quota and workflow delays; runs delayed beyond the preparation window are skipped. External and paid media APIs are not used. Google OAuth tokens created while an OAuth consent app is in **Testing** can expire after seven days; for unattended long-term use, the app owner must complete Google's required publishing/verification steps and refresh/re-save the secret if Google revokes it. YouTube API projects that have not passed the required YouTube audit can be restricted to private uploads, so public release must be checked in YouTube Studio. These limits mean the setup is not fully hands-off until Google authorization and publishing eligibility are stable.

The local Windows ocean-animation schedule and this GitHub Actions fact-video workflow are separate alternatives. Do not run both schedules against the same channel unless you intentionally want both sets of daily uploads.

### Optional Telegram notifications

Create a Telegram bot with [@BotFather](https://t.me/BotFather), open the new bot in Telegram, press **Start**, and send `/start`. Copy the bot token (or the complete BotFather token message), then from the project folder run:

```powershell
python -m ai_kids_video_agent.ocean_cli telegram-setup
```

Paste the copied text at the hidden token prompt; the setup extracts the token from a full BotFather message too. The agent sends a test message, then stores the token locally under `%LOCALAPPDATA%\ai-kids-video-agent\telegram.json` (never share or commit that file). The daily task sends Telegram messages when each Short is successfully scheduled and when a handled rendering/upload error occurs. No phone calls are made.

Set the optional script-generation settings:

```bash
# PowerShell
$env:OPENAI_API_KEY = "your-api-key"
$env:OPENAI_MODEL = "gpt-4o-mini"
# Optional for another OpenAI-compatible service:
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
```

## Run the complete workflow

```bash
ai-news-shorts --output-dir output
```

The CLI lists up to 10 recent stories and uses the newest one by default. Choose a different listed headline with `--story-index 2`, or pass one or more custom RSS/Atom feeds with `--rss https://example.com/feed.xml`. You can also use `NEWS_RSS_URLS` as a comma-separated feed list.

For a headline/script-only run on a machine without Blender and FFmpeg:

```bash
ai-news-shorts --skip-render
```

The same CLI is available without installing the console entry point:

```bash
python -m ai_kids_video_agent --skip-render
```

## Output

- `output/story.json` — selected headline, source, publication date, and feed summary
- `output/story_plan.json` — generated summary, three narration scenes, source attribution, and estimated duration
- `output/youtube_metadata.json` — suggested title, source-linked description, and hashtags
- `output/narration.wav` — spoken English voice track used in the video
- `output/frames/` — uniquely named folders of Blender-rendered frames for each run (rendered at up to 3 FPS, then motion-interpolated to the output frame rate)
- `output/final_short.mp4` — vertical H.264 video with an animated 3D presenter and spoken narration (1080 × 1920, 24 FPS by default)

Progress and warnings are reported by stage. A failed feed is skipped if another feed succeeds; if no usable recent stories remain, the command exits with an actionable error. Blender or FFmpeg failures are reported without removing the headline or script artifacts already generated.

## YouTube Shorts packaging

The first spoken line is written as a truthful hook; captions and a source credit stay on screen while a presenter speaks. Titles and descriptions describe the actual linked report rather than promising guaranteed views. `youtube_metadata.json` is ready to review and paste when publishing.

This packaging is based on [YouTube's Shorts discovery guidance](https://support.google.com/youtube/answer/11914225?hl=en): recommendations are personalized and consider whether viewers choose to watch, how long and what percentage they watch, satisfaction signals, topic interest, and competition. No title, hashtag, VPN, or upload schedule can guarantee a top ranking in 24 hours. After publishing, compare **viewed vs. swiped away**, first-seconds drop-off, and audience retention in YouTube Analytics; use those results to test different animal designs, openings, pacing, and music. The schedule provides an experiment, not a view guarantee.

Run the tests with:

```bash
python -m pytest
```

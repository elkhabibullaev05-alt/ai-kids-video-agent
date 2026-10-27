# Seoul Night Remix — daily production run (instructions for Claude)

Channel: **Seoul Night Remix** — @SeoulNightRemix — Studio id `UCEgWmdwz8gvTmqtDgFMut-A` — Google account eldorbekhabibullaev6 (built-in browser `authuser=5` as of 2026-10-27; re-check with `https://www.youtube.com/getAccountSwitcherEndpoint?authuser=N` from a youtube.com tab). Not made for kids. Owner speaks Uzbek/Kyrgyz.

## Owner's plan (2026-10-28)
- **Every day:** 1 new song as a long music video + **1 Short** cut from that song, linked to it.
- **Every 10 songs:** a ~30-minute mix of the last 10 songs. **Every 20 songs:** a ~1-hour mix of the last 20.
- Music is made in **Suno (Pro plan, owner's account el_khabibullaev05, in the owner's own Chrome = Claude in Chrome tools)**. Only songs created while Pro is active have commercial rights. Songs in the library from before 2026-10-27 were made on the free plan: never upload or remix them.
- The owner gave standing permission for this run to create songs, download them and upload/schedule them. Anything else that needs his permission (payment, new account settings, deleting) → stop and ask him in the final message.

## Owner's style rules (2026-10-28, override anything below)
- **Every song is a love song** (first date, missing someone, confession in the rain, late-night call, breakup and coming back…), told in Seoul night scenes.
- **Strong remix:** hard-hitting dance remix — 124–128 BPM, punchy kick, deep sub bass, big build-up and a loud drop by 0:45, festival energy, catchy female vocal hook. Rotate: K-pop EDM remix · bass house remix · future bass remix · phonk-pop remix.
- **Background = a photorealistic (not anime) beautiful young adult Korean woman** in a neon Seoul night scene, made with Canva generate-image (a fictional AI person — never a real person, celebrity or idol, never anyone who looks under 20). New pose/outfit/place every song, same mood. Owner 2026-10-28: **a different girl look every song, in stylish, more revealing fashion** — rotate: off-shoulder satin mini dress · crop top + high-waist skirt · slip dress · leather jacket over a bodycon dress · summer sundress · sparkly party dress · oversized shirt + shorts. Places rotate: Han river bridge, Hongdae street, convenience store, rooftop, taxi back seat, subway platform, neon alley. Keep it fashion-editorial and tasteful (no lingerie/swimwear, no sexualised poses, no cleavage close-ups): YouTube age-restricts and demonetises suggestive thumbnails, and this channel's goal is ad money. Always a clearly adult woman (mid-twenties). Generate one LANDSCAPE_16_9 and one PORTRAIT_9_16 image with the same outfit/scene. Mark "Altered or synthetic content: Yes" on every upload.
  Full-size image: open `https://www.canva.com/M/<media id>` in Claude in Chrome, take the largest `<img>` and save it to the Downloads folder, stage it, then `render.py cover "TITLE" out.jpg --bg bg.jpg --tag "LOVE REMIX"`; make a PORTRAIT_9_16 version for the Short (`short … --bg bg_vertical.jpg`).
- Title: `Song Title – Love Remix (Seoul Night)`; Short: `POV: he finally called back at 2 AM 🌃 Song Title #shorts`.

## Limits
- Suno Pro = 2,500 credits (≈ 10 per generation) and **20 downloads / month** (renews on the billing date, next 2026-11-22). 1 song/day needs ~30. Check "remaining downloads" on https://suno.com/account first; keep 1 in reserve. If 0 left: skip the new song, still do any due mix from songs already downloaded, and tell the owner ("Suno yuklab olish limiti tugadi — qo'shimcha yuklab olish sotib olinsa davom etaman").
- Never stream-rip Suno audio (cdn URLs) to get around the download limit; only the official Download button.

## Per run
0. **Lock & state.** `git pull`; `seoul/log.json` holds `{"lock":…, "songs":[{n, suno_id, title, file, long_id, short_id, publish_at}], "mixes":[…]}`. Same lock rules as `bolt/AGENT.md` (4 h, remove when done or on failure).
1. **Write the song.** New original English lyrics (verse/pre/chorus ×2, bridge, final chorus), a 2-word title never used before (check log), a theme from Seoul night life (Han river, Hongdae, Namsan, convenience store at 2 a.m., subway line 2, rain on neon…). Rotate styles: K-pop dance pop remix · night-drive synthwave pop · bass house · future bass · lo-fi R&B · city-pop. Always: hook within the first 10 s ("[Intro] short vocal hook" then the beat), 118–128 BPM, female or male vocal alternating. Never name or imitate a real artist or song.
2. **Create in Suno** (Claude in Chrome, your own tab): https://suno.com/create → Advanced/Өркүндөтүлгөн, model v5+/v6. Lyrics editor = `.lyrics-editor-content` (contenteditable: focus, `document.execCommand('insertText', false, lyrics)` — insert line by line with `insertParagraph` so the [Section] tags keep their own lines); style = the textarea whose placeholder starts with the example styles; title = the input "Ырдын аталышы". Click the button with aria-label "Ыр жаратуу"/"Create". Wait ~2–3 min until both versions show a duration.
3. **Pick & download.** Listen-check is impossible, so pick the version whose duration is 2:40–4:00 and whose title shows no error; open its menu → Download → MP3 audio. It lands in the owner's **Downloads** folder (`C:\Users\eldor\Downloads`, must be a connected folder for this conversation's computer; if `device_list_dir` can't see it, stop and tell the owner to add it with "Add folder" in the Claude app).
4. **Bring it here.** `device_stage_files` the new mp3 → `/mnt/user-data/uploads/…`; copy to `seoul/out/<NNN>-<slug>.mp3` in the cloud workspace (not committed — `out/` is in .gitignore).
5. **Render** (`seoul/render.py`, needs ffmpeg + Pillow):
   - `python3 render.py cover "TITLE" out/NNN.jpg --seed NNN --tag "<STYLE IN 2 WORDS>"`
   - `python3 render.py long out/NNN.mp3 out/NNN.jpg out/NNN_long.mp4` (starts at the first loud moment, ≈3x realtime)
   - `python3 render.py short out/NNN.mp3 "<POV hook line>" out/NNN_short.mp4 --seed NNN` (loudest 28 s, 1080×1920, loops)
   - Mix when `len(songs) % 10 == 0`: `python3 render.py mix out/mixNN.mp4 out/mixNN.jpg <last 10 (or 20) mp3s>`; the json gives chapter times for the description. Mix mp3s: re-stage them from Downloads if the workspace was reset.
   Check a frame of each file (Read the jpg) before uploading.
6. **Host temporarily** on the orphan branch `uploads-seoul` (exactly like `hollow/UPLOAD.md` §1). Files over 90 MB: `split -b 90M` into `.partNN` and reassemble in the page with `new Blob([...parts])`.
7. **Upload & schedule** in the built-in browser with the helpers from `hollow/UPLOAD.md` §2–3 (same Studio dialog; this channel's UI may be Uzbek or Russian — match buttons by both). Not made for kids. Release times (UTC; pick minutes not :00/:30, ≥ 30 min ahead): long **12:45–13:45** (Seoul 21:45–22:45), Short **23:15–00:15** (US evening), mix on the next free day at 13:15.
   - **Title formula (Studio AI 2026-10-27):** `Song Title – <Remix style> (<Vibe>)`, e.g. `Neon Rain – Dance Pop Remix (Seoul Night Drive)`; Short: `POV: 2 AM in Seoul 🌃 Neon Rain #shorts`; mix: `1 Hour Seoul Night Drive Mix 🌃 K-Pop Dance Remixes (No Ads Between)` / `30 Min …`. Never a question/CTA as the title.
   - **Description:** 1 mood line, "Full song: <long URL>" (Short) or the chapter list with mm:ss (mix), "Music created with Suno (Pro) — original song by Seoul Night Remix", hashtags `#kpop #nightdrive #remix #seoul`. Lyric question goes in a comment, not the title.
   - **Link the Short to the song:** Studio → the Short → "Related video"/"Видео по теме" → the long video. If Studio asks to verify a phone number, skip and put "Siz: Seoul akkauntida telefon raqamni tasdiqlang (Shorts → Related video)" in the report.
8. **Log, unlock, push** (`seoul/log.json`, never the media). Update the hub: ArtifactData `https://claude.ai/artifact/2itJTvfLFuvUaP66WW2V8r` → `analysis/latest` channels.seoul (`per_day`: 1, `fixes`: today's upload, keep other fields; pin if_version).
9. Final message, Uzbek, 2–4 lines: today's song + Bishkek release times, Suno downloads left, mix status, anything the owner must do.

## Never
Free-plan songs, other artists' songs/voices/names, downloaded music, stream-ripping, passwords, payments, account/Studio settings, deleting anything.


## Growth plan 2026-10-28 — see cloud/growth/PLAN.md (Seoul section)
- Description of every song: 1 mood line + 2 lyric lines + "Music created with Suno (Pro)" + chapters for mixes (human layer against "inauthentic content").
- If a song gets a Content ID claim: do not use it again; generate a new one.

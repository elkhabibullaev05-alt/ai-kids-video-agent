# Owner's channels — Studio ids, Chrome authuser, where each agent lives

Chrome authuser indexes were checked on 2026-11-06. If a channel has moved, re-check with https://studio.youtube.com/?authuser=N.

| key | name | Studio channel id | authuser | agent / guidance files | notes |
|---|---|---|---|---|---|
| roblox | Roblox Top 10 Daily | UCVqJ3Zvk_qPnZDyE5d1bppw | 0 | cloud/makers/roblox.py (+roblox/) | teen/adult only, never kids |
| sleep | Calm Rain for Sleep | UCmDhWfz5KM_sVy58F8i6dEQ | 0 | cloud/makers/sleep.py | 2026-11-14: one cozy animated illustrated rain scene matching the title (drawn by the maker, no stock/watermarks); real rain sound (Commons, credited) matched to the scene |
| max | Max the Curious Cat | UCxHeOROSVQQSZv7zeMaF4Vw | 1 | maxcat/ + cloud/WRITER.md | Made for Kids |
| ufc | Wild Sketchbook (animals) | UCbWs87aJxQxohE0M2MaO7GQ | 1 | cloud/makers/ufc.py + cloud/ink/WRITER_INK.md | no fight footage; free-licence images only |
| seoul | Seoul Night Remix | UCEgWmdwz8gvTmqtDgFMut-A | 2 | seoul/ | Suno Pro songs only; AI backgrounds marked altered/synthetic |
| milo | Milo Survives | UCiaE4voy2yYUHOTDr2wfC5A | 2 | milo/ | |
| hollow | Hollowmere Tales | UCiOfdnuWUlHj5bPi6H5scgA | 3 | hollow/ + cloud/WRITER.md | 13+ |
| dough | Dough Bros | UCsQ8TVoioR_IIJpU_1RE_IA | 3 | doughbros/ + cloud/WRITER.md | Made for Kids; no Ask Studio button (use Analytics) |
| doodle | The Doodle Desk | UCQrteikptRbmzuR8kYD0q8g | 4 | doodle/ | |
| bolt | Inspector Bolt | UCv2hAyDv5m8Rm-0L63a93XQ | 4 | bolt/ + cloud/WRITER.md | Made for Kids |
| money | Money Story Daily | UCyAwBREYT8kQ_3tYLb4CMKg | 5 | cloud/makers/money.py + cloud/makers/money/WRITER.md | |
| funny | Funny Rank Daily | UChKpt9p1vDhAlnWuMMKHUgQ | 5 | cloud/makers/funny.py (+funny/) | every clip CC BY, creator credited |

- Worker config (per-day counts, slots, makers): cloud/channels.json
- Worker: cloud/worker.py
- Live status: cloud/results/<ch>/status.json
- Uploaded videos: cloud/results/<ch>/*.json (id, title, publish_at)

## Browser

Use the owner's Chrome on his laptop through the Claude in Chrome tools (`mcp__claude-in-chrome__*`). Load tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool, computer, get_page_text, find and tabs_close_mcp in ONE ToolSearch call.

The Claude app's built-in browser is NOT signed in to Google, so do not use it.

Work in your own new tab and close it at the end. Keep JavaScript calls short.

## Hard rules (every run)

- Never type passwords.
- Never add accounts.
- Never change account, channel or Studio settings.
- Never touch tokens or credentials.
- Never upload, delete, or make videos private or public.
- Kids flags stay as they are: max, dough and bolt are Made for Kids; roblox and the rest are not.
- No fake engagement.
- No misleading tags, and no clickbait the video does not deliver.
- Never lower a channel's daily upload count. If advice says to upload fewer videos, put it to the owner as a question.
- Owner-only things go to his to-do list: phone verification, re-linking YouTube, retitling published videos.

> **STOPPED 2026-10-29 (owner):** Blocky Quest kids videos must never be made or uploaded to Roblox Top 10 Daily again. The channel is teen/adult Roblox news only (Made for Kids = NO).

# Blocky Quest 3D (on "Roblox Top 10 Daily", UCVqJ3Zvk_qPnZDyE5d1bppw)

- Rendered and uploaded by the owner's PC worker (`cloud/worker.py roblox`, queue `cloud/queue/roblox/`, status `cloud/results/roblox/status.json`).
- Claude only writes jobs (`cloud/WRITER.md`, section roblox).
- The token comes from `Documents\kanal_tokenlar\token_roblox.json`. The owner copies it there himself; Claude never touches token files.
- Story rules: `story/bible.md`. Engine: `engine3d/` (Bolt engine fork; blocky `world.py`; close-ups aim at the face at the top of the body).
- The channel's news Top-10 videos and real gameplay clips come from the separate PC agent `C:\Users\eldor\Documents\robloxtube`.
  - Real gameplay: the owner records his own play (OBS or Win+Alt+R) into `robloxtube\gameplay\`, and the agent cuts it in.
  - Bot play (`mode` ≠ news) breaks Roblox's rules. Keep `mode: "news"`.

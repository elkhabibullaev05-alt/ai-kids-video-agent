#!/usr/bin/env bash
# One-time installs for the cloud/makers/* channel scripts (WSL Ubuntu 24.04 on the owner's laptop).
# Re-running is safe. Other makers may append their own lines below.
set -u

# --- funny (Funny Rank Daily): yt-dlp downloads CC BY source clips from YouTube.
# yt-dlp[default] includes yt-dlp-ejs (YouTube JS challenge scripts). YouTube downloads need a JS runtime:
# deno >= 2.3 (yt-dlp's default) or node >= 22 (funny/fr_source.py passes --js-runtimes node if deno is missing).
pip install --break-system-packages -U "yt-dlp[default]"
if ! command -v deno >/dev/null 2>&1 && [ ! -x "$HOME/.deno/bin/deno" ]; then
  curl -fsSL https://deno.land/install.sh | sh -s -- -y --no-modify-path || echo "deno install failed — install node >= 22 instead"
fi
"$HOME/.deno/bin/deno" --version 2>/dev/null | head -1 || deno --version 2>/dev/null | head -1 || node --version
# yt-dlp breaks when YouTube changes; keep it fresh (cheap): add to cron or run before the worker, e.g.
#   pip install --break-system-packages -U "yt-dlp[default]"   (weekly)

#!/usr/bin/env bash
# Windows PC (WSL) mode: one Windows scheduled task starts this every 20 min.
# Starts channel workers, at most KANAL_PAR at once (one PC, several Blender renders slow each other down),
# then waits so WSL stays alive while they work.
# 2026-10-20: fair turns — the channel that waited longest goes first (before, maxcat+doughbros always took
# both slots and hollow/bolt never ran). A channel without its own token still runs: worker.py picks the
# token whose channel id matches from any ~/kanal/*/token.json and reports "no token" in its status if none.
cd /opt/kanal/repo || exit 1
# 2026-11-08 owner: no internet -> start nothing and wait; this task runs again every 20 min, so work resumes
# by itself as soon as the internet is back (uploads already in progress pause and continue, see youtube_up.py).
if ! timeout 15 bash -c 'exec 3<>/dev/tcp/www.googleapis.com/443' 2>/dev/null && \
   ! timeout 15 bash -c 'exec 3<>/dev/tcp/github.com/443' 2>/dev/null; then
  mkdir -p /root/kanal; echo "$(date -u) internet yo'q - kutilmoqda" >> /root/kanal/offline.log; exit 0
fi
# 2026-11-06: owner can pause all channel work (e.g. so a big game download gets the whole internet):
# cloud/pause_until holds an ISO UTC time; until then nothing starts. Pulled here so a pause pushed from outside arrives.
GIT_TERMINAL_PROMPT=0 timeout 120 git pull -q --rebase --autostash 2>/dev/null
# 2026-11-08: un-stick git + push waiting status + report to Documents\kanal_holat.txt (at most every 20 min)
[ -f cloud/pc_git_heal.sh ] && timeout 400 bash cloud/pc_git_heal.sh
if [ -f cloud/pause_until ] && [ "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \< "$(head -c 20 cloud/pause_until)" ]; then
  echo "$(date -u) paused until $(cat cloud/pause_until)" >> /root/kanal/pause.log; exit 0
fi
# makers need extra tools (yt-dlp …) — installed once per change of cloud/makers/setup.sh
if [ -f cloud/makers/setup.sh ] && ! cmp -s cloud/makers/setup.sh /root/kanal/.makers_setup 2>/dev/null; then
  bash cloud/makers/setup.sh >> /root/kanal/makers_setup.log 2>&1 && mkdir -p /root/kanal && cp cloud/makers/setup.sh /root/kanal/.makers_setup
fi
# 2026-11-09 watchdog: funny (Funny Rank) failed every run since 8 Nov ("no Short made"); yt-dlp breaks whenever
# YouTube changes and setup.sh only ran once. Keep yt-dlp fresh: upgrade at most once a day.
if [ "$(cat /root/kanal/.ytdlp_day 2>/dev/null)" != "$(date -u +%F)" ]; then
  timeout 300 pip install --break-system-packages -q -U "yt-dlp[default]" >> /root/kanal/makers_setup.log 2>&1 && \
    date -u +%F > /root/kanal/.ytdlp_day
fi
PAR=${KANAL_PAR:-3}  # 2026-11-06: 10 channels now (makers are mostly ffmpeg, lighter than Blender)
# 2026-11-09: while the owner plays a game (Call of Duty etc.) the laptop runs out of memory and Windows kills WSL
# mid-render (jobs restarted every 20 min, git objects left empty). During a game: only 1 channel at a time.
if /mnt/c/Windows/System32/tasklist.exe /NH 2>/dev/null | grep -qiE '^(cod\.exe|sp[0-9]+-cod|mp[0-9]+-cod|cod[0-9]+|FortniteClient|RobloxPlayerBeta|NFS|BeamNG)'; then
  PAR=1; echo "$(date -u) game running -> PAR=1" >> /root/kanal/game.log
fi
TOK=$(ls -d /mnt/c/Users/*/Documents/kanal_tokenlar 2>/dev/null | head -1)
CHS="maxcat doughbros hollow bolt roblox funny money ufc sleep"  # 2026-11-06 owner: grind paused for now (no token, not needed yet); funny money ufc sleep + roblox rebuilt as makers (cloud/makers/) after the old laptop died.
# 2026-10-27: sleep (Calm Rain) removed — owner wants it back to its own real-rain agent (sleeptube), no AI videos
# 2026-11-05: stories Claude writes on the PC (Documents\kanal_navbat\<ch>\*.json) go into the queue
NAV=$(ls -d /mnt/c/Users/*/Documents/kanal_navbat 2>/dev/null | head -1)
if [ -n "$NAV" ] && ls "$NAV"/*/*.json >/dev/null 2>&1; then
  ( flock 9
    for f in "$NAV"/*/*.json; do
      ch=$(basename "$(dirname "$f")"); mkdir -p cloud/queue/$ch
      python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$f" && mv -f "$f" cloud/queue/$ch/ || mv -f "$f" "$f.bad"
    done
    git add -A cloud/queue
    git -c user.name=kanal-worker -c user.email=worker@kanal.local commit -qm "[pc] stories from kanal_navbat" && \
      (GIT_TERMINAL_PROMPT=0 git push -q origin HEAD:main || (git pull -q --rebase && git push -q origin HEAD:main))
  ) 9>/tmp/kanal-git.lock
fi
running=0
for ch in $CHS; do
  mkdir -p /root/kanal/$ch
  [ -n "$TOK" ] && [ -s "$TOK/token_$ch.json" ] && cp -f "$TOK/token_$ch.json" /root/kanal/$ch/token.json
  if ! flock -n /tmp/kanal-$ch.lock -c true; then running=$((running+1)); fi
done
# oldest last start first
order=$(for ch in $CHS; do echo "$(cat /root/kanal/$ch/.last_start 2>/dev/null || echo 0) $ch"; done | sort -n | awk '{print $2}')
for ch in $order; do
  [ $running -ge $PAR ] && break
  if flock -n /tmp/kanal-$ch.lock -c true; then
    date +%s > /root/kanal/$ch/.last_start
    # 2026-11-06: timeout — never let one hung worker hold its slot forever
    flock -n /tmp/kanal-$ch.lock timeout -k 60 5h python3 cloud/worker.py $ch >> /root/kanal/$ch/worker.log 2>&1 &
    running=$((running+1)); sleep 5
  fi
done
wait

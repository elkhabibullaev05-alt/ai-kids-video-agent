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
# 2026-11-09: two separate slot pools. Before, the 3D Blender channels (hours per episode) held all 3 slots and the
# light ffmpeg "maker" channels (funny = 12 Shorts/day, money, ufc, sleep, roblox) waited for hours -> Funny Rank starved.
MAKERS="funny money ufc sleep roblox"
PAR3D=${KANAL_PAR3D:-2}; PARMK=${KANAL_PARMK:-5}  # 2026-11-09: all 5 light makers at once — idle ones exit in seconds; with 2 slots Funny waited behind idle channels
[ "$PAR" = "1" ] && { PAR3D=1; PARMK=3; }   # a game is running: one 3D render, light makers still run
for ch in $CHS; do
  mkdir -p /root/kanal/$ch
  [ -n "$TOK" ] && [ -s "$TOK/token_$ch.json" ] && cp -f "$TOK/token_$ch.json" /root/kanal/$ch/token.json
done
start_pool() {  # $1 = max parallel, rest = channels of this pool
  local max=$1; shift; local running=0 ch order
  for ch in "$@"; do flock -n /tmp/kanal-$ch.lock -c true || running=$((running+1)); done
  order=$(for ch in "$@"; do echo "$(cat /root/kanal/$ch/.last_start 2>/dev/null || echo 0) $ch"; done | sort -n | awk '{print $2}')
  for ch in $order; do
    [ $running -ge $max ] && break
    if flock -n /tmp/kanal-$ch.lock -c true; then
      date +%s > /root/kanal/$ch/.last_start
      # 2026-11-06: timeout — never let one hung worker hold its slot forever
      flock -n /tmp/kanal-$ch.lock timeout -k 60 5h python3 cloud/worker.py $ch >> /root/kanal/$ch/worker.log 2>&1 &
      running=$((running+1)); sleep 5
    fi
  done
}
mk=""; d3=""
for ch in $CHS; do case " $MAKERS " in *" $ch "*) mk="$mk $ch";; *) d3="$d3 $ch";; esac; done
# 2026-11-10 owner: CoD gameplay editor (1 long video + 3 Shorts per mission). Runs once per job file,
# resumes if interrupted (finished files are skipped). Output + progress: Videos\MW4\tayyor\holat.txt
if [ -f cloud/cod/job.json ]; then
  J=$(md5sum cloud/cod/job.json | cut -c1-12); mkdir -p /root/kanal/cod
  if [ ! -f /root/kanal/cod/done_$J ]; then
    ( flock -n 9 || exit 0
      nice -n 5 timeout 8h python3 cloud/cod/cod_edit.py cloud/cod/job.json >> /root/kanal/cod/edit.log 2>&1 && touch /root/kanal/cod/done_$J
    ) 9>/tmp/kanal-cod.lock &
  fi
fi
# 2026-11-13 owner: games he plays are recorded by Documents\avto_yozish\game_rec.py -> auto Shorts here (not uploaded
# until Claude approves them in cloud/cod/v4_ok.json)
if ls /mnt/c/Users/*/Documents/kanal_navbat/gameplay/*.json >/dev/null 2>&1; then
  ( flock -n 6 || exit 0; nice -n 6 timeout 6h python3 cloud/cod/auto_gameplay.py >> /root/kanal/cod/auto.log 2>&1 ) 6>/tmp/kanal-auto.lock &

# 2026-11-13: Gemini watches YouTube links (cloud/cod/yt_savollar/*.json) -> E:\MW4_tayyor\gemini\yt_*.txt
( flock -n 7 || exit 0; timeout 2h python3 cloud/cod/yt_korish.py >> /root/kanal/cod/yt_korish.log 2>&1 ) 7>/tmp/kanal-yt.lock &
fi
# 2026-11-11 owner: upload the edited MW4 videos to MW4 Campaign HD (own Cloud project), 1 long + 3 Shorts a day
if [ -s /root/kanal/cod/token.json ] && [ -f cloud/cod/cod_upload.py ]; then
  ( flock -n 8 || exit 0; timeout 14h python3 cloud/cod/cod_upload.py >> /root/kanal/cod/upload.log 2>&1 ) 8>/tmp/kanal-codup.lock &
fi
# 2026-11-11 owner: 2nd, Shorts-only channel MW4 Shorts Daily (its own B-set Shorts, each linking to the full mission)
if [ -s /root/kanal/cod2/token.json ] && [ -f cloud/cod/cod_upload.py ]; then
  ( flock -n 7 || exit 0; COD_CH=2 timeout 6h python3 cloud/cod/cod_upload.py >> /root/kanal/cod2/upload.log 2>&1 ) 7>/tmp/kanal-codup2.lock &
fi
start_pool $PARMK $mk
start_pool $PAR3D $d3
wait

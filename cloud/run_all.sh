#!/usr/bin/env bash
# Windows PC (WSL) mode: one Windows scheduled task starts this every 20 min.
# Starts channel workers, at most KANAL_PAR at once (one PC, several Blender renders slow each other down),
# then waits so WSL stays alive while they work.
# 2026-10-20: fair turns — the channel that waited longest goes first (before, maxcat+doughbros always took
# both slots and hollow/bolt never ran). A channel without its own token still runs: worker.py picks the
# token whose channel id matches from any ~/kanal/*/token.json and reports "no token" in its status if none.
cd /opt/kanal/repo || exit 1
PAR=${KANAL_PAR:-2}
TOK=$(ls -d /mnt/c/Users/*/Documents/kanal_tokenlar 2>/dev/null | head -1)
CHS="maxcat doughbros hollow bolt roblox grind"  # 2026-10-27: sleep (Calm Rain) removed — owner wants it back to its own real-rain agent (sleeptube), no AI videos
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
    flock -n /tmp/kanal-$ch.lock python3 cloud/worker.py $ch >> /root/kanal/$ch/worker.log 2>&1 &
    running=$((running+1)); sleep 5
  fi
done
wait

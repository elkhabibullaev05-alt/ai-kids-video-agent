#!/usr/bin/env bash
# Windows PC (WSL) mode: one Windows scheduled task starts this every 20 min.
# Starts the worker of every channel that has a token and is not already busy, at most KANAL_PAR at once
# (one PC, several Blender renders slow each other down), then waits so WSL stays alive while they work.
cd /opt/kanal/repo || exit 1
PAR=${KANAL_PAR:-2}
TOK=$(ls -d /mnt/c/Users/*/Documents/kanal_tokenlar 2>/dev/null | head -1)
running=0
for ch in maxcat doughbros hollow bolt; do
  mkdir -p /root/kanal/$ch
  [ -n "$TOK" ] && [ -s "$TOK/token_$ch.json" ] && cp -f "$TOK/token_$ch.json" /root/kanal/$ch/token.json
  [ -s /root/kanal/$ch/token.json ] || continue
  if ! flock -n /tmp/kanal-$ch.lock -c true; then running=$((running+1)); fi
done
for ch in maxcat doughbros hollow bolt; do
  [ -s /root/kanal/$ch/token.json ] || continue
  [ $running -ge $PAR ] && break
  if flock -n /tmp/kanal-$ch.lock -c true; then
    flock -n /tmp/kanal-$ch.lock python3 cloud/worker.py $ch >> /root/kanal/$ch/worker.log 2>&1 &
    running=$((running+1)); sleep 5
  fi
done
wait

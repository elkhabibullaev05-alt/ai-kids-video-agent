#!/usr/bin/env bash
# out/epNNN: 12 fps frames ("on twos") -> 24 fps 16:9 (4K by default), burned subtitles, audio.wav
# usage: engine/assemble_long.sh out/epNNN OUT.mp4 [W H]
set -e
D=$1; OUT=$2; W=${3:-1920}; H=${4:-1080}  # 2026-11-11 owner: crisp Full HD (480p frames blown up to 4K at 4.5 Mbit looked soft/blocky)
# GPU encoder (RTX) when available: far faster than x264 medium, so the saved time goes into sharper renders
if ffmpeg -hide_banner -v error -f lavfi -i color=s=256x256:d=0.1 -c:v h264_nvenc -f null - 2>/dev/null; then
  VENC="-c:v h264_nvenc -preset p6 -tune hq -rc vbr -cq ${CQ:-19} -b:v 0 -maxrate 14M -bufsize 28M -spatial-aq 1 -profile:v high"
else
  VENC="-c:v libx264 -preset ${P:-medium} -crf ${CRF:-19} -maxrate ${MAXRATE:-12M} -bufsize 24M"
fi
python3 "$(dirname "$0")/subs.py" "$D"
ffmpeg -v error -y -framerate 12 -i "$D/frames/f_%04d.png" -i "$D/audio.wav" \
  -filter_complex "[0:v]fps=24,scale=$W:$H:flags=lanczos,unsharp=5:5:0.8:5:5:0.0,eq=saturation=1.12:contrast=1.04,ass=$D/subs.ass,format=yuv420p[v]" \
  -map "[v]" -map 1:a -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" $VENC -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart "$OUT"
echo "$OUT"

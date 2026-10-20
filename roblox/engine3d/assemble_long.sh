#!/usr/bin/env bash
# out/epNNN: 12 fps frames ("on twos") -> 24 fps 16:9 (4K by default), burned subtitles, audio.wav
# usage: engine/assemble_long.sh out/epNNN OUT.mp4 [W H]
set -e
D=$1; OUT=$2; W=${3:-3840}; H=${4:-2160}
python3 "$(dirname "$0")/subs.py" "$D"
ffmpeg -v error -y -framerate 12 -i "$D/frames/f_%04d.png" -i "$D/audio.wav" \
  -filter_complex "[0:v]fps=24,scale=$W:$H:flags=lanczos,unsharp=5:5:0.7:5:5:0.0,ass=$D/subs.ass,format=yuv420p[v]" \
  -map "[v]" -map 1:a -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" -c:v libx264 -preset ${P:-medium} -crf ${CRF:-22} -maxrate ${MAXRATE:-4.5M} -bufsize 9M -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart "$OUT"
echo "$OUT"

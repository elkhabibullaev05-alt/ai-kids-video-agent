#!/usr/bin/env bash
# Render every song segment (resumable: finished frames are skipped). usage: songs/render_all.sh out3d/songs
cd "$(dirname "$0")/.."
BL=/opt/bl/blender-4.2.3-linux-x64/blender
R=${1:-out3d/songs}
for tl in $(ls -d $R/*/seg_* | sort); do
  n=$(python3 -c "import json;t=json.load(open('$tl/timeline.json'));print(int(round(t['duration']*12))+1)")
  have=$(ls $tl/frames/f_*.png 2>/dev/null | wc -l)
  if [ "$have" -ge "$n" ]; then echo "done $tl"; continue; fi
  echo "render $tl ($have/$n) $(date -u +%H:%M)"
  $BL -b --factory-startup -P engine3d/story.py -- --tl $tl/timeline.json --out $tl/frames --res 854 --samples 1 > $tl/render.log 2>&1
done
echo ALL_RENDERED

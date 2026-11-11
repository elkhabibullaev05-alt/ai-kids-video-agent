#!/usr/bin/env python3
"""2026-11-11: analyse a new gameplay recording for Claude: keyframe contact sheets (with timestamps),
keyframe 64x36 gray features and per-second audio RMS -> OUT dir (on C:, readable by Claude)."""
import os, sys, subprocess, re, numpy as np
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
def run(c): subprocess.run(c, check=True)
# 1) contact sheets, one frame / 8 s
th = os.path.join(out, "th"); os.makedirs(th, exist_ok=True)
run(["ffmpeg", "-y", "-v", "error", "-skip_frame", "nokey", "-i", src, "-an", "-vsync", "vfr", "-vf",
     "fps=1/8,scale=256:144,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{pts\\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black",
     os.path.join(th, "t_%04d.jpg")])
run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(th, "t_%04d.jpg"), "-vf", "tile=8x6", "-q:v", "4",
     os.path.join(out, "sheet_%02d.jpg")])
# 2) keyframe features
p = subprocess.run(["ffmpeg", "-v", "info", "-skip_frame", "nokey", "-i", src, "-an", "-vsync", "0", "-vf",
                    "scale=64:36,format=gray,showinfo", "-f", "rawvideo", "-"], capture_output=True)
ts = [float(x) for x in re.findall(rb"pts_time:([0-9.]+)", p.stderr)]
F = np.frombuffer(p.stdout, np.uint8).reshape(-1, 36, 64)
m = min(len(ts), len(F)); np.savez_compressed(os.path.join(out, "keys.npz"), T=np.array(ts[:m]), F=F[:m])
# 3) audio rms per second
a = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(a, np.int16).astype(np.float32) / 32768; n = len(x) // 8000
np.save(os.path.join(out, "rms.npy"), np.sqrt((x[:n*8000].reshape(n, 8000) ** 2).mean(1)))
open(os.path.join(out, "TAYYOR.txt"), "w").write("ok\n")
print("analysis done")

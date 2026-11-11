#!/usr/bin/env python3
"""2026-11-11 owner: "only the parts where I shoot / get hit, montage those, make Shorts".
Finds the combat in a gameplay recording from the sound: gunfire, hits and explosions are sharp high-frequency
transients, so we count transients per second (2-8 kHz band) and add on-screen motion. Seconds with fire are
grown by a little padding and merged into combat segments; loading screens, menus, walking and cutscene talk
drop out. Writes <out>/action.json (segments + ranked peaks) and a contact sheet of the top peaks for Claude.
usage: cod_action.py SRC OUTDIR"""
import os, sys, json, subprocess
import numpy as np

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
SR, HOP = 16000, 400            # 25 ms frames

def log(*a):
    print(*a, flush=True); open(os.path.join(out, "aksiya_holat.txt"), "a").write(" ".join(map(str, a)) + "\n")

log("ovoz tahlili boshlandi:", src)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", str(SR),
                      "-af", "highpass=f=2000,lowpass=f=8000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
n = len(x) // HOP
e = np.log1p(200 * np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1)))
fps = SR / HOP                                   # 40 frames / s
# onset = jump over the local floor (median of the previous 0.5 s) and loud enough overall
k = int(fps / 2)
pad = np.r_[np.full(k, e[0]), e]
floor = np.array([np.median(pad[i:i + k]) for i in range(0, n)]) if n < 4000 else None
if floor is None:  # fast running median via strided percentiles on 0.5 s blocks
    blk = np.r_[e, np.full((-n) % k, e[-1])].reshape(-1, k)
    bm = np.median(blk, 1); floor = np.repeat(np.r_[bm[0], bm[:-1]], k)[:n]
thr = np.percentile(e, 75)
onset = (e - floor > 0.35) & (e > thr)
onset &= np.r_[True, ~onset[:-1]]                # count each burst start once
S = n // int(fps)
shots = onset[:S * int(fps)].reshape(S, int(fps)).sum(1).astype(float)
loud = e[:S * int(fps)].reshape(S, int(fps)).max(1)
log(f"ovoz: {S} s, o'q/zarba belgilari jami {int(shots.sum())}")

# motion, 2 fps, tiny gray frames
log("harakat tahlili...")
rv = subprocess.run(["ffmpeg", "-v", "error", "-hwaccel", "auto", "-i", src, "-an", "-vf",
                     "fps=2,scale=96:54,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(rv, np.uint8).reshape(-1, 54, 96).astype(np.float32)
mo = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
m1 = np.array([mo[i * 2:(i + 1) * 2].mean() if i * 2 < len(mo) else 0 for i in range(S)])
dark = np.array([fr[min(i * 2, len(fr) - 1)].mean() < 18 for i in range(S)])   # black/loading frames

z = lambda v: (v - v.mean()) / (v.std() + 1e-6)
score = np.convolve(shots, np.ones(3) / 3, "same") * 1.0 + 0.6 * np.clip(z(m1), -1, 3)
fire = (np.convolve(shots, np.ones(3), "same") >= 3) & ~dark      # >=3 transients within 3 s = a fight
# grow, merge, filter
grow = np.convolve(fire.astype(float), np.ones(5), "same") > 0      # +-2 s around every fight second
seg, i = [], 0
while i < S:
    if grow[i]:
        j = i
        while j < S and grow[j]: j += 1
        seg.append([max(0, i - 0.5), min(S, j + 1.0)]); i = j
    else:
        i += 1
merged = []
for a, b in seg:
    if merged and a - merged[-1][1] < 5: merged[-1][1] = b
    else: merged.append([a, b])
merged = [[float(a), float(b)] for a, b in merged if b - a >= 4]
tot = sum(b - a for a, b in merged)
log(f"jang bo'laklari: {len(merged)} ta, jami {tot/60:.1f} daqiqa (yozuv {S/60:.1f} daqiqa)")

# ranked peaks (3 s windows) for Shorts hooks, at least 20 s apart
win = np.convolve(score, np.ones(3), "same")
peaks = []
for t in np.argsort(-win):
    if fire[t] and all(abs(t - u) > 20 for u in peaks): peaks.append(int(t))
    if len(peaks) >= 40: break
json.dump({"src": src, "dur": S, "segments": merged, "peaks": peaks,
           "shots_per_s": [int(v) for v in shots]}, open(os.path.join(out, "action.json"), "w"))
# contact sheet of the top 24 peaks so Claude can check they really are fights
th = os.path.join(out, "pk"); os.makedirs(th, exist_ok=True)
for q, t in enumerate(peaks[:24]):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf",
                    f"scale=320:180,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                    f"text='{q} {t//60}m{t%60:02d}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black",
                    os.path.join(th, f"p_{q:02d}.jpg")])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(th, "p_%02d.jpg"), "-vf", "tile=6x4",
                "-q:v", "4", os.path.join(out, "peaks_sheet.jpg")])
open(os.path.join(out, "TAYYOR.txt"), "w").write("ok\n")
log("TAYYOR")

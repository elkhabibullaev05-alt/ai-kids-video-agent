#!/usr/bin/env python3
"""2026-11-11 owner: v3 Shorts rejected ("sifatsiz, musiqa tushmayapti, kamera o'ynab yuribdi, o'rtada sichqoncha").
v4 = what the most-viewed MW4/COD Shorts do (vidIQ, 1-2.6M views: Game Record, PlayerKai, Major Alex, EFFECTOR):
  * ONE continuous action moment (no 1.5 s chop), centred on a real firefight found from the gunfire analysis
  * camera stabilised (vidstab, heavy smoothing) -> the view glides instead of jerking with the stick
  * Windows mouse cursor in the middle of the screen removed (delogo at the detected spot)
  * brighter, crisper picture: lifted shadows, a little more colour, denoise -> sharpen, downscaled (never upscaled)
  * speed ramp: the hottest second plays in slow motion with a punch-in zoom, landing on the music's drop
  * white header card with a bold 2-line hook (one word red), like the viral COD Shorts; game sound stays the
    main layer, the music sits under it and is lined up so its drop hits the slow-motion moment
usage: short4.py spec.json   (spec: src, t, out, hook, red, music, pre, post, tag)"""
import os, sys, json, subprocess, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
sp = json.load(open(sys.argv[1]))
src, T, out = sp["src"], float(sp["t"]), sp["out"]
PRE, POST = float(sp.get("pre", 9)), float(sp.get("post", 8))
# 2026-11-12: two editor runs (worker + manual) rendered the same Short into one tmp dir -> one lock per output
import time
lk = out + ".lock"
if os.path.exists(out):
    print("bor, o'tkazildi", flush=True); sys.exit(0)
try:
    if os.path.exists(lk) and time.time() - os.path.getmtime(lk) > 1800: os.remove(lk)
    os.close(os.open(lk, os.O_CREAT | os.O_EXCL))
except FileExistsError:
    print("boshqa jarayon yasayapti, o'tkazildi", flush=True); sys.exit(0)
import atexit; atexit.register(lambda: os.path.exists(lk) and os.remove(lk))
tmp = out + "_tmp"; os.makedirs(tmp, exist_ok=True)
# 2026-11-12 review of V1: 8 s of looking at bodies on the ground after the fight -> boring tail.
# With the gunfire map (cod_action.py) start on the first shots before the peak and stop 1.5 s after the last one.
if sp.get("action") and os.path.exists(sp["action"]):
    sh = json.load(open(sp["action"]))["shots_per_s"]; t0 = int(T)
    c = lambda i: sum(sh[max(0, i):i + 2]) if 0 <= i < len(sh) else 0
    st = next((i for i in range(t0 - 8, t0 - 1) if c(i) >= 2), t0 - 4)
    en = t0
    for i in range(t0, min(len(sh), t0 + 14)):
        if sh[i] > 0: en = i
        elif i - en > 3: break
    PRE = max(3.0, min(8.0, T - st))        # 2026-11-14 owner: first frame = shots already flying (no run-up)
    POST = max(5.0, min(12.0, en - T + 1.5))
    print(f"oyna: {PRE:.1f}s oldin, {POST:.1f}s keyin (otishma xaritasidan)", flush=True)
# 2026-11-14 owner (MW4 rules): Shorts 9-15 s. Final length = PRE + POST + 1.5 (slow-motion second) -> PRE+POST in 7.5..13.5
if PRE + POST > 13.5: POST = max(4.0, 13.5 - PRE); PRE = min(PRE, 13.5 - POST)
if PRE + POST < 7.5: POST = 7.5 - PRE

def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(" ".join(c[:6]) + "\n" + r.stderr[-1500:])
    return r

def nvenc_ok():
    try:
        run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=s=256x256:d=0.1", "-c:v", "h264_nvenc", "-f", "null", "-"]); return True
    except Exception: return False
NV = nvenc_ok()
def venc(q=16):
    return (["-c:v", "h264_nvenc", "-preset", "p7", "-tune", "hq", "-rc", "vbr", "-cq", str(q), "-b:v", "0", "-profile:v", "high"]
            if NV else ["-c:v", "libx264", "-preset", "medium", "-crf", str(q + 1)]) + ["-pix_fmt", "yuv420p"]

# ---- 1) where is the mouse cursor? median of 40 frames keeps only what never moves (HUD + cursor)
def find_cursor():
    fr = []
    for k in range(40):
        t = max(0, T - PRE) + k * (PRE + POST) / 40
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf",
                              "crop=240:240:840:420,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        if len(raw) == 240 * 240: fr.append(np.frombuffer(raw, np.uint8).reshape(240, 240))
    if len(fr) < 10: return None
    F = np.stack(fr).astype(np.float32); med = np.median(F, 0); var = F.std(0)
    m = (med > 200) & (var < 25)          # bright and static = the white arrow
    ys, xs = np.nonzero(m)
    if len(xs) < 15 or len(xs) > 900: return None
    x0, y0, x1, y1 = xs.min() + 840, ys.min() + 420, xs.max() + 840, ys.max() + 420
    return max(1, x0 - 4), max(1, y0 - 4), min(40, x1 - x0 + 9), min(48, y1 - y0 + 9)
cur = find_cursor()   # None -> nothing static found, leave the picture untouched
print("cursor box:", cur, flush=True)

# ---- 2) cut the moment, clean it, stabilise it
a = max(0.0, T - PRE); dur = PRE + POST
clip = os.path.join(tmp, "clip.mov"); trf = os.path.join(tmp, "t.trf"); stab = os.path.join(tmp, "stab.mov")
dl = f"delogo=x={cur[0]}:y={cur[1]}:w={cur[2]}:h={cur[3]}" if cur else "null"
# 2026-11-12: game played in a window -> OBS frame has the window title bar + Windows taskbar; cut them off first
vf0 = dl + ("," + sp["src_crop"] + ",scale=1920:1080:flags=lanczos" if sp.get("src_crop") else "")
run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vf",
     vf0, "-af", "aresample=48000"] + venc(14) + ["-c:a", "pcm_s16le", clip])
run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vf", f"vidstabdetect=shakiness=7:accuracy=15:result={trf}", "-f", "null", "-"])
GRADE = ("hqdn3d=1.5:1.5:3:3,"
         "curves=all='0/0 0.05/0.09 0.25/0.34 0.5/0.6 0.8/0.86 1/1',"
         "eq=saturation=1.22:contrast=1.06,unsharp=5:5:0.6:5:5:0")
run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vf",
     f"vidstabtransform=input={trf}:smoothing=40:optzoom=0:zoom=7:interpol=bicubic,{GRADE}",
     "-c:a", "copy"] + venc(14) + [stab])

# ---- 3) speed ramp: [0, s0) normal | [s0, s1) 0.5x + punch-in | [s1, end) normal
s0, s1 = PRE - 0.6, PRE + 0.9
parts = []
def piece(i, t0, t1, slow=False):
    p = os.path.join(tmp, f"p{i}.mov")
    vf = "setpts=PTS-STARTPTS"
    af = "asetpts=PTS-STARTPTS"
    if slow:
        n = int((t1 - t0) * 2 * 60)
        vf = (f"setpts=2*(PTS-STARTPTS),fps=60,zoompan=z='1+0.14*min(on/{n*0.35:.0f},1)':d=1:"
              f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=60")
        af = "asetpts=PTS-STARTPTS,asetrate=48000*0.75,aresample=48000,atempo=0.6667"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1-t0:.3f}", "-i", stab, "-vf", vf, "-af", af,
         "-r", "60"] + venc(14) + ["-c:a", "pcm_s16le", p])
    parts.append(p)
piece(0, 0, s0); piece(1, s0, s1, True); piece(2, s1, dur)
lst = os.path.join(tmp, "l.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
body = os.path.join(tmp, "body.mov")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])
total = s0 + 2 * (s1 - s0) + (dur - s1)
HIT = s0                                   # where the slow motion starts on the final timeline

# ---- 4) music lined up: its drop (biggest energy jump, on a beat) lands on HIT
def music_plan(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "11025", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; hop = 256; fps = 11025 / hop
    n = len(x) // hop; e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))
    on = np.maximum(np.diff(np.log1p(100 * e), prepend=0), 0); on -= on.mean()
    ac = np.correlate(on[:int(fps * 60)], on[:int(fps * 60)], "full")[int(fps * 60) - 1:]
    lags = np.arange(len(ac)); bpm = 60 * fps / np.maximum(lags, 1); ok = (bpm >= 80) & (bpm <= 170)
    L = lags[ok][np.argmax(ac[ok])]; per = L / fps
    ph = max(range(int(L)), key=lambda p: on[p::int(L)].sum()) / fps
    sm = np.convolve(e, np.ones(int(fps * 2)) / int(fps * 2), "same")
    W = int(fps * 2.5); best, D = -1, None
    for i in range(int(fps * (HIT + 1)), n - int(fps * (total - HIT + 1))):
        j = sm[i:i + W].mean() - sm[i - W:i].mean()
        if j > best: best, D = j, i / fps
    if D is None: return None
    k = round((D - ph) / per); D = ph + k * per
    return max(0.0, D - HIT), 60 / per
mp = os.path.join(sp.get("music_dir", ""), sp["music"]) if sp.get("music") else None
mus = music_plan(mp) if mp and os.path.exists(mp) else None
print("music:", mp, mus, flush=True)

# ---- 5) layout 1080x1920: header card, crisp 4:3.6 window, footer
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")
hook = sp["hook"].upper(); red = (sp.get("red") or "").upper()
words = hook.split(); lines, cur_l = [], ""
for wd in words:
    if len(cur_l) + len(wd) + 1 > 17 and cur_l: lines.append(cur_l); cur_l = wd
    else: cur_l = (cur_l + " " + wd).strip()
lines.append(cur_l); lines = lines[:3]
fs = 84 if len(lines) <= 2 else 70; lh = int(fs * 1.18)
card_h = len(lines) * lh + 70; card_y = 150
txt = [f"drawbox=x=50:y={card_y}:w=980:h={card_h}:color=white@1:t=fill"]
for i, ln in enumerate(lines):
    yy = card_y + 38 + i * lh
    if red and red in ln.split():
        # draw the line in black, then the red word over it at the same advance position
        pre_txt = ln[:ln.index(red)]
        txt.append(f"drawtext=fontfile='{FONT}':text='{esc(ln)}':fontsize={fs}:fontcolor=black:x=(w-text_w)/2:y={yy}")
        # width of the prefix measured with the same font: use a hidden draw to get it is not possible in one pass,
        # so the red word gets its own line position from a Pillow measurement
        try:
            from PIL import ImageFont
            f = ImageFont.truetype(FONT, fs); full = f.getlength(ln); px = f.getlength(pre_txt)
            txt.append(f"drawtext=fontfile='{FONT}':text='{esc(red)}':fontsize={fs}:fontcolor=0xE0201B:"
                       f"x=(w-{full:.0f})/2+{px:.0f}:y={yy}")
        except Exception:
            pass
    else:
        txt.append(f"drawtext=fontfile='{FONT}':text='{esc(ln)}':fontsize={fs}:fontcolor=black:x=(w-text_w)/2:y={yy}")
foot = esc(sp.get("tag", "FULL MISSION ON THE CHANNEL"))
VY = card_y + card_h + 30
fc = ("[0:v]split[s1][s2];[s1]crop=960:1080:480:0,scale=1080:1215:flags=lanczos,unsharp=3:3:0.35,setsar=1[v0];"
      "[s2]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:4,"
      "eq=brightness=-0.32:saturation=0.8[bg];"
      f"[bg][v0]overlay=0:{VY}," + ",".join(txt) + ","
      f"drawbox=x=0:y={VY+1215}:w=1080:h=6:color=0xE0201B@1:t=fill,"
      f"drawtext=fontfile='{FONT}':text='{foot}':fontsize=46:fontcolor=white:x=(w-text_w)/2:y={VY+1215+28},"
      "null[v]")   # 2026-11-14 owner: no fade from/to black -> starts on action and loops into its start
V5 = sp.get("style") == "v5"
if V5:
    # 2026-11-12 Gemini (asked "how do COD Shorts reach millions"): no card/frame - full-bleed 9:16 crop kept a bit right
    # of centre (gun + target), hook in yellow with a thick black outline at 13 % height, one punchy word popping on the hit,
    # no fade to black (the end loops into the start), self-made riser + sub boom on the slow-motion hit, music louder.
    def yl(i, ln, fs2):
        return (f"drawtext=fontfile='{FONT}':text='{esc(ln)}':fontsize={fs2}:fontcolor=0xFFE600:borderw=7:bordercolor=black:"
                f"x=(w-text_w)/2:y={int(1920*0.12) + i*int(fs2*1.12)}")
    fs2 = 92 if len(lines) <= 2 else 76
    pop = esc((sp.get("pop") or "NO MERCY").upper())
    fc = ("[0:v]crop=ih*9/16:ih:(iw-ow)*0.55:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.55,setsar=1,"
          + ",".join(yl(i, ln, fs2) for i, ln in enumerate(lines[:2])) + ","
          f"drawtext=fontfile='{FONT}':text='{pop}':fontcolor=white:borderw=8:bordercolor=0xE0201B:x=(w-text_w)/2:y=h*0.60:"
          f"fontsize='110+40*max(0,1-(t-{HIT:.2f})*6)':enable='between(t,{HIT:.2f},{HIT+1.1:.2f})',"
          f"eq=brightness='if(lt(t,0.12),0.18,0)':eval=frame[v]")
    sfx = (f"aevalsrc='0.35*sin(2*PI*(300+3000*(t/0.4)^2)*t)*(t/0.4)':d=0.4,aformat=channel_layouts=stereo,adelay={max(0,int((HIT-0.4)*1000))}|{max(0,int((HIT-0.4)*1000))}[rs];"
           f"aevalsrc='0.9*sin(2*PI*52*t)*exp(-3.5*t)':d=1.2,aformat=channel_layouts=stereo,adelay={int(HIT*1000)}|{int(HIT*1000)}[bm];")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", body]
    if mus:
        off, bpm = mus
        cmd += ["-ss", f"{off:.3f}", "-i", mp]
        fc += (f";{sfx}[0:a]volume=0.95,highpass=f=40[g];[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
               f"afade=t=in:st=0:d=0.08,afade=t=out:st={total-0.12:.2f}:d=0.12,volume=0.68[m];"
               f"[g][m][rs][bm]amix=inputs=4:normalize=0:duration=first,loudnorm=I=-13:TP=-1.0:LRA=8[a]")
    else:
        fc += f";{sfx}[0:a][rs][bm]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-13:TP=-1.0:LRA=8[a]"
else:
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", body]
    if mus:
        off, bpm = mus
        cmd += ["-ss", f"{off:.3f}", "-i", mp]
        fc += (f";[0:a]volume=1.0,highpass=f=40[g];[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
               f"afade=t=in:st=0:d=0.05,afade=t=out:st={total-0.15:.2f}:d=0.15,volume=0.42[m];"   # sound from frame 0, loop-friendly
               f"[g][m]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.2:LRA=9[a]")
    else:
        fc += ";[0:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]"
cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "60"] + venc(17) + \
       ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{total:.3f}", "-movflags", "+faststart", out + ".part.mp4"]
run(cmd)
os.replace(out + ".part.mp4", out)
# review sheet for Claude: 12 frames + 2 full-size frames (before and inside the slow motion)
rv = out[:-4] + "_review"; os.makedirs(rv, exist_ok=True)
run(["ffmpeg", "-y", "-v", "error", "-i", out, "-vf", f"fps={12/total:.4f},scale=270:480,tile=6x2", "-frames:v", "1",
     "-q:v", "3", os.path.join(rv, "sheet.jpg")])
for nm, tt in (("f_start", 1.0), ("f_hit", HIT + 1.2), ("f_end", total - 2)):
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", out, "-frames:v", "1", "-q:v", "2", os.path.join(rv, nm + ".jpg")])
shutil.rmtree(tmp, ignore_errors=True)
print("TAYYOR", out, f"{total:.1f}s", flush=True)

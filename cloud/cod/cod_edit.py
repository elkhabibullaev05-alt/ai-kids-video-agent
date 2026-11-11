#!/usr/bin/env python3
"""CoD gameplay editor (2026-11-10, owner's request): one long video per mission + 3 Shorts per mission.
Cuts deaths / failed attempts / pause menus / out-of-bounds, adds original meme effects
(freeze-frame zoom + shake + text + synthesized boom), title card, loudness normalisation.
Usage: python3 cod_edit.py job.json   (job format: see cloud/cod/job.json)"""
import json, os, subprocess, sys, shutil, time, glob

def font():
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p): return p
    subprocess.run("apt-get install -y -q fonts-dejavu-core >/dev/null 2>&1", shell=True)
    for p in glob.glob("/usr/share/fonts/**/*Bold*.ttf", recursive=True): return p
    return glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)[0]

FONT = font()
def _venc():
    # 2026-11-10: libx264 in WSL was ~0.2x realtime (CPU shared with channel makers) -> use the laptop's NVIDIA
    # encoder (WSL exposes it via /usr/lib/wsl/lib) when it works; fall back to libx264.
    common = ["-pix_fmt", "yuv420p", "-r", "60", "-g", "120", "-video_track_timescale", "15360"]
    nv = ["-c:v", "h264_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr", "-cq", "18", "-b:v", "0", "-spatial-aq", "1", "-profile:v", "high"]
    t = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=60:d=1",
                        "-pix_fmt", "yuv420p", "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True, text=True)
    if t.returncode == 0 and not os.environ.get("COD_CPU"):
        return nv + common, "h264_nvenc"
    return ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"] + common, "libx264 (" + t.stderr.strip()[-200:] + ")"

VENC, VENC_NAME = _venc()
AENC = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BOOM = "0.85*sin(2*PI*(45+140*exp(-11*t))*t)*exp(-2.6*t)+0.3*(random(0)*2-1)*exp(-20*t)"
LOG = None

def log(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    if LOG:
        with open(LOG, "a") as f: f.write(s + "\n")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        log("FFMPEG XATO:", " ".join(cmd)[:400], r.stderr[-1500:])
        raise RuntimeError("ffmpeg failed")

def fit(text, maxw, maxfs):  # DejaVu Sans Bold ~0.72 em per char
    return int(min(maxfs, maxw / (0.72 * max(len(text), 1))))

def esc(t):  # drawtext text escaping
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")

def dtext(text, size, y, start=None, end=None, color="white", border=8, x="(w-text_w)/2"):
    s = (f"drawtext=fontfile='{FONT}':text='{esc(text)}':fontsize={size}:fontcolor={color}:"
         f"borderw={border}:bordercolor=black:x={x}:y={y}")
    if start is not None: s += f":enable='between(t,{start:.2f},{end:.2f})'"
    return s

# 2026-11-11 owner: "hamma detallar ko'rinsin, ranglar yorqin" -> lift shadows, vivid colour, light sharpening
GRADE_ON = False
GRADE = "curves=all='0/0 0.06/0.11 0.2/0.31 0.5/0.62 1/1',eq=saturation=1.35:contrast=1.04,unsharp=5:5:0.6:5:5:0.0"
def segment(src, a, b, out, events=(), title=None, fade=True):
    """Encode src[a:b] to out. events: [[abs_time, text], ...] -> pop text + boom inside the segment."""
    d = b - a
    vf = [GRADE] if GRADE_ON else []
    if fade is True: vf += [f"fade=t=in:st=0:d=0.25", f"fade=t=out:st={max(d-0.25,0):.2f}:d=0.25"]
    if title:
        vf += [atext(title[0], 170, "(h/2)-190", "white", 9, start=0.3, end=4.3),
               atext(title[1], 76, "(h/2)+10", "#FFD200", 6, start=0.6, end=4.3)]
    inputs = ["-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src]
    amix = ""
    ev = [(t - a, txt) for t, txt in events if a <= t < b - 1.3]
    for i, (o, txt) in enumerate(ev):
        vf.append(dtext(txt, 130, "h*0.18", o, o + 1.3, "#FFD200", 10))
        inputs += ["-f", "lavfi", "-i", f"aevalsrc='{BOOM}':s=48000:d=1.6,aformat=channel_layouts=stereo,volume=0.7,adelay={int(o*1000)}|{int(o*1000)}"]
    fc = f"[0:v]{','.join(vf) if vf else 'null'}[v]"
    af = (f"afade=t=in:st=0:d=0.2,afade=t=out:st={max(d-0.25,0):.2f}:d=0.25" if fade is True else
          f"afade=t=in:st=0:d=0.04,afade=t=out:st={max(d-0.05,0):.2f}:d=0.05")  # v2 hard cut: no click
    if ev:
        fc += (";[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[a0]" + "".join(f"[{i+1}:a]" for i in range(len(ev)))
               + f"amix=inputs={len(ev)+1}:normalize=0:duration=first,{af}[a]")
    else:
        fc += f";[0:a]{af}[a]"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs +
        ["-filter_complex", fc, "-map", "[v]", "-map", "[a]"] + VENC + AENC + ["-shortest", out])

def meme(src, t, text, out, w=1920, h=1080, dur=1.6, fsize=None):
    """Freeze frame at t: still image (no zoom/shake) + desaturate + big text + boom."""
    png = out + ".png"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", png])
    # 2026-11-11 owner: no shaking/zoom at all -> clean still freeze + text + boom
    vf = ("eq=saturation=0.45:contrast=1.15,"
          + dtext(text, fsize or fit(text, w * 0.9, int(h * 0.15)), "(h-text_h)/2", None, None, "white", 12)
          + f",fade=t=out:st={dur-0.15:.2f}:d=0.15")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-framerate", "60", "-t", f"{dur}", "-i", png,
         "-f", "lavfi", "-t", f"{dur}", "-i", f"aevalsrc='{BOOM}':s=48000:d={dur},aformat=channel_layouts=stereo",
         "-vf", vf, "-map", "0:v", "-map", "1:a"] + VENC + AENC + ["-t", f"{dur}", out])
    os.remove(png)

def concat(parts, final, loud=True):
    out = final + ".part.mp4"; lst = out + ".txt"
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    af = ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11"] if loud else []
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "copy"] + af + AENC + ["-movflags", "+faststart", out])
    os.remove(lst); os.replace(out, final)

def thumb(src, t, big, small, out):
    vf = ("scale=1280:720,eq=saturation=1.35:contrast=1.15," + dtext(big, 130, "h-text_h-150", None, None, "white", 10)
          + "," + dtext(small, 64, "h-text_h-60", None, None, "#FFD200", 6))
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
         "-vf", vf, "-q:v", "2", out])

def long_video(job, m, tmp, outdir):
    src = m.get("src", job["src"])
    keep = m["keep"]
    if job.get("tighten"):
        before = sum(b - a for a, b in keep); keep = tighten(src, keep)
        log(m["id"], f"bo'sh joylar qirqildi: {before/60:.1f} -> {sum(b - a for a, b in keep)/60:.1f} daqiqa")
    memes = {round(float(k)): v for k, v in m.get("memes", {}).items()}
    parts = []
    for i, (a, b) in enumerate(keep):
        p = os.path.join(tmp, f"{m['id']}_s{i:02d}.mp4")
        segment(src, a, b, p, m.get("events", []), title=(m["title"], m["subtitle"]) if i == 0 else None,
                fade=(True if not job.get("tighten") else "a"))
        parts.append(p)
        # meme for a death/fail that happens right after this kept piece
        for mt, txt in memes.items():
            if i + 1 < len(keep) and b - 0.5 <= mt <= keep[i + 1][0] + 0.5:
                q = os.path.join(tmp, f"{m['id']}_m{i:02d}.mp4")
                meme(src, mt, txt, q); parts.append(q)
        log(m["id"], f"bo'lak {i+1}/{len(keep)} tayyor")
    out = os.path.join(outdir, f"{m['file']}.mp4")
    concat(parts, out)
    thumb(src, m["thumb_t"], m["thumb_big"], m["thumb_small"], os.path.join(outdir, f"{m['file']}_thumbnail.jpg"))
    for p in parts: os.remove(p)
    log(m["id"], "UZUN VIDEO TAYYOR:", out)

# 2026-11-11 owner: Shorts edited to copyright-safe YouTube Audio Library music (no attribution needed),
# cuts placed on the music's beat grid.
try:
    import numpy as np
except ImportError:
    subprocess.run("pip install --break-system-packages -q numpy", shell=True); import numpy as np
def beat_grid(path, sr=11025, hop=256):
    raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(sr),"-f","s16le","-"],capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)/32768
    n = len(x)//hop; fr = x[:n*hop].reshape(n,hop)
    e = np.log1p(100*np.sqrt((fr**2).mean(1)))
    on = np.maximum(np.diff(e, prepend=e[0]), 0); on -= on.mean()
    fps = sr/hop
    ac = np.correlate(on, on, "full")[len(on)-1:]
    lags = np.arange(len(ac)); bpm = 60*fps/np.maximum(lags,1)
    ok = (bpm>=75)&(bpm<=165); L = lags[ok][np.argmax(ac[ok])]
    period = L/fps
    ph = max(range(int(L)), key=lambda p: on[p::int(L)].sum())
    energy = np.sqrt((fr**2).mean(1))
    return 60/period, period, ph/fps, energy, fps
def loud_start(path, dur, period, phase, energy, fps):
    w = int(dur*fps); cs = np.cumsum(np.r_[0,energy]); best=max(range(0,len(energy)-w, int(fps)), key=lambda i: cs[i+w]-cs[i]) if len(energy)>w else 0
    t = best/fps; k = round((t-phase)/period); return max(phase + k*period, 0)

def music_for(job, s, dur):
    """-> (path, start_offset, beat_period) or None"""
    if not s.get("music"): return None
    path = os.path.join(job.get("music_dir", ""), s["music"])
    if not os.path.exists(path): log("musiqa topilmadi:", path); return None
    bpm, per, ph, en, fps = beat_grid(path)
    return path, loud_start(path, dur, per, ph, en, fps), per

def activity(src, a, b):
    """2026-11-11 retention: per-second score (frame motion + loudness) for src[a:b] -> list of floats."""
    a = max(0, a); d = b - a
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{d:.2f}", "-i", src, "-vf",
                          "fps=4,scale=96:54,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
    mo = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))] if len(fr) > 1 else np.zeros(1)
    au = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{d:.2f}", "-i", src, "-vn", "-ac", "1",
                         "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(au, np.int16).astype(np.float32) / 32768
    n = int(d)
    m1 = np.array([mo[i*4:(i+1)*4].mean() if len(mo[i*4:(i+1)*4]) else 0 for i in range(n)])
    l1 = np.array([np.sqrt((x[i*8000:(i+1)*8000] ** 2).mean() + 1e-9) for i in range(n)])
    z = lambda v: (v - v.mean()) / (v.std() + 1e-6)
    return list(z(m1) + z(l1))

def best_window(src, a, b, length, pad=15):
    """Best continuous `length` seconds inside [a-pad, b+pad] by activity (start on action = fewer swipes)."""
    lo, hi = max(0, a - pad), b + pad
    sc = activity(src, lo, hi)
    L = int(round(length))
    if len(sc) <= L: return a
    cs = np.cumsum(np.r_[0, sc]); best = max(range(len(sc) - L + 1), key=lambda i: cs[i + L] - cs[i] + 1.5 * sum(sc[i:i+3]))
    return lo + best

def thin_font():
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        if os.path.exists(p): return p
    return FONT

def wrap(text, per_line):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > per_line: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def headline(text, y0, size=58):
    """White bold sentence headline, wrapped, left-aligned like the owner's reference Shorts."""
    out = []
    lines = wrap(text, int(980 / (0.62 * size)))
    if len(lines) > 3:  # 2026-11-11: never cut the sentence -> smaller font, up to 4 lines
        size = 48; lines = wrap(text, int(980 / (0.62 * size)))[:4]
    for i, ln in enumerate(lines):
        out.append(dtext(ln, size, str(y0 + i * int(size * 1.25)), None, None, "white", 0, x="50"))
    return ",".join(out)

def short(job, m, s, k, tmp, outdir):
    """2026-11-11 owner sent 3 reference reels (Instagram): (1) cinematic story edit of cutscenes with film
    grade + big spaced title, (2) black 'card' layout: headline sentence on top, native gameplay window under it,
    the joke is the clip itself (no overlay memes), (3) clean native-resolution crop. Max Full HD, nothing shakes."""
    src = m.get("src", job["src"])
    final = os.path.join(outdir, f"{m['file']}_{job.get('short_tag', 'shortHD')}{k}.mp4"); out = final + ".part.mp4"
    if s.get("type") == "cine":
        a, b = s["a"], s["b"]; n = s.get("shots", 8); L = s.get("shot_len", 3.6)
        mus = music_for(job, s, n * L + 2)
        if mus:  # snap shot length to a whole number of beats (cuts land on the beat)
            L = max(2, round(L / mus[2])) * mus[2]
        step = max((b - a - L) / max(n - 1, 1), L)
        starts = [a + i * step for i in range(n) if a + i * step + L <= b]
        try:  # 2026-11-11 retention: open on the most intense shot, then the story in order
            scs = [sum(activity(src, t, t + L)) for t in starts]
            top = int(np.argmax(scs)); starts = [starts[top]] + starts[:top] + starts[top + 1:]
        except Exception as e:
            log("activity xato:", e)
        title = "  ".join(" ".join(w) for w in s["title"].split())
        grade = "eq=contrast=1.12:saturation=0.78:gamma=0.95,colorbalance=rs=-0.05:bs=0.06:rh=0.04:bh=-0.03"
        # 2026-11-11: shots rendered one by one (hook shot first is out of time order -> split/trim overflowed)
        shots = []
        for i, t in enumerate(starts):
            sp = os.path.join(tmp, f"{m['id']}_c{k}_{i}.mp4")
            vfi = ("fade=t=in:st=0:d=0.12," if i else "") + f"fade=t=out:st={L-0.12:.2f}:d=0.12"
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-t", f"{L:.3f}", "-i", src,
                 "-vf", vfi, "-af", f"afade=t=out:st={L-0.1:.2f}:d=0.1"] + VENC + AENC + [sp])
            shots.append(sp)
        lst = os.path.join(tmp, f"{m['id']}_c{k}.txt")
        open(lst, "w").write("".join(f"file '{x}'\n" for x in shots))
        fc = []
        cat = ""
        tf = thin_font()
        lay = (f"[0:v]scale=1080:608:flags=lanczos,{grade},pad=1080:1920:0:656:black,"
               f"drawtext=fontfile='{tf}':text='{esc(title)}':fontsize={fit(title, 1000, 84)}:fontcolor=white:"
               f"x=(w-text_w)/2:y=470,"
               + dtext(s.get("sub", "CALL OF DUTY: MODERN WARFARE 4"), 34, "1330", None, None, "#BBBBBB", 0)
               + "[v]")
        total = len(starts) * L
        amap = "0:a"; extra = []
        if mus:
            extra = ["-ss", f"{mus[1]:.3f}", "-i", mus[0]]
            lay += (f";[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={total-1.2:.2f}:d=1.2,volume=1.0[m];"
                    f"[0:a]volume=0.30[g];[m][g]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[mix]")
            amap = "[mix]"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst] + extra +
            ["-filter_complex", lay, "-map", "[v]", "-map", amap] + VENC + AENC + ["-movflags", "+faststart", out])
        for x in shots + [lst]: os.remove(x)
    else:
        a, b = s["a"], s["b"]
        want = min(b - a, s.get("len", 26))
        try:
            a = best_window(src, a, b, want); b = a + want
        except Exception as e:
            log("best_window xato:", e)
        mus = music_for(job, s, b - a)
        if mus:
            bar = 4 * mus[2]; b = a + max(1, int((b - a) / bar)) * bar
        # card: black 1080x1920, headline at top, 1080x1080 native-pixel gameplay window (no upscaling)
        vf = ("[0:v]crop=1080:1080:420:0,pad=1080:1920:0:560:black," + headline(s["hook"], 300) + "[v]")
        d = b - a
        if mus:
            vf += (f";[1:a]atrim=0:{d:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={d-1:.2f}:d=1,volume=0.55[m];"
                   f"[0:a]volume=1.0[g];[g][m]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[mix]")
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src,
                 "-ss", f"{mus[1]:.3f}", "-i", mus[0], "-filter_complex", vf, "-map", "[v]", "-map", "[mix]"]
                + VENC + AENC + ["-movflags", "+faststart", out])
        else:
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src,
                 "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11"]
                + VENC + AENC + ["-movflags", "+faststart", out])
    os.replace(out, final)
    log(m["id"], f"SHORTS {k} TAYYOR:", final)

# ---------------------------------------------------------------------------------------------------------------
# 2026-11-11 v2 (owner: "zerikarli, sekin" + didn't like the text and the music; long videos boring too)
ANTON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Anton-Regular.ttf")
def atext(text, size, y, color="white", border=7, x="(w-text_w)/2", start=None, end=None):
    """Anton (condensed heavy display font, the look of top gaming Shorts/thumbnails)."""
    f = ANTON if os.path.exists(ANTON) else FONT
    st = (f"drawtext=fontfile='{f}':text='{esc(text)}':fontsize={size}:fontcolor={color}:borderw={border}:"
          f"bordercolor=black:x={x}:y={y}")
    if start is not None: st += f":enable='between(t,{start:.2f},{end:.2f})'"
    return st

def pick_shots(src, a, b, L, n, pad=20):
    """n non-overlapping L-second shots with the most action inside [a-pad, b+pad]; best first, rest in story order."""
    lo, hi = max(0, a - pad), b + pad
    sc = np.array(activity(src, lo, hi)); W = max(1, int(round(L)))
    if len(sc) <= W: return [lo]
    win = np.convolve(sc, np.ones(W), "valid")
    taken, out = np.zeros(len(win), bool), []
    for i in np.argsort(-win):
        if len(out) >= n: break
        if taken[max(0, i - W):i + W].any(): continue
        out.append(int(i)); taken[i] = True
    best = out[0]; rest = sorted(out[1:])
    return [lo + t for t in [best] + rest]

_PEAKS = {}
def mission_peaks(src, m, L, want=12):
    """2026-11-11 baho: R1 opened on a talking close-up (loud dialogue scored high) -> 74%. The hook shot now comes
    from the most intense moments of the WHOLE mission (motion counted double), a different one for every Short."""
    key = (m["id"], round(L, 2))
    if key in _PEAKS: return _PEAKS[key]
    cands = []
    for a, b in m["keep"]:
        if b - a < L + 2: continue
        lo = a
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{b-a:.2f}", "-i", src, "-vf",
                              "fps=4,scale=96:54,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
        if len(fr) < 8: continue
        mo = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
        au = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{b-a:.2f}", "-i", src, "-vn", "-ac", "1",
                             "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
        x = np.frombuffer(au, np.int16).astype(np.float32) / 32768
        n = min(len(mo) // 4, len(x) // 8000)
        m1 = mo[:n*4].reshape(n, 4).mean(1); l1 = np.sqrt((x[:n*8000].reshape(n, 8000) ** 2).mean(1) + 1e-9)
        # peaky sound (gunfire/explosions) beats steady dialogue: use the per-second max-minus-mean of loudness
        for i in range(max(0, n - int(L))):
            cands.append((2 * m1[i:i+int(L)+1].mean() + 40 * l1[i:i+int(L)+1].max(), lo + i))
    cands.sort(reverse=True); out = []
    for sc, t in cands:
        if all(abs(t - u) > 12 for u in out): out.append(t)
        if len(out) >= want: break
    _PEAKS[key] = out
    return out

def hype_short(job, m, s, k, tmp, outdir):
    """Fast montage Short: 1.5-2 s shots cut on the beat of an energetic track, the most intense moment first,
    blurred gameplay fills the 9:16 frame behind a native 1080x1080 window, big Anton headline on top."""
    src = m.get("src", job["src"])
    final = os.path.join(outdir, f"{m['file']}_{job.get('short_tag', 'shortHD')}{k}.mp4"); out = final + ".part.mp4"
    target = s.get("len", 21.0)
    mus = music_for(job, s, target + 2)
    L = 1.8
    if mus:  # whole beats, ~1.4-2.2 s per shot
        per = mus[2]; nb = max(1, round(L / per)); L = nb * per
        while L < 1.35: L += per
        while L > 2.3 and nb > 1: nb -= 1; L = nb * per
    n = max(8, int(target / L))
    starts = pick_shots(src, s["a"], s["b"], L, n)
    try:
        pk = mission_peaks(src, m, L)
        if pk:
            hook = pk[s.get('_peak', k - 1) % len(pk)]
            starts = [hook] + [t for t in starts[1:] if abs(t - hook) > L][:n - 1]
    except Exception as e:
        log("hook tanlash xato:", e)
    shots = []
    for i, t in enumerate(starts):
        sp = os.path.join(tmp, f"{m['id']}_h{k}_{i}.mp4")
        vf = "fade=t=in:st=0:d=0.10:color=white" if i else "null"   # tiny white flash on every cut
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-t", f"{L:.3f}", "-i", src,
             "-vf", vf, "-af", f"afade=t=in:st=0:d=0.03,afade=t=out:st={L-0.05:.3f}:d=0.05"] + VENC + AENC + [sp])
        shots.append(sp)
    lst = os.path.join(tmp, f"{m['id']}_h{k}.txt"); open(lst, "w").write("".join(f"file '{x}'\n" for x in shots))
    total = len(shots) * L
    head = (s.get("hook") or s.get("title") or "").upper()
    size = 92; lines = wrap(head, int(1000 / (0.42 * size)))
    if len(lines) > 3: size = 74; lines = wrap(head, int(1000 / (0.42 * size)))[:4]
    y0 = 520 - len(lines) * int(size * 1.12)
    txt = ",".join(atext(ln, size, str(y0 + i * int(size * 1.12)), "#FFD200" if i == len(lines) - 1 else "white")
                   for i, ln in enumerate(lines))
    fc = ("[0:v]split=2[a][b];"
          "[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.22:saturation=1.2[bg];"
          "[b]crop=1080:1080:420:0," + (GRADE if GRADE_ON else "eq=contrast=1.08:saturation=1.18") + "[fg];"
          "[bg][fg]overlay=0:600," + txt + ","
          + atext(f"MW4  PART {m.get('part', '')}".strip(), 54, "1730", "white", 5) +
          f",fade=t=out:st={total-0.3:.2f}:d=0.3[v]")
    extra, amap = [], "0:a"
    if mus:
        extra = ["-ss", f"{mus[1]:.3f}", "-i", mus[0]]
        fc += (f";[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={total-1:.2f}:d=1,volume=0.9[m];"
               f"[0:a]volume=0.55[g];[m][g]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-13:TP=-1.2:LRA=9[mix]")
        amap = "[mix]"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst] + extra +
        ["-filter_complex", fc, "-map", "[v]", "-map", amap] + VENC + AENC + ["-t", f"{total:.3f}", "-movflags", "+faststart", out])
    for x in shots + [lst]: os.remove(x)
    os.replace(out, final)
    log(m["id"], f"SHORTS {k} TAYYOR (v2):", final, f"{len(shots)} kadr x {L:.2f}s")

def tighten(src, keep, gap=8, edge=1.5):
    """Long videos v2: drop stretches with no action and no sound (walking/waiting/quiet loading) longer than `gap` s,
    keeping `edge` s on both sides so cuts stay smooth. Dialogue/cutscenes are loud -> kept."""
    out = []
    for a, b in keep:
        if b - a < gap * 2: out.append([a, b]); continue
        sc = np.array(activity(src, a, b))
        dead = sc < -0.9
        i, cur = 0, a
        while i < len(dead):
            if dead[i]:
                j = i
                while j < len(dead) and dead[j]: j += 1
                if j - i >= gap:
                    s0, s1 = a + i + edge, a + j - edge
                    if s0 - cur > 1: out.append([cur, s0])
                    cur = s1
                i = j
            else:
                i += 1
        if b - cur > 1: out.append([cur, b])
    return out

def main():
    global LOG
    job = json.load(open(sys.argv[1]))
    global GRADE_ON; GRADE_ON = bool(job.get("grade"))
    outdir = job["out"]
    try:  # 2026-11-11: session-2 outputs go to E: (C: has ~19 GB, the 4 long videos need more)
        os.makedirs(outdir, exist_ok=True)
        if shutil.disk_usage(outdir).free < 25e9: raise OSError("E: da joy kam")
    except OSError:
        outdir = job.get("out_fallback", outdir); os.makedirs(outdir, exist_ok=True)
    tmp = job.get("tmp", os.path.join(outdir, "_tmp")); os.makedirs(tmp, exist_ok=True)
    LOG = os.path.join(outdir, "holat.txt")
    log("BOSHLANDI. encoder:", VENC_NAME, "font:", FONT, "ffmpeg:", shutil.which("ffmpeg"))
    only = os.environ.get("COD_ONLY"); err = 0
    for m in job["missions"]:
        if only and m["id"] != only: continue
        try:
            if not os.path.exists(os.path.join(outdir, f"{m['file']}.mp4")):
                long_video(job, m, tmp, outdir)
            for k, s in enumerate([] if job.get("shorts_paused") else m.get("shorts", []), 1):
                if not os.path.exists(os.path.join(outdir, f"{m['file']}_{job.get('short_tag', 'shortHD')}{k}.mp4")):
                    (hype_short if job.get("style") == "hype" else short)(job, m, s, k, tmp, outdir)
            # 2026-11-11 owner: second, Shorts-only channel (MW4 Shorts Daily) gets its OWN Shorts from other moments
            jb = dict(job, short_tag="B")
            for k, s in enumerate([] if job.get("shorts_paused") else m.get("shorts_b", []), 1):
                if not os.path.exists(os.path.join(outdir, f"{m['file']}_B{k}.mp4")):
                    hype_short(jb, m, dict(s, _peak=k + 5), k, tmp, outdir)
        except Exception as e:
            log(m["id"], "XATO:", repr(e)); err += 1
    log("HAMMASI TUGADI" if not err else f"TUGADI, {err} ta xato bilan")
    sys.exit(1 if err else 0)

if __name__ == "__main__":
    main()

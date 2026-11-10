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
VENC = ["-c:v", "libx264", "-preset", os.environ.get("COD_PRESET", "veryfast"), "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", "60", "-g", "120", "-video_track_timescale", "15360"]
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

def esc(t):  # drawtext text escaping
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")

def dtext(text, size, y, start=None, end=None, color="white", border=8, x="(w-text_w)/2"):
    s = (f"drawtext=fontfile='{FONT}':text='{esc(text)}':fontsize={size}:fontcolor={color}:"
         f"borderw={border}:bordercolor=black:x={x}:y={y}")
    if start is not None: s += f":enable='between(t,{start:.2f},{end:.2f})'"
    return s

def segment(src, a, b, out, events=(), title=None, fade=True):
    """Encode src[a:b] to out. events: [[abs_time, text], ...] -> pop text + boom inside the segment."""
    d = b - a
    vf = []
    if fade: vf += [f"fade=t=in:st=0:d=0.25", f"fade=t=out:st={max(d-0.25,0):.2f}:d=0.25"]
    if title:
        vf += [dtext(title[0], 120, "(h/2)-150", 0.3, 4.3, "white", 10),
               dtext(title[1], 64, "(h/2)", 0.6, 4.3, "#FFD200", 6)]
    inputs = ["-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src]
    amix = ""
    ev = [(t - a, txt) for t, txt in events if a <= t < b - 1.3]
    for i, (o, txt) in enumerate(ev):
        vf.append(dtext(txt, 130, "h*0.18", o, o + 1.3, "#FFD200", 10))
        inputs += ["-f", "lavfi", "-i", f"aevalsrc='{BOOM}':s=48000:d=1.6,aformat=channel_layouts=stereo,volume=0.7,adelay={int(o*1000)}|{int(o*1000)}"]
    fc = f"[0:v]{','.join(vf) if vf else 'null'}[v]"
    af = f"afade=t=in:st=0:d=0.2,afade=t=out:st={max(d-0.25,0):.2f}:d=0.25" if fade else "anull"
    if ev:
        fc += (";[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[a0]" + "".join(f"[{i+1}:a]" for i in range(len(ev)))
               + f"amix=inputs={len(ev)+1}:normalize=0:duration=first,{af}[a]")
    else:
        fc += f";[0:a]{af}[a]"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs +
        ["-filter_complex", fc, "-map", "[v]", "-map", "[a]"] + VENC + AENC + ["-shortest", out])

def meme(src, t, text, out, w=1920, h=1080, dur=1.6):
    """Freeze frame at t: punch zoom + shake + desaturate + big text + boom."""
    png = out + ".png"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", png])
    n = int(dur * 60)
    vf = (f"scale={w*2}:{h*2},zoompan=z='min(1+0.9*on/18,1.45)':d={n}:"
          f"x='iw/2-(iw/zoom/2)+18*sin(on*1.7)*exp(-on/25)':y='ih/2-(ih/zoom/2)+14*cos(on*2.1)*exp(-on/25)':s={w}x{h}:fps=60,"
          f"eq=saturation=0.35:contrast=1.25,vignette=PI/4,"
          + dtext(text, int(h * 0.15), "(h-text_h)/2", None, None, "white", 12)
          + f",fade=t=out:st={dur-0.15:.2f}:d=0.15")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", png,
         "-f", "lavfi", "-t", f"{dur}", "-i", f"aevalsrc='{BOOM}':s=48000:d={dur},aformat=channel_layouts=stereo",
         "-vf", vf, "-map", "0:v", "-map", "1:a"] + VENC + AENC + ["-t", f"{dur}", out])
    os.remove(png)

def concat(parts, out, loud=True):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    af = ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11"] if loud else []
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "copy"] + af + AENC + ["-movflags", "+faststart", out])
    os.remove(lst)

def thumb(src, t, big, small, out):
    vf = ("scale=1280:720,eq=saturation=1.35:contrast=1.15," + dtext(big, 130, "h-text_h-150", None, None, "white", 10)
          + "," + dtext(small, 64, "h-text_h-60", None, None, "#FFD200", 6))
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
         "-vf", vf, "-q:v", "2", out])

def long_video(job, m, tmp, outdir):
    src = m.get("src", job["src"])
    keep = m["keep"]; memes = {round(float(k)): v for k, v in m.get("memes", {}).items()}
    parts = []
    for i, (a, b) in enumerate(keep):
        p = os.path.join(tmp, f"{m['id']}_s{i:02d}.mp4")
        segment(src, a, b, p, m.get("events", []), title=(m["title"], m["subtitle"]) if i == 0 else None)
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

def short(job, m, s, k, tmp, outdir):
    src = m.get("src", job["src"])
    a, b = s["a"], s["b"]; d = b - a
    vf = ("[0:v]split[x][y];"
          "[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[bg];"
          "[y]crop=864:1080:528:0,scale=1080:1350[fg];"
          "[bg][fg]overlay=0:285," + dtext(s["hook"], 76, "120", None, None, "white", 7)
          + "," + dtext(s.get("bottom", m["title"]), 60, "1700", None, None, "#FFD200", 6)
          + f",fade=t=in:st=0:d=0.2[v]")
    p1 = os.path.join(tmp, f"{m['id']}_short{k}_a.mp4")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src,
         "-filter_complex", vf, "-map", "[v]", "-map", "0:a"] + VENC + AENC + [p1])
    parts = [p1]
    if s.get("meme"):
        p2 = os.path.join(tmp, f"{m['id']}_short{k}_m.mp4")
        # vertical meme from the last moment of the clip
        meme_v = p2 + ".h.mp4"
        meme(src, s.get("meme_t", b - 0.3), s["meme"], meme_v, dur=1.3)
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", meme_v, "-filter_complex",
             "[0:v]split[x][y];[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2[bg];"
             "[y]crop=864:1080:528:0,scale=1080:1350[fg];[bg][fg]overlay=0:285[v]",
             "-map", "[v]", "-map", "0:a"] + VENC + AENC + [p2])
        os.remove(meme_v); parts.append(p2)
    out = os.path.join(outdir, f"{m['file']}_short{k}.mp4")
    concat(parts, out)
    for p in parts: os.remove(p)
    log(m["id"], f"SHORTS {k} TAYYOR:", out)

def main():
    global LOG
    job = json.load(open(sys.argv[1]))
    outdir = job["out"]; os.makedirs(outdir, exist_ok=True)
    tmp = job.get("tmp", os.path.join(outdir, "_tmp")); os.makedirs(tmp, exist_ok=True)
    LOG = os.path.join(outdir, "holat.txt")
    log("BOSHLANDI. font:", FONT, "ffmpeg:", shutil.which("ffmpeg"))
    only = os.environ.get("COD_ONLY"); err = 0
    for m in job["missions"]:
        if only and m["id"] != only: continue
        try:
            if not os.path.exists(os.path.join(outdir, f"{m['file']}.mp4")):
                long_video(job, m, tmp, outdir)
            for k, s in enumerate(m.get("shorts", []), 1):
                if not os.path.exists(os.path.join(outdir, f"{m['file']}_short{k}.mp4")):
                    short(job, m, s, k, tmp, outdir)
        except Exception as e:
            log(m["id"], "XATO:", repr(e)); err += 1
    log("HAMMASI TUGADI" if not err else f"TUGADI, {err} ta xato bilan")
    sys.exit(1 if err else 0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Polish a video for YouTube: Full HD (or 4K), sharper, cleaner colour, loud and even sound,
dead air and repeated footage cut out, optional burned captions. Prints a before/after report.

Usage:
  python3 polish.py IN.mp4 OUT.mp4 [--res 1080|1440|2160] [--look natural|vivid|warm|cinematic|none]
                    [--trim-silence] [--cut A-B ...] [--captions subs.srt] [--fps 30|60] [--denoise]
                    [--fast]   (preset veryfast, for previews)
Needs only ffmpeg/ffprobe (numpy optional for the sharpness report).
"""
import argparse, json, re, subprocess, sys

LOOKS = {
    "none": "",
    "natural": "eq=contrast=1.04:saturation=1.08:gamma=1.0",
    "vivid": "eq=contrast=1.08:saturation=1.22:brightness=0.01,vibrance=intensity=0.15",
    "warm": "eq=contrast=1.05:saturation=1.10,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03",
    "cinematic": "eq=contrast=1.10:saturation=0.95:gamma=0.97,colorbalance=rs=-0.03:bs=0.05:rh=0.05:bh=-0.04,vignette=PI/5",
}

def sh(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])
    return r

def probe(p):
    d = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", p]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v.get("avg_frame_rate") or "30/1").split("/")
    return dict(w=int(v["width"]), h=int(v["height"]), fps=round(float(num) / max(1, float(den)), 2),
                dur=float(d["format"]["duration"]), vbit=int(d["format"].get("bit_rate", 0)) // 1000,
                codec=v["codec_name"], audio=a is not None)

def loud(p):
    r = sh(["ffmpeg", "-hide_banner", "-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-"], check=False)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else None

def sharpness(p, t):
    try:
        import numpy as np
    except ImportError:
        return None
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf",
                        "scale=540:-2,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    pr = probe(p); w = 540; h = int(len(r.stdout) / w)
    if h < 3: return None
    a = np.frombuffer(r.stdout[: w * h], np.uint8).reshape(h, w).astype(float)
    lap = a[1:-1, 1:-1] * 4 - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:]
    return round(float(lap.var()), 1)

def silences(p, dur, db=-40, mind=0.7):
    r = sh(["ffmpeg", "-i", p, "-af", f"silencedetect=noise={db}dB:d={mind}", "-f", "null", "-"], check=False)
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    en += [dur] * (len(st) - len(en))
    # keep 0.25 s of breath on each side
    return [(a + .25, b - .25) for a, b in zip(st, en) if b - a > mind and a > 0.3]

def keep_ranges(dur, cuts):
    cuts = sorted((max(0, a), min(dur, b)) for a, b in cuts if b > a)
    keep, t = [], 0.0
    for a, b in cuts:
        if a > t: keep.append((t, a))
        t = max(t, b)
    if t < dur: keep.append((t, dur))
    return [(a, b) for a, b in keep if b - a > 0.05]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--res", type=int, default=1080, choices=[1080, 1440, 2160])
    ap.add_argument("--look", default="natural", choices=list(LOOKS))
    ap.add_argument("--trim-silence", action="store_true")
    ap.add_argument("--cut", nargs="*", default=[], help="ranges to remove, seconds: 5-15 20.5-22")
    ap.add_argument("--captions"); ap.add_argument("--fps", type=int)
    ap.add_argument("--denoise", action="store_true"); ap.add_argument("--fast", action="store_true")
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()

    src = probe(a.inp)
    vertical = src["h"] > src["w"]
    long_side = {1080: 1920, 1440: 2560, 2160: 3840}[a.res]
    W, H = (a.res, long_side) if vertical else (long_side, a.res)
    fps = a.fps or (30 if src["fps"] < 29 else min(60, round(src["fps"])))

    # 1) what to remove
    cuts = []
    for c in a.cut:
        x, y = c.split("-"); cuts.append((float(x), float(y)))
    if a.trim_silence and src["audio"]:
        cuts += silences(a.inp, src["dur"])
    keep = keep_ranges(src["dur"], cuts)

    # 2) video chain: fit to frame (pad with blurred copy, never stretch), upscale lanczos, clean, grade, sharpen
    vf = []
    if a.denoise: vf.append("hqdn3d=1.5:1.5:6:6")
    fit = (f"split[o][b];[b]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40[bg];"
           f"[o]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    vf.append(fit)
    if LOOKS[a.look]: vf.append(LOOKS[a.look])
    vf.append("unsharp=5:5:0.6:5:5:0.0")
    if a.captions:
        vf.append(f"subtitles={a.captions}:force_style='Fontname=DejaVu Sans,Fontsize=16,Bold=1,PrimaryColour=&H00FFFFFF,"
                  f"OutlineColour=&H00000000,Outline=3,Shadow=0,Alignment=2,MarginV=180'")
    vf.append(f"fps={fps},format=yuv420p,setsar=1")

    # trimming via select filters (keeps A/V in sync)
    expr = "+".join(f"between(t,{x:.3f},{y:.3f})" for x, y in keep)
    trimmed = len(keep) != 1 or keep[0][0] > 0.01 or keep[0][1] < src["dur"] - 0.01
    vchain = (f"select='{expr}',setpts=N/FRAME_RATE/TB," if trimmed else "") + ",".join(vf)
    fc = f"[0:v]{vchain}[v]"
    maps = ["-map", "[v]"]
    if src["audio"]:
        ach = (f"aselect='{expr}',asetpts=N/SR/TB," if trimmed else "")
        ach += f"highpass=f=60,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,loudnorm=I={a.lufs}:TP=-1.0:LRA=9,aresample=48000"
        fc += f";[0:a]{ach}[a]"; maps += ["-map", "[a]"]
    enc = ["-c:v", "libx264", "-preset", "veryfast" if a.fast else "slow", "-crf", "17", "-profile:v", "high",
           "-level", "5.1" if a.res > 1080 or fps > 30 else "4.2", "-g", str(fps // 2), "-bf", "2",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart"]
    sh(["ffmpeg", "-y", "-hide_banner", "-i", a.inp, "-filter_complex", fc] + maps + enc + [a.out])

    # loudnorm in one pass often lands 2-4 dB low: fix with a measured gain + limiter, video copied
    if src["audio"]:
        m = loud(a.out)
        if m and abs(float(m["input_i"]) - a.lufs) > 0.8:
            import os, shutil
            g = a.lufs - float(m["input_i"]); tmp = a.out + ".tmp.mp4"
            sh(["ffmpeg", "-y", "-hide_banner", "-i", a.out, "-c:v", "copy", "-af",
                f"volume={g:.2f}dB,alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                "-movflags", "+faststart", tmp])
            shutil.move(tmp, a.out)
    dst = probe(a.out)
    t = min(2.0, src["dur"] / 2)
    rep = {
        "before": {**src, "loudness_LUFS": (loud(a.inp) or {}).get("input_i"), "sharpness": sharpness(a.inp, t)},
        "after": {**dst, "loudness_LUFS": (loud(a.out) or {}).get("input_i"), "sharpness": sharpness(a.out, t)},
        "removed_s": round(src["dur"] - dst["dur"], 2), "removed_ranges": [(round(x, 2), round(y, 2)) for x, y in cuts],
        "look": a.look,
    }
    print(json.dumps(rep, indent=1))

if __name__ == "__main__":
    main()

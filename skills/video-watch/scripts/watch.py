#!/usr/bin/env python3
"""Make a video "watchable" for Claude: info, contact sheets, key frames, transcript.
Usage: python3 watch.py <video path | GitHub blob/raw URL | owner/repo:branch:path> [--out DIR] [--every SEC] [--model base] [--lang auto]
"""
import argparse, json, os, re, subprocess, sys, urllib.request

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def fetch(src, out):
    if os.path.exists(src):
        return src
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/(?:blob|raw)/([^/]+)/(.+)", src)
    if m:
        src = "https://raw.githubusercontent.com/%s/%s/%s/%s" % m.groups()
    m = re.match(r"^([\w.-]+)/([\w.-]+):([^:]+):(.+)$", src)
    if m:
        src = "https://raw.githubusercontent.com/%s/%s/%s/%s" % m.groups()
    dst = os.path.join(out, os.path.basename(src.split("?")[0]) or "video.mp4")
    print("downloading", src)
    r = sh(["curl", "-sSfL", "-o", dst, src])
    if r.returncode != 0:
        sys.exit("download failed: " + r.stderr)
    head = open(dst, "rb").read(200)
    if b"git-lfs" in head:
        sys.exit("file is a Git LFS pointer; use https://media.githubusercontent.com/media/<owner>/<repo>/<branch>/<path>")
    return dst

def info(path):
    r = sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    d = json.loads(r.stdout or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    return {"duration": float(d.get("format", {}).get("duration", 0)),
            "width": v.get("width"), "height": v.get("height"),
            "fps": v.get("avg_frame_rate"), "has_audio": a is not None,
            "size_mb": round(int(d.get("format", {}).get("size", 0)) / 1e6, 1)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("src"); p.add_argument("--out", default="watch_out")
    p.add_argument("--every", type=float, default=0, help="seconds between frames (0 = auto, ~36 frames)")
    p.add_argument("--model", default="base"); p.add_argument("--lang", default=None)
    p.add_argument("--no-audio", action="store_true")
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)
    path = fetch(a.src, a.out)
    inf = info(path); dur = inf["duration"] or 1
    every = a.every or max(0.5, dur / 36)
    inf["frame_every_s"] = round(every, 2)
    print(json.dumps(inf, indent=1))
    fdir = os.path.join(a.out, "frames"); os.makedirs(fdir, exist_ok=True)
    # timestamped frames, 480px wide
    sh(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf",
        "fps=1/%s,scale=480:-2,drawtext=text='%%{pts\\:hms}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6" % every,
        os.path.join(fdir, "f_%03d.jpg")])
    frames = sorted(os.listdir(fdir))
    # contact sheets 3x4 = 12 frames each
    sheets = []
    for i in range(0, len(frames), 12):
        sheet = os.path.join(a.out, "sheet_%02d.jpg" % (i // 12 + 1))
        lst = os.path.join(a.out, "list.txt")
        with open(lst, "w") as f:
            for fr in frames[i:i+12]:
                f.write("file '%s'\n" % os.path.abspath(os.path.join(fdir, fr)))
        sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
            "-vf", "scale=480:-2,tile=3x4:padding=4:color=white", "-frames:v", "1", sheet])
        sheets.append(sheet)
    # first frame full size (hook check) and scene-change times
    sh(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", path, "-frames:v", "1", os.path.join(a.out, "first_frame.jpg")])
    r = sh(["ffmpeg", "-i", path, "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"])
    cuts = [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    gaps = [round(b - a_, 2) for a_, b in zip([0] + cuts, cuts + [dur])]
    report = {"info": inf, "sheets": sheets, "scene_cuts": cuts[:200],
              "longest_no_cut_s": max(gaps) if gaps else dur}
    if inf["has_audio"] and not a.no_audio:
        wav = os.path.join(a.out, "audio.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav])
        r = sh(["ffmpeg", "-i", wav, "-af", "volumedetect", "-f", "null", "-"])
        report["mean_volume"] = (re.findall(r"mean_volume: (\S+ dB)", r.stderr) or [None])[0]
        report["max_volume"] = (re.findall(r"max_volume: (\S+ dB)", r.stderr) or [None])[0]
        try:
            from faster_whisper import WhisperModel
            m = WhisperModel(a.model, device="cpu", compute_type="int8")
            segs, ti = m.transcribe(wav, language=a.lang, vad_filter=True)
            lines = ["[%6.1f-%6.1f] %s" % (s.start, s.end, s.text.strip()) for s in segs]
            open(os.path.join(a.out, "transcript.txt"), "w").write("\n".join(lines))
            report["language"] = ti.language; report["transcript"] = os.path.join(a.out, "transcript.txt")
            report["words"] = sum(len(l.split()) - 2 for l in lines)
        except Exception as e:
            report["transcript_error"] = str(e)
    # repeated footage: tiny grayscale hash per frame, find earlier near-identical frames
    try:
        from PIL import Image
        hs = []
        for fr in frames:
            im = Image.open(os.path.join(fdir, fr)).convert("L")
            w, h = im.size; im = im.crop((0, int(h * 0.3), w, int(h * 0.9))).resize((16, 16))  # skip caption/timestamp area
            px = list(im.getdata()); avg = sum(px) / len(px)
            hs.append([1 if v > avg else 0 for v in px])
        rep = []
        for i in range(len(hs)):
            for j in range(max(0, i - 400), i - 2):
                if sum(x != y for x, y in zip(hs[i], hs[j])) <= 14:
                    rep.append((round(i * every, 1), round(j * every, 1))); break
        report["repeated_frames"] = len(rep); report["repeated_pct"] = round(100 * len(rep) / max(1, len(hs)))
        report["repeat_examples"] = rep[:10]
        # motion: mean hash change between neighbours (0 = frozen, high = busy)
        mv = [sum(x != y for x, y in zip(hs[i], hs[i - 1])) for i in range(1, len(hs))]
        report["still_stretches"] = [round(i * every, 1) for i, v in enumerate(mv, 1) if v <= 2][:20]
    except Exception as e:
        report["repeat_error"] = str(e)
    if inf["has_audio"]:
        r = sh(["ffmpeg", "-i", path, "-af", "silencedetect=noise=-35dB:d=0.6", "-f", "null", "-"])
        st = re.findall(r"silence_start: ([\d.]+)", r.stderr); en = re.findall(r"silence_end: ([\d.]+)", r.stderr)
        report["silences"] = [[round(float(x), 1), round(float(y), 1) if k < len(en) else round(dur, 1)] for k, (x, y) in enumerate(zip(st, en + [dur] * len(st)))][:30]
    json.dump(report, open(os.path.join(a.out, "report.json"), "w"), indent=1)
    print(json.dumps(report, indent=1))
    print("\nNEXT: Read first_frame.jpg and every sheet_*.jpg with the Read tool, then transcript.txt.")

if __name__ == "__main__":
    main()

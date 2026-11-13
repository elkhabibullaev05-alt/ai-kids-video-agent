#!/usr/bin/env python3
"""2026-11-13 owner: Money Story Daily -> Physics Rank Daily, ranked funny physics Shorts (funny.py engine, CC BY clips,
credited). 2026-11-13 owner "ha" to the growth plan (Fabio Morena model: faceless long compilations earn 40-100x more
per view than Shorts): every Short is also kept in HOME/comp_pool; twice a week (Tue, Fri) 12 pooled Shorts become one
8+ minute 16:9 "Top 12" compilation (blurred background, #12 -> #1 badge), credits carried over. Each Short is used once."""
import os, sys, json, glob, shutil, subprocess, argparse, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["FR_THEMES"] = "physics"
os.environ["FR_BRAND"] = "Physics Rank Daily"
os.environ["FR_TAGS"] = "#shorts #physics #science #fails #ranking"
N, MIN_S, DAYS = 12, 480, (1, 4)          # Tue, Fri


def dur(f):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    try: return float(p.stdout.strip())
    except ValueError: return 0.0


def make_long(a, pool):
    today = dt.date.today()
    hist_f = os.path.join(a.home, "long_hist.json")
    hist = json.load(open(hist_f)) if os.path.exists(hist_f) else []
    if today.weekday() not in DAYS or today.isoformat() in hist:
        return None
    items = sorted(glob.glob(os.path.join(pool, "*.json")))
    if len(items) < N:
        print(f"pool {len(items)}/{N}: long later", file=sys.stderr); return None
    pick = [json.load(open(j)) | {"_j": j} for j in items[:N]]
    pick = [p for p in pick if os.path.exists(os.path.join(pool, p["file"]))]
    if len(pick) < N: return None
    work = os.path.join(a.home, "comp_work"); shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    parts, total = [], 0.0
    for i, p in enumerate(pick):
        rank = N - i; src = os.path.join(pool, p["file"]); o = os.path.join(work, f"{i:02d}.mp4")
        vf = ("[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,"
              "eq=brightness=-0.15[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,"
              f"drawtext=fontfile={font}:text='#{rank}':fontsize=150:fontcolor=yellow:borderw=8:bordercolor=black:x=70:y=60,"
              "fps=30,format=yuv420p[v]")
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", vf, "-map", "[v]", "-map", "0:a?",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", o])
        if r.returncode or not os.path.exists(o): return None
        parts.append(o); total += dur(o)
    if total < MIN_S:
        print(f"compilation only {total:.0f}s (<{MIN_S}): wait for more Shorts", file=sys.stderr); return None
    lst = os.path.join(work, "l.txt"); open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    name = f"physics-top{N}-{today:%Y%m%d}"; out = os.path.join(a.out, name + ".mp4")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-14:TP=-1.5",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])
    if r.returncode: return None
    credits = []
    for p in pick:
        credits += [l for l in p.get("description", "").splitlines() if "youtu.be/" in l]
    title = f"Top {N} Funniest Physics Fails Ranked ({total / 60:.0f} Minutes)"
    desc = "\n".join([f"{N} of the funniest physics fails, ranked from #{N} to #1. Which one got you? Comment your #1!", "",
                      "Clips (CC BY):"] + credits + ["", "All clips are used under the Creative Commons Attribution license "
                      "(CC BY 3.0); thank you to every creator above. Edited and ranked by Physics Rank Daily.", "",
                      "#physics #fails #funny #compilation #science"])
    item = {"file": name + ".mp4", "kind": "long", "title": title, "description": desc,
            "tags": ["physics fails", "funny physics", "fails compilation", "try not to laugh", "ranking", "top 12",
                     "funny fails", "science fails", "physics rank daily"]}
    json.dump(item, open(os.path.join(a.out, name + ".json"), "w"), ensure_ascii=False, indent=1)
    for p in pick:                               # each Short goes into one compilation only
        os.remove(p["_j"]); os.remove(os.path.join(pool, p["file"]))
    hist.append(today.isoformat()); json.dump(hist[-50:], open(hist_f, "w"))
    shutil.rmtree(work, ignore_errors=True)
    return item


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--home")
    ap.add_argument("--need-long", type=int, default=0); ap.add_argument("--need-short", type=int, default=1)
    a, _ = ap.parse_known_args()
    pool = os.path.join(a.home, "comp_pool"); os.makedirs(pool, exist_ok=True)
    made, rc = 0, 3
    if a.need_short:
        before = set(os.listdir(a.out)) if os.path.isdir(a.out) else set()
        rc = subprocess.run([sys.executable, os.path.join(HERE, "funny.py")] + sys.argv[1:]).returncode
        for f in sorted(set(os.listdir(a.out)) - before):
            if f.endswith(".json"):
                it = json.load(open(os.path.join(a.out, f)))
                if it.get("kind") == "short" and os.path.exists(os.path.join(a.out, it["file"])):
                    shutil.copy(os.path.join(a.out, it["file"]), pool); shutil.copy(os.path.join(a.out, f), pool)
                    made += 1
    try:
        if make_long(a, pool): made += 1
    except Exception as e:
        print("long compilation failed:", str(e)[:300], file=sys.stderr)
    return 0 if made else (rc if rc not in (0,) else 3)


if __name__ == "__main__":
    sys.exit(main())

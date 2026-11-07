#!/usr/bin/env python3
"""Calm Rain for Sleep — maker (2026-11-06, rebuilt after the old laptop's sleeptube agent was lost).

Owner's rule: REAL rain recordings only — no AI video. Source = Wikimedia Commons files whose licence allows reuse
(CC0 / public domain / CC BY / CC BY-SA), credited in the description.
  long : 2–3 h video — a real rain video clip made into a seamless loop + a real rain recording (looped, crossfaded)
  short: 30–45 s of the same scene with a calm text hook, ends where it starts (loops)
See cloud/makers/README.md for the contract.  --offline-test makes a synthetic scene to test the pipeline.
"""
import argparse, glob, json, os, random, re, subprocess, sys, time, urllib.parse, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True); ap.add_argument("--home", required=True); ap.add_argument("--repo", default=".")
ap.add_argument("--titles", default=""); ap.add_argument("--need-long", type=int, default=1); ap.add_argument("--need-short", type=int, default=1)
ap.add_argument("--hours", type=float, default=0); ap.add_argument("--offline-test", action="store_true")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
CACHE = os.path.join(a.home, "rain_cache"); os.makedirs(CACHE, exist_ok=True)
USED_F = os.path.join(a.home, "used_rain.json")
used = json.load(open(USED_F)) if os.path.exists(USED_F) else {"video": [], "audio": [], "titles": []}
titles = set(json.load(open(a.titles))) if a.titles and os.path.exists(a.titles) else set()
UA = {"User-Agent": "CalmRainForSleep/1.0 (owner's own YouTube channel tool; contact via channel)"}
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[1-4]\.0|cc by(-sa)?|cc-by(-sa)?-[1-4]\.0)", re.I)
FONT = next((f for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
             if os.path.exists(f)), "")


def sh(*cmd, timeout=7200):
    p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-800:]}")
    return p.stdout


def api(**q):
    q.update(format="json")
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
        except Exception:
            time.sleep(5 * (i + 1))
    raise RuntimeError("Commons API unreachable")


def files(kind):
    """Candidate Commons files: categories first, then search."""
    cats = {"video": ["Category:Videos of rain", "Category:Videos of rain on windows", "Category:Videos of rainfall"],
            "audio": ["Category:Sounds of rain", "Category:Audio files of rain"]}[kind]
    out = []
    for c in cats:
        try:
            r = api(action="query", list="categorymembers", cmtitle=c, cmtype="file", cmlimit=200)
            out += [m["title"] for m in r["query"]["categorymembers"]]
        except Exception:
            pass
    ft = "video" if kind == "video" else "audio"
    for q in (["rain", "rain window", "rain forest", "rain night", "heavy rain"] if kind == "video" else ["rain", "rain sound", "rainfall"]):
        try:
            r = api(action="query", list="search", srnamespace=6, srsearch=f"{q} filetype:{ft}", srlimit=50)
            out += [m["title"] for m in r["query"]["search"]]
        except Exception:
            pass
    seen, res = set(), []
    for t in out:
        bad = ("map", "radar", "us rain", "precip", "forecast", "satellite", "animation", "chart", "graph", "simulation", "storm surge")
        if t not in seen and "rain" in t.lower() and not any(b in t.lower() for b in bad):
            seen.add(t); res.append(t)
    return res


def info(titles_):
    r = api(action="query", prop="imageinfo", titles="|".join(titles_), iiprop="url|extmetadata|size|mediatype|mime")
    for p in r["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = re.sub("<[^>]+>", "", md.get("LicenseShortName", {}).get("value", ""))
        art = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()[:80] or "unknown author"
        yield dict(title=p["title"], url=ii.get("url"), lic=lic, artist=art, dur=ii.get("duration") or 0,
                   w=ii.get("width", 0), h=ii.get("height", 0), mime=ii.get("mime", ""))


def pick(kind):
    cands = [t for t in files(kind) if t not in used[kind]]
    random.shuffle(cands)
    for i in range(0, len(cands), 40):
        for f in info(cands[i:i + 40]):
            if not f["url"] or not FREE.match(f["lic"].strip()):
                continue
            if kind == "video" and (f["w"] < 640 or (f["dur"] and f["dur"] < 8)):
                continue
            if kind == "audio" and f["dur"] and f["dur"] < 20:
                continue
            dst = os.path.join(CACHE, re.sub(r"[^\w.-]", "_", f["title"].split(":", 1)[1]))
            if not os.path.exists(dst):
                req = urllib.request.Request(f["url"], headers=UA)
                with urllib.request.urlopen(req, timeout=300) as r, open(dst, "wb") as o:
                    o.write(r.read())
            f["path"] = dst
            return f
    raise RuntimeError(f"no free-licence rain {kind} found on Commons")


def offline_scene(d):
    v = os.path.join(d, "test_rain.mp4"); au = os.path.join(d, "test_rain.wav")
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=0x1a2633:s=1920x1080:d=20", "-f", "lavfi",
       "-i", "nullsrc=s=1920x1080:d=20,geq=random(1)*255:128:128,format=gray", "-filter_complex",
       "[1]boxblur=1,lutyuv=y='if(gt(val,245),220,0)',scroll=v=0.04,format=yuv420p[r];[0][r]blend=all_mode=screen,eq=brightness=-0.05",
       "-r", "30", "-c:v", "libx264", "-preset", "veryfast", v)
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anoisesrc=d=60:c=pink:a=0.5", "-af", "lowpass=f=5000,highpass=f=200", au)
    return dict(path=v, title="File:Test rain.webm", artist="test", lic="CC0", dur=20), \
        dict(path=au, title="File:Test rain.ogg", artist="test", lic="CC0", dur=60)


SCENES = [("Rain on a Window at Night", ["window", "glass"]), ("Rain in a Quiet Forest", ["forest", "tree", "wood", "leaf", "leaves"]),
          ("Rain in the City at Night", ["city", "street", "road", "urban"]), ("Rain on a Calm Lake", ["lake", "pond", "water", "river", "sea"]),
          ("Gentle Rain Falling", [""])]


def scene_name(vtitle):
    t = vtitle.lower()
    for name, keys in SCENES:
        if any(k and k in t for k in keys):
            return name
    # 2026-11-07 review: generic clips all became "Gentle Rain Falling" (3 uploads in a row) — rotate neutral names
    recent = " ".join(used["titles"][-8:])
    return next((n for n in GENERIC if n not in recent), random.choice(GENERIC))


GENERIC = ["Gentle Rain Falling", "Soft Steady Rain", "Peaceful Rainfall", "Relaxing Rain Shower", "Quiet Rainy Day"]


def main():
    tmp = os.path.join(a.home, "sleep_work"); os.makedirs(tmp, exist_ok=True)
    vid, aud = offline_scene(tmp) if a.offline_test else (pick("video"), pick("audio"))
    name = scene_name(vid["title"])
    stamp = time.strftime("%Y%m%d-%H%M")
    # 1) seamless 16 s video unit: 1920x1080 30 fps, calm grade, the clip crossfades into its own start
    src_len = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid["path"]).strip() or 16)
    L = max(6.0, min(16.0, src_len - 2))
    X = min(2.0, L / 4)
    unit = os.path.join(tmp, "unit.mp4")
    pre = (f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,eq=saturation=0.85:brightness=-0.03")
    sh("ffmpeg", "-y", "-v", "error", "-i", vid["path"], "-i", vid["path"], "-filter_complex",
       f"[0:v]{pre},trim={X}:{L + X},setpts=PTS-STARTPTS[body];[1:v]{pre},trim=0:{X},setpts=PTS-STARTPTS[head];"
       f"[body][head]xfade=transition=fade:duration={X}:offset={L - X},format=yuv420p[v]",
       "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-b:v", "1100k", "-maxrate", "1500k", "-bufsize", "3M",
       "-g", "60", unit)
    # 2) real rain audio: loop with a 3 s crossfade, gentle EQ, -20 LUFS (sleep content is quieter on purpose)
    au_len = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", aud["path"]).strip() or 60)
    aunit = os.path.join(tmp, "aunit.m4a")
    AL = max(15.0, min(120.0, au_len - 1))
    sh("ffmpeg", "-y", "-v", "error", "-i", aud["path"], "-i", aud["path"], "-filter_complex",
       f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=3:{AL},asetpts=PTS-STARTPTS[body];"
       f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:3,asetpts=PTS-STARTPTS[head];"
       f"[body][head]acrossfade=d=3:c1=tri:c2=tri,highpass=f=60,lowpass=f=12000,loudnorm=I=-20:TP=-2:LRA=7[o]",
       "-map", "[o]", "-c:a", "aac", "-b:a", "128k", aunit)
    credit = (f"Video: \"{vid['title'].split(':', 1)[1]}\" by {vid['artist']} ({vid['lic']}), Wikimedia Commons.\n"
              f"Rain sound: \"{aud['title'].split(':', 1)[1]}\" by {aud['artist']} ({aud['lic']}), Wikimedia Commons.")
    made = 0
    if a.need_long:
        hours = a.hours or random.choice([2, 3, 3])
        secs = 60 if a.offline_test else int(hours * 3600)
        long_f = os.path.join(a.out, f"{stamp}-0-long.mp4")
        sh("ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", unit, "-stream_loop", "-1", "-i", aunit, "-t", str(secs),
           "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", long_f, timeout=4 * 3600)
        thumb = os.path.join(a.out, f"{stamp}-0-long.jpg")
        txt = f"{int(hours)} HOURS" if not a.offline_test else "3 HOURS"
        # 2026-11-07 Ask Studio (Calm Rain): thumbs were flat/dark and identical → brighter, more contrast, and the
        # badge names this video's scene ("CABIN WINDOW") instead of the same "RAIN FOR SLEEP" every time.
        badge = re.sub(r"[^A-Za-z ]", "", name).strip().upper()[:22] or "RAIN FOR SLEEP"
        sh("ffmpeg", "-y", "-v", "error", "-ss", "3", "-i", unit, "-frames:v", "1", "-vf",
           f"scale=1280:720,eq=brightness=0.03:saturation=1.2:contrast=1.08,drawtext=fontfile={FONT}:text='{txt}':fontsize=110:fontcolor=white:"
           f"borderw=6:bordercolor=black@0.6:x=60:y=h-th-150,drawtext=fontfile={FONT}:text='{badge}':fontsize=64:"
           f"fontcolor=white@0.95:borderw=4:bordercolor=black@0.6:x=64:y=h-th-70", thumb)
        hrs = f"{int(hours)} Hours"
        # 2026-11-07 (PLAN competitors): searchable "Insomnia" + honest "(Real Rain, No AI)" tail, tried first
        # 2026-11-07 (competitors: tiny rain channels at 800k-1M views lead with "Fall Asleep Fast!" + the sound): tried first
        variants = [f"Fall Asleep Fast! {name} | {hrs} of Real Rain Sounds", f"{name} for Insomnia | {hrs} (Real Rain, No AI)", f"{hrs} {name} to Sleep | Real Rain, No AI",
                    f"{name} 🌧️ {hrs} of Real Rain Sounds for Deep Sleep", f"{hrs} of {name} — Fall Asleep Fast",
                    f"Can't Sleep? {name} for {hrs} (Real Rain)", f"{name} Sounds for Sleeping — {hrs} | Calm Your Mind"]
        title = next((t for t in variants if t not in titles and t not in used["titles"]), variants[0] + f" ({stamp[4:8]})")
        json.dump({"file": os.path.basename(long_f), "kind": "long", "pack": stamp, "thumb": os.path.basename(thumb),
                   "title": title[:100],
                   "description": f"{name}: {int(hours)} hours of real, recorded rain sounds to fall asleep fast, study or relax. "
                                  "No music, no talking, no ads in the middle — just steady rain.\n\n" + credit +
                                  "\n\n#rain #rainsounds #sleep #relaxing #whitenoise",
                   "tags": ["rain sounds", "rain for sleep", "sleep sounds", "relaxing rain", "real rain", "white noise",
                            f"{int(hours)} hours rain", "deep sleep", "study", "asmr rain",
                            "rain sounds for sleeping", "fall asleep fast", "rain on window"]},
                  open(os.path.join(a.out, f"{stamp}-0-long.json"), "w"), ensure_ascii=False, indent=1)
        used["titles"].append(title); made += 1
    if a.need_short:
        short_f = os.path.join(a.out, f"{stamp}-1-short.mp4")
        hook = random.choice(["Close your eyes…", "Breathe slowly…", "Listen to the rain…", "Let the day go…"])
        sh("ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", unit, "-stream_loop", "-1", "-i", aunit, "-t", "36",
           "-filter_complex",
           f"[0:v]crop=ih*9/16:ih,scale=1080:1920,drawtext=fontfile={FONT}:text='{hook}':fontsize=78:fontcolor=white:"
           f"borderw=5:bordercolor=black@0.55:x=(w-tw)/2:y=h*0.28,drawtext=fontfile={FONT}:text='real rain for sleep':"
           f"fontsize=46:fontcolor=white@0.9:borderw=3:bordercolor=black@0.5:x=(w-tw)/2:y=h*0.28+110[v];"
           f"[1:a]volume=1.6,afade=t=in:d=0.3[a2]",
           "-map", "[v]", "-map", "[a2]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "128k",
           "-r", "30", short_f)
        st = f"{name} to Fall Asleep Fast 🌧️ #shorts"
        if st in titles or st in used["titles"]:
            st = f"{hook.rstrip('…')} — {name} 🌧️ #shorts"
        json.dump({"file": os.path.basename(short_f), "kind": "short", "pack": stamp, "title": st[:100],
                   "description": "Real rain to calm your mind. The full long version is here: {LONG_URL}\n\n" + credit +
                                  "\n#rain #rainsounds #sleep #shorts",
                   "tags": ["rain sounds", "sleep", "relaxing rain", "real rain", "shorts"]},
                  open(os.path.join(a.out, f"{stamp}-1-short.json"), "w"), ensure_ascii=False, indent=1)
        used["titles"].append(st); made += 1
    if not a.offline_test:
        used["video"].append(vid["title"]); used["audio"].append(aud["title"])
        json.dump(used, open(USED_F, "w"), ensure_ascii=False)
    print("made", made, name)


if __name__ == "__main__":
    main()

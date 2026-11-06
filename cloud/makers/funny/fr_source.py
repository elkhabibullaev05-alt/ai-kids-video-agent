"""Find + download Creative Commons Attribution (CC BY) source clips; offline synthetic fixtures.

YouTube Data API (2026 quota model, checked 2026-11-06 on developers.google.com/youtube/v3/determine_quota_cost):
search.list = 1 unit but a separate limit of 100 search calls/day per Cloud project; videos.list = 1 unit.
We use at most 2 searches + 1-2 videos.list per Short.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import fr_themes as TH

MIN_S, MAX_S = 5, 240


def _dur(iso):
    m = re.match(r"P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def load_used(home):
    try:
        return set(json.load(open(os.path.join(home, "used_sources.json"))))
    except Exception:
        return set()


def save_used(home, used_ids):
    p = os.path.join(home, "used_sources.json")
    old = list(load_used(home))
    allv = old + [x for x in used_ids if x not in old]
    json.dump(allv[-5000:], open(p + ".tmp", "w"))
    os.replace(p + ".tmp", p)


class Finder:
    def __init__(self, yt, home, log=print):
        self.yt, self.home, self.log = yt, home, log
        self.used = load_used(home)
        self.searches = 0
        self.lists = 0
        try:
            r = yt.channels().list(part="id", mine=True).execute()
            self.lists += 1
            self.own = r["items"][0]["id"] if r.get("items") else None
        except Exception as e:  # noqa
            self.own = None
            log("channels.list failed:", str(e)[:200])

    def _search(self, q, order):
        self.searches += 1
        r = self.yt.search().list(part="snippet", q=q, type="video", videoLicense="creativeCommon",
                                  videoDuration="short", maxResults=50, safeSearch="moderate", order=order,
                                  relevanceLanguage="en").execute()
        return [it["id"]["videoId"] for it in r.get("items", []) if it.get("id", {}).get("videoId")]

    def _details(self, ids):
        out = []
        for i in range(0, len(ids), 50):
            self.lists += 1
            r = self.yt.videos().list(part="status,snippet,contentDetails,statistics",
                                      id=",".join(ids[i:i + 50])).execute()
            out += r.get("items", [])
        return out

    def candidates(self, theme, skip=()):
        """CC BY clips for a theme, best first. Double-checks status.license == creativeCommon."""
        name, q, kws = theme
        seen, good = set(skip), []
        for qq, order in ((q, "relevance"), (name.lower() + " funny compilation", "viewCount")):
            ids = [i for i in self._search(qq, order) if i not in seen and i not in self.used]
            seen.update(ids)
            for v in self._details(ids):
                sn, stt, cd = v.get("snippet", {}), v.get("status", {}), v.get("contentDetails", {})
                if stt.get("license") != "creativeCommon":
                    continue
                if sn.get("channelId") == self.own or sn.get("liveBroadcastContent", "none") != "none":
                    continue
                d = _dur(cd.get("duration"))
                if not (MIN_S <= d <= MAX_S):
                    continue
                if cd.get("regionRestriction", {}).get("blocked") and "US" in cd["regionRestriction"]["blocked"]:
                    continue
                if not TH.clip_ok(sn.get("title"), sn.get("description"), kws):
                    continue
                views = int(v.get("statistics", {}).get("viewCount", 0) or 0)
                hd = cd.get("definition") == "hd"
                year = int((sn.get("publishedAt") or "2000")[:4])
                good.append({"id": v["id"], "title": sn.get("title", "").strip(), "channel": sn.get("channelTitle", ""),
                             "channel_id": sn.get("channelId"), "dur": d, "views": views,
                             "score": views ** 0.5 * (1.5 if hd else 1.0) * (1.3 if year >= 2016 else 1.0)})
            if len(good) >= 9:
                break
        good.sort(key=lambda c: -c["score"])
        # at most 2 clips per source channel, so a Short is not one creator's video re-cut
        per, out = {}, []
        for c in good:
            if per.get(c["channel_id"], 0) < 2:
                out.append(c)
                per[c["channel_id"]] = per.get(c["channel_id"], 0) + 1
        return out


def _js_runtime_args():
    deno = shutil.which("deno") or (os.path.expanduser("~/.deno/bin/deno")
                                    if os.path.exists(os.path.expanduser("~/.deno/bin/deno")) else None)
    if deno:
        return ["--js-runtimes", "deno:" + deno]
    node = shutil.which("node")
    if node:
        return ["--js-runtimes", "node:" + node]
    return []


def ytdlp_cmd():
    exe = shutil.which("yt-dlp")
    return [exe] if exe else [sys.executable, "-m", "yt_dlp"]


def download(vid, dst_dir, log=print):
    """720p max mp4. Returns path or None."""
    os.makedirs(dst_dir, exist_ok=True)
    out = os.path.join(dst_dir, vid + ".mp4")
    if os.path.exists(out) and os.path.getsize(out) > 50000:
        return out
    cmd = ytdlp_cmd() + _js_runtime_args() + [
        "-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b[height<=720]/b",
        "--merge-output-format", "mp4", "--no-playlist", "--max-filesize", "300M", "--no-part",
        "--socket-timeout", "30", "--retries", "3", "-q", "--no-warnings", "-o", out,
        "https://www.youtube.com/watch?v=" + vid]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=420)
    except subprocess.TimeoutExpired:
        log("yt-dlp timeout", vid)
        return None
    if p.returncode or not os.path.exists(out):
        log("yt-dlp failed", vid, (p.stderr or p.stdout)[-300:])
        return None
    return out


# ---------------------------------------------------------------- offline fixtures
def synth_clips(dst_dir, n=5, seed=1):
    """n synthetic 'source clips' (moving shapes + tone + one loud 'fail' burst), mixed aspect ratios."""
    import random
    rng = random.Random(seed)
    os.makedirs(dst_dir, exist_ok=True)
    srcs = ["testsrc2", "smptehdbars", "rgbtestsrc", "testsrc", "mandelbrot"]
    cols = ["red", "yellow", "cyan", "magenta", "orange"]
    clips = []
    for i in range(n):
        d = rng.randint(9, 16)
        w, h = ((720, 1280) if i == 2 else (1280, 720))
        peak = round(rng.uniform(3, d - 3), 2)
        out = os.path.join(dst_dir, f"synth{i}.mp4")
        base = srcs[i % len(srcs)]
        vsrc = f"{base}=s={w}x{h}:r=30:d={d}" if base != "mandelbrot" else f"mandelbrot=s={w}x{h}:r=30"
        vf = (f"[0:v]trim=duration={d},setpts=PTS-STARTPTS,format=yuv420p[b];"
              f"[1:v]format=yuva420p[s];"
              f"[b][s]overlay=x='mod(t*{rng.randint(250, 500)},{w})':y='{h // 2}+{h // 3}*sin(t*{rng.uniform(2, 4):.2f})'"
              f":shortest=1,drawbox=x='{w // 3}':y='{h // 3}':w=200:h=200:color=white@0.9:t=fill"
              f":enable='between(t,{peak},{peak + 0.7})'[v]")
        af = (f"[2:a]volume='0.12+0.8*between(t,{peak},{peak + 0.8})':eval=frame[t];"
              f"[3:a]volume='0.9*between(t,{peak},{peak + 0.5})':eval=frame[nz];[t][nz]amix=inputs=2:normalize=0[a]")
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-f", "lavfi", "-i", vsrc,
               "-f", "lavfi", "-i", f"color=c={cols[i % len(cols)]}:s=180x180:r=30:d={d}",
               "-f", "lavfi", "-i", f"sine=f={rng.choice([220, 330, 440, 550])}:d={d}:sample_rate=48000",
               "-f", "lavfi", "-i", f"anoisesrc=d={d}:c=pink:a=0.5:r=48000",
               "-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]", "-t", str(d),
               "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-c:a", "aac", out]
        subprocess.run(cmd, check=True)
        clips.append({"id": f"TEST{i:07d}", "title": f"Synthetic test clip {i + 1} (funny fail)",
                      "channel": f"Test Channel {i + 1}", "channel_id": f"UCtest{i}", "dur": d, "views": 1000 * i,
                      "file": out, "peak_hint": peak})
    return clips

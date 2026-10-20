#!/usr/bin/env python3
"""Cloud worker — one per channel, one per server. No Claude inside.

    python3 cloud/worker.py CHANNEL            # cron, every 20 min (flock keeps one copy running)
    python3 cloud/worker.py CHANNEL --quick    # pipeline test: 2 s of video, no upload, no push

Claude writes the stories into cloud/queue/<CHANNEL>/<id>.json (see cloud/WRITER.md).
This worker: git pull → sync scheduled slots from YouTube → upload anything pending → take the oldest job →
similarity check (no look-alike videos) → voices → Blender render → music → assemble → thumbnail →
rek-ball gate (≥ 85) → Shorts → scheduled upload (made-for-kids flag, 7 languages) →
cloud/results/<CHANNEL>/<id>.json + status.json → git push.  Claude's daily review reads the results.
"""
import datetime as dt
import difflib
import glob
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CH = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: worker.py CHANNEL [--quick]")
QUICK = "--quick" in sys.argv
CFG = json.load(open(os.path.join(ROOT, "cloud", "channels.json")))[CH]
HOME = os.environ.get("KANAL_HOME", os.path.expanduser(f"~/kanal/{CH}"))
WORK = os.path.join(HOME, "work")
STATE_F = os.path.join(HOME, "state.json")
TOKEN = os.path.join(HOME, "token.json")
BL = os.environ.get("BLENDER", "/opt/bl/blender-4.2.3-linux-x64/blender")
PY = sys.executable
ENG = os.path.join(ROOT, CFG["engine"])
Q, DONE, REJ, RES = (os.path.join(ROOT, "cloud", d, CH) for d in ("queue", "done", "rejected", "results"))
GATE = 85
NOW = dt.datetime.now(dt.timezone.utc)
for d in (WORK, Q, DONE, REJ, RES):
    os.makedirs(d, exist_ok=True)


def log(*a):
    print(dt.datetime.now(dt.timezone.utc).strftime("%m-%d %H:%M:%S"), *a, flush=True)


def sh(cmd, cwd=None, check=True, timeout=None):
    log("$", " ".join(str(c) for c in cmd)[:220])
    p = subprocess.run([str(c) for c in cmd], cwd=cwd or ROOT, capture_output=True, text=True, timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f"{os.path.basename(str(cmd[1] if len(cmd) > 1 else cmd[0]))} failed: {(p.stderr or p.stdout)[-800:]}")
    return p


def load_state():
    try:
        return json.load(open(STATE_F))
    except Exception:
        return {"taken": [], "pending": [], "titles": []}


def save_state(st):
    json.dump(st, open(STATE_F + ".tmp", "w"), indent=1)
    os.replace(STATE_F + ".tmp", STATE_F)


# ---------------------------------------------------------------- git
def git(*a, check=True):
    return sh(["git", *a], check=check, timeout=600)


class _GitLock:
    """Several channel workers may share one repo (Windows PC mode): one git operation at a time."""
    def __enter__(self):
        import fcntl
        self.f = open("/tmp/kanal-git.lock", "w"); fcntl.flock(self.f, fcntl.LOCK_EX)
    def __exit__(self, *a):
        self.f.close()


def pull():
    with _GitLock():
        git("pull", "-q", "--rebase", "--autostash", check=False)


def push(msg, paths):
    if QUICK:
        return
    with _GitLock():
        _push(msg, paths)


def _push(msg, paths):
    for p in paths:
        git("add", "-A", "--", p, check=False)
    if not git("diff", "--cached", "--quiet", check=False).returncode:
        return
    git("-c", "user.name=kanal-worker", "-c", "user.email=worker@kanal.local", "commit", "-qm", f"[{CH}] {msg}")
    for _ in range(5):
        if not git("push", "-q", "origin", "HEAD:main", check=False).returncode:
            return
        git("pull", "-q", "--rebase", check=False)
    log("push failed (will retry next run)")


def status(stage, **kw):
    st = load_state()
    d = dict(channel=CH, host=socket.gethostname(), time=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
             stage=stage, queue=len(glob.glob(os.path.join(Q, "*.json"))), pending=len(st["pending"]), **kw)
    json.dump(d, open(os.path.join(RES, "status.json"), "w"), indent=1)


# ---------------------------------------------------------------- YouTube
_yt = None


def yt():
    global _yt
    if _yt is None:
        import youtube_up
        # safety: upload only with a token that belongs to THIS channel. If the owner picked the channels in a
        # different order while signing in, the right token sits in another channel's folder — use that one.
        seen = []
        for tok in [TOKEN] + sorted(glob.glob(os.path.join(os.path.dirname(HOME), "*", "token.json"))):
            if tok in seen or not os.path.exists(tok):
                continue
            seen.append(tok)
            try:
                c = youtube_up.client(tok)
                if youtube_up.my_channel_id(c) == CFG["id"]:
                    _yt = c
                    if tok != TOKEN:
                        log("using token from", tok)
                    break
            except Exception as e:
                log("token check failed:", tok, str(e)[:120])
        if _yt is None:
            raise SystemExit(f"no token for {CFG['name']} ({CFG['id']}) — stop.")
    return _yt


def sync_from_youtube(st):
    """Scheduled (private + publishAt) videos and recent titles straight from the channel — no double booking."""
    y = yt()
    up = y.channels().list(part="contentDetails", id=CFG["id"]).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, titles = [], []
    req = y.playlistItems().list(part="contentDetails,snippet", playlistId=up, maxResults=50)
    for _ in range(4):  # last 200 uploads
        r = req.execute()
        for it in r.get("items", []):
            ids.append(it["contentDetails"]["videoId"]); titles.append(it["snippet"]["title"])
        req = y.playlistItems().list_next(req, r)
        if not req:
            break
    taken = []
    for i in range(0, len(ids), 50):
        for v in y.videos().list(part="status,contentDetails", id=",".join(ids[i:i + 50])).execute().get("items", []):
            pa = v["status"].get("publishAt")
            if pa and pa > NOW.isoformat():
                dur = v["contentDetails"].get("duration", "")
                m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", dur)
                secs = (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else 999
                taken.append({"t": pa.replace(".000Z", "Z"), "kind": "short" if secs <= 60 else "long"})
    keep = [x for x in st["taken"] if x["t"] > NOW.isoformat()]
    seen = {x["t"] for x in taken}
    st["taken"] = taken + [x for x in keep if x["t"] not in seen]
    st["titles"] = titles


def free_slot(st, kind, after=None):
    now = dt.datetime.now(dt.timezone.utc)  # NOW is the process start; a render takes hours, so it is stale here
    after = max(after or now, now + dt.timedelta(minutes=45))
    used = {x["t"] for x in st["taken"]}
    day = after.date()
    for _ in range(30):
        for hm in sorted(CFG["slots"][kind]):
            h, m = map(int, hm.split(":"))
            t = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=dt.timezone.utc)
            iso = t.strftime("%Y-%m-%dT%H:%M:%SZ")
            if t >= after and iso not in used:
                return iso
        day += dt.timedelta(days=1)
    raise RuntimeError("no free slot in 30 days")


def longs_ahead(st):
    return sum(1 for x in st["taken"] if x["kind"] == "long" and x["t"] > NOW.isoformat())


def do_uploads(st):
    import youtube_up
    while st["pending"]:
        it = st["pending"][0]
        res_f = os.path.join(RES, it["job"] + ".json")
        res = json.load(open(res_f)) if os.path.exists(res_f) else {}
        long_id = (res.get("long") or {}).get("video", "")
        desc = it["description"].replace("{LONG_URL}", f"https://youtu.be/{long_id}" if long_id else f"https://www.youtube.com/channel/{CFG['id']}")
        after = None
        if it["kind"] == "short" and (res.get("long") or {}).get("publish_at"):
            after = dt.datetime.fromisoformat(res["long"]["publish_at"].replace("Z", "+00:00")) + dt.timedelta(minutes=20)
        when = free_slot(st, it["kind"], after)
        try:
            vid = youtube_up.upload(yt(), it["file"], it["title"], desc, it.get("tags", []), when, CFG["kids"],
                                    CFG.get("category", "1"), it.get("localizations"), it.get("thumb"))
        except youtube_up.Quota as e:
            log("quota used up, later:", e)
            return False
        log("uploaded", it["kind"], vid, when, it["title"])
        st["taken"].append({"t": when, "kind": it["kind"]})
        entry = {"video": vid, "publish_at": when, "title": it["title"], "ball": it.get("ball")}
        if it["kind"] == "long":
            res["long"] = entry
        else:
            res.setdefault("shorts", []).append(entry)
        json.dump(res, open(res_f, "w"), indent=1, ensure_ascii=False)
        st["pending"].pop(0); save_state(st)
        if not any(p["job"] == it["job"] for p in st["pending"]):
            shutil.rmtree(os.path.join(WORK, it["job"]), ignore_errors=True)
            push(f"{it['job']} uploaded", [RES])
    return True


# ---------------------------------------------------------------- variety check
def words(job):
    return " ".join(b.get("say", "") for b in job["script"].get("beats", [])).lower()


def grams(t, n=5):
    w = re.findall(r"[a-z']+", t)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def similar(job, st):
    t = job["long"]["title"].lower()
    for old in st.get("titles", []) + [json.load(open(f))["long"]["title"] for f in glob.glob(os.path.join(DONE, "*.json"))[-150:]]:
        r = difflib.SequenceMatcher(None, t, old.lower()).ratio()
        if r > 0.78:
            return f"title too close to an old video ({r:.2f}): {old}"
    g = grams(words(job))
    for f in sorted(glob.glob(os.path.join(DONE, "*.json")))[-60:]:
        o = grams(words(json.load(open(f))))
        if g and o:
            j = len(g & o) / len(g | o)
            if j > 0.25:
                return f"dialogue repeats {os.path.basename(f)} ({j:.2f})"
    return None


# ---------------------------------------------------------------- production
def rek(path, title, kind):
    p = sh([PY, os.path.join(ROOT, "tools", "rek_ball.py"), path, title, kind], check=False, timeout=1800)
    try:
        r = json.loads(p.stdout.strip().splitlines()[0])
        return r["ball"], "; ".join(r.get("muammo", [])[:3])
    except Exception:
        return 0, (p.stderr or "rek_ball error")[-300:]


def blender(args):
    cmd = [BL, "-b", "--factory-startup", "-P", os.path.join(ENG, "story.py"), "--", *args]
    p = sh(cmd, check=False, cwd=os.path.join(ROOT, CFG["dir"]))
    if p.returncode and shutil.which("xvfb-run"):
        p = sh(["xvfb-run", "-a", *cmd], check=False, cwd=os.path.join(ROOT, CFG["dir"]))
    if p.returncode:
        raise RuntimeError("blender: " + (p.stderr or p.stdout)[-800:])


def produce(job, jf):
    jid = job["id"]
    d = os.path.join(WORK, jid)
    os.makedirs(d, exist_ok=True)
    json.dump(job["script"], open(os.path.join(d, "script.json"), "w"), indent=1)
    status("voices", job=jid); push(f"{jid} started", [RES])
    if not os.path.exists(os.path.join(d, "timeline.json")):
        out = sh([PY, os.path.join(ENG, "voices.py"), os.path.join(d, "script.json"), d, "12"], cwd=os.path.join(ROOT, CFG["dir"])).stdout
        log((re.findall(r"TOTAL [\d.]+ s", out) or ["?"])[0])
    tl = json.load(open(os.path.join(d, "timeline.json")))
    status("render", job=jid, seconds=tl["duration"])
    rng = ["--range", "1-24"] if QUICK else []
    blender(["--tl", os.path.join(d, "timeline.json"), "--out", os.path.join(d, "frames"), "--res", "854", "--samples", "2", *rng])
    status("assemble", job=jid)
    sh([PY, os.path.join(ENG, "soundtrack.py"), d])
    long_mp4 = os.path.join(d, "long.mp4")
    env_res = ["1280", "720"] if QUICK else []
    sh(["bash", os.path.join(ENG, "assemble_long.sh"), d, long_mp4, *env_res], timeout=4 * 3600)
    frames = sorted(glob.glob(os.path.join(d, "frames", "f_*.png")))
    beats = tl["beats"]
    tb = job["long"].get("thumb_beat", len(beats) // 2)
    fi = min(len(frames) - 1, int((beats[min(tb, len(beats) - 1)]["start"] + 0.8) * 12))
    thumb = os.path.join(d, "thumb.jpg")
    sh([PY, os.path.join(ENG, "thumb.py"), frames[max(fi, 0)], thumb, job["long"].get("thumb_text", "WATCH THIS"),
        "--color", CFG.get("thumb_color", "ffd21e")])
    status("check", job=jid)
    items = []
    ball, why = rek(long_mp4, job["long"]["title"], "long")
    log("rek long", ball, why)
    if ball < GATE and not QUICK:
        return None, f"long rek-ball {ball}: {why}"
    L = job["long"]
    items.append(dict(job=jid, kind="long", file=long_mp4, title=L["title"], description=L["description"], tags=L.get("tags", []),
                      localizations=L.get("localizations"), thumb=thumb, ball=ball))
    for n, s in enumerate(job.get("shorts", []), 1):
        b = beats[min(s.get("beat", 0), len(beats) - 1)]
        start = max(0.0, b["start"] - 0.3)
        dur = min(float(s.get("dur", 30)), max(8.0, tl["duration"] - start - 0.5))
        out = os.path.join(d, f"s{n}.mp4")
        sh([PY, os.path.join(ROOT, "tools", "make_short.py"), long_mp4, out, "--start", f"{start:.2f}", "--dur", f"{dur:.1f}",
            "--top", s.get("top", ""), "--bottom", s.get("bottom", "Full episode on the channel")], timeout=3600)
        sb, swhy = rek(out, s["title"], "short")
        if sb < GATE and not QUICK:
            p = sh([PY, os.path.join(ROOT, "tools", "rek_ball.py"), out, s["title"], "short", "--kuchaytir"], check=False, timeout=1800)
            alt = out[:-4] + "_d.mp4"
            try:
                sb2 = json.loads(p.stdout.strip().splitlines()[0])["ball"]
            except Exception:
                sb2 = 0
            if sb2 >= GATE and os.path.exists(alt):
                out, sb = alt, sb2
        log(f"rek short {n}", sb, swhy)
        if sb < GATE and not QUICK:
            continue
        items.append(dict(job=jid, kind="short", file=out, title=s["title"], description=s["description"], tags=s.get("tags", []),
                          localizations=s.get("localizations"), ball=sb))
    return items, None


def small_thumb(src, dst):
    try:
        from PIL import Image
        im = Image.open(src); im.thumbnail((480, 270)); im.save(dst, quality=80)
    except Exception:
        pass


def main():
    pull()
    st = load_state()
    if QUICK:
        jobs = sorted(glob.glob(os.path.join(ROOT, "cloud", "test_job.json")))
        items, err = produce(json.load(open(jobs[0])), jobs[0])
        log("QUICK result:", err or [(i["kind"], i["file"], i["ball"]) for i in items])
        return
    status("sync")
    sync_from_youtube(st); save_state(st)
    if not do_uploads(st):
        status("quota_wait"); push("quota wait", [RES]); return
    if len(st["pending"]) > 2:
        return
    need = CFG["per_day"]["long"] * 2  # keep two days of long videos scheduled
    if longs_ahead(st) >= need:
        status("idle", ahead=longs_ahead(st)); return
    jobs = sorted(glob.glob(os.path.join(Q, "*.json")))
    if not jobs:
        status("queue_empty", ahead=longs_ahead(st)); push("queue empty", [RES]); return
    jf = jobs[0]
    try:
        job = json.load(open(jf))
        job.setdefault("id", os.path.splitext(os.path.basename(jf))[0])
        bad = similar(job, st)
    except Exception as e:
        job, bad = {"id": os.path.basename(jf)}, f"bad job file: {e}"
    if bad:
        log("REJECT", bad)
        os.replace(jf, os.path.join(REJ, os.path.basename(jf)))
        json.dump({"reason": bad, "time": NOW.isoformat()}, open(os.path.join(REJ, job["id"] + ".reason.json"), "w"))
        status("rejected", job=job["id"], reason=bad); push(f"{job['id']} rejected", [Q, REJ, RES]); return
    try:
        items, err = produce(job, jf)
    except Exception as e:
        err = f"error: {e}"
        log(traceback.format_exc())
        items = None
        fails = st.setdefault("fails", {}); fails[job["id"]] = fails.get(job["id"], 0) + 1; save_state(st)
        if fails[job["id"]] < 3:  # keep the job, the render is resumable
            status("error", job=job["id"], error=str(e)[-500:]); push(f"{job['id']} error", [RES]); return
    if items is None:
        os.replace(jf, os.path.join(REJ, os.path.basename(jf)))
        json.dump({"reason": err, "time": NOW.isoformat()}, open(os.path.join(REJ, job["id"] + ".reason.json"), "w"))
        shutil.rmtree(os.path.join(WORK, job["id"]), ignore_errors=True)
        status("rejected", job=job["id"], reason=err); push(f"{job['id']} rejected", [Q, REJ, RES]); return
    tl = json.load(open(os.path.join(WORK, job["id"], "timeline.json")))
    json.dump({"id": job["id"], "finished": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "seconds": tl["duration"], "place": job["script"].get("set", {}).get("place"),
               "long": None, "shorts": []}, open(os.path.join(RES, job["id"] + ".json"), "w"), indent=1)
    small_thumb(os.path.join(WORK, job["id"], "thumb.jpg"), os.path.join(RES, job["id"] + ".jpg"))
    os.replace(jf, os.path.join(DONE, os.path.basename(jf)))
    st["pending"] += items; save_state(st)
    status("upload", job=job["id"])
    push(f"{job['id']} rendered", [Q, DONE, RES])
    do_uploads(st)
    status("ok", ahead=longs_ahead(st)); push(f"{job['id']} done", [RES])


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):  # e.g. "no token for …" — make it visible in status.json (2026-10-20)
            try:
                status("error", error=str(e.code)[-500:]); push("error", [RES])
            except Exception:
                pass
        raise
    except Exception as e:
        log(traceback.format_exc())
        try:
            status("error", error=str(e)[-500:]); push("error", [RES])
        except Exception:
            pass
        sys.exit(1)

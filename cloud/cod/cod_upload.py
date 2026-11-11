#!/usr/bin/env python3
"""2026-11-11 owner: upload the edited MW4 videos to the new channel MW4 Campaign HD (@MW4CampaignHD,
milanamalina62, own Cloud project mw4-uploader). English titles/tags for US/EU (high-RPM) viewers,
scheduled for US prime time. Per day: 1 long mission video + 3 Shorts (6 uploads/day max by API quota).
State: /root/kanal/cod/uploaded.json. Progress for Claude: Videos\\MW4\\tayyor\\yuklash.txt"""
import json, os, sys, subprocess, glob, datetime as dt
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import youtube_up as Y

HOME = "/root/kanal/cod"; TOKEN = os.path.join(HOME, "token.json"); STATE = os.path.join(HOME, "uploaded.json")
JOB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "job.json")))
OUT = JOB["out"]
if not os.path.isdir(OUT) or not glob.glob(os.path.join(OUT, "*.mp4")):
    OUT = JOB.get("out_fallback", OUT) if os.path.isdir(JOB.get("out_fallback", "")) else OUT
os.makedirs(OUT, exist_ok=True); LOG = os.path.join(OUT, "yuklash.txt")
PER_DAY = {"long": 2, "short": 6}   # 2026-11-11 owner: 2 long + 6 Shorts a day (API quota ~6/day -> rest rolls to next day until a 2nd project is added)
SLOTS = {"long": [23, 2], "short": [13, 15, 17, 19, 21, 1]}   # UTC; long = 18:00 & 21:00 US Eastern, Shorts spread 08:00-20:00 ET
TAGS = ["call of duty", "modern warfare 4", "mw4", "mw4 campaign", "call of duty modern warfare 4", "mw4 gameplay",
        "mw4 walkthrough", "no commentary", "full game", "campaign walkthrough", "cinematic", "1080p 60fps",
        "cod mw4", "call of duty 2026", "fps", "gaming"]
DESC = ("Call of Duty: Modern Warfare 4 campaign gameplay in 1080p 60FPS. No commentary, full cinematic experience.\n\n"
        "Subscribe for every MW4 mission and the best moments as Shorts.\n\n"
        "#CallOfDuty #ModernWarfare4 #MW4 #MW4Campaign #NoCommentary #Gaming")

def log(*a):
    s = dt.datetime.now().strftime("%m-%d %H:%M ") + " ".join(map(str, a))
    print(s, flush=True); open(LOG, "a").write(s + "\n")

def font():
    a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Anton-Regular.ttf")  # v2 thumbnails
    if os.path.exists(a): return a
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p): return p
    return glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)[0]

def thumb(m, n):
    """2026-11-11 owner: thumbnail like the top MW4 walkthroughs (theRadBrad 5.3M, GameRiot): close-up character
    face from a cutscene filling the frame, huge white 'PART N' with a heavy black outline bottom-left, tiny red MW4 tag."""
    out = os.path.join(OUT, f"{m['file']}_thumb_v3.jpg")
    if os.path.exists(out): return out
    F = font()
    vf = (f"crop=iw*0.70:ih*0.70:iw*0.15:ih*0.13,scale=1280:720:flags=lanczos,"
          f"eq=gamma=1.18:saturation=1.4:contrast=1.15:brightness=0.02,unsharp=5:5:0.9,vignette=PI/5,"
          f"drawbox=x=0:y=500:w=1280:h=220:color=black@0.35:t=fill,"
          f"drawbox=x=36:y=34:w=170:h=78:color=0xD81E1E@1:t=fill,"
          f"drawtext=fontfile='{F}':text='MW4':fontsize=62:fontcolor=white:x=36+(170-text_w)/2:y=44,"
          f"drawtext=fontfile='{F}':text='PART {n}':fontsize=200:fontcolor=white:borderw=14:bordercolor=black:x=48:y=h-text_h-40")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(m["thumb_t"]), "-i", JOB["src"], "-frames:v", "1", "-vf", vf,
                    "-q:v", "2", out], check=True)
    return out

def cold_open(m):
    """2026-11-11 retention: open the long video on its loudest action moment (8 s teaser), then the mission.
    Built on the WSL disk (E:) because C: is nearly full. Returns the path to upload."""
    src_long = os.path.join(OUT, m["file"] + ".mp4"); os.makedirs(os.path.join(HOME, "up"), exist_ok=True)
    final = os.path.join(HOME, "up", m["file"] + "_co.mp4")
    if os.path.exists(final): return final
    try:
        best, bt = -1, m.get("teaser_t")  # 2026-11-11: hand-picked moment; scanning audio over /mnt/e took >10 min
        for a, b in ([] if bt is not None else m["keep"]):
            if b - a < 20: continue
            au = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", JOB["src"], "-vn", "-ac", "1",
                                 "-ar", "4000", "-f", "s16le", "-"], capture_output=True).stdout
            x = np.frombuffer(au, np.int16).astype(np.float32) / 32768
            n = len(x) // 4000
            if n < 12: continue
            r = np.sqrt((x[:n*4000].reshape(n, 4000) ** 2).mean(1))
            w = np.convolve(r, np.ones(8), "valid"); i = int(np.argmax(w[2:-2])) + 2
            if w[i] > best: best, bt = w[i], a + i
        if bt is None: return src_long
        tz = os.path.join(HOME, "up", m["file"] + "_teaser.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(bt), "-t", "8", "-i", JOB["src"], "-vf",
                        "fade=t=out:st=7.7:d=0.3", "-af", "afade=t=out:st=7.6:d=0.4",
                        "-c:v", "h264_nvenc", "-preset", "p6", "-rc", "vbr", "-cq", "18", "-b:v", "0", "-profile:v", "high",
                        "-pix_fmt", "yuv420p", "-r", "60", "-g", "120", "-video_track_timescale", "15360",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", tz], check=True)
        lst = tz + ".txt"; open(lst, "w").write(f"file '{tz}'\nfile '{src_long}'\n")
        # 2026-11-11: the laptop is often on a phone hotspot -> 25-28 Mbps masters (3-7.5 GB) took hours to upload.
        # Upload copy at YouTube's recommended 1080p60 rate (12 Mbps); YouTube re-encodes anyway. Masters stay on E:.
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c:v", "h264_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr", "-b:v", "12M", "-maxrate", "16M",
                        "-bufsize", "24M", "-spatial-aq", "1", "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac",
                        "-b:a", "192k", "-movflags", "+faststart", final + ".part.mp4"], check=True)
        os.replace(final + ".part.mp4", final); os.remove(tz); os.remove(lst)
        log(m["id"], f"cold open qo'shildi ({bt:.0f}s dagi eng shiddatli joy)")
        return final
    except Exception as e:
        log(m["id"], "cold open xato, asl video yuklanadi:", e); return src_long

def plan():
    items = []
    for n, m in enumerate(JOB["missions"], 1):
        name = m.get("name", f"Mission {n}")  # 2026-11-11: theRadBrad-style title (most-viewed MW4 walkthrough)
        long_it = dict(key=f"{m['id']}{JOB.get('key_ver', '')}_long", kind="long", path=os.path.join(OUT, m["file"] + ".mp4"), m=m, n=n,
                       title=f"CALL OF DUTY MODERN WARFARE 4 Campaign Walkthrough Gameplay Part {n} - {name} (1080p 60FPS)"[:100])
        for k, s in enumerate(m.get("shorts", []), 1):
            t = s.get("yt_title") or s.get("hook") or f"{s.get('title', '').title()} - Call of Duty Modern Warfare 4"
            items.append(dict(key=f"{m['id']}{JOB.get('key_ver', '')}_short{k}", kind="short", m=m, n=n,
                              path=os.path.join(OUT, f"{m['file']}_{JOB.get('short_tag', 'shortHD')}{k}.mp4"),
                              title=(t[:68] + " #mw4 #modernwarfare4 #cod")))  # 2026-11-11 vidIQ: viral MW4 Shorts all carry these hashtags
        items.append(long_it)  # 2026-11-11: Shorts first (small files pass a slow hotspot quickly), then the long video
    # one long then its 3 Shorts, mission by mission
    return items

def next_slot(kind, used, now):
    d = now.date()
    for day in range(0, 30):
        for h in SLOTS[kind]:
            t = dt.datetime.combine(d + dt.timedelta(days=day), dt.time(h, 0), dt.timezone.utc)
            if t > now + dt.timedelta(hours=1) and t.isoformat() not in used:
                return t

def main():
    if not os.path.exists(TOKEN): print("no token"); return
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"done": {}, "slots": []}
    today = dt.datetime.utcnow().date().isoformat()
    cnt = {"long": 0, "short": 0}
    for v in st["done"].values():
        if v.get("day") == today: cnt[v["kind"]] += 1
    yt = Y.client(TOKEN)
    if Y.my_channel_id(yt) != "UCOJQ4gIRQMlbdr4weDxiVmQ": log("XATO: token boshqa kanalniki"); return
    # 2026-11-11 owner: first-session videos must not come out -> private + schedule cancelled (not deleted)
    for vid in JOB.get("cancel_ids", []):
        if vid in st.setdefault("cancelled", []): continue
        try:
            r = Y.make_private(yt, vid); st["cancelled"].append(vid); log("yopildi (chiqmaydi):", vid, r)
        except Exception as e:
            log("yopib bo'lmadi:", vid, str(e)[:120])
    # also anything else uploaded from the first session (m1..m4 keys, e.g. an upload that was still running)
    for key, v in st["done"].items():
        if key.split("_")[0] in JOB.get("cancel_missions", []) and v["id"] not in st["cancelled"]:
            try:
                r = Y.make_private(yt, v["id"]); st["cancelled"].append(v["id"]); log("yopildi (chiqmaydi):", key, v["id"], r)
            except Exception as e:
                log("yopib bo'lmadi:", key, str(e)[:120])
    json.dump(st, open(STATE, "w"), indent=1)
    if not JOB.get("upload_enabled", True):
        log("yuklash vaqtincha o'chiq (yangi montaj tayyorlanmoqda)"); return
    # 2026-11-11: post the engagement question once a video is public
    now0 = dt.datetime.now(dt.timezone.utc)
    for key, v in st["done"].items():
        if v.get("commented") or dt.datetime.fromisoformat(v["at"]) > now0: continue
        q = ("Which MW4 mission was the hardest for you? 👇" if v["kind"] == "long"
             else "Would you play this mission again? 🔥 Full mission on the channel!")
        try:
            yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": v["id"], "topLevelComment":
                                       {"snippet": {"textOriginal": q}}}}).execute()
            v["commented"] = True; log("izoh yozildi:", key)
        except Exception as e:
            log("izoh hali yozilmadi:", key, str(e)[:100])
    json.dump(st, open(STATE, "w"), indent=1)
    for it in plan():
        if it["key"] in st["done"] or cnt[it["kind"]] >= PER_DAY[it["kind"]]: continue
        if not os.path.exists(it["path"]): continue
        now = dt.datetime.now(dt.timezone.utc); t = next_slot(it["kind"], st["slots"], now)
        th = thumb(it["m"], it["n"]) if it["kind"] == "long" else None
        path = cold_open(it["m"]) if it["kind"] == "long" else it["path"]
        tags = TAGS + ([f"mw4 mission {it['n']}"] if it["kind"] == "long" else ["shorts", "mw4 shorts"])
        try:
            vid = Y.upload(yt, path, it["title"], DESC, tags, t.isoformat().replace("+00:00", "Z"), kids=False,
                           category="20", thumb=th)
        except Y.Quota as e:
            log("kunlik YouTube limiti tugadi, ertaga davom etadi:", e); break
        st["done"][it["key"]] = {"id": vid, "kind": it["kind"], "day": today, "at": t.isoformat(), "title": it["title"]}
        st["slots"].append(t.isoformat()); cnt[it["kind"]] += 1
        if path.startswith(os.path.join(HOME, "up")):
            try: os.remove(path)
            except OSError: pass
        # engagement comment is posted after the video goes public (scheduled/private videos refuse comments: 403)
        json.dump(st, open(STATE, "w"), indent=1)
        if it["kind"] == "long":  # 2026-11-11 owner: link this mission's Shorts to the full video
            pre = it["key"][:-len("_long")]
            for k2, v2 in st["done"].items():
                if k2.startswith(pre + "_short") and not v2.get("linked"):
                    try:
                        Y.set_description(yt, v2["id"], f"Full mission (Part {it['n']}): https://youtu.be/{vid}\n\n" + DESC
                                          + Y.cross_footer(yt, False))
                        v2["linked"] = vid
                    except Exception as e:
                        log("Shorts ga havola qo'yilmadi:", k2, str(e)[:100])
            json.dump(st, open(STATE, "w"), indent=1)
        else:  # the long video may already be up: link straight away
            lk = st["done"].get(it["key"].split("_short")[0] + "_long")
            if lk:
                try:
                    Y.set_description(yt, vid, f"Full mission (Part {it['n']}): https://youtu.be/{lk['id']}\n\n" + DESC
                                      + Y.cross_footer(yt, False))
                    st["done"][it["key"]]["linked"] = lk["id"]; json.dump(st, open(STATE, "w"), indent=1)
                except Exception as e:
                    log("Shorts ga havola qo'yilmadi:", it["key"], str(e)[:100])
        log(f"YUKLANDI {it['key']} -> https://youtu.be/{vid} | chiqadi {t:%Y-%m-%d %H:%M} UTC | {it['title']}")
    log(f"bugun: {cnt['long']} uzun + {cnt['short']} Shorts; jami yuklangan {len(st['done'])}/{len(plan())}")

if __name__ == "__main__":
    main()

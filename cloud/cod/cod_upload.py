#!/usr/bin/env python3
"""2026-11-11 owner: upload the edited MW4 videos to the new channel MW4 Campaign HD (@MW4CampaignHD,
milanamalina62, own Cloud project mw4-uploader). English titles/tags for US/EU (high-RPM) viewers,
scheduled for US prime time. Per day: 1 long mission video + 3 Shorts (6 uploads/day max by API quota).
State: /root/kanal/cod/uploaded.json. Progress for Claude: Videos\\MW4\\tayyor\\yuklash.txt"""
import json, os, sys, subprocess, glob, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import youtube_up as Y

HOME = "/root/kanal/cod"; TOKEN = os.path.join(HOME, "token.json"); STATE = os.path.join(HOME, "uploaded.json")
JOB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "job.json")))
OUT = JOB["out"]; LOG = os.path.join(OUT, "yuklash.txt")
PER_DAY = {"long": 1, "short": 3}
SLOTS = {"long": [23], "short": [16, 20, 1]}   # UTC hours = 11:00, 15:00, 20:00 / 18:00 US Eastern
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
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p): return p
    return glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)[0]

def thumb(m, n):
    """1280x720 thumbnail: graded frame, big yellow MISSION N, red MW4 tag (style of top CoD walkthrough channels)."""
    out = os.path.join(OUT, f"{m['file']}_thumb_v2.jpg")
    if os.path.exists(out): return out
    F = font()
    vf = (f"scale=1280:720,eq=saturation=1.3:contrast=1.15:brightness=0.03,"
          f"drawbox=x=0:y=470:w=1280:h=250:color=black@0.55:t=fill,"
          f"drawbox=x=40:y=40:w=230:h=110:color=0xD81E1E@1:t=fill,"
          f"drawtext=fontfile='{F}':text='MW4':fontsize=86:fontcolor=white:x=40+(230-text_w)/2:y=52,"
          f"drawtext=fontfile='{F}':text='MISSION {n}':fontsize=150:fontcolor=0xFFD200:borderw=8:bordercolor=black:x=(w-text_w)/2:y=505,"
          f"drawtext=fontfile='{F}':text='NO COMMENTARY':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=670")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(m["thumb_t"]), "-i", JOB["src"], "-frames:v", "1", "-vf", vf,
                    "-q:v", "2", out], check=True)
    return out

def plan():
    items = []
    for n, m in enumerate(JOB["missions"], 1):
        part = " Finale" if n == 1 else ""
        items.append(dict(key=f"{m['id']}_long", kind="long", path=os.path.join(OUT, m["file"] + ".mp4"), m=m, n=n,
                          title=f"CALL OF DUTY MODERN WARFARE 4 Campaign Walkthrough Part {n} - Mission {n}{part} [1080p 60FPS] No Commentary"))
        for k, s in enumerate(m.get("shorts", []), 1):
            hook = s.get("hook") or f"{s.get('title', '').title()} - Call of Duty Modern Warfare 4"
            items.append(dict(key=f"{m['id']}_short{k}", kind="short", m=m, n=n,
                              path=os.path.join(OUT, f"{m['file']}_{JOB.get('short_tag', 'shortHD')}{k}.mp4"),
                              title=(hook[:85] + " #shorts")))
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
    for it in plan():
        if it["key"] in st["done"] or cnt[it["kind"]] >= PER_DAY[it["kind"]]: continue
        if not os.path.exists(it["path"]): continue
        now = dt.datetime.now(dt.timezone.utc); t = next_slot(it["kind"], st["slots"], now)
        th = thumb(it["m"], it["n"]) if it["kind"] == "long" else None
        tags = TAGS + ([f"mw4 mission {it['n']}"] if it["kind"] == "long" else ["shorts", "mw4 shorts"])
        try:
            vid = Y.upload(yt, it["path"], it["title"], DESC, tags, t.isoformat().replace("+00:00", "Z"), kids=False,
                           category="20", thumb=th)
        except Y.Quota as e:
            log("kunlik YouTube limiti tugadi, ertaga davom etadi:", e); break
        st["done"][it["key"]] = {"id": vid, "kind": it["kind"], "day": today, "at": t.isoformat(), "title": it["title"]}
        st["slots"].append(t.isoformat()); cnt[it["kind"]] += 1
        json.dump(st, open(STATE, "w"), indent=1)
        log(f"YUKLANDI {it['key']} -> https://youtu.be/{vid} | chiqadi {t:%Y-%m-%d %H:%M} UTC | {it['title']}")
    log(f"bugun: {cnt['long']} uzun + {cnt['short']} Shorts; jami yuklangan {len(st['done'])}/{len(plan())}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Agentlar markazi: yangi noutbuk (KOMPUTER) ishchilarining holatini GitHub repodan yig'adi.
# Ishlatish: python3 hub_sync.py <repo_dir> <out_dir>
# Chiqadi: <out_dir>/agents/<key>.json (merge uchun), <out_dir>/pipeline/<key>.json, <out_dir>/sync.json
import json, os, subprocess, sys, datetime as dt, re, glob

repo, out = sys.argv[1], sys.argv[2]
UTC = dt.timezone.utc
BISH = dt.timezone(dt.timedelta(hours=6))
now = dt.datetime.now(UTC)
# worker channel -> hub key
MAP = {"maxcat": "max", "doughbros": "dough", "hollow": "hollow", "bolt": "bolt", "roblox": "roblox", "grind": "phonk",
       "funny": "funny", "money": "money", "ufc": "ufc", "sleep": "sleep"}
UZ = {"sync": "YouTube bilan solishtiryapti", "voices": "ovoz yozyapti", "render": "3D render qilyapti",
      "assemble": "montaj qilyapti", "check": "sifatni tekshiryapti", "upload": "YouTube'ga yuklayapti",
      "ok": "tayyor, keyingisini kutyapti", "idle": "oldinga yetarli video bor — dam olyapti",
      "queue_empty": "yangi hikoya kutyapti", "quota_wait": "YouTube kunlik limiti tugadi — limit yangilanganda o'zi yuklaydi",
      "net_wait": "internet uzildi — o'zi qayta urinadi", "rejected": "video sifatdan o'tmadi, qayta qilinadi"}

def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout

log = git("log", "--since=3 days ago", "--pretty=%cI\t%s").splitlines()
os.makedirs(f"{out}/agents", exist_ok=True); os.makedirs(f"{out}/pipeline", exist_ok=True)

def bt(iso):
    return dt.datetime.fromisoformat(iso).astimezone(BISH)

today = now.astimezone(BISH).date()
summary = []
for ch, key in MAP.items():
    p = f"{repo}/cloud/results/{ch}/status.json"
    if not os.path.exists(p):
        continue
    st = json.load(open(p))
    pipe = dict(st)
    json.dump(pipe, open(f"{out}/pipeline/{key}.json", "w"), ensure_ascii=False)
    lines = [(t, s) for t, s in (l.split("\t", 1) for l in log if "\t" in l) if s.startswith(f"[{ch}]")]
    act, up_today, up_24 = [], 0, 0
    for t, s in reversed(lines[:40]):
        msg = s[len(ch) + 3:]
        d = bt(t)
        if msg.endswith(" uploaded"):
            if d.date() == today: up_today += 1
            if now - d.astimezone(UTC) < dt.timedelta(hours=24): up_24 += 1
        msg = (msg.replace(" uploaded", " — YouTube'ga yuklandi (rejali)").replace(" rendered", " — tayyorlandi")
                  .replace(" started", " — boshlandi").replace(" done", " — tugadi").replace(" rejected", " — rad etildi")
                  .replace("quota wait", "YouTube limiti — kutyapti").replace("queue empty", "hikoya tugagan")
                  .replace("error", "xato").replace("worker stopped", "to'xtatilgan (egasi o'chirgan)"))
        act.append(f"[{d:%d.%m %H:%M}] {msg}")
    act = act[-14:]
    stage = st.get("stage", "")
    age_h = (now - dt.datetime.fromisoformat(st["time"]).astimezone(UTC)).total_seconds() / 3600 if st.get("time") else 99
    if st.get("note", "").startswith("stopped"):
        status, text = "idle", "To'xtatilgan."
    elif stage == "error":
        e = st.get("error", "")
        if "no token" in e:
            status, text = "bad", "YouTube ulanmagan — Hujjatlar papkasidagi QOLGAN_KANALLARNI_ULASH.bat ni ishga tushiring."
        elif re.search(r"name resolution|timed out|Connection|SSL", e):
            status, text = "warn", "Internet uzilib qoldi — keyingi aylanishda o'zi qayta urinadi."
        else:
            status, text = "bad", "Xato: " + e[:160]
    elif age_h > 3:
        status, text = "bad", f"Ishchi {int(age_h)} soatdan beri jim — noutbuk o'chiq yoki uxlayaptimi?"
    elif stage in ("quota_wait", "queue_empty", "net_wait", "rejected"):
        status, text = "warn", UZ.get(stage, stage)
    else:
        status, text = "ok", UZ.get(stage, stage)
    extra = []
    if st.get("job"): extra.append(f"hozirgi video: {st['job']}")
    extra.append(f"navbatda hikoya: {st.get('queue', 0)}")
    if st.get("pending"): extra.append(f"yuklashni kutyapti: {st['pending']}")
    if st.get("ahead") is not None: extra.append(f"oldinga rejalangan: {st['ahead']}")
    extra.append(f"oxirgi 24 soatda yuklandi: {up_24}")
    doc = {"status": status, "status_text": text + " · " + ", ".join(extra), "activity": act,
           "last_seen": st.get("time"), "host": st.get("host"), "today_made": up_today}
    json.dump(doc, open(f"{out}/agents/{key}.json", "w"), ensure_ascii=False)
    summary.append(f"{key}:{status}")

# Eski noutbukdagi (hali o'rnatilmagan) agentlar
for key, name in {"funny": "Funny Rank", "money": "Money Story", "ufc": "Wild Sketchbook", "sleep": "Calm Rain"}.items():
    if os.path.exists(f"{repo}/cloud/results/{key}/status.json"):
        continue
    json.dump({"status": "bad", "status_text": f"{name} agenti eski noutbukda qolgan — yangi noutbukka hali o'rnatilmagan, video chiqmayapti.",
               "today_made": 0}, open(f"{out}/agents/{key}.json", "w"), ensure_ascii=False)
    summary.append(f"{key}:bad")

json.dump({"at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "error": None, "source": "KOMPUTER (GitHub)"},
          open(f"{out}/sync.json", "w"))
print(" ".join(summary))

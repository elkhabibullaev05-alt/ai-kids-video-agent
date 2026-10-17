"""Rek-ball: har bir videoni YouTube'ga yuklashdan oldin 100 ballik baholaydi.

85 balldan past video yuklanmaydi: fayl videolar/rad_etilgan/ ga ko'chadi, epizod navbatdan olinadi,
agent o'zi yangi video yasaydi. Bir kunda ko'pi bilan KUNLIK_RAD ta rad — undan keyin o'sha kuni yangi
video yasalmaydi (kompyuter va API behuda yonmasin), ertasi kuni yana boshlanadi.

Agentlar shunday ishlatadi:
    import rek_ball as rek                     (markaz papkasi sys.path'da)
    pending = rek.filtr(st, pending, "funny", log)
    if rek.limit(st, log): return {}           (make_episode boshida)
Faqat ffmpeg va numpy kerak (ffmpeg PATH'da yoki imageio-ffmpeg orqali).
"""
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:  # numpy bo'lmasa sekinroq, oddiy Python bilan hisoblanadi
    np = None

CHEGARA = 85
KUNLIK_RAD = 4
_NOWIN = 0x08000000 if sys.platform == "win32" else 0  # CREATE_NO_WINDOW: qora oyna chiqmasin


def _ffmpeg():
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


FF = _ffmpeg()


def _run(args, binary=False):
    return subprocess.run([FF, "-hide_banner", "-nostdin"] + args, capture_output=True,
                          text=not binary, creationflags=_NOWIN, timeout=900)


def _info(path):
    e = _run(["-i", str(path)]).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e)
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)) if d else 0.0
    v = re.search(r"Video: .*?, (\d{2,5})x(\d{2,5})", e)
    w, h = (int(v.group(1)), int(v.group(2))) if v else (0, 0)
    return dur, w, h, ("Audio:" in e)


def _frames(path, step, dur, w=96):
    """Kulrang kichik kadrlar (har biri bytes). Uzun videoda faqat boshidan 120 s."""
    lim = ["-t", "120"] if dur > 150 else []
    h = w * 16 // 9
    r = _run(lim + ["-i", str(path), "-vf", f"fps={1 / step:.4f},scale={w}:{h},format=gray",
                    "-f", "rawvideo", "-"], binary=True)
    raw = r.stdout or b""
    n = len(raw) // (w * h)
    return [raw[i * w * h:(i + 1) * w * h] for i in range(n)]


def _mean(b):
    return sum(b) / max(len(b), 1)


def _absdiff(a, b):
    if np is not None:
        return float(np.abs(np.frombuffer(a, np.uint8).astype(np.int16) - np.frombuffer(b, np.uint8)).mean())
    return sum(abs(x - y) for x, y in zip(a, b)) / max(len(a), 1)


def _vol(path, ss=None, t=None):
    a = (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t is not None else [])
    e = _run(a + ["-i", str(path), "-af", "volumedetect", "-vn", "-f", "null", "-"]).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", e)
    x = re.search(r"max_volume: (-?[\d.]+) dB", e)
    return (float(m.group(1)) if m else -99.0), (float(x.group(1)) if x else 0.0)


def _silences(path, dur):
    a = ["-t", "600"] if dur > 900 else []
    e = _run(a + ["-i", str(path), "-af", "silencedetect=n=-40dB:d=0.6", "-vn", "-f", "null", "-"]).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", e)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    return [(max(s, 0.0), en[i] if i < len(en) else min(dur, 600)) for i, s in enumerate(st)]


def olch(path):
    """Videoning raqamli o'lchovlari."""
    dur, w, h, has_a = _info(path)
    step = 0.25 if dur <= 180 else 1.0
    fr = _frames(path, step, dur)
    diff = [_absdiff(fr[i], fr[i + 1]) for i in range(len(fr) - 1)]
    cuts = sum(1 for x in diff if x > 28)
    seen = min(dur, 120.0) if dur > 150 else dur
    still = best = 0.0
    for x in diff:
        still = still + step if x < 2.0 else 0.0
        best = max(best, still)
    k3 = max(1, int(3 / step))
    m = {
        "dur": round(dur, 1), "w": w, "h": h, "audio": has_a,
        "hook_motion": round(sum(diff[:k3]) / len(diff[:k3]) if diff else 0.0, 1),
        "dark_start": bool(fr and _mean(fr[0]) < 20),
        "cuts_10s": round(cuts / max(seen, 1) * 10, 2),
        "motion": round(sum(diff) / len(diff) if diff else 0.0, 1),
        "static_s": round(best, 1),
        "loop": round(1 - _absdiff(fr[0], fr[-1]) / 255, 3) if len(fr) > 2 and dur <= 180 else None,
    }
    if has_a:
        m["db"], m["db_max"] = _vol(path) if dur <= 900 else _vol(path, 60, 300)
        m["db3"], _ = _vol(path, 0, 3)
        sil = _silences(path, dur)
        m["silent_start"] = round(next((e - s for s, e in sil if s <= 0.1), 0.0), 2)
        m["silent_s"] = round(sum(e - s for s, e in sil), 1)
    else:
        m.update(db=-99.0, db_max=0.0, db3=-99.0, silent_start=dur, silent_s=dur)
    return m


def _pick(x, steps):
    """steps: [(chegara, ball), ...] kamayish tartibida; x >= chegara bo'lsa shu ball."""
    for lim, pts in steps:
        if x >= lim:
            return pts
    return 0


def _title_pts(title):
    t = (title or "").strip()
    p = 0
    p += 4 if 15 <= len(t) <= 60 else (2 if t else 0)
    p += 3 if re.search(r"[?!😂😱🔥👇💀🤯]|\d|vs|why|how|what|never|secret|ranked|top", t, re.I) else 0
    p += 3 if not re.search(r"episode\s*\d+|^ep\s*\d+", t, re.I) else 0
    return p


def ball(m, title, kind):
    """kind: short | long | ambient. Qaytaradi: (ball, {bo'lim: ball}, [muammolar])."""
    q = []
    db_pts = 5 if -18 <= m["db"] <= -8 else (3 if -23 <= m["db"] < -18 else 0)
    clip_pts = 5 if m["db_max"] < -0.5 else 2
    if kind == "ambient":  # uyqu/yomg'ir: tinch bo'lishi kerak, tez kadr talab qilinmaydi
        s = {
            "davomiylik": _pick(m["dur"], [(3600, 25), (1800, 18), (600, 10)]),
            "ovoz": (15 if -30 <= m["db"] <= -12 else 6) + (10 if m["silent_s"] < 5 else 0),
            "texnik": (15 if max(m["w"], m["h"]) >= 1920 else 8) + clip_pts * 2,
            "nom": _title_pts(title) + 15 if _title_pts(title) >= 7 else _title_pts(title) + 8,
        }
        if m["silent_s"] >= 5:
            q.append(f"ovozda {m['silent_s']} s jimlik")
        if m["dur"] < 1800:
            q.append("uyqu videosi uchun juda qisqa")
    elif kind == "short":
        s = {
            "hook": _pick(m["hook_motion"], [(10, 15), (6, 10), (3, 5)]) + (5 if m["silent_start"] < 0.3 else 0)
                    + (5 if not m["dark_start"] else 0) + (5 if m["db3"] >= -20 else 3 if m["db3"] >= -26 else 0),
            "temp": _pick(m["cuts_10s"], [(3, 12), (1.5, 8), (0.5, 4)]) + _pick(m["motion"], [(8, 8), (4, 5), (2, 2)])
                    + (5 if m["static_s"] < 3 else 3 if m["static_s"] < 5 else 0),
            "uzunlik": 10 if 15 <= m["dur"] <= 45 else 7 if m["dur"] <= 60 else 4,
            "loop": 10 if (m["loop"] or 0) >= 0.85 else 6 if (m["loop"] or 0) >= 0.75 else 3,
            "texnik": (5 if m["h"] >= 1920 and m["h"] > m["w"] else 2) + db_pts + clip_pts,
            "nom": _title_pts(title),
        }
        if m["hook_motion"] < 6:
            q.append(f"birinchi 3 s da harakat kam ({m['hook_motion']})")
        if m["silent_start"] >= 0.3:
            q.append(f"boshida {m['silent_start']} s jimlik")
        if m["cuts_10s"] < 1.5 and m["motion"] < 8:
            q.append("kadr juda sekin o'zgaradi")
        if m["static_s"] >= 3:
            q.append(f"{m['static_s']} s qotib qolgan joy")
        if (m["loop"] or 0) < 0.75:
            q.append("oxiri boshiga ulanmaydi")
    else:  # long
        s = {
            "hook": _pick(m["hook_motion"], [(8, 15), (4, 10), (2, 5)]) + (5 if m["silent_start"] < 0.5 else 0)
                    + (5 if not m["dark_start"] else 0) + (5 if m["db3"] >= -22 else 0),
            "temp": _pick(m["cuts_10s"], [(1, 12), (0.4, 8), (0.15, 4)]) + _pick(m["motion"], [(6, 8), (3, 5), (1.5, 2)])
                    + (5 if m["static_s"] < 10 else 3 if m["static_s"] < 20 else 0),
            "uzunlik": 10 if m["dur"] >= 240 else 6 if m["dur"] >= 90 else 3,
            "jimlik": 10 if m["silent_s"] < 3 else 5 if m["silent_s"] < 10 else 0,
            "texnik": (5 if m["w"] >= 1920 and m["w"] > m["h"] else 2) + db_pts + clip_pts,
            "nom": _title_pts(title),
        }
        if m["hook_motion"] < 4:
            q.append(f"boshlanishi sust (harakat {m['hook_motion']})")
        if m["static_s"] >= 10:
            q.append(f"{m['static_s']} s qotib qolgan joy")
        if m["dur"] < 240:
            q.append("uzun video uchun qisqa (4 daqiqadan kam)")
    if m["db"] < -23:
        q.append(f"ovoz past ({m['db']} dB)")
    if m["db_max"] >= -0.5:
        q.append("ovoz chegaradan oshib ketgan (clipping)")
    if _title_pts(title) < 7:
        q.append("nomi kuchsiz")
    return int(sum(s.values())), s, q


def baho(path, title, kind=None):
    m = olch(path)
    if kind is None:
        kind = "short" if (m["h"] > m["w"] and m["dur"] <= 180) else "long"
    b, s, q = ball(m, title, kind)
    return {"ball": b, "qism": s, "muammo": q, "kind": kind, "olchov": m,
            "at": dt.datetime.now().isoformat(timespec="minutes")}


def _today():
    return dt.date.today().isoformat()


def limit(st, log=print):
    """Bugun KUNLIK_RAD ta video rad etilgan bo'lsa True (yangi video yasalmaydi)."""
    n = (st.d.get("rad_kun") or {}).get(_today(), 0)
    if n >= KUNLIK_RAD:
        if st.d.get("rad_limit_note") != _today():
            st.d["rad_limit_note"] = _today()
            st.save()
            msg = f"Rek-ball: bugun {n} ta video 85 balldan o'tmadi — ertagacha yangi video yasalmaydi."
            try:
                log(msg, notify=True)
            except TypeError:
                log(msg)
        return True
    return False


def filtr(st, pending, agent, log=print, kind=None):
    """Navbatdagi videolarni baholaydi; o'tganlarini qaytaradi, o'tmaganlarini rad etadi."""
    ok = []
    for ep in pending:
        f = Path(ep["file"])
        r = ep.get("rek")
        if not r or r.get("file") != f.name:
            try:
                r = baho(f, ep.get("title", ""), kind)
            except Exception as e:  # baholab bo'lmasa (ffmpeg yo'q va h.k.) — xavfsiz tomonga: yuklanmaydi
                log(f"Rek-ball: {f.name} baholanmadi: {str(e)[:200]}")
                continue
            r["file"] = f.name
            ep["rek"] = r
            st.save()
        if r["ball"] >= CHEGARA:
            log(f"Rek-ball: {r['ball']}/100 ✅ — {ep.get('title', '')}")
            ok.append(ep)
            continue
        rad = f.parent / "rad_etilgan"
        rad.mkdir(exist_ok=True)
        try:
            shutil.move(str(f), str(rad / f.name))
            js = f.with_suffix(".json")
            if js.exists():
                shutil.move(str(js), str(rad / js.name))
        except OSError:
            pass
        if ep in st.d["episodes"]:
            st.d["episodes"].remove(ep)
        st.d.setdefault("rad", []).append({k: ep.get(k) for k in ("n", "title", "file", "made", "rek")})
        st.d["rad"] = st.d["rad"][-60:]
        rk = st.d.setdefault("rad_kun", {})
        rk[_today()] = rk.get(_today(), 0) + 1
        for d in list(rk):
            if d < (dt.date.today() - dt.timedelta(days=7)).isoformat():
                rk.pop(d)
        st.save()
        log(f"Rek-ball: {r['ball']}/100 ❌ yuklanmadi — {ep.get('title', '')}. "
            f"Sabab: {'; '.join(r['muammo'][:3]) or 'umumiy ball past'}. Yangi video yasaladi.")
    return ok


if __name__ == "__main__":
    # python3 rek_ball.py VIDEO.mp4 "YouTube title" [short|long|ambient]
    if len(sys.argv) < 2:
        sys.exit('usage: rek_ball.py VIDEO.mp4 "title" [short|long|ambient]')
    r = baho(Path(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else Path(sys.argv[1]).stem,
             sys.argv[3] if len(sys.argv) > 3 else None)
    print(json.dumps(r, ensure_ascii=False))
    print(("OK" if r["ball"] >= CHEGARA else "RAD") + f" {r['ball']}/100", file=sys.stderr)

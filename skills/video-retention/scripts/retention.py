#!/usr/bin/env python3
"""Predict how a video will be watched: a per-second retention curve, average % viewed,
Shorts "stayed to watch" (did not swipe) and a recommend / not-recommend verdict with fixes.

This is a heuristic model, not YouTube data. It looks at what a viewer sees and hears every
second (motion, cuts, repeats, stillness, silence, loudness) and turns that into a drop-off risk.
Calibrate it against real Studio numbers with --calib (see SKILL.md).

Usage:
  python3 retention.py VIDEO [--kind short|long] [--title "..."] [--calib calib.json] [--json out.json] [--png curve.png]
"""
import argparse, json, math, os, re, subprocess, sys
import numpy as np

def run(cmd):
    return subprocess.run(cmd, capture_output=True)

def probe(path):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    d = json.loads(r.stdout or b"{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    return float(d["format"]["duration"]), int(v.get("width", 0)), int(v.get("height", 0)), a

def frames(path, fps=4, w=64, h=112):
    r = run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h},format=gray",
             "-f", "rawvideo", "-"])
    buf = np.frombuffer(r.stdout, np.uint8)
    n = len(buf) // (w * h)
    return buf[: n * w * h].reshape(n, h, w).astype(np.float32)

def loudness(path, dur):
    """RMS dB per second (mono 8 kHz)."""
    r = run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"])
    s = np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768
    secs = max(1, int(math.ceil(dur)))
    out = []
    for i in range(secs):
        c = s[i * 8000:(i + 1) * 8000]
        out.append(-90.0 if len(c) == 0 else 20 * math.log10(max(1e-5, float(np.sqrt((c ** 2).mean())))))
    return np.array(out)

def analyse(path, kind=None):
    dur, W, H, has_audio = probe(path)
    kind = kind or ("short" if H > W and dur <= 180 else "long")
    fps = 4 if dur <= 180 else 1
    F = frames(path, fps)
    n = len(F)
    diff = np.zeros(n)
    diff[1:] = np.abs(F[1:] - F[:-1]).mean(axis=(1, 2))           # motion / change
    cut = diff > 28                                                   # hard cut
    # repeats: frame close to one seen > 2 s earlier (centre crop, ignore captions)
    sig = F[:, int(F.shape[1] * .3): int(F.shape[1] * .9), :]
    sig = (sig - sig.mean(axis=(1, 2), keepdims=True))
    rep = np.zeros(n, bool)
    ccut = np.cumsum(cut)                       # a repeat needs a cut in between (else it's just a still shot)
    for i in range(n):
        lo = max(0, i - 600 * fps)
        hi = i - 2 * fps
        if hi > lo:
            dd = np.abs(sig[lo:hi] - sig[i]).mean(axis=(1, 2))
            ok = (dd < 20) & (ccut[i] - ccut[lo:hi] > 0)
            rep[i] = bool(ok.any())
    secs = int(math.ceil(dur))
    per = lambda arr, f: np.array([f(arr[s * fps:(s + 1) * fps]) if len(arr[s * fps:(s + 1) * fps]) else 0 for s in range(secs)])
    motion = per(diff, np.mean)
    cuts = per(cut, np.sum)
    reps = per(rep, np.mean)
    loud = loudness(path, dur) if has_audio else np.full(secs, -90.0)
    loud = np.resize(loud, secs)
    return dict(dur=dur, W=W, H=H, kind=kind, has_audio=has_audio, motion=motion, cuts=cuts,
                reps=reps, loud=loud, first_motion=float(diff[1:fps + 1].mean() if n > 1 else 0))

def model(m, title=None, calib=None):
    k = calib or {}
    secs = len(m["motion"])
    short = m["kind"] == "short"
    reasons = []
    # ---- the swipe decision (first ~2 s) ----
    swipe = 0.30 if short else 0.18                      # baseline early exit
    if m["first_motion"] < 2: swipe += .12; reasons.append("0:00 kadr deyarli qimirlamaydi (statik boshlanish)")
    if m["has_audio"] and m["loud"][0] < -40: swipe += .10; reasons.append("0:00 da ovoz/gap yo'q (sukut bilan boshlanadi)")
    if not m["has_audio"]: swipe += .15; reasons.append("videoda umuman ovoz yo'q")
    if secs > 3 and m["cuts"][:3].sum() == 0 and m["motion"][:3].mean() < 4: swipe += .06; reasons.append("birinchi 3 s da yangi narsa yo'q")
    if short and not (9 / 16 - .02 < m["W"] / max(1, m["H"]) < 9 / 16 + .02): swipe += .10; reasons.append("Short 9:16 emas")
    if title and len(title) > 60: swipe += .03; reasons.append("sarlavha 60 belgidan uzun")
    swipe = min(.85, max(.05, swipe * k.get("swipe_mult", 1.0)))
    # ---- second-by-second hazard after the hook ----
    base = (0.010 if short else 0.0035) * k.get("hazard_mult", 1.0)
    curve = [1.0]
    alive = 1 - swipe
    since_new = 0
    for s in range(secs):
        h = base
        new = m["cuts"][s] > 0 or m["motion"][s] > 10
        since_new = 0 if new else since_new + 1
        lim = 5 if short else 12
        if since_new > lim: h += (0.012 if short else 0.004) * (since_new - lim) ** .5
        if m["reps"][s] > .5: h += 0.035 if short else 0.010
        if m["has_audio"] and m["loud"][s] < -45 and s > 0: h += 0.02 if short else 0.006
        if m["motion"][s] < 1.0: h += 0.01 if short else 0.003
        if s == 0:
            curve.append(alive)
        else:
            alive *= (1 - min(.5, h))
            curve.append(alive)
    curve = np.array(curve[1:])
    # problems list with timestamps
    def ranges(mask):
        out, st = [], None
        for i, v in enumerate(list(mask) + [False]):
            if v and st is None: st = i
            if not v and st is not None:
                if i - st >= 2: out.append((st, i))
                st = None
        return out
    for a, b in ranges(m["reps"] > .5):
        reasons.append(f"{a//60}:{a%60:02d}-{b//60}:{b%60:02d} takroriy kadrlar (avval ko'rilgan footage)")
    still = ranges((m["motion"] < 1.0) & (m["cuts"] == 0))
    for a, b in still[:5]:
        if b - a >= (3 if short else 8): reasons.append(f"{a//60}:{a%60:02d}-{b//60}:{b%60:02d} deyarli qotib qolgan kadr")
    if m["has_audio"]:
        for a, b in ranges(m["loud"] < -45)[:5]:
            if a > 0: reasons.append(f"{a//60}:{a%60:02d}-{b//60}:{b%60:02d} sukut")
        mean_db = float(np.mean(m["loud"][m["loud"] > -60])) if (m["loud"] > -60).any() else -90
        if mean_db < -26: reasons.append(f"ovoz past (o'rtacha {mean_db:.0f} dB RMS) → loudnorm -14 LUFS")
    # summary numbers
    stayed = 1 - swipe                                 # Shorts "stayed to watch"
    avg_pct = float(curve.mean() * 100)                 # average % viewed (single pass)
    end_ret = float(curve[-1] * 100)
    loop_bonus = 0.0
    if short and m["dur"] <= 60 and end_ret > 45:
        loop_bonus = end_ret * 0.25                     # some viewers rewatch a short loop
    avg_pct_loop = avg_pct + loop_bonus
    if short:
        score = 0.5 * min(1, stayed / .85) + 0.5 * min(1, avg_pct_loop / 100)
        if stayed >= .70 and avg_pct_loop >= 85:
            verdict = "RECOMMEND CHIQISHI EHTIMOLI YUQORI"
        elif stayed >= .60 and avg_pct_loop >= 65:
            verdict = "O'RTA (sinov guruhidan nariga chiqishi qiyin)"
        elif stayed < .60:
            verdict = "RECOMMEND CHIQMAYDI (boshida ko'p swipe)"
        else:
            verdict = "RECOMMEND CHIQMAYDI (oxirigacha ko'rishmaydi)"
    else:
        score = 0.4 * min(1, stayed / .9) + 0.6 * min(1, avg_pct / 60)
        verdict = "TAVSIYAGA YAXSHI" if avg_pct >= 45 and curve[min(29, secs - 1)] >= .70 else \
                  "O'RTA" if avg_pct >= 30 else "ZAIF (boshida ko'p tark etiladi)"
    return dict(kind=m["kind"], duration_s=round(m["dur"], 1), resolution=f'{m["W"]}x{m["H"]}',
                stayed_to_watch_pct=round(stayed * 100), avg_viewed_pct=round(avg_pct),
                avg_viewed_pct_with_loops=round(avg_pct_loop) if short else None,
                retention_at={f"{t}s": round(float(curve[min(t, secs - 1)]) * 100) for t in
                              ([3, 5, 10, 15, 30, 45, 59] if short else [30, 60, 120, 240, 480, 600]) if t < secs},
                end_retention_pct=round(end_ret), score_0_100=round(score * 100), verdict=verdict,
                problems=reasons, curve=[round(float(x) * 100, 1) for x in curve])

def plot(res, png):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except ImportError:
        return
    c = res["curve"]
    plt.figure(figsize=(8, 3.2)); plt.plot(range(len(c)), c, lw=2, color="#d33")
    plt.ylim(0, 105); plt.grid(alpha=.3); plt.xlabel("soniya"); plt.ylabel("% hali ko'ryapti")
    plt.title(f'Bashorat: {res["avg_viewed_pct"]}% o\'rtacha, stayed {res["stayed_to_watch_pct"]}% — {res["verdict"]}', fontsize=9)
    plt.tight_layout(); plt.savefig(png, dpi=110)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("video"); p.add_argument("--kind", choices=["short", "long"])
    p.add_argument("--title"); p.add_argument("--calib"); p.add_argument("--json"); p.add_argument("--png")
    a = p.parse_args()
    calib = json.load(open(a.calib)) if a.calib and os.path.exists(a.calib) else None
    res = model(analyse(a.video, a.kind), a.title, calib)
    if a.json: json.dump(res, open(a.json, "w"), indent=1)
    if a.png: plot(res, a.png)
    out = dict(res); out["curve"] = f'{len(res["curve"])} points (see --json/--png)'
    print(json.dumps(out, indent=1, ensure_ascii=False))

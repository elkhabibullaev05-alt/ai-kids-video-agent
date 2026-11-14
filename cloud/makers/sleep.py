#!/usr/bin/env python3
"""Calm Rain for Sleep — maker.

2026-11-14 owner (hub): the old visuals (Commons clips: weather/satellite maps, a "1984" space photo, a sunny field,
a PixVerse watermark, text-only "RAIN 2H") did not match rain sounds — replace them completely.
New rules (owner's words, summarised):
  1) every video = ONE cozy scene that matches its title 100%: rain on a window at night with a lamp, a cabin in a
     forest, a 1990s village on a rainy night (rain on the roofs), a lake house, a room with tea and a cat.
     Warm hand-drawn / anime-like look — no brand or studio names anywhere.
  2) the scene MOVES: falling rain layers, drops running down the glass, lamp/candle flicker, very slow camera push;
     a 40 s seamless loop stretched to 1–3 h.
  3) the sound matches the scene (window → rain on glass, roof → rain on a roof, forest → rain on leaves).
  4) banned: maps, satellite/space photos, sunny or dry pictures, any watermark/logo, text-only backgrounds.
     Pictures are made by us (here: drawn procedurally by this script — no stock, no third-party watermark possible).
  5) thumbnail = the same scene + big soft text ("3 HOURS" / "Cozy Rainy Night"), warm colours, high contrast.
  6) titles = scene + benefit + length, e.g. "Cozy Rainy Night in a 1990s Village 🌧️ Rain Sounds for Deep Sleep | 3 Hours".
  7) before a video is handed to the uploader one frame is checked (rain visible/moving, not too dark/bright, scene
     matches the title); if the check fails nothing is made.
Rain SOUND is still a real recording from Wikimedia Commons (free licence, credited in the description).
See cloud/makers/README.md for the contract.  --offline-test makes a synthetic sound to test the pipeline.
"""
import argparse, json, math, os, random, re, subprocess, time, urllib.parse, urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True); ap.add_argument("--home", required=True); ap.add_argument("--repo", default=".")
ap.add_argument("--titles", default=""); ap.add_argument("--need-long", type=int, default=1); ap.add_argument("--need-short", type=int, default=1)
ap.add_argument("--hours", type=float, default=0); ap.add_argument("--offline-test", action="store_true")
ap.add_argument("--scene", default="", help="force a scene key (testing)")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
CACHE = os.path.join(a.home, "rain_cache"); os.makedirs(CACHE, exist_ok=True)
USED_F = os.path.join(a.home, "used_rain.json")
used = json.load(open(USED_F)) if os.path.exists(USED_F) else {}
for k in ("video", "audio", "titles", "scenes"):
    used.setdefault(k, [])
titles = set(json.load(open(a.titles))) if a.titles and os.path.exists(a.titles) else set()
UA = {"User-Agent": "CalmRainForSleep/1.0 (owner's own YouTube channel tool; contact via channel)"}
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[1-4]\.0|cc by(-sa)?|cc-by(-sa)?-[1-4]\.0)", re.I)
FPS, LOOP = 30, 40.0          # 40 s seamless loop (owner: 20–60 s)
NF = int(FPS * LOOP)


def font(size):
    for f in [os.path.join(a.home, "fonts", "Fredoka-Bold.ttf"), os.path.expanduser("~/.fonts/Fredoka-Bold.ttf"),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def get_soft_font():
    """Fredoka (OFL, Google Fonts) — big rounded 'soft' thumbnail text; DejaVu Bold if the download fails."""
    d = os.path.join(a.home, "fonts"); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "Fredoka-Bold.ttf")
    if not os.path.exists(f) and not a.offline_test:
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf"
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                open(f + ".part", "wb").write(r.read())
            os.replace(f + ".part", f)
        except Exception as e:
            print("font download failed (DejaVu used):", str(e)[:120], flush=True)


def sh(*cmd, timeout=7200):
    p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-800:]}")
    return p.stdout


# ------------------------------------------------------------------ rain SOUND (real recordings, Wikimedia Commons)
def api(**q):
    q.update(format="json")
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
        except Exception:
            time.sleep(5 * (i + 1))
    raise RuntimeError("Commons API unreachable")


def audio_files(queries):
    out = []
    for c in ["Category:Sounds of rain", "Category:Audio files of rain"]:
        try:
            r = api(action="query", list="categorymembers", cmtitle=c, cmtype="file", cmlimit=200)
            out += [m["title"] for m in r["query"]["categorymembers"]]
        except Exception:
            pass
    for q in queries + ["rain", "rain sound", "rainfall"]:
        try:
            r = api(action="query", list="search", srnamespace=6, srsearch=f"{q} filetype:audio", srlimit=50)
            out += [m["title"] for m in r["query"]["search"]]
        except Exception:
            pass
    bad = ("game", "trailer", "episode", "music", "song", "remix", "speech", "voice", "radio", "train")
    seen, res = set(), []
    for t in out:
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
        yield dict(title=p["title"], url=ii.get("url"), lic=lic, artist=art, dur=ii.get("duration") or 0)


def pick_audio(prefer, queries):
    """Rain recording that matches the scene: titles containing a `prefer` word first (window / roof / leaves …)."""
    allc = audio_files(queries)
    fresh = [t for t in allc if t not in used["audio"]] or allc  # pool used up → reuse is fine for sound
    good = [t for t in fresh if any(p in t.lower() for p in prefer)]
    rest = [t for t in fresh if t not in good]
    random.shuffle(good); random.shuffle(rest)
    cands = good + rest
    for i in range(0, len(cands), 40):
        for f in sorted(info(cands[i:i + 40]), key=lambda f: cands.index(f["title"]) if f["title"] in cands else 9999):
            if not f["url"] or not FREE.match(f["lic"].strip()) or (f["dur"] and f["dur"] < 20):
                continue
            dst = os.path.join(CACHE, re.sub(r"[^\w.-]", "_", f["title"].split(":", 1)[1]))
            try:
                if not os.path.exists(dst):
                    with urllib.request.urlopen(urllib.request.Request(f["url"], headers=UA), timeout=300) as r, \
                            open(dst + ".part", "wb") as o:
                        o.write(r.read())
                    os.replace(dst + ".part", dst)
                sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst, timeout=120)
            except Exception as e:
                print("skip broken file:", f["title"], str(e)[:200], flush=True)
                for x in (dst, dst + ".part"):
                    try:
                        os.remove(x)
                    except OSError:
                        pass
                used["audio"].append(f["title"])
                continue
            f["path"] = dst
            return f
    raise RuntimeError("no free-licence rain audio found on Commons")


# ------------------------------------------------------------------ painted scenes (drawn here, warm hand-drawn look)
def hexc(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def jitter(c, rng, d=10):
    return tuple(int(max(0, min(255, v + rng.integers(-d, d + 1)))) for v in c)


class Canvas:
    """Relative coordinates: x in 0..1 of width, y in 0..1 of height (16:9 scene)."""

    def __init__(self, W, H, rng):
        self.W, self.H, self.rng = W, H, rng
        self.base = Image.new("RGB", (W, H)); self.glow = Image.new("RGB", (W, H)); self.glass = Image.new("L", (W, H))
        self.d, self.g, self.m = ImageDraw.Draw(self.base), ImageDraw.Draw(self.glow), ImageDraw.Draw(self.glass)

    def P(self, pts):
        return [(x * self.W, y * self.H) for x, y in pts]

    def R(self, x0, y0, x1, y1):
        return [x0 * self.W, y0 * self.H, x1 * self.W, y1 * self.H]

    def grad(self, x0, y0, x1, y1, top, bottom):
        bx = self.R(x0, y0, x1, y1); w, h = int(bx[2] - bx[0]), int(bx[3] - bx[1])
        t = np.linspace(0, 1, max(h, 1))[:, None, None]
        arr = (np.array(top)[None, None] * (1 - t) + np.array(bottom)[None, None] * t).repeat(max(w, 1), 1)
        self.base.paste(Image.fromarray(arr.astype(np.uint8)), (int(bx[0]), int(bx[1])))

    def lamp(self, x, y, r, color, strength=1.0):
        """Warm light: a soft blob on the glow layer (flickers in the animation)."""
        c = tuple(int(v * strength) for v in color)
        self.g.ellipse(self.R(x - r, y - r * 16 / 9, x + r, y + r * 16 / 9), fill=c)

    def finish(self):
        s = self.W / 1920
        glow = self.glow.filter(ImageFilter.GaussianBlur(60 * s))
        base = self.base.filter(ImageFilter.GaussianBlur(1.2 * s))
        b = np.asarray(base).astype(np.float32)
        b += self.rng.normal(0, 3.0, b.shape[:2])[..., None]  # paper grain → hand-painted feel
        return b, np.asarray(glow).astype(np.float32), np.asarray(self.glass.filter(ImageFilter.GaussianBlur(1.5 * s))).astype(np.float32) / 255


def silhouette(cv, color, y_base, amp, n, seed_off=0.0):
    pts = [(0, 1.0)]
    for i in range(n + 1):
        x = i / n
        y = y_base - amp * (0.5 + 0.5 * math.sin(x * 7.3 + seed_off) * math.sin(x * 2.1 + seed_off * 2))
        pts.append((x, y))
    pts.append((1, 1.0)); cv.d.polygon(cv.P(pts), fill=color)


def pine(cv, x, y, h, color):
    w = h * 0.22
    for k in range(4):
        top = y - h + k * h * 0.2
        cv.d.polygon(cv.P([(x, top), (x - w * (0.5 + k * 0.17), top + h * 0.38), (x + w * (0.5 + k * 0.17), top + h * 0.38)]), fill=color)
    cv.d.rectangle(cv.R(x - w * 0.06, y - h * 0.1, x + w * 0.06, y), fill=color)


def house(cv, x, y, w, h, wall, roof, lit, tiles=False, rng=None):
    cv.d.rectangle(cv.R(x, y - h, x + w, y), fill=wall)
    cv.d.polygon(cv.P([(x - w * 0.08, y - h), (x + w / 2, y - h - h * 0.55), (x + w * 1.08, y - h)]), fill=roof)
    if tiles:
        for k in range(1, 5):
            f = k / 5; yy = y - h - h * 0.55 * (1 - f)
            cv.d.line(cv.P([(x + w / 2 - (w * 0.58) * f, yy), (x + w / 2 + (w * 0.58) * f, yy)]),
                      fill=tuple(max(0, c - 18) for c in roof), width=max(1, int(cv.W / 900)))
    nw = 2 if w > 0.06 else 1
    for i in range(nw):
        wx = x + w * (0.2 + i * 0.4); wy = y - h * 0.68
        on = lit and (rng is None or rng.random() < 0.8)
        cv.d.rectangle(cv.R(wx, wy, wx + w * 0.22, wy + h * 0.3), fill=hexc("#ffcf86") if on else hexc("#1b2230"))
        if on:
            cv.lamp(wx + w * 0.11, wy + h * 0.15, w * 0.25, hexc("#ff9d4a"), 0.3)


def scene_window(cv, room=False):
    rng = cv.rng
    cv.grad(0, 0, 1, 1, jitter(hexc("#2d1f1b"), rng), jitter(hexc("#1c1412"), rng))  # warm dark wall
    wx0, wy0, wx1, wy1 = (0.30, 0.08, 0.86, 0.66) if room else (0.20, 0.08, 0.80, 0.70)
    # outside: night town under rain
    cv.grad(wx0, wy0, wx1, wy1, jitter(hexc("#16263a"), rng), jitter(hexc("#2b3f57"), rng))
    for i in range(5):
        cx = wx0 + (wx1 - wx0) * rng.random(); cy = wy0 + (wy1 - wy0) * 0.25 * rng.random()
        cv.d.ellipse(cv.R(cx - 0.08, cy - 0.03, cx + 0.08, cy + 0.04), fill=jitter(hexc("#2e4259"), rng, 6))
    x = wx0
    while x < wx1:
        w = 0.04 + 0.04 * rng.random(); h = 0.08 + 0.12 * rng.random()
        house(cv, x, wy1, w, h, jitter(hexc("#1c2838"), rng, 5), jitter(hexc("#141d29"), rng, 5), True, rng=rng)
        x += w * (1.1 + 0.4 * rng.random())
    cv.m.rectangle(cv.R(wx0, wy0, wx1, wy1), fill=255)  # glass
    # wooden frame + mullions
    fr = jitter(hexc("#6a442b"), rng); t = 0.016
    for bx in [(wx0 - t, wy0 - t, wx1 + t, wy0), (wx0 - t, wy1, wx1 + t, wy1 + t), (wx0 - t, wy0, wx0, wy1), (wx1, wy0, wx1 + t, wy1),
               ((wx0 + wx1) / 2 - t / 2, wy0, (wx0 + wx1) / 2 + t / 2, wy1), (wx0, (wy0 + wy1) * 0.47 - t * 0.9, wx1, (wy0 + wy1) * 0.47 + t * 0.9)]:
        cv.d.rectangle(cv.R(*bx), fill=fr); cv.m.rectangle(cv.R(*bx), fill=0)
    # sill
    cv.d.rectangle(cv.R(wx0 - 0.04, wy1 + t, wx1 + 0.04, wy1 + t + 0.045), fill=jitter(hexc("#7a5034"), rng))
    sy = wy1 + t
    # candle + mug + plant on the sill
    cx = wx0 + 0.07
    cv.d.rectangle(cv.R(cx, sy - 0.07, cx + 0.018, sy), fill=hexc("#efe2c4"))
    cv.d.ellipse(cv.R(cx + 0.004, sy - 0.095, cx + 0.014, sy - 0.07), fill=hexc("#ffd27a"))
    cv.lamp(cx + 0.009, sy - 0.085, 0.045, hexc("#ff9a3c"), 0.8)
    mx = wx1 - 0.14
    cv.d.rounded_rectangle(cv.R(mx, sy - 0.06, mx + 0.035, sy), radius=int(cv.W * 0.004), fill=jitter(hexc("#c46a45"), rng))
    cv.d.arc(cv.R(mx + 0.03, sy - 0.05, mx + 0.05, sy - 0.015), -90, 90, fill=hexc("#c46a45"), width=int(cv.W / 300))
    px = wx1 - 0.07
    cv.d.polygon(cv.P([(px, sy - 0.05), (px + 0.04, sy - 0.05), (px + 0.034, sy), (px + 0.006, sy)]), fill=hexc("#a4553a"))
    for k in range(6):
        ang = -2.6 + k * 0.45
        lx, ly = px + 0.02 + 0.035 * math.cos(ang), sy - 0.05 + 0.06 * math.sin(ang)
        cv.d.ellipse(cv.R(min(px + 0.02, lx) - 0.008, min(sy - 0.05, ly) - 0.01, max(px + 0.02, lx) + 0.008, max(sy - 0.05, ly) + 0.01),
                     fill=jitter(hexc("#3f6b45"), rng))
    # lamp on the wall side
    lx = 0.08 if not room else 0.12
    cv.d.rectangle(cv.R(lx - 0.003, 0.32, lx + 0.003, 0.78), fill=hexc("#3a2a22"))
    cv.d.polygon(cv.P([(lx - 0.045, 0.32), (lx + 0.045, 0.32), (lx + 0.03, 0.22), (lx - 0.03, 0.22)]), fill=hexc("#e9a95e"))
    cv.lamp(lx, 0.29, 0.10, hexc("#ff9f50"), 0.55)
    cv.lamp((wx0 + wx1) / 2, wy1 + 0.04, 0.18, hexc("#7a3d1a"), 0.35)
    if room:
        # table with tea in front, a cat sleeping on a cushion on the sill
        cv.grad(0, 0.80, 1, 1, jitter(hexc("#5c3a26"), rng), jitter(hexc("#3d2619"), rng))
        cv.d.rectangle(cv.R(0, 0.80, 1, 0.815), fill=hexc("#6e4630"))
        tx = 0.52
        cv.d.ellipse(cv.R(tx - 0.07, 0.70, tx + 0.07, 0.81), fill=hexc("#b9a27e"))          # teapot
        cv.d.ellipse(cv.R(tx - 0.012, 0.685, tx + 0.012, 0.705), fill=hexc("#c4ae8c"))
        cv.d.polygon(cv.P([(tx + 0.06, 0.75), (tx + 0.11, 0.71), (tx + 0.115, 0.72), (tx + 0.07, 0.775)]), fill=hexc("#b9a27e"))
        cv.d.rounded_rectangle(cv.R(tx + 0.15, 0.75, tx + 0.19, 0.81), radius=int(cv.W * 0.004), fill=hexc("#f1ead9"))  # cup
        cv.d.ellipse(cv.R(tx + 0.15, 0.745, tx + 0.19, 0.76), fill=hexc("#8a4b22"))
        cv.lamp(tx + 0.05, 0.76, 0.12, hexc("#ff9a4c"), 0.25)
        cat = jitter(hexc("#3a2f2d"), rng, 6); cx0, cy0 = (wx0 + wx1) / 2 + 0.04, sy
        cv.d.ellipse(cv.R(cx0 - 0.12, sy - 0.02, cx0 + 0.12, sy + 0.01), fill=hexc("#9b3f3a"))  # cushion
        cv.d.ellipse(cv.R(cx0 - 0.08, cy0 - 0.075, cx0 + 0.06, cy0 - 0.005), fill=cat)         # body
        cv.d.ellipse(cv.R(cx0 + 0.03, cy0 - 0.07, cx0 + 0.085, cy0 - 0.015), fill=cat)          # head
        cv.d.polygon(cv.P([(cx0 + 0.037, cy0 - 0.06), (cx0 + 0.045, cy0 - 0.092), (cx0 + 0.06, cy0 - 0.065)]), fill=cat)
        cv.d.polygon(cv.P([(cx0 + 0.062, cy0 - 0.066), (cx0 + 0.078, cy0 - 0.09), (cx0 + 0.083, cy0 - 0.055)]), fill=cat)
        cv.d.arc(cv.R(cx0 - 0.11, cy0 - 0.05, cx0 + 0.0, cy0 + 0.015), 90, 250, fill=cat, width=int(cv.W / 160))  # tail
        cv.d.line(cv.P([(cx0 + 0.048, cy0 - 0.042), (cx0 + 0.058, cy0 - 0.04)]), fill=hexc("#1c1616"), width=max(1, int(cv.W / 900)))
        cv.d.line(cv.P([(cx0 + 0.066, cy0 - 0.04), (cx0 + 0.076, cy0 - 0.042)]), fill=hexc("#1c1616"), width=max(1, int(cv.W / 900)))
    else:
        cv.grad(0, wy1 + t + 0.045, 1, 1, jitter(hexc("#2a1c17"), rng), jitter(hexc("#160f0d"), rng))
    return dict(ground=None)


def scene_cabin(cv):
    rng = cv.rng
    cv.grad(0, 0, 1, 1, jitter(hexc("#0f1a27"), rng), jitter(hexc("#22343f"), rng))
    for depth, col in enumerate(["#22384a", "#1a2c37", "#12212a"]):
        n = 18 - depth * 4
        for i in range(n):
            x = (i + rng.random()) / n; h = 0.25 + 0.15 * depth + 0.1 * rng.random()
            pine(cv, x, 0.62 + depth * 0.07, h, jitter(hexc(col), rng, 4))
    cv.grad(0, 0.78, 1, 1, jitter(hexc("#142019"), rng), jitter(hexc("#0b1210"), rng))
    cx, cy, w, h = 0.36 + 0.1 * rng.random(), 0.80, 0.24, 0.16
    cv.d.rectangle(cv.R(cx, cy - h, cx + w, cy), fill=jitter(hexc("#5a3b29"), rng))
    for k in range(1, 6):
        cv.d.line(cv.P([(cx, cy - h * k / 6), (cx + w, cy - h * k / 6)]), fill=hexc("#47301f"), width=max(1, int(cv.W / 700)))
    cv.d.polygon(cv.P([(cx - 0.025, cy - h), (cx + w / 2, cy - h - 0.13), (cx + w + 0.025, cy - h)]), fill=jitter(hexc("#2f201a"), rng))
    cv.d.rectangle(cv.R(cx + w * 0.72, cy - h - 0.12, cx + w * 0.8, cy - h - 0.04), fill=hexc("#3b2c26"))
    for wx in (cx + w * 0.12, cx + w * 0.62):
        cv.d.rectangle(cv.R(wx, cy - h * 0.72, wx + w * 0.22, cy - h * 0.3), fill=hexc("#ffcd80"))
        cv.d.line(cv.P([(wx + w * 0.11, cy - h * 0.72), (wx + w * 0.11, cy - h * 0.3)]), fill=hexc("#5a3b29"), width=max(1, int(cv.W / 500)))
        cv.lamp(wx + w * 0.11, cy - h * 0.5, 0.05, hexc("#ff9a40"), 0.75)
    cv.d.rectangle(cv.R(cx + w * 0.4, cy - h * 0.6, cx + w * 0.55, cy), fill=hexc("#2b1b13"))
    cv.d.polygon(cv.P([(cx + w * 0.1, cy), (cx + w * 0.9, cy), (cx + w * 1.3, 1.0), (cx - w * 0.3, 1.0)]), fill=hexc("#2a2a22"))
    cv.lamp(cx + w * 0.5, cy + 0.05, 0.12, hexc("#7a4a20"), 0.45)
    for i in range(6):  # foreground trees, very dark
        x = rng.choice([rng.random() * 0.25, 0.75 + rng.random() * 0.25])
        pine(cv, x, 1.02, 0.7 + 0.2 * rng.random(), hexc("#08100f"))
    return dict(ground=0.80)


def scene_village(cv):
    rng = cv.rng
    cv.grad(0, 0, 1, 1, jitter(hexc("#121c2e"), rng), jitter(hexc("#2c3549"), rng))
    silhouette(cv, hexc("#1a2434"), 0.50, 0.12, 40, rng.random() * 6)
    x = -0.02
    while x < 1.0:  # back row
        w = 0.06 + 0.04 * rng.random(); house(cv, x, 0.66, w, 0.08 + 0.05 * rng.random(), hexc("#1f2a3a"), hexc("#172030"), True, rng=rng)
        x += w * 1.15
    x = -0.03
    while x < 1.0:  # front row, tiled roofs
        w = 0.11 + 0.06 * rng.random()
        house(cv, x, 0.82, w, 0.13 + 0.05 * rng.random(), jitter(hexc("#3a3b44"), rng, 8), jitter(hexc("#2a3442"), rng, 8), True, tiles=True, rng=rng)
        x += w * 1.12
    for px in (0.18, 0.55, 0.9):  # utility poles + sagging wires (1990s countryside)
        cv.d.rectangle(cv.R(px - 0.003, 0.32, px + 0.003, 0.86), fill=hexc("#141a22"))
        cv.d.rectangle(cv.R(px - 0.02, 0.35, px + 0.02, 0.356), fill=hexc("#141a22"))
    for k, yy in enumerate((0.352, 0.36)):
        pts = []
        for i in range(61):
            xx = i / 60
            pts.append((xx, yy + 0.035 * math.sin(math.pi * ((xx * 2.7) % 1))))
        cv.d.line(cv.P(pts), fill=hexc("#0f141b"), width=max(1, int(cv.W / 1200)))
    cv.grad(0, 0.82, 1, 1, jitter(hexc("#232a36"), rng), jitter(hexc("#151a22"), rng))  # wet road
    lx = 0.4 + 0.2 * rng.random()  # street lamp
    cv.d.rectangle(cv.R(lx - 0.002, 0.5, lx + 0.002, 0.84), fill=hexc("#10141b"))
    cv.d.ellipse(cv.R(lx - 0.012, 0.49, lx + 0.012, 0.515), fill=hexc("#ffe3a8"))
    cv.lamp(lx, 0.5, 0.05, hexc("#ffb15a"), 0.85)
    cv.lamp(lx, 0.9, 0.03, hexc("#ff9f45"), 0.5)  # reflection on the wet road
    cv.g.rectangle(cv.R(lx - 0.006, 0.84, lx + 0.006, 1.0), fill=hexc("#7a5528"))
    return dict(ground=0.84)


def scene_lake(cv):
    rng = cv.rng
    cv.grad(0, 0, 1, 0.6, jitter(hexc("#111c2c"), rng), jitter(hexc("#2b3b4f"), rng))
    silhouette(cv, hexc("#1c2838"), 0.40, 0.15, 30, rng.random() * 6)
    silhouette(cv, hexc("#152030"), 0.50, 0.08, 30, rng.random() * 6)
    for i in range(14):
        pine(cv, rng.random(), 0.6, 0.1 + 0.06 * rng.random(), hexc("#0f1922"))
    hx, w, h = 0.16 + 0.1 * rng.random(), 0.16, 0.12
    cv.d.rectangle(cv.R(hx, 0.6 - h, hx + w, 0.6), fill=jitter(hexc("#5b4033"), rng))
    cv.d.polygon(cv.P([(hx - 0.02, 0.6 - h), (hx + w / 2, 0.6 - h - 0.09), (hx + w + 0.02, 0.6 - h)]), fill=hexc("#2c1f1b"))
    for wx in (hx + 0.025, hx + 0.1):
        cv.d.rectangle(cv.R(wx, 0.6 - h * 0.7, wx + 0.035, 0.6 - h * 0.3), fill=hexc("#ffcf86"))
        cv.lamp(wx + 0.017, 0.6 - h * 0.5, 0.04, hexc("#ff9a40"), 0.7)
    cv.d.rectangle(cv.R(hx + w, 0.595, hx + w + 0.14, 0.605), fill=hexc("#3b2a20"))  # dock
    # lake = darkened mirror of the upper picture
    top = cv.base.crop(tuple(int(v) for v in cv.R(0, 0.2, 1, 0.6))).transpose(Image.FLIP_TOP_BOTTOM)
    top = Image.eval(top, lambda v: int(v * 0.55))
    cv.base.paste(top.resize((cv.W, int(cv.H * 0.4))), (0, int(cv.H * 0.6)))
    for i in range(60):
        y = 0.62 + 0.38 * rng.random(); x = rng.random()
        cv.d.line(cv.P([(x, y), (x + 0.03 + 0.05 * rng.random(), y)]), fill=hexc("#2e3e52"), width=max(1, int(cv.W / 900)))
    for wx in (hx + 0.042, hx + 0.117):
        cv.g.rectangle(cv.R(wx - 0.008, 0.61, wx + 0.008, 0.85), fill=hexc("#6a4420"))
    return dict(ground=0.62)


SCENES = {
    "window": dict(paint=lambda cv: scene_window(cv), name="Cozy Rainy Night by the Window", short="Rain on the Window",
                   sound="Rain on Window Sounds for Deep Sleep", prefer=["window", "glass"], q=["rain on window", "rain window"],
                   badge="RAINY WINDOW"),
    "cabin": dict(paint=scene_cabin, name="Cozy Cabin in a Rainy Forest", short="Rainy Forest Cabin",
                  sound="Rain on Leaves Sounds for Deep Sleep", prefer=["forest", "leaves", "leaf", "tree", "wood"],
                  q=["rain forest", "rain leaves", "rain trees"], badge="FOREST CABIN"),
    "village": dict(paint=scene_village, name="Cozy Rainy Night in a 1990s Village", short="Rainy 1990s Village",
                    sound="Rain on the Roof for Deep Sleep", prefer=["roof", "tin", "gutter", "village"],
                    q=["rain on roof", "rain roof"], badge="1990s VILLAGE"),
    "lake": dict(paint=scene_lake, name="Rainy Night at a Quiet Lake House", short="Rainy Lake House",
                 sound="Rain on the Lake Sounds for Deep Sleep", prefer=["lake", "pond", "water", "river"],
                 q=["rain lake", "rain on water", "rain pond"], badge="LAKE HOUSE"),
    "room": dict(paint=lambda cv: scene_window(cv, room=True), name="Cozy Rainy Night with Tea and a Sleeping Cat",
                 short="Tea, Cat and Rain", sound="Rain on Window for Deep Sleep", prefer=["window", "glass"],
                 q=["rain on window", "rain window"], badge="TEA & RAIN"),
}


def paint(key, W, H, seed):
    cv = Canvas(W, H, np.random.default_rng(seed))
    meta = SCENES[key]["paint"](cv)
    base, glow, glass = cv.finish()
    meta.update(interior=key in ("window", "room"))
    return base, glow, glass, meta


# ------------------------------------------------------------------ animation: 40 s seamless loop
def make_unit(key, seed, W, H, path, crop_w=None):
    """Render the moving scene. Every motion has a whole number of cycles in LOOP seconds → frame NF == frame 0."""
    PW = int(H * 16 / 9) if crop_w else W
    base, glow, glass, meta = paint(key, PW, H, seed)
    if crop_w:  # vertical Short: middle slice of a wider painting (no stretching)
        x0 = (PW - crop_w) // 2
        base, glow, glass = base[:, x0:x0 + crop_w], glow[:, x0:x0 + crop_w], glass[:, x0:x0 + crop_w]
        W = crop_w
    rng = np.random.default_rng(seed + 1)
    s = H / 1080
    layers = []  # (x0, y0, k cycles, length, slope, width, alpha)
    for n, kmin, kmax, ln, wd, al in ((420, 16, 22, 26, 1, 0.22), (260, 26, 34, 48, 2, 0.35), (60, 38, 46, 80, 3, 0.45)):
        for _ in range(int(n * W / 1920)):
            layers.append((rng.random() * W * 1.2 - W * 0.1, rng.random(), rng.integers(kmin, kmax), ln * s, 0.12, max(1, int(wd * s)), al))
    drops = [(rng.random() * W, rng.random(), int(rng.integers(1, 4)), (3 + 4 * rng.random()) * s) for _ in range(int(70 * W / 1920))] \
        if meta["interior"] else []
    splashes = [(rng.random() * W, meta["ground"] * H + rng.random() * (H - meta["ground"] * H), rng.random(), int(rng.integers(20, 40)))
                for _ in range(int(90 * W / 1920))] if meta.get("ground") else []
    rain_mask = glass if meta["interior"] else np.ones((H, W), np.float32)
    rc = np.array([205, 218, 236], np.float32)
    span = H * 1.15
    proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "1800k", "-bufsize", "4M",
                             "-pix_fmt", "yuv420p", "-g", "60", path],  # ~2.4 GB for 3 h
                            stdin=subprocess.PIPE)
    for f in range(NF):
        t = f / NF  # 0..1 of the loop
        flick = 1 + 0.07 * math.sin(2 * math.pi * 3 * t) + 0.05 * math.sin(2 * math.pi * 11 * t + 1.3) + 0.03 * math.sin(2 * math.pi * 29 * t + 0.4)
        fr = base + glow * flick
        rl = Image.new("L", (W, H)); d = ImageDraw.Draw(rl)
        for x0, y0, k, ln, sl, wd, al in layers:
            y = ((y0 + k * t) % 1) * span - ln
            x = x0 + sl * y
            d.line([(x, y), (x + sl * ln, y + ln)], fill=int(255 * al), width=wd)
        for x, y, ph, k in splashes:
            age = (ph + k * t) % 1 * (LOOP / k)  # seconds since this splash started
            if age < 0.45:
                r = (4 + 28 * age) * s; a_ = int(160 * (1 - age / 0.45))
                d.ellipse([x - r, y - r * 0.3, x + r, y + r * 0.3], outline=a_, width=max(1, int(s)))
        r_arr = np.asarray(rl).astype(np.float32) / 255 * rain_mask
        fr = fr * (1 - 0.25 * r_arr[..., None]) + rc * r_arr[..., None] * 0.9
        if drops:
            dl = Image.new("L", (W, H)); dd = ImageDraw.Draw(dl); hl = Image.new("L", (W, H)); hd = ImageDraw.Draw(hl)
            for x, y0, k, r in drops:
                y = ((y0 + k * t) % 1) * H
                dd.ellipse([x - r, y - r * 1.3, x + r, y + r * 1.3], fill=150)
                dd.line([(x, y - r * 6), (x, y)], fill=60, width=max(1, int(r * 0.6)))
                hd.ellipse([x - r * 0.45, y - r * 0.9, x + r * 0.1, y - r * 0.2], fill=230)
            dk = np.asarray(dl).astype(np.float32) / 255 * glass; li = np.asarray(hl).astype(np.float32) / 255 * glass
            fr = fr * (1 - 0.35 * dk[..., None]) + np.array([240, 230, 210], np.float32) * li[..., None] * 0.7
        z = 1 + 0.05 * (1 - math.cos(2 * math.pi * t)) / 2  # very slow push in and back
        img = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
        cw, ch = W / z, H / z; cx, cy = W / 2, max(ch / 2, min(H - ch / 2, H * 0.48))  # never crop outside → no black band
        img = img.crop((cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).resize((W, H), Image.BILINEAR)
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg (unit) failed")


def check_unit(path, key):
    """Owner rule 7: look at one frame before anything is uploaded — rain must be visible and moving, the picture not
    black/blown out. Watermarks and maps cannot appear (scene is drawn here); the title comes from the same scene key."""
    fr = []
    for ss in ("5.0", "5.2"):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", ss, "-i", path, "-frames:v", "1", "-vf", "scale=480:-2",
                              "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        fr.append(np.frombuffer(raw, np.uint8).astype(np.float32))
    if len(fr[0]) == 0 or len(fr[0]) != len(fr[1]):
        raise RuntimeError("frame check: could not read frames")
    bright, motion = fr[0].mean(), np.abs(fr[0] - fr[1]).mean()
    print(f"frame check {key}: brightness {bright:.1f}, rain motion {motion:.2f}", flush=True)
    if not (18 <= bright <= 170) or motion < 0.25:
        raise RuntimeError(f"frame check failed ({key}): brightness {bright:.1f}, motion {motion:.2f} — not uploaded")


def offline_audio(d):
    au = os.path.join(d, "test_rain.wav")
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anoisesrc=d=60:c=pink:a=0.5", "-af", "lowpass=f=5000,highpass=f=200", au)
    return dict(path=au, title="File:Test rain.ogg", artist="test", lic="CC0", dur=60)


def main():
    tmp = os.path.join(a.home, "sleep_work"); os.makedirs(tmp, exist_ok=True)
    get_soft_font()
    recent = used["scenes"][-3:]
    key = a.scene or next((k for k in random.sample(list(SCENES), len(SCENES)) if k not in recent), random.choice(list(SCENES)))
    sc = SCENES[key]; seed = int(time.time()) % 100000
    aud = offline_audio(tmp) if a.offline_test else pick_audio(sc["prefer"], sc["q"])
    stamp = time.strftime("%Y%m%d-%H%M")
    # 1) real rain sound unit: loop with a 3 s crossfade, gentle EQ, -20 LUFS (sleep content is quieter on purpose)
    au_len = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", aud["path"]).strip() or 60)
    aunit = os.path.join(tmp, "aunit.m4a")
    AL = max(15.0, min(120.0, au_len - 1))
    sh("ffmpeg", "-y", "-v", "error", "-i", aud["path"], "-i", aud["path"], "-filter_complex",
       f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=3:{AL},asetpts=PTS-STARTPTS[body];"
       f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:3,asetpts=PTS-STARTPTS[head];"
       f"[body][head]acrossfade=d=3:c1=tri:c2=tri,highpass=f=60,lowpass=f=12000,loudnorm=I=-20:TP=-2:LRA=7[o]",
       "-map", "[o]", "-c:a", "aac", "-b:a", "128k", aunit)
    credit = (f"Scene: illustrated and animated by Calm Rain for Sleep.\n"
              f"Rain sound: \"{aud['title'].split(':', 1)[1]}\" by {aud['artist']} ({aud['lic']}), Wikimedia Commons.")
    made = 0
    if a.need_long:
        unit = os.path.join(tmp, "unit.mp4")
        make_unit(key, seed, 1920, 1080, unit)
        check_unit(unit, key)
        hours = a.hours or random.choice([2, 3, 3])
        secs = 60 if a.offline_test else int(hours * 3600)
        long_f = os.path.join(a.out, f"{stamp}-0-long.mp4")
        sh("ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", unit, "-stream_loop", "-1", "-i", aunit, "-t", str(secs),
           "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", long_f, timeout=4 * 3600)
        # thumbnail: the same scene + big soft warm text
        thumb = os.path.join(a.out, f"{stamp}-0-long.jpg")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", unit, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                             capture_output=True).stdout
        import io
        im = Image.open(io.BytesIO(raw)).convert("RGB").resize((1280, 720), Image.LANCZOS)
        im = Image.fromarray(np.clip((np.asarray(im).astype(np.float32) - 128) * 1.12 + 140, 0, 255).astype(np.uint8))
        big, small = f"{int(hours)} HOURS", "Cozy Rainy Night" if key != "lake" else "Rainy Lake Night"
        sh_ = Image.new("L", im.size); sd = ImageDraw.Draw(sh_); fb, fs = font(150), font(68)
        for dd, col in ((sd, 255),):
            dd.text((70, 400), big, font=fb, fill=col); dd.text((76, 575), small, font=fs, fill=col)
        sh_ = sh_.filter(ImageFilter.GaussianBlur(10))
        im.paste(Image.new("RGB", im.size, (20, 12, 8)), (6, 8), sh_.point(lambda v: int(v * 0.85)))
        d = ImageDraw.Draw(im)
        d.text((70, 400), big, font=fb, fill=(255, 236, 205)); d.text((76, 575), small, font=fs, fill=(255, 205, 140))
        im.save(thumb, quality=92)
        hrs = f"{int(hours)} Hours"
        variants = [f"{sc['name']} 🌧️ {sc['sound']} | {hrs}", f"{sc['name']} 🌧️ Rain Sounds to Fall Asleep Fast | {hrs}",
                    f"{sc['name']} 🌧️ Relaxing Rain for Sleep & Study | {hrs}", f"{hrs} {sc['name']} 🌧️ {sc['sound']}"]
        title = next((t for t in variants if t not in titles and t not in used["titles"] and len(t) <= 100), variants[0] + f" ({stamp[4:8]})")
        json.dump({"file": os.path.basename(long_f), "kind": "long", "pack": stamp, "thumb": os.path.basename(thumb),
                   "title": title[:100],
                   "description": f"{sc['name']}: {int(hours)} hours of steady rain sounds to fall asleep fast, study or relax. "
                                  "No music, no talking, no ads in the middle — just a cozy scene and gentle rain.\n\n" + credit +
                                  "\n\n#rain #rainsounds #sleep #relaxing #cozy",
                   "tags": ["rain sounds", "rain for sleep", "sleep sounds", "relaxing rain", "cozy rain", "rainy night",
                            f"{int(hours)} hours rain", "deep sleep", "study", "rain sounds for sleeping", "fall asleep fast",
                            sc["short"].lower(), "cozy rainy night", "rain ambience"]},
                  open(os.path.join(a.out, f"{stamp}-0-long.json"), "w"), ensure_ascii=False, indent=1)
        used["titles"].append(title); made += 1
    if a.need_short:
        sunit = os.path.join(tmp, "sunit.mp4")
        make_unit(key, seed, 1080, 1920, sunit, crop_w=1080)
        check_unit(sunit, key)
        short_f = os.path.join(a.out, f"{stamp}-1-short.mp4")
        hook = random.choice(["Close your eyes…", "Breathe slowly…", "Listen to the rain…", "Let the day go…"])
        FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        sh("ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", sunit, "-stream_loop", "-1", "-i", aunit, "-t", "36",
           "-filter_complex",
           f"[0:v]drawtext=fontfile={FONT}:text='{hook}':fontsize=78:fontcolor=0xFFECCD:"
           f"borderw=5:bordercolor=black@0.45:x=(w-tw)/2:y=h*0.16,drawtext=fontfile={FONT}:text='rain sounds for sleep':"
           f"fontsize=46:fontcolor=white@0.9:borderw=3:bordercolor=black@0.45:x=(w-tw)/2:y=h*0.16+110[v];"
           f"[1:a]volume=1.6,afade=t=in:d=0.3[a2]",
           "-map", "[v]", "-map", "[a2]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "128k",
           "-r", "30", short_f)
        st = f"{sc['short']} to Fall Asleep Fast 🌧️ #shorts"
        if st in titles or st in used["titles"]:
            st = f"{hook.rstrip('…')} — {sc['short']} 🌧️ #shorts"
        json.dump({"file": os.path.basename(short_f), "kind": "short", "pack": stamp, "title": st[:100],
                   "description": "Rain sounds to calm your mind. The full long version is here: {LONG_URL}\n\n" + credit +
                                  "\n#rain #rainsounds #sleep #shorts",
                   "tags": ["rain sounds", "sleep", "relaxing rain", "cozy rain", "shorts"]},
                  open(os.path.join(a.out, f"{stamp}-1-short.json"), "w"), ensure_ascii=False, indent=1)
        used["titles"].append(st); made += 1
    if not a.offline_test:
        used["audio"].append(aud["title"]); used["scenes"].append(key)
        json.dump(used, open(USED_F, "w"), ensure_ascii=False)
    print("made", made, key, sc["name"])


if __name__ == "__main__":
    main()

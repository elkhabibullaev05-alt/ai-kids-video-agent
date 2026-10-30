"""Milo Survives wrapper around the Doodle Desk engine (doodle/engine) — does NOT modify Doodle files.

Adds: island/survival props, a red "DAY N" tag top-right (scene key "day"), per-scene voices
(scene key "voice" for side characters), and writes renders to milo/out/<id>/.

    python3 milo/scripts/milo_engine.py milo/scripts/ep002.json --check | --preview 8 | (full)
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MILO = os.path.dirname(HERE)
REPO = os.path.dirname(MILO)
sys.path.insert(0, os.path.join(REPO, "doodle", "engine"))
import ink  # noqa: E402
import render  # noqa: E402

render.ROOT = MILO  # out/<id> and out/_voice go under milo/ (models path already resolved to doodle/models)

MILO_EXTRAS = ["glasses"]  # Milo = glasses + yellow raincoat (shirt "yellow")


# ----------------------------------------------------------------------------- props
def _palm(p, t, color, text):
    sway = math.sin(t * 1.2) * 6
    p.shape([(-14, 0), (14, 0), (30 + sway, -300), (6 + sway, -300)], "brown", 5)
    for a in (-160, -120, -60, -20, 200):
        r = math.radians(a)
        tx, ty = 18 + sway, -300
        p.shape([(tx, ty), (tx + 160 * math.cos(r), ty + 70 * math.sin(r) + 40), (tx + 90 * math.cos(r), ty + 20 * math.sin(r) - 15)], "green", 4)
    for cx in (-4, 24, 44):
        p.circle(cx + sway, -288, 14, "brown", 3)


def _island(p, t, color, text):
    p.ellipse(0, -10, 420, 70, color or "tan", 5)
    for i in range(5):
        x = -360 + i * 180
        p.arc(x, 40, 60, math.pi * 1.1, math.pi * 1.9, 4, "sea")
    if text:
        p.text(text, 0, -10, 46, "dark")


def _coconut(p, t, color, text):
    p.circle(0, -45, 45, color or "brown")
    for dx in (-12, 4, 18):
        p.circle(dx, -62, 5, "dark", 2)
    if text:
        p.text(text, 0, -120, 40, "dark")


def _crab(p, t, color, text):
    k = math.sin(t * 8) * 6
    p.ellipse(0, -40, 60, 35, color or "red")
    for sx in (-1, 1):
        for j in range(3):
            p.line([(sx * 45, -30 + j * 8), (sx * 85, -5 + j * 10)], 4)
        p.circle(sx * 85, -95 + k, 18, color or "red", 4)
        p.line([(sx * 40, -60), (sx * 80, -80)], 4)
    p.circle(-15, -82, 7, "white", 3)
    p.circle(15, -82, 7, "white", 3)


def _wave(p, t, color, text):
    off = math.sin(t * 2) * 20
    for row in range(3):
        pts = [(-400 + k * 40 + off, -row * 40 + 18 * math.sin(k * 0.8 + t * 3 + row)) for k in range(21)]
        p.line(pts, 6, color or "sea")


def _raft(p, t, color, text):
    for i in range(5):
        p.rect(-150 + i * 60, -40, 58, 40, color or "tan", 4)
    p.line([(0, -40), (0, -230)], 6)
    p.shape([(0, -225), (110, -150), (0, -120)], "white", 4)


def _shelter(p, t, color, text):
    p.line([(-170, 0), (0, -210)], 8, "brown")
    p.line([(170, 0), (0, -210)], 8, "brown")
    p.shape([(-160, 0), (0, -200), (160, 0)], color or "green", 4, alpha=0.85)
    p.shape([(-40, 0), (0, -70), (40, 0)], "dark", 3)


def _sos(p, t, color, text):
    p.ellipse(0, -10, 330, 50, "tan", 3)
    p.text(text or "SOS", 0, -20, 150, color or "dark")


def _bottle(p, t, color, text):
    p.rect(-35, -170, 70, 170, color or "sky", 5, alpha=0.8)
    p.rect(-15, -205, 30, 38, "white", 4)
    if text:
        p.text(text, 0, -85, 34, "dark")


def _mirror(p, t, color, text):
    p.circle(0, -60, 55, "grey")
    p.circle(0, -60, 40, "sky")
    for k in range(6):
        a = 2 * math.pi * k / 6 + t
        p.line([(80 * math.cos(a), -60 + 80 * math.sin(a)), (110 * math.cos(a), -60 + 110 * math.sin(a))], 4, "yellow")


def _pot(p, t, color, text):
    p.shape([(-80, -110), (80, -110), (65, -20), (-65, -20)], color or "grey")
    for k in range(3):
        x = -40 + k * 40
        y0 = -130 - (t * 40 + k * 20) % 60
        p.arc(x, y0, 12, math.pi * 0.2, math.pi * 1.2, 3, "grey")
    _fire(p, t, None, None, y=0, s=0.6)


def _fire(p, t, color, text, y=0, s=1.0):
    c = p.c
    c.save()
    c.translate(0, y)
    c.scale(s, s)
    ink.PROPS["fire"](p, t, color, text)
    c.restore()


def _storm(p, t, color, text):
    for cx, cy, r in ((-90, 0, 70), (0, -40, 90), (90, 0, 70)):
        p.circle(cx, cy, r, "grey")
    f = 1 if math.sin(t * 7) > 0.3 else 0
    if f:
        p.shape([(0, 50), (-30, 140), (10, 140), (-20, 240), (50, 110), (10, 110), (30, 50)], "yellow", 4)


def _fin(p, t, color, text):
    x = math.sin(t * 1.5) * 40
    p.shape([(x - 50, 0), (x + 10, -110), (x + 50, 0)], color or "grey")
    p.line([(x - 120, 5), (x + 120, 5)], 5, "sea")


def _bandage(p, t, color, text):
    p.rect(-110, -40, 220, 80, color or "tan", 5)
    p.rect(-35, -40, 70, 80, "white", 4)
    for dx in (-80, -60, 60, 80):
        p.dot(dx, 0, 4, "dark")


def _heli(p, t, color, text):
    p.ellipse(0, -80, 110, 55, color or "orange")
    p.rect(90, -95, 150, 22, color or "orange", 4)
    p.circle(-30, -90, 26, "sky", 3)
    a = t * 30
    p.line([(-170 * math.cos(a), -145), (170 * math.cos(a), -145)], 6)
    p.line([(0, -135), (0, -150)], 5)
    p.line([(-60, -25), (60, -25)], 5)


def _footprint(p, t, color, text):
    for i, (dx, dy) in enumerate(((-60, 0), (30, -70), (-40, -150), (50, -220))):
        p.ellipse(dx, dy, 22, 36, color or "dark", 3)


for _n, _f in {"palm": _palm, "island": _island, "coconut": _coconut, "crab": _crab, "wave": _wave, "raft": _raft,
               "shelter": _shelter, "sos": _sos, "bottle": _bottle, "mirror": _mirror, "pot": _pot, "storm": _storm,
               "fin": _fin, "bandage": _bandage, "heli": _heli, "footprint": _footprint}.items():
    ink.PROPS[_n] = _f


# --- cold / Antarctica props (ep003)
def _tent(p, t, color, text):
    flap = math.sin(t * 6) * 8
    p.shape([(-170, 0), (0, -190), (170, 0)], color or "orange", 5)
    p.shape([(-45, 0), (0, -90 + flap * 0.3), (45 + flap, 0)], "dark", 3)
    p.line([(0, -190), (0, -230)], 5)


def _penguin(p, t, color, text):
    w = math.sin(t * 5) * 5
    p.ellipse(0, -80, 45, 80, "black")
    p.ellipse(0, -70, 30, 62, "white", 3)
    p.circle(0, -165, 30, "black")
    p.circle(-10, -170, 6, "white", 2)
    p.shape([(18, -165), (40, -158), (18, -152)], "orange", 3)
    p.shape([(-40, -120), (-60 - w, -50), (-38, -60)], "black", 3)
    p.shape([(40, -120), (60 + w, -50), (38, -60)], "black", 3)
    p.ellipse(-15, -2, 16, 6, "orange", 3)
    p.ellipse(15, -2, 16, 6, "orange", 3)


def _iceberg(p, t, color, text):
    b = math.sin(t * 1.3) * 5
    p.shape([(-220, b), (-150, -170 + b), (-40, -230 + b), (60, -150 + b), (150, -210 + b), (230, b)], color or "white", 5)
    p.line([(-40, -230 + b), (-10, -120 + b)], 3, "sky")
    p.line([(150, -210 + b), (120, -110 + b)], 3, "sky")
    if text:
        p.text(text, 0, -90 + b, 50, "dark")


def _snow(p, t, color, text):
    for k in range(40):
        x = ((k * 197) % 1800) - 900 + math.sin(t * 2 + k) * 30 - (t * 300) % 200
        y = ((k * 131 + t * (200 + (k % 5) * 60)) % 900) - 800
        p.dot(x, y, 5 + k % 3, color or "white")


def _hut(p, t, color, text):
    p.rect(-200, -200, 400, 200, color or "red", 5)
    p.shape([(-220, -200), (0, -300), (220, -200)], "white", 5)
    p.rect(-40, -120, 80, 120, "dark", 4)
    p.rect(100, -160, 60, 50, "sky", 4)
    if text:
        p.text(text, 0, -230, 40, "dark")


def _rope(p, t, color, text):
    pts = [(-500 + k * 50, -60 + 18 * math.sin(k * 0.9 + t)) for k in range(21)]
    p.line(pts, 6, color or "orange")
    for k in range(0, 21, 5):
        x = -500 + k * 50
        p.line([(x, 0), (x, -140)], 5, "dark")
        p.shape([(x, -140), (x + 50, -120), (x, -100)], "red", 3)


def _plane2(p, t, color, text):  # ski plane
    p.ellipse(0, -80, 170, 40, color or "red")
    p.rect(-40, -160, 80, 160, "white", 3, alpha=0.0)
    p.shape([(-30, -90), (60, -90), (20, -10), (-60, -10)], "white", 4)
    p.shape([(-170, -85), (-210, -150), (-150, -95)], color or "red", 4)
    p.line([(-100, -40), (-100, -10)], 4)
    p.line([(80, -40), (80, -10)], 4)
    p.line([(-140, -8), (130, -8)], 6, "dark")
    a = t * 30
    p.line([(175, -80 - 40 * math.cos(a)), (175, -80 + 40 * math.cos(a))], 6)


for _n, _f in {"tent": _tent, "penguin": _penguin, "iceberg": _iceberg, "snow": _snow, "hut": _hut, "rope": _rope,
               "skiplane": _plane2}.items():
    ink.PROPS[_n] = _f


# ----------------------------------------------------------------------------- per-scene voice
_orig_tts = render.tts
_cur_voice = {"v": None}


def _tts(text, voice, speed, work):
    return _orig_tts(text, _cur_voice["v"] or voice, speed, work)


render.tts = _tts
_orig_bt = render.build_timeline


def _build_timeline(script, work):
    # same as engine, but honour scene["voice"]
    voice = script.get("voice", "am_michael")
    speed = float(script.get("speed", 1.0))
    t = 0.0
    scenes = []
    for i, sc in enumerate(script["scenes"]):
        a = _orig_tts(sc["say"], sc.get("voice", voice), float(sc.get("speed", speed)), work)
        d = len(a) / render.SR
        dur = d + float(sc.get("hold", render.GAP))
        caps = []
        cs = render.chunks(sc["say"])
        tot = sum(len(c) for c in cs) or 1
        ct = 0.0
        for c in cs:
            cd = d * len(c) / tot
            caps.append((t + ct, t + ct + cd, c))
            ct += cd
        scenes.append({"i": i, "t0": t, "t1": t + dur, "dur": dur, "audio": a, "sc": sc, "caps": caps})
        t += dur
    return scenes, t


render.build_timeline = _build_timeline

# ----------------------------------------------------------------------------- DAY tag
_orig_df = render.draw_frame


def _draw_frame(ctx, scene, lt, gt, boil, caption, total, title_card=None):
    pops = _orig_df(ctx, scene, lt, gt, boil, caption, total, title_card)
    day = scene["sc"].get("day")
    if day is not None:
        p = ink.Pen(ctx, boil)
        label = f"DAY {day}"
        w = 44 * len(label) + 60
        p.rect(1884 - w, 30, w, 92, "red", 5)
        p.text(label, 1884 - w / 2, 78, 70, "white")
    return pops


render.draw_frame = _draw_frame

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--preview", type=int, default=0)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    render.render(a.script, a.check, a.preview, a.limit)

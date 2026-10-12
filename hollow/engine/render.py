#!/usr/bin/env python3
"""Hollowmere video engine — gothic storybook horror.

    python3 hollow/engine/render.py SCRIPT.json [--check] [--preview SEC ...] [--out DIR]

Script format: hollow/story/SCRIPT_FORMAT.md
Output (hollow/out/<id>/): <id>.mp4 (English narration, English subtitles burned in),
subs_<lang>.srt (en es de fr it pt), thumbnail.png, upload.txt
"""
import argparse, io, json, math, os, random, subprocess, sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
import cairosvg
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
import audio as A

FPS = 24
R = 1.25                      # world render scale (allows camera zoom up to ~1.25 without blur)
WW, WH = int(1920 * R), int(1080 * R)
LANGS = ["en", "es", "de", "fr", "it", "pt"]
SPEED = {"walk": 220.0, "run": 650.0, "creep": 110.0}
HERE = os.path.dirname(os.path.abspath(__file__))
TITLE_FONT = "font-family=\"Pirata One, IM FELL English SC, serif\""


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


class Track:
    """piecewise-linear value over time (x position, light level, ...)"""
    def __init__(self, v):
        self.keys = [(-1.0, -1.0, v, v)]   # (t0, t1, v0, v1)

    def to(self, t0, t1, v):
        cur = self.at(t0)
        self.keys.append((t0, max(t1, t0 + 1e-3), cur, v))

    def at(self, t):
        v = self.keys[0][2]
        for t0, t1, v0, v1 in self.keys:
            if t >= t1:
                v = v1
            elif t >= t0:
                v = v0 + (v1 - v0) * ease((t - t0) / (t1 - t0))
        return v

    def final(self):
        return self.keys[-1][3]


class Compiler:
    def __init__(self, script, wd):
        self.s, self.wd = script, wd
        self.t, self.shots, self.subs, self.talk, self.sounds, self.errors = 0.0, [], [], [], [], []
        self.cards, self.flashes, self.shakes = [], [], []

    def err(self, m):
        self.errors.append(m)

    def snd(self, sig, t, g=1.0):
        self.sounds.append((t, np.asarray(sig, dtype=np.float32), g))

    def compile(self):
        for i, sh in enumerate(self.s.get("shots", [])):
            self.shot(i, sh)
        self.total = self.t + 0.3
        return self

    def shot(self, i, sh):
        t0 = self.t
        S = {"i": i, "t0": t0, "bg": sh.get("bg", "forest"), "seed": sh.get("seed", i + 1), "music": sh.get("music", "drone"),
             "wind": sh.get("wind", True), "ambient": sh.get("ambient", 0.42), "lights": sh.get("lights", []),
             "cam": sh.get("cam", {}), "focus": sh.get("focus"), "fade": sh.get("fade", True), "chars": {}, "creatures": {},
             "eyes_n": sh.get("eyes", 8), "eyes": Track(1.0 if sh.get("eyes", 8) else 0.0), "lantern": Track(sh.get("lantern", 1.0)),
             "embers": sh.get("embers", sh.get("bg") in ("clearing", "mill", "forest")), "acts": [], "talk": [], "back": sh.get("back", 0.22)}
        if S["bg"] not in art.BACKGROUNDS:
            self.err(f"shot {i}: unknown bg {S['bg']}")
        for cid, c in sh.get("chars", {}).items():
            if cid not in ("odo", "moth"):
                self.err(f"shot {i}: unknown character {cid}"); continue
            S["chars"][cid] = {"x": Track(c.get("x", 700)), "y": Track(c.get("y", 905 if cid == "odo" else 640)),
                               "face": Track(c.get("face", 1)), "scared": Track(c.get("scared", 0.0)),
                               "s": c.get("scale", 1.25 if cid == "odo" else 1.15), "walk": []}
        for kid, c in sh.get("creatures", {}).items():
            typ = c.get("type")
            if typ not in art.CREATURES:
                self.err(f"shot {i}: unknown creature type {typ}"); continue
            st = c.get("state", "visible")
            S["creatures"][kid] = {"type": typ, "x": Track(c.get("x", 1450)), "y": Track(c.get("y", 905 if typ != "hollowmother" else 520)),
                                   "s": c.get("scale", 1.0), "face": c.get("face", -1), "vis": Track(0.0 if st == "hidden" else 1.0),
                                   "mouth": Track(0.0), "rage": Track(c.get("rage", 0.0)), "extra": Track(c.get("extra", 0.0 if typ != "hollowmother" else 1.0)),
                                   "fly": c.get("fly", 0)}
        S["eyes_pos"] = self.eye_positions(S)
        last = t0
        for b in sh.get("beats", []):
            start = last if b.get("and") else self.t
            end = self.beat(S, b, start)
            last = start
            self.t = max(self.t, end)
        self.t += sh.get("tail", 0.6)
        S["t1"] = self.t
        self.shots.append(S)

    def eye_positions(self, S):
        rnd = random.Random(S["seed"] * 31 + 7)
        out = []
        for k in range(S["eyes_n"]):
            for _ in range(20):
                x, y = rnd.uniform(80, 1840), rnd.uniform(420, 860)
                if all(abs(x - c["x"].keys[0][2]) > 260 for c in S["chars"].values()):
                    break
            out.append((x, y, rnd.uniform(2.5, 4.5), rnd.uniform(14, 22), rnd.uniform(0, 9)))
        return out

    def speaker(self, S, who):
        if who == "narr":
            return "narr", None
        if who in S["chars"]:
            return who, ("char", who)
        if who in S["creatures"]:
            return art.CREATURE_VOICE[S["creatures"][who]["type"]], ("creature", who)
        if who in A.CAST:
            return who, None
        self.err(f"shot {S['i']}: unknown speaker {who}")
        return "narr", None

    def beat(self, S, b, t):
        if "say" in b:
            who = b["say"]
            voice, ref = self.speaker(S, who)
            text = b.get("en", "")
            if not text:
                self.err(f"shot {S['i']}: empty line"); return t
            miss = [l for l in LANGS if not b.get(l)]
            if miss:
                self.err(f"shot {S['i']}: missing subtitles {miss} for '{text[:30]}'")
            sig = A.voice(voice, text, self.wd)
            d = len(sig) / A.SR
            self.snd(sig, t + 0.05, 1.0 if voice == "narr" else 1.05)
            self.subs.append((t + 0.05, t + d + 0.25, {l: b.get(l, "") for l in LANGS}))
            self.talk.append((t, t + d, who))
            S["talk"].append((t, t + d, who))
            if ref and ref[0] == "creature":
                S["creatures"][who]["mouth"].to(t, t + 0.15, 0.8)
                S["creatures"][who]["mouth"].to(t + d, t + d + 0.2, 0.0)
            return t + d + b.get("gap", 0.35)
        if "wait" in b and len(b) <= 2:
            return t + float(b["wait"])
        if "move" in b:
            who, to = b["move"], b.get("to", 0)
            obj = S["chars"].get(who) or S["creatures"].get(who)
            if not obj:
                self.err(f"shot {S['i']}: move unknown {who}"); return t
            x0 = obj["x"].at(t)
            x1 = {"off_left": -350, "off_right": 2270}.get(to, to) if isinstance(to, str) else float(to)
            sp = SPEED.get(b.get("speed", "walk"), 220)
            d = abs(x1 - x0) / sp
            obj["x"].to(t, t + d, x1)
            if who in S["chars"]:
                S["chars"][who]["walk"].append((t, t + d, 1 if b.get("speed") == "run" else 0.6))
                S["chars"][who]["face"].to(t, t + 0.01, 1 if x1 > x0 else -1)
            if "y" in b:
                obj["y"].to(t, t + d, float(b["y"]))
            if who in S["chars"] and who == "odo":
                for k in range(int(d / 0.45)):
                    self.snd(A.step(), t + k * 0.45 + 0.1, 0.5)
            return t + d
        if "show" in b or "hide" in b:
            who = b.get("show") or b.get("hide")
            c = S["creatures"].get(who)
            if not c:
                self.err(f"shot {S['i']}: show/hide unknown {who}"); return t
            d = b.get("dur", 0.9)
            c["vis"].to(t, t + d, 1.0 if "show" in b else 0.0)
            return t + d
        if "lunge" in b:
            c = S["creatures"].get(b["lunge"])
            if not c:
                self.err(f"shot {S['i']}: lunge unknown {b['lunge']}"); return t
            c["x"].to(t, t + 0.45, float(b.get("to", c["x"].at(t) - 300)))
            c["mouth"].to(t, t + 0.2, 1.0); c["mouth"].to(t + 0.9, t + 1.2, 0.0)
            c["rage"].to(t, t + 0.2, 1.0)
            self.snd(A.hit(), t, 0.9); self.snd(A.growl(1.2), t, 0.6)
            self.shakes.append((t, t + 0.6, 22))
            return t + 0.9
        if "growl" in b:
            c = S["creatures"].get(b["growl"])
            if not c:
                self.err(f"shot {S['i']}: growl unknown {b['growl']}"); return t
            c["mouth"].to(t, t + 0.25, 0.7); c["mouth"].to(t + 1.4, t + 1.7, 0.0)
            c["rage"].to(t, t + 0.4, 0.7)
            self.snd(A.growl(1.7), t, 0.8)
            return t + 1.7
        if "act" in b:
            whos = b["act"] if isinstance(b["act"], list) else [b["act"]]
            do = b.get("do", "shake")
            d = {"shake": 1.2, "jump": 0.6, "fall": 0.9, "hide": 0.6, "unhide": 0.6, "turn": 0.3, "scared": 0.3, "calm": 0.3,
                 "reach": 1.2, "rise": 1.0, "drop": 1.4}.get(do, 0.6)
            for w in whos:
                if w in S["chars"]:
                    ch = S["chars"][w]
                    if do in ("scared", "shake"):
                        ch["scared"].to(t, t + 0.3, 1.0)
                    if do == "calm":
                        ch["scared"].to(t, t + 0.3, 0.0)
                    if do == "turn":
                        ch["face"].to(t, t + 0.05, -ch["face"].at(t))
                elif w in S["creatures"]:
                    cr = S["creatures"][w]
                    if do in ("reach", "rise", "drop"):
                        cr["extra"].to(t, t + d, float(b.get("level", 1.0)))
                else:
                    self.err(f"shot {S['i']}: act unknown {w}")
                S["acts"].append((t, t + d, w, do))
            if do == "jump":
                self.snd(A.snap(), t, 0.4)
            return t + d
        if "light" in b:
            mode = b["light"]
            lv = {"on": 1.0, "dim": 0.45, "out": 0.0, "flare": 1.7}.get(mode, 1.0)
            d = {"out": 0.25, "flare": 0.3}.get(mode, 0.7)
            S["lantern"].to(t, t + d, lv)
            if mode == "flare":
                S["lantern"].to(t + d + 0.4, t + d + 1.2, 1.0)
            if mode == "out":
                self.snd(A.whoosh(0.5), t, 0.6)
            return t + d
        if "eyes" in b:
            S["eyes"].to(t, t + 1.0, 1.0 if b["eyes"] == "open" else 0.0)
            if b["eyes"] == "open":
                self.snd(A.whisper(2.0), t, 0.9)
            return t + 1.0
        if "flash" in b:
            self.flashes.append((t, t + 0.35))
            self.snd(A.hit(), t, 1.0)
            return t + 0.35
        if "sfx" in b:
            k = b["sfx"]
            if k not in A.SFX:
                self.err(f"shot {S['i']}: unknown sfx {k}"); return t
            self.snd(A.SFX[k](), t, b.get("gain", 0.8))
            return t + b.get("wait", 0.0)
        if "shake" in b:
            d = float(b["shake"])
            self.shakes.append((t, t + d, b.get("power", 14)))
            return t + d
        if "card" in b:
            d = b.get("dur", 2.4)
            self.cards.append((t, t + d, b["card"]))
            self.snd(A.bell(), t, 0.5)
            return t + d
        self.err(f"shot {S['i']}: unknown beat {b}")
        return t


# ============================================================ frame drawing
C = None
CAMX = None
BG_CACHE = {}
DEFS = ""


def shot_at(t):
    for S in C.shots:
        if t < S["t1"]:
            return S
    return C.shots[-1]


def talking(S, t):
    for a, b, w in S["talk"]:
        if a <= t <= b:
            return w
    return None


def acting(S, who, t):
    for a, b, w, do in S["acts"]:
        if w == who and a <= t <= b:
            return do, (t - a) / (b - a)
    return None, 0


def walking(ch, t):
    for a, b, k in ch["walk"]:
        if a <= t <= b:
            return k
    return 0


def world_layers(S, t):
    """returns (lit_svg, emissive_svg, light list [(x,y,r,intensity,color)])"""
    lit, em, lights = [], [], []
    who = talking(S, t)
    lv = S["lantern"].at(t)
    # soft horizon backlight so silhouettes read against the sky
    lights.append((960, 700, 1150, S.get("back", 0.22), (1.0, 0.75, 0.55)))
    # static fires / lights of the shot
    for L in S["lights"]:
        x, y, r = L.get("x", 960), L.get("y", 880), L.get("r", 520)
        kind = L.get("kind", "fire")
        fl = 1 + 0.08 * math.sin(t * 19 + x) + 0.06 * math.sin(t * 31)
        if kind == "fire":
            lit.append(f'<path d="M{x-70},{y+14} L{x+70},{y-6} L{x+74},{y+8} L{x-66},{y+28} Z M{x-60},{y-8} L{x+64},{y+20} L{x+58},{y+32} L{x-64},{y+4} Z" fill="{art.INK}"/>')
            for k in range(5):
                fx = x + (k - 2) * 18 + math.sin(t * 7 + k) * 4
                fh = (60 + 30 * math.sin(t * 9 + k * 1.7)) * (1.2 - abs(k - 2) * 0.2)
                em.append(f'<path d="M{fx-14},{y} Q{fx-10},{y-fh*0.6} {fx+math.sin(t*11+k)*8},{y-fh} Q{fx+12},{y-fh*0.5} {fx+14},{y} Z" fill="url(#flame)" opacity="0.9"/>')
            em.append(f'<circle cx="{x}" cy="{y-30}" r="{r*0.5*fl}" fill="url(#warm)"/>')
            lights.append((x, y - 40, r * fl, 1.0, (1.0, 0.62, 0.30)))
        elif kind == "moon":
            lights.append((x, y, r, 0.55, (0.70, 0.78, 1.0)))
        elif kind == "window":
            lights.append((x, y, r, 0.6, (1.0, 0.7, 0.35)))
    # creatures (drawn behind characters)
    for kid, c in S["creatures"].items():
        v = c["vis"].at(t)
        if v <= 0.01:
            continue
        x, y = c["x"].at(t), c["y"].at(t)
        fn = art.CREATURES[c["type"]]
        seed = hash(kid) % 97
        typ = c["type"]
        if typ == "gloamhound":
            body, e = fn(x, y, t, c["s"], c["face"], c["mouth"].at(t), c["rage"].at(t), seed)
        elif typ == "rootwraith":
            body, e = fn(x, y, t, c["s"], c["face"], c["extra"].at(t), seed)
        elif typ == "crow":
            body, e = fn(x, y, t, c["s"], c["face"], c["fly"], seed)
        elif typ == "hollowmother":
            body, e = fn(x, y, t, c["s"], c["extra"].at(t), seed)
        elif typ == "wickeater":
            body, e = fn(x, y, t, c["s"], c["face"], 0.4 + 0.6 * c["mouth"].at(t) + 0.3 * (1 - min(1, lv)), seed)
        else:
            body, e = fn(x, y, t, c["s"], c["face"], c["extra"].at(t), seed)
        lit.append(f'<g opacity="{v:.3f}">{body}</g>')
        glow = {"shepherd": ((0.75, 0.80, 1.0), -600), "rootwraith": ((1.0, 0.65, 0.3), -400), "hollowmother": ((0.75, 0.82, 1.0), 0),
                "wickeater": ((1.0, 0.7, 0.3), -60), "gloamhound": ((1.0, 0.25, 0.12), -210), "crow": ((1.0, 0.3, 0.2), -40)}[typ]
        lights.append((x, y + glow[1] * c["s"], 260 * c["s"], 0.30 * v, glow[0]))
        em.append(f'<g opacity="{v:.3f}">{e}</g>')
    # characters
    if "odo" in S["chars"]:
        ch = S["chars"]["odo"]
        x, y = ch["x"].at(t), ch["y"].at(t)
        do, u = acting(S, "odo", t)
        if do == "jump":
            y -= math.sin(u * math.pi) * 90
        s = ch["s"]
        sy = 1.0
        if do == "hide":
            sy = 1 - 0.3 * ease(u)
        elif do == "fall":
            sy = 1 - 0.35 * ease(u)
        body, e, lp = art.odo(x, y, t, s, 1 if ch["face"].at(t) >= 0 else -1, talk=1.0 if who == "odo" else 0.0,
                              lit=lv, scared=ch["scared"].at(t) + (0.6 if do == "shake" else 0), walk=walking(ch, t))
        if sy != 1.0:
            body = f'<g transform="translate({x},{y}) scale(1,{sy:.3f}) translate({-x},{-y})">{body}</g>'
        lit.append(body); em.append(e)
        if lv > 0.02:
            fl = 1 + 0.07 * math.sin(t * 23) + 0.05 * math.sin(t * 41)
            lights.append((lp[0], lp[1], 430 * min(lv, 1.6) * fl, min(lv, 1.6), (1.0, 0.70, 0.38)))
    if "moth" in S["chars"]:
        ch = S["chars"]["moth"]
        body, e = art.moth(ch["x"].at(t), ch["y"].at(t), t, ch["s"], 1 if ch["face"].at(t) >= 0 else -1, talk=1.0 if who == "moth" else 0.0)
        lit.append(body); em.append(e)
        lights.append((ch["x"].at(t), ch["y"].at(t), 170, 0.35, (0.75, 0.82, 1.0)))
    # eyes in the dark
    eo = S["eyes"].at(t)
    if eo > 0.01:
        g = []
        blockers = []
        for c in S["creatures"].values():
            if c["vis"].at(t) > 0.3:
                w = {"shepherd": 170, "rootwraith": 260, "gloamhound": 300, "hollowmother": 260, "wickeater": 80, "crow": 70}[c["type"]] * c["s"]
                blockers.append((c["x"].at(t) - w, c["x"].at(t) + w))
        for ch in S["chars"].values():
            blockers.append((ch["x"].at(t) - 110, ch["x"].at(t) + 190))
        for k, (x, y, r, gap, ph) in enumerate(S["eyes_pos"]):
            if (t + ph) % 7.0 < 0.9 and k % 3 == 0:
                continue   # some pairs vanish now and then
            if any(a < x < b or a < x + gap < b for a, b in blockers):
                continue
            dx = math.sin(t * 0.4 + ph) * 6
            g.append(art.red_eye(x + dx, y, r, t, k) + art.red_eye(x + dx + gap, y, r, t, k))
        em.append(f'<g opacity="{eo:.3f}">{"".join(g)}</g>')
    # embers
    if S["embers"]:
        rnd = random.Random(S["i"])
        g = []
        for k in range(26):
            sx, sp, ph = rnd.uniform(0, 1920), rnd.uniform(30, 70), rnd.uniform(0, 30)
            yy = 1000 - ((t * sp + ph * 40) % 900)
            xx = sx + math.sin(t * 1.3 + ph) * 30
            g.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{1.6 + (k % 3) * 0.6:.1f}" fill="#ffb060" opacity="{0.35 + 0.3 * math.sin(t * 3 + ph):.2f}"/>')
        em.append("".join(g))
    # moving fog
    fog = art.PAL[S["bg"]][5]
    lit.append("".join(f'<ellipse cx="{(300 + k * 520 + t * (12 + k * 5)) % 2600 - 300:.1f}" cy="{860 + k * 30}" rx="520" ry="46" fill="{fog}" opacity="0.05"/>' for k in range(4)))
    return "".join(lit), "".join(em), lights


def svg_png(body, w, h, scale):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}'
           f'<g transform="scale({scale})">{body}</g></svg>')
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA"), dtype=np.float32) / 255.0


def bg_img(S):
    k = (S["bg"], S["seed"])
    if k not in BG_CACHE:
        BG_CACHE.clear()
        BG_CACHE[k] = svg_png(art.background(S["bg"], S["seed"]), WW, WH, R)[..., :3]
    return BG_CACHE[k]


def light_mask(lights, amb, shape):
    """low-res light map -> full res. lights in world coords"""
    h, w = shape[0] // 8, shape[1] // 8
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    xs *= 8 / R; ys *= 8 / R
    m = np.zeros((h, w, 3), np.float32) + amb * np.array([0.78, 0.74, 0.80], np.float32)
    for x, y, r, inten, col in lights:
        d = np.sqrt((xs - x) ** 2 + (ys - y) ** 2) / max(r, 1)
        f = np.clip(1 - d, 0, 1) ** 1.6 * inten
        m += f[..., None] * np.array(col, np.float32)
    m = np.clip(m, 0, 1.6)
    img = Image.fromarray((np.clip(m / 1.6, 0, 1) * 255).astype(np.uint8)).resize((shape[1], shape[0]), Image.BILINEAR)
    return np.asarray(img, np.float32) / 255.0 * 1.6


def over(dst, src):
    a = src[..., 3:4]
    return dst * (1 - a) + src[..., :3] * a


def cam_at(S, t, fi):
    c = S["cam"]
    a = c.get("from", [960, 600, 1.12])
    b = c.get("to", a)
    u = ease((t - S["t0"]) / max(0.1, S["t1"] - S["t0"]))
    cx, cy, z = [a[i] + (b[i] - a[i]) * u for i in range(3)]
    if C.fmt == "short":
        cx = CAMX[min(fi, len(CAMX) - 1)]
    return cx, cy, z


def shake_amt(t):
    p = 0
    for a, b, pw in C.shakes:
        if a <= t <= b:
            p = max(p, pw * (1 - (t - a) / (b - a)))
    return p


GRAIN = None


def frame(fi):
    global GRAIN
    t = fi / FPS
    for a, b, text in C.cards:
        if a <= t < b:
            return card_frame(text, (t - a) / (b - a))
    S = shot_at(t)
    base = bg_img(S).copy()
    lit, em, lights = world_layers(S, t)
    base = over(base, svg_png(lit, WW, WH, R))
    base *= light_mask(lights, S["ambient"], base.shape)
    emi = svg_png(em, WW, WH, R)
    base = base + emi[..., :3] * emi[..., 3:4] * 1.0   # additive glow
    # camera
    cx, cy, z = cam_at(S, t, fi)
    sh = shake_amt(t)
    rnd = random.Random(fi)
    cx += rnd.uniform(-sh, sh); cy += rnd.uniform(-sh, sh)
    OW, OH = (1920, 1080) if C.fmt == "long" else (1080, 1920)
    ch = 1080 / z
    cw = ch * OW / OH
    cx = clamp(cx, cw / 2, 1920 - cw / 2); cy = clamp(cy, ch / 2, 1080 - ch / 2)
    box = tuple(int(v * R) for v in (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)).resize((OW, OH), Image.BILINEAR, box=box)
    out = np.asarray(img, np.float32) / 255.0
    # grade: crush blacks, warm mids, vignette, grain, fades, flash
    out = np.clip((out - 0.03) * 1.12, 0, 1) ** 1.08
    if GRAIN is None:
        g = np.random.RandomState(1).randn(OH // 2, OW // 2).astype(np.float32)
        GRAIN = g
    gy, gx = (fi * 37) % (OH // 2), (fi * 53) % (OW // 2)
    gr = np.roll(np.roll(GRAIN, gy, 0), gx, 1)
    gr = np.repeat(np.repeat(gr, 2, 0), 2, 1)[:OH, :OW]
    out = out + gr[..., None] * 0.028
    ys, xs = np.ogrid[0:OH, 0:OW]
    vig = 1 - 0.55 * (((xs - OW / 2) / (OW / 1.6)) ** 2 + ((ys - OH / 2) / (OH / 1.5)) ** 2)
    out *= np.clip(vig, 0.25, 1)[..., None]
    if S["fade"]:
        k = min(clamp((t - S["t0"]) / 0.35), clamp((S["t1"] - t) / 0.35))
        out *= 0.15 + 0.85 * k if S["i"] else k
    for a, b in C.flashes:
        if a <= t <= b:
            out = out + (1 - (t - a) / (b - a)) * 0.85
    if C.fmt == "short" and HOOK is not None:
        out = over(out, HOOK)
    return (np.clip(out, 0, 1) * 255).astype(np.uint8).tobytes()


HOOK = None


def hook_layer(text):
    lines = wrap(text.upper(), 16)
    t = "".join(f'<text x="540" y="{220 + n * 120}" text-anchor="middle" {TITLE_FONT} font-size="118" fill="{art.BONE}" '
                f'stroke="#3a0804" stroke-width="10" paint-order="stroke">{esc(l)}</text>' for n, l in enumerate(lines[:2]))
    # cairosvg ignores paint-order: draw stroke pass then fill pass
    s1 = t.replace(f'fill="{art.BONE}"', 'fill="#3a0804"')
    s2 = t.replace('stroke="#3a0804" stroke-width="10"', '')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><defs><linearGradient id="tf" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0%" stop-color="#000" stop-opacity="0.85"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></linearGradient></defs>'
           f'<rect width="1080" height="520" fill="url(#tf)"/>{s1}{s2}</svg>')
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA"), np.float32) / 255.0


def card_frame(text, u):
    OW, OH = (1920, 1080) if C.fmt == "long" else (1080, 1920)
    a = min(clamp(u / 0.2), clamp((1 - u) / 0.2))
    lines = wrap(text.upper(), 22 if C.fmt == "long" else 14)
    fs = 92 if C.fmt == "long" else 104
    y0 = OH / 2 - (len(lines) - 1) * fs * 0.6
    tx = "".join(f'<text x="{OW/2}" y="{y0 + n*fs*1.2}" text-anchor="middle" {TITLE_FONT} font-size="{fs}" fill="{art.BONE}" opacity="{a:.3f}">{esc(l)}</text>' for n, l in enumerate(lines))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{OW}" height="{OH}"><rect width="{OW}" height="{OH}" fill="#050302"/>{tx}</svg>'
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGB"), np.uint8).tobytes()


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + ([cur] if cur else [])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def init_worker(c, camx, hook):
    global C, CAMX, DEFS, HOOK
    C, CAMX, HOOK = c, camx, hook
    DEFS = "<defs>" + art.bg_defs() + "</defs>"


def camera_track(c, n):
    """smoothed horizontal camera for vertical shorts: follows the speaker / action"""
    global C
    C = c
    out, cur = [], None
    for fi in range(n):
        t = fi / FPS
        S = shot_at(t)
        if S["cam"].get("x") is not None:
            target = S["cam"]["x"]
        else:
            who = talking(S, t)
            xs = []
            if who in S["chars"]:
                xs = [S["chars"][who]["x"].at(t)]
            elif who in S["creatures"] and S["creatures"][who]["vis"].at(t) > 0.5:
                xs = [S["creatures"][who]["x"].at(t)]
            else:
                foc = S["focus"]
                pool = [foc] if isinstance(foc, str) else (foc or list(S["chars"]) + list(S["creatures"]))
                for k in pool:
                    o = S["chars"].get(k) or S["creatures"].get(k)
                    if o and ("vis" not in o or o["vis"].at(t) > 0.5):
                        xs.append(o["x"].at(t))
            target = sum(xs) / len(xs) if xs else 960
        if cur is None or S["t0"] <= t < S["t0"] + 1 / FPS:
            cur = target
        cur += (target - cur) * 0.05
        out.append(cur)
    return out


# ============================================================ audio / subs / thumb / upload
def build_audio(c, path):
    n = int(c.total * A.SR) + A.SR
    mix = np.zeros(n, np.float32)

    def put(sig, at, g):
        i = int(at * A.SR)
        if i >= n:
            return
        sig = np.asarray(sig[: n - i], np.float32)
        mix[i:i + len(sig)] += sig * g

    for S in c.shots:
        d = S["t1"] - S["t0"] + 0.5
        m = S["music"]
        if m in ("drone", "heartbeat", "choir", "lullaby"):
            put(A.drone(d, 41.2), S["t0"], 1.1)
        if m == "heartbeat":
            put(A.heartbeat(d, 64), S["t0"], 0.9)
        if m == "choir":
            put(A.choir(d), S["t0"], 1.0)
        if m == "lullaby":
            put(A.lullaby(d), S["t0"], 1.0)
        if S["wind"]:
            put(A.wind(d), S["t0"], 0.8)
        if S["lights"] and any(L.get("kind", "fire") == "fire" for L in S["lights"]):
            put(A.crackle(d), S["t0"], 0.7)
    for t, sig, g in c.sounds:
        put(sig, t, g)
    mix /= max(1e-6, float(np.max(np.abs(mix)))) / 0.9
    sf.write(path, mix, A.SR)


def ts(x):
    return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int((x%1)*1000):03}"


def write_srt(c, lang, path):
    rows, n = [], 1
    subs = sorted(c.subs, key=lambda s: s[0])
    for i, (a, b, tx) in enumerate(subs):
        text = tx.get(lang) or ""
        if not text:
            continue
        if i + 1 < len(subs):
            b = min(b, subs[i + 1][0] - 0.02)
        rows.append(f"{n}\n{ts(a)} --> {ts(b)}\n{text}\n"); n += 1
    open(path, "w", encoding="utf-8").write("\n".join(rows))


def thumbnail(script, path):
    th = script.get("thumbnail", {})
    bg = th.get("bg", "forest")
    cr = th.get("creature", "gloamhound")
    text = th.get("text", "DON'T LOOK")
    t = 1.3
    body = [art.background(bg, th.get("seed", 2)), '<rect x="-100" y="-100" width="2200" height="1300" fill="#000" opacity="0.35"/>']
    em = []
    fn = art.CREATURES[cr]
    if cr == "hollowmother":
        b, e = fn(1350, 480, t, 1.6, 1.0)
    elif cr in ("shepherd", "rootwraith"):
        b, e = fn(1420, 1000, t, 1.35, -1, 0.8)
    elif cr == "crow":
        b, e = fn(1400, 700, t, 4.0, -1, 0)
    elif cr == "wickeater":
        b, e = fn(1400, 960, t, 3.4, -1, 1.0)
    else:
        b, e = fn(1300, 1000, t, 1.9, -1, 1.0, 1.0)
    body.append(b); em.append(e)
    o, oe, lp = art.odo(470, 1000, t, 1.7, 1, scared=1.0)
    body.append(o); em.append(oe)
    rnd = random.Random(5)
    for k in range(10):
        x, y = rnd.uniform(80, 1000), rnd.uniform(380, 700)
        em.append(art.red_eye(x, y, 4, t, k) + art.red_eye(x + 18, y, 4, t, k))
    lights = [(lp[0], lp[1], 600, 1.4, (1.0, 0.70, 0.38)), (1350, 600, 700, 0.5, (1.0, 0.25, 0.15))]
    base = svg_png("".join(body), WW, WH, R)[..., :3]
    base *= light_mask(lights, 0.45, base.shape)
    emi = svg_png("".join(em), WW, WH, R)
    base = base + emi[..., :3] * emi[..., 3:4]
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)).resize((1280, 720), Image.LANCZOS)
    lines = wrap(text.upper(), 12)[:2]
    tx = "".join(f'<text x="44" y="{150 + n * 140}" {TITLE_FONT} font-size="150" fill="{{F}}" {{S}}>{esc(l)}</text>' for n, l in enumerate(lines))
    over_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">'
                + tx.replace("{F}", "#1a0302").replace("{S}", 'stroke="#1a0302" stroke-width="18" stroke-linejoin="round"')
                + tx.replace("{F}", "#f2e6cc").replace("{S}", "")
                + "</svg>")
    ov = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=over_svg.encode()))).convert("RGBA")
    img = img.convert("RGBA"); img.alpha_composite(ov)
    img.convert("RGB").save(path)


def upload_txt(script, path, dur):
    s = script
    txt = (f"TITLE:\n{s.get('title','')}\n\nDESCRIPTION:\n{s.get('description','')}\n\nTAGS:\n{', '.join(s.get('tags', []))}\n\n"
           f"LENGTH: {dur:.0f}s   FORMAT: {s.get('format')}\n"
           "AUDIENCE: Not made for kids (general audience 13+)\nSUBTITLES: English burned in; upload subs_es/de/fr/it/pt.srt in YouTube Studio > Subtitles\n")
    open(path, "w", encoding="utf-8").write(txt)


# ============================================================ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out")
    ap.add_argument("--preview", nargs="*", type=float)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    script = json.load(open(args.script, encoding="utf-8"))
    sid = script.get("id") or os.path.splitext(os.path.basename(args.script))[0]
    out = args.out or os.path.join(HERE, "..", "out", sid)
    os.makedirs(out, exist_ok=True)
    wd = os.path.join(HERE, "..", "out", "_voicecache")
    os.makedirs(wd, exist_ok=True)
    c = Compiler(script, wd).compile()
    c.fmt = script.get("format", "long")
    print(f"[{sid}] duration {c.total:.1f}s, shots {len(c.shots)}, lines {len(c.talk)}")
    if c.errors:
        print("PROBLEMS:"); [print("  -", e) for e in c.errors]
        if [e for e in c.errors if "missing subtitles" not in e]:
            sys.exit(2)
    if args.check:
        return
    n = int(c.total * FPS)
    camx = camera_track(c, n) if c.fmt == "short" else None
    hook = hook_layer(script.get("hook", "")) if c.fmt == "short" and script.get("hook") else None
    OW, OH = (1920, 1080) if c.fmt == "long" else (1080, 1920)
    if args.preview is not None:
        init_worker(c, camx, hook)
        for sec in args.preview:
            Image.frombytes("RGB", (OW, OH), frame(int(sec * FPS))).save(os.path.join(out, f"preview_{sec:g}.png"))
        print("previews in", out); return
    build_audio(c, os.path.join(out, "audio.wav"))
    for l in LANGS:
        write_srt(c, l, os.path.join(out, f"subs_{l}.srt"))
    thumbnail(script, os.path.join(out, "thumbnail.png"))
    upload_txt(script, os.path.join(out, "upload.txt"), c.total)
    c.sounds = []
    raw = os.path.join(out, "_video.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
                           "-framerate", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                           "-pix_fmt", "yuv420p", raw], stdin=subprocess.PIPE)
    with Pool(os.cpu_count() or 2, initializer=init_worker, initargs=(c, camx, hook)) as p:
        for i, fr in enumerate(p.imap(frame, range(n), chunksize=8)):
            ff.stdin.write(fr)
            if i % 240 == 0:
                print(f"  frame {i}/{n}", flush=True)
    ff.stdin.close(); ff.wait()
    fs = (17, 1.3, 26) if c.fmt == "long" else (11, 1.0, 70)
    style = (f"FontName=IM FELL English,FontSize={fs[0]},PrimaryColour=&H00E6F2F5,OutlineColour=&H00000000,BackColour=&H80000000,"
             f"BorderStyle=1,Outline={fs[1]},Shadow=1.2,MarginV={fs[2]}")
    srt = os.path.join(out, "subs_en.srt").replace("\\", "/").replace(":", "\\:")
    final = os.path.join(out, f"{sid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", os.path.join(out, "audio.wav"),
                    "-vf", f"subtitles='{srt}':force_style='{style}'", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    os.remove(raw)
    print("DONE", final)


if __name__ == "__main__":
    main()

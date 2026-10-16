#!/usr/bin/env python3
"""Dough Bros video engine.

    python doughbros/engine/render.py SCRIPT.json [--out DIR] [--preview SEC ...] [--fast]

Turns an episode script (see doughbros/story/SCRIPT_FORMAT.md) into:
    video.mp4 (English voices, Spanish subs burned in), subs_<lang>.srt, thumbnail.png, upload.txt
"""
import argparse, json, math, os, random, subprocess, sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
import cairosvg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chars import defs as char_defs, dough
from villains import DRAW as VDRAW, villain_defs, VILLAINS
from backgrounds import background, bg_defs, BACKGROUNDS
import audio as A

FPS = 24
HEROES = ["bup", "pim", "zeek", "lolly", "crispy"]
BASE_MOUTH = {"bup": "stitch", "pim": "wobble", "zeek": "flat", "lolly": "grin", "crispy": "flat"}
SUB_LANGS = ["es", "de", "fr", "it", "pt"]
HERO_Y, VIL_Y = 680, 540
WALK, RUN = 260.0, 950.0
GLOW = {"pot": "#ff4a10", "frost": "#5ab8ff", "toaster": "#ff8a1a", "mixer": "#9aff3a",
        "vacuum": "#ff2a3a", "jelly": "#6aff5a", "kettle": "#ffd23a", "scarecrow": "#ff9a1a"}
IMPACT = "font-family='Inter Display Black, Inter Black, Impact, Arial Black, DejaVu Sans, sans-serif' font-weight='900'"


def bold_text(x, y, text, size, fill="#ffd23a", stroke=10, anchor="middle", extra=""):
    """outlined title text (draws stroke layer then fill layer - cairosvg ignores paint-order)"""
    base = f'x="{x}" y="{y}" text-anchor="{anchor}" {IMPACT} font-size="{size}" {extra}'
    return (f'<text {base} fill="#000" stroke="#000" stroke-width="{stroke}" stroke-linejoin="round">{esc(text)}</text>'
            f'<text {base} fill="{fill}">{esc(text)}</text>')
SCREAMS = {"bup": "Aaaaaah!", "pim": "Aaaaaaaah!", "zeek": "Waaaaah!", "lolly": "Eeeeeek!", "crispy": "Hhhrraaagh!"}


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ======================================================================
#   1. Compile script -> timeline
# ======================================================================
class Actor:
    def __init__(self, x):
        self.seg = [(-1e9, -1e9, x, x, "idle")]  # (t0, t1, x0, x1, kind)
        self.events = []      # (t0, t1, kind)
        self.mood = [(-1e9, "normal")]
        self.hidden = [(-1e9, False)]

    def x_at(self, t):
        cur = self.seg[0]
        for s in self.seg:
            if s[0] <= t:
                cur = s
        t0, t1, x0, x1, k = cur
        if t >= t1:
            return x1, None
        p = (t - t0) / (t1 - t0)
        return x0 + (x1 - x0) * (ease(p) if k == "lunge_back" else p), k

    def final_x(self):
        return self.seg[-1][3]

    def last(self, lst, t):
        v = lst[0][1]
        for tt, vv in lst:
            if tt <= t:
                v = vv
        return v


class Villain(Actor):
    def __init__(self, typ, x, state, scale):
        super().__init__(x)
        self.type, self.scale = typ, scale
        self.awake = [(-1e9, state == "awake", -1e9)]  # (t, awake, transition start)
        self.rage = [(-1e9, 0.0)]
        if state == "hidden":
            self.hidden = [(-1e9, True)]


class Compiler:
    def __init__(self, script, workdir):
        self.s, self.wd = script, workdir
        self.errors = []
        self.t = 0.0
        self.scenes = []     # dicts with t0, t1, bg, heroes{id:Actor}, villain
        self.talk = []       # (t0, dur, who(actor key), env)
        self.sounds = []     # (t, ndarray, gain)
        self.subs = []       # (t0, t1, {lang: text})
        self.cards = []      # (t0, t1, en, es)
        self.shakes = []     # (t0, dur, power)

    def err(self, m):
        self.errors.append(m)

    def snd(self, arr, t, gain=1.0):
        self.sounds.append((t, np.asarray(arr, dtype=np.float32), gain))

    def env(self, a):
        hop = A.SR // FPS
        r = [float(np.sqrt(np.mean(a[i:i + hop] ** 2))) if len(a[i:i + hop]) else 0 for i in range(0, len(a), hop)]
        m = max(r) if r and max(r) > 0 else 1
        return [v / m for v in r]

    def compile(self):
        s = self.s
        if s.get("format") not in ("long", "short"):
            self.err("format must be 'long' or 'short'")
        for i, sc in enumerate(s.get("scenes", [])):
            self.scene(i, sc)
        if s.get("end_card", True) and s.get("format") == "long":
            ec = s.get("end_card") if isinstance(s.get("end_card"), dict) else {}
            self.card(ec.get("en", "TO BE CONTINUED..."), ec.get("es", "CONTINUARÁ..."), 4.0, sting=True)
        self.total = self.t + (0.0 if s.get("format") == "short" else 0.3)
        return self

    def card(self, en, es, dur, sting=False):
        self.cards.append((self.t, self.t + dur, en, es))
        if sting:
            self.snd(A.sting(), self.t, 0.9)
        self.subs.append((self.t + 0.3, self.t + dur, {"es": es}))
        self.t += dur

    def scene(self, i, sc):
        bg = sc.get("bg", "kitchen")
        if bg not in BACKGROUNDS:
            self.err(f"scene {i}: unknown bg '{bg}'")
            bg = "kitchen"
        t0 = self.t
        heroes = {}
        for h, x in (sc.get("heroes") or {}).items():
            if h not in HEROES:
                self.err(f"scene {i}: unknown hero '{h}'")
                continue
            heroes[h] = Actor(float(x))
            if sc.get("moods", {}).get(h):
                heroes[h].mood = [(-1e9, sc["moods"][h])]
        v = None
        vs = sc.get("villain")
        if vs:
            if vs.get("type") not in VDRAW:
                self.err(f"scene {i}: unknown villain '{vs.get('type')}'")
            else:
                v = Villain(vs["type"], float(vs.get("x", 1450)), vs.get("state", "awake"), float(vs.get("scale", 0.8)))
        S = {"t0": t0, "bg": bg, "heroes": heroes, "villain": v, "music": sc.get("music", "drone")}
        self.scenes.append(S)
        # retention: the very first frame must already be moving (no fade-in on scene 0)
        S["fin"] = 0.0 if i == 0 else 0.4
        self.t += S["fin"]  # fade in
        prev_start = end = self.t
        for j, b in enumerate(sc.get("beats", [])):
            start = prev_start if b.get("and") else end
            self.t = start
            prev_start = start
            try:
                d = self.beat(S, b)
            except Exception as e:  # keep going, report
                self.err(f"scene {i} beat {j}: {e}")
                d = 0
            end = max(end, start + d)
            self.t = end
        self.t += float(sc.get("tail", 0.6))
        S["t1"] = self.t
        # Shorts loop: no fade-out to black after the last scene
        last = i == len(self.s.get("scenes", [])) - 1
        S["fout"] = 0.0 if (last and self.s.get("format") == "short") else 0.35
        self.t += S["fout"]  # fade out

    # ------------------------------------------------------------------
    def who(self, S, k):
        if k == "villain":
            if not S["villain"]:
                raise ValueError("no villain in this scene")
            return S["villain"]
        if k not in S["heroes"]:
            raise ValueError(f"'{k}' is not in this scene (add it to scene.heroes)")
        return S["heroes"][k]

    def beat(self, S, b):
        t = self.t
        if "say" in b:
            k = b["say"]
            if k == "narr":
                spk = "narr"
            elif k == "villain":
                spk = S["villain"].type if S["villain"] else None
                if not spk:
                    raise ValueError("villain speaks but scene has no villain")
            else:
                self.who(S, k); spk = k
            if not b.get("en"):
                raise ValueError("say needs 'en'")
            a = A.voice(spk, b["en"], self.wd)
            dur = len(a) / A.SR
            self.snd(a, t, 1.15 if k == "villain" else 1.0)
            if k != "narr":
                self.talk.append((t, dur, k, self.env(a)))
            missing = [l for l in SUB_LANGS if not b.get(l)]
            if missing:
                self.err(f"line '{b['en'][:30]}' missing subtitles: {missing}")
            self.subs.append((t, t + dur + 0.3, {l: b.get(l, "") for l in SUB_LANGS}))
            return dur + float(b.get("gap", 0.3))

        if "move" in b:
            k = b["move"]; a = self.who(S, k)
            x0 = a.final_x()
            to = b.get("to", 960)
            to = {"off_left": -350, "off_right": 2270}.get(to, to)
            sp = RUN if b.get("speed") == "run" else WALK
            d = max(0.3, abs(float(to) - x0) / sp)
            kind = "run" if b.get("speed") == "run" else "walk"
            a.seg.append((t, t + d, x0, float(to), kind))
            if k != "villain":
                period = 0.12 if kind == "run" else 0.32
                for n in range(int(d / period)):
                    self.snd(A.step(), t + n * period, 1.0)
                if kind == "run":
                    self.snd(A.whoosh(), t, 0.4)
            return d

        if "act" in b:
            ks = b["act"] if isinstance(b["act"], list) else [b["act"]]
            do = b.get("do", "jump")
            dur = {"jump": 0.6, "shake": 1.0, "scream": 0.0, "faint": 1.2, "spin": 0.8, "hide": 0.3, "show": 0.3, "bounce": 1.0}.get(do)
            if dur is None:
                raise ValueError(f"unknown act '{do}'")
            for n, k in enumerate(ks):
                a = self.who(S, k)
                if do == "scream":
                    if k == "villain":
                        raise ValueError("use villain: roar")
                    v = A.voice(k, SCREAMS[k], self.wd)
                    d = len(v) / A.SR
                    self.snd(v, t + n * 0.07, 0.9)
                    a.events.append((t, t + d + 0.3, "scream"))
                    dur = max(dur, d + 0.3)
                elif do in ("hide", "show"):
                    a.hidden.append((t + 0.15, do == "hide"))
                    self.snd(A.pop(), t, 0.8)
                else:
                    a.events.append((t, t + dur, do))
                    if do == "jump":
                        self.snd(A.boing(), t, 0.7)
                    if do == "faint":
                        self.snd(A.thump(), t + 0.8, 0.5)
            return dur

        if "mood" in b:
            ks = b["mood"] if isinstance(b["mood"], list) else [b["mood"]]
            if b.get("is") not in ("normal", "scared", "happy", "angry"):
                raise ValueError("mood 'is' must be normal/scared/happy/angry")
            for k in ks:
                self.who(S, k).mood.append((t, b["is"]))
            return 0

        if "villain" in b:
            v = S["villain"]
            if not v:
                raise ValueError("scene has no villain")
            do = b["villain"]
            if do == "wake":
                v.awake.append((t, True, t)); self.snd(A.creak(), t, 0.5); return 1.0
            if do == "sleep":
                v.awake.append((t, False, t)); return 0.8
            if do == "roar":
                v.events.append((t, t + 1.8, "roar")); v.rage.append((t, 1.0)); v.rage.append((t + 1.8, 0.4))
                self.snd(A.roar(2.0), t, 0.8); self.snd(A.rattle(1.2), t, 0.5)
                self.shakes.append((t, 1.4, 18)); return 1.8
            if do == "rage":
                v.rage.append((t, float(b.get("level", 1.0)))); return 0
            if do == "lunge":
                x0 = v.final_x(); tx = float(b.get("to", x0 - 350))
                v.seg.append((t, t + 0.35, x0, tx, "lunge")); v.seg.append((t + 0.35, t + 1.1, tx, x0, "lunge_back"))
                self.snd(A.whoosh(0.5), t, 0.6); self.shakes.append((t + 0.3, 0.4, 14)); return 1.1
            if do == "show":
                v.hidden.append((t, False)); v.awake.append((t, True, t)); self.snd(A.sting(), t, 0.6); return 0.8
            if do == "hide":
                v.hidden.append((t + 0.3, True)); self.snd(A.whoosh(0.6), t, 0.6); return 0.6
            raise ValueError(f"unknown villain action '{do}'")

        if "sfx" in b:
            name = b["sfx"]
            if name not in A.SFX:
                raise ValueError(f"unknown sfx '{name}'. Options: {list(A.SFX)}")
            self.snd(A.SFX[name](), t, float(b.get("gain", 1.0)))
            if name == "thump":
                self.shakes.append((t, 0.5, 20))
            return float(b.get("wait", 0))

        if "wait" in b:
            return float(b["wait"])

        if "shake" in b:
            self.shakes.append((t, float(b["shake"]), float(b.get("power", 18))))
            return 0

        if "card" in b:
            dur = float(b.get("dur", 3.0))
            self.cards.append((t, t + dur, b["card"], b.get("es", "")))
            if b.get("es"):
                self.subs.append((t + 0.3, t + dur, {"es": b["es"]}))
            if b.get("sting", True):
                self.snd(A.sting(), t, 0.8)
            return dur

        raise ValueError(f"unknown beat {list(b)}")


# ======================================================================
#   2. Frame rendering
# ======================================================================
C = None  # compiled timeline (set in worker)
CAM = None


def scene_at(t):
    cur = C.scenes[0]
    for S in C.scenes:
        if S["t0"] <= t:
            cur = S
    return cur


def talking(t):
    for t0, d, who, env in C.talk:
        if t0 <= t < t0 + d:
            i = int((t - t0) * FPS)
            return who, env[min(i, len(env) - 1)]
    return None, 0.0


def event_at(a, t):
    for t0, t1, k in a.events:
        if t0 <= t < t1:
            return k, (t - t0) / (t1 - t0)
    return None, 0


def draw_world(t, rnd):
    S = scene_at(t)
    out = [background(S["bg"])]
    # dust
    for i in range(30):
        r = random.Random(i)
        x = r.uniform(0, 1920) + math.sin(t + i) * 10
        y = (r.uniform(0, 780) + t * 12 * (1 + i % 3)) % 780
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1,3):.1f}" fill="#d8c8a0" opacity="0.2"/>')
    speaker, amp = talking(t)
    v = S["villain"]
    vx = None
    if v and not v.last(v.hidden, t):
        vx, _ = v.x_at(t)
        aw = v.awake[0]
        for a in v.awake:
            if a[0] <= t:
                aw = a
        awake, ts = aw[1], aw[2]
        p = ease((t - ts) / 0.6)
        eyes = p if awake else 1 - p
        if awake and int(t * 3) % 17 == 0 and (t * 3) % 1 < 0.4:
            eyes = 0.1
        blink = 1 - eyes
        rage = v.last(v.rage, t)
        ev, _ = event_at(v, t)
        if ev == "roar":
            mouth = "roar"
        elif speaker == "villain":
            mouth = float(amp)
        else:
            mouth = "grin" if eyes > 0.5 else "closed"
        # look at nearest hero
        hx = [h.x_at(t)[0] for h in S["heroes"].values() if not h.last(h.hidden, t)]
        look = (0, 0.2)
        if hx:
            nearest = min(hx, key=lambda q: abs(q - vx))
            look = (-1 if nearest < vx else 1, 0.3)
        vy = 795 - 200 * v.scale
        if eyes > 0.05:
            out.append(f'<circle cx="{vx}" cy="{vy}" r="{480*v.scale/0.72}" fill="url(#vg_{v.type})" opacity="{eyes*(0.75+0.25*math.sin(t*3)):.2f}"/>')
        op = 0.5 + 0.5 * eyes
        out.append(f'<g opacity="{op:.2f}">' + VDRAW[v.type](vx, vy, scale=v.scale, look=look, blink=blink,
                                                          mouth=mouth, rage=rage, t=t) + "</g>")
    for idx, (k, a) in enumerate(S["heroes"].items()):
        if a.last(a.hidden, t):
            continue
        x, mv = a.x_at(t)
        mood = a.last(a.mood, t)
        ev, ep = event_at(a, t)
        y, rot, step, arms, shiver, squash = HERO_Y, 0.0, 0.0, 0.0, 0.0, 0.0
        mouth = BASE_MOUTH[k]
        scared = angry = False
        if mood == "scared":
            scared, mouth, arms, shiver = True, "wobble", 0.3, rnd.uniform(-1.2, 1.2)
        elif mood == "happy":
            mouth = "smile" if k != "lolly" else "grin"
        elif mood == "angry":
            angry, mouth = True, "flat"
        if mv == "walk":
            step = math.sin(t * 9 + idx); y -= abs(math.sin(t * 9 + idx)) * 10
        elif mv == "run":
            step = math.sin(t * 22 + idx); y -= abs(math.sin(t * 22 + idx)) * 18
            seg_dir = [s for s in a.seg if s[0] <= t][-1]
            rot = -12 if seg_dir[3] < seg_dir[2] else 12
            arms = 1.0
        # look
        if speaker and speaker != k:
            sx = None
            if speaker == "villain" and vx is not None:
                sx = vx
            elif speaker in S["heroes"]:
                sx = S["heroes"][speaker].x_at(t)[0]
            look = ((1 if sx > x else -1), 0) if sx is not None else (0.3, 0)
        elif vx is not None and (mood == "scared" or mv == "run"):
            look = (1 if vx > x else -1, 0.1)
        else:
            look = (0.3, 0)
        if speaker == k:
            mouth = "scream" if amp > 0.55 else ("o" if amp > 0.15 else mouth)
        if ev == "jump":
            y -= math.sin(ep * math.pi) * 130; squash = -0.1 * math.sin(ep * math.pi)
        elif ev == "shake":
            shiver = rnd.uniform(-4, 4); scared = True
        elif ev == "scream":
            mouth, arms, scared = "scream", 1.0, True
            y -= abs(math.sin(ep * 12)) * 30
        elif ev == "faint":
            rot = 85 * ease(ep * 2); y += 50 * ease(ep * 2); mouth = "flat"
        elif ev == "spin":
            rot = 360 * ease(ep)
        elif ev == "bounce":
            y -= abs(math.sin(ep * math.pi * 3)) * 50; mouth = "smile"
        blink = 1.0 if (int(t * 10 + idx * 7) % 41 == 0) else 0.0
        out.append(dough(k, x, y, scale=0.95, look=look, mouth=mouth, step=step, scared=scared, angry=angry,
                         arms_up=arms, shiver=shiver, rot=rot, squash=squash, blink=blink))
    return "".join(out), S


def overlays(t, W, H):
    o = []
    # fade at scene boundaries
    for S in C.scenes:
        fi_, fo_ = S.get("fin", 0.4), S.get("fout", 0.35)
        if fi_ and S["t0"] <= t < S["t0"] + fi_:
            o.append(f'<rect width="{W}" height="{H}" fill="#000" opacity="{1-ease((t-S["t0"])/fi_):.2f}"/>')
        if fo_ and S["t1"] <= t < S["t1"] + fo_:
            o.append(f'<rect width="{W}" height="{H}" fill="#000" opacity="{ease((t-S["t1"])/fo_):.2f}"/>')
    if C.scenes[-1].get("fout", 0.35) and t >= C.scenes[-1]["t1"] + 0.35:
        o.append(f'<rect width="{W}" height="{H}" fill="#000"/>')
    for t0, t1, en, es in C.cards:
        if t0 - 0.3 <= t < t1:
            a = ease((t - t0 + 0.3) / 0.4)
            o.append(f'<rect width="{W}" height="{H}" fill="#050101" opacity="{a:.2f}"/>')
            b = ease((t - t0) / 0.6)
            sz = 130 if W > H else 110
            lines = wrap(en, 16 if W > H else 11)
            y0 = H / 2 - (len(lines) - 1) * sz * 0.55
            for n, ln in enumerate(lines):
                o.append(f'<g opacity="{b:.2f}">' + bold_text(W / 2, y0 + n * sz * 1.1, ln, sz, fill="#f2d27a", stroke=8) + '</g>')
    return "".join(o)


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def shake_at(t):
    p = 0
    for t0, d, pw in C.shakes:
        if 0 <= t - t0 < d:
            p += pw * (1 - (t - t0) / d)
    return p


DEFS = None


def frame(fi):
    t = fi / FPS
    rnd = random.Random(fi)
    world, S = draw_world(t, rnd)
    sh = shake_at(t)
    sx, sy = rnd.uniform(-sh, sh), rnd.uniform(-sh, sh)
    if C.fmt == "long":
        W, H = 1920, 1080
        z = 1 + 0.03 * clamp((t - S["t0"]) / 20)
        body = (f'<g transform="translate({960+sx},{560+sy}) scale({z}) translate(-960,-560)">{world}</g>'
                f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
        hook, hd = C.s.get("hook", ""), float(C.s.get("hook_dur", 3.5))
        if hook and t < hd:
            a = 1.0 if t < hd - 0.4 else max(0.0, (hd - t) / 0.4)
            hl = wrap(hook.upper(), 18)
            body += (f'<g opacity="{a:.2f}"><rect x="0" y="0" width="{W}" height="{90 + 150 * len(hl)}" fill="url(#fadeUp)"/>'
                     + "".join(bold_text(960, 150 + n * 140, l, 128, stroke=14) for n, l in enumerate(hl)) + '</g>')
    else:
        W, H = 1080, 1920
        k = 1.3
        cam = CAM[min(fi, len(CAM) - 1)]
        tx, ty = 540 - k * cam + sx, 1820 - k * 1080 + sy
        hook = C.s.get("hook", "")
        hl = wrap(hook.upper(), 14)
        hook_svg = "".join(bold_text(540, 230 + n * 118, l, 108, stroke=14) for n, l in enumerate(hl))
        body = (f'<rect width="{W}" height="{H}" fill="#070303"/>'
                f'<g transform="translate({tx},{ty}) scale({k})">{world}'
                f'<rect x="-2000" y="1080" width="6000" height="1200" fill="#0a0303"/></g>'
                f'<rect x="0" y="0" width="{W}" height="460" fill="url(#fadeUp)"/>'
                f'{hook_svg}')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}'
           f'{body}{overlays(t, W, H)}</svg>')
    return cairosvg.svg2png(bytestring=svg.encode())


def init_worker(c, cam):
    global C, CAM, DEFS
    C, CAM = c, cam
    DEFS = ("<defs>" + char_defs()[6:-7] + villain_defs() + bg_defs() +
            '<linearGradient id="fadeDown" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0a0303" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#0a0303"/></linearGradient>'
            '<linearGradient id="fadeUp" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#070303"/>'
            '<stop offset="60%" stop-color="#070303" stop-opacity="0.85"/><stop offset="100%" stop-color="#070303" stop-opacity="0"/></linearGradient>'
            + glow_defs() + '</defs>')


def glow_defs():
    return "".join(f'<radialGradient id="vg_{k}" r="50%"><stop offset="0%" stop-color="{c}" stop-opacity="0.5"/>'
                   f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/></radialGradient>' for k, c in GLOW.items())


def camera_track(c, n):
    """smoothed horizontal camera for vertical shorts"""
    global C
    C = c
    cam, cur = [], None
    for fi in range(n):
        t = fi / FPS
        S = scene_at(t)
        sp, _ = talking(t)
        xs = []
        if sp == "villain" and S["villain"]:
            xs = [S["villain"].x_at(t)[0] - 60]
        elif sp in S["heroes"]:
            xs = [S["heroes"][sp].x_at(t)[0]]
        else:
            xs = [h.x_at(t)[0] for h in S["heroes"].values() if -100 < h.x_at(t)[0] < 2000]
            if S["villain"] and not S["villain"].last(S["villain"].hidden, t):
                xs.append(S["villain"].x_at(t)[0])
        target = sum(xs) / len(xs) if xs else 960
        target = clamp(target, 420, 1500)
        if cur is None or (S["t0"] <= t < S["t0"] + 1 / FPS):
            cur = target
        cur += (target - cur) * 0.06
        cam.append(cur)
    return cam


# ======================================================================
#   3. Audio mix, subtitles, thumbnail, upload text
# ======================================================================
def build_audio(c, path):
    n = int(c.total * A.SR) + A.SR
    mix = np.zeros(n, dtype=np.float32)

    def put(sig, at, g):
        i = int(at * A.SR)
        if i >= n:
            return
        sig = sig[: n - i]
        mix[i:i + len(sig)] += sig * g

    for S in c.scenes:
        d = S["t1"] - S["t0"] + 0.4
        m = S["music"]
        if m == "drone":
            put(A.drone(d).astype(np.float32), S["t0"], 1.0)
        elif m == "heartbeat":
            put(A.drone(d).astype(np.float32), S["t0"], 0.8); put(A.heartbeat(d).astype(np.float32), S["t0"], 0.9)
        elif m == "music_box":
            put(A.music_box(d).astype(np.float32), S["t0"], 1.0); put(A.drone(d, 49).astype(np.float32), S["t0"], 0.6)
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
    bg = th.get("bg", "kitchen")
    vt = th.get("villain")
    heroes = th.get("heroes", ["bup", "pim"])
    text = th.get("text", script.get("hook", "DOUGH BROS"))
    g = [background(bg), '<rect width="1920" height="1080" fill="#000" opacity="0.25"/>']
    if vt:
        g.append(f'<circle cx="1400" cy="520" r="700" fill="url(#vg_{vt})"/>')
        g.append(VDRAW[vt](1400, 560, scale=1.15, look=(-1, 0.3), blink=0, mouth="roar", rage=1.0, t=0.3))
    for i, h in enumerate(heroes[:3]):
        g.append(dough(h, 260 + i * 290, 720 - (i % 2) * 40, scale=1.35, look=(1, 0), mouth="scream",
                       scared=True, arms_up=1.0, rot=(-8 if i % 2 else 6)))
    lines = wrap(text.upper(), 13)
    for n, l in enumerate(lines[:2]):
        g.append(bold_text(60, 200 + n * 180, l, 170, stroke=22, anchor="start"))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
           f'<defs>{char_defs()[6:-7]}{villain_defs()}{bg_defs()}{glow_defs()}</defs>{"".join(g)}'
           f'<rect width="1920" height="1080" fill="url(#vign)" opacity="0.6"/></svg>')
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, output_width=1280, output_height=720)


def upload_txt(script, path, dur):
    s = script
    tags = ", ".join(s.get("tags", []))
    txt = (f"TITLE:\n{s.get('title','')}\n\nDESCRIPTION:\n{s.get('description','')}\n\nTAGS:\n{tags}\n\n"
           f"LENGTH: {dur:.0f}s   FORMAT: {s.get('format')}\n"
           "AUDIENCE: Not made for kids (general audience)\nSUBTITLES: upload subs_es/de/fr/it/pt.srt in YouTube Studio > Subtitles\n")
    open(path, "w", encoding="utf-8").write(txt)


# ======================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out", default=None)
    ap.add_argument("--preview", nargs="*", type=float, help="render still PNGs at these seconds only")
    ap.add_argument("--check", action="store_true", help="validate script, build audio timing, no video")
    args = ap.parse_args()

    script = json.load(open(args.script, encoding="utf-8"))
    sid = script.get("id") or os.path.splitext(os.path.basename(args.script))[0]
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", sid)
    os.makedirs(out, exist_ok=True)
    wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "_voicecache")
    os.makedirs(wd, exist_ok=True)

    c = Compiler(script, wd).compile()
    c.fmt = script.get("format", "long")
    print(f"[{sid}] duration {c.total:.1f}s, scenes {len(c.scenes)}, lines {len(c.talk)}")
    if c.errors:
        print("PROBLEMS:"); [print("  -", e) for e in c.errors]
        hard = [e for e in c.errors if "missing subtitles" not in e]
        if hard:
            sys.exit(2)
    if args.check:
        return
    n = int(c.total * FPS)
    cam = camera_track(c, n) if c.fmt == "short" else [960] * n
    if args.preview is not None:
        init_worker(c, cam)
        for sec in args.preview:
            open(os.path.join(out, f"preview_{sec:g}.png"), "wb").write(frame(int(sec * FPS)))
        print("previews in", out); return

    build_audio(c, os.path.join(out, "audio.wav"))
    for l in SUB_LANGS:
        write_srt(c, l, os.path.join(out, f"subs_{l}.srt"))
    thumbnail(script, os.path.join(out, "thumbnail.png"))
    upload_txt(script, os.path.join(out, "upload.txt"), c.total)

    c.sounds = []  # not needed by frame workers
    raw = os.path.join(out, "_video.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", raw], stdin=subprocess.PIPE)
    with Pool(os.cpu_count() or 2, initializer=init_worker, initargs=(c, cam)) as p:
        for i, png in enumerate(p.imap(frame, range(n), chunksize=6)):
            ff.stdin.write(png)
            if i % 240 == 0:
                print(f"  frame {i}/{n}", flush=True)
    ff.stdin.close(); ff.wait()

    fs = (13, 1.6, 18) if c.fmt == "long" else (8, 1.2, 28)
    style = (f"FontName=DejaVu Sans,Bold=1,FontSize={fs[0]},PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
             f"BorderStyle=1,Outline={fs[1]},Shadow=0.8,MarginV={fs[2]}")
    srt = os.path.join(out, "subs_es.srt").replace("\\", "/").replace(":", "\\:")
    final = os.path.join(out, f"{sid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", os.path.join(out, "audio.wav"),
                    "-vf", f"subtitles='{srt}':force_style='{style}'",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    os.remove(raw)
    print("DONE", final)


if __name__ == "__main__":
    main()

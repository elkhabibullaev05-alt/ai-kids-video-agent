"""Doodle Desk renderer: JSON script -> narrated hand-drawn explainer video (1920x1080) + thumbnail + upload.txt.

    python3 engine/render.py scripts/ep001.json --check      # validate, voice it, print duration
    python3 engine/render.py scripts/ep001.json --preview 3  # still frames of every 3rd scene to out/<id>/preview_*.png
    python3 engine/render.py scripts/ep001.json              # full render
"""
import argparse
import hashlib
import json
import math
import os
import random
import subprocess
import sys

import numpy as np
import soundfile as sf
import cairocffi as cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ink  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODELS = os.path.join(ROOT, "models")
FPS = 12
SR = 24000
GAP = 0.28

_kok = None


def kokoro():
    global _kok
    if _kok is None:
        from kokoro_onnx import Kokoro
        _kok = Kokoro(os.path.join(MODELS, "kokoro.onnx"), os.path.join(MODELS, "voices.bin"))
    return _kok


def tts(text, voice, speed, work):
    key = hashlib.md5(f"{voice}|{speed}|{text}".encode()).hexdigest()[:14]
    out = os.path.join(work, f"v_{key}.wav")
    if not os.path.exists(out):
        a, sr = kokoro().create(text, voice=voice, speed=speed, lang="en-us")
        if sr != SR:
            raise RuntimeError("unexpected sample rate")
        sf.write(out, a, SR)
    a, _ = sf.read(out)
    nz = np.where(np.abs(a) > 0.008)[0]
    if len(nz):
        a = a[max(0, nz[0] - int(0.03 * SR)): nz[-1] + int(0.06 * SR)]
    return a.astype(np.float32)


# ----------------------------------------------------------------------------- audio beds
def music_bed(dur, seed=1):
    """Light, unobtrusive plucked loop (C major-ish) so the narration never sits in silence."""
    rng = random.Random(seed)
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    bpm = 96
    beat = 60 / bpm
    prog = [[60, 64, 67], [57, 60, 64], [65, 69, 72], [55, 59, 62]]
    t = 0.0
    k = 0
    while t < dur:
        chord = prog[(k // 8) % 4]
        note = chord[rng.randrange(3)] + (12 if rng.random() < 0.25 else 0)
        f = 440 * 2 ** ((note - 69) / 12)
        L = int(beat * 1.6 * SR)
        tt = np.arange(L) / SR
        tone = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 4.5)
        i0 = int(t * SR)
        i1 = min(n, i0 + L)
        out[i0:i1] += tone[: i1 - i0].astype(np.float32) * (0.5 if k % 2 else 0.35)
        if k % 8 == 0:  # soft bass
            fb = f / 4
            Lb = int(beat * 4 * SR)
            tb = np.arange(Lb) / SR
            b = np.sin(2 * np.pi * fb * tb) * np.exp(-tb * 1.2)
            j1 = min(n, i0 + Lb)
            out[i0:j1] += b[: j1 - i0].astype(np.float32) * 0.5
        t += beat / 2
        k += 1
    out /= max(1e-6, np.abs(out).max())
    return out * 0.055


def pop_sfx():
    L = int(0.09 * SR)
    t = np.arange(L) / SR
    return (np.sin(2 * np.pi * (500 + 900 * t / 0.09) * t) * np.exp(-t * 45) * 0.12).astype(np.float32)


def whoosh_sfx():
    L = int(0.35 * SR)
    t = np.arange(L) / SR
    nz = np.random.RandomState(3).randn(L)
    env = np.sin(np.pi * t / 0.35) ** 2
    k = np.ones(40) / 40
    return (np.convolve(nz, k, "same") * env * 0.06).astype(np.float32)


# ----------------------------------------------------------------------------- timeline
def chunks(text, n=7):
    words = text.split()
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= n or (w[-1] in ".?!" and len(cur) >= 3):
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def build_timeline(script, work):
    voice = script.get("voice", "am_michael")
    speed = float(script.get("speed", 1.0))
    t = 0.0
    scenes = []
    for i, sc in enumerate(script["scenes"]):
        a = tts(sc["say"], voice, speed, work)
        d = len(a) / SR
        dur = d + float(sc.get("hold", GAP))
        caps = []
        cs = chunks(sc["say"])
        tot = sum(len(c) for c in cs) or 1
        ct = 0.0
        for c in cs:
            cd = d * len(c) / tot
            caps.append((t + ct, t + ct + cd, c))
            ct += cd
        scenes.append({"i": i, "t0": t, "t1": t + dur, "dur": dur, "audio": a, "sc": sc, "caps": caps})
        t += dur
    return scenes, t


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def back(x):
    x = max(0.0, min(1.0, x))
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


# ----------------------------------------------------------------------------- drawing
_paper = None


def paper_surface():
    global _paper
    if _paper is None:
        rs = np.random.RandomState(7)
        noise = rs.normal(0, 1, (ink.H // 4, ink.W // 4)).astype(np.float32)
        noise = np.kron(noise, np.ones((4, 4), np.float32))
        base = np.array(ink.PAPER, np.float32) * 255
        img = np.clip(base[None, None, :] + noise[..., None] * 3.0, 0, 255).astype(np.uint8)
        bgra = np.dstack([img[..., 2], img[..., 1], img[..., 0], np.full(img.shape[:2], 255, np.uint8)])
        data = bytearray(bgra.tobytes())
        _paper = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, ink.W, ink.H, ink.W * 4)
        _paper._keep = data
    return _paper


def item_time(it, sc_dur):
    at = float(it.get("at", 0.0))
    return at * sc_dur if at <= 1.0 else at


def draw_item(p, it, lt, sc_dur, gt):
    """lt: local time in the scene, gt: global time."""
    t_in = item_time(it, sc_dur)
    if lt < t_in:
        return False
    until = it.get("until")
    if until is not None and lt > (until * sc_dur if until <= 1.0 else until):
        return False
    k = lt - t_in
    mode = it.get("in", "pop")
    c = p.c
    c.save()
    x, y = it.get("x", 960), it.get("y", 900)
    if "move" in it:  # glide to a new position over the scene
        mx, my = it["move"]
        f = ease((lt - t_in) / max(0.5, sc_dur - t_in))
        x, y = x + (mx - x) * f, y + (my - y) * f
    sc = 1.0
    if mode == "pop":
        sc = back(k / 0.38) if k < 0.38 else 1.0
    elif mode in ("slide_l", "slide_r"):
        f = ease(k / 0.5)
        x += (1 - f) * (-1300 if mode == "slide_l" else 1300)
    elif mode == "drop":
        f = back(k / 0.5) if k < 0.5 else 1.0
        y -= (1 - f) * 700
    anim = it.get("anim")
    rot = 0.0
    if anim == "bob":
        y += math.sin(gt * 2.4) * 8
    elif anim == "shake":
        x += math.sin(gt * 40) * 5
        rot = math.sin(gt * 33) * 0.03
    elif anim == "pulse":
        sc *= 1 + 0.05 * math.sin(gt * 6)
    elif anim == "spin":
        rot = gt * 1.5
    pivot_y = y - (150 if ("guy" in it or "prop" in it) else 0)
    c.translate(x, pivot_y)
    c.scale(max(0.001, sc), max(0.001, sc))
    if rot:
        c.rotate(rot)
    c.translate(-x, -pivot_y)
    if "guy" in it:
        g = it["guy"]
        ink.guy(p, x, y, it.get("s", 1.0), g.get("pose", "stand"), g.get("face", "neutral"), g.get("look", 1), gt + it.get("x", 0) * 0.01,
                g.get("extras", ()), g.get("shirt"), g.get("walk", False), g.get("label"))
    elif "prop" in it:
        ink.prop(p, it["prop"], x, y, it.get("s", 1.0), gt, it.get("color"), it.get("text"))
    elif "text" in it:
        p.text(it["text"], x, y, it.get("size", 80), it.get("color", "black"), it.get("align", "center"),
               "Kalam", True, it.get("outline"))
    elif "count" in it:
        a, b = it["count"]
        f = ease(k / it.get("dur", 1.4))
        v = a + (b - a) * f
        p.text(it.get("fmt", "{:,.0f}").format(v), x, y, it.get("size", 110), it.get("color", "red"), "center", "Kalam", True, it.get("outline"))
    elif "arrow" in it:
        (x1, y1), (x2, y2) = it["arrow"]
        f = ease(k / 0.45)
        ex, ey = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
        p.line([(x1, y1), (ex, ey)], it.get("w", 7), it.get("color"))
        if f > 0.95:
            a = math.atan2(y2 - y1, x2 - x1)
            for s_ in (2.6, -2.6):
                p.line([(x2, y2), (x2 + 34 * math.cos(a + s_), y2 + 34 * math.sin(a + s_))], it.get("w", 7), it.get("color"))
    elif "cross" in it:
        cx, cy, r = it["cross"]
        f = ease(k / 0.3)
        p.line([(cx - r, cy - r), (cx - r + 2 * r * f, cy - r + 2 * r * f)], 14, "red")
        if f >= 1:
            g2 = ease((k - 0.3) / 0.3)
            p.line([(cx + r, cy - r), (cx + r - 2 * r * g2, cy - r + 2 * r * g2)], 14, "red")
    elif "ring" in it:
        cx, cy, r = it["ring"]
        f = ease(k / 0.5)
        p.arc(cx, cy, r, -1.8, -1.8 + 2 * math.pi * f * 1.05, 8, "red")
    elif "bars" in it:
        bb = it["bars"]
        vals, labels = bb["values"], bb.get("labels", [])
        bw, bh = bb.get("w", 700), bb.get("h", 420)
        vmax = max(vals) or 1
        n = len(vals)
        gap = bw / n
        p.line([(x - bw / 2, y), (x + bw / 2, y)], 5)
        for i, v in enumerate(vals):
            f = ease((k - i * 0.25) / 0.6)
            hh = bh * v / vmax * f
            cx = x - bw / 2 + gap * (i + 0.5)
            p.rect(cx - gap * 0.32, y - hh, gap * 0.64, max(1, hh), (bb.get("colors") or ["blue"] * n)[i % len(bb.get("colors") or ["blue"])], 4)
            if f > 0.6:
                p.text(bb.get("fmt", "{}").format(v), cx, y - hh - 38, 46, "black")
            if i < len(labels):
                p.text(labels[i], cx, y + 40, 38, "dark", font="Patrick Hand", bold=False)
    elif "stamp" in it:
        c.save()
        c.translate(x, y)
        c.rotate(math.radians(it.get("angle", -12)))
        sc2 = 1.0 + max(0.0, 1 - k / 0.18) * 0.8
        c.scale(sc2, sc2)
        p.rect(-it.get("w", 380), -70, 2 * it.get("w", 380), 140, None, 10)
        p.text(it["stamp"], 0, 0, it.get("size", 96), "red")
        c.restore()
    elif "box" in it:
        bx, by, bw2, bh2 = it["box"]
        p.rect(bx, by, bw2, bh2, it.get("color", "white"), 5)
    c.restore()
    return k < 0.05 and mode != "none"


def draw_frame(ctx, scene, lt, gt, boil, caption, total, title_card=None):
    sc = scene["sc"]
    ctx.set_source_surface(paper_surface(), 0, 0)
    ctx.paint()
    bg = sc.get("bg")
    if bg and bg != "paper":
        r, g, b = ink.col(bg)
        ctx.set_source_rgba(r, g, b, 0.35)
        ctx.paint()
    p = ink.Pen(ctx, boil)
    cam = sc.get("cam") or {}
    f = ease(lt / max(0.1, scene["dur"]))
    c0 = cam.get("from", [960, 540, 1.0])
    c1 = cam.get("to", [960, 540, 1.045])
    cx = c0[0] + (c1[0] - c0[0]) * f
    cy = c0[1] + (c1[1] - c0[1]) * f
    z = c0[2] + (c1[2] - c0[2]) * f
    ctx.save()
    ctx.translate(960, 540)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)
    if sc.get("ground", True):
        p.line([(-200, 905), (2120, 905)], 4, "dark", 0.55)
    pops = []
    for it in sc.get("items", []):
        if draw_item(p, it, lt, scene["dur"], gt):
            pops.append(it)
    ctx.restore()
    if sc.get("chapter"):  # small chapter tag top-left
        p.rect(36, 30, 24 * len(sc["chapter"]) + 70, 66, "yellow", 4)
        p.text(sc["chapter"], 70, 63, 40, "black", align="left")
    if caption:
        ctx.select_font_face("Patrick Hand", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(54)
        xb, yb, tw, th, _, _ = ctx.text_extents(caption)
        bx, by = 960 - tw / 2 - 26, 1000 - 44
        ctx.set_source_rgba(0.08, 0.08, 0.08, 0.78)
        rr = 14
        ctx.new_sub_path()
        ctx.arc(bx + tw + 52 - rr, by + rr, rr, -math.pi / 2, 0)
        ctx.arc(bx + tw + 52 - rr, by + 70 - rr, rr, 0, math.pi / 2)
        ctx.arc(bx + rr, by + 70 - rr, rr, math.pi / 2, math.pi)
        ctx.arc(bx + rr, by + rr, rr, math.pi, 1.5 * math.pi)
        ctx.close_path()
        ctx.fill()
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(960 - tw / 2 - xb, 1000 - th / 2 - yb - 9)
        ctx.show_text(caption)
    # progress bar keeps people watching to the end
    ctx.set_source_rgba(0.86, 0.33, 0.27, 0.9)
    ctx.rectangle(0, 1074, ink.W * gt / max(1, total), 6)
    ctx.fill()
    return pops


# ----------------------------------------------------------------------------- thumbnail
def thumbnail(script, out_png):
    th = script.get("thumbnail", {})
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, ink.W, ink.H)
    c = cairo.Context(s)
    r, g, b = ink.col(th.get("bg", "yellow"))
    c.set_source_rgb(r, g, b)
    c.paint()
    p = ink.Pen(c, 3, amp=3.0)
    for it in th.get("items", []):
        fake = {"sc": {"items": []}, "dur": 1}
        draw_item(p, dict(it, **{"in": "none"}), 5, 1, 2.0)
    gd = th.get("guy", {"pose": "panic", "face": "scream"})
    ink.guy(p, th.get("guy_x", 1450), th.get("guy_y", 1060), th.get("guy_s", 1.9), gd.get("pose", "panic"), gd.get("face", "scream"), gd.get("look", -1), 0.5,
            gd.get("extras", ()), gd.get("shirt"))
    lines = th.get("text", "WAIT, WHAT?").split("|")
    for i, ln in enumerate(lines):
        p.text(ln, 560, 300 + i * 230, th.get("size", 200), th.get("color", "black"), outline="white")
    s.write_to_png(out_png + ".full.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out_png + ".full.png", "-vf", "scale=1280:720", out_png], check=True)
    os.remove(out_png + ".full.png")


# ----------------------------------------------------------------------------- main
def render(path, check=False, preview=0, limit=None):
    script = json.load(open(path))
    sid = script["id"]
    out = os.path.join(ROOT, "out", sid)
    work = os.path.join(ROOT, "out", "_voice")
    os.makedirs(out, exist_ok=True)
    os.makedirs(work, exist_ok=True)
    scenes, total = build_timeline(script, work)
    if limit:
        scenes = scenes[:limit]
        total = scenes[-1]["t1"]
    words = sum(len(s["sc"]["say"].split()) for s in scenes)
    print(f"{sid}: {len(scenes)} scenes, {words} words, {total / 60:.1f} min")
    if check:
        return
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, ink.W, ink.H)
    ctx = cairo.Context(surf)
    if preview:
        for s in scenes[int(os.environ.get('PREVIEW_START', 0))::preview]:
            lt = s["dur"] * 0.8
            cap = s["caps"][-1][2] if s["caps"] else None
            draw_frame(ctx, s, lt, s["t0"] + lt, 1, cap, total)
            surf.write_to_png(os.path.join(out, f"preview_{s['i']:03d}.png"))
        print("previews in", out)
        return
    # audio
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)
    for s in scenes:
        i0 = int(s["t0"] * SR)
        voice[i0:i0 + len(s["audio"])] += s["audio"]
        if s["sc"].get("whoosh", s["i"] > 0 and s["sc"].get("bg")):
            w = whoosh_sfx()
            sfx[i0:i0 + len(w)] += w[: max(0, min(len(w), n - i0))]
    music = music_bed(total + 1, seed=hash(sid) & 0xFFFF)[:n]
    # duck music under the voice
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, "same")
    duck = 1.0 - 0.55 * np.clip(env / 0.03, 0, 1)
    vid_path = os.path.join(out, "video_noaudio.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{ink.W}x{ink.H}",
                           "-r", str(FPS), "-i", "-", "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "21", vid_path], stdin=subprocess.PIPE)
    frames = int(total * FPS)
    si = 0
    pop = pop_sfx()
    for fi in range(frames):
        gt = fi / FPS
        while si < len(scenes) - 1 and gt >= scenes[si]["t1"]:
            si += 1
        s = scenes[si]
        lt = gt - s["t0"]
        cap = None
        for a, b, txt in s["caps"]:
            if a <= gt < b + 0.25:
                cap = txt
        pops = draw_frame(ctx, s, lt, gt, fi // 2, cap, total)
        if pops:
            i0 = int(gt * SR)
            sfx[i0:i0 + len(pop)] += pop[: max(0, min(len(pop), n - i0))]
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
        if fi % 600 == 0:
            print(f"  frame {fi}/{frames}", flush=True)
    ff.stdin.close()
    ff.wait()
    mix = voice * 1.0 + music * duck + sfx
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    wav = os.path.join(out, "mix.wav")
    sf.write(wav, mix, SR)
    final = os.path.join(out, f"{sid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid_path, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-af", "loudnorm=I=-15:TP=-1.5", "-shortest", "-movflags", "+faststart", final], check=True)
    os.remove(vid_path)
    # captions file for YouTube
    with open(os.path.join(out, "subs_en.srt"), "w") as f:
        k = 1
        for s in scenes:
            for a, b, txt in s["caps"]:
                def ts(x):
                    return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int((x % 1) * 1000):03d}"
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
                k += 1
    thumbnail(script, os.path.join(out, "thumbnail.png"))
    with open(os.path.join(out, "upload.txt"), "w") as f:
        f.write(f"TITLE: {script['title']}\n\nDESCRIPTION:\n{script.get('description', '')}\n\nTAGS: {', '.join(script.get('tags', []))}\n")
    print("done:", final, f"{total / 60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--preview", type=int, default=0)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    render(a.script, a.check, a.preview, a.limit)

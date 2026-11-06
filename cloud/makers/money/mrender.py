"""Money Story Daily — render one script JSON into a 1080x1920 30 fps Short.

render(script_dict, out_mp4, workdir) -> {"duration": s, "seconds_render": s}
Voice (Kokoro) from 0.0 s, animated PIL infographics, word-by-word captions, generated soft pad,
two-pass loudnorm to -14 LUFS, last 0.3 s cross-fades into frame 0 (seamless loop).
"""
import json
import math
import os
import re
import subprocess
import time

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter

import mvis as V
import mvoice

W, H, FPS = V.W, V.H, 30
SR = mvoice.SR
PANEL_Y = 430
CAP_Y = 1395            # caption centre line (bottom 20 % = y > 1536 stays clear)
CAP_W = 840

ACCENTS = {"green": "#0E9F6E", "red": "#E0472B", "blue": "#2563EB", "orange": "#EE7B11", "purple": "#7C3AED",
           "teal": "#0E8C96", "pink": "#DB2777", "gold": "#C98A06"}


def theme(script):
    acc = script.get("accent", "green")
    acc = ACCENTS.get(acc, acc if str(acc).startswith("#") else ACCENTS["green"])
    return {"bg": V.hexc("#F5EFE3"), "ink": V.hexc("#14213D"), "muted": V.hexc("#7A8291"),
            "soft": V.hexc("#E4DACA"), "accent": V.hexc(acc)}


# ---------------------------------------------------------------- audio
def _whoosh(dur=0.28, seed=0):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    x = rng.standard_normal(n).astype(np.float32)
    k = np.ones(24, np.float32) / 24
    x = np.convolve(x, k, "same")
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return (x * env * 0.5).astype(np.float32)


def _pop(dur=0.09):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * (900 - 3000 * t) * t) * np.exp(-t * 45) * 0.35).astype(np.float32)


def bed(total, scene_starts, seed=0):
    """Soft warm pad (slow chord changes, period == video length so the loop is seamless) + whooshes."""
    n = int(total * SR)
    t = np.arange(n) / SR
    chords = [(110.0, 164.81, 220.0, 277.18), (98.0, 146.83, 196.0, 246.94), (87.31, 130.81, 174.61, 220.0),
              (98.0, 146.83, 196.0, 293.66)]
    seg = total / 4
    pad = np.zeros(n, np.float32)
    for ci, ch in enumerate(chords):
        w = np.clip(1 - np.abs((t - (ci + 0.5) * seg) / seg) * 0.9, 0, 1) ** 1.5  # overlapping cross-fades
        w += np.clip(1 - np.abs((t - (ci + 0.5) * seg + total) / seg) * 0.9, 0, 1) ** 1.5 if ci == 3 else 0
        w += np.clip(1 - np.abs((t - (ci + 0.5) * seg - total) / seg) * 0.9, 0, 1) ** 1.5 if ci == 0 else 0
        for j, f in enumerate(ch):
            pad += (w * (np.sin(2 * np.pi * f * t + j) + 0.35 * np.sin(2 * np.pi * f * 1.004 * t))).astype(np.float32) / (j + 1.5)
    lfo = 0.8 + 0.2 * np.sin(2 * np.pi * t * 4 / total)
    pad = pad * lfo
    pad = pad / (np.abs(pad).max() + 1e-9) * 0.075
    for i, s in enumerate(scene_starts[1:], 1):
        w = _whoosh(seed=seed + i)
        a = int(max(0, s - 0.12) * SR)
        b = min(n, a + len(w))
        pad[a:b] += w[: b - a] * 0.22
    return pad


def _ff(args, **kw):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-y"] + args, capture_output=True, text=True, **kw)


def loudnorm_args(wav):
    r = _ff(["-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.findall(r"\{[^{}]*\}", r.stderr, re.S)
    j = json.loads(m[-1])
    return ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:"
            "measured_thresh={input_thresh}:offset={target_offset}:linear=true".format(**j))


# ---------------------------------------------------------------- captions
def chunks(words, maxw=CAP_W, size=84):
    f = V.font(size)
    out, cur = [], []
    for w in words:
        test = " ".join(x["w"] for x in cur + [w])
        if cur and (len(cur) >= 3 or f.getlength(test) > maxw):
            out.append(cur)
            cur = []
        cur.append(w)
        if w["w"][-1:] in ".,!?;:":
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def draw_caption(d, chs, t, th):
    if not chs:
        return
    cur = None
    for c in chs:
        if t >= c[0]["t0"] - 0.05:
            cur = c
    if cur is None:
        cur = chs[0]
    words = [w["w"] for w in cur]
    size = 84
    while size > 52 and V.font(size).getlength(" ".join(words)) > CAP_W:
        size -= 4
    f = V.font(size)
    sp = f.getlength(" ")
    total = sum(f.getlength(w) for w in words) + sp * (len(words) - 1)
    x = V.CX - total / 2
    for w in cur:
        ww = f.getlength(w["w"])
        active = w["t0"] - 0.03 <= t < w["t1"] + 0.03
        if active:
            d.rounded_rectangle([x - 14, CAP_Y - size * 0.72, x + ww + 14, CAP_Y + size * 0.62], radius=20, fill=th["accent"])
            d.text((x, CAP_Y), w["w"], font=f, fill=th["bg"], anchor="lm")
        else:
            d.text((x, CAP_Y), w["w"], font=f, fill=th["ink"], anchor="lm")
        x += ww + sp


# ---------------------------------------------------------------- hook / header
def _hook_layout(text, th):
    f, lines = V.wrap(text.upper(), V.X1 - V.X0, 124, maxlines=3, minsize=70)
    return f, lines


def draw_hook(img, d, text, t, th):
    f, lines = _hook_layout(text, th)
    lh = f.size * 1.16
    y0 = 250
    key = None
    for l in lines:
        for w in l.split():
            if key is None and re.search(r"[\d$]", w):
                key = w
    pulse = 1 + 0.035 * math.sin(t * 7) if t > 0.2 else 1.0
    for i, l in enumerate(lines):
        y = y0 + lh * (i + 0.5)
        sp = f.getlength(" ")
        tot = f.getlength(l)
        x = V.CX - tot / 2
        for w in l.split():
            ww = f.getlength(w)
            if w == key:
                pad = 14 * pulse
                d.rounded_rectangle([x - pad, y - f.size * 0.62 - pad / 2, x + ww + pad, y + f.size * 0.55 + pad / 2],
                                    radius=22, fill=th["accent"])
                d.text((x, y), w, font=f, fill=th["bg"], anchor="lm")
            else:
                d.text((x, y), w, font=f, fill=th["ink"], anchor="lm")
            x += ww + sp
    return y0 + lh * len(lines) + 30


def draw_header(d, text, th, slide=1.0):
    f = V.fit(text.upper(), 700, 40)
    w = f.getlength(text.upper()) + 60
    x0 = V.X0 - (1 - slide) * (w + 100)
    d.rounded_rectangle([x0, 190, x0 + w, 262], radius=36, fill=th["ink"])
    d.text((x0 + 30, 226), text.upper(), font=f, fill=th["bg"], anchor="lm")


# ---------------------------------------------------------------- background
def make_bg(th):
    bg = Image.new("RGB", (W, H), th["bg"][:3])
    blob = Image.new("RGBA", (900, 900), th["accent"][:3] + (0,))
    bd = ImageDraw.Draw(blob)
    bd.ellipse([150, 150, 750, 750], fill=th["accent"][:3] + (60,))
    blob = blob.filter(ImageFilter.GaussianBlur(90))
    blob2 = Image.new("RGBA", (800, 800), th["accent"][:3] + (0,))
    ImageDraw.Draw(blob2).ellipse([150, 150, 650, 650], fill=th["accent"][:3] + (34,))
    blob2 = blob2.filter(ImageFilter.GaussianBlur(80))
    return bg, blob, blob2


def palette(th):
    """Background tones that alternate on every beat (cream -> accent tint -> sand)."""
    cream = th["bg"]
    return [cream, V.mix(cream, th["accent"], 0.2), V.hexc("#E5DBC8")]


def frame_bg(base, t, T, col):
    bg, blob, blob2 = base
    img = Image.new("RGB", (W, H), col[:3])
    a = 2 * math.pi * t / T
    x1 = int(380 + 420 * math.cos(a)) - 450
    y1 = int(700 + 520 * math.sin(2 * a)) - 450
    x2 = int(560 - 380 * math.sin(a)) - 400
    y2 = int(1250 - 450 * math.cos(a)) - 400
    img.paste(blob, (x1, y1), blob)
    img.paste(blob2, (x2, y2), blob2)
    return img


# ---------------------------------------------------------------- main render
def render(script, out_mp4, work, log=print):
    t_start = time.time()
    os.makedirs(work, exist_ok=True)
    th = theme(script)
    scenes = script["scenes"]
    voice = script.get("voice") or "af_heart"
    audio, timing, T = mvoice.speak(scenes, voice=voice, speed=float(script.get("speed", 1.08)),
                                     cache=os.path.join(work, "tts"))
    T = round(math.ceil(T * FPS) / FPS, 4)
    nfr = int(round(T * FPS))
    audio = np.pad(audio, (0, max(0, int(T * SR) - len(audio))))[: int(T * SR)]
    pad = bed(T, [tm["t0"] for tm in timing], seed=len(script.get("title", "")))
    mixd = audio * 1.0 + pad
    for tm in timing:  # tiny pop when a scene starts (sound change every scene)
        a = int(tm["t0"] * SR)
        p = _pop()
        mixd[a:a + len(p)] += p[: len(mixd) - a] * 0.4
    mixd = mixd / (np.abs(mixd).max() + 1e-9) * 0.89
    wav = os.path.join(work, "mix.wav")
    sf.write(wav, mixd.astype(np.float32), SR)
    ln = loudnorm_args(wav)
    log(f"audio {T:.1f}s, speech {timing[-1]['speech_end']:.1f}s, tts+mix {time.time() - t_start:.0f}s")

    caps = [chunks(tm["words"]) for tm in timing]
    base = make_bg(th)
    hook = script.get("hook", "")
    header = script.get("header") or hook

    def scene_at(t):
        for i, tm in enumerate(timing):
            if t < tm["t1"] or i == len(timing) - 1:
                return i, tm
        return len(timing) - 1, timing[-1]

    # beats: every scene start + one punch halfway through longer scenes (+ two extra in the hook)
    beats = []
    for i, tm in enumerate(timing):
        D = tm["t1"] - tm["t0"]
        beats.append(tm["t0"])
        if i == 0:
            beats += [x for x in (0.9, 1.9) if x < D - 0.8]
        tp = tm["t0"] + max(1.7, D * 0.5)
        if D > 3.4 and tp > beats[-1] + 1.2:
            beats.append(tp)
    beats = sorted(set(round(b, 3) for b in beats))
    pal = palette(th)

    def draw(t):
        i, tm = scene_at(t)
        p = t - tm["t0"]
        D = tm["t1"] - tm["t0"]
        bi = max(0, sum(1 for b in beats if b <= t) - 1)
        col = pal[bi % len(pal)]
        th_f = dict(th, bg=col, soft=V.mix(col, th["ink"], 0.12))
        img = frame_bg(base, t, T, col)
        d = ImageDraw.Draw(img)
        sb = [b for b in beats if tm["t0"] < b <= t]  # punches already passed inside this scene
        if i == 0:
            p += 0.45  # frame 0 already shows the number counting and the icon
        spec = scenes[i].get("visual", {"type": "statement", "text": scenes[i]["say"]})
        if i == 0 and hook:
            ybot = draw_hook(img, d, hook, t, th_f)
            scale_base, py = 0.76, max(ybot + 10, 660)
        else:
            draw_header(d, header, th_f, V.ease((t - timing[1]["t0"]) / 0.35) if len(timing) > 1 and i == 1 else 1.0)
            scale_base, py = 1.0, PANEL_Y
        layer = Image.new("RGBA", (W, V.PANEL_H), col[:3] + (0,))
        V.draw_visual(layer, spec, p, D, th_f)
        # camera: slow push + a punch-in on every beat (a visual change every ~2-3 s)
        z = scale_base * (1 + 0.012 * p)
        for b in sb:
            z *= 1 + 0.06 * V.ease((t - b) / 0.12)
        slide = 0 if i == 0 else (1 - V.ease(p / 0.24)) * 300
        lw, lh = int(W * z), int(V.PANEL_H * z)
        lay = layer.resize((lw, lh), Image.BILINEAR) if abs(z - 1) > 1e-3 else layer
        x = int(V.CX - V.CX * z + slide)
        y = int(py + (V.PANEL_H * scale_base - lh) / 2)
        img.paste(lay, (x, y), lay)
        draw_caption(d, caps[i], t, th_f)
        return img

    frame0 = draw(0.0)
    frame0.save(os.path.join(work, "frame0.png"))
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-af", ln + ",aresample=48000", "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{T:.3f}", "-movflags", "+faststart", out_mp4]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    fade = 0.3
    for k in range(nfr):
        t = k / FPS
        im = frame0 if k == 0 else draw(t)
        if t > T - fade:  # loop: the last frames melt into frame 0
            im = Image.blend(im, frame0, V.clamp((t - (T - fade)) / (fade - 1 / FPS)))
        pr.stdin.write(im.tobytes())
        if k % 300 == 0:
            log(f"  frame {k}/{nfr}  {time.time() - t_start:.0f}s")
    pr.stdin.close()
    err = pr.stderr.read().decode(errors="replace")
    if pr.wait() != 0:
        raise RuntimeError("ffmpeg failed: " + err[-800:])
    return {"duration": T, "seconds_render": round(time.time() - t_start, 1)}

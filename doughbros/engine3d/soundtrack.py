"""Dialogue + detective music (8D) + SFX.  python3 engine/soundtrack.py out/epNNN   (reads timeline.json + frames/events.json, writes audio.wav)"""
import json, sys, wave
import numpy as np, soundfile as sf
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OD = sys.argv[1]
import audio8d as A

SR = A.SR
TL = json.load(open(os.path.join(OD, "timeline.json")))
EV = json.load(open(os.path.join(OD, "frames", "events.json")))["events"]
D = TL["duration"]; n = int(D * SR)
rng = np.random.default_rng(9)


def resample(x, sr):
    idx = np.arange(0, len(x), sr / SR)
    return np.interp(idx, np.arange(len(x)), x)


def put(buf, t, x, g=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    m = min(len(x), len(buf) - i); buf[i:i + m] += g * x[:m]


# dialogue (mono, centred) + ducking envelope
dia = np.zeros(n); duck = np.ones(n)
for b in TL["beats"]:
    if b.get("file"):
        x, sr = sf.read(b["file"]); x = resample(x.astype(float), sr)
        put(dia, b["start"], x, 0.95)
        i0, i1 = int(b["start"] * SR), int((b["start"] + b["dur"]) * SR)
        duck[max(0, i0 - 2400):i1 + 4800] = 0.35
duck = A.lp_fast(duck, 3)  # smooth

# detective music: slower, minor, plucky
def detective(D):
    out = np.zeros(int(D * SR)); beat = 60 / 112
    bass = [110.0, 110.0, 116.54, 110.0, 103.83, 103.83, 98.0, 103.83]
    t, k = 0.0, 0
    while t < D:
        i = int(t * SR)
        f = bass[k % 8]
        b_ = A.tone(f / 2, beat * 0.8, "saw") * A.env(int(beat * 0.8 * SR), 0.01, 0.2)
        put(out, t, A.lp_fast(b_, 500), 0.35)
        if k % 2 == 0:
            for j, m in enumerate((1, 1.189, 1.498)):
                nt = A.tone(f * 2 * m, 0.25, "sine") * A.env(int(0.25 * SR), 0.002, 0.07)
                put(out, t + j * beat / 4, nt, 0.12)
        if k % 4 == 2:
            sn = rng.normal(0, 1, int(0.15 * SR)) * A.env(int(0.15 * SR), 0.001, 0.04)
            put(out, t, sn, 0.12)
        t += beat; k += 1
    return out / (np.abs(out).max() + 1e-9) * 0.5

mus = A.spin8d(detective(D), period=9.0, depth=0.9)
mus *= duck[:, None]

# SFX
sfx = np.zeros(n)
def chime():
    tt = np.arange(int(1.2 * SR)) / SR
    return sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.5) for f in (1318, 1661, 1976, 2637)) * 0.12
def siren(d):
    tt = np.arange(int(d * SR)) / SR
    return np.sign(np.sin(2 * np.pi * (650 + 250 * np.sin(2 * np.pi * 2.2 * tt)) * tt)) * 0.12 * np.minimum(1, (d - tt) * 4)
def dun():
    tt = np.arange(int(1.4 * SR)) / SR
    return (np.sin(2 * np.pi * 73 * tt) + 0.5 * np.sin(2 * np.pi * 110 * tt)) * np.exp(-tt / 0.6) * 0.45
def rumble():
    tt = np.arange(int(0.9 * SR)) / SR
    return A.lp_fast(rng.normal(0, 1, len(tt)), 180) * np.sin(np.pi * tt / 0.9) * 0.8
for t, kind in EV:
    if kind in ("crunch", "squish"): put(sfx, t, A.crunch("car"), 0.55 if kind == "crunch" else 0.35)
    elif kind == "clang": put(sfx, t, A.crunch("bus"), 0.4)
    elif kind in ("chime", "clue"): put(sfx, t, chime(), 1.0)
    elif kind == "pop": put(sfx, t, chime()[::-1][: int(0.5 * SR)], 0.8)
    elif kind == "dun": put(sfx, t, dun())
    elif kind == "boing": put(sfx, t, A.boing(0), 1.2)
    elif kind == "engine": put(sfx, t, A.engine(1.4, 120)[::-1], 0.6)
    elif kind == "rumble": put(sfx, t, rumble())
    elif kind == "whoosh": put(sfx, t, A.lp_fast(rng.normal(0, 1, int(0.5 * SR)), 1500) * np.sin(np.linspace(0, np.pi, int(0.5 * SR))) * 0.4)
for b in TL["beats"]:
    if b.get("sfx") == "alarm": put(sfx, b["start"], siren(b["dur"] + 0.6))
    if b.get("sfx") == "suspicious": put(sfx, b["start"], dun(), 1.2)

mix = mus + np.stack([dia + 0.8 * sfx, dia + 0.8 * sfx], 1)
mix = A.reverb(mix, 0.08)
fade = np.ones(n); f = int(1.0 * SR); fade[-f:] = np.linspace(1, 0, f); mix *= fade[:, None]
mix /= np.abs(mix).max() / 0.89
with wave.open(os.path.join(OD, "audio.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("ok", D)

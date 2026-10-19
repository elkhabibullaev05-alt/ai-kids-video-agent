"""Procedural drift-phonk generator (100% original, no samples, no licences needed).

python3 engine/phonk.py OUT.wav --seed 7 [--bars 48] [--bpm 140]
Every seed gives a different key, tempo, cowbell riff, 808 pattern, chord loop and arrangement.
Sounds: Memphis-style cowbell lead (2 detuned square partials through a band-pass), sliding distorted 808,
punchy kick, trap hats with rolls, clap/snare on 3, dark pad, vinyl noise, sidechain pump. 44.1 kHz stereo.
"""
import argparse
import json
import wave

import numpy as np

SR = 44100
p = argparse.ArgumentParser()
p.add_argument("out")
p.add_argument("--seed", type=int, default=1)
p.add_argument("--bars", type=int, default=48)
p.add_argument("--bpm", type=float, default=0)
a = p.parse_args()
R = np.random.default_rng(a.seed)

BPM = a.bpm or float(R.choice([128, 130, 135, 140, 145, 150, 160]))
BEAT = 60.0 / BPM
STEP = BEAT / 4  # 16th
BAR = BEAT * 4
N = int(a.bars * BAR * SR) + SR * 2
ROOT = 36 + int(R.integers(0, 12))  # C2..B2 (midi)
SCALE = [0, 2, 3, 5, 7, 8, 10] if R.random() < 0.7 else [0, 1, 3, 5, 7, 8, 10]  # minor / phrygian


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def deg(d, octv=0):
    return ROOT + 12 * octv + SCALE[d % 7] + 12 * (d // 7)


def env(n, a_=0.002, r=0.1, sus=0.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a_, 1e-4))
    return e * (sus + (1 - sus) * np.exp(-t / max(r, 1e-4)))


def lp(x, cut):
    a_ = np.exp(-2 * np.pi * cut / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # small buffers only
        acc = (1 - a_) * x[i] + a_ * acc
        y[i] = acc
    return y


def onepole(x, cut):
    # vectorised one-pole low-pass via FFT-free IIR approximation (cumulative filter in blocks)
    from scipy.signal import lfilter
    a_ = np.exp(-2 * np.pi * cut / SR)
    return lfilter([1 - a_], [1, -a_], x)


def bp(x, f, q=4.0):
    from scipy.signal import butter, sosfilt
    lo, hi = f / (2 ** (1 / (2 * q))), f * (2 ** (1 / (2 * q)))
    return sosfilt(butter(2, [lo, min(hi, SR / 2 - 100)], "bandpass", fs=SR, output="sos"), x)


def put(buf, t, x, g=1.0):
    i = int(t * SR)
    if i >= len(buf) or i < 0:
        return
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += g * x[:m]


# ---------------- instruments ----------------
def cowbell(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * f * t)) + 0.8 * np.sign(np.sin(2 * np.pi * f * 1.48 * t))
    s = bp(s, f * 1.25, 2.5)
    return s * env(n, 0.001, 0.18 + 0.1 * R.random(), 0.05) * 0.9


def kick(dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.5 * np.sin(ph) * np.exp(-t / 0.18)) * 0.95


def b808(f0, f1, dur, glide=0.06):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / glide) if f0 != f1 else np.full(n, f1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph)
    s = np.tanh(3.2 * s) * env(n, 0.003, dur * 0.9, 0.35)
    return s * 0.75


def hat(dur=0.05, open_=False):
    n = int((0.25 if open_ else dur) * SR)
    x = R.normal(0, 1, n)
    from scipy.signal import butter, sosfilt
    x = sosfilt(butter(4, 7000, "highpass", fs=SR, output="sos"), x)
    return x * env(n, 0.0005, 0.09 if open_ else 0.018) * 0.35


def clap():
    n = int(0.3 * SR)
    x = R.normal(0, 1, n)
    x = bp(x, 1500, 1.2)
    e = np.zeros(n)
    for k, o in enumerate((0, 0.011, 0.022)):
        i = int(o * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR / (0.012 if k < 2 else 0.14))
    return x * e * 0.6


def pad(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t * (1 + d)) for f in freqs for d in (-0.003, 0.003))
    s = onepole(s, 900)
    return s * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4) * 0.08


# ---------------- composition ----------------
riff_len = 16
riff = []
for s in range(riff_len):
    if R.random() < (0.62 if s % 2 == 0 else 0.35):
        riff.append((s, int(R.choice([0, 0, 2, 3, 4, 5, 7, -1, 6])), 1 + int(R.random() < 0.25)))
riff2 = [(s, d + int(R.choice([0, 0, 2, -2])), L) for s, d, L in riff]
prog = [int(x) for x in R.choice([[0, 5, 3, 4], [0, 3, 5, 4], [0, 6, 5, 3], [0, 0, 5, 6], [0, 4, 3, 5]])]
bass_pat = sorted(set([0, 6, 10] + [int(x) for x in R.choice(range(16), 2, replace=False)]))
kick_pat = sorted(set([0, 10] + ([7] if R.random() < 0.5 else []) + ([14] if R.random() < 0.4 else [])))
hat_div = int(R.choice([2, 2, 1]))
cow_oct = int(R.choice([4, 5]))
swing = 0.0 if R.random() < 0.6 else STEP * 0.12

# arrangement: intro 4 | A 8 (no drums -> drums) | B 8 drop | breakdown 4 | C 8 drop2 | outro 4 ... scaled to bars
sections = []
b = 0
plan = [("intro", 4), ("build", 4), ("drop", 8), ("drop", 8), ("break", 4), ("drop2", 8), ("drop2", 8), ("outro", 4)]
while b < a.bars:
    for name, L in plan:
        if b >= a.bars:
            break
        L = min(L, a.bars - b)
        sections.append((name, b, L))
        b += L

mix = np.zeros((N, 2))
drums = np.zeros(N)
bass = np.zeros(N)
lead = np.zeros(N)
padb = np.zeros(N)
sc = np.ones(N)  # sidechain envelope
K = kick()
C = clap()
events = []

for name, b0, L in sections:
    for bi in range(b0, b0 + L):
        t0 = bi * BAR + 1.0
        chord = prog[bi % 4]
        has_drums = name in ("build", "drop", "drop2") or (name == "outro" and bi - b0 < 2)
        has_bass = name in ("drop", "drop2")
        has_lead = name != "break" or (bi - b0) >= L - 1
        # pad every bar
        put(padb, t0, pad([hz(deg(chord + k, 0) + 12) for k in (0, 2, 4)], BAR + 0.05))
        if has_lead:
            rr = riff2 if (name == "drop2" and bi % 2) else riff
            for s, d, Ln in rr:
                f = hz(deg(d + chord * (name == "drop2"), cow_oct - 3))
                put(lead, t0 + s * STEP + (swing if s % 2 else 0), cowbell(f, STEP * Ln * 1.6), 0.55 if name != "intro" else 0.35)
        if has_drums:
            for s in range(16):
                ts = t0 + s * STEP + (swing if s % 2 else 0)
                if s in kick_pat and name != "build":
                    put(drums, ts, K, 1.0)
                    i0 = int(ts * SR)
                    w = int(0.22 * SR)
                    sc[i0:i0 + w] = np.minimum(sc[i0:i0 + w], 0.35 + 0.65 * np.linspace(0, 1, len(sc[i0:i0 + w])))
                if s in (4, 12) and name != "build":
                    put(drums, ts, C, 0.9)
                if s % hat_div == 0:
                    put(drums, ts, hat(), 0.8 if s % 4 else 1.0)
                if s == 14 and R.random() < 0.35:  # hat roll
                    for r in range(4):
                        put(drums, ts + r * STEP / 4, hat(0.03), 0.6)
            if name == "build" and bi == b0 + L - 1:
                for r in range(16):
                    put(drums, t0 + r * STEP, C * (0.3 + r / 20), 0.6)
                events.append(round(t0 + BAR, 2))
        if has_bass:
            for k, s in enumerate(bass_pat):
                nxt = bass_pat[k + 1] if k + 1 < len(bass_pat) else 16
                d = (nxt - s) * STEP
                f1 = hz(deg(chord, -1) + 12)
                f0 = f1 * (2 ** (R.choice([0, 0, 5, 7, -5]) / 12))
                put(bass, t0 + s * STEP, b808(f0, f1, d * 0.98), 0.9)

vinyl = R.normal(0, 1, N) * 0.004 + (R.random(N) < 0.00012) * R.normal(0, 0.25, N)
lead_s = np.tanh(1.6 * lead)
bass = np.tanh(1.3 * bass) * sc
padb = padb * (0.6 + 0.4 * sc)
L_ = drums * 0.9 + bass + lead_s * 0.85 + padb + vinyl
Rr = drums * 0.9 + bass + np.roll(lead_s, int(0.012 * SR)) * 0.85 + np.roll(padb, int(0.02 * SR)) + vinyl
mix = np.stack([L_, Rr], 1)
# simple reverb on lead/pad bus
from scipy.signal import fftconvolve
ir_n = int(1.6 * SR)
ir = R.normal(0, 1, (ir_n, 2)) * np.exp(-np.arange(ir_n) / SR / 0.45)[:, None] * 0.015
wet = np.stack([fftconvolve(lead_s * 0.6 + padb, ir[:, 0])[:N], fftconvolve(lead_s * 0.6 + padb, ir[:, 1])[:N]], 1)
mix = mix + wet
end = int((a.bars * BAR + 1.0) * SR)
fade = int(2.5 * SR)
mix[end - fade:end] *= np.linspace(1, 0, fade)[:, None]
mix = mix[:end + int(0.5 * SR)]
mix /= np.abs(mix).max() / 0.95
mix = np.tanh(1.4 * mix) / np.tanh(1.4)
mix *= 0.93
with wave.open(a.out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
meta = {"seed": a.seed, "bpm": BPM, "root_midi": ROOT, "bars": a.bars, "duration": round(len(mix) / SR, 2), "drops": events}
json.dump(meta, open(a.out.rsplit(".", 1)[0] + ".json", "w"))
print(json.dumps(meta))

"""Original soundtrack + SFX with an "8D" (rotating binaural) mix. Everything is synthesized — no samples.
python3 audio8d.py events.json out.wav
"""
import json, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(3)


def lp(x, a):  # one-pole low-pass
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def lp_fast(x, cutoff):
    # FFT brick-ish low-pass (fast for long signals)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def env(n, a=0.005, r=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)


def tone(freq, dur, kind="sine"):
    t = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * freq * t
    if kind == "saw":
        return 2 * ((freq * t) % 1) - 1
    if kind == "square":
        return np.sign(np.sin(ph))
    return np.sin(ph)


def music(D, bpm=128):
    n = int(D * SR); out = np.zeros(n); beat = 60 / bpm
    chords = [(220.0, 277.18, 329.63), (196.0, 246.94, 293.66), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66)]
    t = 0.0; k = 0
    while t < D:
        i = int(t * SR)
        kick = np.sin(2 * np.pi * (50 + 120 * np.exp(-np.arange(int(0.25 * SR)) / SR / 0.03)) * np.arange(int(0.25 * SR)) / SR) * env(int(0.25 * SR), 0.002, 0.12)
        out[i:i + len(kick)] += 0.9 * kick[: n - i]
        if k % 2 == 1:  # clap/hat
            hh = rng.normal(0, 1, int(0.12 * SR)) * env(int(0.12 * SR), 0.001, 0.03)
            out[i:i + len(hh)] += 0.25 * hh[: n - i]
        ch = chords[(k // 8) % 4]
        for j, fq in enumerate(ch):  # arpeggio 8ths
            s = int((t + j * beat / 3) * SR)
            if s >= n: break
            note = tone(fq * 2, beat / 2, "square") * env(int(beat / 2 * SR), 0.003, 0.08)
            out[s:s + len(note)] += 0.08 * note[: n - s]
        bass = tone(ch[0] / 2, beat * 0.9, "saw") * env(int(beat * 0.9 * SR), 0.01, 0.25)
        out[i:i + len(bass)] += 0.18 * lp_fast(bass, 400)[: n - i]
        t += beat; k += 1
    return out / (np.abs(out).max() + 1e-9) * 0.5


def crunch(kind):
    n = int(1.2 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (45 + 60 * np.exp(-t / 0.05)) * t) * env(n, 0.002, 0.25)
    metal = lp_fast(rng.normal(0, 1, n), 3500) * env(n, 0.001, 0.18)
    ring = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.5) for f in (523, 811, 1297)) * 0.15
    creak = np.sin(2 * np.pi * (300 - 200 * t) * t + 3 * np.sin(2 * np.pi * 9 * t)) * env(n, 0.05, 0.4) * 0.3
    big = 1.3 if kind in ("bus", "truck") else 1.0
    return (1.0 * thump * big + 0.7 * metal + ring + creak) / 2.2


def engine(dur, f0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.6 * t / dur)  # pitch rises as it approaches (Doppler-ish)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.5
    return lp_fast(x, 900) * np.linspace(0.05, 1, n) ** 2 * 0.35


def boing(n_):
    n = int(0.5 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (200 + 500 * np.exp(-t / 0.08)) * t) * env(n, 0.002, 0.15) * 0.3


def spin8d(mono, period=7.0, depth=1.0, offset=0.0):
    """Rotate a mono source around the head: level + time difference + far-ear dulling + room."""
    n = len(mono); t = np.arange(n) / SR
    th = 2 * np.pi * (t / period) + offset
    pan = np.sin(th) * depth                     # -1 left .. +1 right
    front = np.cos(th)                           # behind the head is a bit darker/quieter
    gl = np.sqrt(0.5 * (1 - pan)); gr = np.sqrt(0.5 * (1 + pan))
    itd = (0.00065 * pan * SR).astype(int)        # up to 0.65 ms delay to the far ear
    idx = np.arange(n)
    L = mono[np.clip(idx + np.minimum(itd, 0), 0, n - 1)] * gl
    R = mono[np.clip(idx - np.maximum(itd, 0), 0, n - 1)] * gr
    dull = lp_fast(mono, 2500)
    L = L * (0.75 + 0.25 * front) + dull * gl * 0.25 * (1 - front) / 2
    R = R * (0.75 + 0.25 * front) + dull * gr * 0.25 * (1 - front) / 2
    return np.stack([L, R], 1)


def reverb(st, mix=0.18):
    out = st.copy()
    for d, g in ((0.029, 0.35), (0.037, 0.3), (0.041, 0.28), (0.053, 0.22), (0.079, 0.15)):
        k = int(d * SR)
        out[k:, 0] += st[:-k, 1] * g * mix * 3
        out[k:, 1] += st[:-k, 0] * g * mix * 3
    return out


def main():
    ev = json.load(open(sys.argv[1])); D = ev["duration"]; n = int(D * SR)
    mus = spin8d(music(D), period=8.0)
    sfx = np.zeros(n)
    for e in ev["events"]:
        th = e["t"]
        s0 = int(max(0, th - 2.4) * SR)
        eng = engine(min(2.4, th), 70 if e["kind"] in ("bus", "truck") else 110)
        sfx[s0:s0 + len(eng)] += eng[: n - s0]
        i = int(th * SR); c = crunch(e["kind"])
        sfx[i:i + len(c)] += c[: n - i]
        for k in range(4):
            j = int((th + 0.45 + 0.12 * k) * SR); b = boing(k)
            sfx[j:j + len(b)] += b[: n - j]
    sfx8 = spin8d(sfx, period=5.0, depth=0.8, offset=np.pi / 2)
    mix = reverb(0.55 * mus + 0.9 * sfx8)
    fade = np.ones(n); f = int(0.6 * SR); fade[-f:] = np.linspace(1, 0, f); fade[:int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
    mix *= fade[:, None]
    mix /= np.abs(mix).max() / 0.89
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(sys.argv[2], D)


if __name__ == "__main__":
    main()

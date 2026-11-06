"""Kokoro narration (with approximate word timings), a generated beat bed, whoosh/pop SFX, mix + loudnorm."""
import os
import re
import subprocess

import numpy as np
import soundfile as sf

SR = 24000
_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        kd = os.environ.get("KOKORO_DIR", "/opt/kokoro")
        _K = Kokoro(os.path.join(kd, "kokoro.onnx"), os.path.join(kd, "voices.bin"))
    return _K


def _trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx):
        return a
    return a[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.06 * SR)]


def tts(text, voice="am_adam", speed=1.1):
    """-> (float32 mono @24k, [(word, t0, t1), ...]) — word times spread by letter count within each sentence."""
    cdir = os.environ.get("RBX_TTS_CACHE")  # dev only: reuse narration between test renders
    if cdir:
        import hashlib
        import pickle
        os.makedirs(cdir, exist_ok=True)
        cf = os.path.join(cdir, hashlib.md5(f"{voice}|{speed}|{text}".encode()).hexdigest() + ".pkl")
        if os.path.exists(cf):
            return pickle.load(open(cf, "rb"))
        r = _tts(text, voice, speed)
        pickle.dump(r, open(cf, "wb"))
        return r
    return _tts(text, voice, speed)


def _tts(text, voice, speed):
    k = kokoro()
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    chunks, words, t = [], [], 0.0
    for p in parts:
        a, sr = k.create(p, voice=voice, speed=speed, lang="en-us")
        a = np.asarray(a, np.float32)
        if sr != SR:
            a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)
        a = _trim(a)
        a = a / (np.abs(a).max() + 1e-9) * 0.9
        dur = len(a) / SR
        ws = p.split()
        wts = [len(re.sub(r"[^\w%$]", "", w)) + 1.6 for w in ws]
        tot = sum(wts) or 1
        x = t
        for w, wt in zip(ws, wts):
            d = dur * wt / tot
            words.append((w, round(x, 3), round(x + d, 3)))
            x += d
        chunks.append(a)
        gap = np.zeros(int(0.16 * SR), np.float32)
        chunks.append(gap)
        t += dur + len(gap) / SR
    return np.concatenate(chunks) if chunks else np.zeros(SR, np.float32), words


# ---------------------------------------------------------------- generated music + sfx (no copyrighted audio)

def _env(n, a=0.002, d=0.15):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def beat(seconds, bpm=118, seed=0, intensity=1.0):
    """Simple trap-ish bed: kick, clap, hats, sub-bass, soft pad chords. Mono float32."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR) + SR
    out = np.zeros(n, np.float32)
    spb = 60 / bpm
    step = spb / 4
    keys = [[0, 3, 7], [-4, 0, 3], [-2, 2, 5], [-5, -2, 2]]  # minor-ish loop
    root = 110 * 2 ** (rng.integers(-3, 3) / 12)
    kick_n = int(0.35 * SR)
    tk = np.arange(kick_n) / SR
    kick = (np.sin(2 * np.pi * (45 * tk + 90 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)).astype(np.float32)
    clap = (rng.standard_normal(int(0.18 * SR)) * _env(int(0.18 * SR), 0.001, 0.05)).astype(np.float32)
    hat = (rng.standard_normal(int(0.05 * SR)) * _env(int(0.05 * SR), 0.0005, 0.012)).astype(np.float32)
    hat = np.diff(hat, prepend=0).astype(np.float32)  # brighter
    s = 0
    i = 0
    while s * SR < n - SR:
        p = int(s * SR)
        pos = i % 16
        if pos in (0, 7, 10):
            out[p:p + kick_n] += kick[: n - p] * 0.9
        if pos in (4, 12):
            out[p:p + len(clap)] += clap[: n - p] * 0.35
        if pos % 2 == 0 or rng.random() < 0.3:
            out[p:p + len(hat)] += hat[: n - p] * (0.22 if pos % 4 == 2 else 0.12)
        s += step
        i += 1
    # pad + sub
    bar = spb * 4
    t = np.arange(n) / SR
    pad = np.zeros(n, np.float32)
    for b in range(int(seconds / bar) + 2):
        ch = keys[b % 4]
        a, e = int(b * bar * SR), min(n, int((b + 1) * bar * SR))
        if a >= n:
            break
        tt = t[a:e] - b * bar
        env = np.minimum(1, tt / 0.3) * np.minimum(1, (bar - tt) / 0.3)
        for semi in ch:
            f = root * 2 ** (semi / 12)
            pad[a:e] += (np.sin(2 * np.pi * f * 2 * tt) * 0.05 + np.sin(2 * np.pi * f * 4.01 * tt) * 0.02) * env
        f0 = root * 2 ** (ch[0] / 12) / 2
        pad[a:e] += np.sin(2 * np.pi * f0 * tt) * 0.12 * env
    out = out * intensity + pad
    return (out / (np.abs(out).max() + 1e-9) * 0.8).astype(np.float32)


def whoosh(dur=0.45, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    x = rng.standard_normal(n).astype(np.float32)
    # rising band via moving average of decreasing length
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 2
    y = np.convolve(x, np.ones(6) / 6, mode="same") * env
    return (y / (np.abs(y).max() + 1e-9) * 0.6).astype(np.float32)


def pop(seed=2):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 35)
    return (y * 0.5).astype(np.float32)


def ding():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 6)
    return (y * 0.35).astype(np.float32)


def place(buf, clip, t, gain=1.0):
    p = int(t * SR)
    if p >= len(buf):
        return
    e = min(len(buf), p + len(clip))
    buf[p:e] += clip[: e - p] * gain


def mix_and_master(voice, music, sfx, total, out_wav, music_gain=0.16, duck=0.55):
    """voice/sfx: full-length float arrays; music bed ducked under voice. Writes 48k loudnorm'd (-14 LUFS) wav."""
    n = int(total * SR)

    def fit(a):
        a = a[:n]
        return np.pad(a, (0, n - len(a))) if len(a) < n else a

    v, m, s = fit(voice), fit(music), fit(sfx)
    env = np.convolve(np.abs(v), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    env = np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    m = m * music_gain * (1 - duck * env)
    mix = v + m + s * 0.5
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.85
    raw = out_wav + ".raw.wav"
    sf.write(raw, mix.astype(np.float32), SR)
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.85,aresample=48000",
                        "-ar", "48000", "-ac", "2", out_wav], capture_output=True, text=True)
    os.remove(raw)
    if r.returncode:
        raise RuntimeError("loudnorm failed: " + r.stderr[-300:])
    return out_wav

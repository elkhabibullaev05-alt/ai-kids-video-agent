"""Kokoro narration with word timings (estimated per sentence) + a soft generated ambient pad (no copyrighted music)."""
import os
import re

import numpy as np

SR = 24000
VOICE = os.environ.get("UFC_VOICE", "am_michael")
SPEED = float(os.environ.get("UFC_SPEED", "1.05"))
_k = None


def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        kd = os.environ.get("KOKORO_DIR", "/opt/kokoro")
        _k = Kokoro(os.path.join(kd, "kokoro.onnx"), os.path.join(kd, "voices.bin"))
    return _k


def _clean(text):
    t = text.replace("#", "number ").replace("&", " and ").replace("—", ", ").replace("–", " to ")
    t = re.sub(r"(\d)\+", r"\1 plus", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _trim(a, thr=0.012, keep=0.03):
    x = np.abs(a)
    on = np.nonzero(x > thr)[0]
    if not len(on):
        return a[:0]
    i = max(0, on[0] - int(keep * SR * 0.3))
    j = min(len(a), on[-1] + int(keep * SR))
    return a[i:j]


def say(text, speed=None):
    """-> (audio float32 @24k, words [(word, t0, t1)]). Synthesised sentence by sentence; words spread by length."""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    parts, words, t = [], [], 0.0
    v = VOICE
    for i, s in enumerate(sents):
        a, sr = kokoro().create(_clean(s), voice=v, speed=speed or SPEED, lang="en-gb" if v.startswith("b") else "en-us")
        a = _trim(np.asarray(a, np.float32))
        if not len(a):
            continue
        dur = len(a) / SR
        toks = s.split()
        wts = [len(re.sub(r"[^\w]", "", w)) + 2.2 + (2.5 if re.search(r"[,;:]$", w) else 0) for w in toks]
        tot = sum(wts) or 1
        tt = t + 0.04
        span = dur - 0.08
        for w, wt in zip(toks, wts):
            d = span * wt / tot
            words.append((w, tt, tt + d))
            tt += d
        parts.append(a)
        t += dur
        if i < len(sents) - 1:
            gap = np.zeros(int(0.12 * SR), np.float32)
            parts.append(gap)
            t += len(gap) / SR
    a = np.concatenate(parts) if parts else np.zeros(int(0.5 * SR), np.float32)
    a = a / (np.abs(a).max() + 1e-9) * 0.9
    return a, words


def pad(seconds, seed=1):
    """Gentle ambient chord pad (A minor-ish), slow swells; level is set by the caller."""
    n = int(seconds * SR)
    t = np.arange(n, dtype=np.float32) / SR
    rng = np.random.default_rng(seed)
    out = np.zeros(n, np.float32)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [164.81, 207.65, 246.94]]
    seg = 8.0
    for ci in range(int(seconds / seg) + 2):
        ch = chords[ci % len(chords)]
        t0 = ci * seg - 2.0
        i0, i1 = max(0, int(t0 * SR)), min(n, int((t0 + seg + 4.0) * SR))
        if i1 <= i0:
            continue
        tt = t[i0:i1] - t0
        env = np.sin(np.clip(tt / (seg + 4.0), 0, 1) * np.pi) ** 2
        for f in ch:
            for det in (-0.6, 0.6):
                out[i0:i1] += (np.sin(2 * np.pi * (f / 2 + det) * tt + rng.random() * 6) * 0.5
                               + np.sin(2 * np.pi * (f + det) * tt) * 0.25) * env
    # soft air noise
    noise = rng.normal(0, 1, n).astype(np.float32)
    k = np.ones(400, np.float32) / 400
    noise = np.convolve(noise, k, mode="same") * 4
    out += noise * 0.15
    out /= (np.abs(out).max() + 1e-9)
    return out


def mix(voice, music_db=-24.0):
    """voice: float32 @24k. Adds the pad ~music_db below the voice peak, ducked under speech."""
    m = pad(len(voice) / SR + 0.1)[:len(voice)]
    env = np.convolve(np.abs(voice), np.ones(4800, np.float32) / 4800, mode="same")
    duck = 1.0 - 0.45 * np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    out = voice + m * duck * (10 ** (music_db / 20))
    return out / (np.abs(out).max() + 1e-9) * 0.9

"""Voices (offline Kokoro TTS) and synthesized SFX / music beds."""
import os, subprocess, hashlib
import numpy as np
import soundfile as sf

SR = 24000
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")

# speaker -> (kokoro voice, speed, pitch semitones, extra ffmpeg audio filter)
CAST = {
    "narr":    ("bm_george", 0.90, -2, "aecho=0.8:0.7:60:0.25"),
    "bup":     ("am_puck",   1.05,  4, None),
    "pim":     ("af_sky",    1.15,  6, "vibrato=f=9:d=0.35"),
    "zeek":    ("am_echo",   0.97,  3, None),
    "lolly":   ("af_bella",  1.05,  4, None),
    "crispy":  ("am_fenrir", 0.85, -3, "aecho=0.6:0.5:30:0.2"),
    "pot":     ("am_onyx",   0.80, -7, "aecho=0.8:0.85:90|160:0.45|0.3"),
    "frost":   ("af_nicole", 0.85, -4, "aecho=0.8:0.9:120|240:0.5|0.35"),
    "toaster": ("am_michael", 0.95, -5, "acrusher=bits=8:mode=log:aa=1,aecho=0.8:0.6:40:0.3"),
    "mixer":   ("am_adam",   1.10,  3, "tremolo=f=14:d=0.5"),
}

_kokoro = None


def kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(MODELS, "kokoro.onnx"), os.path.join(MODELS, "voices.bin"))
    return _kokoro


def voice(speaker, text, workdir):
    v, speed, semis, extra = CAST[speaker]
    key = hashlib.md5(f"{speaker}|{text}".encode()).hexdigest()[:12]
    out = os.path.join(workdir, f"v_{key}.wav")
    if not os.path.exists(out):
        s, sr = kokoro().create(text, voice=v, speed=speed, lang="en-us")
        raw = out + ".raw.wav"
        sf.write(raw, s, sr)
        flt = f"rubberband=pitch={2 ** (semis / 12):.4f}" + ("," + extra if extra else "")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", flt, "-ar", str(SR), "-ac", "1", out], check=True)
        os.remove(raw)
    a, _ = sf.read(out)
    # trim trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz):
        a = a[: nz[-1] + int(0.05 * SR)]
    return a.astype(np.float32)


# ---------------- SFX ----------------
def _env(n, attack=0.005, decay=0.3):
    t = np.arange(n) / SR
    return np.minimum(t / attack, 1) * np.exp(-t / decay)


def thump():
    n = int(SR * 0.9); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (60 - 25 * t) * t) * _env(n, 0.003, 0.25)
    return s + np.random.randn(n) * _env(n, 0.001, 0.02) * 0.4


def clank():
    n = int(SR * 0.5); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(523, .5), (1187, .35), (1740, .25), (2630, .15)])
    return s * _env(n, 0.001, 0.12) * 0.6


def rattle(dur=1.3):
    out = np.zeros(int(SR * dur))
    for k in range(int(dur * 9)):
        c = clank() * np.random.uniform(0.4, 0.9)
        i = int((k / 9 + np.random.uniform(0, 0.03)) * SR)
        out[i:i + len(c)] += c[: max(0, len(out) - i)]
    return out


def step():
    n = int(SR * 0.08)
    return np.random.randn(n) * _env(n, 0.001, 0.015) * 0.25


def whoosh(dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR
    return np.convolve(np.random.randn(n), np.ones(40) / 40, "same") * np.sin(np.pi * t / dur) ** 2 * 1.2


def roar(dur=2.0):
    n = int(SR * dur); t = np.arange(n) / SR
    noise = np.convolve(np.random.randn(n), np.ones(120) / 120, "same") * 6
    growl = np.sin(2 * np.pi * 48 * t + 3 * np.sin(2 * np.pi * 7 * t)) * 0.5
    e = np.minimum(t / 0.25, 1) * np.exp(-np.maximum(t - dur * 0.6, 0) / 0.3)
    return (noise + growl) * e * 0.8


def boing():
    n = int(SR * 0.5); t = np.arange(n) / SR
    f = 220 + 400 * np.exp(-t * 8) * np.sin(2 * np.pi * 9 * t) ** 2
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.005, 0.2) * 0.5


def pop():
    n = int(SR * 0.12); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (900 - 5000 * t) * t) * _env(n, 0.001, 0.03) * 0.6


def creak(dur=1.2):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 140 + 60 * np.sin(2 * np.pi * 0.8 * t)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (np.random.rand(n) > 0.6)
    s = np.convolve(s, np.ones(8) / 8, "same")
    return s * np.sin(np.pi * t / dur) * 0.3


def ice():
    out = np.zeros(int(SR * 0.9))
    for k in range(14):
        n = int(SR * 0.05); t = np.arange(n) / SR
        c = np.sin(2 * np.pi * np.random.uniform(2500, 5000) * t) * _env(n, 0.001, 0.01)
        i = int(np.random.uniform(0, 0.8) * SR)
        out[i:i + n] += c * 0.4
    return out


def ding():
    n = int(SR * 1.5); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * t) + 0.4 * np.sin(2 * np.pi * 2640 * t)) * _env(n, 0.002, 0.5) * 0.35


def sting():
    n = int(SR * 3.0); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) for f in (73.4, 77.8, 146.8, 155.6, 311)) * _env(n, 0.01, 1.2) * 0.25
    th = thump()
    return s + np.pad(th, (0, n - len(th)))


def heartbeat(dur, bpm=70):
    out = np.zeros(int(SR * dur)); period = 60 / bpm
    for k in range(int(dur / period)):
        for off, amp in ((0, 1.0), (0.22, 0.7)):
            b = thump()[: int(SR * 0.3)] * amp * 0.35
            i = int((k * period + off) * SR)
            out[i:i + len(b)] += b[: max(0, len(out) - i)]
    return out


def drone(dur, base=55.0):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * base * t) * 0.5 + np.sin(2 * np.pi * base * 1.06 * t) * 0.4 + np.sin(2 * np.pi * base * 2.01 * t) * 0.12
    return s * (0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)) * 0.12


def music_box(dur):
    """creepy little lullaby loop (original melody)"""
    notes = [76, 79, 81, 79, 76, 74, 76, 0, 72, 74, 76, 74, 71, 72, 69, 0]
    out = np.zeros(int(SR * dur)); beat = 0.42
    for k in range(int(dur / beat)):
        m = notes[k % len(notes)]
        if not m:
            continue
        f = 440 * 2 ** ((m - 69) / 12) * (1 + 0.006 * np.sin(k))  # slightly detuned
        n = int(SR * 0.8); t = np.arange(n) / SR
        tone = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 3.01 * t)) * _env(n, 0.002, 0.35)
        i = int(k * beat * SR)
        out[i:i + n] += tone[: max(0, len(out) - i)] * 0.12
    return out


SFX = {"thump": thump, "clank": clank, "rattle": rattle, "whoosh": whoosh, "roar": roar, "boing": boing,
       "pop": pop, "creak": creak, "ice": ice, "ding": ding, "sting": sting, "step": step}
MUSIC = ["drone", "heartbeat", "music_box", "none"]

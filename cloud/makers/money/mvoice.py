"""Money Story Daily — Kokoro voice for each scene + rough word timings.

speak(scenes, voice, speed) -> (audio float32 @24 kHz, [scene timing dicts]).
The voice starts at 0.0 s (leading silence trimmed). Kokoro reads "$5,000" as "dollar five thousand",
so every `say` is rewritten into spoken words first (spoken()); captions keep the written form.
"""
import os
import re

import numpy as np

SR = 24000
KD = os.environ.get("KOKORO_DIR", "/opt/kokoro")
_K = None

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(os.path.join(KD, "kokoro.onnx"), os.path.join(KD, "voices.bin"))
    return _K


def words(n):
    """Integer -> English words (0 .. 999,999,999,999)."""
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + words(n % 100) if n % 100 else "")
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            return words(n // div) + " " + name + (" " + words(n % div) if n % div else "")
    return str(n)


def _num(s):
    """'5,000' / '3.5' / '1.2' -> words."""
    s = s.replace(",", "")
    if "." in s:
        a, b = s.split(".", 1)
        return words(int(a or 0)) + " point " + " ".join(ONES[int(c)] for c in b)
    return words(int(s))


_MULT = {"k": "thousand", "K": "thousand", "m": "million", "M": "million", "b": "billion", "B": "billion"}


def _money(m):
    whole, cents, mult = m.group(1).replace(",", ""), m.group(2), m.group(3)
    if mult:
        num = _num(whole + ("." + cents if cents else ""))
        return f"{num} {_MULT[mult]} dollars"
    w = int(whole or 0)
    out = words(w) + (" dollar" if w == 1 else " dollars")
    if cents and int(cents):
        c = int(cents.ljust(2, "0")[:2])
        out = (words(w) + " " + words(c)) if w and w < 100 else out + " and " + words(c) + " cents"
        if w == 0:
            out = words(c) + " cents"
    return out


ABBR = {"APR": "A P R", "401(k)": "four oh one k", "401k": "four oh one k", "IRA": "I R A", "Roth": "Roth",
        "HYSA": "high-yield savings account", "ETF": "E T F", "ETFs": "E T Fs", "vs": "versus", "vs.": "versus",
        "mo": "month", "/mo": " a month", "/yr": " a year", "BNPL": "buy now pay later", "%": " percent"}


def spoken(text):
    t = text
    t = t.replace("401(k)", "four oh one k").replace("401k", "four oh one k")
    t = re.sub(r"/mo\b", " a month", t)
    t = re.sub(r"/yr\b", " a year", t)
    t = re.sub(r"/hr\b", " an hour", t)
    t = re.sub(r"\$(\d[\d,]*)(?:\.(\d{1,2}))?([kKmMbB])?\b", _money, t)
    t = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s?%", lambda m: _num(m.group(1)) + " percent", t)
    t = re.sub(r"\bAPR\b", "A P R", t)
    t = re.sub(r"\bBNPL\b", "buy now, pay later", t)
    t = re.sub(r"\bHYSA\b", "high-yield savings account", t)
    t = re.sub(r"\bIRA\b", "I R A", t)
    t = re.sub(r"\bETFs?\b", lambda m: "E T F" + ("s" if m.group(0).endswith("s") else ""), t)
    t = re.sub(r"\bvs\.?(?=\s)", "versus", t)
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", lambda m: words(int(m.group(1))) + (" " + words(int(m.group(2))) if int(m.group(2)) else " o'clock"), t)
    t = re.sub(r"\b(19|20)(\d{2})\b", lambda m: words(int(m.group(1))) + " " + (words(int(m.group(2))) if int(m.group(2)) >= 10 else "oh " + words(int(m.group(2)))), t)
    t = re.sub(r"(\d+)(st|nd|rd|th)\b", lambda m: words(int(m.group(1))) + m.group(2), t)
    t = re.sub(r"\d[\d,]*(?:\.\d+)?", lambda m: _num(m.group(0)), t)
    t = t.replace("&", " and ").replace("→", " to ").replace("—", ", ").replace("–", " to ")
    return re.sub(r"\s+", " ", t).strip()


def _trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx):
        return a
    s = max(0, idx[0] - int(0.01 * SR))
    e = min(len(a), idx[-1] + int(0.06 * SR))
    return a[s:e]


def _tts(text, voice, speed, cache=None):
    if cache:
        import hashlib
        os.makedirs(cache, exist_ok=True)
        cf = os.path.join(cache, hashlib.sha1(f"{text}|{voice}|{speed:.3f}".encode()).hexdigest()[:16] + ".npy")
        if os.path.exists(cf):
            return np.load(cf)
        a = _tts(text, voice, speed)
        np.save(cf, a)
        return a
    a, sr = _kokoro().create(spoken(text), voice=voice, speed=speed, lang="en-us")
    a = np.asarray(a, np.float32)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a).astype(np.float32)
    return _trim(a)


def _word_times(text, start, dur):
    """Split the written `say` into display words; time each by the length of its spoken form."""
    ws = text.split()
    wt = []
    for w in ws:
        n = len(spoken(w)) + 2
        if w[-1:] in ".!?":
            n += 6
        elif w[-1:] in ",;:":
            n += 3
        wt.append(n)
    tot = sum(wt) or 1
    out, t = [], start
    for w, n in zip(ws, wt):
        d = dur * n / tot
        out.append({"w": w, "t0": round(t, 3), "t1": round(t + d, 3)})
        t += d
    return out


def speak(scenes, voice="af_heart", speed=1.08, gap=0.16, max_total=58.0, cache=None):
    """TTS every scene; if the total runs past max_total, re-speak faster (once, up to speed 1.28)."""
    clips = [_tts(s["say"], voice, speed, cache) for s in scenes]
    total = sum(len(c) for c in clips) / SR + gap * (len(clips) - 1) + 0.5
    if total > max_total:
        sp = min(1.28, speed * total / (max_total - 0.5))
        clips = [_tts(s["say"], voice, sp, cache) for s in scenes]
    parts, timing, t = [], [], 0.0
    g = np.zeros(int(gap * SR), np.float32)
    for i, (s, c) in enumerate(zip(scenes, clips)):
        c = c / (np.abs(c).max() + 1e-9) * 0.9
        d = len(c) / SR
        timing.append({"i": i, "t0": round(t, 3), "speech_end": round(t + d, 3), "words": _word_times(s["say"], t, d)})
        parts.append(c)
        t += d
        if i < len(clips) - 1:
            parts.append(g)
            t += gap
    tail = np.zeros(int(0.45 * SR), np.float32)  # breath before the loop jumps back to frame 0
    parts.append(tail)
    t += 0.45
    for i, tm in enumerate(timing):  # each scene's picture lasts until the next scene's voice starts
        tm["t1"] = timing[i + 1]["t0"] if i + 1 < len(timing) else round(t, 3)
    return np.concatenate(parts), timing, round(t, 3)

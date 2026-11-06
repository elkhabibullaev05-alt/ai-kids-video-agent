"""Funny Rank Daily — moment picking, overlays, voice, music and the 1080x1920 Short render.

Layout (1080x1920, YouTube Shorts UI safe): banner 110-300 · clip box 330-1210 (clip fills the full width when
landscape) with a blurred copy of itself behind · big "#N" badge · reaction caption · 1-5 list that fills on each
reveal (1270-1590) · bottom 330 px left to the Shorts UI. Frame 0 = the #1 clip's peak + "WAIT FOR #1".
"""
import json
import os
import random
import subprocess
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 48000
BOX_Y, BOX_H = 330, 880
LIST_Y, ROW = 1272, 64
FONT_PATHS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"]
PALETTE = [(255, 59, 48), (255, 149, 0), (0, 122, 255), (175, 82, 222), (52, 199, 89), (255, 45, 85), (0, 170, 170)]
YELLOW = (255, 221, 0)
KD = os.environ.get("KOKORO_DIR", "/opt/kokoro")


def ff(args, timeout=900):
    p = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-nostdin", "-loglevel", "error"] + args,
                       capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError("ffmpeg: " + p.stderr.decode(errors="replace")[-800:])
    return p


def probe(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                        "-of", "json", path], capture_output=True, text=True, timeout=60)
    j = json.loads(p.stdout or "{}")
    w = h = 0
    has_a = False
    for s in j.get("streams", []):
        if s.get("codec_type") == "video" and not w:
            w, h = int(s.get("width") or 0), int(s.get("height") or 0)
        if s.get("codec_type") == "audio":
            has_a = True
    return float(j.get("format", {}).get("duration") or 0), w, h, has_a


# ------------------------------------------------------------------ best moment
def _z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / (x.std() + 1e-6)


def analyse(path, step=0.125):
    """Per-step 'funny peak' curve from audio energy jumps + motion. Returns (curve, step, dur, w, h, has_audio)."""
    dur, w, h, has_a = probe(path)
    n = max(1, int(dur / step))
    fps = 1 / step
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-an", "-vf",
                          f"fps={fps},scale=64:36,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, timeout=300).stdout
    fr = np.frombuffer(raw, np.uint8)
    k = len(fr) // (64 * 36)
    fr = fr[:k * 64 * 36].reshape(k, 64 * 36).astype(np.int16)
    mot = np.zeros(n)
    if k > 1:
        d = np.abs(np.diff(fr, axis=0)).mean(1)
        m = min(n - 1, len(d))
        mot[1:m + 1] = d[:m]
    rms = np.full(n, -60.0)
    if has_a:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-vn", "-ac", "1",
                                          "-ar", "8000", "-f", "s16le", "-"], capture_output=True,
                                         timeout=300).stdout, np.int16).astype(np.float32) / 32768
        hop = int(8000 * step)
        m = min(n, len(a) // hop)
        if m:
            seg = a[:m * hop].reshape(m, hop)
            rms[:m] = 20 * np.log10(np.sqrt((seg ** 2).mean(1)) + 1e-5)
    onset = np.maximum(0, rms - np.concatenate([[rms[0]] * 2, rms[:-2]]))
    curve = 0.5 * _z(rms) + 0.9 * _z(onset) + 0.8 * _z(mot)
    if len(curve) >= 5:
        curve = np.convolve(curve, np.ones(5) / 5, mode="same")
    return curve, step, dur, w, h, has_a


def best_moment(path, length, peak_at=0.55):
    """Window of `length` s around the strongest peak (avoids the first 0.5 s and last 0.4 s: intros/end cards)."""
    curve, step, dur, w, h, has_a = analyse(path)
    lo, hi = int(0.5 / step), max(int(0.5 / step) + 1, len(curve) - int(0.4 / step))
    c = curve.copy()
    c[:lo] = -9
    c[hi:] = -9
    pk = int(np.argmax(c))
    peak = pk * step
    length = min(length, max(2.0, dur - 0.2))
    start = min(max(0.0, peak - peak_at * length), max(0.0, dur - length - 0.05))
    win = curve[int(start / step): int((start + length) / step) + 1]
    score = float(curve[pk] + 0.5 * (win.mean() if len(win) else 0))
    return {"start": round(start, 3), "peak": round(peak, 3), "len": round(length, 3), "score": score,
            "w": w, "h": h, "audio": has_a, "dur": dur}


# ------------------------------------------------------------------ overlays
def font(size):
    for f in FONT_PATHS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def _fit(draw, text, maxw, size, minsize=40, stroke=0):
    while size > minsize:
        f = font(size)
        if draw.textlength(text, font=f) + 2 * stroke <= maxw:
            return f
        size -= 4
    return font(minsize)


def _wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def _ctext(d, y, text, f, fill, stroke, sfill=(0, 0, 0)):
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)


def overlay(path, theme_name, color, sc, rank=None, caption=None, big=None, revealed=()):
    """Transparent 1080x1920 PNG. rank = current #N (badge + highlighted row); big = hook/end text."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # banner
    d.rounded_rectangle((28, 112, W - 28, 300), radius=34, fill=color + (240,), outline=(255, 255, 255, 255), width=6)
    f1 = font(46)
    _ctext(d, 124, "RANKING", f1, (255, 255, 255), 4)
    name = theme_name.upper()
    f2 = _fit(d, name, W - 110, 104, 50, 6)
    bb = d.textbbox((0, 0), name, font=f2, stroke_width=6)
    _ctext(d, 178 + (110 - (bb[3] - bb[1])) / 2 - bb[1] / 2, name, f2, YELLOW, 6)
    # 1..5 list (fills on reveal; current row highlighted)
    fl = font(50)
    for i, r in enumerate(range(1, 6)):
        y = LIST_Y + i * ROW
        cur = (r == rank)
        if cur:
            d.rounded_rectangle((40, y - 4, 900, y + ROW - 8), radius=16, fill=YELLOW + (235,))
        tag = sc["ranks"][r]["tag"] if (r in revealed or cur) else "? ? ?"
        col = (0, 0, 0) if cur else ((255, 255, 255) if r in revealed else (200, 200, 200))
        st = 0 if cur else 5
        d.text((60, y), f"#{r}", font=fl, fill=col if cur else YELLOW, stroke_width=st, stroke_fill=(0, 0, 0))
        d.text((175, y), tag, font=fl, fill=col, stroke_width=st, stroke_fill=(0, 0, 0))
    # big rank badge
    if rank:
        fb = font(230)
        d.text((34, 300), f"#{rank}", font=fb, fill=YELLOW, stroke_width=14, stroke_fill=(0, 0, 0))
    if caption:
        fc = font(68)
        lines = _wrap(d, caption.upper(), fc, W - 120)[:2]
        y0 = 1232 - len(lines) * 80
        for j, ln in enumerate(lines):
            _ctext(d, y0 + j * 80, ln, fc, (255, 255, 255), 8)
    if big:
        fbig = _fit(d, big, W - 80, 150, 70, 12)
        _ctext(d, 640, big, fbig, YELLOW, 12)
    im.save(path)
    return path


# ------------------------------------------------------------------ audio
def tts(lines, voice="am_puck", speed=1.15):
    from kokoro_onnx import Kokoro
    from scipy.signal import resample_poly
    k = Kokoro(os.path.join(KD, "kokoro.onnx"), os.path.join(KD, "voices.bin"))
    out = []
    for text in lines:
        a, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
        a = np.asarray(a, np.float32)
        nz = np.where(np.abs(a) > 0.01)[0]  # trim leading/trailing silence
        if len(nz):
            a = a[max(0, nz[0] - 200): nz[-1] + 1200]
        a = resample_poly(a, SR, sr).astype(np.float32)
        out.append(a / (np.abs(a).max() + 1e-9) * 0.9)
    return out


def music(seconds, rng):
    """Light synthesized comedy bed (no third-party music): 4-on-floor kick, hats, bouncy bass, chord stabs."""
    bpm = rng.uniform(116, 128)
    beat = 60 / bpm
    n = int(seconds * SR) + SR
    out = np.zeros(n, np.float32)
    t = np.arange(int(SR * 0.4)) / SR
    kick = (np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 9)).astype(np.float32)
    th = np.arange(int(SR * 0.05)) / SR
    hat = (np.random.default_rng(rng.randint(0, 999)).standard_normal(len(th)) * np.exp(-th * 90)).astype(np.float32)
    hat = np.diff(hat, prepend=0) * 0.5
    root = rng.choice([48, 50, 53, 55, 57])  # midi
    prog = [0, 7, 9, 5]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa

    def put(sig, at):
        i = int(at * SR)
        if i < n:
            j = min(n, i + len(sig))
            out[i:j] += sig[:j - i]

    nb = int(seconds / beat) + 2
    for b in range(nb):
        at = b * beat
        put(kick * 0.9, at)
        put(hat * 0.35, at + beat / 2)
        put(hat * 0.18, at + beat / 4 * 3)
        ch = prog[(b // 4) % 4]
        bt = np.arange(int(SR * beat * 0.45)) / SR
        f = hz(root - 12 + ch + (12 if b % 2 else 0))
        bass = (np.sign(np.sin(2 * np.pi * f * bt)) * 0.3 + np.sin(2 * np.pi * f * bt)) * np.exp(-bt * 7)
        put(bass.astype(np.float32) * 0.35, at)
        if b % 2 == 1:
            st = np.arange(int(SR * 0.18)) / SR
            stab = sum(np.sin(2 * np.pi * hz(root + 12 + ch + iv) * st) for iv in (0, 4, 7)) * np.exp(-st * 18)
            put(stab.astype(np.float32) * 0.12, at + beat / 2)
    return out[:int(seconds * SR)]


def whoosh(rng):
    n = int(SR * 0.35)
    x = np.random.default_rng(rng.randint(0, 999)).standard_normal(n).astype(np.float32)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    # crude rising band-pass: running mean difference
    k = np.linspace(40, 3, n).astype(int)
    y = np.array([x[max(0, i - k[i]):i + 1].mean() for i in range(n)], np.float32)
    return (y / (np.abs(y).max() + 1e-9) * env * 0.5).astype(np.float32)


def clip_audio(path, start, length, has_a):
    n = int(round(length * SR))
    if not has_a:
        return np.zeros(n, np.float32)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", f"{length:.3f}",
                          "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, timeout=300).stdout
    a = np.frombuffer(raw, np.float32).copy()
    a = np.pad(a, (0, max(0, n - len(a))))[:n]
    loud = a[np.abs(a) > 0.003]
    if len(loud) > SR * 0.2:  # bring every clip to about -19 dBFS RMS (max +15 dB boost)
        rms = np.sqrt((loud ** 2).mean())
        a *= min(10 ** (15 / 20), 10 ** (-19 / 20) / (rms + 1e-9))
    return a


def _env(x, win):
    e = (np.abs(x) > 0.02).astype(np.float32)
    return np.clip(np.convolve(e, np.ones(win) / win, mode="same") * 3, 0, 1)


# ------------------------------------------------------------------ render
def render_segment(src, start, length, out, ov, ov_end=None, end_from=None, intro=False, fw=W, fh=608, punch_seed=0):
    cy = BOX_Y + BOX_H // 2
    if intro:
        z = f"(1.22-0.12*t/{length:.2f})"
    else:
        ph = 1.1 + (punch_seed % 3) * 0.2
        z = f"((1+0.015*t)*if(lt(mod(t+{punch_seed % 2}*{ph:.2f},{2 * ph:.2f}),{ph:.2f}),1.0,1.11))"
    inputs = ["-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", src,
              "-loop", "1", "-framerate", str(FPS), "-t", f"{length:.3f}", "-i", ov]
    fc = (f"[0:v]fps={FPS},setpts=PTS-STARTPTS,setsar=1,split=2[a][b];"
          f"[a]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=8:2,"
          f"scale={W}:{H},eq=brightness=-0.08:saturation=1.35[bg];"
          f"[b]scale=w='trunc({fw}*{z}/2)*2':h='trunc({fh}*{z}/2)*2':eval=frame,"
          f"eq=contrast=1.06:saturation=1.15[fg];"
          f"[bg][fg]overlay=x='(W-w)/2':y='{cy}-h/2':eval=frame[m];[m][1:v]overlay=0:0[o]")
    last = "o"
    if ov_end:
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{length:.3f}", "-i", ov_end]
        fc += f";[o][2:v]overlay=0:0:enable='gte(t,{end_from:.2f})'[o2]"
        last = "o2"
    fc += f";[{last}]" + ("" if intro else "fade=t=in:st=0:d=0.10:color=white,") + "format=yuv420p[v]"
    ff(inputs + ["-filter_complex", fc, "-map", "[v]", "-t", f"{length:.3f}", "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-an", out])
    return out


def fit(w, h):
    if not w or not h:
        return W, 608
    s = min(W / w, BOX_H / h)
    return int(w * s) // 2 * 2, int(h * s) // 2 * 2


def render_short(clips, theme_name, sc, out_mp4, work, seed=0, log=print):
    """clips: 5 dicts with file + moment (start,len,peak,w,h,audio), already ordered #5..#1."""
    t0 = time.time()
    rng = random.Random(seed)
    os.makedirs(work, exist_ok=True)
    color = rng.choice(PALETTE)
    voice = rng.choice(["am_puck", "am_puck", "am_adam", "am_eric"])
    lines = [sc["hook"]] + [sc["ranks"][r]["say"] for r in (5, 4, 3, 2, 1)] + [sc["end_say"]]
    vo = tts(lines, voice=voice, speed=1.15)
    hook_v, rank_v, end_v = vo[0], vo[1:6], vo[6]
    # timeline
    one = clips[4]
    intro_len = max(1.6, len(hook_v) / SR + 0.15)
    segs = [{"kind": "intro", "clip": one, "len": intro_len,
             "start": max(0.0, min(one["m"]["peak"] - 0.5, one["m"]["dur"] - intro_len - 0.05))}]
    for i, r in enumerate((5, 4, 3, 2, 1)):
        c = clips[i]
        base = 6.3 if r == 1 else 5.0
        need = len(rank_v[i]) / SR + (len(end_v) / SR + 1.6 if r == 1 else 0.9)
        L = max(base, need)
        L = min(L, c["m"]["dur"] - 0.05) if c["m"]["dur"] > 2.5 else L
        st = c["m"]["start"]
        if st + L > c["m"]["dur"]:
            st = max(0.0, c["m"]["dur"] - L - 0.05)
        segs.append({"kind": "rank", "rank": r, "clip": c, "len": L, "start": st})
    total = sum(s["len"] for s in segs)
    log(f"timeline {total:.1f}s, voice {voice}")
    # overlays + video segments
    files = []
    revealed = []
    ov_intro = overlay(os.path.join(work, "ov_intro.png"), theme_name, color, sc, big=sc["hook_text"])
    for k, s in enumerate(segs):
        c = s["clip"]
        fw, fh = fit(c["m"]["w"], c["m"]["h"])
        out = os.path.join(work, f"seg{k}.mp4")
        if s["kind"] == "intro":
            render_segment(c["file"], s["start"], s["len"], out, ov_intro, intro=True, fw=fw, fh=fh)
        else:
            r = s["rank"]
            ov = overlay(os.path.join(work, f"ov{r}.png"), theme_name, color, sc, rank=r,
                         caption=sc["ranks"][r]["line"], revealed=tuple(revealed))
            ov_end = end_from = None
            if r == 1:
                ov_end = overlay(os.path.join(work, "ov_end.png"), theme_name, color, sc, rank=None,
                                 caption="COMMENT BELOW", big=sc["end_text"], revealed=(1, 2, 3, 4, 5))
                end_from = s["len"] - len(end_v) / SR - 0.3
                s["end_from"] = end_from
            render_segment(c["file"], s["start"], s["len"], out, ov, ov_end, end_from, fw=fw, fh=fh, punch_seed=k)
            revealed.append(r)
        files.append(out)
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    vid = os.path.join(work, "video.mp4")
    ff(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    # audio mix
    n = int(round(total * SR))
    clip_t = np.zeros(n, np.float32)
    voice_t = np.zeros(n, np.float32)
    sfx_t = np.zeros(n, np.float32)

    def put(arr, sig, at):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if i < n:
            arr[i:j] += sig[:j - i]

    T = 0.0
    for k, s in enumerate(segs):
        a = clip_audio(s["clip"]["file"], s["start"], s["len"], s["clip"]["m"]["audio"])
        fade = int(0.03 * SR)
        a[:fade] *= np.linspace(0, 1, fade)
        a[-fade:] *= np.linspace(1, 0, fade)
        put(clip_t, a, T)
        if s["kind"] == "intro":
            put(voice_t, hook_v, 0.0)
        else:
            i = (5, 4, 3, 2, 1).index(s["rank"])
            put(voice_t, rank_v[i], T + 0.12)
            put(sfx_t, whoosh(rng), max(0, T - 0.12))
            if s["rank"] == 1:
                put(voice_t, end_v, T + s["end_from"] + 0.1)
        T += s["len"]
    bed = music(total, rng)
    env = _env(voice_t, int(0.25 * SR))
    mix = clip_t * (1 - 0.72 * env) + voice_t * 0.95 + bed * (0.16 - 0.08 * env) + sfx_t * 0.35
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    wav = os.path.join(work, "mix.wav")
    import soundfile as sf
    sf.write(wav, mix, SR)
    ff(["-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false,aresample=48000",
        "-ac", "2", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_mp4])
    log(f"rendered {out_mp4} in {time.time() - t0:.0f}s")
    return {"duration": round(total, 2), "voice": voice, "render_s": round(time.time() - t0)}

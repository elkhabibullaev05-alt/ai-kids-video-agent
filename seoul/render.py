#!/usr/bin/env python3
"""Seoul Night Remix — turns a Suno song (mp3/wav) into YouTube videos.

  render.py cover  "TITLE" out.jpg [--w 1920 --h 1080] [--seed N] [--tag "NIGHT DRIVE"]
  render.py long   song.mp3 cover.jpg out.mp4            # full song, 1920x1080, starts at the first loud moment
  render.py short  song.mp3 "HOOK TEXT" out.mp4 [--seed N] # 1080x1920, loudest ~28 s (the chorus/drop), loops
  render.py mix    out.mp4 cover.jpg song1.mp3 song2.mp3 ... # crossfaded mix + out.json with chapter times

Studio AI (2026-10-27) for this channel: viewers left in the first 30-45 s because of long ambient intros,
and the one Short kept 6 %. So: long videos start at the first loud moment (max 8 s cut), Shorts are the
loudest part of the song with bold text on frame 1, and everything is loudness-normalised to -14 LUFS.
"""
import json, math, os, random, re, subprocess, sys

FONT_CANDIDATES = ["/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                   "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]


def font(size):
    from PIL import ImageFont
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    out = subprocess.run(["fc-match", "-f", "%{file}", "sans:bold"], capture_output=True, text=True).stdout
    return ImageFont.truetype(out, size) if out else ImageFont.load_default()


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])
    return r


def duration(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout.strip())


def loudness_per_second(f):
    """RMS level (dB) for every second of the song."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", f, "-af",
                        "aresample=8000,asetnsamples=8000,astats=metadata=1:reset=1,"
                        "ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"],
                       capture_output=True, text=True)
    vals = [float(v) if v not in ("-inf", "inf") else -90.0
            for v in re.findall(r"RMS_level=(-?[\d.]+|-inf|inf)", r.stderr)]
    return vals


def first_loud(f, max_cut=8.0):
    v = loudness_per_second(f)
    if not v:
        return 0.0
    peak = max(v)
    for i, x in enumerate(v):
        if x > peak - 9:
            return float(min(i, max_cut))
    return 0.0


def loudest_window(f, length=28):
    v = loudness_per_second(f)
    if len(v) <= length:
        return 0.0
    best, start = -1e9, 0
    for i in range(0, len(v) - length):
        s = sum(v[i:i + length])
        if s > best:
            best, start = s, i
    return float(start)


# ---------------------------------------------------------------- cover
def cover(title, out, w=1920, h=1080, seed=None, tag="NIGHT DRIVE"):
    """Neon Seoul night skyline in the rain, title in big type. Our own procedural art (no stock, no logos)."""
    from PIL import Image, ImageDraw, ImageFilter
    rnd = random.Random(seed if seed is not None else title)
    hue = rnd.choice([(255, 46, 136), (0, 220, 255), (170, 70, 255), (255, 120, 40)])
    hue2 = rnd.choice([(0, 255, 200), (255, 60, 200), (80, 140, 255)])
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):  # night sky gradient
        t = y / h
        px.line([(0, y), (w, y)], fill=(int(8 + 30 * t), int(6 + 10 * t), int(28 + 40 * t)))
    glow = Image.new("RGB", (w, h))
    g = ImageDraw.Draw(glow)
    base = int(h * 0.78)
    x = 0
    while x < w:  # skyline with lit windows
        bw = rnd.randint(w // 30, w // 12)
        bh = rnd.randint(int(h * 0.15), int(h * 0.55))
        px.rectangle([x, base - bh, x + bw, h], fill=(10, 10, 22))
        for wy in range(base - bh + 10, h - 10, 14):
            for wx in range(x + 6, x + bw - 6, 12):
                if rnd.random() < 0.18:
                    c = hue if rnd.random() < 0.5 else hue2
                    g.rectangle([wx, wy, wx + 5, wy + 7], fill=c)
        if rnd.random() < 0.35:  # neon sign
            sx, sy = x + 4, base - bh + rnd.randint(10, max(11, bh // 3))
            g.rectangle([sx, sy, sx + bw - 8, sy + 10], fill=hue)
        x += bw + rnd.randint(0, 6)
    tower_x = rnd.randint(w // 5, 4 * w // 5)  # Namsan-like tower
    px.rectangle([tower_x - 4, base - int(h * 0.62), tower_x + 4, base], fill=(14, 14, 30))
    g.ellipse([tower_x - 22, base - int(h * 0.62) - 10, tower_x + 22, base - int(h * 0.62) + 14], fill=hue2)
    img = Image.composite(glow, img, glow.convert("L").point(lambda p: 255 if p else 0))
    img = Image.blend(img, Image.eval(glow.filter(ImageFilter.GaussianBlur(14)), lambda p: min(255, p * 2)), 0.35)
    road = ImageDraw.Draw(img)  # wet street reflections
    for y in range(base, h):
        t = (y - base) / (h - base)
        road.line([(0, y), (w, y)], fill=(int(12 + 20 * t), 8, int(26 + 20 * t)))
    refl = img.crop((0, base - (h - base), w, base)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(6))
    img.paste(Image.blend(img.crop((0, base, w, h)), refl, 0.55), (0, base))
    rain = ImageDraw.Draw(img)
    for _ in range(int(w * h / 2500)):
        rx, ry = rnd.randint(0, w), rnd.randint(0, h)
        rain.line([(rx, ry), (rx - 6, ry + 26)], fill=(150, 170, 220), width=1)
    d = ImageDraw.Draw(img)
    big = font(int(h * (0.13 if w > h else 0.075)))
    small = font(int(h * (0.045 if w > h else 0.03)))
    words = title.upper()
    lines, cur = [], ""
    for wd in words.split():
        if d.textlength((cur + " " + wd).strip(), font=big) > w * 0.86:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    ty = int(h * (0.16 if w > h else 0.22))
    for ln in lines:
        tw = d.textlength(ln, font=big)
        for r in (10, 6):  # neon glow
            gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).text(((w - tw) / 2, ty), ln, font=big, fill=hue + (255,))
            img.paste(gl.filter(ImageFilter.GaussianBlur(r)), (0, 0), gl.filter(ImageFilter.GaussianBlur(r)))
        d = ImageDraw.Draw(img)
        d.text(((w - tw) / 2, ty), ln, font=big, fill=(255, 255, 255), stroke_width=3, stroke_fill=(20, 0, 30))
        ty += int(big.size * 1.1)
    if tag:
        tw = d.textlength(tag, font=small)
        d.text(((w - tw) / 2, ty + 10), tag, font=small, fill=hue2, stroke_width=2, stroke_fill=(0, 0, 0))
    img.save(out, quality=92)
    return out


# ---------------------------------------------------------------- videos
def _audio(song, out_wav, start=0.0, length=None, fade_in=0.25, fade_out=0.0):
    """Step 1: cut + loudness-normalise to a wav (doing this inside the video graph deadlocks/slow-downs ffmpeg)."""
    af = [f"afade=t=in:d={fade_in}"] if fade_in else []
    if fade_out and length:
        af.append(f"afade=t=out:st={length - fade_out:.2f}:d={fade_out}")
    af.append("loudnorm=I=-14:TP=-1.5:LRA=11")
    raw = out_wav + ".raw.wav"  # decode first: mp3 -> loudnorm in one ffmpeg call hangs on ffmpeg 6.1
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{start:.2f}", "-i", song]
    if length:
        cmd += ["-t", f"{length:.2f}"]
    sh(cmd + ["-ar", "48000", "-ac", "2", raw])
    sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-af", ",".join(af) + ",aresample=48000",
        "-c:a", "pcm_s16le", out_wav])
    os.remove(raw)
    return out_wav


def _video(img, wav, out, w, h, wave_h, wave_y, fade_out_at=None):
    """Step 2: still picture + live waveform, 15 fps, ultrafast x264 (≈3x realtime on 2 cores)."""
    v = (f"[0:v]scale={w}:{h},format=yuv420p[bg];"
         f"[1:a]showwaves=s={w}x{wave_h}:mode=cline:colors=0xff3b9a|0x00e5ff:rate=15,format=rgba[wv];"
         f"[bg][wv]overlay=0:{wave_y}:shortest=1:format=auto,format=yuv420p")
    if fade_out_at:
        v += f",fade=t=out:st={fade_out_at:.2f}:d=0.4"
    sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "15", "-i", img, "-i", wav,
        "-filter_complex", v + "[v]", "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "ultrafast",
        "-crf", "28", "-maxrate", "1500k", "-bufsize", "3000k", "-tune", "stillimage", "-g", "60", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
    os.remove(wav)


def long_video(song, cover_jpg, out):
    start = first_loud(song)
    wav = _audio(song, out + ".wav", start)
    _video(cover_jpg, wav, out, 1920, 1080, 160, "H-190")
    return {"start_cut": start, "seconds": round(duration(out), 1)}


def short_video(song, hook, out, seed=None, length=28):
    start = loudest_window(song, length)
    tmp = out + ".cover.jpg"
    cover(hook, tmp, 1080, 1920, seed=seed, tag="FULL SONG ON THE CHANNEL")
    wav = _audio(song, out + ".wav", start, length, fade_in=0, fade_out=0.6)
    _video(tmp, wav, out, 1080, 1920, 220, "H-520", fade_out_at=length - 0.4)
    os.remove(tmp)
    return {"start": start, "seconds": round(duration(out), 1)}


def mix_video(out, cover_jpg, songs, xfade=4):
    """Crossfades the songs (each trimmed to its first loud moment); writes out.json with chapter start times (s)."""
    chapters, t, parts = [], 0.0, []
    for i, s in enumerate(songs):
        st = first_loud(s)
        p = f"{out}.p{i}.wav"
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{st:.2f}", "-i", s, "-ar", "48000", "-ac", "2", p])
        parts.append(p)
        chapters.append(round(max(0.0, t), 1))
        t += duration(p) - xfade
    cur = parts[0]
    for i, p in enumerate(parts[1:], 1):  # pairwise crossfade keeps memory low for 20 songs
        nxt = f"{out}.x{i}.wav"
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", cur, "-i", p, "-filter_complex",
            f"acrossfade=d={xfade}:c1=tri:c2=tri", nxt])
        if cur not in parts:
            os.remove(cur)
        cur = nxt
    wav = _audio(cur, out + ".wav", 0, fade_in=0)
    for f in parts + ([cur] if cur not in parts else []):
        os.path.exists(f) and os.remove(f)
    _video(cover_jpg, wav, out, 1920, 1080, 160, "H-190")
    total = duration(out)
    json.dump({"chapters": chapters, "seconds": round(total, 1)}, open(os.path.splitext(out)[0] + ".json", "w"))
    return {"chapters": chapters, "seconds": round(total, 1)}


def _opt(args, name, default=None, cast=str):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return cast(v)
    return default


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a.pop(0)
    if cmd == "cover":
        w, h = _opt(a, "--w", 1920, int), _opt(a, "--h", 1080, int)
        seed, tag = _opt(a, "--seed", None, int), _opt(a, "--tag", "NIGHT DRIVE")
        print(cover(a[0], a[1], w, h, seed, tag))
    elif cmd == "long":
        print(json.dumps(long_video(a[0], a[1], a[2])))
    elif cmd == "short":
        seed = _opt(a, "--seed", None, int)
        print(json.dumps(short_video(a[0], a[1], a[2], seed)))
    elif cmd == "mix":
        print(json.dumps(mix_video(a[0], a[1], a[2:])))
    else:
        sys.exit(__doc__)

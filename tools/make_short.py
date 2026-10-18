#!/usr/bin/env python3
"""Cut a vertical YouTube Short (1080x1920) out of a 16:9 long video.

    python3 tools/make_short.py LONG.mp4 OUT.mp4 --start 12 --dur 40 \
        --top "Tesla's Roadster can FLY?" --bottom "Full video on the channel"

Layout: blurred, zoomed copy of the clip as background; the clip itself (full width) in the middle;
a big headline above it and a small call-to-action below. Audio is normalised to -14 LUFS.
Needs ffmpeg + Pillow.
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONTS = [os.path.expanduser("~/.fonts/Kalam-Bold.ttf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "C:/Windows/Fonts/arialbd.ttf"]


def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def overlay_png(top, bottom, path, clip_h):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    mid_top = (H - clip_h) // 2
    # headline: up to 3 lines, as big as fits above the clip (wrapped by measured width)
    for size in (96, 84, 72, 62, 54, 46):
        f = font(size)
        lines, cur = [], ""
        for word in top.split():
            t = (cur + " " + word).strip()
            if d.textlength(t, font=f) <= W - 90:
                cur = t
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
        lines = [t for t in lines if t]
        hh = len(lines) * int(size * 1.2)
        if len(lines) <= 3 and hh < mid_top - 60:
            break
    y = (mid_top - hh) // 2
    for t in lines[:3]:
        w = d.textlength(t, font=f)
        d.text(((W - w) / 2, y), t, font=f, fill="white", stroke_width=6, stroke_fill="black")
        y += int(size * 1.2)
    if bottom:
        f2 = font(54)
        w = d.textlength(bottom, font=f2)
        yb = mid_top + clip_h + 120
        d.rounded_rectangle(((W - w) / 2 - 36, yb - 18, (W + w) / 2 + 36, yb + 78), radius=40, fill=(255, 214, 0, 235))
        d.text(((W - w) / 2, yb), bottom, font=f2, fill="black")
    img.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--dur", type=float, default=40)
    ap.add_argument("--top", default="")
    ap.add_argument("--bottom", default="Full video on the channel")
    a = ap.parse_args()
    clip_h = int(W * 9 / 16)
    with tempfile.TemporaryDirectory() as td:
        ov = os.path.join(td, "ov.png")
        overlay_png(a.top, a.bottom, ov, clip_h)
        fc = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=20:3,eq=brightness=-0.12[bg];"
              f"[b]scale={W}:{clip_h}[fg];[bg][fg]overlay=0:(H-h)/2[v1];[v1][1:v]overlay=0:0,format=yuv420p[v];"
              f"[0:a]loudnorm=I=-14:TP=-2,alimiter=limit=0.7,aresample=48000[au]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.start), "-t", str(a.dur), "-i", a.src, "-i", ov,
                        "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-r", "30", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                        a.out], check=True)
    print(a.out)


if __name__ == "__main__":
    main()

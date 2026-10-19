"""Original phonk cover art (no stock images): night scene + drift car silhouette + neon title.

python3 engine/cover.py OUT.png "TITLE" --seed 7 [--w 1920 --h 1080]   (use --w 1080 --h 1920 for Shorts)
Every seed changes palette, scene (city / mountain road / tunnel / harbor), car colour, sun/moon, smoke and title glow.
"""
import argparse
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

p = argparse.ArgumentParser()
p.add_argument("out")
p.add_argument("title")
p.add_argument("--seed", type=int, default=1)
p.add_argument("--w", type=int, default=1920)
p.add_argument("--h", type=int, default=1080)
a = p.parse_args()
R = random.Random(a.seed)
W, H = a.w, a.h
S = min(W, H) / 1080

PAL = [((12, 4, 30), (90, 10, 70), (255, 40, 140), (160, 0, 255)),
       ((2, 10, 25), (10, 60, 90), (0, 220, 255), (0, 120, 255)),
       ((20, 2, 2), (90, 10, 10), (255, 60, 30), (255, 0, 60)),
       ((5, 5, 5), (40, 40, 60), (220, 220, 255), (140, 140, 255)),
       ((10, 0, 20), (60, 0, 90), (255, 200, 40), (255, 90, 0)),
       ((0, 15, 10), (0, 70, 50), (60, 255, 160), (0, 200, 120))]
top, bot, neon, glowc = R.choice(PAL)
im = Image.new("RGB", (W, H))
d = ImageDraw.Draw(im)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
# stars
for _ in range(int(220 * S)):
    x, y = R.randrange(W), R.randrange(int(H * 0.55))
    c = R.randint(120, 255)
    d.point((x, y), fill=(c, c, c))
hor = int(H * R.uniform(0.58, 0.68))
# sun / moon
r = int(R.uniform(160, 300) * S)
cx = int(W * R.uniform(0.3, 0.7))
cy = hor - int(r * R.uniform(0.2, 0.9))
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=neon)
for k in range(7):
    yy = cy + int(r * (0.15 + k * 0.12))
    d.rectangle([cx - r, yy, cx + r, yy + int((4 + k * 2) * S)], fill=tuple(int((top[i] + bot[i]) / 2) for i in range(3)))
scene = R.choice(["city", "mountains", "harbor", "city"])
if scene == "city":
    x = 0
    while x < W:
        w = int(R.randint(50, 150) * S)
        h = int(R.randint(100, 420) * S)
        d.rectangle([x, hor - h, x + w, hor], fill=(8, 4, 16))
        for wy in range(hor - h + int(14 * S), hor - int(10 * S), int(28 * S)):
            for wx in range(x + int(8 * S), x + w - int(8 * S), int(22 * S)):
                if R.random() < 0.28:
                    d.rectangle([wx, wy, wx + int(7 * S), wy + int(11 * S)], fill=R.choice([(255, 210, 120), neon]))
        x += w + int(R.randint(0, 18) * S)
elif scene == "mountains":
    pts = [(0, hor)]
    for i in range(12):
        pts.append((W * (i + 0.5) / 12, hor - R.randint(80, 360) * S))
    pts += [(W, hor)]
    d.polygon(pts, fill=(10, 5, 20))
else:
    for i in range(14):
        x0 = int(W * i / 14)
        h = int(R.randint(60, 200) * S)
        d.rectangle([x0, hor - h, x0 + int(W / 18), hor], fill=(8, 6, 14))
        d.line([x0 + int(W / 36), hor - h, x0 + int(W / 36), hor - h - int(120 * S)], fill=(8, 6, 14), width=int(6 * S))
# road with perspective lines
vx = W // 2 + int(R.uniform(-0.15, 0.15) * W)
d.polygon([(0, H), (W, H), (vx + int(30 * S), hor), (vx - int(30 * S), hor)], fill=(18, 14, 26))
for i in range(14):
    t0, t1 = (i / 14) ** 2, ((i + 0.5) / 14) ** 2
    y0, y1 = hor + (H - hor) * t0, hor + (H - hor) * t1
    w0, w1 = 2 + 18 * t0, 2 + 18 * t1
    xa, xb = vx + (W / 2 - vx) * t0, vx + (W / 2 - vx) * t1
    d.polygon([(xa - w0 * S, y0), (xa + w0 * S, y0), (xb + w1 * S, y1), (xb - w1 * S, y1)], fill=(255, 220, 120))
# drift car silhouette (side, slightly rotated) with neon underglow + tail lights + smoke
k = S * (0.72 if H > W else 1.0)
car = Image.new("RGBA", (int(900 * k), int(330 * k)), (0, 0, 0, 0))
c = ImageDraw.Draw(car)
body = [(40, 230), (60, 175), (180, 160), (290, 95), (520, 85), (640, 150), (820, 165), (860, 200), (850, 235), (40, 245)]
c.polygon([(x * k, y * k) for x, y in body], fill=(6, 6, 10, 255))
c.polygon([(x * k, y * k) for x, y in [(310, 105), (510, 98), (600, 150), (250, 158)]], fill=(40, 40, 70, 255))
for wx in (200, 680):
    c.ellipse([(wx - 62) * k, 185 * k, (wx + 62) * k, 309 * k], fill=(2, 2, 4, 255))
    c.ellipse([(wx - 38) * k, 209 * k, (wx + 38) * k, 285 * k], fill=(60, 60, 70, 255))
c.rectangle([40 * k, 190 * k, 70 * k, 205 * k], fill=(255, 30, 40, 255))
glow = Image.new("RGBA", car.size, (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([60 * k, 250 * k, 840 * k, 320 * k], fill=glowc + (255,))
glow = glow.filter(ImageFilter.GaussianBlur(25 * S))
car = Image.alpha_composite(glow, car).rotate(R.uniform(-6, 6), resample=Image.BICUBIC, expand=True)
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(smoke)
cx0 = int(W * R.uniform(0.05, 0.12)) if H > W else int(W * R.uniform(0.18, 0.45))
cy0 = int(H * (0.78 if H > W else 0.70))
for _ in range(60):
    rr = int(R.uniform(30, 120) * S)
    x = cx0 - int(R.uniform(0, 380) * S)
    y = cy0 + int(R.uniform(-40, 80) * S)
    sd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(200, 200, 220, R.randint(10, 35)))
smoke = smoke.filter(ImageFilter.GaussianBlur(20 * S))
base = im.convert("RGBA")
base = Image.alpha_composite(base, smoke)
base.alpha_composite(car, (cx0, cy0 - car.size[1] // 2))
im = base.convert("RGB")
# title with neon glow
FONTS = ["/usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf", "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"]
import os
fp = next(f for f in FONTS if os.path.exists(f))
size = int((150 if W >= H else 120) * S)
d = ImageDraw.Draw(im)
while size > 40 and d.textlength(a.title, font=ImageFont.truetype(fp, size)) > W * 0.9:
    size -= 6
f = ImageFont.truetype(fp, size)
tw = d.textlength(a.title, font=f)
ty = int(H * (0.12 if H > W else 0.06))
gl = Image.new("RGB", (W, H))
ImageDraw.Draw(gl).text(((W - tw) / 2, ty), a.title, font=f, fill=glowc)
gl = gl.filter(ImageFilter.GaussianBlur(16 * S))
im = Image.composite(gl, im, gl.convert("L").point(lambda v: min(255, v * 2)))
d = ImageDraw.Draw(im)
d.text(((W - tw) / 2, ty), a.title, font=f, fill=(255, 240, 255))
im.save(a.out, quality=92)
print(a.out)

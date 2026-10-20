"""Thumbnail 1280x720: a rendered frame + 2-4 huge words.
python3 engine/thumb.py FRAME.png OUT.jpg "WHO DID IT?" [--color ffd21e]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

src, out, text = sys.argv[1], sys.argv[2], sys.argv[3]
col = sys.argv[sys.argv.index("--color") + 1] if "--color" in sys.argv else "ffd21e"
col = tuple(int(col[i:i + 2], 16) for i in (0, 2, 4))
FONTS = ["/usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf", "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
fp = next(f for f in FONTS if os.path.exists(f))

im = Image.open(src).convert("RGB").resize((1280, 720), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.35); im = ImageEnhance.Contrast(im).enhance(1.12)
d = ImageDraw.Draw(im)
words = text.upper().split(); lines = [" ".join(words[: (len(words) + 1) // 2]), " ".join(words[(len(words) + 1) // 2:])] if len(words) > 2 else [" ".join(words)]
size = 150
while size > 60:
    f = ImageFont.truetype(fp, size)
    if all(d.textlength(l, font=f) < 1180 for l in lines): break
    size -= 6
y = 720 - 40 - len(lines) * (size + 10)
for l in lines:
    w = d.textlength(l, font=f); x = (1280 - w) / 2
    d.text((x, y), l, font=f, fill=col, stroke_width=max(6, size // 12), stroke_fill=(0, 0, 0))
    y += size + 10
im.save(out, quality=92); print(out)

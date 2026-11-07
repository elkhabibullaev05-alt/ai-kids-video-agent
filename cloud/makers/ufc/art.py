"""Wild Sketchbook — drawing helpers: paper texture, photo -> ink/pencil sketch, fonts, text layers, thumbnail."""
import os
import random
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

INK = (38, 30, 26)
PAPER = (244, 235, 216)
YELLOW = (255, 214, 0)
RED = (200, 38, 30)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
# OFL / Apache fonts from the google/fonts repo (free to use). Downloaded once into HOME/fonts when online.
FONT_URLS = {
    "Kalam-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/kalam/Kalam-Bold.ttf",
    "PermanentMarker-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/permanentmarker/PermanentMarker-Regular.ttf",
}
FONT_DIRS = [os.path.expanduser("~/.fonts"), "/usr/local/share/fonts", "/usr/share/fonts/truetype/google-fonts"]
_font_cache = {}


def setup_fonts(home, offline=False):
    d = os.path.join(home, "fonts")
    FONT_DIRS.insert(0, d)
    if offline:
        return
    os.makedirs(d, exist_ok=True)
    for name, url in FONT_URLS.items():
        if _find(name):
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WildSketchbookBot/1.0 (owner's channel tool)"})
            data = urllib.request.urlopen(req, timeout=30).read()
            if len(data) > 10000:
                open(os.path.join(d, name), "wb").write(data)
        except Exception:
            pass


def _find(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p) and os.path.getsize(p) > 10000:
            return p
    return None


def font(kind, size):
    """kind: hand (labels), marker (hook / thumbnail), bold (captions)."""
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    order = {"hand": ["Kalam-Bold.ttf", "PermanentMarker-Regular.ttf"],
             "marker": ["PermanentMarker-Regular.ttf", "Kalam-Bold.ttf"],
             "bold": []}[kind]
    path = next((p for p in (_find(n) for n in order) if p), None) or DEJAVU + "DejaVuSans-Bold.ttf"
    f = ImageFont.truetype(path, size)
    _font_cache[key] = f
    return f


# ---------------------------------------------------------------- paper + sketch
def paper(w, h, seed=7):
    rng = np.random.default_rng(seed)
    base = np.array(PAPER, np.float32)[None, None, :] * np.ones((h, w, 1), np.float32)
    low = Image.fromarray((rng.random((h // 16 + 1, w // 16 + 1)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    low = (np.asarray(low, np.float32) / 255 - 0.5) * 14
    grain = (rng.random((h, w)).astype(np.float32) - 0.5) * 9
    fib = Image.fromarray((rng.random((h // 2, w // 2)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    fib = (np.asarray(fib.resize((w, h), Image.BILINEAR), np.float32) / 255 - 0.5) * 6
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = ((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2)
    vig = 1 - 0.22 * np.clip(vig * 2.2, 0, 1) ** 1.5
    out = (base + (low + grain + fib)[..., None]) * vig[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def sketch(photo, w, h, seed=0, centering=(0.5, 0.42), wash=0.5):
    """Photo (PIL) -> ink/pencil drawing on warm paper with a light watercolour wash. Returns uint8 HxWx3."""
    img = ImageOps.fit(photo.convert("RGB"), (w, h), Image.LANCZOS, centering=centering)
    g = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    gf = np.asarray(g, np.float32)
    rad = max(w, h) / 220
    inv_blur = np.asarray(ImageOps.invert(g).filter(ImageFilter.GaussianBlur(rad)), np.float32)
    dodge = np.clip(gf * 255 / (256 - inv_blur), 0, 255) / 255          # pencil lines (white = paper)
    dodge = np.clip(1 - (1 - dodge) * 1.9, 0, 1) ** 1.2
    # ink contour lines from a soft edge detector
    e = np.asarray(g.filter(ImageFilter.GaussianBlur(max(1.0, rad / 3))).filter(ImageFilter.FIND_EDGES), np.float32) / 255
    ink = 1 - np.clip((e - 0.06) * 5.5, 0, 0.85)
    # graphite tone + cross hatching in the shadows
    tone = np.asarray(g.filter(ImageFilter.GaussianBlur(rad * 1.5)), np.float32) / 255
    yy, xx = np.mgrid[0:h, 0:w]
    step = max(7, w // 260)
    hat1 = ((xx + yy) % step) < 1.6
    hat2 = ((xx - yy) % step) < 1.6
    shade = np.ones((h, w), np.float32)
    shade -= 0.28 * hat1 * (tone < 0.45)
    shade -= 0.28 * hat2 * (tone < 0.25)
    lum = dodge * ink * shade * (0.62 + 0.38 * np.clip(tone, 0, 1) ** 0.6)
    # watercolour wash: blurred, softened colours, slightly offset like a hand painting
    col = img.filter(ImageFilter.GaussianBlur(rad * 2.5))
    col = ImageOps.posterize(col, 4).filter(ImageFilter.GaussianBlur(rad))
    c = np.asarray(col, np.float32) / 255
    gray = c.mean(axis=2, keepdims=True)
    c = gray + (c - gray) * 1.35
    c = np.roll(c, (int(rad * 1.5), int(rad)), axis=(0, 1))
    washc = 1 - (1 - np.clip(c, 0, 1)) * wash
    pap = paper(w, h, seed).astype(np.float32) / 255
    out = pap * lum[..., None] * washc
    return np.clip(out * 255, 0, 255).astype(np.uint8)


def title_card(text, w, h, seed=0):
    """Drawn fallback when no free photo exists: the subject's name hand-lettered with a doodle frame."""
    pap = Image.fromarray(paper(w, h, seed))
    d = ImageDraw.Draw(pap)
    rng = random.Random(seed)
    for k in range(3):  # sketchy double frame
        m = int(min(w, h) * 0.08) + k * 6
        pts = [(m + rng.randint(-6, 6), m + rng.randint(-6, 6)), (w - m + rng.randint(-6, 6), m + rng.randint(-6, 6)),
               (w - m + rng.randint(-6, 6), h - m + rng.randint(-6, 6)), (m + rng.randint(-6, 6), h - m + rng.randint(-6, 6))]
        d.line(pts + [pts[0]], fill=INK, width=4)
    size = int(h * 0.16)
    f = font("hand", size)
    lines = wrap(d, text, f, w * 0.75)
    y = h / 2 - len(lines) * size * 0.6
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((w - tw) / 2, y), ln, font=f, fill=INK)
        y += size * 1.2
    return np.asarray(pap.convert("RGB"))


def placeholder_photo(title, seed):
    """Offline test only: a fake 'photo' (gradient sky, ground, a blobby animal shape)."""
    rng = random.Random(seed)
    w, h = 1600, 1067
    im = Image.new("RGB", (w, h))
    top = np.array([rng.randint(60, 200), rng.randint(120, 220), rng.randint(150, 255)], np.float32)
    bot = np.array([rng.randint(40, 120), rng.randint(80, 160), rng.randint(20, 90)], np.float32)
    t = np.linspace(0, 1, h)[:, None, None]
    arr = top * (1 - t) + bot * t
    arr = np.repeat(arr, w, axis=1)
    arr += np.random.default_rng(seed).normal(0, 10, (h, w, 3))
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(14):  # bushes / rocks
        x, y, r = rng.randint(0, w), rng.randint(h // 2, h), rng.randint(40, 160)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(rng.randint(20, 90), rng.randint(60, 130), rng.randint(20, 60)))
    cx, cy = w // 2 + rng.randint(-200, 200), int(h * 0.58)
    body = (rng.randint(90, 200), rng.randint(60, 150), rng.randint(20, 90))
    d.ellipse((cx - 330, cy - 170, cx + 330, cy + 170), fill=body)
    d.ellipse((cx + 200, cy - 300, cx + 430, cy - 80), fill=body)
    d.ellipse((cx + 330, cy - 240, cx + 370, cy - 200), fill=(250, 250, 250))
    d.ellipse((cx + 342, cy - 228, cx + 362, cy - 208), fill=(10, 10, 10))
    for lx in (-250, -120, 120, 250):
        d.rectangle((cx + lx - 25, cy + 100, cx + lx + 25, cy + 300), fill=body)
    d.text((40, 40), title, font=font("bold", 70), fill=(255, 255, 255))
    return im.filter(ImageFilter.GaussianBlur(1.2))


# ---------------------------------------------------------------- text layers (RGBA)
def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, kind, maxw, maxh, start, min_size=30, max_lines=3, spacing=1.12):
    d = ImageDraw.Draw(Image.new("L", (8, 8)))
    size = start
    while True:
        f = font(kind, size)
        lines = wrap(d, text, f, maxw)
        if (len(lines) <= max_lines and len(lines) * size * spacing <= maxh) or size <= min_size:
            return f, lines, size
        size = int(size * 0.92)


def text_layer(text, kind, maxw, maxh, start, fill=YELLOW, stroke=INK, sw=10, max_lines=3, align="center",
               spacing=1.12, rot=0.0, bg=None, pad=24):
    """Returns RGBA image of wrapped text with a thick stroke (optional rounded background)."""
    f, lines, size = fit_text(text, kind, maxw, maxh, start, max_lines=max_lines, spacing=spacing)
    d = ImageDraw.Draw(Image.new("L", (8, 8)))
    tw = int(max(d.textlength(l, font=f) for l in lines)) + 2 * sw + 2 * pad
    lh = int(size * spacing)
    th = lh * len(lines) + 2 * sw + 2 * pad + int(size * 0.25)
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    if bg:
        dd.rounded_rectangle((0, 0, tw - 1, th - 1), radius=min(40, th // 3), fill=bg)
    y = pad + sw
    for l in lines:
        lw = dd.textlength(l, font=f)
        x = (tw - lw) / 2 if align == "center" else pad + sw
        dd.text((x, y), l, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
        y += lh
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    return im


def label_layer(text, maxw=1300):
    """Handwritten caption with a yellow highlighter swipe behind it."""
    f, lines, size = fit_text(text, "hand", maxw, 150, 78, max_lines=2)
    d = ImageDraw.Draw(Image.new("L", (8, 8)))
    tw = int(max(d.textlength(l, font=f) for l in lines))
    lh = int(size * 1.1)
    W, H = tw + 90, lh * len(lines) + 50
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    rng = random.Random(text)
    for i in range(len(lines)):  # highlighter
        y0 = 25 + i * lh + int(size * 0.35)
        dd.polygon([(10, y0 + rng.randint(-6, 6)), (W - 10, y0 + rng.randint(-8, 4)),
                    (W - 18, y0 + int(size * 0.75)), (16, y0 + int(size * 0.8))], fill=(255, 220, 40, 170))
    y = 18
    for l in lines:
        lw = dd.textlength(l, font=f)
        dd.text(((W - lw) / 2, y), l, font=f, fill=INK + (255,), stroke_width=3, stroke_fill=(255, 250, 235, 255))
        y += lh
    return im.rotate(rng.uniform(-2.5, 2.5), resample=Image.BICUBIC, expand=True)


def badge_layer(num, size=230):
    """Red ink stamp '#3'."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = random.Random(num)
    for k in range(3):
        o = 8 + k * 3
        d.ellipse((o + rng.randint(-3, 3), o + rng.randint(-3, 3), size - o + rng.randint(-3, 3), size - o + rng.randint(-3, 3)),
                  outline=RED + (255,), width=7)
    d.ellipse((24, 24, size - 24, size - 24), fill=RED + (235,))
    f = font("marker", int(size * 0.42))
    tw = d.textlength(num, font=f)
    d.text(((size - tw) / 2, size * 0.24), num, font=f, fill=(255, 248, 230, 255), stroke_width=2, stroke_fill=INK + (255,))
    return im.rotate(rng.uniform(-12, 12), resample=Image.BICUBIC, expand=True)


def to_overlay(im, x, y):
    """RGBA PIL -> (x, y, rgb float32, alpha float32 [h,w,1]) for fast numpy compositing."""
    a = np.asarray(im, np.float32)
    return (int(x), int(y), a[..., :3], a[..., 3:4] / 255.0)


def composite(frame, ov, alpha_mul=1.0):
    x, y, rgb, a = ov
    H, W = frame.shape[:2]
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    sub = frame[y0:y1, x0:x1].astype(np.float32)
    rr = rgb[y0 - y:y1 - y, x0 - x:x1 - x]
    aa = a[y0 - y:y1 - y, x0 - x:x1 - x] * alpha_mul
    frame[y0:y1, x0:x1] = (sub * (1 - aa) + rr * aa).astype(np.uint8)


# ---------------------------------------------------------------- thumbnail
def thumbnail(photo_sketch_src, text, out_path):
    """photo_sketch_src: PIL photo (or None). 1280x720, colourful sketch + huge marker text."""
    W, H = 1280, 720
    if photo_sketch_src is not None:
        base = sketch(photo_sketch_src, W, H, seed=3, wash=0.85)
    else:
        base = title_card("", W, H)  # 2026-11-07: no second copy of the text behind the marker words
    im = Image.fromarray(base).convert("RGBA")
    # darken left side for contrast
    grad = Image.linear_gradient("L").rotate(90).resize((W, H))
    shade = Image.new("RGBA", (W, H), (20, 14, 8, 0))
    shade.putalpha(grad.point(lambda v: int(v * 0.55)))
    im = Image.alpha_composite(im, shade)
    t = text_layer(" ".join(text.upper().split()[:4]), "marker", 760, 560, 190, fill=YELLOW, sw=12, max_lines=3, rot=4)
    im.alpha_composite(t, (30, max(10, (H - t.height) // 2)))
    # 2026-11-07: no channel-name tag — Studio: thumbnails cluttered/text-heavy; one subject + <= 4 words
    im.convert("RGB").save(out_path, quality=92)

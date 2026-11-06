"""Drawing helpers: fonts, number formats, placeholder art, text with outline, cover/Ken-Burns crops."""
import colorsys
import hashlib
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/usr/share/fonts/TTF"]
_fc = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _fc:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                _fc[key] = ImageFont.truetype(p, size)
                break
        else:
            _fc[key] = ImageFont.load_default(size)
    return _fc[key]


# ---------------------------------------------------------------- numbers

def short_num(n):
    """88688874288 -> '88.7B', 336897 -> '336.9K', 1234 -> '1,234'."""
    n = float(n or 0)
    a = abs(n)
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if a >= div:
            v = n / div
            s = f"{v:.1f}" if abs(v) < 100 else f"{v:.0f}"
            return s.rstrip("0").rstrip(".") + suf if s.endswith(".0") else s + suf
    return f"{int(n):,}"


def say_num(n):
    """Spoken form for TTS: 88688874288 -> '88.7 billion', 336897 -> '337 thousand'."""
    n = float(n or 0)
    a = abs(n)
    if a >= 1e9:
        v = f"{n / 1e9:.1f}".rstrip("0").rstrip(".")
        return f"{v} billion"
    if a >= 1e6:
        v = f"{n / 1e6:.1f}".rstrip("0").rstrip(".")
        return f"{v} million"
    if a >= 1e4:
        return f"{round(n / 1e3)} thousand"
    if a >= 1e3:
        return f"{n / 1e3:.1f}".rstrip("0").rstrip(".") + " thousand"
    return str(int(n))


# ---------------------------------------------------------------- colours

def accent(seed):
    h = int(hashlib.md5(str(seed).encode()).hexdigest()[:6], 16) / 0xFFFFFF
    r, g, b = colorsys.hsv_to_rgb(h, 0.85, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


YELLOW = (255, 221, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (60, 230, 110)
RED = (255, 70, 70)
CYAN = (60, 200, 255)


# ---------------------------------------------------------------- text

def text_size(txt, f):
    b = f.getbbox(txt)
    return b[2] - b[0], b[3] - b[1]


def fit_font(txt, maxw, start, minsize=24):
    s = start
    while s > minsize and text_size(txt, font(s))[0] > maxw:
        s -= 4
    return font(s)


def draw_text(d, xy, txt, f, fill=WHITE, stroke=0, stroke_fill=BLACK, anchor="la", shadow=0):
    if shadow:
        d.text((xy[0] + shadow, xy[1] + shadow), txt, font=f, fill=(0, 0, 0), anchor=anchor,
               stroke_width=stroke, stroke_fill=(0, 0, 0))
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)


def wrap(txt, f, maxw):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_size(t, f)[0] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- images

def load_rgb(path, fallback_size=(768, 432)):
    try:
        im = Image.open(path)
        im.load()
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, (20, 20, 30, 255))
            im = Image.alpha_composite(bg, im)
        return im.convert("RGB")
    except Exception:
        return Image.new("RGB", fallback_size, (40, 40, 60))


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    nw, nh = max(w, int(sw * s + 0.5)), max(h, int(sh * s + 0.5))
    im = im.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return im.crop((x, y, x + w, y + h))


class KenBurns:
    """Pre-scaled source; .at(u) returns a w x h view, u in 0..1 = progress of a slow zoom/pan."""

    def __init__(self, im, w, h, zoom=(1.0, 1.18), pan=None, seed=0):
        self.w, self.h = w, h
        self.z0, self.z1 = zoom
        zmax = max(zoom) * 1.02
        self.src = cover(im, int(w * zmax), int(h * zmax))
        r = random.Random(seed)
        self.pan = pan or (r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))

    def at(self, u, extra_zoom=1.0):
        u = max(0.0, min(1.0, u))
        z = (self.z0 + (self.z1 - self.z0) * u) * extra_zoom
        sw, sh = self.src.size
        cw = min(sw, sw / z)  # src is w*zmax wide; at zoom z the view covers sw/z source pixels
        ch = cw * self.h / self.w
        px = self.pan[0] + (self.pan[2] - self.pan[0]) * u
        py = self.pan[1] + (self.pan[3] - self.pan[1]) * u
        ch = min(ch, sh)
        x = max(0.0, (sw - cw) / 2 * (1 + px))
        y = max(0.0, (sh - ch) / 2 * (1 + py))
        return self.src.resize((self.w, self.h), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def blur_bg(im, w, h, radius=28, dark=0.45, scale=1.12):
    small = cover(im, int(w * scale) // 4, int(h * scale) // 4).filter(ImageFilter.GaussianBlur(radius / 4))
    big = small.resize((int(w * scale), int(h * scale)), Image.BILINEAR)
    return Image.blend(big, Image.new("RGB", big.size, (8, 10, 24)), dark)


def rounded(size, radius, fill):
    m = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=fill)
    return m


def framed(im, border=8, color=WHITE, radius=18):
    w, h = im.size
    out = Image.new("RGBA", (w + 2 * border, h + 2 * border), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w + 2 * border - 1, h + 2 * border - 1), radius + border, fill=color)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    out.paste(im, (border, border), mask)
    return out


# ---------------------------------------------------------------- offline placeholders

def _placeholder(name, size, seed, icon=False):
    r = random.Random(seed)
    w, h = size
    c1, c2 = accent(name), accent(name + "x")
    im = Image.new("RGB", size)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(c1[i] * (1 - t) + c2[i] * t * 0.6) for i in range(3)))
    for _ in range(26):  # blocky "world"
        bw, bh = r.randint(w // 14, w // 5), r.randint(h // 10, h // 3)
        x, y = r.randint(-20, w), r.randint(h // 3, h)
        col = tuple(min(255, max(0, v + r.randint(-70, 70))) for v in c2)
        d.rectangle((x, y, x + bw, y + bh), fill=col, outline=(0, 0, 0), width=3)
    f = fit_font(name.upper(), int(w * 0.9), int(h * (0.22 if icon else 0.16)))
    draw_text(d, (w // 2, h // 2 - (0 if icon else h // 8)), name.upper(), f, WHITE, stroke=max(3, h // 70),
              anchor="mm")
    return im


def placeholder_images(games, cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
    for g in games:
        u = g["id"]
        n = g.get("clean") or g.get("name", "?")
        for key, size, icon in (("thumb", (768, 432), False), ("icon", (512, 512), True)):
            if g.get(key) and os.path.exists(g[key]):
                continue
            p = os.path.join(cache_dir, f"{u}_{key}_ph.png")
            if not os.path.exists(p):
                _placeholder(n, size, u, icon).save(p)
            g[key] = p

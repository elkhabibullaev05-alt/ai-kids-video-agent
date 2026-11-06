"""Money Story Daily — infographic drawing with PIL (no external images).

Every visual is drawn by draw_visual(layer, spec, p, d, th) into an RGBA layer of size (W, PANEL_H):
p = seconds since the scene started, d = scene length, th = theme dict (colours).
Types: big_number, bars, versus, stack, checklist, counter, line, statement, math, question.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
PANEL_H = 820          # visual panel height
CX = 510               # content centre (a little left: Shorts buttons sit on the right edge)
X0, X1 = 80, 940       # safe content span

FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/usr/share/fonts/TTF"]
_FC = {}


def _font_path(bold=True, mono=False):
    name = ("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else \
        ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return name


def font(size, bold=True, mono=False):
    k = (int(size), bold, mono)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(_font_path(bold, mono), int(size))
    return _FC[k]


def fit(text, maxw, size, bold=True, minsize=28):
    while size > minsize and font(size, bold).getlength(text) > maxw:
        size -= 4
    return font(size, bold)


def wrap(text, maxw, size, bold=True, maxlines=3, minsize=40):
    """Word-wrap into <= maxlines lines, shrinking the font until it fits."""
    while True:
        f = font(size, bold)
        lines, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if f.getlength(t) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if (len(lines) <= maxlines and all(f.getlength(l) <= maxw for l in lines)) or size <= minsize:
            return f, lines
        size -= 4


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def back(x):
    """Ease-out with a small overshoot (pop)."""
    x = clamp(x)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)


def fmt(v, prefix="$", suffix="", dec=None):
    if dec is None:
        dec = 2 if abs(v - round(v)) > 1e-6 else 0
    neg = v < 0
    s = f"{abs(v):,.{dec}f}"
    return ("-" if neg else "") + prefix + s + suffix


def decimals_of(v):
    return 2 if abs(float(v) - round(float(v))) > 1e-6 else 0


def ctext(d, xy, text, f, fill, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- icons (shapes only)
def icon(d, kind, cx, cy, s, col, bg):
    """Simple flat icons drawn with shapes. s = size (px)."""
    h = s / 2
    lw = max(4, int(s / 16))
    k = (kind or "coin").lower()
    if k in ("card", "credit"):
        d.rounded_rectangle([cx - h, cy - h * 0.65, cx + h, cy + h * 0.65], radius=s * 0.1, fill=col)
        d.rectangle([cx - h, cy - h * 0.35, cx + h, cy - h * 0.12], fill=bg)
        d.rounded_rectangle([cx - h * 0.75, cy + h * 0.15, cx - h * 0.25, cy + h * 0.4], radius=4, fill=bg)
    elif k in ("house", "rent", "home"):
        d.polygon([(cx - h, cy - h * 0.05), (cx, cy - h), (cx + h, cy - h * 0.05)], fill=col)
        d.rectangle([cx - h * 0.72, cy - h * 0.1, cx + h * 0.72, cy + h * 0.85], fill=col)
        d.rectangle([cx - h * 0.18, cy + h * 0.25, cx + h * 0.18, cy + h * 0.85], fill=bg)
    elif k in ("cart", "groceries", "shopping"):
        d.line([(cx - h, cy - h * 0.7), (cx - h * 0.6, cy - h * 0.7), (cx - h * 0.35, cy + h * 0.35),
                (cx + h * 0.7, cy + h * 0.35), (cx + h * 0.9, cy - h * 0.4), (cx - h * 0.5, cy - h * 0.4)],
               fill=col, width=lw, joint="curve")
        for x in (cx - h * 0.2, cx + h * 0.55):
            d.ellipse([x - h * 0.15, cy + h * 0.55, x + h * 0.15, cy + h * 0.85], fill=col)
    elif k in ("cup", "coffee", "lunch", "food", "takeout"):
        d.rounded_rectangle([cx - h * 0.6, cy - h * 0.55, cx + h * 0.45, cy + h * 0.8], radius=s * 0.08, fill=col)
        d.arc([cx + h * 0.2, cy - h * 0.3, cx + h * 0.95, cy + h * 0.4], -90, 90, fill=col, width=lw)
        for x in (cx - h * 0.35, cx - h * 0.05, cx + h * 0.25):
            d.line([(x, cy - h * 0.95), (x, cy - h * 0.7)], fill=col, width=lw)
    elif k in ("car", "transport"):
        d.rounded_rectangle([cx - h, cy - h * 0.1, cx + h, cy + h * 0.55], radius=s * 0.1, fill=col)
        d.polygon([(cx - h * 0.6, cy - h * 0.1), (cx - h * 0.35, cy - h * 0.6), (cx + h * 0.4, cy - h * 0.6),
                   (cx + h * 0.65, cy - h * 0.1)], fill=col)
        for x in (cx - h * 0.55, cx + h * 0.55):
            d.ellipse([x - h * 0.25, cy + h * 0.35, x + h * 0.25, cy + h * 0.85], fill=bg, outline=col, width=lw)
    elif k in ("phone", "subscription", "subscriptions", "apps"):
        d.rounded_rectangle([cx - h * 0.5, cy - h, cx + h * 0.5, cy + h], radius=s * 0.12, fill=col)
        d.rounded_rectangle([cx - h * 0.38, cy - h * 0.8, cx + h * 0.38, cy + h * 0.65], radius=s * 0.04, fill=bg)
        d.ellipse([cx - h * 0.09, cy + h * 0.73, cx + h * 0.09, cy + h * 0.91], fill=bg)
    elif k in ("piggy", "savings", "save"):
        d.ellipse([cx - h * 0.9, cy - h * 0.6, cx + h * 0.8, cy + h * 0.6], fill=col)
        d.ellipse([cx + h * 0.6, cy - h * 0.2, cx + h * 1.0, cy + h * 0.2], fill=col)
        d.polygon([(cx - h * 0.4, cy - h * 0.5), (cx - h * 0.2, cy - h * 0.95), (cx, cy - h * 0.55)], fill=col)
        for x in (cx - h * 0.55, cx + h * 0.35):
            d.rectangle([x - h * 0.12, cy + h * 0.4, x + h * 0.12, cy + h * 0.85], fill=col)
        d.rounded_rectangle([cx - h * 0.3, cy - h * 0.45, cx + h * 0.15, cy - h * 0.33], radius=3, fill=bg)
    elif k in ("calendar", "month", "date"):
        d.rounded_rectangle([cx - h * 0.85, cy - h * 0.7, cx + h * 0.85, cy + h * 0.85], radius=s * 0.08, fill=col)
        d.rectangle([cx - h * 0.7, cy - h * 0.3, cx + h * 0.7, cy + h * 0.7], fill=bg)
        for x in (cx - h * 0.45, cx + h * 0.45):
            d.rounded_rectangle([x - h * 0.08, cy - h * 0.95, x + h * 0.08, cy - h * 0.5], radius=3, fill=col)
        for i in range(3):
            for j in range(2):
                x, y = cx - h * 0.45 + i * h * 0.45, cy - h * 0.05 + j * h * 0.42
                d.rectangle([x - h * 0.12, y - h * 0.1, x + h * 0.12, y + h * 0.1], fill=col)
    elif k in ("chart", "growth", "invest"):
        for i, f in enumerate((0.35, 0.6, 0.85)):
            x = cx - h * 0.7 + i * h * 0.6
            d.rectangle([x - h * 0.2, cy + h * 0.8 - s * f * 0.85, x + h * 0.2, cy + h * 0.8], fill=col)
        d.line([(cx - h, cy + h * 0.1), (cx - h * 0.2, cy - h * 0.4), (cx + h * 0.2, cy - h * 0.15),
                (cx + h, cy - h * 0.9)], fill=col, width=lw)
    elif k in ("fire", "debt", "interest"):
        d.polygon([(cx, cy - h), (cx + h * 0.55, cy - h * 0.1), (cx + h * 0.65, cy + h * 0.45), (cx + h * 0.3, cy + h * 0.9),
                   (cx - h * 0.3, cy + h * 0.9), (cx - h * 0.65, cy + h * 0.45), (cx - h * 0.45, cy - h * 0.2),
                   (cx - h * 0.2, cy + h * 0.05)], fill=col)
        d.ellipse([cx - h * 0.25, cy + h * 0.25, cx + h * 0.25, cy + h * 0.85], fill=bg)
    elif k in ("bolt", "utilities", "power", "bills"):
        d.polygon([(cx + h * 0.15, cy - h), (cx - h * 0.55, cy + h * 0.1), (cx - h * 0.05, cy + h * 0.1),
                   (cx - h * 0.2, cy + h), (cx + h * 0.55, cy - h * 0.15), (cx + h * 0.05, cy - h * 0.15)], fill=col)
    elif k in ("shield", "emergency", "insurance"):
        d.polygon([(cx, cy - h), (cx + h * 0.8, cy - h * 0.65), (cx + h * 0.7, cy + h * 0.25), (cx, cy + h),
                   (cx - h * 0.7, cy + h * 0.25), (cx - h * 0.8, cy - h * 0.65)], fill=col)
        d.line([(cx - h * 0.35, cy), (cx - h * 0.05, cy + h * 0.3), (cx + h * 0.4, cy - h * 0.3)], fill=bg, width=lw)
    elif k in ("cap", "school", "student", "loan"):
        d.polygon([(cx - h, cy - h * 0.3), (cx, cy - h * 0.75), (cx + h, cy - h * 0.3), (cx, cy + h * 0.15)], fill=col)
        d.chord([cx - h * 0.55, cy - h * 0.4, cx + h * 0.55, cy + h * 0.7], 0, 180, fill=col)
        d.line([(cx + h * 0.8, cy - h * 0.3), (cx + h * 0.8, cy + h * 0.45)], fill=col, width=lw)
    elif k in ("bag", "wallet", "paycheck", "cash", "money"):
        d.rounded_rectangle([cx - h, cy - h * 0.55, cx + h, cy + h * 0.55], radius=s * 0.08, fill=col)
        d.ellipse([cx - h * 0.3, cy - h * 0.3, cx + h * 0.3, cy + h * 0.3], outline=bg, width=lw)
        ctext(d, (cx, cy + 2), "$", font(int(s * 0.32)), bg)
        for x in (cx - h * 0.75, cx + h * 0.75):
            d.ellipse([x - h * 0.08, cy - h * 0.08, x + h * 0.08, cy + h * 0.08], fill=bg)
    else:  # coin
        d.ellipse([cx - h, cy - h, cx + h, cy + h], fill=col)
        d.ellipse([cx - h * 0.78, cy - h * 0.78, cx + h * 0.78, cy + h * 0.78], outline=bg, width=lw)
        ctext(d, (cx, cy + 3), "$", font(int(s * 0.62)), bg)


# ---------------------------------------------------------------- visuals
def _count(spec_from, to, p, t0=0.15, dur=1.1):
    k = ease((p - t0) / dur)
    return spec_from + (to - spec_from) * k


def v_big_number(d, s, p, D, th):
    val, frm = float(s.get("value", 0)), float(s.get("from", 0))
    pre, suf = s.get("prefix", "$"), s.get("suffix", "")
    dec = decimals_of(val)
    top = 70
    if s.get("icon"):
        k = back(p / 0.45)
        icon(d, s["icon"], CX, top + 105, int(200 * max(0.05, k)), th["accent"], th["bg"])
        top += 240
    v = _count(frm, val, p)
    txt = fmt(v, pre, suf, dec)
    f = fit(fmt(val, pre, suf, dec), X1 - X0, 260)
    ctext(d, (CX, top + 140), txt, f, th["accent"] if s.get("hi", True) else th["ink"])
    y = top + 315
    if s.get("label"):
        a = ease((p - 0.5) / 0.4)
        f2, lines = wrap(s["label"], X1 - X0, 74, maxlines=2)
        for i, l in enumerate(lines):
            ctext(d, (CX, y + i * 86 + (1 - a) * 40), l, f2, mix(th["bg"], th["ink"], a))
        y += 86 * len(lines)
    if s.get("sub"):
        a = ease((p - 1.4) / 0.4)
        f3, lines = wrap(s["sub"], X1 - X0 - 60, 56, bold=False, maxlines=2)
        y += 20
        w = max(f3.getlength(l) for l in lines) + 80
        if a > 0:
            d.rounded_rectangle([CX - w / 2, y - 12, CX + w / 2, y + 70 * len(lines) + 12], radius=40,
                                fill=mix(th["bg"], th["ink"], a))
        for i, l in enumerate(lines):
            ctext(d, (CX, y + 35 + i * 70), l, f3, mix(th["ink"], th["bg"], a))


def v_bars(d, s, p, D, th):
    items = s.get("items", [])[:6]
    pre, suf = s.get("prefix", "$"), s.get("suffix", "")
    mx = max([abs(float(i["value"])) for i in items] + [1e-9])
    y = 40
    if s.get("title"):
        ctext(d, (CX, y + 30), s["title"], fit(s["title"], X1 - X0, 70), th["ink"])
        y += 120
    n = max(1, len(items))
    rowh = min(200, (PANEL_H - y - 20) / n)
    stag = min(0.45, max(0.2, (D * 0.55) / n))
    for i, it in enumerate(items):
        t0 = 0.1 + i * stag
        a = ease((p - t0) / 0.6)
        if a <= 0:
            continue
        yy = y + i * rowh
        hi = it.get("hi")
        col = th["accent"] if hi else th["ink"]
        d.text((X0, yy), it["label"], font=fit(it["label"], 600, 56), fill=mix(th["bg"], th["ink"], ease((p - t0) / 0.3)))
        bw = (X1 - X0 - 250) * abs(float(it["value"])) / mx * a
        bh = rowh * 0.42
        d.rounded_rectangle([X0, yy + 72, X0 + max(bw, 28), yy + 72 + bh], radius=int(bh * 0.3), fill=col)
        val = float(it["value"]) * a
        d.text((X0 + max(bw, 28) + 20, yy + 72 + bh / 2), fmt(val, pre, suf, decimals_of(it["value"])),
               font=font(64), fill=col, anchor="lm")


def v_versus(d, s, p, D, th):
    L, R = s.get("left", {}), s.get("right", {})
    pre, suf = s.get("prefix", "$"), s.get("suffix", "")
    mx = max(abs(float(L.get("value", 0))), abs(float(R.get("value", 0))), 1e-9)
    base, top = PANEL_H - 150, 200
    for j, (side, cx) in enumerate(((L, CX - 210), (R, CX + 210))):
        t0 = 0.1 + j * 0.9
        a = ease((p - t0) / 0.8)
        hi = side.get("hi") if "hi" in side else (j == 1)
        col = th["accent"] if hi else th["ink"]
        h = (base - top) * abs(float(side.get("value", 0))) / mx * a
        if a > 0:
            d.rounded_rectangle([cx - 130, base - max(h, 20), cx + 130, base], radius=26, fill=col)
            ctext(d, (cx, base - max(h, 20) - 60), fmt(float(side.get("value", 0)) * a, pre, suf,
                                                      decimals_of(side.get("value", 0))), fit(fmt(float(side.get("value", 0)), pre, suf), 400, 92), col)
        ctext(d, (cx, base + 55), side.get("label", ""), fit(side.get("label", ""), 400, 58), th["ink"])
        if side.get("sub"):
            ctext(d, (cx, base + 118), side["sub"], fit(side["sub"], 400, 48, bold=False), th["ink"])
    a = back((p - 0.6) / 0.4)
    if a > 0:
        r = 52 * a
        d.ellipse([CX - r, top - 120 - r, CX + r, top - 120 + r], fill=th["ink"])
        ctext(d, (CX, top - 120), "VS", font(int(44 * a) + 1), th["bg"])


SHADES = (0.0, 0.45, 0.7, 0.25, 0.85, 0.55)


def v_stack(d, s, p, D, th):
    items = s.get("items", [])[:6]
    pre = s.get("prefix", "$")
    total = float(s.get("total") or sum(float(i["value"]) for i in items) or 1)
    y = 30
    if s.get("title"):
        ctext(d, (CX, y + 30), s["title"], fit(s["title"], X1 - X0, 70), th["ink"])
        y += 110
    bx0, bx1, by0, by1 = X0, X1, y + 10, y + 170
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=28, fill=th["soft"])
    n = max(1, len(items))
    stag = min(0.55, max(0.25, D * 0.6 / n))
    x = bx0
    for i, it in enumerate(items):
        t0 = 0.15 + i * stag
        a = ease((p - t0) / 0.5)
        frac = float(it["value"]) / total
        segw = (bx1 - bx0) * frac
        hi = it.get("hi")
        col = th["accent"] if hi else mix(th["ink"], th["soft"], SHADES[i % len(SHADES)])
        if a > 0:
            d.rectangle([x, by0, x + segw * a, by1], fill=col)
            ly = by1 + 45 + i * min(100, (PANEL_H - by1 - 60) / n)
            d.rounded_rectangle([X0, ly, X0 + 56, ly + 56], radius=14, fill=col)
            tc = mix(th["bg"], th["accent"] if hi else th["ink"], a)
            d.text((X0 + 80, ly + 28), it["label"], font=fit(it["label"], 480, 58), fill=tc, anchor="lm")
            d.text((X1, ly + 28), fmt(float(it["value"]) * a, pre, "", decimals_of(it["value"])), font=font(60),
                   fill=tc, anchor="rm")
        x += segw
    # round the bar ends again (cover square corners)
    d.rounded_rectangle([bx0 - 2, by0 - 2, bx1 + 2, by1 + 2], radius=30, outline=th["bg"], width=6)


def v_checklist(d, s, p, D, th):
    items = s.get("items", [])[:6]
    y = 40
    if s.get("title"):
        ctext(d, (CX, y + 30), s["title"], fit(s["title"], X1 - X0, 72), th["ink"])
        y += 125
    n = max(1, len(items))
    stag = min(0.7, max(0.3, D * 0.7 / n))
    rowh = min(160, (PANEL_H - y) / n)
    for i, it in enumerate(items):
        if isinstance(it, str):
            it = {"text": it, "ok": True}
        t0 = 0.1 + i * stag
        a = ease((p - t0) / 0.35)
        if a <= 0:
            continue
        yy = y + i * rowh + (1 - a) * 30
        ok = it.get("ok", True)
        col = th["accent"] if ok else th["muted"]
        k = back((p - t0) / 0.35)
        r = 38 * k
        d.ellipse([X0 + 40 - r, yy + 45 - r, X0 + 40 + r, yy + 45 + r], fill=col)
        if k > 0.6:
            if ok:
                d.line([(X0 + 22, yy + 46), (X0 + 36, yy + 62), (X0 + 60, yy + 30)], fill=th["bg"], width=9, joint="curve")
            else:
                d.line([(X0 + 26, yy + 31), (X0 + 54, yy + 59)], fill=th["bg"], width=9)
                d.line([(X0 + 54, yy + 31), (X0 + 26, yy + 59)], fill=th["bg"], width=9)
        f, lines = wrap(it["text"], X1 - X0 - 110, 60, maxlines=2, minsize=38)
        tc = mix(th["bg"], th["ink"] if ok else th["muted"], a)
        for j, l in enumerate(lines):
            d.text((X0 + 105, yy + 45 + (j - (len(lines) - 1) / 2) * (f.size + 6)), l, font=f, fill=tc, anchor="lm")
        if not ok and a >= 1:
            ln = f.getlength(lines[0])
            d.line([(X0 + 100, yy + 45 - (len(lines) - 1) / 2 * (f.size + 6)),
                    (X0 + 110 + ln, yy + 45 - (len(lines) - 1) / 2 * (f.size + 6))], fill=th["muted"], width=5)


def v_counter(d, s, p, D, th):
    frm, to = float(s.get("from", 0)), float(s.get("to", 0))
    steps = int(s.get("steps", 12))
    unit = s.get("unit", "MONTH")
    pre, suf = s.get("prefix", "$"), s.get("suffix", "")
    run = max(1.2, min(D - 0.6, 3.2))
    k = clamp((p - 0.15) / run)
    n = 1 + int(round(k * (steps - 1)))
    cw, chh, top = 380, 300, 40
    d.rounded_rectangle([CX - cw / 2, top, CX + cw / 2, top + chh], radius=36, fill=th["ink"])
    d.rounded_rectangle([CX - cw / 2, top, CX + cw / 2, top + 90], radius=36, fill=th["accent"])
    d.rectangle([CX - cw / 2, top + 54, CX + cw / 2, top + 90], fill=th["accent"])
    ctext(d, (CX, top + 47), unit.upper(), font(48), th["bg"])
    ctext(d, (CX, top + 195), str(n), font(150), th["bg"])
    v = frm + (to - frm) * (n - 1) / max(1, steps - 1)
    ctext(d, (CX, top + 440), fmt(v, pre, suf, decimals_of(to)), fit(fmt(to, pre, suf), X1 - X0, 170), th["accent"])
    if s.get("label"):
        ctext(d, (CX, top + 565), s["label"], fit(s["label"], X1 - X0, 56), th["ink"])
    dots = min(steps, 12)
    gap = (X1 - X0 - 40) / dots
    for i in range(dots):
        x = X0 + 20 + gap * (i + 0.5)
        on = i < round(n * dots / steps)
        r = 20 if on else 14
        d.ellipse([x - r, top + 680 - r, x + r, top + 680 + r], fill=th["accent"] if on else th["soft"])


def v_line(d, s, p, D, th):
    pts = [float(x) for x in s.get("points", [0, 1])]
    pre, suf = s.get("prefix", "$"), s.get("suffix", "")
    gx0, gx1, gy0, gy1 = X0 + 20, X1 - 40, 170, PANEL_H - 150
    if s.get("label"):
        ctext(d, (CX, 60), s["label"], fit(s["label"], X1 - X0, 58), th["ink"])
    lo, hi = min(pts + [0]), max(pts)
    rng = (hi - lo) or 1
    d.line([(gx0, gy1), (gx1, gy1)], fill=th["soft"], width=6)
    for g in (0.33, 0.66):
        y = gy1 - (gy1 - gy0) * g
        for x in range(int(gx0), int(gx1), 40):
            d.line([(x, y), (x + 18, y)], fill=th["soft"], width=3)
    xy = [(gx0 + (gx1 - gx0) * i / max(1, len(pts) - 1), gy1 - (gy1 - gy0) * (v - lo) / rng) for i, v in enumerate(pts)]
    k = ease((p - 0.15) / max(1.2, min(D - 0.8, 3.0)))
    segs = (len(xy) - 1) * k
    m = int(segs)
    cur = xy[:m + 1]
    if m < len(xy) - 1:
        f = segs - m
        cur.append((xy[m][0] + (xy[m + 1][0] - xy[m][0]) * f, xy[m][1] + (xy[m + 1][1] - xy[m][1]) * f))
    if len(cur) >= 2:
        poly = cur + [(cur[-1][0], gy1), (cur[0][0], gy1)]
        d.polygon(poly, fill=th["soft"])
        d.line(cur, fill=th["accent"], width=14, joint="curve")
    hx, hy = cur[-1]
    d.ellipse([hx - 22, hy - 22, hx + 22, hy + 22], fill=th["accent"], outline=th["bg"], width=6)
    vi = pts[min(len(pts) - 1, m)] + ((pts[m + 1] - pts[m]) * (segs - m) if m < len(pts) - 1 else 0)
    tag = fmt(vi, pre, suf, decimals_of(pts[-1]))
    f = font(58)
    tw = f.getlength(tag) + 44
    tx = min(max(hx, X0 + tw / 2), X1 - tw / 2)
    ty = hy - 85 if hy - 85 > 110 else hy + 85
    d.rounded_rectangle([tx - tw / 2, ty - 42, tx + tw / 2, ty + 42], radius=24, fill=th["ink"])
    ctext(d, (tx, ty), tag, f, th["bg"])
    if s.get("start_label"):
        d.text((gx0, gy1 + 55), s["start_label"], font=font(44), fill=th["muted"], anchor="lm")
    if s.get("end_label"):
        d.text((gx1, gy1 + 55), s["end_label"], font=font(44), fill=th["muted"], anchor="rm")


def v_statement(d, s, p, D, th):
    top = 60
    if s.get("icon"):
        k = back(p / 0.45)
        icon(d, s["icon"], CX, top + 90, int(170 * max(0.05, k)), th["accent"], th["bg"])
        top += 220
    f, lines = wrap(s.get("text", ""), X1 - X0, 116, maxlines=4, minsize=56)
    lh = f.size * 1.18
    for i, l in enumerate(lines):
        a = ease((p - 0.08 - i * 0.18) / 0.35)
        ctext(d, (CX, top + 70 + i * lh + (1 - a) * 40), l, f, mix(th["bg"], th["ink"], a))
    yb = top + 70 + len(lines) * lh - lh * 0.35
    k = ease((p - 0.4 - len(lines) * 0.18) / 0.5)
    if k > 0:
        d.rounded_rectangle([CX - 220 * k, yb, CX + 220 * k, yb + 16], radius=8, fill=th["accent"])
    if s.get("sub"):
        a = ease((p - 1.0) / 0.4)
        f2, l2 = wrap(s["sub"], X1 - X0, 52, bold=False, maxlines=2)
        for i, l in enumerate(l2):
            ctext(d, (CX, yb + 90 + i * 64), l, f2, mix(th["bg"], th["muted"], a))


def v_math(d, s, p, D, th):
    rows = s.get("rows", [])[:4]
    n = max(1, len(rows))
    stag = min(1.0, max(0.45, D * 0.65 / n))
    y = 60
    if s.get("title"):
        ctext(d, (CX, y + 20), s["title"], fit(s["title"], X1 - X0, 58), th["ink"])
        y += 110
    rowh = min(210, (PANEL_H - y - 20) / n)
    for i, r in enumerate(rows):
        a = ease((p - 0.1 - i * stag) / 0.35)
        if a <= 0:
            continue
        last = i == n - 1
        f = fit(r, X1 - X0 - 60, 124 if last else 96)
        yy = y + i * rowh + rowh / 2
        if last:
            w = f.getlength(r) + 70
            d.rounded_rectangle([CX - w / 2 * a, yy - rowh * 0.42, CX + w / 2 * a, yy + rowh * 0.42], radius=30,
                                fill=th["accent"])
            ctext(d, (CX, yy), r, f, mix(th["accent"], th["bg"], a))
        else:
            ctext(d, (CX - (1 - a) * 60, yy), r, f, mix(th["bg"], th["ink"], a))


def v_question(d, s, p, D, th):
    top = 30
    k = back(p / 0.45)
    f, lines = wrap(s.get("text", ""), X1 - X0 - 120, 78, maxlines=4, minsize=46)
    lh = f.size * 1.22
    bh = len(lines) * lh + 110
    bw = (X1 - X0) * max(0.05, k)
    d.rounded_rectangle([CX - bw / 2, top, CX + bw / 2, top + bh], radius=48, fill=th["ink"])
    d.polygon([(CX - 160, top + bh - 2), (CX - 60, top + bh - 2), (CX - 190, top + bh + 70)], fill=th["ink"])
    if k > 0.7:
        for i, l in enumerate(lines):
            ctext(d, (CX, top + 55 + lh / 2 + i * lh), l, f, th["bg"])
    a = ease((p - 0.7) / 0.4)
    if a > 0:
        cta = s.get("cta", "Follow for daily money math")
        f2 = fit(cta, X1 - X0 - 140, 54)
        w = f2.getlength(cta) + 120
        y = top + bh + 150
        d.rounded_rectangle([CX - w / 2, y, CX + w / 2, y + 100], radius=50, fill=mix(th["bg"], th["accent"], a))
        ctext(d, (CX + 30, y + 50), cta, f2, th["bg"])
        d.ellipse([CX - w / 2 + 30, y + 26, CX - w / 2 + 78, y + 74], outline=th["bg"], width=6)
        d.line([(CX - w / 2 + 54, y + 38), (CX - w / 2 + 54, y + 62)], fill=th["bg"], width=6)
        d.line([(CX - w / 2 + 42, y + 50), (CX - w / 2 + 66, y + 50)], fill=th["bg"], width=6)


VIS = {"big_number": v_big_number, "bars": v_bars, "versus": v_versus, "stack": v_stack, "checklist": v_checklist,
       "counter": v_counter, "line": v_line, "statement": v_statement, "math": v_math, "question": v_question}


def draw_visual(layer, spec, p, D, th):
    d = ImageDraw.Draw(layer)
    VIS.get(spec.get("type"), v_statement)(d, spec, p, D, th)

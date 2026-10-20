"""Hand-drawn ink look: wobbly 'boiling' lines on paper, a stick-figure cast and a prop library (cairo)."""
import math
import random

import cairocffi as cairo

W, H = 1920, 1080
INK = (0.11, 0.10, 0.09)
PAPER = (0.957, 0.937, 0.890)

PAL = {  # flat, slightly muted fills
    "red": (0.86, 0.33, 0.27), "orange": (0.95, 0.60, 0.25), "yellow": (0.98, 0.83, 0.35),
    "green": (0.47, 0.70, 0.40), "teal": (0.33, 0.64, 0.66), "blue": (0.38, 0.56, 0.82),
    "navy": (0.20, 0.27, 0.45), "purple": (0.58, 0.45, 0.72), "pink": (0.93, 0.60, 0.66),
    "brown": (0.55, 0.38, 0.24), "tan": (0.85, 0.72, 0.53), "grey": (0.62, 0.62, 0.60),
    "dark": (0.30, 0.30, 0.30), "white": (1, 1, 1), "skin": (1, 1, 1), "black": INK,
    "gold": (0.90, 0.72, 0.20), "sky": (0.70, 0.84, 0.93), "sea": (0.40, 0.62, 0.80),
    "money": (0.56, 0.76, 0.50), "paper": PAPER,
}


def col(c):
    if c is None:
        return None
    if isinstance(c, str):
        return PAL.get(c, PAL["grey"])
    return tuple(c)


class Pen:
    """Draws with a tremble that changes every `boil` step, like redrawn animation frames."""

    def __init__(self, ctx, boil=0, amp=2.2):
        self.c = ctx
        self.boil = boil
        self.amp = amp
        self.uid = 0

    # -- noise ------------------------------------------------------------
    def _j(self, key):
        r = random.Random(hash((key, self.boil)) & 0xFFFFFFFF)
        return r.uniform(-1, 1), r.uniform(-1, 1)

    def _wobble(self, pts, closed=False, step=26):
        self.uid += 1
        uid = self.uid
        out = []
        seq = list(pts) + ([pts[0]] if closed else [])
        for i in range(len(seq) - 1):
            (x0, y0), (x1, y1) = seq[i], seq[i + 1]
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for k in range(n):
                t = k / n
                jx, jy = self._j((uid, i, k))
                out.append((x0 + (x1 - x0) * t + jx * self.amp, y0 + (y1 - y0) * t + jy * self.amp))
        if not closed:
            jx, jy = self._j((uid, "end"))
            out.append((seq[-1][0] + jx * self.amp, seq[-1][1] + jy * self.amp))
        return out

    def _path(self, pts, closed):
        c = self.c
        c.move_to(*pts[0])
        if len(pts) > 2:
            for i in range(1, len(pts) - 1):  # smooth through midpoints
                mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
                c.curve_to(pts[i][0], pts[i][1], pts[i][0], pts[i][1], mx, my)
            c.line_to(*pts[-1])
        else:
            c.line_to(*pts[-1])
        if closed:
            c.close_path()

    # -- primitives ---------------------------------------------------------
    def shape(self, pts, fill=None, w=5, stroke=True, closed=True, alpha=1.0, color=None):
        c = self.c
        if fill is not None and closed:
            fp = self._wobble(pts, True, step=40)
            dx, dy = self._j((self.uid, "fill"))
            c.save()
            c.translate(dx * 2.5 + 3, dy * 2.5 + 2)
            self._path(fp, True)
            r, g, b = col(fill)
            c.set_source_rgba(r, g, b, alpha)
            c.fill()
            c.restore()
        if stroke and w > 0:
            sp = self._wobble(pts, closed)
            self._path(sp, closed)
            r, g, b = col(color) if color else INK
            c.set_source_rgba(r, g, b, alpha)
            c.set_line_width(w)
            c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.stroke()

    def line(self, pts, w=5, color=None, alpha=1.0):
        self.shape(pts, None, w, True, False, alpha, color)

    def circle(self, cx, cy, r, fill=None, w=5, alpha=1.0, n=None, color=None):
        n = n or max(10, int(r / 4))
        pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.shape(pts, fill, w, True, True, alpha, color)

    def ellipse(self, cx, cy, rx, ry, fill=None, w=5, alpha=1.0):
        n = max(12, int(max(rx, ry) / 4))
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.shape(pts, fill, w, True, True, alpha)

    def rect(self, x, y, w_, h_, fill=None, w=5, alpha=1.0):
        self.shape([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)], fill, w, True, True, alpha)

    def arc(self, cx, cy, r, a0, a1, w=5, color=None):
        n = max(6, int(abs(a1 - a0) * r / 18))
        pts = [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.line(pts, w, color)

    def dot(self, x, y, r=6, color=None):
        c = self.c
        jx, jy = self._j(("dot", round(x), round(y)))
        c.arc(x + jx, y + jy, r, 0, 2 * math.pi)
        rr, g, b = col(color) if color else INK
        c.set_source_rgb(rr, g, b)
        c.fill()

    def text(self, s, x, y, size=60, color=None, align="center", font="Kalam", bold=True, outline=None, alpha=1.0):
        if "|" in s:  # multi-line text: "LINE ONE|LINE TWO"
            parts = s.split("|")
            for k, part in enumerate(parts):
                self.text(part, x, y + (k - (len(parts) - 1) / 2) * size * 1.1, size, color, align, font, bold, outline, alpha)
            return
        c = self.c
        c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(size)
        xb, yb, tw, th, _, _ = c.text_extents(s)
        tx = x - (tw / 2 + xb if align == "center" else (tw + xb if align == "right" else 0))
        ty = y - (th / 2 + yb)
        jx, jy = self._j(("txt", s))
        c.move_to(tx + jx * 0.8, ty + jy * 0.8)
        c.text_path(s)
        if outline:
            r, g, b = col(outline)
            c.set_source_rgba(r, g, b, alpha)
            c.set_line_width(size * 0.16)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.stroke_preserve()
        r, g, b = col(color) if color else INK
        c.set_source_rgba(r, g, b, alpha)
        c.fill()
        return tw


# ------------------------------------------------------------------------- stick figure
ARMS = {  # absolute screen angles in degrees for (upper arm, forearm) of the right and left arm, figure facing right
    "stand": ((75, 95), (105, 85)),
    "point": ((-5, -5), (105, 85)),
    "pointup": ((-55, -75), (105, 85)),
    "shrug": ((50, -30), (130, 210)),
    "panic": ((-60, -80), (-120, -100)),
    "think": ((40, -118), (105, 85)),
    "hold": ((40, -10), (60, -10)),
    "wave": ((-50, -100), (105, 85)),
    "cry": ((-10, -150), (190, -30)),
    "facepalm": ((-20, -160), (105, 85)),
    "present": ((10, -10), (170, 190)),
    "fist": ((-70, -95), (105, 85)),
    "hips": ((40, 140), (140, 40)),
    "type": ((60, 0), (80, 0)),
    "run": ((30, -40), (150, 100)),
}
FACES = {  # brow tilt, mouth
    "happy": (0, "smile"), "grin": (-4, "grin"), "sad": (12, "frown"), "worried": (14, "wavy"),
    "shock": (-10, "o"), "angry": (-16, "frown"), "neutral": (0, "line"), "smug": (-8, "smirk"),
    "confused": (8, "wavy"), "tired": (6, "line"), "cry": (14, "frown"), "scream": (-12, "big_o"),
}


def guy(p, x, y, s=1.0, pose="stand", face="neutral", look=1, t=0.0, extras=(), shirt=None, walk=False, label=None):
    """Stick figure standing on (x, y). look = 1 faces right, -1 left."""
    c = p.c
    c.save()
    c.translate(x, y)
    c.scale(s * look, s)
    w = 6
    bob = math.sin(t * 2.2) * 2.5
    head_y = -290 + bob
    neck = (0, -238 + bob)
    hip = (0, -110)
    # legs
    if walk:
        ph = math.sin(t * 7)
        p.line([hip, (18 * ph, -55), (34 * ph, 0)], w)
        p.line([hip, (-18 * ph, -55), (-34 * ph, 0)], w)
    else:
        p.line([hip, (22, -55), (34, 0)], w)
        p.line([hip, (-22, -55), (-30, 0)], w)
    # body / shirt
    if shirt:
        p.shape([(-30, -232 + bob), (30, -232 + bob), (26, -105), (-26, -105)], shirt, 5)
    else:
        p.line([neck, hip], w)
    # arms
    # head
    p.circle(0, head_y, 52, "white", 6)
    amp0 = p.amp
    p.amp = 0.7
    tilt, mouth = FACES.get(face, FACES["neutral"])
    ex = 20
    blink = (t % 3.3) < 0.12
    for sx in (-1, 1):
        exx = ex * sx + 8
        if blink:
            p.line([(exx - 7, head_y - 8), (exx + 7, head_y - 8)], 4)
        else:
            p.dot(exx, head_y - 8, 5.5)
        p.line([(exx - 11, head_y - 24 - tilt * 0.6 * (-sx)), (exx + 11, head_y - 24 + tilt * 0.6 * (-sx))], 4)
    my = head_y + 22
    if mouth == "smile":
        p.arc(8, my - 12, 16, 0.3, math.pi - 0.3, 4)
    elif mouth == "grin":
        p.shape([(-10, my - 4), (26, my - 4), (8, my + 12)], "white", 4)
    elif mouth == "frown":
        p.arc(8, my + 10, 15, math.pi + 0.4, 2 * math.pi - 0.4, 4)
    elif mouth == "wavy":
        p.line([(-8, my), (0, my - 5), (8, my), (16, my - 5), (24, my)], 4)
    elif mouth == "o":
        p.circle(8, my + 2, 8, None, 4, n=10)
    elif mouth == "big_o":
        p.ellipse(8, my + 4, 12, 15, (0.3, 0.1, 0.1), 4)
    elif mouth == "smirk":
        p.line([(-6, my + 2), (14, my), (24, my - 8)], 4)
    else:
        p.line([(-6, my), (22, my)], 4)
    p.amp = amp0
    if face == "cry":
        for k in range(2):
            p.dot(28 - k * 34, head_y + 10 + (t * 60 % 40), 5, "blue")
    if face in ("shock", "scream", "worried"):
        p.line([(58, head_y - 40), (66, head_y - 28)], 3, "blue")
        p.dot(68, head_y - 22, 4, "blue")
    ra, la = ARMS.get(pose, ARMS["stand"])
    wav = math.sin(t * 9) * 22 if pose in ("wave", "panic") else 0
    sh = (0, -215 + bob)
    for (a1, a2), sgn in ((ra, 1), (la, -1)):
        a1r = math.radians(a1 + wav * sgn)
        a2r = math.radians(a2 + wav * 0.7 * sgn)
        e = (sh[0] + 72 * math.cos(a1r), sh[1] + 72 * math.sin(a1r))
        hnd = (e[0] + 66 * math.cos(a2r), e[1] + 66 * math.sin(a2r))
        p.line([sh, e, hnd], w)
    # extras
    for ex_ in extras:
        if ex_ == "tie":
            p.shape([(0, -232 + bob), (8, -222 + bob), (5, -170 + bob), (0, -160 + bob), (-5, -170 + bob), (-8, -222 + bob)], "red", 3)
        elif ex_ == "glasses":
            p.circle(-12 + 8, head_y - 8, 13, None, 3, n=10)
            p.circle(28 + 8, head_y - 8, 13, None, 3, n=10)
            p.line([(9, head_y - 8), (23, head_y - 8)], 3)
        elif ex_ == "tophat":
            p.rect(-34, head_y - 120, 68, 74, "black", 4)
            p.rect(-56, head_y - 52, 112, 10, "black", 4)
        elif ex_ == "cap":
            p.shape([(-50, head_y - 26), (-42, head_y - 56), (0, head_y - 66), (42, head_y - 56), (50, head_y - 26)], "red", 4)
            p.shape([(30, head_y - 30), (90, head_y - 26), (50, head_y - 40)], "red", 4)
        elif ex_ == "hardhat":
            p.shape([(-52, head_y - 22), (-44, head_y - 58), (0, head_y - 70), (44, head_y - 58), (52, head_y - 22)], "yellow", 4)
        elif ex_ == "hair":
            p.line([(-30, head_y - 44), (-10, head_y - 62), (6, head_y - 48), (22, head_y - 64), (40, head_y - 42)], 5)
        elif ex_ == "bun":
            p.circle(-30, head_y - 52, 20, "brown", 4)
        elif ex_ == "crown":
            p.shape([(-36, head_y - 46), (-36, head_y - 92), (-18, head_y - 70), (0, head_y - 98), (18, head_y - 70), (36, head_y - 92), (36, head_y - 46)], "gold", 4)
        elif ex_ == "briefcase":
            p.rect(60, -150, 70, 52, "brown", 4)
        elif ex_ == "sweat":
            p.dot(-50, head_y - 10, 6, "blue")
    c.restore()
    if label:
        p.text(label, x, y + 40, 40, "dark", font="Patrick Hand", bold=False)


# ------------------------------------------------------------------------- props
def prop(p, name, x, y, s=1.0, t=0.0, color=None, text=None):
    c = p.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    fn = PROPS.get(name)
    if fn:
        fn(p, t, color, text)
    else:
        p.rect(-60, -60, 120, 120, color or "grey")
        p.text(name, 0, 0, 30)
    c.restore()


def _gaspump(p, t, color, text):
    p.rect(-70, -260, 140, 260, color or "red")
    p.rect(-48, -232, 96, 70, "white")
    p.text(text or "$4.33", 0, -197, 34, "red")
    p.rect(-58, -10, 116, 14, "dark")
    p.line([(70, -200), (110, -200), (120, -120), (100, -60)], 6)
    p.rect(88, -70, 24, 40, "dark", 4)


def _car(p, t, color, text):
    p.shape([(-150, -40), (-130, -95), (-70, -110), (-40, -160), (60, -160), (100, -110), (150, -95), (160, -40)], color or "blue")
    p.rect(-25, -150, 40, 38, "sky", 4)
    p.rect(25, -150, 45, 38, "sky", 4)
    for wx in (-90, 95):
        p.circle(wx, -30, 30, "dark", 5)
        p.circle(wx, -30, 10, "grey", 3)


def _truck(p, t, color, text):
    p.rect(-200, -190, 260, 150, color or "white")
    if text:
        p.text(text, -70, -115, 40)
    p.shape([(60, -150), (130, -150), (165, -100), (165, -40), (60, -40)], "red")
    p.rect(80, -140, 55, 38, "sky", 4)
    for wx in (-150, -60, 115):
        p.circle(wx, -30, 30, "dark", 5)


def _ship(p, t, color, text):
    roll = math.sin(t * 1.6) * 4
    c = p.c
    c.save()
    c.rotate(math.radians(roll * 0.3))
    p.shape([(-260, -80), (260, -80), (210, 0), (-210, 0)], color or "red")
    for i, cc in enumerate(["blue", "orange", "green", "yellow", "teal"]):
        p.rect(-200 + i * 72, -140, 66, 58, cc, 4)
    p.rect(150, -210, 70, 130, "white")
    c.restore()


def _barrel(p, t, color, text):
    p.rect(-55, -150, 110, 150, color or "dark")
    p.line([(-55, -110), (55, -110)], 4)
    p.line([(-55, -40), (55, -40)], 4)
    p.text(text or "OIL", 0, -75, 34, "white")


def _dollar(p, t, color, text):
    p.rect(-110, -55, 220, 110, color or "money")
    p.circle(0, 0, 34, None, 4)
    p.text(text or "$", 0, 2, 50)


def _wallet(p, t, color, text):
    p.rect(-100, -70, 200, 140, color or "brown")
    p.rect(30, -30, 80, 60, "tan", 4)
    p.dot(70, 0, 7)
    if text:
        p.text(text, -30, 0, 34, "white")


def _cart(p, t, color, text):
    p.shape([(-120, -150), (110, -150), (85, -40), (-95, -40)], color or "grey")
    p.line([(-120, -150), (-150, -190), (-185, -190)], 6)
    for i in range(1, 4):
        p.line([(-120 + i * 58, -150), (-110 + i * 50, -40)], 3)
    p.circle(-70, -10, 18, "dark", 4)
    p.circle(60, -10, 18, "dark", 4)


def _plane(p, t, color, text):
    p.shape([(-230, -10), (180, -10), (240, -40), (180, -70), (-200, -60)], color or "white")
    p.shape([(-40, -40), (40, -40), (-40, 70)], "blue")
    p.shape([(-200, -60), (-170, -140), (-140, -60)], "blue")
    for i in range(6):
        p.circle(-120 + i * 45, -40, 8, "sky", 3)


def _building(p, t, color, text):
    p.shape([(-200, -300), (0, -380), (200, -300)], color or "tan")
    p.rect(-200, -300, 400, 300, color or "tan")
    for i in range(5):
        p.rect(-170 + i * 72, -270, 26, 250, "white", 4)
    if text:
        p.rect(-120, -360, 240, 48, "white", 3)
        p.text(text, 0, -336, 36)


def _chart(p, t, color, text):
    p.rect(-220, -300, 440, 300, "white")
    p.line([(-190, -30), (-190, -280)], 4)
    p.line([(-190, -30), (200, -30)], 4)
    pts = [(-180, -60), (-110, -80), (-40, -70), (30, -130), (100, -150), (170, -250)]
    p.line(pts, 8, color or "red")
    p.shape([(150, -270), (190, -260), (165, -225)], color or "red", 3)
    if text:
        p.text(text, 0, -265, 40, color or "red")


def _thermo(p, t, color, text):
    p.rect(-26, -330, 52, 300, "white")
    lvl = 0.75 + 0.05 * math.sin(t * 3)
    p.rect(-14, -40 - 270 * lvl, 28, 270 * lvl, "red", 0)
    p.circle(0, -20, 44, "red")
    if text:
        p.text(text, 80, -330 + 300 * (1 - lvl), 40, "red", align="left")


def _globe(p, t, color, text):
    p.circle(0, -150, 150, "sea")
    p.shape([(-90, -230), (-20, -260), (20, -200), (-30, -150), (-100, -170)], "green", 4)
    p.shape([(30, -120), (110, -150), (120, -60), (60, -40)], "green", 4)


def _house(p, t, color, text):
    p.rect(-140, -200, 280, 200, color or "tan")
    p.shape([(-170, -195), (0, -330), (170, -195)], "red")
    p.rect(-30, -110, 60, 110, "brown", 4)
    p.rect(-110, -160, 50, 46, "sky", 4)
    p.rect(60, -160, 50, 46, "sky", 4)


def _coffee(p, t, color, text):
    p.shape([(-60, -140), (60, -140), (45, 0), (-45, 0)], color or "white")
    p.arc(70, -80, 32, -1.5, 1.5, 6)
    for k in range(3):
        p.line([(-25 + k * 25, -160 - (t * 30 % 20)), (-15 + k * 25, -190), (-25 + k * 25, -215)], 4, "grey")
    if text:
        p.text(text, 0, -70, 34)


def _bread(p, t, color, text):
    p.shape([(-120, 0), (-130, -60), (-90, -110), (90, -110), (130, -60), (120, 0)], color or "tan")
    for k in range(3):
        p.line([(-60 + k * 50, -95), (-40 + k * 50, -60)], 4)
    if text:
        p.text(text, 0, -150, 40, "red")


def _fire(p, t, color, text):
    f = math.sin(t * 10) * 8
    p.shape([(-60, 0), (-70, -60), (-30, -100 - f), (-10, -60), (10, -150 + f), (40, -70), (60, -110 - f), (70, -30), (60, 0)], "orange")
    p.shape([(-30, 0), (-30, -40), (0, -80 + f), (20, -40), (30, 0)], "yellow", 3)


def _sun(p, t, color, text):
    p.circle(0, 0, 70, "yellow")
    for k in range(10):
        a = 2 * math.pi * k / 10 + t * 0.3
        p.line([(95 * math.cos(a), 95 * math.sin(a)), (130 * math.cos(a), 130 * math.sin(a))], 5)


def _cloud(p, t, color, text):
    for cx, cy, r in ((-70, 0, 55), (0, -30, 70), (70, 0, 55)):
        p.circle(cx, cy, r, color or "white")


def _desk(p, t, color, text):
    p.rect(-260, -170, 520, 40, color or "brown")
    p.rect(-240, -130, 40, 130, color or "brown", 4)
    p.rect(200, -130, 40, 130, color or "brown", 4)
    if text:
        p.rect(-130, -230, 260, 60, "white", 4)
        p.text(text, 0, -200, 36)


def _tv(p, t, color, text):
    p.rect(-240, -320, 480, 290, "dark")
    p.rect(-215, -295, 430, 240, color or "blue", 4)
    p.line([(-60, -30), (-100, 0)], 6)
    p.line([(60, -30), (100, 0)], 6)
    p.rect(-215, -110, 430, 55, "red", 3)
    p.text(text or "BREAKING NEWS", 0, -83, 34, "white")


def _strait(p, t, color, text):
    p.rect(-420, -280, 840, 280, "sea")
    p.shape([(-420, -280), (-120, -280), (-60, -210), (-140, -150), (-420, -170)], "tan")
    p.shape([(420, -280), (110, -280), (60, -200), (150, -110), (420, -60), (420, 0), (100, 0)], "tan")
    if text:
        p.text(text, 0, -40, 40, "white", outline="dark")


def _calendar(p, t, color, text):
    p.rect(-110, -240, 220, 240, "white")
    p.rect(-110, -240, 220, 60, color or "red")
    p.text(text or "NOV", 0, -210, 40, "white")
    for r in range(3):
        for k in range(4):
            p.dot(-70 + k * 46, -140 + r * 45, 5)


def _ballot(p, t, color, text):
    p.rect(-120, -180, 240, 180, color or "blue")
    p.rect(-60, -200, 120, 26, "dark", 4)
    p.text(text or "VOTE", 0, -90, 50, "white")
    p.rect(-40, -260 - (t * 40 % 30), 80, 70, "white", 4)


def _moneybag(p, t, color, text):
    p.shape([(-40, -200), (40, -200), (25, -170), (95, -110), (100, -20), (60, 0), (-60, 0), (-100, -20), (-95, -110), (-25, -170)], color or "tan")
    p.text(text or "$", 0, -80, 70, "green")


def _scale(p, t, color, text):
    tilt = math.sin(t * 1.5) * 8
    p.line([(0, 0), (0, -260)], 6)
    p.rect(-60, -10, 120, 14, "dark", 4)
    a = math.radians(tilt)
    lx, ly, rx, ry = -150 * math.cos(a), -260 - 150 * math.sin(a), 150 * math.cos(a), -260 + 150 * math.sin(a)
    p.line([(lx, ly), (rx, ry)], 6)
    for px, py in ((lx, ly), (rx, ry)):
        p.line([(px, py), (px - 50, py + 90)], 3)
        p.line([(px, py), (px + 50, py + 90)], 3)
        p.shape([(px - 60, py + 90), (px + 60, py + 90), (px + 40, py + 115), (px - 40, py + 115)], "gold", 4)


def _arrowup(p, t, color, text):
    p.shape([(-40, 0), (40, 0), (40, -140), (90, -140), (0, -240), (-90, -140), (-40, -140)], color or "red")
    if text:
        p.text(text, 0, 50, 46, color or "red")


def _arrowdown(p, t, color, text):
    p.shape([(-40, -240), (40, -240), (40, -100), (90, -100), (0, 0), (-90, -100), (-40, -100)], color or "green")
    if text:
        p.text(text, 0, 50, 46, color or "green")


def _pricetag(p, t, color, text):
    p.shape([(-100, -50), (60, -50), (110, 0), (60, 50), (-100, 50)], color or "yellow")
    p.circle(55, 0, 9, "white", 3)
    p.text(text or "$$$", -20, 2, 40)


def _egg(p, t, color, text):
    p.ellipse(0, -60, 45, 60, "white")
    if text:
        p.text(text, 0, -160, 40, "red")


def _podium(p, t, color, text):
    p.shape([(-90, -170), (90, -170), (70, 0), (-70, 0)], color or "navy")
    p.line([(-20, -170), (-40, -230)], 4)
    p.circle(-44, -238, 10, "dark", 3)
    if text:
        p.text(text, 0, -90, 34, "white")


def _speech(p, t, color, text):
    """Speech bubble; text is what it says."""
    p.shape([(-180, -160), (180, -160), (180, -40), (-40, -40), (-90, 10), (-80, -40), (-180, -40)], color or "white")
    s = text or "..."
    p.text(s, 0, -100, min(42, int(600 / max(1, len(s)))))


def _bomb(p, t, color, text):
    p.circle(0, -70, 70, "dark")
    p.line([(40, -130), (70, -170), (100, -165)], 5)
    p.dot(105, -168, 9 + 3 * math.sin(t * 20), "orange")


def _houseofgov(p, t, color, text):
    p.rect(-260, -200, 520, 200, color or "white")
    p.shape([(-280, -200), (0, -290), (280, -200)], color or "white")
    p.circle(0, -340, 70, "white")
    p.line([(0, -410), (0, -470)], 5)
    for i in range(7):
        p.line([(-230 + i * 76, -190), (-230 + i * 76, -10)], 5)
    if text:
        p.text(text, 0, 40, 40)


def _sportscar(p, t, color, text):
    p.shape([(-200, -30), (-195, -70), (-120, -90), (-40, -135), (40, -140), (110, -100), (200, -80), (215, -30)], color or "white")
    p.shape([(-30, -125), (35, -130), (90, -98), (-60, -95)], "dark")
    p.line([(-200, -60), (200, -60)], 3)
    for wx in (-125, 135):
        p.circle(wx, -28, 30, "dark", 5)
        p.circle(wx, -28, 11, "grey", 3)
    if text:
        p.text(text, 0, -175, 40, "red")


def _rocket(p, t, color, text):
    p.shape([(0, -330), (55, -230), (55, -40), (-55, -40), (-55, -230)], color or "white")
    p.circle(0, -210, 24, "sky", 4)
    p.shape([(-55, -110), (-100, -20), (-55, -40)], "red")
    p.shape([(55, -110), (100, -20), (55, -40)], "red")
    fl = 30 + 15 * math.sin(t * 20)
    p.shape([(-30, -40), (0, -40 + fl + 40), (30, -40)], "orange")
    if text:
        p.text(text, 0, -360, 40, "dark")


def _stopwatch(p, t, color, text):
    p.rect(-18, -330, 36, 30, "dark", 4)
    p.circle(0, -170, 130, color or "white")
    a = t * 6
    p.line([(0, -170), (60 * math.sin(a), -170 - 60 * math.cos(a))], 7)
    p.dot(0, -170, 9)
    if text:
        p.text(text, 0, -72, 40, "red")


def _tank(p, t, color, text):
    p.rect(-55, -280, 110, 280, color or "grey")
    p.rect(-18, -310, 36, 34, "dark", 4)
    if text:
        p.text(text, 0, -140, 34, "white", outline="dark")


def _fan(p, t, color, text):
    p.circle(0, -120, 110, color or "white")
    for k in range(3):
        a = t * 12 + k * 2.094
        p.shape([(0, -120), (85 * math.cos(a - 0.35), -120 + 85 * math.sin(a - 0.35)), (85 * math.cos(a + 0.35), -120 + 85 * math.sin(a + 0.35))], "grey")
    p.dot(0, -120, 12)
    if text:
        p.text(text, 0, 30, 40, "dark")


def _trophy(p, t, color, text):
    p.shape([(-80, -260), (80, -260), (60, -150), (20, -120), (20, -60), (-20, -60), (-20, -120), (-60, -150)], color or "gold")
    p.rect(-60, -60, 120, 40, "brown", 4)
    if text:
        p.text(text, 0, -200, 34, "dark")


def _phone(p, t, color, text):
    p.rect(-90, -330, 180, 330, "dark")
    p.rect(-75, -305, 150, 260, color or "white", 4)
    p.circle(0, -22, 10, "grey", 3)
    if text:
        p.text(text, 0, -180, min(34, int(240 / max(1, len(text)))), "dark")


def _laptop(p, t, color, text):
    p.rect(-200, -300, 400, 250, "dark")
    p.rect(-180, -282, 360, 214, color or "white", 4)
    p.shape([(-240, -50), (240, -50), (270, 0), (-270, 0)], "grey")
    if text:
        p.text(text, 0, -180, 36, "dark")


def _envelope(p, t, color, text):
    p.rect(-150, -200, 300, 200, color or "white")
    p.line([(-150, -200), (0, -90), (150, -200)], 5)
    if text:
        p.text(text, 0, -40, 30, "dark")


def _robot(p, t, color, text):
    p.line([(0, -330), (0, -380)], 5)
    p.circle(0, -390, 14, "red", 4)
    p.rect(-110, -330, 220, 170, color or "teal")
    p.circle(-45, -260, 22, "white", 4); p.circle(45, -260, 22, "white", 4)
    p.dot(-45, -260, 8); p.dot(45, -260, 8)
    p.line([(-40, -200), (40, -200)], 6)
    p.rect(-80, -150, 160, 150, color or "teal")
    if text:
        p.text(text, 0, -75, 30, "white", outline="dark")


def _lock(p, t, color, text):
    p.arc(0, -160, 70, math.pi, 2 * math.pi, 14)
    p.rect(-110, -160, 220, 160, color or "gold")
    p.circle(0, -95, 16, "dark", 3)
    if text:
        p.text(text, 0, -35, 30, "dark")


def _eye(p, t, color, text):
    p.shape([(-170, -120), (-90, -200), (0, -225), (90, -200), (170, -120), (90, -40), (0, -15), (-90, -40)], "white")
    p.circle(0, -120, 62, color or "blue", 4)
    p.circle(0, -120, 26, "black", 3)
    if text:
        p.text(text, 0, 30, 34, "dark")


def _megaphone(p, t, color, text):
    p.shape([(-150, -170), (-60, -170), (130, -260), (130, -20), (-60, -110), (-150, -110)], color or "red")
    p.rect(-110, -110, 40, 90, "dark")
    if text:
        p.text(text, 0, -300, 34, "dark")


def _clipboard(p, t, color, text):
    p.rect(-140, -360, 280, 360, color or "tan")
    p.rect(-110, -330, 220, 300, "white", 4)
    p.rect(-50, -380, 100, 40, "grey", 4)
    for k in range(5):
        p.line([(-80, -235 + k * 45), (80, -235 + k * 45)], 4)
    if text:
        p.text(text, 0, -300, min(44, int(320 / max(1, len(text)))), "dark")


def _baseball(p, t, color, text):
    p.circle(0, -90, 90, color or "white", 5)
    p.arc(-120, -90, 70, -0.9, 0.9, 4, color="red")
    p.arc(120, -90, 70, math.pi - 0.9, math.pi + 0.9, 4, color="red")
    if text:
        p.text(text, 0, -210, 34, "dark")


def _bat(p, t, color, text):
    p.shape([(-12, 0), (12, 0), (16, -120), (34, -400), (26, -430), (-26, -430), (-34, -400), (-16, -120)], color or "tan")
    p.ellipse(0, 4, 24, 10, "brown", 4)
    if text:
        p.text(text, 0, -470, 34, "dark")


def _scoreboard(p, t, color, text):
    p.rect(-14, -120, 28, 120, "grey", 4)
    p.rect(-260, -420, 520, 300, color or "dark")
    p.rect(-235, -395, 470, 250, "navy", 3)
    if text:
        parts = text.split("|")
        for k, line in enumerate(parts):
            p.text(line, 0, -330 + k * 90 + (45 if len(parts) == 1 else 0), min(70, int(900 / max(1, len(line)))), "yellow")


def _school(p, t, color, text):
    p.rect(-260, -300, 520, 300, color or "tan")
    p.shape([(-290, -300), (0, -430), (290, -300)], "red")
    p.rect(-14, -500, 6, 80, "dark", 3)
    p.shape([(-8, -500), (60, -485), (-8, -470)], "blue")
    for k in (-190, -100, 100, 190):
        p.rect(k - 32, -250, 64, 64, "sky", 4)
    p.rect(-45, -130, 90, 130, "brown", 4)
    p.circle(0, -360, 26, "white", 4)
    if text:
        p.text(text, 0, -175, min(40, int(560 / max(1, len(text)))), "dark")


def _backpack(p, t, color, text):
    p.arc(0, -230, 50, math.pi, 2 * math.pi, 10)
    p.rect(-100, -240, 200, 240, color or "blue")
    p.rect(-70, -110, 140, 90, "white", 4)
    p.line([(-100, -170), (100, -170)], 4)
    if text:
        p.text(text, 0, -65, min(34, int(240 / max(1, len(text)))), "dark")


def _barrier(p, t, color, text):
    for k in (-200, 200):
        p.line([(k, 0), (k, -200)], 10)
    p.rect(-240, -200, 480, 70, color or "red")
    for k in range(-200, 220, 80):
        p.shape([(k - 20, -200), (k + 20, -200), (k - 20, -130), (k - 60, -130)], "white")
    if text:
        p.text(text, 0, -240, 34, "dark")


def _chalkboard(p, t, color, text):
    p.rect(-320, -520, 640, 380, "brown")
    p.rect(-295, -495, 590, 330, color or "dark", 3)
    p.line([(-200, 0), (-160, -140)], 8); p.line([(200, 0), (160, -140)], 8)
    if text:
        parts = text.split("|")
        for k, line in enumerate(parts):
            p.text(line, 0, -400 + k * 85 + (60 if len(parts) == 1 else 0), min(64, int(1000 / max(1, len(line)))), "white")


def _chip(p, t, color, text):
    for k in range(-3, 4):
        x = k * 42
        p.line([(x, -300), (x, -340)], 8); p.line([(x, 0), (x, 40)], 8)
        p.line([(-160, -150 + k * 42), (-200, -150 + k * 42)], 8); p.line([(160, -150 + k * 42), (200, -150 + k * 42)], 8)
    p.rect(-160, -300, 320, 300, color or "dark")
    p.rect(-90, -220, 180, 140, "grey", 4)
    if text:
        p.text(text, 0, -150, 40, "white", outline="dark")


def _balloon(p, t, color, text):
    p.line([(0, -260), (10, -150), (-10, -60), (0, 0)], 4)
    p.circle(0, -420, 160, color or "red", 6)
    p.shape([(-18, -262), (18, -262), (0, -240)], color or "red")
    if text:
        p.text(text, 0, -420, 44, "white", outline="dark")


def _tanker(p, t, color, text):
    roll = math.sin(t * 1.4) * 3
    c = p.c
    c.save()
    c.rotate(math.radians(roll * 0.3))
    p.shape([(-300, -90), (280, -90), (320, -60), (250, 0), (-250, 0)], color or "dark")
    p.rect(-260, -120, 420, 30, "red", 4)
    for k in range(4):
        p.circle(-200 + k * 100, -120, 22, "grey", 4)
    p.rect(180, -230, 80, 140, "white")
    p.rect(195, -210, 50, 30, "sky", 3)
    p.rect(205, -270, 20, 40, "dark", 3)
    if text:
        p.text(text, -20, -45, 40, "white", outline="dark")
    c.restore()


def _pipeline(p, t, color, text):
    p.rect(-420, -110, 840, 70, color or "grey")
    for k in range(-3, 4):
        p.rect(k * 120 - 14, -122, 28, 94, "dark", 4)
    for k in range(-2, 3):
        p.line([(k * 160, -40), (k * 160, 0)], 8)
    if text:
        p.text(text, 0, -170, 44, "dark")

def _satellite(p, t, color, text):
    p.rect(-55, -235, 110, 110, color or "grey")
    for sx in (-1, 1):
        p.rect(sx * 215 - 95, -210, 190, 60, "navy", 4)
        p.line([(sx * 55, -180), (sx * 120, -180)], 5)
    p.line([(0, -235), (0, -290)], 5)
    p.circle(0, -298, 12 + 3 * math.sin(t * 6), "red", 3)
    if text:
        p.text(text, 0, -100, 36, "dark")


def _drone(p, t, color, text):
    p.rect(-70, -150, 140, 50, color or "dark")
    for sx in (-1, 1):
        p.line([(sx * 70, -130), (sx * 150, -160)], 6)
        w = 60 * abs(math.sin(t * 25 + sx))
        p.line([(sx * 150 - w, -170), (sx * 150 + w, -170)], 5)
    p.line([(-40, -100), (-55, -70)], 5)
    p.line([(40, -100), (55, -70)], 5)
    if text:
        p.text(text, 0, -40, 36, "dark")


def _sign(p, t, color, text):
    p.line([(0, 0), (0, -200)], 9)
    p.rect(-110, -460, 220, 270, color or "white")
    p.text("SPEED", 0, -415, 34, "dark")
    p.text("LIMIT", 0, -375, 34, "dark")
    p.text(text or "100", 0, -280, min(110, int(330 / max(1, len(text or "100")))), "dark")


def _dish(p, t, color, text):
    p.line([(0, 0), (0, -120)], 8)
    p.line([(-40, 0), (40, 0)], 8)
    p.shape([(-90, -150), (90, -150), (60, -100), (-60, -100)], color or "white")
    p.line([(0, -150), (0, -200)], 4)
    p.dot(0, -205, 8)
    if text:
        p.text(text, 0, -240, 36, "dark")


def _flag(p, t, color, text):
    p.line([(0, 0), (0, -420)], 9)
    wv = 8 * __import__("math").sin(t * 3)
    p.shape([(0, -420), (300, -420 + wv), (300, -220 + wv), (0, -220)], color or "green")
    p.shape([(150, -400), (280, -320), (150, -240), (20, -320)], "yellow")
    p.circle(150, -320, 52, "blue")
    if text:
        p.text(text, 150, -460, 40, "dark")


PROPS = {
    "flag": _flag, "satellite": _satellite, "drone": _drone, "sign": _sign, "dish": _dish,
    "chip": _chip, "balloon": _balloon, "tanker": _tanker, "pipeline": _pipeline,
    "gaspump": _gaspump, "car": _car, "truck": _truck, "ship": _ship, "barrel": _barrel, "dollar": _dollar,
    "wallet": _wallet, "cart": _cart, "plane": _plane, "building": _building, "chart": _chart, "thermo": _thermo,
    "globe": _globe, "house": _house, "coffee": _coffee, "bread": _bread, "fire": _fire, "sun": _sun, "cloud": _cloud,
    "desk": _desk, "tv": _tv, "strait": _strait, "calendar": _calendar, "ballot": _ballot, "moneybag": _moneybag,
    "scale": _scale, "arrowup": _arrowup, "arrowdown": _arrowdown, "pricetag": _pricetag, "egg": _egg,
    "podium": _podium, "speech": _speech, "bomb": _bomb, "capitol": _houseofgov,
    "sportscar": _sportscar, "rocket": _rocket, "stopwatch": _stopwatch, "tank": _tank, "fan": _fan, "trophy": _trophy,
    "phone": _phone, "laptop": _laptop, "envelope": _envelope, "robot": _robot, "lock": _lock, "eye": _eye,
    "megaphone": _megaphone, "clipboard": _clipboard,
    "baseball": _baseball, "bat": _bat, "scoreboard": _scoreboard,
    "school": _school, "backpack": _backpack, "barrier": _barrier, "chalkboard": _chalkboard,
}

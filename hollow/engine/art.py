"""Hollowmere art: gothic ink-storybook backgrounds, characters and creatures as SVG.

World coordinates: 1920 x 1080 (ground line ~ y 900). Everything is original.
Static parts (backgrounds) are drawn once per shot; characters/creatures every frame.
"""
import math, random

INK = "#080504"
BONE = "#e9dcc4"
EYE_RED = "#ff2a14"


def f(v):
    return f"{v:.1f}"


# ---------------------------------------------------------------- path helpers
def poly(pts, close=True):
    s = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    return s + (" Z" if close else "")


def smooth(pts, close=True):
    """quadratic curves through midpoints -> organic ink shapes"""
    if len(pts) < 3:
        return poly(pts, close)
    p = pts + ([pts[0], pts[1]] if close else [])
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    s = f"M{f(mid(p[0], p[1])[0])},{f(mid(p[0], p[1])[1])}"
    for i in range(1, len(p) - 1):
        m = mid(p[i], p[i + 1])
        s += f" Q{f(p[i][0])},{f(p[i][1])} {f(m[0])},{f(m[1])}"
    return s + (" Z" if close else "")


def jag(pts, amp, rnd, n=2):
    """add ragged ink noise between points"""
    out = []
    m = len(pts)
    for i in range(m):
        a, b = pts[i], pts[(i + 1) % m]
        out.append(a)
        for k in range(1, n + 1):
            u = k / (n + 1)
            nx, ny = -(b[1] - a[1]), b[0] - a[0]
            ln = math.hypot(nx, ny) or 1
            d = rnd.uniform(-amp, amp)
            out.append((a[0] + (b[0] - a[0]) * u + nx / ln * d, a[1] + (b[1] - a[1]) * u + ny / ln * d))
    return out


def taper(x0, y0, x1, y1, w0, w1, bend, rnd, segs=6):
    """tapered, slightly crooked limb from (x0,y0) to (x1,y1) as polygon"""
    left, right = [], []
    for i in range(segs + 1):
        u = i / segs
        x = x0 + (x1 - x0) * u + math.sin(u * math.pi) * bend + rnd.uniform(-2, 2) * (i not in (0, segs))
        y = y0 + (y1 - y0) * u
        w = w0 + (w1 - w0) * u
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    return left + right[::-1]


def twisted_tree(x, base, h, w, rnd, branches=5):
    """gnarled tree silhouette: trunk + crooked branches, returns path d"""
    parts = []
    lean = rnd.uniform(-0.18, 0.18) * h
    trunk = taper(x, base + 10, x + lean, base - h, w, w * 0.18, rnd.uniform(-0.25, 0.25) * w * 2, rnd, 8)
    # roots
    for side in (-1, 1):
        for k in range(2):
            rx = x + side * (w * 0.6 + k * w * 0.5)
            parts.append(smooth(taper(x + side * w * 0.2, base - 8, rx, base + 8 + k * 6, w * 0.35, 3, side * 6, rnd, 4)))
    parts.append(smooth(trunk))
    for b in range(branches):
        u = rnd.uniform(0.35, 0.92)
        bx, by = x + lean * u, base - h * u
        side = rnd.choice((-1, 1))
        L = h * rnd.uniform(0.18, 0.42) * (1.1 - u * 0.4)
        ang = math.radians(rnd.uniform(15, 65))
        ex, ey = bx + side * math.cos(ang) * L, by - math.sin(ang) * L
        parts.append(smooth(taper(bx, by, ex, ey, w * 0.28 * (1 - u * 0.5), 2, rnd.uniform(-20, 20), rnd, 5)))
        # twigs
        for _ in range(rnd.randint(1, 3)):
            v = rnd.uniform(0.4, 0.95)
            tx, ty = bx + (ex - bx) * v, by + (ey - by) * v
            tl = L * rnd.uniform(0.2, 0.45)
            ta = ang + rnd.uniform(-0.9, 0.9)
            parts.append(poly(taper(tx, ty, tx + side * math.cos(ta) * tl, ty - math.sin(ta) * tl, 4, 1, rnd.uniform(-6, 6), rnd, 3)))
    return " ".join(parts)


# ---------------------------------------------------------------- backgrounds
PAL = {   # sky top, sky horizon, far trees, mid trees, ground, fog colour, moon?
    "forest":    ("#0c0605", "#5e2410", "#2a120b", "#140907", "#0e0806", "#c87a45", False),
    "clearing":  ("#0d0605", "#6a2a10", "#2e140b", "#160a07", "#120a07", "#d08850", False),
    "swamp":     ("#070a09", "#2f3a1c", "#18200f", "#0c110a", "#0a0d08", "#9fb07a", True),
    "graveyard": ("#06080c", "#2c3448", "#171c28", "#0c0f16", "#0b0d10", "#9aa6c0", True),
    "chapel":    ("#09060d", "#3a2546", "#1c1424", "#100b16", "#0d0a10", "#b49ac8", True),
    "mill":      ("#0b0505", "#5a1c14", "#28100c", "#150807", "#100807", "#c86a50", False),
    "village":   ("#05070c", "#22304a", "#141b2a", "#0b0f18", "#0a0c12", "#8fa2c8", True),
    "cave":      ("#050403", "#2a1a10", "#1a100a", "#0e0806", "#0a0605", "#a07a50", False),
    "lighthouse":("#05080b", "#2a3a46", "#16212a", "#0b1218", "#0a0e12", "#a8bccb", True),
    "sea":       ("#04070a", "#22323e", "#121c24", "#0a1218", "#081014", "#9fb4c4", True),
    "manor":     ("#08060a", "#33243a", "#1a1420", "#0f0b14", "#0c0a0e", "#b09cc0", True),
}
NO_TREES = ("lighthouse", "sea")
BACKGROUNDS = list(PAL)


def bg_defs():
    s = ""
    for k, p in PAL.items():
        s += (f'<linearGradient id="sky_{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{p[0]}"/>'
              f'<stop offset="70%" stop-color="{p[1]}"/><stop offset="100%" stop-color="{p[1]}"/></linearGradient>')
    s += ('<radialGradient id="moonglow" r="50%"><stop offset="0%" stop-color="#f4ecd8" stop-opacity="0.55"/>'
          '<stop offset="40%" stop-color="#d8d0c0" stop-opacity="0.12"/><stop offset="100%" stop-color="#d8d0c0" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="warm" r="50%"><stop offset="0%" stop-color="#ffb04a" stop-opacity="0.55"/>'
          '<stop offset="45%" stop-color="#ff7a20" stop-opacity="0.16"/><stop offset="100%" stop-color="#ff6010" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="redglow" r="50%"><stop offset="0%" stop-color="#ff3a1a" stop-opacity="0.9"/>'
          '<stop offset="35%" stop-color="#ff2010" stop-opacity="0.35"/><stop offset="100%" stop-color="#ff1000" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="ambglow" r="50%"><stop offset="0%" stop-color="#ffc060" stop-opacity="0.9"/>'
          '<stop offset="35%" stop-color="#ffa030" stop-opacity="0.35"/><stop offset="100%" stop-color="#ff9020" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="paleglow" r="50%"><stop offset="0%" stop-color="#e8f0ff" stop-opacity="0.8"/>'
          '<stop offset="40%" stop-color="#c0d0ff" stop-opacity="0.25"/><stop offset="100%" stop-color="#a0b0ff" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="greenglow" r="50%"><stop offset="0%" stop-color="#b0ff6a" stop-opacity="0.85"/>'
          '<stop offset="40%" stop-color="#80e040" stop-opacity="0.3"/><stop offset="100%" stop-color="#60c020" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="flame" r="50%"><stop offset="0%" stop-color="#fff6c8"/><stop offset="45%" stop-color="#ffc24a"/>'
          '<stop offset="100%" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>'
          )
    for k, p in PAL.items():
        s += (f'<linearGradient id="fog_{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{p[5]}" stop-opacity="0"/>'
              f'<stop offset="50%" stop-color="{p[5]}" stop-opacity="1"/><stop offset="100%" stop-color="{p[5]}" stop-opacity="0"/></linearGradient>')
    return s


def ground_line(rnd, base=900, amp=18):
    pts = [(-200, 1300)]
    for x in range(-200, 2201, 120):
        pts.append((x, base + math.sin(x / 300 + rnd.random()) * amp + rnd.uniform(-6, 6)))
    pts.append((2200, 1300))
    return pts


def grass(rnd, base, color, n=70, h=(14, 46)):
    d = []
    for _ in range(n):
        x = rnd.uniform(-100, 2020)
        y = base + rnd.uniform(-6, 30)
        for k in range(rnd.randint(2, 4)):
            hh = rnd.uniform(*h)
            lean = rnd.uniform(-14, 14)
            d.append(poly([(x + k * 5 - 3, y), (x + k * 5 + lean, y - hh), (x + k * 5 + 3, y)]))
    return f'<path d="{" ".join(d)}" fill="{color}"/>'


def background(kind, seed=1):
    """full static background for a shot (sky, moon, far/mid trees, ground, props, foreground frame)"""
    rnd = random.Random(seed * 7919 + hash(kind) % 1000)
    p = PAL.get(kind, PAL["forest"])
    g = [f'<rect x="-300" y="-300" width="2520" height="1680" fill="url(#sky_{kind})"/>']
    if p[6]:
        mx, my = rnd.uniform(1250, 1650), rnd.uniform(170, 260)
        g.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r="420" fill="url(#moonglow)"/>')
        g.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r="92" fill="#efe6d0"/>')
        g.append(f'<circle cx="{f(mx+22)}" cy="{f(my-14)}" r="18" fill="#d8ccb0" opacity="0.6"/>'
                 f'<circle cx="{f(mx-30)}" cy="{f(my+26)}" r="11" fill="#d8ccb0" opacity="0.5"/>')
    else:
        # ember horizon glow
        g.append('<ellipse cx="960" cy="820" rx="1300" ry="420" fill="url(#warm)" opacity="0.7"/>')
    if kind in NO_TREES:
        return sea_background(kind, rnd, p, "".join(g))
    # far trees
    d = []
    for i in range(26):
        x = -100 + i * 85 + rnd.uniform(-30, 30)
        d.append(twisted_tree(x, 860, rnd.uniform(420, 700), rnd.uniform(14, 26), rnd, 4))
    g.append(f'<path d="{" ".join(d)}" fill="{p[2]}"/>')
    g.append(f'<rect x="-300" y="560" width="2520" height="260" fill="url(#fog_{kind})" opacity="0.10"/>')
    # props behind mid layer
    g.append(props(kind, rnd, p))
    # mid trees
    d = []
    xs = [rnd.uniform(-80, 300), rnd.uniform(1550, 2000)] + [rnd.uniform(200, 1700) for _ in range(3)]
    for x in xs:
        d.append(twisted_tree(x, 905, rnd.uniform(650, 950), rnd.uniform(34, 58), rnd, 7))
    g.append(f'<path d="{" ".join(d)}" fill="{p[3]}"/>')
    # ground
    gl = ground_line(rnd)
    g.append(f'<path d="{smooth(gl)}" fill="{p[4]}"/>')
    g.append(grass(rnd, 905, p[4], 90))
    # path of light dirt in the middle
    g.append(f'<ellipse cx="960" cy="960" rx="760" ry="70" fill="{p[1]}" opacity="0.10"/>')
    # stones & mushrooms
    d = []
    for _ in range(9):
        x, y = rnd.uniform(0, 1920), rnd.uniform(925, 1040)
        r = rnd.uniform(10, 30)
        d.append(smooth(jag([(x - r, y), (x - r * 0.6, y - r * 0.8), (x + r * 0.5, y - r * 0.9), (x + r, y)], r * 0.12, rnd, 1)))
    g.append(f'<path d="{" ".join(d)}" fill="{INK}" opacity="0.8"/>')
    # low fog
    for k in range(4):
        y = 880 + k * 35
        g.append(f'<ellipse cx="{f(rnd.uniform(200,1700))}" cy="{y}" rx="{f(rnd.uniform(500,900))}" ry="40" fill="{p[5]}" opacity="0.045"/>')
    # foreground frame: big black trunks + brambles
    d = [twisted_tree(rnd.uniform(-120, -40), 1120, 1300, 120, rnd, 6),
         twisted_tree(rnd.uniform(1960, 2060), 1120, 1300, 120, rnd, 6)]
    for _ in range(14):
        x = rnd.choice([rnd.uniform(-60, 380), rnd.uniform(1540, 1980)])
        d.append(smooth(taper(x, 1110, x + rnd.uniform(-160, 160), 1110 - rnd.uniform(80, 240), 16, 2, rnd.uniform(-40, 40), rnd, 6)))
    g.append(f'<path d="{" ".join(d)}" fill="{INK}"/>')
    # hanging branches top
    d = []
    for _ in range(8):
        x = rnd.uniform(-50, 1970)
        d.append(smooth(taper(x, -40, x + rnd.uniform(-120, 120), rnd.uniform(60, 190), 22, 2, rnd.uniform(-30, 30), rnd, 6)))
    g.append(f'<path d="{" ".join(d)}" fill="{INK}"/>')
    return "".join(g)


def sea_background(kind, rnd, p, sky):
    g = [sky]
    # distant waves band
    g.append(f'<rect x="-300" y="640" width="2520" height="800" fill="{p[2]}"/>')
    for k in range(14):
        y = 650 + k * 30
        g.append(f'<path d="M-300,{y} ' + " ".join(f"Q{x+60},{y-10-k} {x+120},{y}" for x in range(-300, 2300, 120)) + f'" stroke="{p[5]}" stroke-width="2" fill="none" opacity="{0.05+0.01*k:.2f}"/>')
    if kind == "lighthouse":
        # cliff island + tower + keeper's cottage
        g.append(f'<path d="{smooth(jag([(-300,1300),(-300,760),(300,700),(700,640),(1100,650),(1500,720),(1900,780),(2220,820),(2220,1300)], 18, rnd, 2))}" fill="{p[3]}"/>')
        x = 1280
        g.append(f'<path d="M{x-70},660 L{x-48},250 L{x+48},250 L{x+70},660 Z" fill="{p[2]}" stroke="{INK}" stroke-width="6"/>')
        g.append(f'<rect x="{x-62}" y="200" width="124" height="54" fill="{INK}"/><path d="M{x-70},200 L{x},140 L{x+70},200 Z" fill="{INK}"/>')
        g.append(f'<rect x="{x-44}" y="208" width="88" height="40" fill="#1a1a14"/>')
        for k in range(3):
            g.append(f'<rect x="{x-60}" y="{330+k*100}" width="120" height="16" fill="{INK}" opacity="0.6"/>')
        g.append(f'<path d="M{x-420},700 L{x-420},600 L{x-330},540 L{x-240},600 L{x-240},700 Z" fill="{p[3]}" stroke="{INK}" stroke-width="5"/>'
                 f'<rect x="{x-360}" y="620" width="34" height="40" fill="#000"/>')
        # ground for characters
        g.append(f'<path d="{smooth(ground_line(rnd, 905, 14))}" fill="{p[4]}"/>')
        g.append(grass(rnd, 905, p[4], 60))
    else:
        # deck of a ship in the foreground: planks + rail + mast
        g.append(f'<rect x="-300" y="880" width="2520" height="500" fill="#140e0a"/>')
        g.append("".join(f'<rect x="-300" y="{900+k*40}" width="2520" height="3" fill="{INK}" opacity="0.7"/>' for k in range(6)))
        g.append(f'<rect x="-300" y="800" width="2520" height="14" fill="#1a120c" stroke="{INK}" stroke-width="4"/>'
                 + "".join(f'<rect x="{x}" y="812" width="10" height="70" fill="#1a120c" stroke="{INK}" stroke-width="3"/>' for x in range(-280, 2220, 110)))
        g.append(f'<rect x="1520" y="-300" width="44" height="1190" fill="#1a120c" stroke="{INK}" stroke-width="6"/>'
                 f'<rect x="1300" y="120" width="480" height="14" fill="#1a120c" stroke="{INK}" stroke-width="5"/>')
        g.append(f'<path d="M1320,134 Q1470,330 1330,560 L1760,560 Q1640,330 1760,134 Z" fill="#cfc4ae" opacity="0.55" stroke="{INK}" stroke-width="4"/>')
        for k in range(6):
            g.append(f'<path d="M1542,{-200+k*10} L{1100+k*70},800" stroke="{INK}" stroke-width="2" opacity="0.6"/>')
    # fog
    for k in range(5):
        g.append(f'<ellipse cx="{f(rnd.uniform(0,1920))}" cy="{f(rnd.uniform(600,880))}" rx="{f(rnd.uniform(500,900))}" ry="50" fill="{p[5]}" opacity="0.06"/>')
    return "".join(g)


def props(kind, rnd, p):
    c = p[3]
    if kind == "manor":
        x = 1100
        body = (f'<path d="M{x-520},905 L{x-520},520 L{x-430},430 L{x-340},520 L{x-340},560 L{x+300},560 L{x+300},430 L{x+380},330 L{x+460},430 L{x+460},905 Z" fill="{c}"/>'
                f'<rect x="{x-60}" y="440" width="40" height="120" fill="{c}"/>')
        wins = []
        for i, wx in enumerate(range(x - 480, x + 440, 110)):
            for wy in (600, 730):
                lit = rnd.random() < 0.12
                wins.append(f'<rect x="{wx}" y="{wy}" width="44" height="70" fill="{"#ffb24a" if lit else "#000"}" opacity="0.85"/>'
                            + (f'<circle cx="{wx+22}" cy="{wy+35}" r="70" fill="url(#warm)"/>' if lit else ""))
        door = f'<path d="M{x-40},905 L{x-40},800 Q{x},770 {x+40},800 L{x+40},905 Z" fill="#000"/>'
        return body + "".join(wins) + door
    if kind == "graveyard":
        d = []
        for i in range(9):
            x = 160 + i * 190 + rnd.uniform(-40, 40)
            y = 890 + rnd.uniform(-10, 15)
            tilt = rnd.uniform(-12, 12)
            if rnd.random() < 0.5:
                d.append(f'<g transform="rotate({f(tilt)} {f(x)} {f(y)})"><path d="M{f(x-34)},{f(y)} L{f(x-34)},{f(y-90)} Q{f(x)},{f(y-140)} {f(x+34)},{f(y-90)} L{f(x+34)},{f(y)} Z" fill="{c}"/></g>')
            else:
                d.append(f'<g transform="rotate({f(tilt)} {f(x)} {f(y)})"><rect x="{f(x-8)}" y="{f(y-130)}" width="16" height="130" fill="{c}"/>'
                         f'<rect x="{f(x-40)}" y="{f(y-100)}" width="80" height="15" fill="{c}"/></g>')
        # iron fence
        fence = "".join(f'<rect x="{x}" y="820" width="5" height="90" fill="{c}"/><path d="M{x-5},822 L{x+2.5},800 L{x+10},822 Z" fill="{c}"/>' for x in range(0, 1920, 34))
        return fence + f'<rect x="0" y="836" width="1920" height="5" fill="{c}"/>' + "".join(d)
    if kind == "chapel":
        x = 960
        body = (f'<path d="M{x-330},905 L{x-330},560 L{x-180},430 L{x-150},300 L{x-130},250 L{x-110},300 L{x-80},430 L{x+330},500 L{x+330},905 Z" fill="{c}"/>'
                f'<rect x="{x-132}" y="190" width="6" height="70" fill="{c}"/><rect x="{x-150}" y="210" width="42" height="6" fill="{c}"/>')
        win = "".join(f'<path d="M{wx-30},800 L{wx-30},680 Q{wx},630 {wx+30},680 L{wx+30},800 Z" fill="#000" opacity="0.9"/>' for wx in (x - 230, x + 60, x + 210))
        door = f'<path d="M{x-90},905 L{x-90},760 Q{x-40},700 {x+10},760 L{x+10},905 Z" fill="#000"/>'
        # broken roof gap
        gap = f'<path d="M{x+120},530 L{x+200},545 L{x+170},600 L{x+140},570 Z" fill="url(#sky_chapel)"/>'
        return body + win + door + gap
    if kind == "mill":
        x = 1320
        wheel = "".join(f'<rect x="{x-6}" y="560" width="12" height="300" fill="{c}" transform="rotate({a} {x} 710)"/>' for a in range(0, 180, 30))
        return (f'<path d="M{x-420},905 L{x-420},560 L{x-250},420 L{x-80},560 L{x-80},905 Z" fill="{c}"/>'
                f'<rect x="{x-330}" y="640" width="60" height="80" fill="#000" opacity="0.85"/>'
                f'<circle cx="{x}" cy="710" r="150" fill="none" stroke="{c}" stroke-width="18"/>{wheel}')
    if kind == "village":
        d, wins = [], []
        for i in range(6):
            x = 120 + i * 300 + rnd.uniform(-40, 40)
            w, h = rnd.uniform(160, 230), rnd.uniform(140, 220)
            d.append(f'<path d="M{f(x)},905 L{f(x)},{f(905-h)} L{f(x+w/2)},{f(905-h-110)} L{f(x+w)},{f(905-h)} L{f(x+w)},905 Z" fill="{c}"/>')
            if rnd.random() < 0.6:
                wx, wy = x + w * rnd.uniform(0.25, 0.6), 905 - h * rnd.uniform(0.5, 0.75)
                wins.append(f'<rect x="{f(wx)}" y="{f(wy)}" width="34" height="40" fill="#ffb24a" opacity="0.85"/>'
                            f'<circle cx="{f(wx+17)}" cy="{f(wy+20)}" r="70" fill="url(#warm)"/>')
        return "".join(d) + "".join(wins)
    if kind == "swamp":
        return (f'<rect x="-300" y="905" width="2520" height="200" fill="#1a2414" opacity="0.6"/>'
                + "".join(f'<rect x="{f(rnd.uniform(0,1920))}" y="{f(rnd.uniform(930,1050))}" width="{f(rnd.uniform(80,300))}" height="3" fill="{p[5]}" opacity="0.15"/>' for _ in range(18)))
    if kind == "clearing":
        # ring of old standing stones + a dead campfire spot
        d = []
        for i, x in enumerate((300, 520, 1400, 1620)):
            h = rnd.uniform(160, 240)
            d.append(smooth(jag([(x - 40, 905), (x - 46, 905 - h), (x + 10, 905 - h - 20), (x + 44, 905 - h + 10), (x + 40, 905)], 6, rnd, 1)))
        return f'<path d="{" ".join(d)}" fill="{c}"/>'
    if kind == "cave":
        d = [smooth(jag([(-300, -300), (2220, -300), (2220, 380), (1700, 260), (1400, 330), (960, 220), (500, 320), (200, 260), (-300, 400)], 30, rnd, 2))]
        for _ in range(10):
            x = rnd.uniform(100, 1800)
            d.append(poly([(x - 20, 250), (x, 250 + rnd.uniform(60, 180)), (x + 20, 250)]))
        return f'<path d="{" ".join(d)}" fill="{INK}"/>'
    return ""


# ---------------------------------------------------------------- characters
def lantern(x, y, t, lit=1.0):
    """hanging lantern at (x,y) top hook; returns (lit_svg, emissive_svg)"""
    body = (f'<path d="M{f(x)},{f(y)} L{f(x)},{f(y+12)}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{f(x-14)},{f(y+14)} L{f(x+14)},{f(y+14)} L{f(x+11)},{f(y+20)} L{f(x-11)},{f(y+20)} Z" fill="{INK}"/>'
            f'<rect x="{f(x-12)}" y="{f(y+20)}" width="24" height="30" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{f(x)},{f(y+20)} L{f(x)},{f(y+50)}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{f(x-14)}" y="{f(y+49)}" width="28" height="6" fill="{INK}"/>')
    fl = 1 + 0.12 * math.sin(t * 23) + 0.08 * math.sin(t * 37)
    em = ""
    if lit > 0.02:
        em = (f'<circle cx="{f(x)}" cy="{f(y+35)}" r="{f(120*lit*fl)}" fill="url(#ambglow)" opacity="{f(0.55*lit)}"/>'
              f'<ellipse cx="{f(x)}" cy="{f(y+36)}" rx="{f(7*fl)}" ry="{f(12*fl)}" fill="url(#flame)" opacity="{f(min(1,lit*1.2))}"/>')
    return body, em


def odo(x, y, t, s=1.0, face=1, pose="idle", talk=0.0, lit=1.0, scared=0.0, walk=0.0):
    """Odo: small hooded lantern-bearer (original). (x,y)=feet. returns (lit_svg, emissive_svg, lantern_pos)"""
    bob = math.sin(t * 2.2) * 2 + (abs(math.sin(t * 9)) * 6 if walk else 0)
    shk = math.sin(t * 60) * 3 * scared
    X = lambda v: x + (v * face) * s + shk
    Y = lambda v: y + (v - bob) * s
    leg = math.sin(t * 9) * 10 * walk
    g = []
    # legs + boots
    for lx, sw in ((-14, leg), (14, -leg)):
        g.append(f'<path d="M{f(X(lx))},{f(Y(-40))} L{f(X(lx+sw*0.6))},{f(Y(-6))}" stroke="{INK}" stroke-width="{f(9*s)}" stroke-linecap="round"/>'
                 f'<ellipse cx="{f(X(lx+sw*0.6+5))}" cy="{f(Y(-4))}" rx="{f(14*s)}" ry="{f(7*s)}" fill="{INK}"/>')
    # cloak (ragged hem)
    hem = [(-70, -40), (-52, -30), (-38, -44), (-20, -28), (0, -42), (18, -30), (36, -46), (54, -32), (72, -44)]
    cloak = [(-46, -170), (-64, -110)] + hem + [(66, -112), (46, -172)]
    rr = random.Random(int(t * 3))
    g.append(f'<path d="{smooth([(X(a), Y(b + (rr.uniform(-2,2) if b > -50 else 0))) for a, b in cloak])}" fill="#2a1f1a" stroke="{INK}" stroke-width="{f(5*s)}"/>')
    # stitched patch
    g.append(f'<rect x="{f(min(X(-30),X(-8)))}" y="{f(Y(-110))}" width="{f(22*s)}" height="{f(20*s)}" fill="#4a2a1e" stroke="{INK}" stroke-width="{f(2*s)}"/>')
    # scarf
    g.append(f'<path d="{smooth([(X(-44),Y(-176)),(X(46),Y(-178)),(X(44),Y(-160)),(X(-42),Y(-158))])}" fill="#7a1e14" stroke="{INK}" stroke-width="{f(3*s)}"/>'
             f'<path d="{poly([(X(-30),Y(-165)),(X(-56),Y(-120)),(X(-40),Y(-118)),(X(-22),Y(-160))])}" fill="#7a1e14" stroke="{INK}" stroke-width="{f(3*s)}"/>')
    # hood
    hood = [(-58, -175), (-62, -230), (-40, -268), (0, -282), (40, -270), (64, -236), (60, -176)]
    tip = [(30, -272), (-20 - 30, -300 + 10 * math.sin(t * 2)), (-70, -280), (-46, -258)]
    g.append(f'<path d="{smooth([(X(a),Y(b)) for a,b in tip])}" fill="#2a1f1a" stroke="{INK}" stroke-width="{f(5*s)}"/>')
    g.append(f'<path d="{smooth([(X(a),Y(b)) for a,b in hood])}" fill="#2a1f1a" stroke="{INK}" stroke-width="{f(6*s)}"/>')
    # face in hood opening
    fx, fy = X(8), Y(-218)
    g.append(f'<ellipse cx="{f(fx)}" cy="{f(fy)}" rx="{f(40*s)}" ry="{f(40*s)}" fill="{INK}"/>')
    g.append(f'<ellipse cx="{f(fx)}" cy="{f(fy+4*s)}" rx="{f(33*s)}" ry="{f(32*s)}" fill="{BONE}"/>')
    blink = (t % 4.1) < 0.12
    er = (9 + 4 * scared) * s
    for ex in (-13, 14):
        cx = fx + ex * s
        if blink:
            g.append(f'<path d="M{f(cx-er)},{f(fy-2*s)} L{f(cx+er)},{f(fy-2*s)}" stroke="{INK}" stroke-width="{f(3*s)}"/>')
        else:
            g.append(f'<ellipse cx="{f(cx)}" cy="{f(fy-2*s)}" rx="{f(er)}" ry="{f(er*1.15)}" fill="{INK}"/>'
                     f'<circle cx="{f(cx+3*s*face)}" cy="{f(fy-6*s)}" r="{f(3*s)}" fill="#fff"/>')
    # brows when scared
    if scared > 0.3:
        g.append(f'<path d="M{f(fx-22*s)},{f(fy-20*s)} L{f(fx-6*s)},{f(fy-26*s)} M{f(fx+22*s)},{f(fy-20*s)} L{f(fx+6*s)},{f(fy-26*s)}" stroke="{INK}" stroke-width="{f(3*s)}"/>')
    # mouth
    mo = talk * (0.5 + 0.5 * abs(math.sin(t * 17)))
    if scared > 0.5 and talk < 0.1:
        g.append(f'<ellipse cx="{f(fx)}" cy="{f(fy+18*s)}" rx="{f(5*s)}" ry="{f(7*s)}" fill="{INK}"/>')
    elif mo > 0.05:
        g.append(f'<ellipse cx="{f(fx)}" cy="{f(fy+17*s)}" rx="{f(6*s)}" ry="{f((2+7*mo)*s)}" fill="{INK}"/>')
    else:
        g.append(f'<path d="M{f(fx-6*s)},{f(fy+17*s)} Q{f(fx)},{f(fy+19*s)} {f(fx+6*s)},{f(fy+17*s)}" stroke="{INK}" stroke-width="{f(2.5*s)}" fill="none"/>')
    # arm + pole + lantern (held forward)
    sway = math.sin(t * 1.7) * 6 + (math.sin(t * 9) * 4 if walk else 0)
    hx, hy = X(52), Y(-128)
    px, py = X(110), Y(-190)
    g.append(f'<path d="M{f(X(30))},{f(Y(-140))} Q{f(X(44))},{f(Y(-120))} {f(hx)},{f(hy)}" stroke="#2a1f1a" stroke-width="{f(14*s)}" fill="none" stroke-linecap="round"/>'
             f'<circle cx="{f(hx)}" cy="{f(hy)}" r="{f(8*s)}" fill="{BONE}" stroke="{INK}" stroke-width="{f(2*s)}"/>'
             f'<path d="M{f(X(30))},{f(Y(-100))} L{f(px)},{f(py)}" stroke="{INK}" stroke-width="{f(5*s)}"/>')
    lx, ly = px + sway * s * 0.3, py
    lb, le = lantern(lx, ly, t, lit)
    g.append(lb)
    return "".join(g), le, (lx, ly + 35 * s)


def moth(x, y, t, s=1.0, face=1, talk=0.0, glow=1.0):
    """Mothwick: small moth spirit companion (original). returns (lit, emissive)"""
    yy = y + math.sin(t * 3.1) * 10
    flap = 0.35 + 0.65 * abs(math.sin(t * 13))
    g = []
    for side in (-1, 1):
        for up, (wl, wh) in ((1, (58, 50)), (0, (40, 34))):
            wx = x + side * 8 * s
            wy = yy + (-12 if up else 10) * s
            pts = [(0, 0), (side * wl * flap, -wh if up else wh * 0.2), (side * wl * 1.1 * flap, (-wh * 0.2) if up else wh), (side * 10, 6)]
            g.append(f'<path d="{smooth([(wx + a * s, wy + b * s) for a, b in pts])}" fill="#cbb89a" stroke="{INK}" stroke-width="{f(3*s)}" opacity="0.95"/>')
            if up:
                g.append(f'<circle cx="{f(wx + side*wl*0.55*flap*s)}" cy="{f(wy - wh*0.45*s)}" r="{f(8*s*flap)}" fill="#6a3a24" stroke="{INK}" stroke-width="{f(2*s)}"/>')
    rr = random.Random(int(t * 4))
    body = [(x + a * s, yy + b * s) for a, b in [(-16, -18), (16, -18), (18, 6), (8, 34), (-8, 34), (-18, 6)]]
    g.append(f'<path d="{smooth(jag(body, 2.5*s, rr, 2))}" fill="#e2d4b8" stroke="{INK}" stroke-width="{f(3*s)}"/>')
    for ex in (-7, 7):
        g.append(f'<circle cx="{f(x+ex*s)}" cy="{f(yy-6*s)}" r="{f(6*s)}" fill="{INK}"/><circle cx="{f(x+ex*s+2*s*face)}" cy="{f(yy-8*s)}" r="{f(1.8*s)}" fill="#fff"/>')
    if talk > 0.05:
        g.append(f'<ellipse cx="{f(x)}" cy="{f(yy+8*s)}" rx="{f(3*s)}" ry="{f((1+3*abs(math.sin(t*15)))*s)}" fill="{INK}"/>')
    # feathery antennae
    for side in (-1, 1):
        g.append(f'<path d="M{f(x+side*5*s)},{f(yy-18*s)} Q{f(x+side*14*s)},{f(yy-44*s)} {f(x+side*30*s)},{f(yy-50*s)}" stroke="{INK}" stroke-width="{f(2.5*s)}" fill="none"/>')
    em = f'<circle cx="{f(x)}" cy="{f(yy)}" r="{f(70*s)}" fill="url(#paleglow)" opacity="{f(0.35*glow)}"/>'
    return "".join(g), em


# ---------------------------------------------------------------- creatures
def red_eye(x, y, r, t, seed=0, blink=True, color="red"):
    if blink and ((t + seed * 1.37) % 3.7) < 0.13:
        return f'<path d="M{f(x-r)},{f(y)} L{f(x+r)},{f(y)}" stroke="#ff4020" stroke-width="{f(max(1.5,r*0.3))}"/>'
    glow = {"red": "redglow", "amber": "ambglow", "pale": "paleglow", "green": "greenglow"}[color]
    core = {"red": "#ffd0b0", "amber": "#fff0b0", "pale": "#ffffff", "green": "#f0ffd0"}[color]
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*4)}" fill="url(#{glow})" opacity="0.8"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*0.75)}" fill="{EYE_RED if color=="red" else core}"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*0.4)}" fill="{core}"/>')


def gloamhound(x, y, t, s=1.0, face=-1, mouth=0.0, rage=0.0, seed=0):
    """shadow wolf with jagged smoky fur and red eyes. (x,y)= feet centre"""
    rr = random.Random(int(t * 10) + seed)
    br = math.sin(t * 2.5 + seed) * 4
    X = lambda v: x + v * face * s
    Y = lambda v: y + v * s
    body = [(-170, -120 - br), (-120, -175 - br), (-40, -190 - br), (40, -200 - br), (110, -230 - br),
            (150, -250), (205, -235), (240, -205), (232, -185), (190, -180), (150, -150), (120, -110),
            (100, -60), (60, -100), (-20, -105), (-90, -90), (-140, -70), (-175, -95)]
    pts = [(X(a), Y(b)) for a, b in body]
    g = [f'<path d="{smooth(jag(pts, 10*s, rr, 2))}" fill="{INK}"/>']
    # legs
    step = math.sin(t * 4 + seed)
    for lx, ph in ((-130, 0), (-90, 1.5), (60, 0.7), (100, 2.2)):
        k = math.sin(t * 4 + ph) * 8 * (rage > 0.5)
        g.append(f'<path d="{poly(taper(X(lx), Y(-80), X(lx + 14 + k), Y(0), 26*s, 8*s, 12*face*s, rr, 4))}" fill="{INK}"/>'
                 f'<path d="M{f(X(lx+14+k-12))},{f(Y(0))} L{f(X(lx+14+k+18))},{f(Y(2))}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linecap="round"/>')
    # smoky tail
    tw = math.sin(t * 3 + seed) * 25
    g.append(f'<path d="{smooth(jag([(X(-160),Y(-120)),(X(-250),Y(-170+tw)),(X(-310),Y(-150+tw*1.4)),(X(-240),Y(-130)),(X(-170),Y(-95))], 10*s, rr, 2))}" fill="{INK}" opacity="0.92"/>')
    # jaw
    ja = mouth * 26
    hx, hy = X(205), Y(-205)
    g.append(f'<g transform="rotate({f(ja*face)} {f(X(170))} {f(Y(-190))})"><path d="{poly([(X(160),Y(-192)),(X(238),Y(-190)),(X(222),Y(-170)),(X(165),Y(-168))])}" fill="{INK}"/></g>')
    em = []
    if mouth > 0.1:
        teeth = "".join(f'<path d="M{f(X(175+i*13))},{f(Y(-188))} L{f(X(181+i*13))},{f(Y(-188+10*mouth))} L{f(X(187+i*13))},{f(Y(-188))} Z" fill="{BONE}"/>' for i in range(4))
        g.append(teeth)
        em.append(f'<ellipse cx="{f(X(200))}" cy="{f(Y(-182))}" rx="{f(30*s)}" ry="{f(12*s*mouth)}" fill="#ff3a10" opacity="{f(0.35*mouth)}"/>')
    er = (7 + 3 * rage) * s
    em.append(red_eye(X(200), Y(-222), er, t, seed))
    em.append(red_eye(X(222), Y(-218), er * 0.8, t, seed))
    return "".join(g), "".join(em)


def rootwraith(x, y, t, s=1.0, face=-1, reach=0.0, seed=0):
    """walking tree spirit with a hollow face and reaching branch-arms"""
    rr = random.Random(seed + 11)
    sway = math.sin(t * 1.2 + seed) * 8
    X = lambda v: x + v * face * s
    Y = lambda v: y + v * s
    d = [twisted_tree(x + sway * 0.3, y, 520 * s, 110 * s, rr, 4)]
    for side in (-1, 1):
        L = (200 + 160 * reach) * s
        a = math.radians(25 - 20 * reach + 6 * math.sin(t * 2 + side))
        sx, sy = x + side * 20 * s + sway, y - 330 * s
        ex, ey = sx + side * math.cos(a) * L, sy - math.sin(a) * L * 0.5 + 60 * s
        d.append(smooth(taper(sx, sy, ex, ey, 30 * s, 3, side * 30 * s, rr, 6)))
        for k in range(4):   # fingers
            ang = a + (k - 1.5) * 0.35
            fl = 70 * s
            d.append(poly(taper(ex, ey, ex + side * math.cos(ang) * fl, ey + math.sin(ang) * fl * 0.6, 7 * s, 1, rr.uniform(-6, 6), rr, 3)))
    g = f'<path d="{" ".join(d)}" fill="#120a07" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    fx, fy = x + sway * 0.3, y - 400 * s
    g += (f'<ellipse cx="{f(fx-24*s)}" cy="{f(fy)}" rx="{f(20*s)}" ry="{f(28*s)}" fill="#000"/>'
          f'<ellipse cx="{f(fx+26*s)}" cy="{f(fy+4*s)}" rx="{f(18*s)}" ry="{f(24*s)}" fill="#000"/>'
          f'<path d="M{f(fx-30*s)},{f(fy+60*s)} Q{f(fx)},{f(fy+40*s)} {f(fx+34*s)},{f(fy+64*s)} Q{f(fx)},{f(fy+95*s)} {f(fx-30*s)},{f(fy+60*s)} Z" fill="#000"/>')
    em = red_eye(fx - 24 * s, fy + 4 * s, 7 * s, t, seed, color="amber") + red_eye(fx + 26 * s, fy + 8 * s, 6 * s, t, seed + 1, color="amber")
    return g, em


def crow(x, y, t, s=1.0, face=-1, fly=0.0, seed=0):
    X = lambda v: x + v * face * s
    Y = lambda v: y + v * s
    flap = math.sin(t * 14 + seed) if fly else 0.2 * math.sin(t * 2 + seed)
    body = [(-40, -20), (-10, -38), (24, -40), (40, -50), (56, -44), (48, -34), (30, -20), (-6, -6), (-46, -2), (-70, 0), (-56, -12)]
    g = f'<path d="{smooth([(X(a),Y(b)) for a,b in body])}" fill="{INK}"/>'
    wy = -40 - 50 * flap
    g += f'<path d="{smooth([(X(-10),Y(-30)),(X(-40),Y(wy)),(X(-80),Y(wy+10)),(X(-30),Y(-16))])}" fill="{INK}"/>'
    g += f'<path d="M{f(X(56))},{f(Y(-44))} L{f(X(74))},{f(Y(-40))} L{f(X(54))},{f(Y(-36))} Z" fill="{INK}"/>'
    if not fly:
        g += f'<path d="M{f(X(0))},{f(Y(-6))} L{f(X(-4))},{f(Y(8))} M{f(X(12))},{f(Y(-8))} L{f(X(10))},{f(Y(8))}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    return g, red_eye(X(44), Y(-44), 3.2 * s, t, seed)


def hollowmother(x, y, t, s=1.0, drop=1.0, seed=0):
    """huge hanging spider-thing; (x,y)=body centre at full drop"""
    yy = y - (1 - drop) * 700 + math.sin(t * 1.5) * 10
    rr = random.Random(seed)
    g = [f'<path d="M{f(x)},-200 L{f(x)},{f(yy-80*s)}" stroke="#2a2420" stroke-width="3"/>']
    legs = []
    for side in (-1, 1):
        for k in range(4):
            a0 = math.radians(-60 + k * 40)
            wig = math.sin(t * 3 + k + side) * 0.12
            kx = x + side * math.cos(a0 + wig) * 150 * s
            ky = yy + math.sin(a0 + wig) * 110 * s - 60 * s
            ex = kx + side * 70 * s
            ey = ky + 160 * s
            legs.append(poly(taper(x + side * 30 * s, yy, kx, ky, 22 * s, 12 * s, 0, rr, 3)))
            legs.append(poly(taper(kx, ky, ex, ey, 12 * s, 2, side * 10, rr, 3)))
    g.append(f'<path d="{" ".join(legs)}" fill="{INK}"/>')
    g.append(f'<path d="{smooth(jag([(x-90*s,yy-30*s),(x,yy-110*s),(x+90*s,yy-30*s),(x+70*s,yy+60*s),(x,yy+90*s),(x-70*s,yy+60*s)], 8*s, rr, 2))}" fill="{INK}"/>')
    em = "".join(red_eye(x + dx * s, yy + dy * s, r * s, t, seed + i, color="pale") for i, (dx, dy, r) in
                 enumerate([(-30, -20, 9), (30, -20, 9), (-12, -46, 6), (12, -46, 6), (-50, 0, 5), (50, 0, 5)]))
    return "".join(g), em


def wickeater(x, y, t, s=1.0, face=1, grin=0.6, seed=0):
    """small imp that eats light: round black body, huge grin"""
    hop = abs(math.sin(t * 5 + seed)) * 18
    yy = y - hop * s
    rr = random.Random(int(t * 8) + seed)
    g = f'<path d="{smooth(jag([(x-46*s,yy-20*s),(x-30*s,yy-80*s),(x,yy-96*s),(x+32*s,yy-80*s),(x+46*s,yy-20*s),(x,yy)], 6*s, rr, 2))}" fill="{INK}"/>'
    for side in (-1, 1):
        g += f'<path d="M{f(x+side*24*s)},{f(yy-84*s)} L{f(x+side*40*s)},{f(yy-126*s)} L{f(x+side*12*s)},{f(yy-92*s)} Z" fill="{INK}"/>'
        g += f'<path d="M{f(x+side*18*s)},{f(yy-4*s)} L{f(x+side*22*s)},{f(y+2*s)}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
    w = (26 + 14 * grin) * s
    mouth = (f'<path d="M{f(x-w)},{f(yy-40*s)} Q{f(x)},{f(yy-(14-20*grin)*s)} {f(x+w)},{f(yy-40*s)} Q{f(x)},{f(yy-30*s)} {f(x-w)},{f(yy-40*s)} Z" fill="{BONE}"/>'
             + "".join(f'<path d="M{f(x-w+i*w/3)},{f(yy-38*s)} L{f(x-w+i*w/3)},{f(yy-28*s+grin*6*s)}" stroke="{INK}" stroke-width="{f(2*s)}"/>' for i in range(1, 6)))
    em = red_eye(x - 15 * s, yy - 62 * s, 6 * s, t, seed, color="amber") + red_eye(x + 15 * s, yy - 62 * s, 6 * s, t, seed + 2, color="amber")
    return g + mouth, em


def shepherd(x, y, t, s=1.0, face=-1, raise_=0.0, seed=0):
    """The Pale Shepherd: very tall, ragged robe, blank cracked porcelain mask, crook staff"""
    rr = random.Random(int(t * 3) + seed)
    sway = math.sin(t * 0.9) * 6
    X = lambda v: x + v * face * s + sway * (1 + v / 600)
    Y = lambda v: y + v * s
    robe = [(-40, -560), (40, -560), (70, -380), (95, -160), (120, 0), (80, -18), (60, 4), (20, -14), (-10, 6), (-40, -12), (-70, 4), (-110, 0), (-90, -170), (-70, -380)]
    g = [f'<path d="{smooth(jag([(X(a),Y(b)) for a,b in robe], 7*s, rr, 1))}" fill="#16110f" stroke="{INK}" stroke-width="{f(5*s)}"/>']
    # hood
    g.append(f'<path d="{smooth([(X(-58),Y(-540)),(X(-50),Y(-650)),(X(0),Y(-700)),(X(50),Y(-650)),(X(60),Y(-540))])}" fill="#16110f" stroke="{INK}" stroke-width="{f(5*s)}"/>')
    # mask
    mx, my = X(4), Y(-610)
    g.append(f'<ellipse cx="{f(mx)}" cy="{f(my)}" rx="{f(34*s)}" ry="{f(46*s)}" fill="#ece6da" stroke="{INK}" stroke-width="{f(3*s)}"/>'
             f'<path d="M{f(mx-20*s)},{f(my-8*s)} L{f(mx-6*s)},{f(my-6*s)} M{f(mx+6*s)},{f(my-6*s)} L{f(mx+20*s)},{f(my-8*s)}" stroke="#000" stroke-width="{f(5*s)}" stroke-linecap="round"/>'
             f'<path d="M{f(mx+10*s)},{f(my-46*s)} L{f(mx+4*s)},{f(my-24*s)} L{f(mx+14*s)},{f(my-10*s)}" stroke="#5a5048" stroke-width="{f(2*s)}" fill="none"/>')
    # arm + long fingers + crook
    ay = -420 - 120 * raise_
    g.append(f'<path d="M{f(X(30))},{f(Y(-480))} Q{f(X(90))},{f(Y(-440))} {f(X(110))},{f(Y(ay))}" stroke="#16110f" stroke-width="{f(22*s)}" fill="none" stroke-linecap="round"/>')
    for k in range(4):
        g.append(f'<path d="M{f(X(110))},{f(Y(ay))} L{f(X(118+k*7))},{f(Y(ay+30+k*4))}" stroke="#d8d0c0" stroke-width="{f(3*s)}"/>')
    g.append(f'<path d="M{f(X(115))},{f(Y(0))} L{f(X(115))},{f(Y(-760))} Q{f(X(115))},{f(Y(-830))} {f(X(170))},{f(Y(-820))} Q{f(X(215))},{f(Y(-805))} {f(X(195))},{f(Y(-760))}" stroke="#2a1e16" stroke-width="{f(9*s)}" fill="none"/>')
    em = f'<ellipse cx="{f(mx)}" cy="{f(my)}" rx="{f(60*s)}" ry="{f(70*s)}" fill="url(#paleglow)" opacity="0.25"/>'
    return "".join(g), em


def figure(x, y, t, s=1.0, face=-1, ghost=0.0, seed=0):
    """generic historical person silhouette (coat + hat), optionally a pale ghost"""
    rr = random.Random(seed)
    hat = seed % 3
    sway = math.sin(t * 1.3 + seed) * 2
    X = lambda v: x + v * face * s + sway
    Y = lambda v: y + v * s
    green = seed >= 10   # seed 10-12: green-skinned child (Woolpit), same hat styles
    col = "#cfd8e0" if ghost else ("#1d3418" if green else "#17110e")
    op = 0.55 if ghost else 1.0
    coat = [(-34, -230), (34, -232), (46, -120), (56, 0), (16, 0), (8, -60), (-8, -60), (-16, 0), (-56, 0), (-46, -120)]
    g = [f'<path d="{smooth([(X(a),Y(b)) for a,b in coat])}" fill="{col}" stroke="{INK}" stroke-width="{f(4*s)}" opacity="{op}"/>']
    g.append(f'<circle cx="{f(X(0))}" cy="{f(Y(-262))}" r="{f(30*s)}" fill="{("#8fc46a" if green else BONE) if not ghost else "#e8f0f8"}" stroke="{INK}" stroke-width="{f(4*s)}" opacity="{op}"/>')
    g.append(f'<circle cx="{f(X(8))}" cy="{f(Y(-266))}" r="{f(4*s)}" fill="{INK}"/><circle cx="{f(X(-10))}" cy="{f(Y(-266))}" r="{f(4*s)}" fill="{INK}"/>')
    if hat == 0:   # tricorn / wide hat
        g.append(f'<path d="M{f(X(-52))},{f(Y(-282))} Q{f(X(0))},{f(Y(-300))} {f(X(52))},{f(Y(-282))} L{f(X(28))},{f(Y(-322))} L{f(X(-28))},{f(Y(-322))} Z" fill="{INK}" opacity="{op}"/>')
    elif hat == 1:  # sailor cap
        g.append(f'<path d="M{f(X(-34))},{f(Y(-280))} L{f(X(-30))},{f(Y(-306))} L{f(X(32))},{f(Y(-306))} L{f(X(44))},{f(Y(-282))} Z" fill="{INK}" opacity="{op}"/>')
    else:          # hood / shawl
        g.append(f'<path d="M{f(X(-40))},{f(Y(-240))} Q{f(X(-44))},{f(Y(-310))} {f(X(0))},{f(Y(-306))} Q{f(X(44))},{f(Y(-310))} {f(X(40))},{f(Y(-240))} L{f(X(30))},{f(Y(-262))} Q{f(X(0))},{f(Y(-298))} {f(X(-30))},{f(Y(-262))} Z" fill="{col}" stroke="{INK}" stroke-width="{f(3*s)}" opacity="{op}"/>')
    em = f'<ellipse cx="{f(X(0))}" cy="{f(Y(-150))}" rx="{f(80*s)}" ry="{f(170*s)}" fill="url(#paleglow)" opacity="{0.35 if ghost else 0}"/>'
    return "".join(g), em


def ghostship(x, y, t, s=1.0, face=-1, extra=0.0, seed=0):
    """a ship far out on the water, tattered sails, faint light"""
    bob = math.sin(t * 0.8 + seed) * 6
    X = lambda v: x + v * face * s
    Y = lambda v: y + v * s + bob
    hull = [(-260, -20), (260, -20), (220, 40), (-210, 40)]
    g = [f'<path d="{poly([(X(a),Y(b)) for a,b in hull])}" fill="#0c0a08" stroke="{INK}" stroke-width="{f(4*s)}"/>']
    for mx, h in ((-110, 300), (40, 380), (170, 260)):
        g.append(f'<rect x="{f(X(mx)-4*s)}" y="{f(Y(-20-h))}" width="{f(8*s)}" height="{f(h*s)}" fill="#0c0a08"/>')
        rr = random.Random(seed + mx)
        sail = [(mx - 70, -20 - h * 0.9), (mx + 70, -20 - h * 0.9), (mx + 60, -50), (mx - 60, -50)]
        g.append(f'<path d="{smooth(jag([(X(a),Y(b)) for a,b in sail], 8*s, rr, 2))}" fill="#c8c0ac" opacity="0.45" stroke="{INK}" stroke-width="{f(2*s)}"/>')
    em = f'<circle cx="{f(X(200))}" cy="{f(Y(-40))}" r="{f(40*s)}" fill="url(#ambglow)" opacity="0.6"/>'
    return "".join(g), em


CREATURES = {"gloamhound": gloamhound, "rootwraith": rootwraith, "crow": crow, "hollowmother": hollowmother,
             "wickeater": wickeater, "shepherd": shepherd, "figure": figure, "ghost": figure, "ship": ghostship}
CREATURE_VOICE = {"rootwraith": "rootwraith", "hollowmother": "hollowmother", "wickeater": "wickeater",
                  "shepherd": "shepherd", "gloamhound": "hound", "crow": "crow", "figure": "stranger", "ghost": "grandma", "ship": "narr"}

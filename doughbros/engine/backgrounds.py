"""Backgrounds for a 1920x1080 world. Floor line is at y=790; heroes stand at y=680, villains at y=560."""
import random

W, H = 1920, 1080
FLOOR = 790

BACKGROUNDS = {
    "kitchen": "Dark kitchen at night: moonlit window, hanging knives, shelf of jars, red tablecloth.",
    "freezer": "Inside the freezer: icy blue walls, frozen boxes, frost, cold mist.",
    "pantry":  "Pantry: tall wooden shelves with jars and sacks, a single swinging bulb.",
    "oven":    "Inside a huge oven: glowing orange heating coils, metal racks, heat haze.",
    "table":   "Dinner table at dusk: giant plates, cups and cutlery, candle light.",
    "bathroom": "Dark bathroom: dripping tap, tiles, bathtub edge, foggy mirror, green night light.",
    "garden":  "Night garden outside the kitchen door: full moon, fence, pumpkins, tall grass, fireflies.",
    "attic":   "Dusty attic: wooden beams, cobwebs, boxes, an old rocking chair, round window with lightning.",
    "fridge":  "Inside the fridge: bright cold shelves, milk cartons, jars, eggs, humming light.",
    "lunchbox": "Inside a giant school lunchbox: plastic walls, apple, sandwich, juice box, crayons.",
}


def bg_defs():
    return ('<linearGradient id="bg_shaft" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0%" stop-color="#9fb8ff" stop-opacity="0.22"/>'
            '<stop offset="100%" stop-color="#9fb8ff" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="bg_bulb" r="50%"><stop offset="0%" stop-color="#ffd27a" stop-opacity="0.45"/>'
            '<stop offset="100%" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="vign" cx="50%" cy="50%" r="72%"><stop offset="55%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity="0.9"/></radialGradient>'
            '<radialGradient id="redglow" r="50%"><stop offset="0%" stop-color="#ff4a10" stop-opacity="0.5"/>'
            '<stop offset="100%" stop-color="#ff2a00" stop-opacity="0"/></radialGradient>')


def _grad(id_, a, b):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{a}"/><stop offset="100%" stop-color="{b}"/></linearGradient>'


def _tiles(color, op, size=90, top=0, bottom=FLOOR):
    s = []
    for y in range(top, bottom - 30, size):
        for x in range((y // size % 2) * size // 2, W, size):
            s.append(f'<rect x="{x+3}" y="{y+3}" width="{size-6}" height="{size-6}" fill="{color}" opacity="{op}"/>')
    return "".join(s)


def _floor(a, b, stripe="#000", edge="#5a1414"):
    s = [f'<defs>{_grad("fl", a, b)}</defs><rect x="0" y="{FLOOR}" width="{W}" height="{H-FLOOR}" fill="url(#fl)"/>']
    for x in range(-400, W + 400, 120):
        s.append(f'<path d="M{x},{FLOOR} L{x+60},{FLOOR} L{x+60+(x-W/2)*0.5},{H} L{x+(x-W/2)*0.5},{H} Z" fill="{stripe}" opacity="0.18"/>')
    s.append(f'<rect x="0" y="{FLOOR-8}" width="{W}" height="14" fill="{edge}"/>')
    return "".join(s)


def kitchen():
    s = [f'<defs>{_grad("wall", "#140b09", "#2a1712")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>',
         _tiles("#000", 0.13),
         '<rect x="170" y="110" width="300" height="260" rx="8" fill="#0d1630" stroke="#050202" stroke-width="16"/>'
         '<circle cx="380" cy="190" r="48" fill="#e8edff" opacity="0.9"/><circle cx="398" cy="178" r="44" fill="#0d1630"/>'
         '<line x1="320" y1="110" x2="320" y2="370" stroke="#050202" stroke-width="12"/>'
         '<line x1="170" y1="240" x2="470" y2="240" stroke="#050202" stroke-width="12"/>'
         '<path d="M170,370 L470,370 L900,800 L300,800 Z" fill="url(#bg_shaft)"/>',
         '<rect x="980" y="200" width="760" height="18" fill="#0a0504"/>']
    for jx, jh in [(1010, 70), (1090, 110), (1190, 60), (1600, 90), (1680, 70)]:
        s.append(f'<rect x="{jx}" y="{200-jh}" width="60" height="{jh}" rx="10" fill="#0a0504"/>')
    for i, kx in enumerate((600, 650, 700)):
        s.append(f'<line x1="{kx}" y1="60" x2="{kx}" y2="110" stroke="#0a0504" stroke-width="4"/>'
                 f'<path d="M{kx-8},110 L{kx+8},110 L{kx+4},{230+i*15} L{kx},{250+i*15} Z" fill="#3a3a40" opacity="0.6"/>')
    s.append(_floor("#3a0d0d", "#120303"))
    return "".join(s)


def freezer():
    r = random.Random(5)
    s = [f'<defs>{_grad("wall", "#0b1c2c", "#1d3a52")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>',
         _tiles("#8fc3ea", 0.06, 120)]
    for i in range(7):  # frozen boxes on shelves
        x = 80 + i * 260
        s.append(f'<rect x="{x}" y="{300 + (i%2)*60}" width="{200}" height="{140}" rx="6" fill="#294e6b" stroke="#0b1c2c" stroke-width="6"/>'
                 f'<rect x="{x+20}" y="{330 + (i%2)*60}" width="120" height="20" fill="#8fc3ea" opacity="0.4"/>')
    s.append('<rect x="0" y="450" width="1920" height="16" fill="#0b1c2c"/><rect x="0" y="240" width="1920" height="16" fill="#0b1c2c"/>')
    for _ in range(26):  # icicles from top
        x = r.uniform(0, W); L = r.uniform(30, 110)
        s.append(f'<path d="M{x-10},0 L{x+10},0 L{x},{L} Z" fill="#e9f7ff" opacity="0.8"/>')
    s.append(_floor("#a9d4f0", "#3d6a8a", stripe="#ffffff", edge="#e9f7ff"))
    for _ in range(14):
        s.append(f'<ellipse cx="{r.uniform(0,W)}" cy="{r.uniform(760,1000)}" rx="{r.uniform(80,220)}" ry="30" fill="#ffffff" opacity="0.12"/>')
    return "".join(s)


def pantry():
    s = [f'<defs>{_grad("wall", "#1a120a", "#2b1d10")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    for x in range(0, W, 140):
        s.append(f'<rect x="{x}" y="0" width="134" height="{FLOOR}" fill="#000" opacity="0.12"/>')
    r = random.Random(9)
    for sy in (180, 380, 580):
        s.append(f'<rect x="0" y="{sy}" width="{W}" height="20" fill="#3a2410" stroke="#120a04" stroke-width="4"/>')
        x = 30
        while x < W - 100:
            w = r.uniform(50, 110); h = r.uniform(60, 150)
            if r.random() < 0.5:
                s.append(f'<rect x="{x}" y="{sy-h}" width="{w}" height="{h}" rx="12" fill="#{r.choice(["2c3a1c","3a1c1c","1c2c3a","3a301c"])}" stroke="#0c0804" stroke-width="4"/>'
                         f'<rect x="{x+6}" y="{sy-h-12}" width="{w-12}" height="16" fill="#120a04"/>')
            else:
                s.append(f'<path d="M{x},{sy} Q{x-6},{sy-h} {x+w/2},{sy-h-10} Q{x+w+6},{sy-h} {x+w},{sy} Z" fill="#6a5434" stroke="#0c0804" stroke-width="4"/>')
            x += w + r.uniform(10, 40)
    s.append('<line x1="960" y1="0" x2="960" y2="150" stroke="#000" stroke-width="4"/>'
             '<circle cx="960" cy="165" r="22" fill="#ffd27a"/><circle cx="960" cy="200" r="520" fill="url(#bg_bulb)"/>')
    s.append(_floor("#2a1a0c", "#0a0603", edge="#3a2410"))
    return "".join(s)


def oven():
    s = [f'<defs>{_grad("wall", "#2a0c04", "#120402")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    for y in (120, 230):  # glowing coils
        d = f"M60,{y} " + " ".join(f"Q{100+i*120},{y-40 if i%2 else y+40} {160+i*120},{y}" for i in range(15))
        s.append(f'<path d="{d}" fill="none" stroke="#ff6a1a" stroke-width="22" opacity="0.5" filter="url(#glow)"/>'
                 f'<path d="{d}" fill="none" stroke="#ffb35a" stroke-width="10"/>')
    for y in (420, 600):  # racks
        s.append(f'<rect x="0" y="{y}" width="{W}" height="10" fill="#555"/>' + "".join(
            f'<rect x="{x}" y="{y-60}" width="6" height="70" fill="#444"/>' for x in range(40, W, 80)))
    s.append(_floor("#3a1a0c", "#0a0402", edge="#6a6a6a"))
    s.append(f'<rect width="{W}" height="{H}" fill="#ff5a10" opacity="0.08"/>')
    return "".join(s)


def table():
    s = [f'<defs>{_grad("wall", "#24121c", "#3a1d1a")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>',
         '<rect x="1300" y="80" width="420" height="300" rx="10" fill="#4a2a3a" stroke="#120808" stroke-width="14"/>'
         '<rect x="1320" y="100" width="380" height="260" fill="#ff8a5a" opacity="0.25"/>']
    # giant plate & cup silhouettes
    s.append('<ellipse cx="1500" cy="760" rx="330" ry="60" fill="#d8d0c8" stroke="#120808" stroke-width="6"/>'
             '<ellipse cx="1500" cy="755" rx="240" ry="38" fill="#c2b8ae"/>'
             '<path d="M180,780 L220,480 L470,480 L510,780 Z" fill="#5a2a2a" stroke="#120808" stroke-width="8"/>'
             '<path d="M510,560 q90,0 80,90 q-10,70 -80,70" fill="none" stroke="#120808" stroke-width="22"/>'
             '<rect x="900" y="420" width="40" height="360" fill="#e8dcc8" stroke="#120808" stroke-width="5"/>'
             '<path d="M920,420 q-16,-40 0,-70 q16,30 0,70" fill="#ffcf5a"/><circle cx="920" cy="390" r="200" fill="url(#bg_bulb)"/>')
    s.append(_floor("#e8dcc8", "#6a5a4a", stripe="#8a1a1a", edge="#b03030"))
    return "".join(s)


def bathroom():
    s = [f'<defs>{_grad("wall", "#0d1f1c", "#1d3330")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>', _tiles("#9fe0d0", 0.06, 70)]
    s.append('<rect x="1250" y="120" width="420" height="330" rx="20" fill="#2a4a46" stroke="#081210" stroke-width="12"/>'
             '<rect x="1270" y="140" width="380" height="290" rx="12" fill="#b8d8d0" opacity="0.18"/>'
             '<path d="M1300,180 q60,40 0,80 M1420,170 q40,60 -20,110" stroke="#fff" stroke-width="6" opacity="0.15" fill="none"/>')
    s.append('<path d="M120,560 L880,560 Q900,560 900,600 L880,790 L140,790 L120,600 Q100,560 120,560 Z" fill="#dfe9e6" stroke="#081210" stroke-width="10"/>'
             '<rect x="110" y="545" width="800" height="30" rx="14" fill="#f2f7f6" stroke="#081210" stroke-width="8"/>'
             '<path d="M760,545 L760,470 Q760,440 800,440 L840,440" fill="none" stroke="#8a9a98" stroke-width="18"/>'
             '<path d="M840,440 l0,24" stroke="#8a9a98" stroke-width="14"/><ellipse cx="840" cy="488" rx="6" ry="10" fill="#9fe0ff"/>')
    s.append('<circle cx="1750" cy="600" r="16" fill="#7aff9a"/><circle cx="1750" cy="600" r="260" fill="url(#bg_bulb)" opacity="0.6"/>')
    s.append(_floor("#cfe0dc", "#3a4a48", stripe="#000", edge="#e8f2f0"))
    s.append(f'<rect width="{W}" height="{H}" fill="#0a3a2a" opacity="0.18"/>')
    return "".join(s)


def garden():
    r = random.Random(11)
    s = [f'<defs>{_grad("wall", "#050a1a", "#16203a")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    for _ in range(60):
        s.append(f'<circle cx="{r.uniform(0,W)}" cy="{r.uniform(0,420)}" r="{r.uniform(1,2.6)}" fill="#fff" opacity="{r.uniform(0.3,0.9)}"/>')
    s.append('<circle cx="1500" cy="200" r="110" fill="#f4f0d8"/><circle cx="1500" cy="200" r="260" fill="#f4f0d8" opacity="0.08"/>'
             '<circle cx="1470" cy="180" r="18" fill="#d8d2b0"/><circle cx="1530" cy="235" r="12" fill="#d8d2b0"/>')
    s.append('<path d="M0,620 Q300,540 600,600 T1200,580 T1920,600 L1920,800 L0,800 Z" fill="#0d1a12"/>')
    for x in range(-20, W, 70):  # fence
        s.append(f'<path d="M{x},780 L{x},{560+(x%3)*8} L{x+25},{535+(x%3)*8} L{x+50},{560+(x%3)*8} L{x+50},780 Z" fill="#2a2420" stroke="#0a0806" stroke-width="5"/>')
    s.append('<rect x="0" y="620" width="1920" height="16" fill="#1e1a16"/><rect x="0" y="720" width="1920" height="16" fill="#1e1a16"/>')
    for px, ps in ((300, 1.0), (1650, 1.3), (1100, 0.8)):
        s.append(f'<g transform="translate({px},770) scale({ps})"><ellipse rx="70" ry="52" fill="#e8822a" stroke="#0a0806" stroke-width="5"/>'
                 '<path d="M-30,-48 Q0,-60 30,-48 M-55,-20 Q-62,10 -50,40 M55,-20 Q62,10 50,40" stroke="#b85a14" stroke-width="4" fill="none"/>'
                 '<path d="M0,-50 q5,-25 20,-30" stroke="#3a6a1a" stroke-width="9" fill="none"/></g>')
    s.append(_floor("#1a2a16", "#060a05", stripe="#000", edge="#2a3a1e"))
    for _ in range(14):
        s.append(f'<circle cx="{r.uniform(0,W)}" cy="{r.uniform(300,760)}" r="5" fill="#d8ff6a" opacity="0.8"/>'
                 f'<circle cx="{r.uniform(0,W)}" cy="{r.uniform(300,760)}" r="16" fill="#d8ff6a" opacity="0.12"/>')
    return "".join(s)


def attic():
    r = random.Random(13)
    s = [f'<defs>{_grad("wall", "#1a120c", "#2e2016")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    s.append('<path d="M0,0 L960,-200 L1920,0 L1920,120 L960,-60 L0,120 Z" fill="#0e0a06"/>')
    for x in range(120, W, 300):
        s.append(f'<rect x="{x}" y="0" width="40" height="{FLOOR}" fill="#3a2614" stroke="#120a04" stroke-width="5"/>')
    s.append('<circle cx="960" cy="230" r="120" fill="#141c34" stroke="#120a04" stroke-width="18"/>'
             '<line x1="840" y1="230" x2="1080" y2="230" stroke="#120a04" stroke-width="10"/><line x1="960" y1="110" x2="960" y2="350" stroke="#120a04" stroke-width="10"/>'
             '<path d="M990,140 l-30,50 l25,0 l-35,60" stroke="#e8f0ff" stroke-width="5" fill="none" opacity="0.8"/>')
    for (cx, cy) in ((0, 0), (1920, 0), (500, 120)):
        s.append(f'<g stroke="#d8d0c0" stroke-width="2" opacity="0.35" fill="none">' + "".join(f'<path d="M{cx},{cy} L{cx+(200 if cx<960 else -200)*__import__("math").cos(a/5)},{cy+200*__import__("math").sin(a/5)}"/>' for a in range(0, 8)) +
                 "".join(f'<path d="M{cx+(60*k if cx<960 else -60*k)},{cy} Q{cx+(40*k if cx<960 else -40*k)},{cy+40*k} {cx},{cy+60*k}"/>' for k in range(1, 4)) + '</g>')
    for i, (bx, bw, bh) in enumerate([(200, 220, 150), (380, 160, 110), (1500, 260, 180), (1720, 160, 240)]):
        s.append(f'<rect x="{bx}" y="{FLOOR-bh}" width="{bw}" height="{bh}" fill="#7a5a34" stroke="#1a1006" stroke-width="6"/>'
                 f'<path d="M{bx},{FLOOR-bh+30} h{bw}" stroke="#5a3e20" stroke-width="5"/>')
    s.append('<g transform="translate(1250,640)" fill="none" stroke="#2a1a0c" stroke-width="12"><path d="M-80,140 Q0,175 80,140"/><path d="M-60,140 L-60,-20 L60,-20 L60,140 M-60,40 L60,40 M-60,-20 L-70,-150 L70,-150 L60,-20"/></g>')
    s.append(_floor("#4a3218", "#120a04", edge="#5a3e20"))
    return "".join(s)


def fridge():
    s = [f'<defs>{_grad("wall", "#cfe6ee", "#8fb4c4")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    s.append('<rect x="0" y="0" width="1920" height="40" fill="#fffef0" opacity="0.9"/><rect x="0" y="40" width="1920" height="200" fill="#fffef0" opacity="0.25"/>')
    for y in (300, 560):
        s.append(f'<rect x="0" y="{y}" width="1920" height="18" fill="#e8f4f8" stroke="#6a8a98" stroke-width="4" opacity="0.9"/>')
    items = [(120, 300, 110, 200, "#f4f4f4", "#3a7ad0"), (280, 300, 90, 140, "#ffd060", "#c08010"), (1500, 300, 120, 220, "#f4f4f4", "#d03a3a"),
             (1680, 300, 100, 120, "#b0e070", "#508020"), (700, 560, 140, 90, "#ffe0b0", "#c08040"), (1250, 560, 110, 160, "#ff9aa0", "#b03040")]
    for x, base, w, h, c1, c2 in items:
        s.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="12" fill="{c1}" stroke="#3a5a68" stroke-width="5"/>'
                 f'<rect x="{x}" y="{base-h*0.6}" width="{w}" height="{h*0.25}" fill="{c2}" opacity="0.8"/>')
    for i in range(6):
        s.append(f'<ellipse cx="{860+i*60}" cy="{530}" rx="26" ry="32" fill="#fff8ec" stroke="#8a7a68" stroke-width="3"/>')
    s.append(_floor("#e8f4f8", "#9ab8c6", stripe="#ffffff", edge="#ffffff"))
    s.append(f'<rect width="{W}" height="{H}" fill="#9fd8ff" opacity="0.12"/>')
    return "".join(s)


def lunchbox():
    s = [f'<defs>{_grad("wall", "#2a6ad0", "#173e80")}</defs><rect width="{W}" height="{H}" fill="url(#wall)"/>']
    s.append('<rect x="40" y="40" width="1840" height="740" rx="60" fill="none" stroke="#0e2a5a" stroke-width="20"/>')
    s.append('<g transform="translate(1790,660) scale(0.75)"><circle r="150" fill="#d8282a" stroke="#4a0808" stroke-width="8"/>'
             '<path d="M0,-150 q10,-60 50,-80" stroke="#4a2a10" stroke-width="16" fill="none"/><path d="M20,-200 q60,-40 110,0 q-50,30 -110,0" fill="#4aa02a"/>'
             '<path d="M-80,-80 q-30,60 0,120" stroke="#fff" stroke-width="14" opacity="0.4" fill="none"/></g>')
    s.append('<path d="M180,780 L260,520 L760,520 L840,780 Z" fill="#f2d49a" stroke="#6a4a1a" stroke-width="8"/>'
             '<path d="M220,690 L800,690" stroke="#5aa02a" stroke-width="22"/><path d="M230,650 L790,650" stroke="#d84a3a" stroke-width="16"/>')
    s.append('<rect x="960" y="430" width="220" height="350" rx="16" fill="#ff9a2a" stroke="#6a3a08" stroke-width="8"/>'
             '<rect x="1130" y="360" width="16" height="90" fill="#fff" stroke="#6a3a08" stroke-width="3" transform="rotate(12 1138 405)"/>')
    for i, c in enumerate(("#e83a3a", "#3a9ae8", "#e8d83a", "#3ae86a")):
        s.append(f'<rect x="{300+i*80}" y="140" width="40" height="300" rx="8" fill="{c}" stroke="#0e2a5a" stroke-width="5" transform="rotate({-10+i*7} {320+i*80} 290)"/>')
    s.append(_floor("#4a8ae8", "#1a3a7a", stripe="#ffffff", edge="#0e2a5a"))
    return "".join(s)


DRAW = {"kitchen": kitchen, "freezer": freezer, "pantry": pantry, "oven": oven, "table": table,
        "bathroom": bathroom, "garden": garden, "attic": attic, "fridge": fridge, "lunchbox": lunchbox}
_cache = {}


def background(name):
    if name not in _cache:
        _cache[name] = DRAW[name]()
    return _cache[name]

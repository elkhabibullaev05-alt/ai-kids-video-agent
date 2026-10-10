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


DRAW = {"kitchen": kitchen, "freezer": freezer, "pantry": pantry, "oven": oven, "table": table}
_cache = {}


def background(name):
    if name not in _cache:
        _cache[name] = DRAW[name]()
    return _cache[name]

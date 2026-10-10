"""Dough Bros (creepy edition) character library.
Each function returns an SVG <g> centred at (0,0), body roughly within +-100.
"""
import math

PAL = {
    "bup":    ("#E8B04A", "#7A4A12"),   # stale bread loaf
    "pim":    ("#D9544A", "#5A1414"),   # raw red bean
    "zeek":   ("#6FA8C8", "#1E3E58"),   # blue samsa
    "lolly":  ("#D98AB0", "#5E1F42"),   # star cookie
    "crispy": ("#3A2E2B", "#0E0908"),   # charred lump
}
INK = "#0b0606"


def defs():
    g = ""
    for k, (light, dark) in PAL.items():
        g += (f'<radialGradient id="g_{k}" cx="40%" cy="30%" r="80%">'
              f'<stop offset="0%" stop-color="{light}"/><stop offset="70%" stop-color="{dark}"/>'
              f'<stop offset="100%" stop-color="#000"/></radialGradient>')
    g += ('<radialGradient id="eyeglow" r="50%"><stop offset="0%" stop-color="#ffef7a"/>'
          '<stop offset="60%" stop-color="#ff9a1f"/><stop offset="100%" stop-color="#ff3b00" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="potbody" cx="35%" cy="30%" r="85%"><stop offset="0%" stop-color="#4a403c"/>'
          '<stop offset="100%" stop-color="#050303"/></radialGradient>'
          '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>')
    return f"<defs>{g}</defs>"


# ---------- body shapes ----------
def _star(n=5, R=100, r=58, rot=-90):
    pts = []
    for i in range(n * 2):
        rad = R if i % 2 == 0 else r
        a = math.radians(rot + i * 180 / n)
        pts.append(f"{rad*math.cos(a):.1f},{rad*math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


SHAPES = {
    # tall lumpy bread loaf
    "bup": "M-70,90 Q-90,10 -78,-50 Q-70,-105 -20,-108 Q10,-122 40,-104 Q86,-92 80,-30 Q92,40 70,90 Q0,104 -70,90 Z",
    # long skinny bean / egg
    "pim": "M0,-120 Q62,-118 64,-20 Q66,80 0,108 Q-66,80 -64,-20 Q-62,-118 0,-120 Z",
    # samsa triangle with crimped edge
    "zeek": "M0,-112 Q14,-104 96,74 Q100,92 80,96 L-80,96 Q-100,92 -96,74 Q-14,-104 0,-112 Z",
    "lolly": _star(),
    # jagged burnt rock
    "crispy": "M-80,-40 L-60,-86 L-18,-74 L10,-104 L46,-70 L88,-62 L80,-10 L100,32 L62,70 L30,96 L-22,82 L-64,90 L-84,46 L-100,6 Z",
}

# where eyes/mouth sit for each shape (eye y, mouth y, eye spacing)
FACE = {"bup": (-30, 30, 30), "pim": (-40, 30, 22), "zeek": (10, 58, 26),
        "lolly": (-12, 30, 24), "crispy": (-18, 34, 30)}
FEET_Y = {"bup": 92, "pim": 104, "zeek": 96, "lolly": 70, "crispy": 88}


def _eyes(key, look=(0, 0), blink=0.0, scared=False, angry=False):
    ey, _, sp = FACE[key]
    lx, ly = look
    out = ""
    # deliberately uneven eyes = creepier
    sizes = {"bup": (20, 14), "pim": (18, 22), "zeek": (15, 15), "lolly": (17, 13), "crispy": (6, 6)}
    for side, ex in enumerate((-sp, sp)):
        rr = sizes[key][side]
        h = rr * (1 - blink)
        if key == "crispy":
            # glowing ember eyes, no whites
            out += f'<circle cx="{ex}" cy="{ey}" r="{rr*3}" fill="url(#eyeglow)" opacity="{0.9*(1-blink)}"/>'
            out += f'<ellipse cx="{ex+lx*3}" cy="{ey+ly*3}" rx="{rr}" ry="{max(h,1)}" fill="#fff6c0"/>'
            continue
        # dark sunken ring
        out += f'<ellipse cx="{ex}" cy="{ey+3}" rx="{rr+7}" ry="{rr+8}" fill="#000" opacity="0.45"/>'
        out += f'<ellipse cx="{ex}" cy="{ey}" rx="{rr}" ry="{max(h,1.5)}" fill="#f2ecd8" stroke="{INK}" stroke-width="3"/>'
        if blink < 0.7:
            pr = 3 if scared else rr * 0.42
            out += f'<circle cx="{ex+lx*rr*0.45}" cy="{ey+ly*rr*0.45}" r="{pr}" fill="{INK}"/>'
            # red veins
            out += (f'<path d="M{ex-rr},{ey} l{rr*0.35},{rr*0.12} M{ex+rr},{ey+2} l{-rr*0.3},{-rr*0.1}" '
                    f'stroke="#b3122a" stroke-width="1.5" opacity="0.8"/>')
    if angry:
        out += (f'<path d="M{-sp-24},{ey-26} L{-6},{ey-12}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M{sp+24},{ey-26} L{6},{ey-12}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    return out


def _mouth(key, kind="stitch"):
    _, my, _ = FACE[key]
    if kind == "stitch":   # sewn-shut creepy smile
        s = f'<path d="M-22,{my} Q0,{my+12} 22,{my}" fill="none" stroke="{INK}" stroke-width="4"/>'
        for x in (-15, -5, 5, 15):
            yy = my + 6 - abs(x) * 0.25
            s += f'<line x1="{x}" y1="{yy-7}" x2="{x}" y2="{yy+7}" stroke="{INK}" stroke-width="3"/>'
        return s
    if kind == "grin":     # too-wide toothy grin
        t = "".join(f'<path d="M{x},{my} l5,10 l5,-10" fill="#e9e2c8"/>' for x in range(-26, 26, 10))
        return (f'<path d="M-30,{my} Q0,{my+30} 30,{my} Z" fill="#2a0505" stroke="{INK}" stroke-width="4"/>{t}')
    if kind == "scream":
        return (f'<ellipse cx="0" cy="{my+8}" rx="15" ry="24" fill="#1a0202" stroke="{INK}" stroke-width="4"/>'
                f'<ellipse cx="0" cy="{my+20}" rx="8" ry="8" fill="#6b0f15"/>')
    if kind == "smile":
        return f'<path d="M-20,{my} Q0,{my+16} 20,{my}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    if kind == "o":
        return f'<ellipse cx="0" cy="{my+4}" rx="11" ry="9" fill="#1a0202" stroke="{INK}" stroke-width="4"/>'
    if kind == "wobble":
        return f'<path d="M-18,{my+4} q4,-8 9,0 t9,0 t9,0 t9,0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    if kind == "flat":
        return f'<line x1="-16" y1="{my}" x2="16" y2="{my+3}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    return ""


def _limbs(key, step=0.0, arms_up=0.0):
    fy = FEET_Y[key]
    a = 16 * step
    legs = (f'<g stroke="{INK}" stroke-width="5" stroke-linecap="round" fill="none">'
            f'<path d="M-24,{fy-14} q{-4+a/2},20 {-6+a},{40}"/>'
            f'<path d="M24,{fy-14} q{4-a/2},20 {6-a},{40}"/></g>'
            f'<path d="M{-30+a-10},{fy+26} l20,0 l-4,-6" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{30-a+10},{fy+26} l-20,0 l4,-6" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    # thin spindly arms with 3 fingers
    ay = 10 - arms_up * 70
    arms = ""
    for s in (-1, 1):
        hx, hy = s * 120, ay + 30
        arms += (f'<path d="M{s*70},10 Q{s*100},{ay-10} {hx},{hy}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                 f'<path d="M{hx},{hy} l{s*12},-6 M{hx},{hy} l{s*14},4 M{hx},{hy} l{s*6},12" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return legs, arms


def _details(key):
    d = ""
    if key == "bup":   # scored bread cuts + mould spots
        d += (f'<g stroke="#3a1e05" stroke-width="4" fill="none" opacity="0.7"><path d="M-40,-80 q10,-12 22,0"/>'
              f'<path d="M0,-92 q10,-12 22,0"/><path d="M36,-78 q8,-10 18,0"/></g>'
              '<g fill="#5c7a3a" opacity="0.7"><circle cx="-55" cy="50" r="7"/><circle cx="-46" cy="62" r="4"/><circle cx="58" cy="-48" r="5"/></g>')
    if key == "pim":   # bandage + drip
        d += ('<g transform="rotate(-25 30 -85)"><rect x="5" y="-95" width="52" height="16" rx="4" fill="#e9dcc0" stroke="#0b0606" stroke-width="2"/>'
              '<line x1="22" y1="-95" x2="22" y2="-79" stroke="#b9a983"/><line x1="40" y1="-95" x2="40" y2="-79" stroke="#b9a983"/></g>'
              '<path d="M-44,40 q-4,26 2,36 q6,-10 2,-36 Z" fill="#7a0d18"/>')
    if key == "zeek":  # crimped samsa edge + cracked glasses
        d += "".join(f'<path d="M{x},92 l6,8 l6,-8" fill="none" stroke="#0b1a26" stroke-width="3"/>' for x in range(-78, 78, 13))
        d += ('<g fill="none" stroke="#0b0606" stroke-width="4"><rect x="-48" y="-12" width="40" height="40" rx="6"/>'
              '<rect x="8" y="-12" width="40" height="40" rx="6"/><line x1="-8" y1="2" x2="8" y2="2"/></g>'
              '<path d="M14,-10 l10,14 l-6,8 l12,16" stroke="#e8f4ff" stroke-width="2" fill="none"/>')
    if key == "lolly": # icing drips + cracked heart
        d += ('<path d="M-30,-40 Q0,-56 30,-40 L28,-30 Q24,-18 20,-30 Q12,-12 6,-30 Q-2,-6 -8,-30 Q-16,-16 -20,-30 Q-26,-20 -30,-40 Z" fill="#f5d8e8" opacity="0.85"/>'
              '<path d="M-58,-62 q8,6 0,14" stroke="#0b0606" stroke-width="2" fill="none"/>')
    if key == "crispy":  # cracks with glow + smoke
        d += ('<g stroke="#ff5a14" stroke-width="3" fill="none" filter="url(#glow)" opacity="0.9">'
              '<path d="M-60,-10 l20,10 l-8,20 l22,14"/><path d="M40,-50 l-10,24 l16,10"/></g>'
              '<g stroke="#ff8a3a" stroke-width="2" fill="none"><path d="M-60,-10 l20,10 l-8,20 l22,14"/><path d="M40,-50 l-10,24 l16,10"/></g>'
              '<g fill="#5a5250" opacity="0.6"><circle cx="-8" cy="-122" r="14"/><circle cx="10" cy="-146" r="18"/><circle cx="-6" cy="-176" r="22"/></g>')
    return d


def dough(key, x=0, y=0, scale=1.0, look=(0, 0), blink=0.0, mouth="stitch",
          step=0.0, squash=0.0, scared=False, angry=False, rot=0, arms_up=0.0, shiver=0.0):
    sx, sy = 1 + squash * 0.5, 1 - squash
    legs, arms = _limbs(key, step, arms_up)
    jitter = f"translate({shiver*3},{-shiver*2})" if shiver else ""
    body = f'<path d="{SHAPES[key]}" fill="url(#g_{key})" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({scale}) {jitter}">'
            f'<ellipse cx="0" cy="{FEET_Y[key]+30}" rx="70" ry="10" fill="#000" opacity="0.35"/>'
            f'{legs}{arms}<g transform="scale({sx},{sy})">{body}{_details(key)}'
            f'{_eyes(key, look, blink, scared, angry)}{_mouth(key, mouth)}</g></g>')


def mr_pot(x=0, y=0, scale=1.0, look=(0, 0), blink=0.0, mouth="grin", lid=0.0, rot=0):
    """Giant cursed cauldron with three glowing eyes and oil tendrils."""
    lx, ly = look
    eyes = ""
    for ex, ey, r in [(-80, -20, 34), (80, -20, 34), (0, -78, 24)]:
        eyes += f'<circle cx="{ex}" cy="{ey}" r="{r*2.2}" fill="url(#eyeglow)" opacity="{0.55*(1-blink)}"/>'
        eyes += f'<ellipse cx="{ex}" cy="{ey}" rx="{r}" ry="{max(r*(1-blink)*0.8,2)}" fill="#ffe25a" stroke="{INK}" stroke-width="4"/>'
        if blink < 0.7:
            eyes += f'<ellipse cx="{ex+lx*r*0.4}" cy="{ey+ly*r*0.3}" rx="{r*0.18}" ry="{r*0.7}" fill="#9a0000"/>'
            eyes += f'<ellipse cx="{ex+lx*r*0.4}" cy="{ey+ly*r*0.3}" rx="{r*0.08}" ry="{r*0.55}" fill="{INK}"/>'
    brows = (f'<path d="M-135,-70 L-35,-40" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
             f'<path d="M135,-70 L35,-40" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>')
    if mouth == "grin":
        teeth = "".join(f'<path d="M{x},{48 + abs(x)*0.18} l11,{30 - abs(x)*0.12} l11,{-30 + abs(x)*0.12}" fill="#efe6c6" stroke="{INK}" stroke-width="2"/>'
                        for x in range(-132, 132, 22))
        m = f'<path d="M-140,40 Q0,190 140,40 Q0,110 -140,40 Z" fill="#2a0000" stroke="{INK}" stroke-width="6"/>{teeth}'
    elif mouth == "closed":
        m = f'<path d="M-120,60 Q0,110 120,60" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
    elif isinstance(mouth, float):  # talking: 0..1 openness
        o = mouth
        teeth = "".join(f'<path d="M{x},{50 + abs(x)*0.15} l10,{14+o*16} l10,{-14-o*16}" fill="#efe6c6" stroke="{INK}" stroke-width="2"/>'
                        for x in range(-110, 110, 22))
        m = (f'<path d="M-125,50 Q0,{110+o*90} 125,50 Q0,{80+o*20} -125,50 Z" fill="#2a0000" stroke="{INK}" stroke-width="6"/>{teeth}')
    else:  # roar
        teeth = "".join(f'<path d="M{x},40 l10,30 l10,-30" fill="#efe6c6"/>' for x in range(-90, 90, 20))
        m = (f'<ellipse cx="0" cy="95" rx="110" ry="80" fill="#1a0000" stroke="{INK}" stroke-width="6"/>{teeth}'
             '<path d="M-40,140 q40,40 80,0 q-40,-20 -80,0 Z" fill="#8a1020"/>')
    ly_ = -165 - lid * 80
    lidsvg = (f'<g transform="rotate({-lid*18} -220 -165)">'
              f'<path d="M-235,{ly_} Q0,{ly_-70} 235,{ly_} Q0,{ly_+30} -235,{ly_} Z" fill="#2b2523" stroke="{INK}" stroke-width="6"/>'
              f'<path d="M-30,{ly_-38} q30,-40 60,0" fill="none" stroke="{INK}" stroke-width="12"/></g>')
    steam = "" if lid < 0.15 else (
        f'<g fill="#5b8a3a" opacity="{0.55*lid}"><circle cx="-80" cy="-200" r="34"/><circle cx="10" cy="-230" r="46"/>'
        '<circle cx="100" cy="-195" r="30"/></g>')
    drips = "".join(f'<path d="M{x},-150 q-8,{l*0.5} 0,{l} q8,-{l*0.5} 0,-{l} Z" fill="#c9a227" opacity="0.9"/>'
                    for x, l in [(-170, 70), (-110, 40), (60, 90), (150, 55)])
    tendrils = "".join(f'<path d="M{s*200},{-40+i*60} q{s*70},{-30+i*20} {s*90},{40+i*10} q{s*10},30 {s*-20},40" '
                       f'fill="none" stroke="#1b1512" stroke-width="{18-i*4}" stroke-linecap="round"/>'
                       for s in (-1, 1) for i in range(3))
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">'
            '<ellipse cx="0" cy="215" rx="260" ry="30" fill="#000" opacity="0.4"/>'
            f'{tendrils}'
            f'<path d="M-225,-160 L225,-160 Q250,130 130,205 L-130,205 Q-250,130 -225,-160 Z" fill="url(#potbody)" stroke="{INK}" stroke-width="8"/>'
            '<path d="M-185,-130 Q-200,60 -110,170" fill="none" stroke="#6a5f5a" stroke-width="10" stroke-linecap="round" opacity="0.5"/>'
            '<g stroke="#0b0606" stroke-width="4" fill="none" opacity="0.8"><path d="M140,-100 l-20,40 l14,20 l-24,40"/></g>'
            f'{drips}{steam}{lidsvg}{brows}{eyes}{m}</g>')

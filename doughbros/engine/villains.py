"""Villains. Every function: (x, y, scale, look, blink, mouth, rage, t) -> SVG group.
mouth: "closed" | "grin" | "roar" | float 0..1 (talking openness)
rage: 0..1 extra intensity (glow, shaking)
Ground contact is at y + ~200*scale for all villains.
"""
import math
from chars import mr_pot, INK

VILLAINS = {
    "pot":     "Mr. Pot - three-eyed cursed cauldron. Wants to fry the Dough Bros again.",
    "frost":   "Frostbite - ghost made of freezer frost. Whispers, freezes anything it touches.",
    "toaster": "Toastmaw - old chrome toaster with a slot mouth that shoots burning toast.",
    "mixer":   "Whisker - hand mixer that walks on spinning beaters. Giggles. Wants to whip everything.",
}


def _glow_eye(cx, cy, r, look, blink, iris="#ffe25a", pupil="#9a0000"):
    lx, ly = look
    s = f'<circle cx="{cx}" cy="{cy}" r="{r*2.2}" fill="url(#eyeglow)" opacity="{0.55*(1-blink)}"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{max(r*(1-blink)*0.85,2)}" fill="{iris}" stroke="{INK}" stroke-width="4"/>'
    if blink < 0.7:
        s += f'<ellipse cx="{cx+lx*r*0.4}" cy="{cy+ly*r*0.3}" rx="{r*0.2}" ry="{r*0.65}" fill="{pupil}"/>'
    return s


def pot(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    lid = 0.05 + rage * 0.5
    return mr_pot(x, y, scale=scale, look=look, blink=blink, mouth=mouth, lid=lid,
                  rot=math.sin(t * 40) * 2 * rage)


def frost(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    bob = math.sin(t * 2) * 14
    wave = "".join(f'Q{-180+i*60+30},{170+ (18 if i%2 else -12)} {-180+(i+1)*60},{160}' for i in range(6))
    body = (f'<path d="M-180,160 C-200,-40 -120,-230 0,-230 C120,-230 200,-40 180,160 {wave.replace("Q","Q")} Z" '
            f'fill="#cfe9ff" fill-opacity="0.82" stroke="#8fc3ea" stroke-width="6"/>')
    # rebuild bottom edge properly (wavy hem)
    hem = "M180,160 " + " ".join(f"Q{180-i*60-30},{(195 if i % 2 else 140)} {180-(i+1)*60},160" for i in range(6))
    body = (f'<path d="M-180,160 C-200,-40 -120,-230 0,-230 C120,-230 200,-40 180,160 {hem[9:]} Z" '
            f'fill="#d9efff" fill-opacity="0.85" stroke="#7fb6e0" stroke-width="6"/>')
    icicles = "".join(f'<path d="M{xx},{-150+abs(xx)*0.25} l10,{30+(xx%3)*8} l10,{-30-(xx%3)*8} Z" fill="#ffffff" opacity="0.9"/>'
                      for xx in range(-110, 110, 30))
    eyes = (_glow_eye(-60, -60, 30, look, blink, iris="#e9fbff", pupil="#0a3a6a")
            + _glow_eye(60, -60, 30, look, blink, iris="#e9fbff", pupil="#0a3a6a"))
    if isinstance(mouth, float):
        m = f'<ellipse cx="0" cy="40" rx="{30+mouth*20}" ry="{10+mouth*45}" fill="#0a1e33" stroke="{INK}" stroke-width="4"/>'
    elif mouth == "roar":
        m = '<ellipse cx="0" cy="55" rx="70" ry="70" fill="#0a1e33" stroke="#0b0606" stroke-width="5"/>'
    elif mouth == "grin":
        m = '<path d="M-70,30 Q0,95 70,30 Q0,60 -70,30 Z" fill="#0a1e33"/>'
    else:
        m = '<path d="M-40,40 q20,10 40,0 t40,0" fill="none" stroke="#0a1e33" stroke-width="6"/>'
    mist = "".join(f'<circle cx="{math.sin(t*1.5+i)*150}" cy="{150+i*8}" r="{30+i*6}" fill="#eaf6ff" opacity="{0.25+rage*0.2}"/>' for i in range(5))
    arms = (f'<path d="M-170,0 q-90,{-40-rage*60} -120,{-110-rage*40}" stroke="#bfe0f7" stroke-width="26" stroke-linecap="round" fill="none" opacity="0.85"/>'
            f'<path d="M170,0 q90,{-40-rage*60} 120,{-110-rage*40}" stroke="#bfe0f7" stroke-width="26" stroke-linecap="round" fill="none" opacity="0.85"/>')
    return (f'<g transform="translate({x},{y+bob}) scale({scale})">{mist}{arms}{body}{icicles}{eyes}{m}</g>')


def toaster(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    jit = math.sin(t * 50) * 3 * rage
    body = ('<rect x="-210" y="-150" width="420" height="320" rx="70" fill="url(#chrome)" stroke="#0b0606" stroke-width="7"/>'
            '<rect x="-190" y="150" width="380" height="40" rx="12" fill="#1a1a1a" stroke="#0b0606" stroke-width="5"/>'
            '<path d="M-170,-110 Q-190,40 -150,140" stroke="#ffffff" stroke-width="10" opacity="0.35" fill="none"/>')
    # slot = mouth
    if isinstance(mouth, float):
        oy = 18 + mouth * 40
    elif mouth == "roar":
        oy = 70
    elif mouth == "grin":
        oy = 30
    else:
        oy = 14
    slot = (f'<rect x="-150" y="{-150-oy/2}" width="300" height="{oy}" rx="8" fill="#1a0000" stroke="#0b0606" stroke-width="5"/>'
            f'<rect x="-140" y="{-150-oy/2+oy*0.55}" width="280" height="{oy*0.4}" fill="#ff5a14" opacity="{0.4+0.6*rage}"/>')
    toast = ""
    if mouth == "roar" or rage > 0.6:
        toast = f'<g transform="translate(40,{-260-rage*60}) rotate({t*300%360})"><rect x="-60" y="-55" width="120" height="110" rx="25" fill="#3a1a08" stroke="#0b0606" stroke-width="5"/><circle r="22" fill="#ff5a14" opacity="0.8"/></g>'
    eyes = _glow_eye(-90, -20, 34, look, blink, iris="#ff9a1f", pupil="#2a0000") + _glow_eye(90, -20, 34, look, blink, iris="#ff9a1f", pupil="#2a0000")
    brows = ('<path d="M-150,-70 L-50,-45" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/>'
             '<path d="M150,-70 L50,-45" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/>')
    teeth = "".join(f'<path d="M{xx},70 l12,22 l12,-22" fill="#ddd" stroke="#0b0606" stroke-width="2"/>' for xx in range(-96, 96, 24))
    grille = f'<path d="M-110,60 Q0,{120+rage*40} 110,60 Z" fill="#200000" stroke="#0b0606" stroke-width="5"/>{teeth}'
    lever = f'<rect x="210" y="{-60+rage*80}" width="60" height="30" rx="8" fill="#222" stroke="#0b0606" stroke-width="4"/>'
    cord = '<path d="M-210,120 q-120,30 -90,90 q30,40 -60,60" stroke="#111" stroke-width="10" fill="none"/>'
    return (f'<g transform="translate({x+jit},{y}) scale({scale})">{cord}{toast}{body}{slot}{lever}{brows}{eyes}{grille}</g>')


def mixer(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    spin = t * (8 + rage * 30)
    beaters = ""
    for bx in (-55, 55):
        w = 34 * abs(math.cos(spin + bx))
        beaters += (f'<line x1="{bx}" y1="40" x2="{bx}" y2="120" stroke="#9aa" stroke-width="10"/>'
                    f'<ellipse cx="{bx}" cy="165" rx="{w+6}" ry="50" fill="none" stroke="#c9d3d6" stroke-width="7"/>'
                    f'<ellipse cx="{bx}" cy="165" rx="{max(34-w,4)}" ry="50" fill="none" stroke="#8a9599" stroke-width="5"/>')
    body = ('<path d="M-170,-30 Q-180,-190 0,-200 Q190,-190 170,-30 Q160,40 0,50 Q-160,40 -170,-30 Z" fill="#e8e2d0" stroke="#0b0606" stroke-width="7"/>'
            '<path d="M60,-200 q120,-60 200,10 q30,30 -10,50 q-60,-50 -150,-10 Z" fill="#d0c8b0" stroke="#0b0606" stroke-width="6"/>'
            '<path d="M-140,-60 Q-150,-150 -60,-175" stroke="#fff" stroke-width="10" opacity="0.6" fill="none"/>')
    eyes = _glow_eye(-60, -95, 32, look, blink, iris="#c8ff4a", pupil="#1a3300") + _glow_eye(60, -95, 32, look, blink, iris="#c8ff4a", pupil="#1a3300")
    if isinstance(mouth, float):
        m = f'<path d="M-80,-20 Q0,{10+mouth*70} 80,-20 Q0,0 -80,-20 Z" fill="#300" stroke="#0b0606" stroke-width="4"/>'
    elif mouth == "roar":
        m = '<ellipse cx="0" cy="0" rx="80" ry="40" fill="#300" stroke="#0b0606" stroke-width="5"/>'
    else:
        m = ('<path d="M-95,-25 Q0,45 95,-25 Q0,10 -95,-25 Z" fill="#300" stroke="#0b0606" stroke-width="4"/>'
             + "".join(f'<rect x="{xx}" y="-18" width="16" height="16" fill="#fff" stroke="#0b0606" stroke-width="2"/>' for xx in range(-64, 64, 22)))
    splats = "" if rage < 0.3 else "".join(
        f'<circle cx="{math.cos(spin*0.7+i)*220}" cy="{170+math.sin(spin+i)*30}" r="12" fill="#f5efd9" opacity="0.8"/>' for i in range(6))
    return f'<g transform="translate({x},{y-20}) scale({scale})">{beaters}{splats}{body}{eyes}{m}</g>'


DRAW = {"pot": pot, "frost": frost, "toaster": toaster, "mixer": mixer}


def villain_defs():
    return ('<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#d7dde2"/>'
            '<stop offset="45%" stop-color="#6e7880"/><stop offset="55%" stop-color="#9aa6ae"/>'
            '<stop offset="100%" stop-color="#2c3237"/></linearGradient>')

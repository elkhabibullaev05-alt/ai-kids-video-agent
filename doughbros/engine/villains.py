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
    "vacuum":  "Gulpzilla - giant hungry vacuum cleaner in the closet/attic. Sucks up anything small. Loud, greedy, burps dust.",
    "jelly":   "Wobblor - huge green jelly blob in the garden/fridge. Swallows things into its wobbly body. Slow, sticky, giggly-creepy.",
    "kettle":  "Old Hissy - ancient whistling kettle in the bathroom/attic. Hisses steam, screams with its whistle, very grumpy.",
    "scarecrow": "Sir Stuffing - scarecrow made of old kitchen towels in the night garden. Creaky, whispers riddles, has a carved pumpkin head.",
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


def _mouth_generic(mouth, y=40, w=80):
    if isinstance(mouth, float):
        return f'<ellipse cx="0" cy="{y}" rx="{w*0.6+mouth*w*0.3}" ry="{8+mouth*w*0.55}" fill="#1a0000" stroke="{INK}" stroke-width="5"/>'
    if mouth == "roar":
        teeth = "".join(f'<path d="M{x},{y-w*0.45} l10,22 l10,-22" fill="#eee"/>' for x in range(int(-w*0.8), int(w*0.8), 20))
        return f'<ellipse cx="0" cy="{y}" rx="{w}" ry="{w*0.7}" fill="#1a0000" stroke="{INK}" stroke-width="5"/>{teeth}'
    if mouth == "grin":
        teeth = "".join(f'<path d="M{x},{y-4} l9,16 l9,-16" fill="#eee" stroke="{INK}" stroke-width="2"/>' for x in range(int(-w*0.9), int(w*0.9), 18))
        return f'<path d="M{-w},{y-10} Q0,{y+w*0.9} {w},{y-10} Q0,{y+20} {-w},{y-10} Z" fill="#1a0000" stroke="{INK}" stroke-width="5"/>{teeth}'
    return f'<path d="M{-w*0.6},{y} q{w*0.3},{14} {w*0.6},0 t{w*0.6},0" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'


def vacuum(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    jit = math.sin(t * 60) * 4 * rage
    body = ('<path d="M-170,190 L-190,-60 Q-180,-190 0,-200 Q180,-190 190,-60 L170,190 Z" fill="url(#vac)" stroke="#0b0606" stroke-width="7"/>'
            '<rect x="-200" y="160" width="400" height="50" rx="20" fill="#2a2a2e" stroke="#0b0606" stroke-width="6"/>'
            '<circle cx="-150" cy="215" r="30" fill="#111" stroke="#0b0606" stroke-width="5"/><circle cx="150" cy="215" r="30" fill="#111" stroke="#0b0606" stroke-width="5"/>'
            '<path d="M-130,-150 Q-160,0 -120,140" stroke="#fff" stroke-width="10" opacity="0.25" fill="none"/>')
    hose = (f'<path d="M150,-120 C{330+math.sin(t*3)*30},-200 {360},{40+math.sin(t*2)*40} {260+rage*40},{120}" fill="none" stroke="#1a1a1a" stroke-width="44" stroke-linecap="round"/>'
            f'<path d="M150,-120 C{330+math.sin(t*3)*30},-200 {360},{40+math.sin(t*2)*40} {260+rage*40},{120}" fill="none" stroke="#3a3a40" stroke-width="30" stroke-dasharray="6 14" stroke-linecap="round"/>'
            f'<ellipse cx="{260+rage*40}" cy="140" rx="60" ry="26" fill="#0a0a0a" stroke="#0b0606" stroke-width="5"/>')
    dust = "" if rage < 0.3 else "".join(f'<circle cx="{260+rage*40+math.cos(t*9+i)*90*(1-((t*2+i*0.2)%1))}" cy="{140+math.sin(t*9+i)*40}" r="6" fill="#bba" opacity="0.7"/>' for i in range(8))
    eyes = _glow_eye(-70, -70, 34, look, blink, iris="#ff3b3b", pupil="#200") + _glow_eye(70, -70, 34, look, blink, iris="#ff3b3b", pupil="#200")
    brows = '<path d="M-130,-120 L-40,-95" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/><path d="M130,-120 L40,-95" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/>'
    grille = "".join(f'<rect x="{xx}" y="100" width="14" height="40" rx="6" fill="#111"/>' for xx in range(-90, 100, 30))
    return f'<g transform="translate({x+jit},{y}) scale({scale})">{hose}{dust}{body}{grille}{brows}{eyes}{_mouth_generic(mouth, 30, 75)}</g>'


def jelly(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    w = 1 + math.sin(t * 4) * 0.04 * (1 + rage * 2)
    h = 1 - math.sin(t * 4) * 0.04 * (1 + rage * 2)
    body = (f'<g transform="scale({w},{h})"><path d="M-230,200 Q-260,-40 -150,-170 Q0,-260 150,-170 Q260,-40 230,200 Z" fill="#5fd35a" fill-opacity="0.78" stroke="#1f6b1c" stroke-width="7"/>'
            '<path d="M-150,-130 Q-200,-20 -170,100" stroke="#e8ffe0" stroke-width="16" opacity="0.5" fill="none" stroke-linecap="round"/>'
            '<g opacity="0.55"><rect x="60" y="60" width="50" height="50" rx="8" fill="#a33" transform="rotate(20 85 85)"/><circle cx="-60" cy="120" r="22" fill="#fc3"/><path d="M110,-40 l30,10 l-10,30 Z" fill="#36c"/></g></g>')
    drips = "".join(f'<path d="M{xx},195 q-8,{25+5*math.sin(t*3+xx)} 0,{40+5*math.sin(t*3+xx)} q8,-15 0,-40 Z" fill="#5fd35a" opacity="0.8"/>' for xx in (-160, -40, 90, 180))
    eyes = _glow_eye(-70, -60, 30, look, blink, iris="#fffbe0", pupil="#0a3000") + _glow_eye(60, -80, 22, look, blink, iris="#fffbe0", pupil="#0a3000")
    return f'<g transform="translate({x},{y}) scale({scale})">{body}{drips}{eyes}{_mouth_generic(mouth, 40, 85)}</g>'


def kettle(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    jit = math.sin(t * 50) * 3 * rage
    body = ('<path d="M-200,190 Q-240,-40 -120,-130 L120,-130 Q240,-40 200,190 Z" fill="url(#chrome)" stroke="#0b0606" stroke-width="7"/>'
            '<ellipse cx="0" cy="-135" rx="125" ry="26" fill="#6e7880" stroke="#0b0606" stroke-width="6"/>'
            '<circle cx="0" cy="-170" r="26" fill="#2a2a2a" stroke="#0b0606" stroke-width="5"/>'
            '<path d="M-150,-90 Q-260,-120 -260,20 Q-260,110 -190,120" fill="none" stroke="#2a2a2a" stroke-width="26" stroke-linecap="round"/>'
            '<path d="M180,40 L330,-90 L350,-60 L215,90 Z" fill="url(#chrome)" stroke="#0b0606" stroke-width="6"/>')
    steam = "".join(f'<circle cx="{350+i*25+math.sin(t*5+i)*15}" cy="{-100-i*45-(t*80%40)}" r="{18+i*7}" fill="#f2f2f2" opacity="{(0.3+0.5*rage)*(1-i/7)}"/>' for i in range(6))
    eyes = _glow_eye(-80, -30, 32, look, blink, iris="#ffdf3a", pupil="#300") + _glow_eye(70, -30, 32, look, blink, iris="#ffdf3a", pupil="#300")
    brows = '<path d="M-140,-80 L-40,-55" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/><path d="M130,-80 L30,-55" stroke="#0b0606" stroke-width="14" stroke-linecap="round"/>'
    return f'<g transform="translate({x+jit},{y}) scale({scale})">{steam}{body}{brows}{eyes}{_mouth_generic(mouth, 75, 70)}</g>'


def scarecrow(x, y, scale=1.0, look=(0, 0), blink=0.0, mouth="closed", rage=0.0, t=0.0):
    sway = math.sin(t * 1.5) * 4 + math.sin(t * 30) * 2 * rage
    pole = '<rect x="-14" y="-60" width="28" height="270" fill="#5a3a1a" stroke="#0b0606" stroke-width="5"/>'
    arms = f'<g transform="rotate({sway*0.5})"><rect x="-260" y="-40" width="520" height="24" fill="#5a3a1a" stroke="#0b0606" stroke-width="5"/>'
    arms += '<path d="M-250,-30 L-200,-60 L-80,-60 L-60,90 L60,90 L80,-60 L200,-60 L250,-30 L240,0 L200,-10 L120,40 L-120,40 L-200,-10 L-240,0 Z" fill="#a8423a" stroke="#0b0606" stroke-width="6"/>'
    arms += '<path d="M-60,-60 l20,150 M0,-60 v150 M60,-60 l-20,150" stroke="#e8d0b0" stroke-width="6" opacity="0.6"/>'
    arms += "".join(f'<path d="M{s*255},-25 l{s*25},-15 M{s*255},-20 l{s*30},5 M{s*255},-15 l{s*20},20" stroke="#d9b45a" stroke-width="5"/>' for s in (-1, 1)) + '</g>'
    head = ('<ellipse cx="0" cy="-150" rx="120" ry="100" fill="#e8822a" stroke="#0b0606" stroke-width="7"/>'
            '<path d="M-60,-235 Q0,-260 60,-235 M-100,-180 Q-110,-130 -95,-80 M100,-180 Q110,-130 95,-80" stroke="#b85a14" stroke-width="5" fill="none"/>'
            '<path d="M-10,-250 q10,-40 30,-50" stroke="#3a6a1a" stroke-width="12" fill="none" stroke-linecap="round"/>'
            '<path d="M-150,-200 L150,-200 L110,-280 L-110,-280 Z" fill="#3a2a1a" stroke="#0b0606" stroke-width="6"/><rect x="-200" y="-210" width="400" height="22" rx="10" fill="#3a2a1a" stroke="#0b0606" stroke-width="6"/>')
    lx, ly = look
    eyes = ""
    for ex in (-45, 45):
        eyes += f'<path d="M{ex-28},-140 L{ex},-185 L{ex+28},-140 Z" fill="#1a0800"/>'
        eyes += f'<circle cx="{ex+lx*6}" cy="{-152+ly*5}" r="{12*(1-blink)}" fill="#ffd23a" opacity="{0.6+0.4*(1-blink)}"/>'
    m = _mouth_generic(mouth, -100, 60) if mouth not in ("closed",) else '<path d="M-60,-105 l15,12 l15,-12 l15,12 l15,-12 l15,12 l15,-12 l15,12" fill="none" stroke="#1a0800" stroke-width="8"/>'
    crow = f'<g transform="translate(200,{-60+math.sin(t*2)*3})"><ellipse rx="26" ry="18" fill="#111"/><circle cx="20" cy="-14" r="12" fill="#111"/><path d="M30,-14 l14,4 l-14,4 Z" fill="#e0a020"/><circle cx="23" cy="-16" r="3" fill="#ffd23a"/></g>'
    return f'<g transform="translate({x},{y}) rotate({sway} 0 200) scale({scale})">{pole}{arms}{head}{eyes}{m}{crow}</g>'


DRAW = {"pot": pot, "frost": frost, "toaster": toaster, "mixer": mixer,
        "vacuum": vacuum, "jelly": jelly, "kettle": kettle, "scarecrow": scarecrow}


def villain_defs():
    return ('<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#d7dde2"/>'
            '<stop offset="45%" stop-color="#6e7880"/><stop offset="55%" stop-color="#9aa6ae"/>'
            '<stop offset="100%" stop-color="#2c3237"/></linearGradient>'
            '<linearGradient id="vac" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#b03a4a"/>'
            '<stop offset="100%" stop-color="#3a0a14"/></linearGradient>')

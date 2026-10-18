"""Inspector Bolt — generic story renderer (Blender 4.2, EEVEE).

blender -b --factory-startup -P engine/story.py -- --tl out/epNNN/timeline.json --out out/epNNN/frames --res 854 [--samples 4] [--frames a,b,c] [--range 1-900]
The timeline (from voices.py) carries the script: set, chars, props, beats (+ start/dur/mouth per beat).
Vocabulary of actions and cameras: story/SCRIPT_FORMAT.md. Writes frames f_0001.png… and events.json (sfx cues).
"""
import bpy, math, sys, json, os, random
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d):
    return type(d)(a[a.index(k) + 1]) if k in a else d
TL = json.load(open(arg("--tl", "timeline.json")))
OUT = arg("--out", "frames"); RES = arg("--res", 854); SAMPLES = arg("--samples", 4)
FPS = TL["fps"]; os.makedirs(OUT, exist_ok=True)
SET = TL.get("set", {"press": True, "podium": True})
rnd = random.Random(TL.get("seed", 4))
TINY = (0.001, 0.001, 0.001)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE_NEXT"; sc.eevee.taa_render_samples = SAMPLES
sc.render.resolution_x, sc.render.resolution_y = RES, (RES * 9 // 16) // 2 * 2
sc.render.fps = FPS; sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "Medium High Contrast"
F = lambda t: int(round(t * FPS)) + 1
sc.frame_start, sc.frame_end = 1, F(TL["duration"])


def mat(name, color, rough=0.5, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = emit
    return m


def add(o, m=None, smooth=True):
    if m: o.data.materials.append(m)
    if smooth and hasattr(o.data, "polygons"):
        for p in o.data.polygons: p.use_smooth = True
    return o


def K(o, t, path, val):
    setattr(o, path, val); o.keyframe_insert(data_path=path, frame=max(1, F(t)))


def parent(child, par):
    child.parent = par; child.matrix_parent_inverse = par.matrix_world.inverted()

# ---------------- set ----------------
TOD = SET.get("time", "sunset")  # day | sunset | night
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[1].default_value = {"day": 1.2, "sunset": 1.1, "night": 0.25}[TOD]
sky = w.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "HOSEK_WILKIE"; sky.turbidity = 3.0
sky.sun_direction = {"day": (0.3, -0.4, 0.85), "sunset": (0.6, 0.5, 0.25), "night": (0.6, 0.5, 0.05)}[TOD]
w.node_tree.links.new(sky.outputs[0], bg.inputs[0])
bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, -0.01)); add(bpy.context.object, mat("plaza", (0.55, 0.5, 0.45), 0.85))
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -6, 0)); r = bpy.context.object; r.scale = (200, 7, 1); add(r, mat("road", (0.17, 0.17, 0.18), 0.8))
yel = mat("yel", (0.95, 0.75, 0.05))
for x in range(-60, 60, 6):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, -6, 0.005)); d = bpy.context.object; d.scale = (2.4, 0.18, 1); add(d, yel)
HOUSE_COLS = [(0.85, 0.55, 0.4), (0.6, 0.75, 0.85), (0.9, 0.8, 0.55), (0.7, 0.85, 0.65), (0.85, 0.65, 0.8)]
win_m = mat("win", (1.0, 0.8, 0.4), 0.4, 0, 2.0 if TOD != "day" else 0.3)
for i in range(14):
    x = -40 + i * 6.2; y = 26 + rnd.uniform(-2, 3); h = rnd.uniform(5, 10)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, h / 2)); hs = add(bpy.context.object, mat(f"h{i}", rnd.choice(HOUSE_COLS), 0.9), False)
    hs.scale = (5.2, 5, h)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=3.9, depth=2.5, location=(x, y, h + 1.25), rotation=(0, 0, math.radians(45))); add(bpy.context.object, mat(f"r{i}", (0.6, 0.18, 0.12), 0.8), False)
    for wx in (-1.3, 1.3):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x + wx, y - 2.52, h * 0.6), rotation=(math.radians(90), 0, 0)); add(bpy.context.object, win_m, False).scale = (1.1, 1.3, 1)
for x in (-22, 22):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=6, location=(x, 20, 3)); add(bpy.context.object, mat("pole", (0.1, 0.1, 0.1)))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(x, 20, 6.2)); add(bpy.context.object, mat("bulb", (1, 0.85, 0.5), 0.3, 0, 8))
    bpy.ops.object.light_add(type="POINT", location=(x, 20, 6)); bpy.context.object.data.energy = 800 if TOD != "night" else 3000; bpy.context.object.data.color = (1, 0.8, 0.5)
bpy.ops.object.light_add(type="SUN", location=(0, 0, 40)); sun = bpy.context.object
sun.data.energy = {"day": 4.5, "sunset": 4.0, "night": 0.6}[TOD]; sun.data.color = (1, 0.88, 0.75) if TOD != "night" else (0.6, 0.7, 1)
sun.rotation_euler = (math.radians(55), 0, math.radians(-35))
if TOD == "night":
    bpy.ops.object.light_add(type="AREA", location=(0, -20, 12)); fl = bpy.context.object; fl.data.energy = 6000; fl.data.size = 20
    fl.rotation_euler = (Vector((0, 8, 0)) - fl.location).to_track_quat("-Z", "Y").to_euler()

stone = mat("stone", (0.85, 0.85, 0.82), 0.6)
PODIUM_TOP = Vector((0, 16, 3.6))
if SET.get("podium", True):
    for i, (rr, hh) in enumerate(((3.2, 0.6), (2.6, 0.6), (2.0, 0.8))):
        bpy.ops.mesh.primitive_cylinder_add(radius=rr, depth=hh, location=(0, 16, 0.3 + i * 0.6 + (0.1 if i == 2 else 0))); add(bpy.context.object, stone)
    bpy.ops.object.light_add(type="SPOT", location=(0, 10, 12)); spot = bpy.context.object; spot.data.energy = 3000; spot.data.spot_size = math.radians(30)
    spot.rotation_euler = (Vector((0, 16, 3)) - spot.location).to_track_quat("-Z", "Y").to_euler()

steel, red = mat("steel", (0.8, 0.8, 0.82), 0.25, 1.0), mat("red", (0.85, 0.12, 0.08), 0.4)
DRUMS = []
if SET.get("press", True):
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=2.6, depth=2.0, location=(side * 11, 0, -6), rotation=(0, math.radians(90), 0)); dr = add(bpy.context.object, steel)
        for off in (-0.5, 0.5):
            bpy.ops.mesh.primitive_torus_add(major_radius=2.62, minor_radius=0.1, location=(side * 11 + off, 0, -6), rotation=(0, math.radians(90), 0))
            parent(add(bpy.context.object, red), dr)
        dr.keyframe_insert("location", frame=1)
        DRUMS.append((dr, side))

# ---------------- characters ----------------
black, eyew, tire = mat("black", (0.02, 0.02, 0.02), 0.4), mat("eyew", (0.98, 0.98, 0.98), 0.2), mat("tire", (0.05, 0.05, 0.05), 0.9)
mouth_m, glass = mat("mouth", (0.35, 0.03, 0.05), 0.5), mat("glass", (0.25, 0.45, 0.6), 0.05, 0.3)
hat_m = mat("hat", (0.25, 0.18, 0.1), 0.7)
C = {}


def make_hat(size):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9 * size, depth=0.08); brim = add(bpy.context.object, hat_m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * size, depth=0.6 * size, location=(0, 0, 0.3 * size)); top = add(bpy.context.object, hat_m)
    top.parent = brim
    return brim


def make_char(key, ch):
    size, kind = ch.get("size", 1.0), ch.get("kind", "car")
    root = bpy.data.objects.new(key, None); sc.collection.objects.link(root)
    body_m = mat(f"b_{key}", tuple(ch["color"]), 0.25)
    L = {"small": 3.2, "car": 4.2, "bus": 8.5, "truck": 6.5}[kind] * size
    H = {"small": 1.3, "car": 1.4, "bus": 2.9, "truck": 2.5}[kind] * size
    Wd = (2.6 if kind == "bus" else 2.3 if kind == "truck" else 2.0) * size
    body = bpy.data.objects.new(key + "_body", None); sc.collection.objects.link(body); body.parent = root
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.55 * size + H / 2)); b = add(bpy.context.object, body_m)
    b.scale = (Wd, L, H); bpy.ops.object.modifier_add(type="BEVEL"); b.modifiers[-1].width = 0.25 * size; b.modifiers[-1].segments = 4; b.parent = body
    top_z = 0.55 * size + H
    if kind in ("car", "small"):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.15 * L, top_z + 0.35 * size)); c = add(bpy.context.object, glass)
        c.scale = (Wd * 0.85, L * 0.45, 0.75 * size); bpy.ops.object.modifier_add(type="BEVEL"); c.modifiers[-1].width = 0.2 * size; c.parent = body
        top_z += 0.75 * size
    else:
        for k in range(int(L / (1.6 * size))):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -L / 2 + (k + 0.8) * 1.6 * size, 0.55 * size + H * 0.72))
            g = add(bpy.context.object, glass, False); g.scale = (Wd + 0.02, 1.1 * size, 0.6 * size); g.parent = body
    for sx in (-1, 1):
        for sy in (-0.33, 0.33):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * size, depth=0.45 * size, location=(sx * Wd / 2, sy * L, 0.55 * size), rotation=(0, math.radians(90), 0))
            add(bpy.context.object, tire).parent = body
    fy = -L / 2 - 0.05 * size; fz = 0.55 * size + H * 0.62
    eyes = []
    brow_tilt = ch.get("brows", 8)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * size, location=(sx * Wd * 0.24, fy, fz)); e = add(bpy.context.object, eyew)
        e.scale = (1, 0.5, 1.15); e.parent = body; eyes.append(e)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2 * size, location=(sx * Wd * 0.24, fy - 0.2 * size, fz - 0.05 * size)); parent(add(bpy.context.object, black), e)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * Wd * 0.24, fy - 0.05 * size, fz + 0.62 * size)); br = add(bpy.context.object, black, False)
        br.scale = (0.55 * size, 0.08, 0.12 * size); br.rotation_euler = (0, sx * math.radians(-brow_tilt), 0); br.parent = body
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32 * size, location=(0, fy, 0.55 * size + H * 0.24)); mo = add(bpy.context.object, mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    hat = make_hat(size); hat.location = (0, 0.15 * L, top_z + 0.05); hat.parent = body
    if not ch.get("hat"):
        hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=size,
                  home=Vector((hx, hy, 0)), top=top_z, has_hat=bool(ch.get("hat")))


for key, ch in TL["chars"].items():
    if key != "narr" and "color" in ch:
        make_char(key, ch)

# ---------------- props ----------------
PCOL = {"gold": (1.0, 0.72, 0.15), "red": (0.9, 0.1, 0.1), "blue": (0.1, 0.35, 0.95), "green": (0.15, 0.75, 0.25),
        "yellow": (1, 0.85, 0.1), "pink": (1, 0.45, 0.7), "white": (0.95, 0.95, 0.95), "orange": (1, 0.5, 0.1), "purple": (0.6, 0.25, 0.85)}
P = {}


def make_prop(p):
    col = p.get("color", "gold"); col = PCOL.get(col, col) if isinstance(col, str) else tuple(col)
    shiny = col == PCOL["gold"]
    m = mat("p_" + p["id"], col, 0.18 if shiny else 0.45, 1.0 if shiny else 0.0, 0.4 if shiny else 0)
    t = p.get("type", "box"); s = p.get("scale", 1.0)
    root = bpy.data.objects.new("prop_" + p["id"], None); sc.collection.objects.link(root)
    if t == "wheel":
        bpy.ops.mesh.primitive_torus_add(major_radius=1.1, minor_radius=0.38, rotation=(math.radians(90), 0, 0)); o = add(bpy.context.object, m)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.6, rotation=(math.radians(90), 0, 0)); parent(add(bpy.context.object, m), o)
    elif t == "ball":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.9); o = add(bpy.context.object, m)
    elif t == "banana":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35); o = add(bpy.context.object, m); o.scale = (0.6, 1.6, 0.6)
    elif t == "cone":
        bpy.ops.mesh.primitive_cone_add(radius1=0.6, depth=1.4, location=(0, 0, 0.7)); o = add(bpy.context.object, m)
    elif t == "star":
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=1.0, depth=0.4, rotation=(math.radians(90), 0, 0)); o = add(bpy.context.object, m, False)
    elif t == "trophy":
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.3); o = add(bpy.context.object, m)
        bpy.ops.mesh.primitive_cone_add(radius1=0.2, radius2=0.8, depth=1.2, location=(0, 0, 0.8)); parent(add(bpy.context.object, m), o)
    elif t == "cake":
        bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.7, location=(0, 0, 0.35)); o = add(bpy.context.object, m)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.5, location=(0, 0, 0.95)); parent(add(bpy.context.object, mat("candle", (1, 1, 0.9), 0.4, 0, 3)), o)
    elif t == "key":
        bpy.ops.mesh.primitive_torus_add(major_radius=0.4, minor_radius=0.1, rotation=(math.radians(90), 0, 0)); o = add(bpy.context.object, m)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.8, 0, 0)); bar = add(bpy.context.object, m, False); bar.scale = (1.0, 0.1, 0.12); parent(bar, o)
    else:  # box / gift
        bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, 0, 0.6)); o = add(bpy.context.object, m, False)
        if t == "gift":
            for sx, sy in ((0.13, 1.25), (1.25, 0.13)):
                bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.6)); rb = add(bpy.context.object, mat("ribbon", (0.95, 0.95, 0.2)), False)
                rb.scale = (sx, sy, 1.22); parent(rb, o)
    o.parent = root
    root.scale = (s, s, s)
    if p.get("on") == "podium":
        root.location = PODIUM_TOP
    elif p.get("on") in C:
        c = C[p["on"]]; root.parent = c["root"]; root.location = (0, 0, c["top"] + 0.6)
    else:
        root.location = tuple(p.get("at", (0, 0, 0.5)))
    if not p.get("visible", True):
        root.scale = TINY
    root.keyframe_insert("scale", frame=1); root.keyframe_insert("location", frame=1)
    P[p["id"]] = dict(root=root, s=s, home=root.location.copy())


for p in TL.get("props", []):
    make_prop(p)

# ---------------- action helpers ----------------
POS = {k: C[k]["home"].copy() for k in C}
FACE = {k: 0.0 for k in C}
EVENTS = []
DRUMS_UP = [False]


def move(c, t, d, to):
    r = C[c]["root"]; to = Vector(to)
    K(r, t, "location", POS[c]); K(r, t + d, "location", to); POS[c] = to


def face(c, t, d, ang):
    r = C[c]["root"]
    K(r, t, "rotation_euler", (0, 0, FACE[c])); K(r, t + d, "rotation_euler", (0, 0, ang)); FACE[c] = ang


def look_at(c, t, target):
    v = (POS[target] if target in POS else Vector(target)) - POS[c]
    face(c, t, 0.6, math.atan2(v.x, -v.y) if v.length > 0.1 else 0)


def bounce(c, t, n=1, h=0.8):
    b = C[c]["body"]
    for i in range(n):
        K(b, t + i * 0.35, "location", (0, 0, 0)); K(b, t + i * 0.35 + 0.17, "location", (0, 0, h)); K(b, t + i * 0.35 + 0.34, "location", (0, 0, 0))


def body_scale(c, t, d, s, back_at=None):
    b = C[c]["body"]
    K(b, t, "scale", (1, 1, 1)); K(b, t + d, "scale", s)
    if back_at:
        K(b, back_at, "scale", s); K(b, back_at + 0.4, "scale", (1, 1, 1))


def eyes(c, t, sx, sz, until):
    for e in C[c]["eyes"]:
        K(e, t, "scale", (1, 0.5, 1.15)); K(e, t + 0.35, "scale", (sx, 0.5, sz))
        K(e, until, "scale", (sx, 0.5, sz)); K(e, until + 0.3, "scale", (1, 0.5, 1.15))


def drums_up(t):
    if DRUMS and not DRUMS_UP[0]:
        for dr, side in DRUMS:
            K(dr, t, "location", (side * 11, 0, -6)); K(dr, t + 0.45, "location", (side * 11, 0, 2.6))
        DRUMS_UP[0] = True; EVENTS.append((t, "rumble"))


def drums_down(t):
    if DRUMS and DRUMS_UP[0]:
        for dr, side in DRUMS:
            K(dr, t, "location", (side * 11, 0, 2.6)); K(dr, t + 0.6, "location", (side * 11, 0, -6))
        DRUMS_UP[0] = False


def squeeze(t, gap, hold):
    drums_up(t - 0.5)
    for dr, side in DRUMS:
        K(dr, t, "location", (side * 11, 0, 2.6)); K(dr, t + 0.35, "location", (side * gap, 0, 2.6))
        K(dr, t + 0.35 + hold, "location", (side * gap, 0, 2.6)); K(dr, t + 0.8 + hold, "location", (side * 11, 0, 2.6))


def prop_world(pid, t):
    sc.frame_set(F(t)); return P[pid]["root"].matrix_world.translation.copy()


def char_point(c, dz=0.0):
    return POS[c] + Vector((0, 0, C[c]["top"] + dz))


def do_char(c, act, t, d):
    arg_ = act.split(":", 1)[1] if ":" in act else None
    name = act.split(":")[0]
    if name == "enter":
        side = -1 if arg_ == "left" else 1
        start = Vector((side * 40, C[c]["home"].y, 0))
        C[c]["root"].location = start; C[c]["root"].keyframe_insert("location", frame=1)
        K(C[c]["root"], t, "location", start); K(C[c]["root"], t + 1.6, "location", C[c]["home"]); POS[c] = C[c]["home"].copy()
        EVENTS.append((t, "engine"))
    elif name == "exit":
        move(c, t, 1.4, (40, POS[c].y, 0)); EVENTS.append((t, "engine"))
    elif name == "to_press":
        drums_up(t); move(c, t, 1.2, (0, 0, 0)); EVENTS.append((t, "engine"))
    elif name == "to_home":
        move(c, t, 1.2, C[c]["home"]); face(c, t, 0.5, 0)
    elif name == "to":
        tgt = POS[arg_] + Vector((4.5, 3.0, 0)) if arg_ in POS else Vector([float(v) for v in arg_.split(",")] + [0])[:3]
        move(c, t, 1.5, tgt); EVENTS.append((t, "engine"))
        if arg_ in POS: look_at(c, t + 1.2, arg_)
    elif name == "turn":
        if arg_ in (None, "front"): face(c, t, 0.5, 0)
        else: look_at(c, t, arg_)
    elif name == "jump":
        bounce(c, t, 2, 0.9); EVENTS.append((t, "boing"))
    elif name == "laugh":
        bounce(c, t + 0.2, 4, 0.4)
    elif name == "shake":
        r = C[c]["root"]
        for k in range(6):
            K(r, t + k * 0.12, "rotation_euler", (0, 0, FACE[c] + math.radians(8 if k % 2 else -8)))
        K(r, t + 0.8, "rotation_euler", (0, 0, FACE[c]))
    elif name == "spin":
        r = C[c]["root"]; K(r, t, "rotation_euler", (0, 0, FACE[c])); K(r, t + 0.8, "rotation_euler", (0, 0, FACE[c] + 2 * math.pi))
        K(r, t + 0.81, "rotation_euler", (0, 0, FACE[c])); EVENTS.append((t, "whoosh"))
    elif name == "eyes_big":
        eyes(c, t, 1.6, 1.85, t + d + 0.5); EVENTS.append((t, "dun"))
    elif name == "sad":
        eyes(c, t, 1.0, 0.55, t + d + 2.5)
    elif name == "happy":
        eyes(c, t, 1.15, 0.8, t + d + 1.0); bounce(c, t + 0.2, 2, 0.4)
    elif name == "sleep":
        eyes(c, t, 1.0, 0.12, t + d)
    elif name == "flat_roof":
        body_scale(c, t, 0.2, (1.0, 1.0, 0.6), back_at=t + d + 1.5); EVENTS.append((t, "squish"))
    elif name == "squash":
        body_scale(c, t, 0.12, (0.3, 1.1, 1.0), back_at=t + d + 0.8); EVENTS.append((t, "crunch"))
    elif name == "hat_give" and arg_ in C:
        K(C[c]["hat"], t + 0.3, "scale", (1, 1, 1)); K(C[c]["hat"], t + 0.6, "scale", TINY)
        K(C[arg_]["hat"], t + 0.6, "scale", TINY); K(C[arg_]["hat"], t + 0.9, "scale", (1, 1, 1)); EVENTS.append((t + 0.6, "chime"))


def do_prop(pid, act, t, d):
    pr = P[pid]; r = pr["root"]; s = pr["s"]
    arg_ = act.split(":", 1)[1] if ":" in act else None
    name = act.split(":")[0]
    if name in ("show", "appear"):
        K(r, t, "scale", TINY); K(r, t + 0.25, "scale", (s, s, s)); EVENTS.append((t, "chime"))
    elif name in ("hide", "vanish"):
        K(r, t, "scale", (s, s, s)); K(r, t + 0.15, "scale", TINY); EVENTS.append((t, "pop"))
    elif name == "spin":
        K(r, t, "rotation_euler", (0, 0, 0)); K(r, t + d + 2, "rotation_euler", (0, 0, 2 * math.pi))
    elif name == "bounce":
        p0 = prop_world(pid, t)
        K(r, t, "location", p0); K(r, t + 0.2, "location", p0 + Vector((0, 0, 1.2))); K(r, t + 0.4, "location", p0); EVENTS.append((t, "boing"))
    elif name == "drop" and arg_ in C:  # falls out of a character onto the ground in front of the camera side
        start = char_point(arg_, 0.2); end = POS[arg_] + Vector((0.8, -C[arg_]["L"] / 2 - 1.5, 0.3))
        K(r, t, "scale", TINY); K(r, t + 0.05, "scale", (s, s, s))
        K(r, t + 0.05, "location", start); K(r, t + 0.5, "location", end); EVENTS.append((t + 0.5, "boing"))
    elif name in ("give", "to") and arg_ in C:
        p0 = prop_world(pid, t); end = char_point(arg_, 0.7)
        K(r, t, "location", p0); K(r, t + 0.4, "location", (p0 + end) / 2 + Vector((0, 0, 2))); K(r, t + 0.8, "location", end)
        K(r, t + 0.8, "scale", (s, s, s)); EVENTS.append((t + 0.8, "chime"))
    elif name == "home":
        p0 = prop_world(pid, t); K(r, t, "location", p0); K(r, t + 0.8, "location", pr["home"]); K(r, t + 0.8, "scale", (s, s, s))


TRK = mat("track", (0.12, 0.1, 0.08), 0.9)


def tracks(t, a_, b_):
    p0, p1 = (POS[a_] if a_ in POS else Vector((0, 8, 0))), (POS[b_] if b_ in POS else Vector((0, 8, 0)))
    for i in range(16):
        q = p0.lerp(p1, i / 15)
        for sx in (-0.35, 0.35):
            bpy.ops.mesh.primitive_plane_add(size=1, location=(q.x, q.y + sx, 0.012)); tr = add(bpy.context.object, TRK, False); tr.scale = (0.45, 0.18, 1)
            tr.hide_render = True; tr.keyframe_insert("hide_render", frame=1); tr.keyframe_insert("hide_render", frame=F(t + 0.05 * i))
            tr.hide_render = False; tr.keyframe_insert("hide_render", frame=F(t + 0.05 * i) + 1)
    EVENTS.append((t, "clue"))


for b in TL["beats"]:
    t, d = b["start"], b["dur"]
    if b.get("who") in C and b.get("mouth"):  # lip flap + talking bob
        mo = C[b["who"]]["mouth"]
        K(mo, t - 1 / FPS, "scale", (1.3, 0.3, 0.25))
        for j, lv in enumerate(b["mouth"]):
            K(mo, t + j / FPS, "scale", (1.3 - 0.25 * lv, 0.3, 0.25 + 1.4 * lv))
        K(mo, t + d + 1 / FPS, "scale", (1.3, 0.3, 0.25))
        bb = C[b["who"]]["body"]
        K(bb, t, "rotation_euler", (0, 0, 0)); K(bb, t + d / 2, "rotation_euler", (math.radians(2.5), 0, 0)); K(bb, t + d, "rotation_euler", (0, 0, 0))
    for who, act in b.get("do", []):
        try:
            if who == "press":
                if act in ("rise", "show"): drums_up(t)
                elif act in ("sink", "hide"): drums_down(t)
                elif act == "clap": squeeze(t + 0.6, 0.9, 0.2); EVENTS.append((t + 0.95, "clang"))
                elif act.startswith("squeeze:"):
                    c = act.split(":")[1]; squeeze(t + 0.3, C[c]["W"] / 2 + 2.3, max(0.3, d - 0.6)); EVENTS.append((t + 0.65, "crunch"))
                    body_scale(c, t + 0.55, 0.15, (0.82, 1, 1), back_at=t + d - 0.2)
            elif who == "fx" and act.startswith("tracks:"):
                a_, b_ = act.split(":")[1].split("-"); tracks(t, a_, b_)
            elif who == "all":
                for c in C:
                    if act.startswith("look:"):
                        if c != act.split(":")[1]: look_at(c, t, act.split(":")[1])
                    else:
                        do_char(c, act, t + rnd.uniform(0, 0.2), d)
                if act.startswith("look:"): EVENTS.append((t, "dun"))
            elif who in C:
                do_char(who, act, t, d)
            elif who in P:
                do_prop(who, act, t, d)
        except Exception as e:  # never let one bad action kill a 3-hour render
            print("ACTION SKIPPED", who, act, e)

# ---------------- cameras (hard cuts + slow push-in) ----------------
bpy.ops.object.camera_add(location=(0, -20, 6)); cam = bpy.context.object; sc.camera = cam


def at(c, t):
    sc.frame_set(F(t)); return C[c]["root"].matrix_world.translation.copy()


def shot(name, t, t_end):
    tm = min(t + 1.6, (t + t_end) / 2)
    if name == "wide":
        loc, tgt, lens = Vector((-3, -13, 6.0)), Vector((-3, 9, 1.0)), 26
    elif name == "press":
        loc, tgt, lens = Vector((0, -13, 3.6)), Vector((0, 0, 1.8)), 26
    elif name == "podium":
        loc, tgt, lens = Vector((0, 6.5, 3.4)), Vector((0, 16, 3.3)), 30
    elif name == "overhead":
        loc, tgt, lens = Vector((-3, -2, 16)), Vector((-3, 8, 0)), 22
    elif name.startswith("prop:"):
        p = prop_world(name.split(":")[1], tm); loc, tgt, lens = p + Vector((1.5, -7, 2.5)), p, 35
    elif name.startswith("two:"):
        a_, b_ = name.split(":")[1].split(","); pa, pb = at(a_, tm), at(b_, tm); mid = (pa + pb) / 2
        dist = max(9, (pa - pb).length * 1.1 + 6); loc, tgt, lens = mid + Vector((0, -dist, 3.2)), mid + Vector((0, 0, 1.2)), 30
    else:  # close:<char>
        c = name.split(":")[1]; p = at(c, tm); L = C[c]["L"]
        loc, tgt, lens = p + Vector((1.2, -L / 2 - 7.5 - C[c]["H"], 2.4 + C[c]["H"] * 0.4)), p + Vector((0, -L / 2, 0.6 + C[c]["H"] * 0.6)), 35
    q = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
    for path, val in (("location", loc), ("rotation_euler", q)):
        setattr(cam, path, val); cam.keyframe_insert(path, frame=max(1, F(t)))
    cam.data.lens = lens; cam.data.keyframe_insert("lens", frame=max(1, F(t)))
    cam.location = loc + (tgt - loc).normalized() * min(1.2, 0.3 * (t_end - t)); cam.keyframe_insert("location", frame=F(t_end) - 1)


cuts = []
for b in TL["beats"]:
    cam_ = b.get("cam", "wide")
    if not cuts or cuts[-1][0] != cam_:
        cuts.append([cam_, b["start"]])
for i, (name, t) in enumerate(cuts):
    t_end = cuts[i + 1][1] - 0.15 if i + 1 < len(cuts) else TL["duration"]
    try:
        shot(name, max(0, t - 0.15), t_end)
    except Exception as e:
        print("SHOT FALLBACK", name, e); shot("wide", max(0, t - 0.15), t_end)
for act in (cam.animation_data.action, cam.data.animation_data.action):
    for fc in act.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT" if fc.data_path in ("rotation_euler", "lens") else "LINEAR"
for fc in cam.animation_data.action.fcurves:
    if fc.data_path == "location":
        for k, kp in enumerate(fc.keyframe_points):
            kp.interpolation = "LINEAR" if k % 2 == 0 else "CONSTANT"

json.dump({"events": EVENTS}, open(os.path.join(OUT, "events.json"), "w"))
FR = arg("--frames", "")
if FR:
    for fr in [int(x) for x in FR.split(",")]:
        sc.frame_set(fr); sc.render.filepath = os.path.join(OUT, f"s_{fr:05d}.png"); bpy.ops.render.render(write_still=True)
else:
    # resumable: existing frames are skipped, so a killed render can simply be started again
    sc.render.use_overwrite = False; sc.render.filepath = os.path.join(OUT, "f_")
    RG = arg("--range", "")  # e.g. 1-900 (to split a render over two runs)
    if RG:
        sc.frame_start, sc.frame_end = [int(x) for x in RG.split("-")]
    bpy.ops.render.render(animation=True)

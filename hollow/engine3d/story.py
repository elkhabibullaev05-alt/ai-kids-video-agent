"""Hollowmere Tales 3D — story renderer (fork of Inspector Bolt engine; world in world.py) (Blender 4.2, EEVEE).

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
SET = TL.get("set", {"place": "forest"})
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

# ---------------- set + characters (world plugin) ----------------
_HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])) if "-P" in sys.argv else os.getcwd()
exec(open(os.path.join(_HERE, "world.py")).read())

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
    m = mat("p_" + p["id"], col, 0.18 if shiny else 0.45, 1.0 if shiny else 0.0, p.get("glow", 0.4 if shiny else 0))  # "glow": emission strength
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
    ang = math.atan2(v.x, -v.y) if v.length > 0.1 else 0
    face(c, t, 0.6, max(-0.6, min(0.6, ang)))  # never turn the face away from the audience


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
        loc, tgt, lens = Vector((0, -10, 4.2)), Vector((0, 8, 1.6)), 30
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
        dist = max(6, (pa - pb).length * 1.0 + 3.5); loc, tgt, lens = mid + Vector((0, -dist, 2.4)), mid + Vector((0, 0, 1.3)), 30
    else:  # close:<char>
        c = name.split(":")[1]; p = at(c, tm); L = C[c]["L"]
        rz = C[c]["root"].rotation_euler.z  # film the face: the camera follows where the character looks
        fwd, side = Vector((math.sin(rz), -math.cos(rz), 0)), Vector((math.cos(rz), math.sin(rz), 0))
        d_ = L / 2 + 4.0 + C[c]["H"] * 1.2
        loc, tgt, lens = p + fwd * d_ + side * 0.8 + Vector((0, 0, 1.2 + C[c]["H"] * 0.5)), p + fwd * (L / 2) + Vector((0, 0, C[c]["H"] * 0.55)), 35
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

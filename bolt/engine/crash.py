"""Crash Toons: cartoon cars with faces vs giant machines (own 3D scene, no game assets).

blender -b --factory-startup -P crash.py -- --out DIR --seed 7 --obstacle press --cars 6 --fps 30 --res 1080
Writes PNG frames + events.json (impact times for the sound track).
"""
import bpy, math, random, sys, json, os
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d):
    return type(d)(a[a.index(k) + 1]) if k in a else d
OUT = arg("--out", "/tmp/crash/out"); SEED = arg("--seed", 7); OBST = arg("--obstacle", "press")
NCARS = arg("--cars", 6); FPS = arg("--fps", 30); RES = arg("--res", 1080); SAMPLES = arg("--samples", 16)
LIMIT = arg("--limit", 0)
rnd = random.Random(SEED)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE_NEXT"
sc.eevee.taa_render_samples = SAMPLES
sc.render.resolution_x, sc.render.resolution_y = RES, RES * 16 // 9
sc.render.fps = FPS
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "Medium High Contrast"


def mat(name, color, rough=0.5, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = emit
    return m


def obj_add(o, m=None, smooth=True):
    if m: o.data.materials.append(m)
    if smooth and hasattr(o.data, "polygons"):
        for p in o.data.polygons: p.use_smooth = True
    return o


def key(o, frame, **kw):
    for k, v in kw.items():
        setattr(o, k, v); o.keyframe_insert(data_path=k, frame=frame)

# ---------- world, ground, road ----------
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[1].default_value = 1.0
sky = w.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "HOSEK_WILKIE"; sky.turbidity = 2.2
sky.sun_direction = (0.3, -0.5, 0.8)
w.node_tree.links.new(sky.outputs[0], bg.inputs[0])
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.01)); obj_add(bpy.context.object, mat("grass", (0.25, 0.55, 0.18), 0.9))
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0)); road = bpy.context.object
road.scale = (9, 300, 1); obj_add(road, mat("asphalt", (0.16, 0.16, 0.17), 0.8))
yl = mat("yellow", (0.95, 0.75, 0.05), 0.6)
for y in range(-140, 140, 6):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 0.005)); d = bpy.context.object; d.scale = (0.18, 2.6, 1); obj_add(d, yl)
wl = mat("white", (0.9, 0.9, 0.9), 0.6)
for x in (-4.3, 4.3):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, 0.005)); d = bpy.context.object; d.scale = (0.15, 300, 1); obj_add(d, wl)
# trees & hills for depth
tm, trunk = mat("leaf", (0.12, 0.42, 0.12), 0.9), mat("trunk", (0.35, 0.22, 0.1), 0.9)
for i in range(60):
    x = rnd.choice([-1, 1]) * rnd.uniform(14, 70); y = rnd.uniform(-20, 160)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=3, location=(x, y, 1.5)); obj_add(bpy.context.object, trunk)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=rnd.uniform(1.8, 3), subdivisions=2, location=(x, y, 4)); obj_add(bpy.context.object, tm)
bpy.ops.object.light_add(type="SUN", location=(0, 0, 50)); sun = bpy.context.object
sun.data.energy = 3.2; sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-30))

# ---------- obstacle ----------
steel = mat("steel", (0.8, 0.8, 0.82), 0.25, 1.0)
red = mat("redstripe", (0.85, 0.12, 0.08), 0.4)
press_parts = []
Y0 = 0.0  # crush point
if OBST == "press":  # two giant hydraulic drums close from the sides
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=3.2, depth=2.4, location=(side * 7.5, Y0, 3.2), rotation=(0, math.radians(90), 0))
        drum = obj_add(bpy.context.object, steel)
        for off in (-0.7, 0.7):
            bpy.ops.mesh.primitive_torus_add(major_radius=3.22, minor_radius=0.12, location=(side * 7.5 + off * side * 0.5, Y0, 3.2), rotation=(0, math.radians(90), 0))
            r = obj_add(bpy.context.object, red); r.parent = drum; r.matrix_parent_inverse = drum.matrix_world.inverted()
        press_parts.append((drum, side))
elif OBST == "hammer":  # giant hammer slams from above
    bpy.ops.mesh.primitive_cylinder_add(radius=2.6, depth=5.5, location=(0, Y0, 14), rotation=(0, math.radians(90), 0))
    head = obj_add(bpy.context.object, steel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=14, location=(0, Y0, 21)); h = obj_add(bpy.context.object, mat("handle", (0.55, 0.3, 0.12), 0.7))
    h.parent = head; h.matrix_parent_inverse = head.matrix_world.inverted()
    press_parts.append((head, 0))
else:  # "plate": hydraulic press plate from above
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, Y0, 12)); plate = obj_add(bpy.context.object, steel, False); plate.scale = (8, 6, 1)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9, depth=20, location=(0, Y0, 22)); pist = obj_add(bpy.context.object, red)
    pist.parent = plate; pist.matrix_parent_inverse = plate.matrix_world.inverted()
    press_parts.append((plate, 0))

# ---------- cars with faces ----------
PALETTE = [(0.95, 0.2, 0.15), (0.1, 0.45, 0.95), (0.98, 0.75, 0.05), (0.2, 0.75, 0.3), (0.7, 0.25, 0.85),
           (1.0, 0.45, 0.1), (0.1, 0.8, 0.85), (0.95, 0.35, 0.6)]
black, eyew, tire = mat("black", (0.02, 0.02, 0.02), 0.4), mat("eyew", (0.98, 0.98, 0.98), 0.2), mat("tire", (0.05, 0.05, 0.05), 0.9)
mouth_m = mat("mouth", (0.35, 0.03, 0.05), 0.5)
spark = mat("spark", (1.0, 0.55, 0.1), 0.4, 0.0, 6.0)
glass = mat("glass", (0.25, 0.45, 0.6), 0.05, 0.3)


def make_car(i, color, size, kind):
    root = bpy.data.objects.new(f"car{i}", None); sc.collection.objects.link(root)
    body_m = mat(f"body{i}", color, 0.25, 0.0)
    L = {"small": 3.2, "car": 4.2, "bus": 9.0, "truck": 6.5}[kind] * size
    H = {"small": 1.3, "car": 1.5, "bus": 3.0, "truck": 2.6}[kind] * size
    Wd = 2.0 * size if kind != "bus" else 2.6 * size
    parts = []
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.55 * size + H / 2)); b = obj_add(bpy.context.object, body_m)
    b.scale = (Wd, L, H); bpy.ops.object.modifier_add(type="BEVEL"); b.modifiers[-1].width = 0.25 * size; b.modifiers[-1].segments = 4
    parts.append(b)
    if kind in ("car", "small"):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.2 * L, 0.55 * size + H + 0.4 * size)); c = obj_add(bpy.context.object, glass)
        c.scale = (Wd * 0.85, L * 0.5, 0.8 * size); bpy.ops.object.modifier_add(type="BEVEL"); c.modifiers[-1].width = 0.2 * size; c.modifiers[-1].segments = 3
        parts.append(c)
    else:
        for k in range(int(L / (1.6 * size))):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -L / 2 + (k + 0.8) * 1.6 * size, 0.55 * size + H * 0.7))
            g = obj_add(bpy.context.object, glass, False); g.scale = (Wd + 0.02, 1.1 * size, 0.7 * size); parts.append(g)
    wheels = []
    for sx in (-1, 1):
        for sy in (-0.33, 0.33):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * size, depth=0.45 * size, location=(sx * Wd / 2, sy * L, 0.55 * size), rotation=(0, math.radians(90), 0))
            wh = obj_add(bpy.context.object, tire); wheels.append(wh)
    # face on the front (towards camera = -Y)
    fy = -L / 2 - 0.05 * size; fz = 0.55 * size + H * 0.62
    eyes, pupils = [], []
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * size, location=(sx * Wd * 0.24, fy, fz)); e = obj_add(bpy.context.object, eyew)
        e.scale = (1, 0.5, 1.15); eyes.append(e)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2 * size, location=(sx * Wd * 0.24, fy - 0.2 * size, fz - 0.05 * size)); p = obj_add(bpy.context.object, black)
        pupils.append(p)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * Wd * 0.24, fy - 0.05 * size, fz + 0.62 * size)); br = obj_add(bpy.context.object, black, False)
        br.scale = (0.55 * size, 0.08, 0.12 * size); br.rotation_euler = (0, sx * math.radians(-12), 0); parts.append(br)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32 * size, location=(0, fy, 0.55 * size + H * 0.22)); mo = obj_add(bpy.context.object, mouth_m)
    mo.scale = (1.3, 0.3, 0.45)
    allp = parts + wheels + eyes + pupils + [mo]
    for o in allp:
        o.parent = root
    return root, dict(L=L, H=H, W=Wd, wheels=wheels, eyes=eyes, pupils=pupils, mouth=mo, body=parts[0], size=size)


KINDS = ["small", "car", "car", "bus", "truck", "small", "car", "bus"]
cars = []
SPAN = 4.2  # seconds per car
for i in range(NCARS):
    kind = KINDS[(i + SEED) % len(KINDS)]
    size = rnd.choice([0.7, 1.0, 1.0, 1.3]) if kind in ("small", "car") else 1.0
    root, info = make_car(i, PALETTE[(i + SEED) % len(PALETTE)], size, kind)
    cars.append((root, info, kind))

events = []
f = lambda t: int(round(t * FPS)) + 1
T_END = 1.0 + NCARS * SPAN + 1.0
sc.frame_start, sc.frame_end = 1, f(T_END)
for i, (root, info, kind) in enumerate(cars):
    t0 = 0.6 + i * SPAN            # appears far away
    t_hit = t0 + 2.4               # reaches crush point
    start_y = 70
    key(root, f(t0 - 0.6), location=(0, start_y + 40, 0))
    key(root, f(t0), location=(0, start_y, 0))
    key(root, f(t_hit), location=(0, Y0, 0))
    # scared face just before impact: eyes grow, pupils shake, mouth opens
    for e in info["eyes"]:
        s0 = e.scale.copy()
        key(e, f(t_hit - 1.0), scale=s0); key(e, f(t_hit - 0.4), scale=(s0[0] * 1.45, s0[1], s0[2] * 1.5))
    m = info["mouth"]; ms = m.scale.copy()
    key(m, f(t_hit - 0.9), scale=ms); key(m, f(t_hit - 0.35), scale=(ms[0] * 0.8, ms[1], ms[2] * 2.4))
    # crush: squash (sides -> X, top -> Z), pancake, pop wheels, then slide away
    b = info["body"]
    sq = (0.22, 1.12, 1.0) if OBST == "press" else (1.25, 1.12, 0.18)
    key(root, f(t_hit), scale=(1, 1, 1)); key(root, f(t_hit + 0.12), scale=sq)
    key(root, f(t_hit + 0.9), scale=sq)
    key(root, f(t_hit + 0.9), location=(0, Y0, 0)); key(root, f(t_hit + 1.5), location=(0, -30, 0))
    for k, wh in enumerate(info["wheels"]):
        p0 = wh.location.copy()
        key(wh, f(t_hit + 0.05), location=p0)
        out = Vector((p0[0] * 3 + rnd.uniform(-2, 2), p0[1] + rnd.uniform(-3, 3), p0[2] + rnd.uniform(4, 7)))
        key(wh, f(t_hit + 0.45), location=out)
        key(wh, f(t_hit + 0.9), location=(out[0] * 1.6, out[1], 0.3))
    events.append({"t": t_hit, "kind": kind, "x": 0.0})
    for k in range(14):
        m_ = spark if k % 2 else info["body"].data.materials[0]
        bpy.ops.mesh.primitive_cube_add(size=0.25 * info["size"], location=(0, Y0, 1.0)); sp = obj_add(bpy.context.object, m_, False)
        sp.scale = (0.001, 0.001, 0.001); sp.keyframe_insert("scale", frame=f(t_hit + 0.04))
        sp.scale = (1, 1, 1); sp.keyframe_insert("scale", frame=f(t_hit + 0.06))
        sp.location = (0, Y0, 1.0); sp.keyframe_insert("location", frame=f(t_hit + 0.06))
        tx, ty = rnd.uniform(-5, 5), rnd.uniform(-7, 3)
        sp.location = (tx * 0.6, Y0 + ty * 0.6, rnd.uniform(3, 6)); sp.keyframe_insert("location", frame=f(t_hit + 0.35))
        sp.location = (tx, Y0 + ty, 0.15); sp.keyframe_insert("location", frame=f(t_hit + 0.75))
        sp.rotation_euler = (0, 0, 0); sp.keyframe_insert("rotation_euler", frame=f(t_hit + 0.06))
        sp.rotation_euler = (rnd.uniform(0, 9), rnd.uniform(0, 9), 0); sp.keyframe_insert("rotation_euler", frame=f(t_hit + 0.75))
        sp.scale = (1, 1, 1); sp.keyframe_insert("scale", frame=f(t_hit + 1.3))
        sp.scale = (0.001, 0.001, 0.001); sp.keyframe_insert("scale", frame=f(t_hit + 1.45))
    # obstacle motion
    for obj, side in press_parts:
        if OBST == "press":
            key(obj, f(t_hit - 0.35), location=(side * 7.5, Y0, 3.2))
            key(obj, f(t_hit + 0.05), location=(side * (info["W"] * 0.22 + 1.6), Y0, 3.2))
            key(obj, f(t_hit + 0.8), location=(side * (info["W"] * 0.22 + 1.6), Y0, 3.2))
            key(obj, f(t_hit + 1.4), location=(side * 7.5, Y0, 3.2))
        else:
            top = 14 if OBST == "hammer" else 12
            low = info["H"] * 0.2 + (2.6 if OBST == "hammer" else 0.6)
            key(obj, f(t_hit - 0.3), location=(0, Y0, top)); key(obj, f(t_hit + 0.05), location=(0, Y0, low))
            key(obj, f(t_hit + 0.8), location=(0, Y0, low)); key(obj, f(t_hit + 1.4), location=(0, Y0, top))
    # hide after it leaves
    key(root, f(t_hit + 1.6), scale=sq); key(root, f(t_hit + 1.65), scale=(0.001, 0.001, 0.001))
    if f(t0 - 0.7) > 1:
        root.scale = (0.001, 0.001, 0.001); root.keyframe_insert("scale", frame=f(t0 - 0.7))
    root.scale = (1, 1, 1); root.keyframe_insert("scale", frame=f(t0 - 0.6))

for a_ in bpy.data.actions:  # snappy, cartoon timing
    for fc in a_.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"

# ---------- camera (low, behind obstacle, looking at incoming cars) with shake on impacts ----------
CAM = (0, -12.5, 4.6)
bpy.ops.object.camera_add(location=CAM, rotation=(math.radians(73), 0, 0))
cam = bpy.context.object; cam.data.lens = 21; sc.camera = cam
for e in events:
    for dt, dx in ((0, 0), (0.04, 0.35), (0.08, -0.3), (0.12, 0.2), (0.18, -0.1), (0.26, 0)):
        key(cam, f(e["t"] + dt), location=(CAM[0] + dx, CAM[1], CAM[2] + dx * 0.5))

json.dump({"fps": FPS, "frames": sc.frame_end, "events": events, "duration": T_END}, open(os.path.join(OUT, "events.json"), "w"))
sc.render.filepath = os.path.join(OUT, "f_")
FR = arg("--frames", "")
if FR:
    for fr in [int(x) for x in FR.split(",")]:
        sc.frame_set(fr); sc.render.filepath = os.path.join(OUT, f"s_{fr:04d}.png")
        bpy.ops.render.render(write_still=True)
else:
    if LIMIT:
        sc.frame_end = min(sc.frame_end, LIMIT)
    bpy.ops.render.render(animation=True)

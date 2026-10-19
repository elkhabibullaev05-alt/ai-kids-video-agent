"""Max the Curious Cat 3D world: bright, cosy kids cartoon.
Executed inside story.py (exec). Defines TOD, PODIUM_TOP, DRUMS, C, make_char(), hat_m and builds the set.
SET.place: house (living room) | garden | park | beach | snow ; SET.time: day | sunset
Character kinds: cat | mouse | grandma | dog | bird
"""
TOD = SET.get("time", "day")
PLACE = SET.get("place", "garden")
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[1].default_value = 0.25 if PLACE == "house" else 1.0
sky = w.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "HOSEK_WILKIE"; sky.turbidity = 2.5
sky.sun_direction = (0.3, -0.4, 0.85) if TOD == "day" else (0.6, 0.5, 0.2)
w.node_tree.links.new(sky.outputs[0], bg.inputs[0])

ground = {"garden": (0.25, 0.6, 0.2), "park": (0.3, 0.65, 0.25), "beach": (0.95, 0.85, 0.6), "snow": (0.95, 0.97, 1.0), "house": (0.75, 0.55, 0.35)}[PLACE]
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 10, 0)); g = add(bpy.context.object, mat("ground", ground, 0.85)); g.scale = (160, 120, 1)
if PLACE == "house":
    for (loc, sca, col) in [((0, 18, 7), (40, 0.4, 14), (0.95, 0.85, 0.65)), ((-20, 6, 7), (0.4, 30, 14), (0.9, 0.8, 0.62))]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc); wl = add(bpy.context.object, mat("wall", col, 0.9), False); wl.scale = sca
    bpy.ops.mesh.primitive_cylinder_add(radius=5, depth=0.05, location=(0, 7, 0.03)); add(bpy.context.object, mat("rug", (0.8, 0.2, 0.25), 0.9))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-8, 15, 1.4)); so = add(bpy.context.object, mat("sofa", (0.25, 0.45, 0.75), 0.8), False); so.scale = (8, 3, 2.8)
    bpy.ops.object.modifier_add(type="BEVEL"); so.modifiers[-1].width = 0.4; so.modifiers[-1].segments = 3
    bpy.ops.mesh.primitive_plane_add(size=1, location=(6, 17.7, 8), rotation=(1.5708, 0, 0)); add(bpy.context.object, mat("winsky", (0.6, 0.85, 1.0), 0.3, 0, 1.5), False).scale = (7, 5, 1)
    bpy.ops.object.light_add(type="AREA", location=(6, 12, 9)); a_ = bpy.context.object; a_.data.energy = 600; a_.data.size = 8
else:
    leaf = [(0.2, 0.55, 0.15), (0.3, 0.65, 0.2), (0.15, 0.45, 0.12)] if PLACE != "snow" else [(0.9, 0.95, 1.0)]
    for i in range(16):
        x = rnd.uniform(-35, 35); y = rnd.uniform(18, 45)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4, location=(x, y, 2)); add(bpy.context.object, mat("trunk", (0.4, 0.25, 0.12), 0.9))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rnd.uniform(2.5, 4), location=(x, y, 5.5)); add(bpy.context.object, mat(f"leaf{i%3}", rnd.choice(leaf), 0.8))
    if PLACE in ("garden", "park"):
        fl = [(1, 0.3, 0.4), (1, 0.85, 0.2), (0.6, 0.4, 1)]
        for i in range(40):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(rnd.uniform(-14, 14), rnd.uniform(4, 16), 0.25)); add(bpy.context.object, mat(f"fl{i%3}", fl[i % 3], 0.6))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(10, 20, 3)); hs = add(bpy.context.object, mat("house", (1, 0.8, 0.55), 0.9), False); hs.scale = (10, 7, 6)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=7.5, depth=4, location=(10, 20, 8), rotation=(0, 0, 0.785)); add(bpy.context.object, mat("roof", (0.85, 0.25, 0.2), 0.8), False)
    if PLACE == "beach":
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 40, 0.05)); sea = add(bpy.context.object, mat("sea", (0.1, 0.45, 0.8), 0.1, 0.2)); sea.scale = (200, 40, 1)
bpy.ops.object.light_add(type="SUN", location=(0, 0, 40)); sun = bpy.context.object
sun.data.energy = (1.2 if PLACE == "house" else 4.0) if TOD == "day" else 3.0; sun.data.color = (1, 0.95, 0.85) if TOD == "day" else (1, 0.75, 0.5)
sun.rotation_euler = (math.radians(50), 0, math.radians(-30))
bpy.ops.object.light_add(type="AREA", location=(0, -18, 10)); fill = bpy.context.object
fill.data.energy = 900 if PLACE == "house" else 2500; fill.data.size = 20
fill.rotation_euler = (Vector((0, 6, 1)) - fill.location).to_track_quat("-Z", "Y").to_euler()

PODIUM_TOP = Vector((0, 12, 0.5))
DRUMS = []

black, eyew = mat("black", (0.02, 0.02, 0.02), 0.4), mat("eyew", (0.98, 0.98, 0.98), 0.2)
mouth_m = mat("mouth", (0.45, 0.08, 0.1), 0.5)
hat_m = mat("hat", (0.25, 0.18, 0.1), 0.7)
C = {}


def _o():
    return bpy.context.object


def _shape(key, kind, s, ch):
    col = tuple(ch.get("color", (1, 0.55, 0.15)))
    fur = mat(f"fur_{key}", col, 0.7)
    if kind == "cat":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0.2 * s, 1.0 * s)); o = add(_o(), fur); o.scale = (0.9, 1.1, 0.85)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.85 * s, location=(0, -0.5 * s, 2.2 * s)); hd = add(_o(), fur); parent(hd, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(radius1=0.32 * s, depth=0.6 * s, location=(sx * 0.48 * s, -0.4 * s, 3.0 * s), rotation=(0, sx * -0.3, 0)); parent(add(_o(), fur), o)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25 * s, location=(sx * 0.45 * s, -0.6 * s, 0.2 * s)); ft = add(_o(), fur); ft.scale = (1, 1.4, 0.6); parent(ft, o)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.6 * s, minor_radius=0.15 * s, location=(0, -0.4 * s, 1.55 * s)); parent(add(_o(), mat("scarf", (0.85, 0.08, 0.1), 0.7)), o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12 * s, depth=1.8 * s, location=(0.3 * s, 1.3 * s, 1.6 * s), rotation=(0.6, 0.3, 0)); parent(add(_o(), fur), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1 * s, location=(0, -1.33 * s, 2.15 * s)); parent(add(_o(), mat("nose", (1, 0.45, 0.55), 0.4)), o)
        return o, 2.0 * s, 2.2 * s, 3.2 * s, -1.25 * s, 2.45 * s
    if kind == "mouse":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5 * s, location=(0, 0, 0.55 * s)); o = add(_o(), fur); o.scale = (0.8, 1.2, 0.9)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25 * s, location=(sx * 0.32 * s, -0.25 * s, 1.0 * s)); ear = add(_o(), mat("ear", (1, 0.7, 0.75), 0.6)); ear.scale = (1, 0.3, 1); parent(ear, o)
        return o, 1.0 * s, 1.2 * s, 1.2 * s, -0.55 * s, 0.7 * s
    if kind == "dog":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0.5 * s, 1.3 * s)); o = add(_o(), fur); o.scale = (0.9, 1.5, 0.85)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8 * s, location=(0, -0.9 * s, 2.3 * s)); parent(add(_o(), fur), o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35 * s, location=(sx * 0.75 * s, -0.8 * s, 2.3 * s)); er = add(_o(), mat(f"dear_{key}", tuple(c * 0.6 for c in col), 0.7)); er.scale = (0.4, 0.6, 1.3); parent(er, o)
            for fy in (-0.3, 1.2):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * s, depth=0.8 * s, location=(sx * 0.5 * s, fy * s, 0.4 * s)); parent(add(_o(), fur), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18 * s, location=(0, -1.65 * s, 2.15 * s)); parent(add(_o(), black), o)
        return o, 1.8 * s, 3.0 * s, 3.1 * s, -1.55 * s, 2.5 * s
    if kind == "bird":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45 * s, location=(0, 0, 2.6 * s)); o = add(_o(), fur)
        bpy.ops.mesh.primitive_cone_add(radius1=0.12 * s, depth=0.35 * s, location=(0, -0.5 * s, 2.6 * s), rotation=(1.5708, 0, 0)); parent(add(_o(), mat("beak", (1, 0.6, 0.1), 0.5)), o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35 * s, location=(sx * 0.45 * s, 0.05, 2.6 * s)); wg = add(_o(), fur); wg.scale = (0.4, 0.9, 0.6); parent(wg, o)
        return o, 0.9 * s, 0.9 * s, 3.1 * s, -0.42 * s, 2.75 * s
    # grandma
    dress = mat(f"dress_{key}", col, 0.8)
    bpy.ops.mesh.primitive_cone_add(radius1=1.1 * s, radius2=0.55 * s, depth=2.6 * s, location=(0, 0, 1.3 * s)); o = add(_o(), dress)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6 * s, location=(0, 0, 3.1 * s)); parent(add(_o(), mat("skin", (0.95, 0.78, 0.66), 0.6)), o)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62 * s, location=(0, 0.2 * s, 3.35 * s)); hr = add(_o(), mat("hair", (0.9, 0.9, 0.92), 0.8)); hr.scale = (1, 1, 0.7); parent(hr, o)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3 * s, location=(0, 0.6 * s, 3.8 * s)); parent(add(_o(), mat("hair", (0.9, 0.9, 0.92), 0.8)), o)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.15 * s, minor_radius=0.025 * s, location=(sx * 0.2 * s, -0.58 * s, 3.15 * s), rotation=(1.5708, 0, 0)); parent(add(_o(), black), o)
    return o, 2.2 * s, 2.2 * s, 3.9 * s, -0.58 * s, 3.15 * s


def make_char(key, ch):
    s, kind = ch.get("size", 1.0), ch.get("kind", "cat")
    root = bpy.data.objects.new(key, None); sc.collection.objects.link(root)
    body = bpy.data.objects.new(key + "_body", None); sc.collection.objects.link(body); body.parent = root
    o, Wd, L, H, fy, fz = _shape(key, kind, s, ch)
    o.parent = body
    eyes = []
    sep = {"mouse": 0.17, "bird": 0.13, "grandma": 0.2}.get(kind, 0.3) * s
    big = {"mouse": 0.13, "bird": 0.1, "grandma": 0.09}.get(kind, 0.24) * s
    for sx in (-sep, sep):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=big, location=(sx, fy - 0.02, fz)); e = add(_o(), eyew); e.scale = (1, 0.55, 1.15); e.parent = body; eyes.append(e)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=big * 0.55, location=(sx, fy - big * 0.5, fz - big * 0.1)); parent(add(_o(), black), e)
    mz = fz - {"mouse": 0.18, "bird": 0.2}.get(kind, 0.42) * s
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16 * s, location=(0, fy + 0.02, mz)); mo = add(_o(), mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    hat = bpy.data.objects.new(key + "_hat", None); sc.collection.objects.link(hat); hat.parent = body; hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=s,
                  home=Vector((hx, hy, 0)), top=H, has_hat=False)

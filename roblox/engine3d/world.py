"""Blocky Quest 3D world: original blocky-avatar game worlds (obby / tycoon / lava / city / lobby / tower).
Executed inside story.py (exec). Defines TOD, PODIUM_TOP, DRUMS, C, make_char(), hat_m and builds the set.
SET.place: obby | tycoon | lava | city | lobby | tower ; SET.time: day | night
Character kinds: blocky | zombie | robot | boss | pet
Own designs only: no Roblox logo, no official avatar/items, no real game maps.
blocky options in the cast entry: color = shirt, "pants", "skin", "hair" (cap | spiky | crown | helmet | bun | none), "hair_color".
"""
TOD = SET.get("time", "day")
PLACE = SET.get("place", "obby")
NIGHT = TOD == "night"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[1].default_value = 0.5 if NIGHT else 1.0
sky = w.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "HOSEK_WILKIE"; sky.turbidity = 2.2
sky.sun_direction = (0.3, -0.4, 0.85) if not NIGHT else (0.5, 0.5, 0.05)
w.node_tree.links.new(sky.outputs[0], bg.inputs[0])


def checker(name, c1, c2, scale=40.0, rough=0.7):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    ck = nt.nodes.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = scale
    ck.inputs["Color1"].default_value = (*c1, 1); ck.inputs["Color2"].default_value = (*c2, 1)
    nt.links.new(ck.outputs["Color"], b.inputs["Base Color"])
    return m


def block(loc, size, m, bevel=0.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = add(bpy.context.object, m, False); o.scale = size
    if bevel:
        bpy.ops.object.modifier_add(type="BEVEL"); o.modifiers[-1].width = bevel; o.modifiers[-1].segments = 2
    return o


NEON = [(1, 0.15, 0.2), (0.1, 0.55, 1), (0.15, 0.85, 0.3), (1, 0.8, 0.1), (0.75, 0.25, 1), (1, 0.45, 0.1)]
NM = [mat(f"neon{i}", c, 0.35) for i, c in enumerate(NEON)]
lava_m = mat("lava", (0.95, 0.22, 0.02), 0.4, 0, 1.1)
glow = lambda n, c, e=3.0: mat(n, c, 0.3, 0, e)
base_green = ((0.22, 0.55, 0.2), (0.25, 0.6, 0.23))
base_gray = ((0.45, 0.47, 0.5), (0.5, 0.52, 0.55))

if PLACE in ("obby", "lava", "tower"):
    # main start platform the cast stands on, lava or void below, floating parkour in the back
    block((0, 7, -1), (34, 18, 2), checker("plat", *(base_gray if PLACE != "obby" else ((0.85, 0.85, 0.88), (0.78, 0.78, 0.82))), 30), 0.1)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 30, -3 if PLACE != "lava" else -1.2)); lv = add(bpy.context.object, lava_m); lv.scale = (260, 140, 1)
    for i in range(18):
        x = rnd.uniform(-30, 30); y = rnd.uniform(20, 60); z = rnd.uniform(-1, 9) + (y - 20) * 0.15
        sz = rnd.choice([(3, 3, 0.8), (4, 2, 0.8), (2, 2, 0.8), (6, 1.5, 0.8)])
        block((x, y, z), sz, NM[i % len(NM)])
        if i % 5 == 0:  # red kill-brick strip
            block((x, y, z + 0.5), (sz[0] * 0.6, 0.4, 0.2), glow("kill", (1, 0.05, 0.05), 2.0), 0.02)
    for x in (-13, 13):  # checkpoint flags on the start platform
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=5, location=(x, 14, 2.5)); add(bpy.context.object, mat("pole", (0.9, 0.9, 0.9), 0.3, 0.8))
        block((x + 0.9, 14, 4.4), (1.8, 0.08, 1.1), glow("flag", (0.1, 0.9, 0.3), 0.8), 0.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=2.2, depth=0.25, location=(0, 13, 0.13)); add(bpy.context.object, glow("pad", (0.2, 0.6, 1.0), 1.2))
    if PLACE == "tower":
        for k in range(14):  # tall neon tower of sections in the background
            block((0, 46, 3 + k * 4.2), (10 - k * 0.25, 10 - k * 0.25, 4), NM[k % len(NM)], 0.15)
    if PLACE == "lava":
        for x, y, h in ((-18, 22, 9), (17, 25, 12), (-6, 32, 15), (9, 38, 18)):
            block((x, y, h / 2 - 1), (3, 3, h), mat("rock", (0.25, 0.22, 0.22), 0.9))
elif PLACE == "tycoon":
    block((0, 15, -0.5), (70, 50, 1), checker("base", *base_green, 50), 0)
    block((0, 22, 3.2), (26, 0.6, 6.4), mat("wall", (0.92, 0.9, 0.85), 0.8))  # back wall
    for x in (-9, 0, 9):  # droppers: tower + chute + glowing ore cube
        block((x, 19, 3), (2.4, 2.4, 6), NM[(x // 9 + 1) % len(NM)])
        block((x, 17, 5.2), (1.2, 2.4, 1.2), mat("chute", (0.3, 0.3, 0.35), 0.4, 0.6))
        block((x, 16.4, 2.4), (0.6, 0.6, 0.6), glow(f"ore{x}", (1, 0.85, 0.2), 1.5), 0.04)
    block((0, 15.5, 0.6), (30, 2.4, 0.6), mat("belt", (0.12, 0.12, 0.14), 0.6), 0.05)  # conveyor
    for i in range(10):
        block((-13 + i * 2.9, 15.5, 1.15), (0.5, 0.5, 0.5), glow(f"cube{i%3}", NEON[i % 3], 0.8), 0.03)
    for i, (x, col) in enumerate(((-14, (0.1, 0.9, 0.3)), (-10, (0.1, 0.9, 0.3)), (14, (1, 0.2, 0.2)))):  # buy pads
        bpy.ops.mesh.primitive_cylinder_add(radius=1.3, depth=0.2, location=(x, 9, 0.1)); add(bpy.context.object, glow(f"buy{i}", col, 1.2))
    block((15, 19, 4), (6, 1, 3), glow("cash", (0.2, 1, 0.4), 0.6))  # money board
    for i in range(12):  # fence
        block((-30 + i * 5.5, 30, 1), (0.4, 0.4, 2), mat("fence", (0.95, 0.95, 0.95), 0.6))
elif PLACE == "city":
    block((0, 15, -0.5), (90, 60, 1), checker("pave", *base_gray, 40), 0)
    block((0, 4, 0.02), (90, 7, 0.06), mat("road", (0.12, 0.12, 0.13), 0.8), 0)
    for i in range(9):
        block((-36 + i * 9, 3.9, 0.07), (3, 0.3, 0.02), mat("line", (1, 0.9, 0.2), 0.5), 0)
    win = glow("win", (1, 0.9, 0.55), 2.0 if NIGHT else 0.15)
    for i in range(8):
        x = -35 + i * 10; h = rnd.choice([10, 14, 18, 24]); col = rnd.choice([(0.85, 0.35, 0.3), (0.3, 0.45, 0.8), (0.9, 0.8, 0.6), (0.4, 0.7, 0.5)])
        block((x, 26, h / 2), (8, 8, h), mat(f"bld{i}", col, 0.8), 0.1)
        for r_ in range(int(h // 3.5)):
            for cx in (-2, 0, 2):
                block((x + cx, 21.95, 2 + r_ * 3.4), (1.1, 0.1, 1.4), win, 0)
    for x in (-12, 12):  # street lamps
        bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=6, location=(x, 9, 3)); add(bpy.context.object, mat("lamp", (0.2, 0.2, 0.22), 0.4, 0.7))
        block((x, 9, 6.2), (0.8, 0.8, 0.4), glow("bulb", (1, 0.95, 0.7), 4.0 if NIGHT else 0.5), 0.05)
else:  # lobby: baseplate, spawn pad, portals to other worlds
    block((0, 15, -0.5), (80, 60, 1), checker("lob", *base_gray, 50), 0)
    bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=0.3, location=(0, 8, 0.15)); add(bpy.context.object, glow("spawn", (0.2, 0.6, 1), 1.0))
    for i, x in enumerate((-16, -6, 6, 16)):  # portal arches
        m = NM[i]
        block((x - 2.2, 22, 3.5), (0.8, 0.8, 7), m); block((x + 2.2, 22, 3.5), (0.8, 0.8, 7), m); block((x, 22, 7.2), (5.2, 0.8, 0.8), m)
        block((x, 22, 3.4), (3.6, 0.1, 6.6), glow(f"portal{i}", NEON[i], 1.5), 0)
for i in range(6):  # blocky clouds
    x, y, z = rnd.uniform(-60, 60), rnd.uniform(70, 110), rnd.uniform(25, 40)
    block((x, y, z), (rnd.uniform(8, 16), 4, 2.5), mat("cloud", (1, 1, 1) if not NIGHT else (0.35, 0.38, 0.5), 0.9), 0.3)

bpy.ops.object.light_add(type="SUN", location=(0, 0, 40)); sun = bpy.context.object
sun.data.energy = 4.0 if not NIGHT else 1.2; sun.data.color = (1, 0.96, 0.88) if not NIGHT else (0.6, 0.7, 1.0)
sun.rotation_euler = (math.radians(50), 0, math.radians(-30))
bpy.ops.object.light_add(type="AREA", location=(0, -18, 10)); fill = bpy.context.object
fill.data.energy = 2500 if not NIGHT else 2300; fill.data.size = 20
fill.rotation_euler = (Vector((0, 6, 1)) - fill.location).to_track_quat("-Z", "Y").to_euler()

PODIUM_TOP = Vector((0, 12, 0.5))
DRUMS = []

black, eyew = mat("black", (0.02, 0.02, 0.02), 0.3), mat("eyew", (0.98, 0.98, 0.98), 0.2)
mouth_m = mat("mouth", (0.08, 0.05, 0.05), 0.5)
hat_m = mat("hat", (0.95, 0.75, 0.1), 0.3, 0.8)
C = {}
SKIN = (1.0, 0.8, 0.62)


def _o():
    return bpy.context.object


def _b(loc, size, m, par, bevel=0.05):
    o = block(loc, size, m, bevel)
    if par is not None:
        parent(o, par)
    return o


def _hair(style, s, hc, par):
    hm = mat(f"hair_{id(par)}", hc, 0.6)
    top = 5.3 * s
    if style == "cap":
        _b((0, 0, top), (1.3 * s, 1.3 * s, 0.35 * s), hm, par); _b((0, -0.85 * s, top - 0.1 * s), (1.2 * s, 0.6 * s, 0.12 * s), hm, par)
    elif style == "spiky":
        for k, (x, y) in enumerate(((-0.35, -0.2), (0.35, -0.2), (0, 0.3), (-0.4, 0.4), (0.4, 0.4))):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.38 * s, depth=0.8 * s, location=(x * s, y * s, top + 0.25 * s)); parent(add(_o(), hm, False), par)
        _b((0, 0.1 * s, top - 0.1 * s), (1.32 * s, 1.15 * s, 0.25 * s), hm, par)
    elif style == "crown":
        cm = mat("crown", (1, 0.78, 0.15), 0.2, 1.0, 0.3)
        _b((0, 0, top), (1.1 * s, 1.1 * s, 0.3 * s), cm, par)
        for x in (-0.45, 0, 0.45):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.2 * s, depth=0.5 * s, location=(x * s, -0.45 * s, top + 0.38 * s)); parent(add(_o(), cm, False), par)
    elif style == "helmet":
        _b((0, 0, top - 0.05 * s), (1.35 * s, 1.35 * s, 0.45 * s), hm, par)
    elif style == "bun":
        _b((0, 0.05 * s, top - 0.05 * s), (1.32 * s, 1.3 * s, 0.3 * s), hm, par); _b((0, 0.35 * s, top + 0.3 * s), (0.6 * s, 0.6 * s, 0.5 * s), hm, par)


def _shape(key, kind, s, ch):
    col = tuple(ch.get("color", (0.2, 0.5, 1.0)))
    if kind == "pet":  # blocky dog/cat pet
        fur = mat(f"fur_{key}", col, 0.8)
        o = block((0, 0.4 * s, 1.0 * s), (1.0 * s, 2.0 * s, 0.9 * s), fur)
        _b((0, -0.9 * s, 1.7 * s), (1.0 * s, 0.9 * s, 0.9 * s), fur, o)
        for sx in (-1, 1):
            _b((sx * 0.32 * s, -0.9 * s, 2.3 * s), (0.25 * s, 0.25 * s, 0.4 * s), fur, o)
            for fy in (-0.3, 1.1):
                _b((sx * 0.35 * s, fy * s, 0.3 * s), (0.3 * s, 0.3 * s, 0.6 * s), fur, o)
        _b((0, 1.5 * s, 1.5 * s), (0.2 * s, 0.8 * s, 0.2 * s), fur, o)
        _b((0, -1.38 * s, 1.55 * s), (0.25 * s, 0.1 * s, 0.18 * s), black, o, 0.02)
        return o, 1.2 * s, 2.6 * s, 2.5 * s, -1.36 * s, 1.85 * s
    robot = kind == "robot"
    skin = (0.35, 0.75, 0.3) if kind == "zombie" else (0.62, 0.65, 0.7) if robot else (0.85, 0.15, 0.2) if kind == "boss" else tuple(ch.get("skin", SKIN))
    sk = mat(f"skin_{key}", skin, 0.3 if robot else 0.6, 0.8 if robot else 0.0)
    sh = mat(f"shirt_{key}", col, 0.7, 0.6 if robot else 0.0)
    pa = mat(f"pants_{key}", tuple(ch.get("pants", (0.15, 0.18, 0.3))), 0.75)
    o = _b((0, 0, 3.0 * s), (2.0 * s, 1.0 * s, 2.0 * s), sh, None)  # torso
    for sx in (-1, 1):
        _b((sx * 0.5 * s, 0, 1.0 * s), (0.95 * s, 0.95 * s, 2.0 * s), pa, o)   # legs
        arm = _b((sx * 1.5 * s, 0, 3.0 * s), (0.95 * s, 0.95 * s, 2.0 * s), sk if kind in ("zombie", "robot") else sh, o)
        arm.rotation_euler = (math.radians(-80 if kind == "zombie" else 0), 0, 0)
        if kind == "zombie":
            arm.location = (sx * 1.5 * s, -0.9 * s, 3.6 * s)
        _b((sx * 1.5 * s, (-1.85 if kind == "zombie" else 0) * s, (3.6 if kind == "zombie" else 1.75) * s), (0.8 * s, 0.8 * s, 0.5 * s), sk, o)  # hands
    _b((0, 0, 4.65 * s), (1.25 * s, 1.25 * s, 1.25 * s), sk, o, 0.12)  # head
    if robot:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=0.8 * s, location=(0, 0, 5.6 * s)); parent(add(_o(), sk), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15 * s, location=(0, 0, 6.05 * s)); parent(add(_o(), glow("tip", (1, 0.2, 0.2), 4)), o)
        _b((0, -0.51 * s, 3.2 * s), (0.9 * s, 0.05 * s, 0.6 * s), glow(f"chest_{key}", (0.2, 0.9, 1), 2.0), o, 0.02)
    elif kind == "boss":
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.25 * s, depth=0.9 * s, location=(sx * 0.5 * s, 0, 5.6 * s), rotation=(0, sx * -0.4, 0)); parent(add(_o(), mat("horn", (0.15, 0.1, 0.1), 0.5), False), o)
    else:
        _hair(ch.get("hair", "cap" if kind == "blocky" else "none"), s, tuple(ch.get("hair_color", (0.25, 0.15, 0.08))), o)
    return o, 4.0 * s, 1.3 * s, 5.4 * s, -0.64 * s, 4.85 * s


def make_char(key, ch):
    s, kind = ch.get("size", 0.8), ch.get("kind", "blocky")
    root = bpy.data.objects.new(key, None); sc.collection.objects.link(root)
    body = bpy.data.objects.new(key + "_body", None); sc.collection.objects.link(body); body.parent = root
    o, Wd, L, H, fy, fz = _shape(key, kind, s, ch)
    o.parent = body
    eyes = []
    pet = kind == "pet"
    sep, big = (0.24 if pet else 0.27) * s, (0.1 if pet else 0.12) * s
    em = glow(f"eye_{key}", (1, 0.15, 0.1) if kind == "boss" else (0.3, 1, 1), 3.0) if kind in ("robot", "boss") else black
    for sx in (-sep, sep):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=big, location=(sx, fy, fz)); e = add(_o(), em); e.scale = (1, 0.5, 1.15); e.parent = body; eyes.append(e)
        if em is black:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=big * 0.35, location=(sx + big * 0.3, fy - big * 0.35, fz + big * 0.4)); parent(add(_o(), eyew), e)
    mz = fz - (0.3 if pet else 0.45) * s
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16 * s, location=(0, fy + 0.02, mz)); mo = add(_o(), mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    hat = bpy.data.objects.new(key + "_hat", None); sc.collection.objects.link(hat); hat.parent = body; hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=s,
                  home=Vector((hx, hy, 0)), top=H, has_hat=False)

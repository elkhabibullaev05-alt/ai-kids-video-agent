"""Hollowmere Tales 3D world: night forest places + lantern-bearers + creatures.
Executed inside story.py (exec). Defines TOD, PODIUM_TOP, DRUMS, C, make_char(), hat_m and builds the set.
SET.place: forest | clearing | graveyard | swamp | village | chapel
Character kinds: odo | moth | narr(none) | gloamhound | rootwraith | shepherd | crow | wickeater | hollowmother | horseman | soldier (+ghost) | human
"""
TOD = "night"
PLACE = SET.get("place", "forest")
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.07, 0.12, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
# light fog: world volume scatter (cheap density)
vol = w.node_tree.nodes.new("ShaderNodeVolumePrincipled"); vol.inputs["Density"].default_value = SET.get("fog", 0.02)
vol.inputs["Color"].default_value = (0.55, 0.6, 0.75, 1)
w.node_tree.links.new(vol.outputs[0], w.node_tree.nodes["World Output"].inputs["Volume"])
try:
    sc.eevee.volumetric_end = 60; sc.eevee.volumetric_tile_size = "16"
except Exception:
    pass

ground_col = {"swamp": (0.04, 0.06, 0.04), "graveyard": (0.07, 0.07, 0.06), "village": (0.08, 0.07, 0.06)}.get(PLACE, (0.05, 0.045, 0.035))
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 10, 0)); g = add(bpy.context.object, mat("ground", ground_col, 0.95)); g.scale = (160, 120, 1)
bark = mat("bark", (0.03, 0.025, 0.02), 0.9)
stone_m = mat("stone", (0.25, 0.25, 0.27), 0.8)


def tree(x, y, h, lean=0.0):
    bpy.ops.mesh.primitive_cone_add(radius1=0.55 + h * 0.03, radius2=0.12, depth=h, location=(x, y, h / 2), rotation=(lean, rnd.uniform(-0.15, 0.15), 0)); t = add(bpy.context.object, bark)
    for k in range(rnd.randint(2, 4)):
        z = h * rnd.uniform(0.45, 0.85); ang = rnd.uniform(0, 6.28); L = rnd.uniform(2, 4)
        bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.03, depth=L, location=(x + math.cos(ang) * L * 0.35, y + math.sin(ang) * L * 0.35, z + L * 0.25),
                                        rotation=(math.sin(ang) * -0.9, math.cos(ang) * 0.9, 0)); add(bpy.context.object, bark)


if PLACE in ("forest", "clearing", "swamp"):
    for i in range(70):
        x = rnd.uniform(-45, 45); y = rnd.uniform(6, 60)
        if PLACE == "clearing" and math.hypot(x, y - 12) < 9:
            continue
        if abs(x) < 4 and y < 14:
            continue
        tree(x, y, rnd.uniform(9, 18), rnd.uniform(-0.12, 0.12))
if PLACE == "clearing":
    for i in range(9):
        an = i / 9 * 6.28
        if math.sin(an) < -0.6:  # leave the front of the ring open for the camera
            continue
        bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(an) * 8, 14 + math.sin(an) * 8, 1.6)); s_ = add(bpy.context.object, stone_m, False); s_.scale = (0.9, 0.7, 3.2)
    bpy.ops.mesh.primitive_cone_add(radius1=0.45, depth=0.8, location=(0, 14, 0.4)); add(bpy.context.object, mat("fire", (1, 0.45, 0.08), 0.5, 0, 10))
    for k in range(5):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=1.4, location=(0, 14, 0.12), rotation=(1.5708, 0, k * 0.63)); add(bpy.context.object, bark)
    bpy.ops.object.light_add(type="POINT", location=(0, 14, 1.4)); f = bpy.context.object; f.data.energy = 2500; f.data.color = (1, 0.5, 0.15)
if PLACE == "graveyard":
    for i in range(26):
        x = rnd.uniform(-14, 14); y = rnd.uniform(6, 26)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.8)); gs = add(bpy.context.object, stone_m, False); gs.scale = (0.9, 0.2, 1.6); gs.rotation_euler = (rnd.uniform(-0.15, 0.15), rnd.uniform(-0.1, 0.1), rnd.uniform(-0.2, 0.2))
    for i in range(20):
        tree(rnd.uniform(-40, 40), rnd.uniform(28, 60), rnd.uniform(9, 16))
if PLACE in ("village", "chapel"):
    wm = mat("winlit", (1, 0.6, 0.2), 0.4, 0, 6)
    for i in range(6):
        x = -18 + i * 7.5; y = 24 + rnd.uniform(-2, 2); h = rnd.uniform(5, 8)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, h / 2)); hs = add(bpy.context.object, mat(f"hw{i}", (0.12, 0.1, 0.09), 0.9), False); hs.scale = (6, 5, h)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=4.5, depth=3, location=(x, y, h + 1.5), rotation=(0, 0, 0.785)); add(bpy.context.object, mat("roof", (0.06, 0.05, 0.05), 0.9), False)
        if rnd.random() < 0.6:
            bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y - 2.52, h * 0.55), rotation=(1.5708, 0, 0)); add(bpy.context.object, wm, False).scale = (1.2, 1.4, 1)
    for i in range(30):
        tree(rnd.uniform(-45, 45), rnd.uniform(32, 65), rnd.uniform(10, 18))
if PLACE == "swamp":
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 16, 0.03)); wtr = add(bpy.context.object, mat("water", (0.02, 0.035, 0.04), 0.55, 0.0)); wtr.scale = (60, 22, 1)

# red eyes in the dark
eye_m = mat("redeye", (1, 0.05, 0.02), 0.3, 0, 30)
for i in range(SET.get("eyes", 8)):
    x = rnd.uniform(-30, 30); y = rnd.uniform(22, 50); z = rnd.uniform(1, 4)
    for dx in (-0.25, 0.25):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(x + dx, y, z)); add(bpy.context.object, eye_m)
# moon + cold key light + faint fill
bpy.ops.mesh.primitive_uv_sphere_add(radius=4, location=(-30, 120, 40)); add(bpy.context.object, mat("moon", (0.9, 0.95, 1), 0.3, 0, 6))
bpy.ops.object.light_add(type="SUN", location=(0, 0, 40)); sun = bpy.context.object
sun.data.energy = SET.get("moonlight", 1.2); sun.data.color = (0.55, 0.65, 1.0); sun.rotation_euler = (math.radians(60), 0, math.radians(-30))
bpy.ops.object.light_add(type="AREA", location=(0, -18, 10)); fill = bpy.context.object
fill.data.energy = 1500; fill.data.size = 20; fill.data.color = (0.5, 0.6, 1.0)
fill.rotation_euler = (Vector((0, 6, 1)) - fill.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.light_add(type="AREA", location=(0, 45, 8)); back = bpy.context.object
back.data.energy = 9000; back.data.size = 40; back.data.color = (0.45, 0.55, 0.9)
back.rotation_euler = (Vector((0, 0, 1.5)) - back.location).to_track_quat("-Z", "Y").to_euler()
PODIUM_TOP = Vector((0, 12, 1.2))
DRUMS = []

# ---------------- characters ----------------
black, eyew = mat("black", (0.01, 0.01, 0.01), 0.4), mat("eyew", (0.95, 0.95, 0.92), 0.2)
mouth_m = mat("mouth", (0.08, 0.01, 0.02), 0.5)
hat_m = mat("hat", (0.2, 0.15, 0.1), 0.7)
C = {}


def _o():
    return bpy.context.object


def _shape(key, kind, s, ch):
    col = tuple(ch.get("color", (0.3, 0.2, 0.15)))
    if kind == "odo":
        cloak = mat(f"cloak_{key}", col, 0.9)
        bpy.ops.mesh.primitive_cone_add(radius1=0.9 * s, radius2=0.35 * s, depth=2.0 * s, location=(0, 0, 1.0 * s)); o = add(_o(), cloak)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55 * s, location=(0, 0, 2.3 * s)); hood = add(_o(), cloak); hood.scale = (1, 1, 1.15); parent(hood, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4 * s, location=(0, -0.32 * s, 2.22 * s)); face = add(_o(), mat("pale", (0.88, 0.84, 0.78), 0.6)); parent(face, o)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.42 * s, minor_radius=0.12 * s, location=(0, 0, 1.8 * s)); parent(add(_o(), mat("scarf", (0.65, 0.05, 0.05), 0.8)), o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04 * s, depth=2.6 * s, location=(0.75 * s, -0.2 * s, 1.6 * s), rotation=(0, math.radians(-25), 0)); parent(add(_o(), bark), o)
        bpy.ops.mesh.primitive_cube_add(size=0.35 * s, location=(1.3 * s, -0.2 * s, 2.7 * s)); lan = add(_o(), mat("lantern", (1, 0.75, 0.3), 0.3, 0, 18), False); parent(lan, o)
        bpy.ops.object.light_add(type="POINT", location=(1.3 * s, -0.4 * s, 2.7 * s)); L = _o(); L.data.energy = ch.get("lantern", 450); L.data.color = (1, 0.65, 0.3); L.data.shadow_soft_size = 0.2; parent(L, o)
        return o, 1.8 * s, 1.8 * s, 2.9 * s, -0.7 * s, 2.28 * s
    if kind == "moth":
        glow = mat(f"moth_{key}", (0.92, 0.9, 0.8), 0.6, 0, 0.35)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3 * s, location=(0, 0, 3.2 * s)); o = add(_o(), glow); o.scale = (0.8, 0.8, 1.6)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8 * s, location=(sx * 0.8 * s, 0.05, 3.4 * s)); wg = add(_o(), glow); wg.scale = (1.0, 0.06, 0.75); parent(wg, o)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18 * s, location=(sx * 0.85 * s, -0.02, 3.45 * s)); sp = add(_o(), mat("spot", (0.15, 0.1, 0.05), 0.5)); sp.scale = (1, 0.3, 1); parent(sp, o)
        bpy.ops.object.light_add(type="POINT", location=(0, -0.3, 3.2 * s)); L = _o(); L.data.energy = 25; L.data.color = (0.9, 0.95, 1); parent(L, o)
        return o, 1.0 * s, 0.6 * s, 3.8 * s, -0.25 * s, 3.4 * s
    if kind == "gloamhound":
        smoke = mat(f"sm_{key}", (0.01, 0.01, 0.015), 0.95)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0.6 * s, 1.3 * s)); o = add(_o(), smoke); o.scale = (0.8, 1.6, 0.75)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6 * s, location=(0, -1.0 * s, 1.7 * s)); hd = add(_o(), smoke); hd.scale = (0.9, 1.3, 0.9); parent(hd, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(radius1=0.18 * s, depth=0.5 * s, location=(sx * 0.3 * s, -0.9 * s, 2.3 * s)); parent(add(_o(), smoke), o)
            for fy in (-0.4, 1.4):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.13 * s, depth=1.0 * s, location=(sx * 0.4 * s, fy * s, 0.5 * s)); parent(add(_o(), smoke), o)
        return o, 1.6 * s, 3.5 * s, 2.4 * s, -1.75 * s, 1.85 * s
    if kind == "rootwraith":
        bpy.ops.mesh.primitive_cone_add(radius1=1.2 * s, radius2=0.5 * s, depth=6 * s, location=(0, 0, 3 * s)); o = add(_o(), bark)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(radius1=0.2 * s, radius2=0.04 * s, depth=3.5 * s, location=(sx * 1.6 * s, -0.3, 4 * s), rotation=(0, sx * math.radians(60), 0)); parent(add(_o(), bark), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5 * s, location=(0, -0.8 * s, 4.2 * s)); hollow = add(_o(), mat("hole", (0, 0, 0), 1)); hollow.scale = (1, 0.4, 1.4); parent(hollow, o)
        return o, 2.4 * s, 2.4 * s, 6 * s, -0.95 * s, 4.6 * s
    if kind == "shepherd":
        robe = mat(f"robe_{key}", (0.08, 0.08, 0.09), 0.9)
        bpy.ops.mesh.primitive_cone_add(radius1=1.3 * s, radius2=0.35 * s, depth=6.5 * s, location=(0, 0, 3.25 * s)); o = add(_o(), robe)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55 * s, location=(0, -0.1, 6.9 * s)); mk = add(_o(), mat("porcelain", (0.92, 0.9, 0.86), 0.2)); mk.scale = (0.85, 0.7, 1.15); parent(mk, o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=7.5 * s, location=(1.4 * s, -0.2, 3.75 * s)); parent(add(_o(), bark), o)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.45 * s, minor_radius=0.05 * s, location=(1.4 * s, -0.2, 7.6 * s), rotation=(1.5708, 0, 0)); parent(add(_o(), bark), o)
        return o, 2.6 * s, 2.6 * s, 7.4 * s, -0.55 * s, 7.0 * s
    if kind == "crow":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5 * s, location=(0, 0, 0.7 * s)); o = add(_o(), mat("crow", (0.02, 0.02, 0.03), 0.4)); o.scale = (0.8, 1.3, 0.9)
        bpy.ops.mesh.primitive_cone_add(radius1=0.1 * s, depth=0.4 * s, location=(0, -0.75 * s, 0.85 * s), rotation=(1.5708, 0, 0)); parent(add(_o(), mat("beak", (0.2, 0.18, 0.1), 0.5)), o)
        return o, 0.8 * s, 1.3 * s, 1.2 * s, -0.6 * s, 0.95 * s
    if kind == "wickeater":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8 * s, location=(0, 0, 0.9 * s)); o = add(_o(), mat(f"imp_{key}", (0.12, 0.1, 0.08), 0.7))
        return o, 1.6 * s, 1.6 * s, 1.8 * s, -0.75 * s, 1.1 * s
    if kind == "hollowmother":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=2.0 * s, location=(0, 0, 7 * s)); o = add(_o(), mat("spider", (0.05, 0.05, 0.06), 0.6))
        for i in range(8):
            an = i / 8 * 6.28
            bpy.ops.mesh.primitive_cylinder_add(radius=0.12 * s, depth=6 * s, location=(math.cos(an) * 2.6 * s, math.sin(an) * 2.6 * s, 4.5 * s), rotation=(math.sin(an) * 0.5, -math.cos(an) * 0.5, 0)); parent(add(_o(), mat("spider", (0.05, 0.05, 0.06), 0.6)), o)
        return o, 4 * s, 4 * s, 9 * s, -1.9 * s, 7.4 * s
    if kind == "horseman":  # headless rider on a black horse (Sleepy Hollow)
        hide = mat(f"horse_{key}", (0.02, 0.02, 0.025), 0.6); cloak = mat(f"rc_{key}", (0.04, 0.03, 0.05), 0.9)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0, 1.75 * s)); o = add(_o(), hide); o.scale = (0.6, 1.5, 0.62)
        for sx in (-1, 1):
            for fy_ in (-0.95, 0.95):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.13 * s, depth=1.5 * s, location=(sx * 0.33 * s, fy_ * s, 0.75 * s)); parent(add(_o(), hide), o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.28 * s, depth=1.3 * s, location=(0, -1.45 * s, 2.35 * s), rotation=(math.radians(-35), 0, 0)); parent(add(_o(), hide), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45 * s, location=(0, -1.95 * s, 2.75 * s)); hd = add(_o(), hide); hd.scale = (0.7, 1.25, 0.7); parent(hd, o)
        bpy.ops.mesh.primitive_cone_add(radius1=0.6 * s, radius2=0.32 * s, depth=1.9 * s, location=(0, 0.25 * s, 3.25 * s)); parent(add(_o(), cloak), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5 * s, location=(0, 0.25 * s, 4.15 * s)); sh = add(_o(), cloak); sh.scale = (1.3, 0.8, 0.35); parent(sh, o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=0.4 * s, location=(0, 0.25 * s, 4.35 * s)); parent(add(_o(), mat("neckstub", (0.1, 0.02, 0.02), 0.8)), o)
        return o, 1.6 * s, 3.5 * s, 4.4 * s, -2.42 * s, 2.85 * s
    if kind == "soldier":  # Roman legionary: tunic, plumed helmet, round shield; "ghost": pale glowing + sunk to the knees
        gh = ch.get("ghost", False); sink = 0.75 * s if gh else 0.0
        gm = (lambda n, c_, r_=0.6, m_=0.0: mat(f"{n}_{key}", (0.45, 0.8, 0.75), 0.5, 0, 0.55)) if gh else (lambda n, c_, r_=0.6, m_=0.0: mat(f"{n}_{key}", c_, r_, m_))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * s, depth=2.6 * s, location=(0, 0, 1.3 * s - sink)); o = add(_o(), gm("tunic", col, 0.9))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * s, location=(0, 0, 3.0 * s - sink)); parent(add(_o(), gm("skin", (0.85, 0.72, 0.62))), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.47 * s, location=(0, 0.05 * s, 3.15 * s - sink)); hm = add(_o(), gm("helm", (0.55, 0.5, 0.42), 0.3, 1.0)); hm.scale = (1, 1, 0.75); parent(hm, o)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1 * s, 3.65 * s - sink)); cr = add(_o(), gm("crest", (0.75, 0.06, 0.05), 0.8), False); cr.scale = (0.12 * s, 0.8 * s, 0.35 * s); parent(cr, o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.75 * s, depth=0.12 * s, location=(-0.75 * s, -0.25 * s, 1.6 * s - sink), rotation=(0, math.radians(90), math.radians(15))); parent(add(_o(), gm("shield", (0.5, 0.1, 0.08), 0.7)), o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035 * s, depth=3.2 * s, location=(0.7 * s, -0.1 * s, 1.9 * s - sink)); parent(add(_o(), gm("spear", (0.25, 0.2, 0.15), 0.8)), o)
        return o, 1.4 * s, 1.2 * s, 3.9 * s - sink, -0.4 * s, 3.0 * s - sink
    # human (villager, Wren, historical people)
    cl = mat(f"cl_{key}", col, 0.9)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * s, depth=2.6 * s, location=(0, 0, 1.3 * s)); o = add(_o(), cl)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * s, location=(0, 0, 3.0 * s)); parent(add(_o(), mat("skin", (0.85, 0.72, 0.62), 0.6)), o)
    return o, 1.2 * s, 1.2 * s, 3.4 * s, -0.4 * s, 3.05 * s


def make_char(key, ch):
    s, kind = ch.get("size", 1.0), ch.get("kind", "human")
    root = bpy.data.objects.new(key, None); sc.collection.objects.link(root)
    body = bpy.data.objects.new(key + "_body", None); sc.collection.objects.link(body); body.parent = root
    o, Wd, L, H, fy, fz = _shape(key, kind, s, ch)
    o.parent = body
    eyes = []
    glow_eyes = kind in ("horseman", "gloamhound", "crow", "wickeater", "hollowmother")
    n_eyes = {"hollowmother": 6}.get(kind, 2)
    sep = {"odo": 0.17, "moth": 0.1, "shepherd": 0.18}.get(kind, 0.22) * s
    for i in range(n_eyes):
        sx = (i - (n_eyes - 1) / 2) * sep * (1.0 if n_eyes == 2 else 0.9)
        ez = fz + (0.25 * s if (n_eyes > 2 and i % 2) else 0)
        r_ = (0.11 if kind in ("odo", "moth", "crow") else 0.14) * s
        if kind == "shepherd":  # empty black eye holes in the mask
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1 * s, location=(sx, fy - 0.42 * s, ez)); e = add(_o(), black); e.scale = (1, 0.4, 0.6)
        elif glow_eyes:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_ * 0.6, location=(sx, fy - 0.02, ez)); e = add(_o(), mat("redeye2", (1, 0.08, 0.03), 0.3, 0, 12))
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_, location=(sx, fy - 0.03, ez)); e = add(_o(), black); e.scale = (1, 0.6, 1.3)
        e.parent = body; eyes.append(e)
    mz = fz - (0.28 if kind in ("odo",) else 0.4) * s
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 * s, location=(0, fy - 0.03, mz)); mo = add(_o(), mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    if kind == "wickeater":
        mo.scale = (4.0, 0.3, 0.6)
    if kind == "horseman":
        mo.scale = TINY
    hat = bpy.data.objects.new(key + "_hat", None); sc.collection.objects.link(hat); hat.parent = body; hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=s,
                  home=Vector((hx, hy, 0)), top=H, has_hat=False)

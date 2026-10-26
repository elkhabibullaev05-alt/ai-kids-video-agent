"""Hollowmere Tales 3D world: night forest places + lantern-bearers + creatures.
Executed inside story.py (exec). Defines TOD, PODIUM_TOP, DRUMS, C, make_char(), hat_m and builds the set.
SET.place: forest | hill | clearing | graveyard | swamp | village | chapel
Character kinds: odo | moth | lochbeast | narr(none) | gloamhound | rootwraith | shepherd | crow | wickeater | hollowmother | horseman | soldier (+ghost) | lady (+ghost, Brown Lady) | greyman | human
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


if PLACE in ("forest", "clearing", "swamp", "hill"):
    for i in range(70):
        x = rnd.uniform(-45, 45); y = rnd.uniform(6, 60)
        if PLACE == "hill" and abs(x) < 16 and y < 30:  # open hilltop field
            continue
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
if PLACE == "hill":  # Flatwoods hilltop: a dark grassy mound behind the field, tall grass tufts
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(4, 34, -6)); hm_ = add(bpy.context.object, mat("hillg", (0.045, 0.06, 0.035), 0.95)); hm_.scale = (30, 12, 10)
    gr_ = mat("grass", (0.06, 0.08, 0.04), 0.9)
    for i in range(60):
        bpy.ops.mesh.primitive_cone_add(radius1=0.25, depth=rnd.uniform(0.5, 1.1), location=(rnd.uniform(-16, 16), rnd.uniform(4, 28), 0.3)); add(bpy.context.object, gr_, False)
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
        smoke = mat(f"sm_{key}", col if sum(col) > 0.05 else (0.01, 0.01, 0.015), 0.95)  # a coloured beast if the script gives a colour
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
        if ch.get("rider"):  # Wild Hunt rider: hooded black head + curved hunting horn (no neck stump)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5 * s, location=(0, 0.2 * s, 4.75 * s)); hh = add(_o(), cloak); hh.scale = (1, 1, 1.2); parent(hh, o)
            bpy.ops.mesh.primitive_cone_add(radius1=0.32 * s, radius2=0.12 * s, depth=0.6 * s, location=(0, 0.35 * s, 5.4 * s), rotation=(math.radians(20), 0, 0)); parent(add(_o(), cloak), o)
            bpy.ops.mesh.primitive_cone_add(radius1=0.18 * s, radius2=0.04 * s, depth=1.1 * s, location=(0.55 * s, -0.25 * s, 4.7 * s), rotation=(math.radians(-60), math.radians(30), 0)); parent(add(_o(), mat("horn", (0.75, 0.62, 0.35), 0.4, 0.3)), o)
            for sx in (-0.13, 0.13):  # faint ember eyes under the hood
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06 * s, location=(sx * s, -0.27 * s, 4.75 * s)); parent(add(_o(), mat("ridereye", (1, 0.35, 0.05), 0.3, 0, 10)), o)
        else:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=0.4 * s, location=(0, 0.25 * s, 4.35 * s)); parent(add(_o(), mat("neckstub", (0.1, 0.02, 0.02), 0.8)), o)
        return o, 1.6 * s, 3.5 * s, 4.4 * s, -2.42 * s, 2.85 * s
    if kind == "lochbeast":  # Loch Ness shape: dark humps in the water + long neck and small head (front = -y)
        skin = mat(f"lb_{key}", col, 0.35, 0.0)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0.6 * s, 0.1 * s)); o = add(_o(), skin); o.scale = (0.9, 1.5, 0.75)
        for hy in (2.9, 4.8):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75 * s, location=(0, hy * s, 0.0)); hm = add(_o(), skin); hm.scale = (0.8, 1.3, 0.8); parent(hm, o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.28 * s, depth=3.6 * s, location=(0, -0.55 * s, 2.2 * s), rotation=(math.radians(-18), 0, 0)); parent(add(_o(), skin), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45 * s, location=(0, -1.25 * s, 3.95 * s)); hd = add(_o(), skin); hd.scale = (0.9, 1.5, 0.8); parent(hd, o)
        return o, 2.0 * s, 6.0 * s, 4.4 * s, -1.85 * s, 4.05 * s
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
    if kind == "lady":  # Brown Lady of Raynham: long gown (cone), veil, faint glow; "ghost": pale glowing
        gh = ch.get("ghost", True); em = 0.6 if gh else 0.0
        gown = mat(f"gown_{key}", col, 0.8, 0, em)
        bpy.ops.mesh.primitive_cone_add(radius1=0.95 * s, radius2=0.35 * s, depth=2.9 * s, location=(0, 0, 1.45 * s)); o = add(_o(), gown)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.38 * s, location=(0, 0, 3.15 * s)); parent(add(_o(), mat(f"lface_{key}", (0.85, 0.82, 0.75), 0.6, 0, em * 1.5)), o)
        bpy.ops.mesh.primitive_cone_add(radius1=0.62 * s, radius2=0.2 * s, depth=1.6 * s, location=(0, 0.12 * s, 2.95 * s)); parent(add(_o(), mat(f"veil_{key}", (col[0] * 0.8, col[1] * 0.8, col[2] * 0.8), 0.9, 0, em)), o)
        return o, 1.6 * s, 1.6 * s, 3.6 * s, -0.36 * s, 3.2 * s
    if kind == "winged":  # Point Pleasant winged figure: tall grey body, no neck, huge wings, glowing red eyes (front = -y)
        skin = mat(f"wg_{key}", col, 0.85, 0, 0.3)
        bpy.ops.mesh.primitive_cone_add(radius1=0.55 * s, radius2=0.75 * s, depth=3.4 * s, location=(0, 0, 1.7 * s)); o = add(_o(), skin)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75 * s, location=(0, 0, 3.55 * s)); hd = add(_o(), skin); hd.scale = (1.0, 0.8, 0.7); parent(hd, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(sx * 1.9 * s, 0.25 * s, 3.0 * s), rotation=(0, sx * math.radians(-18), 0)); wg = add(_o(), skin); wg.scale = (1.9, 0.07, 1.25); parent(wg, o)
            bpy.ops.mesh.primitive_cone_add(radius1=0.12 * s, depth=1.0 * s, location=(sx * 3.6 * s, 0.25 * s, 3.9 * s), rotation=(0, sx * math.radians(-60), 0)); parent(add(_o(), skin), o)
        return o, 7.0 * s, 1.6 * s, 4.1 * s, -0.62 * s, 3.55 * s
    if kind == "demon":  # Dover Demon (1977 sketches): thin hairless peach body, long thin limbs, huge watermelon head, glowing eyes, no nose/mouth (front = -y)
        skin = mat(f"dd_{key}", col, 0.55, 0, 0.12)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * s, location=(0, 0, 1.75 * s)); o = add(_o(), skin); o.scale = (0.75, 0.6, 1.35)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95 * s, location=(0, 0, 3.05 * s)); hd = add(_o(), skin); hd.scale = (0.85, 0.85, 1.12); parent(hd, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.07 * s, depth=1.6 * s, location=(sx * 0.2 * s, 0, 0.8 * s)); parent(add(_o(), skin), o)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.06 * s, depth=1.9 * s, location=(sx * 0.62 * s, -0.1 * s, 1.35 * s), rotation=(0, sx * math.radians(-14), 0)); parent(add(_o(), skin), o)
            for fx in (-0.08, 0.0, 0.08):  # long fingers
                bpy.ops.mesh.primitive_cylinder_add(radius=0.02 * s, depth=0.45 * s, location=(sx * 0.86 * s + fx * s, -0.1 * s, 0.3 * s)); parent(add(_o(), skin), o)
        return o, 1.9 * s, 1.0 * s, 4.1 * s, -0.8 * s, 3.15 * s
    if kind == "jack":  # Spring-heeled Jack (1838 accounts): tall thin figure, black cloak, big metal helmet, tight white oilskin suit, claws, red fire eyes (front = -y)
        suit = mat(f"oil_{key}", (0.86, 0.88, 0.9), 0.15, 0.0); cloak = mat(f"jc_{key}", (0.03, 0.02, 0.04), 0.9)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.38 * s, depth=3.0 * s, location=(0, 0, 1.5 * s)); o = add(_o(), suit)
        bpy.ops.mesh.primitive_cone_add(radius1=1.05 * s, radius2=0.42 * s, depth=3.1 * s, location=(0, 0.3 * s, 1.75 * s)); cl = add(_o(), cloak); cl.scale = (1, 0.7, 1); parent(cl, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * s, location=(0, 0, 3.55 * s)); parent(add(_o(), mat("jskin", (0.75, 0.68, 0.62), 0.6)), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.56 * s, location=(0, 0.08 * s, 3.8 * s)); hm = add(_o(), mat("jhelm", (0.55, 0.55, 0.6), 0.25, 1.0)); hm.scale = (1, 1, 0.8); parent(hm, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.08 * s, depth=1.6 * s, location=(sx * 0.55 * s, -0.15 * s, 2.0 * s), rotation=(0, sx * math.radians(-20), 0)); parent(add(_o(), suit), o)
            for fx in (-0.07, 0.0, 0.07):  # claws
                bpy.ops.mesh.primitive_cone_add(radius1=0.03 * s, depth=0.35 * s, location=(sx * 0.82 * s + fx * s, -0.2 * s, 1.1 * s), rotation=(math.pi, 0, 0)); parent(add(_o(), mat("claw", (0.7, 0.7, 0.75), 0.2, 1.0)), o)
        return o, 1.6 * s, 1.2 * s, 4.3 * s, -0.42 * s, 3.55 * s
    if kind == "flatwoods":  # Flatwoods figure (1952 accounts): ~12 ft, red glowing face, ace-of-spades hood behind the head, green pleated skirt, claw hands; floats (front = -y)
        green = mat(f"fw_{key}", (0.05, 0.28, 0.08), 0.35, 0.4, 0.15); hood = mat(f"fwh_{key}", (0.02, 0.05, 0.03), 0.6, 0.3)
        bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=1.35 * s, radius2=0.5 * s, depth=3.6 * s, location=(0, 0, 2.2 * s)); o = add(_o(), green)
        for zz in (1.0, 1.9, 2.8):  # folds
            bpy.ops.mesh.primitive_torus_add(major_radius=(1.35 - (zz - 0.4) / 3.6 * 0.85) * s, minor_radius=0.05 * s, location=(0, 0, zz * s)); parent(add(_o(), hood), o)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5 * s, depth=1.3 * s, location=(0, 0, 4.6 * s)); parent(add(_o(), green), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2 * s, location=(0, 0.4 * s, 5.95 * s)); sp_ = add(_o(), hood); sp_.scale = (1.0, 0.22, 1.05); parent(sp_, o)
        bpy.ops.mesh.primitive_cone_add(radius1=0.55 * s, depth=1.1 * s, location=(0, 0.4 * s, 7.45 * s)); cn_ = add(_o(), hood); cn_.scale = (1, 0.3, 1); parent(cn_, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55 * s, location=(0, -0.05 * s, 5.75 * s)); fc_ = add(_o(), mat(f"fwf_{key}", (0.75, 0.06, 0.04), 0.4, 0, 1.2)); fc_.scale = (0.85, 0.6, 1.0); parent(fc_, o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.09 * s, depth=1.8 * s, location=(sx * 0.85 * s, -0.25 * s, 4.3 * s), rotation=(math.radians(-35), sx * math.radians(-35), 0)); parent(add(_o(), hood), o)
            for fx in (-0.08, 0.0, 0.08):  # claws
                bpy.ops.mesh.primitive_cone_add(radius1=0.04 * s, depth=0.45 * s, location=(sx * 1.35 * s + fx * s, -0.95 * s, 3.75 * s), rotation=(math.radians(-60), 0, 0)); parent(add(_o(), mat("claw", (0.7, 0.7, 0.75), 0.2, 1.0)), o)
        o.location.z += 0.35 * s
        return o, 2.7 * s, 1.4 * s, 8.0 * s, -0.4 * s, 6.1 * s
    if kind == "greyman":  # Grey Man of Ben Macdui (Am Fear Liath Mor): very tall grey hooded shape half lost in the mist, long arms, long legs, pale grey face (front = -y)
        fur = mat(f"gm_{key}", col, 0.95, 0, 0.18)
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.1 * s, radius2=0.75 * s, depth=4.2 * s, location=(0, 0, 2.6 * s)); o = add(_o(), fur)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.22 * s, depth=1.6 * s, location=(sx * 0.45 * s, 0, 0.6 * s)); parent(add(_o(), fur), o)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.16 * s, depth=3.4 * s, location=(sx * 1.05 * s, -0.15 * s, 3.0 * s), rotation=(0, sx * math.radians(-10), 0)); parent(add(_o(), fur), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95 * s, location=(0, 0.05 * s, 4.75 * s)); sh = add(_o(), fur); sh.scale = (1.35, 0.8, 0.45); parent(sh, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62 * s, location=(0, 0.05 * s, 5.45 * s)); hd = add(_o(), fur); hd.scale = (1, 1, 1.15); parent(hd, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42 * s, location=(0, -0.3 * s, 5.35 * s)); fc = add(_o(), mat(f"gmf_{key}", (0.62, 0.64, 0.66), 0.7, 0, 0.25)); fc.scale = (0.9, 0.6, 1.1); parent(fc, o)
        return o, 2.6 * s, 1.6 * s, 6.1 * s, -0.55 * s, 5.45 * s
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
    glow_eyes = kind in ("flatwoods", "jack", "demon", "winged", "lochbeast", "horseman", "gloamhound", "crow", "wickeater", "hollowmother")
    n_eyes = {"hollowmother": 6}.get(kind, 2)
    sep = {"flatwoods": 0.36, "odo": 0.17, "moth": 0.1, "shepherd": 0.18, "winged": 0.36, "demon": 0.5}.get(kind, 0.22) * s
    for i in range(n_eyes):
        sx = (i - (n_eyes - 1) / 2) * sep * (1.0 if n_eyes == 2 else 0.9)
        ez = fz + (0.25 * s if (n_eyes > 2 and i % 2) else 0)
        r_ = (0.11 if kind in ("odo", "moth", "crow") else 0.26 if kind in ("winged", "flatwoods") else 0.3 if kind == "demon" else 0.14) * s
        if kind == "shepherd":  # empty black eye holes in the mask
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1 * s, location=(sx, fy - 0.42 * s, ez)); e = add(_o(), black); e.scale = (1, 0.4, 0.6)
        elif glow_eyes:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_ * 0.6, location=(sx, fy - 0.02, ez)); e = add(_o(), mat("ddeye", (1, 0.5, 0.05), 0.3, 0, 14)) if kind == "demon" else add(_o(), mat("fweye", (1, 0.95, 0.6), 0.3, 0, 20)) if kind == "flatwoods" else add(_o(), mat("redeye2", (1, 0.08, 0.03), 0.3, 0, 12))
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_, location=(sx, fy - 0.03, ez)); e = add(_o(), black); e.scale = (1, 0.6, 1.3)
        e.parent = body; eyes.append(e)
    mz = fz - (0.28 if kind in ("odo",) else 0.4) * s
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 * s, location=(0, fy - 0.03, mz)); mo = add(_o(), mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    if kind == "wickeater":
        mo.scale = (4.0, 0.3, 0.6)
    if kind in ("horseman", "winged", "demon", "flatwoods", "greyman"):
        mo.scale = TINY
    hat = bpy.data.objects.new(key + "_hat", None); sc.collection.objects.link(hat); hat.parent = body; hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=s,
                  home=Vector((hx, hy, 0)), top=H, has_hat=False)

"""Dough Bros 3D world: moonlit kitchen counter + dough heroes + appliance villains.
Executed inside story.py (exec) — uses its helpers: bpy, sc, mat, add, parent, K, TINY, SET, rnd, Vector, math, TL.
Defines: TOD, PODIUM_TOP, DRUMS, C, make_char(), hat_m, and builds the set.
Character "kind": loaf | bean | triangle | star | rock | pot | toaster | kettle | jelly | ghost
"""
import bmesh

TOD = SET.get("time", "night")
PLACE = SET.get("place", "kitchen")  # kitchen | freezer | pantry | table | garden
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs[0].default_value = {"freezer": (0.05, 0.12, 0.2, 1), "garden": (0.02, 0.04, 0.08, 1)}.get(PLACE, (0.03, 0.035, 0.07, 1))
bg.inputs[1].default_value = 1.0

wood = mat("wood", (0.42, 0.26, 0.14), 0.55)
tile = mat("tile", (0.78, 0.82, 0.86), 0.25)
grout = mat("grout", (0.35, 0.37, 0.4), 0.9)
metal = mat("metal", (0.55, 0.57, 0.6), 0.25, 1.0)
dark = mat("darkm", (0.08, 0.08, 0.1), 0.5)
if PLACE == "freezer":
    wood = mat("ice", (0.75, 0.88, 1.0), 0.08, 0, 0.15)
    tile = mat("frost", (0.85, 0.93, 1.0), 0.3)
elif PLACE == "garden":
    wood = mat("grass", (0.08, 0.2, 0.06), 0.9)
    tile = mat("fence", (0.3, 0.22, 0.15), 0.8)

# counter top (floor of the world)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 4, 0)); fl = add(bpy.context.object, wood); fl.scale = (80, 44, 1)
for i in range(-20, 21, 2):  # planks
    bpy.ops.mesh.primitive_plane_add(size=1, location=(i * 1.9, 4, 0.004)); pl = add(bpy.context.object, mat("plank", (0.3, 0.18, 0.09), 0.7), False); pl.scale = (0.05, 44, 1)
# back wall with tiles
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 24, 10), rotation=(math.radians(90), 0, 0)); wl = add(bpy.context.object, grout, False); wl.scale = (80, 20, 1)
for ix in range(-16, 17):
    for iz in range(0, 9):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(ix * 2.2, 23.9, 1.2 + iz * 2.2)); tt = add(bpy.context.object, tile, False); tt.scale = (2.05, 0.1, 2.05)
# side walls so sideways camera angles never see the void
for sx in (-1, 1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(sx * 30, 4, 10), rotation=(math.radians(90), 0, math.radians(90))); sw = add(bpy.context.object, mat("sidewall", (0.55, 0.58, 0.62), 0.6), False); sw.scale = (44, 20, 1)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -28, 10), rotation=(math.radians(90), 0, 0)); fw = add(bpy.context.object, mat("frontwall", (0.35, 0.3, 0.28), 0.8), False); fw.scale = (80, 20, 1)
# window with moon
bpy.ops.mesh.primitive_plane_add(size=1, location=(-6, 23.7, 12), rotation=(math.radians(90), 0, 0)); win = add(bpy.context.object, mat("night", (0.05, 0.08, 0.22), 0.3, 0, 1.2), False); win.scale = (10, 7, 1)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.3, location=(-3.5, 23.5, 13.5)); add(bpy.context.object, mat("moon", (1, 0.97, 0.85), 0.3, 0, 12))
for x in (-11, -1, -6):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 23.6, 12)); fr = add(bpy.context.object, dark, False); fr.scale = (0.3, 0.3, 7.4)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-6, 23.6, 12)); fr = add(bpy.context.object, dark, False); fr.scale = (10.4, 0.3, 0.3)
# background props: fridge (left), stove + pot (right), jars, cutting board
bpy.ops.mesh.primitive_cube_add(size=1, location=(-22, 20, 9)); fz = add(bpy.context.object, mat("fridge", (0.86, 0.88, 0.9), 0.3), False); fz.scale = (7, 6, 18)
bpy.ops.object.modifier_add(type="BEVEL"); fz.modifiers[-1].width = 0.4; fz.modifiers[-1].segments = 3
bpy.ops.mesh.primitive_cube_add(size=1, location=(-18.6, 17, 10)); add(bpy.context.object, metal, False).scale = (0.3, 0.3, 4)
bpy.ops.mesh.primitive_cube_add(size=1, location=(18, 20, 1.2)); st = add(bpy.context.object, dark, False); st.scale = (9, 6, 2.4)
for bx in (15.5, 20.5):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.3, minor_radius=0.15, location=(bx, 19, 2.45)); add(bpy.context.object, mat("burner", (1, 0.25, 0.05), 0.4, 0, 3 if PLACE == "kitchen" else 0))
JARC = [(0.9, 0.5, 0.2), (0.4, 0.7, 0.3), (0.8, 0.2, 0.3), (0.95, 0.85, 0.4)]
for i in range(4):
    x = 6 + i * 2.4
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9, depth=2.6, location=(x, 21.5, 1.3)); add(bpy.context.object, mat(f"jar{i}", JARC[i], 0.05, 0, 0.1))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.95, depth=0.4, location=(x, 21.5, 2.8)); add(bpy.context.object, metal)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-10, 14, 0.15)); cb = add(bpy.context.object, mat("board", (0.65, 0.45, 0.25), 0.6), False); cb.scale = (7, 4.5, 0.3)
bpy.ops.object.modifier_add(type="BEVEL"); cb.modifiers[-1].width = 0.2

# lights: cold moonlight + warm under-cabinet strip + rim + soft fill
bpy.ops.object.light_add(type="SUN", location=(0, 0, 40)); sun = bpy.context.object
sun.data.energy = 1.4; sun.data.color = (0.6, 0.7, 1.0); sun.rotation_euler = (math.radians(50), 0, math.radians(30))
bpy.ops.object.light_add(type="AREA", location=(0, 18, 9)); strip = bpy.context.object
strip.data.energy = 2500; strip.data.size = 30; strip.data.color = (1.0, 0.75, 0.45); strip.rotation_euler = (math.radians(30), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(0, -22, 12)); fill = bpy.context.object
fill.data.energy = 3500; fill.data.size = 24; fill.data.color = (0.8, 0.85, 1.0)
fill.rotation_euler = (Vector((0, 6, 1)) - fill.location).to_track_quat("-Z", "Y").to_euler()
bpy.ops.object.light_add(type="POINT", location=(18, 17, 4)); bpy.context.object.data.energy = 900; bpy.context.object.data.color = (1, 0.35, 0.1)

PODIUM_TOP = Vector((-10, 14, 0.45))  # cutting board: props placed "on podium" sit here
DRUMS = []  # no Truth Press in this world

# ---------------- characters ----------------
black, eyew = mat("black", (0.02, 0.02, 0.02), 0.4), mat("eyew", (0.98, 0.98, 0.98), 0.2)
mouth_m = mat("mouth", (0.3, 0.02, 0.04), 0.5)
hat_m = mat("hat", (0.25, 0.18, 0.1), 0.7)
ember = mat("ember", (1.0, 0.45, 0.05), 0.3, 0, 8)
C = {}


def _bevel(o, wdt, seg=4):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_add(type="BEVEL"); o.modifiers[-1].width = wdt; o.modifiers[-1].segments = seg


def _star_mesh(name, R=1.0, r=0.6, depth=0.5, n=5):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    pts = []
    if R == r:  # regular polygon with a tip pointing up
        for i in range(n):
            ang = math.pi / 2 + i * 2 * math.pi / n
            pts.append((R * math.cos(ang), 0, R * math.sin(ang)))
    else:
        for i in range(2 * n):
            ang = math.pi / 2 + i * math.pi / n
            rr = R if i % 2 == 0 else r
            pts.append((rr * math.cos(ang), 0, rr * math.sin(ang)))
    f = bm.faces.new([bm.verts.new((x, -depth / 2, z)) for x, _, z in pts])
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)], vec=(0, depth, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    return o


def _shape(kind, s, m):
    """Builds the body mesh at the origin (feet at z=0). Returns (obj, W, L, H, front_y)."""
    if kind == "loaf":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.0 * s)); o = add(bpy.context.object, m); o.scale = (2.2 * s, 1.6 * s, 1.6 * s); _bevel(o, 0.55 * s, 5)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1.75 * s)); top = add(bpy.context.object, mat("crust", (0.55, 0.32, 0.12), 0.6)); top.scale = (1.15 * s, 0.85 * s, 0.45 * s); parent(top, o)
        return o, 2.2 * s, 1.6 * s, 2.2 * s, -0.8 * s
    if kind == "bean":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1.5 * s)); o = add(bpy.context.object, m); o.scale = (0.85 * s, 0.75 * s, 1.5 * s)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3 * s, 0, 2.7 * s)); bd = add(bpy.context.object, mat("band", (0.95, 0.9, 0.8), 0.7), False)
        bd.scale = (1.1 * s, 0.3 * s, 0.25 * s); bd.rotation_euler = (0, math.radians(25), 0); parent(bd, o)
        return o, 1.7 * s, 1.5 * s, 3.0 * s, -0.75 * s
    if kind == "triangle":
        o = _star_mesh("tri", 1.7 * s, 1.7 * s, 0.9 * s, n=3)
        o.location = (0, 0, 1.0 * s); add(o, m, False); _bevel(o, 0.3 * s, 4)
        g = mat("glasses", (0.1, 0.1, 0.12), 0.3)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.33 * s, minor_radius=0.05 * s, location=(sx * 0.42 * s, -0.5 * s, 1.55 * s), rotation=(math.radians(90), 0, 0)); parent(add(bpy.context.object, g), o)
        return o, 2.6 * s, 0.9 * s, 2.8 * s, -0.45 * s
    if kind == "star":
        o = _star_mesh("star", 1.5 * s, 0.85 * s, 0.6 * s); o.location = (0, 0, 1.5 * s); add(o, m, False); _bevel(o, 0.18 * s, 3)
        ic = mat("icing", (1, 1, 1), 0.2)
        for i in range(6):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 * s, location=(rnd.uniform(-0.9, 0.9) * s, -0.32 * s, (1.5 + rnd.uniform(0.3, 1.1)) * s)); parent(add(bpy.context.object, ic), o)
        return o, 3.0 * s, 0.6 * s, 3.0 * s, -0.32 * s
    if kind == "rock":
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.2 * s, location=(0, 0, 1.15 * s)); o = add(bpy.context.object, m)
        for v in o.data.vertices:
            v.co *= rnd.uniform(0.85, 1.12)
        return o, 2.4 * s, 2.2 * s, 2.3 * s, -1.05 * s
    if kind in ("pot", "kettle"):
        bpy.ops.mesh.primitive_cylinder_add(radius=2.3 * s, depth=3.0 * s, location=(0, 0, 1.9 * s)); o = add(bpy.context.object, m); _bevel(o, 0.35 * s, 4)
        bpy.ops.mesh.primitive_torus_add(major_radius=2.35 * s, minor_radius=0.18 * s, location=(0, 0, 3.4 * s)); parent(add(bpy.context.object, metal), o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=2.3 * s, location=(0, 0, 3.45 * s)); lid = add(bpy.context.object, m); lid.scale = (1, 1, 0.3); parent(lid, o)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35 * s, location=(0, 0, 4.25 * s)); parent(add(bpy.context.object, dark), o)
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.5 * s, minor_radius=0.13 * s, location=(sx * 2.6 * s, 0, 2.8 * s), rotation=(0, math.radians(90), 0)); parent(add(bpy.context.object, metal), o)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.25 * s, depth=0.6 * s, location=(sx * 1.3 * s, 0, 0.3 * s)); parent(add(bpy.context.object, dark), o)
        return o, 4.6 * s, 4.6 * s, 4.4 * s, -2.3 * s
    if kind == "toaster":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.6 * s)); o = add(bpy.context.object, metal); o.scale = (3.4 * s, 2.0 * s, 3.0 * s); _bevel(o, 0.5 * s, 4)
        for sx in (-0.7, 0.7):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * s, 0, 3.1 * s)); sl = add(bpy.context.object, dark, False); sl.scale = (0.4 * s, 1.4 * s, 0.1 * s); parent(sl, o)
        return o, 3.4 * s, 2.0 * s, 3.2 * s, -1.0 * s
    if kind == "jelly":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=2.2 * s, location=(0, 0, 1.6 * s)); o = add(bpy.context.object, m); o.scale = (1.2, 1.0, 0.8)
        return o, 5.2 * s, 4.4 * s, 3.4 * s, -2.1 * s
    # ghost (Frostbite)
    bpy.ops.mesh.primitive_cone_add(radius1=1.5 * s, radius2=0.9 * s, depth=3.0 * s, location=(0, 0, 1.8 * s)); o = add(bpy.context.object, m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0 * s, location=(0, 0, 3.3 * s)); parent(add(bpy.context.object, m), o)
    return o, 3.0 * s, 2.6 * s, 4.2 * s, -1.05 * s


def make_char(key, ch):
    s, kind = ch.get("size", 1.0), ch.get("kind", "loaf")
    root = bpy.data.objects.new(key, None); sc.collection.objects.link(root)
    alpha_kind = kind in ("jelly", "ghost")
    body_m = mat(f"b_{key}", tuple(ch["color"]), 0.15 if alpha_kind else 0.5, 0.0, 0.3 if kind == "ghost" else 0)
    body = bpy.data.objects.new(key + "_body", None); sc.collection.objects.link(body); body.parent = root
    o, Wd, L, H, fy = _shape(kind, s, body_m)
    bpy.context.view_layer.update()
    zs = [(ob.matrix_world @ Vector(c)).z for ob in [o] + list(o.children_recursive) if ob.type == "MESH" for c in ob.bound_box]
    o.location.z += 0.04 - min(zs)  # stand on the counter
    o.parent = body
    fz = H * (0.62 if kind not in ("pot", "kettle") else 0.55)
    ex = Wd * (0.2 if kind not in ("pot", "kettle", "jelly") else 0.18)
    eyes = []
    sizes = ch.get("eye_sizes", [1.0, 1.0])
    exs = [-ex, ex] + ([0] if kind in ("pot",) else [])
    for i, sx in enumerate(exs):
        es = sizes[i] if i < len(sizes) else 0.9
        ez = fz + (0.55 * s if i == 2 else 0)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.36 * s * es, location=(sx, fy - 0.05, ez)); e = add(bpy.context.object, eyew)
        e.scale = (1, 0.55, 1.1); e.parent = body; eyes.append(e)
        pm = ember if kind in ("rock", "pot", "toaster", "kettle") else black
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17 * s * es, location=(sx, fy - 0.24 * s, ez - 0.03 * s)); parent(add(bpy.context.object, pm), e)
        if ch.get("brows", 0):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(sx, fy - 0.1, ez + 0.5 * s * es)); br = add(bpy.context.object, black, False)
            br.scale = (0.5 * s, 0.06, 0.1 * s); br.rotation_euler = (0, (1 if sx < 0 else -1) * math.radians(ch["brows"]), 0); br.parent = body
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3 * s, location=(0, fy - 0.03, H * 0.33 if kind not in ("star", "triangle") else H * 0.4)); mo = add(bpy.context.object, mouth_m)
    mo.scale = (1.3, 0.3, 0.25); mo.parent = body
    if ch.get("stitch"):
        for k in range(5):
            bpy.ops.mesh.primitive_cube_add(size=1, location=((k - 2) * 0.18 * s, fy - 0.12, mo.location.z)); stc = add(bpy.context.object, black, False); stc.scale = (0.03, 0.03, 0.3 * s); parent(stc, mo)
    if kind in ("loaf", "bean", "triangle", "star", "rock"):  # little feet
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28 * s, location=(sx * Wd * 0.22, fy * 0.3, 0.12 * s)); ft = add(bpy.context.object, body_m); ft.scale = (1, 1.4, 0.55); ft.parent = body
    hat = bpy.data.objects.new(key + "_hat", None); sc.collection.objects.link(hat); hat.parent = body; hat.scale = TINY; hat.keyframe_insert("scale", frame=1)
    hx, hy = ch["home"]
    root.location = (hx, hy, 0)
    C[key] = dict(root=root, body=body, eyes=eyes, mouth=mo, hat=hat, L=L, W=Wd, H=H, size=s,
                  home=Vector((hx, hy, 0)), top=H, has_hat=False)

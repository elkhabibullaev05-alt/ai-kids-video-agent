from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args():
    values = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue-json", required=True, type=Path)
    parser.add_argument("--frames-dir", required=True, type=Path)
    parser.add_argument("--render-width", required=True, type=int)
    parser.add_argument("--render-height", required=True, type=int)
    return parser.parse_args(values)


def enable_mpfb():
    module = "bl_ext.blender_org.mpfb"
    if module not in sys.modules:
        result = bpy.ops.preferences.addon_enable(module=module)
        if "FINISHED" not in result:
            raise RuntimeError("Could not enable the installed MPFB Blender extension.")
    from bl_ext.blender_org.mpfb.services.assetservice import AssetService

    packs = set(AssetService.get_pack_names())
    required = {
        "makehuman_system_assets",
        "hair01",
        "pants01",
        "shirts01",
        "system_eye_materials01",
        "faceunits01",
    }
    missing = sorted(required - packs)
    if missing:
        raise RuntimeError(f"Install the free MakeHuman asset packs in Blender before rendering: {', '.join(missing)}")


def _material(name, color, roughness=0.6, metallic=0.0, emission=None):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1)
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    if emission:
        emission_color, strength = emission
        shader.inputs["Emission Color"].default_value = (*emission_color, 1)
        shader.inputs["Emission Strength"].default_value = strength
    return material


def _box(name, location, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        modifier = obj.modifiers.new("Soft worn edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj


def _text(name, body, location, size, material, rotation=(math.pi / 2, 0, 0)):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = rotation
    obj.data.materials.append(material)
    return obj


def _area_light(name, location, target, power, size, color):
    data = bpy.data.lights.new(name, "AREA")
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    data.energy = power
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj


def build_bodega():
    concrete = _material("aged warm plaster", (0.31, 0.29, 0.25), 0.9)
    dark_green = _material("deep bodega green", (0.025, 0.09, 0.078), 0.46)
    wood = _material("counter walnut", (0.16, 0.075, 0.035), 0.35)
    metal = _material("brushed steel", (0.24, 0.28, 0.29), 0.26, 0.7)
    glass = _material("aged display glass", (0.06, 0.17, 0.19), 0.16, 0.12)
    cream = _material("warm painted lettering", (0.92, 0.79, 0.53), 0.42, emission=((0.8, 0.38, 0.12), 0.18))
    paper = _material("envelope paper", (0.72, 0.59, 0.39), 0.88)
    photo = _material("old photograph", (0.22, 0.29, 0.30), 0.76)
    tile = _material("old green tile", (0.09, 0.22, 0.20), 0.32)

    _box("shop floor", (0, 0, -0.11), (9, 8, 0.22), wood)
    _box("rear plaster wall left", (-2.75, 1.82, 1.65), (2.5, 0.22, 3.3), concrete)
    _box("rear plaster wall right", (2.75, 1.82, 1.65), (2.5, 0.22, 3.3), concrete)
    _box("rear plaster wall below window", (0, 1.82, 0.86), (3.0, 0.22, 1.72), concrete)
    _box("rear plaster wall above window", (0, 1.82, 3.03), (3.0, 0.22, 0.54), concrete)
    _box("left wall", (-3.92, -0.2, 1.65), (0.16, 4.1, 3.3), dark_green)
    _box("right wall", (3.92, -0.2, 1.65), (0.16, 4.1, 3.3), dark_green)
    _box("tile backsplash", (0, 1.66, 1.12), (7.5, 0.055, 1.55), tile)
    for x in [i * 0.25 for i in range(-14, 15)]:
        _box(f"tile grout vertical {x}", (x, 1.625, 1.12), (0.012, 0.015, 1.54), metal)
    for z in [0.43, 0.68, 0.93, 1.18, 1.43, 1.68]:
        _box(f"tile grout horizontal {z}", (0, 1.625, z), (7.5, 0.015, 0.012), metal)

    _box("window recess", (0, 1.67, 2.25), (2.75, 0.12, 1.02), dark_green)
    for x in (-1.34, 0, 1.34):
        _box("window frame", (x, 1.53, 2.25), (0.07, 0.09, 0.98), metal)
    _box("window sill", (0, 1.52, 1.76), (2.82, 0.16, 0.08), wood, 0.025)

    city_colors = (
        _material("brick facade", (0.19, 0.12, 0.11), 0.93),
        _material("stone facade", (0.31, 0.29, 0.25), 0.9),
        _material("night building", (0.12, 0.17, 0.23), 0.85),
    )
    for building_index, x in enumerate((-1.42, -0.48, 0.48, 1.42, -4.4, -2.8, 2.8, 4.4)):
        height = (2.3, 3.1, 2.6)[building_index % 3]
        width = 0.87 if abs(x) < 2 else 1.6
        building_y = 1.72 if abs(x) < 2 else 3.2
        _box(
            f"Astoria apartment building {building_index}",
            (x, building_y, height / 2 + 1.45),
            (width, 0.25, height),
            city_colors[building_index % len(city_colors)],
        )
        for z in range(2, int(height * 2) + 2, 2):
            for window_x in (x - width * 0.27, x + width * 0.27):
                _box(
                    "distant amber apartment window",
                    (window_x, building_y - 0.155, z / 2 + 1.33),
                    (0.24, 0.02, 0.36),
                    cream if (window_x + z) % 2 else dark_green,
                )

    _box("bodega awning sign", (0, 1.49, 3.04), (3.42, 0.12, 0.4), dark_green, 0.04)
    _text("Astoria Deli lettering", "ASTORIA  •  DELI", (0, 1.414, 3.04), 0.19, cream)

    for shelf_x in (-3.25, 3.25):
        _box("steel shelf backing", (shelf_x, 1.39, 1.35), (0.75, 0.19, 1.72), metal)
        for z in (0.67, 1.1, 1.52, 1.94):
            _box("bodega shelf", (shelf_x, 1.15, z), (0.86, 0.52, 0.06), wood)
            for product_index in range(4):
                px = shelf_x - 0.31 + product_index * 0.2
                product_material = (dark_green, cream, glass, tile)[product_index]
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.055,
                    depth=0.23 + (product_index % 2) * 0.05,
                    location=(px, 1.13, z + 0.15),
                )
                bpy.context.object.name = "small grocery product"
                bpy.context.object.data.materials.append(product_material)

    _box("front counter body", (0, -0.47, 0.48), (5.6, 0.72, 0.96), dark_green, 0.06)
    _box("counter wooden top", (0, -0.47, 0.99), (5.75, 0.8, 0.11), wood, 0.04)
    _box("closed envelope", (0.2, -0.53, 1.058), (0.34, 0.24, 0.018), paper)
    _box("old photo", (0.51, -0.47, 1.062), (0.23, 0.17, 0.02), photo)
    _text("envelope stamp", "2009", (0.2, -0.656, 1.071), 0.045, dark_green, rotation=(0, 0, 0))

    for index, color in enumerate(((0.18, 0.28, 0.44), (0.48, 0.18, 0.12), (0.18, 0.38, 0.28))):
        decal = _material(f"old faded sticker {index}", color, 0.8)
        _box(f"counter sticker {index}", (-1.5 + index * 0.48, -0.878, 0.42), (0.38, 0.015, 0.2), decal)

    _area_light("warm ceiling practical", (0, 0.1, 3.3), (0, 0, 1), 300, 2.2, (1.0, 0.65, 0.37))
    _area_light("cool street window", (0, 1.1, 2.6), (0, 0, 1.2), 260, 1.8, (0.38, 0.58, 1.0))
    _area_light("soft camera fill", (0, -1.5, 2.5), (0, 0, 1.45), 110, 2.8, (1.0, 0.83, 0.68))
    _area_light("hair rim", (-2.4, 0.7, 2.5), (-0.4, 0, 1.4), 150, 1.0, (1.0, 0.48, 0.25))


def _create_character(character: dict, index: int):
    from bl_ext.blender_org.mpfb.ui.new_human.randomize.randomizeproperties import RANDOMIZE_PROPERTIES
    from bl_ext.blender_org.mpfb.services.faceservice import FaceService

    scene = bpy.context.scene
    settings = RANDOMIZE_PROPERTIES
    gender = character["gender"]
    for name, value in (
        ("seed", character["seed"]),
        ("discrete_age", True),
        ("age_allow_baby", False),
        ("age_allow_child", False),
        ("age_allow_young", True),
        ("age_allow_middleage", False),
        ("age_allow_old", False),
        ("discrete_gender", True),
        ("gender_allow_female", gender == "female"),
        ("gender_allow_male", gender == "male"),
        ("add_rig", "mixamo"),
        ("eyes_mode", "HIGHPOLY"),
        ("eyes_material_type", "PROCEDURAL_EYES"),
        ("hair_randomize", True),
        ("hair_pack", "hair01"),
        ("hair_include", character["hair_filter"]),
        ("hair_match_gender", True),
        ("clothes_full_body_enable", False),
        ("clothes_upper_body_enable", True),
        ("clothes_upper_body_pack", "shirts01"),
        ("clothes_upper_body_include_any", "t-shirt"),
        ("clothes_upper_body_include_female", character["upper_clothing"] if gender == "female" else ""),
        ("clothes_upper_body_include_male", character["upper_clothing"] if gender == "male" else ""),
        ("clothes_lower_body_enable", True),
        ("clothes_lower_body_pack", "pants01"),
        ("clothes_lower_body_include_any", "cortu_cargo_pants"),
        ("clothes_feet_enable", True),
    ):
        settings.set_value(name, value, entity_reference=scene)

    existing = set(scene.objects)
    result = bpy.ops.mpfb.create_random_human()
    if "FINISHED" not in result:
        raise RuntimeError(f"MPFB could not create the {character['name']} character.")
    created = set(scene.objects) - existing
    rig = next((obj for obj in created if obj.type == "ARMATURE"), None)
    human = next(
        (obj for obj in created if obj.type == "MESH" and obj.data.shape_keys and obj.name.startswith("Human")),
        None,
    )
    if rig is None or human is None:
        raise RuntimeError(f"MPFB created an incomplete character for {character['name']}.")

    rig.name = f"{character['name']}.rig"
    human.name = character["name"]
    rig.location = (-0.72 if index == 0 else 0.72, 0.42, 0)
    rig.rotation_euler.z = math.radians(11 if index == 0 else -11)

    for side, mirror in (("Left", 1), ("Right", -1)):
        arm = rig.pose.bones.get(f"mixamorig:{side}Arm")
        if arm:
            arm.rotation_euler[1] = 1.1 * mirror

    FaceService.set_expression(
        human,
        {
            "jawOpen": 0.0,
            "browInnerUp": 0.0,
            "mouthSmileLeft": 0.0,
            "mouthSmileRight": 0.0,
            "eyeBlinkLeft": 0.0,
            "eyeBlinkRight": 0.0,
        },
    )
    for pose_bone in rig.pose.bones:
        pose_bone.rotation_mode = "XYZ"
    return rig, human


def _add_camera(name: str, location, focus, lens: float, focus_object):
    camera_data = bpy.data.cameras.new(name)
    camera = bpy.data.objects.new(name, camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = location
    camera.rotation_euler = (Vector(focus) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.lens = lens
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = focus_object
    camera_data.dof.aperture_fstop = 4.0
    return camera


def _set_expression(human, values: dict[str, float], frame: int):
    from bl_ext.blender_org.mpfb.services.faceservice import FaceService

    FaceService.set_expression(human, values)
    key_blocks = human.data.shape_keys.key_blocks
    for name in ("jawOpen", "browInnerUp", "mouthSmileLeft", "mouthSmileRight", "eyeBlinkLeft", "eyeBlinkRight"):
        key = key_blocks.get(f"!ex-{name}")
        if key:
            key.keyframe_insert(data_path="value", frame=frame, group="Facial performance")


def _word_opening(text: str, local_time: float, duration: float) -> float:
    words = re.findall(r"[A-Za-z']+", text)
    syllables = [max(1, len(re.findall(r"[aeiouy]+", word.lower()))) for word in words]
    total = sum(syllables)
    if not total or duration <= 0:
        return 0.0
    position = min(total - 0.001, max(0.0, local_time / duration * total))
    syllable_index = int(position)
    word_index = 0
    for index, count in enumerate(syllables):
        if syllable_index < count:
            word_index = index
            break
        syllable_index -= count
    fraction = position - int(position)
    syllabic_pulse = math.sin(math.pi * fraction) ** 0.7
    word_factor = 0.75 if words[word_index].lower() in {"a", "the", "is", "to", "and", "of"} else 1.0
    return 0.04 + 0.36 * syllabic_pulse * word_factor


def main():
    args = parse_args()
    args.dialogue_json = args.dialogue_json.resolve()
    args.frames_dir = args.frames_dir.resolve()
    payload = json.loads(args.dialogue_json.read_text(encoding="utf-8"))
    if bpy.app.version < (4, 2, 0):
        raise RuntimeError("MPFB character creation needs Blender 4.2 or newer.")
    enable_mpfb()

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
        for item in list(block):
            if item.users == 0:
                block.remove(item)

    build_bodega()
    generated = [_create_character(character, index) for index, character in enumerate(payload["characters"])]
    characters = {
        character["name"]: {"rig": generated[index][0], "human": generated[index][1]}
        for index, character in enumerate(payload["characters"])
    }

    world = bpy.data.worlds.new("Pre-dawn Queens sky")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.015, 0.024, 0.05, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.32
    bpy.context.scene.world = world

    cameras = {}
    for character in payload["characters"]:
        x = -0.72 if character["name"] == "Maya" else 0.72
        focus = (x, 0.38, 1.42)
        location = (x + (0.13 if x < 0 else -0.13), -1.82, 1.5)
        cameras[character["name"]] = _add_camera(
            f"{character['name']} close shot",
            location,
            focus,
            70,
            characters[character["name"]]["human"],
        )
    cameras["Establishing"] = _add_camera(
        "Bodega establishing shot",
        (0, -4.1, 2.05),
        (0, 0.4, 1.3),
        37,
        characters["Maya"]["human"],
    )
    cameras["Establishing"].data.dof.use_dof = False

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 8
    scene.render.resolution_x = args.render_width
    scene.render.resolution_y = args.render_height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.render.threads_mode = "FIXED"
    scene.render.threads = max(1, min(6, __import__("os").cpu_count() or 1))
    scene.view_settings.view_transform = "AgX"
    scene.camera = cameras["Maya"]

    output_path = args.frames_dir.parent / "episode_01_scene.blend"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args.frames_dir.mkdir(parents=True, exist_ok=True)
    frame_index = 0
    for dialogue_index, dialogue in enumerate(payload["dialogue"]):
        speaker = dialogue["speaker"]
        speaker_character = characters[speaker]
        listener_name = next(name for name in characters if name != speaker)
        listener_character = characters[listener_name]
        scene.camera = cameras[speaker]
        duration = dialogue["duration_seconds"]
        frame_count = dialogue["frame_count"]
        previous = frame_index

        head = speaker_character["rig"].pose.bones.get("mixamorig:Head")
        listener_head = listener_character["rig"].pose.bones.get("mixamorig:Head")
        speaker_human = speaker_character["human"]
        listener_human = listener_character["human"]
        camera = cameras[speaker]
        base_camera_x = camera.location.x

        for local_index in range(frame_count):
            frame = frame_index + local_index + 1
            local_time = local_index / payload["fps"]
            scene.frame_set(frame)
            scene.camera = (
                cameras["Establishing"]
                if dialogue_index == 0 and local_index < payload["fps"]
                else cameras[speaker]
            )
            pulse = math.sin(local_time * 3.6 + dialogue_index)
            if head:
                head.rotation_euler = (0.018 * pulse, 0.012 * math.sin(local_time * 2.1), 0.018 * pulse)
                head.keyframe_insert(data_path="rotation_euler", frame=frame, group="Dialogue head motion")
            if listener_head:
                listener_head.rotation_euler = (0.008 * math.sin(local_time * 1.7), 0, 0.012 * math.cos(local_time * 1.4))
                listener_head.keyframe_insert(data_path="rotation_euler", frame=frame, group="Listening motion")

            jaw = _word_opening(dialogue["line"], local_time, duration)
            speaking_values = {
                "jawOpen": jaw,
                "browInnerUp": 0.12 if dialogue_index in (2, 5, 6) else 0.035,
                "mouthSmileLeft": 0.025,
                "mouthSmileRight": 0.025,
                "eyeBlinkLeft": 0.55 if local_index % 23 == 20 else 0.0,
                "eyeBlinkRight": 0.55 if local_index % 23 == 20 else 0.0,
            }
            listening_values = {
                "jawOpen": 0.015,
                "browInnerUp": 0.06 if dialogue_index in (2, 5, 6) else 0.025,
                "mouthSmileLeft": 0.015,
                "mouthSmileRight": 0.015,
                "eyeBlinkLeft": 0.5 if local_index % 29 == 25 else 0.0,
                "eyeBlinkRight": 0.5 if local_index % 29 == 25 else 0.0,
            }
            _set_expression(speaker_human, speaking_values, frame)
            _set_expression(listener_human, listening_values, frame)
            camera.location.x = base_camera_x + 0.008 * math.sin(local_time * 0.8)
            scene.render.filepath = str(args.frames_dir / f"frame_{frame_index:05d}.png")
            bpy.ops.render.render(write_still=True)
            frame_index += 1

        frame_index = previous + frame_count
        print(
            f"Rendered shot {dialogue_index + 1}/{len(payload['dialogue'])}: "
            f"{speaker} — {dialogue['place']}",
            flush=True,
        )
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path))
    print(f"Rendered {frame_index} Blender frames at {args.render_width}x{args.render_height}.", flush=True)


if __name__ == "__main__":
    main()

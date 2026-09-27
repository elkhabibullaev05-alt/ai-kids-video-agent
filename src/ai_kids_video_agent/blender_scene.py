from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import textwrap
from pathlib import Path

import bpy
from mathutils import Euler


ACCENTS = {
    "weather": (0.2, 0.75, 0.92, 1),
    "data": (1.0, 0.55, 0.16, 1),
    "science": (0.4, 0.86, 0.52, 1),
    "civic": (0.8, 0.38, 0.75, 1),
    "sports": (0.96, 0.77, 0.18, 1),
    "source": (0.32, 0.78, 0.75, 1),
    "globe": (0.13, 0.47, 0.94, 1),
}
VOWELS = re.compile(r"[aeiouy]+", re.IGNORECASE)


def _arguments():
    values = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--story-plan", required=True)
    parser.add_argument("--frames-dir", required=True)
    parser.add_argument("--fps", required=True, type=int)
    parser.add_argument("--duration-seconds", type=float, default=0)
    return parser.parse_args(values)


def _material(name, color, metallic=0.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = 0.34
    return material


def _text(body, name, location, size, material):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = Euler((math.pi / 2, 0, 0), "XYZ")
    obj.data.materials.append(material)


def _clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for blocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)


def _setup_camera():
    camera_data = bpy.data.cameras.new("Portrait camera")
    camera = bpy.data.objects.new("Portrait camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0, -13, 0)
    camera.rotation_euler = Euler((math.pi / 2, 0, 0), "XYZ")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 10
    bpy.context.scene.camera = camera

    for name, location, energy, size in (
        ("Key light", (-4, -7, 5), 850, 6),
        ("Fill light", (5, -5, -3), 450, 5),
    ):
        light_data = bpy.data.lights.new(name, "AREA")
        light = bpy.data.objects.new(name, light_data)
        bpy.context.collection.objects.link(light)
        light.location = location
        light_data.energy = energy
        light_data.shape = "DISK"
        light_data.size = size

    world = bpy.data.worlds.new("News background")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.02, 0.065, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    bpy.context.scene.world = world


def _visual(category, material):
    if category == "data":
        last = None
        for index, height in enumerate((0.8, 1.35, 1.0, 2.0, 1.55)):
            bpy.ops.mesh.primitive_cube_add(size=1, location=((index - 2) * 0.63, 0, height / 2 - 0.25))
            last = bpy.context.object
            last.scale = (0.38, 0.38, height)
            last.data.materials.append(material)
        return last
    if category == "weather":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=14, location=(0, 0, 0))
        cloud = bpy.context.object
        cloud.scale = (0.9, 0.5, 0.55)
        cloud.data.materials.append(material)
        for x, z, radius in ((-0.55, 0.12, 0.52), (0.5, 0.1, 0.57), (0, 0.45, 0.58)):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=12, radius=radius, location=(x, 0, z))
            bpy.context.object.data.materials.append(material)
        return cloud
    if category == "science":
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.8, location=(0, 0, 0))
        core = bpy.context.object
        core.data.materials.append(material)
        bpy.ops.mesh.primitive_torus_add(major_radius=1.2, minor_radius=0.04, location=(0, 0, 0))
        bpy.context.object.data.materials.append(material)
        return core
    if category == "civic":
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.72, depth=1.3, location=(0, 0, 0))
        column = bpy.context.object
        column.data.materials.append(material)
        for x in (-1.05, -0.35, 0.35, 1.05):
            bpy.ops.mesh.primitive_cube_add(size=0.35, location=(x, 0, -0.35))
            bpy.context.object.data.materials.append(material)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=0.52, location=(0, 0, 0.92))
        bpy.context.object.data.materials.append(material)
        return column
    if category == "source":
        bpy.ops.mesh.primitive_cube_add(size=1.45, location=(0, 0, 0))
        card = bpy.context.object
        card.rotation_euler[1] = math.radians(12)
        card.data.materials.append(material)
        bpy.ops.mesh.primitive_torus_add(major_radius=1.05, minor_radius=0.045, location=(0, 0, 0))
        bpy.context.object.data.materials.append(material)
        return card
    if category == "sports":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.65, location=(0, 0, 0))
        ball = bpy.context.object
        ball.data.materials.append(material)
        for x in (-1.35, 1.35):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0))
            post = bpy.context.object
            post.scale = (0.08, 0.08, 1.25)
            post.data.materials.append(material)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.2))
        crossbar = bpy.context.object
        crossbar.scale = (1.43, 0.08, 0.08)
        crossbar.data.materials.append(material)
        return ball

    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, radius=0.95, location=(0, 0, 0))
    globe = bpy.context.object
    globe.data.materials.append(material)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.35, minor_radius=0.035, location=(0, 0, 0))
    bpy.context.object.data.materials.append(material)
    return globe


def _triangle(name, points, y, material):
    mesh = bpy.data.meshes.new(name)
    vertices = [(x, y, z) for x, z in points]
    mesh.from_pydata(vertices, [], [(0, 1, 2)])
    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def _ocean_animal(plan):
    kind = plan.get("species_kind", "fish")
    body_material = _material("Holographic body", plan["species_color"], 0.05)
    accent_material = _material("Holographic accent", plan["accent_color"], 0.0)
    dark_material = _material("Hologram edge", (0.035, 0.2, 0.39, 1))
    eye_material = _material("Hologram eye", (0.82, 1.0, 1.0, 1))
    objects = []

    def ellipsoid(name, location, scale, material):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=location)
        obj = bpy.context.object
        obj.name = name
        obj.scale = scale
        obj.data.materials.append(material)
        objects.append(obj)
        return obj

    def triangle(name, points, y, material):
        obj = _triangle(name, points, y, material)
        objects.append(obj)
        return obj

    if kind in {"fish", "shark"}:
        body = ellipsoid("Hologram fish", (0, 0, 0), (1.18, 0.32, 0.63), body_material)
        if kind == "shark":
            triangle("Dorsal fin", [(-0.36, 0.43), (0.12, 0.43), (-0.12, 1.03)], -0.04, accent_material)
            triangle("Tail fin", [(-1.05, 0.04), (-1.72, 0.72), (-1.63, -0.68)], 0, accent_material)
            ellipsoid("Shark gill", (-0.63, -0.305, 0.05), (0.035, 0.035, 0.32), accent_material)
        else:
            triangle("Top tail", [(-1.0, 0.08), (-1.72, 0.62), (-1.53, 0.0)], 0, accent_material)
            triangle("Bottom tail", [(-1.0, 0.02), (-1.53, 0.0), (-1.72, -0.58)], 0, accent_material)
            triangle("Dorsal fin", [(-0.45, 0.5), (0.35, 0.49), (0.0, 0.95)], 0.02, accent_material)
            triangle("Bottom fin", [(-0.2, -0.45), (0.42, -0.39), (0.28, -0.82)], 0.03, accent_material)
            for index, x in enumerate((-0.56, -0.12, 0.32)):
                ellipsoid(
                    f"Holographic stripe {index}",
                    (x, -0.305, 0),
                    (0.07, 0.045, 0.48),
                    dark_material if index % 2 == 0 else accent_material,
                )
            ellipsoid("Pectoral fin", (0.05, -0.33, -0.43), (0.37, 0.055, 0.07), accent_material)
        ellipsoid("Hologram eye", (0.84, -0.31, 0.22), (0.12, 0.055, 0.12), eye_material)
        ellipsoid("Eye center", (0.865, -0.36, 0.22), (0.045, 0.025, 0.06), dark_material)
        if "Clownfish" in plan["species"]:
            for x in (-0.65, -0.08, 0.46):
                ellipsoid("Clownfish white band", (x, -0.326, 0), (0.1, 0.035, 0.52), eye_material)
    elif kind == "seahorse":
        ellipsoid("Seahorse head", (0.3, 0, 0.75), (0.43, 0.32, 0.48), body_material)
        ellipsoid("Seahorse nose", (0.69, -0.03, 0.62), (0.34, 0.19, 0.17), accent_material)
        ellipsoid("Seahorse body", (0.08, 0, 0.0), (0.42, 0.28, 0.78), body_material)
        for index in range(4):
            ellipsoid("Seahorse armor", (0.0, -0.26, 0.4 - index * 0.26), (0.36, 0.08, 0.055), accent_material)
        for index in range(5):
            z = -0.45 - index * 0.2
            ellipsoid("Seahorse curled tail", (-0.05 - 0.13 * index, 0, z), (0.2, 0.19, 0.12), body_material)
        ellipsoid("Hologram eye", (0.4, -0.295, 0.91), (0.095, 0.045, 0.09), eye_material)
        triangle("Seahorse crest", [(-0.05, 1.0), (0.35, 1.12), (0.18, 0.76)], 0.02, accent_material)
    elif kind == "jellyfish":
        ellipsoid("Jellyfish bell", (0, 0, 0.35), (0.92, 0.45, 0.58), body_material)
        for index in range(7):
            x = -0.7 + index * 0.23
            ellipsoid("Jellyfish tentacle", (x, 0.02, -0.58 - 0.1 * (index % 3)), (0.045, 0.06, 0.62), accent_material)
        for x in (-0.4, 0.0, 0.4):
            ellipsoid("Jellyfish glow spot", (x, -0.43, 0.42), (0.08, 0.04, 0.08), eye_material)
    elif kind == "ray":
        ellipsoid("Manta body", (0, 0, 0), (0.45, 0.3, 0.78), body_material)
        triangle("Left manta wing", [(0.05, 0.4), (-0.22, 0.36), (-1.7, 1.05)], 0, accent_material)
        triangle("Right manta wing", [(0.05, -0.4), (-1.7, -1.05), (-0.22, -0.36)], 0, accent_material)
        triangle("Manta tail", [(-0.25, -0.1), (-1.35, 0.06), (-1.28, -0.06)], 0, dark_material)
        for x in (-0.18, 0.18):
            ellipsoid("Manta eye", (x, -0.29, 0.35), (0.065, 0.04, 0.07), eye_material)
    elif kind == "turtle":
        ellipsoid("Turtle shell", (0, 0, 0.1), (0.9, 0.45, 0.57), body_material)
        ellipsoid("Turtle shell center", (0, -0.43, 0.12), (0.58, 0.07, 0.4), accent_material)
        ellipsoid("Turtle head", (1.0, 0, 0.33), (0.35, 0.31, 0.32), body_material)
        for x, z, angle in ((-0.52, 0.38, -0.5), (0.38, 0.39, 0.5), (-0.52, -0.24, 0.5), (0.38, -0.23, -0.5)):
            flipper = ellipsoid("Turtle flipper", (x, 0, z), (0.46, 0.18, 0.12), accent_material)
            flipper.rotation_euler[1] = angle
        ellipsoid("Turtle eye", (1.2, -0.27, 0.41), (0.07, 0.045, 0.07), eye_material)
    elif kind == "octopus":
        ellipsoid("Octopus head", (0, 0, 0.62), (0.69, 0.45, 0.78), body_material)
        for index in range(8):
            angle = math.tau * index / 8
            x = 0.84 * math.cos(angle)
            z = -0.08 + 0.55 * math.sin(angle)
            arm = ellipsoid("Octopus arm", (x, 0.02, z), (0.56, 0.12, 0.11), accent_material)
            arm.rotation_euler[1] = -angle
        for x in (-0.25, 0.25):
            ellipsoid("Octopus eye", (x, -0.42, 0.72), (0.11, 0.05, 0.13), eye_material)
    else:
        body = ellipsoid("Hologram ocean animal", (0, 0, 0), (1.12, 0.36, 0.64), body_material)
        triangle("Tail fin", [(-0.9, 0.05), (-1.55, 0.55), (-1.48, -0.52)], 0, accent_material)
        ellipsoid("Hologram eye", (0.82, -0.35, 0.2), (0.12, 0.055, 0.12), eye_material)

    bpy.ops.mesh.primitive_torus_add(major_radius=1.92, minor_radius=0.018, location=(0, 0.16, 0))
    ring = bpy.context.object
    ring.name = "Hologram scanning ring"
    ring.scale = (1.15, 1, 0.58)
    ring.data.materials.append(accent_material)
    objects.append(ring)
    bpy.ops.mesh.primitive_torus_add(major_radius=2.16, minor_radius=0.012, location=(0, 0.18, 0))
    ring = bpy.context.object
    ring.name = "Outer hologram ring"
    ring.scale = (1.15, 1, 0.58)
    ring.data.materials.append(body_material)
    objects.append(ring)

    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = body if kind in {"fish", "shark"} else objects[0]
    bpy.ops.object.join()
    hologram = bpy.context.object
    hologram.name = "Animated 3D hologram animal"
    hologram.location.z = -0.15
    return hologram


def _ellipsoid(name, location, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24,
        ring_count=16,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    return obj


def _create_presenter(x, start_frame, end_frame):
    skin = _material("Presenter skin", (0.78, 0.48, 0.32, 1))
    hair = _material("Presenter hair", (0.12, 0.075, 0.06, 1))
    jacket = _material("Presenter jacket", (0.08, 0.19, 0.36, 1))
    shirt = _material("Presenter shirt", (0.9, 0.93, 0.98, 1))
    eyes = _material("Presenter eyes", (0.97, 0.98, 1, 1))
    pupils = _material("Presenter pupils", (0.07, 0.11, 0.17, 1))
    lips = _material("Presenter mouth", (0.12, 0.025, 0.035, 1))

    _ellipsoid("Presenter torso", (x, 0.05, -1.15), (0.82, 0.42, 1.08), jacket)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24,
        radius=0.25,
        depth=0.52,
        location=(x, 0, -0.18),
    )
    bpy.context.object.name = "Presenter neck"
    bpy.context.object.data.materials.append(skin)

    head_z = 0.88
    _ellipsoid("Presenter head", (x, 0, head_z), (0.64, 0.48, 0.76), skin)
    _ellipsoid("Presenter hair", (x, 0.015, 1.32), (0.65, 0.49, 0.36), hair)
    for eye_x in (x - 0.23, x + 0.23):
        _ellipsoid("Eye", (eye_x, -0.43, 0.99), (0.105, 0.055, 0.075), eyes)
        _ellipsoid("Pupil", (eye_x, -0.48, 0.99), (0.042, 0.025, 0.047), pupils)
        _ellipsoid("Eyebrow", (eye_x, -0.425, 1.13), (0.12, 0.04, 0.035), hair)
    _ellipsoid("Presenter nose", (x, -0.52, 0.76), (0.085, 0.09, 0.14), skin)
    mouth = _ellipsoid(
        "Talking mouth",
        (x, -0.47, 0.55),
        (0.19, 0.045, 0.025),
        lips,
    )
    _ellipsoid("Shirt", (x, -0.34, -0.3), (0.29, 0.09, 0.42), shirt)
    _ellipsoid("Tie", (x, -0.445, -0.51), (0.075, 0.035, 0.3), lips)

    for frame, angle in ((start_frame, -0.025), (end_frame, 0.025)):
        mouth.rotation_euler[1] = angle
        mouth.keyframe_insert(data_path="rotation_euler", frame=frame)
    return mouth


def _animate_mouth(mouth, segments, start_frame, frames, fps):
    word_lists = [
        re.findall(r"[A-Za-z0-9']+", segment.get("narration", ""))
        for segment in segments
    ]
    word_lists = [words or [" "] for words in word_lists]
    word_counts = [len(words) for words in word_lists]
    total_words = sum(word_counts)
    segment_durations = [frames * count / total_words for count in word_counts]
    segment_starts = []
    elapsed = 0.0
    for duration in segment_durations:
        segment_starts.append(elapsed)
        elapsed += duration

    for offset in range(frames):
        time_in_scene = offset + 0.5
        scene_index = next(
            (
                index
                for index, duration in enumerate(segment_durations)
                if time_in_scene < sum(segment_durations[: index + 1])
            ),
            len(segments) - 1,
        )
        local_time = time_in_scene - segment_starts[scene_index]
        words = word_lists[scene_index]
        duration_per_word = segment_durations[scene_index] / len(words)
        word_position = min(int(local_time / duration_per_word), len(words) - 1)
        word = words[word_position]
        word_phase = (local_time / duration_per_word) % 1.0
        syllables = max(1, len(VOWELS.findall(word)))
        syllable_phase = (word_phase * syllables) % 1.0
        mouth_open = (
            0.028 + 0.11 * math.sin(math.pi * syllable_phase)
            if syllable_phase < 0.82 and word.strip()
            else 0.025
        )
        mouth.scale = (0.19, 0.045, mouth_open)
        mouth.keyframe_insert(data_path="scale", frame=start_frame + offset)


def _category(segment):
    visual = segment.get("visual", "").lower()
    scene = segment.get("scene", "").lower()
    if "source card" in visual or ("check" in scene and "source" in scene):
        return "source"
    text = visual + " " + scene
    if any(word in text for word in ("football", "soccer", "sports", "match", "stadium", "f1")):
        return "sports"
    if any(word in text for word in ("weather", "storm", "climate", "cloud", "rain")):
        return "weather"
    if any(word in text for word in ("chart", "data", "market", "money", "graph")):
        return "data"
    if any(word in text for word in ("science", "space", "research", "technology", "health")):
        return "science"
    if any(word in text for word in ("government", "election", "city", "civic", "law")):
        return "civic"
    return "globe"


def _draw_scene(plan, segment, index, start_frame, frames, output_dir, fps):
    _clear_scene()
    _setup_camera()
    accent = _material("Scene accent", ACCENTS[_category(segment)], 0.12)
    white = _material("Headline text", (0.93, 0.97, 1, 1))
    muted = _material("Source text", (0.46, 0.73, 0.94, 1))
    if plan.get("format") == "hologram_aquarium":
        shape = _ocean_animal(plan)
        _text(plan.get("channel_brand", "NEON TIDE"), "Show brand", (0, 0.25, 4.12), 0.25, muted)
        caption = segment.get("scene") or plan["headline"]
        caption_lines = textwrap.wrap(caption.upper(), width=25)[:2]
        for line_index, line in enumerate(caption_lines):
            _text(line, "Show caption", (0, 0.2, 3.42 - line_index * 0.4), 0.36, white)
        for index in range(18):
            phase = (index * 0.61803398875) % 1
            x = -4.0 + phase * 8
            z = -3.8 + ((index * 37) % 71) / 10
            obj = _ellipsoid(
                f"Floating hologram mote {index}",
                (x, 0.12, z),
                (0.018 + (index % 3) * 0.008, 0.015, 0.03 + (index % 4) * 0.014),
                accent if index % 3 else white,
            )
            obj.keyframe_insert(data_path="location", frame=start_frame)
            obj.location.z = z + 0.65
            obj.keyframe_insert(data_path="location", frame=start_frame + frames - 1)
        _text("HOLOGRAM OCEAN", "Show type", (0, 0.2, -3.34), 0.2, muted)
        _text(plan["species"].upper(), "Species label", (0, 0.2, -3.82), 0.43, white)

        end_frame = start_frame + frames - 1
        shape.rotation_euler[2] = -0.045
        shape.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        shape.rotation_euler[2] = 0.045
        shape.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        shape.location.x = -0.16
        shape.keyframe_insert(data_path="location", frame=start_frame)
        shape.location.x = 0.16
        shape.keyframe_insert(data_path="location", frame=end_frame)
        shape.location.z = -0.2
        shape.keyframe_insert(data_path="location", frame=start_frame)
        shape.location.z = 0.2
        shape.keyframe_insert(data_path="location", frame=end_frame)
        for frame in range(start_frame, end_frame + 1):
            bpy.context.scene.frame_set(frame)
            bpy.context.scene.render.filepath = str(output_dir / f"frame_{frame:05d}.png")
            bpy.ops.render.render(write_still=True)
        return

    previous_objects = set(bpy.context.scene.objects)
    shape = _visual(_category(segment), accent)
    visual_objects = [
        obj for obj in bpy.context.scene.objects if obj not in previous_objects
    ]
    for obj in visual_objects:
        obj.location.x -= 1.18
        obj.scale *= 0.58
    mouth = _create_presenter(1.03, start_frame, start_frame + frames - 1)
    _animate_mouth(mouth, plan["script"], start_frame, frames, fps)

    _text("WORLD NEWS", "Section", (0, 0.25, 4.15), 0.28, muted)
    caption = (segment.get("scene") or f"Scene {index + 1}").upper()
    caption_lines = textwrap.wrap(caption, width=24)[:2]
    for line_index, line in enumerate(caption_lines):
        _text(line, "Scene caption", (0, 0.2, 3.55 - line_index * 0.4), 0.34, white)
    headline = textwrap.wrap(plan["headline"], width=34)[:2]
    for line_index, line in enumerate(headline):
        _text(line, "Story headline", (0, 0.2, -2.65 - line_index * 0.36), 0.23, white)
    for line_index, line in enumerate(textwrap.wrap(segment.get("narration", ""), width=38)[:3]):
        _text(line, "Narration caption", (0, 0.2, -3.55 - line_index * 0.24), 0.145, muted)
    _text(plan["source_name"][:38], "Source credit", (0, 0.2, -4.48), 0.15, muted)

    end_frame = start_frame + frames - 1
    shape.rotation_euler[2] = 0
    shape.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    shape.rotation_euler[2] = math.tau
    shape.keyframe_insert(data_path="rotation_euler", frame=end_frame)
    shape.scale = (0.8, 0.8, 0.8)
    shape.keyframe_insert(data_path="scale", frame=start_frame)
    shape.scale = (1.08, 1.08, 1.08)
    shape.keyframe_insert(data_path="scale", frame=end_frame)

    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = str(output_dir / f"frame_{frame:05d}.png")
        bpy.ops.render.render(write_still=True)


def main():
    args = _arguments()
    plan = json.loads(Path(args.story_plan).read_text(encoding="utf-8"))
    segments = plan["script"]
    if not segments:
        raise ValueError("No script scenes in story plan.")
    output_dir = Path(args.frames_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    engines = bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys()
    scene.render.engine = "BLENDER_WORKBENCH" if "BLENDER_WORKBENCH" in engines else "BLENDER_EEVEE"
    scene.render.resolution_x = 360
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.render.fps = args.fps
    scene.render.threads_mode = "FIXED"
    scene.render.threads = max(1, min(8, os.cpu_count() or 1))
    scene.view_settings.view_transform = "Standard"
    if scene.render.engine == "BLENDER_WORKBENCH":
        scene.display.shading.light = "STUDIO"
        scene.display.shading.color_type = "MATERIAL"
        scene.display.shading.background_type = "WORLD"
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True

    narration_counts = [max(1, len(segment.get("narration", "").split())) for segment in segments]
    total_words = sum(narration_counts)
    duration_seconds = args.duration_seconds or plan.get("duration_seconds", 35)
    minimum_duration_frames = args.fps * len(segments)
    if args.duration_seconds > 0:
        total_frames = max(minimum_duration_frames, math.ceil(duration_seconds * args.fps))
    else:
        total_frames = max(args.fps * 30, math.ceil(duration_seconds * args.fps))
    extra_frames = total_frames - args.fps * len(segments)
    start_frame = 1
    for index, (segment, words) in enumerate(zip(segments, narration_counts)):
        frames = (
            total_frames - (start_frame - 1)
            if index == len(segments) - 1
            else args.fps + math.floor(extra_frames * words / total_words)
        )
        print(f"Rendering Blender scene {index + 1}/{len(segments)}: {segment['scene']}", flush=True)
        _draw_scene(plan, segment, index, start_frame, frames, output_dir, args.fps)
        start_frame += frames


if __name__ == "__main__":
    main()

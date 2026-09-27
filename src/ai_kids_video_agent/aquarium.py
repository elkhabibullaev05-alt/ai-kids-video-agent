from __future__ import annotations

import hashlib
import json
import math
import random
import struct
import wave
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class OceanAnimal:
    name: str
    color: tuple[float, float, float, float]
    accent: tuple[float, float, float, float]
    kind: str


OCEAN_ANIMALS = (
    OceanAnimal("Clownfish", (0.08, 0.83, 1.0, 1), (1.0, 0.48, 0.15, 1), "fish"),
    OceanAnimal("Blue Tang", (0.12, 0.52, 1.0, 1), (0.25, 0.95, 0.91, 1), "fish"),
    OceanAnimal("Mandarinfish", (0.24, 0.9, 0.77, 1), (1.0, 0.48, 0.15, 1), "fish"),
    OceanAnimal("Lionfish", (0.18, 0.79, 1.0, 1), (1.0, 0.53, 0.32, 1), "fish"),
    OceanAnimal("Betta Fish", (0.14, 0.95, 0.9, 1), (0.67, 0.36, 1.0, 1), "fish"),
    OceanAnimal("Moorish Idol", (0.12, 0.88, 1.0, 1), (1.0, 0.85, 0.3, 1), "fish"),
    OceanAnimal("Seahorse", (0.22, 1.0, 0.73, 1), (1.0, 0.83, 0.33, 1), "seahorse"),
    OceanAnimal("Jellyfish", (0.28, 0.83, 1.0, 1), (0.83, 0.48, 1.0, 1), "jellyfish"),
    OceanAnimal("Manta Ray", (0.14, 0.58, 1.0, 1), (0.32, 0.96, 0.88, 1), "ray"),
    OceanAnimal("Sea Turtle", (0.22, 0.92, 0.64, 1), (0.93, 0.8, 0.36, 1), "turtle"),
    OceanAnimal("Octopus", (0.72, 0.4, 1.0, 1), (0.32, 0.88, 1.0, 1), "octopus"),
    OceanAnimal("Whale Shark", (0.18, 0.65, 1.0, 1), (0.55, 0.95, 1.0, 1), "shark"),
)

SLOTS = ((9, "morning"), (14, "afternoon"), (18, "evening"))
VIDEO_DURATION_SECONDS = 20
SAMPLE_RATE = 22050
CHANNEL_BRAND = "OCEAN GLOW"


def animal_for_slot(day: date, slot: str) -> OceanAnimal:
    slot_index = {"morning": 0, "afternoon": 1, "evening": 2}.get(slot)
    if slot_index is None:
        raise ValueError("Slot must be 'morning', 'afternoon', or 'evening'.")
    index = (day.toordinal() * 3 + slot_index * (len(OCEAN_ANIMALS) // 3)) % len(OCEAN_ANIMALS)
    return OCEAN_ANIMALS[index]


def make_video_plan(animal: OceanAnimal) -> dict:
    title = f"{animal.name} in a Neon Hologram Ocean #Shorts"
    return {
        "channel_brand": CHANNEL_BRAND,
        "format": "hologram_aquarium",
        "species": animal.name,
        "species_kind": animal.kind,
        "species_color": animal.color,
        "accent_color": animal.accent,
        "headline": f"Meet the {animal.name}",
        "source_name": "Original 3D ocean art",
        "source_url": "",
        "duration_seconds": VIDEO_DURATION_SECONDS,
        "script": [
            {
                "scene": f"MEET THE {animal.name.upper()}",
                "narration": "",
                "visual": animal.kind,
            },
            {
                "scene": "A LIVING LIGHT SHOW",
                "narration": "",
                "visual": animal.kind,
            },
            {
                "scene": "DIVE INTO THE BLUE",
                "narration": "",
                "visual": animal.kind,
            },
        ],
        "youtube_metadata": {
            "title": title,
            "description": (
                f"Meet the {animal.name} in an original 3D hologram-ocean animation. "
                "Made with Blender and original, royalty-free ambient synth music. "
                "Stylized digital artwork, not real wildlife footage. "
                "Follow Ocean Glow for more original ocean holograms.\n\n"
                "#Shorts #Ocean #Aquarium #3DAnimation #Relaxing"
            ),
            "tags": [
                "ocean",
                "aquarium",
                "hologram",
                "3D animation",
                "relaxing",
                animal.name.lower(),
                "YouTube Shorts",
            ],
            "category_id": "15",
            "language": "en",
        },
    }


def write_video_plan(plan: dict, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def synthesize_ambient_music(
    path: str | Path,
    animal_name: str,
    duration_seconds: int = VIDEO_DURATION_SECONDS,
) -> Path:
    if duration_seconds < 1:
        raise ValueError("Music duration must be at least one second.")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(animal_name.encode("utf-8")).digest()
    rng = random.Random(int.from_bytes(digest[:4], "big"))
    root = rng.choice((110.0, 123.47, 130.81, 146.83, 164.81))
    notes = (root, root * 1.25, root * 1.5, root * 2, root * 1.5, root * 1.25)
    frame_count = duration_seconds * SAMPLE_RATE
    fade_seconds = min(2.5, duration_seconds / 5)

    with wave.open(str(target), "wb") as audio:
        audio.setnchannels(2)
        audio.setsampwidth(2)
        audio.setframerate(SAMPLE_RATE)
        chunk = bytearray()
        for frame in range(frame_count):
            elapsed = frame / SAMPLE_RATE
            fade_in = min(1.0, elapsed / fade_seconds)
            fade_out = min(1.0, (duration_seconds - elapsed) / fade_seconds)
            envelope = max(0.0, min(fade_in, fade_out))
            beat = int(elapsed // 2)
            note = notes[beat % len(notes)]
            soft_pulse = 0.77 + 0.23 * math.sin(math.tau * elapsed / 8)
            pad = (
                0.52 * math.sin(math.tau * root * elapsed)
                + 0.24 * math.sin(math.tau * note * elapsed)
                + 0.12 * math.sin(math.tau * root * 1.5 * elapsed + 0.7)
                + 0.08 * math.sin(math.tau * root * 2.0 * elapsed + 1.1)
            )
            shimmer = 0.0
            beat_phase = elapsed % 4
            if beat_phase < 0.9:
                bubble = math.sin(math.pi * beat_phase / 0.9) ** 4
                shimmer = 0.07 * bubble * math.sin(math.tau * (680 + 90 * beat_phase) * elapsed)
            amplitude = (pad * soft_pulse + shimmer) * envelope * 0.12
            stereo = int(max(-1.0, min(1.0, amplitude)) * 32767)
            other = int(stereo * (0.97 + 0.02 * math.sin(math.tau * elapsed / 11)))
            chunk.extend(struct.pack("<hh", stereo, other))
            if len(chunk) >= 65536:
                audio.writeframesraw(chunk)
                chunk.clear()
        if chunk:
            audio.writeframesraw(chunk)
    return target

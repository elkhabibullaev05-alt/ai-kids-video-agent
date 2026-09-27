from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import wave
from dataclasses import asdict, dataclass
from pathlib import Path
from textwrap import wrap


WIDTH = 720
HEIGHT = 1280
RENDER_WIDTH = 540
RENDER_HEIGHT = 960
INPUT_FPS = 4
OUTPUT_FPS = 24
AUDIO_SAMPLE_RATE = 24000
SERIES_TITLE = "The Borough File"


@dataclass(frozen=True)
class Character:
    name: str
    age: int
    description: str
    voice: str
    voice_rate: int
    pitch: float
    gender: str
    seed: int
    hair_filter: str
    upper_clothing: str


@dataclass(frozen=True)
class Dialogue:
    speaker: str
    line: str
    place: str


CHARACTERS = (
    Character(
        "Maya",
        17,
        "A curious Astoria photographer who notices details other people miss.",
        "Microsoft Zira Desktop",
        1,
        1.08,
        "female",
        1821,
        "bob",
        "joepal_crude_t-shirt_female",
    ),
    Character(
        "Noah",
        16,
        "A thoughtful Queens bike mechanic who remembers every neighborhood story.",
        "Microsoft David Desktop",
        0,
        0.96,
        "male",
        4927,
        "short",
        "elvs_crude_t-shirt_male",
    ),
)

PILOT_DIALOGUE = (
    Dialogue("Maya", "This bodega's been shut for months. Then who turned the lights on?", "ASTORIA, QUEENS"),
    Dialogue("Noah", "Nobody. The power's cut. But that envelope is fresh.", "THE CLOSED BODEGA"),
    Dialogue("Maya", "There's a photo. That's my mom. She said she'd never met your aunt.", "A PHOTO FROM 2009"),
    Dialogue("Noah", "The date is May fourteenth, 2009. The night they both left Queens.", "A SHARED PAST"),
    Dialogue("Maya", "The note says, 'Meet where the train stops singing.'", "A MESSAGE"),
    Dialogue("Noah", "The old platform under the elevated tracks. It closed before we were born.", "THE OLD PLATFORM"),
    Dialogue("Maya", "Noah, that figure on the platform—it's wearing my mom's coat.", "TO BE CONTINUED"),
)


def series_bible() -> dict:
    return {
        "title": SERIES_TITLE,
        "format": "Open-ended, continuous realistic 3D mystery serial set in present-day Queens, New York.",
        "story_engine": (
            "Maya and Noah follow ordinary clues through their borough and uncover how their "
            "families' pasts connect. Every episode answers one small question and opens a new one."
        ),
        "characters": [asdict(character) for character in CHARACTERS],
        "visual_style": (
            "Rigged 3D human characters, close cinematic camera shots, a modeled Astoria bodega set, "
            "PBR materials, facial expressions and dialogue mouth movement."
        ),
        "voice_note": (
            "Uses installed Microsoft Zira and David desktop voices with slight pitch adjustments. "
            "They are adult system voices, not actual teen voice actors."
        ),
        "asset_note": (
            "Character generator: MPFB (GPL-3.0-or-later). MakeHuman Community base and selected "
            "hair/clothing/material assets are CC0. No paid assets are used."
        ),
        "episode_one": {
            "title": "The Envelope",
            "setting": "A shuttered bodega in Astoria, Queens, before sunrise",
            "dialogue": [asdict(beat) for beat in PILOT_DIALOGUE],
            "ending": "Cliffhanger; the story is not resolved.",
        },
    }


def _font(bold: bool, size: int):
    from PIL import ImageFont

    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    chosen = path if Path(path).is_file() else fallback
    if Path(chosen).is_file():
        return ImageFont.truetype(chosen, size)
    return ImageFont.load_default()


def _synthesize_line(dialogue: Dialogue, output_path: Path, character: Character, ffmpeg: str) -> float:
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise RuntimeError("Windows PowerShell is required for the local character voices.")

    raw_path = output_path.with_name(f"{output_path.stem}_raw.wav")
    payload = json.dumps(
        {
            "output": str(raw_path.resolve()),
            "voice": character.voice,
            "rate": character.voice_rate,
            "text": dialogue.line,
        },
        ensure_ascii=True,
    )
    command = (
        "$ErrorActionPreference = 'Stop'; "
        "$data = [Console]::In.ReadToEnd() | ConvertFrom-Json; "
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "try { $synth.SelectVoice($data.voice); $synth.Rate = $data.rate; "
        "$synth.Volume = 100; $synth.SetOutputToWaveFile($data.output); "
        "$synth.Speak($data.text) } finally { $synth.Dispose() }"
    )
    try:
        subprocess.run(
            [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(f"Could not create {character.name}'s voice with {character.voice}: {detail}") from exc

    pitch_filter = (
        f"asetrate={AUDIO_SAMPLE_RATE}*{character.pitch},"
        f"aresample={AUDIO_SAMPLE_RATE},atempo={1 / character.pitch:.6f}"
    )
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(raw_path),
            "-af",
            pitch_filter,
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ],
        check=True,
    )
    raw_path.unlink()
    with wave.open(str(output_path), "rb") as audio:
        duration = audio.getnframes() / audio.getframerate()
    if duration <= 0:
        raise RuntimeError(f"Windows produced an empty voice recording for {character.name}.")
    return duration


def _join_audio(
    paths: list[Path],
    output_path: Path,
    durations: list[float],
    frame_counts: list[int],
) -> None:
    if not paths or len(paths) != len(durations) or len(paths) != len(frame_counts):
        raise ValueError("Audio paths, line durations, and frame counts must have the same non-zero length.")
    with wave.open(str(paths[0]), "rb") as first:
        parameters = first.getparams()
    if parameters.framerate != AUDIO_SAMPLE_RATE or parameters.nchannels != 1 or parameters.sampwidth != 2:
        raise RuntimeError("Character audio must be mono 24 kHz PCM.")
    with wave.open(str(output_path), "wb") as output:
        output.setparams(parameters)
        for path, duration, frame_count in zip(paths, durations, frame_counts, strict=True):
            with wave.open(str(path), "rb") as audio:
                if audio.getparams()[:3] != parameters[:3]:
                    raise RuntimeError("Character voice recordings have incompatible audio formats.")
                output.writeframes(audio.readframes(audio.getnframes()))
            aligned_silence = max(0, frame_count / INPUT_FPS - duration)
            silence_frames = round(AUDIO_SAMPLE_RATE * aligned_silence)
            output.writeframes(b"\0" * silence_frames * parameters.sampwidth)


def _compose_captions(raw_frames: Path, final_frames: Path, frame_map: list[int]) -> None:
    from PIL import Image, ImageDraw

    final_frames.mkdir(parents=True, exist_ok=True)
    for stale_frame in final_frames.glob("frame_*.png"):
        if stale_frame.is_file():
            stale_frame.unlink()
    label_font = _font(True, 28)
    caption_font = _font(False, 34)
    character_colors = {"Maya": (211, 125, 75), "Noah": (63, 116, 174)}

    for frame_index, dialogue_index in enumerate(frame_map):
        source = raw_frames / f"frame_{frame_index:05d}.png"
        if not source.is_file():
            raise FileNotFoundError(f"Blender did not render expected frame {source}")
        with Image.open(source) as image:
            frame = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        dialogue = PILOT_DIALOGUE[dialogue_index]
        speaker = dialogue.speaker
        color = character_colors[speaker]

        if frame_index < INPUT_FPS * 3:
            draw.rounded_rectangle((36, 38, 684, 89), radius=17, fill=(9, 15, 28, 192))
            draw.text((56, 49), "THE BOROUGH FILE  /  EPISODE 01", font=label_font, fill=(241, 225, 195, 255))

        draw.rounded_rectangle((35, 1018, 685, 1220), radius=25, fill=(7, 12, 20, 204))
        draw.rounded_rectangle((57, 1040, 185, 1082), radius=13, fill=(*color, 255))
        draw.text((121, 1060), speaker.upper(), font=label_font, fill=(255, 255, 255, 255), anchor="mm")
        lines = wrap(dialogue.line, width=45)
        if len(lines) > 3:
            lines = wrap(dialogue.line, width=55)
        y = 1094
        for line in lines[:3]:
            draw.text((59, y), line, font=caption_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 180))
            y += 42
        frame = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")
        frame.save(final_frames / f"frame_{frame_index:05d}.png", optimize=True)


def render_pilot(output_dir: Path, ffmpeg: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "series_bible.json").write_text(
        json.dumps(series_bible(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    audio_paths: list[Path] = []
    durations: list[float] = []
    for index, dialogue in enumerate(PILOT_DIALOGUE):
        character = next(item for item in CHARACTERS if item.name == dialogue.speaker)
        path = audio_dir / f"line_{index + 1:02d}.wav"
        print(f"[voice {index + 1}/{len(PILOT_DIALOGUE)}] {character.name}: {dialogue.line}", flush=True)
        durations.append(_synthesize_line(dialogue, path, character, ffmpeg))
        audio_paths.append(path)

    frame_counts = [max(4, math.ceil((duration + 0.38) * INPUT_FPS)) for duration in durations]
    frame_map = [
        dialogue_index
        for dialogue_index, frame_count in enumerate(frame_counts)
        for _ in range(frame_count)
    ]
    narration_path = output_dir / "episode_01_dialogue.wav"
    _join_audio(audio_paths, narration_path, durations, frame_counts)

    dialogue_payload = [
        {
            **asdict(dialogue),
            "duration_seconds": duration,
            "frame_count": frame_count,
        }
        for dialogue, duration, frame_count in zip(PILOT_DIALOGUE, durations, frame_counts, strict=True)
    ]
    dialogue_json = output_dir / "episode_01_dialogue.json"
    dialogue_json.write_text(
        json.dumps(
            {
                "series": SERIES_TITLE,
                "episode": 1,
                "title": "The Envelope",
                "fps": INPUT_FPS,
                "render_size": [RENDER_WIDTH, RENDER_HEIGHT],
                "characters": [asdict(character) for character in CHARACTERS],
                "dialogue": dialogue_payload,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    blender = os.environ.get("BLENDER_PATH") or shutil.which("blender")
    if not blender:
        candidate = Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
        if candidate.is_file():
            blender = str(candidate)
    if not blender or not Path(blender).is_file():
        raise FileNotFoundError("Blender 5.2 or newer is required. Install Blender or set BLENDER_PATH.")

    repository_root = Path(__file__).resolve().parents[2]
    blender_script = repository_root / "tools" / "render_borough_scene.py"
    raw_frames = output_dir / "frames_raw"
    raw_frames.mkdir(exist_ok=True)
    blender_command = [
        blender,
        "--background",
        "--python",
        str(blender_script),
        "--",
        "--dialogue-json",
        str(dialogue_json.resolve()),
        "--frames-dir",
        str(raw_frames.resolve()),
        "--render-width",
        str(RENDER_WIDTH),
        "--render-height",
        str(RENDER_HEIGHT),
    ]
    print("[3/5] Building rigged 3D characters and the Astoria bodega set in Blender...", flush=True)
    subprocess.run(blender_command, check=True)

    final_frames = output_dir / "frames"
    print("[4/5] Upscaling frames and adding crisp English subtitles...", flush=True)
    _compose_captions(raw_frames, final_frames, frame_map)
    video_path = output_dir / "the_borough_file_episode_01.mp4"
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-framerate",
        str(INPUT_FPS),
        "-i",
        str(final_frames / "frame_%05d.png"),
        "-i",
        str(narration_path),
        "-vf",
        f"minterpolate=fps={OUTPUT_FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir,format=yuv420p",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        "-c:v",
        "libx264",
        "-profile:v",
        "high",
        "-level:v",
        "4.1",
        "-preset",
        "medium",
        "-crf",
        "19",
        "-r",
        str(OUTPUT_FPS),
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-ar",
        "44100",
        "-movflags",
        "+faststart",
        str(video_path),
    ]
    print("[5/5] Interpolating motion and encoding the 720p vertical episode...", flush=True)
    subprocess.run(command, check=True)
    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg finished without creating the episode video.")
    return video_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the first cinematic 3D episode of The Borough File.")
    parser.add_argument("--output-dir", type=Path, default=Path("output/borough-file"))
    args = parser.parse_args()
    if sys.platform != "win32":
        raise RuntimeError("The character voices and current render setup require Windows.")
    try:
        import imageio_ffmpeg

        ffmpeg = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError('Install the render extra with: python -m pip install -e ".[render,automation]"') from exc
    video = render_pilot(args.output_dir, ffmpeg)
    print(f"Episode ready (not uploaded): {video.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

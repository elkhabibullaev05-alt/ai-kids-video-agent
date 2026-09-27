from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import wave
from dataclasses import asdict, dataclass
from pathlib import Path
from textwrap import wrap


WIDTH = 720
HEIGHT = 1280
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
    jacket: tuple[int, int, int]
    hair: tuple[int, int, int]
    skin: tuple[int, int, int]


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
        (205, 114, 58),
        (48, 34, 30),
        (229, 181, 145),
    ),
    Character(
        "Noah",
        16,
        "A thoughtful Queens bike mechanic who remembers every neighborhood story.",
        "Microsoft David Desktop",
        0,
        0.96,
        (53, 91, 139),
        (40, 32, 27),
        (169, 120, 91),
    ),
)

PILOT_DIALOGUE = (
    Dialogue("Maya", "The bodega was locked before sunrise. Mom says it is just paperwork.", "ASTORIA, QUEENS"),
    Dialogue("Noah", "Then why was this envelope taped under the counter?", "A CLOSED CORNER STORE"),
    Dialogue("Maya", "That is my mother in this photo. But it was taken in 2009.", "THE ENVELOPE"),
    Dialogue("Noah", "My aunt is there too. She left Queens that summer, and nobody says why.", "A NAME FROM THE PAST"),
    Dialogue("Maya", "The note says, tomorrow, the old ferry landing. That is all.", "A MESSAGE"),
    Dialogue("Noah", "Maya, look. Someone wrote your name here. The ink is still wet.", "SOMEONE WAS HERE"),
    Dialogue("Maya", "Then we go together. But if they know we are looking, we need to know who they are.", "TO BE CONTINUED"),
)


def series_bible() -> dict:
    return {
        "title": SERIES_TITLE,
        "format": "Open-ended, continuous animated mystery set in present-day Queens, New York.",
        "story_engine": (
            "Maya and Noah follow ordinary clues through their borough and uncover how their "
            "families' pasts connect. Every episode answers one small question and opens a new one."
        ),
        "characters": [asdict(character) for character in CHARACTERS],
        "visual_style": "Original illustrated 2D animation with New York street details and readable dialogue.",
        "voice_note": (
            "Uses the closest installed Windows voices (Zira for Maya, David for Noah), with a "
            "slight pitch adjustment. These are adult system voices, not recordings of teenagers."
        ),
        "episode_one": {
            "title": "The Envelope",
            "setting": "Astoria, Queens, present day",
            "dialogue": [asdict(beat) for beat in PILOT_DIALOGUE],
            "ending": "Cliffhanger; the story is not resolved.",
        },
    }


def _font(bold: bool, size: int):
    from PIL import ImageFont

    names = (
        (r"C:\Windows\Fonts\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        if bold
        else (r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    )
    for name in names:
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def _draw_city_background(draw, scene_index: int, place: str) -> None:
    sky_top = (14, 27, 54)
    sky_bottom = (72, 93, 119)
    for y in range(HEIGHT):
        amount = y / HEIGHT
        color = tuple(round(a * (1 - amount) + b * amount) for a, b in zip(sky_top, sky_bottom))
        draw.line((0, y, WIDTH, y), fill=color)

    draw.ellipse((515, 100, 580, 165), fill=(241, 214, 167))
    building_colors = ((44, 55, 76), (60, 66, 80), (72, 69, 78), (48, 61, 78))
    for index, x in enumerate(range(-35, WIDTH + 40, 88)):
        height = 245 + (index * 79 % 190)
        top = 720 - height
        draw.rectangle((x, top, x + 92, 745), fill=building_colors[index % len(building_colors)])
        for wx in range(x + 12, x + 82, 24):
            for wy in range(top + 20, 700, 38):
                if ((wx + wy + scene_index * 11) // 7) % 3:
                    draw.rectangle((wx, wy, wx + 10, wy + 17), fill=(224, 184, 112))

    if scene_index == 0:
        draw.rectangle((0, 565, WIDTH, 617), fill=(27, 35, 49))
        draw.rectangle((0, 616, WIDTH, 636), fill=(132, 143, 150))
        for x in range(-40, WIDTH, 105):
            draw.line((x, 565, x + 58, 616), fill=(149, 159, 164), width=8)
        draw.rectangle((47, 425, 190, 490), fill=(20, 111, 106))
        draw.text((63, 441), "ASTORIA", font=_font(True, 25), fill=(255, 249, 225))
        draw.rectangle((0, 744, WIDTH, HEIGHT), fill=(45, 48, 57))
        draw.line((0, 1095, WIDTH, 1065), fill=(241, 194, 91), width=7)
        draw.polygon(((0, 1130), (720, 1060), (720, 1280), (0, 1280)), fill=(35, 42, 52))
    elif scene_index in (1, 2, 3):
        draw.rectangle((55, 320, 665, 780), fill=(43, 39, 43), outline=(199, 158, 91), width=8)
        draw.rectangle((78, 344, 642, 760), fill=(29, 41, 49))
        draw.rectangle((88, 366, 632, 411), fill=(151, 87, 54))
        draw.text((111, 374), "CORNER DELI", font=_font(True, 24), fill=(255, 238, 196))
        for x in range(105, 626, 76):
            draw.rectangle((x, 440, x + 54, 575), fill=(77, 96, 85), outline=(223, 187, 123), width=3)
        draw.rectangle((0, 746, WIDTH, HEIGHT), fill=(43, 46, 53))
        draw.line((0, 1080, WIDTH, 1080), fill=(217, 177, 105), width=5)
        draw.rounded_rectangle((270, 700, 451, 780), radius=9, fill=(99, 67, 46), outline=(197, 151, 96), width=4)
        if scene_index == 2:
            draw.rounded_rectangle((277, 664, 445, 699), radius=5, fill=(224, 204, 159), outline=(78, 56, 39), width=3)
            draw.rectangle((291, 672, 430, 691), fill=(220, 231, 216), outline=(52, 67, 62), width=2)
    else:
        draw.rectangle((0, 746, WIDTH, HEIGHT), fill=(40, 50, 62))
        draw.line((80, 810, 645, 780), fill=(205, 212, 213), width=5)
        draw.line((80, 835, 645, 805), fill=(205, 212, 213), width=5)
        for x in range(150, 650, 130):
            draw.line((x, 800, x - 42, 1000), fill=(221, 224, 221), width=4)
        draw.rectangle((495, 460, 630, 710), fill=(34, 47, 63), outline=(186, 168, 137), width=5)
        draw.text((506, 510), "FERRY", font=_font(True, 22), fill=(245, 226, 186))
        draw.text((506, 540), "PIER", font=_font(True, 22), fill=(245, 226, 186))

    draw.rounded_rectangle((38, 54, 682, 112), radius=20, fill=(9, 17, 34, 220))
    draw.text((60, 69), f"THE BOROUGH FILE   /   {place}", font=_font(True, 20), fill=(235, 226, 201))


def _draw_character(draw, character: Character, center_x: int, speaking: bool, highlighted: bool) -> None:
    cx = center_x
    head_y = 838
    body_top = 930
    draw.ellipse((cx - 87, body_top - 15, cx + 87, 1330), fill=(15, 23, 36))
    draw.rounded_rectangle(
        (cx - 80, body_top, cx + 80, 1270),
        radius=38,
        fill=character.jacket,
        outline=(245, 223, 184) if highlighted else (26, 33, 45),
        width=5 if highlighted else 2,
    )
    draw.polygon(((cx - 25, body_top + 2), (cx + 25, body_top + 2), (cx, body_top + 62)), fill=(220, 208, 188))
    draw.ellipse((cx - 59, head_y - 82, cx + 59, head_y + 62), fill=character.skin, outline=(31, 31, 36), width=3)
    draw.pieslice((cx - 64, head_y - 92, cx + 64, head_y + 21), 180, 360, fill=character.hair)
    draw.rectangle((cx - 61, head_y - 22, cx - 41, head_y + 1), fill=character.hair)
    draw.rectangle((cx + 41, head_y - 40, cx + 61, head_y - 7), fill=character.hair)
    draw.ellipse((cx - 28, head_y - 12, cx - 18, head_y - 2), fill=(31, 37, 41))
    draw.ellipse((cx + 18, head_y - 12, cx + 28, head_y - 2), fill=(31, 37, 41))
    if speaking:
        draw.ellipse((cx - 13, head_y + 20, cx + 13, head_y + 39), fill=(83, 37, 39))
        draw.arc((cx - 12, head_y + 21, cx + 12, head_y + 35), 5, 175, fill=(242, 178, 158), width=3)
    else:
        draw.arc((cx - 14, head_y + 14, cx + 14, head_y + 34), 10, 170, fill=(92, 47, 42), width=3)
    draw.text((cx, 1222), character.name.upper(), font=_font(True, 22), fill=(255, 245, 224), anchor="mm")


def _draw_beat_frame(beat: Dialogue, beat_index: int, frame_index: int, frame_path: Path) -> None:
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image, "RGBA")
    _draw_city_background(draw, beat_index, beat.place)
    speaker = next(character for character in CHARACTERS if character.name == beat.speaker)
    other = next(character for character in CHARACTERS if character.name != beat.speaker)
    _draw_character(draw, other, 226, False, False)
    _draw_character(draw, speaker, 500, frame_index % 2 == 0, True)

    box = (60, 155, 660, 380)
    draw.rounded_rectangle(box, radius=28, fill=(248, 246, 236, 248), outline=(26, 39, 54), width=5)
    draw.polygon(((485, 375), (535, 375), (515, 414)), fill=(248, 246, 236, 248))
    lines = wrap(beat.line, width=32)
    font = _font(True, 31)
    total_height = len(lines) * 43
    y = (box[1] + box[3] - total_height) // 2
    for line in lines:
        draw.text((box[0] + 31, y), line, font=font, fill=(23, 34, 47))
        y += 43
    draw.rounded_rectangle((72, 394, 297, 438), radius=14, fill=speaker.jacket)
    draw.text((184, 416), speaker.name.upper(), font=_font(True, 21), fill=(255, 255, 255), anchor="mm")
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(frame_path, optimize=True)


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


def render_pilot(output_dir: Path, ffmpeg: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "series_bible.json").write_text(
        json.dumps(series_bible(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "episode_01_script.json").write_text(
        json.dumps(
            {"series": SERIES_TITLE, "episode": 1, "title": "The Envelope", "dialogue": [asdict(line) for line in PILOT_DIALOGUE]},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
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
    narration_path = output_dir / "episode_01_dialogue.wav"
    _join_audio(audio_paths, narration_path, durations, frame_counts)
    frames_dir = output_dir / "frames"
    frame_index = 0
    for beat_index, (dialogue, frame_count) in enumerate(zip(PILOT_DIALOGUE, frame_counts, strict=True)):
        for local_frame in range(frame_count):
            frame_path = frames_dir / f"frame_{frame_index:05d}.png"
            _draw_beat_frame(dialogue, beat_index, local_frame, frame_path)
            frame_index += 1

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
        str(frames_dir / "frame_%05d.png"),
        "-i",
        str(narration_path),
        "-vf",
        "zoompan=z='min(zoom+0.00025,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=6:s=1080x1920:fps=24,format=yuv420p",
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
        "21",
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
    print("[video] Assembling the illustrated New York episode...", flush=True)
    subprocess.run(command, check=True)
    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg finished without creating the episode video.")
    return video_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the first episode of The Borough File.")
    parser.add_argument("--output-dir", type=Path, default=Path("output/borough-file"))
    args = parser.parse_args()
    if sys.platform != "win32":
        raise RuntimeError("The local teen-character voices currently require Windows Speech.")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        try:
            import imageio_ffmpeg

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError as exc:
            raise RuntimeError('Install the render extra with: python -m pip install -e ".[render,automation]"') from exc
    video = render_pilot(args.output_dir, ffmpeg)
    print(f"Episode ready (not uploaded): {video.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

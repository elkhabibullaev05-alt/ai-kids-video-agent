from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_executable(name: str) -> str:
    configured = os.environ.get(f"{name.upper()}_PATH")
    executable = configured or shutil.which(name)
    if executable is None and name == "ffmpeg":
        try:
            import imageio_ffmpeg
        except ImportError:
            pass
        else:
            executable = imageio_ffmpeg.get_ffmpeg_exe()
    if executable is None and name == "blender" and sys.platform == "win32":
        install_root = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        candidates = list((install_root / "Blender Foundation").glob("Blender */blender.exe"))
        if candidates:
            executable = str(max(candidates, key=lambda path: path.stat().st_mtime))
    if executable is None or not Path(executable).is_file():
        if name == "ffmpeg":
            fix = "Install with `python -m pip install -e \".[render]\"`, add it to PATH, or set FFMPEG_PATH."
        elif name == "blender":
            fix = "Add Blender to PATH or set BLENDER_PATH to blender.exe."
        else:
            fix = f"Install {name} and add it to PATH."
        raise FileNotFoundError(
            f"Required executable '{name}' was not found. {fix}"
        )
    return str(Path(executable))


def render_blender_scene(
    story_plan_path: str | Path,
    frames_dir: str | Path,
    fps: int = 24,
    duration_seconds: float | None = None,
) -> str:
    blender = ensure_executable("blender")
    manifest = Path(story_plan_path).resolve()
    output = Path(frames_dir).resolve()
    if not manifest.is_file():
        raise FileNotFoundError(f"Story plan not found: {manifest}")
    if fps < 1:
        raise ValueError("FPS must be at least 1.")
    if duration_seconds is not None and duration_seconds <= 0:
        raise ValueError("Audio duration must be positive.")
    output.mkdir(parents=True, exist_ok=True)
    renderer = Path(__file__).with_name("blender_scene.py")
    subprocess.run(
        [
            blender,
            "--background",
            "--python-exit-code",
            "1",
            "--python",
            str(renderer),
            "--",
            "--story-plan",
            str(manifest),
            "--frames-dir",
            str(output),
            "--fps",
            str(fps),
            "--duration-seconds",
            str(duration_seconds or 0),
        ],
        check=True,
    )
    return str(output)


def _encode_frames(
    ffmpeg: str,
    frames_dir: Path,
    output: Path,
    fps: int,
    input_fps: int,
    audio_path: Path | None = None,
) -> None:
    filters = []
    if input_fps != fps:
        filters.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir")
    filters.append(
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
    )
    command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-framerate",
            str(input_fps),
            "-start_number",
            "1",
            "-i",
            str(frames_dir / "frame_%05d.png"),
    ]
    if audio_path is not None:
        if not audio_path.is_file():
            raise FileNotFoundError(f"Narration audio not found: {audio_path}")
        command.extend(["-i", str(audio_path)])
    command.extend([
            "-vf",
            ",".join(filters),
    ])
    if audio_path is not None:
        command.extend(["-map", "0:v:0", "-map", "1:a:0"])
    command.extend([
            "-c:v",
            "libx264",
            "-r",
            str(fps),
            "-movflags",
            "+faststart",
    ])
    if audio_path is not None:
        command.extend(["-c:a", "aac", "-b:a", "128k", "-shortest"])
    else:
        command.append("-an")
    command.append(str(output))
    subprocess.run(command, check=True)


def stitch_vertical_video(
    clips: list[str],
    output_path: str | Path,
    fps: int = 24,
    input_fps: int | None = None,
    audio_path: str | Path | None = None,
) -> str:
    ffmpeg = ensure_executable("ffmpeg")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not clips:
        raise ValueError("No rendered frames provided for video assembly.")
    source_fps = input_fps or fps
    if fps < 1 or source_fps < 1 or source_fps > fps:
        raise ValueError("FPS must be positive and the input FPS cannot exceed the output FPS.")

    frames_dir = Path(clips[0])
    if len(clips) == 1 and frames_dir.is_dir():
        _encode_frames(
            ffmpeg,
            frames_dir,
            output,
            fps,
            source_fps,
            Path(audio_path).resolve() if audio_path is not None else None,
        )
        return str(output)

    for clip in clips:
        if not Path(clip).is_file():
            raise FileNotFoundError(f"Rendered clip not found: {clip}")
    filter_parts = [
        f"[{idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{idx}]"
        for idx, _ in enumerate(clips)
    ]
    concat_inputs = "".join(f"[v{idx}]" for idx in range(len(clips)))
    filter_string = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(clips)}:v=1:a=0[outv]"
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    for clip in clips:
        command += ["-i", clip]
    command += [
        "-filter_complex",
        filter_string,
        "-map",
        "[outv]",
        "-an",
        "-c:v",
        "libx264",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)
    return str(output)

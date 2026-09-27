from __future__ import annotations

import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

from .story import StoryPlan


DEFAULT_VOICE = "Microsoft Zira Desktop"


def synthesize_speech(
    plan: StoryPlan,
    output_path: str | Path,
    voice: str = DEFAULT_VOICE,
) -> float:
    if sys.platform != "win32":
        raise RuntimeError(
            "Local English narration currently requires Windows Speech. "
            "Use this workflow on Windows or configure an online TTS provider."
        )
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise FileNotFoundError("Windows PowerShell is required for local text-to-speech.")

    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    narration = " ".join(segment.narration for segment in plan.script)
    payload = json.dumps(
        {"output": str(target), "voice": voice, "text": narration},
        ensure_ascii=True,
    )
    command = (
        "$ErrorActionPreference = 'Stop'; "
        "$data = [Console]::In.ReadToEnd() | ConvertFrom-Json; "
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "try { "
        "$synth.SelectVoice($data.voice); "
        "$synth.Rate = 0; "
        "$synth.Volume = 100; "
        "$synth.SetOutputToWaveFile($data.output); "
        "$synth.Speak($data.text); "
        "} finally { $synth.Dispose() }"
    )
    try:
        subprocess.run(
            [
                powershell,
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(f"Windows could not synthesize narration with {voice}: {detail}") from exc

    if not target.is_file() or target.stat().st_size < 44:
        raise RuntimeError(f"Text-to-speech did not create a valid WAV file at {target}.")
    try:
        with wave.open(str(target), "rb") as audio:
            duration = audio.getnframes() / audio.getframerate()
    except (wave.Error, ZeroDivisionError) as exc:
        raise RuntimeError(f"Windows text-to-speech created an invalid WAV file: {exc}") from exc
    if duration <= 0:
        raise RuntimeError("Windows text-to-speech produced an empty recording.")
    return duration

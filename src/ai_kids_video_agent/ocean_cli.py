from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .aquarium import (
    OCEAN_ANIMALS,
    SLOTS,
    animal_for_slot,
    make_video_plan,
    synthesize_ambient_music,
    write_video_plan,
)
from .render import render_blender_scene, stitch_vertical_video
from .telegram_notify import configure_telegram, send_telegram_notification
from .youtube import (
    TASK_NAME,
    YouTubeSetupError,
    authorize_youtube,
    install_daily_task,
    publish_time,
    remove_daily_task,
    upload_scheduled_video,
    youtube_service,
)


def _prepare_video(
    plan: dict,
    output_dir: Path,
    name: str,
    fps: int,
) -> Path:
    plan_path = write_video_plan(plan, output_dir / f"{name}.json")
    music_path = synthesize_ambient_music(
        output_dir / f"{name}_music.wav",
        plan["species"],
        plan["duration_seconds"],
    )
    frames_dir = output_dir / "frames" / f"{name}_{uuid.uuid4().hex[:8]}"
    render_fps = min(fps, 3)
    print(f"Rendering {plan['species']} hologram animation in Blender...", flush=True)
    render_blender_scene(
        plan_path,
        frames_dir,
        fps=render_fps,
        duration_seconds=plan["duration_seconds"],
    )
    video_path = output_dir / f"{name}.mp4"
    print("Assembling vertical video with original ambient music in FFmpeg...", flush=True)
    stitch_vertical_video(
        [str(frames_dir)],
        video_path,
        fps=fps,
        input_fps=render_fps,
        audio_path=music_path,
    )
    return video_path


def create_preview(output_dir: Path, selected_day: date, slot: str, fps: int) -> Path:
    animal = animal_for_slot(selected_day, slot)
    output_dir.mkdir(parents=True, exist_ok=True)
    name = f"ocean_{selected_day.isoformat()}_{slot}"
    print(f"[preview] Creating an original hologram aquarium Short: {animal.name}", flush=True)
    plan = make_video_plan(animal)
    video = _prepare_video(plan, output_dir, name, fps)
    root_video = Path.cwd() / "final_short.mp4"
    if root_video.resolve() != video.resolve():
        shutil.copy2(video, root_video)
    print(f"[preview] Preview ready: {root_video}", flush=True)
    return video


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {"uploads": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise YouTubeSetupError(f"Could not read upload state at {path}: {exc}") from exc
    if not isinstance(state, dict) or not isinstance(state.get("uploads"), dict):
        raise YouTubeSetupError(f"Upload state in {path} has an invalid format.")
    return state


def _save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_daily(output_dir: Path, timezone_name: str, fps: int = 24) -> int:
    zone = ZoneInfo(timezone_name)
    now = datetime.now(zone)
    today = now.date()
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / "ocean_upload_state.json"
    state = _load_state(state_path)
    service = youtube_service()

    for hour, slot in SLOTS:
        animal = animal_for_slot(today, slot)
        publish_at = publish_time(today, hour, timezone_name)
        if publish_at <= datetime.now(zone) + timedelta(minutes=15):
            publish_at = publish_time(today + timedelta(days=1), hour, timezone_name)
            print(
                f"[schedule] The {hour:02}:00 slot has passed; scheduling {animal.name} for "
                f"{publish_at.isoformat()} instead.",
                flush=True,
            )
        entry_key = f"{publish_at.date().isoformat()}:{slot}"
        previous = state["uploads"].get(entry_key)
        if previous:
            status = previous.get("status", "unknown")
            video_id = previous.get("video_id")
            if video_id:
                print(f"[schedule] {entry_key} already uploaded: https://youtu.be/{video_id}")
            else:
                print(
                    f"[schedule] {entry_key} has a previous {status} attempt. "
                    "Skipping automatically to avoid duplicate uploads; check output/ocean_upload_state.json.",
                    flush=True,
                )
            continue

        print(
            f"[schedule] Building {animal.name} for {publish_at.strftime('%Y-%m-%d %I:%M %p ET')}...",
            flush=True,
        )
        name = f"ocean_{publish_at.date().isoformat()}_{slot}"
        plan = make_video_plan(animal)
        video_path = _prepare_video(plan, output_dir, name, fps)
        metadata_path = output_dir / f"{name}_youtube.json"
        metadata_path.write_text(
            json.dumps(plan["youtube_metadata"], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        state["uploads"][entry_key] = {
            "status": "uploading",
            "species": animal.name,
            "video": str(video_path.resolve()),
            "publish_at": publish_at.isoformat(),
            "started_at": datetime.now(zone).isoformat(),
        }
        _save_state(state_path, state)
        try:
            video_id = upload_scheduled_video(
                video_path,
                plan["youtube_metadata"],
                publish_at,
                service=service,
            )
        except Exception as exc:
            state["uploads"][entry_key]["status"] = "needs_review"
            state["uploads"][entry_key]["error"] = str(exc)
            _save_state(state_path, state)
            raise
        state["uploads"][entry_key].update(
            {
                "status": "scheduled",
                "video_id": video_id,
                "uploaded_at": datetime.now(zone).isoformat(),
            }
        )
        _save_state(state_path, state)
        print(
            f"[schedule] Scheduled {animal.name}: https://youtu.be/{video_id} "
            f"for {publish_at.isoformat()}",
            flush=True,
        )
        try:
            send_telegram_notification(
                f"✅ Ocean Glow: {animal.name} videosi YouTube’da rejalashtirildi.\n"
                f"Chiqarilish vaqti (New York): {publish_at.strftime('%Y-%m-%d %H:%M ET')}\n"
                f"https://youtu.be/{video_id}"
            )
        except RuntimeError as exc:
            print(f"[notification] Telegram xabari yuborilmadi: {exc}", file=sys.stderr, flush=True)
    return 0


def _notify_daily_failure(output_dir: Path, error: Exception) -> None:
    try:
        sent = send_telegram_notification(
            f"❌ Ocean Glow: bugungi video tayyorlash yoki rejalashtirishda xato yuz berdi.\n"
            f"Sabab: {error}\n"
            f"Jurnal: {output_dir / 'schedule.log'}"
        )
        if sent:
            print("[notification] Telegram xatosi haqida xabar yuborildi.", flush=True)
    except RuntimeError as notification_error:
        print(
            f"[notification] Xato xabari Telegram’ga yuborilmadi: {notification_error}",
            file=sys.stderr,
            flush=True,
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ocean-shorts",
        description="Create original holographic ocean Shorts, then optionally schedule them to YouTube.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    preview = commands.add_parser("preview", help="Render one sample Short locally without uploading.")
    preview.add_argument("--output-dir", type=Path, default=Path("output"))
    preview.add_argument("--date", type=date.fromisoformat, default=date.today())
    preview.add_argument("--slot", choices=("morning", "afternoon", "evening"), default="morning")
    preview.add_argument("--fps", type=int, default=24)

    authorize = commands.add_parser("authorize", help="Connect your own channel through Google's sign-in page.")
    authorize.add_argument("--client-secret", type=Path)

    commands.add_parser("telegram-setup", help="Connect a private Telegram bot for upload notifications.")

    install = commands.add_parser("install-schedule", help="Schedule three daily US-time-zone uploads.")
    install.add_argument("--output-dir", type=Path, default=Path("output"))
    install.add_argument("--timezone", default="America/New_York")

    remove = commands.add_parser("remove-schedule", help="Remove this agent's Windows daily task.")

    status = commands.add_parser("schedule-status", help="Check the Windows daily upload task.")

    run = commands.add_parser("run-daily", help=argparse.SUPPRESS)
    run.add_argument("--output-dir", type=Path, default=Path("output"))
    run.add_argument("--timezone", default="America/New_York")
    run.add_argument("--fps", type=int, default=24)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "preview":
            if args.fps < 1:
                raise ValueError("--fps must be at least 1.")
            create_preview(args.output_dir, args.date, args.slot, args.fps)
            return 0
        if args.command == "authorize":
            authorize_youtube(args.client_secret)
            return 0
        if args.command == "telegram-setup":
            configure_telegram()
            return 0
        if args.command == "install-schedule":
            result = install_daily_task(args.output_dir, args.timezone)
            print(result)
            print(
                f"Daily Task Scheduler job '{TASK_NAME}' will prepare three videos; "
                "YouTube will release them privately scheduled for 09:00, 14:00, and 18:00 Eastern Time."
            )
            return 0
        if args.command == "remove-schedule":
            print(remove_daily_task())
            return 0
        if args.command == "schedule-status":
            from .youtube import task_status

            print(task_status())
            return 0
        if args.command == "run-daily":
            if args.fps < 1:
                raise ValueError("--fps must be at least 1.")
            return run_daily(args.output_dir, args.timezone, args.fps)
    except (YouTubeSetupError, ValueError, OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if args.command == "run-daily":
            _notify_daily_failure(args.output_dir, exc)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

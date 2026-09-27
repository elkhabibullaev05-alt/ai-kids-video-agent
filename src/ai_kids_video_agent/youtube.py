from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .render import ensure_executable


UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
TASK_NAME = "AI Ocean Shorts - 2 daily US posts"


class YouTubeSetupError(RuntimeError):
    """YouTube credentials, API access, or uploads are not ready."""


def credential_directory() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return root / "ai-kids-video-agent"


def _libraries():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise YouTubeSetupError(
            "YouTube API tools are not installed. Run "
            "`python -m pip install -e \".[publish]\"`."
        ) from exc
    return Request, Credentials, InstalledAppFlow, build, MediaFileUpload


def _credential_paths() -> tuple[Path, Path]:
    directory = credential_directory()
    client_json = Path(
        os.environ.get("YOUTUBE_CLIENT_SECRET", directory / "client_secret.json")
    ).expanduser()
    token_json = Path(
        os.environ.get("YOUTUBE_TOKEN_FILE", directory / "token.json")
    ).expanduser()
    return client_json, token_json


def authorize_youtube(client_secret: str | Path | None = None) -> None:
    _, _, InstalledAppFlow, _, _ = _libraries()
    default_client, token_path = _credential_paths()
    client_path = Path(client_secret).expanduser() if client_secret else default_client
    if not client_path.is_file():
        raise YouTubeSetupError(
            "Google OAuth client file was not found. Download the OAuth 2.0 "
            "Desktop app JSON from Google Cloud Console, enable YouTube Data API v3, "
            "and save it as "
            f"`{default_client}` (or pass `--client-secret \"{client_path}\"`)."
        )
    token_path.parent.mkdir(parents=True, exist_ok=True)
    flow = InstalledAppFlow.from_client_secrets_file(str(client_path), [UPLOAD_SCOPE])
    credentials = flow.run_local_server(
        host="localhost",
        port=0,
        open_browser=True,
        authorization_prompt_message=(
            "Opening a Google sign-in window. Sign in with the YouTube channel "
            "you want to connect and approve video uploads."
        ),
        success_message="YouTube channel connected. You may close this browser tab.",
    )
    token_path.write_text(credentials.to_json(), encoding="utf-8")
    print(f"YouTube authorization saved locally at {token_path}.")
    print("Your password was entered only on Google's sign-in page; it was not saved here.")


def youtube_service():
    Request, Credentials, _, build, _ = _libraries()
    _, token_path = _credential_paths()
    if not token_path.is_file():
        raise YouTubeSetupError(
            "This computer is not connected to a YouTube channel yet. Run "
            "`ocean-shorts authorize` and approve access in Google's sign-in page."
        )
    try:
        credentials = Credentials.from_authorized_user_file(str(token_path), [UPLOAD_SCOPE])
    except (ValueError, OSError) as exc:
        raise YouTubeSetupError(
            f"Could not read the local YouTube authorization token: {exc}. "
            "Run `ocean-shorts authorize` again."
        ) from exc
    if credentials.expired and credentials.refresh_token:
        from google.auth.exceptions import RefreshError

        try:
            credentials.refresh(Request())
        except (RefreshError, OSError) as exc:
            raise YouTubeSetupError(
                f"Google authorization expired or was revoked: {exc}. "
                "Run `ocean-shorts authorize` again."
            ) from exc
        token_path.write_text(credentials.to_json(), encoding="utf-8")
    if not credentials.valid:
        raise YouTubeSetupError(
            "YouTube authorization is no longer valid. Run `ocean-shorts authorize` again."
        )
    return build("youtube", "v3", credentials=credentials, cache_discovery=False)


def upload_scheduled_video(
    video_path: str | Path,
    metadata: dict,
    publish_at: datetime,
    service=None,
) -> str:
    if publish_at.tzinfo is None:
        raise ValueError("The scheduled publication time must include a timezone.")
    if publish_at <= datetime.now(publish_at.tzinfo) + timedelta(minutes=2):
        raise ValueError("The YouTube publication time must be at least two minutes in the future.")
    path = Path(video_path)
    if not path.is_file() or path.stat().st_size == 0:
        raise FileNotFoundError(f"Video file is missing or empty: {path}")
    if service is None:
        service = youtube_service()
    _, _, _, _, MediaFileUpload = _libraries()
    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": metadata.get("category_id", "15"),
            "defaultLanguage": metadata.get("language", "en"),
            "defaultAudioLanguage": metadata.get("language", "en"),
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.isoformat(timespec="seconds"),
            "selfDeclaredMadeForKids": False,
        },
    }
    request = service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(
            str(path),
            mimetype="video/mp4",
            chunksize=8 * 1024 * 1024,
            resumable=True,
        ),
        notifySubscribers=False,
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    video_id = response.get("id") if isinstance(response, dict) else None
    if not video_id:
        raise YouTubeSetupError("YouTube accepted the upload without returning a video ID.")
    return video_id


def publish_time(day: date, slot_hour: int, timezone_name: str = "America/New_York") -> datetime:
    try:
        zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown timezone: {timezone_name}") from exc
    if not 0 <= slot_hour <= 23:
        raise ValueError("The publication hour must be between 0 and 23.")
    return datetime.combine(day, time(slot_hour), zone)


def task_start_local_time(timezone_name: str = "America/New_York") -> str:
    target = publish_time(date.today(), 5, timezone_name)
    return target.astimezone().strftime("%H:%M")


def install_daily_task(output_dir: str | Path, timezone_name: str = "America/New_York") -> str:
    if sys.platform != "win32":
        raise YouTubeSetupError("Automatic daily scheduling currently uses Windows Task Scheduler.")
    youtube_service()
    scheduler = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "System32", "schtasks.exe")
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    launcher = credential_directory() / "run_ocean_shorts_daily.cmd"
    launcher.parent.mkdir(parents=True, exist_ok=True)
    module_command = (
        f'"{sys.executable}" -m ai_kids_video_agent.ocean_cli run-daily '
        f'--output-dir "{output}" --timezone "{timezone_name}"'
    )
    launcher.write_text(
        "@echo off\r\n"
        f'cd /d "{output}"\r\n'
        f'{module_command} '
        f'>> "{output / "schedule.log"}" 2>&1\r\n',
        encoding="utf-8",
    )
    task_run = f'cmd.exe /d /s /c ""{launcher}""'
    if len(task_run) > 261:
        raise YouTubeSetupError(
            "The Windows scheduled-task command exceeds its length limit: "
            f"{task_run}"
        )
    completed = subprocess.run(
        [
            scheduler,
            "/Create",
            "/TN",
            TASK_NAME,
            "/SC",
            "DAILY",
            "/ST",
            task_start_local_time(timezone_name),
            "/TR",
            task_run,
            "/F",
            "/RL",
            "LIMITED",
            "/IT",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        raise YouTubeSetupError(
            f"Windows could not install the daily upload task: "
            f"{completed.stderr or completed.stdout}"
        )
    return completed.stdout.strip()


def remove_daily_task() -> str:
    if sys.platform != "win32":
        raise YouTubeSetupError("Automatic daily scheduling currently uses Windows Task Scheduler.")
    scheduler = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "System32", "schtasks.exe")
    completed = subprocess.run(
        [scheduler, "/Delete", "/TN", TASK_NAME, "/F"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        raise YouTubeSetupError(
            f"Windows could not remove the daily upload task: "
            f"{completed.stderr or completed.stdout}"
        )
    return completed.stdout.strip()


def task_status() -> str:
    if sys.platform != "win32":
        raise YouTubeSetupError("Automatic daily scheduling currently uses Windows Task Scheduler.")
    scheduler = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "System32", "schtasks.exe")
    completed = subprocess.run(
        [scheduler, "/Query", "/TN", TASK_NAME, "/FO", "LIST", "/V"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        return (
            "Daily publishing task is not installed yet. After channel authorization, "
            "run `ocean-shorts install-schedule`."
        )
    return completed.stdout.strip()

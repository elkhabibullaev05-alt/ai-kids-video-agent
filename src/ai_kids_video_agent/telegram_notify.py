from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from getpass import getpass
from pathlib import Path


def _config_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return root / "ai-kids-video-agent" / "telegram.json"


def _call_bot_api(token: str, method: str, payload: dict | None = None) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    if payload is None:
        request = urllib.request.Request(url)
    else:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("description", "HTTP error")
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = f"HTTP {exc.code}"
        raise RuntimeError(f"Telegram {method} failed: {detail}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Telegram {method} request failed: {exc.reason}") from None
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Telegram {method} returned an invalid response.") from exc
    if not isinstance(result, dict) or result.get("ok") is not True:
        detail = result.get("description", "Unknown Telegram API error") if isinstance(result, dict) else "Invalid response"
        raise RuntimeError(f"Telegram {method} failed: {detail}")
    return result


def configure_telegram() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        token = getpass("Telegram bot token (input is hidden): ").strip()
    if not token:
        raise ValueError("The Telegram bot token cannot be empty.")
    token = token.replace("\\_", "_")
    if not re.fullmatch(r"\d{6,12}:[A-Za-z0-9_-]{20,}", token):
        match = re.search(r"(?<!\d)\d{6,12}:[A-Za-z0-9_-]{20,}", token)
        if match:
            token = match.group(0)
    if not re.fullmatch(r"\d{6,12}:[A-Za-z0-9_-]{20,}", token):
        raise ValueError(
            "Could not read a Telegram bot token. Copy the token from BotFather "
            "(or its full message) and paste it at this hidden prompt. Do not enter "
            "it at the PowerShell command prompt or share it in chat."
        )
    updates = _call_bot_api(token, "getUpdates").get("result", [])
    private_chats = [
        update["message"]["chat"]
        for update in updates
        if isinstance(update, dict)
        and isinstance(update.get("message"), dict)
        and isinstance(update["message"].get("chat"), dict)
        and update["message"]["chat"].get("type") == "private"
    ]
    if not private_chats:
        raise RuntimeError(
            "No private Telegram chat was found. Open your new bot in Telegram, "
            "press Start, send /start, then run telegram-setup again."
        )
    chat_id = private_chats[-1]["id"]
    _call_bot_api(
        token,
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "✅ Ocean Glow bildirishnomalari ulandi. Agent video tayyorlaganda yoki xato yuz berganda xabar yuboradi.",
        },
    )
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"bot_token": token, "chat_id": chat_id}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Telegram notification settings saved locally at {path}.")
    print("A test message was sent to your private Telegram chat.")


def send_telegram_notification(message: str) -> bool:
    env_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    env_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if env_token or env_chat_id:
        if not env_token or not env_chat_id:
            raise RuntimeError(
                "Both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be configured."
            )
        _call_bot_api(
            env_token,
            "sendMessage",
            {"chat_id": env_chat_id, "text": message[:4000]},
        )
        return True
    path = _config_path()
    if not path.is_file():
        return False
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read Telegram settings at {path}: {exc}") from exc
    token = config.get("bot_token") if isinstance(config, dict) else None
    chat_id = config.get("chat_id") if isinstance(config, dict) else None
    if not isinstance(token, str) or not token or chat_id is None:
        raise RuntimeError(f"Telegram settings at {path} are missing bot_token or chat_id.")
    _call_bot_api(
        token,
        "sendMessage",
        {"chat_id": chat_id, "text": message[:4000]},
    )
    return True

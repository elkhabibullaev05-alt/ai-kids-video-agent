"""YouTube Data API upload (no browser, no Claude).
token.json = authorized-user JSON made once on the owner's PC with cloud/auth.py."""
import time

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]


class Quota(Exception):
    """Daily API quota is used up — try again later."""


def client(token_path):
    cr = Credentials.from_authorized_user_file(token_path)  # keep the scopes the token was granted
    if not cr.valid:
        cr.refresh(Request())
    return build("youtube", "v3", credentials=cr, cache_discovery=False)


def my_channel_id(yt):
    r = yt.channels().list(part="id", mine=True).execute()
    return r["items"][0]["id"] if r.get("items") else None


def _reason(e):
    try:
        return e.error_details[0].get("reason", "")
    except Exception:
        return str(e)


def upload(yt, path, title, description, tags, publish_at, kids, category="1", localizations=None, thumb=None, synthetic=False):
    """Upload as private + scheduled (publish_at = RFC3339 UTC). Returns the video id."""
    body = {
        "snippet": {"title": title[:100], "description": description[:4900], "tags": tags[:30], "categoryId": category,
                    "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": "private", "publishAt": publish_at, "selfDeclaredMadeForKids": bool(kids),
                   "embeddable": True},
    }
    if synthetic:  # realistic AI footage → YouTube "altered or synthetic content" disclosure (2026-10-26)
        body["status"]["containsSyntheticMedia"] = True
    parts = "snippet,status"
    if localizations:
        body["localizations"] = localizations
        parts += ",localizations"
    for attempt in range(2):
        try:
            req = yt.videos().insert(part=parts, body=body,
                                     media_body=MediaFileUpload(path, chunksize=16 * 1024 * 1024, resumable=True))
            resp = None
            while resp is None:
                _, resp = req.next_chunk(num_retries=5)
            vid = resp["id"]
            break
        except HttpError as e:
            r = _reason(e)
            if "quota" in r.lower() or "uploadLimitExceeded" in r:
                raise Quota(r)
            if e.resp.status == 400 and body["status"].pop("containsSyntheticMedia", None) and attempt == 0:
                continue  # API without the disclosure field → upload anyway, owner ticks it in Studio
            if e.resp.status == 400 and "localizations" in body and attempt == 0:
                body.pop("localizations"); parts = "snippet,status"  # bad translation text → upload without it
                continue
            raise
        except (TimeoutError, ConnectionError) as e:  # 2026-10-21: "The write operation timed out" (net blip) — retry once
            if attempt == 1:
                raise
            print("upload network error, retry in 60 s:", e, flush=True)
            time.sleep(60)
    if thumb:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
        except HttpError:
            pass  # unverified channel / Shorts: no custom thumbnails
    time.sleep(2)
    return vid

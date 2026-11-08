"""YouTube Data API upload (no browser, no Claude).
token.json = authorized-user JSON made once on the owner's PC with cloud/auth.py."""
import ssl, http.client, socket
import time

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]


def online(timeout=8):
    """True when the internet (YouTube's API host) answers. Used to pause instead of failing when the link drops."""
    for host in ("www.googleapis.com", "youtube.googleapis.com"):
        try:
            socket.create_connection((host, 443), timeout=timeout).close()
            return True
        except OSError:
            pass
    return False


def wait_online(max_wait=4 * 3600, step=30):
    """2026-11-08 owner: when the internet drops, stop and wait; when it is back, continue where it stopped.
    Returns True when back online, False if still offline after max_wait seconds."""
    if online():
        return True
    print("internet yo'q — kutyapman, qaytishi bilan davom etadi", flush=True)
    waited = 0
    while waited < max_wait:
        time.sleep(step)
        waited += step
        if online():
            print(f"internet qaytdi ({waited // 60} daqiqadan keyin) — davom etyapman", flush=True)
            return True
    return False


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


def make_private(yt, vid):
    """Set a video to private and cancel its schedule. Needs a token with the youtube.force-ssl scope.
    Returns 'ok', 'gone' (deleted/not ours) or raises HttpError (e.g. 403 insufficient scope)."""
    r = yt.videos().list(part="status", id=vid).execute()
    if not r.get("items"):
        return "gone"
    st = r["items"][0]["status"]
    if st.get("privacyStatus") == "private" and not st.get("publishAt"):
        return "ok"
    body = {"id": vid, "status": {"privacyStatus": "private",
                                  "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
                                  "embeddable": st.get("embeddable", True)}}
    yt.videos().update(part="status", body=body).execute()
    return "ok"


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
                                     media_body=MediaFileUpload(path, chunksize=8 * 1024 * 1024, resumable=True))
            resp, fails = None, 0
            while resp is None:
                try:
                    _, resp = req.next_chunk(num_retries=5)
                    fails = 0
                except (ssl.SSLError, OSError, http.client.HTTPException) as ne:
                    # 2026-11-06: weak home link (big game download) -> "EOF occurred in violation of protocol".
                    # The upload is resumable: wait and continue from the last chunk instead of failing the job.
                    # 2026-11-08: internet fully gone -> pause (does not count as a failure) until it is back,
                    # then the same resumable session continues from the last uploaded chunk.
                    if not online():
                        if not wait_online():
                            raise ConnectionError(f"internet down > 4 h: {ne}")
                        continue
                    fails += 1
                    if fails > 30:
                        raise ConnectionError(f"upload stalled: {ne}")
                    print(f"upload chunk network error {fails}/30, retry in {min(300, 20 * fails)} s:", ne, flush=True)
                    time.sleep(min(300, 20 * fails))
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

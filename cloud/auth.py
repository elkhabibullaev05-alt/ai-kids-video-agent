"""One-time YouTube sign-in, run by the OWNER on his own PC (a browser opens; pick the right channel).

    pip install google-auth-oauthlib google-api-python-client
    python auth.py client_secret.json token_doughbros.json

Then copy the token file to that channel's server as ~/kanal/<channel>/token.json (see cloud/README.md).
"""
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl"]  # force-ssl: lets the worker make a wrong video private (2026-10-29)
secret, out = sys.argv[1], sys.argv[2]
cr = InstalledAppFlow.from_client_secrets_file(secret, SCOPES).run_local_server(port=0, prompt="consent")
ch = build("youtube", "v3", credentials=cr).channels().list(part="snippet", mine=True).execute()["items"][0]
open(out, "w").write(cr.to_json())
print(f"OK: {ch['snippet']['title']} ({ch['id']}) -> {out}")

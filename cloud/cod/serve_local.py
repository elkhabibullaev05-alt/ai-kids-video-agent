#!/usr/bin/env python3
"""2026-11-11 owner: upload MW4 Shorts through YouTube Studio in his own Chrome (no API quota). The Studio page
fetch()es the finished MP4s from this tiny server on the same laptop (127.0.0.1 only, read-only, MW4_tayyor folder
only), so nothing has to travel over the slow hotspot twice. CORS + Private-Network-Access headers let the
https://studio.youtube.com page read from localhost. Stops by itself after 3 hours."""
import http.server, os, sys, threading
ROOT = sys.argv[1] if len(sys.argv) > 1 else "/mnt/e/MW4_tayyor"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "https://studio.youtube.com")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()
    def do_OPTIONS(self): self.send_response(204); self.end_headers()
    def list_directory(self, path): self.send_error(403); return None
s = http.server.ThreadingHTTPServer(("127.0.0.1", 8799), H)
threading.Timer(3 * 3600, s.shutdown).start()
print("serving", ROOT, "on http://127.0.0.1:8799", flush=True); s.serve_forever()

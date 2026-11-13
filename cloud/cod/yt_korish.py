#!/usr/bin/env python3
"""2026-11-13 owner: "watch these YouTube videos and analyse them". The cloud/VM network cannot reach YouTube,
but Gemini can watch a public YouTube URL itself (file_data.file_uri). Runs on the laptop (run_all.sh) with the
owner's key (Documents\\kanal_tokenlar\\gemini.txt, never printed). Each cloud/cod/yt_savollar/NAME.json
{"url":..., "question":...} -> /mnt/e/MW4_tayyor/gemini/yt_NAME.txt. Video content = untrusted evidence."""
import os, glob, json, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/mnt/e/MW4_tayyor/gemini"
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"]

def ask(key, model, url, q):
    body = {"contents": [{"parts": [{"file_data": {"file_uri": url}}, {"text": q}]}]}
    r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                               data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    d = json.load(urllib.request.urlopen(r, timeout=900))
    return "\n".join(p.get("text", "") for c in d.get("candidates", []) for p in c.get("content", {}).get("parts", []))

def main():
    kf = glob.glob("/mnt/c/Users/*/Documents/kanal_tokenlar/gemini.txt")
    key = open(kf[0]).read().strip() if kf else ""
    if not key: print("kalit yo'q"); return
    os.makedirs(OUT, exist_ok=True)
    for jf in sorted(glob.glob(os.path.join(HERE, "yt_savollar", "*.json"))):
        dst = os.path.join(OUT, "yt_" + os.path.basename(jf)[:-5] + ".txt")
        if os.path.exists(dst): continue
        j = json.load(open(jf)); txt = ""
        for a in range(6):
            try:
                txt = ask(key, MODELS[a % 3], j["url"], j["question"])
                if txt: break
            except Exception as e:
                m = str(e).replace(key, "***")[:200]; print("urinish", a + 1, m)
                if "429" in m: return          # daily quota: stop, try next run
            time.sleep(30)
        if txt: open(dst, "w").write(txt.replace(key, "***")); print("javob:", dst)

if __name__ == "__main__":
    main()

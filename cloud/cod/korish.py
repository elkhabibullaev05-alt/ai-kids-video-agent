#!/usr/bin/env python3
"""2026-11-12 owner: "Claude must SEE and HEAR the video, not just stills". Uses the MIT 'watch' skill
(github.com/bradautomates/claude-video, copied to cloud/tools/watch) with its Gemini engine: Google's video model
watches the whole clip with sound and answers a strict viewer-style rubric. Report -> <video>_baho.txt (Claude reads it).
The owner's free key lives in Documents\\kanal_tokenlar\\gemini.txt (owner puts it there; never printed or logged).
usage: korish.py VIDEO [VIDEO...]"""
import os, sys, subprocess, glob, time

KEYF = glob.glob("/mnt/c/Users/*/Documents/kanal_tokenlar/gemini.txt")
WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools", "watch", "scripts", "watch.py")
Q = ("You are a harsh YouTube Shorts viewer and editor. Watch AND listen to this whole gaming Short and answer with "
     "timestamps: 1) Would you keep watching after 2 seconds? Why? 2) Picture: sharp or blurry, too dark, are faces and "
     "details clear, colours? 3) Camera: smooth or shaky/jerky, does it make you dizzy? 4) Is a mouse cursor or any "
     "glitch visible? 5) Music: does it fit the action, do the cuts/hits land on the beat, is it too loud vs game sound, "
     "any clash? 6) Text: readable, good hook? 7) Pacing and ending. 8) Score 1-10 and the 3 most important fixes. "
     "Compare with the most viral Call of Duty Shorts.")

MODELS = ["gemini-3.7-flash", "gemini-3.5-flash", "gemini-2.5-flash", "gemini-3.7-flash-lite"]


def main():
    env = dict(os.environ)
    if KEYF:
        env["GEMINI_API_KEY"] = open(KEYF[0]).read().strip()
    if not env.get("GEMINI_API_KEY"):
        print("gemini.txt yo'q: Documents\\kanal_tokenlar\\gemini.txt ga kalit qo'yilishi kerak"); return 2
    for v in sys.argv[1:]:
        out = os.path.splitext(v)[0] + "_baho.txt"
        for attempt in range(6):   # 2026-11-12: "HTTP 503 high demand" on gemini-3.7-flash -> rotate models + back off
            env["WATCH_GEMINI_MODEL"] = MODELS[attempt % len(MODELS)]
            r = subprocess.run([sys.executable, WATCH, v, "--engine", "gemini", "--question", Q],
                               capture_output=True, text=True, env=env, timeout=900)
            txt = r.stdout if r.returncode == 0 else (r.stdout + "\n" + r.stderr[-2000:])
            if "(failed)" not in txt and r.returncode == 0:
                break
            time.sleep(20 if 'not found' in txt.lower() or '404' in txt else 60)
        if "(failed)" in txt or r.returncode:
            print("baho olinmadi (keyingi safar qayta):", v); continue
        open(out, "w").write(txt.replace(env["GEMINI_API_KEY"], "***"))
        print("baho yozildi:", out)

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""2026-11-13 owner: "when I play Roblox or Call of Duty it must record by itself and the agents montage it by themselves".
Windows side (Documents\\avto_yozish\\game_rec.py) records with OBS and drops Documents\\kanal_navbat\\gameplay\\*.json.
Here (laptop WSL, run_all.sh): for each new job -> cod_action.py finds the fights -> the 6 strongest moments become v5 Shorts
(short4.py) in E:\\MW4_tayyor\\auto\\<stem>_V<k>.mp4 + local check. Nothing is uploaded from here: Claude reviews them and
adds the good ones to cloud/cod/v4_ok.json (owner rule: watch it like a viewer first)."""
import os, sys, json, glob, subprocess, random
HERE = os.path.dirname(os.path.abspath(__file__))
Q = glob.glob("/mnt/c/Users/*/Documents/kanal_navbat/gameplay")
OUT = "/mnt/e/MW4_tayyor/auto"
MUSIC = "/mnt/c/Users/1/Videos/MW4/musiqa"
# 2026-11-18 owner + Studio data (MW4 Shorts Daily): first-person story hooks won — 'The Patrol Sent A Dog After Me...'
# 3512, 'This Got Intense FAST' 2388, 'They Never Knew Where I Was' 2331 vs ~1500 for generic ones. Story-first hooks.
# 2026-11-18: first-person story hooks won on MW4 Shorts Daily ('They Never Knew Where I Was' 2331, 'This Got Intense
# FAST' 2388). Hooks are given to clips blindly (no content check), so they must fit ANY firefight — nothing specific
# like a dog, a vehicle or "1 vs 5" that the clip may not show (a false claim = misleading title).
HOOKS = {"cod": [("This got intense FAST", "FAST", "NO WAY"), ("They never knew where I was 🎯", "NEVER", "GHOST"),
                 ("He heard me reload... 😬", "HEARD", "BRUH"), ("I shouldn't have survived this 💀", "SURVIVED", "HOW?"),
                 ("They had no idea I was there", "IDEA", "BOOM"), ("Last bullet. Last chance. 🎯", "LAST", "LOCKED")],
         "roblox": [("This combo is unfair", "UNFAIR", "COMBO"), ("He didn't see that coming", "COMING", "BOOM"),
                    ("Strongest Battlegrounds chaos", "CHAOS", "CHAOS"), ("Wait for the ending", "ENDING", "NO WAY"),
                    ("1v1 gone wrong", "WRONG", "BRUH"), ("This guy is cracked", "CRACKED", "CRACKED")]}


def win2wsl(p):
    p = p.replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:] if len(p) > 2 and p[1] == ":" else p


def windowed(src, t):
    """OBS records the whole screen: a windowed game leaves the white title bar + taskbar in frame -> crop them."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", "scale=192:108,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(raw) < 192 * 108: return False
    top = sum(raw[192 * 0:192 * 3]) / (192 * 3)
    return top > 200


# 2026-11-18 owner: "fix the cutter". 12 overnight Shorts all failed (<85): half were desktop screen recordings
# (the recorder kept recording after the game was minimised; loud YouTube audio looked like gunfire) and the rest
# showed killcams / the downed screen. A clip is now cut only if the frames around the peak are clean gameplay.
import re
import numpy as np
BAD_TEXT = re.compile(r"KILLED\s*BY|\bSKIP\b|REPORT\s*PLAYER|GIVE\s*UP|RETURN\s*TO\s*MISSION|SPECTAT|ELIMINATED|MISSION\s*FAILED")


def bad_frame(src, t):
    """Why the frame at second t is NOT clean gameplay, or None if it is."""
    t = str(max(0.0, t))
    g = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", src, "-frames:v", "1", "-vf", "scale=192:108,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(g) < 192 * 108: return "kadr o'qilmadi"
    if (np.frombuffer(g[:192 * 108], np.uint8) > 225).mean() > 0.22: return "ish stoli (oq oyna)"
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", src, "-frames:v", "1", "-vf", "scale=1280:720",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    if not png: return "kadr o'qilmadi"
    txt = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11"], input=png, capture_output=True).stdout.decode("utf-8", "ignore").upper()
    m = BAD_TEXT.search(txt)
    return ("o'lim/menyu yozuvi: " + m.group(0)) if m else None


def clean_peaks(src, peaks, n, stem):
    """First n peaks whose clip (t-3 .. t+5 s) is clean gameplay. Rejections are printed."""
    good = []
    for t in peaks:
        why = next((w for d in (-3, 0, 3, 5) for w in [bad_frame(src, t + d)] if w), None)
        if why: print(stem, f"{t}s rad etildi:", why, flush=True)
        else: good.append(t)
        if len(good) >= n: break
    return good


def main():
    os.makedirs(OUT, exist_ok=True)
    for qd in Q:
        for jf in sorted(glob.glob(os.path.join(qd, "*.json"))):
            job = json.load(open(jf)); src = win2wsl(job.get("file", "")); game = job.get("game", "cod")
            base = os.path.splitext(os.path.basename(jf))[0] + "_" + game
            stem = base + job.get("tag", "")          # "tag" re-cuts a recording without reusing old file names
            if not os.path.exists(src):
                print("fayl yo'q:", src); os.rename(jf, jf + ".yoq"); continue
            ad = os.path.join(OUT, base + "_aksiya"); act = os.path.join(ad, "action.json")
            if not os.path.exists(act):
                subprocess.run([sys.executable, os.path.join(HERE, "cod_action.py"), src, ad], timeout=4 * 3600)
            a = json.load(open(act)); peaks = a.get("peaks", [])
            peaks = clean_peaks(src, peaks, int(job.get("n", 6)), stem) if game == "cod" else peaks[:int(job.get("n", 6))]
            print(stem, "toza cho'qqilar:", len(peaks), flush=True)
            music = sorted(f for f in os.listdir(MUSIC) if f.endswith(".mp3")) if os.path.isdir(MUSIC) else []
            for k, t in enumerate(peaks, 1):
                dst = os.path.join(OUT, f"{stem}_V{k}.mp4")
                if os.path.exists(dst): continue
                h, red, pop = HOOKS[game][(k - 1) % len(HOOKS[game])]
                sp = dict(t=t, style="v5", pre=3.4, post=5.5, action=act,   # 2026-11-14 owner: 9-15 s, start on the shots
                          hook=h, red=red, pop=pop, src=src, out=dst, music_dir=MUSIC,
                          music=random.choice(music) if music else "", yt_title=f"{h} " + ('#mw4 #callofduty' if game == 'cod' else '#roblox #shorts'))
                if windowed(src, t): sp["src_crop"] = "crop=1714:964:103:40"
                sj = f"/tmp/auto_{stem}_{k}.json"; json.dump(sp, open(sj, "w"))
                r = subprocess.run([sys.executable, os.path.join(HERE, "short4.py"), sj], capture_output=True, text=True)
                print(stem, k, "TAYYOR" if r.returncode == 0 else "XATO " + r.stderr[-500:])
            vids = [os.path.join(OUT, f) for f in sorted(os.listdir(OUT)) if f.startswith(stem) and f.endswith(".mp4")]
            if vids:
                subprocess.run([sys.executable, os.path.join(HERE, "korish.py")] + vids, capture_output=True, text=True)
            os.rename(jf, jf + ".tayyor")


if __name__ == "__main__":
    main()

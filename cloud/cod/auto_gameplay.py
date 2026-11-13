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
HOOKS = {"cod": [("He never saw it coming", "NEVER", "BOOM"), ("This fight got crazy", "CRAZY", "NO WAY"),
                 ("Wait for the last shot", "LAST", "LOCKED"), ("He was waiting for me", "WAITING", "BRUH"),
                 ("Clutch or kicked", "CLUTCH", "CLUTCH"), ("Never peek this corner", "NEVER", "NOPE")],
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


def main():
    os.makedirs(OUT, exist_ok=True)
    for qd in Q:
        for jf in sorted(glob.glob(os.path.join(qd, "*.json"))):
            job = json.load(open(jf)); src = win2wsl(job.get("file", "")); game = job.get("game", "cod")
            stem = os.path.splitext(os.path.basename(jf))[0] + "_" + game
            if not os.path.exists(src):
                print("fayl yo'q:", src); os.rename(jf, jf + ".yoq"); continue
            ad = os.path.join(OUT, stem + "_aksiya"); act = os.path.join(ad, "action.json")
            if not os.path.exists(act):
                subprocess.run([sys.executable, os.path.join(HERE, "cod_action.py"), src, ad], timeout=4 * 3600)
            a = json.load(open(act)); peaks = a.get("peaks", [])[:6]
            music = sorted(f for f in os.listdir(MUSIC) if f.endswith(".mp3")) if os.path.isdir(MUSIC) else []
            for k, t in enumerate(peaks, 1):
                dst = os.path.join(OUT, f"{stem}_V{k}.mp4")
                if os.path.exists(dst): continue
                h, red, pop = HOOKS[game][(k - 1) % len(HOOKS[game])]
                sp = dict(t=t, style="v5", pre=3.4, post=2.5, hook=h, red=red, pop=pop, src=src, out=dst, music_dir=MUSIC,
                          music=random.choice(music) if music else "", yt_title=f"{h} #{'cod' if game == 'cod' else 'roblox'} #shorts")
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

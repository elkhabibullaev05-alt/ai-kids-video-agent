"""Join rendered song segments into one sing-along compilation with karaoke lyrics.
python3 songs/assemble.py out3d/songs OUT.mp4   (1920x1080, < 100 MB for the GitHub-hosted upload)"""
import json, os, sys, subprocess, glob

R, OUT = sys.argv[1], sys.argv[2]
FPS = 12
W, H = 1920, 1080
COL = {"max": "&H0030A0FF&", "mouse": "&H00E0B0FF&", "grandma": "&H00D070C0&", "dog": "&H0040C0FF&", "bird": "&H00FFC060&", "all": "&H0060E060&"}


def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


songs = sorted(d for d in glob.glob(os.path.join(R, "s*_*")) if os.path.isdir(d))
parts, ass_lines, offset = [], [], 0.0
for d in songs:
    plan = json.load(open(os.path.join(d, "plan.json")))
    lyr = json.load(open(os.path.join(d, "lyrics.json")))
    lst = os.path.join(d, "frames.txt")
    with open(lst, "w") as f:
        for p in plan["plan"]:
            fr = sorted(glob.glob(os.path.join(d, "seg_" + p["seg"], "frames", "f_*.png")))
            assert len(fr) >= p["frames"], (d, p, len(fr))
            for x in fr[:p["frames"]]:
                f.write(f"file '{os.path.abspath(x)}'\nduration {1/FPS:.6f}\n")
    seg_mp4 = os.path.join(d, "song.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(d, "audio.wav"),
                    "-vf", f"fps=24,scale={W}:{H}:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "pcm_s16le", "-shortest", seg_mp4.replace(".mp4", ".mkv")], check=True)
    parts.append(seg_mp4.replace(".mp4", ".mkv"))
    for l in lyr:
        t0, t1 = offset + l["t"], offset + l["end"]
        if l.get("card"):
            ass_lines.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},Card,,0,0,0,,{{\\fad(150,250)\\t(0,300,\\fscx110\\fscy110)\\t(300,600,\\fscx100\\fscy100)}}{l['text']}")
            continue
        words = l["text"].split(); dur = max(0.5, l["dur"]) * 100
        tot = sum(len(w) + 1 for w in words)
        k = "".join(f"{{\\kf{int(dur * (len(w) + 1) / tot)}}}{w} " for w in words)
        ass_lines.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Lyric,,0,0,0,,{{\\3c{COL.get(l['who'], COL['all'])}}}{k.strip()}")
    offset += plan["frames"] / FPS

ass = os.path.join(R, "lyrics.ass")
with open(ass, "w") as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Poppins,92,&H0000E8FF&,&H00FFFFFF&,&H0030A0FF&,&H80000000&,1,0,0,0,100,100,1,0,1,7,3,2,80,80,60,1
Style: Card,Poppins,150,&H00FFFFFF&,&H00FFFFFF&,&H002050FF&,&H80000000&,1,0,0,0,100,100,2,0,1,12,6,8,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ass_lines) + "\n")

cl = os.path.join(R, "parts.txt")
open(cl, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
dur = offset
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", cl,
                "-vf", f"ass={ass},format=yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                "-c:v", "libx264", "-preset", "slow", "-b:v", "880k", "-maxrate", "1100k", "-bufsize", "2200k", "-g", "48",
                "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
print(OUT, round(dur, 1), "s", round(os.path.getsize(OUT) / 1e6, 1), "MB")

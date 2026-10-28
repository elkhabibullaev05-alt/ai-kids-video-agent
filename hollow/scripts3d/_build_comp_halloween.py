# Halloween compilation (AGENT.md growth plan 2026-10-28): re-uses 4 finished longs (ep026, ep032, ep034, ep035)
# + a 15 s cold open and narrated bridges.  usage: python3 scripts3d/_build_comp_halloween.py <dir with epNNN/hollow_epNNN_long.mp4> <out dir>
import os, sys, subprocess, json
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
K = Kokoro("models/kokoro.onnx", "models/voices.bin")
EPS = ["026", "032", "034", "035"]
LINES = {
 "cold": ("A figure that leapt over walls. A voice inside the walls. A drum that played by itself. "
          "And a window with no room behind it. Four true stories. Not one has an answer.", "4 TRUE STORIES. NO ANSWERS."),
 "b1": ("Story one. London, eighteen thirty-eight. Something with burning eyes knocked on a family's door.", "1 · LONDON, 1838"),
 "b2": ("Story two. The Isle of Man, nineteen thirty-one. A family heard a voice behind their walls. It said it was a mongoose.", "2 · ISLE OF MAN, 1931"),
 "b3": ("If you like true mysteries, subscribe. Story three. Wiltshire, England, sixteen sixty-two. Every night, a drum played. Nobody was holding it.", "3 · WILTSHIRE, 1662"),
 "b4": ("Story four. Glamis Castle, Scotland. Guests hung a towel in every window. One window stayed empty.", "4 · GLAMIS CASTLE"),
 "end": ("Four stories. No answers. Which one scared you the most? Tell me in the comments.", "WHICH ONE SCARED YOU?"),
}
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
def run(*a): subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def tts(key):
    a, sr = K.create(LINES[key][0], voice="bm_george", speed=0.95, lang="en-gb")
    a = np.concatenate([np.zeros(int(0.15 * sr)), a, np.zeros(int(0.5 * sr))]); p = f"{OUT}/{key}.wav"; sf.write(p, a, sr); return p, len(a) / sr
def card(img_png, text, out_png):
    im = Image.open(img_png).convert("RGB").resize((1920, 1080)).filter(ImageFilter.GaussianBlur(3))
    im = Image.eval(im, lambda v: int(v * 0.55)); d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, 118)
    words = text.split(); lines = [text] if d.textlength(text, font=f) < 1700 else [" ".join(words[:len(words) // 2]), " ".join(words[len(words) // 2:])]
    y = 540 - len(lines) * 75
    for ln in lines:
        w = d.textlength(ln, font=f); d.text(((1920 - w) / 2, y), ln, font=f, fill=(255, 235, 90), stroke_width=9, stroke_fill=(0, 0, 0)); y += 150
    im.save(out_png)
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
def still_seg(key, frame_from, t_from, name):
    wav, dur = tts(key); raw = f"{OUT}/{name}_raw.png"
    run("ffmpeg", "-y", "-ss", str(t_from), "-i", frame_from, "-frames:v", "1", raw)
    card(raw, LINES[key][1], f"{OUT}/{name}.png")
    # slow push-in so the picture keeps moving
    run("ffmpeg", "-y", "-loop", "1", "-i", f"{OUT}/{name}.png", "-i", wav, "-filter_complex",
        f"[0:v]scale=2400:-2,zoompan=z='1+0.0009*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30[v]",
        "-map", "[v]", "-map", "1:a", "-t", f"{dur:.2f}", *ENC, f"{OUT}/{name}.mp4")
    return f"{OUT}/{name}.mp4"
src = {e: f"{SRC}/ep{e}/hollow_ep{e}_long.mp4" for e in EPS}
# cold open: real moving footage (first 4 s of each episode = their hooks), narrator over it, big text from frame 1
wav, dur = tts("cold"); per = dur / 4
parts = []
for i, e in enumerate(EPS):
    p = f"{OUT}/cold_{i}.mp4"; run("ffmpeg", "-y", "-ss", "0.3", "-i", src[e], "-t", f"{per:.2f}", "-an", "-vf", "scale=1920:1080,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", p); parts.append(p)
open(f"{OUT}/cold.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/cold.txt", "-c", "copy", f"{OUT}/cold_v.mp4")
txt = LINES["cold"][1]
run("ffmpeg", "-y", "-i", f"{OUT}/cold_v.mp4", "-i", wav, "-filter_complex",
    f"[0:v]drawbox=y=0:w=iw:h=230:color=black@0.55:t=fill,drawtext=fontfile={FONT}:text='{txt}':fontsize=104:fontcolor=0xFFEB5A:borderw=8:bordercolor=black:x=(w-tw)/2:y=55[v];[1:a]volume=1.6[a]",
    "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", *ENC, f"{OUT}/s00_cold.mp4")
seq = [f"{OUT}/s00_cold.mp4"]
for i, e in enumerate(EPS):
    seq.append(still_seg(f"b{i+1}", src[e], 20, f"s{i+1}0_bridge"))
    body = f"{OUT}/s{i+1}1_ep{e}.mp4"
    run("ffmpeg", "-y", "-i", src[e], "-c", "copy", body); seq.append(body)  # same codec params as the bridges: stream copy, no re-encode
seq.append(still_seg("end", src["035"], 150, "s90_end"))
open(f"{OUT}/all.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in seq))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/all.txt", "-c", "copy", "-movflags", "+faststart", f"{OUT}/comp_halloween.mp4")
d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{OUT}/comp_halloween.mp4"]).decode())
print(json.dumps({"duration": d, "segments": len(seq)}))

"""timeline.json -> subs.ass (speaker-coloured subtitles + big title cards). python3 engine/subs.py out/epNNN"""
import json, os, re, sys
D = sys.argv[1]; TL = json.load(open(os.path.join(D, "timeline.json")))
def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def bgr(c):
    r, g, b = [max(0, min(255, int(v * 255 + 60))) for v in c]
    return f"&H00{b:02X}{g:02X}{r:02X}"
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,60,1
Style: Big,DejaVu Sans,96,&H0028E1FF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,3,8,60,60,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
out = []
for b in TL["beats"]:
    s, e = b["start"], b["start"] + b["dur"] + 0.25
    if s < 0.3:
        s = 0.0  # hook text + subtitle visible on frame 1
    if b.get("say"):
        who = b["who"]; ch = TL["chars"][who]
        txt = b["say"] if who == "narr" or "color" not in ch else "{\\c" + bgr(ch["color"]) + "}" + ch["name"] + ":{\\c&H00FFFFFF&} " + b["say"]
        out.append(f"Dialogue: 0,{ts(s)},{ts(e)},Sub,,0,0,0,,{txt}")
    if b.get("text"):
        t = re.sub(r"[^\x00-⿿]", "", b["text"]).strip()
        out.append(f"Dialogue: 1,{ts(s)},{ts(s + max(1.8, b['dur'] + 0.6))},Big,,0,0,0,,{{\\fad(0,250)}}{t}")
open(os.path.join(D, "subs.ass"), "w").write(hdr + "\n".join(out) + "\n")

"""TTS for every beat (Kokoro), timeline + per-frame mouth levels.
python3 engine/voices.py scripts/epNNN.json out/epNNN [fps=12]   (needs /opt/kokoro/kokoro.onnx + voices.bin, see setup.sh)"""
import json, sys, os, re
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SR = 24000
sc = json.load(open(sys.argv[1])); OUT = sys.argv[2]; FPS = int(sys.argv[3]) if len(sys.argv) > 3 else 12
os.makedirs(OUT, exist_ok=True)
KD = os.environ.get("KOKORO_DIR", "/opt/kokoro")
k = Kokoro(os.path.join(KD, "kokoro.onnx"), os.path.join(KD, "voices.bin"))


def pitch(x, semis):
    if not semis:
        return x
    r = 2 ** (semis / 12)
    idx = np.arange(0, len(x) - 1, r)
    return np.interp(idx, np.arange(len(x)), x).astype(np.float32)


t = float(sc.get("lead_in", 0.6))  # small lead-in (set "lead_in": 0 in the script to start the voice at frame 1)
timeline = []
for i, b in enumerate(sc["beats"]):
    e = dict(b, i=i, start=round(t, 3))
    if "say" in b:
        ch = sc["chars"][b["who"]]
        a, sr = k.create(b["say"], voice=ch["voice"], speed=ch.get("speed", 1.0), lang="en-gb" if ch["voice"][0] == "b" else "en-us")
        a = pitch(np.asarray(a, np.float32), ch.get("pitch", 0))
        a = a / (np.abs(a).max() + 1e-9) * 0.9
        f = os.path.join(OUT, f"line_{i:03d}.wav"); sf.write(f, a, sr)
        dur = len(a) / sr
        hop = sr // FPS
        lv = [float(np.sqrt(np.mean(a[j:j + hop] ** 2))) for j in range(0, len(a), hop)]
        m = max(lv) or 1
        e.update(file=f, dur=round(dur, 3), mouth=[round(min(1, v / m * 1.4), 2) for v in lv])
        t += dur + 0.35
    else:
        e["dur"] = b.get("hold", 1.0)
        t += e["dur"] + 0.2
    timeline.append(e)
    print(i, e.get("who", e.get("sfx")), e["start"], e["dur"])
json.dump(dict({k: v for k, v in sc.items() if k != "beats"}, fps=FPS, duration=round(t + 1.0, 2), beats=timeline),
          open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
print("TOTAL", round(t + 1, 1), "s")

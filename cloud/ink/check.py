"""Ssenariyni tomoshabin ko'zi bilan tekshiradi (100 ball, 85 dan o'tishi shart).
   python3 cloud/ink/check.py cloud/ink/animals/NNN-slug.json"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tomosha  # noqa: E402

sc = json.load(open(sys.argv[1], encoding="utf-8"))
ok = True
for kind in ("long", "short"):
    if kind == "short" and not (sc.get("short") or {}).get("scenes"):
        print("short: YO'Q"); ok = False; continue
    sc2 = json.loads(json.dumps(sc))
    if kind == "short":
        sc2["short"]["scenes"][-1]["cta"] = "full"
    scenes = sc2["scenes"] if kind == "long" else sc2["short"]["scenes"]
    words = sum(len(x.get("say", "").split()) for x in scenes)
    secs = words / 2.6 + 0.3 * len(scenes) + (4 if kind == "long" else 0)  # agent ovozi ~156 so'z/daqiqa
    r = tomosha.baho(sc2, kind, secs, 2.0, True, kind == "short")
    print(f"{kind}: {r['ball']}/100  (~{secs / 60:.1f} min, {words} words)  {r['qism']}")
    for m in r["muammo"]:
        print("  -", m)
    ok &= r["ball"] >= 85
print("O'TDI" if ok else "O'TMADI — tuzating va qayta tekshiring")
sys.exit(0 if ok else 1)

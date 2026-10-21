"""Re-apply a script's chars/props/set/beat actions to an existing timeline.json (keeps the voice timing)."""
import json, sys
sc, tlp = json.load(open(sys.argv[1])), sys.argv[2]
tl = json.load(open(tlp))
assert len(sc["beats"]) == len(tl["beats"])
for k in ("set", "chars", "props", "title", "description"):
    tl[k] = sc[k]
for b, tb in zip(sc["beats"], tl["beats"]):
    assert b.get("say") == tb.get("say")
    for k in ("do", "cam", "text", "sfx"):
        if k in b: tb[k] = b[k]
        else: tb.pop(k, None)
json.dump(tl, open(tlp, "w"), indent=1)
print("patched", tlp)

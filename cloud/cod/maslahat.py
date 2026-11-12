#!/usr/bin/env python3
"""2026-11-12 owner: "work together with Gemini like a partner - ask it how to edit for millions of views".
Sends every question file in cloud/cod/savollar/*.txt that has no answer yet to Gemini (text only, the
watch-skill engine) and writes <name>_javob.txt next to it in OUT/gemini/. Claude reads the answers and edits.
Key: Documents\\kanal_tokenlar\\gemini.txt (owner's; never printed)."""
import os, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools", "watch", "scripts"))
import gemini                                   # noqa: E402
from config import get_config                   # noqa: E402

def main(outdir):
    kf = glob.glob("/mnt/c/Users/*/Documents/kanal_tokenlar/gemini.txt")
    key = open(kf[0]).read().strip() if kf else ""
    if not key: print("kalit yo'q"); return 2
    model = get_config()["gemini_model"]
    os.makedirs(outdir, exist_ok=True)
    for q in sorted(glob.glob(os.path.join(HERE, "savollar", "*.txt"))):
        dst = os.path.join(outdir, os.path.basename(q)[:-4] + "_javob.txt")
        if os.path.exists(dst): continue
        payload = {"model": model, "input": [{"type": "text", "text": open(q).read()}]}
        try:
            _, _, body = gemini._call("POST", gemini.INTERACTIONS, key, data=json.dumps(payload).encode(),
                                      headers={"Content-Type": "application/json"}, timeout=600)
            data = json.loads(body)
            txt = "\n".join(p["text"] for st in data.get("steps", []) if st.get("type") == "model_output"
                            for p in st.get("content", []) if p.get("type") == "text")
            txt = txt or body.decode("utf-8", "replace")[:4000]
        except BaseException as e:
            txt = "XATO: " + str(e)[:800]
        open(dst, "w").write(txt.replace(key, "***"))
        print("javob:", dst)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/mnt/e/MW4_tayyor/gemini"))

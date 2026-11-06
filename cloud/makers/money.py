#!/usr/bin/env python3
"""Money Story Daily (`money`) maker — personal-finance story Shorts from Claude-written scripts.

python3 cloud/makers/money.py --out DIR --home HOME --repo ROOT --titles TITLES.json --need-long 0|1 --need-short 0|1
    [--max 3] [--only cloud/queue/money/X.json]

Takes the oldest scripts in cloud/queue/money/*.json (written daily by the writer task, see money/WRITER.md),
renders ONE vertical Short per script (max --max per run, default 3) into DIR/<stem>.mp4 + DIR/<stem>.json
with "queue_file" so the worker moves the script to cloud/done/money/ after the rek-ball gate.
Exit 0 = made something, 3 = nothing to make (queue empty / no Shorts needed), other = error.
A script whose title was already used (TITLES.json or cloud/done/money) or that is broken is renamed to
*.json.dup / *.json.bad so it never blocks the queue.
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "money"))

NFA = "Not financial advice — just the math."
BASE_TAGS = ["personal finance", "money", "budgeting", "money tips", "Money Story Daily"]
HASH = ["#personalfinance", "#money", "#budgeting", "#shorts"]
VIS_TYPES = {"big_number", "bars", "versus", "stack", "checklist", "counter", "line", "statement", "math", "question"}


def log(*a):
    print(*a, flush=True)


def norm(t):
    return re.sub(r"[^a-z0-9$]+", " ", (t or "").lower()).strip()


def check(sc, used):
    """Returns an error string, or '' when the script is usable."""
    t = sc.get("title", "")
    if not t or len(t) > 70:
        return f"title missing or too long ({len(t)})"
    if norm(t) in used:
        return "title already used"
    sc_ = sc.get("scenes") or []
    if not 6 <= len(sc_) <= 14:
        return f"{len(sc_)} scenes (need 8-12)"
    for i, s in enumerate(sc_):
        if not (s.get("say") or "").strip():
            return f"scene {i} has no say"
        v = s.get("visual") or {}
        if v.get("type") not in VIS_TYPES:
            return f"scene {i}: unknown visual type {v.get('type')!r}"
    return ""


def description(sc):
    d = (sc.get("description") or "").strip()
    d = "\n".join(l for l in d.splitlines() if "financial advice" not in l.lower() and not l.strip().startswith("#")).strip()
    q = (sc.get("question") or "").strip()
    if q and q.lower() not in d.lower():
        d += f"\n\n💬 {q}"
    tags = [h if h.startswith("#") else "#" + re.sub(r"\W", "", h) for h in sc.get("hashtags", [])][:3]
    hs = []
    for h in tags + HASH:
        if h.lower() not in [x.lower() for x in hs]:
            hs.append(h)
    return f"{d}\n\n{NFA}\n{' '.join(hs[:6])}".strip()


def tags_of(sc):
    out = []
    for t in list(sc.get("tags", [])) + BASE_TAGS:
        t = str(t).strip().lstrip("#")
        if t and t.lower() not in [x.lower() for x in out]:
            out.append(t)
    while out and len(",".join(out)) > 480:
        out.pop()
    return out


def est_seconds(sc):
    """Voice length estimate: Kokoro at speed 1.08 says ~2.93 spoken words/s (numbers expanded), 0.16 s between scenes."""
    import mvoice
    n = sum(len(mvoice.spoken(s.get("say", "")).replace("-", " ").split()) for s in sc.get("scenes", []))
    return n / 2.93 * 1.08 / float(sc.get("speed", 1.08)) + 0.16 * (len(sc.get("scenes", [])) - 1) + 0.5


def check_queue(repo):
    """Writer-side validation of every queued script. Prints OK/FAIL per file; exit 0 only if all are OK."""
    qdir = os.path.join(repo, "cloud", "queue", "money")
    ddir = os.path.join(repo, "cloud", "done", "money")
    done = []
    for f in sorted(glob.glob(os.path.join(ddir, "*.json"))):
        try:
            done.append(json.load(open(f)))
        except Exception:
            pass
    used = {norm(d.get("title", "")) for d in done}
    combos = {(str(d.get("character", "")).lower(), str(d.get("amount", ""))) for d in done}
    bad_n = 0
    for f in sorted(glob.glob(os.path.join(qdir, "*.json"))):
        errs = []
        try:
            sc = json.load(open(f))
        except Exception as e:
            print(f"FAIL {os.path.basename(f)}: bad json: {e}")
            bad_n += 1
            continue
        e = check(sc, used)
        if e:
            errs.append(e)
        t, hook = sc.get("title", ""), sc.get("hook", "")
        if len(t) > 60:
            errs.append(f"title {len(t)} chars (max 60)")
        if not re.search(r"[\d$]", t):
            errs.append("title has no number/$ amount")
        if not hook or len(hook.split()) > 6:
            errs.append("hook missing or > 6 words")
        n = len(sc.get("scenes", []))
        if not 8 <= n <= 12:
            errs.append(f"{n} scenes (need 8-12)")
        if n and (sc["scenes"][-1].get("visual") or {}).get("type") != "question":
            errs.append("last scene must be a question visual")
        for k in ("question", "description", "tags"):
            if not sc.get(k):
                errs.append(f"missing {k}")
        combo = (str(sc.get("character", "")).lower(), str(sc.get("amount", "")))
        if combo[0] and combo in combos:
            errs.append(f"character+amount {combo} already used")
        secs = est_seconds(sc)
        if not 42 <= secs <= 57.5:
            errs.append(f"voice ~{secs:.0f}s (need 45-57: {'cut words' if secs > 57 else 'add a scene'})")
        types = {(s.get("visual") or {}).get("type") for s in sc.get("scenes", [])}
        if len(types) < 5:
            errs.append(f"only {len(types)} visual types (need >= 5)")
        name = os.path.basename(f)
        if errs:
            bad_n += 1
            print(f"FAIL {name}: " + "; ".join(errs))
        else:
            print(f"OK   {name}  ~{secs:.0f}s  {t}")
        used.add(norm(t))
        combos.add(combo)
    return 1 if bad_n else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--check", action="store_true", help="only validate cloud/queue/money/*.json (writer task)")
    ap.add_argument("--home", default=".")
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--titles", default="")
    ap.add_argument("--need-long", default="0")
    ap.add_argument("--need-short", default="1")
    ap.add_argument("--max", type=int, default=3)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    if a.check:
        return check_queue(os.path.abspath(a.repo))
    if not a.out:
        ap.error("--out is required")
    if str(a.need_short) == "0" and not a.only:
        log("money: no Shorts needed (this channel makes Shorts only)")
        return 3
    repo = os.path.abspath(a.repo)
    qdir = os.path.join(repo, "cloud", "queue", "money")
    ddir = os.path.join(repo, "cloud", "done", "money")
    os.makedirs(a.out, exist_ok=True)
    used = set()
    try:
        used |= {norm(x if isinstance(x, str) else x.get("title", "")) for x in json.load(open(a.titles))}
    except Exception:
        pass
    for f in glob.glob(os.path.join(ddir, "*.json")):
        try:
            used.add(norm(json.load(open(f)).get("title", "")))
        except Exception:
            pass
    jobs = [os.path.join(repo, a.only)] if a.only else sorted(glob.glob(os.path.join(qdir, "*.json")))
    if not jobs:
        log("money: queue empty (cloud/queue/money)")
        return 3
    import mrender
    made, errors = 0, []
    for jf in jobs:
        if made >= a.max:
            break
        stem = os.path.splitext(os.path.basename(jf))[0]
        if os.path.exists(os.path.join(a.out, stem + ".json")):
            continue
        try:
            sc = json.load(open(jf))
            bad = check(sc, used)
        except Exception as e:
            sc, bad = {}, f"bad json: {e}"
        if bad:
            ext = ".dup" if "already used" in bad else ".bad"
            log(f"money: skip {stem}: {bad}")
            if not a.only:
                os.replace(jf, jf + ext)
            continue
        mp4 = os.path.join(a.out, stem + ".mp4")
        work = os.path.join(a.home, "work", "money", stem)
        try:
            log(f"money: rendering {stem}: {sc['title']}")
            r = mrender.render(sc, mp4, work, log=log)
        except Exception as e:
            import traceback
            traceback.print_exc()
            errors.append(f"{stem}: {e}")
            continue
        meta = {"file": stem + ".mp4", "kind": "short", "title": sc["title"].strip(), "description": description(sc),
                "tags": tags_of(sc), "queue_file": os.path.relpath(jf, repo).replace(os.sep, "/")}
        json.dump(meta, open(os.path.join(a.out, stem + ".json"), "w"), ensure_ascii=False, indent=1)
        used.add(norm(sc["title"]))
        if not os.environ.get("MONEY_KEEP_WORK"):
            shutil.rmtree(work, ignore_errors=True)
        made += 1
        log(f"money: made {stem}.mp4 ({r['duration']:.1f}s, {r['seconds_render']:.0f}s render)")
    if made:
        return 0
    if errors:
        print("money: render failed: " + "; ".join(errors), file=sys.stderr)
        return 1
    log("money: nothing usable in the queue")
    return 3


if __name__ == "__main__":
    t0 = time.time()
    rc = main()
    log(f"money: done in {time.time() - t0:.0f}s, exit {rc}")
    sys.exit(rc)

#!/usr/bin/env python3
"""Maker for "Roblox Top 10 Daily" (key roblox) — teen/adult Roblox news & rankings, never kids content.

    python3 cloud/makers/roblox.py --out DIR --home HOME --repo ROOT --titles TITLES.json --need-long 0|1 --need-short 0|1
    python3 cloud/makers/roblox.py --offline-test --out /tmp/x --home /tmp/h      (fixture data, no internet)

One run = one pack: 1 long Top 10 countdown (1920x1080, 3-6 min, thumbnail) + 2 Shorts (1080x1920, 30-45 s)
when a long is needed, else 2 Shorts. Data: public Roblox web APIs at run time; daily snapshots in HOME/snapshots/
give "+X visits since yesterday", climbers and losers. Helpers live in cloud/makers/roblox/ (rbx_*.py).
Exit 0 = made videos, 3 = nothing needed, other = error.
"""
import argparse
import datetime as dt
import json
import os
import random
import sys
import time
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "roblox"))

import rbx_data  # noqa: E402
import rbx_text  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--home", default=os.path.expanduser("~/roblox_home"))
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--titles", default="")
    ap.add_argument("--need-long", type=int, default=1)
    ap.add_argument("--need-short", type=int, default=1)
    ap.add_argument("--offline-test", action="store_true", help="use cloud/makers/roblox/fixture.json, no network")
    ap.add_argument("--shorts", type=int, default=2)
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--long-mode", default="", help="players|gainers (testing; default rotates by day)")
    ap.add_argument("--formats", default="", help="force short formats, e.g. visits,guess (testing)")
    a = ap.parse_args()
    if not a.need_long and not a.need_short:
        print("nothing needed")
        return 3
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(a.home, exist_ok=True)
    t0 = time.time()
    today = dt.date.today()
    used = []
    if a.titles and os.path.exists(a.titles):
        try:
            used = json.load(open(a.titles))
        except Exception:
            used = []
    titles = rbx_text.Titles(used)
    games, back = rbx_data.load(a.home, today, a.offline_test)
    print(f"data: {len(games)} games, previous snapshot {back} day(s) back, #1 {games[0]['clean']} "
          f"{games[0].get('playing')} playing ({time.time() - t0:.0f}s)")
    state_f = os.path.join(a.home, "maker_state.json")
    try:
        state = json.load(open(state_f))
    except Exception:
        state = {"runs": 0}
    runs = state.get("runs", 0)
    rng = random.Random(f"{today}-{runs}")
    pack = f"rbx{today.strftime('%Y%m%d')}-{runs:03d}"
    workers = a.workers or None
    made = []
    import rbx_long
    import rbx_shorts
    if a.need_long:
        meta = rbx_long.build(games, back, titles, a.out, f"{pack}-0-long", rng, today, workers=workers,
                              voice=rng.choice(["am_adam", "am_michael"]), force_mode=a.long_mode)
        meta.pop("top", None)
        meta.pop("mode", None)
        made.append((f"{pack}-0-long", meta))
    n_short = a.shorts if (a.need_short or a.need_long) else 0
    rot = rbx_shorts.ROTATION
    order = [f for f in a.formats.split(",") if f] or [rot[(runs * 2 + k) % len(rot)] for k in range(len(rot))]
    k = 1
    for f in order:
        if k > n_short:
            break
        try:
            meta = rbx_shorts.build(f, games, back, titles, rng, a.out, f"{pack}-{k}-short", today,
                                    voice=rng.choice(["am_michael", "am_adam", "am_eric"]), workers=workers)
        except Exception:
            traceback.print_exc()
            meta = None
        if not meta:
            print(f"short format {f}: skipped (no data or no unused title)")
            continue
        if not a.need_long:  # no long in this pack -> no {LONG_URL}
            meta["description"] = meta["description"].replace(" Full Top 10: {LONG_URL}", "").replace(
                " Today's full Top 10: {LONG_URL}", "")
        made.append((f"{pack}-{k}-short", meta))
        k += 1
    for name, meta in made:
        meta["pack"] = pack
        meta["made_for_kids"] = False
        json.dump(meta, open(os.path.join(a.out, name + ".json"), "w"), ensure_ascii=False, indent=1)
    state["runs"] = runs + 1
    state["last"] = {"pack": pack, "titles": [m["title"] for _, m in made], "at": dt.datetime.now().isoformat()}
    json.dump(state, open(state_f, "w"), indent=1)
    print(f"made {len(made)} video(s) in {time.time() - t0:.0f}s: " + " | ".join(m["title"] for _, m in made))
    return 0 if made else 2


if __name__ == "__main__":
    sys.exit(main())

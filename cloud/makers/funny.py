#!/usr/bin/env python3
"""Funny Rank Daily (`funny`) maker — ranked #5→#1 funny-moment Shorts from CC BY YouTube clips.

    python3 cloud/makers/funny.py --out DIR --home HOME --repo ROOT --titles TITLES.json --need-long 0|1 --need-short 0|1
    python3 cloud/makers/funny.py --offline-test [--out DIR]      # no internet: 5 synthetic clips → 1 Short

One run = up to 3 Shorts (config per_day short 6 → the worker calls it again for the rest).
Per Short: theme not in the last ~30 titles → YouTube search (videoLicense=creativeCommon, ≤2 search calls) →
videos.list double-checks status.license == creativeCommon → yt-dlp ≤720p → best 4-6 s moment of each of 5 clips
(audio-energy jump + motion peak) → ranked by peak strength → Kokoro voice + synthesized music bed → mp4 + json.
Every clip is credited in the description ("Clips (CC BY): title — channel — link").
Exit 0 = made something, 3 = nothing to make (e.g. need-short 0), other = error.
"""
import argparse
import datetime as dt
import json
import os
import random
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "funny"))
import fr_themes as TH  # noqa: E402
import fr_source as SRC  # noqa: E402
import fr_render as R  # noqa: E402

PER_RUN = 3
RUN_BUDGET_S = 100 * 60
HASHTAGS = "#shorts #funny #fails #ranking #funnyvideos"


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def description(sc, clips, theme_name):
    lines = [f"Which one got you? {sc['hook'].replace('number one', '#1')} 😂",
             f"Our own top 5 {theme_name.lower()}, ranked from #5 to #1 with our commentary. Comment your #1!", "",
             "Clips (CC BY):"]
    for r, c in zip((5, 4, 3, 2, 1), clips):
        lines.append(f"#{r} {c['title']} — {c['channel']} — https://youtu.be/{c['id']}")
    lines += ["", "All clips are used under the Creative Commons Attribution license (CC BY 3.0); "
              "thank you to every creator above. Edited, ranked and narrated by Funny Rank Daily.", "",
              HASHTAGS + " #" + TH.slug(theme_name).replace("-", "")]
    return "\n".join(lines)


def tags(theme_name):
    base = theme_name.lower()
    return [base, base.replace(" fails", " fail"), "funny " + base, "ranking", "top 5", "funny fails", "fails",
            "funny moments", "try not to laugh", "funny videos", "shorts", "funny rank daily"]


def selfcheck(mp4, title):
    """Same gate the worker uses (tools/rek_ball.py). Below 85 → one try with its kuchaytir (punch-in re-edit)."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools"))
        import rek_ball
    except Exception as e:
        log("rek_ball not importable:", e)
        return None
    r = rek_ball.baho(mp4, title, "short")
    log("rek-ball", r["ball"], r["qism"], r["muammo"])
    if r["ball"] >= 85:
        return r["ball"]
    try:
        nf = rek_ball.kuchaytir(mp4, "short")
        r2 = rek_ball.baho(nf, title, "short")
        log("rek-ball after kuchaytir", r2["ball"], r2["muammo"])
        if r2["ball"] > r["ball"]:
            os.replace(nf, mp4)
            return r2["ball"]
        os.remove(nf)
    except Exception as e:
        log("kuchaytir failed:", str(e)[:200])
    return r["ball"]


def build(clips, theme, sc, out_dir, name, work, titles, seed, rng):
    """clips: list of ≥5 dicts with 'file'. Picks moments, ranks, renders, writes mp4+json. Returns item or None."""
    scored = []
    for c in clips:
        try:
            m = R.best_moment(c["file"], 6.3)
        except Exception as e:  # broken download
            log("analyse failed", c.get("id"), str(e)[:200])
            continue
        if m["dur"] < 3.0 or not m["w"]:
            continue
        c["m"] = m
        scored.append(c)
        if len(scored) == 5:
            break
    if len(scored) < 5:
        log(f"only {len(scored)} usable clips for {theme[0]}")
        return None
    order = sorted(scored, key=lambda c: c["m"]["score"])  # weakest = #5 … strongest = #1
    title = TH.make_title(theme[0], titles, rng)
    mp4 = os.path.join(out_dir, name + ".mp4")
    info = R.render_short(order, theme[0], sc, mp4, work, seed=seed, log=log)
    ball = selfcheck(mp4, title)
    if ball is not None:
        info["rek"] = ball
        if ball < 85:
            log(f"rek-ball {ball} < 85 → not handed to the worker")
            os.remove(mp4)
            return None
    item = {"file": name + ".mp4", "kind": "short", "title": title,
            "description": description(sc, order, theme[0]), "tags": tags(theme[0]),
            "sources": [{"rank": r, "id": c["id"], "title": c["title"], "channel": c["channel"],
                         "peak_s": c["m"]["peak"]} for r, c in zip((5, 4, 3, 2, 1), order)],
            "render": info}
    json.dump(item, open(os.path.join(out_dir, name + ".json"), "w"), ensure_ascii=False, indent=1)
    log("made", name, "|", title, "|", info)
    return item, order


def offline_test(args):
    out = args.out or tempfile.mkdtemp(prefix="funny_out_")
    os.makedirs(out, exist_ok=True)
    work = tempfile.mkdtemp(prefix="funny_work_")
    titles = json.load(open(args.titles)) if args.titles and os.path.exists(args.titles) else []
    rng = random.Random(args.seed)
    home = args.home or work
    theme = TH.pick_themes(titles, home, 1, rng)[0]
    sc = TH.script(rng)
    log("OFFLINE TEST theme:", theme[0])
    clips = SRC.synth_clips(os.path.join(work, "src"), 5, seed=args.seed)
    t = time.time()
    res = build(clips, theme, sc, out, "funny-offline-test", os.path.join(work, "r"), titles, args.seed, rng)
    log(f"total {time.time() - t:.0f}s →", os.path.join(out, "funny-offline-test.mp4"))
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0 if res else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--home")
    ap.add_argument("--repo")
    ap.add_argument("--titles")
    ap.add_argument("--need-long", type=int, default=0)
    ap.add_argument("--need-short", type=int, default=1)
    ap.add_argument("--count", type=int, default=PER_RUN)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--offline-test", action="store_true")
    ap.add_argument("--keep", action="store_true", help="keep the work dir (debug)")
    args = ap.parse_args()
    if args.seed is None:
        args.seed = int(time.time()) % 100000
    if args.offline_test:
        return offline_test(args)
    if not args.need_short:
        log("no Shorts needed (this channel makes Shorts only)")
        return 3
    if not (args.out and args.home):
        print("--out and --home are required", file=sys.stderr)
        return 2
    os.makedirs(args.out, exist_ok=True)
    titles = json.load(open(args.titles)) if args.titles and os.path.exists(args.titles) else []
    titles = [t if isinstance(t, str) else (t.get("title") or "") for t in titles]
    rng = random.Random(args.seed)
    sys.path.insert(0, os.path.dirname(HERE))  # cloud/ → youtube_up.py
    import youtube_up
    yt = youtube_up.client(os.path.join(args.home, "token.json"))
    finder = SRC.Finder(yt, args.home, log)
    cache = os.path.join(args.home, "funny_cache")
    os.makedirs(cache, exist_ok=True)
    t_start = time.time()
    made, tried = [], set()
    max_search = 2 * args.count + 2
    for theme in TH.pick_themes(titles, args.home, args.count * 3, rng):
        if len(made) >= args.count or finder.searches >= max_search:
            break
        if time.time() - t_start > RUN_BUDGET_S:
            log("run time budget reached")
            break
        if theme[0] in tried:
            continue
        tried.add(theme[0])
        log("theme:", theme[0])
        try:
            cands = finder.candidates(theme)
        except Exception as e:
            r = str(e)
            log("search failed:", r[:300])
            if "quota" in r.lower() or "rateLimit" in r:
                break
            continue
        log(f"{len(cands)} CC BY candidates (searches so far {finder.searches})")
        if len(cands) < 5:
            continue
        work = tempfile.mkdtemp(prefix="funny_", dir=cache)
        got = []
        for c in cands[:9]:
            f = SRC.download(c["id"], os.path.join(cache, "src"), log)
            if f:
                c["file"] = f
                got.append(c)
            if len(got) >= 6:  # one spare in case a file is broken
                break
        if len(got) < 5:
            log("not enough downloads for", theme[0])
            shutil.rmtree(work, ignore_errors=True)
            continue
        name = f"funny-{dt.date.today():%Y%m%d}-{TH.slug(theme[0])}-{int(time.time()) % 10000}"
        sc = TH.script(rng)
        try:
            res = build(got, theme, sc, args.out, name, work, titles + [m["title"] for m in made],
                        rng.randint(0, 99999), rng)
        except Exception as e:
            log("render failed", theme[0], str(e)[:500])
            res = None
        shutil.rmtree(work, ignore_errors=True)
        if not res:
            continue
        item, used = res
        made.append(item)
        SRC.save_used(args.home, [c["id"] for c in used])
        hist = TH.load_hist(args.home)
        hist[theme[0]] = dt.date.today().isoformat()
        TH.save_hist(args.home, hist)
    # source files are only needed while rendering; keep disk small
    shutil.rmtree(os.path.join(cache, "src"), ignore_errors=True)
    log(f"done: {len(made)} Short(s); API calls: search {finder.searches}, list {finder.lists}")
    if not made:
        print("no Short made (no CC BY clips found / downloads failed / quota)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

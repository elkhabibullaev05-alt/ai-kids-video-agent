#!/usr/bin/env python3
"""Wild Sketchbook (key `ufc`) maker — rebuilds the lost PC agent's ink/sketch renderer.

python3 cloud/makers/ufc.py --out DIR --home HOME --repo ROOT --titles TITLES.json --need-long 0|1 --need-short 0|1
                            [--offline-test] [--script cloud/ink/animals/NNN-slug.json] [--keep-work]

From the oldest script in cloud/ink/animals/ that is not made yet:
  <id>-0-long.mp4/.json/.jpg  1920x1080, 8-11 min ink-sketch explainer (Kokoro narration, Wikipedia lead photos
                              redrawn as pencil sketches, punch-in camera, hook / #N badges / handwritten labels,
                              subscribe scene at the end)
  <id>-1-short.mp4/.json      1080x1920, 45-59 s, word-by-word captions, loops, "full story on my channel" banner
Made ids are kept in HOME/made_ids.json. Exit 3 = nothing left to make.
--offline-test: no network (placeholder photos), long limited to the first 8 scenes (UFC_TEST_SCENES).
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ufc"))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import art  # noqa: E402
import render  # noqa: E402
import voice  # noqa: E402
import wiki  # noqa: E402

FPS = render.FPS
LW, LH = 1920, 1080
LBASE = (2208, 1242)
SW, SH = 1080, 1920
CARD = (0, 0, 1080, 1920)   # Shorts: full-bleed vertical sketch
SBASE = (1188, 2112)
CAP_Y = 1110                 # captions (bottom 20% and right edge stay clear)
TOP_Y = 190                  # hook / labels below the header strip
MAX_LONG = 14 * 60 + 40
MAX_SHORT = 58.5
CTA_LINE = "Want one animal secret every day? Subscribe to the Wild Sketchbook."


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ bookkeeping
def load_state(home):
    p = os.path.join(home, "made_ids.json")
    try:
        d = json.load(open(p))
    except Exception:
        d = {}
    if isinstance(d, list):
        d = {"done": d}
    d.setdefault("done", [])
    d.setdefault("parts", {})
    return d


def save_state(home, st):
    p = os.path.join(home, "made_ids.json")
    json.dump(st, open(p + ".tmp", "w"), indent=1)
    os.replace(p + ".tmp", p)


def norm(t):
    return " ".join("".join(c if c.isalnum() else " " for c in (t or "").lower()).split())


OLD_MADE_MAX = 12  # last cloud/ink/animals script number the old ufctube agent rendered
SEED_BEFORE = os.environ.get("UFC_SEED_BEFORE", "2026-10-30")  # old laptop broke ~30 Oct: older scripts were made by it


def seed_state(a, st):
    """First run only (no made_ids.json): scripts committed before SEED_BEFORE count as made by the lost agent."""
    import subprocess
    sdir = os.path.join(a.repo, "cloud", "ink", "animals")
    for f in sorted(os.listdir(sdir)):
        if not f.endswith(".json"):
            continue
        try:
            d = subprocess.run(["git", "-C", a.repo, "log", "--diff-filter=A", "--format=%cI", "--", os.path.join(sdir, f)],
                               capture_output=True, text=True, timeout=30).stdout.split()
        except Exception:
            return
        if d and d[-1][:10] < SEED_BEFORE:
            st["done"].append(os.path.splitext(f)[0])
    log(f"first run: {len(st['done'])} scripts older than {SEED_BEFORE} marked as already made")


def pick_script(a, st, titles):
    sdir = os.path.join(a.repo, "cloud", "ink", "animals")
    files = [a.script] if a.script else sorted(f for f in os.listdir(sdir) if f.endswith(".json"))
    want = {k for k, n in (("long", a.need_long), ("short", a.need_short)) if n}
    changed = False
    for f in files:
        path = f if os.path.isabs(f) or os.path.exists(f) else os.path.join(sdir, f)
        try:
            sc = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            log(f"skip {f}: bad json ({e})")
            continue
        sid = sc.get("id") or os.path.splitext(os.path.basename(path))[0]
        if sid in st["done"] and not a.script:
            continue
        # 2026-11-06: scripts 001–012 were already made by the lost laptop agent (git dates are unreliable in a
        # shallow clone, so the first-run seeding missed them and 001 was made twice). Never make them again.
        m = re.match(r"(\d+)", os.path.basename(path))
        if m and int(m.group(1)) <= OLD_MADE_MAX and not a.script:
            continue
        parts = set(st["parts"].get(sid, []))
        if norm(sc.get("title")) in titles or sid in titles:
            parts.add("long")
        if not (sc.get("short") or {}).get("scenes") or norm((sc.get("short") or {}).get("title")) in titles:
            parts.add("short")
        if not sc.get("scenes"):
            parts.add("long")
        if {"long", "short"} <= parts and not a.script:
            st["done"].append(sid)
            st["parts"].pop(sid, None)
            changed = True
            continue
        todo = want - parts if not a.script else want
        if todo:
            return sid, sc, path, todo, changed
    return None, None, None, set(), changed


# ------------------------------------------------------------------ images
def gather_images(sc, kinds, cache, offline):
    titles = []
    if "long" in kinds:
        titles += [s.get("img", "") for s in sc["scenes"]]
    if "short" in kinds:
        titles += [s.get("img", "") for s in sc["short"]["scenes"]]
        titles += [s.get("img", "") for s in sc.get("scenes", [])]  # extra Shorts are cut from the long's sections
    photos, metas = {}, {}
    for t in dict.fromkeys(x for x in titles if x):
        if offline:
            photos[t] = art.placeholder_photo(t, int(hashlib.md5(t.encode()).hexdigest()[:6], 16))
            metas[t] = {"file": t + " (placeholder)", "license": "test", "artist": "", "page": "", "needs_credit": False}
            continue
        p, m = wiki.lead_image(t, cache, log)
        if p:
            try:
                im = Image.open(p)
                im.load()
                photos[t] = im.convert("RGB")
                metas[t] = m
            except Exception as e:
                log(f"  img '{t}': unreadable ({e})")
    return photos, metas


def resolve(scenes, photos):
    """For every scene the image title actually used (fallback: nearest scene with a free photo) or None."""
    have = [s.get("img") if s.get("img") in photos else None for s in scenes]
    out = []
    for i, h in enumerate(have):
        if h:
            out.append(h)
            continue
        cand = [have[j] for j in sorted(range(len(have)), key=lambda j: (abs(j - i), j > i)) if have[j]]
        out.append(cand[0] if cand else None)
    return out


def credits(used, metas):
    lines = []
    for t in dict.fromkeys(used):
        m = metas.get(t)
        if not m or not m.get("needs_credit"):
            continue
        who = m.get("artist") or "unknown author"
        lines.append(f"- {t}: \"{m['file']}\" by {who}, {m['license']} — {m['page']}")
    return lines


def clean_desc(s, limit=4900):
    s = s.replace("<", "(").replace(">", ")")
    return s[:limit]


def _cut(x, n):
    """Shorten a source line without breaking a URL in half."""
    if len(x) <= n:
        return x
    cut = x[:n]
    sp = cut.rfind(" ")
    if sp > 0 and not x[n:n + 1].isspace() and cut[sp + 1:].startswith("http"):
        cut = cut[:sp]
    elif sp > n * 0.6 and not x[n:n + 1].isspace():
        cut = cut[:sp]
    return cut.rstrip(" ;,(") + " …"


def build_desc(head, sc, cred_lines, extra=""):
    src = ["- " + _cut(x, 330) for x in sc.get("sources", [])]
    parts = [head.strip()]
    if extra:
        parts.append(extra)
    parts.append("Sources:\n" + "\n".join(src))
    img = "Pictures: Wikipedia lead photos (Wikimedia Commons, free licences) redrawn as pencil sketches."
    if cred_lines:
        img += "\n" + "\n".join(cred_lines)
    parts.append(img)
    parts.append("Narration: synthetic voice (Kokoro). Music: generated ambient pad.")
    d = "\n\n".join(parts)
    while len(d) > 4900 and src:  # keep image credits (licence requirement); shorten sources first
        src = [_cut(x, 160) for x in src]
        parts[-3 if not extra else -3] = "Sources:\n" + "\n".join(src)
        d = "\n\n".join(parts)
        if len(d) > 4900:
            src = src[:-1]
    return clean_desc(d)


def tags_of(sc):
    out, n = [], 0
    for t in sc.get("tags", []):
        t = t.replace("<", "").replace(">", "").strip()
        if t and n + len(t) + 1 <= 480:
            out.append(t)
            n += len(t) + 1
    return out


# ------------------------------------------------------------------ audio
def narrate(scenes, gap, speed, extra_tail=None):
    """-> (audio, starts, durs, words_per_scene)."""
    chunks, starts, durs, words = [], [], [], []
    t = 0.0
    lines = [s.get("say", "") for s in scenes] + ([extra_tail] if extra_tail else [])
    for i, line in enumerate(lines):
        a, w = voice.say(line, speed=speed)
        g = np.zeros(int(gap * voice.SR), np.float32) if i < len(lines) - 1 else np.zeros(int(0.5 * voice.SR), np.float32)
        starts.append(t)
        durs.append((len(a) + len(g)) / voice.SR)
        words.append(w)
        chunks += [a, g]
        t += durs[-1]
        if (i + 1) % 10 == 0:
            log(f"  voice {i + 1}/{len(lines)}  {t / 60:.1f} min")
    return np.concatenate(chunks), starts, durs, words


def frames_for(starts, durs):
    total = starts[-1] + durs[-1]
    edges = [round(s * FPS) for s in starts] + [round(total * FPS)]
    return [edges[i + 1] - edges[i] for i in range(len(starts))]


# ------------------------------------------------------------------ overlays
def save_png(im, work, name):
    p = os.path.join(work, name + ".png")
    im.save(p)
    return p


def subscribe_panel(repo, work):
    """Returns frame(t) for the end card: avatar + SUBSCRIBE button that gets clicked by a drawn cursor."""
    bg = Image.fromarray(art.paper(LW, LH, 5)).convert("RGBA")
    av_p = os.path.join(repo, "cloud", "ink", "brand", "wild_sketchbook_avatar_800.png")
    states = []
    for clicked in (False, True):
        im = bg.copy()
        d = ImageDraw.Draw(im)
        if os.path.exists(av_p):
            av = Image.open(av_p).convert("RGBA").resize((340, 340))
            m = Image.new("L", (340, 340), 0)
            ImageDraw.Draw(m).ellipse((0, 0, 339, 339), fill=255)
            im.paste(av, (300, 300), m)
        d.ellipse((290, 290, 650, 650), outline=art.INK, width=6)
        t = art.text_layer("Wild Sketchbook", "hand", 900, 140, 120, fill=art.INK, stroke=(255, 250, 235), sw=3, max_lines=1)
        im.alpha_composite(t, (720, 280))
        t2 = art.text_layer("one animal secret a day", "hand", 900, 90, 70, fill=(90, 70, 55), stroke=(255, 250, 235), sw=2,
                            max_lines=1)
        im.alpha_composite(t2, (730, 420))
        bx, by, bw, bh = 760, 560, 560, 140
        if clicked:
            d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=30, fill=(120, 116, 110))
            f = art.font("bold", 62)
            d.text((bx + 60, by + 34), "SUBSCRIBED", font=f, fill=(245, 245, 245))
            # bell
            cx, cy = bx + bw + 110, by + bh // 2
            d.pieslice((cx - 50, cy - 60, cx + 50, cy + 40), 180, 360, fill=art.INK)
            d.rectangle((cx - 50, cy - 10, cx + 50, cy + 30), fill=art.INK)
            d.ellipse((cx - 14, cy + 30, cx + 14, cy + 58), fill=art.INK)
        else:
            d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=30, fill=(204, 0, 0))
            f = art.font("bold", 66)
            d.text((bx + 72, by + 32), "SUBSCRIBE", font=f, fill=(255, 255, 255))
        states.append(np.asarray(im.convert("RGB")))
    cur = Image.new("RGBA", (70, 100), (0, 0, 0, 0))
    ImageDraw.Draw(cur).polygon([(4, 4), (4, 80), (24, 62), (40, 96), (54, 90), (38, 56), (64, 56)], fill=(255, 255, 255, 255),
                                outline=(0, 0, 0, 255), width=4)
    cur_ov = art.to_overlay(cur, 0, 0)
    target = (1040, 640)
    rng = random.Random(1)
    sparks = [(rng.uniform(0, 6.28), rng.uniform(80, 160)) for _ in range(10)]

    def frame(t):
        clicked = t >= 1.6
        fr = states[1 if clicked else 0].copy()
        # gentle push-in so the end card never freezes
        z = 1.0 + 0.04 * min(t, 6) / 6
        if z > 1.001:
            fr = render.view(Image.fromarray(fr), LW, LH, z, 0.55, 0.5).copy()
        u = min(1.0, t / 1.4)
        u = u * u * (3 - 2 * u)
        x = int(1700 + (target[0] - 1700) * u)
        y = int(1000 + (target[1] - 1000) * u)
        if 1.5 <= t < 1.7:
            y += 6
        if 1.6 <= t < 2.1:  # click burst
            d = Image.fromarray(fr)
            dd = ImageDraw.Draw(d)
            r = (t - 1.6) / 0.5
            for ang, ln in sparks:
                x0 = target[0] + np.cos(ang) * ln * (0.4 + r)
                y0 = target[1] + np.sin(ang) * ln * (0.4 + r)
                dd.line((x0, y0, x0 + np.cos(ang) * 30, y0 + np.sin(ang) * 30), fill=(255, 200, 0), width=7)
            fr = np.asarray(d).copy()
        ox, oy, rgb, a = cur_ov
        art.composite(fr, (x, y, rgb, a))
        return fr

    return frame


def caption_chunks(words, max_words=3):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or w[0][-1:] in ".,!?;:":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def caption_png(chunk, active, work, name):
    f = art.font("bold", 104)
    d = ImageDraw.Draw(Image.new("L", (8, 8)))
    sp = d.textlength(" ", font=f)
    words = [w[0].upper() for w in chunk]
    # wrap to <= 860 px
    lines, cur, cw = [], [], 0
    for i, w in enumerate(words):
        ww = d.textlength(w, font=f)
        if cur and cw + sp + ww > 860:
            lines.append(cur)
            cur, cw = [], 0
        cur.append((i, w, ww))
        cw += (sp if cw else 0) + ww
    lines.append(cur)
    lh = 124
    Wd = int(max(sum(x[2] for x in l) + sp * (len(l) - 1) for l in lines)) + 40
    Ht = lh * len(lines) + 40
    im = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    y = 14
    for l in lines:
        lw = sum(x[2] for x in l) + sp * (len(l) - 1)
        x = (Wd - lw) / 2
        for i, w, ww in l:
            fill = art.YELLOW if i == active else (255, 255, 255)
            dd.text((x, y), w, font=f, fill=fill, stroke_width=10, stroke_fill=(0, 0, 0))
            x += ww + sp
        y += lh
    return save_png(im, work, name), Wd, Ht


# ------------------------------------------------------------------ LONG
def make_long(sc, photos, metas, a, work, out_dir, pack):
    scenes = sc["scenes"]
    if a.offline_test:
        scenes = scenes[: int(os.environ.get("UFC_TEST_SCENES", "8"))]
    used = resolve(scenes, photos)
    speed = voice.SPEED
    while True:
        log(f"long: narration of {len(scenes)} scenes (speed {speed:.2f})")
        audio, starts, durs, _ = narrate(scenes, 0.2, speed, extra_tail=CTA_LINE)
        total = len(audio) / voice.SR
        if total <= MAX_LONG or speed >= 1.3:
            break
        speed += 0.07
    log(f"long: {total / 60:.2f} min")
    audio = voice.mix(audio, -25)
    wav = os.path.join(work, "long.wav")
    sf.write(wav, audio, voice.SR)
    nfr = frames_for(starts, durs)

    keys = list(dict.fromkeys(u or ("card:" + (s.get("img") or sc["title"])) for u, s in zip(used, scenes)))
    bases, idx = [], {}
    for k in keys:
        if k.startswith("card:"):
            bases.append(art.title_card(k[5:], *LBASE, seed=len(bases)))
        else:
            bases.append(art.sketch(photos[k], *LBASE, seed=len(bases)))
        idx[k] = len(bases) - 1
    rng = random.Random(pack)
    rs, prev = [], None
    mid = len(scenes) // 2
    for i, s in enumerate(scenes):
        k = used[i] or ("card:" + (s.get("img") or sc["title"]))
        dur = nfr[i] / FPS
        ovs = []
        if s.get("hook"):
            hk = art.text_layer(s["hook"].upper(), "marker", 1500, 420, 150, sw=12, rot=rng.uniform(-3, 3))
            ovs.append(dict(png=save_png(hk, work, f"hook{i}"), x=(LW - hk.width) // 2, y=max(20, int(LH * 0.36 - hk.height / 2)),
                            t0=0, t1=dur + 1, fade_in=0 if i == 0 else 0.15))
        if s.get("num"):
            b = art.badge_layer(s["num"])
            ovs.append(dict(png=save_png(b, work, f"num{i}"), x=40, y=30, t0=0.0, t1=dur + 1, fade_in=0.12))
        if s.get("label"):
            lb = art.label_layer(s["label"])
            ovs.append(dict(png=save_png(lb, work, f"lab{i}"), x=(LW - lb.width) // 2, y=LH - lb.height - 70,
                            t0=0.25, t1=dur + 1, fade_in=0.2))
        if i == mid:
            c = art.text_layer("Subscribe for one animal secret a day", "hand", 760, 100, 56, fill=(255, 255, 255),
                               stroke=(0, 0, 0), sw=4, bg=(204, 0, 0, 230), pad=20, max_lines=1)
            ovs.append(dict(png=save_png(c, work, f"cta{i}"), x=LW - c.width - 40, y=40, t0=0.3, t1=min(dur, 5.0),
                            fade_in=0.2, fade_out=0.3))
        rs.append(dict(n=nfr[i], base=idx[k], shots=plan_shots_for(dur, rng, 2.3, i == 0), overlays=ovs,
                       reveal=(i > 0 and k != prev)))
        prev = k
    rs.append(dict(n=nfr[-1], special="subscribe", overlays=[]))
    out = os.path.join(out_dir, f"{pack}-0-long.mp4")
    t0 = time.time()
    render.render_video(rs, bases, {}, LW, LH, work, wav, out, subscribe=subscribe_panel(a.repo, work), procs=a.procs)
    log(f"long rendered in {time.time() - t0:.0f} s -> {out}")
    # thumbnail
    th_src = next((photos[u] for u in used if u), None)
    art.thumbnail(th_src, sc.get("thumb_text") or sc["title"], os.path.join(out_dir, f"{pack}-0-long.jpg"))
    desc = build_desc(sc.get("description", ""), sc, credits([u for u in used if u], metas),
                      "Subscribe for one animal secret a day — this is the Wild Sketchbook.")
    meta = {"file": f"{pack}-0-long.mp4", "kind": "long", "title": sc["title"][:100], "description": desc,
            "tags": tags_of(sc), "thumb": f"{pack}-0-long.jpg", "pack": pack}
    json.dump(meta, open(os.path.join(out_dir, f"{pack}-0-long.json"), "w"), ensure_ascii=False, indent=1)
    return out


def plan_shots_for(dur, rng, L, first, end_at=None):
    return render.plan_shots(dur, rng, L, first=first, end_at=end_at)


# ------------------------------------------------------------------ SHORT
def make_short(sc, sh, photos, metas, a, work, out_dir, pack, num=1):
    scenes = sh["scenes"]
    used = resolve(scenes, photos)
    speed = voice.SPEED + 0.03
    while True:
        log(f"short: narration of {len(scenes)} scenes (speed {speed:.2f})")
        audio, starts, durs, words = narrate(scenes, 0.12, speed)
        total = len(audio) / voice.SR
        if total <= MAX_SHORT or speed >= 1.35:
            break
        speed += 0.06
    # loop: no trailing silence
    tail = int(0.45 * voice.SR)
    audio = audio[:-tail] if len(audio) > tail * 3 else audio
    durs[-1] -= tail / voice.SR
    log(f"short: {len(audio) / voice.SR:.1f} s")
    audio = voice.mix(audio, -24)
    wav = os.path.join(work, "short.wav")
    sf.write(wav, audio, voice.SR)
    nfr = frames_for(starts, durs)

    # static background: paper + header + card frame
    bgs = {"s": np.zeros((SH, SW, 3), np.uint8)}
    hdr = art.text_layer(sh.get("header") or sc["title"], "hand", 860, 100, 64, fill=art.INK, stroke=(255, 250, 235), sw=2,
                         max_lines=1, bg=art.PAPER + (235,), pad=18)
    fpng = save_png(hdr, work, "sheader")
    hdr_xy = (max(20, 470 - hdr.width // 2), 50)

    keys = list(dict.fromkeys(u or ("card:" + (s.get("img") or sh["title"])) for u, s in zip(used, scenes)))
    bases, idx = [], {}
    for k in keys:
        if k.startswith("card:"):
            bases.append(art.title_card(k[5:], *SBASE, seed=len(bases)))
        else:
            bases.append(art.sketch(photos[k], *SBASE, seed=len(bases), centering=(0.5, 0.45), wash=0.6))
        idx[k] = len(bases) - 1
    rng = random.Random(pack + "s")
    rs, prev = [], None
    first_cam = (1.42, 0.5, 0.45)
    k0 = used[0] or ("card:" + (scenes[0].get("img") or sh["title"]))
    hook_png = None
    for i, s in enumerate(scenes):
        k = used[i] or ("card:" + (s.get("img") or sh["title"]))
        dur = nfr[i] / FPS
        last = i == len(scenes) - 1
        ovs = [dict(png=fpng, x=hdr_xy[0], y=hdr_xy[1], t0=0, t1=dur + 1)]
        if i == 0 and s.get("hook"):
            hk = art.text_layer(s["hook"].upper(), "marker", 940, 520, 150, sw=12, rot=-2)
            hook_png = save_png(hk, work, "shook")
            hook_xy = ((SW - hk.width) // 2, TOP_Y)
            ovs.append(dict(png=hook_png, x=hook_xy[0], y=hook_xy[1], t0=0, t1=min(dur, 3.2), fade_out=0.25))
        if s.get("label") and not (i == 0 and s.get("hook")):
            lb = art.label_layer(s["label"], maxw=900)
            ovs.append(dict(png=save_png(lb, work, f"slab{i}"), x=max(10, 470 - lb.width // 2), y=TOP_Y, t0=0.2,
                            t1=(dur - 0.6) if last else dur + 1, fade_in=0.15, fade_out=0.2 if last else 0))
        # word-by-word captions
        ws = words[i]
        chunks = caption_chunks(ws)
        flat = [(ci, j) for ci, ch in enumerate(chunks) for j in range(len(ch))]
        for n_, (ci, j) in enumerate(flat):
            w = chunks[ci][j]
            t0 = 0.0 if n_ == 0 else w[1]
            t1 = flat[n_ + 1] and chunks[flat[n_ + 1][0]][flat[n_ + 1][1]][1] if n_ + 1 < len(flat) else dur + 1
            p, cw, chh = caption_png(chunks[ci], j, work, f"cap{i}_{n_}")
            ovs.append(dict(png=p, x=max(20, min(470 - cw // 2, 900 - cw)), y=CAP_Y, t0=t0, t1=t1))
        if last:
            bn = art.text_layer("FULL STORY ON MY CHANNEL", "bold", 860, 110, 72, fill=(255, 255, 255), stroke=(0, 0, 0), sw=3,
                                bg=(204, 0, 0, 240), pad=22, max_lines=1)
            ovs.append(dict(png=save_png(bn, work, "banner"), x=max(20, 470 - bn.width // 2), y=1430,
                            t0=0.0, t1=max(0.5, dur - 0.55), fade_in=0.15, fade_out=0.2))
            if hook_png:  # loop: the hook comes back on the last frames so the end matches frame 0
                ovs.append(dict(png=hook_png, x=hook_xy[0], y=hook_xy[1], t0=max(0, dur - 0.45), t1=dur + 1, fade_in=0.3))
        shots = render.plan_shots(dur, rng, 0.85, first=(i == 0), end_at=first_cam if last else None, first_len=0.5,
                                   drift=0.5, min_jump=0.26, zmax=1.42)
        if last and used[i] != used[0]:
            pass
        rs.append(dict(n=nfr[i], base=idx[k if not last else (k0 if used[0] else k)], shots=shots, overlays=ovs, card=CARD,
                       bg="s", reveal=(i > 0 and k != prev and not last)))
        prev = k
    out = os.path.join(out_dir, f"{pack}-{num}-short.mp4")
    t0 = time.time()
    render.render_video(rs, bases, bgs, SW, SH, work, wav, out, procs=a.procs)
    log(f"short rendered in {time.time() - t0:.0f} s -> {out}")
    desc = build_desc(sh.get("description", "") + "\n\nFull story: {LONG_URL}", sc,
                      credits([u for u in used if u], metas))
    tags = tags_of(sc)
    if "Shorts" not in tags:
        tags.append("Shorts")
    meta = {"file": f"{pack}-{num}-short.mp4", "kind": "short", "title": sh["title"][:100], "description": desc,
            "tags": tags, "pack": pack}
    json.dump(meta, open(os.path.join(out_dir, f"{pack}-{num}-short.json"), "w"), ensure_ascii=False, indent=1)
    return out


# ------------------------------------------------------------------ extra Shorts cut from the long
def _section(scenes, start, lo=85, hi=135):
    out, words = [], 0
    for s in scenes[start:]:
        if out and (s.get("num") or words >= lo):
            break
        w = len(s.get("say", "").split())
        if out and words + w > hi:
            break
        out.append(dict(s))
        words += w
    return out, words


def _tcase(t):
    return " ".join(w if (w[:1] == "#" or w.isdigit()) else w.capitalize() for w in t.lower().split())


def _unique(title, used):
    t = title[:60].strip()
    if norm(t) not in used:
        return t
    for suf in (" (Part 2)", " - Wild Sketchbook", " #Shorts"):
        u = (title[:60 - len(suf)].strip() + suf)
        if norm(u) not in used:
            return u
    return None


def extra_shorts(sc, used, n=2):
    """Two more vertical Shorts from the long script: the #1 reveal and the opening hook (fallback: #2, #3...)."""
    scenes = sc.get("scenes") or []
    nums = {s.get("num"): i for i, s in enumerate(scenes) if s.get("num")}
    topic = _tcase(sc.get("thumb_text") or sc["short"].get("header") or "")
    cands = [("#1", nums["#1"])] if "#1" in nums else []
    cands.append(("intro", 0))
    cands += [(k, nums[k]) for k in ("#2", "#3", "#4", "#5") if k in nums]
    out = []
    for kind, i in cands:
        if len(out) >= n:
            break
        sec, words = _section(scenes, i)
        if words < 70 or len(sec) < 3:
            continue
        first = sec[0]
        lab = next((s.get("label") for s in sec if s.get("label")), "")
        same = lambda x, y: norm(x).strip("?!. ") == norm(y).strip("?!. ")
        if kind == "intro":
            hook = first.get("hook") or lab or topic
            title = _tcase(hook)
            if topic and not same(hook, topic):
                title += f" | {topic}"
            if len(title) < 18:
                title += " (Wait For It)"
        else:
            hook = f"{kind}: {lab}" if lab else f"{kind} {topic}"
            title = f"The {kind} Secret: {_tcase(lab)}" if lab else f"The {kind} Secret Is Wild"
            if topic and not same(lab, topic):
                title += f" | {topic}"
        title = _unique(title, used)
        if not title:
            continue
        used.add(norm(title))
        sec[0] = dict(sec[0], hook=hook[:40])
        sec[-1] = dict(sec[-1], img=first.get("img"))  # same picture first and last -> clean loop
        for s in sec[1:]:
            s.pop("hook", None)
            s.pop("num", None)
        desc = (f"{lab or hook} - one moment from today's Wild Sketchbook video. " if (lab or hook) else "") + \
            "Subscribe for one animal secret a day."
        out.append({"title": title, "header": sc["short"].get("header") or topic, "description": desc, "scenes": sec})
    return out


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--titles", default="")
    ap.add_argument("--need-long", type=int, default=1)
    ap.add_argument("--need-short", type=int, default=1)
    ap.add_argument("--offline-test", action="store_true")
    ap.add_argument("--script", default="")
    ap.add_argument("--procs", type=int, default=0)
    ap.add_argument("--keep-work", action="store_true")
    a = ap.parse_args()
    if not (a.need_long or a.need_short):
        log("nothing needed")
        sys.exit(3)
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(a.home, exist_ok=True)
    titles = set()
    if a.titles and os.path.exists(a.titles):
        try:
            titles = {norm(t) for t in json.load(open(a.titles, encoding="utf-8")) if isinstance(t, str)}
        except Exception:
            pass
    first = not os.path.exists(os.path.join(a.home, "made_ids.json"))
    st = load_state(a.home)
    if first and not a.script and not a.offline_test:
        seed_state(a, st)
        save_state(a.home, st)
    sid, sc, path, todo, changed = pick_script(a, st, titles)
    if changed and not a.offline_test:
        save_state(a.home, st)
    if not sid:
        log("no new script in cloud/ink/animals — nothing to make")
        sys.exit(3)
    log(f"script {sid}: making {sorted(todo)}")
    art.setup_fonts(a.home, offline=a.offline_test)
    voice.set_cache(os.path.join(a.home, "tts_cache"))
    t_start = time.time()
    photos, metas = gather_images(sc, todo, os.path.join(a.home, "img_cache"), a.offline_test)
    log(f"images: {len(photos)} free photos")
    work = tempfile.mkdtemp(prefix="ufc_", dir=a.home)
    made = []
    try:
        if "long" in todo:
            wl = os.path.join(work, "long")
            os.makedirs(wl)
            made.append(make_long(sc, photos, metas, a, wl, a.out, sid))
        if "short" in todo:
            used_titles = set(titles) | {norm(sc.get("title")), norm(sc["short"].get("title"))}
            shorts = [sc["short"]] + extra_shorts(sc, used_titles)
            for n, sh in enumerate(shorts, 1):
                ws = os.path.join(work, f"short{n}")
                os.makedirs(ws)
                try:
                    made.append(make_short(sc, sh, photos, metas, a, ws, a.out, sid, n))
                except Exception as e:
                    if n == 1:
                        raise
                    log(f"extra short {n} failed: {e}")
    finally:
        if not a.keep_work:
            shutil.rmtree(work, ignore_errors=True)
    if not a.offline_test:
        parts = set(st["parts"].get(sid, [])) | todo
        if {"long", "short"} <= parts or not (sc.get("short") or {}).get("scenes"):
            st["done"].append(sid)
            st["parts"].pop(sid, None)
        else:
            st["parts"][sid] = sorted(parts)
        save_state(a.home, st)
    log(f"done in {(time.time() - t_start) / 60:.1f} min: {made}")


if __name__ == "__main__":
    main()

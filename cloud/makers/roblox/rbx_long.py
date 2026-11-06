"""Daily long video: Top 10 countdown (#10 -> #1), 1920x1080 30 fps, hook at frame 0, chapters, thumbnail."""
import math
import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import rbx_audio as au
import rbx_gfx as gx
import rbx_text as tx
import rbx_video

W, H, FPS = 1920, 1080, 30
PX, PY, PW, PH = 80, 200, 1120, 630  # main panel
CX, CW = 1270, 590  # stat column


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def _panel_mask():
    m = Image.new("L", (PW, PH), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, PW - 1, PH - 1), 22, fill=255)
    return m


class Entry:
    def __init__(self, g, rank, banner, seed, total_ranks=10):
        self.g, self.rank, self.banner = g, rank, banner
        th = gx.load_rgb(g["thumb"])
        ic = gx.load_rgb(g["icon"], (512, 512))
        t2 = gx.load_rgb(g["thumb2"]) if g.get("thumb2") else th
        self.bg = gx.blur_bg(th, W, H, dark=0.5)
        # icon card view
        card = gx.blur_bg(th, PW, PH, radius=18, dark=0.35, scale=1.0)
        icn = gx.framed(gx.cover(ic, 470, 470), 8, gx.WHITE, 40)
        card.paste(icn, (PW // 2 - icn.width // 2, PH // 2 - icn.height // 2), icn)
        self.views = [gx.KenBurns(th, PW, PH, (1.0, 1.22), seed=seed),
                      gx.KenBurns(card, PW, PH, (1.18, 1.0), pan=(0, 0, 0, 0)),
                      gx.KenBurns(t2, PW, PH, (1.25, 1.05), seed=seed + 1)]
        self.acc = gx.accent(g["clean"])
        # static overlay: name, creator, top bar
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rectangle((0, 0, W, 92), fill=(10, 12, 28, 235))
        gx.draw_text(d, (40, 46), "TOP 10 ROBLOX GAMES RIGHT NOW", gx.font(40), gx.WHITE, anchor="lm")
        for k in range(total_ranks, 0, -1):  # progress chips 10..1
            x = W - 70 - (k - 1) * 66
            on = k == rank
            done = k > rank
            d.rounded_rectangle((x - 28, 22, x + 28, 70), 12,
                                fill=gx.YELLOW if on else ((70, 80, 110) if done else (35, 40, 60)))
            gx.draw_text(d, (x, 46), str(k), gx.font(28), gx.BLACK if on else gx.WHITE, anchor="mm")
        nf = gx.fit_font(g["clean"].upper(), PW, 96, 40)
        gx.draw_text(d, (PX, 905), g["clean"].upper(), nf, gx.WHITE, stroke=6, anchor="lm")
        sub = " · ".join(x for x in [("by " + g["creator_name"]) if g.get("creator_name") else "", g.get("genre", "")] if x)
        gx.draw_text(d, (PX + 4, 990), sub, gx.fit_font(sub, PW, 40, 24), (200, 205, 220), stroke=3, anchor="lm")
        self.ov = ov.convert("RGB")
        self.ov_mask = ov.split()[3]
        self.mask = _panel_mask()
        self.cards = self._cards()

    def _cards(self):
        g = self.g
        cards = [("LIVE PLAYERS", g.get("playing") or 0, "", gx.RED),
                 ("TOTAL VISITS", g.get("visits") or 0, "", gx.CYAN)]
        if g.get("d_visits"):
            cards.append(("VISITS SINCE YESTERDAY", g["d_visits"], "+", gx.GREEN))
        else:
            cards.append(("FAVORITES", g.get("favoritedCount") or 0, "", gx.YELLOW))
        if g.get("d_play_pct") is not None and abs(g["d_play_pct"]) >= 3:
            p = g["d_play_pct"]
            cards.append(("PLAYERS VS YESTERDAY", p, "%", gx.GREEN if p > 0 else gx.RED))
        elif g.get("like"):
            cards.append(("LIKE RATIO", g["like"], "%", (255, 150, 60)))
        else:
            cards.append(("CREATED", g.get("year") or 0, "Y", (255, 150, 60)))
        return cards

    def frame(self, lt, dur):
        u = lt / max(dur, 0.1)
        bw, bh = self.bg.size
        ox = int((bw - W) / 2 + math.sin(lt * 0.35) * (bw - W) / 2.2)
        oy = int((bh - H) / 2 + math.cos(lt * 0.27) * (bh - H) / 2.2)
        im = self.bg.crop((ox, oy, ox + W, oy + H))
        d = ImageDraw.Draw(im)
        # panel view switches at 1/3 and 2/3 (cut events)
        k = 0 if u < 0.34 else (1 if u < 0.67 else 2)
        seg_u = (u - (0, 0.34, 0.67)[k]) / (0.34, 0.33, 0.33)[k]
        punch = 1.0 + 0.12 * max(0.0, 1 - seg_u * 6)
        view = self.views[k].at(seg_u, punch)
        slide = int((1 - ease(lt / 0.35)) * 900)
        x = PX + slide
        d.rounded_rectangle((x - 8, PY - 8, x + PW + 8, PY + PH + 8), 30, fill=self.acc)
        im.paste(view, (x, PY), self.mask)
        im.paste(self.ov, (0, 0), self.ov_mask)
        # rank badge
        s = 1.0 + 0.5 * max(0.0, 1 - lt / 0.3)
        f = gx.font(int(150 * s))
        gx.draw_text(d, (PX + 10 + slide // 3, PY - 30), f"#{self.rank}", f, gx.YELLOW, stroke=10, anchor="lt",
                     shadow=8)
        # stat cards
        for i, (lab, val, mode, col) in enumerate(self.cards):
            t0 = 0.5 + i * 0.9
            if lt < t0:
                continue
            a = ease((lt - t0) / 0.3)
            y = PY + i * 160
            cx = CX + int((1 - a) * 500)
            d.rounded_rectangle((cx, y, cx + CW, y + 140), 20, fill=(14, 16, 34))
            d.rectangle((cx, y + 14, cx + 12, y + 126), fill=col)
            gx.draw_text(d, (cx + 36, y + 30), lab, gx.font(30), (190, 195, 215), anchor="lm")
            cnt = min(1.0, (lt - t0) / 0.9)
            v = val * (1 - (1 - cnt) ** 2)
            if mode == "%":
                txt = f"{'+' if val > 0 and lab.startswith('PLAYERS') else ''}{int(round(v))}%"
            elif mode == "Y":
                txt = str(int(val)) if cnt >= 1 else str(int(2006 + (val - 2006) * cnt))
            else:
                txt = mode + gx.short_num(v)
            gx.draw_text(d, (cx + 36, y + 92), txt, gx.font(66), gx.WHITE, anchor="lm")
            if i == 0:  # pulsing LIVE dot
                r = 12 + 4 * math.sin(lt * 6)
                d.ellipse((cx + CW - 60 - r, y + 30 - r, cx + CW - 60 + r, y + 30 + r), fill=gx.RED)
        # why it's hot banner
        if self.banner and u > 0.42:
            a = ease((u - 0.42) * dur / 0.3)
            by = 860 + int((1 - a) * 260)
            bf = gx.fit_font(self.banner, CW - 50, 44, 22)
            d.rounded_rectangle((CX, by, CX + CW, by + 110), 20, fill=gx.YELLOW)
            gx.draw_text(d, (CX + 24, by + 28), "WHY IT'S HOT", gx.font(26), (90, 60, 0), anchor="lm")
            gx.draw_text(d, (CX + 24, by + 74), self.banner, bf, gx.BLACK, anchor="lm")
        if lt < 0.1:  # flash on entry (cut)
            im = Image.blend(im, Image.new("RGB", im.size, gx.WHITE), 0.55)
        elif k and seg_u * (0.33 * dur) < 0.07:
            im = Image.blend(im, Image.new("RGB", im.size, gx.WHITE), 0.4)
        return im


class Hook:
    def __init__(self, top):
        th = gx.load_rgb(top[0]["thumb"])
        self.bg = gx.KenBurns(th.filter(ImageFilter.GaussianBlur(14)), W, H, (1.35, 1.0), pan=(0, 0, 0, 0))
        self.icons = [gx.framed(gx.cover(gx.load_rgb(g["icon"], (512, 512)), 190, 190), 5, gx.WHITE, 24)
                      for g in top[1:10]]

    def frame(self, lt, dur):
        im = self.bg.at(min(1, lt / max(dur, 1)))
        im = Image.blend(im, Image.new("RGB", im.size, (10, 10, 30)), 0.25)
        d = ImageDraw.Draw(im)
        pulse = 1 + 0.06 * math.sin(lt * 7)
        gx.draw_text(d, (W // 2, 250), "TODAY'S #1 IS...", gx.font(int(130 * pulse)), gx.YELLOW, stroke=10,
                     anchor="mm", shadow=8)
        gx.draw_text(d, (W // 2, 540), "?", gx.font(int(330 * pulse)), gx.WHITE, stroke=14, anchor="mm", shadow=10)
        gx.draw_text(d, (W // 2, 770), "TOP 10 BY LIVE PLAYERS", gx.font(64), gx.WHITE, stroke=6, anchor="mm")
        # icon conveyor
        n = len(self.icons)
        span = n * 230
        off = (lt * 380) % span
        for i, ic in enumerate(self.icons):
            x = int(W - ((i * 230 + off) % span) - 100)
            im.paste(ic, (x, 860), ic)
        return im


class Outro:
    def __init__(self, top):
        self.top = top
        self.bg = gx.KenBurns(gx.load_rgb(top[0]["thumb"]).filter(ImageFilter.GaussianBlur(16)), W, H, (1.0, 1.2))
        self.icons = [gx.framed(gx.cover(gx.load_rgb(g["icon"], (512, 512)), 230, 230), 6,
                                gx.YELLOW if i == 0 else gx.WHITE, 26) for i, g in enumerate(top[:10])]

    def frame(self, lt, dur):
        im = Image.blend(self.bg.at(lt / max(dur, 1)), Image.new("RGB", (W, H), (8, 8, 24)), 0.45)
        d = ImageDraw.Draw(im)
        gx.draw_text(d, (W // 2, 120), "WHO TAKES #1 TOMORROW?", gx.font(100), gx.YELLOW, stroke=8, anchor="mm",
                     shadow=6)
        for i, ic in enumerate(self.icons):
            t0 = 0.15 * (9 - i)
            if lt < t0:
                continue
            row, col = divmod(i, 5)
            x = 190 + col * 320
            y = 260 + row * 360
            s = ease((lt - t0) / 0.25)
            if i == 0:
                s *= 1 + 0.05 * math.sin(lt * 6)
            sz = max(10, int(ic.width * s))
            icr = ic.resize((sz, sz))
            im.paste(icr, (x + (ic.width - sz) // 2, y + (ic.width - sz) // 2), icr)
            gx.draw_text(d, (x + 20, y + 10), f"#{i + 1}", gx.font(60), gx.YELLOW if i == 0 else gx.WHITE, stroke=6)
            nm = self.top[i]["clean"]
            gx.draw_text(d, (x + ic.width // 2, y + ic.width + 30), nm, gx.fit_font(nm, 300, 34, 18), gx.WHITE,
                         stroke=4, anchor="mm")
        gx.draw_text(d, (W // 2, 1010), "COMMENT YOUR PICK  ·  SUBSCRIBE FOR TOMORROW'S TOP 10", gx.font(48),
                     gx.WHITE, stroke=5, anchor="mm")
        return im


def thumbnail(top, path, rng, mode):
    g = top[0]
    im = gx.cover(gx.load_rgb(g["thumb"]), 1280, 720)
    im = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), 0.15)
    sh = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for x in range(700):  # left dark gradient for text
        sd.line([(x, 0), (x, 720)], fill=(0, 0, 0, int(200 * (1 - x / 700))))
    im = Image.alpha_composite(im.convert("RGBA"), sh).convert("RGB")
    d = ImageDraw.Draw(im)
    words = rng.choice([["NEW", "#1?"], ["TOP 10", "TODAY"], ["WHO'S", "#1?"], ["#1 RIGHT", "NOW"]]) \
        if mode != "gainers" else rng.choice([["FASTEST", "GROWING"], ["+" + gx.short_num(g.get("d_visits")), "IN 1 DAY"]])
    gx.draw_text(d, (40, 150), words[0], gx.fit_font(words[0], 640, 170), gx.WHITE, stroke=12, anchor="lm", shadow=8)
    gx.draw_text(d, (40, 330), words[1], gx.fit_font(words[1], 640, 190), gx.YELLOW, stroke=12, anchor="lm", shadow=8)
    for i, gg in enumerate(top[1:4]):
        ic = gx.framed(gx.cover(gx.load_rgb(gg["icon"], (512, 512)), 170, 170), 6, gx.WHITE, 20)
        im.paste(ic, (40 + i * 200, 500), ic)
        gx.draw_text(d, (50 + i * 200, 505), f"#{i + 2}", gx.font(46), gx.WHITE, stroke=5)
    big = gx.framed(gx.cover(gx.load_rgb(g["icon"], (512, 512)), 330, 330), 10, gx.YELLOW, 36)
    im.paste(big, (1280 - 380, 300), big)
    gx.draw_text(d, (1280 - 380 + 20, 290), "#1", gx.font(120), gx.YELLOW, stroke=10, shadow=6)
    im.save(path, quality=92)
    return path


def build(games, back, titles, out_dir, name, rng, day, workers=None, voice="am_adam"):
    t_start = time.time()
    mode = "players"
    if back == 1 and day.toordinal() % 3 == 0:
        gainers = sorted([g for g in games[:40] if g.get("d_visits")], key=lambda g: -g["d_visits"])
        if len(gainers) >= 10:
            mode = "gainers"
            games = gainers
    top = games[:10]
    prev1 = None
    if mode == "players":
        p1 = [g for g in games if g.get("prev_rank") == 1]
        prev1 = p1[0]["clean"] if p1 else None
    segs = [("hook", None, tx.hook_script(top, prev1, rng, mode), None)]
    for r in range(10, 0, -1):
        txt, banner = tx.entry_script(top[r - 1], r, rng, mode)
        segs.append(("entry", r, txt, banner))
    segs.append(("outro", None, tx.outro_script(top, rng), None))
    # narration
    voice_parts, timeline, t = [], [], 0.0
    sfx_marks = []
    for kind, r, txt, banner in segs:
        a, _ = au.tts(txt, voice=voice, speed=1.1)
        pad = 0.45 if kind == "entry" else 0.3
        dur = len(a) / au.SR + pad
        if kind == "hook":
            dur = max(dur, 6.0)
        timeline.append(dict(kind=kind, rank=r, start=t, dur=dur, banner=banner, text=txt))
        voice_parts.append((t + (0.25 if kind == "entry" else 0.0), a))
        if kind != "hook":
            sfx_marks.append(t)
        t += dur
    total = t + 0.5
    timeline[-1]["dur"] += 0.5
    print(f"long: mode={mode} narration {total:.1f}s (tts {time.time() - t_start:.0f}s)")
    vbuf = np.zeros(int(total * au.SR) + au.SR, np.float32)
    for st, a in voice_parts:
        au.place(vbuf, a, st)
    sbuf = np.zeros_like(vbuf)
    for m in sfx_marks:
        au.place(sbuf, au.whoosh(seed=int(m * 10)), max(0, m - 0.2), 0.8)
    music = au.beat(total + 1, bpm=rng.choice([112, 118, 124]), seed=day.toordinal())
    wav = os.path.join(out_dir, name + ".wav")
    au.mix_and_master(vbuf, music, sbuf, total, wav, music_gain=0.13)
    # visuals
    objs = []
    for s in timeline:
        if s["kind"] == "hook":
            objs.append(Hook(top))
        elif s["kind"] == "outro":
            objs.append(Outro(top))
        else:
            objs.append(Entry(top[s["rank"] - 1], s["rank"], s["banner"], seed=s["rank"] * 7 + day.toordinal()))
    starts = [s["start"] for s in timeline]

    def frame_fn(i):
        tt = i / FPS
        k = max(0, np.searchsorted(starts, tt, side="right") - 1)
        return objs[k].frame(tt - starts[k], timeline[k]["dur"])

    nframes = int(total * FPS)
    mp4 = os.path.join(out_dir, name + ".mp4")
    rbx_video.render(frame_fn, nframes, W, H, FPS, wav, mp4, workers)
    os.remove(wav)
    title = tx.long_titles(top, mode, titles, rng)
    chapters = []
    for s in timeline:
        mm, ss = divmod(int(s["start"]), 60)
        lab = "Intro" if s["kind"] == "hook" else ("Who takes #1 tomorrow?" if s["kind"] == "outro"
                                                    else f"#{s['rank']} {top[s['rank'] - 1]['clean']}")
        chapters.append(f"{mm}:{ss:02d} {lab}")
    jpg = os.path.join(out_dir, name + ".jpg")
    thumbnail(top, jpg, rng, mode)
    print(f"long: rendered {total:.1f}s in {time.time() - t_start:.0f}s")
    return dict(file=name + ".mp4", kind="long", title=title,
                description=tx.long_description(title, top, chapters, mode, day),
                tags=tx.TAGS + [g["clean"].lower() for g in top[:5]], thumb=name + ".jpg",
                top=[g["clean"] for g in top], mode=mode)

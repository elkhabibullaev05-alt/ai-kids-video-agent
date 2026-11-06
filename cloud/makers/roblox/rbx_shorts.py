"""Shorts (1080x1920, 30 fps, 30-45 s): one fact on screen at frame 0, word-by-word captions, loop ending.

Formats: visits | players | climber | losers | guess | versus. Each is a list of cards:
    card = dict(say=<sentence>, head=<headline>, sub=<small line>, vis=<hero|stat|chart|blur|duo>, ...)
"""
import math
import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import rbx_audio as au
import rbx_gfx as gx
import rbx_text as tx
import rbx_video
from rbx_gfx import say_num, short_num

W, H, FPS = 1080, 1920, 30
VX, VY, VW, VH = 60, 600, 960, 540  # hero visual box
CAP_Y = 1330


def _sweep():
    m = Image.new("L", (260, VH), 0)
    dd = ImageDraw.Draw(m)
    for k in range(60):
        a = int(120 * (1 - abs(k - 30) / 30))
        dd.polygon([(100 + k, 0), (101 + k, 0), (1 + k, VH), (k, VH)], fill=a)
    return m


SWEEP = _sweep()


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- formats

def _pick_game(games, titles, rng, key, n=15, min_val=0):
    pool = [g for g in games[:n] if (g.get(key) or 0) > min_val]
    pool.sort(key=lambda g: (titles.recent_mentions(g["clean"]), -(g.get(key) or 0) * rng.uniform(0.6, 1.0)))
    return pool[0] if pool else None


def fmt_visits(games, titles, rng, back):
    g = _pick_game(sorted(games[:25], key=lambda g: -(g.get("visits") or 0)), titles, rng, "visits")
    if not g:
        return None
    V = short_num(g["visits"])
    n = g["clean"]
    title = titles.pick([f"{V} Visits?! {n} #shorts", f"{n} Has {V} Visits?! #shorts",
                         f"How Does {n} Have {V} Visits? #shorts", f"{V} Visits on {n}?! #shorts"], rng)
    if not title:
        return None
    times = g["visits"] / 8.2e9
    cmp_line = (f"That is about {times:.0f} visits for every person on Earth." if times >= 1.5 else
                f"That is more visits than there are people on Earth." if times >= 1 else
                f"That is about one visit for every {1 / times:.0f} people on the planet.")
    cards = [dict(say=f"{n} has {say_num(g['visits'])} visits.", head=f"{V} VISITS?!", vis="hero", g=g),
             dict(say=cmp_line, head="MORE THAN EARTH?" if times >= 1 else "INSANE NUMBER", vis="stat", g=g,
                  val=g["visits"], lab="TOTAL VISITS"),
             dict(say=f"Right now, {say_num(g.get('playing'))} people are playing it.", head="LIVE RIGHT NOW",
                  vis="stat", g=g, val=g.get("playing"), lab="PLAYING NOW", live=True),
             dict(say=f"That puts it at number {g['rank']} on today's live player chart.", head=f"#{g['rank']} TODAY",
                  vis="chart", g=g, games=games, metric="playing")]
    if g.get("d_visits"):
        cards.append(dict(say=f"And it gained {say_num(g['d_visits'])} visits since yesterday alone.",
                          head=f"+{short_num(g['d_visits'])} IN 1 DAY", vis="stat", g=g, val=g["d_visits"],
                          lab="SINCE YESTERDAY", plus=True))
    if g.get("year"):
        cards.append(dict(say=f"It launched in {g['year']}, made by {g.get('creator_name') or 'its team'}.",
                          head=f"SINCE {g['year']}", vis="hero", g=g, alt=True))
    if g.get("favoritedCount"):
        cards.append(dict(say=f"{say_num(g['favoritedCount'])} players saved it to their favorites"
                              + (f", and {g['like']} percent of votes are likes." if g.get("like") else "."),
                          head=f"{short_num(g['favoritedCount'])} FAVORITES", vis="stat", g=g,
                          val=g["favoritedCount"], lab="FAVORITES"))
    cards.append(dict(say=f"Have you played it? Comment below, and watch that visit counter go up again.",
                      head=f"{V} VISITS?!", vis="hero", g=g, loop=True))
    desc = (f"{n} just passed {V} visits ({g['visits']:,} total) with {short_num(g.get('playing'))} playing right now. "
            f"Today's full Top 10: {{LONG_URL}}")
    return title, cards, desc, [n.lower(), "roblox visits"]


def fmt_players(games, titles, rng, back):
    g = _pick_game(games, titles, rng, "playing", n=12)
    if not g:
        return None
    P = short_num(g["playing"])
    n = g["clean"]
    title = titles.pick([f"{P} Playing Right Now?! {n} #shorts", f"{P} People Are Playing {n} RIGHT NOW #shorts",
                         f"Why Are {P} People Playing {n}? #shorts"], rng)
    if not title:
        return None
    facts = tx.hot_facts(g)
    facts.sort(key=lambda x: -x[2])
    cards = [dict(say=f"{say_num(g['playing'])} people are playing {n} right now.", head=f"{P} PLAYING?!",
                  vis="hero", g=g),
             dict(say=f"That makes it number {g['rank']} on all of Roblox at this moment.", head=f"#{g['rank']} RIGHT NOW",
                  vis="chart", g=g, games=games, metric="playing")]
    for s, b, _ in facts[:3]:
        cards.append(dict(say=s, head=b if len(b) <= 18 else "WHY IT'S HOT", sub=b if len(b) > 18 else "",
                          vis="hero", g=g, alt=len(cards) % 2 == 0))
    cards.append(dict(say=f"With {say_num(g.get('visits'))} visits in total.", head=f"{short_num(g.get('visits'))} VISITS",
                      vis="stat", g=g, val=g.get("visits"), lab="ALL-TIME VISITS"))
    cards.append(dict(say="Are you one of them? Tell me in the comments.", head=f"{P} PLAYING?!", vis="hero", g=g,
                      loop=True))
    desc = f"{n} has {g['playing']:,} players online right now (#{g['rank']} on Roblox today). Full Top 10: {{LONG_URL}}"
    return title, cards, desc, [n.lower(), "roblox players"]


def fmt_climber(games, titles, rng, back):
    if not back:
        return None
    pool = [g for g in games[:40] if g.get("d_play_pct") is not None and (g.get("playing") or 0) > 4000
            and g["d_play_pct"] >= 8 and titles.recent_mentions(g["clean"]) < 3]
    if not pool:
        return None
    g = max(pool, key=lambda g: g["d_play_pct"])
    n, pct = g["clean"], g["d_play_pct"]
    title = titles.pick([f"Biggest Roblox Climber Today: {n} (+{pct}%) #shorts",
                         f"{n} Just Gained {pct}% More Players?! #shorts",
                         f"Why Is {n} Suddenly Blowing Up? (+{pct}%) #shorts"], rng)
    if not title:
        return None
    facts = sorted(tx.hot_facts(g), key=lambda x: -x[2])
    cards = [dict(say=f"The biggest Roblox climber today is {n}.", head=f"+{pct}% TODAY", vis="hero", g=g),
             dict(say=f"Its player count is up {pct} percent since yesterday.", head="PLAYERS SINCE YESTERDAY",
                  vis="stat", g=g, val=pct, lab="PLAYER GROWTH", pct=True),
             dict(say=f"That is {say_num(g['playing'])} people online right now.", head=f"{short_num(g['playing'])} LIVE",
                  vis="stat", g=g, val=g["playing"], lab="PLAYING NOW", live=True)]
    if g.get("prev_rank") and g["prev_rank"] != g["rank"]:
        cards.append(dict(say=f"It moved from number {g['prev_rank']} to number {g['rank']} on the live chart.",
                          head=f"#{g['prev_rank']} → #{g['rank']}", vis="chart", g=g, games=games, metric="playing"))
    for s, b, _ in facts[:2]:
        cards.append(dict(say=s, head="WHY?", sub=b, vis="hero", g=g, alt=True))
    cards.append(dict(say="Will it keep climbing tomorrow? Comment yes or no.", head=f"+{pct}% TODAY", vis="hero",
                      g=g, loop=True))
    desc = f"{n} grew {pct}% in players since yesterday ({g['playing']:,} online now). Full Top 10: {{LONG_URL}}"
    return title, cards, desc, [n.lower(), "trending roblox games"]


def fmt_losers(games, titles, rng, back):
    if not back:
        return None
    pool = [g for g in games[:30] if g.get("d_play") is not None and g["d_play"] < 0 and (g.get("playing") or 0) > 3000]
    if len(pool) < 3:
        return None
    lo = sorted(pool, key=lambda g: g["d_play"])[:3]
    title = titles.pick(["These 3 Roblox Games Lost the Most Players Today #shorts",
                         f"{lo[0]['clean']} Lost {short_num(-lo[0]['d_play'])} Players?! #shorts",
                         "3 Roblox Games Players Are Leaving Right Now #shorts",
                         f"Is {lo[0]['clean']} Dying? Lost {short_num(-lo[0]['d_play'])} Players #shorts"], rng)
    if not title:
        return None
    cards = [dict(say="These three Roblox games lost the most players since yesterday.", head="LOSING PLAYERS?!",
                  vis="duo3", gs=lo, g=lo[0])]
    for i, g in enumerate(reversed(lo)):
        k = 3 - i
        cards.append(dict(say=f"Number {k}: {g['clean']}, down {say_num(-g['d_play'])} players"
                              + (f", that is {abs(g['d_play_pct'])} percent." if g.get("d_play_pct") else "."),
                          head=f"#{k} -{short_num(-g['d_play'])}", vis="stat", g=g, val=-g["d_play"],
                          lab="PLAYERS LOST", minus=True))
        if k == 1 and g.get("upd_days") is not None:
            cards.append(dict(say=f"Its last update was {tx.ago(g['upd_days'])}.", head="WHY?",
                              sub=f"LAST UPDATE {tx.ago(g['upd_days']).upper()}", vis="hero", g=g, alt=True))
    cards.append(dict(say="Still playing any of these? Tell me in the comments.", head="LOSING PLAYERS?!", vis="duo3",
                      gs=lo, g=lo[0], loop=True))
    desc = ("Biggest player drops since yesterday: " + ", ".join(f"{g['clean']} ({g['d_play']:,})" for g in lo)
            + ". Full Top 10: {LONG_URL}")
    return title, cards, desc, ["roblox games dying", "roblox player count"]


def fmt_guess(games, titles, rng, back):
    top = games[:7]
    n1 = top[0]
    title = titles.pick(["Can You Guess Today's #1 Roblox Game? #shorts",
                         f"Guess Today's #1 Roblox Game ({short_num(n1['playing'])} Players) #shorts",
                         "Only Real Fans Can Guess Today's #1 Roblox Game #shorts",
                         f"Guess the #1 Roblox Game Right Now (Hint: {n1.get('genre') or 'Huge'}) #shorts",
                         "Today's #1 Roblox Game Is NOT What You Think #shorts"], rng)
    if not title:
        return None
    cards = [dict(say="Can you guess today's number one Roblox game? Let's count down.", head="GUESS TODAY'S #1",
                  vis="blur", g=n1)]
    for k in range(7, 1, -1):
        g = top[k - 1]
        cards.append(dict(say=f"Number {k}: {g['clean']}, with {say_num(g['playing'])} players.",
                          head=f"#{k} {short_num(g['playing'])}", vis="hero", g=g, alt=k % 2 == 0))
    cards.append(dict(say=f"Number one has {say_num(n1['playing'])} players. Last chance to guess.",
                      head="#1 = ???", vis="blur", g=n1))
    cards.append(dict(say=f"It's {n1['clean']}!", head=f"#1 {n1['clean'].upper()}", vis="hero", g=n1, reveal=True))
    cards.append(dict(say="Did you get it right? Comment your guess for tomorrow.", head="GUESS TODAY'S #1",
                      vis="blur", g=n1, loop=True))
    desc = f"Today's top 7 by live players: " + ", ".join(f"#{i + 1} {g['clean']}" for i, g in enumerate(top)) + \
           ". Full Top 10: {LONG_URL}"
    return title, cards, desc, ["guess the roblox game", "roblox quiz"]


def fmt_versus(games, titles, rng, back):
    pool = games[:12]
    for _ in range(12):
        a, b = rng.sample(pool, 2)
        if a["rank"] > b["rank"]:
            a, b = b, a
        t = titles.pick([f"{a['clean']} vs {b['clean']}: Which Has More Players? #shorts",
                         f"{b['clean']} vs {a['clean']} — Who Wins Right Now? #shorts"], rng)
        if t:
            break
    else:
        return None
    title = t
    rounds = [("LIVE PLAYERS", "playing", "players right now"), ("TOTAL VISITS", "visits", "total visits"),
              ("FAVORITES", "favoritedCount", "favorites")]
    cards = [dict(say=f"{a['clean']} versus {b['clean']}. Which one is bigger right now?",
                  head="WHO WINS?", vis="duo", gs=[a, b], g=a)]
    score = [0, 0]
    for lab, key, spoken in rounds:
        va, vb = a.get(key) or 0, b.get(key) or 0
        w = 0 if va >= vb else 1
        score[w] += 1
        cards.append(dict(say=f"{spoken.capitalize()}: {say_num(va)} against {say_num(vb)}. Point {[a, b][w]['clean']}.",
                          head=lab, vis="duo", gs=[a, b], g=a, vals=[va, vb], win=w))
    if a.get("like") and b.get("like"):
        w = 0 if a["like"] >= b["like"] else 1
        score[w] += 1
        cards.append(dict(say=f"Like ratio: {a['like']} percent against {b['like']} percent.", head="LIKE RATIO",
                          vis="duo", gs=[a, b], g=a, vals=[a["like"], b["like"]], win=w, pct=True))
    win = [a, b][0 if score[0] >= score[1] else 1]
    cards.append(dict(say=f"{win['clean']} wins, {max(score)} to {min(score)}.", head=f"{win['clean'].upper()} WINS",
                      vis="hero", g=win, reveal=True))
    cards.append(dict(say="Which one do you play? Comment below.", head="WHO WINS?", vis="duo", gs=[a, b], g=a,
                      loop=True))
    desc = f"{a['clean']} vs {b['clean']} with live numbers from today. Full Top 10: {{LONG_URL}}"
    return title, cards, desc, [a["clean"].lower(), b["clean"].lower(), "roblox vs"]


def extra_cards(g, rng):
    out = []
    for s_, b, _ in sorted(tx.hot_facts(g), key=lambda x: -x[2]):
        out.append(dict(say=s_, head=b if len(b) <= 18 else "WHY IT'S HOT", sub=b if len(b) > 18 else "",
                        vis="hero", g=g, alt=len(out) % 2 == 0))
    if g.get("creator_name"):
        out.append(dict(say=f"It is made by {g['creator_name']}" + (f", and it started back in {g['year']}." if g.get("year") else "."),
                        head="WHO MADE IT?", sub=g["creator_name"].upper(), vis="hero", g=g, alt=True))
    if g.get("maxPlayers"):
        out.append(dict(say=f"Each server holds up to {g['maxPlayers']} players, so that is a lot of full servers.",
                        head=f"{short_num((g.get('playing') or 0) / max(1, g['maxPlayers']))}+ SERVERS",
                        vis="stat", g=g, val=(g.get("playing") or 0) / max(1, g["maxPlayers"]), lab="FULL SERVERS NOW"))
    return out


FORMATS = {"visits": fmt_visits, "players": fmt_players, "climber": fmt_climber, "losers": fmt_losers,
           "guess": fmt_guess, "versus": fmt_versus}
ROTATION = ["visits", "climber", "guess", "players", "losers", "versus", "visits", "guess", "climber", "players",
            "versus", "losers"]


# ---------------------------------------------------------------- render

class Card:
    def __init__(self, c, seed):
        self.c = c
        g = c["g"]
        th = gx.load_rgb(g.get("thumb2") if c.get("alt") and g.get("thumb2") else g["thumb"])
        self.bg = gx.blur_bg(th, W, H, dark=0.5, scale=1.15)
        self.icon = gx.load_rgb(g["icon"], (512, 512))
        v = c["vis"]
        if v == "hero":
            self.kb = gx.KenBurns(th, VW, VH, (1.0, 1.55), seed=seed)
        elif v == "blur":
            self.kb = gx.KenBurns(th.filter(ImageFilter.GaussianBlur(22)), VW, VH, (1.0, 1.3), pan=(0, 0, 0, 0))
        elif v == "stat":
            self.ic = gx.framed(gx.cover(self.icon, 380, 380), 8, gx.WHITE, 40)
        elif v in ("duo", "duo3"):
            sz = 420 if v == "duo" else 290
            self.ics = [gx.framed(gx.cover(gx.load_rgb(x["icon"], (512, 512)), sz, sz), 8, gx.WHITE, 40)
                        for x in c["gs"]]
        elif v == "chart":
            gs = sorted(c["games"][:40], key=lambda x: -(x.get(c["metric"]) or 0))
            i = next((k for k, x in enumerate(gs) if x["id"] == g["id"]), 0)
            lo = max(0, min(i - 2, len(gs) - 5))
            self.rows = [(k + 1, x) for k, x in enumerate(gs[lo:lo + 5], start=lo)]
            self.rowics = {x["id"]: gx.cover(gx.load_rgb(x["icon"], (512, 512)), 110, 110) for _, x in self.rows}
            self.vmax = max((x.get(c["metric"]) or 1) for _, x in self.rows)
        self.mask = Image.new("L", (VW, VH), 0)
        ImageDraw.Draw(self.mask).rounded_rectangle((0, 0, VW - 1, VH - 1), 30, fill=255)
        self.acc = gx.accent(g["clean"])

    def frame(self, lt, dur, words, t_abs, loop_end=False):
        c = self.c
        u = lt / max(dur, 0.1)
        if loop_end:  # last card runs its motion backwards so the final frame matches frame 0
            u = 1 - u
        bw, bh = self.bg.size
        ox = int((bw - W) / 2 + math.sin(t_abs * 0.9) * (bw - W) / 2.2)
        oy = int((bh - H) / 2 + math.cos(t_abs * 0.7) * (bh - H) / 2.2)
        if loop_end:
            ox = int((bw - W) / 2 + math.sin(0) * (bw - W) / 2.2 * (1 - u) + math.sin(t_abs * 0.9) * (bw - W) / 2.2 * u)
            oy = int((bh - H) / 2 + (bh - H) / 2.2 * (1 - u) + math.cos(t_abs * 0.7) * (bh - H) / 2.2 * u)
        im = self.bg.crop((ox, oy, ox + W, oy + H))
        if dur > 3.0 and lt >= dur / 2 and not loop_end:  # second half: tinted background (visible beat)
            im = Image.blend(im, Image.new("RGB", im.size, self.acc), 0.35)
        d = ImageDraw.Draw(im)
        v = c["vis"]
        still = loop_end or getattr(self, "first", False)  # frame 0 and the loop end: no pop-in
        pop = 1.0 + 0.25 * max(0.0, 1 - lt / 0.25) if not still else 1.0
        # mid-card punch: a held zoom jump halfway through longer cards (a second "cut" per card)
        mid = dur > 3.0 and lt >= dur / 2 and not loop_end
        if mid:
            pop *= 1.35
        if v in ("hero", "blur"):
            view = self.kb.at(u, pop)
            d.rounded_rectangle((VX - 10, VY - 10, VX + VW + 10, VY + VH + 10), 40, fill=self.acc)
            im.paste(view, (VX, VY), self.mask)
            # light sweep across the picture every 1.3 s (keeps the eye moving)
            ph = (t_abs % 1.3) / 1.3
            sx = int(VX + ph * (VW - SWEEP.width))
            im.paste((255, 255, 255), (sx, VY, sx + SWEEP.width, VY + VH), SWEEP)
            if v == "blur":
                q = 1 + 0.08 * math.sin(t_abs * 8)
                gx.draw_text(d, (W // 2, VY + VH // 2), "?", gx.font(int(330 * q)), gx.WHITE, stroke=14, anchor="mm",
                             shadow=10)
            if c.get("reveal"):
                gx.draw_text(d, (VX + 30, VY + 20), "#1", gx.font(150), gx.YELLOW, stroke=10, shadow=8)
        elif v == "stat":
            s = 1 + 0.05 * math.sin(t_abs * 5)
            ic = self.ic.resize((int(self.ic.width * s * pop), int(self.ic.height * s * pop)))
            im.paste(ic, (W // 2 - ic.width // 2, VY - 20 + 200 - ic.height // 2), ic)
            cnt = ease(lt / 1.0) if not loop_end else 1.0
            val = (c.get("val") or 0) * cnt
            txt = (f"+{val:.0f}%" if c.get("pct") else ("+" if c.get("plus") else "-" if c.get("minus") else "")
                   + short_num(val)) if not c.get("pct") else f"+{val:.0f}%"
            gx.draw_text(d, (W // 2, VY + 470), txt, gx.font(150), gx.GREEN if not c.get("minus") else gx.RED,
                         stroke=10, anchor="mm", shadow=8)
            gx.draw_text(d, (W // 2, VY + 590), c.get("lab", ""), gx.font(50), gx.WHITE, stroke=5, anchor="mm")
            if c.get("live"):
                r = 16 + 6 * math.sin(t_abs * 7)
                d.ellipse((W // 2 - 260 - r, VY + 590 - r, W // 2 - 260 + r, VY + 590 + r), fill=gx.RED)
        elif v == "chart":
            for j, (rk, x) in enumerate(self.rows):
                y = VY - 30 + j * 130
                me = x["id"] == c["g"]["id"]
                a = ease((lt - j * 0.12) / 0.5) if not loop_end else 1.0
                bwid = int(560 * (x.get(c["metric"]) or 0) / self.vmax * a)
                d.rounded_rectangle((60, y, 1020, y + 116), 22, fill=(255, 221, 0) if me else (20, 22, 44))
                im.paste(self.rowics[x["id"]], (70, y + 3))
                col = gx.BLACK if me else gx.WHITE
                gx.draw_text(d, (200, y + 32), f"#{rk} {x['clean']}"[:24], gx.font(38), col, anchor="lm")
                d.rounded_rectangle((200, y + 66, 200 + max(8, bwid), y + 100), 12,
                                    fill=(230, 60, 60) if me else (70, 170, 255))
                gx.draw_text(d, (1000, y + 84), short_num(x.get(c["metric"])), gx.font(36), col, anchor="rm")
        elif v in ("duo", "duo3"):
            n = len(self.ics)
            for j, ic in enumerate(self.ics):
                cx = (W // (n + 1)) * (j + 1) if n == 3 else (300 if j == 0 else 780)
                bob = int(14 * math.sin(t_abs * 4 + j * 1.7))
                win = c.get("win") == j
                s = (1.08 if win else (0.9 if c.get("win") is not None else 1.0)) * pop
                icr = ic.resize((int(ic.width * s), int(ic.height * s)))
                y = VY + (170 if n == 2 else 230) + bob
                im.paste(icr, (cx - icr.width // 2, y - icr.height // 2), icr)
                nm = c["gs"][j]["clean"]
                gx.draw_text(d, (cx, y + icr.height // 2 + 45), nm, gx.fit_font(nm, 460 if n == 2 else 320, 44, 22),
                             gx.WHITE, stroke=5, anchor="mm")
                if c.get("vals"):
                    vv = c["vals"][j]
                    vt = f"{vv}%" if c.get("pct") else short_num(vv)
                    gx.draw_text(d, (cx, y + icr.height // 2 + 125), vt, gx.font(84),
                                 gx.GREEN if win else (220, 220, 220), stroke=7, anchor="mm")
                if n == 3:
                    gg = c["gs"][j]
                    gx.draw_text(d, (cx, y + icr.height // 2 + 120), "-" + short_num(-(gg.get("d_play") or 0)),
                                 gx.font(64), gx.RED, stroke=6, anchor="mm")
            if n == 2:
                gx.draw_text(d, (W // 2, VY + 170), "VS", gx.font(120), gx.YELLOW, stroke=10, anchor="mm", shadow=6)
        # headline (visible at frame 0)
        hs = 1.0 + 0.18 * max(0.0, 1 - lt / 0.2) if not still else 1.0
        head = c["head"]
        hs *= 1 + 0.06 * math.sin(t_abs * 9)
        hf = gx.fit_font(head, 980, int(124 * hs), 40)
        lines = gx.wrap(head, hf, 980)
        y0 = 330 - (len(lines) - 1) * 70
        for li, ln in enumerate(lines[:2]):
            gx.draw_text(d, (W // 2, y0 + li * 140), ln, hf, gx.YELLOW if li == len(lines[:2]) - 1 else gx.WHITE,
                         stroke=10, anchor="mm", shadow=8)
        if c.get("sub"):
            sf_ = gx.fit_font(c["sub"], 940, 56, 26)
            gx.draw_text(d, (W // 2, 500), c["sub"], sf_, gx.WHITE, stroke=5, anchor="mm")
        # captions: current 3-word group, current word in yellow
        if words:
            cur = 0
            for k, (w_, a_, b_) in enumerate(words):
                if t_abs >= a_:
                    cur = k
            g0 = cur - cur % 3
            grp = words[g0:g0 + 3]
            f = gx.font(82)
            txts = [w_[0].upper() for w_ in grp]
            full = " ".join(txts)
            if gx.text_size(full, f)[0] > 900:
                f = gx.fit_font(full, 900, 82, 40)
            x = W // 2 - gx.text_size(full, f)[0] // 2
            for k, tw in enumerate(txts):
                col = gx.YELLOW if g0 + k == cur else gx.WHITE
                d.text((x, CAP_Y), tw, font=f, fill=col, stroke_width=8, stroke_fill=gx.BLACK)
                x += gx.text_size(tw + " ", f)[0] + 6
        return im


def build(fmt_name, games, back, titles, rng, out_dir, name, day, voice="am_michael", workers=None):
    t0 = time.time()
    r = FORMATS[fmt_name](games, titles, rng, back)
    if not r:
        return None
    title, cards, desc, tags = r
    # at least ~32 s: add more facts about the main game before the loop card
    have = {c.get("head") for c in cards}
    for c in ([] if fmt_name == "guess" else extra_cards(cards[0]["g"], rng)):
        if sum(len(x["say"].split()) for x in cards) >= 92:
            break
        if c["head"] not in have and c["say"] not in {x["say"] for x in cards}:
            cards.insert(len(cards) - 1, c)
            have.add(c["head"])
    # keep it 30-45 s: ~2.8 spoken words per second -> drop middle cards above ~118 words
    while sum(len(c["say"].split()) for c in cards) > 118 and len(cards) > 5:
        cards.pop(-2)
    parts, t, words = [], 0.0, []
    for c in cards:
        a, ws = au.tts(c["say"], voice=voice, speed=1.12)
        c["start"] = t
        c["dur"] = len(a) / au.SR + 0.12
        parts.append((t, a))
        words += [(w, t + x0, t + x1) for (w, x0, x1) in ws]
        t += c["dur"]
    total = t + 0.15
    cards[-1]["dur"] += 0.15
    if total > 58:
        raise RuntimeError(f"short too long: {total:.1f}s")
    vbuf = np.zeros(int(total * au.SR) + au.SR, np.float32)
    for st, a in parts:
        au.place(vbuf, a, st)
    sbuf = np.zeros_like(vbuf)
    for c in cards[1:]:
        au.place(sbuf, au.whoosh(0.35, seed=int(c["start"] * 10)), max(0, c["start"] - 0.15), 0.7)
        if c.get("reveal"):
            au.place(sbuf, au.ding(), c["start"], 1.0)
    music = au.beat(total + 1, bpm=rng.choice([128, 136, 140]), seed=day.toordinal() + len(title))
    wav = os.path.join(out_dir, name + ".wav")
    au.mix_and_master(vbuf, music, sbuf, total, wav, music_gain=0.2)
    objs = [Card(c, seed=c["g"]["id"] % 997 + (1 if c.get("alt") else 0)) for c in cards]
    objs[0].first = True
    starts = [c["start"] for c in cards]

    def frame_fn(i):
        tt = i / FPS
        k = max(0, int(np.searchsorted(starts, tt, side="right")) - 1)
        c = cards[k]
        lt = tt - c["start"]
        loop_end = bool(c.get("loop"))
        im = objs[k].frame(lt, c["dur"], words, tt, loop_end)
        if k > 0 and lt < 0.07:  # flash cut
            im = Image.blend(im, Image.new("RGB", im.size, gx.WHITE), 0.5)
        return im

    mp4 = os.path.join(out_dir, name + ".mp4")
    rbx_video.render(frame_fn, int(total * FPS), W, H, FPS, wav, mp4, workers)
    os.remove(wav)
    print(f"short {fmt_name}: {total:.1f}s rendered in {time.time() - t0:.0f}s — {title}")
    return dict(file=name + ".mp4", kind="short", title=title,
                description=f"{desc}\n\nNew Roblox Top 10 every day — subscribe.\n\n{tx.DISCLAIMER}\n\n"
                            "#roblox #shorts #robloxgames #robloxnews",
                tags=["roblox", "roblox shorts", "roblox news", "roblox games"] + tags)

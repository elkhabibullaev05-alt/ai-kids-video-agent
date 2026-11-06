"""Titles, narration lines, on-screen 'why it's hot' lines and descriptions (varied, data-driven)."""
import re

from rbx_gfx import say_num, short_num

DISCLAIMER = ("Game names and images come from Roblox's public game pages and APIs and are shown for news "
              "commentary. This channel is independent and is not affiliated with or endorsed by Roblox Corporation.")


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


class Titles:
    def __init__(self, used):
        self.used = {norm(t if isinstance(t, str) else (t or {}).get("title", "")) for t in used or []}
        self.used_raw = " || ".join(sorted(self.used))

    def ok(self, t, limit=60):
        return t and len(t) <= limit and norm(t) not in self.used

    def take(self, t):
        self.used.add(norm(t))
        self.used_raw += " || " + norm(t)
        return t

    def pick(self, cands, rng, limit=60):
        c = [t for t in cands if self.ok(t, limit)]
        if not c:
            return None
        return self.take(rng.choice(c))

    def recent_mentions(self, name):
        return self.used_raw.count(norm(name))


def ago(days):
    if days is None:
        return ""
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    return f"{days} days ago"


def hot_facts(g):
    """[(spoken sentence, on-screen banner, priority)] for one game."""
    f = []
    n = g["clean"]
    if g.get("upd_days") is not None and g["upd_days"] <= 3:
        f.append((f"A fresh update dropped {ago(g['upd_days'])}, and players are flooding back.",
                  f"UPDATED {ago(g['upd_days']).upper()}", 9))
    if "top-trending" in (g.get("sorts") or []):
        f.append(("It is sitting on the Top Trending list right now.", "TOP TRENDING RIGHT NOW", 8))
    if "up-and-coming" in (g.get("sorts") or []):
        f.append(("It is on the Up and Coming list, so it is growing fast.", "UP-AND-COMING", 8))
    if g.get("d_play_pct") is not None and g["d_play_pct"] >= 12:
        f.append((f"Its player count jumped {g['d_play_pct']} percent since yesterday.",
                  f"+{g['d_play_pct']}% PLAYERS SINCE YESTERDAY", 10))
    if g.get("like") and g["like"] >= 88:
        f.append((f"With {g['like']} percent likes, players clearly love it.", f"{g['like']}% LIKE RATIO", 6))
    if g.get("year") and g["year"] <= 2018:
        f.append((f"It launched back in {g['year']}, and it still pulls huge crowds.", f"STILL HUGE SINCE {g['year']}", 5))
    if g.get("year") and g["year"] >= 2025:
        f.append((f"And it only came out in {g['year']}.", f"BRAND NEW IN {g['year']}", 7))
    if g.get("favoritedCount"):
        f.append((f"{say_num(g['favoritedCount'])} players have it in their favorites.",
                  f"{short_num(g['favoritedCount'])} FAVORITES", 4))
    if g.get("genre"):
        f.append((f"{g['genre']} fans keep this one packed all day.", f"TOP {g['genre'].upper()} PICK", 3))
    if g.get("upd_days") is not None and g["upd_days"] > 20:
        f.append((f"No update in {g['upd_days']} days, and it is still this big.", f"NO UPDATE IN {g['upd_days']} DAYS", 4))
    return f


def delta_lines(g):
    out = []
    pr = g.get("prev_rank")
    if pr:
        m = pr - g["rank"]
        if m > 0:
            out.append(f"It climbed {m} {'spot' if m == 1 else 'spots'} since yesterday.")
        elif m < 0:
            out.append(f"It slipped {-m} {'spot' if m == -1 else 'spots'} since yesterday.")
        else:
            out.append("It held the exact same spot as yesterday.")
    if g.get("d_visits"):
        out.append(f"It picked up {say_num(g['d_visits'])} visits in just one day.")
    return out


def entry_script(g, r, rng, mode):
    n = g["clean"]
    if r == 1:
        intro = rng.choice([f"And today's number one is {n}!", f"Number one. It's {n}!",
                            f"And the number one game right now is {n}!"])
    elif r == 3:
        intro = rng.choice([f"Top three time. Number three is {n}.", f"Into the top three: {n} at number three."])
    else:
        intro = rng.choice([f"Number {r}: {n}.", f"At number {r}, it's {n}.", f"Number {r} goes to {n}.",
                            f"Coming in at number {r}, {n}."])
    p, v = say_num(g.get("playing")), say_num(g.get("visits"))
    if mode == "gainers" and g.get("d_visits"):
        stats = rng.choice([f"It gained {say_num(g['d_visits'])} visits since yesterday, with {p} players online right now.",
                            f"{say_num(g['d_visits'])} new visits in one day, and {p} people playing at this moment."])
    else:
        stats = rng.choice([f"Right now, {p} players are in this game, with {v} visits all time.",
                            f"{p} people are playing it at this moment, and it has {v} total visits.",
                            f"It has {p} players online right now and {v} visits in total."])
    facts = sorted(hot_facts(g), key=lambda x: -(x[2] + rng.random() * 3))
    d = delta_lines(g)
    lines = [intro, stats]
    if d and mode != "gainers":
        lines.append(rng.choice(d))
    lines += [x[0] for x in facts[:3 if mode == "gainers" or not d else 2]]
    banner = facts[0][1] if facts else (g.get("genre") or "").upper()
    return " ".join(lines), banner


def hook_script(top, prev1_name, rng, mode):
    n1 = top[0]
    total = sum(g.get("playing") or 0 for g in top)
    if mode == "gainers":
        return rng.choice([
            f"These ten Roblox games gained more visits than any others since yesterday, and number one added "
            f"{say_num(n1.get('d_visits'))} in a single day. Can you guess it? Let's count them down.",
            f"Which Roblox games grew the most since yesterday? Number one picked up {say_num(n1.get('d_visits'))} "
            f"visits in one day. Here's the top ten."])
    if prev1_name and prev1_name != n1["clean"]:
        return (f"Yesterday's number one was {prev1_name}. Today, something changed. "
                f"Here are the ten most played Roblox games right now, with live player counts.")
    return rng.choice([
        f"Right now, {say_num(total)} people are playing just these ten Roblox games, and number one has "
        f"{say_num(n1.get('playing'))} by itself. Can you guess it before the end? Let's count down.",
        f"Bored of the Roblox home page? These are the ten games everyone is actually playing right now. "
        f"Number one has {say_num(n1.get('playing'))} players online. Let's go.",
        f"Ten games, {say_num(total)} players, live numbers. Stay to the end to see which game is number one "
        f"today. Let's count it down."])


def outro_script(top, rng):
    a, b = top[0]["clean"], top[1]["clean"]
    return rng.choice([
        f"That's today's top ten. {a} leads with {say_num(top[0].get('playing'))} players, ahead of {b}. "
        f"Which game should be number one tomorrow? Comment your pick, and subscribe for tomorrow's ranking.",
        f"So {a} takes the crown today. Can {b} catch it tomorrow? Tell me in the comments, and subscribe so "
        f"you see tomorrow's live top ten."])


def long_titles(top, mode, titles, rng):
    a, b = top[0]["clean"], top[1]["clean"]
    climbers = [g for g in top if g.get("prev_rank") and g["prev_rank"] - g["rank"] >= 2]
    c = []
    if mode == "gainers":
        c += ["Top 10 Roblox Games That Gained the Most Visits Today",
              f"{a} Gained {short_num(top[0].get('d_visits'))} Visits in 1 Day?! Top 10 Roblox Games",
              "The 10 Fastest Growing Roblox Games Right Now",
              f"Top 10 Roblox Games Growing Fastest Today ({a} #1?)"]
    else:
        c += [f"Top 10 Roblox Games Right Now ({a} Is #1?!)", f"{a} vs {b}: Top 10 Roblox Games Right Now",
              f"Is {a} Still #1? Top 10 Roblox Games Today", f"Top 10 Roblox Games Today: {a} Takes #1",
              f"NEW #1? Top 10 Roblox Games by Live Players", "Top 10 Most Played Roblox Games Right Now",
              f"Top 10 Roblox Games With the Most Players Today", f"The 10 Biggest Roblox Games Right Now ({a} #1)",
              f"{short_num(top[0].get('playing'))} Players?! Top 10 Roblox Games Right Now"]
        for g in climbers[:2]:
            c.append(f"{g['clean']} Jumped to #{g['rank']}! Top 10 Roblox Games Today")
    t = titles.pick(c, rng)
    k = 2
    while not t:
        t = titles.pick([f"Top 10 Roblox Games Right Now ({a}, {b}, {top[k]['clean']})",
                         f"Top 10 Roblox Games Today: #{k + 1} Is {top[k]['clean']}"], rng)
        k += 1
        if k > 9:
            t = titles.take(f"Top 10 Roblox Games Right Now #{rng.randint(100, 999)}")
    return t


def long_description(title, top, chapters, mode, day):
    lines = [f"{title}", "",
             ("The 10 Roblox games that gained the most visits since yesterday" if mode == "gainers" else
              "The 10 most played Roblox games right now, ranked by live player count") +
             f" (data pulled {day.strftime('%B %-d, %Y')}). New ranking every day.", ""]
    for r in range(10, 0, -1):
        g = top[r - 1]
        if mode == "gainers":
            lines.append(f"#{r} {g['clean']} — +{short_num(g.get('d_visits'))} visits in 24h, {short_num(g.get('playing'))} playing")
        else:
            lines.append(f"#{r} {g['clean']} — {short_num(g.get('playing'))} playing, {short_num(g.get('visits'))} visits")
    lines += ["", "Chapters:"] + chapters + ["",
              "Which game should be #1 tomorrow? Comment below and subscribe for tomorrow's Top 10.", "",
              "Data: public Roblox game pages (live players, visits, favorites, likes).", DISCLAIMER, "",
              "#roblox #robloxgames #top10 #robloxnews #gaming"]
    return "\n".join(lines)


TAGS = ["roblox", "roblox games", "top 10 roblox games", "best roblox games", "roblox news", "roblox top 10",
        "most played roblox games", "roblox games to play", "roblox 2026", "gaming"]

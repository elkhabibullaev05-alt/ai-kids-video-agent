"""Live Roblox game data from public web APIs (no login), daily snapshots, and day-over-day deltas.

Online sources (shapes checked 2026-11-06):
  explore  https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=<uuid>
           -> {"sorts": [{"sortId": "top-trending"|"up-and-coming"|"top-playing-now"|..., "contentType": "Games",
                          "games": [{"universeId", "rootPlaceId", "name", "playerCount", "totalUpVotes",
                                     "totalDownVotes", "isSponsored", "contentMaturity", "genreL1"}]}]}
  details  https://games.roblox.com/v1/games?universeIds=a,b,c   (<= 50 ids)
           -> {"data": [{"id", "rootPlaceId", "name", "creator": {"name", ...}, "playing", "visits",
                         "favoritedCount", "created", "updated", "genre_l1", "maxPlayers", "isContentRestricted"}]}
  votes    https://games.roblox.com/v1/games/votes?universeIds=...  -> {"data": [{"id", "upVotes", "downVotes"}]}
  icons    https://thumbnails.roblox.com/v1/games/icons?universeIds=...&size=512x512&format=Png
           -> {"data": [{"targetId", "state", "imageUrl"}]}
  thumbs   https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=...&size=768x432&format=Png
           -> {"data": [{"universeId", "thumbnails": [{"state", "imageUrl"}]}]}
  place->universe  https://apis.roblox.com/universes/v1/places/<placeId>/universe -> {"universeId"}
"""
import datetime as dt
import json
import os
import re
import time
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) RobloxTop10Daily/1.0", "Accept": "application/json"}

# Big games that must always be checked even when the explore API is down. Known universeIds first;
# the rest are placeIds resolved once via the place->universe API (cached in HOME/universe_cache.json).
FALLBACK_UNIVERSES = {
    "Brookhaven RP": 1686885941, "Blox Fruits": 994732206, "Adopt Me!": 383310974, "RIVALS": 6035872082,
    "Grow a Garden": 7436755782, "Steal a Brainrot": 7709344486, "99 Nights in the Forest": 7326934954,
}
FALLBACK_PLACES = {
    "Dead Rails": 116495829188952, "Murder Mystery 2": 142823291, "Tower of Hell": 1962086868,
    "DOORS": 6516141723, "Pet Simulator 99": 8737899170, "Arsenal": 286090429, "Jailbreak": 606849621,
    "Bee Swarm Simulator": 1537690962, "Royale High": 735030788, "Fisch": 16732694052,
    "Dress to Impress": 15101393044, "The Strongest Battlegrounds": 10449761463, "Blade Ball": 13772394625,
    "Natural Disaster Survival": 189707, "Da Hood": 2788229376, "BedWars": 6872265039,
    "Anime Defenders": 17017769292, "Forsaken": 18687417158, "Ink Game": 99567941238278,
    "Build A Boat For Treasure": 537413528, "Work at a Pizza Place": 192800, "Theme Park Tycoon 2": 69184822,
    "Evade": 9872472334, "Funky Friday": 6447798030, "Car Dealership Tycoon": 1554960397,
    "Dandy's World": 16116270224, "Anime Adventures": 8304191830, "Piggy": 4623386862,
    "Hide and Seek Extreme": 205224386, "Restaurant Tycoon 2": 3398014311, "MeepCity": 370731277,
    "Bloxburg": 185655149, "Flee the Facility": 893973440,
}


def get_json(url, tries=3, timeout=25):
    err = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # 429 / network: back off
            err = e
            time.sleep(2 + 4 * i)
    raise RuntimeError(f"GET failed {url[:90]}: {err}")


def download(url, path, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]}),
                                timeout=timeout) as r:
        data = r.read()
    if len(data) < 500:
        raise RuntimeError("image too small")
    with open(path, "wb") as f:
        f.write(data)
    return path


def clean_name(n):
    """'[🎃] Blox Fruits' -> 'Blox Fruits'; 'Brookhaven 🏡RP' -> 'Brookhaven RP'; '[UPD 21] X' -> 'X'."""
    n = re.sub(r"[\[\(\{][^\]\)\}]*[\]\)\}]", " ", n or "")
    n = "".join(ch if (ord(ch) < 0x2000 or ch in "’'") else " " for ch in n)
    n = re.sub(r"[|•~_*✨]+", " ", n)
    n = re.sub(r"\b(UPD(ATE)?|NEW|EVENT|FREE|SALE|BETA|ALPHA|RELEASE)\b!?", " ", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).strip(" -:!")
    if " - " in n:
        n = n.split(" - ")[0].strip()
    if len(n) > 30:
        n = n[:30].rsplit(" ", 1)[0]
    return n or "Mystery Game"


# ---------------------------------------------------------------- online

def _explore():
    """Games on the home page sorts -> {uid: {"sorts": set, "up", "down", "maturity"}}."""
    out = {}
    d = get_json(f"https://apis.roblox.com/explore-api/v1/get-sorts?sessionId={uuid.uuid4()}")
    for s in d.get("sorts", []):
        if s.get("contentType") != "Games":
            continue
        sid = s.get("sortId") or s.get("id") or "?"
        for g in s.get("games") or []:
            if g.get("isSponsored"):
                continue
            u = int(g["universeId"])
            e = out.setdefault(u, {"sorts": [], "up": g.get("totalUpVotes"), "down": g.get("totalDownVotes"),
                                   "maturity": g.get("contentMaturity")})
            if sid not in e["sorts"]:
                e["sorts"].append(sid)
    return out


def _resolve_places(home):
    cf = os.path.join(home, "universe_cache.json")
    try:
        cache = json.load(open(cf))
    except Exception:
        cache = {}
    ids = list(FALLBACK_UNIVERSES.values())
    for name, pid in FALLBACK_PLACES.items():
        k = str(pid)
        if k not in cache:
            try:
                cache[k] = int(get_json(f"https://apis.roblox.com/universes/v1/places/{pid}/universe")["universeId"])
                time.sleep(0.3)
            except Exception:
                continue
        ids.append(cache[k])
    json.dump(cache, open(cf, "w"))
    return ids


def _chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def fetch_online(home):
    try:
        ex = _explore()
    except Exception as e:
        print("explore failed:", e)
        ex = {}
    ids = list(dict.fromkeys(list(ex.keys()) + _resolve_places(home)))
    games = []
    for ch in _chunks(ids, 50):
        d = get_json("https://games.roblox.com/v1/games?universeIds=" + ",".join(map(str, ch)))
        games += d.get("data", [])
        time.sleep(0.4)
    votes = {}
    for ch in _chunks(ids, 50):
        try:
            d = get_json("https://games.roblox.com/v1/games/votes?universeIds=" + ",".join(map(str, ch)))
            for v in d.get("data", []):
                votes[int(v["id"])] = (v.get("upVotes"), v.get("downVotes"))
        except Exception:
            pass
    out = []
    for g in games:
        u = int(g["id"])
        e = ex.get(u, {})
        if g.get("isContentRestricted") or e.get("maturity") == "restricted":
            continue  # 17+ experiences are left out of the channel
        up, down = votes.get(u, (e.get("up"), e.get("down")))
        out.append(dict(g, totalUpVotes=up, totalDownVotes=down, sorts=e.get("sorts", [])))
    if len(out) < 12:
        raise RuntimeError(f"only {len(out)} games from the Roblox APIs")
    return out


def fetch_images(games, cache_dir):
    """Downloads icon (512) + wide thumbnail (768x432) for each game into cache_dir; sets g['icon'], g['thumb']."""
    os.makedirs(cache_dir, exist_ok=True)
    ids = [int(g["id"]) for g in games]
    icons, thumbs = {}, {}
    for ch in _chunks(ids, 30):
        q = ",".join(map(str, ch))
        try:
            for x in get_json(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={q}&size=512x512&format=Png"
                              "&isCircular=false").get("data", []):
                if x.get("state") == "Completed" and x.get("imageUrl"):
                    icons[int(x["targetId"])] = x["imageUrl"]
        except Exception as e:
            print("icons failed:", e)
        try:
            for x in get_json("https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds="
                              f"{q}&countPerUniverse=2&defaults=true&size=768x432&format=Png&isCircular=false"
                              ).get("data", []):
                ok = [t["imageUrl"] for t in x.get("thumbnails", []) if t.get("state") == "Completed" and t.get("imageUrl")]
                if ok:
                    thumbs[int(x["universeId"])] = ok
        except Exception as e:
            print("thumbs failed:", e)
    for g in games:
        u = int(g["id"])
        tl = thumbs.get(u) or []
        for key, url in (("icon", icons.get(u)), ("thumb", tl[0] if tl else None),
                         ("thumb2", tl[1] if len(tl) > 1 else None)):
            if not url:
                continue
            p = os.path.join(cache_dir, f"{u}_{key}.png")
            if not os.path.exists(p):
                try:
                    download(url, p)
                except Exception:
                    continue
            g[key] = p


# ---------------------------------------------------------------- offline fixture

def fetch_offline(today):
    fx = json.load(open(os.path.join(HERE, "fixture.json")))
    out = []
    for g in fx["today"]:
        g = dict(g)
        m = re.match(r"UPDATED-(\d+)", g.get("updated", ""))
        if m:
            g["updated"] = (dt.datetime.combine(today, dt.time(12)) - dt.timedelta(days=int(m.group(1)))).isoformat() + "Z"
        g["sorts"] = [s for s, ids in fx["sorts"].items() if g["id"] in ids]
        out.append(g)
    return out, fx["yesterday"]


# ---------------------------------------------------------------- snapshots

def snap_record(g):
    return {k: g.get(k) for k in ("name", "visits", "playing", "favoritedCount", "updated", "totalUpVotes",
                                   "totalDownVotes")}


def save_snapshot(home, day, games):
    d = os.path.join(home, "snapshots")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, day.isoformat() + ".json")
    old = {}
    if os.path.exists(p):  # several runs a day: keep the first visit counts of the day for the deltas
        try:
            old = json.load(open(p)).get("games", {})
        except Exception:
            old = {}
    gm = {str(g["id"]): snap_record(g) for g in games}
    for k, v in old.items():
        gm.setdefault(k, v)
    json.dump({"date": day.isoformat(), "saved": dt.datetime.now().isoformat(timespec="minutes"),
               "games": gm}, open(p, "w"))
    for f in sorted(os.listdir(d))[:-30]:  # keep a month
        try:
            os.remove(os.path.join(d, f))
        except OSError:
            pass


def load_previous(home, day):
    """Most recent snapshot from an earlier day (1-3 days back) -> (days_back, {uid: rec}) or (None, {})."""
    for back in (1, 2, 3):
        p = os.path.join(home, "snapshots", (day - dt.timedelta(days=back)).isoformat() + ".json")
        if os.path.exists(p):
            try:
                return back, {int(k): v for k, v in json.load(open(p))["games"].items()}
            except Exception:
                pass
    return None, {}


def enrich(games, prev, today):
    """Adds clean name, ranks, deltas and 'why it's hot' facts."""
    now = dt.datetime.combine(today, dt.time(12), tzinfo=dt.timezone.utc)
    for g in games:
        g["id"] = int(g["id"])
        g["clean"] = clean_name(g.get("name", ""))
        up, down = g.get("totalUpVotes") or 0, g.get("totalDownVotes") or 0
        g["like"] = round(100 * up / (up + down)) if up + down > 1000 else None
        try:
            g["upd_days"] = max(0, (now - dt.datetime.fromisoformat(g["updated"].replace("Z", "+00:00"))).days)
        except Exception:
            g["upd_days"] = None
        try:
            g["year"] = int(g["created"][:4])
        except Exception:
            g["year"] = None
        g["genre"] = g.get("genre_l1") or g.get("genre") or ""
        g["creator_name"] = (g.get("creator") or {}).get("name", "")
    games.sort(key=lambda g: -(g.get("playing") or 0))
    prev_rank = {}
    if prev:
        for i, (u, r) in enumerate(sorted(prev.items(), key=lambda kv: -(kv[1].get("playing") or 0))):
            prev_rank[u] = i + 1
    for i, g in enumerate(games):
        g["rank"] = i + 1
        p = prev.get(g["id"])
        if p:
            g["d_visits"] = (g.get("visits") or 0) - (p.get("visits") or 0)
            pp = p.get("playing") or 0
            g["d_play"] = (g.get("playing") or 0) - pp
            g["d_play_pct"] = round(100 * g["d_play"] / pp) if pp > 500 else None
            g["prev_rank"] = prev_rank.get(g["id"])
            if g["d_visits"] < 0:
                g["d_visits"] = None
        else:
            g.update(d_visits=None, d_play=None, d_play_pct=None, prev_rank=None)
    return games


def load(home, today, offline):
    """-> (games sorted by live players, days_back or None)."""
    cache = os.path.join(home, "cache", "img")
    if offline:
        games, yest = fetch_offline(today)
        prevf = os.path.join(home, "snapshots", (today - dt.timedelta(days=1)).isoformat() + ".json")
        if not os.path.exists(prevf):
            save_snapshot(home, today - dt.timedelta(days=1), yest)
    else:
        games = fetch_online(home)
    back, prev = load_previous(home, today)
    save_snapshot(home, today, games)
    games = enrich(games, prev, today)
    top = games[:40]
    if offline:
        import rbx_gfx
        rbx_gfx.placeholder_images(top, cache)
    else:
        fetch_images(top, cache)
        import rbx_gfx
        rbx_gfx.placeholder_images([g for g in top if not g.get("thumb") or not g.get("icon")], cache)
    return games, back

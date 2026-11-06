"""Lead photo of an English Wikipedia article, only when its Commons licence allows reuse. Cached in HOME/img_cache."""
import hashlib
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

UA = "WildSketchbookBot/1.0 (owner's channel tool; Wild Sketchbook YouTube channel; python-urllib)"
SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/"
COMMONS = "https://commons.wikimedia.org/w/api.php"
FREE = re.compile(r"^(cc0|cc[- ]by(-sa)?([- ][\d.]+)?|public domain|pd\b|pd-|no restrictions|attribution|gfdl|cc[- ]by-sa)", re.I)
NOT_FREE = re.compile(r"\b(nc|nd)\b|non[- ]?free|fair use|copyrighted|all rights", re.I)


def _get(url, binary=False, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json" if not binary else "*/*"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
            return data if binary else json.loads(data.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 503) and k < tries - 1:
                time.sleep(5 * (k + 1))
                continue
            raise
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2 * (k + 1))


def _file_from_url(u):
    """upload.wikimedia.org/wikipedia/commons/[thumb/]a/ab/Name.jpg[/320px-Name.jpg] -> ('commons', 'Name.jpg')."""
    p = urllib.parse.urlparse(u).path.split("/")
    try:
        i = p.index("wikipedia")
    except ValueError:
        return None, None
    proj = p[i + 1]
    rest = p[i + 2:]
    if rest and rest[0] == "thumb":
        rest = rest[1:]
    if len(rest) < 3:
        return proj, None
    return proj, urllib.parse.unquote(rest[2])


def _strip(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h or ""))).strip()


def license_ok(short):
    s = (short or "").strip()
    return bool(s) and not NOT_FREE.search(s) and bool(FREE.search(s))


def lead_image(title, cache_dir, log=print):
    """-> (path, meta) or (None, reason). meta: file, license, artist, page, needs_credit."""
    os.makedirs(cache_dir, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9_-]+", "_", title)[:80] + "_" + hashlib.md5(title.encode()).hexdigest()[:6]
    mj, mp = os.path.join(cache_dir, key + ".json"), os.path.join(cache_dir, key + ".jpg")
    if os.path.exists(mj):
        m = json.load(open(mj))
        if m.get("ok") and os.path.exists(mp):
            return mp, m
        if not m.get("ok") and time.time() - m.get("t", 0) < 14 * 86400:
            return None, m.get("reason", "cached miss")
    m = {"title": title, "t": time.time(), "ok": False}
    try:
        s = _get(SUMMARY + urllib.parse.quote(title.replace(" ", "_"), safe=""))
        src = ((s or {}).get("originalimage") or {}).get("source") or ((s or {}).get("thumbnail") or {}).get("source")
        if not src:
            m["reason"] = "no lead image"
        else:
            proj, fname = _file_from_url(src)
            if proj != "commons" or not fname:
                m["reason"] = f"image not on Commons ({proj}) — probably non-free"
            elif fname.lower().endswith((".svg", ".gif", ".webm", ".ogv", ".pdf")):
                m["reason"] = "lead image is a drawing/map/animation"
            else:
                q = _get(COMMONS + "?" + urllib.parse.urlencode({
                    "action": "query", "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "2000",
                    "titles": "File:" + fname, "format": "json", "formatversion": "2"}))
                pages = ((q or {}).get("query") or {}).get("pages") or []
                ii = (pages[0].get("imageinfo") or [None])[0] if pages else None
                if not ii:
                    m["reason"] = "no Commons imageinfo"
                else:
                    em = ii.get("extmetadata") or {}
                    lic = (em.get("LicenseShortName") or {}).get("value", "")
                    restr = (em.get("Restrictions") or {}).get("value", "")
                    m.update(file=fname, license=_strip(lic), artist=_strip((em.get("Artist") or {}).get("value", ""))[:120],
                             page=ii.get("descriptionurl") or ("https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(fname)),
                             license_url=(em.get("LicenseUrl") or {}).get("value", ""))
                    if not license_ok(m["license"]):
                        m["reason"] = f"licence not free: {m['license'] or '?'}"
                    elif "trademark" in restr.lower() or "personality" in restr.lower():
                        m["reason"] = f"restricted: {restr}"
                    elif min(ii.get("width", 0), ii.get("height", 0)) < 400:
                        m["reason"] = "image too small"
                    else:
                        data = _get(ii.get("thumburl") or ii["url"], binary=True)
                        if not data or len(data) < 5000:
                            m["reason"] = "download failed"
                        else:
                            open(mp, "wb").write(data)
                            lic_l = m["license"].lower()
                            m["needs_credit"] = not (lic_l.startswith("cc0") or "public domain" in lic_l or lic_l.startswith("pd"))
                            m["ok"] = True
        time.sleep(0.3)
    except Exception as e:  # network trouble: don't cache a long miss
        m["reason"] = f"error: {e}"[:200]
        m["t"] = time.time() - 14 * 86400 + 3600
    json.dump(m, open(mj, "w"), ensure_ascii=False, indent=1)
    if m["ok"]:
        return mp, m
    log(f"  img '{title}': {m['reason']}")
    return None, m["reason"]

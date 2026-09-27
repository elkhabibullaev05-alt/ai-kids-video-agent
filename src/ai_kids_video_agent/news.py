from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET


@dataclass
class NewsItem:
    title: str
    link: str
    source: str
    summary: str = ""
    published_at: str | None = None

    @property
    def identifier(self) -> str:
        return self.link


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _clean_markup(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", value))
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def _child_text(node: ET.Element, *names: str) -> str:
    for child in node:
        if _local_name(child.tag) in names:
            return "".join(child.itertext()).strip()
    return ""


def _item_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _feed_source(url: str) -> str:
    host = urllib.parse.urlparse(url).hostname or url
    lowered = host.lower()
    if lowered.endswith(("bbc.co.uk", "bbc.com", "bbci.co.uk")):
        return "BBC News"
    if lowered.endswith("theverge.com"):
        return "The Verge"
    if lowered.endswith("npr.org"):
        return "NPR"
    return host


def _fetch_xml(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-kids-video-agent/0.1 (+news-to-shorts workflow)"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()


def _parse_feed(xml_data: bytes, fallback_source: str) -> list[NewsItem]:
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as exc:
        raise ValueError(f"Feed is not valid XML: {exc}") from exc

    channel = next(
        (node for node in root.iter() if _local_name(node.tag) == "channel"),
        root,
    )
    items: list[NewsItem] = []
    for node in channel:
        if _local_name(node.tag) not in {"item", "entry"}:
            continue
        title = _clean_markup(_child_text(node, "title"))
        link = ""
        for child in node:
            if _local_name(child.tag) != "link":
                continue
            link = (child.attrib.get("href") or child.text or "").strip()
            if child.attrib.get("rel", "alternate") == "alternate":
                break
        if not title or not link:
            continue
        summary = _clean_markup(_child_text(node, "description", "summary", "content", "encoded"))
        source = _clean_markup(_child_text(node, "source")) or fallback_source
        published = _child_text(node, "pubdate", "published", "updated", "date") or None
        items.append(NewsItem(title, link, source, summary, published))
    return items


def fetch_headlines(
    rss_urls: list[str],
    progress: Callable[[str], None] | None = None,
    max_age_hours: int = 72,
) -> list[NewsItem]:
    report = progress or (lambda message: print(message, file=sys.stderr))
    collected: dict[str, NewsItem] = {}
    now = datetime.now(timezone.utc)

    for index, url in enumerate(rss_urls, start=1):
        report(f"[1/4] Fetching feed {index}/{len(rss_urls)}.")
        try:
            items = _parse_feed(_fetch_xml(url), _feed_source(url))
        except urllib.error.HTTPError as exc:
            report(f"      Warning: feed returned HTTP {exc.code}; skipping it.")
            continue
        except urllib.error.URLError as exc:
            report(f"      Warning: could not fetch this feed: {exc.reason}")
            continue
        except (TimeoutError, OSError, ValueError) as exc:
            report(f"      Warning: skipping this feed: {exc}")
            continue

        for item in items:
            published = _item_date(item.published_at)
            if published and published < now - timedelta(hours=max_age_hours):
                continue
            previous = collected.get(item.identifier)
            if previous is None or (not previous.summary and item.summary):
                collected[item.identifier] = item

    results = list(collected.values())
    results.sort(
        key=lambda item: _item_date(item.published_at)
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    if not results:
        raise ValueError(
            "No recent headlines were found. Check network access and RSS URLs, "
            "or set NEWS_RSS_URLS to valid feeds."
        )
    return results


def choose_story(items: list[NewsItem], limit: int = 1) -> list[NewsItem]:
    if limit < 1:
        raise ValueError("Story limit must be at least 1.")
    unique: list[NewsItem] = []
    seen: set[str] = set()
    for item in items:
        key = item.identifier.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    unique.sort(
        key=lambda item: _item_date(item.published_at)
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return unique[:limit]


def save_story_json(path: str | Path, story: NewsItem) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "title": story.title,
        "link": story.link,
        "source": story.source,
        "summary": story.summary,
        "published_at": story.published_at,
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


MIN_SCRIPT_WORDS = 65
MAX_SCRIPT_WORDS = 96


@dataclass
class ScriptSegment:
    scene: str
    narration: str
    visual: str


@dataclass
class StoryPlan:
    headline: str
    source_url: str
    source_name: str
    summary: str
    script: list[ScriptSegment] = field(default_factory=list)
    duration_seconds: int = 35


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b", text))


def fallback_summary(headline: str, source_summary: str = "") -> str:
    summary = re.sub(r"\s+", " ", source_summary).strip()
    if summary:
        return summary
    return (
        f"The headline reports: {headline.strip()}. The linked source has the full "
        "details; read it to understand the context."
    )


def _limited_words(value: str, limit: int) -> str:
    words = value.split()
    if len(words) <= limit:
        return value
    return " ".join(words[:limit]).rstrip(".,;:") + "…"


def _split_narration(narration: str, count: int = 3) -> list[str]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", narration.strip()) if part.strip()]
    if not sentences:
        return [narration.strip()] * count
    return [
        " ".join(sentences[(index * len(sentences)) // count : ((index + 1) * len(sentences)) // count])
        for index in range(count)
    ]


def _fallback_visuals(headline: str, summary: str) -> tuple[str, str, str]:
    subject = f"{headline} {summary}".lower()
    if any(word in subject for word in ("weather", "storm", "climate", "rain", "flood", "heat")):
        story_visual = "3D animated weather cloud"
    elif any(word in subject for word in ("market", "money", "price", "economy", "trade")):
        story_visual = "3D animated data chart"
    elif any(word in subject for word in ("science", "space", "research", "technology", "health")):
        story_visual = "3D science crystal with orbit"
    elif any(word in subject for word in ("government", "election", "city", "law", "president")):
        story_visual = "3D civic column and animated sphere"
    elif any(word in subject for word in ("football", "soccer", "sports", "match", "team", "race", "f1")):
        story_visual = "3D sports ball and stadium lights"
    else:
        story_visual = "3D animated story globe"
    return "3D rotating globe", story_visual, "3D source-card cube"


def youtube_metadata(headline: str, summary: str, source_name: str, source_url: str) -> dict:
    title = re.sub(r"\s+", " ", headline).strip()
    if len(title) > 70:
        title = title[:67].rsplit(" ", 1)[0].rstrip(".,:;!?") + "..."
    description = (
        f"{summary.strip()}\n\n"
        f"Source: {source_name} — {source_url}\n"
        "This Short summarizes the linked report. Check the source for context and updates."
    )
    return {
        "title": title,
        "description": description,
        "hashtags": ["#Shorts", "#News", "#WorldNews"],
        "source_url": source_url,
    }


def fallback_script(
    headline: str,
    source_name: str,
    source_summary: str = "",
) -> list[ScriptSegment]:
    clean_headline = _limited_words(re.sub(r"\s+", " ", headline).strip().rstrip(".!?"), 14)
    summary = _limited_words(
        fallback_summary(clean_headline, source_summary).rstrip(".!?"),
        22,
    )
    source = _limited_words(source_name, 5)
    sentences = [
        f"Here is the key detail: {clean_headline}.",
        f"According to {source}, {summary}.",
        f"This report comes from {source}.",
        "That is what the linked report confirms.",
        "Read the original story for context and exact details.",
        "The source may update this report as more information becomes available.",
        "We will keep confirmed facts separate from what is not yet known.",
        "Follow for more clear, source-linked news updates.",
    ]
    narration = " ".join(sentences[:6])
    for sentence in sentences[6:]:
        if word_count(narration) >= MIN_SCRIPT_WORDS:
            break
        narration += " " + sentence
    visuals = _fallback_visuals(clean_headline, source_summary)
    return [
        ScriptSegment(
            scene=caption,
            narration=segment,
            visual=visual,
        )
        for caption, segment, visual in zip(
            ("THE KEY DETAIL", "WHAT THE REPORT SAYS", "CHECK THE SOURCE"),
            _split_narration(narration),
            visuals,
        )
    ]


def build_story_plan(
    headline: str,
    source_url: str,
    source_name: str,
    summary: str | None = None,
    script: list[ScriptSegment] | None = None,
) -> StoryPlan:
    segments = script or fallback_script(headline, source_name, summary or "")
    narration = " ".join(segment.narration for segment in segments)
    words = word_count(narration)
    duration = round(words / 130 * 60)
    if not MIN_SCRIPT_WORDS <= words <= MAX_SCRIPT_WORDS:
        raise ValueError(
            f"Script must be {MIN_SCRIPT_WORDS}–{MAX_SCRIPT_WORDS} words "
            f"for a 30–45 second short; got {words}."
        )
    return StoryPlan(
        headline=headline,
        source_url=source_url,
        source_name=source_name,
        summary=summary or fallback_summary(headline),
        script=segments,
        duration_seconds=max(30, min(45, duration)),
    )


def save_story_plan(path: str | Path, plan: StoryPlan) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "headline": plan.headline,
        "source_url": plan.source_url,
        "source_name": plan.source_name,
        "summary": plan.summary,
        "duration_seconds": plan.duration_seconds,
        "word_count": word_count(" ".join(s.narration for s in plan.script)),
        "youtube_metadata": youtube_metadata(
            plan.headline,
            plan.summary,
            plan.source_name,
            plan.source_url,
        ),
        "script": [
            {"scene": s.scene, "narration": s.narration, "visual": s.visual} for s in plan.script
        ],
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def save_youtube_metadata(path: str | Path, plan: StoryPlan) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = youtube_metadata(plan.headline, plan.summary, plan.source_name, plan.source_url)
    payload["publishing_note"] = (
        "Shorts recommendations are personalized and depend on viewer response, retention, "
        "topic interest, and competition; metadata cannot guarantee reach."
    )
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

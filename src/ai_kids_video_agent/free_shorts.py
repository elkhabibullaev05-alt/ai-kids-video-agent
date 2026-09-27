from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import textwrap
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .aquarium import SLOTS
from .telegram_notify import send_telegram_notification
from .youtube import upload_scheduled_video, youtube_service


TIMEZONE = "America/New_York"
VIDEO_DURATION_SECONDS = 36
FPS = 30
SLOT_NAMES = tuple(slot for _, slot in SLOTS)


@dataclass(frozen=True)
class FactShort:
    title: str
    hook: str
    narration: tuple[str, ...]
    cards: tuple[str, ...]
    sources: tuple[str, ...]


FACT_SHORTS = (
    FactShort(
        "Venus Takes Longer to Spin Than to Orbit",
        "One planet takes longer to spin once than to go around the Sun.",
        (
            "Venus takes longer to spin once than to orbit the Sun.",
            "That is what happens on Venus, our neighboring planet.",
            "One full rotation takes about 243 Earth days.",
            "But one trip around the Sun takes about 225 Earth days.",
            "So its year ends before its long day is over.",
            "Space keeps finding ways to surprise us. Follow for another quick fact.",
        ),
        (
            "A day longer than a year?",
            "Meet Venus, Earth's neighbor",
            "One rotation: about 243 Earth days",
            "One orbit: about 225 Earth days",
            "Its year is shorter than its day",
            "Space is stranger than fiction",
        ),
        ("https://science.nasa.gov/venus/",),
    ),
    FactShort(
        "An Octopus Has Three Hearts",
        "An octopus has three hearts, and two of them pause while it swims.",
        (
            "An octopus has three hearts, not one.",
            "Two hearts send blood toward the gills to collect oxygen.",
            "The third heart sends oxygen-rich blood around the body.",
            "When an octopus swims, its main heart briefly slows down.",
            "That is one reason crawling can take less energy.",
            "The ocean is full of surprises. Follow for another quick fact.",
        ),
        (
            "Three hearts in one animal",
            "Two hearts send blood to the gills",
            "The third serves the body",
            "Swimming slows its main heart",
            "Crawling can save energy",
            "The ocean is full of surprises",
        ),
        ("https://ocean.si.edu/ocean-life/invertebrates/octopuses-and-squids",),
    ),
    FactShort(
        "Lightning Can Be Hotter Than the Sun's Surface",
        "A lightning bolt can briefly outheat the surface of the Sun.",
        (
            "A lightning channel can reach around 30,000 kelvin.",
            "The Sun's visible surface is about 5,500 kelvin.",
            "That means lightning can be several times hotter, for an instant.",
            "The extreme heat makes nearby air expand very quickly.",
            "That sudden expansion creates the sound we hear as thunder.",
            "A storm is powerful physics in the sky. Follow for more.",
        ),
        (
            "Lightning: a flash of extreme heat",
            "Up to about 30,000 kelvin",
            "The Sun's surface: about 5,500 kelvin",
            "Hot air expands very fast",
            "Rapid expansion makes thunder",
            "A storm is physics in action",
        ),
        ("https://www.weather.gov/safety/lightning-science",),
    ),
    FactShort(
        "Cleopatra Lived Closer to the Moon Landing",
        "Cleopatra lived closer in time to the Moon landing than to the pyramids.",
        (
            "The Great Pyramid was already ancient in Cleopatra's time.",
            "It was built around 2,500 years before Cleopatra ruled Egypt.",
            "Cleopatra lived about 2,000 years ago.",
            "The first Moon landing happened in 1969, less than 2,000 years later.",
            "So Cleopatra's era is closer to Apollo 11 than to the pyramid's construction.",
            "History is longer than it feels. Follow for another surprising fact.",
        ),
        (
            "Cleopatra and the Moon landing?",
            "The Great Pyramid was already ancient",
            "Built about 2,500 years before her",
            "Cleopatra lived about 2,000 years ago",
            "Apollo 11 landed in 1969",
            "Her era is closer to Apollo 11",
        ),
        (
            "https://whc.unesco.org/en/list/86/",
            "https://www.nasa.gov/history/apollo-11-mission-overview/",
        ),
    ),
    FactShort(
        "The Moon Is Slowly Moving Away",
        "Earth's Moon drifts away from us by about four centimeters each year.",
        (
            "The Moon is slowly moving farther from Earth.",
            "Laser measurements show a drift of about 3.8 centimeters each year.",
            "That is roughly the speed your fingernails grow.",
            "The change is tiny from year to year, but measurable.",
            "The Moon's gravity also helps shape ocean tides.",
            "Even the night sky is changing. Follow for another quick fact.",
        ),
        (
            "The Moon is drifting away",
            "About 3.8 centimeters each year",
            "Roughly fingernail-growth speed",
            "Tiny each year, measurable over time",
            "The Moon also shapes ocean tides",
            "Even the sky is changing",
        ),
        ("https://science.nasa.gov/moon/",),
    ),
    FactShort(
        "Why Astronauts Float in Orbit",
        "Astronauts float because they are falling around Earth together.",
        (
            "Astronauts in orbit are still pulled by Earth's gravity.",
            "Their spacecraft is moving sideways so quickly that it keeps missing the ground.",
            "The station and crew fall around Earth together.",
            "Because everything inside is falling at nearly the same rate, it feels weightless.",
            "That is why floating is not the same as having no gravity.",
            "Orbit is a continuous fall. Follow for another quick fact.",
        ),
        (
            "Why do astronauts float?",
            "Earth's gravity still reaches them",
            "The spacecraft moves sideways very fast",
            "It keeps falling around Earth",
            "Crew and station fall together",
            "Orbit is a continuous fall",
        ),
        ("https://www.nasa.gov/learning-resources/for-kids-and-students/what-is-microgravity-grades-5-8/",),
    ),
)


def choose_fact(day: date, slot: str) -> FactShort:
    slot_index = SLOT_NAMES.index(slot) if slot in SLOT_NAMES else -1
    if slot_index < 0:
        raise ValueError(f"Unknown daily slot: {slot}")
    index = (day.toordinal() * 5 + slot_index) % len(FACT_SHORTS)
    return FACT_SHORTS[index]


def _find_font(bold: bool) -> str | None:
    candidates = (
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        )
        if bold
        else (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        )
    )
    return next((candidate for candidate in candidates if Path(candidate).is_file()), None)


def _wrap_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def render_fact_cards(fact: FactShort, output_dir: Path, day: date, slot: str) -> Path:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "Image rendering needs Pillow. Install this project's automation extra."
        ) from exc

    cards_dir = output_dir / "cards" / f"{day.isoformat()}_{slot}"
    cards_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(fact.title.encode("utf-8")).digest()
    base = (12 + digest[0] % 20, 18 + digest[1] % 24, 42 + digest[2] % 32)
    accent = (45 + digest[3] % 80, 155 + digest[4] % 75, 205 + digest[5] % 50)
    highlight = tuple(min(255, int(channel * 1.7 + 24)) for channel in accent)
    headline_font = ImageFont.truetype(_find_font(True), 76) if _find_font(True) else ImageFont.load_default()
    card_font = ImageFont.truetype(_find_font(True), 67) if _find_font(True) else ImageFont.load_default()
    label_font = ImageFont.truetype(_find_font(False), 30) if _find_font(False) else ImageFont.load_default()
    card_texts = (fact.hook, *fact.cards[1:])

    for index, text in enumerate(card_texts):
        gradient = Image.linear_gradient("L").resize((1080, 1920))
        image = ImageOps.colorize(gradient, black=base, white=highlight)
        draw = ImageDraw.Draw(image, "RGBA")
        draw.ellipse((715, 210, 1115, 610), outline=(*accent, 120), width=7)
        draw.ellipse((-150, 1320, 310, 1790), outline=(145, 222, 255, 65), width=5)
        draw.rounded_rectangle((76, 124, 1004, 1796), radius=52, fill=(6, 12, 32, 155), outline=(*accent, 145), width=3)
        draw.text((132, 196), "OCEAN GLOW  /  QUICK FACT", font=label_font, fill=(186, 225, 255, 255))
        font = headline_font if index == 0 else card_font
        lines = _wrap_text(text, 21 if index == 0 else 24)
        line_height = 104 if index == 0 else 92
        total_height = len(lines) * line_height
        y_start = (1920 - total_height) // 2 - 30
        for line in lines:
            box = draw.textbbox((0, 0), line, font=font)
            draw.text(((1080 - (box[2] - box[0])) // 2, y_start), line, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 10, 30, 210))
            y_start += line_height
        draw.text((132, 1675), f"{index + 1:02d}  /  {len(card_texts):02d}", font=label_font, fill=(186, 225, 255, 255))
        image.save(cards_dir / f"card_{index + 1:02d}.png", optimize=True)
    return cards_dir


def assemble_fact_video(
    image_paths: list[Path],
    audio_path: Path,
    video_path: Path,
    output_dir: Path,
    ffmpeg_executable: str,
) -> Path:
    if not image_paths:
        raise ValueError("At least one story card image is required.")
    if not audio_path.is_file() or audio_path.stat().st_size == 0:
        raise FileNotFoundError(f"Narration audio is missing or empty: {audio_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    seconds_per_card = VIDEO_DURATION_SECONDS // len(image_paths)
    command = [ffmpeg_executable, "-hide_banner", "-loglevel", "warning", "-y"]
    for image_path in image_paths:
        command.extend(
            [
                "-loop",
                "1",
                "-framerate",
                str(FPS),
                "-t",
                str(seconds_per_card),
                "-i",
                str(image_path),
            ]
        )
    command.extend(["-i", str(audio_path)])

    filters = []
    for index in range(len(image_paths)):
        filters.append(
            f"[{index}:v]zoompan="
            "z='min(zoom+0.00025,1.06)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s=1080x1920:fps={FPS},"
            f"trim=duration={seconds_per_card},settb=expr=1/{FPS},setpts=N[v{index}]"
        )
    video_inputs = "".join(f"[v{index}]" for index in range(len(image_paths)))
    audio_index = len(image_paths)
    filters.append(
        f"{video_inputs}concat=n={len(image_paths)}:v=1:a=0[outv]"
    )
    filters.append(
        f"[{audio_index}:a]apad=pad_dur={VIDEO_DURATION_SECONDS},"
        f"atrim=duration={VIDEO_DURATION_SECONDS}[outa]"
    )
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            "-t",
            str(VIDEO_DURATION_SECONDS),
            "-fps_mode",
            "cfr",
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-profile:v",
            "high",
            "-level:v",
            "4.1",
            "-preset",
            "medium",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-ar",
            "44100",
            "-movflags",
            "+faststart",
            str(video_path),
        ]
    )
    command_record = output_dir / f"{video_path.stem}_ffmpeg_command.txt"
    command_record.write_text("\n".join(command) + "\n", encoding="utf-8")
    print("[2/4] Adding gentle motion to story cards and assembling narration...", flush=True)
    subprocess.run(command, check=True)
    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg completed without creating a video file.")
    return video_path


def create_fact_video(
    fact: FactShort,
    output_dir: Path,
    day: date,
    slot: str,
    espeak_executable: str = "espeak-ng",
    ffmpeg_executable: str = "ffmpeg",
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    cards_dir = render_fact_cards(fact, output_dir, day, slot)
    video_path = output_dir / f"fact_{day.isoformat()}_{slot}.mp4"
    audio_path = output_dir / f"fact_{day.isoformat()}_{slot}.wav"
    voice_text = " ".join(fact.narration)
    print("[1/4] Creating a simple free US-English system voice with espeak-ng...", flush=True)
    subprocess.run(
        [espeak_executable, "-v", "en-us", "-s", "158", "-w", str(audio_path), voice_text],
        check=True,
    )
    image_paths = [cards_dir / f"card_{index + 1:02d}.png" for index in range(len(fact.cards))]
    return assemble_fact_video(image_paths, audio_path, video_path, output_dir, ffmpeg_executable)


def publish_one(day: date, slot: str, output_dir: Path) -> str:
    fact = choose_fact(day, slot)
    zone = ZoneInfo(TIMEZONE)
    publish_at = datetime.combine(day, datetime.min.time(), zone).replace(
        hour=dict((name, hour) for hour, name in SLOTS)[slot]
    )
    if publish_at <= datetime.now(zone) + timedelta(minutes=15):
        publish_at += timedelta(days=1)
    print(f"[3/4] Rendering: {fact.title}", flush=True)
    video_path = create_fact_video(fact, output_dir, day, slot)
    metadata = {
        "title": f"{fact.title} #Shorts",
        "description": (
            f"{fact.hook}\n\n"
            "A quick, original educational Short narrated in English. "
            "Visuals and voice are generated locally for this channel.\n\n"
            "Sources:\n"
            + "\n".join(fact.sources)
            + "\n\n"
            "#Shorts #Facts #Science #LearnOnYouTube"
        ),
        "tags": ["shorts", "facts", "science", "education", "quick facts"],
        "category_id": "27",
        "language": "en",
    }
    print(f"[4/4] Uploading and scheduling for {publish_at.isoformat()}...", flush=True)
    video_id = upload_scheduled_video(
        video_path,
        metadata,
        publish_at,
        service=youtube_service(),
    )
    return video_id


def scheduled_slot_from_cron(
    cron_expression: str,
    now: datetime,
) -> str | None:
    fields = cron_expression.split()
    if len(fields) != 5 or fields[0] != "0" or not fields[2:] == ["*", "*", "*"]:
        raise ValueError(f"Unsupported daily workflow schedule: {cron_expression}")
    try:
        utc_hour = int(fields[1])
    except ValueError as exc:
        raise ValueError(f"Unsupported workflow schedule hour: {fields[1]}") from exc
    if not 0 <= utc_hour <= 23:
        raise ValueError(f"Invalid workflow UTC hour: {utc_hour}")
    now_utc = now.astimezone(timezone.utc)
    scheduled_utc = datetime.combine(now_utc.date(), time(utc_hour), timezone.utc)
    if scheduled_utc > now_utc:
        scheduled_utc -= timedelta(days=1)
    if now_utc - scheduled_utc > timedelta(minutes=90):
        return None
    scheduled_local = scheduled_utc.astimezone(ZoneInfo(TIMEZONE))
    return next(
        (slot for hour, slot in SLOTS if scheduled_local.hour == hour - 1),
        None,
    )


def run_automation(slot: str, output_dir: Path, preview_only: bool = False) -> int:
    now = datetime.now(ZoneInfo(TIMEZONE))
    if slot == "auto":
        cron_expression = os.environ.get("GITHUB_EVENT_SCHEDULE")
        chosen_slot = scheduled_slot_from_cron(cron_expression, now) if cron_expression else None
    else:
        chosen_slot = slot
    if chosen_slot is None:
        print(f"No publishing preparation is scheduled for {now.strftime('%H:%M ET')}; exiting.")
        return 0
    if chosen_slot not in SLOT_NAMES:
        raise ValueError(f"Slot must be one of {', '.join(SLOT_NAMES)}, or auto.")
    video_day = now.date()
    publish_hour = dict((name, hour) for hour, name in SLOTS)[chosen_slot]
    if slot != "auto" and now.hour >= publish_hour:
        video_day += timedelta(days=1)
    if preview_only:
        fact = choose_fact(video_day, chosen_slot)
        video_path = create_fact_video(fact, output_dir, video_day, chosen_slot)
        print(f"Preview ready (not uploaded): {video_path}", flush=True)
        return 0
    video_id = publish_one(video_day, chosen_slot, output_dir)
    video_url = f"https://youtu.be/{video_id}"
    print(f"Scheduled {video_url}", flush=True)
    try:
        send_telegram_notification(
            f"✅ Ocean Glow: {choose_fact(video_day, chosen_slot).title} YouTube’da rejalashtirildi.\n"
            f"Chiqish vaqti (New York): {video_day.isoformat()} {publish_hour:02d}:00 ET\n"
            f"{video_url}"
        )
    except RuntimeError as exc:
        print(f"Telegram notification failed: {exc}", flush=True)
    return 0


def notify_failure(error: Exception) -> None:
    try:
        send_telegram_notification(f"❌ Ocean Glow agent xatosi: {error}")
    except RuntimeError as exc:
        print(f"Telegram failure notification failed: {exc}", flush=True)


def main() -> int:
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Create and schedule free English fact Shorts.")
    parser.add_argument("--slot", choices=("auto", *SLOT_NAMES), default="auto")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="Render a video locally without connecting to YouTube or uploading it.",
    )
    args = parser.parse_args()
    try:
        ffmpeg = shutil.which("ffmpeg")
        espeak = shutil.which("espeak-ng")
        if not ffmpeg or not espeak:
            raise RuntimeError("Install ffmpeg and espeak-ng before running the video workflow.")
        if not args.preview_only and not os.environ.get("YOUTUBE_TOKEN_FILE"):
            raise RuntimeError("Set YOUTUBE_TOKEN_FILE to the authorized OAuth token JSON file.")
        return run_automation(args.slot, args.output_dir, preview_only=args.preview_only)
    except Exception as exc:
        print(f"Agent failed: {exc}", flush=True)
        notify_failure(exc)
        return 1

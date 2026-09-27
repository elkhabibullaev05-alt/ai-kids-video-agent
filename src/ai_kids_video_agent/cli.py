from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from .agent import create_story_from_headline, get_recent_stories
from .config import get_output_dir, get_rss_urls
from .news import save_story_json
from .speech import DEFAULT_VOICE, synthesize_speech
from .story import save_story_plan, save_youtube_metadata, word_count as count_words


def _log(stage: str, message: str) -> None:
    print(f"[{stage}] {message}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a news-based YouTube Shorts workflow")
    parser.add_argument("--rss", action="append", default=[], help="RSS/Atom feed URL (can be repeated)")
    parser.add_argument("--output-dir", default=get_output_dir(), help="Directory to write generated outputs")
    parser.add_argument("--limit", type=int, default=10, help="How many recent headlines to show (default: 10)")
    parser.add_argument("--story-index", type=int, default=1, help="1-based headline number to use (default: 1)")
    parser.add_argument("--skip-render", action="store_true", help="Generate the script without audio/video rendering")
    parser.add_argument("--fps", type=int, default=24, help="Rendered video frame rate (default: 24)")
    parser.add_argument(
        "--voice",
        default=os.environ.get("NEWS_SHORTS_VOICE", DEFAULT_VOICE),
        help=f"Installed Windows speech voice (default: {DEFAULT_VOICE})",
    )
    args = parser.parse_args(argv)

    if args.limit < 1:
        _log("error", "--limit must be at least 1.")
        return 1
    if args.fps < 1:
        _log("error", "--fps must be at least 1.")
        return 1

    rss_urls = args.rss or get_rss_urls()
    out_dir = Path(args.output_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        _log("1/5 news", f"Collecting recent headlines from {len(rss_urls)} feed(s)...")
        stories = get_recent_stories(rss_urls, limit=args.limit)
        for index, item in enumerate(stories, start=1):
            published = item.published_at or "date not provided"
            _log("news", f"{index}. {item.title} — {item.source} ({published})")
        if args.story_index < 1 or args.story_index > len(stories):
            raise ValueError(f"--story-index must be between 1 and {len(stories)}.")
        story = stories[args.story_index - 1]
        save_story_json(out_dir / "story.json", story)
        _log("news", f"Selected: {story.title}\nSource: {story.link}")

        if os.environ.get("OPENAI_API_KEY"):
            _log("2/5 script", "Writing a simple-English, retention-focused 30–45 second script...")
        else:
            _log(
                "2/5 script",
                "OPENAI_API_KEY is unset; using the source-limited local script template.",
            )
        plan = create_story_from_headline(story.title, story.link, story.source, story.summary)
        plan_file = out_dir / "story_plan.json"
        save_story_plan(plan_file, plan)
        narration = " ".join(segment.narration for segment in plan.script)
        _log("script", f"Summary and {count_words(narration)}-word script saved to {plan_file}")
        for segment in plan.script:
            _log("voiceover", segment.narration)
        metadata_path = out_dir / "youtube_metadata.json"
        save_youtube_metadata(metadata_path, plan)
        _log("YouTube", f"Suggested title, source-linked description, and hashtags: {metadata_path}")

        if args.skip_render:
            _log("done", "Headline, summary, and voiceover script are ready; video rendering was skipped.")
            return 0

        _log("3/5 speech", f"Creating English voice narration with {args.voice}...")
        audio_path = out_dir / "narration.wav"
        audio_duration = synthesize_speech(plan, audio_path, voice=args.voice)
        _log("speech", f"Narration saved ({audio_duration:.1f} seconds): {audio_path}")

        _log("4/5 Blender", "Building an animated 3D news presenter with speech-synchronized mouth movement...")
        from .render import ensure_executable, render_blender_scene, stitch_vertical_video

        ensure_executable("blender")
        ensure_executable("ffmpeg")
        frames_dir = out_dir / "frames" / uuid.uuid4().hex[:10]
        render_fps = min(args.fps, 3)
        _log("render", f"Rendering at {render_fps} FPS; FFmpeg will interpolate to {args.fps} FPS.")
        render_blender_scene(
            plan_file,
            frames_dir,
            fps=render_fps,
            duration_seconds=audio_duration,
        )

        _log("5/5 FFmpeg", "Combining the animated host with its spoken narration...")
        montage = out_dir / "final_short.mp4"
        stitch_vertical_video(
            [str(frames_dir)],
            montage,
            fps=args.fps,
            input_fps=render_fps,
            audio_path=audio_path,
        )
        root_copy = Path.cwd() / "final_short.mp4"
        if root_copy.resolve() != montage.resolve():
            shutil.copy2(montage, root_copy)
        _log("done", f"Spoken vertical Short created at {montage} and copied to {root_copy}")
        return 0
    except subprocess.CalledProcessError as exc:
        _log("error", f"Rendering command failed with exit code {exc.returncode}.")
        return 1
    except (ValueError, OSError, RuntimeError) as exc:
        _log("error", str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())

import json
import struct
import wave
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ai_kids_video_agent.agent import create_story_from_headline
from ai_kids_video_agent.aquarium import (
    CHANNEL_BRAND,
    OCEAN_ANIMALS,
    SLOTS,
    animal_for_slot,
    make_video_plan,
    synthesize_ambient_music,
)
from ai_kids_video_agent.free_shorts import (
    FACT_SHORTS,
    choose_fact,
    create_fact_video,
    run_automation,
    scheduled_slot_from_cron,
)
from ai_kids_video_agent.cli import main
from ai_kids_video_agent.news import NewsItem, _parse_feed, choose_story
from ai_kids_video_agent.render import ensure_executable
from ai_kids_video_agent.series import (
    CHARACTERS,
    PILOT_DIALOGUE,
    SERIES_TITLE,
    _compose_captions,
    _join_audio,
    series_bible,
)
from ai_kids_video_agent.speech import DEFAULT_VOICE, synthesize_speech
from ai_kids_video_agent.story import (
    MAX_SCRIPT_WORDS,
    MIN_SCRIPT_WORDS,
    StoryPlan,
    build_story_plan,
    fallback_summary,
    save_youtube_metadata,
    word_count,
)
from ai_kids_video_agent.youtube import (
    install_daily_task,
    publish_time,
    upload_scheduled_video,
    youtube_service,
)


def test_choose_story_deduplicates():
    items = [
        NewsItem(title="A", link="https://example.com/1", source="news"),
        NewsItem(title="A", link="https://example.com/1", source="news"),
        NewsItem(title="B", link="https://example.com/2", source="feed"),
    ]
    chosen = choose_story(items, limit=2)
    assert len(chosen) == 2
    assert chosen[0].title == "A"


def test_fallback_summary_is_not_empty():
    summary = fallback_summary("AI launches new model")
    assert "AI launches new model" in summary
    assert len(summary) > 20


def test_borough_file_pilot_is_an_open_ended_two_voice_serial():
    bible = series_bible()
    assert bible["title"] == SERIES_TITLE
    assert "open-ended" in bible["format"].lower()
    assert [character.name for character in CHARACTERS] == ["Maya", "Noah"]
    assert [character.age for character in CHARACTERS] == [17, 16]
    assert {beat.speaker for beat in PILOT_DIALOGUE} == {"Maya", "Noah"}
    assert bible["episode_one"]["ending"] == "Cliffhanger; the story is not resolved."
    assert "platform" in PILOT_DIALOGUE[-2].line
    assert "coat" in PILOT_DIALOGUE[-1].line


def test_borough_file_upscales_and_subtitles_rendered_frames(tmp_path):
    from PIL import Image

    raw_frames = tmp_path / "raw"
    raw_frames.mkdir()
    Image.new("RGB", (540, 960), (30, 40, 60)).save(raw_frames / "frame_00000.png")
    output = tmp_path / "captioned"
    output.mkdir()
    Image.new("RGB", (720, 1280), (255, 0, 0)).save(output / "frame_00142.png")
    _compose_captions(raw_frames, output, [0])
    assert not (output / "frame_00142.png").exists()
    with Image.open(output / "frame_00000.png") as image:
        assert image.size == (720, 1280)


def test_borough_file_audio_pauses_match_animation_timing(tmp_path):
    clips = []
    for index in range(2):
        path = tmp_path / f"line_{index}.wav"
        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(24000)
            audio.writeframes(b"\0\0" * 12000)
        clips.append(path)

    joined = tmp_path / "joined.wav"
    _join_audio(clips, joined, [0.5, 0.5], [4, 4])
    with wave.open(str(joined), "rb") as audio:
        assert audio.getnframes() / audio.getframerate() == 2


def test_build_story_plan_sets_defaults():
    plan = build_story_plan("Solar breakthrough", "https://example.com/story", "Example News")
    assert isinstance(plan, StoryPlan)
    assert 30 <= plan.duration_seconds <= 45
    assert len(plan.script) == 3
    narration = " ".join(segment.narration for segment in plan.script)
    assert MIN_SCRIPT_WORDS <= word_count(narration) <= MAX_SCRIPT_WORDS


def test_fallback_visuals_match_story_topic():
    plan = build_story_plan(
        "Football teams prepare for a major match",
        "https://example.com/story",
        "Example News",
        "The teams are preparing for the game.",
    )
    assert plan.script[0].visual == "3D rotating globe"
    assert "sports ball" in plan.script[1].visual
    assert plan.script[2].visual == "3D source-card cube"


def test_parse_namespaced_atom_feed_and_html_summary():
    feed = b"""<?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <title>Example</title>
      <entry>
        <title>New science update</title>
        <link href="https://example.com/story"/>
        <summary>Researchers shared &lt;b&gt;new details&lt;/b&gt;.</summary>
        <updated>2026-09-26T09:00:00Z</updated>
      </entry>
    </feed>"""
    stories = _parse_feed(feed, "example.com")
    assert stories[0].title == "New science update"
    assert stories[0].summary == "Researchers shared new details."
    assert stories[0].published_at == "2026-09-26T09:00:00Z"


def test_default_feed_source_uses_publisher_name():
    from ai_kids_video_agent.news import _feed_source

    assert _feed_source("https://feeds.bbci.co.uk/news/rss.xml") == "BBC News"


def test_ffmpeg_resolver_uses_configured_executable(tmp_path, monkeypatch):
    executable = tmp_path / "ffmpeg.exe"
    executable.write_bytes(b"test binary")
    monkeypatch.setenv("FFMPEG_PATH", str(executable))
    monkeypatch.setattr("shutil.which", lambda _name: None)
    assert ensure_executable("ffmpeg") == str(executable)


def test_ffmpeg_interpolates_low_fps_frames(monkeypatch, tmp_path):
    from ai_kids_video_agent.render import _encode_frames

    command = {}

    def fake_run(args, check):
        command["args"] = args
        command["check"] = check

    monkeypatch.setattr("ai_kids_video_agent.render.subprocess.run", fake_run)
    _encode_frames("ffmpeg.exe", tmp_path, tmp_path / "short.mp4", 24, 2)
    assert command["check"] is True
    assert command["args"][command["args"].index("-framerate") + 1] == "2"
    assert "minterpolate=fps=24" in command["args"][command["args"].index("-vf") + 1]


def test_ffmpeg_muxes_voice_track(monkeypatch, tmp_path):
    from ai_kids_video_agent.render import _encode_frames

    audio = tmp_path / "voice.wav"
    audio.write_bytes(b"wav")
    command = {}

    def fake_run(args, check):
        command["args"] = args
        command["check"] = check

    monkeypatch.setattr("ai_kids_video_agent.render.subprocess.run", fake_run)
    _encode_frames("ffmpeg.exe", tmp_path, tmp_path / "short.mp4", 24, 3, audio)
    args = command["args"]
    assert args.count("-map") == 2
    assert args[args.index("-map") + 1] == "0:v:0"
    assert args[args.index("-map", args.index("-map") + 1) + 1] == "1:a:0"
    assert args[args.index("-c:a") + 1] == "aac"


def test_three_daily_ocean_slots_choose_distinct_species_and_english_metadata():
    today = date(2026, 9, 26)
    assert SLOTS == ((9, "morning"), (14, "afternoon"), (18, "evening"))
    morning = animal_for_slot(today, "morning")
    afternoon = animal_for_slot(today, "afternoon")
    evening = animal_for_slot(today, "evening")
    assert len({morning, afternoon, evening}) == 3
    plan = make_video_plan(morning)
    assert plan["channel_brand"] == CHANNEL_BRAND == "OCEAN GLOW"
    assert plan["duration_seconds"] <= 60
    assert plan["script"][0]["narration"] == ""
    assert "ambient synth music" in plan["youtube_metadata"]["description"]
    assert plan["youtube_metadata"]["language"] == "en"
    assert len(OCEAN_ANIMALS) >= 10


def test_free_fact_shorts_are_distinct_and_have_english_narration():
    today = date(2026, 9, 26)
    morning = choose_fact(today, "morning")
    afternoon = choose_fact(today, "afternoon")
    evening = choose_fact(today, "evening")
    assert len({morning.title, afternoon.title, evening.title}) == 3
    assert choose_fact(today + timedelta(days=1), "morning").title != morning.title
    assert all(len(fact.narration) == len(fact.cards) == 6 for fact in FACT_SHORTS)
    assert all(fact.title and all(segment for segment in fact.narration) for fact in FACT_SHORTS)
    assert all(fact.sources and all(source.startswith("https://") for source in fact.sources) for fact in FACT_SHORTS)


def test_free_fact_scheduler_matches_utc_cron_to_eastern_dst_slot():
    from zoneinfo import ZoneInfo

    eastern = ZoneInfo("America/New_York")
    assert scheduled_slot_from_cron(
        "0 12 * * *",
        datetime(2026, 9, 27, 8, 5, tzinfo=eastern),
    ) == "morning"
    assert scheduled_slot_from_cron(
        "0 17 * * *",
        datetime(2026, 9, 27, 13, 5, tzinfo=eastern),
    ) == "afternoon"
    assert scheduled_slot_from_cron(
        "0 21 * * *",
        datetime(2026, 9, 27, 17, 5, tzinfo=eastern),
    ) == "evening"
    assert scheduled_slot_from_cron(
        "0 12 * * *",
        datetime(2026, 1, 27, 7, 5, tzinfo=eastern),
    ) is None
    assert scheduled_slot_from_cron(
        "0 12 * * *",
        datetime(2026, 9, 27, 9, 31, tzinfo=eastern),
    ) is None


def test_fact_video_uses_animated_vertical_cards_and_full_length_audio(monkeypatch, tmp_path):
    from ai_kids_video_agent import free_shorts

    cards = tmp_path / "cards"
    cards.mkdir()
    for index in range(6):
        (cards / f"card_{index + 1:02d}.png").write_bytes(b"card")
    monkeypatch.setattr(free_shorts, "render_fact_cards", lambda *_args: cards)
    captured = {}

    def fake_run(command, check):
        captured["command"] = command
        assert check is True
        if command[0] == "espeak-ng":
            Path(command[command.index("-w") + 1]).write_bytes(b"audio")
        else:
            Path(command[-1]).write_bytes(b"video")

    monkeypatch.setattr(free_shorts.subprocess, "run", fake_run)
    video = create_fact_video(
        FACT_SHORTS[0],
        tmp_path / "out",
        date(2026, 9, 27),
        "morning",
    )
    command = captured["command"]
    filters = command[command.index("-filter_complex") + 1]

    assert video.is_file()
    assert command.count("-loop") == 6
    assert command[-1] == str(video)
    assert "zoompan=" in filters
    assert "concat=n=6" in filters
    assert "apad=pad_dur=36" in filters
    assert command[command.index("-level:v") + 1] == "4.1"
    assert "-shortest" not in command


def test_preview_only_never_calls_youtube_publish(monkeypatch, tmp_path, capsys):
    from ai_kids_video_agent import free_shorts

    rendered = tmp_path / "preview.mp4"
    monkeypatch.setattr(
        free_shorts,
        "create_fact_video",
        lambda *_args: rendered,
    )
    monkeypatch.setattr(
        free_shorts,
        "publish_one",
        lambda *_args: (_ for _ in ()).throw(AssertionError("preview must not upload")),
    )

    assert run_automation("morning", tmp_path, preview_only=True) == 0
    assert "Preview ready (not uploaded)" in capsys.readouterr().out


def test_original_ambient_music_is_stereo_and_exact_duration(tmp_path):
    path = synthesize_ambient_music(tmp_path / "ambient.wav", "Clownfish", duration_seconds=3)
    with wave.open(str(path), "rb") as music:
        assert music.getnchannels() == 2
        assert music.getframerate() == 22050
        assert music.getnframes() == 3 * 22050
        samples = music.readframes(20)
    assert len(samples) == 20 * 2 * 2
    assert any(struct.unpack("<h", samples[index : index + 2])[0] != 0 for index in range(0, len(samples), 2))


def test_us_release_slots_follow_eastern_daylight_time():
    winter = publish_time(date(2026, 1, 15), 9)
    summer = publish_time(date(2026, 7, 15), 9)
    assert winter.hour == summer.hour == 9
    assert winter.utcoffset() != summer.utcoffset()
    assert publish_time(date(2026, 9, 26), 18).hour == 18


def test_youtube_service_accepts_self_contained_github_oauth_token(monkeypatch, tmp_path):
    from ai_kids_video_agent import youtube

    token_path = tmp_path / "github-token.json"
    token_path.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("YOUTUBE_TOKEN_FILE", str(token_path))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    built = {}

    class FakeCredentials:
        expired = False
        refresh_token = "refresh-token"
        valid = True

        @classmethod
        def from_authorized_user_file(cls, path, scopes):
            assert path == str(token_path)
            assert scopes == [youtube.UPLOAD_SCOPE]
            return cls()

    def fake_build(name, version, **kwargs):
        built.update({"name": name, "version": version, **kwargs})
        return object()

    monkeypatch.setattr(
        youtube,
        "_libraries",
        lambda: (None, FakeCredentials, None, fake_build, None),
    )

    assert youtube_service() is not None
    assert built["name"] == "youtube"
    assert built["version"] == "v3"
    assert not (tmp_path / "appdata" / "ai-kids-video-agent" / "client_secret.json").exists()


def test_daily_task_uses_short_launcher_and_requested_output(monkeypatch, tmp_path):
    from ai_kids_video_agent import youtube

    output = tmp_path / "project" / "output"
    credentials = tmp_path / "credentials"
    captured = {}
    monkeypatch.setattr(youtube.sys, "platform", "win32")
    monkeypatch.setattr(youtube, "youtube_service", lambda: object())
    monkeypatch.setattr(youtube, "credential_directory", lambda: credentials)
    monkeypatch.setenv("WINDIR", str(tmp_path / "Windows"))

    def fake_run(args, **kwargs):
        captured["args"] = args
        return youtube.subprocess.CompletedProcess(args, 0, stdout="created", stderr="")

    monkeypatch.setattr(youtube.subprocess, "run", fake_run)
    assert install_daily_task(output) == "created"

    task_run = captured["args"][captured["args"].index("/TR") + 1]
    launcher = credentials / "run_ocean_shorts_daily.cmd"
    script = launcher.read_text(encoding="utf-8")
    assert len(task_run) <= 261
    assert str(launcher) in task_run
    assert f'cd /d "{output}"' in script
    assert f'--output-dir "{output}"' in script
    assert f'>> "{output / "schedule.log"}" 2>&1' in script


def test_telegram_setup_uses_latest_private_chat_and_sends_test(monkeypatch, tmp_path, capsys):
    from ai_kids_video_agent import telegram_notify

    config_path = tmp_path / "local" / "ai-kids-video-agent" / "telegram.json"
    monkeypatch.setattr(telegram_notify, "_config_path", lambda: config_path)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setattr(
        telegram_notify,
        "getpass",
        lambda _prompt: "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl",
    )
    calls = []

    def fake_call(token, method, payload=None):
        calls.append((token, method, payload))
        if method == "getUpdates":
            return {
                "result": [
                    {"message": {"chat": {"id": 123, "type": "group"}}},
                    {"message": {"chat": {"id": 456, "type": "private"}}},
                ]
            }
        return {"ok": True}

    monkeypatch.setattr(telegram_notify, "_call_bot_api", fake_call)
    telegram_notify.configure_telegram()
    saved = json.loads(config_path.read_text(encoding="utf-8"))

    assert saved == {
        "bot_token": "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl",
        "chat_id": 456,
    }
    assert calls[-1][1:] == (
        "sendMessage",
        {
            "chat_id": 456,
            "text": "✅ Ocean Glow bildirishnomalari ulandi. Agent video tayyorlaganda yoki xato yuz berganda xabar yuboradi.",
        },
    )
    assert "ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in capsys.readouterr().out


def test_telegram_setup_reads_token_from_environment(monkeypatch, tmp_path):
    from ai_kids_video_agent import telegram_notify

    config_path = tmp_path / "local" / "telegram.json"
    monkeypatch.setattr(telegram_notify, "_config_path", lambda: config_path)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl")
    monkeypatch.setattr(
        telegram_notify,
        "getpass",
        lambda _prompt: (_ for _ in ()).throw(AssertionError("must use environment token")),
    )
    monkeypatch.setattr(
        telegram_notify,
        "_call_bot_api",
        lambda _token, method, _payload=None: (
            {"result": [{"message": {"chat": {"id": 456, "type": "private"}}}]}
            if method == "getUpdates"
            else {"ok": True}
        ),
    )

    telegram_notify.configure_telegram()
    assert json.loads(config_path.read_text(encoding="utf-8")) == {
        "bot_token": "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl",
        "chat_id": 456,
    }


def test_telegram_setup_extracts_token_from_copied_botfather_message(monkeypatch, tmp_path):
    from ai_kids_video_agent import telegram_notify

    config_path = tmp_path / "telegram.json"
    monkeypatch.setattr(telegram_notify, "_config_path", lambda: config_path)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setattr(
        telegram_notify,
        "getpass",
        lambda _prompt: "Use this token: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno\\_",
    )
    sent = []
    monkeypatch.setattr(
        telegram_notify,
        "_call_bot_api",
        lambda token, method, payload=None: (
            {"result": [{"message": {"chat": {"id": 456, "type": "private"}}}]}
            if method == "getUpdates"
            else sent.append((token, method, payload)) or {"ok": True}
        ),
    )

    telegram_notify.configure_telegram()

    assert json.loads(config_path.read_text(encoding="utf-8")) == {
        "bot_token": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno_",
        "chat_id": 456,
    }


def test_telegram_notification_sends_configured_message(monkeypatch, tmp_path):
    from ai_kids_video_agent import telegram_notify

    config_path = tmp_path / "telegram.json"
    config_path.write_text(
        json.dumps({"bot_token": "bot-token", "chat_id": 99}),
        encoding="utf-8",
    )
    monkeypatch.setattr(telegram_notify, "_config_path", lambda: config_path)
    calls = []
    monkeypatch.setattr(
        telegram_notify,
        "_call_bot_api",
        lambda token, method, payload=None: calls.append((token, method, payload)) or {"ok": True},
    )

    assert telegram_notify.send_telegram_notification("Video scheduled")
    assert calls == [
        ("bot-token", "sendMessage", {"chat_id": 99, "text": "Video scheduled"})
    ]


def test_telegram_notification_reads_github_secrets(monkeypatch, tmp_path):
    from ai_kids_video_agent import telegram_notify

    monkeypatch.setattr(telegram_notify, "_config_path", lambda: tmp_path / "missing.json")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
    calls = []
    monkeypatch.setattr(
        telegram_notify,
        "_call_bot_api",
        lambda token, method, payload=None: calls.append((token, method, payload)) or {"ok": True},
    )

    assert telegram_notify.send_telegram_notification("Scheduled")
    assert calls == [
        (
            "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl",
            "sendMessage",
            {"chat_id": "42", "text": "Scheduled"},
        )
    ]


def test_youtube_upload_is_scheduled_private_and_general_audience(monkeypatch, tmp_path):
    from ai_kids_video_agent import youtube

    video = tmp_path / "ocean.mp4"
    video.write_bytes(b"test video")
    captured = {}

    class FakeMediaUpload:
        def __init__(self, *args, **kwargs):
            captured["media"] = (args, kwargs)

    class FakeUpload:
        def next_chunk(self):
            return None, {"id": "uploaded-video-id"}

    class FakeVideos:
        def insert(self, **kwargs):
            captured["upload"] = kwargs
            return FakeUpload()

    class FakeService:
        def videos(self):
            return FakeVideos()

    monkeypatch.setattr(
        youtube,
        "_libraries",
        lambda: (None, None, None, None, FakeMediaUpload),
    )
    release = datetime.now(timezone.utc) + timedelta(days=1)
    video_id = upload_scheduled_video(
        video,
        {
            "title": "Hologram Clownfish",
            "description": "Original CGI ocean art",
            "tags": ["ocean", "Shorts"],
            "category_id": "15",
            "language": "en",
        },
        release,
        service=FakeService(),
    )
    assert video_id == "uploaded-video-id"
    assert captured["upload"]["body"]["status"] == {
        "privacyStatus": "private",
        "publishAt": release.isoformat(timespec="seconds"),
        "selfDeclaredMadeForKids": False,
    }
    assert captured["upload"]["notifySubscribers"] is False
    assert captured["upload"]["part"] == "snippet,status"


def test_speech_uses_selected_installed_voice_and_writes_wav(monkeypatch, tmp_path):
    import ai_kids_video_agent.speech as speech

    monkeypatch.setattr(speech.sys, "platform", "win32")
    monkeypatch.setattr(speech.shutil, "which", lambda name: "powershell.exe")
    captured = {}

    def fake_run(command, **kwargs):
        captured["payload"] = json.loads(kwargs["input"])
        captured["command"] = command
        with wave.open(captured["payload"]["output"], "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(16000)
            audio.writeframes(b"\x00\x00" * 16000)

    monkeypatch.setattr(speech.subprocess, "run", fake_run)
    plan = build_story_plan("The main detail is here", "https://example.com", "Example News")
    output = tmp_path / "narration.wav"
    duration = synthesize_speech(plan, output, voice=DEFAULT_VOICE)
    assert duration == 1
    assert captured["payload"]["voice"] == DEFAULT_VOICE
    assert "SelectVoice" in captured["command"][-1]


def test_choose_story_sorts_newest_first_and_deduplicates():
    older = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    newer = datetime.now(timezone.utc).isoformat()
    stories = [
        NewsItem("Old", "https://example.com/old", "example", published_at=older),
        NewsItem("New", "https://example.com/new", "example", published_at=newer),
        NewsItem("Duplicate", "https://example.com/new", "another", published_at=newer),
    ]
    chosen = choose_story(stories, limit=2)
    assert [item.title for item in chosen] == ["New", "Old"]


def test_api_key_is_sent_as_bearer_and_generated_script_is_valid(monkeypatch):
    narration = [
        "Here is the latest report. The headline says local leaders approved a new plan. "
        "The source explains the decision and shares the details.",
        "Officials say the change will begin next month. The report explains who may be affected "
        "and what steps come next. These details come from the linked source.",
        "Readers should check the original report for exact dates and updates. This short "
        "explanation uses only the published summary. That is the story for now.",
    ]
    generated = {
        "summary": "The local report describes a newly approved plan.",
        "script": [
            {"scene": f"Scene {i}", "narration": text, "visual": "3D scene"}
            for i, text in enumerate(narration, start=1)
        ],
    }
    response = {
        "choices": [{"message": {"content": json.dumps(generated)}}],
    }
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def read(self):
            return json.dumps(response).encode()

    def fake_urlopen(request, timeout):
        captured["authorization"] = request.get_header("Authorization")
        return FakeResponse()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    plan = create_story_from_headline(
        "Local leaders approve a new plan",
        "https://example.com/story",
        "Example News",
        "The local report describes a newly approved plan.",
    )
    assert captured["authorization"] == "Bearer test-key"
    assert MIN_SCRIPT_WORDS <= word_count(" ".join(s.narration for s in plan.script)) <= MAX_SCRIPT_WORDS


def test_cli_script_only_pipeline_saves_source_and_script(tmp_path, monkeypatch):
    item = NewsItem(
        title="A major local update",
        link="https://example.com/news",
        source="Example News",
        summary="Officials announced a new plan today.",
    )
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("ai_kids_video_agent.cli.get_recent_stories", lambda _urls, limit: [item])

    assert main(["--skip-render", "--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "story.json").is_file()
    assert (tmp_path / "story_plan.json").is_file()
    assert (tmp_path / "youtube_metadata.json").is_file()
    saved = json.loads((tmp_path / "story_plan.json").read_text(encoding="utf-8"))
    assert saved["source_url"] == item.link
    assert 30 <= saved["duration_seconds"] <= 45
    assert saved["word_count"] == word_count(" ".join(scene["narration"] for scene in saved["script"]))
    metadata = json.loads((tmp_path / "youtube_metadata.json").read_text(encoding="utf-8"))
    assert metadata["source_url"] == item.link
    assert metadata["hashtags"] == ["#Shorts", "#News", "#WorldNews"]


def test_cli_keeps_script_and_reports_missing_renderer(tmp_path, monkeypatch, capsys):
    item = NewsItem(
        title="A major local update",
        link="https://example.com/news",
        source="Example News",
        summary="Officials announced a new plan today.",
    )
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("ai_kids_video_agent.cli.get_recent_stories", lambda _urls, limit: [item])

    def missing_blender(_name):
        raise FileNotFoundError("Required executable 'blender' was not found in PATH.")

    monkeypatch.setattr("ai_kids_video_agent.render.ensure_executable", missing_blender)
    assert main(["--output-dir", str(tmp_path)]) == 1
    assert (tmp_path / "story_plan.json").is_file()
    assert "blender" in capsys.readouterr().err

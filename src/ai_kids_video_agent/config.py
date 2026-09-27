import os

DEFAULT_RSS_URLS = (
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.theverge.com/rss/index.xml",
)


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def get_rss_urls() -> list[str]:
    urls = _split_csv(os.getenv("NEWS_RSS_URLS"))
    return urls or list(DEFAULT_RSS_URLS)


def get_openai_settings() -> dict[str, str | None]:
    return {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    }


def get_output_dir() -> str:
    return os.getenv("OUTPUT_DIR", "output")


def get_runtime_settings() -> dict[str, object]:
    return {
        "rss_urls": get_rss_urls(),
        "output_dir": get_output_dir(),
        "openai": get_openai_settings(),
    }

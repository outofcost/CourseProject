from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"
LOOKUPS_DIR = DATA_DIR / "lookups"
MANUAL_DIR = DATA_DIR / "manual"
LOGS_DIR = ROOT / "logs"
CACHE_DIR = ROOT / ".cache"

for _d in (RAW_DIR, CLEAN_DIR, LOOKUPS_DIR, MANUAL_DIR, LOGS_DIR, CACHE_DIR):
    _d.mkdir(parents=True, exist_ok=True)

SEASONS = list(range(2016, 2025))

MIN_GP = 20
MIN_MPG = 5
MIN_SALARY = 100_000
MAX_PLAUSIBLE_SALARY = 100_000_000

DEFAULT_DELAY_SEC = 3.5
RETRY_STATUSES = (429, 503, 502, 504)
RETRY_MAX_ATTEMPTS = 3
RETRY_BACKOFF_BASE = 4.0

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

HTTP_HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

URLS = {
    "bbref_per_game": "https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html",
    "bbref_advanced": "https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html",
    "bbref_draft": "https://www.basketball-reference.com/draft/NBA_{year}.html",
    "bbref_allstar": "https://www.basketball-reference.com/allstar/NBA_{year}.html",
    "hoopshype_salaries": (
        "https://web.archive.org/web/{ts}id_/"
        "https://hoopshype.com/salaries/players/{start}-{end}/"
    ),
}

WAYBACK_DOMAIN = "web.archive.org"
WAYBACK_TIMEOUT_SEC = 90
WAYBACK_DELAY_SEC = 5.0


def hoopshype_wayback_url(season_end: int) -> str:
    """Build Wayback URL for hoopshype salaries page of given season-end year.

    Live hoopshype geo-redirects EU traffic to a stripped EU domain that lacks
    historical per-season pages. Wayback snapshots preserve the original HTML
    table layout that's parseable without JS.
    """
    ts = f"{season_end}0601"
    return URLS["hoopshype_salaries"].format(
        ts=ts, start=season_end - 1, end=season_end
    )

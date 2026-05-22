from __future__ import annotations

import hashlib
import json
import logging
import random
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from curl_cffi import requests as crequests

from .config import (
    CACHE_DIR,
    DEFAULT_DELAY_SEC,
    HTTP_HEADERS,
    RETRY_BACKOFF_BASE,
    RETRY_MAX_ATTEMPTS,
    RETRY_STATUSES,
    WAYBACK_DELAY_SEC,
    WAYBACK_DOMAIN,
    WAYBACK_TIMEOUT_SEC,
)

log = logging.getLogger("nba_scraper.http")

CACHE_MAX_AGE_DAYS = 30
CLOUDFLARE_DOMAINS = {"www.basketball-reference.com", "basketball-reference.com"}

_last_hit: dict[str, float] = {}
_lock = threading.Lock()
_curl_session: Optional[crequests.Session] = None
_plain_session: Optional[requests.Session] = None


@dataclass
class FetchResult:
    url: str
    status_code: int
    text: str
    from_cache: bool

    @property
    def content_length(self) -> int:
        return len(self.text)


def _get_curl_session() -> crequests.Session:
    global _curl_session
    if _curl_session is None:
        _curl_session = crequests.Session(impersonate="chrome")
    return _curl_session


def _get_plain_session() -> requests.Session:
    global _plain_session
    if _plain_session is None:
        s = requests.Session()
        s.headers.update(HTTP_HEADERS)
        _plain_session = s
    return _plain_session


def _cache_paths(url: str) -> tuple[Path, Path]:
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
    return CACHE_DIR / f"{h}.html", CACHE_DIR / f"{h}.meta.json"


def _read_cache(url: str, max_age_days: int) -> Optional[str]:
    body_path, meta_path = _cache_paths(url)
    if not (body_path.exists() and meta_path.exists()):
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    age_days = (time.time() - meta.get("fetched_at", 0)) / 86400
    if age_days > max_age_days:
        return None
    if meta.get("status") != 200:
        return None
    return body_path.read_text(encoding="utf-8")


def _write_cache(url: str, text: str, status: int) -> None:
    body_path, meta_path = _cache_paths(url)
    body_path.write_text(text, encoding="utf-8")
    meta_path.write_text(
        json.dumps({"url": url, "status": status, "fetched_at": time.time()}, indent=2),
        encoding="utf-8",
    )


def _throttle(domain: str, delay: float) -> None:
    with _lock:
        last = _last_hit.get(domain)
        if last is not None:
            wait = delay - (time.monotonic() - last)
            if wait > 0:
                time.sleep(wait + random.uniform(0.0, 0.4))
        _last_hit[domain] = time.monotonic()


def _needs_cloudflare(domain: str) -> bool:
    return domain in CLOUDFLARE_DOMAINS


def fetch(
    url: str,
    delay: float = DEFAULT_DELAY_SEC,
    force_refresh: bool = False,
    max_age_days: int = CACHE_MAX_AGE_DAYS,
) -> FetchResult:
    domain = urlparse(url).netloc

    if not force_refresh:
        cached = _read_cache(url, max_age_days)
        if cached is not None:
            log.info("GET %s -> 200 [CACHE] (%d chars)", url, len(cached))
            return FetchResult(url=url, status_code=200, text=cached, from_cache=True)

    is_wayback = domain == WAYBACK_DOMAIN
    effective_delay = WAYBACK_DELAY_SEC if is_wayback else delay
    timeout_sec = WAYBACK_TIMEOUT_SEC if is_wayback else 30

    _throttle(domain, effective_delay)
    use_cf = _needs_cloudflare(domain)

    last_exc: Exception | None = None
    for attempt in range(1, RETRY_MAX_ATTEMPTS + 1):
        try:
            if use_cf:
                resp = _get_curl_session().get(url, timeout=timeout_sec)
            else:
                resp = _get_plain_session().get(url, timeout=timeout_sec)

            status = resp.status_code
            text = resp.text
            log.info(
                "GET %s -> %d (%d chars, attempt %d, %s)",
                url,
                status,
                len(text),
                attempt,
                "curl_cffi" if use_cf else "requests",
            )

            if status in RETRY_STATUSES:
                raise RuntimeError(f"retryable status {status}")

            if status >= 400:
                raise RuntimeError(f"http {status}")

            if use_cf and "just a moment" in text.lower():
                raise RuntimeError("cloudflare challenge page returned")

            _write_cache(url, text, status)
            return FetchResult(url=url, status_code=status, text=text, from_cache=False)

        except Exception as exc:
            last_exc = exc
            if attempt == RETRY_MAX_ATTEMPTS:
                break
            backoff = RETRY_BACKOFF_BASE * (2 ** (attempt - 1)) + random.uniform(0.0, 1.5)
            log.warning("attempt %d failed for %s: %s (sleep %.1fs)", attempt, url, exc, backoff)
            time.sleep(backoff)

    assert last_exc is not None
    raise last_exc


def clear_cache(url: Optional[str] = None) -> int:
    if url is not None:
        body, meta = _cache_paths(url)
        n = 0
        for p in (body, meta):
            if p.exists():
                p.unlink()
                n += 1
        return n
    removed = 0
    for p in CACHE_DIR.glob("*.html"):
        p.unlink()
        removed += 1
    for p in CACHE_DIR.glob("*.meta.json"):
        p.unlink()
        removed += 1
    return removed

from __future__ import annotations

import logging
import sys

from .config import LOGS_DIR

_INITIALIZED = False


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    global _INITIALIZED

    logger = logging.getLogger("nba_scraper")
    if _INITIALIZED:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOGS_DIR / "scrape.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    _INITIALIZED = True
    return logger

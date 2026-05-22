from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd
from unidecode import unidecode

from .config import LOOKUPS_DIR

log = logging.getLogger("nba_scraper.names")

ALIAS_FILE = LOOKUPS_DIR / "name_aliases.csv"

_SUFFIX_RE = re.compile(r"\s+(jr|sr|ii|iii|iv|v)\.?$", flags=re.IGNORECASE)
_PUNCT_RE = re.compile(r"[\.\,\'\"‘’“”`]")
_DASH_RE = re.compile(r"[-_]+")
_WS_RE = re.compile(r"\s+")


def canonicalize_name(name: str | float | None) -> str:
    if name is None or (isinstance(name, float) and pd.isna(name)):
        return ""
    s = str(name).strip()
    if not s:
        return ""

    s = unidecode(s)
    s = s.lower()
    s = _PUNCT_RE.sub("", s)
    s = _DASH_RE.sub(" ", s)
    s = _SUFFIX_RE.sub("", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def load_aliases() -> dict[str, str]:
    if not ALIAS_FILE.exists():
        return {}
    try:
        df = pd.read_csv(ALIAS_FILE)
    except Exception as exc:
        log.warning("failed to read aliases file %s: %s", ALIAS_FILE, exc)
        return {}
    if not {"alias", "canonical"}.issubset(df.columns):
        log.warning("aliases file missing alias/canonical columns: %s", ALIAS_FILE)
        return {}
    return dict(zip(df["alias"].map(canonicalize_name), df["canonical"].map(canonicalize_name)))


def ensure_alias_template() -> Path:
    if not ALIAS_FILE.exists():
        pd.DataFrame(
            {
                "alias": ["nikola jokic typo", "luka doncic typo"],
                "canonical": ["nikola jokic", "luka doncic"],
                "note": ["example row — replace with real fixes", "example row"],
            }
        ).iloc[0:0].to_csv(ALIAS_FILE, index=False)
        log.info("created empty alias template at %s", ALIAS_FILE)
    return ALIAS_FILE


def apply_aliases(canon_series: pd.Series, aliases: dict[str, str] | None = None) -> pd.Series:
    aliases = aliases if aliases is not None else load_aliases()
    if not aliases:
        return canon_series
    return canon_series.map(lambda x: aliases.get(x, x))

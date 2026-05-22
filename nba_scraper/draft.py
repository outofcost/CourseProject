from __future__ import annotations

import logging
import re

import pandas as pd
from bs4 import BeautifulSoup, Tag

from .config import CLEAN_DIR, RAW_DIR, URLS
from .http_client import fetch
from .names import apply_aliases, canonicalize_name, load_aliases

log = logging.getLogger("nba_scraper.draft")

_SLUG_RE = re.compile(r"/players/[a-z]/([a-z0-9]+)\.html")

DEFAULT_DRAFT_FROM = 1996
DEFAULT_DRAFT_TO = 2024


def _extract_slug(cell: Tag) -> str | None:
    if cell is None:
        return None
    slug = cell.get("data-append-csv")
    if slug:
        return slug
    link = cell.find("a")
    if link and link.get("href"):
        m = _SLUG_RE.search(link["href"])
        if m:
            return m.group(1)
    return None


def _parse_draft_page(html: str, year: int) -> pd.DataFrame:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id="stats")
    if table is None:
        raise RuntimeError(f"draft table id='stats' not found on year={year}")

    tbody = table.find("tbody")
    rows: list[dict] = []
    for tr in tbody.find_all("tr", recursive=False):
        classes = tr.get("class") or []
        if "thead" in classes:
            continue

        player_cell = tr.find("td", attrs={"data-stat": "player"})
        if player_cell is None:
            continue
        name = player_cell.get_text(strip=True)
        if not name or name == "Player":
            continue
        slug = _extract_slug(player_cell)

        pick_cell = tr.find(["td", "th"], attrs={"data-stat": "pick_overall"})
        team_cell = tr.find("td", attrs={"data-stat": "team_id"})
        college_cell = tr.find("td", attrs={"data-stat": "college_name"})

        try:
            pick = int(pick_cell.get_text(strip=True)) if pick_cell else None
        except ValueError:
            pick = None

        rows.append(
            {
                "player_id": slug,
                "player_name": name,
                "draft_year": year,
                "draft_pick": pick,
                "draft_team": team_cell.get_text(strip=True) if team_cell else None,
                "college": college_cell.get_text(strip=True) if college_cell else None,
            }
        )

    if not rows:
        raise RuntimeError(f"no draft rows parsed for year={year}")
    df = pd.DataFrame(rows)
    df["draft_round"] = df["draft_pick"].apply(
        lambda p: 1 if p is not None and p <= 30 else (2 if p is not None else None)
    )
    return df


def scrape_draft(year: int) -> pd.DataFrame:
    url = URLS["bbref_draft"].format(year=year)
    resp = fetch(url)
    df = _parse_draft_page(resp.text, year)

    aliases = load_aliases()
    df["player_clean"] = df["player_name"].map(canonicalize_name)
    df["player_clean"] = apply_aliases(df["player_clean"], aliases)

    df = df[[
        "player_id", "player_clean", "player_name",
        "draft_year", "draft_round", "draft_pick", "draft_team", "college",
    ]]

    out_path = RAW_DIR / f"draft_{year}.csv"
    df.to_csv(out_path, index=False)
    log.info("wrote %s (%d picks)", out_path, len(df))
    return df


def consolidate_draft(year_from: int = DEFAULT_DRAFT_FROM, year_to: int = DEFAULT_DRAFT_TO) -> pd.DataFrame:
    parts = []
    for y in range(year_from, year_to + 1):
        p = RAW_DIR / f"draft_{y}.csv"
        if p.exists():
            parts.append(pd.read_csv(p))
    if not parts:
        raise RuntimeError("no per-year draft CSVs found in data/raw/")
    df = pd.concat(parts, ignore_index=True)
    df = df.dropna(subset=["player_id"]).drop_duplicates(subset=["player_id"], keep="first")
    out = CLEAN_DIR / "draft_picks.csv"
    df.to_csv(out, index=False)
    log.info("consolidated %s (%d unique players, years %d–%d)", out, len(df), year_from, year_to)
    return df

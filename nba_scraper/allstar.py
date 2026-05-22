from __future__ import annotations

import logging
import re

import pandas as pd
from bs4 import BeautifulSoup, Tag

from .config import CLEAN_DIR, RAW_DIR, URLS
from .http_client import fetch
from .names import apply_aliases, canonicalize_name, load_aliases

log = logging.getLogger("nba_scraper.allstar")

_SLUG_RE = re.compile(r"/players/[a-z]/([a-z0-9]+)\.html")


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


def _parse_allstar_page(html: str, season_end: int) -> pd.DataFrame:
    """Extract All-Star roster from a season's allstar page.

    Format varies year-to-year: East/West (2016, 2024) vs Team-captain
    (2018-2020). Strategy: take *all* tables on the page except `line_score`,
    each of which holds one All-Star roster.
    """
    soup = BeautifulSoup(html, "lxml")
    tables = [t for t in soup.find_all("table") if t.get("id") != "line_score"]
    if not tables:
        raise RuntimeError(f"no roster tables found on allstar page for {season_end}")

    rows: list[dict] = []
    for table in tables:
        team_label = table.get("id") or "?"
        tbody = table.find("tbody")
        if tbody is None:
            continue
        for tr in tbody.find_all("tr", recursive=False):
            if "thead" in (tr.get("class") or []):
                continue
            player_cell = tr.find(["td", "th"], attrs={"data-stat": "player"})
            if player_cell is None:
                continue
            name = player_cell.get_text(strip=True)
            if not name or name in {"Player", "Team Totals"}:
                continue
            slug = _extract_slug(player_cell)
            rows.append({
                "player_id": slug,
                "player_name": name,
                "season": season_end,
                "allstar_team": team_label,
                "allstar": 1,
            })

    if not rows:
        raise RuntimeError(f"no allstar rows parsed for season={season_end}")
    return pd.DataFrame(rows)


def scrape_allstar(season_end: int) -> pd.DataFrame:
    url = URLS["bbref_allstar"].format(year=season_end)
    resp = fetch(url)
    df = _parse_allstar_page(resp.text, season_end)

    aliases = load_aliases()
    df["player_clean"] = df["player_name"].map(canonicalize_name)
    df["player_clean"] = apply_aliases(df["player_clean"], aliases)

    df = df.dropna(subset=["player_id"]).drop_duplicates(
        subset=["player_id", "season"], keep="first"
    )
    df = df[["player_id", "player_clean", "player_name", "season", "allstar", "allstar_team"]]

    out_path = RAW_DIR / f"allstar_{season_end}.csv"
    df.to_csv(out_path, index=False)
    log.info("wrote %s (%d players)", out_path, len(df))
    return df


def consolidate_allstar(seasons: list[int]) -> pd.DataFrame:
    parts = []
    for s in seasons:
        p = RAW_DIR / f"allstar_{s}.csv"
        if p.exists():
            parts.append(pd.read_csv(p))
    if not parts:
        raise RuntimeError("no per-season allstar CSVs found in data/raw/")
    df = pd.concat(parts, ignore_index=True)
    out = CLEAN_DIR / "allstar_all.csv"
    df.to_csv(out, index=False)
    log.info("consolidated %s (%d player-season All-Stars)", out, len(df))
    return df

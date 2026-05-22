from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from .config import MIN_GP, MIN_MPG, RAW_DIR, URLS
from .http_client import fetch
from .names import apply_aliases, canonicalize_name, load_aliases

log = logging.getLogger("nba_scraper.bbref")


PER_GAME_RENAME = {
    "name_display": "player_name",
    "team_name_abbr": "team_abbr",
    "pos": "position",
    "games": "gp",
    "games_started": "gs",
    "mp_per_g": "mpg",
    "fg_per_g": "fg",
    "fga_per_g": "fga",
    "fg_pct": "fg_pct",
    "fg3_per_g": "fg3",
    "fg3a_per_g": "fg3a",
    "fg3_pct": "fg3_pct",
    "fg2_per_g": "fg2",
    "fg2a_per_g": "fg2a",
    "fg2_pct": "fg2_pct",
    "efg_pct": "efg_pct",
    "ft_per_g": "ft",
    "fta_per_g": "fta",
    "ft_pct": "ft_pct",
    "orb_per_g": "orb",
    "drb_per_g": "drb",
    "trb_per_g": "rpg",
    "ast_per_g": "apg",
    "stl_per_g": "spg",
    "blk_per_g": "bpg",
    "tov_per_g": "tov",
    "pf_per_g": "pf",
    "pts_per_g": "ppg",
}

ADVANCED_RENAME = {
    "name_display": "player_name",
    "team_name_abbr": "team_abbr",
    "pos": "position",
    "games": "gp",
    "mp": "mp_total",
    "per": "per",
    "ts_pct": "ts_pct",
    "fg3a_per_fga_pct": "fg3a_rate",
    "fta_per_fga_pct": "ft_rate",
    "orb_pct": "orb_pct",
    "drb_pct": "drb_pct",
    "trb_pct": "trb_pct",
    "ast_pct": "ast_pct",
    "stl_pct": "stl_pct",
    "blk_pct": "blk_pct",
    "tov_pct": "tov_pct",
    "usg_pct": "usg_pct",
    "ows": "ows",
    "dws": "dws",
    "ws": "ws",
    "ws_per_48": "ws_48",
    "obpm": "obpm",
    "dbpm": "dbpm",
    "bpm": "bpm",
    "vorp": "vorp",
}

PER_GAME_NUMERIC = [
    "age", "gp", "gs", "mpg",
    "fg", "fga", "fg_pct", "fg3", "fg3a", "fg3_pct",
    "fg2", "fg2a", "fg2_pct", "efg_pct",
    "ft", "fta", "ft_pct",
    "orb", "drb", "rpg", "apg", "spg", "bpg", "tov", "pf", "ppg",
]

ADVANCED_NUMERIC = [
    "age", "gp", "mp_total", "per", "ts_pct", "fg3a_rate", "ft_rate",
    "orb_pct", "drb_pct", "trb_pct", "ast_pct", "stl_pct", "blk_pct",
    "tov_pct", "usg_pct",
    "ows", "dws", "ws", "ws_48", "obpm", "dbpm", "bpm", "vorp",
]


def _parse_bbref_table(html: str, table_id: str, season: int) -> pd.DataFrame:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=table_id)
    if table is None:
        raise RuntimeError(f"table id={table_id!r} not found on page")

    rows: list[dict] = []
    tbody = table.find("tbody")
    if tbody is None:
        raise RuntimeError(f"<tbody> missing inside table id={table_id!r}")

    for tr in tbody.find_all("tr", recursive=False):
        if "thead" in (tr.get("class") or []):
            continue

        row: dict[str, object] = {}
        name_cell = tr.find("td", attrs={"data-stat": "name_display"})
        if name_cell is None:
            continue

        slug = name_cell.get("data-append-csv")
        if not slug:
            link = name_cell.find("a")
            if link and link.get("href"):
                href = link["href"]
                slug = href.rsplit("/", 1)[-1].replace(".html", "")
        if not slug:
            continue

        row["player_id"] = slug

        for cell in tr.find_all(["td", "th"]):
            stat = cell.get("data-stat")
            if not stat or stat == "ranker":
                continue
            text = cell.get_text(strip=True)
            row[stat] = text if text != "" else np.nan

        rows.append(row)

    if not rows:
        raise RuntimeError(f"table id={table_id!r} returned 0 data rows")

    df = pd.DataFrame(rows)
    df["season"] = season
    return df


def _apply_tot_filter(df: pd.DataFrame) -> pd.DataFrame:
    if "team_name_abbr" not in df.columns and "team_abbr" not in df.columns:
        return df
    col = "team_name_abbr" if "team_name_abbr" in df.columns else "team_abbr"
    has_tot = df.assign(_is_tot=df[col].isin(["TOT", "2TM", "3TM", "4TM"])).groupby(
        ["player_id", "season"], dropna=False
    )["_is_tot"].transform("any")
    keep_tot = has_tot & df[col].isin(["TOT", "2TM", "3TM", "4TM"])
    keep_single = (~has_tot)
    out = df[keep_tot | keep_single].copy()
    return out


def _coerce_numeric(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _add_player_clean(df: pd.DataFrame) -> pd.DataFrame:
    aliases = load_aliases()
    df["player_clean"] = df["player_name"].map(canonicalize_name)
    df["player_clean"] = apply_aliases(df["player_clean"], aliases)
    return df


def scrape_per_game(season: int) -> pd.DataFrame:
    url = URLS["bbref_per_game"].format(year=season)
    resp = fetch(url)
    df = _parse_bbref_table(resp.text, "per_game_stats", season)

    df = _apply_tot_filter(df)
    df = df.rename(columns=PER_GAME_RENAME)
    df = _coerce_numeric(df, PER_GAME_NUMERIC)
    df = _add_player_clean(df)

    keep = [
        "player_id", "player_clean", "player_name", "season",
        "team_abbr", "position", "age",
        "gp", "gs", "mpg",
        "fg", "fga", "fg_pct", "fg3", "fg3a", "fg3_pct",
        "fg2", "fg2a", "fg2_pct", "efg_pct",
        "ft", "fta", "ft_pct",
        "orb", "drb", "rpg", "apg",
        "spg", "bpg", "tov", "pf", "ppg",
    ]
    df = df[[c for c in keep if c in df.columns]].copy()

    before = len(df)
    df = df[(df["gp"] >= MIN_GP) & (df["mpg"] >= MIN_MPG)].copy()
    log.info(
        "per_game season=%d: %d raw rows -> %d after GP>=%d & MPG>=%d",
        season, before, len(df), MIN_GP, MIN_MPG,
    )

    out_path = RAW_DIR / f"per_game_{season}.csv"
    df.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(df))
    return df


def scrape_advanced(season: int) -> pd.DataFrame:
    url = URLS["bbref_advanced"].format(year=season)
    resp = fetch(url)
    df = _parse_bbref_table(resp.text, "advanced", season)

    df = _apply_tot_filter(df)
    df = df.rename(columns=ADVANCED_RENAME)
    df = _coerce_numeric(df, ADVANCED_NUMERIC)
    df = _add_player_clean(df)

    keep = [
        "player_id", "player_clean", "player_name", "season",
        "team_abbr", "position", "age", "gp", "mp_total",
        "per", "ts_pct", "fg3a_rate", "ft_rate",
        "orb_pct", "drb_pct", "trb_pct", "ast_pct", "stl_pct",
        "blk_pct", "tov_pct", "usg_pct",
        "ows", "dws", "ws", "ws_48",
        "obpm", "dbpm", "bpm", "vorp",
    ]
    df = df[[c for c in keep if c in df.columns]].copy()

    out_path = RAW_DIR / f"advanced_{season}.csv"
    df.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(df))
    return df


def scrape_bbref_season(season: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    pg = scrape_per_game(season)
    adv = scrape_advanced(season)
    return pg, adv

"""Scrape Basketball-Reference awards pages (All-NBA, All-Defensive, MVP, DPOY).

Output: data/clean/awards_panel.csv with columns
  player_id, season (=season_end_year), all_nba_team (0/1/2/3),
  all_defense_team (0/1/2), mvp (0/1), dpoy (0/1).

Player_id is extracted from <a href="/players/X/playerid.html"> in each cell.
Season strings of form "YYYY-YY" → season_end_year = YYYY + 1.

Run:
    python3 -m analysis_v2.data_collection.scrape_awards
"""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402
from nba_scraper.http_client import fetch  # noqa: E402

log = logging.getLogger("analysis_v2.awards")

ALL_NBA_URL = "https://www.basketball-reference.com/awards/all_league.html"
ALL_DEF_URL = "https://www.basketball-reference.com/awards/all_defense.html"
MVP_URL = "https://www.basketball-reference.com/awards/mvp.html"
DPOY_URL = "https://www.basketball-reference.com/awards/dpoy.html"

SEASONS = list(range(2016, 2025))  # season_end_year ∈ [2016, 2024] (for sanity-check & filtered output)
# Cumulative-count derivations need pre-panel history (e.g. Curry's 2014/15 All-NBA).
# We save full bbref history to awards_panel_full.csv and also a filtered awards_panel.csv.
FULL_HISTORY_START = 1947  # ABA/NBA-era; bbref has the full table.

_PID_RE = re.compile(r"/players/[a-z]/([a-z0-9]+)\.html")
_TEAM_MAP = {"1st": 1, "2nd": 2, "3rd": 3}


def _season_to_end_year(s: str) -> int | None:
    """'2015-16' → 2016. '2019-20' → 2020."""
    m = re.match(r"(\d{4})-(\d{2})", s)
    if not m:
        return None
    first = int(m.group(1))
    return first + 1


def _player_id_from_cell(cell) -> str | None:
    a = cell.find("a", href=True)
    if a is None:
        return None
    m = _PID_RE.search(a["href"])
    return m.group(1) if m else None


def parse_all_team_table(html: str, table_id: str, team_col: str) -> pd.DataFrame:
    """Parse an All-NBA/All-Defense style wide table.

    Rows: 1 row per (season, team-tier). Cells data-stat='1'..'N' are players.
    Returns long DataFrame: (player_id, season_end_year, team_col=1/2/3).
    """
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=table_id)
    if table is None:
        raise RuntimeError(f"table {table_id!r} not found")
    tbody = table.find("tbody")
    if tbody is None:
        raise RuntimeError(f"<tbody> missing in {table_id!r}")

    rows: list[dict] = []
    for tr in tbody.find_all("tr"):
        if "thead" in (tr.get("class") or []):
            continue
        season_cell = tr.find(attrs={"data-stat": "season"})
        team_cell = tr.find(attrs={"data-stat": "all_team"})
        if season_cell is None or team_cell is None:
            continue
        season_end = _season_to_end_year(season_cell.get_text(strip=True))
        if season_end is None:
            continue
        tier = _TEAM_MAP.get(team_cell.get_text(strip=True))
        if tier is None:
            continue

        for c in tr.find_all("td"):
            stat = c.get("data-stat")
            if stat is None or not stat.isdigit():
                continue
            pid = _player_id_from_cell(c)
            if pid:
                rows.append(
                    {
                        "player_id": pid,
                        "season_end_year": season_end,
                        team_col: tier,
                    }
                )
    return pd.DataFrame(rows)


def parse_solo_award_table(html: str, table_id: str, col: str) -> pd.DataFrame:
    """Parse MVP / DPOY table (one player per season)."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=table_id)
    if table is None:
        raise RuntimeError(f"table {table_id!r} not found")
    tbody = table.find("tbody")
    if tbody is None:
        raise RuntimeError(f"<tbody> missing in {table_id!r}")

    rows: list[dict] = []
    for tr in tbody.find_all("tr"):
        if "thead" in (tr.get("class") or []):
            continue
        season_cell = tr.find(attrs={"data-stat": "season"})
        player_cell = tr.find(attrs={"data-stat": "player"})
        if season_cell is None or player_cell is None:
            continue
        season_end = _season_to_end_year(season_cell.get_text(strip=True))
        if season_end is None:
            continue
        pid = _player_id_from_cell(player_cell)
        if pid is None:
            continue
        rows.append({"player_id": pid, "season_end_year": season_end, col: 1})
    return pd.DataFrame(rows)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    log.info("scraping All-NBA")
    all_nba = parse_all_team_table(
        fetch(ALL_NBA_URL).text, "awards_all_league", "all_nba_team"
    )
    log.info("All-NBA rows: %d", len(all_nba))

    log.info("scraping All-Defense")
    all_def = parse_all_team_table(
        fetch(ALL_DEF_URL).text, "awards_all_defense", "all_defense_team"
    )
    log.info("All-Defense rows: %d", len(all_def))

    log.info("scraping MVP")
    mvp = parse_solo_award_table(fetch(MVP_URL).text, "mvp_NBA", "mvp")
    log.info("MVP rows: %d", len(mvp))

    log.info("scraping DPOY")
    dpoy = parse_solo_award_table(fetch(DPOY_URL).text, "dpoy_NBA", "dpoy")
    log.info("DPOY rows: %d", len(dpoy))

    # Outer-join full history (no season filter) keyed by (player_id, season_end_year).
    full = all_nba
    for p in (all_def, mvp, dpoy):
        full = full.merge(p, on=["player_id", "season_end_year"], how="outer")
    for col in ["all_nba_team", "all_defense_team", "mvp", "dpoy"]:
        if col not in full.columns:
            full[col] = 0
        full[col] = full[col].fillna(0).astype(int)
    full = full.sort_values(["season_end_year", "all_nba_team", "player_id"]).reset_index(
        drop=True
    )
    full = full.rename(columns={"season_end_year": "season"})

    # Self-checks on the panel window
    log.info("sanity checks (within panel window):")
    for season in SEASONS:
        sub = full[full["season"] == season]
        n_anba = int((sub["all_nba_team"] > 0).sum())
        n_adef = int((sub["all_defense_team"] > 0).sum())
        n_mvp = int((sub["mvp"] > 0).sum())
        n_dpoy = int((sub["dpoy"] > 0).sum())
        ok_anba = "OK" if n_anba == 15 else "FAIL (expected 15)"
        ok_adef = "OK" if n_adef == 10 else "FAIL (expected 10)"
        ok_mvp = "OK" if n_mvp == 1 else "FAIL (expected 1)"
        ok_dpoy = "OK" if n_dpoy == 1 else "FAIL (expected 1)"
        log.info(
            "  %d: All-NBA=%d %s | All-Def=%d %s | MVP=%d %s | DPOY=%d %s",
            season,
            n_anba,
            ok_anba,
            n_adef,
            ok_adef,
            n_mvp,
            ok_mvp,
            n_dpoy,
            ok_dpoy,
        )

    full_path = CLEAN_DIR / "awards_panel_full.csv"
    full.to_csv(full_path, index=False)
    log.info("wrote %s (%d rows, full history)", full_path, len(full))

    panel = full[full["season"].isin(SEASONS)].reset_index(drop=True)
    panel_path = CLEAN_DIR / "awards_panel.csv"
    panel.to_csv(panel_path, index=False)
    log.info("wrote %s (%d rows, panel window)", panel_path, len(panel))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Scrape team-season records from basketball-reference (W-L, playoff result).

For each NBA team × season in [2016..2024], fetch
  https://www.basketball-reference.com/teams/{TEAM}/{YEAR}.html
parse the meta block for "Record: W-L" and the playoffs section.

Output: data/clean/team_season.csv with columns
  team_abbr, season, wins, losses, win_pct,
  made_playoffs (0/1),
  playoff_round_reached (0=missed, 1=R1, 2=Conf semis, 3=Conf finals, 4=Finals, 5=Champion)

Note on team abbreviations: bbref uses BRK, CHO, PHO (not BKN/CHA/PHX). We match the
existing panel which already uses BRK/CHO/PHO.

Run:
    python3 -m analysis_v2.data_collection.scrape_team_records
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

log = logging.getLogger("analysis_v2.team_records")

TEAM_URL = "https://www.basketball-reference.com/teams/{team}/{year}.html"
SEASONS = list(range(2016, 2025))
TEAMS = [
    "ATL", "BOS", "BRK", "CHI", "CHO", "CLE", "DAL", "DEN", "DET", "GSW",
    "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
    "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS",
]

_REC_RE = re.compile(r"Record:\s*(\d+)\s*-\s*(\d+)")
_WON_RE = re.compile(r"Won\s+(?:NBA|East|West)")
_LOST_RE = re.compile(r"Lost\s+(?:NBA|East|West)")


def parse_team_page(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    meta = soup.find(id="meta")
    if meta is None:
        return {
            "wins": None,
            "losses": None,
            "made_playoffs": 0,
            "playoff_round_reached": 0,
        }

    text = meta.get_text(" ", strip=True)
    rec = _REC_RE.search(text)
    wins = int(rec.group(1)) if rec else None
    losses = int(rec.group(2)) if rec else None

    # Playoffs section starts with "Playoffs" (e.g. "NBA 2017 Playoffs").
    pi = text.find("Playoffs")
    if pi == -1:
        return {
            "wins": wins,
            "losses": losses,
            "made_playoffs": 0,
            "playoff_round_reached": 0,
        }
    section = text[pi:]
    # Stop section at "More Team Info" or end.
    end = section.find("More Team Info")
    if end > -1:
        section = section[:end]

    n_won = len(_WON_RE.findall(section))
    n_lost = len(_LOST_RE.findall(section))

    if n_won == 0 and n_lost == 0:
        # "Playoffs" mentioned but no series found → likely play-in only / missed.
        return {
            "wins": wins,
            "losses": losses,
            "made_playoffs": 0,
            "playoff_round_reached": 0,
        }

    if n_won == 4 and n_lost == 0:
        reached = 5  # champion
    else:
        reached = min(n_won + 1, 4)  # lost in (n_won + 1)-th round

    return {
        "wins": wins,
        "losses": losses,
        "made_playoffs": 1,
        "playoff_round_reached": reached,
    }


def scrape_one(team: str, year: int) -> dict:
    url = TEAM_URL.format(team=team, year=year)
    try:
        resp = fetch(url)
    except Exception as exc:
        log.warning("FETCH FAIL %s %s: %s", team, year, exc)
        return {
            "team_abbr": team,
            "season": year,
            "wins": None,
            "losses": None,
            "win_pct": None,
            "made_playoffs": 0,
            "playoff_round_reached": 0,
            "fetch_error": str(exc),
        }
    info = parse_team_page(resp.text)
    info["team_abbr"] = team
    info["season"] = year
    info["fetch_error"] = None
    if info["wins"] is not None and info["losses"] is not None:
        total = info["wins"] + info["losses"]
        info["win_pct"] = info["wins"] / total if total > 0 else None
    else:
        info["win_pct"] = None
    return info


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    rows: list[dict] = []
    n = 0
    for year in SEASONS:
        for team in TEAMS:
            n += 1
            if n % 30 == 0:
                log.info("progress: %d / %d", n, len(TEAMS) * len(SEASONS))
            rows.append(scrape_one(team, year))

    df = pd.DataFrame(rows)
    out = CLEAN_DIR / "team_season.csv"
    df.to_csv(out, index=False)
    log.info("wrote %s (%d rows)", out, len(df))

    # Sanity: per-season wins sum = losses sum (zero-sum league).
    log.info("sanity: wins-sum == losses-sum per season")
    for s in SEASONS:
        sub = df[df["season"] == s]
        sw, sl = int(sub["wins"].sum()), int(sub["losses"].sum())
        flag = "OK" if sw == sl else f"FAIL ({sw} vs {sl})"
        log.info("  %d: W=%d, L=%d %s", s, sw, sl, flag)

    # Champion per season check.
    log.info("champions:")
    champs = df[df["playoff_round_reached"] == 5]
    for _, r in champs.iterrows():
        log.info("  %d: %s (%d-%d)", r["season"], r["team_abbr"], int(r["wins"]), int(r["losses"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import logging
import re

import pandas as pd
from bs4 import BeautifulSoup

from .config import (
    MAX_PLAUSIBLE_SALARY,
    MIN_SALARY,
    RAW_DIR,
    hoopshype_wayback_url,
)
from .http_client import fetch
from .names import apply_aliases, canonicalize_name, load_aliases

log = logging.getLogger("nba_scraper.hoopshype")


def _parse_salary_table(html: str, season_end: int) -> pd.DataFrame:
    """Parse the classic hoopshype salaries table (pre-2024 layout, served by Wayback).

    Structure:
      <table class="hh-salaries-ranking-table">
        <tr class="table-index"> <td class="rank"></td> <td class="name">Player</td>
            <td>2023/24</td> <td>2023/24(*)</td> </tr>
        <tr> <td class="rank">1.</td>
             <td class="name"><a href=".../stephen-curry/salary/">Stephen Curry</a></td>
             <td data-value="51915615">$51,915,915</td>   <-- nominal salary
             <td data-value="51915615">$51,915,915</td>   <-- inflation-adjusted (we ignore)
        </tr>
    """
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="hh-salaries-ranking-table")
    if table is None:
        tables = soup.find_all("table")
        raise RuntimeError(
            f"hoopshype salaries table not found; saw {len(tables)} tables on page"
        )

    rows: list[dict] = []
    for tr in table.find_all("tr"):
        if "table-index" in (tr.get("class") or []):
            continue
        name_cell = tr.find("td", class_="name")
        if name_cell is None:
            continue
        link = name_cell.find("a")
        player_name = (link.get_text(strip=True) if link else name_cell.get_text(strip=True))
        if not player_name or player_name.lower() == "player":
            continue

        href = link.get("href") if link else None
        slug = None
        if href:
            m = re.search(r"/player/([^/]+)/", href)
            if m:
                slug = m.group(1)

        salary_cells = [td for td in tr.find_all("td") if td.has_attr("data-value")]
        if not salary_cells:
            continue
        nominal_val = salary_cells[0].get("data-value")
        try:
            salary_usd = float(nominal_val)
        except (TypeError, ValueError):
            continue

        rows.append(
            {
                "player_name": player_name,
                "player_slug_hh": slug,
                "salary_usd": salary_usd,
                "season": season_end,
            }
        )

    if not rows:
        raise RuntimeError(f"no data rows parsed from hoopshype salaries table (season={season_end})")

    return pd.DataFrame(rows)


def scrape_salaries(season_end: int) -> pd.DataFrame:
    url = hoopshype_wayback_url(season_end)
    log.info("hoopshype season=%d via wayback: %s", season_end, url)
    resp = fetch(url)
    df = _parse_salary_table(resp.text, season_end)
    log.info("  parsed %d player rows from table", len(df))

    aliases = load_aliases()
    df["player_clean"] = df["player_name"].map(canonicalize_name)
    df["player_clean"] = apply_aliases(df["player_clean"], aliases)

    before = len(df)
    df = df[(df["salary_usd"] >= MIN_SALARY) & (df["salary_usd"] <= MAX_PLAUSIBLE_SALARY)].copy()
    log.info("  filtered $%s ≤ salary ≤ $%s: %d -> %d rows",
             f"{MIN_SALARY:,}", f"{MAX_PLAUSIBLE_SALARY:,}", before, len(df))

    df = (
        df.sort_values("salary_usd", ascending=False)
          .drop_duplicates(subset=["player_clean", "season"], keep="first")
          .reset_index(drop=True)
    )

    df = df[["player_clean", "player_name", "player_slug_hh", "season", "salary_usd"]]

    out_path = RAW_DIR / f"salaries_{season_end}.csv"
    df.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows, min=$%s, max=$%s)",
             out_path, len(df),
             f"{df['salary_usd'].min():,.0f}" if len(df) else "n/a",
             f"{df['salary_usd'].max():,.0f}" if len(df) else "n/a")
    return df

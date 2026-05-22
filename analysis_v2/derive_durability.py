"""Derive durability features from games_played (no external source).

Outputs (added to whatever panel is passed in):
  - season_length_t:        82 normally; 72 for COVID seasons (2020 & 2021)
  - games_missed_t:         season_length_t - gp (clipped at 0)
  - gp_pct_t:               gp / season_length_t (continuous alternative)
  - games_missed_lag1:      games_missed of t-1, by player_id
  - games_missed_3y_cum:    rolling 3-year cumulative (t-1, t-2, t-3), by player_id

Notes on season length:
  - 2019/20 (season_end=2020): regular season cut short for COVID, teams played 64–67 games.
    Bbref shows max games_played ≈ 75 league-wide (because some pre-bubble FAs played for two
    teams). Using `season_length=72` is the official "scheduled-but-not-played" benchmark; the
    `gp_pct_t` measure may exceed 1 for a handful of TOT rows, that's expected and noted.
  - 2020/21: officially 72 games. season_length=72.
  - All other seasons in window: 82.

Use as a function `add_durability_features(df)` or run as a script to produce a standalone CSV
keyed on (player_id, season).
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402

log = logging.getLogger("analysis_v2.durability")

COVID_SEASONS = {2020, 2021}  # season_end_year
COVID_SEASON_LENGTH = 72
DEFAULT_SEASON_LENGTH = 82


def season_length(season_end_year: int) -> int:
    return COVID_SEASON_LENGTH if season_end_year in COVID_SEASONS else DEFAULT_SEASON_LENGTH


def add_durability_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add games_missed_t, gp_pct_t, games_missed_lag1, games_missed_3y_cum to df.

    Requires columns: player_id, season, gp.
    """
    need = {"player_id", "season", "gp"}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    out = df.copy()
    out["season_length_t"] = out["season"].map(season_length).astype(int)
    out["games_missed_t"] = (out["season_length_t"] - out["gp"]).clip(lower=0)
    out["gp_pct_t"] = out["gp"] / out["season_length_t"]

    out = out.sort_values(["player_id", "season"]).reset_index(drop=True)

    g = out.groupby("player_id", sort=False)
    out["games_missed_lag1"] = g["games_missed_t"].shift(1)

    # 3-year cumulative miss: sum over t-1, t-2, t-3.
    lag1 = g["games_missed_t"].shift(1)
    lag2 = g["games_missed_t"].shift(2)
    lag3 = g["games_missed_t"].shift(3)
    out["games_missed_3y_cum"] = lag1.fillna(0) + lag2.fillna(0) + lag3.fillna(0)
    # If all three lags are NaN (i.e. season 1 in panel), keep NaN.
    out.loc[lag1.isna() & lag2.isna() & lag3.isna(), "games_missed_3y_cum"] = pd.NA

    return out


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    src = CLEAN_DIR / "data_analysis_v1.csv"
    panel = pd.read_csv(src, usecols=["player_id", "season", "gp"])
    log.info("input rows: %d", len(panel))

    out = add_durability_features(panel)
    out_path = CLEAN_DIR / "durability_panel.csv"
    out.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(out))

    # Sanity
    log.info("sanity: max games_played per season (should be ≤ season_length)")
    g = out.groupby("season").agg(max_gp=("gp", "max"), season_length=("season_length_t", "first"))
    for s, row in g.iterrows():
        flag = "OK" if row.max_gp <= row.season_length else "WARN (TOT rows likely)"
        log.info("  %d: max_gp=%d, length=%d  %s", s, row.max_gp, row.season_length, flag)

    log.info("median games_missed_t = %.1f", out["games_missed_t"].median())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

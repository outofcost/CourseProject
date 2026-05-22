"""Derive awards lag / cumulative / supermax features from awards_panel.csv.

Inputs:
  data/clean/awards_panel.csv — (player_id, season, all_nba_team, all_defense_team, mvp, dpoy)
  data/clean/data_analysis_v1.csv — base panel (for player_id × season scaffold, allstar)

Outputs:
  data/clean/awards_features.csv keyed on (player_id, season) with:
    - all_nba_lag1, all_defense_lag1, mvp_lag1, dpoy_lag1
    - career_all_nba_count, career_allstar_count, career_mvp_count, career_dpoy_count
      (cumulative count strictly BEFORE season — i.e. count over s < season)
    - supermax_eligible_loose:
        1 if  (all_nba(t-1) > 0)
           OR (#{s ∈ {t-1, t-2, t-3} : all_nba(s) > 0} ≥ 2)
           OR (mvp(t-1) > 0)
           OR (dpoy(t-1) > 0)
        else 0
        Masked to 0 for season < 2018 (CBA 2017 effective summer 2017).

Note on strict supermax: would additionally require experience ∈ {7,8,9} years and
same-team-as-draft. We compute the loose version here; strict is layered downstream
in prep_v2 using the existing `experience` and `draft_team` / `team_abbr` columns.

Run:
    python3 -m analysis_v2.derive_awards_features
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402

log = logging.getLogger("analysis_v2.awards_features")

SUPERMAX_FIRST_SEASON = 2018  # season_end_year (CBA 2017 effective summer 2017)


def build_awards_features(
    base_panel: pd.DataFrame, awards: pd.DataFrame
) -> pd.DataFrame:
    """For each (player_id, season) in base_panel, attach awards lags / cumsums / supermax_loose.

    base_panel must have columns: player_id, season, allstar.
    awards: player_id, season, all_nba_team, all_defense_team, mvp, dpoy.

    Returns dataframe keyed by (player_id, season).
    """
    # Build a sparse per-(player, season) award table. To make career_* cumulative counts
    # correct for players whose career started before the panel window, we extend min_s
    # back to the earliest season present in `awards` (typically 1947+).
    panel_seasons = sorted(base_panel["season"].unique().tolist())
    awards_min = int(awards["season"].min()) if len(awards) else min(panel_seasons) - 3
    min_s = min(awards_min, min(panel_seasons) - 3)
    max_s = max(panel_seasons)

    # Get every player who ever appears in panel.
    players = base_panel["player_id"].dropna().unique().tolist()

    # Full grid of (player_id, season).
    grid = pd.MultiIndex.from_product(
        [players, range(min_s, max_s + 1)], names=["player_id", "season"]
    )
    g = pd.DataFrame(index=grid).reset_index()

    # Join awards (left, so missing rows = 0).
    a = awards.copy()
    for c in ("all_nba_team", "all_defense_team", "mvp", "dpoy"):
        if c not in a.columns:
            a[c] = 0
    g = g.merge(a, on=["player_id", "season"], how="left").fillna(
        {"all_nba_team": 0, "all_defense_team": 0, "mvp": 0, "dpoy": 0}
    )
    # Indicator versions (1 if got the award, 0 otherwise).
    g["all_nba_ind"] = (g["all_nba_team"] > 0).astype(int)
    g["all_defense_ind"] = (g["all_defense_team"] > 0).astype(int)

    # Allstar from base panel.
    allstar = base_panel[["player_id", "season", "allstar"]].copy()
    allstar["allstar"] = allstar["allstar"].fillna(0).astype(int)
    g = g.merge(allstar, on=["player_id", "season"], how="left").fillna({"allstar": 0})

    g = g.sort_values(["player_id", "season"]).reset_index(drop=True)
    by = g.groupby("player_id", sort=False)

    # Lag-1 indicators.
    g["all_nba_lag1"] = by["all_nba_ind"].shift(1).fillna(0).astype(int)
    g["all_defense_lag1"] = by["all_defense_ind"].shift(1).fillna(0).astype(int)
    g["mvp_lag1"] = by["mvp"].shift(1).fillna(0).astype(int)
    g["dpoy_lag1"] = by["dpoy"].shift(1).fillna(0).astype(int)
    g["allstar_lag1"] = by["allstar"].shift(1).fillna(0).astype(int)

    # Cumulative counts strictly before current season.
    # cumsum is inclusive; subtract current value to get exclusive sum.
    g["career_all_nba_count"] = (by["all_nba_ind"].cumsum() - g["all_nba_ind"]).astype(int)
    g["career_allstar_count"] = (by["allstar"].cumsum() - g["allstar"]).astype(int)
    g["career_mvp_count"] = (by["mvp"].cumsum() - g["mvp"]).astype(int)
    g["career_dpoy_count"] = (by["dpoy"].cumsum() - g["dpoy"]).astype(int)
    g["career_all_defense_count"] = (
        by["all_defense_ind"].cumsum() - g["all_defense_ind"]
    ).astype(int)

    # 3-year rolling count of all_nba over t-1, t-2, t-3.
    lag1 = by["all_nba_ind"].shift(1).fillna(0)
    lag2 = by["all_nba_ind"].shift(2).fillna(0)
    lag3 = by["all_nba_ind"].shift(3).fillna(0)
    g["all_nba_3y_window"] = (lag1 + lag2 + lag3).astype(int)

    # Supermax-eligible (loose).
    eligible = (
        (g["all_nba_lag1"] == 1)
        | (g["all_nba_3y_window"] >= 2)
        | (g["mvp_lag1"] == 1)
        | (g["dpoy_lag1"] == 1)
    )
    g["supermax_eligible_loose"] = eligible.astype(int)
    g.loc[g["season"] < SUPERMAX_FIRST_SEASON, "supermax_eligible_loose"] = 0

    # Trim to panel-season window.
    g = g[g["season"].isin(panel_seasons)].reset_index(drop=True)
    keep = [
        "player_id",
        "season",
        "all_nba_lag1",
        "all_defense_lag1",
        "mvp_lag1",
        "dpoy_lag1",
        "allstar_lag1",
        "career_all_nba_count",
        "career_allstar_count",
        "career_mvp_count",
        "career_dpoy_count",
        "career_all_defense_count",
        "all_nba_3y_window",
        "supermax_eligible_loose",
    ]
    return g[keep].copy()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    base = pd.read_csv(
        CLEAN_DIR / "data_analysis_v1.csv", usecols=["player_id", "season", "allstar"]
    )
    awards_path = CLEAN_DIR / "awards_panel_full.csv"
    if not awards_path.exists():
        awards_path = CLEAN_DIR / "awards_panel.csv"
        log.warning("awards_panel_full.csv missing — falling back to filtered panel; "
                    "career_*_count will undercount pre-2016 awards.")
    awards = pd.read_csv(awards_path)
    log.info("base panel: %d rows; awards: %d rows", len(base), len(awards))

    feats = build_awards_features(base, awards)
    out = CLEAN_DIR / "awards_features.csv"
    feats.to_csv(out, index=False)
    log.info("wrote %s (%d rows)", out, len(feats))

    # Sanity checks
    log.info("sanity: supermax_eligible_loose by season")
    for s in sorted(feats["season"].unique()):
        n = int(feats[(feats["season"] == s) & (feats["supermax_eligible_loose"] == 1)].shape[0])
        log.info("  %d: %d eligible", s, n)

    # Curry should accumulate all_nba over time.
    curry = feats[feats["player_id"] == "curryst01"].sort_values("season")
    log.info(
        "Curry career_all_nba_count progression: %s",
        curry[["season", "career_all_nba_count"]].values.tolist(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

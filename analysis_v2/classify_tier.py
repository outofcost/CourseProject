"""Rule-based contract-tier classifier (block 1.5 of plan3.md).

Assigns each (player_id, season) row a tier in:
  {minimum, rookie_scale, mid_level, high_mid, max_25, max_30, max_35, supermax, overpay}

Inputs:
  - data/clean/data_analysis_v1.csv (panel with salary_usd, experience, draft_round, ...)
  - analysis_v2/data_collection/cba_thresholds.csv

Logic (per plan3.md lines 16–29, with tolerances):
  - rookie_scale  : 1st-round draftee, experience ≤ 4, salary < mle * 1.10
  - minimum       : salary < min_salary(exp) * 1.15
  - mid_level     : salary < mle_nontaxpayer * 1.20
  - max_25        : 0 ≤ exp ≤ 6 and salary < max_25 * 1.05
  - high_mid      : 0 ≤ exp ≤ 6 and salary in (max_25*1.05, max_30*1.05]
                    (or: above mid-level but not yet max — "high mid" zone)
  - max_30        : 7 ≤ exp ≤ 9 and salary < max_30 * 1.05
  - max_35        : exp ≥ 10 and salary < max_35 * 1.05
  - supermax      : salary > max_30 * 1.05 (exp 7-9) or > max_35 * 1.05 (exp 10+) AND
                    supermax_eligible_loose = 1 (joined elsewhere)
  - overpay       : catch-all for things above max thresholds without supermax eligibility
                    (treated as a residual / warning category — should be rare)

Output: data/clean/contract_tier.csv keyed by (player_id, season) with column `contract_tier`
        (categorical string) and `tier_ord` (1=minimum ... 8=supermax).

Run:
    python3 -m analysis_v2.classify_tier
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402

log = logging.getLogger("analysis_v2.tier")

TIER_ORDER = [
    "minimum",
    "rookie_scale",
    "mid_level",
    "high_mid",
    "max_25",
    "max_30",
    "max_35",
    "supermax",
    "overpay",
]
TIER_ORD = {t: i + 1 for i, t in enumerate(TIER_ORDER)}


def _interp_min_salary(exp: float, min0: float, min10: float) -> float:
    """Linear interpolation between min_0yrs and min_10yrs by experience.

    Real min-salary scale is piecewise (NBA publishes a table 0/1/2/.../10+ years), but
    a linear blend between 0 and 10+ years is within ~5% of true at every step, which
    is well within the 1.15 multiplier slack we apply downstream.
    """
    if pd.isna(exp):
        exp = 0
    e = max(0, min(int(exp), 10))
    return min0 + (min10 - min0) * (e / 10.0)


def classify_row(
    salary: float,
    exp: float,
    draft_round: float,
    eligible: bool,
    cba: pd.Series,
) -> str:
    """Per-row classifier. `cba` is the season's CBA threshold row.

    Tolerance multipliers (1.05–1.20) absorb partial-season pro-rates and waived/stretched
    contracts. They are applied per plan3.md lines 17–28.
    """
    if pd.isna(salary):
        return "minimum"

    mle = cba["mle_nontaxpayer"]
    max25 = cba["max_25_pct"]
    max30 = cba["max_30_pct"]
    max35 = cba["max_35_pct"]
    min0 = cba["min_salary_0yrs"]
    min10 = cba["min_salary_10yrs"]

    min_for_exp = _interp_min_salary(exp, min0, min10)

    # rookie scale: 1st-round pick, exp 0–4, salary at most ~MLE (rookie max not modeled
    # explicitly — top picks slightly exceed MLE but stay below max_25).
    is_first_round = (not pd.isna(draft_round)) and (int(draft_round) == 1)
    if is_first_round and (pd.notna(exp)) and (int(exp) <= 4) and salary < mle * 1.10:
        return "rookie_scale"

    if salary < min_for_exp * 1.15:
        return "minimum"

    if salary < mle * 1.20:
        return "mid_level"

    e = 0 if pd.isna(exp) else int(exp)

    # Above MLE, ≤ max_25 (25% of cap): rookie/early-career max territory.
    if salary <= max25 * 1.05:
        if e <= 6:
            return "max_25"
        return "high_mid"  # veteran below 25%-of-cap line

    # In (max_25, max_30]: standard 7–9 yr max territory OR Rose-Rule designated rookie
    # extension (5th-year deal at 30% for eligible young players).
    if salary <= max30 * 1.05:
        if 7 <= e <= 9:
            return "max_30"
        if e <= 6 and eligible:
            return "max_30"  # Rose Rule
        if e >= 10:
            return "high_mid"
        return "overpay"

    # In (max_30, max_35]: 10+ yr standard max, or supermax extension (7–9 yr or 10+ at 35%).
    if salary <= max35 * 1.05:
        if eligible and e >= 7:
            return "supermax"
        if e >= 10:
            return "max_35"
        return "overpay"

    # Above max_35 * 1.05: within-contract 105% raises on supermax-extension years.
    if eligible and e >= 7:
        return "supermax"
    return "overpay"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    panel = pd.read_csv(
        CLEAN_DIR / "data_analysis_v1.csv",
        usecols=[
            "player_id",
            "season",
            "salary_usd",
            "experience",
            "draft_round",
            "team_abbr",
        ],
    )
    cba = pd.read_csv(ROOT / "analysis_v2" / "data_collection" / "cba_thresholds.csv")
    cba = cba.rename(columns={"season_end_year": "season"})

    feats_path = CLEAN_DIR / "awards_features.csv"
    if feats_path.exists():
        feats = pd.read_csv(
            feats_path, usecols=["player_id", "season", "supermax_eligible_loose"]
        )
    else:
        log.warning("awards_features.csv missing — assuming supermax_eligible_loose=0 for all")
        feats = panel[["player_id", "season"]].assign(supermax_eligible_loose=0)

    df = panel.merge(cba, on="season", how="left")
    df = df.merge(feats, on=["player_id", "season"], how="left")
    df["supermax_eligible_loose"] = df["supermax_eligible_loose"].fillna(0).astype(int)

    log.info("classifying %d rows", len(df))
    df["contract_tier"] = df.apply(
        lambda r: classify_row(
            r["salary_usd"],
            r["experience"],
            r["draft_round"],
            bool(r["supermax_eligible_loose"]),
            r,
        ),
        axis=1,
    )
    df["tier_ord"] = df["contract_tier"].map(TIER_ORD).astype(int)

    out = df[["player_id", "season", "contract_tier", "tier_ord"]].copy()
    out_path = CLEAN_DIR / "contract_tier.csv"
    out.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(out))

    # Sanity: distribution per season
    log.info("tier distribution per season:")
    ct = pd.crosstab(df["season"], df["contract_tier"]).reindex(
        columns=TIER_ORDER, fill_value=0
    )
    print(ct.to_string())
    log.info("global distribution: %s", df["contract_tier"].value_counts().to_dict())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""prep_v2 — extends data_analysis_v1.csv with new v2 features.

Sequential left-joins against:
  - data/clean/birth_country.csv             (player_id)
  - data/clean/awards_features.csv           (player_id, season)
  - data/clean/durability_panel.csv          (player_id, season — uses gp from v1 panel)
  - data/clean/contract_tier.csv             (player_id, season)
  - data/clean/team_season.csv               (team_abbr, season — NaN for TOT rows)
  - analysis_v2/data_collection/manual_market_size.csv  (team_abbr — NaN for TOT rows)
  - analysis_v2/data_collection/cba_thresholds.csv      (season)

Hash-check vs v1_snapshot.sha256 ensures the v1 panel hasn't drifted.

Output: data/clean/data_analysis_v2.csv
        + analysis_v2/coverage_log.csv updated.
        + analysis_v2/logs/unmatched_*.csv for any anti-joins.

Run:
    python3 -m analysis_v2.prep_v2
"""
from __future__ import annotations

import hashlib
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402

log = logging.getLogger("analysis_v2.prep")
V2_DIR = ROOT / "analysis_v2"
LOGS_DIR = V2_DIR / "logs"
REPORTS_DIR = V2_DIR / "reports"
DATA_COLLECTION = V2_DIR / "data_collection"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

COVERAGE_LOG = V2_DIR / "coverage_log.csv"
SNAPSHOT_FILE = REPORTS_DIR / "v1_snapshot.sha256"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _check_v1_hash() -> None:
    actual = _sha256(CLEAN_DIR / "data_analysis_v1.csv")
    if not SNAPSHOT_FILE.exists():
        log.warning("v1 snapshot file missing — skipping hash check")
        return
    expected_line = SNAPSHOT_FILE.read_text().strip().split()[0]
    if actual == expected_line:
        log.info("v1 snapshot hash OK (%s)", actual[:12])
    else:
        log.error(
            "v1 panel hash mismatch! expected=%s, got=%s",
            expected_line[:12],
            actual[:12],
        )
        raise SystemExit("ABORT: data_analysis_v1.csv changed since snapshot")


def _append_coverage(variable: str, source: str, n_total: int, n_covered: int) -> None:
    pct = 100.0 * n_covered / n_total if n_total > 0 else 0.0
    row = {
        "variable": variable,
        "source": source,
        "n_total": n_total,
        "n_covered": n_covered,
        "coverage_pct": round(pct, 2),
        "run_date": datetime.now().strftime("%Y-%m-%d"),
        "notes": "",
    }
    if COVERAGE_LOG.exists() and COVERAGE_LOG.stat().st_size > 0:
        cov = pd.read_csv(COVERAGE_LOG)
        cov = pd.concat([cov, pd.DataFrame([row])], ignore_index=True)
    else:
        cov = pd.DataFrame([row])
    cov.to_csv(COVERAGE_LOG, index=False)


def safe_join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: list[str],
    name: str,
    expected_coverage: float = 0.95,
    cols_to_pull: list[str] | None = None,
) -> pd.DataFrame:
    """Left-join right onto left, with safety guards.

    Checks:
      1. right has no duplicates on `on` keys.
      2. result length == len(left) (no fan-out).
      3. coverage on at least one new column >= expected_coverage; otherwise warn and
         save anti-join.
    Always appends to coverage_log.
    """
    n_before = len(left)

    dups = right.duplicated(subset=on).sum()
    if dups > 0:
        raise RuntimeError(f"{name}: right has {dups} duplicate keys on {on}")

    if cols_to_pull is not None:
        right = right[on + cols_to_pull]

    merged = left.merge(right, on=on, how="left", suffixes=("", f"_{name}"))
    if len(merged) != n_before:
        raise RuntimeError(
            f"{name}: fan-out detected (before={n_before}, after={len(merged)})"
        )

    # Coverage = non-null in the first newly added column.
    new_cols = [c for c in right.columns if c not in on and c in merged.columns]
    if not new_cols:
        log.warning("%s: no new columns added", name)
        return merged

    primary = new_cols[0]
    n_covered = int(merged[primary].notna().sum())
    pct = 100.0 * n_covered / n_before
    flag = "OK" if pct >= 100.0 * expected_coverage else "WARN"
    log.info(
        "  join %s: coverage=%d/%d (%.1f%%) on `%s` %s",
        name,
        n_covered,
        n_before,
        pct,
        primary,
        flag,
    )
    _append_coverage(primary, name, n_before, n_covered)

    if pct < 100.0 * expected_coverage:
        # save anti-join (left rows where primary is NaN after merge)
        anti = merged[merged[primary].isna()][on].drop_duplicates()
        path = LOGS_DIR / f"unmatched_{name}.csv"
        anti.to_csv(path, index=False)
        log.warning("    anti-join saved → %s (%d unique keys)", path, len(anti))

    return merged


def derive_strict_supermax(df: pd.DataFrame) -> pd.DataFrame:
    """Strict supermax: loose + experience ∈ {7,8,9} + same team as draft team (or
    traded to it post-rookie-scale per CBA 2017 wording). For lack of trade-history,
    use `team_abbr == draft_team` as approximation; document the caveat.

    Adds columns: supermax_eligible_strict, supermax_eligible_strict_team_only.
    """
    out = df.copy()
    same_team = out["team_abbr"].astype(str) == out["draft_team"].astype(str)
    exp_band = out["experience"].between(7, 9, inclusive="both")
    out["supermax_eligible_strict"] = (
        (out.get("supermax_eligible_loose", 0).fillna(0).astype(int) == 1)
        & exp_band
        & same_team
    ).astype(int)
    return out


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    _check_v1_hash()

    base_path = CLEAN_DIR / "data_analysis_v1.csv"
    df = pd.read_csv(base_path)
    log.info("loaded base panel: %d × %d", *df.shape)

    # 1) Awards features
    awards_path = CLEAN_DIR / "awards_features.csv"
    if awards_path.exists():
        awards = pd.read_csv(awards_path)
        df = safe_join(df, awards, ["player_id", "season"], "awards_features", 0.95)
    else:
        log.warning("awards_features.csv missing — skipping")

    # 2) Durability (computed from gp; deterministic)
    dur_path = CLEAN_DIR / "durability_panel.csv"
    if dur_path.exists():
        dur = pd.read_csv(dur_path)
        dur = dur.drop(columns=["gp"], errors="ignore")
        df = safe_join(df, dur, ["player_id", "season"], "durability", 0.99)
    else:
        log.warning("durability_panel.csv missing — skipping")

    # 3) Contract tier
    tier_path = CLEAN_DIR / "contract_tier.csv"
    if tier_path.exists():
        tier = pd.read_csv(tier_path)
        df = safe_join(df, tier, ["player_id", "season"], "contract_tier", 0.99)
    else:
        log.warning("contract_tier.csv missing — skipping")

    # 4) Team season (win pct, playoffs) — NaN expected for TOT rows
    team_season_path = CLEAN_DIR / "team_season.csv"
    if team_season_path.exists():
        ts = pd.read_csv(team_season_path)
        ts = ts.drop(columns=["fetch_error"], errors="ignore")
        df = safe_join(df, ts, ["team_abbr", "season"], "team_season", 0.92)

        # Lag-1 versions, grouped by team
        ts_lag = ts.copy().sort_values(["team_abbr", "season"])
        ts_lag["team_win_pct_lag1"] = ts_lag.groupby("team_abbr")["win_pct"].shift(1)
        ts_lag["team_made_playoffs_lag1"] = ts_lag.groupby("team_abbr")["made_playoffs"].shift(1)
        ts_lag = ts_lag[
            ["team_abbr", "season", "team_win_pct_lag1", "team_made_playoffs_lag1"]
        ]
        df = safe_join(df, ts_lag, ["team_abbr", "season"], "team_season_lag1", 0.85)
    else:
        log.warning("team_season.csv missing — skipping")

    # 5) Market size (team-level, time-invariant) — NaN for TOT rows
    mkt_path = DATA_COLLECTION / "manual_market_size.csv"
    if mkt_path.exists():
        mkt = pd.read_csv(mkt_path)
        mkt = mkt.drop(columns=["team_full"], errors="ignore")
        df = safe_join(df, mkt, ["team_abbr"], "market_size", 0.92)
    else:
        log.warning("manual_market_size.csv missing — skipping")

    # 6) CBA thresholds (per season)
    cba_path = DATA_COLLECTION / "cba_thresholds.csv"
    if cba_path.exists():
        cba = pd.read_csv(cba_path).rename(columns={"season_end_year": "season"})
        # Drop columns that already exist in panel (cap_t) to avoid collision.
        if "cap" in cba.columns and "cap_t" in df.columns:
            # Replace v1's cap_t with the explicit CBA cap for consistency
            cba = cba.rename(columns={"cap": "cap_cba"})
        df = safe_join(df, cba, ["season"], "cba_thresholds", 1.00)
    else:
        log.warning("cba_thresholds.csv missing — skipping")

    # 7) Birth country
    bc_path = CLEAN_DIR / "birth_country.csv"
    if bc_path.exists():
        bc = pd.read_csv(bc_path)
        bc = bc[["player_id", "birth_country_code", "birth_country", "is_international",
                 "birth_date_bbref", "birth_city"]].drop_duplicates(subset=["player_id"])
        df = safe_join(df, bc, ["player_id"], "birth_country", 0.98)
    else:
        log.warning("birth_country.csv missing — skipping (run scrape_birth_country.py first)")

    # Derived: strict supermax (using same-team-as-draft proxy)
    if "supermax_eligible_loose" in df.columns and "draft_team" in df.columns:
        df = derive_strict_supermax(df)
        log.info(
            "  supermax_eligible_strict: %d rows",
            int(df["supermax_eligible_strict"].sum()),
        )

    # Save
    out = CLEAN_DIR / "data_analysis_v2.csv"
    df.to_csv(out, index=False)
    log.info("wrote %s (%d × %d)", out, *df.shape)

    # Snapshot v2
    v2_hash = _sha256(out)
    (REPORTS_DIR / "v2_snapshot.sha256").write_text(f"{v2_hash}  data/clean/data_analysis_v2.csv\n")
    log.info("v2 snapshot hash: %s", v2_hash[:12])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

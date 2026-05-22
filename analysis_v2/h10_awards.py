"""H10 — Awards channel: do All-NBA selections significantly raise salary
*beyond* current-season performance controls?

Specs (per plan3.md lines 156–161, with the M10a/M10b separation we agreed on):
  M10a — M1c_full as-is (all_nba_lag1 + career_all_nba_count + career_allstar_count, NO supermax)
         — this is the "standard awards channel" spec.
  M10a_robust — M1c with has_career_all_nba + multi_all_nba + has_career_allstar
         — same channel measured with binary indicators (more interpretable, less aging-vet contamination).
  M10b — M1c_full minus all_nba_lag1, plus supermax_eligible_loose
         — isolates the "verified elite eligibility" effect, avoiding r=0.78 collinearity.

  Event study around the FIRST All-NBA selection in panel window. For each player whose first
  All-NBA in our scrape is in {2014…2024}, compute τ = season − t* and create dummies for
  τ ∈ {−2, −1, 0, +1, +2, +3}. Pre-trend (τ = −2, −1) should be ≈ 0 (or controlled by Mincer);
  on-event (τ = 0) and lag-1 (τ = +1) should be significantly positive.

Output: analysis_v2/output/tables/h10_*.txt + h10_combined.csv + h10_event_study.csv

Run:
    python3 -m analysis_v2.h10_awards
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis_v2.m1_full import (  # noqa: E402
    AGE_BLOCK, AWARDS_BLOCK, DEMO_BLOCK_BASE, DURABILITY_BLOCK, INTL_BLOCK,
    STATS_BLOCK, STRUCT_BLOCK, TEAM_BLOCK, add_features, combine_models,
    panel_index, prep_for_full, save_summary,
)

log = logging.getLogger("analysis_v2.h10")
OUT_DIR = ROOT / "analysis_v2" / "output" / "tables"


def fit_panel(d_indexed: pd.DataFrame, regs: list[str], name: str):
    d2 = d_indexed.dropna(subset=regs + ["ln_salary"])
    y = d2["ln_salary"]
    X = sm.add_constant(d2[regs].astype(float))
    res = PanelOLS(y, X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(res, name)
    log.info("%s: N=%d, R²=%.4f", name, int(res.nobs), res.rsquared)
    return res


def build_event_time(df: pd.DataFrame, awards_full: pd.DataFrame) -> pd.DataFrame:
    """For each player, find first season with all_nba_team > 0. Compute τ = season − t*.
    Use awards_panel_full so first All-NBA before 2016 also is detected (e.g. Curry t*=2014).
    """
    first_anba = (
        awards_full[awards_full["all_nba_team"] > 0]
        .groupby("player_id")["season"].min().rename("first_anba_season")
    )
    out = df.merge(first_anba, on="player_id", how="left")
    out["tau"] = out["season"] - out["first_anba_season"]
    return out


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = add_features(df)
    df["supermax_eligible_loose"] = df["supermax_eligible_loose"].fillna(0).astype(int)
    d = prep_for_full(df)
    log.info("sample: %d rows", len(d))
    di = panel_index(d)

    base_no_awards = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK
        + [c for c in STRUCT_BLOCK if c not in ("post_cba_2017", "post_covid")]
        + ["top5_market"]
    )

    # ---- M10a — standard cumulative awards (== M1c_full) -------------------
    m10a = fit_panel(di, base_no_awards + AWARDS_BLOCK, "h10a_cumulative")

    # ---- M10a_robust — binary awards indicators ----------------------------
    m10a_r = fit_panel(
        di,
        base_no_awards + ["all_nba_lag1", "has_career_all_nba",
                           "multi_all_nba", "has_career_allstar"],
        "h10a_robust_binary",
    )

    # ---- M10b — supermax_eligible_loose substitution -----------------------
    m10b = fit_panel(
        di,
        base_no_awards + ["supermax_eligible_loose", "career_allstar_count"],
        "h10b_supermax_eligible",
    )

    combine_models(
        {
            "M10a (cumulative)": m10a,
            "M10a_robust (binary)": m10a_r,
            "M10b (supermax_eligible)": m10b,
        },
        OUT_DIR / "h10_combined.csv",
    )

    # ----------------- Event study around first All-NBA --------------------
    awards_full = pd.read_csv(ROOT / "data" / "clean" / "awards_panel_full.csv")
    d_ev = build_event_time(d.reset_index(drop=True), awards_full)

    # Window: τ ∈ {-2, -1, 0, +1, +2, +3}. Reference: τ < -2 OR no all-NBA at all.
    for tau in [-2, -1, 0, 1, 2, 3]:
        d_ev[f"tau_{tau:+d}"] = (d_ev["tau"] == tau).astype(int)
    d_ev["tau_4plus"] = (d_ev["tau"] >= 4).astype(int)
    event_cols = ["tau_-2", "tau_-1", "tau_+0", "tau_+1",
                  "tau_+2", "tau_+3", "tau_4plus"]

    # Only keep rows where player has a first_anba in our awards data (else they're
    # never-treated controls — fine to include with all tau dummies = 0).
    di_ev = panel_index(d_ev)
    es_regs = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK
        + [c for c in STRUCT_BLOCK if c not in ("post_cba_2017", "post_covid")]
        + ["top5_market", "career_allstar_count"]
        + event_cols
    )
    es = fit_panel(di_ev, es_regs, "h10_event_study")

    # Save event-study coefficients separately
    es_rows = []
    for col in event_cols:
        if col in es.params.index:
            es_rows.append({
                "tau": col.replace("tau_", "").replace("+0", "0"),
                "beta": float(es.params[col]),
                "se": float(es.std_errors[col]),
                "p": float(es.pvalues[col]),
                "ci_lo": float(es.conf_int().loc[col, "lower"]),
                "ci_hi": float(es.conf_int().loc[col, "upper"]),
            })
    es_df = pd.DataFrame(es_rows)
    es_df.to_csv(OUT_DIR / "h10_event_study.csv", index=False)
    log.info("\nEvent study around first All-NBA:\n%s", es_df.to_string(index=False))

    # ---- Notes
    notes = [
        "# H10 — Awards channel: discussion notes\n\n",
        f"Sample: {int(m10a.nobs)} player-seasons.\n\n",
        "## Three spec headline results\n\n",
        "M10a (cumulative cumsums) — see m1_full_notes for coefficients.\n\n",
        "**M10a_robust (binary indicators)** — cleaner interpretation:\n",
    ]
    for var in ["all_nba_lag1", "has_career_all_nba", "multi_all_nba",
                 "has_career_allstar"]:
        if var in m10a_r.params.index:
            b = m10a_r.params[var]
            se = m10a_r.std_errors[var]
            p = m10a_r.pvalues[var]
            notes.append(f"- {var}: β = {b:+.4f}, SE = {se:.4f}, p = {p:.4f}\n")
    notes.append("\n**M10b (supermax_eligible_loose substitution):**\n")
    for var in ["supermax_eligible_loose", "career_allstar_count"]:
        if var in m10b.params.index:
            b = m10b.params[var]
            se = m10b.std_errors[var]
            p = m10b.pvalues[var]
            notes.append(f"- {var}: β = {b:+.4f}, SE = {se:.4f}, p = {p:.4f}\n")

    notes.append("\n## Event study around first All-NBA (τ in years)\n\n")
    notes.append("Pre-event years (τ < 0) should be close to 0 — no anticipation.\n")
    notes.append("Lag-1 (τ = +1) is the headline: salary jump *after* first All-NBA,\n")
    notes.append("conditional on contemporaneous performance.\n\n")
    for r in es_rows:
        sig = "***" if r["p"] < 0.01 else "**" if r["p"] < 0.05 else "*" if r["p"] < 0.10 else ""
        notes.append(
            f"- τ = {r['tau']:>4}: β = {r['beta']:+.4f}, "
            f"CI95 = [{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}]{sig}\n"
        )

    (ROOT / "analysis_v2" / "reports" / "h10_notes.md").write_text(
        "".join(notes), encoding="utf-8"
    )
    log.info("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

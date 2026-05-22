"""H11 — Durability + M_full (combined) + Oster sensitivity.

Specs (per plan3.md day 7):
  M11a — M1c_full + games_missed_lag1 (already in M1c_full as main effect)
  M11b — M1c_full + games_missed_lag1 + games_missed_lag1 × age
         Tests "durability discount intensifies with age" — older players are penalised more
         for the same missed games (signal of decline becomes stronger).
  M_full — Combined: everything from M1c_full + tier dummies + supermax_eligible_loose
         Final picture. R² should match h9b approximately.
  Oster sensitivity (δ=1, R_max = 1.3 · R²_obs) for key new coefficients.
  Multiple-testing correction (Bonferroni and Benjamini-Hochberg FDR) on the 10-hypothesis set.

Output:
  analysis_v2/output/tables/h11_*.txt
  analysis_v2/output/tables/oster_sensitivity.csv
  analysis_v2/output/tables/multiple_testing_corrections.csv
  analysis_v2/reports/phase3_summary.md

Run:
    python3 -m analysis_v2.h11_durability
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

from analysis_v2.h9_tier import REFERENCE_TIER, TIERS, add_tier_dummies  # noqa: E402
from analysis_v2.m1_full import (  # noqa: E402
    AGE_BLOCK, AWARDS_BLOCK, DEMO_BLOCK_BASE, DURABILITY_BLOCK, INTL_BLOCK,
    STATS_BLOCK, STRUCT_BLOCK, TEAM_BLOCK, add_features, combine_models,
    panel_index, prep_for_full, save_summary,
)

log = logging.getLogger("analysis_v2.h11")
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


def oster_delta(
    d: pd.DataFrame,
    controls_restricted: list[str],
    controls_full: list[str],
    target: str,
    R_max_multiplier: float = 1.3,
) -> dict:
    """Compute Oster (2019) δ-statistic: the strength of selection on unobservables
    relative to selection on observables that would explain away the coefficient.

    δ = 1 ⇒ unobservables would have to be equally important as observables to nullify
    the effect. δ > 1 considered "robust". δ ≤ 1 considered "fragile".

    Closed-form approximation per Oster (2019), eq. (3):
        δ ≈ (β̃ − β̂) · (R_max − R̂) / [(β̇ − β̃) · (R̂ − Ṙ)]
    where:
        β̇, Ṙ = uncontrolled (target only)
        β̃, R̃ = restricted (with `controls_restricted`)
        β̂, R̂ = full (with `controls_full`)
        R_max = R_max_multiplier · R̂
    """
    def _fit_ols(regs):
        sub = d.dropna(subset=regs + ["ln_salary"])
        y = sub["ln_salary"].values
        X = sm.add_constant(sub[regs].astype(float))
        res = sm.OLS(y, X).fit()
        return float(res.params.get(target, np.nan)), float(res.rsquared)

    if target not in d.columns:
        return {"target": target, "delta": np.nan, "notes": "target column missing"}

    b_dot, r_dot = _fit_ols([target])
    b_tilde, r_tilde = _fit_ols([target] + controls_restricted)
    b_hat, r_hat = _fit_ols([target] + controls_full)
    R_max = R_max_multiplier * r_hat

    numer = (b_tilde - b_hat) * (R_max - r_hat)
    denom = (b_dot - b_tilde) * (r_hat - r_dot)
    if denom == 0 or not np.isfinite(denom):
        delta = np.nan
    else:
        delta = numer / denom
    return {
        "target": target,
        "beta_uncontrolled": b_dot,
        "beta_restricted": b_tilde,
        "beta_full": b_hat,
        "R2_uncontrolled": r_dot,
        "R2_restricted": r_tilde,
        "R2_full": r_hat,
        "R_max": R_max,
        "delta": delta,
        "robust": "yes" if (np.isfinite(delta) and abs(delta) >= 1) else "no",
    }


def bh_fdr(p_values: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """Benjamini-Hochberg FDR adjusted thresholds. Returns boolean reject array."""
    n = len(p_values)
    order = np.argsort(p_values)
    ranked = p_values[order]
    thresh = alpha * (np.arange(1, n + 1) / n)
    passing = ranked <= thresh
    if not passing.any():
        return np.zeros(n, dtype=bool)
    cutoff_rank = np.where(passing)[0].max()
    reject_sorted = np.zeros(n, dtype=bool)
    reject_sorted[: cutoff_rank + 1] = True
    reject = np.zeros(n, dtype=bool)
    reject[order] = reject_sorted
    return reject


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = add_features(df)
    df["supermax_eligible_loose"] = df["supermax_eligible_loose"].fillna(0).astype(int)
    d = prep_for_full(df)
    d, tier_cols = add_tier_dummies(d)
    di = panel_index(d)

    base = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK + AWARDS_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK
        + [c for c in STRUCT_BLOCK if c not in ("post_cba_2017", "post_covid")]
        + ["top5_market"]
    )

    # ---- M11a is already M1c_full; rerun for record
    m11a = fit_panel(di, base, "h11a_durability_main")

    # ---- M11b: durability × age interaction
    di["games_missed_x_age"] = di["games_missed_lag1"] * di["age"]
    m11b = fit_panel(di, base + ["games_missed_x_age"], "h11b_durability_x_age")

    # ---- M_full: everything (M1c + tier + supermax_eligible_loose)
    m_full = fit_panel(
        di,
        base + tier_cols + ["supermax_eligible_loose"],
        "M_full",
    )

    combine_models(
        {
            "M11a (durability main)": m11a,
            "M11b (durability × age)": m11b,
            "M_full (combined)": m_full,
        },
        OUT_DIR / "h11_combined.csv",
    )

    # ---- Oster sensitivity for key new coefficients ------------------------
    log.info("computing Oster sensitivity…")
    minimal_controls = ["ppg", "age", "age_sq", "experience"]
    full_controls = base  # M1c_full controls minus target
    oster_targets = [
        "all_nba_lag1",
        "top5_market",
        "supermax_eligible_loose",
        "games_missed_lag1",
        "has_career_allstar",
        "multi_all_nba",
    ]
    osters = []
    for tgt in oster_targets:
        if tgt not in d.columns:
            continue
        rc = [c for c in minimal_controls if c != tgt]
        fc = [c for c in full_controls if c != tgt]
        result = oster_delta(d, rc, fc, tgt)
        osters.append(result)
        log.info(
            "  %-24s δ = %s  (β_full = %s)",
            tgt,
            f"{result['delta']:+.3f}" if np.isfinite(result["delta"]) else "NA",
            f"{result['beta_full']:+.4f}",
        )
    pd.DataFrame(osters).to_csv(OUT_DIR / "oster_sensitivity.csv", index=False)

    # ---- Multiple-testing correction across 10 hypotheses ------------------
    log.info("multiple-testing correction across hypotheses…")
    headline_tests = []
    # H1: ppg matters → use M11a coef
    # H2-H6: from v1 (cba/covid/tax/age/experience/contract-year — already published)
    # We focus correction on the new H8-H11 results.
    rows = [
        ("H7 allstar (M1c_full)", "allstar", m11a),
        ("H8a market top5", "top5_market", m11a),
        ("H9 tier supermax (M_full)", "tier_supermax", m_full),
        ("H9 tier max_35 (M_full)", "tier_max_35", m_full),
        ("H9 tier rookie_scale (M_full)", "tier_rookie_scale", m_full),
        ("H9 tier minimum (M_full)", "tier_minimum", m_full),
        ("H10 all_nba_lag1", "all_nba_lag1", m11a),
        ("H10 career_allstar_count", "career_allstar_count", m11a),
        ("H10 supermax_elig (M_full)", "supermax_eligible_loose", m_full),
        ("H11 games_missed_lag1", "games_missed_lag1", m11a),
        ("H11 games_missed × age", "games_missed_x_age", m11b),
    ]
    for label, var, res in rows:
        if var not in res.params.index:
            continue
        headline_tests.append({
            "hypothesis": label,
            "variable": var,
            "beta": float(res.params[var]),
            "se": float(res.std_errors[var]),
            "p_raw": float(res.pvalues[var]),
        })
    h_df = pd.DataFrame(headline_tests)
    n = len(h_df)
    alpha = 0.05
    h_df["bonf_threshold"] = alpha / n
    h_df["bonf_reject"] = h_df["p_raw"] <= h_df["bonf_threshold"]
    h_df["bh_fdr_reject"] = bh_fdr(h_df["p_raw"].values, alpha=alpha)
    h_df.to_csv(OUT_DIR / "multiple_testing_corrections.csv", index=False)
    log.info("\n%s", h_df.to_string(index=False))

    # ---- phase3_summary.md ------------------------------------------------
    summary = [
        "# Phase 3 — econometric summary\n\n",
        f"Sample: 2268 player-seasons (3660 − TOT/early lag).\n\n",
        "## Model specifications and R²\n\n",
        f"- M1c_full           : R² = 0.6510  (extended Mincer + Awards + Market + Durability + Team)\n",
        f"- M1c_full_robust_awards : R² = 0.6518  (binary indicators replace cumulative)\n",
        f"- M9a (pure tier)    : R² = 0.8489  (institutional layer alone)\n",
        f"- M9b (full + tier)  : R² = 0.8623  (tier adds +0.21 R² over M1c_full)\n",
        f"- M11b (durability × age) : R² = {m11b.rsquared:.4f}\n",
        f"- M_full (everything): R² = {m_full.rsquared:.4f}\n\n",
        "## Hypothesis status (10 hypotheses, after BH-FDR @ 5%)\n\n",
    ]
    for _, r in h_df.iterrows():
        verdict = "✅ rejected" if r["bh_fdr_reject"] else "❌ not rejected"
        summary.append(
            f"- **{r['hypothesis']}** (β = {r['beta']:+.4f}, p = {r['p_raw']:.4f}): "
            f"{verdict}\n"
        )

    summary.append("\n## Oster sensitivity (δ ≥ 1 = robust)\n\n")
    for o in osters:
        delta_s = f"{o['delta']:+.3f}" if np.isfinite(o['delta']) else "NA"
        summary.append(
            f"- {o['target']}: β_full = {o['beta_full']:+.4f}, δ = {delta_s} ({o['robust']})\n"
        )

    summary.append("\n## Key content findings (for Chapter 4–5)\n\n")
    summary.extend([
        "1. **Performance + Age = 65.5% of explained variance** (Shapley). Mincer-structure dominant.\n",
        "2. **Awards = 12.2%** explained variance (Shapley) — formal recognition has real pricing weight.\n",
        "3. **Tier dummies alone give R² = 0.85** — CBA structure pseudo-deterministic.\n",
        "4. **top5_market β ≈ −0.10** — anti-marketability (consistent with Hembre 2021); interaction "
        "with allstar/intl is not significant → uniform discount.\n",
        "5. **Awards channel via event study**: 22% jump 2–3 years post-first-All-NBA, "
        "consistent with contract-cycle dynamics.\n",
        "6. **Aging-veteran discount**: multi_all_nba (≥3) carries β = −0.22 — past-elite status "
        "underprices current performance for ageing legends.\n",
        "7. **Durability**: games_missed_lag1 β = −0.005 (per game). 30-game miss = −15% salary.\n",
        "8. **Team controls null**: win_pct_lag1, made_playoffs_lag1, over_luxury_tax all p > 0.15. "
        "Team success doesn't transfer to individual price.\n",
    ])
    (ROOT / "analysis_v2" / "reports" / "phase3_summary.md").write_text(
        "".join(summary), encoding="utf-8"
    )
    log.info("DONE — phase3_summary.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""H9 — Contract-tier structure: does institutional pricing (CBA tiers) explain
salary variation beyond performance?

Specs (per plan3.md lines 145–149):
  M9a — Demo + Awards + Struct + tier dummies (NO performance stats)
        → pure tier effect; baseline for institutional pricing power.
  M9b — M1c_full (Performance + ...) + tier dummies
        → marginal R² gain from tiers after controlling performance.
  M9c — M9b + tier × supermax_eligible_loose interactions
        → does eligibility shift the within-tier pricing?

Plus tier-specific regressions: fit Mincer (Performance + Age) within each tier separately,
showing β_ppg(tier). Expected pattern: high inside mid_level (market zone), low inside
max_25/30/35 (truncated by cap) and rookie_scale (slotted).

Reference tier: mid_level (representative middle-class zone).

Output: analysis_v2/output/tables/h9_tier_*.txt + h9_tier_combined.csv
        analysis_v2/output/tables/h9_tier_specific_betas.csv

Run:
    python3 -m analysis_v2.h9_tier
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

log = logging.getLogger("analysis_v2.h9")
OUT_DIR = ROOT / "analysis_v2" / "output" / "tables"

TIERS = ["minimum", "rookie_scale", "mid_level", "high_mid",
         "max_25", "max_30", "max_35", "supermax", "overpay"]
REFERENCE_TIER = "mid_level"


def add_tier_dummies(d: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    out = d.copy()
    cols: list[str] = []
    for t in TIERS:
        if t == REFERENCE_TIER:
            continue
        col = f"tier_{t}"
        out[col] = (out["contract_tier"] == t).astype(int)
        cols.append(col)
    return out, cols


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


def fit_pooled(d: pd.DataFrame, regs: list[str]):
    """Tier-specific regression on a subset; OLS with cluster SE on player_id."""
    sub = d.dropna(subset=regs + ["ln_salary"])
    if len(sub) < len(regs) + 5:
        return None
    y = sub["ln_salary"].values
    X = sm.add_constant(sub[regs].astype(float))
    return sm.OLS(y, X).fit(
        cov_type="cluster", cov_kwds={"groups": sub["player_id"].values}
    )


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = add_features(df)
    # supermax_eligible_loose imputation: NaN if not joined (shouldn't be)
    df["supermax_eligible_loose"] = df["supermax_eligible_loose"].fillna(0).astype(int)
    d = prep_for_full(df)
    d, tier_cols = add_tier_dummies(d)
    log.info("sample: %d rows, tier dummies: %d", len(d), len(tier_cols))

    # Distribution check
    log.info("tier distribution in regression sample:")
    log.info("\n%s", d["contract_tier"].value_counts().to_string())

    di = panel_index(d)

    # ---- M9a: pure tier (no performance) -----------------------------------
    m9a_regs = (
        DEMO_BLOCK_BASE + INTL_BLOCK + AGE_BLOCK + AWARDS_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK + [c for c in STRUCT_BLOCK if c not in
                                            ("post_cba_2017", "post_covid")]
        + tier_cols
    )
    m9a = fit_panel(di, m9a_regs, "h9a_pure_tier")

    # ---- M9b: M1c_full + tier dummies --------------------------------------
    m9b_regs = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK + AWARDS_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK + [c for c in STRUCT_BLOCK if c not in
                                            ("post_cba_2017", "post_covid")]
        + ["top5_market"] + tier_cols
    )
    m9b = fit_panel(di, m9b_regs, "h9b_full_plus_tier")

    # ---- M9c: M9b + tier × supermax_eligible_loose --------------------------
    # Only meaningful for tiers where supermax_eligible can matter: max_30, max_35, supermax.
    # Only tier_max_30 has variation in eligibility (26/50 eligible). tier_supermax is
    # perfectly collinear with eligibility by classifier design. tier_max_35 has zero
    # eligible cases in panel (all max_35 are 10+ yr veterans on standard max).
    di["tier_max_30_x_supereligible"] = (
        di["tier_max_30"] * di["supermax_eligible_loose"]
    )
    inter_cols = ["tier_max_30_x_supereligible"]
    m9c_regs = m9b_regs + ["supermax_eligible_loose"] + inter_cols
    m9c = fit_panel(di, m9c_regs, "h9c_tier_x_eligible")

    combine_models(
        {
            "M9a (pure tier)": m9a,
            "M9b (full + tier)": m9b,
            "M9c (tier × eligible)": m9c,
        },
        OUT_DIR / "h9_tier_combined.csv",
    )

    # ---- Tier-specific Mincer regressions -----------------------------------
    log.info("\nTier-specific regressions (β_ppg by tier):")
    rows = []
    perf_regs = STATS_BLOCK + AGE_BLOCK
    for t in TIERS:
        sub = d[d["contract_tier"] == t].copy()
        if len(sub) < 30:
            log.info("  %s: n=%d — skipping (too few)", t, len(sub))
            continue
        res = fit_pooled(sub, perf_regs)
        if res is None:
            continue
        try:
            b_ppg = res.params.get("ppg", np.nan)
            se_ppg = res.bse.get("ppg", np.nan)
            p_ppg = res.pvalues.get("ppg", np.nan)
            r2 = res.rsquared
        except Exception:
            b_ppg = se_ppg = p_ppg = r2 = np.nan
        rows.append({
            "tier": t,
            "n": len(sub),
            "beta_ppg": float(b_ppg),
            "se_ppg": float(se_ppg),
            "p_ppg": float(p_ppg),
            "R2_within_tier": float(r2),
        })
        log.info(
            "  %-14s n=%3d  β_ppg=%+.4f (SE %.4f, p=%.3f)  R²=%.3f",
            t, len(sub), b_ppg, se_ppg, p_ppg, r2,
        )
    pd.DataFrame(rows).to_csv(OUT_DIR / "h9_tier_specific_betas.csv", index=False)

    # ---- Notes
    notes = [
        "# H9 — Tier-structure hypothesis: discussion notes\n\n",
        f"Sample: {int(m9b.nobs)} player-seasons. Reference tier: {REFERENCE_TIER}.\n\n",
        "## Headline R² jumps (institutional pricing power)\n\n",
        f"- M1c_full R² (no tiers): 0.6510\n",
        f"- **M9a (pure tier, no performance) R²: {m9a.rsquared:.4f}** — institutional layer alone\n",
        f"- **M9b (M1c + tier) R²: {m9b.rsquared:.4f}** — full picture\n",
        f"- ΔR² from tier dummies on top of M1c: {m9b.rsquared - 0.6510:+.4f}\n\n",
        "## Tier dummy coefficients (M9b, reference = mid_level)\n\n",
    ]
    for col in tier_cols:
        if col in m9b.params.index:
            b = m9b.params[col]
            se = m9b.std_errors[col]
            p = m9b.pvalues[col]
            star = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
            notes.append(
                f"- **{col}**: β = {b:+.4f}, SE = {se:.4f}, p = {p:.4f}{star}\n"
            )
    notes.extend([
        "\n## Tier-specific β_ppg (truncation pattern)\n\n",
        "If institutional CBA structure suppresses performance-pricing in the top tiers (cap-truncation) "
        "and bottom tiers (rookie/min slot), then β_ppg should be highest inside `mid_level` and "
        "close to zero in `max_*` and `rookie_scale`.\n\n",
    ])
    for r in rows:
        notes.append(
            f"- {r['tier']:14s}: n={r['n']:3d}, β_ppg = {r['beta_ppg']:+.4f} (p={r['p_ppg']:.3f})\n"
        )
    (ROOT / "analysis_v2" / "reports" / "h9_notes.md").write_text("".join(notes), encoding="utf-8")
    log.info("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
